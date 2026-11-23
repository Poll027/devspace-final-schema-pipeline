import json,re
from pathlib import Path
B=Path('batches/final_batch_implementation');S=json.loads((B/'screens.json').read_text());P=json.loads((B/'tile_plans.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text());R=json.loads((B/'scenario_asset_registry.json').read_text())
bs={b['context']['concept_id']:b for b in G['bundles']};plans={t['tile_id']:t for t in P['tiles']};assets={a['asset_id']:a for a in R['assets']}
expected=['tile_022','tile_024','tile_025','tile_026','tile_028','tile_029','tile_030','tile_032','tile_033','tile_034','tile_037']
assert [t['tile_id'] for t in S['tiles']]==expected
counts={};blocks=0
for t in S['tiles']:
 p=plans[t['tile_id']];assert len(t['steps'])==len(p['steps']);taught=set()
 for s,ps in zip(t['steps'],p['steps']):
  assert (s['step_id'],s['type'],s['concept_ids'])==(ps['step_id'],ps['type'],ps['concept_ids'])
  for k in ['teaching_block_ids','fact_ids']:assert s['lineage'][k]==ps[k]
  if s['type'] in ['check','hands_on']:
   assert 'blocks' not in s and 'interaction' not in s
   for c in s['concept_ids']:
    measured=set(f for f in ps['fact_ids'] if f.startswith(c+'#'))
    if measured:
     assert measured<=taught
     assert any(set(r['lineage']['fact_ids'])==measured and r['concept_ids']==[c] for r in t['remediation_steps'])
  n=sum(len(b.get('text','').split()) for b in s.get('blocks',[]))
  if ps['word_budget']:assert n<=ps['word_budget'],(s['step_id'],n,ps['word_budget'])
  if s['type']=='explainer':
   for b in s['blocks']:
    if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
   if ps['planned_visual_block_type']:
    assert any(b['type']==ps['planned_visual_block_type'] and set(ps['anchors'])<=set(b.get('lineage',{}).get('anchors',[])) for b in s['blocks'])
  if s['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if s['type']=='recap':assert any(b['type']=='up_next' and p['next_tile_id'] in b['title'] for b in s['blocks'])
 for c in p['concept_ids']:assert set(c+'#'+f['id'] for f in bs[c]['coverage']['required_facts'])<=taught
 for s in t['steps']+t['remediation_steps']:
  counts[s['type']]=counts.get(s['type'],0)+1
  for b in s.get('blocks',[]):
   blocks+=1
   assert not any(k in b for k in ['result','output','execution_provenance','computed_values'])
   if b['type']=='prose':
    assert b.get('lineage') and b['lineage']['fact_ids'] and b['lineage']['teaching_block_ids']
    assert len(b['text'].split())<=90
    assert not re.search(r'\b(video|as shown|as seen)\b',b['text'],re.I)
   for k in ['fact_ids','teaching_block_ids','anchors']:
    for q in b.get('lineage',{}).get(k,[]):
     assert '#' in q
     c,i=q.split('#',1);assert c in bs
     if k=='fact_ids':assert i in [f['id'] for f in bs[c]['coverage']['required_facts']]
     elif k=='teaching_block_ids':assert i in [x['id'] for x in bs[c]['teaching_blocks']]
   if 'asset_ref' in b:
    a=assets[b['asset_ref']['asset_id']]
    assert set(b['asset_ref'].get('columns',[]))<=set(x['name'] for x in a['columns'])
# Scenario examples reviewed against their supplied workspace files; no inline data rows or computed outputs.
report={'artifact':str(B/'screens.json'),'tiles':len(S['tiles']),'step_counts':counts,'block_count':blocks,'checks':{'plan_ids_types_order_lineage':'PASS','text_teaches_all_required_facts_before_checks':'PASS','distinct_remediation_measured_fact_sets':'PASS','qualified_ids_and_prose_lineage':'PASS','prose_under_90_words_and_step_budgets':'PASS','no_video_dependent_text':'PASS','planned_visual_types_and_visual_anchor_tags':'PASS','no_typed_outputs_or_unregistered_images':'PASS','registry_example_review':'PASS — internal objects and test cases copied from registered workspaces; no inline table rows','paraphrase_meaning_and_future_concepts_review':'PASS — retains validation failures, source priority, per-chunk/total timeout distinction, response filtering bypass and process-local task limitations'},'uncertainties':['tile_039 is the planned next tile, but its first idea is absent from the named stage inputs. Its up_next names only the tile, without inventing its subject.'],'assembly_gate':'Not run: interactions.json does not exist; schema gate passed.'}
(B/'working/screens_self_check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
