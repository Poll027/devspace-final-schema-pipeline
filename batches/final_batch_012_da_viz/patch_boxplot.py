#!/usr/bin/env python3
"""Patch the boxplot interaction to use 'labels' instead of 'tick_labels'."""

import json

with open('interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and fix the interaction with step_id tile_viz_line_scatter_box.s15
for tile in data['tiles']:
    for item in tile['interactions']:
        if item['step_id'] == 'tile_viz_line_scatter_box.s15':
            ix = item['interaction']
            
            # Fix 1: the solution file in grading.solution_files
            for sol_file in ix['grading']['solution_files']:
                if sol_file['path'] == 'solution.py':
                    # Replace tick_labels with labels
                    sol_file['content'] = sol_file['content'].replace('tick_labels=', 'labels=')
                    print(f"Fixed solution file in grading.solution_files")
            
            # Fix 2: the allowed_syntax in constraints
            allowed = ix['public']['constraints'].get('allowed_syntax', [])
            for i, syntax in enumerate(allowed):
                if 'tick_labels' in syntax:
                    allowed[i] = syntax.replace('tick_labels', 'labels')
                    print(f"Fixed allowed_syntax: {syntax} -> {allowed[i]}")
            
            print("\nUpdated allowed_syntax:")
            for s in allowed:
                print(f"  {s}")

# Write back
with open('interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatch complete!")
