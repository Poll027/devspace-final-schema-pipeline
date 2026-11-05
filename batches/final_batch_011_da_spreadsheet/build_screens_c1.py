#!/usr/bin/env python3
"""Build screens.part.c1.json for tile_spreadsheet_formula_syntax_refs,
tile_spreadsheet_aggregation_logical, tile_spreadsheet_text_date_conditional_agg."""

import json, textwrap

OUT = "batches/final_batch_011_da_spreadsheet/screens.part.c1.json"

# ── helpers ──────────────────────────────────────────────────────────────────

def prose(block_id, text, role, concept_ids, fact_ids, teaching_block_ids, anchors=None):
    b = {
        "type": "prose",
        "block_id": block_id,
        "text": text,
        "role": role,
        "lineage": {
            "concept_ids": concept_ids,
            "fact_ids": fact_ids,
            "teaching_block_ids": teaching_block_ids,
        }
    }
    if anchors:
        b["lineage"]["anchors"] = anchors
    return b

def heading(block_id, text):
    return {"type": "heading", "block_id": block_id, "text": text}

def media_group(block_id, segment_ids):
    return {
        "type": "media_group",
        "block_id": block_id,
        "segment_ids": segment_ids,
    }

def spreadsheet_grid(block_id, asset_id, sheet_name, rng, show_formula_bar,
                     cells=None, annotations=None, selection=None,
                     concept_ids=None, fact_ids=None, teaching_block_ids=None, anchors=None):
    b = {
        "type": "spreadsheet_grid",
        "block_id": block_id,
        "asset_ref": {"asset_id": asset_id},
        "range": rng,
    }
    if sheet_name:
        b["sheet_name"] = sheet_name
    if show_formula_bar is not None:
        b["show_formula_bar"] = show_formula_bar
    if cells:
        b["cells"] = cells
    if annotations:
        b["annotations"] = annotations
    if selection:
        b["selection"] = selection
    lin = {}
    if concept_ids:
        lin["concept_ids"] = concept_ids
    if fact_ids:
        lin["fact_ids"] = fact_ids
    if teaching_block_ids:
        lin["teaching_block_ids"] = teaching_block_ids
    if anchors:
        lin["anchors"] = anchors
    if lin:
        b["lineage"] = lin
    return b

def before_after(block_id, before_block, after_block, change_summary,
                 concept_ids=None, fact_ids=None, teaching_block_ids=None, anchors=None):
    b = {
        "type": "before_after",
        "block_id": block_id,
        "before": before_block,
        "after": after_block,
        "change_summary": change_summary,
    }
    lin = {}
    if concept_ids:
        lin["concept_ids"] = concept_ids
    if fact_ids:
        lin["fact_ids"] = fact_ids
    if teaching_block_ids:
        lin["teaching_block_ids"] = teaching_block_ids
    if anchors:
        lin["anchors"] = anchors
    if lin:
        b["lineage"] = lin
    return b

def side_by_side(block_id, left_block, right_block, left_label, right_label, takeaway,
                 concept_ids=None, fact_ids=None, teaching_block_ids=None, anchors=None):
    b = {
        "type": "side_by_side",
        "block_id": block_id,
        "left": left_block,
        "right": right_block,
        "left_label": left_label,
        "right_label": right_label,
        "takeaway": takeaway,
    }
    lin = {}
    if concept_ids:
        lin["concept_ids"] = concept_ids
    if fact_ids:
        lin["fact_ids"] = fact_ids
    if teaching_block_ids:
        lin["teaching_block_ids"] = teaching_block_ids
    if anchors:
        lin["anchors"] = anchors
    if lin:
        b["lineage"] = lin
    return b

def up_next(block_id, title, text):
    return {"type": "up_next", "block_id": block_id, "title": title, "text": text}

def step(step_id, stype, concept_ids, title, blocks, lineage,
         eyebrow=None, lede=None, reward=None):
    s = {
        "step_id": step_id,
        "type": stype,
        "concept_ids": concept_ids,
        "title": title,
        "blocks": blocks,
        "lineage": lineage,
    }
    if eyebrow:
        s["eyebrow"] = eyebrow
    if lede:
        s["lede"] = lede
    if reward:
        s["reward"] = reward
    return s

def check_step(step_id, concept_ids, title, lineage, eyebrow=None, lede=None, reward=None):
    """check/hands_on steps carry framing only — no blocks."""
    s = {
        "step_id": step_id,
        "type": "check",
        "concept_ids": concept_ids,
        "title": title,
        "lineage": lineage,
    }
    if eyebrow:
        s["eyebrow"] = eyebrow
    if lede:
        s["lede"] = lede
    if reward:
        s["reward"] = reward
    return s

def hands_on_step(step_id, concept_ids, title, lineage, eyebrow=None, lede=None, reward=None):
    s = {
        "step_id": step_id,
        "type": "hands_on",
        "concept_ids": concept_ids,
        "title": title,
        "lineage": lineage,
    }
    if eyebrow:
        s["eyebrow"] = eyebrow
    if lede:
        s["lede"] = lede
    if reward:
        s["reward"] = reward
    return s

def remediation_step(step_id, concept_ids, title, blocks, lineage, eyebrow=None, lede=None):
    s = {
        "step_id": step_id,
        "type": "remediation",
        "concept_ids": concept_ids,
        "title": title,
        "blocks": blocks,
        "lineage": lineage,
    }
    if eyebrow:
        s["eyebrow"] = eyebrow
    if lede:
        s["lede"] = lede
    return s

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 1: tile_spreadsheet_formula_syntax_refs
# ═══════════════════════════════════════════════════════════════════════════════

T1 = "tile_spreadsheet_formula_syntax_refs"
FS = "spreadsheet.formula_syntax"
RAR = "spreadsheet.relative_absolute_references"

t1_steps = []

# s01 — explainer: formula_syntax tb1+tb2+tb3+tb4, f1+f2+f3+f4, visual=spreadsheet_grid
t1_steps.append(step(
    step_id=f"{T1}.s01",
    stype="explainer",
    concept_ids=[FS],
    eyebrow="Formula Syntax",
    title="Every Formula Starts with =",
    lede="A formula turns a cell into a calculator — here's the pattern every formula follows.",
    blocks=[
        prose(
            f"{T1}.s01.b1",
            "In your QuickDeliver Orders sheet, most cells hold plain values — an amount, a city, a date. "
            "A formula changes that: it tells Excel to compute a result instead. "
            "Every formula begins with the equal sign (=). Without it, Excel treats the entry as text.",
            "intro",
            [FS], [f"{FS}#f1"], [f"{FS}#tb1", f"{FS}#tb2"]
        ),
        prose(
            f"{T1}.s01.b2",
            "Excel's four arithmetic operators are + (addition), - (subtraction), * (multiplication), "
            "and / (division). You can combine them with literal numbers or cell addresses: "
            "=D3-D2 subtracts one order's amount from another; =D2*2 doubles it. "
            "To reference another cell, type its address after the = and operator.",
            "definition",
            [FS], [f"{FS}#f2", f"{FS}#f4"], [f"{FS}#tb2", f"{FS}#tb3"]
        ),
        prose(
            f"{T1}.s01.b3",
            "Built-in functions follow the same = prefix but add a name and parentheses: "
            "=SUM(D2:D51) totals every amount in that range of your Orders sheet. "
            "Type =, the function name, an opening parenthesis, select the range, close the parenthesis, "
            "then press Enter. The cell shows the computed result.",
            "syntax",
            [FS], [f"{FS}#f3"], [f"{FS}#tb4"]
        ),
        spreadsheet_grid(
            f"{T1}.s01.b4",
            "asset_orders_clean",
            "Orders",
            "A1:E4",
            True,
            cells=[
                {"ref": "F2", "formula": "=D3-D2", "note": "Difference between two amounts"},
                {"ref": "F3", "formula": "=SUM(D2:D21)", "note": "Total of all amounts"},
            ],
            annotations=[
                {"target": "F2", "text": "= prefix + cell refs + operator"},
                {"target": "F3", "text": "= prefix + function name + range"},
            ],
            concept_ids=[FS],
            fact_ids=[f"{FS}#f1", f"{FS}#f2", f"{FS}#f3", f"{FS}#f4"],
            teaching_block_ids=[f"{FS}#tb2", f"{FS}#tb3", f"{FS}#tb4"],
            anchors=[f"{FS}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f1", f"{FS}#f2", f"{FS}#f3", f"{FS}#f4"],
        "teaching_block_ids": [f"{FS}#tb1", f"{FS}#tb2", f"{FS}#tb3", f"{FS}#tb4"],
        "anchors": [f"{FS}#visual"],
    },
    reward={"gems": 5}
))

# s02 — video: formula_syntax
t1_steps.append(step(
    step_id=f"{T1}.s02",
    stype="video",
    concept_ids=[FS],
    eyebrow="Formula Syntax",
    title="Formulas in Action",
    blocks=[
        media_group(
            f"{T1}.s02.b1",
            [
                "seg_spreadsheet.formula_syntax_gvhsKtjAmgc_311_418",
                "seg_spreadsheet.formula_syntax_XRPyj7cKVsQ_151_220",
            ]
        ),
    ],
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f1", f"{FS}#f2", f"{FS}#f3"],
        "teaching_block_ids": [],
        "segment_ids": [
            "seg_spreadsheet.formula_syntax_gvhsKtjAmgc_311_418",
            "seg_spreadsheet.formula_syntax_XRPyj7cKVsQ_151_220",
        ],
    }
))

# s03 — explainer: formula_syntax tb5, f5 (operator precedence)
t1_steps.append(step(
    step_id=f"{T1}.s03",
    stype="explainer",
    concept_ids=[FS],
    eyebrow="Formula Syntax",
    title="Operator Precedence and Parentheses",
    lede="Multiplication runs before addition — unless you use parentheses.",
    blocks=[
        prose(
            f"{T1}.s03.b1",
            "Excel evaluates multiplication and division before addition and subtraction. "
            "=5+2*3 gives 11, not 21. Wrap the addition in parentheses — =(5+2)*3 — to get 21. "
            "Whenever a formula mixes operators, check the order or add parentheses to be explicit.",
            "mechanism",
            [FS], [f"{FS}#f5"], [f"{FS}#tb5"]
        ),
    ],
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f5"],
        "teaching_block_ids": [f"{FS}#tb5"],
    },
    reward={"gems": 3}
))

# s04 — check: formula_syntax f1
t1_steps.append(check_step(
    step_id=f"{T1}.s04",
    concept_ids=[FS],
    eyebrow="Quick Check",
    title="The Required Formula Prefix",
    lede="Which character must every Excel formula begin with?",
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f1"],
        "teaching_block_ids": [],
        "anchors": [f"{FS}#assessment:identify_required_equal_sign_prefix"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s05 — check: formula_syntax f3
t1_steps.append(check_step(
    step_id=f"{T1}.s05",
    concept_ids=[FS],
    eyebrow="Quick Check",
    title="Writing a Function Formula",
    lede="Which formula correctly sums the range C2:C21 on the Orders sheet?",
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f3"],
        "teaching_block_ids": [],
        "anchors": [f"{FS}#assessment:construct_function_call_formula_with_range"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s06 — hands_on: formula_syntax f1+f2+f3+f4+f5
t1_steps.append(hands_on_step(
    step_id=f"{T1}.s06",
    concept_ids=[FS],
    eyebrow="Practice",
    title="Write Formulas on the Orders Sheet",
    lede="Apply arithmetic operators, cell references, and a function call to the QuickDeliver data.",
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f1", f"{FS}#f2", f"{FS}#f3", f"{FS}#f4", f"{FS}#f5"],
        "teaching_block_ids": [],
        "anchors": [
            f"{FS}#practice",
            f"{FS}#assessment:apply_arithmetic_operators_in_formula",
            f"{FS}#assessment:build_cell_reference_formula_with_operator",
            f"{FS}#assessment:apply_operator_precedence_and_parentheses",
            f"{FS}#assessment:write_syntactically_correct_formula_for_given_computation",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s07 — explainer: relative_absolute_references tb1+tb2+tb3, f1+f2, visual=before_after
t1_steps.append(step(
    step_id=f"{T1}.s07",
    stype="explainer",
    concept_ids=[RAR],
    eyebrow="Reference Types",
    title="Relative and Absolute References",
    lede="Copy a formula down a column and watch which parts shift — and which stay fixed.",
    blocks=[
        prose(
            f"{T1}.s07.b1",
            "A relative reference such as D2 is position-based: copy the formula one row down "
            "and D2 becomes D3 automatically. By default, every new formula uses relative references. "
            "This is what you want when each row should calculate against its own data.",
            "definition",
            [RAR], [f"{RAR}#f1"], [f"{RAR}#tb1", f"{RAR}#tb2"]
        ),
        prose(
            f"{T1}.s07.b2",
            "An absolute reference such as $H$1 always points to the same cell, no matter where "
            "you copy the formula. Dollar signs lock both the column letter and the row number. "
            "If a delivery fee rate lives in H1, =D2*$H$1 copied down every order row keeps "
            "pointing to H1 for the rate while D2 shifts to D3, D4, and so on.",
            "mechanism",
            [RAR], [f"{RAR}#f2"], [f"{RAR}#tb3"]
        ),
        before_after(
            f"{T1}.s07.b3",
            before_block=spreadsheet_grid(
                f"{T1}.s07.b3.before",
                "asset_orders_clean",
                "Orders",
                "D2:H5",
                True,
                cells=[{"ref": "H2", "formula": "=D2*$H$1", "note": "Original formula in row 2"}],
                annotations=[{"target": "H2", "text": "=D2*$H$1 — D2 is relative, $H$1 is absolute"}]
            ),
            after_block=spreadsheet_grid(
                f"{T1}.s07.b3.after",
                "asset_orders_clean",
                "Orders",
                "D2:H5",
                True,
                cells=[
                    {"ref": "H2", "formula": "=D2*$H$1"},
                    {"ref": "H3", "formula": "=D3*$H$1"},
                    {"ref": "H4", "formula": "=D4*$H$1"},
                ],
                annotations=[{"target": "H3", "text": "D3 shifted; $H$1 unchanged"}]
            ),
            change_summary="After copying H2 down to H3 and H4, the relative part (D2→D3→D4) adjusts while the absolute part ($H$1) stays fixed.",
            concept_ids=[RAR],
            fact_ids=[f"{RAR}#f1", f"{RAR}#f2"],
            teaching_block_ids=[f"{RAR}#tb2", f"{RAR}#tb3"],
            anchors=[f"{RAR}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [RAR],
        "fact_ids": [f"{RAR}#f1", f"{RAR}#f2"],
        "teaching_block_ids": [f"{RAR}#tb1", f"{RAR}#tb2", f"{RAR}#tb3"],
        "anchors": [f"{RAR}#visual"],
    },
    reward={"gems": 5}
))

# s08 — video: relative_absolute_references
t1_steps.append(step(
    step_id=f"{T1}.s08",
    stype="video",
    concept_ids=[RAR],
    eyebrow="Reference Types",
    title="Watching References Shift (or Stay Fixed)",
    blocks=[
        media_group(
            f"{T1}.s08.b1",
            ["seg_spreadsheet.relative_absolute_references_4MVNjzsGokc_31_338"]
        ),
    ],
    lineage={
        "concept_ids": [RAR],
        "fact_ids": [f"{RAR}#f1", f"{RAR}#f2", f"{RAR}#f3"],
        "teaching_block_ids": [],
        "segment_ids": ["seg_spreadsheet.relative_absolute_references_4MVNjzsGokc_31_338"],
    }
))

# s09 — explainer: relative_absolute_references tb4, f3 (mixed references)
t1_steps.append(step(
    step_id=f"{T1}.s09",
    stype="explainer",
    concept_ids=[RAR],
    eyebrow="Reference Types",
    title="Mixed References: Lock One Dimension",
    lede="Lock just the column or just the row — not both.",
    blocks=[
        prose(
            f"{T1}.s09.b1",
            "A mixed reference locks only one dimension. $A1 locks the column (A stays, row shifts); "
            "A$1 locks the row (1 stays, column shifts). Use a mixed reference when copying a formula "
            "across both rows and columns and only one axis should stay fixed.",
            "mechanism",
            [RAR], [f"{RAR}#f3"], [f"{RAR}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [RAR],
        "fact_ids": [f"{RAR}#f3"],
        "teaching_block_ids": [f"{RAR}#tb4"],
    },
    reward={"gems": 3}
))

# s10 — check: relative_absolute_references f3
t1_steps.append(check_step(
    step_id=f"{T1}.s10",
    concept_ids=[RAR],
    eyebrow="Quick Check",
    title="Constructing a Mixed Reference",
    lede="Which reference locks the column but lets the row shift when copied down?",
    lineage={
        "concept_ids": [RAR],
        "fact_ids": [f"{RAR}#f3"],
        "teaching_block_ids": [],
        "anchors": [f"{RAR}#assessment:construct_mixed_reference_locking_one_dimension"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s11 — hands_on: relative_absolute_references f1+f2+f3
t1_steps.append(hands_on_step(
    step_id=f"{T1}.s11",
    concept_ids=[RAR],
    eyebrow="Practice",
    title="Apply Reference Types to the Orders Sheet",
    lede="Choose the right reference type for each copy scenario.",
    lineage={
        "concept_ids": [RAR],
        "fact_ids": [f"{RAR}#f1", f"{RAR}#f2", f"{RAR}#f3"],
        "teaching_block_ids": [],
        "anchors": [
            f"{RAR}#practice",
            f"{RAR}#assessment:identify_relative_reference_adjustment_on_copy",
            f"{RAR}#assessment:apply_absolute_reference_to_fix_cell_on_copy",
            f"{RAR}#assessment:select_correct_reference_type_for_copy_scenario",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s12 — recap
t1_steps.append(step(
    step_id=f"{T1}.s12",
    stype="recap",
    concept_ids=[FS, RAR],
    eyebrow="Recap",
    title="Formulas and Reference Types — Key Takeaways",
    blocks=[
        prose(
            f"{T1}.s12.b1",
            "Every formula starts with =, combines cell references and operators or a function call, "
            "and follows Excel's precedence rules unless parentheses override them. "
            "Relative references shift when copied; absolute references ($A$1) stay fixed; "
            "mixed references lock one dimension. That combination is the basis for every "
            "calculation you'll write in a spreadsheet.",
            "takeaway",
            [FS, RAR],
            [f"{FS}#f1", f"{FS}#f2", f"{FS}#f3", f"{FS}#f4", f"{FS}#f5"],
            [f"{FS}#tb6"]
        ),
        up_next(
            f"{T1}.s12.b2",
            "Up Next: Aggregation Functions",
            "In the next tile you'll use SUM, AVERAGE, COUNT, and COUNTA to summarise "
            "the entire Orders column in a single formula."
        ),
    ],
    lineage={
        "concept_ids": [FS, RAR],
        "fact_ids": [f"{FS}#f1", f"{FS}#f2", f"{FS}#f3", f"{FS}#f4", f"{FS}#f5"],
        "teaching_block_ids": [f"{FS}#tb6"],
    },
    reward={"gems": 5}
))

# ── Remediation steps for tile 1 ─────────────────────────────────────────────

t1_remediation = []

# r01 — remediation for s04 (check on f1: equal sign prefix)
t1_remediation.append(remediation_step(
    step_id=f"{T1}.r01",
    concept_ids=[FS],
    eyebrow="Let's Revisit",
    title="Why the = Sign Matters",
    blocks=[
        prose(
            f"{T1}.r01.b1",
            "Excel distinguishes a formula from plain text by the leading = sign. "
            "Type 5+2 and Excel stores the text '5+2'. Type =5+2 and Excel computes 7. "
            "Every formula — whether it uses arithmetic operators or a function like SUM — "
            "must start with =.",
            "definition",
            [FS], [f"{FS}#f1"], [f"{FS}#tb2"]
        ),
    ],
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f1"],
        "teaching_block_ids": [f"{FS}#tb2"],
    }
))

# r02 — remediation for s05 (check on f3: function call syntax)
t1_remediation.append(remediation_step(
    step_id=f"{T1}.r02",
    concept_ids=[FS],
    eyebrow="Let's Revisit",
    title="Function Call Syntax",
    blocks=[
        prose(
            f"{T1}.r02.b1",
            "A function formula follows the pattern =NAME(range). "
            "=SUM(D2:D21) is correct: equal sign, function name, opening parenthesis, "
            "the range, closing parenthesis. Omitting the = or the parentheses produces "
            "an error or plain text, not a computed result.",
            "syntax",
            [FS], [f"{FS}#f3"], [f"{FS}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [FS],
        "fact_ids": [f"{FS}#f3"],
        "teaching_block_ids": [f"{FS}#tb4"],
    }
))

# r03 — remediation for s10 (check on f3: mixed reference)
t1_remediation.append(remediation_step(
    step_id=f"{T1}.r03",
    concept_ids=[RAR],
    eyebrow="Let's Revisit",
    title="Mixed References: One Dollar Sign",
    blocks=[
        prose(
            f"{T1}.r03.b1",
            "A mixed reference uses exactly one $ sign. $A1 locks the column letter A — "
            "copy the formula across columns and A never changes, but the row number shifts. "
            "A$1 locks the row number 1 — copy down rows and 1 never changes, but the column shifts. "
            "Two $ signs ($A$1) lock both and make the reference fully absolute.",
            "mechanism",
            [RAR], [f"{RAR}#f3"], [f"{RAR}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [RAR],
        "fact_ids": [f"{RAR}#f3"],
        "teaching_block_ids": [f"{RAR}#tb4"],
    }
))

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 2: tile_spreadsheet_aggregation_logical
# ═══════════════════════════════════════════════════════════════════════════════

T2 = "tile_spreadsheet_aggregation_logical"
AGG = "spreadsheet.aggregation_functions"
LOG = "spreadsheet.logical_functions"

t2_steps = []

# s01 — explainer: aggregation_functions tb1+tb2+tb3, f1+f2, visual=side_by_side
t2_steps.append(step(
    step_id=f"{T2}.s01",
    stype="explainer",
    concept_ids=[AGG],
    eyebrow="Aggregation Functions",
    title="SUM, AVERAGE, COUNT, and COUNTA",
    lede="Four functions that reduce a whole column to one summary number.",
    blocks=[
        prose(
            f"{T2}.s01.b1",
            "With a full column of delivery amounts or times, you often want one summary number. "
            "SUM adds every value in a range: =SUM(D2:D21) totals all order amounts on your Orders sheet. "
            "AVERAGE returns the arithmetic mean: =AVERAGE(C2:C21) gives the average delivery time, "
            "skipping any blank cells (Pending or Cancelled orders have no recorded time).",
            "syntax",
            [AGG], [f"{AGG}#f1", f"{AGG}#f2"], [f"{AGG}#tb1", f"{AGG}#tb2", f"{AGG}#tb3"]
        ),
        side_by_side(
            f"{T2}.s01.b2",
            left_block=spreadsheet_grid(
                f"{T2}.s01.b2.left",
                "asset_orders_clean",
                "Orders",
                "C1:C6",
                True,
                cells=[{"ref": "C22", "formula": "=COUNT(C2:C21)", "note": "Counts numeric cells only"}],
                annotations=[{"target": "C22", "text": "=COUNT — numbers only"}]
            ),
            right_block=spreadsheet_grid(
                f"{T2}.s01.b2.right",
                "asset_orders_clean",
                "Orders",
                "C1:C6",
                True,
                cells=[{"ref": "C23", "formula": "=COUNTA(C2:C21)", "note": "Counts all non-blank cells"}],
                annotations=[{"target": "C23", "text": "=COUNTA — any non-blank"}]
            ),
            left_label="COUNT (numbers only)",
            right_label="COUNTA (any non-blank)",
            takeaway="COUNT returns a smaller number than COUNTA when the column contains blanks or text, because COUNT skips non-numeric cells while COUNTA counts everything that is not empty.",
            concept_ids=[AGG],
            fact_ids=[f"{AGG}#f1", f"{AGG}#f2"],
            teaching_block_ids=[f"{AGG}#tb2", f"{AGG}#tb3"],
            anchors=[f"{AGG}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [AGG],
        "fact_ids": [f"{AGG}#f1", f"{AGG}#f2"],
        "teaching_block_ids": [f"{AGG}#tb1", f"{AGG}#tb2", f"{AGG}#tb3"],
        "anchors": [f"{AGG}#visual"],
    },
    reward={"gems": 5}
))

# s02 — video: aggregation_functions
t2_steps.append(step(
    step_id=f"{T2}.s02",
    stype="video",
    concept_ids=[AGG],
    eyebrow="Aggregation Functions",
    title="Aggregation Functions in Action",
    blocks=[
        media_group(
            f"{T2}.s02.b1",
            ["seg_spreadsheet.aggregation_functions_BzwAZ1k3WEY_24_161"]
        ),
    ],
    lineage={
        "concept_ids": [AGG],
        "fact_ids": [f"{AGG}#f1", f"{AGG}#f2", f"{AGG}#f3"],
        "teaching_block_ids": [],
        "segment_ids": ["seg_spreadsheet.aggregation_functions_BzwAZ1k3WEY_24_161"],
    }
))

# s03 — explainer: aggregation_functions tb4, f3+f4 (COUNT vs COUNTA detail)
t2_steps.append(step(
    step_id=f"{T2}.s03",
    stype="explainer",
    concept_ids=[AGG],
    eyebrow="Aggregation Functions",
    title="COUNT vs COUNTA: What Gets Counted",
    lede="The difference matters whenever a column mixes numbers, blanks, or text.",
    blocks=[
        prose(
            f"{T2}.s03.b1",
            "COUNT counts only cells that contain numbers; empty cells, text, and error values are skipped. "
            "On your Orders sheet, =COUNT(C2:C21) counts only the rows where delivery_minutes is recorded "
            "(Delivered orders) — Pending and Cancelled rows with NULL times are excluded.",
            "mechanism",
            [AGG], [f"{AGG}#f3"], [f"{AGG}#tb4"]
        ),
        prose(
            f"{T2}.s03.b2",
            "COUNTA counts every cell that is not empty, regardless of type — numbers, text, or error values "
            "all count. =COUNTA(C2:C21) on the same column returns a larger number than COUNT because it "
            "includes any row that has any value at all. Use COUNTA when you need to count rows, not just "
            "numeric entries.",
            "mechanism",
            [AGG], [f"{AGG}#f4"], [f"{AGG}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [AGG],
        "fact_ids": [f"{AGG}#f3", f"{AGG}#f4"],
        "teaching_block_ids": [f"{AGG}#tb4"],
    },
    reward={"gems": 5}
))

# s04 — check: aggregation_functions f1+f2+f3+f4
t2_steps.append(check_step(
    step_id=f"{T2}.s04",
    concept_ids=[AGG],
    eyebrow="Quick Check",
    title="Choosing the Right Aggregation Function",
    lede="Which function should you use for each summarisation requirement?",
    lineage={
        "concept_ids": [AGG],
        "fact_ids": [f"{AGG}#f1", f"{AGG}#f2", f"{AGG}#f3", f"{AGG}#f4"],
        "teaching_block_ids": [],
        "anchors": [f"{AGG}#assessment:select_correct_aggregation_function_for_a_summarization_requirement"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s05 — hands_on: aggregation_functions f1+f2+f3+f4
t2_steps.append(hands_on_step(
    step_id=f"{T2}.s05",
    concept_ids=[AGG],
    eyebrow="Practice",
    title="Summarise the Orders Sheet",
    lede="Write SUM, AVERAGE, COUNT, and COUNTA formulas on the QuickDeliver data.",
    lineage={
        "concept_ids": [AGG],
        "fact_ids": [f"{AGG}#f1", f"{AGG}#f2", f"{AGG}#f3", f"{AGG}#f4"],
        "teaching_block_ids": [],
        "anchors": [
            f"{AGG}#practice",
            f"{AGG}#assessment:apply_sum_to_a_range",
            f"{AGG}#assessment:apply_average_and_identify_ignored_values",
            f"{AGG}#assessment:apply_count_and_identify_what_is_excluded",
            f"{AGG}#assessment:apply_counta_and_distinguish_from_count",
            f"{AGG}#assessment:choose_count_vs_counta_for_a_given_summarization_requirement",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s06 — explainer: logical_functions tb1+tb2+tb3, f1+f2+f5+f6, visual=spreadsheet_grid
t2_steps.append(step(
    step_id=f"{T2}.s06",
    stype="explainer",
    concept_ids=[LOG],
    eyebrow="Logical Functions",
    title="IF, Nested IF, AND, and OR",
    lede="Label, flag, or categorise rows based on conditions — without changing the data.",
    blocks=[
        prose(
            f"{T2}.s06.b1",
            "IF tests a condition and returns one value when it is TRUE and another when it is FALSE. "
            "Its syntax is IF(logical_test, value_if_true, value_if_false). "
            "Text results go in quotes: =IF(C2>60,\"Late\",\"On Time\") labels each order row "
            "on your Orders sheet based on its delivery_minutes value.",
            "syntax",
            [LOG], [f"{LOG}#f1", f"{LOG}#f5"], [f"{LOG}#tb1", f"{LOG}#tb2"]
        ),
        prose(
            f"{T2}.s06.b2",
            "Multiple IF functions can be nested to handle more than two outcomes. "
            "=IF(D2>89,\"A\",IF(D2>79,\"B\",IF(D2>69,\"C\",IF(D2>59,\"D\",\"F\")))) "
            "converts a numeric score to a letter grade. The same structure could sort "
            "orders into amount bands instead of a single Late/On-Time split.",
            "mechanism",
            [LOG], [f"{LOG}#f2", f"{LOG}#f6"], [f"{LOG}#tb3"]
        ),
        spreadsheet_grid(
            f"{T2}.s06.b3",
            "asset_orders_clean",
            "Orders",
            "C1:D5",
            True,
            cells=[
                {"ref": "D2", "formula": "=IF(C2>60,\"Late\",\"On Time\")", "note": "Logical test on delivery_minutes"},
                {"ref": "D3", "formula": "=IF(C3>60,\"Late\",\"On Time\")"},
                {"ref": "D4", "formula": "=IF(C4>60,\"Late\",\"On Time\")"},
            ],
            annotations=[
                {"target": "D2", "text": "IF formula in formula bar"},
                {"target": "D1", "text": "Grade column shows result"},
            ],
            concept_ids=[LOG],
            fact_ids=[f"{LOG}#f1", f"{LOG}#f2", f"{LOG}#f5", f"{LOG}#f6"],
            teaching_block_ids=[f"{LOG}#tb2", f"{LOG}#tb3"],
            anchors=[f"{LOG}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f1", f"{LOG}#f2", f"{LOG}#f5", f"{LOG}#f6"],
        "teaching_block_ids": [f"{LOG}#tb1", f"{LOG}#tb2", f"{LOG}#tb3"],
        "anchors": [f"{LOG}#visual"],
    },
    reward={"gems": 5}
))

# s07 — video: logical_functions
t2_steps.append(step(
    step_id=f"{T2}.s07",
    stype="video",
    concept_ids=[LOG],
    eyebrow="Logical Functions",
    title="Logical Functions in Action",
    blocks=[
        media_group(
            f"{T2}.s07.b1",
            [
                "seg_spreadsheet.logical_functions_5vHT16cEOPc_0_224",
                "seg_spreadsheet.logical_functions_KkTaQ5OjAGc_55_557",
            ]
        ),
    ],
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f1", f"{LOG}#f2", f"{LOG}#f3", f"{LOG}#f4", f"{LOG}#f5"],
        "teaching_block_ids": [],
        "segment_ids": [
            "seg_spreadsheet.logical_functions_5vHT16cEOPc_0_224",
            "seg_spreadsheet.logical_functions_KkTaQ5OjAGc_55_557",
        ],
    }
))

# s08 — explainer: logical_functions tb4, f3+f4 (AND/OR)
t2_steps.append(step(
    step_id=f"{T2}.s08",
    stype="explainer",
    concept_ids=[LOG],
    eyebrow="Logical Functions",
    title="AND and OR: Testing Multiple Conditions",
    lede="Combine conditions inside IF to test more than one thing at once.",
    blocks=[
        prose(
            f"{T2}.s08.b1",
            "AND returns TRUE only when all of its arguments are TRUE; if any one is FALSE, "
            "AND returns FALSE. Its syntax is AND(logical1, logical2, ...). "
            "Use AND as the logical_test of IF to require every condition to hold: "
            "=IF(AND(C2>30,E2=\"Delivered\"),\"Fast Delivery\",\"Other\") flags only orders "
            "that are both fast and delivered.",
            "syntax",
            [LOG], [f"{LOG}#f3"], [f"{LOG}#tb4"]
        ),
        prose(
            f"{T2}.s08.b2",
            "OR returns TRUE when any of its arguments is TRUE; it returns FALSE only when "
            "all arguments are FALSE. Its syntax is OR(logical1, logical2, ...). "
            "=IF(OR(E2=\"Pending\",E2=\"Cancelled\"),\"Not Delivered\",\"Delivered\") "
            "flags any order that has not yet completed.",
            "syntax",
            [LOG], [f"{LOG}#f4"], [f"{LOG}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f3", f"{LOG}#f4"],
        "teaching_block_ids": [f"{LOG}#tb4"],
    },
    reward={"gems": 5}
))

# s09 — check: logical_functions f1+f2+f5
t2_steps.append(check_step(
    step_id=f"{T2}.s09",
    concept_ids=[LOG],
    eyebrow="Quick Check",
    title="Reading an IF Formula",
    lede="What does =IF(C2>60,\"Late\",\"On Time\") return when C2 is 45?",
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f1", f"{LOG}#f2", f"{LOG}#f5"],
        "teaching_block_ids": [],
        "anchors": [f"{LOG}#assessment:apply_if_to_label_rows_by_condition"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s10 — check: logical_functions f3+f4
t2_steps.append(check_step(
    step_id=f"{T2}.s10",
    concept_ids=[LOG],
    eyebrow="Quick Check",
    title="AND vs OR",
    lede="Which function returns TRUE only when every condition is met?",
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f3", f"{LOG}#f4"],
        "teaching_block_ids": [],
        "anchors": [f"{LOG}#assessment:apply_and_or_as_logical_test_in_if"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s11 — hands_on: logical_functions f1+f2+f3+f4+f5
t2_steps.append(hands_on_step(
    step_id=f"{T2}.s11",
    concept_ids=[LOG],
    eyebrow="Practice",
    title="Label Orders with IF, AND, and OR",
    lede="Write logical formulas to classify QuickDeliver orders by status and delivery time.",
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f1", f"{LOG}#f2", f"{LOG}#f3", f"{LOG}#f4", f"{LOG}#f5"],
        "teaching_block_ids": [],
        "anchors": [
            f"{LOG}#practice",
            f"{LOG}#assessment:apply_if_to_label_rows_by_condition",
            f"{LOG}#assessment:nest_if_for_multiple_outcome_branching",
            f"{LOG}#assessment:apply_and_or_as_logical_test_in_if",
            f"{LOG}#assessment:quote_text_correctly_in_if_formula",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s12 — recap: aggregation + logical
t2_steps.append(step(
    step_id=f"{T2}.s12",
    stype="recap",
    concept_ids=[AGG, LOG],
    eyebrow="Recap",
    title="Aggregation and Logical Functions — Key Takeaways",
    blocks=[
        prose(
            f"{T2}.s12.b1",
            "SUM, AVERAGE, COUNT, and COUNTA each reduce a range to one number; "
            "which one you reach for depends on whether you need a total, a mean, "
            "a count of numbers, or a count of anything non-blank. "
            "IF tests a condition and returns different values for TRUE and FALSE; "
            "nest IFs for multiple outcomes, and use AND or OR to combine conditions.",
            "takeaway",
            [AGG, LOG],
            [f"{AGG}#f1", f"{AGG}#f2", f"{AGG}#f3", f"{AGG}#f4",
             f"{LOG}#f1", f"{LOG}#f2", f"{LOG}#f3", f"{LOG}#f4", f"{LOG}#f5"],
            [f"{AGG}#tb5"]
        ),
        up_next(
            f"{T2}.s12.b2",
            "Up Next: Text, Date, and Conditional Aggregation",
            "In the next tile you'll combine and extract text with TEXTJOIN and LEFT/RIGHT/MID, "
            "calculate date differences with TODAY and DATEDIF, and count or sum only the rows "
            "that meet a condition with COUNTIF and SUMIFS."
        ),
    ],
    lineage={
        "concept_ids": [AGG, LOG],
        "fact_ids": [
            f"{AGG}#f1", f"{AGG}#f2", f"{AGG}#f3", f"{AGG}#f4",
            f"{LOG}#f1", f"{LOG}#f2", f"{LOG}#f3", f"{LOG}#f4", f"{LOG}#f5",
        ],
        "teaching_block_ids": [f"{AGG}#tb5"],
    },
    reward={"gems": 5}
))

# ── Remediation steps for tile 2 ─────────────────────────────────────────────

t2_remediation = []

# r01 — remediation for s04 (check on f1+f2+f3+f4: choosing aggregation function)
t2_remediation.append(remediation_step(
    step_id=f"{T2}.r01",
    concept_ids=[AGG],
    eyebrow="Let's Revisit",
    title="Matching the Function to the Task",
    blocks=[
        prose(
            f"{T2}.r01.b1",
            "SUM totals numbers. AVERAGE finds the mean (blank cells are skipped, zero-value cells are included). "
            "COUNT counts only numeric cells — blank and text cells are excluded. "
            "COUNTA counts every non-blank cell regardless of type. "
            "On the Orders sheet: use SUM for total amount, AVERAGE for mean delivery time, "
            "COUNT for how many deliveries have a recorded time, COUNTA for how many rows have any entry.",
            "mechanism",
            [AGG], [f"{AGG}#f1", f"{AGG}#f2", f"{AGG}#f3", f"{AGG}#f4"], [f"{AGG}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [AGG],
        "fact_ids": [f"{AGG}#f1", f"{AGG}#f2", f"{AGG}#f3", f"{AGG}#f4"],
        "teaching_block_ids": [f"{AGG}#tb4"],
    }
))

# r02 — remediation for s09 (check on f1+f2+f5: IF formula reading)
t2_remediation.append(remediation_step(
    step_id=f"{T2}.r02",
    concept_ids=[LOG],
    eyebrow="Let's Revisit",
    title="How IF Evaluates a Condition",
    blocks=[
        prose(
            f"{T2}.r02.b1",
            "IF(logical_test, value_if_true, value_if_false) evaluates the test first. "
            "If the test is TRUE, the formula returns value_if_true; if FALSE, value_if_false. "
            "=IF(C2>60,\"Late\",\"On Time\"): when C2 is 45, the test 45>60 is FALSE, "
            "so the formula returns \"On Time\". Text values in IF must be wrapped in quotes.",
            "mechanism",
            [LOG], [f"{LOG}#f1", f"{LOG}#f5"], [f"{LOG}#tb2"]
        ),
    ],
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f1", f"{LOG}#f5"],
        "teaching_block_ids": [f"{LOG}#tb2"],
    }
))

# r03 — remediation for s10 (check on f3+f4: AND vs OR)
t2_remediation.append(remediation_step(
    step_id=f"{T2}.r03",
    concept_ids=[LOG],
    eyebrow="Let's Revisit",
    title="AND Requires All; OR Requires Any",
    blocks=[
        prose(
            f"{T2}.r03.b1",
            "AND(condition1, condition2) returns TRUE only when every condition is TRUE — "
            "one FALSE makes the whole AND FALSE. "
            "OR(condition1, condition2) returns TRUE when at least one condition is TRUE — "
            "it returns FALSE only when every condition is FALSE. "
            "Use AND when all criteria must hold; use OR when any one is enough.",
            "mechanism",
            [LOG], [f"{LOG}#f3", f"{LOG}#f4"], [f"{LOG}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [LOG],
        "fact_ids": [f"{LOG}#f3", f"{LOG}#f4"],
        "teaching_block_ids": [f"{LOG}#tb4"],
    }
))

# ═══════════════════════════════════════════════════════════════════════════════
# TILE 3: tile_spreadsheet_text_date_conditional_agg
# ═══════════════════════════════════════════════════════════════════════════════

T3 = "tile_spreadsheet_text_date_conditional_agg"
TC = "spreadsheet.text_combining"
TE = "spreadsheet.text_extraction"
DF = "spreadsheet.date_functions"
CA = "spreadsheet.conditional_aggregation"

t3_steps = []

# s01 — explainer: text_combining tb1+tb2, f1+f2+f3, visual=spreadsheet_grid
t3_steps.append(step(
    step_id=f"{T3}.s01",
    stype="explainer",
    concept_ids=[TC],
    eyebrow="Text Functions",
    title="Combining Text with TEXTJOIN and CONCATENATE",
    lede="Merge values from separate cells into one string — with or without a separator.",
    blocks=[
        prose(
            f"{T3}.s01.b1",
            "TEXTJOIN combines text from multiple ranges or strings and inserts a delimiter between each value. "
            "Its syntax is TEXTJOIN(delimiter, ignore_empty, text1, text2, ...). "
            "Setting ignore_empty to TRUE skips blank cells rather than joining them as empty strings. "
            "On your Orders sheet, TEXTJOIN(\", \", TRUE, B2, E2) would merge the city and status "
            "columns, skipping any blank status.",
            "syntax",
            [TC], [f"{TC}#f1", f"{TC}#f2"], [f"{TC}#tb1"]
        ),
        prose(
            f"{T3}.s01.b2",
            "CONCATENATE joins two or more text strings into one: CONCATENATE(text1, text2, ...). "
            "Microsoft recommends using the newer CONCAT function instead, as CONCATENATE may not "
            "be available in future versions of Excel. Neither function adds a separator automatically — "
            "include it as a literal argument if you need one.",
            "syntax",
            [TC], [f"{TC}#f3"], [f"{TC}#tb2"]
        ),
        spreadsheet_grid(
            f"{T3}.s01.b3",
            "asset_orders_clean",
            "Orders",
            "A1:F4",
            True,
            cells=[
                {"ref": "G2", "formula": "=TEXTJOIN(\", \",TRUE,B2,E2)", "note": "Combines city and status"},
                {"ref": "G3", "formula": "=TEXTJOIN(\", \",TRUE,B3,E3)"},
            ],
            annotations=[
                {"target": "G2", "text": "TEXTJOIN with \", \" delimiter"},
            ],
            concept_ids=[TC],
            fact_ids=[f"{TC}#f1", f"{TC}#f2", f"{TC}#f3"],
            teaching_block_ids=[f"{TC}#tb1", f"{TC}#tb2"],
            anchors=[f"{TC}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [TC],
        "fact_ids": [f"{TC}#f1", f"{TC}#f2", f"{TC}#f3"],
        "teaching_block_ids": [f"{TC}#tb1", f"{TC}#tb2"],
        "anchors": [f"{TC}#visual"],
    },
    reward={"gems": 5}
))

# s02 — check: text_combining f1+f2
t3_steps.append(check_step(
    step_id=f"{T3}.s02",
    concept_ids=[TC],
    eyebrow="Quick Check",
    title="TEXTJOIN's ignore_empty Argument",
    lede="What does setting ignore_empty to TRUE do in a TEXTJOIN formula?",
    lineage={
        "concept_ids": [TC],
        "fact_ids": [f"{TC}#f1", f"{TC}#f2"],
        "teaching_block_ids": [],
        "anchors": [f"{TC}#assessment:apply_textjoin_with_delimiter_and_ignore_empty"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s03 — hands_on: text_combining f1+f2+f3
t3_steps.append(hands_on_step(
    step_id=f"{T3}.s03",
    concept_ids=[TC],
    eyebrow="Practice",
    title="Combine Text Columns on the Orders Sheet",
    lede="Use TEXTJOIN to merge city and status into a single label.",
    lineage={
        "concept_ids": [TC],
        "fact_ids": [f"{TC}#f1", f"{TC}#f2", f"{TC}#f3"],
        "teaching_block_ids": [],
        "anchors": [
            f"{TC}#practice",
            f"{TC}#assessment:apply_textjoin_with_delimiter_and_ignore_empty",
            f"{TC}#assessment:distinguish_textjoin_from_concatenate",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s04 — explainer: text_extraction tb1+tb2+tb3, f1+f2+f3+f4, visual=before_after
t3_steps.append(step(
    step_id=f"{T3}.s04",
    stype="explainer",
    concept_ids=[TE],
    eyebrow="Text Functions",
    title="Extracting Text with LEFT, RIGHT, MID, and TRIM",
    lede="Pull specific characters out of a string — or strip unwanted spaces.",
    blocks=[
        prose(
            f"{T3}.s04.b1",
            "LEFT returns the first N characters of a string: LEFT(text, num_chars). "
            "RIGHT returns the last N characters: RIGHT(text, num_chars). "
            "On order IDs like \"LG-2045\", =LEFT(A2,2) returns \"LG\" and =RIGHT(A2,4) returns \"2045\".",
            "syntax",
            [TE], [f"{TE}#f1", f"{TE}#f2"], [f"{TE}#tb1"]
        ),
        prose(
            f"{T3}.s04.b2",
            "MID returns characters from any position: MID(text, start_num, num_chars). "
            "=MID(A2,4,4) on \"LG-2045\" starts at position 4 and takes 4 characters, returning \"2045\". "
            "TRIM removes all leading and trailing spaces, keeping only single spaces between words: "
            "TRIM(text). If a city was imported as \" Lagos \", =TRIM(B2) returns \"Lagos\".",
            "syntax",
            [TE], [f"{TE}#f3", f"{TE}#f4"], [f"{TE}#tb2", f"{TE}#tb3"]
        ),
        before_after(
            f"{T3}.s04.b3",
            before_block=spreadsheet_grid(
                f"{T3}.s04.b3.before",
                "asset_orders_clean",
                "Orders",
                "A1:B4",
                True,
                cells=[
                    {"ref": "A2", "note": "LG-2045 — raw order ID"},
                    {"ref": "B2", "note": " Lagos  — imported with spaces"},
                ],
                annotations=[
                    {"target": "A2", "text": "Raw: LG-2045"},
                    {"target": "B2", "text": "Raw: \" Lagos \""},
                ]
            ),
            after_block=spreadsheet_grid(
                f"{T3}.s04.b3.after",
                "asset_orders_clean",
                "Orders",
                "A1:D4",
                True,
                cells=[
                    {"ref": "C2", "formula": "=LEFT(A2,2)", "note": "Returns LG"},
                    {"ref": "D2", "formula": "=TRIM(B2)", "note": "Returns Lagos"},
                ],
                annotations=[
                    {"target": "C2", "text": "=LEFT(A2,2) → \"LG\""},
                    {"target": "D2", "text": "=TRIM(B2) → \"Lagos\""},
                ]
            ),
            change_summary="LEFT extracts the two-character prefix from the order ID; TRIM removes the stray spaces from the city name.",
            concept_ids=[TE],
            fact_ids=[f"{TE}#f1", f"{TE}#f2", f"{TE}#f3", f"{TE}#f4"],
            teaching_block_ids=[f"{TE}#tb1", f"{TE}#tb2", f"{TE}#tb3"],
            anchors=[f"{TE}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [TE],
        "fact_ids": [f"{TE}#f1", f"{TE}#f2", f"{TE}#f3", f"{TE}#f4"],
        "teaching_block_ids": [f"{TE}#tb1", f"{TE}#tb2", f"{TE}#tb3"],
        "anchors": [f"{TE}#visual"],
    },
    reward={"gems": 5}
))

# s05 — check: text_extraction f3+f4
t3_steps.append(check_step(
    step_id=f"{T3}.s05",
    concept_ids=[TE],
    eyebrow="Quick Check",
    title="MID and TRIM",
    lede="Which formula extracts 4 characters starting at position 4 from cell A2?",
    lineage={
        "concept_ids": [TE],
        "fact_ids": [f"{TE}#f3", f"{TE}#f4"],
        "teaching_block_ids": [],
        "anchors": [
            f"{TE}#assessment:apply_mid_to_extract_characters_by_position",
            f"{TE}#assessment:apply_trim_to_remove_extraneous_whitespace",
        ],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s06 — check: text_extraction f1+f2+f3+f4
t3_steps.append(check_step(
    step_id=f"{T3}.s06",
    concept_ids=[TE],
    eyebrow="Quick Check",
    title="Choosing the Right Extraction Function",
    lede="Which function should you use for each text extraction task?",
    lineage={
        "concept_ids": [TE],
        "fact_ids": [f"{TE}#f1", f"{TE}#f2", f"{TE}#f3", f"{TE}#f4"],
        "teaching_block_ids": [],
        "anchors": [f"{TE}#assessment:select_correct_extraction_function_for_given_text_task"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s07 — hands_on: text_extraction f1+f2
t3_steps.append(hands_on_step(
    step_id=f"{T3}.s07",
    concept_ids=[TE],
    eyebrow="Practice",
    title="Extract Characters from Order IDs",
    lede="Use LEFT and RIGHT to pull the prefix and numeric suffix from the order_id column.",
    lineage={
        "concept_ids": [TE],
        "fact_ids": [f"{TE}#f1", f"{TE}#f2"],
        "teaching_block_ids": [],
        "anchors": [
            f"{TE}#practice",
            f"{TE}#assessment:apply_left_to_extract_leading_characters",
            f"{TE}#assessment:apply_right_to_extract_trailing_characters",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s08 — explainer: date_functions tb1+tb2+tb3+tb4, f1+f2+f3+f4+f5, visual=spreadsheet_grid
t3_steps.append(step(
    step_id=f"{T3}.s08",
    stype="explainer",
    concept_ids=[DF],
    eyebrow="Date Functions",
    title="TODAY, DATEDIF, and the Date Serial Number",
    lede="Excel stores dates as numbers — which makes date arithmetic straightforward.",
    blocks=[
        prose(
            f"{T3}.s08.b1",
            "Excel stores every date as a sequential serial number: January 1, 1900 is 1, "
            "and each subsequent day adds 1. That is why date functions can do arithmetic on dates "
            "the same way ordinary functions do on numbers — a date cell is just a number "
            "displayed in a date format.",
            "mechanism",
            [DF], [f"{DF}#f4"], [f"{DF}#tb1"]
        ),
        prose(
            f"{T3}.s08.b2",
            "TODAY() returns the serial number of the current date and takes no arguments. "
            "DATEDIF(start_date, end_date, unit) returns the difference between two dates in the unit "
            "you specify: \"Y\" for complete years, \"D\" for days. "
            "DATEDIF is useful for age calculations: DATEDIF(birthdate, TODAY(), \"Y\") "
            "returns the number of complete years between the birthdate and today.",
            "syntax",
            [DF], [f"{DF}#f1", f"{DF}#f2", f"{DF}#f3", f"{DF}#f5"], [f"{DF}#tb2", f"{DF}#tb3"]
        ),
        prose(
            f"{T3}.s08.b3",
            "On your Orders sheet, with an order date in G2, =DATEDIF(G2,TODAY(),\"D\") tells you "
            "how many days have passed since that order was placed. TODAY() supplies the end date "
            "automatically, so the result updates each day the workbook is opened.",
            "example",
            [DF], [f"{DF}#f1", f"{DF}#f2"], [f"{DF}#tb4"]
        ),
        spreadsheet_grid(
            f"{T3}.s08.b4",
            "asset_orders_clean",
            "Orders",
            "G1:H4",
            True,
            cells=[
                {"ref": "H2", "formula": "=DATEDIF(G2,TODAY(),\"D\")", "note": "Days since order placed"},
                {"ref": "H3", "formula": "=DATEDIF(G3,TODAY(),\"D\")"},
            ],
            annotations=[
                {"target": "H2", "text": "DATEDIF formula in formula bar"},
                {"target": "G2", "text": "order_date (serial number)"},
            ],
            concept_ids=[DF],
            fact_ids=[f"{DF}#f1", f"{DF}#f2", f"{DF}#f3", f"{DF}#f4", f"{DF}#f5"],
            teaching_block_ids=[f"{DF}#tb1", f"{DF}#tb2", f"{DF}#tb3", f"{DF}#tb4"],
            anchors=[f"{DF}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [DF],
        "fact_ids": [f"{DF}#f1", f"{DF}#f2", f"{DF}#f3", f"{DF}#f4", f"{DF}#f5"],
        "teaching_block_ids": [f"{DF}#tb1", f"{DF}#tb2", f"{DF}#tb3", f"{DF}#tb4"],
        "anchors": [f"{DF}#visual"],
    },
    reward={"gems": 5}
))

# s09 — check: date_functions f1+f2+f5
t3_steps.append(check_step(
    step_id=f"{T3}.s09",
    concept_ids=[DF],
    eyebrow="Quick Check",
    title="Choosing the Right Date Function",
    lede="Which function returns the number of days between two dates?",
    lineage={
        "concept_ids": [DF],
        "fact_ids": [f"{DF}#f1", f"{DF}#f2", f"{DF}#f5"],
        "teaching_block_ids": [],
        "anchors": [f"{DF}#assessment:select_correct_date_function_for_given_calculation_requirement"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s10 — hands_on: date_functions f1+f2+f3+f4+f5
t3_steps.append(hands_on_step(
    step_id=f"{T3}.s10",
    concept_ids=[DF],
    eyebrow="Practice",
    title="Calculate Days Since Each Order Was Placed",
    lede="Write a DATEDIF formula using TODAY() to find how many days have passed since each order date.",
    lineage={
        "concept_ids": [DF],
        "fact_ids": [f"{DF}#f1", f"{DF}#f2", f"{DF}#f3", f"{DF}#f4", f"{DF}#f5"],
        "teaching_block_ids": [],
        "anchors": [
            f"{DF}#practice",
            f"{DF}#assessment:write_today_function_with_correct_syntax",
            f"{DF}#assessment:write_datedif_with_correct_arguments_and_unit",
            f"{DF}#assessment:construct_age_calculation_formula_using_datedif_and_today",
            f"{DF}#assessment:explain_date_serial_number_model",
            f"{DF}#assessment:select_correct_date_function_for_given_calculation_requirement",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s11 — explainer: conditional_aggregation tb1+tb2, f1+f3, visual=spreadsheet_grid
t3_steps.append(step(
    step_id=f"{T3}.s11",
    stype="explainer",
    concept_ids=[CA],
    eyebrow="Conditional Aggregation",
    title="COUNTIF and SUMIF: One Condition",
    lede="Count or sum only the rows that match a single criterion.",
    blocks=[
        prose(
            f"{T3}.s11.b1",
            "SUM, AVERAGE, COUNT, and COUNTA take every value in their range. "
            "When you only want rows that meet a condition — orders from Lagos, say — "
            "use COUNTIF or SUMIF instead.",
            "intro",
            [CA], [f"{CA}#f1", f"{CA}#f3"], [f"{CA}#tb1"]
        ),
        prose(
            f"{T3}.s11.b2",
            "COUNTIF(range, criteria) counts the cells in range that match criteria. "
            "=COUNTIF(B2:B21,\"Lagos\") counts how many orders in the city column are from Lagos. "
            "SUMIF(range, criteria, sum_range) sums the values in sum_range for rows where range "
            "matches criteria. =SUMIF(B2:B21,\"Lagos\",D2:D21) totals the amounts for Lagos orders only.",
            "syntax",
            [CA], [f"{CA}#f1", f"{CA}#f3"], [f"{CA}#tb2"]
        ),
        spreadsheet_grid(
            f"{T3}.s11.b3",
            "asset_orders_clean",
            "Orders",
            "A1:E6",
            True,
            cells=[
                {"ref": "G2", "formula": "=COUNTIF(B2:B21,\"Lagos\")", "note": "Count of Lagos orders"},
                {"ref": "G3", "formula": "=SUMIF(B2:B21,\"Lagos\",D2:D21)", "note": "Total amount for Lagos"},
            ],
            annotations=[
                {"target": "G2", "text": "COUNTIF — criteria range + criterion"},
                {"target": "G3", "text": "SUMIF — criteria range + criterion + sum range"},
            ],
            concept_ids=[CA],
            fact_ids=[f"{CA}#f1", f"{CA}#f3"],
            teaching_block_ids=[f"{CA}#tb1", f"{CA}#tb2"],
            anchors=[f"{CA}#visual"]
        ),
    ],
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f1", f"{CA}#f3"],
        "teaching_block_ids": [f"{CA}#tb1", f"{CA}#tb2"],
        "anchors": [f"{CA}#visual"],
    },
    reward={"gems": 5}
))

# s12 — explainer: conditional_aggregation tb3, f2+f4 (COUNTIFS/SUMIFS)
t3_steps.append(step(
    step_id=f"{T3}.s12",
    stype="explainer",
    concept_ids=[CA],
    eyebrow="Conditional Aggregation",
    title="COUNTIFS and SUMIFS: Multiple Conditions",
    lede="Add a second (or third) condition by extending the argument list.",
    blocks=[
        prose(
            f"{T3}.s12.b1",
            "COUNTIFS(criteria_range1, criteria1, criteria_range2, criteria2, ...) counts rows "
            "where all criteria are met together. Each additional range must have the same number "
            "of rows and columns as the first. "
            "=COUNTIFS(B2:B21,\"Lagos\",E2:E21,\"Delivered\") counts only Lagos orders that are Delivered.",
            "syntax",
            [CA], [f"{CA}#f2"], [f"{CA}#tb3"]
        ),
        prose(
            f"{T3}.s12.b2",
            "SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...) sums "
            "sum_range for rows where all criteria hold. Note the argument order: sum_range comes first, "
            "then each criteria_range/criteria pair. "
            "=SUMIFS(D2:D21,B2:B21,\"Lagos\",E2:E21,\"Delivered\") totals amounts for Lagos Delivered orders.",
            "syntax",
            [CA], [f"{CA}#f4"], [f"{CA}#tb3"]
        ),
    ],
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f2", f"{CA}#f4"],
        "teaching_block_ids": [f"{CA}#tb3"],
    },
    reward={"gems": 5}
))

# s13 — video: conditional_aggregation
t3_steps.append(step(
    step_id=f"{T3}.s13",
    stype="video",
    concept_ids=[CA],
    eyebrow="Conditional Aggregation",
    title="Building Conditional Aggregation Formulas",
    blocks=[
        media_group(
            f"{T3}.s13.b1",
            [
                "seg_spreadsheet.conditional_aggregation_AZuBNWMh7VM_118_366",
                "seg_spreadsheet.conditional_aggregation_X-xZ3eKvkzo_43_341",
            ]
        ),
    ],
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f1", f"{CA}#f2", f"{CA}#f3", f"{CA}#f4", f"{CA}#f5"],
        "teaching_block_ids": [],
        "segment_ids": [
            "seg_spreadsheet.conditional_aggregation_AZuBNWMh7VM_118_366",
            "seg_spreadsheet.conditional_aggregation_X-xZ3eKvkzo_43_341",
        ],
    }
))

# s14 — explainer: conditional_aggregation tb4, f5+f6 (criteria syntax + same range twice)
t3_steps.append(step(
    step_id=f"{T3}.s14",
    stype="explainer",
    concept_ids=[CA],
    eyebrow="Conditional Aggregation",
    title="Criteria Syntax and the Between Pattern",
    lede="Criteria with comparison symbols or text must be in quotes — and you can use the same range twice.",
    blocks=[
        prose(
            f"{T3}.s14.b1",
            "Criteria can be a number, an expression, a cell reference, or text. "
            "Criteria that contain comparison symbols or text must be enclosed in quotation marks: "
            "use \">32\" not >32, and \"Lagos\" not Lagos. "
            "A bare number like 32 or a cell reference like B4 does not need quotes.",
            "mechanism",
            [CA], [f"{CA}#f5"], [f"{CA}#tb4"]
        ),
        prose(
            f"{T3}.s14.b2",
            "The same range can appear in more than one criteria pair to test a between condition. "
            "=COUNTIFS(C2:C21,\">30\",C2:C21,\"<60\") counts orders where delivery_minutes is "
            "between 30 and 60 — both criteria apply to the same column.",
            "mechanism",
            [CA], [f"{CA}#f6"], [f"{CA}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f5", f"{CA}#f6"],
        "teaching_block_ids": [f"{CA}#tb4"],
    },
    reward={"gems": 5}
))

# s15 — check: conditional_aggregation f1+f2+f3+f4
t3_steps.append(check_step(
    step_id=f"{T3}.s15",
    concept_ids=[CA],
    eyebrow="Quick Check",
    title="Single vs Multi-Condition Aggregation",
    lede="Which function counts rows that meet two conditions at once?",
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f1", f"{CA}#f2", f"{CA}#f3", f"{CA}#f4"],
        "teaching_block_ids": [],
        "anchors": [
            f"{CA}#assessment:write_single_condition_countif_sumif",
            f"{CA}#assessment:write_multi_condition_countifs_sumifs",
        ],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s16 — check: conditional_aggregation f6
t3_steps.append(check_step(
    step_id=f"{T3}.s16",
    concept_ids=[CA],
    eyebrow="Quick Check",
    title="The Between Pattern",
    lede="How do you count values in C2:C21 that are greater than 30 AND less than 60?",
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f6"],
        "teaching_block_ids": [],
        "anchors": [f"{CA}#assessment:use_same_range_twice_for_between_condition"],
    },
    reward={"gems": 5, "first_try_bonus": 3}
))

# s17 — hands_on: conditional_aggregation f5
t3_steps.append(hands_on_step(
    step_id=f"{T3}.s17",
    concept_ids=[CA],
    eyebrow="Practice",
    title="Write Conditional Aggregation Formulas",
    lede="Apply correct criteria quoting to COUNTIF and SUMIFS on the Orders sheet.",
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f5"],
        "teaching_block_ids": [],
        "anchors": [
            f"{CA}#practice",
            f"{CA}#assessment:apply_correct_criteria_syntax_quoting",
        ],
    },
    reward={"gems": 10, "first_try_bonus": 5}
))

# s18 — recap
t3_steps.append(step(
    step_id=f"{T3}.s18",
    stype="recap",
    concept_ids=[TC, TE, DF, CA],
    eyebrow="Recap",
    title="Text, Date, and Conditional Aggregation — Key Takeaways",
    blocks=[
        prose(
            f"{T3}.s18.b1",
            "TEXTJOIN combines text with a delimiter; CONCATENATE (or CONCAT) joins without one. "
            "LEFT, RIGHT, and MID extract characters by position; TRIM removes stray spaces. "
            "Excel stores dates as serial numbers starting from January 1, 1900; "
            "TODAY() returns today's serial number and DATEDIF computes the difference in years or days. "
            "COUNTIF and SUMIF apply one condition; COUNTIFS and SUMIFS apply multiple — "
            "criteria with text or comparison symbols must be in quotes.",
            "takeaway",
            [TC, TE, DF, CA],
            [f"{TC}#f1", f"{TC}#f2", f"{TC}#f3",
             f"{TE}#f1", f"{TE}#f2", f"{TE}#f3", f"{TE}#f4",
             f"{DF}#f1", f"{DF}#f2", f"{DF}#f4",
             f"{CA}#f1", f"{CA}#f2", f"{CA}#f3", f"{CA}#f4", f"{CA}#f5"],
            []
        ),
        up_next(
            f"{T3}.s18.b2",
            "Up Next: VLOOKUP, XLOOKUP, and INDEX/MATCH",
            "In the next tile you'll look up a driver name from the Drivers sheet using VLOOKUP, "
            "then see how XLOOKUP and INDEX/MATCH handle cases VLOOKUP cannot."
        ),
    ],
    lineage={
        "concept_ids": [TC, TE, DF, CA],
        "fact_ids": [],
        "teaching_block_ids": [],
    },
    reward={"gems": 5}
))

# ── Remediation steps for tile 3 ─────────────────────────────────────────────

t3_remediation = []

# r01 — remediation for s02 (check on f1+f2: TEXTJOIN ignore_empty)
t3_remediation.append(remediation_step(
    step_id=f"{T3}.r01",
    concept_ids=[TC],
    eyebrow="Let's Revisit",
    title="TEXTJOIN's ignore_empty Argument",
    blocks=[
        prose(
            f"{T3}.r01.b1",
            "TEXTJOIN(delimiter, ignore_empty, text1, text2, ...) has three required parts. "
            "The delimiter is the separator inserted between each value. "
            "ignore_empty controls blank cells: TRUE skips them so no extra delimiter appears; "
            "FALSE includes them as empty strings. "
            "TEXTJOIN(\", \", TRUE, B2, E2) on a row where E2 is blank returns just the city, "
            "not \"Lagos, \".",
            "syntax",
            [TC], [f"{TC}#f1", f"{TC}#f2"], [f"{TC}#tb1"]
        ),
    ],
    lineage={
        "concept_ids": [TC],
        "fact_ids": [f"{TC}#f1", f"{TC}#f2"],
        "teaching_block_ids": [f"{TC}#tb1"],
    }
))

# r02 — remediation for s05 (check on f3+f4: MID and TRIM)
t3_remediation.append(remediation_step(
    step_id=f"{T3}.r02",
    concept_ids=[TE],
    eyebrow="Let's Revisit",
    title="MID and TRIM Syntax",
    blocks=[
        prose(
            f"{T3}.r02.b1",
            "MID(text, start_num, num_chars) needs three arguments: the text, where to start (1-based), "
            "and how many characters to take. =MID(A2,4,4) on \"LG-2045\" starts at position 4 "
            "(the '2') and takes 4 characters, returning \"2045\". "
            "TRIM(text) takes one argument and removes all leading and trailing spaces, "
            "leaving only single spaces between words.",
            "syntax",
            [TE], [f"{TE}#f3", f"{TE}#f4"], [f"{TE}#tb2", f"{TE}#tb3"]
        ),
    ],
    lineage={
        "concept_ids": [TE],
        "fact_ids": [f"{TE}#f3", f"{TE}#f4"],
        "teaching_block_ids": [f"{TE}#tb2", f"{TE}#tb3"],
    }
))

# r03 — remediation for s09 (check on f1+f2+f5: date function selection)
t3_remediation.append(remediation_step(
    step_id=f"{T3}.r03",
    concept_ids=[DF],
    eyebrow="Let's Revisit",
    title="TODAY vs DATEDIF",
    blocks=[
        prose(
            f"{T3}.r03.b1",
            "TODAY() returns the current date as a serial number and takes no arguments — "
            "it is always =TODAY() with empty parentheses. "
            "DATEDIF(start_date, end_date, unit) computes the difference between two dates. "
            "Use \"D\" as the unit for days and \"Y\" for complete years. "
            "To find days since an order was placed: =DATEDIF(G2,TODAY(),\"D\").",
            "syntax",
            [DF], [f"{DF}#f1", f"{DF}#f2", f"{DF}#f5"], [f"{DF}#tb2", f"{DF}#tb3"]
        ),
    ],
    lineage={
        "concept_ids": [DF],
        "fact_ids": [f"{DF}#f1", f"{DF}#f2", f"{DF}#f5"],
        "teaching_block_ids": [f"{DF}#tb2", f"{DF}#tb3"],
    }
))

# r04 — remediation for s15 (check on f1+f2+f3+f4: single vs multi condition)
t3_remediation.append(remediation_step(
    step_id=f"{T3}.r04",
    concept_ids=[CA],
    eyebrow="Let's Revisit",
    title="COUNTIF/SUMIF vs COUNTIFS/SUMIFS",
    blocks=[
        prose(
            f"{T3}.r04.b1",
            "COUNTIF and SUMIF each accept exactly one criteria range and one criterion. "
            "COUNTIFS and SUMIFS accept any number of criteria_range/criteria pairs — "
            "all conditions must be met for a row to be counted or summed. "
            "For two conditions (city = Lagos AND status = Delivered), use COUNTIFS or SUMIFS, "
            "not COUNTIF or SUMIF.",
            "mechanism",
            [CA], [f"{CA}#f1", f"{CA}#f2", f"{CA}#f3", f"{CA}#f4"], [f"{CA}#tb2", f"{CA}#tb3"]
        ),
    ],
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f1", f"{CA}#f2", f"{CA}#f3", f"{CA}#f4"],
        "teaching_block_ids": [f"{CA}#tb2", f"{CA}#tb3"],
    }
))

# r05 — remediation for s16 (check on f6: between pattern)
t3_remediation.append(remediation_step(
    step_id=f"{T3}.r05",
    concept_ids=[CA],
    eyebrow="Let's Revisit",
    title="Using the Same Range Twice for a Between Condition",
    blocks=[
        prose(
            f"{T3}.r05.b1",
            "COUNTIFS allows the same range to appear in more than one criteria pair. "
            "To count values between 30 and 60 in C2:C21, write: "
            "=COUNTIFS(C2:C21,\">30\",C2:C21,\"<60\"). "
            "The first pair filters rows where delivery_minutes > 30; "
            "the second pair further filters to delivery_minutes < 60. "
            "Both criteria must be in quotes because they contain comparison symbols.",
            "mechanism",
            [CA], [f"{CA}#f6"], [f"{CA}#tb4"]
        ),
    ],
    lineage={
        "concept_ids": [CA],
        "fact_ids": [f"{CA}#f6"],
        "teaching_block_ids": [f"{CA}#tb4"],
    }
))

# ═══════════════════════════════════════════════════════════════════════════════
# Assemble output
# ═══════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "tiles": [
        {
            "tile_id": T1,
            "title": "Writing Formulas and Reference Types",
            "steps": t1_steps,
            "remediation_steps": t1_remediation,
        },
        {
            "tile_id": T2,
            "title": "Aggregation and Logical Functions",
            "steps": t2_steps,
            "remediation_steps": t2_remediation,
        },
        {
            "tile_id": T3,
            "title": "Text, Date, and Conditional Aggregation",
            "steps": t3_steps,
            "remediation_steps": t3_remediation,
        },
    ]
}

with open(OUT, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {OUT}")
print(f"Tile 1 steps: {len(t1_steps)}, remediation: {len(t1_remediation)}")
print(f"Tile 2 steps: {len(t2_steps)}, remediation: {len(t2_remediation)}")
print(f"Tile 3 steps: {len(t3_steps)}, remediation: {len(t3_remediation)}")
EOF
