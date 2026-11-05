#!/usr/bin/env python3
"""Fix all the issues in interactions.part.c1.json"""
import json

# Read the interactions file
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Fix each tile's interactions
for tile in data['tiles']:
    tile_id = tile['tile_id']
    
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        # Fix tile_pandas_creating_inspecting.s04
        # Solution should use variables from starter, not redefine them
        if step_id == 'tile_pandas_creating_inspecting.s04':
            for sol_file in ix['grading']['solution_files']:
                if sol_file['path'] == 'solution.py':
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
        # Remove literals - use only variable references
        elif step_id == 'tile_pandas_selection_filtering.s05':
            for sol_file in ix['grading']['solution_files']:
                if sol_file['path'] == 'solution.py':
                    sol_file['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

loc_result = df.loc[2:4, 'city']
print(loc_result)

iloc_result = df.iloc[2:5, 1]
print(iloc_result)
"""
            print(f"Fixed {step_id}")
        
        # Fix tile_pandas_selection_filtering.s10
        elif step_id == 'tile_pandas_selection_filtering.s10':
            for sol_file in ix['grading']['solution_files']:
                if sol_file['path'] == 'solution.py':
                    sol_file['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

slow = df[df['delivery_time_minutes'] > 25]
print(slow)
"""
            print(f"Fixed {step_id}")
        
        # Fix tile_pandas_sort_rename.s03
        elif step_id == 'tile_pandas_sort_rename.s03':
            for sol_file in ix['grading']['solution_files']:
                if sol_file['path'] == 'solution.py':
                    sol_file['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

sorted_orders = df.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])
print(sorted_orders)
"""
            print(f"Fixed {step_id}")
        
        # Fix tile_pandas_sort_rename.s06
        elif step_id == 'tile_pandas_sort_rename.s06':
            for sol_file in ix['grading']['solution_files']:
                if sol_file['path'] == 'solution.py':
                    sol_file['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

renamed = df.rename(columns={'city': 'destination_city', 'delivery_time_minutes': 'delivery_min'}, index={0: 'first_order'})
print(renamed)
"""
            print(f"Fixed {step_id}")

# Write back
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nAll fixes applied successfully")
