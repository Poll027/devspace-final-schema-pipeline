"""
Patch interactions.part.c2.json and screens.part.c2.json to fix gate errors.
"""
import json, copy

# ── interactions.part.c2.json ──────────────────────────────────────────────
with open('batches/final_batch_009_da_pandas/interactions.part.c2.json') as f:
    ix_data = json.load(f)

for tile in ix_data['tiles']:
    tid = tile['tile_id']

    # ── tile_pandas_dtype_datetime ─────────────────────────────────────────
    if tid == 'tile_pandas_dtype_datetime':
        for ix in tile['interactions']:
            sid = ix['step_id']

            # s04: t1 is hard-coded (stdout_equals "float64" never changes)
            # Fix: change to value_equals checking actual column values
            if sid == 'tile_pandas_dtype_datetime.s04':
                tests = ix['interaction']['grading']['tests']
                # Replace t1 with a data-dependent value_equals test
                tests[0] = {
                    "test_id": "t1",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "df['distance_km'].tolist()",
                        "expected": [4.2, 6.1, 5.5, 3.8, 7.3, 8.0, 12.4, 9.2, 4.9, 5.1, 10.0, 4.4, 6.6, 11.1]
                    },
                    "visible": True,
                    "message_on_fail": "The distance_km values should be floats after conversion. Check that you used astype(float)."
                }
                # Also update the solution to not just print dtype — keep it but
                # the test now checks the variable, not stdout
                # (solution is fine as-is; value_equals checks df['distance_km'])

            # s08: t1 and t2 are hard-coded (dtype strings never change with data)
            # t2 also has wrong expected ("int64" but actual is "int32")
            if sid == 'tile_pandas_dtype_datetime.s08':
                tests = ix['interaction']['grading']['tests']
                # t1: was value_equals str(df['pickup_date'].dtype) → always same string
                # Fix: check actual day values (data-dependent)
                tests[0] = {
                    "test_id": "t1",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "df['pickup_date'].dt.day.tolist()",
                        "expected": [14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20]
                    },
                    "visible": True,
                    "message_on_fail": "The pickup_date column should be datetime after conversion. Check that you used pd.to_datetime()."
                }
                # t2: was value_equals str(df['pickup_month'].dtype) expected "int64"
                # Fix: check actual month values (data-dependent); dtype is int32 not int64
                tests[1] = {
                    "test_id": "t2",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "df['pickup_month'].tolist()",
                        "expected": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
                    },
                    "visible": True,
                    "message_on_fail": "The pickup_month column should contain the month number extracted with .dt.month. Check that you used df['pickup_date'].dt.month."
                }

    # ── tile_pandas_text_dupes_missing ─────────────────────────────────────
    if tid == 'tile_pandas_text_dupes_missing':
        for ix in tile['interactions']:
            sid = ix['step_id']

            # s11: solution uses len() (call:len) and list literal (list_lit)
            # Fix: rewrite solution to use only allowed syntax
            # Allowed: df.isna(), df.notna(), df.dropna(subset=[...]),
            #          df['col'].fillna(value), df['col'].median(), print()
            # Strategy: detect missing with isna(), fill with fillna(median())
            # Use starter variable check_col for subset to avoid bare list_lit
            if sid == 'tile_pandas_text_dupes_missing.s11':
                interaction = ix['interaction']

                # Update prompt to match new task (fill instead of drop+len)
                interaction['public']['prompt'] = (
                    "The `df` DataFrame has a missing value in `delivery_time_minutes`. "
                    "First print `df['delivery_time_minutes'].isna()` to see the gap. "
                    "Then fill the missing value with the column's median using `fillna()`. "
                    "Print the filled column to verify.\n\n"
                    "Use only `df['col'].isna()`, `df['col'].fillna(value)`, "
                    "`df['col'].median()`, and `print()`."
                )

                # Update starter to not use check_col (keep it simple)
                interaction['public']['workspace']['files'][0]['content'] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders_messy.csv')\n\n"
                    "# TODO: Print isna() to detect missing delivery_time_minutes\n\n"
                    "# TODO: Fill missing delivery_time_minutes with its median\n\n"
                    "# TODO: Print the filled column\n"
                )

                # Update solution: only uses allowed syntax
                interaction['grading']['solution_files'][0]['content'] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders_messy.csv')\n\n"
                    "# Print isna() to detect missing delivery_time_minutes\n"
                    "print(df['delivery_time_minutes'].isna())\n\n"
                    "# Fill missing delivery_time_minutes with its median\n"
                    "df['delivery_time_minutes'] = df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median())\n\n"
                    "# Print the filled column\n"
                    "print(df['delivery_time_minutes'])\n"
                )

                # Update tests: data-dependent, no len(), no list_lit
                # After fillna, isna().sum() == 0 and values are data-dependent
                interaction['grading']['tests'] = [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['delivery_time_minutes'].isna().sum()",
                            "expected": 0
                        },
                        "visible": True,
                        "message_on_fail": "After filling, delivery_time_minutes should have no missing values. Check that you used fillna(df['delivery_time_minutes'].median())."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['delivery_time_minutes'].tolist()",
                            "expected": [18.0, 20.0, 22.0, 22.0, 26.0, 28.0, 80.0, 23.0, 19.0, 24.0, 33.0, 21.0, 27.0, 35.0, 22.0]
                        },
                        "visible": True,
                        "message_on_fail": "The missing delivery_time_minutes should be filled with the median (23.0). Check your fillna() call."
                    }
                ]

                # Update feedback to match new task
                interaction['feedback']['correct']['message'] = (
                    "Perfect! You detected the missing value with isna() and filled it with the column median."
                )
                interaction['feedback']['incorrect']['message'] = (
                    "Not quite. Make sure you use `df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median())`."
                )
                interaction['feedback']['hints'] = [
                    "Use `df['delivery_time_minutes'].isna()` to see the gap, then `fillna(df['delivery_time_minutes'].median())` to fill it."
                ]

with open('batches/final_batch_009_da_pandas/interactions.part.c2.json', 'w') as f:
    json.dump(ix_data, f, indent=2)
print("interactions.part.c2.json patched")

# ── screens.part.c2.json ───────────────────────────────────────────────────
with open('batches/final_batch_009_da_pandas/screens.part.c2.json') as f:
    sc_data = json.load(f)

for tile in sc_data['tiles']:
    tid = tile['tile_id']

    # ── tile_pandas_text_dupes_missing ─────────────────────────────────────
    if tid == 'tile_pandas_text_dupes_missing':
        for step in tile['steps']:
            sid = step['step_id']

            # s05: data_table uses ds_orders (base) but highlights occurrence:1 of 1003
            # The base dataset has only one row with order_id=1003, so occurrence:1 doesn't exist
            # Fix: use orders_messy variant which has the duplicate
            if sid == 'tile_pandas_text_dupes_missing.s05':
                for block in step.get('blocks', []):
                    if block.get('type') == 'before_after':
                        before = block.get('before', {})
                        if before.get('type') == 'data_table':
                            asset_ref = before.get('asset_ref', {})
                            if asset_ref.get('asset_id') == 'ds_orders' and 'variant_id' not in asset_ref:
                                # Add variant_id to use the messy variant with the duplicate
                                asset_ref['variant_id'] = 'orders_messy'
                                print(f"Fixed s05 data_table: added variant_id=orders_messy")

            # s12: lineage.teaching_block_ids has extra pandas.drop_duplicates#tb3
            # Plan expects only ['pandas.str_accessor_cleaning#tb3', 'pandas.missing_data_handling#tb5']
            if sid == 'tile_pandas_text_dupes_missing.s12':
                planned = ['pandas.str_accessor_cleaning#tb3', 'pandas.missing_data_handling#tb5']
                # Fix step-level lineage
                if 'lineage' in step:
                    step['lineage']['teaching_block_ids'] = planned
                    print(f"Fixed s12 step lineage.teaching_block_ids")
                # Fix block-level lineage too
                for block in step.get('blocks', []):
                    if 'lineage' in block:
                        # Remove pandas.drop_duplicates#tb3 from block lineage
                        tids = block['lineage'].get('teaching_block_ids', [])
                        new_tids = [t for t in tids if t != 'pandas.drop_duplicates#tb3']
                        if new_tids != tids:
                            block['lineage']['teaching_block_ids'] = new_tids
                            print(f"Fixed s12 block {block.get('block_id')} lineage.teaching_block_ids")

    # ── tile_pandas_descriptive_stats ──────────────────────────────────────
    if tid == 'tile_pandas_descriptive_stats':
        for step in tile['steps']:
            sid = step['step_id']

            # s01: needs annotated_image or diagram block
            # No image assets registered, so use diagram
            if sid == 'tile_pandas_descriptive_stats.s01':
                blocks = step.get('blocks', [])
                # Check if already has annotated_image or diagram
                has_visual = any(b['type'] in ('annotated_image', 'diagram') for b in blocks)
                if not has_visual:
                    # Add a diagram block showing describe() output rows mapped to meaning
                    # Use a mapping diagram: describe() rows on left, meaning on right
                    diagram_block = {
                        "type": "diagram",
                        "block_id": "tile_pandas_descriptive_stats.s01.b5",
                        "diagram_kind": "mapping",
                        "title": "describe() output for delivery_time_minutes — key rows labelled",
                        "nodes": [
                            {"id": "d_mean",   "label": "mean   30.86",  "kind": "describe_row"},
                            {"id": "d_std",    "label": "std    21.93",  "kind": "describe_row"},
                            {"id": "d_min",    "label": "min    18.00",  "kind": "describe_row"},
                            {"id": "d_50",     "label": "50%    22.00",  "kind": "describe_row"},
                            {"id": "d_max",    "label": "max    80.00",  "kind": "describe_row"},
                            {"id": "m_mean",   "label": ".mean() → 30.86",  "kind": "method_result"},
                            {"id": "m_std",    "label": ".std()  → 21.93",  "kind": "method_result"},
                            {"id": "m_min",    "label": "minimum value",     "kind": "method_result"},
                            {"id": "m_median", "label": ".median() → 22.00", "kind": "method_result"},
                            {"id": "m_max",    "label": "maximum value",     "kind": "method_result"}
                        ],
                        "edges": [
                            {"from": "d_mean", "to": "m_mean",   "label": "average delivery time"},
                            {"from": "d_std",  "to": "m_std",    "label": "typical spread"},
                            {"from": "d_min",  "to": "m_min",    "label": "fastest delivery"},
                            {"from": "d_50",   "to": "m_median", "label": "median (half above, half below)"},
                            {"from": "d_max",  "to": "m_max",    "label": "slowest delivery (outlier)"}
                        ],
                        "alt_text": (
                            "Mapping diagram: the five key rows of describe() output for "
                            "delivery_time_minutes (mean 30.86, std 21.93, min 18, 50% 22, max 80) "
                            "are connected by arrows to the matching single-method results "
                            "(.mean(), .std(), .median()) and to plain-language labels for the extremes."
                        ),
                        "lineage": {
                            "concept_ids": ["stats.pandas_descriptive_stats"],
                            "teaching_block_ids": [
                                "stats.pandas_descriptive_stats#tb2",
                                "stats.pandas_descriptive_stats#tb3"
                            ],
                            "fact_ids": [
                                "stats.pandas_descriptive_stats#f1",
                                "stats.pandas_descriptive_stats#f2"
                            ],
                            "anchors": ["stats.pandas_descriptive_stats#visual"]
                        }
                    }
                    blocks.append(diagram_block)
                    step['blocks'] = blocks
                    print(f"Added diagram block to s01")

with open('batches/final_batch_009_da_pandas/screens.part.c2.json', 'w') as f:
    json.dump(sc_data, f, indent=2)
print("screens.part.c2.json patched")
