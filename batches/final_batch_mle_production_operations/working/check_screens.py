import json,sqlite3,re
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations')
s=json.loads((B/'screens.json').read_text());p=json.loads((B/'tile_plans.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
assets={a['asset_id']:a for a in r['assets']};bundles={x['context']['concept_id']:x for x in g['bundles']};errors=[];counts={'tiles':len(s['tiles']),'planned_steps':0,'remediation_steps':0,'prose_blocks':0,'query_visuals':0,'code_visuals':0}
def check(ok,msg):
 if not ok:errors.append(msg)
def visit(b,step):
 typ=b['type'];L=b.get('lineage',{})
 if typ=='prose':
  counts['prose_blocks']+=1
  check(len(b['text'].split())<=90,step['step_id']+' prose over 90')
  check(bool(L.get('concept_ids')) and bool(L.get('teaching_block_ids')),step['step_id']+' missing prose lineage')
  check(not re.search(r'\bvideo\b',b['text'],re.I),step['step_id']+' mentions video')
 for f in L.get('fact_ids',[]):
  c,sep,fid=f.partition('#');check(sep and c in bundles and fid in {x['id'] for x in bundles[c]['coverage']['required_facts']},'invalid fact '+f)
 for q in L.get('teaching_block_ids',[]):
  c,sep,tb=q.partition('#');check(sep and c in bundles and tb in {x['id'] for x in bundles[c]['teaching_blocks']},'invalid teaching block '+q)
 if typ not in ['prose','up_next','media_group']:
  check(any(x.endswith('#visual') for x in L.get('anchors',[])),step['step_id']+' missing visual anchor')
 for key in ['rows','result','computed_values','execution_provenance','output']:
  check(key not in b,step['step_id']+' authored output '+key)
 if 'asset_ref' in b:
  ref=b['asset_ref'];a=assets.get(ref['asset_id']);check(a is not None,'unknown asset')
  if a and typ=='data_table':
   check(a['asset_kind']=='dataset','non-dataset table')
   for col in ref.get('columns',[]):check(col in {x['name'] for x in a['columns']},'absent column '+col)
 if 'result_of' in b:
  counts['query_visuals']+=1
  check('asset_ref' not in b,'query mixes asset_ref')
  # Validate query syntax and source-column names; do not author or persist results.
  con=sqlite3.connect(':memory:')
  for m in b['result_of']['asset_mounts']:
   a=assets[m['asset_id']];cols=a['columns'];names=[x['name'] for x in cols]
   con.execute('CREATE TABLE "'+m['mount_path']+'" ('+','.join('"'+x['name']+'" '+('REAL' if x['type'] in ['number','integer','boolean'] else 'TEXT') for x in cols)+')')
   con.executemany('INSERT INTO "'+m['mount_path']+'" VALUES ('+','.join('?' for x in cols)+')',a['rows'])
  try:con.execute(b['result_of']['sql']).fetchall()
  except Exception as e:errors.append(step['step_id']+' SQL: '+str(e))
  con.close()
 if typ=='code_walkthrough':
  counts['code_visuals']+=1
  if b['language']=='python':
   try:compile(b['code'],'screen','exec')
   except Exception as e:errors.append('invalid Python: '+str(e))
 for key in ['left','right','before','after']:
  if key in b:visit(b[key],step)
for tile,plan in zip(s['tiles'],p['tiles']):
 check(tile['tile_id']==plan['tile_id'],'tile mismatch')
 check(len(tile['steps'])==len(plan['steps']),'missing planned step')
 counts['planned_steps']+=len(tile['steps']);counts['remediation_steps']+=len(tile['remediation_steps'])
 taught=set()
 for st,ps in zip(tile['steps'],plan['steps']):
  for key in ['step_id','type','concept_ids']:check(st[key]==ps[key],'plan mismatch '+key)
  for key in ['teaching_block_ids','fact_ids']:check(st['lineage'][key]==ps[key],'plan lineage mismatch '+key)
  if st['type'] in ['check','hands_on']:
   check('blocks' not in st and 'interaction' not in st,'interaction step is not framing-only')
   check(set(st['lineage']['fact_ids'])<=taught,'assessment facts not taught first')
   check(any(set(st['lineage']['fact_ids'])<=set(x['lineage']['fact_ids']) and x['concept_ids']==st['concept_ids'] for x in tile['remediation_steps']),'missing remediation')
  text_words=sum(len(b['text'].split()) for b in st.get('blocks',[]) if b['type']=='prose')
  check(not ps['word_budget'] or text_words<=ps['word_budget'],'over word budget '+st['step_id'])
  for b in st.get('blocks',[]):
   visit(b,st)
   if b['type']=='prose':taught.update(b.get('lineage',{}).get('fact_ids',[]))
  if st['type']=='recap':check(any(b['type']=='up_next' for b in st['blocks']),'missing up_next')
 for st in tile['remediation_steps']:
  check(re.match(re.escape(tile['tile_id'])+r'\.r\d\d$',st['step_id']) is not None,'invalid remediation ID')
  for b in st['blocks']:visit(b,st)
 for c in plan['concept_ids']:
  check({c+'#'+f['id'] for f in bundles[c]['coverage']['required_facts']}<=taught,'required facts missing '+c)
report={'counts':counts,'checklist':['Same planned steps, order, types and lineage','Qualified facts and teaching-block references','Standalone prose with lineage, no video dependence','Registry-only assets and valid column names','Prose <=90 words and steps within planned budgets','All required facts taught before checks','Separate remediation for differing assessed fact sets','Visual anchors present','No authored rows, query results, expected computed values or code outputs','SQL syntax/source columns and Python syntax checked','Recap with next-tile idea, or documented terminal tile'], 'errors':errors,'semantic_review':'Glossary qualifiers and bounded authorization retained. Registered fixtures are explicitly fictional; expected recovery/cleanup/budget evidence is not presented as learner execution. Code outputs and query results are left for downstream computation.'}
(B/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));assert not errors
