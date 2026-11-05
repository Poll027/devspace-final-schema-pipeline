#!/usr/bin/env python3
"""Fix interactions.part.c2.json based on validation errors."""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix 1: tile_spreadsheet_cleaning_cross_sheet.s01 - change variant from 'messy' to 'asset_orders_messy'
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_cleaning_cross_sheet':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_spreadsheet_cleaning_cross_sheet.s01':
                ix = interaction['interaction']
                if ix['type'] == 'spreadsheet_grid':
                    # Find the asset_ref with variant 'messy' and change it
                    asset_ref = ix['public']['asset_ref']
                    if asset_ref.get('variant_id') == 'messy':
                        asset_ref['variant_id'] = 'asset_orders_messy'
                        print(f"Fixed s01: changed variant from 'messy' to 'asset_orders_messy'")

# Fix 2: tile_spreadsheet_cleaning_cross_sheet.s09 - remove annotated_image or fix asset reference
# Fix 3: tile_spreadsheet_sorting_filtering.s01 - remove annotated_image or fix asset reference
# These are likely using asset_orders_clean as an image when it's a dataset
# Let me check what these look like first and remove them if they're not supposed to be there

for tile in data['tiles']:
    if tile['tile_id'] in ['tile_spreadsheet_cleaning_cross_sheet', 'tile_spreadsheet_sorting_filtering']:
        for interaction in tile['interactions']:
            if interaction['step_id'] in ['tile_spreadsheet_cleaning_cross_sheet.s09', 
                                          'tile_spreadsheet_sorting_filtering.s01']:
                ix = interaction['interaction']
                if ix['type'] == 'annotated_image':
                    # Check if it's using asset_orders_clean
                    asset_ref = ix['public'].get('asset_ref', {})
                    if asset_ref.get('asset_id') == 'asset_orders_clean':
                        print(f"ERROR: {interaction['step_id']} uses asset_orders_clean as image - needs manual review")
                        # This needs to be checked against the plan to see what visual is expected

# Fix 4: tile_spreadsheet_cleaning_cross_sheet.s12 - fix allowed_syntax
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_cleaning_cross_sheet':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_spreadsheet_cleaning_cross_sheet.s12':
                ix = interaction['interaction']
                # Fix allowed_syntax - should be syntax descriptors, not literal formulas
                # Based on other exercises, cross-sheet references use descriptors like:
                # 'cross-sheet references', 'relative cell references', etc.
                ix['public']['constraints']['allowed_syntax'] = [
                    'ref_sheet',  # cross-sheet reference like Sheet!A1
                    'ref_rel'     # relative cell reference
                ]
                print(f"Fixed s12: changed allowed_syntax to ['ref_sheet', 'ref_rel']")
                
                # Also need to add something to the starter so it doesn't pass
                # The starter is currently empty (just comments)
                # Let's add a wrong formula
                for f in ix['public']['workspace']['files']:
                    if f.get('editable'):
                        f['content'] = "// The 'Q1 Sales' sheet is mounted and contains order data.\n// Header is in row 1; data starts from row 2.\n// Column B in 'Q1 Sales' holds the city for each order.\n//\n// Task: In cell B2 of this sheet, write a formula that pulls the value\n// from cell B4 on the sheet named 'Q1 Sales'.\n// Note: the sheet name contains a space, so it must be enclosed in single quotes.\n\nB2: =B4\n"
                        print(f"Fixed s12: added wrong starter formula so learner has something to fix")

# Fix 5: tile_spreadsheet_sorting_filtering.s05 - fix reference_formula from D7 to D8
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_sorting_filtering':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_spreadsheet_sorting_filtering.s05':
                ix = interaction['interaction']
                if ix['type'] == 'formula_entry':
                    # The error says D7 gives 9100 but expected is 1800
                    # Looking at the data, D8 has 1800 (LG-2007)
                    ix['grading']['reference_formula'] = '=D8'
                    # Also update the prompt to reference row 8 instead of row 7
                    prompt = ix['public']['prompt']
                    prompt = prompt.replace('row 7', 'row 8')
                    prompt = prompt.replace('D7', 'D8')
                    ix['public']['prompt'] = prompt
                    # Update feedback
                    ix['feedback']['correct']['message'] = ix['feedback']['correct']['message'].replace('=D7', '=D8')
                    ix['feedback']['incorrect']['message'] = ix['feedback']['incorrect']['message'].replace('D7', 'D8').replace('row 7', 'row 8')
                    ix['feedback']['hints'][1] = ix['feedback']['hints'][1].replace('row 7', 'row 8')
                    print(f"Fixed s05: changed reference from D7 to D8")

# Write the fixed data
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("\nDone! Fixed interactions.part.c2.json")
