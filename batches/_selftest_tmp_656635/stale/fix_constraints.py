#!/usr/bin/env python3
"""
Remove 'constraints' from interaction objects (not from public.constraints in code_exercise).
The schema error says:
  tiles/0/interactions/1/interaction: Additional properties are not allowed ('constraints' was unexpected)
  tiles/0/interactions/6/interaction: Additional properties are not allowed ('constraints' was unexpected)
  tiles/1/interactions/4/interaction: Additional properties are not allowed ('constraints' was unexpected)
"""

import json

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix tiles[0].interactions[1].interaction
if 'constraints' in data['tiles'][0]['interactions'][1]['interaction']:
    del data['tiles'][0]['interactions'][1]['interaction']['constraints']
    print("Removed constraints from tiles[0].interactions[1].interaction")

# Fix tiles[0].interactions[6].interaction
if 'constraints' in data['tiles'][0]['interactions'][6]['interaction']:
    del data['tiles'][0]['interactions'][6]['interaction']['constraints']
    print("Removed constraints from tiles[0].interactions[6].interaction")

# Fix tiles[1].interactions[4].interaction
if 'constraints' in data['tiles'][1]['interactions'][4]['interaction']:
    del data['tiles'][1]['interactions'][4]['interaction']['constraints']
    print("Removed constraints from tiles[1].interactions[4].interaction")

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Fixed interactions.part.c2.json")
