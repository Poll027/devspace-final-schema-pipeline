"""
Fix interactions.json:
1. Remove the spurious top-level 'constraints' key from s05 and s10
2. Add the missing allowed_syntax descriptors to public.constraints for s05 and s10
3. Sync interactions.json to match interactions.part.c0_canary.json
"""
import json

# Read the already-patched canary (source of truth)
canary_path = "batches/final_batch_009_da_pandas/interactions.part.c0_canary.json"
interactions_path = "batches/final_batch_009_da_pandas/interactions.json"

with open(canary_path) as f:
    canary = json.load(f)

with open(interactions_path) as f:
    interactions = json.load(f)

tile = interactions["tiles"][0]

for item in tile["interactions"]:
    sid = item["step_id"]
    ix = item["interaction"]

    if sid == "tile_pandas_dataframe_reading.s05":
        # Remove top-level constraints (schema violation)
        if "constraints" in ix:
            del ix["constraints"]
            print(f"s05: removed top-level 'constraints'")
        # Update public.constraints.allowed_syntax
        constraints = ix["public"]["constraints"]
        extra = [
            "{key: value} dictionary literal",
            "[...] list literal",
            "whole-number literals as in the examples",
            "single- or double-quoted strings",
        ]
        for d in extra:
            if d not in constraints["allowed_syntax"]:
                constraints["allowed_syntax"].append(d)
        print(f"s05 allowed_syntax: {constraints['allowed_syntax']}")

    elif sid == "tile_pandas_dataframe_reading.s10":
        # Remove top-level constraints (schema violation)
        if "constraints" in ix:
            del ix["constraints"]
            print(f"s10: removed top-level 'constraints'")
        # Update public.constraints.allowed_syntax
        constraints = ix["public"]["constraints"]
        d = "single- or double-quoted strings"
        if d not in constraints["allowed_syntax"]:
            constraints["allowed_syntax"].append(d)
        print(f"s10 allowed_syntax: {constraints['allowed_syntax']}")

with open(interactions_path, "w") as f:
    json.dump(interactions, f, indent=2, ensure_ascii=False)

print("interactions.json patched.")
