"""Run validate_tile.py using batch_run_context_c2.json as batch_run_context.json."""
import json
import subprocess
import shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

# Backup and replace
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak2')
shutil.copy(B / 'batch_run_context_c2.json', B / 'batch_run_context.json')

try:
    result = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/validate_tile.py', str(B), '--strict'],
        capture_output=True, text=True, timeout=300
    )
    print('STDOUT:', result.stdout)
    print('STDERR:', result.stderr[-500:] if result.stderr else '(none)')
    print('Return code:', result.returncode)
finally:
    # Restore original context
    shutil.copy(B / 'batch_run_context.json.bak2', B / 'batch_run_context.json')
    print("Restored original batch_run_context.json")
