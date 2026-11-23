
import yaml

import hashlib

from storage_sim import RecoverableFailure, PreconditionFailed

from support import read, inject, record_failure, apply_recovery, validate_output, recovery_suite

# Supplied fixture implementation, unchanged from the validated reference.
with open('provided_syntax_scaffold.py') as supplied_implementation:
    exec(supplied_implementation.read())

# Supplied fixture helper; no learner edits required.
# Supplied practice helpers; inspect but do not edit.
with open('supplied_practice_helpers.py') as supplied_practice_helpers:
    exec(supplied_practice_helpers.read())



# Supplied fixture helper; no learner edits required.





trigger_event_type = 'artifact_ready'
selected_case = 'accepted'
config = read('cloudbuild.yaml')
no_predecessors = []
required_stage_1 = ['recovery']
required_stage_2 = ['required_validation']
stage_1_waits = no_predecessors  # TODO: repair this binding.
stage_2_waits = no_predecessors  # TODO: repair this binding.
config['steps'][1]['waitFor'] = stage_1_waits
config['steps'][2]['waitFor'] = stage_2_waits
with open('resolved.yaml', 'w') as file_handle:
    yaml.safe_dump(config, file_handle)
with open('resolved.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
report = recovery_suite(resolved, recover, selected_case, trigger_event_type)
assert report['runs']['accepted']['steps'][2]['status'] == 'SUCCESS'
assert report['runs']['rejected_gate']['steps'][1]['status'] == 'FAILURE'
assert report['runs']['rejected_gate']['steps'][2]['status'] == 'SKIPPED'
assert not report['outcomes']['invalid_existing']['first']['accepted']
assert not report['outcomes']['conflicting_content']['first']['accepted']
assert not report['outcomes']['unrelated_failure']['first']['accepted']
for name in ['accepted', 'boundary_completed', 'race_412']:
    outcome = report['outcomes'][name]
    assert outcome['first']['accepted'] and outcome['second']['accepted']
    assert outcome['before']['generations']['A'] == outcome['after']['generations']['A'] == outcome['again']['generations']['A']
    assert outcome['before']['hashes']['A'] == outcome['after']['hashes']['A'] == outcome['again']['hashes']['A']
    assert outcome['after']['generations'] == outcome['again']['generations']
    assert len(outcome['after']['uploads']) == len(outcome['again']['uploads'])
    for output in read('fixtures/recovery_contract.json')['outputs']:
        assert outcome['after']['hashes'][output] == read('fixtures/recovery_contract.json')['outputs'][output]['sha256']
        assert outcome['again']['validations'].count(output) > outcome['after']['validations'].count(output)
