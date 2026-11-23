import json,re
from pathlib import Path
from collections import Counter
B=Path('batches/final_batch_mle.region.custom_training')
P=json.loads((B/'tile_plans.json').read_text());S=json.loads((B/'screens.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text());R=json.loads((B/'scenario_asset_registry.json').read_text())
C={c['context']['concept_id']:c for c in G['bundles']};A={a['asset_id']:a for a in R['assets']}
def walk(blocks):
 for b in blocks:
  yield b
  for key in ['left','right','before','after']:
   if key in b:yield from walk([b[key]])
def visible(blocks):
 for b in walk(blocks):
  for key in ['text','caption','takeaway','change_summary','title','alt_text','left_label','right_label']:
   if isinstance(b.get(key),str):yield b[key]
  if b['type']=='diagram':
   for n in b['nodes']:yield n['label']
assert [t['tile_id'] for t in S['tiles']]==[t['tile_id'] for t in P['tiles']]
counts=Counter();rem_count=0
for t,pt in zip(S['tiles'],P['tiles']):
 assert [(s['step_id'],s['type'],s['concept_ids']) for s in t['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in pt['steps']]
 taught=set();seen_visual=set()
 for s,ps in zip(t['steps'],pt['steps']):
  counts[s['type']]+=1
  for key in ['fact_ids','teaching_block_ids','segment_ids','anchors']:
   assert s['lineage'][key]==ps[key],(s['step_id'],key)
  if s['type'] in ['check','hands_on']:
   assert 'blocks' not in s and 'interaction' not in s
   assert set(ps['fact_ids'])<=taught,('untaught',s['step_id'],set(ps['fact_ids'])-taught)
  if s['type']=='hands_on' and ps['planned_interaction_type'] in ['classify','choice']:
   txt=s['title']+' '+s['lede']
   assert not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit|README)\b|ws\.',txt,re.I),s['step_id']
   assert 'supplied excerpts in this step' in s['lede']
  if s['type']=='video':
   assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if ps['word_budget']:
   # Conservative: count all descriptive block text, including alt text.
   n=sum(len(x.split()) for x in visible(s.get('blocks',[])))
   assert n<=ps['word_budget'],('over budget',s['step_id'],n,ps['word_budget'])
  for b in walk(s.get('blocks',[])):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
   seen_visual.update(b.get('lineage',{}).get('anchors',[]))
   if b['type']=='prose':assert len(b['text'].split())<=90,(s['step_id'],len(b['text'].split()))
  if ps['planned_visual_block_type'] and ps['type']=='explainer':
   assert ps['planned_visual_block_type'] in [b['type'] for b in s['blocks']]
   assert ps['concept_ids'][0]+'#visual' in seen_visual
  if s['type']=='recap':assert s['blocks'][-1]['type']=='up_next'
 required={cid+'#'+f['id'] for cid in pt['concept_ids'] for f in C[cid]['coverage']['required_facts']}
 assert required<=taught,('missing facts',required-taught)
 factsets={tuple(sorted(s['lineage']['fact_ids'])) for s in t['remediation_steps']}
 for ps in pt['steps']:
  if ps['type'] in ['check','hands_on']:assert tuple(sorted(ps['fact_ids'])) in factsets
 for s in t['steps']+t['remediation_steps']:
  rem_count+=s['type']=='remediation'
  for b in walk(s.get('blocks',[])):
   assert not set(b).intersection(['output','execution_provenance','result','computed_values','segments','bridge'])
   if b['type']=='prose':
    assert all(k in b['lineage'] for k in ['concept_ids','fact_ids','teaching_block_ids'])
    assert len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b|as .* shows',b['text'],re.I)
   L=b.get('lineage',{})
   for f in L.get('fact_ids',[]):
    cid,fid=f.split('#');assert fid in {x['id'] for x in C[cid]['coverage']['required_facts']}
   for q in L.get('teaching_block_ids',[]):
    cid,tbid=q.split('#');assert tbid in {x['id'] for x in C[cid]['teaching_blocks']}
   if b['type']=='data_table':
    assert 'result_of' not in b and 'rows' not in b
    ar=b['asset_ref'];assert ar['asset_id'] in A
    cols={x['name'] for x in A[ar['asset_id']]['columns']}
    assert set(ar.get('columns',[]))<=cols
report={'artifact':str(B/'screens.json'),'tiles':len(S['tiles']),'planned_steps':sum(counts.values()),'step_types':dict(counts),'remediation_steps':rem_count,'checklist':{'plan_identity_order_and_lineage':'PASS','framing_only_interactions':'PASS','inspect_and_judge_framing':'PASS','qualified_existing_fact_and_teaching_ids':'PASS','required_facts_taught_in_text':'PASS','prose_under_90_words':'PASS','step_budgets_conservative_all_descriptive_text':'PASS','planned_visuals_and_visual_anchors':'PASS','media_segment_ids_only':'PASS','registered_datasets_and_columns':'PASS','no_typed_outputs_or_inline_rows':'PASS','no_video_references_in_prose':'PASS','recaps_and_up_next':'PASS','distinct_measured_fact_sets_remediated':'PASS'},'interactions_exist':(B/'interactions.json').exists()}
(B/'stage03_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
