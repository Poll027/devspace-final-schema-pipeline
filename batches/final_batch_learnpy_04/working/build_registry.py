import ast, io, json, keyword, re, tokenize
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.04')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bundles={b['context']['concept_id'].split('.',1)[1]:b for b in g['bundles']}
scenario='scn.python_order_workshop'
# Vocabulary is mined from the supplied teaching blocks and both anchors.
vocab=set()
for b in g['bundles']:
    texts=[t['content'] for t in b['teaching_blocks']]
    texts += [json.dumps(b[k],ensure_ascii=False) for k in ('visual_anchor','practice_anchor')]
    for text in texts:
        vocab.update(re.findall(r'\b[\w.-]+\.(?:txt|csv|bin)\b',text))
        for snippet in re.findall(r'```python\n(.*?)```',text,re.S):
            try:
                for t in tokenize.generate_tokens(io.StringIO(snippet).readline):
                    if t.type==tokenize.NAME and not keyword.iskeyword(t.string): vocab.add(t.string)
                    if t.type==tokenize.NUMBER: vocab.add(t.string)
                    if t.type==tokenize.STRING:
                        value=ast.literal_eval(t.string) if not t.string.startswith(('f','F')) else None
                        if isinstance(value,str) and value: vocab.add(value)
            except (SyntaxError,tokenize.TokenError,ValueError): pass
    # Mine string literals and named tokens from the anchor's syntax inventory.
    for syntax in b['practice_anchor']['live_code']['allowed_syntax']:
        vocab.update(re.findall(r'\b(?:[A-Z][A-Za-z]+|self\.[A-Za-z_]+|cls|quantity|label|fee|formatter|directory|source|filename|target)\b',syntax))
        vocab.update(re.findall(r'"([^"\n]+)"',syntax))
# Non-code examples have vocabulary that must not be lost.
for key in ('file_modes','file_and_format_errors','pathlib_filesystem_operations'):
    for t in bundles[key]['teaching_blocks']:
        if t['purpose']=='example':
            vocab.update(re.findall(r'\b(?:First|Second|notebook|extra|label|quantity|directory|source|filename|target|FileExistsError|DictReader|None|Unix|Windows)\b',t['content']))
starters={
'classes_and_instances': '# Define Order, then create first and second using separate calls.\n# Compare their identities using is.\n',
'file_modes': 'path = "report.txt"\nreport_text = "First"\n# Exclusively create the report, write report_text, and close it.\n# Handle FileExistsError without modifying an existing report.\n',
'instance_initialization': '''class Order:
    def __init__(self, label, quantity):
        # Store both supplied values on this instance.
        pass

order = Order("notebook", 3)
print(order.label, order.quantity)
''',
'instance_methods': '''class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    # Add add(self, amount) here.

order = Order(3)
# Call the new method with 2, then display the stored quantity.
''',
'class_and_static_methods': '''class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    # Add the alternative constructor from_text here.

# Construct order through Order.from_text("3") and inspect quantity.
''',
'composition': '''class Calculator:
    def cost(self, quantity):
        return quantity * 4

class Report:
    def __init__(self, calculator):
        self.calculator = calculator
    def total(self, quantity):
        return self.calculator.cost(quantity)

report = Report(Calculator())
print(report.total(3))
# Replace the calculator collaborator with a formatter collaborator.
# Keep formatting in the collaborator and delegate from Report.total.
''',
'encapsulation_conventions': '''class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def add(self, amount):
        # Rename supporting state consistently, then update and return it.
        pass

order = Order(3)
print(order.add(2))
''',
'inheritance_and_super': '''class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    def format(self):
        return f"Quantity: {self.quantity}"

class FeeOrder(Order):
    def __init__(self, quantity, fee):
        # Delegate inherited initialization, then store fee.
        pass
    def format(self):
        # Extend the inherited formatted text using super().
        pass

order = FeeOrder(3, 2)
print(order.format())
''',
'custom_exceptions': '''# Define InvalidRecordError as an Exception subclass.
def check_quantity(quantity):
    # Reject negative quantities with the custom exception.
    pass

# Add a caller boundary with an except InvalidRecordError handler.
''',
'instance_vs_class_attributes': '''class Order:
    labels = []

first = Order()
second = Order()
first.labels.append("blue")
print(first.labels)
print(second.labels)
# Move the shared list to per-instance initialization.
''',
'json_serialization': '''import json
record = {"quantities": [(3, 2)], "active": True}
# Serialize to text, deserialize to restored, then compare its values.
''',
'object_introspection': '''class Order:
    def __init__(self):
        self.quantity = 3

def supplied_order():
    return Order()

order = supplied_order()
# Inspect type, membership, candidate public names, quantity, and missing.
# Explain the limitations of dir and the underscore convention.
''',
'pathlib_filesystem_operations': '''from pathlib import Path

directory = Path("output/reports")
source = Path("generated/report.txt")
filename = "report.txt"
# Create the output directory and missing parents.
# Construct target from directory and filename, then move source there.
# Inspect immediate entries without assuming traversal order.
''',
'special_methods': '''class Order:
    def __init__(self, quantity):
        self.quantity = quantity
    # Add __repr__ and __str__, each returning a string.

order = Order(3)
# Inspect repr(order), str(order), and print(order).
''',
'text_file_encodings': '''# Supply explicit UTF-8 encoding arguments on both open calls.
source = open("label.txt", "r")
text = source.read()
source.close()
destination = open("label.txt", "w")
destination.write(text)
destination.close()
print(text)
''',
'file_and_format_errors': '''import csv

def import_rows(path):
    file = None
    rows = []
    try:
        file = open(path, mode="r", encoding="utf-8", newline="")
        reader = csv.DictReader(file)
        for row in reader:
            # Validate label and quantity, including missing/empty/excess fields.
            rows.append(row)
        return rows
    # Add separate missing-source, decoding-failure, and parsing-failure handlers.
    finally:
        if file is not None:
            file.close()
''',
'with_resource_management': '''source = None
try:
    # Use with to open label.txt in UTF-8 and read into text.
    # Test normal processing and a ValueError raised inside the managed body.
    pass
except ValueError:
    print("Processing failed")
# Inspect source.closed after successful entry and either body outcome.
''',
'binary_files': '''# Copy source.bin into the disposable copy.bin using nested with blocks.
# Read in rb mode and write the bytes directly in wb mode.
'''
}
assets=[]
def workspace(key, suffix='', extra=()):
    b=bundles[key]
    files=[{'path':'main.py','content':starters[key]}]
    # Preserve the exact glossary reference for downstream code walkthroughs.
    code=[c for t in b['teaching_blocks'] for c in re.findall(r'```python\n(.*?)```',t['content'],re.S)]
    if code: files.append({'path':'glossary_reference.py','content':'\n\n'.join(code)})
    files.extend({'path':p,'content':c} for p,c in extra)
    assets.append({'asset_id':'ws.'+key+suffix,'asset_kind':'code_workspace','scenario_id':scenario,'title':b['context']['concept_name']+(' — existing report' if suffix else ''),'runtime':'python','files':files})
# Source UTF-8 text is mined from the glossary literal, not transcribed output.
encoding_example=next(t['content'] for t in bundles['text_file_encodings']['teaching_blocks'] if t['purpose']=='example')
label=ast.literal_eval(re.search(r'destination.write\((".*?")\)',encoding_example).group(1))
mode_example=next(t['content'] for t in bundles['file_modes']['teaching_blocks'] if t['purpose']=='example')
report_text=re.search(r'already contains (\w+)',mode_example).group(1)
init_example=next(t['content'] for t in bundles['instance_initialization']['teaching_blocks'] if t['purpose']=='example')
init_code=re.search(r'```python\n(.*?)```',init_example,re.S).group(1)
call=next(n for n in ast.walk(ast.parse(init_code)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Order')
row=[ast.literal_eval(a) for a in call.args]
header = ','.join(a.arg for n in ast.walk(ast.parse(init_code)) if isinstance(n,ast.FunctionDef) and n.name=='__init__' for a in n.args.args[1:])
valid_csv = header + '\n' + ','.join(map(str,row)) + '\n'
missing_csv = header + '\n' + str(row[0]) + '\n'
errors_example = next(t['content'] for t in bundles['file_and_format_errors']['teaching_blocks'] if t['purpose']=='example')
excess_value = re.search(r'notebook,3,(\w+)', errors_example).group(1)
excess_csv = valid_csv.rstrip('\n') + ',' + excess_value + '\n'
empty_quantity_csv = header + '\n' + str(row[0]) + ',\n'
empty_label_csv = header + '\n,' + str(row[1]) + '\n'
for key in bundles:
    extra=[]
    if key in ('text_file_encodings','with_resource_management'):extra=[('label.txt',label)]
    if key=='pathlib_filesystem_operations':extra=[('generated/report.txt',report_text)]
    if key=='binary_files':extra=[('source.bin',label),('copy.bin',report_text)]
    if key=='file_and_format_errors':
        extra=[('orders.csv',valid_csv),('missing_quantity.csv',missing_csv),('excess_field.csv',excess_csv),('empty_quantity.csv',empty_quantity_csv),('empty_label.csv',empty_label_csv),('README.md','Read-only input fixtures illustrate valid, missing, empty and excess fields. missing_source.csv is deliberately absent. Run seed_decoding_fixture.py before testing decoding_failure.csv; that script is fixture setup, not learner code. Test a parser-reported csv.Error with an injected DictReader that raises csv.Error: ordinary short/long rows do not imply parser errors.\n'),('seed_decoding_fixture.py','from pathlib import Path\n# Fixture setup only: deliberately invalid UTF-8 content.\nPath("decoding_failure.csv").write_bytes(bytes([255]))\n')]
    workspace(key,extra=extra)
workspace('file_modes','.existing', [('report.txt',report_text)])
# A minimal reusable table for the order record; every cell is extracted from the taught constructor.
assets.insert(0,{'asset_id':'ds.orders','asset_kind':'dataset','scenario_id':scenario,'title':'Illustrative order record','provenance':'authored','description':'Authored fictional record matching the glossary constructor and valid CSV example. Malformed CSV row-shape fixtures are in the file-and-format-errors workspace, not represented as ragged table rows.','columns':[{'name':'label','type':'string','semantic_role':'categorical','description':'Item label, not a unique identifier.'},{'name':'quantity','type':'integer','semantic_role':'numerical','unit':'items','description':'Count of the labelled item.'}],'rows':[row]})
registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':scenario,'name':'Order report workshop','summary':'A fictional stationery workshop uses notebook orders and disposable report files to practise Python objects and file boundaries. Each exercise has an isolated workspace; names and example values follow the glossary.','domain':'Python order objects and report files','glossary_example_vocab':sorted(vocab)}],'assets':assets}
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
# Deterministic local mistakes-to-avoid audit.
assert len(starters)==len(g['bundles'])
assert len({a['asset_id'] for a in assets})==len(assets)
for a in assets:
    if a['asset_kind']=='dataset':
        assert all(len(r)==len(a['columns']) for r in a['rows'])
        for c in a['columns']:
            assert c['type']!='integer' or c['semantic_role']=='numerical'
        assert not a.get('variants') # No find_issues anchor exists in this scope.
    if a['asset_kind']=='code_workspace':
        for f in a['files']:
            if f['path'].endswith('.py'):ast.parse(f['content'])
assert all(b['practice_anchor']['type']=='live_code' for b in g['bundles'])
assert not any(b['visual_anchor']['type'] in ('chart','data_table','spreadsheet') for b in g['bundles'])
print(json.dumps({'concepts':len(g['bundles']),'scenarios':len(registry['scenarios']),'assets':len(assets),'datasets':sum(a['asset_kind']=='dataset' for a in assets),'workspaces':sum(a['asset_kind']=='code_workspace' for a in assets),'vocabulary_terms':len(vocab),'asset_ids':[a['asset_id'] for a in assets]},indent=2))
