import json,re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.05_1')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
scenario='scenario.audit_sandbox'
assets=[]
# All rows below are authored, fictional read-only evidence. No cloud resources or executable runtimes.
def add(suffix,title,cols,rows,concept):
    types={'id':('string','identifier'),'cat':('string','categorical'),'text':('string','text'),'label':('integer','identifier'),'n':('integer','numerical'),'bool':('boolean','categorical'),'dt':('datetime','datetime')}
    columns=[]
    for spec in cols.split('|'):
        name,kind=spec.split(':');t,role=types[kind]
        c={'name':name,'type':t,'semantic_role':role}
        if kind=='label':c['numeric_looking_label']=True
        columns.append(c)
    rows=[[int(v) if c.get('numeric_looking_label') and v is not None else v for c,v in zip(columns,r)] for r in rows]
    assets.append({'asset_id':'ds.'+suffix,'asset_kind':'dataset','scenario_id':scenario,'title':title,'description':'Authored fictional read-only evidence for '+g['bundles'][concept]['context']['concept_id']+'. These are supplied case observations, not real AWS measurements or live resources.','columns':columns,'rows':rows,'provenance':'authored','variants':[]})
account_a='111111111111';account_b='222222222222';account_c='333333333333'
root='arn:aws:s3:::audit-sandbox-a';obj=root+'/audit/event.json'
writer='audit-writer';reader='audit-reader';outsider='unapproved-reader'
add('guardduty_finding','Finding evidence and established triage procedure','finding_id:id|finding_type:cat|severity:cat|resource_identity:id|activity_start:dt|activity_end:dt|opened_at:dt|suspicious_activity_details:text|preserved_evidence:text|established_next_step:text',[
 ['finding-a','supplied suspicious-activity finding','severe','node A','2026-01-12T10:00:00Z','2026-01-12T10:05:00Z','2026-01-12T11:00:00Z','Supplied finding reports suspicious activity concerning node A; compromise is not established.','Retained finding-a with original activity timestamps and details.','Preserve evidence and escalate to the designated investigator under the supplied finding-type procedure.'],
 ['finding-b','supplied suspicious-activity finding','severe','node B','2026-01-12T10:10:00Z','2026-01-12T10:15:00Z','2026-01-12T11:05:00Z','Detailed activity evidence is incomplete.','Retained available finding-b evidence; missing detail explicitly recorded.','Preserve available evidence and escalate incomplete details under the supplied procedure; no destructive action.']],0)
add('audit_access','Scoped audit authorization and identity tests','principal:id|approval:cat|action:cat|resource_arn:id|bucket_policy_effect:cat|other_applicable_grants_and_denies:text|test_outcome:cat',[
 [writer,'approved writer','s3:PutObject',obj,'Allow','No other applicable grants or denies in this supplied case.','allowed'],
 [reader,'approved reader','s3:GetObject',obj,'Allow','No other applicable grants or denies in this supplied case.','allowed'],
 [outsider,'unapproved reader','s3:GetObject',obj,'Deny','Applicable explicit deny for this unapproved principal.','denied']],1)
add('audit_encryption','Object encryption and separate permission boundaries','case_id:id|object_arn:id|bucket_default_encryption:cat|bucket_default_key:id|object_encryption_metadata:cat|object_key:id|s3_GetObject:cat|kms_Decrypt:cat|read_outcome:cat|evidence_note:text',[
 ['kms-approved',obj,'SSE-KMS','audit-key','SSE-KMS','audit-key','allowed','allowed','success','Object metadata confirms supplied key.'],
 ['kms-denied',obj,'SSE-KMS','audit-key','SSE-KMS','audit-key','allowed','denied','failure','Object permission does not replace key-use authority.'],
 ['existing-s3',root+'/audit/older.json','SSE-KMS','audit-key','SSE-S3',None,'allowed','not required','success','Existing SSE-S3 object was not re-encrypted by the default change.']],2)
add('terraform_plan_review','Saved plan actions and supplied approval scope','plan_file:id|resource_identity:id|planned_action:cat|plan_marker:cat|approved_scope:bool|impact_criterion:text|review_decision:cat|supporting_evidence:text',[
 ['PLAN_FILE','aws_instance.addition','addition','+',True,'Addition is approved in this supplied case.','accept','Resource and addition match approved scope.'],
 ['PLAN_FILE','aws_instance.update','update','~',True,'In-place update is approved in this supplied case.','accept','Update is within supplied impact bounds.'],
 ['PLAN_FILE','aws_instance.replacement','replacement','-/+',False,'Destruction of this resource is not approved.','block','Replacement destroys and creates the affected resource.'],
 ['PLAN_FILE','aws_instance.deletion','deletion','-',False,'Deletion is outside approved scope.','block','Mandatory deletion case identified in saved plan; not executed.']],3)
add('fleet_preview','Wrapper proposed actions versus approved scope','target_id:id|proposed_action:cat|approved_action:cat|approved_target:bool|preview_mode:bool|mutation_enabled:bool|discrepancy:text',[
 ['node A','supplied fleet action','supplied fleet action',True,True,False,'none'],
 ['node B','supplied fleet action','supplied fleet action',True,True,False,'none'],
 ['node C','supplied fleet action',None,False,True,False,'Proposed target is outside the approved node A/node B scope.']],4)
add('ec2_dryrun','Supported EC2 permission-check outcomes','case_id:id|DryRun:bool|api_response:cat|permission_interpretation:cat|operation_executed:bool|later_success_guaranteed:bool',[
 ['permission-approved',True,'DryRunOperation','sufficient permission',False,False],
 ['permission-denied',True,'UnauthorizedOperation','insufficient permission',False,False]],4)
# These exact node names and outcome categories are extracted from the glossary example.
partial=g['bundles'][5]['teaching_blocks'][3]['content']
nodes=re.findall(r'node [ABC]',partial)
node_names=list(dict.fromkeys(nodes))
add('fleet_invocations','Per-target invocation results and supplied scoped follow-up','command_id:id|target_id:id|invocation_status:cat|output_evidence:text|outcome_category:cat|supplied_scoped_follow_up:text',[
 ['command-a',node_names[0],'Success','Supplied invocation output confirms completion.','successful','Keep completion recorded; exclude from repeat execution.'],
 ['command-a',node_names[1],'Failed','Supplied invocation output reports failure.','failed','Use the supplied follow-up scoped to node B; do not repeat successful targets.'],
 ['command-a',node_names[2],'Unresolved','No conclusive completion or failure output is available.','unresolved','Inspect invocation status and output further before selecting any repeat operation.']],5)
add('credential_outcomes','Expired session and mutation-outcome evidence','request_id:id|session_error:cat|original_mutation_outcome:cat|outcome_evidence:text|renewal_provider:text|credential_components:text|idempotency_supported:bool|supplied_token_reference:id|supplied_next_step:text',[
 ['request-completed','expired-session error','completed','Supplied outcome evidence records completion.','approved credential provider','Use newly authorized access key, secret key and session token together; no values shown.',True,'token-reference-a','Renew the approved session; do not repeat the completed mutation.'],
 ['request-unresolved','expired-session error','unresolved','Available evidence does not settle whether mutation took effect.','approved credential provider','Use newly authorized access key, secret key and session token together; no values shown.',True,'token-reference-b','Renew the approved session; inspect outcome before retrying and retain the supported token.']],6)
add('ecs_identity','ECS startup identity versus application identity','case_id:id|taskRoleArn:id|executionRoleArn:id|identity_used:id|operation:cat|scope:cat|result:cat',[
 ['startup-image','approved-application-role','approved-execution-role','approved-execution-role','pull image','startup','success'],
 ['startup-logs','approved-application-role','approved-execution-role','approved-execution-role','publish logs','startup','success'],
 ['app-allowed','approved-application-role','approved-execution-role','approved-application-role','supplied allowed application operation','application','success'],
 ['app-denied','approved-application-role','approved-execution-role','approved-application-role','supplied denied application operation','application','access denied']],7)
add('baseline_checks','Approved baseline per-control checkpoints','account_id:label|baseline_id:id|control_id:id|control_type:cat|supplied_configuration:text|deployment_result:cat|evaluation_result:cat|interpretation:text',[
 [account_a,'approved-baseline','supplied-preventive','preventive','Supplied action restriction unchanged.','deployed','restriction verified','Restricts the supplied action.'],
 [account_a,'approved-baseline','supplied-detective','detective','Supplied noncompliance-reporting configuration unchanged.','deployed','noncompliance reported','Reports noncompliance; this is not an action restriction.']],8)
add('eks_config_references','Bounded Pod-template references and safe consumer checks','deployment:id|container:id|image:id|reference_path:text|object_name:id|object_key:id|consuming_environment_variable:id|consumer_check:cat|secret_values_displayed:bool|observation:text',[
 ['audit-app','app','supplied-image','env.valueFrom.configMapKeyRef','audit-config','mode','APP_MODE','success',False,'Nonconfidential configuration consumed separately from image.'],
 ['audit-app','app','supplied-image','env.valueFrom.secretKeyRef','audit-secret','token','APP_TOKEN','success',False,'Secret consumption confirmed without returning the value; access control and storage protection remain required.'],
 ['audit-app','app','supplied-image','env.valueFrom.configMapKeyRef','audit-config','mode','APP_MODE','existing value retained',False,'After ConfigMap changes, already-running container environment does not update automatically.']],9)
add('pipeline_evidence','Artifact continuity, role authority and failed-action boundary','run_id:id|stage:cat|action_service:cat|input_artifact:id|output_artifact:id|source_revision:id|action_status:cat|service_role:id|trust_principal:id|required_action_permissions:cat|artifact_access_permissions:cat',[
 ['run-success','source','source action',None,'source-artifact','revision-a','succeeded','pipeline-role','codepipeline.amazonaws.com','approved supplied action permissions','approved supplied artifact access'],
 ['run-success','build','CodeBuild','source-artifact','build-artifact','revision-a','succeeded','pipeline-role','codepipeline.amazonaws.com','approved supplied action permissions','approved supplied artifact access'],
 ['run-success','deploy','CodeDeploy','build-artifact',None,'revision-a','succeeded','pipeline-role','codepipeline.amazonaws.com','approved supplied action permissions','approved supplied artifact access'],
 ['run-failure','source','source action',None,'source-artifact','revision-b','succeeded','pipeline-role','codepipeline.amazonaws.com','approved supplied action permissions','approved supplied artifact access'],
 ['run-failure','build','CodeBuild','source-artifact','build-artifact','revision-b','failed','pipeline-role','codepipeline.amazonaws.com','approved supplied action permissions','approved supplied artifact access'],
 ['run-failure','deploy','CodeDeploy','build-artifact',None,'revision-b','not progressed','pipeline-role','codepipeline.amazonaws.com','approved supplied action permissions','approved supplied artifact access']],10)
add('deployment_target_matrix','Separate approved deployment and unapproved absence checks','target_account:label|target_region:cat|approval_status:cat|named_role_profile:id|role_arn:id|source_profile:id|verified_caller_account:label|explicit_region:cat|stack_status:cat|stack_output_bucket_identity:id|observed_bucket_identity:id|observed_bucket_location:cat|absence_check_result:cat',[
 [account_a,'us-east-1','approved','sandbox-a','arn:aws:iam::'+account_a+':role/deployment','approved-source',account_a,'us-east-1','CREATE_COMPLETE','audit-sandbox-a','audit-sandbox-a','us-east-1','not applicable'],
 [account_b,'us-west-2','approved','sandbox-b','arn:aws:iam::'+account_b+':role/deployment','approved-source',account_b,'us-west-2','CREATE_COMPLETE','audit-sandbox-b','audit-sandbox-b','us-west-2','not applicable'],
 [account_c,'us-east-1','unapproved','read-only-check-c',None,'approved-source',account_c,'us-east-1','absent',None,None,None,'confirmed absent'],
 [account_a,'us-west-2','unapproved','read-only-check-a',None,'approved-source',account_a,'us-west-2','unknown',None,None,None,'access error; absence not established']],11)
add('connectivity_evidence','DNS, route association and directional network evidence','case_state:cat|endpoint:id|dns_result:id|intended_address:id|subnet:id|associated_route_table:id|matching_destination:text|route_target:id|route_target_usable:bool|protocol:cat|destination_port:n|request_allowance:cat|response_allowance:cat|failing_layer:cat|approved_correction:text|connection_result:cat',[
 ['before','audit-endpoint','192.0.2.10','192.0.2.10','subnet-a','route-table-a','192.0.2.10/32','supplied-route-target',True,'TCP',443,'allowed','denied','network ACL response direction','Apply the supplied response allowance only; leave DNS, route and unrelated controls unchanged.','failure'],
 ['after','audit-endpoint','192.0.2.10','192.0.2.10','subnet-a','route-table-a','192.0.2.10/32','supplied-route-target',True,'TCP',443,'allowed','allowed','none','Supplied response correction applied.','success']],12)
add('patch_task_results','Approved maintenance-window configuration and per-node results','task_id:id|target_id:id|approved_target:bool|execution_recipient:bool|patch_baseline:id|patch_document:id|patch_document_parameters:text|concurrency_limit:text|error_limit:text|execution_result:cat|patch_compliance:cat|follow_up:text',[
 ['window-task-a','node A',True,True,'supplied-baseline','supplied-patch-document','Supplied Install parameters unchanged.','supplied concurrency unchanged','supplied error limit unchanged','success','compliant','Recorded patched; no repeat requested.'],
 ['window-task-a','node B',True,True,'supplied-baseline','supplied-patch-document','Supplied Install parameters unchanged.','supplied concurrency unchanged','supplied error limit unchanged','failed','noncompliant','Requires supplied target-specific follow-up.']],13)
add('service_endpoint_evidence','Stable Service path, Pod selection and client evidence','service:id|service_address:id|selector:text|pod_id:id|pod_labels:text|selected:bool|service_port:n|targetPort:n|application_container_port:n|endpoint_evidence:text|client:id|client_result:cat',[
 ['audit-service','audit-service.sandbox','app=audit-app','audit-pod-a','app=audit-app',True,80,8080,8080,'EndpointSlice identifies audit-pod-a on target port 8080.','supplied-client','expected application response'],
 ['audit-service','audit-service.sandbox','app=audit-app','audit-pod-b','app=audit-app',True,80,8080,8080,'EndpointSlice identifies audit-pod-b on target port 8080.','supplied-client','expected application response'],
 ['audit-service','audit-service.sandbox','app=audit-app','other-pod','app=other-app',False,80,8080,8080,'Pod is not in the selected EndpointSlice.','supplied-client','not a selected destination']],14)
# Mine exact, reusable glossary vocabulary, not unsupported proper names.
source='\n'.join(t['content'] for b in g['bundles'] for t in b['teaching_blocks'])+'\n'+'\n'.join(json.dumps({k:b[k] for k in ('visual_anchor','practice_anchor')}) for b in g['bundles'])
terms=['GuardDuty','finding type','severity','affected resource','activity timestamps','suspicious activity','S3','bucket policy','bucket or object ARNs','approved writers','approved readers','s3:GetObject','s3:PutObject','kms:Decrypt','SSE-KMS','SSE-S3','KMS','terraform plan -out=PLAN_FILE','terraform show PLAN_FILE','EC2','addition','update','deletion','replacement','DryRunOperation','UnauthorizedOperation','preview mode','mutation','node A','node B','node C','successful','failed','unresolved','access key','secret key','session token','idempotency token','taskRoleArn','task execution role','preventive','detective','ConfigMap','Secret','envFrom.configMapRef','env.valueFrom.configMapKeyRef','env.valueFrom.secretKeyRef','base64','CodePipeline','CodeBuild','CodeDeploy','codepipeline.amazonaws.com','GitHub OIDC','source revision','CloudFormation','role_arn','source_profile','get-caller-identity','DNS','route-table association','network-ACL','Patch Manager','patch baselines','concurrency','error limits','Service','spec.selector','ports.port','ports.targetPort','EndpointSlices','Pod labels']
vocab=[t for t in terms if t in source]
vocab+=list(dict.fromkeys(re.findall(r'\b(?:env\w*|spec|ports)\.[\w.]+',source)))
vocab=list(dict.fromkeys(vocab))
registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':scenario,'name':'Audit sandbox operations review','summary':'A fictional operations team reviews supplied security, infrastructure and workload evidence for an audit application in isolated sandbox accounts. All identities, observations and outcomes are authored case material; no credentials or cloud resources are provisioned.','domain':'AWS sandbox operations and security auditing','glossary_example_vocab':vocab}],'assets':assets}
# Self-check the mistakes-to-avoid list: widths, types, roles, label traps, glossary coverage, and issue consistency.
for a in assets:
 for r in a['rows']:
  assert len(r)==len(a['columns']),a['asset_id']
  for c,v in zip(a['columns'],r):
   if v is None:continue
   assert (isinstance(v,str) if c['type'] in ('string','datetime') else type(v)==bool if c['type']=='boolean' else type(v)==int),(a['asset_id'],c,v)
   if isinstance(v,str) and v.isdigit():assert c.get('numeric_looking_label'),(a['asset_id'],c)
 assert not a['variants'] # No derived messy variants or planted issues; no duplicate occurrences to resolve.
assert len(set(a['asset_id'] for a in assets))==len(assets)
assert all(v in source for v in vocab)
assert all(any(b['context']['concept_id'] in a['description'] for a in assets) for b in g['bundles'])
assert not any(b['visual_anchor']['type'] in ('chart','plot') for b in g['bundles'])
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
print(json.dumps({'concepts':len(g['bundles']),'scenarios':1,'assets':len(assets),'rows':sum(len(a['rows']) for a in assets),'columns':sum(len(a['columns']) for a in assets),'vocabulary_terms':len(vocab),'asset_ids':[a['asset_id'] for a in assets]},indent=2))
