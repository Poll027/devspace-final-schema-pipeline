#!/usr/bin/env python3
"""
Final patch for interactions.part.c2.json to fix all validation errors.
"""
import json

def main():
    # Read the interactions file
    with open('interactions.part.c2.json') as f:
        data = json.load(f)
    
    # Correct allowed_syntax from glossary (MUST be copied verbatim)
    dtype_conversion_allowed = [
        "df['col'].astype(float)",
        "df['col'] = ...",
        "df.astype({...})",
        "df.dtypes",
        "print()"
    ]
    dtype_conversion_blocked = [
        "pd.to_datetime",
        "df['col'].str",
        "df.drop_duplicates",
        "df.fillna"
    ]
    
    drop_duplicates_allowed = [
        "df.duplicated(subset=[...])",
        "df.drop_duplicates(subset=[...])",
        "keep='first'",
        "keep='last'",
        "keep=False",
        "print()"
    ]
    drop_duplicates_blocked = [
        "df.groupby",
        "df.merge",
        "df.sort_values then drop",
        "df.fillna"
    ]
    
    missing_data_allowed = [
        "df.isna()",
        "df.notna()",
        "df.dropna(subset=[...])",
        "df['col'].fillna(value)",
        "df['col'].median()",
        "print()"
    ]
    missing_data_blocked = [
        "df.interpolate",
        "df.ffill",
        "df.replace",
        "df.groupby",
        "df.merge"
    ]
    
    # Process each tile
    for tile in data['tiles']:
        tile_id = tile['tile_id']
        
        if tile_id == 'tile_pandas_dtype_datetime':
            for interaction in tile['interactions']:
                step_id = interaction['step_id']
                
                # Fix s04: allowed_syntax, solution, expected, prompt
                if step_id == 'tile_pandas_dtype_datetime.s04':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary (verbatim)
                    ix['public']['constraints']['allowed_syntax'] = dtype_conversion_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = dtype_conversion_blocked.copy()
                    
                    # Fix solution to not use .dtype - use a value that changes with data
                    # Use the first value to ensure it changes when data changes
                    ix['grading']['solution_files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders.csv', dtype={'distance_km': str})

# Convert distance_km to float
df['distance_km'] = df['distance_km'].astype(float)

# Print the first distance value to verify conversion
print(df['distance_km'][0])
"""
                    
                    # Fix prompt
                    ix['public']['prompt'] = "The `orders` DataFrame has a `distance_km` column loaded as strings (all values are numeric). Convert `distance_km` to float using `astype()`, then print the first value to verify the conversion.\n\nUse only `df['col'].astype(float)`, `df['col'] = ...`, `df['col'][0]`, and `print()`."
                    
                    # Fix starter
                    ix['public']['workspace']['files'][0]['content'] = """import pandas as pd

# Load data with distance_km as strings
df = pd.read_csv('orders.csv', dtype={'distance_km': str})

# TODO: Convert distance_km to float using astype()

# TODO: Print the first distance value
"""
                    
                    # Fix test to check the first value
                    ix['grading']['tests'][0] = {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['distance_km'][0]",
                            "expected": 4.2
                        },
                        "visible": True,
                        "message_on_fail": "The first distance value should be 4.2 after conversion to float."
                    }
                
                # Fix s08: allowed_syntax, solution, expected
                elif step_id == 'tile_pandas_dtype_datetime.s08':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary (verbatim)
                    ix['public']['constraints']['allowed_syntax'] = dtype_conversion_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = dtype_conversion_blocked.copy()
                    
                    # Fix solution to not use .dtype and to use first values
                    ix['grading']['solution_files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

# Convert pickup_date to datetime
df['pickup_date'] = pd.to_datetime(df['pickup_date'])

# Convert distance_km to int64
df['distance_km'] = df['distance_km'].astype('int64')

# Print first values to verify types
print(df['pickup_date'][0])
print(df['distance_km'][0])
"""
                    
                    # Fix expected - print first values instead of dtypes
                    # First pickup_date is '2024-03-14', first distance_km after int conversion is 4
                    ix['grading']['tests'][0]['spec']['expected'] = "2024-03-14 00:00:00\n4"
        
        elif tile_id == 'tile_pandas_text_dupes_missing':
            for interaction in tile['interactions']:
                step_id = interaction['step_id']
                
                # Fix s07: allowed_syntax, provide list in starter
                if step_id == 'tile_pandas_text_dupes_missing.s07':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary (verbatim)
                    ix['public']['constraints']['allowed_syntax'] = drop_duplicates_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = drop_duplicates_blocked.copy()
                    
                    # Provide the list in the starter so learner doesn't write it
                    ix['public']['workspace']['files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders_messy.csv')

# Column to check for duplicates
key_col = ['order_id']

# TODO: Remove duplicates based on key_col, keeping first

# TODO: Print the cleaned DataFrame
"""
                    
                    # Update solution to use the provided variable
                    ix['grading']['solution_files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders_messy.csv')

# Column to check for duplicates
key_col = ['order_id']

# Remove duplicates based on key_col, keeping first
df = df.drop_duplicates(subset=key_col, keep='first')

# Print the cleaned DataFrame
print(df)
"""
                
                # Fix s11: allowed_syntax, expected, provide list in starter
                elif step_id == 'tile_pandas_text_dupes_missing.s11':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary (verbatim)
                    ix['public']['constraints']['allowed_syntax'] = missing_data_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = missing_data_blocked.copy()
                    
                    # Provide the list in the starter
                    ix['public']['workspace']['files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders_messy.csv')

# Column to check for missing values
check_col = ['delivery_time_minutes']

# TODO: Drop rows with missing values in check_col

# TODO: Print shape to show number of rows
"""
                    
                    # Update solution to use the provided variable
                    ix['grading']['solution_files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders_messy.csv')

# Column to check for missing values
check_col = ['delivery_time_minutes']

# Drop rows with missing values in check_col
df = df.dropna(subset=check_col)

# Print shape to show number of rows
print(df.shape)
"""
                    
                    # Fix expected - should be 13 rows
                    # orders_messy has 15 rows (14 base + 1 duplicate of 1003)
                    # After dropping missing delivery_time_minutes (order 1008), we have 14 rows
                    # Wait, we need to check if duplicates are already removed or not
                    # The exercise is only about dropna, not drop_duplicates
                    # So: 15 rows - 1 (missing) = 14 rows
                    ix['grading']['tests'][0]['spec']['expected'] = (14, 10)
    
    # Write back
    with open('interactions.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Patched interactions.part.c2.json")

if __name__ == '__main__':
    main()
