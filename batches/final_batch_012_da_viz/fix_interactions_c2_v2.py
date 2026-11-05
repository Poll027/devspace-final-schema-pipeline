"""Fix interactions.part.c2.json - revert allowed_syntax changes."""
import json

with open('batches/final_batch_012_da_viz/interactions.part.c2.json') as f:
    data = json.load(f)

# Fix tile_viz_labeling_chart_selection.s05
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for step_ix in tile['interactions']:
            if step_ix['step_id'] == 'tile_viz_labeling_chart_selection.s05':
                ix = step_ix['interaction']
                # Revert allowed_syntax to glossary version (remove the additions)
                ix['public']['constraints']['allowed_syntax'] = [
                    "ax.set_xlabel('...')",
                    "ax.set_ylabel('...')",
                    "ax.set_title('...')",
                    "ax.plot(x, y, label='...')",
                    "ax.legend()",
                    "plt.xlabel('...')",
                    "plt.ylabel('...')",
                    "plt.title('...')",
                    "import matplotlib.pyplot as plt",
                    "fig, ax = plt.subplots()",
                    "plt.show()"
                ]
                
            elif step_ix['step_id'] == 'tile_viz_labeling_chart_selection.s10':
                ix = step_ix['interaction']
                # Revert allowed_syntax to glossary version
                ix['public']['constraints']['allowed_syntax'] = [
                    "import matplotlib.pyplot as plt",
                    "plt.scatter(x, y)",
                    "plt.xlabel()",
                    "plt.ylabel()",
                    "plt.title()",
                    "plt.show()",
                    "Python list literals",
                    "variable assignment",
                    "single-line comments (#)"
                ]

with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed interactions.part.c2.json - reverted allowed_syntax")
