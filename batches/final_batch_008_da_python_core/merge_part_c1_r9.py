"""Merge patched interactions from interactions.part.c1.json into interactions.json."""
import json
from pathlib import Path

B = Path('batches/final_batch_008_da_python_core')

# Load both files
with open(B / 'interactions.part.c1.json') as f:
    part = json.load(f)

with open(B / 'interactions.json') as f:
    full = json.load(f)

# Build lookup from part: tile_id -> step_id -> interaction
part_lookup = {}
for tile in part['tiles']:
    tid = tile['tile_id']
    part_lookup[tid] = {}
    for ix_entry in tile['interactions']:
        part_lookup[tid][ix_entry['step_id']] = ix_entry['interaction']

# Update full interactions.json with patched entries from part
updated = 0
for tile in full['tiles']:
    tid = tile['tile_id']
    if tid not in part_lookup:
        continue
    for ix_entry in tile['interactions']:
        sid = ix_entry['step_id']
        if sid in part_lookup[tid]:
            ix_entry['interaction'] = part_lookup[tid][sid]
            updated += 1

print(f"Updated {updated} interactions")

with open(B / 'interactions.json', 'w') as f:
    json.dump(full, f, indent=2, ensure_ascii=False)

print("interactions.json updated.")
