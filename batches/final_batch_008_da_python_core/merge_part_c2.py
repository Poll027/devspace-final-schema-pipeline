#!/usr/bin/env python3
"""Merge the patched interactions.part.c2.json back into interactions.json."""
import json

B = 'batches/final_batch_008_da_python_core'

# Load the full interactions.json
with open(f'{B}/interactions.json') as f:
    full = json.load(f)

# Load the patched part
with open(f'{B}/interactions.part.c2.json') as f:
    part = json.load(f)

# Build a lookup from the part: tile_id -> step_id -> interaction
part_lookup = {}
for tile in part['tiles']:
    part_lookup[tile['tile_id']] = {
        ix['step_id']: ix['interaction']
        for ix in tile['interactions']
    }

# Update full interactions.json with patched data
for tile in full['tiles']:
    tid = tile['tile_id']
    if tid in part_lookup:
        for ix_entry in tile['interactions']:
            sid = ix_entry['step_id']
            if sid in part_lookup[tid]:
                ix_entry['interaction'] = part_lookup[tid][sid]
                print(f"  Updated {sid}")

with open(f'{B}/interactions.json', 'w') as f:
    json.dump(full, f, indent=2)

print("interactions.json updated.")
