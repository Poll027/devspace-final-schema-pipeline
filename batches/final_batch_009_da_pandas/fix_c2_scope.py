"""
Fix interactions.part.c2.json to only include tiles in scope:
- tile_pandas_dtype_datetime
- tile_pandas_text_dupes_missing
- tile_pandas_descriptive_stats
"""
import json

# Tiles in scope for c2
SCOPE = [
    'tile_pandas_dtype_datetime',
    'tile_pandas_text_dupes_missing',
    'tile_pandas_descriptive_stats'
]

with open('interactions.part.c2.json') as f:
    data = json.load(f)

# Filter tiles to only those in scope
original_count = len(data['tiles'])
data['tiles'] = [t for t in data['tiles'] if t['tile_id'] in SCOPE]
new_count = len(data['tiles'])

print(f"Filtered from {original_count} tiles to {new_count} tiles")
print(f"Tiles in part: {[t['tile_id'] for t in data['tiles']]}")

# Count interactions
for tile in data['tiles']:
    print(f"  {tile['tile_id']}: {len(tile['interactions'])} interactions")

with open('interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nDone!")
