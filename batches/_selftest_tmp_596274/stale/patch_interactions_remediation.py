"""
Patch interactions.part.c2.json to add remediation_step_id to the first check/hands_on of each concept.
"""
import json

# Load interactions.part.c2.json
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'r') as f:
    data = json.load(f)

# Find tile_viz_labeling_chart_selection and add remediation_step_id
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for interaction in tile['interactions']:
            step_id = interaction['step_id']
            # s03 is the first check for viz.labeling_annotation -> r01
            if step_id == 'tile_viz_labeling_chart_selection.s03':
                if 'feedback' not in interaction['interaction']:
                    interaction['interaction']['feedback'] = {}
                interaction['interaction']['feedback']['remediation_step_id'] = 'tile_viz_labeling_chart_selection.r01'
                print(f"Added remediation_step_id to {step_id}: r01")
            # s08 is the first check for viz.chart_type_selection -> r02
            elif step_id == 'tile_viz_labeling_chart_selection.s08':
                if 'feedback' not in interaction['interaction']:
                    interaction['interaction']['feedback'] = {}
                interaction['interaction']['feedback']['remediation_step_id'] = 'tile_viz_labeling_chart_selection.r02'
                print(f"Added remediation_step_id to {step_id}: r02")

# Save
with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Done.")
