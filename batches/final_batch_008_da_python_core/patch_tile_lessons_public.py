"""
Patch the tile_lessons_public file for tile_python_operators_conversion.
"""
import json

path = "batches/final_batch_008_da_python_core/working/gate_04_interactions_c1/tile_lessons_public/tile_python_operators_conversion.json"

with open(path) as f:
    tile = json.load(f)

changes = []

for step in tile.get("steps", []):
    sid = step.get("step_id", "")
    ix = step.get("interaction")
    if not ix:
        continue
    fb = ix.get("feedback", {})

    if sid == "tile_python_operators_conversion.s14":
        old = fb.get("remediation_step_id")
        fb["remediation_step_id"] = "tile_python_operators_conversion.r05"
        changes.append(f"s14: {old} -> r05")

    elif sid == "tile_python_operators_conversion.s15":
        old = fb.get("remediation_step_id")
        fb["remediation_step_id"] = "tile_python_operators_conversion.r06"
        changes.append(f"s15: {old} -> r06")

    elif sid == "tile_python_operators_conversion.s16":
        old = fb.get("remediation_step_id")
        fb["remediation_step_id"] = "tile_python_operators_conversion.r05"
        changes.append(f"s16: {old} -> r05")

with open(path, "w") as f:
    json.dump(tile, f, indent=2)
    f.write("\n")

print("Changes made to tile_lessons_public/tile_python_operators_conversion.json:")
for c in changes:
    print(" ", c)
print("Done.")
