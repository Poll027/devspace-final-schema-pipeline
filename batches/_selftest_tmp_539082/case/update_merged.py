"""
Update the merged interactions.json and screens.json with the patched content
from interactions.part.c1.json and screens.part.c1.json.
"""
import json

# ── Update interactions.json ──────────────────────────────────────────────
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json') as f:
    part = json.load(f)

with open('batches/final_batch_009_da_pandas/interactions.json') as f:
    merged = json.load(f)

# Build lookup from part
part_tiles = {t['tile_id']: t for t in part['tiles']}

for tile in merged['tiles']:
    tid = tile['tile_id']
    if tid not in part_tiles:
        continue
    part_tile = part_tiles[tid]
    part_items = {i['step_id']: i['interaction'] for i in part_tile['interactions']}
    for item in tile['interactions']:
        sid = item['step_id']
        if sid in part_items:
            item['interaction'] = part_items[sid]

with open('batches/final_batch_009_da_pandas/interactions.json', 'w') as f:
    json.dump(merged, f, indent=2)
print("interactions.json updated")

# ── Update screens.json ───────────────────────────────────────────────────
with open('batches/final_batch_009_da_pandas/screens.part.c1.json') as f:
    sc_part = json.load(f)

with open('batches/final_batch_009_da_pandas/screens.json') as f:
    sc_merged = json.load(f)

sc_part_tiles = {t['tile_id']: t for t in sc_part['tiles']}

for tile in sc_merged['tiles']:
    tid = tile['tile_id']
    if tid not in sc_part_tiles:
        continue
    part_tile = sc_part_tiles[tid]
    # Replace steps from part
    part_steps = {s['step_id']: s for s in part_tile.get('steps', [])}
    for i, step in enumerate(tile.get('steps', [])):
        sid = step['step_id']
        if sid in part_steps:
            tile['steps'][i] = part_steps[sid]
    # Replace remediation_steps from part
    part_rem = {s['step_id']: s for s in part_tile.get('remediation_steps', [])}
    for i, step in enumerate(tile.get('remediation_steps', [])):
        sid = step['step_id']
        if sid in part_rem:
            tile['remediation_steps'][i] = part_rem[sid]

with open('batches/final_batch_009_da_pandas/screens.json', 'w') as f:
    json.dump(sc_merged, f, indent=2)
print("screens.json updated")
