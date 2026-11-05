#!/usr/bin/env python3
"""
Final fix for s04 and s10.
"""

import json

# Read the interactions file
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Helper to find and update an interaction
def find_interaction(tile_id, interaction_id):
    for tile in data['tiles']:
        if tile['tile_id'] == tile_id:
            for item in tile['interactions']:
                if item['interaction']['interaction_id'] == interaction_id:
                    return item['interaction']
    return None

print("Applying final fixes...")

# Fix s04: The problem is that the solution converts the mounted data to Python
# data structures (lists/dicts), which breaks the connection to the mount.
# Solution: Test the DataFrames directly, not the intermediate data structures.
# Actually, the real issue is that this exercise is about learning the SYNTAX
# of pd.DataFrame(dict) and pd.DataFrame(list_of_dicts), not about working with
# real data. So it's inherently not data-dependent.
# 
# The best fix: change the exercise to test something that IS data-dependent.
# For example, test that the DataFrames have the correct shape or values from
# the mounted data.

print("\n1. Fixing ix.tile_pandas_creating_inspecting.s04...")
ix = find_interaction('tile_pandas_creating_inspecting', 'ix.tile_pandas_creating_inspecting.s04')
if ix:
    # Change the exercise to be simpler and more focused on the syntax
    # Remove the mount and just test that the learner can create DataFrames
    # from the given data structures
    
    # Actually, let me try a different approach: keep the mount, but test
    # that the DataFrames match the mounted data
    
    new_starter = """import pandas as pd

# Load the orders data
orders = pd.read_csv('orders.csv')

# TODO: Create df1 from the first 3 rows using a dict of lists
# Hint: Extract the columns as lists using .tolist()

# TODO: Create df2 from the first 3 rows using a list of dicts
# Hint: Use .to_dict('records')

# TODO: Print both DataFrames to verify they match
"""
    
    new_solution = """import pandas as pd

# Load the orders data
orders = pd.read_csv('orders.csv')

# Create df1 from the first 3 rows using a dict of lists
df1 = pd.DataFrame({
    'order_id': orders['order_id'].head(3).tolist(),
    'city': orders['city'].head(3).tolist(),
    'delivery_time_minutes': orders['delivery_time_minutes'].head(3).tolist()
})

# Create df2 from the first 3 rows using a list of dicts
df2 = pd.DataFrame(orders.head(3)[['order_id', 'city', 'delivery_time_minutes']].to_dict('records'))

print(df1)
print(df2)
"""
    
    ix['public']['workspace']['files'][0]['content'] = new_starter
    ix['grading']['solution_files'][0]['content'] = new_solution
    
    # Update the tests to check that the DataFrames have the correct values
    # from the mounted data (first 3 rows)
    ix['grading']['tests'] = [
        {
            'test_id': 't1',
            'kind': 'dataframe_equals',
            'spec': {
                'expr': 'df1',
                'expected': {
                    'columns': ['order_id', 'city', 'delivery_time_minutes'],
                    'rows': [
                        [1001, 'Lagos', 18],
                        [1002, 'Abuja', 20],
                        [1005, 'Abuja', 26]
                    ]
                }
            }
        },
        {
            'test_id': 't2',
            'kind': 'dataframe_equals',
            'spec': {
                'expr': 'df2',
                'expected': {
                    'columns': ['order_id', 'city', 'delivery_time_minutes'],
                    'rows': [
                        [1001, 'Lagos', 18],
                        [1002, 'Abuja', 20],
                        [1005, 'Abuja', 26]
                    ]
                }
            }
        }
    ]
    
    print("   ✓ Updated exercise to test DataFrames directly")

# Fix s10: The starter already has the solution
print("\n2. Verifying ix.tile_pandas_creating_inspecting.s10...")
ix = find_interaction('tile_pandas_creating_inspecting', 'ix.tile_pandas_creating_inspecting.s10')
if ix:
    starter = ix['public']['workspace']['files'][0]['content']
    if 'print(orders.shape)' in starter or 'print(orders.dtypes)' in starter:
        print("   ERROR: Starter still contains solution!")
        # Fix it
        new_starter = """import pandas as pd

orders = pd.read_csv('orders.csv')

# TODO: print the shape
# TODO: print the dtypes
# TODO: print the first 5 rows
"""
        ix['public']['workspace']['files'][0]['content'] = new_starter
        print("   ✓ Removed solution from starter")
    else:
        print("   ✓ Starter is correct")

# Save the updated data
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✓ All fixes applied.")
