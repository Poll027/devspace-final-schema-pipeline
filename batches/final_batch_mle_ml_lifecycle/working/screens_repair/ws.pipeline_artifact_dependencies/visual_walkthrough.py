import json, copy, yaml
from pathlib import Path
from runtime_sim import run_build
load = lambda p: json.loads(Path(p).read_text())
cases = load('fixtures/dependency_cases.json')
supplied = yaml.safe_load(Path('cloudbuild.yaml').read_text())
print(json.dumps({'supplied_fixtures':cases, 'parsed_supplied_cloudbuild_yaml':supplied}, indent=2))
# Author a demonstration entry point in an isolated copy; the supplied learner.py remains unwritten.
Path('demonstration_entry.py').write_text("import json, sys, math, hashlib\nfrom pathlib import Path\nload = lambda p: json.loads(Path(p).read_text())\n\ncase=load('fixtures/dependency_cases.json')[sys.argv[1]]\nstage=sys.argv[2]\nif stage=='data_validation':\n result={'stage':stage, 'resolved_consumed':case[stage]['consumed'],'validation_ok':case[stage]['validation_ok']}\n passed=result['validation_ok']\nelse:\n result={'stage':stage,'training_produced':case['training']['produced'],'resolved_consumed':sys.argv[3],\n 'dictionary_consumed':case[stage]['consumed'],'identity_matches':case['training']['produced']==sys.argv[3],\n 'args_match_dictionary':sys.argv[3]==case[stage]['consumed'],'validation_ok':case[stage]['validation_ok']}\n passed=result['identity_matches'] and result['args_match_dictionary'] and result['validation_ok']\nprint(json.dumps(result)); sys.exit(not passed)\n")
config = copy.deepcopy(supplied)
for i, step in enumerate(config['steps']):
    step['waitFor'] = ['-'] if i == 0 else [config['steps'][i-1]['id']]
    if 'learner.py' in step['args']:
        step['args'][1] = 'demonstration_entry.py'
    if step['args'][1] == 'demonstration_entry.py':
        step['args'] = ['python', 'demonstration_entry.py', '${_CASE}', step['id']]
        if step['id'] == 'model_validation':
            step['args'].append('${_CONSUMED}')

for event in load('triggers.json')['pubsub']['fixtures'][:2]:
    config['substitutions']['_CONSUMED'] = cases[event['case_id']]['model_validation']['consumed']
    config['substitutions']['_PRODUCED'] = cases[event['case_id']]['training']['produced']
    config['steps'][1]['args'][-1] = '${_PRODUCED}'

    with open('demonstration.yaml', 'w') as f:
        yaml.safe_dump(config, f)
    parsed = yaml.safe_load(Path('demonstration.yaml').read_text())
    run = run_build('demonstration.yaml', 'pubsub', event)
    for step in run['steps']:
        if step['output'].strip():
            step['computed_evidence'] = json.loads(step['output'])
        del step['output']
        if step['id'] == 'training' and step['status'] == 'SUCCESS':
            step['computed_evidence'] = {'produced_identity':load('downstream_invocation.json')['artifact_id']}
    print(json.dumps({'event':event, 'parsed_local_demonstration_config':parsed, 'computed_local_run':run}, indent=2))
