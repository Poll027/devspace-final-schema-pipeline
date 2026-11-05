#!/usr/bin/env python3
"""Fix interactions.part.c2.json - final fixes."""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix: tile_spreadsheet_cleaning_cross_sheet.s12
# 1. Change allowed_syntax to use proper descriptors
# 2. Change target cell to Z1 (so starter doesn't pass)
# 3. Update prompt and feedback
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_cleaning_cross_sheet':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_spreadsheet_cleaning_cross_sheet.s12':
                ix = interaction['interaction']
                
                # Fix allowed_syntax
                ix['public']['constraints']['allowed_syntax'] = [
                    "cross-sheet references",
                    "relative cell reference"
                ]
                
                # Change target cell to Z1
                ix['public']['prompt'] = "The workbook contains a sheet named **'Q1 Sales'** (with a space in the name). In cell Z1 of the current sheet, write a formula that pulls the value from cell B4 on the 'Q1 Sales' sheet.\n\nRemember: when a sheet name contains a space, it must be enclosed in single quotation marks in the reference."
                
                # Update solution
                for f in ix['grading']['solution_files']:
                    f['content'] = "Z1: ='Q1 Sales'!B4\n"
                
                # Update test
                ix['grading']['tests'][0]['spec']['cell'] = 'Z1'
                ix['grading']['tests'][0]['message_on_fail'] = "Z1 should return 'Lagos' (the city in row 4 of the Q1 Sales sheet). Make sure you quote the sheet name: ='Q1 Sales'!B4"
                
                # Update feedback
                ix['feedback']['correct']['message'] = "Well done! ='Q1 Sales'!B4 correctly references cell B4 on the 'Q1 Sales' sheet. The single quotes around the sheet name are required because the name contains a space."
                ix['feedback']['incorrect']['message'] = "The formula should be ='Q1 Sales'!B4. The sheet name 'Q1 Sales' must be enclosed in single quotes because it contains a space. Without the quotes, Excel cannot parse the reference."
                ix['feedback']['hints'] = [
                    "The syntax for a cross-sheet reference is SheetName!CellAddress. When the sheet name has a space, wrap it in single quotes.",
                    "Try typing ='Q1 Sales'!B4 — the single quotes go around the entire sheet name, before the exclamation point."
                ]
                
                # Update starter to be empty (no formula)
                for f in ix['public']['workspace']['files']:
                    if f.get('role') == 'editable':
                        f['content'] = "// The 'Q1 Sales' sheet is mounted and contains order data.\n// Header is in row 1; data starts from row 2.\n// Column B in 'Q1 Sales' holds the city for each order.\n//\n// Task: In cell Z1 of this sheet, write a formula that pulls the value\n// from cell B4 on the sheet named 'Q1 Sales'.\n// Note: the sheet name contains a space, so it must be enclosed in single quotes.\n"
                
                print(f"Fixed s12: changed target to Z1, fixed allowed_syntax, updated prompt/feedback")

# Write the fixed data
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done!")
