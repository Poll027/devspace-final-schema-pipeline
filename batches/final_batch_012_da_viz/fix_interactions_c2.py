#!/usr/bin/env python3
"""Fix interactions.part.c2.json errors."""

import json

# Load the file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json') as f:
    data = json.load(f)

# Load glossary for practice anchors
with open('batches/final_batch_012_da_viz/inputs/path_glossary_bundle.json') as f:
    bundle = json.load(f)

# Build practice anchor map
practice_anchors = {}
for b in bundle['bundles']:
    cid = b['context']['concept_id']
    pa = b.get('practice_anchor', {})
    if pa:
        practice_anchors[cid] = pa

# Helper to find interaction by step_id
def find_interaction(tile_id, step_id):
    for tile in data['tiles']:
        if tile['tile_id'] == tile_id:
            for ix_entry in tile['interactions']:
                if ix_entry['step_id'] == step_id:
                    return ix_entry['interaction']
    return None

# Fix 1: tile_viz_labeling_chart_selection.s10
# Remove xlabel/ylabel from prompt, solution, tests t04/t05
ix = find_interaction('tile_viz_labeling_chart_selection', 'tile_viz_labeling_chart_selection.s10')
if ix:
    # Update prompt - remove xlabel/ylabel requirements
    ix['public']['prompt'] = "Two lists are provided: `distance_km` and `delivery_minutes`, each containing six delivery records.\n\nCreate a scatter plot showing the relationship between distance and delivery time:\n1. Create a scatter plot with `distance_km` on the x-axis and `delivery_minutes` on the y-axis\n\nUse `plt.scatter(distance_km, delivery_minutes)`."
    
    # Update solution - remove xlabel/ylabel
    ix['grading']['solution_files'][0]['content'] = "import matplotlib.pyplot as plt\n\n# Data\ndistance_km = [2.1, 3.4, 2.8, 4.5, 5.2, 3.9]\ndelivery_minutes = [18, 22, 19, 26, 30, 24]\n\n# Create a scatter plot showing the relationship between distance and delivery time\nplt.scatter(distance_km, delivery_minutes)\n"
    
    # Remove tests t04 and t05 (xlabel/ylabel)
    ix['grading']['tests'] = [t for t in ix['grading']['tests'] if t['test_id'] not in ['ix.tile_viz_labeling_chart_selection.s10.t04', 'ix.tile_viz_labeling_chart_selection.s10.t05']]
    
    # Update feedback
    ix['feedback']['incorrect']['message'] = "Make sure you called `plt.scatter(distance_km, delivery_minutes)`."
    ix['feedback']['hints'][1] = "Use `plt.scatter(x, y)` to create a scatter plot."
    
    print("Fixed tile_viz_labeling_chart_selection.s10")

# Fix 2: tile_viz_custom_multi_panel.s04
# Add title_size to starter, use it in solution, fix expected values
ix = find_interaction('tile_viz_custom_multi_panel', 'tile_viz_custom_multi_panel.s04')
if ix:
    # Add title_size to starter
    starter_content = ix['public']['workspace']['files'][0]['content']
    # Insert title_size before the comment
    lines = starter_content.split('\n')
    insert_idx = None
    for i, line in enumerate(lines):
        if '# Apply custom styling' in line:
            insert_idx = i
            break
    if insert_idx:
        lines.insert(insert_idx, '# Styling values (these will be changed by the grader to test your code)')
        lines.insert(insert_idx + 1, 'title_size = 16')
        lines.insert(insert_idx + 2, '')
        ix['public']['workspace']['files'][0]['content'] = '\n'.join(lines)
    
    # Update solution to use title_size
    solution_content = ix['grading']['solution_files'][0]['content']
    solution_content = solution_content.replace("mpl.rcParams['axes.titlesize'] = 16", "mpl.rcParams['axes.titlesize'] = title_size")
    ix['grading']['solution_files'][0]['content'] = solution_content
    
    # Fix t01 expected - should be bar only, not bar+line
    for t in ix['grading']['tests']:
        if t['test_id'] == 'ix.tile_viz_custom_multi_panel.s04.t01':
            t['spec']['expected']['chart_types'] = [['bar']]
    
    # Fix t03 expected - compute correct values from the data
    # The data has 8 values per city: Lagos [18,22,19,26,30,24,28,50], Abuja [25,28,23,32,35,27,31,55], Kano [27,31,26,35,38,29,34,60]
    # Means: Lagos = 27.125, Abuja = 32.0, Kano = 35.0
    for t in ix['grading']['tests']:
        if t['test_id'] == 'ix.tile_viz_custom_multi_panel.s04.t03':
            t['spec']['expected'] = [27.125, 32.0, 35.0]
            t['message_on_fail'] = "The bar chart should show the mean delivery time for each city. Call `sns.barplot(data=df, x='city', y='delivery_time_minutes')`."
    
    print("Fixed tile_viz_custom_multi_panel.s04")

# Fix 3: tile_viz_custom_multi_panel.s08
# Copy allowed/blocked_syntax from viz.multi_panel_figures, fix solution
ix = find_interaction('tile_viz_custom_multi_panel', 'tile_viz_custom_multi_panel.s08')
if ix:
    # Get the correct practice anchor
    pa = practice_anchors.get('viz.multi_panel_figures', {})
    lc = pa.get('live_code', {})
    
    # Copy allowed/blocked_syntax
    ix['public']['constraints']['allowed_syntax'] = lc.get('allowed_syntax', [])
    ix['public']['constraints']['blocked_syntax'] = lc.get('blocked_syntax', [])
    
    # Fix solution - should create 2x2 subplots with histograms
    # The prompt says "Apply a matplotlib style and create a styled line plot" but that's wrong for multi_panel_figures
    # The practice anchor is about creating subplot grids
    # Fix the prompt and solution to match the practice anchor
    ix['public']['prompt'] = "A DataFrame `df` with columns `col_a`, `col_b`, `col_c`, and `col_d` is already loaded.\n\nCreate a 2×2 subplot grid and draw a histogram in each panel:\n1. Create a 2×2 grid using `fig, axs = plt.subplots(2, 2)`\n2. Draw a histogram of `col_a` in the top-left panel: `axs[0, 0].hist(df['col_a'])`\n3. Draw a histogram of `col_b` in the top-right panel: `axs[0, 1].hist(df['col_b'])`\n4. Draw a histogram of `col_c` in the bottom-left panel: `axs[1, 0].hist(df['col_c'])`\n5. Draw a histogram of `col_d` in the bottom-right panel: `axs[1, 1].hist(df['col_d'])`\n\nEach panel will show the distribution of one column."
    
    # Fix runtime - remove seaborn
    ix['public']['runtime']['packages'] = ['matplotlib', 'pandas']
    
    # Fix workspace starter
    ix['public']['workspace']['files'][0]['content'] = "import matplotlib.pyplot as plt\nimport pandas as pd\n\n# Data (already loaded)\ndf = pd.DataFrame({\n    'col_a': [23, 25, 22, 24, 26, 23, 25, 24],\n    'col_b': [45, 47, 44, 46, 48, 45, 47, 46],\n    'col_c': [56, 58, 55, 57, 59, 56, 58, 57],\n    'col_d': [78, 80, 77, 79, 81, 78, 80, 79]\n})\n\n# Create a 2x2 subplot grid and draw histograms below\n"
    
    # Fix solution
    ix['grading']['solution_files'][0]['content'] = "import matplotlib.pyplot as plt\nimport pandas as pd\n\n# Data (already loaded)\ndf = pd.DataFrame({\n    'col_a': [23, 25, 22, 24, 26, 23, 25, 24],\n    'col_b': [45, 47, 44, 46, 48, 45, 47, 46],\n    'col_c': [56, 58, 55, 57, 59, 56, 58, 57],\n    'col_d': [78, 80, 77, 79, 81, 78, 80, 79]\n})\n\n# Create a 2x2 subplot grid and draw histograms below\nfig, axs = plt.subplots(2, 2)\naxs[0, 0].hist(df['col_a'])\naxs[0, 1].hist(df['col_b'])\naxs[1, 0].hist(df['col_c'])\naxs[1, 1].hist(df['col_d'])\n"
    
    # Fix tests
    ix['grading']['tests'] = [
        {
            "test_id": "ix.tile_viz_custom_multi_panel.s08.t01",
            "kind": "figure_equals",
            "spec": {
                "expected": {
                    "n_axes": 4,
                    "chart_types": [["hist"], ["hist"], ["hist"], ["hist"]]
                }
            },
            "visible": True,
            "message_on_fail": "Your figure should contain 4 axes (2×2 grid), each with a histogram. Use `fig, axs = plt.subplots(2, 2)` and call `.hist()` on each `axs[row, col]`."
        },
        {
            "test_id": "ix.tile_viz_custom_multi_panel.s08.t02",
            "kind": "plotted_data_equals",
            "spec": {
                "chart": "hist",
                "field": "heights",
                "axes": 0,
                "expected": [23, 25, 22, 24, 26, 23, 25, 24],
                "sorted": True
            },
            "visible": True,
            "message_on_fail": "The top-left panel (axs[0, 0]) should show a histogram of col_a. Call `axs[0, 0].hist(df['col_a'])`."
        }
    ]
    
    print("Fixed tile_viz_custom_multi_panel.s08")

# Fix 4: tile_viz_seaborn_stats_themes.s03
# Copy allowed/blocked_syntax from viz.seaborn_dataframe_plotting, fix solution
ix = find_interaction('tile_viz_seaborn_stats_themes', 'tile_viz_seaborn_stats_themes.s03')
if ix:
    # Get the correct practice anchor
    pa = practice_anchors.get('viz.seaborn_dataframe_plotting', {})
    lc = pa.get('live_code', {})
    
    # Copy allowed/blocked_syntax
    ix['public']['constraints']['allowed_syntax'] = lc.get('allowed_syntax', [])
    ix['public']['constraints']['blocked_syntax'] = lc.get('blocked_syntax', [])
    
    # Fix solution - should use sns.barplot only
    ix['grading']['solution_files'][0]['content'] = "import matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns\n\n# Data\ndf = pd.read_csv('city_data.csv')\n\nsns.barplot(data=df, x='city', y='delivery_time_minutes')\n"
    
    # Fix prompt to match
    ix['public']['prompt'] = "The `orders` DataFrame is already loaded with columns `'city'` and `'delivery_time_minutes'`.\n\nCall `sns.barplot(data=orders, x='city', y='delivery_time_minutes')` to produce a bar chart showing the mean delivery time per city.\n\nThe figure should show one bar per city (Abuja, Kano, Lagos), with error bars drawn automatically by seaborn."
    
    # Fix starter
    ix['public']['workspace']['files'][0]['content'] = "import matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns\n\n# Data\norders = pd.read_csv('city_data.csv')\n\n# Create a bar chart showing mean delivery time per city\n"
    
    print("Fixed tile_viz_seaborn_stats_themes.s03")

# Fix 5: tile_viz_seaborn_stats_themes.s07
# Copy allowed/blocked_syntax from viz.seaborn_statistical_functions
ix = find_interaction('tile_viz_seaborn_stats_themes', 'tile_viz_seaborn_stats_themes.s07')
if ix:
    # Get the correct practice anchor
    pa = practice_anchors.get('viz.seaborn_statistical_functions', {})
    lc = pa.get('live_code', {})
    
    # Copy allowed/blocked_syntax
    ix['public']['constraints']['allowed_syntax'] = lc.get('allowed_syntax', [])
    ix['public']['constraints']['blocked_syntax'] = lc.get('blocked_syntax', [])
    
    # Fix solution - should use sns.regplot
    ix['grading']['solution_files'][0]['content'] = "import matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns\n\n# Data\norders = pd.read_csv('metrics.csv')\n\nsns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')\n"
    
    # Fix prompt
    ix['public']['prompt'] = "The `orders` DataFrame is already loaded with columns `'distance_km'` and `'delivery_time_minutes'`.\n\nCall `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')` to produce a scatter plot of the observations with a fitted linear regression line drawn through them.\n\nThe figure should show individual data points and a fitted trend line, produced by a single `sns.regplot()` call."
    
    # Fix starter
    ix['public']['workspace']['files'][0]['content'] = "import matplotlib.pyplot as plt\nimport pandas as pd\nimport seaborn as sns\n\n# Data\norders = pd.read_csv('metrics.csv')\n\n# Create a scatter plot with regression line\n"
    
    print("Fixed tile_viz_seaborn_stats_themes.s07")

# Fix 6: tile_viz_seaborn_stats_themes.s10
# Remove xlabel/ylabel, keep only barplot
ix = find_interaction('tile_viz_seaborn_stats_themes', 'tile_viz_seaborn_stats_themes.s10')
if ix:
    # Update prompt - remove xlabel/ylabel
    ix['public']['prompt'] = "A DataFrame `df` with columns `category` and `value` is already loaded.\n\nCreate a seaborn bar plot:\n1. Create a bar plot using `sns.barplot(data=df, x='category', y='value')`\n\nseaborn's barplot shows the mean value for each category with confidence intervals (error bars)."
    
    # Update solution
    ix['grading']['solution_files'][0]['content'] = "import seaborn as sns\nimport pandas as pd\n\n# Data (already loaded)\ndf = pd.DataFrame({\n    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],\n    'value': [23, 25, 22, 45, 47, 44, 56, 58, 55]\n})\n\n# Create a seaborn bar plot below\nsns.barplot(data=df, x='category', y='value')\n"
    
    # Fix t02 expected - compute correct values
    # A: [23, 25, 22] mean = 23.333..., B: [45, 47, 44] mean = 45.333..., C: [56, 58, 55] mean = 56.333...
    for t in ix['grading']['tests']:
        if t['test_id'] == 'ix.tile_viz_seaborn_stats_themes.s10.t02':
            t['spec']['expected'] = [23.333333333333332, 45.333333333333336, 56.333333333333336]
            t['message_on_fail'] = "The bar chart should show the mean value for each category. Call `sns.barplot(data=df, x='category', y='value')`."
    
    # Update feedback
    ix['feedback']['incorrect']['message'] = "Make sure you called `sns.barplot(data=df, x='category', y='value')`."
    ix['feedback']['hints'] = [
        "seaborn's barplot automatically computes the mean per category.",
        "The three keyword arguments are `data=df`, `x='category'`, and `y='value'`."
    ]
    
    print("Fixed tile_viz_seaborn_stats_themes.s10")

# Write the fixed file
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nFixed interactions.part.c2.json")
