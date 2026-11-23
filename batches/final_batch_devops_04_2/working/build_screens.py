import json,re,copy
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.04_2')
plan=json.loads((P/'tile_plans.json').read_text()); glossary=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in glossary['bundles']}
A={a['asset_id']:a for a in registry['assets']}
C={}
for t in plan['tiles']:
 for c in t['concept_ids']: C[c]=t['tile_id'].split('.')[-1] + ('alarm' if 'route_alarm' in c else '')
assets={'067':'ds.retry_counting','068':'ds.billing_evidence','069':'ds.deployment_reconciliation','070':'ds.recovery_dependencies','071':'ds.orders_logs','071alarm':'ds.alarm_receipt','073':'ds.lambda_outcomes'}
def rows(key):
 a=A[assets[key]];return [dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
r=rows('067');bill=rows('068');pods=rows('069');logs=rows('071');alarm=rows('071alarm');lam=rows('073')
# All scenario values, counts and labels come from the named stage inputs.
budget=r[0]['configured_value']; first=r[0]['initial_requests']; retries=r[0]['maximum_retries']; alt_retries=r[1]['maximum_retries']
logdesc=A[assets['071']]['description']; interval=re.search(r'selected interval (\S+) through (\S+)\.',logdesc).groups()
query=re.search(r'Use (fields .*? asc)\.',logdesc).group(1)
text={
'067':[
'A supplied AWS call needs a finite retry budget and a useful final report, not a loop around every failure.',
'SDK retries cover selected transient or throttling errors; not every failed request is safe to repeat.',
'Configure the supplied Boto3 client with botocore.config.Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS}) for bounded SDK backoff. Do not loop around terminal errors. Catch botocore.exceptions.ClientError around the supplied call: inspect response["Error"]["Code"] and response["Error"]["Message"], retain response["ResponseMetadata"]["RequestId"] when present, and report terminal failure or exhausted retries. total_max_attempts includes the initial request; Config max_attempts counts retries after it.',
f'With the approved total_max_attempts budget of {budget}, the initial request leaves at most {retries} retries. Config max_attempts={budget} instead allows {alt_retries} retries after the first request. Invoke the supplied call once at application level; let standard SDK backoff handle eligible retries. Catch ClientError and report Code and Message, retaining RequestId if present.',
'The two settings count different things. Selected retry support does not justify repeating every error indefinitely; terminal or exhausted-retry failures need a final report.'
],
'068':[
'An apparently unused resource is a lead, not a billed-charge conclusion.',
'Cost Explorer analyzes billed cost and usage within selected time intervals and grouping dimensions.',
'Filter the supplied account and period. Group by service or usage type, then inspect cost and usage to identify the supported driver. Justify an avoidable charge with billed usage evidence, not resource existence.',
f"Use account {bill[0]['account']} and {bill[0]['period_start']} through {bill[0]['period_end']}. Compare the service or usage-type groups and their billed cost and usage. The supplied owner record for {bill[0]['usage_type']} says its temporary usage is no longer required; cite its report values when recommending review. The {bill[1]['usage_type']} context says that usage remains required. Keep account, interval, grouping and values with the recommendation so another reviewer can check the attribution.",
'A resource name, age or existence does not establish a numerical charge. Compare suspected drivers within the supplied interval; use billed cost and usage rather than inventing charges from inventory. This is a supported recommendation, not a forecast or an independent deletion decision.'
],
'069':[
'A removed test Pod and the Deployment target are different evidence.',
'A Deployment manages ReplicaSets to reconcile requested Pod replicas and the Pod template.',
f"Apply the supplied Deployment with kubectl apply -f {re.search(r'FILE is (\S+)\.',A[assets['069']]['description']).group(1)}. Inspect kubectl get deployment {pods[0]['deployment']} and associated Pods. Delete one controlled test Pod through the supplied procedure; verify a replacement restores the requested count.",
f"The {pods[0]['deployment']} Deployment requests {pods[0]['requested_replicas']} replicas throughout this exercise. Before removal, inspect its requested count and associated Pods. The controlled removal of {pods[1]['removed_pod']} produces a temporary observed shortage. Continue inspection until the controller creates {pods[2]['replacement_pod']} and restores the target. Completion evidence combines replacement identity with the restored count; accepted deletion alone does not verify reconciliation.",
'The requested count stays the target while the observed count temporarily falls. Deleting one test Pod does not change that target. ReplicaSet reconciliation restores requested Pods and template; this is not demand-based scaling or cluster control-plane administration.'
],
'070':[
'A component list can still describe an unusable recovery order.',
'Account for workload dependencies and the recovery capabilities needed to meet recovery objectives.',
'List supplied infrastructure, data and service dependencies. Restore each prerequisite before dependent work, with readiness verification before dependent services resume. Incomplete restoration is not usable recovery.',
'The supplied record makes infrastructure readiness a prerequisite for database restoration, and database readiness a prerequisite for resuming the orders application. Place restoration and its verification before each dependent step. Compare the ordered plan with the supplied capabilities and recovery objective: usable service with verified prerequisites. A scheduled dependent step is not ready if earlier restoration remains incomplete.',
'These edges describe this exercise, not a universal AWS sequence. If supplied dependencies include independent branches, do not invent an order between them. Listing components is not enough: the plan must show prerequisite order and readiness checkpoints before dependent services resume.'
],
'071':[
'Correlate the failed orders request with its identity and timestamps, not unrelated nearby messages.',
'Logs Insights selects and transforms events with commands connected by pipe characters.',
f'Select the intended log group and supplied interval. Use {query}. Replace template fields and identity with the supplied values. Retain relevant events in timestamp order to reconstruct the symptom sequence.',
f"The supplied group is {logs[0]['log_group']}; the interval is {interval[0]} through {interval[1]}. fields selects timestamp, message and request identity; filter keeps {logs[0]['request_id']}; sort orders ascending timestamps. Retain request receipt, the later failure message and the final response record as the symptom's evidence.",
'Time proximity alone does not establish a shared request or prove causation. Use identity and timestamps together, keep group and interval boundaries, and retain relevant events. Correlation of this request does not prove every nearby error caused it.'
],
'071alarm':[
'An alarm route needs receipt evidence, not configuration alone.',
'An alarm action can publish state-change notifications to SNS without changing metric evaluation.',
'Configure the approved topic as the notification action. Create the approved recipient subscription and confirm it when required. Verify receipt of a test alarm notification with alarm and workload context; an unconfirmed subscription may not deliver.',
f"For {alarm[0]['alarm']}, use {alarm[0]['sns_topic']} and the approved recipient {alarm[0]['recipient']}. Check confirmation, then retain the test receipt containing alarm and workload context alongside the configuration. Compare the supplied confirmed receipt case with the unconfirmed case lacking receipt evidence.",
'A topic action is not proof of delivery. Confirm where required and test receipt. Notification routing is separate from metric evaluation; an unconfirmed subscription may not deliver, rather than necessarily failing in every case.'
],
'073':[
'A supplied Lambda task needs bounded permissions and separate invocation and outcome evidence.',
'The execution role grants the function access to AWS resources during invocation.',
'Assign the approved role limited to the supplied task’s actions and resources. Invoke with the supplied payload. Inspect returned result and execution logs: invocation success is not proof of operational success.',
f"The supplied function {lam[0]['function']} uses {lam[0]['execution_role']}, limited to the approved resource check. Keep its supplied payload unchanged. In the failure case, invocation succeeds but the task result reports failure and the logs support that failure. Do not label the operation successful from invocation status alone. Compare with the case whose task-success result and execution logs support success; record both with role and payload context.",
'This verifies the bounded task, not every possible operation. The execution role is not unlimited authority. If the task reports an action absent from the approved role, retain permission and result evidence rather than broadening the role during the test. Always separate ability to invoke from permission scope and task outcome.'
]}
titles={'067':'Bound retries and preserve error evidence','068':'Support a cost-driver recommendation','069':'Verify fixed-replica reconciliation','070':'Order recovery by verified prerequisites','071':'Correlate a request in logs','071alarm':'Verify the owner receives the alarm','073':'Separate Lambda invocation from task outcome'}
def lineage(c,tbs=None,facts=None,visual=False):
 return {'concept_ids':[c],'teaching_block_ids':tbs or [],'fact_ids':facts or [],**({'anchors':[c+'#visual']} if visual else {})}
def prose(c,txt,tbs,facts,role='mechanism'):
 return {'type':'prose','text':txt,'role':role,'lineage':lineage(c,tbs,facts)}
def table(c,key,caption,sql=None,columns=None):
 out={'type':'data_table','caption':caption,'lineage':lineage(c,visual=True)}
 if sql: out['result_of']={'runtime':'sql','sql':sql,'asset_mounts':[{'asset_id':assets[key],'mount_path':'evidence'}]}
 else: out['asset_ref']={'asset_id':assets[key],**({'columns':columns} if columns else {})}
 return out
def diagram(c,title,nodes,edges=None,kind='container'):
 return {'type':'diagram','diagram_kind':kind,'title':title,'nodes':nodes,'edges':edges or [],'layout':'auto','alt_text':title,'lineage':lineage(c,visual=True)}
def quote(v):return "'"+str(v).replace("'","''")+"'"
def visual(c):
 k=C[c]
 if k=='067':
  code='from botocore.config import Config\nfrom botocore.exceptions import ClientError\n\nconfig = Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS})\nclient = supplied_client_setup(config)\ntry:\n    result = supplied_ready_call(client)\nexcept ClientError as error:\n    code = error.response["Error"]["Code"]\n    message = error.response["Error"]["Message"]\n    request_id = error.response.get("ResponseMetadata", {}).get("RequestId")\n    supplied_report_failure(code, message, request_id)\nelse:\n    supplied_report_success(result)'
  return [{'type':'code_walkthrough','language':'python','code':code,'annotations':[{'start_line':4,'end_line':5,'text':f'Supplied setup and reporting helpers are illustrative. APPROVED_ATTEMPTS={budget}: {first} initial request plus at most {retries} retries; Config max_attempts={budget} counts {alt_retries} retries after the initial request.'},{'start_line':6,'end_line':7,'text':'One application-level call; selected eligible SDK retries use bounded backoff.'},{'start_line':8,'end_line':12,'text':'Report terminal failure or exhausted retries with Code, Message and optional RequestId.'}],'reveal':'all','lineage':lineage(c,visual=True)},table(c,k,'SDK attempt-count comparison')]
 if k=='068':
  scope=bill[0]
  d=diagram(c,'Cost Explorer review: scope, grouping, evidence',[{'id':'scope','label':'Selected account and period','fields':[str(scope['account']),scope['period_start'],scope['period_end']]},{'id':'groups','label':'Group by service or usage type'},{'id':'evidence','label':'Inspect billed cost, usage and supplied owner context'}],[{'from':'scope','to':'groups','directed':True},{'from':'groups','to':'evidence','directed':True}])
  sql=f"SELECT * FROM evidence WHERE account = {scope['account']} AND period_start = {quote(scope['period_start'])} AND period_end = {quote(scope['period_end'])} ORDER BY service, usage_type"
  return [d,table(c,k,'Selected account and interval: compare category evidence',sql)]
 if k=='069':
  def snapshot(row):
   return table(c,k,row['phase'],f"SELECT * FROM evidence WHERE phase = {quote(row['phase'])}")
  return [{'type':'before_after','before':snapshot(pods[0]),'after':snapshot(pods[2]),'change_summary':'The requested target is unchanged; replacement identity and restored observed count verify reconciliation.','lineage':lineage(c,visual=True)},snapshot(pods[1])]
 if k=='070':
  rr=rows(k);nodes=[{'id':x['step_id'],'label':x['step'],'fields':[x['supplied_capability'],x['readiness_objective']]} for x in rr];edges=[{'from':x['prerequisite_step_id'],'to':x['step_id'],'label':'Prerequisite before dependent step','directed':True} for x in rr if x['prerequisite_step_id']]
  return [diagram(c,'Supplied workload recovery dependencies and readiness checkpoints',nodes,edges,'graph')]
 if k=='071':
  nodes=[{'id':'scope','label':'Selected log scope','fields':[logs[0]['log_group'],*interval]},{'id':'query','label':'Logs Insights query','fields':[query]},{'id':'sequence','label':'Retain matching events in ascending timestamp order'}]
  d=diagram(c,'Scoped request evidence review',nodes,[{'from':'scope','to':'query','directed':True},{'from':'query','to':'sequence','directed':True}])
  sql=f'SELECT "@timestamp", "@message", request_id FROM evidence WHERE log_group = {quote(logs[0]["log_group"])} AND "@timestamp" >= {quote(interval[0])} AND "@timestamp" <= {quote(interval[1])} AND request_id = {quote(logs[0]["request_id"])} ORDER BY "@timestamp" ASC'
  return [d,table(c,k,'Computed projection of the supplied identity and time-window selection',sql)]
 if k=='071alarm':
  x=alarm[0];nodes=[{'id':'alarm','label':x['alarm'],'fields':['Metric evaluation is unchanged']},{'id':'topic','label':x['sns_topic']},{'id':'recipient','label':x['recipient'],'fields':['Confirm subscription when required']},{'id':'receipt','label':'Test receipt: alarm and workload context'}]
  d=diagram(c,'Alarm notification route and receipt checkpoint',nodes,[{'from':'alarm','to':'topic','label':'Approved notification action','directed':True},{'from':'topic','to':'recipient','label':'Approved subscription','directed':True},{'from':'recipient','to':'receipt','label':'Verify receipt','directed':True}])
  return [d,table(c,k,'Configuration, confirmation and actual receipt evidence')]
 if k=='073':
  x=lam[0];nodes=[{'id':'function','label':x['function'],'fields':[x['supplied_payload']]},{'id':'role','label':x['execution_role'],'fields':[x['approved_task_scope']]},{'id':'invocation','label':'Invocation status'},{'id':'outcome','label':'Operational outcome','fields':['Inspect returned task result and execution logs']}]
  return [diagram(c,'Bounded role, supplied payload and separate outcome evidence',nodes,[{'from':'role','to':'function','label':'Approved resource permissions','directed':True},{'from':'function','to':'invocation','directed':True},{'from':'function','to':'outcome','directed':True}]),table(c,k,'Invocation status is separate from task result and execution logs')]
takeaways={
'067':'Use standard SDK backoff for selected eligible errors, with a finite total_max_attempts budget including the initial request. Config max_attempts counts retries instead. Report ClientError Code and Message and preserve RequestId when present.',
'068':'Filter account and period, group by service or usage type, and cite billed cost and usage. A resource merely existing does not establish its charge; support the recommendation with report evidence.',
'069':'A Deployment manages ReplicaSets to reconcile replicas and template. Apply the supplied Deployment, inspect it and associated Pods, and verify replacement plus restored count after controlled Pod removal. The requested target stays unchanged.',
'070':'Order supplied infrastructure, data and service prerequisites before dependent work. Match recovery capabilities to objectives and require readiness verification before services resume; incomplete restoration is not usable recovery.',
'071':'Use the supplied group, interval, request identity and piped fields/filter/sort query. Retain timestamp-ordered relevant events; nearby messages alone do not prove correlation or causation.',
'071alarm':'Route the alarm to the approved SNS topic and recipient; confirm when required and verify test receipt with alarm/workload context. Configuration alone is not receipt, and routing leaves metric evaluation unchanged.',
'073':'Keep the approved execution role limited to the supplied task’s actions and resources. Invoke with the supplied payload and inspect returned result plus logs. Invocation success alone is not operational success.'}
contrasts={
'067':'Contrast bounded SDK handling with an unlimited application retry loop. Report terminal or exhausted outcomes instead of treating every error as repeatable.',
'068':'Contrast billed usage and owner context with a resource merely existing. Only the former supports this report-based cost recommendation.',
'069':'Contrast an accepted Pod deletion with a replacement and restored count. Only the latter verifies the requested workload is reconciled.',
'070':'Contrast a scheduled dependent service with one whose prerequisites passed readiness checks. Scheduling alone is not usable recovery.',
'071':'Contrast shared identity plus timestamps with time proximity alone. Nearby events can belong to another request.',
'071alarm':'Contrast a configured subscription with a received test notification. An unconfirmed subscription may not deliver; configuration alone is not receipt evidence.',
'073':'Contrast successful invocation with a successful task result supported by logs. Invocation alone does not verify the operation; keep approved role scope unchanged.'}
remfacts={
'067':{'f1':'SDK retries cover selected transient or throttling errors, not every failed request.','f2':'Use botocore.config.Config(retries={"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS}) on the supplied client for bounded SDK backoff; do not loop around terminal errors.','f3':'Catch botocore.exceptions.ClientError around the supplied call. Inspect response["Error"]["Code"] and response["Error"]["Message"], preserve response["ResponseMetadata"]["RequestId"] when present, and report terminal failure or exhausted retries.','f4':'total_max_attempts includes the initial request; max_attempts in a Config object counts retries after it.'}}
out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for t in plan['tiles']:
 tile={'tile_id':t['tile_id'],'title':' / '.join(titles[C[c]] for c in t['concept_ids']),'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  cs=s['concept_ids'];c=cs[0];key=C[c]
  st={k:copy.deepcopy(s[k]) for k in ['step_id','type','concept_ids']}
  st['lineage']={k:copy.deepcopy(s[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}
  st['title']=titles[key];st['eyebrow']={'explainer':'Understand','check':'Check your judgement','hands_on':'Evidence review','video':'Notification route','recap':'Takeaways'}[s['type']]
  if s['type']=='explainer':
   st['blocks']=[]
   for tbid in s['teaching_block_ids']:
    cid,local=tbid.split('#');tb=next(x for x in B[cid]['teaching_blocks'] if x['id']==local)
    txt=text[C[cid]][int(local[2:])-1]
    # A block teaches just one glossary teaching idea; split multi-paragraph mechanisms into short prose units.
    if len(txt.split())>90:
     sentences=re.split(r'(?<=[.!?])\s+',txt);parts=[];part=''
     for sentence in sentences:
      if len((part+' '+sentence).split())>90:parts.append(part);part=''
      part=(part+' '+sentence).strip()
     if part:parts.append(part)
    else:parts=[txt]
    if local=='tb3' and C[cid]=='067':
     parts=[
      ('Configure the supplied Boto3 client with botocore.config.Config(retries={\"mode\": \"standard\", \"total_max_attempts\": APPROVED_ATTEMPTS}) for bounded SDK backoff. Do not loop around terminal errors.', ['f2']),
      ('Catch botocore.exceptions.ClientError around the supplied call. Inspect response[\"Error\"][\"Code\"] and response[\"Error\"][\"Message\"], retain response[\"ResponseMetadata\"][\"RequestId\"] when present, and report terminal failure or exhausted retries.', ['f3']),
      ('total_max_attempts includes the initial request; Config max_attempts counts retries after it.', ['f4'])]
     for part,fs in parts:st['blocks'].append(prose(cid,part,[tbid],[cid+'#'+f for f in fs],tb['purpose']))
    else:
     for part in parts:st['blocks'].append(prose(cid,part,[tbid],[cid+'#'+f for f in tb['fact_ids']],tb['purpose']))
   if s['planned_visual_block_type']:st['blocks']+=visual(c)
  elif s['type']=='video':
   st['title']='Trace the notification route';st['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif s['type'] in ['check','hands_on']:
   st['title']=('Review ' if s['type']=='hands_on' else 'Judge ')+titles[key][0].lower()+titles[key][1:]
   st['lede']='Read the supplied excerpts in this step and decide which conclusions or procedures are correct, defective or unsafe.'
   facts=s['fact_ids'];tbs=[c+'#'+tb['id'] for tb in B[c]['teaching_blocks'] if set(tb['fact_ids']) & {f.split('#')[-1] for f in facts}]
   rm={'step_id':t['tile_id']+f'.r{len(tile["remediation_steps"])+1:02d}','type':'remediation','required':False,'concept_ids':cs,'title':'Revisit '+titles[key][0].lower()+titles[key][1:],'eyebrow':'One clear contrast','lineage':lineage(c,tbs,facts),'blocks':[]}
   for f in facts:
    local=f.split('#')[-1]
    statement=remfacts.get(key,{}).get(local,next(x['statement'] for x in B[c]['coverage']['required_facts'] if x['id']==local))
    rm['blocks'].append(prose(c,statement,tbs,[f]))
   rm['blocks'].append(prose(c,contrasts[key],tbs,facts,'misconception'))
   rm['blocks'].append(table(c,key,'Revisit the same supplied exercise evidence'))
   tile['remediation_steps'].append(rm)
  else:
   st['title']='Keep the evidence distinctions';st['blocks']=[]
   for cid in cs:
    facts=[cid+'#'+f['id'] for f in B[cid]['coverage']['required_facts']];tbs=[cid+'#'+tb['id'] for tb in B[cid]['teaching_blocks']]
    st['blocks'].append(prose(cid,takeaways[C[cid]],tbs,facts,'takeaway'))
   nt=next((x for x in plan['tiles'] if x['tile_id']==t['next_tile_id']),None)
   if nt:st['blocks'].append({'type':'up_next','title':titles[C[nt['concept_ids'][0]]],'text':text[C[nt['concept_ids'][0]]][0]})
   else:st['blocks'].append({'type':'up_next','title':'Continue to '+t['next_tile_id'],'text':'Continue the operational-response path.'})
  tile['steps'].append(st)
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Mistakes-to-avoid and contract audit: ids, text lineage, budget, assets, plan fidelity and forbidden authored outputs.
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
for t,pt in zip(out['tiles'],plan['tiles']):
 assert t['tile_id']==pt['tile_id']
 for s,ps in zip(t['steps'],pt['steps']):
  for k in ['step_id','type','concept_ids']:assert s[k]==ps[k]
  for k in ['teaching_block_ids','fact_ids']:assert s['lineage'][k]==ps[k]
  count=sum(len(b.get('text','').split()) for b in s.get('blocks',[]) if b['type'] in ['prose','up_next'])
  assert count<=ps['word_budget'],(s['step_id'],count,ps['word_budget'])
for x in walk(out):
 if x.get('type')=='prose':
  assert x.get('lineage') and len(x['text'].split())<=90
  assert not re.search(r'\bvideo\b',x['text'],re.I)
 if 'lineage' in x:
  for f in x['lineage'].get('fact_ids',[]):assert '#f' in f and f.split('#')[0] in B
  for tb in x['lineage'].get('teaching_block_ids',[]):assert '#tb' in tb and tb.split('#')[0] in B
 if x.get('type') in ['diagram','code_walkthrough','data_table','before_after']:assert any(a.endswith('#visual') for a in x['lineage']['anchors'])
 assert not any(k in x for k in ['result','output','computed_values','execution_provenance'])
 if 'asset_ref' in x:
  a=A[x['asset_ref']['asset_id']]
  assert set(x['asset_ref'].get('columns',[])) <= {v['name'] for v in a['columns']}
print('Mistakes-to-avoid checklist passed; tiles',len(out['tiles']),'planned steps',sum(len(t['steps']) for t in out['tiles']),'remediation',sum(len(t['remediation_steps']) for t in out['tiles']))
