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

def aligned_counts(data,names):
    return np.asarray([np.count_nonzero(column(data,'category')==k) for k in names])


policy = {'reference_id': 'reference', 'current_id': 'production', 'comparison_window': '2026-01-02T10:00:00Z/2026-01-02T11:00:00Z', 'fixed_edges': [0, 5, 10], 'eligible_numeric_range': [0, 10], 'declared_categories': ['short_distance', 'long_distance', 'not_reported'], 'ddof': 0, 'distance_equation': '0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions', 'criterion': 'distance > 0.20; equality is not a crossing', 'numeric_rule': 'Apply the same distance to aligned numerical-bin proportions; retain mean and ddof=0 standard deviation separately', 'quality_claim': 'unresolved without matched labels'}
def calculate_contract(reference_input,production_input,mean_function,spread_function):
    supplied_rows = {'reference':reference_input,'production':production_input}
    def load(name):
        return supplied_rows[name]
    policy = {'reference_id': 'reference', 'current_id': 'production', 'comparison_window': '2026-01-02T10:00:00Z/2026-01-02T11:00:00Z', 'fixed_edges': [0, 5, 10], 'eligible_numeric_range': [0, 10], 'declared_categories': ['short_distance', 'long_distance', 'not_reported'], 'ddof': 0, 'distance_equation': '0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions', 'criterion': 'distance > 0.20; equality is not a crossing', 'numeric_rule': 'Apply the same distance to aligned numerical-bin proportions; retain mean and ddof=0 standard deviation separately', 'quality_claim': 'unresolved without matched labels'}
    threshold = 0.2
    factor = 0.5
    reference = load('reference')
    production = load('production')
    r = column(reference,'numeric_values')
    p = column(production,'numeric_values')
    r_total = len(reference)
    p_total = len(production)
    r_counts = aligned_counts(reference,policy['declared_categories'])
    p_counts = aligned_counts(production,policy['declared_categories'])
    fixed_edges = np.asarray(policy['fixed_edges'])
    r_bin_counts = np.histogram(r,bins=fixed_edges)[0]
    p_bin_counts = np.histogram(p,bins=fixed_edges)[0]
    r_mean = mean_function(r)
    
    p_mean = mean_function(p)
    
    r_std = spread_function(r, ddof=0)
    
    p_std = spread_function(p, ddof=0)
    
    r_prob = r_counts / r_total
    
    p_prob = p_counts / p_total
    
    r_bin_prob = r_bin_counts / r_total
    
    p_bin_prob = p_bin_counts / p_total
    
    distance = factor * np.sum(np.abs(p_prob-r_prob))
    
    numeric_distance = factor * np.sum(np.abs(p_bin_prob-r_bin_prob))
    
    category_drift = distance > threshold
    
    numeric_drift = numeric_distance > threshold
    
    report = {'definitions':policy,'r_total':r_total,'p_total':p_total,'r_mean':r_mean,'p_mean':p_mean,'r_std':r_std,'p_std':p_std,'r_prob':r_prob,'p_prob':p_prob,'r_bin_prob':r_bin_prob,'p_bin_prob':p_bin_prob,'category_distance':distance,'numeric_distance':numeric_distance,'category_drift':category_drift,'numeric_drift':numeric_drift,'interpretation':'distribution difference only'}
    return report

# OUTER

reference_rows = load('reference')
production_rows = load('production')
reference_input = reference_rows
production_input = production_rows
mean_function = np.mean
spread_function = np.std
report = calculate_contract(reference_input,production_input,mean_function,spread_function)
