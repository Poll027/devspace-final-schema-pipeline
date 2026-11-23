import json, re, copy
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.05_2')
plan=json.load(open(P/'tile_plans.json'))
g=json.load(open(P/'inputs/path_glossary_bundle.json'))
reg=json.load(open(P/'scenario_asset_registry.json'))
bs={b['context']['concept_id']:b for b in g['bundles']}
# Authored screen voice; placeholder vocabulary remains the glossary's vocabulary.
content={
'inject_a_controlled_failure_and_verify_alarm_behavior':(
'Configuration alone does not demonstrate behavior under disruption. Before the approved sandbox fault, define its limited scope, expected signals and abort conditions. During the fault, inspect alarm state history and actual notification receipt. Then remove the fault and verify recovery.',
['Keep the sandbox record in order: approved limits, fault, alarm behavior, notification receipt, then recovery. An absent notification is a result to preserve, not a successful test inferred from configuration.', 'If an abort condition is reached, follow the approved stop path. Do not extend the fault to obtain a desired alarm. Retain missed signals, absent notifications and unsuccessful recovery honestly; this exercise does not authorize production disruption.'],
'Alarm configuration is not proof of notification receipt or recovery.'),
'perform_a_lambda_version_and_alias_release_with_rollback':(
'A published Lambda version freezes function code and most configuration. The alias is movable: it selects a published version for invocations. Use aws lambda publish-version --function-name NAME, then aws lambda update-alias --function-name NAME --name ALIAS --function-version VERSION. Test NAME:ALIAS. For rollback, point the alias at the approved previous version and repeat verification.',
['Record the alias target before release, after release and after rollback. The supplied NAME:ALIAS test checks the version selected by that alias; an unqualified function invocation is not that test.', 'Rollback changes the alias target, not the immutable published snapshot. Inspect the target and repeat the supplied result check for the approved previous version. A version captures most configuration, not every possible configuration property.'],
'Changing the alias target is not editing the published version.'),
'perform_a_managed_eks_deployment_rollout':(
'A Deployment Pod-template change creates a rollout revision; scaling alone does not. Update the supplied image with kubectl set image deployment/NAME CONTAINER=IMAGE and monitor kubectl rollout status deployment/NAME. On the controlled failure, inspect rollout history, restore the approved prior revision with kubectl rollout undo deployment/NAME --to-revision=REVISION, and verify readiness.',
['Keep the failed revision evidence separate from the approved rollback revision. Use the supplied procedure to select the authorized prior revision, rather than choosing an arbitrary history entry.', 'After undo, inspect readiness. An accepted undo request is not evidence that the restored template’s Pods satisfy the supplied readiness check. Scaling changes alone do not create a new Pod-template revision.'],
'An undo request is not the same as verified readiness.'),
'perform_an_ec2_blue_green_deployment_with_codedeploy':(
'EC2 blue/green installs a revision on replacement instances before traffic leaves the original instances. Use the supplied deployment group, replacement fleet and load balancer configuration. Check lifecycle and health evidence before approved rerouting. For rollback, follow the supplied configuration or redeployment procedure and verify both traffic and application behavior return to the known-good revision.',
['Installation evidence shows the replacement revision is present; it does not show which fleet clients reach. Preserve lifecycle and health evidence before the approved traffic switch.', 'After the switch and after rollback, check client-visible behavior as well as traffic. Rerouting alone does not establish correct application behavior. Follow the supplied rollback path; do not infer automatic rollback or guaranteed zero disruption.'],
'Installation evidence is not client traffic or application-behavior evidence.'),
'perform_cleanup_after_supplied_script_failure':(
'Python finally runs when control leaves try, including after an exception. Put the supplied failing task in try and scoped cleanup calls in finally. Track identities created by this exercise, clean up only those identities, and verify both their removal and preservation of preexisting resources.',
['Use the supplied scaffolding and cleanup calls. Track created identities at the exercise boundary instead of reconstructing ownership from similar resource names after failure.', 'A preexisting resource with a shared label must remain untouched. The postcheck must confirm removal of exercise-created resources and preservation of preexisting ones. finally controls when cleanup runs; it does not make an overbroad cleanup safe.'],
'finally guarantees block execution here, not safe target selection.'),
'reconcile_terraform_ec2_drift':(
'Terraform normally refreshes tracked resources before planning, exposing relevant out-of-band changes. Compare observed EC2 settings with configuration and choose an approved intent: restore the declaration or update it. Inspect a new plan, follow the approval/apply workflow, and verify live settings. Refresh-only planning proposes state and output updates; planning does not persist them. Applying the approved refresh-only plan persists those updates without restoring remote infrastructure to configuration.',
['Keep observed drift, approved intent, planned action and the final live comparison together. Accepting a setting requires an approved declaration change; restoring it requires the appropriate reviewed action.', 'Refresh-only planning does not persist state or output changes. Applying its approved plan persists those updates, but does not change the remote instance to repair drift. Verify live settings against the chosen declaration after the supplied workflow.'],
'Refresh-only state/output updates are not remote repair.'),
'reuse_a_supplied_terraform_module_provisioning_ec2':(
'A module packages resource declarations behind inputs and outputs. Configure module "NAME" with the supplied source and named input arguments; reference its declared output as module.NAME.OUTPUT. Initialize the module, inspect inputs and planned instance settings, apply through the approved workflow, then verify the created instance and declared outputs.',
['The supplied module interface is not proof that its input values are correct. Compare inputs and planned EC2 settings with the approved requirement before apply. Keep the declared output tied to the verified instance rather than treating an output reference as live verification.'],
'A reusable module does not replace plan review or live verification.'),
'rightsize_a_resource_using_a_supplied_workload_baseline':(
'Rightsizing matches resource type and size to workload performance and capacity requirements, not simply the smallest instance. Compare supplied load, utilization and performance with service constraints. Recommend a smaller instance only if those constraints remain satisfied. Include peak and changing demand; one low-utilization sample is not enough.',
['Compare the current size and smaller candidate across normal, peak and changing demand. Keep observed load, measured utilization and latency separate from the recommendation they support.', 'The current peak reaches the supplied latency boundary. The smaller candidate’s peak and changing-demand latency exceed the supplied bound, so the normal sample cannot justify that reduction. Preserve the constraints and withhold the unsupported reduction; do not invent a price comparison.'],
'A low normal sample is not sufficient evidence for a smaller size.'),
'route_a_security_finding_with_evidence_to_its_responsible_owner':(
'Resource identity, severity and activity details give the accountable responder context. Send the supplied finding ID or evidence link, affected resource, observed activity and urgency to the responsible owner, using the established escalation path. Preserve the finding evidence; suspicious activity is not an unsupported conclusion that the resource is compromised.',
['Use the registered finding’s reported severity and urgency. Preserve its activity description and evidence reference so the accountable owner can inspect it. Follow the supplied escalation route if the owner is unavailable; a concise handoff must not erase context or exaggerate the evidence.'],
'A report of suspicious activity is not a supported compromise conclusion.'),
'route_an_operational_event_to_a_notification_or_established_systems_manager_action':(
'An EventBridge rule pairs a pattern with one or more targets for matching events. Set the supplied event bus and pattern, adding only the approved SNS or Systems Manager target and required parameters. Configure the target’s required permissions. Send matching and nonmatching test events and inspect execution or notification evidence at the approved target.',
['Compare matching and nonmatching test results with the intended rule selection. Pattern matching in isolation does not complete the routing check: inspect execution or notification evidence at the approved target. Keep the required target authorization model and parameters with that evidence.'],
'A pattern match alone is not verified target execution or notification.'),
'run_an_ecs_service_with_a_desired_task_count':(
'An ECS service maintains the desired task count and replaces stopped or failed tasks. Create it with the supplied cluster, task definition, network settings and desiredCount. In the controlled exercise, remove the one approved task, then inspect service events and running/pending task counts until the desired count is restored.',
['The task definition supplies what runs; the service maintains how many tasks are requested. Observe the controlled task loss, replacement progress and restored running count. Keep service events and running/pending counts in the record rather than assuming service creation proves replacement.'],
'A service definition is not evidence that the desired running count was restored.')}

def lineage(c,tbs,facts,anchors=None):
 d={'concept_ids':[c],'teaching_block_ids':tbs,'fact_ids':facts}
 if anchors is not None:d['anchors']=anchors
 return d

def prose(text,lin,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lin)}

def diagram(labels,lin,title):
 nodes=[{'id':f'n{i+1}','label':label} for i,label in enumerate(labels)]
 return {'type':'diagram','diagram_kind':'sequence','title':title,'nodes':nodes,'edges':[{'from':a['id'],'to':b['id'],'directed':True} for a,b in zip(nodes,nodes[1:])], 'alt_text':'; '.join(labels),'lineage':copy.deepcopy(lin)}

def visual(c,typ,lin):
 key=c.split('.')[-1]; vl=copy.deepcopy(lin);vl['anchors']=[c+'#visual']
 if typ=='data_table':
  asset=next(a for a in reg['assets'] if ('sizing' in a['asset_id'])==('rightsize' in key))
  return {'type':'data_table','asset_ref':{'asset_id':asset['asset_id'],'columns':[x['name'] for x in asset['columns']]},'caption':asset['title'],'lineage':vl}
 if typ=='annotated_image':
  labels={
   'inject_a_controlled_failure_and_verify_alarm_behavior':['Before fault: approved scope, signals, abort conditions','During fault: alarm state history and notification receipt','After removal: recovery check; preserve unsuccessful outcomes'],
   'perform_a_managed_eks_deployment_rollout':['Image update: CONTAINER=IMAGE','Observe rollout status and revision history','Undo to approved REVISION','Check post-rollback readiness'],
   'route_an_operational_event_to_a_notification_or_established_systems_manager_action':['Setup: supplied bus and pattern','Approved target: required parameters and permissions','Test: matching and nonmatching events','Inspect: target execution or notification evidence'],
   'run_an_ecs_service_with_a_desired_task_count':['Before removal: supplied desiredCount; inspect running/pending counts','Controlled loss: remove one approved task','Replacement: inspect service events and running/pending counts','Recovery: verify running count restored to desiredCount']
  }[key]
  return diagram(labels,vl,'Evidence to inspect')
 if typ=='before_after':
  if 'lambda' in key:
   before=['Same ALIAS → approved previous published version','NAME:ALIAS: inspect supplied test result','Published snapshots remain immutable']
   after=['Same ALIAS → newly approved published version; inspect NAME:ALIAS test','Rollback: same ALIAS → approved previous version; repeat test','Published snapshots remain immutable']
   change='The alias target moves; published snapshots do not change.'
  else:
   before=['Configuration: declared EC2 setting','Live instance: observed out-of-band setting','Decision: restore declaration or approve an intended change']
   after=['Chosen declaration → newly reviewed plan → approved apply','Final check: live EC2 setting matches chosen declaration','Refresh-only apply updates state/outputs, not remote infrastructure']
   change='Resolve the approved intent and verify live settings; distinguish refresh-only from remote repair.'
  return {'type':'before_after','before':diagram(before,vl,'Before'),'after':diagram(after,vl,'After'),'change_summary':change,'lineage':vl}
 if typ=='process_flow':
  labels=['Original fleet serves traffic','Install revision on supplied replacement fleet','Verify replacement lifecycle and health evidence','Approved load balancer traffic rerouting','Verify client traffic and application behavior','Supplied rollback/redeployment path: verify known-good traffic and behavior']
  nodes=[{'id':f'n{i+1}','label':x} for i,x in enumerate(labels)]
  return {'type':'process_flow','direction':'TB','alt_text':'; '.join(labels),'nodes':nodes,'edges':[{'from':a['id'],'to':b['id']} for a,b in zip(nodes,nodes[1:])],'lineage':vl}
 if typ=='code_walkthrough':
  if 'cleanup' in key:
   code='try:\n    # Supplied failing task; track exercise-created identities.\n    pass\nfinally:\n    # Supplied cleanup calls: only tracked exercise-created identities.\n    pass\n# Postcheck: verify removal and preservation of preexisting resources.'
   lang='python'; notes=[(1,3,'The supplied task belongs in try; an exception still leads to finally.'),(4,6,'The supplied cleanup calls must be scoped to tracked exercise-created identities.'),(7,7,'This schematic shows required postchecks, not a computed result.')]
  else:
   code='# Interface schematic, not a shell command:\n# module "NAME" {\n#   source = <supplied source>\n#   <named input argument> = <supplied value>\n# }\n# module.NAME.OUTPUT'
   lang='bash';notes=[(3,4,'Use the supplied source and named inputs; inspect the planned EC2 settings.'),(6,6,'Reference the declared output and verify it with the created instance after approved apply.')]
  return {'type':'code_walkthrough','language':lang,'code':code,'annotations':[{'start_line':a,'end_line':b,'text':text} for a,b,text in notes],'lineage':vl}
 raise ValueError(typ)

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for t in plan['tiles']:
 tile={'tile_id':t['tile_id'],'title':' / '.join(bs[c]['context']['concept_name'] for c in t['concept_ids']),'steps':[],'remediation_steps':[]}
 seen=set()
 for sp in t['steps']:
  c=sp['concept_ids'][0];b=bs[c];key=c.split('.')[-1]; intro,examples,contrast=content[key]
  lin={'concept_ids':sp['concept_ids'],'teaching_block_ids':sp['teaching_block_ids'],'fact_ids':sp['fact_ids'],'segment_ids':sp['segment_ids'],'anchors':sp['anchors']}
  s={'step_id':sp['step_id'],'type':sp['type'],'concept_ids':sp['concept_ids'],'lineage':copy.deepcopy(lin),'eyebrow':{'explainer':'Understand','check':'Check your understanding','hands_on':'Review the evidence','recap':'Takeaways'}.get(sp['type'],'Review')}
  if sp['type'] in ['check','hands_on']:
   s['title']={
    'inject_a_controlled_failure_and_verify_alarm_behavior':'Review the fault-test record',
    'perform_a_lambda_version_and_alias_release_with_rollback':'Review the alias release and rollback',
    'perform_a_managed_eks_deployment_rollout':'Review the rollout and readiness evidence',
    'perform_an_ec2_blue_green_deployment_with_codedeploy':'Review the fleet and traffic evidence',
    'perform_cleanup_after_supplied_script_failure':'Judge the cleanup scope',
    'reconcile_terraform_ec2_drift':'Review the drift-resolution record',
    'reuse_a_supplied_terraform_module_provisioning_ec2':'Review the module interface and verification',
    'rightsize_a_resource_using_a_supplied_workload_baseline':'Review the sizing evidence',
    'route_a_security_finding_with_evidence_to_its_responsible_owner':'Review the finding handoff',
    'route_an_operational_event_to_a_notification_or_established_systems_manager_action':'Review the event route',
    'run_an_ecs_service_with_a_desired_task_count':'Review task-count restoration'
   }[key]
   if sp['planned_interaction_type'] in ['classify','choice']:
    s['lede']='Read the supplied excerpt(s) in this step and decide which are correct, defective or unsafe.'
   else:s['lede']='Inspect the supplied evidence and select the supported recommendation or handoff.'
   signature=(c,tuple(sp['fact_ids']))
   if signature not in seen:
    seen.add(signature)
    facts=[f for f in b['coverage']['required_facts'] if c+'#'+f['id'] in sp['fact_ids']]
    tbs=[c+'#'+tb['id'] for tb in b['teaching_blocks'] if any(f['id'] in tb['fact_ids'] for f in facts)]
    rl=lineage(c,tbs,sp['fact_ids'])
    r={'step_id':t['tile_id']+f'.r{len(tile["remediation_steps"])+1:02d}','type':'remediation','concept_ids':[c],'title':'Contrast: evidence versus assumption','eyebrow':'Try this distinction','lineage':rl,'blocks':[]}
    for f in facts:
     fl=lineage(c,[c+'#'+tb['id'] for tb in b['teaching_blocks'] if f['id'] in tb['fact_ids']],[c+'#'+f['id']])
     r['blocks'].append(prose(f['statement'],fl,'definition'))
    r['blocks'].append(prose(contrast,rl,'misconception'))
    if sp['planned_interaction_type'] not in ['classify','choice']:
     r['blocks'].append(visual(c,'data_table',rl))
    tile['remediation_steps'].append(r)
  elif sp['type']=='explainer':
   first=any(x.endswith('#tb1') for x in sp['teaching_block_ids']); combined=any(x.endswith('#tb4') for x in sp['teaching_block_ids'])
   s['title']='Operating model' if first else 'Keep the evidence distinct'
   s['blocks']=[]
   if first:
    # Split at sentence boundaries, each prose block stays under 90 words.
    sentences=re.split(r'(?<=[.!?])\s+',intro); chunks=[]; chunk=''
    for sentence in sentences:
     if len((chunk+' '+sentence).split())>85 and chunk:chunks.append(chunk);chunk=''
     chunk=(chunk+' '+sentence).strip()
    if chunk:chunks.append(chunk)
    s['blocks'] += [prose(x,lin) for x in chunks]
   if (not first) or combined:s['blocks'] += [prose(x,lin,'example') for x in examples]
   if sp['planned_visual_block_type']:s['blocks'].append(visual(c,sp['planned_visual_block_type'],lin))
  elif sp['type']=='video':
   s['title']='Follow the sequence';s['blocks']=[{'type':'media_group','segment_ids':sp['segment_ids']}]
  elif sp['type']=='recap':
   s['title']='What to carry forward';s['blocks']=[]
   takeaways={
    'inject_a_controlled_failure_and_verify_alarm_behavior':'Bound the fault first. Verify alarm history, actual notification receipt and recovery.',
    'perform_a_lambda_version_and_alias_release_with_rollback':'Lambda rollback moves the alias to an approved previous immutable version; repeat the alias test.',
    'perform_a_managed_eks_deployment_rollout':'EKS rollback restores an approved template revision; verify readiness.',
    'perform_an_ec2_blue_green_deployment_with_codedeploy':'EC2 blue/green needs replacement health evidence before traffic moves, plus verified known-good behavior after rollback.',
    'perform_cleanup_after_supplied_script_failure':'Use finally for supplied cleanup, scope it to exercise-created identities, and verify preexisting resources remain.',
    'reconcile_terraform_ec2_drift':'Choose approved intent, inspect a new plan, apply through approval and verify live settings. Refresh-only apply updates state/outputs, not remote infrastructure.',
    'reuse_a_supplied_terraform_module_provisioning_ec2':'Use supplied module inputs and declared outputs; review planned settings and verify the created instance after approved apply.',
    'rightsize_a_resource_using_a_supplied_workload_baseline':'Match size to requirements across normal, peak and changing demand. A low sample alone cannot justify a reduction.',
    'route_a_security_finding_with_evidence_to_its_responsible_owner':'Preserve finding context and evidence, route to the accountable owner and follow established escalation without exaggerating activity.',
    'route_an_operational_event_to_a_notification_or_established_systems_manager_action':'Use the approved target, parameters and permissions. Verify matching and nonmatching tests with target evidence.',
    'run_an_ecs_service_with_a_desired_task_count':'The service replaces stopped or failed tasks. Verify restoration through events and running/pending counts after controlled removal.'}
   for cid in t['concept_ids']:
    bb=bs[cid];rl=lineage(cid,[cid+'#'+tb['id'] for tb in bb['teaching_blocks']],[cid+'#'+f['id'] for f in bb['coverage']['required_facts']])
    s['blocks'].append(prose(takeaways[cid.split('.')[-1]],rl,'takeaway'))
   nxt=next((x for x in plan['tiles'] if x['tile_id']==t['next_tile_id']),None)
   if nxt:next_name=bs[nxt['concept_ids'][0]]['context']['concept_name']
   else:
    # Next tile is outside this batch; use the supplied glossary name, not invented teaching.
    next_name=g['names']['aws_devops.run_supplied_unit_and_integration_tests_as_blocking_pipeline_gates']
   s['blocks'].append({'type':'up_next','title':'Up next','text':next_name})
  tile['steps'].append(s)
 out['tiles'].append(tile)
# Deterministic author checklist: plan fidelity, framing only, qualified lineage,
# budgets, self-contained prose, registered data columns, and visual anchors.
for t,pt in zip(out['tiles'],plan['tiles']):
 assert [(s['step_id'],s['type']) for s in t['steps']]==[(s['step_id'],s['type']) for s in pt['steps']]
 for s,sp in zip(t['steps'],pt['steps']):
  for k in ['concept_ids','teaching_block_ids','fact_ids']:assert s['lineage'][k]==sp[k]
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s and 'interaction' not in s
  else:
   count=sum(len(x['text'].split()) for x in s['blocks'] if x['type'] in ['prose','up_next'] and 'text' in x)
   assert count<=sp['word_budget'],(s['step_id'],count,sp['word_budget'])
 def check_block(bl):
  if bl['type']=='prose':
   assert bl.get('lineage');assert len(bl['text'].split())<=90
   assert 'video' not in bl['text'].lower()
  if bl['type'] not in ['prose','up_next','media_group']:assert any(a.endswith('#visual') for a in bl['lineage']['anchors'])
  for f in bl.get('lineage',{}).get('fact_ids',[]):assert '#f' in f
  assert not any(k in bl for k in ['result','output','computed_values','execution_provenance'])
  if bl['type']=='data_table':
   a=next(a for a in reg['assets'] if a['asset_id']==bl['asset_ref']['asset_id']);assert set(bl['asset_ref']['columns'])<=set(x['name'] for x in a['columns'])
  for k in ['before','after']:
   if k in bl:check_block(bl[k])
 for s in t['steps']+t['remediation_steps']:
  for bl in s.get('blocks',[]):check_block(bl)
(P/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('tiles',len(out['tiles']),'steps',sum(len(t['steps']) for t in out['tiles']),'remediation',sum(len(t['remediation_steps']) for t in out['tiles']))
