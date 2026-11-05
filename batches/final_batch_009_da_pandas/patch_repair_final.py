#!/usr/bin/env python3
"""
Patch interactions.part.c2.json to fix all validation errors.
"""
import json

def main():
    # Read the interactions file
    with open('interactions.part.c2.json') as f:
        data = json.load(f)
    
    # Correct allowed_syntax from glossary
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
                    
                    # Copy allowed_syntax from glossary
                    ix['public']['constraints']['allowed_syntax'] = dtype_conversion_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = dtype_conversion_blocked.copy()
                    
                    # Fix solution to not use .dtype - use dtypes instead
                    ix['grading']['solution_files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders.csv', dtype={'distance_km': str})

# Convert distance_km to float
df['distance_km'] = df['distance_km'].astype(float)

# Print the dtypes to verify
print(df.dtypes)
"""
                    
                    # Fix prompt to ask for dtypes (which is allowed)
                    ix['public']['prompt'] = "The `orders` DataFrame has a `distance_km` column loaded as strings (all values are numeric). Convert `distance_km` to float using `astype()`, then print `df.dtypes` to verify the conversion.\n\nUse only `df['col'].astype(float)`, `df['col'] = ...`, `df.dtypes`, and `print()`."
                    
                    # Fix starter
                    ix['public']['workspace']['files'][0]['content'] = """import pandas as pd

# Load data with distance_km as strings
df = pd.read_csv('orders.csv', dtype={'distance_km': str})

# TODO: Convert distance_km to float using astype()

# TODO: Print df.dtypes to verify
"""
                    
                    # Fix test to check stdout for dtypes output
                    # The output will include all columns, and distance_km should be float64
                    ix['grading']['tests'][0] = {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "str(df['distance_km'].dtype)",
                            "expected": "float64"
                        },
                        "visible": True,
                        "message_on_fail": "The distance_km column should have dtype float64 after conversion."
                    }
                
                # Fix s08: allowed_syntax, solution, expected
                elif step_id == 'tile_pandas_dtype_datetime.s08':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary
                    ix['public']['constraints']['allowed_syntax'] = dtype_conversion_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = dtype_conversion_blocked.copy()
                    
                    # Fix solution to not use .dtype and to convert distance_km to int64
                    ix['grading']['solution_files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

# Convert pickup_date to datetime
df['pickup_date'] = pd.to_datetime(df['pickup_date'])

# Convert distance_km to int64
df['distance_km'] = df['distance_km'].astype('int64')

# Print dtypes
print(df['pickup_date'].dtypes)
print(df['distance_km'].dtypes)
"""
                    
                    # Fix expected to show int64 instead of int32
                    ix['grading']['tests'][0]['spec']['expected'] = "datetime64[ns]\nint64"
        
        elif tile_id == 'tile_pandas_text_dupes_missing':
            for interaction in tile['interactions']:
                step_id = interaction['step_id']
                
                # Fix s07: allowed_syntax
                if step_id == 'tile_pandas_text_dupes_missing.s07':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary
                    ix['public']['constraints']['allowed_syntax'] = drop_duplicates_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = drop_duplicates_blocked.copy()
                
                # Fix s11: allowed_syntax, expected
                elif step_id == 'tile_pandas_text_dupes_missing.s11':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary
                    ix['public']['constraints']['allowed_syntax'] = missing_data_allowed.copy()
                    ix['public']['constraints']['blocked_syntax'] = missing_data_blocked.copy()
                    
                    # Fix expected - should be 13 rows after dropping rows with missing delivery_time_minutes
                    # The orders_messy variant has 15 rows (14 base + 1 duplicate)
                    # After dropping the row with missing delivery_time_minutes (order 1008), we have 14 rows
                    # But we also need to drop duplicates first, so 15 - 1 (duplicate) - 1 (missing) = 13
                    ix['grading']['tests'][0]['spec']['expected'] = 13
    
    # Write back
    with open('interactions.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Patched interactions.part.c2.json")

if __name__ == '__main__':
    main()
