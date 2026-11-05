"""
Patch script for REPAIR ROUND – stage 01_scenario_assets
Changes:
  BLOCKING  – swap driver_id (col F, index 5) and order_date (col G, index 6)
              in asset_orders_clean columns list, all its rows, the messy
              variant rows, and asset_orders_location_combined columns + rows.
  ADVISORY  – remove the "COUNT and COUNTA differ" claim from asset_orders_clean
              description.
  ADVISORY  – note the D2:D51 / 20-row mismatch in asset_orders_clean description.
"""

import json, copy

PATH = "batches/final_batch_011_da_spreadsheet/scenario_asset_registry.json"

with open(PATH) as f:
    reg = json.load(f)

# ── helpers ──────────────────────────────────────────────────────────────────

def asset_by_id(aid):
    for a in reg["assets"]:
        if a["asset_id"] == aid:
            return a
    raise KeyError(aid)

def swap_cols(asset, idx_a, idx_b):
    """Swap column definitions and every row value at positions idx_a and idx_b."""
    cols = asset["columns"]
    cols[idx_a], cols[idx_b] = cols[idx_b], cols[idx_a]
    for row in asset["rows"]:
        row[idx_a], row[idx_b] = row[idx_b], row[idx_a]

def swap_variant_rows(asset, idx_a, idx_b):
    """Swap row values in every variant's ops set_cell and in variant rows lists."""
    for variant in asset.get("variants", []):
        # swap rows in the variant's own rows list (if present)
        for row in variant.get("rows", []):
            row[idx_a], row[idx_b] = row[idx_b], row[idx_a]
        # ops: set_cell column names don't need swapping (they reference by name)
        # but if any op references a column by index we'd need to fix it – they
        # don't here (they use column names), so nothing to do.

# ── BLOCKING fix: asset_orders_clean ─────────────────────────────────────────
# Current layout: index 5 = order_date, index 6 = driver_id
# Target layout:  index 5 = driver_id,  index 6 = order_date

clean = asset_by_id("asset_orders_clean")

# Verify current order before swapping
assert clean["columns"][5]["name"] == "order_date", \
    f"Expected order_date at index 5, got {clean['columns'][5]['name']}"
assert clean["columns"][6]["name"] == "driver_id", \
    f"Expected driver_id at index 6, got {clean['columns'][6]['name']}"

swap_cols(clean, 5, 6)
swap_variant_rows(clean, 5, 6)

# Verify after swap
assert clean["columns"][5]["name"] == "driver_id"
assert clean["columns"][6]["name"] == "order_date"

# ── BLOCKING fix: asset_orders_location_combined ──────────────────────────────
# Same layout issue: index 5 = order_date, index 6 = driver_id
loc = asset_by_id("asset_orders_location_combined")

assert loc["columns"][5]["name"] == "order_date", \
    f"Expected order_date at index 5, got {loc['columns'][5]['name']}"
assert loc["columns"][6]["name"] == "driver_id", \
    f"Expected driver_id at index 6, got {loc['columns'][6]['name']}"

swap_cols(loc, 5, 6)
swap_variant_rows(loc, 5, 6)

assert loc["columns"][5]["name"] == "driver_id"
assert loc["columns"][6]["name"] == "order_date"

# ── ADVISORY fix 1: remove "COUNT and COUNTA differ" claim ───────────────────
# Old: "… delivery_minutes is NULL for Pending/Cancelled rows so COUNT and COUNTA differ."
# New: remove that sentence; delivery_minutes has only integers and nulls so
#      COUNT (numeric) and COUNTA (non-empty) return the same count on this column.
old_desc = clean["description"]
clean["description"] = (
    "One row per delivery order. Used for formula syntax, aggregation, logical "
    "functions, conditional aggregation, lookups, sorting, filtering, tables, "
    "named ranges, pivot tables, and chart exercises. "
    "delivery_minutes is NULL for Pending/Cancelled rows (non-delivered orders "
    "have no recorded time). "
    "Note: teaching-block ranges such as D2:D51 span 50 rows; this dataset has "
    "20 rows — learners should adjust range references to D2:D21 in practice."
)

# ── write back ────────────────────────────────────────────────────────────────
with open(PATH, "w") as f:
    json.dump(reg, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
print(f"  asset_orders_clean columns[5]={clean['columns'][5]['name']}, "
      f"columns[6]={clean['columns'][6]['name']}")
print(f"  asset_orders_location_combined columns[5]={loc['columns'][5]['name']}, "
      f"columns[6]={loc['columns'][6]['name']}")
print(f"  description updated (old len={len(old_desc)}, new len={len(clean['description'])})")
