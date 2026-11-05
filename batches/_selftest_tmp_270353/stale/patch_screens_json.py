"""
Patch screens.json with the same replacements applied to screens.part.c3.json.
"""
import json

# Load the patched part file to get the replacement blocks
with open("batches/final_batch_011_da_spreadsheet/screens.part.c3.json") as f:
    part = json.load(f)

# Build a map of block_id -> replacement block from the part file
replacement_map = {}
target_block_ids = {
    "tile_spreadsheet_tables_named_ranges.s06.ai1",
    "tile_spreadsheet_pivot_tables.s01.ai1",
    "tile_spreadsheet_formatting_validation.s05.ai1",
}

for tile in part.get("tiles", []):
    for step in tile.get("steps", []) + tile.get("remediation_steps", []):
        for block in step.get("blocks", []):
            if block.get("block_id") in target_block_ids:
                replacement_map[block["block_id"]] = block

print(f"Found replacement blocks: {list(replacement_map.keys())}")

# Now load screens.json and apply the same replacements
with open("batches/final_batch_011_da_spreadsheet/screens.json") as f:
    screens = json.load(f)

replaced = set()
for tile in screens.get("tiles", []):
    for step in tile.get("steps", []) + tile.get("remediation_steps", []):
        blocks = step.get("blocks", [])
        for i, block in enumerate(blocks):
            bid = block.get("block_id", "")
            if bid in replacement_map:
                blocks[i] = replacement_map[bid]
                replaced.add(bid)

print(f"Replaced in screens.json: {replaced}")
assert replaced == target_block_ids, f"Missing: {target_block_ids - replaced}"

with open("batches/final_batch_011_da_spreadsheet/screens.json", "w") as f:
    json.dump(screens, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done.")
