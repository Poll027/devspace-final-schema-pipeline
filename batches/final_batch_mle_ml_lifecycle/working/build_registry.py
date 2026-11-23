import json, hashlib, csv, io, copy, re
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
SID='scenario.ml_lifecycle'
assets=[]
def dataset(aid,title,cols,rows,variants=None):
 a=dict(asset_id=aid,asset_kind='dataset',scenario_id=SID,title=title,description='Authored fictional fixtures, not observed production data.',columns=[dict(name=n,type=t,semantic_role=r,**({'numeric_looking_label':True} if r=='identifier' and any(str(row[i]).isdigit() for row in rows) else {})) for i,(n,t,r) in enumerate(cols)],rows=rows,provenance='authored')
 if variants:a['variants']=variants
 assets.append(a);return a
def file(path,content):return dict(path=path,content=content)
def jf(path,obj):return file(path,json.dumps(obj,indent=2)+'\n')
def csvfile(a,path):
 s=io.StringIO();w=csv.writer(s,lineterminator='\n');w.writerow([c['name'] for c in a['columns']]);w.writerows(a['rows']);return file(path,s.getvalue())
def digest(x):return hashlib.sha256(x.encode()).hexdigest()
def variant(vid,aid,ops,issues=[],purpose='Declared edge fixture'):
 return dict(variant_id=vid,derived_from=aid,purpose=purpose,ops=ops,planted_issues=issues)
def issue(i,k,where,column,description,rule=None,occurrence=0):
 d=dict(issue_id=i,kind=k,locations=[dict(where=where,occurrence=occurrence,column=column)],description=description)
 if rule:d['rule']=rule
 return d
train=dataset('ds.dataset_snapshot','Dataset snapshot with feature and aligned binary target', [('sample_id','string','identifier'),('feature','number','numerical'),('label','integer','categorical')], [['sample.101',0,0],['sample.102',1,0],['sample.103',2,1],['sample.104',3,1],['sample.105',4,1],['sample.106',5,1]])
train['variants']=[variant('missing_feature',train['asset_id'],[dict(op='drop_columns',columns=['feature'])],purpose='Required feature is absent; required schema check must fail.'),variant('unexpected_feature',train['asset_id'],[dict(op='drop_columns',columns=['label'])],purpose='Missing target schema failure; unexpected feature fixture is supplied in workspace JSON.'),variant('invalid_feature',train['asset_id'],[dict(op='set_cell',where={'sample_id':'sample.103'},column='feature',value=-1)],[issue('issue.negative_feature','impossible_value',{'sample_id':'sample.103'},'feature','Feature violates the declared nonnegative fixture contract.',dict(column='feature',op='lt',value=0))]),variant('missing_value',train['asset_id'],[dict(op='set_cell',where={'sample_id':'sample.104'},column='feature',value=None)],[issue('issue.missing_feature_value','missing_value',{'sample_id':'sample.104'},'feature','Required feature value is missing.')]),variant('duplicate_sample',train['asset_id'],[dict(op='duplicate_row',where={'sample_id':'sample.102'},insert='end')],[issue('issue.duplicate_sample','duplicate_row',{'sample_id':'sample.102'},'sample_id','Second occurrence duplicates the complete sample row.',occurrence=1)])]
# Do not misname an edge case.
train['variants'][1]['variant_id']='missing_target'
behavior=dataset('ds.behavior_inputs','Packaged inference fixtures', [('sample_id','string','identifier'),('feature','number','numerical'),('target','integer','categorical')],[['sample.201',0,0],['sample.202',1,0],['sample.203',2,1],['sample.204',5,1]])
behavior['variants']=[variant('boundary',behavior['asset_id'],[dict(op='drop_rows',where={'sample_id':s}) for s in ['sample.202','sample.203','sample.204']]),variant('malformed',behavior['asset_id'],[dict(op='set_cell',where={'sample_id':'sample.203'},column='feature',value='bad')],[issue('issue.behavior_type','wrong_type',{'sample_id':'sample.203'},'feature','The packaged contract requires a number.',dict(column='feature',op='eq',value='bad'))]),variant('negative',behavior['asset_id'],[dict(op='set_cell',where={'sample_id':'sample.202'},column='feature',value=-1)],[issue('issue.behavior_negative','impossible_value',{'sample_id':'sample.202'},'feature','Input is outside the declared boundary.',dict(column='feature',op='lt',value=0))])]
release=dataset('ds.release_evidence','Binary validation and fixed operating evidence', [('candidate_id','string','identifier'),('FP','integer','numerical'),('TN','integer','numerical'),('FN','integer','numerical'),('TP','integer','numerical'),('latency_ms','number','numerical'),('operating_ok','boolean','categorical'),('evidence_complete','boolean','categorical')],[['reference',10,90,10,90,18,True,True],['A',5,95,5,95,20,True,True],['B',4,96,4,96,21,True,True],['boundary',10,90,10,90,20,True,True],['empty_negatives',0,0,5,95,15,True,True],['empty_positives',5,95,0,0,15,True,True],['incomplete',5,95,5,95,None,True,False],['cost_failure',40,60,40,60,15,True,True],['operating_failure',5,95,5,95,15,False,True]])
release['variants']=[variant('failed_latency',release['asset_id'],[dict(op='set_cell',where={'candidate_id':'A'},column='latency_ms',value=21)],[issue('issue.latency','impossible_value',{'candidate_id':'A'},'latency_ms','Exceeds the predeclared fictional release limit, not a physically impossible latency.',dict(column='latency_ms',op='gt',value=20))])]
# Policy failures are not physically impossible values. Keep this as a declared edge, not a misleading data-quality issue.
release['variants'][0]['planted_issues']=[]
artifacts={'A':'fictional fitted package A\npreprocess: divide feature by 5\nthreshold: 0.4\n','B':'fictional fitted package B\npreprocess: divide feature by 5\nthreshold: 0.5\n'}
artifact_rows=[[k,f'gs://fixture-artifacts/{k}.txt',1,digest(v),True] for k,v in artifacts.items()]
artifact_ds=dataset('ds.artifact_records','Immutable named output records', [('artifact_id','string','identifier'),('uri','string','identifier'),('generation','integer','identifier'),('sha256','string','identifier'),('validation_ok','boolean','categorical')],artifact_rows)
artifact_ds['variants']=[variant('invalid_existing',artifact_ds['asset_id'],[dict(op='set_cell',where={'artifact_id':'A'},column='validation_ok',value=False)],purpose='Existing output has failed validation and cannot be reused.')]
# A reproducible local repository fixture: compute the Git object identities from authored bytes, never type a revision.
source='"""Fictional package source retained for lineage inspection."""\ndef transform(feature):\n    return feature / 5.0\n'
def git_hash(kind,body):return hashlib.sha1(f'{kind} {len(body)}\0'.encode()+body).hexdigest()
blob=git_hash('blob',source.encode());tree_body=b'100644 model_source.py\0'+bytes.fromhex(blob);tree=git_hash('tree',tree_body)
identity='Fixture Author <fixture@example.invalid> 1700000000 +0000'
commit_body=f'tree {tree}\nauthor {identity}\ncommitter {identity}\n\nAuthored lineage fixture\n'.encode();revision=git_hash('commit',commit_body)
config={'feature_scale':5.0,'threshold':0.4,'package':'A'}
config_hash=digest(json.dumps(config,sort_keys=True,separators=(',',':')))
snapshot_hash=digest(csvfile(train,'dataset.csv')['content'])
lineage={'deployment':{'deployment_id':'deployment.A','registry_version':'1','artifact_id':'A'},'registry':{'1':{'model_name':'fixture_model','version':'1','artifact_id':'A','artifact_source':'gs://fixture-artifacts/A.txt','generation':1,'sha256':digest(artifacts['A']),'run_id':'run.A'}},'runs':{'run.A':{'run_id':'run.A','artifact_id':'A','artifact_sha256':digest(artifacts['A']),'dataset_id':'snapshot.A','configuration_id':'config.A','code_id':'code.A'}},'approval':{'approval_id':'approval.A','registry_version':'1','artifact_id':'A','authorized':True,'accountable_identity':'fixture-promoter'},'datasets':{'snapshot.A':{'sha256':snapshot_hash,'file':'dataset.csv'}},'configurations':{'config.A':{'sha256':config_hash,'resolved':config}},'artifacts':{r[0]:dict(zip([c['name'] for c in artifact_ds['columns']],r)) for r in artifact_ds['rows']},'code':{'code.A':{'revision':revision,'repository':'local_repo'}}}
lineage_cases={'valid':lineage,'boundary_same_name_other_version':copy.deepcopy(lineage),'approval_A_deployment_B':copy.deepcopy(lineage),'missing_run_link':copy.deepcopy(lineage),'wrong_generation':copy.deepcopy(lineage),'missing_code_revision':copy.deepcopy(lineage),'configuration_mismatch':copy.deepcopy(lineage),'dataset_mismatch':copy.deepcopy(lineage)}
l=lineage_cases['boundary_same_name_other_version'];l['registry']['2']=copy.deepcopy(l['registry']['1']);l['registry']['2']['version']='2' # unselected version must not confuse resolution
l=lineage_cases['approval_A_deployment_B'];l['deployment']['artifact_id']='B'
lineage_cases['missing_run_link']['registry']['1'].pop('run_id')
lineage_cases['wrong_generation']['registry']['1']['generation']=2
lineage_cases['missing_code_revision']['code']['code.A']['revision']='refs/heads/not-present'
lineage_cases['configuration_mismatch']['configurations']['config.A']['sha256']=digest('different configuration')
lineage_cases['dataset_mismatch']['datasets']['snapshot.A']['sha256']=digest('different dataset')
lineage_ds=dataset('ds.lineage_links','Deployment, approval and run identity links', [('case_id','string','identifier'),('deployment_artifact','string','identifier'),('approved_artifact','string','identifier'),('registry_version','integer','identifier'),('run_id','string','identifier'),('dataset_id','string','identifier'),('configuration_id','string','identifier'),('code_revision','string','identifier')],[[name,l['deployment']['artifact_id'],l['approval']['artifact_id'],int(l['deployment']['registry_version']),l['registry']['1'].get('run_id'),l['runs']['run.A']['dataset_id'],l['runs']['run.A']['configuration_id'],l['code']['code.A']['revision']] for name,l in lineage_cases.items()])
terms=['Cloud Build','YAML','JSON','steps','name','args','script','id','waitFor','allowFailure','allowExitCodes','PyYAML','yaml.safe_dump','yaml.safe_load','assert','AssertionError','NumPy','np.testing.assert_allclose','rtol','atol','FP','TN','FN','TP','FPR','FNR','cost_FP','cost_FN','P(Y=0)','P(Y=1)','Pub/Sub','A','B','Secret Manager','availableSecrets.secretManager','secretEnv','Cloud Storage','blob.exists()','blob.reload()','blob.generation','if_generation_match=0','412','hashlib.sha256','git rev-parse','git show','deployment','registry','run','approval','dataset','configuration','artifact','code','generation','snapshot','branch filter','commit trigger','latency']
text='\n'.join(t['content'] for b in g['bundles'] for t in b['teaching_blocks'])+'\n'+'\n'.join(json.dumps({k:b[k] for k in ['assessment_anchors','practice_anchor','visual_anchor']}) for b in g['bundles'])
vocab=[term for term in terms if term.lower() in text.lower()]
common_readme='''# Fictional lifecycle fixture runtime
All rows, limits, identities, bucket/project names and events here are authored examples, not production claims. This is a bounded local simulator of an existing configured pipeline; no cloud requests or policy changes are authorized. A hosted exercise must replace the simulator adapter with its existing authorized runtime before describing results as actual Cloud Build results.

Python 3, numpy and PyYAML are declared dependencies. Files under fixtures/ are inputs and contracts, not answer implementations. learner.py deliberately contains no imports, assertions or gate implementation. Keep protected-test observations out of fitting and tuning. Do not introduce hard-coded fixture verdicts.

Existing build configuration uses the declared step IDs, execution images and entry points. Learners wire the assigned entry point, waitFor edges and fatal gate handling, then safe_dump/safe_load and inspect resolved fields. Existing triggers.json supplies bounded repository-commit and Pub/Sub bindings/filters: do not create triggers or alter filters. Accepted/rejected events are inputs, never captured run output. runtime_sim.py executes Python entry points and captures statuses, resolved args and output; results must be produced by running it, not invented. Required stages cannot use allowFailure or allowed failing exit codes.

Object storage is explicitly simulated by storage_sim.py. It supports exists/reload/generation/download_as_bytes(if_generation_match=...) and upload_from_filename(if_generation_match=0), raises PreconditionFailed with status 412, and records uploads. Injected 412 is a race that creates an output before the failing call returns; recovery must reload and verify. Required validation is supplied per artifact in fixture records; a hash match does not imply a validation pass. No credential values are stored here.
'''
triggers={'repository_commit':{'id':'fixture-commit-trigger','repository':'local_repo','branch_filter':'^main$','bindings':{'_SNAPSHOT':'snapshot_id'},'fixtures':[{'branch':'main','snapshot_id':'valid'},{'branch':'main','snapshot_id':'missing_required_feature'},{'branch':'other','snapshot_id':'valid'}]},'pubsub':{'id':'fixture-artifact-trigger','topic':'projects/fixture-project/topics/artifacts','bindings':{'_CASE':'case_id','_ARTIFACT':'artifact_id'},'filters':{'event_type':'artifact_ready'},'fixtures':[{'event_type':'artifact_ready','case_id':'accepted','artifact_id':'A'},{'event_type':'artifact_ready','case_id':'rejected','artifact_id':'B'},{'event_type':'unrelated','case_id':'accepted','artifact_id':'A'}]}}
storage_code='''"""Bounded local Cloud Storage interface, never a real cloud client."""
from pathlib import Path
class PreconditionFailed(Exception):
    status_code = 412
class RecoverableFailure(Exception):
    pass
class StorageClient:
    def __init__(self, initial=None, race=None):
        self.objects = dict(initial or {})
        self.race = dict(race or {})
        self.uploads = []
        self.requests = []
    def blob(self, name):
        return Blob(self, name)
class Blob:
    def __init__(self, client, name):
        self.client, self.name = client, name
        self.generation = None
    def exists(self):
        return self.name in self.client.objects
    def reload(self):
        self.generation = self.client.objects[self.name]["generation"]
    def download_as_bytes(self, if_generation_match):
        self.client.requests.append((self.name, if_generation_match))
        obj = self.client.objects[self.name]
        if obj["generation"] != if_generation_match:
            raise PreconditionFailed("generation mismatch")
        return obj["data"]
    def upload_from_filename(self, path, if_generation_match):
        if if_generation_match != 0:
            raise ValueError("fixture contract permits create-only upload")
        if self.name in self.client.race:
            self.client.objects[self.name] = self.client.race.pop(self.name)
            raise PreconditionFailed("412 concurrent creation")
        if self.exists():
            raise PreconditionFailed("412 already exists")
        self.client.objects[self.name] = {"generation": 1, "data": Path(path).read_bytes()}
        self.client.uploads.append(self.name)
        self.reload()
'''
prediction_reference_code = '\n'.join([
    '"""Underlying fitted preprocessing and inference, shared by the supplied package."""',
    'import math',
    'class InputContractError(ValueError):',
    '    pass',
    'def predict_records(records):',
    '    ids, values = [], []',
    '    for row in records:',
    '        if set(row) != {"sample_id", "feature"}:',
    '            raise InputContractError("required input columns")',
    '        x = row["feature"]',
    '        if isinstance(x, bool) or not isinstance(x, (int,float)) or not math.isfinite(x) or not 0 <= x <= 5:',
    '            raise InputContractError("feature must be finite in [0,5]")',
    '        ids.append(row["sample_id"])',
    '        values.append([float(x / 5.0 >= 0.4)])',
    '    return {"sample_ids": ids, "values": values}',
]) + '\n'
prediction_code = '\n'.join([
    '"""Supplied fitted package, including preprocessing through its inference path."""',
    'import numpy as np',
    'from prediction_reference import predict_records, InputContractError',
    'class FittedPackage:',
    '    def __init__(self, regression=None):',
    '        self.regression = regression',
    '    def predict(self, records):',
    '        result = predict_records(records)',
    '        ids = result["sample_ids"]',
    '        values = np.array(result["values"], dtype=float).reshape((-1,1))',
    '        if self.regression == "reverse_rows":',
    '            ids, values = ids[::-1], values[::-1]',
    '        elif self.regression == "wrong_shape":',
    '            values = values.ravel()',
    '        elif self.regression == "wrong_values":',
    '            values = values + 0.1',
    '        elif self.regression == "drops_row":',
    '            ids, values = ids[:-1], values[:-1]',
    '        return {"sample_ids": ids, "values": values}',
    'predict = FittedPackage().predict',
]) + '\n'
# Compute expected outputs by executing the supplied prediction package.
ns={};exec(prediction_reference_code,ns)
b_inputs=[{'sample_id':r[0],'feature':r[1]} for r in behavior['rows']]
b_cases={}
for name,inputs in [('valid',b_inputs),('boundary_low',[b_inputs[0]]),('boundary_high',[b_inputs[-1]]),('empty',[])]:
 out=ns['predict_records'](inputs);b_cases[name]={'inputs':inputs,'expected_sample_ids':out['sample_ids'],'expected_values':out['values'],'expected_shape':[len(out['values']),1]}
b_cases['malformed']={'inputs':[{'sample_id':'sample.203','feature':'bad'}],'expected_exception':'InputContractError'}
b_cases['missing_feature']={'inputs':[{'sample_id':'sample.203'}],'expected_exception':'InputContractError'}
b_cases['out_of_bounds']={'inputs':[{'sample_id':'sample.203','feature':-1}],'expected_exception':'InputContractError'}
base_rows=[dict(zip([c['name'] for c in train['columns']],r)) for r in train['rows']]
data_cases={'valid':base_rows,'boundary':[base_rows[0],base_rows[-1]],'missing_required_feature':[{k:v for k,v in row.items() if k!='feature'} for row in base_rows],'unexpected_feature':[dict(row,extra=1) for row in base_rows],'invalid_feature':copy.deepcopy(base_rows),'missing_value':copy.deepcopy(base_rows),'duplicate_sample':base_rows+[base_rows[1]]}
data_cases['invalid_feature'][2]['feature']=-1;data_cases['missing_value'][3]['feature']=None
snapshot_cases={k:{'snapshot_id':'snapshot.'+k,'sha256':digest(json.dumps(v,sort_keys=True,separators=(',',':'))),'rows':v} for k,v in data_cases.items()}
release_records={r[0]:dict(zip([c['name'] for c in release['columns']],r)) for r in release['rows']}
release_contract={'probabilities':{'P(Y=0)':0.8,'P(Y=1)':0.2},'costs':{'cost_FP':1,'cost_FN':4,'correct_prediction':0},'max_expected_error_cost':0.16,'max_latency_ms':20,'accepted_reference':'reference','requirements':['all evidence fields present','nonnegative integer counts','both actual-class denominators nonempty','candidate identity matches event','expected error cost <= fixed maximum and <= accepted reference cost','latency_ms <= fixed maximum','operating_ok is True','evidence_complete is True'],'protected_test_use':'Never fit, select, or tune using protected-test observations.'}
dependencies={'valid':{'data_validation':{'consumed':'snapshot.A','parameters':{'contract':'dataset_contract'},'produced':'validated.snapshot.A','validation_ok':True},'training':{'consumed':'validated.snapshot.A','parameters':config,'produced':'A'},'model_validation':{'consumed':'A','parameters':{'rtol':1e-7,'atol':1e-8},'produced':'validated.A','validation_ok':True}},'mismatch':{},'rejected_data':{},'boundary':{}}
for k in ['mismatch','rejected_data','boundary']:dependencies[k]=copy.deepcopy(dependencies['valid'])
dependencies['mismatch']['model_validation']['consumed']='B';dependencies['rejected_data']['data_validation']['validation_ok']=False
promotion_cases={'accepted':{'registry_version':'1','artifact_id':'A','run_id':'run.A','approval':lineage['approval'],'compatibility_ok':True,'offline_validation_ok':True,'staged_validation_ok':True,'staged_artifact_id':'A'},'unauthorized':{},'wrong_artifact':{},'failed_staging':{}}
for k in ['unauthorized','wrong_artifact','failed_staging']:promotion_cases[k]=copy.deepcopy(promotion_cases['accepted'])
promotion_cases['unauthorized']['approval']['authorized']=False;promotion_cases['wrong_artifact']['artifact_id']='B';promotion_cases['failed_staging']['staged_validation_ok']=False
recovery_cases={'accepted':{'initial_outputs':['A'],'race_outputs':[],'invalid_outputs':[],'gate_ok':True,'exception':'RecoverableFailure'},'boundary_completed':{'initial_outputs':['A','B'],'race_outputs':[],'invalid_outputs':[],'gate_ok':True,'exception':None},'race_412':{'initial_outputs':['A'],'race_outputs':['B'],'invalid_outputs':[],'gate_ok':True,'exception':'RecoverableFailure'},'invalid_existing':{'initial_outputs':['A'],'race_outputs':[],'invalid_outputs':['A'],'gate_ok':True,'exception':'RecoverableFailure'},'conflicting_content':{'initial_outputs':['A'],'race_outputs':[],'invalid_outputs':[],'conflicting_outputs':['A'],'gate_ok':True,'exception':'RecoverableFailure'},'rejected_gate':{'initial_outputs':['A'],'race_outputs':[],'invalid_outputs':[],'gate_ok':False,'exception':'RecoverableFailure'},'unrelated_failure':{'initial_outputs':['A'],'race_outputs':[],'invalid_outputs':[],'gate_ok':True,'exception':'ValueError'}}
# No acceptance/gate solution is supplied. Executable runtime only schedules the existing entry points.
runtime_code='''"""Offline execution adapter. Statuses are generated, never fixture answers."""
import json
import subprocess
import sys
import yaml
from pathlib import Path

def run_build(config_path, trigger_kind, event):
    config = yaml.safe_load(Path(config_path).read_text())
    triggers = json.loads(Path("triggers.json").read_text())
    trigger = triggers[trigger_kind]
    if trigger_kind == "repository_commit":
        import re
        if re.fullmatch(trigger["branch_filter"], event.get("branch", "")) is None:
            return {"triggered": False, "steps": []}
    elif any(event.get(k) != v for k, v in trigger["filters"].items()):
        return {"triggered": False, "steps": []}
    bindings = dict(config.get("substitutions", {}))
    bindings.update({k: event[field] for k, field in trigger["bindings"].items()})
    results, by_id = [], {}
    pending = list(config["steps"])
    while pending:
        progress = False
        for step in list(pending):
            i = config["steps"].index(step)
            dependencies = step.get("waitFor", [s["id"] for s in config["steps"][:i]])
            dependencies = [d for d in dependencies if d != "-"]
            if any(d not in by_id for d in dependencies):
                continue
            args = [str(a) for a in step.get("args", [])]
            for j, arg in enumerate(args):
                for key, value in bindings.items():
                    arg = arg.replace("${" + key + "}", str(value)).replace(key, str(value))
                args[j] = arg
            record = {"id": step["id"], "name": step["name"], "resolved_args": args, "waitFor": dependencies}
            if any(by_id[d]["status"] != "SUCCESS" for d in dependencies):
                record.update(status="NOT_STARTED", exit_code=None, output="")
            else:
                if step.get("allowFailure") or any(x != 0 for x in step.get("allowExitCodes", [])):
                    raise ValueError("required gate failures must be fatal")
                if not args or args[0] != "python":
                    raise ValueError("bounded adapter only supports declared Python entry points")
                p = subprocess.run([sys.executable] + args[1:], text=True, capture_output=True)
                record.update(status="SUCCESS" if p.returncode == 0 else "FAILURE", exit_code=p.returncode, output=p.stdout+p.stderr)
            results.append(record); by_id[step["id"]] = record
            pending.remove(step); progress = True
        if not progress:
            raise ValueError("missing dependency or cycle")
    return {"triggered": True, "resolved_inputs": bindings, "steps": results}
'''
training_entry='''"""Existing training entry point, kept unchanged by dataset-gate exercises."""
import json
import sys
from pathlib import Path
if __name__ == "__main__":
    snapshot_id = sys.argv[1]
    Path("training_invocation.json").write_text(json.dumps({"snapshot_id": snapshot_id, "started": True}))
'''
bootstrap=f'''"""Run in the exercise runtime only; creates the supplied local repo fixture."""
from pathlib import Path
import subprocess
import os
root = Path("local_repo")
root.mkdir(exist_ok=True)
(root / "model_source.py").write_text({source!r})
env = dict(os.environ, GIT_AUTHOR_DATE="1700000000 +0000", GIT_COMMITTER_DATE="1700000000 +0000", GIT_CONFIG_NOSYSTEM="1")
def run(*args):
    return subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True, text=True).stdout.strip()
run("init", "--initial-branch=main")
run("config", "user.name", "Fixture Author")
run("config", "user.email", "fixture@example.invalid")
run("config", "core.autocrlf", "false")
run("add", "model_source.py")
run("-c", "commit.gpgsign=false", "commit", "-m", "Authored lineage fixture")
assert run("rev-parse", "HEAD") == {revision!r}
'''
# Stage configurations are intentionally incomplete assignments (not broken secret/identity policies).
configs={
 'mle.dataset_quality_gate':[('quality','learner.py',['${_SNAPSHOT}'],['-']),('training','training_entry.py',['${_SNAPSHOT}'],[])],
 'mle.model_behavior_tests':[('behavior_tests','learner.py',['${_CASE}'],['-']),('release_gate','downstream_entry.py',['${_ARTIFACT}'],[])],
 'mle.model_release_quality_gate':[('release_gate','learner.py',['${_CASE}','${_ARTIFACT}'],['-']),('promotion','downstream_entry.py',['${_ARTIFACT}'],[])],
 'mle.pipeline_artifact_dependencies':[('data_validation','learner.py',['${_CASE}'],['-']),('training','downstream_entry.py',['${_ARTIFACT}'],[]),('model_validation','learner.py',['${_CASE}','B'],[])],
 'mle.staged_ml_promotion':[('compatibility','learner.py',['${_CASE}'],['-']),('staging_quality','learner.py',['${_CASE}'],[]),('authorization','learner.py',['${_CASE}'],[]),('production','downstream_entry.py',['${_ARTIFACT}'],[])],
 'mle.pipeline_failure_recovery':[('recovery','learner.py',['${_CASE}'],['-']),('required_validation','learner.py',['${_CASE}'],[]),('promotion','downstream_entry.py',['${_ARTIFACT}'],[])],
 'mle.deployed_model_lineage_audit':[('lineage_audit','learner.py',['${_CASE}'],['-'])]}
# Empty waitFor means assignment missing: learner must establish actual explicit dependencies.
for b in g['bundles']:
 cid=b['context']['concept_id']; short=cid.split('.')[-1]
 cfg={'steps':[{'id':i,'name':'python:3.11','args':['python',p]+args,'waitFor':wait} for i,p,args,wait in configs[cid]],'substitutions':{'_SNAPSHOT':'valid','_CASE':'accepted','_ARTIFACT':'A'},'serviceAccount':'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
 if cid=='mle.staged_ml_promotion':
  cfg['availableSecrets']={'secretManager':[{'versionName':'projects/fixture-project/secrets/promotion-token/versions/1','env':'PROMOTION_TOKEN'}]};cfg['steps'][-1]['secretEnv']=['PROMOTION_TOKEN']
 files=[file('README.md',common_readme),file('requirements.txt','numpy\nPyYAML\n'),file('learner.py',f'"""Assignment: {b["coverage"]["learning_objective"]}"""\n# Write the required imports, implementation, assertions and fatal CLI entry point.\nraise NotImplementedError("Learner entry point is intentionally unwritten")\n'),file('cloudbuild.yaml',json.dumps(cfg,indent=2)+'\n'),jf('triggers.json',triggers),file('runtime_sim.py',runtime_code),file('storage_sim.py',storage_code),jf('fixtures/anchor_contract.json',b['practice_anchor']),jf('fixtures/visual_intent.json',b['visual_anchor']),file('training_entry.py',training_entry),file('downstream_entry.py','"""Supplied downstream execution marker; no gate bypass."""\nimport json\nimport sys\nfrom pathlib import Path\nif __name__ == "__main__":\n    Path("downstream_invocation.json").write_text(json.dumps({"artifact_id": sys.argv[1], "started": True}))\n')]
 for k,v in artifacts.items():files.append(file(f'outputs/{k}.txt',v))
 files.append(jf('fixtures/artifacts.json',lineage['artifacts']))
 if cid=='mle.dataset_quality_gate':
  files.extend([csvfile(train,'dataset.csv'),jf('fixtures/dataset_cases.json',snapshot_cases),jf('fixtures/dataset_contract.json',{'columns':{'sample_id':'unique nonempty string label','feature':'finite number in [0,5], inclusive','label':'integer category 0 or 1'},'schema_policy':'exactly declared columns','required_checks':['schema','feature_values','label_values','unique_sample_id'],'gate_policy':'all required named checks must be present and true; otherwise raise or exit nonzero','evidence':'retain snapshot_id, sha256, named results and failed checks; repaired inputs use unchanged requirements'})])
 elif cid=='mle.model_behavior_tests':
  files.extend([csvfile(behavior,'behavior.csv'),file('prediction_package.py',prediction_code),file('prediction_reference.py',prediction_reference_code),jf('fixtures/behavior_cases.json',b_cases),jf('fixtures/behavior_contract.json',{'rtol':1e-7,'atol':1e-8,'output_shape':'(n,1)','expected_correspondence':'returned sample_ids exactly match fixture input order','empty_input':'permitted with shape (0,1)','regressions':['reverse_rows','wrong_shape','wrong_values','drops_row'],'exception':'prediction_package.InputContractError','order':'check count, alignment and shape before assert_allclose'})])
 elif cid=='mle.model_release_quality_gate':
  files.extend([csvfile(release,'release_evidence.csv'),jf('fixtures/release_cases.json',release_records),jf('fixtures/release_contract.json',release_contract)])
 elif cid=='mle.pipeline_artifact_dependencies':
  files.extend([jf('fixtures/dependency_cases.json',dependencies),jf('fixtures/dependency_contract.json',{'required_edges':[['data_validation','training'],['training','model_validation']],'checks':['producer immutable identity equals consumer reference','validation result before dependent execution','resolved run args agree with dependency dictionary'],'assignment':'repair training A / model-validation B mismatch and configure explicit waitFor edges'})])
 elif cid=='mle.staged_ml_promotion':
  files.extend([jf('fixtures/promotion_cases.json',promotion_cases),jf('fixtures/registry.json',lineage['registry']),jf('fixtures/promotion_contract.json',{'scope':'fixture-promoter may promote approved artifact A, registry version 1, only','required_results':['compatibility','offline_validation','staged_validation','authorization'],'record_fields':['approval','accountable_identity','registry_version','run_id','artifact_id','per_stage_results'],'secret_reference_only':'PROMOTION_TOKEN is provided only by the authorized runtime to production. Do not serialize or echo it; inspect captured output without displaying its value. The local adapter never supplies real credentials.'})])
 elif cid=='mle.pipeline_failure_recovery':
  files.extend([jf('fixtures/recovery_cases.json',recovery_cases),jf('fixtures/recovery_contract.json',{'injection_point':'after A upload before B','recoverable_exception':'storage_sim.RecoverableFailure','precondition_exception':'storage_sim.PreconditionFailed','outputs':lineage['artifacts'],'requirements':['record and isolate failure','verify exact existing generation bytes/hash and validation','skip only verified completed upload','create missing output with if_generation_match=0','on 412 reload and verify, never overwrite','unrelated exceptions remain fatal','run retried stage and downstream required gates','second call preserves generations and upload counts but revalidates'],'evidence_fields':['initial_and_final_generations','hashes','validation_results','upload_counts','retry_status','downstream_status','resolved_inputs']})])
 elif cid=='mle.deployed_model_lineage_audit':
  files.extend([csvfile(train,'dataset.csv'),jf('fixtures/lineage_cases.json',lineage_cases),file('bootstrap_local_repo.py',bootstrap),file('model_source.py',source),jf('fixtures/lineage_contract.json',{'repository_setup':'Run bootstrap_local_repo.py once in the exercise runtime; audit must independently inspect the recorded revision with both required git commands. No local repository was created by this stage.','hash_algorithm':'sha256','configuration_serialization':'json.dumps(resolved,sort_keys=True,separators=(comma,colon)).encode()','edge_checks':['deployment to registry','approval to deployed artifact/version','registry to artifact exact source/generation/hash and originating run','run to dataset content identity','run to resolved configuration identity','run to artifact identity','code revision to existing local commit'],'failure_handling':'report the explicit missing or mismatched edge, never infer links from names','boundary_case':'a second unselected registry version with the same model name does not invalidate the selected exact version'})])
 assets.append(dict(asset_id='ws.'+short,asset_kind='code_workspace',scenario_id=SID,title=b['context']['concept_name']+' — local fixture workspace',runtime='python',files=files))
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=g['path_id'],batch_id=B.name,scenarios=[dict(scenario_id=SID,name='Fictional classification release pipeline',summary='A fictional internal ML team validates a binary classifier, carries immutable named artifacts A and B through a configured local lifecycle fixture, and audits code, data, configuration and approval links. All records and limits are authored examples. Cloud and trigger interfaces are bounded simulations; hosted runs require the existing authorized runtime.',domain='machine-learning lifecycle',glossary_example_vocab=vocab)],assets=assets)
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
print('scenarios',len(registry['scenarios']),'assets',len(assets),'datasets',sum(a['asset_kind']=='dataset' for a in assets),'workspaces',sum(a['asset_kind']=='code_workspace' for a in assets),'rows',sum(len(a.get('rows',[])) for a in assets),'files',sum(len(a.get('files',[])) for a in assets))
