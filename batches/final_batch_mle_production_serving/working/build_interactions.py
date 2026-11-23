import json, sys, copy
from pathlib import Path
sys.path.insert(0, str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox, pysyntax
B=Path('batches/final_batch_mle.region.production_serving')
P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
G={x['context']['concept_id']:x for x in G['bundles']}; A={x['asset_id']:x for x in R['assets']}
pin=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']['python']['version']
def wf(cid,name): return next(f['content'] for f in A['ws.'+cid.split('.')[-1]]['files'] if f['path']==name)
contract=json.loads(wf('mle.bounded_batch_inference','contract.json')); policy=json.loads(wf('mle.service_telemetry','measurement_policy.json'))
# Each tuple is prompt, correct option, and two misconception-based alternatives with specific feedback.
C={
'prediction_schema_validation':('Which procedure verifies the declared JSON acceptance and rejection fixtures during ordinary non-optimized execution?', 'Encode the request as JSON bytes, send POST with the JSON content-type and an explicit timeout, decode the response, and assert the declared fixture outcomes.', 'Inspect the raw JSON response text without decoding its fields.', 'Raw JSON text is not the decoded structure: json.loads must precede field checks.', 'Use assertions only for the valid fixture, leaving boundary and failure outcomes unchecked.', 'Assertions must also check the declared boundary and failure cases, not just the normal fixture.'),
'online_prediction_contract':('Where and how should the bounded standard-library HTTP fixture run?', 'Construct HTTPServer with the configured host, port and handler in the existing runtime, then use serve_forever; keep its use bounded rather than recommending it as a production server.', 'Treat http.server as the recommended production serving implementation.', 'The taught scope is a bounded fixture; http.server is not recommended as a production server.', 'Create a new platform instead of using the existing configured runtime.', 'The fixture uses the existing runtime and its configured host and port.'),
'bounded_batch_inference':('Which assertion plan verifies the declared batch fixture outcomes?', 'Assert normal and final-partial-chunk acceptance and the declared failure outcomes; let a false predicate raise AssertionError.', 'Assert only that execution finishes, regardless of the declared fixture outcomes.', 'Finishing execution does not check the required valid, boundary and failure predicates.', 'Treat a false assertion predicate as successful verification.', 'A false predicate raises AssertionError in ordinary non-optimized execution.'),
'model_service_readiness':('After starting the named supplied container with the declared port and nonsecret settings, which evidence should you inspect?', 'Inspect the named container image and State, and inspect captured logs for initialization or execution failures.', 'Accept the start command alone as proof that the intended container state has been verified.', 'Starting the container does not inspect its image identity or State.', 'Skip the captured logs even when initialization failures need to be checked.', 'Container logs provide the captured standard output and error needed to inspect failures.'),
'deployment_configuration_code':('Which repository workflow records the verified deployment configuration?', 'Create the configuration branch with git checkout -b, commit the verified configuration, then merge under the existing workflow.', 'Merge the branch without committing the verified configuration.', 'The taught workflow commits the verified configuration before merging.', 'Commit an unverified configuration instead of the verified configuration.', 'The workflow records the verified configuration, not an unchecked substitute.'),
'deployment_verification':('Which evidence supports accepting the release?', 'The running artifact and configuration match the record; runtime State and available Health are checked; bounded readiness and decoded prediction assertions match the declared contract.', 'Accept the release because deployment started, without checking identity or prediction output.', 'Deployment starting is not verification of the recorded artifact and expected prediction contract.', 'Accept any prediction output shape and values once the endpoint responds.', 'The fixture output shape and values must satisfy the declared task and response contract.'),
'prediction_authentication':('Verification fails with ValueError or GoogleAuthError. Which denied-path behavior is required?', 'Deny through the declared PermissionError path before prediction, and record the failure class without token or protected request values.', 'Execute prediction after verification failure, then report the failure.', 'Verification failure must be denied before executing prediction.', 'Print the token and protected request values to make denial visible.', 'Denial must be visible without disclosing credentials or protected request values.'),
'service_telemetry':('How should external availability and handler evidence be reconciled?', 'Retain every eligible external attempt in the denominator, count only valid HTTP-200 predictions within the deadline in the numerator, and explain failures with absent handler records.', 'Use only attempts reaching the handler as the availability denominator.', 'Connection refusals and response timeouts remain in the external denominator even when they never reach the handler.', 'Discard external failures if no corresponding handler record exists.', 'Absent handler records must be reconciled with external failures, not used to remove attempts.'),
'prediction_load_test':('Which design gives the declared valid-traffic capacity measurement?', 'Use the declared arrival/concurrency profile, valid payload mix, warm-up and fixed measurement duration; retain all client outcomes and run intentional malformed assertion fixtures separately.', 'Mix intentional malformed fixture requests into the valid-traffic capacity measurement.', 'Intentional malformed tests belong outside the valid-traffic capacity measurement.', 'Record only attempted request count and discard response times and failures.', 'The measurement needs client-visible outcomes and response times, with failed attempts counted separately.'),
'inference_batching_decision':('How should a batching limit be chosen from the supplied trace?', 'Match successful responses by request identity and setting, include batch waiting in completion-minus-start durations, and choose only a setting whose declared tail percentile meets the objective.', 'Remove batch waiting from each end-to-end duration before comparing the objective.', 'End-to-end latency includes batch waiting: it is response completion minus request start.', 'Use unmatched responses as successful samples to improve the tail estimate.', 'Only responses matched to a request identity and setting contribute to the successful-response population.'),
'serving_worker_concurrency':('Which sequence applies the declared worker bound in the existing runtime?', 'Set the worker-limit field in YAML, validate its parsed value, apply the declared Compose deployment and inspect resulting containers.', 'Apply the Compose deployment without checking the parsed worker-limit value.', 'The declared worker-limit field must be validated before the referenced image runs under that bound.', 'Change the YAML field but omit applying and inspecting the resulting deployment.', 'Editing alone does not apply the declared deployment or inspect the resulting containers.'),
'serving_replica_scaling':('Which evidence closes the bounded replica/lifecycle check?', 'Compare intended and observed container counts and identities before and after demand changes, inspect instance status and identity around the authorized action, and restore original replica and lifecycle settings.', 'Leave the changed replica and lifecycle settings in place after the bounded test.', 'The nonproduction runtime must be restored to its original replica and lifecycle settings.', 'Record intended replica counts without inspecting running identities or instance state.', 'Intended counts are not observed evidence; containers and instance status/identity must be inspected.'),
'model_release_rollback':('Which artifact is the rollback target?', 'The previously approved registry version and its recorded immutable image reference.', 'An unapproved latest version selected only because it is latest.', 'Rollback preserves the previous approval/version identity rather than selecting an unapproved latest version.', 'A mutable image tag instead of the previous recorded immutable reference.', 'The approved replacement uses the recorded previous immutable image reference.'),
'rollback_secrets':('Where should sensitive values come from during rollback?', 'The runtime secret mechanism; configuration and image instructions contain no secret literals.', 'Dockerfile ARG or ENV instructions containing the secret value.', 'Secret values in Dockerfile ARG or ENV persist in the final image or metadata.', 'Literal credential values embedded in the release configuration.', 'Sensitive values are supplied by the runtime secret mechanism rather than embedded in configuration.')}
# Tables are bounded fixture evidence tasks, not claims of real cloud execution.
T={
'prediction_schema_validation':('ds.orders', [('Select the cell beyond the declared permitted upper numeric boundary; this input must be rejected, not predicted successfully.', lambda r:r['feature_1']>contract['feature_max'],'feature_1')], 'variant.beyond_limit'),
'online_prediction_contract':('ds.batch_results', [('Select the prediction cell for the first observation key in the supplied online request; compare it with the decoded response, not raw JSON.',lambda r:r['order_id']==A['ds.orders']['rows'][0][0],'prediction'),('Select the release-version field in that same keyed result; identical valid requests must keep this fitted package unchanged.',lambda r:r['order_id']==A['ds.orders']['rows'][0][0],'version')], None),
'model_service_readiness':('ds.readiness_cases', [('Select the only row whose initialization state permits successful readiness.',lambda r:r['model_initialized'] and r['preprocessor_initialized'] and not r['initialization_failed'],None),('Select the model-initialization cell in the row where only preprocessing is initialized. This is an unready case despite partial initialization.',lambda r:not r['model_initialized'] and r['preprocessor_initialized'] and not r['initialization_failed'],'model_initialized')],None),
'deployment_configuration_code':('ds.release_records', [('Select the immutable image-reference cell for the approved previous release; use this reference when authoring and validating the deployment configuration.',lambda r:r['approved'],'image_reference'),('Select the published host-port cell for that approved release, to preserve the intended deployment setting.',lambda r:r['approved'],'host_port')],None),
'deployment_verification':('ds.release_records', [('Select the approved image-reference cell against which the running container identity must be verified.',lambda r:r['approved'],'image_reference'),('Select the container identity cell for the same approved release, to identify the target of State, Health and sanitized-log inspection.',lambda r:r['approved'],'container_name')],None),
'prediction_authentication':('ds.release_records', [('Select the approved protected-service container identity to inspect for denial evidence without copying credentials or protected request values.',lambda r:r['approved'],'container_name')],None),
'prediction_load_test':('ds.backlog', [('Select the final unfinished-work cell in the lowest tested offered-rate window. Its non-growing backlog must be considered alongside throughput, failures and tail latency.',lambda r:r['experiment']=='load' and r['setting']=='rate_5' and r['elapsed_seconds']==policy['load']['measurement_seconds'],'unfinished_requests'),('Select the final unfinished-work cell for the middle offered-rate window; growing backlog prevents accepting that rate solely from arrival count.',lambda r:r['experiment']=='load' and r['setting']=='rate_10' and r['elapsed_seconds']==policy['load']['measurement_seconds'],'unfinished_requests')],None),
'serving_worker_concurrency':('ds.worker_processes', [('Select the supervisor row in the within-bound interval; this process must not be counted as a prediction worker.',lambda r:r['interval_id']=='within_limit' and not r['is_prediction_worker'],None),('Select the extra prediction-worker row present only in the oversubscribed interval.',lambda r:r['interval_id']=='oversubscribed' and r['is_prediction_worker'] and r['pid']==max(v['pid'] for v in [dict(zip([c['name'] for c in A['ds.worker_processes']['columns']],row)) for row in A['ds.worker_processes']['rows']]),None)],None),
'serving_replica_scaling':('ds.replica_states', [('Select the restored-phase row that verifies the original replica and lifecycle settings were restored.',lambda r:r['phase']=='restored',None),('Select the intended-replica-count cell for the restored phase; compare it with the original count rather than leaving the changed setting active.',lambda r:r['phase']=='restored','intended_replicas')],None),
'model_release_rollback':('ds.release_transition', [('Select the first event row where the approved replacement is verified while the faulty release remains running.',lambda r:r['A_verified'] and r['B_running'],None),('Select the row where only the faulty release has been removed and the approved replacement remains running and verified.',lambda r:r['B_removed'] and r['A_running'] and r['A_verified'],None)],None)}

def base(s,t,rank):
 cid=s['concept_ids'][0]; aa={x['capability']:x for x in G[cid]['assessment_anchors']}
 measures=[dict(concept_id=cid,capability=a.split('#assessment:')[1],fact_ids=copy.deepcopy(aa[a.split('#assessment:')[1]]['fact_ids'])) for a in s['anchors'] if '#assessment:' in a]
 ix=dict(type=s['planned_interaction_type'],interaction_id='ix.'+s['step_id'],difficulty=rank,grading_mode='client',standalone=False,measures=measures,anchors=copy.deepcopy(s['anchors']),feedback={'correct':{'message':'The evidence matches the declared contract and the taught verification procedure.'},'incorrect':{'message':'Recheck the declared contract and distinguish observed evidence from an unchecked assumption.'},'hints':['Identify the exact contract condition being verified.','Compare every relevant fixture condition rather than accepting execution alone.']})
 return ix

def table(ix,cid):
 aid,tasks,variant=T[cid.split('.')[-1]]; ds=A[aid]
 # Resolve variant operations with the same shared deterministic data implementation used by the gate.
 from checkers.sandbox import resolve_dataset
 cols,rows=resolve_dataset(R,aid,variant)
 ix['public']={'asset_ref':{'asset_id':aid, 'variant_id':variant},'intro':'Fictional offline order lab, not a live deployment. Complete the supplied workspace procedure before using this table as the evidence checkpoint. '+G[cid]['practice_anchor']['objective']+' Then make the selections below; do not treat table selection alone as proof that runtime code or deployment was executed.','tasks':[]}
 ix['grading']={'answers':[],'task_feedback':{}}
 for n,(prompt,pred,column) in enumerate(tasks):
  matches=[r for r in rows if pred(r)];assert len(matches)==1,(cid,prompt,matches)
  r=matches[0]; names=[c['name'] for c in cols]; where={names[0]:r[names[0]]}
  # Use all identifier/context fields needed for an unambiguous predicate.
  if sum(all(v[k]==val for k,val in where.items()) for v in rows)>1:
   where={k:r[k] for k in names if k!=column and r[k] is not None}
  identical=[v for v in rows if all(v[k]==val for k,val in where.items())]; occurrence=identical.index(r)
  tid='task.'+str(n+1); ix['public']['tasks'].append({'task_id':tid,'prompt':prompt,'target_kind':'cell' if column else 'row'})
  answer={'task_id':tid,'row':{'where':where,'occurrence':occurrence}}
  if column:answer.update(column=column,expect_value=r[column])
  ix['grading']['answers'].append(answer);ix['grading']['task_feedback'][tid]={'correct':'This selection satisfies the stated fixture condition.','incorrect':'Check the named phase/key and contract condition; a different phase or key does not provide the requested evidence.'}

# Shared orchestration is supplied scaffolding because several glossary prose syntax descriptors are not mapped by the syntax gate.
# Learner edits are real encoding/decoding, fitted prediction, and statistics operations; none of their starter implementations passes.
def code(ix,cid):
 short=cid.split('.')[-1]
 if short=='bounded_batch_inference':
  scaffold='import pandas as pd\nimport json\n'+ 'exec('+repr(wf(cid,'frozen_package.py')+'\nclass FittedPackage:\n    def predict(self, values):\n        return model.predict(preprocessing_pipeline.transform(values))\nfitted_package = FittedPackage()\n')+')\n'
  scaffold+='contract = '+repr(contract)+'\n'
  starter=scaffold+'''# Implement these four operations. The supplied orchestration below owns bounded IO and fixture assertions.
def predict_chunk(values):
    return None
def encode_record(record):
    return None
def decode_record(text):
    return None
def normalized_keys(keys):
    return None
'''
  sol=scaffold+'''def predict_chunk(values):
    return fitted_package.predict(values)
def encode_record(record):
    import json
    return json.dumps(record)
def decode_record(text):
    import json
    return json.loads(text)
def normalized_keys(keys):
    return sorted(keys)
'''
  orchestration='''# Supplied bounded reader/writer and assertion harness; do not edit.
with open(contract['batch_input_path']) as handle:
    with open(contract['batch_output_path'], 'w') as output:
        expected_keys = []
        chunk_sizes = []
        writes_before_next_read = []
        for chunk in pd.read_csv(handle, chunksize=contract['chunk_size']):
            keys = list(chunk[contract['batch_key']])
            values = chunk[contract['feature_names']].values.tolist()
            predictions = predict_chunk(values)
            assert len(predictions) == len(keys)
            chunk_sizes.append(len(keys))
            for key, prediction in zip(keys, predictions):
                record = {contract['batch_key']: key, 'prediction': prediction, 'version': contract['version']}
                output.write(encode_record(record) + '\\n')
                expected_keys.append(key)
            output.flush()
            writes_before_next_read.append(len(keys))
with open(contract['batch_output_path']) as handle:
    decoded = [decode_record(line) for line in handle]
def supplied_assert_output(records, expected):
    keys = []
    for record in records:
        assert set(record) == {contract['batch_key'], 'prediction', 'version'}
        assert isinstance(record['prediction'], (int, float))
        assert record['version'] == contract['version']
        keys.append(record[contract['batch_key']])
    assert len(keys) == len(set(keys))
    assert normalized_keys(keys) == normalized_keys(expected)
supplied_assert_output(decoded, expected_keys)
supplied_assert_output(list(reversed(decoded)), expected_keys)
failures_detected = []
for bad in [decoded[:-1], decoded + decoded[:1], [dict(r, order_id='unknown') if i == 0 else r for i,r in enumerate(decoded)], [dict(r, prediction='malformed') if i == 0 else r for i,r in enumerate(decoded)]]:
    try:
        supplied_assert_output(bad, expected_keys)
        failures_detected.append(False)
    except AssertionError:
        failures_detected.append(True)
assert all(failures_detected)
batch_report = {'records': decoded, 'chunk_sizes': chunk_sizes, 'writes_before_next_read': writes_before_next_read, 'failures_detected': failures_detected}
'''
  # Keep scaffolding readable. Only supplied function definitions need a scaffold wrapper:
  # the gate otherwise treats unchanged function definitions as learner-authored.
  if short == 'bounded_batch_inference':
   lo=orchestration.index('def supplied_assert_output')
   hi=orchestration.index('supplied_assert_output(decoded, expected_keys)')
   orchestration=orchestration[:lo]+'exec('+repr(orchestration[lo:hi])+')\n'+orchestration[hi:]
  starter+=orchestration;sol+=orchestration; mounts=[{'asset_id':'ds.orders','mount_path':contract['batch_input_path']}];packages=['pandas']; expr='batch_report'
  prompt='Complete predict_chunk(values), encode_record(record), decode_record(text), and normalized_keys(keys). Return predictions from the supplied frozen fitted_package, JSON text for a record, decoded JSON values, and sorted keys respectively. Do not fit or update state. The supplied orchestration reads orders.csv in declared-size chunks, writes keyed JSON Lines before reading the next chunk, decodes the output, and asserts normal/final-partial acceptance and missing/duplicate/mismatched-key/malformed rejection. The output records have order_id, prediction, version. batch_report must retain records, chunk_sizes, writes_before_next_read and failures_detected exactly as supplied by the harness. Record order may differ but key alignment must not. The fixture and orchestration are scaffolding, not a completed learner function.'
 elif short=='service_telemetry':
  scaffold='import json\nimport time\nimport numpy as np\nimport pandas as pd\n'+ 'policy = '+repr(policy)+'\n'
  scaffold+='attempts = pd.read_csv("serving_attempts.csv").to_dict("records")\n'
  # Use the supplied frozen package unchanged; timing is driven by deterministic captured fixture values.
  scaffold+='exec('+repr(wf(cid,'frozen_package.py'))+')\n'
  starter=scaffold+'''# Supply JSON operations, a timing call and the required latency statistics.
def decode_request(body):
    return None
def encode_response(payload):
    return None
def clock():
    return None
def latency_mean(numeric_values):
    return None
def latency_std(numeric_values):
    return None
'''
  sol=scaffold+'''def decode_request(body):
    import json
    return json.loads(body)
def encode_response(payload):
    import json
    return json.dumps(payload)
def clock():
    import time
    return time.perf_counter()
def latency_mean(numeric_values):
    return np.mean(numeric_values)
def latency_std(numeric_values):
    return np.std(numeric_values, ddof=0)
'''
  orchestration='''# Supplied single-handler, external-probe/fault and reconciliation orchestration.
probe = [r for r in attempts if r['experiment'] == 'probe' and r['setting'] == 'baseline' and policy['probe']['t0'] <= r['request_start_seconds'] < policy['probe']['t0'] + policy['probe']['attempt_count']]
handler_events = []
handler_durations = []
original_clock = time.perf_counter
for row in probe:
    if not pd.isna(row['handler_start_seconds']):
        times = iter([row['handler_start_seconds'], row['handler_complete_seconds']])
        time.perf_counter = lambda: next(times)
        start = clock()
        payload = decode_request(json.dumps({'features': [[1.0,2.0]]}))
        try:
            if row['handler_status'] != 200:
                raise ValueError('handled error')
            result = {'predictions': model.predict(preprocessing_pipeline.transform(payload['features']))}
            encoded = encode_response(result)
            status = 200
        except ValueError:
            encoded = encode_response({'error':'ValueError'})
            status = int(row['handler_status'])
        end = clock()
        duration = end-start
        handler_durations.append(duration)
        handler_events.append({'timestamp':start, 'duration':duration, 'status':status, 'body':json.loads(encoded)})
time.perf_counter = original_clock
successful = [r for r in probe if r['http_status'] == 200 and r['valid_prediction'] and not pd.isna(r['response_complete_seconds']) and r['response_complete_seconds'] - r['request_start_seconds'] <= policy['probe']['deadline_seconds']]
external_failures = [r for r in probe if r not in successful]
absent = [r['request_id'] for r in probe if pd.isna(r['handler_start_seconds'])]
report = {'window':policy['probe']['window'], 'units':policy['units'], 'rate_per_second':policy['probe']['rate_per_second'], 'earliest_summary_time_seconds':policy['probe']['earliest_summary_time_seconds'], 'deadline_seconds':policy['probe']['deadline_seconds'], 'attempt_count':len(probe), 'successful_deadline_count':len(successful), 'availability':len(successful)/len(probe), 'error_fraction':len(external_failures)/len(probe), 'error_classification':policy['probe']['error_classification'], 'handler_count':len(handler_events), 'handler_status_counts': {str(status):sum(e['status']==status for e in handler_events) for status in sorted(set(e['status'] for e in handler_events))}, 'handler_mean':latency_mean(handler_durations), 'handler_std':latency_std(handler_durations), 'ddof':policy['ddof'], 'absent_handler_request_ids':absent, 'external_failure_request_ids':[r['request_id'] for r in external_failures], 'handler_events':handler_events}
'''
  # Keep scaffolding readable. Only supplied function definitions need a scaffold wrapper:
  # the gate otherwise treats unchanged function definitions as learner-authored.
  if short == 'bounded_batch_inference':
   lo=orchestration.index('def supplied_assert_output')
   hi=orchestration.index('supplied_assert_output(decoded, expected_keys)')
   orchestration=orchestration[:lo]+'exec('+repr(orchestration[lo:hi])+')\n'+orchestration[hi:]
  starter+=orchestration;sol+=orchestration;mounts=[{'asset_id':'ds.serving_attempts','mount_path':'serving_attempts.csv'}];packages=['numpy','pandas'];expr='report'
  prompt='Complete decode_request(body) with JSON decoding, encode_response(payload) with JSON encoding, clock() with time.perf_counter(), latency_mean(numeric_values) with np.mean, and latency_std(numeric_values) with np.std using ddof=0. The supplied synchronous handler and fault/probe harness times decoding, frozen prediction and encoding on success and handled-error paths using captured deterministic timestamps. Preserve report and its fields: window, units, rate_per_second, earliest_summary_time_seconds, deadline_seconds, attempt_count, successful_deadline_count, availability, error_fraction, error_classification, handler_count, handler_status_counts, handler_mean, handler_std, ddof, absent_handler_request_ids, external_failure_request_ids, handler_events. Keep every external attempt, including refusals and timeouts; the full final deadline must expire before summarizing. The harness classifies every non-valid/non-200/late attempt as an error and reconciles absent handler records without replacing the external denominator. Do not edit the supplied harness or claim these offline observations are production measurements.'
 else:
  scaffold='import json\nimport numpy as np\nimport pandas as pd\n'+ 'policy = '+repr(policy)+'\n'
  scaffold+='trace = pd.read_csv("batching_trace.csv").to_dict("records")\n'
  prefix='''# Supply encoder and decoder, then complete statistics on the matched durations.
'''
  matching='''# Supplied identity/setting matcher; failed and unmatched rows are excluded.
durations = {setting:[] for setting in policy['batching']['settings']}
for row in trace:
    if row['success'] and not pd.isna(row['request_start_seconds']) and not pd.isna(row['response_complete_seconds']):
        decoded = decode(encode(decode(row['response_json'])))
        if decoded['request_id'] == row['request_id'] and decoded['batching_setting'] == row['batching_setting']:
            durations[row['batching_setting']].append(row['response_complete_seconds'] - row['request_start_seconds'])
latencies_1 = durations[policy['batching']['settings'][0]]
latencies_2 = durations[policy['batching']['settings'][1]]
declared_percentile = policy['declared_percentile']
percentile_method = policy['percentile_method']
'''
  starter=scaffold+prefix+'encode = None\ndecode = None\n'+matching+'count_1 = None\ncount_2 = None\nmean_1 = None\nmean_2 = None\nstd_1 = None\nstd_2 = None\ntail_1 = None\ntail_2 = None\n'
  sol=scaffold+prefix+'import json as json\nencode = json.dumps\ndecode = json.loads\n'+matching+'''count_1 = len(latencies_1)
count_2 = len(latencies_2)
mean_1 = np.mean(latencies_1)
mean_2 = np.mean(latencies_2)
std_1 = np.std(latencies_1, ddof=0)
std_2 = np.std(latencies_2, ddof=0)
tail_1 = np.percentile(latencies_1, declared_percentile, method=percentile_method)
tail_2 = np.percentile(latencies_2, declared_percentile, method=percentile_method)
'''
  ending='''# Supplied comparison/report structure: report all feasible limits, selecting neither if none qualifies.
chosen_settings = [setting for setting,tail in zip(policy['batching']['settings'],[tail_1,tail_2]) if tail <= policy['batching']['maximum_p99_seconds']]
batching_report = {'settings':policy['batching']['settings'], 'successful_counts':[count_1,count_2], 'means':[mean_1,mean_2], 'standard_deviations':[std_1,std_2], 'tails':[tail_1,tail_2], 'percentile':declared_percentile, 'percentile_method':percentile_method, 'ddof':policy['ddof'], 'units':policy['units'], 'maximum_tail':policy['batching']['maximum_p99_seconds'], 'chosen_settings':chosen_settings, 'durations':[latencies_1,latencies_2]}
'''
  starter+=ending;sol+=ending;mounts=[{'asset_id':'ds.batching_trace','mount_path':'batching_trace.csv'}];packages=['numpy','pandas'];expr='batching_report'
  prompt='Set encode and decode to json.dumps and json.loads. The supplied matcher round-trips decoded JSON and retains only successful responses matched to request identity and setting. Complete count_1/count_2 with len, mean_1/mean_2 with np.mean, std_1/std_2 with np.std(..., ddof=0), and tail_1/tail_2 with np.percentile(..., declared_percentile, method=percentile_method), using latencies_1 and latencies_2 respectively. Those durations include batch waiting by subtracting request start from response completion in seconds. Keep batching_report fields settings, successful_counts, means, standard_deviations, tails, percentile, percentile_method, ddof, units, maximum_tail, chosen_settings, durations. The supplied final comparison lists only limits satisfying the declared maximum tail under this same successful-response population, or selects neither if none qualifies. Do not edit matching or report scaffolding.'
 ix['public']={'prompt':prompt,'runtime':{'kind':'python','version':pin,'packages':packages},'workspace':{'files':[{'path':'learner.py','role':'editable','language':'python','content':starter}], 'entry':'learner.py','asset_mounts':mounts}, 'constraints':{k:copy.deepcopy(G[cid]['practice_anchor']['live_code'][k]) for k in ['allowed_syntax','blocked_syntax']}}
 viol,unmapped,_=pysyntax.judge(sol,ix['public']['constraints']['allowed_syntax'],ix['public']['constraints']['blocked_syntax'],starter)
 assert not viol,(cid,viol)
 # Obtain expected values from the pinned Pyodide run, not from memory or hand calculations.
 problems=[];tables,_=sandbox._tables(R,mounts,{},problems);assert not problems,problems
 job=sandbox._py_job('python',packages,[sandbox._py_script('expected','learner.py',sol,sandbox._py_mounts(tables),[{'id':'result','kind':'expr','expr':expr}])])
 result=sandbox.node_run(job,sandbox.RUNTIMES['python']['runner'])['results']['expected']
 assert result['ok'],result
 expected=result['probes']['result'];assert expected['ok'],expected
 ix['grading']={'solution_files':[{'path':'learner.py','content':sol}], 'tests':[{'test_id':'test.report','kind':'value_equals','spec':{'expr':expr,'expected':expected['value'],'tolerance':1e-9},'visible':True,'message_on_fail':'Check the required operations and the complete data-derived report, including edge-case evidence.'}]}

out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for t in P['tiles']:
 authored=next(v for v in S['tiles'] if v['tile_id']==t['tile_id']);entries=[];seen=set()
 steps=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 for i,s in enumerate(steps):
  cid=s['concept_ids'][0];ix=base(s,t,'intro' if i==0 else 'stretch' if i==len(steps)-1 else 'core')
  if cid not in seen:
   rem=next((r['step_id'] for r in authored.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem
   seen.add(cid)
  if ix['type']=='choice':
   key=cid.split('.')[-1]
   if key=='model_release_rollback' and any(a.endswith('preserve_runtime_secret_boundary') for a in s['anchors']):key='rollback_secrets'
   prompt,correct,bad1,why1,bad2,why2=C[key]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':'option.a','text':correct},{'option_id':'option.b','text':bad1},{'option_id':'option.c','text':bad2}]}
   ix['grading']={'correct_option_ids':['option.a'],'option_feedback':{'option.a':{'message':'This follows the taught contract and verification procedure.'},'option.b':{'message':why1},'option.c':{'message':why2}}}
   ix['standalone']=True
   ix['feedback']['correct']['message']='This procedure satisfies the stated verification requirement.'
   ix['feedback']['hints']=['Distinguish the declared verification requirement from merely completing an action.']
  elif ix['type']=='table_select':table(ix,cid)
  elif ix['type']=='code_exercise':code(ix,cid)
  else:raise AssertionError(ix['type'])
  entries.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
