#!/usr/bin/env python3
"""Patch interactions.part.c3.json to fix s07 and s05 syntax violations."""
import json

with open('batches/final_batch_009_da_pandas/interactions.part.c3.json') as f:
    data = json.load(f)

# Fix s07: add 'return' and comparison operators to allowed_syntax
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_map_apply':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_pandas_map_apply.s07':
                # Add 'return' and comparison operators to allowed_syntax
                allowed = interaction['interaction']['public']['constraints']['allowed_syntax']
                if 'return' not in allowed:
                    allowed.append('return')
                if '< <= > >= == !=' not in allowed:
                    allowed.append('< <= > >= == !=')
                print(f"Fixed s07: added 'return' and '< <= > >= == !=' to allowed_syntax")

# Fix s05: change solution and starter to use df.groupby(key).agg(agg_funcs)
# where df = orders[['customer_id', 'order_value']]
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_groupby_melt':
        for interaction in tile['interactions']:
            if interaction['step_id'] == 'tile_pandas_groupby_melt.s05':
                # Update starter
                starter_content = '''import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders[['customer_id', 'order_value']]

key = 'customer_id'
agg_funcs = ['sum', 'mean']

# Group df by key, aggregate with agg_funcs
# Store in result

print(result)
'''
                interaction['interaction']['public']['workspace']['files'][0]['content'] = starter_content
                
                # Update solution
                solution_content = '''import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders[['customer_id', 'order_value']]

key = 'customer_id'
agg_funcs = ['sum', 'mean']

result = df.groupby(key).agg(agg_funcs)

print(result)
'''
                interaction['interaction']['grading']['solution_files'][0]['content'] = solution_content
                
                # Update test expr and expected
                # The result has multi-level columns: ('order_value', 'sum'), ('order_value', 'mean')
                # Use stdout_equals instead of dataframe_equals
                test = interaction['interaction']['grading']['tests'][0]
                test['kind'] = 'stdout_equals'
                test['spec'] = {
                    'expected': '''            order_value        
                    sum    mean
customer_id                    
301                2500  2500.0
302                3100  3100.0
303                1800  1800.0
304                2200  2200.0
305                4000  4000.0
306                1500  1500.0
307                5500  5500.0
308                3800  3800.0
309                2100  2100.0
310                2900  2900.0
311                4200  4200.0
312                1700  1700.0
313                3300  3300.0
314                4600  4600.0'''
                }
                test['message_on_fail'] = 'The result should have one row per customer_id with sum and mean of order_value.'
                
                print(f"Fixed s05: changed solution to use df.groupby(key).agg(agg_funcs) and test to stdout_equals")

with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patched interactions.part.c3.json")
