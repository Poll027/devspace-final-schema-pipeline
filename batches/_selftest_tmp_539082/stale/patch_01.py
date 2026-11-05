import json, re

path = "batches/final_batch_009_da_pandas/scenario_asset_registry.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Locate cw_dtype_datetime asset
for asset in data["assets"]:
    if asset["asset_id"] == "cw_dtype_datetime":
        for file_entry in asset["files"]:
            if file_entry["path"] == "starter.py":
                old = file_entry["content"]
                # Replace the TODO line for astype() with a hint about pd.to_numeric
                new = old.replace(
                    "# TODO: convert distance_km to float with astype()",
                    "# TODO: convert distance_km to float\n# Hint: 'unknown' values will cause astype(float) to fail — use pd.to_numeric(errors='coerce') instead"
                )
                assert new != old, "Replacement did not match — check the string"
                file_entry["content"] = new
                print("Patched cw_dtype_datetime/starter.py")
                print("OLD snippet:", repr(old[old.find("# TODO: convert distance_km"):old.find("# TODO: convert distance_km")+60]))
                print("NEW snippet:", repr(new[new.find("# TODO: convert distance_km"):new.find("# TODO: convert distance_km")+120]))

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
