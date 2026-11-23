# Supplied practice implementation. Read-only scaffolding.
def dataset_gate(snapshot, required):
    checks = contract_checks(snapshot)
    failed = []
    for name in required:
        if name not in checks or not checks[name]:
            failed.append(name)
    evidence = {'snapshot_id': snapshot['snapshot_id'], 'sha256': snapshot['sha256'], 'checks': checks, 'failed_checks': failed, 'accepted': not failed}
    return evidence

def fatal_dataset(args):
    snapshot = cases[args[-1]]
    result = dataset_gate(snapshot, contract['required_checks'])
    retained[result['snapshot_id']] = result
    if not result['accepted']:
        raise AssertionError(result['failed_checks'])
    return result
