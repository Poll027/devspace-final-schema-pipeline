import json, sys

path = "batches/final_batch_012_da_viz/scenario_asset_registry.json"

with open(path) as f:
    data = json.load(f)

# --- Fix 1: deduplicate '19' in scen.da_viz_delivery glossary_example_vocab ---
for scen in data["scenarios"]:
    if scen["scenario_id"] == "scen.da_viz_delivery":
        vocab = scen["glossary_example_vocab"]
        seen = []
        deduped = []
        for item in vocab:
            if item not in seen:
                seen.append(item)
                deduped.append(item)
        before = len(vocab)
        scen["glossary_example_vocab"] = deduped
        after = len(deduped)
        print(f"glossary_example_vocab: {before} -> {after} entries (removed duplicate '19')")
        break

# --- Fix 2: set variant_kind to "messy" on ds.orders.messy ---
for asset in data["assets"]:
    if asset["asset_id"] == "ds.orders":
        for variant in asset.get("variants", []):
            if variant.get("variant_id") == "ds.orders.messy":
                old = variant.get("variant_kind")
                variant["variant_kind"] = "messy"
                print(f"ds.orders.messy variant_kind: {old!r} -> 'messy'")
                break
        break

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Patch applied.")
