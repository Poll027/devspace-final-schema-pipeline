#!/usr/bin/env python3
"""Patch t4 in tile_pandas_pivot_export.s08 to be data-dependent."""
import json

path = "batches/final_batch_009_da_pandas/interactions.part.c3.json"

with open(path) as f:
    data = json.load(f)

tiles = data["tiles"]

for tile in tiles:
    if tile["tile_id"] == "tile_pandas_pivot_export":
        for entry in tile["interactions"]:
            if entry["step_id"] == "tile_pandas_pivot_export.s08":
                ix = entry["interaction"]
                tests = ix["grading"]["tests"]
                for t in tests:
                    if t["test_id"] == "t4":
                        # Replace with a data-dependent test: sum of order_value
                        # This changes when rows are added/removed/changed
                        t["kind"] = "value_equals"
                        t["spec"] = {
                            "expr": "int(pd.read_csv('cleaned_orders.csv')['order_value'].sum())",
                            "expected": 43200
                        }
                        t["visible"] = True
                        t["message_on_fail"] = (
                            "The total order_value in the exported CSV should be 43200. "
                            "Make sure you export the full DataFrame with to_csv()."
                        )
                        print("FIX t4: replaced with data-dependent sum of order_value")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done.")
