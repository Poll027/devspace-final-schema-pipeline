import json, re
from pathlib import Path
B = Path('batches/final_batch_aws_devops.region.02_2')
g = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
SID = 'scenario.approved_sandbox_operations'
# Mine the literal vocabulary in teaching blocks and anchors; only retain terms actually present.
texts = '\n'.join(t['content'] for b in g['bundles'] for t in b['teaching_blocks']) + '\n' + '\n'.join(json.dumps(b[k]) for b in g['bundles'] for k in ('practice_anchor','visual_anchor','assessment_anchors'))
candidates = ['operator group','IAM Identity Center','permission set','AWS account','sandbox user','SSO profile','aws configure sso','aws sso login --profile NAME','long-lived IAM user keys','TCP','443','approved source range','security-group ID','Amazon-provided DNS','instance metadata','EC2','Terraform','HCL','hashicorp/aws','APPROVED_VERSION','aws_instance','NAME','ami','instance_type','subnet_id','SUPPLIED_AMI','SUPPLIED_INSTANCE_TYPE','SUPPLIED_SUBNET_ID','terraform init','terraform plan','terraform apply','S3','bucket policy','Principal','Action','Resource','Condition','bucket ARN','object ARN','explicit deny','same-account','cross-account','Account Factory','landing zone','enrollment','organizational-unit placement','baseline checkpoints','applied controls']
vocab = [s for s in candidates if s in texts]
assets=[]
def col(name,typ='string',role='categorical',desc=None,label=False):
    c={'name':name,'type':typ,'semantic_role':role}
    if desc:c['description']=desc
    if label:c['numeric_looking_label']=True
    return c
def dataset(aid,title,cols,rows,desc):
    a={'asset_id':'ds.'+aid,'asset_kind':'dataset','scenario_id':SID,'title':title,'description':desc,'columns':cols,'rows':rows,'provenance':'authored'}
    assets.append(a)
    return a
ACCOUNT=111122223333
OTHER=444455556666
common='Authored fictional evidence for a bounded sandbox review; no AWS access or resources are provisioned. '
dataset('human_access','Approved assignment and access evidence',[
 col('case_id',role='identifier'),col('approved_group'),col('approved_user'),col('account_id','integer','identifier',label=True),col('approved_permission_set'),col('assigned_permission_set'),col('signed_in_permission_set'),col('profile_name',role='identifier'),col('profile_configuration',role='text'),col('session_workflow',role='text'),col('intended_access_test',role='text'),col('test_evidence',role='text')], [
 ['assignment_verified','sandbox-operators','sandbox-user',ACCOUNT,'SandboxObjectRead','SandboxObjectRead','SandboxObjectRead','sandbox-sso','aws configure sso','aws sso login --profile sandbox-sso','Read the approved sandbox object','Supplied test records the intended access as successful'],
 ['sign_in_only','sandbox-operators','sandbox-user',ACCOUNT,'SandboxObjectRead','SandboxObjectRead','SandboxObjectRead','sandbox-sso','aws configure sso','aws sso login --profile sandbox-sso','Read the approved sandbox object',None],
 ['assignment_mismatch','sandbox-operators','sandbox-user',ACCOUNT,'SandboxObjectRead','SandboxOtherAccess','SandboxOtherAccess','sandbox-sso','aws configure sso','aws sso login --profile sandbox-sso','Read the approved sandbox object',None]
],common+'Permission-set names and test descriptions are supplied fictional approvals, not AWS managed permission-set definitions. Missing evidence is unknown, not failure.')
dataset('security_group_traffic','Security-group connection and scope cases',[
 col('case_id',role='identifier'),col('network_interface',role='identifier'),col('protocol'),col('port','integer','categorical','Destination port identifies the service endpoint; it is not a measured quantity.',True),col('source'),col('source_form'),col('connection_kind'),col('destination'),col('inbound_rule',role='text'),col('response_direction_rule',role='text'),col('supplied_observation',role='text'),col('scope_note',role='text')],[
 ['approved_new','eni-sandbox','TCP',443,'192.0.2.0/24','approved source range','new connection','sandbox service','Allow TCP 443 from 192.0.2.0/24','No separate response-direction allow rule','Approved connection succeeds','Evaluated at associated network interface'],
 ['tracked_response','eni-sandbox','TCP',443,'sandbox service','response source','tracked response','approved client','Allow TCP 443 from 192.0.2.0/24','No separate response-direction allow rule','Response to approved connection succeeds','Stateful response; port denotes the original service endpoint'],
 ['unapproved_new','eni-sandbox','TCP',443,'198.51.100.0/24','unapproved source range','new connection','sandbox service','Allow TCP 443 from 192.0.2.0/24','No separate response-direction allow rule','New unapproved connection is not admitted','Not an explicit deny rule'],
 ['source_group','eni-sandbox','TCP',443,'sg-approved-clients','security-group ID','new connection','sandbox service','Allow TCP 443 from sg-approved-clients','No separate response-direction allow rule','Source-group reference is present','Reference does not import source group rules'],
 ['dns_scope','eni-sandbox','not assessed',None,'sandbox workload','workload','scope review','Amazon-provided DNS','Not applicable','Not applicable','No security-group filtering conclusion from this traffic','Outside security-group filtering'],
 ['metadata_scope','eni-sandbox','not assessed',None,'sandbox workload','workload','scope review','EC2 instance metadata','Not applicable','Not applicable','No security-group filtering conclusion from this traffic','Outside security-group filtering']
],common+'Documentation-only source ranges are fictional approved/unapproved inputs. Null ports in scope-review rows mean not applicable. No unrelated firewall behavior is asserted.')
version='5.0.0'; ami='ami-0123456789abcdef0'; instance_type='t3.micro'; subnet='subnet-0123456789abcdef0'
dataset('terraform_settings','Supplied, declared, planned and verified EC2 settings',[
 col('stage',role='identifier'),col('provider_source'),col('approved_provider_version'),col('provider_version_constraint',role='text'),col('resource_type'),col('resource_label',role='identifier'),col('ami',role='identifier'),col('instance_type'),col('subnet_id',role='identifier')], [
 [stage,'hashicorp/aws',version,'= '+version,'aws_instance','NAME',ami,instance_type,subnet] for stage in ['supplied_specification','completed_declaration','inspected_plan','verified_instance']
],common+'The exact version and instance identifiers are fictional supplied exercise values, not availability or compatibility claims. The four rows support comparison of one intended instance; they are not execution logs.')
dataset('terraform_review','Terraform review evidence stages',[
 col('stage',role='identifier'),col('command',role='text'),col('evidence_purpose',role='text'),col('supplied_review_evidence',role='text')],[
 ['initialization','terraform init','Install the approved provider','Reviewer records initialization as successful'],
 ['planning','terraform plan','Inspect intended changes before approved apply','Reviewer records one intended EC2 instance matching the specification'],
 ['approved_apply','terraform apply','Create the intended instance using the approved step','Reviewer records approved creation as complete'],
 ['verification','Inspect resulting instance settings','Compare resulting AMI, instance type and subnet ID','Reviewer records settings matching the specification']
],common+'Authored review notes, not purported CLI stdout or evidence of a real deployment.')
bucket='arn:aws:s3:::sandbox-review-bucket'
obj=bucket+'/approved-object.txt'
principal='arn:aws:iam::'+str(ACCOUNT)+':role/sandbox-reader'
external='arn:aws:iam::'+str(OTHER)+':role/sandbox-reader'
condition={'Bool':{'aws:SecureTransport':'true'}}
policy=dataset('resource_policy','Supplied S3 resource-policy statement fields',[
 col('statement_id',role='identifier'),col('Effect'),col('Principal',role='text'),col('Action'),col('Resource',role='text'),col('Condition',role='text')],[
 ['object_read_allow','Allow',json.dumps({'AWS':[principal,external]}),'s3:GetObject',obj,json.dumps(condition,sort_keys=True)],
 ['object_read_deny','Deny',json.dumps({'AWS':[principal,external]}),'s3:GetObject',obj,json.dumps({'Bool':{'aws:SecureTransport':'false'}},sort_keys=True)]
],common+'One fictional bucket policy. Each row is a statement; principal and condition cells are JSON. Compare the supplied boolean request value to the stated condition; this does not introduce a general condition-operator lesson.')
dataset('resource_requests','Object requests and contributed-permission evidence',[
 col('request_id',role='identifier'),col('caller_account','integer','identifier',label=True),col('resource_account','integer','identifier',label=True),col('Principal',role='text'),col('Action'),col('Resource',role='text'),col('bucket_arn',role='text'),col('condition_key'),col('condition_value','boolean','categorical'),col('identity_allow','boolean','categorical'),col('other_applicable_explicit_deny','boolean','categorical')],[
 ['same_account_allow',ACCOUNT,ACCOUNT,principal,'s3:GetObject',obj,bucket,'aws:SecureTransport',True,True,False],
 ['same_account_contributed_resource_allow',ACCOUNT,ACCOUNT,principal,'s3:GetObject',obj,bucket,'aws:SecureTransport',True,False,False],
 ['explicit_deny',ACCOUNT,ACCOUNT,principal,'s3:GetObject',obj,bucket,'aws:SecureTransport',False,True,False],
 ['cross_account_both_sides',OTHER,ACCOUNT,external,'s3:GetObject',obj,bucket,'aws:SecureTransport',True,True,False],
 ['cross_account_missing_identity_allow',OTHER,ACCOUNT,external,'s3:GetObject',obj,bucket,'aws:SecureTransport',True,False,False],
 ['unapproved_caller',ACCOUNT,ACCOUNT,'arn:aws:iam::'+str(ACCOUNT)+':role/unapproved-reader','s3:GetObject',obj,bucket,'aws:SecureTransport',True,False,False],
 ['bucket_scope_mismatch',ACCOUNT,ACCOUNT,principal,'s3:GetObject',bucket,bucket,'aws:SecureTransport',True,False,False]
],common+'Inputs only, not an answer key. No additional policies or special cross-account exceptions are part of these supplied cases. The bucket-scope row intentionally supplies a nonmatching target for the object-operation request.')
dataset('onboarding_checkpoints','Account onboarding expectations and evidence',[
 col('case_id',role='identifier'),col('account_id','integer','identifier',label=True),col('approved_account_name'),col('checkpoint',role='identifier'),col('supplied_expectation',role='text'),col('observed_evidence',role='text')],[
 ['onboarding_review',ACCOUNT,'sandbox-review','account_inputs','Use supplied account name sandbox-review and approved target OU sandbox-ou','Reviewer records approved inputs used'],
 ['onboarding_review',ACCOUNT,'sandbox-review','creation','Account creation completed','Reviewer records account creation complete'],
 ['onboarding_review',ACCOUNT,'sandbox-review','enrollment','Enrollment in the supplied governed landing zone','Reviewer records enrollment confirmed'],
 ['onboarding_review',ACCOUNT,'sandbox-review','organizational_unit','Placement in sandbox-ou','Reviewer records placement in sandbox-ou'],
 ['onboarding_review',ACCOUNT,'sandbox-review','supplied_baseline_checkpoint_a','Evidence of the applied control for supplied checkpoint A','Reviewer records supporting applied-control evidence for supplied checkpoint A'],
 ['onboarding_review',ACCOUNT,'sandbox-review','supplied_baseline_checkpoint_b','Evidence of the applied control for supplied checkpoint B',None]
],common+'Baseline checkpoints A and B are supplied opaque review labels: no control design or particular AWS control is invented. Missing checkpoint evidence is unverified even though account creation is complete.')
# No path-specific profile exists in this pack. Preserve the sole live_code anchor as a
# bounded static workspace; do not provision the runtime, credentials or any cloud resource.
tf_bundle=next(b for b in g['bundles'] if b['practice_anchor']['type']=='live_code')
provider_block=re.search(r'```hcl\n(.*?)\n```',tf_bundle['teaching_blocks'][1]['content'],re.S).group(1)
resource_template='resource "aws_instance" "NAME" {\n  ami = "SUPPLIED_AMI"\n  instance_type = "SUPPLIED_INSTANCE_TYPE"\n  subnet_id = "SUPPLIED_SUBNET_ID"\n}\n'
assets.append({'asset_id':'code.terraform_instance','asset_kind':'code_workspace','scenario_id':SID,'title':'Bounded Terraform declaration starter (no infrastructure provisioned)','runtime':'terraform','files':[
 {'path':'main.tf','content':provider_block+'\n\n'+resource_template},
 {'path':'specification.json','content':json.dumps({'approved_provider_version':version,'ami':ami,'instance_type':instance_type,'subnet_id':subnet},indent=2)+'\n'},
 {'path':'README.txt','content':'Static authored exercise files only. No runtime, AWS access, host binding or resource is provisioned. Use the supplied specification to replace the placeholders in main.tf. The supplied review datasets separate initialization, planning, approved apply and verification; they are not command output. The native EC2 foundation is a prerequisite.\n'}]})
registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':g['batch_id'],'scenarios':[{'scenario_id':SID,'name':'Approved sandbox operations review','summary':'A fictional operator group reviews one sandbox account: approved human access, TCP 443 ingress, a bounded Terraform instance declaration, S3 object permission requests and Account Factory onboarding evidence. All identifiers, approvals and review records are authored fixtures, not facts about an existing AWS environment.','domain':'AWS sandbox identity, network, infrastructure and governance operations','glossary_example_vocab':vocab}],'assets':assets}
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
# Stage mistakes-to-avoid checklist: all structural assertions use the built data.
assert len({a['asset_id'] for a in assets})==len(assets)
for a in assets:
 if a['asset_kind']!='dataset':continue
 assert len({c['name'] for c in a['columns']})==len(a['columns'])
 for row in a['rows']:
  assert len(row)==len(a['columns']),a['asset_id']
  for c,v in zip(a['columns'],row):
   if v is None:continue
   assert (c['type']=='string' and isinstance(v,str)) or (c['type']=='integer' and type(v)==int) or (c['type']=='boolean' and type(v)==bool)
 for c in a['columns']:
  assert c['semantic_role']!='numerical' or c['type'] in ('integer','number')
  assert not c.get('numeric_looking_label') or (c['type'] in ('integer','number') and c['semantic_role'] in ('identifier','categorical'))
assert all(v in texts for v in vocab)
assert all(not a.get('variants') for a in assets) # No messy variants or duplicate occurrences to resolve.
checklist={'concepts_covered':[b['context']['concept_id'] for b in g['bundles']],'scenario_count':len(registry['scenarios']),'asset_count':len(assets),'dataset_count':sum(a['asset_kind']=='dataset' for a in assets),'row_count':sum(len(a.get('rows',[])) for a in assets),'checks':{'row_width_and_types':'passed','semantic_roles':'passed; ports and account numbers are labels, versions are categorical, evidence is text','planted_issue_predicates_and_duplicate_occurrence':'not applicable; no variants','scope_support':'all five concepts have reusable supplied evidence; S3 statements and requests share generated identifiers','glossary_vocabulary':'literal-match checked; no glossary-named concrete cities or columns omitted','unambiguous_roles':'endpoint port categorical; account identifiers numeric-looking; null means no supporting evidence or not applicable as described','plot_inventory':'no anchor or teaching block depends on a rendered plot'},'uncertainty':'aws_devops_engineer.json is absent; fallback _default.json has no inspect-and-judge overrides. The Terraform live_code anchor is represented by static starter files, with no runtime or AWS resources provisioned.'}
(B/'working/scenario_registry_checklist.json').write_text(json.dumps(checklist,indent=2)+'\n')
print(json.dumps({k:checklist[k] for k in ['scenario_count','asset_count','dataset_count','row_count']},indent=2))
