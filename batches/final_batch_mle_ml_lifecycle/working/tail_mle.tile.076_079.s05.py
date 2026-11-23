trigger_event_type = "artifact_ready"
selected_case = 'valid'
import os
from pathlib import Path
for path, content in support_files.items():
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    Path(path).write_text(content)
import yaml
from support import read, dependency_suite
cases=read('fixtures/dependency_cases.json')
config=read('cloudbuild.yaml')
required_training_waits = ['data_validation']
required_model_waits = ['training']
no_waits = []
training_output = cases['valid']['training']['produced']
other_input = cases['mismatch']['model_validation']['consumed']
training_waits = required_training_waits
model_waits = required_model_waits
model_input = training_output
config['steps'][1]['waitFor']=training_waits
config['steps'][2]['waitFor']=model_waits
config['steps'][2]['args'][3]=model_input
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
assert cases['valid']['training']['produced']==cases['valid']['model_validation']['consumed']
assert cases['boundary']['training']['produced']==cases['boundary']['model_validation']['consumed']
assert cases['mismatch']['training']['produced']!=cases['mismatch']['model_validation']['consumed']
report=dependency_suite(resolved,cases,selected_case,trigger_event_type)
