
trigger_event_type = "artifact_ready"
selected_case = 'accepted'

import yaml
from support import read, promotion_suite
config=read('cloudbuild.yaml')
cases=read('fixtures/promotion_cases.json')
approved_artifact=cases['accepted']['approval']['artifact_id']
other_artifact=cases['wrong_artifact']['artifact_id']
production_artifact=other_artifact  # TODO: repair this binding.
compatibility_required = ['compatibility']
staging_required = ['staging_quality']
quality_and_authorization_required = ['staging_quality','authorization']
no_waits = []
# Learner bindings: production requires quality AND separate authorization.
staging_waits = no_waits  # TODO: repair this binding.
authorization_waits = no_waits  # TODO: repair this binding.
production_waits = no_waits  # TODO: repair this binding.
config['steps'][1]['waitFor']=staging_waits
config['steps'][2]['waitFor']=authorization_waits
config['steps'][3]['waitFor']=production_waits
config['substitutions']['_ARTIFACT']=production_artifact
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
report=promotion_suite(resolved,selected_case,trigger_event_type)
assert report['runs']['accepted']['steps'][3]['status']=='SUCCESS'
assert report['runs']['unauthorized']['steps'][3]['status']=='SKIPPED'
assert report['records']['accepted']['artifact_id']==report['records']['accepted']['approval']['artifact_id']

assert report['records']['accepted']['approval']==cases['accepted']['approval']
assert report['records']['accepted']['accountable_identity']==cases['accepted']['approval']['accountable_identity']
assert report['records']['accepted']['registry_version']==cases['accepted']['registry_version']
assert report['records']['accepted']['run_id']==cases['accepted']['run_id']
assert report['records']['accepted']['artifact_id']==cases['accepted']['artifact_id']
assert all(report['records']['accepted']['per_stage_results'][name] for name in read('fixtures/promotion_contract.json')['required_results'])
assert report['runs']['wrong_artifact']['steps'][3]['status']=='SKIPPED'
assert report['runs']['failed_staging']['steps'][3]['status']=='SKIPPED'
