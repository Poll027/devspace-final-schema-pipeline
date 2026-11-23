trigger_branch = "main"
selected_case = 'accepted'
import os
from pathlib import Path
for path, content in support_files.items():
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    Path(path).write_text(content)
import numpy as np
import yaml
from prediction_package import FittedPackage, InputContractError
from support import read, inspect_config, trigger_run, fixture_events, status, assertion_failure, rejection
Path("gate_impl.py").write_text("def strict_behavior_tests(package, fixture, contract):\n    if 'expected_exception' in fixture:\n        try:\n            package.predict(fixture['inputs'])\n        except InputContractError:\n            return {'rejected_input':True}\n        raise AssertionError('expected InputContractError')\n    output = package.predict(fixture['inputs'])\n    assert len(output['sample_ids']) == len(fixture['inputs'])\n    assert output['sample_ids'] == fixture['expected_sample_ids']\n    assert list(output['values'].shape) == fixture['expected_shape']\n    expected = np.array(fixture['expected_values']).reshape(fixture['expected_shape'])\n    np.testing.assert_allclose(output['values'],expected,rtol=contract['rtol'],atol=contract['atol'])\n    return {'sample_ids':output['sample_ids'],'values':output['values'].tolist(),'shape':list(output['values'].shape)}\n\n\ndef reference_only_tests(package, fixture, contract):\n    if 'expected_exception' in fixture: return {'rejected_input':True}\n    return {'sample_ids':fixture['expected_sample_ids'],'values':fixture['expected_values'],'shape':fixture['expected_shape']}\n\n\ndef fatal_behavior(args):\n    case=execution[args[-1]]\n    return test_behavior(FittedPackage(case['regression']),cases[case['fixture_id']],contract)\n")
exec(Path("gate_impl.py").read_text())
test_behavior = strict_behavior_tests
cases=read('fixtures/behavior_cases.json')
contract=read('fixtures/behavior_contract.json')
execution=read('fixtures/behavior_execution_cases.json')
results={}
for name in cases:
    results[name]=test_behavior(FittedPackage(),cases[name],contract)
regressions={}
for regression in contract['regressions']:
    regressions[regression]=rejection(test_behavior,FittedPackage(regression),cases['valid'],contract)
    assert not regressions[regression]['accepted']
config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['behavior_tests']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
inspect_config(resolved)
runs=[]
for event in fixture_events('repository_commit'):
    runs.append(trigger_run(resolved,'repository_commit',event,{'behavior_tests':fatal_behavior}))
assert status(runs[0],'release_gate')=='SUCCESS'
assert status(runs[1],'behavior_tests')=='FAILURE'
assert status(runs[1],'release_gate')=='SKIPPED'
selected_run=trigger_run(resolved,'repository_commit',{'branch':trigger_branch,'snapshot_id':'valid','case_id':selected_case},{'behavior_tests':fatal_behavior})
report={'config':resolved,'results':results,'regressions':regressions,'runs':runs,'selected_run':selected_run,'false_assert_raises':assertion_failure()}
