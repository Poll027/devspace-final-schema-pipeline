import csv, json, datetime
import numpy as np
SCHEMAS = {'lifecycle': {'INSTANCE': 'string', 'ZONE': 'string', 'workload': 'string', 'reporting_window': 'string', 'start': 'datetime', 'stop': 'datetime', 'before_state': 'string', 'after_state': 'string', 'completed_work': 'integer'}, 'billing_export': {'charge_id': 'string', 'reporting_window': 'string', 'resource_id': 'string', 'charge_category': 'string', 'amount': 'number'}}
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

def verified_lifecycles(data):
    records=[]
    for r in data:
        if r['before_state']!='TERMINATED' or r['after_state']!='TERMINATED':raise ValueError('lifecycle not stopped')
        records.append({'identity':r['INSTANCE'],'ZONE':r['ZONE'],'window':r['reporting_window'],'start':r['start'],'stop':r['stop'],'work':r['completed_work'],'trace':['describe before','start and wait running','ssh and bounded workload','stop and wait stopped','describe after']})
    return records


policy = {'authorized_identity': 'lab.operator', 'resource_mapping': {'training-lab': 'training', 'inference-lab': 'inference', 'training-disk': 'training'}, 'shared_rule': {'training': 0.5, 'inference': 0.5}, 'unmatched_rule': 'explicitly unallocated', 'unusual_rule': 'per-workload per-window allocation >10', 'unit': 'fictional credits', 'reporting_windows': {'w1': ['2026-01-02T00:00:00Z', '2026-01-03T00:00:00Z'], 'w2': ['2026-01-03T00:00:00Z', '2026-01-04T00:00:00Z']}, 'direct_interval_rule': 'direct_compute rows correspond to the named resource lifecycle/work interval; persistent_disk spans reporting window even after stop', 'numeric_values': 'Select per-window attributed costs for each workload; do not mix workload series', 'ddof': 0}
def calculate_contract(lifecycle_input,billing_export_input,mean_function,spread_function):
    supplied_rows = {'lifecycle':lifecycle_input,'billing_export':billing_export_input}
    def load(name):
        return supplied_rows[name]
    policy = {'authorized_identity': 'lab.operator', 'resource_mapping': {'training-lab': 'training', 'inference-lab': 'inference', 'training-disk': 'training'}, 'shared_rule': {'training': 0.5, 'inference': 0.5}, 'unmatched_rule': 'explicitly unallocated', 'unusual_rule': 'per-workload per-window allocation >10', 'unit': 'fictional credits', 'reporting_windows': {'w1': ['2026-01-02T00:00:00Z', '2026-01-03T00:00:00Z'], 'w2': ['2026-01-03T00:00:00Z', '2026-01-04T00:00:00Z']}, 'direct_interval_rule': 'direct_compute rows correspond to the named resource lifecycle/work interval; persistent_disk spans reporting window even after stop', 'numeric_values': 'Select per-window attributed costs for each workload; do not mix workload series', 'ddof': 0}
    lifecycles = verified_lifecycles(load('lifecycle'))
    charges = load('billing_export')
    unusual_threshold = 10.0
    allocated = {'training':{'w1':0,'w2':0},'inference':{'w1':0,'w2':0}}
    
    unallocated = []
    
    eligible_total = 0
    
    for r in charges:
        eligible_total = eligible_total + r['amount']
        if r['resource_id'] in policy['resource_mapping']:
            workload = policy['resource_mapping'][r['resource_id']]
            allocated[workload][r['reporting_window']] = allocated[workload][r['reporting_window']] + r['amount']
        elif r['charge_category']=='shared':
            for workload in ['training','inference']:
                allocated[workload][r['reporting_window']] = allocated[workload][r['reporting_window']] + r['amount']*policy['shared_rule'][workload]
        else:
            unallocated.append(r)
    
    summary = {}
    
    unusual = []
    
    allocated_total = 0
    
    for workload in ['training','inference']:
        numeric_values = np.array([allocated[workload]['w1'],allocated[workload]['w2']])
        works = []
        unit_costs = []
        for window in ['w1','w2']:
            amount = allocated[workload][window]
            allocated_total = allocated_total + amount
            if amount > unusual_threshold:
                unusual.append({'workload':workload,'window':window,'amount':amount})
            completed = 0
            for l in lifecycles:
                if l['identity']==workload+'-lab' and l['window']==window:
                    completed = completed + l['work']
            works.append(completed)
            unit = None
            if completed > 0:
                unit = amount/completed
            unit_costs.append(unit)
        summary[workload] = {'window_costs':numeric_values,'mean':mean_function(numeric_values),'std':spread_function(numeric_values, ddof=0),'work':works,'unit_costs':unit_costs}
    
    unallocated_total = sum([r['amount'] for r in unallocated])
    
    assert allocated_total + unallocated_total == eligible_total
    
    result = {'lifecycle_evidence':lifecycles,'allocations':allocated,'summaries':summary,'unallocated':unallocated,'unusual':unusual,'allocated_total':allocated_total,'unallocated_total':unallocated_total,'eligible_export_total':eligible_total,'unit':policy['unit']}
    
    report = result
    return report

# OUTER

lifecycle_rows = load('lifecycle')
billing_export_rows = load('billing_export')
lifecycle_input = lifecycle_rows
billing_export_input = billing_export_rows
mean_function = np.mean
spread_function = np.std
report = calculate_contract(lifecycle_input,billing_export_input,mean_function,spread_function)
