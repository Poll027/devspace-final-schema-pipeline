"""Run assemble_tiles.py for only the affected tile by temporarily modifying batch_run_context.json."""
import json
import subprocess
import sys
import shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

# Read original context
with open(B / 'batch_run_context.json') as f:
    orig_ctx = json.load(f)

# Create a modified context with only the affected tile
mod_ctx = dict(orig_ctx)
mod_ctx['tile_ids'] = ['tile_python_comprehensions_iterating']

# Backup and replace
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak')
with open(B / 'batch_run_context.json', 'w') as f:
    json.dump(mod_ctx, f, indent=2)

try:
    result = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', str(B)],
        capture_output=True, text=True, timeout=300
    )
    print('STDOUT:', result.stdout)
    print('STDERR:', result.stderr[-1000:] if result.stderr else '(none)')
    print('Return code:', result.returncode)
finally:
    # Restore original context
    shutil.copy(B / 'batch_run_context.json.bak', B / 'batch_run_context.json')
    print("Restored original batch_run_context.json")
