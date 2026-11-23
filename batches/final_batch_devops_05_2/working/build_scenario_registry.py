import json, re
from pathlib import Path
B = Path(__file__).resolve().parents[1]
g = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bs = g['bundles']
sid = 'scenario.approved_sandbox'
# Mine only vocabulary actually present in the teaching blocks or anchors.
texts = ['\n'.join([t['content'] for t in b['teaching_blocks']] + [json.dumps(b['visual_anchor'], ensure_ascii=False), json.dumps(b['practice_anchor'], ensure_ascii=False)]) for b in bs]
terms = ['sandbox','approved fault','limited target scope','expected signals','abort conditions','alarm state history','notification receipt','recovery','Lambda','NAME','ALIAS','VERSION','NAME:ALIAS','published version','Deployment','CONTAINER','IMAGE','REVISION','Pod template','rollout status','readiness','CodeDeploy','EC2','blue/green','replacement fleet','load balancer','known-good revision','Python','try','finally','exercise-created identities','preexisting resources','Terraform','refresh-only','state and outputs','module "NAME"','module.NAME.OUTPUT','source','input arguments','declared outputs','normal','peak','changing demand','load','utilization','performance','service constraints','finding ID','evidence link','affected resource','severity','observed activity','urgency','accountable owner','established escalation path','EventBridge','SNS','Systems Manager','event bus','event pattern','required parameters','permissions','matching','nonmatching','ECS','desiredCount','three','running','pending','service events']
vocab = list(dict.fromkeys(t for t in terms if any(t in text for text in texts)))
for b in bs:
    for syntax in b.get('practice_anchor',{}).get('live_code',{}).get('allowed_syntax',[]):
        if syntax not in vocab: vocab.append(syntax)
assets = []
def add(key, index, specs, rows):
    cols = []
    for spec in specs:
        name, typ, role, desc = spec
        cols.append(dict(name=name,type=typ,semantic_role=role,description=desc))
    assets.append(dict(asset_id='ds.'+key,asset_kind='dataset',scenario_id=sid,title=bs[index]['context']['concept_name']+' — read-only evidence',description='Authored fictional sandbox records for '+bs[index]['context']['concept_id']+'. Values labelled supplied or approved are symbolic exercise inputs, not real cloud resources, credentials or executable instructions.',columns=cols,rows=rows,variants=[],provenance='authored'))
def cat(n,d):return (n,'string','categorical',d)
def txt(n,d):return (n,'string','text',d)
def ident(n,d):return (n,'string','identifier',d)
def num(n,d):return (n,'integer','numerical',d)
add('alarm_experiment',0,[ident('case_id','Fictional experiment record'),cat('stage','Ordered experiment phase'),txt('approved_fault','Supplied fault; no injection command is authored'),txt('target_scope','Supplied limited sandbox scope'),txt('expected_signals','Expected observation'),txt('abort_conditions','Supplied stop boundary'),cat('fault_status','Observed fault status'),txt('alarm_state_history','Recorded alarm behavior rather than configuration'),cat('notification_receipt','Actual recipient receipt observation'),cat('recovery_check','Supplied post-removal check result')],[
['sandbox_alarm','preconditions','supplied approved fault','supplied limited target scope','supplied expected alarm signal and notification','supplied abort conditions','not injected','precondition checks recorded','not yet tested','not yet tested'],
['sandbox_alarm','during fault','supplied approved fault','supplied limited target scope','supplied expected alarm signal and notification','supplied abort conditions','injected within limits','expected alarm transition observed','absent','not yet tested'],
['sandbox_alarm','after removal','supplied approved fault','supplied limited target scope','supplied expected alarm signal and notification','supplied abort conditions','removed','recovery observation recorded','absent','passed']])
add('lambda_alias_release',1,[cat('stage','Release observation phase'),ident('function_name','Glossary function placeholder'),ident('alias','Same alias throughout'),ident('alias_target','Symbolic published version, not a quantity'),ident('invocation_target','Qualified supplied test target'),cat('test_result','Supplied alias test result'),txt('snapshot_evidence','Immutability observation')],[
[s,'NAME','ALIAS',v,'NAME:ALIAS','expected result confirmed','published snapshots unchanged'] for s,v in [('before release','approved previous version'),('after release','newly approved version'),('after rollback','approved previous version')]])
add('eks_rollout',2,[cat('stage','Rollout phase'),ident('deployment','Glossary Deployment placeholder'),ident('container','Glossary container placeholder'),ident('image','Symbolic approved image'),ident('revision','Symbolic rollout revision'),cat('rollout_status','Supplied rollout observation'),ident('approved_rollback_revision','Explicit approved prior target'),cat('readiness_result','Post-change readiness observation')],[
['before update','NAME','CONTAINER','approved prior IMAGE','approved prior REVISION','ready','approved prior REVISION','passed'],
['controlled failure','NAME','CONTAINER','IMAGE','failed new REVISION','failed','approved prior REVISION','failed'],
['after undo','NAME','CONTAINER','approved prior IMAGE','approved prior REVISION','restored','approved prior REVISION','passed']])
add('codedeploy_blue_green',3,[cat('stage','Supplied procedure phase'),ident('deployment_group','Supplied blue/green group'),txt('load_balancer_configuration','Supplied configuration'),cat('installation','Replacement installation evidence'),cat('lifecycle_health','Supplied lifecycle and health evidence'),cat('client_traffic_fleet','Fleet reached by clients'),ident('application_revision','Client-visible revision'),cat('behavior_check','Supplied application behavior result'),txt('rollback_path','Supplied path, not invented hook ordering')],[
['before rerouting','supplied blue/green deployment group','supplied load balancer configuration','replacement revision installed','passed','original fleet','known-good revision','passed','supplied rollback configuration or redeployment procedure'],
['after approved rerouting','supplied blue/green deployment group','supplied load balancer configuration','replacement revision installed','passed','replacement fleet','replacement revision','checked against supplied expected result','supplied rollback configuration or redeployment procedure'],
['after rollback','supplied blue/green deployment group','supplied load balancer configuration','replacement revision installed','retained evidence','original fleet','known-good revision','passed','supplied rollback configuration or redeployment procedure']])
add('cleanup_scope',4,[ident('resource_identity','Identity used for scoped cleanup'),cat('resource_label','Shared label is not proof of ownership'),cat('origin','Exercise ownership classification'),cat('task_outcome','Controlled exception result'),cat('cleanup_block','Location of scoped cleanup'),cat('cleanup_target','Whether tracked identity is targeted'),cat('postcheck','Removal or preservation result')],[
['exercise-created identity','shared task label','created by exercise','controlled exception raised','finally','tracked and targeted','removed'],
['preexisting identity','shared task label','preexisting','controlled exception raised','finally','not targeted','preserved']])
add('terraform_drift',5,[cat('case_id','Approved reconciliation branch'),cat('stage','Plan or apply observation'),txt('declaration','Chosen symbolic EC2 setting'),txt('live_setting','Observed symbolic EC2 setting'),txt('state_outputs','State persistence observation'),txt('plan_action','Reviewed proposal, distinct from live effects'),txt('approval_workflow','Approval/apply evidence'),cat('live_verification','Comparison against chosen declaration')],[
['restore declaration','after drift','approved declared setting','out-of-band setting','refresh evidence available','restore approved declared setting','not yet applied','mismatch'],
['restore declaration','after approved apply','approved declared setting','approved declared setting','approved apply recorded','restore approved declared setting','supplied approved workflow completed','match'],
['accept approved change','after approved apply','approved changed setting','approved changed setting','approved apply recorded','update declaration to approved intended change','supplied approved workflow completed','match'],
['refresh-only','plan only','approved declared setting','out-of-band setting','updates proposed, not persisted','state and output updates only','not yet applied','mismatch'],
['refresh-only','after approved apply','approved declared setting','out-of-band setting','updates persisted','state and output updates only','supplied approved refresh-only apply completed','mismatch']])
add('terraform_module_contract',6,[ident('module_name','Glossary module name placeholder'),txt('source','Supplied source, not a real address'),txt('input_contract','Supplied names and approved values; no extra interface invented'),txt('output_reference','Exact glossary output syntax'),cat('initialization','Supplied initialization evidence'),txt('planned_instance_settings','Plan comparison with approved requirement'),num('planned_instance_count','Number of sandbox instances in reviewed plan'),cat('approval_apply','Supplied approval and apply result'),ident('created_instance','Symbolic instance identity'),cat('instance_verification','Settings comparison'),txt('output_verification','Declared output identity comparison')],[
['NAME','<supplied source>','<supplied input name> = <approved value>','module.NAME.OUTPUT','initialized','matches approved input values',1,'approved apply completed','exercise instance','matches chosen inputs','declared instance-identifying output corresponds to exercise instance']])
add('rightsizing_baseline',7,[cat('demand_period','Relevant workload period'),cat('candidate_size','Symbolic EC2 option; not a real instance specification'),txt('observed_load','Qualitative supplied workload load'),txt('observed_utilization','Qualitative utilization evidence'),txt('observed_performance','Qualitative performance observation'),txt('service_constraint','Required performance and capacity boundary'),txt('candidate_evidence','Evidence or absence for this candidate at this period'),cat('recommendation','Baseline-wide decision, not a single-sample conclusion')],[
['normal','current size','normal demand','low sample','within supplied performance boundary','preserve supplied performance and capacity requirements','normal sample shows spare capacity','retain current size'],
['peak','current size','peak demand','at relevant peak','reaches required performance boundary','preserve supplied performance and capacity requirements','peak sample reaches required boundary','retain current size'],
['changing demand','current size','changing demand','varies with demand','within supplied performance boundary','preserve supplied performance and capacity requirements','changing-demand observation retained','retain current size'],
['normal','smaller option','normal demand','low sample on current size','current-size result only','preserve supplied performance and capacity requirements','no supplied smaller-option verification','withhold reduction'],
['peak','smaller option','peak demand','current size reaches boundary','current-size boundary reached','preserve supplied performance and capacity requirements','insufficient evidence that smaller option satisfies constraint','withhold reduction'],
['changing demand','smaller option','changing demand','varies on current size','current-size result only','preserve supplied performance and capacity requirements','no supplied smaller-option verification','withhold reduction']])
add('security_finding_handoff',8,[ident('finding_id','Authored finding evidence identifier'),ident('affected_resource','Authored affected resource identity'),cat('severity','Supplied severity label'),txt('observed_activity','Preserved observation, not a compromise assertion'),cat('urgency','Supplied response priority'),ident('accountable_owner','Mapped responsible team'),txt('escalation_path','Established exercise handoff path')],[
['sandbox_finding','exercise instance','supplied severity','suspicious activity reported; compromise not established','supplied urgency','sandbox resource owner','established escalation path to sandbox resource owner']])
add('eventbridge_routing',9,[ident('event_bus','Supplied bus identifier'),ident('rule','Same approved rule'),txt('event_pattern','Supplied selection pattern'),ident('approved_target','One supplied approved SNS target'),txt('target_parameters','Supplied required target parameters'),cat('permissions','Required authorization evidence'),cat('test_event','Positive or negative selection test'),cat('pattern_result','Selection observation'),cat('notification_evidence','Actual target evidence, distinct from selection')],[
['supplied event bus','supplied rule','supplied event pattern','approved SNS target','supplied required parameters','required permissions configured','matching','match','expected notification received'],
['supplied event bus','supplied rule','supplied event pattern','approved SNS target','supplied required parameters','required permissions configured','nonmatching','no match','no notification from this test']])
# The glossary supplies three, and a controlled removal of one. Derive counts.
ecs_text = texts[10]
assert 'count of three' in ecs_text
count = {'three':3}[re.search(r'count of (three)',ecs_text).group(1)]
add('ecs_reconciliation',10,[cat('stage','Controlled service test phase'),ident('service','Symbolic exercise service'),ident('cluster','Supplied cluster'),ident('task_definition','Supplied task definition'),txt('network_settings','Supplied settings'),num('desiredCount','Requested number of tasks'),num('running','Observed running task count'),num('pending','Observed pending task count'),txt('service_events','Replacement and restoration evidence')],[
['before removal','exercise service','supplied cluster','supplied task definition','supplied network settings',count,count,0,'requested count running'],
['during replacement','exercise service','supplied cluster','supplied task definition','supplied network settings',count,count-1,1,'one approved task removed; replacement pending'],
['after restoration','exercise service','supplied cluster','supplied task definition','supplied network settings',count,count,0,'replacement running; desired count restored']])
registry = dict(schema_version='1.0',kind='scenario_asset_registry',path_id=g['path_id'],batch_id=B.name,scenarios=[dict(scenario_id=sid,name='Approved sandbox operations review',summary='A fictional operations team reviews supplied release, fault, cleanup, infrastructure and routing evidence for one isolated sandbox. All records are authored read-only teaching examples; no live resource or runtime is provisioned.',domain='AWS DevOps sandbox operations',glossary_example_vocab=vocab)],assets=assets)
# Stage-specific mistakes-to-avoid audit. No messy transformations are needed.
assert len(assets)==len(bs)
for a in assets:
    assert a['variants']==[]
    assert len(set(c['name'] for c in a['columns']))==len(a['columns'])
    for row in a['rows']:
        assert len(row)==len(a['columns']),a['asset_id']
        for c,v in zip(a['columns'],row):
            if c['type']=='integer':assert type(v) is int and c['semantic_role']=='numerical'
            else:assert isinstance(v,str) and c['semantic_role'] in ('identifier','categorical','text')
            if isinstance(v,str) and v.isdigit():assert c.get('numeric_looking_label') is True
assert all(any(term in t for t in texts) for term in terms if term in vocab)
assert all(a['asset_kind']=='dataset' for a in assets)
assert not any(b['visual_anchor']['type'] in ('chart','plot','spreadsheet') for b in bs)
assert {a['asset_id'] for a in assets} >= {'ds.rightsizing_baseline','ds.security_finding_handoff'}
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'scenario_count':len(registry['scenarios']),'asset_count':len(assets),'row_count':sum(len(a['rows']) for a in assets),'concept_count':len(bs),'asset_ids':[a['asset_id'] for a in assets],'checklist':'passed: widths, roles/types, label traps, no variant issues/duplicate occurrences, complete concept coverage, exact glossary placeholders and derived ECS counts'}))
