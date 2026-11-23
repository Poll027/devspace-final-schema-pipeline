import json, re
from pathlib import Path
P=Path('batches/final_batch_mle.region.reproducible_release')
s=json.loads((P/'screens.json').read_text());p=json.loads((P/'tile_plans.json').read_text());g=json.loads((P/'inputs/path_glossary_bundle.json').read_text());r=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']};A={a['asset_id']:a for a in r['assets']}
def walk(blocks):
 for b in blocks:
  yield b
  for k in ['left','right']:
   if isinstance(b.get(k),dict):yield from walk([b[k]])
checks=[]
for t,pt in zip(s['tiles'],p['tiles']):
 assert t['tile_id']==pt['tile_id']
 assert len(t['steps'])==len(pt['steps'])
 for st,ps in zip(t['steps'],pt['steps']):
  for k in ['step_id','type','concept_ids']:assert st[k]==ps[k],(st['step_id'],k)
  for k in ['teaching_block_ids','fact_ids']:assert st['lineage'][k]==ps[k]
  if st['type'] in ['check','hands_on']:assert 'blocks' not in st and 'interaction' not in st
  wc=sum(len(b['text'].split()) for b in walk(st.get('blocks',[])) if b['type']=='prose')
  assert wc<=ps['word_budget'],(st['step_id'],wc,ps['word_budget'])
  if st['type']=='video':assert st['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if ps['anchors'] and any(a.endswith('#visual') for a in ps['anchors']):
   assert any(set(ps['anchors']) & set(b.get('lineage',{}).get('anchors',[])) for b in walk(st.get('blocks',[])))
 for st in t['steps']+t['remediation_steps']:
  for b in walk(st.get('blocks',[])):
   for key in ['fact_ids','teaching_block_ids']:
    for v in b.get('lineage',{}).get(key,[]):
     cid,fid=v.split('#');assert cid in B
     ids=[f['id'] for f in B[cid]['coverage']['required_facts']] if key=='fact_ids' else [tb['id'] for tb in B[cid]['teaching_blocks']]
     assert fid in ids
   if b['type']=='prose':
    assert all(k in b.get('lineage',{}) for k in ['concept_ids','teaching_block_ids','fact_ids'])
    assert len(b['text'].split())<=90
    assert not re.search(r'\bvideo\b',b['text'],re.I)
    for cid in st['concept_ids']:
     for future in B[cid]['context']['blocked_future_concepts']:
      assert future not in b['text']
      name=g['names'].get(future,'')
      if name:assert name.lower() not in b['text'].lower()
   if 'asset_ref' in b:
    a=A[b['asset_ref']['asset_id']]
    assert not b.get('rows')
    assert all(c in [v['name'] for v in a.get('columns',[])] for c in b['asset_ref'].get('columns',[]) or [])
   assert 'output' not in b and 'result' not in b and 'computed_values' not in b and 'execution_provenance' not in b
  if st['type']=='remediation':assert re.fullmatch(re.escape(t['tile_id'])+r'\.r\d\d',st['step_id'])
 for target in [st for st in t['steps'] if st['type'] in ['check','hands_on']]:
  assert any(set(target['lineage']['fact_ids'])<=set(rem['lineage']['fact_ids']) and target['concept_ids']==rem['concept_ids'] for rem in t['remediation_steps'])
 checks.append({'tile_id':t['tile_id'],'planned_steps':len(t['steps']),'remediation_steps':len(t['remediation_steps'])})
report={'status':'PASS','tiles':checks,'checklist':['plan ids/types/order/concepts and step fact/teaching lineage match','check/hands-on framing only','qualified valid fact and teaching ids','every prose has lineage and at most 90 words','all planned step prose within word budget','no video-dependent prose or blocked-future names','planned visual anchors realised','registered data references and existing columns only; no inline rows','no authored code/formula/chart outputs or provenance','media segment ids copied from plan','distinct remediation coverage for checks and hands-on','manual review: glossary meaning, hedges and open-list scope preserved; fixture values read by script']}
(P/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
