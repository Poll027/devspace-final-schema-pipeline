import json, copy

with open("batches/final_batch_008_da_python_core/screens.part.c1.json", "r") as f:
    data = json.load(f)

# ── Helper: find tile by id ──────────────────────────────────────────────────
def get_tile(tile_id):
    for t in data["tiles"]:
        if t["tile_id"] == tile_id:
            return t
    raise KeyError(tile_id)

def get_step(tile, step_id):
    for s in tile["steps"]:
        if s["step_id"] == step_id:
            return s
    raise KeyError(step_id)

# ════════════════════════════════════════════════════════════════════════════
# BLOCKING FIX: Add A.f4 (in operator) prose block to tile_python_sets_strings.s01
# ════════════════════════════════════════════════════════════════════════════
sets_tile = get_tile("tile_python_sets_strings")
s01 = get_step(sets_tile, "tile_python_sets_strings.s01")

# New prose block teaching the `in` operator (A.f4)
new_block = {
    "type": "prose",
    "block_id": "tile_python_sets_strings.s01.b04",
    "role": "mechanism",
    "text": "Test whether a value is in the set with the `in` operator: `'Lagos' in cities` returns `True` if `'Lagos'` is in the set, and `False` otherwise. This membership test is the primary reason to use a set rather than a list when you only need to check presence. \u27e6A.f4\u27e7",
    "lineage": {
        "concept_ids": ["python.sets"],
        "fact_ids": ["python.sets#f4"],
        "teaching_block_ids": ["python.sets#tb4"],
        "anchors": []
    }
}

# Append to s01 blocks (after the before_after visual)
s01["blocks"].append(new_block)

# Ensure f4 and tb4 are in the step-level lineage (they already are, but be safe)
if "python.sets#f4" not in s01["lineage"]["fact_ids"]:
    s01["lineage"]["fact_ids"].append("python.sets#f4")
if "python.sets#tb4" not in s01["lineage"]["teaching_block_ids"]:
    s01["lineage"]["teaching_block_ids"].append("python.sets#tb4")

# ════════════════════════════════════════════════════════════════════════════
# ADVISORY FIX 1: Fix annotation in tile_python_operators_conversion.s01
# "addition runs before multiplication" → "parentheses force addition before multiplication"
# ════════════════════════════════════════════════════════════════════════════
ops_tile = get_tile("tile_python_operators_conversion")
ops_s01 = get_step(ops_tile, "tile_python_operators_conversion.s01")

for block in ops_s01["blocks"]:
    if block.get("type") == "side_by_side":
        right = block.get("right", {})
        for ann in right.get("annotations", []):
            if "addition runs before multiplication" in ann.get("text", ""):
                ann["text"] = ann["text"].replace(
                    "addition runs before multiplication",
                    "parentheses force addition before multiplication"
                )

# ════════════════════════════════════════════════════════════════════════════
# ADVISORY FIX 2: Add ⟦C.f3⟧ tag to before_after block in tile_python_lists_dicts_tuples.s11
# ════════════════════════════════════════════════════════════════════════════
ldt_tile = get_tile("tile_python_lists_dicts_tuples")
s11 = get_step(ldt_tile, "tile_python_lists_dicts_tuples.s11")

for block in s11["blocks"]:
    if block.get("type") == "before_after":
        cs = block.get("change_summary", "")
        if "C.f3" not in cs and "unpacking" in cs.lower():
            block["change_summary"] = cs.rstrip() + " \u27e6C.f3\u27e7"

# ════════════════════════════════════════════════════════════════════════════
# Write output
# ════════════════════════════════════════════════════════════════════════════
with open("batches/final_batch_008_da_python_core/screens.part.c1.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
