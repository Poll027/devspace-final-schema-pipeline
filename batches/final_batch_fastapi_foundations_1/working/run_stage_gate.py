"""Run unchanged stage gate with an offline, batch-local copy of pinned sandbox dependencies.
The pack's node_modules symlink points to an empty directory. No core or registry files are edited.
"""
from pathlib import Path
import sys,runpy
root=Path.cwd(); sys.path.insert(0,str(root/'00_FINAL_PIPELINE_CORE/scripts'))
from checkers import sandbox
sandbox.SANDBOX=root/'batches/final_batch_foundations_1/working/pinned_sandbox'
name=sys.argv[1];sys.argv=[str(root/'00_FINAL_PIPELINE_CORE/scripts'/name),'batches/final_batch_foundations_1']+sys.argv[2:]
runpy.run_path(sys.argv[0],run_name='__main__')
