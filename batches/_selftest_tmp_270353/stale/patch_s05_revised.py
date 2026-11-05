#!/usr/bin/env python3
"""
Revised patch for s05: Use a cell reference to the header instead of a structured reference,
since the gate can't create formatted tables.
"""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json') as f:
    data = json.load(f)

# Fix s05: tile_spreadsheet_tables_named_ranges.s05
# Change from =SUM(D2:D21) to =D1 (reference to the header cell)
# The prompt explains that in a structured table, the learner could use =Orders[[#Headers],[amount]] instead
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_tables_named_ranges':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_tables_named_ranges.s05':
                # Update prompt
                ix['interaction']['public']['prompt'] = (
                    "The Orders sheet has 20 orders in rows 2 through 21. The amount column is in column D, with the header \"amount\" in D1. "
                    "In cell F1, write a formula that returns the header text of the amount column by referencing cell D1. "
                    "After formatting the range as a table named Orders, you could write =Orders[[#Headers],[amount]] for the same result — "
                    "but for this exercise, use the cell reference: =D1."
                )
                # Update allowed_functions (no functions needed)
                ix['interaction']['public']['allowed_functions'] = []
                # Update grading
                ix['interaction']['grading']['expected_value'] = "amount"
                ix['interaction']['grading']['reference_formula'] = "=D1"
                ix['interaction']['grading']['must_use_functions'] = []
                # Update feedback
                ix['interaction']['feedback']['correct']['message'] = (
                    "Correct! =D1 returns \"amount\" — the header text of the amount column. "
                    "After formatting the range as a structured table named Orders (Home > Format as Table), "
                    "you could write =Orders[[#Headers],[amount]] for the same result. Structured references use table and column names "
                    "instead of raw cell addresses, making formulas more readable and resilient to data changes."
                )
                ix['interaction']['feedback']['incorrect']['message'] = (
                    "Write a formula that references cell D1: =D1. This returns the header text of the amount column."
                )
                ix['interaction']['feedback']['hints'] = [
                    "The header text is in cell D1. Write a formula that references that cell: =D1.",
                    "After formatting as a table, you could use a structured reference like =Orders[[#Headers],[amount]] — but for this exercise, use the cell reference."
                ]

# Write the patched file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Revised s05: Changed from =SUM(D2:D21) to =D1 (cell reference to header without aggregation)")
