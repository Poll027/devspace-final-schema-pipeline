"""
Fix: revert s03 remediation_step_id back to r01 (s01 is not a remediation step).
The advisory about mismatched remediation facts generates only a warning, not an error.
"""
import json

files = [
    "batches/final_batch_008_da_python_core/interactions.part.c1.json",
    "batches/final_batch_008_da_python_core/working/gate_04_interactions_c1/interactions.json",
]

for path in files:
    with open(path) as f:
        data = json.load(f)

    for tile in data["tiles"]:
        if tile["tile_id"] == "tile_python_operators_conversion":
            for item in tile["interactions"]:
                if item["step_id"] == "tile_python_operators_conversion.s03":
                    ix = item["interaction"]
                    ix["feedback"]["remediation_step_id"] = "tile_python_operators_conversion.r01"
                    print(f"Reverted s03 remediation_step_id to r01 in {path}")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

print("Done.")
