"""
Final patch for interactions.part.c3.json:
1. Remove extra allowed_syntax entries (order_id=value, city=value) added by previous patch
2. Keep the evaluator's prescribed fix: solution uses describe_order(order_id=order_id2, city=city2)
3. Keep s06 fix: math.sqrt(x)
4. Keep pep8 s03 advisory fix
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

# Remove extra allowed_syntax entries from s14
ix14 = find_interaction(data, "tile_python_functions_scope", "tile_python_functions_scope.s14")
allowed = ix14["public"]["constraints"]["allowed_syntax"]
removed = []
for extra in ["order_id=value", "city=value"]:
    if extra in allowed:
        allowed.remove(extra)
        removed.append(extra)
print(f"Removed from allowed_syntax: {removed}")
print(f"allowed_syntax count: {len(allowed)}")

# Verify the solution is correct
sol = ix14["grading"]["solution_files"][0]["content"]
print(f"s14 solution: {sol!r}")

# Verify s06 solution
ix06 = find_interaction(data, "tile_python_errors_imports", "tile_python_errors_imports.s06")
sol06 = ix06["grading"]["solution_files"][0]["content"]
print(f"s06 solution: {sol06!r}")

src.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("Done.")
