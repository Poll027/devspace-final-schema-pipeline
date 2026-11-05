#!/usr/bin/env python3
"""Patch screens.part.c1.json to replace annotated_image with comparison table."""

import json

# Read the current screens file
with open('batches/final_batch_009_da_pandas/screens.part.c1.json', 'r') as f:
    data = json.load(f)

# Find the tile and step
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_creating_inspecting':
        for step in tile['steps']:
            if step['step_id'] == 'tile_pandas_creating_inspecting.s05':
                # Find the diagram block (should be b3)
                for i, block in enumerate(step['blocks']):
                    if block.get('block_id') == 'tile_pandas_creating_inspecting.s05.b3':
                        # Replace with comparison
                        new_block = {
                            "type": "comparison",
                            "block_id": "tile_pandas_creating_inspecting.s05.b3",
                            "title": "Five inspection methods at a glance",
                            "columns": [
                                {"id": "head", "label": "head()"},
                                {"id": "shape", "label": "shape"},
                                {"id": "dtypes", "label": "dtypes"},
                                {"id": "info", "label": "info()"},
                                {"id": "describe", "label": "describe()"}
                            ],
                            "rows": [
                                {
                                    "criterion": "What it shows",
                                    "cells": {
                                        "head": "First 5 rows by default",
                                        "shape": "Tuple of (rows, columns)",
                                        "dtypes": "Data type of each column",
                                        "info": "Non-null counts, dtypes, and memory usage",
                                        "describe": "Statistical summary of numeric columns"
                                    }
                                },
                                {
                                    "criterion": "Example output",
                                    "cells": {
                                        "head": "DataFrame with 5 rows × all columns",
                                        "shape": "(250, 10)",
                                        "dtypes": "order_id: int64, city: object, ...",
                                        "info": "250 entries, 10 columns, 19.6+ KB",
                                        "describe": "count, mean, std, min, max for numeric columns"
                                    }
                                },
                                {
                                    "criterion": "Best for",
                                    "cells": {
                                        "head": "Quick sanity check of data",
                                        "shape": "Confirming dimensions",
                                        "dtypes": "Checking column types",
                                        "info": "Finding missing values",
                                        "describe": "Understanding numeric distributions"
                                    }
                                }
                            ],
                            "lineage": block['lineage']  # Keep the same lineage
                        }
                        step['blocks'][i] = new_block
                        print(f"✓ Replaced diagram with comparison in {step['step_id']}")
                        break

# Write the patched file
with open('batches/final_batch_009_da_pandas/screens.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Patch complete")
