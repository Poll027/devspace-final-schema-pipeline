#!/usr/bin/env python3
"""Fix all remaining issues."""

import json

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

def find_item(tile_id, step_id):
    for tile in data['tiles']:
        if tile['tile_id'] == tile_id:
            for item in tile['interactions']:
                if item['step_id'] == step_id:
                    return item
    return None

print("Fixing remaining issues...")

# Fix 1: tile_pandas_dtype_datetime.s04
# - Add starter code with pd.read_csv so solution doesn't need it
# - This moves the "not yet taught" constructs to the starter
item = find_item('tile_pandas_dtype_datetime', 'tile_pandas_dtype_datetime.s04')
if item:
    print("\n1. Fixing tile_pandas_dtype_datetime.s04...")
    ix = item['interaction']
    
    # Update starter to include the data loading
    new_starter = """import pandas as pd

# Load orders with distance_km as strings
orders = pd.read_csv('orders.csv', dtype={'distance_km': str})

# TODO: Convert distance_km to float using astype()

# TODO: Print dtypes to verify
"""
    
    for f in ix['public']['workspace']['files']:
        if f.get('role') == 'editable':
            f['content'] = new_starter
    
    # Update solution to not include pd.read_csv
    new_solution = """import pandas as pd

# Load orders with distance_km as strings
orders = pd.read_csv('orders.csv', dtype={'distance_km': str})

# Convert distance_km to float
orders['distance_km'] = orders['distance_km'].astype(float)

# Print dtypes to verify
print(orders.dtypes)
"""
    ix['grading']['solution_files'][0]['content'] = new_solution
    
    print("  ✓ Added starter with data loading")

# Fix 2: tile_pandas_dtype_datetime.s08
# - Add starter with data loading
item = find_item('tile_pandas_dtype_datetime', 'tile_pandas_dtype_datetime.s08')
if item:
    print("\n2. Fixing tile_pandas_dtype_datetime.s08...")
    ix = item['interaction']
    
    new_starter = """import pandas as pd

orders = pd.read_csv('orders.csv')

# TODO: Convert pickup_date to datetime using pd.to_datetime()

# TODO: Extract month into pickup_month using .dt.month

# TODO: Print pickup_month column
"""
    
    for f in ix['public']['workspace']['files']:
        if f.get('role') == 'editable':
            f['content'] = new_starter
    
    print("  ✓ Added starter")

# Fix 3: tile_pandas_text_dupes_missing.s04
# - Add starter with data loading
item = find_item('tile_pandas_text_dupes_missing', 'tile_pandas_text_dupes_missing.s04')
if item:
    print("\n3. Fixing tile_pandas_text_dupes_missing.s04...")
    ix = item['interaction']
    
    new_starter = """import pandas as pd

orders_messy = pd.read_csv('orders_messy.csv')

# TODO: Clean city column with .str.strip().str.lower()

# TODO: Print city column
"""
    
    for f in ix['public']['workspace']['files']:
        if f.get('role') == 'editable':
            f['content'] = new_starter
    
    print("  ✓ Added starter")

# Fix 4: tile_pandas_text_dupes_missing.s07
# - Add starter with data loading
item = find_item('tile_pandas_text_dupes_missing', 'tile_pandas_text_dupes_missing.s07')
if item:
    print("\n4. Fixing tile_pandas_text_dupes_missing.s07...")
    ix = item['interaction']
    
    new_starter = """import pandas as pd

orders_messy = pd.read_csv('orders_messy.csv')

# TODO: Remove duplicates based on order_id, keeping first

# TODO: Print the cleaned DataFrame
"""
    
    for f in ix['public']['workspace']['files']:
        if f.get('role') == 'editable':
            f['content'] = new_starter
    
    print("  ✓ Added starter")

# Fix 5: tile_pandas_text_dupes_missing.s11
# - Add starter with data loading
item = find_item('tile_pandas_text_dupes_missing', 'tile_pandas_text_dupes_missing.s11')
if item:
    print("\n5. Fixing tile_pandas_text_dupes_missing.s11...")
    ix = item['interaction']
    
    new_starter = """import pandas as pd

orders_messy = pd.read_csv('orders_messy.csv')

# TODO: Fill missing delivery_time_minutes with median

# TODO: Print the filled column
"""
    
    for f in ix['public']['workspace']['files']:
        if f.get('role') == 'editable':
            f['content'] = new_starter
    
    print("  ✓ Added starter")

# Fix 6: tile_pandas_descriptive_stats.s04
# - Add starter with data loading
item = find_item('tile_pandas_descriptive_stats', 'tile_pandas_descriptive_stats.s04')
if item:
    print("\n6. Fixing tile_pandas_descriptive_stats.s04...")
    ix = item['interaction']
    
    new_starter = """import pandas as pd

orders = pd.read_csv('orders.csv')

# TODO: Print mean of delivery_time_minutes

# TODO: Print median of delivery_time_minutes

# TODO: Print std of delivery_time_minutes

# TODO: Print describe() output
"""
    
    for f in ix['public']['workspace']['files']:
        if f.get('role') == 'editable':
            f['content'] = new_starter
    
    print("  ✓ Added starter")

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✅ All fixes applied")
