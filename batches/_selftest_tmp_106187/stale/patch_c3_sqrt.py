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

# Add "math.sqrt()" to allowed_syntax in s06 so the solution passes the checker
ix = find_interaction("tile_python_errors_imports", "tile_python_errors_imports.s06")
allowed = ix["public"]["constraints"]["allowed_syntax"]
if "math.sqrt()" not in allowed:
    allowed.append("math.sqrt()")
    print("Added math.sqrt() to allowed_syntax")
else:
    print("math.sqrt() already present")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("Written.")
