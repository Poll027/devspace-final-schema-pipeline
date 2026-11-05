#!/usr/bin/env python3
"""Quick check for the specific errors."""

import json
import sys

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

# Load tile_lessons
tiles_to_check = [
    ('tile_viz_labeling_chart_selection', 'tile_viz_labeling_chart_selection.s10'),
    ('tile_viz_custom_multi_panel', 'tile_viz_custom_multi_panel.s04'),
    ('tile_viz_custom_multi_panel', 'tile_viz_custom_multi_panel.s08'),
    ('tile_viz_seaborn_stats_themes', 'tile_viz_seaborn_stats_themes.s03'),
    ('tile_viz_seaborn_stats_themes', 'tile_viz_seaborn_stats_themes.s07'),
    ('tile_viz_seaborn_stats_themes', 'tile_viz_seaborn_stats_themes.s10'),
]

errors = []

for tile_id, step_id in tiles_to_check:
    with open(f'batches/final_batch_012_da_viz/tile_lessons/{tile_id}.json') as f:
        tl = json.load(f)
    
    for s in tl['steps']:
        if s['step_id'] == step_id:
            ix = s.get('interaction', {})
            if not ix:
                errors.append(f"{step_id}: no interaction")
                continue
            
            # Check 1: solution should not use lit_str for chart_type_selection.s10
            if step_id == 'tile_viz_labeling_chart_selection.s10':
                solution = ix['grading']['solution_files'][0]['content']
                if "plt.xlabel(" in solution or "plt.ylabel(" in solution:
                    errors.append(f"{step_id}: solution still uses xlabel/ylabel (lit_str)")
                tests = ix['grading']['tests']
                if any('xlabel' in t['test_id'] or 'ylabel' in t['test_id'] for t in tests):
                    errors.append(f"{step_id}: still has xlabel/ylabel tests")
            
            # Check 2: s04 should use title_size variable
            if step_id == 'tile_viz_custom_multi_panel.s04':
                solution = ix['grading']['solution_files'][0]['content']
                if "= 16" in solution and "title_size = 16" not in solution:
                    errors.append(f"{step_id}: solution still uses literal 16 instead of title_size")
                starter = ix['public']['workspace']['files'][0]['content']
                if "title_size = 16" not in starter:
                    errors.append(f"{step_id}: starter missing title_size = 16")
                # Check expected values
                for t in ix['grading']['tests']:
                    if t['test_id'] == 'ix.tile_viz_custom_multi_panel.s04.t03':
                        expected = t['spec']['expected']
                        if expected != [27.125, 32.0, 35.0]:
                            errors.append(f"{step_id}: t03 expected is {expected}, should be [27.125, 32.0, 35.0]")
            
            # Check 3: s08 should use multi_panel_figures practice anchor
            if step_id == 'tile_viz_custom_multi_panel.s08':
                pa = practice_anchors.get('viz.multi_panel_figures', {})
                lc = pa.get('live_code', {})
                allowed = ix['public']['constraints']['allowed_syntax']
                if allowed != lc.get('allowed_syntax', []):
                    errors.append(f"{step_id}: allowed_syntax doesn't match viz.multi_panel_figures")
                solution = ix['grading']['solution_files'][0]['content']
                if "import seaborn" in solution or "sns." in solution:
                    errors.append(f"{step_id}: solution still uses seaborn")
            
            # Check 4: s03 should use seaborn_dataframe_plotting practice anchor
            if step_id == 'tile_viz_seaborn_stats_themes.s03':
                pa = practice_anchors.get('viz.seaborn_dataframe_plotting', {})
                lc = pa.get('live_code', {})
                allowed = ix['public']['constraints']['allowed_syntax']
                if allowed != lc.get('allowed_syntax', []):
                    errors.append(f"{step_id}: allowed_syntax doesn't match viz.seaborn_dataframe_plotting")
                solution = ix['grading']['solution_files'][0]['content']
                if ".groupby(" in solution or ".bar(" in solution or "fig, ax" in solution:
                    errors.append(f"{step_id}: solution uses disallowed syntax")
            
            # Check 5: s07 should use seaborn_statistical_functions practice anchor
            if step_id == 'tile_viz_seaborn_stats_themes.s07':
                pa = practice_anchors.get('viz.seaborn_statistical_functions', {})
                lc = pa.get('live_code', {})
                allowed = ix['public']['constraints']['allowed_syntax']
                if allowed != lc.get('allowed_syntax', []):
                    errors.append(f"{step_id}: allowed_syntax doesn't match viz.seaborn_statistical_functions")
            
            # Check 6: s10 should not use lit_str
            if step_id == 'tile_viz_seaborn_stats_themes.s10':
                solution = ix['grading']['solution_files'][0]['content']
                if "plt.xlabel(" in solution or "plt.ylabel(" in solution or "plt.title(" in solution:
                    errors.append(f"{step_id}: solution still uses xlabel/ylabel/title (lit_str)")
                # Check expected values
                for t in ix['grading']['tests']:
                    if t['test_id'] == 'ix.tile_viz_seaborn_stats_themes.s10.t02':
                        expected = t['spec']['expected']
                        # Should be means of [23,25,22], [45,47,44], [56,58,55]
                        correct = [23.333333333333332, 45.333333333333336, 56.333333333333336]
                        if expected != correct:
                            errors.append(f"{step_id}: t02 expected is {expected}, should be {correct}")

if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print("All checks passed!")
    sys.exit(0)
