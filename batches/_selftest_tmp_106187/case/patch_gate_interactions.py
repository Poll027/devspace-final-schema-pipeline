"""
Patch the gate folder's interactions.json with the same fixes.
"""
import json

path = "batches/final_batch_008_da_python_core/working/gate_04_interactions_c1/interactions.json"

with open(path) as f:
    data = json.load(f)

changes = []

for tile in data.get("tiles", []):
    if tile.get("tile_id") == "tile_python_operators_conversion":
        for item in tile.get("interactions", []):
            step_id = item.get("step_id")
            interaction = item.get("interaction", {})
            feedback = interaction.get("feedback", {})

            if step_id == "tile_python_operators_conversion.s14":
                old = feedback.get("remediation_step_id")
                feedback["remediation_step_id"] = "tile_python_operators_conversion.r05"
                changes.append(f"s14: {old} -> r05")

            elif step_id == "tile_python_operators_conversion.s15":
                old = feedback.get("remediation_step_id")
                feedback["remediation_step_id"] = "tile_python_operators_conversion.r06"
                changes.append(f"s15: {old} -> r06")

            elif step_id == "tile_python_operators_conversion.s16":
                old = feedback.get("remediation_step_id")
                feedback["remediation_step_id"] = "tile_python_operators_conversion.r05"
                changes.append(f"s16: {old} -> r05")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Changes made to gate interactions.json:")
for c in changes:
    print(" ", c)
print("Done.")
