import csv, json, datetime
import numpy as np
SCHEMAS = {'predictions': {'prediction_id': 'string', 'prediction_timestamp': 'datetime', 'prediction': 'string', 'cohort_id': 'string', 'eligible': 'boolean'}, 'labels': {'prediction_id': 'string', 'label_timestamp': 'datetime', 'label': 'string', 'loss': 'number'}}
def load(name):
    with open(name+'.csv') as f:
        data=list(csv.DictReader(f))
    for r in data:
        for k,t in SCHEMAS[name].items():
            v=r[k]
            r[k] = None if v=='' else (v=='True' if t=='boolean' else int(v) if t=='integer' else float(v) if t=='number' else v)
    return data
def column(data,key):
    return np.asarray([r[key] for r in data])
def emit(value):
    return value
def mature(pred,label,policy):
    cutoff=datetime.datetime.fromisoformat(policy['analysis_time'].replace('Z','+00:00'))
    available=datetime.datetime.fromisoformat(policy['label_available_through'].replace('Z','+00:00'))
    pt=datetime.datetime.fromisoformat(pred['prediction_timestamp'].replace('Z','+00:00'))
    lt=datetime.datetime.fromisoformat(label['label_timestamp'].replace('Z','+00:00'))
    return lt<=available and lt<=cutoff and (cutoff-pt).total_seconds()>=policy['minimum_age_hours']*3600
policy = {'cohort': 'fixed_100', 'analysis_time': '2026-01-04T00:00:00Z', 'minimum_age_hours': 24, 'label_available_through': '2026-01-04T00:00:00Z', 'duplicate_policy': 'reject repeated prediction or label ID before dictionary construction', 'unmatched_policy': 'exclude and record', 'outside_cohort_policy': 'exclude and record', 'ddof': 0}
def illustrative_cohort():
    predictions=[{'prediction_id':'illustrative.'+str(i),'prediction_timestamp':'2026-01-02T10:00:00Z','prediction':'on_time','cohort_id':policy['cohort'],'eligible':True} for i in range(illustrative_eligible_count)]
    labels=[{'prediction_id':'illustrative.'+str(i),'label_timestamp':'2026-01-03T10:00:00Z','label':'late' if i<6 else 'on_time','loss':1.0 if i<6 else 0.0} for i in range(illustrative_matched_count)]
    return predictions,labels


# Supplied orchestration; operations are selected by the learner.
def cohort_report(predictions, labels, policy):
    prediction_ids = []
    label_ids = []
    for pred in predictions:
        if pred['prediction_id'] in prediction_ids:
            raise ValueError('duplicate prediction ID')
        prediction_ids.append(pred['prediction_id'])
    for label in labels:
        if label['prediction_id'] in label_ids:
            raise ValueError('duplicate label ID')
        label_ids.append(label['prediction_id'])
    pred_by_id = {}
    for pred in predictions:
        if pred['prediction_id'] in pred_by_id:
            raise ValueError('duplicate prediction ID')
        pred_by_id[pred['prediction_id']] = pred
    label_by_id = {}
    for label in labels:
        if label['prediction_id'] in label_by_id:
            raise ValueError('duplicate label ID')
        label_by_id[label['prediction_id']] = label
    eligible = []
    matched = []
    losses = []
    errors = []
    unmatched = []
    excluded = []
    for pred in predictions:
        if pred['eligible'] and pred['cohort_id'] == policy['cohort']:
            eligible.append({'prediction_id': pred['prediction_id'], 'prediction_timestamp': pred['prediction_timestamp']})
    for label in labels:
        if label['prediction_id'] not in pred_by_id:
            unmatched.append(label['prediction_id'])
        else:
            pred = pred_by_id[label['prediction_id']]
            if pred['eligible'] and pred['cohort_id'] == policy['cohort'] and mature(pred, label, policy):
                matched.append(pred['prediction_id'])
                losses.append(label['loss'])
                errors.append(pred['prediction'] != label['label'])
            else:
                excluded.append(label['prediction_id'])
    coverage = None
    if len(eligible) > 0:
        coverage = len(matched) / len(eligible)
    error_count = sum(errors)
    error_proportion = None
    if len(matched) > 0:
        error_proportion = error_count / len(matched)
    mean_loss = mean_operation(losses)
    std_loss = std_operation(losses, ddof=0)
    result = {'cohort': policy, 'eligible_predictions': eligible, 'mature_matched_ids': matched, 'unmatched_labels': unmatched, 'excluded_labels': excluded, 'maturity_coverage': coverage, 'error_count': error_count, 'error_proportion': error_proportion, 'mean_loss': mean_loss, 'std_loss': std_loss, 'scope': 'mature matched cohort only; all traffic quality unestablished'}
    return result

#TAIL

mean_operation = np.mean
std_operation = np.std
illustrative_eligible_count = 100
illustrative_matched_count = 60
report = cohort_report(load('predictions'), load('labels'), policy)
illustrative_predictions, illustrative_labels = illustrative_cohort()
illustrative_report = cohort_report(illustrative_predictions, illustrative_labels, policy)
