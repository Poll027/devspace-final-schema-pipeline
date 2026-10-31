#!/usr/bin/env python3
"""Sync interactions.part.c3.json changes into interactions.json."""
import json

with open("batches/final_batch_006_da_sql_rest/interactions.json") as f:
    ix_all = json.load(f)

with open("batches/final_batch_006_da_sql_rest/interactions.part.c3.json") as f:
    ix_c3 = json.load(f)

# Build lookup from c3
c3_by_step = {}
for tile in ix_c3["tiles"]:
    for entry in tile["interactions"]:
        c3_by_step[entry["step_id"]] = entry["interaction"]

# Update interactions.json
updated = 0
for tile in ix_all["tiles"]:
    for entry in tile["interactions"]:
        sid = entry["step_id"]
        if sid in c3_by_step:
            entry["interaction"] = c3_by_step[sid]
            updated += 1

print(f"Updated {updated} interactions in interactions.json")

with open("batches/final_batch_006_da_sql_rest/interactions.json", "w") as f:
    json.dump(ix_all, f, indent=2)
print("Wrote interactions.json")

# Verify key changes
for tile in ix_all["tiles"]:
    if tile["tile_id"] == "tile_sql_adv_joining_tables":
        for entry in tile["interactions"]:
            if entry["step_id"] == "tile_sql_adv_joining_tables.s07":
                ix = entry["interaction"]
                for opt in ix["public"]["options"]:
                    if opt["option_id"] == "opt_d":
                        print("s07 opt_d:", opt["text"])
