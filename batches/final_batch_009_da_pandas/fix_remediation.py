import json

# Load the interactions file
with open('interactions.part.c3.json', 'r') as f:
    data = json.load(f)

# Fix remediation_step_id for ix.tile_pandas_pivot_export.s05
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_pandas_pivot_export':
        for interaction_obj in tile['interactions']:
            if interaction_obj['interaction']['interaction_id'] == 'ix.tile_pandas_pivot_export.s05':
                interaction = interaction_obj['interaction']
                # Remove remediation_step_id since there's no appropriate remediation
                if 'remediation_step_id' in interaction.get('feedback', {}):
                    del interaction['feedback']['remediation_step_id']
                    print("Removed remediation_step_id from ix.tile_pandas_pivot_export.s05")

# Write back
with open('interactions.part.c3.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed remediation issue")
