#!/usr/bin/env python3
"""Fix the s10 solution to include input cells."""
import json

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json') as f:
    interactions = json.load(f)

# Fix: tile_spreadsheet_aggregation_logical.s10 - add input cells to solution
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_spreadsheet_aggregation_logical':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_spreadsheet_aggregation_logical.s10':
                ix = interaction_entry['interaction']
                if ix['type'] == 'code_exercise':
                    # The solution must include the input cells from the starter
                    old_solution = ix['grading']['solution_files'][0]['content']
                    new_solution = """// Input cells (typed constants):
orders!C2: 28
orders!C3: 45
orders!C4: 62
orders!C5: 19

// Formula cells:
F2: =IF(C2>60,"Late",IF(AND(C2>=30,C2<=60),"On Time","Fast"))
F3: =IF(C3>60,"Late",IF(AND(C3>=30,C3<=60),"On Time","Fast"))
F4: =IF(C4>60,"Late",IF(AND(C4>=30,C4<=60),"On Time","Fast"))
F5: =IF(OR(C5<20,C5>70),"Extreme","Normal")
"""
                    ix['grading']['solution_files'][0]['content'] = new_solution
                    print(f"Fixed s10 solution - added input cells")

with open('batches/final_batch_011_da_spreadsheet/interactions.part.c1.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("Fix applied")
