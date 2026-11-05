#!/usr/bin/env python3
"""
Patch interactions.part.c2.json to fix all validation errors.
"""
import json

def main():
    # Read the interactions file
    with open('interactions.part.c2.json') as f:
        data = json.load(f)
    
    # Read glossary to get correct allowed_syntax
    with open('inputs/path_glossary_bundle.json') as f:
        glossary = json.load(f)
    
    # Extract practice anchors
    practice_anchors = {}
    for bundle in glossary.get('bundles', []):
        for concept in bundle.get('concepts', []):
            cid = concept.get('concept_id', '')
            for anchor in concept.get('assessment_anchors', []):
                if anchor.get('anchor_type') == 'practice':
                    practice_anchors[cid] = {
                        'allowed_syntax': anchor.get('live_code', {}).get('allowed_syntax', []),
                        'blocked_syntax': anchor.get('live_code', {}).get('blocked_syntax', [])
                    }
    
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
                    if 'pandas.dtype_conversion' in practice_anchors:
                        ix['public']['constraints']['allowed_syntax'] = practice_anchors['pandas.dtype_conversion']['allowed_syntax'].copy()
                        ix['public']['constraints']['blocked_syntax'] = practice_anchors['pandas.dtype_conversion']['blocked_syntax'].copy()
                    
                    # Fix solution to not use .dtype
                    ix['grading']['solution_files'][0]['content'] = """import pandas as pd

df = pd.read_csv('orders.csv', dtype={'distance_km': str})

# Convert distance_km to float
df['distance_km'] = df['distance_km'].astype(float)

# Print the mean distance
print(df['distance_km'].mean())
"""
                    
                    # Fix prompt to ask for mean instead of dtype
                    ix['public']['prompt'] = "The `orders` DataFrame has a `distance_km` column loaded as strings (all values are numeric). Convert `distance_km` to float using `astype()`, then print the mean of the column to verify the conversion.\n\nUse only `df['col'].astype(float)`, `df['col'] = ...`, `df['col'].mean()`, and `print()`."
                    
                    # Fix starter
                    ix['public']['workspace']['files'][0]['content'] = """import pandas as pd

# Load data with distance_km as strings
df = pd.read_csv('orders.csv', dtype={'distance_km': str})

# TODO: Convert distance_km to float using astype()

# TODO: Print the mean distance
"""
                    
                    # Fix test to check mean instead of dtype
                    ix['grading']['tests'][0] = {
                        "test_id": "t1",
                        "kind": "stdout_equals",
                        "spec": {
                            "expected": "5.6"
                        },
                        "visible": True,
                        "message_on_fail": "The mean distance should be 5.6. Check that you converted to float and computed the mean."
                    }
                
                # Fix s08: allowed_syntax, solution, expected
                elif step_id == 'tile_pandas_dtype_datetime.s08':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary
                    if 'pandas.dtype_conversion' in practice_anchors:
                        ix['public']['constraints']['allowed_syntax'] = practice_anchors['pandas.dtype_conversion']['allowed_syntax'].copy()
                        ix['public']['constraints']['blocked_syntax'] = practice_anchors['pandas.dtype_conversion']['blocked_syntax'].copy()
                    
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
                
                # Fix s07: allowed_syntax, remove list_lit
                if step_id == 'tile_pandas_text_dupes_missing.s07':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary
                    if 'pandas.drop_duplicates' in practice_anchors:
                        ix['public']['constraints']['allowed_syntax'] = practice_anchors['pandas.drop_duplicates']['allowed_syntax'].copy()
                        ix['public']['constraints']['blocked_syntax'] = practice_anchors['pandas.drop_duplicates']['blocked_syntax'].copy()
                
                # Fix s11: allowed_syntax, expected, remove list_lit
                elif step_id == 'tile_pandas_text_dupes_missing.s11':
                    ix = interaction['interaction']
                    
                    # Copy allowed_syntax from glossary
                    if 'pandas.missing_data_handling' in practice_anchors:
                        ix['public']['constraints']['allowed_syntax'] = practice_anchors['pandas.missing_data_handling']['allowed_syntax'].copy()
                        ix['public']['constraints']['blocked_syntax'] = practice_anchors['pandas.missing_data_handling']['blocked_syntax'].copy()
                    
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
