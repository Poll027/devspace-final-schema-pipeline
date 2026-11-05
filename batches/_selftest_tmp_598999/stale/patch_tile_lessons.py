"""Patch tile_lessons files to match the screens.json fixes.

Fix 1: tile_pandas_text_dupes_missing.s05 data_table occurrence:1 matches nothing
  -> add variant_id: "orders_messy" to the before data_table asset_ref

Fix 2: tile_pandas_text_dupes_missing.s12 lineage.teaching_block_ids != planned
  -> remove pandas.drop_duplicates#tb3 from step lineage and prose block lineage
  -> also remove pandas.drop_duplicates#f1 and #f2 from step lineage fact_ids

Fix 3: tile_pandas_descriptive_stats.s01 must contain annotated_image or diagram block
  -> replace code_walkthrough block (b4) with a diagram block
"""
import json

# ── Fix tile_pandas_text_dupes_missing ──────────────────────────────────────
with open("batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_text_dupes_missing.json") as f:
    lesson = json.load(f)

for step in lesson["steps"]:
    # Fix 1: s05 data_table
    if step["step_id"] == "tile_pandas_text_dupes_missing.s05":
        for block in step.get("blocks", []):
            if block["type"] == "before_after":
                before = block["before"]
                if before.get("type") == "data_table":
                    before["asset_ref"]["variant_id"] = "orders_messy"

    # Fix 2: s12 lineage
    if step["step_id"] == "tile_pandas_text_dupes_missing.s12":
        lin = step.get("lineage", {})
        tbs = lin.get("teaching_block_ids", [])
        lin["teaching_block_ids"] = [
            tb for tb in tbs if tb != "pandas.drop_duplicates#tb3"
        ]
        fids = lin.get("fact_ids", [])
        lin["fact_ids"] = [
            f for f in fids
            if f not in ("pandas.drop_duplicates#f1", "pandas.drop_duplicates#f2")
        ]
        for block in step.get("blocks", []):
            if block.get("type") == "prose":
                blin = block.get("lineage", {})
                btbs = blin.get("teaching_block_ids", [])
                blin["teaching_block_ids"] = [
                    tb for tb in btbs if tb != "pandas.drop_duplicates#tb3"
                ]
                bfids = blin.get("fact_ids", [])
                blin["fact_ids"] = [
                    f for f in bfids
                    if f not in ("pandas.drop_duplicates#f1", "pandas.drop_duplicates#f2")
                ]

with open("batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_text_dupes_missing.json", "w") as f:
    json.dump(lesson, f, indent=2)
print("Patched: tile_pandas_text_dupes_missing.json")

# ── Fix tile_pandas_descriptive_stats ───────────────────────────────────────
with open("batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_descriptive_stats.json") as f:
    lesson2 = json.load(f)

for step in lesson2["steps"]:
    if step["step_id"] == "tile_pandas_descriptive_stats.s01":
        blocks = step.get("blocks", [])
        new_blocks = []
        for block in blocks:
            if block.get("block_id") == "tile_pandas_descriptive_stats.s01.b4":
                diagram = {
                    "type": "diagram",
                    "block_id": "tile_pandas_descriptive_stats.s01.b4",
                    "diagram_kind": "mapping",
                    "title": "describe() output vs single-method results for delivery_time_minutes",
                    "nodes": [
                        {"id": "desc_count",  "label": "count  14.0",              "kind": "describe_row"},
                        {"id": "desc_mean",   "label": "mean   29.0  \u2190 .mean()",  "kind": "describe_row", "group": "labelled"},
                        {"id": "desc_std",    "label": "std    15.6  \u2190 .std()",   "kind": "describe_row", "group": "labelled"},
                        {"id": "desc_min",    "label": "min    18.0  \u2190 .min()",   "kind": "describe_row", "group": "labelled"},
                        {"id": "desc_25",     "label": "25%    21.25",              "kind": "describe_row"},
                        {"id": "desc_50",     "label": "50%    25.0  \u2190 .median()","kind": "describe_row", "group": "labelled"},
                        {"id": "desc_75",     "label": "75%    30.25",              "kind": "describe_row"},
                        {"id": "desc_max",    "label": "max    80.0  \u2190 .max()",   "kind": "describe_row", "group": "labelled"},
                        {"id": "method_mean",   "label": ".mean() \u2192 29.0",   "kind": "single_method"},
                        {"id": "method_std",    "label": ".std()  \u2192 15.6",   "kind": "single_method"},
                        {"id": "method_median", "label": ".median() \u2192 25.0", "kind": "single_method"},
                        {"id": "method_min",    "label": ".min() \u2192 18",      "kind": "single_method"},
                        {"id": "method_max",    "label": ".max() \u2192 80",      "kind": "single_method"}
                    ],
                    "edges": [
                        {"from": "desc_mean", "to": "method_mean",   "label": "same value"},
                        {"from": "desc_std",  "to": "method_std",    "label": "same value"},
                        {"from": "desc_50",   "to": "method_median", "label": "same value"},
                        {"from": "desc_min",  "to": "method_min",    "label": "same value"},
                        {"from": "desc_max",  "to": "method_max",    "label": "same value"}
                    ],
                    "alt_text": (
                        "Side-by-side comparison of describe() output and single-method results "
                        "for delivery_time_minutes. The describe() rows mean=29.0, std=15.6, "
                        "50%=25.0 (median), min=18, and max=80 are each connected by arrows to "
                        "the matching single-method call (.mean(), .std(), .median(), .min(), .max()) "
                        "showing they return the same value."
                    ),
                    "lineage": {
                        "concept_ids": ["stats.pandas_descriptive_stats"],
                        "teaching_block_ids": [
                            "stats.pandas_descriptive_stats#tb2",
                            "stats.pandas_descriptive_stats#tb3"
                        ],
                        "fact_ids": [
                            "stats.pandas_descriptive_stats#f1",
                            "stats.pandas_descriptive_stats#f2"
                        ],
                        "anchors": ["stats.pandas_descriptive_stats#visual"]
                    }
                }
                new_blocks.append(diagram)
            else:
                new_blocks.append(block)
        step["blocks"] = new_blocks

with open("batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_descriptive_stats.json", "w") as f:
    json.dump(lesson2, f, indent=2)
print("Patched: tile_pandas_descriptive_stats.json")

print("Done.")
