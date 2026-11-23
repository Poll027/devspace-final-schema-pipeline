import json, copy, re
from pathlib import Path
from xml.sax.saxutils import escape
B=Path('batches/final_batch_aws_devops.region.01_2')
p=json.loads((B/'tile_plans.json').read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
r=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']}
assets={a['asset_id']:a for a in r['assets']}
def records(aid):
 a=assets[aid]; return [dict(zip([c['name'] for c in a['columns']],row)) for row in a['rows']]
e=records('ds.ec2_launch_evidence'); u,d=records('ds.s3_transfer_evidence'); m=records('ds.metric_identity_evidence')
E=e[1]
def lin(c, facts, tbs, anchors=None):
 return {'concept_ids':[c],'fact_ids':[c+'#'+f if '#' not in f else f for f in facts], 'teaching_block_ids':[c+'#'+t if '#' not in t else t for t in tbs], 'anchors':anchors or []}
def prose(text,c,facts,tbs,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':lin(c,facts,tbs)}
def diagram(nodes,alt,lineage,edges=None):
 return {'type':'diagram','diagram_kind':'container','nodes':nodes,'edges':edges or [],'layout':'auto','alt_text':alt,'lineage':copy.deepcopy(lineage)}
# Visible evidence is derived from registry rows, not manually transcribed.
def ec2_visual(c):
 fields=['ami','instance_type','subnet','instance_profile','attached_role']
 nodes=[{'id':'approved','label':'Approved choices','fields':[f'{k}: {e[0][k]}' for k in fields]},
        {'id':'created','label':'Created instance','fields':[f'instance_id: {E["instance_id"]}']+[f'{k}: {E[k]}' for k in fields]},
        {'id':'state','label':'Lifecycle','fields':[f'lifecycle_state: {E["lifecycle_state"]}']},
        {'id':'health','label':'Status checks','fields':[f'{k}: {E[k]}' for k in ['system_status_check','instance_status_check']]}]
 return diagram(nodes,'Approved selections and created EC2 details; lifecycle state and status checks are separate panels.',lin(c,['f1','f2','f3','f4'],['tb1','tb2','tb3'],[c+'#visual']),[{'from':'approved','to':'created','label':'Compare settings'},{'from':'created','to':'state'},{'from':'created','to':'health'}])
def s3_visual(c):
 code='\n'.join(f'aws s3 cp {x["source"]} {x["destination"]} --profile {x["operator_profile"]} --region {x["bucket_region"]}' for x in [u,d])
 return {'type':'code_walkthrough','language':'bash','code':code,'annotations':[{'start_line':1,'end_line':1,'text':'Upload: local → bucket/key; explicit profile and Region.'},{'start_line':2,'end_line':2,'text':'Download: same bucket/key → local; same explicit context.'}],'reveal':'all','lineage':lin(c,['f2','f3'],['tb3'],[c+'#visual'])}
def identity(x):
 dims=[f'{k}={x[k]}' for k in ['Environment','Service'] if x[k] is not None]
 return f'{x["namespace"]} | {x["metric_name"]} | '+', '.join(dims)
def metric_visual(c):
 l=lin(c,['f1','f3'],['tb1','tb2','tb3'],[c+'#visual'])
 left=diagram([{'id':'published'+str(i),'label':identity(x)} for i,x in enumerate(m[:2])],'Two published metric identities.',l)
 right=diagram([{'id':'queried'+str(i),'label':identity(x)} for i,x in enumerate(m[2:])],'Two complete queries and one query omitting Service.',l)
 return {'type':'side_by_side','left':left,'right':right,'left_label':'Published','right_label':'Queried','takeaway':'Match the complete identity.','lineage':l}
texts=[
 [
  ('Connect choices to the instance', [
   ('Launch choices include AMI, instance type and network placement. The AMI supplies the initial software image. Use the approved AMI, subnet and supplied instance profile; inspect the created ID and settings.', ['f1','f2'],['tb1','tb2','tb3']),
   ('The profile attaches its IAM role; applications can use temporary role credentials. Read lifecycle state separately from reported host or instance health.', ['f3','f4'],['tb3'])]),
  ('Read identity and health separately', [
   (f'The observed instance {E["instance_id"]} matches the approved AMI {E["ami"]}, type {E["instance_type"]} and subnet {E["subnet"]}. The AMI is its initial software image. The supplied profile {E["instance_profile"]} attaches {E["attached_role"]}; applications can use that role’s temporary credentials.', ['f1','f2','f3'],['tb4']),
   (f'Its lifecycle state is {E["lifecycle_state"]}, while the system check is {E["system_status_check"]} and the instance check is {E["instance_status_check"]}. Keep both kinds of evidence: running is not proof of health, and a completed launch does not replace status checks. The profile is a role container, not embedded application access keys.', ['f3','f4'],['tb4','tb5'])]),
  ('Distinguish state from health','Read the supplied evidence and choose the interpretation that keeps lifecycle and health separate.'),
  ('Review EC2 operating evidence','Read the supplied excerpts in this step and judge which interpretations correctly connect launch choices, instance identity, the attached role and health evidence.'),
  ('Keep the operating evidence distinct','Use approved launch choices, inspect the created identity and settings, and identify the role through its profile. Applications can use temporary role credentials. Record lifecycle state and status checks separately.')
 ],
 [
  ('Trace both S3 transfer directions',[
   ('An S3 object contains data and metadata; its key identifies it within a bucket. Upload with aws s3 cp from local file to bucket/key; download reverses the endpoints. Keep profile and Region explicit. Buckets are created in an AWS Region; verify location and caller access.', ['f1','f2','f3'],['tb1','tb2','tb3'])]),
  ('Verify the intended object and context',[
   (f'The upload goes from {u["source"]} to {u["destination"]}. The download reads that same bucket/key into {d["destination"]}. The key {u["object_key"]} identifies the object within {u["bucket"]}; a familiar local filename or key alone does not establish the intended storage location.', ['f1','f2'],['tb4','tb5']),
   (f'Both commands use profile {u["operator_profile"]} and verified bucket Region {u["bucket_region"]}. The supplied access evidence says: {u["caller_access_evidence"]} After retrieval, the supplied comparison says: {d["artifact_comparison_evidence"]} A file arriving locally is not enough if its bucket/key differs from the intended object. Check endpoints, location and access rather than inferring them from the filename.', ['f2','f3'],['tb4','tb5'])]),
  ('Check transfer context','Read the supplied transfer evidence and choose the interpretation that verifies direction, bucket location and caller access.'),
  ('Review S3 transfer excerpts','Read the supplied excerpts in this step and judge which transfers use the intended bucket/key and correct upload or download endpoints.'),
  ('Identify the object, then trace the transfer','An object contains data and metadata; identify it by bucket and key. Upload points from local to S3; download reverses the endpoints. Use explicit profile and Region, and verify bucket location and caller access.')
 ],
 [
  ('Match a metric’s full identity',[
   ('A custom CloudWatch metric’s identity is namespace, name and dimension combination. Publish with put-metric-data, supplying namespace, name, value and intended dimensions. Distinct combinations identify distinct metrics; query the published combination to select the intended series.', ['f1','f2','f3'],['tb1','tb2','tb3'])]),
  ('Compare combinations, not names',[
   (f'The sandbox publication is {identity(m[0])}, with supplied value {m[0]["supplied_value"]}. Publish using put-metric-data with that namespace, name, value and both dimensions. The staging publication is {identity(m[1])}, with supplied value {m[1]["supplied_value"]}. It is a distinct metric despite sharing the name.', ['f1','f2','f3'],['tb4']),
   (f'The complete sandbox query selects {identity(m[2])}. A query omitting Service uses {identity(m[4])}: that is not the published sandbox orders combination. Compare the full published and queried identities, not only the metric name. These query records describe selections, not returned values; do not describe a staging series as the sandbox orders value.', ['f1','f3'],['tb4','tb5'])]),
  ('Check the selected series','Read the supplied identities and choose the query interpretation that matches the full published combination.'),
  ('Review metric publication excerpts','Read the supplied excerpts in this step and judge which publications specify the supplied namespace, metric name, value and intended dimensions.'),
  ('Preserve complete metric identity','Publish namespace, name, supplied value and intended dimensions with put-metric-data. A custom metric’s identity includes the complete dimension combination; query that same combination, not just a familiar name.')
 ]
]
remedies=[
 [
  ('Separate lifecycle from health',f'In the same EC2 evidence, state is {E["lifecycle_state"]} but the instance status check is {E["instance_status_check"]}. State describes lifecycle; status checks report host or instance health. Retain both rather than treating running as proof of health.', ['f4'],['tb3','tb4','tb5']),
  ('Reconnect launch choices and observed details',f'Launch choices include AMI, type and network placement; the AMI supplies the initial software image. Compare the created ID {E["instance_id"]} and settings with the approved AMI, subnet and supplied profile. The profile {E["instance_profile"]} attaches role {E["attached_role"]}; applications can use its temporary credentials. Contrast an approved request with observed instance evidence. Inspect state and status checks separately: running does not establish reported health.', ['f1','f2','f3','f4'],['tb2','tb3','tb4','tb5'])
 ],
 [
  ('Keep direction and context together',f'In the same transfer evidence, upload has local source {u["source"]} and S3 destination {u["destination"]}; download reverses the direction into a local destination. Use aws s3 cp with explicit profile {u["operator_profile"]} and Region {u["bucket_region"]} in both directions. A bucket is created in a Region: verify its intended location and caller access, rather than assuming them from the filename.', ['f2','f3'],['tb3','tb4','tb5']),
  ('Distinguish key from local filename',f'An S3 object consists of data and metadata. In the same evidence, {u["object_key"]} is the key within bucket {u["bucket"]}; {u["source"]} is the local upload source. Those are different roles. With aws s3 cp, upload goes local → S3 bucket/key and download goes from that same S3 bucket/key → local, keeping explicit profile and Region. A familiar local filename is not a substitute for verifying the intended bucket/key.', ['f1','f2'],['tb2','tb3','tb4','tb5'])
 ],
 [
  ('Contrast complete and incomplete identities',f'A custom metric is identified by namespace, name and dimension combination. In the same evidence, {identity(m[0])} and {identity(m[1])} are distinct metrics. Query the complete published combination. Keeping Environment=sandbox but omitting Service=orders does not select the stated sandbox orders identity; matching the name alone is insufficient.', ['f1','f3'],['tb2','tb3','tb4','tb5']),
  ('Keep publication inputs together',f'Use put-metric-data to publish the supplied namespace {m[0]["namespace"]}, metric name {m[0]["metric_name"]}, value {m[0]["supplied_value"]} and dimensions Environment={m[0]["Environment"]}, Service={m[0]["Service"]}. Contrast a complete publication with one missing an intended dimension. Namespace, name and the complete combination identify the metric; a different combination is a distinct metric. Query the same combination that was published.', ['f1','f2','f3'],['tb2','tb3','tb4'])
 ]
]
titles=['Inspect EC2 launch and health evidence','Trace S3 object transfers','Publish and select workload metrics']
visuals=[ec2_visual,s3_visual,metric_visual]
out={k:p[k] for k in ['schema_version','path_id','batch_id']}; out['kind']='screens_part';out['tiles']=[]
for i,t in enumerate(p['tiles']):
 c=t['concept_ids'][0]
 tile={'tile_id':t['tile_id'],'title':titles[i],'steps':[],'remediation_steps':[]}
 for j,s in enumerate(t['steps']):
  title,content=texts[i][j]
  step={k:copy.deepcopy(s[k]) for k in ['step_id','type','concept_ids']}
  step.update(title=title,eyebrow={'explainer':'Inspect the model','check':'Quick check','hands_on':'Evidence review','recap':'Takeaways'}[s['type']],lineage={k:copy.deepcopy(s[k]) for k in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']})
  if s['type']=='explainer':
   step['blocks']=[prose(txt,c,fs,tbs, 'example' if j==1 else 'mechanism') for txt,fs,tbs in content]
   if j==0:step['blocks'].append(visuals[i](c))
  elif s['type'] in ['check','hands_on']:step['lede']=content
  else:
   facts=[f['id'] for f in bundles[c]['coverage']['required_facts']]
   step['blocks']=[prose(content,c,facts,[x['id'] for x in bundles[c]['teaching_blocks']],'takeaway')]
   if i<2:
    nextc=p['tiles'][i+1]['concept_ids'][0]
    first=bundles[nextc]['teaching_blocks'][0]['content']
    # Forward pointer only, not additional teaching of blocked future concepts.
    nexttext=['Next: identify an S3 object by bucket and key.','Next: match a workload metric’s complete identity.'][i]
   else:nexttext='Continue to '+t['next_tile_id']+'.'
   step['blocks'].append({'type':'up_next','title':('Up next: '+titles[i+1]) if i<2 else 'Up next: '+t['next_tile_id'],'text':nexttext})
  for k,block in enumerate(step.get('blocks',[]),1):block['block_id']=step['step_id']+'.b'+str(k).zfill(2)
  tile['steps'].append(step)
 for j,(title,txt,fs,tbs) in enumerate(remedies[i],1):
  sid=t['tile_id']+'.r'+str(j).zfill(2)
  # Each remedy is a short stand-alone contrast for the corresponding planned check/practice.
  if len(txt.split())>90:
   raise ValueError('Remediation prose exceeds 90 words')
  tile['remediation_steps'].append({'step_id':sid,'type':'remediation','required':False,'concept_ids':[c],'eyebrow':'Try the contrast','title':title,'blocks':[dict(prose(txt,c,fs,tbs,'misconception'),block_id=sid+'.b01')],'lineage':lin(c,fs,tbs)})
 out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
# Mistakes-to-avoid audit: exact plan, qualified lineage, standalone and bounded prose,
# planned visuals/alternate, registry-based examples, framing only, no typed outputs.
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
for tile,t in zip(out['tiles'],p['tiles']):
 assert len(tile['steps'])==len(t['steps'])
 for s,plan in zip(tile['steps'],t['steps']):
  for key in ['step_id','type','concept_ids']:assert s[key]==plan[key]
  for key in ['teaching_block_ids','fact_ids']:assert s['lineage'][key]==plan[key]
  if s['type'] in ['check','hands_on']:
   assert 'blocks' not in s and 'interaction' not in s
   if s['type']=='hands_on':assert not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit|README|ws\.)\b',s['title']+' '+s['lede'],re.I)
  else:
   # Budget counts all learner-facing prose plus visual annotations/labels/code.
   def words(x):
    if isinstance(x,dict):
     return sum(len(v.split()) if k in ['text','code','label','takeaway','left_label','right_label'] and isinstance(v,str) else sum(len(z.split()) for z in v) if k=='fields' else words(v) for k,v in x.items() if k not in ['lineage','alt_text','title'])
    if isinstance(x,list):return sum(words(v) for v in x)
    return 0
   count=words(s['blocks'])
   assert count<=plan['word_budget'],(s['step_id'],count,plan['word_budget'])
  for block in s.get('blocks',[]):
   if block['type'] in ['diagram','code_walkthrough','side_by_side']:assert t['concept_ids'][0]+'#visual' in block['lineage']['anchors']
 for obj in walk(tile):
  if obj.get('type')=='prose':
   assert 'lineage' in obj and len(obj['text'].split())<=90
  for key in ['fact_ids','teaching_block_ids']:
   if key in obj:assert all('#' in v for v in obj[key])
  assert 'output' not in obj and 'result' not in obj and 'computed_values' not in obj
assert 'video' not in json.dumps(out).lower()
print('Checklist passed:',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
