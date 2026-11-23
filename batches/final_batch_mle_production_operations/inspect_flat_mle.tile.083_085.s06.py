def coverage_calculation(matched, cohort):
    return len(matched) / len(cohort)


def loss_mean(losses):
    return None

def loss_std(losses):
    return None

import numpy as np

def quality(prediction_rows, label_rows):
    cohort = {}
    rejected = []
    seen_prediction_ids = {}
    seen = {}
    for row in prediction_rows:
        key = row['prediction_id']
        if key in seen_prediction_ids:
            return {'status': 'duplicate_prediction'}
        seen_prediction_ids[key] = row
    for row in label_rows:
        key = row['prediction_id']
        if key in seen:
            return {'status': 'duplicate_label'}
        seen[key] = row
    for row in prediction_rows:
        key = row['prediction_id']
        if row['eligible'] and row['cohort_id'] == policy['cohort']:
            cohort[key] = row
    matched = {}
    losses = []
    errors = []
    for row in label_rows:
        key = row['prediction_id']
        if key in cohort and cohort[key]['prediction_timestamp'] <= cutoff and (row['label_timestamp'] <= policy['label_available_through']):
            matched[key] = row
            losses.append(row['loss'])
            errors.append(cohort[key]['prediction'] != row['label'])
        else:
            rejected.append(key)
    if len(matched) == 0:
        return {'status': 'unavailable', 'cohort': cohort, 'matched': matched, 'eligible_ids': len(cohort), 'mature_ids': len(matched), 'coverage': coverage_calculation(matched, cohort) if len(cohort) > 0 else None, 'errors': None, 'error_proportion': None, 'loss_mean': None, 'loss_std': None, 'excluded_label_ids': rejected}
    return {'status': 'mature_cohort_only', 'cohort': cohort, 'matched': matched, 'eligible_ids': len(cohort), 'mature_ids': len(matched), 'coverage': coverage_calculation(matched, cohort), 'errors': sum(errors), 'error_proportion': sum(errors) / len(matched), 'loss_mean': loss_mean(losses), 'loss_std': loss_std(losses), 'excluded_label_ids': rejected}


import csv, json

import numpy as np

policy = json.loads('{"cohort": "fixed_100", "analysis_time": "2026-01-04T00:00:00Z", "minimum_age_hours": 24, "label_available_through": "2026-01-04T00:00:00Z", "duplicate_policy": "reject repeated prediction or label ID before dictionary construction", "unmatched_policy": "exclude and record", "outside_cohort_policy": "exclude and record", "ddof": 0}')

predictions_rows = list(csv.DictReader(open('predictions.csv')))

predictions = {}

predictions['prediction_id'] = np.array([r['prediction_id'] for r in predictions_rows])

predictions['prediction_timestamp'] = np.array([r['prediction_timestamp'] for r in predictions_rows])

predictions['prediction'] = np.array([r['prediction'] for r in predictions_rows])

predictions['cohort_id'] = np.array([r['cohort_id'] for r in predictions_rows])

predictions['eligible'] = np.array([r['eligible'] == 'True' for r in predictions_rows])

labels_rows = list(csv.DictReader(open('labels.csv')))

labels = {}

labels['prediction_id'] = np.array([r['prediction_id'] for r in labels_rows])

labels['label_timestamp'] = np.array([r['label_timestamp'] for r in labels_rows])

labels['label'] = np.array([r['label'] for r in labels_rows])

labels['loss'] = np.array([float(r['loss'] or 'nan') for r in labels_rows])

from datetime import datetime, timedelta

def typed_rows(columns):
    return [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in columns.items()} for i in range(len(next(iter(columns.values()))))]

prediction_rows = typed_rows(predictions)

label_rows = typed_rows(labels)

cutoff = (datetime.fromisoformat(policy['analysis_time'].replace('Z', '+00:00')) - timedelta(hours=policy['minimum_age_hours'])).isoformat().replace('+00:00', 'Z')

result = quality(prediction_rows, label_rows)

outside_prediction = dict(prediction_rows[0], eligible=False)

outside_duplicate_rows = [outside_prediction, dict(outside_prediction)]