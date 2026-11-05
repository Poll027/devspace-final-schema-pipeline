#!/usr/bin/env python3
"""
Patch script for screens.part.c1.json — REPAIR ROUND advisory fixes.

Changes:
1. tile_python_sets_strings/s01 b04: Replace standalone ⟦A.f4⟧ with ⟦A.f4 A:tb4⟧
2. tile_python_operators_conversion/r06 b02 right: Remove int(float('3.5')) workaround
   (beyond source facts); replace right panel with float('3.5') showing it succeeds
3. tile_python_operators_conversion/s08 b01: Remove the three-variable priority example
   that introduces is_first_week; keep only the rule statement (is_late/is_far only)
4. tile_python_lists_dicts_tuples/s11 b02: Add ⟦C.f3⟧ citation to body text
   (C.f3 tuple unpacking demonstrated in visual but missing from body prose)
"""

import json

with open("batches/final_batch_008_da_python_core/screens.part.c1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def find_tile(tile_id):
    for tile in data["tiles"]:
        if tile["tile_id"] == tile_id:
            return tile
    raise KeyError(f"Tile not found: {tile_id}")

def find_step(tile, step_id):
    for step in tile.get("steps", []) + tile.get("remediation_steps", []):
        if step["step_id"] == step_id:
            return step
    raise KeyError(f"Step not found: {step_id}")

def find_block(step, block_id):
    for block in step.get("blocks", []):
        if block.get("block_id") == block_id:
            return block
    raise KeyError(f"Block not found: {block_id}")

# ─────────────────────────────────────────────────────────────────────────────
# Fix 1: tile_python_sets_strings/s01 b04
# Replace standalone ⟦A.f4⟧ with ⟦A.f4 A:tb4⟧
# ─────────────────────────────────────────────────────────────────────────────
tile_ss = find_tile("tile_python_sets_strings")
step_s01 = find_step(tile_ss, "tile_python_sets_strings.s01")
block_b04 = find_block(step_s01, "tile_python_sets_strings.s01.b04")

old_text = block_b04["text"]
new_text = old_text.replace("⟦A.f4⟧", "⟦A.f4 A:tb4⟧")
assert new_text != old_text, "Fix 1: no change made"
block_b04["text"] = new_text
print(f"Fix 1 applied: standalone ⟦A.f4⟧ → ⟦A.f4 A:tb4⟧")

# ─────────────────────────────────────────────────────────────────────────────
# Fix 2: tile_python_operators_conversion/r06 b02 right panel
# Remove int(float('3.5')) workaround — replace right panel with float('3.5')
# showing that a decimal string IS valid for float(), staying within source facts.
# ─────────────────────────────────────────────────────────────────────────────
tile_oc = find_tile("tile_python_operators_conversion")
step_r06 = find_step(tile_oc, "tile_python_operators_conversion.r06")
block_r06_b02 = find_block(step_r06, "tile_python_operators_conversion.r06.b02")

block_r06_b02["right"]["code"] = "float('3.5')"
block_r06_b02["right"]["annotations"] = [
    {
        "start_line": 1,
        "end_line": 1,
        "text": "Result: 3.5 — decimal strings are valid for float()"
    }
]
block_r06_b02["right_label"] = "float('3.5') — succeeds"
block_r06_b02["takeaway"] = (
    "int() cannot parse a decimal string — it raises ValueError. "
    "float() accepts decimal strings; use float() when the string contains a decimal point."
)
print("Fix 2 applied: r06 right panel updated to float('3.5')")

# ─────────────────────────────────────────────────────────────────────────────
# Fix 3: tile_python_operators_conversion/s08 b01
# Remove the three-variable priority example that introduces is_first_week.
# Keep only the rule statement; the visual (b03) and r03 already show examples.
# ─────────────────────────────────────────────────────────────────────────────
step_s08 = find_step(tile_oc, "tile_python_operators_conversion.s08")
block_s08_b01 = find_block(step_s08, "tile_python_operators_conversion.s08.b01")

old_b01 = block_s08_b01["text"]
# Remove the sentence that introduces is_first_week as a third variable
new_b01 = old_b01.replace(
    " When there are no parentheses, and binds more tightly than or, so is_late or is_far and is_first_week groups as is_late or (is_far and is_first_week).",
    " When there are no parentheses, and binds more tightly than or."
)
assert new_b01 != old_b01, "Fix 3: no change made"
block_s08_b01["text"] = new_b01
print("Fix 3 applied: is_first_week example removed from s08.b01")

# ─────────────────────────────────────────────────────────────────────────────
# Fix 4: tile_python_lists_dicts_tuples/s11 b02
# Add ⟦C.f3⟧ citation to body text.
# b02 is the last prose block before the before_after visual that demonstrates
# unpacking (C.f3). Appending the tag to b02 cites the fact without adding a claim.
# ─────────────────────────────────────────────────────────────────────────────
tile_ldt = find_tile("tile_python_lists_dicts_tuples")
step_s11 = find_step(tile_ldt, "tile_python_lists_dicts_tuples.s11")
block_s11_b02 = find_block(step_s11, "tile_python_lists_dicts_tuples.s11.b02")

old_b02_ldt = block_s11_b02["text"]
# Append ⟦C.f3⟧ tag — the lede already states "unpacking hands each piece back to its own name"
# so this is a citation of that already-stated concept, not a new claim.
new_b02_ldt = old_b02_ldt.rstrip() + " ⟦C.f3⟧"
block_s11_b02["text"] = new_b02_ldt
# Update lineage to include f3 and tb3
if "python.tuples#f3" not in block_s11_b02["lineage"]["fact_ids"]:
    block_s11_b02["lineage"]["fact_ids"].append("python.tuples#f3")
if "python.tuples#tb3" not in block_s11_b02["lineage"]["teaching_block_ids"]:
    block_s11_b02["lineage"]["teaching_block_ids"].append("python.tuples#tb3")
print("Fix 4 applied: ⟦C.f3⟧ appended to s11.b02 body text")

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────
with open("batches/final_batch_008_da_python_core/screens.part.c1.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done — screens.part.c1.json written.")
