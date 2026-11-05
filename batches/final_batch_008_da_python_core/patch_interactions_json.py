"""Patch interactions.json: fix s06 solution to avoid attr:items and attr_module."""
import json

with open('batches/final_batch_008_da_python_core/interactions.json') as f:
    data = json.load(f)

patched = False
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_python_comprehensions_iterating':
        for entry in tile['interactions']:
            if entry['step_id'] == 'tile_python_comprehensions_iterating.s06':
                ix = entry['interaction']

                # 1. Change the prompt
                ix['public']['prompt'] = (
                    "QuickDeliver stores a mapping of order IDs to cities.\n\n"
                    "`order_city` is already assigned below using city variables.\n\n"
                    "Add a `for` loop that iterates directly over `order_city` (which yields each key), "
                    "then prints the order ID and its city on one line using `order_city[key]` to look up the value.\n\n"
                    "Expected output:\n"
                    "```\n"
                    "1042 Lagos\n"
                    "1043 Abuja\n"
                    "1044 Kano\n"
                    "```"
                )

                # 2. Change the solution
                new_solution = (
                    "city_a = 'Lagos'\n"
                    "city_b = 'Abuja'\n"
                    "city_c = 'Kano'\n"
                    "order_city = {1042: city_a, 1043: city_b, 1044: city_c}\n"
                    "for key in order_city:\n"
                    "    print(key, order_city[key])\n"
                )
                ix['grading']['solution_files'][0]['content'] = new_solution

                # 3. Update hints and feedback
                ix['feedback']['correct']['message'] = (
                    "Every key-value pair was printed exactly once. "
                    "Looping directly over a dictionary yields its keys; `order_city[key]` retrieves the matching value."
                )
                ix['feedback']['incorrect']['message'] = (
                    "Use `for key in order_city:` to iterate over the keys, "
                    "then `print(key, order_city[key])` inside the loop body to print each key and its value."
                )
                ix['feedback']['hints'] = [
                    "Looping directly over a dictionary with `for key in order_city:` gives you each key on every pass.",
                    "Inside the loop, `order_city[key]` looks up the value for that key — use `print(key, order_city[key])` to print both."
                ]

                # 4. Update message_on_fail
                ix['grading']['tests'][0]['message_on_fail'] = (
                    "Expected three lines, one per entry. "
                    "Use `for key in order_city:` and `print(key, order_city[key])`."
                )

                patched = True
                print("Patched s06 in interactions.json successfully.")
                break

if not patched:
    print("ERROR: s06 not found!")

with open('batches/final_batch_008_da_python_core/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Written.")
