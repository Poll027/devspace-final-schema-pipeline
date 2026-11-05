#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix validation errors."""

import json

# Read the current file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix s10: Simplify solution to avoid list(), .index, etc.
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_capstone_stats_dashboard':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_capstone_stats_dashboard.s10':
                # New simpler solution that doesn't use list(), .index
                new_solution = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

zone_counts = df['zone'].value_counts()
delivery_times = df['delivery_time']
zone_means = df.groupby('zone')['delivery_time'].mean()

ax1 = plt.subplot(131)
ax1.bar(zone_counts.index, zone_counts.values)
ax1.set_title('Orders per Zone')

ax2 = plt.subplot(132)
ax2.hist(delivery_times)
ax2.set_title('Delivery Time Distribution')

ax3 = plt.subplot(133)
ax3.bar(zone_means.index, zone_means.values)
ax3.set_title('Mean Delivery Time per Zone')

plt.suptitle('QuickRide Capstone Dashboard')
plt.tight_layout()
"""
                
                # Update solution
                for sf in ix['interaction']['grading']['solution_files']:
                    if sf['path'] == 'dashboard.py':
                        sf['content'] = new_solution
                        print("Updated s10 solution")
                
                # Update starter to match
                new_starter = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

zone_counts = df['zone'].value_counts()
delivery_times = df['delivery_time']
zone_means = df.groupby('zone')['delivery_time'].mean()

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
