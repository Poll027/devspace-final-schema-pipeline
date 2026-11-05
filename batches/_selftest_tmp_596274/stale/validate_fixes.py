"""
Simple assembly and validation check for the patched files.
"""
import json

print("Assembling interactions.json...")
# Load all part files
parts = []
for part_name in ['c0_canary', 'c1', 'c2']:
    try:
        with open(f'batches/final_batch_012_da_viz/interactions.part.{part_name}.json', 'r') as f:
            part = json.load(f)
            parts.append(part)
    except FileNotFoundError:
        pass

# Merge tiles
all_tiles = []
for part in parts:
    all_tiles.extend(part['tiles'])

# Create assembled file
assembled = {
    'schema_version': parts[0]['schema_version'],
    'kind': 'interactions',
    'path_id': parts[0]['path_id'],
    'batch_id': parts[0]['batch_id'],
    'tiles': all_tiles
}

with open('batches/final_batch_012_da_viz/interactions.json', 'w') as f:
    json.dump(assembled, f, indent=2, ensure_ascii=False)
    f.write('\n')

print(f"  Assembled {len(all_tiles)} tiles")

print("\nAssembling screens.json...")
# Do the same for screens
parts = []
for part_name in ['c0_canary', 'c1', 'c2']:
    try:
        with open(f'batches/final_batch_012_da_viz/screens.part.{part_name}.json', 'r') as f:
            part = json.load(f)
            parts.append(part)
    except FileNotFoundError:
        pass

all_tiles = []
for part in parts:
    all_tiles.extend(part['tiles'])

assembled = {
    'schema_version': parts[0]['schema_version'],
    'kind': 'screens',
    'path_id': parts[0]['path_id'],
    'batch_id': parts[0]['batch_id'],
    'tiles': all_tiles
}

with open('batches/final_batch_012_da_viz/screens.json', 'w') as f:
    json.dump(assembled, f, indent=2, ensure_ascii=False)
    f.write('\n')

print(f"  Assembled {len(all_tiles)} tiles")

print("\nValidation checks:")

# Load assembled files
with open('batches/final_batch_012_da_viz/screens.json', 'r') as f:
    screens = json.load(f)

with open('batches/final_batch_012_da_viz/interactions.json', 'r') as f:
    interactions = json.load(f)

# Check 1: Does s01 have a chart block?
print("\n1. tile_viz_seaborn_stats_themes.s01 chart block:")
found_error = False
for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_viz_seaborn_stats_themes':
        for step in tile['steps']:
            if step['step_id'] == 'tile_viz_seaborn_stats_themes.s01':
                block_types = [block['type'] for block in step['blocks']]
                has_chart = 'chart' in block_types
                if not has_chart:
                    print(f"   ERROR: Missing chart block! blocks={block_types}")
                    found_error = True
                else:
                    print(f"   OK: Has chart block")

if not found_error:
    print("   All occurrences have chart blocks")

# Check 2: Are remediation steps referenced?
print("\n2. Remediation steps referenced:")
# Find which remediation steps exist in c2
remediation_steps_c2 = set()
for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        if 'remediation_steps' in tile:
            for step in tile['remediation_steps']:
                step_id = step['step_id']
                if step_id in ['tile_viz_labeling_chart_selection.r01', 'tile_viz_labeling_chart_selection.r02']:
                    remediation_steps_c2.add(step_id)

# Check which ones are referenced in interactions
referenced = set()
for tile in interactions['tiles']:
    if tile['tile_id'] == 'tile_viz_labeling_chart_selection':
        for interaction in tile['interactions']:
            remediation_id = interaction['interaction'].get('feedback', {}).get('remediation_step_id')
            if remediation_id:
                referenced.add(remediation_id)

for step_id in sorted(remediation_steps_c2):
    if step_id in referenced:
        print(f"   OK: {step_id} is referenced")
    else:
        print(f"   WARNING: {step_id} is never referenced")

print("\nValidation complete.")
