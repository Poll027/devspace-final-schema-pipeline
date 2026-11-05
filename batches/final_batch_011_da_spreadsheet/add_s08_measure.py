#!/usr/bin/env python3
"""
Add write_rectangular_range_reference_using_colon_notation measure back to s08.
The exercise tests understanding of colon range notation (C2:C21) even though
the answer is a single cell reference. The prompt explains the range notation
and requires the learner to understand it.
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
                print(f"Adding measure to {ix['step_id']}...")
                
                # Add the measure back
                ix['interaction']['measures'] = [
                    {
                        "concept_id": "spreadsheet.cell_references_ranges",
                        "capability": "identify_single_cell_by_column_letter_and_row_number",
                        "fact_ids": ["f2"]
                    },
                    {
                        "concept_id": "spreadsheet.cell_references_ranges",
                        "capability": "write_correct_cell_or_range_reference_for_formula_requirement",
                        "fact_ids": ["f1", "f2"]
                    },
                    {
                        "concept_id": "spreadsheet.cell_references_ranges",
                        "capability": "write_rectangular_range_reference_using_colon_notation",
                        "fact_ids": ["f3"]
                    }
                ]
                
                # Update anchors to match
                ix['interaction']['anchors'] = [
                    "spreadsheet.cell_references_ranges#practice",
                    "spreadsheet.cell_references_ranges#assessment:identify_single_cell_by_column_letter_and_row_number",
                    "spreadsheet.cell_references_ranges#assessment:write_correct_cell_or_range_reference_for_formula_requirement",
                    "spreadsheet.cell_references_ranges#assessment:write_rectangular_range_reference_using_colon_notation"
                ]
                
                print("  Added write_rectangular_range_reference_using_colon_notation measure")
                print("  The prompt explains C2:C21 notation, testing understanding of colon ranges")

# Write the updated file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nUpdate complete!")
