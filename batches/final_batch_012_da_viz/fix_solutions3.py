#!/usr/bin/env python3
"""Try removing data definitions from solution files."""
import json

with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json') as f:
    data = json.load(f)

tile = data['tiles'][0]
interactions = {ix['step_id']: ix for ix in tile['interactions']}

# Fix s05: solution without data definitions
s05 = interactions['tile_viz_figures_layout_plotting.s05']['interaction']
s05['grading']['solution_files'][0]['content'] = """import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(days, delivery_times)
"""

# Fix s12: solution without data definitions
s12 = interactions['tile_viz_figures_layout_plotting.s12']['interaction']
s12['grading']['solution_files'][0]['content'] = """import matplotlib.pyplot as plt

plt.plot(delivery_times)
plt.plot(days, delivery_times)
"""

with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Removed data definitions from solution files")
