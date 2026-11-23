import json
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.05_1')
plan=json.loads((B/'tile_plans.json').read_text())
screens=json.loads((B/'screens.json').read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
r=json.loads((B/'scenario_asset_registry.json').read_text())
concepts=g['bundles']; bycid={c['context']['concept_id']:c for c in concepts}
assets={a['asset_id']:a for a in r['assets']}
def rows(aid):
 a=assets[aid];return [dict(zip([c['name'] for c in a['columns']],row)) for row in a['rows']]
def excerpt(obj):
 if isinstance(obj,list) and obj and isinstance(obj[0],dict):
  obj={'columns':list(obj[0]),'rows':[list(x.values()) for x in obj]}
 return '```json\n'+json.dumps(obj,separators=(',', ':'))+'\n```'
# Choice content: prompt, correct, two misconception options, feedback for each.
checks={
0:[('A supplied GuardDuty finding is severe, but activity details are incomplete. The finding-type procedure says to preserve available evidence and escalate for investigation. Which next step is supported?',
'Preserve resource identity, activity timestamps and available finding details, then escalate under that procedure.',
'Destroy the resource because severity establishes compromise.',
'Replace the activity timestamps with the time the finding was opened and escalate.',
'The supplied procedure supports preserving evidence and escalation, not a compromise conclusion.',
'Severity alone is not supporting evidence for compromise or destructive action.',
'The investigation must retain the supplied activity timestamps, not the time someone opened the finding.')],
1:[('An audit bucket has encryption and retention enabled. Which test set verifies the authorization boundary for the intended object path?',
'An approved writer write, an approved reader read, and an unapproved identity read, recording identity, path and result.',
'Only inspect encryption and retention settings; no identity tests are needed.',
'Only test an approved reader; its success establishes that unapproved readers are denied.',
'The three identity-specific tests verify approved access and the denied boundary.',
'Encryption and retention are not authorization checks.',
'Approved read success does not establish the unapproved identity’s result.')],
2:[('For an object whose metadata confirms SSE-KMS, s3:GetObject is allowed but kms:Decrypt for its key is denied. Which read result is supported?',
'The read fails because both object permission and KMS key-use authority are required.',
'The read succeeds because s3:GetObject alone is sufficient for SSE-KMS.',
'The read succeeds because the bucket default was changed to SSE-S3 after this object was stored.',
'SSE-KMS reads require both s3:GetObject and kms:Decrypt authority.',
'Object permission does not substitute for KMS key-use authority.',
'Changing the bucket default does not re-encrypt existing objects; this object still has SSE-KMS metadata.')],
3:[('The supplied review criteria permit only an in-place update to the approved EC2 instance. terraform show of the saved plan includes deletion of that instance. Which review decision is supported without applying it?',
'Block the plan and cite the deletion as outside the permitted action and impact.',
'Accept because a deletion is an in-place update.',
'Apply the plan to determine whether the deletion is destructive before deciding.',
'The saved plan’s deletion conflicts with the supplied action and impact criteria.',
'A deletion is not an in-place update.',
'Plan review uses plan evidence and does not require destructive execution.')],
4:[('A supplied EC2 operation supports DryRun. With DryRun enabled, its response is DryRunOperation. What does this establish?',
'Sufficient permission for the checked operation, without executing it or guaranteeing later success.',
'The operation executed successfully.',
'Every later AWS service change has now been previewed and is guaranteed to succeed.',
'DryRunOperation is permission evidence, not an execution result.',
'The DryRun request checks permission without executing the operation.',
'This supported EC2 check is not a universal preview or a guarantee of later success.')],
5:[('A fleet command reports node A successful, node B failed with failure output, and node C unresolved. The supplied procedure routes failed targets alone for review and inspects unresolved targets further. Which follow-up preserves the evidence?',
'Exclude node A from repeat execution, retain node B’s failure and route B alone for review, and keep C unresolved pending inspection.',
'Rerun on all nodes because any failure invalidates every successful result.',
'Record node C as successful because the command has a successful node.',
'Per-target evidence supports separate outcomes and scoped follow-up.',
'A failure on B does not erase A’s successful invocation; blindly repeating successful targets is not supported.',
'C’s unresolved evidence does not establish success from A’s separate result.')],
6:[('A request made with temporary credentials returns an expired-session error. Which interpretation is supported?',
'The expired credentials are no longer usable; a newly authorized session is needed.',
'The expired credentials remain usable if the old access key is entered again.',
'The error establishes that broader permissions must be granted.',
'Temporary credentials stop being usable after expiration.',
'Re-entering an old access key does not renew an expired session.',
'Expiration calls for renewal through the approved provider, not a permissions change.')],
7:[('In an ECS task definition, which role supplies credentials for AWS calls made by the application container?',
'The application task role referenced by taskRoleArn.',
'The task execution role solely because it authorizes image pulling and log startup work.',
'Neither role; successful image pulling itself grants the application all AWS permissions.',
'Application AWS permissions come from the task role.',
'The execution role’s startup authority is distinct from application AWS permissions.',
'Startup success is not evidence of application authorization.')],
8:[('A baseline check reports noncompliance for a detective control. What interpretation is supported?',
'The detective control reports noncompliance; this report is not proof that an action was preventively blocked.',
'The report proves the requested action was blocked by the detective control.',
'Preventive controls and detective controls both only report noncompliance and never restrict actions.',
'Detective reports and preventive restrictions are different control results.',
'A noncompliance report is not itself evidence of preventive restriction.',
'Preventive controls restrict actions; detective controls report noncompliance.')],
9:[('A reviewer says a Secret’s base64 encoding makes further protection unnecessary. Which judgement is supported?',
'Incorrect: base64 is not encryption; access control and appropriate storage protection are still required.',
'Correct: base64 encoding replaces both access control and storage protection.',
'Correct if the consumer prints the decoded secret to verify it.',
'Encoding does not replace the Secret’s required protection.',
'Base64 is not encryption and does not eliminate protection requirements.',
'Consumer checks must not expose secret values; printing does not establish safe protection.'),
('A ConfigMap value changes after a container starts with ConfigMap-backed environment variables. Which claim is supported?',
'The change alone does not prove the already-running container’s environment updated; check actual consumer evidence.',
'The already-running container’s environment automatically reflects every ConfigMap change.',
'The ConfigMap object alone proves consumption, so no consumer evidence is relevant.',
'ConfigMap changes do not automatically update environment variables inside already-running containers.',
'The running environment does not automatically refresh from the ConfigMap change.',
'Object updates alone do not establish the actual running consumer’s environment.')],
10:[('In the supplied pipeline execution, CodeBuild fails and CodeDeploy depends on its build output. Which progression matches the operating model?',
'No normal progression to the dependent CodeDeploy action.',
'Normal deployment continues because the source action succeeded.',
'Normal deployment continues using any unrelated build output as evidence for the intended revision.',
'A failed action prevents normal progression to dependent actions.',
'Source success does not remove the failed build dependency.',
'An unrelated input is not evidence for the intended source revision, and failure blocks normal dependent progression.')],
11:[('Both approved targets have successful stacks. A supplied unapproved target’s stack check returns an access error. Which conclusion is justified?',
'Absence in that unapproved target remains unverified; the access error is not proof of no stack.',
'The access error confirms there is no stack in the unapproved target.',
'Approved-target success confirms absence in every unapproved target.',
'Absence requires a successful check, not a failure to inspect.',
'An access error does not establish stack absence.',
'Each supplied unapproved target needs its own absence evidence.')],
12:[('DNS and the intended endpoint are correct, and the associated route is usable. The stateless network ACL permits the request but denies required response traffic. Which layer remains blocked?',
'The response direction of the network ACL.',
'No layer: permitting the request automatically permits its response in a network ACL.',
'DNS, solely because the connection fails despite supplied correct resolution.',
'Stateless ACLs require separate request and response permissions.',
'Network ACLs do not automatically allow response traffic based on a permitted request.',
'The supplied DNS evidence localizes away from resolution; the response denial identifies the failure.')],
13:[('A maintenance-window summary says complete, but one approved node’s execution failed and its patch compliance is unresolved. Which record is supported?',
'That node requires follow-up; retain its execution and compliance evidence separately from patched nodes.',
'All nodes were patched because the window summary says complete.',
'Discard the per-node evidence and widen the next run to every node without reviewing approved bounds.',
'Per-node execution and compliance evidence determine follow-up.',
'The window summary does not replace per-node evidence.',
'Follow-up must preserve approved task bounds and target-specific evidence.')],
14:[('A Service object exists. Which additional evidence verifies that the intended Pods actually receive Service traffic?',
'EndpointSlice or endpoint evidence identifies intended Pods, and the supplied client gets the expected application response through the Service address.',
'The Service name alone matches the application name.',
'Only the declared Service port is present; no endpoint inspection or client test is needed.',
'Endpoint evidence plus the client result verifies the selected Pods receive traffic.',
'A Service name alone is not reachability evidence.',
'A port declaration alone does not verify selected endpoints and actual traffic.')]
}
# Hands-on inspect-and-judge: self-contained scope plus supplied excerpts.
# Each tuple is evidence text, supported judgement, and fact-grounded explanation.
hands={}
def H(i,p,items):hands[i]=(p,items)
H(0,'Read each triage record against the supplied finding and procedure. Decide whether it meets the evidence-preserving triage criterion. Finding: type=representative suspicious activity; severity=high; resource=node A; activity timestamps=10:00–10:05 UTC; opened=11:00 UTC; detail=unusual activity reported, mechanism not established. Procedure: preserve available finding evidence and escalate for investigation.',[
('Triage record: type=representative suspicious activity; severity=high; resource=node A; activity=10:00–10:05 UTC; unusual-activity details retained; finding evidence preserved. Next step=escalate for investigation; compromise not asserted; no destructive action.',True,'The record retains the affected resource, supplied activity timestamps and supporting details and follows the specified procedure.'),
('Triage record: same type, severity and resource; activity=11:00 UTC; details retained; evidence preserved; next step=escalate for investigation. No destructive action.',False,'The record substitutes opening time for the supplied activity timestamps, losing required investigation evidence.'),
('Triage record: type, severity, resource, activity timestamps and details retained; evidence preserved. Next step=destroy node A because high severity proves compromise.',False,'Severity alone does not prove compromise or justify destruction; the specified next step is investigation escalation.')])
audit=rows('ds.audit_access_tests')
H(1,'Read each audit authorization review. Decide whether its policy scope and identity-test evidence meet the stated boundary. Approved audit writers require only writing, approved audit readers only reading, on the intended audit object path. Inspect other applicable grants and denies; the approved write/read must succeed and the unapproved read must be denied.',[
('Review: only the supplied scoped statements apply; all other applicable grants and denies inspected, no broadening. Each test records identity, action, resource and result:\n'+excerpt(audit),True,'The scoped statements and reviewed grants/denies accompany all three required identity tests with the correct allowed/denied results.'),
('Review: policy grants every principal read access on the audit path. Approved write/read succeed and the unapproved read succeeds. Encryption and retention enabled; reviewer marks authorization boundary verified.',False,'An allowed unapproved read and broadened principals violate the boundary; encryption and retention do not replace authorization tests.'),
('Review: supplied scoped policy retained. Other applicable grants and denies were not inspected; only the approved read was tested. Encryption enabled; reviewer marks full authorization verification complete.',False,'The required grants/denies review and approved write and unapproved read evidence are missing.')])
H(2,'Read each encryption review and decide whether it correctly verifies both object and key authority. The supplied key is named audit-key; the required default and new object use that key. Existing objects must be judged from their metadata, not from a later bucket-default change.',[
('Default: SSE-KMS, key=audit-key. New object metadata: SSE-KMS, key=audit-key. Read tests: approved s3:GetObject + approved kms:Decrypt -> success; s3:GetObject allowed + KMS use denied -> failure. Review notes: SSE-S3 uses S3-managed keys, needs no KMS key-use authority; changing the default does not re-encrypt existing objects.',True,'The default, metadata and contrasting reads verify the supplied key and both required authorities while distinguishing SSE-S3 and existing objects.'),
('Default: SSE-KMS, key=audit-key. Object metadata: SSE-KMS, key=audit-key. Review predicts a successful read when s3:GetObject is allowed and KMS use is denied, because object access is sufficient.',False,'SSE-KMS reading requires both object permission and KMS key-use authority.'),
('Default changed to SSE-S3. Existing object metadata remains SSE-KMS, key=audit-key. Review says the object is now re-encrypted and no longer needs kms:Decrypt.',False,'Changing the bucket default does not re-encrypt this existing SSE-KMS object; its read still requires KMS authority.')])
H(3,'Read each saved-plan review and decide whether the action interpretation and accept/block decision meet the supplied scope. Preapproved scaffold evidence: EC2 node A provisioned successfully. Review criteria: allow only an in-place update to node A; block additions, replacements and deletions. Review plans must not be applied.',[
('Evidence: terraform plan -out=review.plan; terraform show review.plan. Cases: node A update in place -> accept; node B addition -> block (outside scope); node A replacement, destruction plus creation -> block (destructive impact); node A deletion -> block (mandatory deletion case). Every decision cites that saved-plan action/resource. No review plan applied.',True,'All four actions are identified with resource identity; replacement is destruction plus creation, deletion is reviewed, and decisions follow the supplied scope without destructive execution.'),
('Evidence: terraform show review.plan identifies node A replacement. Review: accept as an in-place update; no review plan applied.',False,'Replacement includes destruction and creation, so it violates the permitted in-place-only impact.'),
('Evidence: terraform show review.plan identifies node A deletion. Review: apply this plan to determine impact, then accept because node A is in scope.',False,'The permitted action excludes deletion, and destructive application is not needed for review.')])
preview=rows('ds.wrapper_preview')
H(4,'Read each preview review and decide whether its scope judgement and non-mutating settings are supported. Approved targets are exactly those marked approved_target=true in the supplied preview records; each must use its approved_action. Identify discrepancies without enabling mutation. Supplied preview:\n'+excerpt(preview),[
('Review:\n'+'\n'.join(f"{row['target_id']}, {row['proposed_action']}: "+('matches approved target/action' if row['approved_target'] and row['proposed_action']==row['approved_action'] else 'scope discrepancy') for row in preview)+'\npreview_mode remains true; mutation_enabled remains false.',True,'The review retains preview-only settings and records both matching scope and the unapproved-target discrepancy.'),
('Review: every proposed target is approved because the wrapper listed it. No discrepancy recorded; preview_mode=true; mutation_enabled=false.',False,'The supplied records include an unapproved target; appearing in a preview does not establish approval.'),
('Review: the unapproved target is correctly flagged, but mutation_enabled is changed to true to verify the preview.',False,'Preview verification must remain non-mutating; enabling mutation violates the practice criterion.')])
fleet=rows('ds.fleet_invocations')
H(5,'Read each fleet follow-up record and decide whether it preserves target-specific outcomes and the supplied scoped procedure. Invocation evidence and required follow-up:\n'+excerpt(fleet),[
('Record:\n'+'\n'.join(f"{row['target_id']}: {row['outcome_category']}; evidence: {row['output_evidence']} Follow-up: {row['supplied_follow_up']}" for row in fleet)+'\nNo fleet-wide rerun.',True,'All three outcomes and evidence are separately retained, with scoped follow-up and no repeat on successful A.'),
('Record: node A successful; node B failed; node C unresolved. Follow-up: rerun the entire operation on all three nodes to resolve B.',False,'A’s successful result must be preserved and excluded from repeat execution; B’s failure does not justify a fleet-wide rerun.'),
('Record: node A successful and excluded; node B failed and routed alone for review. Node C recorded successful because no final failure is visible.',False,'C’s evidence establishes neither completion nor failure, so it must remain unresolved pending inspection.')])
H(6,'Read each credential-renewal and retry record. Decide whether it uses the complete newly approved session without exposure or permission changes, checks operation outcome, and uses the supplied supported idempotency token when a retry is warranted. Provider: approved session provider. Case complete: evidence says the resource-changing operation completed. Case retry: supplied outcome evidence warrants retry and the operation supports the original idempotency token.',[
('Session record: approved provider issued new access key, secret key and session token; all three used together; values not displayed; permissions unchanged. Complete case: do not repeat. Retry case: outcome evidence checked, warranted retry uses the original supported idempotency token.',True,'The record renews the complete credential set safely and makes distinct outcome-aware retry decisions.'),
('Session record: new access key used with the old secret key and old session token; values not displayed. Complete case not repeated; retry case uses the original token.',False,'Renewal requires the new access key, secret key and session token together, not a mixed old/new set.'),
('Session record: approved new three-part session used without display or permission change. Complete case repeated to confirm success; retry case discards the original supported idempotency token.',False,'A known completed operation must not be repeated, and a warranted retry should use the supplied supported token to avoid duplicate effects.')])
H(7,'Read each ECS task-definition and application-test excerpt. Decide whether it uses the approved least-privilege application role, preserves the execution role, and verifies allowed and denied application operations. Approved task role=application-role; original execution role=startup-role. The supplied allowed operation is reading the audit object; the denied operation is writing it.',[
('Task definition: taskRoleArn=application-role; executionRoleArn=startup-role unchanged. Tests from the application container: approved audit read succeeds; denied audit write returns AccessDenied. Review attributes these AWS calls to the task role, not startup authority.',True,'The approved application role is assigned and tested in both directions while the startup role is unchanged.'),
('Task definition: taskRoleArn=startup-role; executionRoleArn=application-role. Review says successful image pulling proves application read/write authority; no application tests retained.',False,'Startup authority and application permissions are distinct; taskRoleArn must reference the approved application role, with allowed and denied application tests.'),
('Task definition: taskRoleArn=application-role; executionRoleArn=startup-role unchanged. Application read succeeds and the operation required to be denied also succeeds. Review marks least-privilege verification complete.',False,'The denied application operation must return access denial; its success contradicts the supplied boundary.')])
H(8,'Read each baseline result record. Decide whether it verifies the exact approved configuration and interprets every stated control correctly. Designated account=sandbox account. Approved configuration has exactly two controls: P (preventive restriction on the supplied disallowed action) and D (detective noncompliance report). No additional controls are approved.',[
('Applied approved configuration unchanged to sandbox account. P deployment result recorded; supplied disallowed action restricted. D evaluation result recorded: noncompliant, interpreted as a report rather than action blocking. Every stated control has its own result; no extra controls introduced.',True,'The exact approved baseline is applied and both controls have results interpreted according to preventive versus detective behavior.'),
('Applied approved configuration unchanged. P deployment and D noncompliant evaluation recorded. Review says D’s noncompliance result proves D preventively blocked the action.',False,'A detective noncompliance report is not evidence of preventive action restriction.'),
('Applied P plus an extra unapproved control. D omitted without an evaluation record. Review marks the approved baseline fully verified.',False,'The required D result is absent and an unapproved control was introduced; this is not verification of the exact stated baseline.')])
H(9,'Read each supplied Deployment excerpt and safe consumer result. Decide whether it references the intended nonconfidential ConfigMap and Secret names and keys and verifies consumption without revealing values. Required ConfigMap=sandbox-config, key=MODE; required Secret=sandbox-secret, key=TOKEN. Existing container image and name remain unchanged.',[
('Pod-template excerpt:\n```yaml\nenv:\n  - name: MODE\n    valueFrom:\n      configMapKeyRef:\n        name: sandbox-config\n        key: MODE\n  - name: TOKEN\n    valueFrom:\n      secretKeyRef:\n        name: sandbox-secret\n        key: TOKEN\n```\nSafe consumer check: configuration consumed=true; secret consumed=true; values not returned. Existing image/name unchanged; only intended references added.',True,'Both intended object/key references are correct, and the safe consumer check confirms consumption without exposure.'),
('Pod-template excerpt: MODE uses configMapKeyRef(name=sandbox-config,key=MODE); TOKEN uses secretKeyRef(name=other-secret,key=TOKEN). Check says the required sandbox-secret was not consumed; image/name unchanged.',False,'The Secret name does not match the supplied intended object, and the consumer check does not confirm required consumption.'),
('Pod-template excerpt: MODE and TOKEN reference the intended objects and keys. Consumer check prints the decoded TOKEN value to prove it was read.',False,'The consumer test must confirm consumption without printing secret values.')])
H(10,'Read each pipeline configuration and execution record. Decide whether it connects declared artifacts, verifies the service role and intended revision, and stops normal dependent progression in the failed-action case. Intended revision=revision-A; required source output=SourceArtifact; required build output=BuildArtifact. Supplied actions require build/deploy and artifact-access permission.',[
('Source(revision-A) output=SourceArtifact; CodeBuild input=SourceArtifact, output=BuildArtifact; CodeDeploy input=BuildArtifact. Selected service role trusts codepipeline.amazonaws.com and permits supplied build/deploy actions and artifact access. Successful execution traces revision-A through both artifacts to deployment. Separate failed CodeBuild case: dependent CodeDeploy does not progress normally.',True,'Artifact names connect, service trust and required permissions are present, revision evidence reaches deployment, and failed build blocks dependent progression.'),
('Source output=SourceArtifact; CodeBuild input=OtherArtifact, output=BuildArtifact; CodeDeploy input=BuildArtifact. Service trust and permissions valid. Deployment evidence belongs to revision-B; reviewer says stage names prove release of intended revision-A.',False,'The source/build artifact mismatch and different revision break evidence of intended source-to-deployment continuity.'),
('Artifact names all connect. Selected role trusts only GitHub OIDC, not codepipeline.amazonaws.com. Failed CodeBuild case: dependent CodeDeploy proceeds normally. Reviewer marks configuration verified.',False,'The CodePipeline service role needs its service trust and failure must stop normal dependent progression; GitHub OIDC does not substitute.')])
deploy=rows('ds.account_region_deployments')
H(11,'Read each deployment review and decide whether it verifies exactly both approved account/Region pairs and absence at every supplied unapproved target. All deployments use the same supplied S3 CloudFormation template. Inspect caller, profile, Region, stack outputs and bucket evidence in these supplied records:\n'+excerpt(deploy),[
('Review: for each approved pair, role_arn and source_profile from its named profile checked; aws sts get-caller-identity --profile NAME verifies the recorded caller. Stack created with that profile and explicit --region REGION using the same template. Both approved rows independently show successful stacks and matching output/observed bucket identities and approved locations. Every supplied unapproved target’s successful absence check confirms no stack.',True,'Both approved targets have independent caller, stack and bucket evidence; every supplied unapproved target has confirmed absence.'),
('Review: only the first approved row inspected. Its successful stack is used to conclude the second approved account/Region has the correct caller, bucket and location; no unapproved-target checks reviewed.',False,'One target cannot establish the other’s identity or outputs, and every supplied unapproved target also needs an absence check.'),
('Alternative review case: both approved rows verified, but one supplied unapproved target’s check returns AccessDenied. Reviewer records no stack there and marks every unapproved target’s absence confirmed.',False,'An access error is not proof of absence; that supplied unapproved target remains unverified.')])
H(12,'Read each connectivity diagnosis and correction record. Decide whether it localizes the seeded failure, makes only the approved correction, and confirms success by retesting. Supplied evidence: DNS resolves the intended endpoint; used subnet route association has a matching route to a usable target; required request protocol/port is permitted; stateless network ACL denies required response traffic. Approved correction: permit only that required response traffic.',[
('Diagnosis: response-direction ACL rule is the broken layer, based on correct DNS/endpoint, used route association and permitted request evidence. Applied only the approved response allowance; unrelated controls unchanged. Repeated the endpoint connection test: success.',True,'The failing response layer is identified from evidence, the correction is bounded, and the repeated connection test confirms success.'),
('Diagnosis: DNS is the broken layer because any timeout means failed resolution. Replaced unrelated routes; response ACL unchanged. No repeat connection test.',False,'The supplied resolution is correct and the response denial identifies the failure; unrelated changes and no retest do not meet the criterion.'),
('Diagnosis: response ACL denied. Applied only the approved response allowance. Review marks connection success without repeating the endpoint test.',False,'A correction record alone does not confirm connection success; the endpoint test must be repeated.')])
H(13,'Read each maintenance-window patch record. Decide whether it preserves the approved task configuration, compares recipients to approved target IDs and uses per-node execution and patch compliance to identify patched versus follow-up nodes. Supplied task: targets=node A,node B; document=approved patch document with its supplied install parameters; concurrency and error limits must remain as supplied.',[
('Task executed with the supplied targets, document parameters, concurrency and error limits unchanged. Recipients compared by ID: exactly node A,node B. Node A execution successful, compliance confirms patched. Node B execution failed, compliance unresolved; record B requires follow-up with both pieces of evidence retained.',True,'Approved bounds and recipient identities are verified, and each node’s execution/compliance evidence supports its separate outcome.'),
('Task used unchanged document parameters, concurrency and error limits but recipient IDs were node A,node C. Review says approved targets verified because the recipient count is two.',False,'Recipient count does not establish the approved target IDs; C replaces required B.'),
('Task targets and parameters unchanged; recipient IDs exactly node A,node B. Node B execution failed and compliance unresolved, but reviewer marks both patched from the complete window summary.',False,'Per-node B evidence does not establish patch completion; a window summary cannot replace execution and compliance results.')])
H(14,'Read each Service configuration and verification excerpt. Decide whether it supplies a stable endpoint, selects the intended Pods, maps the port correctly, and verifies actual application traffic. Intended Deployment Pods carry app=sandbox-app and listen on container port 8080. Supplied Service port=80. Supplied client’s expected response=application check passed.',[
('Service spec.selector: {app: sandbox-app}; ports: [{port: 80, targetPort: 8080}]. Applied Service provides a stable address for changing selected Pods. EndpointSlice evidence identifies the intended sandbox-app Pods. Client test through the Service address on port 80: application check passed.',True,'Selector and targetPort match the intended workload, endpoint evidence identifies its Pods and the client receives the expected response through the stable Service endpoint.'),
('Service spec.selector: {app: other-app}; ports: [{port: 80, targetPort: 8080}]. EndpointSlice identifies other-app Pods. Review marks the intended sandbox-app Pods selected because the Service name matches sandbox-app.',False,'Actual selector-to-label and endpoint evidence select other Pods; the Service name does not fix that mismatch.'),
('Service spec.selector: {app: sandbox-app}; ports: [{port: 80, targetPort: 80}]. Intended Pods listen on 8080. No endpoint inspection or client test retained; reviewer marks application traffic verified from the Service declaration.',False,'targetPort does not map to the supplied container port, and declarations alone do not establish traffic without endpoints and the client test.')])

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for tile in plan['tiles']:
 stiles=next(t for t in screens['tiles'] if t['tile_id']==tile['tile_id'])
 entries=[]; rem_count={}; checkn={}
 interactive=[s for s in tile['steps'] if s['type'] in ('check','hands_on')]
 for n,s in enumerate(interactive):
  cid=s['concept_ids'][0];c=bycid[cid];i=concepts.index(c)
  measures=[]
  for anch in s['anchors']:
   if '#assessment:' not in anch:continue
   cap=anch.split('#assessment:')[1]
   matches=[a for a in c['assessment_anchors'] if a['capability']==cap or ('-' in cap and a['capability'].startswith(cap.rsplit('-',1)[0]))]
   assert len(matches)==1,(cap,matches)
   a=matches[0];measures.append({'concept_id':cid,'capability':a['capability'],'fact_ids':a['fact_ids']})
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if n==0 else ('stretch' if n==len(interactive)-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors']}
  if s['type']=='check':
   j=checkn.get(cid,0);checkn[cid]=j+1
   prompt,good,bad1,bad2,fg,fb1,fb2=checks[i][j]
   # Rotate the answer position deterministically; ids/key follow the authored option metadata.
   opts=[(good,True,fg),(bad1,False,fb1),(bad2,False,fb2)];shift=(i+j)%3;opts=opts[shift:]+opts[:shift]
   ix['public']={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':f'o{k+1}','text':v[0]} for k,v in enumerate(opts)]}
   ix['grading']={'correct_option_ids':[f'o{k+1}' for k,v in enumerate(opts) if v[1]],'option_feedback':{f'o{k+1}':{'message':v[2]} for k,v in enumerate(opts)}}
   hints=['Identify what the supplied evidence establishes, rather than what a summary might suggest.']
   correct=fg;incorrect='Recheck the stated boundary against the evidence; the selected conclusion is not supported.'
  else:
   prompt,items=hands[i]
   # Keys for text-only inspect-and-judge are derived from authored evidence judgements, not invented asset ids.
   shift=i%len(items);items=items[shift:]+items[:shift]
   ix['public']={'prompt':prompt,'buckets':[{'bucket_id':'meets','label':'Meets the stated criterion'},{'bucket_id':'violates','label':'Violates the stated criterion'}],'items':[{'item_id':f'e{k+1}','text':x[0]} for k,x in enumerate(items)]}
   ix['grading']={'assignments':{f'e{k+1}':('meets' if x[1] else 'violates') for k,x in enumerate(items)},'item_feedback':{f'e{k+1}':{'message':x[2]} for k,x in enumerate(items)}}
   hints=['Compare the actual settings and recorded outcomes with every supplied requirement.','Separate an evidence-supported result from a claim based only on a label or summary.']
   correct='The judgements match the supplied evidence and the stated operational boundary.';incorrect='At least one excerpt misses or contradicts a stated requirement. Check its settings and evidence, not just its conclusion.'
  ix['feedback']={'correct':{'message':correct},'incorrect':{'message':incorrect},'hints':hints}
  rems=[x for x in stiles.get('remediation_steps',[]) if cid in x['concept_ids']]
  if rems:
   ordinal=rem_count.get(cid,0);rem_count[cid]=ordinal+1
   ix['feedback']['remediation_step_id']=rems[min(ordinal,len(rems)-1)]['step_id']
  entries.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('tiles',len(out['tiles']),'interactions',sum(len(t['interactions']) for t in out['tiles']))
