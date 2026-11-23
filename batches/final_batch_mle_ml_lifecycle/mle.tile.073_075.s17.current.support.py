import copy, json, math, hashlib, io

import yaml

from decimal import Decimal

acceptance_checks = list(required_acceptance_checks)

configured_build = {'steps': [{'id': 'release_gate', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}', '${_ARTIFACT}'], 'waitFor': ['-']}, {'id': 'promotion', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'A', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}

configured_build['steps'][1]['waitFor'] = ['release_gate']

def error_cost(row):
    negatives = row['FP'] + row['TN']
    positives = row['FN'] + row['TP']
    if negatives <= 0 or positives <= 0:
        return None
    fpr = row['FP'] / negatives
    fnr = row['FN'] / positives
    cost = Decimal(str(contract['probabilities']['P(Y=0)'])) * Decimal(row['FP']) / Decimal(negatives) * Decimal(contract['costs']['cost_FP']) + Decimal(str(contract['probabilities']['P(Y=1)'])) * Decimal(row['FN']) / Decimal(positives) * Decimal(contract['costs']['cost_FN'])
    return {'FPR': fpr, 'FNR': fnr, 'expected_error_cost': float(cost)}

def release_gate(row, event_artifact):
    fields = ('candidate_id', 'FP', 'TN', 'FN', 'TP', 'latency_ms', 'operating_ok', 'evidence_complete')
    checks = {}
    checks['evidence'] = all((k in row and row[k] is not None for k in fields)) and row.get('evidence_complete') is True
    checks['counts'] = all((type(row.get(k)) is int and row[k] >= 0 for k in ('FP', 'TN', 'FN', 'TP')))
    metrics = error_cost(row) if checks['evidence'] and checks['counts'] else None
    checks['denominators'] = metrics is not None
    checks['identity'] = row.get('candidate_id') is not None and row.get('candidate_id') == event_artifact
    reference = error_cost(cases[contract['accepted_reference']])
    checks['cost'] = metrics is not None and metrics['expected_error_cost'] <= max_error_cost and (metrics['expected_error_cost'] <= reference['expected_error_cost'])
    latency = row.get('latency_ms')
    checks['latency'] = type(latency) in (int, float) and math.isfinite(latency) and (latency <= max_latency)
    checks['operating'] = row.get('operating_ok') is True
    failed = [k for k in required_acceptance_checks if not checks.get(k, False)]
    failed += [k for k in required_acceptance_checks if k not in acceptance_checks and k not in failed]
    return {'ok': not failed and set(acceptance_checks) == set(required_acceptance_checks), 'candidate_id': row.get('candidate_id'), 'metrics': metrics, 'checks': checks, 'failed_checks': failed}

def release_run():
    with open('configured_build.yaml', 'w') as file_handle:
        yaml.safe_dump(configured_build, file_handle)
    with open('configured_build.yaml') as file_handle:
        resolved = yaml.safe_load(file_handle)
    assert resolved == configured_build
    assert resolved['steps'][0]['id'] == 'release_gate'
    assert resolved['steps'][0]['name'] == 'python:3.11'
    assert resolved['steps'][0]['args'] == ['python', 'learner.py', '${_CASE}', '${_ARTIFACT}']
    assert resolved['steps'][0]['waitFor'] == ['-']
    assert resolved['steps'][1]['id'] == 'promotion'
    assert resolved['steps'][1]['name'] == 'python:3.11'
    assert resolved['steps'][1]['args'] == ['python', 'downstream_entry.py', '${_ARTIFACT}']
    assert resolved['steps'][1]['waitFor'] == ['release_gate']
    for step in resolved['steps']:
        assert not step.get('allowFailure')
        assert all((code == 0 for code in step.get('allowExitCodes', [])))
    evidence = {k: release_gate(v, cases['A']['candidate_id'] if k == 'case_artifact_mismatch' else v.get('candidate_id')) for k, v in cases.items()}

    def action(b):
        r = cases.get(b['_CASE'])
        return release_gate(r, b['_ARTIFACT']) if r else {'ok': False, 'failed_checks': ['missing candidate evidence']}
    runs = [execute(resolved, trigger, e, {'release_gate': action}) for e in trigger['fixtures']]
    assert evidence['A']['ok'] and evidence['boundary']['ok']
    assert not evidence['B']['ok']
    for k in ('empty_negatives', 'empty_positives', 'incomplete', 'cost_failure', 'operating_failure', 'missing_field', 'invalid_count', 'case_artifact_mismatch'):
        assert not evidence[k]['ok']
    assert runs[0]['steps'][1]['status'] == 'SUCCESS'
    assert runs[1]['steps'][1]['status'] == 'NOT_STARTED'
    assert 'identity' in evidence['case_artifact_mismatch']['failed_checks']
    assert runs[-1]['steps'][1]['status'] == 'NOT_STARTED'
    return {'cases': evidence, 'config': resolved, 'runs': runs, 'protected_test_used': False}
