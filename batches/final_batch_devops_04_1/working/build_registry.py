import json,re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.04_1')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
# Mine only teaching and anchor strings, excluding prerequisite/future concepts.
def strings(x):
    if isinstance(x,str): yield x
    elif isinstance(x,list):
        for v in x: yield from strings(v)
    elif isinstance(x,dict):
        for v in x.values(): yield from strings(v)
texts=[t for b in g['bundles'] for k in ('teaching_blocks','visual_anchor','practice_anchor','assessment_anchors') for t in strings(b[k])]
source='\n'.join(texts)
terms=['CodeBuild','buildspec','version: 0.2','install','pre_build','build','post_build','commands','artifacts.files','base-directory','CodeDeploy','EC2','appspec.yml','files','hooks','deployment group','revision','service role','agent','target tracking','instance warmup','minimum','desired','maximum','ECR','ecr:GetAuthorizationToken','publisher','consumer','unapproved principal','rulePriority','selection','action','digest','tags','lifecycle preview','Application Load Balancer','listener','target group','health-check path','success codes','CloudWatch','retentionInDays','put-retention-policy','72 hours','RDS','snapshot','available','recovery marker','IAM','log-group','log-stream','resource scope *','containerDefinitions','name','image','portMappings','cpu','memory','cluster','explicit deny','permissions boundaries','organization policies','terraform show PLAN_FILE','terraform apply PLAN_FILE','AMI','instance type','placement','send-command','--instance-ids','--targets','command ID','status','output','terraform init -backend=false','terraform validate','terraform fmt -check','terraform fmt','GitHub Actions','aws_instance','continue-on-error: true']
vocab=[s for s in terms if s in source]
# Include exact anchor syntax automatically, not retyped code or facts.
for b in g['bundles']:
    for s in b['practice_anchor'].get('live_code',{}).get('allowed_syntax',[]):
        if s not in vocab: vocab.append(s)
sc='scen.harbor_operations'
reg={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':sc,'name':'Harbor application operations review','summary':'A fictional team reviews supplied build, deployment, policy, scaling, backup and command evidence for the Harbor application in a prepared AWS sandbox. All records are authored teaching cases, not observations of real infrastructure. Learners inspect evidence; no cloud resources or credentials are provisioned.','domain':'AWS delivery and operations','glossary_example_vocab':vocab}],'assets':[]}
def ds(id,title,cols,rows,desc):
    cc=[]
    for name,typ,role in cols:
        c={'name':name,'type':typ,'semantic_role':role}
        if typ=='string' and any(isinstance(r[len(cc)],str) and re.fullmatch(r'\d+(?:\.\d+)?',r[len(cc)]) for r in rows): c['numeric_looking_label']=True
        cc.append(c)
    reg['assets'].append({'asset_id':'ds.'+id,'asset_kind':'dataset','scenario_id':sc,'title':title,'description':'Read-only authored case. '+desc,'columns':cc,'rows':rows,'provenance':'authored'})
S='string'; N='integer'; F='number'; Q='boolean'; I='identifier'; C='categorical'; T='text'; R='numerical'
ds('scaling_timeline','Bounded target-tracking test', [('elapsed_seconds',N,R),('metric_name',S,C),('metric_value',F,R),('metric_target',F,R),('scaling_activity',S,T),('capacity',N,R),('minimum_capacity',N,R),('initial_desired_capacity',N,R),('maximum_capacity',N,R),('instance_warmup_seconds',N,R)], [[0,'CPU utilization',35,50,'Baseline',2,2,2,4,120],[60,'CPU utilization',75,50,'Increase desired capacity to 3',3,2,2,4,120],[120,'CPU utilization',80,50,'Instance warmup in progress',3,2,2,4,120],[240,'CPU utilization',70,50,'Increase desired capacity to 4',4,2,2,4,120],[360,'CPU utilization',65,50,'At configured maximum',4,2,2,4,120],[480,'CPU utilization',45,50,'Bounded test ends',4,2,2,4,120]], 'Time is in seconds; CPU metric and target are percentages. These values and settings are fictional approved test inputs and observations, not a claimed prediction of AWS timing. Capacity remains within the configured bounds.')
ds('retention_preview','ECR lifecycle preview and needed versions',[('repository',S,I),('digest',S,I),('tags',S,T),('age_days',N,R),('age_threshold_days',N,R),('count_rank_newest_first',N,R),('count_limit',N,R),('age_eligible',Q,C),('count_eligible',Q,C),('deployed',Q,C),('still_needed',Q,C),('previewed_expiry',Q,C),('rulePriority',N,R),('selection',S,T),('action',S,C)], [['harbor-repository','sha256:'+format(i,'064x'),tag,age,30,rank,3,age>30,rank>3,deployed,needed,age>30,1,'Tagged archive images older than 30 days','expire'] for i,tag,age,rank,deployed,needed in [(1,'archive-release-a',45,4,True,True),(2,'archive-release-b',40,3,False,False),(3,'archive-release-c',10,2,False,True),(4,'archive-release-d',2,1,True,True)]], 'The digests are synthetic labels generated from authored row numbers, not hashes of real images. Age and count eligibility are separate comparison columns; this preview uses the stated age selection. A deployed, still-needed image overlaps the preview and must be excluded before application. No policy is applied.')
ds('command_invocations','Approved targets and Systems Manager invocation evidence',[('command_id',S,I),('document',S,I),('parameters',S,T),('parent_status',S,C),('approved_target_id',S,I),('invocation_target_id',S,I),('invocation_status',S,C),('invocation_output',S,T)], [['cmd-harbor-review','supplied-inspection-document','supplied read-only inspection parameters','Incomplete','node-a','node-a','Success','Supplied inspection completed'],['cmd-harbor-review','supplied-inspection-document','supplied read-only inspection parameters','Incomplete','node-b','node-b','Success','Supplied inspection completed'],['cmd-harbor-review','supplied-inspection-document','supplied read-only inspection parameters','Incomplete','node-c','node-c','Failed','Supplied inspection failed'],['cmd-harbor-review','supplied-inspection-document','supplied read-only inspection parameters','Incomplete','node-d',None,'Missing','No invocation record for approved node'],['cmd-harbor-review','supplied-inspection-document','supplied read-only inspection parameters','Incomplete',None,'node-x','Success','Supplied inspection completed on unintended node']], 'Null approved or actual IDs indicate no corresponding approval or invocation, not corrupt data. Two approved invocations succeed and one fails as in the teaching example; additional missing and unintended cases expose scope discrepancies. Document and parameters are excerpt labels, never executable commands.')
ds('repository_access_tests','Publisher, consumer and unapproved repository tests',[('principal',S,I),('approved_role',S,C),('repository',S,I),('repository_grant',S,T),('identity_authentication_permission',S,T),('test_operation',S,C),('expected_result',S,C),('observed_result',S,C)], [['harbor-publisher','publisher','harbor-repository','Approved push operations','ecr:GetAuthorizationToken','push','Allowed','Allowed'],['harbor-consumer','consumer','harbor-repository','Approved pull operations','ecr:GetAuthorizationToken','pull','Allowed','Allowed'],['harbor-unapproved','unapproved','harbor-repository','No repository grant','ecr:GetAuthorizationToken','pull','Denied','Denied']], 'Grants are supplied policy summaries, not invented lists of action-to-resource support rules. Authentication permission is kept separate from repository access.')
ds('log_access_tests','Scoped log-reader policy and test results',[('principal',S,I),('approved_reader',Q,C),('action',S,T),('resource_scope',S,T),('policy_evidence',S,T),('expected_result',S,C),('observed_result',S,C)], [['harbor-reader',True,'supplied resource-scoped read operation','supplied harbor log-group resource','Required read grant; unnecessary broader grants removed','Allowed','Allowed'],['harbor-unapproved',False,'supplied resource-scoped read operation','supplied harbor log-group resource','No reader grant','Denied','Denied'],['harbor-reader',True,'supplied read operation requiring resource scope *','*','Required scope retained for this supplied operation','Allowed','Allowed'],['harbor-unapproved',False,'supplied read operation requiring resource scope *','*','No reader grant','Denied','Denied']], 'Operation labels deliberately avoid inventing action-to-resource compatibility rules absent from the glossary. These are reader tests, not log-collector write evidence.')
ds('reviewed_plan_comparison','Saved Terraform plan versus created EC2 instance',[('plan_file',S,I),('approved_plan',Q,C),('setting',S,C),('planned_value',S,T),('actual_value',S,T),('instance_id',S,I),('apply_command',S,T),('apply_outcome',S,T)], [['harbor-approved.plan',True,'AMI','supplied-ami-a','supplied-ami-a','instance-harbor-a','terraform apply harbor-approved.plan','Completed'],['harbor-approved.plan',True,'instance type','supplied-instance-type','supplied-instance-type','instance-harbor-a','terraform apply harbor-approved.plan','Completed'],['harbor-approved.plan',True,'placement','supplied-placement-a','supplied-placement-a','instance-harbor-a','terraform apply harbor-approved.plan','Completed']], 'Labels stand for supplied fictional settings, not real AMI or instance identifiers. Apply outcome and resource identity are separately retained from setting comparisons.')
(B/'scenario_asset_registry.json').write_text(json.dumps(reg,indent=2)+'\n')
code='''import pandas as pd
import matplotlib.pyplot as plt
d = pd.read_csv("scaling_timeline.csv")
fig, (metric, capacity) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
metric.plot(d.elapsed_seconds, d.metric_value, marker="o", label="Observed CPU utilization")
metric.plot(d.elapsed_seconds, d.metric_target, linestyle="--", label="Approved target")
metric.set_ylabel("CPU utilization (%)")
metric.set_ylim(0, 100)
metric.legend(loc="lower left")
metric.set_title("Harbor bounded target-tracking test (authored evidence)")
capacity.step(d.elapsed_seconds, d.capacity, where="post", label="Resulting capacity")
capacity.plot(d.elapsed_seconds, d.minimum_capacity, linestyle=":", label="Minimum")
capacity.plot(d.elapsed_seconds, d.maximum_capacity, linestyle="--", label="Maximum")
capacity.set_ylim(1, 5.8)
capacity.set_yticks(sorted(d.capacity.unique()))
capacity.set_ylabel("Instances")
capacity.set_xlabel("Elapsed seconds")
capacity.legend(loc="upper left")
for row in d.itertuples():
    capacity.annotate(row.scaling_activity, (row.elapsed_seconds, row.capacity), xytext=(0, -30 if row.Index % 2 == 0 else 15), textcoords="offset points", ha="center", fontsize=7, rotation=15)
fig.text(0.5, 0.01, "Initial desired: " + str(d.initial_desired_capacity.iloc[0]) + "; warmup: " + str(d.instance_warmup_seconds.iloc[0]) + " seconds. No cloud resources run.", ha="center")
fig.tight_layout(rect=(0, 0.04, 1, 1))
'''
plots={'plots':[{'asset_id':'img.scaling_timeline','scenario_id':sc,'title':'Bounded scaling metric, activity and capacity timeline','alt_text':'An authored bounded-test timeline pairs CPU utilization and its target with scaling activities and resulting instance capacity. Capacity reaches but does not exceed the maximum while the metric remains above target. Minimum, initial desired capacity and instance warmup are shown.','datasets':[{'asset_id':'ds.scaling_timeline','mount_path':'scaling_timeline.csv'}],'code':code}]}
(B/'working/plots.json').write_text(json.dumps(plots,indent=2)+'\n')
# Mistakes-to-avoid checks for this registry: no variants or duplicate issue occurrences are authored.
for a in reg['assets']:
    assert all(len(r)==len(a['columns']) for r in a['rows'])
    for c in a['columns']:
        assert not (c['semantic_role']=='numerical' and c['type'] not in ('integer','number'))
    assert not a.get('variants')
assert all(t in source for t in vocab)
assert len(g['bundles'])==14
assert len({a['asset_id'] for a in reg['assets']})==len(reg['assets'])
print('Checklist passed: row widths, roles, vocabulary source, complete concept scan, no undeclared variants/issues, unique IDs.')
print('Datasets:',len(reg['assets']),'Rows:',sum(len(a['rows']) for a in reg['assets']),'Concepts:',len(g['bundles']))
