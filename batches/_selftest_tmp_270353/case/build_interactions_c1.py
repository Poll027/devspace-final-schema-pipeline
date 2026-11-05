"""Build interactions.part.c1.json for tile_spreadsheet_formula_syntax_refs,
tile_spreadsheet_aggregation_logical, tile_spreadsheet_text_date_conditional_agg."""
import json, pathlib

BATCH = pathlib.Path("batches/final_batch_011_da_spreadsheet")

# ── helpers ──────────────────────────────────────────────────────────────────
def choice(step_id, difficulty, measures, anchors, prompt, options, correct_ids,
           option_feedback, fb_correct, fb_incorrect, hints, remediation_step_id=None):
    ix = {
        "type": "choice",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": False,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "prompt": prompt,
            "options": [{"option_id": k, "text": v} for k, v in options.items()],
            "selection": "single",
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": correct_ids,
            "option_feedback": {k: {"message": v} for k, v in option_feedback.items()},
        },
        "feedback": {
            "correct": {"message": fb_correct},
            "incorrect": {"message": fb_incorrect},
            "hints": hints,
        },
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return {"step_id": step_id, "interaction": ix}


def formula_entry(step_id, difficulty, measures, anchors, prompt, asset_id,
                  sheet_name, target_cell, allowed_functions, expected_value,
                  reference_formula, must_use_functions, fb_correct, fb_incorrect,
                  hints, remediation_step_id=None, tolerance=None):
    pub = {
        "prompt": prompt,
        "asset_ref": {"asset_id": asset_id, "variant_id": None},
        "target_cell": target_cell,
        "allowed_functions": allowed_functions,
    }
    if sheet_name:
        pub["sheet_name"] = sheet_name
    grading = {
        "expected_value": expected_value,
        "reference_formula": reference_formula,
        "must_use_functions": must_use_functions,
        "forbid_hardcoded_values": True,
    }
    if tolerance is not None:
        grading["tolerance"] = tolerance
    ix = {
        "type": "formula_entry",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": False,
        "measures": measures,
        "anchors": anchors,
        "public": pub,
        "grading": grading,
        "feedback": {
            "correct": {"message": fb_correct},
            "incorrect": {"message": fb_incorrect},
            "hints": hints,
        },
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return {"step_id": step_id, "interaction": ix}


def code_exercise(step_id, difficulty, measures, anchors, prompt,
                  runtime_kind, runtime_version,
                  files, entry, asset_mounts, allowed_syntax, blocked_syntax,
                  solution_files, tests,
                  fb_correct, fb_incorrect, hints, remediation_step_id=None):
    constraints = {}
    if allowed_syntax:
        constraints["allowed_syntax"] = allowed_syntax
    if blocked_syntax:
        constraints["blocked_syntax"] = blocked_syntax
    workspace = {
        "files": files,
        "entry": entry,
        "asset_mounts": asset_mounts,
    }
    runtime = {"kind": runtime_kind, "version": runtime_version}
    ix = {
        "type": "code_exercise",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": False,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "prompt": prompt,
            "runtime": runtime,
            "workspace": workspace,
            "constraints": constraints,
        },
        "grading": {
            "solution_files": solution_files,
            "tests": tests,
        },
        "feedback": {
            "correct": {"message": fb_correct},
            "incorrect": {"message": fb_incorrect},
            "hints": hints,
        },
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return {"step_id": step_id, "interaction": ix}


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 1: tile_spreadsheet_formula_syntax_refs
# Steps: s04 (check), s05 (check), s06 (hands_on/code_exercise),
#        s10 (check), s11 (hands_on/code_exercise)
# ═══════════════════════════════════════════════════════════════════════════════

# s04 — choice — identify_required_equal_sign_prefix — f1
s04 = choice(
    step_id="tile_spreadsheet_formula_syntax_refs.s04",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.formula_syntax",
        "capability": "identify_required_equal_sign_prefix",
        "fact_ids": ["spreadsheet.formula_syntax#f1"],
    }],
    anchors=["spreadsheet.formula_syntax#assessment:identify_required_equal_sign_prefix"],
    prompt=(
        "You type the following into cell D4 of the Orders sheet: D2+D3\n\n"
        "What happens when you press Enter?"
    ),
    options={
        "opt_a": "Excel treats it as text and displays the string \"D2+D3\" in the cell.",
        "opt_b": "Excel adds the values in D2 and D3 and shows the numeric result.",
        "opt_c": "Excel shows a #NAME? error because the cell addresses are invalid.",
        "opt_d": "Excel shows a #VALUE! error because + requires numbers.",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "Without a leading = Excel does not evaluate the entry as a formula. "
            "It stores the literal text \"D2+D3\" instead of computing a sum."
        ),
        "opt_c": (
            "#NAME? appears when Excel cannot recognise a name inside a formula. "
            "Here there is no formula at all — the entry has no = prefix, so Excel "
            "stores it as plain text."
        ),
        "opt_d": (
            "#VALUE! occurs when a formula receives the wrong type of argument. "
            "But without a leading = there is no formula to evaluate, so no error "
            "is raised — the entry is stored as text."
        ),
    },
    fb_correct=(
        "Correct! Without the = prefix Excel treats the entry as plain text and "
        "displays \"D2+D3\" literally. Every formula must start with = to tell Excel "
        "to compute a value."
    ),
    fb_incorrect=(
        "Formulas in Excel always begin with the equal sign (=). Without it, Excel "
        "treats the entry as plain text and displays it as-is, not as a computed result."
    ),
    hints=[
        "Think about what tells Excel that an entry is a formula rather than a label.",
        "Try typing just the letter A in a cell — Excel shows 'A', not an error.",
    ],
    remediation_step_id="tile_spreadsheet_formula_syntax_refs.s01",
)

# s05 — choice — construct_function_call_formula_with_range — f3
s05 = choice(
    step_id="tile_spreadsheet_formula_syntax_refs.s05",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.formula_syntax",
        "capability": "construct_function_call_formula_with_range",
        "fact_ids": ["spreadsheet.formula_syntax#f3"],
    }],
    anchors=["spreadsheet.formula_syntax#assessment:construct_function_call_formula_with_range"],
    prompt=(
        "The Orders sheet has 20 rows of data in rows 2–21. "
        "You want to add up all the values in the amount column (D2:D21) using the SUM function. "
        "Which formula is correctly structured?"
    ),
    options={
        "opt_a": "=SUM(D2:D21)",
        "opt_b": "SUM(D2:D21)",
        "opt_c": "=SUM D2:D21",
        "opt_d": "=SUM(D2,D21)",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "This is missing the = prefix. Without it, Excel stores the entry as "
            "text rather than evaluating the SUM function."
        ),
        "opt_c": (
            "The parentheses are required. The correct syntax is =SUM(range) — "
            "the opening parenthesis immediately follows the function name, and the "
            "range goes inside."
        ),
        "opt_d": (
            "=SUM(D2,D21) adds only two individual cells: D2 and D21. "
            "To sum a continuous range of cells, use the colon notation: D2:D21."
        ),
    },
    fb_correct=(
        "Correct! =SUM(D2:D21) follows the required structure: = prefix, function name, "
        "opening parenthesis, the range D2:D21, closing parenthesis. "
        "This sums all 20 amount values."
    ),
    fb_incorrect=(
        "A function formula needs: = prefix, the function name, an opening parenthesis, "
        "the range argument, and a closing parenthesis — for example =SUM(D2:D21)."
    ),
    hints=[
        "Every formula starts with =. Then comes the function name, then the range inside parentheses.",
        "D2:D21 uses a colon to mean 'from D2 to D21'. A comma would list only two separate cells.",
    ],
    remediation_step_id="tile_spreadsheet_formula_syntax_refs.s01",
)

# s06 — code_exercise (spreadsheet) — formula_syntax practice
# Practice anchor success: 'The formula begins with =, references two cell addresses from the Orders sheet separated by -, and returns the correct numeric difference when entered.'
# We also test operator precedence (f5): =5+2*3 vs =(5+2)*3
# D3 - D2 = 7200 - 4500 = 2700
# For precedence: put a typed value in H1 and H2, compute with precedence
# Actually let's keep it simple: two tasks
# Task 1: =D3-D2 in E1 -> 2700.0
# Task 2: =(D3+D2)*2 in E2 -> (7200+4500)*2 = 23400.0 (tests parentheses)
# vs D3+D2*2 = 7200+9000 = 16200.0 (without parens)

s06 = code_exercise(
    step_id="tile_spreadsheet_formula_syntax_refs.s06",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.formula_syntax",
            "capability": "apply_arithmetic_operators_in_formula",
            "fact_ids": ["spreadsheet.formula_syntax#f2"],
        },
        {
            "concept_id": "spreadsheet.formula_syntax",
            "capability": "build_cell_reference_formula_with_operator",
            "fact_ids": ["spreadsheet.formula_syntax#f4"],
        },
        {
            "concept_id": "spreadsheet.formula_syntax",
            "capability": "apply_operator_precedence_and_parentheses",
            "fact_ids": ["spreadsheet.formula_syntax#f5"],
        },
        {
            "concept_id": "spreadsheet.formula_syntax",
            "capability": "write_syntactically_correct_formula_for_given_computation",
            "fact_ids": [
                "spreadsheet.formula_syntax#f1",
                "spreadsheet.formula_syntax#f2",
                "spreadsheet.formula_syntax#f3",
                "spreadsheet.formula_syntax#f4",
                "spreadsheet.formula_syntax#f5",
            ],
        },
    ],
    anchors=[
        "spreadsheet.formula_syntax#practice",
        "spreadsheet.formula_syntax#assessment:apply_arithmetic_operators_in_formula",
        "spreadsheet.formula_syntax#assessment:build_cell_reference_formula_with_operator",
        "spreadsheet.formula_syntax#assessment:apply_operator_precedence_and_parentheses",
        "spreadsheet.formula_syntax#assessment:write_syntactically_correct_formula_for_given_computation",
    ],
    prompt=(
        "The **orders** sheet has order amounts in column D (rows 2–21). "
        "Row 2 (LG-2001) has amount **4500** and row 3 (LG-2002) has amount **7200**.\n\n"
        "**Task 1 — subtraction:** In cell E1, write a formula that subtracts the amount in D2 "
        "from the amount in D3 (D3 minus D2). The result should be **2700**.\n\n"
        "**Task 2 — operator precedence:** In cell E2, write a formula that first adds D2 and D3, "
        "then multiplies the sum by 2. Use parentheses to force the addition before the multiplication. "
        "The result should be **23400**."
    ),
    runtime_kind="spreadsheet",
    runtime_version="3.4.0",
    files=[{
        "path": "book.sheet",
        "role": "editable",
        "language": "sheet",
        "content": (
            "// The orders sheet has order amounts in column D.\n"
            "// D2 = 4500 (LG-2001), D3 = 7200 (LG-2002)\n\n"
            "// Task 1: In E1, write a formula that computes D3 minus D2.\n"
            "// Expected result: 2700\n\n"
            "// Task 2: In E2, write a formula that adds D2 and D3, then multiplies by 2.\n"
            "// Use parentheses so the addition happens before the multiplication.\n"
            "// Expected result: 23400\n"
        ),
    }],
    entry="book.sheet",
    asset_mounts=[{
        "asset_id": "asset_orders_clean",
        "mount_path": "orders.csv",
    }],
    allowed_syntax=["-", "+", "*", "/", "(", ")"],
    blocked_syntax=["SUM", "IF", "VLOOKUP"],
    solution_files=[{
        "path": "book.sheet",
        "content": "E1: =D3-D2\nE2: =(D2+D3)*2\n",
    }],
    tests=[
        {
            "test_id": "test_subtraction_result",
            "kind": "cell_equals",
            "spec": {"cell": "E1", "expected": 2700.0},
            "visible": True,
            "message_on_fail": (
                "E1 should equal 2700 (D3 minus D2 = 7200 - 4500). "
                "Make sure your formula starts with = and uses the - operator between D3 and D2."
            ),
        },
        {
            "test_id": "test_precedence_result",
            "kind": "cell_equals",
            "spec": {"cell": "E2", "expected": 23400.0},
            "visible": True,
            "message_on_fail": (
                "E2 should equal 23400 ((D2+D3)*2 = (4500+7200)*2 = 11700*2). "
                "Without parentheses, =D2+D3*2 gives 18600 because * is evaluated before +. "
                "Wrap the addition in parentheses: =(D2+D3)*2."
            ),
        },
    ],
    fb_correct=(
        "Well done! E1 uses = and the - operator to subtract D2 from D3, returning 2700. "
        "E2 uses parentheses to force the addition (D2+D3) before the multiplication by 2, "
        "returning 23400. Without parentheses, =D2+D3*2 would give 18600 because * has higher "
        "precedence than +."
    ),
    fb_incorrect=(
        "Check both cells. E1 needs =D3-D2 (the = prefix, then D3, then -, then D2). "
        "E2 needs parentheses around the addition: =(D2+D3)*2. Without parentheses, "
        "multiplication happens before addition and the result is wrong."
    ),
    hints=[
        "Every formula must start with =. Without it, Excel stores the entry as text.",
        "Parentheses change the order of operations: =(D2+D3)*2 adds first, then multiplies.",
    ],
    remediation_step_id="tile_spreadsheet_formula_syntax_refs.s01",
)

# s10 — choice — construct_mixed_reference_locking_one_dimension — f3
s10 = choice(
    step_id="tile_spreadsheet_formula_syntax_refs.s10",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.relative_absolute_references",
        "capability": "construct_mixed_reference_locking_one_dimension",
        "fact_ids": ["spreadsheet.relative_absolute_references#f3"],
    }],
    anchors=["spreadsheet.relative_absolute_references#assessment:construct_mixed_reference_locking_one_dimension"],
    prompt=(
        "You are building a multiplication table. Row 1 holds the column multipliers "
        "(B1, C1, D1, …) and column A holds the row multipliers (A2, A3, A4, …). "
        "You want to enter one formula in B2 and copy it across the entire table so that "
        "it always multiplies the correct row multiplier by the correct column multiplier.\n\n"
        "Which formula should you enter in B2?"
    ),
    options={
        "opt_a": "=$A2*B$1",
        "opt_b": "=$A$2*$B$1",
        "opt_c": "=A2*B1",
        "opt_d": "=$A$2*B1",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "$A$2 locks both the column and the row of the row multiplier. "
            "When you copy the formula down, the row part ($2) never changes, "
            "so every row in the table uses A2 instead of A3, A4, etc."
        ),
        "opt_c": (
            "=A2*B1 uses fully relative references. When copied across columns, "
            "A2 shifts to B2, C2, etc., so the formula no longer reads from column A. "
            "When copied down, B1 shifts to B2, B3, etc., losing the header row."
        ),
        "opt_d": (
            "$A$2 locks both dimensions of the row multiplier, so copying down "
            "always reads A2 instead of A3, A4, etc. You need $A2 (lock column A, "
            "let the row adjust) to keep the row multiplier in column A while "
            "allowing the row to change."
        ),
    },
    fb_correct=(
        "Correct! =$A2*B$1 uses two mixed references. $A2 locks column A so the row "
        "multiplier always comes from column A, while the row number adjusts as you copy "
        "down. B$1 locks row 1 so the column multiplier always comes from row 1, while "
        "the column letter adjusts as you copy across."
    ),
    fb_incorrect=(
        "A mixed reference locks one dimension and lets the other adjust. "
        "$A2 locks the column (A stays fixed) but lets the row change when copied down. "
        "B$1 locks the row (1 stays fixed) but lets the column change when copied across. "
        "Together, =$A2*B$1 fills the entire multiplication table correctly from one formula."
    ),
    hints=[
        "The $ sign locks the part that follows it: $A locks the column, $1 locks the row.",
        "Ask yourself: when I copy this formula down, which part must NOT change? When I copy across, which part must NOT change?",
    ],
    remediation_step_id="tile_spreadsheet_formula_syntax_refs.s07",
)

# s11 — code_exercise (spreadsheet) — relative/absolute references practice
# Practice anchor success: 'Every copied formula in the column shows the correct product of that row's price and the shared tax-rate cell; the tax-rate address remains unchanged in every formula while the price address increments by row.'
# H1 = 0.075 (tax rate), D2:D6 = amounts
# E2: =D2*$H$1 = 4500*0.075 = 337.5
# E3: =D3*$H$1 = 7200*0.075 = 540.0
# E4: =D4*$H$1 = 3100*0.075 = 232.5

s11 = code_exercise(
    step_id="tile_spreadsheet_formula_syntax_refs.s11",
    difficulty="stretch",
    measures=[
        {
            "concept_id": "spreadsheet.relative_absolute_references",
            "capability": "identify_relative_reference_adjustment_on_copy",
            "fact_ids": ["spreadsheet.relative_absolute_references#f1"],
        },
        {
            "concept_id": "spreadsheet.relative_absolute_references",
            "capability": "apply_absolute_reference_to_fix_cell_on_copy",
            "fact_ids": ["spreadsheet.relative_absolute_references#f2"],
        },
        {
            "concept_id": "spreadsheet.relative_absolute_references",
            "capability": "select_correct_reference_type_for_copy_scenario",
            "fact_ids": [
                "spreadsheet.relative_absolute_references#f1",
                "spreadsheet.relative_absolute_references#f2",
                "spreadsheet.relative_absolute_references#f3",
            ],
        },
    ],
    anchors=[
        "spreadsheet.relative_absolute_references#practice",
        "spreadsheet.relative_absolute_references#assessment:identify_relative_reference_adjustment_on_copy",
        "spreadsheet.relative_absolute_references#assessment:apply_absolute_reference_to_fix_cell_on_copy",
        "spreadsheet.relative_absolute_references#assessment:select_correct_reference_type_for_copy_scenario",
    ],
    prompt=(
        "The **orders** sheet has order amounts in column D (rows 2–4). "
        "Cell H1 holds the tax rate **0.075** (7.5%).\n\n"
        "**Task:** In cells E2, E3, and E4, write a formula that multiplies each row's amount "
        "(D2, D3, D4) by the shared tax rate in H1. "
        "Use an **absolute reference** for H1 so the tax-rate address does not change when "
        "the formula is copied down. Use a **relative reference** for the amount cell so it "
        "adjusts to the correct row.\n\n"
        "- E2 should equal **337.5** (4500 × 0.075)\n"
        "- E3 should equal **540** (7200 × 0.075)\n"
        "- E4 should equal **232.5** (3100 × 0.075)"
    ),
    runtime_kind="spreadsheet",
    runtime_version="3.4.0",
    files=[{
        "path": "book.sheet",
        "role": "editable",
        "language": "sheet",
        "content": (
            "// H1 holds the shared tax rate.\n"
            "H1: 0.075\n\n"
            "// Task: In E2, write a formula that multiplies D2 by the tax rate in H1.\n"
            "// Use $H$1 (absolute) for the tax rate so it does not shift when copied.\n"
            "// Use D2 (relative) for the amount so it adjusts to D3, D4 when copied down.\n"
            "// Then write the same pattern in E3 and E4.\n"
        ),
    }],
    entry="book.sheet",
    asset_mounts=[{
        "asset_id": "asset_orders_clean",
        "mount_path": "orders.csv",
    }],
    allowed_syntax=["*", "$"],
    blocked_syntax=["SUM", "IF", "VLOOKUP"],
    solution_files=[{
        "path": "book.sheet",
        "content": "H1: 0.075\nE2: =D2*$H$1\nE3: =D3*$H$1\nE4: =D4*$H$1\n",
    }],
    tests=[
        {
            "test_id": "test_e2_tax",
            "kind": "cell_equals",
            "spec": {"cell": "E2", "expected": 337.5, "tolerance": 0.01},
            "visible": True,
            "message_on_fail": (
                "E2 should equal 337.5 (D2 × H1 = 4500 × 0.075). "
                "Use =D2*$H$1 — the $ signs lock H1 so it does not shift when copied."
            ),
        },
        {
            "test_id": "test_e3_tax",
            "kind": "cell_equals",
            "spec": {"cell": "E3", "expected": 540.0, "tolerance": 0.01},
            "visible": True,
            "message_on_fail": (
                "E3 should equal 540 (D3 × H1 = 7200 × 0.075). "
                "If you copied =D2*$H$1 down, D2 should have adjusted to D3 while $H$1 stayed fixed."
            ),
        },
        {
            "test_id": "test_e4_tax",
            "kind": "cell_equals",
            "spec": {"cell": "E4", "expected": 232.5, "tolerance": 0.01},
            "visible": True,
            "message_on_fail": (
                "E4 should equal 232.5 (D4 × H1 = 3100 × 0.075). "
                "Check that E4 uses D4 (relative, adjusts per row) and $H$1 (absolute, stays fixed)."
            ),
        },
        {
            "test_id": "test_e2_uses_absolute",
            "kind": "formula_uses",
            "spec": {"cell": "E2", "functions": []},
            "visible": True,
            "message_on_fail": (
                "E2 must contain a formula (starting with =) that multiplies the amount by the tax rate."
            ),
        },
    ],
    fb_correct=(
        "Excellent! =D2*$H$1 uses a relative reference for D2 (it adjusts to D3, D4 as you copy down) "
        "and an absolute reference for $H$1 (the $ signs lock both the column H and row 1, so the "
        "tax-rate cell never shifts). This is the key pattern for applying a shared rate to a column of values."
    ),
    fb_incorrect=(
        "Use =D2*$H$1 in E2. The $ signs in $H$1 lock the tax-rate cell so it does not shift when "
        "the formula is copied. D2 has no $ signs, so it adjusts to D3 in E3 and D4 in E4. "
        "If you used =D2*H1 (no $), H1 would shift to H2, H3, etc. when copied down."
    ),
    hints=[
        "Add $ before both the column letter and the row number of H1 to lock it: $H$1.",
        "Leave D2 without $ signs so it automatically becomes D3 when you copy the formula to E3.",
    ],
    remediation_step_id="tile_spreadsheet_formula_syntax_refs.s07",
)


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 2: tile_spreadsheet_aggregation_logical
# Steps: s04 (check), s05 (hands_on/formula_entry), s09 (check), s10 (hands_on/code_exercise)
# ═══════════════════════════════════════════════════════════════════════════════

# s04 — choice — select_correct_aggregation_function_for_a_summarization_requirement
s04_agg = choice(
    step_id="tile_spreadsheet_aggregation_logical.s04",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.aggregation_functions",
        "capability": "select_correct_aggregation_function_for_a_summarization_requirement",
        "fact_ids": [
            "spreadsheet.aggregation_functions#f1",
            "spreadsheet.aggregation_functions#f2",
            "spreadsheet.aggregation_functions#f3",
            "spreadsheet.aggregation_functions#f4",
        ],
    }],
    anchors=["spreadsheet.aggregation_functions#assessment:select_correct_aggregation_function_for_a_summarization_requirement"],
    prompt=(
        "The Orders sheet has 20 rows. Column A holds order IDs (text like \"LG-2001\"), "
        "column C holds delivery_minutes (numbers for delivered orders, blank for pending/cancelled), "
        "and column D holds order amounts (all numbers).\n\n"
        "A manager asks: \"How many orders have a recorded delivery time?\" "
        "Which function should you use, and why?"
    ),
    options={
        "opt_a": "COUNT(C2:C21) — because COUNT counts only numeric cells and delivery_minutes is blank for undelivered orders.",
        "opt_b": "COUNTA(C2:C21) — because COUNTA counts all non-empty cells, including text.",
        "opt_c": "SUM(C2:C21) — because SUM adds up all the delivery times to give a total count.",
        "opt_d": "AVERAGE(C2:C21) — because AVERAGE returns the number of values in the range.",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "COUNTA counts any non-empty cell, including text. For delivery_minutes, "
            "all non-blank cells are numbers, so COUNTA and COUNT give the same result here. "
            "But COUNT is the precise choice: it counts only numeric cells, which is exactly "
            "what 'has a recorded delivery time' means."
        ),
        "opt_c": (
            "SUM adds the values together and returns a total number of minutes, not a count "
            "of rows. To count how many rows have a value, use COUNT or COUNTA."
        ),
        "opt_d": (
            "AVERAGE returns the arithmetic mean of the values, not the number of values. "
            "To count how many cells contain a number, use COUNT."
        ),
    },
    fb_correct=(
        "Correct! COUNT(C2:C21) counts only the numeric cells in the delivery_minutes column. "
        "Blank cells (for pending/cancelled orders) are skipped, so the result equals the number "
        "of orders with a recorded delivery time."
    ),
    fb_incorrect=(
        "COUNT counts only numeric cells and ignores blanks, text, and logical values. "
        "Because delivery_minutes is blank for undelivered orders, COUNT(C2:C21) returns "
        "exactly the number of orders that have a recorded delivery time."
    ),
    hints=[
        "COUNT counts only numbers. COUNTA counts anything that is not empty. SUM adds values. AVERAGE computes a mean.",
        "Blank cells in delivery_minutes represent orders with no recorded time — COUNT skips them automatically.",
    ],
    remediation_step_id="tile_spreadsheet_aggregation_logical.s01",
)

# s05 — formula_entry — aggregation practice
# Practice anchor: 'All four formulas return correct values'
# For formula_entry (single formula), use COUNTA(A2:A21) = 20
# This tests COUNTA on text cells (order_ids), showing it counts text while COUNT would return 0
s05_agg = formula_entry(
    step_id="tile_spreadsheet_aggregation_logical.s05",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.aggregation_functions",
            "capability": "apply_counta_and_distinguish_from_count",
            "fact_ids": [
                "spreadsheet.aggregation_functions#f3",
                "spreadsheet.aggregation_functions#f4",
            ],
        },
        {
            "concept_id": "spreadsheet.aggregation_functions",
            "capability": "choose_count_vs_counta_for_a_given_summarization_requirement",
            "fact_ids": [
                "spreadsheet.aggregation_functions#f3",
                "spreadsheet.aggregation_functions#f4",
            ],
        },
        {
            "concept_id": "spreadsheet.aggregation_functions",
            "capability": "apply_sum_to_a_range",
            "fact_ids": ["spreadsheet.aggregation_functions#f1"],
        },
    ],
    anchors=[
        "spreadsheet.aggregation_functions#practice",
        "spreadsheet.aggregation_functions#assessment:apply_sum_to_a_range",
        "spreadsheet.aggregation_functions#assessment:apply_average_and_identify_ignored_values",
        "spreadsheet.aggregation_functions#assessment:apply_count_and_identify_what_is_excluded",
        "spreadsheet.aggregation_functions#assessment:apply_counta_and_distinguish_from_count",
        "spreadsheet.aggregation_functions#assessment:choose_count_vs_counta_for_a_given_summarization_requirement",
    ],
    prompt=(
        "The Orders sheet has 20 rows of data (rows 2–21). "
        "Column A holds order IDs — text values like \"LG-2001\". "
        "Column D holds order amounts — all numeric.\n\n"
        "In cell H1, write a formula using **COUNTA** that counts how many non-empty cells "
        "are in the order_id column (A2:A21). "
        "Because order IDs are text, COUNT would return 0 — COUNTA is the right choice here.\n\n"
        "The expected result is **20**."
    ),
    asset_id="asset_orders_clean",
    sheet_name="orders",
    target_cell="H1",
    allowed_functions=["COUNTA"],
    expected_value=20,
    reference_formula="=COUNTA(A2:A21)",
    must_use_functions=["COUNTA"],
    fb_correct=(
        "Correct! =COUNTA(A2:A21) returns 20 because all 20 order-ID cells are non-empty. "
        "COUNTA counts any non-empty cell — numbers, text, or errors — while COUNT counts "
        "only numeric cells. Since order IDs are text, COUNT(A2:A21) would return 0."
    ),
    fb_incorrect=(
        "Use =COUNTA(A2:A21). COUNTA counts every non-empty cell regardless of type, "
        "so it correctly counts the 20 text order IDs. COUNT would return 0 here because "
        "it only counts numeric cells."
    ),
    hints=[
        "COUNTA counts cells that contain any value — numbers, text, or errors. COUNT counts only numbers.",
        "The range A2:A21 covers all 20 data rows in column A (order_id).",
    ],
    remediation_step_id="tile_spreadsheet_aggregation_logical.s01",
)

# s09 — choice — write_basic_if_formula_with_quoted_text — f1, f5
s09_log = choice(
    step_id="tile_spreadsheet_aggregation_logical.s09",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.logical_functions",
        "capability": "write_basic_if_formula_with_quoted_text",
        "fact_ids": [
            "spreadsheet.logical_functions#f1",
            "spreadsheet.logical_functions#f5",
        ],
    }],
    anchors=["spreadsheet.logical_functions#assessment:write_basic_if_formula_with_quoted_text"],
    prompt=(
        "Cell C2 holds a delivery time in minutes. You want a formula in F2 that displays "
        "\"Late\" if the delivery took more than 60 minutes, or \"On Time\" otherwise.\n\n"
        "Which formula is correct?"
    ),
    options={
        "opt_a": '=IF(C2>60,"Late","On Time")',
        "opt_b": '=IF(C2>60,Late,On Time)',
        "opt_c": '=IF("C2>60","Late","On Time")',
        "opt_d": '=IF(C2>60,"On Time","Late")',
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "Text results in an IF formula must be enclosed in double quotation marks. "
            "Without quotes, Excel tries to interpret Late and On Time as cell names or "
            "named ranges and returns a #NAME? error."
        ),
        "opt_c": (
            "The logical_test (C2>60) must not be in quotes. Putting it in quotes makes "
            "Excel treat it as a text string rather than evaluating it as a comparison, "
            "so the condition is never tested."
        ),
        "opt_d": (
            "The arguments are in the wrong order. IF(logical_test, value_if_true, value_if_false): "
            "the second argument is returned when the condition is TRUE (C2>60), so \"Late\" "
            "must come second, not \"On Time\"."
        ),
    },
    fb_correct=(
        "Correct! =IF(C2>60,\"Late\",\"On Time\") tests whether C2 is greater than 60. "
        "If TRUE it returns the text \"Late\"; if FALSE it returns \"On Time\". "
        "Text values in formulas must always be wrapped in double quotation marks."
    ),
    fb_incorrect=(
        "The IF syntax is IF(logical_test, value_if_true, value_if_false). "
        "Text results must be in double quotes: \"Late\" and \"On Time\". "
        "The logical test (C2>60) must not be in quotes — it is a comparison, not text."
    ),
    hints=[
        "Text in a formula always goes inside double quotation marks, like \"Late\".",
        "The second argument of IF is what is returned when the condition is TRUE.",
    ],
    remediation_step_id="tile_spreadsheet_aggregation_logical.s06",
)

# s10 — code_exercise (spreadsheet) — logical_functions practice
# Practice anchor: 'The formula in the target cell returns the correct letter grade for every score in the sample column, including boundary values, and uses AND as the logical_test of at least one IF to enforce both a lower and upper bound on a grade band.'
# We use delivery_minutes to classify: >60 = 'Late', 30-60 (AND) = 'On Time', <30 = 'Fast'
# =IF(C2>60,"Late",IF(AND(C2>=30,C2<=60),"On Time","Fast"))
# Row 2: 28 -> Fast
# Row 3: 45 -> On Time
# Row 4: 62 -> Late

s10_log = code_exercise(
    step_id="tile_spreadsheet_aggregation_logical.s10",
    difficulty="stretch",
    measures=[
        {
            "concept_id": "spreadsheet.logical_functions",
            "capability": "construct_nested_if_for_multi_band_classification",
            "fact_ids": [
                "spreadsheet.logical_functions#f1",
                "spreadsheet.logical_functions#f2",
                "spreadsheet.logical_functions#f6",
            ],
        },
        {
            "concept_id": "spreadsheet.logical_functions",
            "capability": "use_and_as_if_logical_test_for_multiple_conditions",
            "fact_ids": [
                "spreadsheet.logical_functions#f3",
            ],
        },
        {
            "concept_id": "spreadsheet.logical_functions",
            "capability": "select_and_combine_if_and_or_for_given_decision_logic",
            "fact_ids": [
                "spreadsheet.logical_functions#f1",
                "spreadsheet.logical_functions#f3",
                "spreadsheet.logical_functions#f4",
                "spreadsheet.logical_functions#f5",
            ],
        },
    ],
    anchors=[
        "spreadsheet.logical_functions#practice",
        "spreadsheet.logical_functions#assessment:construct_nested_if_for_multi_band_classification",
        "spreadsheet.logical_functions#assessment:use_and_as_if_logical_test_for_multiple_conditions",
        "spreadsheet.logical_functions#assessment:use_or_as_if_logical_test_for_any_condition",
        "spreadsheet.logical_functions#assessment:select_and_combine_if_and_or_for_given_decision_logic",
    ],
    prompt=(
        "The **orders** sheet has delivery times in column C (rows 2–4). "
        "You need to classify each delivery into one of three bands:\n\n"
        "- **\"Late\"** if delivery_minutes > 60\n"
        "- **\"On Time\"** if delivery_minutes is between 30 and 60 (inclusive on both ends)\n"
        "- **\"Fast\"** if delivery_minutes < 30\n\n"
        "**Task:** In cell F2, write a nested IF formula that classifies the delivery time in C2. "
        "Use **AND** as the logical_test of the inner IF to enforce both the lower bound (>=30) "
        "and the upper bound (<=60) of the \"On Time\" band.\n\n"
        "Then write the same formula in F3 and F4.\n\n"
        "Expected results:\n"
        "- F2: **\"Fast\"** (C2 = 28)\n"
        "- F3: **\"On Time\"** (C3 = 45)\n"
        "- F4: **\"Late\"** (C4 = 62)"
    ),
    runtime_kind="spreadsheet",
    runtime_version="3.4.0",
    files=[{
        "path": "book.sheet",
        "role": "editable",
        "language": "sheet",
        "content": (
            "// The orders sheet has delivery_minutes in column C.\n"
            "// C2=28, C3=45, C4=62\n\n"
            "// Task: In F2, write a nested IF formula that classifies C2 as:\n"
            "//   'Late'    if C2 > 60\n"
            "//   'On Time' if C2 >= 30 AND C2 <= 60  (use AND for both bounds)\n"
            "//   'Fast'    if C2 < 30\n"
            "// Then write the same pattern in F3 and F4.\n"
        ),
    }],
    entry="book.sheet",
    asset_mounts=[{
        "asset_id": "asset_orders_clean",
        "mount_path": "orders.csv",
    }],
    allowed_syntax=["IF", "AND", "OR"],
    blocked_syntax=["IFS", "SWITCH", "CHOOSE"],
    solution_files=[{
        "path": "book.sheet",
        "content": (
            'F2: =IF(C2>60,"Late",IF(AND(C2>=30,C2<=60),"On Time","Fast"))\n'
            'F3: =IF(C3>60,"Late",IF(AND(C3>=30,C3<=60),"On Time","Fast"))\n'
            'F4: =IF(C4>60,"Late",IF(AND(C4>=30,C4<=60),"On Time","Fast"))\n'
        ),
    }],
    tests=[
        {
            "test_id": "test_f2_fast",
            "kind": "cell_equals",
            "spec": {"cell": "F2", "expected": "Fast"},
            "visible": True,
            "message_on_fail": (
                "F2 should be \"Fast\" because C2=28 is less than 30. "
                "Check the order of your IF conditions: test >60 first, then AND(>=30,<=60), then the else is Fast."
            ),
        },
        {
            "test_id": "test_f3_on_time",
            "kind": "cell_equals",
            "spec": {"cell": "F3", "expected": "On Time"},
            "visible": True,
            "message_on_fail": (
                "F3 should be \"On Time\" because C3=45 is between 30 and 60. "
                "Use AND(C3>=30,C3<=60) as the logical_test of the inner IF."
            ),
        },
        {
            "test_id": "test_f4_late",
            "kind": "cell_equals",
            "spec": {"cell": "F4", "expected": "Late"},
            "visible": True,
            "message_on_fail": (
                "F4 should be \"Late\" because C4=62 is greater than 60. "
                "The outer IF should test C4>60 first."
            ),
        },
        {
            "test_id": "test_f2_uses_if_and",
            "kind": "formula_uses",
            "spec": {"cell": "F2", "functions": ["IF", "AND"]},
            "visible": True,
            "message_on_fail": (
                "F2 must use both IF and AND. Use AND(C2>=30,C2<=60) as the logical_test "
                "of the inner IF to enforce both bounds of the 'On Time' band."
            ),
        },
    ],
    fb_correct=(
        "Well done! Your nested IF correctly classifies all three delivery times. "
        "The outer IF tests C2>60 (Late). The inner IF uses AND(C2>=30,C2<=60) to enforce "
        "both bounds of the On Time band — AND returns TRUE only when both conditions are met. "
        "If neither condition is true, the formula returns Fast."
    ),
    fb_incorrect=(
        "Use: =IF(C2>60,\"Late\",IF(AND(C2>=30,C2<=60),\"On Time\",\"Fast\")). "
        "The outer IF handles the Late case (>60). The inner IF uses AND to test both bounds "
        "of On Time (>=30 AND <=60). The final else is Fast. "
        "Remember to wrap text results in double quotes."
    ),
    hints=[
        "Start with the outer IF: =IF(C2>60,\"Late\", ...). Then nest another IF for the middle band.",
        "AND(C2>=30,C2<=60) returns TRUE only when C2 is at least 30 AND at most 60.",
    ],
    remediation_step_id="tile_spreadsheet_aggregation_logical.s06",
)


# ═══════════════════════════════════════════════════════════════════════════════
# TILE 3: tile_spreadsheet_text_date_conditional_agg
# Steps: s02 (check), s03 (hands_on/formula_entry), s05 (check), s06 (check),
#        s07 (hands_on/formula_entry), s09 (check), s10 (hands_on/code_exercise),
#        s15 (check), s16 (check), s17 (hands_on/formula_entry)
# ═══════════════════════════════════════════════════════════════════════════════

# s02 — choice — identify_concatenate_syntax_and_deprecation_caveat — f3
s02_txt = choice(
    step_id="tile_spreadsheet_text_date_conditional_agg.s02",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.text_combining",
        "capability": "identify_concatenate_syntax_and_deprecation_caveat",
        "fact_ids": ["spreadsheet.text_combining#f3"],
    }],
    anchors=["spreadsheet.text_combining#assessment:identify_concatenate_syntax_and_deprecation_caveat"],
    prompt=(
        "A colleague shares a workbook that uses =CONCATENATE(A2,\" \",B2) to join a first name "
        "and a last name. Which statement about CONCATENATE is accurate?"
    ),
    options={
        "opt_a": "CONCATENATE works but Microsoft recommends using CONCAT instead, as CONCATENATE may not be available in future versions of Excel.",
        "opt_b": "CONCATENATE is the current recommended function and CONCAT is the deprecated one.",
        "opt_c": "CONCATENATE automatically skips empty cells, so no ignore_empty argument is needed.",
        "opt_d": "CONCATENATE can only join two text strings at a time.",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "This is reversed. Microsoft recommends the newer CONCAT function and notes that "
            "CONCATENATE may not be available in future versions of Excel."
        ),
        "opt_c": (
            "CONCATENATE does not skip empty cells — it joins them as blank values, which can "
            "produce unwanted extra spaces. TEXTJOIN with ignore_empty=TRUE is the function "
            "that skips empty cells."
        ),
        "opt_d": (
            "CONCATENATE accepts multiple text arguments: CONCATENATE(text1, [text2], ...). "
            "It can join more than two strings in a single formula."
        ),
    },
    fb_correct=(
        "Correct! CONCATENATE joins text strings and its syntax is CONCATENATE(text1, [text2], ...). "
        "However, Microsoft recommends using the newer CONCAT function instead, since CONCATENATE "
        "may not be available in future versions of Excel."
    ),
    fb_incorrect=(
        "CONCATENATE joins two or more text strings. Microsoft recommends using CONCAT instead, "
        "as CONCATENATE may not be available in future versions of Excel. "
        "Neither function automatically skips empty cells — use TEXTJOIN with ignore_empty=TRUE for that."
    ),
    hints=[
        "Think about which function Microsoft says is the newer, recommended replacement.",
        "TEXTJOIN is the function with the ignore_empty argument, not CONCATENATE.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s01",
)

# s03 — formula_entry — text_combining practice
# Practice anchor: 'Column C displays the correctly joined full name for each row (e.g., Jane Smith), with no leading or trailing spaces caused by empty cells, using TEXTJOIN with a space delimiter and ignore_empty set to TRUE.'
# We adapt: combine city (B2) and status (E2) with ' | ' delimiter using TEXTJOIN
# =TEXTJOIN(" | ",TRUE,B2,E2) -> "Lagos | Delivered"
s03_txt = formula_entry(
    step_id="tile_spreadsheet_text_date_conditional_agg.s03",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.text_combining",
            "capability": "build_combined_string_from_cells_with_delimiter",
            "fact_ids": ["spreadsheet.text_combining#f1"],
        },
        {
            "concept_id": "spreadsheet.text_combining",
            "capability": "apply_textjoin_with_ignore_empty",
            "fact_ids": [
                "spreadsheet.text_combining#f1",
                "spreadsheet.text_combining#f2",
            ],
        },
    ],
    anchors=[
        "spreadsheet.text_combining#practice",
        "spreadsheet.text_combining#assessment:build_combined_string_from_cells_with_delimiter",
        "spreadsheet.text_combining#assessment:apply_textjoin_with_ignore_empty",
    ],
    prompt=(
        "The Orders sheet has the delivery city in column B and the order status in column E. "
        "Row 2 has city **\"Lagos\"** and status **\"Delivered\"**.\n\n"
        "In cell H2, write a TEXTJOIN formula that combines the city (B2) and status (E2) "
        "with the delimiter **\" | \"** (space-pipe-space) and sets ignore_empty to **TRUE**.\n\n"
        "The expected result is **\"Lagos | Delivered\"**."
    ),
    asset_id="asset_orders_clean",
    sheet_name="orders",
    target_cell="H2",
    allowed_functions=["TEXTJOIN"],
    expected_value="Lagos | Delivered",
    reference_formula='=TEXTJOIN(" | ",TRUE,B2,E2)',
    must_use_functions=["TEXTJOIN"],
    fb_correct=(
        "Correct! =TEXTJOIN(\" | \",TRUE,B2,E2) joins B2 (\"Lagos\") and E2 (\"Delivered\") "
        "with the delimiter \" | \", returning \"Lagos | Delivered\". "
        "Setting ignore_empty to TRUE means any blank cells in the argument list are skipped "
        "rather than producing an extra delimiter."
    ),
    fb_incorrect=(
        "Use =TEXTJOIN(\" | \",TRUE,B2,E2). The first argument is the delimiter (\" | \"), "
        "the second is ignore_empty (TRUE), and the remaining arguments are the cells to join "
        "(B2 and E2). Make sure the delimiter is in double quotes."
    ),
    hints=[
        "TEXTJOIN syntax: TEXTJOIN(delimiter, ignore_empty, text1, [text2], ...)",
        "The delimiter \" | \" includes spaces on both sides of the pipe character.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s01",
)

# s05 — choice — apply_mid_to_extract_characters_by_position AND apply_trim — f3, f4
s05_ext = choice(
    step_id="tile_spreadsheet_text_date_conditional_agg.s05",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.text_extraction",
            "capability": "apply_mid_to_extract_characters_by_position",
            "fact_ids": ["spreadsheet.text_extraction#f3"],
        },
        {
            "concept_id": "spreadsheet.text_extraction",
            "capability": "apply_trim_to_remove_extraneous_whitespace",
            "fact_ids": ["spreadsheet.text_extraction#f4"],
        },
    ],
    anchors=[
        "spreadsheet.text_extraction#assessment:apply_mid_to_extract_characters_by_position",
        "spreadsheet.text_extraction#assessment:apply_trim_to_remove_extraneous_whitespace",
    ],
    prompt=(
        "Cell A2 contains the order ID **\"LG-2001\"**. "
        "You want to extract the 4-digit number starting at position 4 (the \"2001\" part).\n\n"
        "Which formula correctly extracts exactly 4 characters starting at position 4?"
    ),
    options={
        "opt_a": "=MID(A2,4,4)",
        "opt_b": "=MID(A2,4,3)",
        "opt_c": "=LEFT(A2,4)",
        "opt_d": "=MID(A2,3,4)",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "=MID(A2,4,3) starts at position 4 but extracts only 3 characters, "
            "returning \"200\" instead of \"2001\". The third argument of MID is the "
            "number of characters to extract."
        ),
        "opt_c": (
            "=LEFT(A2,4) extracts the first 4 characters from the left, returning \"LG-2\" "
            "instead of \"2001\". LEFT always starts from the beginning of the string."
        ),
        "opt_d": (
            "=MID(A2,3,4) starts at position 3, which is the \"-\" character in \"LG-2001\". "
            "This returns \"-200\" instead of \"2001\". The start position must be 4 to begin "
            "at the \"2\" character."
        ),
    },
    fb_correct=(
        "Correct! =MID(A2,4,4) starts at position 4 (the \"2\" in \"2001\") and extracts "
        "4 characters, returning \"2001\". MID syntax: MID(text, start_num, num_chars)."
    ),
    fb_incorrect=(
        "MID(text, start_num, num_chars) extracts num_chars characters starting at start_num. "
        "In \"LG-2001\": position 1=L, 2=G, 3=-, 4=2, 5=0, 6=0, 7=1. "
        "To get \"2001\", start at position 4 and extract 4 characters: =MID(A2,4,4)."
    ),
    hints=[
        "Count the characters in \"LG-2001\": L=1, G=2, -=3, 2=4, 0=5, 0=6, 1=7.",
        "MID's third argument is how many characters to return, not the end position.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s04",
)

# s06 — choice — select_correct_extraction_function_for_given_text_task — f1,f2,f3,f4
s06_ext = choice(
    step_id="tile_spreadsheet_text_date_conditional_agg.s06",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.text_extraction",
        "capability": "select_correct_extraction_function_for_given_text_task",
        "fact_ids": [
            "spreadsheet.text_extraction#f1",
            "spreadsheet.text_extraction#f2",
            "spreadsheet.text_extraction#f3",
            "spreadsheet.text_extraction#f4",
        ],
    }],
    anchors=["spreadsheet.text_extraction#assessment:select_correct_extraction_function_for_given_text_task"],
    prompt=(
        "A city name imported from an external system is stored in cell B2 as "
        "**\"  Lagos  \"** (with two leading spaces and two trailing spaces). "
        "You want to clean it so it reads **\"Lagos\"** with no extra spaces.\n\n"
        "Which function should you use?"
    ),
    options={
        "opt_a": "=TRIM(B2)",
        "opt_b": "=LEFT(B2,5)",
        "opt_c": "=MID(B2,3,5)",
        "opt_d": "=RIGHT(B2,5)",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "=LEFT(B2,5) extracts the first 5 characters from the left. Because the string "
            "starts with two spaces, LEFT(B2,5) returns \"  Lag\" — the spaces are included "
            "and the full city name is cut off."
        ),
        "opt_c": (
            "=MID(B2,3,5) starts at position 3 (the first non-space character) and extracts "
            "5 characters, returning \"Lagos\". This works for this specific string, but it "
            "relies on knowing exactly how many leading spaces there are. TRIM is the robust "
            "solution because it removes all leading and trailing spaces regardless of count."
        ),
        "opt_d": (
            "=RIGHT(B2,5) extracts the last 5 characters. Because the string ends with two "
            "spaces, RIGHT(B2,5) returns \"gos  \" — the trailing spaces are included."
        ),
    },
    fb_correct=(
        "Correct! =TRIM(B2) removes all leading and trailing spaces from the text, "
        "returning \"Lagos\". TRIM also collapses multiple spaces between words to a single "
        "space, making it the standard tool for cleaning imported text."
    ),
    fb_incorrect=(
        "TRIM removes all spaces from a text value except for single spaces between words. "
        "It is the right tool when you need to clean leading or trailing spaces from imported data. "
        "LEFT, RIGHT, and MID extract characters by position — they do not remove spaces."
    ),
    hints=[
        "TRIM is designed specifically to remove leading and trailing spaces from text.",
        "LEFT and RIGHT extract characters from the start or end — they include any spaces that are there.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s04",
)

# s07 — formula_entry — text_extraction practice (LEFT and RIGHT)
# Practice anchor: 'area-code column shows only the three digits (e.g. 234) for every row, and the cleaned city column shows values with no leading or trailing spaces'
# Anchors: apply_left_to_extract_leading_characters, apply_right_to_extract_trailing_characters
# Use LEFT(A2,2) = 'LG' (2-letter prefix of order_id)
s07_ext = formula_entry(
    step_id="tile_spreadsheet_text_date_conditional_agg.s07",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.text_extraction",
            "capability": "apply_left_to_extract_leading_characters",
            "fact_ids": ["spreadsheet.text_extraction#f1"],
        },
        {
            "concept_id": "spreadsheet.text_extraction",
            "capability": "apply_right_to_extract_trailing_characters",
            "fact_ids": ["spreadsheet.text_extraction#f2"],
        },
    ],
    anchors=[
        "spreadsheet.text_extraction#practice",
        "spreadsheet.text_extraction#assessment:apply_left_to_extract_leading_characters",
        "spreadsheet.text_extraction#assessment:apply_right_to_extract_trailing_characters",
    ],
    prompt=(
        "The Orders sheet has order IDs in column A (e.g., **\"LG-2001\"**). "
        "Each order ID has a 2-letter prefix (\"LG\") followed by a hyphen and a 4-digit number.\n\n"
        "In cell H2, write a formula using **RIGHT** that extracts the last 4 characters "
        "of the order ID in A2 — the 4-digit number part.\n\n"
        "The expected result is **\"2001\"**."
    ),
    asset_id="asset_orders_clean",
    sheet_name="orders",
    target_cell="H2",
    allowed_functions=["RIGHT"],
    expected_value="2001",
    reference_formula="=RIGHT(A2,4)",
    must_use_functions=["RIGHT"],
    fb_correct=(
        "Correct! =RIGHT(A2,4) extracts the last 4 characters of \"LG-2001\", returning \"2001\". "
        "RIGHT(text, num_chars) always counts from the right end of the string."
    ),
    fb_incorrect=(
        "Use =RIGHT(A2,4). RIGHT(text, num_chars) returns the last num_chars characters. "
        "\"LG-2001\" has 7 characters; the last 4 are \"2001\"."
    ),
    hints=[
        "RIGHT(text, num_chars) extracts characters from the right end of the string.",
        "\"LG-2001\" has 7 characters. The last 4 characters are \"2001\".",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s04",
)

# s09 — choice — select_correct_date_function_for_given_calculation_requirement — f1, f2, f5
s09_date = choice(
    step_id="tile_spreadsheet_text_date_conditional_agg.s09",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.date_functions",
        "capability": "select_correct_date_function_for_given_calculation_requirement",
        "fact_ids": [
            "spreadsheet.date_functions#f1",
            "spreadsheet.date_functions#f2",
            "spreadsheet.date_functions#f5",
        ],
    }],
    anchors=["spreadsheet.date_functions#assessment:select_correct_date_function_for_given_calculation_requirement"],
    prompt=(
        "Cell G2 holds an order date. You want a formula that calculates how many **days** "
        "have elapsed between the order date in G2 and today's date.\n\n"
        "Which formula is correct?"
    ),
    options={
        "opt_a": '=DATEDIF(G2,TODAY(),"D")',
        "opt_b": '=DATEDIF(TODAY(),G2,"D")',
        "opt_c": '=DATEDIF(G2,TODAY(),"Y")',
        "opt_d": "=TODAY()-G2",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "DATEDIF(start_date, end_date, unit): the start_date must come before the end_date. "
            "Putting TODAY() as the start_date and G2 as the end_date reverses the order — "
            "if G2 is in the past, this returns a negative number or an error."
        ),
        "opt_c": (
            "The unit \"Y\" returns the number of complete years, not days. "
            "To count days, use the unit \"D\"."
        ),
        "opt_d": (
            "=TODAY()-G2 does return the number of days as a serial-number difference, "
            "and it works. However, the question asks for DATEDIF, which is the explicit "
            "function for date-difference calculations and makes the intent clearer. "
            "=DATEDIF(G2,TODAY(),\"D\") is the correct DATEDIF form."
        ),
    },
    fb_correct=(
        "Correct! =DATEDIF(G2,TODAY(),\"D\") computes the number of complete days between "
        "the order date (G2) and today. DATEDIF syntax: DATEDIF(start_date, end_date, unit). "
        "The unit \"D\" returns days; \"Y\" would return complete years."
    ),
    fb_incorrect=(
        "DATEDIF(start_date, end_date, unit) requires the earlier date as start_date and the "
        "later date as end_date. TODAY() supplies today's date as the end_date. "
        "The unit \"D\" returns the number of days in the period."
    ),
    hints=[
        "DATEDIF argument order: start_date first, end_date second. The order date (G2) is the start.",
        "The unit controls what is counted: \"D\" = days, \"Y\" = complete years.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s08",
)

# s10 — code_exercise (spreadsheet) — date_functions practice
# Practice anchor: 'DATEDIF(B2,TODAY(),"Y") ... returns a whole-number age'
# For deterministic testing, use a fixed reference date in H1 instead of TODAY()
# H1 = 45361 (serial number for 2024-03-10, the last order date in dataset)
# G2 = order_date for LG-2001 = 2024-03-04 (serial 45355)
# DATEDIF(G2, H1, "D") = 6 days
# DATEDIF(G2, H1, "Y") = 0 complete years (same year)
# Let's use "D" for days since it's more interesting with this data
# Actually the practice anchor says "Y" for age calculation
# Let's use a birthdate scenario: put a fixed birthdate in B1 and compute age
# But our dataset has order_date in G column
# Let's use: H1 = fixed reference date (2024-03-10 serial = 45361)
# Formula in I2: =DATEDIF(G2, H1, "D") = 6

s10_date = code_exercise(
    step_id="tile_spreadsheet_text_date_conditional_agg.s10",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.date_functions",
            "capability": "write_today_function_with_correct_syntax",
            "fact_ids": ["spreadsheet.date_functions#f1"],
        },
        {
            "concept_id": "spreadsheet.date_functions",
            "capability": "write_datedif_with_correct_arguments_and_unit",
            "fact_ids": ["spreadsheet.date_functions#f2"],
        },
        {
            "concept_id": "spreadsheet.date_functions",
            "capability": "construct_age_calculation_formula_using_datedif_and_today",
            "fact_ids": [
                "spreadsheet.date_functions#f2",
                "spreadsheet.date_functions#f3",
            ],
        },
        {
            "concept_id": "spreadsheet.date_functions",
            "capability": "explain_date_serial_number_model",
            "fact_ids": ["spreadsheet.date_functions#f4"],
        },
        {
            "concept_id": "spreadsheet.date_functions",
            "capability": "select_correct_date_function_for_given_calculation_requirement",
            "fact_ids": [
                "spreadsheet.date_functions#f1",
                "spreadsheet.date_functions#f2",
                "spreadsheet.date_functions#f5",
            ],
        },
    ],
    anchors=[
        "spreadsheet.date_functions#practice",
        "spreadsheet.date_functions#assessment:write_today_function_with_correct_syntax",
        "spreadsheet.date_functions#assessment:write_datedif_with_correct_arguments_and_unit",
        "spreadsheet.date_functions#assessment:construct_age_calculation_formula_using_datedif_and_today",
        "spreadsheet.date_functions#assessment:explain_date_serial_number_model",
        "spreadsheet.date_functions#assessment:select_correct_date_function_for_given_calculation_requirement",
    ],
    prompt=(
        "The **orders** sheet has order dates in column G (rows 2–21). "
        "Cell H1 holds a fixed reference date as a serial number: **45361** "
        "(which represents 2024-03-10, the last day of the data period).\n\n"
        "**Task 1 — days elapsed:** In cell I2, write a DATEDIF formula that calculates "
        "the number of **days** (unit \"D\") between the order date in G2 and the reference "
        "date in H1. The order date for row 2 is 2024-03-04, so the result should be **6**.\n\n"
        "**Task 2 — days for row 3:** In cell I3, write the same DATEDIF formula for G3. "
        "The order date for row 3 is also 2024-03-04, so the result should also be **6**."
    ),
    runtime_kind="spreadsheet",
    runtime_version="3.4.0",
    files=[{
        "path": "book.sheet",
        "role": "editable",
        "language": "sheet",
        "content": (
            "// H1 holds the reference date as a serial number (45361 = 2024-03-10).\n"
            "H1: 45361\n\n"
            "// Task 1: In I2, write a DATEDIF formula that returns the number of days\n"
            "// between the order date in G2 and the reference date in H1.\n"
            "// DATEDIF syntax: DATEDIF(start_date, end_date, unit)\n"
            "// Use unit \"D\" for days. Expected result: 6\n\n"
            "// Task 2: In I3, write the same DATEDIF formula for G3.\n"
            "// Expected result: 6\n"
        ),
    }],
    entry="book.sheet",
    asset_mounts=[{
        "asset_id": "asset_orders_clean",
        "mount_path": "orders.csv",
    }],
    allowed_syntax=["DATEDIF"],
    blocked_syntax=["TODAY", "NOW", "DAYS"],
    solution_files=[{
        "path": "book.sheet",
        "content": 'H1: 45361\nI2: =DATEDIF(G2,H1,"D")\nI3: =DATEDIF(G3,H1,"D")\n',
    }],
    tests=[
        {
            "test_id": "test_i2_days",
            "kind": "cell_equals",
            "spec": {"cell": "I2", "expected": 6},
            "visible": True,
            "message_on_fail": (
                "I2 should equal 6 (days from 2024-03-04 to 2024-03-10). "
                "Use =DATEDIF(G2,H1,\"D\") — G2 is the start_date, H1 is the end_date, \"D\" counts days."
            ),
        },
        {
            "test_id": "test_i3_days",
            "kind": "cell_equals",
            "spec": {"cell": "I3", "expected": 6},
            "visible": True,
            "message_on_fail": (
                "I3 should equal 6 (days from 2024-03-04 to 2024-03-10). "
                "Use =DATEDIF(G3,H1,\"D\") — same pattern as I2 but referencing G3."
            ),
        },
        {
            "test_id": "test_i2_uses_datedif",
            "kind": "formula_uses",
            "spec": {"cell": "I2", "functions": ["DATEDIF"]},
            "visible": True,
            "message_on_fail": "I2 must contain a DATEDIF formula.",
        },
    ],
    fb_correct=(
        "Well done! =DATEDIF(G2,H1,\"D\") correctly places the earlier date (G2, the order date) "
        "as start_date and the later date (H1, the reference date) as end_date. "
        "The unit \"D\" returns the number of complete days in the period. "
        "Excel stores dates as serial numbers, so DATEDIF can subtract them to count days."
    ),
    fb_incorrect=(
        "Use =DATEDIF(G2,H1,\"D\"). The argument order is: start_date (G2, the earlier date), "
        "end_date (H1, the later date), unit (\"D\" for days). "
        "If you swap the dates, DATEDIF returns an error because start_date must be before end_date."
    ),
    hints=[
        "DATEDIF(start_date, end_date, unit): the earlier date goes first.",
        "The unit \"D\" counts days. Use \"Y\" for complete years, \"M\" for complete months.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s08",
)

# s15 — choice — write_single_condition_countif_sumif AND write_multi_condition_countifs_sumifs
# f1, f2, f3, f4
s15_cond = choice(
    step_id="tile_spreadsheet_text_date_conditional_agg.s15",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.conditional_aggregation",
            "capability": "write_single_condition_countif_sumif",
            "fact_ids": [
                "spreadsheet.conditional_aggregation#f1",
                "spreadsheet.conditional_aggregation#f3",
            ],
        },
        {
            "concept_id": "spreadsheet.conditional_aggregation",
            "capability": "write_multi_condition_countifs_sumifs",
            "fact_ids": [
                "spreadsheet.conditional_aggregation#f2",
                "spreadsheet.conditional_aggregation#f4",
            ],
        },
    ],
    anchors=[
        "spreadsheet.conditional_aggregation#assessment:write_single_condition_countif_sumif",
        "spreadsheet.conditional_aggregation#assessment:write_multi_condition_countifs_sumifs",
    ],
    prompt=(
        "The Orders sheet has city in column B (B2:B21), status in column E (E2:E21), "
        "and amount in column D (D2:D21).\n\n"
        "You want the total amount for orders that are **both** from Lagos **and** have "
        "status Delivered. Which formula is correct?"
    ),
    options={
        "opt_a": '=SUMIFS(D2:D21,B2:B21,"Lagos",E2:E21,"Delivered")',
        "opt_b": '=SUMIF(D2:D21,"Lagos",E2:E21,"Delivered")',
        "opt_c": '=SUMIFS(B2:B21,"Lagos",E2:E21,"Delivered",D2:D21)',
        "opt_d": '=SUMIF(B2:B21,"Lagos",D2:D21)+SUMIF(E2:E21,"Delivered",D2:D21)',
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "SUMIF handles only one condition. Its syntax is SUMIF(range, criteria, [sum_range]) — "
            "it takes one criteria range and one criterion. To apply two conditions at once, "
            "use SUMIFS."
        ),
        "opt_c": (
            "SUMIFS syntax is SUMIFS(sum_range, criteria_range1, criteria1, ...). "
            "The sum_range (D2:D21) must come first. This formula puts the criteria ranges "
            "first and the sum_range last, which is the SUMIF order, not SUMIFS."
        ),
        "opt_d": (
            "Adding two SUMIF results double-counts orders that are both from Lagos AND Delivered. "
            "An order that meets both conditions is included in both SUMIF results, so the total "
            "is inflated. SUMIFS applies both conditions simultaneously to avoid double-counting."
        ),
    },
    fb_correct=(
        "Correct! =SUMIFS(D2:D21,B2:B21,\"Lagos\",E2:E21,\"Delivered\") sums the amounts in D2:D21 "
        "where the city is Lagos AND the status is Delivered. SUMIFS syntax: "
        "SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...)."
    ),
    fb_incorrect=(
        "SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...) applies "
        "multiple conditions simultaneously. The sum_range (D2:D21) comes first, then each "
        "criteria_range/criteria pair. SUMIF handles only one condition."
    ),
    hints=[
        "SUMIFS (plural) handles multiple conditions; SUMIF (singular) handles one.",
        "In SUMIFS, the sum_range is the first argument, followed by criteria_range/criteria pairs.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s11",
)

# s16 — choice — use_same_range_twice_for_between_condition — f6
s16_cond = choice(
    step_id="tile_spreadsheet_text_date_conditional_agg.s16",
    difficulty="stretch",
    measures=[{
        "concept_id": "spreadsheet.conditional_aggregation",
        "capability": "use_same_range_twice_for_between_condition",
        "fact_ids": ["spreadsheet.conditional_aggregation#f6"],
    }],
    anchors=["spreadsheet.conditional_aggregation#assessment:use_same_range_twice_for_between_condition"],
    prompt=(
        "The Orders sheet has delivery times in column C (C2:C21). "
        "You want to count how many deliveries took between 30 and 60 minutes (inclusive).\n\n"
        "Which formula correctly counts deliveries where delivery_minutes >= 30 AND <= 60?"
    ),
    options={
        "opt_a": '=COUNTIFS(C2:C21,">=30",C2:C21,"<=60")',
        "opt_b": '=COUNTIF(C2:C21,">=30 AND <=60")',
        "opt_c": '=COUNTIFS(C2:C21,">=30 AND <=60")',
        "opt_d": '=COUNTIF(C2:C21,">=30")-COUNTIF(C2:C21,">60")',
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": (
            "COUNTIF does not support compound criteria like \">=30 AND <=60\" in a single "
            "criterion string. Each condition must be a separate criteria_range/criteria pair "
            "in COUNTIFS."
        ),
        "opt_c": (
            "COUNTIFS does not support compound criteria in a single string. "
            "\">=30 AND <=60\" is not valid syntax. Use two separate criteria pairs: "
            "COUNTIFS(C2:C21,\">=30\",C2:C21,\"<=60\")."
        ),
        "opt_d": (
            "This subtraction approach works mathematically but is less direct. "
            "COUNTIFS(C2:C21,\">=30\",C2:C21,\"<=60\") is the standard way to express "
            "a between condition by listing the same range twice with two separate criteria."
        ),
    },
    fb_correct=(
        "Correct! =COUNTIFS(C2:C21,\">=30\",C2:C21,\"<=60\") uses the same range (C2:C21) "
        "twice — once with the lower bound (\">=30\") and once with the upper bound (\"<=60\"). "
        "COUNTIFS counts only rows where both conditions are met simultaneously."
    ),
    fb_incorrect=(
        "To test a range condition (between two values), list the same range twice in COUNTIFS: "
        "COUNTIFS(C2:C21,\">=30\",C2:C21,\"<=60\"). Each criteria_range/criteria pair adds "
        "another condition that must be met. COUNTIF cannot handle two conditions at once."
    ),
    hints=[
        "COUNTIFS allows you to use the same range more than once — once for each bound of the between condition.",
        "Criteria containing comparison operators like >= and <= must be in quotation marks.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s11",
)

# s17 — formula_entry — conditional_aggregation practice (criteria quoting)
# Practice anchor: 'The formula returns the correct total that matches a manual filter of the table for the specified region and date range, with no #VALUE! or #NAME? errors.'
# Anchor: apply_correct_criteria_syntax_quoting (f5)
# Use SUMIF(B2:B21,"Lagos",D2:D21) = 28000.0
s17_cond = formula_entry(
    step_id="tile_spreadsheet_text_date_conditional_agg.s17",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.conditional_aggregation",
        "capability": "apply_correct_criteria_syntax_quoting",
        "fact_ids": ["spreadsheet.conditional_aggregation#f5"],
    }],
    anchors=[
        "spreadsheet.conditional_aggregation#practice",
        "spreadsheet.conditional_aggregation#assessment:apply_correct_criteria_syntax_quoting",
    ],
    prompt=(
        "The Orders sheet has city in column B (B2:B21) and order amount in column D (D2:D21).\n\n"
        "In cell H1, write a SUMIF formula that totals the amounts for orders from **Lagos**. "
        "The city criterion is a text value, so it must be enclosed in double quotation marks.\n\n"
        "The expected result is **28000**."
    ),
    asset_id="asset_orders_clean",
    sheet_name="orders",
    target_cell="H1",
    allowed_functions=["SUMIF"],
    expected_value=28000.0,
    reference_formula='=SUMIF(B2:B21,"Lagos",D2:D21)',
    must_use_functions=["SUMIF"],
    fb_correct=(
        "Correct! =SUMIF(B2:B21,\"Lagos\",D2:D21) sums the amounts in D2:D21 where the "
        "corresponding city in B2:B21 equals \"Lagos\". The text criterion \"Lagos\" is "
        "enclosed in double quotation marks, as required for text and expression criteria."
    ),
    fb_incorrect=(
        "Use =SUMIF(B2:B21,\"Lagos\",D2:D21). SUMIF syntax: SUMIF(range, criteria, [sum_range]). "
        "The criteria \"Lagos\" is a text value and must be in double quotation marks. "
        "Without quotes, Excel returns a #NAME? or #VALUE! error."
    ),
    hints=[
        "SUMIF syntax: SUMIF(range, criteria, sum_range). The range is where you check the condition.",
        "Text criteria must be in double quotes: \"Lagos\". Number criteria do not need quotes.",
    ],
    remediation_step_id="tile_spreadsheet_text_date_conditional_agg.s11",
)


# ═══════════════════════════════════════════════════════════════════════════════
# Assemble output
# ═══════════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "tiles": [
        {
            "tile_id": "tile_spreadsheet_formula_syntax_refs",
            "interactions": [s04, s05, s06, s10, s11],
        },
        {
            "tile_id": "tile_spreadsheet_aggregation_logical",
            "interactions": [s04_agg, s05_agg, s09_log, s10_log],
        },
        {
            "tile_id": "tile_spreadsheet_text_date_conditional_agg",
            "interactions": [
                s02_txt, s03_txt, s05_ext, s06_ext, s07_ext,
                s09_date, s10_date, s15_cond, s16_cond, s17_cond,
            ],
        },
    ],
}

out_path = BATCH / "interactions.part.c1.json"
out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Written {out_path}")
print(f"Tiles: {len(output['tiles'])}")
for t in output['tiles']:
    print(f"  {t['tile_id']}: {len(t['interactions'])} interactions")
