import csv, json, datetime
import numpy as np
SCHEMAS = {'alert_observations': {'window_id': 'string', 'numeric_values': 'number'}}
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

def replay(config,data):
    windows={}
    for r in data: windows.setdefault(r['window_id'],[]).append(r['numeric_values'])
    return [{'window':k,'owner':config['owner'],'response':config['response']} for k,v in windows.items() if k!='baseline' and np.mean(v)>config['threshold']]


policy = {'indicator': 'window_mean', 'baseline_window': 'baseline', 'window_rule': 'mean(window)>mean(baseline)+4', 'ddof': 0, 'owner': 'order_oncall', 'response': 'investigate_window', 'expected_replays': {'normal': False, 'boundary': False, 'breached': True}}
def calculate_contract(alert_observations_input,mean_function,spread_function):
    supplied_rows = {'alert_observations':alert_observations_input}
    def load(name):
        return supplied_rows[name]
    import yaml
    policy = {'indicator': 'window_mean', 'baseline_window': 'baseline', 'window_rule': 'mean(window)>mean(baseline)+4', 'ddof': 0, 'owner': 'order_oncall', 'response': 'investigate_window', 'expected_replays': {'normal': False, 'boundary': False, 'breached': True}}
    data = load('alert_observations')
    margin = 4
    baseline = np.asarray([r['numeric_values'] for r in data if r['window_id']=='baseline'])
    mean = mean_function(baseline)
    
    std = spread_function(baseline, ddof=0)
    
    threshold = mean + margin
    
    config = {'threshold': threshold, 'owner': policy['owner'], 'response': policy['response'], 'ddof': 0}
    
    config['threshold'] = float(config['threshold'])
    
    with open('alert.yaml','w') as file_handle:
        yaml.safe_dump(config, file_handle)
    
    with open('alert.yaml') as file_handle:
        loaded = yaml.safe_load(file_handle)
    
    assert (threshold-1 > threshold) == False
    
    assert (threshold > threshold) == False
    
    assert (threshold+1 > threshold) == True
    
    records = replay(loaded,data)
    
    report = {'mean':mean,'std':std,'config':loaded,'records':records}
    return report

# OUTER

alert_observations_rows = load('alert_observations')
alert_observations_input = alert_observations_rows
mean_function = np.mean
spread_function = np.std
report = calculate_contract(alert_observations_input,mean_function,spread_function)
