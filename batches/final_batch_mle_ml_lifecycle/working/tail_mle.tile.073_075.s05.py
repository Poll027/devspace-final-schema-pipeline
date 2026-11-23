trigger_branch = "main"
selected_case = 'valid'
import os
from pathlib import Path
for path, content in support_files.items():
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    Path(path).write_text(content)
import yaml
from support import read, named_dataset_checks, inspect_config, trigger_run, fixture_events, status, assertion_failure
Path("gate_impl.py").write_text("def strict_dataset_gate(snapshot, required):\n    checks = named_dataset_checks(snapshot)\n    failed = []\n    for name in required:\n        if name not in checks or not checks[name]:\n            failed.append(name)\n    evidence = {'snapshot_id':snapshot['snapshot_id'],'sha256':snapshot['sha256'],'checks':checks,'failed_checks':failed,'accepted':not failed}\n    return evidence\n\n\ndef warning_dataset_gate(snapshot, required):\n    checks = named_dataset_checks(snapshot)\n    return {'snapshot_id':snapshot['snapshot_id'],'sha256':snapshot['sha256'],'checks':checks,'failed_checks':[],'accepted':True}\n\n\ndef fatal_dataset(args):\n    snapshot = cases[args[-1]]\n    result = dataset_gate(snapshot, contract['required_checks'])\n    retained[result['snapshot_id']] = result\n    if not result['accepted']:\n        raise AssertionError(result['failed_checks'])\n    return result\n")
exec(Path("gate_impl.py").read_text())
dataset_gate = strict_dataset_gate
cases = read('fixtures/dataset_cases.json')
contract = read('fixtures/dataset_contract.json')
retained = {}
results = {}
for name in cases:
    results[name] = dataset_gate(cases[name],contract['required_checks'])
assert results['valid']['accepted']
assert results['boundary']['accepted']
assert not results['missing_required_feature']['accepted']
assert 'schema' in results['missing_required_feature']['failed_checks']
config = read('cloudbuild.yaml')
config['steps'][1]['waitFor'] = ['quality']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved = yaml.safe_load(file_handle)
inspect_config(resolved)
runs = []
for event in fixture_events('repository_commit'):
    runs.append(trigger_run(resolved,'repository_commit',event,{'quality':fatal_dataset}))
assert status(runs[0],'training') == 'SUCCESS'
assert status(runs[1],'quality') == 'FAILURE'
assert status(runs[1],'training') == 'SKIPPED'
event = {'branch':trigger_branch,'snapshot_id':selected_case}
selected_run = trigger_run(resolved,'repository_commit',event,{'quality':fatal_dataset})
report = {'config':resolved,'results':results,'retained':retained,'runs':runs,'selected_run':selected_run,'false_assert_raises':assertion_failure()}
