"""Fix interactions.json: correct remediation_step_ids and allowed_syntax for tile_python_comprehensions_iterating."""
import json

with open('batches/final_batch_008_da_python_core/interactions.json') as f:
    data = json.load(f)

# Load the correct values from interactions.part.c2.json
with open('batches/final_batch_008_da_python_core/interactions.part.c2.json') as f:
    c2 = json.load(f)

# Build a map of step_id -> interaction from c2
c2_map = {}
for tile in c2['tiles']:
    if tile['tile_id'] == 'tile_python_comprehensions_iterating':
        for entry in tile['interactions']:
            c2_map[entry['step_id']] = entry['interaction']

# Update interactions.json with the correct values from c2
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_python_comprehensions_iterating':
        for entry in tile['interactions']:
            sid = entry['step_id']
            if sid in c2_map:
                # Replace the entire interaction with the c2 version
                entry['interaction'] = c2_map[sid]
                print(f"Updated {sid}")

with open('batches/final_batch_008_da_python_core/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Written.")
