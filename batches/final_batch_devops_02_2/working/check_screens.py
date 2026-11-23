import json,re
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.02_2')
o=json.loads((B/'screens.json').read_text());p=json.loads((B/'tile_plans.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']};assets={x['asset_id']:x for x in r['assets']}
def walk(blocks):
 for x in blocks:
  yield x
  for k in ['left','right','before','after']:
   if isinstance(x.get(k),dict):yield from walk([x[k]])
assert [x['tile_id'] for x in o['tiles']]==[x['tile_id'] for x in p['tiles']]
blocks=proses=0
for t,pt in zip(o['tiles'],p['tiles']):
 c=pt['concept_ids'][0];b=bundles[c]
 known_tb={c+'#'+x['id'] for x in b['teaching_blocks']}
 known_f={c+'#'+f for x in b['teaching_blocks'] for f in x['fact_ids']}
 assert len(t['steps'])==len(pt['steps'])
 for st,ps in zip(t['steps'],pt['steps']):
  assert (st['step_id'],st['type'],st['concept_ids'])==(ps['step_id'],ps['type'],ps['concept_ids'])
  for k in ['concept_ids','fact_ids','teaching_block_ids','segment_ids','anchors']:assert st['lineage'][k]==ps[k]
  if st['type'] in ['check','hands_on']:assert 'blocks' not in st and 'interaction' not in st
  if st['type']=='hands_on' and ps['planned_interaction_type'] in ['choice','classify']:
   assert st['title'].startswith(('Review','Judge'))
   assert 'supplied' in st['lede'] and 'in this step' in st['lede']
   assert not re.search(r'\b(implement|build|run|execute|provision|train|commit|submit|README|ws\.)\b',st['title']+' '+st['lede'],re.I)
  if st['type']=='explainer':
   bs=list(walk(st['blocks']))
   assert set(ps['teaching_block_ids'])<=set(f for x in bs if x['type']=='prose' for f in x['lineage']['teaching_block_ids'])
   assert set(ps['fact_ids'])<=set(f for x in bs if x['type']=='prose' for f in x['lineage']['fact_ids'])
   if ps['anchors']:assert any(c+'#visual' in x.get('lineage',{}).get('anchors',[]) for x in bs)
  if st['type']=='video':assert st['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if st['type']=='recap':assert st['blocks'][-1]['type']=='up_next'
  words=sum(len(x['text'].split()) for x in walk(st.get('blocks',[])) if x['type']=='prose')
  if ps['word_budget']:assert words<=ps['word_budget'],(st['step_id'],words,ps['word_budget'])
 for st in t['steps']+t['remediation_steps']:
  for x in walk(st.get('blocks',[])):
   blocks+=1
   assert not any(k in x for k in ['output','computed_values','execution_provenance','result','rows'])
   if 'lineage' in x:
    assert set(x['lineage']['fact_ids'])<=known_f
    assert set(x['lineage']['teaching_block_ids'])<=known_tb
    assert all('#' in f for f in x['lineage']['fact_ids']+x['lineage']['teaching_block_ids'])
   if x['type']=='prose':
    proses+=1
    assert x['lineage']['concept_ids']==[c] and x['lineage']['fact_ids'] and x['lineage']['teaching_block_ids']
    assert len(x['text'].split())<=90
    assert not re.search(r'\b(video|clip|watch|as shown)\b',x['text'],re.I)
    for future in b['context']['blocked_future_concepts']:
     name=g['names'].get(future,'')
     if name:assert name.lower() not in x['text'].lower()
   if 'asset_ref' in x:
    a=assets[x['asset_ref']['asset_id']]
    assert set(x['asset_ref'].get('columns') or [])<=set(y['name'] for y in a['columns'])
   if x['type']=='diagram':
    ids={n['id'] for n in x['nodes']}; assert all(e['from'] in ids and e['to'] in ids for e in x.get('edges',[]))
 checks=[s for s in pt['steps'] if s['type'] in ['check','hands_on']]
 assert len(t['remediation_steps'])==len(checks)
 for st,check in zip(t['remediation_steps'],checks):
  taught={f for x in st['blocks'] if x['type']=='prose' for f in x['lineage']['fact_ids']}
  assert set(check['fact_ids'])<=taught
print('PASS mistakes-to-avoid checklist: plan/order/lineage, qualified ids, prose lineage and budgets, no video dependencies or future teaching, registered asset columns, visual anchors, media-only segment ids, computed-output exclusion, and measured-fact remediation coverage.')
print('Counts:',len(o['tiles']),'tiles;',sum(len(t['steps']) for t in o['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in o['tiles']),'remediations;',blocks,'blocks;',proses,'prose blocks')
print('Content review: scenario values and exact HCL are copied/generated from registered evidence; cross-account generally and all security-group boundaries retained. No registered images; diagram fallbacks used. HCL is presented as labelled syntax and prose because the code_walkthrough schema has no HCL language.')
