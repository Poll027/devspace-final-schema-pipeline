exec(open('batches/final_batch_mle.region.production_serving/working/build_screens.py').read().split("(P/'screens.json').write_text")[0])
# Add concrete scenario constraints from registry files, without typing fixture values or outputs.
for tile in out['tiles']:
 for s in tile['steps']:
  if s['type']!='explainer':continue
  short=s['concept_ids'][0].split('.')[-1]; c=contract(short);r=runtime(short);mp=json.loads(file(short,'measurement_policy.json'))
  def edit(tb,fn):
   for b in s['blocks']:
    if b['type']=='prose' and any(x.endswith('#'+tb) for x in b['lineage']['teaching_block_ids']): b['text']=fn(b['text']);break
  if short=='prediction_schema_validation':
   edit('tb5',lambda t:'The registered request key is '+repr(c['request_keys'][0])+', with a '+str(c['matrix_rank'])+'-D matrix of width '+str(c['matrix_width'])+' and inclusive feature limits '+str(c['feature_min'])+'–'+str(c['feature_max'])+'. '+t)
  if short=='bounded_batch_inference':
   keys=A['ds.orders']['rows'];chunks=[len(keys[i:i+c['chunk_size']]) for i in range(0,len(keys),c['chunk_size'])]
   edit('tb4',lambda t:'The '+str(len(keys))+' keyed orders progress in chunks of '+', '.join(map(str,chunks))+'. '+t)
  if short=='service_telemetry':
   probe=mp['probe']
   edit('tb4',lambda t:t.replace('Preserve all attempts from the prescribed half-open probe window.','Retain '+str(probe['attempt_count'])+' attempts at '+str(probe['rate_per_second'])+' valid request per second in '+probe['window']+' seconds.'))
   edit('tb5',lambda t:t.replace('stated deadline',str(probe['deadline_seconds'])+'-second deadline').replace('full probe denominator',str(probe['attempt_count'])+'-attempt denominator'))
  if short=='inference_batching_decision':
   edit('tb5',lambda t:'The registered batching objective is p'+str(mp['declared_percentile'])+' ≤ '+str(mp['batching']['maximum_p99_seconds'])+' '+mp['units']+'. '+t)
# Compact, scoped remediation content. All IDs and measured scopes are taken from the plan.
# These are re-teaching contrasts, not interaction answer keys.
rem_text={
('prediction_schema_validation','check'):[
'Contrast parsing success with schema acceptance in the same order fixture. Serialize structured values with json.dumps, send encoded bytes using urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), and read with urlopen using the stated timeout. Decode with json.loads before field checks. Assert declared valid, boundary and failure predicates; a false assert raises AssertionError in ordinary non-optimized execution.'],
('prediction_schema_validation','hands_on'):[
'Contrast a valid order request with a parseable but malformed one. Decode JSON into Python values; compare required/supplied keys, declared types and numeric boundaries. The request schema specifies features and permitted values; the response schema specifies output structure. Build the declared NumPy matrix and inspect rank, width and output-row alignment. Reject invalid input explicitly instead of predicting successfully.',
'Use json.dumps for serialization and json.loads before field checks. Send encoded JSON bytes with urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST") and urlopen with the stated timeout. Assert valid, boundary and failure predicates; false assertions raise AssertionError during ordinary non-optimized execution.'],
('online_prediction_contract','check'):[
'Contrast the supplied bounded fixture with a production-server recommendation: http.server is not recommended for production. On the existing runtime, construct HTTPServer((host, port), Handler) using the configured host/port and call serve_forever(); do not create a new platform.'],
('online_prediction_contract','hands_on'):[
'Contrast a complete response with a printed prediction in the same bounded fixture. Subclass BaseHTTPRequestHandler and implement do_POST. Read the declared body length from headers and those bytes from rfile, then decode and validate. Apply already fitted preprocessing/model without fitting or updating either.',
'Encode the named response dictionary with json.dumps(...).encode("utf-8"). Write send_response, send_header for Content-Type and encoded body length, end_headers, then body bytes to wfile. Construct HTTPServer((host, port), Handler) with configured host/port and serve_forever() on the existing runtime. http.server is not recommended for production. Assert valid, boundary and failure predicates; false asserts raise AssertionError in ordinary non-optimized execution.'],
('bounded_batch_inference','check'):[
'Contrast a correct persisted order fixture with a missing or duplicate output. Assert the declared valid, boundary and failure predicates: a false predicate raises AssertionError during ordinary non-optimized execution. A row-count check alone cannot establish key correspondence.'],
('bounded_batch_inference','hands_on'):[
'Contrast complete key coverage with equal output row counts: duplicates can hide missing results. Use a format-appropriate bounded reader such as pd.read_csv(path, chunksize=declared_rows). Apply the unchanged fitted preprocessing/model to each chunk. Carry each observation key beside its prediction and verify one result per eligible key, not output order.',
'Use explicit with open(...) handles and write each bounded result set before reading the next chunk. Serialize in the declared format, then decode the persisted fixture to verify schema and alignment. Assert valid, boundary and failure predicates; false assertions raise AssertionError during ordinary non-optimized execution.'],
('model_service_readiness','check'):[
'Contrast process startup with inspection of the referenced fixture container. Start it with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE using declared nonsecret settings. Inspect image identity and State using docker container inspect NAME. Inspect captured stdout/stderr with docker container logs NAME for initialization or execution failures.'],
('model_service_readiness','hands_on'):[
'Contrast the model-only fixture with both fitted objects usable. Readiness succeeds only when the loaded model can accept inference, not merely after process startup. In do_GET, return non-ready until model and preprocessor are initialized; then return success. Serialize JSON and test status plus decoded state before/after initialization. The health endpoint must meet the runtime contract; SageMaker uses /ping. Configure command, interval, timeout and retries, then inspect health with docker inspect and ensure unready fixtures fail.',
'Start the referenced image with docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE using declared nonsecret settings. Inspect image identity/State with docker container inspect NAME and initialization/execution output with docker container logs NAME. Assert valid, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution.'],
('deployment_configuration_code','check'):[
'Contrast an edited deployment file with configuration recorded under the existing repository workflow. Create the branch using git checkout -b BRANCH, commit the verified configuration, then merge that branch under the supplied workflow. The same order deployment remains the bounded task.'],
('deployment_configuration_code','hands_on'):[
'Contrast a parsed file with a verified recreated deployment. Declare the recorded immutable image, nonsecret environment, HOST:CONTAINER ports, supported deploy.replicas and deploy.resources.limits.cpus/memory. Reference secrets in services.prediction.secrets and top-level secrets.credential.environment by injected host variable name, never literal value. Dockerfile ARG/ENV persist secrets in image/metadata; use runtime secrets. Validate resolved fields with docker compose -f CONFIG_PATH config, apply with up -d, then inspect containers and running image identity.',
'On the authorized VM, use gcloud compute instances start/stop INSTANCE --zone=ZONE, wait and inspect resulting state. Use describe before/after and ssh on the running VM. Create the branch with git checkout -b BRANCH, commit verified configuration and merge in the existing workflow. Destroy only the test deployment with docker compose -f CONFIG_PATH down, reapply the same file and verify identical identity/settings.',
'With PyYAML, yaml.safe_dump(config, file_handle) writes mappings/lists; yaml.safe_load(file_handle) reloads them. Inspect required fields before application. Safe loading accepts standard tags, not arbitrary Python constructors. Resource deploy fields require runtime support.'],
('deployment_verification','check'):[
'Contrast launch success with release acceptance in the same fixture. Verify the recorded artifact/configuration in the existing environment and compare running identity/State, including Health when configured. Call readiness and prediction with bounded timeouts; inspect status and payload contracts and the small fixture’s output shape/values. Assert valid, boundary and failure predicates; false assertions raise AssertionError during ordinary non-optimized execution. Correct-looking predictions do not repair an identity mismatch.'],
('deployment_verification','hands_on'):[
'Contrast plausible predictions with verified release identity. Start the recorded image using docker run --name NAME -p HOST_PORT:CONTAINER_PORT --env KEY=VALUE IMAGE with declared nonsecret settings. Verify the same artifact/configuration in the existing environment. Use docker container inspect NAME for identity/State and configured Health; docker container logs NAME reveals captured initialization/execution failures. Keep credentials and sensitive requests out of evidence.',
'Call readiness/prediction with bounded timeouts. Serialize with json.dumps; send encoded bytes via urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST") and read with urlopen using the stated timeout. Decode with json.loads before checks. Verify status, payload, small-fixture output shape and declared values. Assert valid, boundary and failure predicates; false assertions raise AssertionError in ordinary non-optimized execution.'],
('prediction_authentication','check'):[
'Contrast an authorized request with a verified-but-unpermitted subject in the same protected fixture. Import GoogleAuthError from google.auth.exceptions; catch verification ValueError or GoogleAuthError and raise PermissionError into the harness denial path before prediction. ValueError signals verification failure; GoogleAuthError includes invalid issuer. Deny missing/invalid credentials and unpermitted subjects without prediction. Failures should be visible in logs, but tokens, credential literals and protected request values must not appear.'],
('prediction_authentication','hands_on'):[
'Contrast authenticated identity with prediction permission. Keep credentials runtime-secret-referenced, available only to the permitted service, separate from nonsecret authentication settings. Author named Compose services with required indented mappings/lists, immutable image, HOST:CONTAINER ports and nonsecret environment. Validate resolved fields with docker compose -f CONFIG_PATH config before up -d; inspect containers. With PyYAML, safe_dump mappings/lists, safe_load and inspect required fields; standard tags are accepted, not arbitrary Python constructors.',
'Import id_token from google.oauth2, requests from google.auth.transport and GoogleAuthError from google.auth.exceptions. In authorize_prediction(token, expected_audience, permitted_subjects), deny missing tokens, call id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience), then require verified claims["sub"] in permitted_subjects; otherwise raise PermissionError. Use verified sub, not unverified decode or email. Catch (ValueError, GoogleAuthError) into PermissionError before prediction; GoogleAuthError includes invalid issuer. Test authorized, missing, invalid and verified-but-unpermitted paths without predicting or logging tokens on denial.',
'Assert declared valid, boundary and failure predicates. False assertions raise AssertionError in ordinary non-optimized execution.'],
('service_telemetry','check'):[
'Contrast all external order-probe attempts with handler-only records. Retain timestamped success/error/timeout outcomes and durations. Availability uses the full prescribed denominator, including connection-refused and timeout attempts without handler records. Reconcile absent handler records with external failures; report window, numerator and denominator alongside handler timing/statistics and status counts.'],
('service_telemetry','hands_on'):[
'Contrast client availability with handler success rate. Choose client-visible outcomes/latency, not container or CPU state alone. Measure elapsed time using time.perf_counter() after completion minus start in one unit. Record timestamped success/error/timeout evidence; divide successes or errors by the same eligible-attempt denominator/window, retaining failures.',
'Time handler JSON decoding, prediction and response encoding, including handled errors; record durations/status counts. Use np.mean for selected observations and np.std(..., ddof=0) for the N divisor before the square root; use ddof=1 only when N−1 is required. Keep the prescribed half-open probe schedule. Count only HTTP 200 with valid prediction within the deadline, allow the final attempt its full deadline, and include refusals/timeouts without handler records. Reconcile missing records and report window, numerator/denominator and handler statistics.'],
('prediction_load_test','check'):[
'Contrast the fixed valid-traffic load fixture with intentional malformed tests. Exercise the declared arrival/concurrency profile for a bounded duration, recording client outcomes and response times. Keep malformed JSON assertions outside capacity measurement. At each offered load preserve valid payload mix, warm-up and measurement duration; retain successes, HTTP errors, timeouts and other failures separately.'],
('prediction_load_test','hands_on'):[
'Contrast offered arrivals with completed successful work in the same fixed-load fixture. Use the declared arrival/concurrency profile, valid payload mix, warm-up and duration; record outcomes and response times. Count success/error/timeout/other failures separately. Success probability and failed fraction divide their respective counts by all eligible attempts, including timeouts.',
'Use np.percentile(completed_latency_values, declared_percentile), retaining convention, successful-response sample count and time unit; this population does not represent every attempt. Successful throughput divides completed successes by elapsed time, not offered arrivals. Inspect backlog/unfinished work throughout. Accept only stable loads meeting fixed success, tail-latency, error and throughput objectives; report highest measured successful throughput or no feasible envelope.'],
('inference_batching_decision','check'):[
'Contrast start-to-response timing with the post-wait execution interval for the same identified trace request. Match each successful decoded response to request identity and batching setting. Measure response completion minus request start in one unit, including waiting. Use np.percentile(latencies, declared_percentile) with explicit convention and successful-response sample count. Compare the same trace/population interpretation and choose only a measured batching limit meeting the latency objective.'],
('serving_worker_concurrency','check'):[
'Contrast an intended worker limit with the runtime it configures. Set the existing YAML worker-limit field and validate its parsed value. Apply the referenced image/settings with docker compose -f CONFIG_PATH up -d, then inspect resulting containers. Configuration alone does not prove the bound was honored.'],
('serving_worker_concurrency','hands_on'):[
'Contrast configured worker intent with actual prediction-worker evidence. Author named Compose services using required mappings/lists, immutable image, HOST:CONTAINER ports and declared nonsecret environment. Run docker compose -f CONFIG_PATH config and compare resolved fields with the contract. Set/validate the existing worker-limit field and run the referenced image under that bound.',
'With PyYAML, write mappings/lists via yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required fields; standard tags are accepted, not arbitrary Python constructors. During the same load interval, inspect docker container top NAME and count prediction workers, not supporting processes. Compare count against the limit for oversubscription, supported by concurrent CPU/memory measurements.'],
('serving_replica_scaling','check'):[
'Contrast intended replica policy with observed identities in the same bounded demand-change fixture. Inspect running container counts/identities before and after and compare with policy. Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect authorized instance status/identity around lifecycle actions. Restore original nonproduction replica and lifecycle settings after the check.'],
('serving_replica_scaling','hands_on'):[
'Contrast more replicas with measured objective compliance at the same load. For fixed Compose scaling, set deploy.replicas or docker compose up -d --scale SERVICE=COUNT and inspect actual count. For the supplied SageMaker target, register explicit MinCapacity/MaxCapacity and apply only supported target tracking with metric, target value and scale-in/out cooldowns.',
'Compare success, p99 and completed throughput: divide successful eligible attempts by all eligible attempts, including failures; use np.percentile(completed_latency_values, declared_percentile) with convention, sample count and units; divide completed successes by elapsed time, not arrivals. Use np.mean and np.std(..., ddof=0) for the N divisor before the square root; ddof=1 only when N−1 is required.',
'Edit YAML bounds from demand/capacity evidence; safe_dump mappings/lists, safe_load and inspect required fields before application. Safe loading accepts standard tags, not arbitrary Python constructors. Inspect container counts/identities before/after demand change and instance status/identity via gcloud compute instances describe INSTANCE --zone=ZONE around authorized lifecycle actions. Restore original nonproduction replica/lifecycle settings.'],
('model_release_rollback','resolve_approved_rollback_artifact'):[
'Contrast the approved previous order release with an unapproved latest selection. Resolve the approved registry version and its artifact, preserving approval/version identity. Use that recorded previous immutable image reference for the replacement, not a mutable or unapproved target.'],
('model_release_rollback','preserve_runtime_secret_boundary'):[
'Contrast a runtime secret reference with a credential embedded in the same release image/configuration. Dockerfile ARG and ENV can persist secrets in the final image or metadata; do not embed them. Supply sensitive values through runtime secrets, never literal Compose values.'],
('model_release_rollback','hands_on'):[
'Contrast verify-then-retire with early retirement. Start the approved replacement under its distinct container identity with required environment/published port. Compare identity and State with the intended release, including Health when configured. Inspect initialization/execution logs without recording credentials or sensitive requests. Call readiness/prediction with bounded timeouts and check status/payload contracts, including the prediction/version response.',
'Serialize with json.dumps, send encoded JSON bytes using urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST"), and read through urlopen with the stated timeout. Decode with json.loads before field checks. Verify restored readiness and bounded prediction response contract before stopping/removing only the faulty test release; preserve the approved replacement.']}
for tile,pt in zip(out['tiles'],plan['tiles']):
 scopes=[];seen=set()
 for ps in pt['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  cid=ps['concept_ids'][0];scope=(cid,tuple(sorted(ps['fact_ids'])))
  if scope in seen:continue
  seen.add(scope);scopes.append(ps)
 for rem,ps in zip(tile['remediation_steps'],scopes):
  short=ps['concept_ids'][0].split('.')[-1];key=ps['type']
  if short=='model_release_rollback' and key=='check':key=ps['anchors'][0].split(':')[-1]
  snippets=rem_text[(short,key)]
  rem['blocks']=[]
  for text in snippets:
   # Split before crossing the 90-word prose cap. No claim is clipped.
   sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text);chunks=[];acc=''
   for sentence in sentences:
    if len((acc+' '+sentence).split())>85 and acc:chunks.append(acc);acc=''
    acc=(acc+' '+sentence).strip()
   if acc:chunks.append(acc)
   for chunk in chunks:rem['blocks'].append(prose(chunk,rem['lineage'],'mechanism'))
  if short=='service_telemetry':
   probe=json.loads(file(short,'measurement_policy.json'))['probe']
   for b in rem['blocks']:
    b['text']=b['text'].replace('full prescribed denominator',str(probe['attempt_count'])+'-attempt denominator').replace('prescribed half-open probe schedule',str(probe['rate_per_second'])+' valid request/second in '+probe['window']+' seconds, retaining all '+str(probe['attempt_count'])+' attempts').replace('within the deadline','within '+str(probe['deadline_seconds'])+' seconds')
# Re-split any augmented prose that exceeds the cap, preserving source lineage.
for tile in out['tiles']:
 for s in tile['steps']+tile['remediation_steps']:
  blocks=[]
  for b in s.get('blocks',[]):
   if b['type']!='prose' or len(b['text'].split())<=90:blocks.append(b);continue
   parts=re.split(r'(?<=[.!?])\s+(?=[A-Z])',b['text']);acc=''
   for part in parts:
    if len((acc+' '+part).split())>85 and acc:
     nb=copy.deepcopy(b);nb['text']=acc;blocks.append(nb);acc=''
    acc=(acc+' '+part).strip()
   if acc:nb=copy.deepcopy(b);nb['text']=acc;blocks.append(nb)
  if 'blocks' in s:s['blocks']=blocks
# Next idea after this batch is looked up in glossary name order, not invented.
last=out['tiles'][-1]['steps'][-1]
keys=list(glossary['names']);next_cid=keys[keys.index(plan['tiles'][-1]['concept_ids'][-1])+1]
last['blocks'][-1]['title']=glossary['names'][next_cid]
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Refined',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediations')
