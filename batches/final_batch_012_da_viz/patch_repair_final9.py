#!/usr/bin/env python3
"""
Fix remaining issues in interactions.part.c2.json.
"""
import json

with open('batches/final_batch_012_da_viz/interactions.part.c2.json') as f:
    interactions = json.load(f)

for tile in interactions['tiles']:
    for ix_entry in tile['interactions']:
        step_id = ix_entry['step_id']
        ix = ix_entry['interaction']
        
        # tile_viz_seaborn_stats_themes.s03: remove t02 (xticklabels test)
        if step_id == 'tile_viz_seaborn_stats_themes.s03':
            print(f"Fixing {step_id}: removing t02")
            new_tests = [t for t in ix['grading']['tests'] if t['test_id'] != 'ix.tile_viz_seaborn_stats_themes.s03.t02']
            ix['grading']['tests'] = new_tests
        
        # tile_viz_seaborn_stats_themes.s10: add scalar variable
        elif step_id == 'tile_viz_seaborn_stats_themes.s10':
            print(f"Fixing {step_id}: adding scalar variable")
            starter_old = ix['public']['workspace']['files'][0]['content']
            solution_old = ix['grading']['solution_files'][0]['content']
            
            starter_new = """import seaborn as sns
import pandas as pd

# Data (these values will be changed by the grader to test your code)
val_a_1 = 23
df = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'value': [val_a_1, 25, 22, 45, 47, 44, 56, 58, 55]
})

# Create a seaborn bar plot below
"""
            
            solution_new = """import seaborn as sns
import pandas as pd

# Data (already loaded)
val_a_1 = 23
df = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'value': [val_a_1, 25, 22, 45, 47, 44, 56, 58, 55]
})

# Create a seaborn bar plot below
sns.barplot(data=df, x='category', y='value')
"""
            
            ix['public']['workspace']['files'][0]['content'] = starter_new
            ix['grading']['solution_files'][0]['content'] = solution_new

with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print("Fixed interactions.part.c2.json")
