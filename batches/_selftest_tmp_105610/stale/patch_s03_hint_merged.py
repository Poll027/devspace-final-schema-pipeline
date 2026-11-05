import json

path = "batches/final_batch_008_da_python_core/interactions.json"

with open(path) as f:
    data = json.load(f)

# Find tile_python_functions_scope, step s03
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_python_functions_scope":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_python_functions_scope.s03":
                hints = item["interaction"]["feedback"]["hints"]
                new_hint = "Variables defined outside the function are still readable inside it — `message` is accessible inside `greet_driver` without being passed as a parameter."
                if new_hint not in hints:
                    hints.append(new_hint)
                    print(f"Added hint to interactions.json. Hints now: {hints}")
                else:
                    print("Hint already present in interactions.json.")
                break

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
