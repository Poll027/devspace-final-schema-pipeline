#!/usr/bin/env python3
"""Patch screens.json to fix s13 lineage.teaching_block_ids."""
import json

with open('batches/final_batch_012_da_viz/screens.json') as f:
    data = json.load(f)

# Find the tile
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_figures_layout_plotting':
        # Find s13
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_figures_layout_plotting.s13':
                # Fix lineage.teaching_block_ids to match plan
                step['lineage']['teaching_block_ids'] = [
                    'viz.matplotlib_figure_axes#tb5',
                    'viz.pyplot_basic_plotting#tb4'
                ]
                print(f"Fixed s13 lineage.teaching_block_ids in screens.json")
                break
        break

# Write back
with open('batches/final_batch_012_da_viz/screens.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patched screens.json")
