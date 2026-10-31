"""
Update interactions.json with the fix from interactions.part.c2.json for s06,
then re-run assemble_tiles.py to regenerate tile_lessons.
"""
import json

# Update interactions.json with the fixed s06 from interactions.part.c2.json
with open("batches/final_batch_006_da_sql_rest/interactions.json") as f:
    ix_all = json.load(f)

with open("batches/final_batch_006_da_sql_rest/interactions.part.c2.json") as f:
    ix_c2 = json.load(f)

# Build lookup from c2
c2_by_step = {}
for tile in ix_c2["tiles"]:
    for entry in tile["interactions"]:
        c2_by_step[entry["step_id"]] = entry["interaction"]

# Update interactions.json
updated = 0
for tile in ix_all["tiles"]:
    for entry in tile["interactions"]:
        sid = entry["step_id"]
        if sid in c2_by_step:
            entry["interaction"] = c2_by_step[sid]
            updated += 1

print(f"Updated {updated} interactions in interactions.json")

with open("batches/final_batch_006_da_sql_rest/interactions.json", "w") as f:
    json.dump(ix_all, f, indent=2)
print("Wrote interactions.json")

# Verify s06 fix
for tile in ix_all["tiles"]:
    if tile["tile_id"] == "tile_sql_text_dates_casts":
        for entry in tile["interactions"]:
            if entry["step_id"] == "tile_sql_text_dates_casts.s06":
                sol = entry["interaction"]["grading"]["solution_files"][0]["content"]
                print("s06 solution:", repr(sol[:80]))
                break
        break
