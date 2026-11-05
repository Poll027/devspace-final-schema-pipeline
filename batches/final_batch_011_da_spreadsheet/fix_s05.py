#!/usr/bin/env python3
"""Patch the s05 interaction to use a formula that depends on data, not just a header."""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Find and fix the problematic interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_tables_named_ranges':
        for ix_wrapper in tile['interactions']:
            if ix_wrapper['step_id'] == 'tile_spreadsheet_tables_named_ranges.s05':
                ix = ix_wrapper['interaction']
                
                # Change the prompt to ask for a formula that counts the data rows
                # This will change when rows are added/removed
                ix['public']['prompt'] = (
                    "The Orders sheet has order data in rows 2 through 21 (20 orders total). "
                    "In cell F1, write a formula that counts how many rows contain data in the "
                    "order_id column (column A, rows 2 through 21). Use the COUNTA function to "
                    "count non-empty cells in the range A2:A21."
                )
                
                # Update the reference formula to count data rows
                ix['grading']['reference_formula'] = '=COUNTA(A2:A21)'
                
                # Update expected value - COUNTA of 20 rows with data
                ix['grading']['expected_value'] = 20
                
                # Update must_use_functions to require COUNTA
                ix['grading']['must_use_functions'] = ['COUNTA']
                
                # Update feedback messages
                ix['feedback']['correct']['message'] = (
                    "Correct! =COUNTA(A2:A21) counts 20 non-empty cells in the order_id column. "
                    "After formatting this range as a structured table named Orders (Home > Format as Table), "
                    "the table will auto-expand when you type a value in row 22. You could then use "
                    "=COUNTA(Orders[order_id]) to count rows using a structured reference that automatically "
                    "adjusts as the table grows."
                )
                
                ix['feedback']['incorrect']['message'] = (
                    "Write a formula that counts non-empty cells in the range A2:A21 using the COUNTA function: "
                    "=COUNTA(A2:A21). This counts how many order_id values are present."
                )
                
                ix['feedback']['hints'] = [
                    "Use the COUNTA function to count non-empty cells in a range: =COUNTA(A2:A21).",
                    "The order_id column is in column A, and the data spans rows 2 through 21."
                ]
                
                print("Fixed interaction tile_spreadsheet_tables_named_ranges.s05")
                break

# Write the patched file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch complete")
