import ast,csv,hashlib,io,json,sys
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers.dataset import resolve_dataset,find_row,rule_holds
r=json.loads((B/'scenario_asset_registry.json').read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
coverage=json.loads((B/'working/asset_coverage.json').read_text())
checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
assets={a['asset_id']:a for a in r['assets']}
check('Full batch: all glossary concepts covered once',len(coverage)==len(g['bundles']) and {c['concept_id'] for c in coverage}=={b['context']['concept_id'] for b in g['bundles']})
check('Every mapped asset exists',all(i in assets for c in coverage for i in c['asset_ids']))
for a in assets.values():
 if a['asset_kind']=='code_workspace':
  paths=[f['path'] for f in a['files']]
  check(a['asset_id']+' unique file paths',len(paths)==len(set(paths)))
  for f in a['files']:
   if f['path'].endswith('.py'):ast.parse(f['content'])
  check(a['asset_id']+' learner implementation absent',next(f['content'] for f in a['files'] if f['path']=='learner.py').strip().startswith('#'))
  continue
 cols=a['columns'];names=[c['name'] for c in cols]
 check(a['asset_id']+' row widths',all(len(row)==len(cols) for row in a['rows']))
 check(a['asset_id']+' unambiguous semantic roles',all(c['semantic_role']!='numerical' or c['type'] in ('integer','number') for c in cols))
 for row in a['rows']:
  for c,v in zip(cols,row):
   if v is None:continue
   typ=c['type']
   check(a['asset_id']+'.'+c['name']+' declared base value type', (typ=='integer' and type(v)==int) or (typ=='number' and type(v) in (float,int)) or (typ in ('string','datetime','date') and isinstance(v,str)) or (typ=='boolean' and type(v)==bool))
 data=(B/a['data_file']['uri']).read_bytes()
 check(a['asset_id']+' computed file hash',hashlib.sha256(data).hexdigest()==a['data_file']['sha256'])
 loaded=list(csv.reader(io.StringIO(data.decode())))
 check(a['asset_id']+' CSV header and row counts',loaded[0]==names and len(loaded)-1==len(a['rows']))
 for v in a['variants']:
  cc,rr=resolve_dataset(r,a['asset_id'],v['variant_id'])
  for p in v.get('planted_issues',[]):
   for loc in p['locations']:
    idx=find_row(rr,loc['where'],loc.get('occurrence',0));check(v['variant_id']+' issue predicate matches',idx is not None)
    if 'rule' in p:ok,_=rule_holds(p['rule'],rr,idx,loc['column'])
    elif p['kind']=='missing_value':ok=rr[idx][loc['column']] is None
    elif p['kind']=='duplicate_row':ok=any(i!=idx and row==rr[idx] for i,row in enumerate(rr))
    else:ok=False
    check(v['variant_id']+' planted issue holds after all ops',ok)
    if p['kind']=='duplicate_row':check(v['variant_id']+' duplicate occurrence points to repeated copy',loc['occurrence']>0)
# Verify fixture breadth and exact glossary examples, calculated from authored data.
namespace={};exec(next(f['content'] for f in assets['ws.numpy_shape_dtype']['files'] if f['path']=='fixtures.py'),namespace)
f=namespace['FIXTURES'];check('Shape fixtures accepted, boundary, flat, empty, wrong width, too many',set(['valid','tuple_boundary','empty','flat','wrong_width','too_many'])<=f.keys())
counts={row[0]:row[1:] for row in assets['ds.outcome_counts']['rows']}
check('Outcome counts keep populations and horizon separate',counts['all orders'][1]>counts['specified zone'][1] and counts['all orders'][2]==counts['specified zone'][2])
order=assets['ds.orders'];check('Glossary zero-padded order key preserved as text',isinstance(order['rows'][0][0],str) and order['rows'][0][0].startswith('00') and order['columns'][0]['semantic_role']=='identifier')
chunk=assets['ds.chunked_orders'];exec(next(f['content'] for f in assets['ws.chunked_ingestion']['files'] if f['path']=='fixtures.py'),namespace);f=namespace['FIXTURES']
limit=f['array_budget']//(f['feature_count']*f['element_width'])
check('Chunk breadth: multiple full chunks and final short chunk',len(chunk['rows'])>2*limit and len(chunk['rows'])%limit>0)
check('Chunk matrix has exactly declared feature width',len(chunk['columns'])==f['feature_count'])
check('No pictures required by any glossary visual/teaching anchor',not any(b['visual_anchor']['type'] in ('chart','plot') for b in g['bundles']))
summary={'status':'PASS','check_count':len(checks),'concept_count':len(g['bundles']),'scenario_count':len(r['scenarios']),'dataset_count':sum(a['asset_kind']=='dataset' for a in assets.values()),'workspace_count':sum(a['asset_kind']=='code_workspace' for a in assets.values()),'variant_count':sum(len(a.get('variants',[])) for a in assets.values()),'row_count':sum(len(a.get('rows',[])) for a in assets.values()),'checklist':['row widths match columns','base declared types and semantic roles agree','variant ops resolve and every planted issue holds','duplicate occurrence identifies repeated copy','whole batch mapped and boundary/failure fixtures supplied','glossary keys, matrix, populations and named fields retained','all data-file hashes computed','workspace Python syntax parsed; learner solutions absent','anchors need code/tables/before-after, not rendered plots'],'notes':['Registry gate has no code_workspace checker; workspaces receive schema and additional local syntax/fixture checks.','The gate permits numeric_looking_label=true only for numeric-typed columns. The leading-zero order key remains string/identifier with explicit text-only description; no flag is set on that string column. Binary numerical target codes are flagged as numeric-looking labels.'],'asset_ids':list(assets)}
(B/'working/registry_self_check.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
