import json,re,copy
from pathlib import Path
P=Path('batches/final_batch_learn_python.region.06')
plan=json.loads((P/'tile_plans.json').read_text())
bundle=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
B={b['context']['concept_id']:b for b in bundle['bundles']}
registry=json.loads((P/'scenario_asset_registry.json').read_text())
A={a['asset_id']:a for a in registry['assets']}
# Each entry follows the source fact order. Values in examples come from sources below.
F={
'assert_statement':[
'In normal debugging execution, `assert condition, message` raises AssertionError if the condition is false.',
'Python can omit assertions with `-O`; they must not replace required production input checks.',
'For required runtime validation, use an explicit conditional and `raise`, not a removable assertion.'],
'iterables_and_iterators':[
'An iterable supplies an iterator through `iter(value)`. An iterator supplies successive items through `next(iterator)` and signals exhaustion with StopIteration.',
'Separate `iter(list_value)` calls have separate traversal state; the list stores reusable items.',
'Calling `iter` on an iterator returns that same iterator, not an independent traversal.',
'At exhaustion, `next(iterator, default)` returns the default instead of raising StopIteration.'],
'generator_functions':[
'Calling a function containing `yield` creates a generator iterator. Advancing it runs to the next yield.',
'`yield value` supplies one item and suspends execution, retaining local state until the next advance.',
'Inside the function, use a for loop and condition to yield accepted items. Reaching the function’s end terminates iteration.'],
'generator_expressions':[
'`(expression for item in iterable if condition)` lazily transforms accepted items. The filtering if clause is optional.',
'The leftmost iterable expression is evaluated immediately; filtering and item transformations happen during iteration.',
'As the sole argument to `sum`, a generator expression totals transformed values without an intermediate list.'],
'iterator_consumption_and_exhaustion':[
'Each `next(iterator)` consumes an item. A later traversal or consumer sees only what remains.',
'Once an iterator raises StopIteration, subsequent calls must continue to raise it.',
'`iter(iterator)` returns the same iterator; it does not reset progress.',
'For another pass over a reusable collection, obtain a fresh iterator from the collection, not its exhausted iterator.'],
'eager_vs_lazy_processing':[
'`list(iterable)` materializes remaining items into a list that supports repeated traversal.',
'Generator expressions compute as consumed and tend to use less memory than equivalent list comprehensions.',
'For a one-pass total, `sum(expression for item in iterable)` avoids an intermediate transformed list.',
'An iterator advances by consuming items and stays exhausted after completion. Reuse may require a stored collection or new source traversal.'],
'itertools_utilities':[
'After `from itertools import chain`, `chain(first, second)` exhausts the first input before traversing the second, without first concatenating them into a list.',
'`sum(chain(first, second))` totals numeric items from that combined traversal.'],
'map_and_filter':[
'`map(function, iterable)` lazily applies a callable to successive items, yielding results.',
'`filter(predicate, iterable)` lazily keeps items whose predicate is true; `filter(None, iterable)` keeps truthy items.',
'`filter(predicate, iterable)` corresponds to `(item for item in iterable if predicate(item))`.',
'`[function(item) for item in iterable if predicate(item)]` materializes a transform-and-filter list; it can replace a map/filter composition when clearer.',
'To preserve lazy traversal, use a parenthesized generator expression rather than a list comprehension.'],
'unittest_test_cases':[
'After `import unittest`, subclass `unittest.TestCase` and name methods `test_*` to express individual supplied checks.',
'Use `self.assertEqual(actual, expected)` for equality and `self.assertTrue(condition)` for a required true condition.',
'Place the supplied failing operation inside `with self.assertRaises(ExceptionType):` to check its expected exception.'],
'unittest_execution_and_results':[
'`python -m unittest test_module` runs a named module; `python -m unittest discover` invokes discovery.',
'Discovery defaults to the current directory and `test*.py`; `-s` selects a starting directory and `-p` a filename pattern.',
'A failure is an unsuccessful assertion. The report identifies the test and failed-assertion traceback.',
'An error is an unexpected exception during a test, rather than an explicitly failed assertion.',
'The reported count tells how many tests ran. Zero supplies no executed checks of the helper’s behavior.'],
'unittest_setup_and_teardown':[
'`setUp(self)` initializes fresh state before each test method; setup errors prevent that method from running.',
'After successful setup, `tearDown(self)` runs after the test, even when the test fails.',
'`self.addCleanup(function, *args, **kwargs)` registers actions that run after tearDown or failed setup, in reverse registration order.',
'After acquiring the supplied resource, register its release callable. Store mutable data on self in setUp, not shared class attributes.'],
'read_generated_code':[
'Trace each input through the conditions to its actual return. A path reaching the function’s end without return produces None.',
'Track assignments and selected branches in order for valid and invalid inputs to determine actual data and control flow.',
'Generated code can be mistaken. Check its behavior; generated form is not proof of correctness.'],
'review_generated_file_operations':[
'Opening in `w` mode truncates existing content. Inspect mode choices for unintended overwrites.',
'`Path.unlink()` removes the file or symbolic link at that path. Remove unintended unlink calls instead of executing them.',
'`Path.rename(target)` moves an entry and can replace an existing file on Unix. Inspect source and destination.',
'An absolute child replaces the preceding base path. A relative rename target uses the working directory. Trace actual destinations before execution.'],
'review_untrusted_input_and_execution':[
'`eval` evaluates Python expressions and can execute arbitrary code; do not use it for untrusted text.',
'`exec` executes supplied text or code objects and is unsafe for untrusted instructions.',
'A shell makes quoting and metacharacters a security responsibility. Inspect `shell=True` and untrusted command construction for injection risk.',
'Replace execution-based parsing with a matching parser: int or float for numeric text, json.loads for JSON. Validate values and handle malformed input.',
'Non-executing parsing is not unlimited resource safety. Limit untrusted JSON input size: malicious input can consume substantial CPU and memory.'],
'verify_generated_api_claims':[
'Compare a generated call’s name, arguments and expected result with the official API entry’s signature, keyword-only options and returned value.',
'Assistants can make mistakes about Python; plausible API claims need checking.',
'`help(object)` displays documentation for an available object, supporting inspection of its interface in the selected runtime.',
'Check the executing interpreter’s version before comparing version-specific documentation.'],
'review_generated_dependencies':[
'pip uses the Python Package Index by default. Browse it to check the named distribution before installing an unchecked suggestion.',
'Distribution and import package names need not match. Confirm the distribution in the project’s installation documentation.',
'`--index-url` changes the package index. Inspect the installation source as well as the name.',
'The standard library supplies modules for many common tasks. Check whether documented functionality meets the requirement before adding a dependency.',
'Assistant suggestions can be mistaken. Withhold installation when identity and documented use cannot be verified.'],
'accept_repair_or_reject_generated_code':[
'Generated code can be wrong. Test it rather than accepting it solely because an assistant generated it.',
'Failed assertions and unexpected exceptions identify behavior needing correction; they do not support unchanged acceptance.',
'Compare traced returns and supplied expectations with requirements. Accept only supported behavior; record correction for an addressable mismatch.',
'Reject execution that evaluates untrusted input or truncates a file contrary to requirements until those unsafe operations are removed or corrected.']}
contrasts={
'assert_statement':'Contrast an internal invariant with a required public input check: optimization must not remove the latter.',
'iterables_and_iterators':'Contrast a fresh list iterator with iter applied to an existing iterator: only the former gives independent progress.',
'generator_functions':'Contrast yielding an item with completing an ordinary return-style calculation: yield suspends and retains state.',
'generator_expressions':'Contrast evaluating the source expression now with transforming its items during iteration.',
'iterator_consumption_and_exhaustion':'Contrast a fresh pass from values with another pass from traversal: the exhausted traversal does not restart.',
'eager_vs_lazy_processing':'Contrast one-pass lazy consumption with repeated traversal of stored items.',
'itertools_utilities':'Contrast exhausting first before second with alternating between the batches: chain follows input order.',
'map_and_filter':'Contrast a materialized comprehension with a parenthesized expression that preserves lazy traversal.',
'unittest_test_cases':'Contrast checking an exception with comparing a return: the failing operation belongs inside assertRaises.',
'unittest_execution_and_results':'Contrast an assertion failure with an unexpected exception; a zero-test report checks neither behavior.',
'unittest_setup_and_teardown':'Contrast failed setup with a failed test after successful setup: only the latter runs tearDown, but registered cleanup covers both.',
'read_generated_code':'Contrast intended behavior in a requirement with the path the helper actually takes.',
'review_generated_file_operations':'Contrast a reassuring variable name with the actual mode and resolved path.',
'review_untrusted_input_and_execution':'Contrast parsing data with executing instructions; a non-executing parser still needs validation and resource limits.',
'verify_generated_api_claims':'Contrast a confident generated claim with documentation for the actual object and interpreter version.',
'review_generated_dependencies':'Contrast a plausible package name with verified distribution identity and documented use.',
'accept_repair_or_reject_generated_code':'Contrast supported behavior with a mismatch or unsafe operation: generated origin justifies none of these decisions.'}
recaps={
'assert_statement':('Assertions are removable debugging checks; required input validation needs a conditional and raise.',[2,3]),
'iterables_and_iterators':('Lists store reusable items; separate list iterators track independent progress.',[2]),
'generator_functions':('Yield supplies an item, suspends execution and retains local state.',[2]),
'generator_expressions':('Evaluate the leftmost source immediately; filter and transform during iteration.',[2]),
'iterator_consumption_and_exhaustion':('Consumption does not reset: obtain a fresh collection iterator for another pass.',[1,3,4]),
'eager_vs_lazy_processing':('Materialize for repeated traversal; a one-pass total can avoid an intermediate list.',[1,3]),
'itertools_utilities':('Chain exhausts inputs in order; sum can total the combined traversal directly.',[1,2]),
'map_and_filter':('Map and filter are lazy; a list comprehension materializes, while a generator expression preserves laziness.',[1,2,4,5]),
'unittest_test_cases':('Use test_* methods with equality, truth and expected-exception assertions for supplied checks.',[1,2,3]),
'unittest_execution_and_results':('Distinguish failed assertions from unexpected exceptions; zero tests supply no executed checks.',[3,4,5]),
'unittest_setup_and_teardown':('Fresh setup isolates mutable state; registered cleanup also covers failed setup.',[1,3,4]),
'read_generated_code':('Trace actual branches and returns; reaching the end without return produces None.',[1,2]),
'review_generated_file_operations':('Inspect modes and resolved paths; remove unintended deletion before execution.',[1,2,3,4]),
'review_untrusted_input_and_execution':('Parse matching data instead of executing untrusted text; validate inputs and limit untrusted JSON size.',[1,2,4,5]),
'verify_generated_api_claims':('Compare API claims with the documented interface for the executing interpreter’s version.',[1,4]),
'review_generated_dependencies':('Verify distribution identity, documented use and source; check standard-library alternatives before installation.',[1,2,3,4,5]),
'accept_repair_or_reject_generated_code':('Accept supported behavior, correct addressable mismatches, and reject unsafe execution until corrected.',[2,3,4])}
def remedy_contrast(k,fs):
 ids={f.split('#')[-1] for f in fs}
 if k=='iterables_and_iterators' and ids=={'f4'}: return 'Contrast exhaustion with and without a default: the default form returns a fallback instead of raising StopIteration.'
 if k=='iterator_consumption_and_exhaustion' and ids=={'f1','f2'}: return 'Contrast the original collection with the consumed traversal: later consumers see only remaining items, and exhaustion persists.'
 if k=='unittest_execution_and_results':
  if ids=={'f1','f2'}:return 'Contrast a named-module command with discovery: discovery searches using its directory and filename-pattern settings.'
  if ids=={'f5'}:return 'Contrast intended discovery with executed checks: a zero count supplies no helper behavior evidence.'
 if k=='review_untrusted_input_and_execution' and ids=={'f3'}:return 'Contrast parsing data with constructing a shell command: shell quoting and metacharacters create an injection responsibility.'
 return contrasts[k]
def lin(c,fs,tbs,anchors=None):
 return {'concept_ids':[c],'fact_ids':fs,'teaching_block_ids':tbs,**({'anchors':anchors} if anchors else {})}
def tbids(c,fs):
 short={f.split('#')[-1] for f in fs}
 return [c+'#'+tb['id'] for tb in B[c]['teaching_blocks'] if short.intersection(tb['fact_ids'])]
def prose(text,L,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(L)}
def factblocks(c,fs,tbs=None):
 out=[]
 for f in fs:
  n=int(f.split('#f')[-1])-1
  permitted=tbids(c,[f]); permitted=[x for x in permitted if tbs is None or x in tbs]
  out.append(prose(F[c.split('.')[-1]][n],lin(c,[f],permitted)))
 return out
def sourcecode(c):
 for tb in B[c]['teaching_blocks']:
  matches=re.findall(r'```python\s*\n(.*?)```',tb['content'],re.S)
  if matches:return matches[0].rstrip()
 aid='ws.'+c.split('.')[-1]
 if aid in A:return A[aid]['files'][0]['content'].split('# TODO')[0].rstrip()
 return None
def cw(code,L,annotations=None):
 return {'type':'code_walkthrough','language':'python','code':code,'annotations':annotations or [],'reveal':'line_by_line','lineage':copy.deepcopy(L)}
def anno(code,needle,text):
 i=next(i for i,x in enumerate(code.splitlines(),1) if needle in x)
 return {'start_line':i,'end_line':i,'text':text}
def diagram(labels,L,title='Review map',kind='mapping',edges=None):
 return {'type':'diagram','diagram_kind':kind,'title':title,'nodes':[{'id':'n'+str(i),'label':x} for i,x in enumerate(labels)],'edges':edges or [],'alt_text':title+': '+'; '.join(labels),'lineage':copy.deepcopy(L)}
def side(left,right,L,ll,rl,takeaway):
 return {'type':'side_by_side','left':left,'right':right,'left_label':ll,'right_label':rl,'takeaway':takeaway,'lineage':copy.deepcopy(L)}
def visual(s):
 c=s['concept_ids'][0]; k=c.split('.')[-1]; v=s['planned_visual_block_type'];L=lin(c,s['fact_ids'],s['teaching_block_ids'],[c+'#visual'])
 if v=='code_walkthrough':
  code=sourcecode(c); annotations=[]
  details={
   'iterables_and_iterators':[('first =','Separate state from second.'),('second =','Independent list traversal.'),('iter(first)','Same iterator; no reset.')],
   'generator_functions':[('if value','Only accepted items reach yield.'),('yield value','Supply an item; suspend with local state retained.')],
   'generator_expressions':[('total =','Evaluate the leftmost source now; filter and transform as consumed.')],
   'iterator_consumption_and_exhaustion':[('next(traversal)','Consumes the next item.'),('iter(traversal)','Same traversal, not a restart.'),('iter(values)','Fresh pass over the reusable list.')],
   'eager_vs_lazy_processing':[('sum(lazy)','Consume lazy items.'),('list(lazy)','Only remaining items.'),('stored =','Materialize for repeated traversal.')],
   'itertools_utilities':[('list(chain','Display input-order traversal.'),('sum(chain','Total directly; no concatenated list required.')],
   'unittest_test_cases':[('class CostTests','TestCase subclass with test_* checks.'),('assertEqual','Actual, then expected.'),('with self.assertRaises','Indent the expected failing operation inside this context.')],
   'read_generated_code':[('if quantity','Trace the selected branch for each supplied input.'),('return quantity','Skipping this branch reaches the end without return.')],
   'review_generated_file_operations':[('output =','Absolute child replaces the base.'),('open(output','w truncates existing content.'),('path.unlink','Remove unintended deletion; do not try it.'),('source.rename','Relative target uses cwd; Unix can replace an existing file.')]
  }
  if k=='read_generated_code':code=A['ws.'+k]['files'][0]['content'].split('# TODO')[0].rstrip()
  if k=='review_untrusted_input_and_execution':
   # Unsafe proposals remain comments; the repaired parser is non-destructive.
   code=A['ws.'+k]['files'][0]['content'].split('# TODO')[0].rstrip()+'\ntry:\n    parsed = int(text)\nexcept ValueError:\n    quantity = None\nelse:\n    if parsed >= 0:\n        quantity = parsed'
   details[k]=[('eval(text)','Unsafe execution proposal: review only.'),('int(text)','Parse numeric text; handle malformed input.'),('parsed >=','Validate the required nonnegative value.')]
  for needle,text in details.get(k,[]):annotations.append(anno(code,needle,text))
  return cw(code,L,annotations)
 if v=='annotated_image':
  # No image asset is registered. Represent the supplied report UI as a labelled diagram.
  files={f['path']:f['content'] for f in A['ws.'+k]['files']}
  report=files['runner_report.txt'];zero=files['zero_test_report.txt']
  labels=['python -m unittest test_cost']+[x for x in report.splitlines() if x.startswith(('FAIL:', 'AssertionError:', 'Ran ', 'FAILED'))]+[x for x in zero.splitlines() if x.startswith(('Ran ','NO TESTS'))]
  return diagram(labels,L,'Named-module runner report and zero-test contrast','container')
 if v=='process_flow':
  labels=['setUp: acquire resource','Register release callable','setUp succeeds?','Test: pass or fail','tearDown','Registered cleanup: reverse registration order']
  edges=[{'from':'n0','to':'n1'},{'from':'n1','to':'n2'},{'from':'n2','to':'n3','label':'yes'},{'from':'n3','to':'n4'},{'from':'n4','to':'n5'},{'from':'n2','to':'n5','label':'no: skip test and tearDown'}]
  return {'type':'process_flow','direction':'TB','nodes':[{'id':'n'+str(i),'label':x} for i,x in enumerate(labels)],'edges':edges,'alt_text':'Successful setup: test, tearDown, registered cleanup. Failed setup: skip test and tearDown; run already registered cleanup.','lineage':L}
 if v=='side_by_side':
  if k=='map_and_filter':
   code=sourcecode(c)
   # Reuse definitions and input values from the glossary, rather than typing example data.
   prefix=code.split('lazy =')[0]
   left=cw(prefix+code[code.index('lazy ='):].split('print([double')[0].rstrip(),L)
   right=cw(prefix+'stored = [double(value) for value in values if positive(value)]\nlazy = (double(value) for value in values if positive(value))',L)
   return side(left,right,L,'Callable pipeline','Comprehension forms','List materializes; the parenthesized form stays lazy.')
  if k=='verify_generated_api_claims':
   claim=re.search(r'sorted\(records, key=quantity_key, reverse=True\)',B[c]['teaching_blocks'][3]['content']).group()
   left=cw(claim,L,[{'start_line':1,'end_line':1,'text':'Compare the name, arguments and claimed result with the actual interface.'}])
   right=cw('help(sorted)',L,[{'start_line':1,'end_line':1,'text':'Inspect available-object documentation; match the executing interpreter version.'}])
   return side(left,right,L,'Proposed call','Runtime documentation','Plausible wording is not an API specification.')
  if k=='review_generated_dependencies':
   left=diagram(['Proposed distribution','Proposed import name','Install command: inspect --index-url'],L,'Suggestion')
   right=diagram(['Python Package Index: verify identity','Project installation documentation: confirm names','Standard library: check necessity','Unverified identity or use: withhold installation'],L,'Verification')
   return side(left,right,L,'Suggestion to review','Evidence to seek','Verify before installation; do not install an unverifiable suggestion.')
  if k=='accept_repair_or_reject_generated_code':
   records=A['ws.'+k]['files'][1]['content'].strip().split('\n\n\n')
   # Evidence is copied verbatim from the authored registry, never recomputed or typed here.
   left=diagram([r.strip() for r in records],L,'Supplied versions and evidence','container')
   right=diagram(['Supported requirements and checks: accept','Failed assertion or unexpected exception: correct','Addressable behavior mismatch: correct','Untrusted evaluation or forbidden truncation: reject execution until corrected'],L,'Decision rules')
   return side(left,right,L,'Requirements, traces and tests','Evidence-based decision','Generated origin is not acceptance evidence.')
 raise ValueError((c,v))

out={'schema_version':plan['schema_version'],'kind':'screens_part','path_id':plan['path_id'],'batch_id':plan['batch_id'],'tiles':[]}
for t in plan['tiles']:
 title=' / '.join(B[c]['context']['concept_name'] for c in t['concept_ids'])
 tile={'tile_id':t['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 remsets={}; rem_index=0
 for ps in t['steps']:
  c=ps['concept_ids'][0];k=c.split('.')[-1];typ=ps['type']
  L={key:copy.deepcopy(ps[key]) for key in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']}
  s={'step_id':ps['step_id'],'type':typ,'concept_ids':ps['concept_ids'],'title':B[c]['context']['concept_name'],'lineage':L}
  if typ=='explainer':
   s['eyebrow']='Understand'; s['blocks']=factblocks(c,ps['fact_ids'],ps['teaching_block_ids'])
   if k=='assert_statement':
    s['blocks'].append(prose(B[c]['teaching_blocks'][3]['content'],lin(c,ps['fact_ids'],[c+'#tb4']),'example'))
   if ps['planned_visual_block_type']:s['blocks'].append(visual(ps))
   else:
    # A short contrast re-voices the example/misconception half of split explainers.
    if any(x.endswith('#tb4') for x in ps['teaching_block_ids']):
     s['blocks'].append(prose(contrasts[k],lin(c,ps['fact_ids'],ps['teaching_block_ids']),'misconception'))
  elif typ in ['check','hands_on']:
   s['eyebrow']='Check your understanding' if typ=='check' else 'Practice'
   if typ=='check':
    s['title']='Check: '+B[c]['context']['concept_name'];s['lede']='Read the supplied question and choose the response supported by the rules you just learned.'
   elif ps['planned_interaction_type'] in ['choice','classify']:
    s['title']='Review '+B[c]['context']['concept_name'].replace('Reviewing ','').replace('Verifying ','')
    s['lede']='Read the supplied excerpts in this step and judge which claims or proposed actions are correct, defective or unsafe.'
   else:
    s['title']='Practice: '+B[c]['context']['concept_name'];s['lede']=B[c]['practice_anchor']['objective']
   # Every distinct measured fact set gets a remediation destination; practice-only anchors use the concept facts.
   fs=list(ps['fact_ids'])
   if not fs:fs=[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]
   key=(c,tuple(sorted(fs)))
   if key not in remsets:
    rem_index+=1;rid=t['tile_id']+'.r'+str(rem_index).zfill(2);remsets[key]=rid
    rL=lin(c,fs,tbids(c,fs))
    tile['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':[c],'title':'Revisit: '+B[c]['context']['concept_name'],'eyebrow':'One contrast','blocks':factblocks(c,fs)+[prose(remedy_contrast(k,fs),rL,'misconception')],'lineage':rL})
  elif typ=='video':
   s['eyebrow']='Worked walkthrough';s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
  elif typ=='recap':
   s['title']='Takeaways';s['eyebrow']='Keep these distinctions';s['blocks']=[]
   for cid in t['concept_ids']:
    # Objectives are the plan's concept-level takeaways, phrased as independent text.
    bb=B[cid];facts=[cid+'#'+f['id'] for f in bb['coverage']['required_facts']]
    summary,indices=recaps[cid.split('.')[-1]]
    facts=[cid+'#f'+str(i) for i in indices]
    s['blocks'].append(prose(summary,lin(cid,facts,tbids(cid,facts)),'takeaway'))
   if t['next_tile_id']:
    nt=next(x for x in plan['tiles'] if x['tile_id']==t['next_tile_id'])
    nc=nt['concept_ids'][0]
    s['blocks'].append({'type':'up_next','title':B[nc]['context']['concept_name'],'text':B[nc]['coverage']['learning_objective']})
  tile['steps'].append(s)
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Tiles:',len(out['tiles']),'steps:',sum(len(t['steps']) for t in out['tiles']),'remediations:',sum(len(t['remediation_steps']) for t in out['tiles']))
