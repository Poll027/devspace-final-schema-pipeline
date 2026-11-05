#!/usr/bin/env python3
"""Update tile_lessons with fixed interactions from interactions.json."""

import json
import copy

# Load interactions.json
with open('batches/final_batch_012_da_viz/interactions.json') as f:
    interactions = json.load(f)

# Build a map of step_id -> interaction
ix_map = {}
for tile in interactions['tiles']:
    for ix_entry in tile['interactions']:
        ix_map[ix_entry['step_id']] = ix_entry['interaction']

# Update each tile_lessons file
tiles_to_update = [
    'tile_viz_labeling_chart_selection',
    'tile_viz_custom_multi_panel',
    'tile_viz_seaborn_stats_themes'
]

for tile_id in tiles_to_update:
    path = f'batches/final_batch_012_da_viz/tile_lessons/{tile_id}.json'
    with open(path) as f:
        tl = json.load(f)
    
    # Update interactions in steps
    for s in tl['steps']:
        step_id = s['step_id']
        if step_id in ix_map:
            s['interaction'] = copy.deepcopy(ix_map[step_id])
            print(f"Updated {step_id}")
    
    # Recompute content_hash
    from hashlib import sha256
    content = {k: v for k, v in tl.items() if k != 'content_hash'}
    tl['content_hash'] = sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
    
    # Write back
    with open(path, 'w') as f:
        json.dump(tl, f, indent=2)
    
    print(f"Updated {tile_id}")

print("\nDone")
