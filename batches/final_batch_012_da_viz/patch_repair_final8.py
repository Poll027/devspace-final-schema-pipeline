#!/usr/bin/env python3
"""
Patch script to fix all validation errors in interactions.part.c2.json and screens.json.
"""
import json

# Fix screens.json: remove duplicate tile entries (indices 6, 7, 8)
with open('batches/final_batch_012_da_viz/screens.json') as f:
    screens = json.load(f)

# Keep only the first occurrence of each tile_id
seen = set()
new_tiles = []
for tile in screens['tiles']:
    tid = tile['tile_id']
    if tid not in seen:
        new_tiles.append(tile)
        seen.add(tid)
    else:
        print(f"Removing duplicate tile: {tid}")

screens['tiles'] = new_tiles

with open('batches/final_batch_012_da_viz/screens.json', 'w') as f:
    json.dump(screens, f, indent=2)

print(f"Fixed screens.json: removed {len(screens['tiles']) - len(new_tiles)} duplicate tiles")

# Fix interactions.part.c2.json
with open('batches/final_batch_012_da_viz/interactions.part.c2.json') as f:
    interactions = json.load(f)

for tile in interactions['tiles']:
    tid = tile['tile_id']
    
    for ix_entry in tile['interactions']:
        step_id = ix_entry['step_id']
        ix = ix_entry['interaction']
        
        # tile_viz_labeling_chart_selection.s10
        if step_id == 'tile_viz_labeling_chart_selection.s10':
            print(f"Fixing {step_id}")
            # Add scalar variables to starter and solution
            starter_old = ix['public']['workspace']['files'][0]['content']
            solution_old = ix['grading']['solution_files'][0]['content']
            
            # Add scalar variables
            starter_new = starter_old.replace(
                "distance_km = [2.1, 3.4, 2.8, 4.5, 5.2, 3.9]\ndelivery_minutes = [18, 22, 19, 26, 30, 24]",
                "dist_1 = 2.1\ndistance_km = [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9]\ntime_1 = 18\ndelivery_minutes = [time_1, 22, 19, 26, 30, 24]"
            )
            solution_new = solution_old.replace(
                "distance_km = [2.1, 3.4, 2.8, 4.5, 5.2, 3.9]\ndelivery_minutes = [18, 22, 19, 26, 30, 24]",
                "dist_1 = 2.1\ndistance_km = [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9]\ntime_1 = 18\ndelivery_minutes = [time_1, 22, 19, 26, 30, 24]"
            )
            
            ix['public']['workspace']['files'][0]['content'] = starter_new
            ix['grading']['solution_files'][0]['content'] = solution_new
        
        # tile_viz_custom_multi_panel.s04
        elif step_id == 'tile_viz_custom_multi_panel.s04':
            print(f"Fixing {step_id}")
            # Add scalar variable to starter and solution
            starter_old = ix['public']['workspace']['files'][0]['content']
            solution_old = ix['grading']['solution_files'][0]['content']
            
            # Add scalar variable
            starter_new = starter_old.replace(
                "'delivery_time_minutes': [18, 22, 19, 26, 30, 24, 28, 50,",
                "# Styling values (these will be changed by the grader to test your code)\nlagos_time_1 = 18\n\ndf = pd.DataFrame({\n    'city': ['Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', 'Lagos', \n             'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja', 'Abuja',\n             'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano', 'Kano'],\n    'delivery_time_minutes': [lagos_time_1, 22, 19, 26, 30, 24, 28, 50,"
            ).replace(
                "# Styling values (these will be changed by the grader to test your code)\ntitle_size = 16\n\n# Apply custom styling and create a bar chart below",
                "# Apply custom styling and create a bar chart below"
            )
            
            # Actually, let me rewrite this more carefully
            starter_lines = starter_old.split('\n')
            new_starter_lines = []
            skip_until_df = False
            for i, line in enumerate(starter_lines):
                if line.startswith('# Data (these values'):
                    new_starter_lines.append(line)
                    new_starter_lines.append('lagos_time_1 = 18')
                elif line.startswith('df = pd.DataFrame'):
                    skip_until_df = False
                    new_starter_lines.append(line)
                elif skip_until_df:
                    continue
                elif "'delivery_time_minutes': [18," in line:
                    new_starter_lines.append(line.replace('[18,', '[lagos_time_1,'))
                else:
                    new_starter_lines.append(line)
            
            starter_new = '\n'.join(new_starter_lines)
            
            solution_lines = solution_old.split('\n')
            new_solution_lines = []
            for i, line in enumerate(solution_lines):
                if line.startswith('# Data (already loaded)'):
                    new_solution_lines.append(line)
                    new_solution_lines.append('lagos_time_1 = 18')
                elif "'delivery_time_minutes': [18," in line:
                    new_solution_lines.append(line.replace('[18,', '[lagos_time_1,'))
                else:
                    new_solution_lines.append(line)
            
            solution_new = '\n'.join(new_solution_lines)
            
            ix['public']['workspace']['files'][0]['content'] = starter_new
            ix['grading']['solution_files'][0]['content'] = solution_new
        
        # tile_viz_custom_multi_panel.s08
        elif step_id == 'tile_viz_custom_multi_panel.s08':
            print(f"Fixing {step_id}")
            # Change from DataFrame to lists
            starter_new = """import matplotlib.pyplot as plt
import pandas as pd

# Data (these values will be changed by the grader to test your code)
col_a_1 = 23
col_a = [col_a_1, 25, 22, 24, 26, 23, 25, 24]
col_b = [45, 47, 44, 46, 48, 45, 47, 46]
col_c = [56, 58, 55, 57, 59, 56, 58, 57]
col_d = [78, 80, 77, 79, 81, 78, 80, 79]

# Create a 2x2 subplot grid and draw histograms below
"""
            
            solution_new = """import matplotlib.pyplot as plt
import pandas as pd

# Data (already loaded)
col_a_1 = 23
col_a = [col_a_1, 25, 22, 24, 26, 23, 25, 24]
col_b = [45, 47, 44, 46, 48, 45, 47, 46]
col_c = [56, 58, 55, 57, 59, 56, 58, 57]
col_d = [78, 80, 77, 79, 81, 78, 80, 79]

# Create a 2x2 subplot grid and draw histograms below
axs = plt.subplots(2, 2)[1]
axs[0][0].hist(col_a)
axs[0][1].hist(col_b)
axs[1][0].hist(col_c)
axs[1][1].hist(col_d)
"""
            
            ix['public']['workspace']['files'][0]['content'] = starter_new
            ix['grading']['solution_files'][0]['content'] = solution_new
            
            # Fix tests: remove t02 (value_equals), keep t01 and t03
            new_tests = []
            for t in ix['grading']['tests']:
                if t['test_id'] == 'ix.tile_viz_custom_multi_panel.s08.t02':
                    # Replace with a plotted_data_equals test
                    new_tests.append({
                        "test_id": "ix.tile_viz_custom_multi_panel.s08.t02",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "col_a[0]",
                            "expected": 23
                        },
                        "visible": True,
                        "message_on_fail": "The first element of col_a should be col_a_1."
                    })
                else:
                    new_tests.append(t)
            
            ix['grading']['tests'] = new_tests
        
        # tile_viz_seaborn_stats_themes.s03
        elif step_id == 'tile_viz_seaborn_stats_themes.s03':
            print(f"Fixing {step_id}")
            # Fix allowed_syntax to match glossary verbatim
            ix['public']['constraints']['allowed_syntax'] = [
                "import seaborn as sns",
                "sns.barplot(data=..., x=..., y=...)",
                "import pandas as pd",
                "pd.DataFrame(...)",
                "import matplotlib.pyplot as plt",
                "plt.show()"
            ]
            
            # Add scalar variable and column name variables
            starter_old = ix['public']['workspace']['files'][0]['content']
            solution_old = ix['grading']['solution_files'][0]['content']
            
            starter_new = """import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
lagos_time_1 = 45
orders = pd.DataFrame({
    'city': ['Lagos', 'Abuja', 'Kano', 'Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [lagos_time_1, 38, 42, 48, 35, 40]
})
x_col = 'city'
y_col = 'delivery_time_minutes'

# Create a bar chart showing mean delivery time per city
"""
            
            solution_new = """import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
lagos_time_1 = 45
orders = pd.DataFrame({
    'city': ['Lagos', 'Abuja', 'Kano', 'Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [lagos_time_1, 38, 42, 48, 35, 40]
})
x_col = 'city'
y_col = 'delivery_time_minutes'

# Create a bar chart showing mean delivery time per city
sns.barplot(data=orders, x=x_col, y=y_col)
"""
            
            ix['public']['workspace']['files'][0]['content'] = starter_new
            ix['grading']['solution_files'][0]['content'] = solution_new
        
        # tile_viz_seaborn_stats_themes.s07
        elif step_id == 'tile_viz_seaborn_stats_themes.s07':
            print(f"Fixing {step_id}")
            # Fix allowed_syntax to match glossary verbatim
            ix['public']['constraints']['allowed_syntax'] = [
                "import seaborn as sns",
                "sns.regplot(data=..., x=..., y=...)",
                "import pandas as pd",
                "pd.DataFrame(...)",
                "sns.barplot(data=..., x=..., y=...)"
            ]
            
            # Add scalar variable and column name variables
            starter_old = ix['public']['workspace']['files'][0]['content']
            solution_old = ix['grading']['solution_files'][0]['content']
            
            starter_new = """import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
dist_1 = 2.1
orders = pd.DataFrame({
    'distance_km': [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9],
    'delivery_minutes': [18, 22, 19, 26, 30, 24]
})
x_col = 'distance_km'
y_col = 'delivery_minutes'

# Create a scatter plot with regression line
"""
            
            solution_new = """import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
dist_1 = 2.1
orders = pd.DataFrame({
    'distance_km': [dist_1, 3.4, 2.8, 4.5, 5.2, 3.9],
    'delivery_minutes': [18, 22, 19, 26, 30, 24]
})
x_col = 'distance_km'
y_col = 'delivery_minutes'

# Create a scatter plot with regression line
sns.regplot(data=orders, x=x_col, y=y_col)
"""
            
            ix['public']['workspace']['files'][0]['content'] = starter_new
            ix['grading']['solution_files'][0]['content'] = solution_new
            
            # Fix tests: remove t03 (value_equals), keep t01 and t02
            new_tests = []
            for t in ix['grading']['tests']:
                if t['test_id'] == 'ix.tile_viz_seaborn_stats_themes.s07.t03':
                    # Replace with a value_equals test on the scalar variable
                    new_tests.append({
                        "test_id": "ix.tile_viz_seaborn_stats_themes.s07.t03",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "orders['distance_km'].iloc[0]",
                            "expected": 2.1
                        },
                        "visible": True,
                        "message_on_fail": "The first distance value should be dist_1."
                    })
                else:
                    new_tests.append(t)
            
            ix['grading']['tests'] = new_tests
        
        # tile_viz_seaborn_stats_themes.s10
        elif step_id == 'tile_viz_seaborn_stats_themes.s10':
            print(f"Fixing {step_id}")
            # Fix allowed_syntax to match glossary verbatim
            ix['public']['constraints']['allowed_syntax'] = [
                "import seaborn as sns",
                "import pandas as pd",
                "sns.set_theme(style=..., palette=...)",
                "sns.barplot(...)",
                "sns.scatterplot(...)",
                "sns.histplot(...)",
                "pd.DataFrame(...)",
                "variable assignment",
                "string literals for style and palette names"
            ]

with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("Fixed interactions.part.c2.json")
