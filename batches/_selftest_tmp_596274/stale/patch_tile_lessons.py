"""Patch tile_lessons/*.json for the two gate failures."""
import json

# ── Fix tile_viz_line_scatter_box.json (s15) ────────────────────────────────
with open("batches/final_batch_012_da_viz/tile_lessons/tile_viz_line_scatter_box.json") as f:
    tile = json.load(f)

for step in tile["steps"]:
    if step["step_id"] == "tile_viz_line_scatter_box.s15":
        ix = step["interaction"]
        # Fix prompt
        ix["public"]["prompt"] = ix["public"]["prompt"].replace(
            "tick_labels=['Lagos', 'Abuja', 'Kano']",
            "labels=['Lagos', 'Abuja', 'Kano']"
        )
        # Fix starter
        for wf in ix["public"]["workspace"]["files"]:
            wf["content"] = wf["content"].replace(
                "tick_labels=[...]",
                "labels=[...]"
            ).replace(
                "# Call plt.boxplot() with a list of the three arrays and tick_labels for each city",
                "# Call plt.boxplot() with a list of the three arrays and labels for each city"
            )
        # Fix allowed_syntax
        cons = ix["public"]["constraints"]
        cons["allowed_syntax"] = [
            "labels=[...]" if d == "tick_labels=[...]" else d
            for d in cons["allowed_syntax"]
        ]
        # Add string literal descriptor
        if "single- or double-quoted strings" not in cons["allowed_syntax"]:
            cons["allowed_syntax"].append("single- or double-quoted strings")
        # Fix solution
        for sf in ix["grading"]["solution_files"]:
            sf["content"] = sf["content"].replace(
                "tick_labels=",
                "labels="
            )
        # Fix test messages
        for t in ix["grading"]["tests"]:
            if "message_on_fail" in t:
                t["message_on_fail"] = t["message_on_fail"].replace(
                    "tick_labels=['Lagos', 'Abuja', 'Kano']",
                    "labels=['Lagos', 'Abuja', 'Kano']"
                )
        print("Fixed s15 in tile_viz_line_scatter_box.json")

with open("batches/final_batch_012_da_viz/tile_lessons/tile_viz_line_scatter_box.json", "w") as f:
    json.dump(tile, f, indent=2)
    f.write("\n")

# ── Fix tile_viz_bar_histograms.json (s06) ──────────────────────────────────
with open("batches/final_batch_012_da_viz/tile_lessons/tile_viz_bar_histograms.json") as f:
    tile = json.load(f)

for step in tile["steps"]:
    if step["step_id"] == "tile_viz_bar_histograms.s06":
        ix = step["interaction"]
        cons = ix["public"]["constraints"]
        allowed = cons["allowed_syntax"]
        # Add descriptors that cover attr_module and idx
        if "module.name" not in allowed:
            allowed.append("module.name")
        if "df['col']" not in allowed:
            allowed.append("df['col']")
        cons["allowed_syntax"] = allowed
        print("Fixed s06 in tile_viz_bar_histograms.json")

with open("batches/final_batch_012_da_viz/tile_lessons/tile_viz_bar_histograms.json", "w") as f:
    json.dump(tile, f, indent=2)
    f.write("\n")

print("Done.")
