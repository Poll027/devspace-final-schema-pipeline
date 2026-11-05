"""
Patch tile_lessons/tile_python_functions_scope.json for s14:
Same changes as patch_s14_final.py but for the assembled tile_lessons file.
"""
import json

path = "batches/final_batch_008_da_python_core/tile_lessons/tile_python_functions_scope.json"

with open(path) as f:
    data = json.load(f)

patched = False
for step in data.get("steps", []):
    if step.get("step_id") != "tile_python_functions_scope.s14":
        continue
    ix = step.get("interaction", {})

    # 1. Revert allowed_syntax to glossary verbatim (remove extra entries)
    allowed = ix["public"]["constraints"]["allowed_syntax"]
    for extra in ["order_id=value", "city=value"]:
        if extra in allowed:
            allowed.remove(extra)
            print(f"Removed: {extra!r}")
    print(f"allowed_syntax count after revert: {len(allowed)}")

    # 2. Change the solution to use **dict unpacking for the second call
    new_solution = (
        "order_id1 = 1042\n"
        "order_id2 = 1043\n"
        "city2 = 'Abuja'\n"
        "\n"
        "def describe_order(order_id, city='Lagos'):\n"
        "    print(order_id, city)\n"
        "\n"
        "describe_order(order_id1)\n"
        "describe_order(**{'order_id': order_id2, 'city': city2})\n"
    )
    ix["grading"]["solution_files"][0]["content"] = new_solution
    print("Updated solution")

    # 3. Update the prompt
    new_prompt = (
        "Starter variables `order_id1 = 1042`, `order_id2 = 1043`, and `city2 = 'Abuja'` are already set.\n"
        "\n"
        "Add a default value of `'Lagos'` to the `city` parameter of `describe_order`.\n"
        "\n"
        "Then make two calls:\n"
        "1. `describe_order(order_id1)` — omit `city` so it uses the default `'Lagos'`\n"
        "2. `describe_order(**{'order_id': order_id2, 'city': city2})` — use `**dict` to pass keyword arguments by name\n"
        "\n"
        "Expected output:\n"
        "```\n"
        "1042 Lagos\n"
        "1043 Abuja\n"
        "```"
    )
    ix["public"]["prompt"] = new_prompt
    print("Updated prompt")

    # 4. Update the starter comment
    ix["public"]["workspace"]["files"][0]["content"] = (
        "# Starter variables are set below.\n"
        "# Add a default value of 'Lagos' to the city parameter.\n"
        "# Then:\n"
        "#   Call describe_order with only order_id1 (city uses its default)\n"
        "#   Call describe_order(**{'order_id': order_id2, 'city': city2})\n"
        "\n"
        "order_id1 = 1042\n"
        "order_id2 = 1043\n"
        "city2 = 'Abuja'\n"
        "\n"
        "def describe_order(order_id, city):\n"
        "    print(order_id, city)\n"
    )
    print("Updated starter")

    # 5. Update feedback messages
    ix["feedback"]["correct"]["message"] = (
        "Well done — the first call used the default `'Lagos'` for `city`, "
        "and the second call passed keyword arguments by name using `**dict`."
    )
    ix["feedback"]["incorrect"]["message"] = (
        "Change `def describe_order(order_id, city):` to `def describe_order(order_id, city='Lagos'):`. "
        "Then call it once with just `order_id1` and once with "
        "`describe_order(**{'order_id': order_id2, 'city': city2})`."
    )
    ix["feedback"]["hints"][0] = (
        "To add a default, change the parameter to `city='Lagos'` in the `def` line."
    )
    ix["feedback"]["hints"][1] = (
        "Use `describe_order(**{'order_id': order_id2, 'city': city2})` "
        "to pass keyword arguments by name via a dictionary."
    )
    print("Updated feedback")

    # 6. Update grading test message
    ix["grading"]["tests"][0]["message_on_fail"] = (
        "Expected '1042 Lagos' then '1043 Abuja'. "
        "Check that city has a default of 'Lagos' and that you use **dict in the second call."
    )
    print("Updated test message")

    patched = True
    break

if not patched:
    raise RuntimeError("Step tile_python_functions_scope.s14 not found in tile_lessons!")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Patch applied to tile_lessons successfully.")
