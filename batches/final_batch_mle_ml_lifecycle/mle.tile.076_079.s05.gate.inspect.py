def dependency_run():
    resolved = reloaded_build
    assert resolved == configured_build
    assert resolved['steps'][0]['id'] == 'data_validation'
    assert resolved['steps'][0]['name'] == 'python:3.11'
    assert resolved['steps'][0]['args'] == ['python', 'learner.py', '${_CASE}']
    assert resolved['steps'][0]['waitFor'] == ['-']
    assert resolved['steps'][1]['id'] == 'training'
    assert resolved['steps'][1]['name'] == 'python:3.11'
    assert resolved['steps'][1]['args'] == ['python', 'downstream_entry.py', '${_ARTIFACT}']
    assert resolved['steps'][1]['waitFor'] == ['data_validation']
    assert resolved['steps'][2]['id'] == 'model_validation'
    assert resolved['steps'][2]['name'] == 'python:3.11'
    assert resolved['steps'][2]['args'] == ['python', 'learner.py', '${_CASE}', 'A']
    assert resolved['steps'][2]['waitFor'] == ['training']
    for step in resolved['steps']:
        assert not step.get('allowFailure')
        assert all((code == 0 for code in step.get('allowExitCodes', [])))
    evidence = {k: dependency_checks(v) for k, v in cases.items()}
    repaired = copy.deepcopy(cases['mismatch'])
    repaired['model_validation']['consumed'] = repaired['training']['produced']
    repair = dependency_checks(repaired)

    def data_action(b):
        row = cases.get(b['_CASE'], cases['mismatch'])
        return {'ok': row['data_validation']['validation_ok'], 'consumed': row['data_validation']['consumed'], 'produced': row['data_validation']['produced'], 'parameters': row['data_validation']['parameters']}

    def training_action(b):
        row = cases.get(b['_CASE'], cases['mismatch'])
        return {'ok': row['data_validation']['produced'] == row['training']['consumed'], 'consumed': row['training']['consumed'], 'produced': b['_RESOLVED_ARGS'][-1], 'parameters': row['training']['parameters']}

    def model_action(b):
        row = cases.get(b['_CASE'], cases['mismatch'])
        record = dependency_checks(row)
        record['resolved_consumer_matches_producer'] = b['_RESOLVED_ARGS'][-1] == b['_ARTIFACT'] == row['training']['produced'] == row['model_validation']['consumed']
        record['ok'] = record['ok'] and record['resolved_consumer_matches_producer']
        return record
    runs = [execute(resolved, trigger, e, {'data_validation': data_action, 'training': training_action, 'model_validation': model_action}) for e in trigger['fixtures']]
    assert evidence['valid']['ok'] and evidence['boundary']['ok']
    assert not evidence['mismatch']['ok'] and (not evidence['rejected_data']['ok'])
    assert repair['ok']
    assert [s['status'] for s in runs[-2]['steps']] == ['FAILURE', 'NOT_STARTED', 'NOT_STARTED']
    for run in runs:
        if run['triggered']:
            for step in run['steps']:
                if step['status'] == 'SUCCESS':
                    assert step['resolved_args']
    return {'cases': evidence, 'repaired': repair, 'required_edges': required_edges, 'config': resolved, 'runs': runs}
