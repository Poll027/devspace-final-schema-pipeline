import json
from pathlib import Path

B = Path(__file__).resolve().parents[1]
g = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
text = '\n'.join(json.dumps({k: b.get(k) for k in ('teaching_blocks', 'practice_anchor', 'visual_anchor')}) for b in g['bundles'])
vocabulary = ['EC2', 'AMI', 'instance type', 'subnet', 'IAM instance profile', 'IAM role', 'temporary credentials', 'instance ID', 'running', 'status checks', 'S3', 'orders-release.zip', 'releases/orders-release.zip', 'LOCAL_FILE', 'BUCKET', 'KEY', '--profile', '--region', 'aws s3 cp', 'CloudWatch', 'QueueDepth', 'Lab/Orders', 'Environment=sandbox', 'Environment=staging', 'Service=orders', 'put-metric-data']
assert all(v in text for v in vocabulary)
scenario = 'scenario.orders_sandbox'

def col(name, typ, role, description):
    return dict(name=name, type=typ, semantic_role=role, description=description)
def dataset(id, title, description, columns, rows):
    return dict(asset_id=id, asset_kind='dataset', scenario_id=scenario, title=title, description=description, columns=columns, rows=rows, provenance='authored', variants=[])

assets = []
assets.append(dataset('ds.ec2_launch_evidence', 'Approved EC2 selections and observed details',
    'Fictional read-only lab record. Compare approved inputs with observed settings; the running lifecycle state and failed instance status check are separate observations. No EC2 resource or credentials are provisioned.',
    [col('record', 'string', 'categorical', 'Approved inputs or observed instance details.'),
     col('instance_id', 'string', 'identifier', 'Illustrative created resource ID; absent before launch.'),
     col('ami', 'string', 'identifier', 'Approved initial software image ID.'),
     col('instance_type', 'string', 'categorical', 'Supplied launch instance type.'),
     col('subnet', 'string', 'identifier', 'Supplied network placement ID.'),
     col('instance_profile', 'string', 'identifier', 'Supplied container attaching the role to EC2.'),
     col('attached_role', 'string', 'identifier', 'Role contained in the supplied instance profile.'),
     col('instance_state', 'string', 'categorical', 'Lifecycle state, not a health verdict.'),
     col('system_status_check', 'string', 'categorical', 'Reported host health evidence; absent before launch.'),
     col('instance_status_check', 'string', 'categorical', 'Reported instance health evidence; absent before launch.')],
    [['approved', None, 'ami-0123456789abcdef0', 't3.micro', 'subnet-0123456789abcdef0', 'orders-sandbox-profile', 'orders-sandbox-role', None, None, None],
     ['observed', 'i-0123456789abcdef0', 'ami-0123456789abcdef0', 't3.micro', 'subnet-0123456789abcdef0', 'orders-sandbox-profile', 'orders-sandbox-role', 'running', 'passed', 'failed']]))

bucket, profile, region = 'orders-sandbox-artifacts', 'orders-sandbox', 'us-east-1'
local = next(v for v in vocabulary if v == 'orders-release.zip')
key = next(v for v in vocabulary if v == 'releases/orders-release.zip')
s3_uri = f's3://{bucket}/{key}'
# These are authored transcript fixtures, not outputs of live cloud commands.
transfers = [('upload', local, s3_uri), ('download', s3_uri, 'retrieved/' + local)]
assets.append(dataset('ds.s3_transfer_evidence', 'S3 upload and retrieval evidence',
    'Fictional read-only transfer transcript. The bucket, profile and Region are supplied lab labels. Access and completion observations are authored fixtures, not a real AWS execution. Comparison is supplied only for retrieval.',
    [col('direction', 'string', 'categorical', 'Upload or download direction.'),
     col('bucket', 'string', 'identifier', 'Intended bucket containing the object.'),
     col('object_key', 'string', 'identifier', 'Object identity scoped within the bucket.'),
     col('operator_profile', 'string', 'identifier', 'Explicit supplied caller profile label; no credentials.'),
     col('bucket_region', 'string', 'categorical', 'Verified supplied bucket location.'),
     col('source', 'string', 'text', 'Local path or S3 reference serving as the source.'),
     col('destination', 'string', 'text', 'Local path or S3 reference serving as the destination.'),
     col('command', 'string', 'text', 'Read-only annotated-command material; not executable here.'),
     col('caller_access_evidence', 'string', 'text', 'Supplied evidence for this transfer direction.'),
     col('transfer_result', 'string', 'categorical', 'Authored observation of transfer completion.'),
     col('artifact_comparison', 'string', 'text', 'Supplied retrieval comparison; absent for upload.')],
    [[direction, bucket, key, profile, region, src, dst,
      f'aws s3 cp {src} {dst} --profile {profile} --region {region}',
      f'Supplied caller access permits {direction} of {key} in {bucket}.',
      'succeeded', f'Retrieved artifact matches {local}.' if direction == 'download' else None]
     for direction, src, dst in transfers]))

namespace = next(v for v in vocabulary if v == 'Lab/Orders')
metric = next(v for v in vocabulary if v == 'QueueDepth')
environments = [v.split('=', 1)[1] for v in vocabulary if v.startswith('Environment=')]
service = next(v.split('=', 1)[1] for v in vocabulary if v.startswith('Service='))
# Only the glossary's two published dimension combinations are present.
# Query records do not invent or assert a returned series/value.
assets.append(dataset('ds.metric_identity_evidence', 'Published and queried metric identities',
    'Fictional evidence for comparing complete metric identities. Values are authored supplied publications, not measured cloud data. A null Service means the query omits that dimension; query rows intentionally make no claim about returned values.',
    [col('record_id', 'string', 'identifier', 'Stable evidence record label.'),
     col('operation', 'string', 'categorical', 'Publication or query selection.'),
     col('namespace', 'string', 'identifier', 'Namespace component of metric identity.'),
     col('metric_name', 'string', 'identifier', 'Name component of metric identity.'),
     col('Environment', 'string', 'categorical', 'Environment dimension label.'),
     col('Service', 'string', 'categorical', 'Service dimension label, null when omitted from query.'),
     col('published_value', 'number', 'numerical', 'Authored supplied publication value; no value asserted for query records.')],
    [['published_sandbox', 'publication', namespace, metric, environments[0], service, 7],
     ['published_staging', 'publication', namespace, metric, environments[1], service, 12],
     ['query_complete', 'query', namespace, metric, environments[0], service, None],
     ['query_omitted_service', 'query', namespace, metric, environments[0], None, None]]))

registry = dict(schema_version='1.0', kind='scenario_asset_registry', path_id=g['path_id'], batch_id=B.name,
    scenarios=[dict(scenario_id=scenario, name='Orders sandbox operations', domain='AWS workload operations',
    summary='A fictional orders-workload operator reviews approved EC2 launch evidence, deployment-artifact transfers and complete CloudWatch metric identities. All records are authored read-only lab fixtures; no AWS resources, credentials or runtime are provided.',
    glossary_example_vocab=vocabulary)], assets=assets)

# Stage mistakes-to-avoid checklist: structural and semantic checks plus source coverage.
assert len({a['asset_id'] for a in assets}) == len(assets)
for a in assets:
    assert all(len(r) == len(a['columns']) for r in a['rows'])
    assert len({c['name'] for c in a['columns']}) == len(a['columns'])
    for c in a['columns']:
        if c['semantic_role'] == 'numerical': assert c['type'] in ('integer', 'number')
        if c['type'] in ('integer', 'number'): assert c['semantic_role'] == 'numerical'
        assert c['description']
    assert not a['variants'] # No planted issues or duplicate-occurrence claims to verify.
assert assets[0]['rows'][0][2:7] == assets[0]['rows'][1][2:7]
assert assets[0]['rows'][1][7:] == ['running', 'passed', 'failed']
assert all(r[2] == key and r[1] == bucket for r in assets[1]['rows'])
assert assets[2]['rows'][0][2:6] == assets[2]['rows'][2][2:6]
assert assets[2]['rows'][3][5] is None
assert {r[4] for r in assets[2]['rows']} == set(environments)
# No digits are used as labels in standalone numeric-label columns.
assert not any(isinstance(r[i], str) and r[i].isdigit() for a in assets for r in a['rows'] for i in range(len(a['columns'])))
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2) + '\n')
print(json.dumps({'concepts': len(g['bundles']), 'scenarios': len(registry['scenarios']), 'assets': len(assets), 'rows': sum(len(a['rows']) for a in assets), 'columns': sum(len(a['columns']) for a in assets), 'checklist': 'passed'}))
