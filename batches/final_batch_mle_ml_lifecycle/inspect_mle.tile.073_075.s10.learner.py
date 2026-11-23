
import numpy as np

import yaml

from prediction_package import FittedPackage, InputContractError

from support import read, inspect_config, trigger_run, fixture_events, status, assertion_failure, rejection

# Supplied fixture implementation, unchanged from the validated reference.
with open('provided_syntax_scaffold.py') as supplied_implementation:
    exec(supplied_implementation.read())

# Supplied fixture helper; no learner edits required.
# Supplied practice helpers; inspect but do not edit.
with open('supplied_practice_helpers.py') as supplied_practice_helpers:
    exec(supplied_practice_helpers.read())





cases = read('fixtures/behavior_cases.json')

contract = read('fixtures/behavior_contract.json')

execution = read('fixtures/behavior_execution_cases.json')

trigger_branch = 'main'
selected_case = 'accepted'
results = {}
for name in cases:
    results[name] = test_behavior(FittedPackage(), cases[name], contract)
regressions = {}
for regression in contract['regressions']:
    regressions[regression] = rejection(test_behavior, FittedPackage(regression), cases['valid'], contract)
    assert not regressions[regression]['accepted']
config = read('cloudbuild.yaml')
no_predecessors = []
required_stage_1 = ['behavior_tests']
stage_1_waits = no_predecessors  # TODO: repair this binding.
config['steps'][1]['waitFor'] = stage_1_waits
with open('resolved.yaml', 'w') as file_handle:
    yaml.safe_dump(config, file_handle)
with open('resolved.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
inspect_config(resolved)
runs = []
for event in fixture_events('repository_commit'):
    runs.append(trigger_run(resolved, 'repository_commit', event, {'behavior_tests': fatal_behavior}))
assert status(runs[0], 'release_gate') == 'SUCCESS'
assert status(runs[1], 'behavior_tests') == 'FAILURE'
assert status(runs[1], 'release_gate') == 'SKIPPED'
selected_run = trigger_run(resolved, 'repository_commit', {'branch': trigger_branch, 'snapshot_id': 'valid', 'case_id': selected_case}, {'behavior_tests': fatal_behavior})
report = {'config': resolved, 'results': results, 'regressions': regressions, 'runs': runs, 'selected_run': selected_run, 'false_assert_raises': assertion_failure()}
for name in cases:
    assert rejection(test_behavior, FittedPackage(), cases[name], contract)['accepted']
