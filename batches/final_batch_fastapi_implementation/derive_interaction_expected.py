import json,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers.sandbox import node_run,_py_job,_py_script,_py_probe,RUNTIMES
B=Path(__file__).parent;out=json.loads((B/'interactions.json').read_text())
items=[i['interaction'] for t in out['tiles'] for i in t['interactions'] if i['interaction']['type']=='code_exercise']
def derive(ix):
 rt=ix['public']['runtime'];gr=ix['grading'];tests=gr['tests'];probes=[_py_probe(t) for t in tests]
 job=_py_job(rt['kind'],rt.get('packages',[]),[_py_script('solution','main.py',gr['solution_files'][0]['content'],[],probes)])
 result=node_run(job,RUNTIMES[rt['kind']]['runner'])['results']['solution']
 if not result['ok']:return ix['interaction_id'],result
 for t in tests:
  p=result['probes'][t['test_id']]
  if not p['ok']:return ix['interaction_id'],p
  v=p['value'];sp=t['spec']
  if t['kind']=='http_equals':
   keys=sp.pop('expected_keys', list(sp.get('expected', {'status':None,'json':None})));sp['expected']={k:v[k] for k in keys}
  else:sp['expected']=v
 return ix['interaction_id'],'derived'
with ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(derive,items))
for k,v in results:print(k,v)
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
(B/'expected_derivation_results.json').write_text(json.dumps(results,indent=2)+'\n')
if any(v!='derived' for k,v in results):sys.exit(1)
