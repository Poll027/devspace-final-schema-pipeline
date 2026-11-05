import json

path = "batches/final_batch_010_da_stats_capstone/interactions.part.c2.json"

with open(path) as f:
    data = json.load(f)

# Find tile_capstone_integrate_tools_model, step s11
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_capstone_integrate_tools_model":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_capstone_integrate_tools_model.s11":
                interaction = item["interaction"]
                anchors = interaction.get("anchors", [])
                print("Before:", anchors)
                # Remove the #practice anchor since this formula_entry only covers
                # COUNTIFS, not the full practice anchor (which requires both
                # PivotTable building AND COUNTIFS). s10's conceptual check
                # partially covers the PivotTable knowledge.
                new_anchors = [a for a in anchors if not a.endswith("#practice")]
                interaction["anchors"] = new_anchors
                print("After:", new_anchors)

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
