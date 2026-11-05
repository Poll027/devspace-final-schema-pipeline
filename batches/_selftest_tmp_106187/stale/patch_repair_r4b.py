"""
Apply the same fixes to interactions.json (the assembled file used by assemble_tiles.py).
"""
import json

with open('batches/final_batch_008_da_python_core/interactions.json') as f:
    data = json.load(f)

# ── Fix 1: tile_python_lists_dicts_tuples.s10 ──────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] != 'tile_python_lists_dicts_tuples':
        continue
    for step in tile['interactions']:
        if step['step_id'] != 'tile_python_lists_dicts_tuples.s10':
            continue
        ix = step['interaction']

        ix['public']['prompt'] = (
            "QuickDeliver maps order IDs to cities. `order_city` is assigned below "
            "using scalar city variables.\n\n"
            "Add lines that:\n"
            "1. Add a new entry: key `1045`, value `new_city`\n"
            "2. Assign `city` — the value for key `1042`\n"
            "3. Print `city` and `order_city[1045]` each on its own line\n\n"
            "Expected output:\n"
            "```\n"
            "Lagos\n"
            "Ibadan\n"
            "```"
        )

        ix['public']['workspace']['files'][0]['content'] = (
            "city_a = 'Lagos'\n"
            "city_b = 'Abuja'\n"
            "city_c = 'Kano'\n"
            "new_city = 'Ibadan'\n"
            "order_city = {1042: city_a, 1043: city_b, 1044: city_c}\n"
            "# Add key 1045 -> new_city, look up key 1042, then print city and order_city[1045]\n"
        )

        new_solution = (
            "city_a = 'Lagos'\n"
            "city_b = 'Abuja'\n"
            "city_c = 'Kano'\n"
            "new_city = 'Ibadan'\n"
            "order_city = {1042: city_a, 1043: city_b, 1044: city_c}\n"
            "order_city[1045] = new_city\n"
            "city = order_city[1042]\n"
            "print(city)\n"
            "print(order_city[1045])\n"
        )
        ix['grading']['solution_files'][0]['content'] = new_solution

        ix['grading']['tests'] = [
            {
                "test_id": "t1_stdout",
                "kind": "stdout_equals",
                "spec": {"expected": "Lagos\nIbadan"},
                "visible": True,
                "message_on_fail": "Output does not match. Print `city` then `order_city[1045]`, each on its own line."
            },
            {
                "test_id": "t2_city",
                "kind": "value_equals",
                "spec": {"expr": "city", "expected": "Lagos"},
                "visible": True,
                "message_on_fail": "`city` should be `'Lagos'`. Use `city = order_city[1042]` to look up the value for key `1042`."
            },
            {
                "test_id": "t3_new_entry",
                "kind": "value_equals",
                "spec": {"expr": "order_city[1045]", "expected": "Ibadan"},
                "visible": True,
                "message_on_fail": "`order_city[1045]` should be `'Ibadan'`. Use `order_city[1045] = new_city` to add the entry."
            }
        ]

        ix['feedback']['correct']['message'] = (
            "All correct — `order_city[1045] = new_city` adds the entry, "
            "`order_city[1042]` returns `city_a` (`'Lagos'`), and "
            "`order_city[1045]` returns `new_city` (`'Ibadan'`)."
        )
        ix['feedback']['incorrect']['message'] = (
            "Use `d[key] = value` to add/update, and `d[key]` to look up. "
            "Make sure you assign `city = order_city[1042]` and print both `city` and `order_city[1045]`."
        )
        ix['feedback']['hints'] = [
            "To add a new key-value pair: `order_city[1045] = new_city`. To look up: `city = order_city[1042]`.",
            "Print each result on its own line: `print(city)` then `print(order_city[1045])`."
        ]

        # Remove hidden_checks and execution_provenance so assemble recomputes them
        ix['grading'].pop('hidden_checks', None)
        ix['grading'].pop('execution_provenance', None)

        print("Fixed tile_python_lists_dicts_tuples.s10 in interactions.json")
        break

# ── Fix 2: tile_python_sets_strings.s06 ────────────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] != 'tile_python_sets_strings':
        continue
    for step in tile['interactions']:
        if step['step_id'] != 'tile_python_sets_strings.s06':
            continue
        ix = step['interaction']

        for t in ix['grading']['tests']:
            if t['test_id'] == 't2_unique_count':
                t['test_id'] = 't2_lagos_present'
                t['kind'] = 'value_equals'
                t['spec'] = {'expr': "'Lagos' in unique_cities", 'expected': True}
                t['message_on_fail'] = (
                    "`'Lagos'` should be in `unique_cities`. "
                    "Use `unique_cities = set(cities_list)` — `city_a` is `'Lagos'` and appears in `cities_list`."
                )
                break

        # Remove hidden_checks and execution_provenance so assemble recomputes them
        ix['grading'].pop('hidden_checks', None)
        ix['grading'].pop('execution_provenance', None)

        print("Fixed tile_python_sets_strings.s06 in interactions.json")
        break

with open('batches/final_batch_008_da_python_core/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done.")
