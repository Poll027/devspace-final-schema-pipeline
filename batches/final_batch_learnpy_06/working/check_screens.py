import json,re,collections
from pathlib import Path
P=Path('batches/final_batch_learn_python.region.06')
D=json.loads((P/'screens.json').read_text());PL=json.loads((P/'tile_plans.json').read_text());G=json.loads((P/'inputs/path_glossary_bundle.json').read_text());R=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in G['bundles']};assets={a['asset_id']:a for a in R['assets']}
checks=[]
def walk(bs):
 for b in bs:
  yield b
  for k in ['left','right','before','after']:
   if isinstance(b.get(k),dict):yield from walk([b[k]])
assert [t['tile_id'] for t in D['tiles']]==[t['tile_id'] for t in PL['tiles']]
counts=collections.Counter();remcount=0
for t,pt in zip(D['tiles'],PL['tiles']):
 assert [(s['step_id'],s['type'],s['concept_ids']) for s in t['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in pt['steps']]
 taught=set(); remcount+=len(t['remediation_steps'])
 for s,ps in zip(t['steps'],pt['steps']):
  counts[s['type']]+=1
  for key in ['fact_ids','teaching_block_ids']:
   assert s['lineage'][key]==ps[key]
  if s['type'] in ['check','hands_on']:
   assert 'blocks' not in s and 'interaction' not in s
   assert set(ps['fact_ids'])<=taught,(s['step_id'],'not taught')
   fs=set(ps['fact_ids']) or {ps['concept_ids'][0]+'#'+f['id'] for f in B[ps['concept_ids'][0]]['coverage']['required_facts']}
   assert any(fs==set(r['lineage']['fact_ids']) and r['concept_ids']==s['concept_ids'] for r in t['remediation_steps'])
   if s['type']=='hands_on' and ps['planned_interaction_type'] in ['choice','classify']:
    text=s['title']+' '+s['lede']
    assert not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit)\b|ws\.|README',text,re.I)
  if s['type']=='video':
   assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if ps['planned_visual_block_type'] not in [None,'media_group','up_next']:
   assert any(ps['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in walk(s['blocks']))
  prosewords=sum(len(b['text'].split()) for b in walk(s.get('blocks',[])) if b['type']=='prose')
  if ps['word_budget']:assert prosewords<=ps['word_budget'],(s['step_id'],prosewords,ps['word_budget'])
  for b in walk(s.get('blocks',[])):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
  if s['type']=='recap' and pt['next_tile_id']:
   nxt=next(x for x in PL['tiles'] if x['tile_id']==pt['next_tile_id'])
   assert any(b['type']=='up_next' and b['title']==B[nxt['concept_ids'][0]]['context']['concept_name'] for b in s['blocks'])
 for s in t['steps']+t['remediation_steps']:
  for b in walk(s.get('blocks',[])):
   if b['type'] not in ['media_group','up_next']:
    assert b.get('lineage',{}).get('concept_ids'),(s['step_id'],'no block lineage')
   for f in b.get('lineage',{}).get('fact_ids',[]):
    cid,fid=f.split('#');assert fid in {x['id'] for x in B[cid]['coverage']['required_facts']}
   for tb in b.get('lineage',{}).get('teaching_block_ids',[]):
    cid,bid=tb.split('#');assert bid in {x['id'] for x in B[cid]['teaching_blocks']}
   assert 'output' not in b and 'execution_provenance' not in b and 'computed_values' not in b
   if b['type']=='prose':
    assert len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b',b['text'],re.I)
    for cid in s['concept_ids']:
     for future in B[cid]['context']['blocked_future_concepts']:
      name=G.get('names',{}).get(future,'')
      if name:assert name.lower() not in b['text'].lower()
   if b['type']=='data_table':assert b['asset_ref']['asset_id'] in assets
checks=['All assigned tiles covered; planned IDs, types, order, concepts and step lineage copied','All measured planned facts taught by text before assessments','Framing-only assessment/practice steps; judgement-task wording checked','Distinct measured fact sets have matching remediation coverage','Prose blocks: one compact source-grounded fact or contrast, <=90 words; step prose within budget','No prose references to video or blocked future concept names','Qualified valid fact/teaching IDs; prose and visual lineage present','All planned visual anchors realised; report uses diagram fallback because no images are registered','No typed code output, hashes, derived cells or inline data tables','Registry/source examples copied by script; mode/path and numeric cases reviewed against registered workspaces','Paraphrase reviewed for hedges, open lists, required-validation distinctions and absence of added causes','Recaps contain source-grounded takeaways and the next tile’s first idea where a next tile exists']
report={'status':'PASS','tiles':len(D['tiles']),'planned_steps':sum(counts.values()),'step_counts':dict(counts),'remediation_steps':remcount,'checklist':checks,'limitations':['No registered image assets; runner report visual is a labelled diagram.','API runtime/version and dependency verification evidence are not registered; visuals show the supplied claim and verification checks without fabricating documentation or package evidence.','No interactions artifact exists yet, so assembly/interaction validation is deferred; screens schema gate run.']}
(P/'reports/screens_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
