# Move verification-only helper code to grading expressions, not learner workspaces.
# This removes constructs unrelated to the lesson from the source syntax judgment.
def probe_helper(h, fn, *args):
    return "(lambda scope: (exec("+repr(h)+", scope), scope["+repr(fn)+"]("+", ".join(args)+"))[1])(globals())"
for c,marker,fn,var,checks in [
    ('assert_statement','# Supplied verification harness','check_contract','total = 10\nquantity = -1\n',[('total','quantity'),('total + 1','quantity')]),
    ('unittest_test_cases','# Supplied checker:','check_tests','multiplier = 4\n',[('multiplier',),('multiplier + 1',)]),
    ('unittest_setup_and_teardown','# Supplied checks:','check_lifecycle','mode = "normal"\n',[]),
    ('review_untrusted_input_and_execution','# Supplied fresh-run checker','check_parse','',[]),
]:
    starter,sol,prompt,tests=codes[c]
    cut=starter.index(marker);h=starter[cut:]
    starter=var+starter[:cut];sol=var+sol[:sol.index(marker)]
    if c=='unittest_setup_and_teardown':
        h=h.replace('if mode == "setup_failure":','if mode not in ("normal", "test_failure"):')
        expr='['+', '.join(probe_helper(h,fn,x) for x in ['mode',repr('test_failure'),repr('setup_failure')])+']'
        tests=[v(expr)]
    elif c=='review_untrusted_input_and_execution':
        # Grading-only harness no longer appears in the source being checked.
        expr='['+', '.join(probe_helper(h,fn,x) for x in ['text',repr('0'),repr('bad'),repr('-1')])+']'
        tests=[v(expr)]
    else:
        expr='['+', '.join(probe_helper(h,fn,*a) for a in checks)+']'
        tests=[v(expr)]
    prompt=prompt.replace('Leave the supplied checker unchanged','The grading checker').replace('Do not change the checker.','Only edit the lesson functions.').replace('Leave the supplied tests and lifecycle checker unchanged.','Leave the supplied tests unchanged.').replace('Leave the fresh-run checker unchanged.','The checker runs independent valid, malformed and negative inputs.')
    codes[c]=(starter,sol,prompt,tests)

# Real execution/report interpretation; the checker's source is not learner code.
s=assets['ws.unittest_execution_and_results']['files'][0]['content']
s='expected = 0\n'+s.replace('self.assertEqual(cost(0), 0)','self.assertEqual(cost(0), expected)')
h='''def run_review(expectation):
    import io, unittest
    global expected
    expected = expectation
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromTestCase(CostTests))
    notes = [line.lower() for line in open("main.py").read().splitlines() if line.startswith("# Review:")]
    noted = any(all(term in line for term in ["failure", "test_cost", "assertequal", "none"]) for line in notes)
    errors = [str(entry[1]).splitlines()[-1] for entry in result.failures]
    return [result.testsRun, len(result.failures), len(result.errors), errors, noted]
'''
sol=s+'\n# Review: failure, not error; test_cost; self.assertEqual(cost(0), expected); actual None does not equal expected 0.\n'
code('unittest_execution_and_results',s,sol,'Execute the supplied TestCase with the browser checker (the equivalent of python -m unittest test_cost; no shell). Keep the supplied helper and assertion unchanged. Add a comment beginning # Review: that identifies the reported test, the assertEqual line, the actual mismatch, and whether the reported outcome is a failure or an error. The checker grades both the executed report and your evidence note.',[v('['+probe_helper(h,'run_review','expected')+', '+probe_helper(h,'run_review','None')+']')])
# Trace annotation prompts ask for a judgment, not a verbatim answer from the prompt.
a,b,_,tests=codes['read_generated_code']
codes['read_generated_code']=(a,b,'Keep cost unchanged. Assign positive_return = cost(positive_quantity) and invalid_return = cost(invalid_quantity) to record actual returns. Add comments starting # Trace positive: and # Trace invalid:. For each, record the input binding, condition result, selected or skipped branch, actual return, and whether it is explicit or implicit. State any mismatch with the requirement that nonpositive quantity returns 0.',tests)
# Retain exact output contract but ask for review findings rather than telling the learner the findings.
a,b,_,tests=codes['review_generated_file_operations']
codes['review_generated_file_operations']=(a,b,'Never call cleanup_helper. Remove the unintended deletion while preserving the permitted disposable write and source rename. Assign rename_destination = Path(cwd) / "target.txt" to resolve the relative target without moving anything. Add comments starting # Review mode:, # Review output:, and # Review rename:. Explain the w-mode effect, whether the absolute child preserves the base, the actual output and rename destinations, and Unix existing-destination behavior. The checker reads source; it never executes the proposed filesystem changes.',tests)
# Compute quantities from the supplied workspace lists into scalar inputs so real input mutations are possible.
import ast
for c,(starter,sol,prompt,tests) in list(codes.items()):
    changes=[]
    for n in ast.parse(starter).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and isinstance(n.value,ast.List):
            try: vals=ast.literal_eval(n.value)
            except (ValueError,TypeError):continue
            if vals and all(isinstance(x,int) for x in vals):
                name=n.targets[0].id
                prefix=''.join(f'{name}_input_{i} = {x!r}\n' for i,x in enumerate(vals))
                old=starter.splitlines()[n.lineno-1]
                new=prefix+name+' = ['+', '.join(f'{name}_input_{i}' for i in range(len(vals)))+']'
                changes.append((old,new))
    for old,new in changes:
        starter=starter.replace(old,new,1);sol=sol.replace(old,new,1)
    if c=='generator_functions':tests=[v("[list(positive_quantities(values)), type(positive_quantities(values)).__name__ == 'generator']")]
    if c=='itertools_utilities':
        tests=[v("[total, __import__('ast').dump(__import__('ast').parse(open('main.py').read()).body[-1].value) == __import__('ast').dump(__import__('ast').parse('sum(chain(first, second))', mode='eval').body)]")]
    codes[c]=(starter,sol,prompt,tests)
# Pin machine-readable annotation forms without supplying the learner's judgments.
a,b,prompt,tests=codes['read_generated_code']
prompt+=' Use these comment templates, filling each bracketed field from the trace: "# Trace positive: binding quantity = <input>; condition <True/False>; <positive branch/branch skipped>; <explicit/implicit> return <actual>." and "# Trace invalid: binding quantity = <input>; condition <True/False>; <positive branch/branch skipped>; <explicit/implicit> return <actual>; required <required-return> is <met/unmet>."'
codes['read_generated_code']=(a,b,prompt,tests)
a,b,prompt,tests=codes['review_generated_file_operations']
prompt+=' Use these exact note forms with your chosen findings: "# Review mode: w <preserves/truncates> existing output content.", "# Review output: <absolute child replaces base/base retained>; <output-path>.", and "# Review rename: relative target uses <cwd/base>; <destination>; Unix <may replace/never replaces> an existing destination file."'
# Verify all preserved behavior by comparing the reviewed function's syntax tree with the reference, not merely its names.
ref=next(n for n in ast.parse(b).body if isinstance(n,ast.FunctionDef) and n.name=='cleanup_helper')
old_expr=tests[0][1]['expr']
new_expr=old_expr.replace('cleanup_helper.__code__.co_names', "__import__('ast').dump(next(n for n in __import__('ast').parse(open('main.py').read()).body if isinstance(n, __import__('ast').FunctionDef) and n.name == 'cleanup_helper')) == "+"__import__('ast').dump(__import__('ast').parse("+repr(ast.unparse(ref))+").body[0])")
codes['review_generated_file_operations']=(a,b,prompt,[v(new_expr)])
# Execution review: exact form keeps a wrong 'error' conclusion from satisfying loose keyword checks.
a,b,prompt,tests=codes['unittest_execution_and_results']
b=b.replace('# Review: failure, not error; test_cost;', '# Review: failure; test_cost;')
h='''def run_review(expectation):
    import io, unittest
    global expected
    expected = expectation
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromTestCase(CostTests))
    source = open("main.py").read()
    note = "# Review: failure; test_cost; self.assertEqual(cost(0), expected); actual None does not equal expected 0."
    noted = note in source
    errors = [str(entry[1]).splitlines()[-1] for entry in result.failures]
    return [result.testsRun, len(result.failures), len(result.errors), errors, noted]
'''
prompt+=' Use the exact evidence-note form "# Review: <failure/error>; <test-method>; <assertion-line>; actual <actual-value> does not equal expected <expected-value>." Fill each field from the executed report.'
codes['unittest_execution_and_results']=(a,b,prompt,[v('['+probe_helper(h,'run_review','expected')+', '+probe_helper(h,'run_review','None')+']')])
# Explicitly define named output placeholders in the starter; they cannot satisfy the solution tests.
for c,names in {'generator_expressions':['total'], 'itertools_utilities':['total'], 'map_and_filter':['stored'], 'read_generated_code':['positive_return','invalid_return'], 'review_generated_file_operations':['rename_destination']}.items():
    a,b,prompt,tests=codes[c]
    declarations=''.join(name+' = None\n' for name in names)
    codes[c]=(declarations+a,declarations+b,prompt,tests)
# Cover the complete traversal-repair practice, including repeated exhaustion evidence.
a,b,prompt,tests=codes['iterator_consumption_and_exhaustion']
a+='\ndef trace_exhaustion(values):\n    # TODO: return the consumed first item, remaining list, two defaulted exhaustion results, and iterator identity.\n    pass\n'
b+='''\ndef trace_exhaustion(values):
    traversal = iter(values)
    first = next(traversal)
    remaining = list(traversal)
    exhausted_once = next(traversal, None)
    exhausted_again = next(traversal, None)
    return first, remaining, exhausted_once, exhausted_again, iter(traversal) is traversal
'''
prompt+=' Also implement trace_exhaustion(values) for a nonempty finite list: consume its first item, materialize the remaining items, and call next(traversal, None) twice more. Return a tuple in this order: first item, remaining list, first defaulted exhaustion result, second defaulted exhaustion result, iter(traversal) is traversal.'
# Test input values come from the existing traversal test specifications.
newtests=list(tests)
for kind,spec in tests:
    if kind=='function_call':newtests.append(call('trace_exhaustion',*spec['args']))
codes['iterator_consumption_and_exhaustion']=(a,b,prompt,newtests)
# Show both a one-pass lazy total and stored values for repeated traversal.
a,b,prompt,tests=codes['eager_vs_lazy_processing']
a='reusable = None\n'+a
b='reusable = None\n'+b+'reusable = [value * 2 for value in values]\n'
prompt+=' For a separate requirement needing two complete passes over the transformed results, assign reusable to a materialized list of the doubled values. The checker traverses this stored list twice.'
expr=tests[0][1]['expr'].replace('body[-1]','body[-2]')
codes['eager_vs_lazy_processing']=(a,b,prompt,[v('['+expr+', reusable, sum(reusable), sum(reusable)]')])
