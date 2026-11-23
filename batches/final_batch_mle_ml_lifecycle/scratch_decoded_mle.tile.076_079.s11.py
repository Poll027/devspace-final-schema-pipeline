cases = {'accepted': {'registry_version': '1', 'artifact_id': 'A', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': True, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': True, 'staged_artifact_id': 'A'}, 'unauthorized': {'registry_version': '1', 'artifact_id': 'A', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': False, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': True, 'staged_artifact_id': 'A'}, 'wrong_artifact': {'registry_version': '1', 'artifact_id': 'B', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': True, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': True, 'staged_artifact_id': 'A'}, 'failed_staging': {'registry_version': '1', 'artifact_id': 'A', 'run_id': 'run.A', 'approval': {'approval_id': 'approval.A', 'registry_version': '1', 'artifact_id': 'A', 'authorized': True, 'accountable_identity': 'fixture-promoter'}, 'compatibility_ok': True, 'offline_validation_ok': True, 'staged_validation_ok': False, 'staged_artifact_id': 'A'}}

contract = {'scope': 'fixture-promoter may promote approved artifact A, registry version 1, only', 'required_results': ['compatibility', 'offline_validation', 'staged_validation', 'authorization'], 'record_fields': ['approval', 'accountable_identity', 'registry_version', 'run_id', 'artifact_id', 'per_stage_results'], 'secret_reference_only': 'PROMOTION_TOKEN is provided only by the authorized runtime to production. Do not serialize or echo it; inspect captured output without displaying its value. The local adapter never supplies real credentials.'}

trigger = {'id': 'fixture-artifact-trigger', 'topic': 'projects/fixture-project/topics/artifacts', 'bindings': {'_CASE': 'case_id', '_ARTIFACT': 'artifact_id'}, 'filters': {'event_type': 'artifact_ready'}, 'fixtures': [{'event_type': 'artifact_ready', 'case_id': 'accepted', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'unauthorized', 'artifact_id': 'A'}, {'event_type': 'unrelated', 'case_id': 'accepted', 'artifact_id': 'A'}]}

contract_stage_results = ['compatibility', 'offline_validation', 'staged_validation', 'authorization']

registry_records = {'1': {'model_name': 'fixture_model', 'version': '1', 'artifact_id': 'A', 'artifact_source': 'gs://fixture-artifacts/A.txt', 'generation': 1, 'sha256': '9400790a7154c4bb7f0ff81cbe3691b7543bda6ce749e6f872b29e64453618b6', 'run_id': 'run.A'}}

approved_secret_references = [{'versionName': 'projects/fixture-project/secrets/promotion-token/versions/1', 'env': 'PROMOTION_TOKEN'}]

captured_output = {'stdout': 'staging accepted; authorized promotion recorded for A', 'stderr': ''}

adapter_source = "evidence_fields = ['_ARTIFACT', '_CASE', '_SNAPSHOT', 'accepted', 'accountable_identity', 'all_evidence', 'approval', 'approval_id', 'artifact_id', 'authorization', 'authorized', 'bindings', 'case', 'cases', 'compatibility', 'credential_value_echoed', 'credential_value_serialized', 'event_identity_matches', 'evidence', 'exit_code', 'failed_staging', 'id', 'identity_matches', 'name', 'offline_validation', 'ok', 'per_stage_results', 'record', 'registry_version', 'resolved_args', 'run_id', 'runs', 'stage', 'staged_validation', 'status', 'steps', 'triggered', 'unauthorized', 'waitFor', 'wrong_artifact']\n\ndef execute(config, trigger, event, actions):\n    import re\n    if 'branch_filter' in trigger:\n        if re.fullmatch(trigger['branch_filter'], event.get('branch', '')) is None:\n            return {'triggered': False, 'steps': []}\n    elif any((event.get(k) != v for k, v in trigger['filters'].items())):\n        return {'triggered': False, 'steps': []}\n    binding = dict(config.get('substitutions', {}))\n    binding.update({k: event[v] for k, v in trigger['bindings'].items()})\n    results = []\n    statuses = {}\n    for step in config['steps']:\n        args = [str(a) for a in step.get('args', [])]\n        for k, v in binding.items():\n            args = [a.replace('${' + k + '}', str(v)) for a in args]\n        deps = [x for x in step['waitFor'] if x != '-']\n        record = {'id': step['id'], 'name': step['name'], 'resolved_args': args, 'waitFor': deps}\n        if any((statuses.get(d) != 'SUCCESS' for d in deps)):\n            record.update(status='NOT_STARTED', exit_code=None, evidence=None)\n        else:\n            if step.get('allowFailure') or any((x != 0 for x in step.get('allowExitCodes', []))):\n                raise ValueError('required gate failure allowances are forbidden')\n            callback = actions.get(step['id'])\n            context = dict(binding)\n            context['_RESOLVED_ARGS'] = args\n            result = callback(context) if callback else {'ok': True}\n            record.update(status='SUCCESS' if result['ok'] else 'FAILURE', exit_code=0 if result['ok'] else 1, evidence=result)\n        statuses[step['id']] = record['status']\n        results.append(record)\n    return {'triggered': True, 'bindings': binding, 'steps': results}\n\ndef promotion_gate(row):\n    approval = row['approval']\n    r = registry_records.get(row['registry_version'], {})\n    stage = {'compatibility': row['compatibility_ok'], 'offline_validation': row['offline_validation_ok'], 'staged_validation': row['staged_validation_ok'], 'authorization': approval['authorized']}\n    identities = row['artifact_id'] == row['staged_artifact_id'] == approval['artifact_id'] == r.get('artifact_id') and row['registry_version'] == approval['registry_version'] == r.get('version') and (row['run_id'] == r.get('run_id'))\n    ok = identities and all((stage.get(k, False) for k in required_stage_results)) and (set(required_stage_results) == set(stage))\n    record = {k: copy.deepcopy(row[k]) for k in ('approval', 'registry_version', 'run_id', 'artifact_id')}\n    record['accountable_identity'] = approval['accountable_identity']\n    record['per_stage_results'] = stage\n    return {'ok': ok, 'identity_matches': identities, 'record': record}\n\ndef exercise_case(case_id):\n    all_evidence = promotion_run()\n    return semantic_evidence({'case': all_evidence['cases'].get(case_id, {'ok': False, 'reason': 'missing case'}), 'all_evidence': all_evidence})\n\ndef semantic_evidence(value):\n    if isinstance(value, dict):\n        return {k: semantic_evidence(v) for k, v in value.items() if k in evidence_fields and k not in ('reason', 'failed', 'validation_count', 'config')}\n    if isinstance(value, list):\n        return [semantic_evidence(v) for v in value]\n    return value\n"

exec(adapter_source)

import copy

import yaml

required_stage_results = list(contract['required_results'])

configured_build = {'steps': [{'id': 'compatibility', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': ['-']}, {'id': 'staging_quality', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': []}, {'id': 'authorization', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}'], 'waitFor': []}, {'id': 'production', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', 'TODO_APPROVED_ARTIFACT_REFERENCE'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}

initial_build = __import__("copy").deepcopy(configured_build)

configured_build['steps'][1]['waitFor'] = ['compatibility']

configured_build['steps'][2]['waitFor'] = ['staging_quality']

configured_build['steps'][3]['waitFor'] = ['authorization']

configured_build['steps'][3]['args'] = ['python', 'downstream_entry.py', '${_ARTIFACT}']

configured_build['steps'][3]['secretEnv'] = ['PROMOTION_TOKEN']

configured_build['availableSecrets'] = {'secretManager': [{'versionName': 'projects/fixture-project/secrets/promotion-token/versions/1', 'env': 'PROMOTION_TOKEN'}]}

build_to_write = configured_build

candidate_build = __import__("copy").deepcopy(configured_build)

configured_build = initial_build

with open('exercise_configuration.yaml', 'w') as file_handle:
    yaml.safe_dump(configured_build, file_handle)

with open('exercise_configuration.yaml') as file_handle:
    reloaded_build = yaml.safe_load(file_handle)

def promotion_run():
    resolved = reloaded_build
    assert resolved == configured_build
    assert resolved['steps'][0]['id'] == 'compatibility'
    assert resolved['steps'][0]['name'] == 'python:3.11'
    assert resolved['steps'][0]['args'] == ['python', 'learner.py', '${_CASE}']
    assert resolved['steps'][0]['waitFor'] == ['-']
    assert resolved['steps'][1]['id'] == 'staging_quality'
    assert resolved['steps'][1]['name'] == 'python:3.11'
    assert resolved['steps'][1]['args'] == ['python', 'learner.py', '${_CASE}']
    assert resolved['steps'][1]['waitFor'] == ['compatibility']
    assert resolved['steps'][2]['id'] == 'authorization'
    assert resolved['steps'][2]['name'] == 'python:3.11'
    assert resolved['steps'][2]['args'] == ['python', 'learner.py', '${_CASE}']
    assert resolved['steps'][2]['waitFor'] == ['staging_quality']
    assert resolved['steps'][3]['id'] == 'production'
    assert resolved['steps'][3]['name'] == 'python:3.11'
    assert resolved['steps'][3]['args'] == ['python', 'downstream_entry.py', '${_ARTIFACT}']
    assert resolved['steps'][3]['waitFor'] == ['authorization']
    for step in resolved['steps']:
        assert not step.get('allowFailure')
        assert all((code == 0 for code in step.get('allowExitCodes', [])))
    evidence = {k: promotion_gate(v) for k, v in cases.items()}

    def action(b):
        row = cases.get(b['_CASE'])
        if row is None:
            return {'ok': False, 'reason': 'unknown case'}
        result = promotion_gate(row)
        result['event_identity_matches'] = row['artifact_id'] == b['_ARTIFACT']
        result['ok'] = result['ok'] and result['event_identity_matches']
        return result

    def compatibility(b):
        row = cases.get(b['_CASE'])
        return {'ok': bool(row and row['compatibility_ok']), 'stage': 'compatibility'}

    def staging(b):
        row = cases.get(b['_CASE'])
        return {'ok': bool(row and row['offline_validation_ok'] and row['staged_validation_ok'] and (row['staged_artifact_id'] == b['_ARTIFACT'])), 'stage': 'staging_quality'}
    runs = [execute(resolved, trigger, e, {'compatibility': compatibility, 'staging_quality': staging, 'authorization': action, 'production': action}) for e in trigger['fixtures']]
    production = [s for s in resolved['steps'] if s['id'] == 'production'][0]
    serialized = yaml.safe_dump(resolved)
    credential_value_serialized = any((marker in serialized for marker in ('PROMOTION_TOKEN=', 'Bearer ', 'credential_value:')))
    credential_value_echoed = any((marker in captured_output[channel] for channel in ('stdout', 'stderr') for marker in ('PROMOTION_TOKEN=', 'Bearer ', 'credential_value:')))
    approved_secret = approved_secret_references
    assert resolved['availableSecrets']['secretManager'] == approved_secret
    assert_promotion_run_fixtures(approved_secret, credential_value_echoed, credential_value_serialized, evidence, production, resolved, runs)
    return {'cases': evidence, 'config': resolved, 'runs': runs, 'credential_value_serialized': credential_value_serialized, 'credential_value_echoed': credential_value_echoed}


exec(supplied_promotion_run_source)

def assert_promotion_run_fixtures(approved_secret, credential_value_echoed, credential_value_serialized, evidence, production, resolved, runs):
    assert evidence['accepted']['ok']
    assert all((not v['ok'] for k, v in evidence.items() if k != 'accepted'))
    assert production['secretEnv'] == ['PROMOTION_TOKEN']
    assert all(('secretEnv' not in s for s in resolved['steps'] if s['id'] != 'production'))
    assert not credential_value_serialized and (not credential_value_echoed)
    assert all((set(ref) == {'versionName', 'env'} for ref in approved_secret))
    for case in evidence.values():
        assert all((field in case['record'] for field in contract['record_fields']))
    assert runs[0]['steps'][-1]['status'] == 'SUCCESS'
    assert runs[1]['steps'][-1]['status'] == 'NOT_STARTED'


result = promotion_run()