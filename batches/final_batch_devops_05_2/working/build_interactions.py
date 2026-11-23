import json, sys
from pathlib import Path
sys.path.insert(0, str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from finlib import assessment_ref
B=Path('batches/final_batch_aws_devops.region.05_2')
plans=json.loads((B/'tile_plans.json').read_text())
screens=json.loads((B/'screens.json').read_text())
gloss={x['context']['concept_id']:x for x in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
registry=json.loads((B/'scenario_asset_registry.json').read_text())
# Each option includes its authored feedback; keys are generated from the marked option.
checks=[
('After removing the approved sandbox fault, which observation verifies recovery?',[
 ('The supplied recovery check reports the post-removal system result.',True,'Recovery must be checked after removing the fault.'),
 ('The alarm configuration still exists.',False,'Configuration does not verify recovery after fault removal.'),
 ('The expected notification arrived during the fault, so no recovery check is needed.',False,'Notification receipt during the fault and recovery after removal are separate observations.')]),
('Which statement correctly distinguishes a published Lambda version from an alias?',[
 ('The published version is an immutable snapshot; the alias can move between published versions.',True,'The version freezes code and most configuration; the alias selects the invocation target.'),
 ('Rollback edits the code inside the previously published version.',False,'Rollback moves the alias; it does not rewrite an immutable published snapshot.'),
 ('An alias is an immutable snapshot, while the published version is the movable pointer.',False,'This reverses the roles: the alias is movable and the version is immutable.')]),
('Which change creates a new Deployment Pod-template rollout revision?',[
 ('Updating the container image in the Pod template.',True,'A Pod-template change creates a new rollout revision.'),
 ('Scaling the number of replicas without changing the Pod template.',False,'Scaling alone does not create a new template revision.'),
 ('Checking rollout status without changing the Pod template.',False,'A status check observes the rollout; it is not a Pod-template change.')]),
('Which evidence verifies an EC2 blue/green rollback to the known-good revision?',[
 ('The supplied rollback procedure is followed, and traffic destination, revision and application behavior are verified.',True,'Rollback requires evidence of the traffic and behavior returning to the known-good revision.'),
 ('A rollback request was accepted, with no traffic or application check.',False,'Request acceptance is not verification of the resulting traffic or application behavior.'),
 ('The replacement revision was installed before the original traffic switch.',False,'Installation before the switch does not verify a later rollback outcome.')]),
('After the controlled Python task raises an exception, which postcheck demonstrates correctly scoped cleanup?',[
 ('Exercise-created identities are removed; preexisting identities remain, including ones sharing a label.',True,'Both removal and preservation must be verified by identity.'),
 ('Every identity sharing the exercise label is gone.',False,'Labels do not establish exercise ownership; a preexisting resource sharing the label must remain.'),
 ('The finally block was entered, so no resource postcheck is necessary.',False,'finally controls when cleanup runs; it does not prove correct cleanup scope or removal.')]),
('Observed EC2 settings differ from the declaration after an out-of-band change. What determines whether to restore the declaration or update it?',[
 ('Compare the observed settings and declaration with the approved intended requirement.',True,'The reconciliation choice follows approved intent, not merely whichever setting was observed last.'),
 ('Always accept the observed settings because refresh exposed them.',False,'Refresh reveals drift; it does not approve the observed change as intended.'),
 ('Always restore the old declaration even if an intended change was approved.',False,'The declaration may be updated to reflect an approved intended change.')]),
('Which evidence completes verification after applying a supplied Terraform EC2 module?',[
 ('The created instance settings and declared outputs agree with the chosen inputs.',True,'The created instance and declared outputs require post-apply verification.'),
 ('The configuration contains an output reference, so the live instance needs no check.',False,'An output reference is not live instance verification.'),
 ('Initialization completed, so no plan or created-instance comparison is needed.',False,'Initialization does not replace review of settings or verification of the created instance.')]),
('A normal observation shows low utilization, but the peak reaches a service performance boundary. What is required before recommending a smaller EC2 size?',[
 ('Compare the proposed size with every supplied capacity and performance constraint across normal, peak and changing demand.',True,'A reduction must preserve constraints across the relevant baseline.'),
 ('Use the normal observation alone because it shows spare capacity.',False,'One low-utilization sample does not account for peak or changing demand.'),
 ('Choose the smallest candidate regardless of the supplied peak performance.',False,'Rightsizing preserves workload requirements rather than simply choosing the smallest size.')]),
('A supplied finding reports suspicious activity. Which handoff preserves its evidentiary meaning?',[
 ('Retain the finding reference and reported activity without declaring compromise unsupported by the record.',True,'Preserve the evidence and avoid unsupported conclusions.'),
 ('Replace the activity description with "the resource is compromised".',False,'A stronger unsupported compromise claim is not a substitute for the finding evidence.'),
 ('Remove the finding reference and activity to make the handoff shorter.',False,'A concise handoff must not erase the evidence needed by the responder.')]),
('Which test evidence verifies the EventBridge route rather than just its pattern?',[
 ('At the approved target, the matching event has execution or notification evidence and the nonmatching event does not.',True,'Both event selection and actual approved-target evidence must be checked.'),
 ('The matching event passes a pattern-only check, without target evidence.',False,'Pattern matching in isolation does not verify target execution or notification.'),
 ('The target is listed in the rule, without testing either event.',False,'Configuration alone does not demonstrate matching and nonmatching event behavior.')]),
('After one approved ECS task is removed, which observation demonstrates restored service task count?',[
 ('Service events show replacement activity; running equals desiredCount and pending settles to zero.',True,'Service events and running/pending counts demonstrate completed restoration.'),
 ('The task definition still exists, without any count check.',False,'The task definition supplies what runs; it does not prove restored service task count.'),
 ('The service was created earlier, so replacement requires no observation.',False,'Service creation alone does not verify replacement after controlled removal.')])
]
# Inspect-and-judge records are intentionally inline, not registry datasets or runnable exercises.
classifiers={
0:('Read each sandbox experiment record. Decide whether it preserves a bounded, evidence-backed outcome or substitutes an unsupported success claim or unsafe scope change.',[
('Approved fault: supplied sandbox disruption; targets: limited approved scope; expected: alarm transition and recipient notification; abort: supplied stop condition.\nFault injected within limits. Alarm history: transition observed. Recipient receipt: absent. Fault removed with supplied control. Recovery check: recovered. Outcome: notification missing; do not claim full success.',True,'This record respects limits, records actual receipt and recovery, and preserves the missing notification honestly.'),
('Approved limits and fault followed. Alarm history: transition observed. Recipient receipt: absent. Fault removed. Recovery check: unsuccessful. Outcome: successful because the alarm was configured.',False,'Configuration cannot override absent receipt or unsuccessful recovery; preserve those outcomes.'),
('Before injection: abort conditions not recorded. During the fault: supplied stop condition reached; fault extended beyond the approved target scope to obtain an alarm. Recovery check omitted.',False,'Limits and abort conditions belong before injection; follow the stop path and verify recovery after removal.')]),
1:('Read each Lambda release-and-rollback transcript. Decide whether it verifies both approved alias updates using the alias-qualified test.',[
('Approved previous version: PREVIOUS; approved new version: NEW.\nBefore: ALIAS -> PREVIOUS.\naws lambda publish-version --function-name NAME\nResult: NEW\naws lambda update-alias --function-name NAME --name ALIAS --function-version NEW\nAfter release: ALIAS -> NEW; supplied test invokes NAME:ALIAS; expected NEW result confirmed.\naws lambda update-alias --function-name NAME --name ALIAS --function-version PREVIOUS\nAfter rollback: ALIAS -> PREVIOUS; supplied test invokes NAME:ALIAS; expected PREVIOUS result confirmed.',True,'The targets are recorded before, after release and after rollback, with alias-qualified result checks after both updates.'),
('Approved previous: PREVIOUS; approved new: NEW. Version NEW published; ALIAS moves PREVIOUS -> NEW -> PREVIOUS. Both checks invoke unqualified NAME. Record says alias verification complete.',False,'The supplied verification must target NAME:ALIAS; an unqualified invocation does not verify the alias target.'),
('Approved previous: PREVIOUS; new: NEW. Before: ALIAS -> PREVIOUS. After release: ALIAS -> NEW; NAME:ALIAS test confirms NEW. Rollback request accepted; no alias-target observation or post-rollback result check.',False,'Rollback needs the restored target observation and the alias-qualified test result, not only request acceptance.')]),
2:('Read each EKS rollout record. Decide whether it verifies the supplied image update and explicit approved rollback, including readiness.',[
('Supplied target: deployment/NAME, container CONTAINER, image IMAGE.\nkubectl set image deployment/NAME CONTAINER=IMAGE\nkubectl rollout status deployment/NAME\nControlled failure observed. Supplied history: failed revision FAILED; approved prior revision REVISION.\nkubectl rollout undo deployment/NAME --to-revision=REVISION\nRestored revision: REVISION. Supplied readiness check: ready.',True,'The record targets only the supplied image update, distinguishes revisions, restores the approved revision and verifies readiness.'),
('Image update targets deployment/NAME and CONTAINER=IMAGE; rollout status and history checked. History identifies approved prior REVISION and another unapproved prior OTHER. Undo targets OTHER; readiness reports ready.',False,'A ready unapproved history entry is not the explicit approved prior revision.'),
('Supplied image update and status checked. History distinguishes FAILED from approved REVISION. Undo to REVISION accepted. No readiness observation; record says rollback verified.',False,'Acceptance of undo alone is not the required readiness verification.')]),
3:('Read each EC2 blue/green record. Decide whether it verifies replacement readiness before traffic switching and verifies the traffic, revision and behavior outcomes after switching and rollback.',[
('Supplied deployment group, replacement fleet and load balancer used. Replacement revision installed; lifecycle passed; health passed before approved traffic switch. After switch: traffic reaches replacement fleet; expected revision and client-visible behavior confirmed. Supplied rollback/redeployment procedure followed. After rollback: traffic reaches procedure-designated known-good destination; known-good revision confirmed; application behavior passes supplied check.',True,'Installation, lifecycle and health precede switching; separate traffic, revision and behavior evidence verifies both outcomes.'),
('Supplied deployment group, fleet and load balancer used. Traffic switched before replacement lifecycle and health evidence was checked. Afterward health passed. Rollback procedure and final traffic, known-good revision and behavior were verified.',False,'Healthy evidence must be verified before the approved switch, not retroactively after rerouting.'),
('Replacement installation, lifecycle and health verified before approved switch; post-switch traffic, revision and behavior verified. Supplied rollback requested; record contains no post-rollback traffic, revision or behavior observations and calls rollback successful.',False,'The request does not verify return of traffic and application behavior to the known-good revision.')]),
4:('Read each controlled-failure cleanup excerpt and postcheck. Decide whether cleanup runs on the exception and removes only tracked exercise-created identities, preserving preexisting ones even with shared labels.',[
('Tracked exercise-created identities: CREATED; preexisting identity PREEXISTING shares the label.\ntry:\n    supplied_failing_task()\nfinally:\n    supplied_scoped_cleanup(CREATED)\nTrace: controlled exception; scoped cleanup called.\nPostcheck: CREATED removed; PREEXISTING remains.',True,'finally triggers the supplied scoped cleanup after the exception; the identity-based postcheck proves both removal and preservation.'),
('Tracked exercise-created identities: CREATED; PREEXISTING shares the label.\ntry:\n    supplied_failing_task()\n    supplied_scoped_cleanup(CREATED)\nfinally:\n    pass\nTrace: controlled exception before cleanup. Postcheck: CREATED still present; PREEXISTING remains.',False,'Cleanup placed after the failing task in try is skipped here; the supplied cleanup belongs in finally.'),
('Tracked exercise-created identities: CREATED; PREEXISTING shares the label.\ntry:\n    supplied_failing_task()\nfinally:\n    cleanup_every_identity_with_shared_label()\nTrace: controlled exception; cleanup called.\nPostcheck: CREATED removed; PREEXISTING also removed.',False,'finally does not make label-wide deletion safe; the preexisting identity must remain.')]),
5:('Read each Terraform drift record. Decide whether it completes reconciliation to approved intent, rather than treating refresh-only as remote repair.',[
('Initial instance provisioned through supplied workflow. Declaration: ORIGINAL; observed drift: CHANGED; approved requirement: restore ORIGINAL. New normal plan inspected: restore remote setting to ORIGINAL. Supplied approval/apply workflow completed. Postcheck: live setting ORIGINAL equals chosen declaration ORIGINAL.',True,'Approved intent, new plan, completed workflow and live comparison agree.'),
('Initial provisioning completed. Declaration ORIGINAL; live CHANGED; approved requirement restore ORIGINAL. Approved refresh-only plan applied: state and outputs reflect CHANGED. Remote remains CHANGED. Record says refresh-only restored ORIGINAL.',False,'Refresh-only state/output updates do not change remote infrastructure to restore the declaration.'),
('Initial provisioning completed. Approved requirement accepts CHANGED; declaration updated to CHANGED; new plan inspected. Approval/apply workflow not completed and no live comparison recorded. Record says editing the declaration completed reconciliation.',False,'The declaration choice alone is insufficient; complete the workflow and verify the live setting against it.')]),
6:('Read each supplied-module configuration and verification record. Decide whether it respects the supplied interface and verifies exactly one sandbox instance and declared outputs against chosen inputs.',[
('Supplied interface: source SOURCE; named input INPUT; declared output OUTPUT. Intended INPUT value: INTENDED.\nmodule "NAME" {\n  source = "SOURCE"\n  INPUT = "INTENDED"\n}\nOutput reference: module.NAME.OUTPUT.\nInitialized. Reviewed plan: exactly one sandbox EC2 instance with settings INTENDED. Approved apply completed. Created instance: exactly one, settings INTENDED. Declared OUTPUT agrees with created instance and chosen inputs.',True,'Only supplied interface names are used; the plan and created instance/outputs agree with chosen inputs.'),
('Supplied interface: source SOURCE; input INPUT; output OUTPUT. Configuration instead supplies invented input OTHER and references module.NAME.INVENTED. No declaration of either name exists in the supplied interface. Record claims module interface respected.',False,'A reusable module does not authorize invented inputs or outputs; use the supplied interface.'),
('Supplied source SOURCE, input INPUT=INTENDED and output module.NAME.OUTPUT used; initialized; plan reviewed for exactly one instance with settings INTENDED. Apply completed; actual instance settings DIFFERENT. Output and instance comparison reports mismatch. Record calls verification successful.',False,'Successful verification requires created settings and declared outputs to agree with the chosen inputs, not a mismatch.')]),
9:('Read each EventBridge configuration-and-test record. Decide whether it verifies only the approved route with required parameters, permissions and matching/nonmatching target evidence.',[
('Supplied bus BUS and pattern PATTERN configured. Only target: approved SNS notification target TARGET. Required target parameters match supplied values; required target permissions configured. Matching test event MATCH: notification observed at TARGET. Nonmatching event NONMATCH: no notification at TARGET. Both observations retained.',True,'The approved-only configuration and actual target evidence verify the positive and negative route tests.'),
('BUS and PATTERN configured. Approved TARGET has required parameters and permissions; an additional unapproved target EXTRA is also present. Matching and nonmatching results at TARGET are as expected.',False,'Correct test results at the approved target do not authorize an extra unapproved target.'),
('BUS and PATTERN configured with only approved TARGET and supplied parameters. Required target permissions not configured. Pattern-only check matches MATCH and rejects NONMATCH; no target execution or notification evidence recorded. Record says route verified.',False,'The route requires target permissions and actual approved-target evidence, not just pattern matching.')]),
10:('Read each ECS service configuration-and-replacement record. Decide whether the supplied configuration and observed task replacement meet the desired-count restoration criterion.',[
('Service uses supplied cluster CLUSTER, task definition TASK_DEFINITION, network NETWORK and desiredCount DESIRED. One approved task removed using supplied procedure. Service events: replacement activity observed. Final running count: DESIRED; final pending count: zero.',True,'The supplied configuration and replacement evidence show completed restoration to desiredCount with no pending tasks.'),
('Service uses supplied CLUSTER, TASK_DEFINITION, NETWORK and desiredCount DESIRED. One approved task removed. Events show replacement started. Running count remains below DESIRED; pending count has not settled to zero. Record says replacement complete.',False,'Replacement progress is not completed restoration; running must return to desiredCount and pending must settle to zero.'),
('Service created with a cluster different from supplied CLUSTER; other settings supplied. After controlled removal, events show replacement and running returns to DESIRED with pending zero. Record says all exercise criteria met.',False,'Restored count does not excuse configuration that differs from the supplied cluster.')])
}
output={k:plans[k] for k in ['schema_version','path_id','batch_id']}; output['kind']='interactions_part';output['tiles']=[]
concept_index=0
for t in plans['tiles']:
 sc=next(x for x in screens['tiles'] if x['tile_id']==t['tile_id'])
 by_c={c:concept_index+i for i,c in enumerate(t['concept_ids'])}; concept_index+=len(by_c)
 out_t={'tile_id':t['tile_id'],'interactions':[]}; seen=set()
 interactive=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 for pos,s in enumerate(interactive):
  c=s['concept_ids'][0]; idx=by_c[c]; g=gloss[c]
  measures=[dict(concept_id=c,**a) for a in g['assessment_anchors'] if assessment_ref(c,a['capability']) in s['anchors']]
  assert len(measures)==len([a for a in s['anchors'] if '#assessment:' in a])
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'], 'difficulty':('intro' if pos==0 else 'stretch' if pos==len(interactive)-1 else 'core'), 'grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors']}
  feedback={'correct':{'message':'The judgement matches the supplied evidence and verification requirements.'},'incorrect':{'message':'Separate the requested outcome from evidence that it actually occurred; check the approved scope and the missing observations.'},'hints':['Compare the recorded observations with every criterion in the question.']}
  if c not in seen:
   rem=next((r for r in sc.get('remediation_steps',[]) if c in r['concept_ids']),None)
   if rem: feedback['remediation_step_id']=rem['step_id']
   seen.add(c)
  else:
   remedies=[r for r in sc.get('remediation_steps',[]) if c in r['concept_ids']]
   if len(remedies)>1: feedback['remediation_step_id']=remedies[1]['step_id']
  ix['feedback']=feedback
  if s['type']=='check':
   prompt,opts=checks[idx]; options=[]; right=[]; of={}
   # Change correct-option position deterministically across concepts.
   opts=opts[idx%len(opts):]+opts[:idx%len(opts)]
   for j,(text,correct,why) in enumerate(opts):
    oid=f'o{j+1}';options.append({'option_id':oid,'text':text});of[oid]={'message':why}
    if correct:right.append(oid)
   ix['public']={'prompt':prompt,'options':options,'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':right,'option_feedback':of}
   feedback['correct']['message']=next(why for _,correct,why in opts if correct)
   feedback['incorrect']['message']='Review why each alternative fails the specific verification requirement.'
  elif ix['type']=='classify':
   prompt,records=classifiers[idx]
   ix['public']={'prompt':prompt,'buckets':[{'bucket_id':'meets','label':'Meets the stated verification criteria'},{'bucket_id':'fails','label':'Fails at least one stated criterion'}], 'items':[]}
   ix['grading']={'assignments':{},'item_feedback':{}}
   records=records[idx%len(records):]+records[:idx%len(records)]
   for j,(excerpt,correct,why) in enumerate(records):
    iid=f'i{j+1}';ix['public']['items'].append({'item_id':iid,'text':excerpt});ix['grading']['assignments'][iid]='meets' if correct else 'fails';ix['grading']['item_feedback'][iid]={'message':why}
  else:
   assert ix['type']=='table_select'
   a=next(a for a in registry['assets'] if ('sizing' in a['asset_id'])==(idx==7))
   cols=[x['name'] for x in a['columns']];rows=[dict(zip(cols,r)) for r in a['rows']]
   ix['public']={'asset_ref':{'asset_id':a['asset_id'],'columns':cols},'tasks':[]};ix['grading']={'answers':[],'task_feedback':{}}
   def task(prompt,row,where_cols,column=None):
    tid='t'+str(len(ix['public']['tasks'])+1)
    ix['public']['tasks'].append({'task_id':tid,'prompt':prompt,'target_kind':'cell' if column else 'row'})
    ans={'task_id':tid,'row':{'where':{k:row[k] for k in where_cols},'occurrence':0}}
    if column:ans.update(column=column,expect_value=row[column])
    ix['grading']['answers'].append(ans)
    ix['grading']['task_feedback'][tid]={'correct':'This selection preserves the supplied evidence needed for the decision.','incorrect':'Select the exact requested evidence, not a different period or an unsupported replacement claim.'}
   if idx==7:
    viable=[option for option in dict.fromkeys(r['size_option'] for r in rows) if all(r['response_latency_ms']<=r['max_response_latency_ms'] and r['capacity_utilization_pct']<=r['max_capacity_utilization_pct'] for r in rows if r['size_option']==option)]
    assert len(viable)==1
    option=viable[0]
    ix['public']['intro']='Choose the option that preserves every supplied latency and capacity bound across all three demand periods. Select its supporting row for each period, then the failing candidate evidence. Together these selections justify whether to withhold the smaller-size reduction; equality satisfies a bound.'
    for period in dict.fromkeys(r['demand_period'] for r in rows):
     row=next(r for r in rows if r['size_option']==option and r['demand_period']==period)
     task(f'Select the {period} row for the only size option that satisfies both constraints in every supplied demand period.',row,['workload','size_option','demand_period'])
    for row in rows:
     if row['response_latency_ms']>row['max_response_latency_ms']:
      task(f'Select the latency cell exceeding the bound in the {row["demand_period"]} row of the smaller candidate; this is evidence against the reduction.',row,['workload','size_option','demand_period'],'response_latency_ms')
    feedback['correct']['message']='The selected option preserves every supplied bound; peak and changing-demand candidate latency rule out the smaller-size reduction.'
   else:
    assert idx==8 and len(rows)==1
    row=rows[0]
    ix['public']['intro']='Select the supplied evidence and routing cells for an accurate finding handoff. Retain the reported activity as evidence, not an unsupported compromise conclusion. Use the mapped owner and established escalation route; each selected cell is part of the handoff.'
    prompts={'finding_id':'Select the evidence reference to retain in the handoff.','affected_resource':'Select the affected resource identity.','severity':'Select the reported severity without changing it.','observed_activity':'Select the reported activity to preserve without asserting compromise.','urgency':'Select the supplied urgency to communicate.','accountable_owner':'Select the accountable recipient from the owner mapping.','established_escalation_path':'Select the established path to follow if the owner is unavailable.'}
    for col in cols:task(prompts[col],row,['finding_id'],col)
    feedback['correct']['message']='The handoff retains evidence, resource, severity, activity and urgency, and follows the mapped owner and established escalation path without an unsupported compromise claim.'
  out_t['interactions'].append({'step_id':s['step_id'],'interaction':ix})
 output['tiles'].append(out_t)
(B/'interactions.json').write_text(json.dumps(output,indent=2)+'\n')
print('tiles',len(output['tiles']),'interactions',sum(len(t['interactions']) for t in output['tiles']))
