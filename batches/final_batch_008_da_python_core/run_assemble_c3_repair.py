#!/usr/bin/env python3
"""Run assemble_tiles.py for all c3 tiles."""
import json
import subprocess
import shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

c3_tiles = [
    "tile_python_functions_scope",
    "tile_python_errors_imports",
    "tile_python_file_io",
    "tile_python_pep8_style"
]

# Read original context
with open(B / 'batch_run_context.json') as f:
    orig_ctx = json.load(f)

# Create c3 context
c3_ctx = dict(orig_ctx)
c3_ctx['tile_ids'] = c3_tiles

print(f"C3 tiles: {c3_ctx['tile_ids']}")

# Backup and replace
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak_c3repair')
with open(B / 'batch_run_context.json', 'w') as f:
    json.dump(c3_ctx, f, indent=2)

try:
    result = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', str(B)],
        capture_output=True, text=True, timeout=600
    )
    print('STDOUT:', result.stdout)
    print('STDERR:', result.stderr[-2000:] if result.stderr else '(none)')
    print('Return code:', result.returncode)
finally:
    # Restore original context
    shutil.copy(B / 'batch_run_context.json.bak_c3repair', B / 'batch_run_context.json')
    print("Restored original batch_run_context.json")
