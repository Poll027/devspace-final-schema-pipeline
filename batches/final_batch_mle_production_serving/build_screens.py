import json, re, copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_serving')
p=json.loads((B/'tile_plans.json').read_text()); g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); r=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']}; assets={a['asset_id']:a for a in r['assets']}
def file(aid,path): return next(f['content'] for f in assets[aid]['files'] if f['path']==path)
contract=json.loads(file('ws.prediction_schema_validation','contract.json'))
policy=json.loads(file('ws.service_telemetry','measurement_policy.json'))
# Short independent examples: no computed output or production deployment claims.
examples={
'prediction_schema_validation': 'In the order fixture, decode the body before checking required keys, numeric types, permitted bounds and matrix dimensions. Check the decoded response separately for required output keys and one output per request row. A missing key must be rejected before prediction; an included boundary and a value beyond it are different test cases. Serialize the request, send encoded bytes with the JSON header and stated timeout, then decode the response. Parsing, schema acceptance and output correctness are separate assertions.',
'online_prediction_contract': 'Trace the supplied request through do_POST: read the declared byte count, decode JSON, validate, then apply the fitted preprocessor and model without updates. Serialize and UTF-8 encode the response before setting its status, content type and byte length. Finish the headers before writing to wfile. The encoded body determines its length, not an assumed character count. Exercise valid, boundary and malformed fixtures on the configured HTTPServer; this bounded demonstration does not prescribe a production server.',
'bounded_batch_inference': 'Use the declared chunk size for orders.csv. Keep each order_id beside its prediction, serialize that chunk, then read the next one using the same fitted objects. Reopen and decode the written fixture to inspect schema and eligible-key correspondence. A duplicate output key and a missing key can leave the total row count unchanged. Verify coverage and uniqueness rather than incidental output order, retaining explicit input and output handles.',
'model_service_readiness': 'Start the referenced image with its declared runtime settings. Inspect identity, State and initialization logs. Before both fitted objects initialize, the readiness route must return the declared non-ready status and JSON state. After initialization, check success status and decoded readiness state together. Configure the readiness healthcheck command, interval, timeout and retries, and inspect its result. Process startup alone cannot pass the ready fixture.',
'deployment_configuration_code': 'In the fixture, configure the approved immutable image, declared port mapping, supported replica count and resource bounds. Safely reload the YAML and inspect compose config before applying it. Compare the running image with the recorded artifact, then commit the verified configuration through the existing branch and merge workflow. Destroy only the test deployment, reapply the same file and verify identical identity and settings. Use only authorized VM lifecycle and connection actions. Secret references name injected variables, never credential values.',
'deployment_verification': 'Inspect the named fixture container against the release record: image, State and Health when configured. Review initialization and execution logs without copying sensitive requests or credentials. Call readiness and prediction with stated timeouts, sending encoded JSON and decoding the response. Verify status, output shape and declared values with assertions. Plausible predictions do not repair an image-identity mismatch; retain separate identity, initialization and contract checks.',
'prediction_authentication': 'Use the supplied audience and permitted-subject policy. Reject a missing token; verify an offered token, then check verified sub membership. A verified but unpermitted subject is denied too. Convert declared verification exceptions into the denied HTTP path before prediction. Safely inspect Compose image, ports, nonsecret settings and runtime secret references. Test authorized, missing, invalid and unpermitted fixtures. Denied requests must neither execute prediction nor disclose tokens in logs.',
'service_telemetry': 'For the prescribed probe, retain every scheduled attempt, including connection refusals and timeouts with no handler record. Count only valid successful predictions received by the deadline, allowing the final attempt its full deadline before summarizing. Report the window, successful-deadline numerator and full attempt denominator. Reconcile missing handler events with external failures. Handler timing covers JSON decoding, prediction and encoding, including handled error paths; its success rate alone is not client-visible availability.',
'prediction_load_test': 'Inspect the registered valid-traffic attempts alongside unfinished work. Keep HTTP errors, timeouts and other failures separate, but include all valid attempts in success and failed-fraction denominators. Calculate successful completions per measurement time, not arrivals per time. Percentiles describe completed-response samples with declared units and convention, not timed-out responses. Accept only stable-backlog points meeting all declared latency, error and throughput objectives, or report no feasible measured envelope. Intentional malformed fixtures stay outside this capacity population.',
'inference_batching_decision': 'For each registered trace row, decode the successful response and match its request identity and batching setting before calculating duration. Measure request start through response completion, including the waiting interval. Compute the declared percentile, mean and spread over matched successful responses, retaining units, convention and sample count. Compare settings using that same population interpretation and choose only a measured limit meeting the objective. A shorter execution interval cannot compensate for a full request interval that misses the latency limit.',
'serving_worker_concurrency': 'Edit the existing worker bound, safely reload it and inspect the Compose-resolved value before applying the referenced image. During the authorized load interval, inspect prediction-worker processes and compare their count with the configured limit. Record CPU and memory in that same interval. A parsed bound is intent; excess observed workers are oversubscription even when configuration validation succeeds. Keep authored settings, reloaded settings and actual process evidence distinct.',
'serving_replica_scaling': 'For the fixed fixture, declare the permitted replica count and compare intended versus observed container identities before and after the bounded demand change. A supplied SageMaker target instead retains explicit capacity bounds, metric target and cooldowns. Compare success, tail latency and successful throughput at the same load and sample conventions. Safely inspect the changed YAML before application; inspect runtime identity and lifecycle state afterward. Restore the original nonproduction replica and lifecycle settings. More replicas alone do not establish an acceptable setting.',
'model_release_rollback': 'Keep the faulty test release running while starting the approved previous release under its distinct identity and published port. Resolve the recorded immutable artifact rather than latest. Inspect replacement State, available Health and sanitized logs. With bounded calls, verify readiness and decoded JSON prediction/version against the contract. Only then stop and remove the faulty test release, preserving the replacement. Keep credentials runtime-injected, not in image metadata, Compose values or evidence.'}
intros={
'prediction_schema_validation':'Parseable JSON can still violate a prediction contract. Decode first; acceptance also needs field, value and response-alignment checks.',
'online_prediction_contract':'This bounded HTTP fixture carries validated data through existing fitted prediction state. It is not a production-server design.',
'bounded_batch_inference':'Bounded chunks still need stable observation identity. Keep keys with predictions and reuse fitted state.',
'model_service_readiness':'A running process may still lack initialized prediction assets. Readiness must describe whether inference can be accepted.',
'deployment_configuration_code':'Prepare repeatable configuration before applying it. Separate nonsecret settings from runtime secret references.',
'deployment_verification':'A launch message is not release acceptance. Verify identity, execution state and bounded endpoint behavior.',
'prediction_authentication':'Verify who the caller is, then whether that identity may predict. Neither check replaces runtime-secret handling.',
'service_telemetry':'Client outcomes can differ from handler records. Reconcile external requests with handler timing, including attempts that never arrived.',
'prediction_load_test':'Measure a capacity envelope from client outcomes, tail latency, completed work and backlog at each declared load.',
'inference_batching_decision':'Batch waiting belongs in full request latency. Match each response to its request and setting first.',
'serving_worker_concurrency':'A worker limit in YAML is intent. Inspect whether running workers honor it during the bounded load.',
'serving_replica_scaling':'More replicas are not automatically better. Compare client outcomes at equal load under explicit capacity bounds.',
'model_release_rollback':'Resolve the approved previous artifact. Verify its replacement service before retiring the faulty test release.'}
def revoice(text):
    replacements={
      'Use the recorded immutable image digest in the deployment instead of a mutable tag that can later resolve to different contents.':'Pin deployment to the recorded immutable image digest; a mutable tag may later resolve to different contents.',
      'A prediction request schema declares the expected features, their types and permitted values, and a response schema declares the expected output structure.':'The request schema specifies features, types and permitted values; the response schema specifies output structure.',
      'Decode the incoming JSON into Python values before validating field presence and value types; raw JSON text is not the structured request.':'Decode JSON into Python values before checking field presence and types. Raw text is not the structured request.',
      'Compare required and supplied key sets, then check each value’s declared type or numeric boundary with conditional predicates.':'Compare required versus supplied key sets, then test declared types and numeric boundaries with conditional predicates.',
      'Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.':'Assert the declared valid, boundary and failure predicates. In ordinary non-optimized execution, a false assertion raises AssertionError.',
      'Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.':'Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations.',
      'Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.':'Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only when the declared calculation requires N−1.',
      'Use json.dumps to encode structured request/response values and json.loads to decode JSON before checking their fields.':'Serialize structured request/response values with json.dumps; decode JSON with json.loads before inspecting fields.',
      'rather than treating process startup alone as model readiness':'not merely after process startup',
      'rather than assuming more replicas are always better':'not merely more replicas',
      'rather than equating arrivals with completed work':'not arrivals',
      'rather than requiring it all in memory':'without loading the entire dataset at once',
      'without fitting new state during inference':'without refitting during inference',
      'Do not embed secrets in Dockerfile ARG or ENV instructions, because they persist in the final image or its metadata.':'Keep secrets out of Dockerfile ARG and ENV: they persist in the final image or its metadata.',
      'Supply sensitive values through the runtime secret mechanism rather than placing their literal values in the Compose configuration.':'Deliver sensitive values through runtime secrets, never as literal Compose values.',
      'Safe loading accepts standard YAML tags, not arbitrary Python object constructors.':'Safe loading supports standard YAML tags, not arbitrary Python object constructors.'}
    for old,new in replacements.items(): text=text.replace(old,new)
    return text

def lin(cids,tbs=(),facts=(),anchors=()):return dict(concept_ids=list(cids),teaching_block_ids=list(tbs),fact_ids=list(facts),anchors=list(anchors))
def prose(text,lineage,role='mechanism'):
    # Keep sentences together only up to 80 words; never split code syntax on dots.
    sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text.replace('\n\n',' '))
    chunks=[]; current=''
    for sent in sentences:
        if current and len((current+' '+sent).split())>80:chunks.append(current);current=''
        current=(current+' '+sent).strip()
    if current:chunks.append(current)
    assert all(len(c.split())<=90 for c in chunks),(text,chunks)
    return [dict(type='prose',text=c,role=role,lineage=copy.deepcopy(lineage)) for c in chunks]

def tb_blocks(cid,bid):
    bundle=bundles[cid];tb=next(t for t in bundle['teaching_blocks'] if t['id']==bid); short=cid.split('.')[-1]
    lineage=lin([cid],[cid+'#'+bid],[cid+'#'+f for f in tb['fact_ids']])
    if tb['purpose']=='intro':return prose(intros[short],lineage,'intro')
    if tb['purpose']=='example':return prose(examples[short],lineage,'example')
    if tb['purpose']=='misconception':return prose(revoice(tb['content']),lineage,'misconception')
    # Mechanisms teach each fact explicitly, not by relying on media or visuals.
    facts={f['id']:f['statement'] for f in bundle['coverage']['required_facts']}
    result=[]
    for fid in tb['fact_ids']:
        result+=prose(revoice(facts[fid]),lin([cid],[cid+'#'+bid],[cid+'#'+fid]), 'definition' if tb['purpose']=='definition' else 'mechanism')
    return result

def table(aid,lineage,caption,columns=None):
    ref={'asset_id':aid}
    if columns:ref['columns']=columns
    return dict(type='data_table',asset_ref=ref,caption=caption,lineage=copy.deepcopy(lineage))
def diagram(labels,lineage,title):
    nodes=[{'id':f'n{i}','label':label} for i,label in enumerate(labels)]
    return dict(type='diagram',diagram_kind='sequence',title=title,nodes=nodes,edges=[{'from':nodes[i]['id'],'to':nodes[i+1]['id'],'directed':True} for i in range(len(nodes)-1)],alt_text=' → '.join(labels),lineage=copy.deepcopy(lineage))
def code(text,lineage):return dict(type='code_walkthrough',language='python',code=text,reveal='all',lineage=copy.deepcopy(lineage))

def visual(cid,typ,lineage):
    short=cid.split('.')[-1]; vl=copy.deepcopy(lineage);vl['anchors']=[cid+'#visual']
    if short=='prediction_schema_validation':
        text='''# Symbolic checks against the supplied contract, not computed output.
body = json.dumps(request_values).encode("utf-8")
request = json.loads(body)
assert set(request) == set(contract["request_keys"])
values = reject_malformed(request)  # checks declared types and bounds
matrix = np.array(values, dtype=contract["numpy_dtype"])
assert matrix.ndim == contract["matrix_rank"]
assert matrix.shape[1] == contract["matrix_width"]
response = json.loads(response_body)
assert set(response) == set(contract["response_keys"])
assert len(response["predictions"]) == matrix.shape[0]
# Use valid, boundary and rejected fixtures; decoding alone is not acceptance.'''
        return code(text,vl)
    if short=='online_prediction_contract':
        labels=['do_POST: declared Content-Length → rfile bytes','Decode JSON; reject schema failures','Validated input → fitted transform and predict; no fitting','json.dumps → UTF-8 bytes','Status; Content-Type; encoded Content-Length; end_headers','wfile body; valid/boundary/failure assertions']
        nodes=[{'id':f'n{i}','label':label} for i,label in enumerate(labels)]
        return dict(type=typ,nodes=nodes,edges=[{'from':nodes[i]['id'],'to':nodes[i+1]['id']} for i in range(len(nodes)-1)],direction='TB',alt_text=' → '.join(labels),lineage=vl)
    if short=='bounded_batch_inference':
        return code('''# Context: json, pandas as pd, contract and fitted objects are supplied.
with open(contract["batch_input_path"]) as source, open(contract["batch_output_path"], "w") as target:
    for chunk in pd.read_csv(source, chunksize=contract["chunk_size"]):
        values = preprocessing_pipeline.transform(chunk[contract["feature_names"]])
        predictions = model.predict(values)
        for key, prediction in zip(chunk[contract["batch_key"]], predictions):
            record = {contract["batch_key"]: key, "prediction": float(prediction), "version": contract["version"]}
            target.write(json.dumps(record) + "\\n")
# Reopen, decode, assert schema and one result per eligible input key.
# Matching row counts alone cannot detect duplicate-plus-missing keys.''',vl)
    if short=='model_service_readiness':
        return dict(type='before_after',before=diagram(['Process started','Either fitted model or preprocessor uninitialized','Non-ready HTTP status '+str(contract['not_ready_status'])+'; decoded JSON '+json.dumps(contract['not_ready_payload'])],vl,'Before initialization'),after=diagram(['Both fitted objects initialized; inference accepted','Successful HTTP status '+str(contract['success_status'])+'; decoded JSON '+json.dumps(contract['ready_payload']),'Inspect configured healthcheck result'],vl,'After initialization'),change_summary='Initialization, not process startup, is the readiness boundary. Inspect the configured command, interval, timeout and retries.',lineage=vl)
    if short=='deployment_configuration_code':
        return dict(type=typ,left=diagram(['Recorded immutable image','HOST:CONTAINER ports; nonsecret environment','Runtime secret-variable reference','Supported replica/resource bounds','Safely reloaded YAML → compose config'],vl,'Authored configuration'),right=diagram(['compose up -d','Inspect running image and State','Compare actual identity and runtime settings','Destroy only test deployment; reapply same file','Verify identical artifact and resolved settings'],vl,'Observed runtime'),left_label='Configuration intent',right_label='Running evidence',takeaway='Parsed configuration is not proof of running identity; runtime support for deploy fields must be checked.',lineage=vl)
    if short=='deployment_verification':
        # Copy registered transport, not an invented response or its output.
        text=file('ws.deployment_verification','transport.py')
        return code(text,vl)
    if short=='prediction_authentication':
        text='''from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError

def authorize_prediction(token, expected_audience, permitted_subjects):
    if not token:
        raise PermissionError("missing credential")
    try:
        claims = id_token.verify_oauth2_token(token, requests.Request(), audience=expected_audience)
    except (ValueError, GoogleAuthError):
        raise PermissionError("verification failed") from None
    if claims["sub"] not in permitted_subjects:
        raise PermissionError("unpermitted subject")
    return claims
# Harness maps PermissionError to denial before prediction.
# Log failure classes only, never the token or protected request values.'''
        return code(text,vl)
    if short=='service_telemetry':return table('ds.serving_attempts',vl,'Authored offline attempts: reconcile client outcomes with handler timestamps and absent handler records. These are not production measurements.')
    if short=='prediction_load_test':return table('ds.serving_attempts',vl,'Authored offline attempts include multiple experiment settings. Select the declared valid-traffic load population before calculating capacity; retain errors and timeouts.')
    if short=='inference_batching_decision':
        return diagram(['Decode successful response; match request_id and batching_setting','request_start_seconds','batch_wait_end_seconds: waiting ends','response_complete_seconds: full duration ends','Matched successful population → declared percentile, mean and spread','Compare same population; choose only a limit meeting the objective'],vl,'End-to-end batching latency includes waiting')
    if short=='serving_worker_concurrency':
        config=json.loads(file('ws.serving_worker_concurrency','original_config.json'))
        return dict(type=typ,left=code('# Supplied original configuration (intent, not process evidence)\nconfig = '+repr(config),vl),right=table('ds.worker_processes',vl,'Authored process evidence: distinguish prediction workers from supervisor processes; align interval_id with resource observations.'),left_label='Configured worker bound',right_label='Observed processes under load',takeaway='Safely reload and resolve the changed worker limit, then compare actual prediction workers with that bound and inspect same-interval CPU/memory.',lineage=vl)
    if short=='serving_replica_scaling':
        return dict(type='before_after',before=diagram(['Original replica and lifecycle settings','Record container count and identities','Inspect authorized instance status and identity'],vl,'Before bounded scaling'),after=diagram(['Parsed bounded replica policy applied','Inspect count, identities and lifecycle state after bounded demand/action','Compare same-load success, tail latency and throughput','Restore original replica and lifecycle settings'],vl,'After bounded scaling and restoration'),change_summary='Intended replica settings and observed capacity are different evidence. Increase capacity only within supplied bounds and service objectives.',lineage=vl)
    if short=='model_release_rollback':
        return dict(type='before_after',before=table('ds.release_records',vl,'Authored approval records identify the previous immutable replacement; the faulty test release is still running.'),after=table('ds.release_transition',vl,'Authored chronology, not live command evidence: replacement is verified before faulty-release retirement.'),change_summary='Start the approved replacement under its distinct identity; inspect State, available Health and sanitized logs, then verify readiness and decoded prediction/version before stopping and removing only the faulty test release.',lineage=vl)
    raise ValueError(cid)

takeaways={
'prediction_schema_validation':'Decoding is not schema acceptance; request validity and response row alignment need separate checks.',
'online_prediction_contract':'A bounded http.server fixture is not a production recommendation; return status, headers and encoded body.',
'bounded_batch_inference':'Preserve keys and fitted state. Matching row counts do not prove one output per eligible key.',
'model_service_readiness':'Running is not ready. Verify initialized assets, HTTP status and decoded readiness state.',
'deployment_configuration_code':'A mutable tag is not immutable identity. Parsed settings do not prove running state or deploy-field support.',
'deployment_verification':'Launch success is not verification; check intended artifact, runtime configuration and prediction contract.',
'prediction_authentication':'Verified identity still needs permission. Never put credential values in YAML or logs.',
'service_telemetry':'Handler success rate is not client availability; retain attempts that never reached the handler.',
'prediction_load_test':'Arrivals are not completions; timeouts and growing backlog cannot be hidden by low completed-response latency.',
'inference_batching_decision':'Include batch waiting in full request latency; fast execution alone does not meet the objective.',
'serving_worker_concurrency':'Configuration is intent. Compare observed workers and same-interval resource evidence with the declared bound.',
'serving_replica_scaling':'More replicas are not guaranteed to pass; distinguish intended counts, observed counts and completed throughput.',
'model_release_rollback':'Rollback preserves approved immutable identity. Verify the replacement before retiring only the faulty test release.'}

out={k:p[k] for k in ('schema_version','path_id','batch_id')};out['kind']='screens_part';out['tiles']=[]
for tile in p['tiles']:
    names=[bundles[c]['context']['concept_name'] for c in tile['concept_ids']]
    titles={
        'mle.tile.060_063':'Validate and serve fitted predictions',
        'mle.tile.064_065':'Reproduce and verify a serving release',
        'mle.tile.066_067':'Protect predictions and measure client outcomes',
        'mle.tile.068_071':'Measure and bound serving capacity',
        'mle.tile.072_072':'Restore an approved serving release'}
    t={'tile_id':tile['tile_id'],'title':titles[tile['tile_id']],'steps':[],'remediation_steps':[]}
    for s in tile['steps']:
        sl=lin(s['concept_ids'],s['teaching_block_ids'],s['fact_ids'],s['anchors'])
        step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'lineage':sl}
        cid=s['concept_ids'][0]
        if s['type'] in ('check','hands_on'):
            step['title']=('Check: ' if s['type']=='check' else 'Practice: ')+bundles[cid]['context']['concept_name']
            step['eyebrow']='Check your decision' if s['type']=='check' else 'Bounded fixture practice'
            # The title is framing; no questions, hints or answer key here.
        elif s['type']=='recap':
            step['title']='Carry these rules forward';step['blocks']=[]
            for c in s['concept_ids']:
                bundle=bundles[c];tb=next(x for x in reversed(bundle['teaching_blocks']) if x['purpose']=='misconception')
                step['blocks']+=prose(takeaways[c.split('.')[-1]],lin([c],[c+'#'+tb['id']],[c+'#'+f for f in tb['fact_ids']]),'takeaway')
            nxt=tile.get('next_tile_id')
            next_plan=next((tt for tt in p['tiles'] if tt['tile_id']==nxt),None)
            if next_plan:next_name=bundles[next_plan['concept_ids'][0]]['context']['concept_name']
            else:
                # Next idea's name is supplied by the glossary name bank, not a new teaching claim.
                order=list(g['names']);next_name=g['names']['mle.dataset_quality_gate']
            step['blocks'].append({'type':'up_next','title':next_name})
        elif s['type']=='video':
            step['title']='Review the supporting segment';step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
        else:
            first=next(x for x in bundles[cid]['teaching_blocks'] if cid+'#'+x['id']==s['teaching_block_ids'][0])
            title_by_purpose={'intro':bundles[cid]['context']['concept_name'],'definition':'The contract to check','mechanism':'Apply and verify','example':'Trace the order fixture','misconception':'Keep this distinction clear'}
            step['title']=title_by_purpose[first['purpose']];step['blocks']=[]
            for tbid in s['teaching_block_ids']:
                c,bid=tbid.split('#');step['blocks']+=tb_blocks(c,bid)
            if s['planned_visual_block_type']:
                step['blocks'].append(visual(cid,s['planned_visual_block_type'],sl))
                vl=copy.deepcopy(sl);vl['anchors']=[cid+'#visual'];short=cid.split('.')[-1]
                if short=='bounded_batch_inference':
                    step['blocks'].append(table('ds.orders',vl,'Authored keyed input: retain observation identity across the declared bounded chunks.'))
                elif short=='model_service_readiness':
                    step['blocks'].append(table('ds.readiness_cases',vl,'Authored initialization cases: both fitted assets must be usable; initialization failure cannot pass readiness.'))
                elif short=='prediction_load_test':
                    step['blocks'].append(table('ds.backlog',vl,'Authored unfinished-work observations for the same fixed load settings; inspect change across the measurement window.'))
                elif short=='inference_batching_decision':
                    trace=assets['ds.batching_trace'];columns=[c['name'] for c in trace['columns']]
                    example=next(dict(zip(columns,row)) for row in trace['rows'] if row[columns.index('batching_setting')]==policy['batching']['settings'][-1] and row[columns.index('success')])
                    timing=diagram([f"{example['request_id']} / {example['batching_setting']}",f"Start: {example['request_start_seconds']} seconds",f"Batch wait ends: {example['batch_wait_end_seconds']} seconds",f"Response completes: {example['response_complete_seconds']} seconds"],vl,'One matched request: full start-to-response interval')
                    step['blocks'].append(timing)
                    step['blocks'].append(table('ds.batching_trace',vl,'Authored trace: exclude failed and unmatched responses; the full start-to-response interval includes batch waiting.'))
                    step['blocks'].append(code('wait = batch_wait_end_seconds - request_start_seconds\npost_wait = response_complete_seconds - batch_wait_end_seconds\nend_to_end = response_complete_seconds - request_start_seconds\n# Compute summaries over matched successful decoded responses only.\ntail = np.percentile(latencies, declared_percentile)\nmean = np.mean(latencies)\nspread = np.std(latencies, ddof=0)',vl))
                elif short=='serving_worker_concurrency':
                    step['blocks'].append(table('ds.worker_resources',vl,'Authored CPU/memory observations: align interval_id with the process evidence.'))
                    step['blocks'].append(code('import json, yaml\nwith open("runtime_contract.json") as source:\n    runtime = json.load(source)\nservice = config["services"][runtime["SERVICE"]]\nservice["environment"][runtime["worker_limit_key"]] = str(runtime["approved_worker_limit"])\nwith open(runtime["CONFIG_PATH"], "w") as target:\n    yaml.safe_dump(config, target)\nwith open(runtime["CONFIG_PATH"]) as source:\n    reloaded = yaml.safe_load(source)\nassert int(reloaded["services"][runtime["SERVICE"]]["environment"][runtime["worker_limit_key"]]) == runtime["approved_worker_limit"]\n# Resolve with compose config; apply and compare observed workers with this bound.',vl))
                elif short=='serving_replica_scaling':
                    step['blocks'].append(table('ds.replica_states',vl,'Authored original, changed and restored phases: compare intended replicas, actual container identities and instance state.'))
                elif short in ('deployment_configuration_code','deployment_verification','model_release_rollback'):
                    step['blocks'].append(code('import json\nwith open("runtime_contract.json") as source:\n    intended = json.load(source)\n# Inspect live fixture execution separately from the intended configuration.\n# Compare container Config.Image with intended["IMAGE_DIGEST"].\n# Check State and Health when configured, plus sanitized initialization/execution logs.\n# Bounded readiness and prediction checks must verify status and decoded payload.\n# Do not interpret launch success as acceptance.',vl))
                if short=='deployment_configuration_code':
                    runtime=json.loads(file('ws.deployment_configuration_code','runtime_contract.json'))
                    config={'services':{runtime['SERVICE']:{'image':runtime['IMAGE_DIGEST'],'environment':{runtime['SETTING']:runtime['VALUE']},'ports':[str(runtime['HOST_PORT'])+':'+str(runtime['CONTAINER_PORT'])],'secrets':[runtime['secret_reference']],'deploy':{'replicas':runtime['REPLICA_COUNT'],'resources':{'limits':runtime['supported_resource_limits']}}}},'secrets':{runtime['secret_reference']:{'environment':runtime['secret_environment_variable']}}}
                    step['blocks'].append(code('# Authored intended fixture configuration; no credential literals.\nconfig = '+repr(config)+'\n# Safely write/reload; resolve fields before application.\n# Compare initial and recreated running identity/settings with this same file.',vl))
                    step['blocks'].append(diagram([f"Authorized instance: {runtime['INSTANCE']}",f"Zone: {runtime['ZONE']}",'Describe identity/status before and after authorized lifecycle action'],vl,'Authorized fixture instance, not a real cloud deployment'))

        t['steps'].append(step)
    # Separate failure destinations for distinct measured fact sets. Use plan assessment anchors
    # to reconstruct measured facts without reading another stage's interactions artifact.
    seen={}
    for s in tile['steps']:
        if s['type'] not in ('check','hands_on'):continue
        key=tuple(s['fact_ids'])
        if key in seen:continue
        cid=s['concept_ids'][0];bundle=bundles[cid]
        facts={cid+'#'+f['id']:f['statement'] for f in bundle['coverage']['required_facts']}
        tbids=[cid+'#'+tb['id'] for tb in bundle['teaching_blocks'] if set(cid+'#'+f for f in tb['fact_ids'])&set(key)]
        rid=tile['tile_id']+f'.r{len(t["remediation_steps"])+1:02d}';seen[key]=rid
        rem={'step_id':rid,'type':'remediation','required':False,'concept_ids':[cid],'title':'Try again: '+bundle['context']['concept_name'],'eyebrow':'One distinction to restore','lineage':lin([cid],tbids,key),'blocks':[]}
        contrast=next(x for x in reversed(bundle['teaching_blocks']) if x['purpose']=='misconception')
        # Teach every fact in the measured set before the contrast. Each block's ids are exact.
        for fid in key:
            teachers=[cid+'#'+tb['id'] for tb in bundle['teaching_blocks'] if fid.split('#')[1] in tb['fact_ids'] and tb['purpose'] in ('mechanism','definition')]
            rem['blocks']+=prose(revoice(facts[fid]),lin([cid],teachers,[fid]),'mechanism')
        rem['blocks']+=prose(revoice(contrast['content']),lin([cid],[cid+'#'+contrast['id']],[cid+'#'+f for f in contrast['fact_ids']]),'misconception')
        rem['lede']='Return to the same authored order-prediction fixture; keep the successful case separate from the failed contract condition.'
        rem['lineage']['fact_ids']=list(dict.fromkeys(list(key)+[cid+'#'+f for f in contrast['fact_ids']]))
        t['remediation_steps'].append(rem)
    out['tiles'].append(t)
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote screens:',len(out['tiles']),'tiles',sum(len(t['steps']) for t in out['tiles']),'steps',sum(len(t['remediation_steps']) for t in out['tiles']),'remediations')
# Checklist: exact plan, budgets, lineage, visual realization, asset columns, no outputs/media claims.
for t,pt in zip(out['tiles'],p['tiles']):
    assert len(t['steps'])==len(pt['steps'])
    for s,ps in zip(t['steps'],pt['steps']):
        assert (s['step_id'],s['type'],s['concept_ids'])==(ps['step_id'],ps['type'],ps['concept_ids'])
        for key in ['fact_ids','teaching_block_ids']:assert s['lineage'][key]==ps[key]
        if s['type'] in ('check','hands_on'):assert 'blocks' not in s
        else:
            words=sum(len(b.get('text','').split()) for b in s['blocks'])
            assert words<=ps['word_budget'],('OVER BUDGET',s['step_id'],words,ps['word_budget'])
    def walk(blocks):
        for block in blocks:
            yield block
            for key in ['before','after','left','right']:
                if key in block:yield from walk([block[key]])
    for s in t['steps']+t['remediation_steps']:
        for b in walk(s.get('blocks',[])):
            assert 'result' not in b and 'output' not in b and 'computed_values' not in b
            if b['type']=='prose':
                assert b.get('lineage') and len(b['text'].split())<=90
                assert not re.search(r'\bvideo\b',b['text'],re.I)
            if 'lineage' in b:
                for fid in b['lineage']['fact_ids']:assert '#f' in fid
                for tb in b['lineage']['teaching_block_ids']:assert '#tb' in tb
            if 'asset_ref' in b:
                a=assets[b['asset_ref']['asset_id']]
                assert all(c in [v['name'] for v in a['columns']] for c in b['asset_ref'].get('columns',[]))
    for s,ps in zip(t['steps'],pt['steps']):
        if ps['planned_visual_block_type'] not in (None,'up_next'):
            assert any(b['type']==ps['planned_visual_block_type'] and ps['concept_ids'][0]+'#visual' in b['lineage']['anchors'] for b in s['blocks'])
print('Checklist PASS: plan order, qualified lineage, framing-only checks, budgets, visual anchors, registry columns, no inline results or video references.')
