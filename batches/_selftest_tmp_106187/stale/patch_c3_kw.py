"""
Patch interactions.part.c3.json — add kw:order_id and kw:city to allowed_syntax for s14.
This is an incremental patch on top of the already-applied blocking fixes.
"""
import json, pathlib

src = pathlib.Path("batches/final_batch_008_da_python_core/interactions.part.c3.json")
data = json.loads(src.read_text())

def find_interaction(data, tile_id, step_id):
    for tile in data["tiles"]:
        if tile["tile_id"] == tile_id:
            for item in tile["interactions"]:
                if item["step_id"] == step_id:
                    return item["interaction"]
    raise KeyError(f"{tile_id}/{step_id} not found")

ix14 = find_interaction(data, "tile_python_functions_scope", "tile_python_functions_scope.s14")
allowed = ix14["public"]["constraints"]["allowed_syntax"]

added = []
if "order_id=value" not in allowed:
    allowed.append("order_id=value")
    added.append("order_id=value")
if "city=value" not in allowed:
    allowed.append("city=value")
    added.append("city=value")

print(f"Added to allowed_syntax: {added}")

src.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("Done.")
