#!/usr/bin/env python3
"""Fix s04 to have DataFrame in starter, not in solution."""

import json

# Read the file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Process each tile
for tile in data['tiles']:
    for ix in tile['interactions']:
        step_id = ix['step_id']
        interaction = ix['interaction']
        
        # Fix tile_viz_custom_multi_panel.s04
        if step_id == 'tile_viz_custom_multi_panel.s04':
            # Starter has DataFrame already defined
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

# Apply custom styling and create a bar chart below
"""
            interaction['public']['workspace']['files'][0]['content'] = starter_content
            
            # Solution only adds the styling and plot calls
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

# Apply custom styling and create a bar chart below
sns.set_palette('pastel')
mpl.rcParams['axes.titlesize'] = 16
sns.barplot(data=df, x='city', y='delivery_time_minutes')
plt.title('Delivery Times by City')
"""
            interaction['grading']['solution_files'][0]['content'] = solution_content
            
            # Update test t02 to expect the title
            for test in interaction['grading']['tests']:
                if test.get('test_id') == 'ix.tile_viz_custom_multi_panel.s04.t02':
                    test['spec']['expected'] = 'Delivery Times by City'
            
            # Update prompt to match the practice anchor
            interaction['public']['prompt'] = """A DataFrame `df` with columns `city` and `delivery_time_minutes` is already loaded.

Apply custom styling and create a bar chart:
1. Set a custom seaborn palette using `sns.set_palette('pastel')`
2. Increase the title font size by setting `mpl.rcParams['axes.titlesize'] = 16`
3. Create a bar chart using `sns.barplot(data=df, x='city', y='delivery_time_minutes')`
4. Add a title `'Delivery Times by City'` using `plt.title()`

The styling changes will affect all subsequent plots."""

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed tile_viz_custom_multi_panel.s04 to match practice anchor")
