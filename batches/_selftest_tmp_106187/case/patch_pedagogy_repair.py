#!/usr/bin/env python3
"""
Patch script for pedagogy repair round:
1. Fix tile_python_operators_conversion/s10 opt_b feedback in interactions.part.c1.json
2. Fix tile_python_pep8_style/s03 instruction #3 in interactions.part.c3.json
"""
import json, copy

# ── Fix 1: interactions.part.c1.json ─────────────────────────────────────────
c1_path = "batches/final_batch_008_da_python_core/interactions.part.c1.json"
with open(c1_path) as f:
    c1 = json.load(f)

fixed_c1 = False
for tile in c1["tiles"]:
    if tile["tile_id"] != "tile_python_operators_conversion":
        continue
    for item in tile["interactions"]:
        if item["step_id"] != "tile_python_operators_conversion.s10":
            continue
        fb = item["interaction"]["grading"]["option_feedback"]
        old_b = fb["opt_b"]["message"]
        new_b = (
            "Even if `not` were evaluated before `==`, the result would be "
            "`(not True) == False` \u2192 `False == False` \u2192 `True`, not `False`. "
            "In fact, `not` has lower priority than `==`, so Python reads "
            "`not (is_late == False)` \u2192 `not False` \u2192 `True`."
        )
        fb["opt_b"]["message"] = new_b
        print(f"[c1] s10 opt_b feedback updated.")
        print(f"  OLD: {old_b}")
        print(f"  NEW: {new_b}")
        fixed_c1 = True

if not fixed_c1:
    print("WARNING: s10 opt_b not found in c1!")

with open(c1_path, "w") as f:
    json.dump(c1, f, indent=2, ensure_ascii=False)
print(f"[c1] Written: {c1_path}")

# ── Fix 2: interactions.part.c3.json ─────────────────────────────────────────
c3_path = "batches/final_batch_008_da_python_core/interactions.part.c3.json"
with open(c3_path) as f:
    c3 = json.load(f)

fixed_c3 = False
for tile in c3["tiles"]:
    if tile["tile_id"] != "tile_python_pep8_style":
        continue
    for item in tile["interactions"]:
        if item["step_id"] != "tile_python_pep8_style.s03":
            continue
        pub = item["interaction"]["public"]
        old_prompt = pub["prompt"]
        # The prompt has instructions 1-5; remove #3 and renumber 4→3, 5→4
        # Current instructions:
        # 1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)
        # 2. Rename `Fee` → `fee` (lowercase)
        # 3. Rename `Minutes` → `minutes` and `Rate` → `rate` (lowercase)  ← REMOVE
        # 4. Use **4-space** indentation (not 2 spaces)
        # 5. Remove extraneous spaces inside `()` and before `,`
        # After removal and renumber:
        # 1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)
        # 2. Rename `Fee` → `fee` (lowercase)
        # 3. Use **4-space** indentation (not 2 spaces)
        # 4. Remove extraneous spaces inside `()` and before `,`
        new_prompt = (
            "Rewrite the function below to follow PEP 8:\n\n"
            "```python\n"
            "def CalcFee( minutes,rate ):\n"
            "  Fee=minutes*rate\n"
            "  return Fee\n\n"
            "print( CalcFee( 30,2 ) )\n"
            "```\n\n"
            "Apply these changes:\n"
            "1. Rename `CalcFee` \u2192 `calc_fee` (lowercase with underscores)\n"
            "2. Rename `Fee` \u2192 `fee` (lowercase)\n"
            "3. Use **4-space** indentation (not 2 spaces)\n"
            "4. Remove extraneous spaces inside `()` and before `,`\n\n"
            "The function must still return `minutes * rate` and the print should output `60` when called with `30` and `2`."
        )
        pub["prompt"] = new_prompt
        print(f"[c3] pep8/s03 prompt updated (instruction #3 removed, renumbered).")
        print(f"  OLD: {old_prompt[:120]}...")
        print(f"  NEW: {new_prompt[:120]}...")
        fixed_c3 = True

if not fixed_c3:
    print("WARNING: pep8/s03 not found in c3!")

with open(c3_path, "w") as f:
    json.dump(c3, f, indent=2, ensure_ascii=False)
print(f"[c3] Written: {c3_path}")
