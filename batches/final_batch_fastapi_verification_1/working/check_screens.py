import json,re
from pathlib import Path
P=Path('batches/final_batch_verification_1')
d=json.loads((P/'screens.json').read_text());p=json.loads((P/'tile_plans.json').read_text());g=json.loads((P/'inputs/path_glossary_bundle.json').read_text());r=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']};A={a['asset_id']:a for a in r['assets']}
expected=[t['tile_id'] for t in p['tiles']]
assert [t['tile_id'] for t in d['tiles']]==expected
counts={'tiles':len(d['tiles']),'planned_steps':0,'remediation_steps':0,'prose_blocks':0,'visual_anchors':0}
def walk(block):
 yield block
 for k in ['before','after']:
  if isinstance(block.get(k),dict):yield from walk(block[k])
 for panel in block.get('panels',[]):
  for b in panel.get('blocks',[]):yield from walk(b)
def valid_lin(lin):
 assert all('#' in f for f in lin['fact_ids']+lin['teaching_block_ids'])
 for f in lin['fact_ids']:
  c,x=f.split('#');assert x in {z['id'] for z in B[c]['coverage']['required_facts']}
 for tb in lin['teaching_block_ids']:
  c,x=tb.split('#');assert x in {z['id'] for z in B[c]['teaching_blocks']}
for t,pt in zip(d['tiles'],p['tiles']):
 assert [(s['step_id'],s['type'],s['concept_ids']) for s in t['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in pt['steps']]
 counts['planned_steps']+=len(t['steps']);counts['remediation_steps']+=len(t['remediation_steps'])
 for s,ps in zip(t['steps'],pt['steps']):
  assert s['lineage']['fact_ids']==ps['fact_ids']
  assert s['lineage']['teaching_block_ids']==ps['teaching_block_ids']
  if s['type'] in ['check','hands_on']:assert 'blocks' not in s and 'interaction' not in s
  if s['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  prosewords=sum(len(re.findall(r"\b[\w'-]+\b",b['text'])) for b in s.get('blocks',[]) if b['type']=='prose')
  if ps['word_budget']:assert prosewords<=ps['word_budget'],(s['step_id'],prosewords,ps['word_budget'])
  if ps.get('anchors') and any(a.endswith('#visual') for a in ps['anchors']):
   assert any(s['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[]) for block in s['blocks'] for b in walk(block))
   counts['visual_anchors']+=1
  if s['type']=='recap':assert s['blocks'][-1]['type']=='up_next' and pt['next_tile_id'] in s['blocks'][-1]['title']
 for s in t['steps']+t['remediation_steps']:
  valid_lin(s['lineage'])
  for block in s.get('blocks',[]):
   for b in walk(block):
    assert not any(k in b for k in ['output','result','computed_values','execution_provenance'])
    if b['type']=='prose':
     counts['prose_blocks']+=1;valid_lin(b['lineage'])
     assert len(re.findall(r"\b[\w'-]+\b",b['text']))<=90
     assert not re.search(r'\bvideo\b',b['text'],re.I)
     for c in s['concept_ids']:
      for blocked in B[c]['context']['blocked_future_concepts']:
       name=g['names'].get(blocked,'')
       assert not name or name.lower() not in b['text'].lower()
    if 'asset_ref' in b:
     ref=b['asset_ref'];assert ref['asset_id'] in A
     asset=A[ref['asset_id']]
     assert set(ref.get('columns',[]))<=set(c['name'] for c in asset.get('columns',[]))
    if b['type']=='data_table':
     assert not ('asset_ref' in b and 'result_of' in b)
     assert 'rows' not in b
     for mount in b.get('result_of',{}).get('asset_mounts',[]):assert mount['asset_id'] in A
 # Every distinct interaction fact set has targeted review with actual prose teaching it.
 for ps in pt['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  assert any(set(rem['lineage']['fact_ids'])==set(ps['fact_ids']) and set(ps['fact_ids'])<=set(f for b in rem['blocks'] if b['type']=='prose' for f in b['lineage']['fact_ids']) for rem in t['remediation_steps'])
 taught={f for s in t['steps'] for b in s.get('blocks',[]) if b['type']=='prose' for f in b['lineage']['fact_ids']}
 assert all(c+'#'+f['id'] in taught for c in pt['concept_ids'] for f in B[c]['coverage']['required_facts'])
report={'status':'PASS','counts':counts,'checks':['Complete tile coverage','Planned step IDs, types, order and lineage preserved','Framing-only check/hands-on steps','Qualified valid fact and teaching-block IDs','Standalone prose; no video references or blocked concept names','Prose blocks at most 90 words and step prose within budget','Every visual anchor realised','Dataset columns exist; query results deferred','No typed output, result, hashes or computed values','Media segment IDs copied only','Recaps name next tile','Measured fact subsets have matching remediation'], 'notes':['No interactions artifact exists yet, so assembly/whole-tile validation is deferred.','Presence comparison has no dedicated dataset; it is a computed SQL rendering of the glossary presence rule using registered request bodies, with ds.orders as the single-row mount.','tile_054 first concept name inferred from the supplied frozen concept-name ordering; its teaching bundle is not included.']}
(P/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
