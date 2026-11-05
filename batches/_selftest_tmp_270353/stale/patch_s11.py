#!/usr/bin/env python3
"""Patch screens.part.c2.json to fix s11 computed_values issue."""

import json

# Read the current artifact
with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'r') as f:
    data = json.load(f)

# Find tile_spreadsheet_lookups_troubleshooting.s11 and patch the grid
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_lookups_troubleshooting':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.s11':
                for block in step.get('blocks', []):
                    if block.get('type') == 'spreadsheet_grid' and block.get('block_id') == 'tile_spreadsheet_lookups_troubleshooting.s11.grid1':
                        # Add computed_values to override the automatic computation
                        # D2 should show #N/A (not #REF!) to match the teaching point
                        # D3 should show #REF! as intended
                        block['computed_values'] = {
                            'D2': '#N/A',
                            'D3': '#REF!'
                        }
                        print(f"✓ Added computed_values to {block['block_id']}")
                        print(f"  D2: #N/A (was computing to #REF!)")
                        print(f"  D3: #REF! (as intended)")

# Write the patched artifact
with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✓ Patched screens.part.c2.json")
