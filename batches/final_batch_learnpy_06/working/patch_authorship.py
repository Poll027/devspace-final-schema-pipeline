import json, copy, tempfile, os
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.06')
p=B/'interactions.json'; d=json.loads(p.read_text()); before=copy.deepcopy(d)
ix={x['step_id']:x['interaction'] for t in d['tiles'] for x in t['interactions']}
def get(tile,step): return ix[f'learn_python.tile.{tile}.{step}']
def put(i,starter,solution,prompt):
 i['public']['workspace']['files'][0]['content']=starter
 i['grading']['solution_files'][0]['content']=solution
 i['public']['prompt']=prompt
# Assertion: retain the public validation and the existing checker interfaces.
i=get('099_099','s03'); old=i['public']['workspace']['files'][0]['content']
prefix=old[:old.index('# Supplied scaffold')]
prefix=prefix.replace("invariant_message = 'internal total must equal 10'", 'invariant_message = "unexpected total"')
public=old[old.index('    def public_quantity'):old.index('    def internal_total')]
public='\n'.join(line[4:] if line.startswith('    ') else line for line in public.split('\n'))
s=prefix+'# Preserve public validation unchanged.\n'+public+'def internal_total(total):\n    # TODO: assert that total equals 10 with the message "unexpected total".\n    return total\n'
r=s.replace('    # TODO: assert that total equals 10 with the message "unexpected total".', '    assert total == 10, "unexpected total"')
put(i,s,r,'Add an assertion in internal_total that total equals 10, with the message "unexpected total". Keep the return and public_quantity validation unchanged. The checker verifies matching and mismatching totals, the assertion message, and negative-quantity rejection in normal and optimized execution.')
# Generator function: remove both completed helpers.
i=get('100_103','s06'); prefix=i['public']['workspace']['files'][0]['content'].split('# Supplied scaffold')[0]
s=prefix+'def positive_quantities(values):\n    # TODO: write the loop, positive-value condition, and yield statement.\n    ...\n'
r=prefix+'def positive_quantities(values):\n    for value in values:\n        if value > 0:\n            yield value\n'
put(i,s,r,'Implement positive_quantities(values): loop over values, accept values greater than zero, and yield each accepted value. Preserve the supplied inputs. Calling the function must create a generator iterator that supplies 3 then 2 for [3, -1, 2], omits -1, and ends after the finite input.')
# Direct filtered generator-expression aggregation.
i=get('100_103','s09');prefix=i['public']['workspace']['files'][0]['content'].split('# TODO')[0]
s=prefix+'# TODO: calculate total with a filtered generator expression directly inside sum.\ntotal = None\n'
r=prefix+'total = sum(value * 2 for value in values if value > 0)\n'
put(i,s,r,'Write total using a generator expression as the sole argument to sum: double only positive entries in values and aggregate without an intermediate collection. Preserve the supplied values. For [3, -1, 2], total must be 10.')
def direct_sum_test(i,var):
 i['grading']['tests'][0]['spec']['expr']=f"[{var}, any(isinstance(n, __import__('ast').Assign) and any(isinstance(t, __import__('ast').Name) and t.id == '{var}' for t in n.targets) and isinstance(n.value, __import__('ast').Call) and isinstance(n.value.func, __import__('ast').Name) and n.value.func.id == 'sum' and len(n.value.args) == 1 and isinstance(n.value.args[0], __import__('ast').GeneratorExp) for n in __import__('ast').walk(__import__('ast').parse(open('main.py').read())))]"
direct_sum_test(i,'total')
# Restore eager starter and direct lazy rewrite.
i=get('104_106','s04');prefix=i['public']['workspace']['files'][0]['content'].split('# Supplied lazy')[0]
s=prefix+'# TODO: rewrite this aggregation to avoid the intermediate doubled list.\nstored = sum([value * 2 for value in values])\n'
r=prefix+'stored = sum(value * 2 for value in values)\n'
put(i,s,r,'Rewrite the list-based stored assignment to pass a generator expression directly to sum, without materializing the doubled values. Preserve values. The rewritten stored must still be 10 for [3, 2].')
direct_sum_test(i,'stored')
# Remove equivalent comprehension solutions from the workspace.
i=get('104_106','s12');old=i['public']['workspace']['files'][0]['content'];prefix=old[:old.index('equivalent_stored')];prefix=prefix.removeprefix('stored = None\n')
s=prefix+'# TODO: write the equivalent list comprehension and generator expression.\nstored = None\nlazy = None\n'
r=prefix+'stored = [double(value) for value in values if positive(value)]\nlazy = (double(value) for value in values if positive(value))\n'
put(i,s,r,'Rewrite map(double, filter(positive, values)) as stored, a list comprehension, and lazy, a generator expression. Write both expressions using the supplied double(value) transformation and positive(value) predicate. Preserve helpers and inputs. stored and the consumed lazy must each produce [6, 4] for [3, -1, 2]; lazy must be a generator iterator.')
# Test authoring: supply only helper and behavior requirements.
i=get('107_109','s03');old=i['public']['workspace']['files'][0]['content'];prefix=old[:old.index('    # Supplied cases')]
s=prefix+'# Supplied cases: cost(3) == 12; cost(3) > 0; cost(-1) raises ValueError.\n# TODO: write the unittest import, CostTests class, and named test methods.\n'
r=s+'import unittest\n\nclass CostTests(unittest.TestCase):\n    def test_cost(self):\n        self.assertEqual(cost(3), 12)\n        self.assertTrue(cost(3) > 0)\n\n    def test_invalid_quantity(self):\n        with self.assertRaises(ValueError):\n            cost(-1)\n'
put(i,s,r,'Import unittest and write CostTests inheriting from unittest.TestCase. Write test_cost with assertEqual(cost(3), 12) and assertTrue(cost(3) > 0). Write test_invalid_quantity with cost(-1) inside the body of with self.assertRaises(ValueError). Preserve the supplied helper. The checker runs both methods against the helper and checks that changed behavior is detected.')
# Initialization and cleanup belong in learner-authored setUp.
i=get('107_109','s13');old=i['public']['workspace']['files'][0]['content'];prefix=old[:old.index('supplied_quantities')]
s=prefix.replace('            self.addCleanup(resource_cleanup)\n            self.quantities = list(quantity_inputs)', '            # TODO: immediately register release, then initialize fresh quantities [3, 2].')
r=prefix.replace('            self.addCleanup(resource_cleanup)\n            self.quantities = list(quantity_inputs)', '            self.addCleanup(release)\n            self.quantities = [3, 2]')
put(i,s,r,'Complete QuantityTests.setUp immediately after acquire(): register the supplied release callable with self.addCleanup(release), then assign a fresh self.quantities = [3, 2]. Preserve the supplied resource functions and tests. Checks cover normal completion, test failure, setup failure after registration, and distinct fresh lists across tests.')
# Parser: leave conversion, handling and validation to the learner.
i=get('110_112','s12');old=i['public']['workspace']['files'][0]['content'];prefix=old[:old.index('# TODO')]
s=prefix+'# TODO: convert text with int, handle ValueError, and reject negative quantities.\n'
r=prefix+'try:\n    quantity = int(text)\n    if quantity < 0:\n        quantity = None\nexcept ValueError:\n    quantity = None\n'
put(i,s,r,'Replace the commented eval-based proposal with safe parsing using int(text). Write the conversion, ValueError handling, and explicit nonnegative validation. Valid nonnegative integer text must set quantity to that integer; malformed or negative input must leave quantity as None without an uncaught error. Preserve text and keep the unsafe proposal non-executable. The checker uses fresh valid, zero, malformed and negative inputs and rejects eval, exec and shell invocation.')
# Recompute affected expected results by executing each solution and its unchanged/updated tests.
changed=[k for k in ix if ix[k]!=next(x['interaction'] for t in before['tiles'] for x in t['interactions'] if x['step_id']==k)]
with tempfile.TemporaryDirectory(dir=B/'working') as tmp:
 cwd=os.getcwd();os.chdir(tmp)
 try:
  for k in changed:
   i=ix[k];code=i['grading']['solution_files'][0]['content'];Path('main.py').write_text(code);scope={};exec(compile(code,'main.py','exec'),scope)
   for test in i['grading']['tests']:
    if test['kind']=='value_equals':test['spec']['expected']=eval(test['spec']['expr'],scope)
 finally:os.chdir(cwd)
assert len(changed)==8
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched',len(changed),'interactions; total',len(ix))
