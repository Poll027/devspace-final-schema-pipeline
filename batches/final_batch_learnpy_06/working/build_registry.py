import json,re,keyword,io,contextlib,unittest
from pathlib import Path
root=Path('batches/final_batch_learn_python.region.06')
bundle=json.loads((root/'inputs/path_glossary_bundle.json').read_text())
profile=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/learn_python.json').read_text())
sid='scenario.python_quantity_review'
# Extract the glossary's literal example names and values, not a separate domain vocabulary.
vocab=set()
for b in bundle['bundles']:
    texts=[t['content'] for t in b['teaching_blocks']]+[json.dumps(b.get(k),ensure_ascii=False) for k in ('visual_anchor','practice_anchor')]
    for text in texts:
        for code in re.findall(r'```python\n(.*?)```',text,re.S):
            vocab.update(t for t in re.findall(r'[A-Za-z_]\w*',code) if not keyword.iskeyword(t))
        vocab.update(re.findall(r'\b\w+_\w+\b|(?<!\w)-?\d+(?!\w)',text))
        vocab.update(t for t in ['Python','assert','AssertionError','ValueError','StopIteration','iter','next','yield','sum','list','chain','map','filter','unittest','setUp','tearDown','addCleanup','Path','unlink','rename','eval','exec','int','float','json.loads','sorted','records','quantity','total','output','source','target','text','pip','--index-url','Python Package Index','-O'] if t in text)
scenarios=[dict(scenario_id=sid,name='Quantity helper review desk',summary='A fictional developer reviews small Python helpers for quantity batches, totals and cost, and supplied tests and generated-code proposals. File-operation proposals are read before execution; dependency and API checks are read-only reviews.',domain='Python quantity processing and code review',glossary_example_vocab=sorted(vocab))]
starters={
'assert_statement':'''def public_quantity(quantity):
    if quantity < 0:
        raise ValueError("negative quantity")
    return quantity

def internal_total(total):
    # TODO: assert the supplied invariant total == 10 with a message.
    return total
''',
'iterables_and_iterators':'values = [3, 2]\n# TODO: create first and second; request values and check iterator identity.\n',
'generator_functions':'values = [3, -1, 2]\n\ndef positive_quantities(values):\n    # TODO: loop, filter positive values and yield each accepted value.\n    pass\n',
'generator_expressions':'values = [3, -1, 2]\n# TODO: assign total using a generator expression directly inside sum.\n',
'iterator_consumption_and_exhaustion':'''values = [3, 2]

def two_passes(values):
    traversal = iter(values)
    first = list(traversal)
    second = list(iter(traversal))
    return first, second
# TODO: repair the second pass.
''',
'eager_vs_lazy_processing':'values = [3, 2]\nstored = sum([value * 2 for value in values])\n# TODO: rewrite the total without the intermediate list.\n',
'itertools_utilities':'first = [3, 2]\nsecond = [5, 4]\n# TODO: import chain and directly total its combined traversal.\n',
'map_and_filter':'''def positive(value):
    return value > 0

def double(value):
    return value * 2

values = [3, -1, 2]
lazy = map(double, filter(positive, values))
# TODO: write the equivalent comprehension and lazy generator expression.
''',
'unittest_test_cases':'''def cost(quantity):
    if quantity < 0:
        raise ValueError("negative quantity")
    return quantity * 4

# Supplied cases: cost(3) == 12; cost(3) > 0; cost(-1) raises ValueError.
# TODO: import unittest and implement CostTests with named test methods.
''',
'unittest_execution_and_results':'''import unittest

def cost(quantity):
    if quantity > 0:
        return quantity * 4

class CostTests(unittest.TestCase):
    def test_cost(self):
        self.assertEqual(cost(0), 0)

# Supplied named-module command: python -m unittest test_cost
# Browser equivalent: TextTestRunner executes this TestCase without a shell.
''',
'unittest_setup_and_teardown':'''import unittest

# Supplied in-memory resource only; no filesystem or host resource.
resource_events = []

def acquire():
    resource_events.append("acquire")

def release():
    resource_events.append("release")

class QuantityTests(unittest.TestCase):
    def setUp(self):
        acquire()
        # TODO: immediately register release (do not call it here).
        # TODO: give each test a fresh quantities list.

    def test_mutation(self):
        self.assertEqual(self.quantities, [3, 2])
        self.quantities[0] = 0

    def test_fresh_state(self):
        self.assertEqual(self.quantities, [3, 2])

# The downstream exercise supplies normal/test-failure/setup-failure checks.
''',
'read_generated_code':'''# Requirement: positive quantity returns quantity * 4; nonpositive returns 0.
def cost(quantity):
    if quantity > 0:
        return quantity * 4

print(cost(3))
print(cost(-1))
# TODO: annotate bindings, conditions, branches and actual returns; do not repair.
''',
'review_generated_file_operations':'''from pathlib import Path

# Fictional review state, not provisioned files:
# cwd: /project; /reports/output.txt already contains a disposable report.
# /project/target.txt exists. /project/preserve.txt must be preserved.
# Writing disposable output and moving source to /project/target.txt are permitted.
# Do NOT call this helper. Review its proposed effects and remove unintended deletion.
def cleanup_helper():
    output = Path("/project") / "/reports/output.txt"
    path = Path("/project/preserve.txt")
    source = Path("/project/source.txt")
    target = Path("target.txt")
    with open(output, "w") as file:
        file.write("report")
    path.unlink()
    source.rename(target)
    return output

# TODO: remove the unintended unlink and add mode/path/Unix replacement notes.
''',
'review_untrusted_input_and_execution':'''text = "3"
quantity = None
# Rejected, non-executable proposal: quantity = eval(text)
# Requirement: a nonnegative integer; malformed/negative text leaves quantity None.
# TODO: use int(text), catch ValueError, and validate quantity explicitly.
''',
'accept_repair_or_reject_generated_code':'''# Review-only implementations and evidence are in review.txt.
# Do not execute unsafe proposals. Record justified decisions as Python strings.
# TODO: assign a decision and justification for every supplied version.
'''
}
assets=[]
# Shared raw authored quantities. Preserve the exact named example sequences in workspaces.
assets.append(dict(asset_id='ds.quantity_batches',asset_kind='dataset',scenario_id=sid,title='Authored quantity batches',description='Small fictional numeric inputs; first and second match the chain example. Filtering inputs and invariant inputs remain separate example cases.',columns=[dict(name='batch',type='string',semantic_role='categorical',description='Named example case, not a measurement.'),dict(name='quantity',type='integer',semantic_role='numerical',description='Quantity supplied as numeric input to a helper.')],rows=[['first',3],['first',2],['second',5],['second',4],['filter',-1],['boundary',0],['invariant',10]],provenance='authored',variants=[]))
for b in bundle['bundles']:
    cid=b['context']['concept_id']; name=cid.split('.',1)[1]
    if cid in profile['practice_type_by_concept']: continue
    assert name in starters,cid
    files=[dict(path='test_cost.py' if name=='unittest_execution_and_results' else 'main.py',content=starters[name])]
    if name=='unittest_execution_and_results':
        ns={};exec(starters[name],ns)
        stream=io.StringIO();unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromTestCase(ns['CostTests']))
        # Timing is real runtime output, not an authored expected value.
        files.append(dict(path='runner_report.txt',content=stream.getvalue()))
        stream=io.StringIO();unittest.TextTestRunner(stream=stream).run(unittest.TestSuite())
        files.append(dict(path='zero_test_report.txt',content=stream.getvalue()))
    if name=='accept_repair_or_reject_generated_code':
        cases=[('supported','def cost(quantity):\n    return quantity * 4\n',3,12),('missing_return','def cost(quantity):\n    if quantity > 0:\n        return quantity * 4\n',0,0),('unexpected_exception','def cost(quantity):\n    raise ValueError("unexpected quantity")\n',3,12)]
        evidence=[]
        for label,code,value,expected in cases:
            ns={};exec(code,ns)
            try:
                actual=ns['cost'](value);result='passed' if actual==expected else 'failed assertion'
                trace=repr(actual)
            except Exception as e:trace=type(e).__name__+': '+str(e);result='unexpected exception'
            evidence.append(f'{label}\n{code}Supplied requirement: cost({value}) == {expected}\nTraced result: {trace}\nSupplied check: {result}\n')
        evidence.extend(['unsafe_input (read-only text, never executed):\ndef cost(text):\n    return eval(text)\nRequirement: do not evaluate untrusted text. Safety finding: evaluates untrusted input.','unsafe_file (read-only text, never executed):\ndef cost(output):\n    with open(output, "w") as file:\n        file.write("report")\nRequirement: preserve existing file content. Safety finding: proposed w mode truncates existing content.'])
        files.append(dict(path='review.txt',content='\n\n'.join(evidence)))
    assets.append(dict(asset_id='ws.'+name,asset_kind='code_workspace',scenario_id=sid,title=b['context']['concept_name'],runtime='python',files=files))
registry=dict(schema_version='1.0',kind='scenario_asset_registry',path_id=bundle['path_id'],batch_id=root.name,scenarios=scenarios,assets=assets)
(root/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2)+'\n')
# Stage-specific mistakes-to-avoid checks.
for a in assets:
    if a['asset_kind']=='dataset':
        assert all(len(r)==len(a['columns']) for r in a['rows'])
        for i,c in enumerate(a['columns']):
            assert c['semantic_role'] in {'numerical','categorical'}
            assert all(isinstance(r[i],int if c['type']=='integer' else str) for r in a['rows'])
    else:
        for f in a['files']:
            if f['path'].endswith('.py'):compile(f['content'],f['path'],'exec')
assert all(not any(a['asset_id']=='ws.'+c.split('.',1)[1] for a in assets) for c in profile['practice_type_by_concept'])
assert len(starters)==sum(b['context']['concept_id'] not in profile['practice_type_by_concept'] for b in bundle['bundles'])
assert not any((b.get('practice_anchor') or {}).get('type') in ('field_selection','data_cleanup') for b in bundle['bundles'])
assert not any((b.get('visual_anchor') or {}).get('type') in ('data_table','spreadsheet','chart') for b in bundle['bundles'])
print('Checklist passed:',len(bundle['bundles']),'concepts;',len(assets),'assets;',len(vocab),'vocabulary entries')
print('\n'.join(a['asset_id'] for a in assets))
