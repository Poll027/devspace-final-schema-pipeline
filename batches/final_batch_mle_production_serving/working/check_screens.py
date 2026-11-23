import json,re
from pathlib import Path
from collections import Counter
P=Path('batches/final_batch_mle.region.production_serving')
d=json.loads((P/'screens.json').read_text());p=json.loads((P/'tile_plans.json').read_text());g=json.loads((P/'inputs/path_glossary_bundle.json').read_text());r=json.loads((P/'scenario_asset_registry.json').read_text());B={b['context']['concept_id']:b for b in g['bundles']};assets={a['asset_id']:a for a in r['assets']}
def walk(x):
 if isinstance(x,dict):
  yield x
  for k,v in x.items():
   if k!='lineage':yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def words(s):
 return sum(len(v.split()) for b in walk(s.get('blocks',[])) for k,v in b.items() if k in ['text','caption','takeaway','change_summary','label','left_label','right_label','alt_text'] and isinstance(v,str))
counts=Counter();results=[]
assert [t['tile_id'] for t in d['tiles']]==[t['tile_id'] for t in p['tiles']]
for t,pt in zip(d['tiles'],p['tiles']):
 assert len(t['steps'])==len(pt['steps'])
 taught=set()
 for s,ps in zip(t['steps'],pt['steps']):
  for k in ['step_id','type','concept_ids']:assert s[k]==ps[k],(s['step_id'],k)
  for k in ['teaching_block_ids','fact_ids']:assert s['lineage'][k]==ps[k],(s['step_id'],k)
  assert words(s)<=ps['word_budget'],(s['step_id'],words(s),ps['word_budget'])
  if s['type'] in ['check','hands_on']:
   assert 'blocks' not in s and 'interaction' not in s
   assert set(ps['fact_ids'])<=taught,(s['step_id'],'untaught facts')
   assert any(set(ps['fact_ids'])<=set(rem['lineage']['fact_ids']) and rem['concept_ids']==ps['concept_ids'] for rem in t['remediation_steps']),(s['step_id'],'no matching remediation')
  if s['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if s['type']=='recap':assert s['blocks'][-1]['type']=='up_next'
  if ps['planned_visual_block_type'] not in [None,'up_next']:
   assert any(b.get('type')==ps['planned_visual_block_type'] and s['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in walk(s['blocks']))
  for b in walk(s.get('blocks',[])):
   if b.get('type')=='prose':taught.update(b['lineage']['fact_ids'])
  counts[s['type']]+=1
 for s in t['steps']+t['remediation_steps']:
  for b in walk(s.get('blocks',[])):
   typ=b.get('type')
   if typ=='prose':
    assert len(b['text'].split())<=90
    assert all(k in b['lineage'] for k in ['concept_ids','teaching_block_ids','fact_ids'])
   if 'lineage' in b:
    lin=b['lineage']
    for fid in lin.get('fact_ids',[]):
     cid,f=fid.split('#');assert f in {v['id'] for v in B[cid]['coverage']['required_facts']}
    for tid in lin.get('teaching_block_ids',[]):
     cid,tb=tid.split('#');assert tb in {v['id'] for v in B[cid]['teaching_blocks']}
   if typ=='data_table':
    assert 'rows' not in b and 'result' not in b
    if 'asset_ref' in b:
     ar=b['asset_ref'];assert ar['asset_id'] in assets
     assert set(ar.get('columns',[]))<={c['name'] for c in assets[ar['asset_id']]['columns']}
   assert 'output' not in b and 'computed_values' not in b and 'execution_provenance' not in b
   if typ=='media_group':assert set(b)<= {'type','segment_ids'}
   for k,v in b.items():
    if k in ['text','caption','alt_text','label','takeaway','change_summary'] and isinstance(v,str):assert not re.search(r'\bvideo\b',v,re.I)
  if s['type']=='remediation':counts['remediation']+=1
 results.append({'tile_id':t['tile_id'],'planned_steps':len(t['steps']),'remediation_steps':len(t['remediation_steps'])})
report={'artifact':str(P/'screens.json'),'tiles':results,'counts':dict(counts),'checks_passed':['complete tile coverage and exact planned step order/types/lineage','qualified glossary fact and teaching-block IDs','text-only teaching before interactions','framing only for checks and hands-on','separate remediation for every distinct measured fact scope','all prose has lineage and at most 90 words','all planned step text within word budget','planned visual types realized with qualified visual anchors','registered dataset references and existing columns; no inline/result rows','no manually authored output, provenance or computed values','no mention of video in teaching text','recaps include next first idea'],'semantic_review':'Reviewed against glossary teaching blocks: retained immutable/artifact, runtime-only secret, initialized-object readiness, nonproduction http.server, assertion optimization, full-denominator/deadline, latency population and percentile/ddof, stable-backlog, same-load/interval, approved-target and verify-before-retire qualifications. Concrete configuration, feature limits, chunk progression, probe schedule and batching objective come from registry inputs.'}
(P/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
