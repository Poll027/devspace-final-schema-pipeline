"""
Patch screens.part.c2.json to replace the before_after block in tile_viz_seaborn_stats_themes.s01
with a chart block, matching the plan's requirement.
"""
import json

# Load screens.part.c2.json
with open('batches/final_batch_012_da_viz/screens.part.c2.json', 'r') as f:
    data = json.load(f)

# Find tile_viz_seaborn_stats_themes.s01 and replace before_after with chart
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_seaborn_stats_themes':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_seaborn_stats_themes.s01':
                # Find the before_after block and replace it with a chart block
                new_blocks = []
                for block in step['blocks']:
                    if block['type'] == 'before_after' and block['block_id'] == 'tile_viz_seaborn_stats_themes.s01.b03':
                        # Create a chart block instead
                        chart_block = {
                            "type": "chart",
                            "block_id": "tile_viz_seaborn_stats_themes.s01.b03",
                            "chart_kind": "bar",
                            "asset_ref": {
                                "asset_id": "ds.orders",
                                "columns": ["city", "delivery_time_minutes"]
                            },
                            "title": "Average Delivery Time by City — seaborn barplot",
                            "alt_text": "A seaborn barplot showing the mean delivery_time_minutes for Lagos, Abuja, and Kano, with error bars indicating uncertainty around each mean.",
                            "encoding": {
                                "x": {
                                    "field": "city",
                                    "type": "nominal",
                                    "title": "City"
                                },
                                "y": {
                                    "field": "delivery_time_minutes",
                                    "type": "quantitative",
                                    "aggregate": "mean",
                                    "title": "Avg delivery time (min)"
                                }
                            },
                            "lineage": block['lineage']  # Keep the same lineage
                        }
                        new_blocks.append(chart_block)
                        print(f"Replaced before_after block with chart block in s01")
                    else:
                        new_blocks.append(block)
                step['blocks'] = new_blocks
                break

# Save
with open('batches/final_batch_012_da_viz/screens.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Done.")
