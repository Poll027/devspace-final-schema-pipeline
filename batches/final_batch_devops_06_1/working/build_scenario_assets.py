import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

B = Path('batches/final_batch_aws_devops.region.06_1')
bundle = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
# Mine vocabulary only from the teaching text and anchors, not prerequisites.
texts = []
for concept in bundle['bundles']:
    texts.extend(t['content'] for t in concept['teaching_blocks'])
    texts.extend(json.dumps(concept[k], ensure_ascii=False) for k in
                 ['visual_anchor', 'practice_anchor', 'assessment_anchors'])
source_text = '\n'.join(texts)
candidates = [
    'unit', 'integration', 'promotion', 'TEST_COMMAND', 'UNIT_JOB', 'INTEGRATION_JOB',
    'needs', 'continue-on-error', 'GitHub Actions', 'git add FILES',
    'git commit -m', 'git push', 'pull request', 'saved plan', 'EC2',
    'Availability Zone', 'two-AZ', 'client-visible', 'abort criteria',
    'CloudFormation', 'S3', 'objects', 'object versions', 'delete markers',
    'retained resources', 'backup-read', 'recovery-resource', 'identity', 'expiry',
    'isolated account', 'network', 'production', 'stop conditions',
    'Automation', 'aws:approve', 'pending', 'rejected', 'stopped',
    'execution ID', 'acting role', 'targets', 'start/end times', 'step statuses',
    'inputs', 'outputs', 'failure information', 'CloudTrail', 'request identity',
    'aws cloudtrail validate-logs', '--trail-arn', '--start-time', '--end-time',
    '--region', '--account-id', 'signed digest files', 'hashes',
    'Object Lock', 'governance', 'compliance', 'retain-until date', 'root',
    'Terraform', 'backend', 'BUCKET', 'KEY', 'REGION', 'local-state bootstrap',
    'terraform init -migrate-state', 'create_before_destroy', 'prevent_destroy',
    'template', 'parameters', 'stack events', 'resource IDs', 'outputs',
    'Inspector', 'severity threshold', 'documented exception', 'scan-policy check',
    'CodePipeline', 'source action', 'build action', 'deployment action',
    'input artifact revision', 'service logs', 'system status checks',
    'instance checks', 'container state', 'exit status', 'health check',
    'Lambda', 'smoke check', 'deployed endpoint', 'PutJobSuccessResult',
    'PutJobFailureResult', 'job ID', 'zero', 'nonzero'
]
vocab = list(dict.fromkeys(v for v in candidates if v in source_text))
assert len(vocab) == len(set(vocab))
scenario_id = 'scenario.alder_delivery_recovery'

def col(name, typ='string', role='text', **extra):
    return dict(name=name, type=typ, semantic_role=role, **extra)

def dataset(asset_id, title, description, columns, rows):
    return dict(asset_id=asset_id, asset_kind='dataset', scenario_id=scenario_id,
                title=title, description=description, columns=columns, rows=rows,
                provenance='authored', variants=[])

def stamp(d):
    return d.isoformat().replace('+00:00', 'Z')

# Fictional authored evidence, not an execution transcript or deployed resources.
start = datetime(2026, 1, 10, 10, 0, tzinfo=timezone.utc)
run_id = 'alder-response-run-a'
role = 'alder-response-role'
bucket = 'alder-exercise-audit'
object_key = 'response/run-a.json'
version = 'audit-version-a'
target = f'{bucket}/{object_key}@{version}'
step_specs = [
    ('inspect_retention', 'GetObjectRetention', 'success', 'mode=COMPLIANCE; version=audit-version-a', None),
    ('read_audit', 'GetObject', 'success', 'audit evidence read', None),
    ('attempt_delete', 'DeleteObject', 'failed', None, 'AccessDenied; retained version not deleted'),
]
audit_rows = []
for i, (step, operation, status, output, failure) in enumerate(step_specs):
    t = start + timedelta(minutes=i)
    audit_rows.append([run_id, role, target, stamp(start), stamp(start + timedelta(minutes=len(step_specs))),
                       step, stamp(t), stamp(t + timedelta(seconds=20)), status,
                       f'bucket={bucket}; key={object_key}; version={version}', output, failure,
                       f'alder-request-{chr(97+i)}', role, operation, stamp(t + timedelta(seconds=1)),
                       target, 'success' if failure is None else 'AccessDenied'])
audit = dataset('ds.response_audit_evidence', 'Alder response run and attributed AWS requests',
    'Read-only fictional Automation and CloudTrail evidence for one run. Successful and failed steps are retained. Request identities, times and targets are explicitly recorded, not inferred from intended actions. No execution or credentials are provided.',
    [col('execution_id', role='identifier'), col('acting_role', role='identifier'),
     col('target_identity', role='identifier'), col('execution_start', 'datetime', 'datetime'),
     col('execution_end', 'datetime', 'datetime'), col('step_id', role='identifier'),
     col('step_start', 'datetime', 'datetime'), col('step_end', 'datetime', 'datetime'),
     col('step_status', role='categorical'), col('inputs'), col('outputs'), col('failure_information'),
     col('cloudtrail_request_id', role='identifier'), col('cloudtrail_request_identity', role='identifier'),
     col('cloudtrail_operation', role='categorical'), col('cloudtrail_event_time', 'datetime', 'datetime'),
     col('cloudtrail_target_identity', role='identifier'), col('cloudtrail_result', role='categorical')], audit_rows)

# The comparison dates and displayed outcomes are calculated, not hand-entered.
required_days = 30
required_end = start + timedelta(days=required_days)
retention_rows = []
retention_cases = [
    (version, 'COMPLIANCE', 'root', True, True),
    ('audit-version-b', 'GOVERNANCE', 'alder-retention-role', True, True),
    ('audit-version-c', 'GOVERNANCE', 'alder-retention-role', True, False),
    ('audit-version-d', 'GOVERNANCE', 'alder-response-role', False, True),
]
for ver, mode, actor, authorization, request in retention_cases:
    bypass = mode == 'GOVERNANCE' and authorization and request
    retention_rows.append([bucket, object_key, ver, mode, required_days,
                           stamp(start), stamp(required_end), stamp(start), mode, stamp(required_end),
                           required_end >= start + timedelta(days=required_days), actor, authorization, request,
                           'delete or shorten retention',
                           'permitted by retention mode' if bypass else 'prevented by retention mode'])
retention = dataset('ds.audit_object_retention', 'Version-specific audit retention and bypass comparison',
    'Read-only authored Object Lock comparison at the inspection time, within the supplied fictional 30-day required interval. The default policy is shown separately from each inspected version. Outcomes concern only retention-mode constraints, not a grant of overall deletion authority. No retention settings are applied.',
    [col('bucket', role='identifier'), col('object_key', role='identifier'), col('version_id', role='identifier'),
     col('supplied_default_mode', role='categorical'), col('supplied_default_duration_days', 'integer', 'numerical', unit='days'),
     col('required_retention_start', 'datetime', 'datetime'), col('required_retention_end', 'datetime', 'datetime'),
     col('inspection_time', 'datetime', 'datetime'), col('version_retention_mode', role='categorical'),
     col('retain_until', 'datetime', 'datetime'), col('covers_required_interval', 'boolean', 'categorical'),
     col('request_actor', role='identifier'), col('has_bypass_authorization', 'boolean', 'categorical'),
     col('bypass_requested', 'boolean', 'categorical'), col('proposed_operation', role='categorical'),
     col('retention_mode_outcome', role='categorical')], retention_rows)

registry = dict(schema_version='1.0', kind='scenario_asset_registry', path_id=bundle['path_id'],
                batch_id=B.name, scenarios=[dict(scenario_id=scenario_id, name='Alder delivery and recovery exercise',
                summary='A fictional team reviews delivery, response and isolated recovery evidence for the Alder service in an approved exercise boundary. The audit bucket and response run are authored read-only records. Workflow, CLI, Terraform and cloud excerpts are inspected as text; no live infrastructure, credentials or executable workspaces are provisioned. Production remains outside the exercise.',
                domain='AWS delivery, operational response and isolated recovery', glossary_example_vocab=vocab)],
                assets=[audit, retention])

# Stage-specific mistakes-to-avoid checks.
assert len(bundle['bundles']) == 17
assert all(v in source_text for v in vocab)
for a in registry['assets']:
    assert all(len(row) == len(a['columns']) for row in a['rows'])
    assert len({c['name'] for c in a['columns']}) == len(a['columns'])
    assert not a['variants']  # No messy variants, duplicate occurrences or planted predicates to validate.
    for j, c in enumerate(a['columns']):
        for row in a['rows']:
            v = row[j]
            if v is None: continue
            if c['type'] == 'integer': assert isinstance(v, int) and not isinstance(v, bool)
            if c['type'] == 'boolean': assert isinstance(v, bool)
            if c['type'] in ('string', 'datetime'): assert isinstance(v, str)
        if c['semantic_role'] == 'numerical': assert c['type'] in ('integer', 'number')
        if c['semantic_role'] == 'datetime': assert c['type'] in ('date', 'datetime')
        if c['type'] == 'string' and any(str(row[j]).isdigit() for row in a['rows']):
            c['numeric_looking_label'] = True
assert {b['visual_anchor']['type'] for b in bundle['bundles']} <= {'UI_state', 'annotated_screenshot', 'diagram', 'process_flow', 'data_table', 'comparison'}
assert sum(b['visual_anchor']['type'] == 'data_table' for b in bundle['bundles']) == len(registry['assets'])
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'scenarios': len(registry['scenarios']), 'concepts': len(bundle['bundles']),
                  'asset_ids': [a['asset_id'] for a in registry['assets']],
                  'rows': sum(len(a['rows']) for a in registry['assets']), 'vocabulary_terms': len(vocab)}))
