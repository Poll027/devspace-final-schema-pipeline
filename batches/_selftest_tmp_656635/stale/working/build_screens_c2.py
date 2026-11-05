"""Build screens.part.c2.json for tiles:
  - tile_capstone_integrate_tools_model
  - tile_capstone_stats_dashboard
"""
import json

# ── helpers ──────────────────────────────────────────────────────────────────

def prose(block_id, role, text, concept_ids, fact_ids, tb_ids, anchors=None):
    lin = {"concept_ids": concept_ids, "fact_ids": fact_ids, "teaching_block_ids": tb_ids}
    if anchors:
        lin["anchors"] = anchors
    return {"type": "prose", "block_id": block_id, "role": role, "text": text, "lineage": lin}

def heading(block_id, text, level=2):
    return {"type": "heading", "block_id": block_id, "text": text, "level": level}

def media_group(block_id, group_title, segment_ids):
    return {"type": "media_group", "block_id": block_id,
            "group_title": group_title, "segment_ids": segment_ids, "default_mode": "video"}

def step_lineage(concept_ids, fact_ids, tb_ids=None, seg_ids=None, anchors=None):
    lin = {"concept_ids": concept_ids, "fact_ids": fact_ids}
    if tb_ids is not None:
        lin["teaching_block_ids"] = tb_ids
    if seg_ids is not None:
        lin["segment_ids"] = seg_ids
    if anchors is not None:
        lin["anchors"] = anchors
    return lin

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 1: tile_capstone_integrate_tools_model
# ═══════════════════════════════════════════════════════════════════════════════

T1 = "tile_capstone_integrate_tools_model"

# ── s01: explainer – integrate_sql – code_walkthrough visual ─────────────────
s01 = {
    "step_id": f"{T1}.s01",
    "type": "explainer",
    "concept_ids": ["capstone.integrate_sql"],
    "eyebrow": "SQL Integration",
    "title": "One SELECT statement: JOIN, WHERE, and GROUP BY together",
    "lede": "The first step of the QuickRide capstone is retrieving last quarter's delivery data. All the SQL clauses you already know — JOIN, WHERE, and GROUP BY — can live in a single SELECT statement.",
    "blocks": [
        heading(f"{T1}.s01.b1", "Combining clauses in one query"),
        prose(
            f"{T1}.s01.b2", "mechanism",
            "A single SELECT statement's syntax allows a FROM clause, a WHERE clause, and a GROUP BY clause to appear together in the same query. "
            "In the capstone, that means one statement can filter orders down to last quarter's rows **and** group the result by zone — no separate steps needed.",
            ["capstone.integrate_sql"],
            ["capstone.integrate_sql#f1"],
            ["capstone.integrate_sql#tb2"]
        ),
        prose(
            f"{T1}.s01.b3", "mechanism",
            "An INNER JOIN can be included in that same FROM clause to combine matching rows from more than one table **before** WHERE filtering or GROUP BY grouping is applied. "
            "In the capstone, the `orders` and `drivers` tables are joined in the FROM clause first; the WHERE and GROUP BY then narrow and group the combined rows.",
            ["capstone.integrate_sql"],
            ["capstone.integrate_sql#f2"],
            ["capstone.integrate_sql#tb3"]
        ),
        {
            "type": "code_walkthrough",
            "block_id": f"{T1}.s01.b4",
            "language": "sql",
            "code": (
                "SELECT o.zone,\n"
                "       AVG(o.delivery_time) AS avg_delivery_time\n"
                "FROM   orders o\n"
                "       INNER JOIN drivers d\n"
                "           ON o.driver_id = d.driver_id\n"
                "WHERE  o.order_date >= '2026-04-01'\n"
                "  AND  o.order_date <  '2026-07-01'\n"
                "GROUP BY o.zone;"
            ),
            "annotations": [
                {"start_line": 3, "end_line": 5,
                 "text": "FROM + INNER JOIN: combines each order row with its matching driver row first."},
                {"start_line": 6, "end_line": 7,
                 "text": "WHERE: narrows the combined rows to last quarter (2026-04-01 to 2026-06-30)."},
                {"start_line": 8, "end_line": 8,
                 "text": "GROUP BY: groups the filtered rows by zone so AVG gives one value per zone."}
            ],
            "reveal": "all",
            "lineage": {
                "concept_ids": ["capstone.integrate_sql"],
                "fact_ids": ["capstone.integrate_sql#f1", "capstone.integrate_sql#f2"],
                "teaching_block_ids": ["capstone.integrate_sql#tb2", "capstone.integrate_sql#tb3", "capstone.integrate_sql#tb4"],
                "anchors": ["capstone.integrate_sql#visual"]
            }
        }
    ],
    "reward": {"gems": 3},
    "lineage": step_lineage(
        ["capstone.integrate_sql"],
        ["capstone.integrate_sql#f1", "capstone.integrate_sql#f2"],
        ["capstone.integrate_sql#tb1", "capstone.integrate_sql#tb2", "capstone.integrate_sql#tb3"],
        anchors=["capstone.integrate_sql#visual"]
    )
}

# ── s02: explainer – integrate_sql – prose only ──────────────────────────────
s02 = {
    "step_id": f"{T1}.s02",
    "type": "explainer",
    "concept_ids": ["capstone.integrate_sql"],
    "eyebrow": "SQL Integration",
    "title": "Clause order: join first, filter next, group last",
    "lede": "The capstone query uses the same SELECT, FROM, WHERE, JOIN, and GROUP BY you already know — aimed at QuickRide's own tables and date range.",
    "blocks": [
        prose(
            f"{T1}.s02.b1", "example",
            "In the capstone query, the INNER JOIN in the FROM clause combines each order row with its matching driver row first. "
            "The WHERE clause then narrows those combined rows to orders placed between 2026-04-01 and 2026-06-30. "
            "Finally, GROUP BY groups what remains by zone, so AVG(delivery_time) returns one average per zone. "
            "None of this is new syntax — it is the same clauses already learned, applied to QuickRide's own tables.",
            ["capstone.integrate_sql"],
            ["capstone.integrate_sql#f1", "capstone.integrate_sql#f2"],
            ["capstone.integrate_sql#tb4", "capstone.integrate_sql#tb5"]
        )
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.integrate_sql"],
        ["capstone.integrate_sql#f1", "capstone.integrate_sql#f2"],
        ["capstone.integrate_sql#tb4"]
    )
}

# ── s03: video – integrate_sql ───────────────────────────────────────────────
s03 = {
    "step_id": f"{T1}.s03",
    "type": "video",
    "concept_ids": ["capstone.integrate_sql"],
    "eyebrow": "SQL Integration",
    "title": "Watch: building a JOIN + WHERE + GROUP BY query",
    "lede": "This clip shows a multi-clause SELECT being built from scratch. Note: the date function used is SQL Server-specific; the capstone uses a plain date comparison in WHERE instead.",
    "blocks": [
        media_group(
            f"{T1}.s03.b1",
            "Building a JOIN + WHERE + GROUP BY query from scratch in a single SELECT",
            ["seg_capstone.integrate_sql_xkYpNfpmbGY_592_770"]
        )
    ],
    "reward": {"gems": 1},
    "lineage": step_lineage(
        ["capstone.integrate_sql"],
        ["capstone.integrate_sql#f1", "capstone.integrate_sql#f2"],
        seg_ids=["seg_capstone.integrate_sql_xkYpNfpmbGY_592_770"]
    )
}

# ── s04: check – integrate_sql ───────────────────────────────────────────────
s04 = {
    "step_id": f"{T1}.s04",
    "type": "check",
    "concept_ids": ["capstone.integrate_sql"],
    "eyebrow": "Quick check",
    "title": "Where does the INNER JOIN go?",
    "lede": "Test your understanding of where a JOIN fits inside a SELECT statement.",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.integrate_sql"],
        ["capstone.integrate_sql#f2"],
        tb_ids=[],
        anchors=["capstone.integrate_sql#assessment:include_inner_join_in_from_clause_before_where_and_group_by"]
    )
}

# ── s05: hands_on – integrate_sql ────────────────────────────────────────────
s05 = {
    "step_id": f"{T1}.s05",
    "type": "hands_on",
    "concept_ids": ["capstone.integrate_sql"],
    "eyebrow": "Hands-on practice",
    "title": "Write the capstone retrieval query",
    "lede": "Write the SQL query that retrieves last quarter's QuickRide orders, joining the orders and drivers tables, filtering to the correct date range, and grouping by zone.",
    "reward": {"gems": 4, "first_try_bonus": 2},
    "lineage": step_lineage(
        ["capstone.integrate_sql"],
        ["capstone.integrate_sql#f1", "capstone.integrate_sql#f2"],
        tb_ids=[],
        anchors=[
            "capstone.integrate_sql#practice",
            "capstone.integrate_sql#assessment:write_select_with_from_where_group_by_in_one_statement",
            "capstone.integrate_sql#assessment:apply_combined_join_filter_group_query_to_capstone_dataset"
        ]
    )
}

# ── s06: explainer – integrate_spreadsheet – spreadsheet_grid visual ─────────
s06 = {
    "step_id": f"{T1}.s06",
    "type": "explainer",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Spreadsheet Integration",
    "title": "PivotTable and COUNTIFS on the capstone delivery sheet",
    "lede": "The capstone's spreadsheet step pairs each order's zone and delivery_time with the driver's shift. A PivotTable and COUNTIFS turn that sheet into a zone-by-shift summary.",
    "blocks": [
        heading(f"{T1}.s06.b1", "Building a PivotTable from the delivery sheet"),
        prose(
            f"{T1}.s06.b2", "mechanism",
            "A PivotTable is built by selecting the data range and inserting a PivotTable, then adding fields: non-numeric fields default to Rows, date/time fields to Columns, and numeric fields to Values. "
            "Fields can be dragged between areas to rearrange the summary. "
            "In the capstone, `zone` and `shift` (both non-numeric) default to Rows, while `delivery_time` (numeric) goes to Values.",
            ["capstone.integrate_spreadsheet"],
            ["capstone.integrate_spreadsheet#f1"],
            ["capstone.integrate_spreadsheet#tb2"]
        ),
        prose(
            f"{T1}.s06.b3", "mechanism",
            "COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2]…) applies criteria across one or more ranges and counts the cells where **all** criteria are met. "
            "In the capstone, `COUNTIFS(zone_range, \"Ikeja\", delivery_time_range, \">45\")` counts how many Ikeja deliveries exceeded 45 minutes.",
            ["capstone.integrate_spreadsheet"],
            ["capstone.integrate_spreadsheet#f2"],
            ["capstone.integrate_spreadsheet#tb3"]
        ),
        {
            "type": "spreadsheet_grid",
            "block_id": f"{T1}.s06.b4",
            "asset_ref": {"asset_id": "ds_capstone_delivery_sheet"},
            "sheet_name": "DeliverySheet",
            "range": "A1:C10",
            "show_formula_bar": True,
            "cells": [
                {"ref": "E1", "note": "PivotTable: zone (Rows) × shift (Columns), Average delivery_time (Values)"},
                {"ref": "E8", "formula": "=COUNTIFS(A2:A37,\"Ikeja\",C2:C37,\">45\")",
                 "note": "Count Ikeja deliveries over 45 minutes"}
            ],
            "annotations": [
                {"target": "A1:C1", "text": "Source data: zone, shift, delivery_time"},
                {"target": "E1", "text": "PivotTable output: zone × shift grid, Average delivery_time per cell"},
                {"target": "E8", "text": "COUNTIFS: counts rows where zone=Ikeja AND delivery_time>45"}
            ],
            "lineage": {
                "concept_ids": ["capstone.integrate_spreadsheet"],
                "fact_ids": ["capstone.integrate_spreadsheet#f1", "capstone.integrate_spreadsheet#f2"],
                "teaching_block_ids": ["capstone.integrate_spreadsheet#tb2", "capstone.integrate_spreadsheet#tb3"],
                "anchors": ["capstone.integrate_spreadsheet#visual"]
            }
        }
    ],
    "reward": {"gems": 3},
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f1", "capstone.integrate_spreadsheet#f2"],
        ["capstone.integrate_spreadsheet#tb1", "capstone.integrate_spreadsheet#tb2", "capstone.integrate_spreadsheet#tb3"],
        anchors=["capstone.integrate_spreadsheet#visual"]
    )
}

# ── s07: explainer – integrate_spreadsheet – prose only ──────────────────────
s07 = {
    "step_id": f"{T1}.s07",
    "type": "explainer",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Spreadsheet Integration",
    "title": "Rearranging the PivotTable and applying COUNTIFS",
    "lede": "Dragging shift from Rows to Columns turns the PivotTable into a zone-by-shift grid. COUNTIFS then counts deliveries that meet two criteria at once.",
    "blocks": [
        prose(
            f"{T1}.s07.b1", "example",
            "For the capstone delivery sheet, selecting the data range and inserting a PivotTable places `zone` and `shift` in Rows by default and `delivery_time` in Values. "
            "Dragging `shift` from Rows to Columns rearranges the summary into a zone-by-shift grid; changing the Values summary function to Average makes each cell an average delivery time.",
            ["capstone.integrate_spreadsheet"],
            ["capstone.integrate_spreadsheet#f1"],
            ["capstone.integrate_spreadsheet#tb4"]
        ),
        prose(
            f"{T1}.s07.b2", "example",
            "Separately, `COUNTIFS(zone_range, \"Ikeja\", delivery_time_range, \">45\")` counts how many Ikeja deliveries in the sheet took more than 45 minutes — both criteria (zone and time threshold) must be met at once. "
            "The PivotTable and COUNTIFS skills already learned are now run on this project's own roster and delivery data.",
            ["capstone.integrate_spreadsheet"],
            ["capstone.integrate_spreadsheet#f2"],
            ["capstone.integrate_spreadsheet#tb4", "capstone.integrate_spreadsheet#tb5"]
        )
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f1", "capstone.integrate_spreadsheet#f2"],
        ["capstone.integrate_spreadsheet#tb4"]
    )
}

# ── s08: video – integrate_spreadsheet ───────────────────────────────────────
s08 = {
    "step_id": f"{T1}.s08",
    "type": "video",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Spreadsheet Integration",
    "title": "Watch: inserting a PivotTable and arranging fields",
    "lede": "This clip shows how non-numeric fields land in Rows automatically and a numeric field jumps to Values. Note: the clip uses an advertising dataset, not the capstone's delivery sheet.",
    "blocks": [
        media_group(
            f"{T1}.s08.b1",
            "Building a PivotTable: selecting a range, inserting, and dragging fields",
            ["seg_capstone.integrate_spreadsheet_K3KqOTdypyw_36_302"]
        )
    ],
    "reward": {"gems": 1},
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f1"],
        seg_ids=["seg_capstone.integrate_spreadsheet_K3KqOTdypyw_36_302"]
    )
}

# ── s09: check – integrate_spreadsheet (COUNTIFS) ────────────────────────────
s09 = {
    "step_id": f"{T1}.s09",
    "type": "check",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Quick check",
    "title": "Applying COUNTIFS with multiple criteria",
    "lede": "Test your understanding of how COUNTIFS handles more than one criterion.",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f2"],
        tb_ids=[],
        anchors=["capstone.integrate_spreadsheet#assessment:apply_countifs_with_multiple_criteria_ranges"]
    )
}

# ── s10: check – integrate_spreadsheet (PivotTable) ──────────────────────────
s10 = {
    "step_id": f"{T1}.s10",
    "type": "check",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Quick check",
    "title": "Building a PivotTable with correct field placement",
    "lede": "Test your understanding of how fields are placed when you insert a PivotTable.",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f1"],
        tb_ids=[],
        anchors=["capstone.integrate_spreadsheet#assessment:build_pivot_table_with_correct_field_placement"]
    )
}

# ── s11: hands_on – integrate_spreadsheet ────────────────────────────────────
s11 = {
    "step_id": f"{T1}.s11",
    "type": "hands_on",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Hands-on practice",
    "title": "Build the capstone PivotTable and COUNTIFS formula",
    "lede": "Using the capstone delivery sheet, build a zone-by-shift PivotTable showing average delivery time, then write a COUNTIFS formula to count Ikeja deliveries over 45 minutes.",
    "reward": {"gems": 4, "first_try_bonus": 2},
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f1", "capstone.integrate_spreadsheet#f2"],
        tb_ids=[],
        anchors=[
            "capstone.integrate_spreadsheet#practice",
            "capstone.integrate_spreadsheet#assessment:execute_capstone_spreadsheet_analysis_step"
        ]
    )
}

# ── s12: explainer – integrate_python_pandas – before_after visual ────────────
s12 = {
    "step_id": f"{T1}.s12",
    "type": "explainer",
    "concept_ids": ["capstone.integrate_python_pandas"],
    "eyebrow": "Python / pandas Integration",
    "title": "Cleaning and grouping the capstone orders in pandas",
    "lede": "Once orders are retrieved, pandas handles cleaning and aggregation. isna()/dropna() remove missing delivery times; groupby().mean() produces one average per zone.",
    "blocks": [
        heading(f"{T1}.s12.b1", "Detecting and removing missing values"),
        prose(
            f"{T1}.s12.b2", "mechanism",
            "isna() detects which values in a DataFrame are missing, and dropna() removes rows with missing values — or fillna() replaces them with a specified value. "
            "In the capstone, `orders['delivery_time'].isna()` flags rows with no delivery time recorded; those rows are then removed with dropna() before any aggregation.",
            ["capstone.integrate_python_pandas"],
            ["capstone.integrate_python_pandas#f1"],
            ["capstone.integrate_python_pandas#tb2"]
        ),
        prose(
            f"{T1}.s12.b3", "mechanism",
            "A groupby operation splits data into groups based on some criteria, applies a function independently to each group, and combines the results back into a single structure. "
            "An aggregation reduces each group to one summary value per column. "
            "In the capstone, `orders.groupby('zone')['delivery_time'].mean()` splits the cleaned orders by zone and returns one mean delivery time per zone.",
            ["capstone.integrate_python_pandas"],
            ["capstone.integrate_python_pandas#f2"],
            ["capstone.integrate_python_pandas#tb3"]
        ),
        {
            "type": "before_after",
            "block_id": f"{T1}.s12.b4",
            "before": {
                "type": "data_table",
                "block_id": f"{T1}.s12.b4.before",
                "asset_ref": {"asset_id": "ds_pandas_orders", "columns": ["zone", "delivery_time"]},
                "caption": "Raw orders DataFrame — NaN delivery_time rows visible",
                "highlight": [
                    {"target": {"kind": "cell", "row": {"where": {"zone": "Ikeja", "delivery_time": None}}, "column": "delivery_time"},
                     "label": "NaN — missing delivery time", "tone": "bad"}
                ]
            },
            "after": {
                "type": "data_table",
                "block_id": f"{T1}.s12.b4.after",
                "result_of": {
                    "runtime": "sql",
                    "sql": "SELECT zone, AVG(delivery_time) AS mean_delivery_time FROM ds_pandas_orders WHERE delivery_time IS NOT NULL GROUP BY zone ORDER BY zone",
                    "asset_mounts": [{"asset_id": "ds_pandas_orders", "mount_path": "ds_pandas_orders"}]
                },
                "caption": "After dropna() + groupby('zone').mean() — one mean per zone"
            },
            "change_summary": "dropna() removes rows where delivery_time is NULL; groupby('zone')['delivery_time'].mean() reduces each zone to one average.",
            "lineage": {
                "concept_ids": ["capstone.integrate_python_pandas"],
                "fact_ids": ["capstone.integrate_python_pandas#f1", "capstone.integrate_python_pandas#f2"],
                "teaching_block_ids": ["capstone.integrate_python_pandas#tb2", "capstone.integrate_python_pandas#tb3", "capstone.integrate_python_pandas#tb4"],
                "anchors": ["capstone.integrate_python_pandas#visual"]
            }
        }
    ],
    "reward": {"gems": 3},
    "lineage": step_lineage(
        ["capstone.integrate_python_pandas"],
        ["capstone.integrate_python_pandas#f1", "capstone.integrate_python_pandas#f2"],
        ["capstone.integrate_python_pandas#tb1", "capstone.integrate_python_pandas#tb2", "capstone.integrate_python_pandas#tb3"],
        anchors=["capstone.integrate_python_pandas#visual"]
    )
}

# ── s13: explainer – integrate_python_pandas – prose only ────────────────────
s13 = {
    "step_id": f"{T1}.s13",
    "type": "explainer",
    "concept_ids": ["capstone.integrate_python_pandas"],
    "eyebrow": "Python / pandas Integration",
    "title": "The same skills, applied to the capstone's own data",
    "lede": "The isna()/dropna()/fillna() and groupby() skills already learned are now run on the capstone's retrieved orders instead of a practice dataset.",
    "blocks": [
        prose(
            f"{T1}.s13.b1", "example",
            "On the capstone's retrieved orders, `orders['delivery_time'].isna()` flags rows with no delivery time; dropna() removes them. "
            "Then `orders.groupby('zone')['delivery_time'].mean()` splits the cleaned orders by zone, computes the mean delivery time within each zone, and combines the per-zone results — an aggregation, since each zone group is reduced to a single number.",
            ["capstone.integrate_python_pandas"],
            ["capstone.integrate_python_pandas#f1", "capstone.integrate_python_pandas#f2"],
            ["capstone.integrate_python_pandas#tb4", "capstone.integrate_python_pandas#tb5"]
        )
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.integrate_python_pandas"],
        ["capstone.integrate_python_pandas#f1", "capstone.integrate_python_pandas#f2"],
        ["capstone.integrate_python_pandas#tb4"]
    )
}

# ── s14: check – integrate_python_pandas ─────────────────────────────────────
s14 = {
    "step_id": f"{T1}.s14",
    "type": "check",
    "concept_ids": ["capstone.integrate_python_pandas"],
    "eyebrow": "Quick check",
    "title": "Detecting and handling missing values",
    "lede": "Test your understanding of isna(), dropna(), and fillna() in the capstone context.",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.integrate_python_pandas"],
        ["capstone.integrate_python_pandas#f1"],
        tb_ids=[],
        anchors=["capstone.integrate_python_pandas#assessment:detect_and_handle_missing_values_with_isna_dropna_fillna"]
    )
}

# ── s15: hands_on – integrate_python_pandas ──────────────────────────────────
s15 = {
    "step_id": f"{T1}.s15",
    "type": "hands_on",
    "concept_ids": ["capstone.integrate_python_pandas"],
    "eyebrow": "Hands-on practice",
    "title": "Clean and aggregate the capstone orders",
    "lede": "Given a small orders DataFrame with zone and delivery_time columns (some NaN), detect the missing delivery times, remove those rows, then compute the mean delivery time per zone.",
    "reward": {"gems": 4, "first_try_bonus": 2},
    "lineage": step_lineage(
        ["capstone.integrate_python_pandas"],
        ["capstone.integrate_python_pandas#f1", "capstone.integrate_python_pandas#f2"],
        tb_ids=[],
        anchors=[
            "capstone.integrate_python_pandas#practice",
            "capstone.integrate_python_pandas#assessment:clean_and_aggregate_capstone_dataset_end_to_end"
        ]
    )
}

# ── s16: explainer – building_data_model – diagram visual ────────────────────
s16 = {
    "step_id": f"{T1}.s16",
    "type": "explainer",
    "concept_ids": ["capstone.building_data_model"],
    "eyebrow": "Data Modelling",
    "title": "Primary keys, foreign keys, and one-to-many in the capstone",
    "lede": "The capstone spans two tables — Orders and Drivers. Before any join or aggregation across them can be trusted, the key columns and their relationship need to be correctly identified.",
    "blocks": [
        heading(f"{T1}.s16.b1", "Primary keys and foreign keys"),
        prose(
            f"{T1}.s16.b2", "mechanism",
            "A primary key uniquely identifies each row of a table; a foreign key's values must match values appearing in some row of the table it references. "
            "In the capstone, the Drivers table needs a column that uniquely identifies each driver, and the Orders table needs a column whose values must match one of those driver identifiers.",
            ["capstone.building_data_model"],
            ["capstone.building_data_model#f1"],
            ["capstone.building_data_model#tb2"]
        ),
        prose(
            f"{T1}.s16.b3", "mechanism",
            "In a one-to-many relationship, one row on the 'one' side relates to many rows on the 'many' side — for example, one department has many employees. "
            "In the Customer/Order example, the foreign key CustID is placed in the Order table and must match a valid CustID in the Customer table. "
            "In the capstone, one driver can appear in many orders: the same one-to-many pattern.",
            ["capstone.building_data_model"],
            ["capstone.building_data_model#f2"],
            ["capstone.building_data_model#tb3"]
        ),
        {
            "type": "diagram",
            "block_id": f"{T1}.s16.b4",
            "diagram_kind": "erd",
            "title": "Capstone data model: Drivers (1) → Orders (many)",
            "nodes": [
                {
                    "id": "drivers_table",
                    "label": "Drivers",
                    "kind": "table",
                    "fields": ["driver_id (PK)", "driver_name"]
                },
                {
                    "id": "orders_table",
                    "label": "Orders",
                    "kind": "table",
                    "fields": ["order_id (PK)", "driver_id (FK)", "zone", "order_date", "delivery_time"]
                }
            ],
            "edges": [
                {
                    "from": "drivers_table",
                    "to": "orders_table",
                    "label": "one driver → many orders",
                    "cardinality": "1:N",
                    "directed": True
                }
            ],
            "layout": "auto",
            "alt_text": "Entity-relationship diagram showing two boxes: Drivers (driver_id as PK, driver_name) and Orders (order_id as PK, driver_id as FK, zone, order_date, delivery_time). An arrow from Drivers.driver_id to Orders.driver_id is labelled '1:N — one driver → many orders'.",
            "lineage": {
                "concept_ids": ["capstone.building_data_model"],
                "fact_ids": ["capstone.building_data_model#f1", "capstone.building_data_model#f2"],
                "teaching_block_ids": ["capstone.building_data_model#tb2", "capstone.building_data_model#tb3", "capstone.building_data_model#tb4"],
                "anchors": ["capstone.building_data_model#visual"]
            }
        }
    ],
    "reward": {"gems": 3},
    "lineage": step_lineage(
        ["capstone.building_data_model"],
        ["capstone.building_data_model#f1", "capstone.building_data_model#f2"],
        ["capstone.building_data_model#tb1", "capstone.building_data_model#tb2", "capstone.building_data_model#tb3"],
        anchors=["capstone.building_data_model#visual"]
    )
}

# ── s17: explainer – building_data_model – prose only ────────────────────────
s17 = {
    "step_id": f"{T1}.s17",
    "type": "explainer",
    "concept_ids": ["capstone.building_data_model"],
    "eyebrow": "Data Modelling",
    "title": "Mapping the capstone tables onto the model",
    "lede": "Getting the primary key / foreign key pairing right connects the two tables correctly before any join or aggregation across them can be trusted.",
    "blocks": [
        prose(
            f"{T1}.s17.b1", "example",
            "In the capstone: Drivers has `driver_id` as its primary key, uniquely identifying each driver row. "
            "Orders has its own primary key, `order_id`, plus a `driver_id` column that is a foreign key — its values must match a `driver_id` that already exists in Drivers. "
            "Since one driver delivers many orders, this is a one-to-many relationship: one row on the Drivers ('one') side relates to many rows on the Orders ('many') side.",
            ["capstone.building_data_model"],
            ["capstone.building_data_model#f1", "capstone.building_data_model#f2"],
            ["capstone.building_data_model#tb4", "capstone.building_data_model#tb5"]
        )
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.building_data_model"],
        ["capstone.building_data_model#f1", "capstone.building_data_model#f2"],
        ["capstone.building_data_model#tb4"]
    )
}

# ── s18: check – building_data_model ─────────────────────────────────────────
s18 = {
    "step_id": f"{T1}.s18",
    "type": "check",
    "concept_ids": ["capstone.building_data_model"],
    "eyebrow": "Quick check",
    "title": "Identifying primary and foreign keys in the capstone tables",
    "lede": "Test your understanding of which columns are primary keys and which are foreign keys in the capstone's two tables.",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.building_data_model"],
        ["capstone.building_data_model#f1", "capstone.building_data_model#f2"],
        tb_ids=[],
        anchors=["capstone.building_data_model#assessment:build_capstone_data_model_with_correct_keys_and_relationships"]
    )
}

# ── s19: hands_on – building_data_model ──────────────────────────────────────
s19 = {
    "step_id": f"{T1}.s19",
    "type": "hands_on",
    "concept_ids": ["capstone.building_data_model"],
    "eyebrow": "Hands-on practice",
    "title": "Match columns to their roles in the capstone data model",
    "lede": "Match each column from the Drivers and Orders tables to its role: primary key of Drivers, primary key of Orders, or foreign key in Orders referencing Drivers. Then identify which table is on the 'one' side and which is on the 'many' side.",
    "reward": {"gems": 4, "first_try_bonus": 2},
    "lineage": step_lineage(
        ["capstone.building_data_model"],
        ["capstone.building_data_model#f1", "capstone.building_data_model#f2"],
        tb_ids=[],
        anchors=[
            "capstone.building_data_model#practice",
            "capstone.building_data_model#assessment:identify_primary_and_foreign_keys_in_capstone_tables",
            "capstone.building_data_model#assessment:identify_one_to_many_relationship_between_drivers_and_orders"
        ]
    )
}

# ── s20: recap – all four concepts ───────────────────────────────────────────
s20 = {
    "step_id": f"{T1}.s20",
    "type": "recap",
    "concept_ids": [
        "capstone.integrate_sql",
        "capstone.integrate_spreadsheet",
        "capstone.integrate_python_pandas",
        "capstone.building_data_model"
    ],
    "eyebrow": "Tile recap",
    "title": "What you've built so far",
    "lede": "You've connected all four tools to the capstone project: SQL retrieves the data, spreadsheets summarise it, pandas cleans and aggregates it, and the data model links the two tables correctly.",
    "blocks": [
        prose(
            f"{T1}.s20.b1", "takeaway",
            "A single SELECT statement combines JOIN, WHERE, and GROUP BY to retrieve last quarter's QuickRide orders by zone. "
            "A PivotTable and COUNTIFS on the delivery sheet summarise zone-by-shift performance. "
            "isna()/dropna() and groupby().mean() clean and aggregate the orders in pandas. "
            "Drivers.driver_id (PK) links to Orders.driver_id (FK) in a one-to-many relationship — the same patterns already learned, applied to this project's own data.",
            ["capstone.integrate_sql", "capstone.integrate_spreadsheet",
             "capstone.integrate_python_pandas", "capstone.building_data_model"],
            [
                "capstone.integrate_sql#f1", "capstone.integrate_sql#f2",
                "capstone.integrate_spreadsheet#f1", "capstone.integrate_spreadsheet#f2",
                "capstone.integrate_python_pandas#f1", "capstone.integrate_python_pandas#f2",
                "capstone.building_data_model#f1", "capstone.building_data_model#f2"
            ],
            [
                "capstone.integrate_sql#tb5",
                "capstone.integrate_spreadsheet#tb5",
                "capstone.integrate_python_pandas#tb5",
                "capstone.building_data_model#tb5"
            ]
        ),
        {
            "type": "up_next",
            "block_id": f"{T1}.s20.b2",
            "title": "Up next: Descriptive statistics on the capstone data",
            "text": "In the next tile you'll run describe() on the cleaned delivery_time column and decide whether the mean or the median better answers the business question."
        }
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.integrate_sql", "capstone.integrate_spreadsheet",
         "capstone.integrate_python_pandas", "capstone.building_data_model"],
        [
            "capstone.integrate_sql#f1", "capstone.integrate_sql#f2",
            "capstone.integrate_spreadsheet#f1", "capstone.integrate_spreadsheet#f2",
            "capstone.integrate_python_pandas#f1", "capstone.integrate_python_pandas#f2",
            "capstone.building_data_model#f1", "capstone.building_data_model#f2"
        ],
        [
            "capstone.integrate_sql#tb5",
            "capstone.integrate_spreadsheet#tb5",
            "capstone.integrate_python_pandas#tb5",
            "capstone.building_data_model#tb5"
        ]
    )
}

# ── Remediation steps for tile 1 ─────────────────────────────────────────────

# r01: for s04 (check on integrate_sql#f2 — INNER JOIN in FROM clause)
r01 = {
    "step_id": f"{T1}.r01",
    "type": "remediation",
    "concept_ids": ["capstone.integrate_sql"],
    "eyebrow": "Let's review",
    "title": "Where does the INNER JOIN go in a SELECT statement?",
    "lede": "The check asked where an INNER JOIN fits inside a SELECT. Here's the key rule.",
    "blocks": [
        prose(
            f"{T1}.r01.b1", "mechanism",
            "An INNER JOIN is placed in the **FROM clause** of a SELECT statement — not in WHERE or GROUP BY. "
            "The FROM clause (including any JOINs) runs first, combining matching rows from both tables. "
            "The WHERE clause then filters those combined rows, and GROUP BY groups what remains. "
            "In the capstone query, `FROM orders o INNER JOIN drivers d ON o.driver_id = d.driver_id` combines the two tables before any filtering or grouping.",
            ["capstone.integrate_sql"],
            ["capstone.integrate_sql#f2"],
            ["capstone.integrate_sql#tb3", "capstone.integrate_sql#tb4"]
        ),
        prose(
            f"{T1}.r01.b2", "misconception",
            "A common mistake is placing the JOIN condition in the WHERE clause (e.g. `WHERE o.driver_id = d.driver_id`). "
            "While some databases accept this older syntax, the standard and clearer approach is `INNER JOIN … ON` in the FROM clause, "
            "which makes the join explicit and keeps the WHERE clause for row filtering only.",
            ["capstone.integrate_sql"],
            ["capstone.integrate_sql#f2"],
            ["capstone.integrate_sql#tb3"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.integrate_sql"],
        ["capstone.integrate_sql#f2"],
        ["capstone.integrate_sql#tb3", "capstone.integrate_sql#tb4"]
    )
}

# r02: for s09 (check on integrate_spreadsheet#f2 — COUNTIFS)
r02 = {
    "step_id": f"{T1}.r02",
    "type": "remediation",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Let's review",
    "title": "How COUNTIFS applies multiple criteria",
    "lede": "The check asked how COUNTIFS handles more than one criterion. Here's the key rule.",
    "blocks": [
        prose(
            f"{T1}.r02.b1", "mechanism",
            "COUNTIFS(criteria_range1, criteria1, criteria_range2, criteria2) counts only the rows where **all** criteria are met simultaneously. "
            "Each criteria_range/criteria pair is evaluated independently, and only rows that pass every pair are counted. "
            "In the capstone, `COUNTIFS(zone_range, \"Ikeja\", delivery_time_range, \">45\")` counts rows where the zone is Ikeja **and** the delivery time exceeds 45 minutes — both conditions must hold.",
            ["capstone.integrate_spreadsheet"],
            ["capstone.integrate_spreadsheet#f2"],
            ["capstone.integrate_spreadsheet#tb3", "capstone.integrate_spreadsheet#tb4"]
        ),
        prose(
            f"{T1}.r02.b2", "misconception",
            "COUNTIFS is not the same as two separate COUNTIF calls added together. "
            "Adding two COUNTIF results would count rows that meet either criterion, not both. "
            "COUNTIFS enforces all criteria at once, so the count is always ≤ the count from any single criterion alone.",
            ["capstone.integrate_spreadsheet"],
            ["capstone.integrate_spreadsheet#f2"],
            ["capstone.integrate_spreadsheet#tb3"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f2"],
        ["capstone.integrate_spreadsheet#tb3", "capstone.integrate_spreadsheet#tb4"]
    )
}

# r03: for s10 (check on integrate_spreadsheet#f1 — PivotTable field placement)
r03 = {
    "step_id": f"{T1}.r03",
    "type": "remediation",
    "concept_ids": ["capstone.integrate_spreadsheet"],
    "eyebrow": "Let's review",
    "title": "How fields are placed when you insert a PivotTable",
    "lede": "The check asked about default field placement in a PivotTable. Here's the rule.",
    "blocks": [
        prose(
            f"{T1}.r03.b1", "mechanism",
            "When you add a field to a PivotTable, the tool places it based on its data type: **non-numeric fields** (like zone and shift) default to Rows, **date/time fields** default to Columns, and **numeric fields** (like delivery_time) default to Values. "
            "You can drag any field between Rows, Columns, Values, and Filters to rearrange the summary. "
            "In the capstone, dragging `shift` from Rows to Columns turns the layout into a zone-by-shift grid.",
            ["capstone.integrate_spreadsheet"],
            ["capstone.integrate_spreadsheet#f1"],
            ["capstone.integrate_spreadsheet#tb2", "capstone.integrate_spreadsheet#tb4"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.integrate_spreadsheet"],
        ["capstone.integrate_spreadsheet#f1"],
        ["capstone.integrate_spreadsheet#tb2", "capstone.integrate_spreadsheet#tb4"]
    )
}

# r04: for s14 (check on integrate_python_pandas#f1 — isna/dropna/fillna)
r04 = {
    "step_id": f"{T1}.r04",
    "type": "remediation",
    "concept_ids": ["capstone.integrate_python_pandas"],
    "eyebrow": "Let's review",
    "title": "Detecting and handling missing values with isna(), dropna(), and fillna()",
    "lede": "The check asked about isna(), dropna(), and fillna(). Here's how they work together.",
    "blocks": [
        prose(
            f"{T1}.r04.b1", "mechanism",
            "isna() returns a boolean mask showing which values in a DataFrame or Series are missing (NaN). "
            "dropna() removes rows (or columns) that contain at least one missing value. "
            "fillna(value) replaces missing values with the specified value instead of removing the row. "
            "In the capstone, `orders['delivery_time'].isna()` identifies which orders have no recorded delivery time; "
            "dropna() then removes those rows before the groupby aggregation runs.",
            ["capstone.integrate_python_pandas"],
            ["capstone.integrate_python_pandas#f1"],
            ["capstone.integrate_python_pandas#tb2", "capstone.integrate_python_pandas#tb4"]
        ),
        prose(
            f"{T1}.r04.b2", "misconception",
            "isna() only **detects** missing values — it does not remove or replace them. "
            "You need dropna() or fillna() to actually change the DataFrame. "
            "Calling isna() alone and then running groupby() will still include NaN rows in the aggregation.",
            ["capstone.integrate_python_pandas"],
            ["capstone.integrate_python_pandas#f1"],
            ["capstone.integrate_python_pandas#tb2"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.integrate_python_pandas"],
        ["capstone.integrate_python_pandas#f1"],
        ["capstone.integrate_python_pandas#tb2", "capstone.integrate_python_pandas#tb4"]
    )
}

# r05: for s18 (check on building_data_model — keys and relationships)
r05 = {
    "step_id": f"{T1}.r05",
    "type": "remediation",
    "concept_ids": ["capstone.building_data_model"],
    "eyebrow": "Let's review",
    "title": "Primary keys, foreign keys, and the one-to-many relationship",
    "lede": "The check asked about the capstone's data model. Here's the key contrast.",
    "blocks": [
        prose(
            f"{T1}.r05.b1", "mechanism",
            "A **primary key** uniquely identifies each row of its table — no two rows can share the same primary key value. "
            "A **foreign key** is a column whose values must match a primary key value in another table. "
            "In the capstone: `driver_id` is the primary key of Drivers (each driver has a unique ID); "
            "`driver_id` in Orders is a foreign key — its values must match a `driver_id` that already exists in Drivers.",
            ["capstone.building_data_model"],
            ["capstone.building_data_model#f1"],
            ["capstone.building_data_model#tb2", "capstone.building_data_model#tb4"]
        ),
        prose(
            f"{T1}.r05.b2", "mechanism",
            "In a **one-to-many** relationship, one row on the 'one' side relates to many rows on the 'many' side. "
            "The foreign key is placed on the 'many' side. "
            "In the capstone, one driver (Drivers table, 'one' side) can appear in many orders (Orders table, 'many' side), "
            "so `driver_id` as a foreign key sits in the Orders table — the same pattern as CustID sitting in the Order table.",
            ["capstone.building_data_model"],
            ["capstone.building_data_model#f2"],
            ["capstone.building_data_model#tb3", "capstone.building_data_model#tb4"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.building_data_model"],
        ["capstone.building_data_model#f1", "capstone.building_data_model#f2"],
        ["capstone.building_data_model#tb2", "capstone.building_data_model#tb3", "capstone.building_data_model#tb4"]
    )
}

tile1 = {
    "tile_id": T1,
    "title": "Integrating SQL, Spreadsheets, and pandas",
    "summary": "Apply already-learned SQL, spreadsheet, and pandas skills to the QuickRide capstone project: retrieve last quarter's orders with a multi-clause SELECT, summarise the delivery sheet with a PivotTable and COUNTIFS, clean and aggregate orders in pandas, and model the two-table relationship with correct primary and foreign keys.",
    "steps": [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20],
    "remediation_steps": [r01, r02, r03, r04, r05]
}

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 2: tile_capstone_stats_dashboard
# ═══════════════════════════════════════════════════════════════════════════════

T2 = "tile_capstone_stats_dashboard"

# ── s01: explainer – applying_descriptive_statistics – data_table visual ─────
t2_s01 = {
    "step_id": f"{T2}.s01",
    "type": "explainer",
    "concept_ids": ["capstone.applying_descriptive_statistics"],
    "eyebrow": "Descriptive Statistics",
    "title": "Running describe() on the capstone delivery data",
    "lede": "With cleaned, modelled data, the business question needs actual numbers: how late are deliveries, by zone? describe() gives the full summary in one call.",
    "blocks": [
        heading(f"{T2}.s01.b1", "Getting the summary statistics"),
        prose(
            f"{T2}.s01.b2", "mechanism",
            "describe() computes a variety of summary statistics about a Series or the columns of a DataFrame — count, mean, std, min, quartiles, and max. "
            "In the capstone, running describe() on a zone's `delivery_time` column returns that full summary in one call, without writing separate mean() or std() calls.",
            ["capstone.applying_descriptive_statistics"],
            ["capstone.applying_descriptive_statistics#f1"],
            ["capstone.applying_descriptive_statistics#tb2"]
        ),
        prose(
            f"{T2}.s01.b3", "mechanism",
            "The mean is more strongly affected by extreme observations than the median, which is more robust to them. "
            "When the goal is to understand a typical individual value in a skewed dataset, the median can be more useful. "
            "In the capstone, a handful of unusually long deliveries in a zone can pull the mean upward while the median stays closer to the typical delivery.",
            ["capstone.applying_descriptive_statistics"],
            ["capstone.applying_descriptive_statistics#f2"],
            ["capstone.applying_descriptive_statistics#tb3"]
        ),
        {
            "type": "data_table",
            "block_id": f"{T2}.s01.b4",
            "result_of": {
                "runtime": "sql",
                "sql": (
                    "SELECT 'count' AS statistic, CAST(COUNT(delivery_time) AS DOUBLE) AS value FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL "
                    "UNION ALL SELECT 'mean', ROUND(AVG(CAST(delivery_time AS DOUBLE)), 1) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL "
                    "UNION ALL SELECT 'median', MEDIAN(delivery_time) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL "
                    "UNION ALL SELECT 'min', MIN(delivery_time) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL "
                    "UNION ALL SELECT 'max', MAX(delivery_time) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL"
                ),
                "asset_mounts": [{"asset_id": "ds_capstone_orders", "mount_path": "ds_capstone_orders"}]
            },
            "caption": "describe() output for Ikeja delivery_time — mean is noticeably higher than median due to extreme observations",
            "highlight": [
                {"target": {"kind": "row", "row": {"where": {"statistic": "mean"}}},
                 "label": "mean — pulled up by extreme deliveries", "tone": "focus"},
                {"target": {"kind": "row", "row": {"where": {"statistic": "median"}}},
                 "label": "median — more robust to extremes", "tone": "good"}
            ],
            "lineage": {
                "concept_ids": ["capstone.applying_descriptive_statistics"],
                "fact_ids": ["capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2"],
                "teaching_block_ids": ["capstone.applying_descriptive_statistics#tb2", "capstone.applying_descriptive_statistics#tb3", "capstone.applying_descriptive_statistics#tb4"],
                "anchors": ["capstone.applying_descriptive_statistics#visual"]
            }
        }
    ],
    "reward": {"gems": 3},
    "lineage": step_lineage(
        ["capstone.applying_descriptive_statistics"],
        ["capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2"],
        ["capstone.applying_descriptive_statistics#tb1", "capstone.applying_descriptive_statistics#tb2", "capstone.applying_descriptive_statistics#tb3"],
        anchors=["capstone.applying_descriptive_statistics#visual"]
    )
}

# ── s02: explainer – applying_descriptive_statistics – prose only ─────────────
t2_s02 = {
    "step_id": f"{T2}.s02",
    "type": "explainer",
    "concept_ids": ["capstone.applying_descriptive_statistics"],
    "eyebrow": "Descriptive Statistics",
    "title": "Choosing mean or median for the business question",
    "lede": "describe() gives the full summary; deciding which statistic actually answers the business question depends on whether extreme values are skewing that particular column.",
    "blocks": [
        prose(
            f"{T2}.s02.b1", "example",
            "Running describe() on Ikeja's `delivery_time` column returns a mean of 52 minutes and a median of 38 minutes. "
            "A handful of deliveries in that zone took over three hours — a stalled vehicle, a wrong address — and the mean is pulled up by those extreme observations, while the median stays at 38 minutes.",
            ["capstone.applying_descriptive_statistics"],
            ["capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2"],
            ["capstone.applying_descriptive_statistics#tb4"]
        ),
        prose(
            f"{T2}.s02.b2", "mechanism",
            "The capstone's business question is which zones are missing the delivery-time target and by how much — which calls for judging a **typical** delivery against that target, not one skewed by a few rare extremes. "
            "So the median is the more useful number here. "
            "describe() gives both; the analyst's job is to choose the one that answers the question.",
            ["capstone.applying_descriptive_statistics"],
            ["capstone.applying_descriptive_statistics#f2"],
            ["capstone.applying_descriptive_statistics#tb4", "capstone.applying_descriptive_statistics#tb5"]
        )
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.applying_descriptive_statistics"],
        ["capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2"],
        ["capstone.applying_descriptive_statistics#tb4"]
    )
}

# ── s03: check – applying_descriptive_statistics ─────────────────────────────
t2_s03 = {
    "step_id": f"{T2}.s03",
    "type": "check",
    "concept_ids": ["capstone.applying_descriptive_statistics"],
    "eyebrow": "Quick check",
    "title": "Mean vs median for a skewed distribution",
    "lede": "Test your understanding of when to use the median instead of the mean.",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.applying_descriptive_statistics"],
        ["capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2"],
        tb_ids=[],
        anchors=["capstone.applying_descriptive_statistics#assessment:compute_and_interpret_descriptive_statistics_for_capstone_business_question"]
    )
}

# ── s04: hands_on – applying_descriptive_statistics ──────────────────────────
t2_s04 = {
    "step_id": f"{T2}.s04",
    "type": "hands_on",
    "concept_ids": ["capstone.applying_descriptive_statistics"],
    "eyebrow": "Hands-on practice",
    "title": "Call describe() and choose the right statistic",
    "lede": "Given a DataFrame with a delivery_time column for one zone, call describe() on that column, then compare the mean and median and state in a comment which better represents a typical delivery.",
    "reward": {"gems": 4, "first_try_bonus": 2},
    "lineage": step_lineage(
        ["capstone.applying_descriptive_statistics"],
        ["capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2"],
        tb_ids=[],
        anchors=[
            "capstone.applying_descriptive_statistics#practice",
            "capstone.applying_descriptive_statistics#assessment:apply_describe_to_capstone_series_or_dataframe_column",
            "capstone.applying_descriptive_statistics#assessment:select_mean_or_median_based_on_skew_and_business_question"
        ]
    )
}

# ── s05: explainer – building_dashboard_or_viz – code_walkthrough visual ──────
t2_s05 = {
    "step_id": f"{T2}.s05",
    "type": "explainer",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Dashboard & Visualisation",
    "title": "Two patterns for multi-panel figures in matplotlib",
    "lede": "The findings now need a visualisation set a stakeholder can look at. matplotlib offers two patterns for placing several charts in one figure.",
    "blocks": [
        heading(f"{T2}.s05.b1", "Pattern 1: plt.subplots(2, 2) — a 2×2 grid"),
        prose(
            f"{T2}.s05.b2", "mechanism",
            "`fig, axs = plt.subplots(2, 2)` creates one Figure containing a 2×2 grid of Axes, so several charts can share one figure. "
            "Each axes is addressed by its row and column index — `axs[0, 0]`, `axs[0, 1]`, `axs[1, 0]`, `axs[1, 1]` — and plotted independently. "
            "In the capstone, four related delivery charts share one figure instead of appearing as four separate figures.",
            ["capstone.building_dashboard_or_viz"],
            ["capstone.building_dashboard_or_viz#f1"],
            ["capstone.building_dashboard_or_viz#tb2"]
        ),
        heading(f"{T2}.s05.b3", "Pattern 2: plt.subplot(131/132/133) — a side-by-side row"),
        prose(
            f"{T2}.s05.b4", "mechanism",
            "`plt.subplot(131)`, `plt.subplot(132)`, and `plt.subplot(133)` each hold a different chart side by side in one figure, "
            "and `plt.suptitle()` adds one title over the whole figure. "
            "In the capstone, three delivery charts can sit side by side under one shared title instead of as three separate figures.",
            ["capstone.building_dashboard_or_viz"],
            ["capstone.building_dashboard_or_viz#f2"],
            ["capstone.building_dashboard_or_viz#tb3"]
        ),
        {
            "type": "code_walkthrough",
            "block_id": f"{T2}.s05.b5",
            "language": "python",
            "code": (
                "# Pattern 1: 2×2 grid\n"
                "fig, axs = plt.subplots(2, 2)\n"
                "axs[0, 0].bar(zones, avg_times)\n"
                "axs[0, 0].set_title('Avg delivery time by zone')\n"
                "axs[0, 1].bar(shifts, shift_avg)\n"
                "axs[0, 1].set_title('Avg delivery time by shift')\n"
                "axs[1, 0].bar(zones, order_counts)\n"
                "axs[1, 0].set_title('Order count by zone')\n"
                "axs[1, 1].hist(delivery_times, bins=10)\n"
                "axs[1, 1].set_title('Distribution of delivery times')\n"
                "plt.tight_layout()\n"
                "\n"
                "# Pattern 2: side-by-side row\n"
                "plt.subplot(131)\n"
                "plt.bar(zones, avg_times)\n"
                "plt.subplot(132)\n"
                "plt.bar(shifts, shift_avg)\n"
                "plt.subplot(133)\n"
                "plt.hist(delivery_times, bins=10)\n"
                "plt.suptitle('Delivery Performance -- Last Quarter')\n"
                "plt.tight_layout()"
            ),
            "annotations": [
                {"start_line": 1, "end_line": 11,
                 "text": "Pattern 1: subplots(2, 2) returns a 2-D array of axes; address each by [row, col]."},
                {"start_line": 13, "end_line": 21,
                 "text": "Pattern 2: subplot(1, 3, n) places charts side by side; suptitle() adds one shared title."}
            ],
            "reveal": "all",
            "lineage": {
                "concept_ids": ["capstone.building_dashboard_or_viz"],
                "fact_ids": ["capstone.building_dashboard_or_viz#f1", "capstone.building_dashboard_or_viz#f2"],
                "teaching_block_ids": ["capstone.building_dashboard_or_viz#tb2", "capstone.building_dashboard_or_viz#tb3", "capstone.building_dashboard_or_viz#tb4"],
                "anchors": ["capstone.building_dashboard_or_viz#visual"]
            }
        }
    ],
    "reward": {"gems": 3},
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        ["capstone.building_dashboard_or_viz#f1", "capstone.building_dashboard_or_viz#f2"],
        ["capstone.building_dashboard_or_viz#tb1", "capstone.building_dashboard_or_viz#tb2", "capstone.building_dashboard_or_viz#tb3"],
        anchors=["capstone.building_dashboard_or_viz#visual"]
    )
}

# ── s06: explainer – building_dashboard_or_viz – prose only ──────────────────
t2_s06 = {
    "step_id": f"{T2}.s06",
    "type": "explainer",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Dashboard & Visualisation",
    "title": "Choosing a layout for the capstone figure",
    "lede": "Either layout turns several separate charts into one coherent figure the stakeholder summary can point to as a set.",
    "blocks": [
        prose(
            f"{T2}.s06.b1", "example",
            "For the capstone, `fig, axs = plt.subplots(2, 2)` lays out four related charts — delivery time by zone, delivery time by shift, order count by zone, and the distribution of delivery times — in one 2×2 figure. "
            "Alternatively, `plt.subplot(131)`, `plt.subplot(132)`, `plt.subplot(133)` place three of those charts side by side in a single row, "
            "and `plt.suptitle('Delivery Performance -- Last Quarter')` puts one title over all three.",
            ["capstone.building_dashboard_or_viz"],
            ["capstone.building_dashboard_or_viz#f1", "capstone.building_dashboard_or_viz#f2"],
            ["capstone.building_dashboard_or_viz#tb4", "capstone.building_dashboard_or_viz#tb5"]
        )
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        ["capstone.building_dashboard_or_viz#f1", "capstone.building_dashboard_or_viz#f2"],
        ["capstone.building_dashboard_or_viz#tb4"]
    )
}

# ── s07: video – building_dashboard_or_viz ───────────────────────────────────
t2_s07 = {
    "step_id": f"{T2}.s07",
    "type": "video",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Dashboard & Visualisation",
    "title": "Watch: arranging multiple charts in one figure with subplots",
    "lede": "This clip shows plt.subplots(2, 2) in action — each axes addressed by [row, col] and given its own title. Note: the clip uses toy curves, not delivery data, and does not cover plt.subplot(131)/plt.suptitle().",
    "blocks": [
        media_group(
            f"{T2}.s07.b1",
            "Arranging multiple charts in one figure with subplots",
            ["seg_capstone.building_dashboard_or_viz_KFMs_ZZNgmo_0_386"]
        )
    ],
    "reward": {"gems": 1},
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        ["capstone.building_dashboard_or_viz#f1"],
        seg_ids=["seg_capstone.building_dashboard_or_viz_KFMs_ZZNgmo_0_386"]
    )
}

# ── s08: check – building_dashboard_or_viz (2x2 grid) ────────────────────────
t2_s08 = {
    "step_id": f"{T2}.s08",
    "type": "check",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Quick check",
    "title": "Creating a 2×2 subplot grid",
    "lede": "Test your understanding of how plt.subplots(2, 2) creates and addresses a grid of axes.",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        ["capstone.building_dashboard_or_viz#f1"],
        tb_ids=[],
        anchors=["capstone.building_dashboard_or_viz#assessment:create_2x2_subplot_grid_with_subplots"]
    )
}

# ── s09: check – building_dashboard_or_viz (side-by-side + suptitle) ─────────
t2_s09 = {
    "step_id": f"{T2}.s09",
    "type": "check",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Quick check",
    "title": "Creating side-by-side subplots with a shared title",
    "lede": "Test your understanding of plt.subplot(131/132/133) and plt.suptitle().",
    "reward": {"gems": 2, "first_try_bonus": 1},
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        ["capstone.building_dashboard_or_viz#f2"],
        tb_ids=[],
        anchors=["capstone.building_dashboard_or_viz#assessment:create_side_by_side_subplots_with_suptitle"]
    )
}

# ── s10: hands_on – building_dashboard_or_viz ────────────────────────────────
t2_s10 = {
    "step_id": f"{T2}.s10",
    "type": "hands_on",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Hands-on practice",
    "title": "Build the capstone multi-panel figure",
    "lede": "Using the capstone delivery dataset, build a multi-panel figure that places at least three related charts together in one figure and adds a single shared title over all panels.",
    "reward": {"gems": 4, "first_try_bonus": 2},
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        [],
        tb_ids=[],
        anchors=[
            "capstone.building_dashboard_or_viz#practice",
            "capstone.building_dashboard_or_viz#assessment:select_appropriate_multi_panel_layout_for_capstone_findings"
        ]
    )
}

# ── s11: recap – both concepts ────────────────────────────────────────────────
t2_s11 = {
    "step_id": f"{T2}.s11",
    "type": "recap",
    "concept_ids": ["capstone.applying_descriptive_statistics", "capstone.building_dashboard_or_viz"],
    "eyebrow": "Tile recap",
    "title": "Statistics and visualisation: the capstone findings are ready",
    "lede": "You've computed the descriptive statistics that answer the business question and assembled them into a multi-panel figure the stakeholder summary can reference.",
    "blocks": [
        prose(
            f"{T2}.s11.b1", "takeaway",
            "describe() gives the full summary for a delivery_time column in one call; choosing between mean and median depends on whether extreme observations are skewing the data. "
            "For the capstone's business question — which zones miss the delivery target and by how much — the median is the more useful measure. "
            "Either `plt.subplots(2, 2)` or `plt.subplot(131/132/133)` + `plt.suptitle()` turns several separate charts into one coherent figure.",
            ["capstone.applying_descriptive_statistics", "capstone.building_dashboard_or_viz"],
            [
                "capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2",
                "capstone.building_dashboard_or_viz#f1", "capstone.building_dashboard_or_viz#f2"
            ],
            [
                "capstone.applying_descriptive_statistics#tb5",
                "capstone.building_dashboard_or_viz#tb5"
            ]
        ),
        {
            "type": "up_next",
            "block_id": f"{T2}.s11.b2",
            "title": "Up next: Independent execution and narrated delivery",
            "text": "In the next tile you'll execute the full capstone workflow independently — without step-by-step guidance — and produce a narrated stakeholder summary of your findings."
        }
    ],
    "reward": {"gems": 2},
    "lineage": step_lineage(
        ["capstone.applying_descriptive_statistics", "capstone.building_dashboard_or_viz"],
        [
            "capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2",
            "capstone.building_dashboard_or_viz#f1", "capstone.building_dashboard_or_viz#f2"
        ],
        [
            "capstone.applying_descriptive_statistics#tb5",
            "capstone.building_dashboard_or_viz#tb5"
        ]
    )
}

# ── Remediation steps for tile 2 ─────────────────────────────────────────────

# r01: for s03 (check on applying_descriptive_statistics — both f1 and f2)
t2_r01 = {
    "step_id": f"{T2}.r01",
    "type": "remediation",
    "concept_ids": ["capstone.applying_descriptive_statistics"],
    "eyebrow": "Let's review",
    "title": "describe() output and choosing mean vs median",
    "lede": "The check asked about interpreting describe() output and selecting the right statistic. Here's the key contrast.",
    "blocks": [
        prose(
            f"{T2}.r01.b1", "mechanism",
            "describe() computes count, mean, std, min, 25th percentile, 50th percentile (the median), 75th percentile, and max for a Series or DataFrame column. "
            "The 50% row in describe()'s output is the median. "
            "In the capstone, running describe() on Ikeja's `delivery_time` column returns a mean of 52 minutes and a median of 38 minutes.",
            ["capstone.applying_descriptive_statistics"],
            ["capstone.applying_descriptive_statistics#f1"],
            ["capstone.applying_descriptive_statistics#tb2", "capstone.applying_descriptive_statistics#tb4"]
        ),
        prose(
            f"{T2}.r01.b2", "mechanism",
            "The mean is pulled upward by extreme observations; the median is not. "
            "When a few deliveries took over three hours, the mean rises to 52 minutes even though most deliveries were around 38 minutes. "
            "For the business question — which zones miss the target and by how much — the median (38 minutes) better represents a typical delivery than the mean (52 minutes).",
            ["capstone.applying_descriptive_statistics"],
            ["capstone.applying_descriptive_statistics#f2"],
            ["capstone.applying_descriptive_statistics#tb3", "capstone.applying_descriptive_statistics#tb4"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.applying_descriptive_statistics"],
        ["capstone.applying_descriptive_statistics#f1", "capstone.applying_descriptive_statistics#f2"],
        ["capstone.applying_descriptive_statistics#tb2", "capstone.applying_descriptive_statistics#tb3", "capstone.applying_descriptive_statistics#tb4"]
    )
}

# r02: for s08 (check on building_dashboard_or_viz#f1 — 2x2 grid)
t2_r02 = {
    "step_id": f"{T2}.r02",
    "type": "remediation",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Let's review",
    "title": "How plt.subplots(2, 2) creates and addresses a grid of axes",
    "lede": "The check asked about the 2×2 subplot pattern. Here's how it works.",
    "blocks": [
        prose(
            f"{T2}.r02.b1", "mechanism",
            "`fig, axs = plt.subplots(2, 2)` returns one Figure and a 2-D NumPy array of four Axes objects. "
            "Each axes is addressed by its row and column index: `axs[0, 0]` is the top-left, `axs[0, 1]` is the top-right, `axs[1, 0]` is the bottom-left, and `axs[1, 1]` is the bottom-right. "
            "You call plotting methods on each axes independently — `axs[0, 0].bar(...)`, `axs[0, 1].hist(...)` — and `plt.tight_layout()` prevents the panels from overlapping.",
            ["capstone.building_dashboard_or_viz"],
            ["capstone.building_dashboard_or_viz#f1"],
            ["capstone.building_dashboard_or_viz#tb2", "capstone.building_dashboard_or_viz#tb4"]
        ),
        prose(
            f"{T2}.r02.b2", "misconception",
            "A common mistake is calling `plt.subplots(2, 2)` but then plotting with `plt.bar(...)` instead of `axs[row, col].bar(...)`. "
            "Using the global `plt` functions after subplots() plots into the last active axes, not the one you intend. "
            "Always address the specific axes object by index.",
            ["capstone.building_dashboard_or_viz"],
            ["capstone.building_dashboard_or_viz#f1"],
            ["capstone.building_dashboard_or_viz#tb2"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        ["capstone.building_dashboard_or_viz#f1"],
        ["capstone.building_dashboard_or_viz#tb2", "capstone.building_dashboard_or_viz#tb4"]
    )
}

# r03: for s09 (check on building_dashboard_or_viz#f2 — side-by-side + suptitle)
t2_r03 = {
    "step_id": f"{T2}.r03",
    "type": "remediation",
    "concept_ids": ["capstone.building_dashboard_or_viz"],
    "eyebrow": "Let's review",
    "title": "plt.subplot(131/132/133) and plt.suptitle()",
    "lede": "The check asked about the side-by-side subplot pattern. Here's how it works.",
    "blocks": [
        prose(
            f"{T2}.r03.b1", "mechanism",
            "`plt.subplot(131)` means: divide the figure into 1 row and 3 columns, and make the 1st panel active. "
            "`plt.subplot(132)` activates the 2nd panel, and `plt.subplot(133)` activates the 3rd. "
            "Each call makes that panel the current axes, so the next `plt.bar(...)` or `plt.hist(...)` call draws into it. "
            "`plt.suptitle('Delivery Performance -- Last Quarter')` then adds one title above all three panels.",
            ["capstone.building_dashboard_or_viz"],
            ["capstone.building_dashboard_or_viz#f2"],
            ["capstone.building_dashboard_or_viz#tb3", "capstone.building_dashboard_or_viz#tb4"]
        ),
        prose(
            f"{T2}.r03.b2", "misconception",
            "plt.title() sets the title of the **current** panel only. "
            "To add one title over the entire figure — above all panels — use plt.suptitle() instead. "
            "In the capstone, `plt.suptitle('Delivery Performance -- Last Quarter')` labels the whole three-panel figure, not just the last panel.",
            ["capstone.building_dashboard_or_viz"],
            ["capstone.building_dashboard_or_viz#f2"],
            ["capstone.building_dashboard_or_viz#tb3"]
        )
    ],
    "lineage": step_lineage(
        ["capstone.building_dashboard_or_viz"],
        ["capstone.building_dashboard_or_viz#f2"],
        ["capstone.building_dashboard_or_viz#tb3", "capstone.building_dashboard_or_viz#tb4"]
    )
}

tile2 = {
    "tile_id": T2,
    "title": "Descriptive Statistics and Dashboard",
    "summary": "Apply pandas describe() to the capstone delivery data, choose between mean and median based on skew and the business question, then build a multi-panel matplotlib figure using either plt.subplots(2, 2) or plt.subplot(131/132/133) + plt.suptitle().",
    "steps": [t2_s01, t2_s02, t2_s03, t2_s04, t2_s05, t2_s06, t2_s07, t2_s08, t2_s09, t2_s10, t2_s11],
    "remediation_steps": [t2_r01, t2_r02, t2_r03]
}

# ═══════════════════════════════════════════════════════════════════════════════
# Final output
# ═══════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "1.0.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_010_da_stats_capstone",
    "tiles": [tile1, tile2]
}

out_path = "batches/final_batch_010_da_stats_capstone/screens.part.c2.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written to {out_path}")
print(f"Tile 1 steps: {len(tile1['steps'])}, remediation: {len(tile1['remediation_steps'])}")
print(f"Tile 2 steps: {len(tile2['steps'])}, remediation: {len(tile2['remediation_steps'])}")
