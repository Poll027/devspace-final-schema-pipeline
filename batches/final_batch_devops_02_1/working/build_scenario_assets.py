import json, re
from pathlib import Path
B = Path('batches/final_batch_aws_devops.region.02_1')
g = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
bundles = {b['context']['concept_id']: b for b in g['bundles']}
text = '\n'.join(t['content'] for b in g['bundles'] for t in b['teaching_blocks']) + '\n' + '\n'.join(json.dumps(b[k]) for b in g['bundles'] for k in ['practice_anchor', 'visual_anchor', 'assessment_anchors'])
# Only terms actually present in the glossary teaching/anchor corpus are mined.
terms = ['FLEET_ALLOWED_INSTANCE_IDS', 'FLEET_MAX_TARGETS', 'two instance IDs', 'two targets', 'Python', 'Bash', 'environment variables', 'CloudFormation', 'CREATE', 'EC2', 'change set', 'replacement indicator', 'MFA', 'aws:MultiFactorAuthPresent', 'BoolIfExists', 'Deny', 'Allow', 'true', 'false', 'absent', 'Principal', 'Action', 'sts:AssumeRole', 'orders-operator', 'cross-account', 'root', 'access keys', 'non-root', 'CloudTrail', 'Region', '09:00', '09:15', 'eventTime', 'eventName', 'userIdentity', 'requestParameters', 'resources', 'Workload', 'orders', 'Cost Explorer', 'unallocated', 'log group', 'stream', 'JSON', 'request ID', 'outcome', 'timestamp', 'CloudWatch Logs Insights', 'rollback files', 'reload', 'restart', 'service status', 'effective-setting check', 'rolling', 'blue/green', 'canary', 'known-good version', 'metrics_collected', 'InstanceId', 'amazon-cloudwatch-agent-ctl', 'fetch-config', '-s', 'CloudWatch', 'EvaluationPeriods', 'DatapointsToAlarm', '3', '2', 'threshold', 'statistic', 'period', 'comparison operator', 'OK', 'ALARM', 'INSUFFICIENT_DATA', 'breaching', 'notBreaching', 'ignore', 'missing', 'zero']
assert all(t in text for t in terms), [t for t in terms if t not in text]
scenario_id = 'scenario.orders_sandbox'
r = {'schema_version': '1.0', 'kind': 'scenario_asset_registry', 'path_id': g['path_id'], 'batch_id': B.name,
     'scenarios': [{'scenario_id': scenario_id, 'name': 'Orders sandbox operations review', 'domain': 'AWS DevOps operations',
                    'summary': 'A fictional operations team reviews supplied evidence for the orders workload in a sandbox: bounded fleet targets, CloudFormation changes, identity and root protection, change attribution, cost allocation, logs, Linux configuration, delivery proposals, host telemetry and alarm evaluation. All records are authored, read-only exercise evidence; no AWS resources, credentials, shell or executable workspace are provisioned. Code, configuration and operation excerpts for non-table anchors are carried in lesson text, not executed.',
                    'glossary_example_vocab': terms}], 'assets': []}
def col(name, typ, role, description, **extra):
    return dict(name=name, type=typ, semantic_role=role, description=description, **extra)
def dataset(id, title, description, columns, rows):
    assert all(len(row) == len(columns) for row in rows)
    r['assets'].append(dict(asset_id=id, asset_kind='dataset', scenario_id=scenario_id, title=title,
                            description=description, columns=columns, rows=rows, provenance='authored'))
# Separate checklist items prevent MFA protection from masking access-key/routine-use problems.
root_rows = [
    ['mfa', 'MFA protection', 'root sign-in', 'MFA enabled', None, None, 'MFA protection confirmed independently of key hygiene'],
    ['routine-root', 'Routine identity use', 'root', 'Routine orders operation used root', None, None, 'Violation: use a non-root identity for routine tasks'],
    ['routine-nonroot', 'Routine identity use', 'orders-operator', 'Routine orders operation used a non-root identity', None, None, 'Non-root routine-use boundary satisfied'],
    ['key-obsolete', 'Root access-key hygiene', 'simulated-root-key-a', 'Existing simulated root access key', False, 'removed', 'No longer needed; simulated removal recorded'],
    ['key-needed', 'Root access-key hygiene', 'simulated-root-key-b', 'Existing simulated root access key', True, 'retained', 'Still marked needed in supplied evidence; not the obsolete-key removal case'],
    ['no-new-keys', 'Root access-key hygiene', 'root', 'No root access keys created during review', None, None, 'Review did not create root access keys']
]
dataset('ds.root_protection', 'Root-protection checklist evidence', 'Simulated review snapshot. MFA, routine-use and key findings are separate. Null key fields mean not applicable, not missing evidence. No actual root access or key material is included.', [
    col('record_id','string','identifier','Unique checklist record'),
    col('checklist_item','string','categorical','Protection check category'),
    col('identity_or_key','string','identifier','Identity or simulated key label; never a credential'),
    col('evidence','string','text','Supplied fictional observation'),
    col('key_remains_needed','boolean','categorical','Whether the simulated existing root key remains needed; null for non-key checks'),
    col('removal_status','string','categorical','Simulated removal status; null for non-key checks'),
    col('finding','string','text','Separate checklist finding')], root_rows)
# Alarm expected cells are derived rather than manually keyed.
alarm = bundles['aws_devops.configure_cloudwatch_alarm_evaluation_and_missing_data_behavior_from_supplied_signals_and_thresholds']
example = next(t['content'] for t in alarm['teaching_blocks'] if t['purpose'] == 'example')
evaluation_periods, datapoints = map(int, re.search(r'EvaluationPeriods to (\d+) and DatapointsToAlarm to (\d+)', example).groups())
states = re.search(r'has (OK), (ALARM) and (INSUFFICIENT_DATA) states', alarm['coverage']['required_facts'][0]['statement']).groups()
OK, ALARM, INSUFFICIENT = states
policy_outcomes = dict(re.findall(r'(breaching|notBreaching|missing) yields (ALARM|OK|INSUFFICIENT_DATA)', alarm['practice_anchor']['success']))
threshold = 60
cases = [([80,40,80], 'missing', OK), ([40,80,40], 'missing', ALARM), ([0,80,0], 'missing', ALARM)]
cases += [([None]*evaluation_periods, policy, ALARM) for policy in ['breaching','notBreaching','ignore','missing']]
rows = []
for i,(samples, policy, prior) in enumerate(cases,1):
    comparisons = [('missing' if x is None else ('above' if x > threshold else 'below' if x < threshold else 'equal')) for x in samples]
    breaches = sum(x is not None and x > threshold for x in samples)
    observed_count = sum(x is not None for x in samples)
    assert observed_count in (0, evaluation_periods) # No unsupported sparse-window rule.
    state = (ALARM if breaches >= datapoints else OK) if observed_count else (prior if policy == 'ignore' else policy_outcomes[policy])
    rows.append([i,'orders_host_signal','Average',60,'GreaterThanThreshold',threshold,evaluation_periods,datapoints,*samples,*comparisons,breaches,policy,prior,state])
columns = [col('window_id','integer','identifier','Comparative evaluation-window label, not a measurement',numeric_looking_label=True),
           col('metric','string','identifier','Fictional supplied host signal name'), col('statistic','string','categorical','Supplied statistic'),
           col('period_seconds','integer','numerical','Supplied period duration',unit='seconds'), col('comparison_operator','string','categorical','Supplied comparison operator'),
           col('threshold','number','numerical','Supplied threshold in exercise signal units',unit='exercise signal units'),
           col('EvaluationPeriods','integer','numerical','Number of evaluated periods'), col('DatapointsToAlarm','integer','numerical','Required breaching datapoint count')]
columns += [col(f'period_{i}_sample','number','numerical','Supplied sample; null is missing and zero is a real observation',unit='exercise signal units') for i in range(1,evaluation_periods+1)]
columns += [col(f'period_{i}_comparison','string','categorical','Threshold comparison or explicit missing marker') for i in range(1,evaluation_periods+1)]
columns += [col('breach_count','integer','numerical','Count of observed real samples above threshold; excludes gaps'),
            col('missing_data_policy','string','categorical','Configured policy; missing is the default'),
            col('prior_state','string','categorical','Supplied state before evaluation'), col('resulting_state','string','categorical','Computed state under taught complete/all-missing rules')]
dataset('ds.alarm_evaluation', 'Alarm windows and missing-data policies', 'Authored sample windows and computed outcomes. First window realizes the glossary above/below/above example. Complete windows include real zeros; all-missing windows compare each taught policy from the same prior state. These are independent supplied test windows, not a claim about sparse-data evaluation.', columns, rows)
# Cost report values are authored fictional billing inputs; no estimates or external facts.
# Aggregate billed amounts by actual category, never by similarity of resource names.
resource_evidence = [
    {'resource': 'orders-host-a', 'Workload': 'orders', 'amount': 24},
    {'resource': 'orders-host-b', 'Workload': 'orders', 'amount': 16},
    {'resource': 'support-host', 'Workload': 'support', 'amount': 12},
    {'resource': 'orders-untagged', 'Workload': None, 'amount': 8}]
cost_rows = []
for category in ['orders', 'support', 'unallocated']:
    evidence = [x for x in resource_evidence if (x['Workload'] or 'unallocated') == category]
    cost_rows.append(['2026-01-01','2026-02-01','Workload',True,category,sum(x['amount'] for x in evidence),
                      '; '.join(x['resource'] + ': Workload=' + (x['Workload'] or 'absent') for x in evidence),
                      'Investigate missing relevant active tag; do not assign by resource name' if category == 'unallocated' else 'Preserve allocated category'])
dataset('ds.workload_cost_allocation', 'Workload cost grouping with tag evidence', 'Fictional supplied monthly billing report grouped by the active Workload cost-allocation tag. Amounts use exercise currency units, not a real AWS price. Resource-tag evidence remains alongside its actual allocated or unallocated report category.', [
    col('period_start','date','datetime','Inclusive report start'), col('period_end','date','datetime','Exclusive report end'),
    col('grouping_tag_key','string','categorical','Selected cost-allocation grouping key'),
    col('cost_allocation_tag_active','boolean','categorical','Activation status for this report'),
    col('Workload','string','categorical','Reported billing category; unallocated means no allocation to an intended workload'),
    col('billed_amount','number','numerical','Computed sum of authored billed inputs in this category',unit='exercise currency units'),
    col('resource_tag_evidence','string','text','Resource-associated tag labels, including an orders-looking name with no relevant tag'),
    col('finding','string','text','Attribution finding without guessed redistribution')],cost_rows)
# Own stage checklist: coverage of mandatory tables, widths, roles, labels, scope, variants.
mandatory = [b for b in g['bundles'] if b['visual_anchor']['type'] in ['data_table','spreadsheet']]
assert len(mandatory) == 2
for a in r['assets']:
    assert len({c['name'] for c in a['columns']}) == len(a['columns'])
    for c in a['columns']:
        if c['semantic_role'] == 'numerical': assert c['type'] in ['integer','number']
        if c['semantic_role'] == 'datetime': assert c['type'] in ['date','datetime']
    for row in a['rows']:
        assert len(row) == len(a['columns'])
        for c,v in zip(a['columns'],row):
            if v is None: continue
            if c['type'] == 'string': assert isinstance(v,str)
            if c['type'] == 'boolean': assert isinstance(v,bool)
            if c['type'] in ['integer','number']: assert isinstance(v,(int,float)) and not isinstance(v,bool)
            if isinstance(v,str) and v.isdigit(): assert c.get('numeric_looking_label') is True
assert not any(a.get('variants') for a in r['assets']) # No planted issue/duplicate occurrence obligations.
assert len(rows[0]) == len(columns)
assert rows[0][-1] == ALARM and rows[2][-1] == OK
assert {row[-1] for row in rows} == set(states)
(B/'scenario_asset_registry.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'concepts': len(g['bundles']), 'scenarios': len(r['scenarios']), 'assets': [a['asset_id'] for a in r['assets']], 'rows':sum(len(a['rows']) for a in r['assets']), 'vocab_terms':len(terms), 'checklist':'PASS'},indent=2))
