import json
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.04_2')
load=lambda p:json.loads((B/p).read_text())
p=load('tile_plans.json'); screens=load('screens.json'); glossary=load('inputs/path_glossary_bundle.json'); registry=load('scenario_asset_registry.json')
g={x['context']['concept_id']:x for x in glossary['bundles']}
assets={x['asset_id']:x for x in registry['assets'] if x['asset_kind']=='dataset'}
def rows(id):
 a=assets[id];return [dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
def block(x):return '```text\n'+(x if isinstance(x,str) else json.dumps(x,indent=2))+'\n```'
def choice(prompt,options,hint):
 return dict(public={'prompt':prompt,'selection':'single','shuffle':True,'options':[{'option_id':f'o{i+1}','text':t} for i,(t,_) in enumerate(options)]},grading={'correct_option_ids':['o1'],'option_feedback':{f'o{i+1}':{'message':msg} for i,(_,msg) in enumerate(options)}},hint=hint,correct=options[0][1],incorrect='Recheck the supplied evidence; configuration or an accepted request alone is not the required outcome.')
def classify(prompt,items,hint,correct,incorrect):
 return dict(public={'prompt':prompt,'buckets':[{'bucket_id':'meets','label':'Meets the stated review criterion'},{'bucket_id':'fails','label':'Does not meet the stated review criterion'}],'items':[{'item_id':f'i{i+1}','text':block(t)} for i,(t,ok,msg) in enumerate(items)]},grading={'assignments':{f'i{i+1}':('meets' if ok else 'fails') for i,(_,ok,_) in enumerate(items)},'item_feedback':{f'i{i+1}':{'message':msg} for i,(_,_,msg) in enumerate(items)}},hint=hint,correct=correct,incorrect=incorrect)
content={}
# Retry reporting check and implementation judgement.
retry=rows('ds.retry_counting'); budget=retry[0]['configured_value']
content['067.check']=choice('A supplied AWS call raises ClientError after a terminal failure or exhausted SDK retries. Which final report preserves the required evidence?',[
 ('Report failure with Error Code and Message, plus ResponseMetadata RequestId when present.','The final failure report preserves the error details and optional request identity.'),
 ('Report failure using only the exception class name.','The class name omits the required Error Code and Message and available RequestId.'),
 ('Report success because the supplied function was called.','Calling the function does not turn its raised ClientError into a successful outcome.')], 'Which fields explain the failure and allow the request to be traced?')
proper=f'''APPROVED_ATTEMPTS = {budget}
client = supplied_client_setup(Config(retries={{"mode": "standard", "total_max_attempts": APPROVED_ATTEMPTS}}))
try:
    result = supplied_ready_call(client)  # one application-level invocation
except ClientError as error:
    code = error.response["Error"]["Code"]
    message = error.response["Error"]["Message"]
    request_id = error.response.get("ResponseMetadata", {{}}).get("RequestId")
    report_failure(code, message, request_id)
else:
    report_success(result)
# SDK handles eligible retries and backoff; terminal/exhausted errors are reported.'''
content['067.hands_on']=classify(f'Read each supplied implementation. Decide whether it meets the approved total budget of {budget} requests, uses standard SDK retries without repeating the call at application level, and reports success or terminal/exhausted failure with Code, Message and optional RequestId safely. The setup/call/report helpers and imports are supplied. Every snippet is a separate implementation.',[
 (proper,True,'The total budget includes the initial request; the call occurs once at application level, and both success and failure paths report outcomes with safe optional metadata access.'),
 (proper.replace('"total_max_attempts"','"max_attempts"'),False,f'Config max_attempts counts retries after the initial request. Here that permits {retry[1]["maximum_total_requests"]} total requests, not the approved total budget.'),
 (proper.replace('request_id = error.response.get("ResponseMetadata", {}).get("RequestId")','request_id = error.response["ResponseMetadata"]["RequestId"]'),False,'Direct indexing of optional RequestId can raise another exception when it is absent, instead of reporting the original failure.'),
 ('while True:\n'+'\n'.join('    '+line for line in proper.splitlines()),False,'An unlimited wrapper repeats terminal failures; SDK retries cover selected transient or throttling errors, not every failed call.')], 'Separate application-level calls from SDK requests, and consider an error response without metadata.', 'All three requirements matter: bounded SDK attempts, one supplied call, and useful final reporting.', 'Do not accept a snippet that meets only the attempt budget or only the reporting requirement.')
# Billed evidence, with derived values and complete recommendation excerpts.
bill=rows('ds.billing_evidence'); driver=bill[0]; required=bill[1]
summary=lambda r:f'account={r["account"]}; period={r["period_start"]} through {r["period_end"]}; service={r["service"]}; usage_type={r["usage_type"]}; billed_cost=USD {r["billed_cost"]}; usage={r["usage"]} {r["usage_unit"]}'
content['068.check']=choice('Read this filtered billed-usage record and owner context. Which recommendation is supported?\n'+block({'billing':driver}),[
 (f'Recommend review of {driver["usage_type"]}; cite {summary(driver)} and the owner record that temporary usage is no longer required.','The recommendation ties the avoidable charge to filtered billed cost, usage and supplied owner context, and requests review.'),
 ('Delete every resource with an old name; its existence proves this billed charge.','Resource existence and age do not establish a specific charge; the evidence supports review, not independent deletion.'),
 (f'Recommend eliminating {required["usage_type"]} solely because storage resources exist.','The supplied context says this usage remains required, and resource existence alone does not justify an avoidable billed charge.')], 'Look for both billed usage attribution and context explaining avoidability.')
content['068.hands_on']=classify(f'Read each proposed Cost Explorer review note. The selected account is {driver["account"]}, the selected inclusive period is {driver["period_start"]} through {driver["period_end"]}, and grouping is by service or usage type. Decide whether the note identifies an avoidable charge with matching billed cost/usage, supplied context, and a recommendation for review only (no deletion or forecast).\nFiltered and comparison records:\n'+block('\n'.join(summary(r)+'; '+r['supplied_context'] for r in bill)),[
 (summary(driver)+'\n'+driver['supplied_context']+'\nRecommendation: review this no-longer-required temporary usage with the owner; no deletion or forecast.',True,'This cites the selected account/period, grouping, cost and usage, and the owner-supported reason for review.'),
 (summary(bill[2])+'\nRecommendation: review this as the selected account cost driver.',False,'This record belongs to a different account, so it cannot establish the selected account driver.'),
 (summary(bill[3])+'\nRecommendation: review this as the selected period cost driver.',False,'This record is outside the selected period.'),
 (summary(required)+'\nRecommendation: remove this charge because storage resources exist.',False,'The owner context says the usage remains required; inventory does not establish avoidability.')], 'Check the scope first, then the owner context behind the recommendation.', 'The accepted note retains scope, grouping, billed values and an evidence-backed review recommendation.', 'Reject scope mismatches and resource-existence guesses even when they contain real billed numbers.')
# EKS snapshots and full evidence judgement.
eks=rows('ds.deployment_reconciliation'); before,during,after=eks; name=before['deployment']
content['069.check']=choice('In the controlled orders Deployment test, one approved Pod deletion is accepted. Which observation verifies reconciliation?',[
 (f'The removed Pod {after["removed_pod"]} is replaced by {after["replacement_pod"]}; requested replicas remain {after["requested_replicas"]} and observed replicas return to {after["observed_replicas"]}.','Replacement identity and restored observed count verify the controller has restored the requested target.'),
 ('The deletion command reports that it was accepted; no later inspection is needed.','Accepted deletion does not establish creation of a replacement or restoration of the requested count.'),
 ('The observed count briefly falls, so the requested replica target must have changed.','The requested target remains unchanged while the observed count temporarily falls during reconciliation.')], 'What must you observe after deletion rather than infer from the command response?')
base={'apply_evidence':f'kubectl apply -f {name}-deployment.yaml accepted','inspection':f'kubectl get deployment {name} and associated Pods','before':before,'controlled_removal':during}
complete={**base,'after':after,'conclusion':'Controller replacement verified; requested target stayed unchanged and observed count returned to target.'}
content['069.hands_on']=classify('Read each supplied test report. Decide whether it verifies applying the supplied Deployment, inspecting requested count and associated Pods before controlled removal, identifying the removed and replacement Pods, and restoring the unchanged requested count. Deletion acceptance by itself is insufficient.',[
 (complete,True,'Before/after Pod identities show the replacement; requested count remains the same and the observed count returns to it.'),
 ({**base,'after':None,'conclusion':'Deletion was accepted, therefore reconciliation is verified.'},False,'The report lacks replacement identity and the restored observed count.'),
 ({**base,'after':during,'conclusion':'The remaining Pods are enough; reconciliation verified.'},False,'This is still the temporary shortage snapshot: no replacement is identified and observed count remains below target.')], 'Compare requested and observed counts separately, then compare Pod identities.', 'Complete reconciliation evidence combines unchanged target, removed/replacement identity and restored count.', 'A temporary shortage or accepted deletion is not the completed controller outcome.')
# Recovery ordering derives all steps/edges and key from registered dependency record.
recovery=rows('ds.recovery_dependencies'); byid={r['step_id']:r for r in recovery}; order=[]
while len(order)<len(recovery):
 ready=[r['step_id'] for r in recovery if r['step_id'] not in order and (r['prerequisite_step_id'] is None or r['prerequisite_step_id'] in order)]
 assert len(ready)==1, 'Ordering must be uniquely justified by supplied dependencies'
 order.append(ready[0])
content['070.check']=choice('A recovery procedure says database restoration finished, but database readiness has not been checked. Application resumption depends on usable database recovery. Which next step is justified?',[
 ('Verify database readiness before resuming the application.','Readiness verification prevents completed restoration from being mistaken for usable recovery.'),
 ('Resume the application immediately because the restore command finished.','A completed restoration step is not the required readiness verification.'),
 ('Skip verification because the recovery plan lists all components.','A component list does not verify prerequisite readiness before a dependent service resumes.')], 'Does a completed procedure establish the readiness the dependent service needs?')
content['070.hands_on']={'public':{'prompt':'Order these supplied steps using the dependency record below. Each verification must pass before the dependent step. Objective: usable orders service with verified infrastructure and database prerequisites. Only the listed restoration, readiness-check and resumption capabilities are supplied; no numeric recovery target is given. Then judge whether this plan supports that objective. These edges apply only to this workload.\n'+block('\n'.join(r['step_id']+' <- '+(r['prerequisite_step_id'] or 'none')+'; '+r['supplied_capability'] for r in recovery)),'items':[{'item_id':r['step_id'],'text':r['step']} for r in reversed(recovery)],'follow_up':{'prompt':'Which comparison with the supplied objective and capabilities is supported?','options':[{'option_id':'supported','text':'The ordered plan uses supplied restoration/readiness capabilities and gates application resumption on verified prerequisites; it supports the stated qualitative objective, but no numerical recovery guarantee is established.'},{'option_id':'guaranteed','text':'Listing these steps guarantees any numerical recovery target without checking readiness.'}]}},'grading':{'correct_order':order,'follow_up_correct_option_ids':['supported']},'hint':'Follow each prerequisite edge, including the readiness checks; distinguish a qualitative objective from an unspecified numeric guarantee.','correct':'The order follows every supplied dependency and verification gate, and the comparison stays within the supplied capabilities and qualitative objective.','incorrect':'Check the prerequisite edges and readiness gates. Listed steps alone do not guarantee an unspecified recovery target.'}
# Logs: query+retained events judgement includes boundaries, identity and order traps.
logs=rows('ds.orders_logs'); sample=logs[0]; group=sample['log_group']; identity=sample['request_id']; field='request_id'
# Window comes from the supplied text description, not authored numeric guesses.
import re
window=re.findall(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ',assets['ds.orders_logs']['description'])[:2]; start,end=window
matching=sorted([r for r in logs if r['log_group']==group and start<=r['@timestamp']<=end and r[field]==identity],key=lambda r:r['@timestamp'])
query=f'fields @timestamp, @message, {field} | filter {field} = "{identity}" | sort @timestamp asc'
seq=' → '.join(r['@message'] for r in matching)
content['071.s03']=choice('Read the relevant request events. Which sequence is supported by shared request identity and ascending timestamps?\n'+block(matching),[
 (seq,'The retained events share the request identity and establish receipt, failure, then response in timestamp order.'),
 ('Response recorded first, then request receipt, then failure.','That reverses the supplied chronological evidence.'),
 ('Every nearby error belongs to this request and proves its root cause.','Time proximity alone neither establishes shared request identity nor proves causation.')], 'Compare the timestamps, not the order in which rows may have arrived.')
report={'selected_log_group':group,'time_window':[start,end],'query':query,'retained_events':matching,'sequence':seq,'claim':'These events correlate this request; they do not prove root cause.'}
wrongid={**report,'query':query.replace(identity,logs[3][field]),'retained_events':[logs[3]],'sequence':logs[3]['@message']}
reverse={**report,'query':query.replace('asc','desc'),'retained_events':list(reversed(matching)),'sequence':' → '.join(r['@message'] for r in reversed(matching))}
outsides={**report,'retained_events':[logs[4]]+matching,'sequence':logs[4]['@message']+' → '+seq}
content['071.s04']=classify(f'Read each supplied Logs Insights query/result report and decide whether it meets the target: log group {group}, interval {start} through {end}, field {field}, request {identity}, ascending timestamp order, and retained receipt/failure/response evidence only. The query commands must be piped together. Do not treat unrelated nearby messages as evidence for this request.',[
 (report,True,'The group, interval, request filter and piped ascending sort match; the retained events support receipt, failure, response without claiming causation.'),
 (wrongid,False,'The filter and retained event belong to a different request, not the supplied identity.'),
 (reverse,False,'The descending sort and reversed evidence violate the required ascending reconstruction.'),
 (outsides,False,'The retained earlier event is outside the supplied time window, even though its request identity matches.')], 'Check scope and identity before reconstructing the order.', 'The accepted report has matching query scope and chronological retained evidence for the target request.', 'A shared identity alone is insufficient if the time window or order is wrong.')
# Alarm action/confirmation/receipt judgement.
alarm=rows('ds.alarm_receipt'); confirmed,unconfirmed=alarm
content['071.s07']=choice('An alarm has its approved SNS action, but the recipient subscription is unconfirmed and no test receipt is recorded. Which conclusion is supported?',[
 ('Delivery to the intended owner is not yet verified; confirm when required and verify a test receipt with alarm and workload context.','Configuration alone does not verify delivery; confirmation and contextual receipt evidence are required.'),
 ('The configured action proves the owner received the test notification.','The supplied case has no receipt evidence, so configuration cannot establish delivery.'),
 ('This proves that every unconfirmed subscription always fails in every situation.','The fact is that an unconfirmed subscription may not deliver; this case does not justify a universal claim.')], 'Which evidence comes from the recipient rather than from configuration?')
changed={**confirmed,'metric_evaluation_changed':True}
content['071.s08']=classify('Read each notification report. The approved configuration and receipt case are shown below. Decide whether each report shows the approved alarm/topic and recipient, confirmation when required, unchanged metric evaluation, and actual test receipt containing alarm and workload context.\nApproved case:\n'+block(confirmed),[
 (confirmed,True,'Approved routing, confirmed subscription, unchanged evaluation and contextual recipient receipt are all recorded.'),
 (unconfirmed,False,'The subscription is unconfirmed and this report has no receipt evidence; delivery is not verified.'),
 (changed,False,'Even with receipt evidence, this proposal changes metric evaluation; the task is routing without such a change.')], 'Inspect routing, subscription state and recipient evidence separately from metric evaluation.', 'The accepted report verifies the route and contextual receipt without modifying metric evaluation.', 'Topic configuration alone is not receipt evidence; changing metric evaluation also violates the stated task.')
# Lambda scope and separate result/log verification.
lamb=rows('ds.lambda_outcomes'); failed,success,permission=lamb
content['073.check']=choice('Read the supplied Lambda result and logs. Which outcome statement is supported?\n'+block(failed),[
 ('Invocation succeeded, but the operational task failed; retain both the returned failure and execution-log evidence.','Invocation status and operational result are distinct; the returned result and logs support task failure.'),
 ('The operation succeeded because invocation_status is success.','Successful invocation does not override the returned task failure and supporting logs.'),
 ('Ignore the result and logs; invocation status is all the operational evidence needed.','Operational success must be assessed using the returned task result and execution logs.')], 'Compare the invocation status with the task result and log message.')
broad={**success,'approved_task_scope':'All actions and resources, including tasks beyond the supplied resource check'}
content['073.hands_on']=classify('Read each supplied Lambda review record and proposed conclusion. Decide whether it keeps the approved role limited to the supplied resource-check actions/resources, uses the supplied payload unchanged, and correctly distinguishes invocation status from task outcome using returned result and execution logs. Do not broaden permissions.\nApproved task/role/payload context:\n'+block({k:failed[k] for k in ['function','execution_role','approved_task_scope','supplied_payload']}),[
 ({**failed,'conclusion':'Invocation succeeded; the task failed, supported by its returned result and execution logs. Keep the approved role unchanged.'},True,'This preserves bounded role/payload context and reports task failure rather than inferring success from invocation.'),
 ({**success,'conclusion':'Invocation and this bounded task succeeded, supported by returned result and logs. No broader operation is verified.'},True,'The result and logs support success for the bounded supplied task, with unchanged scope and payload.'),
 ({**failed,'conclusion':'The task succeeded because invocation succeeded.'},False,'The conclusion contradicts the returned task failure and execution logs.'),
 ({**broad,'conclusion':'Task succeeded; unlimited scope is acceptable for this test.'},False,'The role scope extends beyond the approved task actions/resources, even if this invocation reports task success.'),
 ({**permission,'conclusion':'Report the permission/result evidence and task failure without broadening the approved role.'},True,'The failed task and permission evidence are retained without treating invocation as operational success or widening authority.')], 'Review permission scope and payload independently of the invocation status, then inspect the result and logs.', 'Both successful and failed tasks can be correctly judged when scope stays bounded and the conclusion matches results/logs.', 'Do not accept a success claim contradicted by logs/results or permissions beyond the approved task.')
# Assemble only planned interaction entries, with glossary-derived anchors/measures.
out={k:p[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for tile,screen in zip(p['tiles'],screens['tiles']):
 assert tile['tile_id']==screen['tile_id']
 number=tile['tile_id'].split('.')[-1]; entries=[];seen=set()
 for step in tile['steps']:
  if step['type'] not in ['check','hands_on']:continue
  key=(number+'.'+step['step_id'].split('.')[-1]) if number=='071' else number+'.'+step['type']
  c=content[key];cid=step['concept_ids'][0]
  measures=[]
  for a in step['anchors']:
   if '#assessment:' in a:
    cap=a.split('#assessment:')[1]; anchor=next(x for x in g[cid]['assessment_anchors'] if x['capability']==cap)
    facts=[f for f in anchor['fact_ids'] if cid+'#'+f in step['fact_ids']]
    assert facts
    measures.append({'concept_id':cid,'capability':cap,'fact_ids':facts})
  fb={'correct':{'message':c['correct']},'incorrect':{'message':c['incorrect']},'hints':[c['hint']]}
  if cid not in seen:
   remediation=next((r for r in screen['remediation_steps'] if cid in r['concept_ids']),None)
   if remediation:fb['remediation_step_id']=remediation['step_id']
  seen.add(cid)
  ix={'type':step['planned_interaction_type'],'interaction_id':'ix.'+step['step_id'],'difficulty':'intro' if step['type']=='check' else ('core' if number in ['067','068'] else 'stretch'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':step['anchors'],'public':c['public'],'grading':c['grading'],'feedback':fb}
  entries.append({'step_id':step['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Interactions:',sum(len(t['interactions']) for t in out['tiles']))
