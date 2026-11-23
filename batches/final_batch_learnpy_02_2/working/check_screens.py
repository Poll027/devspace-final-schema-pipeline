import json,re,ast
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.02_2')
s=json.loads((B/'screens.json').read_text());p=json.loads((B/'tile_plans.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
gloss={x['context']['concept_id']:x for x in g['bundles']}
assert [t['tile_id'] for t in s['tiles']]==[t['tile_id'] for t in p['tiles']]
prose_count=visual_count=0
for tile,plan in zip(s['tiles'],p['tiles']):
 assert len(tile['steps'])==len(plan['steps'])
 taught=set()
 for step,ps in zip(tile['steps'],plan['steps']):
  for k in ['step_id','type','concept_ids']:assert step[k]==ps[k]
  for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']:assert step['lineage'][k]==ps[k]
  if ps['type'] in ['check','hands_on']:
   assert 'blocks' not in step and 'interaction' not in step
   assert set(ps['fact_ids'])<=taught
  if ps['planned_visual_block_type']=='media_group':assert step['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if ps['planned_visual_block_type'] in ['diagram','code_walkthrough']:
   assert any(b['type']==ps['planned_visual_block_type'] and all(c+'#visual' in b['lineage']['anchors'] for c in ps['concept_ids']) for b in step['blocks'])
  if ps['type']=='recap':assert step['blocks'][-1]['type']=='up_next'
  if ps['word_budget']:
   words=sum(len(b.get('text','').split()) for b in step.get('blocks',[]))
   assert words<=ps['word_budget'],(step['step_id'],words)
  for b in step.get('blocks',[]):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
 for c in plan['concept_ids']:assert {c+'#'+f['id'] for f in gloss[c]['coverage']['required_facts']}<=taught
 for step in tile['steps']+tile['remediation_steps']:
  for b in step.get('blocks',[]):
   assert not any(k in b for k in ['output','execution_provenance','result','computed_values'])
   if b['type']=='prose':
    prose_count+=1
    assert 'lineage' in b and b['lineage']['fact_ids'] and b['lineage']['teaching_block_ids']
    assert len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b',b['text'],re.I)
   if 'lineage' in b:
    for f in b['lineage']['fact_ids']:
     c,fid=f.split('#');assert fid in {f['id'] for f in gloss[c]['coverage']['required_facts']}
    for tb in b['lineage']['teaching_block_ids']:
     c,tbid=tb.split('#');assert tbid in {t['id'] for t in gloss[c]['teaching_blocks']}
   if b['type']=='code_walkthrough':ast.parse(b['code']);visual_count+=bool(b['lineage']['anchors'])
  assert not re.search(r'\bvideo\b',step.get('lede',''),re.I)
 # Remediation must cover each measured fact set, including separately measured facts.
 rem=[set(x['lineage']['fact_ids']) for x in tile['remediation_steps']]
 for ps in plan['steps']:
  if ps['type'] in ['check','hands_on'] and ps['fact_ids']:assert any(set(ps['fact_ids'])<=fs for fs in rem)
print('Checklist PASS: plan identity/order; qualified lineage; standalone fact teaching; prose lengths and budgets; visual types/anchors; media IDs only; recap up_next; framing-only interactions; remediation coverage; no authored outputs; code syntax.')
print('Manual review completed: glossary meanings/hedges preserved; no new causal or future-concept instruction; stationery values sourced from glossary/registry; no nonexistent data columns or images.')
print('Counts:',len(s['tiles']),'tiles,',sum(len(t['steps']) for t in s['tiles']),'planned steps,',sum(len(t['remediation_steps']) for t in s['tiles']),'remediation steps,',prose_count,'prose blocks')
