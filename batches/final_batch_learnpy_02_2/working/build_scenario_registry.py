import ast
import io
import json
import re
import tokenize
from pathlib import Path

B = Path('batches/final_batch_learn_python.region.02_2')
glossary = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/learn_python.json').read_text())
scenario_id = 'scenario.learn_python.collection_helpers'
vocab = []

def remember(value):
    if value and value not in vocab:
        vocab.append(value)

assets = []
for bundle in glossary['bundles']:
    cid = bundle['context']['concept_id']
    text = '\n'.join(block['content'] for block in bundle['teaching_blocks'])
    anchor_text = json.dumps({key: bundle.get(key) for key in ('visual_anchor', 'practice_anchor')}, ensure_ascii=False)
    examples = re.findall(r'```python\n(.*?)```', text, re.S)
    trees = [ast.parse(code) for code in examples]
    for code in examples:
        for token in tokenize.generate_tokens(io.StringIO(code).readline):
            if token.type in (tokenize.NAME, tokenize.STRING, tokenize.NUMBER):
                remember(token.string)
        for node in ast.walk(ast.parse(code)):
            if isinstance(node, (ast.List, ast.Tuple, ast.Call)):
                remember(ast.unparse(node))
    # Anchors sometimes supply additional edge-case lists or API syntax.
    for match in re.findall(r'\[[^\[\]\n]*\]|[A-Za-z_]\w*\.[A-Za-z_]\w*\([^\n]*?\)', anchor_text):
        try:
            parsed = ast.parse(match, mode='eval')
        except SyntaxError:
            continue
        remember(ast.unparse(parsed.body))
    remember(bundle['context']['concept_name'])
    assert cid not in profile.get('practice_type_by_concept', {}), 'Inspect-and-judge must not get a workspace'
    assert bundle['practice_anchor']['type'] == 'live_code'
    tree = trees[0]
    if cid == 'python.zip_iteration':
        assignments = [node for node in tree.body if isinstance(node, ast.Assign)]
        starter = '\n'.join(ast.unparse(node) for node in assignments) + '\n\n# Write the two-variable zip loop here.\n# Identify the omitted label and explain why it has no pair.\n'
    elif cid == 'python.aliasing_mutability_and_copying':
        original = tree.body[0]
        append = next(node for node in tree.body if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == 'append')
        appended = ast.unparse(append.value.args[0])
        starter = 'def append_copy(items):\n    copied = items\n    copied.append(' + appended + ')\n    return copied\n\n' + ast.unparse(original) + '\nchanged = append_copy(original)\n'
    elif cid == 'python.collections_utilities':
        starter = '\n'.join(ast.unparse(node) for node in tree.body[:2]) + '\n\n# Request the most common pair and report it only if one exists.\n'
    elif cid == 'python.diagnostic_printing':
        assignments = [node for node in tree.body if isinstance(node, ast.Assign)]
        starter = 'def convert_quantity(text):\n' + '\n'.join('    ' + ast.unparse(node) for node in assignments) + '\n    return quantity\n\n# Add labeled observations at the relevant execution points.\n# Use repr for the text; then remove the temporary print calls.\n'
    elif cid == 'python.docstrings':
        func = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
        func.body = [node for node in func.body if isinstance(node, ast.Return)]
        starter = ast.unparse(func) + '\n\n# Add accurate first-statement documentation without changing the calculation.\n# Inspect the documentation with help.\n'
    else:
        raise ValueError('Unhandled concept: ' + cid)
    ast.parse(starter)
    assets.append({
        'asset_id': 'code.' + cid,
        'asset_kind': 'code_workspace',
        'scenario_id': scenario_id,
        'title': bundle['context']['concept_name'] + ' — practice workspace',
        'runtime': profile['runtime_by_concept_prefix'][cid.split('.')[0]],
        'files': [{'path': 'main.py', 'content': starter}],
    })

registry = {
    'schema_version': '1.0',
    'kind': 'scenario_asset_registry',
    'path_id': glossary['path_id'],
    'batch_id': B.name,
    'scenarios': [{
        'scenario_id': scenario_id,
        'name': 'Collection helpers for a small stationery order desk',
        'summary': 'A fictional stationery order desk uses small Python helpers to pair notebook, pen and pencil labels with quantities, summarize blue and red labels, copy nested lists before appending, inspect a text-to-quantity conversion, and document an order-cost calculation. The supplied examples are authored practice inputs, not real orders.',
        'domain': 'Stationery orders and Python collection helpers',
        'glossary_example_vocab': vocab,
    }],
    'assets': assets,
}
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')

# Stage-specific mistakes-to-avoid checklist: this batch has native Python
# collections, not table/spreadsheet/chart anchors, pandas, or SQL examples.
assert len(assets) == len(glossary['bundles'])
assert len({a['asset_id'] for a in assets}) == len(assets)
for bundle, asset in zip(glossary['bundles'], assets):
    assert bundle['visual_anchor']['type'] in ('code', 'diagram')
    assert asset['runtime'] == 'python'
    assert all(f['path'] == 'main.py' for f in asset['files'])
    assert bundle['practice_anchor']['type'] != 'field_selection'
    assert bundle['practice_anchor']['type'] != 'data_cleanup'
    for f in asset['files']:
        ast.parse(f['content'])
assert not any(a['asset_kind'] == 'dataset' for a in assets)
print('Checklist PASS: all concepts covered; starter syntax and runtime checked; no table row widths, semantic roles, numeric-label traps, planted issues, duplicate occurrences, CSV requirements, or plot images apply to this scope.')
print('Scenarios:', len(registry['scenarios']), 'Assets:', len(assets), 'Vocabulary entries:', len(vocab))
print('\n'.join(a['asset_id'] for a in assets))
