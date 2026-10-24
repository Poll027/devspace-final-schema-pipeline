#!/usr/bin/env python3
"""Fix the missing asset reference in screens.part.c1.json"""
import json

# Read the screens file
with open('screens.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and fix the asset reference
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_stats_correlation':
        for step in tile['steps']:
            if step['step_id'] == 'tile_stats_correlation.s01':
                for block in step['blocks']:
                    if block.get('type') == 'chart' and block.get('block_id') == 'tile_stats_correlation.s01.chart1':
                        if block['asset_ref']['asset_id'] == 'ds_delivery_scatter':
                            print(f"Fixing asset_id in {block['block_id']}")
                            print(f"  Old: {block['asset_ref']['asset_id']}")
                            block['asset_ref']['asset_id'] = 'ds_delivery_orders_extended'
                            print(f"  New: {block['asset_ref']['asset_id']}")

# Write back
with open('screens.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Done!")
