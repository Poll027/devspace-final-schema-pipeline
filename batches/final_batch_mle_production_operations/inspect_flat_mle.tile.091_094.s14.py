import csv, json

import numpy as np

policy = json.loads('{"workload_scope": "order-lab", "budget_amount": 100, "period": "monthly", "threshold_ratio": 0.8, "predicate": "observed_spend>=budget_amount*threshold_ratio", "notification_topic": "lab-budget-events", "response_pipeline": "lab-safe-stop", "INSTANCE": "inference-lab", "ZONE": "lab-zone-a", "authorized_identity": "lab.operator", "secret_version_reference": "projects/order-lab/secrets/budget-client/versions/1", "residual_limitation": "Notifications can lag usage and do not enforce a hard spending cap."}')

budget_replay_rows = list(csv.DictReader(open('budget_replay.csv')))

budget_replay = {}

budget_replay['fixture'] = np.array([r['fixture'] for r in budget_replay_rows])

budget_replay['workload_scope'] = np.array([r['workload_scope'] for r in budget_replay_rows])

budget_replay['budget_amount'] = np.array([float(r['budget_amount'] or 'nan') for r in budget_replay_rows])

budget_replay['period'] = np.array([r['period'] for r in budget_replay_rows])

budget_replay['threshold_ratio'] = np.array([float(r['threshold_ratio'] or 'nan') for r in budget_replay_rows])

budget_replay['observed_spend'] = np.array([float(r['observed_spend'] or 'nan') for r in budget_replay_rows])

budget_replay['INSTANCE'] = np.array([r['INSTANCE'] for r in budget_replay_rows])

budget_replay['ZONE'] = np.array([r['ZONE'] for r in budget_replay_rows])

budget_replay['notification_expected'] = np.array([r['notification_expected'] == 'True' for r in budget_replay_rows])

budget_replay['response_expected'] = np.array([r['response_expected'] == 'True' for r in budget_replay_rows])

budget_replay['expected_after_state'] = np.array([r['expected_after_state'] for r in budget_replay_rows])

import yaml

class NotificationResponseSimulator:
    def __init__(self, config):
        self.config = config
        self.states = {(policy['INSTANCE'], policy['ZONE']): 'RUNNING', ('untargeted-control', policy['ZONE']): 'RUNNING'}
        self.receipts = []
        self.actions = []
        self.output = []
        self.runtime_secret = 'fixture-runtime-only-credential'
    def describe(self):
        return {'INSTANCE': self.config['INSTANCE'], 'ZONE': self.config['ZONE'], 'state': self.states[(self.config['INSTANCE'], self.config['ZONE'])]}
    def notify(self, row):
        crossed = float(row['observed_spend']) >= self.config['budget_amount'] * self.config['threshold_ratio']
        if crossed and row['workload_scope'] == self.config['workload_scope']:
            self.receipts.append({'topic': self.config['notification_topic'], 'fixture': row['fixture']})
        return bool(self.receipts)
    def respond(self):
        c = self.config
        authorized = c['authorized_identity'] == policy['authorized_identity'] and [c['INSTANCE'], c['ZONE']] == [policy['INSTANCE'], policy['ZONE']]
        bound = c['event_binding'] == {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}
        secret_ok = c['secret_version_reference'] == policy['secret_version_reference'] and c['secretEnv'] == ['BUDGET_CLIENT']
        step = c.get('response_step', {})
        args = step.get('args', [])
        step_ok = step.get('name') == 'gcloud' and args == ['compute', 'instances', 'stop', policy['INSTANCE'], '--zone=' + policy['ZONE']]
        if self.receipts and authorized and bound and secret_ok and step_ok:
            self.actions.append({'command': step['name'] + ' ' + ' '.join(args[:3]), 'INSTANCE': args[3], 'ZONE': args[4].removeprefix('--zone=')})
            self.states[(c['INSTANCE'], c['ZONE'])] = 'TERMINATED'
            self.output.append('stop completed: ' + c['INSTANCE'] + ' --zone=' + c['ZONE'])
        return authorized and bound and secret_ok and step_ok
    def evidence(self, row):
        before = self.describe()
        notified = self.notify(row)
        authorized = self.respond()
        captured = '\n'.join(self.output)
        target_only = all(a['INSTANCE'] == policy['INSTANCE'] and a['ZONE'] == policy['ZONE'] for a in self.actions) and self.states[('untargeted-control', policy['ZONE'])] == 'RUNNING'
        after = self.describe()
        return {'fixture': row['fixture'], 'notification': notified, 'notification_receipts': self.receipts, 'authorized_response': authorized and bool(self.actions), 'actions': self.actions, 'before': before, 'after': after, 'stop_completed': bool(self.actions) and after['state'] == 'TERMINATED', 'target_only': target_only, 'captured_output': captured, 'credential_non_disclosure': self.runtime_secret not in captured}

def apply_and_replay(config):
    expected = {k: policy[k] for k in ['workload_scope', 'budget_amount', 'period', 'threshold_ratio', 'notification_topic', 'response_pipeline', 'INSTANCE', 'ZONE', 'authorized_identity', 'secret_version_reference']}
    if any(config.get(k) != v for k, v in expected.items()):
        return {'status': 'invalid_config', 'resolved': config}
    results = [NotificationResponseSimulator(config).evidence(r) for r in budget_replay_rows]
    return {'resolved': config, 'fixtures': results, 'limitation': policy['residual_limitation']}

supplied_stop_config = {'workload_scope': policy['workload_scope'], 'budget_amount': policy['budget_amount'], 'period': policy['period'], 'threshold_ratio': policy['threshold_ratio'], 'notification_topic': policy['notification_topic'], 'response_pipeline': policy['response_pipeline'], 'INSTANCE': policy['INSTANCE'], 'ZONE': policy['ZONE'], 'authorized_identity': policy['authorized_identity'], 'secret_version_reference': policy['secret_version_reference'], 'secretEnv': ['BUDGET_CLIENT'], 'event_binding': {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}, 'response_step': {'name': 'gcloud', 'args': ['compute', 'instances', 'stop', policy['INSTANCE'], '--zone=' + policy['ZONE']]}}

config = None

with open('guardrail.yaml', 'w') as h:
    yaml.safe_dump(config, h)

with open('guardrail.yaml') as h:
    resolved = yaml.safe_load(h)

inspected_scope = resolved['workload_scope']

inspected_target = [resolved['INSTANCE'], resolved['ZONE']]

inspected_binding = resolved['event_binding']

inspected_secret = [resolved['secret_version_reference'], resolved['secretEnv']]

assert resolved == config

result = apply_and_replay(resolved)

assert not result['fixtures'][0]['notification'] and result['fixtures'][0]['actions'] == []

assert all(r['stop_completed'] and r['target_only'] and r['authorized_response'] for r in result['fixtures'][1:])

assert all(r['credential_non_disclosure'] for r in result['fixtures'])

assert result['limitation'] == policy['residual_limitation']