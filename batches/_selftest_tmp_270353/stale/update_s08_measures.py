#!/usr/bin/env python3
"""
Update measures for s08 to match what the exercise actually tests.
The exercise now tests understanding of range notation by asking for the first cell
of a described range, but doesn't require writing a colon range reference.
"""

import json

# Read the interactions file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c0_canary.json', 'r') as f:
    data = json.load(f)

# Find and update the s08 interaction measures
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_grid_references':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_grid_references.s08':
                print(f"Updating measures for {ix['step_id']}...")
                
                # The exercise now tests:
                # 1. Understanding that C2:C21 is a range (mentioned in prompt)
                # 2. Identifying that C2 is the first cell (column C, row 2)
                # 3. Writing a cell reference (=C2)
                
                # Remove write_rectangular_range_reference_using_colon_notation
                # since the learner doesn't write a colon range
                
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
                    }
                ]
                
                # Update anchors to match
                ix['interaction']['anchors'] = [
                    "spreadsheet.cell_references_ranges#practice",
                    "spreadsheet.cell_references_ranges#assessment:identify_single_cell_by_column_letter_and_row_number",
                    "spreadsheet.cell_references_ranges#assessment:write_correct_cell_or_range_reference_for_formula_requirement"
                ]
                
                print("  Removed write_rectangular_range_reference_using_colon_notation measure")
                print("  Kept identify_single_cell_by_column_letter_and_row_number")
                print("  Kept write_correct_cell_or_range_reference_for_formula_requirement")

# Write the updated file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nUpdate complete!")
