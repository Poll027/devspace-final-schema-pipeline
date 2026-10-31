"""Build interactions.part.c3.json for tiles:
  - tile_sql_adv_joining_tables
  - tile_sql_adv_execution_order_subquery_where
  - tile_sql_adv_subquery_from_cte
"""
import json, duckdb
from pathlib import Path

BATCH = Path("batches/final_batch_006_da_sql_rest")

# ── load registry and build DuckDB tables ──────────────────────────────────
with open(BATCH / "scenario_asset_registry.json") as f:
    reg = json.load(f)

conn = duckdb.connect()
for asset in reg["assets"]:
    table_name = asset["title"]
    col_defs = []
    for c in asset["columns"]:
        t = c["type"]
        sql_t = {"integer": "INTEGER", "number": "DOUBLE", "date": "DATE", "string": "VARCHAR"}.get(t, "VARCHAR")
        col_defs.append(f'{c["name"]} {sql_t}')
    conn.execute(f'CREATE TABLE {table_name} ({", ".join(col_defs)})')
    for row in asset["rows"]:
        placeholders = ",".join(["?" for _ in row])
        conn.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)


def run(sql):
    """Return (columns, rows) from a SQL query, converting dates to strings."""
    rel = conn.execute(sql)
    cols = [d[0] for d in rel.description]
    raw_rows = rel.fetchall()
    rows = []
    for r in raw_rows:
        row = []
        for v in r:
            import datetime
            if isinstance(v, datetime.date):
                row.append(str(v))
            else:
                row.append(v)
        rows.append(row)
    return cols, rows


# ══════════════════════════════════════════════════════════════════════════════
# TILE 1: tile_sql_adv_joining_tables
# Steps with interactions: s04(check), s05(hands_on), s07(check), s08(check),
#                          s09(hands_on), s13(check), s14(check), s15(hands_on)
# ══════════════════════════════════════════════════════════════════════════════

# ── s04: choice — predict_which_rows_survive_an_inner_join ──────────────────
# Fact: rows from either table with no match are dropped
# Taught by: s01 (explainer tb1,tb2,tb3), s03 (explainer tb4)
s04 = {
    "step_id": "tile_sql_adv_joining_tables.s04",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s04",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.inner_join", "capability": "predict_which_rows_survive_an_inner_join", "fact_ids": ["sql.inner_join#f1"]}
        ],
        "anchors": ["sql.inner_join#assessment:predict_which_rows_survive_an_inner_join"],
        "public": {
            "prompt": (
                "The **customers** table has rows for customer_id 1, 2, 3, 4, and 5. "
                "The **orders** table has rows for customer_id 1, 2, and 3 only. "
                "How many customer rows appear in the result of "
                "`SELECT * FROM customers JOIN orders ON customers.customer_id = orders.customer_id`?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "5 — all customers appear"},
                {"option_id": "opt_b", "text": "3 — only customers who have at least one order"},
                {"option_id": "opt_c", "text": "2 — only customers who have more than one order"},
                {"option_id": "opt_d", "text": "0 — an INNER JOIN always returns an empty result when tables differ in size"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {"message": "An INNER JOIN drops rows with no match on the other side. Customers 4 and 5 have no orders, so they are excluded."},
                "opt_b": {"message": "Correct. An INNER JOIN keeps only rows that have a match on both sides. Customers 4 and 5 have no matching order rows, so they are dropped."},
                "opt_c": {"message": "The join condition is about matching on customer_id, not about how many orders a customer has. Any customer with at least one order produces at least one joined row."},
                "opt_d": {"message": "An INNER JOIN returns rows whenever a match exists — it does not require the tables to be the same size."},
            },
        },
        "feedback": {
            "correct": {"message": "An INNER JOIN produces a row only when both sides have a match. Rows with no counterpart on either side are silently dropped."},
            "incorrect": {"message": "Remember: an INNER JOIN keeps only rows that satisfy the join condition on both sides. Any row with no match is dropped."},
            "hints": [
                "Think about what happens to a customer who has placed zero orders — does the join condition ever become true for that customer?",
                "The rule is symmetric: a row survives only if both sides have a match.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s01",
        },
    },
}

# ── s05: code_exercise — inner join (practice) ─────────────────────────────
# Solution: SELECT c.name, o.order_id, o.delivery_time_minutes
#           FROM customers AS c JOIN orders AS o ON c.customer_id = o.customer_id
#           ORDER BY o.order_id
sol_s05 = (
    "SELECT c.name, o.order_id, o.delivery_time_minutes\n"
    "FROM customers AS c\n"
    "JOIN orders AS o ON c.customer_id = o.customer_id\n"
    "ORDER BY o.order_id;\n"
)
cols_s05, rows_s05 = run(sol_s05.rstrip(";\n") + ";")

s05 = {
    "step_id": "tile_sql_adv_joining_tables.s05",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s05",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.inner_join", "capability": "predict_which_rows_survive_an_inner_join", "fact_ids": ["sql.inner_join#f1"]},
            {"concept_id": "sql.inner_join", "capability": "write_the_join_condition", "fact_ids": ["sql.inner_join#f2", "sql.inner_join#f3"]},
        ],
        "anchors": [
            "sql.inner_join#practice",
            "sql.inner_join#assessment:write_the_join_condition",
        ],
        "public": {
            "prompt": (
                "QuickCart wants to see each order alongside the customer's name. "
                "Write a query that joins **customers** to **orders** on `customer_id` and returns "
                "the columns **name**, **order_id**, and **delivery_time_minutes**, ordered by `order_id` ascending. "
                "Use `JOIN` (or `INNER JOIN`) with an `ON` clause."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- customers columns: customer_id, name, city\n"
                            "-- orders columns: order_id, customer_id, delivery_time_minutes, order_date, region, amount, city\n"
                            "-- Write a JOIN query that returns name, order_id, delivery_time_minutes\n"
                            "-- ordered by order_id.\n"
                        ),
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_customers", "variant_id": None, "mount_path": "customers"},
                    {"asset_id": "ds_orders", "variant_id": None, "mount_path": "orders"},
                ],
            },
            "constraints": {
                "allowed_syntax": [
                    "SELECT", "FROM", "AS output_name", "* and table_name.*",
                    "table alias (FROM table AS alias)", "alias.column qualification",
                    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=",
                    "AND", "OR", "NOT", "parentheses", "IS NULL", "IS NOT NULL",
                    "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                    "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
                    "EXTRACT(field FROM source)", "date - date",
                    "CAST(expression AS type)", "expression::type", "COALESCE",
                    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
                ],
                "blocked_syntax": [
                    "ON with AND across several columns", "USING (a, b)",
                    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
                    "subquery in WHERE", "IN (SELECT ...)",
                    "subquery in FROM with an alias", "WITH name AS (...)",
                    "window functions (OVER)", "EXISTS", "correlated subqueries",
                    "CROSS JOIN", "self-joins",
                ],
            },
        },
        "grading": {
            "solution_files": [{"path": "query.sql", "content": sol_s05}],
            "tests": [
                {
                    "test_id": "ix.tile_sql_adv_joining_tables.s05.t1",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": {"columns": cols_s05, "rows": rows_s05},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return name, order_id, and delivery_time_minutes "
                        "for every order that has a matching customer, ordered by order_id. "
                        "Check your JOIN condition and column list."
                    ),
                }
            ],
        },
        "feedback": {
            "correct": {"message": "Your INNER JOIN correctly links each order to its customer. Only orders with a matching customer_id appear — rows with no match on either side are dropped."},
            "incorrect": {"message": "Check that you are joining on customer_id, selecting name, order_id, and delivery_time_minutes, and ordering by order_id."},
            "hints": [
                "The ON clause should compare the customer_id column from both tables: `ON c.customer_id = o.customer_id`.",
                "Give each table a short alias (e.g. `c` and `o`) so you can qualify columns like `c.name` and `o.order_id`.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s01",
        },
    },
}

# ── s07: choice — extend_on_with_and ───────────────────────────────────────
# Fact: ON clause takes boolean expression, several column-equality tests combined with AND
# Taught by: s06 (explainer tb1,tb2,tb3)
s07 = {
    "step_id": "tile_sql_adv_joining_tables.s07",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s07",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.composite_join_conditions", "capability": "extend_on_with_and", "fact_ids": ["sql.composite_join_conditions#f1"]}
        ],
        "anchors": ["sql.composite_join_conditions#assessment:extend_on_with_and"],
        "public": {
            "prompt": (
                "You are joining `order_items` to `shipments`. A row should only match when "
                "**both** `order_id` and `product_id` are equal. "
                "Which ON clause correctly expresses this two-column condition?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "ON order_items.order_id = shipments.order_id"},
                {"option_id": "opt_b", "text": "ON order_items.order_id = shipments.order_id AND order_items.product_id = shipments.product_id"},
                {"option_id": "opt_c", "text": "ON order_items.order_id = shipments.order_id OR order_items.product_id = shipments.product_id"},
                {"option_id": "opt_d", "text": "ON (order_items.order_id, order_items.product_id) = (shipments.order_id, shipments.product_id)"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {"message": "This only checks order_id. A row from order_items could match a shipment row that shares the order_id but has a different product_id — that is a false match."},
                "opt_b": {"message": "Correct. The ON clause is a boolean expression, so you can chain equality tests with AND to require all columns to match simultaneously."},
                "opt_c": {"message": "OR would match whenever either column agrees, which allows false matches — a row where only order_id matches would still join."},
                "opt_d": {"message": "Row-value comparisons like (a, b) = (c, d) are not standard SQL join syntax. Use AND to combine individual equality tests in the ON clause."},
            },
        },
        "feedback": {
            "correct": {"message": "The ON clause accepts any boolean expression, so you can combine multiple equality tests with AND to require all columns to match."},
            "incorrect": {"message": "To require two columns to match simultaneously, combine two equality tests with AND inside the ON clause."},
            "hints": [
                "The ON clause works like a WHERE clause — you can use AND to combine conditions.",
                "Each condition should compare one column from the left table to the corresponding column on the right.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s06",
        },
    },
}

# ── s08: choice — rewrite_with_using_on_several_columns ────────────────────
# Fact: USING (a, b) is shorthand for ON T1.a = T2.a AND T1.b = T2.b
# Taught by: s06 (explainer tb1,tb2,tb3)
s08 = {
    "step_id": "tile_sql_adv_joining_tables.s08",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s08",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.composite_join_conditions", "capability": "rewrite_with_using_on_several_columns", "fact_ids": ["sql.composite_join_conditions#f2"]}
        ],
        "anchors": ["sql.composite_join_conditions#assessment:rewrite_with_using_on_several_columns"],
        "public": {
            "prompt": (
                "The query below uses a two-column ON clause:\n\n"
                "```sql\n"
                "SELECT *\n"
                "FROM order_items\n"
                "JOIN shipments ON order_items.order_id = shipments.order_id\n"
                "               AND order_items.product_id = shipments.product_id;\n"
                "```\n\n"
                "Both tables share the column names `order_id` and `product_id`. "
                "Which USING clause is the correct shorthand?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "USING (order_id, product_id)"},
                {"option_id": "opt_b", "text": "USING order_id AND product_id"},
                {"option_id": "opt_c", "text": "USING (order_id) AND USING (product_id)"},
                {"option_id": "opt_d", "text": "USING order_id = shipments.order_id AND product_id = shipments.product_id"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. USING (a, b) is the shorthand for ON T1.a = T2.a AND T1.b = T2.b when both tables share those column names."},
                "opt_b": {"message": "USING requires a parenthesised column list, not bare column names joined with AND. The correct form is USING (order_id, product_id)."},
                "opt_c": {"message": "There is only one USING clause per join. List all shared columns inside a single pair of parentheses: USING (order_id, product_id)."},
                "opt_d": {"message": "USING takes only column names, not equality expressions. The equality is implied by the shared name. Write USING (order_id, product_id)."},
            },
        },
        "feedback": {
            "correct": {"message": "USING (a, b) is a compact shorthand: it forms the join condition ON T1.a = T2.a AND T1.b = T2.b automatically, as long as both tables share those column names."},
            "incorrect": {"message": "USING takes a parenthesised list of shared column names. All columns go inside one pair of parentheses, separated by commas."},
            "hints": [
                "USING requires parentheses around the column list.",
                "You only need to list the column names — the equality is implied because both tables share the same name.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s06",
        },
    },
}

# ── s09: code_exercise — composite join (practice) ─────────────────────────
sol_s09 = (
    "SELECT oi.order_id, oi.product_id, oi.quantity, oi.unit_price, s.shipped_date\n"
    "FROM order_items AS oi\n"
    "JOIN shipments AS s ON oi.order_id = s.order_id AND oi.product_id = s.product_id\n"
    "ORDER BY oi.order_id, oi.product_id;\n"
)
cols_s09, rows_s09 = run(sol_s09.rstrip(";\n") + ";")

s09 = {
    "step_id": "tile_sql_adv_joining_tables.s09",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s09",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.composite_join_conditions", "capability": "extend_on_with_and", "fact_ids": ["sql.composite_join_conditions#f1"]},
        ],
        "anchors": ["sql.composite_join_conditions#practice"],
        "public": {
            "prompt": (
                "The `order_items` and `shipments` tables both have `order_id` and `product_id` columns. "
                "A shipment matches a line item only when **both** columns agree. "
                "Write a query that joins `order_items` to `shipments` using an ON clause with AND, "
                "and returns **order_id**, **product_id**, **quantity**, **unit_price**, and **shipped_date**, "
                "ordered by `order_id` then `product_id`."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- order_items columns: order_id, product_id, quantity, unit_price\n"
                            "-- shipments columns: order_id, product_id, shipped_date\n"
                            "-- Join on BOTH order_id AND product_id.\n"
                            "-- Return: order_id, product_id, quantity, unit_price, shipped_date\n"
                            "-- ordered by order_id, product_id.\n"
                        ),
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_order_items", "variant_id": None, "mount_path": "order_items"},
                    {"asset_id": "ds_shipments", "variant_id": None, "mount_path": "shipments"},
                ],
            },
            "constraints": {
                "allowed_syntax": [
                    "SELECT", "FROM", "AS output_name", "* and table_name.*",
                    "table alias (FROM table AS alias)", "alias.column qualification",
                    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=",
                    "AND", "OR", "NOT", "parentheses", "IS NULL", "IS NOT NULL",
                    "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                    "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
                    "EXTRACT(field FROM source)", "date - date",
                    "CAST(expression AS type)", "expression::type", "COALESCE",
                    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
                    "ON with AND across several columns", "USING (a, b)",
                ],
                "blocked_syntax": [
                    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
                    "subquery in WHERE", "IN (SELECT ...)",
                    "subquery in FROM with an alias", "WITH name AS (...)",
                    "window functions (OVER)", "EXISTS", "correlated subqueries",
                    "CROSS JOIN", "self-joins",
                ],
            },
        },
        "grading": {
            "solution_files": [{"path": "query.sql", "content": sol_s09}],
            "tests": [
                {
                    "test_id": "ix.tile_sql_adv_joining_tables.s09.t1",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": {"columns": cols_s09, "rows": rows_s09},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return only rows where both order_id and product_id match. "
                        "Check that your ON clause uses AND to combine both conditions."
                    ),
                }
            ],
        },
        "feedback": {
            "correct": {"message": "Your ON clause with AND correctly requires both order_id and product_id to match. Rows that share only one of the two columns are excluded."},
            "incorrect": {"message": "Make sure your ON clause checks both order_id AND product_id. A single-column condition would allow false matches."},
            "hints": [
                "The ON clause is a boolean expression — use AND to chain two equality tests.",
                "Qualify each column with its table alias to avoid ambiguity: `oi.order_id = s.order_id AND oi.product_id = s.product_id`.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s06",
        },
    },
}

# ── s13: choice — write_a_left_join_keeping_unmatched_rows + choose_right_or_full_join
# Fact f1: LEFT OUTER JOIN keeps every row of T1, null-filling T2 columns
# Fact f2,f3: RIGHT keeps every T2; FULL keeps both
# Taught by: s10 (explainer tb1,tb2), s11 (explainer tb3,tb4)
s13 = {
    "step_id": "tile_sql_adv_joining_tables.s13",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s13",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.outer_joins", "capability": "write_a_left_join_keeping_unmatched_rows", "fact_ids": ["sql.outer_joins#f1"]},
            {"concept_id": "sql.outer_joins", "capability": "choose_right_or_full_join", "fact_ids": ["sql.outer_joins#f2", "sql.outer_joins#f3"]},
        ],
        "anchors": [
            "sql.outer_joins#assessment:write_a_left_join_keeping_unmatched_rows",
            "sql.outer_joins#assessment:choose_right_or_full_join",
        ],
        "public": {
            "prompt": (
                "You want a result that lists **every customer**, including those with no orders, "
                "with `NULL` in the order columns for customers who have not ordered. "
                "Which join type achieves this when customers is the left table?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "INNER JOIN"},
                {"option_id": "opt_b", "text": "LEFT JOIN"},
                {"option_id": "opt_c", "text": "RIGHT JOIN"},
                {"option_id": "opt_d", "text": "FULL JOIN"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {"message": "An INNER JOIN drops customers with no orders. You would lose any customer who has not placed an order yet."},
                "opt_b": {"message": "Correct. A LEFT JOIN performs an inner join and then adds a row for each left-table row with no match, filling the right-table columns with NULL. Every customer appears at least once."},
                "opt_c": {"message": "A RIGHT JOIN keeps every row of the right table (orders here), not every customer. Customers with no orders would still be dropped."},
                "opt_d": {"message": "A FULL JOIN keeps unmatched rows from both sides. That would also add rows for orders with no matching customer — more than you need here."},
            },
        },
        "feedback": {
            "correct": {"message": "LEFT JOIN keeps every row of the left table (customers) and fills the right-table columns with NULL for any customer with no matching order."},
            "incorrect": {"message": "Think about which table you want to preserve completely. A LEFT JOIN keeps every row of the left table, filling NULLs for unmatched right-table columns."},
            "hints": [
                "An INNER JOIN drops unmatched rows from both sides. You need a join that keeps unmatched rows from one side.",
                "The 'left' in LEFT JOIN refers to the table written first — after FROM.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s10",
        },
    },
}

# ── s14: choice — recognize_that_outer_is_optional ─────────────────────────
# Fact f4: INNER and OUTER are optional; LEFT/RIGHT/FULL imply outer
# Taught by: s11 (explainer tb4)
s14 = {
    "step_id": "tile_sql_adv_joining_tables.s14",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s14",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.outer_joins", "capability": "recognize_that_outer_is_optional", "fact_ids": ["sql.outer_joins#f4"]}
        ],
        "anchors": ["sql.outer_joins#assessment:recognize_that_outer_is_optional"],
        "public": {
            "prompt": (
                "A colleague writes `LEFT OUTER JOIN`. Another writes `LEFT JOIN`. "
                "What is the relationship between these two forms?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "They are identical — OUTER is optional and changes nothing"},
                {"option_id": "opt_b", "text": "LEFT OUTER JOIN keeps more rows than LEFT JOIN"},
                {"option_id": "opt_c", "text": "LEFT JOIN is shorthand for LEFT INNER JOIN, which is different"},
                {"option_id": "opt_d", "text": "OUTER is required; omitting it makes LEFT JOIN behave like INNER JOIN"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. INNER and OUTER are both optional keywords. LEFT, RIGHT, and FULL each already imply an outer join, so LEFT JOIN and LEFT OUTER JOIN are exactly the same."},
                "opt_b": {"message": "The two forms are identical. Adding or removing OUTER does not change the number of rows returned."},
                "opt_c": {"message": "There is no LEFT INNER JOIN. LEFT already implies outer. Writing LEFT JOIN alone means LEFT OUTER JOIN."},
                "opt_d": {"message": "OUTER is optional, not required. LEFT JOIN without OUTER still performs a left outer join — it does not become an inner join."},
            },
        },
        "feedback": {
            "correct": {"message": "OUTER is an optional keyword. LEFT, RIGHT, and FULL each imply an outer join on their own, so the word OUTER adds no new meaning."},
            "incorrect": {"message": "Remember: INNER and OUTER are both optional. LEFT JOIN and LEFT OUTER JOIN are exactly the same operation."},
            "hints": [
                "Think about what the word OUTER adds — does removing it change which rows are kept?",
                "The glossary states that LEFT, RIGHT, and FULL each imply an outer join even without writing OUTER.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s11",
        },
    },
}

# ── s15: code_exercise — LEFT JOIN (practice) ──────────────────────────────
sol_s15 = (
    "SELECT c.customer_id, c.name, o.order_id, o.delivery_time_minutes\n"
    "FROM customers AS c\n"
    "LEFT JOIN orders AS o ON c.customer_id = o.customer_id\n"
    "ORDER BY c.customer_id, o.order_id;\n"
)
cols_s15, rows_s15 = run(sol_s15.rstrip(";\n") + ";")

s15 = {
    "step_id": "tile_sql_adv_joining_tables.s15",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_adv_joining_tables.s15",
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.outer_joins", "capability": "write_a_left_join_keeping_unmatched_rows", "fact_ids": ["sql.outer_joins#f1"]},
        ],
        "anchors": ["sql.outer_joins#practice"],
        "public": {
            "prompt": (
                "Write a query that lists **every customer** along with their orders, "
                "including customers who have placed no orders. "
                "Return **customer_id**, **name**, **order_id**, and **delivery_time_minutes**, "
                "ordered by `customer_id` then `order_id`. "
                "Customers with no orders should appear with `NULL` in the order columns."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- customers columns: customer_id, name, city\n"
                            "-- orders columns: order_id, customer_id, delivery_time_minutes, order_date, region, amount, city\n"
                            "-- Use LEFT JOIN so every customer appears even with no orders.\n"
                            "-- Return: customer_id, name, order_id, delivery_time_minutes\n"
                            "-- ordered by customer_id, order_id.\n"
                        ),
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_customers", "variant_id": None, "mount_path": "customers"},
                    {"asset_id": "ds_orders", "variant_id": None, "mount_path": "orders"},
                ],
            },
            "constraints": {
                "allowed_syntax": [
                    "SELECT", "FROM", "AS output_name", "* and table_name.*",
                    "table alias (FROM table AS alias)", "alias.column qualification",
                    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=",
                    "AND", "OR", "NOT", "parentheses", "IS NULL", "IS NOT NULL",
                    "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                    "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
                    "EXTRACT(field FROM source)", "date - date",
                    "CAST(expression AS type)", "expression::type", "COALESCE",
                    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
                    "ON with AND across several columns", "USING (a, b)",
                    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
                ],
                "blocked_syntax": [
                    "subquery in WHERE", "IN (SELECT ...)",
                    "subquery in FROM with an alias", "WITH name AS (...)",
                    "window functions (OVER)", "EXISTS", "correlated subqueries",
                    "CROSS JOIN", "self-joins",
                ],
            },
        },
        "grading": {
            "solution_files": [{"path": "query.sql", "content": sol_s15}],
            "tests": [
                {
                    "test_id": "ix.tile_sql_adv_joining_tables.s15.t1",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": {"columns": cols_s15, "rows": rows_s15},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return every customer at least once, "
                        "with NULL in order columns for customers who have no orders. "
                        "Check that you are using LEFT JOIN and ordering by customer_id then order_id."
                    ),
                }
            ],
        },
        "feedback": {
            "correct": {"message": "Your LEFT JOIN correctly keeps every customer. Customers 4, 5, and 6 appear with NULL order columns because they have no matching orders."},
            "incorrect": {"message": "Make sure you use LEFT JOIN (not INNER JOIN) so that customers with no orders still appear. Check your ORDER BY clause too."},
            "hints": [
                "Put customers first (after FROM) so it is the 'left' table — LEFT JOIN then keeps every customer row.",
                "Customers with no orders will have NULL for order_id and delivery_time_minutes in the result.",
            ],
            "remediation_step_id": "tile_sql_adv_joining_tables.s10",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# TILE 2: tile_sql_adv_execution_order_subquery_where
# Steps with interactions: s04(check), s05(hands_on), s08(check), s09(hands_on)
# ══════════════════════════════════════════════════════════════════════════════

# ── s04: choice — trace_clause_processing_order ────────────────────────────
# Fact f1: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
# Taught by: s01 (explainer tb1,tb2), s02 (video)
s04_exec = {
    "step_id": "tile_sql_adv_execution_order_subquery_where.s04",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_execution_order_subquery_where.s04",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.clause_execution_order", "capability": "trace_clause_processing_order", "fact_ids": ["sql.clause_execution_order#f1"]}
        ],
        "anchors": ["sql.clause_execution_order#assessment:trace_clause_processing_order"],
        "public": {
            "prompt": (
                "In what order does the database engine process the clauses of a SELECT statement "
                "(ignoring WITH)? Choose the correct sequence."
            ),
            "options": [
                {"option_id": "opt_a", "text": "SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY"},
                {"option_id": "opt_b", "text": "FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY"},
                {"option_id": "opt_c", "text": "FROM → SELECT → WHERE → GROUP BY → HAVING → ORDER BY"},
                {"option_id": "opt_d", "text": "WHERE → FROM → GROUP BY → SELECT → HAVING → ORDER BY"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {"message": "SELECT is not processed first. The engine must first identify the source rows (FROM) and filter them (WHERE) before it can compute SELECT expressions."},
                "opt_b": {"message": "Correct. The processing order is FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY. SELECT is computed near the end, which is why aliases defined there cannot be used in WHERE or HAVING."},
                "opt_c": {"message": "SELECT comes after WHERE, not before. The engine filters rows first, then computes the output expressions."},
                "opt_d": {"message": "WHERE cannot run before FROM — the engine needs to know which table to read from before it can filter rows."},
            },
        },
        "feedback": {
            "correct": {"message": "The processing order is FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY. SELECT is evaluated after filtering and grouping, which explains why its aliases are not visible in WHERE or HAVING."},
            "incorrect": {"message": "Remember: FROM comes first (the engine reads the table), then WHERE filters rows, then GROUP BY and HAVING, then SELECT computes output expressions, and finally ORDER BY sorts."},
            "hints": [
                "Think about what the engine needs before it can filter: it must know which rows exist first.",
                "SELECT is near the end of the processing order — that is why aliases defined in SELECT cannot be used in WHERE.",
            ],
            "remediation_step_id": "tile_sql_adv_execution_order_subquery_where.s01",
        },
    },
}

# ── s05: code_exercise — clause_execution_order (practice) ─────────────────
# Practice: 'Given a broken query that uses a SELECT alias inside WHERE, fix it'
# Broken starter: SELECT order_id, amount * 0.1 AS tax FROM orders WHERE tax > 500
# Fixed solution: write the expression out in WHERE
sol_s05_exec = (
    "SELECT order_id, amount * 0.1 AS tax\n"
    "FROM orders\n"
    "WHERE amount * 0.1 > 500\n"
    "ORDER BY order_id;\n"
)
cols_s05_exec, rows_s05_exec = run(sol_s05_exec.rstrip(";\n") + ";")

s05_exec = {
    "step_id": "tile_sql_adv_execution_order_subquery_where.s05",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_adv_execution_order_subquery_where.s05",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.clause_execution_order", "capability": "explain_where_an_alias_can_and_cannot_be_used", "fact_ids": ["sql.clause_execution_order#f2"]},
        ],
        "anchors": [
            "sql.clause_execution_order#practice",
            "sql.clause_execution_order#assessment:explain_where_an_alias_can_and_cannot_be_used",
        ],
        "public": {
            "prompt": (
                "The query below is broken — it tries to use a SELECT alias inside WHERE:\n\n"
                "```sql\n"
                "SELECT order_id, amount * 0.1 AS tax\n"
                "FROM orders\n"
                "WHERE tax > 500;\n"
                "```\n\n"
                "Fix the query so it returns **order_id** and **tax** (= `amount * 0.1`) "
                "for every order where the tax exceeds 500, ordered by `order_id`. "
                "Write the expression directly in WHERE instead of using the alias."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- This query is broken: WHERE references the alias 'tax' which does not exist yet.\n"
                            "-- Fix it by writing the expression amount * 0.1 directly in the WHERE clause.\n"
                            "SELECT order_id, amount * 0.1 AS tax\n"
                            "FROM orders\n"
                            "WHERE tax > 500;\n"
                        ),
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "variant_id": None, "mount_path": "orders"},
                ],
            },
            "constraints": {
                "allowed_syntax": [
                    "SELECT", "FROM", "AS output_name", "* and table_name.*",
                    "table alias (FROM table AS alias)", "alias.column qualification",
                    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=",
                    "AND", "OR", "NOT", "parentheses", "IS NULL", "IS NOT NULL",
                    "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                    "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
                    "EXTRACT(field FROM source)", "date - date",
                    "CAST(expression AS type)", "expression::type", "COALESCE",
                    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
                    "ON with AND across several columns", "USING (a, b)",
                    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
                ],
                "blocked_syntax": [
                    "subquery in WHERE", "IN (SELECT ...)",
                    "subquery in FROM with an alias", "WITH name AS (...)",
                    "window functions (OVER)", "EXISTS", "correlated subqueries",
                    "CROSS JOIN", "self-joins",
                ],
            },
        },
        "grading": {
            "solution_files": [{"path": "query.sql", "content": sol_s05_exec}],
            "tests": [
                {
                    "test_id": "ix.tile_sql_adv_execution_order_subquery_where.s05.t1",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": {"columns": cols_s05_exec, "rows": rows_s05_exec},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return order_id and tax (amount * 0.1) "
                        "for orders where amount * 0.1 > 500, ordered by order_id. "
                        "Replace the alias 'tax' in WHERE with the full expression."
                    ),
                }
            ],
        },
        "feedback": {
            "correct": {"message": "WHERE runs before SELECT, so the alias 'tax' does not exist yet when WHERE is evaluated. Writing the expression `amount * 0.1` directly in WHERE fixes the query."},
            "incorrect": {"message": "The alias 'tax' is defined in SELECT, but WHERE is processed before SELECT. Replace 'tax' in the WHERE clause with the full expression `amount * 0.1`."},
            "hints": [
                "WHERE is processed before SELECT in the execution order, so aliases defined in SELECT are not visible in WHERE.",
                "Write the expression `amount * 0.1` directly in the WHERE condition instead of using the alias.",
            ],
            "remediation_step_id": "tile_sql_adv_execution_order_subquery_where.s01",
        },
    },
}

# ── s08: choice — write_a_scalar_subquery_comparison ───────────────────────
# Fact f2: scalar subquery returns a single value, used in comparison
# Taught by: s06 (explainer tb1,tb2,tb3)
s08_exec = {
    "step_id": "tile_sql_adv_execution_order_subquery_where.s08",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_execution_order_subquery_where.s08",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.subquery_in_where", "capability": "write_a_scalar_subquery_comparison", "fact_ids": ["sql.subquery_in_where#f2"]}
        ],
        "anchors": ["sql.subquery_in_where#assessment:write_a_scalar_subquery_comparison"],
        "public": {
            "prompt": (
                "You want to find all orders whose `amount` is greater than the average `amount` across all orders. "
                "Which WHERE clause correctly uses a scalar subquery for this?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "WHERE amount > AVG(amount)"},
                {"option_id": "opt_b", "text": "WHERE amount > (SELECT AVG(amount) FROM orders)"},
                {"option_id": "opt_c", "text": "WHERE amount IN (SELECT AVG(amount) FROM orders)"},
                {"option_id": "opt_d", "text": "WHERE amount > (SELECT amount FROM orders)"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {"message": "AVG() is an aggregate function and cannot be used directly in a WHERE clause — WHERE runs before aggregation. Wrap it in a subquery instead."},
                "opt_b": {"message": "Correct. The subquery `(SELECT AVG(amount) FROM orders)` returns a single value, which can then be used as the right-hand side of a comparison in WHERE."},
                "opt_c": {"message": "IN is used when the subquery returns a list of values. AVG returns a single number, so use a comparison operator like > rather than IN."},
                "opt_d": {"message": "`SELECT amount FROM orders` returns many rows, not a single value. A scalar subquery must return exactly one row and one column."},
            },
        },
        "feedback": {
            "correct": {"message": "A scalar subquery returns exactly one value and can be used on the right side of a comparison operator in WHERE. Wrapping AVG() in a subquery lets you use it in WHERE."},
            "incorrect": {"message": "A scalar subquery must return exactly one value. Wrap the aggregate in parentheses as a subquery and use a comparison operator like >."},
            "hints": [
                "Aggregate functions like AVG() cannot appear directly in WHERE — they must be inside a subquery.",
                "A scalar subquery returns one row and one column, so it can be used like a single value in a comparison.",
            ],
            "remediation_step_id": "tile_sql_adv_execution_order_subquery_where.s06",
        },
    },
}

# ── s09: code_exercise — subquery_in_where (practice) ──────────────────────
# Practice anchors: write_in_with_a_subquery AND write_a_scalar_subquery_comparison
# Two queries: Q0 = IN subquery, Q1 = scalar subquery comparison
sol_s09_exec_q0 = (
    "SELECT order_id, customer_id\n"
    "FROM orders\n"
    "WHERE customer_id IN (SELECT customer_id FROM customers WHERE city = 'Lagos')\n"
    "ORDER BY order_id;\n"
)
sol_s09_exec_q1 = (
    "SELECT order_id, delivery_time_minutes\n"
    "FROM orders\n"
    "WHERE delivery_time_minutes > (SELECT AVG(delivery_time_minutes) FROM orders)\n"
    "ORDER BY order_id;\n"
)
cols_s09_exec_q0, rows_s09_exec_q0 = run(sol_s09_exec_q0.rstrip(";\n") + ";")
cols_s09_exec_q1, rows_s09_exec_q1 = run(sol_s09_exec_q1.rstrip(";\n") + ";")

sol_s09_exec_combined = sol_s09_exec_q0 + "\n" + sol_s09_exec_q1

s09_exec = {
    "step_id": "tile_sql_adv_execution_order_subquery_where.s09",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_adv_execution_order_subquery_where.s09",
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.subquery_in_where", "capability": "write_in_with_a_subquery", "fact_ids": ["sql.subquery_in_where#f1"]},
            {"concept_id": "sql.subquery_in_where", "capability": "write_a_scalar_subquery_comparison", "fact_ids": ["sql.subquery_in_where#f2"]},
        ],
        "anchors": [
            "sql.subquery_in_where#practice",
            "sql.subquery_in_where#assessment:write_in_with_a_subquery",
            "sql.subquery_in_where#assessment:write_a_scalar_subquery_comparison",
        ],
        "public": {
            "prompt": (
                "Write **two** queries in the file, in order:\n\n"
                "**Query 1** — Return **order_id** and **customer_id** for orders placed by customers "
                "whose `city` is `'Lagos'`. Use `IN` with a subquery on the `customers` table. "
                "Order by `order_id`.\n\n"
                "**Query 2** — Return **order_id** and **delivery_time_minutes** for orders whose "
                "`delivery_time_minutes` is above the average delivery time across all orders. "
                "Use a scalar subquery with `AVG`. Order by `order_id`."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- orders columns: order_id, customer_id, delivery_time_minutes, order_date, region, amount, city\n"
                            "-- customers columns: customer_id, name, city\n"
                            "\n"
                            "-- Query 1: orders from Lagos customers (use IN with a subquery)\n"
                            "\n"
                            "\n"
                            "-- Query 2: orders above average delivery time (use a scalar subquery with AVG)\n"
                            "\n"
                        ),
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "variant_id": None, "mount_path": "orders"},
                    {"asset_id": "ds_customers", "variant_id": None, "mount_path": "customers"},
                ],
            },
            "constraints": {
                "allowed_syntax": [
                    "SELECT", "FROM", "AS output_name", "* and table_name.*",
                    "table alias (FROM table AS alias)", "alias.column qualification",
                    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=",
                    "AND", "OR", "NOT", "parentheses", "IS NULL", "IS NOT NULL",
                    "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                    "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
                    "EXTRACT(field FROM source)", "date - date",
                    "CAST(expression AS type)", "expression::type", "COALESCE",
                    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
                    "ON with AND across several columns", "USING (a, b)",
                    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
                    "subquery in WHERE", "IN (SELECT ...)",
                ],
                "blocked_syntax": [
                    "subquery in FROM with an alias", "WITH name AS (...)",
                    "window functions (OVER)", "EXISTS", "correlated subqueries",
                    "CROSS JOIN", "self-joins",
                ],
            },
        },
        "grading": {
            "solution_files": [{"path": "query.sql", "content": sol_s09_exec_combined}],
            "tests": [
                {
                    "test_id": "ix.tile_sql_adv_execution_order_subquery_where.s09.t1",
                    "kind": "query_result_equals",
                    "spec": {
                        "statement": 0,
                        "expected": {"columns": cols_s09_exec_q0, "rows": rows_s09_exec_q0},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Query 1 should return order_id and customer_id for orders from Lagos customers, "
                        "using IN with a subquery on customers. Order by order_id."
                    ),
                },
                {
                    "test_id": "ix.tile_sql_adv_execution_order_subquery_where.s09.t2",
                    "kind": "query_result_equals",
                    "spec": {
                        "statement": 1,
                        "expected": {"columns": cols_s09_exec_q1, "rows": rows_s09_exec_q1},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Query 2 should return order_id and delivery_time_minutes for orders above the average "
                        "delivery time, using a scalar subquery with AVG. Order by order_id."
                    ),
                },
            ],
        },
        "feedback": {
            "correct": {"message": "Both subquery forms work: IN (SELECT ...) tests membership in a list, while a scalar subquery returns one value for a direct comparison. Both run the inner query first, then filter the outer rows."},
            "incorrect": {"message": "Check each query separately. Query 1 needs IN (SELECT customer_id FROM customers WHERE city = 'Lagos'). Query 2 needs > (SELECT AVG(delivery_time_minutes) FROM orders)."},
            "hints": [
                "For Query 1, the subquery goes inside IN: `WHERE customer_id IN (SELECT customer_id FROM customers WHERE city = 'Lagos')`.",
                "For Query 2, wrap AVG in a subquery: `WHERE delivery_time_minutes > (SELECT AVG(delivery_time_minutes) FROM orders)`.",
            ],
            "remediation_step_id": "tile_sql_adv_execution_order_subquery_where.s06",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# TILE 3: tile_sql_adv_subquery_from_cte
# Steps with interactions: s04(check), s05(hands_on), s08(check), s09(hands_on)
# ══════════════════════════════════════════════════════════════════════════════

# ── s04: choice — use_inner_output_columns_in_the_outer_query ───────────────
# Fact f2: outer query sees inner query's output column names
# Taught by: s01 (explainer tb1,tb2), s02 (explainer tb3)
s04_cte = {
    "step_id": "tile_sql_adv_subquery_from_cte.s04",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_subquery_from_cte.s04",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.subquery_in_from", "capability": "use_inner_output_columns_in_the_outer_query", "fact_ids": ["sql.subquery_in_from#f2"]}
        ],
        "anchors": ["sql.subquery_in_from#assessment:use_inner_output_columns_in_the_outer_query"],
        "public": {
            "prompt": (
                "A FROM subquery is written as:\n\n"
                "```sql\n"
                "SELECT region, SUM(amount) AS total\n"
                "FROM orders\n"
                "GROUP BY region\n"
                "```\n\n"
                "The outer query reads this subquery as a virtual table aliased `sub`. "
                "Which column names can the outer query use from `sub`?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "region and total — the inner query's output column names"},
                {"option_id": "opt_b", "text": "region and SUM(amount) — the original expression, not the alias"},
                {"option_id": "opt_c", "text": "amount and region — the original table's columns"},
                {"option_id": "opt_d", "text": "sub.* only — individual columns cannot be named"},
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. The outer query sees the inner query's output column names: `region` (the column name) and `total` (the AS alias). The original expression SUM(amount) is not visible."},
                "opt_b": {"message": "The outer query sees the alias `total`, not the raw expression `SUM(amount)`. Once a column is aliased with AS, the alias is the name the outer query uses."},
                "opt_c": {"message": "The outer query cannot see the original table's columns directly — it only sees what the inner SELECT outputs. The inner SELECT outputs `region` and `total`."},
                "opt_d": {"message": "Individual columns from a subquery can be named and used in the outer query. The outer query sees `region` and `total` as named columns of the virtual table."},
            },
        },
        "feedback": {
            "correct": {"message": "The outer query sees the inner query's output column names. An AS alias in the inner SELECT becomes the column name that the outer query uses."},
            "incorrect": {"message": "The outer query sees only what the inner SELECT outputs. Column names are the inner query's own column names or AS aliases — not the original expressions."},
            "hints": [
                "Think of the subquery as a temporary table. Its column names are whatever the inner SELECT names them.",
                "If the inner SELECT uses AS to rename a column, the outer query uses that alias, not the original expression.",
            ],
            "remediation_step_id": "tile_sql_adv_subquery_from_cte.s01",
        },
    },
}

# ── s05: code_exercise — subquery_in_from (practice) ───────────────────────
sol_s05_cte = (
    "SELECT customer_id, order_count\n"
    "FROM (\n"
    "    SELECT customer_id, COUNT(*) AS order_count\n"
    "    FROM orders\n"
    "    GROUP BY customer_id\n"
    ") AS order_counts\n"
    "WHERE order_count >= 4\n"
    "ORDER BY customer_id;\n"
)
cols_s05_cte, rows_s05_cte = run(sol_s05_cte.rstrip(";\n") + ";")

s05_cte = {
    "step_id": "tile_sql_adv_subquery_from_cte.s05",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_adv_subquery_from_cte.s05",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.subquery_in_from", "capability": "write_a_from_subquery_with_alias", "fact_ids": ["sql.subquery_in_from#f1"]},
            {"concept_id": "sql.subquery_in_from", "capability": "use_inner_output_columns_in_the_outer_query", "fact_ids": ["sql.subquery_in_from#f2"]},
        ],
        "anchors": [
            "sql.subquery_in_from#practice",
            "sql.subquery_in_from#assessment:write_a_from_subquery_with_alias",
            "sql.subquery_in_from#assessment:use_inner_output_columns_in_the_outer_query",
        ],
        "public": {
            "prompt": (
                "Write a query that uses a **FROM subquery** to find high-volume customers. "
                "The inner query should compute **customer_id** and **order_count** "
                "(= `COUNT(*)`) per customer from the `orders` table, grouped by `customer_id`. "
                "Give the subquery the alias `order_counts`. "
                "The outer query should return **customer_id** and **order_count** "
                "for customers with `order_count >= 4`, ordered by `customer_id`."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- orders columns: order_id, customer_id, delivery_time_minutes, order_date, region, amount, city\n"
                            "-- Write: SELECT ... FROM (inner query) AS order_counts WHERE order_count >= 4\n"
                            "-- The inner query: SELECT customer_id, COUNT(*) AS order_count FROM orders GROUP BY customer_id\n"
                        ),
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "variant_id": None, "mount_path": "orders"},
                ],
            },
            "constraints": {
                "allowed_syntax": [
                    "SELECT", "FROM", "AS output_name", "* and table_name.*",
                    "table alias (FROM table AS alias)", "alias.column qualification",
                    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=",
                    "AND", "OR", "NOT", "parentheses", "IS NULL", "IS NOT NULL",
                    "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                    "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
                    "EXTRACT(field FROM source)", "date - date",
                    "CAST(expression AS type)", "expression::type", "COALESCE",
                    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
                    "ON with AND across several columns", "USING (a, b)",
                    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
                    "subquery in WHERE", "IN (SELECT ...)",
                    "subquery in FROM with an alias",
                ],
                "blocked_syntax": [
                    "WITH name AS (...)",
                    "window functions (OVER)", "EXISTS", "correlated subqueries",
                    "CROSS JOIN", "self-joins",
                ],
            },
        },
        "grading": {
            "solution_files": [{"path": "query.sql", "content": sol_s05_cte}],
            "tests": [
                {
                    "test_id": "ix.tile_sql_adv_subquery_from_cte.s05.t1",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": {"columns": cols_s05_cte, "rows": rows_s05_cte},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return customer_id and order_count for customers with 4 or more orders, "
                        "ordered by customer_id. Check that the subquery is wrapped in parentheses with an alias "
                        "and that the outer WHERE uses the alias column name."
                    ),
                }
            ],
        },
        "feedback": {
            "correct": {"message": "Your FROM subquery correctly wraps the aggregation in parentheses with an alias. The outer query then filters on the inner query's output column `order_count`."},
            "incorrect": {"message": "Make sure the inner query is enclosed in parentheses and given an alias (e.g. AS order_counts). The outer WHERE should reference the column name from the inner SELECT."},
            "hints": [
                "The structure is: SELECT ... FROM (SELECT ... FROM orders GROUP BY customer_id) AS order_counts WHERE order_count >= 4.",
                "The outer query can only use column names that the inner SELECT outputs — here `customer_id` and `order_count`.",
            ],
            "remediation_step_id": "tile_sql_adv_subquery_from_cte.s01",
        },
    },
}

# ── s08: choice — rewrite_a_nested_subquery_as_a_cte ───────────────────────
# Fact f3: CTEs are an alternative to nested subqueries, easier to follow
# Taught by: s06 (explainer tb1,tb2,tb3)
s08_cte = {
    "step_id": "tile_sql_adv_subquery_from_cte.s08",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_adv_subquery_from_cte.s08",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.cte", "capability": "rewrite_a_nested_subquery_as_a_cte", "fact_ids": ["sql.cte#f3"]}
        ],
        "anchors": ["sql.cte#assessment:rewrite_a_nested_subquery_as_a_cte"],
        "public": {
            "prompt": (
                "The query below uses a nested FROM subquery:\n\n"
                "```sql\n"
                "SELECT customer_id, order_count\n"
                "FROM (\n"
                "    SELECT customer_id, COUNT(*) AS order_count\n"
                "    FROM orders\n"
                "    GROUP BY customer_id\n"
                ") AS counts\n"
                "WHERE order_count >= 4;\n"
                "```\n\n"
                "Which CTE rewrite is correct?"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": (
                        "WITH counts AS (\n"
                        "    SELECT customer_id, COUNT(*) AS order_count\n"
                        "    FROM orders GROUP BY customer_id\n"
                        ")\n"
                        "SELECT customer_id, order_count FROM counts WHERE order_count >= 4;"
                    ),
                },
                {
                    "option_id": "opt_b",
                    "text": (
                        "SELECT customer_id, order_count\n"
                        "FROM orders WITH counts AS (\n"
                        "    SELECT customer_id, COUNT(*) AS order_count GROUP BY customer_id\n"
                        ")\n"
                        "WHERE order_count >= 4;"
                    ),
                },
                {
                    "option_id": "opt_c",
                    "text": (
                        "WITH counts AS SELECT customer_id, COUNT(*) AS order_count\n"
                        "FROM orders GROUP BY customer_id\n"
                        "SELECT customer_id, order_count FROM counts WHERE order_count >= 4;"
                    ),
                },
                {
                    "option_id": "opt_d",
                    "text": (
                        "SELECT customer_id, order_count\n"
                        "FROM counts\n"
                        "WHERE order_count >= 4\n"
                        "WITH counts AS (SELECT customer_id, COUNT(*) AS order_count FROM orders GROUP BY customer_id);"
                    ),
                },
            ],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {"message": "Correct. WITH comes before the main SELECT, the CTE body is enclosed in parentheses after AS, and the main query reads the CTE by name as if it were a table."},
                "opt_b": {"message": "WITH cannot appear inside FROM. The WITH clause must come before the entire SELECT statement, not inside it."},
                "opt_c": {"message": "The CTE body must be enclosed in parentheses: `WITH counts AS (SELECT ...)`. Missing parentheses makes this invalid syntax."},
                "opt_d": {"message": "WITH must come before the main SELECT, not after it. The CTE is defined first, then the main query reads it."},
            },
        },
        "feedback": {
            "correct": {"message": "A CTE is written as WITH name AS (query) before the main SELECT. The main query then reads the CTE by name, just like a table."},
            "incorrect": {"message": "Remember: WITH comes before the main SELECT, the CTE body goes inside parentheses after AS, and the main query reads the CTE by name."},
            "hints": [
                "The WITH clause always comes first — before the main SELECT.",
                "The CTE body must be enclosed in parentheses: WITH name AS (SELECT ...).",
            ],
            "remediation_step_id": "tile_sql_adv_subquery_from_cte.s06",
        },
    },
}

# ── s09: code_exercise — CTE (practice) ────────────────────────────────────
sol_s09_cte = (
    "WITH order_counts AS (\n"
    "    SELECT customer_id, COUNT(*) AS order_count\n"
    "    FROM orders\n"
    "    GROUP BY customer_id\n"
    ")\n"
    "SELECT customer_id, order_count\n"
    "FROM order_counts\n"
    "WHERE order_count >= 4\n"
    "ORDER BY customer_id;\n"
)
cols_s09_cte, rows_s09_cte = run(sol_s09_cte.rstrip(";\n") + ";")

s09_cte = {
    "step_id": "tile_sql_adv_subquery_from_cte.s09",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_adv_subquery_from_cte.s09",
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {"concept_id": "sql.cte", "capability": "write_a_with_clause", "fact_ids": ["sql.cte#f1", "sql.cte#f2"]},
        ],
        "anchors": [
            "sql.cte#practice",
            "sql.cte#assessment:write_a_with_clause",
        ],
        "public": {
            "prompt": (
                "Rewrite the FROM-subquery approach as a CTE. "
                "Use a `WITH` clause to define `order_counts` — a named result that computes "
                "**customer_id** and **order_count** (= `COUNT(*)`) per customer from `orders`. "
                "Then write the main query to return **customer_id** and **order_count** "
                "for customers with `order_count >= 4`, ordered by `customer_id`."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- orders columns: order_id, customer_id, delivery_time_minutes, order_date, region, amount, city\n"
                            "-- Write: WITH order_counts AS (...) SELECT ... FROM order_counts WHERE order_count >= 4\n"
                        ),
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "variant_id": None, "mount_path": "orders"},
                ],
            },
            "constraints": {
                "allowed_syntax": [
                    "SELECT", "FROM", "AS output_name", "* and table_name.*",
                    "table alias (FROM table AS alias)", "alias.column qualification",
                    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=",
                    "AND", "OR", "NOT", "parentheses", "IS NULL", "IS NOT NULL",
                    "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET",
                    "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY", "HAVING",
                    "CASE WHEN ... THEN ... ELSE ... END",
                    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
                    "EXTRACT(field FROM source)", "date - date",
                    "CAST(expression AS type)", "expression::type", "COALESCE",
                    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
                    "ON with AND across several columns", "USING (a, b)",
                    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
                    "subquery in WHERE", "IN (SELECT ...)",
                    "subquery in FROM with an alias", "WITH name AS (...)",
                ],
                "blocked_syntax": [
                    "window functions (OVER)", "EXISTS", "correlated subqueries",
                    "CROSS JOIN", "self-joins",
                ],
            },
        },
        "grading": {
            "solution_files": [{"path": "query.sql", "content": sol_s09_cte}],
            "tests": [
                {
                    "test_id": "ix.tile_sql_adv_subquery_from_cte.s09.t1",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": {"columns": cols_s09_cte, "rows": rows_s09_cte},
                        "ordered": True,
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your CTE query should return customer_id and order_count for customers with 4 or more orders, "
                        "ordered by customer_id. Check that WITH comes before SELECT and the CTE body is in parentheses."
                    ),
                }
            ],
        },
        "feedback": {
            "correct": {"message": "Your WITH clause defines order_counts as a named temporary result. The main query then reads it by name, just like a table — producing the same result as the FROM-subquery version."},
            "incorrect": {"message": "Make sure WITH comes before the main SELECT, the CTE body is enclosed in parentheses after AS, and the main query reads the CTE by name."},
            "hints": [
                "The structure is: WITH order_counts AS (SELECT ... FROM orders GROUP BY customer_id) SELECT ... FROM order_counts WHERE ...",
                "The CTE body goes inside parentheses after AS. The main query then uses the CTE name as if it were a table.",
            ],
            "remediation_step_id": "tile_sql_adv_subquery_from_cte.s06",
        },
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# Assemble the output
# ══════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_006_da_sql_rest",
    "tiles": [
        {
            "tile_id": "tile_sql_adv_joining_tables",
            "interactions": [s04, s05, s07, s08, s09, s13, s14, s15],
        },
        {
            "tile_id": "tile_sql_adv_execution_order_subquery_where",
            "interactions": [s04_exec, s05_exec, s08_exec, s09_exec],
        },
        {
            "tile_id": "tile_sql_adv_subquery_from_cte",
            "interactions": [s04_cte, s05_cte, s08_cte, s09_cte],
        },
    ],
}

out_path = BATCH / "interactions.part.c3.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"Written {out_path}")

# Print summary
for tile in output["tiles"]:
    print(f"  {tile['tile_id']}: {len(tile['interactions'])} interactions")
    for ix in tile["interactions"]:
        print(f"    {ix['step_id']} -> {ix['interaction']['type']}")
