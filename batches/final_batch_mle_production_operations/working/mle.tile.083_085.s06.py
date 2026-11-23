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
    pt=datetime.datetime.fromisoformat(pred['prediction_timestamp'].replace('Z','+00:00'))
    lt=datetime.datetime.fromisoformat(label['label_timestamp'].replace('Z','+00:00'))
    return lt<=cutoff and (cutoff-pt).total_seconds()>=policy['minimum_age_hours']*3600


policy = {'cohort': 'fixed_100', 'analysis_time': '2026-01-04T00:00:00Z', 'minimum_age_hours': 24, 'label_available_through': '2026-01-04T00:00:00Z', 'duplicate_policy': 'reject repeated prediction or label ID before dictionary construction', 'unmatched_policy': 'exclude and record', 'outside_cohort_policy': 'exclude and record', 'ddof': 0}
def calculate_contract(predictions_input,labels_input,mean_function,spread_function):
    supplied_rows = {'predictions':predictions_input,'labels':labels_input}
    def load(name):
        return supplied_rows[name]
    policy = {'cohort': 'fixed_100', 'analysis_time': '2026-01-04T00:00:00Z', 'minimum_age_hours': 24, 'label_available_through': '2026-01-04T00:00:00Z', 'duplicate_policy': 'reject repeated prediction or label ID before dictionary construction', 'unmatched_policy': 'exclude and record', 'outside_cohort_policy': 'exclude and record', 'ddof': 0}
    predictions = load('predictions')
    labels = load('labels')
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
            eligible.append({'prediction_id':pred['prediction_id'],'prediction_timestamp':pred['prediction_timestamp']})
    
    for label in labels:
        if label['prediction_id'] not in pred_by_id:
            unmatched.append(label['prediction_id'])
        else:
            pred = pred_by_id[label['prediction_id']]
            if pred['eligible'] and pred['cohort_id']==policy['cohort'] and mature(pred,label,policy):
                matched.append(pred['prediction_id'])
                losses.append(label['loss'])
                errors.append(pred['prediction'] != label['label'])
            else:
                excluded.append(label['prediction_id'])
    
    coverage = len(matched) / len(eligible)
    
    error_count = sum(errors)
    
    error_proportion = error_count / len(matched)
    
    mean_loss = mean_function(losses)
    
    std_loss = spread_function(losses, ddof=0)
    
    result = {'cohort':policy,'eligible_predictions':eligible,'mature_matched_ids':matched,'unmatched_labels':unmatched,'excluded_labels':excluded,'maturity_coverage':coverage,'error_count':error_count,'error_proportion':error_proportion,'mean_loss':mean_loss,'std_loss':std_loss,'scope':'mature matched cohort only; all traffic quality unestablished'}
    
    report = result
    return report

# OUTER

predictions_rows = load('predictions')
labels_rows = load('labels')
predictions_input = predictions_rows
labels_input = labels_rows
mean_function = np.mean
spread_function = np.std
report = calculate_contract(predictions_input,labels_input,mean_function,spread_function)
