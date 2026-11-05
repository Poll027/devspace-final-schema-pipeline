#!/usr/bin/env python3
"""Patch interactions.part.c3.json to fix gate errors - v3."""
import json

with open('batches/final_batch_009_da_pandas/interactions.part.c3.json') as f:
    data = json.load(f)

# Fix tile_pandas_map_apply.s07
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_map_apply':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_map_apply.s07':
                # Update starter - include the function
                ix['interaction']['public']['workspace']['files'][0]['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders

speed_map = {False: 'fast', True: 'slow'}
threshold = 25
col = 'speed_label'
time_col = 'delivery_time_minutes'
axis_val = 1

def label_speed(row):
    return speed_map[row[time_col] > threshold]

# Apply label_speed row-wise (axis=axis_val) and store in orders[col]

print(orders[col])
"""
                # Update solution - same function
                ix['interaction']['grading']['solution_files'][0]['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders

speed_map = {False: 'fast', True: 'slow'}
threshold = 25
col = 'speed_label'
time_col = 'delivery_time_minutes'
axis_val = 1

def label_speed(row):
    return speed_map[row[time_col] > threshold]

orders[col] = df.apply(label_speed, axis=axis_val)

print(orders[col])
"""
                # Revert allowed_syntax to glossary verbatim
                ix['interaction']['public']['constraints']['allowed_syntax'] = [
                    "def function(row): ...",
                    "df.apply(function, axis=1)",
                    "df['new'] = ...",
                    "print()"
                ]
                # Update prompt
                ix['interaction']['public']['prompt'] = "Use `.apply()` with `axis=1` to create a new column `speed_label` by applying the `label_speed` function row-wise. Then print the `speed_label` column.\n\nThe `label_speed` function is already defined. Apply it to `df` with `axis=axis_val` and store the result in `orders[col]`.\n\nUse only `df.apply(function, axis=1)`, `df['new'] = ...`, and `print()`."

# Fix tile_pandas_groupby_melt.s05
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_groupby_melt':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_groupby_melt.s05':
                # Revert allowed_syntax to glossary verbatim
                ix['interaction']['public']['constraints']['allowed_syntax'] = [
                    "df.groupby('key')['col'].sum()",
                    "df.groupby('key')['col'].mean()",
                    "df.groupby('key')['col'].agg([...])",
                    "print()"
                ]

# Fix tile_pandas_concat_merge.s10
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_concat_merge':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_concat_merge.s10':
                # Update starter
                ix['interaction']['public']['workspace']['files'][0]['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')
df = orders

on_col = 'customer_id'

# Merge df with customers on on_col
# Store in result

print(result)
"""
                # Update solution
                ix['interaction']['grading']['solution_files'][0]['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')
df = orders

on_col = 'customer_id'

result = df.merge(customers, on=on_col)

print(result)
"""
                # Update expected (14 rows instead of 8)
                ix['interaction']['grading']['tests'][0]['spec']['expected']['rows'] = [
                    [301, "Ngozi Eze", "Individual"],
                    [302, "Emeka Obi", "Business"],
                    [303, "Fatima Musa", "Individual"],
                    [304, "Tunde Bakare", "Business"],
                    [305, "Amaka Nwosu", "Individual"],
                    [306, "Yusuf Garba", "Business"],
                    [307, "Chisom Ike", "Individual"],
                    [308, "Bisi Adewale", "Business"],
                    [309, "Halima Sule", "Individual"],
                    [310, "Rotimi Coker", "Business"],
                    [311, "Nkechi Okafor", "Individual"],
                    [312, "Musa Ibrahim", "Business"],
                    [313, "Adaeze Chukwu", "Individual"],
                    [314, "Segun Afolabi", "Business"]
                ]

# Fix tile_pandas_pivot_export.s05
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_pivot_export':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_pivot_export.s05':
                # Update starter
                ix['interaction']['public']['workspace']['files'][0]['content'] = """import pandas as pd

product_sales = pd.read_csv('product_sales.csv')
df = product_sales

idx = 'product'
cols = 'month'
vals = 'sales'
func = 'sum'

# Create a pivot table: index=idx, columns=cols, values=vals, aggfunc=func
# Store in result

print(result)
"""
                # Update solution
                ix['interaction']['grading']['solution_files'][0]['content'] = """import pandas as pd

product_sales = pd.read_csv('product_sales.csv')
df = product_sales

idx = 'product'
cols = 'month'
vals = 'sales'
func = 'sum'

result = df.pivot_table(index=idx, columns=cols, values=vals, aggfunc=func)

print(result)
"""
                # Replace t2 with dataframe_equals
                ix['interaction']['grading']['tests'] = [
                    {
                        "test_id": "t1",
                        "kind": "dataframe_equals",
                        "spec": {
                            "expr": "df.pivot_table(index='product', columns='month', values='sales', aggfunc='sum').reset_index()",
                            "expected": {
                                "columns": ["product", "Feb", "Jan", "Mar"],
                                "rows": [
                                    ["Document", 2400, 2100, 4200],
                                    ["Envelope", 5100, 7700, 4800],
                                    ["Parcel", 16700, 8200, 8800]
                                ]
                            }
                        },
                        "visible": True,
                        "message_on_fail": "The pivot table should have one row per product, one column per month, with summed sales."
                    }
                ]

# Fix tile_pandas_pivot_export.s08
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_pivot_export':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_pandas_pivot_export.s08':
                # Update starter
                ix['interaction']['public']['workspace']['files'][0]['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders

out_path = 'cleaned_orders.csv'
no_index = False

# Export df to out_path with index=no_index
# Then read it back into result and print

print(result)
"""
                # Update solution
                ix['interaction']['grading']['solution_files'][0]['content'] = """import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders

out_path = 'cleaned_orders.csv'
no_index = False

df.to_csv(out_path, index=no_index)

result = pd.read_csv(out_path)

print(result)
"""
                # Replace t1, t2 with data-dependent tests
                ix['interaction']['grading']['tests'] = [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "len(pd.read_csv('cleaned_orders.csv'))",
                            "expected": 14
                        },
                        "visible": True,
                        "message_on_fail": "The CSV should have 14 rows (the same as the original orders DataFrame)."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "pd.read_csv('cleaned_orders.csv')['order_id'].iloc[0]",
                            "expected": 1001
                        },
                        "visible": True,
                        "message_on_fail": "The first order_id should be 1001."
                    }
                ]

with open('batches/final_batch_009_da_pandas/interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patched interactions.part.c3.json")
