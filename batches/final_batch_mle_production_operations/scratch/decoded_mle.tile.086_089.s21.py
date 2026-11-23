import csv, json

import numpy as np

policy = json.loads('{"P_Y0": 0.5, "P_Y1": 0.5, "cost_FP": 1, "cost_FN": 2, "acceptance": {"maximum_FPR": 0.1, "maximum_FNR": 0.1, "cost_not_above_incumbent": true, "slice_pass_required": true, "compatibility_pass_required": true}, "empty_group": "undefined; reject", "cohort": "cohort.validation", "decision_record_fields": ["registry_artifact_id", "cohort_id", "FPR", "FNR", "expected_cost", "quality_pass", "slice_pass", "compatibility_pass", "verdict"], "protected_test": "not provided; never used for selection"}')

validation_counts_rows = list(csv.DictReader(open('validation_counts.csv')))

validation_counts = {}

validation_counts['fixture'] = np.array([r['fixture'] for r in validation_counts_rows])

validation_counts['model_role'] = np.array([r['model_role'] for r in validation_counts_rows])

validation_counts['cohort_id'] = np.array([r['cohort_id'] for r in validation_counts_rows])

validation_counts['registry_artifact_id'] = np.array([r['registry_artifact_id'] for r in validation_counts_rows])

validation_counts['FP'] = np.array([float(r['FP'] or 'nan') for r in validation_counts_rows])

validation_counts['TN'] = np.array([float(r['TN'] or 'nan') for r in validation_counts_rows])

validation_counts['FN'] = np.array([float(r['FN'] or 'nan') for r in validation_counts_rows])

validation_counts['TP'] = np.array([float(r['TP'] or 'nan') for r in validation_counts_rows])

validation_counts['slice_pass'] = np.array([r['slice_pass'] == 'True' for r in validation_counts_rows])

validation_counts['compatibility_pass'] = np.array([r['compatibility_pass'] == 'True' for r in validation_counts_rows])

fixtures = {}

for i in range(len(validation_counts_rows)):
    r = {k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in validation_counts.items()}
    fixtures.setdefault(r['fixture'], {})[r['model_role']] = r

def test_all(evaluate):
    out = []
    for name, pair in fixtures.items():
        c = pair['candidate']
        inc = pair['incumbent']
        out.append({'fixture': name, 'record': evaluate(inc, c, c['registry_artifact_id'])})
    pair = fixtures['valid']
    out.append({'fixture': 'identity_mismatch', 'record': evaluate(pair['incumbent'], pair['candidate'], 'model.unrelated')})
    return out

def assert_failures(check_failure):
    for name, pair in fixtures.items():
        if name not in ['valid', 'boundary']:
            check_failure(pair)

def negative_class_error_rate(model):
    return model['FP'] / (model['FP'] + model['TN'])

def positive_class_error_rate(model):
    return model['FN'] / (model['FN'] + model['TP'])

def prevalence_weighted_error_cost(fpr, fnr):
    return policy['P_Y0'] * fpr * policy['cost_FP'] + policy['P_Y1'] * fnr * policy['cost_FN']

def declared_quality_limits(cand, inc):
    return cand['FPR'] <= policy['acceptance']['maximum_FPR'] and cand['FNR'] <= policy['acceptance']['maximum_FNR'] and (cand['cost'] <= inc['cost'])

def all_required_gates(quality, candidate, incumbent, requested_identity):
    return quality and candidate['slice_pass'] and candidate['compatibility_pass'] and (candidate['cohort_id'] == incumbent['cohort_id']) and (candidate['cohort_id'] == policy['cohort']) and (candidate['registry_artifact_id'] == requested_identity)

unavailable_rule = None

fpr_rule = negative_class_error_rate

fnr_rule = positive_class_error_rate

cost_rule = prevalence_weighted_error_cost

quality_rule = declared_quality_limits

passed_rule = all_required_gates

def rates(model):
    if model['FP'] + model['TN'] == 0 or model['FN'] + model['TP'] == 0:
        return {'FPR': None, 'FNR': None, 'cost': None}
    fpr = fpr_rule(model)
    fnr = fnr_rule(model)
    cost = cost_rule(fpr, fnr)
    return {'FPR': fpr, 'FNR': fnr, 'cost': cost}

def evaluate(incumbent, candidate, requested_identity):
    inc = rates(incumbent)
    cand = rates(candidate)
    quality = False
    if cand['cost'] != None and inc['cost'] != None:
        quality = quality_rule(cand, inc)
    passed = passed_rule(quality, candidate, incumbent, requested_identity)
    return {'registry_artifact_id': candidate['registry_artifact_id'], 'cohort_id': candidate['cohort_id'], 'FPR': cand['FPR'], 'FNR': cand['FNR'], 'expected_cost': cand['cost'], 'incumbent_rates': inc, 'quality_pass': quality, 'slice_pass': candidate['slice_pass'], 'compatibility_pass': candidate['compatibility_pass'], 'verdict': passed}

assert evaluate(fixtures['valid']['incumbent'], fixtures['valid']['candidate'], fixtures['valid']['candidate']['registry_artifact_id'])['verdict']

assert evaluate(fixtures['boundary']['incumbent'], fixtures['boundary']['candidate'], fixtures['boundary']['candidate']['registry_artifact_id'])['verdict']

assert not evaluate(fixtures['valid']['incumbent'], fixtures['valid']['candidate'], 'model.unrelated')['verdict']

def check_failure(pair):
    assert not evaluate(pair['incumbent'], pair['candidate'], pair['candidate']['registry_artifact_id'])['verdict']

assert_failures(check_failure)

result = test_all(evaluate)