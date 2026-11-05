"""Run assemble_tiles.py + validate_tile.py for only tile_python_functions_scope."""
import json
import subprocess
import shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

# Read original context
with open(B / 'batch_run_context.json') as f:
    orig_ctx = json.load(f)

# Create a modified context with only the affected tile
mod_ctx = dict(orig_ctx)
mod_ctx['tile_ids'] = ['tile_python_functions_scope']

# Backup and replace
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak_s14')
with open(B / 'batch_run_context.json', 'w') as f:
    json.dump(mod_ctx, f, indent=2)

try:
    # Run assemble
    print("=== ASSEMBLE ===")
    result = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', str(B)],
        capture_output=True, text=True, timeout=180
    )
    print('STDOUT:', result.stdout[-3000:] if result.stdout else '(none)')
    if result.stderr:
        print('STDERR:', result.stderr[-2000:])
    print('Return code:', result.returncode)

    if result.returncode != 0:
        print("Assembly failed, skipping validate")
    else:
        # Run validate
        print("\n=== VALIDATE ===")
        result2 = subprocess.run(
            ['python3', '00_FINAL_PIPELINE_CORE/scripts/validate_tile.py', str(B),
             '--tile', 'tile_python_functions_scope', '--strict'],
            capture_output=True, text=True, timeout=120
        )
        print('STDOUT:', result2.stdout)
        if result2.stderr:
            print('STDERR:', result2.stderr[-2000:])
        print('Return code:', result2.returncode)
finally:
    # Restore original context
    shutil.copy(B / 'batch_run_context.json.bak_s14', B / 'batch_run_context.json')
    print("\nRestored original batch_run_context.json")
