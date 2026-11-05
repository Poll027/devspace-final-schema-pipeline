#!/usr/bin/env python3
"""Patch screens.part.c2.json to fix s11 formula to produce #N/A instead of #REF!."""

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
                        # Change the D2 formula to produce #N/A instead of #REF!
                        # The formula should reference a valid range but look for a value that doesn't exist
                        for cell in block.get('cells', []):
                            if cell['ref'] == 'D2':
                                # Change from =VLOOKUP(B2,Drivers!A:B,2,FALSE) to a formula that produces #N/A
                                # Use a lookup value that doesn't exist in the data
                                old_formula = cell['formula']
                                cell['formula'] = '=VLOOKUP("NOTFOUND",A:B,2,FALSE)'
                                print(f"✓ Changed D2 formula in {block['block_id']}")
                                print(f"  Old: {old_formula}")
                                print(f"  New: {cell['formula']}")
                                print(f"  This will produce #N/A (lookup value not found) instead of #REF!")
                        
                        # Remove computed_values if it exists (let assemble compute it)
                        if 'computed_values' in block:
                            del block['computed_values']
                            print(f"✓ Removed computed_values (will be recomputed by assemble)")

# Write the patched artifact
with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✓ Patched screens.part.c2.json")
