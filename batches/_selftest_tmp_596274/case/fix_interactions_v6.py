#!/usr/bin/env python3
"""Fix s08 and s10 solutions to match their practice anchors."""

import json

# Read the file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Process each tile
for tile in data['tiles']:
    for ix in tile['interactions']:
        step_id = ix['step_id']
        interaction = ix['interaction']
        
        # Fix tile_viz_custom_multi_panel.s08
        # This should be about custom styling, not multi-panel
        # The practice is viz.custom_styling_theming, so it should use single-axis plots with styling
        if step_id == 'tile_viz_custom_multi_panel.s08':
            # Update prompt
            interaction['public']['prompt'] = """A DataFrame `df` with columns `category` and `value` is already loaded.

Apply a matplotlib style and create a styled line plot:
1. Apply the 'ggplot' style using `plt.style.use('ggplot')`
2. Create a line plot using `sns.lineplot(data=df, x='category', y='value')`
3. Add a title `'Sales by Category'` using `plt.title()`
4. Add axis labels using `plt.xlabel('Category')` and `plt.ylabel('Value')`

The style will affect the plot's appearance."""
            
            # Update starter
            starter_content = """import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data (already loaded)
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [23, 45, 56, 78]
})

# Apply style and create a line plot below
"""
            interaction['public']['workspace']['files'][0]['content'] = starter_content
            
            # Update solution
            solution_content = """import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data (already loaded)
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [23, 45, 56, 78]
})

# Apply style and create a line plot below
plt.style.use('ggplot')
sns.lineplot(data=df, x='category', y='value')
plt.title('Sales by Category')
plt.xlabel('Category')
plt.ylabel('Value')
"""
            interaction['grading']['solution_files'][0]['content'] = solution_content
            
            # Remove asset_mounts
            interaction['public']['workspace']['asset_mounts'] = []
        
        # Fix tile_viz_seaborn_stats_themes.s10
        # The practice is viz.seaborn_statistical_functions
        # Should use sns.barplot or sns.regplot without plt.subplots()
        elif step_id == 'tile_viz_seaborn_stats_themes.s10':
            # Update prompt
            interaction['public']['prompt'] = """A DataFrame `df` with columns `category` and `value` is already loaded.

Create a seaborn bar plot with error bars:
1. Create a bar plot using `sns.barplot(data=df, x='category', y='value')`
2. The error bars will be drawn automatically by seaborn

seaborn's barplot shows the mean value for each category with confidence intervals."""
            
            # Update starter
            starter_content = """import seaborn as sns
import pandas as pd

# Data (already loaded)
df = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'value': [23, 25, 22, 45, 47, 44, 56, 58, 55]
})

# Create a seaborn bar plot below
"""
            interaction['public']['workspace']['files'][0]['content'] = starter_content
            
            # Update solution
            solution_content = """import seaborn as sns
import pandas as pd

# Data (already loaded)
df = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'value': [23, 25, 22, 45, 47, 44, 56, 58, 55]
})

# Create a seaborn bar plot below
sns.barplot(data=df, x='category', y='value')
"""
            interaction['grading']['solution_files'][0]['content'] = solution_content
            
            # Remove asset_mounts
            interaction['public']['workspace']['asset_mounts'] = []

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed tile_viz_custom_multi_panel.s08 and tile_viz_seaborn_stats_themes.s10")
