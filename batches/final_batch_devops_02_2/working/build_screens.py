import json, re, copy
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.02_2')
p=json.loads((B/'tile_plans.json').read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
r=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']}
assets={x['asset_id']:x for x in r['assets']}
def rows(a):
    x=assets[a]; return [dict(zip([c['name'] for c in x['columns']],row)) for row in x['rows']]
def lin(c,tbs=(),facts=(),visual=False):
    return {'concept_ids':[c],'teaching_block_ids':[c+'#'+x for x in tbs],'fact_ids':[c+'#'+x for x in facts],**({'anchors':[c+'#visual']} if visual else {})}
def prose(c,text,tbs,facts,role='mechanism'):
    return {'type':'prose','text':text,'role':role,'lineage':lin(c,tbs,facts)}
def table(c,a,cols=None,caption=None,tbs=(),facts=()):
    available=[x['name'] for x in assets[a]['columns']]
    assert cols is None or set(cols)<=set(available)
    return {'type':'data_table','asset_ref':{'asset_id':a,'columns':cols or available},'caption':caption or assets[a]['title'],'lineage':lin(c,tbs,facts)}
def diagram(c,nodes,edges,title,tbs,facts,kind='mapping'):
    return {'type':'diagram','diagram_kind':kind,'title':title,'nodes':[{'id':i,'label':label,**({'fields':fields} if fields else {})} for i,label,fields in nodes],'edges':[{'from':a,'to':b,'label':label,'directed':True} for a,b,label in edges],'layout':'auto','alt_text':title,'lineage':lin(c,tbs,facts,True)}
# Each entry is one short idea with its own exact glossary lineage.
texts={
0:[[
('Permissions are made available through IAM Identity Center permission-set assignments to users or groups in specified AWS accounts. An operator needs approved access, not saved long-lived IAM user keys.',['tb1','tb2'],['f1'],'definition'),
('Use the supplied assignment workflow to assign the approved user or group, account and permission set. Then sign in to that account and test the intended access. Keep the assignment, signed-in permission-set context and test result together: sign-in alone is not the complete access check.',['tb3','tb4','tb5'],['f1','f2'],'workflow'),
('Configure a named SSO profile with aws configure sso. Establish its session with aws sso login --profile NAME, replacing NAME with the profile name. Use this session workflow rather than storing long-lived IAM user keys.',['tb3','tb4','tb5'],['f3'],'mechanism')]],
1:[[
('Security groups contain allow rules evaluated at associated network interfaces, not explicit deny rules.',['tb1','tb2'],['f1'],'definition'),
('They are stateful: responses to allowed connections are allowed regardless of response-direction rules. Add inbound rules for the required protocol, port range and approved source; remove unnecessary ingress, then test required connections and responses.',['tb3'],['f2','f3'],'mechanism')],[
('Use the supplied TCP ingress rule and approved source on the workload’s associated security group. Remove unnecessary ingress and test both the required connection and its response. A tracked response is allowed regardless of response-direction rules; a new connection from an unapproved source is a different case. Do not widen ingress to make an unexplained test pass.',['tb4'],['f1','f2','f3'],'example'),
('A security-group ID used as an allowed source identifies that source; it does not import the referenced group’s rules into the destination group. Security groups contain allow rules, not explicit deny rules.',['tb4','tb5','tb6'],['f1','m1'],'misconception'),
('Security groups do not filter traffic to Amazon-provided DNS or EC2 instance metadata services. Those cases are outside the filtering boundary, so their results do not demonstrate that ordinary ingress is allowed.',['tb4','tb5','tb6'],['f4'],'misconception')]],
2:[[
('Pin the approved hashicorp/aws version in terraform.required_providers. Declare resource "aws_instance" "NAME" with the supplied ami, instance_type and subnet_id; NAME is the chosen resource label.',['tb1','tb2','tb3'],['f1','f2'],'definition'),
('Run terraform init to install providers, terraform plan to inspect intended changes, and the approved terraform apply step to create the instance. Verify the resulting instance settings.',['tb3'],['f3'],'workflow')],[
('Compare the exact provider pin and resource settings against the supplied specification, then compare the inspected plan with those same values before the approved apply step. Keep provider selection, declaration, plan and verified instance settings separate in the evidence. The native EC2 foundation comes before interpreting these settings.',['tb4'],['f1','f2','f3'],'example'),
('A plausible declaration and provider pin are not execution evidence. Initialization installs providers; planning inspects intended changes; the approved apply creates the instance. Completion still needs verification of the resulting instance settings, not just a matching declaration. Use the supplied version and bounded resource settings rather than designing different infrastructure.',['tb4','tb5'],['f1','f2','f3'],'misconception')]],
3:[[
('A resource-based policy is attached to a resource and specifies the principals, actions and resources covered by its statements.',['tb1','tb2'],['f1'],'definition'),
('For an S3 bucket policy, compare Principal, Action, Resource and Condition with the request. Bucket and object ARNs have different scopes. Same-account identity and resource permissions can contribute allows; applicable explicit denies override them. Cross-account access generally requires permission on both sides.',['tb3'],['f2','f3'],'mechanism')],[
('Compare the caller with Principal, the operation with Action, the object ARN with Resource, and request values with Condition. A bucket ARN is not automatically the scope of an object request. A resource policy includes principal scope; it is not just an identity policy moved to another file.',['tb4','tb5'],['f1','f2'],'example'),
('Use the supplied permission evidence alongside the field matches. In a same-account request, identity and resource permissions can contribute allows, but an applicable explicit deny overrides them. For cross-account access, permission is generally required on both sides. Keep that qualification: the supplied ordinary cases are not an exhaustive account of special cases.',['tb4','tb5'],['f3'],'misconception')]],
4:[[
('Account Factory provisions and enrolls accounts into a governed landing zone using standardized account settings. The onboarding request supplies approved inputs and baseline checkpoints; creation is only part of the task.',['tb1','tb2'],['f1'],'definition'),
('Execute the established provisioning workflow with the approved account inputs. Inspect enrollment and organizational-unit placement, then verify each supplied baseline checkpoint against evidence of the account’s applied controls. Do not invent new baseline controls.',['tb3','tb4'],['f2','f3'],'workflow'),
('If the account was created but a checkpoint has no supporting result, record that distinction. Creation, enrollment and placement do not replace the checkpoint comparison. A created account alone does not demonstrate governance completion.',['tb4','tb5'],['f2','f3'],'misconception')]]}
recaps=[
'Permission sets make permissions available through user or group assignments in specified accounts. Match the approved assignment, sign in, and test intended access. Configure a named SSO profile and establish its session instead of storing long-lived IAM user keys.',
'Security groups use allow rules at associated network interfaces. Tracked responses are statefully allowed. Use required protocol, port range and approved source, remove unnecessary ingress, and test connections and responses. Source-group references do not import rules; DNS and metadata traffic are outside security-group filtering.',
'Pin the approved provider version and declare the supplied EC2 settings. Initialization installs providers, planning inspects changes, and the approved apply creates the instance. Verify the resulting settings: declaration alone is not execution evidence.',
'Match Principal, Action, Resource and Condition to the request. Distinguish bucket from object scope. Same-account permissions can contribute allows, but applicable explicit denies override them. Cross-account access generally needs permission on both sides.',
'Account Factory provisions and enrolls accounts using standardized settings. Use approved inputs, inspect enrollment and organizational-unit placement, then compare every supplied baseline checkpoint with applied-control evidence. Account creation alone does not demonstrate governance completion.'
]
remtexts=[
[
[('Configure a named SSO profile with aws configure sso, then establish its session with aws sso login --profile NAME. Use the supplied profile’s name for NAME. This named-session workflow, rather than storing long-lived IAM user keys, is the required access approach.',['tb3','tb5'],['f3'])],
[('Permission sets define permissions made available through assignments to users or groups in specified accounts. Match the approved user or group, account and permission set using the supplied workflow, then sign in and test intended access. Compare a completed test with sign-in alone: an untested operation is not a completed access check.',['tb2','tb3','tb4','tb5'],['f1','f2']),('Keep the named SSO profile configuration and session evidence too: aws configure sso configures the profile; aws sso login --profile NAME establishes its session. Use that session workflow rather than saving long-lived IAM user keys.',['tb3','tb4','tb5'],['f3'])]
],
[
[('Security groups are stateful. A tracked response to an allowed connection is allowed regardless of response-direction rules. Contrast that response with a new connection from an unapproved source: the response is not a fresh ingress request needing a separate response-direction allow.',['tb3','tb4'],['f2'])],
[('Security groups contain allow rules at associated network interfaces, not explicit deny rules. Specify the required protocol, port range and approved source, remove unnecessary ingress, then test the required connections and responses. Compare a matching approved-source rule with a new unapproved-source connection that has no matching inbound allow.',['tb2','tb3','tb4','tb5'],['f1','f3']),('A source-group ID identifies an allowed source without importing that group’s rule list. Compare a source reference with rule import: only the former describes the supplied evidence.',['tb4','tb5','tb6'],['m1'])]
],
[
[('terraform init installs providers. terraform plan inspects intended changes. The approved terraform apply step creates the instance, after which the instance settings must be verified. Compare a declaration with verified live settings: the declaration alone is not execution evidence.',['tb3','tb4','tb5'],['f3'])],
[('Use the exact approved version in the hashicorp/aws required_providers declaration, then declare resource "aws_instance" "NAME" with the supplied ami, instance_type and subnet_id. Compare the declaration and plan with the specification rather than substituting different settings.',['tb2','tb3','tb4'],['f1','f2']),('Initialization installs providers, planning inspects intended changes, and the approved apply creates the instance. Verification needs the resulting instance settings. A matching declaration is not the same as verified provisioning evidence.',['tb3','tb4','tb5'],['f3'])]
],
[
[('Same-account identity and resource permissions can contribute allows, but applicable explicit denies override them. Cross-account access generally requires permission on both sides. Compare the supplied cross-account cases with both sides allowing and with identity-side permission absent; do not treat a resource-side allow as generally sufficient by itself.',['tb3','tb4','tb5'],['f3'])],
[('A resource policy is attached to a resource and specifies principals, actions and resource scope. Match the request’s Principal, Action, Resource and Condition to the S3 policy. Compare the bucket ARN with the object ARN: they identify different scopes.',['tb2','tb3','tb4','tb5'],['f1','f2']),('Same-account identity and resource permissions can contribute allows, but an applicable explicit deny overrides them. Cross-account permission is generally needed on both sides. Matching policy fields alone do not replace the supplied identity-permission and deny evidence.',['tb3','tb4','tb5'],['f3'])]
],
[
[('Use approved inputs in the established onboarding workflow, inspect enrollment and organizational-unit placement, and compare supplied baseline checkpoints against applied-control evidence. Contrast creation completed with every checkpoint verified: creation alone does not demonstrate governance completion. Keep a checkpoint without supporting evidence unverified.',['tb3','tb4','tb5'],['f2','f3'])],
[('Account Factory provisions and enrolls accounts into a governed landing zone using standardized settings. Use the established workflow with approved inputs; inspect enrollment and organizational-unit placement. Compare each supplied baseline checkpoint with applied-control evidence.',['tb2','tb3','tb4'],['f1','f2','f3']),('A created, enrolled account with correct placement still differs from an account whose supplied checkpoints all have supporting results. Record a missing checkpoint result as unverified rather than declaring governance complete.',['tb4','tb5'],['f2','f3'])]
]
]
output={'schema_version':p['schema_version'],'kind':'screens_part','path_id':p['path_id'],'batch_id':p['batch_id'],'tiles':[]}
for idx,t in enumerate(p['tiles']):
    c=t['concept_ids'][0]; bun=bundles[c]
    out={'tile_id':t['tile_id'],'title':bun['context']['concept_name'],'steps':[],'remediation_steps':[]}
    ex=0
    for s in t['steps']:
        st={'step_id':s['step_id'],'type':s['type'],'concept_ids':copy.deepcopy(s['concept_ids']),'lineage':{k:copy.deepcopy(s[k]) for k in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']}}
        if s['type']=='explainer':
            st['title']=['Approved assignment, session and access','Allow the required connection','Pin and declare the supplied instance','Match a request to its resource policy','Creation is not governance completion'][idx] if ex==0 else ['','Keep the filtering boundary clear','Compare declaration with execution','Use scope and permission evidence',''][idx]
            st['eyebrow']='Learn'
            st['blocks']=[prose(c,*v) for v in texts[idx][ex]]
            if ex==0:
                if idx==0:
                    a=rows('ds.human_access')[0]
                    ns=[('approved','Approved assignment',[f"User: {a['user']}",f"Group: {a['operator_group']}",f"Account: {a['approved_account']}",f"Permission set: {a['approved_permission_set']}"]),('assigned','Assigned context',[f"Account: {a['assigned_account']}",f"Permission set: {a['assigned_permission_set']}"]),('signed','Signed-in context',[f"Account: {a['signed_in_account']}",f"Permission set: {a['signed_in_permission_set']}"]),('test','Intended access',[a['intended_access_test'],f"Expected: {a['expected_result']}",f"Observed: {a['observed_result']}"]),('profile','Named SSO profile',[a['profile_configuration'],a['session_evidence'],a['credential_storage']])]
                    st['blocks'].append(diagram(c,ns,[('approved','assigned','Match approval'),('assigned','signed','Sign in'),('signed','test','Test intended access'),('signed','profile','Use named session')],'Approved access context and test', ['tb2','tb3','tb4'],['f1','f2','f3'],'container'))
                elif idx==1:
                    rr=rows('ds.connection_tests'); a,b,d,ref,dns,meta=rr
                    ns=[('source',a['source'],[]),('eni',a['network_interface'],[a['destination_group'],a['inbound_rule']]),('response',b['traffic_case'],[b['observed_result']]),('other',d['source'],[d['observed_result']]),('group',ref['source'],['Identifies source; no rule import']),('outside','Outside filtering',[dns['traffic_case'],meta['traffic_case']])]
                    st['blocks'].append(diagram(c,ns,[('source','eni',f"{a['protocol']} {a['port']}: {a['observed_result']}"),('eni','response','Allowed regardless of response-direction rules'),('other','eni','No matching inbound allow'),('group','eni','Allowed source reference')],'Connection, tracked response and filtering boundary',['tb2','tb3','tb4','tb6'],['f1','f2','f3','f4','m1'],'network'))
                elif idx==2:
                    a=rows('ds.terraform_settings')[0]
                    code='terraform {\n  required_providers {\n    aws = {\n      source = '+json.dumps(a['provider_source'])+'\n      version = '+json.dumps('= '+a['provider_version'])+'\n    }\n  }\n}\n\nresource '+json.dumps(a['resource_type'])+' '+json.dumps(a['resource_label'])+' {\n'+''.join('  '+k+' = '+json.dumps(a[k])+'\n' for k in ['ami','instance_type','subnet_id'])+'}'
                    st['blocks'].append({'type':'side_by_side','left_label':'Exact provider pin and resource','right_label':'Specification, declaration, plan and verified settings','left':diagram(c,[('hcl','HCL declaration',[line for line in code.splitlines() if line.strip()])],[],'Exact provider pin and supplied resource',['tb2','tb3'],['f1','f2'],'container'),'right':table(c,'ds.terraform_settings',tbs=['tb3'],facts=['f2','f3']),'takeaway':'Compare the same supplied values at each evidence stage.','lineage':lin(c,['tb2','tb3'],['f1','f2','f3'],True)})
                elif idx==3:
                    policy=rows('ds.bucket_policy')[0]; req=rows('ds.object_requests')[0]; bucket=next(x['Resource'] for x in rows('ds.object_requests') if x['Resource']!=req['Resource'] and x['request_id'].endswith('bucket_scope'))
                    ns=[('caller',req['Principal'],[]),('request','Request',[f"{k}: {req[k]}" for k in ['Action','Resource','Condition']]),('policy','Attached bucket policy',[f"{k}: {policy[k]}" for k in ['Principal','Action','Resource','Condition']]),('bucket','Bucket scope',[bucket]),('object','Object scope',[req['Resource']]),('allows','Permission evaluation',['Same-account allows can contribute','Explicit deny overrides','Cross-account generally needs both sides'])]
                    st['blocks'].append(diagram(c,ns,[('caller','request','Principal'),('request','policy','Compare four fields'),('policy','bucket','Attached to bucket'),('request','object','Requested object'),('policy','allows','Combine supplied evidence')],'Caller, statement fields and distinct ARN scopes',['tb2','tb3'],['f1','f2','f3']))
                else:
                    rr=rows('ds.onboarding_checkpoints'); a=rr[0]
                    ns=[('inputs','Approved inputs',[a['approved_inputs']]),('created','Account creation',[a['account_name'],str(a['account_id']),a['creation_result']]),('enrolled','Enrollment',[f"Expected: {a['expected_enrollment']}",f"Observed: {a['observed_enrollment']}"]),('ou','Organizational-unit placement',[f"Expected: {a['expected_organizational_unit']}",f"Observed: {a['observed_organizational_unit']}"]),('checkpoints','Baseline evidence',list(dict.fromkeys(x['supplied_baseline_checkpoint'] for x in rr))),('contrast','Alternative evidence cases',list(dict.fromkeys(f"{x['case_id']}: {x['checkpoint_id']}: {x['applied_control_evidence'] or 'No supporting result'}; {x['verification_status']}" for x in rr)))]
                    st['blocks'].append(diagram(c,ns,[('inputs','created','Established workflow'),('created','enrolled','Inspect'),('enrolled','ou','Inspect'),('ou','checkpoints','Verify applied controls'),('checkpoints','contrast','Compare each checkpoint')],'Account onboarding evidence, not creation alone',['tb2','tb3','tb4','tb5'],['f1','f2','f3'],'container'))
            if idx==0:
                a=rows('ds.human_access')[0]
                st['blocks'].insert(2,prose(c,f"For {a['user']} in {a['operator_group']}, compare the assigned account and permission set with the approved context. The intended test is {a['intended_access_test'].lower()}. Keep its expected and observed results alongside the signed-in context.",['tb4'],['f1','f2'],'example'))
            if idx==1 and ex==1:
                st['blocks'].append(table(c,'ds.connection_tests',caption='Compare supplied connection cases, not DNS or metadata as ingress evidence.',tbs=['tb4','tb5','tb6'],facts=['f1','f2','f3','f4','m1']))
            if idx==2 and ex==1:
                a=rows('ds.terraform_settings')[0]
                pin=bun['teaching_blocks'][1]['content'].split('```hcl\n')[1].split('```')[0].strip().replace('APPROVED_VERSION',a['provider_version'])
                st['blocks'].insert(0,prose(c,'Use this exact approved provider declaration:\n\n```hcl\n'+pin+'\n```',['tb2','tb4'],['f1'],'syntax'))
                st['blocks'].append(table(c,'ds.terraform_execution',tbs=['tb4','tb5'],facts=['f3']))
            if idx==3 and ex==1:
                st['blocks'].append(table(c,'ds.bucket_policy',tbs=['tb4'],facts=['f1','f2']))
                st['blocks'].append(table(c,'ds.object_requests',tbs=['tb4','tb5'],facts=['f2','f3']))
            ex+=1
        elif s['type']=='video':
            st['title']='From assignment to signed-in context'
            st['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
        elif s['type']=='check':
            st['eyebrow']='Check your understanding';st['title']=['Choose the named-session workflow','Distinguish response from new ingress','Separate Terraform execution stages','Judge cross-account permission evidence','Distinguish creation from governance'][idx]
        elif s['type']=='hands_on':
            st['eyebrow']='Evidence review'
            st['title']=['Review human-access evidence','Review connection-rule evidence','Review Terraform provisioning evidence','Review policy and request fields','Review managed-account onboarding evidence'][idx]
            st['lede']=['Read the supplied assignment, sign-in, test and named-profile excerpts in this step. Decide which records demonstrate the approved access checks and which are defective.','Read the supplied connection and rule excerpts in this step. Decide which interpretations correctly enforce approved ingress and interpret source-group references.','Read the supplied declaration and execution excerpts in this step. Decide which records correctly show the approved pin, supplied instance settings and verified provisioning.','Read the supplied policy and request evidence. Select the matching fields and permission evidence, keeping bucket scope distinct from object scope.','Read the supplied onboarding excerpts in this step. Decide which records demonstrate enrollment, placement and baseline verification, and which leave governance unverified.'][idx]
        else:
            st['eyebrow']='Takeaways';st['title']='Keep the evidence distinct'
            alltb=[x['id'] for x in bun['teaching_blocks']]
            allfacts=list(dict.fromkeys(f for x in bun['teaching_blocks'] for f in x['fact_ids']))
            st['blocks']=[prose(c,recaps[idx],alltb,allfacts,'takeaway')]
            if idx+1<len(p['tiles']):
                nb=bundles[p['tiles'][idx+1]['concept_ids'][0]]
                nexttitle=nb['context']['concept_name']
                firstidea=['','Allow rules at associated network interfaces.','An approved provider pin and a supplied EC2 declaration.','A resource policy attached to the requested resource.','Standardized account provisioning and enrollment.'][idx+1]
            else:
                nexttitle=g['names'][bun['context']['blocked_future_concepts'][0]]
                firstidea='Next: Python AWS automation in an isolated dependency environment.'
            st['blocks'].append({'type':'up_next','title':nexttitle,'text':firstidea})
        out['steps'].append(st)
    assessed=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
    for j,s in enumerate(assessed):
        rb=[prose(c,text,tbs,facts,'misconception') for text,tbs,facts in remtexts[idx][j]]
        aids=[['ds.human_access'],['ds.connection_tests'],['ds.terraform_execution'] if j==0 else ['ds.terraform_settings','ds.terraform_execution'],['ds.object_requests'] if j==0 else ['ds.bucket_policy','ds.object_requests'],['ds.onboarding_checkpoints']][idx]
        tb=list(dict.fromkeys(tb for v in remtexts[idx][j] for tb in v[1]))
        ff=list(dict.fromkeys(f for v in remtexts[idx][j] for f in v[2]))
        for aid in aids:rb.append(table(c,aid,tbs=tb,facts=ff))
        # Re-show the exact authored provider declaration when that fact is measured.
        if idx==2 and j==1:
            rb.insert(1,copy.deepcopy(out['steps'][1]['blocks'][0]))
        assert set(s['fact_ids']) <= set(c+'#'+f for f in ff)
        out['remediation_steps'].append({'step_id':t['tile_id']+f'.r{j+1:02d}','type':'remediation','concept_ids':[c],'eyebrow':'Try the contrast','title':['Revisit the check','Revisit the evidence review'][j],'blocks':rb,'lineage':lin(c,tb,ff)})
    output['tiles'].append(out)
(B/'screens.json').write_text(json.dumps(output,indent=2)+'\n')
print('Wrote',len(output['tiles']),'tiles;',sum(len(t['steps']) for t in output['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in output['tiles']),'remediation steps')
