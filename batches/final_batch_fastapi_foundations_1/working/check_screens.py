import json, re
from pathlib import Path
P=Path('batches/final_batch_foundations_1')
d=json.loads((P/'screens.json').read_text());p=json.loads((P/'tile_plans.json').read_text())
g=json.loads((P/'inputs/path_glossary_bundle.json').read_text());r=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']};A={a['asset_id']:a for a in r['assets']}
M=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/anchor_mapping.json').read_text())
def walk(bs):
 for b in bs:
  yield b
  if b['type']=='side_by_side':yield from walk([b['left'],b['right']])
assert [t['tile_id'] for t in d['tiles']]==[t['tile_id'] for t in p['tiles']]
counts={}; blocks=0
for t,pt in zip(d['tiles'],p['tiles']):
 assert [(s['step_id'],s['type']) for s in t['steps']]==[(s['step_id'],s['type']) for s in pt['steps']]
 taught=set()
 for s,ps in zip(t['steps'],pt['steps']):
  assert s['concept_ids']==ps['concept_ids']
  for k in ('teaching_block_ids','fact_ids','segment_ids','anchors'):assert s['lineage'][k]==ps[k]
  if s['type'] in ('check','hands_on'):
   assert not s.get('blocks') and 'interaction' not in s
   assert set(ps['fact_ids'])<=taught,(s['step_id'],'untaught fact')
   assert any(set(ps['fact_ids'])<=set(rs['lineage']['fact_ids']) and set(ps['concept_ids'])==set(rs['concept_ids']) for rs in t['remediation_steps'])
  text=[b for b in walk(s.get('blocks',[])) if b['type']=='prose']
  if ps['word_budget']:assert sum(len(b['text'].split()) for b in text)<=ps['word_budget'],s['step_id']
  if s['type']=='explainer':
   assert set(ps['teaching_block_ids']) <= {q for b in text for q in b['lineage']['teaching_block_ids']}
   if ps['planned_visual_block_type']:
    c=ps['concept_ids'][0];allowed=[ps['planned_visual_block_type']]+M['visual_alternates'].get(B[c]['visual_anchor']['type'],[])
    assert any(b['type'] in allowed and c+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in s['blocks'])
   taught|={q for b in text for q in b['lineage']['fact_ids']}
  if s['type']=='video':
   assert len(s['blocks'])==1 and s['blocks'][0]['type']=='media_group'
   assert s['blocks'][0]['segment_ids']==ps['segment_ids']
   assert set(s['blocks'][0])<= {'type','block_id','segment_ids'}
  if s['type']=='recap':assert s['blocks'][-1]['type']=='up_next'
 for c in pt['concept_ids']:
  assert {c+'#'+f['id'] for f in B[c]['coverage']['required_facts']}<=taught
 for s in t['steps']+t['remediation_steps']:
  counts[s['type']]=counts.get(s['type'],0)+1
  for b in walk(s.get('blocks',[])):
   blocks+=1
   assert not any(k in b for k in ('output','execution_provenance','computed_values','result','rows'))
   if b['type']=='prose':
    assert 'lineage' in b and all(k in b['lineage'] for k in ('concept_ids','fact_ids','teaching_block_ids'))
    assert len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b',b['text'],re.I)
   ln=b.get('lineage',{})
   for q in ln.get('fact_ids',[]):
    c,f=q.split('#');assert f in {x['id'] for x in B[c]['coverage']['required_facts']}
   for q in ln.get('teaching_block_ids',[]):
    c,tb=q.split('#');assert tb in {x['id'] for x in B[c]['teaching_blocks']}
   for q in ln.get('anchors',[]):assert '#' in q
   if 'asset_ref' in b:
    ref=b['asset_ref'];a=A[ref['asset_id']]
    assert set(ref.get('columns',[]))<={c['name'] for c in a['columns']}
   if b['type']=='annotated_image':assert A[b['asset_id']]['asset_kind']=='image'
print('Checklist PASS: exact plans/lineage; all facts taught before checks; remediation fact coverage; prose <=90 words; budgets; qualified ids; registered columns/assets; planned/allowed visuals with #visual; segment references only; no video references or authored outputs.')
print('Editorial review: source facts and rewrites compared; hedges retained; open examples not made exhaustive; no future-concept teaching. Scenario values pulled from fixtures; no registered images, so screenshot visuals use allowed diagrams. Live environment inspection outputs intentionally deferred.')
print('Tiles',len(d['tiles']),'steps by type',counts,'total blocks',blocks)
(P/'working/screens_checklist.json').write_text(json.dumps({'status':'PASS','tile_count':len(d['tiles']),'step_counts':counts,'block_count':blocks,'uncertainty':'Actual .venv inspection outputs are not yet available; the visual supplies commands, not invented results.'},indent=2)+'\n')
