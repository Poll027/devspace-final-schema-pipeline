import json,re,collections
from pathlib import Path
B=Path('batches/final_batch_mle.region.custom_training')
S=json.load(open(B/'screens.json'));P=json.load(open(B/'tile_plans.json'));G=json.load(open(B/'inputs/path_glossary_bundle.json'));R=json.load(open(B/'scenario_asset_registry.json'))
C={b['context']['concept_id']:b for b in G['bundles']};assets={a['asset_id']:a for a in R['assets']}
issues=[];missing=[];counts=collections.Counter();nprose=0

def walk(b):
 yield b
 for k in ('before','after','left','right'):
  if isinstance(b.get(k),dict):yield from walk(b[k])

def verify(s):
 global nprose
 for root in s.get('blocks',[]):
  for b in walk(root):
   assert not any(k in b for k in ['output','execution_provenance','result','computed_values']),s['step_id']
   if b['type']=='media_group':assert set(b)=={'type','segment_ids'};continue
   if b['type']=='up_next':continue
   assert 'lineage' in b,s['step_id']
   lin=b['lineage']
   for field,key in [('fact_ids','coverage'),('teaching_block_ids','teaching_blocks')]:
    for q in lin.get(field,[]):
     assert '#' in q,q
     c,k=q.split('#',1)
     allowed={x['id'] for x in (C[c]['coverage']['required_facts'] if field=='fact_ids' else C[c]['teaching_blocks'])}
     assert k in allowed,q
   if b['type']=='prose':
    nprose+=1
    assert len(b['text'].split())<=90,(s['step_id'],len(b['text'].split()))
    assert not re.search(r'\bvideo\b',b['text'],re.I),s['step_id']
   else:
    assert any(a.endswith('#visual') for a in lin.get('anchors',[])),s['step_id']
   if b['type']=='annotated_image':assert b['alt_text']==assets[b['asset_id']]['alt_text']
   if b['type']=='data_table':assert 'rows' not in b

for st,pt in zip(S['tiles'],P['tiles']):
 assert st['tile_id']==pt['tile_id']
 assert len(st['steps'])==len(pt['steps'])
 for s,p in zip(st['steps'],pt['steps']):
  counts[s['type']]+=1
  for k in ['step_id','type','concept_ids']:assert s[k]==p[k]
  for k in ['fact_ids','teaching_block_ids']:assert s['lineage'][k]==p[k]
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s and 'interaction' not in s
  elif s['type']=='explainer':
   wordcount=sum(len(b['text'].split()) for b in s['blocks'] if b['type']=='prose')
   assert wordcount<=p['word_budget'],(s['step_id'],wordcount,p['word_budget'])
   wanted=p['planned_visual_block_type']
   if wanted:
    got={b['type'] for b in s['blocks']}
    if wanted not in got:missing.append({'step_id':s['step_id'],'planned':wanted,'actual':sorted(got),'reason':'No registered dataset asset supports the planned batch-size table. Schematic only; no fabricated rows or measurements.'})
  verify(s)
 for r in st['remediation_steps']:counts['remediation']+=1;verify(r)
 # Every first check / hands-on fact set has its own retry teaching.
 for p in pt['steps']:
  if p['type'] in ('check','hands_on'):
   assert any(r['concept_ids']==p['concept_ids'] and set(r['lineage']['fact_ids'])==set(p['fact_ids']) for r in st['remediation_steps']),p['step_id']
report={'tiles':len(S['tiles']),'step_counts':dict(counts),'prose_blocks_checked':nprose,'mistakes_checklist':{'qualified_ids_and_existing_facts':'PASS','text_lineage':'PASS','no_video_references':'PASS','source_fixture_values':'Source copied by script; no output/peak/row values fabricated','step_and_prose_word_budgets':'PASS','planned_order_type_and_lineage':'PASS','visual_anchor_tags':'PASS','data_asset_integrity':'No dataset or column invented','computed_output_absence':'PASS','registered_image_alt_text':'PASS','paraphrase_meaning':'Reviewed against source facts; preserves conditional SGD, dropout randomness, memory scope, patience and leakage restrictions'},'unresolved_visual_requirements':missing}
(B/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
