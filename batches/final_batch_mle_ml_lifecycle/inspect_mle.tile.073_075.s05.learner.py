
import yaml

import math

from support import read, inspect_config, trigger_run, fixture_events, status, assertion_failure

with open('provided_gate.py') as supplied_implementation:
    exec(supplied_implementation.read())

# Supplied fixture helper; no learner edits required.
# Supplied practice helpers; inspect but do not edit.
with open('supplied_practice_helpers.py') as supplied_practice_helpers:
    exec(supplied_practice_helpers.read())



# Supplied fixture helper; no learner edits required.



# Supplied fixture implementation, unchanged from the validated reference.




cases = read('fixtures/dataset_cases.json')

contract = read('fixtures/dataset_contract.json')

retained = {}

trigger_branch = 'main'
selected_case = 'valid'
results = {}
for name in cases:
    results[name] = dataset_gate(cases[name], contract['required_checks'])
for fixture_name in cases:
    if fixture_name in ['valid', 'boundary']:
        assert results[fixture_name]['accepted']
    else:
        assert not results[fixture_name]['accepted']
        assert results[fixture_name]['failed_checks']
assert results['valid']['accepted']
assert results['boundary']['accepted']
assert not results['missing_required_feature']['accepted']
assert 'schema' in results['missing_required_feature']['failed_checks']
config = read('cloudbuild.yaml')
no_predecessors = []
required_stage_1 = ['quality']
stage_1_waits = no_predecessors  # TODO: repair this binding.
config['steps'][1]['waitFor'] = stage_1_waits
file_handle = open('resolved.yaml', 'w')
yaml.safe_dump(config, file_handle)
file_handle.close()
file_handle = open('resolved.yaml')
resolved = yaml.safe_load(file_handle)
file_handle.close()
inspect_config(resolved)
runs = []
for event in fixture_events('repository_commit'):
    runs.append(trigger_run(resolved, 'repository_commit', event, {'quality': fatal_dataset}))
assert status(runs[0], 'training') == 'SUCCESS'
assert status(runs[1], 'quality') == 'FAILURE'
assert status(runs[1], 'training') == 'SKIPPED'
event = {'branch': trigger_branch, 'snapshot_id': selected_case}
selected_run = trigger_run(resolved, 'repository_commit', event, {'quality': fatal_dataset})
report = {'config': resolved, 'results': results, 'retained': retained, 'runs': runs, 'selected_run': selected_run, 'false_assert_raises': assertion_failure()}
