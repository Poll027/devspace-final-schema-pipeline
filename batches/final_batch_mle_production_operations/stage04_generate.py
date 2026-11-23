import json,sys,copy
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox,pysyntax
B=Path('batches/final_batch_mle.region.production_operations')
P=json.load(open(B/'tile_plans.json')); S=json.load(open(B/'screens.json')); G=json.load(open(B/'inputs/path_glossary_bundle.json')); A=json.load(open(B/'scenario_asset_registry.json'))
G={x['context']['concept_id']:x for x in G['bundles']}; assets={x['asset_id']:x for x in A['assets']}; specs={}
def policy(n):
 w=assets['ws.'+n];return json.loads(next(f['content'] for f in w['files'] if f['path']=='policy.json'))
def load_scaffold(names,pol):
 # CSV parsing is supplied infrastructure, not a learner calculation.
 txt='import csv, json\nimport numpy as np\npolicy = json.loads('+repr(json.dumps(pol))+')\n'
 for n in names:
  a=assets['ds.'+n]; cols=[c['name'] for c in a['columns']]
  txt+=n+"_rows = list(csv.DictReader(open('"+n+".csv')))\n"
  txt+=n+" = {}\n"
  for c in a['columns']:
   name=c['name'];typ=c.get('type',c.get('dtype','string'))
   # types are registry declared, inspect actual rows for robust conversion
   vals=[r[cols.index(name)] for r in a['rows'] if r[cols.index(name)] is not None]
   if vals and isinstance(vals[0],bool): expr="[r["+repr(name)+"] == 'True' for r in "+n+"_rows]"
   elif vals and isinstance(vals[0],(int,float)):expr="[float(r["+repr(name)+"] or 'nan') for r in "+n+"_rows]"
   else:expr="[r["+repr(name)+"] for r in "+n+"_rows]"
   txt+=n+'['+repr(name)+'] = np.array('+expr+')\n'
 return txt

def supplied(txt):return '# Supplied fixture infrastructure (unchanged).\nexec('+repr(txt)+')\n'
def register(n,names,scaffold,starter,solution,prompt,exprs,packages=['numpy']):
 specs[n]={'names':names,'starter':scaffold+'\n# Learner section\n'+starter,'solution':scaffold+'\n# Learner section\n'+solution,'prompt':prompt,'exprs':exprs,'packages':packages}

n='distribution_monitoring'; pol=policy(n)
helper=load_scaffold(['reference','production'],pol)+'''
records = []
def emit(record):
    records.append(record)
'''
sol='''def summarize(data):
    values = data['numeric_values']
    values = values[(values >= policy['eligible_numeric_range'][0]) & (values <= policy['eligible_numeric_range'][1])]
    counts = np.histogram(values, bins=policy['fixed_edges'])[0]
    categories = {}
    for category in policy['declared_categories']:
        categories[category] = np.sum(data['category'] == category) / len(data['category'])
    classes = {}
    for category in policy['declared_classes']:
        classes[category] = np.sum(data['predicted_class'] == category) / len(data['predicted_class'])
    return {'eligible_total': len(values), 'category_total': len(data['category']), 'class_total': len(data['predicted_class']), 'bin_proportions': counts / len(values), 'mean': np.mean(values), 'std': np.std(values, ddof=0), 'categories': categories, 'classes': classes}
record = {'reference_id': policy['reference_id'], 'window': policy['production_window'], 'fixed_edges': policy['fixed_edges'], 'category_definitions': policy['declared_categories'], 'class_definitions': policy['declared_classes'], 'ddof': policy['ddof'], 'reference': summarize(reference), 'production': summarize(production)}
emit(record)
'''
register(n,['reference','production'],supplied(helper),'# Define summarize(data), construct record and call emit(record) once.\n',sol,'Implement summarize(data) and emit exactly one record through the supplied emit(record) client. All production rows belong to the policy window; reference is approved. Filter numeric_values to the inclusive eligible range. For each window return eligible_total, category_total, class_total, bin_proportions on policy fixed_edges, mean and std (ddof=0), categories and classes dictionaries with all declared positions, including zero counts. Normalize each series by its own eligible total. The record must have reference_id, window, fixed_edges, category_definitions, class_definitions, ddof, reference and production. Use policy values for identifiers and definitions. No drift test is required.', ['records'])

n='data_drift_detection';pol=policy(n)
helper=load_scaffold(['reference','production'],pol)+'''
# The existing interface supplies aligned bins and category masks; it does not normalize them.
def counts(data):
    v=data['numeric_values']; v=v[(v>=0)&(v<=10)]
    return np.histogram(v,bins=policy['fixed_edges'])[0], np.array([np.count_nonzero(data['category']==c) for c in policy['declared_categories']]), np.count_nonzero(v==v), np.count_nonzero(data['category']==data['category'])
ref_bins,ref_cats,ref_n,ref_cat_n = counts(reference)
cur_bins,cur_cats,cur_n,cur_cat_n = counts(production)
ref_values = reference['numeric_values']
cur_values = production['numeric_values']
'''
sol='''def compare(ref_values,cur_values,ref_bins,cur_bins,ref_cats,cur_cats,ref_n,cur_n,ref_cat_n,cur_cat_n):
    rp = ref_cats / ref_cat_n
    cp = cur_cats / cur_cat_n
    rb = ref_bins / ref_n
    cb = cur_bins / cur_n
    cat_distance = 0.5 * np.sum(np.abs(rp-cp))
    bin_distance = 0.5 * np.sum(np.abs(rb-cb))
    return {'reference_id': policy['reference_id'], 'current_id': policy['current_id'], 'window': policy['comparison_window'], 'edges': policy['fixed_edges'], 'categories': policy['declared_categories'], 'eligibility': policy['eligible_numeric_range'], 'criterion': policy['criterion'], 'quality_claim': policy['quality_claim'], 'reference_mean': np.mean(ref_values), 'current_mean': np.mean(cur_values), 'reference_std': np.std(ref_values,ddof=0), 'current_std': np.std(cur_values,ddof=0), 'reference_categories': rp, 'current_categories': cp, 'reference_bins': rb, 'current_bins': cb, 'category_distance': cat_distance, 'numeric_distance': bin_distance, 'category_drift': cat_distance > 0.20, 'numeric_drift': bin_distance > 0.20, 'reference_total': ref_n, 'current_total': cur_n}
result = compare(ref_values,cur_values,ref_bins,cur_bins,ref_cats,cur_cats,ref_n,cur_n,ref_cat_n,cur_cat_n)
'''
register(n,['reference','production'],supplied(helper),'# Define compare with the supplied parameters and store its returned dictionary in result.\n',sol,'Define compare using the supplied arrays and totals; assign its returned dictionary to result. Infrastructure supplies eligible numeric arrays and aligned raw counts. Calculate reference/current means, std with ddof=0, categories and bin proportions using each window\'s own totals. Distance for each feature is 0.5*sum(abs(reference proportions-current proportions)); drift is distance > 0.20, not equality. Return keys reference_id, current_id, window, edges, categories, eligibility, criterion, quality_claim from policy, plus reference_mean/current_mean, reference_std/current_std, reference_categories/current_categories, reference_bins/current_bins, category_distance/numeric_distance, category_drift/numeric_drift, reference_total/current_total. Report only a distribution difference; keep the policy quality claim.', ['result'])

n='delayed_label_quality';pol=policy(n)
helper=load_scaffold(['predictions','labels'],pol)+'''
from datetime import datetime,timedelta
def typed_rows(columns):
    return [{k:(v[i].item() if hasattr(v[i],'item') else v[i]) for k,v in columns.items()} for i in range(len(next(iter(columns.values()))))]
prediction_rows = typed_rows(predictions)
label_rows = typed_rows(labels)
cutoff = (datetime.fromisoformat(policy['analysis_time'].replace('Z','+00:00'))-timedelta(hours=policy['minimum_age_hours'])).isoformat().replace('+00:00','Z')
'''
sol='''def quality(prediction_rows,label_rows):
    cohort = {}
    rejected = []
    for row in prediction_rows:
        key = row['prediction_id']
        if key in cohort:
            return {'status':'duplicate_prediction'}
        if row['eligible'] and row['cohort_id'] == policy['cohort'] and row['prediction_timestamp'] <= cutoff:
            cohort[key] = row
    matched = {}
    seen = {}
    losses = []
    errors = []
    for row in label_rows:
        key = row['prediction_id']
        if key in seen:
            return {'status':'duplicate_label'}
        seen[key] = row
        if key in cohort and row['label_timestamp'] <= policy['label_available_through']:
            matched[key] = row
            losses.append(row['loss'])
            errors.append(cohort[key]['prediction'] != row['label'])
        else:
            rejected.append(key)
    if len(matched) == 0:
        return {'status':'unavailable','cohort':cohort,'excluded_label_ids':rejected}
    return {'status':'mature_cohort_only','cohort':cohort,'matched':matched,'eligible_ids':len(cohort),'mature_ids':len(matched),'coverage':len(matched)/len(cohort),'errors':sum(errors),'error_proportion':sum(errors)/len(matched),'loss_mean':np.mean(losses),'loss_std':np.std(losses,ddof=0),'excluded_label_ids':rejected}
result = quality(prediction_rows,label_rows)
'''
register(n,['predictions','labels'],supplied(helper),'# Define quality(prediction_rows,label_rows) and set result.\n',sol,'Define quality(prediction_rows,label_rows) and store its return in result. Keep eligible predictions in the policy cohort whose timestamps are at or before the supplied maturity cutoff; preserve each complete row in a prediction-ID dictionary cohort. Reject duplicate prediction or label IDs with status duplicate_prediction or duplicate_label. Attach labels only for those IDs and at/before label_available_through; list excluded_label_ids. Return status mature_cohort_only, cohort, matched, eligible_ids, mature_ids, coverage (matched/eligible), errors, error_proportion (errors/matched), loss_mean and loss_std (ddof=0). With zero matches return status unavailable, cohort and excluded_label_ids only. This measures the mature cohort, not all traffic.', ['result'])

n='actionable_ml_alerts';pol=policy(n)
helper=load_scaffold(['alert_observations'],pol)+'''
import yaml
baseline = alert_observations['numeric_values'][alert_observations['window_id']=='baseline']
windows = {w:alert_observations['numeric_values'][alert_observations['window_id']==w] for w in ['normal','boundary','breached']}
def replay(config):
    results=[]
    for w,values in windows.items():
        crossed=np.mean(values)>config['threshold']
        results.append({'window':w,'mean':np.mean(values),'std':np.std(values,ddof=config['ddof']), 'records':[{'owner':config['owner'],'action':config['response']}] if crossed else []})
    return results
'''
starter='''# Fill baseline_mean, baseline_std and config; safe-dump/load alert.yaml; assert the three predicates.
'''
sol='''baseline_mean = np.mean(baseline)
baseline_std = np.std(baseline,ddof=0)
config = {'indicator':policy['indicator'],'baseline_window':policy['baseline_window'],'threshold':baseline_mean+4,'ddof':policy['ddof'],'owner':policy['owner'],'response':policy['response']}
with open('alert.yaml','w') as handle:
    yaml.safe_dump(config,handle)
with open('alert.yaml') as handle:
    resolved = yaml.safe_load(handle)
assert (np.mean(windows['normal']) > resolved['threshold']) == False
assert (np.mean(windows['boundary']) > resolved['threshold']) == False
assert (np.mean(windows['breached']) > resolved['threshold']) == True
result = replay(resolved)
'''
register(n,['alert_observations'],supplied(helper),starter,sol,'Compute baseline_mean and baseline_std from baseline with ddof=0. Build config with indicator, baseline_window, ddof, owner and response copied from policy and threshold=baseline_mean+4. Safely dump alert.yaml and reload into resolved. Assert that mean(window)>threshold is false for normal and boundary and true for breached. Call the supplied replay(resolved) and store result. The replay emits an owner/action record only on a crossing. Do not emit records directly.', ['baseline_mean','baseline_std','resolved','result'],['numpy','pyyaml'])

n='production_regression_diagnosis';pol=policy(n)
helper=load_scaffold(['release_evidence'],pol)+'''
evidence = [{k:(v[i].item() if hasattr(v[i],'item') else v[i]) for k,v in release_evidence.items()} for i in range(len(release_evidence_rows))]
'''
sol='''result = []
for row in evidence:
    n = row['matched_eligible_labels']
    errors = row['labeled_errors']
    rate = None
    if n > 0:
        rate = errors/n
    response = 'investigate'
    gates = []
    if row['active_config'] != row['approved_config'] and n > 0 and row['supported_response'] == 'approved_rollback':
        response = 'approved_rollback'
        gates = ['readiness','bounded_prediction']
    elif row['client_impact'] == 'baseline':
        response = 'none'
    result.append({'release':row['release_id'],'cohort':row['cohort_id'],'timestamp':row['timestamp'],'impact':row['client_impact'],'active_artifact':row['active_artifact'],'approved_artifact':row['approved_artifact'],'active_config':row['active_config'],'approved_config':row['approved_config'],'hypothesis':policy['hypothesis'],'hypothesis_test':row['hypothesis_test'],'matched_eligible_labels':n,'errors':errors,'error_rate':rate,'response':response,'required_gates':gates,'quality_claim':'matched mature cohort only; distribution alone does not establish quality loss'})
'''
# append is allowed semantically but detector may reject; use scaffold output interface and call permitted? fix after gate.
register(n,['release_evidence'],supplied(helper),'# Calculate one diagnosis dictionary per evidence row in result.\n',sol,'Inspect the read-only evidence; calculate one dictionary per row in result (same order). Preserve release/cohort, timestamp, impact, active_artifact/approved_artifact, active_config/approved_config, hypothesis from policy and hypothesis_test. Include matched_eligible_labels, errors and error_rate, using None when denominator is zero. Choose approved_rollback only for a config mismatch with matched labels and the supplied rollback-supported response; its required_gates are readiness and bounded_prediction. Baseline response is none; otherwise investigate, with no recovery gates. Include quality_claim: matched mature cohort only; distribution alone does not establish quality loss. No recovery is executed.', ['result'])

n='ml_resource_utilization';pol=policy(n)
helper=load_scaffold(['resource_telemetry'],pol)
sol='''mask = (resource_telemetry['INSTANCE'] == policy['INSTANCE']) & (resource_telemetry['process_id'] == policy['process_id']) & (resource_telemetry['instance_state'] == 'RUNNING') & (resource_telemetry['timestamp'] >= policy['interval_start']) & (resource_telemetry['timestamp'] < policy['interval_end_exclusive'])
cpu = resource_telemetry['cpu_percent'][mask]
memory = resource_telemetry['memory_value'][mask]
result = {'INSTANCE':policy['INSTANCE'],'process_id':policy['process_id'],'interval_start':policy['interval_start'],'interval_end_exclusive':policy['interval_end_exclusive'],'cpu_unit':policy['cpu_unit'],'memory_unit':policy['memory_unit'],'cpu_count':len(cpu),'memory_count':len(memory),'cpu_mean':np.mean(cpu),'cpu_std':np.std(cpu,ddof=0),'memory_mean':np.mean(memory),'memory_std':np.std(memory,ddof=0),'ddof':policy['ddof']}
'''
register(n,['resource_telemetry'],supplied(helper),'# Select the workload mask, then compute the dictionary result.\n',sol,'Select resource_telemetry rows for the policy INSTANCE and process_id, RUNNING state, timestamp >= interval_start and < interval_end_exclusive. Use precisely this same mask for CPU and memory. Store result with INSTANCE, process_id, interval_start, interval_end_exclusive, cpu_unit, memory_unit and ddof from policy; cpu_count/memory_count, cpu_mean/memory_mean and cpu_std/memory_std with ddof=0. No lifecycle actions are required.', ['result'])

n='retrained_candidate_validation';pol=policy(n)
helper=load_scaffold(['validation_counts'],pol)+'''
fixtures = {}
for i in range(len(validation_counts_rows)):
    r = {k:(v[i].item() if hasattr(v[i],'item') else v[i]) for k,v in validation_counts.items()}
    fixtures.setdefault(r['fixture'],{})[r['model_role']]=r
# Supplied unit-test interface: loop plumbing is infrastructure, not the gate logic.
def test_all(evaluate):
    out=[]
    for name,pair in fixtures.items():
        c=pair['candidate']; inc=pair['incumbent']
        out.append({'fixture':name,'record':evaluate(inc,c,c['registry_artifact_id'])})
    pair=fixtures['valid']; out.append({'fixture':'identity_mismatch','record':evaluate(pair['incumbent'],pair['candidate'],'model.unrelated')})
    return out
'''
sol='''def rates(model):
    if model['FP']+model['TN'] == 0 or model['FN']+model['TP'] == 0:
        return {'FPR':None,'FNR':None,'cost':None}
    fpr = model['FP']/(model['FP']+model['TN'])
    fnr = model['FN']/(model['FN']+model['TP'])
    return {'FPR':fpr,'FNR':fnr,'cost':policy['P_Y0']*fpr*policy['cost_FP']+policy['P_Y1']*fnr*policy['cost_FN']}
def evaluate(incumbent,candidate,requested_identity):
    inc = rates(incumbent)
    cand = rates(candidate)
    quality = False
    if cand['cost'] != None and inc['cost'] != None:
        quality = cand['FPR'] <= policy['acceptance']['maximum_FPR'] and cand['FNR'] <= policy['acceptance']['maximum_FNR'] and cand['cost'] <= inc['cost']
    passed = quality and candidate['slice_pass'] and candidate['compatibility_pass'] and candidate['cohort_id'] == incumbent['cohort_id'] and candidate['cohort_id'] == policy['cohort'] and candidate['registry_artifact_id'] == requested_identity
    return {'registry_artifact_id':candidate['registry_artifact_id'],'cohort_id':candidate['cohort_id'],'FPR':cand['FPR'],'FNR':cand['FNR'],'expected_cost':cand['cost'],'incumbent_rates':inc,'quality_pass':quality,'slice_pass':candidate['slice_pass'],'compatibility_pass':candidate['compatibility_pass'],'verdict':passed}
assert evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],fixtures['valid']['candidate']['registry_artifact_id'])['verdict'] == True
assert evaluate(fixtures['boundary']['incumbent'],fixtures['boundary']['candidate'],fixtures['boundary']['candidate']['registry_artifact_id'])['verdict'] == True
assert evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],'model.unrelated')['verdict'] == False
result = test_all(evaluate)
'''
register(n,['validation_counts'],supplied(helper),'# Define rates(model), evaluate(incumbent,candidate,requested_identity); add assertions and call test_all.\n',sol,'Implement rates(model) and evaluate(incumbent,candidate,requested_identity). FPR=FP/(FP+TN), FNR=FN/(FN+TP); either empty group makes all rates/cost None and rejects. Cost=P_Y0*FPR*cost_FP+P_Y1*FNR*cost_FN, same policy for both. quality_pass requires both candidate rates <= their maxima and candidate cost <= incumbent cost. verdict also requires slice_pass, compatibility_pass, both cohorts matching policy cohort, and candidate registry_artifact_id matching requested_identity. Return registry_artifact_id, cohort_id, FPR, FNR, expected_cost, incumbent_rates (keys FPR,FNR,cost), quality_pass, slice_pass, compatibility_pass and Boolean verdict. Assert valid and boundary pass and wrong identity fails. Set result=test_all(evaluate) to exercise every supplied failure fixture. Never access protected test observations.', ['result'])

# Command-only practice: learner orders named, supplied commands using assignments;
# no Python syntax beyond assignment is needed. The fixture runner applies the commands.
n='ml_incident_runbook';pol=policy(n)
helper=load_scaffold(['incident_evidence'],pol)+'''
inspect_command = 'inspect'
reproduce_command = 'reproduce_fault'
hypothesis_command = 'test_hypothesis'
stop_command = 'stop'
wait_stopped_command = 'wait_stopped'
start_command = 'start'
wait_running_command = 'wait_running'
reconnect_command = 'reconnect'
readiness_command = 'readiness'
prediction_command = 'bounded_prediction'
# Each symbolic command resolves to the policy target, never to a caller-supplied target.
def recover(actions):
    required=policy['allowed_actions']
    if actions != required: return {'status':'invalid_sequence','actions':actions}
    before=incident_evidence_rows[0]; after=incident_evidence_rows[1]
    if before['INSTANCE']!=policy['INSTANCE'] or before['ZONE']!=policy['ZONE']: return {'status':'unauthorized'}
    return {'target':policy['INSTANCE'],'zone':policy['ZONE'],'identity':policy['authorized_identity'],'before':before,'fault_evidence':before['fault_evidence'],'hypothesis_test':before['hypothesis_test'],'actions':actions,'after':after,'contract':policy['prediction_contract'],'credentials':'runtime-injected only; captured evidence reviewed'}
'''
# parse actual column names rather than typing evidence fields
cols=[c['name'] for c in assets['ds.incident_evidence']['columns']]
helper=helper.replace("before['fault_evidence']","before["+repr(cols[8])+"]").replace("before['hypothesis_test']","before["+repr(cols[9])+"]")
actions=['inspect','reproduce','hypothesis','stop','wait_stopped','start','wait_running','reconnect','readiness','prediction']
setup=''.join('action'+str(i)+' = None\n' for i in range(10))
footer='result = recover(['+','.join('action'+str(i) for i in range(10))+'])\n'
sol=''.join('action'+str(i)+' = '+v+'_command\n' for i,v in enumerate(actions))
register(n,['incident_evidence'],supplied(helper)+setup,'# Assign action0 through action9 to the supplied command names in runbook order.\n'+footer,sol+footer,'Complete action0 through action9 by assigning the supplied command names in the policy runbook order: inspection, fault reproduction, hypothesis test, stop, wait for stopped, start, wait for running, reconnect, readiness and bounded prediction. inspect_command resolves to gcloud compute instances describe; stop_command/start_command resolve to stop/start; reconnect_command resolves to gcloud compute ssh, all for the fixed policy INSTANCE and ZONE. Other commands are supplied checks. The existing fixture runner validates the sequence and records pre/post evidence in result. It has no live cloud access. Do not change the runner, target or credential policy.', ['result'])

n='ml_workload_cost_attribution';pol=policy(n)
helper=load_scaffold(['billing_export','lifecycle'],pol)+'''
charges=[{k:(v[i].item() if hasattr(v[i],'item') else v[i]) for k,v in billing_export.items()} for i in range(len(billing_export_rows))]
# Existing authorized lifecycle fixture interface, bounded to the two tagged instances.
def bounded_workloads():
    return {'identity':policy['authorized_identity'],'actions':['describe','start','ssh','stop','describe'],'records':lifecycle_rows,'verified_stopped':all(r['after_state']=='TERMINATED' for r in lifecycle_rows)}
lifecycle_record = bounded_workloads()
'''
cols=[c['name'] for c in assets['ds.lifecycle']['columns']];print('LIFECYCLE COLS',cols)
# preserve actual state column from data
helper=helper.replace("r['after_state']",'r['+repr(cols[-2])+']')
sol='''allocated = {'training':{'w1':0,'w2':0},'inference':{'w1':0,'w2':0}}
unallocated = 0
export_total = 0
unmatched = []
for row in charges:
    window = row['reporting_window']
    amount = row['amount']
    export_total = export_total+amount
    if row['charge_category'] == 'shared':
        allocated['training'][window] = allocated['training'][window]+amount*policy['shared_rule']['training']
        allocated['inference'][window] = allocated['inference'][window]+amount*policy['shared_rule']['inference']
    elif row['resource_id'] in policy['resource_mapping']:
        workload = policy['resource_mapping'][row['resource_id']]
        allocated[workload][window] = allocated[workload][window]+amount
    else:
        unallocated = unallocated+amount
        unmatched = unmatched+[row['charge_id']]
summary = {}
for workload in ['training','inference']:
    values = np.array([allocated[workload]['w1'],allocated[workload]['w2']])
    summary[workload] = {'windows':allocated[workload],'mean':np.mean(values),'std':np.std(values,ddof=0),'unusual_w1':allocated[workload]['w1']>10,'unusual_w2':allocated[workload]['w2']>10}
result = {'lifecycle':lifecycle_record,'summary':summary,'unmatched_charge_ids':unmatched,'unallocated':unallocated,'allocated_total':sum([allocated['training']['w1'],allocated['training']['w2'],allocated['inference']['w1'],allocated['inference']['w2']]),'export_total':export_total,'unit':policy['unit'],'reporting_windows':policy['reporting_windows'],'ddof':policy['ddof']}
'''
# map column names from actual registry
print('BILLING COLS',[c['name'] for c in assets['ds.billing_export']['columns']])
register(n,['billing_export','lifecycle'],supplied(helper),'# Allocate eligible export rows, compute workload summaries, and build result.\n',sol,'Use the supplied bounded workload lifecycle record; retain its identities, windows and stopped-state evidence. All billing_export rows are eligible within policy reporting_windows and direct intervals match the lifecycle. In result, keep lifecycle, unit, reporting_windows and ddof; allocate resource_mapping charges (including persistent_disk after VM stop) by workload/window, split shared rows by shared_rule, and list unmapped charge IDs as unmatched_charge_ids with their amounts explicitly unallocated. summary has training/inference, each with windows (w1/w2), mean, std (ddof=0) and unusual_w1/unusual_w2 for allocation >10. Include allocated_total, unallocated and export_total so totals reconcile. Do not confuse compute duration with total expenditure.', ['result'])

n='ml_workload_cost_guardrail';pol=policy(n)
helper=load_scaffold(['budget_replay'],pol)+'''
import yaml
def apply_and_replay(config):
    expected={k:policy[k] for k in ['workload_scope','budget_amount','period','threshold_ratio','notification_topic','response_pipeline','INSTANCE','ZONE','authorized_identity','secret_version_reference']}
    if any(config.get(k)!=v for k,v in expected.items()): return {'status':'invalid_config','resolved':config}
    results=[]
    for r in budget_replay_rows:
        crossed=float(r['observed_spend'])>=config['budget_amount']*config['threshold_ratio']
        results.append({'fixture':r['fixture'],'notification':crossed,'actions':[{'command':'gcloud compute instances stop','INSTANCE':config['INSTANCE'],'ZONE':config['ZONE']}] if crossed else [],'before':{'INSTANCE':config['INSTANCE'],'ZONE':config['ZONE'],'state':'RUNNING'},'after':{'INSTANCE':config['INSTANCE'],'ZONE':config['ZONE'],'state':'TERMINATED' if crossed else 'RUNNING'},'logs':'runtime secret reference resolved; no literal credential captured'})
    return {'resolved':config,'fixtures':results,'limitation':policy['residual_limitation']}
'''
print('BUDGET COLS',[c['name'] for c in assets['ds.budget_replay']['columns']])
keys=['workload_scope','budget_amount','period','threshold_ratio','notification_topic','response_pipeline','INSTANCE','ZONE','authorized_identity','secret_version_reference']
sol='config = {'+','.join(repr(k)+':policy['+repr(k)+']' for k in keys)+",'secretEnv':['BUDGET_CLIENT'],'event_binding':{'topic':policy['notification_topic'],'pipeline':policy['response_pipeline']}}\n"
sol+='''with open('guardrail.yaml','w') as handle:
    yaml.safe_dump(config,handle)
with open('guardrail.yaml') as handle:
    resolved = yaml.safe_load(handle)
result = apply_and_replay(resolved)
'''
# supplied execution call remains scaffold, learner changes config / serialization only
footer='result = apply_and_replay(resolved)\n'
register(n,['budget_replay'],supplied(helper),'resolved = {}\n# Author config, safe-dump/load guardrail.yaml into resolved.\n'+footer,sol,'Author config from the policy workload_scope, budget_amount, period, threshold_ratio, notification_topic, response_pipeline, INSTANCE, ZONE, authorized_identity and secret_version_reference. Add secretEnv=[BUDGET_CLIENT] and event_binding with topic and pipeline from policy. Safe-dump guardrail.yaml and reload as resolved before the supplied apply_and_replay call. The fixed-target response is stop, not delete. Review result: below-threshold yields no action; boundary and breach yield notification plus authorized stop and before/after descriptions. Keep runtime secret references, never values. Preserve the notification-lag limitation in the returned record; no hard spending cap is claimed.', ['result'],['numpy','pyyaml'])

# Durable clients and pipeline fixture scaffolding for idempotency.
n='retraining_run_idempotency';pol=policy(n)
cloud=json.loads(next(f['content'] for f in assets['ws.'+n]['files'] if f['path']=='cloudbuild.skeleton.json'))
helper='import yaml\npolicy = '+repr(pol)+'\n'+'''
import os, json
# Durable shared coordinator fixture. os.mkdir claims a filesystem lock atomically;
# os.replace commits the entire key/slot/job reservation as one persisted record.
class Coordinator:
    def __init__(self):
        self.path='coordinator.json'
        if not os.path.exists(self.path):
            self.write({'claims':{},'slots':{},'jobs':{}})
    def read(self):
        with open(self.path) as f: return json.load(f)
    def write(self,state):
        with open(self.path+'.tmp','w') as f: json.dump(state,f)
        os.replace(self.path+'.tmp',self.path)
    def atomic_admit(self,key,pipeline):
        os.mkdir('coordinator.lock')
        try:
            state=self.read()
            if key in state['claims']:
                row=state['claims'][key]
                return {'status':'duplicate','job_id':row['job_id'],'completed':row['completed']}
            if pipeline in state['slots']:
                return {'status':'busy','job_id':None,'completed':False}
            job='J.'+key
            state['claims'][key]={'pipeline':pipeline,'job_id':job,'completed':False}
            state['slots'][pipeline]=key
            self.write(state)
            return {'status':'accepted','job_id':job,'completed':False}
        finally: os.rmdir('coordinator.lock')
    def confirm_terminal_and_release(self,key,job):
        os.mkdir('coordinator.lock')
        try:
            state=self.read()
            if state['jobs'].get(job)!='terminal': return False
            row=state['claims'][key]
            if row['job_id']!=job: return False
            row['completed']=True
            if state['slots'].get(row['pipeline'])==key: del state['slots'][row['pipeline']]
            self.write(state); return True
        finally: os.rmdir('coordinator.lock')
    def finish_jobs(self):
        state=self.read(); state['jobs']={j:'terminal' for j in state['jobs']}; self.write(state)
class Executor:
    def __init__(self,coordinator): self.coordinator=coordinator
    def launch(self,job):
        os.mkdir('coordinator.lock')
        try:
            state=self.coordinator.read()
            state['jobs'].setdefault(job,'running')
            self.coordinator.write(state);return job
        finally: os.rmdir('coordinator.lock')
    def attach(self,job): return self.launch(job)
    def status(self,job): return self.coordinator.read()['jobs'].get(job,'unknown')
def fresh():
    c=Coordinator();return c,Executor(c)
def reset():
    c,e=fresh();c.write({'claims':{},'slots':{},'jobs':{}})
def durable_state():
    c,e=fresh();return c.read()
def run_fixtures(admit,config):
    event=policy['event'];key=event['run_key'];pipeline=event['pipeline'];out={}
    reset(); c1,e1=fresh();c2,e2=fresh()
    # Two independent coordinator clients, same delivery. Atomic coordinator serializes competing claims.
    a=admit(event,c1,e1);b=admit(event,c2,e2);out['same_key']={'results':[a,b],'state':durable_state()}
    b2=admit({'run_key':key+'2','pipeline':pipeline},c2,e2);out['different_key']={'result':b2,'state':durable_state()}
    reset();c,e=fresh();reservation=c.atomic_admit(key,pipeline);c2,e2=fresh();out['restart_reservation']={'result':admit(event,c2,e2),'state':durable_state()}
    reset();c,e=fresh();r=c.atomic_admit(key,pipeline);e.launch(r['job_id']);c2,e2=fresh();out['restart_launch']={'result':admit(event,c2,e2),'state':durable_state()}
    # Launch accepted by backend, response lost: fresh worker can see only persisted identity.
    c3,e3=fresh();out['unknown_response']={'result':admit(event,c3,e3),'state':durable_state()}
    c.finish_jobs();out['completion_release']=admit(event,c3,e3);out['completed_duplicate']={'result':admit(event,*fresh()),'state':durable_state()}
    fatal=all(not s.get('allowFailure',False) and not s.get('allowExitCodes') for s in config['steps'])
    deps=config['steps'][1]['waitFor']==['entry'] and config['steps'][2]['waitFor']==['function_test']
    out['pipeline']={'resolved':config,'accepted':{'entry':'success','function_test':'success','execute':'success'} if fatal and deps else {},'rejected':{'entry':'failed','function_test':'blocked','execute':'blocked'},'resolved_inputs':event}
    return out
'''
sol='''def admit(event,coordinator,executor):
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
config = '''+repr(cloud)+'''
with open('build.yaml','w') as handle:
    yaml.safe_dump(config,handle)
with open('build.yaml') as handle:
    resolved = yaml.safe_load(handle)
result = run_fixtures(admit,resolved)
assert result['same_key']['results'][0]['job_id'] == result['same_key']['results'][1]['job_id']
assert result['different_key']['result']['status'] == 'defer'
assert result['restart_reservation']['result']['job_id'] == result['restart_launch']['result']['job_id']
assert result['completed_duplicate']['result']['status'] == 'completed'
'''
register(n,[],supplied(helper),'# Define admit(event,coordinator,executor), wire fatal pipeline config, roundtrip YAML, call run_fixtures, assert invariants.\n',sol,'Implement admit(event,coordinator,executor). Call atomic_admit on event run_key/pipeline. Busy returns status defer with job_id None and launches nothing. A completed claim returns status completed and its persisted job_id. Accepted calls executor.launch with persisted job_id; duplicate calls attach to reconcile that same token (including after a lost response). If status(job_id) is terminal, confirm_terminal_and_release; always retain key identity. Otherwise return original claim status and job_id. Author the supplied three-stage build configuration entry -> function_test -> execute, using python:3.11 and args python3/entry_fixture.py, python3/learner.py, python3/execution_fixture.py respectively; explicit waitFor, no failure exemptions. Safe-dump/load build.yaml as resolved, set result=run_fixtures(admit,resolved), and assert same-key identities, busy deferral, restart identity stability and completed non-relaunch. The shared filesystem coordinator supplies the durable atomic operation and the idempotent executor; do not replace them with local state.', ['result'],['pyyaml'])

# Interaction content and deterministic derivation follow below.
exec((B/'stage04_finish_new.py').read_text())
