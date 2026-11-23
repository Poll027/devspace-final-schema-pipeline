import json, copy, re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.05_1')
p=json.load(open(B/'tile_plans.json')); g=json.load(open(B/'inputs/path_glossary_bundle.json')); registry=json.load(open(B/'scenario_asset_registry.json'))
bundles={x['context']['concept_id']:x for x in g['bundles']}; assets={x['asset_id']:x for x in registry['assets']}
# Screen copy: each entry follows the glossary's introductory and worked-case teaching groups.
copytext={
 'triage_a_representative_guardduty_finding': [
 ['A GuardDuty finding contains its type, severity, affected resource and suspicious-activity details. Inspect resource identity, activity timestamps and details; preserve the supporting evidence. Follow the established investigation and escalation procedure for that finding type. Severity alone is not a reason for destructive action.'],
 ['Record the supplied finding’s type, severity, resource identity and activity timestamps. Keep those activity timestamps rather than replacing them with the time the finding was opened. Preserve the detailed activity evidence and follow the finding-type procedure.', 'A severe finding adds urgency, not proof of compromise or permission to destroy a resource. If detail is incomplete, preserve what is available and escalate under the established procedure. Missing detail does not establish an attack mechanism.']],
 'audit_storage_access': [
 ['S3 bucket policies can grant or deny object operations for specified principals and resource paths. Limit approved audit writers and readers to required actions on intended bucket or object ARNs, and inspect other applicable grants and denies.', 'Verify the boundary with an approved write, an approved read and an unapproved read. Keep identity and resource path with each result. Encryption or retention settings do not replace these authorization checks.']],
 'audit_storage_encryption': [
 ['SSE-KMS uses an AWS KMS key; SSE-S3 uses S3-managed keys. An SSE-KMS read needs both s3:GetObject permission and kms:Decrypt authority for that key. SSE-S3 does not require KMS key-use permission. Configure the supplied key as bucket default encryption, test approved object/key authority and denied KMS use, and inspect object metadata.'],
 ['For the supplied SSE-KMS object, compare a read with approved s3:GetObject and kms:Decrypt authority against a read with KMS use denied. Inspect that object’s encryption metadata to determine its encryption model.', 'Changing bucket default encryption does not re-encrypt existing objects. A default setting is therefore not proof of an older object’s encryption. Keep SSE-KMS’s key-use requirement separate from SSE-S3, which needs no KMS key-use permission.']],
 'destroy_review': [
 ['A Terraform plan describes proposed additions, updates, deletions and replacements using configuration, state and observed infrastructure. Save it with terraform plan -out=PLAN_FILE and inspect it with terraform show PLAN_FILE. Replacement includes destruction and creation, not just an in-place update.', 'Compare affected resource identities and every proposed action, including the mandatory deletion case, with supplied scope and impact criteria. Record accept or block with plan evidence. Review does not require destructive execution.'],
 ['Keep each resource identity beside its proposed action. Check additions, updates, replacements and the supplied deletion against approved scope and impact criteria. A replacement includes destruction as well as creation.', 'Record accept or block with the relevant saved-plan evidence. Do not execute a deletion merely to demonstrate that you identified it, and do not treat a general description of an “update” as proof that no infrastructure will be removed.']],
 'dry_run': [
 ['For supported EC2 operations, DryRun checks permissions without executing the operation. DryRunOperation means sufficient permission; UnauthorizedOperation means insufficient permission. Neither is a real operation result or a guarantee of later success.', 'The supplied fleet wrapper’s preview is a separate check: compare proposed targets and actions with approved scope while mutation stays disabled. EC2 DryRun is not a universal preview of every AWS service’s changes.'],
 ['Compare the wrapper’s proposed targets and actions with approved fleet scope and record discrepancies without enabling mutation. Retain that proposed-action evidence separately from the supported EC2 operation’s permission result.', 'DryRunOperation means the dry-run permission check succeeded, not that the real operation ran. UnauthorizedOperation means insufficient permission. Permission success neither guarantees later operation success nor provides a service-wide change preview.']],
 'partial_failure': [
 ['One fleet command has separate invocation results for individual targets, and those results may differ. Inspect statuses and outputs; record successful, failed and unresolved targets separately. Choose the supplied scoped follow-up from target-specific evidence rather than blindly repeating successful work.'],
 ['The supplied three-target case keeps successful, failed and unresolved outcomes separate. Retain target identity, invocation status and output evidence with each category. An unresolved outcome is not a failure established by evidence.', 'Keep successful work visible when selecting the supplied scoped follow-up. A single overall command label cannot replace per-target results, and one failure does not justify repeating the whole operation. Preserve uncertainty until inspection establishes the unresolved target’s outcome.']],
 'credential_expiry': [
 ['Expired temporary credentials are no longer usable. Renew the approved session through its credential provider and use the new access key, secret key and session token together.', 'Before retrying a resource-changing request, inspect its known outcome. Where the supplied operation supports an idempotency token, use it to avoid duplicate effects. Renewed credentials alone do not settle the earlier request’s outcome.'],
 ['Replace the expired credential set through the approved provider, keeping the new access key, secret key and token together. For a mutation, record whether the original request is known to have taken effect before considering a repeat.', 'Compare a known completed mutation with an unresolved result. Neither case makes expired credentials usable again, but completion is not a reason to repeat the mutation. For an unresolved case, inspect available outcome evidence before retrying and use supported idempotency where available.']],
 'ecs_task_identity': [
 ['The ECS task role supplies credentials for application containers’ AWS calls. The task execution role instead authorizes startup work such as pulling images and publishing logs. These roles do not substitute for each other.', 'Set taskRoleArn in the task definition to the approved least-privilege application role. Test supplied allowed and denied application operations from the task, and associate results with that application identity. Successful startup work does not establish application AWS access.']],
 'apply_an_approved_security_baseline_to_sandbox_accounts': [
 ['A governed account baseline applies standardized organizational controls and configuration. Apply the supplied approved configuration to the sandbox account and inspect each stated control’s deployment or evaluation result.', 'Preventive controls restrict actions; detective controls report noncompliance. Record those different checkpoints by control. A detective report is not a preventive restriction, and configuration presence is not verification of every control’s result. This is an established baseline, not a task to design new controls.']],
 'apply_bounded_eks_workload_configuration_and_secrets': [
 ['A ConfigMap supplies nonconfidential configuration separately from the container image. In the Pod template, use envFrom.configMapRef or env.valueFrom.configMapKeyRef. Reference a Secret with env.valueFrom.secretKeyRef or a secret-backed volume; test the consumer without printing secret values. Secrets need access control and appropriate storage protection: base64 encoding is not encryption.'],
 ['Check the intended ConfigMap and Secret references in the supplied Pod template, then test the consuming workload without exposing secret values. Nonconfidential configuration belongs in the ConfigMap; the Secret still needs access control and storage protection.', 'A ConfigMap change does not automatically update ConfigMap-backed environment variables inside already-running containers. Tie consumer evidence to the actual references and running consumer rather than assuming the updated ConfigMap alone proves a change. Base64 encoding is not encryption.']],
 'configure_codepipeline_source_to_deploy_actions': [
 ['Pipeline stages contain actions that pass declared input and output artifacts. Connect source output to CodeBuild input, and CodeBuild output to CodeDeploy input, for the intended revision.', 'The CodePipeline service role needs trust for codepipeline.amazonaws.com and action/artifact permissions; it is not GitHub OIDC federation. Verify the intended revision through deployment evidence. A failed action prevents normal progression to dependent actions.'],
 ['Compare source output names with CodeBuild input names, then build output names with CodeDeploy input names. A stage list alone does not prove artifact continuity. Inspect the service role’s trust for codepipeline.amazonaws.com and required action/artifact permissions, not GitHub OIDC trust.', 'Follow execution evidence for the intended source revision through deployment. In the failure case, check that the failed action stops normal progression to dependent actions. Success on a different input is not evidence for the intended release.']],
 'deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles': [
 ['The same CloudFormation template can provision equivalent declarations in multiple approved environments. Each approved account/Region pair still needs its own verified deployment record. Use a named role profile with role_arn and source_profile; verify the caller with aws sts get-caller-identity --profile NAME. Create the supplied stack with that profile and explicit --region REGION.', 'Inspect stack outputs, S3 bucket identity and bucket location in every intended target. Separately check that supplied unapproved targets received no stack. One successful target does not prove the others; distinguish confirmed absence from a failed absence check.']],
 'diagnose_aws_connectivity_failures': [
 ['A required path needs the subnet’s actual route-table association and a matching destination route to a usable target. Check DNS resolution and intended endpoint address, then inspect route association, required protocol/port rules and response traffic to locate the failing layer.', 'Network ACLs are stateless: requests and responses need permission in their respective directions. Make only the approved correction supported by that layer’s evidence, then repeat the endpoint connection test.'],
 ['Start with DNS resolution and the intended endpoint address. Inspect the used subnet route-table association, matching destination route and usable target, then protocol/port rules and response traffic. A connection symptom alone does not identify the failing layer.', 'If the supplied evidence identifies a missing response allowance in a network ACL, use the approved correction for that layer. A permitted request direction is not sufficient for a stateless ACL. Retest the endpoint connection after correction rather than altering every control or accepting an edited route table as proof of the used path.']],
 'execute_an_established_fleet_patch_task': [
 ['Patch Manager uses patch baselines and managed-node targets to scan or install patches and report compliance. Use the established maintenance-window task with approved targets, patch document parameters, concurrency and error limits.', 'Inspect task execution and per-node patch compliance to identify which approved instances were patched and which need follow-up. Keep node identity with its result. A maintenance-window summary does not replace per-node evidence or justify changing the approved task bounds.']],
 'expose_an_eks_workload_using_a_kubernetes_service': [
 ['A Kubernetes Service provides a stable network endpoint for a changing set of selected Pods. Match spec.selector to intended Pod labels, and map ports.port through ports.targetPort to the application’s container port.', 'Apply the supplied Service, inspect EndpointSlices or endpoints, and test its address from the supplied client. Keep selector, port mapping, endpoint evidence and client result together to verify selected Pods receive traffic. A Service object’s name or declaration alone is not proof of application reachability.']]
}
contrasts={
 'triage_a_representative_guardduty_finding':'Contrast: severity adds urgency; resource and activity evidence support the established investigation path, not destruction from severity alone.',
 'audit_storage_access':'Contrast: encryption or retention describes storage protection, not proof that an unapproved reader is denied.',
 'audit_storage_encryption':'Contrast: SSE-KMS needs object permission and KMS authority; SSE-S3 has no KMS key-use requirement. Inspect object metadata, not just bucket defaults.',
 'destroy_review':'Contrast: replacement includes destruction and creation; an in-place update is not the same action. Review evidence does not require destructive execution.',
 'dry_run':'Contrast: wrapper preview describes proposed scope; supported EC2 DryRun describes permissions, not execution or guaranteed later success.',
 'partial_failure':'Contrast: an unresolved target is not an evidenced failure. Keep successful work distinct and use only the supplied scoped follow-up.',
 'credential_expiry':'Contrast: renewing credentials restores a usable identity, not certainty about the earlier mutation. Inspect the outcome before retrying.',
 'ecs_task_identity':'Contrast: image pulling and log publication concern startup authority, not application AWS permissions under taskRoleArn.',
 'apply_an_approved_security_baseline_to_sandbox_accounts':'Contrast: preventive controls restrict actions; detective controls report noncompliance. Configuration presence is not a per-control result.',
 'apply_bounded_eks_workload_configuration_and_secrets':'Contrast: base64 encoding is not encryption. ConfigMap-backed environment variables also do not automatically update in already-running containers.',
 'configure_codepipeline_source_to_deploy_actions':'Contrast: a stage list is not artifact continuity. Compare linked artifact names and intended revision evidence, with failures stopping dependent progression.',
 'deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles':'Contrast: equivalent template declarations are not one shared deployment result. Keep approved deployments and unapproved-target absence checks separate.',
 'diagnose_aws_connectivity_failures':'Contrast: request permission alone is insufficient for a stateless ACL. Response-direction evidence and a repeated connection test matter too.',
 'execute_an_established_fleet_patch_task':'Contrast: an overall task label does not establish each approved node’s patch outcome. Keep per-node compliance and follow-up evidence.',
 'expose_an_eks_workload_using_a_kubernetes_service':'Contrast: a Service declaration is not a traffic test. Selector, targetPort, observed endpoints and supplied-client results must agree.'
}
shorttitles=['Finding evidence before response','Verify the audit access boundary','Separate object and key authority','Review every Terraform action','Preview scope, check permissions','Keep fleet outcomes separate','Renew identity, inspect outcomes','Separate ECS role responsibilities','Verify each baseline control','Reference configuration safely','Trace the intended pipeline revision','Verify every account and Region','Localize the failing network layer','Preserve patch-task bounds','Verify the Service traffic path']
ctitle={c:shorttitles[i] for i,c in enumerate(bundles)}
def suffix(c):return c.split('.')[-1]
def lin(c,tbs,facts,anchors=None):
 return dict(concept_ids=[c],teaching_block_ids=[c+'#'+v for v in tbs],fact_ids=[c+'#'+v for v in facts],**({'anchors':anchors} if anchors else {}))
def prose(text,lineage,role='mechanism'):return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lineage)}
def table(a,lineage,columns=None):
 x={'type':'data_table','asset_ref':{'asset_id':a},'lineage':copy.deepcopy(lineage)}
 if columns:x['asset_ref']['columns']=columns
 return x
def diagram(title,labels,edges,lineage,kind='architecture'):
 return {'type':'diagram','title':title,'diagram_kind':kind,'nodes':[{'id':'n'+str(i),'label':v} for i,v in enumerate(labels)],'edges':[{'from':'n'+str(i),'to':'n'+str(j),'label':label,'directed':True} for i,j,label in edges],'alt_text':title+'. '+'; '.join(labels),'layout':'auto','lineage':copy.deepcopy(lineage)}
def flow(title,labels,edges,lineage):
 return {'type':'process_flow','title':title,'direction':'LR','nodes':[{'id':'n'+str(i),'label':v} for i,v in enumerate(labels)],'edges':[{'from':'n'+str(i),'to':'n'+str(j),'label':label} for i,j,label in edges],'alt_text':title+'. '+'; '.join(labels),'lineage':copy.deepcopy(lineage)}
def side(left,right,ll,rl,take,lineage):return {'type':'side_by_side','left':left,'right':right,'left_label':ll,'right_label':rl,'takeaway':take,'lineage':copy.deepcopy(lineage)}
def visual(c,L):
 k=suffix(c)
 if k=='triage_a_representative_guardduty_finding':
  return diagram('Finding review layout — field guide, not a live finding',['Finding type / severity','Affected resource identity','Activity timestamps','Suspicious-activity details','Opened time: not activity time','Preserve evidence → established finding-type procedure'],[(0,5,'context'),(1,5,'identity'),(2,5,'timeline'),(3,5,'details'),(4,2,'do not substitute')],L,'container')
 if k=='audit_storage_access':
  return side(table('ds.audit_access_tests',L,['principal','requested_action','resource_arn','scoped_policy_statement','other_grants_and_denies_review']),table('ds.audit_access_tests',L,['test_id','principal','requested_action','resource_arn','observed_result']),'Policy scope and applicable authority','Three observed authorization tests','Check identity, action and resource with each result.',L)
 if k=='audit_storage_encryption':
  return diagram('Two encryption models, separate authority boundaries',['Audit reader','s3:GetObject permission','kms:Decrypt authority for object key','SSE-KMS object metadata','SSE-S3 object metadata: S3-managed keys; no KMS key-use permission','Bucket default: does not re-encrypt existing objects'],[(0,1,'object permission'),(1,2,'SSE-KMS also needs'),(2,3,'key authority'),(1,4,'SSE-S3 path'),(5,3,'inspect individual metadata'),(5,4,'inspect individual metadata')],L)
 if k=='destroy_review':
  return {'type':'code_walkthrough','language':'bash','code':'terraform plan -out=PLAN_FILE\nterraform show PLAN_FILE\n# Review each resource identity and proposed action:\n# addition | update | replacement | deletion\n# Compare with supplied scope and impact criteria.\n# Record accept or block with saved-plan evidence.','annotations':[{'start_line':1,'end_line':2,'text':'Save and inspect; no destructive execution is required.'},{'start_line':3,'end_line':6,'text':'Review checklist, not computed plan output. Replacement includes destruction and creation; include the mandatory deletion case.'}],'lineage':L}
 if k=='dry_run':
  return side(table('ds.wrapper_preview',L),table('ds.ec2_dryrun_evidence',L),'Wrapper: proposed scope, mutation disabled','EC2: supported-operation permission evidence','Neither permission success nor preview is a guarantee of later execution success.',L)
 if k=='partial_failure':return table('ds.fleet_invocations',L)
 if k=='credential_expiry':
  return flow('Expired identity and safe retry are separate checks',['Expired session','Renew through approved provider','New access key + secret key + token','Inspect original operation outcome','Known completed: do not repeat merely due to expiry','Retry warranted: supported idempotency token where available'],[(0,1,'replace'),(1,2,'use together'),(2,3,'before mutation retry'),(3,4,'completed'),(3,5,'after outcome inspection')],L)
 if k=='ecs_task_identity':
  return diagram('ECS has two permission paths',['Task execution role','Startup: image pulling / log publication','taskRoleArn → approved least-privilege task role','Application containers’ AWS calls','Allowed and denied application-operation tests'],[(0,1,'startup authority'),(2,3,'application credentials'),(3,4,'verify application identity')],L)
 if k=='apply_an_approved_security_baseline_to_sandbox_accounts':
  return diagram('Baseline checkpoint layout — evidence to inspect',['Designated sandbox account','Approved standardized control configuration','Preventive control: deployment result / action restriction','Detective control: evaluation result / noncompliance report','Per-control verification record'],[(1,0,'apply approved baseline'),(0,2,'inspect checkpoint'),(0,3,'inspect checkpoint'),(2,4,'retain result'),(3,4,'retain result')],L,'container')
 if k=='apply_bounded_eks_workload_configuration_and_secrets':
  return {'type':'code_walkthrough','language':'bash','code':'# Deployment Pod-template reference checklist (not executable YAML):\n# envFrom.configMapRef -> supplied ConfigMap\n# env.valueFrom.configMapKeyRef -> supplied ConfigMap name and key\n# env.valueFrom.secretKeyRef -> supplied Secret name and key\n# Alternative: supplied secret-backed volume\n# Test consuming workload without printing secret values.','annotations':[{'start_line':2,'end_line':3,'text':'Nonconfidential configuration, separate from the image.'},{'start_line':4,'end_line':6,'text':'Secret references, not secret values; protect access and storage.'}],'lineage':L}
 if k=='configure_codepipeline_source_to_deploy_actions':
  return flow('Stage/action artifact continuity',['Source action: intended revision / declared output','CodeBuild action: matching input / declared output','CodeDeploy action: matching input / revision evidence','Service role: codepipeline.amazonaws.com trust + action/artifact permissions','Failed action: dependent progression stops'],[(0,1,'source output = build input'),(1,2,'build output = deploy input'),(3,0,'service authority'),(3,1,'service authority'),(3,2,'service authority'),(1,4,'failure case')],L)
 if k=='deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles':return table('ds.account_region_deployments',L)
 if k=='diagnose_aws_connectivity_failures':
  return diagram('Endpoint-path evidence and bounded correction',['DNS → intended endpoint address','Subnet’s used route-table association','Matching destination route → usable target','Required request protocol/port rules','Required response direction: stateless network ACL','If evidence shows missing response allowance: approved correction','Repeat endpoint connection test: inspect result'],[(0,1,'inspect path'),(1,2,'verify route'),(2,3,'request'),(3,4,'response'),(4,5,'localized failure case'),(5,6,'verify correction')],L,'network')
 if k=='execute_an_established_fleet_patch_task':
  return diagram('Maintenance-window review layout — per-node evidence',['Established task: patch baseline / managed-node targets','Approved target set + document parameters','Concurrency + error limits','Per-node task execution result','Per-node patch compliance','Approved instances patched / requiring follow-up'],[(0,1,'preserve scope'),(1,2,'preserve bounds'),(2,3,'inspect each target'),(3,4,'associate node identity'),(4,5,'determine from evidence')],L,'container')
 if k=='expose_an_eks_workload_using_a_kubernetes_service':
  return diagram('Stable Service endpoint, verified selected Pods',['Supplied client','Stable Service address / ports.port','spec.selector ↔ intended Pod labels','EndpointSlices or endpoints','Selected Pods / application container port','ports.targetPort','Client connection result'],[(0,1,'request'),(2,3,'verify selected endpoints'),(1,5,'port mapping'),(5,4,'application port'),(3,4,'endpoint evidence'),(4,6,'verify selected Pods receive traffic')],L,'network')
 raise ValueError(k)
# Short recap sentences are sourced only from already taught content.
takeaways={
 'triage_a_representative_guardduty_finding':'Preserve finding evidence and follow the established procedure, not severity alone.',
 'audit_storage_access':'Verify scoped authorization with approved and unapproved identity tests.',
 'audit_storage_encryption':'Separate SSE-KMS object permission, KMS authority and individual-object metadata.',
 'destroy_review':'Inspect every saved-plan action, including deletion and replacement; record an evidence-backed accept/block decision.',
 'dry_run':'Keep wrapper scope preview separate from supported EC2 DryRun permission evidence.',
 'partial_failure':'Record successful, failed and unresolved targets separately for scoped follow-up.',
 'credential_expiry':'Renew the entire credential set, then inspect mutation outcomes before considering retries.',
 'ecs_task_identity':'Task execution authority is not application authority; verify allowed and denied task-role operations.',
 'apply_an_approved_security_baseline_to_sandbox_accounts':'Inspect each approved baseline checkpoint; preventive restrictions and detective reports are different results.',
 'apply_bounded_eks_workload_configuration_and_secrets':'Use intended configuration and secret references, protect secret values, and test the consumer without assuming environment variables refresh.',
 'configure_codepipeline_source_to_deploy_actions':'Link declared artifacts, verify service-role authority and trace revision evidence; failed actions stop dependent progression.',
 'deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles':'Verify caller, stack outputs and bucket location per approved target; separately confirm unapproved-target absence.',
 'diagnose_aws_connectivity_failures':'Localize the failing layer, check request and response directions, make the approved correction and retest.',
 'execute_an_established_fleet_patch_task':'Preserve approved task bounds and inspect each node’s execution and patch-compliance evidence.',
 'expose_an_eks_workload_using_a_kubernetes_service':'Verify selector and port mapping with endpoint evidence and the supplied-client result.'}
out={'schema_version':p['schema_version'],'kind':'screens_part','path_id':p['path_id'],'batch_id':p['batch_id'],'tiles':[]}
for ti,t in enumerate(p['tiles']):
 tile={'tile_id':t['tile_id'],'title':' / '.join(ctitle[c] for c in t['concept_ids']),'steps':[],'remediation_steps':[]}
 groups={}; remseen=set()
 for s in t['steps']:
  L={k:copy.deepcopy(s[k]) for k in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']}
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'title':'','lineage':L}
  c=s['concept_ids'][0]; k=suffix(c)
  if s['type']=='explainer':
   n=groups.get(c,0); groups[c]=n+1
   step['title']=ctitle[c] if n==0 else 'Inspect the evidence and the contrast'
   step['eyebrow']='Explain' if n==0 else 'Worked review'
   step['blocks']=[prose(v,L,'mechanism' if n==0 else 'example') for v in copytext[k][n]]
   if s['planned_visual_block_type']:
    VL=copy.deepcopy(L);VL['anchors']=[c+'#visual'];step['blocks'].append(visual(c,VL))
  elif s['type'] in ['check','hands_on']:
   step['title']=('Review ' if s['type']=='hands_on' else 'Check ')+ctitle[c].lower()
   step['eyebrow']='Evidence judgement' if s['type']=='hands_on' else 'Knowledge check'
   step['lede']='Read the supplied excerpts in this step and decide which interpretations or proposed actions are correct, defective or unsafe.' if s['type']=='hands_on' else 'Choose the interpretation supported by the supplied evidence.'
   # Every distinct measured fact set gets a directly applicable remediation.
   key=(c,tuple(sorted(s['fact_ids'])))
   if key not in remseen:
    remseen.add(key)
    facts=[q.split('#')[-1] for q in s['fact_ids']]
    tbs=[tb['id'] for tb in bundles[c]['teaching_blocks'] if set(tb['fact_ids'])&set(facts)]
    RL=lin(c,tbs,facts)
    factmap={f['id']:f['statement'] for f in bundles[c]['coverage']['required_facts']}
    factmap.update({m['id']:m.get('correction',m.get('statement','')) for m in bundles[c]['coverage'].get('misconceptions',[])})
    # Fact statements retain exact boundaries, with a separate authored contrast.
    texts=[(f,factmap[f]) for f in facts if f in factmap]
    # Same registered evidence is available again where this concept uses datasets.
    rem={'step_id':t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2),'type':'remediation','concept_ids':[c],'title':'Revisit '+ctitle[c].lower(),'eyebrow':'One clear contrast','blocks':[prose(v,lin(c,[tb['id'] for tb in bundles[c]['teaching_blocks'] if f in tb['fact_ids']],[f])) for f,v in texts],'lineage':copy.deepcopy(RL)}
    contrast_facts={
     'triage_a_representative_guardduty_finding':['f2','f3'],
     'audit_storage_access':['f3'],
     'audit_storage_encryption':['f1','f2','m1'],
     'destroy_review':['f2','f3'],
     'dry_run':['f1','f2','f3'],
     'partial_failure':['f2','f3'],
     'credential_expiry':['f1','f2','f3'],
     'ecs_task_identity':['f1','f2','f3'],
     'apply_an_approved_security_baseline_to_sandbox_accounts':['f2','f3'],
     'apply_bounded_eks_workload_configuration_and_secrets':['f4','m1'],
     'configure_codepipeline_source_to_deploy_actions':['f1','f2','f4'],
     'deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles':['f1','f3'],
     'diagnose_aws_connectivity_failures':['f3','f4'],
     'execute_an_established_fleet_patch_task':['f3'],
     'expose_an_eks_workload_using_a_kubernetes_service':['f2','f3']}[k]
    # The second EKS check has its own single-idea contrast.
    contrast_text=contrasts[k]
    if k=='apply_bounded_eks_workload_configuration_and_secrets':
     if facts==['f4']:
      contrast_facts=['f4'];contrast_text='Contrast: base64 encoding is not encryption; a Secret still needs access control and appropriate storage protection.'
     elif facts==['m1']:
      contrast_facts=['m1'];contrast_text='Contrast: an updated ConfigMap is not proof that environment variables inside an already-running container have changed automatically.'
     else:
      contrast_facts=['f1','f2','f3'];contrast_text='Contrast: a configuration or Secret reference is not the consumer test. Check intended references and test the workload without printing secret values.'
    CL=lin(c,[tb['id'] for tb in bundles[c]['teaching_blocks'] if set(tb['fact_ids']) & set(contrast_facts)],contrast_facts)
    rem['blocks'].append(prose(contrast_text,CL,'misconception'))
    for keyname in ['fact_ids','teaching_block_ids']:
     rem['lineage'][keyname]=list(dict.fromkeys(RL[keyname]+CL[keyname]))
    if k in ['audit_storage_access','dry_run','partial_failure','deploy_a_supplied_cloudformation_s3_environment_across_accounts_and_regions_with_assumed_roles']:
     rem['blocks'].append(visual(c,dict(RL,anchors=[c+'#visual'])))
    tile['remediation_steps'].append(rem)
  elif s['type']=='video':
   step['title']='Locate the operational evidence';step['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif s['type']=='recap':
   step['title']='Keep the evidence boundaries clear';step['blocks']=[]
   for rc in s['concept_ids']:
    facts=[f['id'] for f in bundles[rc]['coverage']['required_facts']]
    tbs=[tb['id'] for tb in bundles[rc]['teaching_blocks'] if tb['fact_ids']]
    step['blocks'].append(prose(takeaways[suffix(rc)],lin(rc,tbs,facts),'takeaway'))
   if ti+1<len(p['tiles']):
    nc=p['tiles'][ti+1]['concept_ids'][0]; nextname=ctitle[nc]
   else:
    # The bundle's first blocked future name identifies the coming topic; no new teaching.
    nc=bundles[c]['context']['blocked_future_concepts'][0];nextname=g['names'][nc]
   step['blocks'].append({'type':'up_next','title':'Up next: '+nextname,'text':'Continue to '+t['next_tile_id']+'.'})
  tile['steps'].append(step)
 out['tiles'].append(tile)
# Deterministic local mistakes-to-avoid checks.
assert [t['tile_id'] for t in out['tiles']]==[t['tile_id'] for t in p['tiles']]
def walk(block):
 yield block
 for key in ['left','right']:
  if key in block:yield from walk(block[key])
for tile,plan in zip(out['tiles'],p['tiles']):
 assert [(s['step_id'],s['type'],s['concept_ids']) for s in tile['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in plan['steps']]
 for s,ps in zip(tile['steps'],plan['steps']):
  for key in ['teaching_block_ids','fact_ids']:assert s['lineage'][key]==ps[key]
  wc=sum(len(b['text'].split()) for b in s.get('blocks',[]) if b['type']=='prose')
  assert wc<=ps['word_budget'],(s['step_id'],wc,ps['word_budget'])
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s
 for s in tile['steps']+tile['remediation_steps']:
  for b0 in s.get('blocks',[]):
   for b in walk(b0):
    assert 'result' not in b and 'output' not in b and 'computed_values' not in b
    if b['type']=='prose':
     assert b.get('lineage') and len(b['text'].split())<=90
     assert not re.search(r'\bvideo\b',b['text'],re.I)
    if 'lineage' in b:
     assert all('#' in q for q in b['lineage'].get('fact_ids',[])+b['lineage'].get('teaching_block_ids',[]))
    if b['type'] in ['diagram','side_by_side','code_walkthrough','process_flow','data_table']:assert any(a.endswith('#visual') for a in b['lineage']['anchors'])
    if 'asset_ref' in b:
     ar=b['asset_ref'];assert ar['asset_id'] in assets
     assert set(ar.get('columns',[])) <= {col['name'] for col in assets[ar['asset_id']]['columns']}
json.dump(out,open(B/'screens.json','w'),indent=2,ensure_ascii=False)
print('tiles',len(out['tiles']),'planned steps',sum(len(t['steps']) for t in out['tiles']),'remediation steps',sum(len(t['remediation_steps']) for t in out['tiles']))
from collections import Counter
print(Counter(s['type'] for t in out['tiles'] for s in t['steps']))
print('Local checklist passed: plan order and lineage, prose budgets, qualified IDs, independent text, registered columns, visual anchors, no typed outputs.')
