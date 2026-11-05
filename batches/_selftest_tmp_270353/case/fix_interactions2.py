#!/usr/bin/env python3
"""Fix the starter for s12."""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix: tile_spreadsheet_cleaning_cross_sheet.s12 - add wrong starter so it doesn't pass
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_cleaning_cross_sheet':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_spreadsheet_cleaning_cross_sheet.s12':
                ix = interaction['interaction']
                # Add a wrong formula to the starter
                for f in ix['public']['workspace']['files']:
                    if f.get('role') == 'editable':
                        # Add a wrong formula that references the wrong sheet
                        f['content'] = "// The 'Q1 Sales' sheet is mounted and contains order data.\n// Header is in row 1; data starts from row 2.\n// Column B in 'Q1 Sales' holds the city for each order.\n//\n// Task: In cell B2 of this sheet, write a formula that pulls the value\n// from cell B4 on the sheet named 'Q1 Sales'.\n// Note: the sheet name contains a space, so it must be enclosed in single quotes.\n\nB2: =B4\n"
                        print(f"Fixed s12: added wrong starter formula (=B4 instead of ='Q1 Sales'!B4)")

# Write the fixed data
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done!")
