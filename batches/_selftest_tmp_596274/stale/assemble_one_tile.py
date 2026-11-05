#!/usr/bin/env python3
"""Assemble just tile_viz_custom_multi_panel."""
import sys
sys.path.insert(0, '../../00_FINAL_PIPELINE_CORE/scripts')

from pathlib import Path
from finlib import load, save
import subprocess

B = Path('.')
tile_id = 'tile_viz_custom_multi_panel'

# Run assemble_tiles.py but only for this tile
# Modify the batch_run_context.json temporarily
ctx = load(B / 'batch_run_context.json')
original_tiles = ctx['tile_ids']
ctx['tile_ids'] = [tile_id]
save(B / 'batch_run_context.json', ctx)

try:
    # Run assemble
    result = subprocess.run(
        ['python3', '../../00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py', '.'],
        cwd=B,
        capture_output=True,
        text=True,
        timeout=60
    )
    print(result.stdout)
    if result.stderr:
        print('STDERR:', result.stderr)
    print('Return code:', result.returncode)
finally:
    # Restore original tile list
    ctx['tile_ids'] = original_tiles
    save(B / 'batch_run_context.json', ctx)
