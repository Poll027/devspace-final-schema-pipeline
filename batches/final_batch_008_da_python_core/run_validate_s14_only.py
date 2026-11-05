"""Run validate_tile.py for tile_python_functions_scope only, with timeout."""
import subprocess
import sys

result = subprocess.run(
    ['python3', '00_FINAL_PIPELINE_CORE/scripts/validate_tile.py',
     'batches/final_batch_008_da_python_core/',
     '--tile', 'tile_python_functions_scope',
     '--strict'],
    capture_output=True, text=True, timeout=60
)
print('STDOUT:', result.stdout)
if result.stderr:
    print('STDERR:', result.stderr[-2000:])
print('Return code:', result.returncode)
