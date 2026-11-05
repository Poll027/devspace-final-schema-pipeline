#!/usr/bin/env python3
"""Patch s07 to fix floating-point precision issue by rounding lift to 2 decimal places."""

import json

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and patch s07
for tile in data['tiles']:
    for item in tile.get('interactions', []):
        if 's07' in item['step_id']:
            interaction = item['interaction']
            
            # Update solution to round lift
            solution_content = interaction['grading']['solution_files'][0]['content']
            solution_content = solution_content.replace(
                'lift = treatment_rate / control_rate * 100.0 - 100.0',
                'lift = round(treatment_rate / control_rate * 100.0 - 100.0, 2)'
            )
            interaction['grading']['solution_files'][0]['content'] = solution_content
            
            # Update starter comment to mention rounding
            starter_content = interaction['public']['workspace']['files'][0]['content']
            starter_content = starter_content.replace(
                'lift = None  # replace with: treatment_rate / control_rate * 100.0 - 100.0',
                'lift = None  # replace with: round(treatment_rate / control_rate * 100.0 - 100.0, 2)'
            )
            interaction['public']['workspace']['files'][0]['content'] = starter_content
            
            # Update expected output
            interaction['grading']['tests'][0]['spec']['expected'] = (
                'Positive lift of 10.0%\n'
                'Negative lift of -20.0%\n'
                'Neutral lift of 0.0%'
            )
            
            print(f"Patched {item['step_id']}")
            break

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done")
