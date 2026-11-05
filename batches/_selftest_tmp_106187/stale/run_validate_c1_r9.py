"""Run validate_tile.py for c1 tiles."""
import json
import subprocess
import shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

# Read c1 context
with open(B / 'batch_run_context_c1.json') as f:
    c1_ctx = json.load(f)

# Backup and replace batch_run_context.json with c1 context
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak_r9v')
with open(B / 'batch_run_context.json', 'w') as f:
    json.dump(c1_ctx, f, indent=2)

try:
    result = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/validate_tile.py', str(B), '--strict'],
        capture_output=True, text=True, timeout=600
    )
    print('STDOUT:', result.stdout)
    print('STDERR:', result.stderr[-2000:] if result.stderr else '(none)')
    print('Return code:', result.returncode)
finally:
    # Restore original context
    shutil.copy(B / 'batch_run_context.json.bak_r9v', B / 'batch_run_context.json')
    print("Restored original batch_run_context.json")
