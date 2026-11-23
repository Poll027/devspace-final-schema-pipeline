import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox,pysyntax
B=Path('batches/final_batch_mle.region.data_readiness'); path=B/'interactions.json';d=json.loads(path.read_text());registry=json.loads((B/'scenario_asset_registry.json').read_text())
groups={}
for tile in d['tiles']:
 for ent in tile['interactions']:
  ix=ent['interaction']
  if ix['type']!='code_exercise':continue
  pub=ix['public'];sol=ix['grading']['solution_files'][0]['content'];starter=pub['workspace']['files'][0]['content']
  viol,unmapped,tags=pysyntax.judge(sol,pub['constraints']['allowed_syntax'],pub['constraints']['blocked_syntax'],starter)
  print(ent['step_id'],'SYNTAX',viol,'UNMAPPED',unmapped,flush=True)
  tables,_=sandbox._tables(registry,pub['workspace']['asset_mounts'],{},[])
  probes=[sandbox._py_probe(t) for t in ix['grading']['tests'] if t['kind']!='stdout_equals']
  sc=sandbox._py_script(ent['step_id'],'main.py',sol,sandbox._py_mounts(tables),probes)
  pkgs=tuple(pub['runtime']['packages']);groups.setdefault(pkgs,[]).append((ent,sc))
for pkgs,entries in groups.items():
 print('EXECUTE',pkgs,len(entries),flush=True)
 try:res=sandbox.node_run(sandbox._py_job('python',list(pkgs),[sc for _,sc in entries]),sandbox.RUNTIMES['python']['runner'])
 except Exception as e: print('RUNNER FAILURE',str(e)[:1000],flush=True);continue
 for ent,sc in entries:
  r=res['results'][ent['step_id']]
  if not r['ok']:print(ent['step_id'],'ERROR',r.get('error'),flush=True);continue
  for t in ent['interaction']['grading']['tests']:
   pr=r['probes'].get(t['test_id'],{})
   if not pr.get('ok'): print(ent['step_id'],t['test_id'],'PROBE ERROR',pr,flush=True);continue
   t['spec']['expected']=pr['value']
  print(ent['step_id'],'computed',len(r['probes']),flush=True)
path.write_text(json.dumps(d,indent=2)+'\n')
