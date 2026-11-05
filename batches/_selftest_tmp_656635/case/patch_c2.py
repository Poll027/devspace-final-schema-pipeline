import json

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Helper: find interaction by step_id
def find_interaction(tile_id, step_id):
    for tile in data['tiles']:
        if tile['tile_id'] == tile_id:
            for item in tile['interactions']:
                if item['step_id'] == step_id:
                    return item['interaction']
    raise KeyError(f"{tile_id}/{step_id} not found")

# ── BLOCKING: s10 and s11 in tile_capstone_integrate_tools_model ──────────────

s10 = find_interaction('tile_capstone_integrate_tools_model',
                        'tile_capstone_integrate_tools_model.s10')
s11 = find_interaction('tile_capstone_integrate_tools_model',
                        'tile_capstone_integrate_tools_model.s11')

# 1. Add build_pivot_table_with_correct_field_placement to s10 measures
pivot_measure = {
    "concept_id": "capstone.integrate_spreadsheet",
    "capability": "build_pivot_table_with_correct_field_placement",
    "fact_ids": ["f1"]
}
s10['measures'].append(pivot_measure)

# 2. Add the assessment anchor to s10 anchors
s10['anchors'].append(
    "capstone.integrate_spreadsheet#assessment:build_pivot_table_with_correct_field_placement"
)

# 3. s11 measures: keep only apply_countifs_with_multiple_criteria_ranges
s11['measures'] = [
    m for m in s11['measures']
    if m['capability'] == 'apply_countifs_with_multiple_criteria_ranges'
]

# 4. s11 anchors: only practice + assessment:apply_countifs_with_multiple_criteria_ranges
s11['anchors'] = [
    "capstone.integrate_spreadsheet#practice",
    "capstone.integrate_spreadsheet#assessment:apply_countifs_with_multiple_criteria_ranges"
]

# ── ADVISORY: s14 opt_group_only feedback ─────────────────────────────────────
s14 = find_interaction('tile_capstone_integrate_tools_model',
                        'tile_capstone_integrate_tools_model.s14')
s14['grading']['option_feedback']['opt_group_only']['message'] = (
    "pandas groupby().mean() skips NaN values by default, so the result would be "
    "numerically the same. However, calling dropna() first makes the cleaning step "
    "explicit in your code: anyone reading the workflow can see that missing rows were "
    "intentionally removed, making the analysis visible and reproducible rather than "
    "relying on a silent default."
)

# ── ADVISORY: stats_dashboard s09 opt_subplots_1x3 feedback ──────────────────
s09_dash = find_interaction('tile_capstone_stats_dashboard',
                             'tile_capstone_stats_dashboard.s09')
s09_dash['grading']['option_feedback']['opt_subplots_1x3']['message'] = (
    "plt.subplots(1, 3) is also a valid way to create three side-by-side panels "
    "and is taught in this tile. However, this question specifically asks about the "
    "plt.subplot(131/132/133) pattern that is demonstrated in the capstone exercise, "
    "so that pattern is the expected answer here."
)

with open('batches/final_batch_010_da_stats_capstone/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
