#!/usr/bin/env python3
"""Final fix: Update constraints to use validator-detectable syntax descriptors."""

import json

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        ix = interaction['interaction']
        
        if step_id == 'tile_capstone_integrate_tools_model.s05':
            # SQL - keep glossary base but add validator-detectable equivalents
            new_allowed = [
                "SELECT", "FROM", "WHERE", "AND", "GROUP BY",
                "JOIN / INNER JOIN", "ON",  # validator names for INNER JOIN
                "AVG",  # validator name for AVG()
                "< > <= >= = <> !=",  # validator name for comparisons
                "alias.column qualification",  # validator name for o.zone
                "table alias (FROM table AS alias)",  # validator name for aliases
            ]
            new_blocked = [
                "HAVING", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN",
                "subquery in WHERE", "WITH name AS (...)", "UNION",
                "CASE WHEN ... THEN ... ELSE ... END", "COALESCE", "ORDER BY"
            ]
            ix['constraints'] = {'allowed_syntax': new_allowed, 'blocked_syntax': new_blocked}
            ix['public']['constraints'] = {'allowed_syntax': new_allowed, 'blocked_syntax': new_blocked}
            
        elif step_id == 'tile_capstone_integrate_tools_model.s15':
            # Python - add attr_module
            base_allowed = [
                "import pandas as pd", "pd.read_csv()", "df.dropna()", 
                "df.groupby('column')['column'].mean()", "print()",
                "variable assignment", "attr_module"
            ]
            base_blocked = ["df.describe()", "df.merge()", "matplotlib.pyplot", "seaborn"]
            ix['constraints'] = {'allowed_syntax': base_allowed, 'blocked_syntax': base_blocked}
            ix['public']['constraints'] = {'allowed_syntax': base_allowed, 'blocked_syntax': base_blocked}
            
        elif step_id == 'tile_capstone_stats_dashboard.s10':
            # Chart - add all needed attr descriptors
            base_allowed = [
                "plt.subplot(131)", "plt.subplot(132)", "plt.subplot(133)",
                "plt.bar(...)", "plt.hist(...)", "plt.title(...)", "plt.suptitle(...)",
                "plt.tight_layout()", "df['column'].value_counts()", "df.groupby(...).mean()",
                "import matplotlib.pyplot as plt", "import pandas as pd",
                "attr_module", "attr:keys", "attr:notna"
            ]
            ix['constraints'] = {'allowed_syntax': base_allowed, 'blocked_syntax': []}
            ix['public']['constraints'] = {'allowed_syntax': base_allowed, 'blocked_syntax': []}

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Final constraints fix complete")
