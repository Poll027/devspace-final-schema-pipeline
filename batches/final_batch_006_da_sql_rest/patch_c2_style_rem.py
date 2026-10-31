"""
Additional patch for interactions.part.c2.json: fix style_conventions remediation_step_ids.
"""
import json

with open('batches/final_batch_006_da_sql_rest/interactions.part.c2.json') as f:
    data = json.load(f)

style_step_rem = {
    'tile_sql_style_conventions.s02': 'tile_sql_style_conventions.r01',
    'tile_sql_style_conventions.s03': 'tile_sql_style_conventions.r01',
}

for tile in data['tiles']:
    for step in tile.get('interactions', []):
        ix = step.get('interaction', {})
        sid = step['step_id']
        fb = ix.get('feedback', {})
        if fb and 'remediation_step_id' in fb and sid in style_step_rem:
            old = fb['remediation_step_id']
            new = style_step_rem[sid]
            if old != new:
                print(f'  Fixed {sid}: {old} -> {new}')
                fb['remediation_step_id'] = new

with open('batches/final_batch_006_da_sql_rest/interactions.part.c2.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("interactions.part.c2.json style_conventions remediation patched")
