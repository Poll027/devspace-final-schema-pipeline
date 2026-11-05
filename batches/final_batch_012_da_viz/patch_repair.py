import json, copy

path = "batches/final_batch_012_da_viz/screens.part.c0_canary.json"
with open(path) as f:
    data = json.load(f)

tile = data["tiles"][0]
steps = tile["steps"]

# Helper: find step by id
def find_step(sid):
    for s in steps:
        if s["step_id"] == sid:
            return s
    return None

# Helper: find block by id within a step
def find_block(step, bid):
    for b in step.get("blocks", []):
        if b.get("block_id") == bid:
            return b
    return None

# ── ADVISORY 1: s09/intro (b01) ──────────────────────────────────────────────
# Remove viz.pyplot_basic_plotting#f1 and #f2 from the intro block's fact_ids.
# The intro only previews the two forms; the dedicated syntax blocks (b02, b03)
# carry those fact tags.
s09 = find_step("tile_viz_figures_layout_plotting.s09")
b01 = find_block(s09, "tile_viz_figures_layout_plotting.s09.b01")
b01["lineage"]["fact_ids"] = []   # intro previews only; facts belong to syntax blocks

# ── ADVISORY 2: s06/annotation ───────────────────────────────────────────────
# Reword the code_walkthrough annotation for tight_layout from the
# "fix overlapping labels" framing to neutral wording.
s06 = find_step("tile_viz_figures_layout_plotting.s06")
for block in s06.get("blocks", []):
    if block.get("type") == "code_walkthrough":
        for ann in block.get("annotations", []):
            if "labels and titles fit without clipping" in ann.get("text", ""):
                ann["text"] = "fig.tight_layout() adjusts spacing so subplot contents fit within the figure area"

# ── ADVISORY 3: s13/recap (b01) ──────────────────────────────────────────────
# B.f1–B.f3 (viz.figure_size_layout#f1–f3) are tagged under A:tb5
# (viz.matplotlib_figure_axes#tb5) only. Add viz.figure_size_layout teaching
# block ids so the B facts are covered by a B teaching block.
s13 = find_step("tile_viz_figures_layout_plotting.s13")
b01_s13 = find_block(s13, "tile_viz_figures_layout_plotting.s13.b01")

# Block-level: add figure_size_layout teaching blocks alongside matplotlib#tb5
existing_tbs = b01_s13["lineage"]["teaching_block_ids"]
for tb in ["viz.figure_size_layout#tb1", "viz.figure_size_layout#tb2"]:
    if tb not in existing_tbs:
        existing_tbs.append(tb)

# Step-level lineage: same addition
step_tbs = s13["lineage"]["teaching_block_ids"]
for tb in ["viz.figure_size_layout#tb1", "viz.figure_size_layout#tb2"]:
    if tb not in step_tbs:
        step_tbs.append(tb)

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
