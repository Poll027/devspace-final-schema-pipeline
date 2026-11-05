#!/usr/bin/env python3
"""Merge interactions.part.*.json into interactions.json."""
import json

# Read all parts
parts = []
for part_name in ['c0_canary', 'c1', 'c2', 'c3']:
    try:
        with open(f'batches/final_batch_011_da_spreadsheet/interactions.part.{part_name}.json') as f:
            parts.append(json.load(f))
    except FileNotFoundError:
        pass

# Merge tiles
tiles_by_id = {}
for part in parts:
    for tile in part.get('tiles', []):
        tile_id = tile['tile_id']
        if tile_id not in tiles_by_id:
            tiles_by_id[tile_id] = {'tile_id': tile_id, 'interactions': []}
        tiles_by_id[tile_id]['interactions'].extend(tile.get('interactions', []))

# Create merged interactions.json
merged = {
    'schema_version': parts[0]['schema_version'],
    'kind': 'interactions',
    'path_id': parts[0]['path_id'],
    'batch_id': parts[0]['batch_id'],
    'tiles': list(tiles_by_id.values())
}

with open('batches/final_batch_011_da_spreadsheet/interactions.json', 'w') as f:
    json.dump(merged, f, indent=2)

print(f"Merged {len(parts)} parts into interactions.json with {len(tiles_by_id)} tiles")
