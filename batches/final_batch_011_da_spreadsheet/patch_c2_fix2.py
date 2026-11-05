#!/usr/bin/env python3
"""Corrective patch: remove invalid 'note' from grid block, add prose block instead."""
import json

SRC = "batches/final_batch_011_da_spreadsheet/screens.part.c2.json"
DST = SRC

with open(SRC) as f:
    doc = json.load(f)

def find_tile(tile_id):
    for tile in doc["tiles"]:
        if tile["tile_id"] == tile_id:
            return tile
    raise KeyError(tile_id)

def find_step(tile, step_id):
    for step in tile.get("steps", []) + tile.get("remediation_steps", []):
        if step["step_id"] == step_id:
            return step
    raise KeyError(step_id)

def find_block(step, block_id):
    for block in step.get("blocks", []):
        if block.get("block_id") == block_id:
            return block
    raise KeyError(block_id)

lt_tile = find_tile("tile_spreadsheet_lookups_troubleshooting")
s11 = find_step(lt_tile, "tile_spreadsheet_lookups_troubleshooting.s11")

# Remove invalid 'note' field from the grid block
for block in s11["blocks"]:
    if block.get("block_id") == "tile_spreadsheet_lookups_troubleshooting.s11.grid1":
        if "note" in block:
            del block["note"]
            print("Removed 'note' from grid block.")
        break

# Add prose note block after the grid (if not already present)
existing_ids = [b.get("block_id","") for b in s11["blocks"]]
if "tile_spreadsheet_lookups_troubleshooting.s11.p4" not in existing_ids:
    note_block = {
        "type": "prose",
        "block_id": "tile_spreadsheet_lookups_troubleshooting.s11.p4",
        "role": "note",
        "text": (
            "Note: the formulas shown in cells C2 and C3 above are illustrative "
            "examples placed over the data layout to demonstrate error codes; "
            "they do not reflect actual cell contents from the dataset."
        ),
        "lineage": {
            "concept_ids": ["spreadsheet.formula_error_troubleshooting"],
            "teaching_block_ids": [
                "spreadsheet.formula_error_troubleshooting#tb2",
                "spreadsheet.formula_error_troubleshooting#tb3"
            ],
            "fact_ids": [
                "spreadsheet.formula_error_troubleshooting#f1",
                "spreadsheet.formula_error_troubleshooting#f2"
            ]
        }
    }
    s11["blocks"].append(note_block)
    print("Added prose note block to s11.")
else:
    print("s11.p4 already present.")

with open(DST, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print("Corrective patch applied.")
