import csv, json

import numpy as np

policy = json.loads('{"authorized_identity": "lab.operator", "resource_mapping": {"training-lab": "training", "inference-lab": "inference", "training-disk": "training"}, "shared_rule": {"training": 0.5, "inference": 0.5}, "unmatched_rule": "explicitly unallocated", "unusual_rule": "per-workload per-window allocation >10", "unit": "fictional credits", "reporting_windows": {"w1": ["2026-01-02T00:00:00Z", "2026-01-03T00:00:00Z"], "w2": ["2026-01-03T00:00:00Z", "2026-01-04T00:00:00Z"]}, "direct_interval_rule": "direct_compute rows correspond to the named resource lifecycle/work interval; persistent_disk spans reporting window even after stop", "numeric_values": "Select per-window attributed costs for each workload; do not mix workload series", "ddof": 0}')

billing_export_rows = list(csv.DictReader(open('billing_export.csv')))

billing_export = {}

billing_export['charge_id'] = np.array([r['charge_id'] for r in billing_export_rows])

billing_export['reporting_window'] = np.array([r['reporting_window'] for r in billing_export_rows])

billing_export['resource_id'] = np.array([r['resource_id'] for r in billing_export_rows])

billing_export['charge_category'] = np.array([r['charge_category'] for r in billing_export_rows])

billing_export['amount'] = np.array([float(r['amount'] or 'nan') for r in billing_export_rows])

lifecycle_rows = list(csv.DictReader(open('lifecycle.csv')))

lifecycle = {}

lifecycle['INSTANCE'] = np.array([r['INSTANCE'] for r in lifecycle_rows])

lifecycle['ZONE'] = np.array([r['ZONE'] for r in lifecycle_rows])

lifecycle['workload'] = np.array([r['workload'] for r in lifecycle_rows])

lifecycle['reporting_window'] = np.array([r['reporting_window'] for r in lifecycle_rows])

lifecycle['start'] = np.array([r['start'] for r in lifecycle_rows])

lifecycle['stop'] = np.array([r['stop'] for r in lifecycle_rows])

lifecycle['before_state'] = np.array([r['before_state'] for r in lifecycle_rows])

lifecycle['after_state'] = np.array([r['after_state'] for r in lifecycle_rows])

lifecycle['completed_work'] = np.array([float(r['completed_work'] or 'nan') for r in lifecycle_rows])

charges = [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in billing_export.items()} for i in range(len(billing_export_rows))]

class LifecycleSimulator:
    def __init__(self, rows):
        self.rows = rows
        self.actions = []
        self.records = []
        self.sessions = {}
    def act(self, row, action):
        key = (row['INSTANCE'], row['ZONE'], row['reporting_window'])
        session = self.sessions.setdefault(key, {'state': row['before_state'], 'sequence': [], 'completed_work': '0'})
        allowed = ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']
        position = len(session['sequence'])
        if position >= len(allowed) or action != allowed[position]:
            return False
        session['sequence'].append(action)
        self.actions.append({'INSTANCE': row['INSTANCE'], 'ZONE': row['ZONE'], 'reporting_window': row['reporting_window'], 'action': action})
        if action == 'start':
            session['state'] = 'RUNNING'
        elif action == 'workload' and session['state'] == 'RUNNING':
            session['completed_work'] = row['completed_work']
        elif action == 'stop':
            session['state'] = 'TERMINATED'
        if len(session['sequence']) == len(allowed):
            record = dict(row)
            record['completed_work'] = session['completed_work']
            record['after_state'] = session['state']
            self.records.append(record)
        return True
    def evidence(self):
        verified = len(self.rows) > 0 and len(self.records) == len(self.rows) and all(s['state'] == 'TERMINATED' and s['sequence'] == ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'] for s in self.sessions.values())
        return {'identity': policy['authorized_identity'], 'actions': self.actions, 'records': self.records, 'verified_stopped': verified}

def simulate_sequences(sequences):
    sim = LifecycleSimulator(lifecycle_rows)
    for row in lifecycle_rows:
        for action in sequences[row['workload']]:
            sim.act(row, action)
    return sim.evidence()

sequences = {'training': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'], 'inference': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']}

lifecycle_record = simulate_sequences(sequences)

allocated = {'training': {'w1': 0, 'w2': 0}, 'inference': {'w1': 0, 'w2': 0}}

unallocated = 0

export_total = 0

unmatched = []

for row in charges:
    window = row['reporting_window']
    amount = row['amount']
    export_total = export_total + amount
    if row['charge_category'] == 'shared':
        allocated['training'][window] = allocated['training'][window] + amount * policy['shared_rule']['training']
        allocated['inference'][window] = allocated['inference'][window] + amount * policy['shared_rule']['inference']
    elif row['resource_id'] in policy['resource_mapping']:
        workload = policy['resource_mapping'][row['resource_id']]
        allocated[workload][window] = allocated[workload][window] + amount
    else:
        unallocated = unallocated + amount
        unmatched = unmatched + [row['charge_id']]

training_values = np.array([allocated['training']['w1'], allocated['training']['w2']])

inference_values = np.array([allocated['inference']['w1'], allocated['inference']['w2']])

training_mean = None

training_std = None

inference_mean = None

inference_std = None

summary = {}

for workload in ['training', 'inference']:
    values = np.array([allocated[workload]['w1'], allocated[workload]['w2']])
    summary[workload] = {'windows': allocated[workload], 'mean': training_mean if workload == 'training' else inference_mean, 'std': training_std if workload == 'training' else inference_std, 'unusual_w1': allocated[workload]['w1'] > 10, 'unusual_w2': allocated[workload]['w2'] > 10}

allocated_total = sum([allocated['training']['w1'], allocated['training']['w2'], allocated['inference']['w1'], allocated['inference']['w2']])

reconciled = allocated_total + unallocated == export_total

result = {'lifecycle': lifecycle_record, 'summary': summary, 'unmatched_charge_ids': unmatched, 'unallocated': unallocated, 'allocated_total': allocated_total, 'export_total': export_total, 'unit': policy['unit'], 'reporting_windows': policy['reporting_windows'], 'ddof': policy['ddof']}