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

# Fix s14: feedback.incorrect must be an object with "message" key, not a plain string
ix14 = find_interaction("tile_python_functions_scope", "tile_python_functions_scope.s14")

# Check current state
print("Before fix - feedback.incorrect type:", type(ix14["feedback"]["incorrect"]))

# Fix: wrap in object if it's a string
if isinstance(ix14["feedback"]["incorrect"], str):
    ix14["feedback"]["incorrect"] = {"message": ix14["feedback"]["incorrect"]}

print("After fix - feedback.incorrect:", ix14["feedback"]["incorrect"])

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fix applied.")
