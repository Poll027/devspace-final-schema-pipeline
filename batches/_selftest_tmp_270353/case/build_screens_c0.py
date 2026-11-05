"""Build screens.part.c0_canary.json for tile_spreadsheet_grid_references."""
import json

tile_id = "tile_spreadsheet_grid_references"

# ── helpers ──────────────────────────────────────────────────────────────────
def qid(concept, local):
    """Qualify a local fact/tb/anchor id."""
    return f"{concept}#{local}"

GM = "spreadsheet.grid_model"
CR = "spreadsheet.cell_references_ranges"

# ── STEPS ────────────────────────────────────────────────────────────────────

# s01 – explainer, grid_model, tb1+tb2, f1+f2, annotated_image visual
# word_budget: 125
s01 = {
    "step_id": f"{tile_id}.s01",
    "type": "explainer",
    "concept_ids": [GM],
    "eyebrow": "The Spreadsheet Grid",
    "title": "Every cell has an address",
    "lede": "A spreadsheet is a grid of cells, each one named by its column letter and row number.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s01.b1",
            "role": "intro",
            "text": (
                "Open a new workbook and you already have structure before you type anything. "
                "Cells are grouped into rows and columns, forming a grid, and each cell can hold "
                "a number, text, or a formula. Think of it like a table where every slot has its own name."
            ),
            "lineage": {
                "concept_ids": [GM],
                "fact_ids": [qid(GM, "f1")],
                "teaching_block_ids": [qid(GM, "tb1")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{tile_id}.s01.b2",
            "role": "definition",
            "text": (
                "Each cell's name is its address: the column letter followed by the row number. "
                "Excel uses the A1 reference style by default — columns are letters, rows are numbers. "
                "So the cell at the intersection of column B and row 2 is called B2. "
                "If you type a delivery city into the second row of the second column, you're typing into B2."
            ),
            "lineage": {
                "concept_ids": [GM],
                "fact_ids": [qid(GM, "f2")],
                "teaching_block_ids": [qid(GM, "tb2")]
            }
        },
        {
            "type": "annotated_image",
            "block_id": f"{tile_id}.s01.b3",
            "asset_id": "asset_grid_model_visual",
            "alt_text": (
                "A small spreadsheet grid showing column letters A, B, C across the top and row numbers "
                "1, 2, 3 down the side. Cell B2 is highlighted with a callout showing its address. "
                "Two sheet tabs at the bottom are labelled Sheet1 and Sheet2."
            ),
            "hotspots": [
                {
                    "x": 0.33, "y": 0.05, "w": 0.12, "h": 0.08,
                    "label": "Column letters (A, B, C…)",
                    "detail": "Columns run left to right and are labelled with letters."
                },
                {
                    "x": 0.02, "y": 0.35, "w": 0.10, "h": 0.08,
                    "label": "Row numbers (1, 2, 3…)",
                    "detail": "Rows run top to bottom and are labelled with numbers."
                },
                {
                    "x": 0.33, "y": 0.35, "w": 0.12, "h": 0.12,
                    "label": "Cell B2",
                    "detail": "The intersection of column B and row 2 — its address is B2."
                },
                {
                    "x": 0.10, "y": 0.90, "w": 0.18, "h": 0.08,
                    "label": "Sheet tabs",
                    "detail": "Sheet1 and Sheet2 are two separate grids inside the same workbook."
                }
            ],
            "lineage": {
                "concept_ids": [GM],
                "fact_ids": [qid(GM, "f1"), qid(GM, "f2")],
                "teaching_block_ids": [qid(GM, "tb1"), qid(GM, "tb2")],
                "anchors": [qid(GM, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [GM],
        "fact_ids": [qid(GM, "f1"), qid(GM, "f2")],
        "teaching_block_ids": [qid(GM, "tb1"), qid(GM, "tb2")],
        "anchors": [qid(GM, "visual")]
    }
}

# s02 – explainer, grid_model, tb3, f3+f4, no visual
# word_budget: 87
s02 = {
    "step_id": f"{tile_id}.s02",
    "type": "explainer",
    "concept_ids": [GM],
    "eyebrow": "The Spreadsheet Grid",
    "title": "One workbook, many sheets",
    "lede": "A workbook can hold multiple sheets, each with its own grid.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s02.b1",
            "role": "mechanism",
            "text": (
                "A workbook is not limited to one grid. It can contain multiple sheets — "
                "you can add as many as you need. By default Excel names them Sheet1, Sheet2, Sheet3 "
                "and so on; the name appears on the sheet tab at the bottom and can be renamed. "
                "A QuickDeliver workbook might start with Sheet1 for orders and Sheet2 for drivers, "
                "then you rename each tab to Orders and Drivers."
            ),
            "lineage": {
                "concept_ids": [GM],
                "fact_ids": [qid(GM, "f3"), qid(GM, "f4")],
                "teaching_block_ids": [qid(GM, "tb3")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [GM],
        "fact_ids": [qid(GM, "f3"), qid(GM, "f4")],
        "teaching_block_ids": [qid(GM, "tb3")]
    }
}

# s03 – check, grid_model, f1+f2, framing only (no blocks)
s03 = {
    "step_id": f"{tile_id}.s03",
    "type": "check",
    "concept_ids": [GM],
    "eyebrow": "Quick Check",
    "title": "Cell address vs. cell contents",
    "lede": "Test your understanding of what a cell address is and what a cell can contain.",
    "reward": {"gems": 5, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": [GM],
        "fact_ids": [qid(GM, "f1"), qid(GM, "f2")],
        "teaching_block_ids": [],
        "anchors": [qid(GM, "assessment:distinguish_cell_contents_and_address")]
    }
}

# s04 – hands_on, grid_model, f1+f2+f3+f4, framing only
s04 = {
    "step_id": f"{tile_id}.s04",
    "type": "hands_on",
    "concept_ids": [GM],
    "eyebrow": "Practice",
    "title": "Navigate the QuickDeliver workbook",
    "lede": "Identify cell addresses and sheet names in the Orders workbook.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [GM],
        "fact_ids": [qid(GM, "f1"), qid(GM, "f2"), qid(GM, "f3"), qid(GM, "f4")],
        "teaching_block_ids": [],
        "anchors": [
            qid(GM, "practice"),
            qid(GM, "assessment:identify_cell_address_from_grid_position"),
            qid(GM, "assessment:identify_sheet_name_from_workbook_tab"),
            qid(GM, "assessment:distinguish_cell_contents_and_address")
        ]
    }
}

# s05 – explainer, cell_references_ranges, tb1+tb2+tb3, f1+f2+f3, spreadsheet_grid visual
# word_budget: 158
s05 = {
    "step_id": f"{tile_id}.s05",
    "type": "explainer",
    "concept_ids": [CR],
    "eyebrow": "Cell References and Ranges",
    "title": "Pointing at one cell or many",
    "lede": "A reference tells Excel exactly which cell or cells to use in a formula.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s05.b1",
            "role": "intro",
            "text": (
                "A reference identifies a cell or a range of cells on a worksheet and tells Excel "
                "where to look for the values a formula needs. Without a reference, a formula "
                "can only work with numbers you type directly — references let it reach into the grid."
            ),
            "lineage": {
                "concept_ids": [CR],
                "fact_ids": [qid(CR, "f1")],
                "teaching_block_ids": [qid(CR, "tb1")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{tile_id}.s05.b2",
            "role": "definition",
            "text": (
                "In the A1 reference style, a single cell is referred to by its column letter "
                "followed by its row number — for example B2. That is the same address you would "
                "use to describe one order's city in the Orders sheet."
            ),
            "lineage": {
                "concept_ids": [CR],
                "fact_ids": [qid(CR, "f2")],
                "teaching_block_ids": [qid(CR, "tb2")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{tile_id}.s05.b3",
            "role": "mechanism",
            "text": (
                "A reference can also point at a block of cells at once. A10:A20 refers to the "
                "range in column A, rows 10 through 20. A10:E20 refers to the range in columns A "
                "through E, rows 10 through 20. If delivery times sit in column C, rows 2 through 21, "
                "then C2:C21 covers every delivery time in that batch."
            ),
            "lineage": {
                "concept_ids": [CR],
                "fact_ids": [qid(CR, "f3")],
                "teaching_block_ids": [qid(CR, "tb3")]
            }
        },
        {
            "type": "spreadsheet_grid",
            "block_id": f"{tile_id}.s05.b4",
            "asset_ref": {"asset_id": "asset_orders_clean"},
            "range": "A1:E21",
            "selection": "A10:E20",
            "annotations": [
                {
                    "target": "A10:E20",
                    "text": "Rectangular range A10:E20 — rows 10 through 20, columns A through E"
                }
            ],
            "lineage": {
                "concept_ids": [CR],
                "fact_ids": [qid(CR, "f2"), qid(CR, "f3")],
                "teaching_block_ids": [qid(CR, "tb2"), qid(CR, "tb3")],
                "anchors": [qid(CR, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [CR],
        "fact_ids": [qid(CR, "f1"), qid(CR, "f2"), qid(CR, "f3")],
        "teaching_block_ids": [qid(CR, "tb1"), qid(CR, "tb2"), qid(CR, "tb3")],
        "anchors": [qid(CR, "visual")]
    }
}

# s06 – explainer, cell_references_ranges, tb4, f4, no visual
# word_budget: 75
s06 = {
    "step_id": f"{tile_id}.s06",
    "type": "explainer",
    "concept_ids": [CR],
    "eyebrow": "Cell References and Ranges",
    "title": "Referencing an entire row or column",
    "lede": "Use a repeated letter or number to select every cell in a column or row.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s06.b1",
            "role": "mechanism",
            "text": (
                "You can reference an entire row or column by repeating its letter or number on "
                "either side of a colon: 5:5 selects all cells in row 5, and H:H selects all cells "
                "in column H. If new orders keep being added to the Orders sheet and you want a "
                "reference that always covers the whole city column, B:B does that."
            ),
            "lineage": {
                "concept_ids": [CR],
                "fact_ids": [qid(CR, "f4")],
                "teaching_block_ids": [qid(CR, "tb4")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [CR],
        "fact_ids": [qid(CR, "f4")],
        "teaching_block_ids": [qid(CR, "tb4")]
    }
}

# s07 – check, cell_references_ranges, f4, framing only
s07 = {
    "step_id": f"{tile_id}.s07",
    "type": "check",
    "concept_ids": [CR],
    "eyebrow": "Quick Check",
    "title": "Whole-row and whole-column references",
    "lede": "Choose the correct reference notation for an entire row or column.",
    "reward": {"gems": 5, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": [CR],
        "fact_ids": [qid(CR, "f4")],
        "teaching_block_ids": [],
        "anchors": [qid(CR, "assessment:write_whole_row_or_whole_column_reference")]
    }
}

# s08 – hands_on, cell_references_ranges, f1+f2+f3+f4, framing only
s08 = {
    "step_id": f"{tile_id}.s08",
    "type": "hands_on",
    "concept_ids": [CR],
    "eyebrow": "Practice",
    "title": "Write range references for the Orders sheet",
    "lede": "Given a described data region, write the exact range reference that covers it.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [CR],
        "fact_ids": [qid(CR, "f1"), qid(CR, "f2"), qid(CR, "f3"), qid(CR, "f4")],
        "teaching_block_ids": [],
        "anchors": [
            qid(CR, "practice"),
            qid(CR, "assessment:write_correct_cell_or_range_reference_for_formula_requirement"),
            qid(CR, "assessment:identify_single_cell_by_column_letter_and_row_number"),
            qid(CR, "assessment:write_rectangular_range_reference_using_colon_notation"),
            qid(CR, "assessment:write_whole_row_or_whole_column_reference")
        ]
    }
}

# s09 – recap, both concepts, tb4 (grid_model) + tb5 (cell_references_ranges), all facts
# word_budget: 90
s09 = {
    "step_id": f"{tile_id}.s09",
    "type": "recap",
    "concept_ids": [GM, CR],
    "eyebrow": "Recap",
    "title": "The grid, addresses, and ranges",
    "lede": "Everything in a spreadsheet starts from the cell address and the range.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s09.b1",
            "role": "takeaway",
            "text": (
                "A cell is found by its column-letter/row-number address, and a workbook can hold "
                "several grids as separate sheets. A reference points at one cell or a block of cells; "
                "a range like A10:E20 covers a rectangular block, while H:H covers an entire column. "
                "Every formula you write from here will use one of these reference forms."
            ),
            "lineage": {
                "concept_ids": [GM, CR],
                "fact_ids": [
                    qid(GM, "f1"), qid(GM, "f2"), qid(GM, "f3"), qid(GM, "f4"),
                    qid(CR, "f1"), qid(CR, "f2"), qid(CR, "f3"), qid(CR, "f4")
                ],
                "teaching_block_ids": [qid(GM, "tb4"), qid(CR, "tb5")]
            }
        },
        {
            "type": "up_next",
            "block_id": f"{tile_id}.s09.b2",
            "title": "Up next: Structured Tables",
            "text": (
                "In the next tile you will convert the Orders range into an Excel table — "
                "giving each column a labelled header and letting formulas refer to columns by name."
            )
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [GM, CR],
        "fact_ids": [
            qid(GM, "f1"), qid(GM, "f2"), qid(GM, "f3"), qid(GM, "f4"),
            qid(CR, "f1"), qid(CR, "f2"), qid(CR, "f3"), qid(CR, "f4")
        ],
        "teaching_block_ids": [qid(GM, "tb4"), qid(CR, "tb5")]
    }
}

# ── REMEDIATION STEPS ────────────────────────────────────────────────────────
# Rule 7: first check/hands_on of each concept gets a remediation step.
# grid_model: s03 is the first check (measures f1+f2 = distinguish_cell_contents_and_address)
# s04 is the first hands_on (measures f1+f2+f3+f4 — multiple capabilities)
# Since s03 and s04 measure different fact sets, give each its own remediation.
# cell_references_ranges: s07 is the first check (measures f4)
# s08 is the first hands_on (measures f1+f2+f3+f4)

r01 = {
    "step_id": f"{tile_id}.r01",
    "type": "remediation",
    "concept_ids": [GM],
    "title": "Re-check: address vs. contents",
    "lede": "A cell's address and its contents are two different things — here is the contrast.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r01.b1",
            "role": "misconception",
            "text": (
                "The address B2 is the cell's location — column B, row 2. "
                "The contents of B2 is whatever you have typed or calculated there: "
                "a number, a city name, or a formula. Changing the contents does not change "
                "the address; B2 is always B2 regardless of what is inside it."
            ),
            "lineage": {
                "concept_ids": [GM],
                "fact_ids": [qid(GM, "f1"), qid(GM, "f2")],
                "teaching_block_ids": [qid(GM, "tb2")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [GM],
        "fact_ids": [qid(GM, "f1"), qid(GM, "f2")],
        "teaching_block_ids": [qid(GM, "tb2")]
    }
}

r02 = {
    "step_id": f"{tile_id}.r02",
    "type": "remediation",
    "concept_ids": [GM],
    "title": "Re-check: grid structure and sheet names",
    "lede": "Rows, columns, and sheet tabs — a quick contrast to clear up confusion.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r02.b1",
            "role": "misconception",
            "text": (
                "Columns run left to right and are labelled with letters (A, B, C…). "
                "Rows run top to bottom and are labelled with numbers (1, 2, 3…). "
                "A workbook can hold multiple sheets; by default they are named Sheet1, Sheet2 "
                "and so on, and each name appears on its tab at the bottom of the screen."
            ),
            "lineage": {
                "concept_ids": [GM],
                "fact_ids": [qid(GM, "f1"), qid(GM, "f2"), qid(GM, "f3"), qid(GM, "f4")],
                "teaching_block_ids": [qid(GM, "tb3")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [GM],
        "fact_ids": [qid(GM, "f1"), qid(GM, "f2"), qid(GM, "f3"), qid(GM, "f4")],
        "teaching_block_ids": [qid(GM, "tb3")]
    }
}

r03 = {
    "step_id": f"{tile_id}.r03",
    "type": "remediation",
    "concept_ids": [CR],
    "title": "Re-check: whole-row and whole-column notation",
    "lede": "The colon syntax for selecting an entire row or column — a clear contrast.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r03.b1",
            "role": "misconception",
            "text": (
                "To reference all cells in row 5, write 5:5 — the row number on both sides of the colon. "
                "To reference all cells in column H, write H:H — the column letter on both sides. "
                "This is different from a rectangular range like A10:E20, which uses different "
                "start and end addresses. H:H always expands as new rows are added."
            ),
            "lineage": {
                "concept_ids": [CR],
                "fact_ids": [qid(CR, "f4")],
                "teaching_block_ids": [qid(CR, "tb4")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [CR],
        "fact_ids": [qid(CR, "f4")],
        "teaching_block_ids": [qid(CR, "tb4")]
    }
}

r04 = {
    "step_id": f"{tile_id}.r04",
    "type": "remediation",
    "concept_ids": [CR],
    "title": "Re-check: single-cell and range references",
    "lede": "Single cells, rectangular blocks, and whole-column references — the three forms side by side.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r04.b1",
            "role": "mechanism",
            "text": (
                "A single-cell reference uses column letter then row number: B2. "
                "A rectangular range uses a start address, a colon, and an end address: A10:E20 "
                "covers columns A through E, rows 10 through 20. "
                "A whole-column reference repeats the letter: B:B covers every cell in column B. "
                "A formula picks the form that matches how many cells it needs."
            ),
            "lineage": {
                "concept_ids": [CR],
                "fact_ids": [qid(CR, "f1"), qid(CR, "f2"), qid(CR, "f3"), qid(CR, "f4")],
                "teaching_block_ids": [qid(CR, "tb1"), qid(CR, "tb2"), qid(CR, "tb3"), qid(CR, "tb4")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [CR],
        "fact_ids": [qid(CR, "f1"), qid(CR, "f2"), qid(CR, "f3"), qid(CR, "f4")],
        "teaching_block_ids": [qid(CR, "tb1"), qid(CR, "tb2"), qid(CR, "tb3"), qid(CR, "tb4")]
    }
}

# ── ASSEMBLE ─────────────────────────────────────────────────────────────────
output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "tiles": [
        {
            "tile_id": tile_id,
            "title": "The Spreadsheet Grid and Cell References",
            "summary": (
                "Introduces the spreadsheet grid model (cells, rows, columns, sheets) and "
                "A1 cell references and ranges, using the QuickDeliver orders workbook as context."
            ),
            "steps": [s01, s02, s03, s04, s05, s06, s07, s08, s09],
            "remediation_steps": [r01, r02, r03, r04]
        }
    ]
}

out_path = "batches/final_batch_011_da_spreadsheet/screens.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {out_path}")
print(f"Steps: {len(output['tiles'][0]['steps'])}")
print(f"Remediation steps: {len(output['tiles'][0]['remediation_steps'])}")
for s in output['tiles'][0]['steps']:
    print(f"  {s['step_id']} ({s['type']}): blocks={len(s.get('blocks', []))}")
