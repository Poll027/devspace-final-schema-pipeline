import json, re
from pathlib import Path
root=Path('batches/final_batch_aws_devops.region.05_1')
g=json.loads((root/'inputs/path_glossary_bundle.json').read_text())
# Only teaching blocks and anchors supply the example vocabulary.
texts=[]
for b in g['bundles']:
    texts += [t['content'] for t in b['teaching_blocks']]
    texts += [json.dumps(b[k],ensure_ascii=False) for k in ('practice_anchor','visual_anchor','assessment_anchors')]
text='\n'.join(texts)
candidates=['GuardDuty','finding type','severity','affected resource','activity timestamps','suspicious activity','S3','bucket policies','approved writers','approved readers','bucket or object ARNs','s3:GetObject','kms:Decrypt','SSE-KMS','SSE-S3','AWS KMS','Terraform','terraform plan -out=PLAN_FILE','terraform show PLAN_FILE','EC2','additions','updates','deletions','replacements','DryRun','DryRunOperation','UnauthorizedOperation','preview mode','mutation','node A','node B','node C','successful','failed','unresolved','access key','secret key','session token','idempotency token','ECS','taskRoleArn','task execution role','task role','preventive controls','detective controls','ConfigMap','Secret','Deployment','envFrom.configMapRef','env.valueFrom.configMapKeyRef','env.valueFrom.secretKeyRef','CodePipeline','CodeBuild','CodeDeploy','codepipeline.amazonaws.com','GitHub OIDC','source revision','artifact names','CloudFormation','account/Region','role_arn','source_profile','aws sts get-caller-identity --profile NAME','--region REGION','stack outputs','bucket identity','bucket location','DNS','route-table association','protocol/port','network ACLs','Patch Manager','patch baselines','maintenance-window task','concurrency','error limits','Service','spec.selector','ports.port','ports.targetPort','Pod labels','EndpointSlices','endpoints','supplied client']
vocab=[s for s in candidates if s.lower() in text.lower()]
scenario='scenario.sandbox_operations'
assets=[]
def col(name,typ='string',role='categorical',**kwargs):
    return dict(name=name,type=typ,semantic_role=role,**kwargs)
def dataset(aid,title,description,columns,rows):
    assets.append(dict(asset_id=aid,asset_kind='dataset',scenario_id=scenario,title=title,description='Fictional authored read-only evidence; no AWS resources are provisioned. '+description,columns=columns,rows=rows,provenance='authored'))
dataset('ds.fleet_invocations','Separate fleet invocation results','One command on the glossary\'s node A, node B and node C. Follow-up is the supplied bounded procedure, not a new remedial action.',[
 col('command_id',role='identifier'),col('target_id',role='identifier'),col('invocation_status'),col('output_evidence',role='text'),col('outcome_category'),col('supplied_follow_up',role='text')],[
 ['command-review','node A','Success','Successful output confirms completion.','successful','Retain completion evidence; exclude from repeat execution.'],
 ['command-review','node B','Failed','Invocation output reports failure.','failed','Retain failure evidence and use the supplied node B scoped follow-up.'],
 ['command-review','node C','Unresolved','Available invocation evidence does not establish completion or failure.','unresolved','Inspect further before assigning an outcome or considering repeat execution.']])
# Account identifiers are numeric-looking labels, never quantities.
accounts=[str(111111111111+i*111111111111) for i in range(3)]
regions=['us-east-1','us-west-2']
columns=[col('target_id',role='identifier'),col('account_id','integer',role='identifier',numeric_looking_label=True),col('region'),col('approved','boolean'),col('role_profile',role='identifier'),col('role_arn',role='identifier'),col('source_profile',role='identifier'),col('verified_caller_account','integer',role='identifier',numeric_looking_label=True),col('explicit_region'),col('stack_name',role='identifier'),col('stack_status'),col('stack_output_bucket',role='identifier'),col('observed_bucket_identity',role='identifier'),col('observed_bucket_location'),col('absence_check_result')]
rows=[]
for i,region in enumerate(regions):
    profile='sandbox-'+('east' if i==0 else 'west')
    bucket='sandbox-audit-'+accounts[i]+'-'+region
    rows.append(['approved-'+str(i+1),accounts[i],region,True,profile,'arn:aws:iam::'+accounts[i]+':role/SandboxDeployment','sandbox-source',accounts[i],region,'sandbox-audit','CREATE_COMPLETE',bucket,bucket,region,'not applicable: approved deployment'])
for i,region in enumerate(regions):
    rows.append(['unapproved-'+str(i+1),accounts[2],region,False,None,None,None,None,None,'sandbox-audit','ABSENT',None,None,None,'confirmed absent'])
for row in rows:
    for index in (1,7):
        if row[index] is not None: row[index]=int(row[index])
dataset('ds.account_region_deployments','Per-target CloudFormation S3 evidence','Exactly two approved account/Region pairs and two supplied unapproved targets. The approved rows retain independent caller, stack output and observed bucket evidence; unapproved absence is a successful check, not an access error.',columns,rows)
dataset('ds.audit_access_tests','Audit object authorization checks','Scoped policy statements and the three required authorization tests. The approved write/read succeed and the unapproved read is denied; encryption and retention are not authorization evidence.',[
 col('test_id',role='identifier'),col('principal',role='identifier'),col('requested_action'),col('resource_arn',role='identifier'),col('scoped_policy_statement',role='text'),col('other_grants_and_denies_review',role='text'),col('observed_result')],[
 ['approved-write','audit-writer','s3:PutObject','arn:aws:s3:::sandbox-audit/audit/record.json','Allow audit-writer s3:PutObject on arn:aws:s3:::sandbox-audit/audit/* only.','Applicable grants and denies reviewed for this request.','allowed'],
 ['approved-read','audit-reader','s3:GetObject','arn:aws:s3:::sandbox-audit/audit/record.json','Allow audit-reader s3:GetObject on arn:aws:s3:::sandbox-audit/audit/* only.','Applicable grants and denies reviewed for this request.','allowed'],
 ['unapproved-read','unapproved-reader','s3:GetObject','arn:aws:s3:::sandbox-audit/audit/record.json','No grant to unapproved-reader in the supplied scoped policy.','Applicable grants and denies reviewed; no applicable permission permits this read.','denied']])
dataset('ds.wrapper_preview','Wrapper preview versus approved scope','Preview and scope evidence remain distinct from EC2 DryRun permission checks. No mutation is enabled.',[
 col('target_id',role='identifier'),col('proposed_action'),col('approved_target','boolean'),col('approved_action'),col('preview_mode','boolean'),col('mutation_enabled','boolean')],[
 ['node A','supplied fleet operation',True,'supplied fleet operation',True,False],
 ['node B','supplied fleet operation',True,'supplied fleet operation',True,False],
 ['node C','supplied fleet operation',False,None,True,False]])
dataset('ds.ec2_dryrun_evidence','Supported EC2 DryRun permission outcomes','These supplied cases are permission checks only. Neither result is an execution result or a guarantee of later operation success.',[
 col('case_id',role='identifier'),col('operation',role='text'),col('dry_run','boolean'),col('response_code'),col('permission_evidence',role='text'),col('operation_executed','boolean'),col('later_success_guaranteed','boolean')],[
 ['permission-sufficient','Supplied EC2 operation that supports DryRun',True,'DryRunOperation','sufficient permission',False,False],
 ['permission-insufficient','Supplied EC2 operation that supports DryRun',True,'UnauthorizedOperation','insufficient permission',False,False]])
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=g['path_id'],batch_id=g['batch_id'],scenarios=[dict(scenario_id=scenario,name='Sandbox operations review',summary='A fictional operations team reviews supplied read-only evidence for sandbox AWS changes, audit storage and bounded fleet operations. Learners inspect records and excerpts; no cloud service, shell, credentials or runtime is provisioned.',domain='AWS sandbox operations',glossary_example_vocab=vocab)],assets=assets)
# Self-check the mistakes list: widths, roles/types, labels, vocabulary, anchor coverage.
for a in assets:
    names=[c['name'] for c in a['columns']]
    assert len(names)==len(set(names))
    for row in a['rows']:
        assert len(row)==len(names),a['asset_id']
        for c,v in zip(a['columns'],row):
            if v is None: continue
            assert c['type']!='boolean' or type(v) is bool
            assert c['type']!='string' or isinstance(v,str)
            assert not(c['semantic_role']=='numerical' and c['type']=='string')
            if isinstance(v,str) and v.isdigit(): assert c.get('numeric_looking_label') is True
assert all(s.lower() in text.lower() for s in vocab)
assert [r[1] for r in assets[0]['rows']]==['node A','node B','node C']
assert sum(r[3] for r in assets[1]['rows'])==2
assert all(a['asset_kind']=='dataset' for a in assets)
(root/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
print('Mistakes checklist passed: widths, roles/types, digit labels, vocabulary, three-node outcomes, two approved deployments; no variants or runtime/plot assets required.')
print('Assets:',len(assets),'Rows:',sum(len(a['rows']) for a in assets),'Vocabulary:',len(vocab))
