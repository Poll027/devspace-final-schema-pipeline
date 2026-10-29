"""Build screens.part.c0_canary.json for tile_sql_fund_filtering_rows."""
import json

# ── helpers ──────────────────────────────────────────────────────────────────
def qid(concept, local):
    """Return qualified fact/tb/anchor id."""
    return f"{concept}#{local}"

# ── dataset facts (from registry) ────────────────────────────────────────────
# ds_orders columns: order_id, customer_id, delivery_time_minutes, order_date, region, amount, city
# rows (first 6 for display):
# 1001,1,15,2024-01-05,south,4200.0,Lagos
# 1002,2,22,2024-01-12,north,8750.0,Kano
# 1003,1,41,2024-02-03,south,3100.0,Lagos
# 1004,3,18,2024-02-14,other,5600.0,Abuja
# 1005,2,35,2024-03-01,north,2900.0,Kano
# 1006,1,63,2024-03-18,south,7400.0,Lagos
# 1011,2,NULL,2024-06-01,north,4100.0,Kano
# 1012,1,NULL,2024-06-15,south,5500.0,Lagos

TILE = "tile_sql_fund_filtering_rows"

# ── step builder helpers ──────────────────────────────────────────────────────
def step(step_id, stype, concept_ids, title, eyebrow=None, lede=None, blocks=None, reward=None, lineage=None):
    s = {
        "step_id": step_id,
        "type": stype,
        "concept_ids": concept_ids,
        "title": title,
    }
    if eyebrow:
        s["eyebrow"] = eyebrow
    if lede:
        s["lede"] = lede
    if blocks is not None:
        s["blocks"] = blocks
    if reward:
        s["reward"] = reward
    if lineage:
        s["lineage"] = lineage
    return s

def lineage(concept_ids=None, fact_ids=None, teaching_block_ids=None, segment_ids=None, anchors=None):
    d = {}
    if concept_ids is not None:
        d["concept_ids"] = concept_ids
    if fact_ids is not None:
        d["fact_ids"] = fact_ids
    if teaching_block_ids is not None:
        d["teaching_block_ids"] = teaching_block_ids
    if segment_ids is not None:
        d["segment_ids"] = segment_ids
    if anchors is not None:
        d["anchors"] = anchors
    return d

def prose(block_id, text, role, fact_ids, teaching_block_ids=None, concept_ids=None, anchors=None):
    b = {
        "type": "prose",
        "block_id": block_id,
        "text": text,
        "role": role,
        "lineage": lineage(
            concept_ids=concept_ids,
            fact_ids=fact_ids,
            teaching_block_ids=teaching_block_ids,
            anchors=anchors,
        )
    }
    return b

def heading(block_id, text, level=2):
    return {"type": "heading", "block_id": block_id, "text": text, "level": level}

def data_table_asset(block_id, asset_id, columns, caption=None, highlight=None, lineage_obj=None):
    b = {
        "type": "data_table",
        "block_id": block_id,
        "asset_ref": {"asset_id": asset_id, "columns": columns},
    }
    if caption:
        b["caption"] = caption
    if highlight:
        b["highlight"] = highlight
    if lineage_obj:
        b["lineage"] = lineage_obj
    return b

def data_table_result(block_id, sql, asset_mounts, caption=None, highlight=None, lineage_obj=None):
    b = {
        "type": "data_table",
        "block_id": block_id,
        "result_of": {
            "runtime": "sql",
            "sql": sql,
            "asset_mounts": asset_mounts,
        },
    }
    if caption:
        b["caption"] = caption
    if highlight:
        b["highlight"] = highlight
    if lineage_obj:
        b["lineage"] = lineage_obj
    return b

# ─────────────────────────────────────────────────────────────────────────────
# STEP s01 — explainer: WHERE filtering (before_after visual)
# ─────────────────────────────────────────────────────────────────────────────
# before: full orders table (asset_ref)
# after: result of WHERE delivery_time_minutes > 40 (result_of)

s01_before = data_table_asset(
    block_id=f"{TILE}.s01.before",
    asset_id="ds_orders",
    columns=["order_id", "customer_id", "delivery_time_minutes"],
    caption="All orders — no filter applied",
    highlight=[
        {"target": {"kind": "row", "row": {"where": {"order_id": 1003}}}, "label": "kept", "tone": "good"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1006}}}, "label": "kept", "tone": "good"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1008}}}, "label": "kept", "tone": "good"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1010}}}, "label": "kept", "tone": "good"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1013}}}, "label": "kept", "tone": "good"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1001}}}, "label": "discarded", "tone": "bad"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1002}}}, "label": "discarded", "tone": "bad"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1004}}}, "label": "discarded", "tone": "bad"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1005}}}, "label": "discarded", "tone": "bad"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1007}}}, "label": "discarded", "tone": "bad"},
        {"target": {"kind": "row", "row": {"where": {"order_id": 1009}}}, "label": "discarded", "tone": "bad"},
    ],
)

s01_after = data_table_result(
    block_id=f"{TILE}.s01.after",
    sql="SELECT order_id, customer_id, delivery_time_minutes FROM orders WHERE delivery_time_minutes > 40",
    asset_mounts=[{"asset_id": "ds_orders", "mount_path": "orders"}],
    caption="After WHERE delivery_time_minutes > 40 — only rows where the condition is true",
)

s01_before_after = {
    "type": "before_after",
    "block_id": f"{TILE}.s01.ba",
    "before": s01_before,
    "after": s01_after,
    "change_summary": "WHERE delivery_time_minutes > 40 keeps only the five orders whose delivery time exceeds 40 minutes; the other rows are discarded.",
    "lineage": lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f1"), qid("sql.where_filtering", "f2")],
        teaching_block_ids=[qid("sql.where_filtering", "tb2"), qid("sql.where_filtering", "tb3")],
        anchors=[qid("sql.where_filtering", "visual")],
    ),
}

s01_intro = prose(
    block_id=f"{TILE}.s01.p1",
    text=(
        "SELECT * FROM orders returns every order in the QuickCart database. "
        "To answer a real question — 'which orders took longer than 40 minutes to deliver?' — "
        "you need to narrow the result to just the matching rows. "
        "That is what WHERE does: it takes a search condition and evaluates it for every row. "
        "A row is kept in the output only if the condition is true; rows where it is false are discarded."
    ),
    role="intro",
    fact_ids=[qid("sql.where_filtering", "f1")],
    teaching_block_ids=[qid("sql.where_filtering", "tb1"), qid("sql.where_filtering", "tb2")],
    concept_ids=["sql.where_filtering"],
)

s01_syntax = prose(
    block_id=f"{TILE}.s01.p2",
    text=(
        "The comparison operators <, >, <=, >=, =, and <> compare two values of the same or a compatible type "
        "and produce a boolean result. "
        "= tests for equal; <> tests for not equal (!= is an alias for <>). "
        "WHERE customer_id = 2 keeps only orders placed by customer 2; "
        "WHERE delivery_time_minutes <> 20 keeps every order whose recorded delivery time is something other than 20 minutes."
    ),
    role="syntax",
    fact_ids=[qid("sql.where_filtering", "f2")],
    teaching_block_ids=[qid("sql.where_filtering", "tb3")],
    concept_ids=["sql.where_filtering"],
)

step_s01 = step(
    step_id=f"{TILE}.s01",
    stype="explainer",
    concept_ids=["sql.where_filtering"],
    title="Filtering rows with WHERE",
    eyebrow="WHERE clause",
    lede="Ask a question of your data by keeping only the rows where a condition is true.",
    blocks=[s01_intro, s01_syntax, s01_before_after],
    reward={"gems": 5},
    lineage=lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f1"), qid("sql.where_filtering", "f2")],
        teaching_block_ids=[
            qid("sql.where_filtering", "tb1"),
            qid("sql.where_filtering", "tb2"),
            qid("sql.where_filtering", "tb3"),
        ],
        anchors=[qid("sql.where_filtering", "visual")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s02 — check: choose_the_right_comparison_operator (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s02 = step(
    step_id=f"{TILE}.s02",
    stype="check",
    concept_ids=["sql.where_filtering"],
    title="Pick the right comparison operator",
    eyebrow="Quick check",
    lede="Choose the operator that matches the filter requirement.",
    reward={"gems": 5, "first_try_bonus": 3},
    lineage=lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f2")],
        anchors=[qid("sql.where_filtering", "assessment:choose_the_right_comparison_operator")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s03 — check: write_where_for_a_filter_requirement (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s03 = step(
    step_id=f"{TILE}.s03",
    stype="check",
    concept_ids=["sql.where_filtering"],
    title="Write a WHERE clause for a requirement",
    eyebrow="Quick check",
    lede="Select the WHERE clause that correctly expresses the stated filter.",
    reward={"gems": 5, "first_try_bonus": 3},
    lineage=lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f1"), qid("sql.where_filtering", "f2")],
        anchors=[qid("sql.where_filtering", "assessment:write_where_for_a_filter_requirement")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s04 — hands_on: explain_which_rows_where_keeps / practice (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s04 = step(
    step_id=f"{TILE}.s04",
    stype="hands_on",
    concept_ids=["sql.where_filtering"],
    title="Write a WHERE filter in SQL",
    eyebrow="Practice",
    lede="Query the QuickCart orders table to return only the orders that exceed a delivery threshold.",
    reward={"gems": 10, "first_try_bonus": 5},
    lineage=lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f1")],
        anchors=[
            qid("sql.where_filtering", "practice"),
            qid("sql.where_filtering", "assessment:explain_which_rows_where_keeps"),
        ],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s05 — explainer: logical_operators (side_by_side visual)
# ─────────────────────────────────────────────────────────────────────────────
# side_by_side: without parentheses vs with parentheses
# Without: WHERE customer_id = 1 AND delivery_time_minutes > 30 OR customer_id = 2
# With:    WHERE customer_id = 1 AND (delivery_time_minutes > 30 OR customer_id = 2)

s05_left = data_table_result(
    block_id=f"{TILE}.s05.left",
    sql="SELECT order_id, customer_id, delivery_time_minutes FROM orders WHERE customer_id = 1 AND delivery_time_minutes > 30 OR customer_id = 2",
    asset_mounts=[{"asset_id": "ds_orders", "mount_path": "orders"}],
    caption="Without parentheses: AND binds first, then OR",
)

s05_right = data_table_result(
    block_id=f"{TILE}.s05.right",
    sql="SELECT order_id, customer_id, delivery_time_minutes FROM orders WHERE customer_id = 1 AND (delivery_time_minutes > 30 OR customer_id = 2)",
    asset_mounts=[{"asset_id": "ds_orders", "mount_path": "orders"}],
    caption="With parentheses: OR is evaluated first inside the group",
)

s05_side_by_side = {
    "type": "side_by_side",
    "block_id": f"{TILE}.s05.sbs",
    "left": s05_left,
    "right": s05_right,
    "left_label": "No parentheses",
    "right_label": "Parentheses around OR",
    "takeaway": "The same three conditions produce different result sets depending on where the parentheses go — AND always binds before OR unless you override it.",
    "lineage": lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f1"), qid("sql.logical_operators", "f2")],
        teaching_block_ids=[qid("sql.logical_operators", "tb2"), qid("sql.logical_operators", "tb3")],
        anchors=[qid("sql.logical_operators", "visual")],
    ),
}

s05_intro = prose(
    block_id=f"{TILE}.s05.p1",
    text=(
        "A WHERE clause often needs more than one condition at once — for example, "
        "orders from customer 1 that also took longer than 30 minutes. "
        "AND, OR, and NOT let you combine boolean conditions. "
        "AND is true only when both sides are true; OR is true when at least one side is true; "
        "NOT reverses a true or false value."
    ),
    role="definition",
    fact_ids=[qid("sql.logical_operators", "f1")],
    teaching_block_ids=[qid("sql.logical_operators", "tb1"), qid("sql.logical_operators", "tb2")],
    concept_ids=["sql.logical_operators"],
)

step_s05 = step(
    step_id=f"{TILE}.s05",
    stype="explainer",
    concept_ids=["sql.logical_operators"],
    title="Combining conditions with AND, OR, and NOT",
    eyebrow="Logical operators",
    lede="Join multiple filter conditions to express precise requirements.",
    blocks=[s05_intro, s05_side_by_side],
    reward={"gems": 5},
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f1")],
        teaching_block_ids=[
            qid("sql.logical_operators", "tb1"),
            qid("sql.logical_operators", "tb2"),
        ],
        anchors=[qid("sql.logical_operators", "visual")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s06 — explainer: logical_operators tb3 (precedence / parentheses)
# ─────────────────────────────────────────────────────────────────────────────
s06_p1 = prose(
    block_id=f"{TILE}.s06.p1",
    text=(
        "Without parentheses, NOT is evaluated before AND, and AND is evaluated before OR. "
        "WHERE customer_id = 1 AND delivery_time_minutes > 30 OR customer_id = 2 "
        "is read as (customer_id = 1 AND delivery_time_minutes > 30) OR customer_id = 2, "
        "which keeps any order from customer 2 regardless of delivery time."
    ),
    role="mechanism",
    fact_ids=[qid("sql.logical_operators", "f2")],
    teaching_block_ids=[qid("sql.logical_operators", "tb3")],
    concept_ids=["sql.logical_operators"],
)

s06_p2 = prose(
    block_id=f"{TILE}.s06.p2",
    text=(
        "Parentheses group expressions to force a different evaluation order. "
        "WHERE customer_id = 1 AND (delivery_time_minutes > 30 OR customer_id = 2) "
        "evaluates the OR first; because customer_id = 1 already rules out customer_id = 2, "
        "this version keeps only customer 1's orders that took longer than 30 minutes. "
        "NOT reverses a condition: WHERE NOT (customer_id = 1) keeps every order whose customer_id is not 1."
    ),
    role="mechanism",
    fact_ids=[qid("sql.logical_operators", "f2")],
    teaching_block_ids=[qid("sql.logical_operators", "tb3")],
    concept_ids=["sql.logical_operators"],
)

step_s06 = step(
    step_id=f"{TILE}.s06",
    stype="explainer",
    concept_ids=["sql.logical_operators"],
    title="Evaluation order and parentheses",
    eyebrow="Operator precedence",
    lede="NOT binds tightest, then AND, then OR — use parentheses to override.",
    blocks=[s06_p1, s06_p2],
    reward={"gems": 5},
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f2")],
        teaching_block_ids=[qid("sql.logical_operators", "tb3")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s07 — check: predict_result_of_unparenthesized_conditions (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s07 = step(
    step_id=f"{TILE}.s07",
    stype="check",
    concept_ids=["sql.logical_operators"],
    title="Predict the result of unparenthesized conditions",
    eyebrow="Quick check",
    lede="Trace the default evaluation order to predict which rows a query returns.",
    reward={"gems": 5, "first_try_bonus": 3},
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f2")],
        anchors=[qid("sql.logical_operators", "assessment:predict_result_of_unparenthesized_conditions")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s08 — check: use_parentheses_to_force_evaluation_order (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s08 = step(
    step_id=f"{TILE}.s08",
    stype="check",
    concept_ids=["sql.logical_operators"],
    title="Use parentheses to force evaluation order",
    eyebrow="Quick check",
    lede="Choose the version of the WHERE clause that uses parentheses to match the stated requirement.",
    reward={"gems": 5, "first_try_bonus": 3},
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f1"), qid("sql.logical_operators", "f2")],
        anchors=[qid("sql.logical_operators", "assessment:use_parentheses_to_force_evaluation_order")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s09 — hands_on: combine_conditions_with_and_or_not / practice (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s09 = step(
    step_id=f"{TILE}.s09",
    stype="hands_on",
    concept_ids=["sql.logical_operators"],
    title="Combine conditions with AND, OR, and parentheses",
    eyebrow="Practice",
    lede="Write a WHERE clause that combines conditions with AND and OR, using parentheses to match the requirement.",
    reward={"gems": 10, "first_try_bonus": 5},
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f1")],
        anchors=[
            qid("sql.logical_operators", "practice"),
            qid("sql.logical_operators", "assessment:combine_conditions_with_and_or_not"),
        ],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s10 — explainer: null_handling (before_after visual)
# ─────────────────────────────────────────────────────────────────────────────
# before: = NULL (returns no rows)
# after: IS NULL (returns rows 1011, 1012)

s10_before = data_table_result(
    block_id=f"{TILE}.s10.before",
    sql="SELECT order_id, customer_id, delivery_time_minutes FROM orders WHERE delivery_time_minutes = NULL",
    asset_mounts=[{"asset_id": "ds_orders", "mount_path": "orders"}],
    caption="WHERE delivery_time_minutes = NULL — returns no rows (= NULL never evaluates to true)",
)

s10_after = data_table_result(
    block_id=f"{TILE}.s10.after",
    sql="SELECT order_id, customer_id, delivery_time_minutes FROM orders WHERE delivery_time_minutes IS NULL",
    asset_mounts=[{"asset_id": "ds_orders", "mount_path": "orders"}],
    caption="WHERE delivery_time_minutes IS NULL — returns the two orders with a missing delivery time",
)

s10_before_after = {
    "type": "before_after",
    "block_id": f"{TILE}.s10.ba",
    "before": s10_before,
    "after": s10_after,
    "change_summary": "Replacing = NULL with IS NULL returns the rows with a missing delivery time; = NULL silently returns nothing because NULL is not considered equal to NULL.",
    "lineage": lineage(
        concept_ids=["sql.null_handling"],
        fact_ids=[
            qid("sql.null_handling", "f1"),
            qid("sql.null_handling", "f2"),
            qid("sql.null_handling", "m1"),
        ],
        teaching_block_ids=[
            qid("sql.null_handling", "tb2"),
            qid("sql.null_handling", "tb3"),
        ],
        anchors=[qid("sql.null_handling", "visual")],
    ),
}

s10_intro = prose(
    block_id=f"{TILE}.s10.p1",
    text=(
        "Some orders in the QuickCart database have no recorded delivery time — "
        "the value is missing, not zero. "
        "SQL represents a missing value with NULL. "
        "NULL means unknown: it is not known whether two unknown values are equal, "
        "so testing for NULL with an ordinary comparison operator does not work."
    ),
    role="intro",
    fact_ids=[qid("sql.null_handling", "f1")],
    teaching_block_ids=[qid("sql.null_handling", "tb1")],
    concept_ids=["sql.null_handling"],
)

s10_definition = prose(
    block_id=f"{TILE}.s10.p2",
    text=(
        "To test whether a value is or is not null, use the predicates IS NULL and IS NOT NULL. "
        "WHERE delivery_time_minutes IS NULL finds the orders with a missing delivery time; "
        "WHERE delivery_time_minutes IS NOT NULL finds the rest."
    ),
    role="definition",
    fact_ids=[qid("sql.null_handling", "f2")],
    teaching_block_ids=[qid("sql.null_handling", "tb2")],
    concept_ids=["sql.null_handling"],
)

s10_misconception = prose(
    block_id=f"{TILE}.s10.p3",
    text=(
        "Writing WHERE delivery_time_minutes = NULL does not test for null. "
        "NULL is not considered 'equal to' NULL, so that comparison never evaluates to true, "
        "and the query silently returns zero rows instead of the missing-time orders you meant to find."
    ),
    role="misconception",
    fact_ids=[qid("sql.null_handling", "m1")],
    teaching_block_ids=[qid("sql.null_handling", "tb3")],
    concept_ids=["sql.null_handling"],
)

step_s10 = step(
    step_id=f"{TILE}.s10",
    stype="explainer",
    concept_ids=["sql.null_handling"],
    title="Testing for missing values with IS NULL",
    eyebrow="NULL handling",
    lede="Missing values are unknown — use IS NULL and IS NOT NULL, never = NULL.",
    blocks=[s10_intro, s10_definition, s10_misconception, s10_before_after],
    reward={"gems": 5},
    lineage=lineage(
        concept_ids=["sql.null_handling"],
        fact_ids=[
            qid("sql.null_handling", "f1"),
            qid("sql.null_handling", "f2"),
            qid("sql.null_handling", "m1"),
        ],
        teaching_block_ids=[
            qid("sql.null_handling", "tb1"),
            qid("sql.null_handling", "tb2"),
            qid("sql.null_handling", "tb3"),
        ],
        anchors=[qid("sql.null_handling", "visual")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s11 — video: null_handling segment
# ─────────────────────────────────────────────────────────────────────────────
step_s11 = step(
    step_id=f"{TILE}.s11",
    stype="video",
    concept_ids=["sql.null_handling"],
    title="Testing for missing values (video)",
    eyebrow="Watch",
    lede="See IS NULL and IS NOT NULL in action on a live query.",
    blocks=[
        {
            "type": "media_group",
            "block_id": f"{TILE}.s11.mg",
            "segment_ids": ["seg_sql.null_handling_X_cPXHV2NQ4_2574_2798"],
        }
    ],
    lineage=lineage(
        concept_ids=["sql.null_handling"],
        fact_ids=[qid("sql.null_handling", "f2")],
        segment_ids=["seg_sql.null_handling_X_cPXHV2NQ4_2574_2798"],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s12 — check: explain_why_equals_null_never_matches (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s12 = step(
    step_id=f"{TILE}.s12",
    stype="check",
    concept_ids=["sql.null_handling"],
    title="Why does = NULL never match?",
    eyebrow="Quick check",
    lede="Explain why a query with = NULL returns no rows.",
    reward={"gems": 5, "first_try_bonus": 3},
    lineage=lineage(
        concept_ids=["sql.null_handling"],
        fact_ids=[qid("sql.null_handling", "f1"), qid("sql.null_handling", "m1")],
        anchors=[qid("sql.null_handling", "assessment:explain_why_equals_null_never_matches")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s13 — hands_on: write_is_null_and_is_not_null_filters / practice (framing only)
# ─────────────────────────────────────────────────────────────────────────────
step_s13 = step(
    step_id=f"{TILE}.s13",
    stype="hands_on",
    concept_ids=["sql.null_handling"],
    title="Write IS NULL and IS NOT NULL filters",
    eyebrow="Practice",
    lede="Query the orders table to find rows with a missing delivery time, then rows where it is present.",
    reward={"gems": 10, "first_try_bonus": 5},
    lineage=lineage(
        concept_ids=["sql.null_handling"],
        fact_ids=[qid("sql.null_handling", "f2")],
        anchors=[
            qid("sql.null_handling", "practice"),
            qid("sql.null_handling", "assessment:write_is_null_and_is_not_null_filters"),
        ],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# STEP s14 — recap
# ─────────────────────────────────────────────────────────────────────────────
s14_takeaway = prose(
    block_id=f"{TILE}.s14.p1",
    text=(
        "WHERE evaluates a condition for every row and keeps only those where it is true. "
        "Comparison operators (<, >, <=, >=, =, <>) produce the boolean result. "
        "AND, OR, and NOT combine conditions; AND binds before OR unless you add parentheses. "
        "NULL means unknown — use IS NULL or IS NOT NULL to test for missing values; = NULL never matches."
    ),
    role="takeaway",
    fact_ids=[
        qid("sql.where_filtering", "f1"),
        qid("sql.where_filtering", "f2"),
    ],
    teaching_block_ids=[qid("sql.where_filtering", "tb4")],
    concept_ids=["sql.where_filtering", "sql.logical_operators", "sql.null_handling"],
)

s14_up_next = {
    "type": "up_next",
    "block_id": f"{TILE}.s14.un",
    "title": "Next: Sorting Results with ORDER BY",
    "text": (
        "WHERE decides which rows come back, but not what order they appear in. "
        "Next you will use ORDER BY to sort results from slowest to fastest delivery — "
        "or any other direction you need."
    ),
}

step_s14 = step(
    step_id=f"{TILE}.s14",
    stype="recap",
    concept_ids=["sql.where_filtering", "sql.logical_operators", "sql.null_handling"],
    title="Recap: Filtering Rows",
    eyebrow="Recap",
    lede="Three tools for precise row selection: WHERE, logical operators, and IS NULL.",
    blocks=[s14_takeaway, s14_up_next],
    reward={"gems": 5},
    lineage=lineage(
        concept_ids=["sql.where_filtering", "sql.logical_operators", "sql.null_handling"],
        fact_ids=[
            qid("sql.where_filtering", "f1"),
            qid("sql.where_filtering", "f2"),
        ],
        teaching_block_ids=[qid("sql.where_filtering", "tb4")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# REMEDIATION STEPS
# Rule: first check/hands_on of each concept gets a remediation step.
# s02 = first check for sql.where_filtering (measures f2)
# s03 = second check for sql.where_filtering (measures f1, f2) — different facts → own remediation
# s04 = first hands_on for sql.where_filtering (measures f1)
# s07 = first check for sql.logical_operators (measures f2)
# s08 = second check for sql.logical_operators (measures f1, f2) — different facts → own remediation
# s09 = first hands_on for sql.logical_operators (measures f1)
# s12 = first check for sql.null_handling (measures f1, m1)
# s13 = first hands_on for sql.null_handling (measures f2)
# ─────────────────────────────────────────────────────────────────────────────

# r01: remediation for s02 (choose_the_right_comparison_operator → f2)
rem_r01 = step(
    step_id=f"{TILE}.r01",
    stype="remediation",
    concept_ids=["sql.where_filtering"],
    title="Comparison operators: which one to use",
    eyebrow="Let's review",
    lede="Each comparison operator tests a different relationship between two values.",
    blocks=[
        prose(
            block_id=f"{TILE}.r01.p1",
            text=(
                "The six comparison operators are <, >, <=, >=, =, and <>. "
                "= tests whether two values are equal; <> (or !=) tests whether they are not equal. "
                "< and > test strict less-than and greater-than; <= and >= include the boundary value. "
                "WHERE delivery_time_minutes > 40 keeps rows where the time is strictly above 40; "
                "WHERE delivery_time_minutes >= 40 would also keep a row with exactly 40 minutes."
            ),
            role="syntax",
            fact_ids=[qid("sql.where_filtering", "f2")],
            teaching_block_ids=[qid("sql.where_filtering", "tb3")],
            concept_ids=["sql.where_filtering"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f2")],
        teaching_block_ids=[qid("sql.where_filtering", "tb3")],
    ),
)

# r02: remediation for s03 (write_where_for_a_filter_requirement → f1, f2)
rem_r02 = step(
    step_id=f"{TILE}.r02",
    stype="remediation",
    concept_ids=["sql.where_filtering"],
    title="How WHERE evaluates each row",
    eyebrow="Let's review",
    lede="WHERE tests the condition against every row and keeps only those where it is true.",
    blocks=[
        prose(
            block_id=f"{TILE}.r02.p1",
            text=(
                "WHERE takes a search condition and evaluates it for each row in the table. "
                "A row is kept only if the condition evaluates to true; rows where it is false are discarded. "
                "SELECT order_id FROM orders WHERE customer_id = 2 keeps only the rows where customer_id equals 2 "
                "and discards every other row."
            ),
            role="definition",
            fact_ids=[qid("sql.where_filtering", "f1"), qid("sql.where_filtering", "f2")],
            teaching_block_ids=[qid("sql.where_filtering", "tb2"), qid("sql.where_filtering", "tb3")],
            concept_ids=["sql.where_filtering"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f1"), qid("sql.where_filtering", "f2")],
        teaching_block_ids=[qid("sql.where_filtering", "tb2"), qid("sql.where_filtering", "tb3")],
    ),
)

# r03: remediation for s04 (explain_which_rows_where_keeps → f1)
rem_r03 = step(
    step_id=f"{TILE}.r03",
    stype="remediation",
    concept_ids=["sql.where_filtering"],
    title="Which rows does WHERE keep?",
    eyebrow="Let's review",
    lede="WHERE keeps a row only when the condition is true for that row.",
    blocks=[
        prose(
            block_id=f"{TILE}.r03.p1",
            text=(
                "Think of WHERE as a row-by-row question: for each row, is this condition true? "
                "If yes, the row appears in the result. If no, it is discarded. "
                "WHERE delivery_time_minutes > 40 asks that question for every order in the QuickCart table "
                "and returns only the orders where the delivery time is above 40 minutes."
            ),
            role="mechanism",
            fact_ids=[qid("sql.where_filtering", "f1")],
            teaching_block_ids=[qid("sql.where_filtering", "tb2")],
            concept_ids=["sql.where_filtering"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.where_filtering"],
        fact_ids=[qid("sql.where_filtering", "f1")],
        teaching_block_ids=[qid("sql.where_filtering", "tb2")],
    ),
)

# r04: remediation for s07 (predict_result_of_unparenthesized_conditions → f2)
rem_r04 = step(
    step_id=f"{TILE}.r04",
    stype="remediation",
    concept_ids=["sql.logical_operators"],
    title="Default evaluation order: NOT, then AND, then OR",
    eyebrow="Let's review",
    lede="Without parentheses, AND always binds before OR — which can change the rows you get.",
    blocks=[
        prose(
            block_id=f"{TILE}.r04.p1",
            text=(
                "When you write multiple conditions without parentheses, SQL evaluates NOT first, then AND, then OR. "
                "WHERE customer_id = 1 AND delivery_time_minutes > 30 OR customer_id = 2 "
                "is treated as (customer_id = 1 AND delivery_time_minutes > 30) OR customer_id = 2. "
                "That keeps every order from customer 2, regardless of delivery time — "
                "which may not be what you intended."
            ),
            role="mechanism",
            fact_ids=[qid("sql.logical_operators", "f2")],
            teaching_block_ids=[qid("sql.logical_operators", "tb3")],
            concept_ids=["sql.logical_operators"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f2")],
        teaching_block_ids=[qid("sql.logical_operators", "tb3")],
    ),
)

# r05: remediation for s08 (use_parentheses_to_force_evaluation_order → f1, f2)
rem_r05 = step(
    step_id=f"{TILE}.r05",
    stype="remediation",
    concept_ids=["sql.logical_operators"],
    title="Using parentheses to control AND/OR grouping",
    eyebrow="Let's review",
    lede="Parentheses override the default precedence so the OR is evaluated where you need it.",
    blocks=[
        prose(
            block_id=f"{TILE}.r05.p1",
            text=(
                "AND, OR, and NOT combine boolean conditions. "
                "AND is true only when both sides are true; OR is true when at least one side is true. "
                "By default AND binds before OR. "
                "Adding parentheses forces the OR to be evaluated first: "
                "WHERE customer_id = 1 AND (delivery_time_minutes > 30 OR customer_id = 2) "
                "evaluates the OR group first, then applies the AND — giving a different result set."
            ),
            role="mechanism",
            fact_ids=[qid("sql.logical_operators", "f1"), qid("sql.logical_operators", "f2")],
            teaching_block_ids=[qid("sql.logical_operators", "tb2"), qid("sql.logical_operators", "tb3")],
            concept_ids=["sql.logical_operators"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f1"), qid("sql.logical_operators", "f2")],
        teaching_block_ids=[qid("sql.logical_operators", "tb2"), qid("sql.logical_operators", "tb3")],
    ),
)

# r06: remediation for s09 (combine_conditions_with_and_or_not → f1)
rem_r06 = step(
    step_id=f"{TILE}.r06",
    stype="remediation",
    concept_ids=["sql.logical_operators"],
    title="AND, OR, and NOT: combining conditions",
    eyebrow="Let's review",
    lede="Use AND to require both conditions, OR to accept either, and NOT to exclude.",
    blocks=[
        prose(
            block_id=f"{TILE}.r06.p1",
            text=(
                "AND requires both conditions to be true: "
                "WHERE customer_id = 1 AND delivery_time_minutes > 30 keeps only customer 1's slow orders. "
                "OR accepts either: WHERE customer_id = 1 OR customer_id = 2 keeps orders from either customer. "
                "NOT reverses a condition: WHERE NOT (customer_id = 1) keeps every order that is not from customer 1."
            ),
            role="definition",
            fact_ids=[qid("sql.logical_operators", "f1")],
            teaching_block_ids=[qid("sql.logical_operators", "tb2")],
            concept_ids=["sql.logical_operators"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.logical_operators"],
        fact_ids=[qid("sql.logical_operators", "f1")],
        teaching_block_ids=[qid("sql.logical_operators", "tb2")],
    ),
)

# r07: remediation for s12 (explain_why_equals_null_never_matches → f1, m1)
rem_r07 = step(
    step_id=f"{TILE}.r07",
    stype="remediation",
    concept_ids=["sql.null_handling"],
    title="Why = NULL never matches",
    eyebrow="Let's review",
    lede="NULL means unknown — and an unknown value is not considered equal to anything, including another unknown.",
    blocks=[
        prose(
            block_id=f"{TILE}.r07.p1",
            text=(
                "NULL represents an unknown value. "
                "It is not known whether two unknown values are equal, "
                "so the comparison delivery_time_minutes = NULL never evaluates to true — "
                "not even when the value is actually missing. "
                "The query runs without error but silently returns zero rows, "
                "which is not what you want when looking for missing delivery times."
            ),
            role="misconception",
            fact_ids=[qid("sql.null_handling", "f1"), qid("sql.null_handling", "m1")],
            teaching_block_ids=[qid("sql.null_handling", "tb1"), qid("sql.null_handling", "tb3")],
            concept_ids=["sql.null_handling"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.null_handling"],
        fact_ids=[qid("sql.null_handling", "f1"), qid("sql.null_handling", "m1")],
        teaching_block_ids=[qid("sql.null_handling", "tb1"), qid("sql.null_handling", "tb3")],
    ),
)

# r08: remediation for s13 (write_is_null_and_is_not_null_filters → f2)
rem_r08 = step(
    step_id=f"{TILE}.r08",
    stype="remediation",
    concept_ids=["sql.null_handling"],
    title="IS NULL and IS NOT NULL: the right predicates",
    eyebrow="Let's review",
    lede="Use IS NULL to find missing values and IS NOT NULL to find present ones.",
    blocks=[
        prose(
            block_id=f"{TILE}.r08.p1",
            text=(
                "To test whether a value is missing, use IS NULL. "
                "To test whether a value is present, use IS NOT NULL. "
                "WHERE delivery_time_minutes IS NULL returns the orders with no recorded delivery time; "
                "WHERE delivery_time_minutes IS NOT NULL returns the orders that do have one. "
                "Together these two predicates cover the whole table."
            ),
            role="definition",
            fact_ids=[qid("sql.null_handling", "f2")],
            teaching_block_ids=[qid("sql.null_handling", "tb2")],
            concept_ids=["sql.null_handling"],
        ),
    ],
    lineage=lineage(
        concept_ids=["sql.null_handling"],
        fact_ids=[qid("sql.null_handling", "f2")],
        teaching_block_ids=[qid("sql.null_handling", "tb2")],
    ),
)

# ─────────────────────────────────────────────────────────────────────────────
# Assemble tile
# ─────────────────────────────────────────────────────────────────────────────
tile = {
    "tile_id": TILE,
    "title": "Filtering Rows with WHERE and Logical Operators",
    "summary": (
        "Learn to filter query results with WHERE, combine conditions using AND, OR, and NOT, "
        "control evaluation order with parentheses, and test for missing values with IS NULL."
    ),
    "steps": [
        step_s01,
        step_s02,
        step_s03,
        step_s04,
        step_s05,
        step_s06,
        step_s07,
        step_s08,
        step_s09,
        step_s10,
        step_s11,
        step_s12,
        step_s13,
        step_s14,
    ],
    "remediation_steps": [
        rem_r01,
        rem_r02,
        rem_r03,
        rem_r04,
        rem_r05,
        rem_r06,
        rem_r07,
        rem_r08,
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# Final document
# ─────────────────────────────────────────────────────────────────────────────
doc = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_006_da_sql_rest",
    "tiles": [tile],
}

out_path = "batches/final_batch_006_da_sql_rest/screens.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(doc, f, indent=2)

print(f"Written: {out_path}")
print(f"Steps: {len(tile['steps'])}")
print(f"Remediation steps: {len(tile['remediation_steps'])}")
