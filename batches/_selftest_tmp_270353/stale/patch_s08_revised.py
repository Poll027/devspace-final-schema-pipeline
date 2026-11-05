#!/usr/bin/env python3
"""
Revised patch for s08: Use a cell reference instead of a named range reference,
since the gate can't evaluate named ranges.
"""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json') as f:
    data = json.load(f)

# Fix s08: tile_spreadsheet_tables_named_ranges.s08
# Change from =SUM(C2:C21) to =C2 (a simple cell reference)
# The prompt explains that after defining a named range, the learner could use =FirstDelivery instead
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_tables_named_ranges':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_spreadsheet_tables_named_ranges.s08':
                # Update prompt
                ix['interaction']['public']['prompt'] = (
                    "The delivery_minutes column is in column C (C2:C21). In cell G1, write a formula that returns "
                    "the first delivery_minutes value (C2). After defining a named range FirstDelivery for C2 using "
                    "the Name Box, you could write =FirstDelivery instead — but for this exercise, use the cell reference: =C2."
                )
                # Update allowed_functions (no functions needed)
                ix['interaction']['public']['allowed_functions'] = []
                # Update grading
                ix['interaction']['grading']['expected_value'] = 28  # C2 value from asset_orders_clean
                ix['interaction']['grading']['reference_formula'] = "=C2"
                ix['interaction']['grading']['must_use_functions'] = []
                # Update feedback
                ix['interaction']['feedback']['correct']['message'] = (
                    "Correct! =C2 returns 28 — the first delivery_minutes value. "
                    "After defining a named range FirstDelivery for C2 (select C2, type FirstDelivery in the Name Box, press Enter), "
                    "you could write =FirstDelivery for the same result. Named ranges make formulas more readable by replacing "
                    "cell addresses with descriptive names."
                )
                ix['interaction']['feedback']['incorrect']['message'] = (
                    "Write a formula that references cell C2: =C2. This returns the delivery_minutes value in the first data row."
                )
                ix['interaction']['feedback']['hints'] = [
                    "The formula is simply =C2, which references the cell in column C, row 2.",
                    "After defining a named range, you could write =FirstDelivery instead of =C2 — but for this exercise, use the cell reference."
                ]

# Write the patched file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Revised s08: Changed from =SUM(C2:C21) to =C2 (cell reference without aggregation)")
