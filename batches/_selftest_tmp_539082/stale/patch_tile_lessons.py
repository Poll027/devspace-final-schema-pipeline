"""
Update tile_lessons/tile_pandas_creating_inspecting.json with the patched
interactions and screens content.

This patches:
1. s04 interaction (tests + starter + solution)
2. s05 blocks (add diagram)
3. s10 interaction (tests)
"""
import json, copy

# Load the tile lesson
with open('batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_creating_inspecting.json') as f:
    lesson = json.load(f)

# Load the patched interactions
with open('batches/final_batch_009_da_pandas/interactions.part.c1.json') as f:
    ix_part = json.load(f)

# Load the patched screens
with open('batches/final_batch_009_da_pandas/screens.part.c1.json') as f:
    sc_part = json.load(f)

# Build lookups
ix_tile = next(t for t in ix_part['tiles'] if t['tile_id'] == 'tile_pandas_creating_inspecting')
ix_map = {i['step_id']: i['interaction'] for i in ix_tile['interactions']}

sc_tile = next(t for t in sc_part['tiles'] if t['tile_id'] == 'tile_pandas_creating_inspecting')
sc_steps = {s['step_id']: s for s in sc_tile.get('steps', [])}

# Patch steps
for step in lesson['steps']:
    sid = step['step_id']

    # Update interaction for s04 and s10
    if sid in ix_map and step.get('type') in ('check', 'hands_on'):
        new_ix = copy.deepcopy(ix_map[sid])
        # Preserve execution_provenance if present (computed by assemble)
        old_ix = step.get('interaction', {})
        if 'execution_provenance' in old_ix:
            new_ix['execution_provenance'] = old_ix['execution_provenance']
        step['interaction'] = new_ix

    # Update blocks for s05
    if sid == 'tile_pandas_creating_inspecting.s05' and sid in sc_steps:
        step['blocks'] = copy.deepcopy(sc_steps[sid]['blocks'])

# Save
with open('batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_creating_inspecting.json', 'w') as f:
    json.dump(lesson, f, indent=2)
print("tile_lessons/tile_pandas_creating_inspecting.json patched")

# Also update tile_lessons_public if it exists
import os
pub_path = 'batches/final_batch_009_da_pandas/tile_lessons_public/tile_pandas_creating_inspecting.json'
if os.path.exists(pub_path):
    with open(pub_path) as f:
        pub = json.load(f)
    for step in pub['steps']:
        sid = step['step_id']
        if sid in ix_map and step.get('type') in ('check', 'hands_on'):
            new_ix = copy.deepcopy(ix_map[sid])
            # Remove grading from public version
            new_ix.pop('grading', None)
            old_ix = step.get('interaction', {})
            if 'execution_provenance' in old_ix:
                new_ix['execution_provenance'] = old_ix['execution_provenance']
            step['interaction'] = new_ix
        if sid == 'tile_pandas_creating_inspecting.s05' and sid in sc_steps:
            step['blocks'] = copy.deepcopy(sc_steps[sid]['blocks'])
    with open(pub_path, 'w') as f:
        json.dump(pub, f, indent=2)
    print("tile_lessons_public/tile_pandas_creating_inspecting.json patched")
