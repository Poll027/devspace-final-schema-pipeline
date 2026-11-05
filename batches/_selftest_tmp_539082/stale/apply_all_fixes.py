import json

# Load the interactions file
with open('interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Comprehensive fixes for all reported issues
fixes = {
    # 1. ix.tile_pandas_map_apply.s03: Remove comments, keep scaffolding exact
    'ix.tile_pandas_map_apply.s03': {
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}

orders['city_name'] = orders['city_code'].map(city_lookup)

print(orders['city_name'])
'''
    },
    
    # 2. ix.tile_pandas_map_apply.s07: Keep scaffolding exact
    'ix.tile_pandas_map_apply.s07': {
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

def label_speed(row):
    if row['delivery_time_minutes'] > 25:
        return 'slow'
    else:
        return 'fast'

orders['speed_label'] = orders.apply(label_speed, axis=1)

print(orders['speed_label'])
'''
    },
    
    # 3. ix.tile_pandas_groupby_melt.s05: Keep scaffolding exact
    'ix.tile_pandas_groupby_melt.s05': {
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

result = orders.groupby('customer_id')['order_value'].agg(['sum', 'mean'])

print(result)
'''
    },
    
    # 4. ix.tile_pandas_groupby_melt.s09: Fix dataset name to match starter
    'ix.tile_pandas_groupby_melt.s09': {
        'solution': '''import pandas as pd

city_deliveries = pd.read_csv('city_deliveries.csv')

result = city_deliveries.melt(id_vars='city', var_name='month', value_name='deliveries')

print(result)
''',
        'prompt': "The `city_deliveries` DataFrame has a `city` column and three month columns (`jan`, `feb`, `mar`). Use `.melt()` to reshape it to long format with `id_vars='city'`, `var_name='month'`, and `value_name='deliveries'`. Print the result.\n\nThe result should have one row per city-month combination.\n\nUse only `df.melt(id_vars=[...])`, `pd.melt(df, id_vars=[...])`, `var_name='month'`, `value_name='value'`, and `print()`.",
    },
    
    # 5. ix.tile_pandas_concat_merge.s04: Fix variable names to match starter
    'ix.tile_pandas_concat_merge.s04': {
        'solution': '''import pandas as pd

jan_orders = pd.read_csv('jan_orders.csv')
feb_orders = pd.read_csv('feb_orders.csv')
mar_orders = pd.read_csv('mar_orders.csv')

result = pd.concat([jan_orders, feb_orders, mar_orders])

print(result)
'''
    },
    
    # 6. ix.tile_pandas_concat_merge.s10: Keep scaffolding exact
    'ix.tile_pandas_concat_merge.s10': {
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')

result = orders.merge(customers, on='customer_id')

print(result)
'''
    },
    
    # 7. ix.tile_pandas_pivot_export.s05: Keep scaffolding exact
    'ix.tile_pandas_pivot_export.s05': {
        'solution': '''import pandas as pd

product_sales = pd.read_csv('product_sales.csv')

result = product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum')

print(result)
'''
    },
    
    # 8. ix.tile_pandas_pivot_export.s08: Remove .columns.tolist(), just print df
    'ix.tile_pandas_pivot_export.s08': {
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

orders.to_csv('cleaned_orders.csv', index=False)

result = pd.read_csv('cleaned_orders.csv')

print(result)
''',
        'prompt': "The `orders` DataFrame is loaded. Export it to a CSV file named `cleaned_orders.csv` with `index=False` (no row numbers), then read it back with `pd.read_csv()` and print it to verify.\n\nUse only `df.to_csv(path)`, `df.to_csv(path, index=False)`, `pd.read_csv(path)`, and `print()`.",
    },
}

# Apply fixes
for tile in data['tiles']:
    for interaction_obj in tile['interactions']:
        ix_id = interaction_obj['interaction']['interaction_id']
        if ix_id in fixes:
            fix = fixes[ix_id]
            interaction = interaction_obj['interaction']
            
            # Update solution
            if 'solution' in fix:
                for sf in interaction.get('grading', {}).get('solution_files', []):
                    sf['content'] = fix['solution']
            
            # Update prompt if needed
            if 'prompt' in fix:
                interaction['public']['prompt'] = fix['prompt']

# Write back
with open('interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Applied all fixes")
