#!/usr/bin/env python3
"""
Fix screens.part.c1.json:
1. Change tile_spreadsheet_aggregation_logical.s10 type from 'check' to 'hands_on'
2. Replace spreadsheet_grid block in tile_spreadsheet_text_date_conditional_agg.s01
   with a before_after block (required by plan's planned_visual_block_type)
"""
import json
import copy

with open('batches/final_batch_011_da_spreadsheet/screens.part.c1.json') as f:
    screens = json.load(f)

for tile in screens['tiles']:
    # Fix 1: Change s10 type from 'check' to 'hands_on'
    if tile['tile_id'] == 'tile_spreadsheet_aggregation_logical':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_aggregation_logical.s10':
                if step['type'] == 'check':
                    step['type'] = 'hands_on'
                    # hands_on steps use 'Practice' eyebrow, not 'Quick Check'
                    step['eyebrow'] = 'Practice'
                    # lede should reflect the hands_on nature
                    step['lede'] = 'Write nested IF formulas with AND and OR to classify delivery times.'
                    print(f"Fixed s10 type: check -> hands_on")

    # Fix 2: Replace spreadsheet_grid block in s01 with before_after block
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for step in tile['steps']:
            if step['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s01':
                # Find and replace the spreadsheet_grid block with a before_after block
                new_blocks = []
                for block in step.get('blocks', []):
                    if block['type'] == 'spreadsheet_grid':
                        # Replace with before_after block
                        before_after = {
                            "type": "before_after",
                            "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.b3",
                            "before": {
                                "type": "spreadsheet_grid",
                                "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.b3.before",
                                "asset_ref": {
                                    "asset_id": "asset_orders_clean"
                                },
                                "range": "B1:E4",
                                "sheet_name": "Orders",
                                "show_formula_bar": True,
                                "annotations": [
                                    {
                                        "target": "B1",
                                        "text": "city — separate column"
                                    },
                                    {
                                        "target": "E1",
                                        "text": "status — separate column"
                                    }
                                ]
                            },
                            "after": {
                                "type": "spreadsheet_grid",
                                "block_id": "tile_spreadsheet_text_date_conditional_agg.s01.b3.after",
                                "asset_ref": {
                                    "asset_id": "asset_orders_clean"
                                },
                                "range": "B1:G4",
                                "sheet_name": "Orders",
                                "show_formula_bar": True,
                                "cells": [
                                    {
                                        "ref": "G2",
                                        "formula": "=TEXTJOIN(\", \",TRUE,B2,E2)",
                                        "note": "Combines city and status with delimiter"
                                    },
                                    {
                                        "ref": "G3",
                                        "formula": "=TEXTJOIN(\", \",TRUE,B3,E3)"
                                    }
                                ],
                                "annotations": [
                                    {
                                        "target": "G1",
                                        "text": "Full_Name — combined with TEXTJOIN"
                                    },
                                    {
                                        "target": "G2",
                                        "text": "=TEXTJOIN(\", \",TRUE,B2,E2)"
                                    }
                                ]
                            },
                            "change_summary": "TEXTJOIN(\", \", TRUE, B2, E2) combines the city and status columns with a comma-space delimiter; setting ignore_empty to TRUE means a blank status cell produces no trailing comma.",
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
                        new_blocks.append(before_after)
                        print(f"Replaced spreadsheet_grid with before_after in s01")
                    else:
                        new_blocks.append(block)
                step['blocks'] = new_blocks

with open('batches/final_batch_011_da_spreadsheet/screens.part.c1.json', 'w') as f:
    json.dump(screens, f, indent=2, ensure_ascii=False)

print("screens.part.c1.json fixed")
