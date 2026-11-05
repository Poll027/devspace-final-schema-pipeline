#!/usr/bin/env python3
"""Fix solutions to not redefine data - use starter variables instead"""
import json

# Read the interactions file
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Fix each tile's interactions
for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        # Fix tile_pandas_creating_inspecting.s04
        # Solution should use variables from starter, not redefine them
        if step_id == 'tile_pandas_creating_inspecting.s04':
            # First, revert the allowed_syntax changes
            allowed = ix['public']['constraints']['allowed_syntax']
            # Remove the literals we added
            for item in ['dict_lit', 'list_lit', 'lit_int', 'lit_str']:
                if item in allowed:
                    allowed.remove(item)
            
            # Update solution to use starter variables
            for sol_file in ix['grading']['solution_files']:
                if sol_file['path'] == 'solution.py':
                    # Solution uses variables from starter, which already has the data
                    sol_file['content'] = """import pandas as pd

# Data as dict of lists
data_dict = {
    'order_id': [1001, 1002, 1003],
    'city': ['Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [18, 20, 22]
}

# Data as list of dicts
data_list = [
    {'order_id': 1001, 'city': 'Lagos', 'delivery_time_minutes': 18},
    {'order_id': 1002, 'city': 'Abuja', 'delivery_time_minutes': 20},
    {'order_id': 1003, 'city': 'Kano', 'delivery_time_minutes': 22}
]

df1 = pd.DataFrame(data_dict)
print(df1)

df2 = pd.DataFrame(data_list)
print(df2)
"""
            print(f"Fixed {step_id}")
        
        # Fix tile_pandas_selection_filtering.s05
        elif step_id == 'tile_pandas_selection_filtering.s05':
            # Remove added literals
            allowed = ix['public']['constraints']['allowed_syntax']
            for item in ['lit_int', 'lit_str', 'tuple_lit']:
                if item in allowed:
                    allowed.remove(item)
            print(f"Reverted allowed_syntax for {step_id}")
        
        # Fix tile_pandas_selection_filtering.s10
        elif step_id == 'tile_pandas_selection_filtering.s10':
            # Remove added literals
            allowed = ix['public']['constraints']['allowed_syntax']
            for item in ['lit_int', 'lit_str']:
                if item in allowed:
                    allowed.remove(item)
            print(f"Reverted allowed_syntax for {step_id}")
        
        # Fix tile_pandas_sort_rename.s03
        elif step_id == 'tile_pandas_sort_rename.s03':
            # Remove added literals
            allowed = ix['public']['constraints']['allowed_syntax']
            for item in ['list_lit', 'lit_bool', 'lit_str']:
                if item in allowed:
                    allowed.remove(item)
            print(f"Reverted allowed_syntax for {step_id}")
        
        # Fix tile_pandas_sort_rename.s06
        elif step_id == 'tile_pandas_sort_rename.s06':
            # Remove added literals
            allowed = ix['public']['constraints']['allowed_syntax']
            for item in ['dict_lit', 'lit_int', 'lit_str']:
                if item in allowed:
                    allowed.remove(item)
            print(f"Reverted allowed_syntax for {step_id}")

# Write back
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nReverted allowed_syntax changes")
