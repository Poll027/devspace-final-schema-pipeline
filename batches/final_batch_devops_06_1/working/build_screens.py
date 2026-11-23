import json,copy,re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.06_1')
p=json.load(open(B/'tile_plans.json'));g=json.load(open(B/'inputs/path_glossary_bundle.json'));reg=json.load(open(B/'scenario_asset_registry.json'))
bundles={x['context']['concept_id']:x for x in g['bundles']}
assets={x['asset_id']:x for x in reg['assets']}
cs=[c for t in p['tiles'] for c in t['concept_ids']]
# Each paragraph is a single teaching idea. Fact associations are explicit.
texts=[
[
('Failure must reach the workflow: a nonzero command exit status means failure; zero means success.',[1]),
('Use run: TEST_COMMAND for the supplied unit and integration commands. Set promotion to needs: [UNIT_JOB, INTEGRATION_JOB], requiring both jobs.',[2]),
('Leave continue-on-error unset on blocking test steps. In the supplied failure case, promotion is skipped even though the other test succeeds. Tolerating that failure would defeat the blocking gate.',[3,2])],
[
('Keep the change small and coherent: this reduces review complexity and makes delivery feedback easier to act on.',[1]),
('Stage focused files with git add FILES, commit with git commit -m "MESSAGE", then git push the review branch. Request review through the supplied pull-request interface.',[2]),
('Include intent, a coherent diff and saved-plan evidence for the affected EC2 resource. After supplied approval, use that approved saved plan for the supplied CI apply; attach execution and resource-verification evidence.',[3,4])],
[
('Resilience testing deliberately introduces failures to check availability requirements. Bound the approved experiment to the supplied AZ components, define abort criteria and monitor client-visible behavior.',[1,2]),
('Verify that remaining independent capacity and the request path maintain required service behavior. Surviving instances alone do not prove availability.',[3])],
[
('Delete only exercise resources identified by stack membership or approved tags. Remove dependents before prerequisites and verify results. CloudFormation uses resource relationships when deleting a stack.',[1,2]),
('Empty the exercise S3 bucket before deletion: remove objects, all object versions and delete markers.',[3]),
('Inspect retained resources and failed deletions for approved follow-up. Completed deletion is not billing verification.',[4])],
[
('Recovery needs a valid, unexpired session with permissions for backup access and resource creation. Establish the approved session and inspect identity and expiry.',[1,2]),
('Before rehearsal, test the supplied backup-read and recovery-resource operations. Record both outcomes alongside lifetime. Unexpired credentials with denied backup access are not ready; successful access does not remove the lifetime requirement.',[2,3])],
[
('A recovery test belongs in a controlled environment that limits its effects. Prepare the supplied isolated account and network target.',[1,2]),
('Check that restoration destinations and client test traffic do not point to production. Record approved scope and stop conditions before provisioning resources or directing traffic. A sandbox label alone is not evidence of isolation.',[2,3])],
[
('An aws:approve Automation step pauses for the designated approvers to approve or reject. Place it before the protected operation; a pending request is not approval.',[1,2]),
('Use the supplied branching or failure path to prevent the protected operation on rejection or stop. When a stop condition occurs, use the approved stop operation and inspect execution state before allowing further actions.',[2,3])],
[
('Automation details include execution ID, step statuses, inputs, outputs and failure information. Record the supplied response’s execution ID, acting role, targets, start/end times and per-step outcomes.',[1,2]),
('Attribute underlying AWS actions using CloudTrail request identity and operation evidence. Retain both success and failure outcomes, not just a success-focused summary.',[3])],
[
('CloudTrail integrity validation uses signed digest files and hashes to detect modification or deletion of delivered logs.',[1]),
('Use aws cloudtrail validate-logs with --trail-arn ARN, --start-time TIME, --end-time TIME and --region REGION for the supplied interval. For an organization trail, also supply the required --account-id. Inspect validation failures.',[2]),
('Digest validation provides tamper evidence; it does not prevent unauthorized access or deletion.',[3])],
[
('S3 Object Lock retains object versions using governance or compliance mode and a retain-until date. Apply the supplied default duration and mode on the prepared bucket, then inspect individual audit-object versions.',[1,2]),
('During retention, compliance prevents deletion or shortening even by root. Governance permits bypass only with the necessary bypass authorization and request. Record each version’s mode and date rather than treating the modes as interchangeable.',[3])],
[
('The S3 backend stores state at a specified bucket and key, separate from managed-resource declarations. First provision the protected bucket using the supplied local-state bootstrap configuration.',[1,2]),
('Select that existing bucket with the line-separated backend block below, using the supplied bucket, key, Region and protection settings.',[3]),
('After changing the backend, run terraform init -migrate-state, approve the supplied migration and verify state at the intended bucket/key.',[4])],
[
('Terraform normally destroys an object before creating its replacement. create_before_destroy requests the reverse order where supported.',[1]),
('prevent_destroy rejects a destruction plan while that lifecycle rule remains in the resource’s configuration.',[2]),
('Set the supplied lifecycle argument in the resource block, introduce the controlled replacement-triggering change and inspect the plan’s order or prevention error before an approved permitted apply. Lifecycle controls do not replace scope and impact approval.',[3,4])],
[
('Stack creation provisions the template’s declared resources under the target account’s execution authority and selected Region.',[1]),
('Create the replacement EC2 stack with the supplied restoration template, approved recovery credentials, explicit isolated target and required parameters.',[2]),
('Monitor events until creation completes. Inspect resource IDs and outputs, then perform the supplied instance and service recovery-ready checks.',[3])],
[
('Inspector findings provide vulnerability evidence, affected resources and severity to inform release decisions.',[1]),
('Compare the supplied scan report with the stated severity threshold and documented exception policy to decide actionability.',[2]),
('The policy check must fail for an actionable unexcepted finding, and promotion must require its success. Retain the report and policy decision: running a scan alone does not enforce a gate.',[3])],
[
('Execution and action history identify failures and error details. Start with the first failing action in the selected execution; inspect its input revision and linked service logs to identify the correction.',[1,2]),
('After the approved correction, retest and verify that action succeeds before investigating later dependent actions that did not run.',[3])],
[
('EC2 system status checks concern underlying AWS host issues; instance checks concern instance software and networking.',[1]),
('Locate the affected workload using the supplied metric/log window. Inspect component service status, events and logs: the symptom alone does not prove its cause.',[2]),
('For a container, inspect state, exit status and recent logs. Apply the evidence-supported correction and repeat the supplied health check.',[3])],
[
('Deployment completion is not a live behavior check. Run the supplied smoke-check action against the deployed endpoint and compare its response with the expectation for the deployed revision.',[1,2]),
('In the supplied Lambda validation action, call PutJobSuccessResult with the job ID only after a passing check. On failure, call PutJobFailureResult so dependent progression remains blocked. Retain revision, endpoint result and job outcome together.',[3])]
]
contrasts=[
'One successful test does not satisfy two required gates. Inspect the failing command and the skipped promotion together.',
'Approval alone is not execution evidence. The focused change record also needs the approved saved plan, CI apply outcome and resulting resource verification.',
'Compare the supplied cases: independent capacity remains in both, but only the case with a working client request path demonstrates the required behavior. Preserve scope, abort criteria and client outcomes together; do not widen the experiment beyond the approved AZ components.',
'A current object listing is not complete version cleanup. The bucket also needs all versions and delete markers removed. Inspect retained and failed resources rather than assuming the completed operation removed everything; this flow verifies deletion, not charges.',
'An unexpired session can still lack backup-read permission. Read the session lifetime and both operation outcomes as separate readiness requirements.',
'A named recovery target is not enough if restoration or client traffic points to production. Check actual destinations within the recorded scope and stop conditions.',
'Pending, rejected and stopped are not approval to perform the protected operation. A stop request also needs execution-state inspection before further action.',
'A failed response step still belongs in the record. Keep its inputs, outputs and failure information with execution identity, targets and attributed CloudTrail operations.',
'A pass for one interval does not establish integrity for another. Preserve the seeded failure, with trail, account scope, interval and Region. Validation detects tampering; it is not access prevention.',
'The governance version’s authorized requested bypass does not apply to compliance. Inspect version-specific mode and retain-until date against the required interval.',
'The backend block selects storage; it does not create its own bucket. Keep the local-state bootstrap result and migrated-state destination in the record, then verify the intended bucket/key.',
'Compare ordering with prevention: create_before_destroy requests reversed order where supported, while a still-configured prevent_destroy rejects destruction. Neither outcome establishes acceptable scope or impact. Inspect plan evidence before an approved permitted apply; do not apply a rejected plan.',
'Completed stack events are not the service recovery-ready result. Compare the supplied instance and service checks with resource IDs and outputs; preserve a failed service check even when the instance check passes.',
'Compare an unexcepted actionable finding with a documented exception. Both remain scan evidence; retain the exception basis for its different gate outcome. A tolerated policy failure would not enforce the promotion precondition.',
'The supplied source succeeded, the build failed and deployment did not run. Inspect build error details and linked logs, apply the evidence-supported approved correction, then verify build success with the intended input. An unrun deployment is not an independent error.',
'A restarted component or improved metric does not erase a failed health check. Tie component logs to the affected workload and telemetry interval, and retain original and repeated health-check outcomes after the approved correction.',
'A completed deployment can still have a failing smoke response. Compare behavior for the intended revision before selecting the job-result reporting path.'
]
recaps=[
'Nonzero means failure. Require both supplied test jobs and do not tolerate blocking failures.',
'Keep changes focused and carry intent, diff and saved plan through approval, CI apply and resource verification.',
'Bound the failure and abort criteria. Judge availability by required client behavior and the remaining independent path, not survivor count.',
'Delete approved exercise resources dependent-first. Empty all S3 versions and delete markers; inspect retained or failed resources without claiming billing verification.',
'Check session identity and expiry plus both required access operations. Lifetime alone does not prove authorization.',
'Keep restoration and test traffic inside the isolated target. Record approved scope and stop conditions before action.',
'Approval precedes the protected operation. Rejection or stop prevents it; inspect execution state after stopping.',
'Keep execution identity, role, targets, timing and complete step evidence. Attribute AWS actions with CloudTrail; retain failures too.',
'Validate the supplied trail and interval with the required scope. Signed digests detect tampering; they do not prevent it.',
'Inspect each object version’s mode and retain-until date. Governance bypass needs authorization and request; compliance bars deletion or shortening during retention even by root.',
'Bootstrap the protected bucket first. Select the existing backend, initialize and migrate with approval, then verify the intended state location.',
'Inspect replacement order or prevention errors. create_before_destroy is conditional; prevent_destroy applies while configured. Keep scope and impact approval separate.',
'Use the approved isolated target and supplied template. Verify stack completion, IDs and outputs, then both instance and service readiness.',
'Apply the stated threshold and documented exceptions to scan evidence. Fail actionable unexcepted findings and require policy success for promotion.',
'Find the first failing action, inspect revision and logs, and verify an approved correction before investigating unrun dependents.',
'Distinguish system from instance checks. Inspect the affected component in the telemetry window, correct from evidence and repeat the health check.',
'Validate live behavior for the deployed revision. Report job success only after a pass; report failure to block dependent progression.'
]
review_topics=['blocking test gates','focused infrastructure change evidence','AZ availability evidence','exercise deletion evidence','recovery session readiness','rehearsal boundaries','approval and stop states','response execution evidence','log integrity validation','audit-object retention','backend setup and migration','replacement lifecycle evidence','isolated stack restoration','scan-policy gate evidence','pipeline failure evidence','component health evidence','smoke-check reporting']
asset_ids=list(assets)
assert len(cs)==len(texts)==len(asset_ids)==len(contrasts)
C={c:{'text':texts[i],'contrast':contrasts[i],'recap':recaps[i],'asset':asset_ids[i]} for i,c in enumerate(cs)}
# Abstract screen/topology labels; actual observations remain in referenced datasets.
ui_labels={
0:['Unit test command: exit status and job outcome','Integration test command: exit status and job outcome','Promotion: depends on both test jobs'],
1:['Focused review: intent and diff','Commit reference and saved EC2 plan','Reviewer approval','CI apply and resulting instance verification'],
4:['Approved session identity and expiry','Backup-read authorization outcome','Recovery-resource authorization outcome'],
6:['aws:approve: pending designated decision','Rejected or stopped execution','Protected operation: unexecuted'],
8:['Validation command: trail, account, interval and Region','Signed digest and delivered log validation','Pass or seeded integrity failure'],
12:['Isolated account, Region and execution authority','Supplied template and required parameters','Stack events, resource IDs and outputs','Separate instance and service checks'],
13:['Finding: vulnerability evidence, affected resource and severity','Threshold and documented exception policy','Policy result and promotion dependency','Retained report and policy decision'],
14:['Selected execution and input artifact revision','Successful source action','First failing build: error details and linked logs','Dependent deployment: did not run','Approved correction and intended-input retest'],
15:['Affected workload and telemetry interval','Component state, exit status and recent logs','Evidence-supported correction','Original and repeated health checks']}
def lin(c,facts,tbs,visual=False):
 d={'concept_ids':[c],'fact_ids':facts,'teaching_block_ids':tbs}
 if visual:d['anchors']=[c+'#visual']
 return d
def prose(c,text,nums,tbs,role='mechanism'):
 return {'type':'prose','role':role,'text':text,'lineage':lin(c,[c+'#f'+str(n) for n in nums],tbs)}
def table(c,lineage=None):
 return {'type':'data_table','asset_ref':{'asset_id':C[c]['asset'],'columns':[x['name'] for x in assets[C[c]['asset']]['columns']]},'lineage':lineage or lin(c,[],[],True)}
def graph(c,labels,edges=None,kind='container'):
 nodes=[{'id':'n'+str(i),'label':v} for i,v in enumerate(labels)]
 return {'type':'diagram','diagram_kind':kind,'nodes':nodes,'edges':[{'from':'n'+str(a),'to':'n'+str(b),'label':label} for a,b,label in (edges or [])],'alt_text':bundles[c]['visual_anchor']['purpose'],'lineage':lin(c,[],[],True)}
def flow(c,labels,edges=None):
 nodes=[{'id':'n'+str(i),'label':v} for i,v in enumerate(labels)]
 if edges is None:edges=[(i,i+1,'next') for i in range(len(labels)-1)]
 return {'type':'process_flow','nodes':nodes,'edges':[{'from':'n'+str(a),'to':'n'+str(b),'label':lab} for a,b,lab in edges],'alt_text':bundles[c]['visual_anchor']['purpose'],'lineage':lin(c,[],[],True)}
def visual(c,v):
 i=cs.index(c)
 if v=='data_table':return [table(c)]
 if v=='annotated_image':
  edges={0:[(0,2,'required'),(1,2,'required')],6:[(0,2,'must precede'),(1,2,'prevents execution')],14:[(1,2,'execution order'),(2,3,'dependency blocked'),(2,4,'approved correction and retest')]}.get(i)
  return [graph(c,ui_labels[i],edges),table(c)]
 if i==2:
  return [graph(c,['Client request','Approved failed AZ components','Remaining independent AZ capacity','Remaining request path','Observed behavior versus requirement'],[(0,3,'client path'),(3,2,'remaining capacity'),(3,4,'verify required behavior')],'architecture'),table(c)]
 if i==5:
  return [graph(c,['Approved scope and stop conditions','Isolated recovery account and network','Restoration destination','Client test traffic','Production: outside rehearsal paths'],[(0,1,'before action'),(2,1,'confined to'),(3,1,'confined to')],'network'),table(c)]
 if i==3:
  return [flow(c,['Approved stack membership or tags','Remove dependents before prerequisites; CloudFormation uses relationships','Remove objects, all object versions and delete markers','Delete empty exercise S3 bucket','Inspect deletion results','Confirmed removal','Retained or failed: inspect and obtain approved follow-up'],[(0,1,'bounded scope'),(1,2,'dependent-first'),(2,3,'bucket empty'),(3,4,'verify'),(4,5,'removed'),(4,6,'retained or failed')]),table(c)]
 if i==10:
  return [flow(c,['Local-state bootstrap: provision protected bucket','Backend block: select existing bucket and key','terraform init -migrate-state; approve supplied migration','Verify state at intended bucket/key']),table(c)]
 if i==11:
  left=graph(c,['Default: destroy before create','create_before_destroy: reverse order where supported'],kind='mapping')
  right=graph(c,['prevent_destroy configured: destruction plan rejected','Scope and impact approval still required for permitted apply'],kind='mapping')
  return [{'type':'side_by_side','left':left,'right':right,'left_label':'Replacement ordering','right_label':'Prevention and separate approval','takeaway':'Ordering requests and destruction prevention are distinct; neither replaces scope and impact approval.','lineage':lin(c,[],[],True)},table(c)]
 if i==16:
  return [flow(c,['Deployment operation completed','Supplied endpoint smoke check','Compare response with expected deployed revision','Pass: PutJobSuccessResult with job ID','Fail: PutJobFailureResult; dependent progression blocked'],[(0,1,'then validate'),(1,2,'live behavior'),(2,3,'matches'),(2,4,'does not match')]),table(c)]
 raise ValueError((c,v))
def teaching(s,c):
 tb=s['teaching_block_ids']
 first=any(x.endswith('#tb1') for x in tb)
 if first:
  blocks=[prose(c,text,nums,tb) for text,nums in C[c]['text']]
  if cs.index(c)==10:
   fact=next(f['statement'] for f in bundles[c]['coverage']['required_facts'] if f['id']=='f3')
   code=fact[fact.index('terraform {'):fact.rindex('}')+1]
   blocks.append(prose(c,code,[3],tb,'syntax'))
 else:
  blocks=[prose(c,C[c]['contrast'],[int(f.split('#f')[-1]) for f in s['fact_ids']],tb,'example')]
 if s.get('planned_visual_block_type'):blocks+=visual(c,s['planned_visual_block_type'])
 return blocks
out={'schema_version':p['schema_version'],'kind':'screens_part','path_id':p['path_id'],'batch_id':p['batch_id'],'tiles':[]}
for t in p['tiles']:
 title=' / '.join(bundles[c]['coverage']['learning_objective'] for c in t['concept_ids'])
 tile={'tile_id':t['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  c=s['concept_ids'][0];typ=s['type']
  lineage={k:copy.deepcopy(s[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}
  step={'step_id':s['step_id'],'type':typ,'concept_ids':s['concept_ids'],'title':title,'lineage':lineage}
  if typ=='explainer':
   step['eyebrow']='Read the evidence';step['title']=bundles[c]['coverage']['learning_objective'] if any(x.endswith('#tb1') for x in s['teaching_block_ids']) else 'Compare the evidence';step['blocks']=teaching(s,c)
  elif typ in ['check','hands_on']:
   step['eyebrow']='Evidence review' if typ=='hands_on' else 'Check your understanding'
   step['title']='Review '+review_topics[cs.index(c)]
   step['lede']='Read the supplied excerpts in this step and decide which conclusions or actions are correct, defective or unsafe.'
  elif typ=='video':step['title']='A closer look';step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  elif typ=='recap':
   step['title']='Keep these distinctions';step['blocks']=[]
   for rc in s['concept_ids']:
    fids=[rc+'#'+f['id'] for f in bundles[rc]['coverage']['required_facts']]
    step['blocks'].append({'type':'prose','role':'takeaway','text':C[rc]['recap'],'lineage':lin(rc,fids,[rc+'#'+tb['id'] for tb in bundles[rc]['teaching_blocks']])})
   nxt=next((x for x in p['tiles'] if x['tile_id']==t['next_tile_id']),None)
   if nxt:nc=nxt['concept_ids'][0];nt=bundles[nc]['teaching_blocks'][0]['content']
   else:
    nb=next((x for x in g['bundles'] if x['context']['toc_location']['tile_id']==t['next_tile_id']),None)
    nt=nb['teaching_blocks'][0]['content'] if nb else 'Continue to the next lesson.'
   # First idea named without importing future teaching claims into this tile.
   if nxt:next_title=bundles[nxt['concept_ids'][0]]['coverage']['learning_objective']
   elif nb:next_title=nb['coverage']['learning_objective']
   else:
    ordered_names=list(g['names']); ni=ordered_names.index(t['concept_ids'][-1])+1
    next_concept=ordered_names[ni]
    assert next_concept in bundles[t['concept_ids'][-1]]['context']['blocked_future_concepts']
    next_title=g['names'][next_concept]
   step['blocks'].append({'type':'up_next','title':next_title,'text':'Next: '+next_title+'.'})
  tile['steps'].append(step)
 # A separate remediation for each distinct measured fact set, including practice.
 seen=set()
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  c=s['concept_ids'][0];key=(c,tuple(s['fact_ids']))
  if key in seen:continue
  seen.add(key);nums=[int(f.split('#f')[-1]) for f in s['fact_ids']];tb=[c+'#'+x['id'] for x in bundles[c]['teaching_blocks']]
  blocks=[prose(c,text,[n for n in ns if n in nums],tb) for text,ns in C[c]['text'] if set(ns)&set(nums)]
  blocks.append(prose(c,C[c]['contrast'],nums,tb,'misconception'))
  blocks.append(table(c,lin(c,s['fact_ids'],tb)))
  tile['remediation_steps'].append({'step_id':t['tile_id']+'.r'+str(len(seen)).zfill(2),'type':'remediation','required':False,'concept_ids':[c],'title':'Separate the evidence','blocks':blocks,'lineage':lin(c,s['fact_ids'],tb)})
 out['tiles'].append(tile)
json.dump(out,open(B/'screens.json','w'),ensure_ascii=False,indent=2)
print('Wrote',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
# Local checklist: skeleton, traceability, prose length, budget, visual anchors, framing and asset columns.
for pt,t in zip(p['tiles'],out['tiles']):
 assert [(s['step_id'],s['type'],s['concept_ids']) for s in t['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in pt['steps']]
 for ps,s in zip(pt['steps'],t['steps']):
  for k in ['teaching_block_ids','fact_ids']:assert s['lineage'][k]==ps[k]
  prosewords=sum(len(x['text'].split()) for x in s.get('blocks',[]) if x['type']=='prose')
  assert prosewords<=ps['word_budget'],(s['step_id'],prosewords,ps['word_budget'])
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s and 'interaction' not in s
 for s in t['steps']+t['remediation_steps']:
  for block in s.get('blocks',[]):
   if block['type']=='prose':
    assert len(block['text'].split())<=90,(s['step_id'],len(block['text'].split()))
    assert 'lineage' in block and 'video' not in block['text'].lower()
    assert all('#' in x for x in block['lineage']['fact_ids']+block['lineage']['teaching_block_ids'])
   if block['type'] in ['diagram','side_by_side','process_flow'] or (block['type']=='data_table' and s['type']=='explainer'):assert any(a.endswith('#visual') for a in block['lineage']['anchors'])
   if block['type']=='data_table':assert block['asset_ref']['columns']==[x['name'] for x in assets[block['asset_ref']['asset_id']]['columns']]
print('Local mistakes-to-avoid checklist passed.')
