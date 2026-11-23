trigger_event_type = "artifact_ready"
selected_case = 'A'
import os
from pathlib import Path
for path, content in support_files.items():
    os.makedirs(os.path.dirname(path) or ".",exist_ok=True)
    Path(path).write_text(content)
import yaml
from support import read, inspect_config, trigger_run, fixture_events, status, rejection, valid_count
Path("gate_impl.py").write_text("def expected_cost(evidence, contract):\n    for name in ['FP','TN','FN','TP']:\n        if name not in evidence or not valid_count(evidence[name]):\n            raise ValueError('invalid_count:'+name)\n    negative=evidence['FP']+evidence['TN']\n    positive=evidence['FN']+evidence['TP']\n    if negative <= 0 or positive <= 0:\n        raise ValueError('undefined_actual_class_rate')\n    return contract['probabilities']['P(Y=0)'] * evidence['FP']/negative * contract['costs']['cost_FP'] + contract['probabilities']['P(Y=1)'] * evidence['FN']/positive * contract['costs']['cost_FN']\n\n\ndef complete_acceptance(candidate, reference, contract, event_id):\n    for name in ['candidate_id','evidence_complete','latency_ms','operating_ok','FP','TN','FN','TP']:\n        if name not in candidate: raise ValueError('missing:'+name)\n    checks={'complete':candidate['evidence_complete'],'identity':candidate['candidate_id']==event_id,\n            'latency_present':candidate['latency_ms'] is not None,'operating':candidate['operating_ok']}\n    for name in checks:\n        if not checks[name]: raise ValueError(name)\n    cost=expected_cost(candidate,contract)\n    checks['cost_maximum']=cost <= contract['max_expected_error_cost']\n    checks['reference_cost']=cost <= expected_cost(reference,contract)\n    checks['latency']=candidate['latency_ms'] <= contract['max_latency_ms']\n    for name in checks:\n        if not checks[name]: raise ValueError(name)\n    return {'candidate_id':candidate['candidate_id'],'expected_error_cost':cost,'checks':checks}\n\n\ndef cost_only_acceptance(candidate, reference, contract, event_id):\n    cost=expected_cost(candidate,contract)\n    return {'candidate_id':candidate['candidate_id'],'expected_error_cost':cost,'checks':{'cost_maximum':cost <= contract['max_expected_error_cost']}}\n\n\ndef fatal_acceptance(args):\n    return acceptance(cases[args[-1]],cases[contract['accepted_reference']],contract,args[-1])\n")
exec(Path("gate_impl.py").read_text())
acceptance = complete_acceptance
cases=read('fixtures/release_cases.json')
contract=read('fixtures/release_contract.json')
results={}
for name in cases:
    results[name]=rejection(acceptance,cases[name],cases[contract['accepted_reference']],contract,cases[name]['candidate_id'])
assert results['A']['accepted']
assert results['boundary']['accepted']
assert not results['B']['accepted']
assert not results['empty_negatives']['accepted']
assert not results['empty_positives']['accepted']
assert not results['incomplete']['accepted']
config=read('cloudbuild.yaml')
config['steps'][1]['waitFor']=['release_gate']
with open('resolved.yaml','w') as file_handle:
    yaml.safe_dump(config,file_handle)
with open('resolved.yaml') as file_handle:
    resolved=yaml.safe_load(file_handle)
inspect_config(resolved)
runs=[]
for event in fixture_events('pubsub'):
    runs.append(trigger_run(resolved,'pubsub',event,{'release_gate':fatal_acceptance}))
assert status(runs[0],'promotion')=='SUCCESS'
assert status(runs[1],'release_gate')=='FAILURE'
assert status(runs[1],'promotion')=='SKIPPED'
event={'event_type':trigger_event_type,'case_id':selected_case,'artifact_id':selected_case}
selected_run=trigger_run(resolved,'pubsub',event,{'release_gate':fatal_acceptance})
report={'config':resolved,'results':results,'runs':runs,'selected_run':selected_run}
