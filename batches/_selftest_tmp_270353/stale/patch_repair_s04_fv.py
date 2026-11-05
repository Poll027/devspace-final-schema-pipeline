"""
Repair patch: tile_spreadsheet_formatting_validation.s04
- Change step type from check to hands_on (plan says hands_on)
- Change interaction type from choice to formula_entry (plan says formula_entry)
"""
import json, copy

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json') as f:
    data = json.load(f)

# Find the tile and step
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_formatting_validation':
        for entry in tile['interactions']:
            if entry['step_id'] == 'tile_spreadsheet_formatting_validation.s04':
                ix = entry['interaction']
                # Change type from choice to formula_entry
                ix['type'] = 'formula_entry'
                # Add practice anchor (hands_on requires it)
                ix['anchors'] = [
                    'spreadsheet.conditional_formatting#practice',
                    'spreadsheet.conditional_formatting#assessment:apply_conditional_formatting_rule_for_given_condition'
                ]
                # Remove choice-specific public fields, replace with formula_entry fields
                old_public = ix['public']
                ix['public'] = {
                    'prompt': (
                        'The delivery_minutes column (C2:C21) contains the delivery time in minutes for each order. '
                        'A conditional formatting rule highlights every cell in that column whose value is less than 30 in red. '
                        'In cell F1, write a formula that counts how many cells in C2:C21 contain a value less than 30 — '
                        'the same cells the conditional formatting rule would highlight. '
                        'Use COUNTIF with the range C2:C21 and the criterion "<30".'
                    ),
                    'asset_ref': {
                        'asset_id': 'asset_orders_clean',
                        'variant_id': None
                    },
                    'sheet_name': 'Orders',
                    'target_cell': 'F1',
                    'allowed_functions': ['COUNTIF']
                }
                # Replace grading
                ix['grading'] = {
                    'expected_value': 4,
                    'reference_formula': '=COUNTIF(C2:C21,"<30")',
                    'must_use_functions': ['COUNTIF'],
                    'forbid_hardcoded_values': True
                }
                # Update feedback
                ix['feedback'] = {
                    'correct': {
                        'message': (
                            'Correct! =COUNTIF(C2:C21,"<30") returns 4 — there are 4 orders with a delivery time below 30 minutes. '
                            'These are exactly the cells that the conditional formatting Less Than rule would highlight in red.'
                        )
                    },
                    'incorrect': {
                        'message': (
                            'Use COUNTIF with the delivery_minutes range and the criterion "<30": =COUNTIF(C2:C21,"<30"). '
                            'COUNTIF counts all cells in the range that satisfy the condition — the same cells the conditional formatting rule highlights.'
                        )
                    },
                    'hints': [
                        'COUNTIF takes two arguments: the range and the criterion. The criterion for "less than 30" is written as "<30" in double quotes.',
                        'The delivery_minutes column is column C, rows 2 through 21. The criterion string must include the comparison operator: "<30".'
                    ],
                    'remediation_step_id': 'tile_spreadsheet_formatting_validation.r01'
                }
                print('Patched tile_spreadsheet_formatting_validation.s04: choice->formula_entry, check->hands_on')
                break

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print('Done.')
