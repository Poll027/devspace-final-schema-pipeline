import json, re, hashlib
from pathlib import Path
B = Path('batches/final_batch_aws_devops.region.04_1')
bundle = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/'+bundle['path_id']+'.json').read_text())
assert all(b['context']['concept_id'] in profile['practice_type_by_concept'] for b in bundle['bundles'])
# Mine vocabulary exclusively from the scoped teaching blocks and anchors.
texts=[]
for b in bundle['bundles']:
    texts.extend(t['content'] for t in b['teaching_blocks'])
    texts.extend([json.dumps(b['visual_anchor']), json.dumps(b['practice_anchor']), json.dumps(b['assessment_anchors'])])
text='\n'.join(texts)
candidates=['CodeBuild','buildspec','YAML','version: 0.2','install','pre_build','build','post_build','commands','artifacts.files','base-directory','CodeDeploy','appspec.yml','EC2','AppSpec','deployment group','revision','service role','agent','lifecycle hooks','Auto Scaling','target tracking','warmup','minimum','desired','maximum','ECR','publisher','consumer','push','pull','ecr:GetAuthorizationToken','rulePriority','selection','action','digest','tag status','count','age','lifecycle preview','Application Load Balancer','ALB','listener','target group','health-check path','success codes','fails open','CloudWatch','put-retention-policy','retentionInDays','72 hours','RDS','snapshot','available','endpoint','recovery marker','reader','resource scope *','IAM','ECS','containerDefinitions','name','image','portMappings','cpu','memory','launch type','principal','operation','resource','context','identity policy','resource policies','session policies','permissions boundaries','organization policies','explicit deny','missing applicable allow','unsatisfied condition','Terraform','terraform show PLAN_FILE','terraform apply PLAN_FILE','AMI','instance type','placement','Systems Manager','Run Command','send-command','--instance-ids','--targets','command ID','status','output','terraform init -backend=false','terraform validate','terraform fmt -check','terraform fmt','GitHub Actions','aws_instance']
vocab=[v for v in candidates if v in text]
S='scen.delivery_operations'
assets=[]
def column(name, typ='string', role='text', unit=None, description=None):
    c={'name':name,'type':typ,'semantic_role':role}
    if unit: c['unit']=unit
    if description: c['description']=description
    return c

def ds(asset_id,title,cols,rows,description):
    a={'asset_id':asset_id,'asset_kind':'dataset','scenario_id':S,'title':title,'description':'Fictional authored read-only evidence; no AWS resources or runtime are provisioned. '+description,'columns':cols,'rows':rows,'provenance':'authored'}
    assets.append(a)
    return a

def ident(label, prefix, length=17):
    return prefix+hashlib.sha256(('fictional sandbox '+label).encode()).hexdigest()[:length]
node_ids=[ident('node '+str(n),'i-') for n in range(1,5)]
image_digests=['sha256:'+hashlib.sha256(('fictional application release '+str(n)).encode()).hexdigest() for n in range(1,6)]
C=column
scaling=ds('ds.scaling_timeline','Bounded Auto Scaling test',[
 C('elapsed_seconds','integer','numerical','seconds'),C('metric_name',role='categorical'),C('metric_value','number','numerical','percent'),C('metric_target','number','numerical','percent'),C('scaling_activity'),C('resulting_capacity','integer','numerical','instances'),C('minimum_capacity','integer','numerical','instances'),C('desired_capacity_at_start','integer','numerical','instances'),C('maximum_capacity','integer','numerical','instances'),C('instance_warmup_seconds','integer','numerical','seconds')],
 [[t,'CPU utilization',m,50,activity,cap,1,2,4,120] for t,m,activity,cap in [
 (0,35,'No scaling activity',2),(60,70,'Scale-out activity: add one instance',3),(120,78,'New instance warming up',3),(180,72,'Scale-out activity: add one instance',4),(240,68,'New instance warming up',4),(300,63,'At configured maximum',4),(360,54,'At configured maximum',4)]],
 'The supplied fictional test uses a 50 percent CPU target, 120-second warmup and capacities 1/2/4. Observations are an authored timeline, not a promise of exact AWS response times. Desired capacity at start is a baseline, not a claim that desired capacity remains fixed during scaling.')
ret=ds('ds.retention_preview','Image retention preview and needed versions',[
 C('digest',role='identifier'),C('tags'),C('tag_status',role='categorical'),C('age_days','integer','numerical','days'),C('age_threshold_days','integer','numerical','days'),C('rulePriority','integer','numerical'),C('selection'),C('action',role='categorical'),C('eligible','boolean','categorical'),C('deployed','boolean','categorical'),C('still_needed','boolean','categorical'),C('previewed_expiry','boolean','categorical')],
 [[digest,tags,status,age,30,1,'Untagged images older than 30 days','expire',status=='untagged' and age>30,deployed,needed,status=='untagged' and age>30] for digest,tags,status,age,deployed,needed in [
 (image_digests[0],'release-current','tagged',45,True,True),(image_digests[1],'release-rollback','tagged',60,False,True),(image_digests[2],'','untagged',40,False,False),(image_digests[3],'','untagged',10,False,False),(image_digests[4],'release-candidate','tagged',5,False,True)]],
 'One supplied age-based rule selects untagged images older than 30 days. Tags are protected by exclusion from this selection, not by deployment immunity. The unsafe variant removes the rollback tag; preview must expose its overlap with a still-needed digest.')
def setop(where,col,val): return {'op':'set_cell','where':where,'occurrence':0,'column':col,'value':val}
def issue(i,where,col,value,description): return {'issue_id':i,'kind':'other','locations':[{'where':where,'occurrence':0,'column':col}],'description':description,'rule':{'column':col,'op':'eq','value':value}}
w={'digest':image_digests[1]}
ret['variants']=[{'variant_id':'var.retention_unsafe','derived_from':ret['asset_id'],'purpose':'Preview exposes a rollback image made eligible by loss of its tag. Exclude the still-needed digest before applying the policy.','ops':[setop(w,'tags',''),setop(w,'tag_status','untagged'),setop(w,'eligible',True),setop(w,'previewed_expiry',True)],'planted_issues':[issue('issue.needed_image_expiry',w,'previewed_expiry',True,'The preview expires this exact still-needed rollback digest. Deployment or rollback need does not itself override lifecycle selection.')]}]
ssm=ds('ds.command_invocations','Scoped command invocation evidence',[
 C('command_id',role='identifier'),C('document_name',role='identifier'),C('document_parameters'),C('approved_target_set'),C('invocation_target',role='identifier'),C('approved_target','boolean','categorical'),C('parent_status',role='categorical'),C('invocation_status',role='categorical'),C('invocation_output')],
 [[ident('command 1','cmd-'), 'SuppliedInspectionDocument','Mode=inspect',', '.join(node_ids[:3]),n,True,'Success',status,out] for n,status,out in zip(node_ids[:3],['Success','Success','Failed'],['Supplied inspection completed','Supplied inspection completed','Supplied inspection failed; retain node-specific output'])],
 'Three approved nodes share a command ID: two invocations succeed and one fails, matching the glossary example. Parent status is only the supplied summary. SuppliedInspectionDocument is a fictional prepared document name, not an executable asset.')
w={'invocation_target':node_ids[2]}
ssm['variants']=[{'variant_id':'var.command_scope_discrepancy','derived_from':ssm['asset_id'],'purpose':'The third invocation is on an unintended node while the third approved node has no result. A successful out-of-scope invocation does not repair the missing approved invocation.','ops':[setop(w,'invocation_target',node_ids[3]),setop({'invocation_target':node_ids[3]},'approved_target',False),setop({'invocation_target':node_ids[3]},'invocation_status','Success'),setop({'invocation_target':node_ids[3]},'invocation_output','Supplied inspection completed on an unintended node')],'planted_issues':[issue('issue.unapproved_invocation',{'invocation_target':node_ids[3]},'approved_target',False,'Invocation target is outside the unchanged approved target set; the original third approved target is missing from invocation results.')]}]
# Numeric-looking network ports are labels, unlike CPU/memory quantities.
port=C('containerPort','integer','categorical',description='TCP endpoint label, not a measured quantity.');port['numeric_looking_label']=True
hostport=C('hostPort','integer','categorical',description='TCP endpoint label, not a measured quantity.');hostport['numeric_looking_label']=True
spec={'name':'delivery-api','image':'delivery-api@'+image_digests[0],'containerPort':8080,'hostPort':8080,'cpu':256,'memory':512,'launch_type':'EC2','cluster':'delivery-cluster','network_configuration':'supplied prepared network'}
ecscols=[C('evidence_stage',role='categorical'),C('task_definition',role='identifier'),C('task_id',role='identifier'),C('status',role='categorical'),C('name',role='identifier'),C('image',role='identifier'),port,hostport,C('cpu','integer','numerical','CPU units'),C('memory','integer','numerical','MiB'),C('launch_type',role='categorical'),C('cluster',role='identifier'),C('network_configuration')]
ecsrows=[]
for stage,definition,task,status in [('supplied specification','delivery-task:1','not run','specified'),('registered definition','delivery-task:1','not run','registered'),('observed task','delivery-task:1','delivery-task-run-1','RUNNING')]:
 ecsrows.append([stage,definition,task,status]+list(spec.values()))
ds('ds.ecs_configuration_evidence','Supplied, registered and observed ECS settings',ecscols,ecsrows,'Supplied settings and runtime evidence are recorded separately. Repeated settings are copied by script from the authored specification. The matching RUNNING row is fictional inspection evidence, not a learner-executed task.')
plan={'AMI':ident('application AMI','ami-'),'instance_type':'t3.micro','placement':'sandbox-zone-a'}
ds('ds.reviewed_plan_comparison','Approved plan and resulting EC2 comparison',[
 C('evidence_stage',role='categorical'),C('plan_file',role='identifier'),C('approved','boolean','categorical'),C('instance_id',role='identifier'),C('AMI',role='identifier'),C('instance_type',role='categorical'),C('placement',role='categorical'),C('execution_command'),C('apply_outcome')],
 [[stage,'PLAN_FILE',True,instance]+list(plan.values())+[cmd,outcome] for stage,instance,cmd,outcome in [
 ('reviewed plan','not yet created','terraform show PLAN_FILE','not executed'),('resulting resource',node_ids[0],'terraform apply PLAN_FILE','Apply complete: one resource added')]],
 'PLAN_FILE is the glossary\'s supplied approved saved-plan name. The actual settings are copied from the authored plan. sandbox-zone-a is fictional supplied placement; this is not a real EC2 inventory or provisioning record.')
ds('ds.repository_access_tests','Publisher, consumer and unapproved access tests',[
 C('principal',role='identifier'),C('approved_role',role='categorical'),C('repository',role='identifier'),C('operation',role='categorical'),C('repository_grant'),C('identity_authentication_action'),C('identity_authentication_allowed','boolean','categorical'),C('expected_result',role='categorical'),C('observed_result',role='categorical')],
 [[p,role,'delivery-api',operation,grant,'ecr:GetAuthorizationToken',auth,expected,expected] for p,role,operation,grant,auth,expected in [
 ('delivery-publisher','publisher','push','Supplied image-layer upload and image-publish operations',True,'allowed'),('delivery-consumer','consumer','pull','Supplied image-pull operations',True,'allowed'),('unapproved-reader','unapproved','pull','No repository grant',True,'denied')]],
 'The unapproved principal can authenticate in this supplied case but has no repository pull grant. Authentication and repository authorization are separate. Expected and observed outcomes are authored case evidence, copied once rather than repeated by hand.')
ds('ds.log_access_tests','Scoped log reader test evidence',[
 C('principal',role='identifier'),C('approved_reader','boolean','categorical'),C('read_operation'),C('resource_scope'),C('scope_reason'),C('expected_result',role='categorical'),C('observed_result',role='categorical')],
 [[principal,approved,operation,scope,reason,result,result] for principal,approved,result in [('delivery-log-reader',True,'allowed'),('unapproved-reader',False,'denied')] for operation,scope,reason in [
 ('supplied resource-scoped read operation','supplied delivery log-group resource','Supplied operation supports resource scoping'),('supplied wildcard-required read operation','*','Supplied operation requires resource scope *')]],
 'Operations intentionally keep the supplied-operation vocabulary: the glossary does not name particular Logs API actions. The table distinguishes intended-resource reads from the supplied operation that requires wildcard resource scope, without inventing service-specific scope facts.')
registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':bundle['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':S,'name':'Delivery application operations review','summary':'A fictional delivery application team reviews supplied build, deployment and operations evidence in an approved sandbox case. The application is delivery-api; publisher, consumer and log-reader roles are delivery-publisher, delivery-consumer and delivery-log-reader. All records and identifiers are authored, not real AWS observations. Learners inspect excerpts, configurations and read-only tables; no shell, cloud service, credentials or resources are provisioned. CodeBuild, CodeDeploy, load-balancer, log-retention, database-restore, IAM-denial and validation examples can be carried as plain-text code/config/log evidence in interactions; their scaffolding requires no executable assets.','domain':'AWS delivery and operations','glossary_example_vocab':vocab}],'assets':assets}
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
plot_code='''import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("scaling_timeline.csv")
fig, (metric_ax, capacity_ax) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
metric_ax.plot(df["elapsed_seconds"], df["metric_value"], marker="o", label="Observed CPU utilization")
metric_ax.plot(df["elapsed_seconds"], df["metric_target"], linestyle="--", label="Approved metric target")
metric_ax.set_ylabel("CPU utilization (%)")
metric_ax.legend(loc="upper left")
metric_ax.grid(alpha=0.3)
capacity_ax.step(df["elapsed_seconds"], df["resulting_capacity"], where="post", marker="o", label="Resulting capacity")
capacity_ax.axhline(df["maximum_capacity"].iloc[0], color="red", linestyle="--", label="Maximum capacity")
capacity_ax.axhline(df["minimum_capacity"].iloc[0], color="gray", linestyle=":", label="Minimum capacity")
capacity_ax.axhline(df["desired_capacity_at_start"].iloc[0], color="green", linestyle=":", label="Desired capacity at start")
for i in [1, 3, 5]:
    r = df.iloc[i]
    capacity_ax.annotate(r["scaling_activity"], (r["elapsed_seconds"], r["resulting_capacity"]), xytext=(7, -32 if i == 3 else -20), textcoords="offset points", fontsize=8)
capacity_ax.set_xlabel("Elapsed time in bounded test (seconds)")
capacity_ax.set_ylabel("Capacity (instances)")
capacity_ax.set_yticks(range(int(df["minimum_capacity"].iloc[0]), int(df["maximum_capacity"].iloc[0]) + 1))
capacity_ax.set_ylim(0.5, df["maximum_capacity"].iloc[0] + 1.4)
capacity_ax.legend(loc="upper left", fontsize=8)
capacity_ax.grid(alpha=0.3)
fig.suptitle("Fictional bounded Auto Scaling test")
fig.text(0.5, 0.02, "Instance warmup: " + str(df["instance_warmup_seconds"].iloc[0]) + " seconds; desired capacity is the starting baseline.", ha="center", fontsize=9)
fig.tight_layout(rect=(0, 0.04, 1, 0.95))
'''
plots={'plots':[{'asset_id':'img.scaling_bounded_timeline','scenario_id':S,'title':'Metric target, activities and bounded capacity','alt_text':'Two aligned panels show the fictional bounded-test timeline. CPU utilization rises above the approved target while capacity increases from its starting desired capacity to the configured maximum. CPU remains above target at the maximum; capacity does not exceed that bound. The lower panel labels scale-out activities and the maximum-capacity observation, minimum and maximum bounds and the starting desired capacity; the footer states the supplied instance warmup. These are authored observations, not exact response-time guarantees.','datasets':[{'asset_id':scaling['asset_id'],'mount_path':'scaling_timeline.csv'}],'code':plot_code}]}
(B/'working/plots.json').write_text(json.dumps(plots,indent=2)+'\n')
print('Wrote',len(assets),'datasets;',sum(len(a['rows']) for a in assets),'base rows;',len(vocab),'mined vocabulary entries; scope',len(bundle['bundles']),'concepts')
