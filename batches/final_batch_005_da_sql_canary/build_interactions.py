"""Build interactions.json for final_batch_005_da_sql_canary.
Run from pack root: python3 batches/final_batch_005_da_sql_canary/build_interactions.py
"""
import json
import subprocess
from pathlib import Path

BATCH = Path("batches/final_batch_005_da_sql_canary")

# ── Registry data (from scenario_asset_registry.json) ──────────────────────
customers_cols = [
    {"name": "customer_id", "type": "integer"},
    {"name": "name", "type": "string"},
    {"name": "city", "type": "string"},
]
customers_rows = [
    [1, "Amara Okafor", "Lagos"],
    [2, "Chidi Nwosu", "Abuja"],
    [3, "Fatima Bello", "Lagos"],
    [4, "Emeka Eze", "Kano"],
    [5, "Ngozi Adeyemi", "Abuja"],
    [6, "Tunde Adesanya", "Lagos"],
    [7, "Aisha Musa", "Kano"],
    [8, "Yemi Okonkwo", "Abuja"],
]
orders_cols = [
    {"name": "order_id", "type": "integer"},
    {"name": "customer_id", "type": "integer"},
    {"name": "delivery_time_minutes", "type": "integer"},
]
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

# Messy variant: customer_id=1 city='lagos' (lowercase), duplicate of customer_id=4 appended
customers_messy_rows = [
    [1, "Amara Okafor", "lagos"],
    [2, "Chidi Nwosu", "Abuja"],
    [3, "Fatima Bello", "Lagos"],
    [4, "Emeka Eze", "Kano"],
    [5, "Ngozi Adeyemi", "Abuja"],
    [6, "Tunde Adesanya", "Lagos"],
    [7, "Aisha Musa", "Kano"],
    [8, "Yemi Okonkwo", "Abuja"],
    [4, "Emeka Eze", "Kano"],  # duplicate row
]

TABLES = [
    {"name": "customers", "columns": customers_cols, "rows": customers_rows},
    {"name": "orders", "columns": orders_cols, "rows": orders_rows},
]

TABLES_MESSY_CUSTOMERS = [
    {"name": "customers", "columns": customers_cols, "rows": customers_messy_rows},
]

SQL_VERSION = "1.32.0"


# ── SQL helper ──────────────────────────────────────────────────────────────
def run_sql(queries: dict, tables=None) -> dict:
    """Run named SQL queries against the given tables; return results dict."""
    if tables is None:
        tables = TABLES
    job = {
        "tables": tables,
        "scripts": [{"id": k, "statements": [v]} for k, v in queries.items()],
    }
    r = subprocess.run(
        ["node", "--max-old-space-size=512", "00_FINAL_PIPELINE_CORE/sandbox/run_sql.mjs"],
        input=json.dumps(job),
        capture_output=True,
        text=True,
        cwd=".",
    )
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)["results"]


# ── Compute expected values from real SQL runs ──────────────────────────────
results = run_sql({
    "select_fund": "SELECT customer_id, name, city AS location FROM customers",
    "aliasing":    "SELECT o.order_id, o.customer_id, o.delivery_time_minutes AS delivery_min FROM orders AS o",
    "distinct":    "SELECT DISTINCT city FROM customers",
})

# Messy variant: what does DISTINCT city return on the messy customers table?
messy_results = run_sql(
    {"distinct_messy": "SELECT DISTINCT city FROM customers"},
    tables=TABLES_MESSY_CUSTOMERS,
)

SF_COLS  = results["select_fund"]["columns"]   # ["customer_id","name","location"]
SF_ROWS  = results["select_fund"]["rows"]
AL_COLS  = results["aliasing"]["columns"]      # ["order_id","customer_id","delivery_min"]
AL_ROWS  = results["aliasing"]["rows"]
DI_COLS  = results["distinct"]["columns"]      # ["city"]
DI_ROWS  = results["distinct"]["rows"]
DI_MESSY_COLS = messy_results["distinct_messy"]["columns"]
DI_MESSY_ROWS = messy_results["distinct_messy"]["rows"]

# ── Interaction definitions ─────────────────────────────────────────────────

# ── tile_sql_fund_relational_select ─────────────────────────────────────────

# s03 — choice — judge_whether_a_table_design_is_well_formed
# Tests f3 (unique name, no duplicate rows, row/column order insignificant) and
# f5 (one kind of thing per table). Taught in s02 (text blocks).
# Difficulty: intro (first check in tile)
ix_s03 = {
    "type": "choice",
    "interaction_id": "ix.tile_sql_fund_relational_select.s03",
    "difficulty": "intro",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.relational_model",
            "capability": "judge_whether_a_table_design_is_well_formed",
            "fact_ids": ["f3", "f5"],
        }
    ],
    "anchors": ["sql.relational_model#assessment:judge_whether_a_table_design_is_well_formed"],
    "public": {
        "prompt": (
            "A designer creates a single table called shop_data with columns: "
            "customer_id, customer_name, order_id, and delivery_time_minutes. "
            "Which property of a well-formed table does this design violate?"
        ),
        "options": [
            {
                "option_id": "opt_a",
                "text": "The table mixes two kinds of thing — customer details and order details — in the same rows.",
            },
            {
                "option_id": "opt_b",
                "text": "The table has too many columns to be a valid relation.",
            },
            {
                "option_id": "opt_c",
                "text": "The table name shop_data is not allowed because it contains an underscore.",
            },
            {
                "option_id": "opt_d",
                "text": "The table will contain duplicate rows because customer_id and order_id are both identifiers.",
            },
        ],
        "selection": "single",
        "shuffle": True,
    },
    "grading": {
        "correct_option_ids": ["opt_a"],
        "option_feedback": {
            "opt_a": {
                "message": "Correct. Each table should contain information about one kind of thing only — customer details belong in a customers table and order details in an orders table, not mixed together."
            },
            "opt_b": {
                "message": "Incorrect. A relation has no maximum column count — the number of columns is not a well-formedness property."
            },
            "opt_c": {
                "message": "Incorrect. Table names can contain underscores; the uniqueness rule says the name must not be reused for another table in the same database, not that it must avoid certain characters."
            },
            "opt_d": {
                "message": "Incorrect. Having two identifier columns does not cause duplicate rows. Duplicate rows are a separate well-formedness violation — they occur when the same complete row appears more than once."
            },
        },
    },
    "feedback": {
        "correct": {
            "message": "Exactly right. A well-formed table covers one kind of thing only — mixing customer and order data in one table is the violation here."
        },
        "incorrect": {
            "message": "Not quite. Think about the rule that says each table should contain information about one kind of thing only."
        },
        "hints": [
            "Re-read the columns: customer_id and customer_name describe a customer; order_id and delivery_time_minutes describe an order.",
            "The three well-formedness properties are: unique table name, no duplicate rows, and one kind of thing per table.",
        ],
        "remediation_step_id": "tile_sql_fund_relational_select.r01",
    },
}

# s04 — table_select — identify_table_rows_columns_in_scenario (practice + assessment)
# Tests f1 (row = record/tuple), f2 (column = field/attribute), f4 (database = multiple tables).
# Taught in s01 (text blocks). Difficulty: core (hands-on after intro check)
ix_s04 = {
    "type": "table_select",
    "interaction_id": "ix.tile_sql_fund_relational_select.s04",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.relational_model",
            "capability": "identify_table_rows_columns_in_scenario",
            "fact_ids": ["f1", "f2", "f4"],
        }
    ],
    "anchors": [
        "sql.relational_model#practice",
        "sql.relational_model#assessment:identify_table_rows_columns_in_scenario",
    ],
    "public": {
        "asset_ref": {
            "asset_id": "ds_orders",
            "variant_id": None,
            "columns": ["order_id", "customer_id", "delivery_time_minutes"],
        },
        "intro": (
            "The orders table is shown above. Use it to answer the two tasks below."
        ),
        "tasks": [
            {
                "task_id": "task_row",
                "prompt": "Click the row (record/tuple) for order 1007.",
                "target_kind": "row",
            },
            {
                "task_id": "task_col",
                "prompt": "Click the column (field/attribute) that records how long each delivery took.",
                "target_kind": "column",
            },
        ],
    },
    "grading": {
        "answers": [
            {
                "task_id": "task_row",
                "row": {"where": {"order_id": 1007}},
            },
            {
                "task_id": "task_col",
                "column": "delivery_time_minutes",
            },
        ],
        "task_feedback": {
            "task_row": {
                "correct": "Right — that is the row (record/tuple) for order 1007.",
                "incorrect": "Not quite. A row represents one complete group of related values — look for the row where order_id is 1007.",
            },
            "task_col": {
                "correct": "Correct — delivery_time_minutes is the field/attribute that records delivery duration.",
                "incorrect": "Not quite. Look for the column whose name describes delivery duration, not an identifier.",
            },
        },
    },
    "feedback": {
        "correct": {
            "message": "Well done. You identified both the row (record/tuple) and the column (field/attribute) correctly."
        },
        "incorrect": {
            "message": "Check each task: a row is a complete record; a column is a named attribute of every row."
        },
        "hints": [
            "A row runs horizontally across the table — each row is one order.",
            "A column runs vertically — every cell in that column holds the same kind of value.",
        ],
        "remediation_step_id": "tile_sql_fund_relational_select.r01",
    },
}

# s08 — choice — write_select_for_listed_columns
# Tests f1 (SELECT list specifies output expressions) and f3 (FROM derives the table).
# Taught in s05 (text blocks). Difficulty: core.
ix_s08 = {
    "type": "choice",
    "interaction_id": "ix.tile_sql_fund_relational_select.s08",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.select_fundamentals",
            "capability": "write_select_for_listed_columns",
            "fact_ids": ["f1", "f3"],
        }
    ],
    "anchors": ["sql.select_fundamentals#assessment:write_select_for_listed_columns"],
    "public": {
        "prompt": (
            "You need a query that returns only the name and city columns from the customers table. "
            "Which statement is correct?"
        ),
        "options": [
            {
                "option_id": "opt_a",
                "text": "SELECT name, city FROM customers",
            },
            {
                "option_id": "opt_b",
                "text": "FROM customers SELECT name, city",
            },
            {
                "option_id": "opt_c",
                "text": "SELECT customers FROM name, city",
            },
            {
                "option_id": "opt_d",
                "text": "SELECT name, city customers",
            },
        ],
        "selection": "single",
        "shuffle": True,
    },
    "grading": {
        "correct_option_ids": ["opt_a"],
        "option_feedback": {
            "opt_a": {
                "message": "Correct. SELECT names the output columns; FROM names the table. SELECT name, city FROM customers is the right form."
            },
            "opt_b": {
                "message": "Incorrect. The SELECT keyword must come before the column list; FROM follows the SELECT list, not the other way around."
            },
            "opt_c": {
                "message": "Incorrect. The SELECT list names the columns you want in the output — customers is the table name and belongs after FROM, not in the SELECT list."
            },
            "opt_d": {
                "message": "Incorrect. The FROM keyword is required to name the table. Without FROM, the database does not know which table to read from."
            },
        },
    },
    "feedback": {
        "correct": {
            "message": "Correct. The SELECT list specifies the output columns; FROM specifies the table."
        },
        "incorrect": {
            "message": "Not quite. Remember: SELECT lists the columns you want, then FROM names the table to read them from."
        },
        "hints": [
            "Every SELECT statement has two required parts: the SELECT list (column names) and the FROM clause (table name).",
            "The order is always SELECT … FROM …, never the reverse.",
        ],
        "remediation_step_id": "tile_sql_fund_relational_select.r02",
    },
}

# s09 — code_exercise — rename_output_column_with_as (practice + assessment)
# Tests f2 (AS output_name renames a column). Taught in s05 (text blocks).
# Practice anchor: live_code, allowed: SELECT, FROM, AS output_name, * and table_name.*
# Blocked: table alias, DISTINCT, WHERE, etc.
# Prompt pins: return customer_id, name, city AS location from customers (3 columns, city renamed)
# Solution: SELECT customer_id, name, city AS location FROM customers
# Difficulty: stretch (final hands-on of tile)
SELECT_FUND_SOLUTION = "SELECT customer_id, name, city AS location FROM customers"
SELECT_FUND_STARTER = (
    "-- The customers table has columns: customer_id, name, city\n"
    "-- Task: return all three columns, but rename city as 'location'\n"
    "-- Write your SELECT statement below:\n"
)

ix_s09 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_sql_fund_relational_select.s09",
    "difficulty": "stretch",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.select_fundamentals",
            "capability": "rename_output_column_with_as",
            "fact_ids": ["f2"],
        }
    ],
    "anchors": [
        "sql.select_fundamentals#practice",
        "sql.select_fundamentals#assessment:rename_output_column_with_as",
    ],
    "public": {
        "prompt": (
            "The customers table has three columns: customer_id, name, and city. "
            "Write a SELECT statement that returns all three columns in that order, "
            "but renames city as location in the output. "
            "Your result must have exactly the columns: customer_id, name, location."
        ),
        "runtime": {"kind": "sql", "version": SQL_VERSION},
        "workspace": {
            "files": [
                {
                    "path": "query.sql",
                    "role": "editable",
                    "language": "sql",
                    "content": SELECT_FUND_STARTER,
                }
            ],
            "entry": "query.sql",
            "asset_mounts": [
                {
                    "asset_id": "ds_customers",
                    "variant_id": None,
                    "mount_path": "customers",
                }
            ],
        },
        "constraints": {
            "allowed_syntax": ["SELECT", "FROM", "AS output_name", "* and table_name.*"],
            "blocked_syntax": [
                "table alias (FROM table AS alias)",
                "alias.column qualification",
                "DISTINCT",
                "ALL",
                "WHERE",
                "< > <= >= = <> !=",
                "AND",
                "OR",
                "NOT",
                "parentheses",
                "IS NULL",
                "IS NOT NULL",
                "ORDER BY",
                "ASC",
                "DESC",
                "LIMIT",
                "OFFSET",
                "COUNT",
                "SUM",
                "AVG",
                "MIN",
                "MAX",
                "GROUP BY",
                "HAVING",
                "CASE WHEN ... THEN ... ELSE ... END",
                "LOWER",
                "UPPER",
                "TRIM",
                "CONCAT",
                "LENGTH",
                "EXTRACT(field FROM source)",
                "date - date",
                "CAST(expression AS type)",
                "expression::type",
                "COALESCE",
                "UNION",
                "UNION ALL",
                "JOIN / INNER JOIN",
                "ON",
                "USING",
                "ON with AND across several columns",
                "USING (a, b)",
                "LEFT JOIN",
                "RIGHT JOIN",
                "FULL JOIN",
                "OUTER keyword",
                "subquery in WHERE",
                "IN (SELECT ...)",
                "subquery in FROM with an alias",
                "WITH name AS (...)",
                "window functions (OVER)",
                "EXISTS",
                "correlated subqueries",
                "CROSS JOIN",
                "self-joins",
            ],
        },
    },
    "grading": {
        "solution_files": [
            {
                "path": "query.sql",
                "content": SELECT_FUND_SOLUTION,
            }
        ],
        "tests": [
            {
                "test_id": "test_select_fund_result",
                "kind": "query_result_equals",
                "spec": {
                    "expected": {
                        "columns": SF_COLS,
                        "rows": SF_ROWS,
                    },
                    "ordered": False,
                },
                "visible": True,
                "message_on_fail": (
                    "Your query should return three columns named customer_id, name, and location "
                    "(city renamed with AS), with one row per customer."
                ),
            },
            {
                "test_id": "test_select_fund_no_alias",
                "kind": "forbidden_syntax",
                "spec": {
                    "descriptors": ["table alias (FROM table AS alias)"],
                },
                "visible": False,
                "message_on_fail": "This exercise does not use table aliases — use only SELECT, FROM, and AS for column renaming.",
            },
        ],
    },
    "feedback": {
        "correct": {
            "message": "Your query returns all three columns with city correctly renamed to location using AS."
        },
        "incorrect": {
            "message": "Check that you list all three columns (customer_id, name, city) and rename city as location with AS."
        },
        "hints": [
            "The AS keyword goes right after the column expression: city AS location.",
            "Make sure you list all three columns: customer_id, name, and city AS location.",
        ],
        "remediation_step_id": "tile_sql_fund_relational_select.r02",
    },
}

# ── tile_sql_fund_alias_distinct ─────────────────────────────────────────────

# s03 — choice — qualify_and_alias_columns_correctly
# Tests f3 (column alias with AS) and f4 (correlation.columnname qualification).
# Taught in s02 (text blocks). Difficulty: intro.
ix_alias_s03 = {
    "type": "choice",
    "interaction_id": "ix.tile_sql_fund_alias_distinct.s03",
    "difficulty": "intro",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.aliasing",
            "capability": "qualify_and_alias_columns_correctly",
            "fact_ids": ["f3", "f4"],
        }
    ],
    "anchors": ["sql.aliasing#assessment:qualify_and_alias_columns_correctly"],
    "public": {
        "prompt": (
            "A query starts with FROM orders AS o. "
            "Which SELECT clause correctly qualifies the delivery_time_minutes column "
            "using the alias and renames it as delivery_min?"
        ),
        "options": [
            {
                "option_id": "opt_a",
                "text": "SELECT o.delivery_time_minutes AS delivery_min",
            },
            {
                "option_id": "opt_b",
                "text": "SELECT orders.delivery_time_minutes AS delivery_min",
            },
            {
                "option_id": "opt_c",
                "text": "SELECT o.delivery_min AS delivery_time_minutes",
            },
            {
                "option_id": "opt_d",
                "text": "SELECT delivery_time_minutes AS o.delivery_min",
            },
        ],
        "selection": "single",
        "shuffle": True,
    },
    "grading": {
        "correct_option_ids": ["opt_a"],
        "option_feedback": {
            "opt_a": {
                "message": "Correct. o.delivery_time_minutes uses the alias o to qualify the column, and AS delivery_min renames the output."
            },
            "opt_b": {
                "message": "Incorrect. Once the alias o is assigned, the original table name orders can no longer be used to qualify columns in that query — use o instead."
            },
            "opt_c": {
                "message": "Incorrect. delivery_min is the desired output name, not a column that exists in the table. The actual column name is delivery_time_minutes."
            },
            "opt_d": {
                "message": "Incorrect. The AS output_name syntax places the alias after the column expression, not after AS. Writing AS o.delivery_min is not valid SQL."
            },
        },
    },
    "feedback": {
        "correct": {
            "message": "Right. The alias qualifies the column reference (o.delivery_time_minutes) and AS renames the output column."
        },
        "incorrect": {
            "message": "Remember: once an alias is assigned, use the alias — not the original table name — to qualify columns."
        },
        "hints": [
            "The alias o replaces orders for the rest of the query — use o.column_name, not orders.column_name.",
            "AS output_name goes after the column expression: o.delivery_time_minutes AS delivery_min.",
        ],
        "remediation_step_id": "tile_sql_fund_alias_distinct.r01",
    },
}

# s04 — code_exercise — alias_a_table_and_use_the_alias + qualify_and_alias_columns_correctly (practice)
# Tests f1, f2, f3, f4. Taught in s01 and s02 (text blocks).
# Practice anchor: live_code, allowed: SELECT, FROM, AS output_name, * and table_name.*, table alias, alias.column
# Blocked: DISTINCT, WHERE, etc.
# Prompt: alias orders as o, qualify all columns with o., rename delivery_time_minutes as delivery_min
# Solution: SELECT o.order_id, o.customer_id, o.delivery_time_minutes AS delivery_min FROM orders AS o
# Difficulty: core
ALIASING_SOLUTION = "SELECT o.order_id, o.customer_id, o.delivery_time_minutes AS delivery_min FROM orders AS o"
ALIASING_STARTER = (
    "-- The orders table has columns: order_id, customer_id, delivery_time_minutes\n"
    "-- Task: alias the orders table as 'o', qualify every column with o.,\n"
    "--       and rename delivery_time_minutes as delivery_min\n"
    "-- Write your SELECT statement below:\n"
)

ix_alias_s04 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_sql_fund_alias_distinct.s04",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.aliasing",
            "capability": "alias_a_table_and_use_the_alias",
            "fact_ids": ["f1", "f2"],
        },
        {
            "concept_id": "sql.aliasing",
            "capability": "qualify_and_alias_columns_correctly",
            "fact_ids": ["f3", "f4"],
        },
    ],
    "anchors": [
        "sql.aliasing#practice",
        "sql.aliasing#assessment:alias_a_table_and_use_the_alias",
        "sql.aliasing#assessment:qualify_and_alias_columns_correctly",
    ],
    "public": {
        "prompt": (
            "The orders table has three columns: order_id, customer_id, and delivery_time_minutes. "
            "Write a SELECT statement that: "
            "(1) gives the orders table the alias o using FROM orders AS o, "
            "(2) qualifies every column reference with o. (e.g. o.order_id), and "
            "(3) renames delivery_time_minutes as delivery_min in the output. "
            "Your result must have exactly the columns: order_id, customer_id, delivery_min."
        ),
        "runtime": {"kind": "sql", "version": SQL_VERSION},
        "workspace": {
            "files": [
                {
                    "path": "query.sql",
                    "role": "editable",
                    "language": "sql",
                    "content": ALIASING_STARTER,
                }
            ],
            "entry": "query.sql",
            "asset_mounts": [
                {
                    "asset_id": "ds_orders",
                    "variant_id": None,
                    "mount_path": "orders",
                }
            ],
        },
        "constraints": {
            "allowed_syntax": [
                "SELECT",
                "FROM",
                "AS output_name",
                "* and table_name.*",
                "table alias (FROM table AS alias)",
                "alias.column qualification",
            ],
            "blocked_syntax": [
                "DISTINCT",
                "ALL",
                "WHERE",
                "< > <= >= = <> !=",
                "AND",
                "OR",
                "NOT",
                "parentheses",
                "IS NULL",
                "IS NOT NULL",
                "ORDER BY",
                "ASC",
                "DESC",
                "LIMIT",
                "OFFSET",
                "COUNT",
                "SUM",
                "AVG",
                "MIN",
                "MAX",
                "GROUP BY",
                "HAVING",
                "CASE WHEN ... THEN ... ELSE ... END",
                "LOWER",
                "UPPER",
                "TRIM",
                "CONCAT",
                "LENGTH",
                "EXTRACT(field FROM source)",
                "date - date",
                "CAST(expression AS type)",
                "expression::type",
                "COALESCE",
                "UNION",
                "UNION ALL",
                "JOIN / INNER JOIN",
                "ON",
                "USING",
                "ON with AND across several columns",
                "USING (a, b)",
                "LEFT JOIN",
                "RIGHT JOIN",
                "FULL JOIN",
                "OUTER keyword",
                "subquery in WHERE",
                "IN (SELECT ...)",
                "subquery in FROM with an alias",
                "WITH name AS (...)",
                "window functions (OVER)",
                "EXISTS",
                "correlated subqueries",
                "CROSS JOIN",
                "self-joins",
            ],
        },
    },
    "grading": {
        "solution_files": [
            {
                "path": "query.sql",
                "content": ALIASING_SOLUTION,
            }
        ],
        "tests": [
            {
                "test_id": "test_aliasing_result",
                "kind": "query_result_equals",
                "spec": {
                    "expected": {
                        "columns": AL_COLS,
                        "rows": AL_ROWS,
                    },
                    "ordered": False,
                },
                "visible": True,
                "message_on_fail": (
                    "Your query should return three columns named order_id, customer_id, and delivery_min "
                    "(delivery_time_minutes renamed with AS), with one row per order."
                ),
            },
            {
                "test_id": "test_aliasing_no_distinct",
                "kind": "forbidden_syntax",
                "spec": {
                    "descriptors": ["DISTINCT"],
                },
                "visible": False,
                "message_on_fail": "DISTINCT is not part of this exercise — focus on aliasing and column qualification.",
            },
        ],
    },
    "feedback": {
        "correct": {
            "message": "Your query aliases the table as o, qualifies every column with o., and renames delivery_time_minutes as delivery_min."
        },
        "incorrect": {
            "message": "Check three things: FROM orders AS o assigns the alias; o.column_name qualifies each column; AS delivery_min renames the output."
        },
        "hints": [
            "Start with FROM orders AS o — that assigns the alias o to the orders table.",
            "Once the alias is assigned, every column reference must use o.column_name, not orders.column_name.",
        ],
        "remediation_step_id": "tile_sql_fund_alias_distinct.r01",
    },
}

# s06 — choice — predict_rows_with_and_without_distinct
# Tests f2 (SELECT ALL is the default, keeps all rows including duplicates).
# Taught in s05 (text blocks). Difficulty: core.
# The customers table has 8 rows; 3 distinct cities (Lagos, Abuja, Kano).
ix_distinct_s06 = {
    "type": "choice",
    "interaction_id": "ix.tile_sql_fund_alias_distinct.s06",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.distinct",
            "capability": "predict_rows_with_and_without_distinct",
            "fact_ids": ["f2"],
        }
    ],
    "anchors": ["sql.distinct#assessment:predict_rows_with_and_without_distinct"],
    "public": {
        "prompt": (
            "The customers table has 8 rows. Three cities appear: Lagos (3 customers), "
            "Abuja (3 customers), and Kano (2 customers). "
            "How many rows does SELECT DISTINCT city FROM customers return?"
        ),
        "options": [
            {"option_id": "opt_a", "text": "3"},
            {"option_id": "opt_b", "text": "8"},
            {"option_id": "opt_c", "text": "6"},
            {"option_id": "opt_d", "text": "1"},
        ],
        "selection": "single",
        "shuffle": True,
    },
    "grading": {
        "correct_option_ids": ["opt_a"],
        "option_feedback": {
            "opt_a": {
                "message": "Correct. DISTINCT keeps one row per unique city value — Lagos, Abuja, and Kano — so 3 rows are returned."
            },
            "opt_b": {
                "message": "Incorrect. 8 is the row count without DISTINCT (SELECT ALL). DISTINCT removes duplicates, so only one row per unique city is kept."
            },
            "opt_c": {
                "message": "Incorrect. 6 is not the count of unique cities. DISTINCT collapses all rows that share the same city value into one row."
            },
            "opt_d": {
                "message": "Incorrect. DISTINCT does not collapse all rows into one — it keeps one row per unique value. There are 3 unique cities, so 3 rows are returned."
            },
        },
    },
    "feedback": {
        "correct": {
            "message": "Right. DISTINCT returns one row per unique city value — 3 cities, 3 rows."
        },
        "incorrect": {
            "message": "Think about how many unique city values exist in the table, not how many customers there are."
        },
        "hints": [
            "DISTINCT removes duplicate rows — two rows with the same city value become one.",
            "Count the unique city names: Lagos, Abuja, Kano.",
        ],
        "remediation_step_id": "tile_sql_fund_alias_distinct.r02",
    },
}

# s07 — code_exercise — write_distinct_to_list_unique_values + predict_rows_with_and_without_distinct (practice)
# Tests f1 (DISTINCT removes duplicates) and f2 (ALL is default).
# Taught in s05 (text blocks). Difficulty: stretch.
# Practice anchor: live_code, allowed: SELECT, FROM, AS output_name, * and table_name.*, table alias, alias.column, DISTINCT, ALL
# Blocked: WHERE, etc.
# Prompt: return each distinct city from customers exactly once
# Solution: SELECT DISTINCT city FROM customers
# Hidden test: mount_variants uses ds_customers_messy — solution returns 4 rows (lagos, Abuja, Lagos, Kano)
# because the messy variant has lowercase 'lagos' as a distinct value from 'Lagos'.
# This test verifies that a query without DISTINCT would fail (it would return 9 rows on messy data).
DISTINCT_SOLUTION = "SELECT DISTINCT city FROM customers"
DISTINCT_STARTER = (
    "-- The customers table has a city column with repeated values.\n"
    "-- Task: return each city exactly once (no duplicates).\n"
    "-- Your result must have exactly one column named: city\n"
    "-- Write your SELECT statement below:\n"
)

ix_distinct_s07 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_sql_fund_alias_distinct.s07",
    "difficulty": "stretch",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "sql.distinct",
            "capability": "write_distinct_to_list_unique_values",
            "fact_ids": ["f1"],
        },
        {
            "concept_id": "sql.distinct",
            "capability": "predict_rows_with_and_without_distinct",
            "fact_ids": ["f2"],
        },
    ],
    "anchors": [
        "sql.distinct#practice",
        "sql.distinct#assessment:write_distinct_to_list_unique_values",
        "sql.distinct#assessment:predict_rows_with_and_without_distinct",
    ],
    "public": {
        "prompt": (
            "The customers table has a city column. Several customers share the same city. "
            "Write a SELECT statement that returns each city exactly once — no duplicates. "
            "Your result must have exactly one column named: city."
        ),
        "runtime": {"kind": "sql", "version": SQL_VERSION},
        "workspace": {
            "files": [
                {
                    "path": "query.sql",
                    "role": "editable",
                    "language": "sql",
                    "content": DISTINCT_STARTER,
                }
            ],
            "entry": "query.sql",
            "asset_mounts": [
                {
                    "asset_id": "ds_customers",
                    "variant_id": None,
                    "mount_path": "customers",
                }
            ],
        },
        "constraints": {
            "allowed_syntax": [
                "SELECT",
                "FROM",
                "AS output_name",
                "* and table_name.*",
                "table alias (FROM table AS alias)",
                "alias.column qualification",
                "DISTINCT",
                "ALL",
            ],
            "blocked_syntax": [
                "WHERE",
                "< > <= >= = <> !=",
                "AND",
                "OR",
                "NOT",
                "parentheses",
                "IS NULL",
                "IS NOT NULL",
                "ORDER BY",
                "ASC",
                "DESC",
                "LIMIT",
                "OFFSET",
                "COUNT",
                "SUM",
                "AVG",
                "MIN",
                "MAX",
                "GROUP BY",
                "HAVING",
                "CASE WHEN ... THEN ... ELSE ... END",
                "LOWER",
                "UPPER",
                "TRIM",
                "CONCAT",
                "LENGTH",
                "EXTRACT(field FROM source)",
                "date - date",
                "CAST(expression AS type)",
                "expression::type",
                "COALESCE",
                "UNION",
                "UNION ALL",
                "JOIN / INNER JOIN",
                "ON",
                "USING",
                "ON with AND across several columns",
                "USING (a, b)",
                "LEFT JOIN",
                "RIGHT JOIN",
                "FULL JOIN",
                "OUTER keyword",
                "subquery in WHERE",
                "IN (SELECT ...)",
                "subquery in FROM with an alias",
                "WITH name AS (...)",
                "window functions (OVER)",
                "EXISTS",
                "correlated subqueries",
                "CROSS JOIN",
                "self-joins",
            ],
        },
    },
    "grading": {
        "solution_files": [
            {
                "path": "query.sql",
                "content": DISTINCT_SOLUTION,
            }
        ],
        "tests": [
            {
                "test_id": "test_distinct_result",
                "kind": "query_result_equals",
                "spec": {
                    "expected": {
                        "columns": DI_COLS,
                        "rows": DI_ROWS,
                    },
                    "ordered": False,
                },
                "visible": True,
                "message_on_fail": (
                    "Your query should return exactly one column named city, "
                    "with one row per unique city (3 rows total — Lagos, Abuja, Kano)."
                ),
            },
            {
                "test_id": "test_distinct_hidden_variant",
                "kind": "query_result_equals",
                "spec": {
                    "expected": {
                        "columns": DI_MESSY_COLS,
                        "rows": DI_MESSY_ROWS,
                    },
                    "ordered": False,
                    "mount_variants": {"customers": "ds_customers_messy"},
                },
                "visible": False,
                "message_on_fail": (
                    "Your query must use DISTINCT to deduplicate — a query that returns all rows "
                    "will fail when the data has extra duplicates."
                ),
            },
        ],
    },
    "feedback": {
        "correct": {
            "message": "Your query uses DISTINCT to return each city exactly once."
        },
        "incorrect": {
            "message": "Make sure you use SELECT DISTINCT to remove duplicate city values."
        },
        "hints": [
            "Add DISTINCT right after SELECT: SELECT DISTINCT city FROM customers.",
            "Without DISTINCT, you get one row per customer — 8 rows. With DISTINCT, you get one row per unique city.",
        ],
        "remediation_step_id": "tile_sql_fund_alias_distinct.r02",
    },
}

# ── Assemble interactions.json ──────────────────────────────────────────────
interactions = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_005_da_sql_canary",
    "tiles": [
        {
            "tile_id": "tile_sql_fund_relational_select",
            "interactions": [
                {"step_id": "tile_sql_fund_relational_select.s03", "interaction": ix_s03},
                {"step_id": "tile_sql_fund_relational_select.s04", "interaction": ix_s04},
                {"step_id": "tile_sql_fund_relational_select.s08", "interaction": ix_s08},
                {"step_id": "tile_sql_fund_relational_select.s09", "interaction": ix_s09},
            ],
        },
        {
            "tile_id": "tile_sql_fund_alias_distinct",
            "interactions": [
                {"step_id": "tile_sql_fund_alias_distinct.s03", "interaction": ix_alias_s03},
                {"step_id": "tile_sql_fund_alias_distinct.s04", "interaction": ix_alias_s04},
                {"step_id": "tile_sql_fund_alias_distinct.s06", "interaction": ix_distinct_s06},
                {"step_id": "tile_sql_fund_alias_distinct.s07", "interaction": ix_distinct_s07},
            ],
        },
    ],
}

out_path = BATCH / "interactions.json"
out_path.write_text(json.dumps(interactions, indent=2, ensure_ascii=False) + "\n")
print(f"Written {out_path}")
print(f"Tile 1 interactions: {len(interactions['tiles'][0]['interactions'])}")
print(f"Tile 2 interactions: {len(interactions['tiles'][1]['interactions'])}")
print(f"SF_COLS={SF_COLS}, SF_ROWS count={len(SF_ROWS)}")
print(f"AL_COLS={AL_COLS}, AL_ROWS count={len(AL_ROWS)}")
print(f"DI_COLS={DI_COLS}, DI_ROWS={DI_ROWS}")
print(f"DI_MESSY_COLS={DI_MESSY_COLS}, DI_MESSY_ROWS={DI_MESSY_ROWS}")
