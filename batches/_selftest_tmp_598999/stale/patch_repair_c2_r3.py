"""
Repair round patch for interactions.part.c2.json
BLOCKING: tile_pandas_descriptive_stats/s04 - add describe() call + interpretation
ADVISORY: tile_pandas_dtype_datetime/s03/opt_c - fix feedback about non-persisting calls
"""
import json, copy

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json') as f:
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
                print("Fixed tile_pandas_dtype_datetime/s03/opt_c feedback")

# ── BLOCKING fix: tile_pandas_descriptive_stats/s04 ──────────────────────────
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_descriptive_stats':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_pandas_descriptive_stats.s04':
                ix = item['interaction']

                # 1. Update prompt to include describe() call and std interpretation
                old_prompt = ix['public']['prompt']
                new_prompt = (
                    "The `df` DataFrame has a `delivery_time_minutes` column. "
                    "Calculate the mean, median, and standard deviation of the `delivery_time_minutes` column. "
                    "Store the results in `mean_val`, `median_val`, and `std_val` and print each. "
                    "Then call `describe()` on the column, store the result in `desc`, and print it. "
                    "In a comment, state what the standard deviation tells you about delivery times.\n\n"
                    "Use only `df['col'].mean()`, `df['col'].median()`, `df['col'].std()`, "
                    "`df['col'].describe()`, and `print()`."
                )
                ix['public']['prompt'] = new_prompt
                print("Updated s04 prompt")

                # 2. Update starter to include desc placeholder
                old_starter = ix['public']['workspace']['files'][0]['content']
                new_starter = (
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
                ix['public']['workspace']['files'][0]['content'] = new_starter
                print("Updated s04 starter")

                # 3. Update solution to include describe() call
                new_solution = (
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
                ix['grading']['solution_files'][0]['content'] = new_solution
                print("Updated s04 solution")

                # 4. Add test for round(desc['mean'], 1) == 29.0
                existing_test_ids = {t['test_id'] for t in ix['grading']['tests']}
                new_test = {
                    "test_id": "t4",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "round(desc['mean'], 1)",
                        "expected": 29.0
                    },
                    "visible": True,
                    "message_on_fail": "desc should be the describe() output for delivery_time_minutes. Check that you called df['delivery_time_minutes'].describe() and stored it in desc."
                }
                if 't4' not in existing_test_ids:
                    ix['grading']['tests'].append(new_test)
                    print("Added t4 test for desc['mean']")
                else:
                    print("t4 already exists, skipping")

                # 5. Update feedback messages to reflect describe() requirement
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
                print("Updated s04 feedback")

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch complete.")
