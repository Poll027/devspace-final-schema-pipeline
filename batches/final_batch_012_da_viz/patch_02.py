import json

path = "batches/final_batch_012_da_viz/scenario_asset_registry.json"

with open(path) as f:
    data = json.load(f)

# Remove variant_kind from ds.orders.messy (not in schema, additionalProperties: false)
for asset in data["assets"]:
    if asset["asset_id"] == "ds.orders":
        for variant in asset.get("variants", []):
            if variant.get("variant_id") == "ds.orders.messy":
                if "variant_kind" in variant:
                    del variant["variant_kind"]
                    print("Removed variant_kind from ds.orders.messy")
        break

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Patch applied.")
