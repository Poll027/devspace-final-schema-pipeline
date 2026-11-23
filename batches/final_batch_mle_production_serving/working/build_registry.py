import csv, hashlib, io, json, re, sys
from pathlib import Path
from collections import Counter

B = Path('batches/final_batch_mle.region.production_serving')
g = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
sid = 'scenario.order_prediction_lab'
assets = []
# Mine teaching/anchor vocabulary before choosing any authored fixture values.
texts=[]
for bundle in g['bundles']:
    texts.extend(t['content'] for t in bundle['teaching_blocks'])
    texts.append(json.dumps(bundle['practice_anchor'],ensure_ascii=False))
    texts.append(json.dumps(bundle['visual_anchor'],ensure_ascii=False))
text='\n'.join(texts)
candidates=['orders','order keys','two-feature matrix','three rows','five keyed orders','two, two and one','A','B','JSON','UTF-8','Content-Type','Content-Length','POST','GET','BaseHTTPRequestHandler','HTTPServer','do_POST','do_GET','rfile','wfile','send_response','send_header','end_headers','serve_forever','NumPy','Python','pandas','pd.read_csv','chunksize','json.dumps','json.loads','np.asarray','np.mean','np.std','np.percentile','ddof=0','ddof=1','time.perf_counter','urllib.request.Request','urllib.request.urlopen','HTTPError','PyYAML','yaml.safe_dump','yaml.safe_load','Docker','docker','Compose','docker compose','docker container top','CPU','memory','SageMaker','/ping','Google','GoogleAuthError','PermissionError','ValueError','claims[\"sub\"]','expected_audience','permitted_subjects','authorize_prediction','verify_oauth2_token','Compute Engine','gcloud','git','CONFIG_PATH','NAME','SERVICE','INSTANCE','ZONE','IMAGE_DIGEST','HOST_PORT','CONTAINER_PORT','SETTING','VALUE','REPLICA_COUNT','INJECTED_SECRET_VARIABLE','credential','services.prediction','MinCapacity','MaxCapacity','p99','one replica','worker limit is two','three observed workers','300','294','0.98','100','90','six HTTP errors','four timeouts','ten-second window','1.0','1.4','1.6','0.6','0.4','0.2','two-second deadline','one valid request per second','[t0, t0+300 seconds)','approved version A','faulty test version B','numeric_values','completed_latency_values','declared_percentile']
vocab = sorted(set(x for x in candidates if x in text) | set(re.findall(r'\b(?:json|np|pd|yaml|urllib\.request|services|secrets|docker|gcloud|git|id_token|requests)\.[A-Za-z_][\w.]*',text)))

def col(name,typ,role,unit=None,description=None,label=False):
    c={'name':name,'type':typ,'semantic_role':role}
    if unit is not None:c['unit']=unit
    if description:c['description']=description
    if label:c['numeric_looking_label']=True
    return c

def ds(id,title,columns,rows,description):
    a={'asset_id':'ds.'+id,'asset_kind':'dataset','scenario_id':sid,'title':title,'description':description+' All observations are authored nonproduction fixture data, not production measurements.','columns':columns,'rows':rows,'provenance':'authored','variants':[]}
    assets.append(a);return a

def dictrows(a):return [dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
def csvtext(a):
    s=io.StringIO();w=csv.writer(s);w.writerow([c['name'] for c in a['columns']]);w.writerows(a['rows']);return s.getvalue()
def dumps(x):return json.dumps(x,indent=2,ensure_ascii=False)+'\n'
def variant(a,name,ops,kind=None,where=None,column=None,occurrence=0,rule=None):
    v={'variant_id':'variant.'+name,'derived_from':a['asset_id'],'purpose':name.replace('_',' '),'ops':ops,'planted_issues':[]}
    if kind:
        issue={'issue_id':'issue.'+name,'kind':kind,'locations':[{'where':where,'occurrence':occurrence,'column':column}],'description':'Authored '+name.replace('_',' ')+' fixture.'}
        if rule:issue['rule']=rule
        v['planted_issues'].append(issue)
    a['variants'].append(v)

orders=ds('orders','Five keyed orders',[
    col('order_id','string','identifier',description='Synthetic order identity; A and B retain the glossary key example.'),
    col('feature_1','number','numerical',description='First anonymous prediction-time feature, permitted closed interval [0, 10].'),
    col('feature_2','number','numerical',description='Second anonymous prediction-time feature, permitted closed interval [0, 10].')],
    [[k,float(i),float(i+1)] for i,k in enumerate('ABCDE',1)],
    'The glossary specifies unnamed features, not real-world feature semantics. These two anonymous feature names are the declared running contract. The first three rows are the online matrix; all five form the two-two-one batch input.')
for name,value,kind,rule in [('included_limit',10.0,None,None),('beyond_limit',11.0,'impossible_value',{'column':'feature_1','op':'gt','value':10}),('missing_feature',None,'missing_value',None),('wrong_type','not_numeric','wrong_type',{'column':'feature_1','op':'eq','value':'not_numeric'})]:
    variant(orders,name,[{'op':'set_cell','where':{'order_id':'A'},'column':'feature_1','value':value}],kind,{'order_id':'A'},'feature_1',rule=rule)
variant(orders,'duplicate_order',[{'op':'duplicate_row','where':{'order_id':'A'},'insert':'after'}],'duplicate_row',{'order_id':'A'},'order_id',1)
variant(orders,'missing_order',[{'op':'drop_rows','where':{'order_id':'B'}}])
variant(orders,'wrong_width',[{'op':'drop_columns','columns':['feature_2']}])

# A fixed, already fitted, deliberately simple package; no learner fitting is required.
frozen_source='''FEATURE_NAMES = ("feature_1", "feature_2")
class FrozenPreprocessor:
    def transform(self, values):
        return [[float(x) for x in row] for row in values]
class FrozenModel:
    def predict(self, values):
        return [row[0] + 2.0 * row[1] for row in values]
preprocessing_pipeline = FrozenPreprocessor()
model = FrozenModel()
'''
namespace={};exec(frozen_source,namespace)
def predict(matrix):return namespace['model'].predict(namespace['preprocessing_pipeline'].transform(matrix))
matrix=[r[1:] for r in orders['rows'][:3]]
request={'features':matrix}
response={'predictions':predict(matrix),'version':'A'}
outputs=[{'order_id':r[0],'prediction':predict([r[1:]])[0],'version':'A'} for r in orders['rows']]
outds=ds('batch_results','Persisted keyed batch results',[
    col('order_id','string','identifier'),col('prediction','number','numerical'),col('version','string','categorical')],
    [[r['order_id'],r['prediction'],r['version']] for r in outputs],
    'Predictions computed by executing the supplied frozen fixture package; keyed JSONL mirrors these rows. Not an answer for the learner batch procedure.')
variant(outds,'missing_result',[{'op':'drop_rows','where':{'order_id':'B'}}])
variant(outds,'duplicate_result',[{'op':'duplicate_row','where':{'order_id':'A'},'insert':'after'}],'duplicate_row',{'order_id':'A'},'order_id',1)
variant(outds,'same_count_wrong_keys',[{'op':'drop_rows','where':{'order_id':'B'}},{'op':'duplicate_row','where':{'order_id':'A'},'insert':'after'}],'duplicate_row',{'order_id':'A'},'order_id',1)
variant(outds,'malformed_result',[{'op':'set_cell','where':{'order_id':'C'},'column':'prediction','value':None}],'missing_value',{'order_id':'C'},'prediction')

# Complete individual attempts: preserve failures, completion sample and absent handler evidence.
measurement_cols=[col('request_id','string','identifier'),col('experiment','string','categorical'),col('setting','string','categorical'),col('attempt_index','integer','identifier',label=True),col('request_start_seconds','number','numerical','seconds'),col('response_complete_seconds','number','numerical','seconds'),col('outcome','string','categorical'),col('http_status','integer','categorical',description='HTTP protocol code, not a measured magnitude.',label=True),col('valid_prediction','boolean','categorical'),col('handler_start_seconds','number','numerical','seconds'),col('handler_complete_seconds','number','numerical','seconds'),col('handler_status','integer','categorical',label=True)]
measurements=[]
def attempts(experiment,setting,count,success,http_error,timeout,rate,slow=False):
    for i in range(count):
        start=i/rate
        if i<success:
            outcome='success';status=200;valid=True;elapsed=(0.15+(i%7)*0.01) if not slow else (2.2+(i%7)*0.02)
        elif i<success+http_error:
            outcome='http_error';status=500;valid=False;elapsed=0.25
        elif i<success+http_error+timeout:
            outcome='timeout';status=None;valid=False;elapsed=None
        else:
            outcome='connection_refused';status=None;valid=False;elapsed=None
        complete=None if elapsed is None else round(start+elapsed,6)
        # External-only timeout/refusal records intentionally have no handler counterpart.
        hs=round(start+0.01,6) if status is not None else None
        he=round(hs+0.05+(i%5)*0.005,6) if hs is not None else None
        measurements.append([f'{experiment}.{setting}.{i:03d}',experiment,setting,i,round(start,6),complete,outcome,status,valid,hs,he,status])
attempts('probe','baseline',300,294,2,2,1)
attempts('load','rate_5',50,50,0,0,5)
attempts('load','rate_10',100,90,6,4,10)
attempts('load','rate_15',150,100,30,20,15)
attempts('scaling','replicas_2',100,96,2,2,10)
attempts('scaling','replicas_3',100,98,1,1,10,True)
serving=ds('serving_attempts','Complete client and handler evidence',measurement_cols,measurements,'Probe retains exactly 300 starts in [0,300), with 294 HTTP-200 valid responses inside two seconds, two handled HTTP errors, two external timeouts and two connection refusals. Load rate_10 preserves the glossary 100/90/6/4 ten-second example. Scaling compares two and three replicas at the same offered load. Null completion is not a zero latency.')
backlogrows=[]
for exp,setting,queue in [('load','rate_5',[0,0,0]),('load','rate_10',[0,0,0]),('load','rate_15',[0,8,16]),('scaling','replicas_2',[0,0,0]),('scaling','replicas_3',[0,3,6])]:
    for t,q in zip([0.0,5.0,10.0],queue):backlogrows.append([exp,setting,t,q])
backlog=ds('backlog','Backlog observations throughout each measurement',[
    col('experiment','string','categorical'),col('setting','string','categorical'),col('elapsed_seconds','number','numerical','seconds'),col('unfinished_requests','integer','numerical','requests')],backlogrows,'Three observations per fixed ten-second window distinguish stable backlog from growth. Timed-out attempts remain failures; unfinished work is an additional boundary observation, not a second category of attempts to sum into the denominator.')

batchrows=[]
for setting in ['limit_1','limit_2']:
    for i in range(5):
        start=1.0+i
        wait=(0.0 if setting=='limit_1' else 0.4)
        end=round(start+wait+0.2,6)
        key=f'order_{i+1}'
        payload={'request_id':key,'batching_setting':setting,'predictions':predict([orders['rows'][i][1:]])}
        batchrows.append([key,setting,start,round(start+wait,6),end,True,json.dumps(payload)])
# A failed matched attempt and an unmatched response must not silently enter the success sample.
batchrows.extend([['failed_order','limit_2',6.0,6.4,None,False,None],['unmatched_response','limit_2',None,None,7.6,True,json.dumps({'request_id':'unmatched_response','batching_setting':'limit_2','predictions':[0.0]})]])
batching=ds('batching_trace','Identified batching trace',[
    col('request_id','string','identifier'),col('batching_setting','string','categorical'),col('request_start_seconds','number','numerical','seconds'),col('batch_wait_end_seconds','number','numerical','seconds'),col('response_complete_seconds','number','numerical','seconds'),col('success','boolean','categorical'),col('response_json','string','text')],batchrows,'The first limit_2 observation preserves start 1.0, wait end 1.4, response completion 1.6. Same input identities under two measured limits; failure and unmatched response are explicit edge records.')

workerrows=[]
for interval,n in [('within_limit',2),('oversubscribed',3)]:
    workerrows.append([interval,'prediction',100,'supervisor',False])
    for i in range(n):workerrows.append([interval,'prediction',101+i,'prediction_worker',True])
workers=ds('worker_processes','Authored container-top process snapshots',[
    col('interval_id','string','identifier'),col('container_name','string','identifier'),col('pid','integer','identifier',label=True),col('process_kind','string','categorical'),col('is_prediction_worker','boolean','categorical')],workerrows,'Both snapshots accompany a configured worker limit of two. Supporting supervisor is not a prediction worker; three actual workers expose oversubscription.')
resources=ds('worker_resources','Concurrent CPU and memory observations',[
    col('interval_id','string','identifier'),col('elapsed_seconds','number','numerical','seconds'),col('cpu_percent','number','numerical','percent'),col('memory_mib','number','numerical','MiB')],[[k,t,c+t,m+2*t] for k,c,m in [('within_limit',70.0,128.0),('oversubscribed',95.0,192.0)] for t in [0.0,5.0,10.0]],'CPU and memory recorded during the matching process/load interval; no CPU-only availability inference is intended.')

scale_states=ds('replica_states','Original, changed and restored identities',[
    col('phase','string','categorical'),col('intended_replicas','integer','numerical','containers'),col('container_name','string','identifier'),col('container_running','boolean','categorical'),col('instance','string','identifier'),col('zone','string','categorical'),col('instance_status','string','categorical')],
    [[p,n,f'prediction-{i+1}',True,'order-lab','fixture-zone','RUNNING'] for p,n in [('original',1),('changed_two',2),('changed_three',3),('restored',1)] for i in range(n)],'Nonproduction lifecycle and replica fixture preserves the original one-replica setting. Identifiers are local fictional fixture labels, not real cloud resources.')

readiness=ds('readiness_cases','Controllable initialization fixtures',[
    col('case_id','string','identifier'),col('model_initialized','boolean','categorical'),col('preprocessor_initialized','boolean','categorical'),col('initialization_failed','boolean','categorical')],
    [['neither',False,False,False],['model_only',True,False,False],['preprocessor_only',False,True,False],['both',True,True,False],['initialization_failure',False,False,True]],'All partial initialization states are supplied; the learner implements readiness status and JSON handling.')

# Immutable fixture identities computed from the exact authored package bytes, not typed digests.
release_refs={v:'fixture.local/orders@sha256:'+hashlib.sha256((frozen_source+'\n# release '+v+'\n').encode()).hexdigest() for v in ['A','B']}
releases=ds('release_records','Approval and immutable fixture artifact records',[
    col('version','string','categorical'),col('approved','boolean','categorical'),col('image_reference','string','identifier'),col('container_name','string','identifier'),col('host_port','integer','categorical',label=True),col('release_role','string','categorical')],
    [['A',True,release_refs['A'],'prediction-A',8081,'approved_previous'],['B',False,release_refs['B'],'prediction-B',8082,'faulty_test']],
    'Synthetic content-addressed artifact identities are computed from included authored package sources. They are offline fixture references, not remotely pullable production images. A is approved previous; B is faulty test. No latest version selection is authorized.')
transition=ds('release_transition','Rollback ordering fixture',[
    col('sequence','integer','numerical'),col('event','string','categorical'),col('A_running','boolean','categorical'),col('A_verified','boolean','categorical'),col('B_running','boolean','categorical'),col('B_removed','boolean','categorical')],
    [[0,'initial',False,False,True,False],[1,'start_A',True,False,True,False],[2,'verify_A',True,True,True,False],[3,'stop_B',True,True,False,False],[4,'remove_B',True,True,False,True]],'Authored reference chronology for before/after visuals; not evidence of commands run on an actual container.')
variant(transition,'retire_before_verify',[{'op':'set_cell','where':{'event':'start_A'},'column':'B_running','value':False}],'other',{'event':'start_A'},'B_running',rule={'column':'B_running','op':'eq','value':False})

contract={
    'fixture_only':True,'domain':'anonymous two-feature orders','feature_names':['feature_1','feature_2'],
    'request_keys':['features'],'response_keys':['predictions','version'],'matrix_rank':2,'matrix_width':2,
    'feature_min':0.0,'feature_max':10.0,'limits_inclusive':True,'numpy_dtype':'float64',
    'prediction_rows':'one per request row','batch_key':'order_id','batch_result_keys':['order_id','prediction','version'],
    'chunk_size':2,'batch_input_path':'orders.csv','batch_output_path':'learner_results.jsonl',
    'host':'127.0.0.1','port':8080,'prediction_route':'/predict','readiness_route':'/ping',
    'success_status':200,'schema_rejection_status':400,'denied_status':403,'not_ready_status':503,
    'ready_payload':{'ready':True},'not_ready_payload':{'ready':False},'timeout_seconds':2.0,
    'healthcheck':{'command':['CMD','python','health_probe.py'],'interval_seconds':5,'timeout_seconds':2,'retries':3},
    'version':'A','expected_request':request,'expected_response':response,
    'expected_audience':'order-prediction-fixture','permitted_subjects':['fixture-subject-permitted'],
    'credential_secret_reference':'credential','injected_secret_variable':'ORDER_FIXTURE_CREDENTIAL',
    'logging_policy':'Record failure class only; never record token, credential literal or protected request values.'}
httpcases=[]
for name,req in [('valid',request),('included_limit',{'features':[[10.0,2.0]]}),('beyond_limit',{'features':[[11.0,2.0]]}),('missing_key',{}),('wrong_type',{'features':[['not_numeric',2.0]]}),('wrong_rank',{'features':[1.0,2.0]}),('wrong_width',{'features':[[1.0,2.0,3.0]]})]:
    httpcases.append({'case_id':name,'request':req,'expected_acceptance':name in ['valid','included_limit']})
httpcases.append({'case_id':'invalid_json','request_text':'{','expected_acceptance':False})
responsecases=[{'case_id':'aligned','response':response},{'case_id':'missing_output_key','response':{'version':'A'}},{'case_id':'incorrect_row_alignment','response':{'predictions':response['predictions'][:-1],'version':'A'}},{'case_id':'wrong_output_type','response':{'predictions':'not_a_list','version':'A'}}]
common_runtime={'fixture_only':True,'CONFIG_PATH':'compose.yaml','NAME':'prediction','SERVICE':'prediction','INSTANCE':'order-lab','ZONE':'fixture-zone','BRANCH':'verify-order-release','BASE_BRANCH':'main','IMAGE_DIGEST':release_refs['A'],'HOST_PORT':8080,'CONTAINER_PORT':8080,'SETTING':'MODE','VALUE':'fixture','REPLICA_COUNT':1,'worker_limit_key':'WORKER_LIMIT','approved_worker_limit':2,'supported_resource_limits':{'cpus':1.0,'memory':'256M'},'secret_reference':'credential','secret_environment_variable':'ORDER_FIXTURE_CREDENTIAL','supports_deploy_fields':True,'original_replica_count':1,'replica_bounds':{'min':1,'max':3},'original_instance_status':'RUNNING','scaling_policy':{'MinCapacity':1,'MaxCapacity':3,'metric':'SageMakerVariantInvocationsPerInstance','target_value':10.0,'scale_in_cooldown_seconds':60,'scale_out_cooldown_seconds':30},'authorization':'Only local nonproduction fixture identities and supplied lifecycle/secret hooks; no cloud or registry credentials are bundled.'}
measurement_policy={'units':'seconds','ddof':0,'declared_percentile':99,'percentile_method':'linear','probe':{'t0':0.0,'window':'[0, 300)','attempt_count':300,'rate_per_second':1,'deadline_seconds':2.0,'earliest_summary_time_seconds':301.0,'error_classification':'Every attempt not HTTP 200 with a valid prediction received within two seconds'},'load':{'offered_rates':[5,10,15],'measurement_seconds':10.0,'warmup_seconds':2.0,'arrival_profile':'fixed evenly spaced starts','payload_mix':'valid first-three-order matrix only; intentional malformed fixtures run separately','max_in_flight':30,'timeout_seconds':2.0,'minimum_success_probability':0.9,'maximum_failed_fraction':0.1,'maximum_p99_seconds':1.0,'minimum_successful_throughput_per_second':5.0,'backlog_rule':'No increase between sampled unfinished-work observations; end unfinished work zero'},'batching':{'settings':['limit_1','limit_2'],'maximum_p99_seconds':0.5,'population':'Matched successful decoded responses only; exclude failure and unmatched response'},'scaling':{'offered_rate':10.0,'measurement_seconds':10.0,'settings':['replicas_2','replicas_3'],'minimum_success_probability':0.95,'maximum_p99_seconds':1.0,'minimum_successful_throughput_per_second':9.0}}
transport_source='''# Infrastructure helper: bounded status/body transport, not a client validation solution.
import urllib.request
from urllib.error import HTTPError

def request_bytes(request, timeout_seconds):
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            return response.status, response.read()
    except HTTPError as response:
        return response.code, response.read()
'''
health_source='''import json
import urllib.request
with urllib.request.urlopen("http://127.0.0.1:8080/ping", timeout=2) as response:
    if response.status != 200 or json.loads(response.read().decode("utf-8")) != {"ready": True}:
        raise SystemExit(1)
'''
original_compose={'services':{'prediction':{'image':release_refs['A'],'environment':{'MODE':'fixture','WORKER_LIMIT':'1'},'ports':['8080:8080'],'secrets':['credential'],'deploy':{'replicas':1,'resources':{'limits':{'cpus':1.0,'memory':'256M'}}}}},'secrets':{'credential':{'environment':'ORDER_FIXTURE_CREDENTIAL'}}}
# A bounded offline scaffold records supplied infrastructure observations. It never claims live Docker/cloud execution.
fixture_api='''import json
from pathlib import Path

handler_durations = []
handler_events = []

def read_fixture(filename):
    return json.loads(Path(filename).read_text())

def external_probe():
    """Return supplied complete attempt records; scheduling/fault injection belongs to infrastructure."""
    return read_fixture("measurement_records.json")

def bounded_load_driver(setting):
    """Offline driver record, not learner load-generation code or production performance."""
    return [r for r in external_probe() if r["experiment"] == "load" and r["setting"] == setting]

def captured_runtime():
    return read_fixture("runtime_observations.json")

def record_handler(timestamp, duration, status, error_class=None):
    handler_durations.append(duration)
    handler_events.append({"timestamp": timestamp, "duration": duration, "status": status, "error_class": error_class})
'''
runtime_observations={'fixture_only':True,'container_inspect':{'Name':'prediction','Config':{'Image':release_refs['A']},'State':{'Running':True,'Status':'running','ExitCode':0,'Health':{'Status':'healthy'}}},'logs':['initialization completed','request validation failed: ValueError'],'instance':{'name':'order-lab','zone':'fixture-zone','status':'RUNNING'},'wrong_image_case':{'Name':'prediction','Config':{'Image':release_refs['B']},'State':{'Running':True,'Status':'running'}},'failed_initialization_case':{'Name':'prediction','Config':{'Image':release_refs['A']},'State':{'Running':False,'Status':'exited','ExitCode':1}},'readiness_response':{'status':200,'body':json.dumps(contract['ready_payload'])},'prediction_response':{'status':200,'body':json.dumps(response)}}

mounts={
'prediction_schema_validation':[orders],
'online_prediction_contract':[orders],
'bounded_batch_inference':[orders,outds],
'model_service_readiness':[readiness,releases],
'deployment_configuration_code':[releases],
'deployment_verification':[orders,releases],
'prediction_authentication':[orders,releases],
'service_telemetry':[serving],
'prediction_load_test':[orders,serving,backlog],
'inference_batching_decision':[batching],
'serving_worker_concurrency':[workers,resources,releases],
'serving_replica_scaling':[serving,backlog,scale_states,releases],
'model_release_rollback':[orders,releases,transition]}

for bundle in g['bundles']:
    name=bundle['context']['concept_id'].split('.',1)[1]
    practice=bundle['practice_anchor']['live_code']
    # Files contain contracts/scaffolding only: no completed target learner function or assertions.
    readme='# '+bundle['context']['concept_name']+'\n\nFictional order-prediction lab; all data and runtime observations are authored fixtures. No credentials, live cloud resources or pullable container images are supplied. The image identities are computed from the included release package bytes. A deployment-capable authorized runtime must bind these fixture identities to its local image/scaffold; these files do not claim deployment occurred.\n\n## Supplied contract\nAnonymous feature_1 and feature_2, request key features, output keys predictions and version. These concrete names and limits are authored here because the glossary leaves them unnamed. Read contract.json before using any fixtures.\n\n## Learner task (glossary)\n'+bundle['practice_anchor']['objective']+'\n\n## Starter-state intent (glossary)\n'+practice['starter_state_intent']+'\n\n## Observable success (glossary)\n'+practice['observable_success']+'\n\n## Visual intent (glossary)\n'+bundle['visual_anchor']['purpose']+'\n\nDataset CSV headers and all records are copied from the registry by the builder. Measurement records are observations, not computed summary answers. Offline infrastructure helpers supply transport/status bytes or recorded outcomes; author the requested imports, logic, fixtures and assertions in learner.py. Runtime commands listed by the glossary are tasks for the authorized fixture environment, not commands this registry builder executes.\n'
    files=[{'path':'README.md','content':readme},{'path':'contract.json','content':dumps(contract)},{'path':'runtime_contract.json','content':dumps(common_runtime)},{'path':'measurement_policy.json','content':dumps(measurement_policy)},{'path':'learner.py','content':'# Author the glossary task here, including your imports, functions and assertions.\n'},{'path':'constraints.json','content':dumps({'allowed_syntax':practice['allowed_syntax'],'blocked_syntax':practice['blocked_syntax']})},{'path':'asset_mounts.json','content':dumps([{'asset_id':a['asset_id'],'path':a['asset_id'][3:]+'.csv'} for a in mounts[name]])}]
    for a in mounts[name]:files.append({'path':a['asset_id'][3:]+'.csv','content':csvtext(a)})
    if name in ['prediction_schema_validation','online_prediction_contract','bounded_batch_inference','deployment_verification','prediction_authentication','prediction_load_test','model_release_rollback']:
        files.extend([{'path':'request_cases.json','content':dumps(httpcases)},{'path':'response_cases.json','content':dumps(responsecases)},{'path':'transport.py','content':transport_source}])
    if name in ['online_prediction_contract','bounded_batch_inference','service_telemetry']:
        files.append({'path':'frozen_package.py','content':frozen_source})
    if name=='bounded_batch_inference':
        files.append({'path':'reference_results.jsonl','content':''.join(json.dumps(r)+'\n' for r in outputs)})
        for variant_name,records in [('missing_result',outputs[:1]+outputs[2:]),('duplicate_result',outputs[:1]+outputs),('same_count_wrong_keys',[outputs[0],outputs[0]]+outputs[2:]),('malformed_record',outputs[:2]+[{'order_id':'C'}]+outputs[3:])]:
            files.append({'path':'fixtures/'+variant_name+'.jsonl','content':''.join(json.dumps(r)+'\n' for r in records)})
    if name in ['model_service_readiness','deployment_configuration_code','deployment_verification','prediction_authentication','prediction_load_test','serving_worker_concurrency','serving_replica_scaling','model_release_rollback']:
        files.extend([{'path':'runtime_observations.json','content':dumps(runtime_observations)},{'path':'health_probe.py','content':health_source}])
        # Approved source bytes let consumers independently recompute every immutable fixture digest.
        for v in ['A','B']:files.append({'path':'artifacts/release_'+v+'.py','content':frozen_source+'\n# release '+v+'\n'})
    if name in ['serving_worker_concurrency','serving_replica_scaling']:
        files.append({'path':'original_config.json','content':dumps(original_compose)})
    if name=='prediction_authentication':
        files.append({'path':'authentication_cases.json','content':dumps([
            {'case_id':'authorized','credential_source':'runtime secret fixture: permitted token','verified_claims':{'sub':'fixture-subject-permitted'},'expected_status':200},
            {'case_id':'missing','credential_source':None,'expected_status':403},
            {'case_id':'invalid_token','verifier_exception':'ValueError','expected_status':403},
            {'case_id':'invalid_issuer','verifier_exception':'GoogleAuthError','expected_status':403},
            {'case_id':'unpermitted_subject','verified_claims':{'sub':'fixture-subject-unpermitted'},'expected_status':403}])})
    if name in ['service_telemetry','prediction_load_test','serving_replica_scaling']:
        files.extend([{'path':'fixture_api.py','content':fixture_api},{'path':'measurement_records.json','content':dumps(dictrows(serving))}])
    if name=='model_service_readiness':files.append({'path':'initialization_cases.json','content':dumps(dictrows(readiness))})
    if name=='inference_batching_decision':files.append({'path':'trace_records.json','content':dumps(dictrows(batching))})
    if name=='serving_replica_scaling':files.append({'path':'restoration_contract.json','content':dumps({'original_configuration':original_compose,'original_instance_status':'RUNNING','required_final_phase':'restored','preserve_evidence':True})})
    if name=='model_release_rollback':files.append({'path':'rollback_contract.json','content':dumps({'initial_running_version':'B','approved_target_version':'A','approved_image_reference':release_refs['A'],'replacement_identity':'prediction-A','faulty_identity':'prediction-B','replacement_host_port':8081,'verify_before_retire':True,'expected_prediction_response':response})})
    assets.append({'asset_id':'ws.'+name,'asset_kind':'code_workspace','scenario_id':sid,'title':bundle['context']['concept_name']+' — bounded fixture workspace','runtime':'python','files':files})

registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':sid,'name':'Order prediction in an authorized nonproduction serving lab','summary':'A fictional ML engineer carries one frozen, anonymous two-feature order prediction package through schema checks, online and chunked inference, readiness, reproducible deployment, authorization, bounded service measurements, scaling and approved rollback. All records, artifact sources and runtime observations are authored lab fixtures. No real production results or credentials are asserted.','domain':'bounded ML production-serving practice','glossary_example_vocab':vocab}],'assets':assets}
(B/'scenario_asset_registry.json').write_text(dumps(registry))
# Deterministic local checklist, beyond the registry gate.
assert len(mounts)==len(g['bundles'])
assert len(set(a['asset_id'] for a in assets))==len(assets)
for a in assets:
    if a['asset_kind']=='dataset':
        assert all(len(r)==len(a['columns']) for r in a['rows'])
        assert len(set(c['name'] for c in a['columns']))==len(a['columns'])
        assert all(c['semantic_role']!='numerical' or c['type'] in ['integer','number'] for c in a['columns'])
    else:
        assert len({f['path'] for f in a['files']})==len(a['files'])
        for f in a['files']:
            if f['path'].endswith('.json'):json.loads(f['content'])
            if f['path'].endswith('.py'):compile(f['content'],f['path'],'exec')
assert Counter(r[6] for r in serving['rows'] if r[1]=='probe')['success']==294
assert len([r for r in serving['rows'] if r[1]=='probe'])==300
assert Counter(r[6] for r in serving['rows'] if r[1]=='load' and r[2]=='rate_10')=={'success':90,'http_error':6,'timeout':4}
for v in ['A','B']:
    assert release_refs[v].split('sha256:')[1]==hashlib.sha256((frozen_source+'\n# release '+v+'\n').encode()).hexdigest()
print('Wrote',B/'scenario_asset_registry.json')
print('Scenarios:',len(registry['scenarios']),'Assets:',len(assets),'Kinds:',dict(Counter(a['asset_kind'] for a in assets)))
print('Rows:',sum(len(a.get('rows',[])) for a in assets),'Variants:',sum(len(a.get('variants',[])) for a in assets))
