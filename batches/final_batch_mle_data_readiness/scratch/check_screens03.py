import json,copy,ast,re,collections
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
S=json.loads((B/'screens.json').read_text()); P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); A=json.loads((B/'scenario_asset_registry.json').read_text())
assets={x['asset_id']:x for x in A['assets']}; bundles={b['context']['concept_id']:b for b in G['bundles']}
def blocks(block):
 yield block
 for k in ['before','after','left','right']:
  if k in block:yield from blocks(block[k])
def words(block):
 n=0
 for k,v in block.items():
  if k in ['code','lineage','result_of','asset_ref']:continue
  if k in ['text','title','takeaway','change_summary','left_label','right_label']:n+=len(v.split())
  if isinstance(v,dict):n+=words(v)
  if isinstance(v,list):
   for item in v:
    if isinstance(item,dict):n+=words(item)
 return n
checks=collections.Counter()
assert [t['tile_id'] for t in S['tiles']]==[t['tile_id'] for t in P['tiles']]
for tile, plan in zip(S['tiles'],P['tiles']):
 assert len(tile['steps'])==len(plan['steps'])
 taught=set()
 for st,ps in zip(tile['steps'],plan['steps']):
  for field in ['step_id','type','concept_ids']:assert st[field]==ps[field]
  for field in ['fact_ids','teaching_block_ids']:assert st['lineage'][field]==ps[field]
  checks['plan_exact']+=1
  if st['type'] in ['check','hands_on']:
   assert 'blocks' not in st and 'interaction' not in st
   assert set(ps['fact_ids'])<=taught
   if st['type']=='hands_on' and ps['planned_interaction_type'] in ['choice','classify']:
    assert re.match(r'(Review|Judge) ',st['title'])
    assert not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit|README|ws\.)',st['title']+' '+st['lede'])
   checks['framing_only']+=1
  if st['type']=='video':
   assert st['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
   checks['segment_ids_copied']+=1
  if ps['word_budget']:
   assert sum(words(b) for b in st.get('blocks',[]))<=ps['word_budget'], st['step_id']
   checks['within_budget']+=1
  for b in st.get('blocks',[]):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
  if st['type']=='explainer' and ps['planned_visual_block_type']:
   assert any(b['type']==ps['planned_visual_block_type'] and set(ps['anchors'])<=set(b['lineage'].get('anchors',[])) for b in st['blocks'])
   checks['planned_visual_and_anchor']+=1
  if st['type']=='recap':assert st['blocks'][-1]['type']=='up_next'
 for cid in plan['concept_ids']:
  assert {cid+'#'+f['id'] for f in bundles[cid]['coverage']['required_facts']}<=taught
  checks['facts_taught_by_text']+=1
 for ps in plan['steps']:
  if ps['type'] in ['check','hands_on']:
   assert any(r['concept_ids']==ps['concept_ids'] and set(ps['fact_ids'])<=set(r['lineage']['fact_ids']) for r in tile['remediation_steps'])
   checks['measured_facts_have_remediation']+=1
 for st in tile['steps']+tile['remediation_steps']:
  for top in st.get('blocks',[]):
   for b in blocks(top):
    assert not any(k in b for k in ['result','output','computed_values','execution_provenance','rows'])
    checks['no_authored_outputs']+=1
    if b['type'] not in ['media_group','up_next']:
     assert 'lineage' in b
     for key in ['fact_ids','teaching_block_ids','anchors']:
      for identifier in b['lineage'].get(key,[]):assert '#' in identifier
    if b['type']=='prose':
     assert len(b['text'].split())<=90
     assert not re.search(r'\bvideo\b',b['text'],re.I)
     checks['short_standalone_lineaged_prose']+=1
    if b['type']=='code_walkthrough':
     ast.parse(b['code'])
     checks['code_syntax_valid_no_typed_output']+=1
    if 'asset_ref' in b:
     a=assets[b['asset_ref']['asset_id']]
     assert set(b['asset_ref'].get('columns',[]))<={x['name'] for x in a['columns']}
     checks['registered_asset_columns']+=1
    if b['type']=='data_table' and 'result_of' in b:
     assert 'asset_ref' not in b
     for mount in b['result_of']['asset_mounts']:assert mount['asset_id'] in assets
     checks['query_result_computed_not_typed']+=1
report={'status':'PASS','tiles':len(S['tiles']),'steps':sum(len(t['steps']) for t in S['tiles']),'remediation_steps':sum(len(t['remediation_steps']) for t in S['tiles']),'checks':dict(checks),'uncertainties':[]}
(B/'scratch/screens03_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
