"""
Repair-round patch for screens.part.c1.json
Addresses two ADVISORY findings:

1. tile_viz_bar_histograms/s07 — after code uses bins=10 (default); change to bins=20.
2. tile_viz_line_scatter_box/s09 — img.boxplot_anatomy is MISSING from the registry;
   replace the annotated_image block with a diagram block (layers kind) that conveys
   the same box-plot anatomy without requiring an external image asset.
"""
import json, copy

path = "batches/final_batch_012_da_viz/screens.part.c1.json"
with open(path) as f:
    data = json.load(f)

# ── helpers ──────────────────────────────────────────────────────────────────

def find_tile(tid):
    for t in data["tiles"]:
        if t["tile_id"] == tid:
            return t
    raise KeyError(tid)

def find_step(tile, sid):
    for s in tile["steps"]:
        if s["step_id"] == sid:
            return s
    raise KeyError(sid)

def find_block(step, bid):
    for b in step.get("blocks", []):
        if b.get("block_id") == bid:
            return b
    raise KeyError(bid)

# ── FIX 1: tile_viz_bar_histograms/s07 — bins=10 → bins=20 ──────────────────
tile_bar = find_tile("tile_viz_bar_histograms")
s07 = find_step(tile_bar, "tile_viz_bar_histograms.s07")

# The before_after block is b05; its "after" sub-block has block_id ending in .after
for block in s07.get("blocks", []):
    if block.get("type") == "before_after":
        after = block.get("after", {})
        if "bins=10" in after.get("code", ""):
            after["code"] = after["code"].replace("bins=10", "bins=20")
            # Update annotation text to reflect the non-default value
            for ann in after.get("annotations", []):
                if "bins" in ann.get("text", "").lower() or "distribution" in ann.get("text", "").lower():
                    # Keep annotation text neutral — just update if it mentions bins=10
                    ann["text"] = ann["text"].replace("bins=10", "bins=20")
        # Also update change_summary if it mentions bins=10
        if "bins=10" in block.get("change_summary", ""):
            block["change_summary"] = block["change_summary"].replace("bins=10", "bins=20")
        break

print("FIX 1 applied: bins=10 → bins=20 in tile_viz_bar_histograms/s07 after code")

# ── FIX 2: tile_viz_line_scatter_box/s09 — replace annotated_image with diagram ──
# img.boxplot_anatomy is not registered; replace with a layers diagram that
# labels the same anatomical parts (lower whisker, Q1, median, Q3, upper whisker,
# flier point) so the step's pedagogical content is preserved without a missing asset.

tile_lsb = find_tile("tile_viz_line_scatter_box")
s09 = find_step(tile_lsb, "tile_viz_line_scatter_box.s09")

# Find and replace the annotated_image block
blocks = s09.get("blocks", [])
for i, block in enumerate(blocks):
    if block.get("type") == "annotated_image" and block.get("asset_id") == "img.boxplot_anatomy":
        diagram_block = {
            "type": "diagram",
            "block_id": "tile_viz_line_scatter_box.s09.b02",
            "diagram_kind": "layers",
            "title": "Box Plot Anatomy",
            "nodes": [
                {
                    "id": "flier_top",
                    "label": "Flier point (outlier)",
                    "kind": "outlier",
                    "group": "outlier"
                },
                {
                    "id": "upper_whisker",
                    "label": "Upper whisker — farthest point within 1.5\u00d7IQR above Q3",
                    "kind": "whisker",
                    "group": "whisker"
                },
                {
                    "id": "q3",
                    "label": "Q3 (third quartile) — top edge of box",
                    "kind": "quartile",
                    "group": "box"
                },
                {
                    "id": "median",
                    "label": "Median — line inside the box",
                    "kind": "median",
                    "group": "box"
                },
                {
                    "id": "q1",
                    "label": "Q1 (first quartile) — bottom edge of box",
                    "kind": "quartile",
                    "group": "box"
                },
                {
                    "id": "lower_whisker",
                    "label": "Lower whisker — farthest point within 1.5\u00d7IQR below Q1",
                    "kind": "whisker",
                    "group": "whisker"
                }
            ],
            "edges": [
                {"from": "flier_top",     "to": "upper_whisker", "directed": True},
                {"from": "upper_whisker", "to": "q3",            "directed": True},
                {"from": "q3",            "to": "median",        "directed": True},
                {"from": "median",        "to": "q1",            "directed": True},
                {"from": "q1",            "to": "lower_whisker", "directed": True}
            ],
            "alt_text": "A layered diagram of box plot anatomy from top to bottom: flier point (outlier) above the upper whisker; upper whisker reaching to the farthest in-range point above Q3; Q3 at the top of the box; median as a line inside the box; Q1 at the bottom of the box; lower whisker reaching to the farthest in-range point below Q1.",
            "lineage": {
                "concept_ids": ["viz.box_plots"],
                "teaching_block_ids": ["viz.box_plots#tb1"],
                "fact_ids": ["viz.box_plots#f3"],
                "anchors": ["viz.box_plots#visual"]
            }
        }
        blocks[i] = diagram_block
        print(f"FIX 2 applied: replaced annotated_image (img.boxplot_anatomy) with diagram block at index {i}")
        break

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch written to", path)
