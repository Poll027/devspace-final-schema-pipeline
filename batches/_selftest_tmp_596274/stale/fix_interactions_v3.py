#!/usr/bin/env python3
"""Fix the interactions.part.c2.json file - remove bad test t04."""

import json

# Read the file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Process each tile
for tile in data['tiles']:
    for ix in tile['interactions']:
        step_id = ix['step_id']
        interaction = ix['interaction']
        
        # Fix tile_viz_custom_multi_panel.s04 - remove test t04
        if step_id == 'tile_viz_custom_multi_panel.s04':
            # Remove test t04
            interaction['grading']['tests'] = [
                test for test in interaction['grading']['tests']
                if test.get('test_id') != 't04'
            ]

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Removed test t04 from tile_viz_custom_multi_panel.s04")
