import ast
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parents[1]
bundle = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
concepts = bundle['bundles']
scenario_id = 'scenario.order_helper'

def example(x):
    return '\n'.join(t['content'] for t in x['teaching_blocks'] if t['purpose'] == 'example')

def code(x):
    found = re.search(r'```python\n(.*?)```', example(x), re.S)
    return found.group(1).rstrip() if found else ''

def initial_assignment(x):
    return code(x).splitlines()[0]

# Vocabulary is mined from the glossary, not an independent example domain.
vocab = set()
for x in concepts:
    text = '\n'.join(t['content'] for t in x['teaching_blocks'])
    text += '\n' + json.dumps(x['practice_anchor'], ensure_ascii=False)
    text += '\n' + json.dumps(x['visual_anchor'], ensure_ascii=False)
    for q in re.findall(r'"([^"\n]+)"', '\n'.join(t['content'] for t in x['teaching_blocks']) + '\n' + x['practice_anchor']['objective'] + '\n' + x['practice_anchor']['success'] + '\n' + x['visual_anchor']['purpose']):
        vocab.add(q)
    for name in re.findall(r'\b[A-Z][a-z]+\b', x['practice_anchor']['objective'] + '\n' + x['practice_anchor']['success']):
        vocab.add(name)
    for n in re.findall(r'(?<![\w.])-?\d+(?:\.\d+)?(?:e-?\d+)?(?![\w.])', text):
        vocab.add(n)
    source = code(x)
    if source:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                vocab.add(node.id)
            elif isinstance(node, ast.Attribute):
                vocab.add(node.attr)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value:
                    vocab.add(node.value)
# Plain-text example code still contributes its names and filename.
for x in concepts:
    for token in re.findall(r'\b[A-Za-z_]+(?:\.py)?\b', example(x)):
        if token.endswith('.py') or token in {'quantity', 'cost', 'selected_python', 'sys', 'exit', 'SyntaxError', 'ValueError', 'UnicodeDecodeError', 'CPython', 'UTF', 'Ada'}:
            vocab.add(token)

assets = []
for x in concepts:
    cid = x['context']['concept_id']
    short = cid.removeprefix('python.')
    p = x['practice_anchor']
    intent = p['live_code']['starter_state_intent']
    source = code(x)
    path = 'main.py'
    extra_files = []
    if short == 'collection_selection':
        mapping_text = re.search(r'\{"notebook":.*?\}', example(x)).group()
        initial = list(ast.literal_eval(mapping_text).values())
        source = 'quantities = ' + repr(initial) + '\n'
    elif short == 'console_input_output':
        source = ''
    elif short in {'enumerate_iteration', 'nested_loops', 'truth_value_testing', 'none_and_identity', 'unicode_and_bytes'}:
        source = initial_assignment(x) + '\n'
    elif short == 'floating_point_limits':
        source = '\n'.join(source.splitlines()[:2]) + '\n'
    elif short == 'indentation_and_blocks':
        source = '\n'.join(line.lstrip() for line in source.splitlines()) + '\n'
    elif short == 'math_utilities':
        source = source.splitlines()[0] + '\nside_length = math.sqrt()\n'
    elif short == 'nested_collections':
        source = re.search(r'Provide (order = .*?) so the learner', intent).group(1) + '\n'
    elif short == 'range_iteration':
        source = '\n'.join(source.splitlines()[:2])
        source = re.sub(r'range\([^)]*\)', 'range()', source) + '\n'
    elif short == 'running_scripts':
        path = re.search(r'\b\w+\.py\b', intent).group()
        source = p['live_code']['allowed_syntax'][0] + '\n'
    elif short == 'statements_and_expressions':
        source += '\n'
    elif short == 'comments':
        quantity_assignment = re.search(r'assign (quantity = \d+)', intent).group(1)
        cost_assignment = re.search(r'and (cost = \d+)', intent).group(1)
        condition = re.search(r'use (if quantity >= \d+:)', intent).group(1)
        update = re.search(r'assign (cost = quantity \* \d+ \+ \d+)', intent).group(1)
        source = '\n'.join([quantity_assignment, cost_assignment, condition, '    ' + update]) + '\n'
    elif short == 'interactive_execution':
        commands = re.search(r'supply (quantity = \d+) and (quantity \* \([^)]*\)) as commands', intent).groups()
        extra_files.append({'path': 'commands.txt', 'content': '\n'.join(commands) + '\n'})
        source = ''
    elif short == 'interpreter_execution_model':
        statements = re.search(r'statements, (quantity = \d+) and (cost = quantity \* \d+),', intent).groups()
        source = '\n'.join(statements) + '\n'
    elif short == 'multiline_expressions':
        calculation, call = re.search(r'Provide (cost = \([^)]*\)) followed by (print\([^)]*\))\.', intent).groups()
        source = calculation + '\n' + call + '\n'
    elif short == 'string_methods':
        source = initial_assignment(x) + '\n'
        # Mount the additional literal inputs, not their already-solved outputs.
        expressions = ast.parse(code(x))
        strings = []
        for stmt in expressions.body:
            if isinstance(stmt, ast.Expr):
                for node in ast.walk(stmt):
                    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Constant) and node.attr == 'split':
                        strings.append(node.value.value)
        source += 'comma_text = ' + repr(strings[0]) + '\nwhitespace_text = ' + repr(strings[1]) + '\n'
    elif short == 'syntax_vs_runtime_errors':
        quantity = re.search(r'Provide (quantity = \d+)', intent).group(1)
        condition = re.search(r'followed by (if quantity > \d+) without', intent).group(1)
        conversion = re.search(r'statement (quantity = int\("[^"]+"\))', intent).group(1)
        source = quantity + '\n' + condition + '\n    ' + conversion + '\n'
    else:
        raise ValueError(cid)
    readme = '\n\n'.join([x['context']['concept_name'], p['objective'], 'Starter state: ' + intent, 'Success: ' + p['success']]) + '\n'
    files = [{'path': path, 'content': source}, {'path': 'README.txt', 'content': readme}] + extra_files
    assets.append({'asset_id': 'workspace.' + short, 'asset_kind': 'code_workspace', 'scenario_id': scenario_id, 'title': x['context']['concept_name'] + ' — starter workspace', 'runtime': 'python', 'files': files})

registry = {
    'schema_version': '1.0.0',
    'kind': 'scenario_asset_registry',
    'path_id': bundle['path_id'],
    'batch_id': B.name,
    'scenarios': [{
        'scenario_id': scenario_id,
        'name': 'The fictional order helper',
        'summary': 'A small fictional stationery order helper works with notebook, pen and pencil labels and editable quantities. Its console examples, cost calculations and text handling use the glossary\'s authored values; the isolated math and interpreter examples belong to the same learner workspace.',
        'domain': 'Fictional stationery order helper and Python learning workspace',
        'glossary_example_vocab': sorted(vocab)
    }],
    'assets': assets
}
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n')

# Stage-specific mistakes-to-avoid audit. There are no table/plot/cleanup anchors
# in this batch, so dataset width, role/type, duplicate occurrence and planted
# predicate tests are inapplicable, not silently omitted.
assert len(assets) == len(concepts)
assert len({a['asset_id'] for a in assets}) == len(assets)
assert all(x['practice_anchor']['type'] == 'live_code' for x in concepts)
assert all(x['visual_anchor']['type'] not in {'data_table', 'spreadsheet', 'chart'} for x in concepts)
assert all(a['scenario_id'] == scenario_id for a in assets)
for x, a in zip(concepts, assets):
    assert x['practice_anchor']['objective'] in a['files'][1]['content']
    assert x['practice_anchor']['success'] in a['files'][1]['content']
    assert len({f['path'] for f in a['files']}) == len(a['files'])
    if x['context']['concept_id'] not in {'python.indentation_and_blocks', 'python.syntax_vs_runtime_errors'}:
        ast.parse(a['files'][0]['content'])
assert {'notebook', 'pen', 'pencil', 'Ada', 'café', 'Ready'} <= vocab
print(json.dumps({'concepts': len(concepts), 'scenarios': 1, 'assets': len(assets), 'code_workspaces': len(assets), 'datasets': 0, 'variants': 0, 'images': 0, 'vocabulary_entries': len(vocab), 'mistakes_to_avoid': 'PASS (table/variant checks not applicable)', 'asset_ids': [a['asset_id'] for a in assets]}, indent=2))
