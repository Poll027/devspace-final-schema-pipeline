#!/usr/bin/env python3
"""Final targeted fix based on validation errors."""
import json

def main():
    with open('interactions.part.c2.json') as f:
        data = json.load(f)
    
    # Remove all remediation interactions that aren't in the plan
    for tile in data['tiles']:
        tile['interactions'] = [i for i in tile['interactions'] 
                               if not i['step_id'].endswith(('.r01', '.r02', '.r03'))]
    
    # Fix specific interactions
    for tile in data['tiles']:
        tile_id = tile['tile_id']
        
        for interaction_obj in tile['interactions']:
            step_id = interaction_obj['step_id']
            interaction = interaction_obj['interaction']
            
            # Fix s03: Use correct CSV filename
            if step_id == 'tile_viz_seaborn_stats_themes.s03':
                for file in interaction['grading']['solution_files']:
                    if file['path'] == 'solution.py':
                        file['content'] = file['content'].replace('metrics.csv', 'city_data.csv')
            
            # Fix s07: Update expected data and copy allowed_syntax exactly
            if step_id == 'tile_viz_seaborn_stats_themes.s07':
                # Copy allowed_syntax exactly from glossary
                interaction['public']['constraints']['allowed_syntax'] = [
                    "import seaborn as sns",
                    "sns.regplot(data=..., x=..., y=...)",
                    "import pandas as pd",
                    "pd.DataFrame(...)",
                    "sns.barplot(data=..., x=..., y=...)"
                ]
                # Update expected data in t02
                for test in interaction['grading']['tests']:
                    if test['test_id'] == 'ix.tile_viz_seaborn_stats_themes.s07.t02':
                        test['spec']['expected'] = [1.2, 2.5, 3.8, 4.1, 5.6, 6.3]
            
            # Fix s10: Copy allowed_syntax exactly from glossary
            if step_id == 'tile_viz_seaborn_stats_themes.s10':
                interaction['public']['constraints']['allowed_syntax'] = [
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
                interaction['public']['constraints']['blocked_syntax'] = [
                    "matplotlib.rcParams direct manipulation",
                    "sns.set_style()",
                    "sns.set_palette()",
                    "plt.style.use()",
                    "custom theme dictionaries",
                    "subplots / multi-panel figures"
                ]
            
            # Fix s08: Copy allowed_syntax exactly from glossary
            if step_id == 'tile_viz_custom_multi_panel.s08':
                interaction['public']['constraints']['allowed_syntax'] = [
                    "plt.subplots(2, 2)",
                    "axs[0, 0].hist(...)",
                    "axs[0, 1].hist(...)",
                    "axs[1, 0].hist(...)",
                    "axs[1, 1].hist(...)",
                    "axs[row, col].set_title(...)",
                    "axs[row, col].set_xlabel(...)",
                    "axs[row, col].set_ylabel(...)",
                    "plt.tight_layout()",
                    "plt.show()"
                ]
                interaction['public']['constraints']['blocked_syntax'] = []
    
    with open('interactions.part.c2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Applied targeted fixes")

if __name__ == '__main__':
    main()
