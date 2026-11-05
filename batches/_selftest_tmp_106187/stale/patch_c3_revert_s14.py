import json

path = "batches/final_batch_008_da_python_core/interactions.part.c3.json"

with open(path) as f:
    data = json.load(f)

def find_interaction(tile_id, step_id):
    for tile in data["tiles"]:
        if tile["tile_id"] == tile_id:
            for item in tile["interactions"]:
                if item["step_id"] == step_id:
                    return item["interaction"]
    raise KeyError(f"{tile_id}/{step_id} not found")

# Revert s14 back to original **dict form (advisory change broke the gate)
ix14 = find_interaction("tile_python_functions_scope", "tile_python_functions_scope.s14")

# Restore original prompt
ix14["public"]["prompt"] = (
    "Starter variables `order_id1 = 1042`, `order_id2 = 1043`, and `city2 = 'Abuja'` are already set.\n\n"
    "Add a default value of `'Lagos'` to the `city` parameter of `describe_order`.\n\n"
    "Then make two calls:\n"
    "1. `describe_order(order_id1)` \u2014 omit `city` so it uses the default `'Lagos'`\n"
    "2. `describe_order(**{'order_id': order_id2, 'city': city2})` \u2014 use `**dict` to pass keyword arguments by name\n\n"
    "Expected output:\n"
    "```\n"
    "1042 Lagos\n"
    "1043 Abuja\n"
    "```"
)

# Restore original starter
ix14["public"]["workspace"]["files"][0]["content"] = (
    "# Starter variables are set below.\n"
    "# Add a default value of 'Lagos' to the city parameter.\n"
    "# Then:\n"
    "#   Call describe_order with only order_id1 (city uses its default)\n"
    "#   Call describe_order with **{'order_id': order_id2, 'city': city2}\n\n"
    "order_id1 = 1042\n"
    "order_id2 = 1043\n"
    "city2 = 'Abuja'\n\n"
    "def describe_order(order_id, city):\n"
    "    print(order_id, city)\n"
)

# Restore original solution
ix14["grading"]["solution_files"][0]["content"] = (
    "order_id1 = 1042\n"
    "order_id2 = 1043\n"
    "city2 = 'Abuja'\n\n"
    "def describe_order(order_id, city='Lagos'):\n"
    "    print(order_id, city)\n\n"
    "describe_order(order_id1)\n"
    "describe_order(**{'order_id': order_id2, 'city': city2})\n"
)

# Restore original feedback
ix14["feedback"]["incorrect"] = {
    "message": (
        "Change `def describe_order(order_id, city):` to `def describe_order(order_id, city='Lagos'):`. "
        "Then call it once with just `1042` and once with `**{'order_id': order_id2, 'city': city2}`."
    )
}
ix14["feedback"]["hints"][1] = (
    "Use `**{'order_id': order_id2, 'city': city2}` to pass keyword arguments by name via a dictionary."
)

print("s14 reverted to original **dict form.")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Written.")
