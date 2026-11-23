import yaml
from support import read, inspect_config, trigger_run, fixture_events, status, rejection, valid_count
def expected_cost(evidence, contract):
    for name in ['FP','TN','FN','TP']:
        if name not in evidence or not valid_count(evidence[name]):
            raise ValueError('invalid_count:'+name)
    negative=evidence['FP']+evidence['TN']
    positive=evidence['FN']+evidence['TP']
    if negative <= 0 or positive <= 0:
        raise ValueError('undefined_actual_class_rate')
    fpr=evidence['FP']/negative
    fnr=evidence['FN']/positive
    return contract['probabilities']['P(Y=0)'] * evidence['FP']/negative * contract['costs']['cost_FP'] + contract['probabilities']['P(Y=1)'] * evidence['FN']/positive * contract['costs']['cost_FN']
def acceptance(candidate, reference, contract, event_id):
    for name in ['candidate_id','evidence_complete','latency_ms','operating_ok','FP','TN','FN','TP']:
        if name not in candidate: raise ValueError('missing:'+name)
    checks={'complete':candidate['evidence_complete'] is True,'identity':candidate['candidate_id']==event_id,
            'latency_present':candidate['latency_ms'] is not None,'operating':candidate['operating_ok'] is True}
    for name in checks:
        if not checks[name]: raise ValueError(name)
    cost=expected_cost(candidate,contract)
    checks['cost_maximum']=cost <= contract['max_expected_error_cost']
    checks['reference_cost']=cost <= expected_cost(reference,contract)
    checks['latency']=candidate['latency_ms'] <= contract['max_latency_ms']
    for name in checks:
        if not checks[name]: raise ValueError(name)
    return {'candidate_id':candidate['candidate_id'],'expected_error_cost':cost,'checks':checks}
def fatal_acceptance(args):
    return acceptance(cases[args[-2]],cases[contract['accepted_reference']],contract,args[-1])
