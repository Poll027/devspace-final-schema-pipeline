import json, copy, re
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.04_1')
plan=json.loads((P/'tile_plans.json').read_text()); glossary=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((P/'scenario_asset_registry.json').read_text())
bundles=glossary['bundles']; C=[b['context']['concept_id'] for b in bundles]; B=dict(zip(C,bundles)); assets={a['asset_id']:a for a in registry['assets']}
facts=[
['A buildspec describes commands and artifacts in YAML. Version 0.2 supports commands in the same shell environment.','Put supplied commands in commands lists under needed phases, such as install, pre_build, build and post_build.','Match artifacts.files and, when needed, base-directory to generated output. Inspect phase logs and the exported artifact.'],
['For EC2, appspec.yml maps revision files to destinations and lists lifecycle-hook scripts.','Use the supplied application and deployment group to identify intended EC2 targets and revision, with the approved service role and installed agent.','Inspect AppSpec mappings and hooks; execute the supplied action, then verify hook results and application files on the target.'],
['Target tracking adjusts Auto Scaling capacity to keep a chosen metric near its target.','Choose the approved metric and target; configure instance warmup and minimum, desired and maximum capacities.','During the bounded load test, compare metric values, scaling activities and resulting capacity. Capacity cannot exceed the configured maximum.'],
['An ECR repository policy grants specified principals operations such as image pulls or image-layer uploads.','Scope principals and actions to approved publishers and consumers; test push, pull and an unapproved principal.','Authentication also needs ecr:GetAuthorizationToken through an identity policy. Repository permissions alone do not grant that action.'],
['ECR lifecycle policies expire images selected by criteria such as tag status and count or age.','Express supplied retention using rulePriority, selection and action. Run a lifecycle preview before applying it.','Compare previewed digests with deployed versions. Exclude still-needed versions from eligible expiry; deployment does not make images immune.'],
['An ALB listener evaluates routing rules and forwards matching requests to a target group.','Configure supplied listener protocol/port, forwarding rule and registered target protocol/port; test the endpoint.','Match health-check path, port and success codes to the backend. Inspect target health reasons when a request path fails.','ALB normally routes to healthy registered targets. If every registered target in a group is unhealthy, it fails open and routes to those unhealthy targets.'],
['CloudWatch log-group retention controls how long events remain. By default, logs are retained indefinitely.','Set the supplied interval with put-retention-policy; inspect the intended log group’s retentionInDays.','Expired events are marked for deletion. Physical deletion typically takes up to 72 hours, so expiry need not mean immediate disappearance.'],
['An RDS DB snapshot captures a database instance for later restoration.','Create a manual snapshot of the intended instance and wait for snapshot status available.','Restore to a new DB instance identifier with supplied network settings. This creates a separate instance, not an overwrite of the source.','Wait for the restored instance to become available. Connect to its endpoint and run the supplied query to verify the recovery marker.'],
['CloudWatch Logs authorizes log-group and log-stream operations through IAM policies.','Grant the approved reader required read actions on intended log-group resources; remove unnecessary broader grants. Some operations require resource scope *.','Test intended read operations under approved and unapproved principals. Collecting logs does not itself grant reader access.'],
['An ECS task definition specifies the image and container runtime settings for tasks.','Set containerDefinitions name, image, portMappings, cpu and memory appropriate to the supplied launch type; register the definition.','Run that registered definition with the supplied cluster and network configuration. Inspect task status and container details to verify image and runtime settings.'],
['Diagnose access denial for the specific principal, operation, resource and request context.','Inspect the request and applicable policies for explicit deny, missing allow or unsatisfied condition. Use available denial context to localize the cause.','Resource policies, session policies, permissions boundaries and organization policies can constrain access beyond one identity policy. Explicit deny takes precedence.','Make the smallest approved policy or request correction supported by evidence, then retest the denied operation.'],
['terraform apply PLAN_FILE executes saved changes without generating a new plan or prompting for approval.','Use the supplied approved saved plan, not an unplanned apply. Retain the apply outcome as execution evidence.','Inspect terraform show PLAN_FILE and resulting resources or outputs to check the created EC2 instance against the approved plan.'],
['Run Command executes Systems Manager documents on managed nodes under authorized access.','Use send-command with supplied document, parameters and explicit approved --instance-ids or tag-based --targets.','Record the command ID. Inspect each invocation’s status and output; parent status does not replace per-node checks.'],
['terraform validate checks syntax and internal consistency, not remote service state or provider API success.','Where backend access is unnecessary, initialize needed providers and modules with terraform init -backend=false before static validation.','Make terraform validate blocking. Stop on nonzero exit, correct the invalid declaration and rerun before the supplied approved apply step.','terraform fmt -check checks canonical formatting and can serve as an additional blocking configuration check.']]
examples=[
'For delivery-api, compare the generated output path literally with artifact selection. If commands succeed but the selected path misses the generated file, export is not verified. Do not add unfamiliar commands merely to fill every phase.',
'Trace one supplied AppSpec mapping to files inspected on the intended target. Relate hook results to that same revision. A requested action, failed hook or successful hook from another deployment cannot establish this revision’s target change.',
'In the supplied timeline, read metric values alongside activities and capacity. At the maximum, an above-target metric is not permission to exceed the bound. These authored observations are not exact response-time guarantees.',
'Compare the publisher’s push, consumer’s pull and unapproved principal’s test. Authentication and repository authorization are separate: an authenticated principal still needs the relevant repository grant.',
'Use the preview table to compare eligible digests with deployed and still-needed flags. If a needed digest would expire, revise eligibility before applying the policy; a deployment reference is not protection.',
'If the supplied health-check path differs from the backend requirement, inspect health reasons and make the approved correction rather than changing unrelated settings. An unhealthy label is not an unconditional no-traffic guarantee: keep the all-unhealthy fail-open exception beside normal routing.',
'An expired event may remain visible immediately after expiry. Compare retentionInDays with the supplied requirement before interpreting that visibility; deletion delay is not proof that retention is absent.',
'Keep source, snapshot and restored identifiers together. An available snapshot is not restored-data verification. A query against the source endpoint cannot verify the recovery marker on the separate restored instance.',
'Test the supplied reader and unapproved principal for each intended operation. Keep identity, action and resource scope with results. Do not force resource scope narrower than the supplied operation supports.',
'Compare the registered specification with observed task details. Registration alone is not proof that the intended image and runtime settings were used. Do not generalize cpu or memory settings across launch types.',
'Finding an Allow in one identity policy does not settle this request. Inspect the other applicable constraints and denial context. Choose a minimal approved correction supported by that evidence, then repeat the same operation—not a different request.',
'Compare planned AMI, instance type and placement with resulting resource evidence. Saved-plan execution has no new approval prompt: the file must already be approved. Completion and resource comparison are distinct checks.',
'Compare invocation targets with the approved target set before interpreting results. A successful unintended-node invocation is still a scope discrepancy. Preserve each node’s status and output under the shared command ID; missing or unresolved invocations are not success.',
'For the supplied invalid EC2 declaration, validation failure must block apply. After correction, rerun validation and any blocking formatting check. A formatting-only change is not a configuration-validity correction, and static-check success is not provisioning evidence.']
recaps=[
'Match supplied phase commands and generated output selection; verify both phase logs and exported files.',
'Keep revision, intended targets, AppSpec mappings, hook results and target files connected.',
'Compare metric, activities and capacity within approved bounds; above-target load cannot override the maximum.',
'Test publisher, consumer and unapproved access; separate repository authorization from identity-policy authentication.',
'Preview expiry by digest and protect still-needed versions by excluding them from eligibility.',
'Check listener routing and backend health settings; remember the all-unhealthy fail-open exception.',
'Inspect retentionInDays; distinguish expiry from physical deletion, which typically takes up to 72 hours.',
'Restore to a separate instance and verify its recovery marker at its own endpoint.',
'Grant required reader actions with supported scopes; test approved and unapproved identities.',
'Compare registered task settings with task status and container details for the supplied launch type.',
'Localize denial for the exact request; inspect applicable constraints and retest the smallest approved correction.',
'Apply the approved saved file and compare the created instance with that plan.',
'Keep approved targets and command ID with each invocation’s status and output.',
'Initialize dependencies, block on validation failure, and distinguish formatting, static validity and provisioning evidence.']
contrasts=[
'Command success is not verified artifact export.', 'An action request is not verified target change.', 'Target tracking is bounded, not unlimited capacity.', 'Authentication is not repository authorization.', 'Deployment is not immunity from expiry.', 'Unhealthy does not always mean no routed traffic.', 'Expiry is not necessarily immediate deletion.', 'A source-endpoint query is not restored-data verification.', 'Log collection is not reader authorization.', 'Registration is not observed runtime verification.', 'An identity-policy Allow is not the whole access decision.', 'Saved-plan apply is execution, not a new approval decision.', 'Parent status is not per-node evidence.', 'Formatting success is not configuration validity or provider API success.']
I={c:i for i,c in enumerate(C)}
def lin(c, fs=None, ts=None, anchors=None):
 return {'concept_ids':[c], 'fact_ids':fs or [], 'teaching_block_ids':ts or [], **({'anchors':anchors} if anchors else {})}
def prose(text,c,fs,ts,role): return {'type':'prose','text':text,'role':role,'lineage':lin(c,fs,ts)}
def diagram(title, labels,c,anchors=None):
 nodes=[{'id':f'n{j+1}','label':v} for j,v in enumerate(labels)]
 return {'type':'diagram','diagram_kind':'sequence','title':title,'nodes':nodes,'edges':[{'from':nodes[j]['id'],'to':nodes[j+1]['id'],'directed':True} for j in range(len(nodes)-1)],'alt_text':title+': '+' → '.join(labels),'lineage':lin(c,anchors=anchors)}
def table(a,c,cols=None):
 a=assets[a]; available=[v['name'] for v in a['columns']]
 return {'type':'data_table','asset_ref':{'asset_id':a['asset_id'],'columns':[v for v in available if cols is None or v in cols]},'lineage':lin(c)}
def pair(l,r,ll,rl,take,c,an): return {'type':'side_by_side','left':l,'right':r,'left_label':ll,'right_label':rl,'takeaway':take,'lineage':lin(c,anchors=an)}
def visual(s):
 c=s['concept_ids'][0];i=I[c];an=[c+'#visual']
 if i==0:
  return pair(diagram('Phase plan',['version: 0.2','Needed phases: supplied commands lists','Generated output path','Inspect phase logs'],c),diagram('Artifact selection',['Supplied base-directory, if needed','artifacts.files selects generated output','Inspect exported file'],c),'Commands','Export','Compare the generated path with the selected file.',c,an)
 if i==1:return diagram('Deployment review',['Supplied application and deployment group','Intended EC2 targets and revision; approved service role; installed agent','appspec.yml: revision files → destinations; supplied hook scripts','Inspect this revision’s hook results and target files'],c,an)
 if i==2:
  a=assets['img.scaling_bounded_timeline'];return {'type':'annotated_image','asset_id':a['asset_id'],'alt_text':a['alt_text'],'lineage':lin(c,anchors=an)}
 if i==3:return pair(table('ds.repository_access_tests',c,['principal','repository','operation','repository_grant']),table('ds.repository_access_tests',c,['principal','identity_authentication_action','identity_authentication_allowed','expected_result','observed_result']),'Repository grants','Authentication and tests','Authentication and repository authorization need separate evidence.',c,an)
 if i==4:
  v=table('ds.retention_preview',c);v['lineage']['anchors']=an;return v
 if i==5:return diagram('Routing and health review',['Supplied listener protocol/port and routing rule','Registered target group protocol/port','Backend health-check path, port and success codes','Endpoint test and target health reasons','Normally healthy targets; all registered targets unhealthy → fail open to those targets'],c,an)
 if i==6:return diagram('Log retention state',['Intended log group: default indefinite retention','put-retention-policy with supplied interval','Inspect retentionInDays','Expired events marked for deletion','Physical deletion typically takes up to 72 hours'],c,an)
 if i==7:return diagram('Separate restore verification',['Intended source DB instance','Manual snapshot: wait for available','New DB identifier + supplied network settings','Separate restored instance: wait for available','Restored endpoint → supplied recovery-marker query'],c,an)
 if i==8:return pair(table('ds.log_access_tests',c,['principal','read_operation','resource_scope','scope_reason']),table('ds.log_access_tests',c,['principal','approved_reader','read_operation','expected_result','observed_result']),'Required actions and supported scopes','Access boundary tests','Collecting logs does not itself authorize a reader.',c,an)
 if i==9:return pair(table('ds.ecs_configuration_evidence',c,['evidence_stage','task_definition','name','image','containerPort','hostPort','cpu','memory','launch_type']),table('ds.ecs_configuration_evidence',c,['evidence_stage','task_definition','task_id','status','image','cpu','memory','launch_type','cluster','network_configuration']),'Registered specification','Observed task evidence','Match runtime details with the supplied specification and launch type.',c,an)
 if i==10:return diagram('Request-specific denial review',['Principal + operation + resource + context','Applicable identity, resource, session, boundary and organization policies','Explicit deny / missing allow / unsatisfied condition; denial context','Explicit deny takes precedence','Smallest approved correction → same-operation retest'],c,an)
 if i==11:return pair(table('ds.reviewed_plan_comparison',c,['evidence_stage','plan_file','approved','AMI','instance_type','placement']),table('ds.reviewed_plan_comparison',c,['evidence_stage','plan_file','instance_id','AMI','instance_type','placement','execution_command','apply_outcome']),'Approved saved plan','Execution and resource evidence','Compare the created instance with the approved saved plan.',c,an)
 if i==12:
  v=table('ds.command_invocations',c);v['lineage']['anchors']=an;return v
 if i==13:return {'type':'code_walkthrough','language':'bash','code':'# Static checks where backend access is unnecessary\nterraform init -backend=false &&\nterraform validate &&\nterraform fmt -check\n# Only after blocking checks pass: supplied approved apply step','annotations':[{'start_line':2,'end_line':2,'text':'Initialize needed providers and modules.'},{'start_line':3,'end_line':3,'text':'Nonzero validation blocks progression; correct the supplied declaration and rerun.'},{'start_line':4,'end_line':4,'text':'Additional blocking canonical-format check, not remote-state verification.'},{'start_line':5,'end_line':5,'text':'Static success and provisioning success are distinct evidence.'}],'reveal':'all','lineage':lin(c,anchors=an)}
result={k:plan[k] for k in ['schema_version','path_id','batch_id']};result['kind']='screens_part';result['tiles']=[]
for t in plan['tiles']:
 tc=t['concept_ids']; title=t['title'] if t['title']!=t['tile_id'] else B[tc[0]]['context']['concept_name'].split(' after external')[0]
 out={'tile_id':t['tile_id'],'title':title,'summary':' '.join(recaps[I[c]] for c in tc),'steps':[],'remediation_steps':[]}
 seen=set()
 for ps in t['steps']:
  c=ps['concept_ids'][0];i=I[c];fs=ps['fact_ids'];ts=ps['teaching_block_ids'];typ=ps['type']
  s={'step_id':ps['step_id'],'type':typ,'concept_ids':copy.deepcopy(ps['concept_ids']),'eyebrow':{'explainer':'Understand the evidence','video':'Evidence walkthrough','check':'Check your judgement','hands_on':'Evidence review','recap':'Takeaways'}[typ],'title':title,'lineage':{'concept_ids':copy.deepcopy(ps['concept_ids']),'fact_ids':copy.deepcopy(fs),'teaching_block_ids':copy.deepcopy(ts),'anchors':copy.deepcopy(ps['anchors']),'segment_ids':copy.deepcopy(ps['segment_ids'])}}
  if typ in ['check','hands_on']:
   s['title']=('Review ' if typ=='hands_on' else 'Judge ')+['buildspec evidence','deployment evidence','bounded scaling evidence','repository access evidence','retention preview evidence','listener and health-check evidence','log-retention evidence','snapshot and restore evidence','log-reader access evidence','ECS task evidence','IAM denial evidence','saved-plan execution evidence','per-node command evidence','configuration-gate evidence'][i]
   s['lede']='Read the supplied excerpts in this step and decide which claims or configurations are correct, defective or unsafe.'
   key=(c,tuple(fs))
   if key not in seen:
    seen.add(key); rts=[c+'#tb'+str(j) for j in [2,3,4,5]]
    r={'step_id':t['tile_id']+f'.r{len(out["remediation_steps"])+1:02d}','type':'remediation','concept_ids':[c],'title':contrasts[i],'eyebrow':'One contrast','lineage':lin(c,copy.deepcopy(fs),rts),'blocks':[]}
    for f in fs:
     j=int(f.split('#f')[1])-1
     r['blocks'].append(prose(facts[i][j],c,[f],rts,'mechanism'))
    r['blocks'].append(prose(examples[i],c,fs,rts,'example'))
    out['remediation_steps'].append(r)
  elif typ=='video':
   s['title']='Trace the supplied evidence';s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
  elif typ=='explainer':
   s['title']=(B[c]['context']['concept_name'].split(' after external')[0] if '#tb1' in ''.join(ts) else contrasts[i]);s['blocks']=[]
   if any(x.endswith('#tb1') for x in ts):
    for j,f in enumerate(facts[i]):
     s['blocks'].append(prose(f,c,[c+f'#f{j+1}'],ts,'definition' if j==0 else 'mechanism'))
    if any(x.endswith('#tb4') for x in ts):s['blocks'].append(prose(examples[i],c,fs,ts,'example'))
   else:
    # The detailed example screen retains the operating facts while distinguishing evidence.
    s['blocks'].append(prose(examples[i],c,fs,ts,'example'))
    for j,f in enumerate(facts[i]):s['blocks'].append(prose(f,c,[c+f'#f{j+1}'],ts,'mechanism'))
   if ps['planned_visual_block_type']:s['blocks'].append(visual(ps))
   if i==13:
    s['blocks'].append(pair(diagram('Invalid declaration case',['Supplied invalid aws_instance declaration','Blocking validation: nonzero exit prevents apply'],c),diagram('Corrected declaration case',['Supplied correction to aws_instance declaration','Rerun static checks before supplied approved apply','Retain provisioning evidence separately'],c),'Configuration defect','Correction and recheck','A formatting-only change is separate from correcting an invalid declaration.',c,[c+'#visual']))
  elif typ=='recap':
   s['title']='Keep these checks separate';s['blocks']=[]
   for rc in tc:
    rfs=[rc+'#'+f['id'] for f in B[rc]['coverage']['required_facts']];rts=[rc+'#'+b['id'] for b in B[rc]['teaching_blocks']]
    s['blocks'].append(prose(recaps[I[rc]],rc,rfs,rts,'takeaway'))
   nxt=next((x for x in plan['tiles'] if x['tile_id']==t['next_tile_id']),None)
   if nxt:
    nc=nxt['concept_ids'][0]; up=B[nc]['context']['concept_name'].split(' after external')[0]; first=facts[I[nc]][0]
    s['blocks'].append({'type':'up_next','title':up,'text':first})
   else:s['blocks'].append({'type':'up_next','title':t['next_tile_id'],'text':'Continue to the next tile.'})
  for j,block in enumerate(s.get('blocks',[])):block['block_id']=s['step_id']+f'.b{j+1:02d}'
  out['steps'].append(s)
 for r in out['remediation_steps']:
  for j,block in enumerate(r['blocks']):block['block_id']=r['step_id']+f'.b{j+1:02d}'
 result['tiles'].append(out)
(P/'screens.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('tiles',len(result['tiles']),'steps',sum(len(t['steps']) for t in result['tiles']),'remediation',sum(len(t['remediation_steps']) for t in result['tiles']))
for t,ot in zip(plan['tiles'],result['tiles']):
 for ps,s in zip(t['steps'],ot['steps']):
  wc=sum(len(b.get('text','').split()) for b in s.get('blocks',[]))
  if ps['word_budget'] and wc>ps['word_budget']:print('OVER',s['step_id'],wc,ps['word_budget'])
