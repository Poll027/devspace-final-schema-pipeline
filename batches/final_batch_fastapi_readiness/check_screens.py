import json,re,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers.sandbox import run_query
P=Path('batches/final_batch_readiness')
S=json.loads((P/'screens.json').read_text());R=json.loads((P/'scenario_asset_registry.json').read_text());G=json.loads((P/'inputs/path_glossary_bundle.json').read_text());PL=json.loads((P/'tile_plans.json').read_text())
B={b['context']['concept_id']:b for b in G['bundles']};A={a['asset_id']:a for a in R['assets']}
def blocks(xs):
 for b in xs:
  yield b
  for k in ['left','right','before','after']:
   if k in b:yield from blocks([b[k]])
assert len(S['tiles'])==len(PL['tiles'])
counts=[];queries=[]
for t,pt in zip(S['tiles'],PL['tiles']):
 assert t['tile_id']==pt['tile_id'] and len(t['steps'])==len(pt['steps'])
 taught=set()
 for st,ps in zip(t['steps'],pt['steps']):
  for k in ['step_id','type','concept_ids']:assert st[k]==ps[k]
  for k in ['fact_ids','teaching_block_ids']:assert st['lineage'][k]==ps[k]
  if st['type'] in ['check','hands_on']:
   assert not st.get('blocks') and 'interaction' not in st
   assert set(ps['fact_ids'])<=taught
  else:
   n=sum(len(b.get('text','').split()) for b in blocks(st['blocks']) if b['type']=='prose')
   assert n<=ps['word_budget'],(st['step_id'],n,ps['word_budget'])
  for b in blocks(st.get('blocks',[])):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
  if ps['planned_visual_block_type'] and st['type']=='explainer':
   assert any(b['type']==ps['planned_visual_block_type'] and ps['concept_ids'][0]+'#visual' in b['lineage']['anchors'] for b in st['blocks'])
 for c in pt['concept_ids']:assert {c+'#'+x['id'] for x in B[c]['coverage']['required_facts']}<=taught
 for st in t['steps']+t['remediation_steps']:
  for b in blocks(st.get('blocks',[])):
   if b['type']=='prose':
    assert len(b['text'].split())<=90 and b['lineage']['teaching_block_ids'] and b['lineage']['fact_ids']
    assert not re.search(r'\bvideo\b',b['text'],re.I)
   for fid in b.get('lineage',{}).get('fact_ids',[]):
    c,f=fid.split('#');assert f in {x['id'] for x in B[c]['coverage']['required_facts']}
   for tbid in b.get('lineage',{}).get('teaching_block_ids',[]):
    c,tb=tbid.split('#');assert tb in {x['id'] for x in B[c]['teaching_blocks']}
   if st['type']=='explainer':
    assert set(b.get('lineage',{}).get('concept_ids',[]))<=set(st['concept_ids'])
   if 'asset_ref' in b:
    a=A[b['asset_ref']['asset_id']];assert set(b['asset_ref'].get('columns',[]))<=set(x['name'] for x in a['columns'])
   assert 'result' not in b and 'output' not in b and 'computed_values' not in b
   if 'result_of' in b:
    assert 'asset_ref' not in b
    result,problems=run_query(R,b['result_of']);assert not problems,problems
    queries.append({'step_id':st['step_id'],'computed_row_count':len(result['rows'])})
 for st in pt['steps']:
  if st['type'] in ['check','hands_on']:
   assert any(set(st['fact_ids'])<=set(f for b in rr['blocks'] if b['type']=='prose' for f in b['lineage']['fact_ids']) for rr in t['remediation_steps'])
 counts.append({'tile_id':t['tile_id'],'planned_steps':len(t['steps']),'remediation_steps':len(t['remediation_steps'])})
print('Mistakes-to-avoid checklist PASS: exact plan/order/lineage; framing-only checks/practice; full required-fact text coverage before assessment; qualified fact and teaching-block IDs; prose lineage; standalone wording; per-prose and per-step word limits; registered assets/columns; visual type and anchor coverage; query execution; no authored results; measured-fact remediation coverage.')
print('Query execution checks:',queries)
print('Counts:',counts)
