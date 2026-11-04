#!/usr/bin/env python3
"""Run assemble_tiles.py for just tile_python_errors_imports."""
import json
import subprocess
import shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

# Read original context
with open(B / 'batch_run_context.json') as f:
    orig_ctx = json.load(f)

# Create single-tile context
single_ctx = dict(orig_ctx)
single_ctx['tile_ids'] = ['tile_python_errors_imports']

print(f"Running assemble for: {single_ctx['tile_ids']}")

# Backup and replace
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak_single')
with open(B / 'batch_run_context.json', 'w') as f:
    json.dump(single_ctx, f, indent=2)

try:
    result = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', str(B)],
        capture_output=True, text=True, timeout=300
    )
    print('STDOUT:', result.stdout)
    print('STDERR:', result.stderr[-2000:] if result.stderr else '(none)')
    print('Return code:', result.returncode)
finally:
    # Restore original context
    shutil.copy(B / 'batch_run_context.json.bak_single', B / 'batch_run_context.json')
    print("Restored original batch_run_context.json")
