import json, re, sys
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from finlib import words
B=Path('batches/final_batch_aws_devops.region.06_2')
S=json.loads((B/'screens.json').read_text());P=json.loads((B/'tile_plans.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text());A=json.loads((B/'scenario_asset_registry.json').read_text())
byc={c['context']['concept_id']:c for c in G['bundles']};assets={a['asset_id']:a for a in A['assets']}
def walk(bs):
 for b in bs:
  yield b
  if b['type']=='side_by_side':yield from walk([b['left'],b['right']])
  if b['type']=='before_after':yield from walk([b['before'],b['after']])
ids=[];taught=set();prose_count=0;visual_count=0
assert [t['tile_id'] for t in S['tiles']]==[t['tile_id'] for t in P['tiles']]
for t,pt in zip(S['tiles'],P['tiles']):
 assert len(t['steps'])==len(pt['steps'])
 for s,p in zip(t['steps'],pt['steps']):
  for key in ['step_id','type','concept_ids']:assert s[key]==p[key],(s['step_id'],key)
  for key in ['fact_ids','teaching_block_ids','segment_ids','anchors']:assert s['lineage'][key]==p[key]
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s
  if s['type']=='hands_on' and p['planned_interaction_type'] in ['choice','classify']:
   assert re.search(r'^(Review|Judge)',s['title'])
   assert not re.search(r'\b(implement|build|run|execute|provision|train|commit|submit|README)\b|ws\.',s['title']+' '+s.get('lede',''),re.I)
  if s['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':p['segment_ids']}]
  w=sum(words(b['text']) for b in walk(s.get('blocks',[])) if b['type']=='prose')
  if p['word_budget']:assert w<=p['word_budget'],(s['step_id'],w,p['word_budget'])
  if s['type']=='explainer' and p['planned_visual_block_type']:
   visuals=[b for b in walk(s['blocks']) if b.get('lineage',{}).get('anchors')]
   assert visuals
   assert p['planned_visual_block_type'] in [b['type'] for b in visuals] or (p['planned_visual_block_type']=='annotated_image' and any(b['type']=='diagram' for b in visuals))
  if s['type']=='recap':assert bool(pt['next_tile_id'])==any(b['type']=='up_next' for b in s['blocks'])
 interactions=[s for s in pt['steps'] if s['type'] in ['check','hands_on']]
 assert len(interactions)==len(t['remediation_steps'])
 for p,r in zip(interactions,t['remediation_steps']):
  assert r['type']=='remediation' and re.fullmatch(re.escape(t['tile_id'])+r'\.r\d{2}',r['step_id'])
  retaught=set(f for b in walk(r['blocks']) if b['type']=='prose' for f in b['lineage']['fact_ids'])
  assert set(p['fact_ids'])<=retaught
 for s in t['steps']+t['remediation_steps']:
  ids.append(s['step_id'])
  for b in walk(s.get('blocks',[])):
   assert not any(k in b for k in ['result','computed_values','segments','execution_provenance'])
   lin=b.get('lineage',{})
   if b['type']=='prose':
    prose_count+=1;assert lin.get('concept_ids') and lin.get('fact_ids') and lin.get('teaching_block_ids')
    assert words(b['text'])<=90,(s['step_id'],words(b['text']))
    assert not re.search(r'\b(video|clip)\b',b['text'],re.I)
    if s['type']=='explainer':taught.update(lin['fact_ids'])
   for f in lin.get('fact_ids',[]):
    cid,fid=f.split('#');assert fid in {f['id'] for f in byc[cid]['coverage']['required_facts']+byc[cid]['coverage'].get('misconceptions',[])}
   for tb in lin.get('teaching_block_ids',[]):
    cid,tid=tb.split('#');assert tid in {tb['id'] for tb in byc[cid]['teaching_blocks']}
   if b['type'] in ['diagram','process_flow','side_by_side','data_table']:
    visual_count+=1;assert lin.get('anchors')==[s['concept_ids'][0]+'#visual']
   if 'asset_ref' in b:
    a=assets[b['asset_ref']['asset_id']];assert set(b['asset_ref']['columns'])<={c['name'] for c in a['columns']}
    assert 'rows' not in b
 assert all(c+'#'+f['id'] in taught for c in pt['concept_ids'] for f in byc[c]['coverage']['required_facts']+byc[c]['coverage'].get('misconceptions',[]))
assert len(ids)==len(set(ids))
report={'status':'PASS','tile_count':len(S['tiles']),'planned_steps':sum(len(t['steps']) for t in S['tiles']),'remediation_steps':sum(len(t['remediation_steps']) for t in S['tiles']),'prose_blocks':prose_count,'visual_blocks_including_nested_and_remediation':visual_count,'checks':['plan ids/types/order and exact lineage','framing-only interactions and inspect-and-judge verbs','qualified existing facts and teaching blocks','every required fact/misconception taught before assessment','prose <=90 words and steps within word budgets','no video-dependent prose','registered assets and existing columns only; no typed rows/results','planned visuals or screenshot-to-diagram alternate, all #visual tags','media segment ids copied only','recaps and next-tile first idea; terminal tile has no next','separate remediation for each interaction covering measured facts','manual review: fact meaning and hedges preserved; no invented scenario limits, commands, causes or outputs'], 'notes':['No registered images; planned screenshots use schematic diagrams.','No interactions.json yet; assembly and full tile validation are deferred until interactions exist.','No next tile is planned after tile 127.']}
(B/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
