"""Build scenario_asset_registry.json for final_batch_005_da_sql_canary.

Glossary vocabulary mined:
  Tables: customers, orders, products
  customers columns: customer_id, name, city
  orders columns: order_id, customer_id, delivery_time_minutes
  products columns: product_id, name, price (implied by 'products table')
  Cities mentioned: Lagos (sql.distinct tb2)
  Alias example: orders AS o  (sql.aliasing tb2, tb4)
  SELECT examples: SELECT name, city FROM customers
                   SELECT name AS customer_name, city FROM customers
                   SELECT * FROM customers
                   SELECT DISTINCT city FROM customers
                   SELECT o.order_id, o.delivery_time_minutes FROM orders AS o
"""
import json
from pathlib import Path

BATCH = Path(__file__).parent
OUT = BATCH / "scenario_asset_registry.json"

# ------------------------------------------------------------------ scenario
scenario = {
    "scenario_id": "scen.sql_delivery_shop",
    "name": "QuickDeliver — a small delivery-order business",
    "summary": (
        "A fictional small delivery business called QuickDeliver stores its data in three "
        "SQL tables: customers (who placed orders), orders (each delivery request), and "
        "products (items available for delivery). The schema is introduced in "
        "sql.relational_model and reused across the whole SQL run."
    ),
    "locale": "en-NG",
    "currency": "NGN",
    "domain": "retail_delivery",
    "glossary_example_vocab": [
        # tables
        "customers", "orders", "products",
        # customers columns
        "customer_id", "name", "city",
        # orders columns
        "order_id", "delivery_time_minutes",
        # products columns
        "product_id", "price",
        # cities (Lagos named in sql.distinct tb2)
        "Lagos",
        # alias example
        "o",
        # SQL keywords used in teaching blocks
        "SELECT", "FROM", "AS", "DISTINCT", "ALL",
        # column alias example
        "customer_name",
        # correlation reference example
        "o.order_id", "o.delivery_time_minutes", "o.customer_id",
    ],
}

# ------------------------------------------------------------------ customers table
# Columns: customer_id (integer PK), name (string), city (string)
# Needs: enough rows so DISTINCT city returns fewer rows than SELECT city
# Lagos must appear more than once (sql.distinct tb2 says "Lagos once per customer who lives there")
# Need >= 3 distinct cities so hidden tests can distinguish correct DISTINCT from lazy queries
# customer_id is a numeric identifier (numeric_looking_label=True)

customers_columns = [
    {
        "name": "customer_id",
        "type": "integer",
        "semantic_role": "identifier",
        "numeric_looking_label": True,
        "description": "Unique integer identifier for each customer (used as a label, not a quantity).",
    },
    {
        "name": "name",
        "type": "string",
        "semantic_role": "text",
        "description": "Full name of the customer.",
    },
    {
        "name": "city",
        "type": "string",
        "semantic_role": "categorical",
        "description": "City where the customer is located.",
    },
]

# 8 rows: Lagos appears 3 times, Abuja 2 times, Kano 2 times, Port Harcourt 1 time
# → SELECT city returns 8 rows; SELECT DISTINCT city returns 4 rows
customers_rows = [
    [1, "Amara Okafor",    "Lagos"],
    [2, "Emeka Nwosu",     "Abuja"],
    [3, "Fatima Bello",    "Lagos"],
    [4, "Chidi Eze",       "Kano"],
    [5, "Ngozi Adeyemi",   "Lagos"],
    [6, "Yusuf Musa",      "Abuja"],
    [7, "Aisha Garba",     "Kano"],
    [8, "Tunde Fashola",   "Port Harcourt"],
]

# Messy variant: one duplicate row (customer_id=3 duplicated) + one wrong-type city value
# duplicate_row: duplicate row where customer_id=3
# set_cell: set city of customer_id=7 to a numeric-looking value to test wrong_type detection
# We'll use a simpler messy variant: one duplicate row + one inconsistent casing
customers_variant_messy = {
    "variant_id": "customers.messy_v1",
    "derived_from": "ds.customers",
    "purpose": "find_issues practice: one duplicate row and one inconsistent city casing",
    "ops": [
        # duplicate row for customer_id=3
        {
            "op": "duplicate_row",
            "where": {"customer_id": 3},
            "occurrence": 0,
            "insert": "end",
        },
        # inconsistent casing: change city of customer_id=6 to lowercase "abuja"
        {
            "op": "set_cell",
            "where": {"customer_id": 6},
            "occurrence": 0,
            "column": "city",
            "value": "abuja",
        },
    ],
    "planted_issues": [
        {
            "issue_id": "issue.customers.dup_row_3",
            "kind": "duplicate_row",
            "locations": [
                {"where": {"customer_id": 3}, "occurrence": 0, "column": "customer_id"},
                {"where": {"customer_id": 3}, "occurrence": 1, "column": "customer_id"},
            ],
            "description": "Row for customer_id=3 (Fatima Bello, Lagos) appears twice after the duplicate_row op.",
        },
        {
            "issue_id": "issue.customers.casing_city_6",
            "kind": "inconsistent_category",
            "locations": [
                {"where": {"customer_id": 6}, "occurrence": 0, "column": "city"},
            ],
            "description": "City value for customer_id=6 is 'abuja' (lowercase) while all other Abuja entries use 'Abuja'.",
            "rule": {
                "column": "city",
                "op": "casing_differs_from_siblings",
            },
        },
    ],
}

dataset_customers = {
    "asset_id": "ds.customers",
    "asset_kind": "dataset",
    "scenario_id": "scen.sql_delivery_shop",
    "title": "customers — QuickDeliver customer records",
    "description": (
        "One row per customer. Columns: customer_id (integer PK), name, city. "
        "Used in sql.relational_model, sql.select_fundamentals, sql.aliasing, sql.distinct."
    ),
    "columns": customers_columns,
    "rows": customers_rows,
    "variants": [customers_variant_messy],
    "provenance": "authored",
}

# ------------------------------------------------------------------ orders table
# Columns: order_id (integer PK), customer_id (integer FK), delivery_time_minutes (integer)
# Named in: sql.relational_model tb1/tb2, sql.aliasing tb2/tb4
# Alias example: FROM orders AS o → o.order_id, o.delivery_time_minutes, o.customer_id
# Need enough rows for hidden tests to distinguish correct queries from lazy ones
# order_id and customer_id are numeric labels

orders_columns = [
    {
        "name": "order_id",
        "type": "integer",
        "semantic_role": "identifier",
        "numeric_looking_label": True,
        "description": "Unique integer identifier for each order (label, not a quantity).",
    },
    {
        "name": "customer_id",
        "type": "integer",
        "semantic_role": "identifier",
        "numeric_looking_label": True,
        "description": "Foreign key referencing customers.customer_id.",
    },
    {
        "name": "delivery_time_minutes",
        "type": "integer",
        "semantic_role": "numerical",
        "unit": "minutes",
        "description": "Time in minutes from order placement to delivery.",
    },
]

# 10 rows covering all 8 customers (some customers have multiple orders)
# delivery_time_minutes: realistic values 18–95 minutes
orders_rows = [
    [1001, 1, 42],
    [1002, 2, 31],
    [1003, 3, 55],
    [1004, 4, 28],
    [1005, 5, 67],
    [1006, 6, 19],
    [1007, 7, 83],
    [1008, 8, 45],
    [1009, 1, 38],
    [1010, 3, 72],
]

# Messy variant: one impossible delivery_time_minutes (negative) + one duplicate row
orders_variant_messy = {
    "variant_id": "orders.messy_v1",
    "derived_from": "ds.orders",
    "purpose": "find_issues practice: one impossible value (negative delivery time) and one duplicate row",
    "ops": [
        # set delivery_time_minutes of order_id=1005 to -5 (impossible)
        {
            "op": "set_cell",
            "where": {"order_id": 1005},
            "occurrence": 0,
            "column": "delivery_time_minutes",
            "value": -5,
        },
        # duplicate row for order_id=1002
        {
            "op": "duplicate_row",
            "where": {"order_id": 1002},
            "occurrence": 0,
            "insert": "end",
        },
    ],
    "planted_issues": [
        {
            "issue_id": "issue.orders.impossible_delivery_time",
            "kind": "impossible_value",
            "locations": [
                {"where": {"order_id": 1005}, "occurrence": 0, "column": "delivery_time_minutes"},
            ],
            "description": "delivery_time_minutes is -5 for order_id=1005, which is impossible (time cannot be negative).",
            "rule": {
                "column": "delivery_time_minutes",
                "op": "lt",
                "value": 0,
            },
        },
        {
            "issue_id": "issue.orders.dup_row_1002",
            "kind": "duplicate_row",
            "locations": [
                {"where": {"order_id": 1002}, "occurrence": 0, "column": "order_id"},
                {"where": {"order_id": 1002}, "occurrence": 1, "column": "order_id"},
            ],
            "description": "Row for order_id=1002 appears twice after the duplicate_row op.",
        },
    ],
}

dataset_orders = {
    "asset_id": "ds.orders",
    "asset_kind": "dataset",
    "scenario_id": "scen.sql_delivery_shop",
    "title": "orders — QuickDeliver delivery orders",
    "description": (
        "One row per delivery order. Columns: order_id (integer PK), customer_id (integer FK), "
        "delivery_time_minutes (integer). "
        "Used in sql.relational_model, sql.aliasing."
    ),
    "columns": orders_columns,
    "rows": orders_rows,
    "variants": [orders_variant_messy],
    "provenance": "authored",
}

# ------------------------------------------------------------------ products table
# Named in sql.relational_model tb1/tb2 as a third table in the database
# Columns: product_id (integer PK), name (string), price (number)
# Needed so the relational_model concept can show a three-table database

products_columns = [
    {
        "name": "product_id",
        "type": "integer",
        "semantic_role": "identifier",
        "numeric_looking_label": True,
        "description": "Unique integer identifier for each product (label, not a quantity).",
    },
    {
        "name": "name",
        "type": "string",
        "semantic_role": "text",
        "description": "Name of the product.",
    },
    {
        "name": "price",
        "type": "number",
        "semantic_role": "numerical",
        "unit": "NGN",
        "description": "Price of the product in Nigerian Naira.",
    },
]

products_rows = [
    [101, "Jollof Rice (large)",   2500.0],
    [102, "Fried Chicken (4 pcs)", 3200.0],
    [103, "Puff Puff (dozen)",      800.0],
    [104, "Suya (500g)",           1800.0],
    [105, "Moi Moi (6 pcs)",       1200.0],
]

dataset_products = {
    "asset_id": "ds.products",
    "asset_kind": "dataset",
    "scenario_id": "scen.sql_delivery_shop",
    "title": "products — QuickDeliver product catalogue",
    "description": (
        "One row per product. Columns: product_id (integer PK), name, price (NGN). "
        "Introduced in sql.relational_model to complete the three-table database picture."
    ),
    "columns": products_columns,
    "rows": products_rows,
    "provenance": "authored",
}

# ------------------------------------------------------------------ assemble registry
registry = {
    "schema_version": "1.0.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_005_da_sql_canary",
    "scenarios": [scenario],
    "assets": [
        dataset_customers,
        dataset_orders,
        dataset_products,
    ],
}

OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
print(f"Written: {OUT}")
print(f"Scenarios: {len(registry['scenarios'])}")
print(f"Assets: {len(registry['assets'])}")
for a in registry["assets"]:
    ncols = len(a["columns"])
    nrows = len(a.get("rows", []))
    nvars = len(a.get("variants", []))
    print(f"  {a['asset_id']}: {ncols} cols, {nrows} rows, {nvars} variants")
    for r in a.get("rows", []):
        assert len(r) == ncols, f"Row width mismatch in {a['asset_id']}: {r}"
