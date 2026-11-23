import json, copy
from pathlib import Path
B=Path(__file__).resolve().parents[1]
plan=json.loads((B/'tile_plans.json').read_text())
screens=json.loads((B/'screens.json').read_text())
gloss=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
registry=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in gloss['bundles']}
assets={a['asset_id']:a for a in registry['assets']}
def rows(aid):
 a=assets[aid]; return [dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
ec=rows('ds.ec2_launch_evidence') if 'ds.ec2_launch_evidence' in assets else rows(next(a for a in assets if 'ec2' in a))
approved,observed=ec
up,down=rows('ds.s3_transfer_evidence')
metric=rows('ds.metric_identity_evidence'); pub=metric[0]; staging=metric[1]
def identity(r):
 ds=', '.join(f'{k}={r[k]}' for k in ['Environment','Service'] if r.get(k) is not None)
 return f"{r['namespace']} | {r['metric_name']} | {ds}"
def command(r):
 return f"aws s3 cp {r['source']} {r['destination']} --profile {r['operator_profile']} --region {r['bucket_region']}"
def metric_command(r):
 dims=' '.join(f'Name={k},Value={r[k]}' for k in ['Environment','Service'] if r.get(k) is not None)
 return f"aws cloudwatch put-metric-data --namespace {r['namespace']} --metric-name {r['metric_name']} --value {r['supplied_value']} --dimensions {dims}"
def feedback(correct,incorrect,hint):
 return {'correct':{'message':correct},'incorrect':{'message':incorrect},'hints':[hint]}
def base(tile,step):
 cid=step['concept_ids'][0]; bundle=bundles[cid]
 caps=[a.split('#assessment:')[1] for a in step['anchors'] if '#assessment:' in a]
 if not caps: caps=[a['capability'] for a in bundle['assessment_anchors']]
 measures=[dict(concept_id=cid,capability=a['capability'],fact_ids=a['fact_ids']) for a in bundle['assessment_anchors'] if a['capability'] in caps]
 return dict(type=step['planned_interaction_type'],interaction_id='ix.'+step['step_id'],difficulty='intro' if step['type']=='check' else 'stretch',grading_mode='client',standalone=True,measures=measures,anchors=step['anchors'])
def choice(ix,prompt,options):
 # options consist of (text, predicate result, fact-grounded feedback).
 opts=[{'option_id':f'o{i+1}','text':o[0]} for i,o in enumerate(options)]
 ix['public']={'prompt':prompt,'options':opts,'selection':'single','shuffle':True}
 ix['grading']={'correct_option_ids':[o['option_id'] for o,s in zip(opts,options) if s[1]],'option_feedback':{o['option_id']:{'message':s[2]} for o,s in zip(opts,options)}}
 assert len(ix['grading']['correct_option_ids'])==1

def classify(ix,prompt,items):
 # Inline inspect-and-judge (9e): no asset_ref/source or role_map for judgement buckets.
 ix['public']={'prompt':prompt,'buckets':[{'bucket_id':'meets','label':'Meets the stated review criteria'},{'bucket_id':'fails','label':'Violates at least one stated review criterion'}],'items':[{'item_id':f'i{i+1}','text':x[0]} for i,x in enumerate(items)]}
 ix['grading']={'assignments':{f'i{i+1}':('meets' if x[1] else 'fails') for i,x in enumerate(items)},'item_feedback':{f'i{i+1}':{'message':x[2]} for i,x in enumerate(items)}}
 assert any(x[1] for x in items) and any(not x[1] for x in items)

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='interactions_part',tiles=[])
for ti,tile in enumerate(plan['tiles']):
 entries=[]
 for step in tile['steps']:
  if step['type'] not in ['check','hands_on']:continue
  ix=base(tile,step);check=step['type']=='check'
  if ti==0 and check:
   prompt=f"Read this instance excerpt. Which conclusion preserves the distinction between lifecycle and reported health?\n```text\ninstance_id: {observed['instance_id']}\nlifecycle_state: {observed['lifecycle_state']}\nsystem_status_check: {observed['system_status_check']}\ninstance_status_check: {observed['instance_status_check']}\n```"
   options=[('Record the running lifecycle state and the status-check results separately; running does not prove health.',observed['lifecycle_state']=='running' and observed['instance_status_check']=='impaired','State and status checks answer different questions; retain both observations.'),('Mark the instance healthy because it is running.',False,'Running is lifecycle evidence, not proof that the status checks report health.'),('Replace the lifecycle state with impaired.',False,'Impaired is the instance status-check result here, not the lifecycle state.'),('Discard the instance check because the system check is ok.',False,'The system and instance checks are separate reported health evidence; the ok system check does not erase the impaired instance check.')]
   choice(ix,prompt,options)
   ix['feedback']=feedback('You kept lifecycle and health evidence separate.','Read the state and each status check as distinct evidence.','Ask which field describes lifecycle, and which fields report health.')
  elif ti==0:
   fields=['instance_id','ami','instance_type','subnet','instance_profile','attached_role','lifecycle_state','system_status_check','instance_status_check']
   brief='\n'.join(f'{k}: {approved[k]}' for k in ['ami','instance_type','subnet','instance_profile','attached_role'])
   prompt=f"Read the approved choices and each independent review excerpt. Decide whether each review meets ALL criteria: one created instance, its ID/settings correctly recorded against the supplied choices, the profile-attached role correctly identified, and lifecycle/status checks retained separately without treating running as proof of health. Judge the review, not whether an impaired check is desirable.\nApproved choices:\n```text\n{brief}\n```"
   items=[]
   for variant in ['complete','wrong_ami','embedded_keys','running_proves_health']:
    rec=copy.deepcopy(observed)
    if variant=='wrong_ami':rec['ami']=approved['subnet']
    role_ok=variant!='embedded_keys'; health_ok=variant!='running_proves_health'
    report='Created instances: one\n'+'\n'.join(f'{k}: {rec[k]}' for k in fields)
    report+='\nRole interpretation: '+('The supplied instance profile attaches the listed IAM role; applications use temporary role credentials.' if role_ok else 'The instance profile is embedded application access keys, not a container attaching an IAM role.')
    report+='\nHealth interpretation: '+('Lifecycle and both status checks recorded separately; running is not proof of health.' if health_ok else 'Record running as proof that the instance is healthy; status-check results can be ignored.')
    valid=all(rec[k]==approved[k] for k in ['ami','instance_type','subnet','instance_profile','attached_role']) and rec['instance_id']==observed['instance_id'] and role_ok and health_ok
    message={'complete':'The ID and approved settings match, the profile attaches the role, and the running state remains separate from ok/impaired status checks.','wrong_ami':'The recorded AMI is the subnet identifier, not the approved initial-image identifier; the settings record does not match the created instance.','embedded_keys':'An instance profile contains and attaches an IAM role; it is not embedded application access keys.','running_proves_health':'Running is lifecycle state; the impaired instance check remains reported health evidence and cannot be discarded.'}[variant]
    items.append(('```text\n'+report+'\n```',valid,message))
   classify(ix,prompt,items)
   ix['feedback']=feedback('You checked the settings, role attachment and separate health evidence.','A matching launch alone is insufficient: also inspect the role interpretation and state/status-check record.','Compare field names as well as identifiers; then inspect the review conclusions.')
  elif ti==1 and check:
   prompt=f"The intended download is from {down['source']} to {down['destination']}. Supplied profile: {down['operator_profile']}; verified bucket Region: {down['bucket_region']}. Access evidence: {down['caller_access_evidence']} Which command specifies that download with the supplied AWS context?"
   bad1=copy.deepcopy(down);bad1['source'],bad1['destination']=bad1['destination'],bad1['source']
   bad2=command(down).split(' --profile')[0]+f" --region {down['bucket_region']}"
   bad3=command(down).split(' --region')[0]
   options=[(command(bad1),False,'The endpoints are reversed: this sends a local file to S3 instead of retrieving the intended object.'),(command(down),all(down[k]==up[k] for k in ['bucket','object_key','operator_profile','bucket_region']),'The S3 URI is the source, the local path is the destination, and profile/Region are explicit.'),(bad2,False,'The supplied operator profile is omitted; the task requires an explicit profile.'),(bad3,False,'The verified bucket Region is omitted; the task requires an explicit Region.')]
   choice(ix,prompt,options)
   ix['feedback']=feedback('The endpoints and explicit AWS context match the intended retrieval.','A valid review needs the correct direction, profile and verified bucket Region together.','Locate the source first; then check both context flags.')
  elif ti==1:
   prompt=f"Read each independent transfer record and decide whether it meets ALL criteria: upload the supplied local file to the intended bucket/key, download that same object to the separate local destination, use the supplied profile and verified Region in BOTH commands, and retain successful transfer and matching-artifact evidence.\nSupplied upload: {up['source']} → {up['destination']}. Supplied download: {down['source']} → {down['destination']}. Bucket: {up['bucket']}; key: {up['object_key']}; profile: {up['operator_profile']}; verified Region: {up['bucket_region']}. Access evidence: {up['caller_access_evidence']}"
   items=[]
   for variant in ['complete','reversed_download','wrong_key','missing_context','unconfirmed_match']:
    u,d=copy.deepcopy(up),copy.deepcopy(down)
    if variant=='reversed_download': d['source'],d['destination']=d['destination'],d['source']
    if variant=='wrong_key':d['source']=f"s3://{down['bucket']}/{down['destination']}"
    cmds=[command(u),command(d)]
    if variant=='missing_context':cmds[1]=cmds[1].split(' --profile')[0]
    compare=down['artifact_comparison_evidence'] if variant!='unconfirmed_match' else 'Local file exists; no artifact-comparison result is supplied.'
    record='\n'.join(cmds)+'\nTransfer record: both displayed commands completed successfully.\nComparison evidence: '+compare
    valid=cmds==[command(up),command(down)] and compare==down['artifact_comparison_evidence']
    why={'complete':'Both directions use the intended bucket/key, both context flags are explicit, and the supplied comparison confirms the retrieved artifact matches.','reversed_download':'The second command uploads from the local destination; it does not download the intended S3 object.','wrong_key':'The second command uses the local destination path as the S3 key instead of the supplied releases key. Successful transfer alone does not establish the intended object.','missing_context':'The second command omits the supplied profile and verified Region, so both-command context criteria are not met.','unconfirmed_match':'A local file existing is not the supplied confirmation that the retrieved artifact matches the original file.'}[variant]
    items.append(('```text\n'+record+'\n```',valid,why))
   classify(ix,prompt,items)
   ix['feedback']=feedback('You judged the complete round trip rather than just a successful copy.','Check the same bucket/key in both directions, both context flags and the artifact comparison.','Trace the S3 URI through both commands; then inspect what the comparison evidence actually says.')
  elif ti==2 and check:
   prompt=f"The intended published workload series is {identity(pub)}. Which supplied query identity selects that exact series? Query records below are selections only, not returned values."
   options=[]
   for r in metric[2:]:
    valid=all(r[k]==pub[k] for k in ['namespace','metric_name','Environment','Service'])
    why=('The namespace, name and complete dimension combination match the published sandbox orders identity.' if valid else ('This selects the staging combination, a distinct metric, not the sandbox orders series.' if r['Service'] else 'Service is omitted, so the query does not match the complete published dimension combination.'))
    options.append((identity(r),valid,why))
   choice(ix,prompt,options)
   ix['feedback']=feedback('The complete queried identity matches the intended publication.','A familiar metric name is not enough; compare the entire dimension combination.','Compare all identity components, including the set of dimensions.')
  else:
   prompt=f"Read each independent fictional publication/result excerpt and decide whether it meets ALL criteria: put-metric-data specifies namespace {pub['namespace']}, name {pub['metric_name']}, supplied value {pub['supplied_value']}, and exactly Environment={pub['Environment']}, Service={pub['Service']}; only that combination is published; the exercise result associates the value with that complete identity. Do not accept an omitted dimension or a staging result merely because the name matches."
   items=[]
   for variant in ['complete','omitted_dimension','wrong_value','wrong_result_identity','extra_combination']:
    r=copy.deepcopy(pub);result=copy.deepcopy(pub)
    if variant=='omitted_dimension':r['Service']=None;result['Service']=None
    if variant=='wrong_value':r['supplied_value']=staging['supplied_value'];result['supplied_value']=staging['supplied_value']
    if variant=='wrong_result_identity': result=copy.deepcopy(staging);result['supplied_value']=pub['supplied_value']
    cmds=[metric_command(r)]
    if variant=='extra_combination':cmds.append(metric_command(staging))
    text='\n'.join(cmds)+f"\nPublication record: displayed publication(s) completed.\nExercise result: value {result['supplied_value']} associated with {identity(result)}."
    valid=r==pub and result==pub and len(cmds)==1
    why={'complete':'The publication uses the supplied value and exactly both intended dimensions, and the result retains the complete sandbox orders identity.','omitted_dimension':'Service is absent from the publication and result identity; this is not the intended complete dimension combination.','wrong_value':'The publication and result use the staging supplied value instead of the supplied sandbox value.','wrong_result_identity':'The command uses the sandbox dimensions, but the result is associated with staging; distinct dimension combinations identify distinct metrics.','extra_combination':'A second staging publication adds a distinct dimension combination; the stated practice requires only the supplied sandbox combination.'}[variant]
    items.append(('```text\n'+text+'\n```',valid,why))
   classify(ix,prompt,items)
   ix['feedback']=feedback('You checked both publication inputs and the complete identity attached to its result.','The publication value, exact dimension set and result identity must all agree with the supplied sandbox case.','Compare the publication with its result record; check for missing or additional combinations.')
  if check:
   st=next(t for t in screens['tiles'] if t['tile_id']==tile['tile_id'])
   rem=next((r for r in st['remediation_steps'] if step['concept_ids'][0] in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
  if not check:
   st=next(t for t in screens['tiles'] if t['tile_id']==tile['tile_id'])
   rems=[r for r in st['remediation_steps'] if step['concept_ids'][0] in r['concept_ids']]
   if len(rems)>1:ix['feedback']['remediation_step_id']=rems[1]['step_id']
  entries.append({'step_id':step['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
