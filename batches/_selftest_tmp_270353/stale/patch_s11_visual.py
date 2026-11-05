#!/usr/bin/env python3
"""Patch step s11 to fix visual contradiction with annotation."""
import json

with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'r') as f:
    data = json.load(f)

# Find step s11 and fix the visual
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_lookups_troubleshooting':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_lookups_troubleshooting.s11':
                # Find the spreadsheet_grid block
                for block in step['blocks']:
                    if block['type'] == 'spreadsheet_grid' and block['block_id'] == 'tile_spreadsheet_lookups_troubleshooting.s11.grid1':
                        # Change to show errors in column D (a new column for demonstration)
                        # This avoids contradicting the amount column (C)
                        block['range'] = 'A1:D5'
                        block['cells'] = [
                            {
                                "ref": "D2",
                                "formula": "=VLOOKUP(B2,Drivers!A:B,2,FALSE)",
                                "note": "Returns #N/A if driver ID not found in Drivers sheet"
                            },
                            {
                                "ref": "D3",
                                "formula": "=SUM(#REF!)",
                                "note": "#REF! after referenced column was deleted"
                            }
                        ]
                        block['annotations'] = [
                            {
                                "target": "D2",
                                "text": "#N/A — lookup value not found in source data"
                            },
                            {
                                "target": "D3",
                                "text": "#REF! — formula references a deleted range"
                            }
                        ]
                        print(f"Fixed step s11 visual: moved error formulas from column C to column D")
                        break

with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch complete")
