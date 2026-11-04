#!/usr/bin/env python3
"""
Patch screens.part.c0_canary.json:
  Advisory s05/intro: add an explicit bool definition prose block (b05_bool)
  after b03 (str definition) and before b04 (side_by_side visual), so that
  bool gets the same treatment as int/float (b02) and str (b03).
  The text is drawn directly from glossary fact python.core_data_types#f3
  and teaching block python.core_data_types#tb4.
"""
import json, copy, sys

PATH = "batches/final_batch_008_da_python_core/screens.part.c0_canary.json"

with open(PATH) as f:
    doc = json.load(f)

tile = doc["tiles"][0]
assert tile["tile_id"] == "tile_python_variables_types"

# Find step s05
s05 = next(s for s in tile["steps"] if s["step_id"] == "tile_python_variables_types.s05")

# Verify current block order: b01 intro, b02 int/float def, b03 str def, b04 side_by_side
block_ids = [b["block_id"] for b in s05["blocks"]]
print("Current blocks:", block_ids)

# Build the new bool definition prose block
bool_def_block = {
    "type": "prose",
    "block_id": "tile_python_variables_types.s05.b05",
    "role": "definition",
    "text": (
        "The bool type has exactly two values: True and False. "
        "For example, is_late = True records whether a delivery ran late, "
        "and there is no third bool value."
    ),
    "lineage": {
        "concept_ids": ["python.core_data_types"],
        "fact_ids": ["python.core_data_types#f3"],
        "teaching_block_ids": ["python.core_data_types#tb4"],
        "anchors": []
    }
}

# Insert after b03 (index 2) and before b04 (index 3)
b03_idx = next(i for i, b in enumerate(s05["blocks"])
               if b["block_id"] == "tile_python_variables_types.s05.b03")
s05["blocks"].insert(b03_idx + 1, bool_def_block)

# Verify new order
block_ids_after = [b["block_id"] for b in s05["blocks"]]
print("Updated blocks:", block_ids_after)

with open(PATH, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Patch applied successfully.")
