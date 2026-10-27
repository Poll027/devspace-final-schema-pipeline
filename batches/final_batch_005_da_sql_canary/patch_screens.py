#!/usr/bin/env python3
"""Patch screens.json per repair-round findings."""
import json, copy

path = "batches/final_batch_005_da_sql_canary/screens.json"

with open(path) as f:
    data = json.load(f)

# Helper: find a tile by id
def get_tile(tile_id):
    for t in data["tiles"]:
        if t["tile_id"] == tile_id:
            return t
    raise KeyError(tile_id)

# Helper: find a step (regular or remediation) by step_id
def get_step(tile, step_id):
    for s in tile.get("steps", []):
        if s["step_id"] == step_id:
            return s
    for s in tile.get("remediation_steps", []):
        if s["step_id"] == step_id:
            return s
    raise KeyError(step_id)

# Helper: find a block by block_id within a step
def get_block(step, block_id):
    for b in step.get("blocks", []):
        if b.get("block_id") == block_id:
            return b
    raise KeyError(block_id)

# ── BLOCKING FIX ──────────────────────────────────────────────────────────────
# tile_sql_fund_alias_distinct/r03.b1:
#   "three distinct cities" → "four distinct cities"
tile_alias = get_tile("tile_sql_fund_alias_distinct")
step_r03 = get_step(tile_alias, "tile_sql_fund_alias_distinct.r03")
block_r03_b1 = get_block(step_r03, "tile_sql_fund_alias_distinct.r03.b1")

old_text = block_r03_b1["text"]
assert "three distinct cities" in old_text, f"Expected phrase not found: {old_text!r}"
block_r03_b1["text"] = old_text.replace("three distinct cities", "four distinct cities", 1)
print("BLOCKING fix applied: r03.b1 text updated.")

# ── ADVISORY FIX 1 ───────────────────────────────────────────────────────────
# tile_sql_fund_alias_distinct/s08 lineage:
#   Add sql.distinct#f1, sql.distinct#f2, sql.aliasing#f2 to block b1 lineage
#   and to the step-level lineage.
step_s08 = get_step(tile_alias, "tile_sql_fund_alias_distinct.s08")
block_s08_b1 = get_block(step_s08, "tile_sql_fund_alias_distinct.s08.b1")

missing_facts = ["sql.distinct#f1", "sql.distinct#f2", "sql.aliasing#f2"]

# Block lineage
b_facts = block_s08_b1["lineage"]["fact_ids"]
for fid in missing_facts:
    if fid not in b_facts:
        b_facts.append(fid)

# Step lineage
s_facts = step_s08["lineage"]["fact_ids"]
for fid in missing_facts:
    if fid not in s_facts:
        s_facts.append(fid)

print("ADVISORY fix 1 applied: s08 lineage updated with missing fact_ids.")

# ── ADVISORY FIX 2 ───────────────────────────────────────────────────────────
# tile_sql_fund_relational_select/s01.b1 lineage:
#   Add sql.relational_model#f5 to block lineage
tile_rel = get_tile("tile_sql_fund_relational_select")
step_s01 = get_step(tile_rel, "tile_sql_fund_relational_select.s01")
block_s01_b1 = get_block(step_s01, "tile_sql_fund_relational_select.s01.b1")

b1_facts = block_s01_b1["lineage"]["fact_ids"]
if "sql.relational_model#f5" not in b1_facts:
    b1_facts.append("sql.relational_model#f5")

print("ADVISORY fix 2 applied: s01.b1 lineage updated with sql.relational_model#f5.")

# ── WRITE ─────────────────────────────────────────────────────────────────────
with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done — screens.json written.")
