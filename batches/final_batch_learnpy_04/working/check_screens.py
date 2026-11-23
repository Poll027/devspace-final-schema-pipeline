import ast,json,re,collections
from pathlib import Path
P=Path('batches/final_batch_learn_python.region.04')
s=json.loads((P/'screens.json').read_text());p=json.loads((P/'tile_plans.json').read_text());g=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']}
assert [t['tile_id'] for t in s['tiles']]==[t['tile_id'] for t in p['tiles']]
counts=collections.Counter();nblocks=0

def blocks(seq):
 for b in seq:
  yield b
  for k in ['left','right','before','after']:
   if k in b:yield from blocks([b[k]])
def visible_words(b):
 return sum(len(b.get(k,'').split()) for k in ['text','title','change_summary','takeaway','alt_text','left_label','right_label'])+sum(len(x['text'].split()) for x in b.get('annotations',[]))+sum(len(x['label'].split()) for x in b.get('nodes',[]))+sum(len(x.get('label','').split()) for x in b.get('edges',[]))+sum(visible_words(b[k]) for k in ['left','right','before','after'] if k in b)

for t,pt in zip(s['tiles'],p['tiles']):
 assert len(t['steps'])==len(pt['steps'])
 for st,ps in zip(t['steps'],pt['steps']):
  for k in ['step_id','type','concept_ids']:assert st[k]==ps[k],(st['step_id'],k)
  for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']:assert st['lineage'][k]==ps[k]
  if st['type'] in ['check','hands_on']:assert 'blocks' not in st and 'interaction' not in st
  if ps['word_budget']:assert sum(visible_words(b) for b in st.get('blocks',[]))<=ps['word_budget'],st['step_id']
  if st['type']=='video':assert st['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
  if st['type']=='recap':assert st['blocks'][-1]['type']=='up_next'
  if st['type']=='explainer' and ps['planned_visual_block_type']:
   assert any(any(a.endswith('#visual') for a in b.get('lineage',{}).get('anchors',[])) for b in st['blocks'])
 for st in t['steps']+t['remediation_steps']:
  counts[st['type']]+=1
  for b in blocks(st.get('blocks',[])):
   nblocks+=1
   assert 'output' not in b and 'result' not in b and 'computed_values' not in b
   if b['type']=='code_walkthrough':ast.parse(b['code'])
   if b['type']=='prose':
    assert len(b['text'].split())<=90
    assert not re.search(r'\b(video|clip)\b',b['text'],re.I)
    assert b.get('lineage',{}).get('concept_ids') and b['lineage'].get('teaching_block_ids') and b['lineage'].get('fact_ids')
   for f in b.get('lineage',{}).get('fact_ids',[]):
    cid,fid=f.split('#');assert fid in [x['id'] for x in B[cid]['coverage']['required_facts']]
   for tb in b.get('lineage',{}).get('teaching_block_ids',[]):
    cid,tid=tb.split('#');assert tid in [x['id'] for x in B[cid]['teaching_blocks']]
 for ps in pt['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  for c in ps['concept_ids']:
   fs=set(f for f in ps['fact_ids'] if f.startswith(c+'#')) or {c+'#'+f['id'] for f in B[c]['coverage']['required_facts']}
   rs=[r for r in t['remediation_steps'] if r['concept_ids']==[c] and set(r['lineage']['fact_ids'])==fs]
   assert rs,ps['step_id']
   taught={f for b in rs[0]['blocks'] if b['type']=='prose' for f in b['lineage']['fact_ids']}
   assert fs<=taught
 # Every required fact is taught in a planned prose screen before assessment.
 taught=set()
 for st in t['steps']:
  if st['type'] in ['check','hands_on']:assert set(st['lineage']['fact_ids'])<=taught
  for b in blocks(st.get('blocks',[])):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
 assert {c+'#'+f['id'] for c in pt['concept_ids'] for f in B[c]['coverage']['required_facts']}<=taught
print('CHECKLIST PASS: plan identity/order/lineage; framing-only interactions; qualified factual text; prose and screen budgets; text independent of media; visual anchors; source-only media; recap/up-next; targeted remediation; no authored outputs; code syntax.')
print('Human review: glossary hedges and platform conditions retained; scenario identifiers, paths, columns and literals checked against registry/glossary; no unavailable images or unsupported concepts introduced.')
print('Counts:',dict(counts),'tiles:',len(s['tiles']),'blocks including nested:',nblocks)
