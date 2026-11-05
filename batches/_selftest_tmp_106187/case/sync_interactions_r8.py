"""Sync interactions.json from the patched interactions.part.c2.json for c2 tiles."""
import json

with open('batches/final_batch_008_da_python_core/interactions.json') as f:
    data = json.load(f)

with open('batches/final_batch_008_da_python_core/interactions.part.c2.json') as f:
    c2 = json.load(f)

# Build a map of step_id -> interaction from c2 (all c2 tiles)
c2_map = {}
for tile in c2['tiles']:
    for entry in tile['interactions']:
        c2_map[entry['step_id']] = entry['interaction']

# Update interactions.json with the patched values from c2
updated = []
for tile in data['tiles']:
    for entry in tile['interactions']:
        sid = entry['step_id']
        if sid in c2_map:
            entry['interaction'] = c2_map[sid]
            updated.append(sid)

with open('batches/final_batch_008_da_python_core/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print(f"Updated {len(updated)} interactions: {updated}")
print("Written interactions.json")
