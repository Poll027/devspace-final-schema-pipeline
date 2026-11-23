import json, re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.03_1')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
texts=[]
for b in g['bundles']:
    texts.extend(t['content'] for t in b['teaching_blocks'])
    texts.append(json.dumps(b['visual_anchor'],ensure_ascii=False))
    texts.append(json.dumps(b['practice_anchor'],ensure_ascii=False))
text='\n'.join(texts)
# All vocabulary entries must be literal glossary spans, not invented labels.
candidates='''Python|AWS|virtual environment|ENV_DIR|requirements.txt|source ENV_DIR/bin/activate|python -m venv ENV_DIR|python -m pip install -r requirements.txt|python -m pip list|AWS profile|Region|AWS CLI|--profile|--region|--output json|--no-paginate|--page-size|--max-items|NextToken|--starting-token|inventory|restart task|preconditions|ordered actions|expected results|failure-handling|stop condition|escalation recipient|receiving operator|Pod|Pending|Running|Succeeded|Failed|Unknown|kubectl get pod NAME|kubectl describe pod NAME|kubectl logs NAME -c CONTAINER|RDS|DB instance identifier|engine|operational status|endpoint|data marker|describe-db-instances|S3|releases/orders.zip|delete marker|noncurrent-version expiration|recovery window|ECR|Docker|REGISTRY/REPOSITORY:TAG|REGISTRY/REPOSITORY@sha256:DIGEST|publisher|consumer|aws ecr get-login-password --region REGION|docker login --username AWS --password-stdin REGISTRY|orders release file|rev-42|SHA256|workflow run|artifact name|actions/attest@v4|subject-path|actions/upload-artifact@v4|actions/download-artifact|id-token: write|contents: read|attestations: write|gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME --format json|Resources|Type: AWS::S3::Bucket|Properties|Ref|Outputs|aws cloudformation validate-template --template-body file://TEMPLATE|stack events|stack outputs|live property|Secrets Manager|GetSecretValue|secretsmanager:GetSecretValue|runtime identity|safe success result|review handoff|bottleneck|bounded change|success signal|baseline|after-change|improved|remained unchanged|worsened|AWS Config|rule parameters|recorded configuration|evaluation result|remediation|escalation|declared value A|current value B|UPDATE_ROLLBACK_COMPLETE|UPDATE_ROLLBACK_FAILED|first failing resource event|failure reason|EC2|instance profile|IAM role|associate-iam-instance-profile|Modify IAM role|caller identity|allowed operation|denied operation|EKS Pod Identity|cluster|namespace|service account|serviceAccountName|Pod Identity agent|supported SDK credential chain|unassociated workload|GitHub Actions OIDC|IAM OIDC provider|aud|sub|repository/branch|temporary credentials|aws sts assume-role|--role-arn|--role-session-name|--duration-seconds|access key ID|secret access key|session token|Expiration|identity-based policies|session policies|resource-based grants|session ARN|explicit deny|EventBridge|events.amazonaws.com|execution role|SNS|Lambda|resource-based invocation permissions|event pattern'''.split('|')
vocab=[v for v in candidates if v in text]
# Include every glossary-provided command template, without reconstructing it.
for b in g['bundles']:
    for s in b['practice_anchor'].get('live_code',{}).get('allowed_syntax',[]):
        if s not in vocab: vocab.append(s)
sid='scenario.orders_operations'
def col(name,role='text',type='string',**kw):
    return dict(name=name,type=type,semantic_role=role,**kw)
assets=[]
assets.append(dict(asset_id='ds.restart_runbook',asset_kind='dataset',scenario_id=sid,title='Orders restart: receiving-operator runbook',description='Authored, read-only fictional established procedure for the supplied restart task. No command is executed. Expected results must be checked before advancing; no recovery action beyond stopping and escalation is authorized.',provenance='authored',columns=[
    col('step_order','numerical','integer',description='Execution sequence, not a resource identifier.'),
    col('outcome'),col('preconditions'),col('approved_action'),col('expected_result'),col('failure_handling'),col('stop_condition'),col('escalation_recipient','categorical',description='Fictional responsible operational role; not contact details.')],rows=[
    [1,'Orders service restarted and supplied health check successful','Restart is approved; receiving operator has the established procedure and owner record','Check approval and supplied procedure before beginning','Approval is present and the restart procedure and owner record are available','Do not begin; report the missing precondition','Approval, procedure or owner record is absent','Orders on-call operator'],
    [2,'Orders service restarted and supplied health check successful','Step 1 expected result is verified','Perform only the restart action in the supplied established procedure','Supplied restart-action result reports completion','Stop routine work and preserve the restart-action result for the owner','Restart action reports failure or its expected result cannot be checked','Orders on-call operator'],
    [3,'Orders service restarted and supplied health check successful','Step 2 expected result is verified','Inspect the supplied post-restart health-check result','Supplied health check reports success for the intended orders service','Stop and hand off the restart result and health-check evidence; no additional recovery action is authorized','Health check reports failure or does not identify the intended service','Orders on-call operator']]))
assets.append(dict(asset_id='ds.review_handoff_evidence',asset_kind='dataset',scenario_id=sid,title='Delivery review handoff: same-signal before/after evidence',description='Authored fictional delivery records, not AWS measurements. All stages use elapsed minutes over the same review window; only the review handoff receives a bounded change. Its success signal is lower review-handoff elapsed time, with no invented target. Edge variants preserve the same signal when the result is unchanged or worsens.',provenance='authored',columns=[
    col('stage','categorical'),col('evidence'),col('selected_bottleneck','categorical'),col('bounded_change'),col('success_signal'),col('baseline_minutes','numerical','number',unit='minutes'),col('after_change_minutes','numerical','number',unit='minutes'),col('desired_direction','categorical')],rows=[
    ['review handoff','Review handoff has the longest baseline elapsed time in these supplied delivery records','yes','Use one explicit receiving-reviewer handoff record for this review handoff','Elapsed minutes for the same delivery stage',40,25,'lower'],
    ['build','Build baseline elapsed time is shorter than review handoff','no','No change to this stage','Elapsed minutes for the same delivery stage',8,8,'lower'],
    ['publication','Publication baseline elapsed time is shorter than review handoff','no','No change to this stage','Elapsed minutes for the same delivery stage',4,4,'lower']],variants=[
    dict(variant_id='variant.review_unchanged',derived_from='ds.review_handoff_evidence',purpose='The bounded change is completed but the chosen success signal remains unchanged.',ops=[dict(op='set_cell',where={'stage':'review handoff'},column='after_change_minutes',value=40)]),
    dict(variant_id='variant.review_worsened',derived_from='ds.review_handoff_evidence',purpose='The bounded change is completed but the same chosen signal worsens; do not replace it with a more flattering measure.',ops=[dict(op='set_cell',where={'stage':'review handoff'},column='after_change_minutes',value=50)])]))
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=g['path_id'],batch_id=B.name,scenarios=[dict(scenario_id=sid,name='Orders sandbox operations and release handoff',domain='Fictional AWS operations and delivery',summary='An orders team reviews supplied sandbox operational evidence and a revision-based orders release. Operators inspect excerpts and records only: no AWS resources, credentials, cluster, Docker host or executable workspace is provisioned. The authored restart procedure and review-handoff records are shared read-only tables; other concepts can use their glossary command/configuration excerpts directly.',glossary_example_vocab=vocab)],assets=assets)
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
# Stage-specific mistakes-to-avoid audit.
assert len(g['bundles'])==19
assert all(v in text for v in vocab)
for a in assets:
    assert all(len(r)==len(a['columns']) for r in a['rows'])
    assert len(set(c['name'] for c in a['columns']))==len(a['columns'])
    for c in a['columns']:
        assert (c['semantic_role']=='numerical')==(c['type'] in ('integer','number'))
    for r in a['rows']:
        for c,v in zip(a['columns'],r):
            if c['type']=='string': assert isinstance(v,str)
            elif c['type']=='integer': assert isinstance(v,int)
            elif c['type']=='number': assert isinstance(v,(int,float))
    for variant in a.get('variants',[]):
        cols=[c['name'] for c in a['columns']]
        for op in variant['ops']:
            matches=[r for r in a['rows'] if all(r[cols.index(k)]==v for k,v in op['where'].items())]
            assert len(matches)==1 and op['column'] in cols
            assert op['value'] >= 0
assert all(a['asset_kind']=='dataset' for a in assets)
# No planted data-quality issues or duplicate rows; numeric columns are quantities.
assert all(len({json.dumps(r) for r in a['rows']})==len(a['rows']) for a in assets)
print('Checklist passed:',len(g['bundles']),'concepts;',len(vocab),'literal glossary vocabulary entries;',len(assets),'datasets;',sum(len(a['rows']) for a in assets),'base rows;',sum(len(a.get('variants',[])) for a in assets),'variants')
