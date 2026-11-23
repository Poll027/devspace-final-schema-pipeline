import ast
import json
from pathlib import Path

batch = Path(__file__).parent
path = batch / 'interactions.json'
data = json.loads(path.read_text())
targets = {f'mle.tile.012_015.{step}' for step in ('s05', 's11', 's16')}
changed = []
for tile in data['tiles']:
    for entry in tile['interactions']:
        if entry['step_id'] not in targets:
            continue
        ix = entry['interaction']
        # Load the real estimators' scipy dependency explicitly in unchanged
        # infrastructure scaffolding, before their transitive import.
        for file in ix['public']['workspace']['files'] + ix['grading']['solution_files']:
            assert '    from sklearn.' in file['content']
            file['content'] = file['content'].replace(
                '    from sklearn.',
                '    import scipy  # Supplied estimator dependency preload.\n    from sklearn.')
        imports = []
        for node in ast.walk(ast.parse(ix['grading']['solution_files'][0]['content'])):
            if isinstance(node, ast.Import):
                imports.extend(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module.split('.')[0])
        ix['public']['runtime']['packages'] = list(dict.fromkeys(
            'scikit-learn' if name == 'sklearn' else name for name in imports))
        changed.append(entry['step_id'])
path.write_text(json.dumps(data, indent=2) + '\n')
print('Patched:', changed)
print('Tiles:', len(data['tiles']))
print('Interactions:', sum(len(t['interactions']) for t in data['tiles']))
