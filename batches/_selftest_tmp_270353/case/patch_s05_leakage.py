#!/usr/bin/env python3
"""
Patch s05 interaction to remove COUNTA requirement (blocked by spreadsheet.aggregation_functions).
Change to simple cell reference to test structured table concepts without aggregation functions.
"""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Find and patch the s05 interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_tables_named_ranges':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_spreadsheet_tables_named_ranges.s05':
                # Change to simple cell reference exercise
                interaction['interaction']['public']['prompt'] = (
                    "The Orders sheet has order data in rows 2 through 21 (20 orders total). "
                    "In cell F1, write a formula that references the first order_id value (cell A2). "
                    "This simple reference will help you verify that after formatting the range as a "
                    "structured table, the reference behavior changes: the formula will automatically "
                    "convert to a structured reference like =Orders[@order_id] when you click the cell."
                )
                
                # Update grading to expect the value from A2
                interaction['interaction']['grading']['expected_value'] = "LG-2001"
                interaction['interaction']['grading']['reference_formula'] = "=A2"
                
                # Remove must_use_functions since we're not requiring any specific function
                del interaction['interaction']['grading']['must_use_functions']
                
                # Update feedback
                interaction['interaction']['feedback']['correct']['message'] = (
                    "Correct! =A2 references the first order_id value (LG-2001). After formatting "
                    "this range as a structured table named Orders (Home > Format as Table), Excel "
                    "will display the formula as =A2 but you can also write it as =Orders[@order_id] "
                    "using structured reference syntax. The table will auto-expand when you type a "
                    "value in row 22, and structured references automatically adjust to include new rows."
                )
                
                interaction['interaction']['feedback']['incorrect']['message'] = (
                    "Write a formula that references cell A2: =A2. This references the first order_id value."
                )
                
                interaction['interaction']['feedback']['hints'] = [
                    "Reference cell A2 directly: =A2",
                    "The order_id column is in column A, and the first data value is in row 2."
                ]
                
                print(f"✓ Patched {interaction['step_id']}")
                break

# Write back
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✓ Patch complete")
