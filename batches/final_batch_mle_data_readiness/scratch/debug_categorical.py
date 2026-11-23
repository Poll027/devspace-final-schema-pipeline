import sys,json
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts');from checkers import sandbox
b=Path('batches/final_batch_mle.region.data_readiness');d=json.loads((b/'interactions.json').read_text());ix=next(i['interaction'] for t in d['tiles'] for i in t['interactions'] if i['step_id']=='mle.tile.012_015.s16');entry,code=sandbox._entry(ix,'solution')
wrapped='import traceback\ntry:\n'+''.join('    '+l+'\n' for l in code.splitlines())+'except Exception:\n    print(traceback.format_exc())\n'
r=sandbox.node_run(sandbox._py_job('python',ix['public']['runtime']['packages'],[sandbox._py_script('debug',entry,wrapped,[],[])]),sandbox.RUNTIMES['python']['runner'])
(b/'scratch/categorical_debug.json').write_text(json.dumps(r,indent=2));print(r)
