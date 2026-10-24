#!/usr/bin/env python3
"""Fix the chart encoding to match the actual dataset columns"""
import json

# Read the screens file
with open('screens.part.c1.json', 'r') as f:
    data = json.load(f)

# Find and fix the chart encoding
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_stats_correlation':
        for step in tile['steps']:
            if step['step_id'] == 'tile_stats_correlation.s01':
                for block in step['blocks']:
                    if block.get('type') == 'chart' and block.get('block_id') == 'tile_stats_correlation.s01.chart1':
                        print(f"Fixing chart encoding in {block['block_id']}")
                        
                        # Update encoding to match ds_delivery_orders_extended columns
                        block['encoding'] = {
                            "x": {
                                "field": "distance_km",
                                "type": "quantitative",
                                "title": "Distance (km)"
                            },
                            "y": {
                                "field": "delivery_minutes",
                                "type": "quantitative",
                                "title": "Delivery Time (minutes)"
                            }
                        }
                        
                        # Update title and alt_text to match the actual data
                        block['title'] = "Distance vs. Delivery Time: Positive Correlation"
                        block['alt_text'] = "Scatter plot showing delivery orders. Points trend upward from left to right, indicating that as distance increases, delivery time also tends to increase — a positive correlation."
                        
                        # Remove annotations since they referenced the synthetic patterns
                        if 'annotations' in block:
                            del block['annotations']
                        
                        print("  Updated encoding to use distance_km and delivery_minutes")
                        print("  Updated title and alt_text")
                        print("  Removed annotations")

# Write back
with open('screens.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Done!")
