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
def emit(value):
    return value


policy = {'reference_id': 'reference', 'production_window': {'start': '2026-01-02T10:00:00Z', 'end': '2026-01-02T11:00:00Z'}, 'fixed_edges': [0, 5, 10], 'eligible_numeric_range': [0, 10], 'declared_categories': ['short_distance', 'long_distance', 'not_reported'], 'declared_classes': ['on_time', 'late', 'abstain'], 'ddof': 0, 'window_membership': 'All rows of production.csv are in the declared bounded window; reference.csv is the approved reference. Alternate fixtures are independent windows.', 'summary_client': 'from summary_client import emit; emit(record) appends a single JSON record to summary.jsonl'}
def calculate_contract(reference_input,production_input,mean_function,spread_function):
    supplied_rows = {'reference':reference_input,'production':production_input}
    def load(name):
        return supplied_rows[name]
    policy = {'reference_id': 'reference', 'production_window': {'start': '2026-01-02T10:00:00Z', 'end': '2026-01-02T11:00:00Z'}, 'fixed_edges': [0, 5, 10], 'eligible_numeric_range': [0, 10], 'declared_categories': ['short_distance', 'long_distance', 'not_reported'], 'declared_classes': ['on_time', 'late', 'abstain'], 'ddof': 0, 'window_membership': 'All rows of production.csv are in the declared bounded window; reference.csv is the approved reference. Alternate fixtures are independent windows.', 'summary_client': 'from summary_client import emit; emit(record) appends a single JSON record to summary.jsonl'}
    reference = load('reference')
    production = load('production')
    r = column(reference,'numeric_values')
    p = column(production,'numeric_values')
    rc = column(reference,'category')
    pc = column(production,'category')
    rpred = column(reference,'predicted_class')
    ppred = column(production,'predicted_class')
    fixed_edges = np.asarray(policy['fixed_edges'])
    category_names = np.asarray(policy['declared_categories'])
    class_names = np.asarray(policy['declared_classes'])
    r_count = len(r)
    
    p_count = len(p)
    
    r_bins = np.histogram(r, bins=fixed_edges)[0] / r_count
    
    p_bins = np.histogram(p, bins=fixed_edges)[0] / p_count
    
    r_category = np.sum(rc[:, None] == category_names, axis=0) / len(rc)
    
    p_category = np.sum(pc[:, None] == category_names, axis=0) / len(pc)
    
    r_class = np.sum(rpred[:, None] == class_names, axis=0) / len(rpred)
    
    p_class = np.sum(ppred[:, None] == class_names, axis=0) / len(ppred)
    
    r_mean = mean_function(r)
    
    p_mean = mean_function(p)
    
    r_std = spread_function(r, ddof=0)
    
    p_std = spread_function(p, ddof=0)
    
    report = {'definitions':policy,'reference':{'eligible':r_count,'bins':r_bins,'category':r_category,'classes':r_class,'mean':r_mean,'std':r_std},'production':{'eligible':p_count,'bins':p_bins,'category':p_category,'classes':p_class,'mean':p_mean,'std':p_std}}
    return report

# OUTER

reference_rows = load('reference')
production_rows = load('production')
reference_input = reference_rows
production_input = production_rows
mean_function = np.mean
spread_function = np.std
report = calculate_contract(reference_input,production_input,mean_function,spread_function)
