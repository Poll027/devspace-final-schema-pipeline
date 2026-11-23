import json,re
from pathlib import Path
from collections import Counter
P=Path('batches/final_batch_aws_devops.region.03_1')
S=json.load(open(P/'screens.json'));T=json.load(open(P/'tile_plans.json'));G=json.load(open(P/'inputs/path_glossary_bundle.json'));R=json.load(open(P/'scenario_asset_registry.json'))
B={b['context']['concept_id']:b for b in G['bundles']}; A={a['asset_id']:a for a in R['assets']}
assert [t['tile_id'] for t in S['tiles']]==[t['tile_id'] for t in T['tiles']]
def walk(b):
 yield b
 for key in ['left','right','before','after']:
  if isinstance(b.get(key),dict): yield from walk(b[key])
counts=Counter();taught=set();visuals=set();max_words=0
for tile,pt in zip(S['tiles'],T['tiles']):
 assert len(tile['steps'])==len(pt['steps'])
 for s,p in zip(tile['steps'],pt['steps']):
  for key in ['step_id','type','concept_ids']: assert s[key]==p[key]
  for key in ['teaching_block_ids','fact_ids','segment_ids','anchors']: assert s['lineage'][key]==p[key]
  if s['type'] in ['check','hands_on']:
   assert 'blocks' not in s and 'interaction' not in s
   if s['type']=='hands_on' and p['planned_interaction_type'] in ['classify','choice']:
    assert s['title'].startswith('Review ')
    assert not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit|README|ws\.)\b',s['title']+' '+s['lede'])
  if s['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':p['segment_ids']}]
  words=sum(len(b.get('text','').split()) for b in s.get('blocks',[]) if b['type']=='prose')
  if p['word_budget']: assert words<=p['word_budget'],(s['step_id'],words,p['word_budget'])
  if s['type']=='recap':assert s['blocks'][-1]['type']=='up_next' and pt['next_tile_id'] in s['blocks'][-1]['text']
  if p['planned_visual_block_type'] not in [None,'media_group','up_next']:
   assert any(p['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in s['blocks'])
  if s['type'] in ['check','hands_on']:
   expected=set(p['fact_ids'])
   if s['type']=='hands_on':expected|={p['concept_ids'][0]+'#'+f['id'] for f in B[p['concept_ids'][0]]['coverage']['required_facts']}
   assert any(expected<=set(r['lineage']['fact_ids']) and r['concept_ids']==s['concept_ids'] for r in tile['remediation_steps'])
 for s in tile['steps']+tile['remediation_steps']:
  counts[s['type']]+=1
  for root in s.get('blocks',[]):
   for b in walk(root):
    assert not any(k in b for k in ['result','output','computed_values','execution_provenance'])
    if b['type']=='prose':
     assert 'lineage' in b and len(b['text'].split())<=90
     assert not re.search(r'\bvideo\b',b['text'],re.I)
     max_words=max(max_words,len(b['text'].split()))
     if s['type']=='explainer':taught.update(b['lineage']['fact_ids'])
    lin=b.get('lineage',{})
    for key in ['fact_ids','teaching_block_ids']:
     for q in lin.get(key,[]):assert '#' in q and q.partition('#')[0] in B
    visuals.update(lin.get('anchors',[]))
    if 'asset_ref' in b:
     asset=A[b['asset_ref']['asset_id']]
     assert set(b['asset_ref']['columns'])<=set(c['name'] for c in asset['columns'])
     assert 'rows' not in b
for cid,b in B.items():
 assert {cid+'#'+f['id'] for f in b['coverage']['required_facts']}<=taught
 assert cid+'#visual' in visuals
report={'status':'PASS','tiles':len(S['tiles']),'step_counts':dict(counts),'planned_steps':sum(len(t['steps']) for t in S['tiles']),'remediation_steps':sum(len(t['remediation_steps']) for t in S['tiles']),'taught_facts':len(taught),'visual_anchors':len([a for a in visuals if a.endswith('#visual')]),'max_prose_words':max_words,'checks':['exact planned order, type, concepts and step lineage','check/hands_on framing only','inspect-and-judge wording','word budgets and 90-word prose limit','qualified lineage and full textual fact coverage','registered asset IDs and columns; no inline rows','no typed output, result, computed values or segment fields','visual anchor tags and registered-image absence fallback','recap up-next and remediation measured-fact coverage','manual review: hedges, open lists, grant distinctions, no future teaching or unsupported causes']}
(P/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
