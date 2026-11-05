#!/usr/bin/env python3
"""Fix the expected value for s04 to match the actual data."""

import json

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

for tile in data['tiles']:
    for item in tile['interactions']:
        if item['step_id'] == 'tile_pandas_text_dupes_missing.s04':
            # Fix the expected value to match the 10-row dataset
            test = item['interaction']['grading']['tests'][0]
            test['spec']['expected'] = ['lagos', 'abuja', 'kano', 'kano', 'lagos', 'abuja', 'kano', 'lagos', 'abuja', 'kano']
            print("Fixed s04 expected value to 10 items")

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Fixed")
