import ast
import json
from pathlib import Path

path = Path('batches/final_batch_mle.region.custom_training/scenario_asset_registry.json')
registry = json.loads(path.read_text())
assets = {a['asset_id']: a for a in registry['assets']}
def file(asset, name):
    return next(f for f in assets[asset]['files'] if f['path'] == name)

f = file('ws.training_failure_diagnosis', 'fixtures.py')
old = "    before = model.weight.detach().clone()\n    outputs = model(state['features'])"
new = "    before = model.weight.detach().clone()\n    state['optimizer'].zero_grad()\n    outputs = model(state['features'])"
assert f['content'].count(old) == 1
f['content'] = f['content'].replace(old, new, 1)

def remove_functions(content, names):
    lines = content.splitlines(keepends=True)
    nodes = [n for n in ast.parse(content).body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    for n in sorted(nodes, key=lambda n: n.lineno, reverse=True):
        del lines[n.lineno - 1:n.end_lineno]
    return ''.join(lines).rstrip() + '\n'

f = file('ws.dataset_minibatch_loader', 'infrastructure.py')
f['content'] = remove_functions(f['content'], ['training_fixture'])
f['content'] = f['content'].replace('from torch import nn\n', '').replace('from torch.utils.data import DataLoader, TensorDataset\n', '')
# These imports/constants have no remaining dataset-fixture consumers.
f['content'] = f['content'].replace('import torch\n', '').replace('ATOL = 1e-6\n', '').replace('RTOL = 1e-5\n', '')
f = file('ws.dataset_minibatch_loader', 'acceptance.py')
f['content'] = remove_functions(f['content'], ['check_fresh_gradient', 'check_plain_sgd', 'check_state_mapping', 'check_dropout_output'])

# No authorized host provider or executable runtime exists in this environment.
# Leave all six blocked bindings and their README notices truthful and unchanged.
for a in assets.values():
    for f in a.get('files', []):
        if f['path'].endswith('.py'):
            ast.parse(f['content'])
path.write_text(json.dumps(registry, indent=2) + '\n')
print('Patched 2 workspaces, 3 embedded files; 6 host bindings remain unresolved.')
