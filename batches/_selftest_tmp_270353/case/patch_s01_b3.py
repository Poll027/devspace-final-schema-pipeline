"""
Patch: replace the annotated_image block (b3) in step s01 with a diagram block.
The diagram uses diagram_kind='container' to show the grid structure:
columns A/B/C, rows 1/2/3, cell B2 highlighted, and sheet tabs.
"""
import json, copy

path = "batches/final_batch_011_da_spreadsheet/screens.part.c0_canary.json"
with open(path) as f:
    doc = json.load(f)

# Locate tile_spreadsheet_grid_references -> s01 -> b3
tile = next(t for t in doc["tiles"] if t["tile_id"] == "tile_spreadsheet_grid_references")
step = next(s for s in tile["steps"] if s["step_id"] == "tile_spreadsheet_grid_references.s01")

# Find the annotated_image block
b3_idx = next(i for i, b in enumerate(step["blocks"]) if b.get("block_id") == "tile_spreadsheet_grid_references.s01.b3")

# Build replacement diagram block
diagram_block = {
    "type": "diagram",
    "block_id": "tile_spreadsheet_grid_references.s01.b3",
    "diagram_kind": "container",
    "title": "Spreadsheet grid: columns, rows, cells, and sheet tabs",
    "nodes": [
        {
            "id": "col_header_row",
            "label": "Column headers",
            "kind": "header_row",
            "group": "grid"
        },
        {
            "id": "col_a",
            "label": "A",
            "kind": "column_header",
            "group": "grid"
        },
        {
            "id": "col_b",
            "label": "B",
            "kind": "column_header",
            "group": "grid"
        },
        {
            "id": "col_c",
            "label": "C",
            "kind": "column_header",
            "group": "grid"
        },
        {
            "id": "row1",
            "label": "Row 1",
            "kind": "row_header",
            "group": "grid"
        },
        {
            "id": "row2",
            "label": "Row 2",
            "kind": "row_header",
            "group": "grid"
        },
        {
            "id": "row3",
            "label": "Row 3",
            "kind": "row_header",
            "group": "grid"
        },
        {
            "id": "cell_b2",
            "label": "B2 — column B, row 2",
            "kind": "highlighted_cell",
            "group": "grid"
        },
        {
            "id": "sheet1_tab",
            "label": "Sheet1",
            "kind": "sheet_tab",
            "group": "tabs"
        },
        {
            "id": "sheet2_tab",
            "label": "Sheet2",
            "kind": "sheet_tab",
            "group": "tabs"
        }
    ],
    "edges": [
        {
            "from": "col_b",
            "to": "cell_b2",
            "label": "column B"
        },
        {
            "from": "row2",
            "to": "cell_b2",
            "label": "row 2"
        }
    ],
    "layout": "manual",
    "positions": {
        "col_header_row": {"x": 200, "y": 10},
        "col_a": {"x": 100, "y": 40},
        "col_b": {"x": 200, "y": 40},
        "col_c": {"x": 300, "y": 40},
        "row1": {"x": 10, "y": 80},
        "row2": {"x": 10, "y": 130},
        "row3": {"x": 10, "y": 180},
        "cell_b2": {"x": 200, "y": 130},
        "sheet1_tab": {"x": 80, "y": 260},
        "sheet2_tab": {"x": 180, "y": 260}
    },
    "alt_text": "A small spreadsheet grid showing column letters A, B, C across the top and row numbers 1, 2, 3 down the side. Cell B2 is highlighted at the intersection of column B and row 2. Two sheet tabs at the bottom are labelled Sheet1 and Sheet2.",
    "lineage": {
        "concept_ids": [
            "spreadsheet.grid_model"
        ],
        "fact_ids": [
            "spreadsheet.grid_model#f1",
            "spreadsheet.grid_model#f2"
        ],
        "teaching_block_ids": [
            "spreadsheet.grid_model#tb1",
            "spreadsheet.grid_model#tb2"
        ],
        "anchors": [
            "spreadsheet.grid_model#visual"
        ]
    }
}

step["blocks"][b3_idx] = diagram_block

with open(path, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print("Patch applied: annotated_image replaced with diagram at s01.b3")
