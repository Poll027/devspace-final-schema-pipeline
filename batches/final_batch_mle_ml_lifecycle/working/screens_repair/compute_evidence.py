import os, json, sys, subprocess, hashlib, importlib.util, copy
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent

def load(p): return json.loads(Path(p).read_text())
def dump(x): return json.dumps(x,indent=2)
def sha(b): return hashlib.sha256(b).hexdigest()
COMMON='''import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())
'''
IMPLEMENTATIONS={}
IMPLEMENTATIONS['dataset_quality_gate']=COMMON+'''
case = load('fixtures/dataset_cases.json')[sys.argv[1]]
contract = load('fixtures/dataset_contract.json')
rows = case['rows']
def number(x): return not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(x)
checks = {
 'schema': all(set(r)==set(contract['columns']) for r in rows),
 'feature_values': all(number(r.get('feature')) and 0 <= r['feature'] <= 5 for r in rows),
 'label_values': all(type(r.get('label')) is int and r['label'] in (0,1) for r in rows),
 'unique_sample_id': all(isinstance(r.get('sample_id'),str) and r['sample_id'] for r in rows) and len({r.get('sample_id') for r in rows})==len(rows)
}
failed = [k for k in contract['required_checks'] if not checks.get(k,False)]
print(json.dumps({'snapshot_id':case['snapshot_id'],'recorded_sha256':case['sha256'],'named_checks':checks,'failed_checks':failed}))
sys.exit(bool(failed))
'''
IMPLEMENTATIONS['model_behavior_tests']=COMMON+'''
import numpy as np
from prediction_package import FittedPackage, InputContractError
execution = load('fixtures/behavior_execution_cases.json')[sys.argv[1]]
package = FittedPackage(execution['regression'])
contract = load('fixtures/behavior_contract.json')
results = {}
for name, case in load('fixtures/behavior_cases.json').items():
 if 'expected_exception' in case:
  try: package.predict(case['inputs'])
  except InputContractError as e: results[name]={'required_rejection':True,'exception':type(e).__name__}
  else: results[name]={'required_rejection':False}
  continue
 actual = package.predict(case['inputs'])
 expected = np.array(case['expected_values']).reshape(case['expected_shape'])
 shape_ok = list(actual['values'].shape)==case['expected_shape']
 checks={'row_count':len(actual['values'])==len(case['expected_sample_ids']),
 'correspondence':actual['sample_ids']==case['expected_sample_ids'], 'shape':shape_ok}
 structural_ok = all(checks.values())
 comparison = {'rtol':contract['rtol'],'atol':contract['atol'], 'executed_after_structure_pass':structural_ok}
 if structural_ok:
  try: np.testing.assert_allclose(actual['values'],expected,rtol=contract['rtol'],atol=contract['atol'])
  except AssertionError: comparison['allclose']=False
  else: comparison['allclose']=True
  comparison['absolute_error']=np.abs(actual['values']-expected).tolist()
  comparison['allowed_error']=(contract['atol']+contract['rtol']*np.abs(expected)).tolist()
 else: comparison['not_executed_reason']='structural check failed; values cannot substitute for correspondence'
 results[name]={'actual_row_count':len(actual['values']), 'expected_row_count':len(case['expected_sample_ids']),
 'actual_sample_ids':actual['sample_ids'],'expected_sample_ids':case['expected_sample_ids'],
 'actual_shape':list(actual['values'].shape),'expected_shape':case['expected_shape'],'checks':checks,'tolerance_comparison':comparison}
passed=all(r.get('required_rejection', all(r.get('checks',{}).values()) and r.get('tolerance_comparison',{}).get('allclose',False)) for r in results.values())
print(json.dumps({'execution':execution,'fixture_results':results,'passed':passed}))
sys.exit(not passed)
'''
IMPLEMENTATIONS['model_release_quality_gate']=COMMON+'''
cases=load('fixtures/release_cases.json'); c=cases[sys.argv[1]]; contract=load('fixtures/release_contract.json')
def cost(c):
 fpr=c['FP']/(c['FP']+c['TN']); fnr=c['FN']/(c['FN']+c['TP'])
 return fpr*contract['costs']['cost_FP']*contract['probabilities']['P(Y=0)']+fnr*contract['costs']['cost_FN']*contract['probabilities']['P(Y=1)']
value=cost(c); reference=cost(cases[contract['accepted_reference']])
checks={'all_evidence_present':all(k in c and c[k] is not None for k in cases[contract['accepted_reference']]),
 'nonnegative_integer_counts':all(type(c[k]) is int and c[k]>=0 for k in ('FP','TN','FN','TP')),
 'negative_denominator_nonempty':c['FP']+c['TN']>0,'positive_denominator_nonempty':c['FN']+c['TP']>0,
 'candidate_identity_matches_event':c['candidate_id']==sys.argv[2],
 'cost_within_fixed_maximum':value<=contract['max_expected_error_cost'], 'cost_not_worse_than_reference':value<=reference,
 'latency_within_fixed_maximum':c['latency_ms']<=contract['max_latency_ms'],
 'operating_ok':c['operating_ok'] is True,'evidence_complete':c['evidence_complete'] is True}
print(json.dumps({'candidate':c,'expected_error_cost':value,'reference_cost':reference,
 'fixed_cost_limit':contract['max_expected_error_cost'],'fixed_latency_limit_ms':contract['max_latency_ms'],
 'probabilities':contract['probabilities'],'costs':contract['costs'],'predicates':checks,'failed_predicates':[k for k,v in checks.items() if not v]}))
sys.exit(not all(checks.values()))
'''
IMPLEMENTATIONS['pipeline_artifact_dependencies']=COMMON+'''
case=load('fixtures/dependency_cases.json')[sys.argv[1]]
stage=sys.argv[2]
if stage=='data_validation':
 result={'stage':stage, 'resolved_consumed':case[stage]['consumed'],'validation_ok':case[stage]['validation_ok']}
 passed=result['validation_ok']
else:
 result={'stage':stage,'training_produced':case['training']['produced'],'resolved_consumed':sys.argv[3],
 'dictionary_consumed':case[stage]['consumed'],'identity_matches':case['training']['produced']==sys.argv[3],
 'args_match_dictionary':sys.argv[3]==case[stage]['consumed'],'validation_ok':case[stage]['validation_ok']}
 passed=result['identity_matches'] and result['args_match_dictionary'] and result['validation_ok']
print(json.dumps(result)); sys.exit(not passed)
'''
IMPLEMENTATIONS['staged_ml_promotion']=COMMON+'''
c=load('fixtures/promotion_cases.json')[sys.argv[1]]; stage=sys.argv[2]; r=load('fixtures/registry.json')[c['registry_version']]
identity=(c['artifact_id']==r['artifact_id']==c['staged_artifact_id']==c['approval']['artifact_id'] and c['run_id']==r['run_id'] and c['registry_version']==c['approval']['registry_version'])
checks={'compatibility':c['compatibility_ok'], 'offline_validation':c['offline_validation_ok'],
 'staged_validation':c['staged_validation_ok'] and identity,
 'authorization':c['approval']['authorized'] and identity and bool(c['approval']['accountable_identity'])}
passed={'compatibility':checks['compatibility'], 'staging_quality':checks['offline_validation'] and checks['staged_validation'], 'authorization':checks['authorization']}[stage]
print(json.dumps({'stage':stage,'passed':passed,'immutable_artifact_reference':r,
 'promotion_record':{**{k:c[k] for k in ('approval','registry_version','run_id','artifact_id')},'accountable_identity':c['approval']['accountable_identity'],'per_stage_results':checks}}))
sys.exit(not passed)
'''
IMPLEMENTATIONS['pipeline_failure_recovery']=COMMON+'''
from storage_sim import StorageClient, RecoverableFailure, PreconditionFailed
case_id=sys.argv[1]; stage=sys.argv[2]; case=load('fixtures/recovery_cases.json')[case_id]
contract=load('fixtures/recovery_contract.json'); state_path=Path('state.'+case_id+'.json')
if not state_path.exists():
 state={'objects':{k:{'generation':contract['outputs'][k]['generation'],'data':Path('outputs/'+k+'.txt').read_text()} for k in case['initial_outputs']},'uploads':[], 'invocations':0}
else: state=load(state_path)
client=StorageClient({k:{'generation':v['generation'],'data':v['data'].encode()} for k,v in state['objects'].items()})
def inspect():
 result={}
 for k, expected in contract['outputs'].items():
  b=client.blob(k); exists=b.exists()
  if exists:
   b.reload(); digest=hashlib.sha256(b.download_as_bytes(if_generation_match=b.generation)).hexdigest()
   result[k]={'exists':True,'generation':b.generation,'sha256':digest,'validation_ok':digest==expected['sha256'] and expected['validation_ok']}
  else: result[k]={'exists':False,'generation':None,'sha256':None,'validation_ok':False}
 return result
before=inspect()
if stage=='recovery':
 for k, expected in contract['outputs'].items():
  b=client.blob(k)
  if b.exists():
   if not inspect()[k]['validation_ok']: raise ValueError('invalid completed artifact '+k)
  else:
   try: b.upload_from_filename('outputs/'+k+'.txt',if_generation_match=0)
   except PreconditionFailed:
    if not inspect()[k]['validation_ok']: raise ValueError('conflicting artifact '+k)
 state['invocations']+=1; state['uploads']+=client.uploads
 state['objects']={k:{'generation':v['generation'],'data':v['data'].decode()} for k,v in client.objects.items()}
 state_path.write_text(json.dumps(state))
passed=all(v['validation_ok'] for v in inspect().values()) and (stage=='recovery' or case['gate_ok'])
print(json.dumps({'stage':stage,'before':before,'after':inspect(),'upload_count':len(state['uploads']),'uploads':state['uploads'],'invocations':state['invocations'],'required_validation_ok':all(v['validation_ok'] for v in inspect().values()) and case['gate_ok']}))
sys.exit(not passed)
'''

def module(root):
 spec=importlib.util.spec_from_file_location('runtime_sim',root/'runtime_sim.py'); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def execute(name):
 root=ROOT/('ws.'+name); os.chdir(root)
 original=yaml.safe_load(Path('cloudbuild.yaml').read_text()); config=copy.deepcopy(original)
 Path('demonstration_entry.py').write_text(IMPLEMENTATIONS[name])
 # Explicit local demonstration wiring, not a claim that the supplied starter is complete.
 for i,s in enumerate(config['steps']):
  s['waitFor']=['-'] if i==0 else [config['steps'][i-1]['id']]
  if 'learner.py' in s['args']: s['args'][1]='demonstration_entry.py'
  if name in ('pipeline_artifact_dependencies','staged_ml_promotion','pipeline_failure_recovery') and s['args'][1]=='demonstration_entry.py':
   if name=='pipeline_artifact_dependencies': s['args']=['python','demonstration_entry.py','${_CASE}',s['id']]+(['${_CONSUMED}'] if s['id']=='model_validation' else [])
   else: s['args'].append(s['id'])
 triggers=load('triggers.json'); kind='repository_commit' if name in ('dataset_quality_gate','model_behavior_tests') else 'pubsub'
 results=[]
 for event in triggers[kind]['fixtures'][:2]:
  if name=='pipeline_artifact_dependencies':
   case=load('fixtures/dependency_cases.json')[event['case_id']]
   config['substitutions']['_CONSUMED']=case['model_validation']['consumed']
   config['substitutions']['_PRODUCED']=case['training']['produced']
   config['steps'][1]['args'][-1]='${_PRODUCED}'
  Path('demonstration.yaml').write_text(yaml.safe_dump(config)); parsed=yaml.safe_load(Path('demonstration.yaml').read_text())
  for marker in ('training_invocation.json','downstream_invocation.json'): Path(marker).unlink(missing_ok=True)
  if name=='pipeline_failure_recovery': Path('state.'+event['case_id']+'.json').unlink(missing_ok=True)
  before_failure=None
  if name=='pipeline_failure_recovery':
   Path('inject_failure.py').write_text(COMMON+"\nfrom storage_sim import StorageClient, RecoverableFailure\nclient=StorageClient()\ntry:\n client.blob('A').upload_from_filename('outputs/A.txt',if_generation_match=0)\n raise RecoverableFailure('injected after A upload, before B')\nexcept RecoverableFailure as e:\n state={'objects':{k:{'generation':v['generation'],'data':v['data'].decode()} for k,v in client.objects.items()},'uploads':client.uploads,'invocations':0}\n Path('state.'+sys.argv[1]+'.json').write_text(json.dumps(state))\n print(json.dumps({'failure':str(e),'exception':type(e).__name__,'A':{'exists':True,'generation':client.objects['A']['generation'],'sha256':hashlib.sha256(client.objects['A']['data']).hexdigest()},'B':{'exists':False,'generation':None,'sha256':None}}))\n sys.exit(1)\n")
   failed_config=copy.deepcopy(config);failed_config['steps'][0]['args']=['python','inject_failure.py','${_CASE}']
   Path('injected_failure.yaml').write_text(yaml.safe_dump(failed_config))
   before_failure=module(root).run_build('injected_failure.yaml',kind,event)
   for step in before_failure['steps']:
    if step['output'].strip(): step['evidence']=json.loads(step['output'])
    del step['output']
  run=module(root).run_build('demonstration.yaml',kind,event)
  for s in run['steps']:
   if s['output'].strip(): s['evidence']=json.loads(s['output'])
   del s['output']
   if name=='pipeline_artifact_dependencies' and s['id']=='training' and s['status']=='SUCCESS':
    s['evidence']={'produced_identity':load('downstream_invocation.json')['artifact_id']}
  result={'event':event,'parsed_local_demonstration_config':parsed,'run':run}
  if name=='pipeline_failure_recovery':
   second=module(root).run_build('demonstration.yaml',kind,event)
   for s in second['steps']:
    if s['output'].strip(): s['evidence']=json.loads(s['output'])
    del s['output']
   result['before_recovery']=before_failure
   result['second_invocation']=second
  if name=='staged_ml_promotion':
   # Adapter provides no credentials. Examine every emitted record; never print secret values.
   result['secret_reference_and_scope']={'references':parsed['availableSecrets']['secretManager'], 'step_scopes':{s['id']:s.get('secretEnv',[]) for s in parsed['steps']}}
   result['non_disclosure_check']={'adapter_supplies_credentials':False,'credential_fields_in_emitted_records':any(k.lower() in ('promotion_token','credential','secret_value') for k in recursive_keys(run)), 'production_marker':load('downstream_invocation.json') if Path('downstream_invocation.json').exists() else None}
  results.append(result)
 os.chdir(ROOT)
 return {'asset_id':'ws.'+name,'parsed_supplied_cloudbuild_yaml':original,'entry_point_implementation':IMPLEMENTATIONS[name],'computed_local_results':results}

def recursive_keys(x):
 if isinstance(x,dict):
  for k,v in x.items(): yield k;yield from recursive_keys(v)
 elif isinstance(x,list):
  for v in x: yield from recursive_keys(v)

if __name__=='__main__':
 evidence={k:execute(k) for k in IMPLEMENTATIONS}
 (ROOT/'evidence.json').write_text(dump(evidence))
