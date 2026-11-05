#!/usr/bin/env python3
"""Fix solutions to work with actual registry data."""

import json

def main():
    # Load the interactions file
    with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
        data = json.load(f)
    
    # Define correct solutions for each step
    solutions = {
        'tile_viz_labeling_chart_selection.s10': """import matplotlib.pyplot as plt
import pandas as pd

# Data
df = pd.read_csv('delivery_times.csv')

fig, ax = plt.subplots()
city_avg = df.groupby('city')['delivery_time_minutes'].mean()
ax.bar(city_avg.index, city_avg.values)
ax.set_title('Delivery Times by City')
ax.set_xlabel('City')
ax.set_ylabel('Average delivery time (minutes)')
""",
        'tile_viz_custom_multi_panel.s04': """import matplotlib.pyplot as plt
import pandas as pd

# Data
df = pd.read_csv('sales.csv')

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.bar(df['category'], df['value'])
""",
        'tile_viz_custom_multi_panel.s08': """import matplotlib.pyplot as plt
import pandas as pd

# Data
df = pd.read_csv('delivery_times.csv')

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].hist(df['delivery_time_minutes'])

city_counts = df['city'].value_counts()
axes[1].bar(city_counts.index, city_counts.values)
""",
        'tile_viz_seaborn_stats_themes.s03': """import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
df = pd.read_csv('city_data.csv')

fig, ax = plt.subplots()
city_avg = df.groupby('city')['delivery_time_minutes'].mean()
ax.bar(city_avg.index, city_avg.values)
""",
        'tile_viz_seaborn_stats_themes.s07': """import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
df = pd.read_csv('metrics.csv')

fig, ax = plt.subplots()
ax.scatter(df['distance_km'], df['delivery_minutes'])
""",
        'tile_viz_seaborn_stats_themes.s10': """import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Data
df = pd.read_csv('sales.csv')

sns.set_theme(style='darkgrid')
fig, ax = plt.subplots()
ax.bar(df['category'], df['value'])
"""
    }
    
    changes = []
    
    # Process each tile
    for tile in data['tiles']:
        for interaction_entry in tile['interactions']:
            step_id = interaction_entry['step_id']
            interaction = interaction_entry['interaction']
            
            if step_id in solutions:
                # Update solution
                interaction['grading']['solution_files'][0]['content'] = solutions[step_id]
                changes.append(f"Updated solution for {step_id}")
                
                # Update starter
                solution_lines = solutions[step_id].strip().split('\n')
                starter_lines = []
                for line in solution_lines:
                    if line.startswith('import ') or line.startswith('from ') or '# Data' in line or 'pd.read_csv' in line or line.startswith('df = '):
                        starter_lines.append(line)
                    elif line.strip() == '':
                        starter_lines.append(line)
                    else:
                        break
                
                starter_lines.append('')
                starter_lines.append('# Your code here')
                starter_content = '\n'.join(starter_lines) + '\n'
                
                interaction['workspace']['files'][0]['content'] = starter_content
                changes.append(f"Updated starter for {step_id}")
    
    # Write the updated file
    with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Applied {len(changes)} changes:")
    for change in changes:
        print(f"  - {change}")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
