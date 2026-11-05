"""Merge all interactions.part.*.json files into interactions.json."""
import json

parts = [
    'batches/final_batch_012_da_viz/interactions.part.c0_canary.json',
    'batches/final_batch_012_da_viz/interactions.part.c1.json',
    'batches/final_batch_012_da_viz/interactions.part.c2.json',
]

tiles = []
for path in parts:
    with open(path) as f:
        part = json.load(f)
    tiles.extend(part['tiles'])

merged = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_012_da_viz",
    "tiles": tiles
}

with open('batches/final_batch_012_da_viz/interactions.json', 'w') as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"Written interactions.json with {len(tiles)} tiles")
for t in tiles:
    print(f"  {t['tile_id']}: {len(t['interactions'])} interactions")
