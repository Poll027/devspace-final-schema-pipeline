import json, copy

path = "batches/final_batch_005_da_sql_canary/screens.json"
with open(path) as f:
    data = json.load(f)

tiles = {t["tile_id"]: t for t in data["tiles"]}

# ── Fix 1: tile_sql_fund_relational_select / s01.b01 ─────────────────────────
# Remove the near-verbatim trailing sentence.
tile_rs = tiles["tile_sql_fund_relational_select"]
steps_rs = {s["step_id"]: s for s in tile_rs["steps"]}
s01 = steps_rs["tile_sql_fund_relational_select.s01"]
b01 = next(b for b in s01["blocks"] if b["block_id"] == "tile_sql_fund_relational_select.s01.b01")

old_text = b01["text"]
# Remove the redundant final sentence
new_text = (
    "Greenleaf Online Shop stores its data in a relational database. "
    "Instead of one big spreadsheet, the data lives in separate tables \u2014 "
    "a customers table, an orders table \u2014 each holding its own kind of data."
)
assert new_text != old_text, "Text unchanged — check source"
b01["text"] = new_text
print(f"s01.b01 text updated:\n  OLD: {old_text}\n  NEW: {new_text}\n")

# ── Fix 2: tile_sql_fund_alias_distinct / s08 ─────────────────────────────────
# Add sql.distinct#f1 and sql.distinct#f2 to:
#   (a) block s08.b01 lineage.fact_ids
#   (b) step s08 lineage.fact_ids
tile_ad = tiles["tile_sql_fund_alias_distinct"]
steps_ad = {s["step_id"]: s for s in tile_ad["steps"]}
s08 = steps_ad["tile_sql_fund_alias_distinct.s08"]

to_add = ["sql.distinct#f1", "sql.distinct#f2"]

# (a) block-level
b01_s08 = next(b for b in s08["blocks"] if b["block_id"] == "tile_sql_fund_alias_distinct.s08.b01")
for fid in to_add:
    if fid not in b01_s08["lineage"]["fact_ids"]:
        b01_s08["lineage"]["fact_ids"].append(fid)
        print(f"Added {fid} to s08.b01 block lineage.fact_ids")

# (b) step-level
for fid in to_add:
    if fid not in s08["lineage"]["fact_ids"]:
        s08["lineage"]["fact_ids"].append(fid)
        print(f"Added {fid} to s08 step lineage.fact_ids")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nPatch complete.")
