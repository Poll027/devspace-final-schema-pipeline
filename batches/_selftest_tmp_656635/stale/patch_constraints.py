#!/usr/bin/env python3
"""Patch interactions to add missing constraints fields."""

import json

# Read the interactions file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Define the constraints for each practice
constraints_map = {
    'tile_capstone_integrate_tools_model.s05': {
        'allowed_syntax': [
            "SELECT",
            "FROM",
            "INNER JOIN ... ON",
            "WHERE",
            "AND",
            "GROUP BY",
            "AVG()",
            "table alias (e.g. o, d)",
            "date literal comparison (>=, <)",
            "column dot notation (e.g. o.zone, o.driver_id)"
        ],
        'blocked_syntax': [
            "HAVING",
            "LEFT JOIN",
            "RIGHT JOIN",
            "FULL OUTER JOIN",
            "subquery",
            "CTE (WITH ...)",
            "UNION",
            "FORMAT()",
            "CASE",
            "COALESCE",
            "ORDER BY"
        ]
    },
    'tile_capstone_integrate_tools_model.s15': {
        'allowed_syntax': [
            "import pandas as pd",
            "pd.DataFrame()",
            "df['column'].isna()",
            "df.dropna()",
            "df.fillna(value)",
            "df.groupby('column')['column'].mean()",
            "df.groupby('column').agg()",
            "variable assignment",
            "print()",
            "f-strings",
            "basic arithmetic operators",
            "for loops",
            "if/elif/else",
            "list and dict literals",
            "pd.read_csv()"
        ],
        'blocked_syntax': [
            "df.describe()",
            "df.merge()",
            "df.pivot_table()",
            "df.melt()",
            "matplotlib.pyplot",
            "seaborn",
            "df.apply()",
            "df.map()",
            "df.concat()",
            "df.to_csv()"
        ]
    },
    'tile_capstone_stats_dashboard.s10': {
        'allowed_syntax': [
            "plt.subplots(nrows, ncols)",
            "axs[row, col].plot(...)",
            "axs[row, col].bar(...)",
            "axs[row, col].hist(...)",
            "axs[row, col].set_title(...)",
            "plt.subplot(131)",
            "plt.subplot(132)",
            "plt.subplot(133)",
            "plt.suptitle(...)",
            "plt.tight_layout()",
            "plt.show()",
            "ax.set_xlabel(...)",
            "ax.set_ylabel(...)",
            "sns.barplot(..., ax=ax)",
            "sns.histplot(..., ax=ax)",
            "sns.boxplot(..., ax=ax)",
            "df['column'].value_counts()",
            "df.groupby(...).mean()",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns"
        ],
        'blocked_syntax': []
    }
}

# Patch the interactions
for tile in data['tiles']:
    for interaction in tile['interactions']:
        step_id = interaction['step_id']
        if step_id in constraints_map:
            # Add the constraints field
            interaction['interaction']['constraints'] = constraints_map[step_id]
            print(f"Added constraints to {step_id}")

# Write the patched file
with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nPatching complete!")
