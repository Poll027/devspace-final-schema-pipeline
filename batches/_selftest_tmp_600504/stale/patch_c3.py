#!/usr/bin/env python3
"""Patch interactions.part.c3.json for the three repair-round findings."""
import json, copy

path = "batches/final_batch_009_da_pandas/interactions.part.c3.json"

with open(path) as f:
    data = json.load(f)

# ── helpers ──────────────────────────────────────────────────────────────────

def find_interaction(tiles, tile_id, step_id):
    for tile in tiles:
        if tile["tile_id"] == tile_id:
            for entry in tile["interactions"]:
                if entry["step_id"] == step_id:
                    return entry["interaction"]
    raise KeyError(f"{tile_id}/{step_id} not found")

tiles = data["tiles"]

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: tile_pandas_map_apply.s07 – measures capability must be
#         apply_function_down_columns (not apply_function_across_rows_with_axis_1)
#         so that the assessment anchor pandas.apply_transform#apply_function_down_columns
#         is covered.
# ─────────────────────────────────────────────────────────────────────────────
ix_s07 = find_interaction(tiles, "tile_pandas_map_apply", "tile_pandas_map_apply.s07")
for m in ix_s07["measures"]:
    if m["concept_id"] == "pandas.apply_transform" and m["capability"] == "apply_function_across_rows_with_axis_1":
        m["capability"] = "apply_function_down_columns"
        print("FIX 1 applied: s07 measures capability → apply_function_down_columns")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: tile_pandas_groupby_melt.s09 – allowed_syntax must be copied verbatim
#         from pandas.melt_reshaping practice anchor.
#         Glossary says: value_name='value'  (not value_name='deliveries')
# ─────────────────────────────────────────────────────────────────────────────
ix_s09 = find_interaction(tiles, "tile_pandas_groupby_melt", "tile_pandas_groupby_melt.s09")
allowed = ix_s09["public"]["constraints"]["allowed_syntax"]
new_allowed = []
changed = False
for item in allowed:
    if item == "value_name='deliveries'":
        new_allowed.append("value_name='value'")
        changed = True
    else:
        new_allowed.append(item)
ix_s09["public"]["constraints"]["allowed_syntax"] = new_allowed
if changed:
    print("FIX 2 applied: s09 allowed_syntax value_name='deliveries' → value_name='value'")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: tile_pandas_pivot_export.s08 – t4 must be data-dependent.
#         Old t4: "'Unnamed: 0' not in pd.read_csv('cleaned_orders.csv').columns"
#         → always True regardless of data changes.
#         New t4: check that the list of columns in the written CSV matches the
#         original DataFrame's columns (data-dependent: changes if a column is
#         added/removed from the source data).
# ─────────────────────────────────────────────────────────────────────────────
ix_s08 = find_interaction(tiles, "tile_pandas_pivot_export", "tile_pandas_pivot_export.s08")
tests = ix_s08["grading"]["tests"]
for t in tests:
    if t["test_id"] == "t4":
        t["kind"] = "value_equals"
        t["spec"] = {
            "expr": "list(pd.read_csv('cleaned_orders.csv').columns)",
            "expected": ["order_id", "city", "city_code", "courier", "driver_id",
                         "customer_id", "pickup_date", "delivery_time_minutes",
                         "distance_km", "order_value"]
        }
        t["visible"] = True
        t["message_on_fail"] = (
            "The CSV columns should match the original DataFrame columns exactly "
            "(no extra index column). Use index=False when calling to_csv()."
        )
        print("FIX 3 applied: s08 t4 replaced with data-dependent columns check")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done.")
