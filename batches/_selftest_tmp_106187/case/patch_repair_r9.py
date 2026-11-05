"""Repair round patch for interactions.part.c1.json.

Fixes:
1. tile_python_operators_conversion.s12: t1_stdout hard-coded answer.
   The starter used boolean literals (True/False) which py_var_mutations skips.
   Fix: use numeric starter variables (delivery_minutes, sla, distance_km, max_km)
   so that mutating sla from 45 to 52 changes is_late from True to False,
   changing the output from "True" to "False".

2. tile_python_operators_conversion.s16: t1_stdout, t2_dm_int_type, t3_dm_float_type
   hard-coded answers.
   The starter had delivery_minutes_str = '32' (string). String mutations append _x,
   making int('32_x') raise ValueError — the mutated script fails to run, so the
   result is None and the test is never added to mine (hard-coded).
   Fix: use delivery_minutes = 32 (int). Mutation gives 39. Solution converts:
     dm_str = str(delivery_minutes)   -> '32' (mutated: '39')
     dm_float = float(dm_str)         -> 32.0 (mutated: 39.0)
     dm_int = int(dm_str)             -> 32 (mutated: 39)
   Grade with value_equals mixing type and value so the expected changes with mutation.
"""
import json
from pathlib import Path

PATH = Path('batches/final_batch_008_da_python_core/interactions.part.c1.json')

with open(PATH) as f:
    d = json.load(f)

for tile in d['tiles']:
    if tile['tile_id'] != 'tile_python_operators_conversion':
        continue

    for ix_entry in tile['interactions']:
        sid = ix_entry['step_id']
        ix = ix_entry['interaction']

        # ── Fix 1: s12 ──────────────────────────────────────────────────────
        if sid == 'tile_python_operators_conversion.s12':
            # New prompt: single case with numeric inputs, demonstrates precedence
            ix['public']['prompt'] = (
                "QuickDeliver flags an order for review if it is late **or** it is far "
                "**and** not late (far-but-on-time is a different concern).\n\n"
                "The rule is: `is_late or is_far and not is_late`\n\n"
                "`delivery_minutes`, `sla`, `distance_km`, and `max_km` are assigned below.\n\n"
                "Add lines that:\n"
                "1. Assign `is_late` — `True` if `delivery_minutes > sla`, else `False`\n"
                "2. Assign `is_far` — `True` if `distance_km > max_km`, else `False`\n"
                "3. Print `is_late or is_far and not is_late`\n\n"
                "Expected output:\n"
                "```\n"
                "True\n"
                "```\n\n"
                "*(Hint: `and` has higher priority than `or`, so `is_far and not is_late` "
                "is evaluated first.)*"
            )

            # New starter: numeric variables
            ix['public']['workspace']['files'][0]['content'] = (
                "delivery_minutes = 50\n"
                "sla = 45\n"
                "distance_km = 5\n"
                "max_km = 10\n"
                "# Derive is_late and is_far, then print the compound expression\n"
            )

            # New solution: derives booleans from numeric inputs
            ix['grading']['solution_files'][0]['content'] = (
                "delivery_minutes = 50\n"
                "sla = 45\n"
                "distance_km = 5\n"
                "max_km = 10\n"
                "is_late = delivery_minutes > sla\n"
                "is_far = distance_km > max_km\n"
                "print(is_late or is_far and not is_late)\n"
            )

            # New test: single output line
            ix['grading']['tests'] = [
                {
                    "test_id": "t1_stdout",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "True"
                    },
                    "visible": True,
                    "message_on_fail": (
                        "Output does not match. Derive `is_late = delivery_minutes > sla` "
                        "and `is_far = distance_km > max_km`, then print "
                        "`is_late or is_far and not is_late`."
                    )
                }
            ]

            # Update feedback to match single-case design
            ix['feedback']['correct']['message'] = (
                "Correct — `and` has higher priority than `or`, so Python evaluates "
                "`is_far and not is_late` first (`False and False = False`), "
                "then `is_late or False = True`."
            )
            ix['feedback']['incorrect']['message'] = (
                "Derive `is_late = delivery_minutes > sla` and `is_far = distance_km > max_km`, "
                "then print `is_late or is_far and not is_late`. "
                "Remember: `and` binds tighter than `or`."
            )
            ix['feedback']['hints'] = [
                "Use `>` to derive `is_late` and `is_far` from the numeric inputs.",
                "For `is_late=True, is_far=False`: `is_far and not is_late` = "
                "`False and False` = `False`, then `True or False` = `True`."
            ]

        # ── Fix 2: s16 ──────────────────────────────────────────────────────
        if sid == 'tile_python_operators_conversion.s16':
            # New prompt: integer starter, convert to str/float/int
            ix['public']['prompt'] = (
                "A delivery record stores the time as an integer. "
                "Convert it to different types and print each result.\n\n"
                "`delivery_minutes` is assigned below as an integer.\n\n"
                "Add four lines that:\n"
                "1. Assign `dm_str` — `delivery_minutes` converted to a **string** using `str()`\n"
                "2. Assign `dm_float` — `dm_str` converted to a **float** using `float()`\n"
                "3. Assign `dm_int` — `dm_str` converted to an **integer** using `int()`\n"
                "4. Print `dm_str`, `dm_float`, and `dm_int` each on its own line.\n\n"
                "Expected output:\n"
                "```\n"
                "32\n"
                "32.0\n"
                "32\n"
                "```"
            )

            # New starter: integer variable
            ix['public']['workspace']['files'][0]['content'] = (
                "delivery_minutes = 32\n"
                "# Convert to str, float, and int; then print each\n"
            )

            # New solution
            ix['grading']['solution_files'][0]['content'] = (
                "delivery_minutes = 32\n"
                "dm_str = str(delivery_minutes)\n"
                "dm_float = float(dm_str)\n"
                "dm_int = int(dm_str)\n"
                "print(dm_str)\n"
                "print(dm_float)\n"
                "print(dm_int)\n"
            )

            # New tests: value_equals mixing type and value so they change with mutation
            ix['grading']['tests'] = [
                {
                    "test_id": "t1_dm_str",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "type(dm_str).__name__ + ':' + dm_str",
                        "expected": "str:32"
                    },
                    "visible": True,
                    "message_on_fail": (
                        "`dm_str` should be a string. Use `str(delivery_minutes)` to convert."
                    )
                },
                {
                    "test_id": "t2_dm_float",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "type(dm_float).__name__ + ':' + str(dm_float)",
                        "expected": "float:32.0"
                    },
                    "visible": True,
                    "message_on_fail": (
                        "`dm_float` should be a float. Use `float(dm_str)` to convert."
                    )
                },
                {
                    "test_id": "t3_dm_int",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "type(dm_int).__name__ + ':' + str(dm_int)",
                        "expected": "int:32"
                    },
                    "visible": True,
                    "message_on_fail": (
                        "`dm_int` should be an integer. Use `int(dm_str)` to convert."
                    )
                }
            ]

            # Update feedback
            ix['feedback']['correct']['message'] = (
                "All three conversions correct — `str(32)` gives `'32'`, "
                "`float('32')` gives `32.0`, and `int('32')` gives `32`."
            )
            ix['feedback']['incorrect']['message'] = (
                "Use `str()`, `float()`, and `str()` to convert between types. "
                "First convert `delivery_minutes` to a string with `str()`, "
                "then convert that string to float and int."
            )
            ix['feedback']['hints'] = [
                "Step 1: `dm_str = str(delivery_minutes)` converts the integer to a string.",
                "Step 2: `dm_float = float(dm_str)` and `dm_int = int(dm_str)` convert the string to float and int."
            ]

with open(PATH, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
