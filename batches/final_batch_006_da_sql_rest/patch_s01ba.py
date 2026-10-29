"""
Patch: s01.ba before table — add max_rows:10 to asset_ref (excludes NULL rows 1011,1012)
and remove the highlight for row 1013 (no longer displayed).
This is a pure deletion/limiting fix; no new claims are added.
"""
import json, copy

path = "batches/final_batch_006_da_sql_rest/screens.part.c0_canary.json"

with open(path) as f:
    data = json.load(f)

tile = data["tiles"][0]
assert tile["tile_id"] == "tile_sql_fund_filtering_rows"

patched = False
for step in tile["steps"]:
    if step["step_id"] != "tile_sql_fund_filtering_rows.s01":
        continue
    for block in step["blocks"]:
        if block.get("block_id") != "tile_sql_fund_filtering_rows.s01.ba":
            continue
        before = block["before"]
        # 1. Add max_rows to asset_ref so only rows 1001-1010 are shown (no NULLs)
        assert "asset_ref" in before, "Expected asset_ref on before table"
        before["asset_ref"]["max_rows"] = 10
        # 2. Remove the highlight for row 1013 (now outside the displayed window)
        before["highlight"] = [
            h for h in before.get("highlight", [])
            if not (
                h.get("target", {}).get("kind") == "row"
                and h.get("target", {}).get("row", {}).get("where", {}).get("order_id") == 1013
            )
        ]
        patched = True
        break
    if patched:
        break

assert patched, "Did not find the target block — check step/block ids"

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied. max_rows=10 set; 1013 highlight removed.")
print("Remaining highlights:", [
    h["target"]["row"]["where"]["order_id"]
    for step in tile["steps"]
    if step["step_id"] == "tile_sql_fund_filtering_rows.s01"
    for block in step["blocks"]
    if block.get("block_id") == "tile_sql_fund_filtering_rows.s01.ba"
    for h in block["before"].get("highlight", [])
])
