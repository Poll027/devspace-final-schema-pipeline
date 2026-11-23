import json,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox as sb
B=Path('batches/final_batch_mle.region.validation_and_selection'); D=json.loads((B/'interactions.json').read_text());R=json.loads((B/'scenario_asset_registry.json').read_text())
for tile in D['tiles']:
 for e in tile['interactions']:
  ix=e['interaction'];typ=ix['type'];print(e['step_id'],flush=True)
  if typ=='code_exercise':
   pub=ix['public'];gr=ix['grading'];entry,sol=sb._entry(ix,'solution');tb,_=sb._tables(R,pub['workspace']['asset_mounts'],{},[])
   if pub['runtime']['kind']=='python':
    probes=[sb._py_probe(t) for t in gr['tests']];job=sb._py_job('python',pub['runtime'].get('packages',[]),[sb._py_script('compute',entry,sol,sb._py_mounts(tb),probes)]);res=sb.node_run(job,sb.RUNTIMES['python']['runner'])['results']['compute']
    if not res['ok']:raise RuntimeError(res.get('error'))
    for t in gr['tests']:
     q=res['probes'][t['test_id']]
     if not q['ok']:raise RuntimeError(q)
     t['spec']['expected']=q['value']
   else:
    script=sb._sheet_script('compute',sol,tb,sb._sheet_probes(gr['tests']));res=sb.node_run({'scripts':[script]},sb.RUNTIMES['spreadsheet']['runner'])['results']['compute']
    for t in gr['tests']:
     got,why=sb._sheet_result(res,t['test_id'])
     if why:raise RuntimeError(why)
     t['spec']['expected']=got
  elif typ=='formula_entry':
   pub=ix['public'];gr=ix['grading'];tb,_=sb._tables(R,[{'asset_id':pub['asset_ref']['asset_id'],'mount_path':pub['sheet_name']+'.csv'}],{},[])
   script=sb._sheet_script('compute',pub['target_cell']+': '+gr['reference_formula'],tb,[{'id':'value','kind':'cell','ref':pub['target_cell']}]);res=sb.node_run({'scripts':[script]},sb.RUNTIMES['spreadsheet']['runner'])['results']['compute'];got,why=sb._sheet_result(res,'value')
   if why:raise RuntimeError(why)
   if isinstance(got,str) and got.startswith('#'):raise RuntimeError(got)
   gr['expected_value']=got
(B/'interactions.json').write_text(json.dumps(D,indent=2)+'\n')
