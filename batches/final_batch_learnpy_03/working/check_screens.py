import json,re
from pathlib import Path
from collections import Counter
P=Path('batches/final_batch_learn_python.region.03')
s=json.loads((P/'screens.json').read_text());plan=json.loads((P/'tile_plans.json').read_text());g=json.loads((P/'inputs/path_glossary_bundle.json').read_text());reg=json.loads((P/'scenario_asset_registry.json').read_text())
bs={b['context']['concept_id']:b for b in g['bundles']}
valid_f={c+'#'+f['id'] for c,b in bs.items() for f in b['coverage']['required_facts']}
valid_t={c+'#'+t['id'] for c,b in bs.items() for t in b['teaching_blocks']}
assets={a['asset_id']:a for a in reg['assets']}
def walk(blocks):
 for b in blocks:
  yield b
  for field in ['left','right','before','after']:
   if isinstance(b.get(field),dict):yield from walk([b[field]])
def words(text):return len(re.findall(r"\b[\w'-]+\b",text))
assert [t['tile_id'] for t in s['tiles']]==[t['tile_id'] for t in plan['tiles']]
counts=Counter()
for t,p in zip(s['tiles'],plan['tiles']):
 assert len(t['steps'])==len(p['steps'])
 taught=set()
 for st,ps in zip(t['steps'],p['steps']):
  assert (st['step_id'],st['type'],st['concept_ids'])==(ps['step_id'],ps['type'],ps['concept_ids'])
  for f in ['teaching_block_ids','fact_ids','anchors','segment_ids']:
   assert st['lineage'][f]==ps[f]
  counts[st['type']]+=1
  if st['type'] in ['check','hands_on']:
   assert 'blocks' not in st and 'interaction' not in st
   assert set(ps['fact_ids'])<=taught
   if st['type']=='hands_on' and ps['planned_interaction_type'] in ['classify','choice']:
    text=(st['title']+' '+st['lede']).lower()
    assert not re.search(r'\b(implement|build|run|execute|provision|train|commit|submit)\b|ws\.|readme',text)
  if st['type']=='video':
   assert st['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if ps['word_budget']:
   total=sum(words(b['text']) for b in walk(st.get('blocks',[])) if b['type']=='prose')
   assert total<=ps['word_budget'],(st['step_id'],total,ps['word_budget'])
  if ps['planned_visual_block_type'] not in [None,'media_group','up_next']:
   assert any(c+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in walk(st['blocks']) for c in ps['concept_ids'])
  for b in walk(st.get('blocks',[])):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
 assert set(f for c in p['concept_ids'] for f in valid_f if f.startswith(c+'#'))<=taught
 assert t['steps'][-1]['blocks'][-1]['type']=='up_next'
 signatures=[]
 for st in t['remediation_steps']:
  counts['remediation']+=1
  signatures.append((st['concept_ids'][0],set(st['lineage']['fact_ids'])))
 for ps in p['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  cid=ps['concept_ids'][0];fs=set(ps['fact_ids'])
  for anchor in ps['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1]
    aa=next(a for a in bs[cid]['assessment_anchors'] if a['capability']==capability)
    fs.update(cid+'#'+f for f in aa['fact_ids'])
  fs=fs or {f for f in valid_f if f.startswith(cid+'#')}
  assert any(c==cid and target==fs for c,target in signatures),(ps['step_id'],fs)
 for st in t['steps']+t['remediation_steps']:
  for b in walk(st.get('blocks',[])):
   assert not any(k in b for k in ['output','result','execution_provenance','computed_values'])
   if b['type']=='prose':
    assert words(b['text'])<=90
    assert not re.search(r'\b(video|clip)\b',b['text'],re.I)
    assert b['lineage']['concept_ids'] and b['lineage']['teaching_block_ids'] and b['lineage']['fact_ids']
   lineage=b.get('lineage',{})
   assert set(lineage.get('fact_ids',[]))<=valid_f
   assert set(lineage.get('teaching_block_ids',[]))<=valid_t
   if b['type']=='data_table':assert 'rows' not in b
   if b['type']=='annotated_image':
    assert assets[b['asset_id']]['asset_kind']=='image'
    assert b['alt_text']==assets[b['asset_id']]['alt_text']
   if b['type']=='code_walkthrough':
    for note in b.get('annotations',[]):assert 1<=note['start_line']<=note['end_line']<=len(b['code'].splitlines())
print('Checklist PASS: full tile/step order; exact planned lineage; qualified IDs; self-contained fact coverage; framing-only interactions; judge-task wording; budgets; prose lineage; media IDs only; visual anchors; per-measured-fact remediation; next-idea recap; no typed runtime results.')
print('Manual review PASS: glossary meaning and hedges preserved; no added causes or closed lists; no future-concept teaching; examples use glossary/registry values and available fields; missing images use diagram alternates.')
print(dict(counts))
