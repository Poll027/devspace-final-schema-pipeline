import json,re
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle')
p=json.loads((B/'tile_plans.json').read_text());o=json.loads((B/'screens.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
G={x['context']['concept_id']:x for x in g['bundles']};A={x['asset_id']:x for x in r['assets']}
facts={c+'#'+f['id'] for c,x in G.items() for f in x['coverage']['required_facts']};tbs={c+'#'+tb['id'] for c,x in G.items() for tb in x['teaching_blocks']}
def visit(block):
 yield block
 for key in ['left','right','before','after']:
  if key in block:yield from visit(block[key])
assert [x['tile_id'] for x in p['tiles']]==[x['tile_id'] for x in o['tiles']]
prose_count=0;visual_count=0
for pt,ot in zip(p['tiles'],o['tiles']):
 assert len(pt['steps'])==len(ot['steps'])
 for ps,s in zip(pt['steps'],ot['steps']):
  for k in ['step_id','type','concept_ids']:assert ps[k]==s[k],(s['step_id'],k)
  for k in ['teaching_block_ids','fact_ids']:assert ps[k]==s['lineage'][k],(s['step_id'],k)
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s and 'interaction' not in s
  word_count=sum(len(x.get('text','').split()) for x in s.get('blocks',[]) if x['type'] in ['prose','up_next'])
  assert word_count<=ps['word_budget'],(s['step_id'],word_count,ps['word_budget'])
  if ps['planned_visual_block_type'] and ps['planned_visual_block_type']!='up_next':
   assert any(c+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in s['blocks'] for c in s['concept_ids'])
 for s in ot['steps']+ot['remediation_steps']:
  assert set(s['lineage']['fact_ids'])<=facts
  assert set(s['lineage']['teaching_block_ids'])<=tbs
  for top in s.get('blocks',[]):
   for b in visit(top):
    if b['type']=='up_next':continue # This schema does not allow lineage.
    assert 'lineage' in b,(s['step_id'],b['type'])
    assert set(b['lineage']['fact_ids'])<=facts
    assert set(b['lineage']['teaching_block_ids'])<=tbs
    if b['type']=='prose':
     prose_count+=1;assert len(b['text'].split())<=90,(s['step_id'],len(b['text'].split()))
     assert b['lineage']['teaching_block_ids']
     assert not re.search(r'\bvideo\b',b['text'],re.I)
    else:
     visual_count+=1
     assert all(c+'#visual' in b['lineage'].get('anchors',[]) for c in b['lineage']['concept_ids'])
    assert not any(k in b for k in ['output','result','computed_values','execution_provenance'])
    if 'asset_ref' in b:
     ref=b['asset_ref'];asset=A[ref['asset_id']]
     if ref.get('variant_id'):assert ref['variant_id'] in [x['variant_id'] for x in asset.get('variants',[])]
     if ref.get('columns'):assert set(ref['columns'])<=set(x['name'] for x in asset['columns'])
 for ps in pt['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  matching=[s for s in ot['remediation_steps'] if s['concept_ids']==ps['concept_ids'] and s['lineage']['fact_ids']==ps['fact_ids']]
  assert matching,ps['step_id']
  taught={fid for b in matching[0]['blocks'] if b['type']=='prose' for fid in b['lineage']['fact_ids']}
  assert set(ps['fact_ids'])<=taught,(ps['step_id'],'remediation coverage')
report={'passed':True,'tiles':len(o['tiles']),'planned_steps':sum(len(t['steps']) for t in o['tiles']),'remediation_steps':sum(len(t['remediation_steps']) for t in o['tiles']),'prose_blocks':prose_count,'visual_blocks_including_nested':visual_count,'checks':['plan step IDs/types/order/concepts and exact planned lineage','qualified glossary fact and teaching-block IDs','prose lineage and 90-word limit','step text budgets','no interaction payload on framing-only steps','visual anchor tags','registered dataset/variant/column references','no video mentions in prose','no typed execution outputs','separate remediation coverage for each measured fact set'],'manual_review':['Paraphrases retain fatal failure boundaries, protected-test restriction and safe-loading limitation.','Numerical tolerances, identities and hashes in visual source specifications were copied by script from registered assets.','No registered image exists; dataset-gate visual uses the permitted diagram fallback.','Execution-dependent visual results are not authored as outcomes; displayed panels are explicitly fixture specifications.']}
(B/'screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
