import json

path = "batches/final_batch_007_da_nocode/scenario_asset_registry.json"

with open(path) as f:
    data = json.load(f)

# Find ds_finding_statements asset
for asset in data["assets"]:
    if asset["asset_id"] == "ds_finding_statements":
        for row in asset["rows"]:
            if row[0] == 4:  # finding_id == 4
                # Fix vague_finding (index 1) and precise_finding (index 2)
                row[1] = "Driver 202 is our best driver."
                row[2] = "Driver 202 completed both assigned orders in March 2024 with an average delivery time of 21 minutes, the lowest among the five active drivers."
                print(f"Patched row 4: vague='{row[1]}', precise='{row[2]}'")
                break

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
