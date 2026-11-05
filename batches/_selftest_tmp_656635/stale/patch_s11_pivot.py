#!/usr/bin/env python3
"""
Patch interactions.part.c2.json:
- Add build_pivot_table_with_correct_field_placement to s11 measures and anchors
  so the coverage check passes.
"""
import json

path = "batches/final_batch_010_da_stats_capstone/interactions.part.c2.json"

with open(path) as f:
    data = json.load(f)

for tile in data["tiles"]:
    if tile["tile_id"] != "tile_capstone_integrate_tools_model":
        continue
    for ix_entry in tile["interactions"]:
        if ix_entry["step_id"] != "tile_capstone_integrate_tools_model.s11":
            continue
        ix = ix_entry["interaction"]

        # 1. Add build_pivot_table_with_correct_field_placement to measures
        #    (f1 is the PivotTable fact per the glossary)
        existing_caps = {m["capability"] for m in ix["measures"]}
        if "build_pivot_table_with_correct_field_placement" not in existing_caps:
            ix["measures"].append({
                "concept_id": "capstone.integrate_spreadsheet",
                "capability": "build_pivot_table_with_correct_field_placement",
                "fact_ids": ["f1"]
            })

        # 2. Add the assessment anchor to anchors list
        pivot_anchor = "capstone.integrate_spreadsheet#assessment:build_pivot_table_with_correct_field_placement"
        if pivot_anchor not in ix["anchors"]:
            ix["anchors"].append(pivot_anchor)

        # 3. Fix apply_countifs fact_ids: COUNTIFS is f2, not f1
        for m in ix["measures"]:
            if m["capability"] == "apply_countifs_with_multiple_criteria_ranges":
                m["fact_ids"] = ["f2"]

        print("Patched s11:")
        print(json.dumps(ix_entry, indent=2))
        break

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
