#!/usr/bin/env python3
"""Fix the boxplot interaction to use 'labels' instead of 'tick_labels' (matplotlib 3.8.4)."""

import json

# Read the file
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and fix the problematic interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_viz_line_scatter_box.s15':
                # Fix the solution: change tick_labels to labels
                solution_content = ix['interaction']['grading']['solution_files'][0]['content']
                fixed_solution = solution_content.replace('tick_labels=', 'labels=')
                ix['interaction']['grading']['solution_files'][0]['content'] = fixed_solution
                
                # Fix the prompt
                prompt = ix['interaction']['public']['prompt']
                fixed_prompt = prompt.replace('`tick_labels` parameter', '`labels` parameter')
                ix['interaction']['public']['prompt'] = fixed_prompt
                
                # Fix allowed_syntax
                allowed = ix['interaction']['public']['constraints']['allowed_syntax']
                fixed_allowed = [s.replace('tick_labels=', 'labels=') for s in allowed]
                ix['interaction']['public']['constraints']['allowed_syntax'] = fixed_allowed
                
                print(f"Fixed interaction {ix['step_id']}:")
                print(f"  - Solution: tick_labels -> labels")
                print(f"  - Prompt: tick_labels -> labels")
                print(f"  - Allowed syntax: tick_labels -> labels")
                break
        break

# Write back
with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nFile updated successfully.")
