import ast, json, copy, sys
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations'); P=B/'interactions.json'
d=json.loads(P.read_text()); before=copy.deepcopy(d)
prompts={
'080_082.s04':'Implement summarize(reference, production, policy). Select eligible numeric observations; calculate fixed-edge bin proportions, means and ddof=0 standard deviations; calculate probabilities for every declared category and predicted class using each window’s own total; construct and emit exactly one monitoring record retaining the supplied identity, window, definitions and totals.',
'080_082.s14':'Complete the numeric summaries, aligned category probabilities, category and numeric-bin distances, and strict distance > 0.20 decisions. Use each window’s own eligible totals and retain the supplied comparison metadata and unresolved-quality wording.',
'083_085.s06':'Complete quality(prediction_rows, label_rows): reject duplicate prediction and label IDs, preserve eligible cohort records and prediction times, attach only available labels belonging to the mature cohort, record excluded label IDs, and return separate eligible/mature counts, coverage, matched error proportion and mature-loss mean/std with ddof=0. Report unavailable when no mature labels match.',
'083_085.s16':'Calculate each release/cohort’s error rate from its own matched eligible count, returning None for zero counts. Evaluate the configuration-mismatch hypothesis using active/approved identities and the supplied replay evidence, then select the policy-supported response and required gates without executing recovery.',
'086_089.s16':'Implement admit(event, coordinator, executor) using the supplied contracts. Defer busy claims; return completed claims without relaunching; launch accepted claims with their persisted job ID; attach or reconcile duplicates using that same identity; release only after terminal confirmation. Complete assertions over the supplied concurrency and restart results.',
'086_089.s21':'Implement rates(model) and evaluate(incumbent, candidate, requested_identity). Calculate actual-class conditional rates and expected cost, reject undefined conditioning groups, enforce incumbent-relative cost and every required quality/slice/compatibility/cohort/identity gate, and return the declared identity-bound record. Complete assertions for valid, equality-boundary and failing fixtures.',
'091_094.s09':'Complete the approved describe/start/connect/workload/stop/describe sequences for both tagged instances using the supplied lifecycle simulator. Allocate direct charges using the supplied mapping, shared charges using the explicit sharing rule, and unmatched charges as explicitly unallocated. Calculate the requested workload statistics and retain separate lifecycle windows, verified final states and reconciliation totals.',
'091_094.s14':'Complete the guardrail mapping from policy: workload scope, amount, period, threshold, existing event binding, approved fixed instance and runtime secret references. Safely serialize/reload it and inspect the resolved fields before passing it to the supplied notification/response simulator. Return its target-state and captured-output evidence with the delayed-notification limitation.'}
def unpack(code):
 out=[]
 for n in ast.parse(code).body:
  text=ast.get_source_segment(code,n)
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec':text=ast.literal_eval(n.value.args[0])
  out.append(text)
 return out

def name(text):
 n=ast.parse(text).body[0]
 if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name):return n.targets[0].id
 if isinstance(n,ast.FunctionDef):return n.name
 return ''
def todo_fn(text,comment):
 n=ast.parse(text).body[0]
 return text.splitlines()[0]+'\n    # TODO: '+comment+'\n    return None\n'
def assertion_todos(text):
 lines=text.splitlines()
 for idx,line in enumerate(lines):
  if line.lstrip().startswith('assert '):lines[idx]=line[:len(line)-len(line.lstrip())]+'assert False  # TODO: complete the invariant predicate for '+line.strip()[7:]
 # Do not give predicate in comment: replace with fixture scope only.
 for idx,line in enumerate(lines):
  if '# TODO: complete the invariant predicate for ' in line:
   predicate=line.split(' for ',1)[1]
   refs=[]
   for n in ast.walk(ast.parse('assert '+predicate)):
    if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value in ['same_key','different_key','restart_reservation','restart_launch','completed_duplicate','unknown_response','valid','boundary','model.unrelated']: refs.append(n.value)
   lines[idx]=line.split('# TODO:')[0]+'# TODO: assert '+(', '.join(dict.fromkeys(refs)) or 'the failing fixture')+' invariants.'
 return '\n'.join(lines)
for tile in d['tiles']:
 for step in tile['interactions']:
  key=step['step_id'].removeprefix('mle.tile.')
  if key not in prompts:continue
  ix=step['interaction']; ix['public']['prompt']=prompts[key]
  starter=ix['public']['workspace']['files'][0]; solution=ix['grading']['solution_files'][0]
  # Preserve all unchanged scaffold nodes byte-for-byte. Unwrap only edited logic in both files.
  ss=unpack(starter['content']); sol=unpack(solution['content']); assert len(ss)==len(sol),(key,len(ss),len(sol))
  orig_s=ast.parse(starter['content']).body; orig_sol=ast.parse(solution['content']).body
  new_s=[];new_sol=[]
  for i,(a,b) in enumerate(zip(ss,sol)):
   n=name(a); changed=False
   if key=='080_082.s04' and n in ['summary_mean','summary_std']:
    a=b; changed=True # NumPy aliases now supplied; learner implements whole function.
   elif key=='080_082.s04' and n=='summarize':
    a=todo_fn(a,'select eligible values, calculate window-specific summaries and totals, construct one record, emit it once and return it.');changed=True
   elif key=='080_082.s14' and n in ['ref_mean','cur_mean','ref_std','cur_std','reference_categories','current_categories','reference_bins','current_bins','category_distance','numeric_distance','category_drift','numeric_drift']:
    a=n+' = None  # TODO: calculate '+n+' under the declared policy.'; changed=True
   elif key=='083_085.s06' and n in ['summary_mean','summary_std']:
    a=b;changed=True
   elif key=='083_085.s06' and n=='quality':
    a=todo_fn(a,'reject duplicate IDs; preserve cohort rows/times; join mature available labels; record exclusions; return the scoped report or unavailable.');changed=True
   elif key=='083_085.s16' and n=='rollback_response':a=b;changed=True
   elif key=='083_085.s16' and a.startswith('for group in rate_groups:'):
    a='for group in rate_groups:\n    rate = None  # TODO: calculate using this group’s matched count; retain None for zero.\n    selected_rates = selected_rates + [rate]';changed=True
   elif key=='083_085.s16' and a.startswith('for row in evidence:'):
    lines=a.splitlines();start=next(j for j,l in enumerate(lines) if l.startswith('    response ='))
    a='\n'.join(lines[:start]+['    # TODO: evaluate identities and replay evidence; select response and required gates.','    response = None','    gates = None',lines[-1]]);changed=True
   elif key=='086_089.s16' and n=='busy_response':a=b;changed=True
   elif key=='086_089.s16' and n=='admit':
    a=todo_fn(a,'implement atomic admission, persisted identity reuse, unknown-response reconciliation and terminal-only release.');changed=True
   elif key=='086_089.s16' and a.startswith('assert '):a=assertion_todos(a);changed=True
   elif key=='086_089.s21' and n=='validation_cohort':a=b;changed=True
   elif key=='086_089.s21' and n in ['rates','evaluate']:
    a=todo_fn(a,'calculate conditional rates and cost.' if n=='rates' else 'apply all incumbent-relative, quality, slice, compatibility, cohort and identity gates; return the declared record.');changed=True
   elif key=='086_089.s21' and (a.startswith('assert ') or n=='check_failure'):a=assertion_todos(a);changed=True
   elif key=='091_094.s09' and n=='sequences':
    a="sequences = {'training': [], 'inference': []}  # TODO: complete both approved lifecycle sequences.";changed=True
   elif key=='091_094.s09' and a.startswith('for row in charges:'):
    lines=a.splitlines();a='\n'.join(lines[:4])+ '\n    # TODO: allocate shared/direct charges and record explicitly unallocated unmatched charges.\n';changed=True
   elif key=='091_094.s14' and n in ['target_instance','target_zone','config','inspected_scope','inspected_target','inspected_binding','inspected_secret']:
    if n=='config':
     node=ast.parse(a).body[0]; keys=ast.literal_eval(ast.Expression(node.value.keys[0])) if False else [ast.literal_eval(k) for k in node.value.keys]
     a='config = {\n'+''.join('    '+repr(k)+': None,  # TODO: resolve '+k+' from policy.\n' for k in keys)+'}'
    else:a=n+' = None  # TODO: '+('resolve from policy.' if n.startswith('target_') else 'inspect the corresponding reloaded fields.')
    changed=True
   elif key=='091_094.s14' and a.startswith("config['secretEnv']"):
    a="config['secretEnv'] = None  # TODO: runtime secret environment references.";changed=True
   elif key=='091_094.s14' and a.startswith("config['event_binding']"):
    a="config['event_binding'] = None  # TODO: bind the existing topic and response pipeline from policy.";changed=True
   elif key=='091_094.s14' and a.startswith('with open('):
    if 'safe_dump' in a:a=a.replace('yaml.safe_dump(config, h)','...  # TODO: safely serialize config to h.')
    else:a=a.replace('yaml.safe_load(h)','None  # TODO: safely reload from h.')
    changed=True
   new_s.append(a if changed else ast.get_source_segment(starter['content'],orig_s[i]))
   new_sol.append(b if changed else ast.get_source_segment(solution['content'],orig_sol[i]))
  header='# Complete the marked learner TODOs. Supplied loading, contracts and fixtures are scaffolding.\n'
  starter['content']=header+'\n\n'.join(new_s)+'\n';solution['content']=header+'\n\n'.join(new_sol)+'\n'
# Scope: prompts and code representation only; answer keys, tests, anchors, constraints, and measures unchanged.
for oldt,newt in zip(before['tiles'],d['tiles']):
 for old,new in zip(oldt['interactions'],newt['interactions']):
  if old==new:continue
  o=copy.deepcopy(old);nn=copy.deepcopy(new)
  for x in [o,nn]:
   x['interaction']['public'].pop('prompt');x['interaction']['public']['workspace']['files'][0].pop('content');x['interaction']['grading']['solution_files'][0].pop('content')
  assert o==nn
P.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('patched',len(prompts),'interactions; total',sum(len(t['interactions']) for t in d['tiles']))
