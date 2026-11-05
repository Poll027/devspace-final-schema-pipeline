"""Merge interactions.part.c2.json into interactions.json."""
import json

# Load the existing interactions.json
with open('batches/final_batch_012_da_viz/interactions.json') as f:
    main = json.load(f)

# Load the c2 part
with open('batches/final_batch_012_da_viz/interactions.part.c2.json') as f:
    c2 = json.load(f)

# Build a map of tile_id -> interactions from c2
c2_tiles = {t['tile_id']: t['interactions'] for t in c2['tiles']}

# Replace the tiles in main with c2 tiles
for i, tile in enumerate(main['tiles']):
    tile_id = tile['tile_id']
    if tile_id in c2_tiles:
        main['tiles'][i]['interactions'] = c2_tiles[tile_id]
        print(f"Replaced {tile_id}: {len(c2_tiles[tile_id])} interactions")

# Write back
with open('batches/final_batch_012_da_viz/interactions.json', 'w') as f:
    json.dump(main, f, indent=2)

print(f"Merged c2 into interactions.json")
