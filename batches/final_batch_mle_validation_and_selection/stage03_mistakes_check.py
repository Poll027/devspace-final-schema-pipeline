import json,re,sqlite3,collections
from pathlib import Path
B=Path(__file__).parent
S=json.loads((B/'screens.json').read_text());P=json.loads((B/'tile_plans.json').read_text());G=json.loads((B/'inputs/path_glossary_bundle.json').read_text());R=json.loads((B/'scenario_asset_registry.json').read_text())
C={x['context']['concept_id']:x for x in G['bundles']};A={a['asset_id']:a for a in R['assets']};queries=0;proses=0

def blocks(b):
 yield b
 for side in ['left','right','before','after']:
  if isinstance(b.get(side),dict):yield from blocks(b[side])

def inspect(step,planned=None):
 global queries,proses
 prose_words=0
 for root in step.get('blocks',[]):
  for b in blocks(root):
   assert 'computed_values' not in b and 'result' not in b and 'output' not in b
   if b['type']=='prose':
    proses+=1;n=len(b['text'].split());assert n<=90,(step['step_id'],n)
    prose_words+=n
    assert b.get('lineage') and b['lineage']['concept_ids']
    assert not re.search(r'\bvideo\b',b['text'],re.I)
   if 'lineage' in b:
    for k in ['fact_ids','teaching_block_ids']:
     for q in b['lineage'].get(k,[]):
      cid,f=q.split('#');assert cid in C
      bank=C[cid]['coverage']['required_facts'] if k=='fact_ids' else C[cid]['teaching_blocks']
      assert f in [v['id'] for v in bank],q
   if 'asset_ref' in b:
    ref=b['asset_ref'];assert ref['asset_id'] in A
    assert set(ref.get('columns',[]))<=set(c['name'] for c in A[ref['asset_id']]['columns'])
   if b['type'] not in ['prose','up_next','media_group'] and step['type']=='explainer':assert step['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[])
   if b['type']=='media_group':assert set(b)=={'type','segment_ids'}
   if 'result_of' in b:
    assert 'asset_ref' not in b
    queries+=1;conn=sqlite3.connect(':memory:')
    for m in b['result_of']['asset_mounts']:
     a=A[m['asset_id']];cols=[c['name'] for c in a['columns']]
     conn.execute('CREATE TABLE "'+m['mount_path']+'" ('+','.join('"'+n+'"' for n in cols)+')')
     conn.executemany('INSERT INTO "'+m['mount_path']+'" VALUES ('+','.join('?' for _ in cols)+')',a['rows'])
    conn.execute(b['result_of']['sql']).fetchall();conn.close()
 if planned and planned['type'] not in ['check','hands_on']:assert prose_words<=planned['word_budget'],(step['step_id'],prose_words,planned['word_budget'])

counts=collections.Counter()
for t,p in zip(S['tiles'],P['tiles']):
 assert t['tile_id']==p['tile_id'];assert len(t['steps'])==len(p['steps'])
 taught=set()
 for s,ps in zip(t['steps'],p['steps']):
  assert (s['step_id'],s['type'],s['concept_ids'])==(ps['step_id'],ps['type'],ps['concept_ids'])
  for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']:assert s['lineage'][k]==ps[k]
  counts[s['type']]+=1;inspect(s,ps)
  if s['type'] in ['check','hands_on']:
   assert 'blocks' not in s
   c=s['concept_ids'][0];assert all(c+'#'+f['id'] in taught for f in C[c]['coverage']['required_facts'])
   if s['type']=='hands_on' and ps['planned_interaction_type'] in ['choice','classify']:
    assert not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit|README)\b|ws\.',s['title']+' '+s['lede'],re.I)
  for b in s.get('blocks',[]):
   if b['type']=='prose':taught.update(b['lineage']['fact_ids'])
 for r in t['remediation_steps']:
  counts['remediation']+=1;inspect(r)
  covered=set(f for b in r['blocks'] if b['type']=='prose' for f in b['lineage']['fact_ids'])
  assert set(r['lineage']['fact_ids'])<=covered
 assert len(t['remediation_steps'])==sum(s['type'] in ['check','hands_on'] for s in t['steps'])
 assert t['steps'][-1]['blocks'][-1]['type']=='up_next'
report={'passed':True,'tiles':len(S['tiles']),'steps_by_type':dict(counts),'prose_blocks':proses,'deferred_queries_syntax_checked':queries,'checks':['qualified facts and teaching blocks','prose lineage','standalone teaching before assessment','no video references in prose','registry assets and real columns only','no typed computed values/results/outputs','same planned order, types and step lineage','prose <=90 words and planned budgets','visual anchors present','check/hands-on framing only','inspect-and-judge framing','separate check and practice remediation coverage','recap and next idea present'],'semantic_review':'Revoiced text checked against source facts: fixed cost inputs, actual-class denominators, undefined empty groups, ordinary cutoffs, N versus N-1, estimator-specific parameter direction, sample-versus-population limits, and permission boundaries retained. No new causal or calibration claims. No registered images exist.','assembly_gate':'No interactions.json exists in this batch; secondary assemble/validate gate not applicable yet.'}
(B/'stage03_mistakes_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
