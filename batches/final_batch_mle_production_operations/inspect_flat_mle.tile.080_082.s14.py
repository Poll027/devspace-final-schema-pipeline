import csv, json

import numpy as np

policy = json.loads('{"reference_id": "reference", "current_id": "production", "comparison_window": "2026-01-02T10:00:00Z/2026-01-02T11:00:00Z", "fixed_edges": [0, 5, 10], "eligible_numeric_range": [0, 10], "declared_categories": ["short_distance", "long_distance", "not_reported"], "ddof": 0, "distance_equation": "0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions", "criterion": "distance > 0.20; equality is not a crossing", "numeric_rule": "Apply the same distance to aligned numerical-bin proportions; retain mean and ddof=0 standard deviation separately", "quality_claim": "unresolved without matched labels"}')

reference_rows = list(csv.DictReader(open('reference.csv')))

reference = {}

reference['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in reference_rows])

reference['category'] = np.array([r['category'] for r in reference_rows])

reference['predicted_class'] = np.array([r['predicted_class'] for r in reference_rows])

production_rows = list(csv.DictReader(open('production.csv')))

production = {}

production['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in production_rows])

production['category'] = np.array([r['category'] for r in production_rows])

production['predicted_class'] = np.array([r['predicted_class'] for r in production_rows])

def counts(data):
    v = data['numeric_values']
    v = v[(v >= 0) & (v <= 10)]
    return (np.histogram(v, bins=policy['fixed_edges'])[0], np.array([np.count_nonzero(data['category'] == c) for c in policy['declared_categories']]), np.count_nonzero(v == v), np.count_nonzero(data['category'] == data['category']))

ref_bins, ref_cats, ref_n, ref_cat_n = counts(reference)

cur_bins, cur_cats, cur_n, cur_cat_n = counts(production)

ref_values = reference['numeric_values']

cur_values = production['numeric_values']

ref_values = ref_values[(ref_values >= 0) & (ref_values <= 10)]

cur_values = cur_values[(cur_values >= 0) & (cur_values <= 10)]

ref_mean = None

cur_mean = None

ref_std = None

cur_std = None

reference_categories = ref_cats / ref_cat_n

current_categories = cur_cats / cur_cat_n

reference_bins = ref_bins / ref_n

current_bins = cur_bins / cur_n

category_distance = 0.5 * np.sum(np.abs(reference_categories - current_categories))

numeric_distance = 0.5 * np.sum(np.abs(reference_bins - current_bins))

category_drift = category_distance > 0.2

numeric_drift = numeric_distance > 0.2

result = {'reference_id': policy['reference_id'], 'current_id': policy['current_id'], 'window': policy['comparison_window'], 'edges': policy['fixed_edges'], 'categories': policy['declared_categories'], 'eligibility': policy['eligible_numeric_range'], 'criterion': policy['criterion'], 'quality_claim': policy['quality_claim'], 'reference_mean': ref_mean, 'current_mean': cur_mean, 'reference_std': ref_std, 'current_std': cur_std, 'reference_categories': reference_categories, 'current_categories': current_categories, 'reference_bins': reference_bins, 'current_bins': current_bins, 'category_distance': category_distance, 'numeric_distance': numeric_distance, 'category_drift': category_drift, 'numeric_drift': numeric_drift, 'reference_total': ref_n, 'current_total': cur_n}