import csv, json, datetime
import numpy as np
SCHEMAS = {'reference': {'numeric_values': 'number', 'category': 'string', 'predicted_class': 'string'}, 'production': {'numeric_values': 'number', 'category': 'string', 'predicted_class': 'string'}}
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
policy = {'reference_id': 'reference', 'production_window': {'start': '2026-01-02T10:00:00Z', 'end': '2026-01-02T11:00:00Z'}, 'fixed_edges': [0, 5, 10], 'eligible_numeric_range': [0, 10], 'declared_categories': ['short_distance', 'long_distance', 'not_reported'], 'declared_classes': ['on_time', 'late', 'abstain'], 'ddof': 0, 'window_membership': 'All rows of production.csv are in the declared bounded window; reference.csv is the approved reference. Alternate fixtures are independent windows.', 'summary_client': 'from summary_client import emit; emit(record) appends a single JSON record to summary.jsonl'}
emitted_records = []
def emit(record):
    def plain(x):
        if isinstance(x, dict): return {k:plain(v) for k,v in x.items()}
        if isinstance(x, (list,tuple)): return [plain(v) for v in x]
        if isinstance(x, np.ndarray): return x.tolist()
        if isinstance(x, np.generic): return x.item()
        return x
    value=plain(record)
    emitted_records.append(value)
    with open('summary.jsonl','a') as f: f.write(json.dumps(value)+'\n')
    return value


# Supplied orchestration; operations are selected by the learner.
def summarize(reference_rows, production_rows, policy):
    reference = reference_rows
    production = production_rows
    r = column(reference, 'numeric_values')
    p = column(production, 'numeric_values')
    low = policy['eligible_numeric_range'][0]
    high = policy['eligible_numeric_range'][1]
    r = r[(r >= low) & (r <= high)]
    p = p[(p >= low) & (p <= high)]
    rc = column(reference, 'category')
    pc = column(production, 'category')
    rpred = column(reference, 'predicted_class')
    ppred = column(production, 'predicted_class')
    fixed_edges = asarray_operation(policy['fixed_edges'])
    category_names = asarray_operation(policy['declared_categories'])
    class_names = asarray_operation(policy['declared_classes'])
    r_count = len(r)
    p_count = len(p)
    r_bins = histogram_operation(r, bins=fixed_edges)[0] / r_count
    p_bins = histogram_operation(p, bins=fixed_edges)[0] / p_count
    r_category = sum_operation(rc[:, None] == category_names, axis=0) / len(rc)
    p_category = sum_operation(pc[:, None] == category_names, axis=0) / len(pc)
    r_class = sum_operation(rpred[:, None] == class_names, axis=0) / len(rpred)
    p_class = sum_operation(ppred[:, None] == class_names, axis=0) / len(ppred)
    r_mean = mean_operation(r)
    p_mean = mean_operation(p)
    r_std = std_operation(r, ddof=0)
    p_std = std_operation(p, ddof=0)
    report = {'definitions': policy, 'reference': {'eligible': r_count, 'bins': r_bins, 'category': r_category, 'classes': r_class, 'mean': r_mean, 'std': r_std}, 'production': {'eligible': p_count, 'bins': p_bins, 'category': p_category, 'classes': p_class, 'mean': p_mean, 'std': p_std}}
    return report

#TAIL

asarray_operation = np.asarray
histogram_operation = np.histogram
sum_operation = np.sum
mean_operation = np.mean
std_operation = np.std
report = emit(summarize(load('reference'), load('production'), policy))
