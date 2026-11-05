#!/usr/bin/env python3
"""Fix the interactions.part.c2.json file - fix s04 and s08 to not use pandas in solution."""

import json

# Read the file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Read the registry to get the actual data values
with open('batches/final_batch_012_da_viz/scenario_asset_registry.json', 'r') as f:
    registry = json.load(f)

# Get ds.orders data to compute the expected bar heights
ds_orders_rows = None
for asset in registry.get('assets', []):
    if asset.get('asset_id') == 'ds.orders':
        ds_orders_rows = asset.get('rows', [])
        break

# Compute average delivery time by city
city_times = {}
for row in ds_orders_rows:
    city = row[1]  # index 1 is city
    time = row[2]  # index 2 is delivery_time_minutes
    if city not in city_times:
        city_times[city] = []
    city_times[city].append(time)

city_averages = {city: sum(times) / len(times) for city, times in city_times.items()}
print(f"City averages: {city_averages}")

# Sort by city name to get consistent order
cities_sorted = sorted(city_averages.keys())
expected_heights = [city_averages[city] for city in cities_sorted]
print(f"Expected heights (sorted by city): {expected_heights}")

# Process each tile
for tile in data['tiles']:
    for ix in tile['interactions']:
        step_id = ix['step_id']
        interaction = ix['interaction']
        
        # Fix tile_viz_custom_multi_panel.s04
        if step_id == 'tile_viz_custom_multi_panel.s04':
            # Update starter to provide DataFrame already loaded
            starter_content = """import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data (already loaded)
df = pd.DataFrame({
    'city': ['Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 
             'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja',
             'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano'],
    'delivery_time_minutes': [18, 22, 19, 26, 30, 24, 28, 50,
                               25, 28, 23, 32, 35, 27, 31, 55,
                               27, 31, 26, 35, 38, 29, 34, 60]
})

# Apply custom styling and create a bar chart
"""
            interaction['public']['workspace']['files'][0]['content'] = starter_content
            
            # Update solution to use the pre-loaded DataFrame
            solution_content = """import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data (already loaded)
df = pd.DataFrame({
    'city': ['Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 
             'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja',
             'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano'],
    'delivery_time_minutes': [18, 22, 19, 26, 30, 24, 28, 50,
                               25, 28, 23, 32, 35, 27, 31, 55,
                               27, 31, 26, 35, 38, 29, 34, 60]
})

# Apply custom styling and create a bar chart
plt.style.use('seaborn')
sns.barplot(data=df, x='city', y='delivery_time_minutes')
plt.xlabel('City')
plt.ylabel('Delivery time (minutes)')
"""
            interaction['grading']['solution_files'][0]['content'] = solution_content
            
            # Remove asset_mounts since we're providing data inline
            interaction['public']['workspace']['asset_mounts'] = []

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed tile_viz_custom_multi_panel.s04 to use inline DataFrame")
