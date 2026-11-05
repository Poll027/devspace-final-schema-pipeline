#!/usr/bin/env python3
"""Merge interactions.part.c3.json into interactions.json."""
import json

with open('batches/final_batch_009_da_pandas/interactions.json') as f:
    full = json.load(f)

with open('batches/final_batch_009_da_pandas/interactions.part.c3.json') as f:
    c3 = json.load(f)

# Replace tiles from c3 in full
c3_tile_ids = {t['tile_id'] for t in c3['tiles']}
full['tiles'] = [t for t in full['tiles'] if t['tile_id'] not in c3_tile_ids] + c3['tiles']

# Sort tiles by the order they appear in the original
tile_order = [
    'tile_pandas_dataframe_reading',
    'tile_pandas_creating_inspecting',
    'tile_pandas_selection_filtering',
    'tile_pandas_sort_rename',
    'tile_pandas_dtype_datetime',
    'tile_pandas_text_dupes_missing',
    'tile_pandas_descriptive_stats',
    'tile_pandas_map_apply',
    'tile_pandas_groupby_melt',
    'tile_pandas_concat_merge',
    'tile_pandas_pivot_export'
]
full['tiles'].sort(key=lambda t: tile_order.index(t['tile_id']) if t['tile_id'] in tile_order else 999)

with open('batches/final_batch_009_da_pandas/interactions.json', 'w') as f:
    json.dump(full, f, indent=2)

print("Merged c3 into interactions.json")
