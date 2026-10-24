#!/usr/bin/env python3
"""Build interactions.part.c2.json for chunk c2:
  tile_datamodel_normalization_many_to_many
  tile_datamodel_dimensional_er
  tile_stakeholder_recommendation_translation
"""
import json, sys

# ── Load inputs ──────────────────────────────────────────────────────────────
with open("batches/final_batch_003_da_chunk/tile_plans.json") as f:
    plans_raw = json.load(f)
with open("batches/final_batch_003_da_chunk/inputs/path_glossary_bundle.json") as f:
    gb = json.load(f)
with open("batches/final_batch_003_da_chunk/scenario_asset_registry.json") as f:
    sar = json.load(f)
with open("batches/final_batch_003_da_chunk/screens.json") as f:
    screens_raw = json.load(f)

# ── Index helpers ─────────────────────────────────────────────────────────────
plans = {t["tile_id"]: t for t in plans_raw["tiles"]}
screens = {t["tile_id"]: t for t in screens_raw["tiles"]}
bundles = {b["context"]["concept_id"]: b for b in gb["bundles"]}
assets = {a["asset_id"]: a for a in sar["assets"]}

TARGET = [
    "tile_datamodel_normalization_many_to_many",
    "tile_datamodel_dimensional_er",
    "tile_stakeholder_recommendation_translation",
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def ix_id(step_id):
    return f"ix.{step_id}"

def anchor(concept_id, kind, capability=None):
    if capability:
        return f"{concept_id}#assessment:{capability}"
    return f"{concept_id}#{kind}"

def measure(concept_id, capability, fact_ids):
    return {"concept_id": concept_id, "capability": capability, "fact_ids": fact_ids}

def feedback(correct_msg, incorrect_msg, hints, remediation_step_id=None):
    fb = {
        "correct": {"message": correct_msg},
        "incorrect": {"message": incorrect_msg},
        "hints": hints,
    }
    if remediation_step_id:
        fb["remediation_step_id"] = remediation_step_id
    return fb

# ── Verify asset rows ─────────────────────────────────────────────────────────
def get_rows(asset_id, variant_id=None):
    a = assets[asset_id]
    if variant_id is None:
        return a["rows"], a["columns"]
    for v in a.get("variants", []):
        if v["variant_id"] == variant_id:
            # Apply ops to base rows
            import copy
            rows = copy.deepcopy(a["rows"])
            cols = [c["name"] for c in a["columns"]]
            for op in v.get("ops", []):
                if op["op"] == "drop_rows":
                    where = op["where"]
                    rows = [r for r in rows if not all(r[cols.index(k)] == v2 for k, v2 in where.items())]
                elif op["op"] == "set_cell":
                    where = op["where"]
                    col = op["column"]
                    val = op["value"]
                    for r in rows:
                        if all(r[cols.index(k)] == v2 for k, v2 in where.items()):
                            r[cols.index(col)] = val
                elif op["op"] == "duplicate_row":
                    where = op["where"]
                    for r in rows:
                        if all(r[cols.index(k)] == v2 for k, v2 in where.items()):
                            rows.append(list(r))
                            break
            return rows, a["columns"]
    raise KeyError(f"variant {variant_id} not found in {asset_id}")

def cell_value(asset_id, where, column, variant_id=None):
    rows, cols = get_rows(asset_id, variant_id)
    col_names = [c["name"] for c in cols]
    col_idx = col_names.index(column)
    for r in rows:
        if all(r[col_names.index(k)] == v for k, v in where.items()):
            return r[col_idx]
    raise KeyError(f"row {where} not found in {asset_id}")

# ── Verify key values ─────────────────────────────────────────────────────────
# ds_order_items rows: (order_id, product_id)
oi_rows, oi_cols = get_rows("ds_order_items")
oi_col_names = [c["name"] for c in oi_cols]
print("order_items rows:", oi_rows)

# ds_customers rows
cust_rows, cust_cols = get_rows("ds_customers")
cust_col_names = [c["name"] for c in cust_cols]
print("customers rows:", cust_rows)

# ds_city_delivery_summary rows
city_rows, city_cols = get_rows("ds_city_delivery_summary")
city_col_names = [c["name"] for c in city_cols]
print("city_delivery_summary rows:", city_rows)
print("city_delivery_summary cols:", city_col_names)

# ── Tile 1: tile_datamodel_normalization_many_to_many ─────────────────────────
# Steps: s03 (check/choice), s04 (hands_on/find_issues), s08 (check/choice), s09 (hands_on/table_select)

# s03: check / choice
# Anchor: datamodel.normalization_basics#assessment:split_a_table_to_remove_redundancy
# Facts tested: f3 (taught in s02)
# Lede: "A single orders table stores customer_id, customer_name, customer_city, and delivery_minutes on every row. Which change removes the redundancy?"
s03 = {
    "step_id": "tile_datamodel_normalization_many_to_many.s03",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_datamodel_normalization_many_to_many.s03"),
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("datamodel.normalization_basics", "split_a_table_to_remove_redundancy", ["f3"])
        ],
        "anchors": [
            anchor("datamodel.normalization_basics", "assessment", "split_a_table_to_remove_redundancy")
        ],
        "public": {
            "prompt": "A single orders table stores customer_id, customer_name, customer_city, and delivery_minutes on every row. A customer with five orders has their name and city repeated five times. Which change removes that redundancy?",
            "options": [
                {"option_id": "opt_split", "text": "Move customer_name and customer_city into a separate customers table, linked back by customer_id"},
                {"option_id": "opt_index", "text": "Add an index on customer_name to speed up lookups"},
                {"option_id": "opt_null", "text": "Replace repeated customer_name values with NULL after the first row"},
                {"option_id": "opt_sort", "text": "Sort the table by customer_id so repeated rows are grouped together"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_split"],
            "option_feedback": {
                "opt_split": {"message": "Correct. Moving the repeating data into a separate table and linking it by key is exactly how normalization removes redundancy — each customer's name and city is stored once."},
                "opt_index": {"message": "Not quite. An index speeds up queries but does not remove the repeated data; the name and city are still stored five times."},
                "opt_null": {"message": "Not quite. Replacing repeated values with NULL would break the data — you would lose the customer's name and city for most orders. Normalization moves the data to a separate table, not removes it."},
                "opt_sort": {"message": "Not quite. Sorting groups the repeated rows visually but does not remove the redundancy — the name and city are still stored five times, and an update anomaly is still possible."}
            }
        },
        "feedback": feedback(
            "Exactly right. Splitting the repeating data into a separate table and linking by key is the normalization move that removes redundancy.",
            "Remember: normalization removes redundancy by moving repeating data into a new table linked by a key column.",
            [
                "Think about what 'removing redundancy' means — the data should be stored only once.",
                "Which option actually changes where the data lives, rather than just changing how it looks or how fast it can be found?"
            ],
            "tile_datamodel_normalization_many_to_many.r01"
        )
    }
}

# s04: hands_on / find_issues
# Anchor: datamodel.normalization_basics#practice, #assessment:identify_redundancy_and_its_update_problem, #assessment:split_a_table_to_remove_redundancy
# Facts tested: f1, f2, f3 (all taught by s01+s02)
# Use ds_customers.with_duplicate variant — planted issue: issue_duplicate_customer
# The practice success: "The written recommendation names a specific finding..." — wait, that's stakeholder.
# normalization_basics practice: "The learner identifies which columns repeat across rows, names the update anomaly risk, and describes the split into two tables."
# Actually the practice_anchor for normalization_basics is:
#   type: data_cleanup
#   objective: Given a denormalized table, identify which columns repeat across rows, explain the update anomaly risk, and describe the split into two tables.
#   success: The learner identifies the repeating columns, names the update anomaly risk, and correctly describes the two-table split.
# The planned_interaction_type is find_issues.
# We need to use a dataset with planted issues. The ds_customers.with_duplicate has issue_duplicate_customer.
# But the lede says "orders table has customer details repeated on every row" — this is about normalization redundancy.
# The find_issues interaction should use ds_customers.with_duplicate to find the duplicate row.
# issue_id must match the planted_issues from the variant.

s04 = {
    "step_id": "tile_datamodel_normalization_many_to_many.s04",
    "interaction": {
        "type": "find_issues",
        "interaction_id": ix_id("tile_datamodel_normalization_many_to_many.s04"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("datamodel.normalization_basics", "identify_redundancy_and_its_update_problem", ["f1", "f2"]),
            measure("datamodel.normalization_basics", "split_a_table_to_remove_redundancy", ["f3"])
        ],
        "anchors": [
            anchor("datamodel.normalization_basics", "practice"),
            anchor("datamodel.normalization_basics", "assessment", "identify_redundancy_and_its_update_problem"),
            anchor("datamodel.normalization_basics", "assessment", "split_a_table_to_remove_redundancy")
        ],
        "public": {
            "asset_ref": {
                "asset_id": "ds_customers",
                "variant_id": "ds_customers.with_duplicate",
                "columns": ["customer_id", "name", "city"]
            },
            "instructions": "The table below shows a customers table where a data entry error has introduced a duplicate row. Flag the cell that reveals the redundancy problem — the repeated customer_id that would cause an update anomaly if the customer's details changed.",
            "categories": [
                {"category_id": "cat_redundant_row", "label": "Redundant row — update anomaly risk"},
                {"category_id": "cat_clean", "label": "Clean — no redundancy issue"}
            ],
            "goal_count": 1
        },
        "grading": {
            "issues": [
                {
                    "issue_id": "issue_duplicate_customer",
                    "category_id": "cat_redundant_row",
                    "locations": [
                        {"where": {"customer_id": 1}, "column": "customer_id", "occurrence": 0},
                        {"where": {"customer_id": 1}, "column": "customer_id", "occurrence": 1}
                    ],
                    "explanation": "customer_id 1 appears twice. This duplicate row means that if Amara Okafor's city changes, both rows must be updated — missing one creates an update anomaly where the same customer appears to live in two different cities."
                }
            ],
            "decoys": [
                {
                    "location": {"where": {"customer_id": 2}, "column": "customer_id", "occurrence": 0},
                    "message": "customer_id 2 (Emeka Nwosu) appears only once — no redundancy here."
                },
                {
                    "location": {"where": {"customer_id": 3}, "column": "customer_id", "occurrence": 0},
                    "message": "customer_id 3 (Fatima Bello) appears only once — no redundancy here."
                }
            ],
            "wrong_category_message": "You found the duplicate row, but check the category. A repeated customer_id is a redundancy problem — it creates an update anomaly risk, not a clean record.",
            "completion_message": "Well done. You identified the duplicate row for customer_id 1. Storing the same customer twice means any update to their details must be applied to both rows — missing one leaves inconsistent data."
        },
        "feedback": feedback(
            "Correct. The duplicate row for customer_id 1 is the redundancy problem. If the customer's city changes, both rows must be updated — missing one creates an update anomaly.",
            "Look for a customer_id that appears more than once. That repeated row is the redundancy that normalization removes.",
            [
                "Scan the customer_id column for any value that appears more than once.",
                "A redundant row means the same customer's details are stored twice — what happens if their city changes?"
            ],
            "tile_datamodel_normalization_many_to_many.r01"
        )
    }
}

# s08: check / choice
# Anchor: datamodel.many_to_many_junction_tables#assessment:design_the_junction_table_keys
# Facts tested: f2, f3 (taught in s06)
# Lede: "A junction table called enrollments resolves a many-to-many between students and courses. Which columns must it contain, and what forms its primary key?"
s08 = {
    "step_id": "tile_datamodel_normalization_many_to_many.s08",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_datamodel_normalization_many_to_many.s08"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("datamodel.many_to_many_junction_tables", "design_the_junction_table_keys", ["f2", "f3"])
        ],
        "anchors": [
            anchor("datamodel.many_to_many_junction_tables", "assessment", "design_the_junction_table_keys")
        ],
        "public": {
            "prompt": "A junction table called enrollments resolves a many-to-many relationship between students and courses. Which columns must it contain, and what forms its primary key?",
            "options": [
                {"option_id": "opt_correct", "text": "It must contain student_id and course_id as foreign keys; the pair (student_id, course_id) forms the primary key"},
                {"option_id": "opt_one_fk", "text": "It must contain only student_id as a foreign key; course_id is optional"},
                {"option_id": "opt_new_pk", "text": "It must contain student_id and course_id, but needs a separate enrollment_id as its primary key"},
                {"option_id": "opt_no_fk", "text": "It must contain student_name and course_name so the data is self-contained"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_correct"],
            "option_feedback": {
                "opt_correct": {"message": "Correct. The junction table must contain the primary keys of both original tables as foreign keys, and the combination of those two foreign keys forms the primary key of the junction table."},
                "opt_one_fk": {"message": "Not quite. A junction table must contain the primary keys of both original tables as foreign keys — both student_id and course_id are required to record which student is enrolled in which course."},
                "opt_new_pk": {"message": "Not quite. While a separate surrogate key is sometimes added, the combination of the two foreign keys (student_id, course_id) is what makes the primary key of the junction table — that pair is unique because the same student won't enrol in the same course twice."},
                "opt_no_fk": {"message": "Not quite. Storing names instead of keys reintroduces redundancy and breaks the relational link. The junction table must contain the primary keys of both original tables as foreign keys."}
            }
        },
        "feedback": feedback(
            "Exactly right. The junction table holds the primary keys of both original tables as foreign keys, and their combination is the primary key.",
            "Remember: the junction table must contain the primary keys of both original tables as foreign keys, and those two keys together form the junction table's primary key.",
            [
                "What two pieces of information does the junction table need to record a single enrollment?",
                "The primary key of the junction table must uniquely identify each pairing — what combination of columns achieves that?"
            ],
            "tile_datamodel_normalization_many_to_many.r02"
        )
    }
}

# s09: hands_on / table_select
# Anchor: datamodel.many_to_many_junction_tables#practice, #assessment:recognize_that_many_to_many_needs_a_junction_table, #assessment:design_the_junction_table_keys
# Facts tested: f1, f2, f3 (all taught by s05+s06)
# Use ds_order_items (the junction table) — select the FK columns and the composite PK pair
# Verify values from the data
oi_order_id_col = "order_id"
oi_product_id_col = "product_id"
# First row: order_id=101, product_id=10
first_row_order_id = cell_value("ds_order_items", {"order_id": 101, "product_id": 10}, "order_id")
first_row_product_id = cell_value("ds_order_items", {"order_id": 101, "product_id": 10}, "product_id")
print(f"order_items first row: order_id={first_row_order_id}, product_id={first_row_product_id}")

s09 = {
    "step_id": "tile_datamodel_normalization_many_to_many.s09",
    "interaction": {
        "type": "table_select",
        "interaction_id": ix_id("tile_datamodel_normalization_many_to_many.s09"),
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("datamodel.many_to_many_junction_tables", "recognize_that_many_to_many_needs_a_junction_table", ["f1"]),
            measure("datamodel.many_to_many_junction_tables", "design_the_junction_table_keys", ["f2", "f3"])
        ],
        "anchors": [
            anchor("datamodel.many_to_many_junction_tables", "practice"),
            anchor("datamodel.many_to_many_junction_tables", "assessment", "recognize_that_many_to_many_needs_a_junction_table"),
            anchor("datamodel.many_to_many_junction_tables", "assessment", "design_the_junction_table_keys")
        ],
        "public": {
            "asset_ref": {
                "asset_id": "ds_order_items",
                "variant_id": None,
                "columns": ["order_id", "product_id"]
            },
            "intro": "The order_items table is the junction table that resolves the many-to-many relationship between orders and products. Each row records one order/product pairing.",
            "tasks": [
                {
                    "task_id": "task_fk_order",
                    "prompt": "Select the column that is a foreign key referencing the orders table.",
                    "target_kind": "column"
                },
                {
                    "task_id": "task_fk_product",
                    "prompt": "Select the column that is a foreign key referencing the products table.",
                    "target_kind": "column"
                },
                {
                    "task_id": "task_pk_pair_order",
                    "prompt": "Select a cell in the order_id column that is part of the composite primary key for the first pairing (order 101 with the rice bag, product 10).",
                    "target_kind": "cell"
                },
                {
                    "task_id": "task_pk_pair_product",
                    "prompt": "Select a cell in the product_id column that completes the composite primary key for that same first pairing.",
                    "target_kind": "cell"
                }
            ]
        },
        "grading": {
            "answers": [
                {
                    "task_id": "task_fk_order",
                    "column": "order_id"
                },
                {
                    "task_id": "task_fk_product",
                    "column": "product_id"
                },
                {
                    "task_id": "task_pk_pair_order",
                    "row": {"where": {"order_id": 101, "product_id": 10}, "occurrence": 0},
                    "column": "order_id",
                    "expect_value": first_row_order_id
                },
                {
                    "task_id": "task_pk_pair_product",
                    "row": {"where": {"order_id": 101, "product_id": 10}, "occurrence": 0},
                    "column": "product_id",
                    "expect_value": first_row_product_id
                }
            ],
            "task_feedback": {
                "task_fk_order": {
                    "correct": "Correct. order_id is a foreign key referencing orders.order_id — it links each row back to the order it belongs to.",
                    "incorrect": "Not quite. Look for the column that references the orders table by storing the order's primary key."
                },
                "task_fk_product": {
                    "correct": "Correct. product_id is a foreign key referencing products.product_id — it links each row to the product included in that order.",
                    "incorrect": "Not quite. Look for the column that references the products table by storing the product's primary key."
                },
                "task_pk_pair_order": {
                    "correct": "Correct. order_id 101 is the first half of the composite primary key for this pairing.",
                    "incorrect": "Not quite. Select the order_id value in the row where order 101 is paired with product 10 (the rice bag)."
                },
                "task_pk_pair_product": {
                    "correct": "Correct. product_id 10 completes the composite primary key (101, 10) — this pair is unique because the same order won't list the same product twice.",
                    "incorrect": "Not quite. Select the product_id value in the row where order 101 is paired with product 10 (the rice bag)."
                }
            }
        },
        "feedback": feedback(
            "Well done. You identified both foreign key columns and the composite primary key pair — the two foreign keys together uniquely identify each order/product pairing.",
            "Review the junction table structure. Each column is a foreign key to one of the original tables, and together they form the composite primary key.",
            [
                "Each column in the junction table is a foreign key to one of the two original tables — which table does each column reference?",
                "The composite primary key is the pair of foreign keys — find the row where order 101 is paired with product 10."
            ],
            "tile_datamodel_normalization_many_to_many.r02"
        )
    }
}

# ── Tile 2: tile_datamodel_dimensional_er ─────────────────────────────────────
# Steps: s03 (check/choice), s04 (hands_on/classify)

# s03: check / choice
# Anchor: datamodel.er_diagram_reading#assessment:read_relationship_cardinality_markings
# Facts tested: f3, f4 (taught in s01)
# Lede: "A relationship line between Customer and Order has a three-pronged symbol on the Order side and a one-and-only-one symbol on the Customer side. What does this mean?"
s03_er = {
    "step_id": "tile_datamodel_dimensional_er.s03",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_datamodel_dimensional_er.s03"),
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("datamodel.er_diagram_reading", "read_relationship_cardinality_markings", ["f3", "f4"])
        ],
        "anchors": [
            anchor("datamodel.er_diagram_reading", "assessment", "read_relationship_cardinality_markings")
        ],
        "public": {
            "prompt": "A relationship line between Customer and Order has a three-pronged symbol on the Order side and a one-and-only-one symbol on the Customer side. What does this mean?",
            "options": [
                {"option_id": "opt_one_to_many", "text": "Each customer must have exactly one order, and each order can belong to many customers"},
                {"option_id": "opt_correct", "text": "Each customer must exist (mandatory), and one customer can be linked to many orders"},
                {"option_id": "opt_many_to_many", "text": "Many customers can be linked to many orders"},
                {"option_id": "opt_optional", "text": "A customer may have zero or one order, and each order belongs to exactly one customer"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_correct"],
            "option_feedback": {
                "opt_correct": {"message": "Correct. The one-and-only-one symbol on the Customer side means each order must be linked to exactly one customer (mandatory). The three-pronged symbol on the Order side means one customer can be linked to many orders — a one-to-many relationship."},
                "opt_one_to_many": {"message": "Not quite. The three-pronged symbol is on the Order side, meaning 'many orders' per customer — not 'many customers' per order. The one-and-only-one symbol on the Customer side means each order belongs to exactly one customer."},
                "opt_many_to_many": {"message": "Not quite. A many-to-many relationship would require three-pronged symbols on both sides. Here only the Order side has the three-pronged symbol, making this a one-to-many relationship."},
                "opt_optional": {"message": "Not quite. A 'zero or one' symbol would show a zero and a one together. The one-and-only-one symbol means mandatory — exactly one customer per order, not zero or one."}
            }
        },
        "feedback": feedback(
            "Correct. The three-pronged symbol means 'many' on the Order side; the one-and-only-one symbol means each order must belong to exactly one customer.",
            "Remember: a three-pronged symbol means 'many'; a one-and-only-one symbol means that side is mandatory (exactly one).",
            [
                "Which side of the line has the three-pronged symbol? That side is the 'many' side.",
                "The one-and-only-one symbol means that side is mandatory — every order must be linked to exactly one customer."
            ],
            "tile_datamodel_dimensional_er.r01"
        )
    }
}

# s04: hands_on / classify
# Anchor: datamodel.er_diagram_reading#practice, #assessment:identify_entities_and_attributes_in_an_erd, #assessment:read_relationship_cardinality_markings
# Facts tested: f1, f2, f3, f4 (all taught in s01)
# Practice success: "The learner names each box as an entity, finds each underlined key, and reads each relationship line as one-to-one, one-to-many or many-to-many with the correct side marked many or mandatory."
# Use classify: items are ERD elements, buckets are entity/attribute/primary_key/relationship_type
# Items should come from the QuickShip ERD (customers, orders, products, order_items)
# No asset with planted issues needed — this is a conceptual classify
# The classify anchor is about a trap: numeric-looking labels (customer_id looks like a number but is a label)
# We need a trap item per the "mistakes to avoid" rule for classify with a trap anchor

s04_er = {
    "step_id": "tile_datamodel_dimensional_er.s04",
    "interaction": {
        "type": "classify",
        "interaction_id": ix_id("tile_datamodel_dimensional_er.s04"),
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("datamodel.er_diagram_reading", "identify_entities_and_attributes_in_an_erd", ["f1", "f2"]),
            measure("datamodel.er_diagram_reading", "read_relationship_cardinality_markings", ["f3", "f4"])
        ],
        "anchors": [
            anchor("datamodel.er_diagram_reading", "practice"),
            anchor("datamodel.er_diagram_reading", "assessment", "identify_entities_and_attributes_in_an_erd"),
            anchor("datamodel.er_diagram_reading", "assessment", "read_relationship_cardinality_markings")
        ],
        "public": {
            "prompt": "The QuickShip ER diagram contains four entity boxes (Customer, Order, Product, Order_Item), attribute ovals, underlined primary keys, and relationship lines. Classify each element below as it would appear in the diagram.",
            "buckets": [
                {"bucket_id": "bkt_entity", "label": "Entity (rectangle/box)"},
                {"bucket_id": "bkt_attribute", "label": "Attribute (oval)"},
                {"bucket_id": "bkt_pk", "label": "Primary key attribute (underlined oval)"},
                {"bucket_id": "bkt_rel_one_to_many", "label": "One-to-many relationship line"},
                {"bucket_id": "bkt_rel_many_to_many", "label": "Many-to-many relationship line"}
            ],
            "items": [
                {"item_id": "item_customer_box", "text": "Customer — the rectangle labelled 'Customer'"},
                {"item_id": "item_order_box", "text": "Order — the rectangle labelled 'Order'"},
                {"item_id": "item_customer_id_oval", "text": "customer_id — the oval attached to Customer, with its name underlined"},
                {"item_id": "item_city_oval", "text": "city — the oval attached to Customer, name not underlined"},
                {"item_id": "item_customer_order_line", "text": "The line between Customer and Order (three-pronged symbol on the Order side)"},
                {"item_id": "item_order_product_line", "text": "The line between Order and Product (three-pronged symbols on both sides, resolved via Order_Item)"},
                {"item_id": "item_order_item_box", "text": "Order_Item — the rectangle labelled 'Order_Item'"},
                {"item_id": "item_trap_customer_id_number", "text": "customer_id = 1 — the integer value stored in the first row of the customers table"}
            ]
        },
        "grading": {
            "assignments": {
                "item_customer_box": "bkt_entity",
                "item_order_box": "bkt_entity",
                "item_customer_id_oval": "bkt_pk",
                "item_city_oval": "bkt_attribute",
                "item_customer_order_line": "bkt_rel_one_to_many",
                "item_order_product_line": "bkt_rel_many_to_many",
                "item_order_item_box": "bkt_entity",
                "item_trap_customer_id_number": "bkt_attribute"
            },
            "role_map": {
                "bkt_entity": "entity",
                "bkt_attribute": "attribute",
                "bkt_pk": "primary_key_attribute",
                "bkt_rel_one_to_many": "one_to_many_relationship",
                "bkt_rel_many_to_many": "many_to_many_relationship"
            },
            "item_feedback": {
                "item_customer_box": {"message": "Correct. In an ERD, an entity type is represented by its name inside a rectangle — Customer is an entity box."},
                "item_order_box": {"message": "Correct. Order is an entity type, drawn as a rectangle labelled 'Order'."},
                "item_customer_id_oval": {"message": "Correct. customer_id is the primary key attribute of Customer — it is shown as an oval with its name underlined."},
                "item_city_oval": {"message": "Correct. city is a regular attribute of Customer — shown as an oval without underlining, since it is not the primary key."},
                "item_customer_order_line": {"message": "Correct. The three-pronged symbol on the Order side means 'many orders per customer' — a one-to-many relationship line."},
                "item_order_product_line": {"message": "Correct. Three-pronged symbols on both sides indicate a many-to-many relationship between Order and Product (resolved in the schema by the Order_Item junction table)."},
                "item_order_item_box": {"message": "Correct. Order_Item is an entity type (the junction/composite entity), drawn as a rectangle in the ERD."},
                "item_trap_customer_id_number": {"message": "This is a data value (the integer 1 stored in a row), not an ERD element. In an ERD, customer_id appears as an underlined oval (a primary key attribute), not as a row value. The ERD shows structure, not data."}
            }
        },
        "feedback": feedback(
            "Excellent. You correctly identified entities, attributes, primary keys, and relationship types — and recognised that a data value is not an ERD element.",
            "Review the ERD notation: rectangles are entities, ovals are attributes, underlined ovals are primary keys, and lines with cardinality markings show relationships.",
            [
                "In an ERD, shapes matter: rectangles are entities, ovals are attributes. Is the item a shape in the diagram or a value in a table row?",
                "For relationship lines, count the prongs: one prong on each side means one-to-one; three prongs on one side means one-to-many; three prongs on both sides means many-to-many."
            ],
            "tile_datamodel_dimensional_er.r01"
        )
    }
}

# ── Tile 3: tile_stakeholder_recommendation_translation ───────────────────────
# Steps: s02 (check/choice), s03 (hands_on/table_select), s05 (check/choice), s06 (hands_on/classify)

# s02: check / choice
# Anchor: stakeholder.data_driven_recommendation#assessment:write_data_grounded_recommendation
# Facts tested: f1, f2 (taught in s01)
# Lede: "Which of the following best follows the 'because we found X, we recommend Y' pattern for a finding that average Kano delivery times rose from 21 to 22.5 minutes?"
# Verify: Kano Month 1 avg = 21.0, Month 2 avg = 22.5
kano_m1 = cell_value("ds_city_delivery_summary", {"city": "Kano", "month": "Month 1"}, "avg_delivery_minutes")
kano_m2 = cell_value("ds_city_delivery_summary", {"city": "Kano", "month": "Month 2"}, "avg_delivery_minutes")
print(f"Kano Month 1 avg: {kano_m1}, Month 2 avg: {kano_m2}")

s02_stk = {
    "step_id": "tile_stakeholder_recommendation_translation.s02",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_stakeholder_recommendation_translation.s02"),
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("stakeholder.data_driven_recommendation", "write_data_grounded_recommendation", ["f1", "f2"])
        ],
        "anchors": [
            anchor("stakeholder.data_driven_recommendation", "assessment", "write_data_grounded_recommendation")
        ],
        "public": {
            "prompt": f"Average Kano delivery times rose from {kano_m1} to {kano_m2} minutes between Month 1 and Month 2. Which option best follows the 'because we found X, we recommend Y' pattern?",
            "options": [
                {"option_id": "opt_correct", "text": f"Because average Kano delivery times rose from {kano_m1} to {kano_m2} minutes, we recommend adding a courier to the Kano route."},
                {"option_id": "opt_no_finding", "text": "We recommend adding a courier to the Kano route to improve performance."},
                {"option_id": "opt_vague", "text": "Because delivery times have been increasing, we recommend reviewing operations."},
                {"option_id": "opt_reversed", "text": "We should add a courier to the Kano route because that is what the operations manager wants."}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_correct"],
            "option_feedback": {
                "opt_correct": {"message": f"Correct. This recommendation names the specific finding ({kano_m1} to {kano_m2} minutes) and connects it directly to a concrete action (adding a courier) — exactly the 'because X, we recommend Y' pattern."},
                "opt_no_finding": {"message": "Not quite. This recommendation states an action but gives no data finding to justify it. A data-driven recommendation must cite the specific finding that supports the action."},
                "opt_vague": {"message": "Not quite. 'Delivery times have been increasing' is too vague — it does not cite the specific numbers. A data-driven recommendation names the precise finding."},
                "opt_reversed": {"message": "Not quite. This justifies the recommendation by what the manager wants, not by a data finding. The 'because X' part must be a data result, not a stakeholder preference."}
            }
        },
        "feedback": feedback(
            "Correct. A data-driven recommendation names the specific finding and connects it to a concrete action.",
            "Remember: the recommendation must cite the specific data finding ('because we found X') and connect it to a concrete action ('we recommend Y').",
            [
                "Which option actually names a specific number from the data as the reason for the recommendation?",
                "The 'because' clause must be a data result — a specific finding, not a general observation or a stakeholder preference."
            ],
            "tile_stakeholder_recommendation_translation.r01"
        )
    }
}

# s03: hands_on / table_select
# Anchor: stakeholder.data_driven_recommendation#practice, #assessment:write_data_grounded_recommendation
# Facts tested: f1, f2 (taught in s01)
# Practice success: "The written recommendation names a specific finding and connects it directly to a concrete suggested action, with no recommendation left unjustified by the cited data."
# Use ds_city_delivery_summary — select the cells that justify a recommendation
# Lagos Month 1 = 22.0, Month 2 = 30.0 (the big rise)
lagos_m1 = cell_value("ds_city_delivery_summary", {"city": "Lagos", "month": "Month 1"}, "avg_delivery_minutes")
lagos_m2 = cell_value("ds_city_delivery_summary", {"city": "Lagos", "month": "Month 2"}, "avg_delivery_minutes")
print(f"Lagos Month 1 avg: {lagos_m1}, Month 2 avg: {lagos_m2}")

s03_stk = {
    "step_id": "tile_stakeholder_recommendation_translation.s03",
    "interaction": {
        "type": "table_select",
        "interaction_id": ix_id("tile_stakeholder_recommendation_translation.s03"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("stakeholder.data_driven_recommendation", "write_data_grounded_recommendation", ["f1", "f2"])
        ],
        "anchors": [
            anchor("stakeholder.data_driven_recommendation", "practice"),
            anchor("stakeholder.data_driven_recommendation", "assessment", "write_data_grounded_recommendation")
        ],
        "public": {
            "asset_ref": {
                "asset_id": "ds_city_delivery_summary",
                "variant_id": None,
                "columns": ["city", "month", "avg_delivery_minutes", "order_count"]
            },
            "intro": "The table shows average delivery times and order volumes for three cities across two months. Select the cells that provide the strongest data justification for a recommendation to add a courier to the Lagos route.",
            "tasks": [
                {
                    "task_id": "task_baseline_value",
                    "prompt": "Select the cell showing Lagos's average delivery time in Month 1 — the baseline before the increase.",
                    "target_kind": "cell"
                },
                {
                    "task_id": "task_current_value",
                    "prompt": "Select the cell showing Lagos's average delivery time in Month 2 — the value that reveals the problem.",
                    "target_kind": "cell"
                }
            ]
        },
        "grading": {
            "answers": [
                {
                    "task_id": "task_baseline_value",
                    "row": {"where": {"city": "Lagos", "month": "Month 1"}, "occurrence": 0},
                    "column": "avg_delivery_minutes",
                    "expect_value": lagos_m1
                },
                {
                    "task_id": "task_current_value",
                    "row": {"where": {"city": "Lagos", "month": "Month 2"}, "occurrence": 0},
                    "column": "avg_delivery_minutes",
                    "expect_value": lagos_m2
                }
            ],
            "task_feedback": {
                "task_baseline_value": {
                    "correct": f"Correct. {lagos_m1} minutes is the Lagos baseline in Month 1 — the starting point that makes the Month 2 increase meaningful.",
                    "incorrect": "Not quite. Look for the Lagos row in Month 1 and select the average delivery time — that is the baseline before the increase."
                },
                "task_current_value": {
                    "correct": f"Correct. {lagos_m2} minutes in Month 2 is the finding that justifies the recommendation — the rise from {lagos_m1} to {lagos_m2} minutes is the 'because X' in 'because we found X, we recommend Y'.",
                    "incorrect": "Not quite. Look for the Lagos row in Month 2 and select the average delivery time — that is the value that reveals the problem."
                }
            }
        },
        "feedback": feedback(
            f"Well done. The rise from {lagos_m1} to {lagos_m2} minutes in Lagos is the specific finding that justifies a recommendation — 'because average Lagos delivery times rose from {lagos_m1} to {lagos_m2} minutes, we recommend adding a courier to the Lagos route.'",
            "Look for the Lagos rows and select the average delivery time values that show the change between months.",
            [
                "A data-driven recommendation needs a specific 'before' and 'after' value — which city shows the largest change?",
                "Find the Lagos rows and compare the average delivery times across the two months."
            ],
            "tile_stakeholder_recommendation_translation.r01"
        )
    }
}

# s05: check / choice
# Anchor: stakeholder.plain_language_translation#assessment:replace_formal_or_long_word_with_simpler_equivalent
# Facts tested: f2 (taught in s04)
# Lede: "Which word best replaces 'utilise' in the sentence: 'We should utilise the new courier route to reduce delivery times'?"
s05_stk = {
    "step_id": "tile_stakeholder_recommendation_translation.s05",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_stakeholder_recommendation_translation.s05"),
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("stakeholder.plain_language_translation", "replace_formal_or_long_word_with_simpler_equivalent", ["f2"])
        ],
        "anchors": [
            anchor("stakeholder.plain_language_translation", "assessment", "replace_formal_or_long_word_with_simpler_equivalent")
        ],
        "public": {
            "prompt": "Which word best replaces 'utilise' in the sentence: 'We should utilise the new courier route to reduce delivery times'?",
            "options": [
                {"option_id": "opt_use", "text": "use"},
                {"option_id": "opt_employ", "text": "employ"},
                {"option_id": "opt_leverage", "text": "leverage"},
                {"option_id": "opt_implement", "text": "implement"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_use"],
            "option_feedback": {
                "opt_use": {"message": "Correct. 'Use' is the short, everyday word that replaces the formal 'utilise' — plain language prefers the simpler equivalent."},
                "opt_employ": {"message": "Not quite. 'Employ' is also a formal word — it is no simpler than 'utilise'. Plain language calls for the shortest, most everyday word: 'use'."},
                "opt_leverage": {"message": "Not quite. 'Leverage' is a buzzword that is often vague and can be misinterpreted. Plain language avoids jargon and buzzwords; 'use' is the clear, simple choice."},
                "opt_implement": {"message": "Not quite. 'Implement' is a formal word that is longer and less everyday than 'use'. Plain language prefers the short, simple equivalent."}
            }
        },
        "feedback": feedback(
            "Correct. 'Use' is the short, everyday word that replaces the formal 'utilise' — exactly the kind of substitution plain language calls for.",
            "Remember: plain language replaces formal or long words with short, everyday equivalents. 'Utilise' → 'use' is a classic example.",
            [
                "Which of the options is the shortest, most everyday word for the same action?",
                "Plain language avoids formal words like 'utilise', 'employ', and buzzwords like 'leverage' — which option is the simplest?"
            ],
            "tile_stakeholder_recommendation_translation.r02"
        )
    }
}

# s06: hands_on / classify
# Anchor: stakeholder.plain_language_translation#practice, #assessment:restate_technical_result_in_plain_language, #assessment:introduce_specialist_term_with_plain_english_gloss, #assessment:replace_formal_or_long_word_with_simpler_equivalent
# Facts tested: f1, f2 (taught in s04)
# Practice success: "The learner correctly identifies the plain-language rewrite for each technical result and can explain which rule (or both) each rewrite applies."
# Classify: match technical sentences to plain-language rewrites
# Buckets: "Applies rule 1 only (specialist term glossed)", "Applies rule 2 only (formal word replaced)", "Applies both rules"
# Items: plain-language rewrites of technical sentences
# We need a trap item (a rewrite that applies neither rule correctly)

s06_stk = {
    "step_id": "tile_stakeholder_recommendation_translation.s06",
    "interaction": {
        "type": "classify",
        "interaction_id": ix_id("tile_stakeholder_recommendation_translation.s06"),
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            measure("stakeholder.plain_language_translation", "restate_technical_result_in_plain_language", ["f1", "f2"]),
            measure("stakeholder.plain_language_translation", "introduce_specialist_term_with_plain_english_gloss", ["f1"]),
            measure("stakeholder.plain_language_translation", "replace_formal_or_long_word_with_simpler_equivalent", ["f2"])
        ],
        "anchors": [
            anchor("stakeholder.plain_language_translation", "practice"),
            anchor("stakeholder.plain_language_translation", "assessment", "restate_technical_result_in_plain_language"),
            anchor("stakeholder.plain_language_translation", "assessment", "introduce_specialist_term_with_plain_english_gloss"),
            anchor("stakeholder.plain_language_translation", "assessment", "replace_formal_or_long_word_with_simpler_equivalent")
        ],
        "public": {
            "prompt": "Each sentence below is a plain-language rewrite of a technical result. Classify each rewrite by which plain-language rule it applies: Rule 1 — specialist terms are glossed on first use; Rule 2 — formal or long words are replaced with simpler equivalents.",
            "buckets": [
                {"bucket_id": "bkt_rule1_only", "label": "Rule 1 only — specialist term glossed in plain English"},
                {"bucket_id": "bkt_rule2_only", "label": "Rule 2 only — formal word replaced with a simpler one"},
                {"bucket_id": "bkt_both_rules", "label": "Both rules applied"},
                {"bucket_id": "bkt_neither", "label": "Neither rule applied correctly"}
            ],
            "items": [
                {
                    "item_id": "item_gloss_only",
                    "text": "The average (mean) Lagos delivery time rose from 22 to 30 minutes."
                },
                {
                    "item_id": "item_replace_only",
                    "text": "Lagos delivery times got worse this month."
                },
                {
                    "item_id": "item_both",
                    "text": "The average (mean) delivery time — how long each order takes from dispatch to doorstep — rose by 8 minutes, so we recommend adding a courier."
                },
                {
                    "item_id": "item_trap",
                    "text": "Delivery time performance exhibited negative variance this period."
                }
            ]
        },
        "grading": {
            "assignments": {
                "item_gloss_only": "bkt_rule1_only",
                "item_replace_only": "bkt_rule2_only",
                "item_both": "bkt_both_rules",
                "item_trap": "bkt_neither"
            },
            "role_map": {
                "bkt_rule1_only": "rule_1_gloss",
                "bkt_rule2_only": "rule_2_replace",
                "bkt_both_rules": "both_rules",
                "bkt_neither": "neither_rule"
            },
            "item_feedback": {
                "item_gloss_only": {"message": "Correct. 'The average (mean)' glosses the specialist term 'mean' in plain English on first use — Rule 1. No formal words are replaced here, so only Rule 1 applies."},
                "item_replace_only": {"message": "Correct. 'Got worse' replaces the formal phrase 'exhibited negative variance' with a short, everyday equivalent — Rule 2. No specialist term is glossed, so only Rule 2 applies."},
                "item_both": {"message": "Correct. 'The average (mean)' glosses the specialist term (Rule 1), and the sentence uses plain, everyday language throughout rather than formal terms (Rule 2). Both rules are applied."},
                "item_trap": {"message": "This sentence applies neither rule. 'Exhibited' is a formal word that should be replaced with 'showed' or 'got worse' (Rule 2 not applied), and 'negative variance' is jargon that is not glossed (Rule 1 not applied). This is the kind of technical sentence that needs to be rewritten."}
            }
        },
        "feedback": feedback(
            "Well done. You correctly identified which plain-language rule each rewrite applies — and spotted the sentence that applies neither rule.",
            "Review the two rules: Rule 1 glosses specialist terms on first use; Rule 2 replaces formal or long words with simpler equivalents. Which rule does each rewrite apply?",
            [
                "Look for parenthetical glosses like '(mean)' — that is Rule 1 in action. Look for short, everyday words replacing formal ones — that is Rule 2.",
                "One sentence applies neither rule — it still uses formal language and unexplained jargon. Which one is it?"
            ],
            "tile_stakeholder_recommendation_translation.r02"
        )
    }
}

# ── Assemble output ───────────────────────────────────────────────────────────
output = {
    "schema_version": "1.0.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_003_da_chunk",
    "tiles": [
        {
            "tile_id": "tile_datamodel_normalization_many_to_many",
            "interactions": [s03, s04, s08, s09]
        },
        {
            "tile_id": "tile_datamodel_dimensional_er",
            "interactions": [s03_er, s04_er]
        },
        {
            "tile_id": "tile_stakeholder_recommendation_translation",
            "interactions": [s02_stk, s03_stk, s05_stk, s06_stk]
        }
    ]
}

out_path = "batches/final_batch_003_da_chunk/interactions.part.c2.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nWrote {out_path}")
print(f"Tiles: {len(output['tiles'])}")
for tile in output['tiles']:
    print(f"  {tile['tile_id']}: {len(tile['interactions'])} interactions")
    for ix in tile['interactions']:
        print(f"    {ix['step_id']} -> {ix['interaction']['type']}")
