"""
Patch interactions.part.c1.json:
Fix remediation_step_id references in tile_sql_fund_sorting_limiting.
s01 and s04 are explainer steps, not remediation steps.
The actual remediation steps are r01 (for order_by) and r02 (for limit_offset).
"""
import json

path = "batches/final_batch_006_da_sql_rest/interactions.part.c1.json"

with open(path) as f:
    data = json.load(f)

fixes = {
    "tile_sql_fund_sorting_limiting.s01": "tile_sql_fund_sorting_limiting.r01",
    "tile_sql_fund_sorting_limiting.s04": "tile_sql_fund_sorting_limiting.r02",
}

changed = 0
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_fund_sorting_limiting":
        continue
    for ix_entry in tile["interactions"]:
        fb = ix_entry["interaction"].get("feedback", {})
        rid = fb.get("remediation_step_id")
        if rid in fixes:
            fb["remediation_step_id"] = fixes[rid]
            print(f"  {ix_entry['step_id']}: {rid} -> {fixes[rid]}")
            changed += 1

print(f"Total changes: {changed}")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done.")
