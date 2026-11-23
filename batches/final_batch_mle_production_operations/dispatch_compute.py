import sys,json,pathlib
B=pathlib.Path(__file__).parent
sys.path.insert(0,str(pathlib.Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox as s
D=json.loads((B/'interactions.json').read_text()); registry=json.loads((B/'scenario_asset_registry.json').read_text())
named={'mle.tile.'+x for x in ['080_082.s04','080_082.s14','083_085.s06','083_085.s16','086_089.s16','086_089.s21','091_094.s09','091_094.s14']}
for tile in D['tiles']:
 for row in tile['interactions']:
  if row['step_id'] not in named:continue
  i=row['interaction']; tests=i['grading']['tests']; problems=[]
  tables,_=s._tables(registry,i['public']['workspace'].get('asset_mounts',[]),{},problems)
  assert not problems,problems
  entry,code=s._entry(i,'solution');probe=[s._py_probe(t) for t in tests]
  job=s._py_job('python',i['public']['runtime'].get('packages',[]),[s._py_script('solution',entry,code,s._py_mounts(tables),probe)])
  r=s.node_run(job,s.RUNTIMES['python']['runner'])['results']['solution']
  (B/('dispatch_execution_'+row['step_id']+'.json')).write_text(json.dumps(r,indent=2))
  if not r.get('ok'):print(row['step_id'],r);continue
  for t in tests:
   got,why=s._py_result(t['kind'],t['spec'],r,t['test_id'])
   assert not why,(row['step_id'],t['test_id'],why)
   # Repair only changed scaffold evidence and the named quality report; retain other original answer keys.
   if row['step_id'] in {'mle.tile.091_094.s09','mle.tile.091_094.s14','mle.tile.083_085.s06'} or 'expected' not in t['spec']:
    t['spec']['expected']=got
   else: assert s._py_match(t['kind'],t['spec'],got),(row['step_id'],t['test_id'],'unexpected answer-key change',got)
  print(row['step_id'],'executed',len(tests),'tests')
(B/'interactions.json').write_text(json.dumps(D,indent=2)+'\n')
