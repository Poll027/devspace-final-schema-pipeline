"""Fix interactions.json: replace all c2 tile interactions with values from interactions.part.c2.json."""
import json

with open('batches/final_batch_008_da_python_core/interactions.json') as f:
    data = json.load(f)

# Load the correct values from interactions.part.c2.json
with open('batches/final_batch_008_da_python_core/interactions.part.c2.json') as f:
    c2 = json.load(f)

# Build a map of tile_id -> {step_id -> interaction} from c2
c2_tiles = {}
for tile in c2['tiles']:
    c2_tiles[tile['tile_id']] = {entry['step_id']: entry['interaction'] for entry in tile['interactions']}

# Update interactions.json with the correct values from c2
for tile in data['tiles']:
    tid = tile['tile_id']
    if tid in c2_tiles:
        for entry in tile['interactions']:
            sid = entry['step_id']
            if sid in c2_tiles[tid]:
                entry['interaction'] = c2_tiles[tid][sid]
                print(f"Updated {sid}")

with open('batches/final_batch_008_da_python_core/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Written.")
