#!/usr/bin/env python3
"""Patch the solution code for s05 and s10 to fix syntax and hard-coded answer issues."""

import json

# Files to patch
files_to_patch = ['interactions.part.c0_canary.json', 'interactions.json']

for filename in files_to_patch:
    print(f"\nPatching {filename}...")
    
    # Read the artifact
    with open(filename, 'r') as f:
        data = json.load(f)

    # Fix s05 and s10
    for tile in data['tiles']:
        if tile['tile_id'] == 'tile_pandas_dataframe_reading':
            for item in tile['interactions']:
                ix = item['interaction']
                
                # Fix s05: The solution should just use the variables from the starter
                # The starter provides delivery_times and data, so the solution should use them
                if ix['interaction_id'] == 'ix.tile_pandas_dataframe_reading.s05':
                    for sf in ix['grading']['solution_files']:
                        if sf['path'] == 'starter.py':
                            # Solution should use the variables from the starter
                            sf['content'] = """import pandas as pd

# Data provided for you
delivery_times = [18, 20, 22, 22, 26, 28, 80]
data = {
    'order_id': [1001, 1002, 1003],
    'city': ['Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [18, 20, 26]
}

# Create a Series from delivery_times and print it
s = pd.Series(delivery_times)
print(s)

# Create a DataFrame from data and print it
df = pd.DataFrame(data)
print(df)

# Pull out the 'delivery_time_minutes' column and print its type
col = df['delivery_time_minutes']
print(type(col))
"""
                            print(f"  Fixed {ix['interaction_id']}: Solution uses starter variables")
                
                # Fix s10: Use the literal string instead of the variable
                elif ix['interaction_id'] == 'ix.tile_pandas_dataframe_reading.s10':
                    for sf in ix['grading']['solution_files']:
                        if sf['path'] == 'starter.py':
                            # Use the literal string 'orders.csv' instead of file_path variable
                            sf['content'] = """import pandas as pd

# File path provided for you
file_path = 'orders.csv'

# Load the CSV file and print the DataFrame
orders = pd.read_csv('orders.csv')
print(orders)
"""
                            print(f"  Fixed {ix['interaction_id']}: Use literal string for file path")

    # Write back
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

print("\nPatching complete!")
