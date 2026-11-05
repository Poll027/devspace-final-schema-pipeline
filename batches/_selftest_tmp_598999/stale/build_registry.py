"""
Build script for scenario_asset_registry.json — batch final_batch_009_da_pandas.
Run from pack root: python3 batches/final_batch_009_da_pandas/build_registry.py
"""
import json, sys
from pathlib import Path

BATCH = Path("batches/final_batch_009_da_pandas")
OUT   = BATCH / "scenario_asset_registry.json"

# ── helpers ──────────────────────────────────────────────────────────────────
def row(*vals):
    return list(vals)

# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO
# One scenario covers the whole pandas batch: a Lagos-based last-mile delivery
# company whose analysts wrangle order data in Python/pandas.  All column names,
# city names, order_ids, courier names, and numeric values are taken verbatim
# from the glossary's teaching blocks.
# ─────────────────────────────────────────────────────────────────────────────
scenarios = [
    {
        "scenario_id": "scen_swiftdrop",
        "name": "SwiftDrop Delivery Analytics",
        "summary": (
            "SwiftDrop is a fictional last-mile delivery company operating across Lagos, "
            "Abuja, and Kano, Nigeria. Analysts use Python/pandas to clean, reshape, and "
            "summarise order data exported from the dispatch system. The scenario provides "
            "a consistent set of tables — orders, drivers, customers, and monthly delivery "
            "summaries — that recur across all pandas tiles in this batch."
        ),
        "locale": "en-NG",
        "currency": "NGN",
        "domain": "logistics / last-mile delivery",
        "glossary_example_vocab": [
            # column names used in teaching blocks
            "order_id", "city", "delivery_time_minutes", "courier",
            "driver_id", "customer_id", "distance_km", "pickup_date",
            "pickup_month", "city_code", "speed_label", "order_value",
            # city / person names used in teaching blocks
            "Lagos", "Abuja", "Kano",
            "Ada", "Bayo", "Chidi",
            # city codes used in map_substitution teaching block
            "LOS", "ABJ", "KAN",
            # file names used in teaching blocks
            "orders.csv", "orders.xlsx", "cleaned_orders.csv",
            # DataFrame variable names used in teaching blocks
            "orders", "drivers", "customers",
            "jan_orders", "feb_orders", "mar_orders",
            "city_deliveries", "long_deliveries",
            # month column values used in melt/pivot teaching blocks
            "jan_deliveries", "feb_deliveries", "mar_deliveries",
            # speed labels used in apply_transform teaching block
            "fast", "slow",
            # stats values from descriptive_stats teaching block
            "mean ~30.9", "median 22", "std ~21.9",
        ],
    }
]

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 1 — orders (main table)
# Covers: dataframe_series_model, reading_data, creating_dataframes,
#         inspecting_dataframes, descriptive_stats, loc_iloc_selection,
#         boolean_filtering, sort_values, rename_columns_index,
#         dtype_conversion, datetime_handling, str_accessor_cleaning,
#         missing_data_handling, map_substitution, apply_transform,
#         groupby_aggregation, export_to_csv
#
# Glossary pins:
#   order_id values: 1001, 1002, 1003 (and more for hidden tests)
#   city values: Lagos, Abuja, Kano
#   delivery_time_minutes: 18, 20, 22, 22, 26, 28, 80 (the 7-value batch)
#   courier: Ada, Bayo, Chidi (and more)
#   pickup_date: ISO date strings (2024-03-14 style)
#   distance_km: stored as string in messy variant (dtype_conversion concept)
#   city_code: LOS, ABJ, KAN (map_substitution concept)
#   order_value: numeric (groupby_aggregation concept)
# ─────────────────────────────────────────────────────────────────────────────
orders_columns = [
    {"name": "order_id",               "type": "integer", "semantic_role": "identifier",
     "numeric_looking_label": True,
     "description": "Unique dispatch order number (1001, 1002, …) — numeric-looking label, not a quantity"},
    {"name": "city",                   "type": "string",  "semantic_role": "categorical",
     "description": "Destination city: Lagos, Abuja, or Kano"},
    {"name": "city_code",              "type": "string",  "semantic_role": "categorical",
     "description": "Three-letter city code used in map_substitution examples: LOS, ABJ, KAN"},
    {"name": "courier",                "type": "string",  "semantic_role": "categorical",
     "description": "Courier name (Ada, Bayo, Chidi, …)"},
    {"name": "driver_id",              "type": "integer", "semantic_role": "identifier",
     "numeric_looking_label": True,
     "description": "Driver identifier — numeric-looking label, not a quantity"},
    {"name": "customer_id",            "type": "integer", "semantic_role": "identifier",
     "numeric_looking_label": True,
     "description": "Customer identifier — numeric-looking label, not a quantity"},
    {"name": "pickup_date",            "type": "date",    "semantic_role": "datetime",
     "description": "ISO date string of order pickup (2024-03-14 style); converted with pd.to_datetime()"},
    {"name": "delivery_time_minutes",  "type": "integer", "semantic_role": "numerical",
     "unit": "minutes",
     "description": "Minutes from pickup to delivery; the 7-value batch [18,20,22,22,26,28,80] is used in descriptive-stats examples"},
    {"name": "distance_km",            "type": "number",  "semantic_role": "numerical",
     "unit": "km",
     "description": "Route distance in kilometres"},
    {"name": "order_value",            "type": "number",  "semantic_role": "numerical",
     "unit": "NGN",
     "description": "Order value in Naira; used in groupby_aggregation examples"},
]

# 14 rows — enough for hidden tests to distinguish correct from lazy answers.
# The first 7 rows reproduce the exact delivery_time_minutes sequence from the
# descriptive-stats teaching block: [18, 20, 22, 22, 26, 28, 80].
# order_id, city, city_code, courier, driver_id, customer_id, pickup_date, delivery_time_minutes, distance_km, order_value
orders_rows = [
    row(1001, "Lagos", "LOS", "Ada",   201, 301, "2024-03-14", 18, 4.2,  2500),
    row(1002, "Abuja", "ABJ", "Bayo",  202, 302, "2024-03-14", 20, 6.1,  3100),
    row(1003, "Kano",  "KAN", "Chidi", 203, 303, "2024-03-15", 22, 5.5,  1800),
    row(1004, "Lagos", "LOS", "Ada",   201, 304, "2024-03-15", 22, 3.8,  2200),
    row(1005, "Abuja", "ABJ", "Bayo",  202, 305, "2024-03-16", 26, 7.3,  4000),
    row(1006, "Kano",  "KAN", "Chidi", 203, 306, "2024-03-16", 28, 8.0,  1500),
    row(1007, "Lagos", "LOS", "Ada",   201, 307, "2024-03-17", 80, 12.4, 5500),
    row(1008, "Abuja", "ABJ", "Bayo",  202, 308, "2024-03-17", 31, 9.2,  3800),
    row(1009, "Kano",  "KAN", "Chidi", 203, 309, "2024-03-18", 19, 4.9,  2100),
    row(1010, "Lagos", "LOS", "Ada",   201, 310, "2024-03-18", 24, 5.1,  2900),
    row(1011, "Abuja", "ABJ", "Bayo",  202, 311, "2024-03-19", 33, 10.0, 4200),
    row(1012, "Kano",  "KAN", "Chidi", 203, 312, "2024-03-19", 21, 4.4,  1700),
    row(1013, "Lagos", "LOS", "Ada",   201, 313, "2024-03-20", 27, 6.6,  3300),
    row(1014, "Abuja", "ABJ", "Bayo",  202, 314, "2024-03-20", 35, 11.1, 4600),
]

# ── Variant: messy_orders ────────────────────────────────────────────────────
# Used by: str_accessor_cleaning, dtype_conversion, missing_data_handling,
#          drop_duplicates, find_issues interactions.
# Planted issues:
#   iss_city_case   — " lagos" (leading space + lowercase) in row order_id=1004
#   iss_city_upper  — "LAGOS " (uppercase + trailing space) in row order_id=1007
#   iss_dist_string — distance_km stored as string "bad_value" in row order_id=1005
#   iss_missing_dt  — delivery_time_minutes is null in row order_id=1008
#   iss_duplicate   — order_id=1003 row duplicated (duplicate_row op)
#
# NOTE: set_cell ops use the BASE row values as the `where` predicate.
# After duplicate_row for 1003, there will be two identical rows for 1003;
# the planted_issue occurrence=1 points to the second copy.

orders_variants = [
    {
        "variant_id": "orders_messy",
        "derived_from": "ds_orders",
        "purpose": "Messy version for cleaning exercises: mixed-case city values, a distance stored as a non-numeric string, a missing delivery time, and a duplicate order row.",
        "ops": [
            # 1. Corrupt city in row 1004 → " lagos" (leading space, lowercase)
            {
                "op": "set_cell",
                "where": {"order_id": 1004},
                "occurrence": 0,
                "column": "city",
                "value": " lagos"
            },
            # 2. Corrupt city in row 1007 → "LAGOS " (uppercase, trailing space)
            {
                "op": "set_cell",
                "where": {"order_id": 1007},
                "occurrence": 0,
                "column": "city",
                "value": "LAGOS "
            },
            # 3. Corrupt distance_km in row 1005 → non-numeric string
            {
                "op": "set_cell",
                "where": {"order_id": 1005},
                "occurrence": 0,
                "column": "distance_km",
                "value": "unknown"
            },
            # 4. Set delivery_time_minutes to null in row 1008
            {
                "op": "set_cell",
                "where": {"order_id": 1008},
                "occurrence": 0,
                "column": "delivery_time_minutes",
                "value": None
            },
            # 5. Duplicate row 1003 (appended at end)
            {
                "op": "duplicate_row",
                "where": {"order_id": 1003},
                "occurrence": 0,
                "insert": "end"
            }
        ],
        "planted_issues": [
            {
                "issue_id": "iss_city_case_1004",
                "kind": "inconsistent_category",
                "description": "City value ' lagos' has a leading space and is lowercase; siblings are title-cased without spaces.",
                "locations": [
                    {"where": {"order_id": 1004}, "occurrence": 0, "column": "city"}
                ],
                "rule": {"column": "city", "op": "casing_differs_from_siblings"}
            },
            {
                "issue_id": "iss_city_case_1007",
                "kind": "inconsistent_category",
                "description": "City value 'LAGOS ' is uppercase with a trailing space; siblings are title-cased without spaces.",
                "locations": [
                    {"where": {"order_id": 1007}, "occurrence": 0, "column": "city"}
                ],
                "rule": {"column": "city", "op": "casing_differs_from_siblings"}
            },
            {
                "issue_id": "iss_dist_string",
                "kind": "wrong_type",
                "description": "distance_km holds the string 'unknown' instead of a numeric value; astype(float) would raise an exception here.",
                "locations": [
                    {"where": {"order_id": 1005}, "occurrence": 0, "column": "distance_km"}
                ],
                "rule": {"column": "distance_km", "op": "eq", "value": "unknown"}
            },
            {
                "issue_id": "iss_missing_dt",
                "kind": "missing_value",
                "description": "delivery_time_minutes is null for order 1008; detected by isna().",
                "locations": [
                    {"where": {"order_id": 1008}, "occurrence": 0, "column": "delivery_time_minutes"}
                ],
                "rule": {"column": "delivery_time_minutes", "op": "is_null"}
            },
            {
                "issue_id": "iss_duplicate_1003",
                "kind": "duplicate_row",
                "description": "Order 1003 appears twice (identical rows); drop_duplicates(subset=['order_id']) removes the second copy.",
                "locations": [
                    {"where": {"order_id": 1003}, "occurrence": 0, "column": "order_id"},
                    {"where": {"order_id": 1003}, "occurrence": 1, "column": "order_id"}
                ]
            }
        ]
    }
]

ds_orders = {
    "asset_id":    "ds_orders",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "SwiftDrop Orders",
    "description": (
        "One row per delivery order. Columns match the names used in all pandas "
        "teaching blocks: order_id, city, city_code, courier, driver_id, customer_id, "
        "pickup_date, delivery_time_minutes, distance_km, order_value. "
        "The first 7 rows reproduce the exact delivery_time_minutes sequence "
        "[18, 20, 22, 22, 26, 28, 80] from the descriptive-stats teaching block."
    ),
    "columns":     orders_columns,
    "rows":        orders_rows,
    "variants":    orders_variants,
    "provenance":  "authored",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 2 — drivers
# Covers: merge_join (orders.merge(drivers, on="driver_id"))
# Glossary pins: driver_id shared key; one unmatched driver_id on each side
# ─────────────────────────────────────────────────────────────────────────────
drivers_columns = [
    {"name": "driver_id",   "type": "integer", "semantic_role": "identifier",
     "numeric_looking_label": True,
     "description": "Driver identifier — matches driver_id in orders table"},
    {"name": "driver_name", "type": "string",  "semantic_role": "categorical",
     "description": "Full name of the driver"},
    {"name": "vehicle",     "type": "string",  "semantic_role": "categorical",
     "description": "Vehicle type: Motorcycle or Van"},
    {"name": "base_city",   "type": "string",  "semantic_role": "categorical",
     "description": "City where the driver is based"},
]

# driver_id 204 is in drivers but NOT in orders → unmatched on right side
# driver_id 203 is in orders but also in drivers → matched
# driver_id 201, 202, 203 appear in orders; 204 is extra in drivers
drivers_rows = [
    row(201, "Ada Okafor",    "Motorcycle", "Lagos"),
    row(202, "Bayo Adeyemi",  "Van",        "Abuja"),
    row(203, "Chidi Okonkwo", "Motorcycle", "Kano"),
    row(204, "Dami Fashola",  "Van",        "Lagos"),   # not in orders → NA on left join
]

ds_drivers = {
    "asset_id":    "ds_drivers",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "SwiftDrop Drivers",
    "description": (
        "Driver reference table. Shares driver_id with ds_orders. "
        "driver_id 204 exists here but not in orders (unmatched on right side of a left join). "
        "Used in merge_join teaching block: orders.merge(drivers, on='driver_id')."
    ),
    "columns":  drivers_columns,
    "rows":     drivers_rows,
    "provenance": "authored",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 3 — customers
# Covers: merge_join (orders.merge(customers, on="customer_id"))
#         groupby_aggregation starter mentions customer_id + order_value
# Glossary pins: customer_id shared key; unmatched IDs on each side
# ─────────────────────────────────────────────────────────────────────────────
customers_columns = [
    {"name": "customer_id",   "type": "integer", "semantic_role": "identifier",
     "numeric_looking_label": True,
     "description": "Customer identifier — matches customer_id in orders table"},
    {"name": "customer_name", "type": "string",  "semantic_role": "categorical",
     "description": "Customer full name"},
    {"name": "segment",       "type": "string",  "semantic_role": "categorical",
     "description": "Customer segment: Individual or Business"},
    {"name": "signup_date",   "type": "date",    "semantic_role": "datetime",
     "description": "Date the customer registered"},
]

# customer_id 315 is in customers but NOT in orders → unmatched on right side
# customer_ids 301-314 are in orders; 315 is extra in customers
customers_rows = [
    row(301, "Ngozi Eze",       "Individual", "2023-01-10"),
    row(302, "Emeka Obi",       "Business",   "2023-02-14"),
    row(303, "Fatima Musa",     "Individual", "2023-03-05"),
    row(304, "Tunde Bakare",    "Business",   "2023-04-20"),
    row(305, "Amaka Nwosu",     "Individual", "2023-05-11"),
    row(306, "Yusuf Garba",     "Business",   "2023-06-01"),
    row(307, "Chisom Ike",      "Individual", "2023-07-18"),
    row(308, "Bisi Adewale",    "Business",   "2023-08-09"),
    row(309, "Halima Sule",     "Individual", "2023-09-22"),
    row(310, "Rotimi Coker",    "Business",   "2023-10-03"),
    row(311, "Nkechi Okafor",   "Individual", "2023-11-15"),
    row(312, "Musa Ibrahim",    "Business",   "2023-12-07"),
    row(313, "Adaeze Chukwu",   "Individual", "2024-01-19"),
    row(314, "Segun Afolabi",   "Business",   "2024-02-28"),
    row(315, "Zainab Aliyu",    "Individual", "2024-03-12"),  # not in orders → NA on left join
]

ds_customers = {
    "asset_id":    "ds_customers",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "SwiftDrop Customers",
    "description": (
        "Customer reference table. Shares customer_id with ds_orders. "
        "customer_id 315 exists here but not in orders (unmatched on right side). "
        "Used in merge_join practice: orders.merge(customers, on='customer_id')."
    ),
    "columns":  customers_columns,
    "rows":     customers_rows,
    "provenance": "authored",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 4 — monthly_deliveries_wide (city_deliveries)
# Covers: melt_reshaping, pivot_table_reshaping
# Glossary pins:
#   columns: city, jan_deliveries, feb_deliveries, mar_deliveries
#   melt id_vars=["city"], var_name="month", value_name="deliveries"
#   pivot_table(index="city", columns="month", values="deliveries")
# ─────────────────────────────────────────────────────────────────────────────
wide_columns = [
    {"name": "city",            "type": "string",  "semantic_role": "categorical",
     "description": "Destination city"},
    {"name": "jan_deliveries",  "type": "integer", "semantic_role": "numerical",
     "unit": "orders",
     "description": "Number of deliveries completed in January"},
    {"name": "feb_deliveries",  "type": "integer", "semantic_role": "numerical",
     "unit": "orders",
     "description": "Number of deliveries completed in February"},
    {"name": "mar_deliveries",  "type": "integer", "semantic_role": "numerical",
     "unit": "orders",
     "description": "Number of deliveries completed in March"},
]

wide_rows = [
    row("Lagos", 142, 138, 155),
    row("Abuja",  98, 104, 110),
    row("Kano",   76,  81,  88),
]

ds_wide = {
    "asset_id":    "ds_monthly_wide",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "Monthly Deliveries by City (Wide)",
    "description": (
        "One row per city, one column per month (jan_deliveries, feb_deliveries, mar_deliveries). "
        "Used in melt_reshaping teaching block as city_deliveries. "
        "melt(id_vars=['city'], var_name='month', value_name='deliveries') produces ds_monthly_long."
    ),
    "columns":  wide_columns,
    "rows":     wide_rows,
    "provenance": "authored",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 5 — monthly_deliveries_long (long_deliveries)
# Covers: pivot_table_reshaping (the long → wide direction)
# Glossary pins:
#   columns: city, month, deliveries
#   pivot_table(index="city", columns="month", values="deliveries")
#   Some city-month pairs repeat (aggfunc='sum' vs 'mean' distinction)
# ─────────────────────────────────────────────────────────────────────────────
long_columns = [
    {"name": "city",       "type": "string",  "semantic_role": "categorical",
     "description": "Destination city"},
    {"name": "month",      "type": "string",  "semantic_role": "categorical",
     "description": "Month label: jan_deliveries, feb_deliveries, or mar_deliveries"},
    {"name": "deliveries", "type": "integer", "semantic_role": "numerical",
     "unit": "orders",
     "description": "Number of deliveries for this city-month combination"},
]

# 9 base rows (one per city × month) + 3 duplicate city-month rows so that
# aggfunc='sum' vs 'mean' gives different results — the pivot_table teaching
# block explicitly says "if a city had two rows for the same month, the default
# call would average them instead of erroring".
long_rows = [
    row("Lagos", "jan_deliveries",  142),
    row("Lagos", "feb_deliveries",  138),
    row("Lagos", "mar_deliveries",  155),
    row("Abuja", "jan_deliveries",   98),
    row("Abuja", "feb_deliveries",  104),
    row("Abuja", "mar_deliveries",  110),
    row("Kano",  "jan_deliveries",   76),
    row("Kano",  "feb_deliveries",   81),
    row("Kano",  "mar_deliveries",   88),
    # duplicate Lagos-jan row so aggfunc matters
    row("Lagos", "jan_deliveries",   18),
]

ds_long = {
    "asset_id":    "ds_monthly_long",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "Monthly Deliveries by City (Long)",
    "description": (
        "One row per city-month combination (city, month, deliveries). "
        "Used in pivot_table_reshaping teaching block as long_deliveries. "
        "Contains a duplicate Lagos-jan row so that aggfunc='sum' and aggfunc='mean' "
        "give different results, preventing a hard-coded answer from passing."
    ),
    "columns":  long_columns,
    "rows":     long_rows,
    "provenance": "authored",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 6 — product_sales_long
# Covers: pivot_table_reshaping practice starter
# Glossary pins: "product, month and sales columns where some product-month pairs repeat"
# ─────────────────────────────────────────────────────────────────────────────
product_columns = [
    {"name": "product", "type": "string",  "semantic_role": "categorical",
     "description": "Product name"},
    {"name": "month",   "type": "string",  "semantic_role": "categorical",
     "description": "Month label (Jan, Feb, Mar)"},
    {"name": "sales",   "type": "number",  "semantic_role": "numerical",
     "unit": "NGN",
     "description": "Sales amount in Naira"},
]

# Some product-month pairs repeat (as required by the practice starter)
product_rows = [
    row("Envelope",  "Jan",  4500),
    row("Envelope",  "Jan",  3200),   # duplicate product-month
    row("Envelope",  "Feb",  5100),
    row("Envelope",  "Mar",  4800),
    row("Parcel",    "Jan",  8200),
    row("Parcel",    "Feb",  7600),
    row("Parcel",    "Feb",  9100),   # duplicate product-month
    row("Parcel",    "Mar",  8800),
    row("Document",  "Jan",  2100),
    row("Document",  "Feb",  2400),
    row("Document",  "Mar",  2300),
    row("Document",  "Mar",  1900),   # duplicate product-month
]

ds_product = {
    "asset_id":    "ds_product_sales",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "Product Sales by Month (Long)",
    "description": (
        "Long-format sales table with product, month, and sales columns. "
        "Several product-month pairs repeat so that pivot_table aggfunc='sum' "
        "and aggfunc='mean' give different results. "
        "Used in pivot_table_reshaping practice."
    ),
    "columns":  product_columns,
    "rows":     product_rows,
    "provenance": "authored",
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 7 — jan_orders / feb_orders / mar_orders (concat_stacking)
# Glossary pins: "January, February, and March deliveries each live in their
#   own DataFrame with identical columns"
# Three separate datasets with identical columns; concat stacks them.
# ─────────────────────────────────────────────────────────────────────────────
monthly_cols = [
    {"name": "order_id",              "type": "integer", "semantic_role": "identifier",
     "numeric_looking_label": True},
    {"name": "city",                  "type": "string",  "semantic_role": "categorical"},
    {"name": "courier",               "type": "string",  "semantic_role": "categorical"},
    {"name": "delivery_time_minutes", "type": "integer", "semantic_role": "numerical",
     "unit": "minutes"},
    {"name": "order_value",           "type": "number",  "semantic_role": "numerical",
     "unit": "NGN"},
]

ds_jan = {
    "asset_id":    "ds_jan_orders",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "January Orders",
    "description": "January delivery orders — identical columns to ds_feb_orders and ds_mar_orders. Used in concat_stacking teaching block as jan_orders.",
    "columns":  monthly_cols,
    "rows": [
        row(2001, "Lagos", "Ada",   18, 2500),
        row(2002, "Abuja", "Bayo",  22, 3100),
        row(2003, "Kano",  "Chidi", 26, 1800),
        row(2004, "Lagos", "Ada",   31, 2900),
        row(2005, "Abuja", "Bayo",  19, 3400),
    ],
    "provenance": "authored",
}

ds_feb = {
    "asset_id":    "ds_feb_orders",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "February Orders",
    "description": "February delivery orders — identical columns to ds_jan_orders and ds_mar_orders. Used in concat_stacking teaching block as feb_orders.",
    "columns":  monthly_cols,
    "rows": [
        row(2006, "Lagos", "Ada",   20, 2700),
        row(2007, "Abuja", "Bayo",  28, 4000),
        row(2008, "Kano",  "Chidi", 24, 1600),
        row(2009, "Lagos", "Ada",   35, 5100),
        row(2010, "Kano",  "Chidi", 21, 2000),
    ],
    "provenance": "authored",
}

ds_mar = {
    "asset_id":    "ds_mar_orders",
    "asset_kind":  "dataset",
    "scenario_id": "scen_swiftdrop",
    "title":       "March Orders",
    "description": "March delivery orders — identical columns to ds_jan_orders and ds_feb_orders. Used in concat_stacking teaching block as mar_orders.",
    "columns":  monthly_cols,
    "rows": [
        row(2011, "Lagos", "Ada",   22, 2600),
        row(2012, "Abuja", "Bayo",  30, 3700),
        row(2013, "Kano",  "Chidi", 27, 1900),
        row(2014, "Lagos", "Ada",   80, 5500),
        row(2015, "Abuja", "Bayo",  23, 3200),
    ],
    "provenance": "authored",
}

# ─────────────────────────────────────────────────────────────────────────────
# CODE WORKSPACES
# One per tile that has a live_code practice anchor.
# File names match the glossary's practice starter descriptions.
# ─────────────────────────────────────────────────────────────────────────────

cw_series_df = {
    "asset_id":    "cw_series_dataframe",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "Series and DataFrame Construction Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "# A list of delivery times (minutes)\n"
                "# delivery_times = [18, 20, 22, 22, 26, 28, 80]\n\n"
                "# A dict of equal-length lists for an orders table\n"
                "# data = {\n"
                "#     'order_id': [1001, 1002, 1003],\n"
                "#     'city': ['Lagos', 'Abuja', 'Kano'],\n"
                "#     'delivery_time_minutes': [18, 20, 26]\n"
                "# }\n\n"
                "# TODO: build a Series from delivery_times\n"
                "# TODO: build a DataFrame from data\n"
                "# TODO: pull out the 'city' column and print its type\n"
            )
        }
    ]
}

cw_reading = {
    "asset_id":    "cw_reading_data",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "Reading Data Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "# The orders CSV is available at: 'orders.csv'\n"
                "# orders = pd.read_csv('orders.csv')\n\n"
                "# TODO: read orders.csv into a DataFrame called orders\n"
                "# TODO: print the DataFrame\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,city_code,courier,driver_id,customer_id,"
                "pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,ABJ,Bayo,202,302,2024-03-14,20,6.1,3100\n"
                "1003,Kano,KAN,Chidi,203,303,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,LOS,Ada,201,304,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,ABJ,Bayo,202,305,2024-03-16,26,7.3,4000\n"
                "1006,Kano,KAN,Chidi,203,306,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,LOS,Ada,201,307,2024-03-17,80,12.4,5500\n"
                "1008,Abuja,ABJ,Bayo,202,308,2024-03-17,31,9.2,3800\n"
                "1009,Kano,KAN,Chidi,203,309,2024-03-18,19,4.9,2100\n"
                "1010,Lagos,LOS,Ada,201,310,2024-03-18,24,5.1,2900\n"
                "1011,Abuja,ABJ,Bayo,202,311,2024-03-19,33,10.0,4200\n"
                "1012,Kano,KAN,Chidi,203,312,2024-03-19,21,4.4,1700\n"
                "1013,Lagos,LOS,Ada,201,313,2024-03-20,27,6.6,3300\n"
                "1014,Abuja,ABJ,Bayo,202,314,2024-03-20,35,11.1,4600\n"
            )
        }
    ]
}

cw_creating = {
    "asset_id":    "cw_creating_dataframes",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "Creating DataFrames Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "# Build the same orders table two ways:\n\n"
                "# Way 1 — dict of equal-length lists\n"
                "# data_dict = {\n"
                "#     'order_id': [1001, 1002, 1003],\n"
                "#     'city': ['Lagos', 'Abuja', 'Kano'],\n"
                "#     'delivery_time_minutes': [18, 20, 26]\n"
                "# }\n\n"
                "# Way 2 — list of dicts (one dict per row)\n"
                "# data_list = [\n"
                "#     {'order_id': 1001, 'city': 'Lagos', 'delivery_time_minutes': 18},\n"
                "#     {'order_id': 1002, 'city': 'Abuja', 'delivery_time_minutes': 20},\n"
                "#     {'order_id': 1003, 'city': 'Kano',  'delivery_time_minutes': 26},\n"
                "# ]\n\n"
                "# TODO: build a DataFrame from data_dict and print it\n"
                "# TODO: build a DataFrame from data_list and print it\n"
            )
        }
    ]
}

cw_inspecting = {
    "asset_id":    "cw_inspecting_dataframes",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "Inspecting DataFrames Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders.csv')\n\n"
                "# TODO: show the first 5 rows\n"
                "# TODO: print the shape\n"
                "# TODO: print the dtypes\n"
                "# TODO: call info()\n"
                "# TODO: call describe()\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,city_code,courier,driver_id,customer_id,"
                "pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,ABJ,Bayo,202,302,2024-03-14,20,6.1,3100\n"
                "1003,Kano,KAN,Chidi,203,303,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,LOS,Ada,201,304,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,ABJ,Bayo,202,305,2024-03-16,26,7.3,4000\n"
                "1006,Kano,KAN,Chidi,203,306,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,LOS,Ada,201,307,2024-03-17,80,12.4,5500\n"
                "1008,Abuja,ABJ,Bayo,202,308,2024-03-17,31,9.2,3800\n"
                "1009,Kano,KAN,Chidi,203,309,2024-03-18,19,4.9,2100\n"
                "1010,Lagos,LOS,Ada,201,310,2024-03-18,24,5.1,2900\n"
                "1011,Abuja,ABJ,Bayo,202,311,2024-03-19,33,10.0,4200\n"
                "1012,Kano,KAN,Chidi,203,312,2024-03-19,21,4.4,1700\n"
                "1013,Lagos,LOS,Ada,201,313,2024-03-20,27,6.6,3300\n"
                "1014,Abuja,ABJ,Bayo,202,314,2024-03-20,35,11.1,4600\n"
            )
        }
    ]
}

cw_stats = {
    "asset_id":    "cw_descriptive_stats",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "Descriptive Statistics Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders.csv')\n\n"
                "# delivery_time_minutes holds [18, 20, 22, 22, 26, 28, 80]\n"
                "# mean ≈ 30.9, median = 22, std ≈ 21.9\n\n"
                "# TODO: compute mean, median, std of delivery_time_minutes\n"
                "# TODO: call describe() on the column\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,city_code,courier,driver_id,customer_id,"
                "pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,ABJ,Bayo,202,302,2024-03-14,20,6.1,3100\n"
                "1003,Kano,KAN,Chidi,203,303,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,LOS,Ada,201,304,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,ABJ,Bayo,202,305,2024-03-16,26,7.3,4000\n"
                "1006,Kano,KAN,Chidi,203,306,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,LOS,Ada,201,307,2024-03-17,80,12.4,5500\n"
            )
        }
    ]
}

cw_loc_iloc = {
    "asset_id":    "cw_loc_iloc_selection",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "loc and iloc Selection Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders.csv')\n\n"
                "# orders has default integer row labels 0, 1, 2, ...\n"
                "# Columns: order_id, city, city_code, courier, driver_id,\n"
                "#          customer_id, pickup_date, delivery_time_minutes,\n"
                "#          distance_km, order_value\n\n"
                "# TODO: use .loc to select the 'city' column for rows labeled 2 through 4\n"
                "# TODO: use .iloc to select the first 3 rows and first 2 columns\n"
                "# TODO: note the boundary difference: loc[2:4] gives 3 rows, iloc[0:3] gives 3 rows\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,city_code,courier,driver_id,customer_id,"
                "pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,ABJ,Bayo,202,302,2024-03-14,20,6.1,3100\n"
                "1003,Kano,KAN,Chidi,203,303,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,LOS,Ada,201,304,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,ABJ,Bayo,202,305,2024-03-16,26,7.3,4000\n"
                "1006,Kano,KAN,Chidi,203,306,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,LOS,Ada,201,307,2024-03-17,80,12.4,5500\n"
                "1008,Abuja,ABJ,Bayo,202,308,2024-03-17,31,9.2,3800\n"
                "1009,Kano,KAN,Chidi,203,309,2024-03-18,19,4.9,2100\n"
                "1010,Lagos,LOS,Ada,201,310,2024-03-18,24,5.1,2900\n"
            )
        }
    ]
}

cw_bool_filter = {
    "asset_id":    "cw_boolean_filtering",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "Boolean Filtering Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders.csv')\n\n"
                "# Threshold: delivery_time_minutes > 25 means 'slow'\n\n"
                "# TODO: filter to keep only orders where delivery_time_minutes > 25\n"
                "# TODO: filter to keep Lagos orders where delivery_time_minutes > 25\n"
                "#       (remember to wrap each condition in parentheses)\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,city_code,courier,driver_id,customer_id,"
                "pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,ABJ,Bayo,202,302,2024-03-14,20,6.1,3100\n"
                "1003,Kano,KAN,Chidi,203,303,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,LOS,Ada,201,304,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,ABJ,Bayo,202,305,2024-03-16,26,7.3,4000\n"
                "1006,Kano,KAN,Chidi,203,306,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,LOS,Ada,201,307,2024-03-17,80,12.4,5500\n"
                "1008,Abuja,ABJ,Bayo,202,308,2024-03-17,31,9.2,3800\n"
                "1009,Kano,KAN,Chidi,203,309,2024-03-18,19,4.9,2100\n"
                "1010,Lagos,LOS,Ada,201,310,2024-03-18,24,5.1,2900\n"
                "1011,Abuja,ABJ,Bayo,202,311,2024-03-19,33,10.0,4200\n"
                "1012,Kano,KAN,Chidi,203,312,2024-03-19,21,4.4,1700\n"
                "1013,Lagos,LOS,Ada,201,313,2024-03-20,27,6.6,3300\n"
                "1014,Abuja,ABJ,Bayo,202,314,2024-03-20,35,11.1,4600\n"
            )
        }
    ]
}

cw_sort_rename = {
    "asset_id":    "cw_sort_rename",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "Sort and Rename Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders.csv')\n\n"
                "# TODO: sort by city ascending, then delivery_time_minutes descending\n"
                "# TODO: rename 'delivery_time_minutes' to 'delivery_min'\n"
                "#       and 'city' to 'destination_city'\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,city_code,courier,driver_id,customer_id,"
                "pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,ABJ,Bayo,202,302,2024-03-14,20,6.1,3100\n"
                "1003,Kano,KAN,Chidi,203,303,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,LOS,Ada,201,304,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,ABJ,Bayo,202,305,2024-03-16,26,7.3,4000\n"
                "1006,Kano,KAN,Chidi,203,306,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,LOS,Ada,201,307,2024-03-17,80,12.4,5500\n"
                "1008,Abuja,ABJ,Bayo,202,308,2024-03-17,31,9.2,3800\n"
            )
        }
    ]
}

cw_dtype_datetime = {
    "asset_id":    "cw_dtype_datetime",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "dtype Conversion and Datetime Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders_messy_dtype.csv')\n\n"
                "# distance_km is loaded as a string — convert it to float\n"
                "# pickup_date is a string — convert it to datetime\n\n"
                "# TODO: print orders.dtypes to see the problem\n"
                "# TODO: convert distance_km to float with astype()\n"
                "# TODO: convert pickup_date to datetime with pd.to_datetime()\n"
                "# TODO: extract the month number into a new column 'pickup_month'\n"
            )
        },
        {
            "path": "orders_messy_dtype.csv",
            "content": (
                "order_id,city,pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,2024-03-14,20,6.1,3100\n"
                "1003,Kano,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,2024-03-16,26,7.3,4000\n"
                "1006,Kano,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,2024-03-17,80,12.4,5500\n"
                "1008,Abuja,2024-03-17,31,9.2,3800\n"
            )
        }
    ]
}

cw_text_dupes_missing = {
    "asset_id":    "cw_text_dupes_missing",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "String Cleaning, Duplicates, and Missing Values Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders_messy.csv')\n\n"
                "# The city column has mixed case and stray spaces\n"
                "# Some order_ids are duplicated\n"
                "# Some delivery_time_minutes values are missing\n\n"
                "# TODO: clean city with .str.strip().str.lower()\n"
                "# TODO: remove duplicate order_ids with drop_duplicates()\n"
                "# TODO: detect missing delivery times with isna()\n"
                "# TODO: fill missing delivery times with the column median\n"
            )
        },
        {
            "path": "orders_messy.csv",
            "content": (
                "order_id,city,courier,delivery_time_minutes,order_value\n"
                "1001,Lagos,Ada,18,2500\n"
                "1002,Abuja,Bayo,20,3100\n"
                "1003,Kano,Chidi,22,1800\n"
                "1003,Kano,Chidi,22,1800\n"
                "1004, lagos,Ada,22,2200\n"
                "1005,Abuja,Bayo,26,4000\n"
                "1006,Kano,Chidi,28,1500\n"
                "1007,LAGOS ,Ada,80,5500\n"
                "1008,Abuja,Bayo,,3800\n"
                "1009,Kano,Chidi,19,2100\n"
            )
        }
    ]
}

cw_map_apply = {
    "asset_id":    "cw_map_apply",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "map and apply Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders.csv')\n\n"
                "# Lookup dict for city codes\n"
                "city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}\n\n"
                "# TODO: use .map(city_lookup) to replace city_code with full city names\n\n"
                "# Labelling rule: delivery_time_minutes > 25 → 'slow', else → 'fast'\n"
                "# def label_speed(row):\n"
                "#     if row['delivery_time_minutes'] > 25:\n"
                "#         return 'slow'\n"
                "#     else:\n"
                "#         return 'fast'\n\n"
                "# TODO: use .apply(label_speed, axis=1) to add a 'speed_label' column\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,city_code,courier,driver_id,customer_id,"
                "pickup_date,delivery_time_minutes,distance_km,order_value\n"
                "1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n"
                "1002,Abuja,ABJ,Bayo,202,302,2024-03-14,20,6.1,3100\n"
                "1003,Kano,KAN,Chidi,203,303,2024-03-15,22,5.5,1800\n"
                "1004,Lagos,LOS,Ada,201,304,2024-03-15,22,3.8,2200\n"
                "1005,Abuja,ABJ,Bayo,202,305,2024-03-16,26,7.3,4000\n"
                "1006,Kano,KAN,Chidi,203,306,2024-03-16,28,8.0,1500\n"
                "1007,Lagos,LOS,Ada,201,307,2024-03-17,80,12.4,5500\n"
                "1008,Abuja,ABJ,Bayo,202,308,2024-03-17,31,9.2,3800\n"
                "1009,Kano,KAN,Chidi,203,309,2024-03-18,19,4.9,2100\n"
                "1010,Lagos,LOS,Ada,201,310,2024-03-18,24,5.1,2900\n"
            )
        }
    ]
}

cw_groupby_melt = {
    "asset_id":    "cw_groupby_melt",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "groupby and melt Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "orders = pd.read_csv('orders.csv')\n"
                "city_deliveries = pd.read_csv('city_deliveries.csv')\n\n"
                "# groupby: average delivery time per city\n"
                "# TODO: orders.groupby('city')['delivery_time_minutes'].mean()\n"
                "# TODO: also compute sum and mean together with .agg(['mean', 'sum'])\n\n"
                "# melt: wide → long\n"
                "# TODO: city_deliveries.melt(id_vars=['city'],\n"
                "#                            var_name='month',\n"
                "#                            value_name='deliveries')\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,customer_id,delivery_time_minutes,order_value\n"
                "1001,Lagos,301,18,2500\n"
                "1002,Abuja,302,20,3100\n"
                "1003,Kano,303,22,1800\n"
                "1004,Lagos,304,22,2200\n"
                "1005,Abuja,305,26,4000\n"
                "1006,Kano,306,28,1500\n"
                "1007,Lagos,307,80,5500\n"
                "1008,Abuja,308,31,3800\n"
                "1009,Kano,309,19,2100\n"
                "1010,Lagos,310,24,2900\n"
                "1011,Abuja,311,33,4200\n"
                "1012,Kano,312,21,1700\n"
                "1013,Lagos,313,27,3300\n"
                "1014,Abuja,314,35,4600\n"
            )
        },
        {
            "path": "city_deliveries.csv",
            "content": (
                "city,jan_deliveries,feb_deliveries,mar_deliveries\n"
                "Lagos,142,138,155\n"
                "Abuja,98,104,110\n"
                "Kano,76,81,88\n"
            )
        }
    ]
}

cw_concat_merge = {
    "asset_id":    "cw_concat_merge",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "concat and merge Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "jan_orders = pd.read_csv('jan_orders.csv')\n"
                "feb_orders = pd.read_csv('feb_orders.csv')\n"
                "mar_orders = pd.read_csv('mar_orders.csv')\n"
                "orders    = pd.read_csv('orders.csv')\n"
                "customers = pd.read_csv('customers.csv')\n\n"
                "# concat: stack monthly tables row-wise\n"
                "# TODO: pd.concat([jan_orders, feb_orders, mar_orders])\n\n"
                "# merge: join orders with customers on customer_id\n"
                "# TODO: orders.merge(customers, on='customer_id')          # inner\n"
                "# TODO: orders.merge(customers, on='customer_id', how='left')  # left\n"
            )
        },
        {
            "path": "jan_orders.csv",
            "content": (
                "order_id,city,courier,delivery_time_minutes,order_value\n"
                "2001,Lagos,Ada,18,2500\n"
                "2002,Abuja,Bayo,22,3100\n"
                "2003,Kano,Chidi,26,1800\n"
                "2004,Lagos,Ada,31,2900\n"
                "2005,Abuja,Bayo,19,3400\n"
            )
        },
        {
            "path": "feb_orders.csv",
            "content": (
                "order_id,city,courier,delivery_time_minutes,order_value\n"
                "2006,Lagos,Ada,20,2700\n"
                "2007,Abuja,Bayo,28,4000\n"
                "2008,Kano,Chidi,24,1600\n"
                "2009,Lagos,Ada,35,5100\n"
                "2010,Kano,Chidi,21,2000\n"
            )
        },
        {
            "path": "mar_orders.csv",
            "content": (
                "order_id,city,courier,delivery_time_minutes,order_value\n"
                "2011,Lagos,Ada,22,2600\n"
                "2012,Abuja,Bayo,30,3700\n"
                "2013,Kano,Chidi,27,1900\n"
                "2014,Lagos,Ada,80,5500\n"
                "2015,Abuja,Bayo,23,3200\n"
            )
        },
        {
            "path": "orders.csv",
            "content": (
                "order_id,city,customer_id,delivery_time_minutes,order_value\n"
                "1001,Lagos,301,18,2500\n"
                "1002,Abuja,302,20,3100\n"
                "1003,Kano,303,22,1800\n"
                "1004,Lagos,304,22,2200\n"
                "1005,Abuja,305,26,4000\n"
                "1006,Kano,306,28,1500\n"
                "1007,Lagos,307,80,5500\n"
                "1008,Abuja,308,31,3800\n"
            )
        },
        {
            "path": "customers.csv",
            "content": (
                "customer_id,customer_name,segment\n"
                "301,Ngozi Eze,Individual\n"
                "302,Emeka Obi,Business\n"
                "303,Fatima Musa,Individual\n"
                "304,Tunde Bakare,Business\n"
                "305,Amaka Nwosu,Individual\n"
                "306,Yusuf Garba,Business\n"
                "307,Chisom Ike,Individual\n"
                "308,Bisi Adewale,Business\n"
                "315,Zainab Aliyu,Individual\n"
            )
        }
    ]
}

cw_pivot_export = {
    "asset_id":    "cw_pivot_export",
    "asset_kind":  "code_workspace",
    "scenario_id": "scen_swiftdrop",
    "title":       "pivot_table and Export Workspace",
    "runtime":     "pyodide",
    "files": [
        {
            "path": "starter.py",
            "content": (
                "import pandas as pd\n\n"
                "long_deliveries = pd.read_csv('long_deliveries.csv')\n"
                "product_sales   = pd.read_csv('product_sales.csv')\n\n"
                "# pivot_table: long → wide (city × month)\n"
                "# TODO: long_deliveries.pivot_table(index='city',\n"
                "#                                   columns='month',\n"
                "#                                   values='deliveries')\n\n"
                "# pivot_table with aggfunc='sum' (product_sales has duplicate product-month rows)\n"
                "# TODO: product_sales.pivot_table(index='product',\n"
                "#                                 columns='month',\n"
                "#                                 values='sales',\n"
                "#                                 aggfunc='sum')\n\n"
                "# export\n"
                "# TODO: save the result to 'cleaned_orders.csv' with index=False\n"
            )
        },
        {
            "path": "long_deliveries.csv",
            "content": (
                "city,month,deliveries\n"
                "Lagos,jan_deliveries,142\n"
                "Lagos,feb_deliveries,138\n"
                "Lagos,mar_deliveries,155\n"
                "Abuja,jan_deliveries,98\n"
                "Abuja,feb_deliveries,104\n"
                "Abuja,mar_deliveries,110\n"
                "Kano,jan_deliveries,76\n"
                "Kano,feb_deliveries,81\n"
                "Kano,mar_deliveries,88\n"
                "Lagos,jan_deliveries,18\n"
            )
        },
        {
            "path": "product_sales.csv",
            "content": (
                "product,month,sales\n"
                "Envelope,Jan,4500\n"
                "Envelope,Jan,3200\n"
                "Envelope,Feb,5100\n"
                "Envelope,Mar,4800\n"
                "Parcel,Jan,8200\n"
                "Parcel,Feb,7600\n"
                "Parcel,Feb,9100\n"
                "Parcel,Mar,8800\n"
                "Document,Jan,2100\n"
                "Document,Feb,2400\n"
                "Document,Mar,2300\n"
                "Document,Mar,1900\n"
            )
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSEMBLE REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
assets = [
    ds_orders,
    ds_drivers,
    ds_customers,
    ds_wide,
    ds_long,
    ds_product,
    ds_jan,
    ds_feb,
    ds_mar,
    cw_series_df,
    cw_reading,
    cw_creating,
    cw_inspecting,
    cw_stats,
    cw_loc_iloc,
    cw_bool_filter,
    cw_sort_rename,
    cw_dtype_datetime,
    cw_text_dupes_missing,
    cw_map_apply,
    cw_groupby_melt,
    cw_concat_merge,
    cw_pivot_export,
]

registry = {
    "schema_version": "1.0.0",
    "kind":           "scenario_asset_registry",
    "path_id":        "data_analyst",
    "batch_id":       "final_batch_009_da_pandas",
    "scenarios":      scenarios,
    "assets":         assets,
}

OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False))
print(f"Written: {OUT}  ({len(assets)} assets, {len(scenarios)} scenario)")
