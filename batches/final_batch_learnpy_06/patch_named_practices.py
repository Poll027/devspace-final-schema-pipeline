import json, textwrap, pathlib, os
B = pathlib.Path(__file__).resolve().parent
P = B / 'interactions.json'
d = json.loads(P.read_text())
ids = ['learn_python.tile.100_103.s09', 'learn_python.tile.104_106.s04', 'learn_python.tile.107_109.s03', 'learn_python.tile.107_109.s13', 'learn_python.tile.110_112.s12']
for tile in d['tiles']:
    for row in tile['interactions']:
        sid = row['step_id']
        if sid not in ids:
            continue
        ix = row['interaction']
        pub = ix['public']
        old = ix['grading']['solution_files'][0]['content']
        if sid == ids[0]:
            head = old.split('# TODO:')[0]
            starter = head + '# TODO: Assign total using a filtered generator expression directly inside sum.\n'
            solution = head + 'total = sum(value * supplied_factor for value in values if value > supplied_minimum)\n'
            pub['prompt'] = 'Using the supplied values and inputs unchanged, write the assignment to total. Filter entries strictly greater than supplied_minimum, multiply each accepted value by supplied_factor, and total them using a generator expression as the sole argument to sum. Do not construct an intermediate collection.'
        elif sid == ids[1]:
            head = old.split('# TODO:')[0]
            starter = head + 'stored = sum([value * supplied_factor for value in values])\n# TODO: Rewrite the assignment above to avoid the intermediate transformed list.\n'
            solution = head + 'stored = sum(value * supplied_factor for value in values)\n'
            pub['prompt'] = 'Rewrite the supplied eager assignment to stored as a one-pass lazy total. Keep values and supplied_factor unchanged, multiply every entry by supplied_factor, and pass a generator expression directly to sum instead of materializing the transformed list. Store the same total in stored.'
        elif sid == ids[2]:
            head = old.split('# TODO:')[0]
            behavior = '# Supplied cases: cost(3) equals supplied_expected_cost; cost(3) is positive; cost(-1) raises ValueError.\n'
            starter = head + behavior + '# TODO: Import unittest and write CostTests with test_cost and test_invalid_quantity.\n'
            body = textwrap.dedent(old.split('if True:\n', 2)[2])
            solution = head + behavior + 'import unittest\n\n' + body
            pub['prompt'] = 'Keep the supplied helper and inputs unchanged. Import unittest and implement CostTests as a unittest.TestCase subclass. In test_cost, use assertEqual to check cost(3) against supplied_expected_cost and assertTrue to check that cost(3) is positive. In test_invalid_quantity, use assertRaises to check ValueError, placing cost(-1) inside its with body. Do not add a test runner; the checker runs the methods and checks whether they detect changed helper behavior.'
        elif sid == ids[3]:
            head = old.split('    class QuantityTests')[0].replace('# Supplied resource and test scaffold; complete only the setUp TODO.', '# Supplied inputs and in-memory resource scaffold: leave unchanged.')
            cls = 'class QuantityTests' + old.split('    class QuantityTests', 1)[1].split('    # The downstream')[0]
            cls = 'class QuantityTests' + textwrap.dedent('    class QuantityTests' + old.split('    class QuantityTests', 1)[1].split('    # The downstream')[0]).split('class QuantityTests',1)[1]
            cls = cls.replace('self.addCleanup(cleanup)', 'self.addCleanup(release)').replace('list(initial_quantities)', '[quantity_input_0, quantity_input_1]')
            solution = head + cls
            starter = head + cls.replace('    def setUp(self):\n        acquire()\n        self.addCleanup(release)\n        self.quantities = [quantity_input_0, quantity_input_1]', '    def setUp(self):\n        acquire()\n        # TODO: Register cleanup immediately after acquisition.\n        # TODO: Initialize a fresh quantities list from the two supplied inputs.')
            # A syntactically valid unfinished setUp still acquires the resource but neither registers cleanup nor initializes state.
            pub['prompt'] = 'Complete QuantityTests.setUp after the supplied acquire() call. Register the supplied release callable immediately after acquisition, without calling it immediately, and initialize self.quantities to a fresh list containing quantity_input_0 and quantity_input_1 in that order. Keep the inputs, resource functions, and test methods unchanged. Each test must start with independent state, and release must run after normal completion, test failure, and setup failure occurring after cleanup registration.'
        else:
            head = old.split('# TODO:')[0]
            starter = head + '# TODO: Convert text without executing it; handle malformed text and reject negative quantities.\n'
            solution = head + 'try:\n    quantity = int(text)\n    if quantity < 0:\n        quantity = None\nexcept ValueError:\n    quantity = None\n'
            pub['prompt'] = 'Repair the commented eval-based proposal by implementing a non-executing quantity parser. Keep text unchanged. Convert numeric text with int(text), handle ValueError for malformed input, and explicitly reject negative quantities. Store a valid nonnegative integer in quantity; leave quantity as None for malformed or negative text. Keep the rejected proposal commented and never use eval, exec, or shell invocation.'
        pub['workspace']['files'][0]['content'] = starter
        ix['grading']['solution_files'][0]['content'] = solution
        # Execute the repaired solution and all existing checks: preserve answer keys and verify them against execution.
        work = B / 'working' / 'named_practice_verification'
        work.mkdir(parents=True, exist_ok=True)
        (work / 'main.py').write_text(solution)
        previous = pathlib.Path.cwd()
        os.chdir(work)
        try:
            scope = {}
            exec(compile(solution, 'main.py', 'exec'), scope)
            for test in ix['grading']['tests']:
                if test['kind'] == 'value_equals':
                    actual = eval(test['spec']['expr'], scope)
                    assert actual == test['spec']['expected'], (sid, actual, test['spec']['expected'])
        finally:
            os.chdir(previous)
        print('Verified', sid)
P.write_text(json.dumps(d, indent=2) + '\n')
print('Interactions:', sum(len(t['interactions']) for t in d['tiles']))
