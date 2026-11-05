#!/usr/bin/env python3
"""Patch screens to fix s09.b01 missing fact_ids."""
import json

# Fix screens.part.c0_canary.json
with open('batches/final_batch_012_da_viz/screens.part.c0_canary.json') as f:
    data = json.load(f)

tile = data['tiles'][0]
for step in tile['steps']:
    if step['step_id'] == 'tile_viz_figures_layout_plotting.s09':
        for block in step['blocks']:
            if block['block_id'] == 'tile_viz_figures_layout_plotting.s09.b01':
                block['lineage']['fact_ids'] = [
                    'viz.pyplot_basic_plotting#f1',
                    'viz.pyplot_basic_plotting#f2'
                ]
                print(f"Fixed s09.b01 fact_ids in screens.part.c0_canary.json")
                break
        break

with open('batches/final_batch_012_da_viz/screens.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

# Fix screens.json
with open('batches/final_batch_012_da_viz/screens.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_figures_layout_plotting':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_figures_layout_plotting.s09':
                for block in step['blocks']:
                    if block['block_id'] == 'tile_viz_figures_layout_plotting.s09.b01':
                        block['lineage']['fact_ids'] = [
                            'viz.pyplot_basic_plotting#f1',
                            'viz.pyplot_basic_plotting#f2'
                        ]
                        print(f"Fixed s09.b01 fact_ids in screens.json")
                        break
                break
        break

with open('batches/final_batch_012_da_viz/screens.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patched s09.b01 fact_ids")
