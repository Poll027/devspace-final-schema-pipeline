import ast
import json
import re
from pathlib import Path

batch = Path('batches/final_batch_learn_python.region.04')
bundle = json.loads((batch / 'inputs/path_glossary_bundle.json').read_text())
bs = bundle['bundles']
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/learn_python.json').read_text())
scenario_id = 'scenario.order_reports'
vocab = set()
for b in bs:
    texts = [t['content'] for t in b['teaching_blocks']]
    texts += [json.dumps(b['practice_anchor'], ensure_ascii=False), json.dumps(b['visual_anchor'], ensure_ascii=False)]
    for text in texts:
        vocab.update(re.findall(r'\b[\w]+\.(?:txt|csv|bin)\b', text))
        for code in re.findall(r'```python\n(.*?)```', text, flags=re.S):
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Name): vocab.add(node.id)
                elif isinstance(node, (ast.ClassDef, ast.FunctionDef)): vocab.add(node.name)
                elif isinstance(node, ast.Attribute): vocab.add(node.attr)
                elif isinstance(node, ast.arg): vocab.add(node.arg)
                elif isinstance(node, ast.Constant): vocab.add(str(node.value))
    for syntax in b['practice_anchor'].get('live_code', {}).get('allowed_syntax', []):
        vocab.update(re.findall(r'[A-Za-z_]\w*', syntax))
        vocab.update(re.findall(r'"([^"\n]+)"', syntax))

starters = {
'classes_and_instances': '# Define Order and create first and second as separate instances.\n# Print their identity comparison.\n',
'file_modes': 'path = "report.txt"\nreport_text = "First"\n\n# Exclusively create and write the report, closing it afterward.\n# Handle an existing destination without changing it.\n',
'instance_initialization': 'class Order:\n    def __init__(self, label, quantity):\n        # Store the constructor arguments on this instance.\n        pass\n\norder = Order("notebook", 3)\nprint(order.label, order.quantity)\n',
'instance_methods': 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n\n    # Implement add(self, amount).\n\norder = Order(3)\norder.add(2)\nprint(order.quantity)\n',
'class_and_static_methods': 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n\n    # Implement from_text as a class method, constructing through cls.\n\norder = Order.from_text("3")\nprint(order.quantity)\n',
'composition': None,
'encapsulation_conventions': 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n\n    def add(self, amount):\n        # Update and return the supporting state.\n        pass\n\norder = Order(3)\nprint(order.add(2))\n',
'inheritance_and_super': 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n\n    def format(self):\n        return f"Quantity: {self.quantity}"\n\n# Implement FeeOrder with delegated initialization and formatting.\n\nprint(FeeOrder(3, 2).format())\n',
'custom_exceptions': '# Define InvalidRecordError as an Exception subclass.\n\ndef check_quantity(quantity):\n    # Reject negative quantities with the custom exception.\n    pass\n\n# Complete a caller boundary with a matching handler.\n# Check both quantity 2 and quantity -1.\n',
'instance_vs_class_attributes': 'class Order:\n    labels = []\n\nfirst = Order()\nsecond = Order()\nfirst.labels.append("blue")\nprint(first.labels)\nprint(second.labels)\n',
'json_serialization': 'import json\n\nrecord = {"quantities": [(3, 2)], "active": True}\n\n# Serialize record, deserialize the text, and compare reconstructed values.\n',
'object_introspection': 'class Order:\n    def __init__(self):\n        self.quantity = 3\n\ndef make_order():\n    return Order()\n\norder = make_order()\n# Inspect type, membership, candidate public names, and named attributes.\n',
'pathlib_filesystem_operations': 'from pathlib import Path\n\ndirectory = Path("output/reports")\nsource = Path("incoming/report.txt")\nfilename = "report.txt"\n\n# Create the directory, construct target, and move source to target.\n# Inspect immediate entries without assuming their order.\n',
'special_methods': 'class Order:\n    def __init__(self, quantity):\n        self.quantity = quantity\n\n    # Add __repr__ and __str__, each returning a string.\n\norder = Order(3)\nprint(repr(order))\nprint(order)\n',
 'text_file_encodings': 'source = open("label.txt", "r")  # Specify the explicit matching encoding.\ntext = source.read()\nsource.close()\ndestination = open("label.txt", "w")  # Specify the explicit matching encoding.\ndestination.write(text)\ndestination.close()\nprint(text)\n',
'file_and_format_errors': 'import csv\n\ndef import_rows(path):\n    file = None\n    rows = []\n    try:\n        file = open(path, mode="r", encoding="utf-8", newline="")\n        reader = csv.DictReader(file)\n        for row in reader:\n            # Validate missing/empty required fields and excess fields.\n            rows.append(row)\n        return rows\n    # Add cause-specific exception handlers here.\n    finally:\n        if file is not None:\n            file.close()\n',
'with_resource_management': '# Replace the unfinished file-processing boundary with managed opening.\ntry:\n    # Read label.txt into text inside the managed body.\n    # Test normal processing, then raise ValueError("Processing failed").\n    pass\nexcept ValueError:\n    print("Processing failed")\n\n# Inspect source.closed after either path.\n',
'binary_files': '# Copy source.bin to disposable copy.bin with nested managed blocks.\n# Read bytes into payload and write that value directly.\n',
}
# Keep the composition reference exactly as supplied by the glossary.
composition = next(b for b in bs if b['context']['concept_id'] == 'python.composition')
starters['composition'] = re.search(r'```python\n(.*?)```', '\n'.join(t['content'] for t in composition['teaching_blocks']), re.S).group(1) + '\n# Replace the calculator collaborator with a formatter collaborator.\n'
assets = []
def workspace(b, files, suffix='', title_suffix=''):
    cid = b['context']['concept_id']
    assets.append({'asset_id': 'ws.' + cid.split('.',1)[1] + suffix,
                   'asset_kind': 'code_workspace', 'scenario_id': scenario_id,
                   'title': b['context']['concept_name'] + title_suffix,
                   'runtime': 'python',
                   'files': [{'path': p, 'content': c} for p,c in files.items()]})
for b in bs:
    cid = b['context']['concept_id']
    assert cid not in profile['practice_type_by_concept']
    short = cid.split('.',1)[1]
    files = {'main.py': starters[short]}
    if short == 'file_modes':
        workspace(b, files, '.absent', ' — absent report')
        workspace(b, {**files, 'report.txt': 'First'}, '.existing', ' — existing report')
        continue
    if short in ('text_file_encodings', 'with_resource_management'):
        files['label.txt'] = 'café'
    elif short == 'pathlib_filesystem_operations':
        files['incoming/report.txt'] = 'First'
    elif short == 'binary_files':
        # Authored ASCII-range bytes represented losslessly as workspace text.
        files['source.bin'] = bytes([0, 1, 2, 3, 10, 13, 65, 127]).decode('ascii')
        files['copy.bin'] = 'Disposable destination'
    elif short == 'file_and_format_errors':
        files['valid.csv'] = 'label,quantity\nnotebook,3\nnotebook,2\n'
        files['missing.csv'] = 'label,quantity\nnotebook\n'
        files['empty.csv'] = 'label,quantity\nnotebook,\n'
        files['excess.csv'] = 'label,quantity\nnotebook,3,extra\n'
        files['parser_case.py'] = '# Host-side fixture: call import_rows with this reader patched into csv.DictReader.\nimport csv\n\ndef parser_failure(file):\n    raise csv.Error("Parser-reported failure")\n'
        files['fixture_setup.py'] = '# Host-side fixture setup, not learner code. Run before the decoding-failure check.\nfrom pathlib import Path\n\nPath("invalid_utf8.csv").write_bytes(b"label,quantity\\nnotebook,\\xff\\n")\n'
        files['FIXTURES.md'] = ('Authored fixtures use only label and quantity. valid.csv has accepted rows; missing.csv has an absent field, empty.csv an empty field, and excess.csv an excess field under DictReader\'s default None key. For the missing-source check use a nonexistent path. The host can run fixture_setup.py to create invalid_utf8.csv, then call import_rows on it. For a parser-reported failure the host can substitute parser_case.parser_failure for csv.DictReader; malformed row widths alone do not establish csv.Error. Fixture helpers are not part of the learner\'s allowed syntax.\n')
    workspace(b, files)

# Read-only record data complements the CSV import examples; raw row-shape
# defects remain in the workspace fixtures, since a rectangular CSV mount
# cannot represent an excess-field row without changing the header.
columns = [{'name':'label', 'type':'string', 'semantic_role':'categorical', 'description':'Item label supplied to Order.'},
           {'name':'quantity', 'type':'integer', 'semantic_role':'numerical', 'description':'Item count supplied to Order.'}]
rows = [['notebook',3], ['notebook',2]]
where = {'label':'notebook', 'quantity':2}
assets.append({'asset_id':'ds.orders','asset_kind':'dataset','scenario_id':scenario_id,
               'title':'Authored order records','description':'Small label/quantity records consistent with the Order and CSV examples. Raw missing-field and excess-field CSV fixtures are in ws.file_and_format_errors.',
               'columns':columns,'rows':rows,'provenance':'authored',
               'variants':[{'variant_id':'missing_quantity','derived_from':'ds.orders',
                            'purpose':'Required quantity missing for explicit row validation.',
                            'ops':[{'op':'set_cell','where':where,'occurrence':0,'column':'quantity','value':None}],
                            'planted_issues':[{'issue_id':'issue.missing_quantity','kind':'missing_value',
                                               'locations':[{'where':{'label':'notebook','quantity':None},'occurrence':0,'column':'quantity'}],
                                               'description':'The required quantity is missing.'}]}]})
registry = {'schema_version':'1.0','kind':'scenario_asset_registry', 'path_id':bundle['path_id'], 'batch_id':bundle['batch_id'],
            'scenarios':[{'scenario_id':scenario_id,'name':'Order report workshop',
                          'summary':'A fictional stationery workshop uses small Order objects for notebook quantities and writes local reports. Learners edit isolated Python examples with authored local fixtures; no real orders or services are involved.',
                          'domain':'Local order records and report files','glossary_example_vocab':sorted(vocab)}],
            'assets':assets}
(batch / 'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
# Stage-local mistakes-to-avoid audit.
assert len(starters) == len(bs)
assert len({a['asset_id'] for a in assets}) == len(assets)
for a in assets:
    if a['asset_kind'] == 'code_workspace':
        for f in a['files']:
            if f['path'].endswith('.py'): ast.parse(f['content'])
    if a['asset_kind'] == 'dataset':
        assert all(len(r) == len(a['columns']) for r in a['rows'])
        for c in a['columns']:
            assert c['semantic_role'] in ('categorical','numerical')
            assert not (c['semantic_role']=='numerical' and c['type']=='string')
        for v in a['variants']:
            derived = [dict(zip([c['name'] for c in a['columns']], r)) for r in a['rows']]
            for op in v['ops']:
                matches = [r for r in derived if all(r[k]==val for k,val in op['where'].items())]
                matches[op.get('occurrence',0)][op['column']] = op['value']
            for issue in v['planted_issues']:
                for loc in issue['locations']:
                    matches = [r for r in derived if all(r[k]==val for k,val in loc['where'].items())]
                    assert matches[loc['occurrence']][loc['column']] is None
assert not any(b['practice_anchor']['type'] in ('field_selection','data_cleanup') for b in bs)
assert not any(b['visual_anchor']['type'] in ('chart','data_table','spreadsheet') for b in bs)
print(json.dumps({'concepts':len(bs),'scenarios':len(registry['scenarios']),'assets':len(assets),'asset_ids':[a['asset_id'] for a in assets], 'mistakes_checklist':'passed'},indent=2))
