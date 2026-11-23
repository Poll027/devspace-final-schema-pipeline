import json, io, contextlib, ast, copy
from pathlib import Path
B=Path(__file__).parent
plan=json.loads((B/'tile_plans.json').read_text()); screens=json.loads((B/'screens.json').read_text()); registry=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
assets={a['asset_id']:a for a in registry['assets']}
version=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']['python']['version']
questions={}
def q(cid,n,prompt,options,correct,reasons,hint): questions[(cid,n)]=(prompt,options,correct,reasons,hint)
Z='python.zip_iteration'; A='python.aliasing_mutability_and_copying'; C='python.collections_utilities'; D='python.diagnostic_printing'; F='python.docstrings'
# Keys and displayed predictions are computed by executing the supplied snippets.
def run(code):
 ns={'__name__':'__main__'}; buf=io.StringIO()
 with contextlib.redirect_stdout(buf): exec(code,ns)
 return ns,buf.getvalue()
zsrc=assets['code.'+Z]['files'][0]['content'].split('\n\n')[0]+'\nfor label, quantity in zip(labels, quantities):\n    print(label, quantity)\n'
zns,zout=run(zsrc)
omitted=zns['labels'][len(zns['quantities']):]
q(Z,3,'Read this code. Which description accounts for every printed pair and any omitted label?\n```python\n'+zsrc+'```',[zout.strip()+f'\n{omitted[0]} is omitted because it has no corresponding quantity.',zout.strip()+f'\n{omitted[0]} is also printed with a missing quantity.', 'Only the first pair is printed; zip stops after one pair.'],0,['zip pairs corresponding entries and stops at the shorter input.','Default zip does not supply a missing value for an unmatched trailing entry.','zip visits all corresponding pairs, not just the first pair.'],'Compare the number of entries available in each input.')
asrc=assets['code.'+A]['files'][0]['content']
ans,_=run(asrc)
q(A,3,'Before repair, what is original after this helper call?\n```python\n'+asrc+'```',[repr(ans['original']),repr([[3,2]]),'The caller\'s list is unaffected because the helper uses the name items.'],0,['items and original refer to the shared list, so the append is visible to the caller.','No copy is made: the top-level append changes the caller\'s list.','Changing the name does not copy the object; mutation can remain visible to the caller.'],'Follow the object referred to by each name, not the name spelling.')
nested='original = [[3, 2]]\ncopied = original.copy()\ncopied[0][0] = 9\n'
nns,_=run(nested)
q(A,4,'Which result follows this nested update?\n```python\n'+nested+'```',[f'original = {nns["original"]}; copied = {nns["copied"]}', 'original = [[3, 2]]; copied = [[9, 2]]','original = [[9, 2]]; copied = [[3, 2]]'],0,['The separate outer lists still reference the same inner list.','A shallow copy does not make the existing inner list independent.','The update was made through copied, and that inner list remains shared with original.'],'Distinguish copying the outer list from copying its elements.')
csrc="from collections import Counter\ncounts = Counter(['blue', 'red', 'blue'])\npairs = counts.most_common(1)\n"
cns,_=run(csrc)
q(C,8,'Read the code. Which description gives the counts and a safe way to report the winning pair, including if counts were empty?\n```python\n'+csrc+'```',[f'Counts: {dict(cns["counts"])}. pairs is {cns["pairs"]}; check if pairs before unpacking pairs[0].',f'Counts: {dict(cns["counts"])}. most_common(1) returns the bare pair, so unpack pairs directly.',f'Counts: {dict(cns["counts"])}. Access pairs[0] unconditionally, even for an empty counter.'],0,['Counter counts occurrences; most_common returns a list whose first pair is accessed only when nonempty.','most_common(1) returns a list containing a pair, not a bare pair.','An empty counter returns an empty list; access its first pair only when nonempty.'],'Check the shape of the result as well as the empty-input rule.')
tiesrc="from collections import Counter\ncounts = Counter(['red', 'blue'])\npairs = counts.most_common(1)\n"
tns,_=run(tiesrc)
q(C,9,'Which pair is selected, and why?\n```python\n'+tiesrc+'```',[f'{tns["pairs"][0]!r}, because tied counts follow first encounter.',"('blue', 1), because labels are alphabetized.","No pair, because tied frequencies cannot be reported."],0,['Both counts are equal, so first encounter determines the selected pair.','Ties follow first encounter, not alphabetic label ranking.','most_common can return a pair for tied counts; it uses first encounter.'],'Look at the encounter order only after comparing the counts.')
dsrc="def convert_quantity(text):\n    text = ' 3 '\n    quantity = int(text)\n    return quantity\n"
q(D,3,'You want to observe the current text before conversion and the bound quantity afterward. Which placement is appropriate?\n```python\n'+dsrc+'```',['Put print("raw text", repr(text)) after text is reassigned and before int(text); put print("converted quantity", quantity) after quantity is bound. Remove both diagnostics when finished.','Print text only before its reassignment, and use that output to describe the later text.','Print quantity before quantity is bound, to observe the conversion result.'],0,['Each label observes state at the relevant execution point; removing the print calls removes temporary output.','A print before reassignment cannot reveal the later value.','Observe quantity after its binding, not before the value exists at that execution point.'],'Place each observation next to the binding or operation it is meant to inspect.')
dns,_=run("text = ' 3 '\nrepresentation = repr(text)\n")
q(D,4,'The helper has just assigned text = \' 3 \' and has not yet converted it. Which diagnostic best exposes the surrounding spaces and quotes, and what should happen when the diagnostic is no longer needed?',['Use print("raw text", repr(text)) now; remove that print when finished.','Use print("raw text", text) before the reassignment; keep it to describe the later text.','Use print("converted quantity", quantity) after conversion to expose the original string\'s surrounding spaces.'],0,['repr exposes string details at the relevant point, and the print call is temporary.','Ordinary display can obscure string details, and an earlier observation does not reveal a later binding.','The converted quantity is not the original represented text. Use a text observation before conversion.'],'Choose an observation of the string itself at its current binding.')
fbase=assets['code.'+F]['files'][0]['content']
q(F,7,'cost(quantity, unit_price) has a first-statement docstring describing its numeric arguments and returned product. Which operation displays both its signature and documentation?',['help(cost)','cost(3, 2)','Read a string placed after the return statement as the function\'s docstring.'],0,['help(function) displays its signature and documentation, including the docstring.','Calling cost computes its returned product; that is not documentation inspection.','The function\'s docstring is a string literal first in its body, not a later string.'],'Distinguish inspecting an interface from invoking its calculation.')
exercises={}
# Tests bundle any static criterion with a data-dependent observation so constant answers fail.
zstarter="first_label = 'notebook'\nlabels = [first_label, 'pen', 'pencil']\nquantities = [3, 2]\npairs = zip(labels, labels)\n\n# Repair the zip arguments above; retain this supplied two-variable loop.\nfor label, quantity in pairs:\n    print(label, quantity)\n\n# Add a comment identifying the omitted label and explaining the stopping rule.\n"
zsol=zstarter.replace('pairs = zip(labels, labels)', 'pairs = zip(labels, quantities)')+f'# {omitted[0]} is omitted: no corresponding quantity; zip stops at the shorter list.\n'
zexpr="[labels, any("+repr(omitted[0])+" in line.lower() and 'omitted' in line.lower() and ('shorter' in line.lower() or 'shortest' in line.lower()) and 'quantity' in line.lower() for line in open('main.py').read().splitlines() if line.lstrip().startswith('#'))]"
exercises[Z]=(zstarter,zsol,'Repair the pairs assignment in main.py so zip pairs labels with quantities rather than labels with themselves. Keep the supplied two-variable loop: label and quantity receive each corresponding pair, and print(label, quantity) displays it on its own line separated by a space. Add a comment naming the omitted label, saying it is omitted because it has no corresponding quantity, and explaining that zip stops at the shorter list. Keep the supplied inputs and loop unchanged.', [('stdout_equals',{}),('value_equals',{'expr':zexpr})], 'Compare what the two inputs represent and account for their different lengths.')
astarter=asrc+'\n# Repair the assignment inside append_copy; keep the other helper lines.\n'
asol=astarter.replace('copied = items\n','copied = items.copy()\n')
# function calls cover arbitrary outer contents; a post-call top-level append is verified by a probe.
aexpr="(changed.append([9]), [original, changed])[1]"
exercises[A]=(astarter,asol,'Repair append_copy by replacing its aliasing assignment with a shallow-copy operation before the existing append. Keep the caller input and the helper\'s append and return unchanged. original must remain unchanged while changed contains the appended [5]. A subsequent top-level append to changed must not change original; this repair does not make existing nested elements independent.', [('function_call',{'function':'append_copy','args':[[[3,2]]]}),('function_call',{'function':'append_copy','args':[[[9]]]}),('value_equals',{'expr':'[original, changed]'})], 'Separate the outer list before the top-level mutation, without claiming a deep copy.')
# A numeric scaffold input makes probes of the caller-visible lists sensitive to mutations.
astarter='first_quantity = 3\n'+astarter.replace('original = [[3, 2]]','original = [[first_quantity, 2]]')
asol='first_quantity = 3\n'+asol.replace('original = [[3, 2]]','original = [[first_quantity, 2]]')
exercises[A]=(astarter,asol,exercises[A][2],exercises[A][3]+[('value_equals',{'expr':aexpr})],exercises[A][4])
cstarter="from collections import Counter\nfirst_label = 'blue'\n\ndef report_labels(labels):\n    counts = Counter(labels)\n    pairs = []\n    # Replace pairs = [] with the request for the most common pair.\n    # Add the nonempty guard, unpack the first pair and print label, count.\n    return pairs\n\nreport_labels([first_label, 'red', first_label])\n"
csol=cstarter.replace('    pairs = []\n','    pairs = counts.most_common(1)\n    if pairs:\n        label, count = pairs[0]\n        print(label, count)\n')
exercises[C]=(cstarter,csol,'Complete the supplied report_labels scaffold. Build pairs with counts.most_common(1), check if pairs before unpacking label, count = pairs[0], and print(label, count) only inside that guard. Keep the supplied return pairs and final call. The starting call must report blue 2; empty input must produce no output and return []; ["red", "blue"] must report red 1 and return its one-pair list. Ties follow first encounter.', [('stdout_equals',{}),('function_call',{'function':'report_labels','args':[['blue','red','blue']]}),('function_call',{'function':'report_labels','args':[[]]}),('function_call',{'function':'report_labels','args':[['red','blue']]})], 'Request a list of pairs and guard access to its first entry.')
def capture_expr(arg):
 return "(lambda buf: (lambda cm: (cm.__enter__(), report_labels("+arg+"), cm.__exit__(None, None, None), buf.getvalue())[3])(__import__('contextlib').redirect_stdout(buf)))(__import__('io').StringIO())"
c_probe="[report_labels([first_label, 'red', first_label]), "+capture_expr("[]")+", "+capture_expr("['red', 'blue']")+"]"
e=exercises[C]
exercises[C]=(e[0],e[1],e[2],e[3]+[('value_equals',{'expr':c_probe})],e[4])
# The second copy preserves a clean final helper while retaining a runnable diagnostic stage.
dstarter="raw_quantity = 3\nspaced_text = ' ' + str(raw_quantity) + ' '\n\ndef inspect_quantity(text):\n    text = spaced_text\n    quantity = int(text)\n    return quantity\n\ndef convert_quantity(text):\n    text = spaced_text\n    quantity = int(text)\n    return quantity\n\ndebug_result = inspect_quantity('ignored')\nresult = convert_quantity('ignored')\n"
dsol=dstarter.replace("def inspect_quantity(text):\n    text = spaced_text\n    quantity = int(text)\n", "def inspect_quantity(text):\n    text = spaced_text\n    print('raw text', repr(text))\n    quantity = int(text)\n    print('converted quantity', quantity)\n")
dexpr="[result, debug_result, not any(isinstance(n, __import__('ast').Call) and isinstance(n.func, __import__('ast').Name) and n.func.id == 'print' for f in __import__('ast').parse(open('main.py').read()).body if isinstance(f, __import__('ast').FunctionDef) and f.name == 'convert_quantity' for n in __import__('ast').walk(f))]"
exercises[D]=(dstarter,dsol,'Work in two stages retained side by side. The supplied text-building line models the unexpected reassignment to spaced numeric text; do not edit that scaffold or the conversion and return. Add print("raw text", repr(text)) in inspect_quantity after reassignment and before conversion, then print("converted quantity", quantity) after conversion. The supplied debug call runs that temporary version. Keep convert_quantity as the final version with the diagnostic calls removed: it must still convert and return the same quantity with no diagnostic output. Keep the supplied debug_result and result calls; the whole program prints only the two labeled observations from inspect_quantity.', [('stdout_equals',{}),('value_equals',{'expr':dexpr}),('function_call',{'function':'convert_quantity','args':['9']}),('function_call',{'function':'convert_quantity','args':['2']})], 'Observe each value after its relevant binding, and preserve conversion behavior in the cleaned-up helper.')
fstarter=fbase+"\nquantity = 3\nunit_price = 2\n"
fsol=fstarter.replace('def cost(quantity, unit_price):\n','def cost(quantity, unit_price):\n    """Calculate an order cost.\n\n    Arguments are numeric quantity and unit_price.\n    Return their product.\n    """\n')+'\nhelp(cost)\n'
fexpr="[cost(quantity, unit_price), __import__('inspect').cleandoc(cost.__doc__), any(isinstance(n, __import__('ast').Expr) and isinstance(n.value, __import__('ast').Call) and isinstance(n.value.func, __import__('ast').Name) and n.value.func.id == 'help' and len(n.value.args) == 1 and isinstance(n.value.args[0], __import__('ast').Name) and n.value.args[0].id == 'cost' for n in __import__('ast').parse(open('main.py').read()).body)]"
exercises[F]=(fstarter,fsol,'Add a first-statement triple-quoted docstring to cost without changing return quantity * unit_price. Use the following documentation text (indent its detail lines by four spaces, as shown), which accurately describes this numeric helper without unsupported exception claims:\n```text\nCalculate an order cost.\n\n    Arguments are numeric quantity and unit_price.\n    Return their product.\n    \n```\nKeep the supplied quantity and unit_price inputs. After the definition add help(cost), run it, and inspect the signature and documentation. The concise summary and blank line must precede the calling details.', [('function_call',{'function':'cost','args':[3,2]}),('function_call',{'function':'cost','args':[2,5]}),('value_equals',{'expr':fexpr})], 'Put interface documentation first in the body and keep it consistent with the unchanged calculation.')
result={k:plan[k] for k in ['schema_version','path_id','batch_id']}; result['kind']='interactions_part'; result['tiles']=[]
for t in plan['tiles']:
 st=next(x for x in screens['tiles'] if x['tile_id']==t['tile_id']); rems=st.get('remediation_steps',[]); out={'tile_id':t['tile_id'],'interactions':[]}; seen=set(); checks=[x for x in t['steps'] if x['planned_interaction_type']]
 for i,s in enumerate(checks):
  cid=s['concept_ids'][0]; b=bundles[cid]; caps=[a.split('#assessment:')[1] for a in s['anchors'] if '#assessment:' in a]
  if not caps: caps=[a['capability'] for a in b['assessment_anchors']]
  measures=[{'concept_id':cid,**copy.deepcopy(next(a for a in b['assessment_anchors'] if a['capability']==cap))} for cap in caps]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'stretch' if s['type']=='hands_on' else ('intro' if cid not in seen else 'core'),'grading_mode':'client','standalone':s['type']=='check','measures':measures,'anchors':s['anchors']}
  if ix['type']=='choice':
   prompt,options,key,reasons,hint=questions[(cid,int(s['step_id'].rsplit('s',1)[1]))]
   ix['public']={'prompt':prompt,'options':[{'option_id':f'o{j+1}','text':x} for j,x in enumerate(options)],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':[f'o{key+1}'],'option_feedback':{f'o{j+1}':{'message':x} for j,x in enumerate(reasons)}}
   success=reasons[key]; failure='Review the stated rule and trace the supplied example again.'
  else:
   starter,solution,prompt,tests,hint=exercises[cid]
   ix['public']={'prompt':prompt,'runtime':{'kind':'python','version':version,'packages':[]},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'asset_mounts':[]},'constraints':{k:copy.deepcopy(b['practice_anchor']['live_code'][k]) for k in ['allowed_syntax','blocked_syntax']}}
   ns,stdout=run(solution); tt=[]
   # Compute every expected from executing the actual solution, never from memory.
   for j,(kind,spec0) in enumerate(tests):
    spec=copy.deepcopy(spec0)
    if kind=='stdout_equals': expected=stdout
    elif kind=='function_call':
     with contextlib.redirect_stdout(io.StringIO()): expected=ns[spec['function']](*spec.get('args',[]))
    else:
     # Native calculation uses an equivalent workspace file for file-reading probes.
     temp=B/'main.py'; temp.write_text(solution)
     expr=spec['expr'].replace("open('main.py')",f'open({str(temp)!r})')
     with contextlib.redirect_stdout(io.StringIO()): expected=eval(expr,ns)
     temp.unlink()
    spec['expected']=copy.deepcopy(expected)
    tt.append({'test_id':f't{j+1}','kind':kind,'spec':spec,'visible':True,'message_on_fail':hint})
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':tt}
   success=b['practice_anchor']['success']; failure='Check the requested behavior and keep the supplied scaffold unchanged.'
  ix['feedback']={'correct':{'message':success},'incorrect':{'message':failure},'hints':[hint]}
  candidates=[r for r in rems if cid in r['concept_ids']]
  facts=set(s['fact_ids'])
  rem=next((r for r in candidates if facts and set(r.get('lineage',{}).get('fact_ids',[]))==facts),None)
  if rem is None: rem=next((r for r in candidates if facts and facts <= set(r.get('lineage',{}).get('fact_ids',[]))),None)
  if rem is None and candidates: rem=candidates[0]
  if rem: ix['feedback']['remediation_step_id']=rem['step_id']
  seen.add(cid); out['interactions'].append({'step_id':s['step_id'],'interaction':ix})
 result['tiles'].append(out)
(B/'interactions.json').write_text(json.dumps(result,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in result['tiles']),'interactions')
