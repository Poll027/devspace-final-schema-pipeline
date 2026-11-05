#!/usr/bin/env python3
"""Merge updated interactions.part.c2.json into interactions.json."""

import json

# Read the full interactions file
with open('interactions.json', 'r') as f:
    full_data = json.load(f)

# Read the updated c2 part
with open('interactions.part.c2.json', 'r') as f:
    c2_data = json.load(f)

# Create a mapping of tile_id to updated interactions from c2
c2_tiles = {tile['tile_id']: tile for tile in c2_data['tiles']}

# Update the full data with c2 changes
for i, tile in enumerate(full_data['tiles']):
    if tile['tile_id'] in c2_tiles:
        # Replace the tile's interactions with the updated ones from c2
        full_data['tiles'][i] = c2_tiles[tile['tile_id']]
        print(f"Updated {tile['tile_id']}")

# Write back
with open('interactions.json', 'w') as f:
    json.dump(full_data, f, indent=2, ensure_ascii=False)

print('\nMerge complete.')
