#!/usr/bin/env python3
"""Patch screens.part.c2.json to fix evaluator findings."""

import json

with open('screens.part.c2.json', 'r') as f:
    data = json.load(f)

# ADVISORY tile_viz_labeling_chart_selection/s06: 
# The alt text is actually correct - ds.orders contains all three cities.
# No change needed.

# ADVISORY tile_viz_labeling_chart_selection/s11: 
# UP NEXT says "Viz Seaborn Stats Themes" but tile_viz_custom_multi_panel may come first
# Need to verify the tile order and update UP NEXT accordingly
# Looking at the tiles array, the order is:
# 1. tile_viz_labeling_chart_selection
# 2. tile_viz_custom_multi_panel
# 3. tile_viz_seaborn_stats_themes
# So the next tile after tile_viz_labeling_chart_selection is tile_viz_custom_multi_panel

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_labeling_chart_selection.s11':
                for block in step['blocks']:
                    if block.get('type') == 'up_next':
                        # Update to reference tile_viz_custom_multi_panel
                        block['title'] = 'Up next: Viz Custom Multi Panel'
                        block['text'] = 'Next: style sheets, rcParams, and multi-panel figures'

# ADVISORY tile_viz_custom_multi_panel/s09: 
# UP NEXT label "Stats Ab Test Lift" contradicts the description
# The next tile is tile_viz_seaborn_stats_themes

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_custom_multi_panel':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_custom_multi_panel.s09':
                for block in step['blocks']:
                    if block.get('type') == 'up_next':
                        # Update to match the description
                        block['title'] = 'Up next: Viz Seaborn Stats Themes'
                        # Keep the text as is - it correctly describes seaborn

# ADVISORY tile_viz_custom_multi_panel/s05: 
# Explainer references orders['delivery_time_minutes'] and orders['distance_km'] 
# but no data asset is declared. Change to generic placeholder values.

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_custom_multi_panel':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_custom_multi_panel.s05':
                for block in step['blocks']:
                    if block.get('block_id') == 'tile_viz_custom_multi_panel.s05.b02':
                        # Replace specific column references with generic placeholders
                        old_text = block['text']
                        new_text = old_text.replace(
                            "axs[0, 0].hist(orders['delivery_time_minutes']) draws the histogram into the top-left panel; axs[0, 1].scatter(orders['distance_km'], orders['delivery_time_minutes']) draws the scatter into the top-right panel without disturbing the first.",
                            "axs[0, 0].hist(data) draws a histogram into the top-left panel; axs[0, 1].scatter(x_values, y_values) draws a scatter into the top-right panel without disturbing the first."
                        )
                        block['text'] = new_text

# ADVISORY tile_viz_seaborn_stats_themes/r01: 
# The matplotlib "before" example plots raw rows without aggregation, 
# while sns.barplot computes means. Change the prose in r01 to match the before code in s01.

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_seaborn_stats_themes':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_seaborn_stats_themes.r01':
                for block in step['blocks']:
                    if block.get('block_id') == 'tile_viz_seaborn_stats_themes.r01.b01':
                        # Update the prose to match the s01 before code (which uses groupby)
                        block['text'] = "With matplotlib you write city_avg = orders.groupby('city')['delivery_time_minutes'].mean() then ax.bar(city_avg.index, city_avg.values). With seaborn you write sns.barplot(data=orders, x='city', y='delivery_time_minutes'). The difference: seaborn takes the whole DataFrame and column names as strings, computing the mean automatically."

with open('screens.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patched screens.part.c2.json")
