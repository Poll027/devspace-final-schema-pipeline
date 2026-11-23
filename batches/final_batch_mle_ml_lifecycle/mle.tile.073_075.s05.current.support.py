import copy, json, math, hashlib, io

import yaml

gate_checks = list(contract['required_checks'])

configured_build = {'steps': [{'id': 'quality', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_SNAPSHOT}'], 'waitFor': ['-']}, {'id': 'training', 'name': 'python:3.11', 'args': ['python', 'training_entry.py', '${_SNAPSHOT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'accepted', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}

configured_build['steps'][1]['waitFor'] = ['quality']

def dataset_gate(case, rules):
    rows = case['rows']
    result = {}
    result['schema'] = bool(rows) and all((set(r) == set(contract['columns']) for r in rows))
    result['feature_values'] = all((isinstance(r.get('feature'), (int, float)) and (not isinstance(r.get('feature'), bool)) and math.isfinite(r['feature']) and (feature_min <= r['feature'] <= feature_max) for r in rows))
    result['label_values'] = all((type(r.get('label')) is int and r['label'] in (0, 1) for r in rows))
    ids = [r.get('sample_id') for r in rows]
    result['unique_sample_id'] = all((isinstance(i, str) and i for i in ids)) and len(ids) == len(set(ids))
    failed = [k for k in contract['required_checks'] if k not in rules or not result.get(k, False)]
    return {'ok': not failed and set(rules) == set(contract['required_checks']), 'snapshot_id': case['snapshot_id'], 'sha256': case['sha256'], 'checks': result, 'failed_checks': failed}

def dataset_run():
    resolved = reloaded_build
    assert resolved == configured_build
    assert resolved['steps'][0]['id'] == 'quality'
    assert resolved['steps'][0]['name'] == 'python:3.11'
    assert resolved['steps'][0]['args'] == ['python', 'learner.py', '${_SNAPSHOT}']
    assert resolved['steps'][0]['waitFor'] == ['-']
    assert resolved['steps'][1]['id'] == 'training'
    assert resolved['steps'][1]['name'] == 'python:3.11'
    assert resolved['steps'][1]['args'] == ['python', 'training_entry.py', '${_SNAPSHOT}']
    assert resolved['steps'][1]['waitFor'] == ['quality']
    for step in resolved['steps']:
        assert not step.get('allowFailure')
        assert all((code == 0 for code in step.get('allowExitCodes', [])))
    evidence = {k: dataset_gate(v, gate_checks) for k, v in cases.items()}
    events = trigger['fixtures']
    runs = [execute(resolved, trigger, e, {'quality': lambda b: dataset_gate(cases.get(b['_SNAPSHOT'], {'rows': [], 'snapshot_id': b['_SNAPSHOT'], 'sha256': None}), gate_checks)}) for e in events]
    assert evidence['valid']['ok']
    assert evidence['boundary']['ok']
    for k in cases:
        if k not in ('valid', 'boundary'):
            assert not evidence[k]['ok']
            assert evidence[k]['failed_checks']
    assert runs[0]['steps'][1]['status'] == 'SUCCESS'
    assert runs[1]['steps'][1]['status'] == 'NOT_STARTED'
    repaired = copy.deepcopy(cases['missing_required_feature'])
    repaired['rows'] = copy.deepcopy(cases['valid']['rows'])
    repaired['snapshot_id'] = repaired['snapshot_id'] + '.repaired'
    repaired['sha256'] = hashlib.sha256(json.dumps(repaired['rows'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    repair = dataset_gate(repaired, gate_checks)
    assert repair['ok'] and repair['snapshot_id'] != evidence['missing_required_feature']['snapshot_id']
    assert repair['sha256'] != evidence['missing_required_feature']['sha256']
    assert not dataset_gate(cases['valid'], gate_checks[:-1])['ok']
    return {'cases': evidence, 'config': resolved, 'runs': runs, 'repaired_under_same_contract': repair}
