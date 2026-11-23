import ast, io, json, re, subprocess, sys, tokenize
from pathlib import Path
B = Path('batches/final_batch_learn_python.region.03')
g = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bs = {b['context']['concept_id'].split('.',1)[1]: b for b in g['bundles']}
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/learn_python.json').read_text())
sid = 'scenario.python_quantity_helpers'
# Mine the teaching examples and anchors, preserving their exact vocabulary.
vocab = []
def add(v):
    v = str(v)
    if v and v not in vocab: vocab.append(v)
examples = {}
for key,b in bs.items():
    text = '\n'.join(t['content'] for t in b['teaching_blocks'])
    text += '\n' + json.dumps(b['practice_anchor']) + '\n' + json.dumps(b['visual_anchor'])
    for code in re.findall(r'```python\n(.*?)```', text, re.S):
        examples[key] = code
        try:
            for token in tokenize.generate_tokens(io.StringIO(code).readline):
                if token.type in (tokenize.NAME, tokenize.NUMBER): add(token.string)
                elif token.type == tokenize.STRING:
                    try: add(ast.literal_eval(token.string))
                    except Exception: pass
        except tokenize.TokenError: pass
    for token in re.findall(r'\b(?:[A-Z][A-Za-z]*(?:Error|Exception|Exit|Interrupt)|[a-z]+_[a-z_]+)\b', text): add(token)
    for p in re.findall(r'(?:/[a-zA-Z_]+)+(?:/[a-zA-Z_.]+)?|\b[a-zA-Z_-]+\.(?:csv|txt)\b',text): add(p)
    for syntax in b['practice_anchor'].get('live_code',{}).get('allowed_syntax',[]):
        # Command/identifier vocabulary comes straight from the anchor.
        if '(' in syntax or ':' in syntax or syntax.startswith(('p ', 'b ', 'l ', 'n ', 's ', 'c ')):
            add(syntax)
for term in ('p quantity', 'l', 'n', 's', 'c', 'b line_number', 'pdb', 'breakpoint()'):
    if any(term in json.dumps(b['teaching_blocks']) for b in bs.values()): add(term)

# Retrieve glossary literal datasets rather than retyping records or expected values.
def literal_assignment(code, name):
    for node in ast.walk(ast.parse(code)):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError(name)
records = literal_assignment(examples['sorting_with_key_functions'], 'records')
intent = bs['sorting_with_key_functions']['practice_anchor']['live_code']['starter_state_intent']
practice_records = ast.literal_eval(re.search(r'records = (\[.*?\])',intent).group(1))
columns = list(records[0])
assets = [{
    'asset_id':'ds.orders', 'asset_kind':'dataset', 'scenario_id':sid,
    'title':'Order labels and quantities', 'provenance':'authored',
    'description':'Authored order records from the glossary quantity-key example. The case-label practice variant reproduces the separate lowercase-label example; it is not defective data. CSV name: orders.csv.',
    'columns':[{'name':c,'type':'integer' if isinstance(records[0][c],int) else 'string',
                'semantic_role':'numerical' if isinstance(records[0][c],int) else 'categorical',
                'description':'Quantity used as a comparison key.' if c=='quantity' else 'Color label used for grouping or text comparison; not a unique identifier.',
                'numeric_looking_label':False} for c in columns],
    'rows':[[r[c] for c in columns] for r in records],
    'variants':[{'variant_id':'case_labels','derived_from':'ds.orders',
       'purpose':'Exact lowercase-label sorting practice records, with equal normalized labels for stable-order checks.',
       'ops':[{'op':'set_cell','where':{'label':old['label']},'occurrence':0,'column':c,'value':new[c]}
              for old,new in zip(records,practice_records) for c in columns if old[c]!=new[c]],
       'planted_issues':[]}]
}]

starters = {}
starters['exception_propagation'] = examples['exception_propagation']
starters['finally_cleanup'] = '''def read_quantity(text):
    try:
        return int(text.read())
    finally:
        # TODO: release the supplied, already opened file without overriding its result.
        pass
'''
starters['functions_as_values'] = examples['functions_as_values'].replace('return operation(value)', 'pass  # TODO: invoke the supplied operation and return its result').replace('chosen = double','chosen = None  # TODO: store the function object, without calling it')
starters['closures_and_enclosing_scope'] = examples['closures_and_enclosing_scope'].replace('        nonlocal count\n        count = count + 1\n        return count','        pass  # TODO: rebind the enclosing count and return it').replace('    return advance','    return None  # TODO: return the nested function object')
starters['pathlib_paths'] = '''from pathlib import Path

# Chosen absolute POSIX base from the glossary; this exercise constructs paths only.
base = Path("/work/project")
output = None  # TODO: construct the relative orders.csv child beneath base.
print(output)
'''
# Use the glossary's initial implementation, which deliberately lacks validation.
starters['raising_exceptions'] = '''def cost(quantity):
    return quantity * 4
'''
starters['reading_tracebacks'] = '''def read_quantity(text):
    return int(text)

def outer(text):
    return read_quantity(text)

outer("three")
'''
starters['debugger_usage'] = '''# Intended behavior: a positive quantity returns "positive".
# The comparison below is deliberately wrong. Inspect it before correcting it.
def quantity_branch(quantity):
    breakpoint()
    if quantity < 0:
        return "positive"
    else:
        return "not positive"

quantity = 3
result = quantity_branch(quantity)
'''
starters['safe_mutable_defaults'] = '''def add_label(label, labels=[]):
    labels.append(label)
    return labels

print(add_label("blue"))
print(add_label("red"))
'''
starters['sorting_with_key_functions'] = 'records = ' + repr(practice_records) + '''

def label_key(record):
    pass  # TODO: return the lowercase label.

ordered = None  # TODO: produce a new sorted list using the named key.
'''
pairs = literal_assignment(examples['lambda_expressions'],'pairs')
starters['lambda_expressions'] = 'pairs = ' + repr(pairs) + '\nordered = None  # TODO: sorted with a single-expression lambda quantity key.\nprint(ordered)\n'
starters['specific_exception_handlers'] = '''try:
    raise FileNotFoundError("missing-example.txt")
except OSError:
    print("Other file operation failure")
except FileNotFoundError:
    print("File missing")
'''
starters['validation_vs_programming_errors'] = '''# Supplied report 1: ValueError from int("three"): unsuitable numeric text.
input_category = ""
input_response = ""

# Supplied report 2: NameError caused by a misspelled local quantity name.
implementation_category = ""
implementation_response = ""

# Supplied report 3: PermissionError opening an otherwise valid input path:
# inadequate access rights. No filesystem operation needs to run here.
access_category = ""
access_response = ""
'''
starters['variadic_arguments_and_unpacking'] = examples['variadic_arguments_and_unpacking'].replace('return target(*args, **kwargs)','pass  # TODO: forward both argument collections and return the result')

# Derive filesystem exercise fixtures from the actual conversion examples.
valid_text = next(n.value for n in ast.walk(ast.parse(examples['finally_cleanup'])) if isinstance(n,ast.Constant) and isinstance(n.value,str) and n.value.isdigit())
invalid_text = next(n.value for n in ast.walk(ast.parse(examples['exception_propagation'])) if isinstance(n,ast.Constant) and n.value == 'three')
for key,b in bs.items():
    if b['practice_anchor']['type'] != 'live_code' or b['context']['concept_id'] in profile['practice_type_by_concept']: continue
    files = [{'path':'main.py','content':starters[key]}]
    files.append({'path':'README.txt','content':b['practice_anchor']['objective']+'\n\n'+b['practice_anchor']['live_code']['starter_state_intent']+'\n\n'+b['practice_anchor']['success']+'\n'})
    if key == 'finally_cleanup':
        files.extend([{'path':'valid.txt','content':valid_text},{'path':'invalid.txt','content':invalid_text}])
        files.append({'path':'scaffold.py','content':'''# Instructor scaffolding, not learner syntax: supplies a manually opened file.
# Change the fixture to invalid.txt to observe failure after cleanup.
from main import read_quantity
text = open("valid.txt", "r")
try:
    result = read_quantity(text)
    print(result)
finally:
    print("closed:", text.closed)
'''})
    if key == 'debugger_usage':
        # A real read-only pdb session for a browser without an interactive terminal.
        source=B/'working/debugger_source.py'
        source.write_text(starters[key])
        tree=ast.parse(starters[key]); branch=next(n.lineno for n in ast.walk(tree) if isinstance(n,ast.If))
        commands='l\np quantity\np quantity < 0\nb '+str(branch)+'\nc\nn\nl\nc\n'
        run=subprocess.run([sys.executable,str(source)],input=commands,text=True,capture_output=True)
        files.extend([{'path':'debugger_session.txt','content':run.stdout+run.stderr},
                      {'path':'debugger_commands.txt','content':commands}])
        files[1]['content'] += '\nThe registered session is a real, read-only pdb transcript. Interactive stdin is unavailable in the browser; inspect the source and session rather than invoking breakpoint there. No terminal or external service is provisioned.\n'
    assets.append({'asset_id':'ws.'+key,'asset_kind':'code_workspace','scenario_id':sid,
                   'title':b['context']['concept_name']+' practice','runtime':'python','files':files})

registry = {'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],
 'batch_id':B.name,
 'scenarios':[{'scenario_id':sid,'name':'Small order-processing helper workshop',
 'summary':'A fictional project processes color-labelled order quantities and reviews its small Python helpers. Learners follow conversions and cleanup, pass and retain callable state, construct orders.csv paths without file operations, sort labels, and diagnose errors using the glossary examples.',
 'domain':'Python order-processing helpers','glossary_example_vocab':vocab}], 'assets':assets}
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
# Stage-specific mistakes checklist: exact row widths, unambiguous roles, source values,
# declared operations and occurrences, practice coverage, and no plot dependence.
assert len(registry['scenarios']) == 1
assert all(len(row)==len(columns) for row in assets[0]['rows'])
assert assets[0]['rows']==[[r[c] for c in columns] for r in records]
derived=[dict(r) for r in records]
for op in assets[0]['variants'][0]['ops']:
    matches=[r for r in derived if all(r[k]==v for k,v in op['where'].items())]
    matches[op['occurrence']][op['column']]=op['value']
assert derived==practice_records
assert len({a['asset_id'] for a in assets})==len(assets)
for key,b in bs.items():
    if b['practice_anchor']['type']=='live_code' and b['context']['concept_id'] not in profile['practice_type_by_concept']:
        assert 'ws.'+key in {a['asset_id'] for a in assets}
    assert b['practice_anchor']['type'] not in ('field_selection','data_cleanup')
    assert b['visual_anchor']['type'] not in ('chart','plot','data_table','spreadsheet')
for a in assets:
    if a['asset_kind']=='code_workspace':
        for f in a['files']:
            if f['path'].endswith('.py'): ast.parse(f['content'])
print(json.dumps({'scenarios':len(registry['scenarios']),'concepts':len(bs),'assets':len(assets),'datasets':1,'rows':len(records),'variants':1,'workspaces':len(assets)-1,'vocabulary_terms':len(vocab),'checklist':'PASS','asset_ids':[a['asset_id'] for a in assets]},indent=2))
