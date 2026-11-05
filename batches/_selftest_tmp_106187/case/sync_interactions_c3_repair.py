"""Sync interactions.json from the patched interactions.part.c3.json for c3 tiles."""
import json

with open('batches/final_batch_008_da_python_core/interactions.json') as f:
    data = json.load(f)

with open('batches/final_batch_008_da_python_core/interactions.part.c3.json') as f:
    c3 = json.load(f)

# Build a map of step_id -> interaction from c3 (all c3 tiles)
c3_map = {}
for tile in c3['tiles']:
    for entry in tile['interactions']:
        c3_map[entry['step_id']] = entry['interaction']

# Update interactions.json with the patched values from c3
updated = []
for tile in data['tiles']:
    for entry in tile['interactions']:
        sid = entry['step_id']
        if sid in c3_map:
            entry['interaction'] = c3_map[sid]
            updated.append(sid)

with open('batches/final_batch_008_da_python_core/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print(f"Updated {len(updated)} interactions: {updated}")
print("Written interactions.json")
