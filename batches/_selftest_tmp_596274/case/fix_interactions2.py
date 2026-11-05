#!/usr/bin/env python3
import json

# Read the current artifact
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix: Restore allowed_syntax to match glossary EXACTLY, but keep solution with double brackets
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_custom_multi_panel':
        for interaction_entry in tile['interactions']:
            if interaction_entry['step_id'] == 'tile_viz_custom_multi_panel.s08':
                interaction = interaction_entry['interaction']
                
                # Restore allowed_syntax to match glossary EXACTLY (with tuple notation)
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
                
                # But keep solution and prompt using double-bracket notation (which doesn't use tuple_lit)
                # The solution is already fixed, just verify
                solution = interaction['grading']['solution_files'][0]['content']
                if 'axs[0][0]' in solution:
                    print("Solution correctly uses double-bracket notation")
                else:
                    print("ERROR: Solution doesn't use double-bracket notation!")
                
                print(f"Restored allowed_syntax to match glossary")

# Write the fixed artifact
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Fix applied")
