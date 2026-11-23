import json,re,collections
from pathlib import Path
B=Path('batches/final_batch_aws_devops.region.01_1')
x=json.loads((B/'screens.json').read_text());p=json.loads((B/'tile_plans.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
gs={b['context']['concept_id']:b for b in g['bundles']};rs={a['asset_id']:a for a in r['assets']}
def walk(bs):
 for b in bs:
  yield b
  for k in ['left','right']:
   if k in b:yield from walk([b[k]])
counts=collections.Counter();nblocks=0
assert [t['tile_id'] for t in x['tiles']]==[t['tile_id'] for t in p['tiles']]
for t,pt in zip(x['tiles'],p['tiles']):
 assert [(s['step_id'],s['type']) for s in t['steps']]==[(s['step_id'],s['type']) for s in pt['steps']]
 taught=set()
 for s,ps in zip(t['steps'],pt['steps']):
  counts[s['type']]+=1
  assert s['concept_ids']==ps['concept_ids']
  for k in ['fact_ids','teaching_block_ids','segment_ids','anchors']:assert s['lineage'][k]==ps[k]
  if s['type'] in ['check','hands_on']:
   assert not s.get('blocks') and 'interaction' not in s
   assert set(ps['fact_ids'])<=taught
   if s['type']=='hands_on' and ps['planned_interaction_type'] in ['classify','choice']:
    assert not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit)\b',s['title'])
    assert not re.search(r'ws\.|README|own execution',s.get('lede',''),re.I)
  else:
   total=sum(len(b['text'].split()) for b in walk(s['blocks']) if b['type']=='prose')
   assert total<=ps['word_budget'],(s['step_id'],total,ps['word_budget'])
   if s['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
   if s['type']=='recap':assert s['blocks'][-1]['type']=='up_next'
   for b in walk(s['blocks']):
    if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
  if ps['planned_visual_block_type'] not in [None,'up_next','media_group']:
   assert any(any(a.endswith('#visual') for a in b.get('lineage',{}).get('anchors',[])) for b in walk(s['blocks']))
 assert all(c+'#'+f['id'] in taught for c in t['steps'][0]['concept_ids'] for f in gs[c]['coverage']['required_facts'])
 for s in t['steps']+t['remediation_steps']:
  for b in walk(s.get('blocks',[])):
   nblocks+=1
   assert not any(k in b for k in ['result','computed_values','execution_provenance','output','segments'])
   if b['type']=='prose':
    assert 'lineage' in b and len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b',b['text'],re.I)
   if 'lineage' in b:
    for f in b['lineage']['fact_ids']:
     c, fid=f.split('#');assert fid in [z['id'] for z in gs[c]['coverage']['required_facts']]
    for tb in b['lineage']['teaching_block_ids']:
     c,bid=tb.split('#');assert bid in [z['id'] for z in gs[c]['teaching_blocks']]
   if 'asset_ref' in b:
    a=rs[b['asset_ref']['asset_id']]
    assert set(b['asset_ref']['columns'])<={z['name'] for z in a['columns']}
   if b['type']=='annotated_image':assert rs[b['asset_id']]['asset_kind']=='image'
 for ps in pt['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  target=set(ps['fact_ids']) or {c+'#'+f['id'] for c in ps['concept_ids'] for f in gs[c]['coverage']['required_facts']}
  assert any(target <= {f for b in rr['blocks'] if b['type']=='prose' for f in b['lineage']['fact_ids']} for rr in t['remediation_steps'])
report={'artifact':str(B/'screens.json'),'tiles':len(x['tiles']),'planned_steps':sum(counts.values()),'step_types':dict(counts),'remediation_steps':sum(len(t['remediation_steps']) for t in x['tiles']),'blocks_including_nested':nblocks,'checklist':'PASS: plan equality, qualified lineage, standalone text, prose and step budgets, registry columns and image availability, visual anchors, framing only, copied media IDs, measured-fact remediation coverage, no typed outputs. Scenario values are populated by build_screens.py from the registry/glossary; meaning and scope contrasts were reviewed against source teaching blocks.','uncertainties':['The next tile has no teaching-block bundle in this batch. Its up-next title uses the EC2 concept name available in the supplied glossary names.','The capacity hands-on plan has no fact_ids; its remediation covers all required facts of that concept.'],'interactions_available':(B/'interactions.json').exists()}
(B/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
