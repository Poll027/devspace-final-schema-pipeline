"""
Combined patch for interactions.part.c2.json and screens.part.c2.json to fix validation errors:
1. Add remediation_step_id to first check/hands_on of each concept in tile_viz_labeling_chart_selection
2. Replace before_after block with chart block in tile_viz_seaborn_stats_themes.s01
"""
import json

print("Patching interactions.part.c2.json...")
# Load interactions.part.c2.json
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    interactions = json.load(f)

# Add remediation_step_id to tile_viz_labeling_chart_selection
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for interaction in tile['interactions']:
            step_id = interaction['step_id']
            # s03 is the first check for viz.labeling_annotation -> r01
            if step_id == 'tile_viz_labeling_chart_selection.s03':
                if 'feedback' not in interaction['interaction']:
                    interaction['interaction']['feedback'] = {}
                interaction['interaction']['feedback']['remediation_step_id'] = 'tile_viz_labeling_chart_selection.r01'
                print(f"  Added remediation_step_id to {step_id}: r01")
            # s08 is the first check for viz.chart_type_selection -> r02
            elif step_id == 'tile_viz_labeling_chart_selection.s08':
                if 'feedback' not in interaction['interaction']:
                    interaction['interaction']['feedback'] = {}
                interaction['interaction']['feedback']['remediation_step_id'] = 'tile_viz_labeling_chart_selection.r02'
                print(f"  Added remediation_step_id to {step_id}: r02")

# Save interactions
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(interactions, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("\nPatching screens.part.c2.json...")
# Load screens.part.c2.json
with open('batches/final_batch_012_da_viz/screens.part.c2.json', 'r') as f:
    screens = json.load(f)

# Replace before_after with chart in tile_viz_seaborn_stats_themes.s01
for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_viz_seaborn_stats_themes':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_seaborn_stats_themes.s01':
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
                            "lineage": block['lineage']
                        }
                        new_blocks.append(chart_block)
                        print(f"  Replaced before_after block with chart block in s01")
                    else:
                        new_blocks.append(block)
                step['blocks'] = new_blocks
                break

# Save screens
with open('batches/final_batch_012_da_viz/screens.part.c2.json', 'w') as f:
    json.dump(screens, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("\nDone. Both files patched successfully.")
