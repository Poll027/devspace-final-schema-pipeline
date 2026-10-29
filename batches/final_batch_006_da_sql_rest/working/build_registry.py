"""Build scenario_asset_registry.json for final_batch_006_da_sql_rest."""
import json, pathlib

BATCH = pathlib.Path("batches/final_batch_006_da_sql_rest")

# ── helpers ──────────────────────────────────────────────────────────────────
def col(name, typ, role, unit=None, desc=None, numeric_looking_label=False):
    c = {"name": name, "type": typ, "semantic_role": role}
    if unit:
        c["unit"] = unit
    if desc:
        c["description"] = desc
    if numeric_looking_label:
        c["numeric_looking_label"] = True
    return c

# ─────────────────────────────────────────────────────────────────────────────
# SCENARIO
# ─────────────────────────────────────────────────────────────────────────────
scenario = {
    "scenario_id": "scen_da_sql_ecommerce",
    "name": "QuickCart e-commerce operations",
    "summary": (
        "QuickCart is a fictional online retailer operating across Nigerian cities. "
        "Its operations database tracks customers, orders, order line-items and shipments. "
        "Analysts query this database to monitor delivery performance, customer behaviour "
        "and fulfilment quality."
    ),
    "locale": "NG",
    "currency": "NGN",
    "domain": "e-commerce / retail operations",
    "glossary_example_vocab": [
        # tables
        "orders", "customers", "order_items", "shipments",
        # orders columns
        "order_id", "customer_id", "delivery_time_minutes", "order_date", "region", "amount", "city",
        # customers columns
        "name",
        # order_items / shipments columns
        "product_id", "quantity", "unit_price", "shipped_date",
        # specific values from teaching blocks
        "Lagos", "Kano", "fast", "normal", "slow", "north", "south",
        # thresholds mentioned in examples
        "20", "30", "40", "60",
        # SQL constructs demonstrated on this data
        "WHERE", "AND", "OR", "NOT", "IS NULL", "IS NOT NULL",
        "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
        "COUNT", "SUM", "AVG", "MIN", "MAX",
        "GROUP BY", "HAVING",
        "CASE WHEN THEN ELSE END",
        "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
        "EXTRACT", "CAST", "COALESCE", "UNION", "UNION ALL",
        "JOIN", "INNER JOIN", "LEFT JOIN", "ON", "USING",
        "WITH", "CTE", "subquery",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 1 — orders
# Glossary examples use: order_id, customer_id, delivery_time_minutes (nullable),
# order_date, region, amount, city
# Thresholds: 20, 30, 40, 60
# Need: rows above/below each threshold; NULL delivery_time; Lagos/Kano cities;
#       enough rows for LIMIT/OFFSET (>6), GROUP BY per customer, HAVING,
#       subquery-in-WHERE (avg comparison), UNION (delivery_time_minutes > 60).
# customer_id 1 and 2 are explicitly named in glossary.
# ─────────────────────────────────────────────────────────────────────────────
orders_columns = [
    col("order_id",               "integer", "identifier",  desc="Unique order identifier"),
    col("customer_id",            "integer", "identifier",  desc="FK to customers.customer_id",
        numeric_looking_label=True),
    col("delivery_time_minutes",  "integer", "numerical",   unit="minutes",
        desc="Elapsed minutes from order placement to delivery; NULL when not yet delivered"),
    col("order_date",             "date",    "datetime",    desc="Calendar date the order was placed"),
    col("region",                 "string",  "categorical", desc="Broad geographic region of the delivery address"),
    col("amount",                 "number",  "numerical",   unit="NGN",
        desc="Total order value in Naira"),
    col("city",                   "string",  "categorical", desc="City of the delivery address"),
]

# 12 rows — enough for LIMIT 3 OFFSET 3, GROUP BY 3 customers, HAVING, subquery avg, UNION
# delivery_time_minutes: 15, 18, 22, 25, 31, 35, 41, 45, 55, 63, NULL, NULL
# customer_id 1,2,3 (1 and 2 named in glossary; 3 for outer-join unmatched customer)
# city: Lagos, Kano, Abuja (Lagos and Kano named in glossary)
# region: south, north, other (matches CASE city example labels)
# order_date: spread across months for EXTRACT(month ...) demo
orders_rows = [
    # order_id, customer_id, delivery_time_minutes, order_date,   region,  amount,   city
    [1001,       1,           15,                   "2024-01-05", "south", 4200.00,  "Lagos"],
    [1002,       2,           22,                   "2024-01-12", "north", 8750.00,  "Kano"],
    [1003,       1,           41,                   "2024-02-03", "south", 3100.00,  "Lagos"],
    [1004,       3,           18,                   "2024-02-14", "other", 5600.00,  "Abuja"],
    [1005,       2,           35,                   "2024-03-01", "north", 2900.00,  "Kano"],
    [1006,       1,           63,                   "2024-03-18", "south", 7400.00,  "Lagos"],
    [1007,       3,           25,                   "2024-04-02", "other", 1800.00,  "Abuja"],
    [1008,       2,           55,                   "2024-04-20", "north", 9200.00,  "Kano"],
    [1009,       1,           31,                   "2024-05-07", "south", 6300.00,  "Lagos"],
    [1010,       3,           45,                   "2024-05-22", "other", 3750.00,  "Abuja"],
    [1011,       2,           None,                 "2024-06-01", "north", 4100.00,  "Kano"],
    [1012,       1,           None,                 "2024-06-15", "south", 5500.00,  "Lagos"],
]

# Verify row widths
assert all(len(r) == len(orders_columns) for r in orders_rows), "orders row width mismatch"

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 2 — customers
# Glossary examples: customer_id, name, city (nullable for COALESCE)
# customer_id 1,2 named in glossary; need a customer with no orders (for LEFT JOIN)
# name nullable for COALESCE('unnamed customer') example
# city nullable for COALESCE(city, 'unknown') example
# Customer 6 has city='Kano' so that after the messy variant sets customer 2's
# city to 'kano', the casing_differs_from_siblings rule still finds a sibling 'Kano'.
# ─────────────────────────────────────────────────────────────────────────────
customers_columns = [
    col("customer_id", "integer", "identifier",  desc="Unique customer identifier",
        numeric_looking_label=True),
    col("name",        "string",  "pii",         desc="Customer full name; NULL if not recorded"),
    col("city",        "string",  "categorical", desc="Customer home city; NULL if not recorded"),
]

# 6 rows:
#   1,2,3 have orders; 4 has no orders (LEFT JOIN unmatched row demo);
#   5 has NULL name and city (COALESCE demo);
#   6 has city='Kano' — sibling needed for casing rule in messy variant
customers_rows = [
    # customer_id, name,              city
    [1,            "Amara Okafor",    "Lagos"],
    [2,            "Emeka Nwosu",     "Kano"],
    [3,            "Fatima Aliyu",    "Abuja"],
    [4,            "Chidi Eze",       None],       # no orders → LEFT JOIN unmatched row
    [5,            None,              None],        # COALESCE demo: both name and city NULL
    [6,            "Ngozi Bello",     "Kano"],      # second Kano customer; sibling for casing rule
]

assert all(len(r) == len(customers_columns) for r in customers_rows), "customers row width mismatch"

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 3 — order_items
# Glossary: order_id, product_id (composite join with shipments)
# Need: multiple products per order; some items with no matching shipment (outer join)
# ─────────────────────────────────────────────────────────────────────────────
order_items_columns = [
    col("order_id",    "integer", "identifier",  desc="FK to orders.order_id",
        numeric_looking_label=True),
    col("product_id",  "integer", "identifier",  desc="FK to a products catalogue",
        numeric_looking_label=True),
    col("quantity",    "integer", "numerical",   unit="units",
        desc="Number of units ordered"),
    col("unit_price",  "number",  "numerical",   unit="NGN",
        desc="Price per unit at time of order"),
]

order_items_rows = [
    # order_id, product_id, quantity, unit_price
    [1001,       101,        2,        1200.00],
    [1001,       102,        1,        1800.00],
    [1002,       103,        3,        2500.00],
    [1003,       101,        1,        1200.00],
    [1003,       104,        2,         950.00],
    [1004,       102,        4,        1800.00],
    [1005,       103,        2,        2500.00],
    [1006,       105,        1,        7400.00],
    [1007,       101,        3,        1200.00],
    [1008,       104,        5,         950.00],
]

assert all(len(r) == len(order_items_columns) for r in order_items_rows), "order_items row width mismatch"

# ─────────────────────────────────────────────────────────────────────────────
# DATASET 4 — shipments
# Glossary: order_id, product_id (composite join key), shipped_date
# Some order_items rows have no matching shipment (for outer join demo)
# ─────────────────────────────────────────────────────────────────────────────
shipments_columns = [
    col("order_id",     "integer", "identifier", desc="FK to orders.order_id",
        numeric_looking_label=True),
    col("product_id",   "integer", "identifier", desc="FK to a products catalogue",
        numeric_looking_label=True),
    col("shipped_date", "date",    "datetime",   desc="Date the item was physically dispatched"),
]

# Matches for (1001,101), (1001,102), (1002,103), (1003,101), (1004,102), (1005,103)
# No match for (1003,104), (1006,105), (1007,101), (1008,104) → composite join drops them
shipments_rows = [
    # order_id, product_id, shipped_date
    [1001,       101,        "2024-01-06"],
    [1001,       102,        "2024-01-06"],
    [1002,       103,        "2024-01-13"],
    [1003,       101,        "2024-02-04"],
    [1004,       102,        "2024-02-15"],
    [1005,       103,        "2024-03-02"],
]

assert all(len(r) == len(shipments_columns) for r in shipments_rows), "shipments row width mismatch"

# ─────────────────────────────────────────────────────────────────────────────
# VARIANTS
# ─────────────────────────────────────────────────────────────────────────────

# orders_messy: planted issues for find_issues interaction
# Issue 1: impossible_value — delivery_time_minutes = -5 (negative, impossible)
# Issue 2: inconsistent_category — city casing differs from siblings ('LAGOS' vs 'Lagos')
# Issue 3: duplicate_row — duplicate of order 1004
orders_messy_ops = [
    # Op 1: set delivery_time_minutes to -5 for order 1007 (impossible value)
    {
        "op": "set_cell",
        "where": {"order_id": 1007},
        "occurrence": 0,
        "column": "delivery_time_minutes",
        "value": -5
    },
    # Op 2: set city to 'LAGOS' for order 1009 (casing inconsistency — siblings have 'Lagos')
    {
        "op": "set_cell",
        "where": {"order_id": 1009},
        "occurrence": 0,
        "column": "city",
        "value": "LAGOS"
    },
    # Op 3: duplicate order 1004
    {
        "op": "duplicate_row",
        "where": {"order_id": 1004},
        "occurrence": 0,
        "insert": "end"
    },
]

orders_messy_planted = [
    {
        "issue_id": "iss_impossible_delivery",
        "kind": "impossible_value",
        "locations": [
            {"where": {"order_id": 1007}, "occurrence": 0, "column": "delivery_time_minutes"}
        ],
        "description": "delivery_time_minutes is -5, which is impossible for a delivery duration.",
        "rule": {"column": "delivery_time_minutes", "op": "lt", "value": 0}
    },
    {
        "issue_id": "iss_casing_city",
        "kind": "inconsistent_category",
        "locations": [
            {"where": {"order_id": 1009}, "occurrence": 0, "column": "city"}
        ],
        "description": "city is 'LAGOS' but all other Lagos rows use 'Lagos' — inconsistent casing.",
        "rule": {"column": "city", "op": "casing_differs_from_siblings"}
    },
    {
        "issue_id": "iss_duplicate_order",
        "kind": "duplicate_row",
        "locations": [
            {"where": {"order_id": 1004}, "occurrence": 0, "column": "order_id"},
            {"where": {"order_id": 1004}, "occurrence": 1, "column": "order_id"}
        ],
        "description": "Order 1004 appears twice — a duplicate row.",
    },
]

# customers_messy: planted issues for NULL/COALESCE and string-function exercises
# Issue 1: missing_value — city is NULL for customer 4 (already in base)
# Issue 2: inconsistent_category — city 'kano' vs sibling 'Kano' (customer 6)
customers_messy_ops = [
    # Set city to 'kano' for customer 2 (should be 'Kano'; customer 6 still has 'Kano')
    {
        "op": "set_cell",
        "where": {"customer_id": 2},
        "occurrence": 0,
        "column": "city",
        "value": "kano"
    },
]

customers_messy_planted = [
    {
        "issue_id": "iss_missing_city",
        "kind": "missing_value",
        "locations": [
            {"where": {"customer_id": 4}, "occurrence": 0, "column": "city"}
        ],
        "description": "city is NULL for customer 4 — city was never recorded.",
    },
    {
        "issue_id": "iss_casing_kano",
        "kind": "inconsistent_category",
        "locations": [
            {"where": {"customer_id": 2}, "occurrence": 0, "column": "city"}
        ],
        "description": "city is 'kano' but the standard casing used elsewhere is 'Kano' (see customer 6).",
        "rule": {"column": "city", "op": "casing_differs_from_siblings"}
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# ASSEMBLE REGISTRY
# ─────────────────────────────────────────────────────────────────────────────
registry = {
    "schema_version": "1.0.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_006_da_sql_rest",
    "scenarios": [scenario],
    "assets": [
        {
            "asset_id": "ds_orders",
            "asset_kind": "dataset",
            "scenario_id": "scen_da_sql_ecommerce",
            "title": "orders",
            "description": (
                "One row per customer order. Used for WHERE, ORDER BY, LIMIT/OFFSET, "
                "aggregate functions, GROUP BY, HAVING, CASE, string/date/cast functions, "
                "COALESCE, UNION, clause execution order, and subquery exercises."
            ),
            "columns": orders_columns,
            "rows": orders_rows,
            "provenance": "authored",
            "variants": [
                {
                    "variant_id": "ds_orders_messy",
                    "derived_from": "ds_orders",
                    "purpose": "Messy version with an impossible delivery time, a city casing inconsistency, and a duplicate row — used for find_issues interactions.",
                    "ops": orders_messy_ops,
                    "planted_issues": orders_messy_planted,
                }
            ],
        },
        {
            "asset_id": "ds_customers",
            "asset_kind": "dataset",
            "scenario_id": "scen_da_sql_ecommerce",
            "title": "customers",
            "description": (
                "One row per registered customer. Used for JOIN, outer join, "
                "COALESCE, style conventions, and UNION exercises. "
                "Customer 4 has no orders (LEFT JOIN unmatched row demo). "
                "Customer 5 has NULL name and city (COALESCE demo). "
                "Customer 6 has city='Kano' (sibling for casing rule in messy variant)."
            ),
            "columns": customers_columns,
            "rows": customers_rows,
            "provenance": "authored",
            "variants": [
                {
                    "variant_id": "ds_customers_messy",
                    "derived_from": "ds_customers",
                    "purpose": "Messy version with a city casing inconsistency and a pre-existing NULL city — used for find_issues and COALESCE exercises.",
                    "ops": customers_messy_ops,
                    "planted_issues": customers_messy_planted,
                }
            ],
        },
        {
            "asset_id": "ds_order_items",
            "asset_kind": "dataset",
            "scenario_id": "scen_da_sql_ecommerce",
            "title": "order_items",
            "description": (
                "One row per line item within an order. Used for composite join "
                "exercises (join to shipments on order_id AND product_id)."
            ),
            "columns": order_items_columns,
            "rows": order_items_rows,
            "provenance": "authored",
        },
        {
            "asset_id": "ds_shipments",
            "asset_kind": "dataset",
            "scenario_id": "scen_da_sql_ecommerce",
            "title": "shipments",
            "description": (
                "One row per dispatched line item. Used for composite join exercises "
                "(join to order_items on order_id AND product_id). "
                "Several order_items rows have no matching shipment row, "
                "so an inner join drops them while an outer join keeps them."
            ),
            "columns": shipments_columns,
            "rows": shipments_rows,
            "provenance": "authored",
        },
    ],
}

out = BATCH / "scenario_asset_registry.json"
out.write_text(json.dumps(registry, indent=2))
print(f"Written: {out}")
print(f"Scenarios: {len(registry['scenarios'])}")
print(f"Assets: {len(registry['assets'])}")
for a in registry["assets"]:
    rows = a.get("rows", [])
    variants = a.get("variants", [])
    print(f"  {a['asset_id']}: {len(a['columns'])} cols, {len(rows)} rows, {len(variants)} variants")
