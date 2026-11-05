import json
import sys

# Load the interactions file
with open('interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Define comprehensive fixes
fixes = {
    'ix.tile_pandas_map_apply.s03': {
        # The solution is fine, just needs to match the starter
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

# Lookup dict for city codes
city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}

# Use .map(city_lookup) to create city_name column
orders['city_name'] = orders['city_code'].map(city_lookup)

# Print the city_name column
print(orders['city_name'])
''',
    },
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
''',
    },
    'ix.tile_pandas_groupby_melt.s05': {
        # Starter already loads orders, solution should use it
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

result = orders.groupby('customer_id')['order_value'].agg(['sum', 'mean'])

print(result)
''',
    },
    'ix.tile_pandas_groupby_melt.s09': {
        # Fix: use the same dataset name as the starter
        'solution': '''import pandas as pd

city_deliveries = pd.read_csv('city_deliveries.csv')

result = city_deliveries.melt(id_vars='city', var_name='month', value_name='deliveries')

print(result)
''',
        'prompt': "The `city_deliveries` DataFrame has a `city` column and three month columns (`jan`, `feb`, `mar`). Use `.melt()` to reshape it to long format with `id_vars='city'`, `var_name='month'`, and `value_name='deliveries'`. Print the result.\n\nThe result should have one row per city-month combination.\n\nUse only `df.melt(id_vars=[...])`, `pd.melt(df, id_vars=[...])`, `var_name='month'`, `value_name='value'`, and `print()`.",
    },
    'ix.tile_pandas_concat_merge.s04': {
        # Fix: use the same variable names as the starter
        'solution': '''import pandas as pd

jan_orders = pd.read_csv('jan_orders.csv')
feb_orders = pd.read_csv('feb_orders.csv')
mar_orders = pd.read_csv('mar_orders.csv')

result = pd.concat([jan_orders, feb_orders, mar_orders])

print(result)
''',
    },
    'ix.tile_pandas_concat_merge.s10': {
        # The solution looks fine, just ensure it matches the expected output
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')

result = orders.merge(customers, on='customer_id')

print(result)
''',
    },
    'ix.tile_pandas_pivot_export.s05': {
        # Solution looks fine
        'solution': '''import pandas as pd

product_sales = pd.read_csv('product_sales.csv')

result = product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum')

print(result)
''',
    },
    'ix.tile_pandas_pivot_export.s08': {
        # Need to avoid .columns.tolist() - just print the dataframe or use a simpler check
        'solution': '''import pandas as pd

orders = pd.read_csv('orders.csv')

orders.to_csv('cleaned_orders.csv', index=False)

result = pd.read_csv('cleaned_orders.csv')

print(result)
''',
        'prompt': "The `orders` DataFrame is loaded. Export it to a CSV file named `cleaned_orders.csv` with `index=False` (no row numbers), then read it back with `pd.read_csv()` and print it to verify.\n\nUse only `df.to_csv(path)`, `df.to_csv(path, index=False)`, `pd.read_csv(path) to check`, and `print()`.",
    },
}

# Apply fixes
for tile in data['tiles']:
    for interaction_obj in tile['interactions']:
        ix_id = interaction_obj['interaction']['interaction_id']
        if ix_id in fixes:
            fix = fixes[ix_id]
            interaction = interaction_obj['interaction']
            
            # Update solution content
            if 'solution' in fix:
                for sf in interaction.get('grading', {}).get('solution_files', []):
                    sf['content'] = fix['solution']
            
            # Update prompt if needed
            if 'prompt' in fix:
                interaction['public']['prompt'] = fix['prompt']

# Write back
with open('interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed interactions")
