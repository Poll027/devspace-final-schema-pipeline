
import yaml

from support import read, inspect_config, trigger_run, fixture_events, status, rejection, valid_count

# Supplied fixture implementation, unchanged from the validated reference.
with open('provided_syntax_scaffold.py') as supplied_implementation:
    exec(supplied_implementation.read())

# Supplied fixture helper; no learner edits required.
# Supplied practice helpers; inspect but do not edit.
with open('supplied_practice_helpers.py') as supplied_practice_helpers:
    exec(supplied_practice_helpers.read())



# Supplied fixture helper; no learner edits required.






cases = read('fixtures/release_cases.json')

contract = read('fixtures/release_contract.json')

trigger_event_type = 'artifact_ready'
selected_case = 'A'
results = {}
for name in cases:
    results[name] = rejection(acceptance, cases[name], cases[contract['accepted_reference']], contract, cases[name]['candidate_id'])
assert results['A']['accepted']
assert results['boundary']['accepted']
assert not results['B']['accepted']
assert not results['empty_negatives']['accepted']
assert not results['empty_positives']['accepted']
assert not results['incomplete']['accepted']
for predicate in ['evidence_complete', 'operating_ok']:
    for value in ['false', 1]:
        candidate = dict(cases['A'])
        candidate[predicate] = value
        outcome = rejection(acceptance, candidate, cases[contract['accepted_reference']], contract, candidate['candidate_id'])
        assert not outcome['accepted']
        results[predicate + str(value)] = outcome
config = read('cloudbuild.yaml')
no_predecessors = []
required_stage_1 = ['release_gate']
stage_1_waits = no_predecessors  # TODO: repair this binding.
config['steps'][1]['waitFor'] = stage_1_waits
with open('resolved.yaml', 'w') as file_handle:
    yaml.safe_dump(config, file_handle)
with open('resolved.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
inspect_config(resolved)
runs = []
for event in fixture_events('pubsub'):
    runs.append(trigger_run(resolved, 'pubsub', event, {'release_gate': fatal_acceptance}))
assert status(runs[0], 'promotion') == 'SUCCESS'
assert status(runs[1], 'release_gate') == 'FAILURE'
assert status(runs[1], 'promotion') == 'SKIPPED'
event = {'event_type': trigger_event_type, 'case_id': selected_case, 'artifact_id': selected_case}
selected_run = trigger_run(resolved, 'pubsub', event, {'release_gate': fatal_acceptance})
identity_run = trigger_run(resolved, 'pubsub', {'event_type': fixture_events('pubsub')[0]['event_type'], 'case_id': 'B', 'artifact_id': 'A'}, {'release_gate': fatal_acceptance})
assert status(identity_run, 'release_gate') == 'FAILURE'
assert status(identity_run, 'promotion') == 'SKIPPED'
report = {'identity_run': identity_run, 'config': resolved, 'results': results, 'runs': runs, 'selected_run': selected_run}
