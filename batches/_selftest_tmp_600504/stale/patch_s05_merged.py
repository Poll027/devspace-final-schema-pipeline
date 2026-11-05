"""
Patch the merged interactions.json and gate interactions.json for tile_pandas_groupby_melt.s05
"""
import json, copy

def patch_s05(data):
    for tile in data['tiles']:
        if tile['tile_id'] == 'tile_pandas_groupby_melt':
            for ix_entry in tile['interactions']:
                if ix_entry['step_id'] == 'tile_pandas_groupby_melt.s05':
                    ix = ix_entry['interaction']

                    ix['public']['prompt'] = (
                        "The `orders` DataFrame has `city` and `order_value` columns. "
                        "Use `groupby('city')` to compute both the sum and mean of `order_value` "
                        "for each city in one call using `.agg(['sum', 'mean'])`. Print the result.\n\n"
                        "The city names should form the index of the result.\n\n"
                        "Use only `df.groupby('key')['col'].sum()`, "
                        "`df.groupby('key')['col'].mean()`, "
                        "`df.groupby('key')['col'].agg([...])`, and `print()`."
                    )

                    starter_content = (
                        "import pandas as pd\n\n"
                        "orders = pd.read_csv('orders.csv')\n\n"
                        "df = orders.groupby('city')['order_value']\n"
                        "agg_funcs = ['sum', 'mean']\n"
                        "# Use .agg(agg_funcs) on df to compute both aggregations\n"
                        "# Store in result\n\n"
                        "print(result)\n"
                    )
                    ix['public']['workspace']['files'][0]['content'] = starter_content

                    solution_content = (
                        "import pandas as pd\n\n"
                        "orders = pd.read_csv('orders.csv')\n\n"
                        "df = orders.groupby('city')['order_value']\n"
                        "agg_funcs = ['sum', 'mean']\n"
                        "result = df.agg(agg_funcs)\n\n"
                        "print(result)\n"
                    )
                    ix['grading']['solution_files'][0]['content'] = solution_content

                    ix['grading']['tests'] = [
                        {
                            "test_id": "t1",
                            "kind": "dataframe_equals",
                            "spec": {
                                "expr": "result",
                                "expected": {
                                    "columns": ["sum", "mean"],
                                    "rows": [
                                        [19700.0, 3940.0],
                                        [7100.0,  1775.0],
                                        [16400.0, 3280.0]
                                    ]
                                }
                            },
                            "visible": True,
                            "message_on_fail": "The result should have one row per city with sum and mean of order_value."
                        }
                    ]

                    ix['feedback']['correct']['message'] = (
                        "Perfect! You computed multiple aggregations in one call, "
                        "and the city names form the index."
                    )
                    ix['feedback']['incorrect']['message'] = (
                        "Not quite. Make sure you use `.agg(['sum', 'mean'])` on "
                        "`orders.groupby('city')['order_value']` to compute both aggregations."
                    )
                    ix['feedback']['hints'] = [
                        "Use `orders.groupby('city')['order_value'].agg(['sum', 'mean'])` "
                        "to compute both aggregations in one call."
                    ]
                    return True
    return False

# Patch main merged interactions.json
for path in [
    'batches/final_batch_009_da_pandas/interactions.json',
    'batches/final_batch_009_da_pandas/working/gate_04_interactions_c3/interactions.json',
]:
    with open(path) as f:
        data = json.load(f)
    result = patch_s05(data)
    if result:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
            f.write('\n')
        print(f"Patched: {path}")
    else:
        print(f"NOT FOUND in: {path}")
