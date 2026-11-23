import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_mle.region.production_operations');p=B/'interactions.json';d=json.loads(p.read_text());registry=json.loads((B/'scenario_asset_registry.json').read_text());scripts=[];idx={}
for t in d['tiles']:
 for x in t['interactions']:
  i=x['interaction'];k=x['step_id']
  if i['type']!='code_exercise':continue
  tests=[i['grading']['tests'][0]]
  if k.endswith('080_082.s04'):
   tests += [{'test_id':'single_emission','kind':'value_equals','spec':{'expr':'emitted_records','expected':None}},{'test_id':'emitted_jsonl','kind':'value_equals','spec':{'expr':"[json.loads(line) for line in open('summary.jsonl')]",'expected':None}}]
  if k.endswith('083_085.s06'):tests+=[{'test_id':'illustrative_cohort','kind':'value_equals','spec':{'expr':'illustrative_report','expected':None}}]
  if k.endswith('091_094.s14'):tests+=[{'test_id':'verification','kind':'value_equals','spec':{'expr':"{'checks':verification,'replay':outputs}",'expected':None}}]
  i['grading']['tests']=tests;probes=[sandbox._py_probe(t) for t in tests];tables,_=sandbox._tables(registry,i['public']['workspace']['asset_mounts'],{},[])
  scripts.append(sandbox._py_script(k,'main.py',i['grading']['solution_files'][0]['content'],sandbox._py_mounts(tables),probes));idx[k]=i
res=sandbox.node_run(sandbox._py_job('python',['numpy','pyyaml'],scripts),sandbox.RUNTIMES['python']['runner'])['results']
(B/'working/recompute_results.json').write_text(json.dumps(res,indent=2))
for k,r in res.items():
 if not r['ok']:print('ERROR',k,r.get('error'));continue
 i=idx[k]
 for t in i['grading']['tests']:
  pr=r['probes'][t['test_id']]
  if pr['ok']:t['spec']['expected']=pr['value']
  else:print('PROBE ERROR',k,pr)
 print('computed',k)
p.write_text(json.dumps(d,indent=2)+'\n')
