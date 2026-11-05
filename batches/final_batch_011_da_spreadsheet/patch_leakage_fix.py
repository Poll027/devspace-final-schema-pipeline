#!/usr/bin/env python3
"""
Patch interactions.part.c3.json to fix leakage issues:
- s05: Remove SUM (blocked aggregation_functions), use structured reference without aggregation
- s08: Remove SUM (blocked aggregation_functions), use named range without aggregation
- s10: Remove OR (blocked logical_functions), use arithmetic/comparison operators
"""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json') as f:
    data = json.load(f)

# Fix s05: tile_spreadsheet_tables_named_ranges.s05
# Change from =SUM(D2:D21) to =Orders[[#Headers],[amount]]
# This tests structured reference syntax without using aggregation functions
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_tables_named_ranges':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_tables_named_ranges.s05':
                # Update prompt
                ix['interaction']['public']['prompt'] = (
                    "The Orders sheet has 20 orders in rows 2 through 21, formatted as a table named Orders. "
                    "The amount column is in column D. In cell F1, write a formula using a structured reference "
                    "that returns the header text of the amount column. Use the syntax Orders[[#Headers],[amount]]."
                )
                # Update allowed_functions (no functions needed)
                ix['interaction']['public']['allowed_functions'] = []
                # Update grading
                ix['interaction']['grading']['expected_value'] = "amount"
                ix['interaction']['grading']['reference_formula'] = "=Orders[[#Headers],[amount]]"
                ix['interaction']['grading']['must_use_functions'] = []
                # Update feedback
                ix['interaction']['feedback']['correct']['message'] = (
                    "Correct! =Orders[[#Headers],[amount]] returns \"amount\" — the header text of the amount column. "
                    "This structured reference uses the table name (Orders) and the special #Headers specifier to access "
                    "the column header, demonstrating how structured references name table parts directly instead of using raw cell addresses."
                )
                ix['interaction']['feedback']['incorrect']['message'] = (
                    "Use the structured reference syntax: =Orders[[#Headers],[amount]]. "
                    "This references the header of the amount column in the Orders table."
                )
                ix['interaction']['feedback']['hints'] = [
                    "The syntax for a table header is: =TableName[[#Headers],[ColumnName]].",
                    "For the Orders table and amount column, write: =Orders[[#Headers],[amount]]."
                ]

# Fix s08: tile_spreadsheet_tables_named_ranges.s08
# Change from =SUM(C2:C21) to =FirstDelivery where FirstDelivery is defined as C2
# This tests named range usage without using aggregation functions
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_tables_named_ranges':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_tables_named_ranges.s08':
                # Update prompt
                ix['interaction']['public']['prompt'] = (
                    "The delivery_minutes column is in column C (C2:C21). Define a named range called FirstDelivery "
                    "for cell C2 using the Name Box. Then in cell G1, write a formula that references C2 using the "
                    "named range: =FirstDelivery."
                )
                # Update allowed_functions (no functions needed)
                ix['interaction']['public']['allowed_functions'] = []
                # Update grading
                ix['interaction']['grading']['expected_value'] = 28  # C2 value from asset_orders_clean
                ix['interaction']['grading']['reference_formula'] = "=FirstDelivery"
                ix['interaction']['grading']['must_use_functions'] = []
                # Update feedback
                ix['interaction']['feedback']['correct']['message'] = (
                    "Correct! =FirstDelivery returns 28 — the delivery_minutes value in C2. "
                    "By defining FirstDelivery as the name for C2, you can write =FirstDelivery instead of =C2. "
                    "Named ranges make formulas more readable and easier to maintain."
                )
                ix['interaction']['feedback']['incorrect']['message'] = (
                    "First, select cell C2 and type FirstDelivery in the Name Box (to the left of the formula bar), then press Enter. "
                    "Then in G1, write: =FirstDelivery. This references C2 using the name you defined."
                )
                ix['interaction']['feedback']['hints'] = [
                    "To define a named range: select the cell, click the Name Box, type the name, and press Enter.",
                    "Once FirstDelivery is defined for C2, the formula is simply =FirstDelivery."
                ]

# Fix s10: tile_spreadsheet_formatting_validation.s10
# Change from =OR(E2="Delivered",E2="Pending",E2="Cancelled") to =(E2="Delivered")+(E2="Pending")+(E2="Cancelled")>0
# This tests understanding of allowed values without using logical functions
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_formatting_validation':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_formatting_validation.s10':
                # Update prompt
                ix['interaction']['public']['prompt'] = (
                    "You want to restrict the status column (E2:E21) so that users can only enter Delivered, Pending, or Cancelled. "
                    "In cell G1, write a formula that returns TRUE if the value in E2 is one of these three allowed values, and FALSE otherwise. "
                    "Use arithmetic and comparison operators: =(E2=\"Delivered\")+(E2=\"Pending\")+(E2=\"Cancelled\")>0"
                )
                # Update allowed_functions (no functions needed)
                ix['interaction']['public']['allowed_functions'] = []
                # Update grading
                ix['interaction']['grading']['expected_value'] = True  # E2 is "Delivered"
                ix['interaction']['grading']['reference_formula'] = '=(E2="Delivered")+(E2="Pending")+(E2="Cancelled")>0'
                ix['interaction']['grading']['must_use_functions'] = []
                # Update feedback
                ix['interaction']['feedback']['correct']['message'] = (
                    "Correct! =(E2=\"Delivered\")+(E2=\"Pending\")+(E2=\"Cancelled\")>0 returns TRUE because E2 contains \"Delivered\", "
                    "which is one of the allowed values. Each comparison returns 1 (TRUE) or 0 (FALSE); adding them gives a count of matches, "
                    "and >0 checks if at least one match exists. In data validation, you would use Data → Data Validation → Allow: List "
                    "with Source set to Delivered,Pending,Cancelled to create a dropdown that restricts entry to these three values."
                )
                ix['interaction']['feedback']['incorrect']['message'] = (
                    "Use arithmetic and comparison operators to check if E2 equals any of the three allowed values: "
                    "=(E2=\"Delivered\")+(E2=\"Pending\")+(E2=\"Cancelled\")>0. Each comparison returns 1 or 0; adding them counts matches; >0 checks if any match exists."
                )
                ix['interaction']['feedback']['hints'] = [
                    "Each comparison like E2=\"Delivered\" returns TRUE (1) or FALSE (0). Adding three comparisons counts how many match.",
                    "Use quotes around text values: E2=\"Delivered\". The full formula is =(E2=\"Delivered\")+(E2=\"Pending\")+(E2=\"Cancelled\")>0."
                ]

# Write the patched file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patched interactions.part.c3.json:")
print("- s05: Changed from =SUM(D2:D21) to =Orders[[#Headers],[amount]] (structured reference without aggregation)")
print("- s08: Changed from =SUM(C2:C21) to =FirstDelivery (named range without aggregation)")
print("- s10: Changed from =OR(...) to =(E2=\"Delivered\")+(E2=\"Pending\")+(E2=\"Cancelled\")>0 (arithmetic/comparison without logical functions)")
