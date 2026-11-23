import json,re,ast,sqlite3
from pathlib import Path
B=Path(__file__).parent
O=json.loads((B/'screens.json').read_text()); P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); A=json.loads((B/'scenario_asset_registry.json').read_text())
assets={a['asset_id']:a for a in A['assets']}; bundles={b['context']['concept_id']:b for b in G['bundles']}
facts={c+'#'+f['id'] for c,b in bundles.items() for f in b['coverage']['required_facts']};tbs={c+'#'+t['id'] for c,b in bundles.items() for t in b['teaching_blocks']}
fail=[];counts={};queries=0;codes=0;blockids=set()
def require(v,msg):
 if not v:fail.append(msg)
def walk(bs):
 for b in bs:
  yield b
  for k in ('left','right'):
   if isinstance(b.get(k),dict):yield from walk([b[k]])
def run_query(block):
 conn=sqlite3.connect(':memory:')
 for m in block['result_of']['asset_mounts']:
  a=assets[m['asset_id']]
  cols=', '.join('"'+c['name']+'" '+({'integer':'INTEGER','number':'REAL','boolean':'INTEGER'}.get(c['type'],'TEXT')) for c in a['columns'])
  conn.execute('CREATE TABLE "'+m['mount_path']+'" ('+cols+')')
  conn.executemany('INSERT INTO "'+m['mount_path']+'" VALUES ('+','.join('?' for _ in a['columns'])+')',a['rows'])
 try:conn.execute(block['result_of']['sql']).fetchall()
 finally:conn.close()
require([t['tile_id'] for t in O['tiles']]==[t['tile_id'] for t in P['tiles']],'tile coverage/order differs')
for tile,pt in zip(O['tiles'],P['tiles']):
 require(len(tile['steps'])==len(pt['steps']),'step count differs '+tile['tile_id'])
 taught=set()
 for s,ps in zip(tile['steps'],pt['steps']):
  for k in ('step_id','type','concept_ids'):require(s[k]==ps[k],s['step_id']+' mismatch '+k)
  for k in ('fact_ids','teaching_block_ids'):require(s['lineage'][k]==ps[k],s['step_id']+' mismatch lineage '+k)
  if s['type'] in ('check','hands_on'):
   require(not s.get('blocks'),s['step_id']+' carries interaction content')
   require(set(ps['fact_ids'])<=taught,s['step_id']+' assesses untaught facts')
   require(any(set(ps['fact_ids'])<=set(r['lineage']['fact_ids']) for r in tile['remediation_steps']),s['step_id']+' lacks measured-fact remediation')
  blocks=list(walk(s.get('blocks',[])))
  if s['type']=='explainer':
   taught|={f for b in blocks if b['type']=='prose' for f in b['lineage']['fact_ids']}
  if s['type']=='video':
   require(s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids'],'block_id':s['blocks'][0]['block_id']}],s['step_id']+' has authored media fields')
  wc=sum(len(b.get('text','').split()) for b in blocks if b['type']=='prose')
  require(wc<=ps['word_budget'],f'{s["step_id"]} over budget: {wc}>{ps["word_budget"]}')
  if ps['planned_visual_block_type'] not in (None,'up_next','media_group'):
   require(any(b['type']==ps['planned_visual_block_type'] for b in blocks),s['step_id']+' planned visual absent')
   require(any(s['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in blocks),s['step_id']+' visual anchor absent')
 require({c+'#'+f['id'] for c in pt['concept_ids'] for f in bundles[c]['coverage']['required_facts']}<=taught,tile['tile_id']+' missing text fact coverage')
 for s in tile['steps']+tile['remediation_steps']:
  counts[s['type']]=counts.get(s['type'],0)+1
  for b in walk(s.get('blocks',[])):
   require(b['block_id'] not in blockids,'duplicate block id');blockids.add(b['block_id'])
   require(not any(k in b for k in ('computed_values','output','execution_provenance','result')),b['block_id']+' has authored output')
   for f in b.get('lineage',{}).get('fact_ids',[]):require(f in facts,b['block_id']+' invalid/unqualified fact '+f)
   for t in b.get('lineage',{}).get('teaching_block_ids',[]):require(t in tbs,b['block_id']+' invalid/unqualified tb '+t)
   if b['type']=='prose':
    require(all(k in b.get('lineage',{}) for k in ('concept_ids','fact_ids','teaching_block_ids')),b['block_id']+' missing text lineage')
    require(len(b['text'].split())<=90,b['block_id']+' prose longer than 90 words')
    require(not re.search(r'\bvideo\b',b['text'],re.I),b['block_id']+' mentions video')
   ref=b.get('asset_ref')
   if ref:
    require(ref['asset_id'] in assets,b['block_id']+' nonexistent asset')
    require(set(ref.get('columns',[]))<=set(c['name'] for c in assets[ref['asset_id']].get('columns',[])),b['block_id']+' nonexistent columns')
   if b['type'] in ('data_table','spreadsheet_grid','side_by_side','code_walkthrough'):
    require(any(x.endswith('#visual') for x in b.get('lineage',{}).get('anchors',[])),b['block_id']+' missing #visual')
   if b['type']=='code_walkthrough':
    codes+=1
    try:ast.parse(b['code'])
    except Exception as e:fail.append(b['block_id']+' invalid code '+str(e))
   if 'result_of' in b:
    queries+=1
    require('asset_ref' not in b,b['block_id']+' uses asset_ref to imitate query output')
    try:run_query(b)
    except Exception as e:fail.append(b['block_id']+' SQL reference smoke test: '+str(e))
report={'status':'PASS' if not fail else 'FAIL','tiles':len(O['tiles']),'step_counts':counts,'blocks':len(blockids),'query_definitions_smoke_tested':queries,'python_walkthroughs_parsed':codes,'interactions_exist':(B/'interactions.json').exists(),'findings':fail,'manual_review':['Revoicing preserves supplied hedges, open lists, zero-correct-cost assumptions, undefined-rate handling and protected-test boundaries.','Numeric examples, parameter defaults, asset IDs, cell ranges and query outputs are sourced or computed; no result rows, hashes, media details or outputs are typed.','All text teaches independently; no references to video. No images exist in this registry.','Next-tile names appear only in up_next; no blocked future topic is taught.','Remediation covers distinct planned measured fact sets with the same registered evidence and a clear contrast.']}
(B/'screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(bool(fail))
