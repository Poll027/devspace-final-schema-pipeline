import json
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.04_1')
p=json.loads((B/'tile_plans.json').read_text()); g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); s=json.loads((B/'screens.json').read_text()); registry=json.loads((B/'scenario_asset_registry.json').read_text())
assets={a['asset_id']:a for a in registry['assets']}
def records(a):
 d=assets[a]; return [dict(zip([c['name'] for c in d['columns']],r)) for r in d['rows']]
def evidence(a): return json.dumps(records(a),indent=2)
# Questions and misconception-based alternatives, authored only from glossary facts.
checks=[
('Phase logs show the supplied build commands succeeded, but the exported artifact has not been inspected. Which conclusion is justified?', 'Command success is known; intended artifact export still needs verification.', 'Successful commands prove the intended file was exported.', 'Artifact selection is irrelevant once commands succeed.', 'Artifact paths must match generated output, and the exported artifact must be inspected.'),
('A deployment used the intended revision and EC2 targets, but hook results and destination files have not been inspected. What is still needed?', 'Inspect hooks for that revision and compare target files with AppSpec destinations.', 'Nothing: selecting the revision proves destination files match.', 'Check only the application name; target file evidence is unnecessary.', 'Revision and target alignment does not replace hook and target-file verification.'),
('During a bounded target-tracking test, the metric remains above target while capacity is at its configured maximum. Which interpretation is valid?', 'The metric cannot cause capacity to exceed that maximum.', 'Target tracking must exceed the configured maximum to reach the metric target.', 'An above-target metric proves that the maximum setting is ignored.', 'Capacity cannot exceed the configured maximum even when the metric remains above target.'),
('A principal has repository pull permissions but no identity-policy authorization for ecr:GetAuthorizationToken. What does the repository policy alone establish?', 'Repository pull permission, not authorization for the authentication action.', 'Authorization for ecr:GetAuthorizationToken as well as pull.', 'Authentication is unnecessary whenever repository pull is granted.', 'ECR authentication requires ecr:GetAuthorizationToken through an identity policy.'),
('A lifecycle preview includes a digest still used by a deployed version. What should happen before applying the policy?', 'Revise selection to exclude the still-needed digest and preview again.', 'Apply unchanged because deployment automatically prevents expiry.', 'Skip digest comparison because lifecycle rules only affect unused images.', 'Deployed versions are not immune to lifecycle rules; exclude needed digests from eligible expiry.'),
('Every registered target in an ALB target group is unhealthy, yet requests reach those targets. Which interpretation matches the documented behavior?', 'The ALB fails open to those unhealthy targets; this does not prove health.', 'A response proves at least one registered target is healthy.', 'ALB routing to any unhealthy target is impossible in this situation.', 'When all registered targets are unhealthy, an ALB fails open to them.'),
('After the supplied retention policy is applied, an expired event remains physically visible. Which interpretation is valid?', 'Expiry marks events for deletion; physical deletion is not necessarily immediate.', 'Visible expired events prove the retention setting was not saved.', 'Retention requires every expired event to disappear immediately.', 'Expired events are marked for deletion; physical deletion typically takes up to 72 hours.'),
('A snapshot and its new restored DB instance are available. No recovery query has been run. Which verification is still needed?', 'Query the restored endpoint and compare the recovery marker with the expected marker.', 'Query only the source endpoint, since restoration overwrites the source.', 'Treat available status as proof that the expected recovery marker was returned.', 'Restoration creates a separate instance; verify the marker against its endpoint.'),
('Logs are being collected. Does that alone show an approved role can perform the intended reads while an unapproved principal cannot?', 'No; test both identities against the intended read operations and resource scopes.', 'Yes; collecting logs automatically grants reader access.', 'Yes; reader identity and resource scope do not affect log read authorization.', 'Collection does not grant reader access; IAM authorization and identity-specific tests are required.'),
('An ECS task definition is registered with the supplied settings, but no task has been run or inspected. Which verification remains?', 'Run it with the supplied cluster/network and inspect task status and container details.', 'Registration alone proves a task is running the intended image.', 'A task name alone proves its runtime settings match the specification.', 'The running task image and settings require task-status and container-detail evidence.'),
('An identity policy allows a specific request, but an applicable organization policy explicitly denies it. Which finding is decisive?', 'The applicable explicit deny takes precedence over the identity allow.', 'The identity allow overrides the organization deny.', 'The identity allow proves no other policy evidence needs inspection.', 'Applicable constraints beyond the identity policy matter, and explicit deny takes precedence.'),
('Which execution follows a supplied approved saved plan without generating a new plan?', 'terraform apply PLAN_FILE, using that supplied approved file.', 'terraform apply with no saved plan file, assuming it will reproduce the approval.', 'Generate a different plan and execute it under the old approval.', 'Applying the supplied saved plan executes its recorded changes; unplanned apply is not the approved file.'),
('A parent Run Command status is Success, but one approved node invocation is Failed. Which record is required?', 'Retain the command ID and each node status/output, including the failed invocation.', 'Record only parent Success and mark every node successful.', 'Drop the failed node from the record because parent status is authoritative.', 'Parent status does not replace per-node status and output checks.'),
('terraform validate returns a nonzero result in the supplied workflow. Which next action respects a blocking configuration gate?', 'Stop before apply, correct the invalid declaration and rerun validation.', 'Execute apply anyway because static validation is only advisory.', 'Treat a formatting pass as overriding the validation failure.', 'Nonzero validation must block apply; formatting and configuration validity are separate checks.')
]
# Pin each check to its planned capability rather than a different fact in the concept.
checks[1]=('The approved deployment is revision-A on approved-node-1, but the action selected revision-B on that target. Which verification conclusion is justified?', 'Target selection matches, but revision alignment fails; retain the mismatch.', 'The correct target alone proves the intended revision was selected.', 'An installed agent makes revision comparison unnecessary.', 'The deployment must use both the intended target set and the intended revision; the agent does not replace that comparison.')
checks[10]=('For this request, the only applicable allow requires environment=sandbox, but the request context is environment=production. All other applicable policies have been checked and impose no additional restriction. What explains the denial?', 'The allow condition is unsatisfied for this request context.', 'The operation name alone guarantees that the conditional allow applies.', 'Request context is irrelevant once a principal is named in an allow.', 'A diagnosis is tied to principal, operation, resource and context; an unsatisfied condition prevents the conditional allow from applying.')
checks[11]=('An approved saved plan has been applied. Which evidence verifies that the created EC2 instance matches the reviewed plan?', 'Inspect terraform show PLAN_FILE and compare the resulting resource identity and supported settings with the plan.', 'An apply completion message alone proves every resulting setting matches.', 'Using any saved plan file is enough; resulting resource inspection is unnecessary.', 'Inspect the reviewed plan and the resulting resource or outputs; retaining apply outcome alone is not a settings comparison.')
checks[13]=('terraform validate exits successfully, but terraform fmt -check exits nonzero because of noncanonical formatting. What does the formatting result establish?', 'A formatting failure, not by itself a configuration-validity failure; the additional formatting gate should block progression.', 'A formatting failure proves the configuration is syntactically invalid.', 'A formatting failure proves remote provider APIs will reject the resource.', 'fmt -check checks canonical formatting; validate checks syntax and internal consistency, and neither verifies remote API success.')
# Each item is a supplied excerpt plus a review decision, not a request to operate a cloud/runtime.
cases={}
def case(i,text,decision,ok,why): cases.setdefault(i,[]).append((text+'\nReviewer decision: '+decision,ok,why))
build='''version: 0.2
phases:
  build:
    commands:
      - mkdir -p dist
      - cp supplied-release.txt dist/release.txt
artifacts:
  base-directory: dist
  files: [release.txt]
Phase log: both supplied commands succeeded.
Generated: dist/release.txt
Export inspection: release.txt retained and matches generated file.'''
case(0,build,'Commands, output selection and export inspection meet the supplied requirement.',True,'The command list produces dist/release.txt, selected relative to dist and confirmed in the export.')
case(0,build.replace('files: [release.txt]','files: [other.txt]').replace('Export inspection: release.txt retained and matches generated file.','Export inspection: intended release.txt absent.'),'Accept as complete because phase commands succeeded.',False,'Successful commands do not repair selection of the wrong output file.')
case(0,build.replace('Phase log: both supplied commands succeeded.','Phase log: cp command failed.').replace('Export inspection: release.txt retained and matches generated file.','Export inspection: not performed.'),'Accept without phase or export follow-up.',False,'The supplied commands must succeed and the intended exported file must be verified.')
dep='''Approval: application delivery-api; group delivery-sandbox; target approved-node-1; revision revision-A; role delivery-deploy-role; agent installed.
Selected deployment: all approved values above.
appspec.yml: release.txt maps to /opt/delivery-api; AfterInstall uses scripts/check-release.sh.
revision-A on approved-node-1: AfterInstall succeeded; inspected /opt/delivery-api/release.txt matches revision-A.'''
case(1,dep,'Accept: selection, hook results and destination file all match.',True,'The intended revision and target are backed by hook and AppSpec destination evidence.')
case(1,dep.replace('Selected deployment: all approved values above.','Selected deployment: revision-B; all other approved values match.'),'Accept the deployment as the intended revision.',False,'The selected revision differs from the supplied revision even with the correct target.')
case(1,dep.replace('AfterInstall succeeded; inspected /opt/delivery-api/release.txt matches revision-A.','AfterInstall failed; inspected /opt/delivery-api/release.txt does not match revision-A.'),'Keep both failures as evidence and do not mark deployment completed.',True,'A failed hook and file mismatch must remain visible rather than count as completion.')
sc=records('ds.scaling_timeline'); last=sc[-1]
case(2,evidence('ds.scaling_timeline')+'\nSaved settings: match all supplied metric, target, warmup and min/desired/max values.','Accept configuration and bounded response; correlate activities with capacity, without assuming an exact response time.',all(r['minimum_capacity']<=r['resulting_capacity']<=r['maximum_capacity'] for r in sc),'The complete timeline links metric values, activities and capacity within the saved bounds.')
case(2,json.dumps(last),'Above-target metric means capacity must grow beyond maximum_capacity.',False,'Target tracking does not override the group maximum.')
case(2,evidence('ds.scaling_timeline')+'\nSaved settings: warmup differs from supplied instance_warmup_seconds.','Approve settings because capacity stayed in bounds.',False,'Bounded capacity is not proof that the saved warmup matches the approved configuration.')
repo=evidence('ds.repository_access_tests')+'\nPolicy review: only listed approved publishers/consumers receive their intended repository operations; no broader grants.'
case(3,repo,'Accept scoped grants and authentication, with successful publisher/consumer tests and denied unapproved pull.',all(r['expected_result']==r['observed_result'] for r in records('ds.repository_access_tests')),'The evidence separates identity authentication from repository grants and covers all three identities.')
case(3,repo,'Unapproved authentication means its repository pull should also be allowed.',False,'Authentication permission does not grant repository pull.')
case(3,repo+'\nProposed change: remove approved principals’ identity authorization for ecr:GetAuthorizationToken; keep repository grants.','Publisher and consumer authentication will still be authorized by the repository policy.',False,'Repository permissions alone do not grant ecr:GetAuthorizationToken.')
ret=evidence('ds.retention_preview')
case(4,ret+'\nApproved criteria match selection, rulePriority and action; this preview was inspected before application.','Accept: eligible old images expire and all deployed/still-needed digests are excluded.',all(not r['previewed_expiry'] for r in records('ds.retention_preview') if r['still_needed'] or r['deployed']),'Preview selection matches criteria and excludes every needed digest.')
needed=next(r for r in records('ds.retention_preview') if r['deployed'])
case(4,json.dumps(needed)+'\nAlternative proposed selection: all images older than age_threshold_days; preview now includes this deployed digest.','Apply unchanged because deployment protects the digest.',False,'A needed digest must be excluded from eligibility; deployment is not immunity.')
case(4,ret+'\nProposed policy changed after this preview; revised preview not inspected.','Apply the changed policy using the old preview as proof of safety.',False,'Preview the policy that will be applied and compare its eligible digests with needed versions.')
alb='''Supplied requirement: listener and forwarding rule to intended delivery-api target group; registered target protocol/port and backend health-check path/port/success codes.
Saved settings: all match the supplied requirement.
Endpoint test: intended backend response confirmed. Target health inspection: healthy; no failure reasons.'''
case(5,alb,'Accept routing and health settings; request and health evidence both support the result.',True,'Settings, endpoint result and health inspection agree; a response alone is not enough.')
case(5,alb.replace('Target health inspection: healthy; no failure reasons.','Target health inspection: every registered target unhealthy; reason: health-check path does not match backend.'),'A response proves healthy targets, so ignore the health-check mismatch.',False,'All-unhealthy fail-open can produce responses; health-check settings and reasons still matter.')
case(5,alb.replace('Saved settings: all match the supplied requirement.','Saved settings: forwarding rule selects a different target group.'),'Accept because the listener port matches.',False,'The forwarding rule must select the intended target group; port agreement alone is insufficient.')
logs='''Intended log group: /delivery-api/sandbox; supplied interval: 30 days.
put-retention-policy: applied 30 days to /delivery-api/sandbox.
Inspection: that log group retentionInDays=30.
Expired events: marked for deletion; physical deletion pending.'''
case(6,logs,'Accept the saved interval; pending physical deletion is not immediate-policy failure.',True,'The intended setting matches and expiry is distinguished from physical deletion.')
case(6,logs,'The visible expired events prove that retentionInDays must be wrong.',False,'Physical deletion typically takes up to 72 hours rather than necessarily occurring at expiry.')
case(6,logs.replace('that log group retentionInDays=30.','that log group has no retention policy (default indefinite).'),'Approve the supplied 30-day requirement.',False,'Indefinite default retention does not match the supplied bounded interval.')
rds='''Source: delivery-source, unchanged.
Manual snapshot: delivery-snapshot, source delivery-source, available.
Restore: delivery-restored, distinct identifier, available, supplied network settings used.
Connection: delivery-restored.example.invalid.
Supplied recovery query: expected marker-A; observed marker-A.'''
case(7,rds,'Accept recovery verification on the separate restored instance.',True,'Snapshot and restored availability, separate identity, network settings and restored-endpoint marker all agree.')
case(7,rds.replace('Connection: delivery-restored.example.invalid.','Connection: source endpoint only.'),'Accept marker verification for the restored instance.',False,'A source-endpoint query does not verify the restored endpoint.')
case(7,rds.replace('Restore: delivery-restored, distinct identifier, available, supplied network settings used.','Restore: delivery-restored, distinct identifier, still creating, supplied network settings used.').replace('Supplied recovery query: expected marker-A; observed marker-A.','Supplied recovery query: not run.'),'Available snapshot alone proves completed recovery.',False,'Wait for restored availability and verify the recovery marker on its endpoint.')
la=evidence('ds.log_access_tests')+'\nPolicy review: unnecessary broader grants removed; wildcard retained only for supplied operations that require it.'
case(8,la,'Accept approved-reader reads and unapproved denials with identity, operation and scope recorded.',all(r['observed_result']==r['expected_result'] for r in records('ds.log_access_tests')),'The complete test set distinguishes required wildcard scope from unnecessary broad grants.')
case(8,la,'Remove every wildcard resource scope even for the supplied wildcard-required operation.',False,'Some operations require resource scope *; keep it only where required.')
case(8,la+'\nProposed evidence replacement: logs collected successfully, read tests discarded.','Collection alone proves approved access and unapproved denial.',False,'Collection does not establish reader authorization; keep principal-specific read tests.')
ecs=evidence('ds.ecs_configuration_evidence')
case(9,ecs,'Accept registered and running settings as matching the supplied specification and prepared cluster/network.',all(records('ds.ecs_configuration_evidence')[0][k]==records('ds.ecs_configuration_evidence')[2][k] for k in ['name','image','containerPort','hostPort','cpu','memory','launch_type','cluster','network_configuration']),'The registered definition and observed task match the supplied image and runtime settings.')
case(9,json.dumps(records('ds.ecs_configuration_evidence')[:2],indent=2),'Registration proves the supplied task is running; omit task status and container inspection.',False,'Registration alone does not verify running task status, image or runtime settings.')
case(9,ecs+'\nAlternate task observation: image differs from the supplied specification; all other settings match.','Accept because CPU and memory match.',False,'Matching resources do not excuse a different image in the observed task.')
iam='''Request: delivery-log-reader; supplied read operation; supplied resource; environment=production.
Identity allow applies. Organization policy explicitly denies this operation/resource when environment=production.
Resource/session/boundary evidence: no additional restriction.
Approved correction: authorized sandbox context. Retest: same principal/operation/resource, environment=sandbox, allowed.'''
case(10,iam,'Identify decisive organization deny; accept only the approved context correction and this request-specific retest.',True,'The explicit deny dominates the allow; the bounded correction and same-request retest support success, not unrestricted access.')
case(10,'''Request: delivery-log-reader; supplied read operation; supplied resource; environment=sandbox.
Applicable identity policy: no allow for this operation/resource. Resource policy: no applicable allow. Session, boundary and organization evidence: no additional restriction or explicit deny.
Approval: add only the supplied allow for this principal, operation and resource. Retest: same request allowed.''','Diagnose missing applicable allow and accept the supplied narrow correction with retest.',True,'The evidence localizes missing allow for this specific request after other constraints are checked.')
case(10,'''Request: delivery-log-reader; supplied read operation; supplied resource; environment=production.
Only applicable allow requires environment=sandbox; condition not satisfied. All other applicable policies inspected: no additional restriction or deny.
Approval: use sandbox context. Retest: same principal/operation/resource with environment=sandbox allowed.''','Diagnose unsatisfied condition and accept only the supplied request-context correction.',True,'The condition fails for production and is satisfied by the approved sandbox retest.')
case(10,iam,'Add a broader identity allow to override the organization deny; omit retest.',False,'An identity allow cannot override explicit deny, and a correction needs a request-specific retest.')
plan=evidence('ds.reviewed_plan_comparison')
case(11,plan,'Accept approved saved-plan execution and retained outcome with AMI, type and placement comparison.',all(records('ds.reviewed_plan_comparison')[0][k]==records('ds.reviewed_plan_comparison')[1][k] for k in ['plan_file','AMI','instance_type','placement']),'The command applies the approved file and the resource evidence matches the reviewed settings.')
case(11,plan+'\nAlternate execution command: terraform apply (no PLAN_FILE).','Treat this alternate execution as execution of the approved saved plan.',False,'An apply without the saved file is not execution of that approved recorded plan.')
case(11,plan+'\nAlternate observed instance: placement differs from reviewed placement.','Accept because the apply command used the approved file.',False,'Retaining apply outcome is not enough; resulting instance settings must match the reviewed plan.')
cmd=evidence('ds.command_invocations')+'\nApproval/submission: supplied document, parameters and approved target set match; authorization confirmed. All approved targets are represented; none extra.'
case(12,cmd,'Accept scope and complete evidence, but flag the failed invocation rather than declaring all nodes successful.',any(r['invocation_status']=='Failed' for r in records('ds.command_invocations')),'The command ID, target comparison and each output are retained; parent Success does not erase a node failure.')
case(12,cmd,'Parent Success proves all approved targets succeeded; remove node-specific outputs.',False,'Each invocation status and output must be inspected and retained.')
case(12,cmd+'\nAlternate target submission: includes an extra unapproved node.','Accept target scope because all originally approved nodes are also included.',False,'Including approved nodes does not authorize extra targets; compare actual scope with approval.')
case(13,'''Workflow: init -backend=false, then blocking validate, then blocking fmt -check, then supplied approved apply.
Before correction: instance_typ argument; validate exit 1; apply not executed.
After supplied correction to instance_type: validate exit 0; fmt -check exit 0.
Approved apply outcome: one EC2 instance provisioned; result retained separately from static results.''','Accept the failed-to-corrected gate evidence and separate provisioning outcome.',True,'Initialization precedes blocking checks; invalid configuration stops apply, correction passes checks and provisioning has its own evidence.')
case(13,'''Workflow: init -backend=false; validate exit 1; continue-on-error: true; approved apply executed.''','Accept as a blocking validation gate.',False,'The nonzero validation result did not block apply.')
case(13,'''Workflow: init -backend=false; validate exit 0; fmt -check exit 1 due only to noncanonical spacing; apply blocked.
After terraform fmt: validate exit 0; fmt -check exit 0; apply not yet executed.''','The first failure is formatting-only; corrected static success does not prove provisioning.',True,'Canonical formatting is distinct from syntax/internal consistency and from remote provisioning success.')
case(13,'''Workflow: init -backend=false; validate exit 0; fmt -check exit 0; apply not executed.''','Declare one EC2 instance provisioned because static checks passed.',False,'Static checks do not verify remote state or provider API success; provisioning needs separate execution evidence.')

out={k:p[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
concept_index={x['context']['concept_id']:i for i,x in enumerate(g['bundles'])}
for tile in p['tiles']:
 st=next(t for t in s['tiles'] if t['tile_id']==tile['tile_id']); rem=st.get('remediation_steps',[]); seen=set(); entries=[]
 for step in tile['steps']:
  if step['type'] not in ['check','hands_on']:continue
  cid=step['concept_ids'][0]; i=concept_index[cid]; bundle=g['bundles'][i]; assessment={a['capability']:a for a in bundle['assessment_anchors']}
  measures=[dict(concept_id=cid,**assessment[a.split('#assessment:')[1]]) for a in step['anchors'] if '#assessment:' in a]
  ix={'type':step['planned_interaction_type'],'interaction_id':'ix.'+step['step_id'],'difficulty':'intro' if step['type']=='check' and not seen else ('stretch' if step['type']=='hands_on' else 'core'),'grading_mode':'client','standalone':True,'anchors':step['anchors'],'measures':measures}
  if step['type']=='check':
   question,correct,wrong1,wrong2,why=checks[i]
   opts=[(correct,True),(wrong1,False),(wrong2,False)]
   # Stable rotation avoids always placing the answer first. Derive key from authored truth tag.
   rotation=i%3;opts=opts[rotation:]+opts[:rotation]
   ix['public']={'prompt':question,'options':[{'option_id':f'o{j+1}','text':txt} for j,(txt,ok) in enumerate(opts)],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':[f'o{j+1}' for j,(_,ok) in enumerate(opts) if ok],'option_feedback':{f'o{j+1}':{'message':('Correct. ' if ok else 'Not supported. ')+why} for j,(_,ok) in enumerate(opts)}}
   hints=['Separate the observation already recorded from the additional evidence the conclusion needs.']
  else:
   why='Compare every review decision with the supplied settings and observed results; keep discrepancies visible.'
   ix['public']={'prompt':'Read each independent supplied evidence excerpt and its reviewer decision. Decide whether that decision is supported by the evidence and the verification requirements, or unsupported. A supported decision may correctly identify a failure; it does not always mean the operation succeeded.','buckets':[{'bucket_id':'supported','label':'Supported decision'},{'bucket_id':'unsupported','label':'Unsupported decision'}],'items':[{'item_id':f'item{j+1}','text':'```text\n'+txt+'\n```'} for j,(txt,ok,msg) in enumerate(cases[i])]}
   ix['grading']={'assignments':{f'item{j+1}':'supported' if ok else 'unsupported' for j,(_,ok,_) in enumerate(cases[i])},'item_feedback':{f'item{j+1}':{'message':msg} for j,(_,ok,msg) in enumerate(cases[i])}}
   hints=['Distinguish saved configuration from observed execution evidence.','Check whether the reviewer preserves failures and respects the supplied scope.']
  ix['feedback']={'correct':{'message':why},'incorrect':{'message':why},'hints':hints}
  candidates=[r for r in rem if cid in r['concept_ids']]
  if candidates:
   facts=set(step['fact_ids'])
   best=min(candidates,key=lambda r:len(set(r['lineage']['fact_ids']) ^ facts))
   ix['feedback']['remediation_step_id']=best['step_id']
  seen.add(cid);entries.append({'step_id':step['step_id'],'interaction':ix})
 for j, entry in enumerate(entries):
  entry['interaction']['difficulty']='intro' if j==0 else ('stretch' if j==len(entries)-1 else 'core')
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Tiles:',len(out['tiles']),'Interactions:',sum(len(t['interactions']) for t in out['tiles']))
