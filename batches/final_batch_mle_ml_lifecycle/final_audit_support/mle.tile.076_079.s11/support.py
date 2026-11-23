import json, math, copy, re, hashlib
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

def dependency_suite(config, cases, selected, event_type):
    inspect_config(config)
    edges=read('fixtures/dependency_contract.json')['required_edges']
    steps={s['id']:s for s in config['steps']}
    for producer,consumer in edges: assert producer in steps[consumer]['waitFor']
    runs={}
    events=fixture_events('pubsub')
    for name,case in cases.items():
        event=dict(events[0]);event['case_id']=name
        runs[name]=trigger_run(config,'pubsub',event,dependency_gates(case))
    event=dict(events[0]);event['case_id']=selected;event['event_type']=event_type
    chosen=trigger_run(config,'pubsub',event,dependency_gates(cases[selected]))
    return {'config':config,'runs':runs,'selected_run':chosen,'false_assert_raises':assertion_failure()}

def promotion_suite(config, selected, event_type):
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
    def execute(name, event_type_override=None):
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
        if event_type_override is not None: event['event_type']=event_type_override
        run=trigger_run(config,'pubsub',event,{'compatibility':compatibility,'staging_quality':staging,'authorization':authorization,'production':production})
        return run,record
    for name in cases: runs[name],records[name]=execute(name)
    chosen,record=execute(selected,event_type)
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

def recovery_suite(config, recover, selected, event_type):
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
    ctx=recovery_context(selected)
    def selected_retry(args): return recover(ctx)
    def selected_gate(args):
        fatal({'required_validation':ctx['case']['gate_ok']})
        return {'validated_outputs':list(ctx['client'].objects)}
    event=dict(fixture_events('pubsub')[0]);event['case_id']=selected;event['event_type']=event_type
    selected_run=trigger_run(config,'pubsub',event,{'recovery':selected_retry,'required_validation':selected_gate})
    return {'config':config,'outcomes':outcomes,'runs':runs,'selected_run':selected_run}
