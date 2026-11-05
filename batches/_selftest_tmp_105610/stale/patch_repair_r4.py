"""
Repair patch for interactions.part.c1.json:
1. tile_python_lists_dicts_tuples.s10: fix attr_module error and hard-coded tests
   - Remove .get() (blocked by attr_module via module.name in blocked_syntax)
   - Use scalar variables so mutations change the output
   - Replace t3_missing with t3_new_entry (tests order_city[1045])
2. tile_python_sets_strings.s06: fix t2_unique_count hard-coded test
   - Replace len(unique_cities)==4 with 'Lagos' in unique_cities (changes when city_a mutated)
"""
import json, copy

with open('batches/final_batch_008_da_python_core/interactions.part.c1.json') as f:
    data = json.load(f)

# ── Fix 1: tile_python_lists_dicts_tuples.s10 ──────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] != 'tile_python_lists_dicts_tuples':
        continue
    for step in tile['interactions']:
        if step['step_id'] != 'tile_python_lists_dicts_tuples.s10':
            continue
        ix = step['interaction']

        # New prompt: remove .get(), use new_city scalar, test membership
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

        # New starter: scalar variables so mutations affect the output
        ix['public']['workspace']['files'][0]['content'] = (
            "city_a = 'Lagos'\n"
            "city_b = 'Abuja'\n"
            "city_c = 'Kano'\n"
            "new_city = 'Ibadan'\n"
            "order_city = {1042: city_a, 1043: city_b, 1044: city_c}\n"
            "# Add key 1045 -> new_city, look up key 1042, then print city and order_city[1045]\n"
        )

        # New solution: no .get(), uses scalar variables
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

        # New tests: t1_stdout, t2_city, t3_new_entry (all change with mutations)
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

        # Update feedback messages to match new task
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

        print("Fixed tile_python_lists_dicts_tuples.s10")
        break

# ── Fix 2: tile_python_sets_strings.s06 ────────────────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] != 'tile_python_sets_strings':
        continue
    for step in tile['interactions']:
        if step['step_id'] != 'tile_python_sets_strings.s06':
            continue
        ix = step['interaction']

        # Replace t2_unique_count with a test that changes when city_a is mutated
        # 'Lagos' in unique_cities is True normally, False when city_a -> 'Lagos_x'
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

        print("Fixed tile_python_sets_strings.s06")
        break

with open('batches/final_batch_008_da_python_core/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done.")
