import json, pathlib, zipfile, sys, subprocess, textwrap
B=pathlib.Path(__file__).parent
load=lambda p:json.loads(p.read_text())
plan=load(B/'tile_plans.json'); screens=load(B/'screens.json'); glossary=load(B/'inputs/path_glossary_bundle.json'); registry=load(B/'scenario_asset_registry.json')
bundles={b['context']['concept_id']:b for b in glossary['bundles']}
assets={a['asset_id']:a for a in registry['assets']}
runtime=load(pathlib.Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']['python']['version']
# Package source is extracted from the installed pinned sandbox wheel, not reimplemented.
wheel=next(pathlib.Path('00_FINAL_PIPELINE_CORE/sandbox/node_modules/pyodide').glob('pyyaml-*.whl'))
with zipfile.ZipFile(wheel) as z:
 yaml_files={n:z.read(n).decode() for n in z.namelist() if n.startswith('yaml/') and n.endswith('.py')}

def files_for(c):return {f['path']:f['content'] for f in assets['ws.'+c]['files']}

def common(c):
 f=files_for(c)
 # Preserve the frozen input fixtures and supplied prediction/storage implementations.
 f={p:s for p,s in f.items() if p.startswith('fixtures/') or p.startswith('outputs/') or p in ['cloudbuild.yaml','triggers.json','prediction_package.py','prediction_reference.py','storage_sim.py']}
 return {**yaml_files,**f}

SUPPORT='''import json, math, copy, re, hashlib
from pathlib import Path
from storage_sim import StorageClient, RecoverableFailure, PreconditionFailed

def read(path):
    return json.loads(Path(path).read_text())

def valid_count(value): return type(value) is int and value >= 0

def fatal(checks):
    failed = [key for key, value in checks.items() if not value]
    if failed: raise AssertionError(','.join(failed))

def named_dataset_checks(snapshot):
    rows = snapshot['rows']
    required = read('fixtures/dataset_contract.json')['columns']
    schema = all(set(row) == set(required) for row in rows)
    values = all(isinstance(row.get('feature'), (int,float)) and not isinstance(row.get('feature'), bool) and math.isfinite(row['feature']) and 0 <= row['feature'] <= 5 for row in rows)
    labels = all(type(row.get('label')) is int and row['label'] in [0,1] for row in rows)
    ids = [row.get('sample_id') for row in rows]
    unique = all(isinstance(x,str) and x for x in ids) and len(ids) == len(set(ids))
    return {'schema':schema,'feature_values':values,'label_values':labels,'unique_sample_id':unique}

def inspect_config(config):
    base = read('cloudbuild.yaml')
    assert len(config['steps']) == len(base['steps'])
    for step, original in zip(config['steps'],base['steps']):
        assert step['id'] == original['id'] and step['name'] == original['name']
        assert step['args'][:2] == original['args'][:2]
        assert not step.get('allowFailure',False)
        assert not any(code != 0 for code in step.get('allowExitCodes',[]))
    assert config['serviceAccount'] == base['serviceAccount']
    return config

def trigger_run(config, kind, event, gates):
    trigger = read('triggers.json')[kind]
    if kind == 'repository_commit':
        matches = re.fullmatch(trigger['branch_filter'],event.get('branch','')) is not None
    else:
        matches = all(event.get(k) == v for k,v in trigger['filters'].items())
    if not matches: return {'triggered':False,'steps':[]}
    substitutions = dict(config['substitutions'])
    for key, payload in trigger['bindings'].items(): substitutions[key] = event[payload]
    statuses, results = {}, []
    for step in config['steps']:
        sid = step['id']; waits = step.get('waitFor',[])
        args = list(step['args'])
        for i, arg in enumerate(args):
            for key,value in substitutions.items(): arg = arg.replace('${'+key+'}',str(value))
            args[i] = arg
        blocked = any(statuses.get(dep) != 'SUCCESS' for dep in waits if dep != '-')
        if blocked:
            result={'id':sid,'status':'SKIPPED','resolved_args':args,'exit_code':None}
        else:
            try:
                value = gates[sid](args) if sid in gates else {'artifact_id':args[-1]}
                result={'id':sid,'status':'SUCCESS','resolved_args':args,'exit_code':0,'evidence':value}
            except (AssertionError, ValueError, SystemExit, RecoverableFailure) as exc:
                result={'id':sid,'status':'FAILURE','resolved_args':args,'exit_code':int(exc.code or 1) if isinstance(exc,SystemExit) else 1,'failure':str(exc)}
        statuses[sid]=result['status']; results.append(result)
    return {'triggered':True,'steps':results}

def fixture_events(kind):
    return read('triggers.json')[kind]['fixtures']

def status(run, sid):
    return next(s['status'] for s in run['steps'] if s['id']==sid)

def assertion_failure():
    try:
        assert False
    except AssertionError:
        return True
    return False

def rejection(call, *args):
    try:
        value=call(*args)
        return {'accepted':True,'result':value}
    except (AssertionError,ValueError,RecoverableFailure) as exc:
        return {'accepted':False,'failure':str(exc)}

# Gate functions supplied for configuration-only practices. They compute results from input records.
def dependency_gates(case):
    def data(args):
        fatal({'data_validation':case['data_validation']['validation_ok']})
        return case['data_validation']
    def training(args):
        fatal({'data_to_training':case['training']['consumed']==case['data_validation']['produced']})
        return case['training']
    def model(args):
        fatal({'training_to_model':case['model_validation']['consumed']==case['training']['produced'],
               'resolved_consumer':args[-1]==case['training']['produced'],
               'model_validation':case['model_validation']['validation_ok']})
        return case['model_validation']
    return {'data_validation':data,'training':training,'model_validation':model}

def dependency_suite(config, cases, selected):
    inspect_config(config)
    edges=read('fixtures/dependency_contract.json')['required_edges']
    steps={s['id']:s for s in config['steps']}
    for producer,consumer in edges: assert producer in steps[consumer]['waitFor']
    runs={}
    events=fixture_events('pubsub')
    for name,case in cases.items():
        event=dict(events[0]);event['case_id']=name
        runs[name]=trigger_run(config,'pubsub',event,dependency_gates(case))
    event=dict(events[0]);event['case_id']=selected
    chosen=trigger_run(config,'pubsub',event,dependency_gates(cases[selected]))
    return {'config':config,'runs':runs,'selected_run':chosen,'false_assert_raises':assertion_failure()}

def promotion_suite(config, selected):
    inspect_config(config)
    expected=read('cloudbuild.yaml')
    assert config['availableSecrets']==expected['availableSecrets']
    for s in config['steps']:
        assert s.get('secretEnv',[]) == (expected['steps'][-1]['secretEnv'] if s['id']=='production' else [])
    steps={s['id']:s for s in config['steps']}
    assert 'compatibility' in steps['staging_quality']['waitFor']
    assert 'staging_quality' in steps['authorization']['waitFor']
    assert 'staging_quality' in steps['production']['waitFor'] and 'authorization' in steps['production']['waitFor']
    cases=read('fixtures/promotion_cases.json'); reg=read('fixtures/registry.json'); runs={}; records={}
    def execute(name):
        case=cases[name];record={};version=reg[case['registry_version']]
        def compatibility(args):
            fatal({'compatibility':case['compatibility_ok'],'offline_validation':case['offline_validation_ok']})
            return {'artifact_id':case['artifact_id'],'compatibility':True,'offline_validation':True}
        def staging(args):
            fatal({'staged_validation':case['staged_validation_ok'],'staged_identity':case['staged_artifact_id']==case['artifact_id']==version['artifact_id']})
            return {'artifact_id':case['staged_artifact_id'],'staged_validation':True}
        def authorization(args):
            approval=case['approval']
            fatal({'authorization':approval['authorized'],'accountable_identity':approval['accountable_identity']=='fixture-promoter',
                   'approved_version':approval['registry_version']==case['registry_version'],
                   'approved_artifact':approval['artifact_id']==case['artifact_id']==version['artifact_id'],
                   'recorded_run':case['run_id']==version['run_id']})
            return approval
        def production(args):
            fatal({'resolved_production_artifact':args[-1]==case['artifact_id']})
            record.update({'approval':case['approval'],'accountable_identity':case['approval']['accountable_identity'],
                           'registry_version':case['registry_version'],'run_id':case['run_id'],'artifact_id':case['artifact_id'],
                           'per_stage_results':{'compatibility':True,'offline_validation':True,'staged_validation':True,'authorization':True}})
            return record
        event=dict(fixture_events('pubsub')[0]);event['case_id']=name;event['artifact_id']=case['artifact_id']
        run=trigger_run(config,'pubsub',event,{'compatibility':compatibility,'staging_quality':staging,'authorization':authorization,'production':production})
        return run,record
    for name in cases: runs[name],records[name]=execute(name)
    chosen,record=execute(selected)
    return {'config':config,'runs':runs,'records':records,'selected_run':chosen,'selected_record':record,'credential_values_recorded':False}

# Recovery helper interfaces: identity/validation observations, bounded action and execution trace.
def recovery_context(name):
    case=read('fixtures/recovery_cases.json')[name];contract=read('fixtures/recovery_contract.json');objects={};race={}
    for output in case['initial_outputs']:
        data=Path('outputs/'+output+'.txt').read_bytes()
        if output in case.get('conflicting_outputs',[]): data=b'conflicting fixture content'
        objects[output]={'generation':contract['outputs'][output]['generation'],'data':data}
    for output in case['race_outputs']:
        race[output]={'generation':contract['outputs'][output]['generation'],'data':Path('outputs/'+output+'.txt').read_bytes()}
    return {'case':case,'contract':contract,'client':StorageClient(objects,race),'failures':[],'actions':[],'validations':[]}

def inject(context):
    exc=context['case']['exception']
    if exc=='RecoverableFailure': raise RecoverableFailure('injected after A before B')
    if exc=='ValueError': raise ValueError('unrelated failure')

def record_failure(context, error): context['failures'].append(str(error))
def apply_recovery(context): context['actions'].append('resume_verified_artifact_boundary')
def validate_output(context, output):
    context['validations'].append(output)
    return context['contract']['outputs'][output]['validation_ok'] and output not in context['case']['invalid_outputs']

def recovery_observation(context):
    return {'generations':{k:v['generation'] for k,v in context['client'].objects.items()},
            'hashes':{k:hashlib.sha256(v['data']).hexdigest() for k,v in context['client'].objects.items()},
            'uploads':list(context['client'].uploads),'requests':[list(x) for x in context['client'].requests],
            'validations':list(context['validations']),'failures':list(context['failures']),'actions':list(context['actions'])}

def recovery_suite(config, recover, selected):
    inspect_config(config)
    assert config['steps'][1]['waitFor']==['recovery']
    assert config['steps'][2]['waitFor']==['required_validation']
    cases=read('fixtures/recovery_cases.json'); outcomes={};runs={}
    for name in cases:
        context=recovery_context(name);before=recovery_observation(context)
        first=rejection(recover,context);after=recovery_observation(context)
        second=rejection(recover,context);again=recovery_observation(context)
        if first['accepted']:
            assert before['generations'].get('A')==after['generations']['A']==again['generations']['A']
            assert before['hashes'].get('A')==after['hashes']['A']==again['hashes']['A']
            assert after['generations']==again['generations'] and after['uploads']==again['uploads']
            assert len(again['validations'])>len(after['validations'])
        outcomes[name]={'before':before,'first':first,'after':after,'second':second,'again':again}
        ctx=recovery_context(name)
        def retry(args): return recover(ctx)
        def gate(args):
            fatal({'required_validation':ctx['case']['gate_ok']})
            return {'validated_outputs':list(ctx['client'].objects)}
        event=dict(fixture_events('pubsub')[0]);event['case_id']=name
        runs[name]=trigger_run(config,'pubsub',event,{'recovery':retry,'required_validation':gate})
    return {'config':config,'outcomes':outcomes,'runs':runs,'selected_run':runs[selected]}
'''

SOLUTIONS={}
STARTERS={}
PROMPTS={}

SOLUTIONS['dataset_quality_gate']='''import yaml
from support import read, named_dataset_checks, inspect_config, trigger_run, fixture_events, status, assertion_failure

def dataset_gate(snapshot, required):
    checks = named_dataset_checks(snapshot)
    failed = []
    for name in required:
        if name not in checks or not checks[name]:
            failed.append(name)
    evidence = {'snapshot_id':snapshot['snapshot_id'],'sha256':snapshot['sha256'],'checks':checks,'failed_checks':failed,'accepted':not failed}
    return evidence

def fatal_dataset(args):
    snapshot = cases[args[-1]]
    result = dataset_gate(snapshot, contract['required_checks'])
    retained[result['snapshot_id']] = result
    if not result['accepted']:
        raise AssertionError(result['failed_checks'])
    return result

cases = read('fixtures/dataset_cases.json')
contract = read('fixtures/dataset_contract.json')
retained = {}
results = {}
for name in cases:
    results[name] = dataset_gate(cases[name],contract['required_checks'])
assert results['valid']['accepted']
assert results['boundary']['accepted']
assert not results['missing_required_feature']['accepted']
assert 'schema' in results['missing_required_feature']['failed_checks']
config = read('cloudbuild.yaml')
config['steps'][1]['waitFor'] = ['quality']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
inspect_config(resolved)
runs = []
for event in fixture_events('repository_commit'):
    runs.append(trigger_run(resolved,'repository_commit',event,{'quality':fatal_dataset}))
assert status(runs[0],'training') == 'SUCCESS'
assert status(runs[1],'quality') == 'FAILURE'
assert status(runs[1],'training') == 'SKIPPED'
event = {'branch':'main','snapshot_id':selected_case}
selected_run = trigger_run(resolved,'repository_commit',event,{'quality':fatal_dataset})
report = {'config':resolved,'results':results,'retained':retained,'runs':runs,'selected_run':selected_run,'false_assert_raises':assertion_failure()}
'''
STARTERS['dataset_quality_gate']='''# Implement dataset_gate(snapshot, required) and fatal_dataset(args).
# Read fixtures and the contract, retain named results, then wire and round-trip the configuration.
# Assemble report with config, results, retained, runs, selected_run and false_assert_raises.
report = None
'''
PROMPTS['dataset_quality_gate']='''Implement dataset_gate(snapshot, required) using named_dataset_checks: collect every missing/false required check and return snapshot_id, sha256, checks, failed_checks and accepted. Implement fatal_dataset(args), retaining evidence by snapshot_id and raising AssertionError on rejection. Use all dataset fixtures; assert valid/boundary acceptance and missing-required-feature rejection with a named schema failure. Read the unchanged contract. Wire training to waitFor quality; safely write resolved.yaml and reload it, inspecting images, entry points, IDs and fatal settings. Execute the existing repository_commit fixture events with trigger_run and inspect accepted/rejected training statuses. Also run the main-branch event for selected_case. Set report to {config, results, retained, runs, selected_run, false_assert_raises}; results maps every case to its gate evidence; retained maps tested snapshot IDs to evidence; runs follows fixture-event order. The helper assertion_failure tests ordinary false-assert behavior. Supplied checks validate concrete row values, not fixture names. This is a bounded in-process fixture runtime, not an actual cloud submission; statuses and exit codes must be computed by executing your gate.'''

SOLUTIONS['model_behavior_tests']='''import numpy as np
import yaml
from prediction_package import FittedPackage, InputContractError
from support import read, inspect_config, trigger_run, fixture_events, status, assertion_failure, rejection

def test_behavior(package, fixture, contract):
    if 'expected_exception' in fixture:
        try:
            package.predict(fixture['inputs'])
        except InputContractError:
            return {'rejected_input':True}
        raise AssertionError('expected InputContractError')
    output = package.predict(fixture['inputs'])
    assert len(output['sample_ids']) == len(fixture['inputs'])
    assert output['sample_ids'] == fixture['expected_sample_ids']
    assert list(output['values'].shape) == fixture['expected_shape']
    expected = np.array(fixture['expected_values']).reshape(fixture['expected_shape'])
    np.testing.assert_allclose(output['values'],expected,rtol=contract['rtol'],atol=contract['atol'])
    return {'sample_ids':output['sample_ids'],'values':output['values'].tolist(),'shape':list(output['values'].shape)}

cases=read('fixtures/behavior_cases.json')
contract=read('fixtures/behavior_contract.json')
execution=read('fixtures/behavior_execution_cases.json')
results={}
for name in cases:
    results[name]=test_behavior(FittedPackage(),cases[name],contract)
regressions={}
for regression in contract['regressions']:
    regressions[regression]=rejection(test_behavior,FittedPackage(regression),cases['valid'],contract)
    assert not regressions[regression]['accepted']

def fatal_behavior(args):
    case=execution[args[-1]]
    return test_behavior(FittedPackage(case['regression']),cases[case['fixture_id']],contract)

config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['behavior_tests']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
inspect_config(resolved)
runs=[]
for event in fixture_events('repository_commit'):
    runs.append(trigger_run(resolved,'repository_commit',event,{'behavior_tests':fatal_behavior}))
assert status(runs[0],'release_gate')=='SUCCESS'
assert status(runs[1],'behavior_tests')=='FAILURE'
assert status(runs[1],'release_gate')=='SKIPPED'
selected_run=trigger_run(resolved,'repository_commit',{'branch':'main','snapshot_id':'valid','case_id':selected_case},{'behavior_tests':fatal_behavior})
report={'config':resolved,'results':results,'regressions':regressions,'runs':runs,'selected_run':selected_run,'false_assert_raises':assertion_failure()}
'''
STARTERS['model_behavior_tests']='''# Write imports and test_behavior(package, fixture, contract).
# Check structure first, then explicit tolerances, and the InputContractError path.
# Wire and round-trip the configuration; execute fixture events and build report.
report = None
'''
PROMPTS['model_behavior_tests']='''Write test_behavior(package, fixture, contract) against the supplied FittedPackage prediction path. For ordinary/empty fixtures assert row count, sample_id correspondence and expected_shape before np.testing.assert_allclose with contract rtol/atol. Return {sample_ids, values, shape}, using lists. For prohibited input assert the declared InputContractError; return {rejected_input: True}, failing if no exception occurs. Evaluate every fixture and all four injected regressions through rejection; none may pass. Write fatal_behavior(args) using the execution-case regression and fixture. Wire release_gate to waitFor behavior_tests; safe_dump and safe_load resolved.yaml and inspect required fields/fatal settings. Execute the unchanged repository_commit events, asserting accepted success and regressed fatal failure with release_gate skipped. Also execute the main-branch event for selected_case. Set report to {config, results, regressions, runs, selected_run, false_assert_raises}; results/regressions map fixture/regression names to results; runs follows fixture-event order. Use assertion_failure for the false-assert observation. The supplied in-process fixture runtime computes gate-process exit codes and stage statuses; no real Cloud Build execution is claimed.'''

SOLUTIONS['model_release_quality_gate']='''import yaml
from support import read, inspect_config, trigger_run, fixture_events, status, rejection, valid_count

def expected_cost(evidence, contract):
    for name in ['FP','TN','FN','TP']:
        if name not in evidence or not valid_count(evidence[name]):
            raise ValueError('invalid_count:'+name)
    negative=evidence['FP']+evidence['TN']
    positive=evidence['FN']+evidence['TP']
    if negative <= 0 or positive <= 0:
        raise ValueError('undefined_actual_class_rate')
    return contract['probabilities']['P(Y=0)'] * evidence['FP']/negative * contract['costs']['cost_FP'] + contract['probabilities']['P(Y=1)'] * evidence['FN']/positive * contract['costs']['cost_FN']

def acceptance(candidate, reference, contract, event_id):
    for name in ['candidate_id','evidence_complete','latency_ms','operating_ok','FP','TN','FN','TP']:
        if name not in candidate: raise ValueError('missing:'+name)
    checks={'complete':candidate['evidence_complete'],'identity':candidate['candidate_id']==event_id,
            'latency_present':candidate['latency_ms'] is not None,'operating':candidate['operating_ok']}
    for name in checks:
        if not checks[name]: raise ValueError(name)
    cost=expected_cost(candidate,contract)
    checks['cost_maximum']=cost <= contract['max_expected_error_cost']
    checks['reference_cost']=cost <= expected_cost(reference,contract)
    checks['latency']=candidate['latency_ms'] <= contract['max_latency_ms']
    for name in checks:
        if not checks[name]: raise ValueError(name)
    return {'candidate_id':candidate['candidate_id'],'expected_error_cost':cost,'checks':checks}

cases=read('fixtures/release_cases.json')
contract=read('fixtures/release_contract.json')
results={}
for name in cases:
    results[name]=rejection(acceptance,cases[name],cases[contract['accepted_reference']],contract,cases[name]['candidate_id'])
assert results['A']['accepted']
assert results['boundary']['accepted']
assert not results['B']['accepted']
assert not results['empty_negatives']['accepted']
assert not results['empty_positives']['accepted']
assert not results['incomplete']['accepted']

def fatal_acceptance(args):
    return acceptance(cases[args[-1]],cases[contract['accepted_reference']],contract,args[-1])

config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['release_gate']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
inspect_config(resolved)
runs=[]
for event in fixture_events('pubsub'):
    runs.append(trigger_run(resolved,'pubsub',event,{'release_gate':fatal_acceptance}))
assert status(runs[0],'promotion')=='SUCCESS'
assert status(runs[1],'release_gate')=='FAILURE'
assert status(runs[1],'promotion')=='SKIPPED'
event={'event_type':'artifact_ready','case_id':selected_case,'artifact_id':selected_case}
selected_run=trigger_run(resolved,'pubsub',event,{'release_gate':fatal_acceptance})
report={'config':resolved,'results':results,'runs':runs,'selected_run':selected_run}
'''
STARTERS['model_release_quality_gate']='''# Write imports, expected_cost(evidence, contract), acceptance(candidate, reference, contract, event_id).
# Reject named failed/incomplete predicates, assert declared cases, and wire the fatal acceptance stage.
# Safely round-trip the configuration and build report from actual local fixture executions.
report = None
'''
PROMPTS['model_release_quality_gate']='''Implement expected_cost(evidence, contract): validate nonnegative integer confusion counts, reject empty actual-class denominators, and compute validation error cost from the fixed probabilities/costs. Implement acceptance(candidate, reference, contract, event_id): require complete evidence, matching candidate identity, operating_ok, defined latency within its limit, cost within the fixed maximum and accepted-reference cost; raise an exception naming any failed/incomplete predicate. Return {candidate_id, expected_error_cost, checks}. Do not use protected-test observations to tune anything. Map every release fixture through rejection into results and assert A/boundary pass while B, incomplete and empty-group cases fail. Implement fatal_acceptance(args) using the resolved artifact ID. Wire promotion to waitFor release_gate; safely write/reload resolved.yaml and inspect images, commands, IDs, dependencies and fatal settings. Execute the existing Pub/Sub events and inspect intended resolved candidates, accepted promotion and rejected nonexecution. Also run selected_case as the artifact_id of an artifact_ready event. Set report to {config, results, runs, selected_run}; runs follows fixture-event order. Execution is a bounded local fixture adapter, not a cloud claim.'''

SOLUTIONS['pipeline_artifact_dependencies']='''import yaml
from support import read, dependency_suite
cases=read('fixtures/dependency_cases.json')
config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['data_validation']
config['steps'][2]['waitFor']=['training']
config['steps'][2]['args'][3]=cases['valid']['training']['produced']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
assert cases['valid']['training']['produced']==cases['valid']['model_validation']['consumed']
assert cases['boundary']['training']['produced']==cases['boundary']['model_validation']['consumed']
assert cases['mismatch']['training']['produced']!=cases['mismatch']['model_validation']['consumed']
report=dependency_suite(resolved,cases,selected_case)
'''
STARTERS['pipeline_artifact_dependencies']='''import yaml
from support import read, dependency_suite
cases=read('fixtures/dependency_cases.json')
config=read('cloudbuild.yaml')
# Repair explicit waitFor edges and the model-validation artifact argument.
# Assert valid/boundary identity agreement and mismatch disagreement.
# Safely dump/load resolved.yaml, then report=dependency_suite(resolved,cases,selected_case).
report=None
'''
PROMPTS['pipeline_artifact_dependencies']='''Repair the supplied configuration, not the negative fixtures: training must waitFor data_validation, and model_validation must waitFor training. Replace model_validation's final argument B with the immutable training-produced identity from cases['valid']['training']['produced']. Keep execution images, entry points, IDs and failure settings intact. Assert producer/consumer agreement for valid and boundary, and disagreement for mismatch. safe_dump to resolved.yaml, safe_load into resolved, then set report = dependency_suite(resolved, cases, selected_case). This supplied gate runner executes contract checks on consumed/produced identities and required validation, records resolved command inputs and stage statuses for every fixture, and returns {config, runs, selected_run, false_assert_raises}. Its accepted runs must preserve actual edges; mismatch and failed_validation must fail without their dependent stages executing. Do not rename artifacts to conceal a mismatch. This is the existing bounded local runtime: no real cloud execution or policy change is claimed.'''

SOLUTIONS['staged_ml_promotion']='''import yaml
from support import read, promotion_suite
config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['compatibility']
config['steps'][2]['waitFor']=['staging_quality']
config['steps'][3]['waitFor']=['staging_quality','authorization']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
report=promotion_suite(resolved,selected_case)
assert report['runs']['accepted']['steps'][3]['status']=='SUCCESS'
assert report['runs']['unauthorized']['steps'][3]['status']=='SKIPPED'
assert report['records']['accepted']['artifact_id']==report['records']['accepted']['approval']['artifact_id']
'''
STARTERS['staged_ml_promotion']='''import yaml
from support import read, promotion_suite
config=read('cloudbuild.yaml')
# Wire explicit dependencies; preserve approved artifacts and reference-only secret bindings.
# Safely dump/load resolved.yaml; call promotion_suite and assert accountable accepted/rejected outcomes.
report=None
'''
PROMPTS['staged_ml_promotion']='''Wire the existing supplied gate entry points: staging_quality waits for compatibility; authorization waits for staging_quality; production waits for BOTH staging_quality and authorization. Preserve the immutable event-bound artifact, registry/run link, images, commands and IDs; do not permit required failures. Preserve availableSecrets.secretManager version references and expose PROMOTION_TOKEN only to production through secretEnv; never put credential values in YAML or records. Safely write/reload resolved.yaml. Set report = promotion_suite(resolved, selected_case), then assert accepted production SUCCESS, unauthorized production SKIPPED, and the accepted record's artifact_id equals its approval artifact_id. The supplied suite computes compatibility/offline/staged/authorization predicates from all promotion fixtures and returns {config, runs, records, selected_run, selected_record, credential_values_recorded}. Verify wrong_artifact and failed_staging cannot reach production either. Records retain approval, accountable_identity, registry_version, run_id, artifact_id and per_stage_results. This local fixture runtime has no real credential values and makes no real-cloud submission or expanded-authorization claim.'''

SOLUTIONS['pipeline_failure_recovery']='''import yaml
import hashlib
from storage_sim import RecoverableFailure, PreconditionFailed
from support import read, inject, record_failure, apply_recovery, validate_output, recovery_suite

def verify(context, output, blob):
    blob.reload()
    data=blob.download_as_bytes(if_generation_match=blob.generation)
    expected=context['contract']['outputs'][output]
    assert hashlib.sha256(data).hexdigest()==expected['sha256']
    assert validate_output(context,output)
    return {'generation':blob.generation,'sha256':hashlib.sha256(data).hexdigest(),'validation_ok':True}

def recover(context):
    try:
        inject(context)
    except RecoverableFailure as error:
        record_failure(context,error)
        apply_recovery(context)
    verified={}
    for output in context['contract']['outputs']:
        blob=context['client'].blob(output)
        if not blob.exists():
            try:
                blob.upload_from_filename('outputs/'+output+'.txt',if_generation_match=0)
            except PreconditionFailed:
                blob.reload()
        verified[output]=verify(context,output,blob)
    return verified

config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['recovery']
config['steps'][2]['waitFor']=['required_validation']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
report=recovery_suite(resolved,recover,selected_case)
assert report['runs']['accepted']['steps'][2]['status']=='SUCCESS'
assert report['runs']['rejected_gate']['steps'][1]['status']=='FAILURE'
assert report['runs']['rejected_gate']['steps'][2]['status']=='SKIPPED'
assert not report['outcomes']['invalid_existing']['first']['accepted']
assert not report['outcomes']['conflicting_content']['first']['accepted']
assert not report['outcomes']['unrelated_failure']['first']['accepted']
'''
STARTERS['pipeline_failure_recovery']='''# Write imports, verify(context, output, blob) and recover(context).
# Use exact-generation bytes, content identity and validation; create-only uploads and 412 reconciliation.
# Catch only RecoverableFailure and keep unrelated errors fatal. Wire gates and round-trip YAML.
# Call recovery_suite(resolved,recover,selected_case) into report; assert declared outcomes.
report=None
'''
PROMPTS['pipeline_failure_recovery']='''Write verify(context, output, blob): reload, download at blob.generation, compare sha256 with the declared output and require validate_output; return {generation, sha256, validation_ok}. Write recover(context): call inject, catch ONLY RecoverableFailure, record_failure and apply_recovery. Reconcile each declared output; verify existing bytes and validation before reuse; create only missing outputs with upload_from_filename('outputs/'+output+'.txt', if_generation_match=0). On PreconditionFailed re-read and verify the concurrently created object; never overwrite. Return verified evidence by output. Wire required_validation waitFor recovery and promotion waitFor required_validation; safely dump/load resolved.yaml. Set report = recovery_suite(resolved, recover, selected_case). Assert accepted promotion success; rejected required_validation failure with promotion skipped; invalid_existing, conflicting_content and unrelated_failure rejection. The suite executes every fixture twice, asserting unchanged A generation/hash, only missing B created, safe 412 handling, no second-call uploads/generations and repeated validation. It returns {config, outcomes, runs, selected_run}, with actual computed observations and resolved inputs. This is a bounded local storage/trigger simulator, not a real-cloud execution.'''

# Choices test only the planned facts. Options are predicates/interpretations of supplied evidence.
CHOICES={
'mle.tile.073_075.s04':('After safe_dump and safe_load, quality has its original image and command; training has waitFor: [quality]; quality has allowFailure: true. Which inspection result follows?',[
 ('a','Reject: required quality failure is permitted, despite the explicit dependency.','Required failures must stay fatal; waitFor does not excuse allowFailure.'),
 ('b','Accept: waitFor makes allowFailure harmless.','An explicit dependency cannot restore a required failure that the configuration permits.'),
 ('c','Accept: safe_load automatically removes failure allowances.','Safe loading parses standard YAML; it does not enforce the gate policy.')],'a'),
'mle.tile.073_075.s09':('A model-test configuration was written with safe_dump and reloaded with safe_load. Before using it in the existing runtime, what is still required?',[
 ('a','Inspect the reloaded required fields, rather than assuming serialization verified them.','Safe round-tripping still requires inspection of resolved configuration fields.'),
 ('b','Nothing: safe_load proves every test-stage field is correct.','Safe loading restricts tag construction; it is not semantic verification of the configuration.'),
 ('c','Replace safe_load with a loader that constructs arbitrary Python objects.','Safe loading accepts standard YAML tags, not arbitrary Python object constructors.')],'a'),
'mle.tile.073_075.s15':('A team uses protected-test observations to tune a candidate setting before its release gate. Which judgement follows?',[
 ('a','Reject that use: protected-test observations must not drive fitting, selection or tuning.','Using protected-test information to choose the system violates isolation.'),
 ('b','Permit it if the gate is still called afterward.','Calling a later gate does not undo protected-test information used in tuning.'),
 ('c','Permit it when only a setting, not model weights, changes.','Isolation applies to tuning settings as well as fitting and selection.')],'a'),
'mle.tile.073_075.s16':('A release configuration mapping must be written and then reloaded safely for inspection. Which sequence matches the taught procedure?',[
 ('a','Use yaml.safe_dump(config, file_handle), then yaml.safe_load(file_handle), then inspect required resolved fields.','Both safe operations and the subsequent field inspection are required.'),
 ('b','Write safely, but inspect only the original in-memory mapping.','Inspection must cover the configuration that was actually reloaded.'),
 ('c','Reload with arbitrary Python object construction enabled.','The safe procedure accepts standard YAML tags, not arbitrary Python object constructors.')],'a'),
'mle.tile.076_079.s04':('Training produces immutable artifact A. The model-validation step waits for training, but its actual resolved input names B. What does the evidence establish?',[
 ('a','The completion dependency exists, but the artifact edge is mismatched.','Successful predecessor completion and consumer identity are separate checks.'),
 ('b','The artifact edge is valid because waitFor names training.','waitFor establishes completion order, not the identity of the artifact consumed.'),
 ('c','Ignore the resolved input and infer A from the intended stage order.','The actual resolved consumer input must agree with the upstream immutable identity.')],'a'),
'mle.tile.076_079.s10':('Promotion uses an approved Secret Manager version reference. Which configuration-and-output inspection satisfies the taught non-disclosure rule?',[
 ('a','Bind the version reference in availableSecrets.secretManager; use secretEnv only on the needed step; inspect output without exposing values.','Configuration carries references, and injection is scoped to the needed step.'),
 ('b','Put the credential value directly into the YAML for reproducibility.','Credential values must not be serialized into configuration.'),
 ('c','Bind references correctly but echo the injected value in the captured output.','Reference-only configuration does not permit disclosure in output.')],'a'),
'mle.tile.076_079.s16':('After a recovery event passes the configured Pub/Sub filter, what evidence is needed to verify that the retry and required later gates executed?',[
 ('a','Actual stage results and resolved inputs for accepted and rejected fixture runs.','Inspect execution results and inputs; distinguish retried execution from merely intended wiring.'),
 ('b','A parsed configuration alone, without execution observations.','A configuration does not establish that the retry or required later checks actually executed.'),
 ('c','A success message from the catch block, without inspecting stages.','Handling the declared exception is not proof that the retry and required gates ran.')],'a'),
'mle.tile.076_079.s21':('To trace a served model back to training evidence, which sequence follows the taught lineage chain?',[
 ('a','Resolve the deployed registry version, retrieve its linked run, and compare artifact, dataset and configuration evidence with deployment and approval.','The registry/run links connect the served artifact to its recorded training evidence.'),
 ('b','Find a similarly named run and assume its configuration was used.','Similar names do not establish the recorded deployment-to-run link.'),
 ('c','Inspect only the deployment label and stop before retrieving the run.','The training execution and its dataset/configuration evidence are part of the lineage chain.')],'a')}

# Build measures from assessment anchors, intersecting planned/taught facts.
def base_ix(t,s,index,total):
 measures=[]
 for anchor in s['anchors']:
  if '#assessment:' in anchor:
   cid,cap=anchor.split('#assessment:')
   a=next(a for a in bundles[cid]['assessment_anchors'] if a['capability']==cap)
   measures.append({'concept_id':cid,'capability':cap,'fact_ids':[f for f in a['fact_ids'] if cid+'#'+f in s['fact_ids']]})
 cid=s['concept_ids'][0]
 remediation=next((r['step_id'] for r in t.get('remediation_steps',[]) if cid in r['concept_ids']),None)
 feedback={'correct':{'message':'Correct: the supplied evidence meets the required identity, configuration or gate criterion.'},'incorrect':{'message':'Recheck the required predicates and the actual evidence; a passing label cannot replace a missing or failed requirement.'},'hints':['Separate the intended configuration from the evidence that was inspected or executed.','Check every required predicate, not just the most favorable one.']}
 if cid not in seen and remediation:feedback['remediation_step_id']=remediation
 seen.add(cid)
 return {'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if index==0 else 'stretch' if index>=total-2 else 'core','grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors'],'feedback':feedback}

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
seen=set();jobs=[]
for tile in plan['tiles']:
 st=next(t for t in screens['tiles'] if t['tile_id']==tile['tile_id'])
 steps=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
 authored=[]
 for index,s in enumerate(steps):
  ix=base_ix(st,s,index,len(steps));cid=s['concept_ids'][0];c=cid.split('.')[-1]
  if ix['type']=='choice':
   prompt,options,key=CHOICES[s['step_id']]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':o[0],'text':o[1]} for o in options]}
   ix['grading']={'correct_option_ids':[key],'option_feedback':{o[0]:{'message':o[2]} for o in options}}
   ix['feedback']['correct']['message']=next(o[2] for o in options if o[0]==key)
  elif ix['type']=='code_exercise':
   f=common(c);f['support.py']=SUPPORT
   # Pyodide's checker executes one entry: the supplied scaffold materializes its fixture files.
   # A selected event is an explicit mutable input for the deterministic anti-hardcoding check.
   selected={'dataset_quality_gate':'valid','model_behavior_tests':'accepted','model_release_quality_gate':'A','pipeline_artifact_dependencies':'valid','staged_ml_promotion':'accepted','pipeline_failure_recovery':'accepted'}[c]
   scaffold='selected_case = '+repr(selected)+'\nimport os\nfrom pathlib import Path\nsupport_files = '+repr(f)+'\nfor path, content in support_files.items():\n    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)\n    Path(path).write_text(content)\n\n'
   starter=scaffold+STARTERS[c]; solution=scaffold+SOLUTIONS[c]
   constraints=bundles[cid]['practice_anchor']['live_code']
   ix['standalone']=False
   ix['public']={'prompt':PROMPTS[c],'runtime':{'kind':'python','version':runtime,'packages':['numpy'] if c=='model_behavior_tests' else []},'workspace':{'entry':'learner.py','files':[{'path':'learner.py','role':'editable','language':'python','content':starter}],'asset_mounts':[]},'constraints':{k:constraints[k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'learner.py','content':solution}],'tests':[{'test_id':'test.'+s['step_id']+'.report','kind':'value_equals','spec':{'expr':'report','expected':None},'visible':True,'message_on_fail':'Compare named contract outcomes, reloaded configuration and actual fixture-run evidence.'}]}
   ix['feedback']['correct']['message']='The declared fixture outcomes, fatal dependencies and recorded evidence agree with the contract.'
   ix['feedback']['incorrect']['message']='Inspect the named failure or mismatch and the resolved stage inputs; keep rejected required checks fatal.'
   jobs.append({'id':s['step_id'],'entry':'learner.py','files':[{'path':'learner.py','content':solution}],'mounts':[],'probes':[{'id':'report','kind':'expr','expr':'report'}]})
  else:
   # Inspect-and-judge: authored excerpts are inside the interaction and have no asset references.
   source=read_source=json.loads(files_for(c)['fixtures/lineage_cases.json'])
   valid=source['valid']; registry_record=valid['registry']; run_record=next(iter(valid['runs'].values()))
   # Full identities and revision are copied from the frozen fixtures below.
   descriptions=[]
   revision=run_record.get('code_revision',valid.get('code',{}).get('revision',''))
   descriptions.append(('chain','All supplied deployment/registry/run/approval/dataset/configuration identities agree pairwise. The artifact download uses the registry recorded generation; its computed hash equals the recorded hash. Both git rev-parse --verify REVISION and git show REVISION return zero for the recorded revision. Valid, boundary and failure predicates all evaluate true.\nDecision returned: verified chain.','verified','All necessary identity, content, local-commit and assertion observations support verification.'))
   descriptions.append(('approval','All other checks pass. Approval artifact_id = '+str(source['approval_A_deployment_B']['approval']['artifact_id'])+'; deployment artifact_id = '+str(source['approval_A_deployment_B']['deployment']['artifact_id'])+'.\nDecision returned: verified chain.','reject','Approval and deployment artifact identities differ; similar names cannot repair the link.'))
   descriptions.append(('missing','All other checks pass. The registry run_id is missing (null); the audit substitutes a similarly named run without a recorded link.\nDecision returned: verified chain.','reject','A missing recorded run link must be reported, not inferred from names.'))
   descriptions.append(('generation','All other links pass. The registry records generation = recorded_generation; the download requests a DIFFERENT generation. The audit never compares downloaded bytes with the recorded content hash.\nDecision returned: verified chain.','reject','Exact recorded generation retrieval and content verification are both required.'))
   descriptions.append(('commit','All identity/content checks pass. The audit copies the recorded revision string into the report. git rev-parse --verify REVISION returns nonzero, and git show REVISION returns nonzero.\nDecision returned: verified chain.','reject','Copying a revision string is not proof that its local commit exists; both unsuccessful inspections prevent verification.'))
   descriptions.append(('boundary','Two registry entries have the same model name but different versions. The audit follows the exact deployed version, not the similarly named entry. All pairwise identities, exact-generation/hash and both local Git inspections agree; declared case predicates pass.\nDecision returned: verified chain.','verified','Exact version and identity checks, rather than name similarity, make this boundary case defensible.'))
   descriptions.append(('assertion','Identity/content/commit checks pass. In ordinary non-optimized execution a declared failure-case predicate is false. The audit executes assert predicate and then nevertheless reports that all required assertions passed.\nDecision returned: verified chain.','reject','A false predicate raises AssertionError; the asserted case cannot be reported as passing.'))
   ix['public']={'prompt':'Read each supplied audit excerpt and decide whether its verified-chain decision is supported or must be rejected. Each excerpt states the remaining checks explicitly; judge only the supplied evidence. REVISION denotes the revision recorded in that excerpt, not a guessed name.','buckets':[{'bucket_id':'verified','label':'Verified-chain decision supported'},{'bucket_id':'reject','label':'Reject the verified-chain decision'}],'items':[{'item_id':i,'text':text} for i,text,k,feedback in descriptions]}
   ix['grading']={'assignments':{i:k for i,text,k,feedback in descriptions},'item_feedback':{i:{'message':feedback} for i,text,k,feedback in descriptions}}
   ix['feedback']['correct']['message']='Verification requires agreeing identity links, exact artifact content, an existing recorded commit and passing declared assertions.'
   ix['feedback']['incorrect']['message']='A missing or mismatched link, wrong artifact retrieval, failed local commit check or false assertion prevents a verified-chain report.'
   ix['feedback']['hints']=['Ask whether the exact recorded link was checked, not merely a similarly named record.','Separate content identity, generation and local commit evidence.']
  authored.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':authored})
# The deterministic runner supplies every expected report. Nothing is typed from memory.
(B/'stage04_execution_job.json').write_text(json.dumps({'packages':['numpy','pandas'],'scripts':jobs}))
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Authored',sum(len(t['interactions']) for t in out['tiles']),'interactions; runner jobs',len(jobs))
