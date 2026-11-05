"""
Patch interactions.json (merged) with the same fixes as interactions.part.c2.json
"""
import json

with open('batches/final_batch_009_da_pandas/interactions.json') as f:
    data = json.load(f)

# ── ADVISORY fix: tile_pandas_dtype_datetime/s03/opt_c feedback ──────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_dtype_datetime':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_pandas_dtype_datetime.s03':
                ix = item['interaction']
                ix['grading']['option_feedback']['opt_c']['message'] = (
                    "These calls produce converted copies but never assign them back, "
                    "so the DataFrame is unchanged. Use `astype()` with a dict to convert "
                    "both columns in one call: `orders.astype({'distance_km': float, 'order_id': str})`."
                )
                print("Fixed tile_pandas_dtype_datetime/s03/opt_c feedback in interactions.json")

# ── BLOCKING fix: tile_pandas_descriptive_stats/s04 ──────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_descriptive_stats':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_pandas_descriptive_stats.s04':
                ix = item['interaction']

                # 1. Update prompt
                ix['public']['prompt'] = (
                    "The `df` DataFrame has a `delivery_time_minutes` column. "
                    "Calculate the mean, median, and standard deviation of the `delivery_time_minutes` column. "
                    "Store the results in `mean_val`, `median_val`, and `std_val` and print each. "
                    "Then call `describe()` on the column, store the result in `desc`, and print it. "
                    "In a comment, state what the standard deviation tells you about delivery times.\n\n"
                    "Use only `df['col'].mean()`, `df['col'].median()`, `df['col'].std()`, "
                    "`df['col'].describe()`, and `print()`."
                )
                print("Updated s04 prompt in interactions.json")

                # 2. Update starter
                ix['public']['workspace']['files'][0]['content'] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders.csv')\n\n"
                    "# TODO: Calculate mean, median, and std\n"
                    "mean_val = None  # TODO: replace with df['delivery_time_minutes'].mean()\n"
                    "median_val = None  # TODO: replace with df['delivery_time_minutes'].median()\n"
                    "std_val = None  # TODO: replace with df['delivery_time_minutes'].std()\n\n"
                    "# TODO: Call describe() on the column, store in desc, and print\n"
                    "# desc = ...\n\n"
                    "# TODO: In a comment, state what the std tells you about delivery times\n"
                    "# e.g. # The std of X minutes means ...\n"
                )
                print("Updated s04 starter in interactions.json")

                # 3. Update solution
                ix['grading']['solution_files'][0]['content'] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders.csv')\n\n"
                    "# Calculate mean, median, and std\n"
                    "mean_val = df['delivery_time_minutes'].mean()\n"
                    "median_val = df['delivery_time_minutes'].median()\n"
                    "std_val = df['delivery_time_minutes'].std()\n\n"
                    "print(mean_val)\n"
                    "print(median_val)\n"
                    "print(std_val)\n\n"
                    "# Call describe() on the column\n"
                    "desc = df['delivery_time_minutes'].describe()\n"
                    "print(desc)\n\n"
                    "# The std of ~15.6 minutes means delivery times typically vary\n"
                    "# about 15.6 minutes from the mean of 29.0 minutes.\n"
                )
                print("Updated s04 solution in interactions.json")

                # 4. Add test t4 for round(desc['mean'], 1) == 29.0
                existing_test_ids = {t['test_id'] for t in ix['grading']['tests']}
                if 't4' not in existing_test_ids:
                    ix['grading']['tests'].append({
                        "test_id": "t4",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "round(desc['mean'], 1)",
                            "expected": 29.0
                        },
                        "visible": True,
                        "message_on_fail": "desc should be the describe() output for delivery_time_minutes. Check that you called df['delivery_time_minutes'].describe() and stored it in desc."
                    })
                    print("Added t4 test in interactions.json")

                # Also ensure t3 is present (std test)
                if 't3' not in existing_test_ids:
                    ix['grading']['tests'].append({
                        "kind": "value_equals",
                        "spec": {
                            "expr": "round(std_val, 1)",
                            "expected": 15.6
                        },
                        "test_id": "t3",
                        "message_on_fail": "The standard deviation should be approximately 15.6. Check that you computed it correctly.",
                        "visible": True
                    })
                    print("Added t3 test in interactions.json")

                # 5. Update feedback
                ix['feedback']['correct']['message'] = (
                    "Excellent! You computed the key descriptive statistics and called describe() "
                    "to see the full summary."
                )
                ix['feedback']['incorrect']['message'] = (
                    "Not quite. Make sure you compute mean, median, std, call describe() on the column, "
                    "and store the result in desc."
                )
                ix['feedback']['hints'] = [
                    "Call `.mean()`, `.median()`, `.std()`, and `.describe()` on the delivery_time_minutes column.",
                    "Store the describe() result in `desc` so the test can check `desc['mean']`."
                ]
                print("Updated s04 feedback in interactions.json")

with open('batches/final_batch_009_da_pandas/interactions.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch of interactions.json complete.")
