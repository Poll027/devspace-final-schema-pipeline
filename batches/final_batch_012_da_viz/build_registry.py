"""Build scenario_asset_registry.json for final_batch_012_da_viz.

All values come from the glossary teaching blocks and practice anchors.
Key glossary vocabulary:
  - DataFrame named `orders` with columns: order_id, city, delivery_time_minutes, distance_km, order_value, num_items
  - Cities: Lagos, Abuja, Kano
  - Delivery times (week 1, days 1-5): 18, 22, 26, 19, 30
  - Lagos daily averages (days 1-5): 21, 23, 19, 25, 20
  - Box plot example: Lagos Q1=20, Q3=30, IQR=10, whisker max=45, flier=50
  - chart_type_selection practice uses column name 'delivery_minutes' (not delivery_time_minutes)
  - seaborn_themes_palettes practice uses 'category'/'value' columns
"""
import json
from pathlib import Path

BATCH = Path("batches/final_batch_012_da_viz")

# ── helpers ──────────────────────────────────────────────────────────────────

def col(name, typ, role, unit=None, desc=None, numeric_looking_label=False):
    c = {"name": name, "type": typ, "semantic_role": role}
    if unit is not None:
        c["unit"] = unit
    if desc is not None:
        c["description"] = desc
    if numeric_looking_label:
        c["numeric_looking_label"] = True
    return c


# ── scenarios ────────────────────────────────────────────────────────────────

scenarios = [
    {
        "scenario_id": "scen.da_viz_delivery",
        "name": "QuickDeliver — Nigerian last-mile logistics",
        "summary": (
            "QuickDeliver is a fictional Nigerian last-mile delivery company operating in Lagos, "
            "Abuja, and Kano. Analysts use an `orders` DataFrame to explore delivery performance: "
            "how long deliveries take, how far riders travel, order values, and item counts. "
            "The scenario supports all matplotlib and seaborn visualisation exercises."
        ),
        "locale": "NG",
        "currency": "NGN",
        "domain": "logistics",
        "glossary_example_vocab": [
            "orders", "delivery_time_minutes", "distance_km", "city", "order_value", "num_items",
            "Lagos", "Abuja", "Kano",
            "plt.subplots()", "ax.plot()", "plt.plot()", "plt.bar()", "plt.hist()", "plt.scatter()",
            "plt.boxplot()", "ax.set_xlabel()", "ax.set_ylabel()", "ax.set_title()", "ax.legend()",
            "sns.barplot()", "sns.regplot()", "sns.set_theme()", "sns.set_palette()",
            "groupby", "city_avg", "lagos_times", "abuja_times", "kano_times",
            "figsize", "tight_layout", "tick_labels",
            "18", "22", "26", "19", "30",
            "21", "23", "19", "25", "20",
            "Q1=20", "Q3=30", "IQR=10"
        ]
    },
    {
        "scenario_id": "scen.da_viz_theming",
        "name": "QuickDeliver — theme and palette demo",
        "summary": (
            "A minimal two-column summary table (category / value) used exclusively for "
            "seaborn theme and palette exercises where the data content is intentionally "
            "neutral so the visual styling change is the focus."
        ),
        "locale": "NG",
        "domain": "logistics",
        "glossary_example_vocab": [
            "category", "value",
            "sns.set_theme()", "sns.set_palette()", "style", "palette",
            "whitegrid", "deep", "pastel", "darkgrid"
        ]
    }
]

# ── main orders dataset ───────────────────────────────────────────────────────
# Columns: order_id, city, delivery_time_minutes, distance_km, order_value, num_items
# Constraints from glossary:
#   - Three cities: Lagos, Abuja, Kano
#   - Days 1-5 delivery times (week 1): 18, 22, 26, 19, 30 (used in ax.plot examples)
#   - Lagos daily averages (days 1-5): 21, 23, 19, 25, 20
#   - Lagos box: Q1=20, Q3=30, IQR=10, whisker max=45, flier=50
#   - Kano average > Lagos average (bar chart example: Kano taller bar)
#   - distance_km and delivery_time_minutes should show positive relationship (scatter)
#   - Need enough rows for hidden checks (>= 20 rows), duplicates/missing for messy variant
#
# We need per-city distributions that honour the Q1/Q3 example:
#   Lagos: Q1=20, Q3=30 → values spread 15-50 with one flier at 50
#   Abuja: moderate spread
#   Kano: higher average than Lagos (bar chart: Kano bar taller)
#
# order_id: numeric-looking label (integer used as identifier)

orders_columns = [
    col("order_id",               "integer", "identifier",  desc="Unique order identifier", numeric_looking_label=True),
    col("city",                   "string",  "categorical", desc="Delivery city: Lagos, Abuja, or Kano"),
    col("delivery_time_minutes",  "integer", "numerical",   unit="minutes", desc="Total delivery time in minutes"),
    col("distance_km",            "number",  "numerical",   unit="km",      desc="Delivery distance in kilometres"),
    col("order_value",            "number",  "numerical",   unit="NGN",     desc="Order value in Nigerian Naira"),
    col("num_items",              "integer", "numerical",   desc="Number of items in the order"),
]

# 24 rows: 8 Lagos, 8 Abuja, 8 Kano
# Lagos: Q1=20, Q3=30 → need values such that Q1=20, Q3=30, median ~25, one flier at 50
# Values: 15, 18, 20, 22, 25, 28, 30, 50  → sorted: 15,18,20,22,25,28,30,50
#   Q1 = (18+20)/2 = 19 ... let's use: 16,19,20,22,25,28,30,50
#   Q1 = (19+20)/2=19.5 ... try: 15,20,20,22,25,28,30,50
#   Q1=20, Q3=30: need 8 values where 25th pct=20, 75th pct=30
#   With 8 values sorted: Q1=val[1]=20, Q3=val[5]=30 (numpy default interpolation)
#   sorted: 15, 20, 22, 24, 26, 30, 35, 50  → Q1=(20+22)/2=21, Q3=(30+35)/2=32.5 ... not exact
#   The glossary says "if Lagos's box runs from Q1=20 to Q3=30" as an EXAMPLE, not a constraint
#   we must honour. We just need the data to be plausible.
# Kano average > Lagos average (glossary: "bar for Kano simply looks taller than Lagos's")
# Lagos avg from teaching: 21,23,19,25,20 → mean=21.6 (daily averages, not individual orders)
# We'll make Lagos mean ~24, Kano mean ~30, Abuja mean ~27

orders_rows = [
    # order_id, city,    delivery_time_minutes, distance_km, order_value, num_items
    # Lagos (8 rows) — mean ~24, spread 15-50, one flier at 50
    [1001, "Lagos",  18,  2.1,  1850.0,  2],
    [1002, "Lagos",  22,  3.4,  2200.0,  3],
    [1003, "Lagos",  19,  2.8,  1600.0,  1],
    [1004, "Lagos",  26,  4.5,  3100.0,  4],
    [1005, "Lagos",  30,  5.2,  2750.0,  3],
    [1006, "Lagos",  24,  3.9,  2400.0,  2],
    [1007, "Lagos",  28,  4.8,  3300.0,  5],
    [1008, "Lagos",  50,  9.1,  4800.0,  6],  # flier: 50-minute delivery
    # Abuja (8 rows) — mean ~27
    [1009, "Abuja",  25,  3.2,  2100.0,  2],
    [1010, "Abuja",  28,  4.1,  2600.0,  3],
    [1011, "Abuja",  23,  3.0,  1900.0,  1],
    [1012, "Abuja",  31,  5.5,  3400.0,  4],
    [1013, "Abuja",  27,  4.3,  2800.0,  3],
    [1014, "Abuja",  29,  4.7,  3000.0,  2],
    [1015, "Abuja",  26,  4.0,  2500.0,  3],
    [1016, "Abuja",  32,  5.8,  3600.0,  5],
    # Kano (8 rows) — mean ~30, higher than Lagos
    [1017, "Kano",   28,  4.6,  2300.0,  2],
    [1018, "Kano",   32,  5.9,  3100.0,  4],
    [1019, "Kano",   27,  4.2,  2000.0,  2],
    [1020, "Kano",   35,  6.8,  3800.0,  5],
    [1021, "Kano",   30,  5.3,  2700.0,  3],
    [1022, "Kano",   33,  6.1,  3400.0,  4],
    [1023, "Kano",   29,  5.0,  2600.0,  3],
    [1024, "Kano",   36,  7.2,  4100.0,  6],
]

# Verify row widths
assert all(len(r) == len(orders_columns) for r in orders_rows), "Row width mismatch in orders"

# ── messy variant of orders ───────────────────────────────────────────────────
# Purpose: find_issues / data-quality exercises
# Planted issues:
#   1. missing_value: delivery_time_minutes is null for order 1003
#   2. impossible_value: delivery_time_minutes = -5 for order 1010 (negative time)
#   3. inconsistent_category: city = "lagos" (lowercase) for order 1005
#   4. duplicate_row: order 1007 duplicated
#   5. outlier_suspicious: distance_km = 99.9 for order 1020 (implausibly large)

orders_messy_ops = [
    # 1. Set delivery_time_minutes to null for order 1003
    {"op": "set_cell", "where": {"order_id": 1003}, "column": "delivery_time_minutes", "value": None},
    # 2. Set delivery_time_minutes to -5 for order 1010
    {"op": "set_cell", "where": {"order_id": 1010}, "column": "delivery_time_minutes", "value": -5},
    # 3. Set city to "lagos" (lowercase) for order 1005
    {"op": "set_cell", "where": {"order_id": 1005}, "column": "city", "value": "lagos"},
    # 4. Duplicate order 1007
    {"op": "duplicate_row", "where": {"order_id": 1007}},
    # 5. Set distance_km to 99.9 for order 1020
    {"op": "set_cell", "where": {"order_id": 1020}, "column": "distance_km", "value": 99.9},
]

orders_messy_planted = [
    {
        "issue_id": "iss.missing_delivery_time",
        "kind": "missing_value",
        "locations": [{"where": {"order_id": 1003}, "column": "delivery_time_minutes"}],
        "description": "delivery_time_minutes is null for order 1003 — value was not recorded.",
        "rule": {"column": "delivery_time_minutes", "op": "is_null"}
    },
    {
        "issue_id": "iss.negative_delivery_time",
        "kind": "impossible_value",
        "locations": [{"where": {"order_id": 1010}, "column": "delivery_time_minutes"}],
        "description": "delivery_time_minutes is -5 for order 1010 — delivery time cannot be negative.",
        "rule": {"column": "delivery_time_minutes", "op": "lt", "value": 0}
    },
    {
        "issue_id": "iss.city_casing",
        "kind": "inconsistent_category",
        "locations": [{"where": {"order_id": 1005}, "column": "city"}],
        "description": "city is 'lagos' (lowercase) for order 1005 — all other city values use title case.",
        "rule": {"column": "city", "op": "casing_differs_from_siblings"}
    },
    {
        "issue_id": "iss.duplicate_order_1007",
        "kind": "duplicate_row",
        "locations": [
            {"where": {"order_id": 1007}, "occurrence": 0, "column": "order_id"},
            {"where": {"order_id": 1007}, "occurrence": 1, "column": "order_id"}
        ],
        "description": "order_id 1007 appears twice — the row was duplicated."
    },
    {
        "issue_id": "iss.implausible_distance",
        "kind": "outlier_suspicious",
        "locations": [{"where": {"order_id": 1020}, "column": "distance_km"}],
        "description": "distance_km is 99.9 km for order 1020 — implausibly large for a city delivery.",
        "rule": {"column": "distance_km", "op": "gt", "value": 50}
    },
]

# ── daily_averages dataset ────────────────────────────────────────────────────
# Used for line-plot and labeling exercises.
# Columns: day, lagos_avg, abuja_avg
# Values from glossary: Lagos days 1-5: 21, 23, 19, 25, 20
# Abuja added for multi-series legend exercise (labeling_annotation TB2)

daily_columns = [
    col("day",       "integer", "identifier",  desc="Day number (1=Monday … 5=Friday)", numeric_looking_label=True),
    col("lagos_avg", "number",  "numerical",   unit="minutes", desc="Average delivery time in Lagos for that day"),
    col("abuja_avg", "number",  "numerical",   unit="minutes", desc="Average delivery time in Abuja for that day"),
]

daily_rows = [
    # day, lagos_avg, abuja_avg
    [1, 21.0, 24.0],
    [2, 23.0, 26.0],
    [3, 19.0, 22.0],
    [4, 25.0, 28.0],
    [5, 20.0, 25.0],
]

assert all(len(r) == len(daily_columns) for r in daily_rows), "Row width mismatch in daily_averages"

# ── chart_selection_mini dataset ─────────────────────────────────────────────
# chart_type_selection practice anchor uses column names 'distance_km' and 'delivery_minutes'
# (not delivery_time_minutes — the practice anchor explicitly names 'delivery_minutes')
# Six rows as stated in the starter_state_intent.

chart_sel_columns = [
    col("distance_km",      "number",  "numerical", unit="km",      desc="Delivery distance in kilometres"),
    col("delivery_minutes", "integer", "numerical", unit="minutes", desc="Delivery time in minutes"),
]

chart_sel_rows = [
    # distance_km, delivery_minutes
    [1.2,  14],
    [2.5,  21],
    [3.8,  28],
    [4.1,  31],
    [5.6,  38],
    [6.3,  44],
]

assert all(len(r) == len(chart_sel_columns) for r in chart_sel_rows), "Row width mismatch in chart_sel"

# ── theming_demo dataset ──────────────────────────────────────────────────────
# seaborn_themes_palettes practice: 'category' and 'value' columns

theme_columns = [
    col("category", "string",  "categorical", desc="Delivery city category"),
    col("value",    "number",  "numerical",   unit="minutes", desc="Average delivery time in minutes"),
]

theme_rows = [
    ["Lagos",  24.0],
    ["Abuja",  27.0],
    ["Kano",   30.0],
]

assert all(len(r) == len(theme_columns) for r in theme_rows), "Row width mismatch in theme"

# ── assemble registry ─────────────────────────────────────────────────────────

registry = {
    "schema_version": "1.0.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_012_da_viz",
    "scenarios": scenarios,
    "assets": [
        # ── 1. Main orders dataset (clean) ──────────────────────────────────
        {
            "asset_id": "ds.orders",
            "asset_kind": "dataset",
            "scenario_id": "scen.da_viz_delivery",
            "title": "QuickDeliver orders — clean",
            "description": (
                "Individual delivery orders for QuickDeliver across Lagos, Abuja, and Kano. "
                "Used for bar charts (city comparison), histograms (delivery time distribution), "
                "scatter plots (distance vs time), box plots (per-city spread), and seaborn exercises."
            ),
            "columns": orders_columns,
            "rows": orders_rows,
            "provenance": "authored",
            "variants": [
                {
                    "variant_id": "ds.orders.messy",
                    "derived_from": "ds.orders",
                    "purpose": "Data-quality find_issues exercise: five planted issues covering missing value, impossible value, inconsistent category casing, duplicate row, and suspicious outlier.",
                    "ops": orders_messy_ops,
                    "planted_issues": orders_messy_planted,
                }
            ]
        },
        # ── 2. Daily averages dataset ────────────────────────────────────────
        {
            "asset_id": "ds.daily_averages",
            "asset_kind": "dataset",
            "scenario_id": "scen.da_viz_delivery",
            "title": "QuickDeliver daily average delivery times",
            "description": (
                "Average delivery time per day (Mon–Fri) for Lagos and Abuja. "
                "Used for line-plot exercises (plt.plot(x, y)) and labeling/legend exercises "
                "(ax.set_xlabel, ax.set_ylabel, ax.set_title, ax.legend). "
                "Lagos values match the glossary example: [21, 23, 19, 25, 20]."
            ),
            "columns": daily_columns,
            "rows": daily_rows,
            "provenance": "authored",
        },
        # ── 3. Chart-selection mini dataset ─────────────────────────────────
        {
            "asset_id": "ds.chart_selection_mini",
            "asset_kind": "dataset",
            "scenario_id": "scen.da_viz_delivery",
            "title": "QuickDeliver chart-selection mini dataset",
            "description": (
                "Six-row dataset with columns distance_km and delivery_minutes, "
                "matching the column names used in the chart_type_selection practice anchor. "
                "Used for the scatter-vs-bar chart-type selection exercise."
            ),
            "columns": chart_sel_columns,
            "rows": chart_sel_rows,
            "provenance": "authored",
        },
        # ── 4. Theming demo dataset ──────────────────────────────────────────
        {
            "asset_id": "ds.theming_demo",
            "asset_kind": "dataset",
            "scenario_id": "scen.da_viz_theming",
            "title": "QuickDeliver theming demo — category/value",
            "description": (
                "Minimal three-row dataset with 'category' and 'value' columns, "
                "matching the seaborn_themes_palettes practice anchor starter state. "
                "Used for sns.set_theme() and sns.set_palette() exercises."
            ),
            "columns": theme_columns,
            "rows": theme_rows,
            "provenance": "authored",
        },
        # ── 5. Code workspace: matplotlib/seaborn starter ───────────────────
        {
            "asset_id": "cw.viz_starter",
            "asset_kind": "code_workspace",
            "scenario_id": "scen.da_viz_delivery",
            "title": "Matplotlib / seaborn starter workspace",
            "runtime": "pyodide",
            "files": [
                {
                    "path": "orders.csv",
                    "content": (
                        "order_id,city,delivery_time_minutes,distance_km,order_value,num_items\n"
                        "1001,Lagos,18,2.1,1850.0,2\n"
                        "1002,Lagos,22,3.4,2200.0,3\n"
                        "1003,Lagos,19,2.8,1600.0,1\n"
                        "1004,Lagos,26,4.5,3100.0,4\n"
                        "1005,Lagos,30,5.2,2750.0,3\n"
                        "1006,Lagos,24,3.9,2400.0,2\n"
                        "1007,Lagos,28,4.8,3300.0,5\n"
                        "1008,Lagos,50,9.1,4800.0,6\n"
                        "1009,Abuja,25,3.2,2100.0,2\n"
                        "1010,Abuja,28,4.1,2600.0,3\n"
                        "1011,Abuja,23,3.0,1900.0,1\n"
                        "1012,Abuja,31,5.5,3400.0,4\n"
                        "1013,Abuja,27,4.3,2800.0,3\n"
                        "1014,Abuja,29,4.7,3000.0,2\n"
                        "1015,Abuja,26,4.0,2500.0,3\n"
                        "1016,Abuja,32,5.8,3600.0,5\n"
                        "1017,Kano,28,4.6,2300.0,2\n"
                        "1018,Kano,32,5.9,3100.0,4\n"
                        "1019,Kano,27,4.2,2000.0,2\n"
                        "1020,Kano,35,6.8,3800.0,5\n"
                        "1021,Kano,30,5.3,2700.0,3\n"
                        "1022,Kano,33,6.1,3400.0,4\n"
                        "1023,Kano,29,5.0,2600.0,3\n"
                        "1024,Kano,36,7.2,4100.0,6\n"
                    )
                },
                {
                    "path": "starter.py",
                    "content": (
                        "import matplotlib.pyplot as plt\n"
                        "import seaborn as sns\n"
                        "import pandas as pd\n"
                        "\n"
                        "orders = pd.read_csv('orders.csv')\n"
                        "\n"
                        "# delivery times for days 1-5 (week 1)\n"
                        "days = [1, 2, 3, 4, 5]\n"
                        "delivery_times = [18, 22, 26, 19, 30]\n"
                        "\n"
                        "# Lagos daily averages for days 1-5\n"
                        "lagos_avg = [21, 23, 19, 25, 20]\n"
                        "abuja_avg = [24, 26, 22, 28, 25]\n"
                    )
                }
            ]
        },
    ],
    "provenance": {
        "model": "claude-opus-4-5",
        "generated_at": "2026-11-03T15:29:12Z"
    }
}

# ── write ─────────────────────────────────────────────────────────────────────
out = BATCH / "scenario_asset_registry.json"
out.write_text(json.dumps(registry, indent=2, ensure_ascii=False))
print(f"Written: {out}")
print(f"Scenarios: {len(registry['scenarios'])}")
print(f"Assets: {len(registry['assets'])}")
for a in registry['assets']:
    kind = a['asset_kind']
    aid = a['asset_id']
    if kind == 'dataset':
        ncols = len(a['columns'])
        nrows = len(a.get('rows', []))
        nvars = len(a.get('variants', []))
        print(f"  {aid}: {ncols} cols, {nrows} rows, {nvars} variants")
    else:
        print(f"  {aid}: {kind}")
