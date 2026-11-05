#!/usr/bin/env python3
"""Fix role: 'note' -> 'practical_context' in s11.p4 prose block."""
import json

SRC = "batches/final_batch_011_da_spreadsheet/screens.part.c2.json"
DST = SRC

with open(SRC) as f:
    doc = json.load(f)

def find_tile(tile_id):
    for tile in doc["tiles"]:
        if tile["tile_id"] == tile_id:
            return tile

def find_step(tile, step_id):
    for step in tile.get("steps", []) + tile.get("remediation_steps", []):
        if step["step_id"] == step_id:
            return step

lt_tile = find_tile("tile_spreadsheet_lookups_troubleshooting")
s11 = find_step(lt_tile, "tile_spreadsheet_lookups_troubleshooting.s11")

for block in s11["blocks"]:
    if block.get("block_id") == "tile_spreadsheet_lookups_troubleshooting.s11.p4":
        block["role"] = "practical_context"
        print("Fixed role to 'practical_context'.")
        break

with open(DST, "w") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print("Done.")
