import json,io,contextlib,traceback
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.03')
p=json.loads((B/'tile_plans.json').read_text()); sc=json.loads((B/'screens.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); reg=json.loads((B/'scenario_asset_registry.json').read_text());cs={c['context']['concept_id']:c for c in g['bundles']};assets={a['asset_id']:a for a in reg['assets']};runtime=json.load(open('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']['python']
# Authored questions: every incorrect response has its own fact-grounded explanation.
Q={}
def q(tile,s,prompt,correct,wrong1,why1,wrong2,why2):Q[(tile,s)]=(prompt,correct,[(wrong1,why1),(wrong2,why2)])
q('051_053','s02','Which is the direct parent of FileNotFoundError?','OSError','ValueError','ValueError is a separate subclass of Exception, not the parent of FileNotFoundError.','BaseException','BaseException is the root; FileNotFoundError is directly beneath OSError.')
q('051_053','s05','A helper has no local handler and raises ValueError. Its caller has except Exception first and except ValueError second. Which handler runs?','The caller\'s Exception handler.','The caller\'s ValueError handler.','Exception matches its subclasses; the first matching handler runs even if a later one is more specific.','No handler; the failure is inside a helper.','An exception without a matching local handler propagates to callers.')
q('051_053','s08','An aligned finally body only closes a supplied file and completes normally. What happens when try completes normally, returns a value, or raises an unhandled exception?','Cleanup runs in all three cases; the return remains a return and the unhandled exception propagates afterward.','Cleanup runs only when an exception occurs.','finally also runs on normal completion and return.','Cleanup runs in all cases and always suppresses the exception.','A normally completing finally does not suppress an unhandled exception.')
q('051_053','s09','A try body has a pending return of 3, but its finally body returns 0. Which result leaves the function?','0, because the finally return replaces the pending return.','3, because the first return always wins.','A return from finally can replace a pending return.','Both values are returned.','The finally return replaces rather than combines with the pending return.')
q('054_055','s02','double is a function. apply(operation, value) calls operation(value). Which call passes double itself to transform 3?','apply(double, 3)','apply(double(3), 3)','double(3) invokes double first and passes its result, not the function object.','apply("double", 3)','A quoted name is text, not the function bound to the bare name double.')
q('054_055','s03','chosen stores double. In def apply(operation, value), which return invokes the supplied callable on value?','return operation(value)','return operation','The bare parameter refers to the callable but does not invoke it.','return double(value)','Calling double directly ignores the supplied operation; the receiving helper must invoke its parameter.')
q('054_055','s07','counter and other come from separate make_counter() calls. Each factory starts count at 0; its returned advance uses nonlocal count to increment and return it. Which state description is correct?','counter retains its own count across calls; other retains a separate count.','Both returned functions update one shared count.','Each factory call has its own local bindings.','Each advance call starts count at 0 again.','The returned function retains its enclosing state after the factory returns.')
q('054_055','s08','advance is nested inside make_counter, which already binds count. Which declaration lets advance rebind that existing enclosing count?','nonlocal count','global count','nonlocal targets an existing enclosing function binding, not a global binding.','No declaration; assigning count automatically rebinds the enclosing variable.','Rebinding that existing enclosing name requires nonlocal in the nested function.')
q('056_056','s02','A program constructs Path("orders.csv") without an explicit base. Against which location is that relative path interpreted?','The current working directory.','Always the directory containing the script.','A relative path uses the current working directory, which need not be the script directory.','Always the filesystem root.','Root-based resolution is not the rule for relative paths; an explicit base avoids an unintended working directory.')
q('057_059','s02','cost receives a numeric quantity of -1 where the contract requires a nonnegative number. Which exception best communicates the invalid value?','ValueError','OSError','The evidence concerns an inappropriate numeric value, not a file-operation failure.','FileNotFoundError','No missing file is involved; this is an unsuitable argument value.')
q('057_059','s03','Which statement signals a failure with explanatory context instead of merely displaying text?','raise ValueError("quantity must be nonnegative")','print("quantity must be nonnegative")','Printing a message does not raise the exception.','ValueError("quantity must be nonnegative")','Constructing the exception without raise does not signal it.')
q('057_059','s07','Read this traceback excerpt:\n```text\nFile "main.py", line 5, in outer\n    return read_quantity(text)\nFile "main.py", line 2, in read_quantity\n    return int(text)\nValueError: invalid literal for int() with base 10: \'three\'\n```\nWhich statement connects the caller to the immediate failure?','outer calls read_quantity(text); int(text) in read_quantity is the immediate failing operation.','outer performs int(text) at line 5.','The caller frame displays read_quantity(text); the innermost frame displays int(text).','The first displayed frame is necessarily the immediate failing operation.','The call-chain frames lead down to the most recent failing operation; here it is in read_quantity.')
q('057_059','s12','breakpoint() is immediately before a suspect if quantity < 0 branch. Execution pauses with quantity = 3. Which sequence locates the source and inspects the controlling value and condition?','l, then p quantity, then p quantity < 0','c, then c again','c continues execution rather than displaying source or the controlling expressions.','Only b 5; no inspection is needed.','b sets a breakpoint at a line; it does not inspect quantity or the branch condition.')
q('057_059','s13','At a pdb pause before a helper call, you want to execute the next line without stepping into the called helper. Which command fits?','n','s','s steps into calls; the task explicitly asks not to step into the helper.','c','c continues until another breakpoint or termination, not just the next line.')
q('060_060','s03','add_label(label, labels=[]) appends label and returns labels. Two consecutive calls omit labels. Why can the second result include the first label?','The default list is created once at function definition and retains earlier modifications.','An omitted default list is freshly created at each call.','Mutable defaults are evaluated once, not recreated for each omitted argument.','append always copies a list before changing it.','Here the same default object retains modifications across calls; no per-call list is created.')
q('060_060','s04','Which pattern creates fresh state for omitted labels while preserving an explicitly supplied list?','Use labels=None; inside the function, if labels is None: assign labels = [].','Keep labels=[] in the signature.','That mutable default is evaluated once and can retain modifications.','Always assign labels = [] at function entry.','That would discard a caller-supplied list; the None check limits allocation to the omitted-list case.')
q('061_062','s03','What does sorted(records, key=label_key, reverse=True) do to the original list and the result?','It returns a new list in reversed key order and leaves records unchanged.','It sorts records in place and returns that same list.','sorted does not mutate the original list.','It leaves records unchanged but ignores reverse=True.','reverse=True reverses the ordering of the returned sorted result.')
q('061_062','s06','Each pair is (label, quantity). Which one-parameter, single-expression lambda returns the quantity as a sorting key?','lambda pair: pair[1]','lambda pair: pair[0]','Index 0 is the label, not the quantity.','lambda: pair[1]','This lambda has no parameter to receive the pair being sorted.')
q('063_064','s03','A try body raises FileNotFoundError. except OSError appears before except FileNotFoundError. Which recovery action runs?','The OSError action, because it is the first matching handler.','The FileNotFoundError action, regardless of order.','FileNotFoundError is a subclass of OSError; the earlier OSError handler already matches.','Both actions run.','Only the first matching handler runs.')
q('063_064','s06','The input contract requires numeric text. int("three") raises ValueError. What response fits this evidence?','Reject the unsuitable input or request corrected numeric text.','Treat the conversion failure as proof of an implementation defect.','The supplied text violates the stated input value contract; that evidence does not establish a coding defect.','Treat it as proof of inadequate filesystem access rights.','The report is a numeric conversion failure, not a path access failure.')
q('065_065','s04','For wrapper(*args, **kwargs), what is collected by each parameter when called as wrapper(3, price=5)?','args collects positional arguments in a tuple; kwargs collects additional keywords in a dictionary.','args collects a dictionary; kwargs collects a tuple.','The collection types are reversed: positional arguments form a tuple and keyword arguments form a dictionary.','Both parameters collect lists.','The documented collections are a tuple and a dictionary, not lists.')
q('065_065','s05','A wrapper must pass its collected positional and keyword arguments to target without adding any duplicate bindings. Which call expands both collections?','target(*args, **kwargs)','target(args, kwargs)','That passes the two collections as ordinary arguments rather than expanding them.','target(*args, **kwargs, price=5)','Adding price can duplicate a price already supplied through the caller\'s expanded arguments.')

# Code tasks; scaffold is identical in starter and solution. Test values are executed, not transcribed.
C={}
def code(cid,prompt,starter,solution,exprs=None,calls=None):
 tests=[];ns={};out=io.StringIO()
 with contextlib.redirect_stdout(out):exec(compile(solution,'main.py','exec'),ns)
 for i,expr in enumerate(exprs or []):
  expected=eval(expr,ns)
  tests.append({'test_id':f't{i+1}','kind':'value_equals','spec':{'expr':expr,'expected':json.loads(json.dumps(expected))},'visible':True,'message_on_fail':'Check the requested result and preserve the supplied inputs and scaffolding.'})
 for fun,args,kw in calls or []:
  expected=ns[fun](*args,**kw)
  tests.append({'test_id':f't{len(tests)+1}','kind':'function_call','spec':{'function':fun,'args':args,'kwargs':kw,'expected':json.loads(json.dumps(expected))},'visible':True,'message_on_fail':'The function must preserve this argument-dependent behavior.'})
 C['python.'+cid]=(prompt,starter,solution,tests)

a=assets['ws.exception_propagation']['files'][0]['content']
# Trace predictions select from supplied descriptions; copied strings are learner assignments.
prefix='failure_site = "int(text)"\nskipped_site = "print(\\"Converted\\", value)"\nresume_site = "after try/except"\n'
# Identical executable demonstration, with the prediction fields missing in the starter.
pred='predicted_failure = ""\npredicted_skip = ""\npredicted_resume = ""\n'
solpred='predicted_failure = failure_site\npredicted_skip = skipped_site\npredicted_resume = resume_site\n'
code('exception_propagation','Before running the supplied conversion example, record predictions: set predicted_failure to the supplied description of the failure point, predicted_skip to the skipped statement description, and predicted_resume to the resumption description. Select from failure_site, skipped_site, and resume_site. Keep the demonstration unchanged, then run it to confirm Invalid quantity followed by After recovery, with no Converted output.',prefix+pred+a,prefix+solpred+a,['[predicted_failure, predicted_skip, predicted_resume]'])

fixture='''\n# Instructor harness: supplied already-open file objects; do not edit.
import io
valid_text = "3"
invalid_text = "three"
good = io.StringIO(valid_text)
bad = io.StringIO(invalid_text)
good_result = read_quantity(good)
try:
    read_quantity(bad)
    failure = "no failure"
except ValueError as exc:
    failure = type(exc).__name__
'''
a=assets['ws.finally_cleanup']['files'][0]['content']
code('finally_cleanup','Complete the finally body of read_quantity(text) with the file release operation, without returning from finally. Keep the harness unchanged. good_result must retain the integer conversion; both supplied files must be closed, and the invalid conversion must still raise ValueError (the harness records its type in failure).',a+fixture,a.replace('pass','text.close()')+fixture,['[good_result, good.closed, bad.closed, failure]'])
a=assets['ws.functions_as_values']['files'][0]['content'];print('functions starter',a)
code('functions_as_values','Complete apply(operation, value) to return operation(value). Bind chosen to the function double without calling it. Keep the supplied double implementation. The checker calls apply with chosen and with a different supplied callable; it also checks chosen refers to double.', 'def double(value):\n    return value * 2\n\ndef apply(operation, value):\n    pass\n\nchosen = None\ninput_value = 3\n', 'def double(value):\n    return value * 2\n\ndef apply(operation, value):\n    return operation(value)\n\nchosen = double\ninput_value = 3\n',['[chosen is double, apply(chosen, input_value), apply(lambda x: x + 1, input_value)]'])
st='def make_counter():\n    count = 0\n    def advance():\n        pass\n    return advance\n\ncounter = make_counter()\nother = make_counter()\n'
so=st.replace('        pass','        nonlocal count\n        count = count + 1\n        return count')
code('closures_and_enclosing_scope','Complete advance inside make_counter: declare nonlocal count, increment count by one, and return it. The factory must return advance without calling it. Keep counter and other as separate factory results. The checker calls counter twice and other once, expecting independent retained state.',st,so,['[counter(), counter(), other()]'])
st='from pathlib import Path\nbase_directory = "/work/project"\nbase = Path(base_directory)\noutput = None\nprint(output)\n'
code('pathlib_paths','Keep the supplied absolute base directory. Construct output as the orders.csv child using base and a relative child filename with /. Do not perform filesystem operations. The checker reads str(output).',st,st.replace('output = None','output = base / "orders.csv"'),['str(output)'])
# Catch the deliberate failure only in the instructor harness, so the function itself retains it.
h='''\n# Instructor harness; leave unchanged.
negative_quantity = -1
zero_quantity = 0
positive_quantity = 2
try:
    cost(negative_quantity)
    negative_result = "no failure"
except ValueError as exc:
    negative_result = [type(exc).__name__, str(exc)]
zero_result = cost(zero_quantity)
positive_result = cost(positive_quantity)
'''
st='def cost(quantity):\n    return quantity * 4\n'+h
so='def cost(quantity):\n    if quantity < 0:\n        raise ValueError("quantity must be nonnegative")\n    return quantity * 4\n'+h
code('raising_exceptions','Add a negative-value check to cost(quantity) that raises ValueError("quantity must be nonnegative"). Preserve quantity * 4 for nonnegative inputs. Keep the harness: negative_result records the type/message, zero_result and positive_result record the return values.',st,so,['[negative_result, zero_result, positive_result]'])
# Real traceback and numbered source, exposed as evidence rather than a synthesized output.
source=assets['ws.reading_tracebacks']['files'][0]['content']
th='''# Instructor traceback capture; do not edit.
import traceback
raw_text = "three"
source_file = "quantity_example.py"
source_code = %r
scope = {"raw_text": raw_text}
try:
    exec(compile(source_code, source_file, "exec"), scope)
except ValueError as exc:
    observed_type = type(exc).__name__
    observed_message = str(exc)
    frames = traceback.extract_tb(exc.__traceback__)
    inner_file = frames[-1].filename
    inner_line = frames[-1].lineno
    inner_function = frames[-1].name
    caller_function = frames[-2].name
    caller_line = frames[-2].lineno
    rendered_traceback = "".join(traceback.format_exception(exc))
print(rendered_traceback)
print(source_code)
''' % source.replace('outer("three")','outer(raw_text)')
pred='exception_type = ""\nexception_message = ""\nfailing_file = ""\nfailing_line = 0\nfailing_function = ""\ncalling_function = ""\ncalling_line = 0\n'
sol='exception_type = observed_type\nexception_message = observed_message\nfailing_file = inner_file\nfailing_line = inner_line\nfailing_function = inner_function\ncalling_function = caller_function\ncalling_line = caller_line\n'
code('reading_tracebacks','Run the supplied traceback capture and inspect the displayed two-function source. Fill the report assignments using the supplied evidence variables: record exception_type, exception_message, failing_file, failing_line, failing_function, calling_function, and calling_line. Locate return int(text) as the immediate cause in read_quantity and connect it to outer\'s return read_quantity(text). Use evidence variables, not hard-coded output text; keep the capture unchanged.',th+pred,th+sol,['[exception_type, exception_message, failing_file, failing_line, failing_function, calling_function, calling_line]'])
# Browser stdin is not interactive: inspect the authentic registered session, then record commands and fix its comparison.
session=next(f['content'] for f in assets['ws.debugger_usage']['files'] if f['path']=='debugger_session.txt')
dh='# Supplied recorded pdb session (interactive stdin is unavailable).\n'+''.join('# '+l+'\n' for l in session.splitlines())+'\n'
st=dh+'''def quantity_branch(quantity):
    # Recorded pause is immediately before the following condition.
    if quantity < 0:
        return "positive"
    else:
        return "not positive"

quantity = 3
source_command = ""
value_command = ""
condition_command = ""
break_command = ""
next_command = ""
continue_command = ""
'''
so=st.replace('if quantity < 0:', 'if quantity > 0:').replace('source_command = ""','source_command = "l"').replace('value_command = ""','value_command = "p quantity"').replace('condition_command = ""','condition_command = "p quantity < 0"').replace('break_command = ""','break_command = "b 5"').replace('next_command = ""','next_command = "n"').replace('continue_command = ""','continue_command = "c"')
code('debugger_usage','Inspect the supplied recorded pdb session: l shows breakpoint() before the branch, p shows quantity and quantity < 0, b 5 sets a breakpoint, n reveals the unexpected branch, and c resumes. Record the exact commands from that session in source_command, value_command, condition_command, break_command, next_command, and continue_command. Diagnose the wrong comparison, then repair quantity_branch so positive quantities return "positive" and all others "not positive". Keep quantity as the supplied input. The checker reads the six command strings and evaluates the repaired helper.',st,so,['[source_command, value_command, condition_command, break_command, next_command, continue_command, quantity_branch(quantity), quantity_branch(-quantity)]'])

st='''def add_label(label, labels=[]):
    labels.append(label)
    return labels

first_label = "blue"
second_label = "red"
# Instructor probes; leave unchanged.
first = add_label(first_label)
second = add_label(second_label)
supplied = []
explicit = add_label(first_label, supplied)
'''
so=st.replace('labels=[]','labels=None').replace('    labels.append(label)','    if labels is None:\n        labels = []\n    labels.append(label)')
code('safe_mutable_defaults','Repair add_label with a None default and per-call allocation only when labels is None. first and second must be separate single-label lists, with first unchanged by the second call. A supplied list must be updated and returned unchanged in identity. Keep the probes.',st,so,['[first, second, first is second, explicit, explicit is supplied]'])
a=assets['ws.sorting_with_key_functions']['files'][0]['content']
so=a.replace('pass  # TODO: return the lowercase label.','return record["label"].lower()').replace('ordered = None  # TODO: produce a new sorted list using the named key.','ordered = sorted(records, key=label_key)')
code('sorting_with_key_functions','Complete label_key(record) to return record["label"].lower(); assign ordered using sorted and this named function as key, in ascending order. Preserve original labels and quantities and do not mutate records. Equal lowercase labels must retain their original relative order. The checker reads ordered, records and whether they are different list objects.',a,so,['[ordered, records, ordered is records]'])
a=assets['ws.lambda_expressions']['files'][0]['content'];so=a.replace('ordered = None  # TODO: sorted with a single-expression lambda quantity key.','ordered = sorted(pairs, key=lambda pair: pair[1])')
code('lambda_expressions','Assign ordered to a new ascending quantity-sorted list of pairs using a one-parameter, single-expression lambda key accessing pair[1]. Keep pairs unchanged. The checker reads ordered.',a,so,['ordered'])
a=assets['ws.specific_exception_handlers']['files'][0]['content']
pre='missing_notice = "File missing"\nother_notice = "Other file operation failure"\n'
a=pre+a.replace('print("File missing")','print(missing_notice)').replace('print("Other file operation failure")','print(other_notice)')
so=pre+'try:\n    raise FileNotFoundError("missing-example.txt")\nexcept FileNotFoundError:\n    print(missing_notice)\nexcept OSError:\n    print(other_notice)\n'
# stdout is derived by actually running the reference.
code('specific_exception_handlers','Reorder only the except branches so the missing-file exception reaches the specific handler before OSError. Preserve both supplied recovery actions and notice variables. The output must be the supplied missing_notice exactly once, not other_notice.',a,so)
out=io.StringIO()
with contextlib.redirect_stdout(out):exec(so,{})
C['python.specific_exception_handlers'][3].append({'test_id':'t1','kind':'stdout_equals','spec':{'expected':out.getvalue().rstrip()},'visible':True,'message_on_fail':'Place the specific matching handler first; preserve its recovery message.'})
# Assignment-only anchor: reports carry original causal input names alongside diagnostic entries.
a=assets['ws.validation_vs_programming_errors']['files'][0]['content']
pre='numeric_text = "three"\nmisspelled_name = "quanity"\ninput_path = "orders.csv"\n'
so=pre+a
for name,value in {'input_category':'input failure','input_response':'request corrected numeric text','implementation_category':'implementation defect','implementation_response':'correct the misspelled name','access_category':'external operational failure','access_response':'report access failure'}.items():so=so.replace(name+' = ""',name+' = '+repr(value))
st=pre+a+'\ninput_evidence = ""\nimplementation_evidence = ""\naccess_evidence = ""\n'
so+='\ninput_evidence = numeric_text\nimplementation_evidence = misspelled_name\naccess_evidence = input_path\n'
code('validation_vs_programming_errors','Read the three supplied reports: unsuitable numeric_text fails conversion; misspelled_name causes NameError; inadequate rights for otherwise valid input_path cause PermissionError. Fill each category/response string. Use exactly these category labels: "input failure", "implementation defect", "external operational failure"; and response labels: "request corrected numeric text", "correct the misspelled name", "report access failure". Copy the causal evidence names into input_evidence, implementation_evidence, and access_evidence respectively. Do not run a filesystem operation. The checker reads each report\'s category, response and evidence.',st,so,['[input_category, input_response, input_evidence]','[implementation_category, implementation_response, implementation_evidence]','[access_category, access_response, access_evidence]'])
a=assets['ws.variadic_arguments_and_unpacking']['files'][0]['content'];so=a.replace('pass  # TODO: forward both argument collections and return the result','return target(*args, **kwargs)')
code('variadic_arguments_and_unpacking','Complete wrapper(*args, **kwargs) to return target(*args, **kwargs) without adding bindings. Preserve target(quantity, price=4). The checker calls wrapper(3, price=5), wrapper(3, 5), and wrapper(3), which must preserve supplied positional and keyword arguments and the target default.',a,so,calls=[('wrapper',[3],{'price':5}),('wrapper',[3,5],{}),('wrapper',[3],{})])

exec((B/'working/constrained_tasks.py').read_text())

result={k:p[k] for k in ['schema_version','path_id','batch_id']};result['kind']='interactions_part';result['tiles']=[]
for t,screen in zip(p['tiles'],sc['tiles']):
 dest={'tile_id':t['tile_id'],'interactions':[]};result['tiles'].append(dest);seen=set()
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  cid=s['concept_ids'][0];c=cs[cid];anchors=[a for a in s['anchors'] if '#assessment:' in a];measures=[]
  for a in anchors:
   cap=a.split('#assessment:')[1];aa=next(x for x in c['assessment_anchors'] if x['capability']==cap)
   measures.append({'concept_id':cid,'capability':cap,'fact_ids':aa['fact_ids']})
  if not measures:
   measures=[{'concept_id':cid,'capability':aa['capability'],'fact_ids':aa['fact_ids']} for aa in c['assessment_anchors']]
  feedback={'correct':{'message':'Correct. '+(c['practice_anchor']['success'] if s['type']=='hands_on' else 'Your answer follows the rule taught in the text.')},'incorrect':{'message':'Review the execution or relationships in the written example, then try again.'},'hints':['Trace the relevant relationship or operation one step at a time.','Compare your result with the stated input and required behavior.']}
  if cid not in seen:
   rem=next((r['step_id'] for r in screen.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:feedback['remediation_step_id']=rem
  seen.add(cid)
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'stretch' if s['type']=='hands_on' else ('intro' if len(dest['interactions'])==0 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':[a for a in s['anchors'] if '#practice' in a],'feedback':feedback}
  if ix['type']=='choice':
   prompt,correct,wrongs=Q[(t['tile_id'].split('.')[-1],s['step_id'].split('.')[-1])]
   # Alternate correct position deterministically, so option location is not a cue.
   opts=[(correct,'Correct. The stated rule applies here.')]+wrongs
   shift=len(dest['interactions'])%len(opts);opts=opts[shift:]+opts[:shift]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':f'o{i+1}','text':text} for i,(text,why) in enumerate(opts)]}
   ix['grading']={'correct_option_ids':[f'o{i+1}' for i,(text,why) in enumerate(opts) if text==correct],'option_feedback':{f'o{i+1}':{'message':why} for i,(text,why) in enumerate(opts)}}
  elif ix['type']=='classify':
   names=['ValueError','OSError','FileNotFoundError','KeyboardInterrupt','Exception']
   parents={n:getattr(__builtins__,n).__bases__[0].__name__ for n in names} if not isinstance(__builtins__,dict) else {}
   import builtins
   parents={n:getattr(builtins,n).__bases__[0].__name__ for n in names};bs=sorted(set(parents.values()));ids={name:'b'+str(i+1) for i,name in enumerate(bs)}
   ix['public']={'prompt':'Classify each exception class by its direct parent in the built-in hierarchy. Include the ordinary failure branch and the direct BaseException signal; do not substitute the root for a nearer parent.','buckets':[{'bucket_id':ids[b],'label':b} for b in bs],'items':[{'item_id':f'i{i+1}','text':n} for i,n in enumerate(names)]}
   ix['grading']={'assignments':{f'i{i+1}':ids[parents[n]] for i,n in enumerate(names)},'item_feedback':{f'i{i+1}':{'message':n+' is directly beneath '+parents[n]+'.'} for i,n in enumerate(names)}}
  else:
   prompt,starter,solution,tests=C[cid]
   ix['public']={'prompt':prompt,'runtime':{'kind':'python','version':runtime['version'],'packages':[]},'workspace':{'files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'entry':'main.py','asset_mounts':[]},'constraints':{k:c['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':tests}
  dest['interactions'].append({'step_id':s['step_id'],'interaction':ix})
(B/'interactions.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('wrote',len(result['tiles']),'tiles',sum(len(t['interactions']) for t in result['tiles']),'interactions')
