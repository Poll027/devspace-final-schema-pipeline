#!/usr/bin/env python3
"""
Patch script to replace annotated_image blocks with spreadsheet_grid or diagram blocks.
The registry has no image assets, so we must use the allowed alternates.
"""
import json

def create_cross_sheet_spreadsheet_grid():
    """
    Create spreadsheet_grid showing cross-sheet reference syntax.
    This is better than diagram for showing formula syntax.
    """
    return {
        "type": "spreadsheet_grid",
        "block_id": "tile_spreadsheet_cleaning_cross_sheet.s09.img1",
        "sheet_name": "Orders",
        "range": "A1:C4",
        "show_formula_bar": True,
        "cells": [
            {
                "ref": "A1",
                "value": "Example"
            },
            {
                "ref": "B1",
                "value": "Formula"
            },
            {
                "ref": "C1",
                "value": "Explanation"
            },
            {
                "ref": "A2",
                "value": "Simple reference"
            },
            {
                "ref": "B2",
                "formula": "=Drivers!B1"
            },
            {
                "ref": "C2",
                "value": "Sheet name, !, cell address"
            },
            {
                "ref": "A3",
                "value": "Name with space"
            },
            {
                "ref": "B3",
                "formula": "='January Revenue'!A1"
            },
            {
                "ref": "C3",
                "value": "Single quotes required for spaces"
            },
            {
                "ref": "A4",
                "value": "External workbook"
            },
            {
                "ref": "B4",
                "formula": "=[Budget.xlsx]Annual!C10"
            },
            {
                "ref": "C4",
                "value": "Workbook in square brackets"
            }
        ],
        "annotations": [
            {
                "target": "B2",
                "text": "Sheet name (Drivers), exclamation point, cell address (B1)"
            },
            {
                "target": "B3",
                "text": "Single quotes wrap sheet names containing spaces"
            },
            {
                "target": "B4",
                "text": "Square brackets contain external workbook name"
            }
        ],
        "lineage": {
            "concept_ids": ["spreadsheet.cross_sheet_references"],
            "teaching_block_ids": ["spreadsheet.cross_sheet_references#tb3"],
            "fact_ids": ["spreadsheet.cross_sheet_references#f3"],
            "anchors": ["spreadsheet.cross_sheet_references#visual"]
        }
    }

def create_sort_dialog_diagram():
    """
    Create structured diagram showing Sort dialog with two levels.
    Using 'container' diagram_kind to represent UI elements.
    """
    return {
        "type": "diagram",
        "block_id": "tile_spreadsheet_sorting_filtering.s01.img1",
        "diagram_kind": "container",
        "title": "Excel Sort Dialog with Two Levels",
        "nodes": [
            {
                "id": "dialog",
                "label": "Sort Dialog",
                "kind": "container"
            },
            {
                "id": "level1",
                "label": "Level 1: Sort by order_date, Order: Oldest to Newest",
                "kind": "level",
                "group": "dialog"
            },
            {
                "id": "level1_column",
                "label": "order_date",
                "kind": "column_selector",
                "group": "level1"
            },
            {
                "id": "level1_order",
                "label": "Oldest to Newest",
                "kind": "order_selector",
                "group": "level1"
            },
            {
                "id": "level2",
                "label": "Level 2: Then by amount, Order: Largest to Smallest",
                "kind": "level",
                "group": "dialog"
            },
            {
                "id": "level2_column",
                "label": "amount",
                "kind": "column_selector",
                "group": "level2"
            },
            {
                "id": "level2_order",
                "label": "Largest to Smallest",
                "kind": "order_selector",
                "group": "level2"
            },
            {
                "id": "note1",
                "label": "Each level has its own independent Order dropdown",
                "kind": "annotation"
            }
        ],
        "edges": [
            {
                "from": "dialog",
                "to": "level1",
                "label": "contains",
                "order": 1
            },
            {
                "from": "dialog",
                "to": "level2",
                "label": "contains",
                "order": 2
            },
            {
                "from": "level1",
                "to": "level1_column",
                "label": "sort by"
            },
            {
                "from": "level1",
                "to": "level1_order",
                "label": "order"
            },
            {
                "from": "level2",
                "to": "level2_column",
                "label": "then by"
            },
            {
                "from": "level2",
                "to": "level2_order",
                "label": "order"
            }
        ],
        "layout": "auto",
        "alt_text": "Excel Sort dialog with two levels configured. Level 1 shows Sort by: order_date, Order: Oldest to Newest. Level 2 shows Then by: amount, Order: Largest to Smallest. Each level has its own independent Order dropdown.",
        "lineage": {
            "concept_ids": ["spreadsheet.sorting"],
            "teaching_block_ids": [
                "spreadsheet.sorting#tb1",
                "spreadsheet.sorting#tb2",
                "spreadsheet.sorting#tb3"
            ],
            "fact_ids": [
                "spreadsheet.sorting#f1",
                "spreadsheet.sorting#f2",
                "spreadsheet.sorting#f3",
                "spreadsheet.sorting#f4"
            ],
            "anchors": ["spreadsheet.sorting#visual"]
        }
    }

def main():
    # Read the screens file
    with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'r') as f:
        data = json.load(f)
    
    # Find and replace the annotated_image blocks
    replacements_made = 0
    
    for tile in data['tiles']:
        for step in tile['steps']:
            if 'blocks' not in step:
                continue
            
            for i, block in enumerate(step['blocks']):
                if block.get('type') == 'diagram' and block.get('block_id') in [
                    'tile_spreadsheet_cleaning_cross_sheet.s09.img1',
                    'tile_spreadsheet_sorting_filtering.s01.img1'
                ]:
                    block_id = block['block_id']
                    
                    if block_id == 'tile_spreadsheet_cleaning_cross_sheet.s09.img1':
                        step['blocks'][i] = create_cross_sheet_spreadsheet_grid()
                        replacements_made += 1
                        print(f"✓ Replaced {block_id} with spreadsheet_grid")
                    
                    elif block_id == 'tile_spreadsheet_sorting_filtering.s01.img1':
                        step['blocks'][i] = create_sort_dialog_diagram()
                        replacements_made += 1
                        print(f"✓ Replaced {block_id} with structured diagram")
    
    # Write the patched file
    with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nTotal replacements: {replacements_made}")
    print("Patched file written successfully.")

if __name__ == '__main__':
    main()
