#!/usr/bin/env python3
"""
Revert s05 change (append causes attr_module violation with blocked module.name).
Keep s13 and s09 fixes.
"""
import json

SRC = 'batches/final_batch_008_da_python_core/interactions.part.c1.json'

with open(SRC) as f:
    data = json.load(f)

# Revert s05 to original concatenation approach
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_python_lists_dicts_tuples':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_python_lists_dicts_tuples.s05':
                ix = item['interaction']
                
                # Revert prompt step 4
                old_step4 = "4. Append `new_time` to `delivery_times` using `.append()`"
                new_step4 = "4. Reassign `delivery_times` to `delivery_times + [new_time]` (adds `new_time` to the end)"
                assert old_step4 in ix['public']['prompt'], "Step 4 text not found"
                ix['public']['prompt'] = ix['public']['prompt'].replace(old_step4, new_step4)
                
                # Revert solution
                old_sol_line = "delivery_times.append(new_time)\n"
                new_sol_line = "delivery_times = delivery_times + [new_time]\n"
                sol = ix['grading']['solution_files'][0]['content']
                assert old_sol_line in sol, "append line not found"
                ix['grading']['solution_files'][0]['content'] = sol.replace(old_sol_line, new_sol_line)
                
                # Revert feedback
                ix['feedback']['correct']['message'] = (
                    "All correct — `delivery_times[0]` gives `first`, `delivery_times[-1]` gives `last`, "
                    "`delivery_times[1:3]` gives `sliced`, and `delivery_times + [new_time]` extends the list."
                )
                ix['feedback']['incorrect']['message'] = (
                    "Use `delivery_times[0]` for the first item, `delivery_times[-1]` for the last, "
                    "`delivery_times[1:3]` for the slice, and `delivery_times = delivery_times + [new_time]` to extend."
                )
                old_hint2 = "To add `new_time` to the end: `delivery_times.append(new_time)`. `.append()` modifies the list in place."
                new_hint2 = "To add `new_time` to the end: `delivery_times = delivery_times + [new_time]`. This creates a new list with `new_time` appended."
                assert old_hint2 in ix['feedback']['hints'], "Hint 2 not found"
                ix['feedback']['hints'][ix['feedback']['hints'].index(old_hint2)] = new_hint2
                
                print("Reverted s05 to concatenation")

with open(SRC, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("s05 reverted in interactions.part.c1.json")
