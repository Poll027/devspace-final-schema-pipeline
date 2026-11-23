import sys,json,re,collections
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from assemble_tiles import iter_blocks
from checkers.sandbox import run_query
from schema_check import errors as schema_errors
B=Path('batches/final_batch_mle.region.production_operations')
S=json.load(open(B/'screens.json'));P=json.load(open(B/'tile_plans.json'));R=json.load(open(B/'scenario_asset_registry.json'));G=json.load(open(B/'inputs/path_glossary_bundle.json'))
A={a['asset_id']:a for a in R['assets']};C={c['context']['concept_id']:c for c in G['bundles']}
fail=[];queries=0;counts=collections.Counter();maxprose=0;maxrem=0
ck=lambda value,message:fail.append(message) if not value else None
ck(not schema_errors(S,'screens_part.schema.json'),'Schema')
ck([t['tile_id'] for t in S['tiles']]==[t['tile_id'] for t in P['tiles']],'Tile coverage/order')
for tile,plan in zip(S['tiles'],P['tiles']):
 taught=set()
 ck([s['step_id'] for s in tile['steps']]==[s['step_id'] for s in plan['steps']],'Step order')
 for st,ps in zip(tile['steps'],plan['steps']):
  counts[st['type']]+=1
  for k in ['concept_ids','type']:ck(st[k]==ps[k],st['step_id']+' '+k)
  for k in ['teaching_block_ids','fact_ids']:ck(st['lineage'][k]==ps[k],st['step_id']+' '+k)
  if st['type'] in ['check','hands_on']:
   ck(not st.get('blocks'),st['step_id']+' framing only')
   ck(set(ps['fact_ids'])<=taught,st['step_id']+' facts taught before measurement')
   if st['type']=='hands_on' and ps['planned_interaction_type'] in ['choice','classify']:
    text=st['title']+' '+st.get('lede','')
    ck(not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit)\b|ws\.|README',text,re.I),st['step_id']+' inspect-and-judge framing')
   rems=[r for r in tile['remediation_steps'] if r['concept_ids']==st['concept_ids'] and set(r['lineage']['fact_ids'])==set(ps['fact_ids'])]
   ck(bool(rems),st['step_id']+' fact-specific remediation')
  textwords=sum(len(b['text'].split()) for b in st.get('blocks',[]) if b['type'] in ['prose','up_next'] and b.get('text'))
  if st.get('blocks'):ck(textwords<=ps['word_budget'],st['step_id']+' budget')
  if ps.get('planned_visual_block_type') and st['type']=='explainer':
   ck(any(st['concept_ids'][0]+'#visual' in b.get('lineage',{}).get('anchors',[]) for b in iter_blocks(st.get('blocks'))),st['step_id']+' visual anchor')
  for block in iter_blocks(st.get('blocks')):
   if block['type']=='prose':taught.update(block['lineage']['fact_ids'])
 for st in tile['steps']+tile['remediation_steps']:
  if st['type']=='remediation':
   counts['remediation']+=1
   maxrem=max(maxrem,sum(len(b.get('text','').split()) for b in st['blocks']))
  for b in iter_blocks(st.get('blocks')):
   ck(not any(k in b for k in ['result','computed_values','output','execution_provenance']),st['step_id']+' no authored outputs')
   if b['type']=='prose':
    ck('lineage' in b,st['step_id']+' prose lineage');n=len(b['text'].split());maxprose=max(maxprose,n)
    ck(n<=90,st['step_id']+' single bounded prose idea')
    ck(not re.search(r'\bvideo\b|as shown|as you saw',b['text'],re.I),st['step_id']+' standalone text')
   for k,section in [('fact_ids','coverage'),('teaching_block_ids','teaching_blocks')]:
    for ref in b.get('lineage',{}).get(k,[]):
     cid,_,rid=ref.partition('#');ck(bool(rid) and cid in C,st['step_id']+' qualified '+ref)
     if cid in C:
      ids={x['id'] for x in (C[cid]['coverage']['required_facts'] if k=='fact_ids' else C[cid]['teaching_blocks'])}
      ck(rid in ids,st['step_id']+' valid '+ref)
   if b['type'] in ['data_table','diagram','process_flow','side_by_side','before_after','code_walkthrough']:
    ck(bool(b.get('lineage',{}).get('anchors')),st['step_id']+' visual block lineage')
   if 'asset_ref' in b:
    a=b['asset_ref'];ck(a['asset_id'] in A,st['step_id']+' registered asset')
    cols={x['name'] for x in A[a['asset_id']].get('columns',[])}
    ck(set(a.get('columns',[]) or [])<=cols,st['step_id']+' registered columns')
   if 'result_of' in b:
    queries+=1;result,err=run_query(R,b['result_of']);ck(not err,st['step_id']+' executable query: '+str(err))
ck(not (B/'interactions.json').exists(),'Interactions absent: assembly gate not yet applicable')
report={'status':'PASS' if not fail else 'FAIL','tile_count':len(S['tiles']),'step_counts':dict(counts),'query_checks':queries,'max_prose_words':maxprose,'max_remediation_words':maxrem,'failures':fail,'manual_review':['Compared teaching text with glossary conditions and uncertainty: no hedge strengthened, no causal claim added, no open list closed.','Scenario references and policy literals are extracted from the registry; displayed derived quantities are result_of queries, never authored rows.','Planned visual types realized with #visual lineage; no registered image assets exist.','Each distinct planned check/hands-on fact set has its own remediation; original concept dataset/policy is retained.','Last tile has no next_tile_id; recap uses Path complete rather than inventing a next concept.']}
(B/'03_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(bool(fail))
