#!/usr/bin/env python3
"""
Patch screens.part.c2.json for REPAIR ROUND advisories:
  1. tile_datamodel_normalization_many_to_many/s01.b2:
     Restructure before_after → side_by_side so the left side shows
     an un-normalized table structure (diagram) and the right shows
     the normalized customers table (data_table). This demonstrates
     the actual redundancy problem rather than two already-normalized tables.
  2. tile_stakeholder_recommendation_translation/s02:
     Update lede to use registry-consistent Kano values (21 → 22.5 min,
     an increase) instead of hypothetical 28 → 19 min (a decrease).
"""
import json, copy

SRC = "batches/final_batch_003_da_chunk/screens.part.c2.json"

with open(SRC) as f:
    doc = json.load(f)

# ── Helper: find a step by step_id ──────────────────────────────────────────
def find_step(tiles, step_id):
    for tile in tiles:
        for step in tile.get("steps", []):
            if step["step_id"] == step_id:
                return step
        for step in tile.get("remediation_steps", []):
            if step["step_id"] == step_id:
                return step
    return None

# ── Helper: find a block by block_id within a step ──────────────────────────
def find_block(step, block_id):
    for i, blk in enumerate(step.get("blocks", [])):
        if blk.get("block_id") == block_id:
            return i, blk
    return None, None

# ════════════════════════════════════════════════════════════════════════════
# FIX 1: s01.b2 — restructure before_after → side_by_side
# Left: diagram showing un-normalized orders table (columns that repeat)
# Right: data_table for ds_customers (normalized, name+city stored once)
# ════════════════════════════════════════════════════════════════════════════
step_s01 = find_step(doc["tiles"], "tile_datamodel_normalization_many_to_many.s01")
assert step_s01 is not None, "step s01 not found"

idx, blk_b2 = find_block(step_s01, "tile_datamodel_normalization_many_to_many.s01.b2")
assert blk_b2 is not None, "block s01.b2 not found"
assert blk_b2["type"] == "before_after", f"unexpected type: {blk_b2['type']}"

# Preserve lineage from the original block
original_lineage = copy.deepcopy(blk_b2["lineage"])

new_b2 = {
    "type": "side_by_side",
    "block_id": "tile_datamodel_normalization_many_to_many.s01.b2",
    "left_label": "Un-normalized (redundant)",
    "right_label": "Normalized (split)",
    "left": {
        "type": "diagram",
        "diagram_kind": "container",
        "title": "orders_flat (un-normalized)",
        "nodes": [
            {
                "id": "col_order_id",
                "label": "order_id",
                "kind": "column"
            },
            {
                "id": "col_customer_name",
                "label": "customer_name  ← repeats per order",
                "kind": "column_bad"
            },
            {
                "id": "col_customer_city",
                "label": "customer_city  ← repeats per order",
                "kind": "column_bad"
            },
            {
                "id": "col_delivery_minutes",
                "label": "delivery_minutes",
                "kind": "column"
            }
        ],
        "alt_text": "A single flat orders table with columns order_id, customer_name, customer_city, delivery_minutes. customer_name and customer_city are marked as repeating on every order row — the un-normalized design that causes update anomalies."
    },
    "right": {
        "type": "data_table",
        "asset_ref": {
            "asset_id": "ds_customers",
            "variant_id": None,
            "columns": [
                "customer_id",
                "name",
                "city"
            ]
        },
        "caption": "customers table — name and city stored once; orders link back via customer_id",
        "tag_columns": [
            {
                "column": "customer_id",
                "tag": "primary key",
                "tone": "good"
            }
        ]
    },
    "takeaway": "Moving customer_name and customer_city into their own table stores each value exactly once. The orders table keeps only customer_id to link back — no more repeated values, no update anomaly.",
    "lineage": original_lineage
}

step_s01["blocks"][idx] = new_b2

# ════════════════════════════════════════════════════════════════════════════
# FIX 2: tile_stakeholder_recommendation_translation/s02 — update lede
# Registry: Kano avg_delivery_minutes month 1 = 21.0, month 2 = 22.5 (rose)
# Replace hypothetical "fell from 28 to 19 minutes" with registry values
# ════════════════════════════════════════════════════════════════════════════
step_s02 = find_step(doc["tiles"], "tile_stakeholder_recommendation_translation.s02")
assert step_s02 is not None, "step tile_stakeholder_recommendation_translation.s02 not found"

old_lede = step_s02["lede"]
assert "28 to 19" in old_lede, f"Expected '28 to 19' in lede, got: {old_lede!r}"

step_s02["lede"] = (
    "Which of the following best follows the 'because we found X, we recommend Y' pattern "
    "for a finding that average Kano delivery times rose from 21 to 22.5 minutes?"
)

print("Fix 1 applied: s01.b2 restructured from before_after to side_by_side")
print("Fix 2 applied: s02 lede updated from '28 to 19 minutes' to '21 to 22.5 minutes'")

with open(SRC, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Patch written successfully.")
