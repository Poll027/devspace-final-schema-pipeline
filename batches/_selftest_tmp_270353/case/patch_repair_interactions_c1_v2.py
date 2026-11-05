#!/usr/bin/env python3
"""Fix the remaining errors in interactions.part.c1.json."""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json') as f:
    interactions = json.load(f)

# Fix 1: tile_spreadsheet_text_date_conditional_agg.s03 - change TRUE() to 1
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_text_date_conditional_agg':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_spreadsheet_text_date_conditional_agg.s03':
                ix = interaction_entry['interaction']
                if ix['type'] == 'formula_entry':
                    # Change TRUE() to 1 in reference_formula
                    old_ref = ix['grading']['reference_formula']
                    new_ref = old_ref.replace(',TRUE(),', ',1,')
                    ix['grading']['reference_formula'] = new_ref
                    print(f"Fixed s03 reference_formula: {old_ref} -> {new_ref}")
                    # Also update the feedback messages to mention 1 instead of TRUE
                    ix['feedback']['correct']['message'] = ix['feedback']['correct']['message'].replace('TRUE', '1 (or TRUE())')
                    ix['feedback']['incorrect']['message'] = ix['feedback']['incorrect']['message'].replace('TRUE', '1 (or TRUE())')

# Fix 2: tile_spreadsheet_aggregation_logical.s10 - the test_f5_extreme issue
# The problem is that F5 references C5, which is a typed constant in the starter.
# The gate mutates C5 and checks if F5 changes. But the formula =IF(OR(C5<20,C5>70),"Extreme","Normal")
# should change when C5 changes. Let me check the actual solution.
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_aggregation_logical':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_spreadsheet_aggregation_logical.s10':
                ix = interaction_entry['interaction']
                if ix['type'] == 'code_exercise':
                    # Check the solution
                    solution = ix['grading']['solution_files'][0]['content']
                    print(f"s10 solution:\n{solution}")
                    # The issue might be that the test is checking F5 but the formula is correct.
                    # Let me check if there's a test for F5
                    for test in ix['grading']['tests']:
                        if test['test_id'] == 'test_f5_extreme':
                            print(f"test_f5_extreme: {test}")

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("Fixes applied")
