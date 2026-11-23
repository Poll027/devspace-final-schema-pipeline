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
    assert evidence['accepted']['ok']
    assert all((not v['ok'] for k, v in evidence.items() if k != 'accepted'))
    production = [s for s in resolved['steps'] if s['id'] == 'production'][0]
    assert production['secretEnv'] == ['PROMOTION_TOKEN']
    assert all(('secretEnv' not in s for s in resolved['steps'] if s['id'] != 'production'))
    serialized = yaml.safe_dump(resolved)
    credential_value_serialized = any((marker in serialized for marker in ('PROMOTION_TOKEN=', 'Bearer ', 'credential_value:')))
    credential_value_echoed = any((marker in captured_output[channel] for channel in ('stdout', 'stderr') for marker in ('PROMOTION_TOKEN=', 'Bearer ', 'credential_value:')))
    assert not credential_value_serialized and (not credential_value_echoed)
    approved_secret = approved_secret_references
    assert resolved['availableSecrets']['secretManager'] == approved_secret
    assert all((set(ref) == {'versionName', 'env'} for ref in approved_secret))
    for case in evidence.values():
        assert all((field in case['record'] for field in contract['record_fields']))
    assert runs[0]['steps'][-1]['status'] == 'SUCCESS'
    assert runs[1]['steps'][-1]['status'] == 'NOT_STARTED'
    return {'cases': evidence, 'config': resolved, 'runs': runs, 'credential_value_serialized': credential_value_serialized, 'credential_value_echoed': credential_value_echoed}
