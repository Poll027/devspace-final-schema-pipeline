"""Patch interactions.part.c0_canary.json to fix s04 errors:
1. Remove op_mul from solution (use name-only reassignment, no *)
2. Add choose_valid_variable_name to measures and anchors
"""
import json, copy

PATH = "batches/final_batch_008_da_python_core/interactions.part.c0_canary.json"

with open(PATH) as f:
    data = json.load(f)

# Find tile_python_variables_types / s04
tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_python_variables_types")
entry = next(e for e in tile["interactions"] if e["step_id"] == "tile_python_variables_types.s04")
ix = entry["interaction"]

# ── 1. Fix the prompt (no multiplication required) ──────────────────────────
ix["public"]["prompt"] = (
    "The QuickDeliver team tracks how many orders each driver handles per day.\n\n"
    "Three variables are already assigned below. Add one line that **reassigns** "
    "`total_orders` to the value stored in `orders_per_driver`.\n\n"
    "After your line runs:\n"
    "- `orders_per_driver` must still hold `23`\n"
    "- `days_worked` must still hold `5`\n"
    "- `total_orders` must hold `23` (the same value as `orders_per_driver`)\n\n"
    "Use only `name = value` assignment and the name of an already-assigned variable "
    "on the right-hand side. Do not use `print()`, `type()`, or any arithmetic operator."
)

# ── 2. Fix the solution (no * operator) ─────────────────────────────────────
ix["grading"]["solution_files"][0]["content"] = (
    "orders_per_driver = 23\n"
    "days_worked = 5\n"
    "total_orders = 0\n"
    "total_orders = orders_per_driver\n"
)

# ── 3. Fix the test expected value (23, not 115) ────────────────────────────
for test in ix["grading"]["tests"]:
    if test.get("kind") == "value_equals" and test["spec"].get("expr") == "total_orders":
        test["spec"]["expected"] = 23

# ── 4. Add choose_valid_variable_name to measures ───────────────────────────
already = {m["capability"] for m in ix["measures"]}
if "choose_valid_variable_name" not in already:
    ix["measures"].append({
        "concept_id": "python.variables_assignment",
        "capability": "choose_valid_variable_name",
        "fact_ids": ["f4"]
    })

# ── 5. Add assessment anchor for choose_valid_variable_name ─────────────────
anchor_id = "python.variables_assignment#assessment:choose_valid_variable_name"
if anchor_id not in ix.get("anchors", []):
    ix.setdefault("anchors", []).append(anchor_id)

with open(PATH, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Patch applied.")
