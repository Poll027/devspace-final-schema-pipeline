import ast
import json
import re
from pathlib import Path

B = Path(__file__).resolve().parents[1]
bundle = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
bs = {b['context']['concept_id'].split('.', 1)[1]: b for b in bundle['bundles']}
scenario_id = 'scenario.quantity_project'

def examples(b):
    return [c for t in b['teaching_blocks'] for c in re.findall(r'```python\n(.*?)```', t['content'], re.S)]

def assignment(code, name):
    for node in ast.walk(ast.parse(code)):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(name)

# Mine vocabulary from the scope, including practice syntax and literal records.
vocab = set()
for b in bs.values():
    text = '\n'.join(t['content'] for t in b['teaching_blocks']) + '\n' + json.dumps([b['practice_anchor'], b['visual_anchor']], ensure_ascii=False)
    vocab.update(re.findall(r'\b(?:[A-Z][A-Za-z]*(?:Error|Exception|Interrupt|Exit)|[a-z]+_[a-z_]+)\b', text))
    for code in examples(b):
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Name): vocab.add(node.id)
            if isinstance(node, (ast.FunctionDef, ast.arg)): vocab.add(node.name if isinstance(node, ast.FunctionDef) else node.arg)
            if isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float)): vocab.add(str(node.value))
    # Standalone concrete file paths and mentioned tools, rather than prose words.
    vocab.update(re.findall(r'(?:/[a-zA-Z0-9_./-]+|\b[\w-]+\.(?:csv|txt)\b)', text))
    for tool in ['Python', 'Path', 'pathlib', 'pdb', 'pdb.set_trace', 'breakpoint', 'sorted', 'str.lower', 'BaseException', 'Exception', 'ValueError', 'OSError', 'FileNotFoundError', 'NameError', 'PermissionError', 'KeyboardInterrupt', 'SystemExit', 'GeneratorExit']:
        if tool in text: vocab.add(tool)

sort_b = bs['sorting_with_key_functions']
records = assignment(examples(sort_b)[0], 'records')
intent = sort_b['practice_anchor']['live_code']['starter_state_intent']
practice_records = ast.literal_eval(re.search(r'records = (\[.*?\])', intent).group(1))
pairs = assignment(examples(bs['lambda_expressions'])[0], 'pairs')
vocab.update(str(v) for r in practice_records for v in r.values())
cols = list(records[0])
ops = []
for old, new in zip(records, practice_records):
    for col in cols:
        if old[col] != new[col]:
            ops.append({'op': 'set_cell', 'where': {'label': old['label']}, 'occurrence': 0, 'column': col, 'value': new[col]})
assets = [{
    'asset_id': 'ds.orders', 'asset_kind': 'dataset', 'scenario_id': scenario_id,
    'title': 'Illustrative order records',
    'description': 'Authored label and quantity records copied from the glossary example, in its original order. Case-label and pair variants support the distinct practice examples; case differences are intentional, not planted quality defects. CSV mount name: orders.csv.',
    'columns': [{'name': col, 'type': 'string' if isinstance(records[0][col], str) else 'integer', 'semantic_role': 'categorical' if col == 'label' else 'numerical', 'numeric_looking_label': False} for col in cols],
    'rows': [[r[c] for c in cols] for r in records], 'provenance': 'authored',
    'variants': [
        {'variant_id': 'var.orders.case_labels', 'derived_from': 'ds.orders', 'purpose': 'Exact lowercase-label sorting practice, with equal normalized keys and unchanged source order.', 'ops': ops, 'planted_issues': []},
        {'variant_id': 'var.orders.pairs', 'derived_from': 'ds.orders', 'purpose': 'Exact two-row data from the lambda pair example.', 'ops': [{'op': 'drop_rows', 'where': {'label': r['label']}} for r in records if (r['label'], r['quantity']) not in pairs], 'planted_issues': []}
    ]
}]

starters = {
'finally_cleanup': '''def read_quantity(text):
    try:
        return int(text.read())
    finally:
        # Complete the release operation without replacing the result.
        pass
''',
'functions_as_values': '''def double(value):
    return value * 2

def apply(operation, value):
    # Invoke the supplied function and return its result.
    pass

# Assign chosen to the function object, then call apply.
''',
'closures_and_enclosing_scope': '''def make_counter():
    count = 0
    def advance():
        # Rebind and return the enclosing count.
        pass
    # Return the nested function without calling it.

counter = make_counter()
other = make_counter()
''',
'pathlib_paths': '''from pathlib import Path
base = Path("/work/project")
# Construct output using the relative filename orders.csv.
''',
'raising_exceptions': '''def cost(quantity):
    return quantity * 4
''',
'reading_tracebacks': '''def read_quantity(text):
    return int(text)

def outer(text):
    return read_quantity(text)

outer("three")
''',
'debugger_usage': '''# Intended behavior: nonnegative quantity selects the nonnegative branch.
def inspect_quantity(quantity):
    breakpoint()
    if quantity < 0:
        return "nonnegative"
    else:
        return "negative"

quantity = 3
inspect_quantity(quantity)
''',
'safe_mutable_defaults': '''def add_label(label, labels=[]):
    labels.append(label)
    return labels

print(add_label("blue"))
print(add_label("red"))
''',
'specific_exception_handlers': '''try:
    raise FileNotFoundError("missing-example.txt")
except OSError:
    print("Other file operation failure")
except FileNotFoundError:
    print("File missing")
''',
'validation_vs_programming_errors': '''# ValueError from malformed numeric quantity input.
input_category = ""
input_response = ""
# NameError caused by a misspelled local quantity name.
implementation_category = ""
implementation_response = ""
# PermissionError opening an otherwise valid input path.
access_category = ""
access_response = ""
''',
'variadic_arguments_and_unpacking': '''def target(quantity, price=4):
    return quantity * price

def wrapper(*args, **kwargs):
    # Forward both collections and return the target result.
    pass
'''
}
starters['exception_propagation'] = examples(bs['exception_propagation'])[0]
starters['sorting_with_key_functions'] = 'records = ' + repr(practice_records) + '\n# Define a named lowercase-label key function and assign ordered.\n'
starters['lambda_expressions'] = 'pairs = ' + repr(pairs) + '\n# Assign ordered using sorted and a one-expression lambda key.\n'

for key, b in bs.items():
    if b['practice_anchor']['type'] != 'live_code': continue
    files = [{'path': 'main.py', 'content': starters[key]}]
    # Full scaffold intent is source-derived; it is not an additional teaching claim.
    files.append({'path': 'README.txt', 'content': b['practice_anchor']['live_code']['starter_state_intent'] + '\n\n' + b['practice_anchor']['objective'] + '\n'})
    for i, code in enumerate(examples(b)):
        files.append({'path': f'reference/example_{i+1}.py', 'content': code})
    if key == 'finally_cleanup':
        # These texts are literal conversion inputs in this scope, not fabricated results.
        good_tree = ast.parse(examples(b)[0])
        good = next(n.args[0].value for n in ast.walk(good_tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'read_quantity')
        bad_tree = ast.parse(examples(bs['exception_propagation'])[0])
        bad = next(n.args[0].value for n in ast.walk(bad_tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'quantity')
        files += [{'path': 'quantity_valid.txt', 'content': good}, {'path': 'quantity_invalid.txt', 'content': bad}]
        files[1]['content'] += '\nFixture files quantity_valid.txt and quantity_invalid.txt contain the glossary conversion inputs. The caller supplies an already opened file as text; the function must close it.\n'
    if key == 'debugger_usage':
        files[1]['content'] += '\nThis asset stores source only. It does not provision an interactive debugger session. Debugger commands belong at the pdb prompt, not in main.py.\n'
    assets.append({'asset_id': 'ws.' + key, 'asset_kind': 'code_workspace', 'scenario_id': scenario_id, 'title': b['context']['concept_name'] + ' practice', 'runtime': 'python', 'files': files})

registry = {'schema_version': '1.0', 'kind': 'scenario_asset_registry', 'path_id': bundle['path_id'], 'batch_id': B.name,
 'scenarios': [{'scenario_id': scenario_id, 'name': 'Quantity project', 'summary': 'A fictional small project processes numeric quantity text, calculates order costs, labels order records, and constructs an orders.csv output path. Its isolated helper exercises use the glossary examples to inspect failure handling and function behavior; no real orders, people, or filesystem services are claimed.', 'domain': 'Python helper functions and illustrative order records', 'glossary_example_vocab': sorted(vocab)}], 'assets': assets}

# Mistakes-to-avoid self-check: shape, unambiguous roles, exact source values,
# variant predicates/ops, scope completeness, and no unneeded plot/runtime assets.
assert len(assets) == 1 + sum(b['practice_anchor']['type'] == 'live_code' for b in bs.values())
assert all(len(row) == len(cols) for row in assets[0]['rows'])
assert assets[0]['columns'][0]['semantic_role'] == 'categorical'
assert assets[0]['columns'][1]['semantic_role'] == 'numerical'
assert [dict(zip(cols, row)) for row in assets[0]['rows']] == records
for variant in assets[0]['variants']:
    derived = [dict(r) for r in records]
    for op in variant['ops']:
        hits = [r for r in derived if all(r[k] == v for k, v in op['where'].items())]
        assert hits
        if op['op'] == 'set_cell': hits[op['occurrence']][op['column']] = op['value']
        else: derived = [r for r in derived if r not in hits]
    if variant['variant_id'].endswith('case_labels'): assert derived == practice_records
    else: assert [(r['label'], r['quantity']) for r in derived] == pairs
    assert not variant['planted_issues']
for b in bs.values():
    assert b['visual_anchor']['type'] not in ['data_table', 'spreadsheet', 'chart']
    assert b['practice_anchor']['type'] not in ['field_selection', 'data_cleanup']
for a in assets[1:]:
    ast.parse(a['files'][0]['content'])
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')
print('Self-check PASS:', len(bs), 'concepts;', len(registry['scenarios']), 'scenario;', len(assets), 'assets;', len(assets[0]['rows']), 'base rows;', len(assets[0]['variants']), 'variants')
print('Asset ids:', ', '.join(a['asset_id'] for a in assets))
