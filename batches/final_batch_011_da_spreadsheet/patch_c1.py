#!/usr/bin/env python3
"""Patch screens.part.c1.json per repair-round findings."""
import json, copy, re

SRC = "batches/final_batch_011_da_spreadsheet/screens.part.c1.json"
DST = SRC

with open(SRC) as f:
    data = json.load(f)

def find_tile(tile_id):
    for t in data["tiles"]:
        if t["tile_id"] == tile_id:
            return t
    raise KeyError(tile_id)

def find_step(tile, step_id):
    for s in tile.get("steps", []) + tile.get("remediation_steps", []):
        if s["step_id"] == step_id:
            return s
    raise KeyError(step_id)

def find_block(step, block_id):
    for b in step.get("blocks", []):
        if b.get("block_id") == block_id:
            return b
        # nested blocks (before_after, side_by_side)
        for key in ("before", "after", "left", "right"):
            sub = b.get(key)
            if sub and sub.get("block_id") == block_id:
                return sub
    raise KeyError(block_id)

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1 (formula_syntax/s01):
#   Change "=SUM(D2:D51)" to "=SUM(D2:D21)" in prose block b3
# ─────────────────────────────────────────────────────────────────────────────
tile_fsr = find_tile("tile_spreadsheet_formula_syntax_refs")
step_s01 = find_step(tile_fsr, "tile_spreadsheet_formula_syntax_refs.s01")
b3 = find_block(step_s01, "tile_spreadsheet_formula_syntax_refs.s01.b3")
assert "D2:D51" in b3["text"], f"Expected D2:D51 in b3 text: {b3['text']}"
b3["text"] = b3["text"].replace("=SUM(D2:D51)", "=SUM(D2:D21)")
print("FIX 1 applied: D2:D51 → D2:D21 in formula_syntax s01.b3")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2 (aggregation_logical/s06):
#   Move IF formula cells from column D to column H in the spreadsheet_grid visual
# ─────────────────────────────────────────────────────────────────────────────
tile_agg = find_tile("tile_spreadsheet_aggregation_logical")
step_s06 = find_step(tile_agg, "tile_spreadsheet_aggregation_logical.s06")
b3_s06 = find_block(step_s06, "tile_spreadsheet_aggregation_logical.s06.b3")
assert b3_s06["type"] == "spreadsheet_grid"

# Update range to include column H
b3_s06["range"] = "C1:H5"

# Move cells from D2/D3/D4 → H2/H3/H4
for cell in b3_s06["cells"]:
    if cell["ref"] == "D2":
        cell["ref"] = "H2"
    elif cell["ref"] == "D3":
        cell["ref"] = "H3"
    elif cell["ref"] == "D4":
        cell["ref"] = "H4"

# Update annotations
for ann in b3_s06["annotations"]:
    if ann["target"] == "D2":
        ann["target"] = "H2"
        ann["text"] = "IF formula in formula bar"
    elif ann["target"] == "D1":
        ann["target"] = "H1"
        ann["text"] = "Status label column shows result"

print("FIX 2 applied: IF formula cells moved from column D to column H in s06.b3")

# Also update the prose text in b1 to reference a helper column instead of D
b1_s06 = find_block(step_s06, "tile_spreadsheet_aggregation_logical.s06.b1")
# The prose uses =IF(C2>60,"Late","On Time") — update to place result in H2
b1_s06["text"] = b1_s06["text"].replace(
    "=IF(C2>60,\"Late\",\"On Time\") labels each order row on your Orders sheet based on its delivery_minutes value.",
    "=IF(C2>60,\"Late\",\"On Time\") placed in a helper column (H) labels each order row based on its delivery_minutes value without overwriting the amount column."
)
print("FIX 2b applied: prose b1 updated to reference helper column H")

# Update b2 nested IF example — it references D2 which is the amount column; change to H2
b2_s06 = find_block(step_s06, "tile_spreadsheet_aggregation_logical.s06.b2")
b2_s06["text"] = b2_s06["text"].replace(
    "=IF(D2>89,\"A\",IF(D2>79,\"B\",IF(D2>69,\"C\",IF(D2>59,\"D\",\"F\")))) converts a numeric score to a letter grade. The same structure could sort orders into amount bands instead of a single Late/On-Time split.",
    "=IF(H2>89,\"A\",IF(H2>79,\"B\",IF(H2>69,\"C\",IF(H2>59,\"D\",\"F\")))) converts a numeric score to a letter grade. The same structure could sort orders into delivery-time bands in a helper column instead of a single Late/On-Time split."
)
print("FIX 2c applied: prose b2 updated to reference H2 instead of D2")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3 (aggregation_logical/s10):
#   Change step type from "hands_on" to "check"
# ─────────────────────────────────────────────────────────────────────────────
step_s10 = find_step(tile_agg, "tile_spreadsheet_aggregation_logical.s10")
assert step_s10["type"] == "hands_on", f"Expected hands_on, got {step_s10['type']}"
step_s10["type"] = "check"
print("FIX 3 applied: s10 type changed from hands_on to check")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4 (aggregation_logical/s01):
#   Add note that AVERAGE skips blanks and text but includes cells containing zero
# ─────────────────────────────────────────────────────────────────────────────
step_agg_s01 = find_step(tile_agg, "tile_spreadsheet_aggregation_logical.s01")
b1_agg_s01 = find_block(step_agg_s01, "tile_spreadsheet_aggregation_logical.s01.b1")
# Current text ends with "...skipping any blank cells (Pending or Cancelled orders have no recorded time)."
# Append the zero-value note
old_text = b1_agg_s01["text"]
assert "skipping any blank cells" in old_text, f"Unexpected text: {old_text}"
b1_agg_s01["text"] = old_text.replace(
    "skipping any blank cells (Pending or Cancelled orders have no recorded time).",
    "skipping blank cells and text but including any cell that contains zero (Pending or Cancelled orders with no recorded time are blank, not zero, so they are excluded)."
)
print("FIX 4 applied: AVERAGE zero-value note added to aggregation_logical s01.b1")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5 (text_date/s01):
#   Rephrase CONCATENATE/TEXTJOIN separator sentence in b2
# ─────────────────────────────────────────────────────────────────────────────
tile_tdc = find_tile("tile_spreadsheet_text_date_conditional_agg")
step_tdc_s01 = find_step(tile_tdc, "tile_spreadsheet_text_date_conditional_agg.s01")
b2_tdc_s01 = find_block(step_tdc_s01, "tile_spreadsheet_text_date_conditional_agg.s01.b2")
old_text = b2_tdc_s01["text"]
assert "Neither function adds a separator automatically" in old_text, f"Unexpected text: {old_text}"
b2_tdc_s01["text"] = old_text.replace(
    "Neither function adds a separator automatically \u2014 include it as a literal argument if you need one.",
    "CONCATENATE does not add a separator automatically \u2014 include it as a literal argument. TEXTJOIN uses its delimiter argument to insert one for you."
)
print("FIX 5 applied: CONCATENATE/TEXTJOIN separator sentence rephrased in tdc s01.b2")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6a (text_date/s04):
#   Rephrase TRIM description in prose b2
# ─────────────────────────────────────────────────────────────────────────────
step_tdc_s04 = find_step(tile_tdc, "tile_spreadsheet_text_date_conditional_agg.s04")
b2_tdc_s04 = find_block(step_tdc_s04, "tile_spreadsheet_text_date_conditional_agg.s04.b2")
old_text = b2_tdc_s04["text"]
assert "TRIM removes all leading and trailing spaces, keeping only single spaces between words" in old_text, f"Unexpected text: {old_text}"
b2_tdc_s04["text"] = old_text.replace(
    "TRIM removes all leading and trailing spaces, keeping only single spaces between words: TRIM(text).",
    "TRIM removes all extra spaces \u2014 leading, trailing, and multiple spaces between words \u2014 leaving only single spaces between words: TRIM(text)."
)
print("FIX 6a applied: TRIM description updated in tdc s04.b2")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6b (text_date/s04):
#   Change "LG-2045" to "LG-2001" everywhere in s04 blocks
# ─────────────────────────────────────────────────────────────────────────────
def replace_in_block(block, old, new):
    """Recursively replace old with new in all string values of a dict/list."""
    if isinstance(block, dict):
        for k, v in block.items():
            if isinstance(v, str):
                block[k] = v.replace(old, new)
            elif isinstance(v, (dict, list)):
                replace_in_block(v, old, new)
    elif isinstance(block, list):
        for i, item in enumerate(block):
            if isinstance(item, str):
                block[i] = item.replace(old, new)
            elif isinstance(item, (dict, list)):
                replace_in_block(item, old, new)

for block in step_tdc_s04.get("blocks", []):
    replace_in_block(block, "LG-2045", "LG-2001")
    replace_in_block(block, "2045", "2001")  # numeric suffix in notes/annotations

# Also fix the remediation step r02 which also references LG-2045
step_tdc_r02 = find_step(tile_tdc, "tile_spreadsheet_text_date_conditional_agg.r02")
for block in step_tdc_r02.get("blocks", []):
    replace_in_block(block, "LG-2045", "LG-2001")
    replace_in_block(block, "2045", "2001")

print("FIX 6b applied: LG-2045 → LG-2001 in tdc s04 blocks and r02")

# ─────────────────────────────────────────────────────────────────────────────
# NOTE: leakage_surface advisory — blocked_future_concepts is in the glossary
# bundle (an input), not in the screens artifact. No change possible here.
# ─────────────────────────────────────────────────────────────────────────────

with open(DST, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nPatched file written to {DST}")
