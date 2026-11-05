import json

# Load the interactions file
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Load glossary to get correct allowed_syntax
with open('batches/final_batch_009_da_pandas/inputs/path_glossary_bundle.json', 'r') as f:
    glossary = json.load(f)

# Extract practice anchors for each concept
practice_anchors = {}
for bundle in glossary['bundles']:
    concept_id = bundle['context']['concept_id']
    if 'practice_anchor' in bundle:
        practice_anchors[concept_id] = bundle['practice_anchor'].get('live_code', {})

print(f"Found {len(practice_anchors)} practice anchors")

# Fix each tile
for tile in data['tiles']:
    for item in tile['interactions']:
        step_id = item['step_id']
        interaction = item['interaction']
        
        # Fix tile_pandas_creating_inspecting.s04
        if step_id == 'tile_pandas_creating_inspecting.s04':
            print(f"\nFixing {step_id}...")
            
            # Fix the expected values (rows 0,1,2 are 1001,1002,1003 not 1005)
            for test in interaction['grading']['tests']:
                if test['test_id'] in ['t1', 't2']:
                    test['spec']['expected']['rows'][2] = [1003, "Kano", 22]
            
            # Fix the solution to not use forbidden syntax
            # The solution should be simple and only use allowed syntax
            new_solution = """import pandas as pd

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

# Create DataFrames
df1 = pd.DataFrame(data_dict)
df2 = pd.DataFrame(data_list)

print(df1)
print(df2)
"""
            interaction['grading']['solution_files'][0]['content'] = new_solution
            
            # Update the starter to not reference CSV
            new_starter = """import pandas as pd

# TODO: Create data_dict with keys 'order_id', 'city', 'delivery_time_minutes'
# Each key should map to a list of 3 values

# TODO: Create df1 from data_dict using pd.DataFrame()

# TODO: Create data_list as a list of 3 dicts
# Each dict should have the same keys

# TODO: Create df2 from data_list using pd.DataFrame()

# TODO: Print both DataFrames
"""
            interaction['public']['workspace']['files'][0]['content'] = new_starter
            
            # Remove asset_mounts since we're not using CSV
            interaction['public']['workspace']['asset_mounts'] = []
            
            # Update prompt
            interaction['public']['prompt'] = "Build a DataFrame two ways and print each:\n1. From a dict of lists with keys `order_id`, `city`, `delivery_time_minutes` (3 values each: orders 1001/Lagos/18, 1002/Abuja/20, 1003/Kano/22).\n2. From a list of 3 dicts, each with the same keys.\n\nBoth should produce the same table with 3 rows and 3 columns."
            
            print(f"  Fixed solution, starter, prompt, and expected values")
        
        # Fix tile_pandas_creating_inspecting.s10
        elif step_id == 'tile_pandas_creating_inspecting.s10':
            print(f"\nFixing {step_id}...")
            
            # Get correct allowed_syntax from glossary
            if 'pandas.inspecting_dataframes' in practice_anchors:
                correct_syntax = practice_anchors['pandas.inspecting_dataframes']
                interaction['public']['constraints']['allowed_syntax'] = correct_syntax.get('allowed_syntax', [])
                interaction['public']['constraints']['blocked_syntax'] = correct_syntax.get('blocked_syntax', [])
                print(f"  Updated allowed_syntax from glossary")
            
            # Fix the solution to use df instead of orders
            new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

print(df.shape)
print(df.dtypes)
print(df.head())
"""
            interaction['grading']['solution_files'][0]['content'] = new_solution
            
            # Fix the starter to use df and not pass tests
            new_starter = """import pandas as pd

df = pd.read_csv('orders.csv')

# TODO: print the shape
# TODO: print the dtypes
# TODO: print the first 5 rows
"""
            interaction['public']['workspace']['files'][0]['content'] = new_starter
            
            # Change tests to check stdout instead of values
            # This way the starter doesn't pass (it doesn't print anything)
            interaction['grading']['tests'] = [
                {
                    "test_id": "t1",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "(14, 10)\norder_id                 int64\ncity                    object\ncity_code               object\ncourier                 object\ndriver_id                int64\ncustomer_id              int64\npickup_date             object\ndelivery_time_minutes    int64\ndistance_km            float64\norder_value            float64\ndtype: object\n   order_id   city city_code courier  driver_id  customer_id pickup_date  \\\n0      1001  Lagos       LOS     Ada        201          301  2024-03-14   \n1      1002  Abuja       ABJ    Bayo        202          302  2024-03-14   \n2      1003   Kano       KAN   Chidi        203          303  2024-03-15   \n3      1004  Lagos       LOS     Ada        201          304  2024-03-15   \n4      1005  Abuja       ABJ    Bayo        202          305  2024-03-16   \n\n   delivery_time_minutes  distance_km  order_value  \n0                     18          4.2       2500.0  \n1                     20          6.1       3100.0  \n2                     22          5.5       1800.0  \n3                     22          3.8       2200.0  \n4                     26          7.3       4000.0  "
                    },
                    "visible": True,
                    "message_on_fail": "The output should show the shape, dtypes, and first 5 rows. Check that you printed all three."
                }
            ]
            
            print(f"  Fixed solution, starter, and tests to use df and check stdout")
        
        # Fix tile_pandas_selection_filtering.s05
        elif step_id == 'tile_pandas_selection_filtering.s05':
            print(f"\nFixing {step_id}...")
            
            if 'pandas.loc_iloc_selection' in practice_anchors:
                correct_syntax = practice_anchors['pandas.loc_iloc_selection']
                interaction['public']['constraints']['allowed_syntax'] = correct_syntax.get('allowed_syntax', [])
                interaction['public']['constraints']['blocked_syntax'] = correct_syntax.get('blocked_syntax', [])
                print(f"  Updated allowed_syntax from glossary")
            
            # Fix the solution to use df instead of orders
            new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

loc_result = df.loc[2:4, 'city']
print(loc_result)

iloc_result = df.iloc[2:5, 1]
print(iloc_result)
"""
            interaction['grading']['solution_files'][0]['content'] = new_solution
            
            # Fix the starter to use df
            new_starter = """import pandas as pd

df = pd.read_csv('orders.csv')

# TODO: use .loc to select rows 2:4 (inclusive), column 'city'
# TODO: use .iloc to select rows 2:5 (exclusive stop), column 1
# TODO: print both results
"""
            interaction['public']['workspace']['files'][0]['content'] = new_starter
            
            print(f"  Fixed solution and starter to use df")
        
        # Fix tile_pandas_selection_filtering.s10
        elif step_id == 'tile_pandas_selection_filtering.s10':
            print(f"\nFixing {step_id}...")
            
            if 'pandas.boolean_filtering' in practice_anchors:
                correct_syntax = practice_anchors['pandas.boolean_filtering']
                interaction['public']['constraints']['allowed_syntax'] = correct_syntax.get('allowed_syntax', [])
                interaction['public']['constraints']['blocked_syntax'] = correct_syntax.get('blocked_syntax', [])
                print(f"  Updated allowed_syntax from glossary")
            
            # Fix the solution to use df instead of orders
            new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

slow = df[df['delivery_time_minutes'] > 25]
print(slow)
"""
            interaction['grading']['solution_files'][0]['content'] = new_solution
            
            # Fix the starter to use df
            new_starter = """import pandas as pd

df = pd.read_csv('orders.csv')

# TODO: filter to rows where delivery_time_minutes > 25
# TODO: print the result
"""
            interaction['public']['workspace']['files'][0]['content'] = new_starter
            
            print(f"  Fixed solution and starter to use df")
        
        # Fix tile_pandas_sort_rename.s03
        elif step_id == 'tile_pandas_sort_rename.s03':
            print(f"\nFixing {step_id}...")
            
            if 'pandas.sort_values' in practice_anchors:
                correct_syntax = practice_anchors['pandas.sort_values']
                interaction['public']['constraints']['allowed_syntax'] = correct_syntax.get('allowed_syntax', [])
                interaction['public']['constraints']['blocked_syntax'] = correct_syntax.get('blocked_syntax', [])
                print(f"  Updated allowed_syntax from glossary")
            
            # Fix the solution to use df instead of orders
            new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

sorted_orders = df.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])
print(sorted_orders)
"""
            interaction['grading']['solution_files'][0]['content'] = new_solution
            
            # Fix the starter to use df
            new_starter = """import pandas as pd

df = pd.read_csv('orders.csv')

# TODO: sort by city ascending, then delivery_time_minutes descending
# TODO: print the result
"""
            interaction['public']['workspace']['files'][0]['content'] = new_starter
            
            print(f"  Fixed solution and starter to use df")
        
        # Fix tile_pandas_sort_rename.s06
        elif step_id == 'tile_pandas_sort_rename.s06':
            print(f"\nFixing {step_id}...")
            
            if 'pandas.rename_columns_index' in practice_anchors:
                correct_syntax = practice_anchors['pandas.rename_columns_index']
                interaction['public']['constraints']['allowed_syntax'] = correct_syntax.get('allowed_syntax', [])
                interaction['public']['constraints']['blocked_syntax'] = correct_syntax.get('blocked_syntax', [])
                print(f"  Updated allowed_syntax from glossary")
            
            # Fix the solution to use df instead of orders
            new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

renamed = df.rename(columns={'city': 'destination_city', 'delivery_time_minutes': 'delivery_min'}, index={0: 'first_order'})
print(renamed)
"""
            interaction['grading']['solution_files'][0]['content'] = new_solution
            
            # Fix the starter to use df
            new_starter = """import pandas as pd

df = pd.read_csv('orders.csv')

# TODO: rename columns and index
# TODO: print the result
"""
            interaction['public']['workspace']['files'][0]['content'] = new_starter
            
            # Fix test t4 to use the renamed index
            for test in interaction['grading']['tests']:
                if test['test_id'] == 't4':
                    test['spec']['expr'] = "renamed.loc['first_order', 'destination_city']"
                    print(f"  Fixed test t4 to use renamed index")
            
            print(f"  Fixed solution and starter to use df")

# Write back
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✓ Fixed interactions file")
