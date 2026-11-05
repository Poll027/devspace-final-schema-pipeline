#!/usr/bin/env python3
"""
Repair patch for interactions.part.c0_canary.json
Addresses two BLOCKING findings and one ADVISORY:

BLOCKING s04/t3_total_orders:
  Add a hidden source_contains test that checks total_orders = orders_per_driver.

BLOCKING s04/practice_anchor + ADVISORY s04/prompt:
  Change exercise to require total_orders = orders_per_driver * days_worked
  (expected value 115). Remove "Do not use any arithmetic operator" instruction.
  Update prompt, solution, value_equals test, and success feedback accordingly.
"""
import json, re, copy

ARTIFACT = "batches/final_batch_008_da_python_core/interactions.part.c0_canary.json"

with open(ARTIFACT) as f:
    data = json.load(f)

# Locate s04 interaction
s04_interaction = None
for tile in data["tiles"]:
    for step in tile["interactions"]:
        if step["step_id"] == "tile_python_variables_types.s04":
            s04_interaction = step["interaction"]
            break

assert s04_interaction is not None, "s04 interaction not found"

# ── BLOCKING s04/practice_anchor + ADVISORY s04/prompt ──────────────────────
# Change exercise: total_orders = orders_per_driver * days_worked → 115
# orders_per_driver=23, days_worked=5 → 23*5=115

# 1. Update prompt: change description and remove "Do not use any arithmetic operator"
old_prompt = s04_interaction["public"]["prompt"]
new_prompt = (
    "The QuickDeliver team tracks how many orders each driver handles per day.\n\n"
    "Three variables are already assigned below. Add one line that **reassigns** "
    "`total_orders` to the product of `orders_per_driver` and `days_worked` "
    "(i.e. `orders_per_driver * days_worked`).\n\n"
    "After your line runs:\n"
    "- `orders_per_driver` must still hold `23`\n"
    "- `days_worked` must still hold `5`\n"
    "- `total_orders` must hold `115` (the product of the two variables)\n\n"
    "Use only `name = value` assignment and the `*` operator on assigned names. "
    "Do not use `print()`, `type()`, or any other arithmetic operator."
)
s04_interaction["public"]["prompt"] = new_prompt

# 2. Update solution file
for sf in s04_interaction["grading"]["solution_files"]:
    if sf["path"] == "solution.py":
        sf["content"] = (
            "orders_per_driver = 23\n"
            "days_worked = 5\n"
            "total_orders = 0\n"
            "total_orders = orders_per_driver * days_worked\n"
        )

# 3. Update t3_total_orders value_equals test: expected 23 → 115
for test in s04_interaction["grading"]["tests"]:
    if test["test_id"] == "t3_total_orders":
        test["spec"]["expected"] = 115
        test["message_on_fail"] = (
            "`total_orders` should hold `115` (the product of `orders_per_driver` "
            "and `days_worked`). Check that you wrote `total_orders = orders_per_driver * days_worked`."
        )

# ── BLOCKING s04/t3_total_orders: add source_contains hidden test ────────────
source_contains_test = {
    "test_id": "t4_source_uses_variable",
    "kind": "source_contains",
    "spec": {
        "pattern": "total_orders\\s*=\\s*orders_per_driver"
    },
    "visible": False,
    "message_on_fail": (
        "You must assign `total_orders` using the variable name `orders_per_driver`, "
        "not a literal number."
    )
}
s04_interaction["grading"]["tests"].append(source_contains_test)

# 4. Update feedback messages to reflect new expected value
s04_interaction["feedback"]["correct"]["message"] = (
    "Well done \u2014 `total_orders` now holds `115`, the product of `orders_per_driver` "
    "and `days_worked`. Reassigning a name with an expression reads the current values "
    "of the other names and computes a new result."
)
s04_interaction["feedback"]["incorrect"]["message"] = (
    "Check that you added exactly one line: `total_orders = orders_per_driver * days_worked`. "
    "This rebinds `total_orders` to the product of the two variables without touching them."
)
s04_interaction["feedback"]["hints"][0] = (
    "Assignment always goes `name = expression`. What name are you reassigning, "
    "and what expression multiplies `orders_per_driver` by `days_worked`?"
)
s04_interaction["feedback"]["hints"][1] = (
    "You only need one new line. Use the `*` operator between the two variable names."
)

# Write patched artifact
with open(ARTIFACT, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
print(f"s04 tests: {[t['test_id'] for t in s04_interaction['grading']['tests']]}")
print(f"t3 expected: {next(t['spec']['expected'] for t in s04_interaction['grading']['tests'] if t['test_id']=='t3_total_orders')}")
print(f"solution: {s04_interaction['grading']['solution_files'][0]['content']!r}")
