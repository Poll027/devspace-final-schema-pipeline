import json,ast,re,copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations');p=B/'interactions.json';d=json.loads(p.read_text());before=copy.deepcopy(d)
prompts={
'080_082.s04': 'Complete the marked eligible-value selection, bin proportions, declared category/class probabilities, numeric summary callbacks and record emission. Retain loading, record fields and identity binding; use each series’ own eligible total and the declared ddof=0 divisor.',
'080_082.s14': 'Complete the marked reference/current numeric summaries, category and bin probabilities, distances and threshold verdicts. Use each series’ own eligible total and distance > 0.20; retain the supplied result fields and quality limitation.',
'083_085.s06': 'Complete cohort construction, eligible-label joining, coverage, error proportion and loss-summary calculations inside quality. Retain duplicate rejection, loading, cutoff preparation and scoped output fields.',
'083_085.s11': 'Complete the baseline statistics, policy-derived config fields, safe YAML write/reload calls and replay assertions. Normal and exact-boundary windows must emit no records; a crossing must emit exactly the configured owner/action.',
'083_085.s16': 'Complete the conditional error-rate calculation and evidence-supported response selection in the existing loops. Report None for zero eligible labels, select approved_rollback only when the supplied mismatch/replay predicate holds, use none for baseline impact, and investigate otherwise. Retain readiness and bounded_prediction gates for rollback.',
'086_089.s16': 'Implement admit(event, coordinator, executor) using the supplied contracts. Atomically admit the event; defer busy claims, return completed claims without relaunching, launch accepted claims with the persisted job_id, attach duplicates and reconcile unknown responses using that same identity, and release only after confirmed terminal state.',
'086_089.s21': 'Complete rates(model) and evaluate(incumbent, candidate, requested_identity). Calculate actual-class conditional rates and policy-weighted expected cost; reject undefined conditioning groups and enforce incumbent-relative cost, both quality limits, slice, compatibility, declared cohort and exact artifact identity.',
'091_094.s04': 'Complete mask and the four summary assignments. Match the policy instance and process, running-process evidence, RUNNING state and the start-inclusive/end-exclusive interval; apply the same mask to CPU and memory.',
'091_094.s09': 'Complete the training/inference lifecycle sequences, charge-allocation branches, workload-specific summary calculations and reconciliation expression. Retain shared charges under policy fractions and unmatched amounts as explicitly unallocated.',
'091_094.s14': 'Construct config from the supplied policy, including scope, amount, period, threshold, topic/event binding, approved identity, runtime secret reference and fixed-target stop step; safely write, reload and inspect it before replay.'}
def sub(s,a,b):
 assert a in s,a
 return s.replace(a,b)
def assign_todos(s,names):
 for name in names:
  s,n=re.subn(r'(?m)^(\s*)('+re.escape(name)+r') = [^\n]+',r'\1\2 = None # TODO: complete this assignment',s)
 return s
def edit(s,k):
 if k=='080_082.s04' and 'def summarize' in s:
  s=sub(s,"values = values[(values >= policy['eligible_numeric_range'][0]) & (values <= policy['eligible_numeric_range'][1])]","values = None # TODO: select eligible numeric values")
  s=sub(s,'proportions = counts / len(values)','proportions = None # TODO: normalize bin counts by eligible total')
  s=sub(s,"categories[category] = np.sum(data['category'] == category) / len(data['category'])","categories[category] = None # TODO: declared-category probability")
  s=sub(s,"classes[predicted_class] = np.sum(data['predicted_class'] == predicted_class) / len(data['predicted_class'])","classes[predicted_class] = None # TODO: declared-class probability")
  s=sub(s,'    emit(record)','    pass # TODO: emit the identity-bound record')
 elif k=='080_082.s14':
  s=assign_todos(s,['ref_mean','cur_mean','ref_std','cur_std','reference_categories','current_categories','reference_bins','current_bins','category_distance','numeric_distance','category_drift','numeric_drift'])
 elif k=='083_085.s06' and 'def quality' in s:
  s=sub(s,"if row['eligible'] and row['cohort_id'] == policy['cohort']:","if None: # TODO: select eligible predictions in the declared cohort")
  s=sub(s,"if key in cohort and cohort[key]['prediction_timestamp'] <= cutoff and (row['label_timestamp'] <= policy['label_available_through']):","if None: # TODO: join eligible labels under maturity and availability cutoffs")
  for a,b in [("'coverage': len(matched) / len(cohort) if len(cohort) > 0 else None","'coverage': None"),("'coverage': len(matched) / len(cohort)","'coverage': None"),("'error_proportion': sum(errors) / len(matched)","'error_proportion': None"),("'loss_mean': mean_calculation(losses)","'loss_mean': None"),("'loss_std': std_calculation(losses, ddof=0)","'loss_std': None")]:s=sub(s,a,b)
  s=s.replace("    return {'status': 'mature_cohort_only'","    # TODO: complete coverage, error_proportion, loss_mean and loss_std below\n    return {'status': 'mature_cohort_only'")
  s=s.replace("        return {'status': 'unavailable'","        # TODO: complete coverage with its zero-total guard\n        return {'status': 'unavailable'")
 elif k=='083_085.s11':
  s=assign_todos(s,['baseline_mean','baseline_std'])
  if s.startswith('config ='):
   n=ast.parse(s).body[0]; vals=n.value.values
   for v in reversed(vals):
    lines=s.splitlines(True);start=sum(len(x) for x in lines[:v.lineno-1])+v.col_offset;end=sum(len(x) for x in lines[:v.end_lineno-1])+v.end_col_offset;s=s[:start]+'None'+s[end:]
   s+=' # TODO: derive all config fields from policy and baseline'
  s=s.replace('yaml.safe_dump(serializable(config), h)','pass # TODO: safely write serializable(config) with yaml.safe_dump')
  s=s.replace('resolved = yaml.safe_load(h)','resolved = None # TODO: reload with yaml.safe_load')
  if s.startswith('assert '):s='assert None # TODO: '+s
 elif k=='083_085.s16':
  s=s.replace('rollback_response = None','')
  s=s.replace('    rate = None\n    if matched_counts[group] > 0:\n        rate = error_counts[group] / matched_counts[group]','    rate = None # TODO: guarded error rate; None for zero eligible labels')
  s=s.replace('    response = label_investigate','    response = None # TODO: evidence-supported response selection')
  s=s.replace("    if mismatch_replay:\n        response = rollback_response\n        gates = ['readiness', 'bounded_prediction']\n    elif row['client_impact'] == 'baseline':\n        response = label_none", "    # TODO: select rollback only on mismatch_replay, none for baseline, investigate otherwise\n    # Rollback must retain these gates; other responses must retain empty gates.\n    if mismatch_replay:\n        response = None # TODO: select the supported response\n        gates = ['readiness', 'bounded_prediction']\n    else:\n        response = None # TODO: distinguish baseline impact from investigation")
 elif k=='086_089.s16':
  if 'def supplied_admit' in s:
   start=s.index('def supplied_admit');s=s[:start]+'''def admit(event, coordinator, executor):
    # TODO: atomically claim the event with its pipeline and run key.
    # TODO: defer busy claims; return completed claims without relaunching.
    # TODO: launch accepted claims with persisted job_id; attach duplicates.
    # TODO: reconcile unknown responses using the same persisted identity.
    # TODO: release only after confirmed terminal state.
    return {'status': None, 'job_id': None}
'''
  s=re.sub(r'(?m)^admit = None[^\n]*\n?', '',s)
 elif k=='086_089.s21':
  if 'def supplied_evaluate' in s:
   # Keep existing return fields, but delete completed calculations and predicates.
   s=sub(s,"if model['FP'] + model['TN'] == 0 or model['FN'] + model['TP'] == 0:","if None: # TODO: reject undefined actual-class conditioning groups")
   s=assign_todos(s,['fpr','fnr','inc','cand','quality','passed'])
   s=sub(s,"'cost': policy['P_Y0'] * fpr * policy['cost_FP'] + policy['P_Y1'] * fnr * policy['cost_FN']","'cost': None # TODO: policy-weighted expected cost\n    ")
   s=s.replace('def supplied_evaluate','def evaluate')
   s=sub(s,"if cand['cost'] != None and inc['cost'] != None:","if None: # TODO: require defined candidate and incumbent costs")
  s=re.sub(r'(?m)^evaluate = None[^\n]*\n?', '',s)
 elif k=='091_094.s04':s=assign_todos(s,['mask'])
 elif k=='091_094.s09':
  if s.startswith('sequences ='):s="sequences = {'training': None, 'inference': None} # TODO: lifecycle action sequences"
  s=assign_todos(s,["allocated['training'][window]","allocated['inference'][window]","allocated[workload][window]",'unallocated','reconciled']) if ('for row in charges:' in s or s.startswith('reconciled')) else s
  # Preserve initial unallocated zero; only loop updates are learner work.
 elif k=='091_094.s14':
  if s.startswith('config ='):
   n=ast.parse(s).body[0];changes=[]
   def placeholders(v):
    if isinstance(v,ast.Dict):
     for key,value in zip(v.keys,v.values):
      if ast.literal_eval(key) in ['name','secretEnv']:continue
      placeholders(value)
    elif isinstance(v,ast.List):
     # Preserve fixed command structure, remove only policy-derived target expressions.
     for v2 in v.elts:
      if not isinstance(v2,ast.Constant):placeholders(v2)
    else:changes.append(v)
   placeholders(n.value)
   for v in sorted(changes,key=lambda v:(v.lineno,v.col_offset),reverse=True):
    lines=s.splitlines(True);a=sum(len(x) for x in lines[:v.lineno-1])+v.col_offset;b=sum(len(x) for x in lines[:v.end_lineno-1])+v.end_col_offset;s=s[:a]+'None'+s[b:]
   s+=' # TODO: policy-derived fields, including INSTANCE/ZONE in fixed stop args'
  s=re.sub(r'(?m)^(safe_dump_interface|safe_load_interface|dump_config|load_config) = [^\n]*\n?', '',s)
  s=s.replace('dump_config(config, h)','pass # TODO: write config using yaml.safe_dump')
  s=s.replace('resolved = load_config(h)','resolved = None # TODO: reload config using yaml.safe_load')
 return s

def process(s,k):
 # Patch only named statements, including nested exec scaffold strings.
 out=[]
 for n in ast.parse(s).body:
  text=ast.get_source_segment(s,n)
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec' and isinstance(n.value.args[0],ast.Constant):
   inner=ast.literal_eval(n.value.args[0]);new=edit(inner,k)
   out.append(new if new!=inner else text)
  else:out.append(edit(text,k))
 return '\n\n'.join(x for x in out if x.strip())+'\n'
changed=[]
for t in d['tiles']:
 for x in t['interactions']:
  k=t['tile_id'].split('.')[-1]+'.'+x['step_id'].split('.')[-1];i=x['interaction']
  if k in prompts:
   i['public']['prompt']=prompts[k];f=i['public']['workspace']['files'][0];f['content']=process(f['content'],k);ast.parse(f['content']);changed.append(x['step_id'])
  elif k=='090_090.s05':
   old=i['public']['prompt'];print('LEAD-IN',old)
   i['public']['prompt']=re.sub(r'^Practice[^\n]*', 'Practice — Complete the symbolic action sequence under the supplied runbook and inspect the simulator’s recovery checks.',old,count=1);changed.append(x['step_id'])
# Ensure grading, anchors, constraints, all other entries remain untouched.
for oldt,newt in zip(before['tiles'],d['tiles']):
 for old,new in zip(oldt['interactions'],newt['interactions']):
  if old['step_id'] not in changed:assert old==new
  else:
   oi=copy.deepcopy(old);ni=copy.deepcopy(new)
   for item in [oi,ni]:
    item['interaction']['public'].pop('prompt',None)
    if 'workspace' in item['interaction']['public']: item['interaction']['public']['workspace']['files'][0].pop('content',None)
   assert oi==ni
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Changed',len(changed),'of',sum(len(t['interactions']) for t in d['tiles']))
