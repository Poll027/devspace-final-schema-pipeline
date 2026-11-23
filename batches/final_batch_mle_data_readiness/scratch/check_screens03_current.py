import json,re,sys,ast
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from finlib import words
B=Path('batches/final_batch_mle.region.data_readiness')
p=json.loads((B/'tile_plans.json').read_text());s=json.loads((B/'screens.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());r=json.loads((B/'scenario_asset_registry.json').read_text());mapping=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/anchor_mapping.json').read_text())
assets={a['asset_id']:a for a in r['assets']};bundles={b['context']['concept_id']:b for b in g['bundles']};errors=[]
def require(ok,msg):
 if not ok:errors.append(msg)
def blocks(bs):
 for z in bs:
  yield z
  for k in ('left','right','before','after'):
   if k in z:yield from blocks([z[k]])
knownfacts={c+'#'+f['id'] for c,b in bundles.items() for f in b['coverage']['required_facts']}
knowntbs={c+'#'+tb['id'] for c,b in bundles.items() for tb in b['teaching_blocks']}
require([t['tile_id'] for t in s['tiles']]==[t['tile_id'] for t in p['tiles']], 'tile coverage/order')
counts={'tiles':len(s['tiles']),'planned_steps':0,'remediation_steps':0,'prose_blocks':0,'walkthroughs':0,'visual_blocks':0}
for plan,tile in zip(p['tiles'],s['tiles']):
 require([(x['step_id'],x['type']) for x in tile['steps']]==[(x['step_id'],x['type']) for x in plan['steps']],tile['tile_id']+' step plan')
 counts['planned_steps']+=len(tile['steps']);counts['remediation_steps']+=len(tile['remediation_steps']);taught=set()
 for ps,x in zip(plan['steps'],tile['steps']):
  sid=x['step_id'];require(x['concept_ids']==ps['concept_ids'],sid+' concepts')
  for k in ('teaching_block_ids','fact_ids','segment_ids','anchors'):require(x['lineage'][k]==ps[k],sid+' '+k)
  bs=list(blocks(x.get('blocks',[])))
  if x['type'] in ('check','hands_on'):
   require(not x.get('blocks') and 'interaction' not in x,sid+' must be framing only')
   require(set(ps['fact_ids'])<=taught,sid+' facts not taught in preceding prose')
   rems=[z for z in tile['remediation_steps'] if z['concept_ids']==x['concept_ids'] and set(ps['fact_ids'])<=set(z['lineage']['fact_ids'])]
   require(bool(rems),sid+' targeted remediation absent')
   if x['type']=='hands_on' and ps['planned_interaction_type'] in ('classify','choice'):
    text=x['title']+' '+x.get('lede','');require(not re.search(r'\b(Implement|Build|Run|Execute|Provision|Train|Commit|Submit|README)\b|ws\.',text),sid+' inspect-and-judge framing')
  if x['type']=='video':require(x['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}],sid+' media fields')
  prose=[z for z in bs if z['type']=='prose'];n=sum(words(z['text']) for z in prose)
  require(n<=ps['word_budget'],sid+' word budget')
  for z in prose:taught.update(z['lineage']['fact_ids'])
  vt=ps['planned_visual_block_type']
  if vt:require(any(z['type']==vt for z in bs),sid+' planned visual absent')
  if '#visual' in ' '.join(ps['anchors']):
   for c in ps['concept_ids']:require(any(c+'#visual' in z.get('lineage',{}).get('anchors',[]) for z in bs if z['type']!='prose'),sid+' visual anchor absent')
  if x['type']=='recap':require(any(z['type']=='up_next' for z in bs),sid+' next tile absent')
 required={c+'#'+f['id'] for c in plan['concept_ids'] for f in bundles[c]['coverage']['required_facts']}
 require(required<=taught,tile['tile_id']+' required fact not text-taught')
 for x in tile['steps']+tile['remediation_steps']:
  sid=x['step_id']
  for z in blocks(x.get('blocks',[])):
   require(not any(k in z for k in ('output','result','computed_values','execution_provenance')),sid+' authored computed output')
   if z['type']=='prose':
    counts['prose_blocks']+=1;require('lineage' in z,sid+' text missing lineage');require(words(z['text'])<=90,sid+' prose >90 words');require(not re.search(r'\bvideo\b',z['text'],re.I),sid+' video mention')
   if 'lineage' in z:
    require(set(z['lineage'].get('fact_ids',[]))<=knownfacts,sid+' invalid fact lineage')
    require(set(z['lineage'].get('teaching_block_ids',[]))<=knowntbs,sid+' invalid teaching lineage')
   if z['type']=='code_walkthrough':counts['walkthroughs']+=1;ast.parse(z['code'])
   if z['type'] not in ('prose','media_group','up_next'):
    counts['visual_blocks']+=1;require(any(a.endswith('#visual') for a in z.get('lineage',{}).get('anchors',[])),sid+' visual missing anchor')
   if 'asset_ref' in z:
    ref=z['asset_ref'];a=assets.get(ref['asset_id']);require(bool(a),sid+' unknown asset')
    if a:require(set(ref.get('columns',[]))<={c['name'] for c in a.get('columns',[])},sid+' nonexistent column')
   if z['type']=='data_table':require('rows' not in z,sid+' typed data rows')
  if x['type']=='remediation':require(re.fullmatch(re.escape(tile['tile_id'])+r'\.r\d{2}',sid) is not None,sid+' remediation id')
report={'status':'PASS' if not errors else 'FAIL','counts':counts,'checks':['All assigned tiles and planned step ids/types/order preserved','Exact planned concept and lineage fields','Framing-only interactions; inspect-and-judge wording','Every required fact taught by preceding standalone prose','Every check/hands-on has fact-complete same-concept recovery','Per-step budgets and <=90 words per prose block','Qualified, glossary-valid lineage on every prose block','Registry-valid asset references and columns; no inline table rows','Planned visual block types and #visual anchors','Segment ids only; no copied segment fields','Computed output/provenance absent','Recap plus next-tile first-idea teaser','Manual source review: hedges/open lists preserved; examples use registered fictional policies and computed rather than typed outputs'],'errors':errors,'notes':['No interactions.json exists; assembly/interaction validation is deferred until that stage supplies it.','Final next-tile teaser uses the immediately following concept in the glossary ordered names; its bundle is outside this batch.']}
(B/'scratch/screens03_checklist_current.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));sys.exit(bool(errors))
