"""Build interactions.part.c1.json for chunk c1:
  tile_python_operators_conversion
  tile_python_lists_dicts_tuples
  tile_python_sets_strings

Constraints are loaded verbatim from the glossary bundle (never hand-typed).
"""
import json
from pathlib import Path

BATCH = Path(__file__).parent
OUT = BATCH / "interactions.part.c1.json"
GLOSSARY = BATCH / "inputs" / "path_glossary_bundle.json"

PYODIDE_VERSION = "0.29.5"

# ─────────────────────────────────────────────────────────────────────────────
# Load constraints verbatim from glossary
# ─────────────────────────────────────────────────────────────────────────────

with open(GLOSSARY) as f:
    _g = json.load(f)

_CONSTRAINTS = {}
for _b in _g["bundles"]:
    _cid = _b["context"]["concept_id"]
    _pa = _b.get("practice_anchor", {})
    _lc = _pa.get("live_code", {})
    _CONSTRAINTS[_cid] = {
        "allowed_syntax": list(_lc.get("allowed_syntax", [])),
        "blocked_syntax": list(_lc.get("blocked_syntax", [])),
    }


def _constraints(concept_id):
    return _CONSTRAINTS[concept_id]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def choice(step_id, difficulty, standalone, measures, anchors, prompt, options, correct_ids, option_feedback, correct_msg, incorrect_msg, hints, remediation_step_id=None):
    fb = {
        "correct": {"message": correct_msg},
        "incorrect": {"message": incorrect_msg},
        "hints": hints,
    }
    if remediation_step_id:
        fb["remediation_step_id"] = remediation_step_id
    ix = {
        "type": "choice",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": standalone,
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
        "feedback": fb,
    }
    return {"step_id": step_id, "interaction": ix}


def code_ex(step_id, difficulty, standalone, measures, anchors, prompt, starter_content, solution_content, tests, correct_msg, incorrect_msg, hints, concept_id_for_constraints, remediation_step_id=None):
    c = _constraints(concept_id_for_constraints)
    fb = {
        "correct": {"message": correct_msg},
        "incorrect": {"message": incorrect_msg},
        "hints": hints,
    }
    if remediation_step_id:
        fb["remediation_step_id"] = remediation_step_id
    ix = {
        "type": "code_exercise",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": standalone,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "prompt": prompt,
            "runtime": {"kind": "python", "version": PYODIDE_VERSION},
            "workspace": {
                "files": [
                    {
                        "path": "solution.py",
                        "role": "editable",
                        "language": "python",
                        "content": starter_content,
                    }
                ],
                "entry": "solution.py",
            },
            "constraints": {
                "allowed_syntax": c["allowed_syntax"],
                "blocked_syntax": c["blocked_syntax"],
            },
        },
        "grading": {
            "solution_files": [{"path": "solution.py", "content": solution_content}],
            "tests": tests,
        },
        "feedback": fb,
    }
    return {"step_id": step_id, "interaction": ix}


# ─────────────────────────────────────────────────────────────────────────────
# tile_python_operators_conversion
# ─────────────────────────────────────────────────────────────────────────────

# s02 — check: predict_grouped_and_mixed_type_result (f4, f5)
# Taught in s01 (explainer covering f1-f5)
s02 = choice(
    step_id="tile_python_operators_conversion.s02",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.arithmetic_operators",
        "capability": "predict_grouped_and_mixed_type_result",
        "fact_ids": ["f4", "f5"],
    }],
    anchors=["python.arithmetic_operators#assessment:predict_grouped_and_mixed_type_result"],
    prompt=(
        "What does Python evaluate `4 * 3.75 - 1` to?\n\n"
        "*(Hint: mixed int/float operands convert the integer to float.)*"
    ),
    options={
        "opt_a": "`14.0` — a float, because one operand is a float",
        "opt_b": "`14` — an int, because the result is a whole number",
        "opt_c": "`13.0` — subtraction happens before multiplication",
        "opt_d": "`15.0` — Python rounds up when mixing types",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `4 * 3.75` is `15.0` (float), then `15.0 - 1` is `14.0`. When an int and a float are combined, the int is converted to float first.",
        "opt_b": "The result is a float, not an int. When any operand is a float, Python converts the int operand to float, so the result is `14.0`, not `14`.",
        "opt_c": "Multiplication and division have higher precedence than subtraction, so `4 * 3.75` is evaluated first, giving `15.0`, then `15.0 - 1 = 14.0`.",
        "opt_d": "Python does not round when mixing types. It converts the int to float and computes exactly: `4 * 3.75 = 15.0`, then `15.0 - 1 = 14.0`.",
    },
    correct_msg="Right — `4 * 3.75 - 1` evaluates to `14.0`. Multiplication runs first (higher precedence), and the int `4` is converted to float because `3.75` is a float.",
    incorrect_msg="Remember: `*` has higher precedence than `-`, so `4 * 3.75 = 15.0` first. Then `15.0 - 1 = 14.0`. Any int mixed with a float gives a float result.",
    hints=[
        "Which operator has higher precedence: `*` or `-`? Apply that one first.",
        "When one operand is a float (like `3.75`), what type does Python use for the result?",
    ],
    remediation_step_id="tile_python_operators_conversion.r01",
)

# s03 — hands_on: arithmetic operators practice (f1, f2, f3)
# Taught in s01 (explainer covering f1-f5)
# success: Each derived value prints the correct number, with / giving a float and // and % giving the quotient and remainder.
# orders_per_driver = 20, days_worked = 5
# total = 20 * 5 = 100, avg = 100 / 5 = 20.0, quotient = 100 // 3 = 33, remainder = 100 % 3 = 1
# stdout: "100\n20.0\n33\n1"
s03 = code_ex(
    step_id="tile_python_operators_conversion.s03",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.arithmetic_operators", "capability": "choose_arithmetic_operator", "fact_ids": ["f1"]},
        {"concept_id": "python.arithmetic_operators", "capability": "use_floor_division_and_remainder", "fact_ids": ["f2"]},
        {"concept_id": "python.arithmetic_operators", "capability": "use_power_operator", "fact_ids": ["f3"]},
    ],
    anchors=[
        "python.arithmetic_operators#practice",
        "python.arithmetic_operators#assessment:choose_arithmetic_operator",
        "python.arithmetic_operators#assessment:use_floor_division_and_remainder",
        "python.arithmetic_operators#assessment:use_power_operator",
    ],
    prompt=(
        "QuickDeliver's analytics team needs four derived values from two base numbers.\n\n"
        "`orders_per_driver` and `days_worked` are already assigned below.\n\n"
        "Add four lines that compute and print:\n"
        "1. `total` — `orders_per_driver` multiplied by `days_worked`\n"
        "2. `avg` — `total` divided by `days_worked` (use `/`; the result must be a float)\n"
        "3. `quotient` — `total` floor-divided by `3` (use `//`)\n"
        "4. `remainder` — `total` modulo `3` (use `%`)\n\n"
        "Print each variable on its own line in the order above.\n\n"
        "Expected output:\n"
        "```\n"
        "100\n"
        "20.0\n"
        "33\n"
        "1\n"
        "```"
    ),
    starter_content=(
        "orders_per_driver = 20\n"
        "days_worked = 5\n"
        "# Compute total, avg, quotient, remainder and print each\n"
    ),
    solution_content=(
        "orders_per_driver = 20\n"
        "days_worked = 5\n"
        "total = orders_per_driver * days_worked\n"
        "avg = total / days_worked\n"
        "quotient = total // 3\n"
        "remainder = total % 3\n"
        "print(total)\n"
        "print(avg)\n"
        "print(quotient)\n"
        "print(remainder)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "100\n20.0\n33\n1"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `total`, `avg`, `quotient`, `remainder` each on its own line, in that order.",
        },
        {
            "test_id": "t2_avg_float",
            "kind": "value_equals",
            "spec": {"expr": "avg", "expected": 20.0},
            "visible": True,
            "message_on_fail": "`avg` should be `20.0` (a float). Use `/` for division, not `//`.",
        },
    ],
    correct_msg="All four values correct — `total=100`, `avg=20.0` (float from `/`), `quotient=33` and `remainder=1` from `//` and `%`.",
    incorrect_msg="Check each operator: `*` for total, `/` for avg (must give a float), `//` for floor quotient, `%` for remainder. Print them in order.",
    hints=[
        "For `avg`, use `/` (not `//`) — regular division always returns a float in Python 3.",
        "For `quotient` and `remainder`, use `//` and `%` on `total` divided by `3`.",
    ],
    concept_id_for_constraints="python.arithmetic_operators",
    remediation_step_id="tile_python_operators_conversion.r01",
)

# s05 — check: write_comparison_expression (f1, f2)
# Taught in s04 (explainer covering f1, f2)
s05 = choice(
    step_id="tile_python_operators_conversion.s05",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.comparison_operators",
        "capability": "write_comparison_expression",
        "fact_ids": ["f1", "f2"],
    }],
    anchors=["python.comparison_operators#assessment:write_comparison_expression"],
    prompt=(
        "A QuickDeliver order has `delivery_minutes = 60` and the SLA threshold is `45` minutes.\n\n"
        "Which expression correctly checks whether the delivery exceeded the SLA?"
    ),
    options={
        "opt_a": "`delivery_minutes > 45`",
        "opt_b": "`delivery_minutes = 45`",
        "opt_c": "`delivery_minutes => 45`",
        "opt_d": "`delivery_minutes <> 45`",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `delivery_minutes > 45` evaluates to `True` when `delivery_minutes` is `60`, meaning the delivery exceeded the SLA.",
        "opt_b": "`=` is the assignment operator, not a comparison. To compare two values, use `>`, `<`, `==`, `!=`, `>=`, or `<=`.",
        "opt_c": "Python does not have a `=>` operator. The greater-than-or-equal operator is `>=` (the `>` comes first).",
        "opt_d": "`<>` is not valid Python syntax. To check inequality, use `!=`.",
    },
    correct_msg="Right — `delivery_minutes > 45` is `True` when `delivery_minutes` is `60`. The six comparison operators are `<`, `<=`, `>`, `>=`, `==`, and `!=`.",
    incorrect_msg="Use one of the six comparison operators: `<`, `<=`, `>`, `>=`, `==`, `!=`. Remember that `=` is assignment, not comparison.",
    hints=[
        "To check if one value is greater than another, which operator do you use?",
        "Python's comparison operators are `<`, `<=`, `>`, `>=`, `==`, `!=`. Which one means 'greater than'?",
    ],
    remediation_step_id="tile_python_operators_conversion.r02",
)

# s06 — check: predict_boolean_result_of_comparison (f2)
# Taught in s04 (explainer covering f1, f2)
s06 = choice(
    step_id="tile_python_operators_conversion.s06",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.comparison_operators",
        "capability": "predict_boolean_result_of_comparison",
        "fact_ids": ["f2"],
    }],
    anchors=["python.comparison_operators#assessment:predict_boolean_result_of_comparison"],
    prompt=(
        "After running:\n\n"
        "```python\n"
        "delivery_minutes = 45\n"
        "sla = 45\n"
        "print(delivery_minutes == sla)\n"
        "print(delivery_minutes > sla)\n"
        "```\n\n"
        "What is printed?"
    ),
    options={
        "opt_a": "`True` then `False`",
        "opt_b": "`True` then `True`",
        "opt_c": "`False` then `True`",
        "opt_d": "`False` then `False`",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `45 == 45` is `True` (equal values), and `45 > 45` is `False` (not strictly greater).",
        "opt_b": "`45 > 45` is `False`, not `True`. The `>` operator requires the left side to be strictly greater than the right.",
        "opt_c": "`45 == 45` is `True`, not `False`. Two equal values satisfy `==`.",
        "opt_d": "`45 == 45` is `True` because both sides are equal. Only `45 > 45` is `False`.",
    },
    correct_msg="Correct — `45 == 45` is `True` (equal), and `45 > 45` is `False` (not strictly greater). Comparisons always return a boolean.",
    incorrect_msg="`==` checks equality (both sides equal → `True`), while `>` checks strict greater-than (`45 > 45` is `False` because they are equal, not greater).",
    hints=[
        "Does `==` return `True` when both sides are the same value?",
        "Does `>` return `True` when both sides are equal, or only when the left is strictly larger?",
    ],
)

# s07 — hands_on: comparison operators practice
# success: Each check prints True or False correctly for values below, at and above the threshold.
# dm_below=32, dm_at=45, dm_above=60, sla=45
# print(dm_below < sla) -> True, print(dm_at == sla) -> True, print(dm_above > sla) -> True
# stdout: "True\nTrue\nTrue"
s07 = code_ex(
    step_id="tile_python_operators_conversion.s07",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.comparison_operators", "capability": "write_comparison_expression", "fact_ids": ["f1", "f2"]},
        {"concept_id": "python.comparison_operators", "capability": "predict_boolean_result_of_comparison", "fact_ids": ["f2"]},
    ],
    anchors=["python.comparison_operators#practice"],
    prompt=(
        "QuickDeliver's SLA is 45 minutes. Three delivery times are assigned below: one below, one at, and one above the threshold.\n\n"
        "Add three `print()` calls that each output a boolean:\n"
        "1. Whether `dm_below` is **less than** `sla`\n"
        "2. Whether `dm_at` is **equal to** `sla`\n"
        "3. Whether `dm_above` is **greater than** `sla`\n\n"
        "Expected output:\n"
        "```\n"
        "True\n"
        "True\n"
        "True\n"
        "```"
    ),
    starter_content=(
        "dm_below = 32\n"
        "dm_at = 45\n"
        "dm_above = 60\n"
        "sla = 45\n"
        "# Print three boolean results: dm_below < sla, dm_at == sla, dm_above > sla\n"
    ),
    solution_content=(
        "dm_below = 32\n"
        "dm_at = 45\n"
        "dm_above = 60\n"
        "sla = 45\n"
        "print(dm_below < sla)\n"
        "print(dm_at == sla)\n"
        "print(dm_above > sla)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "True\nTrue\nTrue"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `dm_below < sla`, `dm_at == sla`, `dm_above > sla` each on its own line.",
        },
    ],
    correct_msg="All three comparisons correct — `32 < 45` is `True`, `45 == 45` is `True`, and `60 > 45` is `True`.",
    incorrect_msg="Check each comparison: use `<` for 'less than', `==` for 'equal to', and `>` for 'greater than'. Each `print()` should wrap one comparison expression.",
    hints=[
        "Each `print()` call should look like `print(variable operator sla)`. Which operator goes with each check?",
        "Remember: `==` (two equals signs) tests equality; `=` (one equals sign) is assignment.",
    ],
    concept_id_for_constraints="python.comparison_operators",
    remediation_step_id="tile_python_operators_conversion.r02",
)

# s10 — check: predict_operator_priority (f1, f4)
# Taught in s08 (f1, f2, f3) and s09 (f2, f3, f4)
s10 = choice(
    step_id="tile_python_operators_conversion.s10",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.logical_operators",
        "capability": "predict_operator_priority",
        "fact_ids": ["f1", "f4"],
    }],
    anchors=["python.logical_operators#assessment:predict_operator_priority"],
    prompt=(
        "What does Python evaluate `not is_late == False` to when `is_late = True`?\n\n"
        "*(Hint: `not` has lower priority than comparison operators.)*"
    ),
    options={
        "opt_a": "`True` — `not` applies to the result of `is_late == False`",
        "opt_b": "`False` — `not is_late` is evaluated first, then compared to `False`",
        "opt_c": "`True` — `not is_late` is `False`, and `False == False` is `True`",
        "opt_d": "A `SyntaxError` — `not` cannot appear before a comparison",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `not` has lower priority than `==`, so Python reads `not (is_late == False)`. `is_late == False` is `True == False` which is `False`, then `not False` is `True`.",
        "opt_b": "This would be correct if `not` had higher priority than `==`, but it does not. `not` is evaluated last, so `is_late == False` is computed first.",
        "opt_c": "This is the result if `not is_late` were evaluated first (giving `False`), then `False == False` giving `True`. But `not` has lower priority than `==`, so `is_late == False` is evaluated first.",
        "opt_d": "`not` is a valid operator and can appear before a comparison expression. Python evaluates the comparison first, then applies `not`.",
    },
    correct_msg="Right — `not` has lower priority than `==`, so Python evaluates `is_late == False` first (`True == False` = `False`), then `not False` = `True`.",
    incorrect_msg="Remember: `not` has lower priority than comparison operators. Python evaluates `is_late == False` first, then applies `not` to the result.",
    hints=[
        "The priority order (ascending) is: `or`, `and`, `not`, then comparison operators. Which is evaluated first: `==` or `not`?",
        "Rewrite the expression with explicit parentheses to show which part Python evaluates first.",
    ],
    remediation_step_id="tile_python_operators_conversion.r03",
)

# s11 — check: predict_short_circuit_result (f2, f3)
# Taught in s08 (f1, f2, f3) and s09 (f2, f3, f4)
s11 = choice(
    step_id="tile_python_operators_conversion.s11",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.logical_operators",
        "capability": "predict_short_circuit_result",
        "fact_ids": ["f2", "f3"],
    }],
    anchors=["python.logical_operators#assessment:predict_short_circuit_result"],
    prompt=(
        "Given `is_late = False` and `is_far = True`, what does `is_late and is_far` evaluate to?"
    ),
    options={
        "opt_a": "`False` — `and` short-circuits: if the left side is false, it returns the left side without evaluating the right",
        "opt_b": "`True` — `and` returns `True` if either operand is `True`",
        "opt_c": "`False` — `and` always returns `False` unless both sides are `True`",
        "opt_d": "`True` — `and` evaluates both sides and returns the last one",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `x and y` returns `x` if `x` is false (short-circuit), so `False and is_far` returns `False` without evaluating `is_far`.",
        "opt_b": "That describes `or`, not `and`. `and` requires both sides to be true; if the left side is false, it short-circuits and returns the left side.",
        "opt_c": "The result is correct (`False`), but the reason is short-circuiting: `and` returns the left operand (`False`) without evaluating the right side at all.",
        "opt_d": "That describes `or` when the left side is true. For `and`, if the left side is false, Python returns it immediately without evaluating the right side.",
    },
    correct_msg="Correct — `and` short-circuits: `False and is_far` returns `False` immediately, without evaluating `is_far`.",
    incorrect_msg="`x and y` returns `x` if `x` is false (short-circuit). Since `is_late` is `False`, Python returns `False` without checking `is_far`.",
    hints=[
        "For `x and y`: if `x` is false, what does Python return — and does it even look at `y`?",
        "Short-circuit means Python stops as soon as the result is determined. Can `True and False` change the result of `False and ...`?",
    ],
)

# s12 — hands_on: logical operators practice (f1, f2, f3, f4)
# success: The compound expression prints the expected True or False for sample values of is_late and is_far,
# including a case where the priority of and over or matters.
# Case 1: is_late=True, is_far=False -> True or (False and False) = True
# Case 2: is_late=False, is_far=True -> False or (True and True) = True
# Case 3: is_late=False, is_far=False -> False or (False and True) = False
# stdout: "True\nTrue\nFalse"
s12 = code_ex(
    step_id="tile_python_operators_conversion.s12",
    difficulty="stretch",
    standalone=False,
    measures=[
        {"concept_id": "python.logical_operators", "capability": "write_compound_boolean_expression", "fact_ids": ["f1", "f2", "f3", "f4"]},
        {"concept_id": "python.logical_operators", "capability": "predict_operator_priority", "fact_ids": ["f1", "f4"]},
        {"concept_id": "python.logical_operators", "capability": "predict_short_circuit_result", "fact_ids": ["f2", "f3"]},
    ],
    anchors=[
        "python.logical_operators#practice",
        "python.logical_operators#assessment:write_compound_boolean_expression",
    ],
    prompt=(
        "QuickDeliver flags an order for review if it is late **or** it is far **and** it is not late "
        "(i.e. far but on time — a different concern).\n\n"
        "The expression is: `is_late or is_far and not is_late`\n\n"
        "Three sets of values are assigned below. For each set, add one `print()` call that evaluates "
        "the expression `is_late or is_far and not is_late` using those values.\n\n"
        "Expected output:\n"
        "```\n"
        "True\n"
        "True\n"
        "False\n"
        "```\n\n"
        "*(The third case — `is_late=False`, `is_far=False` — shows that `and` binds tighter than `or`.)*"
    ),
    starter_content=(
        "# Case 1: late but not far\n"
        "is_late = True\n"
        "is_far = False\n"
        "# print the compound expression here\n"
        "\n"
        "# Case 2: not late but far\n"
        "is_late = False\n"
        "is_far = True\n"
        "# print the compound expression here\n"
        "\n"
        "# Case 3: neither late nor far\n"
        "is_late = False\n"
        "is_far = False\n"
        "# print the compound expression here\n"
    ),
    solution_content=(
        "# Case 1: late but not far\n"
        "is_late = True\n"
        "is_far = False\n"
        "print(is_late or is_far and not is_late)\n"
        "\n"
        "# Case 2: not late but far\n"
        "is_late = False\n"
        "is_far = True\n"
        "print(is_late or is_far and not is_late)\n"
        "\n"
        "# Case 3: neither late nor far\n"
        "is_late = False\n"
        "is_far = False\n"
        "print(is_late or is_far and not is_late)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "True\nTrue\nFalse"},
            "visible": True,
            "message_on_fail": "Output does not match. Each `print()` should evaluate `is_late or is_far and not is_late` for the values assigned just above it.",
        },
    ],
    correct_msg="All three cases correct — `and` binds tighter than `or`, so `is_far and not is_late` is evaluated first, then combined with `is_late or ...`.",
    incorrect_msg="Use the expression `is_late or is_far and not is_late` exactly. Remember `and` has higher priority than `or`, so `is_far and not is_late` is evaluated first.",
    hints=[
        "Each `print()` call should be `print(is_late or is_far and not is_late)` — use the values assigned just above it.",
        "For case 1 (`is_late=True, is_far=False`): `is_far and not is_late` = `False and False` = `False`, then `True or False` = `True`.",
    ],
    concept_id_for_constraints="python.logical_operators",
    remediation_step_id="tile_python_operators_conversion.r03",
)

# s14 — check: convert_value_to_target_type (f1, f2, f3, f4)
# Taught in s13 (explainer covering f1-f6)
s14 = choice(
    step_id="tile_python_operators_conversion.s14",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.type_conversion",
        "capability": "convert_value_to_target_type",
        "fact_ids": ["f1", "f2", "f3", "f4"],
    }],
    anchors=["python.type_conversion#assessment:convert_value_to_target_type"],
    prompt=(
        "A CSV file stores delivery times as strings. The value `'45'` needs to be used in arithmetic.\n\n"
        "Which expression converts the string `'45'` to an integer?"
    ),
    options={
        "opt_a": "`int('45')`",
        "opt_b": "`float('45')`",
        "opt_c": "`str(45)`",
        "opt_d": "`bool('45')`",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `int('45')` returns the integer `45`, constructed from the string `'45'`.",
        "opt_b": "`float('45')` returns `45.0`, a floating-point number — not an integer. Use `int()` when you need a whole number.",
        "opt_c": "`str(45)` converts the integer `45` to the string `'45'` — the opposite direction. You need `int()` to go from string to integer.",
        "opt_d": "`bool('45')` returns `True` (any non-empty string is truthy), not an integer. Use `int()` to convert a numeric string to an integer.",
    },
    correct_msg="Right — `int('45')` constructs the integer `45` from the string `'45'`. This is the standard way to convert a numeric string to an integer.",
    incorrect_msg="To convert a string to an integer, use `int(string)`. `float()` gives a decimal, `str()` goes the other direction, and `bool()` gives `True`/`False`.",
    hints=[
        "Which constructor produces an integer object: `int()`, `float()`, `str()`, or `bool()`?",
        "The function name matches the type you want: `int()` → integer, `float()` → float, `str()` → string.",
    ],
    remediation_step_id="tile_python_operators_conversion.r04",
)

# s15 — check: recognize_invalid_conversion (f5, f6)
# Taught in s13 (explainer covering f1-f6)
s15 = choice(
    step_id="tile_python_operators_conversion.s15",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.type_conversion",
        "capability": "recognize_invalid_conversion",
        "fact_ids": ["f5", "f6"],
    }],
    anchors=["python.type_conversion#assessment:recognize_invalid_conversion"],
    prompt=(
        "What happens when Python executes `int('3.5')`?"
    ),
    options={
        "opt_a": "Raises a `ValueError` — `int()` requires an integer-format string, not a decimal string",
        "opt_b": "Returns `3` — `int()` truncates the decimal part",
        "opt_c": "Returns `4` — `int()` rounds to the nearest integer",
        "opt_d": "Returns `3.5` — `int()` passes the value through unchanged",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `int()` requires a string in integer format (digits only, with optional sign and whitespace). `'3.5'` contains a decimal point, so Python raises `ValueError`.",
        "opt_b": "`int()` does not truncate decimal strings. To truncate, first convert to float: `int(float('3.5'))` gives `3`. Passing `'3.5'` directly to `int()` raises `ValueError`.",
        "opt_c": "`int()` does not round. It raises `ValueError` for any string that is not in integer format. To round, use `round(float('3.5'))`.",
        "opt_d": "`int()` cannot pass a string through unchanged — it must parse it as an integer. `'3.5'` is not a valid integer string, so it raises `ValueError`.",
    },
    correct_msg="Correct — `int('3.5')` raises `ValueError` because `'3.5'` is not in integer format. To convert a decimal string, use `int(float('3.5'))` instead.",
    incorrect_msg="`int()` requires the string to be in integer format (whole number only). `'3.5'` has a decimal point, so Python raises `ValueError`.",
    hints=[
        "What format does `int()` require its string argument to be in?",
        "If you need to convert `'3.5'` to an integer, what two-step conversion would work?",
    ],
)

# s16 — hands_on: type_conversion practice
# success: The converted values print correctly
# delivery_minutes_str = '32', dm_int = int('32') = 32, dm_float = float('32') = 32.0, dm_back = str(32) = '32'
# stdout: "32\n32.0\n32"
s16 = code_ex(
    step_id="tile_python_operators_conversion.s16",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.type_conversion", "capability": "convert_value_to_target_type", "fact_ids": ["f1", "f2", "f3", "f4"]},
    ],
    anchors=["python.type_conversion#practice"],
    prompt=(
        "A delivery record stores the time as a string. Convert it to different types and print each result.\n\n"
        "`delivery_minutes_str` is assigned below.\n\n"
        "Add three lines that:\n"
        "1. Assign `dm_int` — `delivery_minutes_str` converted to an **integer** using `int()`\n"
        "2. Assign `dm_float` — `delivery_minutes_str` converted to a **float** using `float()`\n"
        "3. Assign `dm_back` — `dm_int` converted back to a **string** using `str()`\n\n"
        "Then print `dm_int`, `dm_float`, and `dm_back` each on its own line.\n\n"
        "Expected output:\n"
        "```\n"
        "32\n"
        "32.0\n"
        "32\n"
        "```"
    ),
    starter_content=(
        "delivery_minutes_str = '32'\n"
        "# Convert to int, float, and back to str, then print each\n"
    ),
    solution_content=(
        "delivery_minutes_str = '32'\n"
        "dm_int = int(delivery_minutes_str)\n"
        "dm_float = float(delivery_minutes_str)\n"
        "dm_back = str(dm_int)\n"
        "print(dm_int)\n"
        "print(dm_float)\n"
        "print(dm_back)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "32\n32.0\n32"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `dm_int`, `dm_float`, `dm_back` each on its own line in that order.",
        },
        {
            "test_id": "t2_dm_int_type",
            "kind": "value_equals",
            "spec": {"expr": "type(dm_int).__name__", "expected": "int"},
            "visible": True,
            "message_on_fail": "`dm_int` should be an integer. Use `int(delivery_minutes_str)` to convert the string.",
        },
        {
            "test_id": "t3_dm_float_type",
            "kind": "value_equals",
            "spec": {"expr": "type(dm_float).__name__", "expected": "float"},
            "visible": True,
            "message_on_fail": "`dm_float` should be a float. Use `float(delivery_minutes_str)` to convert the string.",
        },
    ],
    correct_msg="All three conversions correct — `int('32')` gives `32`, `float('32')` gives `32.0`, and `str(32)` gives `'32'`.",
    incorrect_msg="Use `int()`, `float()`, and `str()` to convert between types. Print `dm_int`, `dm_float`, `dm_back` in that order.",
    hints=[
        "To convert a string to an integer: `dm_int = int(delivery_minutes_str)`. What function converts to float?",
        "To convert an integer back to a string: `dm_back = str(dm_int)`.",
    ],
    concept_id_for_constraints="python.type_conversion",
    remediation_step_id="tile_python_operators_conversion.r04",
)

tile_operators = {
    "tile_id": "tile_python_operators_conversion",
    "interactions": [s02, s03, s05, s06, s07, s10, s11, s12, s14, s15, s16],
}


# ─────────────────────────────────────────────────────────────────────────────
# tile_python_lists_dicts_tuples
# ─────────────────────────────────────────────────────────────────────────────

# s04 — check: modify_and_extend_a_list (f3, f4)
# Taught in s01 (f1, f2, f3, f5) and s03 (f4)
s04_lists = choice(
    step_id="tile_python_lists_dicts_tuples.s04",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.lists",
        "capability": "modify_and_extend_a_list",
        "fact_ids": ["f3", "f4"],
    }],
    anchors=["python.lists#assessment:modify_and_extend_a_list"],
    prompt=(
        "After running:\n\n"
        "```python\n"
        "delivery_times = [32, 45, 21]\n"
        "delivery_times[1] = 50\n"
        "delivery_times.append(18)\n"
        "```\n\n"
        "What is the value of `delivery_times`?"
    ),
    options={
        "opt_a": "`[32, 50, 21, 18]`",
        "opt_b": "`[32, 45, 21, 18]`",
        "opt_c": "`[50, 45, 21, 18]`",
        "opt_d": "`[32, 50, 21]`",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `delivery_times[1] = 50` replaces the item at index 1 (which was `45`) with `50`, and `.append(18)` adds `18` at the end.",
        "opt_b": "The assignment `delivery_times[1] = 50` replaces the item at index 1. Index 1 holds `45`, so after the assignment it becomes `50`, not `45`.",
        "opt_c": "Index 1 is the second item (`45`), not the first (`32`). `delivery_times[1] = 50` replaces `45` with `50`, leaving `32` unchanged.",
        "opt_d": "`.append(18)` adds `18` to the end of the list. The list should have four items after both operations.",
    },
    correct_msg="Right — `delivery_times[1] = 50` replaces the item at index 1 (was `45`, now `50`), and `.append(18)` adds `18` at the end: `[32, 50, 21, 18]`.",
    incorrect_msg="Index 1 is the second item. `delivery_times[1] = 50` replaces `45` with `50`. Then `.append(18)` adds `18` at the end.",
    hints=[
        "List indexes start at 0. What item is at index 1 in `[32, 45, 21]`?",
        "`.append(value)` always adds to the end. How many items does the list have after both operations?",
    ],
    remediation_step_id="tile_python_lists_dicts_tuples.r01",
)

# s05 — hands_on: lists practice (f1, f2, f3, f4, f5)
# success: The list has the right items; indexing and slicing return the expected values; append adds a new item.
# delivery_times = [32, 45, 21, 60, 18]
# first = delivery_times[0] = 32
# last = delivery_times[-1] = 18
# sliced = delivery_times[1:3] = [45, 21]
# delivery_times.append(27) -> [32, 45, 21, 60, 18, 27]
# stdout: "32\n18\n[45, 21]\n[32, 45, 21, 60, 18, 27]"
s05_lists = code_ex(
    step_id="tile_python_lists_dicts_tuples.s05",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.lists", "capability": "create_a_list", "fact_ids": ["f1"]},
        {"concept_id": "python.lists", "capability": "index_and_slice_a_list", "fact_ids": ["f2", "f5"]},
        {"concept_id": "python.lists", "capability": "modify_and_extend_a_list", "fact_ids": ["f3", "f4"]},
    ],
    anchors=[
        "python.lists#practice",
        "python.lists#assessment:create_a_list",
        "python.lists#assessment:index_and_slice_a_list",
        "python.lists#assessment:modify_and_extend_a_list",
    ],
    prompt=(
        "QuickDeliver stores delivery times in a list. `delivery_times` is assigned below.\n\n"
        "Add lines that:\n"
        "1. Assign `first` — the item at index `0`\n"
        "2. Assign `last` — the item at index `-1`\n"
        "3. Assign `sliced` — items from index `1` up to (but not including) index `3`\n"
        "4. Append `27` to `delivery_times`\n\n"
        "Then print `first`, `last`, `sliced`, and `delivery_times` each on its own line.\n\n"
        "Expected output:\n"
        "```\n"
        "32\n"
        "18\n"
        "[45, 21]\n"
        "[32, 45, 21, 60, 18, 27]\n"
        "```"
    ),
    starter_content=(
        "delivery_times = [32, 45, 21, 60, 18]\n"
        "# Assign first, last, sliced; append 27; then print all four\n"
    ),
    solution_content=(
        "delivery_times = [32, 45, 21, 60, 18]\n"
        "first = delivery_times[0]\n"
        "last = delivery_times[-1]\n"
        "sliced = delivery_times[1:3]\n"
        "delivery_times.append(27)\n"
        "print(first)\n"
        "print(last)\n"
        "print(sliced)\n"
        "print(delivery_times)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "32\n18\n[45, 21]\n[32, 45, 21, 60, 18, 27]"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `first`, `last`, `sliced`, `delivery_times` each on its own line in that order.",
        },
        {
            "test_id": "t2_sliced",
            "kind": "value_equals",
            "spec": {"expr": "sliced", "expected": [45, 21]},
            "visible": True,
            "message_on_fail": "`sliced` should be `[45, 21]`. Use `delivery_times[1:3]` — the end index is excluded.",
        },
    ],
    correct_msg="All correct — index `0` gives `32`, index `-1` gives `18`, slice `[1:3]` gives `[45, 21]` (end excluded), and `.append(27)` adds to the end.",
    incorrect_msg="Check each operation: `[0]` for first, `[-1]` for last, `[1:3]` for the slice (end index excluded), and `.append(27)` to extend.",
    hints=[
        "Negative indexes count from the end: `[-1]` is the last item. What is the last item in `[32, 45, 21, 60, 18]`?",
        "In `delivery_times[1:3]`, the start index `1` is included but the end index `3` is excluded. Which items does that give?",
    ],
    concept_id_for_constraints="python.lists",
    remediation_step_id="tile_python_lists_dicts_tuples.r01",
)

# s09 — check: predict_missing_key_error (f3)
# Taught in s06 (f1, f2, f3, f4) and s08 (f5)
s09_dicts = choice(
    step_id="tile_python_lists_dicts_tuples.s09",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.dictionaries",
        "capability": "predict_missing_key_error",
        "fact_ids": ["f3"],
    }],
    anchors=["python.dictionaries#assessment:predict_missing_key_error"],
    prompt=(
        "After running:\n\n"
        "```python\n"
        "order_city = {1042: 'Lagos', 1043: 'Abuja'}\n"
        "print(order_city[1099])\n"
        "```\n\n"
        "What happens?"
    ),
    options={
        "opt_a": "Raises a `KeyError` — key `1099` is not in the dictionary",
        "opt_b": "Prints `None` — Python returns `None` for missing keys",
        "opt_c": "Prints an empty string — Python returns `''` for missing keys",
        "opt_d": "Raises a `ValueError` — the key type does not match",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. Subscripting a dictionary with a key that does not exist raises `KeyError`. Use `.get()` if you want `None` instead of an error.",
        "opt_b": "Subscripting with `[]` raises `KeyError` for a missing key. To get `None` for a missing key, use `order_city.get(1099)` instead.",
        "opt_c": "Python does not return an empty string for missing keys. Subscripting with `[]` raises `KeyError`; use `.get()` to get a default value.",
        "opt_d": "The error is `KeyError`, not `ValueError`. Python raises `KeyError` when the key is not present, regardless of the key's type.",
    },
    correct_msg="Right — `order_city[1099]` raises `KeyError` because `1099` is not a key in the dictionary. Use `.get(1099)` to get `None` instead of an error.",
    incorrect_msg="Subscripting a dictionary with a missing key raises `KeyError`. To avoid the error, use `.get(key)` which returns `None` (or a default) when the key is absent.",
    hints=[
        "What does Python do when you use `d[key]` and `key` is not in `d`?",
        "Which method returns `None` instead of raising an error for a missing key?",
    ],
    remediation_step_id="tile_python_lists_dicts_tuples.r02",
)

# s10 — hands_on: dictionaries practice (f1, f2)
# success: The dictionary has the right key-value pairs; lookup returns the correct city; get() returns None for a missing key.
# order_city = {1042: 'Lagos', 1043: 'Abuja', 1044: 'Kano'}
# order_city[1045] = 'Ibadan'
# city = order_city[1042] = 'Lagos'
# missing = order_city.get(9999) = None
# stdout: "Lagos\nNone"
s10_dicts = code_ex(
    step_id="tile_python_lists_dicts_tuples.s10",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.dictionaries", "capability": "build_and_update_dictionary", "fact_ids": ["f1", "f2"]},
        {"concept_id": "python.dictionaries", "capability": "look_up_value_by_key", "fact_ids": ["f2"]},
    ],
    anchors=[
        "python.dictionaries#practice",
        "python.dictionaries#assessment:build_and_update_dictionary",
        "python.dictionaries#assessment:look_up_value_by_key",
    ],
    prompt=(
        "QuickDeliver maps order IDs to cities. `order_city` is assigned below.\n\n"
        "Add lines that:\n"
        "1. Add a new entry: key `1045`, value `'Ibadan'`\n"
        "2. Assign `city` — the value for key `1042`\n"
        "3. Assign `missing` — the result of looking up key `9999` with `.get()` (returns `None` if absent)\n\n"
        "Then print `city` and `missing` each on its own line.\n\n"
        "Expected output:\n"
        "```\n"
        "Lagos\n"
        "None\n"
        "```"
    ),
    starter_content=(
        "order_city = {1042: 'Lagos', 1043: 'Abuja', 1044: 'Kano'}\n"
        "# Add key 1045 -> 'Ibadan', look up key 1042, get key 9999, then print city and missing\n"
    ),
    solution_content=(
        "order_city = {1042: 'Lagos', 1043: 'Abuja', 1044: 'Kano'}\n"
        "order_city[1045] = 'Ibadan'\n"
        "city = order_city[1042]\n"
        "missing = order_city.get(9999)\n"
        "print(city)\n"
        "print(missing)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "Lagos\nNone"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `city` then `missing`, each on its own line.",
        },
        {
            "test_id": "t2_city",
            "kind": "value_equals",
            "spec": {"expr": "city", "expected": "Lagos"},
            "visible": True,
            "message_on_fail": "`city` should be `'Lagos'`. Use `order_city[1042]` to look up the value for key `1042`.",
        },
        {
            "test_id": "t3_missing",
            "kind": "value_equals",
            "spec": {"expr": "missing", "expected": None},
            "visible": True,
            "message_on_fail": "`missing` should be `None`. Use `order_city.get(9999)` — `.get()` returns `None` when the key is absent.",
        },
    ],
    correct_msg="All correct — `order_city[1045] = 'Ibadan'` adds the entry, `order_city[1042]` returns `'Lagos'`, and `.get(9999)` returns `None` for a missing key.",
    incorrect_msg="Use `d[key] = value` to add/update, `d[key]` to look up, and `d.get(key)` to look up safely (returns `None` if absent).",
    hints=[
        "To add a new key-value pair: `order_city[1045] = 'Ibadan'`. To look up: `city = order_city[1042]`.",
        "`.get(key)` returns `None` when the key is not in the dictionary — no `KeyError`.",
    ],
    concept_id_for_constraints="python.dictionaries",
    remediation_step_id="tile_python_lists_dicts_tuples.r02",
)

# s12 — check: recognize_single_item_tuple_needs_comma (m1)
# Taught in s11 (f1, f2, f3, m1)
s12_tuples = choice(
    step_id="tile_python_lists_dicts_tuples.s12",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.tuples",
        "capability": "recognize_single_item_tuple_needs_comma",
        "fact_ids": ["m1"],
    }],
    anchors=["python.tuples#assessment:recognize_single_item_tuple_needs_comma"],
    prompt=(
        "Which of the following creates a **tuple** containing the single value `'Lagos'`?"
    ),
    options={
        "opt_a": "`singleton = 'Lagos',`",
        "opt_b": "`singleton = ('Lagos')`",
        "opt_c": "`singleton = ['Lagos']`",
        "opt_d": "`singleton = {'Lagos'}`",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. A trailing comma after the value creates a one-item tuple: `'Lagos',` is a tuple. The parentheses are optional.",
        "opt_b": "`('Lagos')` is just `'Lagos'` in parentheses — the parentheses are grouping, not a tuple. Without a trailing comma, Python sees a plain string.",
        "opt_c": "`['Lagos']` creates a **list** with one item, not a tuple. Lists use square brackets; tuples use commas (with optional parentheses).",
        "opt_d": "`{'Lagos'}` creates a **set** with one item, not a tuple. Sets use curly braces; tuples use commas.",
    },
    correct_msg="Right — a one-item tuple requires a trailing comma: `'Lagos',` or `('Lagos',)`. Without the comma, `('Lagos')` is just a string in parentheses.",
    incorrect_msg="A one-item tuple needs a trailing comma: `singleton = 'Lagos',`. Without the comma, parentheses alone do not create a tuple.",
    hints=[
        "What makes a tuple a tuple — the parentheses, or the commas?",
        "Try `type(('Lagos'))` versus `type(('Lagos',))` — what does each return?",
    ],
    remediation_step_id="tile_python_lists_dicts_tuples.r03",
)

# s13 — hands_on: tuples practice (f1, f2, f3)
# success: The tuple has two values; unpacking gives each value its own name, and printing both shows the correct numbers.
# order_stats = (32, 45)
# min_time, max_time = order_stats
# print(min_time) -> 32, print(max_time) -> 45
# stdout: "32\n45"
s13_tuples = code_ex(
    step_id="tile_python_lists_dicts_tuples.s13",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.tuples", "capability": "create_a_tuple", "fact_ids": ["f1"]},
        {"concept_id": "python.tuples", "capability": "recognize_tuple_immutability", "fact_ids": ["f2"]},
        {"concept_id": "python.tuples", "capability": "unpack_tuple_into_variables", "fact_ids": ["f3"]},
    ],
    anchors=[
        "python.tuples#practice",
        "python.tuples#assessment:create_a_tuple",
        "python.tuples#assessment:recognize_tuple_immutability",
        "python.tuples#assessment:unpack_tuple_into_variables",
    ],
    prompt=(
        "QuickDeliver records the minimum and maximum delivery times as a fixed pair.\n\n"
        "`order_stats` is assigned below as a tuple of two values.\n\n"
        "Add lines that:\n"
        "1. Unpack `order_stats` into two variables: `min_time` and `max_time`\n"
        "2. Print `min_time` and `max_time` each on its own line\n\n"
        "Expected output:\n"
        "```\n"
        "32\n"
        "45\n"
        "```"
    ),
    starter_content=(
        "order_stats = (32, 45)\n"
        "# Unpack order_stats into min_time and max_time, then print each\n"
    ),
    solution_content=(
        "order_stats = (32, 45)\n"
        "min_time, max_time = order_stats\n"
        "print(min_time)\n"
        "print(max_time)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "32\n45"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `min_time` then `max_time`, each on its own line.",
        },
        {
            "test_id": "t2_min_time",
            "kind": "value_equals",
            "spec": {"expr": "min_time", "expected": 32},
            "visible": True,
            "message_on_fail": "`min_time` should be `32`. Unpack with `min_time, max_time = order_stats`.",
        },
        {
            "test_id": "t3_max_time",
            "kind": "value_equals",
            "spec": {"expr": "max_time", "expected": 45},
            "visible": True,
            "message_on_fail": "`max_time` should be `45`. Unpack with `min_time, max_time = order_stats`.",
        },
    ],
    correct_msg="Correct — `min_time, max_time = order_stats` unpacks the tuple into two names, giving `min_time=32` and `max_time=45`.",
    incorrect_msg="Use tuple unpacking: `min_time, max_time = order_stats`. The number of variables on the left must match the number of items in the tuple.",
    hints=[
        "Tuple unpacking looks like: `a, b = some_tuple`. How many items are in `order_stats`?",
        "After unpacking, `min_time` holds the first item and `max_time` holds the second.",
    ],
    concept_id_for_constraints="python.tuples",
    remediation_step_id="tile_python_lists_dicts_tuples.r03",
)

tile_lists_dicts_tuples = {
    "tile_id": "tile_python_lists_dicts_tuples",
    "interactions": [s04_lists, s05_lists, s09_dicts, s10_dicts, s12_tuples, s13_tuples],
}


# ─────────────────────────────────────────────────────────────────────────────
# tile_python_sets_strings
# ─────────────────────────────────────────────────────────────────────────────

# s04 — check: create_set_of_unique_values (f1, f2, f3)
# Taught in s01 (f1, f2, f3, f4) and s03 (f5)
# NOTE: s04 tests f1, f2, f3 which are taught in s01 (text explainer) — OK
s04_sets = choice(
    step_id="tile_python_sets_strings.s04",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.sets",
        "capability": "create_set_of_unique_values",
        "fact_ids": ["f1", "f2", "f3"],
    }],
    anchors=["python.sets#assessment:create_set_of_unique_values"],
    prompt=(
        "Which expression creates a set of unique cities from the list `['Lagos', 'Abuja', 'Lagos', 'Kano']`?"
    ),
    options={
        "opt_a": "`set(['Lagos', 'Abuja', 'Lagos', 'Kano'])`",
        "opt_b": "`{}`",
        "opt_c": "`['Lagos', 'Abuja', 'Kano']`",
        "opt_d": "`{'Lagos': True, 'Abuja': True, 'Kano': True}`",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `set(iterable)` builds a set from any iterable, removing duplicates. `set(['Lagos', 'Abuja', 'Lagos', 'Kano'])` gives `{'Lagos', 'Abuja', 'Kano'}`.",
        "opt_b": "`{}` creates an **empty dictionary**, not an empty set. To create an empty set, use `set()`. To create a non-empty set, use `set(iterable)` or `{val1, val2, ...}`.",
        "opt_c": "`['Lagos', 'Abuja', 'Kano']` is a list, not a set. Lists preserve order and allow duplicates; sets do not.",
        "opt_d": "That creates a dictionary with string keys and `True` values — not a set. Use `set(iterable)` or `{val1, val2, ...}` to create a set.",
    },
    correct_msg="`set(iterable)` builds a set of unique values from any iterable. Note: `{}` alone creates an empty dictionary — use `set()` for an empty set.",
    incorrect_msg="Use `set(iterable)` to build a set from a list, removing duplicates. `{}` creates an empty dictionary, not a set.",
    hints=[
        "Which function builds a set from an existing collection, removing duplicates?",
        "What does `{}` create — a set or a dictionary? How do you create an empty set?",
    ],
    remediation_step_id="tile_python_sets_strings.r01",
)

# s05 — check: combine_sets_with_union_and_intersection (f5)
# Taught in s03 (f5)
s05_sets = choice(
    step_id="tile_python_sets_strings.s05",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.sets",
        "capability": "combine_sets_with_union_and_intersection",
        "fact_ids": ["f5"],
    }],
    anchors=["python.sets#assessment:combine_sets_with_union_and_intersection"],
    prompt=(
        "Given:\n\n"
        "```python\n"
        "morning = {'Lagos', 'Abuja', 'Kano'}\n"
        "evening = {'Kano', 'Ibadan', 'Lagos'}\n"
        "```\n\n"
        "What does `morning & evening` return?"
    ),
    options={
        "opt_a": "A set containing `'Lagos'` and `'Kano'` — cities that appear in both sets",
        "opt_b": "A set containing all four cities — all cities from both sets",
        "opt_c": "A set containing `'Abuja'` and `'Ibadan'` — cities that appear in only one set",
        "opt_d": "A set containing `'Lagos'`, `'Kano'`, and `'Ibadan'` — cities from the evening set",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. `&` is the intersection operator — it returns only the elements that appear in **both** sets. `'Lagos'` and `'Kano'` are in both `morning` and `evening`.",
        "opt_b": "That is the **union** (`|`), which returns all elements from both sets. The intersection (`&`) returns only elements present in both.",
        "opt_c": "That is the **symmetric difference** (`^`), which returns elements in one set but not the other. The intersection (`&`) returns elements in both.",
        "opt_d": "That is the `evening` set itself. The intersection (`&`) returns only elements that appear in both sets.",
    },
    correct_msg="Right — `&` is intersection: elements in both sets. `morning & evening` gives `{'Lagos', 'Kano'}`. Use `|` for union (all elements from both).",
    incorrect_msg="`&` is intersection — only elements present in **both** sets. `|` is union — all elements from either set.",
    hints=[
        "In set mathematics, intersection means 'in both'. Which cities appear in both `morning` and `evening`?",
        "Remember: `|` is union (all elements), `&` is intersection (shared elements only).",
    ],
)

# s06 — hands_on: sets practice (f4)
# success: The set holds each city once; the membership test prints True for a city in the list and False for one that is not.
# cities_list = ['Lagos', 'Abuja', 'Kano', 'Lagos', 'Ibadan', 'Abuja']
# unique_cities = set(cities_list)
# print('Lagos' in unique_cities) -> True
# print('Enugu' in unique_cities) -> False
# stdout: "True\nFalse"
s06_sets = code_ex(
    step_id="tile_python_sets_strings.s06",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.sets", "capability": "create_set_of_unique_values", "fact_ids": ["f1", "f2", "f3"]},
        {"concept_id": "python.sets", "capability": "test_set_membership", "fact_ids": ["f4"]},
    ],
    anchors=[
        "python.sets#practice",
        "python.sets#assessment:test_set_membership",
    ],
    prompt=(
        "QuickDeliver wants to know which unique cities appear in a batch of orders.\n\n"
        "`cities_list` is assigned below (it contains duplicates).\n\n"
        "Add lines that:\n"
        "1. Assign `unique_cities` — a set built from `cities_list` using `set()`\n"
        "2. Print whether `'Lagos'` is in `unique_cities`\n"
        "3. Print whether `'Enugu'` is in `unique_cities`\n\n"
        "Expected output:\n"
        "```\n"
        "True\n"
        "False\n"
        "```"
    ),
    starter_content=(
        "cities_list = ['Lagos', 'Abuja', 'Kano', 'Lagos', 'Ibadan', 'Abuja']\n"
        "# Build unique_cities set, then print membership for 'Lagos' and 'Enugu'\n"
    ),
    solution_content=(
        "cities_list = ['Lagos', 'Abuja', 'Kano', 'Lagos', 'Ibadan', 'Abuja']\n"
        "unique_cities = set(cities_list)\n"
        "print('Lagos' in unique_cities)\n"
        "print('Enugu' in unique_cities)\n"
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "True\nFalse"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `'Lagos' in unique_cities` then `'Enugu' in unique_cities`, each on its own line.",
        },
        {
            "test_id": "t2_unique_cities_type",
            "kind": "value_equals",
            "spec": {"expr": "type(unique_cities).__name__", "expected": "set"},
            "visible": True,
            "message_on_fail": "`unique_cities` should be a set. Use `set(cities_list)` to build it.",
        },
    ],
    correct_msg="Correct — `set(cities_list)` removes duplicates, and `'Lagos' in unique_cities` is `True` while `'Enugu' in unique_cities` is `False`.",
    incorrect_msg="Use `set(cities_list)` to build the set, then `print('Lagos' in unique_cities)` and `print('Enugu' in unique_cities)`.",
    hints=[
        "To build a set from a list: `unique_cities = set(cities_list)`. Sets automatically remove duplicates.",
        "The `in` operator tests membership: `'Lagos' in unique_cities` returns `True` if `'Lagos'` is in the set.",
    ],
    concept_id_for_constraints="python.sets",
    remediation_step_id="tile_python_sets_strings.r01",
)

# s08 — check: embed_quote_without_escaping (f1)
# Taught in s07 (f1, f2, f3)
s08_strings = choice(
    step_id="tile_python_sets_strings.s08",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.string_basics_formatting",
        "capability": "embed_quote_without_escaping",
        "fact_ids": ["f1"],
    }],
    anchors=["python.string_basics_formatting#assessment:embed_quote_without_escaping"],
    prompt=(
        "Which string literal correctly stores the text: `The driver's route`?"
    ),
    options={
        "opt_a": '`"The driver\'s route"`',
        "opt_b": "`'The driver's route'`",
        "opt_c": '`"The driver"s route"`',
        "opt_d": "`The driver's route`",
    },
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": "Correct. Enclosing the string in double quotes lets you include a single quote (`'`) inside without escaping it.",
        "opt_b": "The single quote in `driver's` ends the string early, causing a `SyntaxError`. Use double quotes to enclose a string that contains a single quote.",
        "opt_c": "The double quote after `driver` ends the string, and `s route\"` is invalid syntax. The string must be enclosed consistently.",
        "opt_d": "A string literal must be enclosed in quotes. Without quotes, Python treats `The` as a name and raises a `NameError`.",
    },
    correct_msg="Right — enclosing in double quotes lets you include a single quote inside: `\"The driver's route\"`. No escaping needed.",
    incorrect_msg="To include a single quote in a string, enclose the whole string in double quotes: `\"The driver's route\"`. The outer quote type must differ from the embedded one.",
    hints=[
        "If the string contains a `'`, which type of outer quotes avoids a conflict?",
        "Python lets you mix quote types: use `\"...\"` when the string contains `'`, and `'...'` when it contains `\"`.",
    ],
    remediation_step_id="tile_python_sets_strings.r02",
)

# s09 — hands_on: string formatting practice (f2, f3)
# success: The printed sentence contains the computed total rounded to two decimal places.
# delivery_a = 32, delivery_b = 45, total = 77, avg = 38.5
# print(f"Average delivery time: {avg:.2f} minutes") -> "Average delivery time: 38.50 minutes"
s09_strings = code_ex(
    step_id="tile_python_sets_strings.s09",
    difficulty="core",
    standalone=False,
    measures=[
        {"concept_id": "python.string_basics_formatting", "capability": "write_formatted_fstring", "fact_ids": ["f2", "f3"]},
    ],
    anchors=[
        "python.string_basics_formatting#practice",
        "python.string_basics_formatting#assessment:write_formatted_fstring",
    ],
    prompt=(
        "QuickDeliver wants a summary sentence showing the average delivery time.\n\n"
        "`delivery_a` and `delivery_b` are assigned below.\n\n"
        "Add lines that:\n"
        "1. Assign `total` — the sum of `delivery_a` and `delivery_b`\n"
        "2. Assign `avg` — `total` divided by `2`\n"
        "3. Print the sentence using an f-string with `avg` rounded to **two decimal places**\n\n"
        "Expected output:\n"
        "```\n"
        "Average delivery time: 38.50 minutes\n"
        "```"
    ),
    starter_content=(
        "delivery_a = 32\n"
        "delivery_b = 45\n"
        "# Compute total and avg, then print the formatted sentence\n"
    ),
    solution_content=(
        "delivery_a = 32\n"
        "delivery_b = 45\n"
        "total = delivery_a + delivery_b\n"
        "avg = total / 2\n"
        'print(f"Average delivery time: {avg:.2f} minutes")\n'
    ),
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "Average delivery time: 38.50 minutes"},
            "visible": True,
            "message_on_fail": "Output does not match. Use an f-string with `{avg:.2f}` to round to two decimal places.",
        },
        {
            "test_id": "t2_avg",
            "kind": "value_equals",
            "spec": {"expr": "avg", "expected": 38.5},
            "visible": True,
            "message_on_fail": "`avg` should be `38.5`. Compute `total = delivery_a + delivery_b`, then `avg = total / 2`.",
        },
    ],
    correct_msg="Correct — `{avg:.2f}` in the f-string formats `38.5` as `38.50`, giving the sentence `Average delivery time: 38.50 minutes`.",
    incorrect_msg="Use an f-string: `f\"Average delivery time: {avg:.2f} minutes\"`. The `:.2f` format specifier rounds to two decimal places.",
    hints=[
        "An f-string starts with `f` before the opening quote: `f\"...\"`.",
        "To embed a value rounded to two decimal places, write `{avg:.2f}` inside the f-string.",
    ],
    concept_id_for_constraints="python.string_basics_formatting",
    remediation_step_id="tile_python_sets_strings.r02",
)

tile_sets_strings = {
    "tile_id": "tile_python_sets_strings",
    "interactions": [s04_sets, s05_sets, s06_sets, s08_strings, s09_strings],
}


# ─────────────────────────────────────────────────────────────────────────────
# Assemble and write
# ─────────────────────────────────────────────────────────────────────────────

artifact = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_008_da_python_core",
    "tiles": [tile_operators, tile_lists_dicts_tuples, tile_sets_strings],
}

OUT.write_text(json.dumps(artifact, indent=2, ensure_ascii=False))
print(f"Written: {OUT}")

# Count interactions
total = sum(len(t["interactions"]) for t in artifact["tiles"])
for t in artifact["tiles"]:
    print(f"  {t['tile_id']}: {len(t['interactions'])} interactions")
print(f"  Total: {total}")
