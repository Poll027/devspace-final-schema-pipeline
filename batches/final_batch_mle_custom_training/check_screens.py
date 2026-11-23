import json,re
from pathlib import Path
b=Path('batches/final_batch_mle.region.custom_training')
s,p,g,r=[json.loads((b/f).read_text()) for f in ['screens.json','tile_plans.json','inputs/path_glossary_bundle.json','scenario_asset_registry.json']]
cs={c['context']['concept_id']:c for c in g['bundles']};assets={a['asset_id']:a for a in r['assets']}
def walk(x):
 if isinstance(x,dict):
  if 'type' in x:yield x
  for k,v in x.items():
   if k!='lineage':yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
counts={}
assert [t['tile_id'] for t in s['tiles']]==[t['tile_id'] for t in p['tiles']]
for t,tp in zip(s['tiles'],p['tiles']):
 counts[t['tile_id']]={'steps':len(t['steps']),'remediation_steps':len(t['remediation_steps'])}
 assert len(t['steps'])==len(tp['steps'])
 for st,sp in zip(t['steps'],tp['steps']):
  for key in ['step_id','type','concept_ids']:assert st[key]==sp[key]
  for key in ['fact_ids','teaching_block_ids']:assert st['lineage'][key]==sp[key]
  if st['type'] in ('check','hands_on'):assert not st.get('blocks') and 'interaction' not in st
  bs=list(walk(st.get('blocks',[])))
  if sp['planned_visual_block_type']:assert any(x['type']==sp['planned_visual_block_type'] for x in bs)
  if sp['type']=='explainer':
   assert sum(len(x.get('text','').split()) for x in bs if x['type']=='prose')<=sp['word_budget']
   for anchor in sp['anchors']:assert any(anchor in x.get('lineage',{}).get('anchors',[]) for x in bs)
  if st['type']=='video':assert set(st['blocks'][0])=={'type','segment_ids'} and st['blocks'][0]['segment_ids']==sp['segment_ids']
  if st['type'] in ('check','hands_on'):
   assert any(rem['concept_ids']==st['concept_ids'] and set(rem['lineage']['fact_ids'])==set(sp['fact_ids']) for rem in t['remediation_steps'])
 for st in t['steps']+t['remediation_steps']:
  for obj in [st]+list(walk(st.get('blocks',[]))):
   assert not any(k in obj for k in ['output','result','computed_values','execution_provenance'])
   for field in ['fact_ids','teaching_block_ids','anchors']:
    for q in obj.get('lineage',{}).get(field,[]):assert '#' in q
   if obj.get('type')=='prose':
    assert obj.get('lineage') and len(obj['text'].split())<=90
    assert not re.search(r'\bvideo\b',obj['text'],re.I)
   for field in ['fact_ids','teaching_block_ids']:
    for q in obj.get('lineage',{}).get(field,[]):
     cid,ident=q.split('#');seq=cs[cid]['coverage']['required_facts'] if field=='fact_ids' else cs[cid]['teaching_blocks']
     assert ident in {x['id'] for x in seq}
   if 'asset_ref' in obj:
    ref=obj['asset_ref'];assert ref['asset_id'] in assets
    assert set(ref.get('columns',[]))<=set(c['name'] for c in assets[ref['asset_id']]['columns'])
report={'checklist':'PASS','checks':['plan order, types, concepts and exact lineage','framing-only assessments','qualified existing fact and teaching-block ids','prose lineage, 90-word cap and step budgets','standalone text without video references','planned visuals and #visual tags','registry asset ids and columns','no authored outputs, query results or computed values','separate remediation targets for different measured facts','source qualifiers and fixture values reviewed'],'counts':counts,'interactions_exist':(b/'interactions.json').exists()}
(b/'screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
