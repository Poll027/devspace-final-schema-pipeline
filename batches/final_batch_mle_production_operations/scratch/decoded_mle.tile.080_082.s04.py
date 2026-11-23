def normalize_counts(counts, values):
    return counts / len(values)


import numpy as np

def summarize(reference, production, policy):
    fixed_edges = policy['fixed_edges']
    summaries = []
    for data in [reference, production]:
        values = data['numeric_values']
        values = values[(values >= policy['eligible_numeric_range'][0]) & (values <= policy['eligible_numeric_range'][1])]
        counts = np.histogram(values, bins=fixed_edges)[0]
        proportions = normalize_counts(counts, values)
        categories = {}
        for category in policy['declared_categories']:
            categories[category] = np.sum(data['category'] == category) / len(data['category'])
        classes = {}
        for predicted_class in policy['declared_classes']:
            classes[predicted_class] = np.sum(data['predicted_class'] == predicted_class) / len(data['predicted_class'])
        summaries = summaries + [{'eligible_total': len(values), 'category_total': len(data['category']), 'class_total': len(data['predicted_class']), 'bin_proportions': proportions, 'mean': mean_calculation(values), 'std': std_calculation(values, ddof=0), 'categories': categories, 'classes': classes}]
    record = {'reference_id': policy['reference_id'], 'window': policy['production_window'], 'fixed_edges': fixed_edges, 'category_definitions': policy['declared_categories'], 'class_definitions': policy['declared_classes'], 'ddof': policy['ddof'], 'reference': summaries[0], 'production': summaries[1]}
    emit(record)
    return record


def mean_calculation(values):
    return np.mean(values)

def std_calculation(values, ddof):
    return np.std(values, ddof=ddof)

import csv, json

import numpy as np

policy = json.loads('{"reference_id": "reference", "production_window": {"start": "2026-01-02T10:00:00Z", "end": "2026-01-02T11:00:00Z"}, "fixed_edges": [0, 5, 10], "eligible_numeric_range": [0, 10], "declared_categories": ["short_distance", "long_distance", "not_reported"], "declared_classes": ["on_time", "late", "abstain"], "ddof": 0, "window_membership": "All rows of production.csv are in the declared bounded window; reference.csv is the approved reference. Alternate fixtures are independent windows.", "summary_client": "from summary_client import emit; emit(record) appends a single JSON record to summary.jsonl"}')

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

records = []

def emit(record):
    records.append(record)

summarize(reference, production, policy)