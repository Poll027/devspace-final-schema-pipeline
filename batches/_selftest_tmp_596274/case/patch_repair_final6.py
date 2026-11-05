#!/usr/bin/env python3
"""
Try to fix tile_viz_bar_histograms.s06 by adding more explicit syntax patterns.
"""
import json

# Read the interactions file
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Fix tile_viz_bar_histograms.s06
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_bar_histograms':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_bar_histograms.s06':
                interaction = interaction_entry['interaction']
                
                # Add more explicit patterns to allowed syntax
                allowed = interaction['public']['constraints']['allowed_syntax']
                
                # Add patterns for attribute access and indexing if not already there
                patterns_to_add = [
                    "variable assignment",
                    "attribute access (.index, .mean())",
                    "method chaining"
                ]
                
                for pattern in patterns_to_add:
                    if pattern not in allowed:
                        allowed.append(pattern)
                
                print(f"Updated allowed syntax for tile_viz_bar_histograms.s06")
                print(f"New allowed syntax: {allowed}")
                break
        break

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done! Fixed interactions.part.c1.json")
