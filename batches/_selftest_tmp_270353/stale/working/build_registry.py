"""
Build scenario_asset_registry.json for final_batch_011_da_spreadsheet.

The glossary's running example is a delivery-orders workbook with:
  - An Orders sheet (order_id, city, delivery_minutes, amount, status, order_date, driver_id)
  - A Drivers sheet (driver_id, driver_name)

All column names, table names, and values are taken directly from the glossary teaching blocks.
"""

import json, datetime

# ── helpers ──────────────────────────────────────────────────────────────────

def row(*vals):
    return list(vals)

# ── scenario ─────────────────────────────────────────────────────────────────

scenarios = [
    {
        "scenario_id": "scenario_delivery_orders",
        "name": "QuickDeliver — Weekly Orders Workbook",
        "summary": (
            "A fictional same-day delivery company, QuickDeliver, tracks one week of "
            "delivery orders in an Excel workbook. The workbook has two sheets: "
            "Orders (one row per delivery) and Drivers (one row per driver). "
            "Learners use this workbook to practise every spreadsheet concept in the path."
        ),
        "locale": "en-NG",
        "currency": "NGN",
        "domain": "logistics / delivery operations",
        "glossary_example_vocab": [
            # grid / cell references
            "workbook", "sheet", "Sheet1", "Sheet2", "Orders", "Drivers",
            "cell", "row", "column", "grid", "A1 reference style",
            "B2", "C2:C51", "A10:A20", "A10:E20", "H:H", "5:5",
            # formula syntax
            "=", "+", "-", "*", "/", "=SUM(D2:D51)", "=D3-D2",
            "=5+2*3", "=(5+2)*3", "operator precedence", "parentheses",
            # relative / absolute references
            "$A$1", "$H$1", "=D2*$H$1", "relative reference", "absolute reference",
            "mixed reference", "$A1", "A$1",
            # aggregation
            "SUM", "AVERAGE", "COUNT", "COUNTA",
            "=SUM(D2:D51)", "=AVERAGE(C2:C51)", "=COUNT(C2:C51)", "=COUNTA(C2:C51)",
            # logical
            "IF", "AND", "OR", "nested IF",
            '=IF(C2>60,"Late","On Time")',
            # text functions
            "TEXTJOIN", "CONCATENATE", "CONCAT",
            "LEFT", "RIGHT", "MID", "TRIM",
            "LG-2045", "=LEFT(A2,2)", "=RIGHT(A2,4)", "=MID(A2,4,4)",
            # date functions
            "TODAY", "DATEDIF", "serial number", "January 1 1900",
            '=DATEDIF(G2,TODAY(),"D")',
            # conditional aggregation
            "COUNTIF", "SUMIF", "COUNTIFS", "SUMIFS",
            '=COUNTIF(B2:B51,"Lagos")', '=SUMIF(B2:B51,"Lagos",D2:D51)',
            '=SUMIFS(D2:D51,B2:B51,"Lagos",E2:E51,"Delivered")',
            # lookups
            "VLOOKUP", "HLOOKUP", "XLOOKUP", "INDEX", "MATCH",
            "=VLOOKUP(F2,Drivers!A:B,2,FALSE)",
            "=XLOOKUP(F2,Drivers!A:A,Drivers!B:B)",
            "=INDEX(Drivers!A:A,MATCH(F2,Drivers!B:B,0))",
            # errors
            "#N/A", "#REF!", "#VALUE!",
            # tables / named ranges
            "Orders table", "DeptSales", "=SUM(Orders[Amount])",
            "structured reference", "DeliveryTimes", "Name Box",
            # sorting / filtering
            "Sort Smallest to Largest", "Sort Largest to Smallest",
            "Sort Oldest to Newest", "Sort Newest to Oldest",
            "AutoFilter", "Number Filters", "Text Filters", "Greater Than",
            # cleaning
            "Remove Duplicates", "Text to Columns", "Delimited", "Comma",
            "Lagos,Nigeria",
            # cross-sheet
            "Marketing!B1", "Drivers!B1", "'January Revenue'!A1",
            "[Budget.xlsx]Annual!C10:C25",
            # conditional formatting / data validation
            "Highlight Cells Rules", "Less Than",
            "Pending", "Delivered", "Cancelled",
            # pivot tables
            "PivotTable", "Rows area", "Columns area", "Values area", "Filters area",
            "City", "Status", "Amount",
            # charts
            "bar chart", "line chart", "pie chart",
            "Insert > Recommended Charts", "All Charts tab",
            # cities used in examples
            "Lagos",
        ]
    }
]

# ── dataset: orders (clean baseline) ─────────────────────────────────────────
# Columns match exactly what the glossary names:
#   order_id  (A) – glossary: "LG-2045" style IDs
#   city      (B) – glossary: Lagos, Abuja, Kano, Port Harcourt, Ibadan, Enugu (≤7 for pie chart)
#   delivery_minutes (C) – glossary: C2:C51, DeliveryTimes, =AVERAGE(C2:C51), IF(C2>60,"Late","On Time")
#   amount    (D) – glossary: =SUM(D2:D51), =SUM(Orders[Amount]), SUMIF/SUMIFS on D2:D51
#   status    (E) – glossary: Pending / Delivered / Cancelled (data-validation dropdown)
#   order_date    – glossary: G2 in =DATEDIF(G2,TODAY(),"D")
#   driver_id (F) – glossary: F2 in =VLOOKUP(F2,Drivers!A:B,2,FALSE)
#
# driver_id values are "D01"–"D05" — string identifiers, NOT numeric-looking labels
# (they have a letter prefix, so numeric_looking_label does not apply).
#
# 20 rows — enough for COUNT/COUNTA to differ, SUMIFS to be non-trivial,
# pivot to show multiple city×status combos, and charts to have ≥2 data points per series.

orders_columns = [
    {"name": "order_id",          "type": "string",  "semantic_role": "identifier",
     "description": "Unique order identifier in the format LG-NNNN"},
    {"name": "city",              "type": "string",  "semantic_role": "categorical",
     "description": "Delivery destination city"},
    {"name": "delivery_minutes",  "type": "integer", "semantic_role": "numerical",
     "unit": "minutes",
     "description": "Actual delivery time in minutes; null if not yet delivered"},
    {"name": "amount",            "type": "number",  "semantic_role": "numerical",
     "unit": "NGN",
     "description": "Order value in Nigerian Naira"},
    {"name": "status",            "type": "string",  "semantic_role": "categorical",
     "description": "Order status: Pending, Delivered, or Cancelled"},
    {"name": "order_date",        "type": "date",    "semantic_role": "datetime",
     "description": "Date the order was placed (YYYY-MM-DD)"},
    {"name": "driver_id",         "type": "string",  "semantic_role": "identifier",
     "description": "Driver identifier string (e.g. D01); used as a label, not a number"},
]

# 20 rows; delivery_minutes is null for Pending/Cancelled rows (COUNTA vs COUNT differ)
# Cities: Lagos(8), Abuja(4), Kano(3), Port Harcourt(2), Ibadan(2), Enugu(1) → 6 cities ≤7 for pie
# Statuses: Delivered(12), Pending(5), Cancelled(3)
orders_rows = [
    # order_id,    city,            del_min, amount,  status,       order_date,    driver_id
    ["LG-2001", "Lagos",            28,      4500.00, "Delivered",  "2024-03-04",  "D01"],
    ["LG-2002", "Abuja",            45,      7200.00, "Delivered",  "2024-03-04",  "D02"],
    ["LG-2003", "Lagos",            62,      3100.00, "Delivered",  "2024-03-05",  "D01"],
    ["LG-2004", "Kano",             None,    5800.00, "Pending",    "2024-03-05",  "D03"],
    ["LG-2005", "Lagos",            19,      2200.00, "Delivered",  "2024-03-05",  "D02"],
    ["LG-2006", "Port Harcourt",    55,      9100.00, "Delivered",  "2024-03-06",  "D04"],
    ["LG-2007", "Lagos",            None,    1800.00, "Cancelled",  "2024-03-06",  "D01"],
    ["LG-2008", "Abuja",            38,      6300.00, "Delivered",  "2024-03-06",  "D02"],
    ["LG-2009", "Lagos",            71,      4100.00, "Delivered",  "2024-03-07",  "D03"],
    ["LG-2010", "Kano",             None,    3700.00, "Pending",    "2024-03-07",  "D05"],
    ["LG-2011", "Lagos",            14,      2900.00, "Delivered",  "2024-03-07",  "D01"],
    ["LG-2012", "Ibadan",           42,      5500.00, "Delivered",  "2024-03-08",  "D04"],
    ["LG-2013", "Lagos",            None,    6800.00, "Pending",    "2024-03-08",  "D02"],
    ["LG-2014", "Abuja",            33,      4400.00, "Delivered",  "2024-03-08",  "D03"],
    ["LG-2015", "Lagos",            None,    2600.00, "Cancelled",  "2024-03-09",  "D05"],
    ["LG-2016", "Enugu",            58,      7700.00, "Delivered",  "2024-03-09",  "D04"],
    ["LG-2017", "Kano",             None,    3300.00, "Pending",    "2024-03-09",  "D01"],
    ["LG-2018", "Port Harcourt",    47,      8800.00, "Delivered",  "2024-03-10",  "D02"],
    ["LG-2019", "Ibadan",           None,    4200.00, "Cancelled",  "2024-03-10",  "D03"],
    ["LG-2020", "Abuja",            29,      5100.00, "Delivered",  "2024-03-10",  "D05"],
]

# Verify row widths
assert all(len(r) == len(orders_columns) for r in orders_rows), "Row width mismatch in orders_rows"

# ── dataset: drivers (VLOOKUP layout) ────────────────────────────────────────
# Columns: driver_id (A in Drivers sheet), driver_name (B in Drivers sheet)
# Glossary: =VLOOKUP(F2,Drivers!A:B,2,FALSE)  → driver_id in col A, driver_name in col B
#           =XLOOKUP(F2,Drivers!A:A,Drivers!B:B)

drivers_columns = [
    {"name": "driver_id",   "type": "string", "semantic_role": "identifier",
     "description": "Driver identifier string (e.g. D01); used as a label, not a number"},
    {"name": "driver_name", "type": "string", "semantic_role": "text",
     "description": "Full name of the driver"},
]

drivers_rows = [
    ["D01", "Amara Okafor"],
    ["D02", "Bello Musa"],
    ["D03", "Chisom Eze"],
    ["D04", "Damilola Adeyemi"],
    ["D05", "Emeka Nwosu"],
]

assert all(len(r) == len(drivers_columns) for r in drivers_rows), "Row width mismatch in drivers_rows"

# ── dataset: monthly_summary (for line chart) ─────────────────────────────────
# Glossary: "A summary of total order amount by month is exactly this kind of
#            evenly-spaced, time-ordered data."
monthly_columns = [
    {"name": "month_label",   "type": "string", "semantic_role": "categorical",
     "description": "Month label (e.g. Jan-2024)"},
    {"name": "total_amount",  "type": "number",  "semantic_role": "numerical",
     "unit": "NGN",
     "description": "Total order amount for the month"},
]

monthly_rows = [
    ["Jan-2024", 312000.00],
    ["Feb-2024", 287500.00],
    ["Mar-2024", 341200.00],
    ["Apr-2024", 298700.00],
    ["May-2024", 375400.00],
    ["Jun-2024", 362100.00],
]

assert all(len(r) == len(monthly_columns) for r in monthly_rows), "Row width mismatch in monthly_rows"

# ── dataset: city_totals (for bar chart and pie chart) ────────────────────────
# Glossary: "A summary table of total order amount by city is exactly the kind of
#            category-versus-value data a bar chart compares."
# Also: "A summary of total order amount by city, for no more than seven cities"
city_totals_columns = [
    {"name": "city",         "type": "string", "semantic_role": "categorical",
     "description": "Delivery destination city"},
    {"name": "total_amount", "type": "number",  "semantic_role": "numerical",
     "unit": "NGN",
     "description": "Total order amount for the city"},
]

city_totals_rows = [
    ["Lagos",         28200.00],
    ["Abuja",         23000.00],
    ["Kano",          12800.00],
    ["Port Harcourt", 17900.00],
    ["Ibadan",         9700.00],
    ["Enugu",          7700.00],
]

assert all(len(r) == len(city_totals_columns) for r in city_totals_rows), "Row width mismatch in city_totals_rows"

# ── variant: orders_messy ─────────────────────────────────────────────────────
# Planted issues:
#  1. duplicate_row  — LG-2005 appears twice
#  2. inconsistent_category — status "delivered" (lowercase) in one row
#  3. impossible_value — delivery_minutes = -5 (negative, violates ≥0 rule)
#  4. wrong_type — amount cell contains text "N/A" instead of a number
#
# For issue 4 (wrong_type), we use rule op "eq" with value "N/A" to verify the
# set_cell op placed the string "N/A" in the amount column.

orders_messy_ops = [
    # Op 1: duplicate row — copy row where order_id=LG-2005
    {
        "op": "duplicate_row",
        "where": {"order_id": "LG-2005"},
        "occurrence": 0
    },
    # Op 2: inconsistent category — set status of LG-2009 to lowercase "delivered"
    {
        "op": "set_cell",
        "where": {"order_id": "LG-2009"},
        "occurrence": 0,
        "column": "status",
        "value": "delivered"
    },
    # Op 3: impossible value — set delivery_minutes of LG-2011 to -5
    {
        "op": "set_cell",
        "where": {"order_id": "LG-2011"},
        "occurrence": 0,
        "column": "delivery_minutes",
        "value": -5
    },
    # Op 4: wrong type — set amount of LG-2016 to text "N/A"
    {
        "op": "set_cell",
        "where": {"order_id": "LG-2016"},
        "occurrence": 0,
        "column": "amount",
        "value": "N/A"
    },
]

orders_messy_planted = [
    {
        "issue_id": "issue_dup_LG2005",
        "kind": "duplicate_row",
        "locations": [
            {"where": {"order_id": "LG-2005"}, "occurrence": 0, "column": "order_id"},
            {"where": {"order_id": "LG-2005"}, "occurrence": 1, "column": "order_id"},
        ],
        "description": "Order LG-2005 appears twice; the second row is a duplicate entry."
    },
    {
        "issue_id": "issue_case_status_LG2009",
        "kind": "inconsistent_category",
        "locations": [
            {"where": {"order_id": "LG-2009"}, "occurrence": 0, "column": "status"}
        ],
        "description": "Status value 'delivered' uses lowercase; all other rows use 'Delivered'.",
        "rule": {"column": "status", "op": "casing_differs_from_siblings"}
    },
    {
        "issue_id": "issue_neg_delivery_LG2011",
        "kind": "impossible_value",
        "locations": [
            {"where": {"order_id": "LG-2011"}, "occurrence": 0, "column": "delivery_minutes"}
        ],
        "description": "delivery_minutes is -5, which is impossible for a delivery time.",
        "rule": {"column": "delivery_minutes", "op": "lt", "value": 0}
    },
    {
        "issue_id": "issue_wrong_type_amount_LG2016",
        "kind": "wrong_type",
        "locations": [
            {"where": {"order_id": "LG-2016"}, "occurrence": 0, "column": "amount"}
        ],
        "description": "amount contains text 'N/A' instead of a numeric value.",
        "rule": {"column": "amount", "op": "eq", "value": "N/A"}
    },
]

# ── assemble registry ─────────────────────────────────────────────────────────

registry = {
    "schema_version": "0.1.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "scenarios": scenarios,
    "assets": [
        # ── 1. Orders (clean) ──────────────────────────────────────────────
        {
            "asset_id": "asset_orders_clean",
            "asset_kind": "dataset",
            "scenario_id": "scenario_delivery_orders",
            "title": "Orders — clean baseline (20 rows)",
            "description": (
                "One row per delivery order. Used for formula syntax, aggregation, "
                "logical functions, conditional aggregation, lookups, sorting, filtering, "
                "tables, named ranges, pivot tables, and chart exercises. "
                "delivery_minutes is NULL for Pending/Cancelled rows so COUNT and COUNTA differ."
            ),
            "columns": orders_columns,
            "rows": orders_rows,
            "provenance": "authored",
            "variants": [
                {
                    "variant_id": "asset_orders_messy",
                    "derived_from": "asset_orders_clean",
                    "purpose": (
                        "Messy version for data-cleaning exercises: contains a duplicate row, "
                        "an inconsistent-category value, an impossible delivery time, "
                        "and a wrong-type amount cell."
                    ),
                    "ops": orders_messy_ops,
                    "planted_issues": orders_messy_planted,
                }
            ]
        },

        # ── 2. Drivers (VLOOKUP layout: driver_id col A, driver_name col B) ──
        {
            "asset_id": "asset_drivers_vlookup",
            "asset_kind": "dataset",
            "scenario_id": "scenario_delivery_orders",
            "title": "Drivers — VLOOKUP layout (driver_id left, driver_name right)",
            "description": (
                "Driver reference table with driver_id in the leftmost column and "
                "driver_name in the second column. Supports "
                "=VLOOKUP(F2,Drivers!A:B,2,FALSE) and "
                "=XLOOKUP(F2,Drivers!A:A,Drivers!B:B) exercises."
            ),
            "columns": drivers_columns,
            "rows": drivers_rows,
            "provenance": "authored",
        },

        # ── 3. Drivers (INDEX/MATCH layout: driver_name col A, driver_id col B) ──
        {
            "asset_id": "asset_drivers_index_match",
            "asset_kind": "dataset",
            "scenario_id": "scenario_delivery_orders",
            "title": "Drivers — INDEX/MATCH layout (driver_name left, driver_id right)",
            "description": (
                "Driver reference table with driver_name in column A and driver_id in "
                "column B — the reversed layout that VLOOKUP cannot handle. "
                "Supports =INDEX(Drivers!A:A,MATCH(F2,Drivers!B:B,0)) exercises."
            ),
            "columns": [
                {"name": "driver_name", "type": "string", "semantic_role": "text",
                 "description": "Full name of the driver"},
                {"name": "driver_id",   "type": "string", "semantic_role": "identifier",
                 "description": "Driver identifier string (e.g. D01); used as a label, not a number"},
            ],
            "rows": [
                ["Amara Okafor",    "D01"],
                ["Bello Musa",      "D02"],
                ["Chisom Eze",      "D03"],
                ["Damilola Adeyemi","D04"],
                ["Emeka Nwosu",     "D05"],
            ],
            "provenance": "authored",
        },

        # ── 4. Monthly summary (line chart) ───────────────────────────────
        {
            "asset_id": "asset_monthly_summary",
            "asset_kind": "dataset",
            "scenario_id": "scenario_delivery_orders",
            "title": "Monthly order totals — line chart source",
            "description": (
                "Aggregated total order amount by month. Used for line-chart exercises "
                "where evenly-spaced time-ordered data is required."
            ),
            "columns": monthly_columns,
            "rows": monthly_rows,
            "provenance": "authored",
        },

        # ── 5. City totals (bar chart + pie chart) ────────────────────────
        {
            "asset_id": "asset_city_totals",
            "asset_kind": "dataset",
            "scenario_id": "scenario_delivery_orders",
            "title": "City order totals — bar and pie chart source",
            "description": (
                "Aggregated total order amount by city (6 cities, all amounts positive). "
                "Used for bar-chart and pie-chart exercises. 6 categories and no negative "
                "values satisfy the pie-chart eligibility conditions from the glossary."
            ),
            "columns": city_totals_columns,
            "rows": city_totals_rows,
            "provenance": "authored",
        },

        # ── 6. Orders with text-to-columns raw data ───────────────────────
        # Glossary: "Lagos,Nigeria" as one text value → split with Text to Columns
        {
            "asset_id": "asset_orders_location_combined",
            "asset_kind": "dataset",
            "scenario_id": "scenario_delivery_orders",
            "title": "Orders — location column combined (Text to Columns exercise)",
            "description": (
                "Orders table where city and country are stored as a single "
                "'city,country' string (e.g. 'Lagos,Nigeria'). Used for the "
                "Text to Columns exercise."
            ),
            "columns": [
                {"name": "order_id",        "type": "string",  "semantic_role": "identifier",
                 "description": "Unique order identifier"},
                {"name": "location",        "type": "string",  "semantic_role": "text",
                 "description": "City and country combined as 'city,country'"},
                {"name": "delivery_minutes","type": "integer", "semantic_role": "numerical",
                 "unit": "minutes", "description": "Delivery time in minutes"},
                {"name": "amount",          "type": "number",  "semantic_role": "numerical",
                 "unit": "NGN", "description": "Order value in NGN"},
                {"name": "status",          "type": "string",  "semantic_role": "categorical",
                 "description": "Order status"},
                {"name": "order_date",      "type": "date",    "semantic_role": "datetime",
                 "description": "Date the order was placed"},
                {"name": "driver_id",       "type": "string",  "semantic_role": "identifier",
                 "description": "Driver identifier string"},
            ],
            "rows": [
                ["LG-2001", "Lagos,Nigeria",         28,   4500.00, "Delivered", "2024-03-04", "D01"],
                ["LG-2002", "Abuja,Nigeria",          45,   7200.00, "Delivered", "2024-03-04", "D02"],
                ["LG-2003", "Lagos,Nigeria",          62,   3100.00, "Delivered", "2024-03-05", "D01"],
                ["LG-2004", "Kano,Nigeria",           None, 5800.00, "Pending",   "2024-03-05", "D03"],
                ["LG-2005", "Lagos,Nigeria",          19,   2200.00, "Delivered", "2024-03-05", "D02"],
                ["LG-2006", "Port Harcourt,Nigeria",  55,   9100.00, "Delivered", "2024-03-06", "D04"],
                ["LG-2007", "Lagos,Nigeria",          None, 1800.00, "Cancelled", "2024-03-06", "D01"],
                ["LG-2008", "Abuja,Nigeria",          38,   6300.00, "Delivered", "2024-03-06", "D02"],
            ],
            "provenance": "authored",
        },
    ],
    "provenance": {
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
}

# ── final row-width check ─────────────────────────────────────────────────────
for asset in registry["assets"]:
    if asset["asset_kind"] != "dataset":
        continue
    ncols = len(asset["columns"])
    for i, r in enumerate(asset.get("rows", [])):
        assert len(r) == ncols, (
            f"Asset {asset['asset_id']} row {i}: expected {ncols} cells, got {len(r)}"
        )
    # check variant set_cell ops reference valid columns
    for v in asset.get("variants", []):
        col_names = [c["name"] for c in asset["columns"]]
        for op in v.get("ops", []):
            if op["op"] == "set_cell":
                assert op["column"] in col_names, (
                    f"set_cell column '{op['column']}' not in {asset['asset_id']} columns"
                )

print("All assertions passed.")

out_path = "batches/final_batch_011_da_spreadsheet/scenario_asset_registry.json"
with open(out_path, "w") as f:
    json.dump(registry, f, indent=2)
print(f"Written: {out_path}")
print(f"Scenarios: {len(registry['scenarios'])}")
print(f"Assets: {len(registry['assets'])}")
for a in registry['assets']:
    kind = a['asset_kind']
    aid = a['asset_id']
    if kind == 'dataset':
        nrows = len(a.get('rows', []))
        nvars = len(a.get('variants', []))
        print(f"  {aid}: {len(a['columns'])} cols, {nrows} rows, {nvars} variants")
    else:
        print(f"  {aid}: {kind}")
