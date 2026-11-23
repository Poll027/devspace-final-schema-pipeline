import json, ipaddress
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.01_1')
plan=json.loads((P/'tile_plans.json').read_text()); screens=json.loads((P/'screens.json').read_text()); reg=json.loads((P/'scenario_asset_registry.json').read_text()); glossary=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
bs={b['context']['concept_id']:b for b in glossary['bundles']}; sc={t['tile_id']:t for t in screens['tiles']}; assets={a['asset_id']:a for a in reg['assets']}
def rows(a):
 d=assets[a];return [dict(zip([c['name'] for c in d['columns']],r)) for r in d['rows']]
def ref(row,cols):return {'where':{c:row[c] for c in cols},'occurrence':0}
# Each option has an explicit truth annotation: keys are derived from these annotations.
choices={
'000':('The approved profile is lab-operator. Which command explicitly selects that named profile for the caller check?',[
('aws sts get-caller-identity --profile lab-operator',True,'--profile selects the named credential and configuration group.'),
('aws sts get-caller-identity --region lab-operator',False,'--region selects a Region, not a named profile.'),
('aws sts get-caller-identity',False,'This command does not explicitly select the supplied named profile.')]),
'001':('Which subnet assignment violates the single-Availability-Zone boundary?',[
('One subnet is assigned across both Zone A and Zone B.',True,'A subnet resides entirely in one Availability Zone.'),
('One subnet is assigned to Zone A and a separate subnet to Zone B.',False,'Separate subnets are the taught way to serve different Availability Zones.'),
('Two separate, nonoverlapping subnets are assigned to Zone A.',False,'Each still resides entirely in one Availability Zone; this is not the boundary violation asked about.')]),
'002':('A team requires Kubernetes APIs and ecosystem and is willing to operate Kubernetes workloads. Which selection fits those constraints while preserving the taught responsibility boundary?',[
('Managed EKS; AWS runs the control plane, customers configure workloads, and worker-node duties depend on the compute option.',True,'This matches the Kubernetes requirement and preserves retained workload and compute-dependent duties.'),
('ECS; AWS runs a Kubernetes control plane for the team.',False,'The taught Kubernetes control-plane boundary is managed EKS, not ECS scheduling.'),
('Managed EKS; AWS assumes all application and worker-node responsibilities.',False,'Customers retain workload configuration; worker-node responsibility depends on the compute option.')]),
'003':('For destination 10.20.2.10, the effective table has 10.20.0.0/16 → local and 0.0.0.0/0 → attached internet gateway. Which route takes priority?',[
('10.20.0.0/16 → local',True,'Both match, but the /16 destination prefix is more specific than /0.'),
('0.0.0.0/0 → attached internet gateway',False,'The default route does not take priority over a more specific matching route.'),
('Neither route, because two matching routes cancel one another.',False,'The most specific matching prefix resolves this choice.')]),
'004':('A business tolerates at most 30 minutes to restore service and at most 5 minutes of data loss. Which labels express these requirements?',[
('RTO = 30 minutes; RPO = 5 minutes.',True,'RTO measures restoration time; RPO measures tolerated data loss in time.'),
('RTO = 5 minutes; RPO = 30 minutes.',False,'This reverses restoration tolerance and data-loss tolerance.'),
('RTO = 30 minutes; RPO = 30 minutes because recovery has one shared limit.',False,'The business supplied distinct downtime and data-loss limits.')]),
'005':('Read the report labels: EC2 OS-update report; RDS parameter-check report. Which boundary interpretation is supported?',[
('Both concern customer work: EC2 guest-OS maintenance and RDS customer-controlled engine configuration.',True,'EC2 OS updates are customer guest-OS work; RDS parameters are customer-controlled configuration.'),
('Both concern AWS work because both services run on AWS.',False,'Running on AWS does not transfer guest-OS or customer-controlled configuration duties.'),
('EC2 OS updates are customer work, but RDS parameter checks are AWS operating-system maintenance.',False,'The parameter report concerns database engine configuration, not RDS operating-system maintenance.')]),
'006a':('Demand rises beyond the supplied component capacity, but no component-loss requirement is stated. What kind of requirement is evidenced?',[
('Capacity must adjust to changing demand.',True,'Changing demand calls for matching capacity to demand.'),
('The only evidenced requirement is independent redundancy for component loss.',False,'No component-loss constraint is stated; redundancy addresses a different requirement.'),
('Capacity cannot be adjusted unless a component fails.',False,'The capacity requirement comes from changing demand, not from failure.')]),
'006b':('The requirement is to keep service available after the loss of one component. Which proposal addresses that requirement rather than merely increasing the same component’s capacity?',[
('Independent redundant capacity with enough surviving capacity to meet the requirement.',True,'Independent redundancy and sufficient surviving capacity address component loss.'),
('Enlarge the same single component, with no independent capacity.',False,'Losing that component still leaves no surviving independent capacity.'),
('Measure rising demand but provide no independent capacity.',False,'Demand measurement alone does not provide the redundant capacity required after component loss.')]),
'007':('The supplied policy says: initially engage the application operations team; if the issue remains unresolved after the established routine response checklist, escalate to the process operations team. Which escalation record follows that policy?',[
('After the checklist, escalate an unresolved issue to the process operations team.',True,'It preserves both the supplied condition and recipient.'),
('Escalate every event immediately to the process operations team, regardless of the checklist.',False,'This replaces the supplied escalation condition with an invented one.'),
('Leave an unresolved issue with the initial responder indefinitely.',False,'This omits the documented escalation path.')]),
'008':('In this isolated identity-policy exercise, an Allow and a Deny both apply to the same request after action, resource and condition comparisons. What is the outcome?',[
('Explicit deny.',True,'An applicable explicit deny overrides an applicable allow.'),
('Allow, because one matching allow is enough even with a matching deny.',False,'The explicit deny overrides that allow.'),
('Implicit deny, because no statement applies.',False,'Statements do apply; this is explicit deny, not absent applicable allow.')]),
'009':('Read this evidence from one supplied execution: YAML lists Build and Test; the same run’s logs show Build: success, Test: failure. What conclusion is supported?',[
('Build and Test ran; Build succeeded and Test failed.',True,'The same execution’s step logs establish both execution and results.'),
('Both succeeded because both appear in YAML.',False,'YAML defines steps; it does not prove they succeeded. The Test log says failure.'),
('Test never ran because it failed.',False,'A logged failure is evidence of a failed executed step, not proof that the step never ran.')]),
'010':('One application’s deployment frequency increased. With no other measures supplied, which interpretation respects the limits taught here?',[
('This shows more frequent deployment, but cannot alone establish overall performance or rank individuals.',True,'Interpret throughput and instability together over time and in application context.'),
('This alone proves lower change fail rate.',False,'Deployment frequency and change fail rate measure different things.'),
('This alone establishes which individual is the best performer.',False,'One measure is not a complete performance score or a basis for ranking individuals.')]),
'011':('Read the pattern {"source":["lab.orders"],"detail-type":["OrderReady"]}. An event has both accepted values. Only its id changes. What happens to the match?',[
('It still matches because id is omitted from the pattern.',True,'Fields omitted from the pattern are unconstrained.'),
('It stops matching because every event field must duplicate the original sample.',False,'The pattern constrains only fields it includes.'),
('The pattern must add the new id before any matching event is accepted.',False,'No id requirement exists in the supplied pattern.')])}

def choice(key):
 prompt,options=choices[key]; opts=[];correct=[];fb={}
 for i,(text,truth,why) in enumerate(options):
  oid=f'o{i+1}';opts.append({'option_id':oid,'text':text});fb[oid]={'message':why}
  if truth:correct.append(oid)
 assert len(correct)==1
 return {'prompt':prompt,'options':opts,'selection':'single','shuffle':True},{'correct_option_ids':correct,'option_feedback':fb}

def classification(prompt,buckets,entries):
 items=[];assign={};feed={}
 for i,(text,bucket,why) in enumerate(entries):
  iid=f'i{i+1}';items.append({'item_id':iid,'text':text});assign[iid]=bucket;feed[iid]={'message':why}
 return {'prompt':prompt,'buckets':[{'bucket_id':k,'label':v} for k,v in buckets.items()],'items':items},{'assignments':assign,'item_feedback':feed}

def inspect(n):
 buckets={'meets':'Meets the supplied criterion','violates':'Violates the supplied criterion'}
 if n=='000':
  caller='Account: [REDACTED_ACCOUNT]\nArn: arn:aws:iam::[REDACTED_ACCOUNT]:user/[REDACTED_OPERATOR]'
  prompt='Read each supplied operator-context review and decide whether its conclusion meets the stated check. Expected caller: '+caller+'; configured Region us-west-2; approved command target differs and is supplied as TARGET_REGION. Do not change credentials.'
  e=[('aws sts get-caller-identity --profile lab-operator\n'+caller+'\nReview: both returned values agree with the expected context.','meets','Both caller ARN and account are compared, using the explicit profile.'),
  ('aws configure list --profile lab-operator\nRegion Value: us-west-2; Type: config-file; Location: ~/.aws/config\nReview: configuration evidence identifies the effective Region and its origin.','meets','The Region row supplies value, type and location, not caller evidence.'),
  ('Review: caller and configuration were checked first without changing credentials. The supplied sandbox command retains --profile lab-operator and adds --region TARGET_REGION for its differing approved target.','meets','The explicit profile is retained and the differing command Region overrides configuration.'),
  ('Review: the profile label alone confirms the expected ARN and account, so skip get-caller-identity.','violates','A profile label is not caller evidence; returned ARN and account must be compared.'),
  ('Region Value: us-west-2; Type: config-file; Location: ~/.aws/config\nReview: because a Region is configured, ignore the different approved command target and omit --region.','violates','The differing approved command target requires an explicit Region override, not ignoring the target.')]
 elif n=='003':
  prompt='Read the supplied route-table review excerpts. The subnet must be explicitly associated with the intended table, retain 10.20.0.0/16 → local, and use 0.0.0.0/0 → the supplied attached internet gateway. Decide which excerpts meet that configuration criterion.'
  e=[('Association: subnet → intended table (explicit)\nRoutes: 10.20.0.0/16 → local; 0.0.0.0/0 → supplied attached internet gateway','meets','The intended explicit association, VPC route and required default route are all present.'),
  ('Association: none explicit; main table differs from intended table\nIntended table routes: 10.20.0.0/16 → local; 0.0.0.0/0 → supplied attached internet gateway','violates','Without explicit association the subnet uses the main table, not this intended table.'),
  ('Association: subnet → intended table (explicit)\nRoutes: only 0.0.0.0/0 → supplied attached internet gateway; VPC route removed','violates','The success criterion retains the VPC route as well as adding the default route.'),
  ('Association: subnet → intended table (explicit)\nRoutes: only 10.20.0.0/16 → local','violates','The required IPv4 default route to the attached gateway is missing.')]
 elif n=='005':
  buckets={'aws':'AWS responsibility','customer':'Customer responsibility'};e=[]
  for r in rows('ds.service_responsibilities'):
   e.append((f"Service: {r['service']}\nDuty/report: {r['duty_or_report']}\nDecide who is responsible.",'aws' if r['responsible_party']=='AWS' else 'customer',r['boundary_rationale']))
  prompt='Read each supplied service duty or report label and decide whether it is AWS or customer responsibility. Distinguish infrastructure and OS maintenance from retained data, access and configuration duties.'
 elif n=='007':
  r=rows('ds.ownership_escalation')[0]
  prompt='Read the supplied responsibility policy, then decide whether each proposed response record follows it:\n'+ '\n'.join(f'{k}: {v}' for k,v in r.items())
  e=[(f"Service owner: {r['resource_owner']}; process owner: {r['process_owner']}; initially engage: {r['initial_event_responder']}; escalate when: {r['unresolved_issue_condition']}; recipient: {r['escalation_recipient']}",'meets','This preserves resource and process owners, the initial responder, and the documented condition and recipient.'),
  (f"Service owner: {r['process_owner']}; process owner: {r['resource_owner']}; initially engage: {r['initial_event_responder']}",'violates','This swaps the supplied service and process responsibilities and omits escalation.'),
  (f"Service owner: {r['resource_owner']}; process owner: {r['process_owner']}; initial responder: {r['initial_event_responder']}; escalate immediately for every alert to {r['escalation_recipient']}",'violates','The recipient is supplied, but immediate escalation invents a different condition.'),
  (f"Service owner: {r['resource_owner']}; process owner: {r['process_owner']}; initial responder: {r['initial_event_responder']}; unresolved issues remain with the initial responder; no escalation.",'violates','This leaves out the documented unresolved-issue escalation path.')]
 elif n=='008':
  rr=rows('ds.identity_policy_evaluation');p=[r for r in rr if r['request_id']==rr[0]['request_id']]
  policy=[{k:r[k] for k in ['Effect','Action','Resource','Condition']} for r in p]
  prompt='Read this supplied identity policy and decide each request outcome. Scope: only these identity statements, with no other policies. Compare action, resource and both supplied principal-tag conditions; distinguish implicit from explicit denial.\n```json\n'+json.dumps({'Statement':policy},indent=2)+'\n```'
  buckets={'allow':'Allow','implicit_deny':'Implicit deny: no applicable allow','explicit_deny':'Explicit deny overrides allow'};e=[]
  for r in rr[::2]:
   text=json.dumps({'request_id':r['request_id'],'Action':r['request_action'],'Resource':r['request_resource'],'principal_tags':{'approved':r['request_approved'],'blocked':r['request_blocked']}},indent=2)
   outcome=r['identity_policy_result'];why={'allow':'Action and resource match; approved satisfies the allow and blocked does not satisfy the deny.','implicit deny':'No applicable allow: compare the supplied resource and approved condition with the allow statement.','explicit deny':'Both statements apply; blocked satisfies the explicit deny, which overrides the allow.'}[outcome]
   e.append((text,outcome.replace(' ','_'),why))
 elif n=='009':
  prompt='Read the supplied workflow and same-execution logs, then decide whether each review conclusion is supported. File: .github/workflows/orders.yml\n```yaml\non: push\njobs:\n  build_test:\n    runs-on: ubuntu-latest\n    steps:\n      - name: Build\n        run: build-command\n      - name: Test\n        run: test-command\n```\nExecution orders-review: event push; job build_test; selected runner ubuntu-latest; Build started → success; Test started → failure. Commands are supplied labels; judge the evidence, not their implementation.'
  e=[('Review: this file is in .github/workflows and this execution has the expected push event.','meets','The file location and logged event agree with the YAML trigger.'),
  ('Review: build_test selects ubuntu-latest; its Build and Test steps use run commands, not uses actions.','meets','runs-on selects the runner and run marks commands in steps.'),
  ('Review: in orders-review, Build and Test both ran; Build succeeded and Test failed.','meets','These results come from step logs in that same execution.'),
  ('Review: Test succeeded because its run command appears in YAML.','violates','The YAML definition does not establish results; this execution logs Test failure.'),
  ('Review: Build success in an unrelated previous run proves Build success in orders-review without reading orders-review logs.','violates','Verification must use evidence from the same execution, not another run.')]
 elif n=='011':
  prompt='Read each supplied EventBridge pattern and sandbox test report. Decide whether the pattern and BOTH results meet the requirement: accept source lab.orders with detail-type OrderReady; reject lab.orders with OrderCancelled. Each test sample has the stated source and detail-type; other supplied event fields are omitted from these patterns.'
  e=[('Pattern: {"source":["lab.orders"],"detail-type":["OrderReady"]}\nTest lab.orders / OrderReady: match\nTest lab.orders / OrderCancelled: no match','meets','Arrays constrain both fields; positive and negative results agree with the intended selection.'),
  ('Pattern: {"source":["lab.orders"]}\nTest lab.orders / OrderReady: match\nTest lab.orders / OrderCancelled: match','violates','Omitting detail-type leaves it unconstrained, so the unwanted event also matches.'),
  ('Pattern: {"source":["lab.orders"],"detail-type":["OrderReady","OrderCancelled"]}\nTest lab.orders / OrderReady: match\nTest lab.orders / OrderCancelled: match','violates','The acceptable-values array admits the event the requirement must reject.'),
  ('Pattern: {"source":["lab.orders"],"detail-type":["OrderReady"]}\nTest lab.orders / OrderReady: match\nOrderCancelled sample: not tested','violates','The success criterion requires matching and nonmatching test evidence; the negative result is missing.')]
 pub,gr=classification(prompt,buckets,e)
 if n=='005':
  aid='ds.service_responsibilities';column='responsible_party'
  role=next(c['semantic_role'] for c in assets[aid]['columns'] if c['name']==column)
  gr['role_map']={k:role for k in buckets}
  for item,r in zip(pub['items'],rows(aid)):
   item['source']={'asset_id':aid,'row':ref(r,['service','duty_or_report']),'column':column}
 return pub,gr

# Table keys are selected algorithmically and cell values copied only from the selected row.
def table(n):
 tasks=[];answers=[];tf={}
 def add(prompt,row,cols,column=None,why='Compare all relevant requirements, not just one field.'):
  tid=f't{len(tasks)+1}';tasks.append({'task_id':tid,'prompt':prompt,'target_kind':'cell' if column else 'row'});a={'task_id':tid,'row':ref(row,cols)}
  if column:a.update(column=column,expect_value=row[column])
  answers.append(a);tf[tid]={'correct':why,'incorrect':why}
 if n=='001':
  aid='ds.subnet_candidates';rr=rows(aid);valid=[]
  for r in rr:
   net=ipaddress.ip_network(r['subnet_cidr']);vpc=ipaddress.ip_network(r['vpc_cidr'])
   if net.subnet_of(vpc) and 16<=net.prefixlen<=28 and net.num_addresses-5>=r['required_usable_addresses']:valid.append(r)
  assert len(valid)==2 and not ipaddress.ip_network(valid[0]['subnet_cidr']).overlaps(ipaddress.ip_network(valid[1]['subnet_cidr']))
  for r in valid:add(f"Select the candidate for {r['availability_zone']} that fits inside the supplied VPC, does not overlap the selected candidate in the other zone, has a /16 through /28 prefix, and meets required usable capacity after five reserved addresses.",r,['candidate_id'],why='The selected /24 fits the VPC and capacity requirement; the /25 overlaps and has insufficient usable capacity.')
  intro='Select one subnet for each supplied zone. Check containment, overlap, legal prefix size and usable capacity together.'
 elif n=='002':
  aid='ds.container_ownership';rr=rows(aid)
  for need in [True,False]:
   case=[r for r in rr if r['needs_kubernetes_apis_and_ecosystem']==need and r['willing_to_operate_kubernetes_workloads']==need];win=next(r for r in case if r['platform']==('managed EKS' if need else 'ECS'))
   add(f"Select the full platform-and-responsibility row for requirement case '{win['requirement_case']}' that fits its Kubernetes need and willingness to operate Kubernetes workloads. Retain the compute-option qualification where it applies.",win,['requirement_case','platform'],why='Fit the platform to Kubernetes requirements and operating willingness, while keeping customer application/workload duties and the EKS node qualification.')
   for col,label in [('managed_platform_duties','managed platform duty'),('customer_workload_duties','retained customer duty')]:add(f"In the fitting row for '{win['requirement_case']}', select the cell describing the {label}.",win,['requirement_case','platform'],col)
   if need:add('In the fitting Kubernetes-requirement row, select the cell preserving the worker-node compute-option qualification.',win,['requirement_case','platform'],'worker_node_qualification')
  intro='Review both supplied team cases; choose the platform and responsibility evidence for each.'
 elif n=='004':
  aid='ds.recovery_options';rr=rows(aid);wins=[r for r in rr if r['restoration_minutes']<=r['rto_minutes'] and r['data_loss_minutes']<=r['rpo_minutes']];assert len(wins)==1;w=wins[0]
  intro='Business limits are the repeated rto_minutes and rpo_minutes values. Select evidence distinguishing restoration time from data-loss time, and judge both together.'
  add('Select the only approach whose restoration and data loss each meet their corresponding business limit.',w,['approach_id'],why='The selected approach meets both limits; meeting only restoration or only data loss is insufficient.')
  for col,prompt in [('rto_minutes','Select the business maximum tolerated service-restoration time (RTO) in the qualifying row.'),('rpo_minutes','Select the business maximum tolerated data-loss time (RPO) in the qualifying row.'),('restoration_minutes','Select the qualifying row’s capability to compare with RTO.'),('data_loss_minutes','Select the qualifying row’s capability to compare with RPO.')]:add(prompt,w,['approach_id'],col,why='Restoration is compared with RTO; data-loss time is compared with RPO. Both comparisons must pass.')
 elif n=='006':
  aid='ds.capacity_proposals';rr=rows(aid)
  single=next(r for r in rr if r['independent_components']==1)
  surviving=[r for r in rr if r['independent_components']>1 and r['surviving_capacity_after_one_loss']>=r['required_capacity_after_one_loss']];assert len(surviving)==1
  intro=f"Two different requirements: demand grows from {single['ordinary_demand']} to {single['total_capacity']} requests/second with no component-loss constraint; separately, after loss of one component the service must retain the table's required post-loss capacity. Do not confuse ordinary total capacity with surviving capacity."
  add('For the changing-demand case, keep exactly one component and select the adjustment that supplies the increased demand. No component-loss requirement is imposed in this case.',single,['proposal'],why='This one-component adjustment matches the increased demand; independence is a separate failure requirement.')
  add('For the changing-demand case, select the total_capacity cell of the one-larger-component adjustment that meets the stated increased demand. This task has no component-loss requirement.',single,['proposal'],'total_capacity',why='The supplied larger-component adjustment meets increased demand through total capacity, but does not provide surviving capacity after its own loss.')
  w=surviving[0]
  add('For the component-loss case, select the only proposal with independent components and surviving capacity meeting the required_capacity_after_one_loss value.',w,['proposal'],why='Only independent redundant capacity leaves enough surviving capacity after one component is lost; enlarging the same component does not.')
  add('In the qualifying component-loss proposal, select the surviving-capacity cell that supports that selection.',w,['proposal'],'surviving_capacity_after_one_loss',why='Compare surviving capacity, not just ordinary total capacity, with the post-loss service requirement.')
 elif n=='010':
  aid='ds.delivery_evidence';rr=rows(aid);assert len(rr)==2;a,b=rr;assert b['deployment_frequency']>a['deployment_frequency'] and b['change_lead_time']<a['change_lead_time'] and b['change_fail_rate']>a['change_fail_rate'] and b['failed_deployment_recovery_time']>a['failed_deployment_recovery_time']
  intro='For the same application across the two reporting periods, investigate the concern that throughput improved while instability worsened. Select the later evidence for each measure. This is an application-level comparison, not a complete performance score or an individual ranking.'
  add('Select the reporting-period row that, compared with the other period for this application, has higher deployment frequency and shorter change lead time, but also higher change fail rate and longer failed-deployment recovery time. Treat this as mixed throughput and instability evidence, not a complete performance score.',b,['application','reporting_period'],why='The same-period evidence shows faster throughput alongside worse instability; neither throughput alone nor one metric establishes overall performance.')
  for col,prompt in [('deployment_frequency','Select the later-period cell showing how often changes are deployed; compare it with the earlier period.'),('change_lead_time','Select the later-period cell showing elapsed commit-to-production time; compare it with the earlier period.'),('change_fail_rate','Select the later-period cell supporting concern about the proportion of deployments requiring intervention.'),('failed_deployment_recovery_time','Select the later-period cell supporting concern about time to recover from a failed deployment.')]:add(prompt,b,['application','reporting_period'],col,why='Frequency and lead time describe throughput; fail rate and failed-deployment recovery time describe instability. Compare all four in the same application context.')
 return {'asset_ref':{'asset_id':aid},'intro':intro,'tasks':tasks},{'answers':answers,'task_feedback':tf}

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='interactions_part',tiles=[])
for t in plan['tiles']:
 n=t['tile_id'].split('.')[-1];cid=t['concept_ids'][0];b=bs[cid];items=[];seen=set();steps=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 for pos,s in enumerate(steps):
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1];a=next(a for a in b['assessment_anchors'] if a['capability']==capability);measures.append({'concept_id':cid,'capability':capability,'fact_ids':a['fact_ids']})
  if not measures:
   # Practice-only planned steps still require assessment measures: use the same
   # glossary capabilities whose facts the practice selections assess.
   measures=[{'concept_id':cid,'capability':a['capability'],'fact_ids':a['fact_ids']} for a in b['assessment_anchors']]
  typ=s['planned_interaction_type']
  if typ=='choice':pub,gr=choice(n if n!='006' else ('006a' if pos==0 else '006b'))
  elif typ=='classify':pub,gr=inspect(n)
  elif typ=='table_select':pub,gr=table(n)
  else:raise ValueError(typ)
  hint_by_tile={
   '000':'Keep caller identity evidence separate from configuration evidence, and distinguish profile selection from Region selection.',
   '001':'Check the address ranges and capacity before judging the zone assignments.',
   '002':'Compare the Kubernetes requirement and operating willingness before assigning retained duties.',
   '003':'Check association, destination prefix and target separately.',
   '004':'Compare each recovery capability with the business limit for that same kind of time.',
   '005':'Identify whether each duty concerns infrastructure, a guest OS, data or customer-controlled configuration.',
   '006':'Ask whether the requirement concerns changing demand or what remains after component loss.',
   '007':'Separate the resource owner, process owner, initial responder, escalation condition and recipient.',
   '008':'Compare action, resource and conditions for every statement before combining the outcomes.',
   '009':'Separate workflow definitions from evidence about a particular execution.',
   '010':'Keep the same application context and reporting periods when comparing throughput with instability.',
   '011':'Check which fields the pattern constrains, then review the positive and negative sample results.'}
  feedback={'correct':{'message':'Your selections match the supplied evidence and the taught criteria.'},'incorrect':{'message':'Recheck the supplied evidence against each criterion; a label or a partial match is not enough.'},'hints':[hint_by_tile[n]]}
  rems=[r for r in sc[t['tile_id']].get('remediation_steps',[]) if cid in r['concept_ids']]
  if rems:
   if not seen:rem=rems[0]
   else:
    tested={cid+'#'+f for m in measures for f in m['fact_ids']}
    rem=max(rems,key=lambda r:len(tested.intersection(r.get('lineage',{}).get('fact_ids',[]))))
   feedback['remediation_step_id']=rem['step_id']
  seen.add(cid)
  ix={'type':typ,'interaction_id':'ix.'+s['step_id'],'difficulty':('intro' if pos==0 else 'stretch' if pos==len(steps)-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors'],'public':pub,'grading':gr,'feedback':feedback}
  items.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':items})
(P/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Generated',sum(len(t['interactions']) for t in out['tiles']),'interactions')
