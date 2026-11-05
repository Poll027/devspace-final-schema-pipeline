"""
Repair round patch:
1. Fix s05 constraints.allowed_syntax to verbatim copy from viz.matplotlib_figure_axes practice anchor
2. Fix s05 t02 expected: [1,2,3] -> [1,2,3,4,5]  (solution reads 5-row CSV)
3. Fix s05 t03 expected: [21,23,19] -> [21,23,19,25,20]
4. Fix s08 constraints.allowed_syntax to verbatim copy from viz.figure_size_layout practice anchor
5. Fix s12 constraints.allowed_syntax to verbatim copy from viz.pyplot_basic_plotting practice anchor
6. Fix s12 t02 expected: [0,1,2] -> [0,1,2,3,4]
7. Fix s12 t03 expected: [1,2,3] -> [1,2,3,4,5]
8. Fix s12 t04 expected: [21,23,19] -> [21,23,19,25,20]
9. Fix s12 t05 expected: [21,23,19] -> [21,23,19,25,20]
10. Fix s13 lineage.teaching_block_ids in screens.json to match plan: ['viz.matplotlib_figure_axes#tb5', 'viz.pyplot_basic_plotting#tb4']
"""
import json, copy

# ── 1. Fix interactions.part.c0_canary.json ──────────────────────────────────
INTERACTIONS_PATH = 'batches/final_batch_012_da_viz/interactions.part.c0_canary.json'

with open(INTERACTIONS_PATH) as f:
    data = json.load(f)

# Verbatim allowed_syntax from glossary practice anchors
ALLOWED_SYNTAX_FIGURE_AXES = [
    "import matplotlib.pyplot as plt",
    "fig, ax = plt.subplots()",
    "ax.plot(x, y)"
]

ALLOWED_SYNTAX_FIGURE_SIZE = [
    "plt.subplots(figsize=(width, height))",
    "fig.tight_layout()",
    "plt.tight_layout()",
    "tuple literals for figsize",
    "variable assignment (fig, ax = ...)"
]

ALLOWED_SYNTAX_PYPLOT_BASIC = [
    "import matplotlib.pyplot as plt",
    "plt.plot(y_list)",
    "plt.plot(x_list, y_list)"
]

for tile in data['tiles']:
    for ix in tile['interactions']:
        step_id = ix['step_id']
        interaction = ix['interaction']

        if step_id == 'tile_viz_figures_layout_plotting.s05':
            # Fix allowed_syntax
            interaction['public']['constraints']['allowed_syntax'] = ALLOWED_SYNTAX_FIGURE_AXES
            # Fix t02 expected: [1,2,3] -> [1,2,3,4,5]
            # Fix t03 expected: [21,23,19] -> [21,23,19,25,20]
            for test in interaction['grading']['tests']:
                if test['test_id'] == 'ix.tile_viz_figures_layout_plotting.s05.t02':
                    test['spec']['expected'] = [1, 2, 3, 4, 5]
                    test['message_on_fail'] = "The x-values of the line should be the `day` column (1, 2, 3, 4, 5). Pass `days` as the first argument to `ax.plot()`."
                elif test['test_id'] == 'ix.tile_viz_figures_layout_plotting.s05.t03':
                    test['spec']['expected'] = [21, 23, 19, 25, 20]
                    test['message_on_fail'] = "The y-values of the line should be the `lagos_avg` column (21, 23, 19, 25, 20). Pass `delivery_times` as the second argument to `ax.plot()`."

        elif step_id == 'tile_viz_figures_layout_plotting.s08':
            # Fix allowed_syntax
            interaction['public']['constraints']['allowed_syntax'] = ALLOWED_SYNTAX_FIGURE_SIZE

        elif step_id == 'tile_viz_figures_layout_plotting.s12':
            # Fix allowed_syntax
            interaction['public']['constraints']['allowed_syntax'] = ALLOWED_SYNTAX_PYPLOT_BASIC
            # Fix t02: [0,1,2] -> [0,1,2,3,4]
            # Fix t03: [1,2,3] -> [1,2,3,4,5]
            # Fix t04: [21,23,19] -> [21,23,19,25,20]
            # Fix t05: [21,23,19] -> [21,23,19,25,20]
            for test in interaction['grading']['tests']:
                if test['test_id'] == 'ix.tile_viz_figures_layout_plotting.s12.t02':
                    test['spec']['expected'] = [0, 1, 2, 3, 4]
                    test['message_on_fail'] = "The first line should have auto-generated x-positions 0, 1, 2, 3, 4. Use `plt.plot(delivery_times)` with only one argument."
                elif test['test_id'] == 'ix.tile_viz_figures_layout_plotting.s12.t03':
                    test['spec']['expected'] = [1, 2, 3, 4, 5]
                    test['message_on_fail'] = "The second line should have x-values from `days` (1, 2, 3, 4, 5). Use `plt.plot(days, delivery_times)` with two arguments."
                elif test['test_id'] == 'ix.tile_viz_figures_layout_plotting.s12.t04':
                    test['spec']['expected'] = [21, 23, 19, 25, 20]
                    test['message_on_fail'] = "The y-values of the first line should be the `lagos_avg` column (21, 23, 19, 25, 20)."
                elif test['test_id'] == 'ix.tile_viz_figures_layout_plotting.s12.t05':
                    test['spec']['expected'] = [21, 23, 19, 25, 20]
                    test['message_on_fail'] = "The y-values of the second line should be the `lagos_avg` column (21, 23, 19, 25, 20)."

with open(INTERACTIONS_PATH, 'w') as f:
    json.dump(data, f, indent=2)
print("interactions.part.c0_canary.json patched")

# ── 2. Fix screens.json: s13 lineage.teaching_block_ids ──────────────────────
SCREENS_PATH = 'batches/final_batch_012_da_viz/screens.json'
PLANNED_TB_IDS = ['viz.matplotlib_figure_axes#tb5', 'viz.pyplot_basic_plotting#tb4']

with open(SCREENS_PATH) as f:
    screens = json.load(f)

for tile in screens.get('tiles', []):
    if tile.get('tile_id') == 'tile_viz_figures_layout_plotting':
        for step in tile.get('steps', []):
            if step.get('step_id') == 'tile_viz_figures_layout_plotting.s13':
                step['lineage']['teaching_block_ids'] = PLANNED_TB_IDS
                print(f"Fixed s13 lineage.teaching_block_ids -> {PLANNED_TB_IDS}")

with open(SCREENS_PATH, 'w') as f:
    json.dump(screens, f, indent=2)
print("screens.json patched")
