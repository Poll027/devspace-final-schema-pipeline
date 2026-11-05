#!/usr/bin/env python3
"""Patch screens.json with the fixed s11 grid from screens.part.c2.json."""

import json

# Load the patched part file
with open("batches/final_batch_011_da_spreadsheet/screens.part.c2.json") as f:
    part = json.load(f)

# Find the s11 grid block in the part file
s11_grid = None
for tile in part.get("tiles", []):
    if tile["tile_id"] == "tile_spreadsheet_lookups_troubleshooting":
        for step in tile.get("steps", []):
            if step["step_id"] == "tile_spreadsheet_lookups_troubleshooting.s11":
                for block in step.get("blocks", []):
                    if block.get("type") == "spreadsheet_grid":
                        s11_grid = block
                        break

if not s11_grid:
    print("ERROR: Could not find s11 grid in part file")
    exit(1)

print(f"Found s11 grid block: {s11_grid['block_id']}")
print(f"D2 formula: {[c for c in s11_grid['cells'] if c['ref'] == 'D2'][0]['formula']}")

# Now load screens.json and replace the s11 grid
with open("batches/final_batch_011_da_spreadsheet/screens.json") as f:
    screens = json.load(f)

replaced = False
for tile in screens.get("tiles", []):
    if tile["tile_id"] == "tile_spreadsheet_lookups_troubleshooting":
        for step in tile.get("steps", []):
            if step["step_id"] == "tile_spreadsheet_lookups_troubleshooting.s11":
                blocks = step.get("blocks", [])
                for i, block in enumerate(blocks):
                    if block.get("type") == "spreadsheet_grid":
                        blocks[i] = s11_grid
                        replaced = True
                        print(f"Replaced grid in screens.json")
                        break

if not replaced:
    print("ERROR: Could not find s11 grid in screens.json")
    exit(1)

with open("batches/final_batch_011_da_spreadsheet/screens.json", "w") as f:
    json.dump(screens, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("✓ Patched screens.json")
