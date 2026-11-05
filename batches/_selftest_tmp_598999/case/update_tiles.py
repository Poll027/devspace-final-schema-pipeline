#!/usr/bin/env python3
"""
Manually update the three affected tiles with the fixes from interactions.part.c3.json
"""
import json
from pathlib import Path

# Read the fixed interactions
with open('interactions.part.c3.json') as f:
    interactions_part = json.load(f)

# Create a map of step_id -> interaction for the affected tiles
interactions_map = {}
for tile in interactions_part['tiles']:
    tile_id = tile['tile_id']
    if tile_id in ['tile_pandas_map_apply', 'tile_pandas_groupby_melt', 'tile_pandas_pivot_export']:
        for interaction_entry in tile['interactions']:
            step_id = interaction_entry['step_id']
            interactions_map[step_id] = interaction_entry['interaction']

print(f"Found {len(interactions_map)} interactions to update")

# Update each affected tile
tiles_to_update = ['tile_pandas_map_apply', 'tile_pandas_groupby_melt', 'tile_pandas_pivot_export']

for tile_id in tiles_to_update:
    tile_path = Path('tile_lessons') / f'{tile_id}.json'
    
    if not tile_path.exists():
        print(f"Warning: {tile_path} does not exist")
        continue
    
    with open(tile_path) as f:
        tile_data = json.load(f)
    
    # Update interactions in the tile
    updated_count = 0
    for step in tile_data.get('steps', []):
        step_id = step.get('step_id')
        if step_id in interactions_map:
            # Replace the interaction
            step['interaction'] = interactions_map[step_id]
            updated_count += 1
            print(f"  Updated {step_id}")
    
    if updated_count > 0:
        # Write back the tile
        with open(tile_path, 'w') as f:
            json.dump(tile_data, f, indent=2)
        print(f"✓ Updated {tile_id} ({updated_count} interactions)")
    else:
        print(f"  No updates needed for {tile_id}")

print("\nDone!")
