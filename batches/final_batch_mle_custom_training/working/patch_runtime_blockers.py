import json
from pathlib import Path
p = Path('batches/final_batch_mle.region.custom_training/scenario_asset_registry.json')
original = json.loads(p.read_text())
d = json.loads(p.read_text())
ids = {
    'ws.device_placement', 'ws.training_batch_sizing',
    'ws.training_memory_diagnosis', 'ws.training_bottleneck_profiling',
    'ws.training_hardware_selection', 'ws.task_specific_pretrained_weight_fine_tuning',
}
loader = '''def load_runtime():
    path = ROOT / 'authorized_runtime.json'
    if not path.is_file():
        raise RuntimeError('Exercise unavailable: no registered runtime authorization')
    runtime = json.loads(path.read_text())
    if not isinstance(runtime, dict) or runtime.get('status') != 'authorized':
        raise RuntimeError('Exercise unavailable: runtime binding is not authorized')
    # No authorized binding or authorization verifier is supplied in this registry.
    # A status string alone is never proof of permission to access a host resource.
    raise RuntimeError('Exercise unavailable: verified host authorization and required runtime assets are absent')
'''
for a in d['assets']:
    if a['asset_id'] not in ids:
        continue
    for f in a['files']:
        if f['path'] == 'README.md':
            title, body = f['content'].split('\n', 1)
            f['content'] = title + '\n\n> **Unavailable — runtime binding not supplied.** Do not offer or execute this exercise. The following is the intended exercise contract, not evidence that its host resources or policies exist. Actual authorized resources and required runtime assets must be supplied and verified before release.\n' + body
        if f['path'] == 'fixtures.py':
            text = f['content']
            start = text.index('def load_runtime():')
            end = text.find('\ndef ', start + 1)
            if end < 0:
                end = len(text)
            # Preserve any subsequent fixture definitions verbatim.
            text = text[:start] + loader + text[end:]
            # Put the readiness check before any supplied fixture initialization.
            preflight = 'from infrastructure import ROOT\nimport json\n\n' + loader + '\nload_runtime()\n\n'
            f['content'] = preflight + text
    # Explicit absence, not fabricated authorization, telemetry, policies or predictions.
    a['files'].append({'path': 'authorized_runtime.json', 'content': json.dumps({'status': 'unavailable', 'binding': None}, indent=2) + '\n'})
# Verify scope and that no assessed code, table, or other workspace changed.
for old, new in zip(original['assets'], d['assets']):
    if old['asset_id'] not in ids:
        assert old == new
    else:
        for f in old['files']:
            if f['path'] not in {'README.md', 'fixtures.py'}:
                assert f == next(g for g in new['files'] if g['path'] == f['path'])
        for f in new['files']:
            if f['path'].endswith('.py'):
                compile(f['content'], f['path'], 'exec')
assert original['scenarios'] == d['scenarios']
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
print('Patched', len(ids), 'runtime-bound workspaces; assets:', len(d['assets']))
