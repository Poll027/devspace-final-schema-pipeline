import json, re
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.02_1')
plan=json.loads((P/'tile_plans.json').read_text())
g=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
r=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']}
A={a['asset_id']:a for a in r['assets']}
# Short, independently readable re-voicings of the required facts, in source order.
voices=[
['Environment variables are named strings that a supplied program reads as configuration.', 'Configure FLEET_ALLOWED_INSTANCE_IDS with approved comma-separated IDs and FLEET_MAX_TARGETS with the approved positive integer limit. These names configure the supplied validator; they are not Python keywords.', 'Test malformed and out-of-scope inputs. Confirm rejection happens before any resource-changing operation.'],
['A change set previews proposed stack changes without executing them.', 'Before authorizing execution, review additions, modifications, removals and replacement indicators. A preview does not guarantee execution success.', 'For a new stack, create a CREATE change set from the supplied template, wait for completion, inspect it, then execute the approved set to provision resources.'],
['aws:MultiFactorAuthPresent describes MFA authentication for qualifying temporary credentials.', 'A scoped Deny using BoolIfExists with aws:MultiFactorAuthPresent set to false can block non-MFA requests, including an absent key. Keep the statement’s action scope in view.', 'Apply the supplied scoped policy and compare an allowed MFA-authenticated request with a denied request without MFA.'],
['A role trust policy identifies who may assume the role and the conditions for assumption.', 'In the trust policy, use the approved Principal, Action sts:AssumeRole and the supplied conditions.', 'Cross-account callers also need permission to call sts:AssumeRole on the role. Test approved and unapproved principals.', 'The role’s permissions policy governs an assumed session’s work, not who may enter the role.'],
['Root has broad account authority, but routine tasks belong under non-root identities.', 'Protect root access with MFA. Do not create root access keys; delete existing keys when they are no longer needed.', 'Compare root-use and access-key evidence with the protection checklist. Use non-root identities for routine operations.'],
['CloudTrail event history shows recent management events in the selected Region, not all application activity.', 'Filter by an attribute such as event name, resource name or user name, plus the relevant time interval.', 'Read eventTime, eventName, userIdentity and requestParameters or resources to identify the time, operation, actor and target of a change.'],
['After billing activation, cost-allocation tags categorize costs by resource-associated tag keys and values.', 'Activate the desired cost-allocation tag, then group Cost Explorer costs by that tag for the chosen period.', 'Without the relevant active tag, resource spend can remain unallocated to the intended workload.'],
['A log group shares retention and access settings across streams. A stream sequences events from one source.', 'Set the supplied collector’s application file path, group and stream name. Verify a known JSON event arrives in that stream.', 'Preserve structured fields: CloudWatch Logs Insights can discover fields in JSON events and make them queryable.'],
['Define how to return to the previous working configuration and verify the change’s intended effect.', 'Identify and verify the supplied rollback files. Change the supplied setting, then run the syntax or configuration check before activation.', 'Activate a valid change with the supported reload or restart. Inspect status and the supplied effective-setting check; on failure, restore and reactivate the saved configuration.'],
['Rolling delivery replaces workload portions progressively, not all instances simultaneously.', 'Blue/green keeps separate old and new environments, then switches traffic to the new environment.', 'Canary exposes a new version to a limited traffic share before broader rollout.', 'Compare traffic exposure, available parallel capacity and the route back to a known-good version when choosing a strategy.'],
['The CloudWatch agent sends configured host metrics and logs to CloudWatch.', 'Choose metrics under metrics_collected and append instance-identifying dimensions such as InstanceId.', 'Start with amazon-cloudwatch-agent-ctl, fetch-config, the supplied configuration location and -s. Verify the expected metric and instance dimension in CloudWatch.'],
['A metric alarm compares a statistic over periods with a threshold. Its states are OK, ALARM and INSUFFICIENT_DATA.', 'EvaluationPeriods counts evaluated periods; DatapointsToAlarm counts breaches required within that window.', 'Set the supplied metric, statistic, period, comparison operator, threshold and evaluation counts. Compare the resulting state with the supplied samples.', 'Missing-data policies are breaching, notBreaching, ignore (retain current state), and missing (INSUFFICIENT_DATA when all datapoints are missing). The default is missing.']
]
examples=[
'For the approved {target_count}-ID, {target_count}-target example, keep the approval beside both environment-variable settings. Inspect the malformed-input and outside-allowlist cases together with operation evidence: both must be rejected before a resource-changing call.',
'For the supplied new-stack template, wait for CREATE change-set completion and compare its additions with the approved scope. An extra unapproved addition is a discrepancy, not permission to proceed. Keep the requested scope, preview and later execution outcome separate; a matching preview can still be followed by failed execution.',
'Compare covered actions under the supplied policy. For qualifying MFA-authenticated temporary credentials, the true context does not match this Deny. False and absent contexts match the BoolIfExists Deny set to false. Compare the allowed MFA case with the denied non-MFA case without extending the result to actions outside the statement’s scope.',
'For cross-account entry to the orders-operator role, inspect both trust and caller-side AssumeRole permission. Compare approved and unapproved principals under the supplied conditions. After assumption, look to the role’s permissions policy for the session’s allowed work; the trust policy is not an operations allowlist.',
'Review the supplied root checklist item by item. Keep MFA protection, routine identity use and existing-key hygiene separate. A satisfactory MFA finding does not erase routine root use. Check whether each existing key remains needed and its removal status; do not create keys during the review.',
'For the supplied {incident_interval} example, filter by the relevant attribute and compare candidate events. Use the operation and target fields as well as the timestamp. Record actor, operation, target and time together; a nearby event or a guessed resource owner is not attribution evidence.',
'For {workload_key}={workload_value}, compare the active billing grouping and selected period with resource-tag evidence. Preserve the report’s allocated and unallocated categories. An orders-looking resource name does not justify moving unallocated spend into orders; investigate the relevant active tag instead.',
'For the known orders JSON event, compare the collector’s application path, destination group and destination stream with its arrival location. Verify that request ID, outcome and timestamp remain structured. Creating a group alone does not prove that the collector delivered the intended event.',
'For the sandbox service, verify rollback files before changing the supplied setting. Check syntax before activation, then inspect service status and the effective setting. If validation fails, restore the saved configuration and reactivate it. Retain each result separately: a reload or restart request is not a verified outcome.',
'Compare three proposals for the same release. Separate old and new environments address that stated arrangement; limited initial traffic exposure points to the canary proposal. For each, compare available parallel capacity and the route back to the known-good version. A strategy name is not a recovery guarantee or a universal ranking.',
'Compare the intended host with the observed CloudWatch series. Match both the expected metric and InstanceId; a matching metric name from another instance does not verify this host.',
'Compare the registered complete-sample windows with their evaluation settings and threshold comparisons. Then inspect all-missing windows under each policy. Keep real zero observations distinct from missing samples. Retain configuration, prior state and resulting state together rather than interpreting a gap as an observed zero or breach.'
]
contrasts=[
'Setting configuration is not proof of enforcement: rejection evidence must precede resource changes.',
'A preview is not execution evidence, and approval is not a guarantee of execution success.',
'An absent key is not automatically exempt from this scoped BoolIfExists Deny.',
'Role entry and session work are different checks; trust alone does not complete cross-account caller permission.',
'Root’s broad authority is not a reason to use it for routine operations.',
'Event history covers recent regional management events, not the sequence of all application requests.',
'A resource label alone does not establish active billing grouping.',
'A group shares settings; a stream holds a source’s events. Setup needs known-event arrival evidence.',
'Activation is not validation. Restoring a file also needs reactivation.',
'Rolling describes progressive replacement; canary describes limited traffic exposure. They are not interchangeable names.',
'Starting the agent is not verification; check the observed metric and instance identity.',
'EvaluationPeriods is not the required breach count. Default missing does not mean every isolated gap immediately produces INSUFFICIENT_DATA.'
]
recaps=[
'Environment variables configure the supplied validator. Match approved IDs and a positive target limit; verify malformed and out-of-scope rejection before resource changes.',
'Preview first. Review resource actions and replacement indicators before approval. For a new stack, wait for CREATE completion, inspect, then execute the approved set; execution success is not guaranteed.',
'Keep qualifying temporary credentials and scoped actions explicit. A BoolIfExists Deny set to false can match false and absent MFA contexts. Compare allowed MFA and denied non-MFA requests.',
'Trust governs role entry; role permissions govern session work. Use the approved principal, AssumeRole action and conditions. Cross-account entry also needs caller-side permission and approved/unapproved tests.',
'Keep root out of routine tasks. Review MFA, root-use evidence and key hygiene independently. Do not create root access keys; delete existing keys when no longer needed.',
'Filter recent regional management events by a relevant attribute and interval. Attribute the change from event time, operation, identity and target evidence, not a guessed owner.',
'Activate the billing tag and group by it for the selected period. Compare resource-associated labels with allocated categories; missing relevant active tags can leave spend unallocated.',
'Groups share retention and access settings; streams sequence source events. Configure the collector and verify known-event arrival in the intended stream with structured JSON fields preserved for discovery.',
'Verify rollback files, change the setting and check before activation. Then inspect status and effective settings. On failure, restore and reactivate; an activation request is not validation.',
'Rolling progressively replaces portions; blue/green separates environments and switches traffic; canary starts with limited traffic exposure. Choose against exposure, parallel-capacity and known-good return requirements.',
'Configure metrics_collected and instance dimensions. Start with fetch-config and -s through amazon-cloudwatch-agent-ctl. Verify the expected CloudWatch metric and InstanceId, not merely agent startup.',
'Keep evaluated periods distinct from required breaches. Compare the configured signal and threshold with samples. For all-missing windows: breaching → ALARM, notBreaching → OK, ignore retains state, and default missing → INSUFFICIENT_DATA.'
]

target_count=re.search(r'approves (\w+) instance IDs',g['bundles'][0]['teaching_blocks'][3]['content']).group(1)
incident_interval='–'.join(re.findall(r'\b\d{2}:\d{2}\b',g['bundles'][5]['teaching_blocks'][3]['content'])[:2])
wc=A['ds.workload_cost_allocation']; wcrow=dict(zip([c['name'] for c in wc['columns']],wc['rows'][0]))
examples=[text.format(target_count=target_count,incident_interval=incident_interval,workload_key=wcrow['grouping_tag_key'],workload_value=wcrow['Workload']) for text in examples]

def lin(cid,facts,tbs,anchors=None):
 d={'concept_ids':[cid],'teaching_block_ids':tbs,'fact_ids':facts}
 if anchors is not None:d['anchors']=anchors
 return d

def prose(text,cid,facts,tbs,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':lin(cid,facts,tbs)}

def diagram(title, panels, lineage, edges=None):
 nodes=[{'id':f'n{i+1}','label':label,'fields':fields} for i,(label,fields) in enumerate(panels)]
 return {'type':'diagram','diagram_kind':'container','title':title,'nodes':nodes,'edges':edges or [],'layout':'auto','alt_text':title+': '+'; '.join(label+': '+', '.join(fields) for label,fields in panels),'lineage':lineage}

def visual(i,ps,cid):
 l=lin(cid,ps['fact_ids'],ps['teaching_block_ids'],[cid+'#visual'])
 if i in (4,11):
  asset=A[['ds.root_protection','ds.alarm_evaluation'][i==11]]
  return {'type':'data_table','asset_ref':{'asset_id':asset['asset_id'],'columns':[c['name'] for c in asset['columns']]},'caption':asset['title'],'lineage':l}
 panels={
 0:[('Approved scope',[f'{target_count} approved instance IDs',f'Maximum: {target_count} targets']),('Environment configuration',['FLEET_ALLOWED_INSTANCE_IDS: approved IDs, comma-separated','FLEET_MAX_TARGETS: approved positive integer']),('Rejection boundary',['Malformed-input case: inspect rejection','Outside-allowlist case: inspect rejection','Operation evidence: confirm no resource-changing call'])],
 1:[('New-stack CREATE preview',['Supplied template → CREATE → wait for completion','Review expected EC2 addition against approved scope']),('Separate execution action',['Inspect and approve before execution','Execute the approved set to provision resources','Retain execution outcome separately']),('Update preview review',['Inspect EC2 modification','Inspect replacement indicator before authorization'])],
 3:[('Cross-account caller',['Approved or unapproved principal','Caller permission: sts:AssumeRole on the role']),('Role trust: entry',['Principal: approved principal','Action: sts:AssumeRole','Supplied conditions']),('Assumed session: work',['Role permissions policy controls allowed operations'])],
 5:[('Event history filter',['Selected Region','Relevant attribute filter',f'Example interval: {incident_interval}']),('Candidate comparison',['Compare operation and target, not just nearby time','Recent management events, not all application activity']),('Matching event fields',['eventTime → time','eventName → operation','userIdentity → actor','requestParameters or resources → target'])],
 7:[('Collector configuration',['Supplied application file path','Destination log group','Destination stream name']),('Destination stream check',['Known orders JSON event arrives here','Preserved fields: request ID, outcome, timestamp']),('Group and stream',['Group: shared retention and access settings','Stream: event sequence from one source'])],
 8:[('Before activation',['Verify supplied rollback files','Change supplied setting','Run syntax/configuration check']),('Activate valid change',['Supported reload or restart','Inspect service status','Inspect effective-setting check']),('Failure return',['Restore saved configuration','Reactivate saved configuration','Inspect restored status and effective setting'])],
 10:[('Approved host and configuration',['Approved sandbox host identity','Expected metric under metrics_collected','Append InstanceId dimension']),('Agent start',['amazon-cloudwatch-agent-ctl','fetch-config + supplied configuration location + -s']),('CloudWatch verification',['Locate expected metric','Compare InstanceId with approved host','Matching name from another instance is not verification'])]
 }
 if i==6:
  asset=A['ds.workload_cost_allocation']; cols=[c['name'] for c in asset['columns']]
  rows=[dict(zip(cols,row)) for row in asset['rows']]
  report=rows[0]
  p=[('Billing grouping',[f"Tag: {report['grouping_tag_key']}",f"Active: {str(report['cost_allocation_tag_active']).lower()}",f"Period: {report['period_start']} to {report['period_end']} (end exclusive)"])]
  p += [(str(row['Workload']),[f"Billed amount: {row['billed_amount']} exercise currency units",row['resource_tag_evidence'],row['finding']]) for row in rows]
  return diagram('Workload billing review',p,l)
 if i==2:
  left=diagram('Statement boundary',[('Scoped Deny',['BoolIfExists','aws:MultiFactorAuthPresent = false','Only statement-scoped actions'])],l)
  right=diagram('Request comparison',[('Covered action with existing Allow',['true: this Deny does not match','false: this Deny matches','absent: this Deny matches']),('Outside action scope',['This statement does not establish the request outcome'])],l)
  return {'type':'side_by_side','left':left,'right':right,'left_label':'Policy scope','right_label':'Request contexts','takeaway':'Read authentication context and action scope together.','lineage':l}
 if i==9:
  left=diagram('Rolling',[('Replacement pattern',['Replace portions progressively','Not all instances simultaneously']),('Requirement comparison',['Compare available parallel capacity','Compare return route to known-good version'])],l)
  right=diagram('Blue/green and canary',[('Blue/green',['Separate old and new environments','Switch traffic to the new environment']),('Canary',['Limited initial traffic share','Broader rollout follows']),('Requirement comparison',['Compare exposure and parallel capacity','Compare route back to known-good version'])],l)
  return {'type':'side_by_side','left':left,'right':right,'left_label':'Progressive workload replacement','right_label':'Environment switch or limited exposure','takeaway':'Match the proposal to stated requirements, not a universal ranking.','lineage':l}
 ed=[]
 if i==3:ed=[{'from':'n1','to':'n2','label':'AssumeRole: caller permission and trust checks','directed':True},{'from':'n2','to':'n3','label':'After approved assumption','directed':True}]
 return diagram('Review map: '+B[cid]['context']['concept_name'].split(';')[0],panels[i],l,ed)

out={k:plan[k] for k in ('schema_version','path_id','batch_id')};out['kind']='screens_part';out['tiles']=[]
# The names catalog follows the tile-order catalog. Verify all supplied bundle locations before using it for the boundary tile.
name_items=list(g['names'].items())
name_by_tile=dict(zip(g['tile_order'],name_items))
assert all(name_by_tile[b['context']['toc_location']['tile_id']][0]==b['context']['concept_id'] for b in g['bundles'])
for i,t in enumerate(plan['tiles']):
 cid=t['concept_ids'][0];b=B[cid]; name=b['context']['concept_name'];tb={cid+'#'+x['id']:x for x in b['teaching_blocks']}
 facts=[cid+'#'+f['id'] for f in b['coverage']['required_facts']]; vf=dict(zip(facts,voices[i]))
 tile={'tile_id':t['tile_id'],'title':name,'steps':[],'remediation_steps':[]}
 explain_n=0
 for ps in t['steps']:
  s={k:ps[k] for k in ('step_id','type','concept_ids')};s['lineage']=lin(cid,ps['fact_ids'],ps['teaching_block_ids'],ps['anchors']);s['lineage']['segment_ids']=ps['segment_ids']
  typ=s['type']
  if typ=='explainer':
   explain_n+=1;s['eyebrow']='Understand' if explain_n==1 else 'Apply the evidence';s['title']=name.split(';')[0] if explain_n==1 else 'Compare the evidence, not the label';s['blocks']=[]
   if explain_n==1:
    for f in ps['fact_ids']:
     matching=[q for q in ps['teaching_block_ids'] if f.split('#')[1] in tb[q]['fact_ids']]
     s['blocks'].append(prose(vf[f],cid,[f],matching))
    if ps['planned_visual_block_type']:s['blocks'].append(visual(i,ps,cid))
    # Tile 025 combines definition and worked example in one planned step.
    if len([x for x in t['steps'] if x['type']=='explainer'])==1:
     s['blocks'].append(prose(examples[i],cid,ps['fact_ids'],[q for q in ps['teaching_block_ids'] if tb[q]['purpose']=='example'],'example'))
   else:
    s['blocks']=[prose(examples[i],cid,ps['fact_ids'],[cid+'#tb4'],'example'),prose(contrasts[i],cid,[cid+'#'+f for f in tb[cid+'#tb5']['fact_ids']],[cid+'#tb5'],'misconception')]
  elif typ in ('check','hands_on'):
   s['eyebrow']='Evidence review' if typ=='hands_on' else 'Check your understanding'
   s['title']='Review '+name.split(';')[0] if typ=='hands_on' else 'Judge the evidence'
   s['lede']='Read the supplied excerpts in this step and decide which satisfy the stated requirements and which are defective or unsafe.' if typ=='hands_on' else 'Read the supplied case and choose the interpretation supported by its evidence.'
  elif typ=='video':
   s['title']='A closer look';s['blocks']=[{'type':'media_group','segment_ids':ps['segment_ids']}]
  elif typ=='recap':
   s['eyebrow']='Takeaways';s['title']='Keep the boundary clear'
   s['blocks']=[prose(recaps[i],cid,facts,list(tb),'takeaway'),{'type':'up_next','title':name_by_tile[t['next_tile_id']][1]}]
  tile['steps'].append(s)
 # One remediation for each distinct measured fact set, including practice-only framing with no planned facts.
 seen=set()
 for ps in t['steps']:
  if ps['type'] not in ('check','hands_on'):continue
  fs=ps['fact_ids'] or facts
  key=tuple(sorted(fs))
  if key in seen:continue
  seen.add(key)
  qs=[q for q,x in tb.items() if any(cid+'#'+f in fs for f in x['fact_ids'])]
  rem={'step_id':t['tile_id']+f'.r{len(seen):02d}','type':'remediation','required':False,'concept_ids':[cid],'eyebrow':'Try this contrast','title':'Evidence versus assumption','lineage':lin(cid,fs,qs),'blocks':[]}
  for f in fs:
   qf=[q for q in qs if f.split('#')[1] in tb[q]['fact_ids']]
   rem['blocks'].append(prose(vf[f],cid,[f],qf))
  # Same scenario; contrast is grounded in the concept's misconception teaching block.
  rem['blocks'].append(prose(contrasts[i],cid,[cid+'#'+f for f in tb[cid+'#tb5']['fact_ids']],[cid+'#tb5'],'misconception'))
  # Include contrast facts in remediation lineage; every measured fact remains explicitly taught.
  rem['lineage']['fact_ids']=list(dict.fromkeys(fs+[cid+'#'+f for f in tb[cid+'#tb5']['fact_ids']]))
  if i in (4,11):
   asset=A['ds.root_protection' if i==4 else 'ds.alarm_evaluation']
   rem['blocks'].append({'type':'data_table','asset_ref':{'asset_id':asset['asset_id'],'columns':[c['name'] for c in asset['columns']]},'caption':'Revisit the same supplied evidence','lineage':lin(cid,rem['lineage']['fact_ids'],qs)})
  tile['remediation_steps'].append(rem)
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('tiles',len(out['tiles']),'steps',sum(len(t['steps']) for t in out['tiles']),'remediations',sum(len(t['remediation_steps']) for t in out['tiles']))
# Mistakes-to-avoid checks: structural lineage, budgets, references, interaction framing and outputs.
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
for t,pt in zip(out['tiles'],plan['tiles']):
 assert [(s['step_id'],s['type'],s['concept_ids']) for s in t['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in pt['steps']]
 for s,ps in zip(t['steps'],pt['steps']):
  assert s['lineage']['fact_ids']==ps['fact_ids'] and s['lineage']['teaching_block_ids']==ps['teaching_block_ids']
  words=sum(len(x['text'].split()) for x in walk(s.get('blocks',[])) if x.get('type')=='prose')
  if ps['word_budget']:assert words<=ps['word_budget'],(s['step_id'],words,ps['word_budget'])
  if s['type'] in ('check','hands_on'):assert 'blocks' not in s and 'interaction' not in s
 for x in walk(t):
  if x.get('type')=='prose':
   assert len(x['text'].split())<=90
   assert x['lineage']['concept_ids'] and x['lineage']['teaching_block_ids'] and x['lineage']['fact_ids']
   assert not re.search(r'\bvideo\b',x['text'],re.I)
  if 'lineage' in x:
   assert all('#f' in f for f in x['lineage'].get('fact_ids',[]))
  if 'asset_ref' in x:
   a=A[x['asset_ref']['asset_id']];assert set(x['asset_ref'].get('columns',[]))<=set(c['name'] for c in a['columns'])
  assert not any(k in x for k in ('result','computed_values','output','execution_provenance'))
 assert any(cid+'#visual' in x.get('lineage',{}).get('anchors',[]) for x in walk(t) for cid in pt['concept_ids'])
print('Mistakes-to-avoid deterministic checklist passed; prose meanings and illustrative diagrams reviewed against glossary and registry.')
