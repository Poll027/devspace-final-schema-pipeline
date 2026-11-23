
trigger_event_type = "artifact_ready"
selected_case = 'valid'

import yaml
from support import read, dependency_suite
cases=read('fixtures/dependency_cases.json')
config=read('cloudbuild.yaml')
required_training_waits = ['data_validation']
required_model_waits = ['training']
no_waits = []
training_output = cases['valid']['training']['produced']
other_input = cases['mismatch']['model_validation']['consumed']
# Learner bindings: completion dependencies and artifact identity are separate.
training_waits = no_waits  # TODO: repair this binding.
model_waits = no_waits  # TODO: repair this binding.
model_input = other_input  # TODO: repair this binding.
config['steps'][1]['waitFor']=training_waits
config['steps'][2]['waitFor']=model_waits
config['steps'][1]['args'][-2]=cases['valid']['data_validation']['produced']
config['steps'][2]['args'][3]=model_input
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
assert cases['valid']['training']['produced']==cases['valid']['model_validation']['consumed']
assert cases['boundary']['training']['produced']==cases['boundary']['model_validation']['consumed']
assert cases['mismatch']['training']['produced']!=cases['mismatch']['model_validation']['consumed']
report=dependency_suite(resolved,cases,selected_case,trigger_event_type)
