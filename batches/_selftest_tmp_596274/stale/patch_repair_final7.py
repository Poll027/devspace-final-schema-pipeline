#!/usr/bin/env python3
"""
Fix tile_viz_bar_histograms.s06 by adding necessary syntax patterns.
The glossary's allowed syntax is incomplete - it doesn't include variable assignment
or pandas imports, which are needed for the exercise to work.
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
                
                # Add necessary patterns to allowed syntax
                allowed = interaction['public']['constraints']['allowed_syntax']
                
                # Patterns needed for the solution to work
                patterns_to_add = [
                    "import pandas as pd",
                    "pd.read_csv('orders.csv')",
                    "variable assignment"
                ]
                
                for pattern in patterns_to_add:
                    if pattern not in allowed:
                        allowed.insert(0, pattern)  # Insert at beginning
                
                print(f"Updated allowed syntax for tile_viz_bar_histograms.s06")
                print(f"New allowed syntax:")
                for s in allowed:
                    print(f"  - {s}")
                break
        break

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nDone! Fixed interactions.part.c1.json")
