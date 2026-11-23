import copy
import json
from pathlib import Path
p = Path('batches/final_batch_mle.region.production_operations/screens.json')
data = json.loads(p.read_text())
before = copy.deepcopy(data)
replacements = {
    'mle.tile.086_089.s16': 'Implement atomic admission, accepted/duplicate/busy handling, same-job recovery and terminal-only release; complete concurrency/restart assertions and fatal pipeline dependencies.',
    'mle.tile.086_089.s21': 'Implement conditional rates, expected costs, undefined-group rejection, incumbent-relative and required-gate checks, exact artifact binding, and valid/boundary/failure assertions.',
    'mle.tile.091_094.s14': 'Construct the budget mapping, existing event binding and fixed-target safe-stop response from policy; safely reload, inspect and replay it.',
}
changed = []
for tile in data['tiles']:
    for step in tile['steps']:
        if step['step_id'] in replacements:
            assert step['type'] == 'hands_on'
            if step['lede'] != replacements[step['step_id']]:
                step['lede'] = replacements[step['step_id']]
                changed.append(step['step_id'])
assert len(changed) == len(replacements)
# Verify no change outside the three framing fields.
restored = copy.deepcopy(data)
for old_tile, tile in zip(before['tiles'], restored['tiles']):
    for old, step in zip(old_tile['steps'], tile['steps']):
        if step['step_id'] in replacements:
            step['lede'] = old['lede']
assert restored == before
p.write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({'changed_ledes': changed, 'tiles': len(data['tiles']), 'steps': sum(len(t['steps']) for t in data['tiles']), 'remediation_steps': sum(len(t.get('remediation_steps', [])) for t in data['tiles'])}, indent=2))
