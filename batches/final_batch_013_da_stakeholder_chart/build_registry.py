"""
Build script for scenario_asset_registry.json
Batch: final_batch_013_da_stakeholder_chart
Tile:  tile_stakeholder_chart_matching_simplifying
Concepts:
  - stakeholder.chart_type_to_point_matching
  - stakeholder.simplifying_charts_for_audience

Glossary vocabulary extracted from teaching blocks:
  Cities: Lagos, Abuja, Kano
  Domain: logistics / delivery operations (Nigeria)
  Columns: city, avg_delivery_minutes, week, order_count, distance_km
  Chart types: bar chart, line graph, boxplot, pie chart, scatterplot
  Clutter elements: border, gridlines, data labels, trailing zeros, rotated tick labels
"""

import json, pathlib

BATCH = pathlib.Path("batches/final_batch_013_da_stakeholder_chart")
OUT   = BATCH / "scenario_asset_registry.json"

# ── Scenario ──────────────────────────────────────────────────────────────────
# The glossary teaching blocks name Lagos, Abuja, Kano; an operations manager;
# delivery times; and weekly trends. We use a Nigerian logistics company scenario.

scenario = {
    "scenario_id": "scen_ng_logistics",
    "name": "SwiftMove Nigeria — City Delivery Operations",
    "summary": (
        "SwiftMove Nigeria is a fictional last-mile delivery company operating in "
        "Lagos, Abuja, and Kano. An operations manager wants to understand delivery "
        "performance across cities and over time. A data analyst prepares charts to "
        "communicate findings clearly to this non-technical audience."
    ),
    "locale": "en-NG",
    "currency": "NGN",
    "domain": "logistics",
    "glossary_example_vocab": [
        # cities named in teaching blocks
        "Lagos", "Abuja", "Kano",
        # roles named in teaching blocks
        "operations manager",
        # metrics named in teaching blocks
        "delivery time", "average delivery time", "delivery volume", "order count",
        # chart types named in teaching blocks
        "bar chart", "line graph", "boxplot", "pie chart", "scatterplot",
        # chart-simplification elements named in teaching blocks
        "gridlines", "border", "data labels", "trailing zeros",
        "rotated tick labels", "axis labels",
        # framing terms
        "part-to-whole", "comparison", "trend", "distribution",
        # specific example values named in teaching blocks
        "22.00 minutes", "22 min",
        # column names used in teaching blocks
        "avg_delivery_minutes", "week", "order_count", "distance_km",
    ],
}

# ── Dataset 1: city_delivery_summary ─────────────────────────────────────────
# Supports: bar chart (city comparison), pie chart (part-to-whole share),
#           boxplot (distribution comparison), classify interaction.
# Columns the glossary names: city, avg_delivery_minutes, order_count.
# We add share_pct so pie-chart part-to-whole sums to 100 %.
# order_count values: Lagos 3120, Abuja 1560, Kano 780 → total 5460
# share_pct: Lagos 57.1, Abuja 28.6, Kano 14.3  (sum = 100.0)

city_delivery_summary = {
    "asset_id": "ds_city_delivery_summary",
    "asset_kind": "dataset",
    "scenario_id": "scen_ng_logistics",
    "title": "City Delivery Summary",
    "description": (
        "One row per city. Captures average delivery time, total order count, "
        "and each city's share of total orders. Supports bar-chart (comparison), "
        "pie-chart (part-to-whole), and boxplot (distribution) exercises."
    ),
    "columns": [
        {
            "name": "city",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Delivery city name (Lagos, Abuja, Kano)"
        },
        {
            "name": "avg_delivery_minutes",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Average delivery time in minutes for the city"
        },
        {
            "name": "order_count",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "orders",
            "description": "Total number of orders fulfilled in the city"
        },
        {
            "name": "share_pct",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "percent",
            "description": "City's share of total orders (values sum to 100)"
        },
    ],
    # rows: [city, avg_delivery_minutes, order_count, share_pct]
    # Lagos 3120 / 5460 = 57.14…  → 57.1
    # Abuja 1560 / 5460 = 28.57…  → 28.6
    # Kano   780 / 5460 = 14.29…  → 14.3
    # sum = 100.0 ✓
    "rows": [
        ["Lagos",  38.4, 3120, 57.1],
        ["Abuja",  27.2, 1560, 28.6],
        ["Kano",   22.0,  780, 14.3],
    ],
    "variants": [
        {
            # Messy variant: introduces data-quality issues for find_issues exercises.
            # Issues:
            #   1. impossible_value: avg_delivery_minutes = -5.0 for Kano (negative time)
            #   2. inconsistent_category: city casing "lagos" (duplicate row with wrong case)
            #   3. missing_value: share_pct is null for Abuja
            #
            # Op sequence:
            #   op1: set Kano avg_delivery_minutes to -5.0
            #   op2: duplicate the Lagos row (insert at end)
            #   op3: set the duplicate Lagos row's city to "lagos" (occurrence=1)
            #   op4: set Abuja share_pct to null
            #
            # After ops the rows are:
            #   0: {city: Lagos,  avg_delivery_minutes: 38.4, order_count: 3120, share_pct: 57.1}
            #   1: {city: Abuja,  avg_delivery_minutes: 27.2, order_count: 1560, share_pct: null}
            #   2: {city: Kano,   avg_delivery_minutes: -5.0, order_count: 780,  share_pct: 14.3}
            #   3: {city: lagos,  avg_delivery_minutes: 38.4, order_count: 3120, share_pct: 57.1}
            #
            # casing_differs_from_siblings: "lagos" has sibling "Lagos" → rule holds ✓
            "variant_id": "ds_city_delivery_summary.messy",
            "derived_from": "ds_city_delivery_summary",
            "purpose": "find_issues practice — contains impossible value, inconsistent casing, and missing value",
            "ops": [
                # op 1: set Kano avg_delivery_minutes to -5.0 (impossible)
                {
                    "op": "set_cell",
                    "where": {"city": "Kano"},
                    "occurrence": 0,
                    "column": "avg_delivery_minutes",
                    "value": -5.0
                },
                # op 2: duplicate the Lagos row (insert at end) so "Lagos" still exists
                #        as a sibling when we rename the copy to "lagos"
                {
                    "op": "duplicate_row",
                    "where": {"city": "Lagos"},
                    "occurrence": 0,
                    "insert": "end"
                },
                # op 3: rename the duplicate (occurrence=1) to "lagos" (wrong casing)
                {
                    "op": "set_cell",
                    "where": {"city": "Lagos"},
                    "occurrence": 1,
                    "column": "city",
                    "value": "lagos"
                },
                # op 4: set Abuja share_pct to null (missing)
                {
                    "op": "set_cell",
                    "where": {"city": "Abuja"},
                    "occurrence": 0,
                    "column": "share_pct",
                    "value": None
                },
            ],
            "planted_issues": [
                {
                    "issue_id": "issue_impossible_delivery_time",
                    "kind": "impossible_value",
                    "locations": [
                        {
                            "where": {"city": "Kano"},
                            "occurrence": 0,
                            "column": "avg_delivery_minutes"
                        }
                    ],
                    "description": "avg_delivery_minutes is -5.0 for Kano — delivery time cannot be negative.",
                    "rule": {
                        "column": "avg_delivery_minutes",
                        "op": "lt",
                        "value": 0
                    }
                },
                {
                    "issue_id": "issue_city_casing",
                    "kind": "inconsistent_category",
                    "locations": [
                        {
                            "where": {"city": "lagos"},
                            "occurrence": 0,
                            "column": "city"
                        }
                    ],
                    "description": (
                        "City name 'lagos' uses lowercase; the sibling row 'Lagos' "
                        "uses title case — inconsistent category encoding."
                    ),
                    "rule": {
                        "column": "city",
                        "op": "casing_differs_from_siblings"
                    }
                },
                {
                    "issue_id": "issue_missing_share_pct",
                    "kind": "missing_value",
                    "locations": [
                        {
                            "where": {"city": "Abuja"},
                            "occurrence": 0,
                            "column": "share_pct"
                        }
                    ],
                    "description": "share_pct is null for Abuja — the part-to-whole percentage is missing."
                },
            ],
        }
    ],
    "provenance": "authored",
}

# ── Dataset 2: weekly_delivery_trend ─────────────────────────────────────────
# Supports: line graph (trend over time), scatterplot (distance vs time).
# Glossary names: "Lagos delivery time rising week over week",
#                 "distance/delivery-time relationship".
# Columns: week_number (integer label — numeric_looking_label=true),
#          city, avg_delivery_minutes, distance_km.
# 12 rows (4 weeks × 3 cities) — enough for trend and hidden checks.

weekly_delivery_trend = {
    "asset_id": "ds_weekly_delivery_trend",
    "asset_kind": "dataset",
    "scenario_id": "scen_ng_logistics",
    "title": "Weekly Delivery Trend by City",
    "description": (
        "One row per city per week. Captures average delivery time and average "
        "distance per delivery. Supports line-graph (trend) and scatterplot "
        "(distance vs. delivery-time relationship) exercises."
    ),
    "columns": [
        {
            "name": "week_number",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": (
                "Week identifier (1–4). A digit used as a label, not a quantity "
                "to aggregate — the misconception trap for numeric-looking labels."
            )
        },
        {
            "name": "city",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Delivery city name (Lagos, Abuja, Kano)"
        },
        {
            "name": "avg_delivery_minutes",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Average delivery time in minutes for that city-week"
        },
        {
            "name": "distance_km",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "km",
            "description": "Average delivery distance in kilometres for that city-week"
        },
    ],
    # Lagos trend: rising week over week (as stated in tb2 of concept 1)
    # Abuja and Kano: relatively stable
    # rows: [week_number, city, avg_delivery_minutes, distance_km]
    "rows": [
        [1, "Lagos", 34.0, 8.2],
        [1, "Abuja", 27.0, 6.1],
        [1, "Kano",  22.0, 4.8],
        [2, "Lagos", 36.5, 8.5],
        [2, "Abuja", 27.3, 6.0],
        [2, "Kano",  21.8, 4.9],
        [3, "Lagos", 38.1, 8.9],
        [3, "Abuja", 27.1, 6.2],
        [3, "Kano",  22.3, 4.7],
        [4, "Lagos", 40.2, 9.3],
        [4, "Abuja", 27.5, 6.1],
        [4, "Kano",  22.0, 4.8],
    ],
    "variants": [
        {
            # Messy variant: duplicate row + outlier for hidden-check robustness.
            # Issues:
            #   1. duplicate_row: week 2 Lagos row duplicated (appended at end)
            #   2. outlier_suspicious: week 3 Kano avg_delivery_minutes = 180.0
            #
            # After ops the rows are (13 total):
            #   0–11: original rows with week3 Kano changed to 180.0
            #   12:   duplicate of week2 Lagos (appended)
            "variant_id": "ds_weekly_delivery_trend.messy",
            "derived_from": "ds_weekly_delivery_trend",
            "purpose": "find_issues practice — contains a duplicate row and a suspicious outlier",
            "ops": [
                # op 1: duplicate the week 2 Lagos row (insert at end)
                {
                    "op": "duplicate_row",
                    "where": {"week_number": 2, "city": "Lagos"},
                    "occurrence": 0,
                    "insert": "end"
                },
                # op 2: set week 3 Kano avg_delivery_minutes to 180.0 (outlier)
                {
                    "op": "set_cell",
                    "where": {"week_number": 3, "city": "Kano"},
                    "occurrence": 0,
                    "column": "avg_delivery_minutes",
                    "value": 180.0
                },
            ],
            "planted_issues": [
                {
                    # The duplicate is at occurrence=1 (the appended copy).
                    # Both occurrence=0 and occurrence=1 have an identical sibling,
                    # so the checker passes for either; we use occurrence=1 to point
                    # explicitly to the inserted copy.
                    "issue_id": "issue_duplicate_lagos_week2",
                    "kind": "duplicate_row",
                    "locations": [
                        {
                            "where": {"week_number": 2, "city": "Lagos"},
                            "occurrence": 1,
                            "column": "city"
                        }
                    ],
                    "description": (
                        "The week 2 Lagos row appears twice — a duplicate that would "
                        "inflate any aggregate computed over this city-week."
                    )
                },
                {
                    "issue_id": "issue_outlier_kano_week3",
                    "kind": "outlier_suspicious",
                    "locations": [
                        {
                            "where": {"week_number": 3, "city": "Kano"},
                            "occurrence": 0,
                            "column": "avg_delivery_minutes"
                        }
                    ],
                    "description": (
                        "avg_delivery_minutes is 180.0 for Kano week 3 — three hours, "
                        "far above the 20–40 min range of all other rows."
                    ),
                    "rule": {
                        "column": "avg_delivery_minutes",
                        "op": "gt",
                        "value": 100
                    }
                },
            ],
        }
    ],
    "provenance": "authored",
}

# ── Registry ──────────────────────────────────────────────────────────────────

registry = {
    "schema_version": "1.0.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_013_da_stakeholder_chart",
    "scenarios": [scenario],
    "assets": [city_delivery_summary, weekly_delivery_trend],
    "provenance": {
        "model": "claude-opus-4-5",
        "generated_at": "2026-11-05T15:12:08Z"
    },
}

OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False))
print(f"Written: {OUT}")
print(f"Scenarios: {len(registry['scenarios'])}")
print(f"Assets:    {len(registry['assets'])}")
for a in registry['assets']:
    print(f"  {a['asset_id']} ({a['asset_kind']}) — {len(a.get('rows', []))} rows, "
          f"{len(a.get('columns', []))} cols, "
          f"{len(a.get('variants', []))} variants")
