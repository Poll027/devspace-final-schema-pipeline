import json, pathlib, subprocess
B=pathlib.Path(__file__).parent
load=lambda p:json.loads(p.read_text())
P=load(B/'tile_plans.json'); S=load(B/'screens.json'); G={b['context']['concept_id']:b for b in load(B/'inputs/path_glossary_bundle.json')['bundles']}; R=load(B/'scenario_asset_registry.json'); A={a['asset_id']:a for a in R['assets']}
def file(a,p):return next(f['content'] for f in A[a]['files'] if f['path']==p)
C=json.loads(file('ws.prediction_schema_validation','contract.json')); RT=json.loads(file('ws.prediction_schema_validation','runtime_contract.json')); M=json.loads(file('ws.service_telemetry','measurement_policy.json'))
def rows(a):return [dict(zip([c['name'] for c in A[a]['columns']],r)) for r in A[a]['rows']]
release=rows('ds.release_records'); approved=next(r for r in release if r['approved']); faulty=next(r for r in release if not r['approved'])
rem={}
for t in S['tiles']:
 for r in t.get('remediation_steps',[]):
  for c in r['concept_ids']:rem.setdefault(c, []).append(r['step_id'])
rem_used={}
# Each wrong option is an authored misconception, not a second valid solution.
Q={
'prediction_schema_validation':('A client must check successful and rejected JSON fixtures. Which sequence implements the declared exchange and assertions?', [('Serialize and encode the request; POST with application/json and an explicit timeout; decode the response and assert each fixture outcome.',True,'Encoding precedes transport; decoding precedes structured checks, and assertions verify outcomes.'),('Send a Python dictionary directly as the request body and inspect raw response text as if it were decoded fields.',False,'The JSON exchange requires encoded bytes and decoded structured values, not an unencoded dictionary or raw text.'),('Send encoded JSON correctly but skip failure assertions whenever the valid fixture passes.',False,'A passing valid fixture does not verify the declared rejection cases; each case needs its assertion.')]),
'online_prediction_contract':('For this bounded standard-library fixture, which runtime plan respects the stated scope?', [('Construct HTTPServer with the configured host, port and Handler, then serve_forever on the existing authorized fixture runtime; do not claim production-server suitability.',True,'The supplied HTTPServer fixture is bounded, and http.server is not recommended as a production server.'),('Treat a successful HTTPServer fixture run as proof that http.server is recommended for production serving.',False,'The glossary explicitly limits this implementation to a bounded fixture, not a production recommendation.'),('Omit the declared Handler when constructing HTTPServer because the host and port identify the prediction logic.',False,'HTTPServer must be constructed with the declared Handler as well as the configured host and port.')]),
'bounded_batch_inference':('The valid batch fixture passes. Which assertion plan also verifies the declared boundary and failure cases?', [('Assert the expected predicate for every valid, boundary and failure fixture during ordinary non-optimized execution.',True,'Each declared case needs its predicate; a false assertion raises AssertionError in ordinary execution.'),('Assert only the valid case and mark all failure fixtures verified without running their predicates.',False,'Valid-case success does not establish the separate boundary and failure predicates.'),('Catch every AssertionError and record every fixture as passing regardless of its expected result.',False,'A false predicate is a failed check, not evidence of universal success.')]),
'model_service_readiness':('After starting the referenced image with the declared name, published port and nonsecret environment, what evidence is still required to inspect that container?', [('Inspect the named container image identity and State, and inspect its captured logs for initialization or execution failures.',True,'Run settings do not replace inspection of image/State and captured logs.'),('Accept the docker run command alone as evidence of the observed image identity, State and absence of logged failures.',False,'The run command supplies settings; inspect and logs provide the required observations.'),('Read logs but skip container inspection because output proves the intended image and State.',False,'Logs do not replace the explicit image-identity and State inspection.')]),
'deployment_configuration_code':('The deployment configuration has been verified. Which repository sequence follows the existing workflow?', [('Create the configuration branch with git checkout -b BRANCH, commit the verified configuration and merge that branch under the existing workflow.',True,'The verified configuration is committed on the named branch and merged under the supplied workflow.'),('Create a branch but never commit or merge the verified configuration.',False,'Branch creation alone omits the required commit and merge.'),('Merge a branch containing no committed verified configuration and count the local uncommitted file as the merged result.',False,'The required committed configuration must be the one merged; an uncommitted local file does not meet that sequence.')]),
'deployment_verification':('Which acceptance rule is defensible for the supplied release fixture?', [('Accept only after recorded artifact/configuration match inspection, readiness passes and assertions verify the declared output shape/values and each valid, boundary and malformed outcome.',True,'Acceptance combines identity, runtime, readiness and explicit fixture checks.'),('Accept as soon as deployment starts, without matching the observed artifact or checking endpoint contracts.',False,'Startup alone is not verification of the recorded release or its endpoint contracts.'),('Accept when readiness passes even if a required prediction assertion fails.',False,'Readiness does not replace the required output and fixture assertions.')]),
'prediction_authentication':('A denied prediction request must be visible in the evidence record. Which log entry respects the declared disclosure boundary?', [('Record the denial/failure class without the credential or protected request values.',True,'Failure visibility must not disclose credentials or protected values.'),('Record the denial together with the complete credential to make the rejection easy to reproduce.',False,'Disclosure of the credential violates the log boundary even when the denial is visible.'),('Suppress every denial record to avoid disclosing secrets.',False,'The task requires visible failure evidence without sensitive values, not silence.')]),
'service_telemetry':('Some external probe attempts never reach the handler. How should availability be reported for the prescribed probe?', [('Keep all 300 attempts in the denominator, count only valid HTTP 200 predictions received within the deadline, and reconcile absent handler records with external failures.',True,'External failures remain attempts; handler counts cannot replace the denominator.'),('Drop attempts with no handler record and divide by the remaining handler count.',False,'Connection refusals and response timeouts remain in the prescribed 300-attempt denominator.'),('Use the handler error count alone as the availability fraction without examining external outcomes.',False,'Availability requires external deadline/validity outcomes and reconciliation, not handler errors alone.')]),
'prediction_load_test':('Which traffic plan measures capacity for the declared valid workload rather than mixing contract-rejection checks into it?', [('Run intentional malformed fixtures separately; measure the stated valid payload mix with explicit offered rates, arrival/concurrency profile, warm-up and duration.',True,'The workload and measurement profile must be declared; rejection checks remain separate.'),('Mix intentional malformed fixtures into capacity traffic and count their expected rejections as valid-workload serving failures.',False,'Intentional contract-rejection tests are separate from the valid traffic used for capacity measurements.'),('Declare an offered rate but leave payload validity, arrival/concurrency profile and measurement window unspecified.',False,'Rate alone does not define the representative valid workload and its measurement conditions.')]),
'inference_batching_decision':('Which comparison supports choosing a supplied batching limit against its tail-latency objective?', [('Match successful decoded responses by identity and setting, use completion minus request start including waiting, and compare the declared percentile on the same population and unit.',True,'Matching, end-to-end duration and a common percentile convention are all required.'),('Subtract batch-wait-end from completion and compare it with the end-to-end latency objective.',False,'That duration omits batch waiting and changes the latency interpretation.'),('Include failed and unmatched responses in one setting but only matched successes in the other.',False,'Different response populations do not support the required like-for-like comparison.')]),
'serving_worker_concurrency':('The safe-reloaded and resolved YAML contains the approved worker limit. Which next action applies the bound?', [('Apply the referenced configuration with docker compose -f CONFIG_PATH up -d and inspect the resulting runtime under that worker limit.',True,'The validated worker setting must be applied to the referenced runtime, then inspected.'),('Apply a different configuration file whose worker setting has not been checked.',False,'A checked limit in one file does not validate the file actually applied.'),('Treat YAML parsing alone as proof that the referenced runtime is running under the bound.',False,'Parsing is not application or runtime inspection.')]),
'serving_replica_scaling':('After the authorized bounded scaling and lifecycle check, which evidence completes the exercise?', [('Inspect actual container count/identities and instance identity/status around the actions, then restore and verify the original replica and lifecycle settings.',True,'Observed scaling and instance state must be checked, and the original nonproduction settings restored.'),('Leave changed settings active because the changed count was observed once.',False,'The exercise explicitly requires restoring original replica and lifecycle settings.'),('Restore a replica number in YAML but skip observed container and instance checks.',False,'A written setting alone does not verify observed identities, counts or lifecycle state.')]),
'rollback_target':('The supplied record approves version A as the previous release; version B is the faulty unapproved test release. Which target preserves rollback identity?', [('Select the recorded approved version A and its recorded immutable image reference.',True,'Rollback resolves the approved registry version and its immutable artifact.'),('Select an unapproved latest tag because it is newer than the previous release.',False,'Latest does not preserve previous approval/version identity, and a mutable tag is not the recorded immutable reference.'),('Keep the A label but start an unrelated image reference.',False,'The approved version and its recorded artifact identity must remain paired.')]),
'rollback_secret':('Which release configuration keeps sensitive values within the runtime secret boundary?', [('Reference the supplied runtime secret mechanism and never embed the credential literal in Compose or Dockerfile ARG/ENV.',True,'Runtime secret references preserve the boundary; credential literals must not persist in configuration or image metadata.'),('Put the credential literal in Dockerfile ENV because the container needs it later.',False,'Dockerfile ARG/ENV secret literals persist in the image or metadata.'),('Write the credential literal into Compose and call it a secret reference.',False,'Renaming a literal does not make it a runtime secret reference.')])
}
# Inspection excerpts are authored in the interaction. No asset_ref/source is needed for this profile override.

# Metric excerpts are computed from the registered attempts/backlog, never hand-entered.
def measured_evidence(experiment):
 import statistics, math
 policy=M['load' if experiment=='load' else 'scaling']
 duration=policy['measurement_seconds']
 attempts=rows('ds.serving_attempts'); backlog=rows('ds.backlog')
 settings=sorted({r['setting'] for r in attempts if r['experiment']==experiment})
 reports={}; qualifying=[]
 for setting in settings:
  subset=[r for r in attempts if r['experiment']==experiment and r['setting']==setting]
  successful=[r for r in subset if r['outcome']=='success' and r['http_status']==C['success_status'] and r['valid_prediction']]
  lat=sorted(r['response_complete_seconds']-r['request_start_seconds'] for r in successful)
  q=(len(lat)-1)*M['declared_percentile']/100
  lo=math.floor(q) if lat else None
  p99=lat[lo]+(q-lo)*(lat[min(lo+1,len(lat)-1)]-lat[lo]) if lat else None
  series=sorted([r for r in backlog if r['experiment']==experiment and r['setting']==setting],key=lambda r:r['elapsed_seconds'])
  increasing=all(b['unfinished_requests']>=a['unfinished_requests'] for a,b in zip(series,series[1:])) and series[-1]['unfinished_requests']>series[0]['unfinished_requests']
  record={'attempts':len(subset),'completed_successes':len(successful),'successful_throughput_per_second':len(successful)/duration,'success_probability':len(successful)/len(subset),'failed_fraction':1-len(successful)/len(subset),'mean_seconds':statistics.mean(lat) if lat else None,'std_seconds_ddof0':statistics.pstdev(lat) if lat else None,'p99_seconds':p99,'successful_latency_count':len(lat),'percentile_method':M['percentile_method'],'backlog_samples':[{'elapsed_seconds':r['elapsed_seconds'],'unfinished_requests':r['unfinished_requests']} for r in series],'increasing_backlog':increasing}
  if experiment=='load':
   record['offered_rate_per_second']=len(subset)/duration
   feasible=record['success_probability']>=policy['minimum_success_probability'] and record['failed_fraction']<=policy['maximum_failed_fraction'] and p99 is not None and p99<=policy['maximum_p99_seconds'] and record['successful_throughput_per_second']>=policy['minimum_successful_throughput_per_second'] and series[-1]['unfinished_requests']==0 and all(b['unfinished_requests']<=a['unfinished_requests'] for a,b in zip(series,series[1:]))
  else:
   record['offered_rate_per_second']=policy['offered_rate']
   feasible=record['success_probability']>=policy['minimum_success_probability'] and p99 is not None and p99<=policy['maximum_p99_seconds'] and record['successful_throughput_per_second']>=policy['minimum_successful_throughput_per_second']
  record['meets_all_declared_criteria']=feasible
  reports[setting]=record
  if feasible:qualifying.append(setting)
 if experiment=='load':selected=max(qualifying,key=lambda x:reports[x]['offered_rate_per_second']) if qualifying else None
 else:selected=qualifying
 return json.dumps({'measurement_seconds':duration,'latency_population':'completed successful responses (timeouts excluded)','failed_population':'every non-successful eligible attempt','requirements':policy,'measurements':reports,'selected':selected,'verdict':'bounded tested evidence only, no unmeasured setting claim'},indent=2)

def inspect(cid):
 k=cid.split('.')[-1]; good=[]; bad=[]
 if k=='prediction_schema_validation':
  req=C['expected_request']; resp=C['expected_response']; boundary={'features':[[C['feature_max'],C['feature_min']]]}
  good=[('Transport and validation fragment', 'body = json.dumps(payload).encode("utf-8")\nrequest = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")\nwith urllib.request.urlopen(request, timeout=timeout_seconds) as response:\n    decoded = json.loads(response.read().decode("utf-8"))\nassert set(decoded) == set(response_keys)\nassert len(decoded["predictions"]) == len(payload["features"])'),('Accepted fixtures',json.dumps({'valid_request':req,'valid_response':resp,'included_boundary_request':boundary,'checks':['decode JSON; required keys and declared value types','NumPy declared dtype; rank 2, width 2','all values in inclusive declared limits','one prediction per request row'],'assertions':'valid and included-boundary acceptance confirmed'}))]
  bad=[('Missing-key fixture','Decoded request = {}\nrequired keys = '+repr(C['request_keys'])+'\nvalidator returns success without checking required keys.'),('Out-of-range fixture','Decoded request = '+json.dumps({'features':[[C['feature_max']+1,C['feature_min']]]})+'\nValidator accepts despite the declared inclusive range '+repr([C['feature_min'],C['feature_max']])),('Wrong-width and wrong-type fixtures','Decoded features = [[1, 2, 3]]; required width = '+str(C['matrix_width'])+'\nSecond decoded fixture: features = "not a matrix"\nBoth are marked accepted without rank/type/width checks.'),('Misaligned response','Request = '+json.dumps(req)+'\nDecoded response = '+json.dumps({'predictions':resp['predictions'][:-1],'version':resp['version']})+'\nClient records the response-alignment assertion as passing.'),('Malformed JSON handling','json.loads raises a decoding error. Client treats it as successful acceptance instead of explicit rejection.')]
 elif k=='online_prediction_contract':
  good=[('Bounded handler path','class Handler(BaseHTTPRequestHandler):\n    def do_POST(self):\n        # Declared route has already been checked by supplied scaffolding.\n        size = int(self.headers["Content-Length"])\n        payload = json.loads(self.rfile.read(size).decode("utf-8"))\n        values = validate_request(payload)\n        predictions = model.predict(preprocessing_pipeline.transform(values))\n        body = json.dumps({"predictions": predictions, "version": version}).encode("utf-8")\n        self.send_response(success_status)\n        self.send_header("Content-Type", "application/json")\n        self.send_header("Content-Length", str(len(body)))\n        self.end_headers()\n        self.wfile.write(body)'),('Fixture assertion record','Repeated identical valid requests: equal predictions. No fit or state update executed. Included boundary accepted; malformed requests explicitly rejected. Decoded fields, HTTP status and actual UTF-8 body headers all match the declared contract; ordinary assertions pass.')]
  bad=[('Request-time state update','After validation, the handler calls preprocessing_pipeline.fit(values) and model.fit(values) before each prediction. It claims stable frozen-state inference.'),('Body-length mismatch','body = json.dumps(response_dict).encode("utf-8")\nself.send_header("Content-Length", "1")\n# body contains multiple bytes\nself.end_headers()\nself.wfile.write(body)')]
 elif k=='model_service_readiness':
  good=[('Readiness branches','GET '+C['readiness_route']+' returns '+str(C['not_ready_status'])+' and '+json.dumps(C['not_ready_payload'])+' while neither object or either fitted object is unavailable, or initialization failed. Only both initialized AND usable returns '+str(C['success_status'])+' and '+json.dumps(C['ready_payload'])+'. Ordinary assertions check status and decoded state in every case.'),('Container inspection evidence',json.dumps({'image':RT['IMAGE_DIGEST'],'State':{'Running':True,'Health':{'Status':'healthy'}},'healthcheck':C['healthcheck'],'sanitized_logs':'both fitted objects initialized; no initialization or execution failures','comparison':'image and State match named fixture; observed Health agrees with ready fixture'}))]
  bad=[('Premature readiness','model_initialized = True\npreprocessor_initialized = False\nGET '+C['readiness_route']+' returns '+str(C['success_status'])+' and '+json.dumps(C['ready_payload'])+' because the process is running.'),('Healthcheck mismatch','The runtime contract specifies '+json.dumps(C['healthcheck'])+'. The applied healthcheck probes an unrelated route and uses no stated timeout. Evidence treats running State alone as Health success.')]
 elif k=='deployment_configuration_code':
  cfg={'services':{RT['SERVICE']:{'image':RT['IMAGE_DIGEST'],'environment':{RT['SETTING']:RT['VALUE']},'ports':[str(RT['HOST_PORT'])+':'+str(RT['CONTAINER_PORT'])],'secrets':[RT['secret_reference']],'deploy':{'replicas':RT['REPLICA_COUNT'],'resources':{'limits':RT['supported_resource_limits']}}}},'secrets':{RT['secret_reference']:{'environment':RT['secret_environment_variable']}}}
  good=[('Configuration fragment',json.dumps(cfg,indent=2)+'\nWritten with yaml.safe_dump; reloaded with yaml.safe_load. Compose config resolves these exact fields; resource fields are supported by this fixture runtime. No secret literal is present.'),('Recreation evidence','Authorized instance '+RT['INSTANCE']+' in '+RT['ZONE']+': describe before RUNNING; authorized stop operation awaited then describe TERMINATED; start awaited then describe RUNNING; ssh to the running authorized instance. Commit verified branch '+RT['BRANCH']+' and merge under existing workflow. Initial and recreated deployments use '+RT['IMAGE_DIGEST']+' and the same resolved ports/environment/replicas/resources. Only test Compose deployment was destroyed then reapplied. Container running state and credential-safe logs inspected; no failures or sensitive values. Reproducible-deployment verdict: accept.')]
  bad=[('Mutable recreation','Initial image = recorded immutable digest. Recreated image = fixture.local/orders:latest. No comparison with recorded artifact. Verdict: identical reproducible release.'),('Credential persistence','Dockerfile ARG contains a credential literal; Compose environment contains the same literal. Evidence calls these runtime secret references.')]
 elif k=='deployment_verification':
  good=[('Acceptance evidence','Container image '+RT['IMAGE_DIGEST']+' and named runtime configuration match record. State Running=true; Health healthy where configured. Sanitized logs contain no initialization/execution failures. GET '+C['readiness_route']+' within '+str(C['timeout_seconds'])+' seconds: '+str(C['success_status'])+' '+json.dumps(C['ready_payload'])+'. POST encoded JSON with application/json and same explicit timeout; decode response '+json.dumps(C['expected_response'])+'. Ordinary assertions verify valid and included-boundary shape/values; malformed fixture receives '+str(C['schema_rejection_status'])+'. Verdict: accept.')]
  bad=[('Wrong artifact','Container Running=true and readiness passes, but observed image is the faulty test artifact '+faulty['image_reference']+' rather than recorded '+approved['image_reference']+'. Verdict: accept.'),('Unverified boundary and error cases','The valid request returns expected predictions. Boundary and malformed fixtures were not run; endpoint calls omit timeouts. Verdict: accept complete verification.')]
 elif k=='prediction_authentication':
  good=[('Credential/config evidence','Safe-reloaded and Compose-resolved service '+RT['SERVICE']+' keeps image '+RT['IMAGE_DIGEST']+', declared ports and nonsecret authentication settings. Credential is referenced by secret '+RT['secret_reference']+' from runtime variable '+RT['secret_environment_variable']+' and granted only to prediction. Applied service inspection matches configuration; no literal credential.'),('Verifier and request evidence','claims = id_token.verify_oauth2_token(credential, requests.Request(), expected_audience)\nif claims["sub"] not in permitted_subjects:\n    raise PermissionError("prediction denied")\n# expected_audience and permitted_subjects are supplied policy values.\n# Missing credential, invalid credential, GoogleAuthError, and valid identity with unpermitted subject are explicitly denied.\n# Authorized identity receives valid prediction; missing/invalid/unpermitted identities receive declared denial.\n# Logs show failure class only, never credential or protected request values.')]
  bad=[('Identity-only authorization','Token verifier validates the declared audience and returns a valid subject not in permitted_subjects. authorize_prediction returns success without the subject policy check.'),('Audience bypass','Token is decoded but not verified against expected_audience. Endpoint accepts its subject as authenticated and permits prediction.'),('Disclosure on denial','Denied requests are logged with the complete credential and protected feature values, described as safe failure visibility.')]
 elif k=='prediction_load_test':
  good=[('Bounded workload setup','Inspect named image '+RT['IMAGE_DIGEST']+' with declared published port and nonsecret settings: Running=true; captured logs inspected without failures. Separate ordinary assertions accept valid and boundary JSON fixtures and reject malformed fixtures. Capacity driver uses '+json.dumps(M['load'])+'; all rate windows use the same valid payload mix and stated arrival/concurrency controls.'),('Measurement/report code','For each offered rate: retain attempted requests and all success/error/timeout outcomes. success_probability = completed_successes / attempted_requests; failed_fraction = all_failed_attempts / attempted_requests. Successful throughput = completed_successes / measurement_seconds; report offered rate separately. Latencies = response completion minus request start, seconds, successful completed responses only. Report sample count, np.mean, np.std(ddof=0), p99 with linear convention. Inspect unfinished requests throughout and at the end. Select only tested rates satisfying every predeclared probability/error/p99/throughput/backlog requirement; report the highest tested qualifying rate, not an unmeasured production claim.')]
  bad=[('False throughput','All arrival attempts are divided by the window duration and labeled successful throughput, even when several fail or time out.'),('Backlog ignored','End unfinished requests are positive and intermediate samples increase. The rate is marked feasible solely because average latency is small.')]
 elif k=='serving_worker_concurrency':
  good=[('Applied configuration','yaml.safe_dump then yaml.safe_load preserve service '+RT['SERVICE']+', immutable image '+RT['IMAGE_DIGEST']+', ports and nonsecret environment. Resolved Compose config confirms '+RT['worker_limit_key']+'='+str(RT['approved_worker_limit'])+'. Apply same configuration with compose up -d and inspect resulting containers.'),('Same-interval runtime evidence','docker container top '+RT['NAME']+' identifies one supervisor and '+str(RT['approved_worker_limit'])+' prediction workers in interval within_limit. Only prediction workers count toward limit. Concurrent CPU/memory samples from interval within_limit are retained. Observed prediction worker count equals approved limit: within bound.')]
  bad=[('Oversubscription trap','Resolved YAML limit = '+str(RT['approved_worker_limit'])+'. Same load interval shows '+str(RT['approved_worker_limit']+1)+' prediction workers, plus a supervisor. CPU/memory samples are concurrent. Verdict says bound honored because Compose config validated.'),('Nonconcurrent resource evidence','Worker processes observed during load interval X, but resource samples are idle-period Y. Record claims CPU/memory evidence from the same fixture interval.')]
 elif k=='serving_replica_scaling':
  good=[('Demand/capacity verdict','At the same declared offered load, use all eligible attempts for success probability, all completed successful latencies for p99 (linear, seconds, count stated), completed successes / measurement seconds for throughput, np.mean and np.std(ddof=0). Choose only a supplied setting satisfying all '+json.dumps(M['scaling'])+' requirements; do not infer a benefit from replica count alone.'),('Bounded settings and restoration','Safe YAML round trip and resolved fields preserve approved immutable image and runtime settings. Fixed Compose count or supported scale action is checked against actual container counts/identities before and after bounded demand. Supplied scalable target uses explicit MinCapacity/MaxCapacity '+json.dumps(RT['replica_bounds'])+' and supplied metric/target/cooldowns only. Authorized describe '+RT['INSTANCE']+' --zone='+RT['ZONE']+' records identity/status before and after the lifecycle action. Restore original '+str(RT['original_replica_count'])+' replica and '+RT['original_instance_status']+' lifecycle state, inspect restored identities/count and retain evidence.')]
  bad=[('More-is-always-better trap','Choose the largest supplied replica count even though its measured p99 fails the stated objective at the same offered load.'),('No restoration','Changed replica and instance settings remain active after the bounded check; report calls written YAML a restoration without inspecting restored runtime state.')]
 elif k=='model_release_rollback':
  good=[('Verified transition','B initially remains running. Start '+approved['container_name']+' from approved '+approved['image_reference']+' with required nonsecret environment, runtime-injected secret and distinct published host port '+str(approved['host_port'])+'. Inspect intended identity, Running State and Health where configured; sanitized logs show no initialization/execution failure. GET readiness within '+str(C['timeout_seconds'])+' seconds checks status and decoded state; POST encoded JSON with application/json and same timeout checks decoded version '+approved['version']+' and predictions '+json.dumps(C['expected_response']['predictions'])+'. Only after both verification checks pass: stop and remove '+faulty['container_name']+'. Approved A remains running; evidence contains no credentials or sensitive request data.')]
  bad=[('Early retirement','Stop and remove '+faulty['container_name']+' before checking replacement readiness or prediction/version response. Then start A and assume it is ready.'),('Wrong replacement identity','Launch the A container name but use faulty B artifact '+faulty['image_reference']+'. Prediction response confirms version B. Verdict says approved A restored.'),('Secret leak','Release configuration embeds credential literal in Dockerfile ENV; evidence includes protected request values. Runtime secret injection is bypassed.')]
 if k=='prediction_load_test':good.append(('Computed capacity record',measured_evidence('load')))
 if k=='serving_replica_scaling':
  good.append(('Computed same-load decision record',measured_evidence('scaling')))
  bad[0]=('More-is-always-better trap','Choose the largest supplied replica count without regard to its measured timeout fraction, absent successful latency sample and unfinished-request evidence. More replicas alone prove it meets every objective.')
 if k=='prediction_schema_validation':bad.append(('Wrong-rank acceptance','Decoded features is a flat one-dimensional vector rather than the declared rank-two matrix. Validator accepts without checking rank.'))
 return [('Meets declared practice',good),('Violates declared practice',bad)]

def feedback(cid):
 return {'correct':{'message':'The judgement follows the declared contract and the required evidence.'},'incorrect':{'message':'Recheck each required predicate and the observation it must verify; do not replace evidence with configuration or a partial passing case.'},'hints':['Separate the supplied intention from what the excerpt actually checks.','Compare every outcome with the declared success criteria.']}

code_jobs=[]
def code(cid,ix):
 k=cid.split('.')[-1]; mounts=[]
 constraints={x:G[cid]['practice_anchor']['live_code'][x] for x in ['allowed_syntax','blocked_syntax']}
 if k=='bounded_batch_inference':
  mounts=[{'asset_id':'ds.orders','mount_path':C['batch_input_path']}]
  # Frozen package and fixture runner are supplied infrastructure. Learner owns batching, serialization and key checks.
  scaffold='import pandas as pd\nimport json\n'+file('ws.bounded_batch_inference','frozen_package.py')+'\nclass FittedPackage:\n    def predict(self, values):\n        return model.predict(preprocessing_pipeline.transform(values.values.tolist()))\nfitted_package = FittedPackage()\n'
  scaffold+='input_path = '+repr(C['batch_input_path'])+'\noutput_path = '+repr(C['batch_output_path'])+'\ndeclared_rows = '+repr(C['chunk_size'])+'\nfeature_names = '+repr(C['feature_names'])+'\nresult_keys = '+repr(C['batch_result_keys'])+'\nversion = '+repr(C['version'])+'\n'
  starter_fun='def validate_records(records, expected_records):\n    # TODO: schema, key uniqueness and keyed prediction checks\n    return False\n\ndef run_batch():\n    # TODO: bounded reader; write each chunk before next read; decode output\n    return []\n'
  sol_fun='''def validate_records(records, expected_records):
    assert len(records) == len(expected_records)
    actual_keys = []
    expected_keys = []
    for record in records:
        assert set(record) == set(result_keys)
        actual_keys.append(record["order_id"])
        matches = []
        for expected in expected_records:
            if record["order_id"] == expected["order_id"]:
                matches.append(expected)
        assert len(matches) == 1
        assert record == matches[0]
    for expected in expected_records:
        expected_keys.append(expected["order_id"])
    assert len(set(actual_keys)) == len(actual_keys)
    assert sorted(actual_keys) == sorted(expected_keys)
    return True

def run_batch():
    decoded = []
    expected_records = []
    with open(input_path) as input_handle:
        with open(output_path, "w") as output_handle:
            for chunk in pd.read_csv(input_handle, chunksize=declared_rows):
                predictions = fitted_package.predict(chunk[feature_names])
                for key, prediction in zip(chunk["order_id"], predictions):
                    record = {"order_id": key, "prediction": prediction, "version": version}
                    expected_records.append(record)
                    output_handle.write(json.dumps(record) + "\\n")
    with open(output_path) as input_handle:
        for line in input_handle:
            decoded.append(json.loads(line))
    assert validate_records(decoded, expected_records)
    return decoded
'''
  # Supplied harness produces malformed keyed fixtures from actual output, not precomputed answers.
  tail='''records = run_batch()
def exercise_validation():
    checks = []
    fixtures = [records[::-1], records[:-1], records + records[:1], [{**r, "order_id": "unknown"} if i == 0 else r for i, r in enumerate(records)], [{"order_id": r["order_id"]} for r in records], [{**r, "prediction": r["prediction"] + 1} if i == 0 else r for i, r in enumerate(records)]]
    for fixture in fixtures:
        try:
            checks.append(validate_records(fixture, records))
        except AssertionError:
            checks.append(False)
    return {"records": records, "validation_results": checks}
batch_report = exercise_validation()
'''
  starter=scaffold+starter_fun+tail;solution=scaffold+sol_fun+tail
  exprs=['batch_report']
  prompt='Complete run_batch and validate_records; leave the supplied frozen package and fixture runner unchanged. Read orders.csv with the declared chunk size (two for the five-order fixture), preserve order_id, call fitted_package.predict on feature_names without refitting, and write each chunk before reading the next. Write JSON lines to learner_results.jsonl with exactly order_id, prediction, version, then decode them and validate one correct record per eligible input key independent of ordering. validate_records returns True or raises AssertionError for wrong schema, missing/duplicate/mismatched keys or predictions. run_batch returns decoded records. The supplied batch_report grades records and validation_results for reordered-valid, missing, duplicate, mismatched-key, malformed-schema and wrong-prediction fixtures in that order. The final partial chunk must be processed.'
  packages=['pandas']
 elif k=='inference_batching_decision':
  mounts=[{'asset_id':'ds.batching_trace','mount_path':'batching_trace.csv'}]
  scaffold='import json\nimport numpy as np\nimport csv\nwith open("batching_trace.csv") as handle:\n    raw_rows = list(csv.DictReader(handle))\ntrace = [{"request_id": r["request_id"], "batching_setting": r["batching_setting"], "request_start_seconds": float(r["request_start_seconds"]) if r["request_start_seconds"] else None, "response_complete_seconds": float(r["response_complete_seconds"]) if r["response_complete_seconds"] else None, "success": r["success"].lower() == "true", "response_json": r["response_json"]} for r in raw_rows]\n'
  scaffold+='settings = '+repr(M['batching']['settings'])+'\ndeclared_percentile = '+repr(M['declared_percentile'])+'\npercentile_method = '+repr(M['percentile_method'])+'\nlatency_objective = '+repr(M['batching']['maximum_p99_seconds'])+'\nunits = '+repr(M['units'])+'\ndivisor = '+repr(M['ddof'])+'\n'
  starter=scaffold+'# TODO: encode/decode trace; match responses; summarize and select\nreport = {}\nselected = []\n'
  solution=scaffold+'''encoded_trace = json.dumps(trace)
decoded_trace = json.loads(encoded_trace)
report = {}
selected = []
for setting in settings:
    latencies = []
    for row in decoded_trace:
        if row["batching_setting"] == setting and row["success"] and row["request_start_seconds"] is not None and row["response_complete_seconds"] is not None:
            response = json.loads(row["response_json"])
            if response["request_id"] == row["request_id"] and response["batching_setting"] == setting:
                latencies.append(row["response_complete_seconds"] - row["request_start_seconds"])
    numeric_values = np.array(latencies)
    mean = np.mean(numeric_values)
    std = np.std(numeric_values, ddof=0)
    tail = np.percentile(numeric_values, declared_percentile, method=percentile_method)
    report[setting] = {"count": len(latencies), "mean": mean, "std": std, "p99": tail, "units": units, "ddof": divisor, "percentile_method": percentile_method}
    if tail <= latency_objective:
        selected.append(setting)
'''
  exprs=['report','selected']
  packages=['numpy']
  prompt='Leave the supplied CSV loader and policy values unchanged. Encode trace with json.dumps and decode it with json.loads. Decode each response_json and include only successful responses matching both request_id and batching_setting with supplied request-start and response-completion times. Exclude a response lacking a request-start trace as unmatched. Compute end-to-end seconds as response_complete_seconds minus request_start_seconds (including batch waiting). For each supplied setting, create report[setting] with exactly count, mean, std, p99, units, ddof, percentile_method. Use arithmetic mean, population np.std(..., ddof=0) and np.percentile with declared_percentile and percentile_method (linear). Set selected to the supplied settings meeting p99 <= latency_objective, in settings order; use [] if none qualify. Do not include failed or unmatched responses.'
 else:
  mounts=[{'asset_id':'ds.serving_attempts','mount_path':'serving_attempts.csv'}]
  scaffold='import json\nimport time\nimport numpy as np\nimport csv\nwith open("serving_attempts.csv") as handle:\n    raw_rows = list(csv.DictReader(handle))\n'
  scaffold+='attempts = [{"request_id": r["request_id"], "request_start_seconds": float(r["request_start_seconds"]) if r["request_start_seconds"] else None, "response_complete_seconds": float(r["response_complete_seconds"]) if r["response_complete_seconds"] else None, "http_status": int(r["http_status"]) if r["http_status"] else None, "valid_prediction": r["valid_prediction"].lower() == "true", "handler_start_seconds": float(r["handler_start_seconds"]) if r["handler_start_seconds"] else None, "handler_complete_seconds": float(r["handler_complete_seconds"]) if r["handler_complete_seconds"] else None, "handler_status": int(r["handler_status"]) if r["handler_status"] else None, "outcome": r["outcome"]} for r in raw_rows if r["experiment"] == "probe"]\n'
  scaffold+='deadline_seconds = '+repr(M['probe']['deadline_seconds'])+'\nwindow_start = '+repr(M['probe']['t0'])+'\nwindow_seconds = '+repr(M['probe']['attempt_count'])+'\nsummary_time = '+repr(M['probe']['earliest_summary_time_seconds'])+'\nerror_classification = '+repr(M['probe']['error_classification'])+'\nunits = '+repr(M['units'])+'\n'
  # Deterministic virtual clock/fault helpers replay registry handler boundaries. No sleeps/network required.
  scaffold+='''telemetry = []
current_attempt = None
clock_phase = 0
def timestamp():
    global clock_phase
    result = current_attempt["handler_start_seconds"] if clock_phase == 0 else current_attempt["handler_complete_seconds"]
    clock_phase += 1
    return result
def supplied_predict(payload):
    if current_attempt["handler_status"] != 200:
        raise ValueError("supplied handled prediction error")
    return {"predictions": [sum(row) for row in payload["features"]], "version": "A"}
def record_telemetry(start, finish, status):
    telemetry.append({"request_id": current_attempt["request_id"], "timestamp": start, "duration": finish - start, "status": status})
def run_supplied_probe(handler):
    global current_attempt, clock_phase
    for attempt in attempts:
        if attempt["handler_start_seconds"] is not None:
            current_attempt = attempt
            clock_phase = 0
            handler(json.dumps({"features": [[1.0, 2.0]]}))
    return attempts
'''
  starter=scaffold+'''def instrumented_handler(body):
    # TODO: timing encompasses decode, prediction, encode; record both paths
    return "{}"
external = run_supplied_probe(instrumented_handler)
# TODO: preserve external denominator and reconcile handler evidence
report = {}
'''
  solution=scaffold+'''def instrumented_handler(body):
    start = timestamp()
    status = 200
    try:
        payload = json.loads(body)
        response = supplied_predict(payload)
        encoded = json.dumps(response)
    except ValueError:
        status = 500
        encoded = json.dumps({"error": "prediction failure"})
    finally:
        finish = timestamp()
        record_telemetry(start, finish, status)
    return encoded
external = run_supplied_probe(instrumented_handler)
successes = 0
absent = []
external_failures = {}
for attempt in external:
    if attempt["http_status"] == 200 and attempt["valid_prediction"] and attempt["response_complete_seconds"] is not None and attempt["response_complete_seconds"] - attempt["request_start_seconds"] <= deadline_seconds:
        successes = successes + 1
    else:
        outcome = attempt["outcome"]
        if outcome not in external_failures:
            external_failures[outcome] = 0
        external_failures[outcome] = external_failures[outcome] + 1
    if attempt["handler_start_seconds"] is None:
        absent.append({"request_id": attempt["request_id"], "outcome": attempt["outcome"]})
status_counts = {}
handler_errors = 0
numeric_values = []
for record in telemetry:
    status = record["status"]
    if status not in status_counts:
        status_counts[status] = 0
    status_counts[status] = status_counts[status] + 1
    if status != 200:
        handler_errors = handler_errors + 1
    numeric_values.append(record["duration"])
report = {"window": [window_start, window_start + window_seconds], "summary_time": summary_time, "attempted": len(external), "successful": successes, "availability": successes / window_seconds, "error_fraction": (len(external) - successes) / window_seconds, "error_classification": error_classification, "handler_status_counts": status_counts, "handler_errors": handler_errors, "handler_mean": np.mean(numeric_values), "handler_std": np.std(numeric_values, ddof=0), "handler_count": len(telemetry), "units": units, "external_failures": external_failures, "absent_handler_records": absent, "telemetry": telemetry}
'''
  exprs=['report'];packages=['numpy']
  prompt='Complete instrumented_handler and report, leaving the deterministic supplied probe/fault/clock helpers and CSV loader unchanged. timestamp() is the supplied replay clock in seconds: bracket JSON decode, supplied_predict and JSON encode, and call record_telemetry(start, finish, status) in finally for success (200) and handled ValueError (500). Return encoded JSON. Run run_supplied_probe once. Keep every external attempt in the half-open [window_start, window_start+window_seconds) window, one per second; summary_time allows the final attempt its full deadline. Use the prescribed window_seconds denominator (300 in this fixture), not handler_count. Success requires HTTP 200, valid_prediction and completion within deadline_seconds. report must have exactly window (two endpoints), summary_time, attempted, successful, availability, error_fraction (every non-success/all attempts), error_classification, handler_status_counts, handler_errors (non-200), handler_mean, handler_std (ddof=0), handler_count, units, external_failures (counts by outcome), absent_handler_records (request_id/outcome dictionaries in attempt order), telemetry (timestamped records). Include all handler durations, even handled errors, in mean/std. Reconcile missing handler records without dropping their external outcomes.'
 ix['public']={'prompt':prompt,'runtime':{'kind':'python','version':load(pathlib.Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']['python']['version'],'packages':packages},'workspace':{'entry':'learner.py','files':[{'path':'learner.py','role':'editable','language':'python','content':starter}],'asset_mounts':mounts},'constraints':constraints}
 ix['grading']={'solution_files':[{'path':'learner.py','content':solution}],'tests':[]}
 for i,expr in enumerate(exprs):ix['grading']['tests'].append({'test_id':'t'+str(i+1),'kind':'value_equals','message_on_fail':'Compare the computed report with every requested field, population, and fixture predicate.','spec':{'expr':expr,'expected':None,'tolerance':1e-8}})
 code_jobs.append((ix,solution,mounts,exprs))

out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
seen=set()
for t in P['tiles']:
 result={'tile_id':t['tile_id'],'interactions':[]};out['tiles'].append(result)
 steps=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 for n,s in enumerate(steps):
  cid=s['concept_ids'][0];k=cid.split('.')[-1]
  measures=[{'concept_id':cid,'capability':a.split('#assessment:')[1],'fact_ids':next(x['fact_ids'] for x in G[cid]['assessment_anchors'] if x['capability']==a.split('#assessment:')[1])} for a in s['anchors'] if '#assessment:' in a]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if n==0 else ('stretch' if n==len(steps)-1 else 'core'),'grading_mode':'client','standalone':False,'measures':measures,'anchors':s['anchors'],'feedback':feedback(cid)}
  if cid in rem:
   ri=rem_used.get(cid,0)
   if ri < len(rem[cid]):ix['feedback']['remediation_step_id']=rem[cid][ri]
   rem_used[cid]=ri+1
  seen.add(cid)
  if ix['type']=='choice':
   key=k
   if k=='model_release_rollback':key='rollback_target' if '#assessment:resolve_approved_rollback_artifact' in ''.join(s['anchors']) else 'rollback_secret'
   prompt,options=Q[key]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':'o'+str(i+1),'text':v[0]} for i,v in enumerate(options)]}
   ix['grading']={'correct_option_ids':['o'+str(i+1) for i,v in enumerate(options) if v[1]],'option_feedback':{'o'+str(i+1):{'message':v[2]} for i,v in enumerate(options)}}
  elif ix['type']=='classify':
   groups=inspect(cid);items=[];assign={};fb={}
   for i,(label,excerpts) in enumerate(groups):
    for title,text in excerpts:
     iid='item'+str(len(items)+1);items.append({'item_id':iid,'text':title+'\n```\n'+text+'\n```'});assign[iid]='b'+str(i+1);fb[iid]={'message':('This excerpt meets the declared predicates and evidence requirements.' if i==0 else 'This excerpt violates a required predicate: ' + title + '. Compare the stated observation with the declared contract; a partial passing case does not cure this defect.')}
   ix['public']={'prompt':'Inspect each independent authored nonproduction-lab excerpt. Classify whether the shown fragment/evidence meets the part of the declared practice it addresses or violates it. Judge only the explicit evidence; do not assume unseen checks. Names, limits and artifact identities are supplied fixture values.','buckets':[{'bucket_id':'b'+str(i+1),'label':label} for i,(label,_) in enumerate(groups)],'items':items}
   ix['grading']={'assignments':assign,'item_feedback':fb}
  else:code(cid,ix)
  result['interactions'].append({'step_id':s['step_id'],'interaction':ix})

# Descriptor conflicts: scaffold unsupported glue, keep learner edits in allowed calls/assignments.
for ix, old_solution, mounts, exprs in code_jobs:
    cid=ix['measures'][0]['concept_id']
    k=cid.split('.')[-1]
    if k == 'bounded_batch_inference':
        helper=old_solution[:old_solution.index('def validate_records')]
        helper += '''
def validate_keyed_records(records, expected_records):
    assert len(records) == len(expected_records)
    assert len({r["order_id"] for r in records}) == len(records)
    assert {r["order_id"] for r in records} == {r["order_id"] for r in expected_records}
    expected = {r["order_id"]: r for r in expected_records}
    for record in records:
        assert set(record) == set(result_keys)
        assert record == expected[record["order_id"]]
    return True
def no_validation(records, expected_records):
    return True
def discard_identity(key, prediction):
    return {"prediction": prediction, "version": version}
def keyed_record(key, prediction):
    return {"order_id": key, "prediction": prediction, "version": version}
def run_pipeline(reader, size, make_record, validate_records):
    decoded = []
    expected = []
    chunk_lengths = []
    events = []
    with open(input_path) as inp, open(output_path, "w") as out:
        for chunk in reader(inp, chunksize=size):
            events.append("read")
            chunk_lengths.append(len(chunk))
            predictions = fitted_package.predict(chunk[feature_names])
            for key, prediction in zip(chunk["order_id"], predictions):
                expected.append(keyed_record(key, prediction))
                out.write(json.dumps(make_record(key, prediction)) + "\\n")
            events.append("write")
    with open(output_path) as inp:
        for line in inp:
            decoded.append(json.loads(line))
    fixtures = [decoded[::-1], decoded[:-1], decoded + decoded[:1], [{**r, "order_id": "unknown"} if i == 0 else r for i, r in enumerate(decoded)], [{"order_id": r["order_id"]} for r in decoded], [{**r, "prediction": r["prediction"] + 1} if i == 0 else r for i, r in enumerate(decoded)]]
    checks = []
    for fixture in fixtures:
        try:
            checks.append(validate_records(fixture, expected))
        except AssertionError:
            checks.append(False)
    return {"records": decoded, "chunk_lengths": chunk_lengths, "events": events, "validation_results": checks}
'''
        prefix='import pandas as pd\nfrom scaffold import declared_rows, run_pipeline, keyed_record, discard_identity, validate_keyed_records, no_validation\n'
        prefix+='full_fixture_rows = '+repr(len(A['ds.orders']['rows']))+'\n'
        starter=prefix+'# Complete the callback/size wiring; inspect the readonly pipeline and validators.\nreader = pd.read_csv\nchunk_rows = full_fixture_rows\nmake_record = keyed_record\nvalidate_records = no_validation\nbatch_report = run_pipeline(reader, chunk_rows, make_record, validate_records)\n'
        solution=prefix+'reader = pd.read_csv\nchunk_rows = declared_rows\nmake_record = keyed_record\nvalidate_records = validate_keyed_records\nbatch_report = run_pipeline(reader, chunk_rows, make_record, validate_records)\n'
        prompt='Inspect scaffold.py, then correct the callback/size wiring in learner.py. Keep the supplied run_pipeline call and readonly frozen package unchanged. reader must be pandas.read_csv, chunk_rows must be the supplied declared_rows, make_record must preserve order_id with prediction and version, and validate_records must verify exact schema, unique complete keys and keyed predictions independent of order. Choose among the supplied validator callbacks; no_validation intentionally checks nothing. The pipeline writes each chunk before reading the next, then decodes JSON lines and runs reordered-valid, missing, duplicate, mismatched-key, malformed-schema and wrong-prediction fixtures in that order. batch_report must contain records, chunk_lengths, alternating read/write events, and validation_results. The five orders must form chunks of two, two and one with no refitting. Do not change scaffold.py. This is a bounded wiring exercise: transport/iteration/assertion glue is supplied because its syntax descriptors are not executable by this gate.'
    elif k == 'inference_batching_decision':
        prefix_end=old_solution.index('encoded_trace =')
        helper=old_solution[:prefix_end]
        helper+='''
def keep_success(candidate):
    return candidate["success"]
def keep_matched_success(candidate):
    return candidate["success"] and candidate["request_start_seconds"] is not None and candidate["response_complete_seconds"] is not None and candidate["decoded_response"]["request_id"] == candidate["request_id"] and candidate["decoded_response"]["batching_setting"] == candidate["batching_setting"]
def report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat):
    decoded_trace = decode(encode(trace))
    report = {}
    selected = []
    for setting in settings:
        latencies = []
        for row in decoded_trace:
            if row["batching_setting"] == setting:
                row["decoded_response"] = decode(row["response_json"]) if row["response_json"] else {}
                if eligible(row):
                    latencies.append(row["response_complete_seconds"] - row["request_start_seconds"])
        values = np.array(latencies)
        tail = tail_stat(values)
        report[setting] = {"count": len(latencies), "mean": mean_stat(values), "std": std_stat(values), "p99": tail, "units": units, "ddof": divisor, "percentile_method": percentile_method}
        if tail <= latency_objective:
            selected.append(setting)
    return report, selected
'''
        prefix='import numpy as np\nfrom json import loads, dumps\nfrom scaffold import report_from_trace, keep_success, keep_matched_success, declared_percentile, percentile_method\n'
        functions='''def mean_stat(numeric_values):
    return np.mean(numeric_values)
def std_stat(numeric_values):
    return np.std(numeric_values, ddof=0)
def tail_stat(latencies):
    return np.percentile(latencies, declared_percentile, method=percentile_method)
'''
        starter=prefix+'''# TODO: replace the empty statistics with the taught NumPy calls.
def mean_stat(numeric_values):
    return None
def std_stat(numeric_values):
    return None
def tail_stat(latencies):
    return None
# Choose the callback that matches response identity/setting and excludes missing request traces.
decode = loads
encode = dumps
eligible = keep_success
report, selected = report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat)
'''
        solution=prefix+functions+'decode = loads\nencode = dumps\neligible = keep_matched_success\nreport, selected = report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat)\n'
        prompt='Inspect the supplied trace matching/report scaffold, then complete mean_stat, std_stat and tail_stat using np.mean, np.std(..., ddof=0) and np.percentile(..., declared_percentile, method=percentile_method). Keep supplied imports and final report_from_trace call unchanged. Wire decode to loads and encode to dumps, and select the eligible callback that excludes failures and responses lacking a request-start trace and matches decoded response identity and setting (keep_success does not perform those checks). The supplied pipeline uses response completion minus request start, including waiting, in seconds. report contains each supplied setting in settings order with count, mean, std, p99, units, ddof, percentile_method; selected lists settings with p99 <= latency_objective, or [] if none qualify. Do not change scaffold.py. The scaffold supplies matching/iteration glue; the learner completes the supported eligibility wiring and numerical functions.'
    else:
        prefix_end=old_solution.index('def instrumented_handler')
        helper=old_solution[:prefix_end]
        helper=helper.replace('return {"predictions": [sum(row) for row in payload["features"]], "version": "A"}', 'return {"predictions": model.predict(preprocessing_pipeline.transform(payload["features"])), "version": version}')
        helper+='\n'+file('ws.service_telemetry','frozen_package.py')+'\nversion = '+repr(C['version'])+'\n'
        handler=old_solution[prefix_end:old_solution.index('external = run_supplied_probe')]
        helper+=handler
        summary=old_solution[old_solution.index('external = run_supplied_probe'):]
        summary=summary.replace('np.mean(numeric_values)','mean_stat(numeric_values)').replace('np.std(numeric_values, ddof=0)','std_stat(numeric_values)')
        # Two eligible policies make the denominator/negative-case distinction learner-controlled.
        summary=summary.replace('if attempt["http_status"] == 200 and attempt["valid_prediction"] and attempt["response_complete_seconds"] is not None and attempt["response_complete_seconds"] - attempt["request_start_seconds"] <= deadline_seconds:', 'if available(attempt):')
        summary=summary.replace('successes / window_seconds', 'successes / denominator').replace('(len(external) - successes) / window_seconds', '(len(external) - successes) / denominator')
        helper+='''
def accept_http_only(attempt):
    return attempt["http_status"] == 200
def accept_valid_deadline(attempt):
    return attempt["http_status"] == 200 and attempt["valid_prediction"] and attempt["response_complete_seconds"] is not None and attempt["response_complete_seconds"] - attempt["request_start_seconds"] <= deadline_seconds
handler_denominator = sum(a["handler_start_seconds"] is not None for a in attempts)
def report_probe(mean_stat, std_stat, available, denominator):
'''
        helper+='\n'.join('    '+line for line in summary.splitlines())+'\n    return report\n'
        prefix='import numpy as np\nfrom scaffold import report_probe, accept_http_only, accept_valid_deadline, window_seconds, handler_denominator\n'
        functions='''def mean_stat(numeric_values):
    return np.mean(numeric_values)
def std_stat(numeric_values):
    return np.std(numeric_values, ddof=0)
'''
        starter=prefix+'''# Inspect the supplied instrumented handler, external outcomes and deadline policies.
def mean_stat(numeric_values):
    return None
def std_stat(numeric_values):
    return None
available = accept_http_only
denominator = handler_denominator
report = report_probe(mean_stat, std_stat, available, denominator)
'''
        solution=prefix+functions+'available = accept_valid_deadline\ndenominator = window_seconds\nreport = report_probe(mean_stat, std_stat, available, denominator)\n'
        prompt='Inspect scaffold.py: its deterministic external probe preserves one valid request per second in the half-open [window_start, window_start+window_seconds) window and summary_time allows the final two-second deadline. Its instrumented handler brackets JSON decode, frozen prediction and JSON encode with timestamp(); finally records success and handled ValueError duration/status. Complete mean_stat with np.mean and std_stat with np.std(..., ddof=0) over all handler durations, including errors. Wire available to the supplied policy requiring HTTP 200, valid prediction and timely completion, not HTTP status alone; wire denominator to prescribed window_seconds (300), never handler_denominator. Keep report_probe call and readonly scaffold unchanged. report must contain window endpoints, summary_time, attempted, successful, availability, error_fraction (non-success/300), explicit error_classification, handler_status_counts, handler_errors, handler_mean, handler_std, handler_count, units, external_failures by outcome, absent_handler_records (request_id/outcome dictionaries) and timestamped telemetry. Missing handler records remain external attempts. The handler/transport/report assembly are supplied glue; supported learner work is statistical function completion and availability/denominator wiring.'
    if k == 'inference_batching_decision':
        helper=helper.replace('tail = tail_stat(values)', 'tail = tail_stat(values, declared_percentile, method=percentile_method)')
        starter='import numpy as np\nfrom json import loads, dumps\n# Complete numerical callback and eligibility wiring.\nmean_stat = np.median\nstd_stat = np.var\ntail_stat = np.percentile\ndecode = loads\nencode = dumps\neligible = keep_success\nreport, selected = report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat)\n'
        solution='import numpy as np\nfrom json import loads, dumps\nmean_stat = np.mean\nstd_stat = np.std\ntail_stat = np.percentile\ndecode = loads\nencode = dumps\neligible = keep_matched_success\nreport, selected = report_from_trace(decode, encode, eligible, mean_stat, std_stat, tail_stat)\n'
        prompt='Inspect the supplied infrastructure block, then correct the numerical and eligibility callback wiring in learner.py. Set mean_stat to np.mean (arithmetic mean), std_stat to np.std (the supplied call uses its population default ddof=0), tail_stat to np.percentile (the supplied call uses declared_percentile and percentile_method). Wire decode to loads and encode to dumps. Select keep_matched_success rather than keep_success: only matched successful decoded responses with both request-start and response-completion traces contribute. The supplied pipeline uses response completion minus request start in seconds including batch waiting. report must contain each setting with count, mean, std, p99, units, ddof, percentile_method; selected lists supplied settings meeting p99 <= latency_objective, in settings order, or [] if none qualify. Keep the final report_from_trace call and supplied infrastructure block unchanged. This is a callback-wiring adaptation because definition, iteration and predicate syntax descriptors are not executable by the gate.'
    bootstrap = '# Supplied infrastructure glue; do not edit this block.\nexec(' + repr(helper) + ')\n'
    starter = bootstrap + '\n'.join(line for line in starter.splitlines() if not line.startswith('from scaffold import')) + '\n'
    solution = bootstrap + '\n'.join(line for line in solution.splitlines() if not line.startswith('from scaffold import')) + '\n'
    prompt = prompt.replace('scaffold.py', 'the supplied infrastructure block')
    ix['public']['prompt']=prompt
    ix['public']['workspace']['files']=[{'path':'learner.py','role':'editable','language':'python','content':starter}]
    ix['grading']['solution_files']=[{'path':'learner.py','content':solution}]
    for j,(jix,_,jm,je) in enumerate(code_jobs):
        if jix is ix:
            code_jobs[j]=(ix,solution,mounts,exprs)
            break

# Expected answers are obtained by a real execution in the pinned player engine.
scripts=[]
for i,(ix,solution,mounts,exprs) in enumerate(code_jobs):
 scripts.append({'id':str(i),'entry':'learner.py','files':ix['grading']['solution_files'],'mounts':[{'path':m['mount_path'],'columns':[c['name'] for c in A[m['asset_id']]['columns']],'rows':A[m['asset_id']]['rows']} for m in mounts],'probes':[{'id':str(j),'kind':'expr','expr':expr} for j,expr in enumerate(exprs)]})
job={'scripts':scripts}
(B/'stage04_execution_job.json').write_text(json.dumps(job))
proc=subprocess.run(['node','00_FINAL_PIPELINE_CORE/sandbox/run_py.mjs'],input=json.dumps(job),text=True,capture_output=True)
(B/'stage04_execution_result.json').write_text(proc.stdout)
if proc.returncode:raise RuntimeError(proc.stderr)
data=json.loads(proc.stdout)
for i,(ix,_,_,exprs) in enumerate(code_jobs):
 res=data['results'][str(i)]
 if not res['ok']:raise RuntimeError(res)
 for j,test in enumerate(ix['grading']['tests']):
  probe=res['probes'][str(j)]
  if not probe['ok']:raise RuntimeError(probe)
  test['spec']['expected']=probe['value']
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
