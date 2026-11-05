"""Run assemble_tiles.py then validate_tile.py for tile_python_functions_scope only."""
import json, subprocess, shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

with open(B / 'batch_run_context.json') as f:
    orig = json.load(f)

mod = dict(orig)
mod['tile_ids'] = ['tile_python_functions_scope']

shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak_s14final')
with open(B / 'batch_run_context.json', 'w') as f:
    json.dump(mod, f, indent=2)

try:
    r1 = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', str(B)],
        capture_output=True, text=True, timeout=600)
    print('ASSEMBLE STDOUT:', r1.stdout[-3000:])
    if r1.stderr: print('ASSEMBLE STDERR:', r1.stderr[-1000:])
    print('ASSEMBLE RC:', r1.returncode)

    if r1.returncode == 0:
        r2 = subprocess.run(
            ['python3', '00_FINAL_PIPELINE_CORE/scripts/validate_tile.py', str(B),
             '--tile', 'tile_python_functions_scope', '--strict'],
            capture_output=True, text=True, timeout=300)
        print('VALIDATE STDOUT:', r2.stdout)
        if r2.stderr: print('VALIDATE STDERR:', r2.stderr[-1000:])
        print('VALIDATE RC:', r2.returncode)
finally:
    shutil.copy(B / 'batch_run_context.json.bak_s14final', B / 'batch_run_context.json')
    print('Restored context.')
