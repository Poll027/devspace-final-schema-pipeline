import json
from pathlib import Path

batch = Path(__file__).parent
path = batch / 'screens.json'
original = path.read_text()
screens = json.loads(original)
registry = json.loads((batch / 'scenario_asset_registry.json').read_text())
asset = next(a for a in registry['assets'] if a['asset_id'] == 'ds.release_evidence')
columns = [c['name'] for c in asset['columns']]
approved = {row[columns.index('approved_config')] for row in asset['rows'] if row[columns.index('release_id')] == 'r2'}
assert len(approved) == 1
old = 'approved rollback cfg.bad -> cfg.r1 under lab.operator; readiness and bounded prediction gates required'
new = old.replace('cfg.r1', next(iter(approved)))
# Only stage-03-owned content in the named step is eligible for repair.
changes = 0
for tile in screens['tiles']:
    for step in tile['steps']:
        if step['step_id'] == 'mle.tile.083_085.s16':
            def patch(value):
                global changes
                if isinstance(value, dict):
                    return {k: patch(v) for k, v in value.items()}
                if isinstance(value, list):
                    return [patch(v) for v in value]
                if isinstance(value, str) and old in value:
                    changes += value.count(old)
                    return value.replace(old, new)
                return value
            replacement = patch(step)
            step.clear()
            step.update(replacement)
# Preserve the artifact byte-for-byte when the reported value is not stage-owned.
if changes:
    path.write_text(json.dumps(screens, indent=2) + '\n')
assert old not in json.dumps(next(s for t in screens['tiles'] for s in t['steps'] if s['step_id'] == 'mle.tile.083_085.s16'))
print(json.dumps({'changed_policy_values': changes, 'tiles': len(screens['tiles']), 'steps': sum(len(t['steps']) for t in screens['tiles']), 'remediation_steps': sum(len(t.get('remediation_steps', [])) for t in screens['tiles']), 'scope_note': 'Named policy absent from screens; registered workspace and embedded interaction are outside stage 03 ownership.'}, indent=2))
