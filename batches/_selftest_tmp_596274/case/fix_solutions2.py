#!/usr/bin/env python3
"""Fix solutions to contain only learner code, not starter."""
import json

with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json') as f:
    data = json.load(f)

tile = data['tiles'][0]
interactions = {ix['step_id']: ix for ix in tile['interactions']}

# Fix s05: solution should only have learner code
s05 = interactions['tile_viz_figures_layout_plotting.s05']['interaction']
s05['grading']['solution_files'][0]['content'] = """import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5]
delivery_times = [21, 23, 19, 25, 20]

fig, ax = plt.subplots()
ax.plot(days, delivery_times)
"""

# Fix s12: solution should only have learner code
s12 = interactions['tile_viz_figures_layout_plotting.s12']['interaction']
s12['grading']['solution_files'][0]['content'] = """import matplotlib.pyplot as plt

days = [1, 2, 3, 4, 5]
delivery_times = [21, 23, 19, 25, 20]

plt.plot(delivery_times)
plt.plot(days, delivery_times)
"""

with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed s05 and s12 solutions")
