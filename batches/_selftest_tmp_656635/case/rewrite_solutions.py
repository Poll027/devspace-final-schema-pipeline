#!/usr/bin/env python3
"""Rewrite solutions to use simpler syntax."""

import json

# Read the interactions file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        if step_id == 'tile_capstone_integrate_tools_model.s05':
            # SQL solution - try to avoid table aliases and AS
            # But we NEED a JOIN per the practice requirements
            # Let's try using the full table names without aliases
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'query.sql':
                    # Try without table aliases
                    new_solution = """SELECT orders.zone, AVG(orders.delivery_time)
FROM orders
INNER JOIN drivers ON orders.driver_id = drivers.driver_id
WHERE orders.order_date >= '2026-04-01' AND orders.order_date < '2026-07-01'
GROUP BY orders.zone"""
                    
                    sf['content'] = new_solution
                    print(f"Rewrote {step_id} solution (no aliases)")
                    
                    # Update expected column name
                    for test in ix['grading']['tests']:
                        if test['kind'] == 'query_result_equals':
                            test['spec']['expected']['columns'] = ['zone', 'AVG(orders.delivery_time)']
        
        elif step_id == 'tile_capstone_integrate_tools_model.s15':
            # Python solution - simplify to avoid attr_module issues
            # The issue might be with how we're calling methods
            # Let's try a more explicit approach
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'solution.py':
                    # Simplify - avoid chaining, use explicit steps
                    new_solution = """import pandas as pd

df = pd.read_csv('orders.csv')

clean_df = df.dropna()

grouped = clean_df.groupby('zone')
result = grouped['delivery_time'].mean()

print(result)
"""
                    
                    sf['content'] = new_solution
                    print(f"Rewrote {step_id} solution (simplified)")
        
        elif step_id == 'tile_capstone_stats_dashboard.s10':
            # Chart solution - avoid .index and .values
            # Use list() or other methods to convert
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'dashboard.py':
                    # Rewrite to avoid .index and .values
                    # Use the data directly without accessing these attributes
                    new_solution = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

# First subplot - orders per zone
zone_counts = df['zone'].value_counts()
plt.subplot(131)
zones = list(zone_counts.keys())
counts = list(zone_counts)
plt.bar(zones, counts)
plt.title('Orders per Zone')

# Second subplot - delivery time distribution
plt.subplot(132)
delivery_times = df['delivery_time']
clean_times = delivery_times[delivery_times.notna()]
plt.hist(clean_times)
plt.title('Delivery Time Distribution')

# Third subplot - mean delivery time per zone
zone_means = df.groupby('zone')['delivery_time'].mean()
plt.subplot(133)
mean_zones = list(zone_means.keys())
means = list(zone_means)
plt.bar(mean_zones, means)
plt.title('Mean Delivery Time per Zone')

plt.suptitle('QuickRide Capstone Dashboard')
plt.tight_layout()
"""
                    
                    sf['content'] = new_solution
                    print(f"Rewrote {step_id} solution (no .index/.values)")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nSolution rewriting complete!")
