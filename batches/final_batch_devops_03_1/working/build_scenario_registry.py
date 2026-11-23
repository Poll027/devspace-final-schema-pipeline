import json
import re
from pathlib import Path

B = Path('batches/final_batch_aws_devops.region.03_1')
bundle = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles').joinpath(bundle['path_id'] + '.json').read_text())
scid = 'scenario.orders_operations'

# Mine source vocabulary, preserving source spellings; do not invent concrete
# AWS resource addresses, digest values, credentials, or command output.
source_parts = []
syntax = []
for concept in bundle['bundles']:
    source_parts.extend(t['content'] for t in concept['teaching_blocks'])
    source_parts.extend(json.dumps(concept[k], ensure_ascii=False) for k in ['visual_anchor', 'practice_anchor', 'assessment_anchors'])
    syntax.extend(concept['practice_anchor'].get('live_code', {}).get('allowed_syntax', []))
source = '\n'.join(source_parts)
candidates = [
    'Python', 'AWS', 'requirements.txt', 'ENV_DIR', 'Unix', 'AWS profile', 'Region',
    'python -m venv ENV_DIR', 'source ENV_DIR/bin/activate',
    'python -m pip install -r requirements.txt', 'python -m pip list',
    'AWS CLI', 'JSON', 'NextToken', '--starting-token', '--max-items', '--page-size',
    '--no-paginate', '--profile', '--region', '--output json',
    'restart', 'runbook', 'preconditions', 'expected results', 'escalation recipient',
    'EKS', 'Pod', 'Pending', 'Running', 'Succeeded', 'Failed', 'Unknown',
    'kubectl get pod NAME', 'kubectl describe pod NAME', 'kubectl logs NAME -c CONTAINER',
    'RDS', 'DB instance', 'identifier', 'engine', 'endpoint', 'data marker',
    'S3', 'releases/orders.zip', 'delete marker', 'noncurrent-version expiration',
    'ECR', 'Docker', 'REGISTRY/REPOSITORY:TAG', 'REGISTRY/REPOSITORY@sha256:DIGEST',
    'publisher', 'consumer', 'orders', 'rev-42', 'GitHub Actions', 'SHA256',
    'id-token: write', 'contents: read', 'attestations: write',
    'actions/attest@v4', 'subject-path', 'actions/upload-artifact@v4',
    'actions/download-artifact', 'gh attestation verify',
    'CloudFormation', 'Resources', 'Type', 'Properties', 'AWS::S3::Bucket', 'Ref', 'Outputs',
    'Secrets Manager', 'GetSecretValue', 'secretsmanager:GetSecretValue',
    'review handoff', 'baseline', 'after-change', 'success signal',
    'AWS Config', 'rule parameters', 'recorded configuration', 'noncompliant',
    'declared value A', 'current value B', 'UPDATE_ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_FAILED',
    'EC2', 'IAM', 'associate-iam-instance-profile', 'Modify IAM role', 'caller identity',
    'Pod Identity', 'serviceAccountName', 'namespace', 'service account', 'SDK',
    'OIDC', 'aud', 'sub', 'aws sts assume-role', '--role-arn', '--role-session-name',
    '--duration-seconds', 'access key ID', 'secret access key', 'session token', 'Expiration',
    'session ARN', 'identity-based policies', 'resource-based grants', 'explicit deny',
    'EventBridge', 'events.amazonaws.com', 'SNS', 'Lambda', 'execution role',
]
vocab = sorted(set([term for term in candidates if term in source] + syntax + re.findall(r'--[a-z]+(?:-[a-z]+)*', source)))


def col(name, role, description, typ='string', unit=None):
    result = dict(name=name, type=typ, semantic_role=role, description=description)
    if unit is not None:
        result['unit'] = unit
    return result


def dataset(aid, title, description, columns, rows):
    return dict(asset_id=aid, asset_kind='dataset', scenario_id=scid, title=title,
                description=description, columns=columns, rows=rows,
                provenance='authored', variants=[])

outcome = 'Orders service restart completed and the supplied health result checked.'
preconditions = 'Approved restart task; intended orders service identified; receiving operator has the established procedure and on-call owner information.'
stop = 'Stop routine execution if a precondition or any expected result is not satisfied; do not invent a recovery action.'
owner = 'Orders on-call operator'
runbook = dataset(
    'ds.orders_restart_runbook', 'Orders restart: operator handover',
    'Read-only fictional established procedure for a bounded restart. These authored rows are a teaching example, not instructions for a provisioned service. Every action has a checkable expected result and a stop/escalation path; no additional recovery action is authorized.',
    [col('action_order', 'numerical', 'Ordinal execution order, not a resource identifier.', 'integer'),
     col('outcome', 'text', 'Known operational outcome of the complete procedure.'),
     col('preconditions', 'text', 'Conditions required before beginning routine execution.'),
     col('approved_action', 'text', 'Action from this fictional established procedure.'),
     col('expected_result', 'text', 'Observable result to check before advancing.'),
     col('failure_handling', 'text', 'Bounded response if the expected result is absent.'),
     col('stop_condition', 'text', 'When routine execution must stop.'),
     col('escalation_recipient', 'categorical', 'Operational owner who takes over; not an individual person.')],
    [[1, outcome, preconditions,
      'Compare the task record with the intended service and approved restart procedure.',
      'Task record names the orders service and includes restart approval and owner information.',
      'Record the missing or mismatched precondition and escalate without restarting.', stop, owner],
     [2, outcome, preconditions,
      'Perform the single restart action specified by the approved procedure.',
      'The restart action reports completion for the intended orders service.',
      'Record the restart failure and escalate; do not repeat or substitute an action.', stop, owner],
     [3, outcome, preconditions,
      'Inspect the supplied service health result and compare it with the procedure\'s expected healthy result.',
      'The supplied health result matches the expected healthy result for the orders service.',
      'Preserve the health-check result and escalate; restart completion alone does not close the task.', stop, owner],
     [4, outcome, preconditions,
      'Hand over the task record, action outcomes and checked health result to the receiving operator.',
      'The receiving operator has the ordered action results and the checked health result.',
      'Record the handover gap and escalate without claiming the task is handed over.', stop, owner]])

handoff = dataset(
    'ds.orders_review_handoff', 'Orders delivery: review-handoff evidence',
    'Read-only authored fictional comparison records. Minutes are illustrative measured values, not glossary-prescribed targets or real-world findings. Each row keeps the same measure before and after one bounded handoff change. The three separate cases permit improved, unchanged and worsened judgments without implying that the change always works.',
    [col('case_id', 'identifier', 'Distinct fictional comparison case; not a quantity.'),
     col('review_handoff_evidence', 'text', 'Supplied observation supporting the selected bottleneck.'),
     col('selected_bottleneck', 'categorical', 'Delivery stage supported by the observation.'),
     col('bounded_change', 'text', 'One change scoped only to the review handoff.'),
     col('success_signal', 'text', 'Identical measure used in both observations.'),
     col('expected_outcome', 'text', 'Direction of the intended measurable outcome; no invented numerical target.'),
     col('baseline_minutes', 'numerical', 'Observed baseline for the named success signal.', 'number', 'minutes'),
     col('after_change_minutes', 'numerical', 'Observed after-change value for the same success signal.', 'number', 'minutes')],
    [[case_id,
      'Delivery record identifies waiting for a review handoff as the measured bottleneck.',
      'Review handoff',
      'Name one receiving reviewer in the existing handoff record.',
      'Minutes from review-ready handoff to review start',
      'Reduce time waiting for review to start.', before, after]
     for case_id, before, after in [('handoff.improved', 40, 25), ('handoff.unchanged', 40, 40), ('handoff.worsened', 40, 55)]])

registry = dict(schema_version='1.0', kind='scenario_asset_registry',
                path_id=bundle['path_id'], batch_id=B.name,
                scenarios=[dict(scenario_id=scid, name='Orders sandbox operations',
                    summary='A fictional operations team inspects supplied evidence for its orders workload and hands over restart and delivery-review records. The orders release vocabulary, releases/orders.zip and rev-42 come from the glossary. AWS targets and identity contexts remain the supplied approved contexts; nothing is executed or provisioned. Authored table observations are fictional, not real-world facts.',
                    domain='AWS operations and delivery evidence', glossary_example_vocab=vocab)],
                assets=[runbook, handoff])
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')

# Stage mistakes-to-avoid checklist, run against the actual written artifact.
written = json.loads((B / 'scenario_asset_registry.json').read_text())
for asset in written['assets']:
    assert all(len(row) == len(asset['columns']) for row in asset['rows']), 'row width'
    for column in asset['columns']:
        if column['semantic_role'] == 'numerical':
            assert column['type'] in ('integer', 'number'), 'contradictory role/type'
        elif column['semantic_role'] in ('identifier', 'categorical', 'text'):
            assert column['type'] == 'string', 'ambiguous role/type'
    assert not asset['variants'], 'No planted issues or duplicate occurrence claims are needed for inspect-and-judge tables.'
    for row in asset['rows']:
        for value, column in zip(row, asset['columns']):
            if column['type'] in ('integer', 'number'):
                assert isinstance(value, (int, float)) and not isinstance(value, bool)
            else:
                assert isinstance(value, str)
                if value.isdigit():
                    assert column.get('numeric_looking_label'), 'unmarked digits used as label'
assert len(runbook['rows']) >= 3 and len(handoff['rows']) >= 3, 'too small for later tiles'
assert all(term in source for term in vocab), 'vocabulary contradicts glossary'
mandatory_tables = [x['context']['concept_id'] for x in bundle['bundles'] if x['visual_anchor']['type'] in ('data_table', 'spreadsheet')]
assert mandatory_tables == [bundle['bundles'][i]['context']['concept_id'] for i in (2, 10)]
assert all(x['asset_kind'] == 'dataset' for x in written['assets']), 'no runtime for inspect-and-judge'
assert len(profile['practice_type_by_concept']) > 0
assert not any(x['visual_anchor']['type'] in ('chart', 'plot') for x in bundle['bundles'])
print('Checklist PASS: row widths, types/roles, label traps, no unverified planted issues or duplicates, sufficient table coverage, source-consistent vocabulary, no executable resources, no plot-dependent anchors.')
print(json.dumps(dict(concepts=len(bundle['bundles']), scenarios=len(written['scenarios']), assets=len(written['assets']), rows=sum(len(a['rows']) for a in written['assets']), asset_ids=[a['asset_id'] for a in written['assets']]), indent=2))
