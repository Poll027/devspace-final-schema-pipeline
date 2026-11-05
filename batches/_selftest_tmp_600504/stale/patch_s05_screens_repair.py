#!/usr/bin/env python3
"""
Repair patch for screens.part.c3.json
Finding: tile_pandas_groupby_melt/s05 title/lede says "by city" and mentions
delivery times, but the exercise groups by customer_id and aggregates only
order_value. Fix: change title/lede to match the actual exercise content.
"""
import json

ARTIFACT = "batches/final_batch_009_da_pandas/screens.part.c3.json"

with open(ARTIFACT) as f:
    data = json.load(f)

patched = False
for tile in data.get("tiles", []):
    if tile.get("tile_id") != "tile_pandas_groupby_melt":
        continue
    for step in tile.get("steps", []):
        if step.get("step_id") != "tile_pandas_groupby_melt.s05":
            continue
        # Apply option (b): change title and lede to match the actual exercise
        # which groups by customer_id and aggregates order_value (sum and mean)
        old_title = step.get("title")
        old_lede = step.get("lede")
        step["title"] = "Aggregate order values by customer"
        step["lede"] = (
            "Use groupby to compute the sum and mean of order_value per customer "
            "from the SwiftDrop orders table."
        )
        print(f"Patched step: {step['step_id']}")
        print(f"  title: {old_title!r} -> {step['title']!r}")
        print(f"  lede:  {old_lede!r} -> {step['lede']!r}")
        patched = True
        break
    if patched:
        break

if not patched:
    raise RuntimeError("Step tile_pandas_groupby_melt.s05 not found — check artifact structure")

with open(ARTIFACT, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done. Artifact written.")
