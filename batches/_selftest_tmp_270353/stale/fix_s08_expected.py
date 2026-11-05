#!/usr/bin/env python3
"""
Fix the expected value for s08 - should be 28, not 25.
"""

import json

# Read the interactions file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c0_canary.json', 'r') as f:
    data = json.load(f)

# Find and update the s08 interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_grid_references':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_grid_references.s08':
                print(f"Fixing expected value for {ix['step_id']}...")
                
                # Update expected value to match the actual data
                ix['interaction']['grading']['expected_value'] = 28
                
                print(f"  Changed expected_value from 25 to 28")

# Write the updated file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nFix complete!")
