#!/usr/bin/env python3
"""Patch screens.json to add missing diagram for s05."""
import json

def main():
    # Read the screens file
    with open('batches/final_batch_009_da_pandas/screens.json', 'r') as f:
        data = json.load(f)
    
    # Find and patch s05
    for tile in data['tiles']:
        if tile['tile_id'] == 'tile_pandas_creating_inspecting':
            for step in tile['steps']:
                if step['step_id'] == 'tile_pandas_creating_inspecting.s05':
                    # Add an annotated_image block
                    # Insert it after the prose blocks
                    annotated_image_block = {
                        "type": "annotated_image",
                        "block_id": "tile_pandas_creating_inspecting.s05.b_diagram",
                        "image_asset_id": "img_pandas_inspection_outputs",
                        "alt_text": "Five pandas inspection methods and their outputs on the orders DataFrame",
                        "annotations": [
                            {
                                "region": {"x": 10, "y": 10, "width": 600, "height": 100},
                                "label": "orders.head()",
                                "description": "Shows first 5 rows: order_id, city, courier, delivery times, ratings"
                            },
                            {
                                "region": {"x": 10, "y": 120, "width": 600, "height": 50},
                                "label": "orders.shape",
                                "description": "(14, 10) — 14 orders, 10 columns"
                            },
                            {
                                "region": {"x": 10, "y": 180, "width": 600, "height": 150},
                                "label": "orders.dtypes",
                                "description": "order_id: int64, city: object, delivery_time_minutes: int64, etc."
                            },
                            {
                                "region": {"x": 10, "y": 340, "width": 600, "height": 120},
                                "label": "orders.info()",
                                "description": "RangeIndex: 14 entries, Data columns: 10 total, dtypes: float64(3), int64(4), object(3)"
                            },
                            {
                                "region": {"x": 10, "y": 470, "width": 600, "height": 150},
                                "label": "orders.describe()",
                                "description": "Statistics for numeric columns: count, mean, std, min, 25%, 50%, 75%, max"
                            }
                        ],
                        "lineage": {
                            "concept_ids": ["pandas.inspecting_dataframes"],
                            "teaching_block_ids": [
                                "pandas.inspecting_dataframes#tb1",
                                "pandas.inspecting_dataframes#tb2",
                                "pandas.inspecting_dataframes#tb3",
                                "pandas.inspecting_dataframes#tb4",
                                "pandas.inspecting_dataframes#tb5"
                            ],
                            "fact_ids": [
                                "pandas.inspecting_dataframes#f1",
                                "pandas.inspecting_dataframes#f2",
                                "pandas.inspecting_dataframes#f3",
                                "pandas.inspecting_dataframes#f4"
                            ]
                        }
                    }
                    # Add the block to the step
                    step['blocks'].append(annotated_image_block)
                    print(f"Added annotated_image block to {step['step_id']}")
                    break
    
    # Write the patched file
    with open('batches/final_batch_009_da_pandas/screens.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Patched screens.json")

if __name__ == '__main__':
    main()
