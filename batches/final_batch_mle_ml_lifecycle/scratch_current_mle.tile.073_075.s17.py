# LOCAL SIMULATION ONLY: execute invokes fixture callbacks. Its exits, statuses,
# resolved inputs and promotion records are simulated, not actual triggered execution.
# Actual execution/promotion requires a human-provisioned authorized hosted route;
# no such callable route or credentials are supplied by these frozen inputs.
cases = {'reference': {'candidate_id': 'reference', 'FP': 10, 'TN': 90, 'FN': 10, 'TP': 90, 'latency_ms': 18, 'operating_ok': True, 'evidence_complete': True}, 'A': {'candidate_id': 'A', 'FP': 5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'B': {'candidate_id': 'B', 'FP': 4, 'TN': 96, 'FN': 4, 'TP': 96, 'latency_ms': 21, 'operating_ok': True, 'evidence_complete': True}, 'boundary': {'candidate_id': 'boundary', 'FP': 10, 'TN': 90, 'FN': 10, 'TP': 90, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'empty_negatives': {'candidate_id': 'empty_negatives', 'FP': 0, 'TN': 0, 'FN': 5, 'TP': 95, 'latency_ms': 15, 'operating_ok': True, 'evidence_complete': True}, 'empty_positives': {'candidate_id': 'empty_positives', 'FP': 5, 'TN': 95, 'FN': 0, 'TP': 0, 'latency_ms': 15, 'operating_ok': True, 'evidence_complete': True}, 'incomplete': {'candidate_id': 'incomplete', 'FP': 5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': None, 'operating_ok': True, 'evidence_complete': False}, 'cost_failure': {'candidate_id': 'cost_failure', 'FP': 40, 'TN': 60, 'FN': 40, 'TP': 60, 'latency_ms': 15, 'operating_ok': True, 'evidence_complete': True}, 'operating_failure': {'candidate_id': 'operating_failure', 'FP': 5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 15, 'operating_ok': False, 'evidence_complete': True}, 'missing_field': {'candidate_id': 'A', 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'invalid_count': {'candidate_id': 'A', 'FP': -5, 'TN': 95, 'FN': 5, 'TP': 95, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}, 'case_artifact_mismatch': {'candidate_id': 'B', 'FP': 4, 'TN': 96, 'FN': 4, 'TP': 96, 'latency_ms': 20, 'operating_ok': True, 'evidence_complete': True}}
contract = {'probabilities': {'P(Y=0)': 0.8, 'P(Y=1)': 0.2}, 'costs': {'cost_FP': 1, 'cost_FN': 4, 'correct_prediction': 0}, 'max_expected_error_cost': 0.16, 'max_latency_ms': 20, 'accepted_reference': 'reference', 'requirements': ['all evidence fields present', 'nonnegative integer counts', 'both actual-class denominators nonempty', 'candidate identity matches event', 'expected error cost <= fixed maximum and <= accepted reference cost', 'latency_ms <= fixed maximum', 'operating_ok is True', 'evidence_complete is True'], 'protected_test_use': 'Never fit, select, or tune using protected-test observations.'}
trigger = {'id': 'fixture-artifact-trigger', 'topic': 'projects/fixture-project/topics/artifacts', 'bindings': {'_CASE': 'case_id', '_ARTIFACT': 'artifact_id'}, 'filters': {'event_type': 'artifact_ready'}, 'fixtures': [{'event_type': 'artifact_ready', 'case_id': 'A', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'B', 'artifact_id': 'B'}, {'event_type': 'unrelated', 'case_id': 'A', 'artifact_id': 'A'}, {'event_type': 'artifact_ready', 'case_id': 'case_artifact_mismatch', 'artifact_id': 'A'}]}
max_error_cost = 0.16
max_latency = 20
required_acceptance_checks = ['evidence', 'counts', 'denominators', 'identity', 'cost', 'latency', 'operating']
adapter_source = "evidence_fields = ['A', 'B', 'FNR', 'FPR', '_ARTIFACT', '_CASE', '_SNAPSHOT', 'all_evidence', 'bindings', 'boundary', 'candidate_id', 'case', 'case_artifact_mismatch', 'cases', 'checks', 'cost', 'cost_failure', 'counts', 'denominators', 'empty_negatives', 'empty_positives', 'evidence', 'exit_code', 'expected_error_cost', 'failed_checks', 'id', 'identity', 'incomplete', 'invalid_count', 'latency', 'metrics', 'missing_field', 'name', 'ok', 'operating', 'operating_failure', 'protected_test_used', 'reference', 'resolved_args', 'runs', 'status', 'steps', 'triggered', 'waitFor']\n\ndef execute(config, trigger, event, actions):\n    # This is a local simulation, never actual hosted execution or promotion.\n    import re\n    if 'branch_filter' in trigger:\n        if re.fullmatch(trigger['branch_filter'], event.get('branch', '')) is None:\n            return {'evidence_kind': 'simulation', 'triggered': False, 'steps': []}\n    elif any((event.get(k) != v for k, v in trigger['filters'].items())):\n        return {'evidence_kind': 'simulation', 'triggered': False, 'steps': []}\n    binding = dict(config.get('substitutions', {}))\n    binding.update({k: event[v] for k, v in trigger['bindings'].items()})\n    results = []\n    statuses = {}\n    for step in config['steps']:\n        args = [str(a) for a in step.get('args', [])]\n        for k, v in binding.items():\n            args = [a.replace('${' + k + '}', str(v)) for a in args]\n        deps = [x for x in step['waitFor'] if x != '-']\n        record = {'id': step['id'], 'name': step['name'], 'resolved_args': args, 'waitFor': deps}\n        if any((statuses.get(d) != 'SUCCESS' for d in deps)):\n            record.update(status='NOT_STARTED', exit_code=None, evidence=None)\n        else:\n            if step.get('allowFailure') or any((x != 0 for x in step.get('allowExitCodes', []))):\n                raise ValueError('required gate failure allowances are forbidden')\n            callback = actions.get(step['id'])\n            context = dict(binding)\n            context['_RESOLVED_ARGS'] = args\n            result = callback(context) if callback else {'ok': True}\n            record.update(status='SUCCESS' if result['ok'] else 'FAILURE', exit_code=0 if result['ok'] else 1, evidence=result)\n        statuses[step['id']] = record['status']\n        results.append(record)\n    return {'evidence_kind': 'simulation', 'triggered': True, 'bindings': binding, 'steps': results}\n\ndef exercise_case(case_id):\n    all_evidence = release_run()\n    return semantic_evidence({'case': all_evidence['cases'].get(case_id, {'ok': False, 'reason': 'missing case'}), 'all_evidence': all_evidence})\n\ndef semantic_evidence(value):\n    if isinstance(value, dict):\n        return {k: sorted(v) if k == 'failed_checks' else semantic_evidence(v) for k, v in value.items() if k in evidence_fields and k not in ('reason', 'failed', 'validation_count', 'config')}\n    if isinstance(value, list):\n        return [semantic_evidence(v) for v in value]\n    return value\n"
exec(adapter_source)
import math
import yaml
from decimal import Decimal
acceptance_checks = list(required_acceptance_checks)
configured_build = {'steps': [{'id': 'release_gate', 'name': 'python:3.11', 'args': ['python', 'learner.py', '${_CASE}', '${_ARTIFACT}'], 'waitFor': ['-']}, {'id': 'promotion', 'name': 'python:3.11', 'args': ['python', 'downstream_entry.py', '${_ARTIFACT}'], 'waitFor': []}], 'substitutions': {'_SNAPSHOT': 'valid', '_CASE': 'A', '_ARTIFACT': 'A'}, 'serviceAccount': 'projects/fixture-project/serviceAccounts/fixture-build@fixture-project.iam.gserviceaccount.com'}
configured_build['steps'][1]['waitFor'] = ['release_gate']

# Supplied fixture assertions.
# Supplied fixture support (not an editable task).
if True:
    def error_cost(row):
        negatives = row['FP'] + row['TN']
        positives = row['FN'] + row['TP']
        if negatives <= 0 or positives <= 0:
            return None
        fpr = row['FP'] / negatives
        fnr = row['FN'] / positives
        cost = Decimal(str(contract['probabilities']['P(Y=0)'])) * Decimal(row['FP']) / Decimal(negatives) * Decimal(contract['costs']['cost_FP']) + Decimal(str(contract['probabilities']['P(Y=1)'])) * Decimal(row['FN']) / Decimal(positives) * Decimal(contract['costs']['cost_FN'])
        return {'FPR': fpr, 'FNR': fnr, 'expected_error_cost': float(cost)}

# Supplied fixture assertions.
# Supplied fixture support (not an editable task).
if True:
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
        evidence = {'ok': not failed and set(acceptance_checks) == set(required_acceptance_checks), 'candidate_id': row.get('candidate_id'), 'metrics': metrics, 'checks': checks, 'failed_checks': failed}
        if not evidence['ok']:
            raise ReleaseRejected(evidence)
        return evidence

# Supplied fixture assertions.
supplied_definition_16 = 'class ReleaseRejected(ValueError):\n    def __init__(self, evidence):\n        self.evidence = evidence\n        super().__init__("failed checks: " + ", ".join(evidence["failed_checks"]))\n'
exec(supplied_definition_16)

# Supplied fixture assertions.
supplied_definition_17 = 'def capture_release(row, event_artifact):\n    # Capture only the declared rejection; unrelated runtime failures propagate.\n    try:\n        return release_gate(row, event_artifact)\n    except ReleaseRejected as rejection:\n        return rejection.evidence\n'
exec(supplied_definition_17)
supplied_release_run_source = "def release_run():\n    resolved = reloaded_build\n    assert resolved == configured_build\n    assert resolved['steps'][0]['id'] == 'release_gate'\n    assert resolved['steps'][0]['name'] == 'python:3.11'\n    assert resolved['steps'][0]['args'] == ['python', 'learner.py', '${_CASE}', '${_ARTIFACT}']\n    assert resolved['steps'][0]['waitFor'] == ['-']\n    assert resolved['steps'][1]['id'] == 'promotion'\n    assert resolved['steps'][1]['name'] == 'python:3.11'\n    assert resolved['steps'][1]['args'] == ['python', 'downstream_entry.py', '${_ARTIFACT}']\n    assert resolved['steps'][1]['waitFor'] == ['release_gate']\n    for step in resolved['steps']:\n        assert not step.get('allowFailure')\n        assert all((code == 0 for code in step.get('allowExitCodes', [])))\n    evidence = {k: capture_release(v, cases['A']['candidate_id'] if k == 'case_artifact_mismatch' else v.get('candidate_id')) for k, v in cases.items()}\n\n    def action(b):\n        r = cases.get(b['_CASE'])\n        result = capture_release(r, b['_ARTIFACT']) if r else {'ok': False, 'failed_checks': ['evidence']}\n        result['ok'] = bool(result.get('ok')) and not result.get('failed_checks')\n        return result\n    runs = [execute(resolved, trigger, e, {'release_gate': action}) for e in trigger['fixtures']]\n    assert_release_run_fixtures(evidence, runs)\n    return {'cases': evidence, 'config': resolved, 'runs': runs, 'protected_test_used': False}\n"
exec(supplied_release_run_source)
with open('exercise_configuration.yaml', 'w') as file_handle:
    yaml.safe_dump(configured_build, file_handle)
with open('exercise_configuration.yaml') as file_handle:
    loaded_build = yaml.safe_load(file_handle)
# Safely write, reload and inspect the configuration, then bind reloaded_build.
# TODO: Bind reloaded_build to the safely reloaded mapping above.
reloaded_build = None

# Supplied fixture assertions.
# Supplied fixture support (not an editable task).
if True:
    def assert_release_run_fixtures(evidence, runs):
        assert evidence['A']['ok'] and evidence['boundary']['ok']
        assert not evidence['B']['ok']
        for k in ('empty_negatives', 'empty_positives', 'incomplete', 'cost_failure', 'operating_failure', 'missing_field', 'invalid_count', 'case_artifact_mismatch'):
            assert not evidence[k]['ok']
        assert runs[0]['steps'][1]['status'] == 'SUCCESS'
        assert runs[1]['steps'][1]['status'] == 'NOT_STARTED'
        assert 'identity' in evidence['case_artifact_mismatch']['failed_checks']
        assert runs[-1]['steps'][1]['status'] == 'NOT_STARTED'
    
        # Assert actual rejection exceptions, not merely false flags from the harness.
        for key, row in cases.items():
            event_artifact = cases['A']['candidate_id'] if key == 'case_artifact_mismatch' else row.get('candidate_id')
            if evidence[key]['ok']:
                assert release_gate(row, event_artifact)['ok']
            else:
                try:
                    release_gate(row, event_artifact)
                except ReleaseRejected as rejection:
                    assert rejection.evidence == evidence[key]
                    for check in evidence[key]['failed_checks']:
                        assert check in str(rejection)
                else:
                    raise AssertionError('required release rejection did not raise')
result = release_run()
