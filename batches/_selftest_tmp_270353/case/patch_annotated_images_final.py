#!/usr/bin/env python3
"""
Patch script to replace annotated_image blocks with diagram blocks.
The registry has no image assets, so we must use the allowed alternate: diagram.
Both blocks will be replaced with structured diagrams.
"""
import json

def create_cross_sheet_diagram():
    """
    Create structured diagram showing cross-sheet reference syntax.
    Using 'mapping' diagram_kind to show syntax components.
    """
    return {
        "type": "diagram",
        "block_id": "tile_spreadsheet_cleaning_cross_sheet.s09.img1",
        "diagram_kind": "mapping",
        "title": "Cross-Sheet Reference Syntax",
        "nodes": [
            {
                "id": "example1",
                "label": "Drivers!B1",
                "kind": "formula"
            },
            {
                "id": "sheet_name",
                "label": "Drivers",
                "kind": "component",
                "group": "example1"
            },
            {
                "id": "exclamation",
                "label": "!",
                "kind": "separator",
                "group": "example1"
            },
            {
                "id": "cell_ref",
                "label": "B1",
                "kind": "component",
                "group": "example1"
            },
            {
                "id": "example2",
                "label": "'January Revenue'!A1",
                "kind": "formula"
            },
            {
                "id": "quoted_sheet",
                "label": "'January Revenue'",
                "kind": "component",
                "group": "example2"
            },
            {
                "id": "exclamation2",
                "label": "!",
                "kind": "separator",
                "group": "example2"
            },
            {
                "id": "cell_ref2",
                "label": "A1",
                "kind": "component",
                "group": "example2"
            },
            {
                "id": "example3",
                "label": "[Budget.xlsx]Annual!C10",
                "kind": "formula"
            },
            {
                "id": "workbook",
                "label": "[Budget.xlsx]",
                "kind": "component",
                "group": "example3"
            },
            {
                "id": "sheet3",
                "label": "Annual",
                "kind": "component",
                "group": "example3"
            },
            {
                "id": "exclamation3",
                "label": "!",
                "kind": "separator",
                "group": "example3"
            },
            {
                "id": "cell_ref3",
                "label": "C10",
                "kind": "component",
                "group": "example3"
            },
            {
                "id": "note1",
                "label": "Sheet name (no spaces, no quotes needed)",
                "kind": "annotation"
            },
            {
                "id": "note2",
                "label": "Single quotes required when name contains space",
                "kind": "annotation"
            },
            {
                "id": "note3",
                "label": "Square brackets around external workbook name",
                "kind": "annotation"
            }
        ],
        "edges": [
            {
                "from": "example1",
                "to": "sheet_name",
                "label": "sheet"
            },
            {
                "from": "example1",
                "to": "exclamation",
                "label": "separator"
            },
            {
                "from": "example1",
                "to": "cell_ref",
                "label": "cell"
            },
            {
                "from": "sheet_name",
                "to": "note1",
                "label": "explains"
            },
            {
                "from": "example2",
                "to": "quoted_sheet",
                "label": "sheet"
            },
            {
                "from": "example2",
                "to": "exclamation2",
                "label": "separator"
            },
            {
                "from": "example2",
                "to": "cell_ref2",
                "label": "cell"
            },
            {
                "from": "quoted_sheet",
                "to": "note2",
                "label": "explains"
            },
            {
                "from": "example3",
                "to": "workbook",
                "label": "workbook"
            },
            {
                "from": "example3",
                "to": "sheet3",
                "label": "sheet"
            },
            {
                "from": "example3",
                "to": "exclamation3",
                "label": "separator"
            },
            {
                "from": "example3",
                "to": "cell_ref3",
                "label": "cell"
            },
            {
                "from": "workbook",
                "to": "note3",
                "label": "explains"
            }
        ],
        "layout": "auto",
        "alt_text": "Formula bar showing cross-sheet reference syntax. Three examples: Drivers!B1 (simple reference with sheet name, exclamation point, and cell address), 'January Revenue'!A1 (single quotes wrap sheet names containing spaces), and [Budget.xlsx]Annual!C10 (square brackets contain external workbook name).",
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
    
    # Find and replace the blocks
    replacements_made = 0
    
    for tile in data['tiles']:
        for step in tile['steps']:
            if 'blocks' not in step:
                continue
            
            for i, block in enumerate(step['blocks']):
                block_id = block.get('block_id')
                
                if block_id == 'tile_spreadsheet_cleaning_cross_sheet.s09.img1':
                    step['blocks'][i] = create_cross_sheet_diagram()
                    replacements_made += 1
                    print(f"✓ Replaced {block_id} with diagram (mapping)")
                
                elif block_id == 'tile_spreadsheet_sorting_filtering.s01.img1':
                    step['blocks'][i] = create_sort_dialog_diagram()
                    replacements_made += 1
                    print(f"✓ Replaced {block_id} with diagram (container)")
    
    # Write the patched file
    with open('batches/final_batch_011_da_spreadsheet/screens.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nTotal replacements: {replacements_made}")
    print("Patched file written successfully.")

if __name__ == '__main__':
    main()
