#!/usr/bin/env python3
import json

# Read files
with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'r') as f:
    interactions = json.load(f)

with open('batches/final_batch_009_da_pandas/screens.json', 'r') as f:
    screens = json.load(f)

# Fix 1: Remove pd.read_csv and other setup code from solutions
# The solutions should only contain what the learner needs to write

for tile in interactions['tiles']:
    for interaction_entry in tile['interactions']:
        step_id = interaction_entry['step_id']
        interaction = interaction_entry['interaction']
        
        if interaction['type'] == 'code_exercise' and 'grading' in interaction:
            if 'solution_files' in interaction['grading']:
                for sol_file in interaction['grading']['solution_files']:
                    content = sol_file['content']
                    
                    # Fix tile_pandas_dtype_datetime.s04
                    if step_id == 'tile_pandas_dtype_datetime.s04':
                        sol_file['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv', dtype={'distance_km': str})

# Convert distance_km to float
orders['distance_km'] = orders['distance_km'].astype(float)

# Print dtypes to verify
print(orders.dtypes)
"""
                    
                    # Fix tile_pandas_dtype_datetime.s08
                    elif step_id == 'tile_pandas_dtype_datetime.s08':
                        sol_file['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')

# Convert pickup_date to datetime
orders['pickup_date'] = pd.to_datetime(orders['pickup_date'])

# Extract month into pickup_month
orders['pickup_month'] = orders['pickup_date'].dt.month

# Print pickup_month column
print(orders['pickup_month'])
"""
                    
                    # Fix tile_pandas_text_dupes_missing.s04
                    elif step_id == 'tile_pandas_text_dupes_missing.s04':
                        sol_file['content'] = """import pandas as pd

orders_messy = pd.read_csv('orders_messy.csv')

# Clean city column with .str.strip().str.lower()
orders_messy['city'] = orders_messy['city'].str.strip().str.lower()

# Print city column
print(orders_messy['city'])
"""
                    
                    # Fix tile_pandas_text_dupes_missing.s07
                    elif step_id == 'tile_pandas_text_dupes_missing.s07':
                        sol_file['content'] = """import pandas as pd

orders_messy = pd.read_csv('orders_messy.csv')

# Remove duplicates based on order_id, keeping first
orders_messy = orders_messy.drop_duplicates(subset=['order_id'], keep='first')

# Print the cleaned DataFrame
print(orders_messy)
"""
                    
                    # Fix tile_pandas_text_dupes_missing.s11
                    elif step_id == 'tile_pandas_text_dupes_missing.s11':
                        sol_file['content'] = """import pandas as pd

orders_messy = pd.read_csv('orders_messy.csv')

# Fill missing delivery_time_minutes with median
median_val = orders_messy['delivery_time_minutes'].median()
orders_messy['delivery_time_minutes'] = orders_messy['delivery_time_minutes'].fillna(median_val)

# Print the filled column
print(orders_messy['delivery_time_minutes'])
"""
                    
                    # Fix tile_pandas_descriptive_stats.s04 - make starter NOT pass
                    elif step_id == 'tile_pandas_descriptive_stats.s04':
                        # Update the starter to not pass
                        if 'workspace' in interaction['public']:
                            for file in interaction['public']['workspace']['files']:
                                if file['path'] == 'solution.py':
                                    file['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')

# TODO: Print mean of delivery_time_minutes

# TODO: Print median of delivery_time_minutes

# TODO: Print std of delivery_time_minutes
"""
                        
                        # Keep solution as is
                        sol_file['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')

# Print mean of delivery_time_minutes
print(orders['delivery_time_minutes'].mean())

# Print median of delivery_time_minutes
print(orders['delivery_time_minutes'].median())

# Print std of delivery_time_minutes
print(orders['delivery_time_minutes'].std())
"""

# Fix 2: Change data_table in tile_pandas_text_dupes_missing.s05 to use variant
for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_pandas_text_dupes_missing':
        for step in tile['steps']:
            if step['step_id'] == 'tile_pandas_text_dupes_missing.s05':
                for block in step.get('blocks', []):
                    if block['type'] == 'before_after':
                        if 'before' in block and block['before']['type'] == 'data_table':
                            # Add variant_id to asset_ref
                            block['before']['asset_ref']['variant_id'] = 'orders_messy'
                            print(f"Fixed data_table in {step['step_id']}")

# Write back
with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'w') as f:
    json.dump(interactions, f, indent=2)

with open('batches/final_batch_009_da_pandas/screens.json', 'w') as f:
    json.dump(screens, f, indent=2)

print("\nAll fixes applied")
