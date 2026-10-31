"""
Fix remediation_step_id references in tile_sql_adv_joining_tables.
s01, s06, s10, s11 are explainer steps, not remediation steps.
The actual remediation steps are:
  r01 -> sql.inner_join
  r02 -> sql.composite_join_conditions
  r03 -> sql.outer_joins
"""
import json

path = "batches/final_batch_006_da_sql_rest/interactions.part.c3.json"

with open(path) as f:
    data = json.load(f)

# Map wrong step ids to correct remediation step ids
fixes = {
    "tile_sql_adv_joining_tables.s01": "tile_sql_adv_joining_tables.r01",
    "tile_sql_adv_joining_tables.s06": "tile_sql_adv_joining_tables.r02",
    "tile_sql_adv_joining_tables.s10": "tile_sql_adv_joining_tables.r03",
    "tile_sql_adv_joining_tables.s11": "tile_sql_adv_joining_tables.r03",
}

changed = 0
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_adv_joining_tables":
        continue
    for ix in tile["interactions"]:
        fb = ix["interaction"].get("feedback", {})
        rid = fb.get("remediation_step_id")
        if rid in fixes:
            old = rid
            fb["remediation_step_id"] = fixes[rid]
            print(f"  {ix['step_id']}: {old} -> {fixes[old]}")
            changed += 1

print(f"Total changes: {changed}")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done.")
