"""Assemble all 3 c2 tiles then validate them, all under the c2 batch_run_context."""
import json, subprocess, shutil
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')
shutil.copy(B / 'batch_run_context.json', B / 'batch_run_context.json.bak5')
shutil.copy(B / 'batch_run_context_c2.json', B / 'batch_run_context.json')

try:
    r1 = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', str(B)],
        capture_output=True, text=True, timeout=600)
    print('ASSEMBLE STDOUT:', r1.stdout)
    print('ASSEMBLE STDERR:', r1.stderr[-300:] if r1.stderr else '')
    print('ASSEMBLE RC:', r1.returncode)

    r2 = subprocess.run(
        ['python3', '00_FINAL_PIPELINE_CORE/scripts/validate_tile.py', str(B), '--strict'],
        capture_output=True, text=True, timeout=600)
    print('VALIDATE STDOUT:', r2.stdout)
    print('VALIDATE STDERR:', r2.stderr[-300:] if r2.stderr else '')
    print('VALIDATE RC:', r2.returncode)
finally:
    shutil.copy(B / 'batch_run_context.json.bak5', B / 'batch_run_context.json')
    print("Restored.")
