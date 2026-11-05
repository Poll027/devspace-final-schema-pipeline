import json, sys

path = "batches/final_batch_012_da_viz/interactions.part.c0_canary.json"

with open(path) as f:
    data = json.load(f)

# Locate the s12 interaction
tile = data["tiles"][0]
s12 = None
for item in tile["interactions"]:
    if item["step_id"] == "tile_viz_figures_layout_plotting.s12":
        s12 = item
        break

assert s12 is not None, "s12 not found"

tests = s12["interaction"]["grading"]["tests"]

# Verify t03 is not already present
ids = [t["test_id"] for t in tests]
assert "ix.tile_viz_figures_layout_plotting.s12.t03" not in ids, "t03 already exists"

# Find position of t02 to insert t03 right after it
t02_idx = next(i for i, t in enumerate(tests) if t["test_id"] == "ix.tile_viz_figures_layout_plotting.s12.t02")

t03 = {
    "test_id": "ix.tile_viz_figures_layout_plotting.s12.t03",
    "kind": "plotted_data_equals",
    "spec": {
        "chart": "line",
        "field": "x",
        "expected": [0, 1, 2, 3, 4],
        "series": 0,
        "axes": 0
    },
    "visible": True,
    "message_on_fail": "The first line's x-values should be auto-generated starting from 0. Call `plt.plot(delivery_times)` with only one argument."
}

tests.insert(t02_idx + 1, t03)

# Verify order: t01, t02, t03, t04, t05
new_ids = [t["test_id"] for t in tests]
print("Test order after patch:", new_ids)

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Patch applied successfully.")
