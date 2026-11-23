import json, re, ipaddress
from pathlib import Path
root=Path(__file__).resolve().parents[1]
g=json.loads((root/'inputs/path_glossary_bundle.json').read_text())
bs=g['bundles']
texts=['\n'.join(t['content'] for t in b['teaching_blocks'])+'\n'+json.dumps(b['visual_anchor'])+'\n'+json.dumps(b['practice_anchor']) for b in bs]
alltext='\n'.join(texts)
# Mine the supplied vocabulary, never replace the supplied names or numbers.
terms=['AWS CLI','lab-operator','Account','Arn','[REDACTED_ACCOUNT]','[REDACTED_OPERATOR]','us-west-2','config-file','~/.aws/config','--profile','--region','get-caller-identity','configure list','VPC','Availability Zones','ECS','managed EKS','Kubernetes APIs','Kubernetes control plane','worker nodes','compute option','internet gateway','VPC main route table','RTO','RPO','EC2','RDS','parameter groups','application operations team','sandbox orders service','Effect','Action','Resource','Condition','Allow','Deny','implicit deny','explicit deny','.github/workflows','on','jobs','runs-on','steps','uses','run','deployment frequency','change lead time','change fail rate','failed deployment recovery time','EventBridge','TestEventPattern','source','detail-type','lab.orders','OrderReady','OrderCancelled','id','account','time','region','resources']
vocab=[]
for term in terms:
 if term in alltext and term not in vocab: vocab.append(term)
for token in re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d+)?|(?<![\w])(?:/\d+|\d+)(?![\w])',alltext):
 if token not in vocab: vocab.append(token)
sid='scenario.orders_sandbox'
assets=[]
def col(name,role='text',typ='string',unit=None,description=None):
 c={'name':name,'type':typ,'semantic_role':role}
 if unit: c['unit']=unit
 if description: c['description']=description
 return c
def dataset(aid,title,columns,rows,description):
 assets.append({'asset_id':'ds.'+aid,'asset_kind':'dataset','scenario_id':sid,'title':title,'description':description,'columns':columns,'rows':rows,'provenance':'authored','variants':[]})
def number_from(i,pattern): return int(re.search(pattern,texts[i]).group(1))
# Allocation values come straight from the named subnet example; counts are computed.
vpc=re.search(r'10\.20\.0\.0/16',texts[1]).group()
cidrs=list(dict.fromkeys(re.findall(r'10\.20\.[\d.]+/\d+',texts[1])))
cidrs=[c for c in cidrs if c!=vpc]
reserved=5
minimum=number_from(1,r'at least (\d+) usable')
rows=[]
for n,c in enumerate(cidrs):
 net=ipaddress.ip_network(c)
 rows.append(['candidate.'+str(n+1),vpc,c,'Zone A' if n==0 else 'Zone B',net.num_addresses,net.num_addresses-reserved,minimum,str(net.network_address)+' through '+str(net.network_address+3)+'; '+str(net.broadcast_address)])
dataset('subnet_candidates','Subnet allocation candidates',[col('candidate_id','identifier'),col('vpc_cidr','identifier'),col('subnet_cidr','identifier'),col('availability_zone','categorical',description='Fictional supplied zone labels, not provisioned zones.'),col('total_addresses','numerical','integer','addresses'),col('usable_addresses','numerical','integer','addresses'),col('required_usable_addresses','numerical','integer','addresses'),col('reserved_addresses')],rows,'Read-only authored allocation worksheet. Zone A and Zone B are distinct supplied locations. Candidate ranges and minimum capacity preserve the glossary example; the third candidate overlaps the first.')
# One table covers both ownership boundaries and both stated platform requirements.
rows=[]
for case,dependency,willingness in [('Kubernetes requirement',True,True),('No Kubernetes dependency',False,False)]:
 for platform,managed,customer,nodes in [('ECS','Container workload scheduling','Supply and operate applications','Not specified by this ECS comparison'),('managed EKS','Kubernetes control plane','Configure and operate Kubernetes workloads','Worker-node responsibility depends on the selected compute option')]:
  rows.append([case,dependency,willingness,platform,managed,customer,nodes])
dataset('container_ownership','Container platform requirements and retained duties',[col('requirement_case','categorical'),col('needs_kubernetes_apis_and_ecosystem','categorical','boolean'),col('willing_to_operate_kubernetes_workloads','categorical','boolean'),col('platform','categorical'),col('managed_platform_duties'),col('customer_workload_duties'),col('worker_node_qualification')],rows,'Two fictional supplied requirements compare ECS and managed EKS. No application ownership is transferred to AWS; EKS worker-node duties remain compute-dependent.')
rto=number_from(4,r'at most (\d+) minutes to restore')
rpo=number_from(4,r'at most (\d+) minutes of lost data')
lag=number_from(4,r'data is (\d+) minutes behind')
dataset('recovery_options','Business recovery limits and candidate capabilities',[col('approach_id','identifier'),col('rto_minutes','numerical','integer','minutes'),col('rpo_minutes','numerical','integer','minutes'),col('restoration_minutes','numerical','integer','minutes'),col('data_loss_minutes','numerical','integer','minutes')],[['approach.both',rto,rpo,rto,rpo],['approach.stale_data',rto,rpo,rto,lag],['approach.slow_restore',rto,rpo,rto*2,rpo]],'Authored comparison options, not AWS defaults or measured recovery performance. Each approach must be compared with both business limits.')
dataset('service_responsibilities','EC2 and RDS responsibility boundaries',[col('service','categorical'),col('duty_or_report'),col('responsible_party','categorical'),col('boundary_rationale')],[['EC2','Guest-OS updates and security patches','Customer','Customer guest-operating-system maintenance'],['EC2','Supplied OS-update report','Customer','Report concerns guest-operating-system work'],['RDS','Database infrastructure','AWS','Managed database infrastructure'],['RDS','Operating-system maintenance','AWS','Managed operating-system maintenance'],['RDS','Supplied parameter-check report','Customer','Parameter groups contain customer-controlled database engine configuration values'],['RDS','Data, access and application use','Customer','Retained customer responsibilities'],['EC2','Data, access and customer-controlled configuration','Customer','Retained customer responsibilities']],'Read-only responsibility assignment consistent with the glossary service boundary; reports are labels, not fabricated operational results.')
demand=number_from(6,r'handle (\d+) requests per second')
# Equal totals, explicitly supplied post-failure requirement, calculated surviving capacity.
rows=[]
for name,count,size in [('One larger component',1,demand*2),('Two independent components',2,demand)]:
 rows.append([name,count,size,count*size,(count-1)*size,demand,demand,'One location' if count==1 else 'Two independent locations'])
dataset('capacity_proposals','Ordinary demand versus surviving capacity',[col('proposal','categorical'),col('independent_components','numerical','integer','components'),col('capacity_per_component','numerical','integer','requests/second'),col('total_capacity','numerical','integer','requests/second'),col('surviving_capacity_after_one_loss','numerical','integer','requests/second'),col('ordinary_demand','numerical','integer','requests/second'),col('required_capacity_after_one_loss','numerical','integer','requests/second'),col('placement')],rows,'Authored hypothetical capacities, not real service performance. Both proposals have equal ordinary capacity; the supplied post-loss service requirement is stated separately.')
dataset('ownership_escalation','Sandbox orders service ownership and escalation',[col('resource','identifier'),col('resource_owner','categorical'),col('associated_process','identifier'),col('process_owner','categorical'),col('initial_event_responder','categorical'),col('unresolved_issue_condition'),col('escalation_recipient','categorical')],[['sandbox orders service','application operations team','orders event-response process','process operations team','application operations team','Issue remains unresolved after the established routine response checklist is completed','process operations team']],'Fictional supplied established ownership record: the process team and checklist condition are authored scenario inputs, not a universal escalation policy or time limit. Resource and process ownership are separate.')
# Authored policy scope and requests. Derive applicability and decisions rather than typing answers.
policy_action='s3:GetObject'
policy_resource='arn:aws:s3:::sandbox-orders/*'
condition_key='aws:PrincipalTag/approved'
requests=[('request.allowed',policy_action,'arn:aws:s3:::sandbox-orders/order-a','yes',False),('request.condition',policy_action,'arn:aws:s3:::sandbox-orders/order-a','no',False),('request.resource',policy_action,'arn:aws:s3:::other-sandbox/order-a','yes',False),('request.denied',policy_action,'arn:aws:s3:::sandbox-orders/order-a','yes',True)]
rows=[]
for rid,action,resource,approved,deny in requests:
 applicability=[]
 for statement,effect,condkey,condval,actual in [('statement.allow','Allow',condition_key,'yes',approved),('statement.deny','Deny','aws:PrincipalTag/blocked','yes','yes' if deny else 'no')]:
  applies=action==policy_action and resource.startswith(policy_resource[:-1]) and actual==condval
  applicability.append(applies)
  rows.append([rid,action,resource,approved,'yes' if deny else 'no',statement,effect,policy_action,policy_resource,json.dumps({'StringEquals':{condkey:condval}},separators=(',',':')),applies,None])
 result='explicit deny' if applicability[1] else 'allow' if applicability[0] else 'implicit deny'
 for row in rows[-2:]: row[-1]=result
dataset('identity_policy_evaluation','Object-read requests matched to identity-policy statements',[col('request_id','identifier'),col('request_action','categorical'),col('request_resource','identifier'),col('request_approved','categorical'),col('request_blocked','categorical'),col('statement_id','identifier'),col('Effect','categorical'),col('Action','categorical'),col('Resource','identifier'),col('Condition'),col('statement_applicable','categorical','boolean'),col('identity_policy_result','categorical')],rows,'Read-only authored identity-policy examples. Supplied aws:PrincipalTag/approved and aws:PrincipalTag/blocked are illustrative condition inputs only. The table evaluates only the identity-policy rules taught here, not all policy types or real AWS authorization.')
# Comparable synthetic reporting periods: keep all four measures and units together.
dataset('delivery_evidence','Orders delivery throughput and instability over two periods',[col('application','identifier'),col('reporting_period','categorical'),col('deployment_frequency','numerical','integer','deployments/week'),col('change_lead_time','numerical','number','hours'),col('change_fail_rate','numerical','number','percent of deployments requiring intervention'),col('failed_deployment_recovery_time','numerical','number','minutes')],[['sandbox orders service','Period A',10,24,10,30],['sandbox orders service','Period B',20,12,20,45]],'Two equal-length fictional reporting periods for the same application, with authored illustrative aggregates, not actual production metrics. More frequent delivery and shorter lead time coexist with higher failure proportion and longer failed-deployment recovery time. No individual ranking is supported.')
registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':root.name,'scenarios':[{'scenario_id':sid,'name':'Sandbox orders operations review','summary':'A fictional application operations team reviews supplied, read-only evidence for a sandbox orders service: operator context, network choices, platform and service boundaries, recovery and capacity requirements, response ownership, identity-policy matching, workflow logs, delivery measures and event selection. No credentials, cloud resources or executable tooling are provisioned. Additional teams, conditions and measurements are authored exercise inputs, not real-world observations.','domain':'AWS operational readiness','glossary_example_vocab':vocab}],'assets':assets}
# Local mistakes-to-avoid checklist: widths, roles, numeric labels, adequate anchor coverage.
for a in assets:
 assert all(len(r)==len(a['columns']) for r in a['rows'])
 for c in a['columns']:
  assert (c['type'] in ('integer','number')) == (c['semantic_role']=='numerical')
  for r in a['rows']:
   value=r[a['columns'].index(c)]
   if c['type']=='string' and value is not None and re.fullmatch(r'\d+',value): c['numeric_looking_label']=True
 assert not a['variants'] # No messy-data concept: no unjustified variants or planted issues.
assert len([b for b in bs if b['visual_anchor']['type']=='data_table'])==6
assert len(assets)==8
(root/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
print('Concepts:',len(bs),'Scenarios:',len(registry['scenarios']),'Assets:',len(assets),'Rows:',sum(len(a['rows']) for a in assets),'Vocabulary:',len(vocab))
print('Checklist passed: widths, type/role agreement, numeric-label marking, no unverified variant issues, six mandatory table anchors plus allocation and capacity comparisons. No plots or executable workspaces required by this batch.')
