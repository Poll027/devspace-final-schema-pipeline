#!/usr/bin/env python3
"""Fix the s10 input values so mutations cross thresholds."""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json') as f:
    interactions = json.load(f)

# Fix: tile_spreadsheet_aggregation_logical.s10 - change C3 and C4 values
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_aggregation_logical':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_spreadsheet_aggregation_logical.s10':
                ix = interaction_entry['interaction']
                if ix['type'] == 'code_exercise':
                    # Update starter
                    old_starter = ix['public']['workspace']['files'][0]['content']
                    new_starter = old_starter.replace('orders!C3: 45', 'orders!C3: 25')
                    new_starter = new_starter.replace('orders!C4: 62', 'orders!C4: 56')
                    ix['public']['workspace']['files'][0]['content'] = new_starter
                    
                    # Update solution
                    old_solution = ix['grading']['solution_files'][0]['content']
                    new_solution = old_solution.replace('orders!C3: 45', 'orders!C3: 25')
                    new_solution = new_solution.replace('orders!C4: 62', 'orders!C4: 56')
                    ix['grading']['solution_files'][0]['content'] = new_solution
                    
                    # Update test expected values
                    for test in ix['grading']['tests']:
                        if test['test_id'] == 'test_f3_on_time':
                            # C3=25 is < 30, so it's Fast, not On Time
                            test['spec']['expected'] = 'Fast'
                            test['message_on_fail'] = 'F3 should be "Fast" because C3=25 is less than 30. Check the order of your IF conditions: test >60 first, then AND(>=30,<=60), then the else is Fast.'
                        elif test['test_id'] == 'test_f4_late':
                            # C4=56 is between 30 and 60, so it's On Time, not Late
                            test['spec']['expected'] = 'On Time'
                            test['message_on_fail'] = 'F4 should be "On Time" because C4=56 is between 30 and 60. Use AND(C4>=30,C4<=60) as the logical_test of the inner IF.'
                    
                    # Update prompt
                    old_prompt = ix['public']['prompt']
                    new_prompt = old_prompt.replace('C3 = 45', 'C3 = 25')
                    new_prompt = new_prompt.replace('C4 = 62', 'C4 = 56')
                    new_prompt = new_prompt.replace('F3: **"On Time"** (C3 = 45)', 'F3: **"Fast"** (C3 = 25)')
                    new_prompt = new_prompt.replace('F4: **"Late"** (C4 = 62)', 'F4: **"On Time"** (C4 = 56)')
                    ix['public']['prompt'] = new_prompt
                    
                    print(f"Fixed s10 input values: C3: 45->25, C4: 62->56")
                    print(f"Updated expected: F3: On Time->Fast, F4: Late->On Time")

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("Fix applied")
