#!/usr/bin/env python3
"""
Repair script for pedagogy review findings in screens.part.c1.json

BLOCKING tile_spreadsheet_text_date_conditional_agg/s01:
Remove computed_values from the before_after block's "after" grid.
Per GENERATOR.md: "spreadsheet_grid formulas are run in the engine: 
give cells[].formula, never type computed_values (assemble derives them)."
"""

import json

# Load the screens part file
with open('batches/final_batch_011_da_spreadsheet/screens.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and fix tile_spreadsheet_text_date_conditional_agg.s01
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s01':
                for block in step['blocks']:
                    if block.get('type') == 'before_after':
                        # Remove computed_values from the after block
                        if 'computed_values' in block['after']:
                            print(f"Removing computed_values from {block['block_id']}.after")
                            print(f"  Was: {block['after']['computed_values']}")
                            del block['after']['computed_values']
                            print("  Removed (assemble will compute from formulas)")

# Write back
with open('batches/final_batch_011_da_spreadsheet/screens.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatch complete.")
