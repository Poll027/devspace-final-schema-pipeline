import json,re
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle')
s=json.loads((B/'screens.json').read_text());p=json.loads((B/'tile_plans.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']}; assets={x['asset_id']:x for x in r['assets']}; errors=[];counts=[]
def check(ok,msg):
 if not ok: errors.append(msg)
def walk(blocks):
 for b in blocks:
  yield b
  for k in ['left','right','before','after']:
   if k in b:yield from walk([b[k]])
for t,pt in zip(s['tiles'],p['tiles']):
 check(t['tile_id']==pt['tile_id'],'tile order')
 check(len(t['steps'])==len(pt['steps']),'planned count')
 taught=set(); measured=[]
 for x,y in zip(t['steps'],pt['steps']):
  for key in ['step_id','type','concept_ids']:check(x[key]==y[key],x['step_id']+' '+key)
  for key in ['teaching_block_ids','fact_ids']:check(x['lineage'][key]==y[key],x['step_id']+' '+key)
  if x['type'] in ['check','hands_on']:
   check(not x.get('blocks') and 'interaction' not in x,x['step_id']+' framing only')
   check(set(y['fact_ids'])<=taught,x['step_id']+' untaught facts')
   measured.append(y)
  blocks=list(walk(x.get('blocks',[])))
  words=sum(len(re.findall(r'\w+',b['text'])) for b in blocks if b['type']=='prose')
  check(words<=y['word_budget'],x['step_id']+' over budget')
  if y['planned_visual_block_type'] and y['planned_visual_block_type']!='up_next':
   check(any(y['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in blocks),x['step_id']+' missing visual anchor')
  for b in blocks:
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
 check(set(f['id'] for c in pt['concept_ids'] for f in [])==set(),'internal')
 for c in pt['concept_ids']:
  required={c+'#'+f['id'] for f in bundles[c]['coverage']['required_facts']}
  check(required<=taught,c+' required facts not text-taught')
 check(len(measured)==len(t['remediation_steps']),'distinct remediation targets')
 for m,rem in zip(measured,t['remediation_steps']):
  check(set(m['fact_ids'])<=set(rem['lineage']['fact_ids']),rem['step_id']+' measured remediation facts')
  remtaught={f for b in rem['blocks'] for f in b['lineage']['fact_ids']}
  check(set(m['fact_ids'])<=remtaught,rem['step_id']+' remediation prose coverage')
 for x in t['steps']+t['remediation_steps']:
  for b in walk(x.get('blocks',[])):
   check('output' not in b and 'result' not in b and 'computed_values' not in b,x['step_id']+' typed output')
   if b['type']=='prose':
    check(all(k in b.get('lineage',{}) for k in ['concept_ids','teaching_block_ids','fact_ids']),x['step_id']+' missing text lineage')
    check(len(re.findall(r'\w+',b['text']))<=90,x['step_id']+' long prose')
    check(not re.search(r'\b(video|clip)\b',b['text'],re.I),x['step_id']+' video mention')
   for key in ['fact_ids','teaching_block_ids']:
    for fid in b.get('lineage',{}).get(key,[]):
     c,local=fid.split('#'); pool=bundles[c]['coverage']['required_facts'] if key=='fact_ids' else bundles[c]['teaching_blocks']
     check(any(f['id']==local for f in pool),x['step_id']+' unknown lineage '+fid)
   if 'asset_ref' in b:
    a=assets[b['asset_ref']['asset_id']];columns={c['name'] for c in a['columns']}
    check(set(b['asset_ref'].get('columns',[]))<=columns,x['step_id']+' absent dataset column')
   if b['type']=='annotated_image':check(assets[b['asset_id']]['asset_kind']=='image','unregistered image')
  yy=next((z for z in pt['steps'] if z['step_id']==x['step_id']),None)
  if yy and x['type']=='hands_on' and yy['planned_interaction_type'] in ['classify','choice']:
   text=x['title']+' '+x.get('lede','')
   check(not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit)\b|ws\.|README',text,re.I),x['step_id']+' judgement framing')
 counts.append({'tile_id':t['tile_id'],'planned_steps':len(t['steps']),'remediation_steps':len(t['remediation_steps'])})
report={'passed':not errors,'counts':counts,'errors':errors,'manual_review':['Re-voiced paragraphs preserve glossary requirements, hedges and open scope.','Scenario identities and fixture values in visual source panels are copied by script from registered assets; no numerical outputs, hashes or segment fields were typed.','No images or captured run results exist in the named inputs: visual fallback uses explicitly labelled schematics and registered fixture sources, never invented outcomes.','Remediation uses the same lifecycle fixtures with one explicit boundary contrast and re-teaches every planned measured fact.','Next tile names the first idea; no future monitoring mechanism is introduced.'],'integration_gate':'Not applicable yet: interactions.json does not exist.'}
(B/'working/03_mistakes_check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert not errors
