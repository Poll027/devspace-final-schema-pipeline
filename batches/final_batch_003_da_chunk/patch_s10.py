#!/usr/bin/env python3
"""Patch s10 interaction to add 'off-diagonal' clarification to task 2 for consistency."""
import json

with open('interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and patch the s10 interaction
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_stats_correlation':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_stats_correlation.s10':
                # Update task 2 prompt to include off-diagonal clarification
                tasks = interaction['interaction']['public']['tasks']
                for task in tasks:
                    if task['task_id'] == 'task_middle_magnitude':
                        # Add off-diagonal clarification for consistency
                        task['prompt'] = "Select the cell showing the pair with the middle-ranked strength (excluding the diagonal)."
                        print(f"Updated task_middle_magnitude prompt to: {task['prompt']}")
                        break
                break
        break

with open('interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Patch complete.")
