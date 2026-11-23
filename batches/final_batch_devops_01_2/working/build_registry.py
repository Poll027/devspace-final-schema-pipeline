import json
from pathlib import Path

batch = Path(__file__).resolve().parents[1]
glossary = json.loads((batch / 'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/aws_devops_engineer.json').read_text())
bundles = glossary['bundles']
assert all(b['context']['concept_id'] in profile['practice_type_by_concept'] for b in bundles)
# Mine only teaching text and anchors, preserving the glossary's exact vocabulary.
def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from strings(v)
    elif isinstance(x, list):
        for v in x: yield from strings(v)
text = '\n'.join(s for b in bundles for k in ('teaching_blocks', 'practice_anchor', 'visual_anchor') for s in strings(b[k]))
terms = ['EC2', 'AMI', 'instance type', 'subnet', 'IAM instance profile', 'IAM role', 'temporary credentials', 'instance ID', 'running', 'lifecycle state', 'status checks', 'S3', 'data and metadata', 'object key', 'bucket', 'orders-release.zip', 'releases/orders-release.zip', 'LOCAL_FILE', 'BUCKET', 'KEY', '--profile NAME', '--region REGION', 'aws s3 cp', 'upload', 'download', 'CloudWatch', 'orders', 'QueueDepth', 'Lab/Orders', 'Environment=sandbox', 'Environment=staging', 'Service=orders', 'put-metric-data', 'namespace', 'dimension combination']
vocab = [t for t in terms if t in text]
scenario_id = 'scenario.orders_sandbox'
registry = {
    'schema_version': '1.0', 'kind': 'scenario_asset_registry',
    'path_id': glossary['path_id'], 'batch_id': batch.name,
    'scenarios': [{
        'scenario_id': scenario_id, 'name': 'Orders sandbox operating evidence',
        'domain': 'AWS workload operations',
        'summary': 'A fictional orders workload team reviews supplied EC2 launch details, transfers orders-release.zip in an approved sandbox S3 bucket, and compares QueueDepth metric identities in Lab/Orders. All resource identifiers, locations, permissions evidence and values are authored exercise fixtures; no cloud resources or credentials are provisioned. Learners inspect the evidence rather than execute operations.',
        'glossary_example_vocab': vocab
    }], 'assets': []
}
def column(name, role, description, typ='string'):
    return {'name': name, 'type': typ, 'semantic_role': role, 'description': description}
def dataset(asset_id, title, description, columns, rows):
    registry['assets'].append({'asset_id': asset_id, 'asset_kind': 'dataset', 'scenario_id': scenario_id,
        'title': title, 'description': description, 'columns': columns, 'rows': rows, 'provenance': 'authored', 'variants': []})

ami = 'ami-0a000000000000001'
subnet = 'subnet-0b000000000000001'
instance = 'i-0c000000000000001'
instance_type = 't3.micro'
instance_profile = 'orders-sandbox-instance-profile'
role = 'orders-sandbox-instance-role'
dataset('ds.ec2_launch_evidence', 'Approved launch choices and observed EC2 details',
    'Read-only fictional launch evidence. The approved row is a request, not a second instance. Null instance ID, state and checks on that row mean not yet observed. The single created instance matches the supplied choices; running state and an impaired instance status check remain separate observations. No health diagnosis or role-policy configuration is implied.', [
    column('record', 'categorical', 'Approved request or observed instance details.'),
    column('instance_id', 'identifier', 'Created instance identifier; absent on the approved request.'),
    column('ami', 'identifier', 'Supplied approved initial software image identifier.'),
    column('instance_type', 'categorical', 'Supplied instance type selection.'),
    column('subnet', 'identifier', 'Supplied network-placement identifier.'),
    column('instance_profile', 'identifier', 'Supplied container attaching the IAM role to EC2.'),
    column('attached_role', 'identifier', 'IAM role contained in the supplied profile.'),
    column('lifecycle_state', 'categorical', 'Lifecycle evidence, not a health conclusion.'),
    column('system_status_check', 'categorical', 'Reported host health evidence.'),
    column('instance_status_check', 'categorical', 'Reported instance health evidence.')
], [
    ['approved', None, ami, instance_type, subnet, instance_profile, role, None, None, None],
    ['observed', instance, ami, instance_type, subnet, instance_profile, role, 'running', 'ok', 'impaired']
])

bucket = 'orders-sandbox-artifacts-lab'
region = 'us-east-1'
operator_profile = 'orders-sandbox-operator'
local_file = next(t for t in vocab if t == 'orders-release.zip')
key = next(t for t in vocab if t == 'releases/orders-release.zip')
s3_uri = f's3://{bucket}/{key}'
retrieved = 'retrieved/' + local_file
dataset('ds.s3_transfer_evidence', 'Supplied S3 transfer endpoints and verification evidence',
    'Read-only fictional transfer record. Bucket, operator profile and Region are supplied exercise labels, not provisioned resources or credentials. Caller access and artifact comparison are supplied evidence; no additional policy or comparison command is required.', [
    column('direction', 'categorical', 'Upload or download direction.'),
    column('bucket', 'identifier', 'Same approved bucket in both transfers.'),
    column('object_key', 'identifier', 'Key scoped within the bucket.'),
    column('source', 'text', 'Local path for upload; S3 URI for download.'),
    column('destination', 'text', 'S3 URI for upload; separate local path for download.'),
    column('operator_profile', 'identifier', 'Supplied operator profile label; not credentials.'),
    column('bucket_region', 'categorical', 'Verified location supplied in the exercise brief.'),
    column('caller_access_evidence', 'text', 'Supplied access evidence for this bucket/key.'),
    column('artifact_comparison_evidence', 'text', 'Supplied comparison evidence after retrieval; null before retrieval.')
], [
    ['upload', bucket, key, local_file, s3_uri, operator_profile, region, 'Caller can upload and retrieve the intended bucket/key.', None],
    ['download', bucket, key, s3_uri, retrieved, operator_profile, region, 'Caller can upload and retrieve the intended bucket/key.', 'Retrieved artifact matches the supplied orders-release.zip file.']
])

namespace = next(t for t in vocab if t == 'Lab/Orders')
metric = next(t for t in vocab if t == 'QueueDepth')
environment_sandbox = next(t for t in vocab if t == 'Environment=sandbox').split('=', 1)[1]
environment_staging = next(t for t in vocab if t == 'Environment=staging').split('=', 1)[1]
service = next(t for t in vocab if t == 'Service=orders').split('=', 1)[1]
dataset('ds.metric_identity_evidence', 'Published and queried QueueDepth identities',
    'Read-only fictional metric evidence with exactly the two published dimension combinations from the glossary. Values 7 and 3 are authored supplied publication values, not live observations or thresholds. Query rows record requested identities only, not query results. A null Service on the incomplete query means the dimension is omitted; it is not a third publication. Null values on query rows mean no observed value is asserted.', [
    column('record_id', 'identifier', 'Unique evidence record label.'),
    column('operation', 'categorical', 'Publication or query selection.'),
    column('namespace', 'identifier', 'Namespace component of metric identity.'),
    column('metric_name', 'identifier', 'Name component of metric identity.'),
    column('Environment', 'categorical', 'Environment dimension, sandbox or staging.'),
    column('Service', 'categorical', 'Service dimension; null only where query omits it.'),
    column('supplied_value', 'numerical', 'Authored value supplied for publication; queries have no asserted result.', 'integer')
], [
    ['publication.sandbox', 'publication', namespace, metric, environment_sandbox, service, 7],
    ['publication.staging', 'publication', namespace, metric, environment_staging, service, 3],
    ['query.sandbox', 'query', namespace, metric, environment_sandbox, service, None],
    ['query.staging', 'query', namespace, metric, environment_staging, service, None],
    ['query.omitted_service', 'query', namespace, metric, environment_sandbox, None, None]
])

# Stage mistakes-to-avoid checklist: widths, semantic types, labels, variants,
# duplicate occurrences, sufficient concept coverage, and vocabulary consistency.
assert len(registry['scenarios']) == 1
assert len(registry['assets']) == len(bundles)
for a in registry['assets']:
    names = [c['name'] for c in a['columns']]
    assert len(names) == len(set(names))
    assert all(len(r) == len(names) for r in a['rows'])
    assert not a['variants'] # No planted issues or duplicate-occurrence predicates required.
    for i, c in enumerate(a['columns']):
        assert c['semantic_role'] != 'numerical' or c['type'] in ('number', 'integer')
        for row in a['rows']:
            v = row[i]
            if v is None: continue
            if c['type'] == 'string': assert isinstance(v, str)
            if c['type'] == 'integer': assert type(v) is int
            if isinstance(v, str) and v.isdigit(): assert c.get('numeric_looking_label') is True
assert all(t in text for t in vocab)
assert all(a['asset_kind'] == 'dataset' for a in registry['assets'])
assert {tuple(r[4:6]) for r in registry['assets'][2]['rows'] if r[1] == 'publication'} == {(environment_sandbox, service), (environment_staging, service)}
assert local_file in text and key in text and namespace in text and metric in text
out = batch / 'scenario_asset_registry.json'
out.write_text(json.dumps(registry, indent=2) + '\n')
print(out)
print('Checklist PASS: three concepts covered; row widths/types/roles/vocabulary checked; no numeric-only labels, variants, planted issues, duplicate occurrences, executable workspaces or plot anchors.')
print('Scenarios:', len(registry['scenarios']), 'Assets:', len(registry['assets']), 'Rows:', sum(len(a['rows']) for a in registry['assets']))
