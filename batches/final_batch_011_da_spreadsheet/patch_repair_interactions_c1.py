#!/usr/bin/env python3
"""Repair interactions.part.c1.json and screens.json for the gate errors."""
import json

# Fix 1: tile_spreadsheet_text_date_conditional_agg.s03 - change TRUE to TRUE() in reference_formula
with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json') as f:
    interactions = json.load(f)

for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s03':
                ix = interaction_entry['interaction']
                if ix['type'] == 'formula_entry':
                    # Change TRUE to TRUE() in reference_formula
                    old_ref = ix['grading']['reference_formula']
                    new_ref = old_ref.replace(',TRUE,', ',TRUE(),')
                    ix['grading']['reference_formula'] = new_ref
                    print(f"Fixed s03 reference_formula: {old_ref} -> {new_ref}")

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'w') as f:
    json.dump(interactions, f, indent=2)

# Fix 2: tile_spreadsheet_aggregation_logical.s10 - change screens.json step type from check to hands_on
with open('batches/final_batch_011_da_spreadsheet/screens.json') as f:
    screens = json.load(f)

for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_aggregation_logical':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_aggregation_logical.s10':
                old_type = step['type']
                step['type'] = 'hands_on'
                print(f"Fixed s10 type: {old_type} -> hands_on")

# Fix 3: tile_spreadsheet_text_date_conditional_agg.s01 - add before_after block
for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s01':
                # Check if there's already a before_after block
                has_before_after = any(b.get('type') == 'before_after' for b in step.get('blocks', []))
                if not has_before_after:
                    # Add a before_after block
                    before_after_block = {
                        "type": "before_after",
                        "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.ba1",
                        "before": {
                            "type": "spreadsheet_grid",
                            "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.ba1.before",
                            "asset_ref": {
                                "asset_id": "asset_orders_clean"
                            },
                            "range": "A1:B4",
                            "sheet_name": "Orders",
                            "show_formula_bar": False,
                            "cells": [],
                            "annotations": [
                                {
                                    "target": "A2",
                                    "text": "First_Name: Jane"
                                },
                                {
                                    "target": "B2",
                                    "text": "Last_Name: Smith"
                                }
                            ]
                        },
                        "after": {
                            "type": "spreadsheet_grid",
                            "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.ba1.after",
                            "asset_ref": {
                                "asset_id": "asset_orders_clean"
                            },
                            "range": "A1:C4",
                            "sheet_name": "Orders",
                            "show_formula_bar": True,
                            "cells": [
                                {
                                    "ref": "C2",
                                    "formula": "=TEXTJOIN(\" \",TRUE(),A2,B2)",
                                    "note": "Combines first and last name"
                                }
                            ],
                            "annotations": [
                                {
                                    "target": "C2",
                                    "text": "=TEXTJOIN(\" \",TRUE(),A2,B2) → \"Jane Smith\""
                                }
                            ]
                        },
                        "change_summary": "TEXTJOIN with a space delimiter combines the First_Name and Last_Name columns into a single Full_Name column, with ignore_empty set to TRUE() to skip any blank cells.",
                        "lineage": {
                            "concept_ids": [
                                "spreadsheet.text_combining"
                            ],
                            "fact_ids": [
                                "spreadsheet.text_combining#f1",
                                "spreadsheet.text_combining#f2",
                                "spreadsheet.text_combining#f3"
                            ],
                            "teaching_block_ids": [
                                "spreadsheet.text_combining#tb1",
                                "spreadsheet.text_combining#tb2"
                            ],
                            "anchors": [
                                "spreadsheet.text_combining#visual"
                            ]
                        }
                    }
                    # Replace the existing spreadsheet_grid block (b3) with the before_after
                    new_blocks = []
                    for b in step.get('blocks', []):
                        if b.get('block_id') == 'tile_spreadsheet_text_date_conditional_agg.s01.b3':
                            # Replace with before_after
                            new_blocks.append(before_after_block)
                            print(f"Replaced s01.b3 with before_after block")
                        else:
                            new_blocks.append(b)
                    step['blocks'] = new_blocks

with open('batches/final_batch_011_da_spreadsheet/screens.json', 'w') as f:
    json.dump(screens, f, indent=2)

print("All fixes applied successfully")
