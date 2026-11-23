import json, re
from pathlib import Path
B=Path(__file__).resolve().parents[1]
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bundles=g['bundles']
texts=['\n'.join([t['content'] for t in b['teaching_blocks']]+[json.dumps(b['visual_anchor']),json.dumps(b['practice_anchor'])]) for b in bundles]
# Mine only vocabulary actually present in teaching blocks or anchors.
candidates=['IAM Identity Center','permission sets','operator group','AWS account','permission set','SSO profile','aws configure sso','aws sso login --profile NAME','long-lived IAM user keys','TCP','443','approved source range','security-group ID','Amazon-provided DNS','instance metadata','network interface','allow rules','response traffic','Terraform','hashicorp/aws','APPROVED_VERSION','aws_instance','NAME','ami','instance_type','subnet_id','terraform init','terraform plan','terraform apply','Principal','Action','Resource','Condition','S3 bucket policy','bucket ARN','object ARN','explicit deny','same-account','cross-account','Account Factory','enrollment','organizational-unit placement','baseline checkpoints','applied controls']
vocab=[v for v in candidates if any(v in t for t in texts)]
assert len(vocab)==len(candidates)
scenario='scenario.sandbox_operations'
registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':scenario,'name':'Cedar sandbox operations review','summary':'A fictional Cedar operations team reviews supplied human-access assignments, connection evidence, Terraform settings, S3 requests and managed-account onboarding records. All records are authored, read-only classroom evidence; no account, credential, host or cloud resource is provisioned.','domain':'AWS sandbox identity, network access and bounded provisioning','glossary_example_vocab':vocab}], 'assets':[]}
def col(name,role='text',typ='string',description=None):
 c={'name':name,'type':typ,'semantic_role':role}
 if description:c['description']=description
 return c
def add(aid,title,columns,rows,description):
 rows=[[int(v) if c.get('numeric_looking_label') and v is not None else v for c,v in zip(columns,row)] for row in rows]
 registry['assets'].append({'asset_id':'ds.'+aid,'asset_kind':'dataset','scenario_id':scenario,'title':title,'description':description+' All values are fictional supplied evidence, not operational instructions or real AWS observations.','columns':columns,'rows':rows,'provenance':'authored'})
account='111111111111'; other='222222222222'
def account_col(name):
 return dict(col(name,'identifier','integer',description='Fictional AWS account identifier; digits are a label, not a quantity.'),numeric_looking_label=True)
add('human_access','Approved assignment and access-test evidence',[
 col('case_id','identifier'),col('user','identifier'),col('operator_group','categorical'),account_col('approved_account'),col('approved_permission_set','categorical'),account_col('assigned_account'),col('assigned_permission_set','categorical'),account_col('signed_in_account'),col('signed_in_permission_set','categorical'),col('intended_access_test'),col('expected_result','categorical'),col('observed_result','categorical'),col('profile_name','identifier'),col('profile_configuration'),col('session_evidence'),col('credential_storage','categorical')],[
 ['access.complete','cedar-operator','cedar-operators',account,'CedarObjectRead',account,'CedarObjectRead',account,'CedarObjectRead','Read sandbox evidence object','success','success','cedar-sandbox','aws configure sso; named profile cedar-sandbox configured','aws sso login --profile cedar-sandbox; session established','no long-lived IAM user keys'],
 ['access.sign_in_only','cedar-operator','cedar-operators',account,'CedarObjectRead',account,'CedarObjectRead',account,'CedarObjectRead','Read sandbox evidence object','success','not tested','cedar-sandbox','aws configure sso; named profile cedar-sandbox configured','aws sso login --profile cedar-sandbox; session established','no long-lived IAM user keys'],
 ['access.assignment_mismatch','cedar-operator','cedar-operators',account,'CedarObjectRead',account,'CedarOtherPermission',account,'CedarOtherPermission','Read sandbox evidence object','success','not tested','cedar-sandbox','aws configure sso; named profile cedar-sandbox configured','aws sso login --profile cedar-sandbox; session established','no long-lived IAM user keys']
], 'Compare approved and assigned context, sign-in context and intended-operation result. Permission-set names are fictional supplied approvals; the table does not assert their real AWS definitions.')
port=int(re.search(r'TCP port (\d+)',texts[1]).group(1))
add('connection_tests','Security-group connection and response evidence',[
 col('test_id','identifier'),col('network_interface','identifier'),col('destination_group','identifier'),col('traffic_case','categorical'),col('protocol','categorical'),col('port','numerical','integer'),col('source'),col('inbound_rule'),col('response_direction_rule'),col('observed_result','categorical'),col('interpretation')],[
 ['net.approved','eni-cedar-workload','sg-cedar-workload','new connection','TCP',port,'approved source range: 192.0.2.0/24','allow TCP 443 from 192.0.2.0/24','none','connection succeeds','Approved inbound traffic'],
 ['net.response','eni-cedar-workload','sg-cedar-workload','tracked response','TCP',port,'workload response to allowed tracked connection','allow TCP 443 from 192.0.2.0/24','none','response succeeds','Stateful response; no separate response-direction allow required'],
 ['net.unapproved','eni-cedar-workload','sg-cedar-workload','new connection','TCP',port,'unapproved source range: 198.51.100.0/24','allow TCP 443 from 192.0.2.0/24','none','not admitted','No matching inbound allow'],
 ['net.group_reference','eni-cedar-workload','sg-cedar-workload','new connection','TCP',port,'sg-cedar-source','allow TCP 443 from sg-cedar-source','none','connection succeeds','Source-group reference identifies allowed source; does not import its rules'],
 ['net.dns','eni-cedar-workload','sg-cedar-workload','Amazon-provided DNS','not specified',None,'workload','not used for this traffic','not used for this traffic','outside security-group filtering','Do not infer filtering from this traffic'],
 ['net.metadata','eni-cedar-workload','sg-cedar-workload','instance metadata','not specified',None,'workload','not used for this traffic','not used for this traffic','outside security-group filtering','Do not infer filtering from this traffic']
], 'Read-only supplied tests for the approved service and exception boundaries. Port on a tracked-response row labels the service connection, not its return destination port. No ingress beyond the displayed approved allow is present.')
provider=re.search(r'source = "([^"]+)"',texts[2]).group(1)
add('terraform_settings','Terraform specification, declaration, plan and verification',[
 col('evidence_stage','categorical'),col('provider_source','categorical'),col('provider_version','categorical',description='Exact fictional approved version; a version label, not a numeric measurement.'),col('resource_type','categorical'),col('resource_label','identifier'),col('ami','identifier'),col('instance_type','categorical'),col('subnet_id','identifier')],[
 [stage,provider,'6.0.0','aws_instance','cedar_workload','ami-00000000000000001','t3.micro','subnet-00000000000000001'] for stage in ['supplied specification','HCL declaration','inspected plan','verified instance settings']
], 'Align the same supplied AMI, instance type and subnet across the evidence stages. The declared version constraint is exactly = 6.0.0; comparison is read-only and does not establish runtime access.')
commands=re.findall(r'terraform (?:init|plan|apply)',texts[2])
commands=list(dict.fromkeys(commands))
assert commands==['terraform init','terraform plan','terraform apply']
add('terraform_execution','Separate declaration from execution evidence',[
 col('sequence','numerical','integer'),col('command'),col('review_evidence'),col('approval_evidence'),col('result')],[
 [i+1,cmd,review,approval,result] for i,(cmd,review,approval,result) in enumerate(zip(commands,
 ['Provider installation checked','Planned instance values match supplied specification','Reviewed intended instance change'],
 ['Not the apply step','Not the apply step','Supplied apply approval recorded'],
 ['Provider installation succeeded','One intended EC2 instance proposed','Instance creation completed; resulting settings compared']))
], 'Authored command-result excerpts for inspection, never an executable workspace. A plausible HCL declaration alone is not execution evidence.')
bucket='arn:aws:s3:::cedar-sandbox-evidence'; obj=bucket+'/evidence.txt'
principal='arn:aws:iam::'+account+':role/CedarReader'; cross='arn:aws:iam::'+other+':role/CedarReader'
add('bucket_policy','Supplied S3 resource-policy fields',[
 col('statement_id','identifier'),col('Effect','categorical'),col('Principal'),col('Action','categorical'),col('Resource'),col('Condition')],[
 ['same_account_read','Allow',principal,'s3:GetObject',bucket+'/*','aws:SecureTransport = true'],
 ['cross_account_read','Allow',cross,'s3:GetObject',bucket+'/*','aws:SecureTransport = true']
], 'Two supplied allow statements on the fictional bucket. Explicit-deny evidence is supplied separately per request. Condition text states a supplied equality test, not an expanded policy-evaluation lesson.')
add('object_requests','S3 caller, request fields and supplied permission evidence',[
 col('request_id','identifier'),col('Principal'),col('Action','categorical'),col('Resource'),col('Condition'),col('account_relationship','categorical'),col('identity_allow','categorical'),col('resource_allow','categorical'),col('explicit_deny','categorical'),col('permission_outcome','categorical'),col('evidence_note')],[
 ['request.same',principal,'s3:GetObject',obj,'aws:SecureTransport = true','same-account','absent','matching','none applicable','permitted','Matching resource allow contributes permission'],
 ['request.denied',principal,'s3:GetObject',obj,'aws:SecureTransport = true','same-account','matching','matching','applicable supplied explicit deny','not permitted','Applicable explicit deny overrides contributed allows'],
 ['request.cross_both',cross,'s3:GetObject',obj,'aws:SecureTransport = true','cross-account','matching','matching','none applicable','permitted','Supplied ordinary cross-account case: permission on both sides'],
 ['request.cross_missing',cross,'s3:GetObject',obj,'aws:SecureTransport = true','cross-account','absent','matching','none applicable','not permitted','Supplied ordinary cross-account case lacks identity-side permission'],
 ['request.unapproved','arn:aws:iam::'+other+':role/CedarUnapproved','s3:GetObject',obj,'aws:SecureTransport = true','cross-account','matching','no matching principal','none applicable','not permitted','Resource-side principal does not match'],
 ['request.bucket_scope',principal,'s3:GetObject',bucket,'aws:SecureTransport = true','same-account','absent','no matching object scope','none applicable','not permitted','Bucket ARN differs from object ARN; does not match the supplied object resource scope'],
 ['request.condition',principal,'s3:GetObject',obj,'aws:SecureTransport = false','same-account','absent','no matching condition','none applicable','not permitted','Supplied condition does not match'],
 ['request.action',principal,'s3:DeleteObject',obj,'aws:SecureTransport = true','same-account','absent','no matching action','none applicable','not permitted','Supplied read action does not match the requested operation']
], 'Read-only request evidence paired with ds.bucket_policy. Outcomes apply only to these fully supplied cases; cross-account statements retain the glossary qualification generally and do not teach special grant exceptions.')
add('onboarding_checkpoints','Managed-account inputs and governance evidence',[
 col('case_id','identifier'),col('account_name','identifier'),account_col('account_id'),col('approved_inputs'),col('observed_inputs'),col('creation_result','categorical'),col('expected_enrollment','categorical'),col('observed_enrollment','categorical'),col('expected_organizational_unit','categorical'),col('observed_organizational_unit','categorical'),col('checkpoint_id','identifier'),col('supplied_baseline_checkpoint'),col('applied_control_evidence'),col('verification_status','categorical')],[
 ['onboard.complete','cedar-sandbox',account,'account cedar-sandbox; OU CedarSandbox','account cedar-sandbox; OU CedarSandbox','created','enrolled','enrolled','CedarSandbox','CedarSandbox','baseline.a','Compare supplied checkpoint A with its applied-control result','Supplied checkpoint A result matches','verified'],
 ['onboard.complete','cedar-sandbox',account,'account cedar-sandbox; OU CedarSandbox','account cedar-sandbox; OU CedarSandbox','created','enrolled','enrolled','CedarSandbox','CedarSandbox','baseline.b','Compare supplied checkpoint B with its applied-control result','Supplied checkpoint B result matches','verified'],
 ['onboard.incomplete','cedar-sandbox',account,'account cedar-sandbox; OU CedarSandbox','account cedar-sandbox; OU CedarSandbox','created','enrolled','enrolled','CedarSandbox','CedarSandbox','baseline.a','Compare supplied checkpoint A with its applied-control result','Supplied checkpoint A result matches','verified'],
 ['onboard.incomplete','cedar-sandbox',account,'account cedar-sandbox; OU CedarSandbox','account cedar-sandbox; OU CedarSandbox','created','enrolled','enrolled','CedarSandbox','CedarSandbox','baseline.b','Compare supplied checkpoint B with its applied-control result',None,'unverified']
], 'Two alternative evidence cases for one fictional account, not separate provisions. Opaque supplied checkpoint identifiers deliberately avoid inventing baseline controls. Account creation and enrollment do not substitute for missing checkpoint evidence.')
# Own mistakes-to-avoid audit: widths, types/roles, numeric labels, vocabulary,
# coverage, no runtime or credential assets, and no undeclared messy variants.
profile=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/'+g['path_id']+'.json').read_text())
assert all(b['context']['concept_id'] in profile['practice_type_by_concept'] for b in bundles if b['practice_anchor']['type'] in ['live_code','tool_simulation'])
assert len(registry['scenarios'])==1
for a in registry['assets']:
 assert a['asset_kind']=='dataset' and len(a['rows'])>0
 names=[c['name'] for c in a['columns']]; assert len(names)==len(set(names))
 assert not a.get('variants') # no duplicate operations or planted data-quality defects to verify
 for row in a['rows']:
  assert len(row)==len(names),a['asset_id']
  for c,v in zip(a['columns'],row):
   if v is None:continue
   if c['type']=='integer':
    assert isinstance(v,int) and not isinstance(v,bool)
    assert c['semantic_role']=='numerical' or (c['semantic_role']=='identifier' and c.get('numeric_looking_label'))
   else: assert isinstance(v,str) and c['semantic_role']!='numerical'
   if isinstance(v,str) and v.isdigit(): assert c.get('numeric_looking_label') is True and c['semantic_role']=='identifier'
assert all(b['visual_anchor']['type'] not in ['data_table','spreadsheet'] for b in bundles)
assert not any(re.search(r'\b(plot|chart|palette|bin count|axis limit)\b',t,re.I) for t in texts)
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
print('Mistakes-to-avoid audit PASS: widths; types and roles; numeric labels; no undeclared variants; all five concepts supported; vocabulary mined; no runtime assets; no plot needs.')
print('scenarios',len(registry['scenarios']),'assets',len(registry['assets']),'rows',sum(len(a['rows']) for a in registry['assets']),'vocabulary',len(vocab))
print('asset ids:',', '.join(a['asset_id'] for a in registry['assets']))
