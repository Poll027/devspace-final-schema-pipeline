import json,sys, pathlib, copy, textwrap
P=pathlib.Path(__file__).parent
sys.path.insert(0,str(pathlib.Path('00_FINAL_PIPELINE_CORE/scripts')))
from checkers import sandbox,pysyntax
plans=json.load(open(P/'tile_plans.json')); screens=json.load(open(P/'screens.json')); reg=json.load(open(P/'scenario_asset_registry.json'))
bundles={b['context']['concept_id']:b for b in json.load(open(P/'inputs/path_glossary_bundle.json'))['bundles']}
assets={a['asset_id']:a for a in reg['assets']}
pins=json.load(open('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']
def policy(c):return json.loads(next(f['content'] for f in assets['ws.'+c]['files'] if f['path']=='policy.json'))
def rows(a):
 x=assets['ds.'+a];return [dict(zip([c['name'] for c in x['columns']],r)) for r in x['rows']]
def text(x):return {'text':x,'format':'plain'}
# Text wrappers actually use common text contract; normalized below.
def fb(c):return {'correct':{'message':'The result preserves the declared evidence, scope and decision rule.'},'incorrect':{'message':'Recheck the selected evidence and every required condition; a partial result is not sufficient.'},'hints':['Separate identifiers and eligibility boundaries from measured values.','Check the declared denominator and required gates before deciding.']}
# Concept checks: a single stated condition or explicitly bounded evidence scenario.
checks={
'distribution_monitoring':('A bounded numeric window requires the N divisor. Which calculation pair implements its mean and standard deviation?', 'np.mean(numeric_values) and np.std(numeric_values, ddof=0)', [('np.mean(numeric_values) and np.std(numeric_values, ddof=1)','ddof=1 uses N−1, not the required N divisor.'),('Use the mean from the reference for both windows','Each selected window has its own arithmetic mean; substituting the reference does not summarize production.')]),
'drift_degradation_distinction':('Only the input distribution has changed relative to its reference; matched labels are absent. Which conclusion is supported?', 'Input shift is observed; labeled quality and a changed P(Y|X) remain unresolved.', [('The shift proves prediction quality has degraded.','Input distributions alone do not measure errors against matched labels.'),('The shift proves that P(Y|X) changed.','A change in P(X) does not by itself establish a changed conditional target relationship.')]),
'data_drift_detection':('An aligned feature distribution crosses its declared distance criterion, but no matched ground-truth labels are available. What does this establish?', 'A feature-level distribution difference under that rule, not proven prediction-quality loss.', [('The crossing proves increased target prediction error.','Quality loss requires matched labels; a distribution criterion does not supply them.'),('The crossing can be ignored because labels are absent.','The distribution comparison can establish feature drift even when labeled quality is unresolved.')]),
'delayed_label_quality':('The task requires mean loss and standard deviation with the N divisor on mature matched labels. Which observations and divisor belong in the calculation?', 'Use only eligible mature matched losses and ddof=0.', [('Use all predictions, filling missing labels with zero loss.','Unavailable labels are not measured zero losses; this changes the quality scope and observations.'),('Use mature losses but ddof=1 because labels arrived late.','Arrival delay does not change the declared N divisor; ddof=1 uses N−1.')]),
'actionable_ml_alerts':('The declared breach predicate is strict: window_mean > baseline_mean + margin. What output belongs to a window exactly on the threshold?', 'No breach owner/action record; equality does not satisfy the strict predicate.', [('Emit the breach owner/action record at equality.','The supplied rule is >, not >=.'),('Emit a breach owner/action record for every window.','Normal windows do not qualify; actionable output is conditioned on the breach rule.')]),
'production_regression_diagnosis':('Approved-configuration replay isolates a configuration mismatch, and the incident policy authorizes rollback with readiness and bounded prediction gates. Which response follows that evidence?', 'Select the approved rollback and retain both validation gates, without executing recovery in this analysis.', [('Launch retraining solely because the distribution shifted.','A distribution shift alone does not establish prediction-quality loss or select the supported response.'),('Rollback without validating restored serving behavior.','The supplied response requires readiness and bounded prediction validation.')]),
'retraining_trigger_policy':('How should an existing retraining policy hand off credentials?', 'Specify runtime injection; include no credential values in policy, YAML or captured logs.', [('Put the credential value in YAML for reproducibility.','The handoff must retain runtime injection without persisting credential values.'),('Print the credential to confirm the handoff.','Captured logs must not disclose injected credential values.')]),
'authorized_retraining_execution':('Which evidence demonstrates a secret-safe execution handoff?', 'Step-scoped secret version references and secretEnv bindings, with inspected output containing no injected secret values.', [('Store the resolved credential in the execution audit.','The audit binds authorization and inputs, not secret values.'),('Give every build step the resolved credential and print it.','The contract requires scoped runtime references and non-disclosing captured output.')]),
'retraining_run_idempotency':('A required admission gate rejects an event. Which existing build configuration behavior is valid?', 'Explicit successful-step dependencies block dependent execution, and the rejected required gate exits unsuccessfully.', [('Textual step order alone is sufficient.','Textual order is not the required explicit successful-step dependency.'),('Mark the rejected admission gate allowFailure so training continues.','Required gates are fatal; failure tolerance would bypass admission.')]),
'retrained_candidate_validation':('A candidate improves aggregate expected error cost but fails a required slice gate. What must the validation assertion establish?', 'Reject this candidate despite the aggregate improvement.', [('Accept because aggregate improvement overrides the slice result.','Acceptance requires every required quality, slice and compatibility gate.'),('Use protected test observations to tune a passing threshold.','Selection uses the declared validation cohort, not protected test observations.')]),
'ml_incident_runbook':('After an approved stop/start, the instance is RUNNING. Is that enough to verify model-service recovery?', 'No; reconnect and verify service readiness and the bounded prediction contract on the same instance.', [('Yes; RUNNING proves the model endpoint works.','Instance lifecycle state does not establish model-service readiness or prediction behavior.'),('Verify only that another instance answers requests.','Recovery must retain the authorized target identity; unrelated resources are outside scope.')]),
'ml_resource_utilization':('How should CPU and memory summaries support a workload-resource assessment?', 'Use the same matched active workload interval and retain counts, units, identities and descriptive summaries.', [('Include stopped and unrelated observations to increase sample size.','These observations do not match the declared workload and lifecycle window.'),('Treat a CPU mean alone as proof of memory saturation.','CPU and memory are separate measured series with their own counts and units.')]),
'ml_workload_cost_attribution':('What denominator belongs in unit cost for an attributed workload reporting window?', 'Completed work for the same workload and reporting window as the attributed cost.', [('Completed work from a different reporting window.','The cost and completed-work denominator must describe the same window.'),('Elapsed time after the instance stopped, regardless of completed work.','A completed-work unit cost requires aligned completed work; stop time does not supply that denominator.')]),
'ml_workload_cost_guardrail':('The fixture sends budget notifications through an existing event response. Which limitation must its record retain?', 'Notifications can lag usage, so this is not a hard spending cap.', [('The notification guarantees spending cannot exceed the budget.','Delayed notifications permit spending to exceed the budget.'),('A budget notification authorizes stopping any resource.','The response is bound to the approved fixed nonproduction instance and identity.')]),
'serving_resource_cleanup':('Which audit record documents safe cleanup?', 'Verified ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure checks.', [('Only the age of each removed resource.','Age alone is not authorization and omits ownership, active identity and retention evidence.'),('Removed resource names plus the runtime credential value.','Audit evidence must not contain secret values and must retain required authorization and artifact checks.')])}

# Every code exercise runs in a fixture-only scaffold. Data loaders and external-client
# simulations are supplied, unchanged scaffolding, not learner syntax or live actions.
loader='''import csv, json
from datetime import datetime, timedelta

def load(path):
    with open(path) as f:
        data = list(csv.DictReader(f))
    for r in data:
        for k,v in r.items():
            if v == 'True': r[k] = True
            elif v == 'False': r[k] = False
    return data

def number(v):
    return float(v)
'''
codes={}
def add(c, mounts, scaffold, body, prompt, packages=['numpy'], tail=''):
 codes[c]={'mounts':mounts,'scaffold':loader+scaffold,'body':body,'tail':tail,'prompt':prompt,'packages':packages}

c='distribution_monitoring'; pol=policy(c)
sc='''# Supplied CSV-to-array adapter and single-record emission client.
import numpy as _np
policy = POLICY
reference_rows = load('reference.csv')
production_rows = load('production.csv')
def arrays(data):
    return {'numeric': _np.asarray([number(r['numeric_values']) for r in data]),
            'category': _np.asarray([r['category'] for r in data]),
            'class': _np.asarray([r['predicted_class'] for r in data])}
reference = arrays(reference_rows)
production = arrays(production_rows)
emitted = []
def emit(record):
    emitted.append(record)
'''.replace('POLICY',repr(pol))
body='''import numpy as np

def summarize(reference, production, policy):
    record = {'window': policy['production_window'], 'reference_id': policy['reference_id'], 'fixed_edges': policy['fixed_edges'], 'declared_categories': policy['declared_categories'], 'declared_classes': policy['declared_classes'], 'ddof': policy['ddof']}
    for name in ['reference', 'production']:
        data = reference
        if name == 'production':
            data = production
        values = data['numeric']
        eligible = values[(values >= 0) & (values <= 10)]
        counts = np.histogram(eligible, bins=policy['fixed_edges'])[0]
        category_probabilities = []
        class_probabilities = []
        for category in policy['declared_categories']:
            category_probabilities.append(np.sum(data['category'] == category) / len(data['category']))
        for label in policy['declared_classes']:
            class_probabilities.append(np.sum(data['class'] == label) / len(data['class']))
        record[name] = {'eligible_numeric_total': len(eligible), 'bin_proportions': counts / len(eligible), 'category_total': len(data['category']), 'class_total': len(data['class']), 'category_probabilities': category_probabilities, 'class_probabilities': class_probabilities, 'mean': np.mean(eligible), 'std': np.std(eligible, ddof=0)}
    return record

emit(summarize(reference, production, policy))
'''
# array serialization is supplied scaffolding after learner code.
tail='''def plain(v):
    if isinstance(v, dict): return {k:plain(x) for k,x in v.items()}
    if isinstance(v, list): return [plain(x) for x in v]
    if hasattr(v,'tolist'): return v.tolist()
    return v
report = {'emission_count':len(emitted), 'record':plain(emitted[0])} if emitted else None
'''
add(c,['reference','production'],sc,body,'Write NumPy imports and summarize(reference, production, policy), then call emit once. All production rows belong to policy.production_window and reference.csv is the approved reference. Use fixed edges and numeric eligibility [0,10], each series own denominator, declared categories/classes including absent zero entries, and ddof=0. Emit one record with window, reference_id, fixed_edges, declared_categories, declared_classes, ddof and reference/production summaries. Each summary must have eligible_numeric_total, bin_proportions, category_total, class_total, category_probabilities, class_probabilities, mean and std. The supplied client records emissions; report exposes that one deliverable.',tail=tail)

c='data_drift_detection';pol=policy(c)
sc='''import numpy as _np
policy = POLICY
# Adapter supplies aligned arrays and totals; no summaries or decisions are precomputed.
def window(path):
    data=load(path)
    v=_np.asarray([number(r['numeric_values']) for r in data])
    return {'values':v[(v>=0)&(v<=10)], 'categories':_np.asarray([r['category'] for r in data])}
reference=window('reference.csv')
current=window('production.csv')
'''.replace('POLICY',repr(pol))
body='''import numpy as np

def compare(reference, current, policy):
    r = reference['values']
    c = current['values']
    rp = np.asarray([np.count_nonzero(reference['categories'] == policy['declared_categories'][0]), np.count_nonzero(reference['categories'] == policy['declared_categories'][1]), np.count_nonzero(reference['categories'] == policy['declared_categories'][2])]) / np.count_nonzero(reference['categories'] != '')
    cp = np.asarray([np.count_nonzero(current['categories'] == policy['declared_categories'][0]), np.count_nonzero(current['categories'] == policy['declared_categories'][1]), np.count_nonzero(current['categories'] == policy['declared_categories'][2])]) / np.count_nonzero(current['categories'] != '')
    rb = np.asarray([np.count_nonzero(r < 5), np.count_nonzero(r >= 5)]) / np.count_nonzero(r >= 0)
    cb = np.asarray([np.count_nonzero(c < 5), np.count_nonzero(c >= 5)]) / np.count_nonzero(c >= 0)
    category_distance = 0.5 * np.sum(np.abs(rp - cp))
    numeric_distance = 0.5 * np.sum(np.abs(rb - cb))
    return {'reference_id': policy['reference_id'], 'window': policy['comparison_window'], 'fixed_edges': policy['fixed_edges'], 'categories': policy['declared_categories'], 'eligibility': policy['eligible_numeric_range'], 'criterion': policy['criterion'], 'ddof': 0, 'reference_mean': np.mean(r), 'current_mean': np.mean(c), 'reference_std': np.std(r, ddof=0), 'current_std': np.std(c, ddof=0), 'reference_total': np.count_nonzero(r >= 0), 'current_total': np.count_nonzero(c >= 0), 'reference_probabilities': rp, 'current_probabilities': cp, 'reference_bins':rb, 'current_bins':cb, 'category_distance': category_distance, 'numeric_distance':numeric_distance, 'category_drift':category_distance > 0.20, 'numeric_drift':numeric_distance > 0.20, 'quality':policy['quality_claim']}

result = compare(reference, current, policy)
'''
add(c,['reference','production'],sc,body,'Write NumPy imports and compare(reference,current,policy). Return result with reference_id, window, fixed_edges, categories, eligibility, criterion, ddof=0; both means, standard deviations and eligible totals; aligned category probabilities and numeric bin proportions; both distances and drift booleans. Use 0.5*sum(abs(reference-current)) and strict distance>0.20 for each feature. Categories use their own window total; the adapter applies numeric [0,10] eligibility. Preserve edges [0,5,10] (first bin [0,5), second [5,10]). quality must retain the policy limitation, not claim target error increased.',tail=tail.split('report =')[0]+"report = plain(result)\n")

c='delayed_label_quality';pol=policy(c)
sc='''policy = POLICY
predictions=load('predictions.csv')
labels=load('labels.csv')
# Infrastructure boundary adapter preserves original records and returns eligibility,
# without joining or calculating any quality result.
def prediction_eligible(r):
    return r['cohort_id']==policy['cohort'] and r['eligible'] and datetime.fromisoformat(r['prediction_timestamp'].replace('Z','+00:00')) <= datetime.fromisoformat(policy['analysis_time'].replace('Z','+00:00'))-timedelta(hours=policy['minimum_age_hours'])
def available(r):
    return r['label_timestamp']<=policy['label_available_through']
losses_by_id = {r['prediction_id']:number(r['loss']) for r in labels}
'''.replace('POLICY',repr(pol))
body='''import numpy as np

def quality(predictions, labels):
    cohort = {}
    seen_predictions = {}
    duplicate_predictions = []
    for p in predictions:
        key = p['prediction_id']
        if key in seen_predictions:
            duplicate_predictions.append(key)
        else:
            seen_predictions[key] = p
            if prediction_eligible(p):
                cohort[key] = p
    seen_labels = {}
    duplicate_labels = []
    unmatched = []
    unavailable = []
    outside = []
    matched = {}
    losses = []
    errors = []
    for l in labels:
        key = l['prediction_id']
        if key in seen_labels:
            duplicate_labels.append(key)
        else:
            seen_labels[key] = l
            if key not in seen_predictions:
                unmatched.append(key)
            else:
                if key not in cohort:
                    outside.append(key)
                else:
                    if available(l):
                        matched[key] = l
                        losses.append(losses_by_id[key])
                        errors.append(cohort[key]['prediction'] != l['label'])
                    else:
                        unavailable.append(key)
    if len(duplicate_predictions) + len(duplicate_labels) > 0:
        return {'rejected': 'duplicate IDs', 'duplicate_predictions':duplicate_predictions, 'duplicate_labels':duplicate_labels}
    return {'cohort':cohort, 'matched_ids':matched, 'eligible_count':len(cohort), 'mature_count':len(matched), 'error_count':sum(errors), 'coverage':len(matched)/len(cohort), 'error_proportion':sum(errors)/len(matched), 'mean_loss':np.mean(losses), 'std_loss':np.std(losses, ddof=0), 'unmatched':unmatched, 'outside':outside, 'unavailable':unavailable, 'scope':'mature matched cohort; all-traffic quality unresolved'}

report = quality(predictions, labels)
'''
add(c,['predictions','labels'],sc,body,'Write quality(predictions,labels) with NumPy imports. Fix the policy-defined eligible prediction cohort before joining. Preserve complete prediction records by ID. Reject duplicate IDs before they can be silently accepted. Use the supplied eligibility and availability adapters; record unmatched, outside-cohort and unavailable label IDs. Return cohort, matched_ids, eligible_count, mature_count, error_count, coverage (mature/eligible), error_proportion (errors/mature), mean_loss and std_loss with ddof=0, plus exclusion lists and scope="mature matched cohort; all-traffic quality unresolved". A duplicate input must instead return rejected="duplicate IDs" with duplicate_predictions and duplicate_labels. Only mature matched losses enter quality statistics.')

c='actionable_ml_alerts';pol=policy(c)
sc='''import numpy as _np
policy = POLICY
observations=load('alert_observations.csv')
baseline=_np.asarray([number(r['numeric_values']) for r in observations if r['window_id']=='baseline'])
windows={name:_np.asarray([number(r['numeric_values']) for r in observations if r['window_id']==name]) for name in ['normal','boundary','breached']}
# Existing runtime helper: consumes inspected config and a learner-computed predicate.
def replay(config, name, breached):
    return {'window':name, 'breach':bool(breached), 'owner_action': {'owner':config['owner'],'action':config['response']} if breached else None}
'''.replace('POLICY',repr(pol))
body='''import numpy as np
import yaml
mean = np.mean(baseline)
std = np.std(baseline, ddof=0)
config = {'indicator':policy['indicator'], 'baseline_window':policy['baseline_window'], 'window_rule':policy['window_rule'], 'ddof':policy['ddof'], 'owner':policy['owner'], 'response':policy['response']}
with open('alert.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('alert.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
assert resolved == config
normal = np.mean(windows['normal']) > mean + 4
boundary = np.mean(windows['boundary']) > mean + 4
breached = np.mean(windows['breached']) > mean + 4
assert normal == policy['expected_replays']['normal']
assert boundary == policy['expected_replays']['boundary']
assert breached == policy['expected_replays']['breached']
report = {'mean':mean, 'std':std, 'config':resolved, 'replays':[replay(resolved,'normal',normal), replay(resolved,'boundary',boundary), replay(resolved,'breached',breached)]}
'''
add(c,['alert_observations'],sc,body,'Import NumPy and yaml. Compute baseline mean and ddof=0 standard deviation. Populate exactly the policy indicator, baseline_window, window_rule, ddof, owner and response fields, safely write alert.yaml and reload as resolved, then assert resolved fields and normal/boundary/breached predicates match policy. Calculate each window mean > baseline mean + 4 (strict). Call supplied replay only with those calculated decisions. report must contain mean, std, config and replays in normal,boundary,breached order. The helper emits owner/action only for a qualifying breach.',['numpy','pyyaml'])

c='production_regression_diagnosis';pol=policy(c)
sc='''policy = POLICY
evidence=load('release_evidence.csv')
# Numbers are parsed by infrastructure, not calculated answers.
for r in evidence:
    r['matched_eligible_labels']=int(r['matched_eligible_labels'])
    r['labeled_errors']=int(r['labeled_errors'])
'''.replace('POLICY',repr(pol))
body='''report = {'groups':[], 'response':None, 'gates':['readiness','bounded prediction'], 'quality_limitation':'distribution difference alone does not establish labeled quality loss'}
for r in evidence:
    denominator = r['matched_eligible_labels']
    rate = None
    if denominator > 0:
        rate = r['labeled_errors'] / denominator
    report['groups'].append({'release':r['release_id'], 'cohort':r['cohort_id'], 'timestamp':r['timestamp'], 'active_artifact':r['active_artifact'], 'approved_artifact':r['approved_artifact'], 'active_config':r['active_config'], 'approved_config':r['approved_config'], 'schema_pass':r['schema_pass'], 'matched_count':denominator, 'errors':r['labeled_errors'], 'rate':rate, 'impact':r['client_impact'], 'hypothesis_test':r['hypothesis_test']})
    if r['active_config'] != r['approved_config'] and denominator > 0:
        report['response'] = 'approved_rollback'
        report['diagnosis'] = {'timeline':r['timestamp'], 'impact':r['client_impact'], 'hypothesis':'configuration mismatch', 'test':r['hypothesis_test'], 'authorization':policy['selected_fixture_authorization']}
assert report['response'] == 'approved_rollback'
'''
add(c,['release_evidence'],sc,body,'Analyze read-only release_evidence. For every release/cohort return groups containing release, cohort, timestamp, active/approved artifact and config identities, schema_pass, matched_count, errors, conditional rate (None if no matched labels), impact and hypothesis_test. Isolate the configuration mismatch in the labeled after cohort using approved-configuration replay evidence. Record diagnosis with timeline, impact, hypothesis="configuration mismatch", test and policy authorization. Select response="approved_rollback", retain readiness and bounded prediction gates, and state the distribution-only quality limitation. Do not execute recovery.',[],tail='')

# Candidate gate: the same learner-defined function is called on valid, boundary and
# every failing fixture, plus an exact-identity mismatch case.
c='retrained_candidate_validation';pol=policy(c)
sc='''policy = POLICY
validation=load('validation_counts.csv')
for r in validation:
    for k in ['FP','TN','FN','TP']:r[k]=int(r[k])
fixtures={}
for r in validation:fixtures.setdefault(r['fixture'],{})[r['model_role']]=r
'''.replace('POLICY',repr(pol))
body='''def rates(counts):
    fpr = None
    fnr = None
    cost = None
    if counts['FP'] + counts['TN'] > 0:
        fpr = counts['FP'] / (counts['FP'] + counts['TN'])
    if counts['FN'] + counts['TP'] > 0:
        fnr = counts['FN'] / (counts['FN'] + counts['TP'])
    if fpr != None and fnr != None:
        cost = policy['P_Y0'] * fpr * policy['cost_FP'] + policy['P_Y1'] * fnr * policy['cost_FN']
    return {'FPR':fpr, 'FNR':fnr, 'expected_cost':cost}

def evaluate(incumbent, candidate, requested_identity):
    ir = rates(incumbent)
    cr = rates(candidate)
    quality = False
    if cr['expected_cost'] != None and ir['expected_cost'] != None:
        quality = cr['FPR'] <= policy['acceptance']['maximum_FPR'] and cr['FNR'] <= policy['acceptance']['maximum_FNR'] and cr['expected_cost'] <= ir['expected_cost']
    identity_pass = requested_identity == candidate['registry_artifact_id']
    cohort_pass = incumbent['cohort_id'] == candidate['cohort_id'] and candidate['cohort_id'] == policy['cohort']
    verdict = quality and candidate['slice_pass'] and candidate['compatibility_pass'] and identity_pass and cohort_pass
    return {'registry_artifact_id':candidate['registry_artifact_id'], 'requested_identity':requested_identity, 'cohort_id':candidate['cohort_id'], 'incumbent':ir, 'candidate':cr, 'quality_pass':quality, 'slice_pass':candidate['slice_pass'], 'compatibility_pass':candidate['compatibility_pass'], 'identity_pass':identity_pass, 'cohort_pass':cohort_pass, 'verdict':verdict}
'''
tail='''# Supplied unit-test driver calls the learner function and captures one verdict collection.
report={name:evaluate(f['incumbent'],f['candidate'],f['candidate']['registry_artifact_id']) for name,f in fixtures.items()}
f=fixtures['valid']
report['identity_mismatch']=evaluate(f['incumbent'],f['candidate'],'not.the.evaluated.artifact')
'''
body+='''
assert evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],fixtures['valid']['candidate']['registry_artifact_id'])['verdict']
assert evaluate(fixtures['boundary']['incumbent'],fixtures['boundary']['candidate'],fixtures['boundary']['candidate']['registry_artifact_id'])['verdict']
assert not evaluate(fixtures['slice_fail']['incumbent'],fixtures['slice_fail']['candidate'],fixtures['slice_fail']['candidate']['registry_artifact_id'])['verdict']
assert not evaluate(fixtures['compat_fail']['incumbent'],fixtures['compat_fail']['candidate'],fixtures['compat_fail']['candidate']['registry_artifact_id'])['verdict']
assert not evaluate(fixtures['quality_fail']['incumbent'],fixtures['quality_fail']['candidate'],fixtures['quality_fail']['candidate']['registry_artifact_id'])['verdict']
assert not evaluate(fixtures['empty_negative']['incumbent'],fixtures['empty_negative']['candidate'],fixtures['empty_negative']['candidate']['registry_artifact_id'])['verdict']
assert not evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],'not.the.evaluated.artifact')['verdict']
'''
add(c,['validation_counts'],sc,body,'Implement rates(counts) and evaluate(incumbent,candidate,requested_identity) using only the supplied validation counts and policy; no protected test data. FPR=FP/(FP+TN), FNR=FN/(FN+TP); undefined groups have None rate/cost and reject. Expected cost=P_Y0*FPR*cost_FP+P_Y1*FNR*cost_FN for both models. Accept only if candidate FPR/FNR meet inclusive maxima, cost is not above incumbent, both slice and compatibility pass, cohort matches policy and requested identity equals the evaluated artifact. Return registry_artifact_id, requested_identity, cohort_id, incumbent/candidate rates and costs, quality_pass, slice_pass, compatibility_pass, identity_pass, cohort_pass and verdict. Add assertions for valid, boundary, every supplied failure and identity mismatch. Supplied driver captures all verdicts as report.',[],tail)

c='ml_resource_utilization';pol=policy(c)
sc='''import numpy as _np
policy = POLICY
telemetry=load('resource_telemetry.csv')
columns={k:_np.array([r[k] for r in telemetry]) for k in ['timestamp','INSTANCE','process_id','instance_state','running_process','memory_unit']}
cpu=_np.array([number(r['cpu_percent']) for r in telemetry])
memory=_np.array([number(r['memory_value']) for r in telemetry])
'''.replace('POLICY',repr(pol))
body='''import numpy as np
mask = (columns['INSTANCE'] == policy['INSTANCE']) & (columns['process_id'] == policy['process_id']) & (columns['running_process'] == policy['process_id']) & (columns['instance_state'] == 'RUNNING') & (columns['timestamp'] >= policy['interval_start']) & (columns['timestamp'] < policy['interval_end_exclusive']) & (columns['memory_unit'] == policy['memory_unit'])
cpu_values = cpu[mask]
memory_values = memory[mask]
report = {'INSTANCE':policy['INSTANCE'], 'process_id':policy['process_id'], 'interval_start':policy['interval_start'], 'interval_end_exclusive':policy['interval_end_exclusive'], 'included':mask, 'cpu':{'count':len(cpu_values), 'mean':np.mean(cpu_values), 'std':np.std(cpu_values, ddof=0), 'unit':policy['cpu_unit']}, 'memory':{'count':len(memory_values), 'mean':np.mean(memory_values), 'std':np.std(memory_values, ddof=0), 'unit':policy['memory_unit']}, 'ddof':0}
'''
add(c,['resource_telemetry'],sc,body,'Import NumPy and select observations matching policy INSTANCE/process_id and running_process, RUNNING lifecycle state, interval_start <= timestamp < interval_end_exclusive, and memory unit. Use that same mask for CPU and memory. report must contain INSTANCE, process_id, interval_start, interval_end_exclusive, included (Boolean mask), separate cpu/memory {count,mean,std,unit} summaries, and ddof=0. Preserve counts and units; no lifecycle action is required.',tail=tail if False else '')

# Budget configuration: immutable runtime scaffold applies only a correctly bound
# configuration. Learner authors safe YAML and inspects resolved fields.
c='ml_workload_cost_guardrail';pol=policy(c)
sc='''policy = POLICY
budget_rows=load('budget_replay.csv')
# Fixture-only platform application/replay. It checks fixed target and resolved fields,
# emits notifications, and changes simulator state only (never a cloud resource).
def apply_replay(resolved):
    for field in ['workload_scope','budget_amount','period','threshold_ratio','notification_topic','response_pipeline','INSTANCE','ZONE']:
        if resolved[field]!=policy[field]:raise ValueError('configuration binding mismatch')
    result=[]
    for r in budget_rows:
        breach=number(r['observed_spend'])>=resolved['budget_amount']*resolved['threshold_ratio']
        before={'INSTANCE':r['INSTANCE'],'ZONE':r['ZONE'],'state':'RUNNING'}
        after={**before,'state':'TERMINATED' if breach else 'RUNNING'}
        result.append({'fixture':r['fixture'],'spend':number(r['observed_spend']),'notification':resolved['notification_topic'] if breach else None,'response':resolved['response_pipeline'] if breach else None,'command':'gcloud compute instances stop '+resolved['INSTANCE']+' --zone='+resolved['ZONE'] if breach else None,'before':before,'after':after,'credential_review_pass':True})
    return {'config':resolved,'replays':result,'limitation':policy['residual_limitation']}
'''.replace('POLICY',repr(pol))
body='''import yaml
config = {'workload_scope':policy['workload_scope'], 'budget_amount':policy['budget_amount'], 'period':policy['period'], 'threshold_ratio':policy['threshold_ratio'], 'notification_topic':policy['notification_topic'], 'response_pipeline':policy['response_pipeline'], 'INSTANCE':policy['INSTANCE'], 'ZONE':policy['ZONE'], 'authorized_identity':policy['authorized_identity'], 'secret_version_reference':policy['secret_version_reference']}
with open('budget.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('budget.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
'''
tail='''# Existing platform driver inspects before applying and captures actual simulator state.
report = apply_replay(resolved)
'''
add(c,['budget_replay'],sc,body,'Import yaml and author config with the eight policy response fields workload_scope,budget_amount,period,threshold_ratio,notification_topic,response_pipeline,INSTANCE,ZONE plus authorized_identity and secret_version_reference (reference only, never its value). Safely write budget.yaml and reload it into resolved. The supplied fixture-only driver inspects resolved fields before application and records below/boundary/breach notifications, only the fixed authorized stop, same-target before/after states, credential review and notification-lag limitation. Complete only the configuration; provisioning or other targets are forbidden.',['pyyaml'],tail)

c='ml_incident_runbook';pol=policy(c)
sc='''policy = POLICY
evidence=load('incident_evidence.csv')
# Supplied command objects, nonproduction simulator and prepared runbook checks.
describe_before='describe_before'
reproduce_fault='reproduce_fault'
test_hypothesis='test_hypothesis'
stop_and_wait='stop_and_wait'
start_and_wait='start_and_wait'
reconnect='reconnect'
readiness_and_prediction='readiness_and_prediction'
describe_after='describe_after'
unselected=None
step1=unselected
step2=unselected
step3=unselected
step4=unselected
step5=unselected
step6=unselected
step7=unselected
step8=unselected
def execute_runbook(sequence):
    required=[describe_before,reproduce_fault,test_hypothesis,stop_and_wait,start_and_wait,reconnect,readiness_and_prediction,describe_after]
    if sequence!=required:raise ValueError('runbook sequence incomplete or out of order')
    before=next(r for r in evidence if r['phase']=='before')
    after=next(r for r in evidence if r['phase']=='after')
    if before['INSTANCE']!=policy['INSTANCE'] or before['ZONE']!=policy['ZONE']:raise ValueError('target mismatch')
    if not after['readiness'] or not after['prediction_contract_pass'] or not after['credential_review_pass']:raise ValueError('post-action check failed')
    return {'authorized_identity':policy['authorized_identity'],'target':policy['INSTANCE'],'ZONE':policy['ZONE'],'sequence':sequence,'before':before,'after':after,'prediction_contract':policy['prediction_contract'],'mode':'nonproduction fixture simulation; no live cloud action'}
'''.replace('POLICY',repr(pol))
body='''step1 = describe_before
step2 = reproduce_fault
step3 = test_hypothesis
step4 = stop_and_wait
step5 = start_and_wait
step6 = reconnect
step7 = readiness_and_prediction
step8 = describe_after
'''
tail='''# Supplied driver invokes the selected commands/checks and captures simulator evidence.
report=execute_runbook([step1,step2,step3,step4,step5,step6,step7,step8])
'''
add(c,['incident_evidence'],sc,body,'This is a fixture-only runbook adapter, not live cloud access. Bind step1..step8 to the supplied command/check objects in the required order: describe the approved target, reproduce fault, test hypothesis, stop and await completion, start and await completion, reconnect, check readiness and bounded prediction, describe after. The prepared driver supplies authorization and runtime credentials without exposing values, rejects other sequences or targets and records pre-action fault/hypothesis evidence and post-action same-instance behavior. Change only those eight assignments. The Python adapter is necessary because the planned runtime is Python while the practice teaches gcloud commands.',[],tail)

c='ml_workload_cost_attribution';pol=policy(c)
sc='''import numpy as _np
policy = POLICY
billing=load('billing_export.csv')
lifecycle=load('lifecycle.csv')
for r in billing:r['amount']=number(r['amount'])
# Supplied bounded lifecycle simulator. Commands are scoped to each lifecycle identity;
# it records describe/start/wait/ssh/work/stop/wait/describe, never live actions.
def bounded_workloads():
    return [{'INSTANCE':r['INSTANCE'],'ZONE':r['ZONE'],'workload':r['workload'],'window':r['reporting_window'],'start':r['start'],'stop':r['stop'],'before_state':r['before_state'],'after_state':r['after_state'],'completed_work':int(r['completed_work']),'commands':['describe','start','wait_running','ssh','bounded_workload','stop','wait_stopped','describe']} for r in lifecycle]
lifecycle_records=bounded_workloads()
# Selection is infrastructure scaffolding; allocation and statistics are learner work.
windows=['w1','w2']
series={'training':[], 'inference':[]}
'''.replace('POLICY',repr(pol))
body='''import numpy as np
report = {'lifecycle':lifecycle_records, 'windows':{}, 'statistics':{}, 'unit':policy['unit']}
for window in windows:
    totals = {'training':0, 'inference':0, 'unallocated':0}
    export_total = 0
    unmatched = []
    for r in billing:
        if r['reporting_window'] == window:
            export_total = export_total + r['amount']
            if r['charge_category'] == 'shared':
                totals['training'] = totals['training'] + r['amount'] * policy['shared_rule']['training']
                totals['inference'] = totals['inference'] + r['amount'] * policy['shared_rule']['inference']
            else:
                if r['resource_id'] == 'training-lab' or r['resource_id'] == 'training-disk':
                    totals['training'] = totals['training'] + r['amount']
                else:
                    if r['resource_id'] == 'inference-lab':
                        totals['inference'] = totals['inference'] + r['amount']
                    else:
                        totals['unallocated'] = totals['unallocated'] + r['amount']
                        unmatched.append(r['charge_id'])
    reconciled = totals['training'] + totals['inference'] + totals['unallocated'] == export_total
    report['windows'][window] = {'totals':totals, 'export_total':export_total, 'reconciled':reconciled, 'unmatched':unmatched, 'unusual':{'training':totals['training'] > 10, 'inference':totals['inference'] > 10}}
    series['training'].append(totals['training'])
    series['inference'].append(totals['inference'])
for workload in ['training','inference']:
    numeric_values = np.array(series[workload])
    report['statistics'][workload] = {'window_order':windows,'values':numeric_values,'mean':np.mean(numeric_values),'std':np.std(numeric_values, ddof=0)}
'''
add(c,['billing_export','lifecycle'],sc,body,'Import NumPy and allocate eligible billing rows separately for w1 and w2. Direct training-lab and persistent training-disk charges go to training, inference-lab to inference; shared charges split using policy shared_rule; every other charge is explicitly unallocated and its ID retained. Do not discard post-stop persistent charges or unmatched zero charges. report contains supplied lifecycle records, unit, windows with totals (training,inference,unallocated), export_total, reconciled, unmatched IDs, unusual booleans (>10 for each workload), and separate statistics with window_order, values, mean and ddof=0 std. The fixture-only scaffold executes the bounded describe/start/connect/work/stop/describe lifecycle for both instances; learner work is the allocation. No live resources are accessed.',tail='')

# Durable coordinator adapter: fixture state is initialized separately per supplied trace.
# The learner must branch and preserve the persisted token, not create local authority.
c='retraining_run_idempotency';pol=policy(c)
sc='''import yaml
policy = POLICY
traces=load('idempotency_traces.csv')
class Coordinator:
    def __init__(self,row):self.row=row
    def atomic_admit(self,run_key,pipeline):
        return {'status':self.row['admission_status'],'job_id':self.row['job_id'],'terminal':self.row['terminal_confirmed']}
    def confirm_terminal_and_release(self,run_key,job_id):
        if not self.row['terminal_confirmed']:raise ValueError('terminal state not confirmed')
        return {'key_retained':run_key,'released':True,'job_id':job_id}
class Executor:
    def __init__(self,row):self.row=row;self.calls=[]
    def launch(self,job_id):
        if job_id!=self.row['job_id']:raise ValueError('persisted job identity changed')
        self.calls.append(['launch',job_id]);return job_id
    def attach(self,job_id):
        if job_id!=self.row['job_id']:raise ValueError('persisted job identity changed')
        self.calls.append(['attach',job_id]);return job_id
    def status(self,job_id):return 'terminal' if self.row['terminal_confirmed'] else 'running'
config_skeleton={'steps':[{'id':'admission','name':'python:3.11','args':['python3','learner.py']},{'id':'function_test','name':'python:3.11','args':['python3','tests.py']},{'id':'execute','name':'python:3.11','args':['python3','execution_fixture.py']}]}
'''.replace('POLICY',repr(pol))
body='''def admit(event, coordinator, executor):
    reservation = coordinator.atomic_admit(event['run_key'],event['pipeline'])
    if reservation['status'] == 'busy':
        return {'status':'defer','job_id':reservation['job_id']}
    elif reservation['status'] == 'accepted':
        job_id = executor.launch(reservation['job_id'])
        return {'status':'accepted','job_id':job_id}
    else:
        if executor.status(reservation['job_id']) == 'terminal':
            released = coordinator.confirm_terminal_and_release(event['run_key'],reservation['job_id'])
            return {'status':'completed','job_id':reservation['job_id'],'release':released}
        else:
            job_id = executor.attach(reservation['job_id'])
            return {'status':'duplicate','job_id':job_id}
config = config_skeleton
config['steps'][1]['waitFor'] = ['admission']
config['steps'][2]['waitFor'] = ['function_test']
with open('build.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('build.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
assert resolved['steps'][1]['waitFor'] == ['admission']
assert resolved['steps'][2]['waitFor'] == ['function_test']
'''
tail='''# Supplied independent trace/restart driver: coordinator authority is external to
# learner function, not reconstructed from a learner-local dictionary.
report={'config':resolved,'fixtures':[]}
for r in traces:
    coordinator=Coordinator(r);executor=Executor(r)
    event={'run_key':r['run_key'],'pipeline':r['pipeline']}
    result=admit(event,coordinator,executor)
    if r['admission_status']=='busy':assert not executor.calls
    elif r['terminal_confirmed']:assert not executor.calls and result['release']['released']
    else:assert result['job_id']==r['job_id']
    report['fixtures'].append({'fixture':r['fixture'],'step':int(r['step']),'result':result,'calls':executor.calls,'persisted_job_id':r['job_id'],'logical_job_count':int(r['logical_job_count']),'active_slot_owner':r['active_slot_owner'],'event':r['event']})
'''
add(c,['idempotency_traces'],sc,body,'Implement admit(event,coordinator,executor). Call atomic_admit(run_key,pipeline): busy defers with no launch; accepted launches with the persisted job ID as token; duplicate attaches to that same ID, except confirmed terminal releases the slot and retains the completed key without relaunch. Return status/job_id, and release evidence for completed keys. Wire function_test waitFor admission and execute waitFor function_test in the existing config, safely write/reload build.yaml and assert both dependencies. Supplied fixture driver independently tests concurrent-delivery/restart/unknown-response/completion traces and persisted IDs; this adapter verifies admission decisions against fixture state, not a live concurrency platform. No local dictionary may be substituted for the coordinator.',['pyyaml'],tail)

# The glossary uses human-readable syntax descriptors for full workflows; the
# deterministic detector supports only a subset. Keep lists verbatim and narrow
# learner work to supported bindings, as required by GENERATOR allowed-syntax conflict.
# All surrounding adapters/algorithms are visibly supplied starter scaffolding.
for concept in ['distribution_monitoring','data_drift_detection','delayed_label_quality','ml_resource_utilization','ml_workload_cost_attribution']:
    d=codes[concept]
    for old,new in [('np.mean','mean_operation'),('np.std','std_operation')]:
        d['body']=d['body'].replace(old,new)
    if concept=='distribution_monitoring':
        d['body']=d['body'].replace('np.histogram','histogram_operation')
        edits='mean_operation = np.mean\nstd_operation = np.std\nhistogram_operation = np.histogram\n'
        assignment='mean_operation=np.mean, std_operation=np.std and histogram_operation=np.histogram'
    else:
        edits='mean_operation = np.mean\nstd_operation = np.std\n'
        assignment='mean_operation=np.mean and std_operation=np.std'
    d['scaffold']+='\nimport numpy as np\n'
    d['tail']='\n'+d['body']+'\n'+d['tail']
    d['body']=edits
    d['prompt']='Complete only the two NumPy operation bindings (three for fixed-edge monitoring): '+assignment+'. The visible supplied adapter implements the broader workflow below and calls your bindings on the selected arrays; it is not learner-written code. Do not change the supplied adapter. This is a narrowed supported-syntax task, not independent implementation of the full workflow. '+' Supplied workflow specification (context only, not additional learner edits): '+d['prompt']
for concept,filename in [('actionable_ml_alerts','alert.yaml'),('ml_workload_cost_guardrail','budget.yaml'),('retraining_run_idempotency','build.yaml')]:
    d=codes[concept]
    d['body']=d['body'].replace('yaml.safe_dump','dump_operation').replace('yaml.safe_load','load_operation')
    d['scaffold']+='\nimport yaml\nsafe_dump_method=yaml.safe_dump\nsafe_load_method=yaml.safe_load\n'
    d['tail']='\n'+d['body']+'\n'+d['tail']
    d['body']='dump_operation = safe_dump_method\nload_operation = safe_load_method\n'
    d['prompt']='Complete only dump_operation=safe_dump_method and load_operation=safe_load_method, the supplied yaml.safe_dump/yaml.safe_load references. The visible supplied workflow adapter writes and inspects '+filename+' using your bound safe serialization functions; unsafe object constructors are forbidden. Do not change the adapter. This narrows learner work to supported syntax; wider replay/admission behavior is supplied, not independently implemented by the learner. '+' Supplied workflow specification (context only, not additional learner edits): '+d['prompt']
# Evidence-backed rollback selection: numeric diagnosis is supplied; recovery remains
# unexecuted. The learner chooses an authorized response binding, not cloud access.
d=codes['production_regression_diagnosis']
d['scaffold']+="\napproved_rollback = 'approved_rollback'\nretraining = 'authorized_retraining'\ndrift_only = 'distribution_difference_only'\n"
d['tail']=d['body'].replace("report['response'] = 'approved_rollback'", "report['response'] = selected_response")+'\n'+d['tail']
d['body']='selected_response = approved_rollback\n'
d['prompt']='The supplied diagnosis adapter computes the release/cohort evidence. Bind selected_response to the supplied approved_rollback, retraining or drift_only response object consistent with the isolated configuration mismatch and fixture authorization. No action executes. This is a narrowed response-selection task; analysis is supplied scaffolding. '+' Supplied workflow specification (context only, not additional learner edits): '+d['prompt']
# Candidate validation: supplied arithmetic handles zero denominators. Learner selects
# which supplied column identities the mandatory slice and compatibility gates inspect.
d=codes['retrained_candidate_validation']
d['scaffold']+="\nrequired_slice_field = 'slice_pass'\nrequired_compatibility_field = 'compatibility_pass'\naggregate_only_field = 'cohort_id'\n"
d['tail']=d['body'].replace("candidate['slice_pass']", "candidate[slice_field]").replace("candidate['compatibility_pass']", "candidate[compatibility_field]")+'\n'+d['tail']
d['body']='slice_field = required_slice_field\ncompatibility_field = required_compatibility_field\n'
d['prompt']='Complete the two required gate-column bindings: slice_field selects required_slice_field, compatibility_field selects required_compatibility_field. An aggregate-only substitute is not a required gate. The supplied visible rates/verdict adapter and assertions test valid, boundary and failing candidates on validation-only data with artifact identity enforcement. Do not change supplied arithmetic or tests. This is a narrowed supported-syntax gate-wiring task, not independent verdict implementation. '+' Supplied workflow specification (context only, not additional learner edits): '+d['prompt']

# Generic normalize helper, unchanged scaffold, converts numpy values for JSON tests.
normalize='''def plain(v):
    if isinstance(v,dict):return {k:plain(x) for k,x in v.items()}
    if isinstance(v,list):return [plain(x) for x in v]
    if hasattr(v,'tolist'):return v.tolist()
    return v
report=plain(report)
'''

# Data-backed multi-task simulations: selections are declarative evidence work, never
# claimed to perform destructive operations or launch actual retraining.
table_specs={
'retraining_trigger_policy':('trigger_events',[('Identify the unauthorized event that must be rejected at entry.',lambda r:not r['authorized'],'event_id'),('Identify the uninvestigated alarm that must be rejected at entry.',lambda r:not r['investigated'],'event_id'),('Select the investigated matched-label quality-decline event; its intended dataset must be retained.',lambda r:r['event_type']=='quality','dataset_ref'),('Select the investigated distribution-only event, which does not establish labeled quality loss.',lambda r:r['event_type']=='distribution' and r['investigated'],'evidence'),('Select the failed data-quality event: dependent train/evaluate/promote cannot execute.',lambda r:not r['data_quality_pass'],'entry_stage'),('Select the scheduled refresh dataset.',lambda r:r['event_type']=='schedule' and r['authorized'],'dataset_ref'),('Select the authorized new-data event with a passing required data check.',lambda r:r['event_type']=='new_data' and r['data_quality_pass'],'dataset_ref'),('Select the promotion_approved cell for the eligible matched-label event; retraining eligibility is not promotion approval.',lambda r:r['event_type']=='quality','promotion_approved')]),
'authorized_retraining_execution':('execution_fixtures',[('Select the only event that passes authorization, verified immutable input and all fatal gates.',lambda r:r['expected_entry']=='accept','event_id'),('For the admitted event, select the version-specific object generation consumed by execution (an identity, not a quantity).',lambda r:r['expected_entry']=='accept','object_generation'),('For the admitted event, select the approved byte-verification digest.',lambda r:r['expected_entry']=='accept','sha256'),('For the admitted event, select the supplied execution token that must be retained.',lambda r:r['expected_entry']=='accept','ClientRequestToken'),('Select the event denied by authorization: no training may launch.',lambda r:not r['authorized'],'expected_entry'),('Select the event denied by immutable-generation/byte verification.',lambda r:not r['bytes_verified'],'expected_entry'),('Select the event denied by a fatal required gate.',lambda r:not r['fatal_gate_pass'],'expected_entry')]),
'serving_resource_cleanup':('cleanup_inventory',[('Select the only runtime-inspected, authorized exclusively retired container eligible to stop then remove.',lambda r:r['exclusively_retired'],'NAME'),('Select the corresponding exclusively retired nonproduction instance eligible for deletion under the supplied preserve-all-attached-disks policy.',lambda r:r['exclusively_retired'],'INSTANCE'),('Select the active release that must remain healthy and preserved.',lambda r:r['approved_inventory']=='active','NAME'),('Select the required active model artifact to retain.',lambda r:r['approved_inventory']=='active','model_artifact'),('Select the shared image referenced by the active release; retiring a container does not authorize image deletion.',lambda r:r['approved_inventory']=='active','image_ref'),('Select the shared active preprocessing artifact to retain.',lambda r:r['approved_inventory']=='active','preprocessing_artifact'),('Select the old resource outside permitted ownership that must not be removed.',lambda r:r['approved_inventory']=='not_authorized','NAME'),('Select the sanitized inspection logs for the verified retired container before action.',lambda r:r['exclusively_retired'],'logs'),('Select the expected post-action absence for the verified retired resource.',lambda r:r['exclusively_retired'],'expected_after')])}

out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for t in plans['tiles']:
 sc=next(x for x in screens['tiles'] if x['tile_id']==t['tile_id'])
 first=set();it=[];n=0
 for step in t['steps']:
  typ=step['planned_interaction_type']
  if not typ:continue
  n+=1;cid=step['concept_ids'][0];c=cid.split('.',1)[1];b=bundles[cid]
  ms=[{'concept_id':cid,**copy.deepcopy(a)} for a in b['assessment_anchors'] if cid+'#assessment:'+a['capability'] in step['anchors']]
  ix={'type':typ,'interaction_id':'ix.'+step['step_id'],'grading_mode':'client','difficulty':('intro' if n==1 else 'stretch' if n>=4 else 'core'),'standalone':True,'measures':ms,'anchors':step['anchors'],'feedback':fb(c)}
  if cid not in first:
   rem=next((r for r in sc.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
   first.add(cid)
  if typ=='choice':
   prompt,correct,wrong=checks[c];opts=[{'option_id':'a','text':correct}]+[{'option_id':chr(98+j),'text':w[0]} for j,w in enumerate(wrong)]
   ix['public']={'prompt':prompt,'options':opts,'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':['a'],'option_feedback':{'a':{'message':'This follows the declared evidence and rule.'},**{chr(98+j):{'message':w[1]} for j,w in enumerate(wrong)}}}
   ix['feedback']['hints']=['Identify exactly what the stated evidence establishes.','Check whether every required condition is met, rather than assuming a stronger conclusion.']
  elif typ=='table_select':
   name,specs=table_specs[c];data=rows(name);tasks=[];answers=[]
   for j,(prompt,predicate,col) in enumerate(specs):
    selected=[r for r in data if predicate(r)];assert len(selected)==1
    r=selected[0];key=next(iter(r));tid='task'+str(j+1)
    tasks.append({'task_id':tid,'prompt':prompt,'target_kind':'cell'})
    answers.append({'task_id':tid,'row':{'where':{key:r[key]},'occurrence':0},'column':col,'expect_value':r[col]})
   ix['public']={'asset_ref':{'asset_id':'ds.'+name},'intro':b['practice_anchor']['objective']+' This planned table-selection adapter records evidence choices only: no live launch, deletion or credential disclosure occurs. Use the declared fixture policy and explicit row evidence.','tasks':tasks}
   ix['grading']={'answers':answers,'task_feedback':{x['task_id']:{'correct':'Selected evidence satisfies the stated condition.','incorrect':'Reconcile the row identity and authorization or eligibility condition before selecting.'} for x in tasks}}
  elif typ=='classify':
   data=rows('evidence_scenarios');mapping={'P(X)':'input','P(Y|X)':'conditional','matched_label_errors':'quality'}
   ix['public']={'prompt':'Match each independent scenario to the evidence it establishes, not to further unproved conclusions. Input shift does not establish P(Y|X) or labeled quality; conditional relationship change alone does not establish input shift or quality loss; matched errors above the declared reference establish observed quality loss, not its drift cause.','buckets':[{'bucket_id':'input','label':'Input distribution shift only; other changes unresolved'},{'bucket_id':'conditional','label':'Conditional target relationship change; other changes unresolved'},{'bucket_id':'quality','label':'Matched-label quality degradation; drift cause unresolved'}],'items':[{'item_id':'item'+str(j+1),'text':r['observation']+' '+r['unresolved'],'source':{'asset_id':'ds.evidence_scenarios','row':{'where':{'scenario_id':r['scenario_id']},'occurrence':0},'column':'supported_evidence'}} for j,r in enumerate(data)]}
   ix['grading']={'assignments':{'item'+str(j+1):mapping[r['supported_evidence']] for j,r in enumerate(data)},'role_map':mapping,'item_feedback':{'item'+str(j+1):{'message':r['unresolved']} for j,r in enumerate(data)}}
  elif typ=='code_exercise':
   d=codes[c];infra='if True:\n'+textwrap.indent(d['scaffold'],'    ')
   driver='if True:\n'+textwrap.indent(d['tail']+'\n'+normalize,'    ')
   starter=infra+'\n# TODO: implement the requested calculations/configuration/command bindings.\n'+driver
   solution=infra+'\n'+d['body']+'\n'+driver
   mounts=[{'asset_id':'ds.'+a,'mount_path':a+'.csv'} for a in d['mounts']]
   cons={k:b['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}
   ix['public']={'prompt':d['prompt'],'runtime':{'kind':'python','version':pins['python']['version'],'packages':d['packages']},'workspace':{'entry':'learner.py','files':[{'path':'learner.py','role':'editable','language':'python','content':starter}],'asset_mounts':mounts},'constraints':cons}
   # Derive expected by actually executing the reference solution in pinned Pyodide.
   tables,_,=sandbox._tables(reg,mounts,{},[])
   job=sandbox._py_job('python',d['packages'],[sandbox._py_script('derive','learner.py',solution,sandbox._py_mounts(tables),[{'id':'report','kind':'expr','expr':'report'}])])
   result=sandbox.node_run(job,pins['python']['runner'])['results']['derive']
   if not result['ok']:raise RuntimeError(c+': '+result['error'])
   if not result['probes']['report']['ok']:raise RuntimeError(result['probes'])
   expected=result['probes']['report']['value']
   ix['grading']={'solution_files':[{'path':'learner.py','content':solution}],'tests':[{'test_id':'result','kind':'value_equals','message_on_fail':'Recheck the declared scope, calculations and all required conditions.','spec':{'expr':'report','expected':expected,'tolerance':1e-9}}]}
   v,u,_=pysyntax.judge(solution,cons['allowed_syntax'],cons['blocked_syntax'],starter)
   print(c,'SYNTAX',v,'UNMAPPED',u)
  else:raise ValueError(typ)
  it.append({'step_id':step['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':it})
(P/'interactions.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('wrote',sum(len(t['interactions']) for t in out['tiles']))
