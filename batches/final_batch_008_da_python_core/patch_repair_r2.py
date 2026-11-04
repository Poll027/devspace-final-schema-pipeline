#!/usr/bin/env python3
"""
Repair patch v3 for s04 interaction (REPAIR ROUND):

BLOCKING fix: The success sentence "built from the others" is satisfied by
  total_orders = orders_per_driver (a copy reads the value of another assigned
  variable; per GENERATOR.md note 9b, allowed_syntax wins and a copy satisfies
  "built from the others" in the sense of "derived from another assigned name").
  The allowed_syntax must be verbatim from the glossary (gate enforces this),
  so * cannot be added. Revert solution and t3 to the copy exercise.
  Also restore verbatim allowed_syntax (remove the extra '+ - * / // % **' entry).

ADVISORY: Do NOT remove choose_valid_variable_name - tile plan requires it.
"""
import json

SRC = 'batches/final_batch_008_da_python_core/interactions.part.c0_canary.json'

with open(SRC) as f:
    data = json.load(f)

for tile in data['tiles']:
    for item in tile['interactions']:
        if item['step_id'] != 'tile_python_variables_types.s04':
            continue
        ix = item['interaction']

        # 1. Restore verbatim allowed_syntax from glossary (remove extra entry)
        ix['public']['constraints']['allowed_syntax'] = [
            "name = value assignment",
            "using assigned names in an expression, as in the width * height example",
            "whole-number literals as in the examples"
        ]

        # 2. Restore prompt: copy exercise (allowed_syntax wins per GENERATOR.md note 9b)
        #    "built from the others" is satisfied by reading another assigned variable's value.
        ix['public']['prompt'] = (
            "The QuickDeliver team tracks how many orders each driver handles per day.\n\n"
            "Three variables are already assigned below. Add one line that **reassigns** "
            "`total_orders` to the value currently stored in `orders_per_driver`.\n\n"
            "After your line runs:\n"
            "- `orders_per_driver` must still hold `23`\n"
            "- `days_worked` must still hold `5`\n"
            "- `total_orders` must hold `23` (the value read from `orders_per_driver`)\n\n"
            "Use only `name = value` assignment and the name of an already-assigned variable "
            "on the right-hand side. Do not use `print()`, `type()`, or any arithmetic operator."
        )

        # 3. Restore starter comment
        ix['public']['workspace']['files'][0]['content'] = (
            "orders_per_driver = 23\n"
            "days_worked = 5\n"
            "total_orders = 0\n"
            "# Reassign total_orders to the value stored in orders_per_driver\n"
        )

        # 4. Restore solution: copy exercise
        ix['grading']['solution_files'][0]['content'] = (
            "orders_per_driver = 23\n"
            "days_worked = 5\n"
            "total_orders = 0\n"
            "total_orders = orders_per_driver\n"
        )

        # 5. Restore t3 expected value to 23
        for test in ix['grading']['tests']:
            if test['test_id'] == 't3_total_orders':
                test['spec']['expected'] = 23
                test['message_on_fail'] = (
                    "`total_orders` should hold `23` "
                    "(the value stored in `orders_per_driver`). "
                    "Check that you wrote `total_orders = orders_per_driver`."
                )

        # 6. Ensure choose_valid_variable_name is in measures and anchors (tile plan requires it)
        has_cvn_measure = any(
            m.get('capability') == 'choose_valid_variable_name'
            for m in ix['measures']
        )
        if not has_cvn_measure:
            ix['measures'].append({
                "concept_id": "python.variables_assignment",
                "capability": "choose_valid_variable_name",
                "fact_ids": ["f4"]
            })
        has_cvn_anchor = any(
            'choose_valid_variable_name' in a for a in ix['anchors']
        )
        if not has_cvn_anchor:
            ix['anchors'].append(
                "python.variables_assignment#assessment:choose_valid_variable_name"
            )

        # 7. Restore feedback messages
        ix['feedback']['correct']['message'] = (
            "Right \u2014 `total_orders` now holds `23`, the value stored in "
            "`orders_per_driver`. Reassigning a name replaces what it held; "
            "the other names are unchanged."
        )
        ix['feedback']['incorrect']['message'] = (
            "Check that you added exactly one line: `total_orders = orders_per_driver`. "
            "The right-hand side should be the name `orders_per_driver`, not a literal number."
        )
        ix['feedback']['hints'] = [
            "The right-hand side of `=` can be a name that was already assigned. "
            "What name holds the value you want?",
            "After `total_orders = orders_per_driver`, what value does `total_orders` hold? "
            "What about `orders_per_driver`?"
        ]

        break

with open(SRC, 'w') as f:
    json.dump(data, f, indent=2)

print("Patch v3 applied.")
