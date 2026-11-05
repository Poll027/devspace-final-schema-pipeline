#!/usr/bin/env python3
"""
Patch interactions.part.c2.json per repair-round findings.

Changes:
1. tile_spreadsheet_lookups_troubleshooting/s10 (MANDATORY):
   Wrong-answer feedback and hints reference drivers!A:A / drivers!B:B but the
   starter instructs the learner to use A:A / B:B (no sheet prefix).
   → Strip the "drivers!" prefix from the incorrect feedback message and hints.

2. tile_spreadsheet_lookups_troubleshooting/s05 (ADVISORY):
   f5 (XLOOKUP direction advantage) claimed in MEASURES but the exercise layout
   is left-to-right, not demonstrating the direction advantage.
   → Remove f5 from the second measures entry for s05.

3. tile_spreadsheet_cleaning_cross_sheet/s10 (ADVISORY):
   MEASURES claims write_cross_workbook_link_with_square_bracket_syntax (f3)
   but the question only tests same-workbook reference syntax.
   → Remove that measures entry and its anchor from s10.
"""

import json, re, copy

PATH = "batches/final_batch_011_da_spreadsheet/interactions.part.c2.json"

with open(PATH) as f:
    data = json.load(f)

def find_interaction(tiles, step_id):
    for tile in tiles:
        for ix in tile["interactions"]:
            if ix["step_id"] == step_id:
                return ix["interaction"]
    raise KeyError(f"step_id not found: {step_id}")

tiles = data["tiles"]

# ── Fix 1: s10 wrong-answer feedback and hints ──────────────────────────────
s10 = find_interaction(tiles, "tile_spreadsheet_lookups_troubleshooting.s10")

# Fix the incorrect feedback message
inc_msg = s10["feedback"]["incorrect"]["message"]
inc_msg = inc_msg.replace("drivers!A:A", "A:A").replace("drivers!B:B", "B:B")
s10["feedback"]["incorrect"]["message"] = inc_msg

# Fix the hints
new_hints = []
for hint in s10["feedback"]["hints"]:
    hint = hint.replace("drivers!A:A", "A:A").replace("drivers!B:B", "B:B")
    new_hints.append(hint)
s10["feedback"]["hints"] = new_hints

# ── Fix 2: s05 — remove f5 from XLOOKUP measures entry ──────────────────────
s05 = find_interaction(tiles, "tile_spreadsheet_lookups_troubleshooting.s05")

for m in s05["measures"]:
    if m["capability"] == "write_xlookup_with_lookup_array_return_array_and_direction_awareness":
        if "f5" in m["fact_ids"]:
            m["fact_ids"].remove("f5")
        break

# ── Fix 3: s10 cleaning_cross_sheet — remove cross-workbook measures entry ──
s10_clean = find_interaction(tiles, "tile_spreadsheet_cleaning_cross_sheet.s10")

# Remove the measures entry for write_cross_workbook_link_with_square_bracket_syntax
s10_clean["measures"] = [
    m for m in s10_clean["measures"]
    if m["capability"] != "write_cross_workbook_link_with_square_bracket_syntax"
]

# Remove the corresponding anchor
s10_clean["anchors"] = [
    a for a in s10_clean["anchors"]
    if "write_cross_workbook_link_with_square_bracket_syntax" not in a
]

# ── Write out ────────────────────────────────────────────────────────────────
with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Patch applied successfully.")
