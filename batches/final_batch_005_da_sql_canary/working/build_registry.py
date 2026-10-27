"""Build scenario_asset_registry.json for final_batch_005_da_sql_canary.

Tiles in scope:
  tile_sql_fund_relational_select  -> sql.relational_model, sql.select_fundamentals
  tile_sql_fund_alias_distinct     -> sql.aliasing, sql.distinct

Glossary vocabulary mined:
  Tables: customers (customer_id, name, city), orders (order_id, customer_id, delivery_time_minutes)
  Video segment: first_name, country columns mentioned for customers
  DISTINCT example: city column with repeated values; Lagos mentioned
  Aliasing: FROM orders AS o, o.customer_id, o.delivery_time_minutes
  SELECT: SELECT name, city FROM customers; SELECT name AS customer_name, city FROM customers
  SELECT *: SELECT * FROM customers

Design decisions:
  - customers table: customer_id, name, city  (glossary names these explicitly)
    The video segment mentions first_name and country — but the teaching text uses 'name' and 'city'.
    We use 'name' and 'city' to match the text; the video segment is a support clip, not the authoritative vocab.
    We add enough rows so DISTINCT city returns fewer rows than SELECT city (need repeated cities).
    Lagos is mentioned in the DISTINCT teaching block — must appear more than once.
  - orders table: order_id, customer_id, delivery_time_minutes  (glossary names these explicitly)
    Aliasing practice: FROM orders AS o, o.customer_id, o.delivery_time_minutes
    Need enough rows to distinguish correct queries from lazy ones.
  - Both tables get a 'messy' variant for find_issues practice.
"""

import json
import pathlib

OUT = pathlib.Path("batches/final_batch_005_da_sql_canary/scenario_asset_registry.json")

# ---------------------------------------------------------------------------
# customers base rows
# Columns: customer_id (integer, identifier), name (string, text), city (string, categorical)
# Need: repeated cities (Lagos appears >=2 times per DISTINCT teaching block)
# Need: enough rows for hidden tests to distinguish correct from lazy queries
# ---------------------------------------------------------------------------
customers_columns = [
    {"name": "customer_id", "type": "integer", "semantic_role": "identifier",
     "description": "Unique integer identifier for each customer",
     "numeric_looking_label": True},
    {"name": "name",        "type": "string",  "semantic_role": "text",
     "description": "Full name of the customer"},
    {"name": "city",        "type": "string",  "semantic_role": "categorical",
     "description": "City where the customer is located"},
]

# Rows: [customer_id, name, city]
# 8 rows, 3 distinct cities (Lagos x3, Abuja x3, Kano x2) so DISTINCT returns 3 rows vs 8 rows
customers_rows = [
    [1, "Amara Okafor",   "Lagos"],
    [2, "Chidi Nwosu",    "Abuja"],
    [3, "Fatima Bello",   "Lagos"],
    [4, "Emeka Eze",      "Kano"],
    [5, "Ngozi Adeyemi",  "Abuja"],
    [6, "Tunde Adesanya", "Lagos"],
    [7, "Aisha Musa",     "Kano"],
    [8, "Yemi Okonkwo",   "Abuja"],
]

# ---------------------------------------------------------------------------
# orders base rows
# Columns: order_id (integer, identifier), customer_id (integer, identifier),
#          delivery_time_minutes (integer, numerical)
# Aliasing practice: FROM orders AS o, o.customer_id, o.delivery_time_minutes
# Need enough rows for hidden tests; customer_ids reference customers table
# ---------------------------------------------------------------------------
orders_columns = [
    {"name": "order_id",               "type": "integer", "semantic_role": "identifier",
     "description": "Unique integer identifier for each order",
     "numeric_looking_label": True},
    {"name": "customer_id",            "type": "integer", "semantic_role": "identifier",
     "description": "Foreign key referencing the customer who placed the order",
     "numeric_looking_label": True},
    {"name": "delivery_time_minutes",  "type": "integer", "semantic_role": "numerical",
     "unit": "minutes",
     "description": "Number of minutes from order placement to delivery"},
]

# Rows: [order_id, customer_id, delivery_time_minutes]
# 10 rows; varied delivery times so aggregate queries are non-trivial
orders_rows = [
    [1001, 1, 32],
    [1002, 3, 47],
    [1003, 2, 19],
    [1004, 5, 55],
    [1005, 1, 28],
    [1006, 4, 63],
    [1007, 6, 41],
    [1008, 2, 22],
    [1009, 7, 38],
    [1010, 8, 51],
]

# ---------------------------------------------------------------------------
# customers_messy variant
# Purpose: find_issues practice — planted issues for data-quality tiles
# Op 1: set_cell — set customer_id=1 row's city to "lagos" (wrong casing vs siblings "Lagos")
# Op 2: duplicate_row — duplicate customer_id=4 row (duplicate_row issue)
# ---------------------------------------------------------------------------
customers_messy_ops = [
    {
        "op": "set_cell",
        "where": {"customer_id": 1},
        "column": "city",
        "value": "lagos"
    },
    {
        "op": "duplicate_row",
        "where": {"customer_id": 4},
        "insert": "end"
    }
]

# After ops the variant rows are:
# [1, "Amara Okafor", "lagos"]   <- casing issue
# [2, "Chidi Nwosu",  "Abuja"]
# [3, "Fatima Bello", "Lagos"]
# [4, "Emeka Eze",    "Kano"]
# [5, "Ngozi Adeyemi","Abuja"]
# [6, "Tunde Adesanya","Lagos"]
# [7, "Aisha Musa",   "Kano"]
# [8, "Yemi Okonkwo", "Abuja"]
# [4, "Emeka Eze",    "Kano"]   <- duplicate of row 4

# Planted issues:
# issue_1: inconsistent_category — city "lagos" vs siblings "Lagos"
#   location: where={customer_id:1}, column=city
#   rule: casing_differs_from_siblings
# issue_2: duplicate_row — customer_id=4 appears twice
#   location: where={customer_id:4}, occurrence=1, column=customer_id
#   (occurrence=1 means the second match, i.e. the duplicate)

customers_messy_planted = [
    {
        "issue_id": "issue_cust_city_casing",
        "kind": "inconsistent_category",
        "locations": [
            {"where": {"customer_id": 1}, "column": "city"}
        ],
        "description": "City value 'lagos' uses lower-case while all other city values use title-case (e.g. 'Lagos').",
        "rule": {"column": "city", "op": "casing_differs_from_siblings"}
    },
    {
        "issue_id": "issue_cust_duplicate",
        "kind": "duplicate_row",
        "locations": [
            {"where": {"customer_id": 4}, "occurrence": 1, "column": "customer_id"}
        ],
        "description": "Customer 4 (Emeka Eze, Kano) appears twice — the second row is an exact duplicate."
    }
]

# ---------------------------------------------------------------------------
# orders_messy variant
# Purpose: find_issues practice — planted issues
# Op 1: set_cell — set order_id=1006 delivery_time_minutes to -5 (impossible: negative delivery time)
# Op 2: set_cell — set order_id=1003 customer_id to None (missing value)
# ---------------------------------------------------------------------------
orders_messy_ops = [
    {
        "op": "set_cell",
        "where": {"order_id": 1006},
        "column": "delivery_time_minutes",
        "value": -5
    },
    {
        "op": "set_cell",
        "where": {"order_id": 1003},
        "column": "customer_id",
        "value": None
    }
]

# After ops:
# order 1006: delivery_time_minutes = -5  (impossible: must be > 0)
# order 1003: customer_id = None          (missing value)

orders_messy_planted = [
    {
        "issue_id": "issue_ord_negative_delivery",
        "kind": "impossible_value",
        "locations": [
            {"where": {"order_id": 1006}, "column": "delivery_time_minutes"}
        ],
        "description": "delivery_time_minutes is -5, which is impossible — delivery time cannot be negative.",
        "rule": {"column": "delivery_time_minutes", "op": "lt", "value": 0}
    },
    {
        "issue_id": "issue_ord_missing_customer",
        "kind": "missing_value",
        "locations": [
            {"where": {"order_id": 1003}, "column": "customer_id"}
        ],
        "description": "customer_id is NULL for order 1003 — every order must reference a customer."
    }
]

# ---------------------------------------------------------------------------
# Assemble registry
# ---------------------------------------------------------------------------
registry = {
    "schema_version": "1.0.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_005_da_sql_canary",
    "scenarios": [
        {
            "scenario_id": "scenario_sql_shop",
            "name": "Greenleaf Online Shop",
            "summary": (
                "A small fictional e-commerce business, Greenleaf Online Shop, "
                "stores its data in a relational database with a customers table "
                "and an orders table. Learners query these tables to practise "
                "SELECT, aliasing, DISTINCT and basic data-quality checks."
            ),
            "locale": "NG",
            "currency": "NGN",
            "domain": "e-commerce",
            "glossary_example_vocab": [
                # Tables named in teaching blocks
                "customers", "orders", "products",
                # customers columns (tb2 of sql.relational_model and sql.select_fundamentals)
                "customer_id", "name", "city",
                # orders columns (sql.aliasing practice_anchor)
                "order_id", "delivery_time_minutes",
                # alias used in sql.aliasing teaching blocks
                "o",
                # city values (sql.distinct tb2 mentions Lagos)
                "Lagos", "Abuja", "Kano",
                # renamed column example (sql.select_fundamentals tb3)
                "customer_name",
                # video segment mentions first_name, country (sql.select_fundamentals media)
                "first_name", "country",
                # SQL keywords taught
                "SELECT", "FROM", "AS", "DISTINCT", "ALL",
            ]
        }
    ],
    "assets": [
        # ------------------------------------------------------------------ customers (base)
        {
            "asset_id": "ds_customers",
            "asset_kind": "dataset",
            "scenario_id": "scenario_sql_shop",
            "title": "customers",
            "description": (
                "The customers table for Greenleaf Online Shop. "
                "Each row is one customer. Used for SELECT, AS, and DISTINCT examples."
            ),
            "columns": customers_columns,
            "rows": customers_rows,
            "variants": [
                {
                    "variant_id": "ds_customers_messy",
                    "derived_from": "ds_customers",
                    "purpose": "find_issues practice: one inconsistent-casing city value and one duplicate row",
                    "ops": customers_messy_ops,
                    "planted_issues": customers_messy_planted
                }
            ],
            "provenance": "authored"
        },
        # ------------------------------------------------------------------ orders (base)
        {
            "asset_id": "ds_orders",
            "asset_kind": "dataset",
            "scenario_id": "scenario_sql_shop",
            "title": "orders",
            "description": (
                "The orders table for Greenleaf Online Shop. "
                "Each row is one order. Used for aliasing (FROM orders AS o) "
                "and delivery-time queries."
            ),
            "columns": orders_columns,
            "rows": orders_rows,
            "variants": [
                {
                    "variant_id": "ds_orders_messy",
                    "derived_from": "ds_orders",
                    "purpose": "find_issues practice: one impossible negative delivery time and one missing customer_id",
                    "ops": orders_messy_ops,
                    "planted_issues": orders_messy_planted
                }
            ],
            "provenance": "authored"
        }
    ]
}

# ---------------------------------------------------------------------------
# Validate row widths before writing
# ---------------------------------------------------------------------------
for asset in registry["assets"]:
    if asset["asset_kind"] != "dataset":
        continue
    ncols = len(asset["columns"])
    for i, row in enumerate(asset["rows"]):
        assert len(row) == ncols, (
            f"{asset['asset_id']} row {i}: width {len(row)} != {ncols} columns"
        )

print("Row-width check passed.")

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    json.dump(registry, f, indent=2)

print(f"Written: {OUT}")
print(f"  scenarios: {len(registry['scenarios'])}")
print(f"  assets:    {len(registry['assets'])}")
for a in registry["assets"]:
    if a["asset_kind"] == "dataset":
        print(f"    {a['asset_id']}: {len(a['columns'])} cols x {len(a['rows'])} rows, "
              f"{len(a.get('variants', []))} variant(s)")
