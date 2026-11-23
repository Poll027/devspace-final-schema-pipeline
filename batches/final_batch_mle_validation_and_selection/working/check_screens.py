import json, re, sqlite3
from pathlib import Path
B=Path('batches/final_batch_mle.region.validation_and_selection')
P=json.load(open(B/'tile_plans.json'));O=json.load(open(B/'screens.json'));R=json.load(open(B/'scenario_asset_registry.json'));G=json.load(open(B/'inputs/path_glossary_bundle.json'))
A={a['asset_id']:a for a in R['assets']};BG={b['context']['concept_id']:b for b in G['bundles']}
errors=[];queries=0;proses=0

def require(ok,msg):
 if not ok:errors.append(msg)
def blocks(b):
 yield b
 for k in ('left','right'):
  if k in b:yield from blocks(b[k])
def textwords(bs):
 return sum(len(str(b.get(k,'')).split()) for x in bs for b in blocks(x) for k in ('text','caption','takeaway','left_label','right_label'))

def query_check(b):
 global queries
 db=sqlite3.connect(':memory:')
 for m in b['result_of']['asset_mounts']:
  a=A[m['asset_id']];cols=a['columns']
  types={'integer':'INTEGER','number':'REAL','boolean':'INTEGER','string':'TEXT'}
  db.execute('CREATE TABLE "'+m['mount_path']+'" ('+', '.join('"'+c['name']+'" '+types.get(c['type'],'TEXT') for c in cols)+')')
  db.executemany('INSERT INTO "'+m['mount_path']+'" VALUES ('+','.join('?' for c in cols)+')',a['rows'])
 try:
  result=db.execute(b['result_of']['sql']).fetchall();queries+=1
  require(len(result)>0,'Empty query: '+b.get('caption',''))
  if b.get('caption')=='Resolved budget gates trial evidence.':
   # The unexecuted row has neither a conditional rate nor completed status.
   require(sum(row[-3]=='completed' for row in result)==A['ds.execution_contract']['rows'][0][4], 'Resolved search-budget count mismatch')
 except Exception as e:errors.append('SQL: '+str(e)+' in '+b.get('caption',''))
 finally:db.close()

require([t['tile_id'] for t in O['tiles']]==[t['tile_id'] for t in P['tiles']],'Tile coverage mismatch')
for pt,t in zip(P['tiles'],O['tiles']):
 require([(s['step_id'],s['type'],s['concept_ids']) for s in t['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in pt['steps']],'Plan order/type/concepts mismatch')
 taught=set();allids=set()
 for ps,s in zip(pt['steps'],t['steps']):
  allids.add(s['step_id'])
  for k in ('fact_ids','teaching_block_ids','segment_ids'):
   require(s['lineage'][k]==ps[k],s['step_id']+' mismatched '+k)
  if s['type'] in ('check','hands_on'):
   require('blocks' not in s and 'interaction' not in s,'Framing contains interactions or blocks')
   require(set(ps['fact_ids'])<=taught,'Untaught measured facts '+s['step_id'])
   require(any(set(ps['fact_ids'])<=set(rs['lineage']['fact_ids']) and rs['concept_ids']==ps['concept_ids'] for rs in t['remediation_steps']),'Missing measured-fact remediation')
  if ps['word_budget']:
   n=textwords(s.get('blocks',[]))+len(s['title'].split())
   require(n<=ps['word_budget'],f'{s["step_id"]}: {n}>{ps["word_budget"]} words')
  for b in s.get('blocks',[]):
   for bb in blocks(b):
    if bb['type']=='prose':taught.update(bb['lineage']['fact_ids'])
  if ps['planned_visual_block_type'] and s['type']=='explainer':
   require(any(bb['type']==ps['planned_visual_block_type'] and ps['concept_ids'][0]+'#visual' in bb.get('lineage',{}).get('anchors',[]) for b in s['blocks'] for bb in blocks(b)),'Missing planned anchored visual '+s['step_id'])
 for c in pt['concept_ids']:
  require(set(c+'#'+f['id'] for f in BG[c]['coverage']['required_facts'])<=taught,'Missing required fact '+c)
 for s in t['steps']+t['remediation_steps']:
  for x in s.get('blocks',[]):
   for b in blocks(x):
    require(not any(k in b for k in ('result','computed_values','output','execution_provenance')),'Authored computed output')
    if b['type']=='prose':
     proses+=1
     require(len(b['text'].split())<=90,'Prose exceeds 90 words')
     require('lineage' in b,'Missing prose lineage')
     require(not re.search(r'\bvideo\b',b['text'],re.I),'Prose mentions video')
    for f in b.get('lineage',{}).get('fact_ids',[]):
     require('#f' in f,'Unqualified fact '+f)
     c,fid=f.split('#');require(c in BG and fid in [f['id'] for f in BG[c]['coverage']['required_facts']],'Unknown fact '+f)
    for q in b.get('lineage',{}).get('teaching_block_ids',[]):
     c,tid=q.split('#');require(c in BG and tid in [tb['id'] for tb in BG[c]['teaching_blocks']],'Unknown teaching block '+q)
    if 'asset_ref' in b:
     a=A.get(b['asset_ref']['asset_id']);require(a is not None,'Unknown asset')
     if a:
      require(set(b['asset_ref'].get('columns') or [])<=set(c['name'] for c in a.get('columns',[])),'Nonexistent dataset column')
      if b['asset_ref'].get('variant_id'):
       require(b['asset_ref']['variant_id'] in [v['variant_id'] for v in a['variants']],'Unknown variant')
    if 'result_of' in b:query_check(b)
    if b['type']=='code_walkthrough':
     try:compile(b['code'],'walkthrough','exec')
     except Exception as e:errors.append('Invalid Python walkthrough: '+str(e))
report={'status':'PASS' if not errors else 'FAIL','tile_count':len(O['tiles']),'main_steps':sum(len(t['steps']) for t in O['tiles']),'remediation_steps':sum(len(t['remediation_steps']) for t in O['tiles']),'prose_blocks_checked':proses,'sql_visuals_executed_in_memory':queries,'checks':['exact plan ids/types/order/concepts/step lineage','required facts taught before checks','fact-set-specific remediation coverage','qualified existing fact and teaching-block ids','standalone prose without video references','prose <=90 words and exact step word budgets','registered columns and variants only','planned visuals with qualified visual anchors','no authored outputs/hashes/segment fields','SQL queries valid on registry data','code walkthrough syntax'], 'errors':errors}
(B/'reports/screens_self_check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(bool(errors))
