#!/usr/bin/env python3
"""
Comprehensive patch for interactions.part.c3.json to fix all validation errors.
"""
import json

# Load the interactions file
with open('interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Track changes
changes = []

# Fix each problematic interaction
for tile in data['tiles']:
    tile_id = tile['tile_id']
    
    for interaction_obj in tile['interactions']:
        step_id = interaction_obj['step_id']
        interaction = interaction_obj['interaction']
        ix_id = interaction['interaction_id']
        
        # Fix ix.tile_pandas_map_apply.s03
        if ix_id == 'ix.tile_pandas_map_apply.s03':
            # Ensure allowed_syntax matches glossary exactly
            interaction['public']['constraints']['allowed_syntax'] = [
                "df['col'].map(function)",
                "df['col'].map(dict)",
                "df['new'] = ...",
                "print()"
            ]
            # Solution should match starter scaffolding exactly
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

orders = pd.read_csv('orders.csv')

city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}

orders['city_name'] = orders['city_code'].map(city_lookup)

print(orders['city_name'])
'''
            changes.append(f"{ix_id}: Fixed allowed_syntax and solution")
        
        # Fix ix.tile_pandas_map_apply.s07
        elif ix_id == 'ix.tile_pandas_map_apply.s07':
            # Ensure allowed_syntax matches glossary (def, not lambda)
            interaction['public']['constraints']['allowed_syntax'] = [
                "def function(row): ...",
                "df.apply(function, axis=1)",
                "df['new'] = ...",
                "print()"
            ]
            # Solution uses def, not lambda
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

orders = pd.read_csv('orders.csv')

def label_speed(row):
    if row['delivery_time_minutes'] > 25:
        return 'slow'
    else:
        return 'fast'

orders['speed_label'] = orders.apply(label_speed, axis=1)

print(orders['speed_label'])
'''
            changes.append(f"{ix_id}: Fixed allowed_syntax to use def instead of lambda")
        
        # Fix ix.tile_pandas_groupby_melt.s05
        elif ix_id == 'ix.tile_pandas_groupby_melt.s05':
            # Solution should match starter scaffolding
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

orders = pd.read_csv('orders.csv')

result = orders.groupby('customer_id')['order_value'].agg(['sum', 'mean'])

print(result)
'''
            changes.append(f"{ix_id}: Fixed solution to match starter")
        
        # Fix ix.tile_pandas_groupby_melt.s09
        elif ix_id == 'ix.tile_pandas_groupby_melt.s09':
            # Fix dataset name to match starter (city_deliveries, not sales)
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

city_deliveries = pd.read_csv('city_deliveries.csv')

result = city_deliveries.melt(id_vars='city', var_name='month', value_name='deliveries')

print(result)
'''
            # Update prompt to match
            interaction['public']['prompt'] = "The `city_deliveries` DataFrame has a `city` column and three month columns (`jan`, `feb`, `mar`). Use `.melt()` to reshape it to long format with `id_vars='city'`, `var_name='month'`, and `value_name='deliveries'`. Print the result.\n\nThe result should have one row per city-month combination.\n\nUse only `df.melt(id_vars=[...])`, `pd.melt(df, id_vars=[...])`, `var_name='month'`, `value_name='value'`, and `print()`."
            changes.append(f"{ix_id}: Fixed dataset name to city_deliveries")
        
        # Fix ix.tile_pandas_concat_merge.s04
        elif ix_id == 'ix.tile_pandas_concat_merge.s04':
            # Fix variable names to match starter (jan_orders, not jan)
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

jan_orders = pd.read_csv('jan_orders.csv')
feb_orders = pd.read_csv('feb_orders.csv')
mar_orders = pd.read_csv('mar_orders.csv')

result = pd.concat([jan_orders, feb_orders, mar_orders])

print(result)
'''
            changes.append(f"{ix_id}: Fixed variable names to match starter")
        
        # Fix ix.tile_pandas_concat_merge.s10
        elif ix_id == 'ix.tile_pandas_concat_merge.s10':
            # Solution should match starter scaffolding
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')

result = orders.merge(customers, on='customer_id')

print(result)
'''
            changes.append(f"{ix_id}: Fixed solution to match starter")
        
        # Fix ix.tile_pandas_pivot_export.s05
        elif ix_id == 'ix.tile_pandas_pivot_export.s05':
            # Solution should match starter scaffolding
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

product_sales = pd.read_csv('product_sales.csv')

result = product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum')

print(result)
'''
            # Remove remediation_step_id (it teaches wrong facts)
            if 'remediation_step_id' in interaction.get('feedback', {}):
                del interaction['feedback']['remediation_step_id']
                changes.append(f"{ix_id}: Removed mismatched remediation_step_id")
            changes.append(f"{ix_id}: Fixed solution to match starter")
        
        # Fix ix.tile_pandas_pivot_export.s08
        elif ix_id == 'ix.tile_pandas_pivot_export.s08':
            # Remove .columns.tolist() - just print the dataframe
            for sf in interaction.get('grading', {}).get('solution_files', []):
                sf['content'] = '''import pandas as pd

orders = pd.read_csv('orders.csv')

orders.to_csv('cleaned_orders.csv', index=False)

result = pd.read_csv('cleaned_orders.csv')

print(result)
'''
            # Update prompt
            interaction['public']['prompt'] = "The `orders` DataFrame is loaded. Export it to a CSV file named `cleaned_orders.csv` with `index=False` (no row numbers), then read it back with `pd.read_csv()` and print it to verify.\n\nUse only `df.to_csv(path)`, `df.to_csv(path, index=False)`, `pd.read_csv(path)`, and `print()`."
            changes.append(f"{ix_id}: Removed .columns.tolist() from solution")

# Write back
with open('interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Applied {len(changes)} fixes:")
for change in changes:
    print(f"  - {change}")
