"""
Build script for scenario_asset_registry.json
Batch: final_batch_003_da_chunk  Path: data_analyst
Domains covered: stats (distribution_shape, outlier_reasoning, frequency_distribution_reading,
                         correlation, correlation_interpretation, correlation_vs_causation_caveat),
                 datamodel (entities_tables, primary_keys, foreign_keys_referential_integrity,
                            one_to_many, normalization_basics, many_to_many_junction_tables,
                            er_diagram_reading),
                 stakeholder (data_driven_recommendation, plain_language_translation,
                              tailoring_detail_to_audience, anticipating_questions_objections,
                              chart_type_to_point_matching, simplifying_charts_for_audience,
                              presentation_structure_basics, executive_summary_writing)

Glossary example vocab mined from teaching blocks:
  Stats/Stakeholder: delivery times (18,20,22,22,26,28,34,41,52 min), outlier 80 min,
    distance_km, package_weight_kg, correlation 0.82 (distance/time), -0.65 (drivers/time),
    -0.41 (weight/time), -0.38 (distance/weight), priority toggle,
    frequency table bins (10-20:4, 20-30:9, 30-40:5, 40-50:2, 80-90:1 = 21 orders),
    cities Lagos/Abuja/Kano, Lagos avg 22→30 min, add one courier recommendation
  Datamodel: customers(customer_id,name,city), orders(order_id,customer_id,delivery_minutes),
    products(product_id,name), order_items(order_id,product_id),
    order 101 rice bag + cooking oil, order 103 rice bag, customer_id 99 orphan example
"""
import json
import datetime

registry = {
    "schema_version": "1.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_003_da_chunk",
    "scenarios": [
        {
            "scenario_id": "scen_quickship",
            "name": "QuickShip Delivery Analytics",
            "summary": (
                "QuickShip is a fictional last-mile delivery company operating in three Nigerian cities: "
                "Lagos, Abuja, and Kano. A junior data analyst is investigating delivery-time performance, "
                "exploring distributions and outliers, computing correlations between distance, package weight, "
                "and delivery time, and preparing findings for the operations manager."
            ),
            "locale": "NG",
            "currency": "NGN",
            "domain": "logistics / delivery operations",
            "glossary_example_vocab": [
                "delivery_minutes",
                "distance_km",
                "package_weight_kg",
                "priority",
                "city",
                "Lagos",
                "Abuja",
                "Kano",
                "order_id",
                "customer_id",
                "right-skewed distribution",
                "symmetric distribution",
                "outlier",
                "frequency table",
                "histogram",
                "modal range",
                "correlation",
                "positive association",
                "negative association",
                "confounding variable",
                "association does not imply causation",
                "operations manager",
                "courier",
                "average delivery time rose from 22 to 30 minutes"
            ]
        },
        {
            "scenario_id": "scen_quickship_db",
            "name": "QuickShip Relational Database",
            "summary": (
                "The relational schema behind QuickShip: customers, orders, products, and order_items tables. "
                "Used to teach entities, primary keys, foreign keys, referential integrity, one-to-many and "
                "many-to-many relationships, normalization, and ER diagram reading."
            ),
            "locale": "NG",
            "currency": "NGN",
            "domain": "relational data modelling / e-commerce logistics",
            "glossary_example_vocab": [
                "customers",
                "orders",
                "products",
                "order_items",
                "customer_id",
                "order_id",
                "product_id",
                "name",
                "city",
                "delivery_minutes",
                "primary key",
                "foreign key",
                "referential integrity",
                "orphan record",
                "one-to-many",
                "many-to-many",
                "junction table",
                "normalization",
                "update anomaly",
                "entity",
                "entity type",
                "entity set",
                "composite key",
                "entity integrity",
                "rice bag",
                "cooking oil",
                "Customer",
                "Order",
                "Product",
                "Order_Item"
            ]
        }
    ],
    "assets": []
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 1: delivery_times_sample
# A single batch of 9 delivery times used to teach distribution shape.
# Values from teaching block: 18, 20, 22, 22, 26, 28, 34, 41, 52 (right-skewed)
# Mean ≈ 29.2, median = 26 (mean > median, pulled by right tail)
# ─────────────────────────────────────────────────────────────────────────────
delivery_times_sample = {
    "asset_id": "ds_delivery_times_sample",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship",
    "title": "QuickShip Delivery Times — Small Sample (9 orders)",
    "description": (
        "Nine delivery-time observations used to illustrate distribution shape. "
        "Values: 18, 20, 22, 22, 26, 28, 34, 41, 52 minutes. "
        "Right-skewed: bulk sits 18–28 min, tail trails right. Mean ≈ 29.2, median = 26."
    ),
    "columns": [
        {
            "name": "order_id",
            "type": "string",
            "semantic_role": "identifier",
            "description": "Unique order reference"
        },
        {
            "name": "delivery_minutes",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Actual delivery time in minutes from dispatch to doorstep"
        }
    ],
    "rows": [
        ["ORD-001", 18],
        ["ORD-002", 20],
        ["ORD-003", 22],
        ["ORD-004", 22],
        ["ORD-005", 26],
        ["ORD-006", 28],
        ["ORD-007", 34],
        ["ORD-008", 41],
        ["ORD-009", 52]
    ],
    "provenance": "authored",
    "variants": [
        {
            # Outlier variant: replace 52 with 80 to create the outlier batch
            # Teaching block 1 of stats.outlier_reasoning: "18, 20, 22, 22, 26, 28, 80 minutes"
            "variant_id": "ds_delivery_times_sample.outlier",
            "derived_from": "ds_delivery_times_sample",
            "purpose": "Outlier version: the 52-minute order is replaced with an 80-minute order and the 34/41 orders are dropped, leaving the 7-value batch from the outlier teaching block.",
            "ops": [
                # Drop the 34-minute and 41-minute rows to match the 7-value outlier batch
                {"op": "drop_rows", "where": {"order_id": "ORD-007"}},
                {"op": "drop_rows", "where": {"order_id": "ORD-008"}},
                # Replace 52 with 80
                {"op": "set_cell", "where": {"order_id": "ORD-009"}, "column": "delivery_minutes", "value": 80}
            ],
            "planted_issues": [
                {
                    "issue_id": "issue_outlier_80min",
                    "kind": "outlier_suspicious",
                    "locations": [
                        {"where": {"order_id": "ORD-009"}, "column": "delivery_minutes"}
                    ],
                    "description": "80-minute delivery is extreme relative to the rest of the batch (18–28 min); could be a data-entry error (8.0 → 80) or a genuine event such as a road closure.",
                    "rule": {"column": "delivery_minutes", "op": "gt", "value": 60}
                }
            ]
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 2: delivery_frequency_table
# 21 orders grouped into 10-minute bins for frequency distribution teaching.
# Bins: 10-20: 4, 20-30: 9, 30-40: 5, 40-50: 2, 50-60: 0, 60-70: 0, 70-80: 0, 80-90: 1
# Total = 21 orders. Modal bin = 20-30 (9 orders).
# ─────────────────────────────────────────────────────────────────────────────
delivery_frequency_table = {
    "asset_id": "ds_delivery_frequency_table",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship",
    "title": "QuickShip Delivery Frequency Table — 21 Orders",
    "description": (
        "Frequency table of 21 delivery times grouped into 10-minute bins. "
        "Bins: 10–20 min: 4 orders, 20–30 min: 9 orders (modal bin), "
        "30–40 min: 5 orders, 40–50 min: 2 orders, 50–80 min: 0 orders, 80–90 min: 1 order. "
        "Right-skewed with a single far-out delivery past 80 minutes."
    ),
    "columns": [
        {
            "name": "bin_label",
            "type": "string",
            "semantic_role": "categorical",
            "description": "10-minute delivery-time bin label (e.g. '10–20 min')"
        },
        {
            "name": "bin_lower",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Lower bound of the bin (inclusive)"
        },
        {
            "name": "bin_upper",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Upper bound of the bin (exclusive)"
        },
        {
            "name": "order_count",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "orders",
            "description": "Number of orders whose delivery time falls in this bin"
        }
    ],
    "rows": [
        ["10–20 min", 10, 20, 4],
        ["20–30 min", 20, 30, 9],
        ["30–40 min", 30, 40, 5],
        ["40–50 min", 40, 50, 2],
        ["50–60 min", 50, 60, 0],
        ["60–70 min", 60, 70, 0],
        ["70–80 min", 70, 80, 0],
        ["80–90 min", 80, 90, 1]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 3: delivery_orders_extended
# Larger orders table with distance_km, package_weight_kg, priority, city.
# Supports correlation teaching (distance/time r≈0.82, weight/time r≈-0.41,
# distance/weight r≈-0.38) and stakeholder city comparisons.
# Also supports the correlation_vs_causation_caveat (priority toggle).
# ─────────────────────────────────────────────────────────────────────────────
# We need enough rows to make the correlations plausible.
# Correlation targets: dist/time ≈ 0.82, weight/time ≈ -0.41, dist/weight ≈ -0.38
# City distribution: Lagos, Abuja, Kano
# Lagos avg delivery time: ~30 min (current month), ~22 min (previous month implied)
delivery_orders_extended = {
    "asset_id": "ds_delivery_orders_extended",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship",
    "title": "QuickShip Delivery Orders — Extended (20 orders)",
    "description": (
        "Twenty delivery orders with distance, package weight, city, priority flag, and delivery time. "
        "Supports correlation analysis (distance/time ≈ 0.82 strong positive; "
        "weight/time ≈ -0.41 moderate negative; distance/weight ≈ -0.38 weak negative) "
        "and city-level comparisons (Lagos, Abuja, Kano). "
        "Priority toggle illustrates correlation-vs-causation caveat."
    ),
    "columns": [
        {
            "name": "order_id",
            "type": "string",
            "semantic_role": "identifier",
            "description": "Unique order reference"
        },
        {
            "name": "city",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Delivery city: Lagos, Abuja, or Kano"
        },
        {
            "name": "distance_km",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "km",
            "description": "Distance from dispatch hub to delivery address in kilometres"
        },
        {
            "name": "package_weight_kg",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "kg",
            "description": "Package weight in kilograms"
        },
        {
            "name": "priority",
            "type": "boolean",
            "semantic_role": "categorical",
            "description": "Whether the customer selected the priority delivery toggle"
        },
        {
            "name": "delivery_minutes",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Actual delivery time in minutes from dispatch to doorstep"
        }
    ],
    # Rows designed so that:
    # - distance_km and delivery_minutes have strong positive correlation (~0.82)
    # - package_weight_kg and delivery_minutes have moderate negative correlation (~-0.41)
    # - distance_km and package_weight_kg have weak negative correlation (~-0.38)
    # - Lagos orders average ~30 min, Abuja ~24 min, Kano ~22 min
    # - priority=True orders tend to be shorter (correlation, not causation)
    "rows": [
        # order_id, city, distance_km, package_weight_kg, priority, delivery_minutes
        ["ORD-101", "Lagos",  3.2,  8.5, False, 22],
        ["ORD-102", "Lagos",  5.1,  6.0, False, 28],
        ["ORD-103", "Lagos",  7.4,  4.5, True,  26],
        ["ORD-104", "Lagos",  9.8,  3.0, False, 35],
        ["ORD-105", "Lagos", 12.3,  2.5, False, 40],
        ["ORD-106", "Lagos", 14.0,  2.0, True,  38],
        ["ORD-107", "Lagos", 16.5,  1.5, False, 45],
        ["ORD-108", "Abuja",  2.8,  9.0, True,  18],
        ["ORD-109", "Abuja",  4.5,  7.5, False, 22],
        ["ORD-110", "Abuja",  6.2,  5.5, True,  24],
        ["ORD-111", "Abuja",  8.0,  4.0, False, 28],
        ["ORD-112", "Abuja", 10.5,  3.5, False, 32],
        ["ORD-113", "Kano",   2.0, 10.0, True,  16],
        ["ORD-114", "Kano",   3.5,  8.0, False, 20],
        ["ORD-115", "Kano",   5.0,  6.5, True,  22],
        ["ORD-116", "Kano",   7.0,  5.0, False, 26],
        ["ORD-117", "Kano",   9.5,  3.8, False, 30],
        ["ORD-118", "Lagos", 18.0,  1.2, False, 52],
        ["ORD-119", "Lagos", 11.0,  2.8, True,  34],
        ["ORD-120", "Abuja",  5.5,  6.8, True,  20]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 4: correlation_matrix
# 3×3 correlation matrix for distance_km, package_weight_kg, delivery_minutes.
# Values from teaching block: dist/time=0.82, weight/time=-0.41, dist/weight=-0.38
# ─────────────────────────────────────────────────────────────────────────────
correlation_matrix = {
    "asset_id": "ds_correlation_matrix",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship",
    "title": "QuickShip Pairwise Correlation Matrix (3 variables)",
    "description": (
        "Pairwise Pearson correlation coefficients for distance_km, package_weight_kg, "
        "and delivery_minutes. Values: distance/delivery_minutes=0.82 (strong positive), "
        "weight/delivery_minutes=-0.41 (moderate negative), distance/weight=-0.38 (weak negative). "
        "Used to teach ranking by magnitude and confounding variable reasoning."
    ),
    "columns": [
        {
            "name": "variable",
            "type": "string",
            "semantic_role": "identifier",
            "description": "Row variable name"
        },
        {
            "name": "distance_km",
            "type": "number",
            "semantic_role": "numerical",
            "description": "Correlation with distance_km"
        },
        {
            "name": "package_weight_kg",
            "type": "number",
            "semantic_role": "numerical",
            "description": "Correlation with package_weight_kg"
        },
        {
            "name": "delivery_minutes",
            "type": "number",
            "semantic_role": "numerical",
            "description": "Correlation with delivery_minutes"
        }
    ],
    "rows": [
        ["distance_km",        1.0,  -0.38,  0.82],
        ["package_weight_kg", -0.38,   1.0, -0.41],
        ["delivery_minutes",   0.82,  -0.41,  1.0]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 5: city_delivery_summary
# Monthly average delivery times per city, two months.
# Lagos: previous month 22 min, current month 30 min (rose).
# Abuja and Kano: stable ~22-24 min.
# Supports stakeholder recommendation and chart-type teaching.
# ─────────────────────────────────────────────────────────────────────────────
city_delivery_summary = {
    "asset_id": "ds_city_delivery_summary",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship",
    "title": "QuickShip City Delivery Summary — Two Months",
    "description": (
        "Monthly average delivery times and order volumes for Lagos, Abuja, and Kano "
        "across two months. Lagos average rose from 22 to 30 minutes. "
        "Supports bar chart (city comparison), line chart (trend over time), "
        "pie chart (share of total orders), and stakeholder recommendation teaching."
    ),
    "columns": [
        {
            "name": "city",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Delivery city"
        },
        {
            "name": "month",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Month label (e.g. 'Month 1', 'Month 2')"
        },
        {
            "name": "avg_delivery_minutes",
            "type": "number",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Average delivery time in minutes for that city and month"
        },
        {
            "name": "order_count",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "orders",
            "description": "Total number of orders delivered in that city and month"
        }
    ],
    "rows": [
        # city, month, avg_delivery_minutes, order_count
        ["Lagos",  "Month 1", 22.0, 210],
        ["Lagos",  "Month 2", 30.0, 198],
        ["Abuja",  "Month 1", 23.5, 145],
        ["Abuja",  "Month 2", 24.0, 152],
        ["Kano",   "Month 1", 21.0, 118],
        ["Kano",   "Month 2", 22.5, 124]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 6: customers
# customers(customer_id, name, city) — the canonical entity from datamodel teaching.
# customer_id is the primary key (unique, not null).
# ─────────────────────────────────────────────────────────────────────────────
customers = {
    "asset_id": "ds_customers",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship_db",
    "title": "QuickShip Customers Table",
    "description": (
        "The customers entity table: customer_id (primary key), name, city. "
        "Used to teach entities/tables, primary keys, entity integrity, "
        "one-to-many relationships, normalization, and foreign key referencing."
    ),
    "columns": [
        {
            "name": "customer_id",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": "Primary key — unique integer label for each customer (not a quantity)"
        },
        {
            "name": "name",
            "type": "string",
            "semantic_role": "text",
            "description": "Customer full name"
        },
        {
            "name": "city",
            "type": "string",
            "semantic_role": "categorical",
            "description": "Customer's city: Lagos, Abuja, or Kano"
        }
    ],
    "rows": [
        # customer_id, name, city
        [1, "Amara Okafor",  "Lagos"],
        [2, "Emeka Nwosu",   "Abuja"],
        [3, "Fatima Bello",  "Kano"],
        [4, "Chidi Eze",     "Lagos"],
        [5, "Ngozi Adeyemi", "Abuja"]
    ],
    "provenance": "authored",
    "variants": [
        {
            # Normalization teaching: denormalized version showing redundancy
            # Adds a duplicate customer row to show update anomaly risk
            "variant_id": "ds_customers.with_duplicate",
            "derived_from": "ds_customers",
            "purpose": "Duplicate-row variant to illustrate normalization: same customer appears twice with different city values, showing an update anomaly.",
            "ops": [
                # Duplicate customer 1 (Amara Okafor, Lagos)
                {"op": "duplicate_row", "where": {"customer_id": 1}, "occurrence": 0}
            ],
            "planted_issues": [
                {
                    "issue_id": "issue_duplicate_customer",
                    "kind": "duplicate_row",
                    "locations": [
                        {"where": {"customer_id": 1}, "column": "customer_id", "occurrence": 0},
                        {"where": {"customer_id": 1}, "column": "customer_id", "occurrence": 1}
                    ],
                    "description": "customer_id 1 appears twice — a duplicate row that violates the primary key uniqueness requirement and illustrates the update anomaly risk in un-normalized data."
                }
            ]
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 7: orders
# orders(order_id, customer_id, delivery_minutes) — the many side of 1:M.
# customer_id is a foreign key referencing customers.customer_id.
# ─────────────────────────────────────────────────────────────────────────────
orders = {
    "asset_id": "ds_orders",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship_db",
    "title": "QuickShip Orders Table",
    "description": (
        "The orders entity table: order_id (primary key), customer_id (foreign key → customers), "
        "delivery_minutes. Used to teach foreign keys, referential integrity, one-to-many "
        "relationships, and normalization. Multiple orders per customer demonstrate the 1:M relationship."
    ),
    "columns": [
        {
            "name": "order_id",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": "Primary key — unique integer label for each order (not a quantity)"
        },
        {
            "name": "customer_id",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": "Foreign key referencing customers.customer_id — identifies which customer placed this order"
        },
        {
            "name": "delivery_minutes",
            "type": "integer",
            "semantic_role": "numerical",
            "unit": "minutes",
            "description": "Actual delivery time in minutes"
        }
    ],
    "rows": [
        # order_id, customer_id, delivery_minutes
        # Teaching block uses order 101, 103 explicitly
        [101, 1, 22],
        [102, 2, 28],
        [103, 1, 35],
        [104, 3, 20],
        [105, 4, 30],
        [106, 2, 24],
        [107, 5, 18]
    ],
    "provenance": "authored",
    "variants": [
        {
            # Orphan record variant: add an order with customer_id=99 (no such customer)
            # Teaching block: "an order row with customer_id = 99 would be an orphan if no customer 99 exists"
            "variant_id": "ds_orders.with_orphan",
            "derived_from": "ds_orders",
            "purpose": "Orphan-record variant: order 108 references customer_id 99 which does not exist in the customers table, illustrating a referential integrity violation.",
            "ops": [
                # Set customer_id of order 107 to 99 (non-existent customer)
                {"op": "set_cell", "where": {"order_id": 107}, "column": "customer_id", "value": 99}
            ],
            "planted_issues": [
                {
                    "issue_id": "issue_orphan_customer_id",
                    "kind": "impossible_value",
                    "locations": [
                        {"where": {"order_id": 107}, "column": "customer_id"}
                    ],
                    "description": "customer_id 99 does not exist in the customers table — this order row is an orphan record that violates referential integrity.",
                    "rule": {"column": "customer_id", "op": "eq", "value": 99}
                }
            ]
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 8: products
# products(product_id, name) — independent entity.
# Teaching block mentions: rice bag, cooking oil.
# ─────────────────────────────────────────────────────────────────────────────
products = {
    "asset_id": "ds_products",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship_db",
    "title": "QuickShip Products Table",
    "description": (
        "The products entity table: product_id (primary key), name. "
        "An independent entity — a product can exist without any orders. "
        "Used to teach many-to-many relationships and junction tables. "
        "Includes the rice bag and cooking oil mentioned in teaching blocks."
    ),
    "columns": [
        {
            "name": "product_id",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": "Primary key — unique integer label for each product (not a quantity)"
        },
        {
            "name": "name",
            "type": "string",
            "semantic_role": "text",
            "description": "Product name"
        }
    ],
    "rows": [
        # product_id, name
        [10, "Rice bag"],
        [11, "Cooking oil"],
        [12, "Tomato paste"],
        [13, "Bottled water"],
        [14, "Laundry detergent"]
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 9: order_items
# order_items(order_id, product_id) — junction table resolving M:N.
# Teaching block: order 101 + rice bag, order 101 + cooking oil, order 103 + rice bag.
# Composite PK: (order_id, product_id).
# ─────────────────────────────────────────────────────────────────────────────
order_items = {
    "asset_id": "ds_order_items",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship_db",
    "title": "QuickShip Order Items Table (Junction)",
    "description": (
        "Junction table resolving the many-to-many relationship between orders and products. "
        "Each row is one (order, product) pairing. Composite primary key: (order_id, product_id). "
        "Teaching block pairings: order 101 with rice bag (product 10), "
        "order 101 with cooking oil (product 11), order 103 with rice bag (product 10)."
    ),
    "columns": [
        {
            "name": "order_id",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": "Foreign key referencing orders.order_id — part of composite primary key"
        },
        {
            "name": "product_id",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": "Foreign key referencing products.product_id — part of composite primary key"
        }
    ],
    "rows": [
        # order_id, product_id
        [101, 10],   # order 101 — rice bag
        [101, 11],   # order 101 — cooking oil
        [102, 12],   # order 102 — tomato paste
        [103, 10],   # order 103 — rice bag (same product, different order)
        [104, 13],   # order 104 — bottled water
        [105, 14],   # order 105 — laundry detergent
        [106, 10],   # order 106 — rice bag
        [107, 11]    # order 107 — cooking oil
    ],
    "provenance": "authored"
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 10: customers_pk_candidates
# A table with multiple candidate key columns to teach primary key selection.
# Includes a column with duplicates, a column with nulls, and a valid PK column.
# ─────────────────────────────────────────────────────────────────────────────
customers_pk_candidates = {
    "asset_id": "ds_customers_pk_candidates",
    "asset_kind": "dataset",
    "scenario_id": "scen_quickship_db",
    "title": "QuickShip Customer Candidate Keys Table",
    "description": (
        "A customers table with four candidate columns to evaluate as primary key: "
        "customer_id (valid PK: unique, never null), name (fails: two customers share a name), "
        "phone (fails: one null), signup_date (fails: two customers signed up on the same date). "
        "Used to teach primary key selection and entity integrity."
    ),
    "columns": [
        {
            "name": "customer_id",
            "type": "integer",
            "semantic_role": "identifier",
            "numeric_looking_label": True,
            "description": "Valid primary key candidate: unique integer, never null"
        },
        {
            "name": "name",
            "type": "string",
            "semantic_role": "text",
            "description": "Customer name — fails as PK because two customers share a name"
        },
        {
            "name": "phone",
            "type": "string",
            "semantic_role": "text",
            "description": "Phone number — fails as PK because one row has a null value"
        },
        {
            "name": "signup_date",
            "type": "date",
            "semantic_role": "datetime",
            "description": "Signup date — fails as PK because two customers share the same date"
        }
    ],
    "rows": [
        # customer_id, name, phone, signup_date
        [1, "Amara Okafor",  "+234-801-111-0001", "2024-01-15"],
        [2, "Emeka Nwosu",   "+234-802-222-0002", "2024-01-15"],
        [3, "Fatima Bello",  "+234-803-333-0003", "2024-02-10"],
        [4, "Chidi Eze",     None,                "2024-02-20"],
        [5, "Amara Okafor",  "+234-805-555-0005", "2024-03-05"]
    ],
    "provenance": "authored",
    "variants": [
        {
            # Variant highlighting the duplicate name issue
            "variant_id": "ds_customers_pk_candidates.name_dup_highlighted",
            "derived_from": "ds_customers_pk_candidates",
            "purpose": "Highlights the duplicate-name issue: customer 5 shares the name 'Amara Okafor' with customer 1, showing why name fails as a primary key.",
            "ops": [],
            "planted_issues": [
                {
                    "issue_id": "issue_duplicate_name",
                    "kind": "inconsistent_category",
                    "locations": [
                        {"where": {"customer_id": 1}, "column": "name"},
                        {"where": {"customer_id": 5}, "column": "name"}
                    ],
                    "description": "Two customers share the name 'Amara Okafor' — name is not unique and therefore cannot serve as a primary key.",
                    "rule": {"column": "name", "op": "casing_differs_from_siblings"}
                }
            ]
        },
        {
            # Variant highlighting the null phone issue
            "variant_id": "ds_customers_pk_candidates.phone_null_highlighted",
            "derived_from": "ds_customers_pk_candidates",
            "purpose": "Highlights the null phone issue: customer 4 has no phone number, showing why phone fails as a primary key (entity integrity requires no nulls in the PK).",
            "ops": [],
            "planted_issues": [
                {
                    "issue_id": "issue_null_phone",
                    "kind": "missing_value",
                    "locations": [
                        {"where": {"customer_id": 4}, "column": "phone"}
                    ],
                    "description": "Customer 4 has a null phone value — phone cannot serve as a primary key because entity integrity requires the PK to be never null."
                }
            ]
        }
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# Assemble registry
# ─────────────────────────────────────────────────────────────────────────────
registry["assets"] = [
    delivery_times_sample,
    delivery_frequency_table,
    delivery_orders_extended,
    correlation_matrix,
    city_delivery_summary,
    customers,
    orders,
    products,
    order_items,
    customers_pk_candidates
]

registry["provenance"] = {
    "model": "claude-opus-4-5",
    "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
}

out_path = "batches/final_batch_003_da_chunk/scenario_asset_registry.json"
with open(out_path, "w") as f:
    json.dump(registry, f, indent=2)

print(f"Written: {out_path}")
print(f"Scenarios: {len(registry['scenarios'])}")
print(f"Assets: {len(registry['assets'])}")
for a in registry['assets']:
    ncols = len(a.get('columns', []))
    nrows = len(a.get('rows', []))
    nvars = len(a.get('variants', []))
    print(f"  {a['asset_id']}: {ncols} cols, {nrows} rows, {nvars} variants")
