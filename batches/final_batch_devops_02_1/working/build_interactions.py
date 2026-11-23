import json, re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.02_1')
load=lambda n: json.loads((B/n).read_text())
plans=load('tile_plans.json'); screens={t['tile_id']:t for t in load('screens.json')['tiles']}; bundles={b['context']['concept_id']:b for b in load('inputs/path_glossary_bundle.json')['bundles']}; assets={a['asset_id']:a for a in load('scenario_asset_registry.json')['assets']}
def rows(a):
 a=assets[a]; return [dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
def choice(prompt,opts):
 # Each authored option couples the judgement with its factual explanation; derive key from its correctness tag.
 options=[{'option_id':f'o{i+1}','text':x[0]} for i,x in enumerate(opts)]
 return {'prompt':prompt,'options':options,'selection':'single','shuffle':True},{'correct_option_ids':[o['option_id'] for o,x in zip(options,opts) if x[1]],'option_feedback':{o['option_id']:{'message':x[2]} for o,x in zip(options,opts)}}
def classify(prompt, buckets, cases):
 items=[]; assigns={}; feedback={}; rolemap={}
 for i,(text,role,why,source) in enumerate(cases):
  it={'item_id':f'i{i+1}','text':text}
  if source:
   it['source']=source
   col=next(c for c in assets[source['asset_id']]['columns'] if c['name']==source['column'])
   rolemap[role]=col['semantic_role']
  items.append(it); assigns[it['item_id']]=role; feedback[it['item_id']]={'message':why}
 gr={'assignments':assigns,'item_feedback':feedback}
 if rolemap: gr['role_map']=rolemap
 return {'prompt':prompt,'buckets':[{'bucket_id':k,'label':v} for k,v in buckets.items()],'items':items},gr
checks={
'015':[
('A malformed-input test is rejected, but the operation trace shows a resource-changing call before rejection. What does this establish?', [('The required rejection boundary failed.',True,'Malformed input must be rejected before any resource-changing operation.'),('The test passed because rejection eventually occurred.',False,'A late rejection does not meet the before-mutation requirement.'),('The configuration names alone establish safe enforcement.',False,'Configuration is not proof; the rejection case and operation evidence must agree.')]),
('An input contains an instance ID outside the approved allowlist. Which verification result meets the required boundary?', [('Validator rejects it and the trace shows no resource-changing call.',True,'Out-of-scope input must be rejected before mutation.'),('Validator rejects it after a resource-changing call.',False,'Rejection after mutation violates the boundary.'),('Validator accepts it because its ID is well formed.',False,'Well-formed input can still be outside the approved scope.')])],
'016': [('Read this update preview:\n```text\nOrdersHost: AWS::EC2::Instance\nAction: Modify\nReplacement: True\nPreview creation: CREATE_COMPLETE\nApproval: replacement is unintended\n```\nWhich judgement follows?', [('Withhold execution authorization: the EC2 modification indicates replacement.',True,'Review the action and replacement indicator against approved scope before execution.'),('Authorize it because Modify rules out replacement.',False,'A modification can carry a replacement indicator; this excerpt explicitly does.'),('Authorize it because preview success guarantees execution success.',False,'A preview is not execution and does not guarantee execution success.')])],
'017': [('For a statement-scoped action, an existing Allow applies. The only relevant Deny uses BoolIfExists with aws:MultiFactorAuthPresent = false. The request has no such context key. Which outcome follows?', [('Denied by the supplied statement.',True,'The scoped BoolIfExists Deny set to false also covers an absent key.'),('Allowed because absence always avoids BoolIfExists.',False,'This Deny also covers the absent-key case within its action scope.'),('Denied for every action, even outside the statement scope.',False,'The statement only establishes a denial for its scoped actions.')])],
'018': [('Which policy answers who may enter orders-operator, rather than what an assumed session may do?', [('The role trust policy and its conditions.',True,'Trust identifies permitted principals and assumption conditions.'),('Only the role permissions policy.',False,'Role permissions govern the assumed session’s operations, not who may enter.'),('Only the caller’s permissions, without role trust.',False,'Cross-account assumption also requires role trust and its conditions.')])],
'019': [('Root MFA is enabled, but the checklist records root performing routine operations. How should that use be judged?', [('A routine-root-use violation; use non-root identities for routine work.',True,'Root has broad authority and should not perform routine tasks.'),('Acceptable because MFA removes the routine-use restriction.',False,'MFA protection and routine-root-use findings are separate checks.'),('Acceptable if no root access key was created.',False,'Key hygiene does not make routine root operations appropriate.')])],
'020': [('A nearby CloudTrail event has the requested operation but a different target. What is the defensible attribution decision?', [('Compare operation and target, then record actor and time from the matching event.',True,'Attribution requires eventName, target fields, userIdentity and eventTime together.'),('Use the closest timestamp regardless of target.',False,'Timestamp proximity alone cannot establish the requested change.'),('Use the resource’s apparent owner instead of userIdentity.',False,'The event’s userIdentity supplies actor evidence; an assumed owner is not attribution.')])],
'021': [('A Cost Explorer report grouped by the active Workload tag includes spend from orders-untagged with Workload absent. How should that spend be treated?', [('Keep it unallocated and investigate missing tag evidence.',True,'Without the relevant active tag, spend can remain unallocated to the intended workload.'),('Assign it to orders from the resource name alone.',False,'Resource-associated tag evidence, not a suggestive name, establishes billing allocation.'),('Claim activation necessarily allocates every resource.',False,'Activation does not supply a missing resource tag value.')])],
'022': [('The orders collector is configured, but the known JSON event is found only in a different stream. What does the evidence establish?', [('Arrival in the intended stream is not verified.',True,'Verify the known event’s arrival in the configured group and stream.'),('The intended stream is verified because its group exists.',False,'Group creation does not prove event delivery to the intended stream.'),('Any stream in the group proves the intended source arrived.',False,'A stream is an event sequence from one source; the intended destination matters.')])],
'023': [('After activation, service status is running but the effective-setting check fails. Which response meets the taught failure procedure?', [('Restore the saved configuration, reactivate it, and verify status and the previous effective setting.',True,'Failure recovery requires restoration, reactivation and outcome checks.'),('Restore the file without reactivation or checks.',False,'Restoring a file alone does not verify the active configuration.'),('Ignore the failed setting check because status is running.',False,'Running status is not proof that the intended setting is effective.')])],
'024': [('Read these supplied proposals:\n```text\nRequirement: initial new-version traffic <=10%; extra capacity <= one full workload; retain a return route to known-good.\nRolling: first batch 25%; extra capacity one batch; replace changed portions to return.\nBlue/green: switch 100%; extra capacity one full workload; switch back to retained old environment.\nCanary: initial 10%; extra capacity 10% workload; route back to retained known-good.\n```\nWhich proposal meets all requirements?', [('Canary: limited exposure fits the bound and the retained version supplies the return route.',True,'This proposal matches exposure, capacity and the stated return arrangement.'),('Blue/green: a return route makes the 100% switch meet the 10% bound.',False,'Its return route does not remove the initial exposure violation.'),('Rolling: progressive replacement necessarily means at most 10% initial traffic.',False,'The supplied first batch exposes 25%; progressive replacement alone does not meet the bound.')])],
'025': [('The agent starts successfully, but the expected metric appears with an InstanceId different from the approved host. Which judgement follows?', [('Source verification failed despite successful start.',True,'Verify the expected metric and matching instance dimension in CloudWatch.'),('Start success proves the expected metric’s source.',False,'Agent start and metric/source verification are distinct evidence.'),('The metric name alone proves the approved host sent it.',False,'The instance-identifying dimension must match the approved host.')])],
'026': [('All evaluated datapoints are missing and the alarm’s policy is ignore. Its supplied current state is ALARM. What state should the all-missing evaluation retain?', [('ALARM.',True,'ignore retains the supplied current state.'),('OK.',False,'notBreaching, not ignore, yields OK for the all-missing window.'),('INSUFFICIENT_DATA.',False,'missing yields INSUFFICIENT_DATA when all datapoints are missing; ignore retains state.')])]
}
# Non-executable cases are authored evidence excerpts, not executable assets.
case_sets={
'015': ('Read each supplied validator review. Decide whether its configuration AND both rejection boundaries meet the approval. Approval: i-00000000000000001,i-00000000000000002; maximum targets 2.', [
("FLEET_ALLOWED_INSTANCE_IDS='i-00000000000000001,i-00000000000000002'\nFLEET_MAX_TARGETS='2'\nmalformed: REJECTED; resource-changing calls=0\nout-of-scope i-00000000000000003: REJECTED; resource-changing calls=0",'meets','Both string configuration values match approval; both cases reject before mutation.',None),
("FLEET_ALLOWED_INSTANCE_IDS='i-00000000000000001,i-00000000000000002,i-00000000000000003'\nFLEET_MAX_TARGETS='2'\nmalformed: REJECTED; resource-changing calls=0\nout-of-scope i-00000000000000003: ACCEPTED; resource-changing calls=1",'fails','The configuration expands approved scope and the out-of-scope case is not rejected.',None),
("FLEET_ALLOWED_INSTANCE_IDS='i-00000000000000001,i-00000000000000002'\nFLEET_MAX_TARGETS='2'\nmalformed: REJECTED; resource-changing calls=1 before rejection\nout-of-scope i-00000000000000003: REJECTED; resource-changing calls=0",'fails','Matching configuration does not excuse mutation before malformed-input rejection.',None)]),
'016': ('Read each CloudFormation review record. Decide whether it meets the supplied approval: CREATE provisions only one sandbox EC2 instance after inspection and approval; unintended update replacement is not authorized. Distinguish preview from execution.',[
('CREATE set orders-create: CREATE_COMPLETE; inspected: OrdersHost Add AWS::EC2::Instance, one instance only; scope approved; execute orders-create after approval: complete, one sandbox EC2 instance provisioned. Separate update: OrdersHost Modify, Replacement=True; replacement unintended; execution withheld. Preview success was not treated as an execution guarantee.','meets','Inspection and scope approval precede execution of the specific set; the update replacement is withheld.',None),
('CREATE set orders-create: CREATE_COMPLETE; inspected: OrdersHost Add AWS::EC2::Instance; execution not requested. Review conclusion: preview alone provisioned one instance and guarantees successful execution. Update: Modify, Replacement=True; unintended replacement withheld.','fails','A change set preview does not execute or provision resources and cannot guarantee execution success.',None),
('CREATE set orders-create inspected and approved for one EC2 instance, then executed successfully. Separate update: OrdersHost Modify AWS::EC2::Instance, Replacement=True; approval excludes replacement; authorized anyway because Action=Modify.','fails','The replacement indicator must be reviewed even for Modify; unintended replacement is not authorized.',None)]),
'017': ('Read the scoped-policy request records and decide whether each recorded outcome follows the supplied policy. The unchanged Deny covers only ec2:StopInstances, uses BoolIfExists aws:MultiFactorAuthPresent=false, and an existing Allow covers the test requests; no other Deny applies.',[
('Policy applied unchanged. Action=ec2:StopInstances; aws:MultiFactorAuthPresent=true; recorded result=Allow.','meets','MFA true does not match this Deny; the existing Allow covers the request.',None),
('Policy applied unchanged. Action=ec2:StopInstances; aws:MultiFactorAuthPresent=false; recorded result=Deny.','meets','The scoped Deny matches non-MFA context false.',None),
('Policy applied unchanged. Action=ec2:StopInstances; aws:MultiFactorAuthPresent=absent; recorded result=Deny.','meets','BoolIfExists Deny set to false also covers absence for scoped actions.',None),
('Policy applied unchanged. Action=ec2:StopInstances; aws:MultiFactorAuthPresent=absent; recorded result=Allow because absent keys bypass BoolIfExists.','fails','An absent key does not bypass this scoped Deny.',None),
('Supplied Deny action=ec2:StopInstances; applied Deny action=ec2:*; true request allowed, false request denied. Review claims action scope was preserved.','fails','The applied statement expands scope; correct sample outcomes do not establish unchanged scope.',None)]),
'018': ('Read each cross-account role review and decide whether it satisfies the supplied approval. Only the supplied approved orders-operator caller may enter; Action must remain sts:AssumeRole and supplied conditions must be preserved. The approved caller must have permission on this role and both caller tests must be retained.',[
('Trust Principal=only approved orders-operator caller; Action=sts:AssumeRole; supplied conditions unchanged. Caller permission=sts:AssumeRole on this role. Approved caller with conditions met: succeeds. Unapproved caller: rejected. Both outcomes retained.','meets','The trust, caller permission and paired test outcomes meet the approval.',None),
('Trust Principal=only approved orders-operator caller; Action=sts:AssumeRole; supplied conditions unchanged. Approved cross-account caller permission on this role: absent. Claimed result: approved caller succeeds because role permissions allow EC2 work. Unapproved caller rejected.','fails','Session permissions do not replace the cross-account caller’s AssumeRole permission.',None),
('Trust Principal=approved caller plus unapproved caller; Action=sts:AssumeRole; supplied conditions removed. Both callers succeed.','fails','Trust must preserve the approved principal boundary and supplied conditions; the unapproved caller should be rejected.',None)]),
'020': ('Read the event-history filter and records. Decide which event matches the supplied change, not merely a nearby timestamp. Region us-east-1; filter Event name=StopInstances; interval 2026-01-15 09:00–09:15 UTC; change: StopInstances on i-00000000000000001. Each record supplies actor, operation, target and time.',[
('Region=us-east-1; eventTime=2026-01-15T09:05:00Z; eventName=StopInstances; userIdentity=arn:aws:iam::111122223333:user/orders-operator; requestParameters.instanceId=i-00000000000000002','fails','The target differs, so timestamp proximity does not identify the supplied change.',None),
('Region=us-east-1; eventTime=2026-01-15T09:10:00Z; eventName=StopInstances; userIdentity=arn:aws:iam::111122223333:user/orders-operator; requestParameters.instanceId=i-00000000000000001','meets','The Region, interval, operation and target match; userIdentity records the actor.',None),
('Region=us-east-1; eventTime=2026-01-15T09:10:00Z; eventName=StartInstances; userIdentity=arn:aws:iam::111122223333:user/orders-operator; requestParameters.instanceId=i-00000000000000001','fails','The operation differs despite matching target and time.',None)]),
'022': ('Read each collection record. Decide whether it verifies the known event at the intended destination with its structured fields preserved. Required file /var/log/orders/application.json; group /orders/sandbox; stream orders-host-a; event request_id=orders-001, outcome=success, timestamp=2026-01-15T09:10:00Z.',[
('collector: file=/var/log/orders/application.json; group=/orders/sandbox; stream=orders-host-a\narrival: group=/orders/sandbox; stream=orders-host-a\nJSON={"request_id":"orders-001","outcome":"success","timestamp":"2026-01-15T09:10:00Z"}','meets','The known structured event arrives in the configured group and stream.',None),
('collector: file=/var/log/orders/application.json; group=/orders/sandbox; stream=orders-host-a\narrival: group=/orders/sandbox; stream=orders-host-b\nJSON={"request_id":"orders-001","outcome":"success","timestamp":"2026-01-15T09:10:00Z"}','fails','The intended stream is not the observed stream.',None),
('collector: file=/var/log/orders/application.json; group=/orders/sandbox; stream=orders-host-a\narrival: group=/orders/sandbox; stream=orders-host-a\nJSON={"message":"orders event"}','fails','The known request ID, outcome and timestamp are not preserved as structured fields.',None)]),
'023': ('Read each service-change record and decide whether it follows the validation and recovery procedure. Designated setting: request_timeout_seconds 30→45 in /etc/orders/service.conf; saved previous file /etc/orders/service.conf.saved. Other settings must remain unchanged.',[
('Saved file verified as previous working configuration before edit; only request_timeout_seconds changed to 45; config check PASS before supported reload; status running; effective-setting check PASS, observed 45.','meets','Rollback verification, bounded edit, pre-activation check and both outcome checks are present.',None),
('Saved file verified before edit; only request_timeout_seconds changed to 45; config check PASS before supported reload; status running; effective-setting FAIL, observed 30 instead of 45. Saved file restored; supported reload completed; status running; effective-setting PASS, observed previous value 30.','meets','The failed effect triggers restoration and reactivation, then checks confirm the previous working state.',None),
('Saved file verified before edit; only request_timeout_seconds changed to 45; config check PASS; reload completed; status running; effective-setting FAIL. Saved file copied back; no reactivation or outcome checks performed.','fails','Restoration alone does not confirm the active prior configuration; reactivation and checks are required.',None),
('Saved file verified before edit; only request_timeout_seconds changed to 45; config check FAIL; supported reload performed anyway; status running.','fails','A passing configuration check must precede activation; running status does not cure this failure.',None)]),
'025': ('Read each host telemetry record. Decide whether configuration, start and CloudWatch verification all meet the requirement: mem_used_percent from approved host i-00000000000000001, profile /opt/orders/agent.json.',[
('profile: metrics_collected selects mem_used_percent; append_dimensions includes InstanceId\nstart: amazon-cloudwatch-agent-ctl fetch-config, location=/opt/orders/agent.json, -s; result started\nCloudWatch: mem_used_percent; InstanceId=i-00000000000000001','meets','Required metric selection, identifying dimension, supplied start and matching CloudWatch evidence are all present.',None),
('profile: metrics_collected selects mem_used_percent; append_dimensions includes InstanceId\nstart: amazon-cloudwatch-agent-ctl fetch-config, location=/opt/orders/agent.json, -s; result started\nCloudWatch: mem_used_percent; InstanceId=i-00000000000000002','fails','The observed instance dimension does not match the approved host.',None),
('profile: metrics_collected selects mem_used_percent; append_dimensions absent\nstart: amazon-cloudwatch-agent-ctl fetch-config, location=/opt/orders/agent.json, -s; result started\nCloudWatch: mem_used_percent; no InstanceId dimension','fails','The profile and observed metric lack the required instance-identifying dimension.',None)])
}
out={k:plans[k] for k in ['schema_version','path_id','batch_id']}; out.update(kind='interactions_part',tiles=[])
for tile in plans['tiles']:
 tid=tile['tile_id']; n=tid[-3:]; cid=tile['concept_ids'][0]; bundle=bundles[cid]; stlist=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]; authored=[]; ci=0
 for j,s in enumerate(stlist):
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if j==0 else ('stretch' if s['type']=='hands_on' else 'core'),'grading_mode':'client','standalone':True,'anchors':s['anchors'],'measures':[]}
  aa=[a for a in s['anchors'] if '#assessment:' in a]
  # Truncated anchor IDs are generated by the planner; match their original capability using its own helper.
  import sys
  sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
  from finlib import assessment_ref
  for a in bundle['assessment_anchors']:
   if assessment_ref(cid,a['capability']) in aa: ix['measures'].append({'concept_id':cid,'capability':a['capability'],'fact_ids':a['fact_ids']})
  if not ix['measures'] and s['type']=='hands_on':
   ix['measures']=[{'concept_id':cid,'capability':a['capability'],'fact_ids':a['fact_ids']} for a in bundle['assessment_anchors']]
  if s['type']=='check':
   pub,gr=choice(*checks[n][ci]); ci+=1
  elif n in case_sets:
   prompt,cases=case_sets[n]; labels={'meets':'Meets the supplied criterion','fails':'Violates the supplied criterion'}
   if n=='020': labels={'meets':'Matches the supplied change','fails':'Does not match the supplied change'}
   pub,gr=classify(prompt,labels,cases)
  elif n=='019':
   cases=[]
   for r in rows('ds.root_protection'):
    # key hygiene must distinguish obsolete and still-needed keys as the fact states.
    role='violates' if r['record_id']=='routine-root' else 'meets'
    if r['record_id']=='key-needed': role='needed'
    text='\n'.join(f'{k}: {r[k]}' for k in ['checklist_item','identity_or_key','evidence','key_remains_needed','removal_status'])
    cases.append((text,role,r['finding'],{'asset_id':'ds.root_protection','row':{'where':{'record_id':r['record_id']},'occurrence':0},'column':'evidence'}))
   pub,gr=classify('Read the root-protection evidence. Judge MFA, routine identity use and key hygiene separately. Classify a still-needed existing key separately from an obsolete-key removal; do not infer that MFA permits routine root work.',{'meets':'Meets the relevant checklist criterion','violates':'Routine-root-use violation','needed':'Existing key still marked needed; not the obsolete-key removal case'},cases)
  elif n=='021':
   cases=[]
   for r in rows('ds.workload_cost_allocation'):
    role='unallocated' if r['Workload']=='unallocated' else 'allocated'
    text='\n'.join(f'{k}: {v}' for k,v in r.items() if k!='finding')
    cases.append((text,role,r['finding'],{'asset_id':'ds.workload_cost_allocation','row':{'where':{'Workload':r['Workload']},'occurrence':0},'column':'resource_tag_evidence'}))
   pub,gr=classify('Read each billing category from the selected period grouped by the active Workload cost-allocation tag. Decide which allocated charges to preserve and which spend to leave unallocated pending tag investigation; resource names are not allocation evidence.',{'allocated':'Preserve the reported allocated workload charge','unallocated':'Keep unallocated and investigate missing tag evidence'},cases)
  elif n=='026':
   cases=[]
   for r in rows('ds.alarm_evaluation'):
    visible={k:v for k,v in r.items() if k not in ['resulting_state','breach_count','period_1_comparison','period_2_comparison','period_3_comparison']}
    text='Saved configuration and supplied evaluation window:\n'+'\n'.join(f'{k}: {v}' for k,v in visible.items())
    cases.append((text,r['resulting_state'],'Complete windows use the required observed breach count; all-missing windows apply the named policy, and ignore retains the prior state.',{'asset_id':'ds.alarm_evaluation','row':{'where':{'window_id':r['window_id']},'occurrence':0},'column':'resulting_state'}))
   pub,gr=classify('Read the saved alarm configuration and samples in each excerpt and decide the resulting state. The supplied required settings are metric orders_host_signal, Average, period 60 seconds, GreaterThanThreshold 60, EvaluationPeriods 3 and DatapointsToAlarm 2; the policy is the one named per test. null means missing, not zero. Compare the settings before evaluating complete and all-missing windows.',{k:k for k in ['OK','ALARM','INSUFFICIENT_DATA']},cases)
  elif n=='024':
   # Upstream registry has no delivery proposal dataset. Preserve planned interaction type and expose the missing dependency rather than silently substituting unrelated billing data.
   prompt=checks[n][0][0].split('Which proposal')[0]+'Select the proposal meeting all requirements, then select its return-route evidence and the exposure evidence that rules out each alternative.'
   pub={'asset_ref':{'asset_id':'ds.delivery_proposals'},'intro':prompt,'tasks':[{'task_id':'select_proposal','prompt':'Select the proposal whose initial exposure, capacity and return arrangement meet every requirement.','target_kind':'row'}]}
   # The row label is copied from the authored screen, not guessed from memory.
   def nodes(b):
    yield from b.get('nodes',[])
    for k in ['left','right']:
     if isinstance(b.get(k),dict): yield from nodes(b[k])
   label=next(nd['label'] for st in screens[tid]['steps'] for b in st.get('blocks',[]) for nd in nodes(b) if nd['label']=='Canary')
   gr={'answers':[{'task_id':'select_proposal','row':{'where':{'strategy':label},'occurrence':0}}],'task_feedback':{'select_proposal':{'correct':'The supplied canary exposure and retained-version return arrangement satisfy the requirements within available capacity.','incorrect':'The supplied rolling first batch and blue/green switch exceed the initial traffic bound; a return route alone does not remove that violation.'}}}
  else: raise ValueError(n)
  ix.update(public=pub,grading=gr)
  facts={f['id']:f['statement'] for f in bundle['coverage']['required_facts']}
  explanation=' '.join(facts[f] for f in dict.fromkeys(f for m in ix['measures'] for f in m['fact_ids']))
  ix['feedback']={'correct':{'message':'Correct. '+explanation},'incorrect':{'message':'Compare the supplied evidence with the required criterion. '+explanation},'hints':['Separate the configuration or approval from the recorded outcome.','Check every named criterion, not only a successful status or familiar label.']}
  if j==0:
   rem=next((r for r in screens[tid].get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem: ix['feedback']['remediation_step_id']=rem['step_id']
  authored.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tid,'interactions':authored})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
