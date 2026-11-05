"""
Patch screens.part.c3.json for ADVISORY tile_pandas_groupby_melt/s06:
- ds_monthly_long has 9 proper city-month rows (3 cities × 3 months = 9),
  so max_rows in the after data_table should be 9 (not 8).
- change_summary should say "9 rows" (not "8 rows").
"""
import json

path = "batches/final_batch_009_da_pandas/screens.part.c3.json"

with open(path) as f:
    data = json.load(f)

# Find tile_pandas_groupby_melt
tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_pandas_groupby_melt")

# Find step s06
step = next(s for s in tile["steps"] if s["step_id"] == "tile_pandas_groupby_melt.s06")

# Find block b4 (before_after)
block = next(b for b in step["blocks"] if b["block_id"] == "tile_pandas_groupby_melt.s06.b4")

# Fix 1: max_rows in the after data_table
assert block["after"]["asset_ref"]["asset_id"] == "ds_monthly_long"
old_max = block["after"]["asset_ref"]["max_rows"]
assert old_max == 8, f"Expected 8, got {old_max}"
block["after"]["asset_ref"]["max_rows"] = 9
print(f"Fixed max_rows: {old_max} -> 9")

# Fix 2: change_summary
old_summary = block["change_summary"]
assert "8 rows" in old_summary, f"Expected '8 rows' in change_summary, got: {old_summary}"
block["change_summary"] = old_summary.replace("8 rows", "9 rows")
print(f"Fixed change_summary: '{old_summary}' -> '{block['change_summary']}'")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
