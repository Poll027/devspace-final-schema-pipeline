#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix validation errors - comprehensive fix."""

import json

# Read the current interactions file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix 1: Update tile_viz_custom_multi_panel.s08 to use comma notation throughout
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
                
                # Update prompt to use comma notation
                interaction['public']['prompt'] = (
                    "A 2×2 subplot grid has already been created for you with `fig, axs = plt.subplots(2, 2)`. "
                    "Four lists of data are also provided: `col_a`, `col_b`, `col_c`, and `col_d`.\n\n"
                    "Draw a histogram in each panel:\n"
                    "1. Top-left panel: `axs[0, 0].hist(col_a)`\n"
                    "2. Top-right panel: `axs[0, 1].hist(col_b)`\n"
                    "3. Bottom-left panel: `axs[1, 0].hist(col_c)`\n"
                    "4. Bottom-right panel: `axs[1, 1].hist(col_d)`\n\n"
                    "Each panel will show the distribution of one column."
                )
                
                # Update solution to use comma notation
                interaction['grading']['solution_files'][0]['content'] = (
                    "import matplotlib.pyplot as plt\n\n"
                    "# Data (these values will be changed by the grader to test your code)\n"
                    "col_a_1 = 23\n"
                    "col_a = [col_a_1, 25, 22, 24, 26, 23, 25, 24]\n"
                    "col_b = [45, 47, 44, 46, 48, 45, 47, 46]\n"
                    "col_c = [56, 58, 55, 57, 59, 56, 58, 57]\n"
                    "col_d = [78, 80, 77, 79, 81, 78, 80, 79]\n\n"
                    "fig, axs = plt.subplots(2, 2)\n"
                    "# Draw a histogram in each panel below\n"
                    "axs[0, 0].hist(col_a)\n"
                    "axs[0, 1].hist(col_b)\n"
                    "axs[1, 0].hist(col_c)\n"
                    "axs[1, 1].hist(col_d)\n"
                )
                
                # Update feedback messages to use comma notation
                interaction['feedback']['incorrect']['message'] = (
                    "Make sure you called `.hist()` on each of the four `axs[row, col]` objects with a different list: "
                    "`axs[0, 0].hist(col_a)`, `axs[0, 1].hist(col_b)`, `axs[1, 0].hist(col_c)`, `axs[1, 1].hist(col_d)`."
                )
                
                interaction['feedback']['hints'][1] = (
                    "Each panel is addressed by axs[row, col] — for example axs[0, 0] is top-left and axs[1, 1] is bottom-right."
                )
                
                print("Fixed tile_viz_custom_multi_panel.s08 to use comma notation")
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
