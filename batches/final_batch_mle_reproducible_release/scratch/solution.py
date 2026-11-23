# Supplied infrastructure (leave unchanged): prepares the frozen artifacts, aligned Boolean masks and matched-report function.
# Executed scaffolding is embedded because the pinned stage runner mounts only the entry file.
supplied_support = '''
import csv
from pathlib import Path

class FittedPreprocessor:
    def __init__(self, mean):
        self.mean_ = mean
    def transform(self, inputs):
        return [[float(row[0]) - self.mean_] for row in inputs]

class FittedModel:
    def __init__(self, boundary):
        self.boundary_ = boundary
    def predict(self, transformed):
        return [int(row[0] >= self.boundary_) for row in transformed]

_FROZEN = {'B': (FittedPreprocessor(42.5), FittedModel(-2.5)), 'baseline': (FittedPreprocessor(42.5), FittedModel(17.5))}

def read_orders(path):
    with open(path, newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    return rows

def supplied_workflow(dataset_path='training_orders.csv', threshold=40.0):
    rows = read_orders(dataset_path)
    inputs = [[float(row['order_amount'])] for row in rows]
    mean = sum(row[0] for row in inputs)/len(inputs)
    preprocessor = FittedPreprocessor(mean)
    model = FittedModel(threshold - mean)
    predictions = model.predict(preprocessor.transform(inputs))
    accuracy = sum(p == int(row['late']) for p,row in zip(predictions,rows))/len(rows)
    return {'model': model, 'preprocessor': preprocessor, 'validation_accuracy': accuracy,
            'resolved_parameters': {'dataset_path': dataset_path, 'threshold': threshold}}

def frozen_prediction_helper(rows, identity):
    if identity not in ('B', 'baseline'):
        raise ValueError('Only the supplied frozen identities are authorized')
    preprocessor, model = _FROZEN[identity]
    return model.predict(preprocessor.transform([[float(r['order_amount'])] for r in rows]))

def protected_data_access(variant='base'):
    rows = read_orders('protected_orders.csv')
    if variant == 'no_negatives': rows = [r for r in rows if int(r['late']) != 0]
    elif variant == 'no_positives': rows = [r for r in rows if int(r['late']) != 1]
    elif variant != 'base': raise ValueError(variant)
    return rows

# Infrastructure scaffolding; leave unchanged. Imports and evaluation bodies below are yours.
policy = {'selected_candidate': 'B', 'preprocessing_identity': 'B.fitted.order_amount.center', 'threshold': 40.0, 'baseline_threshold': 60.0, 'deployment_probabilities': {'0': 0.7, '1': 0.3}, 'error_costs': {'FP': 2.0, 'FN': 5.0}, 'requirements': {'max_expected_error_cost': 0.5, 'max_FPR': 0.25, 'max_FNR': 0.4}, 'correct_prediction_cost': 0.0}

def supplied_arrays(variant):
    import numpy as np
    rows = protected_data_access(variant)
    return np.array([int(row["late"]) for row in rows]), np.array(frozen_prediction_helper(rows, "B")), np.array(frozen_prediction_helper(rows, "baseline"))

import numpy as np
def score_counts(TN, FP, FN, TP, policy):
    negatives = FP + TN
    positives = FN + TP
    if negatives == 0:
        FPR = None
    else:
        FPR = FP / negatives
    if positives == 0:
        FNR = None
    else:
        FNR = FN / positives
    if (negatives == 0) & (positives == 0):
        expected_error_cost = None
    else:
        if negatives == 0:
            expected_error_cost = None
        else:
            if positives == 0:
                expected_error_cost = None
            else:
                expected_error_cost = policy["deployment_probabilities"]["0"] * FPR * policy["error_costs"]["FP"] + policy["deployment_probabilities"]["1"] * FNR * policy["error_costs"]["FN"]
    if expected_error_cost == None:
        FPR_requirement = None
        FNR_requirement = None
        cost_requirement = None
        requirement_outcome = "undefined"
        if negatives != 0:
            FPR_requirement = FPR <= policy["requirements"]["max_FPR"]
        if positives != 0:
            FNR_requirement = FNR <= policy["requirements"]["max_FNR"]
    else:
        FPR_requirement = FPR <= policy["requirements"]["max_FPR"]
        FNR_requirement = FNR <= policy["requirements"]["max_FNR"]
        cost_requirement = expected_error_cost <= policy["requirements"]["max_expected_error_cost"]
        if FPR_requirement & FNR_requirement & cost_requirement:
            requirement_outcome = "pass"
        else:
            requirement_outcome = "fail"
    return {"TN": TN, "FP": FP, "FN": FN, "TP": TP, "actual_negatives": negatives, "actual_positives": positives, "FPR": FPR, "FNR": FNR, "expected_error_cost": expected_error_cost, "FPR_requirement": FPR_requirement, "FNR_requirement": FNR_requirement, "cost_requirement": cost_requirement, "requirement_outcome": requirement_outcome}



_masks = {}
for _variant in ['base', 'no_negatives', 'no_positives']:
    _y, _bp, _baselinep = supplied_arrays(_variant)
    for _identity, _prediction in [("B", _bp), ("baseline", _baselinep)]:
        _m = {"TN": (_y == 0) & (_prediction == 0), "FP": (_y == 0) & (_prediction == 1), "FN": (_y == 1) & (_prediction == 0), "TP": (_y == 1) & (_prediction == 1)}
        for _name, _mask in _m.items():
            globals()["mask_"+_variant+"_"+_identity+"_"+_name] = _mask

def finish(counts):
    comparison = {}
    for variant in ['base', 'no_negatives', 'no_positives']:
        comparison[variant] = {"selected_candidate": policy["selected_candidate"], "threshold": policy["threshold"], "baseline_threshold": policy["baseline_threshold"], "preprocessing_identity": policy["preprocessing_identity"]}
        for identity in ["B", "baseline"]:
            c = counts[variant][identity]
            comparison[variant][identity] = score_counts(c["TN"], c["FP"], c["FN"], c["TP"], policy)
    return comparison
'''
exec(supplied_support)
import numpy as np
count_base_B_TN = np.sum(mask_base_B_TN)
count_base_B_FP = np.sum(mask_base_B_FP)
count_base_B_FN = np.sum(mask_base_B_FN)
count_base_B_TP = np.sum(mask_base_B_TP)
count_base_baseline_TN = np.sum(mask_base_baseline_TN)
count_base_baseline_FP = np.sum(mask_base_baseline_FP)
count_base_baseline_FN = np.sum(mask_base_baseline_FN)
count_base_baseline_TP = np.sum(mask_base_baseline_TP)
count_no_negatives_B_TN = np.sum(mask_no_negatives_B_TN)
count_no_negatives_B_FP = np.sum(mask_no_negatives_B_FP)
count_no_negatives_B_FN = np.sum(mask_no_negatives_B_FN)
count_no_negatives_B_TP = np.sum(mask_no_negatives_B_TP)
count_no_negatives_baseline_TN = np.sum(mask_no_negatives_baseline_TN)
count_no_negatives_baseline_FP = np.sum(mask_no_negatives_baseline_FP)
count_no_negatives_baseline_FN = np.sum(mask_no_negatives_baseline_FN)
count_no_negatives_baseline_TP = np.sum(mask_no_negatives_baseline_TP)
count_no_positives_B_TN = np.sum(mask_no_positives_B_TN)
count_no_positives_B_FP = np.sum(mask_no_positives_B_FP)
count_no_positives_B_FN = np.sum(mask_no_positives_B_FN)
count_no_positives_B_TP = np.sum(mask_no_positives_B_TP)
count_no_positives_baseline_TN = np.sum(mask_no_positives_baseline_TN)
count_no_positives_baseline_FP = np.sum(mask_no_positives_baseline_FP)
count_no_positives_baseline_FN = np.sum(mask_no_positives_baseline_FN)
count_no_positives_baseline_TP = np.sum(mask_no_positives_baseline_TP)

# Supplied infrastructure: form the matched report from your counts.
counts = {'base': {'B': {'TN': count_base_B_TN, 'FP': count_base_B_FP, 'FN': count_base_B_FN, 'TP': count_base_B_TP}, 'baseline': {'TN': count_base_baseline_TN, 'FP': count_base_baseline_FP, 'FN': count_base_baseline_FN, 'TP': count_base_baseline_TP}}, 'no_negatives': {'B': {'TN': count_no_negatives_B_TN, 'FP': count_no_negatives_B_FP, 'FN': count_no_negatives_B_FN, 'TP': count_no_negatives_B_TP}, 'baseline': {'TN': count_no_negatives_baseline_TN, 'FP': count_no_negatives_baseline_FP, 'FN': count_no_negatives_baseline_FN, 'TP': count_no_negatives_baseline_TP}}, 'no_positives': {'B': {'TN': count_no_positives_B_TN, 'FP': count_no_positives_B_FP, 'FN': count_no_positives_B_FN, 'TP': count_no_positives_B_TP}, 'baseline': {'TN': count_no_positives_baseline_TN, 'FP': count_no_positives_baseline_FP, 'FN': count_no_positives_baseline_FN, 'TP': count_no_positives_baseline_TP}}}
comparison = finish(counts)
