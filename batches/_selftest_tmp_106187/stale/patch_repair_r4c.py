"""
Fix tile_python_lists_dicts_tuples.s05:
1. Add scalar variables so mutations change the output (fix hard-coded tests)
2. Replace delivery_times.append(27) with delivery_times = delivery_times + [new_time]
   to avoid attr_module (list.append() triggers attr_module which is blocked by module.name)
"""
import json

with open('batches/final_batch_008_da_python_core/interactions.json') as f:
    data = json.load(f)

# Also update interactions.part.c1.json
with open('batches/final_batch_008_da_python_core/interactions.part.c1.json') as f:
    data_part = json.load(f)

def fix_s05(ix):
    # New prompt: use new_time scalar, use + instead of .append()
    ix['public']['prompt'] = (
        "QuickDeliver stores delivery times in a list. `delivery_times` is assigned below "
        "from scalar time variables.\n\n"
        "Add lines that:\n"
        "1. Assign `first` — the item at index `0`\n"
        "2. Assign `last` — the item at index `-1`\n"
        "3. Assign `sliced` — items from index `1` up to (but not including) index `3`\n"
        "4. Reassign `delivery_times` to `delivery_times + [new_time]` (adds `new_time` to the end)\n\n"
        "Then print `first`, `last`, `sliced`, and `delivery_times` each on its own line.\n\n"
        "Expected output:\n"
        "```\n"
        "32\n"
        "18\n"
        "[45, 21]\n"
        "[32, 45, 21, 60, 18, 27]\n"
        "```"
    )

    # New starter: scalar variables
    ix['public']['workspace']['files'][0]['content'] = (
        "t0 = 32\n"
        "t1 = 45\n"
        "t2 = 21\n"
        "t3 = 60\n"
        "t4 = 18\n"
        "new_time = 27\n"
        "delivery_times = [t0, t1, t2, t3, t4]\n"
        "# Assign first, last, sliced; extend delivery_times with new_time; then print all four\n"
    )

    # New solution: scalar variables, no .append()
    new_solution = (
        "t0 = 32\n"
        "t1 = 45\n"
        "t2 = 21\n"
        "t3 = 60\n"
        "t4 = 18\n"
        "new_time = 27\n"
        "delivery_times = [t0, t1, t2, t3, t4]\n"
        "first = delivery_times[0]\n"
        "last = delivery_times[-1]\n"
        "sliced = delivery_times[1:3]\n"
        "delivery_times = delivery_times + [new_time]\n"
        "print(first)\n"
        "print(last)\n"
        "print(sliced)\n"
        "print(delivery_times)\n"
    )
    ix['grading']['solution_files'][0]['content'] = new_solution

    # Tests remain the same structure but expected values are the same
    ix['grading']['tests'] = [
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": "32\n18\n[45, 21]\n[32, 45, 21, 60, 18, 27]"},
            "visible": True,
            "message_on_fail": "Output does not match. Print `first`, `last`, `sliced`, `delivery_times` each on its own line in that order."
        },
        {
            "test_id": "t2_sliced",
            "kind": "value_equals",
            "spec": {"expr": "sliced", "expected": [45, 21]},
            "visible": True,
            "message_on_fail": "`sliced` should be `[45, 21]`. Use `delivery_times[1:3]` — the end index is excluded."
        }
    ]

    # Remove cached values so assemble recomputes them
    ix['grading'].pop('hidden_checks', None)
    ix['grading'].pop('execution_provenance', None)

    # Update feedback
    ix['feedback']['correct']['message'] = (
        "All correct — `delivery_times[0]` gives `first`, `delivery_times[-1]` gives `last`, "
        "`delivery_times[1:3]` gives `sliced`, and `delivery_times + [new_time]` extends the list."
    )
    ix['feedback']['incorrect']['message'] = (
        "Use `delivery_times[0]` for the first item, `delivery_times[-1]` for the last, "
        "`delivery_times[1:3]` for the slice, and `delivery_times = delivery_times + [new_time]` to extend."
    )
    ix['feedback']['hints'] = [
        "Index `0` gives the first item; index `-1` gives the last. Slicing `[1:3]` gives items at positions 1 and 2.",
        "To add `new_time` to the end: `delivery_times = delivery_times + [new_time]`. This creates a new list with `new_time` appended."
    ]

# Fix in interactions.json
for tile in data['tiles']:
    if tile['tile_id'] != 'tile_python_lists_dicts_tuples':
        continue
    for step in tile['interactions']:
        if step['step_id'] != 'tile_python_lists_dicts_tuples.s05':
            continue
        fix_s05(step['interaction'])
        print("Fixed s05 in interactions.json")
        break

# Fix in interactions.part.c1.json
for tile in data_part['tiles']:
    if tile['tile_id'] != 'tile_python_lists_dicts_tuples':
        continue
    for step in tile['interactions']:
        if step['step_id'] != 'tile_python_lists_dicts_tuples.s05':
            continue
        fix_s05(step['interaction'])
        print("Fixed s05 in interactions.part.c1.json")
        break

with open('batches/final_batch_008_da_python_core/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)

with open('batches/final_batch_008_da_python_core/interactions.part.c1.json', 'w') as f:
    json.dump(data_part, f, indent=2)

print("Done.")
