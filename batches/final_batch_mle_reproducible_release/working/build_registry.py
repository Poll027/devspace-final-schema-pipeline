import csv, io, json, hashlib, sys, datetime, re
from pathlib import Path
B=Path('batches/final_batch_mle.region.reproducible_release')
bundle=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
SID='scenario.order_training_release'
assets=[]
def dump(x): return json.dumps(x,indent=2)+'\n'
def csv_text(columns,rows):
    s=io.StringIO(newline=''); w=csv.writer(s); w.writerow(columns);w.writerows(rows);return s.getvalue()
def dataset(aid,title,cols,rows,variants=[]):
    assets.append(dict(asset_id=aid,asset_kind='dataset',scenario_id=SID,title=title,description='Authored fictional fixture, not observed production data.',columns=[dict(name=n,type=t,semantic_role=r,numeric_looking_label=(r=='categorical' and any((isinstance(row[i],str) and row[i].isdigit()) or (isinstance(row[i],(int,float)) and not isinstance(row[i],bool)) for row in rows))) for i,(n,t,r) in enumerate(cols)],rows=rows,variants=variants,provenance='authored'))
    return csv_text([c[0] for c in cols],rows)
# No task fields were named in the glossary; these are explicitly authored order fields.
train=[[f'order_{i:02}',float(x),int(y)] for i,(x,y) in enumerate([(5,0),(10,0),(15,0),(20,0),(25,0),(30,0),(35,0),(40,1),(45,0),(50,1),(55,1),(60,1),(65,1),(70,1),(75,1),(80,1)],1)]
cols=[('order_id','string','identifier'),('order_amount','number','numerical'),('late','integer','categorical')]
training=dataset('ds.training_orders','Local training orders',cols,train,[dict(variant_id='changed_latest',derived_from='ds.training_orders',purpose='A valid but changed current object; not the recorded snapshot.',ops=[dict(op='set_cell',where={'order_id':train[0][0]},occurrence=0,column='order_amount',value=95.0)],planted_issues=[])])
protected=[[f'protected_{i:02}',float(x),int(y)] for i,(x,y) in enumerate([(10,0),(20,1),(30,0),(40,1),(45,0),(50,1),(60,1),(70,1)],1)]
protected_csv=dataset('ds.protected_orders','Protected matched cohort',cols,protected,[dict(variant_id='no_negatives',derived_from='ds.protected_orders',purpose='Undefined FPR and dependent cost: empty actual-negative group.',ops=[dict(op='drop_rows',where={'late':0})],planted_issues=[]),dict(variant_id='no_positives',derived_from='ds.protected_orders',purpose='Undefined FNR and dependent cost: empty actual-positive group.',ops=[dict(op='drop_rows',where={'late':1})],planted_issues=[])])
fixed=[[r[0],r[1],r[2]] for r in (train[0],train[7],train[-1])]
fixed_csv=dataset('ds.fixed_orders','Fixed valid and boundary prediction inputs',cols,fixed)
common_code='''import csv
from pathlib import Path

class FittedPreprocessor:
    def __init__(self, mean):
        self.mean_ = mean
    def transform(self, inputs):
        return [[float(row[0]) - self.mean_] for row in inputs]

class FittedModel:
    def __init__(self, boundary):
        self.boundary_ = boundary
    def predict(self, transformed):
        return [int(row[0] >= self.boundary_) for row in transformed]

def read_orders(path):
    with open(path, newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    return rows

def supplied_workflow(dataset_path='training_orders.csv', threshold=40.0):
    rows = read_orders(dataset_path)
    inputs = [[float(row['order_amount'])] for row in rows]
    mean = sum(row[0] for row in inputs)/len(inputs)
    preprocessor = FittedPreprocessor(mean)
    model = FittedModel(threshold - mean)
    predictions = model.predict(preprocessor.transform(inputs))
    accuracy = sum(p == int(row['late']) for p,row in zip(predictions,rows))/len(rows)
    return {'model': model, 'preprocessor': preprocessor, 'validation_accuracy': accuracy,
            'resolved_parameters': {'dataset_path': dataset_path, 'threshold': threshold}}

def frozen_prediction_helper(rows, identity):
    if identity not in ('B', 'baseline'):
        raise ValueError('Only the supplied frozen identities are authorized')
    threshold = 40.0 if identity == 'B' else 60.0
    state = supplied_workflow(threshold=threshold)
    return state['model'].predict(state['preprocessor'].transform([[float(r['order_amount'])] for r in rows]))

def protected_data_access(variant='base'):
    rows = read_orders('protected_orders.csv')
    if variant == 'no_negatives': rows = [r for r in rows if int(r['late']) != 0]
    elif variant == 'no_positives': rows = [r for r in rows if int(r['late']) != 1]
    elif variant != 'base': raise ValueError(variant)
    return rows
'''
ns={};exec(common_code,ns)
# Execute the supplied workflow over registered CSV; do not author expected outputs.
W=B/'working/fixture';W.mkdir(parents=True,exist_ok=True)
(W/'training_orders.csv').write_text(training)
state=ns['supplied_workflow'](str(W/'training_orders.csv'))
settings={'dataset_path':'training_orders.csv','threshold':50.0}
override=ns['supplied_workflow'](str(W/'training_orders.csv'),threshold=settings['threshold'])
expected={'default':{'threshold':40.0,'validation_accuracy':state['validation_accuracy']},'configured':{'threshold':settings['threshold'],'validation_accuracy':override['validation_accuracy']}}
fixed_inputs=[[r[1]] for r in fixed]
fixed_predictions=state['model'].predict(state['preprocessor'].transform(fixed_inputs))
package_contract={'model_identity':'B','registry_version':1,'package_path':'package/B/version_1.pkl','manifest_path':'requirements.txt','serving_source':'serve_fixture.py','serving_command':['python','serve_fixture.py'],'compatible_python_image':f'python:{sys.version_info.major}.{sys.version_info.minor}-slim','image_tag':'order-fixture:version-1','container_name':'order-fixture','host_port':8080,'container_port':8080,'nonsecret_settings':{'FIXTURE_MODE':'fixed-orders'},'secret_policy':'Use authorized runtime secret mounts only; no literal credentials in Dockerfile or Compose.','fixed_inputs':fixed_inputs,'pre_save_predictions':fixed_predictions,'expected_preprocessor_mean':state['preprocessor'].mean_,'rtol':1e-7,'atol':1e-9,'failure_cases':['changed preprocessing mean','flipped prediction','untrusted artifact: reject before pickle.load','deliberately false predicate raises AssertionError without -O']}
policy={'selected_candidate':'B','preprocessing_identity':'B.fitted.order_amount.center','threshold':40.0,'baseline_threshold':60.0,'deployment_probabilities':{'0':0.7,'1':0.3},'error_costs':{'FP':2.0,'FN':5.0},'requirements':{'max_expected_error_cost':0.5,'max_FPR':0.25,'max_FNR':0.4},'correct_prediction_cost':0.0}
comparison=[]
for ident,threshold in [('B',40.0),('baseline',60.0)]:
    p=ns['supplied_workflow'](str(W/'training_orders.csv'),threshold=threshold)
    pred=p['model'].predict(p['preprocessor'].transform([[r[1]] for r in protected]))
    for variant in ['base','no_negatives','no_positives']:
        pairs=[(r[2],y) for r,y in zip(protected,pred) if variant=='base' or (variant=='no_negatives' and r[2]==1) or (variant=='no_positives' and r[2]==0)]
        tn=sum(a==0 and y==0 for a,y in pairs);fp=sum(a==0 and y==1 for a,y in pairs);fn=sum(a==1 and y==0 for a,y in pairs);tp=sum(a==1 and y==1 for a,y in pairs)
        fpr=fp/(fp+tn) if fp+tn else None;fnr=fn/(fn+tp) if fn+tp else None
        cost=None if fpr is None or fnr is None else policy['deployment_probabilities']['0']*fpr*policy['error_costs']['FP']+policy['deployment_probabilities']['1']*fnr*policy['error_costs']['FN']
        req=policy['requirements'];verdict='undefined' if cost is None else ('pass' if cost<=req['max_expected_error_cost'] and fpr<=req['max_FPR'] and fnr<=req['max_FNR'] else 'fail')
        comparison.append([variant,ident,policy['preprocessing_identity'] if ident=='B' else 'baseline.fitted.order_amount.center',threshold,len(pairs),tn,fp,fn,tp,fpr,fnr,policy['deployment_probabilities']['0'],policy['deployment_probabilities']['1'],policy['error_costs']['FP'],policy['error_costs']['FN'],cost,req['max_expected_error_cost'],req['max_FPR'],req['max_FNR'],verdict])
comparison_csv=dataset('ds.protected_comparison','Computed frozen B versus baseline comparison',[(n,t,r) for n,t,r in [('cohort','string','identifier'),('model_identity','string','categorical'),('preprocessing_identity','string','identifier'),('threshold','number','numerical'),('cohort_size','integer','numerical'),('TN','integer','numerical'),('FP','integer','numerical'),('FN','integer','numerical'),('TP','integer','numerical'),('FPR','number','numerical'),('FNR','number','numerical'),('P_Y0','number','numerical'),('P_Y1','number','numerical'),('cost_FP','number','numerical'),('cost_FN','number','numerical'),('expected_error_cost','number','numerical'),('max_expected_error_cost','number','numerical'),('max_FPR','number','numerical'),('max_FNR','number','numerical'),('requirement_outcome','string','categorical')]],comparison)
assets[-1]['provenance']='generated_by_script'
changed=[r[:] for r in train];changed[0][1]=95.0
changed_csv=csv_text([c[0] for c in cols],changed)
artifact_bytes=dump({'fixture_artifact':'B','threshold':40.0,'preprocessor_mean':state['preprocessor'].mean_}).encode()
replacement_bytes=dump({'fixture_artifact':'B','threshold':50.0,'preprocessor_mean':state['preprocessor'].mean_}).encode()
sha=lambda b:hashlib.sha256(b).hexdigest()
# Generations and registry versions are allocated from the authored fixture sequences.
original_generation,latest_generation=range(1,3)
run={'run_id':'run.order.B','bucket_name':'authorized-fixture','key':'models/B/latest.json','generation':original_generation,'expected_hash':sha(artifact_bytes),'version_qualified_source':f'gs://authorized-fixture/models/B/latest.json#{original_generation}','model_name':'B','new_name_model':'baseline','local_path':'downloads/B.json'}
mismatch={**run,'expected_hash':sha(replacement_bytes)}
snapshot={'bucket_name':'authorized-fixture','object_name':'datasets/latest.csv','generation':original_generation,'expected_hash':sha(training.encode()),'local_path':'training_orders.csv','record_path':'snapshot_record.json','download_path':'downloads/training_orders.csv'}
# Explicit local stand-ins: no cloud credentials, network, or real registry side effects.
gcs='''from pathlib import Path
import json
_STATE = None

def reset_fixture():
    global _STATE
    _STATE = json.loads(Path('storage_fixture.json').read_text())

def overwrite_latest(bucket_name, object_name, replacement_path='changed_latest.csv'):
    bucket = Client().bucket(bucket_name)
    bucket.blob(object_name).upload_from_filename(replacement_path)

class Client:
    def __init__(self):
        if _STATE is None: reset_fixture()
    def bucket(self, name):
        if name != 'authorized-fixture': raise PermissionError(name)
        return Bucket(name)
class Bucket:
    def __init__(self,name): self.name=name
    def blob(self, name, generation=None): return Blob(name,generation)
class Blob:
    def __init__(self,name,generation): self.name=name;self.generation=generation
    def _entry(self):
        item=_STATE[self.name]
        gen=self.generation if self.generation is not None else item['latest']
        return item['versions'][str(gen)]
    def exists(self,client=None):
        try: self._entry();return True
        except KeyError:return False
    def download_to_filename(self,path):
        p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(self._entry().encode())
    def upload_from_filename(self,path): self.upload_from_string(Path(path).read_bytes())
    def upload_from_string(self,data):
        item=_STATE.setdefault(self.name,{'latest':0,'versions':{}})
        gen=max([int(k) for k in item['versions']] or [0])+1
        item['versions'][str(gen)]=data.decode() if isinstance(data,bytes) else data
        item['latest']=gen;self.generation=gen
'''
registry_mock='''import json
from pathlib import Path
from types import SimpleNamespace
_MODELS={'B':{}}
_CALLS=[]
class MlflowClient:
    def get_run(self,run_id):
        record=json.loads(Path('run_artifact_record.json').read_text())
        if run_id != record['run_id']:raise KeyError(run_id)
        return SimpleNamespace(info=SimpleNamespace(run_id=run_id),data=SimpleNamespace(tags=record),artifact_record=record)
    def get_registered_model(self,name):
        if name not in _MODELS:raise KeyError(name)
        return SimpleNamespace(name=name)
    def create_registered_model(self,name):
        if name in _MODELS:raise ValueError('already exists')
        _MODELS[name]={};return SimpleNamespace(name=name)
    def create_model_version(self,name,source,run_id):
        versions=_MODELS[name];version=str(len(versions)+1)
        result=SimpleNamespace(name=name,version=version,source=source,run_id=run_id,tags={})
        versions[version]=result;_CALLS.append(('create_model_version',name,source,run_id));return result
    def set_model_version_tag(self,name,version,tag_key,tag_value):
        _MODELS[name][str(version)].tags[tag_key]=str(tag_value)
    def get_model_version(self,name,version): return _MODELS[name][str(version)]
def reset_fixture():
    _MODELS.clear();_MODELS['B']={};_CALLS.clear()
'''
managed_contract={'job_name':'order-training-job','image':'fixture.local/order-training:custom','role':'arn:aws:iam::000000000000:role/fixture-training','channel':'training','input_bucket':'authorized-fixture','input_key':'datasets/latest.csv','input_version':str(original_generation),'immutable_key':'snapshots/order-training/input.csv','output_uri':'s3://authorized-fixture/outputs','instance_type':'ml.m5.large','max_instance_count':1,'max_runtime_seconds':120,'dataset_snapshot':snapshot,'code_reference':'managed_training_code.py','configuration_path':'job_config.json','artifact_uri':'s3://authorized-fixture/outputs/order-training-job/output/model.tar.gz','channel_path':'/opt/ml/input/data/training','model_output_path':'/opt/ml/model'}
managed_mock='''import io,json
from pathlib import Path
_CONTRACT=json.loads(Path('managed_contract.json').read_text())
_VERSIONS=json.loads(Path('s3_fixture.json').read_text())
_SUBMISSIONS=[]
_COPIES=[]
_CASE='completed'
def reset_fixture(case='completed'):
    global _CASE
    _CASE=case;_SUBMISSIONS.clear();_COPIES.clear()
    _VERSIONS.clear();_VERSIONS.update(json.loads(Path('s3_fixture.json').read_text()))
class Storage:
    def _get(self,Bucket,Key,VersionId=None):
        if Bucket!=_CONTRACT['input_bucket']:raise PermissionError(Bucket)
        item=_VERSIONS[Key];version=str(VersionId) if VersionId is not None else item['latest']
        return item['versions'][version].encode()
    def head_object(self,**kw):return {'ContentLength':len(self._get(**kw)),'VersionId':str(kw.get('VersionId'))}
    def get_object(self,**kw):return {'Body':io.BytesIO(self._get(**kw))}
    def copy_object(self,Bucket,Key,CopySource):
        data=self._get(**CopySource);_VERSIONS[Key]={'latest':'1','versions':{'1':data.decode()}};_COPIES.append((Bucket,Key,CopySource));return {'VersionId':'1'}
    def download_file(self,Bucket,Key,Filename):
        p=Path(Filename);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(self._get(Bucket,Key))
class Training:
    def create_training_job(self,**configuration):
        c=_CONTRACT
        if _SUBMISSIONS:raise ValueError('one job only')
        assert configuration['TrainingJobName']==c['job_name']
        assert configuration['RoleArn']==c['role']
        assert configuration['AlgorithmSpecification']['TrainingImage']==c['image']
        assert configuration['AlgorithmSpecification']['TrainingInputMode']=='File'
        resource=configuration['ResourceConfig']
        assert resource['InstanceCount']==c['max_instance_count'] and resource['InstanceType']==c['instance_type']
        assert configuration['StoppingCondition']['MaxRuntimeInSeconds']<=c['max_runtime_seconds']
        assert configuration['OutputDataConfig']['S3OutputPath']==c['output_uri']
        channels=configuration['InputDataConfig'];assert len(channels)==1
        channel=channels[0];assert channel['ChannelName']==c['channel']
        source=channel['DataSource']['S3DataSource']
        assert source['S3Uri']=='s3://'+c['input_bucket']+'/'+c['immutable_key']
        assert 'VersionId' not in source
        assert c['immutable_key'] in _VERSIONS
        assert _VERSIONS[c['immutable_key']]['versions']['1']==_VERSIONS[c['input_key']]['versions'][c['input_version']]
        _SUBMISSIONS.append(configuration)
        return {'TrainingJobArn':'arn:fixture:'+c['job_name']}
    def describe_training_job(self,TrainingJobName):
        assert _SUBMISSIONS and TrainingJobName==_CONTRACT['job_name']
        if _CASE=='failed':return {'TrainingJobStatus':'Failed','FailureReason':'authorized fixture failure'}
        if _CASE=='running':return {'TrainingJobStatus':'InProgress'}
        artifact=_CONTRACT['artifact_uri'] if _CASE!='wrong_artifact' else 's3://authorized-fixture/outputs/wrong/model.tar.gz'
        return {'TrainingJobStatus':'Completed','ModelArtifacts':{'S3ModelArtifacts':artifact}}
def client(service):
    if service=='s3':return Storage()
    if service=='sagemaker':return Training()
    raise PermissionError(service)
'''
serve='''import json,pickle,os
from pathlib import Path
from fixture_workflow import FittedModel,FittedPreprocessor
# Only the learner's trusted, provenance-verified package may be mounted here.
contract=json.loads(Path('package_contract.json').read_text())
with open(contract['package_path'],'rb') as handle:
    package=pickle.load(handle)
inputs=contract['fixed_inputs']
predictions=package['model'].predict(package['preprocessor'].transform(inputs))
print(json.dumps({'predictions':predictions,'preprocessor_mean':package['preprocessor'].mean_,'fixture_mode':os.environ.get('FIXTURE_MODE')}))
'''
bootstrap='''# Run ONLY in the authorized learner sandbox, not during registry generation.
# Supplies a local repository and runtime record; it is not the learner's solution.
import json,subprocess,sys,importlib.metadata
from pathlib import Path
root=Path.cwd()
Path('.gitignore').write_text('recorded_experiment.json\\npinned_requirements.txt\\nrequirements.txt\\n__pycache__/\\ndownloads/\\ncapture.log\\nsnapshot_record.json\\n')
subprocess.run(['git','init'],cwd=root,check=True)
subprocess.run(['git','add','.'],cwd=root,check=True)
subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-m','Authored training fixture'],cwd=root,check=True)
revision=subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=root,check=True,capture_output=True,text=True).stdout.strip()
freeze=subprocess.run([sys.executable,'-m','pip','freeze'],check=True,capture_output=True,text=True).stdout
# The authorized runtime must already contain its pinned inference dependency NumPy.
np_version=importlib.metadata.version('numpy')
Path('requirements.txt').write_text('numpy=='+np_version+'\\n',encoding='utf-8')
Path('pinned_requirements.txt').write_text(freeze,encoding='utf-8')
record={'revision':revision,'python_version':sys.version,'python_executable':sys.executable,'runtime_identity':'authorized.order.fixture','dependency_pins':freeze.splitlines(),'working_directory':str(root),'script':'recorded_training_script.py','configuration_path':'configuration.json','dataset_snapshot':json.loads(Path('snapshot_fixture.json').read_text()),'settings':json.loads(Path('configuration.json').read_text()),'expected_outcome':json.loads(Path('expected_notebook_behavior.json').read_text())['configured'],'rtol':1e-7,'atol':1e-9}
Path('recorded_experiment.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
'''
recorded_script='''import json
from fixture_workflow import supplied_workflow
if __name__ == '__main__':
    with open('configuration.json') as handle: configuration=json.load(handle)
    result=supplied_workflow(**configuration)
    print(json.dumps({'resolved_parameters':result['resolved_parameters'],'validation_accuracy':result['validation_accuracy']}))
'''
base_files={'fixture_workflow.py':common_code,'training_orders.csv':training,'protected_orders.csv':protected_csv,'fixed_orders.csv':fixed_csv,'configuration.json':dump(settings),'expected_notebook_behavior.json':dump(expected),'snapshot_fixture.json':dump(snapshot),'changed_latest.csv':changed_csv,'prepare_authorized_fixture.py':bootstrap,'recorded_training_script.py':recorded_script}
storage_state={'datasets/latest.csv':{'latest':latest_generation,'versions':{str(original_generation):training,str(latest_generation):changed_csv}},'models/B/latest.json':{'latest':latest_generation,'versions':{str(original_generation):artifact_bytes.decode(),str(latest_generation):replacement_bytes.decode()}}}
cloud_files={'google/__init__.py':'','google/cloud/__init__.py':'','google/cloud/storage.py':gcs,'storage_fixture.json':dump(storage_state)}
README='''# Authored order-training fixture
All rows, names, budgets, costs and probabilities are fictional supplied fixture values, not real-world observations. The binary target late is categorical; order_amount is a quantity, not a label. B and baseline are the only protected-comparison identities.

Mount all files together in an isolated authorized Python sandbox. Dataset CSVs match the registered base assets; changed_latest.csv matches the declared changed_latest variant. No learner implementation is prefilled. prepare_authorized_fixture.py is provisioning code: run it once in the learner sandbox with NumPy and pip already provisioned. It creates a real local fixture commit and derives requirements and runtime records from observations. Do not type replacement commit hashes, Python identities, package pins or output evidence. Learners collect fresh independent environment observations themselves.

Cloud clients provided here are explicit offline, authorized API-shape fixtures, not real cloud services. google.cloud.storage, mlflow and boto3 fixture modules make no network requests. Their counters expose submissions/version creations for checks. Real deployments require the existing authorized runtime; this registry makes no claim of cloud execution or actual image build. Docker must be available in that sandbox. Capture real image identities, State and logs there, not fabricated output. No secrets are supplied.

The model and preprocessor are supplied fitted Python objects from fixture_workflow.supplied_workflow. They deliberately use only standard-library computation. NumPy is the pinned assertion dependency collected at provisioning. The learner writes serialization and assertion checks; never unpickle untrusted test artifacts. No chart depends on seeing a rendered plot in this batch; comparison datasets and code are sufficient.
'''
scaffolds={
'mle.ml_training_script':('training_script.py','def training_entry(dataset_path="training_orders.csv", threshold=40.0):\n    raise NotImplementedError("Write imports, local task state and reporting")\n\n# Learner: add JSON handling and guarded default/configured calls.\n'),
'mle.training_dataset_version':('snapshot.py','def snapshot_dataset(bucket_name, object_name, local_path, record_path, download_path):\n    raise NotImplementedError("Import dependencies; upload, confirm, record and verify exact generation")\n'),
'mle.training_environment_record':('record_environment.py','def record_environment(repository, runtime_identity, manifest_path):\n    raise NotImplementedError("Collect actual observations, write/read JSON and verify independently")\n'),
'mle.experiment_reproduction':('reproduce.py','def reproduce(record_path="recorded_experiment.json", threshold=50.0):\n    raise NotImplementedError("Resolve recorded execution context and inspect a checked clean rerun")\n'),
'mle.model_version_registration':('register_version.py','def register_version(run_artifact_record):\n    raise NotImplementedError("Verify exact artifact, register, inspect links and return keyed verdict")\n'),
'mle.model_preprocessing_package':('package_model.py','def package_model(model, preprocessor, package_path, manifest_path):\n    raise NotImplementedError("Persist fitted state, build/inspect image and assert reproducibility")\n'),
'mle.protected_test_comparison':('evaluate_protected.py','def evaluate_protected(policy, variant="base"):\n    raise NotImplementedError("Import dependencies and compute final matched comparison without tuning")\n'),
'mle.bounded_managed_training':('submit_training.py','def run_bounded_training(contract, record_path):\n    raise NotImplementedError("Author/parse request, verify inputs, submit once, inspect and retrieve artifact")\n')}
for b in bundle['bundles']:
    cid=b['context']['concept_id'];files=dict(base_files)
    if cid in ('mle.training_dataset_version','mle.experiment_reproduction','mle.model_version_registration'):files.update(cloud_files)
    if cid=='mle.model_version_registration':
        files.update({'mlflow/__init__.py':registry_mock,'run_artifact_record.json':dump(run),'hash_mismatch_record.json':dump(mismatch),'replacement_artifact.json':replacement_bytes.decode()})
    if cid=='mle.model_preprocessing_package':
        files.update({'package_contract.json':dump(package_contract),'serve_fixture.py':serve,'Dockerfile':'# Learner: complete FROM, WORKDIR, COPY, RUN and JSON-array CMD using package_contract.json.\n','package/B/.keep':'','requirements.txt':'# Provisioning writes the observed NumPy pin; learner writes/reads the manifest.\n','compose.yaml':'# Optional runtime secret references only; no literal secret values.\n'})
    if cid=='mle.protected_test_comparison':files.update({'protected_policy.json':dump(policy),'expected_comparison.csv':comparison_csv})
    if cid=='mle.bounded_managed_training':
        output_key=managed_contract['artifact_uri'].split('/',3)[3]
        s3_state={'datasets/latest.csv':{'latest':str(latest_generation),'versions':{str(original_generation):training,str(latest_generation):changed_csv}},output_key:{'latest':'1','versions':{'1':artifact_bytes.decode()}}}
        files.update({'boto3.py':managed_mock,'managed_contract.json':dump(managed_contract),'s3_fixture.json':dump(s3_state),'managed_training_code.py':'from fixture_workflow import supplied_workflow\nfrom pathlib import Path\nimport json\nif __name__ == "__main__":\n    state=supplied_workflow("/opt/ml/input/data/training/input.csv")\n    out=Path("/opt/ml/model");out.mkdir(parents=True,exist_ok=True)\n    (out/"model.json").write_text(json.dumps({"threshold":40.0,"preprocessor_mean":state["preprocessor"].mean_}))\n'})
    path,content=scaffolds[cid];files[path]=content
    files['README.md']=README+'\n## This exercise\n'+b['practice_anchor']['objective']+'\n\n'+b['practice_anchor']['live_code']['starter_state_intent']+'\n'
    files['anchor_contract.json']=dump({'concept_id':cid,'practice_anchor':b['practice_anchor'],'visual_anchor':b['visual_anchor']})
    files['fixture_checks.json']=dump({'cases':['default versus explicit override','changed latest does not change original generation','nonexistent generation rejected','changed revision/dependency/runtime rejected','wrong working directory not accepted','hash mismatch creates zero registry versions','existing B and new-name baseline registry paths','preserved fitted preprocessing and predictions','false assertion raises without optimization','protected empty conditioning groups remain undefined','protected failures never change frozen choice','managed completed/failed/running/wrong_artifact cases'], 'note':'Execute only cases belonging to this anchor; expected numeric outputs are supplied by the computed fixture records.'})
    assets.append(dict(asset_id='ws.'+cid.split('.',1)[1],asset_kind='code_workspace',scenario_id=SID,title=b['context']['concept_name'],runtime='python',files=[dict(path=p,content=c) for p,c in sorted(files.items())]))
# Mine existing teaching and anchor vocabulary, rather than inventing source examples.
vocab=[]
for b in bundle['bundles']:
    texts=[t['content'] for t in b['teaching_blocks']]+[json.dumps(b['practice_anchor'],ensure_ascii=False),json.dumps(b['visual_anchor'],ensure_ascii=False)]
    joined='\n'.join(texts)
    for term in re.findall(r'\b(?:[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)+|__[A-Za-z_]+__|[A-Z][A-Za-z]+(?:[A-Z][a-z]*)+)\b|/opt/ml/(?:input/data(?:/CHANNEL)?|model)|/app|\b(?:B|baseline|JSON|Python|Dockerfile|Compose|SHA-256|FPR|FNR|FP|TN|FN|TP|pickle|git|pip|SageMaker|MlflowClient|Google Cloud Storage|Object Versioning)\b',joined):
        if term not in vocab:vocab.append(term)
reg=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=bundle['path_id'],batch_id=B.name,scenarios=[dict(scenario_id=SID,name='Reproduce and package a fictional order-training experiment',summary='A small fictional order team turns a notebook workflow into a verified, reproducible run, registers its exact artifact, packages fitted state, compares frozen B with baseline on protected orders, and runs one authorized bounded managed-training fixture. All data and resource settings are authored examples.',domain='order-model training lineage and reproducible release',glossary_example_vocab=vocab)],assets=assets)
(B/'scenario_asset_registry.json').write_text(dump(reg))
# Self-check the mistakes-to-avoid list against every authored row and op.
for a in assets:
    if a['asset_kind']!='dataset':continue
    names=[c['name'] for c in a['columns']]
    assert len(names)==len(set(names))
    assert all(len(row)==len(names) for row in a['rows'])
    for c in a['columns']:
        assert c['semantic_role']!='numerical' or c['type'] in ('integer','number')
        assert not c['numeric_looking_label'] or c['semantic_role'] in ('identifier','categorical')
    for v in a.get('variants',[]):
        rows=[dict(zip(names,row)) for row in a['rows']]
        for op in v['ops']:
            matches=[i for i,r in enumerate(rows) if all(r.get(k)==value for k,value in op['where'].items())]
            assert matches
            if op['op']=='set_cell':rows[matches[op.get('occurrence',0)]][op['column']]=op['value']
            elif op['op']=='drop_rows':rows=[r for i,r in enumerate(rows) if i not in matches]
        assert not v['planted_issues'] # these are valid alternate/empty-cohort edge cases, not errors
assert len([a for a in assets if a['asset_kind']=='code_workspace'])==len(bundle['bundles'])
assert set(scaffolds)=={b['context']['concept_id'] for b in bundle['bundles']}
assert all(r[-1]=='undefined' for r in comparison if r[0]!='base')
print(dump({'concepts':len(bundle['bundles']),'scenarios':len(reg['scenarios']),'datasets':sum(a['asset_kind']=='dataset' for a in assets),'workspaces':sum(a['asset_kind']=='code_workspace' for a in assets),'base_rows':sum(len(a.get('rows',[])) for a in assets),'variants':sum(len(a.get('variants',[])) for a in assets),'asset_ids':[a['asset_id'] for a in assets],'checklist':'PASS: widths, roles, ops and occurrence; no planted issues; all concepts covered; no named source column omitted; outputs/hashes computed; code/comparison anchors require no plot.'}))
