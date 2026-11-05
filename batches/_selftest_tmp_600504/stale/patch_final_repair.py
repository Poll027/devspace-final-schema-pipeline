"""Apply all repair patches to screens.json and interactions.json, then re-assemble affected tiles."""
import json, copy, subprocess, sys
from pathlib import Path

B = Path('batches/final_batch_009_da_pandas')

# ── 1. Patch interactions.json ─────────────────────────────────────────────
with open(B / 'interactions.json') as f:
    ix = json.load(f)

for tile in ix['tiles']:
    tid = tile['tile_id']

    if tid == 'tile_pandas_dtype_datetime':
        for entry in tile['interactions']:
            sid = entry['step_id']

            # s04: t1 stdout_equals "float64" is hard-coded → value_equals on actual data
            if sid == 'tile_pandas_dtype_datetime.s04':
                entry['interaction']['grading']['tests'] = [{
                    "test_id": "t1",
                    "kind": "value_equals",
                    "spec": {
                        "expr": "df['distance_km'].tolist()",
                        "expected": [4.2, 6.1, 5.5, 3.8, 7.3, 8.0, 12.4, 9.2, 4.9, 5.1, 10.0, 4.4, 6.6, 11.1]
                    },
                    "visible": True,
                    "message_on_fail": "The distance_km values should be floats after conversion. Check that you used astype(float)."
                }]

            # s08: t1 hard-coded dtype string; t2 hard-coded dtype string + wrong expected "int64"
            if sid == 'tile_pandas_dtype_datetime.s08':
                entry['interaction']['grading']['tests'] = [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['pickup_date'].dt.day.tolist()",
                            "expected": [14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20]
                        },
                        "visible": True,
                        "message_on_fail": "pickup_date should be datetime. Check that you used pd.to_datetime()."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['pickup_month'].tolist()",
                            "expected": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
                        },
                        "visible": True,
                        "message_on_fail": "pickup_month should contain month numbers from .dt.month. Check your extraction."
                    }
                ]

    if tid == 'tile_pandas_text_dupes_missing':
        for entry in tile['interactions']:
            sid = entry['step_id']

            # s11: solution uses len() (call:len) and list_lit → rewrite to use only allowed syntax
            if sid == 'tile_pandas_text_dupes_missing.s11':
                ix_obj = entry['interaction']
                ix_obj['public']['prompt'] = (
                    "The `df` DataFrame has a missing value in `delivery_time_minutes`. "
                    "Print `df['delivery_time_minutes'].isna()` to detect the gap. "
                    "Then fill the missing value with the column median using `fillna()`. "
                    "Print the filled column.\n\n"
                    "Use only `df['col'].isna()`, `df['col'].fillna(value)`, "
                    "`df['col'].median()`, and `print()`."
                )
                ix_obj['public']['workspace']['files'][0]['content'] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders_messy.csv')\n\n"
                    "# TODO: Print isna() to detect missing delivery_time_minutes\n\n"
                    "# TODO: Fill missing delivery_time_minutes with its median\n\n"
                    "# TODO: Print the filled column\n"
                )
                ix_obj['grading']['solution_files'][0]['content'] = (
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('orders_messy.csv')\n\n"
                    "# Print isna() to detect missing delivery_time_minutes\n"
                    "print(df['delivery_time_minutes'].isna())\n\n"
                    "# Fill missing delivery_time_minutes with its median\n"
                    "df['delivery_time_minutes'] = df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median())\n\n"
                    "# Print the filled column\n"
                    "print(df['delivery_time_minutes'])\n"
                )
                ix_obj['grading']['tests'] = [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['delivery_time_minutes'].isna().sum()",
                            "expected": 0
                        },
                        "visible": True,
                        "message_on_fail": "After filling, delivery_time_minutes should have no missing values."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "df['delivery_time_minutes'].tolist()",
                            "expected": [18.0, 20.0, 22.0, 22.0, 26.0, 28.0, 80.0, 23.0, 19.0, 24.0, 33.0, 21.0, 27.0, 35.0, 22.0]
                        },
                        "visible": True,
                        "message_on_fail": "The missing value should be filled with the median (23.0)."
                    }
                ]
                ix_obj['feedback']['correct']['message'] = "Perfect! You detected the missing value with isna() and filled it with the column median."
                ix_obj['feedback']['incorrect']['message'] = "Not quite. Use `df['delivery_time_minutes'].fillna(df['delivery_time_minutes'].median())`."
                ix_obj['feedback']['hints'] = ["Use isna() to see the gap, then fillna(median()) to fill it."]

with open(B / 'interactions.json', 'w') as f:
    json.dump(ix, f, indent=2)
# Also write back to part file
with open(B / 'interactions.part.c2.json', 'w') as f:
    json.dump(ix, f, indent=2)
print("interactions.json patched")

# ── 2. Patch screens.json ──────────────────────────────────────────────────
with open(B / 'screens.json') as f:
    sc = json.load(f)

for tile in sc['tiles']:
    tid = tile['tile_id']

    if tid == 'tile_pandas_text_dupes_missing':
        for step in tile['steps']:
            sid = step['step_id']

            # s05: data_table uses base ds_orders but highlights occurrence:1 of 1003
            # Fix: add variant_id=orders_messy so the duplicate row exists
            if sid == 'tile_pandas_text_dupes_missing.s05':
                for block in step.get('blocks', []):
                    if block.get('type') == 'before_after':
                        ar = block['before'].get('asset_ref', {})
                        if ar.get('asset_id') == 'ds_orders' and 'variant_id' not in ar:
                            ar['variant_id'] = 'orders_messy'
                            print("Fixed s05 data_table variant_id")

            # s12: lineage.teaching_block_ids has extra pandas.drop_duplicates#tb3
            if sid == 'tile_pandas_text_dupes_missing.s12':
                planned = ['pandas.str_accessor_cleaning#tb3', 'pandas.missing_data_handling#tb5']
                if 'lineage' in step:
                    step['lineage']['teaching_block_ids'] = planned
                    print("Fixed s12 step lineage.teaching_block_ids")
                for block in step.get('blocks', []):
                    if 'lineage' in block:
                        tids = block['lineage'].get('teaching_block_ids', [])
                        new_tids = [t for t in tids if t != 'pandas.drop_duplicates#tb3']
                        if new_tids != tids:
                            block['lineage']['teaching_block_ids'] = new_tids
                            print(f"Fixed s12 block {block.get('block_id')} lineage")

    if tid == 'tile_pandas_descriptive_stats':
        for step in tile['steps']:
            sid = step['step_id']

            # s01: needs annotated_image or diagram block (no images registered → use diagram)
            if sid == 'tile_pandas_descriptive_stats.s01':
                blocks = step.get('blocks', [])
                has_visual = any(b['type'] in ('annotated_image', 'diagram') for b in blocks)
                if not has_visual:
                    diagram_block = {
                        "type": "diagram",
                        "block_id": "tile_pandas_descriptive_stats.s01.b5",
                        "diagram_kind": "mapping",
                        "title": "describe() output — key rows mapped to single-method results",
                        "nodes": [
                            {"id": "d_mean",   "label": "mean   30.86",  "kind": "describe_row"},
                            {"id": "d_std",    "label": "std    21.93",  "kind": "describe_row"},
                            {"id": "d_min",    "label": "min    18.00",  "kind": "describe_row"},
                            {"id": "d_50",     "label": "50%    22.00",  "kind": "describe_row"},
                            {"id": "d_max",    "label": "max    80.00",  "kind": "describe_row"},
                            {"id": "m_mean",   "label": ".mean() → 30.86",   "kind": "method_result"},
                            {"id": "m_std",    "label": ".std()  → 21.93",   "kind": "method_result"},
                            {"id": "m_min",    "label": "minimum value",      "kind": "method_result"},
                            {"id": "m_median", "label": ".median() → 22.00", "kind": "method_result"},
                            {"id": "m_max",    "label": "maximum value (outlier)", "kind": "method_result"}
                        ],
                        "edges": [
                            {"from": "d_mean", "to": "m_mean",   "label": "average delivery time"},
                            {"from": "d_std",  "to": "m_std",    "label": "typical spread"},
                            {"from": "d_min",  "to": "m_min",    "label": "fastest delivery"},
                            {"from": "d_50",   "to": "m_median", "label": "median: half above, half below"},
                            {"from": "d_max",  "to": "m_max",    "label": "slowest delivery"}
                        ],
                        "alt_text": (
                            "Mapping diagram: five key rows of describe() output for delivery_time_minutes "
                            "(mean 30.86, std 21.93, min 18, 50% 22, max 80) connected by arrows to the "
                            "matching single-method results (.mean(), .std(), .median()) and plain-language "
                            "labels for the extremes."
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
                    print("Added diagram block to descriptive_stats.s01")

with open(B / 'screens.json', 'w') as f:
    json.dump(sc, f, indent=2)
# Also write back to part file
with open(B / 'screens.part.c2.json', 'w') as f:
    json.dump(sc, f, indent=2)
print("screens.json patched")
print("Done. Now run: python3 00_FINAL_PIPELINE_CORE/scripts/assemble_tiles.py batches/final_batch_009_da_pandas")
