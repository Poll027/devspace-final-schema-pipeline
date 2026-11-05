#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix validation errors."""

import json

# Read the current interactions file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix 1: Update tile_viz_custom_multi_panel.s08 allowed_syntax
# Change from axs[row][col] to axs[row, col] to match glossary
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_custom_multi_panel':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_custom_multi_panel.s08':
                interaction = interaction_entry['interaction']
                # Update allowed_syntax to match glossary exactly
                interaction['public']['constraints']['allowed_syntax'] = [
                    "plt.subplots(2, 2)",
                    "axs[0, 0].hist(...)",
                    "axs[0, 1].hist(...)",
                    "axs[1, 0].hist(...)",
                    "axs[1, 1].hist(...)",
                    "axs[row, col].set_title(...)",
                    "axs[row, col].set_xlabel(...)",
                    "axs[row, col].set_ylabel(...)",
                    "plt.tight_layout()",
                    "plt.show()"
                ]
                print("Fixed tile_viz_custom_multi_panel.s08 allowed_syntax")
                break

# Fix 2: Add identify_line_graph_use_case to tile_viz_labeling_chart_selection.s09 measures
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_labeling_chart_selection.s09':
                interaction = interaction_entry['interaction']
                # Add the missing measure
                interaction['measures'].insert(0, {
                    "concept_id": "viz.chart_type_selection",
                    "capability": "identify_line_graph_use_case",
                    "fact_ids": ["f3"]
                })
                # Add the missing anchor
                interaction['anchors'].insert(0, 
                    "viz.chart_type_selection#assessment:identify_line_graph_use_case"
                )
                print("Added identify_line_graph_use_case to tile_viz_labeling_chart_selection.s09")
                break

# Write the patched file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch complete")
