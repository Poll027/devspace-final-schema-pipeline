"""Run assemble_tiles.py for all 3 c2 tiles."""
import json
import subprocess
import shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

# Read c2 context
with open(B / 'batch_run_context_c2.json') as f:
    c2_ctx = json.load(f)

print(f"C2 tiles: {c2_ctx['tile_ids']}")

# Backup and replace
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak4')
shutil.copy(B / 'batch_run_context_c2.json', B / 'batch_run_context.json')

try:
    result = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', str(B)],
        capture_output=True, text=True, timeout=600
    )
    print('STDOUT:', result.stdout)
    print('STDERR:', result.stderr[-500:] if result.stderr else '(none)')
    print('Return code:', result.returncode)
finally:
    # Restore original context
    shutil.copy(B / 'batch_run_context.json.bak4', B / 'batch_run_context.json')
    print("Restored original batch_run_context.json")
