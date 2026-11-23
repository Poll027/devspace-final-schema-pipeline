import json, copy, re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.06_2')
P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); A=json.loads((B/'scenario_asset_registry.json').read_text())
byc={c['context']['concept_id']:c for c in G['bundles']}; assets={a['asset_id']:a for a in A['assets']}
# Authored re-voicing: each entry names precisely the facts and teaching blocks it teaches.
texts={
117:[
 [('definition','tb2','f1','EventBridge retries retryable target-delivery failures within two configured limits: maximum event age and retry attempts.'),('mechanism','tb3','f2 f3 f4','Set RetryPolicy MaximumRetryAttempts and MaximumEventAgeInSeconds to the approved finite budget. Set DeadLetterConfig to the approved SQS queue ARN, with required queue permissions, and inspect the seeded exhausted failure there. Some nonretryable failures go directly to capture; not every failure receives retries.')],
 [('example','tb4','f1 f2 f3','Review both finite limits and the capture route. A retry count alone does not prove the approved queue can accept the failed event. Check its permissions and inspect the seeded exhausted-delivery event in that queue.'),('misconception','tb4 tb5','f1 f4 f3','Contrast retry exhaustion with direct capture. A retryable failure is interpreted against the age and attempt limits; some nonretryable failures reach capture without a full retry history. Both need inspectable capture evidence. An ARN in the configuration is not a substitute for checking the captured event.')]],
118:[
 [('definition','tb1 tb2','f1','An ECS rolling deployment replaces service tasks within minimumHealthyPercent and maximumPercent bounds relative to desiredCount. These settings do not mean every update replaces all tasks at once.'),('mechanism','tb3 tb4','f2 f3','Register the supplied new image version in a task-definition revision, then update the service to that revision. Follow service events, running task revisions and health until the supplied steady-state criteria pass.'),('misconception','tb5','f3','An accepted service-update request is not evidence of a healthy rollout. Keep the replacement settings alongside the observed events, revisions and health; completion depends on the supplied steady-state checks, not the request.')]],
119:[
 [('definition','tb1 tb2','f1','Build produces an artifact. Release combines that build with environment configuration, and run executes the release. A staging-tested output should remain the same built content when promoted.'),('mechanism','tb3 tb4','f2 f3','Carry the same immutable artifact reference or digest from staging to production, supplying production configuration rather than rebuilding the source. Compare deployed digests and recorded build provenance in both environments to verify that the tested output is the promoted output.'),('misconception','tb5','f2 f3','The registered comparison keeps one artifact and build provenance across staging and production while configuration differs. Rebuilding from the same source is not this same-artifact check. Different deployed digests do not show that the tested output was promoted.')]],
120:[
 [('definition','tb1 tb2','f1','Deleted resources do not establish zero cost. Cost Explorer refreshes at least once every 24 hours; some data can take longer to appear.'),('mechanism','tb3','f2 f3','Filter the supplied teardown interval by account and service or usage type. Compare usage timestamps with deletion evidence. Distinguish pre-deletion charges from continuing usage, then repeat after billing-data refresh rather than concluding from resource absence.')],
 [('example','tb4','f1 f2 f3','In the registered initial and refreshed reports, use the same teardown interval and account/service filter. The initial extract has no matching usage row: retain that as a provisional reporting observation, not measured zero usage. The refreshed extract adds a charge for usage before deletion. Its appearance in a later report is not proof of continuing usage.'),('misconception','tb4 tb5','f1 f3','Compare when usage occurred with the deletion evidence, not merely when the report was opened. Repeat after refresh, remembering that some data can appear later. Neither an early empty report nor resource absence proves zero cost; a later charge is not automatically post-deletion usage. This is a timing check, not a new price estimate.')]],
121:[
 [('definition','tb1 tb2','f1','Remote Terraform state can contain sensitive values. S3 backend access therefore needs permissions for the selected state bucket and object key.'),('mechanism','tb3 tb4','f2 f3','Scope approved readers and writers to the required ListBucket prefix and GetObject/PutObject state-object operations. Configure supplied locking permissions separately. Initialize the intended backend and provision the separate exercise bucket through the approved identity. Test that an unapproved identity cannot read or overwrite state, retaining outcomes without exposing state contents.'),('misconception','tb3 tb5','f4','State access isolation prevents unauthorized access; a separate mechanism coordinates concurrent authorized writers. Backend initialization does not prove isolation, and locking is not the authorization boundary. Check unapproved read and overwrite attempts independently of approved provisioning.')]],
122:[
 [('definition','tb1 tb2','f1','S3 lock-file locking is opt-in: enable it with use_lockfile = true. Two authorized operations must not change shared state concurrently.'),('mechanism','tb3','f2 f3','Use the supplied s3:GetObject, s3:PutObject and s3:DeleteObject permissions on the .tflock object. While the controlled state-changing operation holds the lock, attempt the competing operation. Verify it cannot acquire the lock or change state; do not disable locking to bypass contention.'),('mental_model','tb3','f4','Locking coordinates concurrent state writers. It does not protect against identities authorized to change state objects directly.')],
 [('example','tb4','f1 f2 f3 f4','Review the two authorized operations against the same state. The first holds the lock; the competing operation must fail lock acquisition and leave state unchanged. Retain the .tflock observations and contention evidence. Keep this coordination test separate from authorization tests for direct state-object access.'),('misconception','tb5 tb6','m1 f1 f4','Force-unlock has a narrow recovery role: a failed operation left a lock and automatic unlocking failed. It is not a safe bypass for another active writer. Lock-file locking remains opt-in and is not an authorization boundary; disabling it to let the second operation proceed defeats the contention test.')]],
123:[
 [('definition','tb1 tb2','f1','Manual approval stops pipeline progression until an authorized approver approves. Rejection or expiration fails the action.'),('mechanism','tb3 tb4','f2 f3','Place approval between staging and production with the supplied review link or revision context and authorized approver permissions. Verify the pipeline waits there, then advances only after approval of the intended execution and revision.'),('misconception','tb5 tb6','m1 f3','A notification does not grant approval authority. Check the approver permissions separately from notification delivery. Approval recorded for one revision is not approval of another; keep the intended execution and revision with the wait and progression evidence.')]],
124:[
 [('definition','tb1 tb2','f1','A runbook describes known procedures and expected operational outcomes.'),('mechanism','tb3','f2 f3','Verify its preconditions, take only approved actions, and check each expected result before advancing. On a supplied stop condition or an out-of-bounds outcome, stop routine execution and escalate with observed evidence.')],
 [('example','tb4','f1 f2 f3','Use the supplied runbook to compare each actual result with its expected outcome. A passing result permits the next approved action. A supplied stop condition or result outside the bounds calls for stopping and escalation. Preserve the last completed action and the result that required escalation so the next responder has a reproducible record.'),('misconception','tb4 tb5','f2 f3','A runbook that initially matches the incident is not unconditional permission to continue. Its preconditions, expected results and stop bounds remain in force at each action boundary. Do not improvise extra resource changes when a check says the situation is outside routine execution; preserve the observed evidence and escalate.')]],
125:[
 [('definition','tb1 tb2','f1','An isolated recovery rehearsal needs two independent comparisons: restoration time against RTO and recoverable data loss against RPO.'),('mechanism','tb3','f2 f3','Measure elapsed time from the defined disruption start to passing service-readiness checks for RTO. Measure the gap from the disruption point to the latest recovered data point for RPO. A running service alone proves neither objective.')],
 [('example','tb4','f1 f2 f3','Inspect the registered illustrative timestamps, passing-readiness evidence and recovered markers. Compare restoration_minutes with rto_minutes, and data_gap_minutes with rpo_minutes. The alternative marker leaves restoration time unchanged but changes the data-loss comparison. Keep each conclusion attached to its own evidence; these are illustrative objectives and measurements, not AWS defaults.'),('misconception','tb5','f1 f2 f3','A good RTO result cannot substitute for the RPO result. Passing readiness establishes the endpoint for the restoration-time measurement, not the latest recovered data point. Likewise, a recent recovered marker does not establish how long restoration took. Retain both timestamp comparisons instead of calling recovery successful because the service runs.')]],
126:[
 [('definition','tb1 tb2','f1','Post-incident analysis records impact, events, contributing causes and actions to reduce recurrence.'),('mechanism','tb3','f2 f3','Build the timeline from supplied evidence. Separate direct observations from causal conclusions supported by the verified fix. Tie one preventive action to the demonstrated cause, naming an accountable owner and a completion check.')],
 [('example','tb4','f1 f2 f3','Read the registered symptom, investigation, correction and verification observations in timestamp order. The verified correction supports the identified configuration error, not an additional invented cause. The follow-up detects that same mismatch, assigns an accountable owner and checks completion by replaying the supplied mismatch. Keep this bounded conclusion separate from the factual timeline.'),('misconception','tb4 tb5','f2 f3','A plausible causal story is not a supported conclusion. Do not treat every nearby event as a contributing cause, assign unsupported blame, or choose unrelated improvements. A preventive action should address the recurrence path demonstrated by the verified fix. Its owner and verification method make the follow-up accountable.')]],
127:[
 [('definition','tb1 tb2','f1','Recovery includes restoring service and directing clients to the recovered environment. A restored target alone is not verified client convergence.'),('mechanism','tb3 tb4','f2 f3','First confirm the restored target passes the supplied readiness checks. Perform the approved DNS or application endpoint switch, then verify clients reach the restored target. For DNS, account for cached answers and TTL in those client checks.'),('misconception','tb4 tb5','f2 f3','An updated DNS setting and an old cached client answer can coexist. Keep actual client-target evidence rather than declaring every client moved at the update request. Configuration change is not proof of convergence: verify clients reach the ready restored target, with caching and the supplied TTL accounted for.')]]
}
recaps={
117:'Bound retries by both age and attempts. Verify queue permissions and inspect the captured failure. Some nonretryable failures go directly to capture without a full retry history.',
118:'Replacement percentage bounds are relative to desiredCount. Register the new image revision and update the service, then verify events, running revisions and health against the supplied steady-state criteria. Update acceptance alone is not completion.',
119:'Build once; release combines that artifact with environment configuration. Promote the same immutable reference or digest, not a rebuild. Compare deployed digests and build provenance across staging and production.',
120:'Filter the teardown interval and compare usage timestamps with deletion evidence. Reporting can lag; repeat after refresh. An early empty report does not prove zero cost, and a later charge does not automatically prove continuing usage.',
121:'Protect the selected state bucket, prefix and object key with scoped access. Verify approved provisioning and denied unapproved read/overwrite without exposing state contents. Authorization and concurrent-writer coordination are separate checks.',
122:'Enable opt-in S3 lock-file locking and its .tflock permissions. During contention, verify the competitor cannot acquire the lock or change state. Do not bypass an active writer. Locking coordinates writers; it is not an authorization boundary.',
123:'Approval belongs between staging and production. Verify waiting and progression for the intended execution and revision. Rejection or expiration fails the action; a notification alone does not grant approval authority.',
124:'Verify preconditions, take only approved actions and compare each result with the expected outcome. At a stop condition or out-of-bounds result, stop and escalate with evidence. A familiar runbook is not unconditional permission to continue.',
125:'Measure disruption-to-passing-readiness time against RTO. Separately measure the recovered-data gap against RPO. One passing comparison cannot replace the other, and a running service alone proves neither.',
126:'Keep the incident timeline factual. Separate observations from the causal conclusion supported by the verified fix. Justify one preventive action from that demonstrated cause, with an accountable owner and a verifiable completion condition.',
127:'Confirm restored-target readiness before the approved endpoint switch. Verify clients actually reach the restored target afterward. For DNS, account for cached answers and TTL rather than assuming an immediate universal switch.'}
short_titles={117:'Bound retries and verify capture',118:'Observe the ECS rollout',119:'Promote one built artifact',120:'Separate usage time from report time',121:'Test the state access boundary',122:'Verify lock contention',123:'Wait for authorized approval',124:'Stay within the runbook',125:'Measure time and data separately',126:'Connect evidence to prevention',127:'Verify endpoint convergence'}
contrasts={
117:'Contrast a retryable failure exhausting finite limits with a nonretryable failure that can go directly to capture. A full retry history is not required for every captured failure.',
118:'Contrast an accepted update request with verified steady state: only the latter checks service events, running revisions and health.',
119:'Contrast one promoted build with a rebuild from the same source. Compare deployed digests and provenance, not merely source identity.',
120:'Contrast report appearance time with usage time. The refreshed registered row concerns usage before deletion; an early empty extract is provisional.',
121:'Contrast authorization with coordination: denying unapproved read/overwrite protects access; locking coordinates authorized writers.',
122:'Contrast legitimate recovery of a failed operation’s leftover lock with bypassing an active writer. Contention is a reason to verify blocking, not disable locking.',
123:'Contrast notification receipt with permission to approve. Only authorized approval of the intended execution and revision supports progression.',
124:'Contrast a matching expected result with an out-of-bounds result. The first permits the next approved action; the second requires stopping and escalation.',
125:'Contrast the registered alternative recovered marker with the illustrative marker: restoration time is unchanged, but the data-loss comparison differs.',
126:'Contrast a direct observation with a supported causal conclusion. The registered verified correction supports the configuration error, not an invented additional cause.',
127:'Contrast the changed DNS setting with clients’ actual targets. Cached answers can persist; verify convergence with the supplied TTL in view.'}
contrast_facts={117:'f1 f4',118:'f3',119:'f2 f3',120:'f1 f2 f3',121:'f4',122:'f3 m1',123:'f3 m1',124:'f2 f3',125:'f1 f2 f3',126:'f2',127:'f2 f3'}
check_titles={117:'Does capture require retries?',118:'Is the rollout verified?',119:'Is the tested artifact unchanged?',120:'What does the report timing prove?',121:'Authorization or writer coordination?',122:'What does contention establish?',123:'What permits pipeline progression?',124:'When must routine execution stop?',125:'Are both recovery objectives verified?',126:'Is prevention justified by evidence?',127:'Does a DNS update prove convergence?'}
data_for={119:'ds.artifact_promotion',120:'ds.residual_charge_reports',125:'ds.recovery_objectives',126:'ds.incident_evidence_to_action'}

def lineage(c,fs=(),tbs=(),anchors=()):
 return {'concept_ids':[c], 'fact_ids':[c+'#'+f for f in fs], 'teaching_block_ids':[c+'#'+tb for tb in tbs], 'anchors':[c+'#'+a for a in anchors]}
def prose(c,text,fs,tbs,role):return {'type':'prose','text':text,'role':role,'lineage':lineage(c,fs,tbs)}
def diagram(c,labels,edges=(),kind='sequence',alt=None):
 nodes=[{'id':'n'+str(i+1),'label':label} for i,label in enumerate(labels)]
 return {'type':'diagram','diagram_kind':kind,'nodes':nodes,'edges':[{'from':'n'+str(a),'to':'n'+str(b),'label':label,'directed':True} for a,b,label in edges], 'alt_text':alt or ' → '.join(labels),'lineage':lineage(c,anchors=['visual'])}
def table(n,c):
 a=assets[data_for[n]]
 return {'type':'data_table','asset_ref':{'asset_id':a['asset_id'],'columns':[col['name'] for col in a['columns']]},'caption':a['title'],'lineage':lineage(c,anchors=['visual'])}
def visual(n,c):
 if n in data_for:return table(n,c)
 if n==117:
  return {'type':'process_flow','direction':'LR','nodes':[{'id':'failure','label':'Delivery failure','kind':'decision'},{'id':'retry','label':'Finite age + attempt limits'},{'id':'capture','label':'Approved SQS capture'},{'id':'inspect','label':'Permissions + event inspection'}], 'edges':[{'from':'failure','to':'retry','label':'Retryable'},{'from':'retry','to':'capture','label':'Exhausted'},{'from':'failure','to':'capture','label':'Some nonretryable failures'},{'from':'capture','to':'inspect'}], 'alt_text':'Retryable delivery is bounded by event age and attempts before exhaustion reaches capture. Some nonretryable failures go directly to capture. Verify queue permissions and inspect the captured event.','lineage':lineage(c,anchors=['visual'])}
 if n==118:
  d=diagram(c,['Service settings: desiredCount; minimumHealthyPercent; maximumPercent','Register supplied image version B in a task-definition revision','Service updated to selected revision','During replacement: inspect service events, running revisions and health','Verified steady state: supplied criteria pass'],[(1,4,'Replacement bounds'),(2,3,'Select revision'),(3,4,'Observe'),(4,5,'Verify')]);d['title']='Schematic ECS rollout review';return d
 if n==121:
  left=diagram(c,['Selected state bucket / ListBucket prefix','Selected state key / GetObject + PutObject','Approved readers and writers: scoped operations','Unapproved identity: verify denied read and overwrite'],[(3,1,'Scoped listing'),(3,2,'Scoped object access'),(4,2,'Denial check')],kind='architecture')
  right=diagram(c,['Approved identity initializes intended backend','Separate exercise bucket provisioned','Record access outcomes, not state contents','Supplied locking permissions configured separately'],[(1,2,'Approved provisioning'),(2,3,'Retain evidence')],kind='sequence')
  return {'type':'side_by_side','left_label':'State authorization boundary','right_label':'Separate provisioning and coordination','left':left,'right':right,'takeaway':'Authorization prevents unapproved access; locking coordinates authorized writers.','lineage':lineage(c,anchors=['visual'])}
 if n==122:
  left=diagram(c,['Authorized terminal 1: controlled state-changing operation holds lock','.tflock present during contention','Authorized terminal 2: competing operation fails lock acquisition','Verify competitor makes no state change'],[(1,2,'Lock held'),(2,3,'Contention'),(3,4,'Verify')])
  right=diagram(c,['First operation completes normally','.tflock absent after normal completion','Retain contention and lock observations'],[(1,2,'Released'),(2,3,'Evidence')])
  return {'type':'side_by_side','left_label':'Schematic: contention','right_label':'Schematic: normal completion','left':left,'right':right,'takeaway':'Verify blocking without disabling locking or bypassing an active writer.','lineage':lineage(c,anchors=['visual'])}
 if n==123:
  d=diagram(c,['Staging: intended execution and revision','Approval pending: review link / revision context','Authorized approver approves intended execution and revision','Production progression verified','Rejection or expiration: action fails'],[(1,2,'Wait point'),(2,3,'Authorized decision'),(3,4,'Advance'),(2,5,'Reject / expire')]);d['title']='Schematic approval state review';return d
 if n==124:
  d=diagram(c,['Verify supplied runbook preconditions','Current approved action','Expected outcome ↔ actual result','Within bounds: record result, next approved action','Stop condition / outside bounds: stop and escalate with evidence'],[(1,2,'Before action'),(2,3,'Check'),(3,4,'Matches'),(3,5,'Stop / mismatch')]);d['title']='Schematic runbook execution record';return d
 if n==127:
  return diagram(c,['Restored target passes supplied readiness checks','Approved DNS or application endpoint switch','Updated endpoint setting','Some DNS clients may retain cached answers within supplied TTL','Verify clients reach the restored target'],[(1,2,'Ready first'),(2,3,'Setting changes'),(3,4,'Not immediate convergence'),(3,5,'Client checks'),(4,5,'Account for caching / TTL')],kind='timeline')
 raise ValueError(n)

out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
rem_targets={}
for tile in P['tiles']:
 n=int(tile['tile_id'].split('.')[-1]);c=tile['concept_ids'][0];bundle=byc[c];facts={f['id']:f['statement'] for f in bundle['coverage']['required_facts']+bundle['coverage'].get('misconceptions',[])};tbs={tb['id']:tb for tb in bundle['teaching_blocks']}
 T={'tile_id':tile['tile_id'],'title':short_titles[n],'steps':[],'remediation_steps':[]};ei=0
 for ps in tile['steps']:
  s={k:copy.deepcopy(ps[k]) for k in ['step_id','type','concept_ids']};s['lineage']={k:copy.deepcopy(ps[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']};s['eyebrow']={'explainer':'Learn','video':'Observe','check':'Check','hands_on':'Review evidence','recap':'Takeaways'}[ps['type']]
  if ps['type']=='explainer':
   s['title']=short_titles[n] if ei==0 else 'Read the evidence, not the shortcut'
   s['blocks']=[prose(c,text,fs.split(),ts.split(),role) for role,ts,fs,text in texts[n][ei]];ei+=1
   if ps['planned_visual_block_type']:s['blocks'].append(visual(n,c))
  elif ps['type']=='video':
   s['title']='Observe the operating model';s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
  elif ps['type']=='check':
   s['title']=check_titles[n]
   if n==122 and ps['fact_ids']==[c+'#f4']:s['title']='Is locking an access boundary?'
   s['lede']='Read the supplied question and choose the conclusion supported by the evidence.'
  elif ps['type']=='hands_on':
   s['title']='Review '+short_titles[n].lower()
   if ps['planned_interaction_type'] in ['classify','choice']:
    s['lede']='Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.'
   else:
    s['title']='Document the supported follow-up';s['lede']='Use the supplied incident evidence to write a factual timeline, a separately supported causal conclusion and one accountable preventive action.'
  elif ps['type']=='recap':
   s['title']='Keep these distinctions';s['blocks']=[prose(c,recaps[n],[f for f in facts if not (n==122 and f=='m1')],list(tbs),'takeaway')]
   if tile['next_tile_id']:
    nt=next(t for t in P['tiles'] if t['tile_id']==tile['next_tile_id']);nc=byc[nt['concept_ids'][0]]
    first=next(tb for tb in nc['teaching_blocks'] if tb['purpose']=='intro')
    # The up-next names the first idea without teaching the future operating details.
    s['blocks'].append({'type':'up_next','title':'Next: '+short_titles[int(nt['tile_id'].split('.')[-1])],'text':first['content'].split('. ')[0].rstrip('.')+'.'})
  T['steps'].append(s)
  if ps['type'] in ['check','hands_on']:
   rid=tile['tile_id']+'.r'+str(len(T['remediation_steps'])+1).zfill(2);rem_targets[ps['step_id']]=rid
   fs=[f.split('#')[1] for f in ps['fact_ids']];rtbs=[tb['id'] for tb in tbs.values() if set(tb['fact_ids'])&set(fs)]
   blocks=[];chunk=[];chunkfs=[]
   for f in fs:
    if sum(len(x.split()) for x in chunk)+len(facts[f].split())>85:
     blocks.append(prose(c,' '.join(chunk),chunkfs,rtbs,'definition'));chunk=[];chunkfs=[]
    chunk.append(facts[f]);chunkfs.append(f)
   if chunk:blocks.append(prose(c,' '.join(chunk),chunkfs,rtbs,'definition'))
   # Contrast lineage also records the extra facts explicitly discussed in the review.
   contrast=contrasts[n];cfs=contrast_facts[n].split()
   if n==122 and fs==['f4']:
    contrast='Contrast competing authorized operations with direct state-object access. A lock coordinates the former; it is not an authorization boundary for identities able to change state objects directly.';cfs=['f4']
   ctbs=[tb['id'] for tb in tbs.values() if set(tb['fact_ids'])&set(cfs)]
   blocks.append(prose(c,contrast,cfs,ctbs,'misconception'))
   if n in data_for:blocks.append(table(n,c))
   T['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':[c],'title':'Review: '+short_titles[n].lower(),'eyebrow':'Try the contrast','required':False,'blocks':blocks,'lineage':lineage(c,fs,rtbs)})
 out['tiles'].append(T)
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
(B/'working/remediation_targets.json').write_text(json.dumps(rem_targets,indent=2)+'\n')
print('Wrote',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
