#!/usr/bin/env python3
"""
Patch interactions.part.c3.json to change s04 and s10 from choice to formula_entry.

Note: These concepts (conditional_formatting and data_validation) are UI-based operations.
The glossary teaches using the UI, not writing formulas. However, the plan specifies
formula_entry, so we must match it. We'll create formula-based exercises that test
the underlying logic, even though this doesn't perfectly match the glossary practice.
"""

import json

# Read the interactions file
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Find the tile and update the interactions
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_formatting_validation':
        for i, interaction in enumerate(tile['interactions']):
            if interaction['step_id'] == 'tile_spreadsheet_formatting_validation.s04':
                # Change from choice to formula_entry
                # For conditional formatting: write a formula that checks if a value should be highlighted
                tile['interactions'][i] = {
                    "step_id": "tile_spreadsheet_formatting_validation.s04",
                    "interaction": {
                        "type": "formula_entry",
                        "interaction_id": "ix.tile_spreadsheet_formatting_validation.s04",
                        "difficulty": "core",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "spreadsheet.conditional_formatting",
                                "capability": "apply_conditional_formatting_rule_for_given_condition",
                                "fact_ids": ["f1", "f2"]
                            }
                        ],
                        "anchors": [
                            "spreadsheet.conditional_formatting#practice",
                            "spreadsheet.conditional_formatting#assessment:apply_conditional_formatting_rule_for_given_condition"
                        ],
                        "public": {
                            "prompt": "You want to highlight all cells in the delivery_minutes column (C2:C21) that contain values less than 30. In cell F1, write a formula that returns TRUE if the value in C2 is less than 30, and FALSE otherwise. This formula logic is what a conditional formatting rule would use to determine which cells to highlight.",
                            "asset_ref": {
                                "asset_id": "asset_orders_clean",
                                "variant_id": None
                            },
                            "sheet_name": "Orders",
                            "target_cell": "F1"
                        },
                        "grading": {
                            "expected_value": True,  # C2 is 28, which is < 30
                            "reference_formula": "=C2<30",
                            "forbid_hardcoded_values": False  # This is a logical test, not a calculation
                        },
                        "feedback": {
                            "correct": {
                                "message": "Correct! =C2<30 returns TRUE because 28 is less than 30. In conditional formatting, you would use Home → Conditional Formatting → Highlight Cells Rules → Less Than to apply this logic to the entire range C2:C21, highlighting all cells where the value is less than 30."
                            },
                            "incorrect": {
                                "message": "Write a formula that compares C2 to 30: =C2<30. This returns TRUE if the value is less than 30, FALSE otherwise."
                            },
                            "hints": [
                                "Use the less than operator (<) to compare C2 to 30.",
                                "The formula should return TRUE or FALSE based on whether the value meets the condition."
                            ],
                            "remediation_step_id": "tile_spreadsheet_formatting_validation.r01"
                        }
                    }
                }
                print(f"Changed {interaction['step_id']} to formula_entry")
            
            elif interaction['step_id'] == 'tile_spreadsheet_formatting_validation.s10':
                # Change from choice to formula_entry
                # For data validation: write a formula that checks if a value is valid
                tile['interactions'][i] = {
                    "step_id": "tile_spreadsheet_formatting_validation.s10",
                    "interaction": {
                        "type": "formula_entry",
                        "interaction_id": "ix.tile_spreadsheet_formatting_validation.s10",
                        "difficulty": "core",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "spreadsheet.data_validation",
                                "capability": "configure_dropdown_list_validation_with_source_values",
                                "fact_ids": ["f2"]
                            }
                        ],
                        "anchors": [
                            "spreadsheet.data_validation#practice",
                            "spreadsheet.data_validation#assessment:configure_dropdown_list_validation_with_source_values"
                        ],
                        "public": {
                            "prompt": "You want to restrict the status column (E2:E21) so that users can only enter Delivered, Pending, or Cancelled. In cell G1, write a formula that returns TRUE if the value in E2 is one of these three allowed values, and FALSE otherwise. Use OR to check if E2 equals any of the three values.",
                            "asset_ref": {
                                "asset_id": "asset_orders_clean",
                                "variant_id": None
                            },
                            "sheet_name": "Orders",
                            "target_cell": "G1",
                            "allowed_functions": ["OR"]
                        },
                        "grading": {
                            "expected_value": True,  # E2 is "Delivered", which is valid
                            "reference_formula": '=OR(E2="Delivered",E2="Pending",E2="Cancelled")',
                            "must_use_functions": ["OR"],
                            "forbid_hardcoded_values": False  # This is a logical test
                        },
                        "feedback": {
                            "correct": {
                                "message": "Correct! =OR(E2=\"Delivered\",E2=\"Pending\",E2=\"Cancelled\") returns TRUE because E2 contains \"Delivered\", which is one of the allowed values. In data validation, you would use Data → Data Validation → Allow: List with Source set to Delivered,Pending,Cancelled to create a dropdown that restricts entry to these three values."
                            },
                            "incorrect": {
                                "message": "Use OR to check if E2 equals any of the three allowed values: =OR(E2=\"Delivered\",E2=\"Pending\",E2=\"Cancelled\")."
                            },
                            "hints": [
                                "OR returns TRUE if any of its arguments is TRUE. Check if E2 equals each of the three allowed values.",
                                "Use quotes around text values: E2=\"Delivered\"."
                            ],
                            "remediation_step_id": "tile_spreadsheet_formatting_validation.r03"
                        }
                    }
                }
                print(f"Changed {interaction['step_id']} to formula_entry")

# Write back
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nDone! Changed 2 interactions from choice to formula_entry.")
