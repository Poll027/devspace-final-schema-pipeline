import ast
import csv
import hashlib
import io
import json
import re
from pathlib import Path

B = Path('batches/final_batch_learn_python.region.05')
bundle = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/learn_python.json').read_text())
concepts = {b['context']['concept_id'].split('.', 1)[1]: b for b in bundle['bundles']}
def texts(key):
    b = concepts[key]
    return '\n'.join(t['content'] for t in b['teaching_blocks']) + '\n' + json.dumps(b['practice_anchor']) + '\n' + json.dumps(b['visual_anchor'])
def example(key):
    return next(t['content'] for t in concepts[key]['teaching_blocks'] if t['purpose'] == 'example')
def code(key):
    return re.search(r'```python\n(.*?)```', example(key), re.S).group(1)

# Mine only teaching blocks and anchors, not prerequisites or blocked future concepts.
vocab = set()
for key, b in concepts.items():
    text = '\n'.join(t['content'] for t in b['teaching_blocks'])
    anchor = b['practice_anchor']
    text += '\n' + anchor['objective'] + '\n' + anchor['success'] + '\n' + b['visual_anchor']['purpose']
    live = anchor.get('live_code', {})
    text += '\n' + live.get('starter_state_intent', '') + '\n' + '\n'.join(live.get('allowed_syntax', []))
    for pattern in [r'\b[\w/]+\.py\b', r'\b[\w]+\.(?:csv|txt)\b', r'\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b', r'\bORDER_[A-Z]+\b', r'--[a-z_]+', r'(?<!\w)-?\d+(?:\.\d+)*(?!\w)', r'"([^"\n]+)"']:
        vocab.update(re.findall(pattern, text))
    for c in re.findall(r'```python\n(.*?)```', text, re.S):
        tree = ast.parse(c)
        vocab.update(n.id for n in ast.walk(tree) if isinstance(n, ast.Name))
        vocab.update(n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value)
    for word in ['report', 'orders', 'cost', 'quantity', 'price', 'helpers', 'logging', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'argparse', 'json', 'os', 'random', 'secrets', 're', 'sys', 'venv', '.venv', 'pip', 'POSIX', 'Windows', 'bin/python', 'Scripts/python.exe', '.venv/bin/python', '.venv/Scripts/python.exe', 'package_name==version', 'module_name', 'notebook', 'simulation']:
        if word in text:
            vocab.add(word)
scenario_id = 'scenario.order_report'
assets = []
def dataset(id_, title, columns, rows, description):
    a = dict(asset_id='ds.' + id_, asset_kind='dataset', scenario_id=scenario_id, title=title, description=description, columns=[dict(name=n, type=t, semantic_role=r, description=d) for n,t,r,d in columns], rows=rows, provenance='authored', variants=[])
    assets.append(a)
    return a

# Extract fixed inputs directly from glossary code, retaining the taught names.
date_tree = ast.parse(code('datetime_operations'))
date_assigns = [n for n in date_tree.body if isinstance(n, ast.Assign)]
date_names = [n.targets[0].id for n in date_assigns]
date_values = [n.value.func.value.args[0].value for n in date_assigns]
dates = dataset('report_dates', 'Report calendar dates', [(n,'date','datetime','Calendar date supplied as year-month-day text; subtraction order is significant.') for n in date_names], [date_values], 'Fictional report dates using the glossary inputs. No elapsed-time result is stored.')
first, second = date_names
for suffix, col, val, purpose in [('reversed',first,date_values[1],'Reverse the supplied calendar-date order.'),('same_day',second,date_values[0],'Two equal calendar dates.')]:
    ops = [dict(op='set_cell', where={first:date_values[0]}, occurrence=0, column=col, value=val)]
    if suffix == 'reversed':
        ops.append(dict(op='set_cell', where={first:date_values[1]}, occurrence=0, column=second, value=date_values[0]))
    dates['variants'].append(dict(variant_id='var.dates_'+suffix, derived_from=dates['asset_id'], purpose=purpose, ops=ops, planted_issues=[]))

main_tree = ast.parse(code('main_entry_point'))
helper = next(n for n in main_tree.body if isinstance(n, ast.FunctionDef))
helper_code = ast.unparse(helper) + '\n'
call = next(n for n in ast.walk(main_tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == helper.name)
params = [p.arg for p in helper.args.args]
args = [n.value for n in call.args]
orders = dataset('orders', 'Order cost inputs', [(params[0],'integer','numerical','Authored quantity passed to cost; this is a count, not an identifier.'),(params[1],'number','numerical','Authored unit price passed to cost; no real-world price or currency claim.')], [args, [args[1],args[0]]], 'Minimal fictional orders.csv inputs for the shared cost helper; totals are computed by learner code.')
for i, name in enumerate(params):
    orders['variants'].append(dict(variant_id='var.orders_zero_'+name, derived_from=orders['asset_id'], purpose='A valid zero '+name+' edge case, not a data defect.', ops=[dict(op='set_cell',where={params[0]:args[0]},occurrence=0,column=name,value=0)],planted_issues=[]))
label_text = concepts['regular_expressions']['practice_anchor']['live_code']['starter_state_intent']
label_values = ast.literal_eval(re.search(r'\[.*?\]', label_text).group(0))
label_tree = ast.parse(code('regular_expressions'))
label_name = next(n.target.id for n in label_tree.body if isinstance(n,ast.For))
labels = dataset('labels', 'Whole-label validation inputs', [(label_name,'string','text','Complete input text to validate, not a predefined category. The empty string is an intentional input.')], [[v] for v in label_values], 'The exact practice labels: valid uppercase strings, mixed case, a trailing disallowed character, and an intentionally empty string. No expected Booleans are authored.')

# Only live-code concepts not overridden by the path profile receive workspaces.
def workspace(key, files):
    cid = concepts[key]['context']['concept_id']
    assert cid not in profile['practice_type_by_concept']
    assets.append(dict(asset_id='ws.'+key,asset_kind='code_workspace',scenario_id=scenario_id,title=concepts[key]['context']['concept_name'],runtime='python',files=[dict(path=p,content=c) for p,c in files.items()]))
workspace('datetime_operations', {'main.py': 'from datetime import datetime\n' + ''.join(f'{n} = {v!r}\n' for n,v in zip(date_names,date_values)) + '# Parse both strings into calendar dates, then display both signed day differences.\n'})
report_file = re.search(r'\breport\.py\b', example('local_modules')).group(0)
workspace('local_modules', {report_file: helper_code + '\n' + ast.unparse(call) + '\n# Move the helper into sibling helpers.py, then import and call it here.\n'})
costs_file = re.search(r'\bcosts\.py\b', example('importable_packages')).group(0)
workspace('importable_packages', {costs_file: helper_code, 'report.py':'# Group costs.py and a second related module in orders, including an empty __init__.py.\n# Import orders.costs and display the package-qualified cost call.\n'})
logging_tree = ast.parse(code('logging'))
messages = [n.args[0].value for n in ast.walk(logging_tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('debug','info')]
workspace('logging', {'report.py': 'def report():\n' + ''.join(f'    print({m!r})\n' for m in messages) + '\nreport()\n# Replace diagnostic prints with a module logger and configure application logging.\n'})
workspace('main_entry_point', {'report.py':helper_code + '\nprint(' + ast.unparse(call) + ')\n# Guard command actions while keeping the helper importable.\n'})
# This command-line concept is NOT overridden in the supplied path profile.
workspace('argparse_command_line', {'report.py':'import argparse\n# Define required input_path and optional --verbose, parse arguments and print their values.\n'})
workspace('module_search_paths', {'report.py':code('module_search_paths'), 'json.py':'# This local filename deliberately conflicts with the standard-library module.\n'})
workspace('os_environment', {'main.py':'import os\nrequired = None\n# Complete required using os.environ.get for ORDER_SOURCE.\n# Explicitly report absence; otherwise display the configured nonsecret directory string.\n'})
seed_syntax = next(s for s in concepts['random_vs_secrets']['practice_anchor']['live_code']['allowed_syntax'] if s.startswith('random.seed('))
workspace('random_vs_secrets', {'main.py':'import random\n'+seed_syntax+'\n# Store several random.random() results, reset the seed, and repeat the calls.\n# Display sequence equality and comparisons to the documented bounds.\n'})
workspace('regular_expressions', {'main.py':'import re\n# Define a pattern requiring a nonempty uppercase-letter label.\npattern = None\nfor '+label_name+' in '+repr(label_values)+':\n    # Replace the placeholder with a whole-text match and an explicit success test.\n    accepted = None\n    print('+label_name+', accepted)\n'})

registry = dict(schema_version='0.1.0',kind='scenario_asset_registry',path_id=bundle['path_id'],batch_id=B.name,scenarios=[dict(scenario_id=scenario_id,name='Notebook order-report workshop',summary='A fictional small project calculates order costs and signed report-date differences, validates uppercase labels, and organises reusable report helpers. Its maintainers practise diagnostics, command arguments, environment settings and simulation code. Interpreter and dependency exercises are read-only inspection tasks, not provisioned services or environments.',domain='Fictional Python order-report project',glossary_example_vocab=sorted(vocab))],assets=assets)
# Materialise dataset CSVs without authored hashes or copied outputs.
for a in assets:
    if a['asset_kind'] != 'dataset':
        continue
    name = 'orders.csv' if a['asset_id'] == orders['asset_id'] else a['asset_id'].split('.',1)[1]+'.csv'
    p = B/'assets'/name
    with p.open('w',newline='') as f:
        w=csv.writer(f);w.writerow([c['name'] for c in a['columns']]);w.writerows(a['rows'])
    raw=p.read_bytes()
    a['data_file']=dict(uri=str(p.relative_to(B)),format='csv',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')

# Own mistakes-to-avoid and scope checklist.
assert len({a['asset_id'] for a in assets}) == len(assets)
for a in assets:
    if a['asset_kind']=='dataset':
        assert all(len(row)==len(a['columns']) for row in a['rows'])
        for c in a['columns']:
            assert c['semantic_role']!='numerical' or c['type'] in ('integer','number')
            assert not c.get('numeric_looking_label',False)  # No digits used as labels in this batch.
    else:
        for f in a['files']:
            if f['path'].endswith('.py'):
                ast.parse(f['content'])
planned_find=[]
for key,b in concepts.items():
    p=b['practice_anchor']
    if p['type'] in ('field_selection','data_cleanup') and re.search(r'flag|problem|issue|quality|duplicate|missing',p['objective']+' '+p['success'],re.I):
        planned_find.append(key)
assert not planned_find
expected = {b['context']['concept_id'] for b in bundle['bundles'] if b['practice_anchor']['type']=='live_code'} - set(profile['practice_type_by_concept'])
actual = {'python.'+a['asset_id'][3:] for a in assets if a['asset_kind']=='code_workspace'}
assert expected==actual
assert not any(b['visual_anchor']['type'] in ('chart','data_table','spreadsheet') for b in bundle['bundles'])
checklist=dict(concepts_covered=len(concepts),scenario_count=len(registry['scenarios']),asset_count=len(assets),dataset_count=sum(a['asset_kind']=='dataset' for a in assets),workspace_count=len(actual),inspect_and_judge_count=len(set(b['context']['concept_id'] for b in bundle['bundles'])&set(profile['practice_type_by_concept'])),variant_count=sum(len(a.get('variants',[])) for a in assets),planned_find_issues=planned_find,checks=['Row widths match columns.','Numeric measures have numeric types; calendar dates have datetime roles; whole-label inputs are text.','No numeric-looking identifier traps appear in the supplied glossary.','All variants use declared operations; edge variants intentionally contain no defects.','No duplicate-row operations or occurrence ambiguity.','Exact glossary date, cost and label inputs retained; output values not typed.','All non-overridden live-code anchors have Python workspaces; inspect-and-judge anchors have none.','No glossary plots or required table visuals; no image rendering needed.'])
(B/'working/scenario_registry_checklist.json').write_text(json.dumps(checklist,indent=2)+'\n')
print(json.dumps(checklist,indent=2))
