#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix validation errors."""

import json

# Read the current file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix s10: Use pandas plot accessor and 'ax' as variable name
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_capstone_stats_dashboard':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_capstone_stats_dashboard.s10':
                # New solution that uses only allowed syntax
                new_solution = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

ax = plt.subplot(131)
df['zone'].value_counts().plot.bar(ax=ax)
ax.set_title('Orders per Zone')

ax = plt.subplot(132)
ax.hist(df['delivery_time'])
ax.set_title('Delivery Time Distribution')

ax = plt.subplot(133)
df.groupby('zone')['delivery_time'].mean().plot.bar(ax=ax)
ax.set_title('Mean Delivery Time per Zone')

plt.suptitle('QuickRide Capstone Dashboard')
plt.tight_layout()
"""
                
                # Update solution
                for sf in ix['interaction']['grading']['solution_files']:
                    if sf['path'] == 'dashboard.py':
                        sf['content'] = new_solution
                        print("Updated s10 solution")
                
                # Update starter to remove intermediate variables
                new_starter = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

# TODO: Create first panel with plt.subplot(131), then bar chart
# TODO: Create second panel with plt.subplot(132), then histogram
# TODO: Create third panel with plt.subplot(133), then bar chart
# TODO: Add suptitle and tight_layout
"""
                
                for f in ix['interaction']['public']['workspace']['files']:
                    if f['path'] == 'dashboard.py':
                        f['content'] = new_starter
                        print("Updated s10 starter")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatching complete!")
