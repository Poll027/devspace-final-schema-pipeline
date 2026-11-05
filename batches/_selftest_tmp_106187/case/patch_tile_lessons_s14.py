"""Patch tile_lessons/tile_python_functions_scope.json: add 'order_id=value' and 'city=value'
to the allowed_syntax of tile_python_functions_scope.s14."""
import json

path = "batches/final_batch_008_da_python_core/tile_lessons/tile_python_functions_scope.json"

with open(path) as f:
    data = json.load(f)

patched = False
for step in data.get("steps", []):
    if step.get("step_id") == "tile_python_functions_scope.s14":
        ix = step.get("interaction", {})
        allowed = ix.get("public", {}).get("constraints", {}).get("allowed_syntax", [])
        for desc in ["order_id=value", "city=value"]:
            if desc not in allowed:
                allowed.append(desc)
                print(f"  Added: {desc!r}")
        patched = True
        break

if not patched:
    raise RuntimeError("Step tile_python_functions_scope.s14 not found in tile_lessons!")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Patch applied to tile_lessons successfully.")
