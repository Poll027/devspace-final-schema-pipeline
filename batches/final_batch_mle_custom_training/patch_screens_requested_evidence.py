import json
from pathlib import Path

batch = Path(__file__).parent
path = batch / 'screens.json'
data = json.loads(path.read_text())
targets = {
    'mle.tile.044_045.s07': ('Failing training record — pinned evidence unavailable', 'Corrected training record — pinned evidence unavailable'),
    'mle.tile.046_048.s12': ('Failed memory run — pinned evidence unavailable', 'Corrected memory run — pinned evidence unavailable'),
    'mle.tile.049_050.s01': ('Baseline profile — pinned evidence unavailable', 'One-factor rerun — pinned evidence unavailable'),
    'mle.tile.051_051.s01': ('Frozen reference — pinned evidence unavailable', 'Adapted model — pinned evidence unavailable'),
}
changed = []
for tile in data['tiles']:
    for step in tile['steps']:
        if step['step_id'] not in targets:
            continue
        visual = next(block for block in step['blocks'] if block['type'] == 'side_by_side')
        for side, title in zip(('left', 'right'), targets[step['step_id']]):
            panel = visual[side]
            panel['title'] = title
            if step['step_id'] == 'mle.tile.044_045.s07':
                replacements = {
                    'Expected selected gradient: negative': 'Compare the selected derivative with its declared reference',
                    'Measured failing gradient: zero': 'Inspect the measured failing parameter gradient',
                    'Failing loss: supplied record; selected gradient fails derivative-reference sign': 'Compare failing loss, gradient sign and magnitude with the declared computation',
                    'Preserve fixture, target representation, learning rate and derivative reference': 'Preserve the fixture and derivative reference; identify the single changed factor',
                    'Supported hypothesis to test: a missing gradient path to the selected parameter': 'Check the declared learning rate against the reproduced computation',
                    'Single correction: restore that path; rerun the identical bounded fixture': 'Test one evidence-supported correction on the identical bounded fixture',
                    'Gradient sign predicate: corrected_gradient < 0': 'Compare the corrected gradient sign with the declared derivative reference',
                }
                for node in panel['nodes']:
                    node['label'] = replacements.get(node['label'], node['label'])
            panel['alt_text'] = panel['title'] + ': ' + '; '.join(node['label'] for node in panel['nodes'])
        changed.append(step['step_id'])
path.write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({'changed_steps': changed, 'steps': sum(len(t['steps']) for t in data['tiles']), 'remediation_steps': sum(len(t.get('remediation_steps', [])) for t in data['tiles'])}, indent=2))
