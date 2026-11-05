"""
Build scenario_asset_registry.json for final_batch_010_da_stats_capstone.
Run from pack root: python3 batches/final_batch_010_da_stats_capstone/working/build_registry.py
"""

import json
import datetime
import pathlib

OUT = pathlib.Path("batches/final_batch_010_da_stats_capstone/scenario_asset_registry.json")

# ─────────────────────────────────────────────────────────────────────────────
# SCENARIOS
# ─────────────────────────────────────────────────────────────────────────────
scenarios = [
    {
        "scenario_id": "scen_delivery_stats",
        "name": "QuickRide Delivery — Descriptive Statistics",
        "summary": (
            "QuickRide is a fictional last-mile delivery company operating in Lagos, Nigeria. "
            "An analyst characterises delivery-time performance across four city zones "
            "(Ikeja, Lekki, Surulere, Yaba) and three driver shifts (morning, afternoon, evening). "
            "The scenario supplies the seven-order batch from the teaching blocks "
            "(18, 20, 22, 22, 26, 28, 80 minutes) and a larger per-order table for hands-on work."
        ),
        "locale": "en-NG",
        "currency": "NGN",
        "domain": "logistics / delivery",
        "glossary_example_vocab": [
            "delivery_time", "mean", "median", "mode",
            "18", "20", "22", "26", "28", "80",
            "30.9", "22 minutes", "range", "variance", "standard deviation",
            "481.1", "21.9", "62 minutes",
            "zone", "Ikeja", "Lekki", "Surulere", "Yaba",
            "shift", "morning", "afternoon", "evening",
            "describe()", "mean=52", "median=38",
            "plt.subplots(2, 2)", "plt.subplot(131)", "plt.suptitle",
            "Delivery Performance -- Last Quarter",
            "order_id", "driver_id", "driver_name",
            "orders", "drivers",
            "isna()", "dropna()", "fillna()", "groupby().mean()",
            "COUNTIFS", "PivotTable",
            "2026-04-01", "2026-06-30"
        ]
    },
    {
        "scenario_id": "scen_ab_test",
        "name": "QuickRide App — Checkout Button A/B Test",
        "summary": (
            "QuickRide's product team runs a randomised A/B test on the ordering app's checkout button. "
            "The control group (A) sees the original button; the treatment group (B) sees a redesigned button. "
            "The metric compared is the share of users who complete an order (conversion rate). "
            "Control rate: 0.20 (20 %); treatment rate: 0.22 (22 %); lift: 10 %."
        ),
        "locale": "en-NG",
        "currency": "NGN",
        "domain": "product / experimentation",
        "glossary_example_vocab": [
            "control group", "treatment group", "A/B test",
            "checkout button", "conversion rate",
            "0.20", "0.22", "10%", "lift",
            "randomized experiment", "baseline",
            "positive lift", "negative lift", "neutral",
            "user_id", "group", "converted"
        ]
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 1 — seven-order teaching batch
# Exactly the seven delivery times from the teaching blocks: 18,20,22,22,26,28,80
# Used by: tile_stats_center_spread (both concepts)
# mean=30.9, median=22, mode=22, range=62, variance≈481.1, std≈21.9
# ─────────────────────────────────────────────────────────────────────────────
ds_seven = {
    "asset_id": "ds_seven_delivery_times",
    "asset_kind": "dataset",
    "scenario_id": "scen_delivery_stats",
    "title": "Seven-Order Delivery Batch (Teaching Example)",
    "description": (
        "The exact seven delivery times used in the teaching blocks for measures of center and spread: "
        "18, 20, 22, 22, 26, 28, 80 minutes. "
        "Mean ≈ 30.9, median = 22, mode = 22, range = 62, variance ≈ 481.1, std ≈ 21.9."
    ),
    "columns": [
        {
            "name": "order_id",
            "type": "string",
            "semantic_role": "identifier",
            "description": "Unique order identifier"
        },
        {
            "name": "delivery_time",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Delivery time in minutes from dispatch to drop-off"
        }
    ],
    # Rows: exactly the seven values from the teaching blocks, sorted ascending
    # (sorted order is used in the teaching block for median explanation)
    "rows": [
        ["ORD-001", 18],
        ["ORD-002", 20],
        ["ORD-003", 22],
        ["ORD-004", 22],
        ["ORD-005", 26],
        ["ORD-006", 28],
        ["ORD-007", 80]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 2 — capstone orders table
# Columns: order_id, driver_id, zone, order_date, delivery_time
#
# Glossary constraints:
#   - SQL query: orders INNER JOIN drivers ON driver_id, WHERE order_date
#     >= '2026-04-01' AND < '2026-07-01', GROUP BY zone → AVG(delivery_time)
#   - Zones: Ikeja, Lekki, Surulere, Yaba
#   - Shifts: morning, afternoon, evening (in spreadsheet variant)
#   - Ikeja describe(): mean=52.0, median=38.0 (skewed by extreme values)
#   - COUNTIFS: Ikeja deliveries > 45 minutes
#   - Some NaN delivery_times for pandas cleaning exercise
#   - Enough rows per zone for hidden tests (≥ 8 per zone)
#
# Ikeja times (10 rows): 28,32,35,36,38,38,42,45,48,178
#   sum=520, mean=52.0, median=(38+38)/2=38.0 ✓
#   Ikeja rows with delivery_time > 45: 48, 178 → 2 rows
#
# ─────────────────────────────────────────────────────────────────────────────

# driver_id values: D01–D08
# order_date: all within 2026-04-01 to 2026-06-30

orders_columns = [
    {
        "name": "order_id",
        "type": "string",
        "semantic_role": "identifier",
        "description": "Unique order identifier"
    },
    {
        "name": "driver_id",
        "type": "string",
        "semantic_role": "identifier",
        "description": "Foreign key referencing drivers.driver_id"
    },
    {
        "name": "zone",
        "type": "string",
        "semantic_role": "categorical",
        "description": "Delivery zone within Lagos"
    },
    {
        "name": "order_date",
        "type": "date",
        "semantic_role": "datetime",
        "description": "Date the order was placed (YYYY-MM-DD)"
    },
    {
        "name": "delivery_time",
        "type": "integer",
        "semantic_role": "numerical",
        "unit": "minutes",
        "description": "Delivery time in minutes; NULL where not yet recorded"
    }
]

# Build rows: 10 Ikeja + 8 Lekki + 8 Surulere + 8 Yaba = 34 rows
# Ikeja: mean=52.0, median=38.0
# We include 2 NaN delivery_times (one Lekki, one Surulere) for pandas exercise
# All dates within 2026-04-01 to 2026-06-30

orders_rows = [
    # Ikeja (10 rows) — driver_id D01/D02
    # times: 28,32,35,36,38,38,42,45,48,178 → mean=52.0, median=38.0
    ["O-001", "D01", "Ikeja", "2026-04-03", 28],
    ["O-002", "D01", "Ikeja", "2026-04-10", 32],
    ["O-003", "D02", "Ikeja", "2026-04-17", 35],
    ["O-004", "D02", "Ikeja", "2026-04-24", 36],
    ["O-005", "D01", "Ikeja", "2026-05-02", 38],
    ["O-006", "D02", "Ikeja", "2026-05-09", 38],
    ["O-007", "D01", "Ikeja", "2026-05-16", 42],
    ["O-008", "D02", "Ikeja", "2026-05-23", 45],
    ["O-009", "D01", "Ikeja", "2026-06-06", 48],
    ["O-010", "D02", "Ikeja", "2026-06-20", 178],  # extreme outlier (stalled vehicle / wrong address)

    # Lekki (8 rows) — driver_id D03/D04
    # times: 22,25,28,30,32,35,38,40 → mean=31.2
    ["O-011", "D03", "Lekki", "2026-04-04", 22],
    ["O-012", "D03", "Lekki", "2026-04-11", 25],
    ["O-013", "D04", "Lekki", "2026-04-18", 28],
    ["O-014", "D04", "Lekki", "2026-04-25", 30],
    ["O-015", "D03", "Lekki", "2026-05-03", 32],
    ["O-016", "D04", "Lekki", "2026-05-10", 35],
    ["O-017", "D03", "Lekki", "2026-05-17", None],  # NaN — for pandas cleaning exercise
    ["O-018", "D04", "Lekki", "2026-06-07", 40],

    # Surulere (8 rows) — driver_id D05/D06
    # times: 18,20,22,25,28,30,32,35 → mean=26.2
    ["O-019", "D05", "Surulere", "2026-04-05", 18],
    ["O-020", "D05", "Surulere", "2026-04-12", 20],
    ["O-021", "D06", "Surulere", "2026-04-19", 22],
    ["O-022", "D06", "Surulere", "2026-04-26", 25],
    ["O-023", "D05", "Surulere", "2026-05-04", 28],
    ["O-024", "D06", "Surulere", "2026-05-11", None],  # NaN — for pandas cleaning exercise
    ["O-025", "D05", "Surulere", "2026-05-18", 32],
    ["O-026", "D06", "Surulere", "2026-06-08", 35],

    # Yaba (8 rows) — driver_id D07/D08
    # times: 25,28,30,32,35,38,40,42 → mean=33.8
    ["O-027", "D07", "Yaba", "2026-04-06", 25],
    ["O-028", "D07", "Yaba", "2026-04-13", 28],
    ["O-029", "D08", "Yaba", "2026-04-20", 30],
    ["O-030", "D08", "Yaba", "2026-04-27", 32],
    ["O-031", "D07", "Yaba", "2026-05-05", 35],
    ["O-032", "D08", "Yaba", "2026-05-12", 38],
    ["O-033", "D07", "Yaba", "2026-05-19", 40],
    ["O-034", "D08", "Yaba", "2026-06-09", 42],
]

# Verify Ikeja stats
ikeja_times = [r[4] for r in orders_rows if r[2] == "Ikeja" and r[4] is not None]
ikeja_times_sorted = sorted(ikeja_times)
n = len(ikeja_times)
mean_ikeja = sum(ikeja_times) / n
median_ikeja = (ikeja_times_sorted[n//2 - 1] + ikeja_times_sorted[n//2]) / 2
ikeja_gt45 = [t for t in ikeja_times if t > 45]
print(f"Ikeja n={n}, mean={mean_ikeja:.1f}, median={median_ikeja:.1f}, >45: {ikeja_gt45}")

ds_orders = {
    "asset_id": "ds_capstone_orders",
    "asset_kind": "dataset",
    "scenario_id": "scen_delivery_stats",
    "title": "Capstone Orders Table",
    "description": (
        "Last-quarter orders (2026-04-01 to 2026-06-30) for QuickRide. "
        "Used for SQL retrieval (INNER JOIN with drivers, WHERE date range, GROUP BY zone), "
        "pandas cleaning (NaN delivery_times, groupby zone mean), "
        "descriptive statistics (Ikeja mean=52.0, median=38.0), "
        "and multi-panel dashboard visualisation."
    ),
    "columns": orders_columns,
    "rows": orders_rows,
    "provenance": "authored",
    # ── messy variant: planted issues for find_issues exercise ──────────────
    "variants": [
        {
            "variant_id": "ds_capstone_orders_messy",
            "derived_from": "ds_capstone_orders",
            "purpose": "Data-quality exercise: impossible delivery_time, duplicate order, inconsistent zone casing",
            "ops": [
                # Op 1: set an impossible delivery_time (negative value) on O-003
                {
                    "op": "set_cell",
                    "where": {"order_id": "O-003"},
                    "occurrence": 0,
                    "column": "delivery_time",
                    "value": -5
                },
                # Op 2: duplicate row O-011 (Lekki, D03, 2026-04-04, 22)
                {
                    "op": "duplicate_row",
                    "where": {"order_id": "O-011"},
                    "occurrence": 0,
                    "insert": "end"
                },
                # Op 3: inconsistent zone casing on O-027 (Yaba → yaba)
                {
                    "op": "set_cell",
                    "where": {"order_id": "O-027"},
                    "occurrence": 0,
                    "column": "zone",
                    "value": "yaba"
                }
            ],
            "planted_issues": [
                {
                    "issue_id": "issue_impossible_delivery_time",
                    "kind": "impossible_value",
                    "locations": [
                        {
                            "where": {"order_id": "O-003"},
                            "occurrence": 0,
                            "column": "delivery_time"
                        }
                    ],
                    "description": "delivery_time of -5 minutes is impossible; delivery times must be positive.",
                    "rule": {
                        "column": "delivery_time",
                        "op": "lt",
                        "value": 0
                    }
                },
                {
                    "issue_id": "issue_duplicate_order",
                    "kind": "duplicate_row",
                    "locations": [
                        {
                            "where": {"order_id": "O-011"},
                            "occurrence": 0,
                            "column": "order_id"
                        },
                        {
                            "where": {"order_id": "O-011"},
                            "occurrence": 1,
                            "column": "order_id"
                        }
                    ],
                    "description": "Order O-011 appears twice; the second row is a duplicate."
                },
                {
                    "issue_id": "issue_zone_casing",
                    "kind": "inconsistent_category",
                    "locations": [
                        {
                            "where": {"order_id": "O-027"},
                            "occurrence": 0,
                            "column": "zone"
                        }
                    ],
                    "description": "Zone value 'yaba' uses lower-case while all other zone values use title-case (e.g. 'Yaba').",
                    "rule": {
                        "column": "zone",
                        "op": "casing_differs_from_siblings"
                    }
                }
            ]
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 3 — capstone drivers table
# Columns: driver_id, driver_name
# Used by: capstone.integrate_sql (INNER JOIN), capstone.building_data_model
# driver_id is PK; referenced as FK in orders.driver_id
# ─────────────────────────────────────────────────────────────────────────────
ds_drivers = {
    "asset_id": "ds_capstone_drivers",
    "asset_kind": "dataset",
    "scenario_id": "scen_delivery_stats",
    "title": "Capstone Drivers Table",
    "description": (
        "Driver roster for QuickRide. driver_id is the primary key. "
        "Orders.driver_id is a foreign key referencing this table. "
        "One driver delivers many orders (one-to-many relationship)."
    ),
    "columns": [
        {
            "name": "driver_id",
            "type": "string",
            "semantic_role": "identifier",
            "description": "Primary key — uniquely identifies each driver"
        },
        {
            "name": "driver_name",
            "type": "string",
            "semantic_role": "text",
            "description": "Driver's full name"
        }
    ],
    "rows": [
        ["D01", "Amara Okafor"],
        ["D02", "Chidi Eze"],
        ["D03", "Ngozi Adeyemi"],
        ["D04", "Emeka Nwosu"],
        ["D05", "Fatima Bello"],
        ["D06", "Tunde Adesanya"],
        ["D07", "Kemi Lawal"],
        ["D08", "Seun Adebayo"]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 4 — capstone delivery sheet (spreadsheet variant)
# Columns: zone, shift, delivery_time
# Used by: capstone.integrate_spreadsheet (PivotTable zone×shift, COUNTIFS)
# Glossary: COUNTIFS(zone_range, "Ikeja", delivery_time_range, ">45")
# ─────────────────────────────────────────────────────────────────────────────
# We need enough rows per zone×shift cell for the PivotTable to be meaningful.
# Ikeja/morning, Ikeja/afternoon, Ikeja/evening
# Lekki/morning, Lekki/afternoon, Lekki/evening
# Surulere/morning, Surulere/afternoon, Surulere/evening
# Yaba/morning, Yaba/afternoon, Yaba/evening
# At least 2 rows per cell = 24 rows minimum; we'll use 3 per cell = 36 rows.
# Ikeja deliveries > 45: at least 3 rows (for COUNTIFS to return a non-trivial count)

delivery_sheet_rows = [
    # Ikeja morning (3 rows): 28, 38, 48 → avg=38.0; 48>45 ✓
    ["Ikeja", "morning", 28],
    ["Ikeja", "morning", 38],
    ["Ikeja", "morning", 48],
    # Ikeja afternoon (3 rows): 35, 42, 178 → avg=85.0; 178>45 ✓
    ["Ikeja", "afternoon", 35],
    ["Ikeja", "afternoon", 42],
    ["Ikeja", "afternoon", 178],
    # Ikeja evening (3 rows): 32, 36, 45 → avg=37.7; none >45
    ["Ikeja", "evening", 32],
    ["Ikeja", "evening", 36],
    ["Ikeja", "evening", 45],
    # Lekki morning (3 rows): 22, 28, 32 → avg=27.3
    ["Lekki", "morning", 22],
    ["Lekki", "morning", 28],
    ["Lekki", "morning", 32],
    # Lekki afternoon (3 rows): 25, 30, 38 → avg=31.0
    ["Lekki", "afternoon", 25],
    ["Lekki", "afternoon", 30],
    ["Lekki", "afternoon", 38],
    # Lekki evening (3 rows): 20, 25, 40 → avg=28.3
    ["Lekki", "evening", 20],
    ["Lekki", "evening", 25],
    ["Lekki", "evening", 40],
    # Surulere morning (3 rows): 18, 22, 28 → avg=22.7
    ["Surulere", "morning", 18],
    ["Surulere", "morning", 22],
    ["Surulere", "morning", 28],
    # Surulere afternoon (3 rows): 20, 25, 32 → avg=25.7
    ["Surulere", "afternoon", 20],
    ["Surulere", "afternoon", 25],
    ["Surulere", "afternoon", 32],
    # Surulere evening (3 rows): 22, 30, 35 → avg=29.0
    ["Surulere", "evening", 22],
    ["Surulere", "evening", 30],
    ["Surulere", "evening", 35],
    # Yaba morning (3 rows): 25, 30, 35 → avg=30.0
    ["Yaba", "morning", 25],
    ["Yaba", "morning", 30],
    ["Yaba", "morning", 35],
    # Yaba afternoon (3 rows): 28, 32, 40 → avg=33.3
    ["Yaba", "afternoon", 28],
    ["Yaba", "afternoon", 32],
    ["Yaba", "afternoon", 40],
    # Yaba evening (3 rows): 30, 38, 42 → avg=36.7
    ["Yaba", "evening", 30],
    ["Yaba", "evening", 38],
    ["Yaba", "evening", 42],
]

# Verify Ikeja >45 count
ikeja_gt45_sheet = [r[2] for r in delivery_sheet_rows if r[0] == "Ikeja" and r[2] > 45]
print(f"Delivery sheet Ikeja >45: {ikeja_gt45_sheet} (count={len(ikeja_gt45_sheet)})")

ds_delivery_sheet = {
    "asset_id": "ds_capstone_delivery_sheet",
    "asset_kind": "dataset",
    "scenario_id": "scen_delivery_stats",
    "title": "Capstone Delivery Sheet (Spreadsheet Exercise)",
    "description": (
        "Delivery records with zone, shift, and delivery_time for the spreadsheet PivotTable and COUNTIFS exercise. "
        "Each row pairs an order's zone and delivery_time with the driver's shift. "
        "COUNTIFS(zone_range, 'Ikeja', delivery_time_range, '>45') returns 2 (rows with 48 and 178 minutes)."
    ),
    "columns": [
        {
            "name": "zone",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Delivery zone within Lagos"
        },
        {
            "name": "shift",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Driver shift: morning, afternoon, or evening"
        },
        {
            "name": "delivery_time",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Delivery time in minutes"
        }
    ],
    "rows": delivery_sheet_rows,
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 5 — A/B test results table
# Columns: user_id, group, converted
# Used by: tile_stats_ab_test_lift (both concepts)
# Control (A): 500 users, 100 converted → rate = 0.20
# Treatment (B): 500 users, 110 converted → rate = 0.22
# Lift = (0.22 - 0.20) / 0.20 * 100 = 10.0%
# We store a summary table (not 1000 individual rows) for the teaching display.
# ─────────────────────────────────────────────────────────────────────────────
ds_ab_summary = {
    "asset_id": "ds_ab_test_summary",
    "asset_kind": "dataset",
    "scenario_id": "scen_ab_test",
    "title": "A/B Test Summary — Checkout Button",
    "description": (
        "Summary of the checkout-button A/B test. "
        "Control (A): 500 users, 100 converted, rate=0.20. "
        "Treatment (B): 500 users, 110 converted, rate=0.22. "
        "Absolute difference: 0.02. Lift: 10.0% (positive)."
    ),
    "columns": [
        {
            "name": "group",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Test group: control (A) or treatment (B)"
        },
        {
            "name": "users",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "count",
            "description": "Number of users in the group"
        },
        {
            "name": "conversions",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "count",
            "description": "Number of users who completed an order"
        },
        {
            "name": "conversion_rate",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "proportion",
            "description": "Conversions / users; control=0.20, treatment=0.22"
        }
    ],
    "rows": [
        ["control",   500, 100, 0.20],
        ["treatment", 500, 110, 0.22]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 6 — A/B test individual-user table (for live_code exercise)
# Columns: user_id, group, converted
# Enough rows for hidden tests; control rate=0.20, treatment rate=0.22
# We use 50 rows (25 control, 25 treatment) as a representative sample.
# Control: 5 converted out of 25 → rate=0.20
# Treatment: 5.5 → round to 6 converted out of 25 → rate=0.24 (close enough for
#   the exercise; the function is tested with the exact floats 0.20 and 0.22)
# Actually the live_code exercise passes floats directly, not this table.
# This table is for field_selection (ab_test_structure) and classify exercises.
# Let's keep it simple: 20 rows, 10 per group.
# Control: 2 converted (rate=0.20), Treatment: 2.2 → 2 converted (rate=0.20)
# That's too close. Let's use 50 rows: 25 control (5 converted=0.20),
# 25 treatment (6 converted=0.24). The exact 0.20/0.22 numbers come from
# the summary table; this table is for structural exercises.
# ─────────────────────────────────────────────────────────────────────────────

# Build 50 user rows: 25 control (5 converted), 25 treatment (6 converted)
ab_user_rows = []
for i in range(1, 26):
    converted = 1 if i <= 5 else 0
    ab_user_rows.append([f"U-C{i:03d}", "control", converted])
for i in range(1, 26):
    converted = 1 if i <= 6 else 0
    ab_user_rows.append([f"U-T{i:03d}", "treatment", converted])

# Verify
ctrl_rate = sum(r[2] for r in ab_user_rows if r[1] == "control") / 25
trt_rate  = sum(r[2] for r in ab_user_rows if r[1] == "treatment") / 25
print(f"AB user table: control_rate={ctrl_rate:.2f}, treatment_rate={trt_rate:.2f}")

ds_ab_users = {
    "asset_id": "ds_ab_test_users",
    "asset_kind": "dataset",
    "scenario_id": "scen_ab_test",
    "title": "A/B Test Individual User Records — Checkout Button",
    "description": (
        "Individual user records for the checkout-button A/B test. "
        "50 rows: 25 control users (5 converted, rate=0.20) and "
        "25 treatment users (6 converted, rate=0.24). "
        "Used for field_selection exercises identifying control/treatment groups and the comparison metric."
    ),
    "columns": [
        {
            "name": "user_id",
            "type": "string",
            "semantic_role": "identifier",
            "description": "Unique user identifier"
        },
        {
            "name": "group",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Test group assignment: 'control' or 'treatment'"
        },
        {
            "name": "converted",
            "type": "integer",
            "semantic_role": "numerical",
            "numeric_looking_label": False,
            "description": "1 if the user completed an order, 0 otherwise"
        }
    ],
    "rows": ab_user_rows,
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 7 — pandas practice DataFrame (capstone.integrate_python_pandas)
# Columns: zone, delivery_time (with NaN values)
# Exactly matches the practice anchor: "small orders DataFrame with 'zone' and
# 'delivery_time' columns containing some NaN values"
# Enough rows for hidden tests; NaN values present; groupby zone mean computable.
# ─────────────────────────────────────────────────────────────────────────────
pandas_rows = [
    # Ikeja: 28, 38, None, 42 → after dropna: 28,38,42 → mean=36.0
    ["Ikeja",    28],
    ["Ikeja",    38],
    ["Ikeja",    None],
    ["Ikeja",    42],
    # Lekki: 22, None, 30, 35 → after dropna: 22,30,35 → mean=29.0
    ["Lekki",    22],
    ["Lekki",    None],
    ["Lekki",    30],
    ["Lekki",    35],
    # Surulere: 18, 25, 32 → mean=25.0
    ["Surulere", 18],
    ["Surulere", 25],
    ["Surulere", 32],
    # Yaba: 28, 35, 40, None → after dropna: 28,35,40 → mean=34.3
    ["Yaba",     28],
    ["Yaba",     35],
    ["Yaba",     40],
    ["Yaba",     None],
]

# Verify
from collections import defaultdict
zone_times = defaultdict(list)
for r in pandas_rows:
    if r[1] is not None:
        zone_times[r[0]].append(r[1])
for z, ts in sorted(zone_times.items()):
    print(f"  pandas {z}: mean={sum(ts)/len(ts):.1f}")

ds_pandas_orders = {
    "asset_id": "ds_pandas_orders",
    "asset_kind": "dataset",
    "scenario_id": "scen_delivery_stats",
    "title": "Pandas Practice Orders (Missing Values Exercise)",
    "description": (
        "Small orders DataFrame for the pandas cleaning exercise. "
        "Contains 'zone' and 'delivery_time' columns with NaN delivery_times. "
        "After dropna(), groupby('zone')['delivery_time'].mean() returns one mean per zone."
    ),
    "columns": [
        {
            "name": "zone",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Delivery zone within Lagos"
        },
        {
            "name": "delivery_time",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Delivery time in minutes; None where not recorded"
        }
    ],
    "rows": pandas_rows,
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSEMBLE REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
registry = {
    "schema_version": "1.0.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_010_da_stats_capstone",
    "scenarios": scenarios,
    "assets": [
        ds_seven,
        ds_orders,
        ds_drivers,
        ds_delivery_sheet,
        ds_ab_summary,
        ds_ab_users,
        ds_pandas_orders,
    ],
    "provenance": {
        "model": "claude-opus-4-5",
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# SELF-CHECK: row widths
# ─────────────────────────────────────────────────────────────────────────────
for a in registry["assets"]:
    if a["asset_kind"] != "dataset":
        continue
    n_cols = len(a["columns"])
    for i, row in enumerate(a.get("rows", [])):
        assert len(row) == n_cols, (
            f"{a['asset_id']} row {i}: width {len(row)} != {n_cols} columns"
        )
print("Row-width check: PASS")

# ─────────────────────────────────────────────────────────────────────────────
# WRITE
# ─────────────────────────────────────────────────────────────────────────────
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    json.dump(registry, f, indent=2)
print(f"Written: {OUT}")
print(f"Scenarios: {len(registry['scenarios'])}")
print(f"Assets: {len(registry['assets'])}")
for a in registry["assets"]:
    n_rows = len(a.get("rows", []))
    n_variants = len(a.get("variants", []))
    print(f"  {a['asset_id']} ({a['asset_kind']}): {n_rows} rows, {n_variants} variants")
