"""
Patch interactions.part.c2.json to fix the errors reported by validate_tile.py:

1. tile_pandas_descriptive_stats.s04:
   - Fix starter to be valid Python (replace 'mean_val = # TODO' with 'mean_val = None  # TODO')
   - Fix spec.expected for t3 from 17.5 to 15.6
   - Fix message_on_fail for t3
   - Add 'interpret_mean_and_std_in_context' to measures and anchors

2. tile_pandas_text_dupes_missing.s11:
   - Add 'drop_rows_missing_required_field' to measures and anchors
   - Update solution to include df.dropna(subset=['order_id']) call
   - Update prompt to mention the dropna step
"""
import json

path = "batches/final_batch_009_da_pandas/interactions.part.c2.json"
with open(path) as f:
    data = json.load(f)

for tile in data["tiles"]:
    # ---- Fix tile_pandas_descriptive_stats ----
    if tile["tile_id"] == "tile_pandas_descriptive_stats":
        for entry in tile["interactions"]:
            if entry["step_id"] == "tile_pandas_descriptive_stats.s04":
                ix = entry["interaction"]

                # Fix 1: Add interpret_mean_and_std_in_context to measures
                ix["measures"].append({
                    "concept_id": "stats.pandas_descriptive_stats",
                    "capability": "interpret_mean_and_std_in_context",
                    "fact_ids": ["f1", "f2"]
                })

                # Fix 2: Add to anchors
                if "stats.pandas_descriptive_stats#assessment:interpret_mean_and_std_in_context" not in ix["anchors"]:
                    ix["anchors"].append("stats.pandas_descriptive_stats#assessment:interpret_mean_and_std_in_context")

                # Fix 3: Fix the starter to be valid Python
                # Replace 'mean_val = # TODO' etc. with 'mean_val = None  # TODO'
                old_starter = ix["public"]["workspace"]["files"][0]["content"]
                new_starter = old_starter.replace(
                    "mean_val = # TODO\nmedian_val = # TODO\nstd_val = # TODO\n",
                    "mean_val = None  # TODO: replace with df['delivery_time_minutes'].mean()\nmedian_val = None  # TODO: replace with df['delivery_time_minutes'].median()\nstd_val = None  # TODO: replace with df['delivery_time_minutes'].std()\n"
                )
                ix["public"]["workspace"]["files"][0]["content"] = new_starter

                # Fix 4: Fix spec.expected for t3 from 17.5 to 15.6
                for test in ix["grading"]["tests"]:
                    if test["test_id"] == "t3":
                        test["spec"]["expected"] = 15.6
                        test["message_on_fail"] = "The standard deviation should be approximately 15.6. Check that you computed it correctly."

    # ---- Fix tile_pandas_text_dupes_missing ----
    if tile["tile_id"] == "tile_pandas_text_dupes_missing":
        for entry in tile["interactions"]:
            if entry["step_id"] == "tile_pandas_text_dupes_missing.s11":
                ix = entry["interaction"]

                # Fix 5: Add drop_rows_missing_required_field to measures
                ix["measures"].append({
                    "concept_id": "pandas.missing_data_handling",
                    "capability": "drop_rows_missing_required_field",
                    "fact_ids": ["f2"]
                })

                # Fix 6: Add to anchors
                if "pandas.missing_data_handling#assessment:drop_rows_missing_required_field" not in ix["anchors"]:
                    ix["anchors"].append("pandas.missing_data_handling#assessment:drop_rows_missing_required_field")

                # Fix 7: Update prompt to mention dropna step
                ix["public"]["prompt"] = (
                    "The `df` DataFrame has a missing value in `delivery_time_minutes`. "
                    "Print `df['delivery_time_minutes'].isna()` to detect the gap. "
                    "Then drop rows missing the required `order_id` field using `dropna()`. "
                    "Finally, print the `delivery_time_minutes` column with the missing value filled by the column median using `fillna()` and `median()`.\n\n"
                    "Use only `df['col'].isna()`, `df.dropna(subset=[...])`, `df['col'].fillna(value)`, `df['col'].median()`, and `print()`."
                )

                # Fix 8: Update starter to include dropna step
                ix["public"]["workspace"]["files"][0]["content"] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders_messy.csv')\n\n"
                    "# TODO: Print isna() to detect missing delivery_time_minutes\n\n"
                    "# TODO: Drop rows missing the required order_id field\n\n"
                    "# TODO: Print the column with missing value filled by its median\n"
                )

                # Fix 9: Update solution to include dropna step
                ix["grading"]["solution_files"][0]["content"] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders_messy.csv')\n\n"
                    "# Print isna() to detect missing delivery_time_minutes\n"
                    "print(df['delivery_time_minutes'].isna())\n\n"
                    "# Drop rows missing the required order_id field\n"
                    "df = df.dropna(subset=['order_id'])\n\n"
                    "# Print the column with missing value filled by its median\n"
                    "print(df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median()))\n"
                )

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Patch applied successfully.")
