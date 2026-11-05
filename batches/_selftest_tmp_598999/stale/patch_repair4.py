"""
Repair patch: add missing allowed_syntax descriptors for s05 and s10.

s05 solution uses dict_lit, list_lit, lit_int, lit_str — not covered by the
current allowed_syntax. Add the four descriptors that cover them.

s10 solution uses lit_str (the file_path string literal) — not covered.
Add 'single- or double-quoted strings'.
"""
import json

path = "batches/final_batch_009_da_pandas/interactions.part.c0_canary.json"

with open(path) as f:
    data = json.load(f)

tile = data["tiles"][0]  # tile_pandas_dataframe_reading

for item in tile["interactions"]:
    sid = item["step_id"]
    ix = item["interaction"]

    if sid == "tile_pandas_dataframe_reading.s05":
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
        print(f"s05 allowed_syntax now: {constraints['allowed_syntax']}")

    elif sid == "tile_pandas_dataframe_reading.s10":
        constraints = ix["public"]["constraints"]
        d = "single- or double-quoted strings"
        if d not in constraints["allowed_syntax"]:
            constraints["allowed_syntax"].append(d)
        print(f"s10 allowed_syntax now: {constraints['allowed_syntax']}")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied.")
