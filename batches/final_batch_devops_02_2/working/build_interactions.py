import json, copy
from pathlib import Path
B=Path(__file__).resolve().parents[1]
load=lambda f:json.loads((B/f).read_text())
P=load('tile_plans.json'); S=load('screens.json'); G=load('inputs/path_glossary_bundle.json'); R=load('scenario_asset_registry.json')
bundles={x['context']['concept_id']:x for x in G['bundles']}
assets={a['asset_id']:a for a in R['assets']}
def rows(aid):
 a=assets[aid]; return [dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
def evidence(r,omit=()):return '\n'.join(f'{k}: {v if v is not None else "no supplied evidence"}' for k,v in r.items() if k not in omit)
def fenced(t,lang='text'):return f'```{lang}\n{t}\n```'
def choice(prompt,opts):
 return {'prompt':prompt,'options':[{'option_id':f'o{i+1}','text':o[0]} for i,o in enumerate(opts)],'selection':'single','shuffle':True}, {'correct_option_ids':[f'o{i+1}' for i,o in enumerate(opts) if o[1]],'option_feedback':{f'o{i+1}':{'message':o[2]} for i,o in enumerate(opts)}}
def classify(prompt,labels,items):
 # Excerpt judgments have no dataset-column source: they grade configurations/results,
 # not semantic column roles (GENERATOR 9e).
 return {'prompt':prompt,'buckets':[{'bucket_id':k,'label':v} for k,v in labels.items()], 'items':[{'item_id':f'i{i+1}','text':text} for i,(text,key,msg) in enumerate(items)]}, {'assignments':{f'i{i+1}':key for i,(text,key,msg) in enumerate(items)},'item_feedback':{f'i{i+1}':{'message':msg} for i,(text,key,msg) in enumerate(items)}}
checks={
 '027':('Which workflow establishes a named AWS CLI SSO session without storing long-lived IAM user keys?',[
 ('Configure the named profile with aws configure sso, then use aws sso login --profile NAME for that profile.',True,'The named SSO profile is configured first, then its session is established using that profile.'),
 ('Save long-lived IAM user keys under a profile name instead of using SSO login.',False,'A profile name does not change the credential method. The taught workflow uses SSO rather than storing long-lived IAM user keys.'),
 ('Configure the named SSO profile and treat configuration alone as an established session.',False,'Configuration and session establishment are separate: aws sso login --profile NAME establishes the session.')]),
 '028':('A security group allowed a new connection. For the response to that tracked connection, there is no allow rule in the response direction. What follows from security-group statefulness?',[
 ('The response is allowed regardless of response-direction rules.',True,'Statefulness allows response traffic for the allowed connection.'),
 ('The response is blocked until a separate response-direction allow is added.',False,'Statefulness means this response does not require a separate response-direction allow rule.'),
 ('Every later new connection from any source is also allowed.',False,'A tracked response is not a new connection from an arbitrary source; new connections still need applicable allows.')]),
 '029':('A matching Terraform declaration is supplied. Which sequence distinguishes provider installation, intended-change inspection, creation and verification?',[
 ('terraform init; terraform plan and inspect the intended instance; approved terraform apply; compare resulting instance settings with the specification.',True,'Initialization installs providers, planning inspects changes, approved apply creates the instance, and the resulting settings still need verification.'),
 ('terraform init, then regard provider installation as proof that the instance was created.',False,'Initialization installs providers; it is not instance creation or verification.'),
 ('terraform plan, then regard the proposed instance as a verified created instance without apply.',False,'A plan describes intended changes; the approved apply creates the instance and resulting settings must be verified.')]),
 '030':('For an ordinary supplied cross-account S3 request with no applicable explicit deny, the resource side allows the request but identity-side permission is absent. Which judgement follows from the taught general rule?',[
 ('Permission is not demonstrated: cross-account access generally requires permission on both sides.',True,'The ordinary supplied case lacks identity-side permission; the general cross-account rule requires permission on both sides.'),
 ('The resource allow alone is sufficient because same-account contributed-allow reasoning always applies across accounts.',False,'Same-account contributed allows do not replace the general cross-account requirement for permission on both sides.'),
 ('The identity side alone would be sufficient even if the resource side did not permit the request.',False,'The general cross-account rule requires permission on both sides, not only identity-side permission.')]),
 '031':('An Account Factory account was created and its enrollment and organizational-unit placement match the approved inputs. One supplied baseline checkpoint has no supporting applied-control result. Which completion judgement is supported?',[
 ('Record that checkpoint as unverified; account creation alone does not demonstrate governance completion.',True,'The missing checkpoint evidence remains unverified even though creation, enrollment and placement have evidence.'),
 ('Mark governance complete solely because account creation succeeded.',False,'Creating an account does not substitute for checking enrollment, placement and supplied baseline evidence.'),
 ('Treat the missing checkpoint as verified because enrollment and placement match.',False,'Enrollment and placement do not supply the missing applied-control evidence for that checkpoint.')])}

# Human access: compare every supplied assignment, sign-in, test and SSO field.
hr=rows('ds.human_access'); hitems=[]
for r in hr:
 match=(r['assigned_account']==r['approved_account'] and r['assigned_permission_set']==r['approved_permission_set'] and r['signed_in_account']==r['approved_account'] and r['signed_in_permission_set']==r['approved_permission_set'])
 test=r['observed_result']==r['expected_result']
 key='complete' if match and test else ('assignment' if not match else 'test')
 msg={'complete':'Assignment and signed-in context match the approval, the intended access test matches its expected result, and named SSO configuration and session evidence show no stored long-lived IAM user keys.','assignment':'The assigned permission set differs from the supplied approval; sign-in to that same unapproved context is not a matching assignment.','test':'The intended access test is not tested. Successful sign-in does not establish its expected result.'}[key]
 hitems.append((fenced(evidence(r)),key,msg))
r=copy.deepcopy(hr[0]); r['credential_storage']='long-lived IAM user keys stored'; r['profile_configuration']='named profile populated with stored IAM user keys'; r['session_evidence']='no SSO login session evidence'
hitems.append((fenced(evidence(r,('case_id',))),'credentials','Matching account, permission set and access-test results do not satisfy the separate requirement for named SSO configuration and a session without stored long-lived IAM user keys.'))
hands={}
hands['027']=classify('Read each alternative access-review excerpt. Decide whether it meets all supplied assignment, account sign-in, intended-access test and named-SSO requirements, or identify its single unmet requirement. Permission-set names denote supplied approvals, not inferred AWS definitions.',{'complete':'All supplied requirements met','assignment':'Approved assignment/context mismatch','test':'Intended access test not verified','credentials':'Required SSO credential/session method not met'},hitems)

# Security-group judgement: full baseline evidence plus the source-reference trap.
nr=rows('ds.connection_tests'); n={r['test_id']:r for r in nr}; a=n[next(k for k in n if k.endswith('approved'))]; response=n[next(k for k in n if k.endswith('response'))]; unapproved=n[next(k for k in n if k.endswith('unapproved'))]; group=n[next(k for k in n if k.endswith('group_reference'))]
base=f"Associated network interface: {a['network_interface']}\nSecurity group: {a['destination_group']}\nApproved ingress: {a['inbound_rule']}\nComplete inbound rule list:\n- {a['inbound_rule']}\nNo other inbound rules.\nResponse-direction allow rule: {a['response_direction_rule']}\nTest: {a['source']} -> {a['observed_result']}\nTracked response: {response['observed_result']}\nNew connection: {unapproved['source']} -> {unapproved['observed_result']}"
extra=base.replace('No other inbound rules.',f"- allow {unapproved['protocol']} {unapproved['port']} from {unapproved['source'].split(': ')[-1]}").replace(unapproved['observed_result'],'connection succeeds')
gtext=evidence(group,('test_id','interpretation'))
hands['028']=classify('Read the ingress-review excerpts and decide whether the associated group meets the stated approved-ingress baseline and required connection checks. For the separate source-reference explanations, decide whether the interpretation is correct. A new unapproved-source connection is not a tracked response.',{'meets':'Ingress baseline and connection checks met','violates':'Ingress baseline or checks violated','reference_ok':'Source-reference explanation correct','reference_bad':'Source-reference explanation incorrect'},[
 (fenced(base),'meets','The only ingress rule admits the approved TCP connection, its tracked response succeeds without a separate response-direction rule, and the unapproved new connection is not admitted.'),
 (fenced(extra),'violates','The extra rule admits a new connection from an unapproved source. That unnecessary ingress violates the supplied baseline; statefulness does not justify it.'),
 (fenced(gtext+'\nReviewer explanation: The source-group ID identifies the allowed source; the destination group does not acquire the source group rules.'),'reference_ok','A source-group reference identifies an allowed source, not imported rules.'),
 (fenced(gtext+'\nReviewer explanation: The source-group ID imports all rules of that group into the destination group.'),'reference_bad','A security-group source reference does not import the referenced group rules into the destination group.')])

# Terraform: derived supplied values and stage evidence, with bounded excerpt defects.
tr=rows('ds.terraform_settings'); spec=tr[0]; execution=rows('ds.terraform_execution')
def tftext(pin=True,subnet=True,applied=True):
 version=('= ' if pin else '>= ')+spec['provider_version']
 hcl='terraform {\n  required_providers {\n    aws = {\n      source = '+json.dumps(spec['provider_source'])+'\n      version = '+json.dumps(version)+'\n    }\n  }\n}\nresource '+json.dumps(spec['resource_type'])+' '+json.dumps(spec['resource_label'])+' {\n  ami = '+json.dumps(spec['ami'])+'\n  instance_type = '+json.dumps(spec['instance_type'])+'\n'
 if subnet:hcl+='  subnet_id = '+json.dumps(spec['subnet_id'])+'\n'
 hcl+='}'
 text='Supplied specification:\n'+fenced(evidence(spec,('evidence_stage',)))+'\nObserved declaration:\n'+fenced(hcl,'hcl')
 text+='\nSupplied execution log:\n'+fenced('\n'.join(f"{r['command']}: {r['result']}" for r in execution[:(3 if applied else 2)]))
 text+='\nInspected plan: one intended instance\n'+fenced(evidence(tr[2],('evidence_stage',)))
 if applied:text+='\nApply approval: '+execution[-1]['approval_evidence']+'\nResulting instance settings:\n'+fenced(evidence(tr[-1],('evidence_stage',)))
 else:text+='\nNo apply or resulting-instance evidence supplied.'
 return text
hands['029']=classify('Read each alternative Terraform declaration and supplied execution/result excerpt. Compare the provider requirement and instance settings with the included specification; decide whether all declaration, initialization, one-instance plan, approved-apply and resulting-setting checks are met, or identify the single defect.',{'complete':'All supplied checks met','pin':'Provider requirement is not an exact approved pin','settings':'Declared instance values incomplete','execution':'Creation/result verification evidence missing'},[
 (tftext(),'complete','The exact provider pin and declared instance values match the specification, initialization succeeds, the plan contains one intended instance, and approved apply plus resulting settings are evidenced.'),
 (tftext(pin=False),'pin','A greater-than-or-equal provider constraint is not an exact approved version pin, even if the supplied execution evidence used that approved version.'),
 (tftext(subnet=False),'settings','The declaration omits the supplied subnet_id. Matching plan and result evidence cannot make the incomplete declaration satisfy the requirement to declare all three supplied settings.'),
 (tftext(applied=False),'execution','A matching declaration and plan do not demonstrate creation or resulting-instance verification; the approved apply and resulting settings need evidence.')])

# S3 row selections: hide stored outcomes and explanatory notes so judgement is required.
requests=rows('ds.object_requests'); policy=rows('ds.bucket_policy')
intro='Read the supplied bucket-policy statements and request evidence. Select one request row per judgement; compare Principal, Action, Resource and Condition before considering identity-side permission and explicit deny. These are ordinary supplied permission cases.\nBucket policy attached to the sandbox evidence bucket:\n'+fenced('\n\n'.join(evidence(r) for r in policy))
def outcome(r):
 if r['explicit_deny']!='none applicable':return False
 resource=r['resource_allow']=='matching'; identity=r['identity_allow']=='matching'
 return (resource and identity) if r['account_relationship']=='cross-account' else (resource or identity)
criteria=[
 ('Which same-account request is permitted by a matching resource allow even though identity-side allow evidence is absent?',lambda r:r['account_relationship']=='same-account' and r['identity_allow']=='absent' and outcome(r),'A matching resource allow contributes permission in this same-account case with no applicable explicit deny.'),
 ('Which request has matching identity and resource allows but is not permitted because an applicable explicit deny overrides them?',lambda r:r['identity_allow']=='matching' and r['resource_allow']=='matching' and r['explicit_deny']!='none applicable','An applicable explicit deny overrides both contributed allows.'),
 ('Which ordinary cross-account request is permitted because both identity and resource permission are present and no applicable explicit deny is supplied?',lambda r:r['account_relationship']=='cross-account' and outcome(r),'Both sides supply permission and no applicable explicit deny overrides it.'),
 ('Which ordinary cross-account request matches all four policy fields but is not permitted because identity-side permission is absent?',lambda r:r['account_relationship']=='cross-account' and r['resource_allow']=='matching' and r['identity_allow']=='absent','A field-matching resource allow does not replace absent identity-side permission in this ordinary cross-account case.'),
 ('Which request is not permitted because the caller fails to match Principal, although identity-side allow evidence is present?',lambda r:r['resource_allow']=='no matching principal','The unapproved caller does not match a resource-side Principal; the cross-account request lacks permission on that side.'),
 ('Which request is not permitted because its bucket ARN does not match the policy object-resource scope, with no identity allow to contribute permission?',lambda r:r['resource_allow']=='no matching object scope','The bucket ARN and object ARN identify different scopes; this request does not match the object-resource scope.'),
 ('Which request has a matching caller, action and object scope but is not permitted because Condition does not match and identity-side allow is absent?',lambda r:r['resource_allow']=='no matching condition','The supplied condition value fails to match the policy condition and no identity allow contributes permission.'),
 ('Which request has a matching caller, object scope and condition but is not permitted because Action does not match and identity-side allow is absent?',lambda r:r['resource_allow']=='no matching action','The requested operation differs from the policy Action; no matching resource or identity allow supplies permission.')]
tasks=[]; answers=[]; tfeedback={}
for i,(prompt,pred,msg) in enumerate(criteria):
 matches=[r for r in requests if pred(r)];assert len(matches)==1
 r=matches[0]; tid=f't{i+1}'
 tasks.append({'task_id':tid,'prompt':prompt,'target_kind':'row'})
 answers.append({'task_id':tid,'row':{'where':{'request_id':r['request_id']},'occurrence':0}})
 tfeedback[tid]={'correct':msg,'incorrect':'Recheck the four policy fields, the account relationship, contributed allows and applicable explicit deny. '+msg}
visible=[c['name'] for c in assets['ds.object_requests']['columns'] if c['name'] not in ('permission_outcome','evidence_note')]
hands['030']=({'asset_ref':{'asset_id':assets['ds.object_requests']['asset_id'],'columns':visible},'intro':intro,'tasks':tasks},{'answers':answers,'task_feedback':tfeedback})
# Checkpoint review: full approved context on each row, missing-result trap included.
on=rows('ds.onboarding_checkpoints'); oi=[]
for r in on:
 matches=r['approved_inputs']==r['observed_inputs'] and r['expected_enrollment']==r['observed_enrollment'] and r['expected_organizational_unit']==r['observed_organizational_unit']
 supported=matches and r['applied_control_evidence'] is not None
 key='verified' if supported else 'unverified'
 assert key==r['verification_status']
 msg='Approved inputs, enrollment and OU placement match. The supplied checkpoint has matching applied-control evidence.' if supported else 'The account exists and enrollment and placement match, but this checkpoint has no supporting applied-control result. It remains unverified; creation does not establish governance completion.'
 oi.append((fenced(evidence(r,('verification_status',))),key,msg))
hands['031']=classify('Read each checkpoint-review excerpt from two alternative onboarding cases for the same account. Compare approved and observed inputs, enrollment and OU placement, then judge each baseline checkpoint against its applied-control evidence. Decide whether the checkpoint is verified or remains unverified; all checkpoints need supporting evidence before governance completion is demonstrated.',{'verified':'Context matches and checkpoint verified','unverified':'Checkpoint remains unverified'},oi)

out={k:P[k] for k in ('schema_version','path_id','batch_id')};out['kind']='interactions_part';out['tiles']=[]
for t in P['tiles']:
 tile={'tile_id':t['tile_id'],'interactions':[]};num=t['tile_id'].split('.')[-1];screen=next(x for x in S['tiles'] if x['tile_id']==t['tile_id']);seen=set()
 for s in t['steps']:
  if s['type'] not in ('check','hands_on'):continue
  cid=s['concept_ids'][0];bundle=bundles[cid]
  measures=[]
  for ref in s['anchors']:
   if '#assessment:' in ref:
    cap=ref.split('#assessment:')[1];a=next(a for a in bundle['assessment_anchors'] if a['capability']==cap)
    measures.append({'concept_id':cid,'capability':a['capability'],'fact_ids':copy.deepcopy(a['fact_ids'])})
  pub,grading=choice(*checks[num]) if s['type']=='check' else hands[num]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if s['type']=='check' else 'stretch','grading_mode':'client','standalone':True,'measures':measures,'anchors':copy.deepcopy(s['anchors']),'public':pub,'grading':grading,'feedback':{'correct':{'message':'Your judgement follows the supplied evidence and the taught checks.'},'incorrect':{'message':'Separate the individual evidence checks; success at one stage does not establish all required conditions.'},'hints':['Compare each required condition with the specific evidence supplied.','Do not substitute a successful earlier stage for a missing later check.']}}
  hint_bank={
   '027':['Keep assignment, sign-in and intended-operation results as separate checks.','Distinguish profile configuration from establishing its session.'],
   '028':['Distinguish a tracked response from a new connection.','Read the complete inbound rule list and the source-reference explanation separately.'],
   '029':['Compare each declared setting and the provider requirement with the specification.','Keep proposed changes distinct from created-instance evidence.'],
   '030':['Match the four request fields before considering contributed permission.','Keep account relationship and explicit-deny evidence in the decision.'],
   '031':['Compare the approved context with the observed context.','Check each baseline result separately from the creation result.']}
  ix['feedback']['hints']=hint_bank[num][:1] if s['type']=='check' else hint_bank[num]
  if s['type']=='check':
   ix['feedback']['correct']['message']=next(o[2] for o in checks[num][1] if o[1])
   ix['feedback']['incorrect']['message']={
    '027':'A named profile must use the taught SSO configuration and session workflow rather than stored long-lived IAM user keys.',
    '028':'Judge the response as response traffic for the already allowed connection, not as an arbitrary new connection.',
    '029':'Separate provider installation, intended changes, actual creation and resulting-setting verification.',
    '030':'Apply the general cross-account requirement rather than treating this as a same-account contributed-allow case.',
    '031':'Creation, enrollment and placement do not provide a missing applied-control checkpoint result.'}[num]
  remediations=[r for r in screen.get('remediation_steps',[]) if cid in r['concept_ids']]
  if remediations:
   ix['feedback']['remediation_step_id']=remediations[0 if cid not in seen else min(1,len(remediations)-1)]['step_id']
  seen.add(cid)
  tile['interactions'].append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append(tile)
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
