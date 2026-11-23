import json,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox
B=Path('batches/final_batch_mle.region.data_readiness');p=B/'interactions.json';D=json.loads(p.read_text());R=json.loads((B/'scenario_asset_registry.json').read_text())
for tile in D['tiles']:
 for item in tile['interactions']:
  ix=item['interaction']
  if ix['type']!='code_exercise':continue
  ws=ix['public']['workspace'];starter=ws['files'][0]['content'];solution=ix['grading']['solution_files'][0]['content']
  fixtures=next((f['content'] for f in ws['files'] if f['path']=='fixtures.py'),None)
  if fixtures:
   starter=starter.replace('from fixtures import FIXTURES',fixtures)
   solution=solution.replace('from fixtures import FIXTURES',fixtures)
  auth=next((f['content'] for f in ws['files'] if f['path']=='authorized_runtime.py'),None)
  if auth:
   starter=starter.replace('from authorized_runtime import read_sample, use_secret',auth)
   solution=solution.replace('from authorized_runtime import read_sample, use_secret',auth)
  ws['files']=[dict(path='learner.py',role='editable',language='python',content=starter)]
  ix['grading']['solution_files'][0]['content']=solution
p.write_text(json.dumps(D,indent=2)+'\n')
for tile in D['tiles']:
 for item in tile['interactions']:
  ix=item['interaction']
  if ix['type']!='code_exercise':continue
  sid=item['step_id'];ws=ix['public']['workspace'];entry,code=sandbox._entry(ix,'solution');tables,_=sandbox._tables(R,ws.get('asset_mounts',[]),{},[])
  probes=[sandbox._py_probe(t) for t in ix['grading']['tests']]
  job=sandbox._py_job('python',ix['public']['runtime']['packages'],[sandbox._py_script('solution',entry,code,sandbox._py_mounts(tables),probes)])
  res=sandbox.node_run(job,sandbox.RUNTIMES['python']['runner'])['results']['solution']
  (B/'scratch'/('runtime_'+sid+'.json')).write_text(json.dumps(res,indent=2))
  if not res['ok']:print(sid,'ERROR',res['error'],flush=True);continue
  for t in ix['grading']['tests']:
   v=res['probes'][t['test_id']]
   if not v['ok']:print(sid,t['test_id'],'PROBE ERROR',v,flush=True);continue
   t['spec']['expected']=v['value']
  p.write_text(json.dumps(D,indent=2)+'\n');print(sid,'computed',len(ix['grading']['tests']),'tests',flush=True)
