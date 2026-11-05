#!/usr/bin/env python3
"""
Update screens.json with the patched tile from screens.part.c1.json
"""

import json

# Read the patched part
with open('screens.part.c1.json', 'r') as f:
    part = json.load(f)

# Read the full screens file
with open('screens.json', 'r') as f:
    screens = json.load(f)

# Find and replace the tile_stats_ab_test_lift tile
for i, tile in enumerate(screens['tiles']):
    if tile['tile_id'] == 'tile_stats_ab_test_lift':
        # Replace with the patched version
        screens['tiles'][i] = part['tiles'][0]
        print(f"Replaced tile {tile['tile_id']} in screens.json")
        break

# Write back
with open('screens.json', 'w') as f:
    json.dump(screens, f, indent=2)

print("Updated screens.json")
