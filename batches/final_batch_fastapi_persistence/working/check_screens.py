import json,re
from pathlib import Path
B=Path('batches/final_batch_persistence')
o=json.loads((B/'screens.json').read_text());p=json.loads((B/'tile_plans.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());a=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in g['bundles']}; assets={x['asset_id']:x for x in a['assets']}
assert [t['tile_id'] for t in o['tiles']]==[t['tile_id'] for t in p['tiles']]
def descend(block):
 yield block
 for key in ('left','right','before','after'):
  if isinstance(block.get(key),dict):yield from descend(block[key])
def lineage(L):
 for key,tag in [('fact_ids','f'),('teaching_block_ids','tb')]:
  for q in L.get(key,[]):
   cid,sep,local=q.partition('#');assert sep and cid in bundles
   bank=bundles[cid]['coverage']['required_facts'] if tag=='f' else bundles[cid]['teaching_blocks']
   assert local in {b['id'] for b in bank}
for t,pt in zip(o['tiles'],p['tiles']):
 assert len(t['steps'])==len(pt['steps'])
 taught=set()
 for s,ps in zip(t['steps'],pt['steps']):
  assert (s['step_id'],s['type'],s['concept_ids'])==(ps['step_id'],ps['type'],ps['concept_ids'])
  for key in ('fact_ids','teaching_block_ids'):assert s['lineage'][key]==ps[key]
  if s['type'] in ('check','hands_on'):
   assert 'blocks' not in s and 'interaction' not in s
   assert set(ps['fact_ids'])<=taught
   assert any(set(ps['fact_ids'])<=set(r['lineage']['fact_ids']) for r in t['remediation_steps'] if r['concept_ids']==s['concept_ids'])
  if s['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  text=[b['text'] for root in s.get('blocks',[]) for b in descend(root) if b['type']=='prose']
  if ps['word_budget']:assert sum(len(x.split()) for x in text)<=ps['word_budget'],s['step_id']
  if s['type']=='explainer':
   for root in s['blocks']:
    for b in descend(root):
     if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
  if ps['planned_visual_block_type'] and s['type']=='explainer':
   allowed={ps['planned_visual_block_type']}
   if ps['planned_visual_block_type']=='annotated_image':allowed.add('diagram')
   visuals=[b for b in s['blocks'] if b['type'] in allowed]
   assert visuals,s['step_id']
   for b in visuals:assert ps['concept_ids'][0]+'#visual' in b['lineage']['anchors']
 assert all(any(b['type']=='up_next' for b in s.get('blocks',[])) for s in t['steps'] if s['type']=='recap')
 for s in t['steps']+t['remediation_steps']:
  lineage(s['lineage'])
  for root in s.get('blocks',[]):
   for b in descend(root):
    if b['type']=='prose':
     assert b.get('lineage') and b['lineage']['fact_ids'] and b['lineage']['teaching_block_ids']
     assert len(b['text'].split())<=90
     assert not re.search(r'\bvideo\b',b['text'],re.I)
    if 'lineage' in b:lineage(b['lineage'])
    assert not set(b)&{'output','result','computed_values','execution_provenance','segments','bridge'}
    if 'asset_ref' in b:
     ref=b['asset_ref'];assert ref['asset_id'] in assets
     assert set(ref.get('columns',[]))<={c['name'] for c in assets[ref['asset_id']]['columns']}
    if 'result_of' in b:
     assert 'asset_ref' not in b
     for m in b['result_of']['asset_mounts']:assert m['asset_id'] in assets
# Human semantic checklist was also applied to the templates: every re-voice preserves the source
# hedge, open list, and stated boundary; fixture labels and numbers come from contracts/assets;
# data query outputs remain result_of; image-free creation uses the permitted diagram fallback.
print('PASS: plan/order/lineage; facts taught before measurement; measured-fact remediation; budgets; qualified IDs; text lineage; visual anchors; registry columns; media IDs; no authored outputs; recap navigation.')
print('Tiles:',len(o['tiles']),'planned steps:',sum(len(t['steps']) for t in o['tiles']),'remediation steps:',sum(len(t['remediation_steps']) for t in o['tiles']))
print('Blocks:',sum(1 for t in o['tiles'] for s in t['steps']+t['remediation_steps'] for root in s.get('blocks',[]) for b in descend(root)))
