import json, re, copy
from pathlib import Path
P=Path('batches/final_batch_learn_python.region.03')
plan=json.loads((P/'tile_plans.json').read_text())
gloss=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
registry=json.loads((P/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in gloss['bundles']}
assets={a['asset_id']:a for a in registry['assets']}
# Short, standalone restatements in the same order as the glossary facts.
voice={
'exception_hierarchy':[
'BaseException is the root of Python’s built-in exception hierarchy. Its Exception subclass covers ordinary application failures.',
'ValueError and OSError sit under Exception. FileNotFoundError sits under OSError.',
'KeyboardInterrupt, SystemExit and GeneratorExit sit directly under BaseException, not under Exception.'
],
'exception_propagation':[
'When an exception is raised, the remaining operations in the current try body are skipped while Python searches for a matching handler.',
'A handler accepts its named exception class or a subclass. Python examines handlers in their written order.',
'Without a matching local handler, the exception travels through callers toward an outer handler. If none matches, it remains unhandled.',
'After a handler recovers, execution continues after that try/except statement. It does not restart the failed operation.'
],
'finally_cleanup':[
'Put release operations in a finally: body aligned with the preceding try:. They run when execution leaves the protected operation.',
'The finally body runs after normal completion, an exception, or a return from the try body.',
'If finally completes normally, an unhandled exception is re-raised afterward. A return inside finally can replace a pending return or suppress a pending exception.'
],
'functions_as_values':[
'Defining a function creates a function object bound to its name. The bare name refers to that function; name(arguments) calls it.',
'Pass a function itself when the receiving helper requires a function object.',
'You can store a callable and invoke it later.',
'A helper can call its supplied function parameter with parameter(value). Passing an earlier call’s result is different from supplying the function.'
],
'closures_and_enclosing_scope':[
'A nested function can resolve a free name in an enclosing function scope. Each call has its own local bindings.',
'A returned nested function can still use enclosing values after the call that created it has finished.',
'Use nonlocal name to rebind an existing name in the nearest enclosing function scope.',
'A stateful factory can bind state and return a nested function that reads it and uses nonlocal to rebind it.'
],
'pathlib_paths':[
'Import Path with from pathlib import Path. It provides concrete paths using the platform’s path conventions.',
'base / "child" builds a child path. An absolute right operand instead replaces the previous path; it does not stay beneath that base.',
'Relative paths are interpreted against the current working directory. Choose an explicit base directory to avoid depending on an unintended working directory.'
],
'raising_exceptions':[
'Use raise ExceptionType(message) to signal a particular failure and give explanatory context.',
'ValueError indicates an argument with an appropriate type but an inappropriate value, except where a more precise exception applies.',
'Choose a specific exception so callers can handle the failure precisely.'
],
'reading_tracebacks':[
'The final line of an exception report names the exception type and gives its message.',
'The preceding traceback frames show source locations and the calling context in which the exception occurred.',
'Follow the call-chain frames down to the most recent failing operation. Its displayed file, line and statement locate the immediate cause.'
],
'debugger_usage':[
'breakpoint() enters the debugger where it is called. By default, it invokes pdb.set_trace().',
'In pdb, p expression prints an expression’s value. Use l to list nearby source lines.',
'Use n for the next line without entering a called function, s to step into calls, and c to continue until another breakpoint or termination.',
'Use b line_number to set a breakpoint. When paused there, inspect the values controlling the suspect branch.'
],
'safe_mutable_defaults':[
'Default values are evaluated once, when the function is defined. A mutable default can therefore retain modifications across calls.',
'For fresh per-call state, use a None default and create a new list or dictionary inside an if parameter is None: branch in the function body.'
],
'sorting_with_key_functions':[
'sorted(records, key=function) creates a new sorted list. Each function(record) result supplies that record’s comparison key.',
'sorted leaves the original list unchanged. Use reverse=True to reverse the ordering.',
'Sorting is stable: records with equal keys keep their original relative order.',
'For case-normalized text ordering, str.lower can supply a lowercase comparison key.'
],
'lambda_expressions':[
'lambda parameters: expression creates an anonymous function. Its result is the value of that single expression.',
'A lambda contains just one expression. You can pass it to sorting as key=lambda item: expression.'
],
'specific_exception_handlers':[
'An except handler matches its named exception class and subclasses. The first matching handler runs.',
'Put subclass-specific handlers before broader parent handlers so the specific recovery remains reachable.',
'FileNotFoundError is an OSError subclass. When recovery actions differ, except FileNotFoundError: must come before except OSError:.'
],
'validation_vs_programming_errors':[
'ValueError can identify unsuitable input, such as malformed numeric text. Reject or request correction of input that violates the stated value contract.',
'NameError means a local or global name cannot be found. Correct a misspelled implementation name rather than rejecting the supplied input.',
'PermissionError reports inadequate access rights for a filesystem operation. Report the access failure; do not assume the path or implementation is inherently wrong.'
],
'variadic_arguments_and_unpacking':[
'In a definition, *args collects remaining positional arguments into a tuple.',
'In a definition, **kwargs collects additional keyword arguments into a dictionary. A call cannot give one parameter two values.',
'In a call, *args expands a sequence into positional arguments; **kwargs expands a dictionary into keyword arguments.',
'A forwarding wrapper can define wrapper(*args, **kwargs) and return target(*args, **kwargs). Do not add arguments that duplicate a supplied binding.'
]}
contrast={
'exception_hierarchy':'Contrast the ordinary Exception branch with the three signals directly under BaseException; these are not all children of Exception.',
'exception_propagation':'In quantity("three"), recovery follows the caller’s try/except; it does not retry int(text) or the skipped converted-value print.',
'finally_cleanup':'In read_quantity, cleanup belongs to finally, not to a replacement return. Keep the exit action separate from the calculation’s result.',
'functions_as_values':'chosen = double stores the function. double(3) calls it now; it does not supply the function for apply to call later.',
'closures_and_enclosing_scope':'counter and other come from separate make_counter calls. Updating counter’s enclosing count does not continue other’s state.',
'pathlib_paths':'A relative orders.csv is a child of base. An absolute right operand replaces base instead of staying beneath it.',
'raising_exceptions':'In cost, a negative quantity violates the stated value requirement. raise signals that failure; merely displaying a message is different.',
'reading_tracebacks':'The outer helper’s frame shows who requested the conversion. The int(text) frame identifies the operation that immediately failed.',
'debugger_usage':'Choose n to stay outside a called function and s to enter it. These are pdb commands, not Python source statements.',
'safe_mutable_defaults':'labels=[] is evaluated at definition time. labels=None with the None guard creates fresh storage during an omitted-list call.',
'sorting_with_key_functions':'The quantity key is a comparison value, not a rearranged record. Equal-key blue and green retain their relative order.',
'lambda_expressions':'lambda pair: pair[1] supplies a pair’s comparison key. It is one expression, not a loop or statement body.',
'specific_exception_handlers':'For a missing file, an earlier OSError handler matches before FileNotFoundError. Put the specific handler first when recoveries differ.',
'validation_vs_programming_errors':'Malformed numeric text calls for input correction; a misspelled quantity name calls for code correction. Inadequate access rights need an access-failure report.',
'variadic_arguments_and_unpacking':'The wrapper collects arguments in its definition and expands them at the target call. Adding another price can duplicate the caller’s binding.'}
recaps={
'exception_hierarchy':'BaseException is the root; ordinary failures belong to its Exception branch.',
'exception_propagation':'Find the matching handler, then resume after its try/except—not at the failed operation.',
'finally_cleanup':'finally runs on exit; a return there can replace a pending return or suppress an exception.',
'functions_as_values':'Pass the function itself when a helper needs to call it later.',
'closures_and_enclosing_scope':'Use nonlocal for an existing enclosing binding; separate factory calls have separate local state.',
'pathlib_paths':'Distinguish relative children, absolute replacements, and working-directory-dependent paths.',
'raising_exceptions':'Signal a value-contract failure with context and a specific exception.',
'reading_tracebacks':'Read the final exception line, then locate the immediate failure in the most recent frame.',
'debugger_usage':'Inspect paused values and choose whether to step into a call.',
'safe_mutable_defaults':'Defaults are evaluated once; a None guard can create fresh per-call storage.',
'sorting_with_key_functions':'sorted creates a new list using comparison keys; equal keys retain relative order.',
'lambda_expressions':'A lambda is an anonymous function with one expression.',
'specific_exception_handlers':'The first matching handler runs; place a specific subclass before its broader parent.',
'validation_vs_programming_errors':'Separate input correction, implementation correction, and access-failure reporting.',
'variadic_arguments_and_unpacking':'Collect arguments in definitions, expand them in calls, and avoid duplicate bindings.'}
def key(cid): return cid.split('.',1)[1]
def fact_ids(cid): return [cid+'#'+f['id'] for f in bundles[cid]['coverage']['required_facts']]
def tb_ids(cid, fs):
 return [cid+'#'+tb['id'] for tb in bundles[cid]['teaching_blocks'] if set(cid+'#'+f for f in tb['fact_ids']) & set(fs)]
def lin(cid, fs=None, ts=None, visual=False):
 fs=fact_ids(cid) if fs is None else fs
 d={'concept_ids':[cid],'fact_ids':fs,'teaching_block_ids':tb_ids(cid,fs) if ts is None else ts}
 if visual:d['anchors']=[cid+'#visual']
 return d
def prose(cid,text,fs=None,ts=None,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':lin(cid,fs,ts)}
def teach(cid, fs, planned_tbs=None):
 result=[]
 for f in fs:
  idx=next(i for i,x in enumerate(bundles[cid]['coverage']['required_facts']) if cid+'#'+x['id']==f)
  ts=tb_ids(cid,[f])
  if planned_tbs is not None: ts=[t for t in ts if t in planned_tbs]
  result.append(prose(cid,voice[key(cid)][idx],[f],ts,role='definition' if idx==0 else 'mechanism'))
 return result
def code_example(cid):
 text=next(tb['content'] for tb in bundles[cid]['teaching_blocks'] if tb['id']=='tb4')
 found=re.search(r'```python\n(.*?)```',text,re.S)
 if found:return found.group(1).rstrip()
 a=assets['ws.'+key(cid)]
 return next(f['content'] for f in a['files'] if f['path']=='main.py').rstrip()
def walkthrough(cid,code,notes):
 annotations=[]
 for needle,text in notes:
  matching=[i for i,line in enumerate(code.splitlines(),1) if needle in line]
  if matching:annotations.append({'start_line':matching[0],'end_line':matching[0],'text':text})
 return {'type':'code_walkthrough','language':'python','code':code,'annotations':annotations,'reveal':'all','lineage':lin(cid,visual=True)}
notes={
'finally_cleanup': [('try:', 'Protected calculation; a pending return leaves through cleanup.'),('finally:', 'Aligned exit action: normal completion, return, or exception.'),('print("Leaving', 'Cleanup completes before a pending return or unhandled exception proceeds.')],
'functions_as_values':[('def double','Definition binds the function object.'),('chosen =','Store the callable, rather than the result of a call.'),('return operation','Invoke the supplied function through the parameter.'),('print(apply','Pass the stored function and the value to the receiving helper.')],
'closures_and_enclosing_scope':[('count = 0','State belongs to this factory call.'),('nonlocal','Rebind the existing enclosing count.'),('return advance','The returned function retains access to enclosing state.'),('counter =','First factory call: retain its own binding.'),('other =','Separate factory call: distinct local state.')],
'raising_exceptions':[('if quantity','Check the stated value requirement.'),('raise ValueError','The negative-quantity path signals failure and does not reach the return.'),('return quantity','An accepted quantity reaches the calculation.'),('except ValueError','Specific handling of the signaled value failure.')],
'reading_tracebacks':[('return int','Immediate failing operation for the supplied numeric text; find this frame’s file and line.'),('return read_quantity','The outer helper’s calling frame provides context, not the immediate conversion failure.'),('outer("','Follow the report down the call chain; its final line supplies the exception type and message.')],
'sorting_with_key_functions':[('return record','Return a comparison key, not a rearranged record.'),('ordered =','Create a new list; equal keys retain original relative order.'),('print([record','Inspect the new ordering and the unchanged original list in the computed output.')],
'lambda_expressions':[('ordered =','The anonymous key function returns the second item’s value; its body is one expression.')],
'specific_exception_handlers':[('except FileNotFoundError','Specific subclass recovery comes first.'),('except OSError','Broader parent recovery comes later; first match wins.')],
'variadic_arguments_and_unpacking':[('def wrapper','Collect positional arguments and additional keyword arguments.'),('return target','Expand both collections at the target call; do not duplicate a parameter.'),('print(wrapper','The supplied positional quantity and keyword price reach the target.')]
}
def diagram(cid, labels, edges=(), kind='sequence', title=None, alt=None):
 nodes=[{'id':'n'+str(i+1),'label':label} for i,label in enumerate(labels)]
 return {'type':'diagram','diagram_kind':kind,'title':title or bundles[cid]['context']['concept_name'], 'nodes':nodes,'edges':[{'from':nodes[a]['id'],'to':nodes[b]['id'],'label':label,'directed':True} for a,b,label in edges], 'layout':'auto','alt_text':alt or ' → '.join(labels),'lineage':lin(cid,visual=True)}
def visual(cid):
 k=key(cid)
 if k=='exception_hierarchy':
  fs=bundles[cid]['coverage']['required_facts']
  labels=[]
  for f in fs:
   for name in re.findall(r'\b(?:[A-Z][A-Za-z]*Exception|BaseException|Exception|ValueError|OSError|FileNotFoundError|KeyboardInterrupt|SystemExit|GeneratorExit)\b',f['statement']):
    if name not in labels:labels.append(name)
  index={n:i for i,n in enumerate(labels)}
  root=labels[0]; ordinary=labels[1]
  parents=[(root,ordinary),(ordinary,'ValueError'),(ordinary,'OSError'),('OSError','FileNotFoundError')]+[(root,n) for n in re.findall(r'KeyboardInterrupt|SystemExit|GeneratorExit',fs[-1]['statement'])]
  return diagram(cid,labels,[(index[p],index[c],'subclass') for p,c in parents],kind='tree',alt='Built-in exception branches: '+ '; '.join(p+' → '+c for p,c in parents))
 if k=='exception_propagation':
  code=code_example(cid)
  lines=code.splitlines()
  labels=[next(l.strip() for l in lines if 'value = ' in l),next(l.strip() for l in lines if 'return int' in l),next(l.strip() for l in lines if 'except ValueError' in l),next(l.strip() for l in lines if 'print("Converted' in l),lines[-1].strip()]
  return diagram(cid,labels,[(0,1,'enter helper'),(1,2,'conversion failure propagates'),(2,4,'recover, then resume')],alt='Caller enters conversion; failure reaches ValueError handler. Converted-value print is skipped. Execution resumes after try/except.')
 if k=='pathlib_paths':
  example=next(tb['content'] for tb in bundles[cid]['teaching_blocks'] if tb['id']=='tb4')
  code=code_example(cid)
  relbase=next(l for l in code.splitlines() if l.startswith('base ='))
  child=next(l for l in code.splitlines() if l.startswith('output ='))
  absolute=re.search(r'on POSIX, (.*?) represents',example).group(1)
  base_literal=re.search(r'Path\("[^"]+"\)',absolute).group(0)
  return diagram(cid,[base_literal,child,absolute,relbase,'Current working directory'],[(0,1,'relative child appended'),(0,2,'absolute right operand replaces base'),(4,3,'relative base interpreted here')],kind='mapping',alt='Relative child stays beneath an absolute project base. Absolute right operand replaces it. Relative project base is interpreted against the current working directory.')
 if k=='debugger_usage':
  a=assets['ws.debugger_usage']; files={f['path']:f['content'] for f in a['files']}
  source=files['main.py'].splitlines(); session=files['debugger_session.txt']
  # Copy registered observed state, never fabricate command results or positions.
  inspect=[]
  for command in ['p quantity','p quantity < 0']:
   match=re.search(r'\(Pdb\) '+re.escape(command)+r'\n([^\n]+)',session)
   inspect.append(command+'\n'+match.group(1))
  positions=re.findall(r'-> (.+)',session)
  labels=['Numbered helper source\n'+'\n'.join(str(i)+': '+s for i,s in enumerate(source,1) if s.strip()), 'Paused before branch\n'+positions[0], 'Inspect values\n'+'\n'.join(inspect), 'After n\n'+positions[-1]]
  return diagram(cid,labels,[(1,2,'p inspects'),(2,3,'n steps')],kind='sequence',alt='Numbered source and registered paused pdb state: inspect quantity and its comparison before stepping to the defective return branch.')
 if k=='safe_mutable_defaults':
  bad=next(f['content'] for f in assets['ws.'+k]['files'] if f['path']=='main.py').rstrip()
  good=code_example(cid)
  return {'type':'side_by_side','left':walkthrough(cid,bad,[('labels=[]','Default list is evaluated once at definition time.')]),'right':walkthrough(cid,good,[('labels=None','Distinguish an omitted list from supplied storage.'),('if labels is None','Create fresh storage in the function body.')]),'left_label':'Shared mutable default','right_label':'Fresh omitted-list state','takeaway':'Create omitted-list storage during the call, not as a mutable default.','lineage':lin(cid,visual=True)}
 if k=='validation_vs_programming_errors':
  # Three reports are glossary teaching examples, not executable filesystem operations.
  left=diagram(cid,['ValueError from int("three")','Request corrected numeric input'],[(0,1,'unsuitable value')],kind='mapping')
  right=diagram(cid,['NameError: misspelled quantity name','Correct implementation name','PermissionError: inadequate access rights','Report access failure'],[(0,1,'missing implementation name'),(2,3,'access problem')],kind='mapping')
  return {'type':'side_by_side','left':left,'right':right,'left_label':'Input value failure','right_label':'Implementation or access failure','takeaway':'Choose the response from the reported cause, not an assumption that every failure is bad input.','lineage':lin(cid,visual=True)}
 return walkthrough(cid,code_example(cid),notes.get(k,[]))
# Interaction framing states only the task; stage 04 provides the supplied evidence and grading.
framing={
'exception_hierarchy':('Review the exception branches','Read the supplied exception excerpts and decide which classifications are correct.'),
'exception_propagation':('Recover from a conversion failure','Complete the supplied helper and recovery path so execution continues after the protected conversion.'),
'finally_cleanup':('Keep cleanup at the exit boundary','Complete the supplied finally body with the requested release action while preserving the return and exception behavior.'),
'functions_as_values':('Pass the calculation itself','Complete the helper so it receives and calls the supplied function rather than an earlier call’s result.'),
'closures_and_enclosing_scope':('Retain separate counter state','Complete the factory so each returned function reads and rebinds its own enclosing state.'),
'pathlib_paths':('Construct the child path','Complete the path construction with a relative child beneath the supplied explicit base.'),
'raising_exceptions':('Signal the value-contract failure','Complete the argument check with a specific exception and explanatory context.'),
'reading_tracebacks':('Locate the immediate failure','Inspect the supplied conversion traceback and identify the failing statement and its calling context.'),
'debugger_usage':('Review the paused branch','Read the supplied source and debugger excerpt and decide which command or diagnosis is correct.'),
'safe_mutable_defaults':('Repair the shared default','Complete the helper so omitted-list calls create fresh storage while supplied lists are still used.'),
'sorting_with_key_functions':('Order records by their key','Complete the supplied sorting task using a key function without changing the original list.'),
'lambda_expressions':('Supply a one-expression key','Complete the sorting key with a lambda that returns the required comparison value.'),
'specific_exception_handlers':('Keep specific recovery reachable','Complete the supplied handlers with the subclass-specific recovery before its broader parent.'),
'validation_vs_programming_errors':('Review the failure reports','Read the supplied reports and decide which diagnostic category and response fits each cause.'),
'variadic_arguments_and_unpacking':('Forward the caller’s arguments','Complete the wrapper so it expands both collected argument groups without duplicate bindings.')}
def measured(cid,s):
 fs=list(s['fact_ids'])
 for anchor in s['anchors']:
  if '#assessment:' in anchor:
   capability=anchor.split('#assessment:',1)[1]
   aa=next(a for a in bundles[cid]['assessment_anchors'] if a['capability']==capability)
   for f in aa['fact_ids']:
    q=cid+'#'+f
    if q not in fs: fs.append(q)
 return fs or fact_ids(cid)
def next_title(tile):
 nid=tile['next_tile_id']
 nxt=next((t for t in plan['tiles'] if t['tile_id']==nid),None)
 if nxt:return bundles[nxt['steps'][0]['concept_ids'][0]]['context']['concept_name']
 b=next((b for b in gloss['bundles'] if b['context']['toc_location']['tile_id']==nid),None)
 if b:return b['context']['concept_name']
 # The assembled glossary gives concept names even when next-tile facts are out of batch scope.
 next_concept=next(c for c in bundles[tile['concept_ids'][-1]]['context']['blocked_future_concepts'])
 return gloss['names'][next_concept]
out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for tile in plan['tiles']:
 title=tile['title']
 if title==tile['tile_id']:title=' and '.join(bundles[c]['context']['concept_name'] for c in tile['concept_ids'])
 t={'tile_id':tile['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 seen=set()
 for s in tile['steps']:
  cid=s['concept_ids'][0]; k=key(cid); typ=s['type']
  step={'step_id':s['step_id'],'type':typ,'concept_ids':copy.deepcopy(s['concept_ids']),'title':bundles[cid]['context']['concept_name'], 'lineage':{field:copy.deepcopy(s[field]) for field in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']}}
  if typ=='explainer':
   step['blocks']=teach(cid,s['fact_ids'],s['teaching_block_ids'])
   # The split continuation screens re-voice the running example explicitly.
   if not s['planned_visual_block_type']:
    step['title']='Apply the distinction: '+bundles[cid]['context']['concept_name']
    # Facts remain taught on this screen as well; the contrast is short enough for the planned continuation budget.
    step['blocks'].append(prose(cid,contrast[k],s['fact_ids'],s['teaching_block_ids'],role='example'))
   else:step['blocks'].append(visual(cid))
  elif typ=='video':
   step['title']=bundles[cid]['media']['group_title']
   step['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif typ in ['check','hands_on']:
   if typ=='check':
    step['title']='Check: '+bundles[cid]['context']['concept_name']
    step['lede']='Read the supplied evidence and choose the answer that matches the rule.'
   else:
    step['title'],step['lede']=framing[k]
    if s['planned_interaction_type'] in ['classify','choice']:
     step['title']='Review '+bundles[cid]['context']['concept_name']
     step['lede']='Read the supplied excerpts in this step and decide which classifications or diagnoses are correct.'
   fs=measured(cid,s);signature=(cid,tuple(sorted(fs)))
   if signature not in seen:
    seen.add(signature);rid=tile['tile_id']+'.r'+str(len(t['remediation_steps'])+1).zfill(2)
    t['remediation_steps'].append({'step_id':rid,'type':'remediation','required':False,'concept_ids':[cid],'eyebrow':'Try the contrast','title':'Review: '+bundles[cid]['context']['concept_name'],'blocks':teach(cid,fs)+[prose(cid,contrast[k],fs,role='example')],'lineage':lin(cid,fs)})
  elif typ=='recap':
   step['title']='Keep these distinctions'
   step['blocks']=[prose(c,recaps[key(c)],role='takeaway') for c in s['concept_ids']]
   step['blocks'].append({'type':'up_next','title':next_title(tile)})
  t['steps'].append(step)
 out['tiles'].append(t)
(P/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Wrote',P/'screens.json')
print('tiles',len(out['tiles']),'steps',sum(len(t['steps']) for t in out['tiles']),'remediation',sum(len(t['remediation_steps']) for t in out['tiles']))
