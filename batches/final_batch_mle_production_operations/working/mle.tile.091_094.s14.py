import csv, json, datetime
import numpy as np
SCHEMAS = {'budget_replay': {'fixture': 'string', 'workload_scope': 'string', 'budget_amount': 'number', 'period': 'string', 'threshold_ratio': 'number', 'observed_spend': 'number', 'INSTANCE': 'string', 'ZONE': 'string', 'notification_expected': 'boolean', 'response_expected': 'boolean', 'expected_after_state': 'string'}}
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

def budget_replay(config,data):
    outputs=[]
    for row in data:
        breached=row['observed_spend']>=config['budget_amount']*config['threshold_ratio']
        outputs.append({'fixture':row['fixture'],'observed_spend':row['observed_spend'],'notified':breached,'topic':config['notification_topic'] if breached else None,'executed':('gcloud compute instances stop '+config['INSTANCE']+' --zone='+config['ZONE']) if breached else None,'before':{'INSTANCE':config['INSTANCE'],'ZONE':config['ZONE'],'state':'RUNNING'},'after':{'INSTANCE':config['INSTANCE'],'ZONE':config['ZONE'],'state':'TERMINATED' if breached else 'RUNNING'},'credentials':'runtime Secret Manager reference; captured output reviewed'})
    return outputs


policy = {'workload_scope': 'order-lab', 'budget_amount': 100, 'period': 'monthly', 'threshold_ratio': 0.8, 'predicate': 'observed_spend>=budget_amount*threshold_ratio', 'notification_topic': 'lab-budget-events', 'response_pipeline': 'lab-safe-stop', 'INSTANCE': 'inference-lab', 'ZONE': 'lab-zone-a', 'authorized_identity': 'lab.operator', 'secret_version_reference': 'projects/order-lab/secrets/budget-client/versions/1', 'residual_limitation': 'Notifications can lag usage and do not enforce a hard spending cap.'}
def calculate_contract(budget_replay_input):
    supplied_rows = {'budget_replay':budget_replay_input}
    def load(name):
        return supplied_rows[name]
    import yaml
    policy = {'workload_scope': 'order-lab', 'budget_amount': 100, 'period': 'monthly', 'threshold_ratio': 0.8, 'predicate': 'observed_spend>=budget_amount*threshold_ratio', 'notification_topic': 'lab-budget-events', 'response_pipeline': 'lab-safe-stop', 'INSTANCE': 'inference-lab', 'ZONE': 'lab-zone-a', 'authorized_identity': 'lab.operator', 'secret_version_reference': 'projects/order-lab/secrets/budget-client/versions/1', 'residual_limitation': 'Notifications can lag usage and do not enforce a hard spending cap.'}
    data = load('budget_replay')
    
    config = policy
    with open('budget.yaml','w') as file_handle:
        yaml.safe_dump(config, file_handle)
    with open('budget.yaml') as file_handle:
        loaded = yaml.safe_load(file_handle)
    outputs = budget_replay(loaded,data)
    report = {'config':loaded,'replay':outputs,'limitation':policy['residual_limitation']}
    return report

# OUTER

budget_replay_rows = load('budget_replay')
budget_replay_input = budget_replay_rows
report = calculate_contract(budget_replay_input)
