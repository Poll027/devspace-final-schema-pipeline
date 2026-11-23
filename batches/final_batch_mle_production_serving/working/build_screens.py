import json, copy, re
from pathlib import Path
P=Path('batches/final_batch_mle.region.production_serving')
plan=json.loads((P/'tile_plans.json').read_text()); glossary=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in glossary['bundles']}; A={a['asset_id']:a for a in registry['assets']}
def file(cid,path): return next(f['content'] for f in A['ws.'+cid]['files'] if f['path']==path)
def contract(cid):return json.loads(file(cid,'contract.json'))
def runtime(cid):return json.loads(file(cid,'runtime_contract.json'))
# Authored re-voicing of teaching blocks; numeric examples are substituted from registered fixtures below.
texts={
'prediction_schema_validation':{
2:'The request schema specifies features, types and permitted values; the response schema specifies output structure. Decode JSON into Python values first: raw text is not a request dictionary. Compare required and supplied keys, then use conditional predicates for declared types and numeric boundaries.',
3:'For matrix input, build the declared NumPy representation and check rank, feature width and response-row alignment. Explicitly reject malformed or out-of-contract input rather than predicting successfully. Assert valid, boundary and failure predicates: a false assert raises AssertionError in ordinary, non-optimized execution.',
4:'Encode structured values with json.dumps and decode with json.loads before field checks. Send encoded JSON bytes using urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"). Read through urlopen with the stated timeout.',
5:'In the order fixture, validate decoded keys, types, matrix dimensions and permitted values before using features as model input. Test an included limit separately from a value beyond it. A missing key is a different rejection from an out-of-range value. After prediction, independently check output keys, declared values or shape, and row correspondence. Serialize the request, send encoded bytes with the JSON header and bounded timeout, then decode the response. Parsing, request acceptance and response correctness are separate assertions; transport timing cannot replace schema validation.',
6:'Parsing JSON does not establish schema acceptance. Raw text still needs decoding, and a decoded response with incorrect row correspondence violates the contract.'},
'online_prediction_contract':{
2:'Subclass BaseHTTPRequestHandler and implement do_POST for the declared route. Read Content-Length from headers, then that many bytes from rfile. Decode and validate before applying the already fitted preprocessing and model. Do not fit or update either object during a request.',
3:'Serialize the named response dictionary with json.dumps(...).encode("utf-8"). Use send_response for status and send_header for Content-Type and encoded body length; finish with end_headers, then write bytes to wfile. This bounded http.server fixture is not a production-server recommendation.',
4:'Construct HTTPServer((host, port), Handler) on the existing runtime with the configured host and port; call serve_forever(). Assert declared valid, boundary and failure cases. A false predicate raises AssertionError during ordinary non-optimized execution.',
5:'Trace one request from the declared byte-length read through decoded fields, validation and unchanged fitted prediction state to UTF-8 JSON output. Serialize and encode before writing headers: Content-Length must describe the actual encoded body, not an assumed character count. Write status, headers and body as one complete bounded exchange. Exercise normal, boundary and invalid fixtures with assertions. Input length defines the read boundary; schema predicates determine whether those decoded values are permitted. Neither step authorizes fitting during a request.',
6:'A printed prediction is not a complete response: declared status, content type and byte length still matter. Keep the standard-library demonstration bounded, not a production-server design.'},
'bounded_batch_inference':{
2:'Iterate with a format-appropriate bounded reader, such as pd.read_csv(path, chunksize=declared_rows), instead of loading the entire dataset. Apply the same fitted preprocessing and model without refitting. Carry observation keys beside predictions and verify one result per eligible input key, not incidental output order.',
3:'Serialize results in the declared format, then decode the written fixture to verify schema and key alignment. Use explicit with open(...) handles and write each bounded result set before reading the next chunk. Assert valid, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution.',
4:'Process the keyed orders in bounded chunks, keeping each key with its prediction through writing. Reopen and decode the persisted fixture, inspect its schema, and compare key coverage with eligible input IDs. A duplicate result for one key and a missing result for another can leave the total row count unchanged. Explicit handles identify where the results were written and rechecked. Reuse the same fitted package throughout; inference correctness includes persistence and identity, not just in-memory values.',
5:'Equal row counts can hide duplicate and missing keys. Preserve observation identity and unchanged fitted state rather than trusting output order.'},
'model_service_readiness':{
2:'A health endpoint must succeed within its runtime health-check contract; SageMaker uses /ping. Report ready only after the model is loaded and inference can be accepted, not merely after startup. Configure the declared readiness command, interval, timeout and retry count.',
3:'Implement do_GET for the readiness route. Return non-ready until both fitted model and preprocessor are initialized; only then return success. Serialize readiness as JSON and check status plus decoded state before and after initialization. Use docker inspect to inspect health status and ensure the unready fixture does not pass.',
4:'Start the referenced image with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE, using declared nonsecret settings. Check image identity and State with docker container inspect NAME; inspect captured stdout/stderr for initialization or execution failures using docker container logs NAME.',
5:'Assert valid, boundary and failure fixtures; false predicates raise AssertionError in ordinary non-optimized execution.',
6:'In the initialization fixture, a running process remains non-ready while either fitted object is unavailable. Inspect image identity, State and initialization logs, then test both sides of initialization using HTTP status and decoded JSON. Configure the supplied healthcheck and inspect its health result. A readiness success reported before the objects become usable must fail the fixture.',
7:'Running is not ready. An endpoint response alone is insufficient: successful readiness requires the inference-ready condition, correct status and decoded state.'},
'deployment_configuration_code':{
2:'Use the approved immutable image digest, not a mutable tag. In Compose, declare services.prediction with image, environment for nonsecret settings, HOST:CONTAINER ports, secrets references and deploy.replicas. Declare top-level secrets.credential.environment as the injected host variable name, never its value. Substitute the supplied digest, ports and supported replica count; keep configuration repeatable on the existing runtime.',
3:'Run docker compose -f CONFIG_PATH config before application and compare resolved fields with the runtime contract. Apply with docker compose -f CONFIG_PATH up -d, then inspect containers. Set replicas at services.<service>.deploy.replicas and CPU/memory bounds at deploy.resources.limits.cpus and memory only where these deploy fields are supported. Validate resolved counts and bounds first.',
4:'Dockerfile ARG and ENV can persist secrets in the final image or metadata: do not embed them. Deliver sensitive values through runtime secrets, not literal Compose values. After application, inspect running image identity and compare it with the recorded artifact.',
5:'On the supplied authorized VM, use gcloud compute instances start INSTANCE --zone=ZONE or stop to change lifecycle state. Wait for completion and inspect state. Use gcloud compute instances describe INSTANCE --zone=ZONE before and after the action, and gcloud compute ssh INSTANCE --zone=ZONE to execute the workload on the running VM.',
6:'Create the configuration branch with git checkout -b BRANCH; commit verified configuration and merge under the existing workflow. Destroy only the test deployment with docker compose -f CONFIG_PATH down, then reapply the same file and verify identical image identity and resolved settings. With PyYAML, write mappings/lists using yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required fields. Safe loading supports standard tags, not arbitrary Python constructors.',
7:'Author the registered digest, port mapping, replica count and supported resource bounds. Parse YAML, inspect compose config, apply, then inspect actual identity and runtime settings. Record the verified configuration through the existing branch/commit workflow. In the bounded test, destroy only that deployment and recreate it from the same file, checking identical identity and settings. Use only supplied authorized VM lifecycle hooks. Name secret references or injected variables without recording their literal values.',
8:'A parsed file proves neither running state nor immutable identity. Mutable tags can change, and deploy resource fields require runtime support.'},
'deployment_verification':{
2:'Verify the recorded artifact and configuration in the actual existing execution environment; launch success is not enough. Start the referenced image using docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE with declared nonsecret settings. Inspect its image identity and State using docker container inspect NAME.',
3:'Inspect initialization and execution stdout/stderr with docker container logs NAME. Compare running identity and State with the intended release, including Health when a healthcheck exists. Preserve sanitized findings without copying credentials or sensitive request data into evidence.',
4:'Call readiness and prediction with bounded timeouts and check status and payload contracts. Use json.dumps for serialization, encoded JSON bytes in urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), and urlopen with the stated timeout. Decode with json.loads before checking fields.',
5:'Check the small fixed prediction fixture for declared output shape and values. Assert valid, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution.',
6:'Compare the running image and settings with the release record, inspect State and available Health, and capture sanitized log findings. Exercise readiness and a small JSON prediction fixture with explicit timeouts and decoded response assertions. Retain separate identity, initialization and contract checks so failures remain attributable. Plausible predictions cannot repair a running-image mismatch.',
7:'A successful launch or correct-looking prediction does not verify a release whose artifact identity or runtime configuration differs from the intended record.'},
'prediction_authentication':{
2:'Authentication establishes caller identity; authorization determines whether that identity may predict. Both are required. Give the protected credential only to its permitted service through a runtime secret reference. Keep platform nonsecret authentication settings in configuration, separate from the credential literal.',
3:'Exercise authorized, missing and invalid credential requests and check allowed or denied responses under the supplied policy. Inspect failure visibility without exposing credentials or protected request values. Compose declares named services using indented mappings; use specification-required list or mapping forms for their fields.',
4:'Set the immutable image, HOST:CONTAINER port mappings and declared nonsecret environment values. Run docker compose -f CONFIG_PATH config and compare resolved fields with the intended contract before docker compose -f CONFIG_PATH up -d. Inspect resulting containers.',
5:'Import id_token from google.oauth2 and requests from google.auth.transport. In authorize_prediction(token, expected_audience, permitted_subjects), reject missing tokens; call id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience). Return verified claims only when claims["sub"] belongs to permitted_subjects, otherwise raise PermissionError. Use verified sub, not unverified decoding or changeable email. Assert valid, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution. With PyYAML, safe_dump mappings/lists, safe_load them and inspect required fields; standard tags are accepted, not arbitrary Python constructors.',
6:'Import GoogleAuthError from google.auth.exceptions. Catch verification ValueError or GoogleAuthError and raise PermissionError into the harness denial path before prediction. ValueError signals verification failure; GoogleAuthError includes invalid issuer. Deny missing, invalid and verified-but-unpermitted tokens without predicting or logging the token.',
7:'Use the supplied audience and subject policy. Check missing, invalid, authorized and verified-but-unpermitted fixtures. A valid token does not grant permission to every subject. Inspect denied responses, prediction-execution records and redacted logs. Parse the immutable image, ports and nonsecret authentication configuration with credentials represented only by runtime references. Neither an unverified decode nor email replaces the verified-subject check.',
8:'Verification is not permission. Deny a verified but unpermitted subject, and keep credential literals out of YAML and logs.'},
'service_telemetry':{
2:'Use client-visible outcomes and latency as indicators; container or CPU state alone cannot establish availability. Measure elapsed time with time.perf_counter() after completion minus its start value. Retain timestamped outcomes and durations in a consistent unit to distinguish success, error and timeout attempts.',
3:'Divide error attempts by eligible attempts in the declared window. Use the same window and denominator for successful eligible attempts divided by all eligible attempts, including failures. Compute the arithmetic mean of selected numeric observations with np.mean(numeric_values).',
4:'Use np.std(numeric_values, ddof=0) for the N divisor; choose ddof=1 only when the stated calculation requires N−1. Time JSON decoding, prediction and response encoding in the handler, recording duration and status/error counts even for handled errors. Preserve all attempts from the prescribed half-open probe window.',
5:'Availability requires HTTP 200 with a valid prediction within the stated deadline. Let the final attempt use its full deadline before summarizing. Divide successful-deadline outcomes by the full probe denominator, retaining connection refusals and timeouts even without handler records. Report window, numerator and denominator alongside handler statistics/status counts, reconciling absent handler records with external failures.',
6:'Keep the prescribed probe schedule and every external attempt. A response counts only if its status, prediction validity and deadline all pass. Reconcile connection refusals or timeouts against absent handler records; do not silently drop them. Record handler timing across decoding, prediction and encoding, including handled errors. Use timestamped durations in one unit and allow the final request its full deadline before computing the summary.',
7:'Handler success rate is not automatically client availability. Dropping attempts that never arrived changes the denominator and conceals failures.'},
'prediction_load_test':{
2:'At each declared arrival/concurrency profile, run for a bounded duration and retain client outcomes and response times. Acceptance requires the predeclared success, tail-latency and completed-throughput objectives. Keep failures and timeouts separate: completed-response latency does not represent every attempt.',
3:'Success probability is successful eligible attempts divided by all eligible attempts in the measurement window, including failures. Use np.percentile(completed_latency_values, declared_percentile), retaining convention, sample count and time unit. Successful throughput is completed successful requests divided by elapsed measurement time; compare it with offered load rather than equating arrivals with work completed.',
4:'Run valid and malformed HTTP JSON assertions separately: intentional malformed cases do not belong in valid-traffic capacity measurement. At each fixed offered load, retain the stated valid payload mix, warm-up and measurement duration. Count successes, HTTP errors, timeouts and other failures separately; failed fraction divides all failed attempts by all valid-traffic attempts.',
5:'Inspect unfinished work and backlog throughout the window. Accept only stable-backlog loads meeting the fixed latency and error objectives; report the highest measured successful throughput or no feasible envelope. Start the referenced image with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE and inspect image identity and State with docker container inspect NAME.',
6:'Inspect captured initialization/execution output with docker container logs NAME. Encode JSON with json.dumps, send bytes using urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), and use urlopen with a stated timeout. Decode returned JSON with json.loads before field checks.',
7:'Use np.mean(numeric_values) for the arithmetic mean. For standard deviation, np.std(numeric_values, ddof=0) divides squared deviations by N before the square root; use ddof=1 only for a required N−1 divisor. Assert valid, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution.',
8:'Compare attempts, successful completions and separate failure categories over the fixed valid-traffic window. Compute success and failure fractions from all eligible attempts, and throughput from successful completions per elapsed time. Evaluate the declared completed-response percentile with its sample count, convention and units. Inspect backlog throughout, then accept only stable passing measured loads or report no feasible envelope. Keep intentional malformed fixtures outside this denominator.',
9:'Arrivals are not completed work. Fast completed responses cannot hide timeouts, and growing backlog cannot establish a stable acceptable load.'},
'inference_batching_decision':{
2:'Serialize with json.dumps and decode with json.loads before field checks. Match each successful response to its request identity and batching setting. Measure response completion minus request start in one declared unit, including batch waiting.',
3:'Compute np.percentile(latencies, declared_percentile) with explicit convention and successful-response sample count. Compare settings under the same trace/population interpretation and choose only a limit meeting the latency objective. Use np.mean(numeric_values) for the arithmetic mean.',
4:'For standard deviation, np.std(numeric_values, ddof=0) uses the N divisor before the square root. Use ddof=1 only if the stated calculation requires N−1.',
5:'Follow the same identified request from start through batch waiting to response completion. Decode and associate its successful response with the request and setting before measuring the full interval. Summarize eligible successful-response durations using the declared percentile, mean and specified spread; retain units, convention and sample count. Compare only measured settings with the same population interpretation. A shorter execution interval can still fail the full latency objective when waiting is included; unmatched responses are not valid duration samples.',
6:'Waiting is part of end-to-end latency. Faster execution alone cannot make a batching limit pass the full request objective.'},
'serving_worker_concurrency':{
2:'Compose uses named services and specification-required indented mappings/lists. Declare immutable image identity, HOST:CONTAINER ports and nonsecret environment settings. Run docker compose -f CONFIG_PATH config and compare resolved fields with the runtime contract before application.',
3:'Set the existing runtime worker-limit field, validate its parsed value, and apply the referenced image with docker compose -f CONFIG_PATH up -d. Inspect containers. During the bounded load, use docker container top NAME and compare actual prediction-worker count with the configured limit to detect oversubscription.',
4:'Observe CPU and memory during that same load interval to support the bound check. With PyYAML, write mappings/lists using yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields. Safe loading permits standard tags, not arbitrary Python constructors.',
5:'Keep authored, safely reloaded and Compose-resolved limits separate from running process evidence. Apply the declared image and settings, then inspect prediction workers during load; supporting processes are not workers. Compare the observed worker count with the registered limit, alongside CPU/memory observations from the same interval. A successful configuration command cannot erase a count above the bound.',
6:'Configuration records intent, not proof of process count. Compare worker evidence and concurrent resources from the same bounded fixture.'},
'serving_replica_scaling':{
2:'For fixed Compose scaling, declare deploy.replicas or use docker compose up -d --scale SERVICE=COUNT, then inspect actual replicas. For the supplied SageMaker target, register the endpoint variant with explicit MinCapacity/MaxCapacity. Target tracking declares a metric, target value and scale-in/out cooldowns; apply only the supported supplied policy to the existing target.',
3:'Compare settings at the same declared load against observed success, p99 latency and throughput objectives. Success probability divides successful eligible attempts by all eligible attempts, including failures. Use np.percentile(completed_latency_values, declared_percentile), retaining convention, sample count and time unit. More replicas are not automatically better.',
4:'Successful throughput divides completed successful requests by elapsed measurement time, not arrivals. Edit the existing YAML replica policy from demand/capacity evidence; parse and inspect resolved bounds before application. Inspect containers before and after the bounded demand change, comparing observed count and identities with intended policy.',
5:'After the check, restore original nonproduction replica and lifecycle settings. Use np.mean(numeric_values) for arithmetic mean and np.std(numeric_values, ddof=0) for the N divisor before the square root; use ddof=1 only when N−1 is required.',
6:'Inspect authorized instance status and identity before and after lifecycle actions using gcloud compute instances describe INSTANCE --zone=ZONE. With PyYAML, write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required fields. Safe loading accepts standard tags, not arbitrary Python constructors.',
7:'Retain fixed replica counts or the supplied scalable target bounds, metric target and cooldowns. Parse changed settings before application; inspect container counts, identities and instance lifecycle state afterward. Compare success, p99 and completed throughput at the same load and sample conventions. A larger count that misses latency still fails. Restore original nonproduction settings after the bounded check and preserve the evidence.',
8:'Intended counts differ from observed counts. Extra replicas do not guarantee the objective, and offered load cannot replace completed throughput.'},
'model_release_rollback':{
2:'Resolve the previously approved registry version and immutable artifact as the target, not an unapproved latest version. Use that recorded previous image for the replacement. Verify readiness and a bounded prediction fixture, including the response contract, after restoration.',
3:'Keep secrets out of Dockerfile ARG/ENV because they persist in the image or metadata; use runtime secrets rather than literal Compose values. Start the approved replacement under a distinct identity with required environment and published port. Do not retire the faulty test release before replacement readiness.',
4:'Only after readiness and a verified JSON prediction/version response, stop and remove the faulty test release while preserving the replacement. Serialize with json.dumps, send encoded bytes using urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), and read through urlopen with the stated timeout. Decode with json.loads before checking fields.',
5:'Compare replacement identity and State with the intended release, including Health when configured. Inspect initialization/execution logs without recording credentials or sensitive requests. Call readiness and prediction with bounded timeouts; check returned status and payload contracts.',
6:'Start the approved previous release under its distinct replacement identity. Inspect image identity, State and available Health, then verify readiness and the bounded decoded prediction/version response. Only afterward stop and remove the faulty test container. Preserve the replacement and sanitized evidence. Credentials remain runtime-injected rather than embedded in images or Compose literals; the chronology must show verification before retirement.',
7:'Rollback is neither “use latest” nor blanket removal. Preserve approved version/artifact identity and verify replacement readiness before retiring the faulty test release.'}}
# Titles and concise recap takeaways.
concept_titles={
'prediction_schema_validation':'Decode, validate, then accept', 'online_prediction_contract':'Serve with unchanged fitted state', 'bounded_batch_inference':'Persist predictions with their keys', 'model_service_readiness':'Running is not ready', 'deployment_configuration_code':'Make deployment reproducible', 'deployment_verification':'Verify the running release', 'prediction_authentication':'Verify identity and permission', 'service_telemetry':'Keep the client denominator', 'prediction_load_test':'Measure the feasible load envelope', 'inference_batching_decision':'Include batch waiting', 'serving_worker_concurrency':'Check the observed worker bound', 'serving_replica_scaling':'Compare capacity under one objective', 'model_release_rollback':'Verify replacement before retirement'}
tile_titles=['Validate and serve predictions','Configure and verify deployment','Secure and observe the endpoint','Load-test and scale serving','Roll back a model release']
recaps=[
'Decode and validate requests and responses independently. Keep fitted prediction state unchanged online and across bounded chunks. Preserve persisted observation keys. Admit inference only after both fitted objects are usable, checking readiness status and decoded state.',
'Preserve the immutable artifact and resolved runtime contract across recreation. Keep secrets runtime-injected. Verify actual identity, State, available Health, sanitized logs and bounded decoded endpoint responses rather than trusting launch success.',
'Verify caller identity and prediction permission separately; denied paths must not predict or expose credentials. Measure client-visible success over the full eligible-attempt denominator, including absent handler records, and reconcile it with handler timing and status evidence.',
'Accept only measured loads meeting success, tail-latency, throughput and stable-backlog objectives. Include batch waiting in request latency. Compare observed workers with the configured bound. Evaluate replicas at the same load and restore original nonproduction settings.',
'Resolve the approved previous version and immutable artifact. Start a distinct replacement, inspect it and verify readiness plus decoded prediction/version evidence before stopping and removing only the faulty test release. Preserve the replacement and runtime secret boundary.']
def lineage(cid,tbs,facts,anchors=None):
 return {'concept_ids':[cid], 'teaching_block_ids':[cid+'#'+x for x in tbs], 'fact_ids':[cid+'#'+x for x in facts], **({'anchors':anchors} if anchors else {})}
def prose(text,lin,role='mechanism'): return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lin)}
def table(asset,lin,caption,columns=None):
 ref={'asset_id':asset}
 if columns:ref['columns']=columns
 return {'type':'data_table','asset_ref':ref,'caption':caption,'lineage':copy.deepcopy(lin)}
def diagram(labels,lin,kind='sequence',edges=True):
 nodes=[{'id':'n'+str(i),'label':x} for i,x in enumerate(labels)]
 return {'type':'diagram','diagram_kind':kind,'nodes':nodes,'edges':[{'from':nodes[i]['id'],'to':nodes[i+1]['id'],'directed':True} for i in range(len(nodes)-1)] if edges else [],'alt_text':' → '.join(labels),'lineage':copy.deepcopy(lin)}
def code(src,lin,lang='python'):return {'type':'code_walkthrough','language':lang,'code':src,'reveal':'all','lineage':copy.deepcopy(lin)}
def visual(cid,ps):
 short=cid.split('.')[-1];lin=lineage(cid,[x.split('#')[1] for x in ps['teaching_block_ids']],[x.split('#')[1] for x in ps['fact_ids']],[cid+'#visual']); c=contract(short);r=runtime(short)
 if short=='prediction_schema_validation':
  src='import json\nimport numpy as np\nrequest = json.loads(serialized_body)\nrequired = set(contract["request_keys"])\nsupplied = set(request)\nassert required <= supplied\nmatrix = np.asarray(request[contract["request_keys"][0]], dtype=contract["numpy_dtype"])\nassert matrix.ndim == contract["matrix_rank"]\nassert matrix.shape[1] == contract["matrix_width"]\nresponse = json.loads(serialized_response)\nassert set(contract["response_keys"]) <= set(response)\nassert len(response[contract["response_keys"][0]]) == len(matrix)'
  return [code(src,lin)]
 if short=='online_prediction_contract':
  labels=['Read declared body bytes','Decode and validate','Apply fitted preprocessing/model','Encode UTF-8 JSON','Write status, headers, body']
  nodes=[{'id':'n'+str(i),'label':x} for i,x in enumerate(labels)]
  return [{'type':'process_flow','nodes':nodes,'edges':[{'from':nodes[i]['id'],'to':nodes[i+1]['id']} for i in range(len(nodes)-1)],'direction':'LR','alt_text':'Validated input uses unchanged fitted state before encoded response.','lineage':lin}]
 if short=='bounded_batch_inference':
  return [code('import json\nimport pandas as pd\nwith open(contract["batch_input_path"]) as source, open(contract["batch_output_path"], "w") as sink:\n    for chunk in pd.read_csv(source, chunksize=contract["chunk_size"]):\n        records = predict_keyed_chunk(chunk, fitted_package)\n        for record in records:\n            sink.write(json.dumps(record) + "\\n")\nwith open(contract["batch_output_path"]) as persisted:\n    decoded = [json.loads(line) for line in persisted]\nassert declared_schema_and_key_alignment(decoded, eligible_keys)',lin)]
 if short=='model_service_readiness':
  before=diagram(['Process running','Either fitted object unavailable','Non-ready status and JSON'],lin)
  after=diagram(['Both fitted objects usable','Ready status and JSON','Inspect configured health result'],lin)
  return [{'type':'before_after','before':before,'after':after,'change_summary':'Initialization gates readiness, not process startup.','lineage':lin},table('ds.readiness_cases',lin,'Initialization fixtures; compare status and decoded readiness.')]
 if short=='deployment_configuration_code':
  # Values copied from registered contract, including immutable reference; no literal secret.
  cfg={'services':{r['SERVICE']:{'image':r['IMAGE_DIGEST'],'environment':{r['SETTING']:r['VALUE']},'ports':[str(r['HOST_PORT'])+':'+str(r['CONTAINER_PORT'])],'secrets':[r['secret_reference']],'deploy':{'replicas':r['REPLICA_COUNT'],'resources':{'limits':r['supported_resource_limits']}}}},'secrets':{r['secret_reference']:{'environment':r['secret_environment_variable']}}}
  left=code('config = '+repr(cfg),lin)
  right=code('docker compose -f '+r['CONFIG_PATH']+' config\ndocker compose -f '+r['CONFIG_PATH']+' up -d\ndocker container inspect '+r['NAME']+'\ndocker compose -f '+r['CONFIG_PATH']+' down\ndocker compose -f '+r['CONFIG_PATH']+' up -d\ndocker container inspect '+r['NAME'],lin,'bash')
  return [{'type':'side_by_side','left':left,'right':right,'left_label':'Intended mapping','right_label':'Resolve, apply, recreate, inspect','takeaway':'Compare immutable identity and settings, not command success.','lineage':lin}]
 if short=='deployment_verification':
  return [code('docker container inspect '+r['NAME']+'\ndocker container logs '+r['NAME'],lin,'bash'),code('import json\nimport urllib.request\nbody = json.dumps(payload).encode("utf-8")\nrequest = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")\nwith urllib.request.urlopen(request, timeout=contract["timeout_seconds"]) as response:\n    status = response.status\n    decoded = json.loads(response.read().decode("utf-8"))\nassert declared_response_contract(status, decoded)',lin),table('ds.release_records',lin,'Compare intended immutable identity with runtime inspection.')]
 if short=='prediction_authentication':
  return [code('from google.oauth2 import id_token\nfrom google.auth.transport import requests\nfrom google.auth.exceptions import GoogleAuthError\n\ndef authorize_prediction(token, expected_audience, permitted_subjects):\n    if not token:\n        raise PermissionError("missing credential")\n    try:\n        claims = id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience)\n    except (ValueError, GoogleAuthError):\n        raise PermissionError("verification failed") from None\n    if claims["sub"] not in permitted_subjects:\n        raise PermissionError("subject not permitted")\n    return claims',lin)]
 if short in ['service_telemetry','prediction_load_test']:
  cols=[x['name'] for x in A['ds.serving_attempts']['columns']]
  out=[table('ds.serving_attempts',lin,'Authored client and handler evidence; seconds.',cols)]
  if short=='prediction_load_test':out.append(table('ds.backlog',lin,'Unfinished work throughout each fixed-load window.'))
  return out
 if short=='inference_batching_decision':
  a=A['ds.batching_trace'];names=[x['name'] for x in a['columns']];row=next(dict(zip(names,x)) for x in a['rows'] if x[names.index('batch_wait_end_seconds')]>x[names.index('request_start_seconds')]); labels=[row['request_id']+' / '+row['batching_setting'],str(row['request_start_seconds'])+' s: request start',str(row['batch_wait_end_seconds'])+' s: waiting ends',str(row['response_complete_seconds'])+' s: response complete']
  return [diagram(labels,lin,'timeline'),table('ds.batching_trace',lin,'Match successful responses to request and setting.')] 
 if short=='serving_worker_concurrency':
  left=code('worker_limit = '+repr(r['approved_worker_limit'])+'\nworker_key = '+repr(r['worker_limit_key'])+'\nconfig["services"]["'+r['SERVICE']+'"]["environment"][worker_key] = worker_limit\n# safe_dump, safe_load; inspect resolved value',lin)
  right=table('ds.worker_processes',lin,'Prediction workers versus supporting processes.')
  return [{'type':'side_by_side','left':left,'right':right,'left_label':'Configured bound','right_label':'Observed processes','takeaway':'Compare only prediction workers from the same interval.','lineage':lin},table('ds.worker_resources',lin,'Concurrent CPU/memory evidence; pair by interval_id.')]
 if short=='serving_replica_scaling':
  return [{'type':'before_after','before':diagram(['Original policy','Inspect count and identities'],lin),'after':diagram(['Changed bounded policy','Measure same-load outcomes','Restore original settings'],lin),'change_summary':'Inspect intended and observed capacity through restoration.','lineage':lin},table('ds.replica_states',lin,'Original, changed and restored fixture identities.')]
 if short=='model_release_rollback':
  rb=json.loads(file(short,'rollback_contract.json'))
  return [{'type':'before_after','before':diagram([rb['faulty_identity']+' running','Resolve approved '+rb['approved_target_version']],lin),'after':diagram(['Start '+rb['replacement_identity'],'Inspect; verify readiness and prediction/version','Stop/remove only '+rb['faulty_identity']],lin),'change_summary':'Verify the approved replacement before retirement.','lineage':lin},table('ds.release_transition',lin,'Authored chronology: verification precedes retirement.')]
 raise ValueError(cid)

# Each distinct measured scope has its own remediation; later stage can route by fact coverage.
out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for ti,pt in enumerate(plan['tiles']):
 tile={'tile_id':pt['tile_id'],'title':tile_titles[ti],'summary':registry['scenarios'][0]['summary'],'steps':[],'remediation_steps':[]}
 seen=set()
 for ps in pt['steps']:
  cid=ps['concept_ids'][0];short=cid.split('.')[-1]
  sl={k:copy.deepcopy(ps[k]) for k in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']}
  s={'step_id':ps['step_id'],'type':ps['type'],'concept_ids':ps['concept_ids'],'title':concept_titles[short],'lineage':sl}
  if ps['type'] in ['check','hands_on']:
   s['eyebrow']='Check your understanding' if ps['type']=='check' else 'Apply it in the order lab'
   s['title']=('Check: ' if ps['type']=='check' else 'Practice: ')+concept_titles[short]
   facts=set(ps['fact_ids']);scope=(cid,tuple(sorted(facts)))
   if scope not in seen:
    seen.add(scope)
    # Pull only the primary blocks that re-teach this interaction's facts.
    chosen=[];covered=set()
    for tb in B[cid]['teaching_blocks']:
     n=int(tb['id'][2:]);tf={cid+'#'+f for f in tb.get('fact_ids',[])}
     if tb['purpose'] not in ['definition','mechanism'] or not tf.intersection(facts):continue
     chosen.append((n,tb,tf.intersection(facts)));covered.update(tf)
    assert facts <= covered,(cid,facts-covered)
    rid=pt['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
    rl=lineage(cid,[tb['id'] for _,tb,_ in chosen],[f.split('#')[1] for f in sorted(facts)])
    rem={'step_id':rid,'type':'remediation','required':False,'concept_ids':[cid],'title':'Try the contrast: '+concept_titles[short],'lineage':rl,'blocks':[]}
    contrast={
    'prediction_schema_validation':'Contrast the valid order fixture with a missing-key request: parsing can succeed while contract acceptance fails.',
    'online_prediction_contract':'Contrast a complete encoded response with a printed prediction: the bounded handler still owes status, headers and body.',
    'bounded_batch_inference':'Contrast persisted key coverage with equal row counts: a duplicate and a missing key can cancel in the count.',
    'model_service_readiness':'Contrast the model-only initialization case with both fitted objects usable: a running process is not sufficient.',
    'deployment_configuration_code':'Contrast the verified recreated deployment with a parsed file: configuration intent still needs runtime identity and setting checks.',
    'deployment_verification':'Contrast launch success with release acceptance: a plausible prediction cannot repair an artifact mismatch.',
    'prediction_authentication':'Contrast an authorized subject with a verified-but-unpermitted subject: verification alone does not grant prediction permission.',
    'service_telemetry':'Contrast handler records with the full client probe: missing handler evidence does not remove an eligible failed attempt.',
    'prediction_load_test':'Contrast offered arrivals with completed successful work: timeouts and growing backlog cannot be hidden by fast completed responses.',
    'inference_batching_decision':'Contrast request-start-to-response with post-wait execution: the latency objective includes waiting.',
    'serving_worker_concurrency':'Contrast resolved worker intent with prediction-worker evidence during load: supporting processes are not workers.',
    'serving_replica_scaling':'Contrast intended replica counts with same-load measured results: a larger count can still miss the objective.',
    'model_release_rollback':'Contrast verify-then-retire with early retirement: preserve the approved replacement and remove only the faulty test release.'}[short]
    rem['blocks'].append(prose(contrast,rl,'misconception'))
    for n,tb,tf in chosen:
     lin=lineage(cid,[tb['id']],[f.split('#')[1] for f in sorted(tf)])
     rem['blocks'].append(prose(texts[short][n],lin))
    tile['remediation_steps'].append(rem)
  elif ps['type']=='video':
   s['title']='Supporting segments';s['blocks']=[{'type':'media_group','segment_ids':ps['segment_ids']}]
  elif ps['type']=='recap':
   s['title']='Take the working rules with you';s['blocks']=[prose(recaps[ti],{'concept_ids':ps['concept_ids'],'teaching_block_ids':[],'fact_ids':[]},'takeaway')]
   next_id=pt['next_tile_id'];next_pt=next((t for t in plan['tiles'] if t['tile_id']==next_id),None)
   next_cid=next_pt['concept_ids'][0] if next_pt else 'mle.dataset_quality_gate'
   s['blocks'].append({'type':'up_next','title':glossary['names'][next_cid],'text':'Next tile: '+next_id})
  else:
   s['eyebrow']='Order prediction lab · authored fixture';s['blocks']=[]
   tbs={t['id']:t for t in B[cid]['teaching_blocks']}
   nums=[int(x.split('#tb')[1]) for x in ps['teaching_block_ids']]
   for n in nums:
    if n==1:continue
    tb=tbs['tb'+str(n)];tbids=[tb['id']]
    if 1 in nums and n==nums[1]:tbids.insert(0,'tb1')
    lin=lineage(cid,tbids,tb.get('fact_ids',[]))
    content=texts[short][n]
    # Split long prose at sentence boundaries; never clip a teaching claim.
    sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',content);chunks=[];acc=''
    for sentence in sentences:
     if len((acc+' '+sentence).split())>85 and acc:chunks.append(acc);acc=''
     acc=(acc+' '+sentence).strip()
    if acc:chunks.append(acc)
    for chunk in chunks:s['blocks'].append(prose(chunk,lin,tb['purpose'] if tb['purpose'] in ['definition','mechanism','example','misconception'] else 'mechanism'))
   if ps['planned_visual_block_type']:s['blocks']+=visual(cid,ps)
   s['title']=(concept_titles[short] if 1 in nums else { 'example':'Trace the bounded fixture','misconception':'Keep the distinction','mechanism':'Apply and verify'}[tbs['tb'+str(nums[0])]['purpose']])
  tile['steps'].append(s)
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediations')
