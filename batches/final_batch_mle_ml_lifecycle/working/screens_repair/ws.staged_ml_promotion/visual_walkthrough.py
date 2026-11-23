import json, copy, yaml
from pathlib import Path
from runtime_sim import run_build
load = lambda p: json.loads(Path(p).read_text())
cases = load('fixtures/promotion_cases.json')
supplied = yaml.safe_load(Path('cloudbuild.yaml').read_text())
print(json.dumps({'supplied_fixtures':cases, 'parsed_supplied_cloudbuild_yaml':supplied}, indent=2))
# Author a demonstration entry point in an isolated copy; the supplied learner.py remains unwritten.
Path('demonstration_entry.py').write_text("import json, sys, math, hashlib\nfrom pathlib import Path\nload = lambda p: json.loads(Path(p).read_text())\n\nc=load('fixtures/promotion_cases.json')[sys.argv[1]]; stage=sys.argv[2]; r=load('fixtures/registry.json')[c['registry_version']]\nidentity=(c['artifact_id']==r['artifact_id']==c['staged_artifact_id']==c['approval']['artifact_id'] and c['run_id']==r['run_id'] and c['registry_version']==c['approval']['registry_version'])\nchecks={'compatibility':c['compatibility_ok'], 'offline_validation':c['offline_validation_ok'],\n 'staged_validation':c['staged_validation_ok'] and identity,\n 'authorization':c['approval']['authorized'] and identity and bool(c['approval']['accountable_identity'])}\npassed={'compatibility':checks['compatibility'], 'staging_quality':checks['offline_validation'] and checks['staged_validation'], 'authorization':checks['authorization']}[stage]\nprint(json.dumps({'stage':stage,'passed':passed,'immutable_artifact_reference':r,\n 'promotion_record':{**{k:c[k] for k in ('approval','registry_version','run_id','artifact_id')},'accountable_identity':c['approval']['accountable_identity'],'per_stage_results':checks}}))\nsys.exit(not passed)\n")
config = copy.deepcopy(supplied)
for i, step in enumerate(config['steps']):
    step['waitFor'] = ['-'] if i == 0 else [config['steps'][i-1]['id']]
    if 'learner.py' in step['args']:
        step['args'][1] = 'demonstration_entry.py'
    if step['args'][1] == 'demonstration_entry.py':
        step['args'].append(step['id'])

def recursive_keys(x):
    if isinstance(x, dict):
        for k, v in x.items():
            yield k
            yield from recursive_keys(v)
    elif isinstance(x, list):
        for v in x:
            yield from recursive_keys(v)

for event in load('triggers.json')['pubsub']['fixtures'][:2]:
    with open('demonstration.yaml', 'w') as f:
        yaml.safe_dump(config, f)
    parsed = yaml.safe_load(Path('demonstration.yaml').read_text())
    run = run_build('demonstration.yaml', 'pubsub', event)
    for step in run['steps']:
        if step['output'].strip():
            step['computed_evidence'] = json.loads(step['output'])
        del step['output']
    run['secret_reference_and_scope'] = {'references':config['availableSecrets']['secretManager'], 'step_scopes':{s['id']:s.get('secretEnv',[]) for s in config['steps']}}
    # The bounded adapter supplies no credentials; inspect emitted field names, never credential values.
    run['non_disclosure_check'] = {'adapter_supplies_credentials':False, 'credential_fields_in_emitted_records':any(k.lower() in ('promotion_token','credential','secret_value') for k in recursive_keys(run))}

    print(json.dumps({'event':event, 'parsed_local_demonstration_config':parsed, 'computed_local_run':run}, indent=2))
