import ast
import json
import re
from pathlib import Path

B = Path('batches/final_batch_learn_python.region.02_2')
glossary = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
scenario_id = 'scenario.python_supply_helpers'
assets = []
vocab = set()

for bundle in glossary['bundles']:
    cid = bundle['context']['concept_id']
    short = cid.split('.', 1)[1]
    blocks = bundle['teaching_blocks']
    anchor = bundle['practice_anchor']
    example = next(t['content'] for t in blocks if t['purpose'] == 'example')
    code = re.search(r'```python\n(.*?)```', example, re.S).group(1)
    tree = ast.parse(code)
    # Mine the taught code's identifiers, member names, literals and import tools.
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            vocab.add(node.id)
        elif isinstance(node, ast.Attribute):
            vocab.add(node.attr)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float)):
            if isinstance(node.value, str) and '\n' in node.value:
                continue  # documentation prose is not example vocabulary
            vocab.add(str(node.value))
        elif isinstance(node, ast.ImportFrom):
            vocab.add(node.module)
            vocab.update(n.name for n in node.names)
        elif isinstance(node, ast.FunctionDef):
            vocab.add(node.name)
            vocab.update(a.arg for a in node.args.args)
    # Also retain exact example literals and operation spellings from anchors.
    for text in [anchor['objective'], anchor['success'], anchor['live_code']['starter_state_intent'], bundle['visual_anchor']['purpose']]:
        vocab.update(re.findall(r'"([^"\n]+)"', text))
        vocab.update(re.findall(r'\b\d+\b', text))
    if short == 'zip_iteration':
        assignments = [n for n in tree.body if isinstance(n, ast.Assign)]
        starter = '\n'.join(ast.unparse(n) for n in assignments) + '\n\n# Write the paired traversal and identify the omitted label in a comment.\n'
    elif short == 'aliasing_mutability_and_copying':
        original = ast.unparse(tree.body[0])
        append_call = next(n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'append')
        append_value = ast.unparse(append_call.args[0])
        starter = ('def extend_items(items):\n    copied = items\n    copied.append(' + append_value + ')\n    return copied\n\n' + original + '\nchanged = extend_items(original)\n')
    elif short == 'collections_utilities':
        starter = '\n'.join(ast.unparse(n) for n in tree.body if isinstance(n, (ast.ImportFrom, ast.Assign)) and (isinstance(n, ast.ImportFrom) or any(isinstance(t, ast.Name) and t.id == 'counts' for t in n.targets))) + '\n\n# Create pairs, guard the result, and report the selected label and count.\n'
    elif short == 'diagnostic_printing':
        assignments = [ast.unparse(n) for n in tree.body if isinstance(n, ast.Assign)]
        starter = 'def convert_quantity(text):\n' + '\n'.join('    ' + n for n in assignments) + '\n    return quantity\n'
    elif short == 'docstrings':
        func = next(n for n in tree.body if isinstance(n, ast.FunctionDef))
        if isinstance(func.body[0], ast.Expr) and isinstance(func.body[0].value, ast.Constant) and isinstance(func.body[0].value.value, str):
            func.body.pop(0)
        starter = ast.unparse(func) + '\n\n# Add the docstring without changing the calculation, then inspect with help.\n'
    else:
        raise ValueError(cid)
    ast.parse(starter)
    assets.append({
        'asset_id': 'workspace.' + short,
        'asset_kind': 'code_workspace',
        'scenario_id': scenario_id,
        'title': bundle['context']['concept_name'] + ' practice',
        'runtime': 'python',
        'files': [
            {'path': 'main.py', 'content': starter},
            {'path': 'README.md', 'content': '# ' + bundle['context']['concept_name'] + '\n\n' + anchor['objective'] + '\n\nSuccess: ' + anchor['success'] + '\n\nObservable success: ' + anchor['live_code']['observable_success'] + '\n'}
        ]
    })

registry = {
    'schema_version': '1.0',
    'kind': 'scenario_asset_registry',
    'path_id': glossary['path_id'],
    'batch_id': B.name,
    'scenarios': [{
        'scenario_id': scenario_id,
        'name': 'Supply desk helper workshop',
        'summary': 'A fictional small supply desk is developing Python helpers for stationery labels and quantities, repeated blue and red labels, shared lists, text-to-quantity conversion and order cost documentation. All practice inputs are authored examples, not real records.',
        'domain': 'Python helper development',
        'glossary_example_vocab': sorted(vocab)
    }],
    'assets': assets
}
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')

# Stage 01 mistakes-to-avoid checklist, checked against the whole scope.
assert len(assets) == len(glossary['bundles'])
assert len({a['asset_id'] for a in assets}) == len(assets)
for bundle in glossary['bundles']:
    assert bundle['practice_anchor']['type'] == 'live_code'
    assert bundle['visual_anchor']['type'] in ('code', 'diagram')
    assert not any(re.search(r'\b(?:matplotlib|seaborn|pandas|read_csv)\b', t['content']) for t in bundle['teaching_blocks'])
# No table/spreadsheet anchors, CSV examples, plotted visuals or find_issues
# anchors exist in scope: row widths, column-role ambiguity, variant predicates
# and duplicate occurrence checks are therefore not applicable. Each list
# and helper is kept in its actual Python starter, without fabricating tables.
for a in assets:
    ast.parse(a['files'][0]['content'])
print(json.dumps({'concepts': len(glossary['bundles']), 'scenarios': len(registry['scenarios']), 'assets': len(assets), 'asset_ids': [a['asset_id'] for a in assets], 'checklist': 'PASS: all five anchors covered; glossary-derived example inputs preserved; no table, plot or find_issues anchors; no fabricated datasets or variants'}, indent=2))
