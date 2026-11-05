#!/usr/bin/env python3
"""Move most of the solution into the starter, leaving only a small piece for the learner."""

import json

# Read the interactions file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        if step_id == 'tile_capstone_integrate_tools_model.s05':
            # SQL - put most of the query in the starter
            # Have the learner only add the GROUP BY clause
            for wf in ix['workspace']['files']:
                if wf['path'] == 'query.sql':
                    # Starter has everything except GROUP BY
                    wf['content'] = """-- Complete the query by adding a GROUP BY clause at the end
SELECT zone, AVG(delivery_time)
FROM orders
INNER JOIN drivers ON orders.driver_id = drivers.driver_id
WHERE order_date >= '2026-04-01' AND order_date < '2026-07-01'
-- Add GROUP BY here"""
                    print(f"Updated starter for {step_id}")
            
            # Solution just adds GROUP BY
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'query.sql':
                    sf['content'] = """-- Complete the query by adding a GROUP BY clause at the end
SELECT zone, AVG(delivery_time)
FROM orders
INNER JOIN drivers ON orders.driver_id = drivers.driver_id
WHERE order_date >= '2026-04-01' AND order_date < '2026-07-01'
GROUP BY zone"""
                    print(f"Updated solution for {step_id}")
        
        elif step_id == 'tile_capstone_integrate_tools_model.s15':
            # Python - put most in the starter
            for wf in ix['workspace']['files']:
                if wf['path'] == 'solution.py':
                    # Starter has imports and data load
                    wf['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

# TODO: Remove rows with missing delivery_time values
# TODO: Group by zone and calculate mean delivery_time
# TODO: Print the result
"""
                    print(f"Updated starter for {step_id}")
            
            # Solution completes it
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'solution.py':
                    sf['content'] = """import pandas as pd

df = pd.read_csv('orders.csv')

clean_df = df.dropna()
result = clean_df.groupby('zone')['delivery_time'].mean()
print(result)
"""
                    print(f"Updated solution for {step_id}")
        
        elif step_id == 'tile_capstone_stats_dashboard.s10':
            # Chart - put most in the starter
            for wf in ix['workspace']['files']:
                if wf['path'] == 'dashboard.py':
                    # Starter has imports, data load, and subplot setup
                    wf['content'] = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

# TODO: Create three subplots showing:
# 1. Orders per zone (bar chart)
# 2. Delivery time distribution (histogram)
# 3. Mean delivery time per zone (bar chart)
# Add a figure title with plt.suptitle()
"""
                    print(f"Updated starter for {step_id}")
            
            # Solution completes it
            for sf in ix['grading']['solution_files']:
                if sf['path'] == 'dashboard.py':
                    sf['content'] = """import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

zone_counts = df['zone'].value_counts()
plt.subplot(131)
plt.bar(list(zone_counts.keys()), list(zone_counts))
plt.title('Orders per Zone')

plt.subplot(132)
clean_times = df['delivery_time'][df['delivery_time'].notna()]
plt.hist(clean_times)
plt.title('Delivery Time Distribution')

zone_means = df.groupby('zone')['delivery_time'].mean()
plt.subplot(133)
plt.bar(list(zone_means.keys()), list(zone_means))
plt.title('Mean Delivery Time per Zone')

plt.suptitle('QuickRide Capstone Dashboard')
plt.tight_layout()
"""
                    print(f"Updated solution for {step_id}")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nStarter/solution update complete!")
