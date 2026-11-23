import json, ast, copy, pathlib
B=pathlib.Path(__file__).parent
P=B/'interactions.json'
d=json.loads(P.read_text()); before=copy.deepcopy(d)
ix={r['step_id']:r['interaction'] for t in d['tiles'] for r in t['interactions']}
def get(tile,step):return ix['mle.tile.'+tile+'.'+step]
def chunks(i):
 s=i['grading']['solution_files'][0]['content']; out=[]
 for n in ast.parse(s).body:
  text=ast.get_source_segment(s,n)
  if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec':
   out.append((ast.literal_eval(n.value.args[0]),True))
  else:out.append((text,False))
 return out
def wrap(s):return 'exec('+repr(s)+')'
def commit(i,pairs,prompt):
 # Each pair is (solution, starter); unchanged infrastructure remains verbatim.
 i['grading']['solution_files'][0]['content']='\n\n'.join(x for x,y in pairs)+'\n'
 i['public']['workspace']['files'][0]['content']='\n\n'.join(y for x,y in pairs)+'\n'
 i['public']['prompt']=prompt
 for key in ['hidden_checks','execution_provenance']:i['grading'].pop(key,None)
def supplied(text,wrapped):
 s=wrap(text) if wrapped else text
 return (s,s)
def todo(s,starter):return (s,starter)
# All numerical summaries, selection, normalization, identity-bound construction and emission are learner work.
i=get('080_082','s04'); c=chunks(i); cut=next(n for n,(s,w) in enumerate(c) if s.startswith('ref_values ='))
pairs=[supplied(s,w) for s,w in c[:cut]]
summary='''def summarize(reference, production, policy):
    fixed_edges = policy['fixed_edges']
    summaries = []
    for data in [reference, production]:
        values = data['numeric_values']
        values = values[(values >= policy['eligible_numeric_range'][0]) & (values <= policy['eligible_numeric_range'][1])]
        counts = np.histogram(values, bins=fixed_edges)[0]
        proportions = counts / len(values)
        categories = {}
        for category in policy['declared_categories']:
            categories[category] = np.sum(data['category'] == category) / len(data['category'])
        classes = {}
        for predicted_class in policy['declared_classes']:
            classes[predicted_class] = np.sum(data['predicted_class'] == predicted_class) / len(data['predicted_class'])
        summaries = summaries + [{'eligible_total': len(values), 'category_total': len(data['category']), 'class_total': len(data['predicted_class']), 'bin_proportions': proportions, 'mean': np.mean(values), 'std': np.std(values, ddof=0), 'categories': categories, 'classes': classes}]
    record = {'reference_id': policy['reference_id'], 'window': policy['production_window'], 'fixed_edges': fixed_edges, 'category_definitions': policy['declared_categories'], 'class_definitions': policy['declared_classes'], 'ddof': policy['ddof'], 'reference': summaries[0], 'production': summaries[1]}
    emit(record)
    return record'''
pairs += [todo(summary,"def summarize(reference, production, policy):\n    # TODO: select observations, calculate all window summaries, build and emit one record.\n    return None"),supplied('summarize(reference, production, policy)',True)]
commit(i,pairs,'Implement summarize(reference, production, policy) using the supplied loader and emission client. Select eligible numeric observations; calculate fixed-edge bin proportions, means and ddof=0 standard deviations; calculate probabilities for every declared category and predicted class using each window’s own total; construct and emit exactly one monitoring record with the supplied identity, window, definitions and totals.')
i=get('080_082','s14'); pairs=[]
names=['ref_mean','cur_mean','ref_std','cur_std','reference_categories','current_categories','reference_bins','current_bins','category_distance','numeric_distance','category_drift','numeric_drift']
for s,w in chunks(i):
 name=s.split(' =')[0]
 pairs.append(todo(s,'# TODO: calculate '+name+'\n'+name+' = None') if name in names else supplied(s,w))
commit(i,pairs,'Complete the marked learner assignments using the supplied scaffold and declared policy. Complete the numeric summaries, aligned category probabilities, category and numeric-bin distances, and strict distance > 0.20 decisions. Use each window’s own eligible totals and retain the supplied comparison metadata and unresolved-quality wording.')
# Keep parsing/cutoff infrastructure but remove the fully solved quality scaffold.
i=get('083_085','s06');pairs=[]
for s,w in chunks(i):
 if s.startswith(('loss_mean =','loss_std =')):continue
 if s.startswith('def quality('):
  s=s.replace('loss_mean(losses)','np.mean(losses)').replace('loss_std(losses, ddof=0)','np.std(losses, ddof=0)')
  # Preserve eligible cohort before checking maturity, so availability boundaries do not shrink its denominator.
  s=s.replace(" and (row['prediction_timestamp'] <= cutoff)", '')
  s=s.replace("if key in cohort and row['label_timestamp']", "if key in cohort and cohort[key]['prediction_timestamp'] <= cutoff and row['label_timestamp']")
  pairs.append(todo(s,"def quality(prediction_rows, label_rows):\n    # TODO: duplicate rejection, keyed eligible cohort, maturity/availability join, exclusions and scoped report.\n    return None"))
 else:pairs.append(supplied(s,w))
commit(i,pairs,'Complete quality(prediction_rows, label_rows): reject duplicate prediction and label IDs, preserve eligible cohort records and prediction times, attach only available labels belonging to the mature cohort, record excluded label IDs, and return separate eligible/mature counts, coverage, matched error proportion and mature-loss mean/std with ddof=0. Report unavailable when no mature labels match.')
# Replace rate aliases and solved evidence selection, while retaining schema construction as infrastructure.
i=get('083_085','s16');c=chunks(i);pairs=[]
start=next(n for n,(s,w) in enumerate(c) if s.startswith('supplied_rates ='))
end=next(n for n,(s,w) in enumerate(c) if s=='result = []')
pairs=[supplied(s,w) for s,w in c[:start]]
rate="""selected_rates = []
for group in rate_groups:
    rate = None
    if matched_counts[group] > 0:
        rate = error_counts[group] / matched_counts[group]
    selected_rates = selected_rates + [rate]"""
pairs.append(todo(rate,"selected_rates = []\n# TODO: append each group's own error/count rate; None for zero matched counts."))
# Infrastructure only transfers metadata and the learner-selected response into the declared schema.
for s,w in c[end:]:
 if s.startswith('for row in evidence:'):
  old=s
  begin=s.index("    response = 'investigate'"); finish=s.index('    result.append(')
  logic="""    response = 'investigate'
    gates = []
    if row['active_config'] != row['approved_config'] and row['active_artifact'] == row['approved_artifact'] and n > 0 and row['schema_pass'] and row['hypothesis_test'] == 'bad configuration reproduces errors; approved rollback restores baseline' and row['supported_response'] == 'approved_rollback':
        response = 'approved_rollback'
        gates = ['readiness', 'bounded_prediction']
    elif row['client_impact'] == 'baseline':
        response = 'none'
"""
  # The quoted replay observation is taken directly from the registered dataset, not an invented answer.
  asset=json.loads((B/'scenario_asset_registry.json').read_text())
  a=next(a for a in asset['assets'] if a['asset_id']=='ds.release_evidence')
  cols=[x['name'] for x in a['columns']]
  replay=next(dict(zip(cols,row))['hypothesis_test'] for row in a['rows'] if dict(zip(cols,row))['supported_response']=='approved_rollback')
  logic=logic.replace(repr('bad configuration reproduces errors; approved rollback restores baseline'),repr(replay))
  # A supplied per-row schema helper does not supply calculations or decisions.
  helper="def diagnostic_record(row, rate, response, gates):\n    n = row['matched_eligible_labels']\n    errors = row['labeled_errors']\n    return "+s[finish:].split('result.append(',1)[1].rstrip(')')
  pairs.append(supplied(helper,True))
  learner="for row in evidence:\n    n = row['matched_eligible_labels']\n    rate = selected_rates[len(result)]\n"+logic+"    result = result + [diagnostic_record(row, rate, response, gates)]"
  starter="for row in evidence:\n    # TODO: evaluate identity and replay evidence, then select response and required gates.\n    rate = None\n    response = None\n    gates = []\n    result = result + [diagnostic_record(row, rate, response, gates)]"
  pairs.append(todo(learner,starter))
 else:pairs.append(supplied(s,w))
commit(i,pairs,'Calculate each release/cohort’s error rate from its own matched eligible count, returning None for zero counts. Evaluate the configuration-mismatch hypothesis using the active/approved identities and supplied replay evidence, then select the policy-supported response and required gates without executing recovery. Return result in the supplied diagnostic-record schema.')
# Durable-admission implementation and assertions, with a real persisted unknown-response fixture.
i=get('086_089','s16');pairs=[]
for s,w in chunks(i):
 if s.startswith('def run_fixtures('):
  s=s.replace("    c3, e3 = fresh()\n    out['unknown_response'] = {'result': admit(event, c3, e3), 'state': durable_state()}","    reset()\n    c3, e3 = fresh()\n    e3.unknown_once = True\n    uncertain = admit(event, c3, e3)\n    c4, e4 = fresh()\n    out['unknown_response'] = {'result': admit(event, c4, e4), 'state': durable_state()}")
 if s.startswith('class Executor:'):
  s=s.replace("            self.coordinator.write(state)\n            return job", "            self.coordinator.write(state)\n            if getattr(self, 'unknown_once', False):\n                self.unknown_once = False\n                return None\n            return job")
 if s.startswith('def supplied_admit('):
  s=s.replace('def supplied_admit(', 'def admit(')
  s=s.replace("        executor.launch(claim['job_id'])", "        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.attach(claim['job_id'])")
  pairs.append(todo(s,"def admit(event, coordinator, executor):\n    # TODO: atomic claim, defer/completed paths, persisted launch/attach, terminal release.\n    return None"));continue
 if s=='admit = supplied_admit':continue
 if s.startswith('assert '):pairs.append(todo(s,'assert None  # TODO: invariant over concurrency/restart results'));continue
 pairs.append(supplied(s,w))
extra="assert result['unknown_response']['result']['job_id'] == result['restart_launch']['result']['job_id'] and result['unknown_response']['state']['jobs'] == result['restart_launch']['state']['jobs']"
pairs.append(todo(extra,'assert None  # TODO: unknown launch response and fresh-worker reconciliation retain one logical job.'))
commit(i,pairs,'Implement admit(event, coordinator, executor) using the supplied contracts. Defer busy claims; return completed claims without relaunching; launch accepted claims using their persisted job ID; attach or reconcile duplicate claims using that same identity; release only after terminal confirmation. Complete assertions over the supplied concurrency and restart results.')
# Candidate calculations and predicates are learner functions, not aliases.
i=get('086_089','s21');pairs=[]
for s,w in chunks(i):
 if s.startswith(('rates = supplied_rates','evaluate = supplied_evaluate')):continue
 if s.startswith(('def supplied_rates(','def supplied_evaluate(')):
  s=s.replace('supplied_rates','rates').replace('supplied_evaluate','evaluate')
  signature=s.splitlines()[0]
  pairs.append(todo(s,signature+'\n    # TODO: implement the declared calculations and gates.\n    return None'));continue
 if s.startswith('assert '):pairs.append(todo(s,'assert None  # TODO: fixture acceptance/rejection predicate'));continue
 if s.startswith('def check_failure('):pairs.append(todo(s,"def check_failure(pair):\n    assert None  # TODO: reject every failing fixture"));continue
 pairs.append(supplied(s,w))
commit(i,pairs,'Implement rates(model) and evaluate(incumbent, candidate, requested_identity). Calculate actual-class conditional rates and expected cost, reject undefined conditioning groups, enforce incumbent-relative cost and every required quality/slice/compatibility/cohort/identity gate, and return the declared identity-bound record. Complete assertions for valid, equality-boundary and failing fixtures.')
# State transition simulator: describe/start/connect/workload/stop/describe must actually occur.
i=get('091_094','s09');pairs=[]
simulator='''class LifecycleSimulator:
    def __init__(self, rows):
        self.rows = rows
        self.actions = []
        self.records = []
        self.sessions = {}
    def act(self, row, action):
        key = (row['INSTANCE'], row['ZONE'], row['reporting_window'])
        session = self.sessions.setdefault(key, {'state': row['before_state'], 'sequence': [], 'completed_work': '0'})
        allowed = ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']
        position = len(session['sequence'])
        if position >= len(allowed) or action != allowed[position]:
            return False
        session['sequence'].append(action)
        self.actions.append({'INSTANCE': row['INSTANCE'], 'ZONE': row['ZONE'], 'reporting_window': row['reporting_window'], 'action': action})
        if action == 'start':
            session['state'] = 'RUNNING'
        elif action == 'workload' and session['state'] == 'RUNNING':
            session['completed_work'] = row['completed_work']
        elif action == 'stop':
            session['state'] = 'TERMINATED'
        if len(session['sequence']) == len(allowed):
            record = dict(row)
            record['completed_work'] = session['completed_work']
            record['after_state'] = session['state']
            self.records.append(record)
        return True
    def evidence(self):
        verified = len(self.records) == len(self.rows) and all(s['state'] == 'TERMINATED' and s['sequence'] == ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'] for s in self.sessions.values())
        return {'identity': policy['authorized_identity'], 'actions': self.actions, 'records': self.records, 'verified_stopped': verified}

def simulate_sequences(sequences):
    sim = LifecycleSimulator(lifecycle_rows)
    for row in lifecycle_rows:
        for action in sequences[row['workload']]:
            sim.act(row, action)
    return sim.evidence()'''
for s,w in chunks(i):
 if s.startswith('def bounded_workloads('):
  pairs.append(supplied(simulator,True))
  seq="sequences = {'training': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'], 'inference': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']}"
  pairs.append(todo(seq,"# TODO: complete each approved lifecycle action sequence.\nsequences = {'training': [], 'inference': []}"));continue
 if s=='lifecycle_record = bounded_workloads()':pairs.append(supplied('lifecycle_record = simulate_sequences(sequences)',True));continue
 if s.startswith('for row in charges:'):
  pairs.append(todo(s,"for row in charges:\n    # TODO: accumulate export total and apply direct/shared/unallocated policy.\n    export_total = export_total"));continue
 if s.split(' =')[0] in ['training_mean','training_std','inference_mean','inference_std']:
  name=s.split(' =')[0];pairs.append(todo(s,'# TODO: numeric summary\n'+name+' = None'));continue
 pairs.append(supplied(s,w))
commit(i,pairs,'Complete the approved describe/start/connect/workload/stop/describe sequences for both tagged instances using the supplied lifecycle simulator; retain the resulting separate workload windows and verified final states. Complete the direct/shared/unallocated allocation loop from policy, and training_mean, training_std, inference_mean and inference_std for the separate per-window arrays with ddof=0. Return result and retain reconciliation.')
# Guardrail simulator has distinct notification delivery, authorized response and captured-output evidence.
i=get('091_094','s14');pairs=[]
sim='''class NotificationResponseSimulator:
    def __init__(self, config):
        self.config = config
        self.states = {(policy['INSTANCE'], policy['ZONE']): 'RUNNING', ('untargeted-control', policy['ZONE']): 'RUNNING'}
        self.receipts = []
        self.actions = []
        self.output = []
        self.runtime_secret = 'fixture-runtime-only-credential'
    def describe(self):
        return {'INSTANCE': self.config['INSTANCE'], 'ZONE': self.config['ZONE'], 'state': self.states[(self.config['INSTANCE'], self.config['ZONE'])]}
    def notify(self, row):
        crossed = float(row['observed_spend']) >= self.config['budget_amount'] * self.config['threshold_ratio']
        if crossed and row['workload_scope'] == self.config['workload_scope']:
            self.receipts.append({'topic': self.config['notification_topic'], 'fixture': row['fixture']})
        return bool(self.receipts)
    def respond(self):
        c = self.config
        authorized = c['authorized_identity'] == policy['authorized_identity'] and [c['INSTANCE'], c['ZONE']] == [policy['INSTANCE'], policy['ZONE']]
        bound = c['event_binding'] == {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}
        secret_ok = c['secret_version_reference'] == policy['secret_version_reference'] and c['secretEnv'] == ['BUDGET_CLIENT']
        if self.receipts and authorized and bound and secret_ok:
            self.actions.append({'command': 'gcloud compute instances stop', 'INSTANCE': c['INSTANCE'], 'ZONE': c['ZONE']})
            self.states[(c['INSTANCE'], c['ZONE'])] = 'TERMINATED'
            self.output.append('stop completed: ' + c['INSTANCE'] + ' --zone=' + c['ZONE'])
        return authorized and bound and secret_ok
    def evidence(self, row):
        before = self.describe()
        notified = self.notify(row)
        authorized = self.respond()
        captured = '\\n'.join(self.output)
        target_only = all(a['INSTANCE'] == policy['INSTANCE'] and a['ZONE'] == policy['ZONE'] for a in self.actions) and self.states[('untargeted-control', policy['ZONE'])] == 'RUNNING'
        after = self.describe()
        return {'fixture': row['fixture'], 'notification': notified, 'notification_receipts': self.receipts, 'authorized_response': authorized and bool(self.actions), 'actions': self.actions, 'before': before, 'after': after, 'stop_completed': bool(self.actions) and after['state'] == 'TERMINATED', 'target_only': target_only, 'captured_output': captured, 'credential_non_disclosure': self.runtime_secret not in captured}

def apply_and_replay(config):
    expected = {k: policy[k] for k in ['workload_scope', 'budget_amount', 'period', 'threshold_ratio', 'notification_topic', 'response_pipeline', 'INSTANCE', 'ZONE', 'authorized_identity', 'secret_version_reference']}
    if any(config.get(k) != v for k, v in expected.items()):
        return {'status': 'invalid_config', 'resolved': config}
    results = [NotificationResponseSimulator(config).evidence(r) for r in budget_replay_rows]
    return {'resolved': config, 'fixtures': results, 'limitation': policy['residual_limitation']}'''
for s,w in chunks(i):
 if s.startswith('def apply_and_replay('):pairs.append(supplied(sim,True));continue
 if s.startswith('config ='):
  node=ast.parse(s).body[0]; keys=[ast.literal_eval(x) for x in node.value.keys]
  pairs.append(todo(s,'# TODO: populate from policy\nconfig = {'+', '.join(repr(k)+': None' for k in keys)+'}'));continue
 if s.startswith("config['secretEnv']") or s.startswith("config['event_binding']"):
  left=s.split(' =')[0];pairs.append(todo(s,'# TODO: runtime secret/event binding\n'+left+' = None'));continue
 if s.startswith(('safe_writer =','write_config =','safe_reader =','read_config =')):continue
 if s.startswith("with open('guardrail.yaml', 'w')"):
  pairs.append(todo("with open('guardrail.yaml', 'w') as h:\n    yaml.safe_dump(config, h)","with open('guardrail.yaml', 'w') as h:\n    # TODO: safely serialize mapping\n    h"));continue
 if s.startswith("with open('guardrail.yaml')"):
  pairs.append(todo("with open('guardrail.yaml') as h:\n    resolved = yaml.safe_load(h)","with open('guardrail.yaml') as h:\n    # TODO: safely reload mapping\n    resolved = None"));continue
 pairs.append(supplied(s,w))
commit(i,pairs,'Complete the supplied guardrail mapping from policy: workload scope, amount, period, threshold, existing event binding, approved fixed instance and runtime secret references. Safely serialize/reload it and inspect the resolved fields before passing it to the supplied notification/response simulator. Return that simulator’s target-state and captured-output evidence with the delayed-notification limitation.')
# Advisory edits only reword lead-ins for exercises that retain assignment structure.
for tile,step in [('083_085','s11'),('090_090','s05'),('091_094','s04')]:
 i=get(tile,step)
 i['public']['prompt']='Complete the marked learner assignments using the supplied scaffold and declared policy. '+i['public']['prompt']
# Add independent negative lifecycle evidence tests. Expected values will be computed, not typed.
i=get('091_094','s09')
for name,seq in [('no_workload',['describe','start','ssh','stop','describe']),('no_stop',['describe','start','ssh','workload','describe'])]:
 i['grading']['tests'].append({'test_id':name,'kind':'value_equals','spec':{'expr':"simulate_sequences("+repr({'training':seq,'inference':seq})+")[\"verified_stopped\"]"},'visible':True,'message_on_fail':'Incomplete lifecycle execution must not be verified as stopped.'})
# Independent persisted unknown-response evidence test.
i=get('086_089','s16')
i['grading']['tests'].append({'test_id':'unknown_response_durable_job','kind':'value_equals','spec':{'expr':"len(result['unknown_response']['state']['jobs']) == 1 and result['unknown_response']['result']['job_id'] in result['unknown_response']['state']['jobs']"},'visible':True,'message_on_fail':'Unknown response reconciliation must retain the persisted single logical job.'})
# Save ONLY named interactions; unchanged measures/keys outside named blocking tasks remain untouched.
named={'mle.tile.'+t+'.'+s for t,s in [('080_082','s04'),('080_082','s14'),('083_085','s06'),('083_085','s11'),('083_085','s16'),('086_089','s16'),('086_089','s21'),('090_090','s05'),('091_094','s04'),('091_094','s09'),('091_094','s14')]}
for bt,at in zip(before['tiles'],d['tiles']):
 for br,ar in zip(bt['interactions'],at['interactions']):
  if br['step_id'] not in named:assert br==ar
  else:
   for key in ['measures','anchors','feedback','type','difficulty','grading_mode','standalone']:assert br['interaction'].get(key)==ar['interaction'].get(key)
P.write_text(json.dumps(d,indent=2)+'\n')
print('Patched named interactions only:',len(named))
