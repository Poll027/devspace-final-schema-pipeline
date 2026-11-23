import json,sys
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox as s
B=Path('batches/final_batch_mle.region.production_serving');p=B/'interactions.json';d=json.loads(p.read_text());registry=json.loads((B/'scenario_asset_registry.json').read_text())
for tile in d['tiles']:
 for e in tile['interactions']:
  sid=e['step_id'];i=e['interaction']
  if sid not in ['mle.tile.060_063.s16','mle.tile.066_067.s11']:continue
  pub=i['public'];tests=i['grading']['tests'];problems=[]
  tables,_=s._tables(registry,pub['workspace']['asset_mounts'],{},problems)
  assert not problems, problems
  solution=i['grading']['solution_files'][0]['content']
  script=s._py_script('solution',pub['workspace']['entry'],solution,s._py_mounts(tables),[s._py_probe(t) for t in tests])
  result=s.node_run(s._py_job(pub['runtime']['kind'],pub['runtime']['packages'],[script]),s.RUNTIMES['python']['runner'])['results']['solution']
  for test in tests:
   if test['kind']=='value_equals':
    computed,why=s._py_result(test['kind'],test['spec'],result,test['test_id'])
    assert why is None,why
    assert s._py_match(test['kind'],test['spec'],computed), 'Modified solution must preserve the declared report contract'
    test['spec']['expected']=computed
    test['message_on_fail']=('Implement bounded reading, per-chunk frozen prediction and writes, JSON Lines reopening/decoding, and learner-authored schema and unique key coverage assertions; retain all fixture and IO-observer outcomes.' if sid.endswith('s16') else 'Implement handler timing across JSON decoding, prediction and encoding on success and handled errors; calculate deadline-qualified outcomes using every external attempt, reconcile absent handler records, and compute np.mean and np.std(..., ddof=0).')
    print(sid, 'computed expected from pinned runtime; output contract unchanged')
p.write_text(json.dumps(d,indent=2)+'\n')
