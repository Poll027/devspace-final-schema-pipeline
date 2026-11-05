"""
Patch interactions.part.c3.json: fix tile_pandas_groupby_melt.s05
- Change groupby key from 'customer_id' to 'city'
- Keep aggregated column as 'order_value' (within allowed_syntax)
- Update prompt, starter, solution, tests, feedback, hints
- Expected values derived from running the solution on ds_orders data
"""
import json, copy

path = 'batches/final_batch_009_da_pandas/interactions.part.c3.json'
with open(path) as f:
    data = json.load(f)

# Find tile_pandas_groupby_melt / s05
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_groupby_melt':
        for ix_entry in tile['interactions']:
            if ix_entry['step_id'] == 'tile_pandas_groupby_melt.s05':
                ix = ix_entry['interaction']

                # --- public.prompt ---
                ix['public']['prompt'] = (
                    "The `orders` DataFrame has `city` and `order_value` columns. "
                    "Use `groupby('city')` to compute both the sum and mean of `order_value` "
                    "for each city in one call using `.agg(['sum', 'mean'])`. Print the result.\n\n"
                    "The city names should form the index of the result.\n\n"
                    "Use only `df.groupby('key')['col'].sum()`, "
                    "`df.groupby('key')['col'].mean()`, "
                    "`df.groupby('key')['col'].agg([...])`, and `print()`."
                )

                # --- starter file ---
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

                # --- solution file ---
                solution_content = (
                    "import pandas as pd\n\n"
                    "orders = pd.read_csv('orders.csv')\n\n"
                    "df = orders.groupby('city')['order_value']\n"
                    "agg_funcs = ['sum', 'mean']\n"
                    "result = df.agg(agg_funcs)\n\n"
                    "print(result)\n"
                )
                ix['grading']['solution_files'][0]['content'] = solution_content

                # --- tests: expected values from running solution on ds_orders ---
                # groupby('city')['order_value'].agg(['sum','mean'])
                # Abuja: sum=19700, mean=3940.0
                # Kano:  sum=7100,  mean=1775.0
                # Lagos: sum=16400, mean=3280.0
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

                # --- feedback ---
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

                print("Patched tile_pandas_groupby_melt.s05 successfully.")
                break

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Written:", path)
