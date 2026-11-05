#!/usr/bin/env python3
"""
Patch interactions.part.c1.json for REPAIR ROUND advisories:
  1. s05 (lists): change step 4 from concatenation to .append()
  2. s13 (tuples): remove recognize_tuple_immutability (f2) from measures and anchors
  3. s09 (sets_strings): change exercise from average to total to match anchor
  4. s03/r01 (operators): no change needed in this file (r01 is in screens)
"""
import json, copy

SRC = 'batches/final_batch_008_da_python_core/interactions.part.c1.json'
DST = SRC

with open(SRC) as f:
    data = json.load(f)

# ── Helper ──────────────────────────────────────────────────────────────────
def find_interaction(tile_id, step_id):
    for tile in data['tiles']:
        if tile['tile_id'] == tile_id:
            for item in tile['interactions']:
                if item['step_id'] == step_id:
                    return item['interaction']
    raise KeyError(f'{tile_id}/{step_id} not found')

# ════════════════════════════════════════════════════════════════════════════
# FIX 1 — s05: use .append() instead of concatenation
# ════════════════════════════════════════════════════════════════════════════
ix05 = find_interaction('tile_python_lists_dicts_tuples', 'tile_python_lists_dicts_tuples.s05')

# Update prompt: replace step 4 wording
old_step4 = "4. Reassign `delivery_times` to `delivery_times + [new_time]` (adds `new_time` to the end)"
new_step4 = "4. Append `new_time` to `delivery_times` using `.append()`"
assert old_step4 in ix05['public']['prompt'], f"Step 4 text not found in prompt"
ix05['public']['prompt'] = ix05['public']['prompt'].replace(old_step4, new_step4)

# Update solution: replace concatenation with append
old_sol_line = "delivery_times = delivery_times + [new_time]\n"
new_sol_line = "delivery_times.append(new_time)\n"
sol = ix05['grading']['solution_files'][0]['content']
assert old_sol_line in sol, f"Concatenation line not found in solution"
ix05['grading']['solution_files'][0]['content'] = sol.replace(old_sol_line, new_sol_line)

# Update feedback/hints to mention .append()
ix05['feedback']['correct']['message'] = (
    "All correct — `delivery_times[0]` gives `first`, `delivery_times[-1]` gives `last`, "
    "`delivery_times[1:3]` gives `sliced`, and `.append(new_time)` adds `new_time` to the end of the list."
)
ix05['feedback']['incorrect']['message'] = (
    "Use `delivery_times[0]` for the first item, `delivery_times[-1]` for the last, "
    "`delivery_times[1:3]` for the slice, and `delivery_times.append(new_time)` to add `new_time` to the end."
)
old_hint2 = "To add `new_time` to the end: `delivery_times = delivery_times + [new_time]`. This creates a new list with `new_time` appended."
new_hint2 = "To add `new_time` to the end: `delivery_times.append(new_time)`. `.append()` modifies the list in place."
assert old_hint2 in ix05['feedback']['hints'], f"Hint 2 not found"
ix05['feedback']['hints'][ix05['feedback']['hints'].index(old_hint2)] = new_hint2

# ════════════════════════════════════════════════════════════════════════════
# FIX 2 — s13: remove recognize_tuple_immutability (f2) from measures + anchors
# ════════════════════════════════════════════════════════════════════════════
ix13 = find_interaction('tile_python_lists_dicts_tuples', 'tile_python_lists_dicts_tuples.s13')

# Remove the immutability measure entry
before = len(ix13['measures'])
ix13['measures'] = [
    m for m in ix13['measures']
    if m.get('capability') != 'recognize_tuple_immutability'
]
after = len(ix13['measures'])
assert before - after == 1, f"Expected to remove 1 measure, removed {before - after}"

# Remove the immutability anchor
before_a = len(ix13['anchors'])
ix13['anchors'] = [
    a for a in ix13['anchors']
    if 'recognize_tuple_immutability' not in a
]
after_a = len(ix13['anchors'])
assert before_a - after_a == 1, f"Expected to remove 1 anchor, removed {before_a - after_a}"

# ════════════════════════════════════════════════════════════════════════════
# FIX 3 — s09: change exercise from average to total to match anchor
# Practice anchor success: "The printed sentence contains the computed total
#   rounded to two decimal places."
# Change: compute total (sum) and print it, not average.
# delivery_a=32, delivery_b=45 → total=77 → "Total delivery time: 77.00 minutes"
# ════════════════════════════════════════════════════════════════════════════
ix09 = find_interaction('tile_python_sets_strings', 'tile_python_sets_strings.s09')

# Update prompt
ix09['public']['prompt'] = (
    "QuickDeliver wants a summary sentence showing the total delivery time.\n\n"
    "`delivery_a` and `delivery_b` are assigned below.\n\n"
    "Add lines that:\n"
    "1. Assign `total` — the sum of `delivery_a` and `delivery_b`\n"
    "2. Print the sentence using an f-string with `total` formatted to **two decimal places**\n\n"
    "Expected output:\n"
    "```\n"
    "Total delivery time: 77.00 minutes\n"
    "```"
)

# Update solution
ix09['grading']['solution_files'][0]['content'] = (
    "delivery_a = 32\n"
    "delivery_b = 45\n"
    "total = delivery_a + delivery_b\n"
    "print(f\"Total delivery time: {total:.2f} minutes\")\n"
)

# Update tests
ix09['grading']['tests'] = [
    {
        "test_id": "t1_stdout",
        "kind": "stdout_equals",
        "spec": {
            "expected": "Total delivery time: 77.00 minutes"
        },
        "visible": True,
        "message_on_fail": "Output does not match. Use an f-string with `{total:.2f}` to format the total to two decimal places."
    },
    {
        "test_id": "t2_total",
        "kind": "value_equals",
        "spec": {
            "expr": "total",
            "expected": 77
        },
        "visible": True,
        "message_on_fail": "`total` should be `77`. Compute `total = delivery_a + delivery_b`."
    }
]

# Update feedback
ix09['feedback']['correct']['message'] = (
    "Correct — `{total:.2f}` in the f-string formats `77` as `77.00`, "
    "giving the sentence `Total delivery time: 77.00 minutes`."
)
ix09['feedback']['incorrect']['message'] = (
    "Use an f-string: `f\"Total delivery time: {total:.2f} minutes\"`. "
    "The `:.2f` format specifier formats to two decimal places."
)
ix09['feedback']['hints'] = [
    "An f-string starts with `f` before the opening quote: `f\"...\"`.",
    "To embed a value formatted to two decimal places, write `{total:.2f}` inside the f-string."
]

# ════════════════════════════════════════════════════════════════════════════
# Write output
# ════════════════════════════════════════════════════════════════════════════
with open(DST, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Patch applied successfully.")
print(f"  s05: step 4 now uses .append()")
print(f"  s13: removed recognize_tuple_immutability from measures and anchors")
print(f"  s09: exercise now computes total (77.00) instead of average (38.50)")
