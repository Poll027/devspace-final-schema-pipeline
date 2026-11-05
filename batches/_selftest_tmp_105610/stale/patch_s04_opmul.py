"""
Patch: fix tile_python_variables_types.s04 code_exercise.
The solution used `orders_per_driver * days_worked` which generates op_mul.
op_mul is not covered by any allowed_syntax descriptor (the descriptor
"using assigned names in an expression, as in the width * height example"
maps to set() in pysyntax.py, so it adds nothing to the allowed tag set).

Fix: redesign the exercise so the solution only uses plain assignment (=)
and a name reference, with no arithmetic operator.
New task: reassign total_orders to the value stored in orders_per_driver.
"""
import json, copy

PATH = "batches/final_batch_008_da_python_core/interactions.part.c0_canary.json"

with open(PATH) as f:
    data = json.load(f)

for tile in data["tiles"]:
    for item in tile["interactions"]:
        if item["step_id"] != "tile_python_variables_types.s04":
            continue
        ix = item["interaction"]

        # --- public.prompt ---
        ix["public"]["prompt"] = (
            "The QuickDeliver team tracks how many orders each driver handles per day.\n\n"
            "Three variables are already assigned below. Add one line that **reassigns** "
            "`total_orders` to the value currently stored in `orders_per_driver`.\n\n"
            "After your line runs:\n"
            "- `orders_per_driver` must still hold `23`\n"
            "- `days_worked` must still hold `5`\n"
            "- `total_orders` must hold `23` (the value stored in `orders_per_driver`)\n\n"
            "Use only `name = value` assignment and the name of an already-assigned variable "
            "on the right-hand side. Do not use `print()`, `type()`, or any arithmetic operator."
        )

        # --- workspace starter (must NOT pass the tests) ---
        ix["public"]["workspace"]["files"][0]["content"] = (
            "orders_per_driver = 23\n"
            "days_worked = 5\n"
            "total_orders = 0\n"
            "# Reassign total_orders to the value stored in orders_per_driver\n"
        )

        # --- solution ---
        ix["grading"]["solution_files"][0]["content"] = (
            "orders_per_driver = 23\n"
            "days_worked = 5\n"
            "total_orders = 0\n"
            "total_orders = orders_per_driver\n"
        )

        # --- tests ---
        ix["grading"]["tests"] = [
            {
                "test_id": "t1_orders_per_driver",
                "kind": "value_equals",
                "spec": {"expr": "orders_per_driver", "expected": 23},
                "visible": True,
                "message_on_fail": "`orders_per_driver` should still hold `23` after your reassignment."
            },
            {
                "test_id": "t2_days_worked",
                "kind": "value_equals",
                "spec": {"expr": "days_worked", "expected": 5},
                "visible": True,
                "message_on_fail": "`days_worked` should still hold `5` — reassigning `total_orders` must not change the other variables."
            },
            {
                "test_id": "t3_total_orders",
                "kind": "value_equals",
                "spec": {"expr": "total_orders", "expected": 23},
                "visible": True,
                "message_on_fail": "`total_orders` should hold `23` (the value stored in `orders_per_driver`). Check that you wrote `total_orders = orders_per_driver`."
            }
        ]

        # --- feedback ---
        ix["feedback"]["correct"]["message"] = (
            "Right — `total_orders` now holds `23`, the value stored in `orders_per_driver`. "
            "Reassigning a name replaces what it held; the other names are unchanged."
        )
        ix["feedback"]["incorrect"]["message"] = (
            "Check that you added exactly one line: `total_orders = orders_per_driver`. "
            "The right-hand side should be the name `orders_per_driver`, not a literal number."
        )
        ix["feedback"]["hints"] = [
            "The right-hand side of `=` can be a name that was already assigned. What name holds the value you want?",
            "After `total_orders = orders_per_driver`, what value does `total_orders` hold? What about `orders_per_driver`?"
        ]

        print("Patched s04.")
        break

with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done.")
