import yaml
import math
from support import read, inspect_config, trigger_run, fixture_events, status, assertion_failure
def contract_checks(snapshot):
    rows = snapshot['rows']
    required = read('fixtures/dataset_contract.json')['columns']
    schema = all(set(row) == set(required) for row in rows)
    values = all(isinstance(row.get('feature'), (int,float)) and not isinstance(row.get('feature'), bool) and math.isfinite(row['feature']) and 0 <= row['feature'] <= 5 for row in rows)
    labels = all(type(row.get('label')) is int and row['label'] in [0,1] for row in rows)
    ids = [row.get('sample_id') for row in rows]
    unique = all(isinstance(x,str) and x for x in ids) and len(ids) == len(set(ids))
    return {'schema':schema,'feature_values':values,'label_values':labels,'unique_sample_id':unique}
def dataset_gate(snapshot, required):
    checks = contract_checks(snapshot)
    failed = []
    for name in required:
        if name not in checks or not checks[name]:
            failed.append(name)
    evidence = {'snapshot_id':snapshot['snapshot_id'],'sha256':snapshot['sha256'],'checks':checks,'failed_checks':failed,'accepted':not failed}
    return evidence
def fatal_dataset(args):
    snapshot = cases[args[-1]]
    result = dataset_gate(snapshot, contract['required_checks'])
    retained[result['snapshot_id']] = result
    if not result['accepted']:
        raise AssertionError(result['failed_checks'])
    return result
