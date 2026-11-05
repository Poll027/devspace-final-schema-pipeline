#!/usr/bin/env python3
"""
Patch script for REPAIR ROUND findings - Version 2
Fixed iloc to use column position instead of column name
"""
import json

# Load the artifact
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# FINDING 2: Fix s05 solution to use comma form
# For iloc, we need to use column position, not column name
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_selection_filtering':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_pandas_selection_filtering.s05':
                # Update solution to use comma form
                # For iloc, compute the column position
                new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

# Slice bounds and column info provided
start_row = 2
end_row_loc = 4  # loc stop is inclusive
end_row_iloc = 5  # iloc stop is exclusive
city_col_name = 'city'

# Select rows and column using comma form
loc_result = df.loc[start_row:end_row_loc, city_col_name]
print(loc_result)

# For iloc, compute the column position
city_col_pos = df.columns.get_loc(city_col_name)
iloc_result = df.iloc[start_row:end_row_iloc, city_col_pos]
print(iloc_result)
"""
                interaction['interaction']['grading']['solution_files'][0]['content'] = new_solution
                print("✓ Fixed s05 solution to use comma form with column position for iloc")
                break

# Write the patched artifact
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✓ Patch applied successfully")
