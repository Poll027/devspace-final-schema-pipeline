"""
Repair round 6: fix ix.tile_viz_figures_layout_plotting.s12.t03
The test checks auto-generated x-values [0,1,2,3,4] for series 0,
which are always constant regardless of data mutations (they are just
indices 0..len-1 for a fixed-length list). The gate rejects it as a
hard-coded answer.

Fix: replace t03 with a test that checks the NUMBER of data points
plotted in series 0 (i.e., the length of delivery_times), expressed
as a plotted_data_equals on field "y" for series 0 — but t02 already
does that. Instead, we change t03 to test field "x" for series 1
(the days-based line) — but t04 already does that too.

Cleanest valid fix: remove t03 entirely. The remaining tests cover:
  t01 - figure structure (1 axes, line chart type)
  t02 - series 0 y-values (delivery_times, changes with dt_1)
  t04 - series 1 x-values (days, changes with day_1)
  t05 - series 1 y-values (delivery_times, changes with dt_1)
All four remaining tests depend on starter variables that get mutated.
"""
import json, sys

path = "batches/final_batch_012_da_viz/interactions.part.c0_canary.json"

with open(path) as f:
    data = json.load(f)

# Find the s12 interaction
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_viz_figures_layout_plotting":
        for item in tile["interactions"]:
            if item["step_id"] == "tile_viz_figures_layout_plotting.s12":
                tests = item["interaction"]["grading"]["tests"]
                # Remove t03 (the constant auto-x test)
                before = len(tests)
                tests[:] = [t for t in tests if t["test_id"] != "ix.tile_viz_figures_layout_plotting.s12.t03"]
                after = len(tests)
                print(f"Removed {before - after} test(s). Tests remaining: {after}")
                for t in tests:
                    print(f"  {t['test_id']}")

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
