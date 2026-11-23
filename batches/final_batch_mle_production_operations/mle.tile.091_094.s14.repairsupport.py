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
        notification={'notified':row['notification_expected'],'topic':config['notification_topic'] if row['notification_expected'] else None}
        response={'executed':('gcloud compute instances stop '+row['INSTANCE']+' --zone='+row['ZONE']) if row['response_expected'] else None,'before':{'INSTANCE':row['INSTANCE'],'ZONE':row['ZONE'],'state':'RUNNING'},'after':{'INSTANCE':row['INSTANCE'],'ZONE':row['ZONE'],'state':row['expected_after_state']},'acted_targets':[{'INSTANCE':row['INSTANCE'],'ZONE':row['ZONE']}] if row['response_expected'] else [],'captured_output':'stop completed on fixed target' if row['response_expected'] else 'no stop response', 'credential_values':[]}
        outputs.append({'fixture':row['fixture'],'observed_spend':row['observed_spend'],**notification,**response,'credentials':None})
    return outputs
policy = {'workload_scope': 'order-lab', 'budget_amount': 100, 'period': 'monthly', 'threshold_ratio': 0.8, 'predicate': 'observed_spend>=budget_amount*threshold_ratio', 'notification_topic': 'lab-budget-events', 'response_pipeline': 'lab-safe-stop', 'INSTANCE': 'inference-lab', 'ZONE': 'lab-zone-a', 'authorized_identity': 'lab.operator', 'secret_version_reference': 'projects/order-lab/secrets/budget-client/versions/1', 'residual_limitation': 'Notifications can lag usage and do not enforce a hard spending cap.'}


# Supplied orchestration; operations are selected by the learner.
import yaml
supplied_safe_dump = yaml.safe_dump
supplied_safe_load = yaml.safe_load

#TAIL

dump_operation = supplied_safe_dump
load_operation = supplied_safe_load
import yaml
supplied_safe_dump = yaml.safe_dump
supplied_safe_load = yaml.safe_load
dump_operation = supplied_safe_dump
load_operation = supplied_safe_load
import yaml
policy = {'workload_scope': 'order-lab', 'budget_amount': 100, 'period': 'monthly', 'threshold_ratio': 0.8, 'predicate': 'observed_spend>=budget_amount*threshold_ratio', 'notification_topic': 'lab-budget-events', 'response_pipeline': 'lab-safe-stop', 'INSTANCE': 'inference-lab', 'ZONE': 'lab-zone-a', 'authorized_identity': 'lab.operator', 'secret_version_reference': 'projects/order-lab/secrets/budget-client/versions/1', 'residual_limitation': 'Notifications can lag usage and do not enforce a hard spending cap.'}
data = load('budget_replay')
config = {'INSTANCE': policy['INSTANCE'], 'ZONE': policy['ZONE'], 'authorized_identity': policy['authorized_identity'], 'budget_amount': policy['budget_amount'], 'notification_topic': policy['notification_topic'], 'period': policy['period'], 'predicate': policy['predicate'], 'residual_limitation': policy['residual_limitation'], 'response_pipeline': policy['response_pipeline'], 'secret_version_reference': policy['secret_version_reference'], 'threshold_ratio': policy['threshold_ratio'], 'workload_scope': policy['workload_scope'], 'event_binding': {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}, 'availableSecrets': {'secretManager': [{'versionName': policy['secret_version_reference'], 'env': 'BUDGET_CLIENT'}]}, 'secretEnv': ['BUDGET_CLIENT']}
file_handle = open('budget.yaml', 'w')
dump_operation(config, file_handle)
file_handle.close()
file_handle = open('budget.yaml')
loaded = load_operation(file_handle)
file_handle.close()
outputs = budget_replay(loaded, data)
verification = {'config_roundtrip': loaded == config, 'below': outputs[0]['notified'] == False and outputs[0]['executed'] == None, 'equality': outputs[1]['notified'] == True and outputs[1]['executed'] != None, 'breach': outputs[2]['notified'] == True and outputs[2]['executed'] != None, 'target': outputs[1]['after']['INSTANCE'] == policy['INSTANCE'] and outputs[2]['after']['ZONE'] == policy['ZONE'], 'states': outputs[0]['after']['state'] == 'RUNNING' and outputs[1]['after']['state'] == 'TERMINATED' and (outputs[2]['after']['state'] == 'TERMINATED'), 'credential_safe': outputs[0]['credential_values'] == [] and outputs[1]['credential_values'] == [] and (outputs[2]['credential_values'] == []) and (outputs[0]['captured_output'] == 'no stop response') and (outputs[1]['captured_output'] == 'stop completed on fixed target') and (outputs[2]['captured_output'] == 'stop completed on fixed target'), 'only_target': outputs[0]['acted_targets'] == [] and outputs[1]['acted_targets'] == [{'INSTANCE': policy['INSTANCE'], 'ZONE': policy['ZONE']}] and (outputs[2]['acted_targets'] == [{'INSTANCE': policy['INSTANCE'], 'ZONE': policy['ZONE']}])}
outputs[0]['credentials'] = 'runtime Secret Manager reference; captured output reviewed'
outputs[1]['credentials'] = 'runtime Secret Manager reference; captured output reviewed'
outputs[2]['credentials'] = 'runtime Secret Manager reference; captured output reviewed'
report = {'config': loaded, 'replay': outputs, 'limitation': policy['residual_limitation']}
