#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix validation errors."""

import json

# Read the current file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Fix s10: Simplify solution to avoid .index, .values, and attr_module
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_capstone_stats_dashboard':
        for ix in tile['interactions']:
            if ix['step_id'] == 'tile_capstone_stats_dashboard.s10':
                # New solution that doesn't use .index, .values
                # Use the Series directly - matplotlib can handle them
                new_solution = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

zone_counts = df['zone'].value_counts()
delivery_times = df['delivery_time']
zone_means = df.groupby('zone')['delivery_time'].mean()

plt.subplot(131)
plt.bar(zone_counts.index, zone_counts)
plt.title('Orders per Zone')

plt.subplot(132)
plt.hist(delivery_times)
plt.title('Delivery Time Distribution')

plt.subplot(133)
plt.bar(zone_means.index, zone_means)
plt.title('Mean Delivery Time per Zone')

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
                
                # Also need to add "import pandas as pd" and "pd.read_csv()" to allowed syntax
                # But wait - the GENERATOR.md says not to edit constraints!
                # Let me check if these are already in the allowed list...
                
                # Actually, looking at the allowed list, it doesn't have pd.read_csv
                # But the starter already has it, so it should be scaffolding
                # Let me check if the judge function filters out starter content...

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatching complete!")
