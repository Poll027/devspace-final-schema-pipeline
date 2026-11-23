import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
bundle = json.loads((BASE / 'inputs/path_glossary_bundle.json').read_text())
bs = {b['context']['concept_id'].split('.')[-1]: b for b in bundle['bundles']}
scenario_id = 'scenario.order_report'

def example(key):
    return next(t['content'] for t in bs[key]['teaching_blocks'] if t['purpose'] == 'example')

def fenced(key):
    return re.search(r'```python\n(.*?)```', example(key), re.S).group(1)

# Mine literal examples, identifiers and filenames from the actual taught text.
vocab = ['order-report script', 'order-cost helper', 'calendar dates', 'uppercase-letter label', 'virtual environment', 'standard-library module']
for b in bundle['bundles']:
    text = '\n'.join(t['content'] for t in b['teaching_blocks']) + '\n' + json.dumps(b['practice_anchor']) + '\n' + json.dumps(b['visual_anchor'])
    vocab.extend(re.findall(r'\b(?:[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+|[A-Z][A-Z_]+|\d{4}-\d{2}-\d{2}|\d+(?:\.\d+)?|datetime|strptime|timedelta|helpers|orders|cost|quantity|price|first|second|logging|logger|argparse|parser|input_path|verbose|random|secrets|pattern|label|accepted|notebook|json|sys|os|venv|pip|package_name|module_name|version)\b', text))
    vocab.extend(re.findall(r'--[a-z_]+|%[Ymd]|\.venv(?:/[\w./]+)?|__init__\.py|requirements\.txt|\[A-Z\]\[A-Z\]\*', text))
vocab = list(dict.fromkeys(vocab))

# Input literals are extracted, not retyped. No expected execution output is authored.
dates = re.findall(r'"(\d{4}-\d{2}-\d{2})"', fenced('datetime_operations'))
call = re.search(r'cost\((\d+), (\d+)\)', example('local_modules'))
q, p = map(int, call.groups())
regex_starter = bs['regular_expressions']['practice_anchor']['live_code']['starter_state_intent']
labels = ast.literal_eval(re.search(r'list (\[.*?\])', regex_starter).group(1))
seed = int(re.search(r'random.seed\((\d+)\)', example('random_vs_secrets')).group(1))
messages = re.findall(r'logger\.(?:debug|info)\("(.*?)"\)', fenced('logging'))

assets = []
# Minimal shared authored table; values beyond the exact glossary example are
# fictional exercise inputs, not real-world records or computed answer cells.
rows = [[q, p], [q + 1, p], [q, p + 1], [0, p], [q, 0]]
columns = [dict(name=n, type='integer', semantic_role='numerical', description=d)
           for n, d in [('quantity', 'Number of units in the fictional order.'), ('price', 'Unit price used only as an exercise input; no currency is asserted.')]]
asset_id = 'ds.orders'
s = io.StringIO(newline='')
w = csv.writer(s)
w.writerow([c['name'] for c in columns]); w.writerows(rows)
raw = s.getvalue().encode()
(BASE / 'assets').mkdir(exist_ok=True)
(BASE / 'assets/orders.csv').write_bytes(raw)
assets.append(dict(asset_id=asset_id, asset_kind='dataset', scenario_id=scenario_id,
                   title='Fictional order-cost inputs', description='Authored quantity and price inputs for the shared cost helper and the orders.csv input path.',
                   columns=columns, rows=rows, provenance='authored',
                   data_file=dict(uri='assets/orders.csv', format='csv', sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)),
                   variants=[dict(variant_id='variant.orders.changed_inputs', derived_from=asset_id,
                                  purpose='Alternate cost inputs for hidden checks without hard-coded results.',
                                  ops=[dict(op='set_cell', where={'quantity': q + 1, 'price': p}, occurrence=0, column='price', value=p + 2)], planted_issues=[])]))

cost_definition = 'def cost(quantity, price):\n    return quantity * price\n'
cost_call = f'cost({q}, {p})'
starter_files = {
 'datetime_operations': [('main.py', f'first = {dates[0]!r}\nsecond = {dates[1]!r}\n# Parse both dates and display both signed differences.\n')],
 'local_modules': [('report.py', cost_definition + f'\nprint({cost_call})\n')],
 'importable_packages': [('costs.py', cost_definition), ('report.py', '# Create the orders package and a second related module, then import and call the cost helper.\n')],
 'logging': [('report.py', 'def report():\n' + ''.join(f'    print({m!r})\n' for m in messages) + '\nreport()\n')],
 'main_entry_point': [('report.py', cost_definition + '\nquantity = int(input("Quantity: "))\nprice = int(input("Price: "))\nprint(cost(quantity, price))\n')],
 'argparse_command_line': [('report.py', 'import argparse\n# Declare the command interface, parse arguments, and display their attributes.\n'), ('orders.csv', raw.decode())],
 'module_search_paths': [('report.py', fenced('module_search_paths')), ('json.py', '# Deliberately conflicting local module for the import-location diagnostic.\n')],
 'os_environment': [('main.py', 'import os\n# Read required ORDER_SOURCE and report its absence explicitly.\n')],
 'random_vs_secrets': [('main.py', f'import random\nrandom.seed({seed})\n# Store several random.random() values, reset the seed, and repeat.\n')],
 'regular_expressions': [('main.py', 'import re\npattern = ""  # Complete the pattern.\n' + f'for label in {labels!r}:\n    accepted = None  # Complete the whole-text validation.\n    print(label, accepted)\n')],
 'sys_runtime_interface': [('main.py', '# Add the sys import and print the actual executable and version.\n')],
 'virtual_environments': [('diagnostic.py', '# Inspect sys.prefix and sys.base_prefix in the explicitly selected environment.\n')],
 'environment_interpreter_selection': [('diagnostic.py', 'import sys\nprint(sys.executable)\nprint(sys.prefix != sys.base_prefix)\n')],
 'pip_installation': [('import_check.py', '# Use only the project-documented import name; no distribution name is assumed.\n')],
 'requirements_files': [('requirements.txt', '# No verified project dependencies were supplied in the glossary.\n# package_name==version is illustrative only, not an installable specification.\n'), ('import_check.py', '# Add only imports documented by the verified project dependency specification.\n')],
}
for key, b in bs.items():
    anchor = b['practice_anchor']
    # The README preserves scaffolding requirements without inventing runtime
    # paths, package versions, installation logs, or provisioning resources.
    instructions = '\n\n'.join([anchor['objective'], anchor['live_code']['starter_state_intent'], anchor['success']]) + '\n'
    files = [dict(path=path, content=content) for path, content in starter_files[key]]
    files.append(dict(path='README.md', content=instructions))
    assets.append(dict(asset_id='ws.' + key, asset_kind='code_workspace', scenario_id=scenario_id,
                       title=b['context']['concept_name'], runtime='python', files=files))
registry = dict(schema_version='1.0', kind='scenario_asset_registry', path_id=bundle['path_id'], batch_id=BASE.name,
                scenarios=[dict(scenario_id=scenario_id, name='Order report workshop',
                                summary='A fictional small project maintains an order-cost helper and report scripts, checks calendar-date differences and labels, and reviews its Python environment configuration.',
                                domain='Fictional Python order-report project', glossary_example_vocab=vocab)], assets=assets)
(BASE / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2) + '\n')
# Stage mistakes-to-avoid checklist, scoped to the actual anchors.
assert set(starter_files) == set(bs)
assert all(len(row) == len(columns) for row in rows)
assert all(c['semantic_role'] == 'numerical' and c['type'] == 'integer' for c in columns)
assert len(set(tuple(row) for row in rows)) == len(rows)
assert rows[0] == [q, p]
assert dates and labels and messages
assert all(b['practice_anchor']['type'] == 'live_code' for b in bs.values())  # no planned find_issues
assert all(b['visual_anchor']['type'] not in ('chart', 'data_table', 'spreadsheet') for b in bs.values())
assert len({a['asset_id'] for a in assets}) == len(assets)
print(json.dumps({'concepts': len(bs), 'scenarios': 1, 'assets': len(assets), 'datasets': 1, 'workspaces': len(bs), 'variants': 1, 'vocabulary_terms': len(vocab), 'checklist': 'PASS'}, indent=2))
