"""
Generate screens.part.c2.json for tiles:
  tile_sql_style_conventions
  tile_sql_text_dates_casts
  tile_sql_null_fallback_and_union
"""
import json

# ── helpers ──────────────────────────────────────────────────────────────────

def prose(block_id, text, role, concept_ids, fact_ids, tb_ids=None, anchors=None):
    lin = {"concept_ids": concept_ids, "fact_ids": fact_ids}
    if tb_ids:
        lin["teaching_block_ids"] = tb_ids
    if anchors:
        lin["anchors"] = anchors
    return {"type": "prose", "block_id": block_id, "text": text, "role": role, "lineage": lin}

def heading(block_id, text, level=3):
    return {"type": "heading", "block_id": block_id, "text": text, "level": level}

def up_next(block_id, title, text):
    return {"type": "up_next", "block_id": block_id, "title": title, "text": text}

def step_lineage(concept_ids, fact_ids, tb_ids=None, anchors=None, segment_ids=None):
    lin = {"concept_ids": concept_ids, "fact_ids": fact_ids}
    if tb_ids:
        lin["teaching_block_ids"] = tb_ids
    if anchors:
        lin["anchors"] = anchors
    if segment_ids:
        lin["segment_ids"] = segment_ids
    return lin

def check_step(step_id, concept_ids, title, eyebrow, lede, fact_ids, anchors):
    return {
        "step_id": step_id,
        "type": "check",
        "concept_ids": concept_ids,
        "title": title,
        "eyebrow": eyebrow,
        "lede": lede,
        "reward": {"gems": 5, "first_try_bonus": 3},
        "lineage": step_lineage(concept_ids, fact_ids, anchors=anchors),
    }

def hands_on_step(step_id, concept_ids, title, eyebrow, lede, fact_ids, anchors):
    return {
        "step_id": step_id,
        "type": "hands_on",
        "concept_ids": concept_ids,
        "title": title,
        "eyebrow": eyebrow,
        "lede": lede,
        "reward": {"gems": 10, "first_try_bonus": 5},
        "lineage": step_lineage(concept_ids, fact_ids, anchors=anchors),
    }

def remediation_step(step_id, concept_ids, title, eyebrow, lede, blocks, fact_ids, tb_ids):
    return {
        "step_id": step_id,
        "type": "remediation",
        "concept_ids": concept_ids,
        "title": title,
        "eyebrow": eyebrow,
        "lede": lede,
        "blocks": blocks,
        "lineage": step_lineage(concept_ids, fact_ids, tb_ids=tb_ids),
    }

# ═══════════════════════════════════════════════════════════════════════════
# TILE 1: tile_sql_style_conventions
# Steps: s01 (explainer), s02 (check), s03 (hands_on), s04 (recap)
# Concepts: sql.style_conventions (f1-f5)
# ═══════════════════════════════════════════════════════════════════════════

T1 = "tile_sql_style_conventions"
C1 = ["sql.style_conventions"]

# s01 — explainer — before_after visual — budget 175
# Plan: tb1 (f1,f2), tb2 (f3,f4,f5), visual=before_after
s01_prose1 = prose(
    f"{T1}.s01.p1",
    "Reserved keywords — SELECT, FROM, WHERE, AND, OR — should always be written in uppercase. "
    "Column names should always be written in lowercase, except where it makes sense not to, such as proper nouns. "
    "So SELECT customer_id, city FROM customers WHERE city = 'Lagos' follows the convention; "
    "a mix like select Customer_ID from Customers where City = 'Lagos' does not.",
    "definition",
    C1,
    ["sql.style_conventions#f1", "sql.style_conventions#f2"],
    tb_ids=["sql.style_conventions#tb1"],
)

s01_prose2 = prose(
    f"{T1}.s01.p2",
    "An alias name should relate to the object it aliases — as a rule of thumb, the first letter of each word in the object's name — "
    "and the AS keyword should always be included: FROM orders AS o, not FROM orders o or FROM orders AS x. "
    "Each root keyword starts a new line and is right-aligned so all keywords end on the same character boundary (a 'river'). "
    "Values sit left-aligned after them; spaces go around '=' and after commas; "
    "a newline comes before AND or OR so each condition starts its own line.",
    "syntax",
    C1,
    ["sql.style_conventions#f3", "sql.style_conventions#f4", "sql.style_conventions#f5"],
    tb_ids=["sql.style_conventions#tb2"],
)

# before_after: messy query vs. formatted query (code_walkthrough panels)
s01_before = {
    "type": "code_walkthrough",
    "block_id": f"{T1}.s01.cw_before",
    "language": "sql",
    "code": "select customer_id,city from customers where city='Lagos' and customer_id>1",
    "annotations": [
        {"start_line": 1, "end_line": 1,
         "text": "Keywords lowercase, column names mixed-case, no line breaks, no spaces around operators"}
    ],
    "reveal": "all",
}

s01_after = {
    "type": "code_walkthrough",
    "block_id": f"{T1}.s01.cw_after",
    "language": "sql",
    "code": "  SELECT customer_id, city\n    FROM customers\n   WHERE city = 'Lagos'\n     AND customer_id > 1",
    "annotations": [
        {"start_line": 1, "end_line": 1, "text": "Keywords uppercase; column names lowercase"},
        {"start_line": 2, "end_line": 2, "text": "FROM starts a new line, right-aligned to the 'river'"},
        {"start_line": 3, "end_line": 3, "text": "WHERE starts a new line; spaces around '='"},
        {"start_line": 4, "end_line": 4, "text": "AND on its own line, right-aligned"},
    ],
    "reveal": "all",
}

s01_ba = {
    "type": "before_after",
    "block_id": f"{T1}.s01.ba",
    "before": s01_before,
    "after": s01_after,
    "change_summary": "The same query reformatted: keywords uppercased, columns lowercased, alias added with AS, each clause on its own right-aligned line, spaces around operators.",
    "lineage": {
        "concept_ids": C1,
        "fact_ids": [
            "sql.style_conventions#f1",
            "sql.style_conventions#f2",
            "sql.style_conventions#f3",
            "sql.style_conventions#f4",
            "sql.style_conventions#f5",
        ],
        "teaching_block_ids": ["sql.style_conventions#tb1", "sql.style_conventions#tb2"],
        "anchors": ["sql.style_conventions#visual"],
    },
}

step_s01 = {
    "step_id": f"{T1}.s01",
    "type": "explainer",
    "concept_ids": C1,
    "title": "SQL style conventions",
    "eyebrow": "Style guide",
    "lede": "Consistent formatting makes queries easier to read, review, and debug.",
    "blocks": [s01_prose1, s01_prose2, s01_ba],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C1,
        ["sql.style_conventions#f1", "sql.style_conventions#f2",
         "sql.style_conventions#f3", "sql.style_conventions#f4", "sql.style_conventions#f5"],
        tb_ids=["sql.style_conventions#tb1", "sql.style_conventions#tb2"],
        anchors=["sql.style_conventions#visual"],
    ),
}

# s02 — check — f4, f5 — lay_out_a_query_with_line_breaks_and_spacing
step_s02 = check_step(
    f"{T1}.s02",
    C1,
    "Line breaks and the keyword 'river'",
    "Quick check",
    "Pick the correctly formatted version of a two-condition WHERE clause.",
    ["sql.style_conventions#f4", "sql.style_conventions#f5"],
    ["sql.style_conventions#assessment:lay_out_a_query_with_line_breaks_and_spacing"],
)

# s03 — hands_on — f1-f5 — practice + assessments
step_s03 = hands_on_step(
    f"{T1}.s03",
    C1,
    "Reformat a query to follow the style guide",
    "Practice",
    "Rewrite the given query so keywords are uppercase, columns lowercase, aliases use AS, and each clause starts its own right-aligned line.",
    ["sql.style_conventions#f1", "sql.style_conventions#f2",
     "sql.style_conventions#f3", "sql.style_conventions#f4", "sql.style_conventions#f5"],
    [
        "sql.style_conventions#practice",
        "sql.style_conventions#assessment:apply_keyword_and_column_case",
        "sql.style_conventions#assessment:write_a_conventional_alias",
        "sql.style_conventions#assessment:lay_out_a_query_with_line_breaks_and_spacing",
    ],
)

# s04 — recap — up_next → tile_sql_text_dates_casts
s04_prose = prose(
    f"{T1}.s04.p1",
    "Write reserved keywords in uppercase and column names in lowercase. "
    "Alias with AS and choose a name derived from the object — FROM orders AS o. "
    "Right-align root keywords to form a 'river', put each clause on its own line, "
    "and place a newline before AND or OR so every condition is easy to scan.",
    "takeaway",
    C1,
    ["sql.style_conventions#f1", "sql.style_conventions#f2",
     "sql.style_conventions#f3", "sql.style_conventions#f4", "sql.style_conventions#f5"],
    tb_ids=["sql.style_conventions#tb1", "sql.style_conventions#tb2"],
)

s04_un = up_next(
    f"{T1}.s04.un",
    "Next: Text and Date Functions",
    "Now that your queries are consistently formatted, you will learn to transform the values inside them — "
    "cleaning city names with LOWER and TRIM, building labels with CONCAT, and pulling date parts with EXTRACT.",
)

step_s04 = {
    "step_id": f"{T1}.s04",
    "type": "recap",
    "concept_ids": C1,
    "title": "Recap: SQL Style Conventions",
    "eyebrow": "Recap",
    "lede": "Five rules that keep every query readable at a glance.",
    "blocks": [s04_prose, s04_un],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C1,
        ["sql.style_conventions#f1", "sql.style_conventions#f2",
         "sql.style_conventions#f3", "sql.style_conventions#f4", "sql.style_conventions#f5"],
        tb_ids=["sql.style_conventions#tb1", "sql.style_conventions#tb2"],
    ),
}

# ── remediation steps for tile_sql_style_conventions ──────────────────────
# s02 measures f4, f5 → r01 re-teaches f4, f5
r01_blocks = [
    prose(
        f"{T1}.r01.p1",
        "Each root keyword — SELECT, FROM, WHERE — starts its own line and is right-aligned so all keywords end on the same character boundary, "
        "forming a vertical 'river'. Values sit left-aligned after them on the same line. "
        "Spaces go before and after '=' and after every comma. "
        "A newline always comes before AND or OR so each condition starts its own line: "
        "WHERE city = 'Lagos' / AND customer_id > 1, not WHERE city = 'Lagos' AND customer_id > 1 on one line.",
        "syntax",
        C1,
        ["sql.style_conventions#f4", "sql.style_conventions#f5"],
        tb_ids=["sql.style_conventions#tb2"],
    )
]
rem_r01 = remediation_step(
    f"{T1}.r01",
    C1,
    "The keyword 'river' and line-break rules",
    "Let's review",
    "Right-align keywords to form a 'river'; put each clause and each AND/OR condition on its own line.",
    r01_blocks,
    ["sql.style_conventions#f4", "sql.style_conventions#f5"],
    ["sql.style_conventions#tb2"],
)

# s03 measures f1-f5 — add r02 for f1/f2 (case rules) and r03 for f3 (aliasing)
r02_blocks = [
    prose(
        f"{T1}.r02.p1",
        "Reserved keywords — SELECT, FROM, WHERE, AND, OR, AS, GROUP BY, ORDER BY — should always be uppercase. "
        "Column names should always be lowercase, except proper nouns. "
        "SELECT customer_id, city FROM customers WHERE city = 'Lagos' is correct; "
        "select Customer_ID from Customers where City = 'Lagos' breaks both rules.",
        "definition",
        C1,
        ["sql.style_conventions#f1", "sql.style_conventions#f2"],
        tb_ids=["sql.style_conventions#tb1"],
    )
]
rem_r02 = remediation_step(
    f"{T1}.r02",
    C1,
    "Keyword and column casing",
    "Let's review",
    "Keywords uppercase, column names lowercase — every time.",
    r02_blocks,
    ["sql.style_conventions#f1", "sql.style_conventions#f2"],
    ["sql.style_conventions#tb1"],
)

r03_blocks = [
    prose(
        f"{T1}.r03.p1",
        "An alias name should relate to the object it aliases. "
        "As a rule of thumb, use the first letter of each word in the object's name: "
        "orders → o, order_items → oi, customers → c. "
        "Always include the AS keyword to make the alias explicit: "
        "FROM orders AS o, not FROM orders o or FROM orders AS x.",
        "definition",
        C1,
        ["sql.style_conventions#f3"],
        tb_ids=["sql.style_conventions#tb2"],
    )
]
rem_r03 = remediation_step(
    f"{T1}.r03",
    C1,
    "Writing a conventional alias",
    "Let's review",
    "Use AS and choose an alias name derived from the object's name.",
    r03_blocks,
    ["sql.style_conventions#f3"],
    ["sql.style_conventions#tb2"],
)

tile1 = {
    "tile_id": T1,
    "title": "SQL Style Conventions",
    "summary": "Format SQL queries consistently: uppercase keywords, lowercase columns, meaningful aliases with AS, right-aligned keyword 'river', and one clause per line.",
    "steps": [step_s01, step_s02, step_s03, step_s04],
    "remediation_steps": [rem_r01, rem_r02, rem_r03],
}

# ═══════════════════════════════════════════════════════════════════════════
# TILE 2: tile_sql_text_dates_casts
# Steps: s01-s10
# Concepts: sql.string_functions, sql.date_time_functions, sql.type_casting
# ═══════════════════════════════════════════════════════════════════════════

T2 = "tile_sql_text_dates_casts"
C_STR = ["sql.string_functions"]
C_DT  = ["sql.date_time_functions"]
C_TC  = ["sql.type_casting"]
C_ALL = ["sql.string_functions", "sql.date_time_functions", "sql.type_casting"]

# ── s01 explainer: string_functions — before_after — budget 108 ──────────
# Plan: tb1 (f1), tb2 (f2,f3,f4), visual=before_after
# Visual purpose: messy city values → cleaned forms after TRIM and LOWER/UPPER

s01_t2_prose1 = prose(
    f"{T2}.s01.p1",
    "LOWER(text) converts a string to all lower case; UPPER(text) converts it to all upper case. "
    "LOWER(city) turns 'LAGOS' or 'Lagos' into 'lagos', which is useful for comparing city names that were entered inconsistently.",
    "definition",
    C_STR,
    ["sql.string_functions#f1"],
    tb_ids=["sql.string_functions#tb1"],
)

s01_t2_prose2 = prose(
    f"{T2}.s01.p2",
    "TRIM removes leading or trailing spaces (by default) from a string — TRIM(city) strips accidental spaces from a city value. "
    "CONCAT joins its arguments into one string and ignores any NULL arguments: CONCAT(name, ' (', city, ')') builds a single label. "
    "LENGTH(text) returns the number of characters: LENGTH(name) gives the character count of a customer's name.",
    "syntax",
    C_STR,
    ["sql.string_functions#f2", "sql.string_functions#f3", "sql.string_functions#f4"],
    tb_ids=["sql.string_functions#tb2"],
)

# before_after: messy city column → cleaned city column
# "before" shows ds_customers_messy city column (has 'kano' lowercase and NULL)
# "after" shows result of LOWER(TRIM(city)) — this is a query output
s01_t2_before = {
    "type": "data_table",
    "block_id": f"{T2}.s01.dt_before",
    "asset_ref": {
        "asset_id": "ds_customers",
        "variant_id": "ds_customers_messy",
        "columns": ["customer_id", "name", "city"],
        "max_rows": 6,
    },
    "caption": "Raw city values — inconsistent casing and stray spaces",
    "tag_columns": [
        {"column": "city", "tag": "raw text", "tone": "bad"},
    ],
}

s01_t2_after = {
    "type": "data_table",
    "block_id": f"{T2}.s01.dt_after",
    "result_of": {
        "runtime": "sql",
        "sql": "SELECT customer_id, name, LOWER(TRIM(city)) AS city FROM customers",
        "asset_mounts": [
            {"asset_id": "ds_customers", "variant_id": "ds_customers_messy", "mount_path": "customers"}
        ],
    },
    "caption": "After LOWER(TRIM(city)) — consistent lowercase, spaces removed",
}

s01_t2_ba = {
    "type": "before_after",
    "block_id": f"{T2}.s01.ba",
    "before": s01_t2_before,
    "after": s01_t2_after,
    "change_summary": "LOWER(TRIM(city)) standardises city values to lowercase and removes stray spaces.",
    "lineage": {
        "concept_ids": C_STR,
        "fact_ids": ["sql.string_functions#f1", "sql.string_functions#f2"],
        "teaching_block_ids": ["sql.string_functions#tb1", "sql.string_functions#tb2"],
        "anchors": ["sql.string_functions#visual"],
    },
}

step_t2_s01 = {
    "step_id": f"{T2}.s01",
    "type": "explainer",
    "concept_ids": C_STR,
    "title": "Cleaning text with LOWER, UPPER, TRIM, CONCAT, and LENGTH",
    "eyebrow": "String functions",
    "lede": "Four functions that clean, combine, and measure text values in a query.",
    "blocks": [s01_t2_prose1, s01_t2_prose2, s01_t2_ba],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C_STR,
        ["sql.string_functions#f1", "sql.string_functions#f2",
         "sql.string_functions#f3", "sql.string_functions#f4"],
        tb_ids=["sql.string_functions#tb1", "sql.string_functions#tb2"],
        anchors=["sql.string_functions#visual"],
    ),
}

# ── s02 check: string_functions — f1 — apply_lower_and_upper ─────────────
step_t2_s02 = check_step(
    f"{T2}.s02",
    C_STR,
    "LOWER and UPPER: which function to use",
    "Quick check",
    "Choose the expression that converts a city name to all lower case for comparison.",
    ["sql.string_functions#f1"],
    ["sql.string_functions#assessment:apply_lower_and_upper"],
)

# ── s03 hands_on: string_functions — f2,f3,f4 ────────────────────────────
step_t2_s03 = hands_on_step(
    f"{T2}.s03",
    C_STR,
    "Trim, concat, and measure customer city names",
    "Practice",
    "Write a query that trims stray spaces from the city column, standardises its case, and builds a label column with CONCAT.",
    ["sql.string_functions#f2", "sql.string_functions#f3", "sql.string_functions#f4"],
    [
        "sql.string_functions#practice",
        "sql.string_functions#assessment:apply_trim_to_stray_spaces",
        "sql.string_functions#assessment:build_a_label_with_concat_and_length",
    ],
)

# ── s04 explainer: date_time_functions — code_walkthrough — budget 65 ────
# Plan: tb1 (f1), tb2 (f2), visual=code_walkthrough
s04_t2_prose = prose(
    f"{T2}.s04.p1",
    "EXTRACT(field FROM source) retrieves a subfield — year, month, day, hour — from a date or timestamp. "
    "EXTRACT(month FROM order_date) returns the month number an order was placed. "
    "Subtracting two dates gives the number of days between them: a later order_date minus an earlier one gives the elapsed days.",
    "definition",
    C_DT,
    ["sql.date_time_functions#f1", "sql.date_time_functions#f2"],
    tb_ids=["sql.date_time_functions#tb1", "sql.date_time_functions#tb2"],
)

s04_t2_cw = {
    "type": "code_walkthrough",
    "block_id": f"{T2}.s04.cw",
    "language": "sql",
    "code": (
        "SELECT order_id,\n"
        "       order_date,\n"
        "       EXTRACT(year  FROM order_date) AS order_year,\n"
        "       EXTRACT(month FROM order_date) AS order_month,\n"
        "       order_date - '2024-01-01'      AS days_since_jan1\n"
        "  FROM orders\n"
        " LIMIT 5"
    ),
    "annotations": [
        {"start_line": 3, "end_line": 3, "text": "EXTRACT(year FROM order_date) pulls the 4-digit year"},
        {"start_line": 4, "end_line": 4, "text": "EXTRACT(month FROM order_date) pulls the month number (1–12)"},
        {"start_line": 5, "end_line": 5, "text": "date - date gives the number of elapsed days as an integer"},
    ],
    "reveal": "line_by_line",
    "lineage": {
        "concept_ids": C_DT,
        "fact_ids": ["sql.date_time_functions#f1", "sql.date_time_functions#f2"],
        "teaching_block_ids": ["sql.date_time_functions#tb1", "sql.date_time_functions#tb2"],
        "anchors": ["sql.date_time_functions#visual"],
    },
}

step_t2_s04 = {
    "step_id": f"{T2}.s04",
    "type": "explainer",
    "concept_ids": C_DT,
    "title": "Extracting date parts and computing elapsed days",
    "eyebrow": "Date functions",
    "lede": "Pull year, month, or hour from a date; subtract two dates to get the number of days between them.",
    "blocks": [s04_t2_prose, s04_t2_cw],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C_DT,
        ["sql.date_time_functions#f1", "sql.date_time_functions#f2"],
        tb_ids=["sql.date_time_functions#tb1", "sql.date_time_functions#tb2"],
        anchors=["sql.date_time_functions#visual"],
    ),
}

# ── s05 check: date_time_functions — f2 — compute_days_between_dates ─────
step_t2_s05 = check_step(
    f"{T2}.s05",
    C_DT,
    "Days between two dates",
    "Quick check",
    "What does subtracting one date from another return in SQL?",
    ["sql.date_time_functions#f2"],
    ["sql.date_time_functions#assessment:compute_days_between_dates"],
)

# ── s06 hands_on: date_time_functions — f1,f2 ────────────────────────────
step_t2_s06 = hands_on_step(
    f"{T2}.s06",
    C_DT,
    "Extract order month and compute days since order",
    "Practice",
    "Write a query that extracts the month from order_date and computes how many days have elapsed since a reference date.",
    ["sql.date_time_functions#f1", "sql.date_time_functions#f2"],
    [
        "sql.date_time_functions#practice",
        "sql.date_time_functions#assessment:extract_a_date_part",
        "sql.date_time_functions#assessment:compute_days_between_dates",
    ],
)

# ── s07 explainer: type_casting — side_by_side — budget 94 ───────────────
# Plan: tb1 (f1), tb2 (f2), visual=side_by_side (comparison in plan, side_by_side in needs)
# Visual anchor type is "comparison" but plan says side_by_side — use side_by_side per plan
s07_t2_prose1 = prose(
    f"{T2}.s07.p1",
    "PostgreSQL accepts two equivalent syntaxes for a type cast. "
    "CAST(expression AS type) is the standard form; expression::type is the shorthand. "
    "CAST(delivery_time_minutes AS text) and delivery_time_minutes::text both convert that integer column to text — same result, two ways to write it.",
    "definition",
    C_TC,
    ["sql.type_casting#f1"],
    tb_ids=["sql.type_casting#tb1"],
)

s07_t2_prose2 = prose(
    f"{T2}.s07.p2",
    "A cast succeeds only if a suitable type conversion is defined between the source type and the target type. "
    "Converting delivery_time_minutes (an integer) to text works because an integer-to-text conversion is defined. "
    "A cast between two types with no defined conversion does not succeed.",
    "mechanism",
    C_TC,
    ["sql.type_casting#f2"],
    tb_ids=["sql.type_casting#tb2"],
)

# side_by_side: CAST syntax vs :: syntax
s07_t2_sbs = {
    "type": "side_by_side",
    "block_id": f"{T2}.s07.sbs",
    "left_label": "CAST(... AS type) syntax",
    "right_label": "expression::type shorthand",
    "left": {
        "type": "code_walkthrough",
        "block_id": f"{T2}.s07.sbs_left",
        "language": "sql",
        "code": "SELECT CAST(delivery_time_minutes AS text) AS minutes_text\n  FROM orders\n LIMIT 3",
        "annotations": [
            {"start_line": 1, "end_line": 1, "text": "Standard SQL CAST syntax: CAST(value AS target_type)"}
        ],
        "reveal": "all",
    },
    "right": {
        "type": "code_walkthrough",
        "block_id": f"{T2}.s07.sbs_right",
        "language": "sql",
        "code": "SELECT delivery_time_minutes::text AS minutes_text\n  FROM orders\n LIMIT 3",
        "annotations": [
            {"start_line": 1, "end_line": 1, "text": "PostgreSQL shorthand: value::target_type — identical result"}
        ],
        "reveal": "all",
    },
    "takeaway": "Both expressions produce the same result. Use whichever your team's style guide prefers; the :: shorthand is common in PostgreSQL codebases.",
    "lineage": {
        "concept_ids": C_TC,
        "fact_ids": ["sql.type_casting#f1"],
        "teaching_block_ids": ["sql.type_casting#tb1"],
        "anchors": ["sql.type_casting#visual"],
    },
}

step_t2_s07 = {
    "step_id": f"{T2}.s07",
    "type": "explainer",
    "concept_ids": C_TC,
    "title": "Type casting: CAST and :: syntax",
    "eyebrow": "Type casting",
    "lede": "Convert a value from one type to another using CAST or the :: shorthand.",
    "blocks": [s07_t2_prose1, s07_t2_prose2, s07_t2_sbs],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C_TC,
        ["sql.type_casting#f1", "sql.type_casting#f2"],
        tb_ids=["sql.type_casting#tb1", "sql.type_casting#tb2"],
        anchors=["sql.type_casting#visual"],
    ),
}

# ── s08 check: type_casting — f2 — judge_whether_a_cast_is_defined ───────
step_t2_s08 = check_step(
    f"{T2}.s08",
    C_TC,
    "Will this cast succeed?",
    "Quick check",
    "Decide whether a given cast expression will succeed or fail based on whether a conversion is defined.",
    ["sql.type_casting#f2"],
    ["sql.type_casting#assessment:judge_whether_a_cast_is_defined"],
)

# ── s09 hands_on: type_casting — f1 ──────────────────────────────────────
step_t2_s09 = hands_on_step(
    f"{T2}.s09",
    C_TC,
    "Write a cast in both syntaxes",
    "Practice",
    "Convert delivery_time_minutes to text once using CAST(... AS text) and once using the :: shorthand.",
    ["sql.type_casting#f1"],
    [
        "sql.type_casting#practice",
        "sql.type_casting#assessment:write_a_cast_in_both_syntaxes",
    ],
)

# ── s10 recap ─────────────────────────────────────────────────────────────
s10_t2_prose = prose(
    f"{T2}.s10.p1",
    "LOWER and UPPER change string case; TRIM removes leading/trailing spaces; CONCAT joins strings (ignoring NULLs); LENGTH counts characters. "
    "EXTRACT(field FROM source) pulls a date subfield such as year or month; subtracting two dates gives elapsed days. "
    "CAST(expression AS type) and expression::type are two equivalent ways to convert a value to a different type — "
    "the cast succeeds only when a conversion between those types is defined.",
    "takeaway",
    C_ALL,
    [
        "sql.string_functions#f1", "sql.string_functions#f2",
        "sql.string_functions#f3", "sql.string_functions#f4",
        "sql.date_time_functions#f1", "sql.date_time_functions#f2",
        "sql.type_casting#f1", "sql.type_casting#f2",
    ],
    tb_ids=[
        "sql.string_functions#tb1", "sql.string_functions#tb2",
        "sql.date_time_functions#tb1", "sql.date_time_functions#tb2",
        "sql.type_casting#tb1", "sql.type_casting#tb2",
    ],
)

s10_t2_un = up_next(
    f"{T2}.s10.un",
    "Next: NULL Fallbacks and UNION",
    "You can now transform values inside a query. Next you will handle missing values with COALESCE "
    "and combine the results of two queries into one list using UNION.",
)

step_t2_s10 = {
    "step_id": f"{T2}.s10",
    "type": "recap",
    "concept_ids": C_ALL,
    "title": "Recap: Text, Dates, and Casts",
    "eyebrow": "Recap",
    "lede": "Five string functions, two date operations, and two cast syntaxes.",
    "blocks": [s10_t2_prose, s10_t2_un],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C_ALL,
        [
            "sql.string_functions#f1", "sql.string_functions#f2",
            "sql.string_functions#f3", "sql.string_functions#f4",
            "sql.date_time_functions#f1", "sql.date_time_functions#f2",
            "sql.type_casting#f1", "sql.type_casting#f2",
        ],
        tb_ids=[
            "sql.string_functions#tb1", "sql.string_functions#tb2",
            "sql.date_time_functions#tb1", "sql.date_time_functions#tb2",
            "sql.type_casting#tb1", "sql.type_casting#tb2",
        ],
    ),
}

# ── remediation steps for tile_sql_text_dates_casts ──────────────────────
# s02 measures f1 (apply_lower_and_upper) → r01
r01_t2_blocks = [
    prose(
        f"{T2}.r01.p1",
        "LOWER(text) converts every character in the string to lower case: LOWER('LAGOS') → 'lagos', LOWER('Lagos') → 'lagos'. "
        "UPPER(text) converts every character to upper case: UPPER('lagos') → 'LAGOS'. "
        "These functions are useful when city names or other categorical values were entered with inconsistent casing "
        "and you need to compare or group them reliably.",
        "definition",
        C_STR,
        ["sql.string_functions#f1"],
        tb_ids=["sql.string_functions#tb1"],
    )
]
rem_t2_r01 = remediation_step(
    f"{T2}.r01",
    C_STR,
    "LOWER and UPPER: converting string case",
    "Let's review",
    "LOWER converts to all lower case; UPPER converts to all upper case.",
    r01_t2_blocks,
    ["sql.string_functions#f1"],
    ["sql.string_functions#tb1"],
)

# s03 measures f2,f3,f4 (trim, concat, length) → r02
r02_t2_blocks = [
    prose(
        f"{T2}.r02.p1",
        "TRIM removes the longest string of the given characters (a space by default) from the start, end, or both ends of a string. "
        "TRIM(city) strips accidental leading or trailing spaces from a city value. "
        "CONCAT joins its arguments into one string and ignores any NULL arguments: "
        "CONCAT(name, ' (', city, ')') builds a label even when city is NULL. "
        "LENGTH(text) returns the number of characters: LENGTH(name) gives the character count of a customer's name.",
        "syntax",
        C_STR,
        ["sql.string_functions#f2", "sql.string_functions#f3", "sql.string_functions#f4"],
        tb_ids=["sql.string_functions#tb2"],
    )
]
rem_t2_r02 = remediation_step(
    f"{T2}.r02",
    C_STR,
    "TRIM, CONCAT, and LENGTH",
    "Let's review",
    "TRIM removes spaces; CONCAT joins strings; LENGTH counts characters.",
    r02_t2_blocks,
    ["sql.string_functions#f2", "sql.string_functions#f3", "sql.string_functions#f4"],
    ["sql.string_functions#tb2"],
)

# s05 measures f2 (compute_days_between_dates) → r03
r03_t2_blocks = [
    prose(
        f"{T2}.r03.p1",
        "Subtracting one date from another in SQL produces the number of days elapsed between them as an integer. "
        "If order_date is '2024-02-03' and you subtract '2024-01-01', the result is 33 days. "
        "This is different from EXTRACT, which pulls a single subfield (year, month, day) out of one date value.",
        "mechanism",
        C_DT,
        ["sql.date_time_functions#f2"],
        tb_ids=["sql.date_time_functions#tb2"],
    )
]
rem_t2_r03 = remediation_step(
    f"{T2}.r03",
    C_DT,
    "Date subtraction gives elapsed days",
    "Let's review",
    "Subtracting two dates returns the number of days between them.",
    r03_t2_blocks,
    ["sql.date_time_functions#f2"],
    ["sql.date_time_functions#tb2"],
)

# s06 measures f1,f2 (extract_a_date_part, compute_days_between_dates) → r04
r04_t2_blocks = [
    prose(
        f"{T2}.r04.p1",
        "EXTRACT(field FROM source) retrieves a single subfield from a date, time, timestamp, or interval value. "
        "The field can be year, month, day, hour, minute, second, and others. "
        "EXTRACT(month FROM order_date) returns the month number (1–12) for each order. "
        "To get the number of days between two dates, subtract them directly: order_date - '2024-01-01' gives elapsed days.",
        "definition",
        C_DT,
        ["sql.date_time_functions#f1", "sql.date_time_functions#f2"],
        tb_ids=["sql.date_time_functions#tb1", "sql.date_time_functions#tb2"],
    )
]
rem_t2_r04 = remediation_step(
    f"{T2}.r04",
    C_DT,
    "EXTRACT and date subtraction",
    "Let's review",
    "EXTRACT pulls a subfield from one date; subtraction gives days between two dates.",
    r04_t2_blocks,
    ["sql.date_time_functions#f1", "sql.date_time_functions#f2"],
    ["sql.date_time_functions#tb1", "sql.date_time_functions#tb2"],
)

# s08 measures f2 (judge_whether_a_cast_is_defined) → r05
r05_t2_blocks = [
    prose(
        f"{T2}.r05.p1",
        "A type cast succeeds only if a suitable conversion is defined between the source type and the target type. "
        "Converting an integer to text works because that conversion is defined. "
        "A cast between two types that have no defined conversion does not succeed — the database will return an error. "
        "Always check that the conversion you need is supported before relying on it in a query.",
        "mechanism",
        C_TC,
        ["sql.type_casting#f2"],
        tb_ids=["sql.type_casting#tb2"],
    )
]
rem_t2_r05 = remediation_step(
    f"{T2}.r05",
    C_TC,
    "When does a cast succeed?",
    "Let's review",
    "A cast succeeds only when a conversion between the two types is defined.",
    r05_t2_blocks,
    ["sql.type_casting#f2"],
    ["sql.type_casting#tb2"],
)

# s09 measures f1 (write_a_cast_in_both_syntaxes) → r06
r06_t2_blocks = [
    prose(
        f"{T2}.r06.p1",
        "PostgreSQL provides two equivalent syntaxes for a type cast. "
        "The standard form is CAST(expression AS type): CAST(delivery_time_minutes AS text). "
        "The shorthand is expression::type: delivery_time_minutes::text. "
        "Both produce exactly the same result. The :: shorthand is specific to PostgreSQL; "
        "CAST(... AS type) is portable across SQL dialects.",
        "definition",
        C_TC,
        ["sql.type_casting#f1"],
        tb_ids=["sql.type_casting#tb1"],
    )
]
rem_t2_r06 = remediation_step(
    f"{T2}.r06",
    C_TC,
    "Two cast syntaxes: CAST and ::",
    "Let's review",
    "CAST(expression AS type) and expression::type are equivalent — use either.",
    r06_t2_blocks,
    ["sql.type_casting#f1"],
    ["sql.type_casting#tb1"],
)

tile2 = {
    "tile_id": T2,
    "title": "Text and Date Functions",
    "summary": "Clean and transform text with LOWER, UPPER, TRIM, CONCAT, and LENGTH; extract date parts with EXTRACT and compute elapsed days; convert types with CAST and :: syntax.",
    "steps": [
        step_t2_s01, step_t2_s02, step_t2_s03,
        step_t2_s04, step_t2_s05, step_t2_s06,
        step_t2_s07, step_t2_s08, step_t2_s09,
        step_t2_s10,
    ],
    "remediation_steps": [
        rem_t2_r01, rem_t2_r02,
        rem_t2_r03, rem_t2_r04,
        rem_t2_r05, rem_t2_r06,
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# TILE 3: tile_sql_null_fallback_and_union
# Steps: s01-s09
# Concepts: sql.coalesce, sql.union
# ═══════════════════════════════════════════════════════════════════════════

T3 = "tile_sql_null_fallback_and_union"
C_CO = ["sql.coalesce"]
C_UN = ["sql.union"]
C_T3 = ["sql.coalesce", "sql.union"]

# ── s01 explainer: coalesce — before_after — budget 73 ───────────────────
# Plan: tb1 (f1), tb2 (f2), visual=before_after
s01_t3_prose = prose(
    f"{T3}.s01.p1",
    "COALESCE(value [, ...]) returns the first of its arguments that is not null, "
    "and returns null only if every argument is null. "
    "COALESCE(city, 'unknown') returns the customer's actual city when it is recorded, "
    "and 'unknown' when it is missing. "
    "It is commonly used to substitute a default value for null — "
    "COALESCE(name, 'unnamed customer') falls back to a fixed label whenever a name was not recorded.",
    "definition",
    C_CO,
    ["sql.coalesce#f1", "sql.coalesce#f2"],
    tb_ids=["sql.coalesce#tb1", "sql.coalesce#tb2"],
)

# before_after: city column with NULLs → city column after COALESCE
s01_t3_before = {
    "type": "data_table",
    "block_id": f"{T3}.s01.dt_before",
    "asset_ref": {
        "asset_id": "ds_customers",
        "columns": ["customer_id", "name", "city"],
        "max_rows": 6,
    },
    "caption": "Customers table — city is NULL for some rows",
    "highlight": [
        {"target": {"kind": "cell", "column": "city"}, "label": "NULL", "tone": "bad"},
    ],
}

s01_t3_after = {
    "type": "data_table",
    "block_id": f"{T3}.s01.dt_after",
    "result_of": {
        "runtime": "sql",
        "sql": "SELECT customer_id, name, COALESCE(city, 'unknown') AS city FROM customers",
        "asset_mounts": [
            {"asset_id": "ds_customers", "mount_path": "customers"}
        ],
    },
    "caption": "After COALESCE(city, 'unknown') — NULLs replaced with 'unknown'",
}

s01_t3_ba = {
    "type": "before_after",
    "block_id": f"{T3}.s01.ba",
    "before": s01_t3_before,
    "after": s01_t3_after,
    "change_summary": "COALESCE(city, 'unknown') fills every NULL city with the fallback value 'unknown'.",
    "lineage": {
        "concept_ids": C_CO,
        "fact_ids": ["sql.coalesce#f1", "sql.coalesce#f2"],
        "teaching_block_ids": ["sql.coalesce#tb1", "sql.coalesce#tb2"],
        "anchors": ["sql.coalesce#visual"],
    },
}

step_t3_s01 = {
    "step_id": f"{T3}.s01",
    "type": "explainer",
    "concept_ids": C_CO,
    "title": "Replacing NULL with a default using COALESCE",
    "eyebrow": "COALESCE",
    "lede": "COALESCE returns the first non-null argument — use it to substitute a default for missing values.",
    "blocks": [s01_t3_prose, s01_t3_ba],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C_CO,
        ["sql.coalesce#f1", "sql.coalesce#f2"],
        tb_ids=["sql.coalesce#tb1", "sql.coalesce#tb2"],
        anchors=["sql.coalesce#visual"],
    ),
}

# ── s02 check: coalesce — f1 — predict_coalesce_result ───────────────────
step_t3_s02 = check_step(
    f"{T3}.s02",
    C_CO,
    "What does COALESCE return?",
    "Quick check",
    "Predict the value returned by a COALESCE expression given a specific input.",
    ["sql.coalesce#f1"],
    ["sql.coalesce#assessment:predict_coalesce_result"],
)

# ── s03 check: coalesce — f2 — substitute_a_default_for_null ─────────────
step_t3_s03 = check_step(
    f"{T3}.s03",
    C_CO,
    "Substituting a default for NULL",
    "Quick check",
    "Choose the COALESCE expression that replaces a missing customer name with a fixed label.",
    ["sql.coalesce#f2"],
    ["sql.coalesce#assessment:substitute_a_default_for_null"],
)

# ── s04 hands_on: coalesce ────────────────────────────────────────────────
step_t3_s04 = hands_on_step(
    f"{T3}.s04",
    C_CO,
    "Replace missing city values with COALESCE",
    "Practice",
    "Write a query that uses COALESCE to replace NULL city values with the string 'unknown'.",
    # plan fact_ids is empty for s04 — use empty list
    [],
    ["sql.coalesce#practice"],
)

# ── s05 explainer: union — diagram — budget 137 ───────────────────────────
# Plan: tb1 (f1), tb2 (f2), visual=diagram
s05_t3_prose1 = prose(
    f"{T3}.s05.p1",
    "UNION effectively appends the result rows of the second query to the result of the first, "
    "although there is no guarantee that this is the order the rows actually come back in. "
    "SELECT customer_id FROM customers WHERE city = 'Lagos' "
    "UNION "
    "SELECT customer_id FROM orders WHERE delivery_time_minutes > 60 "
    "combines Lagos customers with customers who had a slow order into one list.",
    "definition",
    C_UN,
    ["sql.union#f1"],
    tb_ids=["sql.union#tb1"],
)

s05_t3_prose2 = prose(
    f"{T3}.s05.p2",
    "UNION eliminates duplicate rows from its combined result, the same way DISTINCT does, "
    "unless UNION ALL is used, which keeps every row. "
    "A Lagos customer who also placed two orders over 60 minutes appears once under UNION "
    "but three times under UNION ALL — once from the first query, twice from the second.",
    "mechanism",
    C_UN,
    ["sql.union#f2"],
    tb_ids=["sql.union#tb2"],
)

# diagram: two result lists stacked, UNION ALL keeps duplicate, UNION collapses it
s05_t3_diagram = {
    "type": "diagram",
    "block_id": f"{T3}.s05.diag",
    "diagram_kind": "container",
    "title": "UNION vs UNION ALL",
    "nodes": [
        {"id": "q1", "label": "Query 1 result\ncustomer_id: 1, 2, 3", "kind": "result_set", "group": "input"},
        {"id": "q2", "label": "Query 2 result\ncustomer_id: 1, 4", "kind": "result_set", "group": "input"},
        {"id": "union_all", "label": "UNION ALL\ncustomer_id: 1, 2, 3, 1, 4\n(duplicate 1 kept)", "kind": "result_set", "group": "union_all"},
        {"id": "union", "label": "UNION\ncustomer_id: 1, 2, 3, 4\n(duplicate 1 removed)", "kind": "result_set", "group": "union"},
    ],
    "edges": [
        {"from": "q1", "to": "union_all", "label": "stacked", "directed": True},
        {"from": "q2", "to": "union_all", "label": "stacked", "directed": True},
        {"from": "q1", "to": "union", "label": "stacked + deduplicated", "directed": True},
        {"from": "q2", "to": "union", "label": "stacked + deduplicated", "directed": True},
    ],
    "layout": "auto",
    "alt_text": "Two query result sets stacked by UNION ALL (keeping the duplicate customer_id 1) and by UNION (removing the duplicate, leaving four distinct ids).",
    "lineage": {
        "concept_ids": C_UN,
        "fact_ids": ["sql.union#f1", "sql.union#f2"],
        "teaching_block_ids": ["sql.union#tb1", "sql.union#tb2"],
        "anchors": ["sql.union#visual"],
    },
}

step_t3_s05 = {
    "step_id": f"{T3}.s05",
    "type": "explainer",
    "concept_ids": C_UN,
    "title": "Stacking query results with UNION and UNION ALL",
    "eyebrow": "UNION",
    "lede": "UNION appends one result set to another; UNION removes duplicates while UNION ALL keeps every row.",
    "blocks": [s05_t3_prose1, s05_t3_prose2, s05_t3_diagram],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C_UN,
        ["sql.union#f1", "sql.union#f2"],
        tb_ids=["sql.union#tb1", "sql.union#tb2"],
        anchors=["sql.union#visual"],
    ),
}

# ── s06 explainer: union — no visual — budget 46 ─────────────────────────
# Plan: tb3 (f3), no visual
s06_t3_prose = prose(
    f"{T3}.s06.p1",
    "For UNION, both queries must return the same number of columns with compatible data types. "
    "SELECT customer_id FROM customers WHERE city = 'Lagos' "
    "UNION "
    "SELECT customer_id FROM orders WHERE delivery_time_minutes > 60 "
    "works because both return one integer column.",
    "syntax",
    C_UN,
    ["sql.union#f3"],
    tb_ids=["sql.union#tb3"],
)

step_t3_s06 = {
    "step_id": f"{T3}.s06",
    "type": "explainer",
    "concept_ids": C_UN,
    "title": "UNION compatibility: matching columns and types",
    "eyebrow": "UNION rules",
    "lede": "Both queries must return the same number of columns with compatible types.",
    "blocks": [s06_t3_prose],
    "reward": {"gems": 3},
    "lineage": step_lineage(
        C_UN,
        ["sql.union#f3"],
        tb_ids=["sql.union#tb3"],
    ),
}

# ── s07 check: union — f3 — check_union_compatibility ────────────────────
step_t3_s07 = check_step(
    f"{T3}.s07",
    C_UN,
    "Are these two queries compatible for UNION?",
    "Quick check",
    "Decide whether two given SELECT statements can be combined with UNION.",
    ["sql.union#f3"],
    ["sql.union#assessment:check_union_compatibility"],
)

# ── s08 hands_on: union — f1,f2 ──────────────────────────────────────────
step_t3_s08 = hands_on_step(
    f"{T3}.s08",
    C_UN,
    "Stack two queries with UNION and UNION ALL",
    "Practice",
    "Write a query that combines Lagos customers and customers with slow orders, first with UNION and then with UNION ALL.",
    ["sql.union#f1", "sql.union#f2"],
    [
        "sql.union#practice",
        "sql.union#assessment:describe_how_union_combines_results",
        "sql.union#assessment:choose_union_or_union_all",
    ],
)

# ── s09 recap ─────────────────────────────────────────────────────────────
s09_t3_prose = prose(
    f"{T3}.s09.p1",
    "COALESCE(value [, ...]) returns the first non-null argument; use it to substitute a default for missing values. "
    "UNION appends the rows of the second query to the first — UNION removes duplicate rows, UNION ALL keeps every row. "
    "For UNION to work, both queries must return the same number of columns with compatible data types.",
    "takeaway",
    C_T3,
    [
        "sql.coalesce#f1", "sql.coalesce#f2",
        "sql.union#f1", "sql.union#f2", "sql.union#f3",
    ],
    tb_ids=[
        "sql.coalesce#tb1", "sql.coalesce#tb2",
        "sql.union#tb1", "sql.union#tb2", "sql.union#tb3",
    ],
)

s09_t3_un = up_next(
    f"{T3}.s09.un",
    "Next: Joining Tables",
    "You can now combine rows from separate queries with UNION. "
    "Next you will combine columns from separate tables using JOIN — "
    "matching rows from an orders table to rows in a customers table on a shared key.",
)

step_t3_s09 = {
    "step_id": f"{T3}.s09",
    "type": "recap",
    "concept_ids": C_T3,
    "title": "Recap: NULL Fallbacks and UNION",
    "eyebrow": "Recap",
    "lede": "COALESCE fills missing values; UNION stacks compatible result sets.",
    "blocks": [s09_t3_prose, s09_t3_un],
    "reward": {"gems": 5},
    "lineage": step_lineage(
        C_T3,
        [
            "sql.coalesce#f1", "sql.coalesce#f2",
            "sql.union#f1", "sql.union#f2", "sql.union#f3",
        ],
        tb_ids=[
            "sql.coalesce#tb1", "sql.coalesce#tb2",
            "sql.union#tb1", "sql.union#tb2", "sql.union#tb3",
        ],
    ),
}

# ── remediation steps for tile_sql_null_fallback_and_union ───────────────
# s02 measures f1 (predict_coalesce_result) → r01
r01_t3_blocks = [
    prose(
        f"{T3}.r01.p1",
        "COALESCE evaluates its arguments from left to right and returns the first one that is not null. "
        "COALESCE(city, 'unknown') returns city when city is not null, and 'unknown' when city is null. "
        "COALESCE returns null only when every argument is null — COALESCE(NULL, NULL) returns null.",
        "definition",
        C_CO,
        ["sql.coalesce#f1"],
        tb_ids=["sql.coalesce#tb1"],
    )
]
rem_t3_r01 = remediation_step(
    f"{T3}.r01",
    C_CO,
    "How COALESCE picks its return value",
    "Let's review",
    "COALESCE returns the first non-null argument, or null if all arguments are null.",
    r01_t3_blocks,
    ["sql.coalesce#f1"],
    ["sql.coalesce#tb1"],
)

# s03 measures f2 (substitute_a_default_for_null) → r02
r02_t3_blocks = [
    prose(
        f"{T3}.r02.p1",
        "COALESCE is commonly used to substitute a default value for null. "
        "COALESCE(name, 'unnamed customer') returns the customer's actual name when it is recorded, "
        "and the fixed string 'unnamed customer' when the name column is null. "
        "This pattern keeps downstream calculations and labels clean even when source data has gaps.",
        "mechanism",
        C_CO,
        ["sql.coalesce#f2"],
        tb_ids=["sql.coalesce#tb2"],
    )
]
rem_t3_r02 = remediation_step(
    f"{T3}.r02",
    C_CO,
    "COALESCE as a default-value substitution",
    "Let's review",
    "Use COALESCE(column, default) to replace NULL with a fixed fallback value.",
    r02_t3_blocks,
    ["sql.coalesce#f2"],
    ["sql.coalesce#tb2"],
)

# s07 measures f3 (check_union_compatibility) → r03
r03_t3_blocks = [
    prose(
        f"{T3}.r03.p1",
        "UNION requires both queries to return the same number of columns, "
        "with corresponding columns having compatible data types. "
        "If the first query returns one integer column and the second also returns one integer column, "
        "they are compatible. "
        "If the column counts differ, or if a text column is paired with an integer column, "
        "the UNION will fail.",
        "syntax",
        C_UN,
        ["sql.union#f3"],
        tb_ids=["sql.union#tb3"],
    )
]
rem_t3_r03 = remediation_step(
    f"{T3}.r03",
    C_UN,
    "UNION compatibility rules",
    "Let's review",
    "Both queries must return the same number of columns with compatible types.",
    r03_t3_blocks,
    ["sql.union#f3"],
    ["sql.union#tb3"],
)

# s08 measures f1,f2 (describe_how_union_combines_results, choose_union_or_union_all) → r04
r04_t3_blocks = [
    prose(
        f"{T3}.r04.p1",
        "UNION appends the rows of the second query to the rows of the first. "
        "UNION removes duplicate rows from the combined result, the same way DISTINCT does. "
        "UNION ALL keeps every row, including duplicates. "
        "Use UNION when you want a distinct list; use UNION ALL when you need every occurrence, "
        "including rows that appear in both queries.",
        "mechanism",
        C_UN,
        ["sql.union#f1", "sql.union#f2"],
        tb_ids=["sql.union#tb1", "sql.union#tb2"],
    )
]
rem_t3_r04 = remediation_step(
    f"{T3}.r04",
    C_UN,
    "UNION vs UNION ALL: deduplication",
    "Let's review",
    "UNION removes duplicates; UNION ALL keeps every row.",
    r04_t3_blocks,
    ["sql.union#f1", "sql.union#f2"],
    ["sql.union#tb1", "sql.union#tb2"],
)

tile3 = {
    "tile_id": T3,
    "title": "NULL Fallbacks and UNION",
    "summary": "Replace missing values with a default using COALESCE, and combine the results of two compatible queries into one list using UNION or UNION ALL.",
    "steps": [
        step_t3_s01, step_t3_s02, step_t3_s03, step_t3_s04,
        step_t3_s05, step_t3_s06, step_t3_s07, step_t3_s08,
        step_t3_s09,
    ],
    "remediation_steps": [rem_t3_r01, rem_t3_r02, rem_t3_r03, rem_t3_r04],
}

# ═══════════════════════════════════════════════════════════════════════════
# Assemble final artifact
# ═══════════════════════════════════════════════════════════════════════════

artifact = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_006_da_sql_rest",
    "tiles": [tile1, tile2, tile3],
}

out_path = "batches/final_batch_006_da_sql_rest/screens.part.c2.json"
with open(out_path, "w") as f:
    json.dump(artifact, f, indent=2)

print(f"Written: {out_path}")
# Count steps
for tile in artifact["tiles"]:
    main = len(tile["steps"])
    rem  = len(tile.get("remediation_steps", []))
    print(f"  {tile['tile_id']}: {main} main steps, {rem} remediation steps")
