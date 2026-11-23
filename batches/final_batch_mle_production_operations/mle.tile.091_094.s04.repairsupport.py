import csv, json, datetime
import numpy as np
SCHEMAS = {'resource_telemetry': {'timestamp': 'datetime', 'INSTANCE': 'string', 'process_id': 'string', 'instance_state': 'string', 'running_process': 'string', 'cpu_percent': 'number', 'memory_value': 'number', 'memory_unit': 'string', 'included': 'boolean'}}
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
policy = {'INSTANCE': 'serving-lab', 'process_id': 'model-service', 'interval_start': '2026-01-02T10:00:00Z', 'interval_end_exclusive': '2026-01-02T10:03:00Z', 'cpu_unit': 'percent', 'memory_unit': 'MiB', 'ddof': 0, 'action_required': False, 'lifecycle_policy': 'These lifecycle records belong to the utilization fixture; no recovery fault or learner lifecycle action is required.'}

policy = {'INSTANCE': 'serving-lab', 'process_id': 'model-service', 'interval_start': '2026-01-02T10:00:00Z', 'interval_end_exclusive': '2026-01-02T10:03:00Z', 'cpu_unit': 'percent', 'memory_unit': 'MiB', 'ddof': 0, 'action_required': False, 'lifecycle_policy': 'These lifecycle records belong to the utilization fixture; no recovery fault or learner lifecycle action is required.'}

# Supplied orchestration; operations are selected by the learner.

#TAIL

data = load('resource_telemetry')
instance = column(data, 'INSTANCE')
process = column(data, 'process_id')
running_process = column(data, 'running_process')
state = column(data, 'instance_state')
time = column(data, 'timestamp')
cpu_all = column(data, 'cpu_percent')
memory_all = column(data, 'memory_value')
mask = (instance == policy['INSTANCE']) & (process == policy['process_id']) & (running_process == policy['process_id']) & (state == 'RUNNING') & (time >= policy['interval_start']) & (time < policy['interval_end_exclusive'])
cpu = cpu_all[mask]
memory = memory_all[mask]
count = len(cpu)
cpu_mean = np.mean(cpu)
cpu_std = np.std(cpu, ddof=0)
memory_mean = np.mean(memory)
memory_std = np.std(memory, ddof=0)
report = {'scope': policy, 'count': count, 'cpu_mean': cpu_mean, 'cpu_std': cpu_std, 'memory_mean': memory_mean, 'memory_std': memory_std, 'cpu_count': count, 'memory_count': len(memory), 'interpretation': 'descriptive utilization for this matched workload interval only'}
