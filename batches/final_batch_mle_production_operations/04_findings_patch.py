import json,ast,re,copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations'); P=B/'interactions.json'
d=json.loads(P.read_text()); original=copy.deepcopy(d)
ix={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
def get(k): return ix['mle.tile.'+k]
def flat(k):
 s=get(k)['grading']['solution_files'][0]['content']; out=''
 for n in ast.parse(s).body:
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec': out+=ast.literal_eval(n.value.args[0])+'\n'
  else: out+=ast.get_source_segment(s,n)+'\n'
 return out
def supply(s): return '# Supplied infrastructure\nexec('+repr(s)+')\n\n'
def save(k,prefix,learn,tail,starter,prompt):
 i=get(k); i['public']['prompt']=prompt
 i['grading']['solution_files'][0]['content']=supply(prefix)+'# Learner section\n'+learn+'\n'+supply(tail)
 i['public']['workspace']['files'][0]['content']=supply(prefix)+'# Learner section: complete the TODOs\n'+starter+'\n'+supply(tail)
# Normalize and declared probabilities
k='080_082.s04';s=flat(k); a=s.index('ref_mean ='); b=s.index('def complete_summary')
prefix=s[:a]; learn=s[a:b]
for tag,data,values in [('ref','reference','ref_values'),('cur','production','cur_values')]:
 learn+=f"{tag}_proportions = {tag}_counts[0]/len({values})\n{tag}_categories = {{}}\nfor category in policy['declared_categories']:\n    {tag}_categories[category] = np.sum({data}['category']==category)/len({data}['category'])\n{tag}_classes = {{}}\nfor predicted_class in policy['declared_classes']:\n    {tag}_classes[predicted_class] = np.sum({data}['predicted_class']==predicted_class)/len({data}['predicted_class'])\n"
tail=s[b:].replace('mean,std,hist','mean,std,proportions,categories,classes').replace(' or hist is None',' or proportions is None').replace("hist[0]/len(values)",'proportions')
tail=re.sub(r"\{c:np.sum\(data\['category'\]==c\)/len\(data\['category'\]\) for c in policy\['declared_categories'\]\}",'categories',tail)
tail=re.sub(r"\{c:np.sum\(data\['predicted_class'\]==c\)/len\(data\['predicted_class'\]\) for c in policy\['declared_classes'\]\}",'classes',tail)
for tag in ['ref','cur']: tail=tail.replace(tag+'_std,'+tag+'_counts)',tag+'_std,'+tag+'_proportions,'+tag+'_categories,'+tag+'_classes)')
starter='\n'.join(n+' = None' for n in ['ref_mean','cur_mean','ref_std','cur_std','ref_counts','cur_counts','ref_proportions','cur_proportions','ref_categories','cur_categories','ref_classes','cur_classes'])+'\n'
save(k,prefix,learn,tail,starter,'Complete the numerical bin proportions and declared category/class probabilities as well as the means and ddof=0 standard deviations. Divide each series by its own window’s eligible total, and retain zero-probability declared categories/classes.')
k='080_082.s14';s=flat(k);a=s.index('category_deltas=');b=s.index('result=');prefix=s[:a]
learn="""ref_mean = np.mean(ref_values)
cur_mean = np.mean(cur_values)
ref_std = np.std(ref_values,ddof=0)
cur_std = np.std(cur_values,ddof=0)
reference_categories = ref_cats/ref_cat_n
current_categories = cur_cats/cur_cat_n
reference_bins = ref_bins/ref_n
current_bins = cur_bins/cur_n
category_distance = 0.5*np.sum(np.abs(reference_categories-current_categories))
numeric_distance = 0.5*np.sum(np.abs(reference_bins-current_bins))
category_drift = category_distance>0.20
numeric_drift = numeric_distance>0.20
"""
tail=s[b:]
for old,new in [('ref_cats/ref_cat_n','reference_categories'),('cur_cats/cur_cat_n','current_categories'),('ref_bins/ref_n','reference_bins'),('cur_bins/cur_n','current_bins'),('category_distance>0.20 if category_distance is not None else None','category_drift'),('numeric_distance>0.20 if numeric_distance is not None else None','numeric_drift')]:tail=tail.replace(old,new)
save(k,prefix,learn,tail,'\n'.join(line.split(' = ')[0]+' = None' for line in learn.strip().splitlines())+'\n','Calculate reference/current category and bin proportions using their respective totals, calculate each distance as 0.5*np.sum(np.abs(reference_proportions-current_proportions)), and calculate each feature verdict with distance>0.20. Also complete the eligible-window means and ddof=0 standard deviations.')
k='083_085.s06';s=flat(k);a=s.index('def quality');b=s.index('joined =');learn=s[a:b].replace('    cohort = {}','    cohort = {}\n    seen_prediction_ids = {}').replace('if key in cohort:','if key in seen_prediction_ids:',1).replace("        if row['eligible']", "        seen_prediction_ids[key] = row\n        if row['eligible']",1)
save(k,s[:a],learn,'result = quality(prediction_rows,label_rows)\n',"def quality(prediction_rows,label_rows):\n    # TODO preserve cohort, reject every duplicate ID, join bounded labels,\n    # record exclusions and calculate mature-only coverage/error/loss.\n    return None\n",'Complete quality(prediction_rows, label_rows): preserve the declared eligible cohort by prediction ID and timestamp; explicitly reject duplicate IDs; attach only cohort labels within the availability boundary; record excluded labels; calculate mature coverage, matched error proportion, loss mean and ddof=0 loss standard deviation; return a mature-cohort-only report.')
i=get(k)
# fixture derived from a supplied prediction, forcing both repeated rows outside eligibility
fixture=supply("outside_prediction = dict(prediction_rows[0], eligible=False)\noutside_duplicate_rows = [outside_prediction, dict(outside_prediction)]\n")
for f in [i['grading']['solution_files'][0],i['public']['workspace']['files'][0]]:f['content']+=fixture
# expected supplied by executing the implementation against the derived fixture in gate, predicate tests rejection
newtest=copy.deepcopy(i['grading']['tests'][0]);newtest['test_id']='excluded_prediction_duplicates';newtest['spec']={'expr':"quality(outside_duplicate_rows, label_rows)['status'] == 'duplicate_prediction'",'expected':True};i['grading']['tests'].append(newtest)
k='083_085.s11';s=flat(k);a=s.index('normal_valid=');prefix=s[:a];learn="""baseline_mean = np.mean(baseline)
baseline_std = np.std(baseline,ddof=0)
config = {'indicator':policy['indicator'],'baseline_window':policy['baseline_window'],'threshold':float(baseline_mean+4),'ddof':policy['ddof'],'owner':policy['owner'],'response':policy['response']}
with open('alert.yaml','w') as h: yaml.safe_dump(config,h)
with open('alert.yaml') as h: resolved=yaml.safe_load(h)
assert resolved == config
result = replay(resolved)
assert result[0]['records'] == []
assert result[1]['records'] == []
assert result[2]['records'] == [{'owner':resolved['owner'],'action':resolved['response']}]
""".replace('float(baseline_mean+4)','baseline_mean+4')
# NumPy scalar serialization needs conversion supplied dependency helper (learner threshold still computed)
prefix+="def serializable(config):\n    config=dict(config);config['threshold']=float(config['threshold']);return config\n"
learn=learn.replace('yaml.safe_dump(config,h)','yaml.safe_dump(serializable(config),h)')
save(k,prefix,learn,'',"baseline_mean = None\nbaseline_std = None\nconfig = None\nresolved = None\nresult = None\n# TODO construct config, safe roundtrip, inspect and assert replay records\n",'Compute the baseline statistics; construct the policy indicator, threshold, baseline window, ddof, owner and response mapping; safely write and reload alert.yaml; inspect the resolved fields; replay the windows; assert empty records for normal and equality windows and the exact configured owner/action record for the breached window.')
k='083_085.s16';s=flat(k);a=s.index('nonempty=');b=s.index('result = []');prefix=s[:a]+"rate_groups = list(range(len(matched_counts)))\n"
learn="""selected_rates = []
for group in rate_groups:
    rate = None
    if matched_counts[group]>0:
        rate = error_counts[group]/matched_counts[group]
    selected_rates = selected_rates+[rate]
selected_response = None
for row in evidence:
    if row['active_config'] != row['approved_config']:
        if row['matched_eligible_labels']>0:
            if row['supported_response'] in policy['permitted_responses']:
                selected_response = row['supported_response']
"""
save(k,prefix,learn,s[b:],"selected_rates = None\nselected_response = None\n# TODO guarded division per group, evidence-supported permitted response\n",'Build selected_rates from error_counts and matched_counts, using a separate denominator for each group and None when its denominator is zero. Inspect the release evidence and policy to select selected_response; do not execute recovery.')
k='086_089.s21';s=flat(k);a=s.index('def rates');b=s.index('checked_records=');prefix=s[:a];learn=s[a:b]
# assertions are actual executable predicates, not precomputed answer variables
learn+="""assert evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],fixtures['valid']['candidate']['registry_artifact_id'])['verdict']
assert evaluate(fixtures['boundary']['incumbent'],fixtures['boundary']['candidate'],fixtures['boundary']['candidate']['registry_artifact_id'])['verdict']
assert not evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],'model.unrelated')['verdict']
"""
# supply fixture iteration, learner assertion function so no untaught loop required
prefix+="def assert_failures(check_failure):\n    for name,pair in fixtures.items():\n        if name not in ['valid','boundary']: check_failure(pair)\n"
learn+="def check_failure(pair):\n    assert not evaluate(pair['incumbent'],pair['candidate'],pair['candidate']['registry_artifact_id'])['verdict']\nassert_failures(check_failure)\nresult = test_all(evaluate)\n"
save(k,prefix,learn,'',"def rates(model):\n    # TODO actual-class denominators, undefined guard, expected cost\n    return None\ndef evaluate(incumbent,candidate,requested_identity):\n    # TODO incumbent-relative quality, slice, compatibility, cohort, identity gates\n    return None\n# TODO executable success/equality/failure assertions\nresult = None\n",'Complete rates(model) and evaluate(incumbent, candidate, requested_identity). Calculate actual-class conditional rates and expected cost; reject undefined groups; enforce incumbent-relative cost, quality, slice, compatibility, cohort and exact-identity requirements. Then write executable assertions for valid, equality-boundary and declared failure cases and assign result=test_all(evaluate).')
k='091_094.s04';s=flat(k);a=s.index('mask =');b=s.index('result =');learn=s[a:b]
save(k,s[:a],learn,s[b:],'\n'.join(n+' = None' for n in ['mask','cpu','memory','cpu_mean','cpu_std','memory_mean','memory_std'])+'\n','Construct one mask for the declared instance, process, matching running process, RUNNING state and half-open interval. Use that same mask for CPU and memory, then calculate their means and ddof=0 standard deviations.')
k='091_094.s09';s=flat(k);a=s.index('allocated =');b=s.index('result =');learn=s[a:b]
learn+="allocated_total = sum([allocated['training']['w1'],allocated['training']['w2'],allocated['inference']['w1'],allocated['inference']['w2']])\nreconciled = allocated_total+unallocated == export_total\n"
tail=s[b:].replace("sum([allocated['training']['w1'],allocated['training']['w2'],allocated['inference']['w1'],allocated['inference']['w2']])",'allocated_total')
save(k,s[:a],learn,tail,"# TODO allocate each eligible charge, retain unmatched amounts and IDs;\n# build per-window totals and unusual flags, reconcile, summarize each series\nallocated = None\nunallocated = None\nexport_total = None\nunmatched = None\nsummary = None\nallocated_total = None\nreconciled = None\n",'Allocate each eligible charge using resource_mapping and shared_rule; retain unmatched amounts explicitly; calculate per-workload per-window totals, unusual flags and the allocated-plus-unallocated reconciliation. Then calculate each workload’s per-window mean and ddof=0 standard deviation.')
i=get(k);nt=copy.deepcopy(i['grading']['tests'][0]);nt['test_id']='reconciliation';nt['spec']={'expr':"result['allocated_total']+result['unallocated'] == result['export_total'] and reconciled",'expected':True};i['grading']['tests'].append(nt)
k='091_094.s14';s=flat(k);a=s.index('approved_config =');prefix=s[:a]
fields=['workload_scope','budget_amount','period','threshold_ratio','notification_topic','response_pipeline','INSTANCE','ZONE','authorized_identity','secret_version_reference']
learn='config = {'+','.join(repr(n)+":policy["+repr(n)+']' for n in fields)+"}\nconfig['secretEnv']=['BUDGET_CLIENT']\nconfig['event_binding']={'topic':policy['notification_topic'],'pipeline':policy['response_pipeline']}\nwith open('guardrail.yaml','w') as h: yaml.safe_dump(config,h)\nwith open('guardrail.yaml') as h: resolved=yaml.safe_load(h)\ninspected_scope = resolved['workload_scope']\ninspected_target = [resolved['INSTANCE'],resolved['ZONE']]\ninspected_binding = resolved['event_binding']\ninspected_secret = [resolved['secret_version_reference'],resolved['secretEnv']]\nresult=apply_and_replay(resolved)\n"
save(k,prefix,learn,'',"config = None\nresolved = None\nresult = None\n# TODO construct all policy fields, scoped secretEnv and event_binding;\n# safe write/reload and inspect resolved mapping before replay\n",'Construct config from the supplied policy: workload scope, amount, period, threshold, existing topic/pipeline binding, fixed authorized instance, identity and runtime secret reference with scoped secretEnv. Safely write and reload guardrail.yaml, inspect the resolved fields, and pass the resolved mapping to apply_and_replay.')
# remainder below: durable admission and recovery simulator
k='086_089.s16';s=flat(k);a=s.index('event_run_key =');prefix=s[:a]
# Critical sections use atomic mkdir and return the contract's busy status on contention.
prefix=prefix.replace("        os.mkdir('coordinator.lock')\n        try:","        try: os.mkdir('coordinator.lock')\n        except FileExistsError: return {'status':'busy','job_id':None,'completed':False}\n        try:",1)
# Overlap hook is invoked after durable commit/unlock but BEFORE the first atomic call returns.
# The second worker enters while the first worker's admission is still in flight.
prefix=prefix.replace("        finally: os.rmdir('coordinator.lock')", "        finally:\n            os.rmdir('coordinator.lock')\n            hook = getattr(self,'overlap_hook',None)\n            self.overlap_hook = None\n            if hook is not None: hook()",1)
prefix=prefix.replace("        os.mkdir('coordinator.lock')\n        try:\n            state=self.read()\n            if state['jobs']", "        try: os.mkdir('coordinator.lock')\n        except FileExistsError: return False\n        try:\n            state=self.read()\n            if state['jobs']",1)
# Executor never raises lock contention; pending token is reconciled through attach, never a new ID.
prefix=prefix.replace("        os.mkdir('coordinator.lock')\n        try:\n            state=self.coordinator.read()", "        try: os.mkdir('coordinator.lock')\n        except FileExistsError: return job\n        try:\n            state=self.coordinator.read()",1)
old="""    # Two independent coordinator clients, same delivery. Atomic coordinator serializes competing claims.
    a=admit(event,c1,e1);b=admit(event,c2,e2);out['same_key']={'results':[a,b],'state':durable_state()}
    b2=admit({'run_key':key+'2','pipeline':pipeline},c2,e2);out['different_key']={'result':b2,'state':durable_state()}
"""
new="""    # Deterministic overlapping worker attempts: worker 2 runs before worker 1's
    # atomic admission returns, with the first reservation already committed.
    # This is a cooperative concurrency fixture, not two sequential admit calls.
    second=[]
    c1.overlap_hook=lambda:second.append(admit(event,c2,e2))
    a=admit(event,c1,e1);b=second[0]
    state=durable_state()
    out['same_key']={'results':[a,b],'state':state}
    out['same_key']['logical_job_count']=len(state['jobs'])
    reset();c1,e1=fresh();c2,e2=fresh();second=[]
    c1.overlap_hook=lambda:second.append(admit({'run_key':key+'2','pipeline':pipeline},c2,e2))
    a=admit(event,c1,e1);b2=second[0];state=durable_state()
    out['different_key']={'result':b2,'state':state,'logical_job_count':len(state['jobs'])}
"""
assert old in prefix;prefix=prefix.replace(old,new)
learn="""def admit(event,coordinator,executor):
    claim = coordinator.atomic_admit(event['run_key'],event['pipeline'])
    if claim['status'] == 'busy':
        return {'status':'defer','job_id':claim['job_id']}
    elif claim['completed']:
        return {'status':'completed','job_id':claim['job_id']}
    elif claim['status'] == 'accepted':
        executor.launch(claim['job_id'])
    else:
        executor.attach(claim['job_id'])
    if executor.status(claim['job_id']) == 'terminal':
        coordinator.confirm_terminal_and_release(event['run_key'],claim['job_id'])
    return {'status':claim['status'],'job_id':claim['job_id']}
"""
a=s.index('    config =');b=s.index("    assert result['same_key']");tail='\n'.join(line[4:] for line in s[a:b].splitlines())+'\n'
asserts="""assert result['same_key']['results'][0]['job_id'] == result['same_key']['results'][1]['job_id']
assert result['same_key']['logical_job_count'] == 1
assert result['different_key']['result']['status'] == 'defer'
assert result['different_key']['logical_job_count'] == 1
assert result['restart_reservation']['result']['job_id'] == result['restart_launch']['result']['job_id']
assert result['restart_reservation']['state']['jobs'] == result['restart_launch']['state']['jobs']
assert result['completed_duplicate']['result']['status'] == 'completed'
assert result['completed_duplicate']['state']['slots'] == {}
"""
# assertions belong to learner section AFTER supplied fixture execution
save(k,prefix,learn,tail,"def admit(event,coordinator,executor):\n    # TODO atomic admission, busy/completed no-launch branches, persisted-token\n    # launch/reconciliation and terminal-only release\n    return None\n",'Complete admit(event, coordinator, executor). Atomically admit the event; defer busy claims without launch; return completed claims without relaunch; launch accepted claims with the persisted job ID; attach or reconcile duplicates with that same ID; release the slot only after confirmed terminal state. Add assertions over the supplied durable-state and logical-job-count fixtures. The supplied concurrency fixture overlaps two worker admission attempts and returns their durable records and logical-job counts.')
i=get(k);i['grading']['solution_files'][0]['content']+='\n# Learner assertions\n'+asserts;i['public']['workspace']['files'][0]['content']+='\n# TODO assertions over durable state and logical-job counts\n'
# Existing report test is subset-sensitive? preserve original test by grading projection
# extra count fields are tested separately, existing expected report remains identical
for f in [i['grading']['solution_files'][0],i['public']['workspace']['files'][0]]:
 f['content']+=supply("logical_job_counts={name:result[name].pop('logical_job_count') for name in ['same_key','different_key']}\n" )
nt=copy.deepcopy(i['grading']['tests'][0]);nt['test_id']='overlap_logical_jobs';nt['spec']={'expr':"logical_job_counts['same_key']==1 and logical_job_counts['different_key']==1",'expected':True};i['grading']['tests'].append(nt)
k='090_090.s05';s=flat(k);a=s.index('def recover');b=s.index('action0 =');prefix=s[:a]
# Fixture values and hypothesis success text are read from the registry dataset, not invented.
r=json.loads((B/'scenario_asset_registry.json').read_text());asset=next(a for a in r['assets'] if a['asset_id']=='ds.incident_evidence');cols=[c['name'] for c in asset['columns']];rows=[dict(zip(cols,row)) for row in asset['rows']];before=rows[0];after=rows[1]
simulator="""# Each symbolic action advances simulated state; no live commands execute.
def recover(actions, evidence_rows=None, stop_complete=True):
    rows=incident_evidence_rows if evidence_rows is None else evidence_rows
    before=rows[0]; after=rows[1]
    state={'instance_state':before['instance_state'],'process_state':before['process_state']}
    successful_hypothesis=False; stopped=False; reconnected=False; ready=False; prediction_pass=False
    def fail(check): return {'status':'failure','failed_check':check,'state':dict(state)}
    def truth(value): return value is True or value == 'True'
    for row in [before,after]:
        if row['INSTANCE']!=policy['INSTANCE'] or row['ZONE']!=policy['ZONE'] or row['authorized_identity']!=policy['authorized_identity']:
            return fail('authorized_same_target')
        if not truth(row['credential_review_pass']): return fail('credential_review')
    if actions != policy['allowed_actions']: return {'status':'invalid_sequence','actions':actions}
    for action in actions:
        if action=='inspect':
            if state['instance_state']!='RUNNING': return fail('initial_state')
        elif action=='reproduce_fault':
            if not before['fault_evidence'] or state['process_state']!='failed': return fail('fault_reproduction')
        elif action=='test_hypothesis':
            successful_hypothesis = before['hypothesis_result'] == SUCCESSFUL_HYPOTHESIS
            if not successful_hypothesis: return fail('hypothesis')
        elif action=='stop':
            if not successful_hypothesis: return fail('hypothesis')
            state['instance_state']='STOPPING'
        elif action=='wait_stopped':
            if not stop_complete: return fail('stop_completion')
            state['instance_state']='TERMINATED'; stopped=True
        elif action=='start':
            if not stopped or state['instance_state']!='TERMINATED': return fail('stop_completion')
            state['instance_state']='STARTING'
        elif action=='wait_running':
            if after['instance_state']!='RUNNING': return fail('running_poststate')
            state['instance_state']='RUNNING'
        elif action=='reconnect':
            if state['instance_state']!='RUNNING' or after['process_state']!='running': return fail('restored_process')
            state['process_state']=after['process_state']; reconnected=True
        elif action=='readiness':
            ready=reconnected and truth(after['readiness'])
            if not ready: return fail('readiness')
        elif action=='bounded_prediction':
            prediction_pass=ready and truth(after['prediction_contract_pass'])
            if not prediction_pass: return fail('bounded_prediction')
    if not (stopped and reconnected and ready and prediction_pass): return fail('incomplete_recovery')
    return {'target':policy['INSTANCE'],'zone':policy['ZONE'],'identity':policy['authorized_identity'],'before':before,'fault_evidence':before['fault_evidence'],'hypothesis_test':before['hypothesis_result'],'actions':actions,'after':after,'contract':policy['prediction_contract'],'credentials':'runtime-injected only; captured evidence reviewed'}
"""
prefix+='SUCCESSFUL_HYPOTHESIS = '+repr(before['hypothesis_result'])+'\n'+simulator
# Keep symbolic learner assignments and existing tests.
old_i=get(k);old_start=old_i['public']['workspace']['files'][0]['content'];start_flat=''
for n in ast.parse(old_start).body:
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec':start_flat+=ast.literal_eval(n.value.args[0])+'\n'
 else:start_flat+=ast.get_source_segment(old_start,n)+'\n'
learn=s[b:s.index('result = recover')];starter=start_flat[start_flat.index('action0 ='):start_flat.index('result = recover')]
tail=s[s.index('result = recover'):]
tail+="""failed_hypothesis_rows=[dict(incident_evidence_rows[0],hypothesis_result='failed'),dict(incident_evidence_rows[1])]
failed_service_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],prediction_contract_pass=False)]
failed_readiness_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],readiness=False)]
failure_records=[recover(policy['allowed_actions'],failed_hypothesis_rows),recover(policy['allowed_actions'],stop_complete=False),recover(policy['allowed_actions'],failed_service_rows),recover(policy['allowed_actions'],failed_readiness_rows)]
"""
save(k,prefix,learn,tail,starter,'Complete the symbolic command assignments for the declared target and recovery sequence. Each symbolic action advances a simulated state. Stop is permitted only after a successful hypothesis test; start is permitted only after confirmed stop completion; successful recovery requires the same authorized target to be running, restored process state, readiness and a passing bounded prediction exchange. Failed checks return a failure record.')
i=get(k);nt=copy.deepcopy(i['grading']['tests'][0]);nt['test_id']='failed_recovery_checks';nt['spec']={'expr':"[r.get('failed_check') for r in failure_records] == ['hypothesis','stop_completion','bounded_prediction','readiness']",'expected':True};i['grading']['tests'].append(nt)
# Advisory credential judgment: reword only, no key or claim changes.
i=get('086_089.s04');i['public']['prompt']="Read the handoff excerpt and decide which judgement is justified.\n```text\nCredentials arrive through runtime injection. YAML contains references only, not credential values. Captured logs omit the resolved values.\n```"
texts=['The excerpt preserves runtime-only credential handoff without values in YAML or captured logs.','The excerpt is incomplete because YAML should contain the credential value.','The excerpt is incomplete because captured logs should print the resolved value.']
for o,text in zip(i['public']['options'],texts):o['text']=text
# Audit excerpts are rewordings of existing option evidence/omissions.
i=get('091_094.s18');i['public']['prompt']='Inspect the three audit excerpts. Which record satisfies the cleanup evidence contract?'
texts=['Audit A: ownership verified; active and retired identities recorded; authorized actions recorded; retained artifacts recorded; credential non-disclosure checks recorded.','Audit B: container ages recorded; deletion count recorded. No ownership, identity, authorization, retained-artifact or credential review evidence recorded.','Audit C: removed names recorded; full resolved credential values copied into the audit.']
for o,text in zip(i['public']['options'],texts):o['text']=text
# The advisory points at 083_085/s09, but the named classification excerpt lives at 080_082/s09.
i=get('080_082.s09')
for item in i['public']['items']:item['text']='\n'.join(line for line in item['text'].splitlines() if not line.startswith('unresolved:'))
# Preserve every measure, anchor, constraint, type and original test.
for t,ot in zip(d['tiles'],original['tiles']):
 for e,oe in zip(t['interactions'],ot['interactions']):
  i=e['interaction'];oi=oe['interaction']
  for key in ['type','measures','anchors']:assert i.get(key)==oi.get(key),(e['step_id'],key)
  if i['type']=='code_exercise':
   assert i['public']['constraints']==oi['public']['constraints']
   assert i['grading']['tests'][:len(oi['grading']['tests'])]==oi['grading']['tests']
P.write_text(json.dumps(d,indent=2)+'\n')
print('Patched',sum(e!=oe for t,ot in zip(d['tiles'],original['tiles']) for e,oe in zip(t['interactions'],ot['interactions'])),'interactions')
