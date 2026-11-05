#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix validation errors."""

import json

# Read the current file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix s10: Use Series directly without .index and .values
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_capstone_stats_dashboard':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_capstone_stats_dashboard.s10':
                # New solution that passes Series directly to plotting functions
                new_solution = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

zone_counts = df['zone'].value_counts()
delivery_times = df['delivery_time']
zone_means = df.groupby('zone')['delivery_time'].mean()

plt.subplot(131)
plt.bar(range(len(zone_counts)), zone_counts)
plt.title('Orders per Zone')

plt.subplot(132)
plt.hist(delivery_times)
plt.title('Delivery Time Distribution')

plt.subplot(133)
plt.bar(range(len(zone_means)), zone_means)
plt.title('Mean Delivery Time per Zone')

plt.suptitle('QuickRide Capstone Dashboard')
plt.tight_layout()
"""
                
                # Update solution
                for sf in ix['interaction']['grading']['solution_files']:
                    if sf['path'] == 'dashboard.py':
                        sf['content'] = new_solution
                        print("Updated s10 solution")
                
                # Starter stays the same
                print("Starter unchanged")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatching complete!")
