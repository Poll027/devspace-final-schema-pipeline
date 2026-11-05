import json

# Read the part file (source of truth)
with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json') as f:
    part = json.load(f)

# Read the merged file
with open('batches/final_batch_012_da_viz/interactions.json') as f:
    merged = json.load(f)

# Update the tile_viz_figures_layout_plotting tile in the merged file
# with the content from the part file
part_tile = None
for tile in part['tiles']:
    if tile['tile_id'] == 'tile_viz_figures_layout_plotting':
        part_tile = tile
        break

if part_tile is None:
    print("ERROR: tile not found in part file")
    exit(1)

patched = 0
for i, tile in enumerate(merged['tiles']):
    if tile['tile_id'] == 'tile_viz_figures_layout_plotting':
        merged['tiles'][i] = part_tile
        patched += 1
        print(f"Patched tile_viz_figures_layout_plotting in interactions.json")

print(f"Total patched: {patched}")

with open('batches/final_batch_012_da_viz/interactions.json', 'w') as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Done.")
