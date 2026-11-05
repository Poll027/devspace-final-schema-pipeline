#!/usr/bin/env python3
"""Patch interactions.part.c2.json to add remediation_step_id references."""

import json

# Read the interactions file
with open('interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Read screens to see what remediation steps actually exist
with open('screens.json', 'r') as f:
    screens_data = json.load(f)

# Build dict of available remediation steps per tile
screens_dict = {t['tile_id']: t for t in screens_data['tiles']}

# Define which steps need remediation_step_id
# Based on: first check/hands_on per concept
remediation_mapping = {
    'tile_viz_custom_multi_panel': {
        'tile_viz_custom_multi_panel.s02': 'tile_viz_custom_multi_panel.r01',  # first for viz.custom_styling_theming
        'tile_viz_custom_multi_panel.s07': 'tile_viz_custom_multi_panel.r02',  # first for viz.multi_panel_figures (r02, not r03!)
    },
    'tile_viz_seaborn_stats_themes': {
        'tile_viz_seaborn_stats_themes.s02': 'tile_viz_seaborn_stats_themes.r01',  # first for viz.seaborn_dataframe_plotting
        'tile_viz_seaborn_stats_themes.s05': 'tile_viz_seaborn_stats_themes.r02',  # first for viz.seaborn_statistical_functions
        'tile_viz_seaborn_stats_themes.s09': 'tile_viz_seaborn_stats_themes.r03',  # first for viz.seaborn_themes_palettes
    }
}

# Verify remediation steps exist
for tile_id, mappings in remediation_mapping.items():
    tile_screen = screens_dict.get(tile_id)
    if tile_screen:
        available_rems = [r['step_id'] for r in tile_screen.get('remediation_steps', [])]
        print(f'{tile_id} has remediation steps: {available_rems}')
        for step_id, rem_id in mappings.items():
            if rem_id not in available_rems:
                print(f'  WARNING: {rem_id} not in available remediation steps!')

# Patch the interactions
for tile in data['tiles']:
    tile_id = tile['tile_id']
    if tile_id in remediation_mapping:
        for interaction in tile['interactions']:
            step_id = interaction['step_id']
            if step_id in remediation_mapping[tile_id]:
                remediation_step_id = remediation_mapping[tile_id][step_id]
                # Add remediation_step_id to feedback
                if 'feedback' in interaction['interaction']:
                    interaction['interaction']['feedback']['remediation_step_id'] = remediation_step_id
                    print(f'Added remediation_step_id to {step_id}: {remediation_step_id}')

# Write back
with open('interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('\nPatching complete.')
