"""Build interactions.part.c2.json for tiles:
  tile_sql_style_conventions
  tile_sql_text_dates_casts
  tile_sql_null_fallback_and_union
"""
import json, sys
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers.sandbox import node_run
from checkers.dataset import resolve_dataset

with open('batches/final_batch_006_da_sql_rest/scenario_asset_registry.json') as f:
    registry = json.load(f)


def run_sql(sql, mounts):
    """Run SQL against mounted tables; return the node_run result dict."""
    tables = []
    for asset_id, mount_path, variant_id in mounts:
        cols, rows = resolve_dataset(registry, asset_id, variant_id)
        names = [c['name'] for c in cols]
        tables.append({
            'name': mount_path,
            'columns': [{'name': c['name'], 'type': c.get('type', 'string')} for c in cols],
            'rows': [[r[n] for n in names] for r in rows]
        })
    from checkers.sqlsyntax import split_statements
    stmts = split_statements(sql)
    result = node_run({'tables': tables, 'scripts': [{'id': 'q', 'statements': stmts}]}, 'run_sql.mjs')
    return result['results']['q']


# ─────────────────────────────────────────────────────────────────────────────
# Shared syntax lists (copied verbatim from glossary practice anchors)
# ─────────────────────────────────────────────────────────────────────────────

STYLE_ALLOWED = [
    "SELECT", "FROM", "AS output_name", "* and table_name.*",
    "table alias (FROM table AS alias)", "alias.column qualification",
    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=", "AND", "OR", "NOT",
    "parentheses", "IS NULL", "IS NOT NULL", "ORDER BY", "ASC", "DESC",
    "LIMIT", "OFFSET", "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY",
    "HAVING", "CASE WHEN ... THEN ... ELSE ... END"
]
STYLE_BLOCKED = [
    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
    "EXTRACT(field FROM source)", "date - date",
    "CAST(expression AS type)", "expression::type", "COALESCE",
    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
    "ON with AND across several columns", "USING (a, b)",
    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
    "subquery in WHERE", "IN (SELECT ...)", "subquery in FROM with an alias",
    "WITH name AS (...)", "window functions (OVER)", "EXISTS",
    "correlated subqueries", "CROSS JOIN", "self-joins"
]

STRING_ALLOWED = [
    "SELECT", "FROM", "AS output_name", "* and table_name.*",
    "table alias (FROM table AS alias)", "alias.column qualification",
    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=", "AND", "OR", "NOT",
    "parentheses", "IS NULL", "IS NOT NULL", "ORDER BY", "ASC", "DESC",
    "LIMIT", "OFFSET", "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY",
    "HAVING", "CASE WHEN ... THEN ... ELSE ... END",
    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH"
]
STRING_BLOCKED = [
    "EXTRACT(field FROM source)", "date - date",
    "CAST(expression AS type)", "expression::type", "COALESCE",
    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
    "ON with AND across several columns", "USING (a, b)",
    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
    "subquery in WHERE", "IN (SELECT ...)", "subquery in FROM with an alias",
    "WITH name AS (...)", "window functions (OVER)", "EXISTS",
    "correlated subqueries", "CROSS JOIN", "self-joins"
]

DATE_ALLOWED = [
    "SELECT", "FROM", "AS output_name", "* and table_name.*",
    "table alias (FROM table AS alias)", "alias.column qualification",
    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=", "AND", "OR", "NOT",
    "parentheses", "IS NULL", "IS NOT NULL", "ORDER BY", "ASC", "DESC",
    "LIMIT", "OFFSET", "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY",
    "HAVING", "CASE WHEN ... THEN ... ELSE ... END",
    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
    "EXTRACT(field FROM source)", "date - date"
]
DATE_BLOCKED = [
    "CAST(expression AS type)", "expression::type", "COALESCE",
    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
    "ON with AND across several columns", "USING (a, b)",
    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
    "subquery in WHERE", "IN (SELECT ...)", "subquery in FROM with an alias",
    "WITH name AS (...)", "window functions (OVER)", "EXISTS",
    "correlated subqueries", "CROSS JOIN", "self-joins"
]

CAST_ALLOWED = [
    "SELECT", "FROM", "AS output_name", "* and table_name.*",
    "table alias (FROM table AS alias)", "alias.column qualification",
    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=", "AND", "OR", "NOT",
    "parentheses", "IS NULL", "IS NOT NULL", "ORDER BY", "ASC", "DESC",
    "LIMIT", "OFFSET", "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY",
    "HAVING", "CASE WHEN ... THEN ... ELSE ... END",
    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
    "EXTRACT(field FROM source)", "date - date",
    "CAST(expression AS type)", "expression::type"
]
CAST_BLOCKED = [
    "COALESCE", "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
    "ON with AND across several columns", "USING (a, b)",
    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
    "subquery in WHERE", "IN (SELECT ...)", "subquery in FROM with an alias",
    "WITH name AS (...)", "window functions (OVER)", "EXISTS",
    "correlated subqueries", "CROSS JOIN", "self-joins"
]

COALESCE_ALLOWED = [
    "SELECT", "FROM", "AS output_name", "* and table_name.*",
    "table alias (FROM table AS alias)", "alias.column qualification",
    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=", "AND", "OR", "NOT",
    "parentheses", "IS NULL", "IS NOT NULL", "ORDER BY", "ASC", "DESC",
    "LIMIT", "OFFSET", "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY",
    "HAVING", "CASE WHEN ... THEN ... ELSE ... END",
    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
    "EXTRACT(field FROM source)", "date - date",
    "CAST(expression AS type)", "expression::type", "COALESCE"
]
COALESCE_BLOCKED = [
    "UNION", "UNION ALL", "JOIN / INNER JOIN", "ON", "USING",
    "ON with AND across several columns", "USING (a, b)",
    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
    "subquery in WHERE", "IN (SELECT ...)", "subquery in FROM with an alias",
    "WITH name AS (...)", "window functions (OVER)", "EXISTS",
    "correlated subqueries", "CROSS JOIN", "self-joins"
]

UNION_ALLOWED = [
    "SELECT", "FROM", "AS output_name", "* and table_name.*",
    "table alias (FROM table AS alias)", "alias.column qualification",
    "DISTINCT", "ALL", "WHERE", "< > <= >= = <> !=", "AND", "OR", "NOT",
    "parentheses", "IS NULL", "IS NOT NULL", "ORDER BY", "ASC", "DESC",
    "LIMIT", "OFFSET", "COUNT", "SUM", "AVG", "MIN", "MAX", "GROUP BY",
    "HAVING", "CASE WHEN ... THEN ... ELSE ... END",
    "LOWER", "UPPER", "TRIM", "CONCAT", "LENGTH",
    "EXTRACT(field FROM source)", "date - date",
    "CAST(expression AS type)", "expression::type", "COALESCE",
    "UNION", "UNION ALL"
]
UNION_BLOCKED = [
    "JOIN / INNER JOIN", "ON", "USING",
    "ON with AND across several columns", "USING (a, b)",
    "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "OUTER keyword",
    "subquery in WHERE", "IN (SELECT ...)", "subquery in FROM with an alias",
    "WITH name AS (...)", "window functions (OVER)", "EXISTS",
    "correlated subqueries", "CROSS JOIN", "self-joins"
]

# ─────────────────────────────────────────────────────────────────────────────
# Run solutions to get expected values
# ─────────────────────────────────────────────────────────────────────────────

ORDERS_MOUNTS = [('ds_orders', 'orders', None)]
CUSTOMERS_MOUNTS = [('ds_customers', 'customers', None)]
BOTH_MOUNTS = [('ds_orders', 'orders', None), ('ds_customers', 'customers', None)]

# ── style_conventions.s03 solution ──────────────────────────────────────────
STYLE_SOLUTION = """\
SELECT order_id,
       amount
  FROM orders AS o
 WHERE o.region = 'south'
"""
r_style = run_sql(STYLE_SOLUTION, ORDERS_MOUNTS)
assert r_style['ok'], f"style solution failed: {r_style.get('error')}"
STYLE_EXPECTED = {'columns': r_style['columns'], 'rows': r_style['rows']}
print("style_conventions expected:", STYLE_EXPECTED)

# ── string_functions.s03 solution ────────────────────────────────────────────
STRING_SOLUTION = """\
SELECT customer_id,
       LOWER(TRIM(city))          AS city_clean,
       CONCAT(name, ' (', city, ')') AS label
  FROM customers AS c
"""
r_str = run_sql(STRING_SOLUTION, CUSTOMERS_MOUNTS)
assert r_str['ok'], f"string solution failed: {r_str.get('error')}"
STRING_EXPECTED = {'columns': r_str['columns'], 'rows': r_str['rows']}
print("string_functions expected:", STRING_EXPECTED)

# ── date_time_functions.s06 solution ─────────────────────────────────────────
DATE_SOLUTION = """\
SELECT order_id,
       EXTRACT(MONTH FROM order_date)    AS order_month,
       order_date - DATE '2024-01-01'    AS days_since_start
  FROM orders AS o
"""
r_dt = run_sql(DATE_SOLUTION, ORDERS_MOUNTS)
assert r_dt['ok'], f"date solution failed: {r_dt.get('error')}"
DATE_EXPECTED = {'columns': r_dt['columns'], 'rows': r_dt['rows']}
print("date_time expected:", DATE_EXPECTED)

# ── type_casting.s09 solution (two statements) ───────────────────────────────
CAST_SOLUTION = """\
SELECT order_id,
       CAST(amount AS TEXT) AS amount_text
  FROM orders AS o;
SELECT order_id,
       amount::TEXT AS amount_text
  FROM orders AS o;
"""
r_cast = run_sql(CAST_SOLUTION, ORDERS_MOUNTS)
assert r_cast['ok'], f"cast solution failed: {r_cast.get('error')}"
CAST_EXPECTED_0 = {'columns': r_cast['outputs'][0]['columns'], 'rows': r_cast['outputs'][0]['rows']}
CAST_EXPECTED_1 = {'columns': r_cast['outputs'][1]['columns'], 'rows': r_cast['outputs'][1]['rows']}
print("type_casting expected stmt0:", CAST_EXPECTED_0)
print("type_casting expected stmt1:", CAST_EXPECTED_1)

# ── coalesce.s04 solution ────────────────────────────────────────────────────
COALESCE_SOLUTION = """\
SELECT customer_id,
       name,
       COALESCE(city, 'Unknown') AS city
  FROM customers AS c
"""
r_coal = run_sql(COALESCE_SOLUTION, CUSTOMERS_MOUNTS)
assert r_coal['ok'], f"coalesce solution failed: {r_coal.get('error')}"
COALESCE_EXPECTED = {'columns': r_coal['columns'], 'rows': r_coal['rows']}
print("coalesce expected:", COALESCE_EXPECTED)

# ── union.s08 solution (two statements) ──────────────────────────────────────
UNION_SOLUTION = """\
SELECT customer_id
  FROM customers AS c
 WHERE c.city = 'Lagos'
UNION
SELECT customer_id
  FROM orders AS o
 WHERE o.region = 'south';
SELECT customer_id
  FROM customers AS c
 WHERE c.city = 'Lagos'
UNION ALL
SELECT customer_id
  FROM orders AS o
 WHERE o.region = 'south';
"""
r_union = run_sql(UNION_SOLUTION, BOTH_MOUNTS)
assert r_union['ok'], f"union solution failed: {r_union.get('error')}"
UNION_EXPECTED_0 = {'columns': r_union['outputs'][0]['columns'], 'rows': r_union['outputs'][0]['rows']}
UNION_EXPECTED_1 = {'columns': r_union['outputs'][1]['columns'], 'rows': r_union['outputs'][1]['rows']}
print("union expected stmt0:", UNION_EXPECTED_0)
print("union expected stmt1:", UNION_EXPECTED_1)

# ─────────────────────────────────────────────────────────────────────────────
# Build the interactions
# ─────────────────────────────────────────────────────────────────────────────

tiles = []

# ═══════════════════════════════════════════════════════════════════════════
# TILE: tile_sql_style_conventions
# Steps with interactions: s02 (check/choice), s03 (hands_on/code_exercise)
# ═══════════════════════════════════════════════════════════════════════════

style_interactions = []

# ── s02: choice — lay_out_a_query_with_line_breaks_and_spacing ───────────────
# Tests f4 and f5 (taught in s01 via tb2)
# Difficulty: intro (first check in tile)
style_interactions.append({
    "step_id": "tile_sql_style_conventions.s02",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_style_conventions.s02",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.style_conventions",
                "capability": "lay_out_a_query_with_line_breaks_and_spacing",
                "fact_ids": ["sql.style_conventions#f4", "sql.style_conventions#f5"]
            }
        ],
        "anchors": [
            "sql.style_conventions#assessment:lay_out_a_query_with_line_breaks_and_spacing"
        ],
        "public": {
            "prompt": (
                "Which version of this query follows the style-guide rules for keyword alignment, "
                "spacing, and line breaks?\n\n"
                "**A.**\n```sql\nSELECT order_id, amount FROM orders WHERE region='south' AND amount>5000\n```\n\n"
                "**B.**\n```sql\nSELECT order_id,\n       amount\n  FROM orders AS o\n WHERE o.region = 'south'\n   AND o.amount > 5000\n```\n\n"
                "**C.**\n```sql\nSELECT order_id, amount\nFROM orders\nWHERE region = 'south' AND\namount > 5000\n```\n\n"
                "**D.**\n```sql\nSELECT order_id,\n       amount\nFROM orders AS o\nWHERE o.region = 'south' AND o.amount > 5000\n```"
            ),
            "options": [
                {"option_id": "opt_a", "text": "A — single line, no spaces around ="},
                {"option_id": "opt_b", "text": "B — keywords right-aligned, AND on its own line"},
                {"option_id": "opt_c", "text": "C — AND at end of line, FROM not indented"},
                {"option_id": "opt_d", "text": "D — FROM not right-aligned, AND on same line as condition"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "A puts everything on one line with no spaces around = and no line breaks. "
                        "The style guide requires each root keyword on its own line, spaces around =, "
                        "and a newline before AND."
                    )
                },
                "opt_b": {
                    "message": (
                        "Correct. B right-aligns the root keywords (SELECT, FROM, WHERE) so they end "
                        "on the same character boundary, puts AND on its own line, and uses spaces "
                        "around = — all required by the style guide."
                    )
                },
                "opt_c": {
                    "message": (
                        "C puts AND at the end of the WHERE line rather than at the start of the next "
                        "line. The style guide requires a newline *before* AND or OR, not after."
                    )
                },
                "opt_d": {
                    "message": (
                        "D keeps AND on the same line as the first condition instead of starting a new "
                        "line before it, and FROM is not right-aligned to the same column as SELECT and WHERE."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "Each root keyword starts a new line and is right-aligned to the same column. "
                    "AND and OR always start their own line. Spaces appear around = and after commas."
                )
            },
            "incorrect": {
                "message": (
                    "Review the layout rules: each root keyword (SELECT, FROM, WHERE) starts a new line "
                    "and is right-aligned so the keywords end on the same column. AND and OR always "
                    "begin a new line, not end the previous one."
                )
            },
            "hints": [
                "Look at where AND appears — does it end the previous line or start the next one?",
                "Check whether SELECT, FROM, and WHERE all end on the same character column."
            ],
            "remediation_step_id": "tile_sql_style_conventions.s01"
        }
    }
})

# ── s03: code_exercise — style_conventions practice ──────────────────────────
# Tests f1–f5 (all taught in s01 via tb1+tb2)
# The practice anchor says: rewrite a working but inconsistently formatted query
# Success: same result, follows keyword case, alias, alignment, spacing, line-break conventions
style_interactions.append({
    "step_id": "tile_sql_style_conventions.s03",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_style_conventions.s03",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.style_conventions",
                "capability": "apply_keyword_and_column_case",
                "fact_ids": ["sql.style_conventions#f1", "sql.style_conventions#f2"]
            },
            {
                "concept_id": "sql.style_conventions",
                "capability": "write_a_conventional_alias",
                "fact_ids": ["sql.style_conventions#f3"]
            },
            {
                "concept_id": "sql.style_conventions",
                "capability": "lay_out_a_query_with_line_breaks_and_spacing",
                "fact_ids": ["sql.style_conventions#f4", "sql.style_conventions#f5"]
            }
        ],
        "anchors": [
            "sql.style_conventions#practice",
            "sql.style_conventions#assessment:apply_keyword_and_column_case",
            "sql.style_conventions#assessment:write_a_conventional_alias",
            "sql.style_conventions#assessment:lay_out_a_query_with_line_breaks_and_spacing"
        ],
        "public": {
            "prompt": (
                "The query below works but breaks every style-guide rule. "
                "Rewrite it so it follows the conventions: keywords in uppercase, "
                "column names in lowercase, a meaningful alias with AS, each root keyword "
                "right-aligned on its own line (the 'river'), spaces around = and after commas, "
                "and a newline before AND.\n\n"
                "The rewritten query must return **order_id** and **amount** for orders "
                "in the **'south'** region — the same rows as the original.\n\n"
                "```sql\n"
                "select ORDER_ID, AMOUNT from orders where REGION='south'\n"
                "```"
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- Rewrite the query below following the style-guide conventions.\n"
                            "-- Keywords: uppercase  |  Column names: lowercase\n"
                            "-- Alias the table with AS (first letter of each word in the name)\n"
                            "-- Each root keyword on its own right-aligned line (the 'river')\n"
                            "-- Spaces around = and after commas; newline before AND/OR\n"
                            "\n"
                            "-- Original (do not submit this):\n"
                            "-- select ORDER_ID, AMOUNT from orders where REGION='south'\n"
                        )
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "mount_path": "orders"}
                ]
            },
            "constraints": {
                "allowed_syntax": STYLE_ALLOWED,
                "blocked_syntax": STYLE_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "query.sql",
                    "content": STYLE_SOLUTION
                }
            ],
            "tests": [
                {
                    "test_id": "t_style_result",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": STYLE_EXPECTED,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return order_id and amount for all orders in the 'south' region "
                        "(6 rows). Check that your WHERE clause filters on region = 'south'."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "Your query returns the right rows and follows the style conventions. "
                    "Consistent formatting makes queries easier to read and review."
                )
            },
            "incorrect": {
                "message": (
                    "Check that your query returns order_id and amount for region = 'south'. "
                    "Also verify: keywords are uppercase, column names lowercase, the table has an AS alias, "
                    "and each root keyword starts its own right-aligned line."
                )
            },
            "hints": [
                "Start with SELECT, then FROM with an alias (FROM orders AS o), then WHERE.",
                "Right-align the keywords so SELECT, FROM, and WHERE all end on the same column — "
                "use leading spaces to push shorter keywords to the right."
            ],
            "remediation_step_id": "tile_sql_style_conventions.s01"
        }
    }
})

tiles.append({
    "tile_id": "tile_sql_style_conventions",
    "interactions": style_interactions
})

# ═══════════════════════════════════════════════════════════════════════════
# TILE: tile_sql_text_dates_casts
# Steps with interactions:
#   s02 (check/choice) — string_functions: apply_lower_and_upper
#   s03 (hands_on/code_exercise) — string_functions practice
#   s05 (check/choice) — date_time_functions: compute_days_between_dates
#   s06 (hands_on/code_exercise) — date_time_functions practice
#   s08 (check/choice) — type_casting: judge_whether_a_cast_is_defined
#   s09 (hands_on/code_exercise) — type_casting practice
# ═══════════════════════════════════════════════════════════════════════════

text_interactions = []

# ── s02: choice — apply_lower_and_upper ──────────────────────────────────────
# Tests f1 (taught in s01 via tb1)
text_interactions.append({
    "step_id": "tile_sql_text_dates_casts.s02",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_text_dates_casts.s02",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.string_functions",
                "capability": "apply_lower_and_upper",
                "fact_ids": ["sql.string_functions#f1"]
            }
        ],
        "anchors": [
            "sql.string_functions#assessment:apply_lower_and_upper"
        ],
        "public": {
            "prompt": (
                "A customer's city is stored as `'LAGOS'`. "
                "Which expression returns `'lagos'`?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "UPPER(city)"},
                {"option_id": "opt_b", "text": "LOWER(city)"},
                {"option_id": "opt_c", "text": "TRIM(city)"},
                {"option_id": "opt_d", "text": "LENGTH(city)"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "UPPER converts a string to all upper case, so UPPER('LAGOS') returns 'LAGOS' — "
                        "unchanged because it is already uppercase."
                    )
                },
                "opt_b": {
                    "message": (
                        "Correct. LOWER converts a string to all lower case, so LOWER('LAGOS') returns 'lagos'."
                    )
                },
                "opt_c": {
                    "message": (
                        "TRIM removes leading and trailing spaces (or other specified characters). "
                        "It does not change the case of letters."
                    )
                },
                "opt_d": {
                    "message": (
                        "LENGTH returns the number of characters in a string — for 'LAGOS' that is 5, "
                        "not the lowercase version."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "LOWER(text) converts every character to lower case. UPPER(text) does the opposite."
            },
            "incorrect": {
                "message": (
                    "Remember: LOWER converts to lower case, UPPER converts to upper case. "
                    "TRIM removes spaces; LENGTH counts characters."
                )
            },
            "hints": [
                "The function name tells you the direction: LOWER → lower case.",
                "TRIM and LENGTH do not change letter case at all."
            ],
            "remediation_step_id": "tile_sql_text_dates_casts.s01"
        }
    }
})

# ── s03: code_exercise — string_functions practice ───────────────────────────
# Tests f2, f3, f4 (taught in s01 via tb1+tb2)
# Practice: clean city column (TRIM + LOWER) and build CONCAT label
text_interactions.append({
    "step_id": "tile_sql_text_dates_casts.s03",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_text_dates_casts.s03",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.string_functions",
                "capability": "apply_trim_to_stray_spaces",
                "fact_ids": ["sql.string_functions#f2"]
            },
            {
                "concept_id": "sql.string_functions",
                "capability": "build_a_label_with_concat_and_length",
                "fact_ids": ["sql.string_functions#f3", "sql.string_functions#f4"]
            }
        ],
        "anchors": [
            "sql.string_functions#practice",
            "sql.string_functions#assessment:apply_trim_to_stray_spaces",
            "sql.string_functions#assessment:build_a_label_with_concat_and_length"
        ],
        "public": {
            "prompt": (
                "The `customers` table has columns `customer_id`, `name`, and `city`. "
                "Some city values may have stray spaces. Write a query that returns:\n\n"
                "- **customer_id** — unchanged\n"
                "- **city_clean** — the city value trimmed of spaces and converted to lower case\n"
                "- **label** — a combined string built with CONCAT in the form `'Name (City)'`, "
                "for example `'Amara Okafor (Lagos)'`\n\n"
                "Return all rows. Name the columns exactly as shown."
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
                            "-- Return: customer_id, city_clean, label\n"
                            "-- city_clean: trim spaces then convert to lower case\n"
                            "-- label: CONCAT(name, ' (', city, ')')\n"
                            "\n"
                        )
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_customers", "mount_path": "customers"}
                ]
            },
            "constraints": {
                "allowed_syntax": STRING_ALLOWED,
                "blocked_syntax": STRING_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "query.sql",
                    "content": STRING_SOLUTION
                }
            ],
            "tests": [
                {
                    "test_id": "t_string_result",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": STRING_EXPECTED,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return customer_id, city_clean (trimmed + lower-cased city), "
                        "and label (CONCAT of name and city) for all 6 customers."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "Your query correctly trims and lower-cases the city column and builds the label "
                    "with CONCAT. Note that CONCAT ignores NULL arguments, so customers with a NULL "
                    "city still get a partial label."
                )
            },
            "incorrect": {
                "message": (
                    "Check that city_clean uses LOWER(TRIM(city)) and that label uses "
                    "CONCAT(name, ' (', city, ')'). Make sure the column aliases match exactly."
                )
            },
            "hints": [
                "Nest TRIM inside LOWER: LOWER(TRIM(city)) trims first, then lower-cases.",
                "CONCAT takes any number of arguments: CONCAT(name, ' (', city, ')') builds the label."
            ],
            "remediation_step_id": "tile_sql_text_dates_casts.s01"
        }
    }
})

# ── s05: choice — compute_days_between_dates ─────────────────────────────────
# Tests f2 (taught in s04 via tb1+tb2)
text_interactions.append({
    "step_id": "tile_sql_text_dates_casts.s05",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_text_dates_casts.s05",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.date_time_functions",
                "capability": "compute_days_between_dates",
                "fact_ids": ["sql.date_time_functions#f2"]
            }
        ],
        "anchors": [
            "sql.date_time_functions#assessment:compute_days_between_dates"
        ],
        "public": {
            "prompt": (
                "Order 1003 has `order_date = '2024-02-03'`. "
                "What does the expression `order_date - DATE '2024-01-01'` return for that row?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "33"},
                {"option_id": "opt_b", "text": "34"},
                {"option_id": "opt_c", "text": "'2024-02-03'"},
                {"option_id": "opt_d", "text": "1"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "Correct. 2024-02-03 minus 2024-01-01 is 33 days: "
                        "31 days in January plus 2 days into February."
                    )
                },
                "opt_b": {
                    "message": (
                        "34 is off by one. Count from Jan 1 to Feb 3: "
                        "January has 31 days, so Jan 1 to Feb 1 is 31 days, plus 2 more days to Feb 3 = 33."
                    )
                },
                "opt_c": {
                    "message": (
                        "date - date produces an integer number of days, not a date string. "
                        "The result is 33, not the original date."
                    )
                },
                "opt_d": {
                    "message": (
                        "1 would be the result if the two dates were one day apart. "
                        "2024-02-03 is 33 days after 2024-01-01."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "date - date subtracts two dates and returns the number of days elapsed. "
                    "2024-02-03 − 2024-01-01 = 33 days."
                )
            },
            "incorrect": {
                "message": (
                    "date - date returns an integer count of days. "
                    "Count the days from 2024-01-01 to 2024-02-03: 31 days in January plus 2 days = 33."
                )
            },
            "hints": [
                "January has 31 days, so 2024-01-01 to 2024-02-01 is 31 days.",
                "date - date always returns an integer, never a date string."
            ],
            "remediation_step_id": "tile_sql_text_dates_casts.s04"
        }
    }
})

# ── s06: code_exercise — date_time_functions practice ────────────────────────
# Tests f1, f2 (taught in s04 via tb1+tb2)
# Practice: pull month from order_date, compute days since a reference date
text_interactions.append({
    "step_id": "tile_sql_text_dates_casts.s06",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_text_dates_casts.s06",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.date_time_functions",
                "capability": "extract_a_date_part",
                "fact_ids": ["sql.date_time_functions#f1"]
            },
            {
                "concept_id": "sql.date_time_functions",
                "capability": "compute_days_between_dates",
                "fact_ids": ["sql.date_time_functions#f2"]
            }
        ],
        "anchors": [
            "sql.date_time_functions#practice",
            "sql.date_time_functions#assessment:extract_a_date_part",
            "sql.date_time_functions#assessment:compute_days_between_dates"
        ],
        "public": {
            "prompt": (
                "The `orders` table has an `order_date` column (type date). "
                "Write a query that returns, for every order:\n\n"
                "- **order_id** — unchanged\n"
                "- **order_month** — the month number extracted from order_date "
                "(use `EXTRACT(MONTH FROM order_date)`)\n"
                "- **days_since_start** — the number of days between `order_date` and "
                "`DATE '2024-01-01'` (use `order_date - DATE '2024-01-01'`)\n\n"
                "Return all rows. Name the columns exactly as shown."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- orders columns: order_id, customer_id, delivery_time_minutes,\n"
                            "--                 order_date, region, amount, city\n"
                            "-- Return: order_id, order_month, days_since_start\n"
                            "-- order_month: EXTRACT(MONTH FROM order_date)\n"
                            "-- days_since_start: order_date - DATE '2024-01-01'\n"
                            "\n"
                        )
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "mount_path": "orders"}
                ]
            },
            "constraints": {
                "allowed_syntax": DATE_ALLOWED,
                "blocked_syntax": DATE_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "query.sql",
                    "content": DATE_SOLUTION
                }
            ],
            "tests": [
                {
                    "test_id": "t_date_result",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": DATE_EXPECTED,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return order_id, order_month (1–7), and days_since_start "
                        "for all 13 orders. Check that you use EXTRACT(MONTH FROM order_date) and "
                        "order_date - DATE '2024-01-01'."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "Your query correctly extracts the month with EXTRACT and computes the day count "
                    "with date subtraction. Both operations return integers."
                )
            },
            "incorrect": {
                "message": (
                    "Check that order_month uses EXTRACT(MONTH FROM order_date) and that "
                    "days_since_start uses order_date - DATE '2024-01-01'. "
                    "Make sure the column aliases match exactly."
                )
            },
            "hints": [
                "EXTRACT syntax: EXTRACT(MONTH FROM column_name) — the field name goes before FROM.",
                "Date subtraction: order_date - DATE '2024-01-01' returns an integer number of days."
            ],
            "remediation_step_id": "tile_sql_text_dates_casts.s04"
        }
    }
})

# ── s08: choice — judge_whether_a_cast_is_defined ────────────────────────────
# Tests f2 (taught in s07 via tb1+tb2)
text_interactions.append({
    "step_id": "tile_sql_text_dates_casts.s08",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_text_dates_casts.s08",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.type_casting",
                "capability": "judge_whether_a_cast_is_defined",
                "fact_ids": ["sql.type_casting#f2"]
            }
        ],
        "anchors": [
            "sql.type_casting#assessment:judge_whether_a_cast_is_defined"
        ],
        "public": {
            "prompt": (
                "Which of these casts is **not** guaranteed to succeed because no suitable "
                "type conversion is defined between the value's type and the target type?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "CAST(42 AS TEXT)"},
                {"option_id": "opt_b", "text": "CAST('2024-01-05' AS DATE)"},
                {"option_id": "opt_c", "text": "CAST('Lagos' AS INTEGER)"},
                {"option_id": "opt_d", "text": "CAST(3.14 AS INTEGER)"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_c"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "CAST(42 AS TEXT) succeeds: a defined conversion exists from integer to text, "
                        "producing '42'."
                    )
                },
                "opt_b": {
                    "message": (
                        "CAST('2024-01-05' AS DATE) succeeds: a defined conversion exists from a "
                        "date-formatted text string to the date type."
                    )
                },
                "opt_c": {
                    "message": (
                        "Correct. 'Lagos' is a text string that does not represent a number, so no "
                        "suitable conversion to INTEGER is defined — this cast will fail at runtime."
                    )
                },
                "opt_d": {
                    "message": (
                        "CAST(3.14 AS INTEGER) succeeds: a defined conversion exists from numeric to "
                        "integer (the decimal part is truncated, giving 3)."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "A cast succeeds only if a suitable type conversion is defined. "
                    "Text that does not represent a number cannot be cast to INTEGER."
                )
            },
            "incorrect": {
                "message": (
                    "A cast succeeds only when a suitable conversion is defined between the source "
                    "type and the target type. Think about whether the value can actually be "
                    "interpreted as the target type."
                )
            },
            "hints": [
                "Ask: can this value be meaningfully interpreted as the target type?",
                "Numbers can be cast to text; text that looks like a number can be cast to a number. "
                "Text that does not look like a number cannot."
            ],
            "remediation_step_id": "tile_sql_text_dates_casts.s07"
        }
    }
})

# ── s09: code_exercise — type_casting practice ───────────────────────────────
# Tests f1 (taught in s07 via tb1+tb2)
# Practice: convert amount to text using CAST and :: — two queries
text_interactions.append({
    "step_id": "tile_sql_text_dates_casts.s09",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_text_dates_casts.s09",
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.type_casting",
                "capability": "write_a_cast_in_both_syntaxes",
                "fact_ids": ["sql.type_casting#f1"]
            }
        ],
        "anchors": [
            "sql.type_casting#practice",
            "sql.type_casting#assessment:write_a_cast_in_both_syntaxes"
        ],
        "public": {
            "prompt": (
                "The `orders` table has an `amount` column (numeric). "
                "Write **two** SELECT statements in the same file:\n\n"
                "1. Use `CAST(amount AS TEXT)` to convert amount to text, aliased as **amount_text**. "
                "Also return **order_id**.\n"
                "2. Use the `::` shorthand (`amount::TEXT`) to do the same conversion, "
                "aliased as **amount_text**. Also return **order_id**.\n\n"
                "Both statements should return all rows with columns **order_id** and **amount_text** "
                "in that order. Separate the two statements with a semicolon."
            ),
            "runtime": {"kind": "sql", "version": "1.32.0"},
            "workspace": {
                "files": [
                    {
                        "path": "query.sql",
                        "role": "editable",
                        "language": "sql",
                        "content": (
                            "-- orders columns: order_id, customer_id, delivery_time_minutes,\n"
                            "--                 order_date, region, amount, city\n"
                            "-- Statement 1: use CAST(amount AS TEXT) aliased as amount_text\n"
                            "-- Statement 2: use amount::TEXT aliased as amount_text\n"
                            "-- Both return order_id and amount_text for all rows.\n"
                            "\n"
                        )
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "mount_path": "orders"}
                ]
            },
            "constraints": {
                "allowed_syntax": CAST_ALLOWED,
                "blocked_syntax": CAST_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "query.sql",
                    "content": CAST_SOLUTION
                }
            ],
            "tests": [
                {
                    "test_id": "t_cast_stmt0",
                    "kind": "query_result_equals",
                    "spec": {
                        "statement": 0,
                        "expected": CAST_EXPECTED_0,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Statement 1 (CAST syntax) should return order_id and amount_text for all 13 orders. "
                        "Check that you use CAST(amount AS TEXT) AS amount_text."
                    )
                },
                {
                    "test_id": "t_cast_stmt1",
                    "kind": "query_result_equals",
                    "spec": {
                        "statement": 1,
                        "expected": CAST_EXPECTED_1,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Statement 2 (:: syntax) should return order_id and amount_text for all 13 orders. "
                        "Check that you use amount::TEXT AS amount_text."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "Both syntaxes produce identical results. "
                    "CAST(expression AS type) is the SQL standard; expression::type is a PostgreSQL shorthand."
                )
            },
            "incorrect": {
                "message": (
                    "Make sure you have two separate SELECT statements separated by a semicolon. "
                    "Statement 1 must use CAST(amount AS TEXT) and statement 2 must use amount::TEXT. "
                    "Both should alias the result as amount_text."
                )
            },
            "hints": [
                "Write the first SELECT, end it with a semicolon, then write the second SELECT.",
                "Both syntaxes: CAST(amount AS TEXT) and amount::TEXT — the :: is a shorthand for CAST."
            ],
            "remediation_step_id": "tile_sql_text_dates_casts.s07"
        }
    }
})

tiles.append({
    "tile_id": "tile_sql_text_dates_casts",
    "interactions": text_interactions
})

# ═══════════════════════════════════════════════════════════════════════════
# TILE: tile_sql_null_fallback_and_union
# Steps with interactions:
#   s02 (check/choice) — coalesce: predict_coalesce_result
#   s03 (check/choice) — coalesce: substitute_a_default_for_null
#   s04 (hands_on/code_exercise) — coalesce practice
#   s07 (check/choice) — union: check_union_compatibility
#   s08 (hands_on/code_exercise) — union practice
# ═══════════════════════════════════════════════════════════════════════════

null_interactions = []

# ── s02: choice — predict_coalesce_result ────────────────────────────────────
# Tests f1 (taught in s01 via tb1+tb2)
null_interactions.append({
    "step_id": "tile_sql_null_fallback_and_union.s02",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_null_fallback_and_union.s02",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.coalesce",
                "capability": "predict_coalesce_result",
                "fact_ids": ["sql.coalesce#f1"]
            }
        ],
        "anchors": [
            "sql.coalesce#assessment:predict_coalesce_result"
        ],
        "public": {
            "prompt": (
                "What does `COALESCE(NULL, NULL, 'Abuja')` return?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "NULL"},
                {"option_id": "opt_b", "text": "'Abuja'"},
                {"option_id": "opt_c", "text": "0"},
                {"option_id": "opt_d", "text": "An error"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "COALESCE returns NULL only when *every* argument is NULL. "
                        "Here the third argument is 'Abuja', so COALESCE returns 'Abuja'."
                    )
                },
                "opt_b": {
                    "message": (
                        "Correct. COALESCE returns the first non-null argument. "
                        "The first two are NULL, so it skips them and returns 'Abuja'."
                    )
                },
                "opt_c": {
                    "message": (
                        "COALESCE does not return 0 unless 0 is one of its arguments. "
                        "It returns the first non-null argument, which is 'Abuja'."
                    )
                },
                "opt_d": {
                    "message": (
                        "COALESCE does not raise an error when some arguments are NULL — "
                        "that is exactly what it is designed to handle. It returns 'Abuja'."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "COALESCE scans its arguments left to right and returns the first one that is not NULL. "
                    "It returns NULL only when every argument is NULL."
                )
            },
            "incorrect": {
                "message": (
                    "COALESCE(value [, ...]) returns the first non-null argument. "
                    "It skips NULL arguments and returns the first non-null one it finds."
                )
            },
            "hints": [
                "COALESCE reads its arguments from left to right and stops at the first non-null value.",
                "It only returns NULL if every single argument is NULL."
            ],
            "remediation_step_id": "tile_sql_null_fallback_and_union.s01"
        }
    }
})

# ── s03: choice — substitute_a_default_for_null ──────────────────────────────
# Tests f2 (taught in s01 via tb1+tb2)
null_interactions.append({
    "step_id": "tile_sql_null_fallback_and_union.s03",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_null_fallback_and_union.s03",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.coalesce",
                "capability": "substitute_a_default_for_null",
                "fact_ids": ["sql.coalesce#f2"]
            }
        ],
        "anchors": [
            "sql.coalesce#assessment:substitute_a_default_for_null"
        ],
        "public": {
            "prompt": (
                "Customer 5 has `name = NULL` and `city = NULL`. "
                "Which expression returns `'(none)'` for that customer's city?"
            ),
            "options": [
                {"option_id": "opt_a", "text": "COALESCE(city)"},
                {"option_id": "opt_b", "text": "COALESCE(city, '(none)')"},
                {"option_id": "opt_c", "text": "COALESCE('(none)', city)"},
                {"option_id": "opt_d", "text": "COALESCE(NULL, city)"}
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "COALESCE(city) with only one argument returns city itself — NULL for customer 5. "
                        "You need to provide the fallback value as a second argument."
                    )
                },
                "opt_b": {
                    "message": (
                        "Correct. COALESCE(city, '(none)') returns city when it is not NULL, "
                        "and '(none)' when city is NULL — exactly the substitution pattern."
                    )
                },
                "opt_c": {
                    "message": (
                        "COALESCE('(none)', city) always returns '(none)' because '(none)' is the "
                        "first argument and it is never NULL. The arguments must be in the right order: "
                        "the column first, the fallback second."
                    )
                },
                "opt_d": {
                    "message": (
                        "COALESCE(NULL, city) skips the literal NULL and returns city — which is also "
                        "NULL for customer 5, so the result is still NULL, not '(none)'."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "COALESCE(city, '(none)') is the standard pattern: put the column first and the "
                    "default value second. When city is NULL, COALESCE returns the default."
                )
            },
            "incorrect": {
                "message": (
                    "The order of arguments matters. COALESCE returns the first non-null argument, "
                    "so the column must come first and the fallback default must come after it."
                )
            },
            "hints": [
                "The column you want to check goes first; the fallback value goes after it.",
                "If the fallback is listed first, COALESCE always returns it — even when the column is not NULL."
            ],
            "remediation_step_id": "tile_sql_null_fallback_and_union.s01"
        }
    }
})

# ── s04: code_exercise — coalesce practice ───────────────────────────────────
# Tests f1, f2 (taught in s01 via tb1+tb2)
# Practice: replace missing city with 'Unknown'
null_interactions.append({
    "step_id": "tile_sql_null_fallback_and_union.s04",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_null_fallback_and_union.s04",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.coalesce",
                "capability": "predict_coalesce_result",
                "fact_ids": ["sql.coalesce#f1"]
            },
            {
                "concept_id": "sql.coalesce",
                "capability": "substitute_a_default_for_null",
                "fact_ids": ["sql.coalesce#f2"]
            }
        ],
        "anchors": [
            "sql.coalesce#practice"
        ],
        "public": {
            "prompt": (
                "The `customers` table has columns `customer_id`, `name`, and `city`. "
                "Customers 4 and 5 have a NULL city. "
                "Write a query that returns all three columns for every customer, "
                "but replaces any NULL city with the string `'Unknown'`. "
                "Name the city column **city** in the output.\n\n"
                "Return all rows."
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
                            "-- Return: customer_id, name, city\n"
                            "-- Replace NULL city with 'Unknown' using COALESCE\n"
                            "\n"
                        )
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_customers", "mount_path": "customers"}
                ]
            },
            "constraints": {
                "allowed_syntax": COALESCE_ALLOWED,
                "blocked_syntax": COALESCE_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "query.sql",
                    "content": COALESCE_SOLUTION
                }
            ],
            "tests": [
                {
                    "test_id": "t_coalesce_result",
                    "kind": "query_result_equals",
                    "spec": {
                        "expected": COALESCE_EXPECTED,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Your query should return 6 rows with customer_id, name, and city. "
                        "Customers 4 and 5 should show 'Unknown' for city instead of NULL."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "Your query correctly substitutes 'Unknown' for NULL city values using COALESCE. "
                    "Customers with a city keep their original value; customers 4 and 5 get 'Unknown'."
                )
            },
            "incorrect": {
                "message": (
                    "Use COALESCE(city, 'Unknown') AS city to replace NULL city values. "
                    "Make sure you return all three columns and all 6 rows."
                )
            },
            "hints": [
                "COALESCE(city, 'Unknown') returns city when it is not NULL, and 'Unknown' when it is.",
                "Alias the expression AS city so the output column is named city."
            ],
            "remediation_step_id": "tile_sql_null_fallback_and_union.s01"
        }
    }
})

# ── s07: choice — check_union_compatibility ──────────────────────────────────
# Tests f3 (taught in s06 via tb3)
null_interactions.append({
    "step_id": "tile_sql_null_fallback_and_union.s07",
    "interaction": {
        "type": "choice",
        "interaction_id": "ix.tile_sql_null_fallback_and_union.s07",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.union",
                "capability": "check_union_compatibility",
                "fact_ids": ["sql.union#f3"]
            }
        ],
        "anchors": [
            "sql.union#assessment:check_union_compatibility"
        ],
        "public": {
            "prompt": (
                "Which pair of queries **cannot** be combined with UNION because they are not compatible?"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": (
                        "SELECT customer_id FROM customers\n"
                        "UNION\n"
                        "SELECT customer_id FROM orders"
                    )
                },
                {
                    "option_id": "opt_b",
                    "text": (
                        "SELECT customer_id FROM customers\n"
                        "UNION\n"
                        "SELECT order_id, amount FROM orders"
                    )
                },
                {
                    "option_id": "opt_c",
                    "text": (
                        "SELECT customer_id FROM customers\n"
                        "UNION\n"
                        "SELECT customer_id FROM orders WHERE region = 'south'"
                    )
                },
                {
                    "option_id": "opt_d",
                    "text": (
                        "SELECT order_id FROM orders WHERE amount > 5000\n"
                        "UNION\n"
                        "SELECT order_id FROM orders WHERE region = 'north'"
                    )
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_b"],
            "option_feedback": {
                "opt_a": {
                    "message": (
                        "Both queries return exactly one integer column (customer_id), so they are "
                        "compatible and can be combined with UNION."
                    )
                },
                "opt_b": {
                    "message": (
                        "Correct. The first query returns one column (customer_id) and the second "
                        "returns two columns (order_id, amount). UNION requires the same number of "
                        "columns with compatible types."
                    )
                },
                "opt_c": {
                    "message": (
                        "Both queries return exactly one integer column (customer_id), so they are "
                        "compatible. The WHERE clause on the second query does not affect compatibility."
                    )
                },
                "opt_d": {
                    "message": (
                        "Both queries return exactly one integer column (order_id), so they are "
                        "compatible and can be combined with UNION."
                    )
                }
            }
        },
        "feedback": {
            "correct": {
                "message": (
                    "UNION requires both queries to return the same number of columns with compatible "
                    "data types. A one-column query cannot be combined with a two-column query."
                )
            },
            "incorrect": {
                "message": (
                    "Check the number of columns each query returns. UNION requires both queries to "
                    "return the same number of columns, with corresponding columns having compatible types."
                )
            },
            "hints": [
                "Count the columns in each SELECT list — they must match.",
                "A WHERE clause does not affect compatibility; only the SELECT list matters."
            ],
            "remediation_step_id": "tile_sql_null_fallback_and_union.s06"
        }
    }
})

# ── s08: code_exercise — union practice ──────────────────────────────────────
# Tests f1, f2 (taught in s05 via tb1+tb2)
# Practice: UNION and UNION ALL of two compatible queries
null_interactions.append({
    "step_id": "tile_sql_null_fallback_and_union.s08",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": "ix.tile_sql_null_fallback_and_union.s08",
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "sql.union",
                "capability": "describe_how_union_combines_results",
                "fact_ids": ["sql.union#f1"]
            },
            {
                "concept_id": "sql.union",
                "capability": "choose_union_or_union_all",
                "fact_ids": ["sql.union#f2"]
            }
        ],
        "anchors": [
            "sql.union#practice",
            "sql.union#assessment:describe_how_union_combines_results",
            "sql.union#assessment:choose_union_or_union_all"
        ],
        "public": {
            "prompt": (
                "Write **two** SELECT statements in the same file:\n\n"
                "1. Use **UNION** to combine the `customer_id` of customers whose city is `'Lagos'` "
                "(from the `customers` table) with the `customer_id` of orders in the `'south'` region "
                "(from the `orders` table). Return the column as **customer_id**.\n\n"
                "2. Repeat the same combination using **UNION ALL** instead of UNION.\n\n"
                "Separate the two statements with a semicolon. "
                "The UNION result should have fewer rows than the UNION ALL result because duplicates exist."
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
                            "-- orders columns: order_id, customer_id, delivery_time_minutes,\n"
                            "--                 order_date, region, amount, city\n"
                            "-- Statement 1: UNION of customer_id from customers (city='Lagos')\n"
                            "--              and customer_id from orders (region='south')\n"
                            "-- Statement 2: same combination with UNION ALL\n"
                            "\n"
                        )
                    }
                ],
                "entry": "query.sql",
                "asset_mounts": [
                    {"asset_id": "ds_orders", "mount_path": "orders"},
                    {"asset_id": "ds_customers", "mount_path": "customers"}
                ]
            },
            "constraints": {
                "allowed_syntax": UNION_ALLOWED,
                "blocked_syntax": UNION_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "query.sql",
                    "content": UNION_SOLUTION
                }
            ],
            "tests": [
                {
                    "test_id": "t_union_stmt0",
                    "kind": "query_result_equals",
                    "spec": {
                        "statement": 0,
                        "expected": UNION_EXPECTED_0,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Statement 1 (UNION) should return 1 distinct customer_id. "
                        "Check that you use UNION (not UNION ALL) and that both SELECT lists "
                        "return exactly one column named customer_id."
                    )
                },
                {
                    "test_id": "t_union_stmt1",
                    "kind": "query_result_equals",
                    "spec": {
                        "statement": 1,
                        "expected": UNION_EXPECTED_1,
                        "ordered": False
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Statement 2 (UNION ALL) should return 7 rows (1 from customers + 6 from orders). "
                        "Check that you use UNION ALL and the same two SELECT queries as statement 1."
                    )
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": (
                    "UNION deduplicates: customer 1 appears in both queries but only once in the result. "
                    "UNION ALL keeps every row: 1 from customers plus 6 from orders = 7 rows."
                )
            },
            "incorrect": {
                "message": (
                    "Make sure you have two statements separated by a semicolon. "
                    "Statement 1 uses UNION; statement 2 uses UNION ALL. "
                    "Both SELECT lists must return exactly one column (customer_id)."
                )
            },
            "hints": [
                "Both SELECT lists must return the same column: customer_id. "
                "Filter customers by city = 'Lagos' and orders by region = 'south'.",
                "UNION removes duplicates; UNION ALL keeps every row including duplicates."
            ],
            "remediation_step_id": "tile_sql_null_fallback_and_union.s05"
        }
    }
})

tiles.append({
    "tile_id": "tile_sql_null_fallback_and_union",
    "interactions": null_interactions
})

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_006_da_sql_rest",
    "tiles": tiles
}

out_path = 'batches/final_batch_006_da_sql_rest/interactions.part.c2.json'
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nWrote {out_path}")
total = sum(len(t['interactions']) for t in tiles)
print(f"Total interactions: {total}")
for t in tiles:
    print(f"  {t['tile_id']}: {len(t['interactions'])} interactions")
