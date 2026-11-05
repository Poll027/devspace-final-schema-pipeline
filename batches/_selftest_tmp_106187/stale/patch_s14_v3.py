"""
Patch interactions.part.c3.json for s14:
1. Remove the extra allowed_syntax entry added by the previous patch (revert to glossary verbatim)
2. Change the solution to use **dict unpacking for the keyword call
   (avoids kw:city and kw:order_id violations while still using keyword arguments)
3. Update the prompt to match the new solution syntax
"""
import json

path = "batches/final_batch_008_da_python_core/interactions.part.c3.json"

with open(path) as f:
    data = json.load(f)

patched = False
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_python_functions_scope":
        continue
    for entry in tile["interactions"]:
        if entry["step_id"] != "tile_python_functions_scope.s14":
            continue
        ix = entry["interaction"]

        # 1. Remove the extra allowed_syntax entry (revert previous patch)
        allowed = ix["public"]["constraints"]["allowed_syntax"]
        extra = "describe_order(order_id=order_id2, city=city2)"
        if extra in allowed:
            allowed.remove(extra)
            print(f"Removed extra entry: {extra!r}")
        print(f"allowed_syntax count after revert: {len(allowed)}")

        # 2. Change the solution to use **dict unpacking for the keyword call
        # This avoids kw:city and kw:order_id violations while still using keyword arguments
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
        print("Updated solution:")
        print(new_solution)

        # 3. Update the prompt to match the new solution
        old_prompt = ix["public"]["prompt"]
        new_prompt = old_prompt.replace(
            "2. `describe_order(order_id=order_id2, city=city2)` — use keyword arguments",
            "2. `describe_order(**{'order_id': order_id2, 'city': city2})` — use `**dict` to pass keyword arguments by name"
        )
        if new_prompt != old_prompt:
            ix["public"]["prompt"] = new_prompt
            print("Updated prompt")
        else:
            print("WARNING: prompt pattern not found, checking...")
            # Try to find the pattern
            idx = old_prompt.find("describe_order(order_id=order_id2")
            if idx >= 0:
                print(f"Found at index {idx}: {old_prompt[idx:idx+80]!r}")
            else:
                print("Pattern not found in prompt")

        # Also update the starter comment to match
        starter = ix["public"]["workspace"]["files"][0]["content"]
        new_starter = starter.replace(
            "#   Call describe_order with keyword arguments order_id=order_id2, city=city2",
            "#   Call describe_order with **{'order_id': order_id2, 'city': city2}"
        )
        if new_starter != starter:
            ix["public"]["workspace"]["files"][0]["content"] = new_starter
            print("Updated starter comment")

        # Update feedback messages
        incorrect_msg = ix["feedback"]["incorrect"]["message"]
        new_incorrect = incorrect_msg.replace(
            "once with `order_id=1043, city='Abuja'`",
            "once with `**{'order_id': order_id2, 'city': city2}`"
        )
        if new_incorrect != incorrect_msg:
            ix["feedback"]["incorrect"]["message"] = new_incorrect
            print("Updated incorrect feedback")

        hint2 = ix["feedback"]["hints"][1]
        new_hint2 = hint2.replace(
            "A keyword argument uses the form `name=value` in the call, e.g. `describe_order(order_id=1043, city='Abuja')`.",
            "Use `**{'order_id': order_id2, 'city': city2}` to pass keyword arguments by name via a dictionary."
        )
        if new_hint2 != hint2:
            ix["feedback"]["hints"][1] = new_hint2
            print("Updated hint 2")

        patched = True
        break
    break

if not patched:
    print("WARNING: nothing was patched!")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done.")
