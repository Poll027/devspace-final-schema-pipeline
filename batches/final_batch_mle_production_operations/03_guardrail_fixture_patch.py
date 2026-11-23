import copy
import json
from pathlib import Path

batch = Path(__file__).resolve().parent
path = batch / 'screens.json'
original = json.loads(path.read_text())
patched = copy.deepcopy(original)
registry = json.loads((batch / 'scenario_asset_registry.json').read_text())
asset = next(a for a in registry['assets'] if a['asset_id'] == 'ds.budget_replay')
step_id = 'mle.tile.091_094.s10'
step = next(s for t in patched['tiles'] for s in t['steps'] if s['step_id'] == step_id)
visual = next(b for b in step['blocks'] if b['type'] == 'before_after')
visual['after'] = {
    'type': 'data_table',
    'asset_ref': {
        'asset_id': asset['asset_id'],
        'columns': [column['name'] for column in asset['columns']],
    },
    'caption': 'Registered replay fixtures: expected notification, response and target state, not captured execution evidence.',
    'lineage': copy.deepcopy(visual['lineage']),
}
visual['change_summary'] = 'Compare safely reloaded configuration with the registered replay expectations. Expected notifications, responses and target states are not receipt, execution or before/after inspection records.'
for old_tile, new_tile in zip(original['tiles'], patched['tiles']):
    for old_step, new_step in zip(old_tile['steps'], new_tile['steps']):
        if old_step['step_id'] != step_id:
            assert old_step == new_step
assert len(step['blocks']) == len(next(s for t in original['tiles'] for s in t['steps'] if s['step_id'] == step_id)['blocks'])
assert 'rows' not in visual['after'] and 'result' not in visual['after']
assert set(visual['after']['asset_ref']['columns']) == {c['name'] for c in asset['columns']}
path.write_text(json.dumps(patched, indent=2) + '\n')
print(json.dumps({'tiles': len(patched['tiles']), 'steps': sum(len(t['steps']) for t in patched['tiles']), 'remediation_steps': sum(len(t.get('remediation_steps', [])) for t in patched['tiles']), 'changed_steps': [step_id]}, indent=2))
