#!/usr/bin/env python3
"""Assemble all tiles one by one."""
import sys
sys.path.insert(0, '../../00_FINAL_PIPELINE_CORE/scripts')

from pathlib import Path
from finlib import load, save
import subprocess

B = Path('.')
ctx = load(B / 'batch_run_context.json')
all_tiles = ctx['tile_ids']

for tile_id in all_tiles:
    print(f'\n=== Assembling {tile_id} ===')
    ctx['tile_ids'] = [tile_id]
    save(B / 'batch_run_context.json', ctx)
    
    try:
        result = subprocess.run(
            ['python3', '../../00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', '.'],
            cwd=B,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f'✓ {tile_id} assembled')
        else:
            print(f'✗ {tile_id} FAILED')
            print(result.stdout)
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print(f'✗ {tile_id} TIMEOUT')

# Restore original
ctx['tile_ids'] = all_tiles
save(B / 'batch_run_context.json', ctx)
print('\n=== All tiles assembled ===')
