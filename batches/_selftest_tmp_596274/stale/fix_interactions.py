#!/usr/bin/env python3
import json

# Read the current artifact
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix 1: Remove identify_line_graph_use_case anchor from s09 since it doesn't measure it
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_labeling_chart_selection.s09':
                # Remove the line graph anchor - this interaction only measures boxplot
                interaction = interaction_entry['interaction']
                if 'anchors' in interaction:
                    interaction['anchors'] = [
                        a for a in interaction['anchors'] 
                        if 'identify_line_graph_use_case' not in a
                    ]
                print(f"Fixed s09 anchors: {interaction['anchors']}")

# Fix 2: Change tile_viz_custom_multi_panel.s08 to use double-bracket indexing
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_custom_multi_panel':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_custom_multi_panel.s08':
                interaction = interaction_entry['interaction']
                
                # Update the prompt to use double-bracket notation
                old_prompt = interaction['public']['prompt']
                new_prompt = old_prompt.replace('axs[0, 0]', 'axs[0][0]')
                new_prompt = new_prompt.replace('axs[0, 1]', 'axs[0][1]')
                new_prompt = new_prompt.replace('axs[1, 0]', 'axs[1][0]')
                new_prompt = new_prompt.replace('axs[1, 1]', 'axs[1][1]')
                interaction['public']['prompt'] = new_prompt
                
                # Update allowed_syntax to use double-bracket notation
                interaction['public']['constraints']['allowed_syntax'] = [
                    "plt.subplots(2, 2)",
                    "axs[0][0].hist(...)",
                    "axs[0][1].hist(...)",
                    "axs[1][0].hist(...)",
                    "axs[1][1].hist(...)",
                    "axs[row][col].set_title(...)",
                    "axs[row][col].set_xlabel(...)",
                    "axs[row][col].set_ylabel(...)",
                    "plt.tight_layout()",
                    "plt.show()"
                ]
                
                # Update solution to use double-bracket notation
                old_solution = interaction['grading']['solution_files'][0]['content']
                new_solution = old_solution.replace('axs[0, 0]', 'axs[0][0]')
                new_solution = new_solution.replace('axs[0, 1]', 'axs[0][1]')
                new_solution = new_solution.replace('axs[1, 0]', 'axs[1][0]')
                new_solution = new_solution.replace('axs[1, 1]', 'axs[1][1]')
                interaction['grading']['solution_files'][0]['content'] = new_solution
                
                # Update feedback hints to use double-bracket notation
                interaction['feedback']['incorrect']['message'] = interaction['feedback']['incorrect']['message'].replace('axs[row][col]', 'axs[row][col]')
                interaction['feedback']['hints'][1] = "Each panel is addressed by axs[row][col] — for example axs[0][0] is top-left and axs[1][1] is bottom-right."
                
                print(f"Fixed s08 to use double-bracket indexing")

# Write the fixed artifact
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fixes applied successfully")
