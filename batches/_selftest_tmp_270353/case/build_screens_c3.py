#!/usr/bin/env python3
"""Build screens.part.c3.json for chunk c3 tiles."""
import json, re, sys

BATCH = "batches/final_batch_011_da_spreadsheet"
OUT   = f"{BATCH}/screens.part.c3.json"

# ── helpers ──────────────────────────────────────────────────────────────────
def qid(concept_id, suffix):
    """Return qualified id like spreadsheet.foo#f1"""
    return f"{concept_id}#{suffix}"

def prose(block_id, role, text, concept_ids, tb_ids, fact_ids, anchors=None):
    b = {"type": "prose", "block_id": block_id, "role": role, "text": text,
         "lineage": {"concept_ids": concept_ids, "teaching_block_ids": tb_ids,
                     "fact_ids": fact_ids}}
    if anchors:
        b["lineage"]["anchors"] = anchors
    return b

def step_lineage(concept_ids, tb_ids, fact_ids, seg_ids=None, anchors=None):
    d = {"concept_ids": concept_ids, "teaching_block_ids": tb_ids, "fact_ids": fact_ids}
    if seg_ids:
        d["segment_ids"] = seg_ids
    if anchors:
        d["anchors"] = anchors
    return d

# ─────────────────────────────────────────────────────────────────────────────
# TILE 1: tile_spreadsheet_tables_named_ranges
# ─────────────────────────────────────────────────────────────────────────────
T1 = "tile_spreadsheet_tables_named_ranges"
C_ST = "spreadsheet.structured_tables"
C_NR = "spreadsheet.named_ranges"

tile_tables_named_ranges = {
    "tile_id": T1,
    "title": "Structured Tables and Named Ranges",
    "summary": "Convert a data range into an Excel table with structured references, and name ranges for readable formulas.",
    "steps": [
        # s01 – explainer, before_after visual
        {
            "step_id": f"{T1}.s01",
            "type": "explainer",
            "concept_ids": [C_ST],
            "eyebrow": "Concept",
            "title": "From Plain Range to Structured Table",
            "lede": "Converting your Orders range into a table gives every column a label and lets formulas refer to columns by name.",
            "blocks": [
                prose(f"{T1}.s01.p1", "intro",
                    "Your Orders sheet keeps growing as new deliveries come in. Converting its range into an Excel table gives each column a labeled header, lets formulas refer to columns by name, and lets the table expand automatically as you add data just below or beside it.",
                    [C_ST],
                    [qid(C_ST,"tb1")],
                    [qid(C_ST,"f1"), qid(C_ST,"f4")]),
                prose(f"{T1}.s01.p2", "definition",
                    "To create a table from a data range, select the cell or range, then choose Home > Format as Table and pick a table style. By default the resulting table has a header row that labels each column, though that header row can be turned off if it isn't wanted.",
                    [C_ST],
                    [qid(C_ST,"tb2")],
                    [qid(C_ST,"f1"), qid(C_ST,"f2")]),
                prose(f"{T1}.s01.p3", "mechanism",
                    "Once a range is a table, formulas can refer to its columns by name instead of by raw cell address — this is called a structured reference. Instead of =SUM(C2:C7), a formula can use =SUM(DeptSales[Sales Amount]), naming the table and the column directly. On an Orders table that same pattern looks like =SUM(Orders[Amount]).",
                    [C_ST],
                    [qid(C_ST,"tb3")],
                    [qid(C_ST,"f3")]),
                {
                    "type": "before_after",
                    "block_id": f"{T1}.s01.ba1",
                    "before": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None,
                                      "columns": ["order_id","city","delivery_minutes","amount","status"]},
                        "range": "A1:E5",
                        "sheet_name": "Orders",
                        "annotations": [
                            {"target": "A1:E1", "text": "Plain header row — no table style"}
                        ]
                    },
                    "after": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None,
                                      "columns": ["order_id","city","delivery_minutes","amount","status"]},
                        "range": "A1:E5",
                        "sheet_name": "Orders",
                        "annotations": [
                            {"target": "A1:E1", "text": "Table header row with column labels and filter arrows"},
                            {"target": "D2:D5", "text": "=SUM(Orders[amount]) references this column by name"}
                        ]
                    },
                    "change_summary": "Home > Format as Table converts the plain range into a structured table with labeled column headers and filter arrows on each column.",
                    "lineage": {
                        "concept_ids": [C_ST],
                        "teaching_block_ids": [qid(C_ST,"tb2"), qid(C_ST,"tb3")],
                        "fact_ids": [qid(C_ST,"f1"), qid(C_ST,"f2"), qid(C_ST,"f3")],
                        "anchors": [qid(C_ST,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_ST],
                [qid(C_ST,"tb1"), qid(C_ST,"tb2"), qid(C_ST,"tb3")],
                [qid(C_ST,"f1"), qid(C_ST,"f2"), qid(C_ST,"f3"), qid(C_ST,"f4")],
                anchors=[qid(C_ST,"visual")]
            )
        },
        # s02 – video
        {
            "step_id": f"{T1}.s02",
            "type": "video",
            "concept_ids": [C_ST],
            "eyebrow": "Watch",
            "title": "Auto-Expansion and Structured References in Action",
            "lede": "See how typing at the table edge expands it and how Excel replaces cell addresses with column names.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T1}.s02.mg1",
                    "segment_ids": ["seg_spreadsheet.structured_tables_VT479YDPB0I_1381_1573"]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_ST],
                [],
                [qid(C_ST,"f3"), qid(C_ST,"f4")],
                seg_ids=["seg_spreadsheet.structured_tables_VT479YDPB0I_1381_1573"]
            )
        },
        # s03 – explainer (tb4, f4)
        {
            "step_id": f"{T1}.s03",
            "type": "explainer",
            "concept_ids": [C_ST],
            "eyebrow": "Concept",
            "title": "Tables Grow With Your Data",
            "lede": "Typing just below or beside a table automatically extends it.",
            "blocks": [
                prose(f"{T1}.s03.p1", "example",
                    "The table also grows with your data on its own: typing a value in a cell just below the table's last row, or in a cell to the right of its last column, expands the table to include that new row or column. As tomorrow's deliveries are typed in just below your existing Orders table, the table expands to include those new rows.",
                    [C_ST],
                    [qid(C_ST,"tb4")],
                    [qid(C_ST,"f4")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_ST],
                [qid(C_ST,"tb4")],
                [qid(C_ST,"f4")]
            )
        },
        # s04 – check (framing only)
        {
            "step_id": f"{T1}.s04",
            "type": "check",
            "concept_ids": [C_ST],
            "eyebrow": "Quick Check",
            "title": "Table Auto-Expansion",
            "lede": "Test your understanding of how a table expands when new data is added.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_ST],
                [],
                [qid(C_ST,"f4")],
                anchors=[qid(C_ST,"assessment:verify_table_auto_expansion_on_new_data")]
            )
        },
        # s05 – hands_on (framing only)
        {
            "step_id": f"{T1}.s05",
            "type": "hands_on",
            "concept_ids": [C_ST],
            "eyebrow": "Practice",
            "title": "Create a Table and Write a Structured Reference",
            "lede": "Convert the Orders range into a table, then write a formula using a structured reference.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_ST],
                [],
                [qid(C_ST,"f1"), qid(C_ST,"f2"), qid(C_ST,"f3"), qid(C_ST,"f4")],
                anchors=[
                    qid(C_ST,"practice"),
                    qid(C_ST,"assessment:create_table_from_range_and_manage_header"),
                    qid(C_ST,"assessment:write_formula_using_structured_reference"),
                    qid(C_ST,"assessment:verify_table_auto_expansion_on_new_data")
                ]
            )
        },
        # s06 – explainer, annotated_image visual
        {
            "step_id": f"{T1}.s06",
            "type": "explainer",
            "concept_ids": [C_NR],
            "eyebrow": "Concept",
            "title": "Naming a Range for Readable Formulas",
            "lede": "A named range lets a formula use a label like DeliveryTimes instead of a raw address like C2:C51.",
            "blocks": [
                prose(f"{T1}.s06.p1", "definition",
                    "A named range lets a formula use a readable label instead of a raw cell address. To name a cell or range, select it, type a name into the Name Box, and press Enter — for example, selecting C2:C51 (the delivery-time column) and naming it DeliveryTimes.",
                    [C_NR],
                    [qid(C_NR,"tb1")],
                    [qid(C_NR,"f1")]),
                prose(f"{T1}.s06.p2", "example",
                    "Once a name is defined, typing the name into a formula — or selecting Formulas > Use in Formula and choosing the name — lets that formula reference the named range instead of its raw address. A formula can refer to DeliveryTimes instead of C2:C51.",
                    [C_NR],
                    [qid(C_NR,"tb2")],
                    [qid(C_NR,"f2")]),
                {
                    "type": "annotated_image",
                    "block_id": f"{T1}.s06.ai1",
                    "asset_id": "img_named_range_name_box",
                    "alt_text": "Spreadsheet screenshot showing the Name Box containing 'DeliveryTimes' while the range C2:C51 is selected, and the formula bar showing =AVERAGE(DeliveryTimes) in place of the raw cell address.",
                    "hotspots": [
                        {"x": 0.05, "y": 0.04, "w": 0.18, "h": 0.06,
                         "label": "Name Box",
                         "detail": "Type a name here and press Enter to define a named range for the selected cells."},
                        {"x": 0.25, "y": 0.04, "w": 0.40, "h": 0.06,
                         "label": "Formula bar",
                         "detail": "The formula uses DeliveryTimes instead of C2:C51 — same result, more readable."},
                        {"x": 0.05, "y": 0.12, "w": 0.08, "h": 0.70,
                         "label": "Selected range C2:C51",
                         "detail": "This is the delivery-time column that has been named DeliveryTimes."}
                    ],
                    "lineage": {
                        "concept_ids": [C_NR],
                        "teaching_block_ids": [qid(C_NR,"tb1"), qid(C_NR,"tb2")],
                        "fact_ids": [qid(C_NR,"f1"), qid(C_NR,"f2")],
                        "anchors": [qid(C_NR,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_NR],
                [qid(C_NR,"tb1"), qid(C_NR,"tb2")],
                [qid(C_NR,"f1"), qid(C_NR,"f2")],
                anchors=[qid(C_NR,"visual")]
            )
        },
        # s07 – check (framing only)
        {
            "step_id": f"{T1}.s07",
            "type": "check",
            "concept_ids": [C_NR],
            "eyebrow": "Quick Check",
            "title": "Replacing a Cell Reference with a Named Range",
            "lede": "Test your understanding of how to define and use a named range in a formula.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_NR],
                [],
                [qid(C_NR,"f1"), qid(C_NR,"f2")],
                anchors=[qid(C_NR,"assessment:replace_cell_reference_with_named_range_in_formula")]
            )
        },
        # s08 – hands_on (framing only)
        {
            "step_id": f"{T1}.s08",
            "type": "hands_on",
            "concept_ids": [C_NR],
            "eyebrow": "Practice",
            "title": "Define a Named Range and Use It in a Formula",
            "lede": "Name a range using the Name Box, then replace a raw cell address in a formula with that name.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_NR],
                [],
                [qid(C_NR,"f1"), qid(C_NR,"f2")],
                anchors=[
                    qid(C_NR,"practice"),
                    qid(C_NR,"assessment:replace_cell_reference_with_named_range_in_formula")
                ]
            )
        },
        # s09 – recap
        {
            "step_id": f"{T1}.s09",
            "type": "recap",
            "concept_ids": [C_ST, C_NR],
            "eyebrow": "Recap",
            "title": "Structured Tables and Named Ranges — Key Points",
            "lede": "You can now convert a range into a table, write structured references, and name ranges for readable formulas.",
            "blocks": [
                prose(f"{T1}.s09.p1", "takeaway",
                    "Select a range and choose Home > Format as Table to create a structured table with a labeled header row. Formulas can then reference columns by name — =SUM(Orders[amount]) instead of =SUM(D2:D51) — which is called a structured reference. The table also expands automatically when you type a value just below its last row or to the right of its last column. For any range, type a name in the Name Box and press Enter to define a named range; formulas can then use that name instead of the raw address.",
                    [C_ST, C_NR],
                    [qid(C_ST,"tb2"), qid(C_ST,"tb3"), qid(C_ST,"tb4"), qid(C_NR,"tb1"), qid(C_NR,"tb2")],
                    [qid(C_ST,"f1"), qid(C_ST,"f2"), qid(C_ST,"f3"), qid(C_ST,"f4"),
                     qid(C_NR,"f1"), qid(C_NR,"f2")]),
                {
                    "type": "up_next",
                    "block_id": f"{T1}.s09.up_next",
                    "title": "Next: Sorting and Filtering",
                    "text": "In the next tile you'll sort and filter your Orders table to surface the rows that matter most — fast deliveries, specific cities, or pending orders."
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_ST, C_NR],
                [qid(C_ST,"tb2"), qid(C_ST,"tb3"), qid(C_ST,"tb4"), qid(C_NR,"tb1"), qid(C_NR,"tb2")],
                [qid(C_ST,"f1"), qid(C_ST,"f2"), qid(C_ST,"f3"), qid(C_ST,"f4"),
                 qid(C_NR,"f1"), qid(C_NR,"f2")]
            )
        }
    ],
    "remediation_steps": [
        # r01 – for s04 check (verify_table_auto_expansion_on_new_data → f4)
        {
            "step_id": f"{T1}.r01",
            "type": "remediation",
            "concept_ids": [C_ST],
            "eyebrow": "Let's Revisit",
            "title": "How a Table Expands Automatically",
            "lede": "A clear example shows exactly what triggers table expansion and what doesn't.",
            "blocks": [
                prose(f"{T1}.r01.p1", "example",
                    "Typing a value in a cell just below the table's last row, or in a cell to the right of its last column, expands the table to include that new row or column. On the Orders table, if the last data row is row 21, typing a new order_id in A22 causes the table border and style to extend to row 22 automatically. Typing in a cell that is not adjacent to the table does not expand it.",
                    [C_ST],
                    [qid(C_ST,"tb4")],
                    [qid(C_ST,"f4")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_ST],
                [qid(C_ST,"tb4")],
                [qid(C_ST,"f4")]
            )
        },
        # r02 – for s07 check (replace_cell_reference_with_named_range_in_formula → f1, f2)
        {
            "step_id": f"{T1}.r02",
            "type": "remediation",
            "concept_ids": [C_NR],
            "eyebrow": "Let's Revisit",
            "title": "Defining and Using a Named Range",
            "lede": "Two steps: name the range in the Name Box, then use that name in a formula.",
            "blocks": [
                prose(f"{T1}.r02.p1", "example",
                    "To name a range, select it — for example C2:C51 — then click the Name Box at the top-left of the spreadsheet, type DeliveryTimes, and press Enter. The name is now defined. In any formula, type DeliveryTimes where you would have typed C2:C51: =AVERAGE(DeliveryTimes) gives the same result as =AVERAGE(C2:C51) but is easier to read and maintain.",
                    [C_NR],
                    [qid(C_NR,"tb1"), qid(C_NR,"tb2")],
                    [qid(C_NR,"f1"), qid(C_NR,"f2")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_NR],
                [qid(C_NR,"tb1"), qid(C_NR,"tb2")],
                [qid(C_NR,"f1"), qid(C_NR,"f2")]
            )
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# TILE 2: tile_spreadsheet_pivot_tables
# ─────────────────────────────────────────────────────────────────────────────
T2 = "tile_spreadsheet_pivot_tables"
C_PT = "spreadsheet.pivot_tables"
C_PS = "spreadsheet.pivot_summarization"

tile_pivot_tables = {
    "tile_id": T2,
    "title": "Pivot Tables",
    "summary": "Build a PivotTable to summarise Orders data by city and status, then change the value-field summary function.",
    "steps": [
        # s01 – explainer, annotated_image visual
        {
            "step_id": f"{T2}.s01",
            "type": "explainer",
            "concept_ids": [C_PT],
            "eyebrow": "Concept",
            "title": "What a PivotTable Does and How to Build One",
            "lede": "A PivotTable summarises your Orders data by city, status, or any other field — no formulas required.",
            "blocks": [
                prose(f"{T2}.s01.p1", "intro",
                    "Reading down a long Orders sheet to compare total amounts by city and status by hand would take forever. A PivotTable is a tool to calculate, summarize, and analyze data that lets you see comparisons, patterns, and trends in your data.",
                    [C_PT],
                    [qid(C_PT,"tb1"), qid(C_PT,"tb2")],
                    [qid(C_PT,"f1")]),
                prose(f"{T2}.s01.p2", "mechanism",
                    "To create a PivotTable, select the data cells, select Insert > PivotTable, choose where to place the PivotTable report, and select OK. To add a field, select its checkbox in the PivotTable Fields pane; non-numeric fields go to Rows and numeric fields go to Values by default. A field can be moved to a different area by dragging it there.",
                    [C_PT],
                    [qid(C_PT,"tb3")],
                    [qid(C_PT,"f2"), qid(C_PT,"f3")]),
                prose(f"{T2}.s01.p3", "example",
                    "Filters area fields appear as top-level report filters above the PivotTable. Columns area fields appear as Column Labels at the top. Rows area fields appear as Row Labels on the left. Values area fields appear as summarised numeric values in the body. Building a PivotTable from your Orders data with City in Rows, Status in Columns, and Amount in Values gives a grid of summarised order amounts for every city/status combination.",
                    [C_PT],
                    [qid(C_PT,"tb4")],
                    [qid(C_PT,"f4")]),
                {
                    "type": "annotated_image",
                    "block_id": f"{T2}.s01.ai1",
                    "asset_id": "img_pivot_fields_pane",
                    "alt_text": "Screenshot of the PivotTable Fields pane showing four drop zones: Filters (top), Columns (top-right), Rows (bottom-left), and Values (bottom-right), with City in Rows, Status in Columns, and Amount in Values.",
                    "hotspots": [
                        {"x": 0.05, "y": 0.05, "w": 0.90, "h": 0.12,
                         "label": "Filters area",
                         "detail": "Fields here appear as top-level report filters above the PivotTable."},
                        {"x": 0.50, "y": 0.55, "w": 0.45, "h": 0.20,
                         "label": "Columns area",
                         "detail": "Fields here appear as Column Labels at the top of the PivotTable. Status is placed here."},
                        {"x": 0.05, "y": 0.55, "w": 0.40, "h": 0.20,
                         "label": "Rows area",
                         "detail": "Fields here appear as Row Labels on the left side. City is placed here."},
                        {"x": 0.50, "y": 0.78, "w": 0.45, "h": 0.18,
                         "label": "Values area",
                         "detail": "Fields here appear as summarised numeric values in the body. Amount is placed here."}
                    ],
                    "lineage": {
                        "concept_ids": [C_PT],
                        "teaching_block_ids": [qid(C_PT,"tb3"), qid(C_PT,"tb4")],
                        "fact_ids": [qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")],
                        "anchors": [qid(C_PT,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PT],
                [qid(C_PT,"tb1"), qid(C_PT,"tb2"), qid(C_PT,"tb3"), qid(C_PT,"tb4")],
                [qid(C_PT,"f1"), qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")],
                anchors=[qid(C_PT,"visual")]
            )
        },
        # s02 – video
        {
            "step_id": f"{T2}.s02",
            "type": "video",
            "concept_ids": [C_PT],
            "eyebrow": "Watch",
            "title": "Building a PivotTable: Fields, Areas, and Layout",
            "lede": "Watch how each field snaps into its area and the summary grid rearranges instantly.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T2}.s02.mg1",
                    "segment_ids": ["seg_spreadsheet.pivot_tables_aofsdpjvK7w_84_302"]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PT],
                [],
                [qid(C_PT,"f1"), qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")],
                seg_ids=["seg_spreadsheet.pivot_tables_aofsdpjvK7w_84_302"]
            )
        },
        # s03 – explainer (tb4, f4)
        {
            "step_id": f"{T2}.s03",
            "type": "explainer",
            "concept_ids": [C_PT],
            "eyebrow": "Concept",
            "title": "What Each PivotTable Area Displays",
            "lede": "Each of the four drop zones produces a distinct visual output in the PivotTable.",
            "blocks": [
                prose(f"{T2}.s03.p1", "definition",
                    "Filters area fields are shown as top-level report filters above the PivotTable. Columns area fields are shown as Column Labels at the top of the PivotTable. Rows area fields are shown as Row Labels on the left side of the PivotTable. Values area fields are shown as summarised numeric values in the body of the PivotTable.",
                    [C_PT],
                    [qid(C_PT,"tb4")],
                    [qid(C_PT,"f4")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PT],
                [qid(C_PT,"tb4")],
                [qid(C_PT,"f4")]
            )
        },
        # s04 – check (framing only)
        {
            "step_id": f"{T2}.s04",
            "type": "check",
            "concept_ids": [C_PT],
            "eyebrow": "Quick Check",
            "title": "Creating a PivotTable and Reading Its Areas",
            "lede": "Test your understanding of the creation steps and what each area displays.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PT],
                [],
                [qid(C_PT,"f2"), qid(C_PT,"f4")],
                anchors=[
                    qid(C_PT,"assessment:execute_pivot_table_creation_steps"),
                    qid(C_PT,"assessment:identify_visual_output_of_each_pivot_area")
                ]
            )
        },
        # s05 – check (framing only)
        {
            "step_id": f"{T2}.s05",
            "type": "check",
            "concept_ids": [C_PT],
            "eyebrow": "Quick Check",
            "title": "Building a PivotTable to Answer a Question",
            "lede": "Apply your knowledge of fields, areas, and creation steps to a summarisation task.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PT],
                [],
                [qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")],
                anchors=[qid(C_PT,"assessment:build_pivot_table_to_answer_summarization_requirement")]
            )
        },
        # s06 – hands_on (framing only)
        {
            "step_id": f"{T2}.s06",
            "type": "hands_on",
            "concept_ids": [C_PT],
            "eyebrow": "Practice",
            "title": "Build a PivotTable from the Orders Data",
            "lede": "Create a PivotTable and place fields in the Rows, Columns, and Values areas.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_PT],
                [],
                [qid(C_PT,"f1"), qid(C_PT,"f3")],
                anchors=[
                    qid(C_PT,"practice"),
                    qid(C_PT,"assessment:define_pivot_table_purpose"),
                    qid(C_PT,"assessment:add_and_reposition_fields_in_pivot_areas")
                ]
            )
        },
        # s07 – explainer, before_after visual
        {
            "step_id": f"{T2}.s07",
            "type": "explainer",
            "concept_ids": [C_PS],
            "eyebrow": "Concept",
            "title": "Changing How Values Are Summarised",
            "lede": "The Values area defaults to Sum for numbers and Count for text — and you can change it.",
            "blocks": [
                prose(f"{T2}.s07.p1", "definition",
                    "Data in a PivotTable's Values area summarises the underlying source data by default using the SUM function for numeric values and the COUNT function for text values. Placing Amount in Values on your Orders PivotTable defaults to a total of every matching order's amount, not an average.",
                    [C_PS],
                    [qid(C_PS,"tb1")],
                    [qid(C_PS,"f1")]),
                prose(f"{T2}.s07.p2", "mechanism",
                    "To change a value field's summary function, select the field in the Values area, then on the PivotTable Analyze tab select Active Field > Field Settings (or right-click the value and choose Value Field Settings), select the Summarize Values By tab, and choose the function you want, such as Average. Switching Amount from Sum to Average turns the same PivotTable from showing total revenue per city into showing average order value per city.",
                    [C_PS],
                    [qid(C_PS,"tb2")],
                    [qid(C_PS,"f2")]),
                {
                    "type": "before_after",
                    "block_id": f"{T2}.s07.ba1",
                    "before": {
                        "type": "data_table",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None,
                                      "columns": ["city", "amount"]},
                        "caption": "PivotTable: Sum of Amount by City",
                        "tag_columns": [
                            {"column": "amount", "tag": "Sum of Amount", "tone": "focus"}
                        ]
                    },
                    "after": {
                        "type": "data_table",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None,
                                      "columns": ["city", "amount"]},
                        "caption": "PivotTable: Average of Amount by City",
                        "tag_columns": [
                            {"column": "amount", "tag": "Average of Amount", "tone": "focus"}
                        ]
                    },
                    "change_summary": "Value Field Settings > Summarize Values By > Average changes the Values area from Sum to Average — the same row/column layout, different numbers.",
                    "lineage": {
                        "concept_ids": [C_PS],
                        "teaching_block_ids": [qid(C_PS,"tb1"), qid(C_PS,"tb2")],
                        "fact_ids": [qid(C_PS,"f1"), qid(C_PS,"f2")],
                        "anchors": [qid(C_PS,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PS],
                [qid(C_PS,"tb1"), qid(C_PS,"tb2")],
                [qid(C_PS,"f1"), qid(C_PS,"f2")],
                anchors=[qid(C_PS,"visual")]
            )
        },
        # s08 – video
        {
            "step_id": f"{T2}.s08",
            "type": "video",
            "concept_ids": [C_PS],
            "eyebrow": "Watch",
            "title": "Changing a PivotTable's Value-Field Summary Function",
            "lede": "See how to open Value Field Settings and switch between Sum and Average.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T2}.s08.mg1",
                    "segment_ids": [
                        "seg_spreadsheet.pivot_summarization_UsdedFoTA68_239_280",
                        "seg_spreadsheet.pivot_summarization_RpCZ_kb1Gfs_0_132"
                    ]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PS],
                [],
                [qid(C_PS,"f1"), qid(C_PS,"f2")],
                seg_ids=[
                    "seg_spreadsheet.pivot_summarization_UsdedFoTA68_239_280",
                    "seg_spreadsheet.pivot_summarization_RpCZ_kb1Gfs_0_132"
                ]
            )
        },
        # s09 – check (framing only)
        {
            "step_id": f"{T2}.s09",
            "type": "check",
            "concept_ids": [C_PS],
            "eyebrow": "Quick Check",
            "title": "Default Summarisation by Data Type",
            "lede": "Test your understanding of when a PivotTable defaults to Sum versus Count.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PS],
                [],
                [qid(C_PS,"f1")],
                anchors=[qid(C_PS,"assessment:identify_default_summarization_by_data_type")]
            )
        },
        # s10 – hands_on (framing only)
        {
            "step_id": f"{T2}.s10",
            "type": "hands_on",
            "concept_ids": [C_PS],
            "eyebrow": "Practice",
            "title": "Switch the Summary Function to Average",
            "lede": "Change the Values area from Sum to Average using Value Field Settings.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_PS],
                [],
                [qid(C_PS,"f2")],
                anchors=[
                    qid(C_PS,"practice"),
                    qid(C_PS,"assessment:select_correct_value_field_summarization_setting")
                ]
            )
        },
        # s11 – recap
        {
            "step_id": f"{T2}.s11",
            "type": "recap",
            "concept_ids": [C_PT, C_PS],
            "eyebrow": "Recap",
            "title": "Pivot Tables — Key Points",
            "lede": "You can now build a PivotTable, place fields in the four areas, and change the summary function.",
            "blocks": [
                prose(f"{T2}.s11.p1", "takeaway",
                    "A PivotTable lets you calculate, summarise, and analyse data to see comparisons, patterns, and trends. Select the data, choose Insert > PivotTable, and drag fields into Rows, Columns, Values, or Filters. Non-numeric fields default to Rows; numeric fields default to Values. The Values area defaults to Sum for numbers and Count for text. To change the summary function, open Value Field Settings and choose from the Summarize Values By tab.",
                    [C_PT, C_PS],
                    [qid(C_PT,"tb2"), qid(C_PT,"tb3"), qid(C_PT,"tb4"),
                     qid(C_PS,"tb1"), qid(C_PS,"tb2")],
                    [qid(C_PT,"f1"), qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4"),
                     qid(C_PS,"f1"), qid(C_PS,"f2")]),
                {
                    "type": "up_next",
                    "block_id": f"{T2}.s11.up_next",
                    "title": "Next: Chart Types",
                    "text": "In the next tile you'll build bar, line, and pie charts from your Orders data to visualise comparisons, trends, and part-of-whole relationships."
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PT, C_PS],
                [qid(C_PT,"tb2"), qid(C_PT,"tb3"), qid(C_PT,"tb4"),
                 qid(C_PS,"tb1"), qid(C_PS,"tb2")],
                [qid(C_PT,"f1"), qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4"),
                 qid(C_PS,"f1"), qid(C_PS,"f2")]
            )
        }
    ],
    "remediation_steps": [
        # r01 – for s04 check (execute_pivot_table_creation_steps → f2; identify_visual_output → f4)
        {
            "step_id": f"{T2}.r01",
            "type": "remediation",
            "concept_ids": [C_PT],
            "eyebrow": "Let's Revisit",
            "title": "Creating a PivotTable Step by Step",
            "lede": "Walk through the creation steps and see what each area produces.",
            "blocks": [
                prose(f"{T2}.r01.p1", "example",
                    "To create a PivotTable: select the data cells, choose Insert > PivotTable, pick where to place the report, and click OK. In the Fields pane, check City — it goes to Rows because it is text. Check Amount — it goes to Values because it is numeric. Drag Status to Columns. The result: Row Labels show cities on the left, Column Labels show statuses at the top, and the body shows summarised amounts. Filters area fields would appear above the table as top-level report filters.",
                    [C_PT],
                    [qid(C_PT,"tb3"), qid(C_PT,"tb4")],
                    [qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PT],
                [qid(C_PT,"tb3"), qid(C_PT,"tb4")],
                [qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")]
            )
        },
        # r02 – for s05 check (build_pivot_table_to_answer_summarization_requirement → f2, f3, f4)
        {
            "step_id": f"{T2}.r02",
            "type": "remediation",
            "concept_ids": [C_PT],
            "eyebrow": "Let's Revisit",
            "title": "Choosing Fields and Areas for a Summarisation Task",
            "lede": "Match the question you want to answer to the correct field placement.",
            "blocks": [
                prose(f"{T2}.r02.p1", "example",
                    "To answer 'What is the total order amount per city?' place City in Rows and Amount in Values — the PivotTable sums Amount for each city. To add a breakdown by status, drag Status to Columns. To filter to a single city, drag City to Filters instead of Rows. Non-numeric fields added to the Fields pane go to Rows by default; numeric fields go to Values. You can always drag a field from one area to another.",
                    [C_PT],
                    [qid(C_PT,"tb3"), qid(C_PT,"tb4")],
                    [qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PT],
                [qid(C_PT,"tb3"), qid(C_PT,"tb4")],
                [qid(C_PT,"f2"), qid(C_PT,"f3"), qid(C_PT,"f4")]
            )
        },
        # r03 – for s09 check (identify_default_summarization_by_data_type → f1)
        {
            "step_id": f"{T2}.r03",
            "type": "remediation",
            "concept_ids": [C_PS],
            "eyebrow": "Let's Revisit",
            "title": "Sum vs. Count: The Default Rule",
            "lede": "The data type of the field determines which summary function the PivotTable uses by default.",
            "blocks": [
                prose(f"{T2}.r03.p1", "example",
                    "When you drag a numeric field such as Amount into the Values area, the PivotTable defaults to Sum — it adds up all matching values. When you drag a text field such as Status into Values, the PivotTable defaults to Count — it counts how many rows match. A numeric column that contains blank cells is treated as mixed and also defaults to Count. You can always change the function via Value Field Settings.",
                    [C_PS],
                    [qid(C_PS,"tb1")],
                    [qid(C_PS,"f1")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PS],
                [qid(C_PS,"tb1")],
                [qid(C_PS,"f1")]
            )
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# TILE 3: tile_spreadsheet_chart_types
# ─────────────────────────────────────────────────────────────────────────────
T3 = "tile_spreadsheet_chart_types"
C_BC = "spreadsheet.bar_chart_creation"
C_LC = "spreadsheet.line_chart_creation"
C_PC = "spreadsheet.pie_chart_creation"

tile_chart_types = {
    "tile_id": T3,
    "title": "Chart Types",
    "summary": "Build bar, line, and pie charts from Orders data to visualise comparisons, trends, and part-of-whole shares.",
    "steps": [
        # s01 – explainer, data_table visual
        {
            "step_id": f"{T3}.s01",
            "type": "explainer",
            "concept_ids": [C_BC],
            "eyebrow": "Concept",
            "title": "Bar Charts: Comparing Categories",
            "lede": "A bar chart places categories on one axis and values on the other to show comparisons at a glance.",
            "blocks": [
                prose(f"{T3}.s01.p1", "definition",
                    "Bar charts illustrate comparisons among individual items; in a bar chart, the categories are typically organised along one axis and the values along the other. A summary table of total order amount by city is exactly the kind of category-versus-value data a bar chart compares.",
                    [C_BC],
                    [qid(C_BC,"tb1")],
                    [qid(C_BC,"f1")]),
                prose(f"{T3}.s01.p2", "mechanism",
                    "To create a chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a bar chart you like, select the All Charts tab to see all chart types, select the chart, and click OK.",
                    [C_BC],
                    [qid(C_BC,"tb2")],
                    [qid(C_BC,"f2")]),
                {
                    "type": "data_table",
                    "block_id": f"{T3}.s01.dt1",
                    "asset_ref": {
                        "asset_id": "asset_city_totals",
                        "variant_id": None,
                        "columns": ["city", "total_amount"]
                    },
                    "caption": "City order totals — source data for a bar chart. Each city is a category; total_amount is the value.",
                    "tag_columns": [
                        {"column": "city", "tag": "Category axis", "tone": "focus"},
                        {"column": "total_amount", "tag": "Bar height (NGN)", "tone": "focus"}
                    ],
                    "lineage": {
                        "concept_ids": [C_BC],
                        "teaching_block_ids": [qid(C_BC,"tb1")],
                        "fact_ids": [qid(C_BC,"f1")],
                        "anchors": [qid(C_BC,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_BC],
                [qid(C_BC,"tb1"), qid(C_BC,"tb2")],
                [qid(C_BC,"f1"), qid(C_BC,"f2")],
                anchors=[qid(C_BC,"visual")]
            )
        },
        # s02 – video
        {
            "step_id": f"{T3}.s02",
            "type": "video",
            "concept_ids": [C_BC],
            "eyebrow": "Watch",
            "title": "Building a Bar Chart in Excel",
            "lede": "See how to select data and insert a bar chart from the Charts group.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T3}.s02.mg1",
                    "segment_ids": [
                        "seg_spreadsheet.bar_chart_creation_gMAHXrty6wI_136_359",
                        "seg_spreadsheet.bar_chart_creation_RY526I9h2SE_0_58"
                    ]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_BC],
                [],
                [qid(C_BC,"f1"), qid(C_BC,"f2")],
                seg_ids=[
                    "seg_spreadsheet.bar_chart_creation_gMAHXrty6wI_136_359",
                    "seg_spreadsheet.bar_chart_creation_RY526I9h2SE_0_58"
                ]
            )
        },
        # s03 – check (framing only)
        {
            "step_id": f"{T3}.s03",
            "type": "check",
            "concept_ids": [C_BC],
            "eyebrow": "Quick Check",
            "title": "Building a Bar Chart from Category Data",
            "lede": "Test your understanding of bar chart axis encoding and the Insert > Recommended Charts workflow.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_BC],
                [],
                [qid(C_BC,"f1"), qid(C_BC,"f2")],
                anchors=[qid(C_BC,"assessment:build_correctly_encoded_bar_chart_from_categorical_summary_data")]
            )
        },
        # s04 – hands_on (framing only)
        {
            "step_id": f"{T3}.s04",
            "type": "hands_on",
            "concept_ids": [C_BC],
            "eyebrow": "Practice",
            "title": "Build a Bar Chart from City Totals",
            "lede": "Select the city totals table and insert a bar chart using Insert > Recommended Charts.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_BC],
                [],
                [qid(C_BC,"f1"), qid(C_BC,"f2")],
                anchors=[
                    qid(C_BC,"practice"),
                    qid(C_BC,"assessment:identify_bar_chart_axis_encoding"),
                    qid(C_BC,"assessment:create_bar_chart_via_insert_recommended_charts")
                ]
            )
        },
        # s05 – explainer, data_table visual
        {
            "step_id": f"{T3}.s05",
            "type": "explainer",
            "concept_ids": [C_LC],
            "eyebrow": "Concept",
            "title": "Line Charts: Showing Trends Over Time",
            "lede": "A line chart distributes evenly-spaced time intervals along the horizontal axis and values along the vertical axis.",
            "blocks": [
                prose(f"{T3}.s05.p1", "definition",
                    "In a line chart, category data is distributed evenly along the horizontal axis and value data along the vertical axis. Line charts can show continuous data over time on an evenly scaled axis, making them well suited to showing trends at equal intervals such as months, quarters, or fiscal years. A summary of total order amount by month is exactly this kind of evenly-spaced, time-ordered data.",
                    [C_LC],
                    [qid(C_LC,"tb1")],
                    [qid(C_LC,"f1")]),
                prose(f"{T3}.s05.p2", "mechanism",
                    "To create a line chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a line chart you like, select the All Charts tab to see all chart types, select the chart, and click OK.",
                    [C_LC],
                    [qid(C_LC,"tb2")],
                    [qid(C_LC,"f2")]),
                {
                    "type": "data_table",
                    "block_id": f"{T3}.s05.dt1",
                    "asset_ref": {
                        "asset_id": "asset_monthly_summary",
                        "variant_id": None,
                        "columns": ["month_label", "total_amount"]
                    },
                    "caption": "Monthly order totals — source data for a line chart. Each month is evenly spaced on the horizontal axis; total_amount maps to the vertical axis.",
                    "tag_columns": [
                        {"column": "month_label", "tag": "Horizontal axis (equal intervals)", "tone": "focus"},
                        {"column": "total_amount", "tag": "Vertical axis (NGN)", "tone": "focus"}
                    ],
                    "lineage": {
                        "concept_ids": [C_LC],
                        "teaching_block_ids": [qid(C_LC,"tb1")],
                        "fact_ids": [qid(C_LC,"f1")],
                        "anchors": [qid(C_LC,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_LC],
                [qid(C_LC,"tb1"), qid(C_LC,"tb2")],
                [qid(C_LC,"f1"), qid(C_LC,"f2")],
                anchors=[qid(C_LC,"visual")]
            )
        },
        # s06 – video
        {
            "step_id": f"{T3}.s06",
            "type": "video",
            "concept_ids": [C_LC],
            "eyebrow": "Watch",
            "title": "Building a Line Chart from Monthly Sales Data",
            "lede": "See how to assign the data range and set the horizontal-axis labels.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T3}.s06.mg1",
                    "segment_ids": ["seg_spreadsheet.line_chart_creation_FnvE1SF1Wx0_82_360"]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_LC],
                [],
                [qid(C_LC,"f1"), qid(C_LC,"f2")],
                seg_ids=["seg_spreadsheet.line_chart_creation_FnvE1SF1Wx0_82_360"]
            )
        },
        # s07 – check (framing only)
        {
            "step_id": f"{T3}.s07",
            "type": "check",
            "concept_ids": [C_LC],
            "eyebrow": "Quick Check",
            "title": "Axis Roles and Interval Suitability",
            "lede": "Test your understanding of which axis carries time intervals and when a line chart is appropriate.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_LC],
                [],
                [qid(C_LC,"f1")],
                anchors=[qid(C_LC,"assessment:identify_axis_roles_and_interval_suitability")]
            )
        },
        # s08 – check (framing only)
        {
            "step_id": f"{T3}.s08",
            "type": "check",
            "concept_ids": [C_LC],
            "eyebrow": "Quick Check",
            "title": "Building a Line Chart from Time-Ordered Data",
            "lede": "Apply your knowledge of axis encoding and the Recommended Charts workflow.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_LC],
                [],
                [qid(C_LC,"f1"), qid(C_LC,"f2")],
                anchors=[qid(C_LC,"assessment:build_correctly_encoded_line_chart_from_time_ordered_data")]
            )
        },
        # s09 – hands_on (framing only)
        {
            "step_id": f"{T3}.s09",
            "type": "hands_on",
            "concept_ids": [C_LC],
            "eyebrow": "Practice",
            "title": "Build a Line Chart from Monthly Totals",
            "lede": "Select the monthly summary table and insert a line chart using Insert > Recommended Charts.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_LC],
                [],
                [qid(C_LC,"f2")],
                anchors=[
                    qid(C_LC,"practice"),
                    qid(C_LC,"assessment:create_line_chart_via_insert_recommended_charts")
                ]
            )
        },
        # s10 – explainer, chart visual
        {
            "step_id": f"{T3}.s10",
            "type": "explainer",
            "concept_ids": [C_PC],
            "eyebrow": "Concept",
            "title": "Pie Charts: Part-of-Whole Shares",
            "lede": "A pie chart shows each category's share of a total — but only when the data meets four conditions.",
            "blocks": [
                prose(f"{T3}.s10.p1", "definition",
                    "Pie charts show the size of items in one data series proportional to the sum of the items. They are appropriate when you have only one data series to plot, none of the values are negative, there are no more than seven categories, and the categories represent parts of the whole pie. A summary of total order amount by city, for no more than seven cities, fits that description as long as no amount is negative.",
                    [C_PC],
                    [qid(C_PC,"tb1")],
                    [qid(C_PC,"f1")]),
                prose(f"{T3}.s10.p2", "mechanism",
                    "To create a pie chart, select the data, choose Insert > Recommended Charts, and select a chart on the Recommended Charts tab to preview it. If you don't see a pie chart you like, select the All Charts tab to see all chart types, select the chart, and click OK.",
                    [C_PC],
                    [qid(C_PC,"tb2")],
                    [qid(C_PC,"f2")]),
                {
                    "type": "chart",
                    "block_id": f"{T3}.s10.ch1",
                    "chart_kind": "pie",
                    "asset_ref": {
                        "asset_id": "asset_city_totals",
                        "variant_id": None,
                        "columns": ["city", "total_amount"]
                    },
                    "title": "Total Order Amount by City (NGN)",
                    "alt_text": "Pie chart showing six slices, one per city. Lagos is the largest slice, followed by Abuja, Port Harcourt, Kano, Ibadan, and Enugu. Each slice is labelled with the city name and its share of total order amount.",
                    "encoding": {
                        "x": {"field": "city", "type": "nominal", "title": "City"},
                        "y": {"field": "total_amount", "type": "quantitative", "title": "Total Amount (NGN)"}
                    },
                    "lineage": {
                        "concept_ids": [C_PC],
                        "teaching_block_ids": [qid(C_PC,"tb1")],
                        "fact_ids": [qid(C_PC,"f1")],
                        "anchors": [qid(C_PC,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PC],
                [qid(C_PC,"tb1"), qid(C_PC,"tb2")],
                [qid(C_PC,"f1"), qid(C_PC,"f2")],
                anchors=[qid(C_PC,"visual")]
            )
        },
        # s11 – video
        {
            "step_id": f"{T3}.s11",
            "type": "video",
            "concept_ids": [C_PC],
            "eyebrow": "Watch",
            "title": "When a Pie Chart Works: Proportional Slices",
            "lede": "See how even-split versus clear-winner data affects whether a pie chart communicates clearly.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T3}.s11.mg1",
                    "segment_ids": ["seg_spreadsheet.pie_chart_creation_VgBxnayDXk0_38_198"]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PC],
                [],
                [qid(C_PC,"f1")],
                seg_ids=["seg_spreadsheet.pie_chart_creation_VgBxnayDXk0_38_198"]
            )
        },
        # s12 – check (framing only)
        {
            "step_id": f"{T3}.s12",
            "type": "check",
            "concept_ids": [C_PC],
            "eyebrow": "Quick Check",
            "title": "Building a Pie Chart from Category Totals",
            "lede": "Test your understanding of pie chart eligibility conditions and the creation workflow.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_PC],
                [],
                [qid(C_PC,"f1"), qid(C_PC,"f2")],
                anchors=[qid(C_PC,"assessment:build_correctly_encoded_pie_chart_from_category_totals")]
            )
        },
        # s13 – hands_on (framing only)
        {
            "step_id": f"{T3}.s13",
            "type": "hands_on",
            "concept_ids": [C_PC],
            "eyebrow": "Practice",
            "title": "Build a Pie Chart from City Totals",
            "lede": "Select the city totals table and insert a pie chart using Insert > Recommended Charts.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_PC],
                [],
                [qid(C_PC,"f1"), qid(C_PC,"f2")],
                anchors=[
                    qid(C_PC,"practice"),
                    qid(C_PC,"assessment:identify_pie_chart_eligibility_conditions"),
                    qid(C_PC,"assessment:build_correctly_encoded_pie_chart_from_category_totals")
                ]
            )
        },
        # s14 – recap
        {
            "step_id": f"{T3}.s14",
            "type": "recap",
            "concept_ids": [C_BC, C_LC, C_PC],
            "eyebrow": "Recap",
            "title": "Chart Types — Key Points",
            "lede": "You can now build bar, line, and pie charts and choose the right type for your data.",
            "blocks": [
                prose(f"{T3}.s14.p1", "takeaway",
                    "Bar charts compare categories: the category axis holds labels and the value axis holds bar heights. Line charts show trends over equal time intervals: months, quarters, or fiscal years go on the horizontal axis and values on the vertical axis. Pie charts show part-of-whole shares and require one data series, no negative values, no more than seven categories, and categories that sum to a meaningful whole. For all three types, select the data and use Insert > Recommended Charts to preview and insert.",
                    [C_BC, C_LC, C_PC],
                    [qid(C_BC,"tb1"), qid(C_BC,"tb2"),
                     qid(C_LC,"tb1"), qid(C_LC,"tb2"),
                     qid(C_PC,"tb1"), qid(C_PC,"tb2")],
                    [qid(C_BC,"f1"), qid(C_BC,"f2"),
                     qid(C_LC,"f1"), qid(C_LC,"f2"),
                     qid(C_PC,"f1"), qid(C_PC,"f2")]),
                {
                    "type": "up_next",
                    "block_id": f"{T3}.s14.up_next",
                    "title": "Next: Python Figures and Layouts",
                    "text": "In the next tile you'll move from spreadsheet charts to Python's matplotlib, building figures with axes and controlling layout programmatically."
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_BC, C_LC, C_PC],
                [qid(C_BC,"tb1"), qid(C_BC,"tb2"),
                 qid(C_LC,"tb1"), qid(C_LC,"tb2"),
                 qid(C_PC,"tb1"), qid(C_PC,"tb2")],
                [qid(C_BC,"f1"), qid(C_BC,"f2"),
                 qid(C_LC,"f1"), qid(C_LC,"f2"),
                 qid(C_PC,"f1"), qid(C_PC,"f2")]
            )
        }
    ],
    "remediation_steps": [
        # r01 – for s03 check (build_correctly_encoded_bar_chart → f1, f2)
        {
            "step_id": f"{T3}.r01",
            "type": "remediation",
            "concept_ids": [C_BC],
            "eyebrow": "Let's Revisit",
            "title": "Bar Chart Axis Encoding and Creation Steps",
            "lede": "A clear contrast shows which data goes on which axis and how to insert the chart.",
            "blocks": [
                prose(f"{T3}.r01.p1", "example",
                    "In a bar chart, categories go on one axis and values on the other. For the city totals table, city names go on the category axis and total_amount values determine bar height. To insert: select the city and total_amount columns, choose Insert > Recommended Charts, preview the bar chart, and click OK. If the bar chart is not on the Recommended tab, open All Charts, select Bar, and click OK.",
                    [C_BC],
                    [qid(C_BC,"tb1"), qid(C_BC,"tb2")],
                    [qid(C_BC,"f1"), qid(C_BC,"f2")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_BC],
                [qid(C_BC,"tb1"), qid(C_BC,"tb2")],
                [qid(C_BC,"f1"), qid(C_BC,"f2")]
            )
        },
        # r02 – for s07 check (identify_axis_roles_and_interval_suitability → f1)
        {
            "step_id": f"{T3}.r02",
            "type": "remediation",
            "concept_ids": [C_LC],
            "eyebrow": "Let's Revisit",
            "title": "Line Chart Axis Roles and When to Use One",
            "lede": "Equal time intervals on the horizontal axis make a line chart the right choice.",
            "blocks": [
                prose(f"{T3}.r02.p1", "example",
                    "In a line chart, category data — typically time labels such as Jan-2024, Feb-2024 — is distributed evenly along the horizontal axis, and value data goes on the vertical axis. Line charts are well suited to data measured at equal intervals: months, quarters, or fiscal years. The monthly summary table has six months at equal intervals, so a line chart shows the trend clearly. A table of city totals is not time-ordered, so a bar chart is more appropriate there.",
                    [C_LC],
                    [qid(C_LC,"tb1")],
                    [qid(C_LC,"f1")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_LC],
                [qid(C_LC,"tb1")],
                [qid(C_LC,"f1")]
            )
        },
        # r03 – for s12 check (build_correctly_encoded_pie_chart → f1, f2)
        {
            "step_id": f"{T3}.r03",
            "type": "remediation",
            "concept_ids": [C_PC],
            "eyebrow": "Let's Revisit",
            "title": "Pie Chart Eligibility and Creation",
            "lede": "Four conditions must hold before a pie chart is appropriate.",
            "blocks": [
                prose(f"{T3}.r03.p1", "example",
                    "A pie chart is appropriate when: (1) you have only one data series to plot, (2) none of the values are negative, (3) there are no more than seven categories, and (4) the categories represent parts of the whole. The city totals table has six cities (≤ 7), all positive amounts, one series, and the cities together represent all orders — so a pie chart is appropriate. To insert: select the city and total_amount columns, choose Insert > Recommended Charts, preview the pie chart, and click OK.",
                    [C_PC],
                    [qid(C_PC,"tb1"), qid(C_PC,"tb2")],
                    [qid(C_PC,"f1"), qid(C_PC,"f2")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_PC],
                [qid(C_PC,"tb1"), qid(C_PC,"tb2")],
                [qid(C_PC,"f1"), qid(C_PC,"f2")]
            )
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# TILE 4: tile_spreadsheet_formatting_validation
# ─────────────────────────────────────────────────────────────────────────────
T4 = "tile_spreadsheet_formatting_validation"
C_CF = "spreadsheet.conditional_formatting"
C_DV = "spreadsheet.data_validation"

tile_formatting_validation = {
    "tile_id": T4,
    "title": "Conditional Formatting and Data Validation",
    "summary": "Apply automatic cell formatting based on value rules, and restrict what users can enter into a cell.",
    "steps": [
        # s01 – explainer, before_after visual
        {
            "step_id": f"{T4}.s01",
            "type": "explainer",
            "concept_ids": [C_CF],
            "eyebrow": "Concept",
            "title": "Highlighting Cells Automatically by Value",
            "lede": "Conditional formatting applies a format to cells based on rules you create — no manual colouring needed.",
            "blocks": [
                prose(f"{T4}.s01.p1", "definition",
                    "Conditional formatting applies a format to cells automatically based on rules you create that determine the format based on the cells' values — rather than you manually colouring cells one at a time.",
                    [C_CF],
                    [qid(C_CF,"tb1")],
                    [qid(C_CF,"f1")]),
                prose(f"{T4}.s01.p2", "mechanism",
                    "To apply a quick conditional formatting rule, select the cells, then on the Home tab in the Style group select Conditional Formatting > Highlight Cells Rules, choose a comparison command such as Less Than, enter the comparison value, and select a format. Selecting the delivery-time column and applying Highlight Cells Rules > Less Than with a value of 15 and a green fill automatically colours every delivery under 15 minutes.",
                    [C_CF],
                    [qid(C_CF,"tb2")],
                    [qid(C_CF,"f2")]),
                {
                    "type": "before_after",
                    "block_id": f"{T4}.s01.ba1",
                    "before": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None,
                                      "columns": ["order_id", "delivery_minutes"]},
                        "range": "A1:B8",
                        "sheet_name": "Orders",
                        "annotations": [
                            {"target": "B1:B8", "text": "delivery_minutes — no formatting applied"}
                        ]
                    },
                    "after": {
                        "type": "spreadsheet_grid",
                        "asset_ref": {"asset_id": "asset_orders_clean", "variant_id": None,
                                      "columns": ["order_id", "delivery_minutes"]},
                        "range": "A1:B8",
                        "sheet_name": "Orders",
                        "annotations": [
                            {"target": "B2", "text": "28 — no fill (≥ 15)"},
                            {"target": "B6", "text": "19 — no fill (≥ 15)"},
                            {"target": "B11", "text": "14 — green fill (< 15)"}
                        ]
                    },
                    "change_summary": "Home > Conditional Formatting > Highlight Cells Rules > Less Than, value 15, green fill — cells below 15 are automatically coloured; cells at or above 15 remain unformatted.",
                    "lineage": {
                        "concept_ids": [C_CF],
                        "teaching_block_ids": [qid(C_CF,"tb1"), qid(C_CF,"tb2")],
                        "fact_ids": [qid(C_CF,"f1"), qid(C_CF,"f2")],
                        "anchors": [qid(C_CF,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_CF],
                [qid(C_CF,"tb1"), qid(C_CF,"tb2")],
                [qid(C_CF,"f1"), qid(C_CF,"f2")],
                anchors=[qid(C_CF,"visual")]
            )
        },
        # s02 – video
        {
            "step_id": f"{T4}.s02",
            "type": "video",
            "concept_ids": [C_CF],
            "eyebrow": "Watch",
            "title": "Applying a Conditional Formatting Rule via Highlight Cells Rules",
            "lede": "See the menu path and how the rule re-evaluates automatically when cell values change.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T4}.s02.mg1",
                    "segment_ids": ["seg_spreadsheet.conditional_formatting__eZRkmRfVTM_467_520"]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_CF],
                [],
                [qid(C_CF,"f1"), qid(C_CF,"f2")],
                seg_ids=["seg_spreadsheet.conditional_formatting__eZRkmRfVTM_467_520"]
            )
        },
        # s03 – check (framing only)
        {
            "step_id": f"{T4}.s03",
            "type": "check",
            "concept_ids": [C_CF],
            "eyebrow": "Quick Check",
            "title": "Applying a Conditional Formatting Rule",
            "lede": "Test your understanding of how to set up a Highlight Cells Rules rule.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_CF],
                [],
                [qid(C_CF,"f1"), qid(C_CF,"f2")],
                anchors=[qid(C_CF,"assessment:apply_conditional_formatting_rule_for_given_condition")]
            )
        },
        # s04 – hands_on (framing only)
        {
            "step_id": f"{T4}.s04",
            "type": "hands_on",
            "concept_ids": [C_CF],
            "eyebrow": "Practice",
            "title": "Apply a Less Than Rule to Delivery Times",
            "lede": "Use Highlight Cells Rules to colour delivery times below a threshold in red.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_CF],
                [],
                [qid(C_CF,"f1"), qid(C_CF,"f2")],
                anchors=[
                    qid(C_CF,"practice"),
                    qid(C_CF,"assessment:apply_conditional_formatting_rule_for_given_condition")
                ]
            )
        },
        # s05 – explainer, annotated_image visual
        {
            "step_id": f"{T4}.s05",
            "type": "explainer",
            "concept_ids": [C_DV],
            "eyebrow": "Concept",
            "title": "Restricting What Users Can Enter",
            "lede": "Data validation restricts the type of data or values users can enter into a cell, and can display a custom error message.",
            "blocks": [
                prose(f"{T4}.s05.p1", "definition",
                    "Data validation restricts the type of data or the values users can enter into a cell, such as a dropdown list, and can display a customised error message when a user enters invalid data.",
                    [C_DV],
                    [qid(C_DV,"tb1")],
                    [qid(C_DV,"f1")]),
                prose(f"{T4}.s05.p2", "example",
                    "To add a dropdown-list validation rule, select the cells, choose Data > Data Validation, on the Settings tab set Allow to List, then in the Source box type the list values separated by commas, making sure the In-cell dropdown check box is selected. Restricting the Orders sheet's status column with Source set to Pending,Delivered,Cancelled gives each cell a dropdown of those three words.",
                    [C_DV],
                    [qid(C_DV,"tb2")],
                    [qid(C_DV,"f2")]),
                {
                    "type": "annotated_image",
                    "block_id": f"{T4}.s05.ai1",
                    "asset_id": "img_data_validation_dialog",
                    "alt_text": "Screenshot of the Data Validation dialog open on the Settings tab with Allow set to List and the Source box containing 'Pending,Delivered,Cancelled', alongside a Status column cell showing a dropdown arrow.",
                    "hotspots": [
                        {"x": 0.10, "y": 0.20, "w": 0.35, "h": 0.08,
                         "label": "Allow: List",
                         "detail": "Set Allow to List to create a dropdown restriction."},
                        {"x": 0.10, "y": 0.45, "w": 0.75, "h": 0.08,
                         "label": "Source: Pending,Delivered,Cancelled",
                         "detail": "Type the allowed values separated by commas. These become the dropdown options."},
                        {"x": 0.10, "y": 0.60, "w": 0.40, "h": 0.06,
                         "label": "In-cell dropdown checked",
                         "detail": "Ensures the dropdown arrow appears in the cell."},
                        {"x": 0.65, "y": 0.30, "w": 0.30, "h": 0.12,
                         "label": "Dropdown arrow in Status cell",
                         "detail": "The cell now shows a dropdown arrow; only the three listed values are accepted."}
                    ],
                    "lineage": {
                        "concept_ids": [C_DV],
                        "teaching_block_ids": [qid(C_DV,"tb1"), qid(C_DV,"tb2")],
                        "fact_ids": [qid(C_DV,"f1"), qid(C_DV,"f2")],
                        "anchors": [qid(C_DV,"visual")]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_DV],
                [qid(C_DV,"tb1"), qid(C_DV,"tb2")],
                [qid(C_DV,"f1"), qid(C_DV,"f2")],
                anchors=[qid(C_DV,"visual")]
            )
        },
        # s06 – explainer (tb3, f3) — no visual planned
        {
            "step_id": f"{T4}.s06",
            "type": "explainer",
            "concept_ids": [C_DV],
            "eyebrow": "Concept",
            "title": "Numeric, Date, and Text-Length Validation",
            "lede": "Data validation can also restrict entry to a number, date, or text of a specific length.",
            "blocks": [
                prose(f"{T4}.s06.p1", "example",
                    "Data validation can restrict entry to a whole number, decimal, date, time, or text length within limits: under Allow choose the type (for example Whole Number), under Data choose a condition (for example between), and then enter the minimum, maximum, or specific value to allow. On the delivery-time column, choosing Whole Number, between 0 and 300, blocks anyone from typing a negative or unreasonably large delivery time.",
                    [C_DV],
                    [qid(C_DV,"tb3")],
                    [qid(C_DV,"f3")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_DV],
                [qid(C_DV,"tb3")],
                [qid(C_DV,"f3")]
            )
        },
        # s07 – video
        {
            "step_id": f"{T4}.s07",
            "type": "video",
            "concept_ids": [C_DV],
            "eyebrow": "Watch",
            "title": "Restricting Cell Input: Error Alerts and Numeric Rules",
            "lede": "See how the Allow menu switches between types and how error alerts work.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": f"{T4}.s07.mg1",
                    "segment_ids": ["seg_spreadsheet.data_validation_FRiFfKb_B_A_494_849"]
                }
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_DV],
                [],
                [qid(C_DV,"f1"), qid(C_DV,"f3")],
                seg_ids=["seg_spreadsheet.data_validation_FRiFfKb_B_A_494_849"]
            )
        },
        # s08 – check (framing only)
        {
            "step_id": f"{T4}.s08",
            "type": "check",
            "concept_ids": [C_DV],
            "eyebrow": "Quick Check",
            "title": "Data Validation Purpose and Numeric Rules",
            "lede": "Test your understanding of what data validation does and how to configure a numeric rule.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_DV],
                [],
                [qid(C_DV,"f1"), qid(C_DV,"f3")],
                anchors=[
                    qid(C_DV,"assessment:identify_data_validation_purpose_and_error_message_behaviour"),
                    qid(C_DV,"assessment:configure_numeric_date_or_text_length_validation_with_condition_and_limits")
                ]
            )
        },
        # s09 – check (framing only)
        {
            "step_id": f"{T4}.s09",
            "type": "check",
            "concept_ids": [C_DV],
            "eyebrow": "Quick Check",
            "title": "Choosing the Right Validation Type",
            "lede": "Given an input restriction requirement, identify the correct validation type to use.",
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_DV],
                [],
                [qid(C_DV,"f1"), qid(C_DV,"f2"), qid(C_DV,"f3")],
                anchors=[qid(C_DV,"assessment:select_correct_validation_type_for_a_given_input_restriction_requirement")]
            )
        },
        # s10 – hands_on (framing only)
        {
            "step_id": f"{T4}.s10",
            "type": "hands_on",
            "concept_ids": [C_DV],
            "eyebrow": "Practice",
            "title": "Add a Dropdown Validation Rule to the Status Column",
            "lede": "Restrict the Status column to Pending, Delivered, and Cancelled using Data > Data Validation.",
            "reward": {"gems": 10},
            "lineage": step_lineage(
                [C_DV],
                [],
                [qid(C_DV,"f2")],
                anchors=[
                    qid(C_DV,"practice"),
                    qid(C_DV,"assessment:configure_dropdown_list_validation_with_source_values")
                ]
            )
        },
        # s11 – recap
        {
            "step_id": f"{T4}.s11",
            "type": "recap",
            "concept_ids": [C_CF, C_DV],
            "eyebrow": "Recap",
            "title": "Conditional Formatting and Data Validation — Key Points",
            "lede": "You can now apply automatic cell formatting rules and restrict what users can enter.",
            "blocks": [
                prose(f"{T4}.s11.p1", "takeaway",
                    "Conditional formatting applies a format to cells automatically based on rules you create from cell values. Use Home > Conditional Formatting > Highlight Cells Rules, choose a comparison such as Less Than, enter the threshold, and pick a format. Data validation restricts what users can enter: choose Data > Data Validation, set Allow to List and type comma-separated values for a dropdown, or choose Whole Number, Date, or Text Length with a condition and limits for numeric restrictions. A customised error message can be shown when invalid data is entered.",
                    [C_CF, C_DV],
                    [qid(C_CF,"tb1"), qid(C_CF,"tb2"),
                     qid(C_DV,"tb1"), qid(C_DV,"tb2"), qid(C_DV,"tb3")],
                    [qid(C_CF,"f1"), qid(C_CF,"f2"),
                     qid(C_DV,"f1"), qid(C_DV,"f2"), qid(C_DV,"f3")]),
                {
                    "type": "up_next",
                    "block_id": f"{T4}.s11.up_next",
                    "title": "Next: Cleaning and Cross-Sheet References",
                    "text": "In the next tile you'll remove duplicates, split combined text into columns, and reference data across sheets in the same workbook."
                }
            ],
            "reward": {"gems": 5},
            "lineage": step_lineage(
                [C_CF, C_DV],
                [qid(C_CF,"tb1"), qid(C_CF,"tb2"),
                 qid(C_DV,"tb1"), qid(C_DV,"tb2"), qid(C_DV,"tb3")],
                [qid(C_CF,"f1"), qid(C_CF,"f2"),
                 qid(C_DV,"f1"), qid(C_DV,"f2"), qid(C_DV,"f3")]
            )
        }
    ],
    "remediation_steps": [
        # r01 – for s03 check (apply_conditional_formatting_rule → f1, f2)
        {
            "step_id": f"{T4}.r01",
            "type": "remediation",
            "concept_ids": [C_CF],
            "eyebrow": "Let's Revisit",
            "title": "Setting Up a Highlight Cells Rule",
            "lede": "Walk through the exact menu path and see the rule trigger automatically.",
            "blocks": [
                prose(f"{T4}.r01.p1", "example",
                    "Conditional formatting applies a format automatically based on cell values — you do not colour cells manually. To apply a Less Than rule to the delivery-time column: select the column cells, go to Home > Conditional Formatting > Highlight Cells Rules > Less Than, type 15 in the value box, choose a red fill, and click OK. Every cell whose value is below 15 is immediately coloured red; cells at or above 15 remain unformatted. The rule re-evaluates whenever a cell value changes.",
                    [C_CF],
                    [qid(C_CF,"tb1"), qid(C_CF,"tb2")],
                    [qid(C_CF,"f1"), qid(C_CF,"f2")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_CF],
                [qid(C_CF,"tb1"), qid(C_CF,"tb2")],
                [qid(C_CF,"f1"), qid(C_CF,"f2")]
            )
        },
        # r02 – for s08 check (identify_data_validation_purpose → f1; configure_numeric → f3)
        {
            "step_id": f"{T4}.r02",
            "type": "remediation",
            "concept_ids": [C_DV],
            "eyebrow": "Let's Revisit",
            "title": "What Data Validation Does and How to Set Numeric Limits",
            "lede": "Data validation blocks invalid input before it reaches the cell.",
            "blocks": [
                prose(f"{T4}.r02.p1", "example",
                    "Data validation restricts the type of data or the values users can enter into a cell, and can display a customised error message when a user enters invalid data. For a numeric restriction on the delivery-time column: select the column, choose Data > Data Validation, set Allow to Whole Number, set Data to between, enter 0 as the minimum and 300 as the maximum, and click OK. Typing a negative number or a value above 300 triggers the restriction notice.",
                    [C_DV],
                    [qid(C_DV,"tb1"), qid(C_DV,"tb3")],
                    [qid(C_DV,"f1"), qid(C_DV,"f3")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_DV],
                [qid(C_DV,"tb1"), qid(C_DV,"tb3")],
                [qid(C_DV,"f1"), qid(C_DV,"f3")]
            )
        },
        # r03 – for s09 check (select_correct_validation_type → f1, f2, f3)
        {
            "step_id": f"{T4}.r03",
            "type": "remediation",
            "concept_ids": [C_DV],
            "eyebrow": "Let's Revisit",
            "title": "Choosing the Right Validation Type",
            "lede": "Match the input restriction requirement to the correct Allow setting.",
            "blocks": [
                prose(f"{T4}.r03.p1", "example",
                    "Use List when you want to restrict entry to a fixed set of text values — for example, Pending, Delivered, Cancelled in the status column. Use Whole Number or Decimal when you want to restrict entry to a number within a range — for example, delivery times between 0 and 300. Use Date or Time for date or time restrictions. Use Text Length when you want to restrict how many characters can be entered. All types are set through Data > Data Validation > Settings > Allow.",
                    [C_DV],
                    [qid(C_DV,"tb1"), qid(C_DV,"tb2"), qid(C_DV,"tb3")],
                    [qid(C_DV,"f1"), qid(C_DV,"f2"), qid(C_DV,"f3")])
            ],
            "reward": {"gems": 3},
            "lineage": step_lineage(
                [C_DV],
                [qid(C_DV,"tb1"), qid(C_DV,"tb2"), qid(C_DV,"tb3")],
                [qid(C_DV,"f1"), qid(C_DV,"f2"), qid(C_DV,"f3")]
            )
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# Assemble output
# ─────────────────────────────────────────────────────────────────────────────
output = {
    "schema_version": "1.0.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "tiles": [
        tile_tables_named_ranges,
        tile_pivot_tables,
        tile_chart_types,
        tile_formatting_validation
    ]
}

with open(OUT, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {OUT}")
# Count steps
for tile in output["tiles"]:
    steps = tile["steps"]
    rem = tile.get("remediation_steps", [])
    print(f"  {tile['tile_id']}: {len(steps)} steps, {len(rem)} remediation steps")
