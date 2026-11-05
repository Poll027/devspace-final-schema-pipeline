#!/usr/bin/env python3
"""Fix the interactions.part.c2.json file based on validator errors."""

import json

# Read the file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Read the registry to get the actual data values
with open('batches/final_batch_012_da_viz/scenario_asset_registry.json', 'r') as f:
    registry = json.load(f)

# Get ds.orders data
ds_orders_rows = None
for asset in registry.get('assets', []):
    if asset.get('asset_id') == 'ds.orders':
        ds_orders_rows = asset.get('rows', [])
        break

# Extract distance_km and delivery_time_minutes from first 6 rows
distance_km = [row[3] for row in ds_orders_rows[:6]]  # index 3 is distance_km
delivery_minutes = [row[2] for row in ds_orders_rows[:6]]  # index 2 is delivery_time_minutes

print(f"distance_km: {distance_km}")
print(f"delivery_minutes: {delivery_minutes}")

# Fix 1: Update allowed_syntax and blocked_syntax for viz.chart_type_selection (s10)
viz_chart_type_allowed = [
    "import matplotlib.pyplot as plt",
    "plt.scatter(x, y)",
    "plt.xlabel()",
    "plt.ylabel()",
    "plt.title()",
    "plt.show()",
    "Python list literals",
    "variable assignment",
    "single-line comments (#)"
]

viz_chart_type_blocked = [
    "import seaborn",
    "sns.*",
    "plt.subplots() with nrows/ncols > 1",
    "plt.style.use()",
    "plt.hist()",
    "plt.bar()",
    "plt.plot()",
    "plt.boxplot()"
]

# Fix 2: Update allowed_syntax and blocked_syntax for viz.custom_styling_theming (s04, s08)
viz_custom_styling_allowed = [
    "import matplotlib as mpl",
    "import matplotlib.pyplot as plt",
    "import seaborn as sns",
    "sns.set_palette(palette_name)",
    "mpl.rcParams['axes.titlesize'] = value",
    "mpl.rcParams['lines.linewidth'] = value",
    "plt.style.use('style-name')",
    "plt.style.available",
    "sns.lineplot(data=df, x=col, y=col)",
    "sns.barplot(data=df, x=col, y=col)",
    "plt.title(str)",
    "plt.xlabel(str)",
    "plt.ylabel(str)",
    "plt.show()"
]

viz_custom_styling_blocked = [
    "plt.subplots(nrows, ncols)",
    "fig.add_subplot()",
    "axes[i]",
    "FacetGrid",
    "GridSpec"
]

# Fix 3: Update allowed_syntax and blocked_syntax for viz.seaborn_statistical_functions (s10)
viz_seaborn_stat_allowed = [
    "import seaborn as sns",
    "sns.regplot(data=..., x=..., y=...)",
    "import pandas as pd",
    "pd.DataFrame(...)",
    "sns.barplot(data=..., x=..., y=...)"
]

viz_seaborn_stat_blocked = [
    "sns.set_theme()",
    "sns.set_style()",
    "sns.set_palette()",
    "plt.subplots()",
    "fig, axes",
    "sns.FacetGrid()",
    "sns.lmplot()"
]

# Process each tile
for tile in data['tiles']:
    tile_id = tile['tile_id']
    
    # Remove extra remediation steps
    if tile_id in ['tile_viz_labeling_chart_selection', 'tile_viz_seaborn_stats_themes']:
        tile['interactions'] = [ix for ix in tile['interactions'] 
                                if not ix['step_id'].endswith(('.r01', '.r02', '.r03'))]
    
    for ix in tile['interactions']:
        step_id = ix['step_id']
        interaction = ix['interaction']
        
        # Fix tile_viz_labeling_chart_selection.s10
        if step_id == 'tile_viz_labeling_chart_selection.s10':
            # Update constraints
            interaction['public']['constraints']['allowed_syntax'] = viz_chart_type_allowed
            interaction['public']['constraints']['blocked_syntax'] = viz_chart_type_blocked
            
            # Fix the prompt to ask for scatter plot
            interaction['public']['prompt'] = """Two lists are provided: `distance_km` and `delivery_minutes`, each containing six delivery records.

Create a scatter plot showing the relationship between distance and delivery time:
1. Create a scatter plot with `distance_km` on the x-axis and `delivery_minutes` on the y-axis
2. Set the x-axis label to `'Distance (km)'`
3. Set the y-axis label to `'Delivery time (minutes)'`

Use `plt.scatter()`, `plt.xlabel()`, and `plt.ylabel()`."""
            
            # Fix the starter - provide data as lists, no pandas
            starter_content = f"""import matplotlib.pyplot as plt

# Data
distance_km = {distance_km}
delivery_minutes = {delivery_minutes}

# Create a scatter plot showing the relationship between distance and delivery time
"""
            interaction['public']['workspace']['files'][0]['content'] = starter_content
            
            # Remove asset_mounts since we're not using CSV
            interaction['public']['workspace']['asset_mounts'] = []
            
            # Fix the solution
            solution_content = f"""import matplotlib.pyplot as plt

# Data
distance_km = {distance_km}
delivery_minutes = {delivery_minutes}

# Create a scatter plot showing the relationship between distance and delivery time
plt.scatter(distance_km, delivery_minutes)
plt.xlabel('Distance (km)')
plt.ylabel('Delivery time (minutes)')
"""
            interaction['grading']['solution_files'][0]['content'] = solution_content
            
            # Update test expected values to match the actual data
            for test in interaction['grading']['tests']:
                if test['test_id'].endswith('.t02'):
                    test['spec']['expected'] = distance_km
                    test['message_on_fail'] = "The scatter plot's x-values should be the distance_km list. Call `plt.scatter(distance_km, delivery_minutes)`."
                elif test['test_id'].endswith('.t03'):
                    test['spec']['expected'] = delivery_minutes
                    test['message_on_fail'] = "The scatter plot's y-values should be the delivery_minutes list. Call `plt.scatter(distance_km, delivery_minutes)`."
            
            # Update feedback
            interaction['feedback']['correct']['message'] = "Great work! Your scatter plot shows the relationship between distance and delivery time with properly labeled axes."
            interaction['feedback']['incorrect']['message'] = "Make sure you called `plt.scatter(distance_km, delivery_minutes)` and added both axis labels."
            interaction['feedback']['hints'] = [
                "A scatter plot is used when you want to see the relationship between two numerical variables.",
                "Use `plt.scatter(x, y)` to create a scatter plot, then `plt.xlabel()` and `plt.ylabel()` to add labels."
            ]
        
        # Fix tile_viz_custom_multi_panel.s04
        elif step_id == 'tile_viz_custom_multi_panel.s04':
            # Update constraints
            interaction['public']['constraints']['allowed_syntax'] = viz_custom_styling_allowed
            interaction['public']['constraints']['blocked_syntax'] = viz_custom_styling_blocked
        
        # Fix tile_viz_custom_multi_panel.s08
        elif step_id == 'tile_viz_custom_multi_panel.s08':
            # Update constraints
            interaction['public']['constraints']['allowed_syntax'] = viz_custom_styling_allowed
            interaction['public']['constraints']['blocked_syntax'] = viz_custom_styling_blocked
        
        # Fix tile_viz_seaborn_stats_themes.s10
        elif step_id == 'tile_viz_seaborn_stats_themes.s10':
            # Update constraints
            interaction['public']['constraints']['allowed_syntax'] = viz_seaborn_stat_allowed
            interaction['public']['constraints']['blocked_syntax'] = viz_seaborn_stat_blocked

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed interactions.part.c2.json")
print(f"Used distance_km: {distance_km}")
print(f"Used delivery_minutes: {delivery_minutes}")
