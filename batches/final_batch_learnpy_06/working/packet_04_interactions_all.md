# EVALUATOR PACKET — Development checks with the Python assert statement (learn_python.tile.099_099)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.assert_statement — Development checks with the Python assert statement

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: learn_python.tile.099_099.s03/ix.learn_python.tile.099_099.s03: ADVISORY — syntax descriptors with no detector: ['<', '==', 'assert condition, message', 'function parameters and calls', 'generator expressions', 'integer literals', 'string literals', 'yield', 'yield from']

## SOURCE FACTS — A (python.assert_statement)   objective: Use assert to express development-only invariants.
A.f1: assert condition, message raises AssertionError when the condition is false in normal debugging execution.   [sources: python_language_reference#simple_stmts.html#assert]
A.f2: Python can omit assert statements when optimization is requested with -O, so an assertion must not replace input checks required in production.   [sources: python_language_reference#simple_stmts.html#assert]
A.f3: Use an explicit conditional and raise for required runtime validation rather than relying on a removable debugging assertion.   [sources: python_tutorial#errors.html#raising-exceptions]
note: Begin with this objective: Use assert to express development-only invariants.
note: Keep the example in the Python assertions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.iterables_and_iterators, python.generator_functions, python.generator_expressions.
PRACTICE ANCHOR (live_code): Add an assertion that an internal helper's total equals 10, while preserving the public function's explicit rejection of negative quantity.  SUCCESS: The helper checks total with an assertion and an explanatory message. The public function retains its if quantity < 0 branch and raises ValueError independently of the assertion.
ASSESSMENT ANCHOR: distinguish_internal_invariant_assertions_from_required_runtime_validation facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Generator expressions; Generator functions with yield; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Reading and explaining generated Python; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Development checks with the Python assert statement
Understand — 
(mechanism) In normal debugging execution, `assert condition, message` raises AssertionError if the condition is false. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Python can omit assertions with `-O`; they must not replace required production input checks. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(mechanism) For required runtime validation, use an explicit conditional and `raise`, not a removable assertion. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(example) For a supplied expected total, `assert total == 10, "unexpected total"` raises AssertionError when false in normal debugging execution. If nonnegative quantity is a required runtime contract, use an explicit `if quantity < 0:` branch followed by raise ValueError(...) instead. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Contrast an internal invariant with a required public input check: optimization must not remove the latter. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

### s02 · check · Check: Development checks with the Python assert statement
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, intro, grading=client] A public function must reject negative quantity in production, including runs with -O. Which design meets this requirement and still checks an internal total during debugging?
  ✔ o1: Keep if quantity < 0: raise ValueError(...) in the public function; use assert total == 10, message inside the helper.
      why: assert condition, message raises AssertionError when the condition is false in normal debugging execution. Python can omit assert statements when optimization is requested with -O, so an assertion must not replace input checks required in production. Use an explicit conditional and raise for required runtime validation rather than relying on a removable debugging assertion.
  ✘ o2: Replace public validation with assert quantity >= 0.
      why: Optimization can omit assert, so this would remove a required production check.
  ✘ o3: Use only an internal assert total == 10; it also validates every public input.
      why: The total invariant does not replace the public negative-quantity validation, and assert can be omitted.
  feedback✔: assert condition, message raises AssertionError when the condition is false in normal debugging execution. Python can omit assert statements when optimization is requested with -O, so an assertion must not replace input checks required in production. Use an explicit conditional and raise for required runtime validation rather than relying on a removable debugging assertion.  feedback✘: Recheck the evidence against the stated requirement. assert condition, message raises AssertionError when the condition is false in normal debugging execution. Python can omit assert statements when optimization is requested with -O, so an assertion must not replace input checks required in production. Use an explicit conditional and raise for required runtime validation rather than relying on a removable debugging assertion.  hints: ['Separate checks that must always run from checks used only during debugging.']  remediation→r01
  MEASURES: A:distinguish_internal_invariant_assertions_from_required_runtime_validation(f1,f2,f3)   anchors=['assessment:distinguish_internal_invariant_assertions_from_required_runtime_validation']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s03 · hands_on · Practice: Development checks with the Python assert statement
Practice — Add an assertion that an internal helper's total equals 10, while preserving the public function's explicit rejection of negative quantity.
QUESTION [code_exercise, core, grading=client] The supplied helpers preserve public_quantity and its explicit ValueError rejection even with assertions omitted. internal_total already contains the supplied assertion and message. Change only invariant_check to select the supplied predicate that checks equality with invariant_total: the internal assertion must check equality with invariant_total, not whether total is nonzero. Preserve all supplied constants and helpers. The checker verifies matching and mismatching totals and normal/optimized public rejection.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def', 'function parameters and calls', 'return', 'variable assignment', 'integer literals', 'string literals', '==', '<', 'if', 'raise ValueError(...)', 'assert condition, message'] blocked=9 items
  file main.py [editable]:
invariant_total = 10
invariant_message = 'internal total must equal 10'
minimum_quantity = 0
quantity_message = 'negative quantity'
total = 10
quantity = -1
# Supplied scaffold: preserve this block unchanged.
if True:
    def exact_total(total):
        return total == invariant_total

    def truthy_total(total):
        return bool(total)

    def public_quantity(quantity):
        if quantity < minimum_quantity:
            raise ValueError(quantity_message)
        return quantity

    def internal_total(total):
        assert invariant_check(total), invariant_message
        return total

# TODO: select the predicate that checks the invariant, not mere truthiness.
invariant_check = truthy_total

  SOLUTION main.py:
invariant_total = 10
invariant_message = 'internal total must equal 10'
minimum_quantity = 0
quantity_message = 'negative quantity'
total = 10
quantity = -1
# Supplied scaffold: preserve this block unchanged.
if True:
    def exact_total(total):
        return total == invariant_total

    def truthy_total(total):
        return bool(total)

    def public_quantity(quantity):
        if quantity < minimum_quantity:
            raise ValueError(quantity_message)
        return quantity

    def internal_total(total):
        assert invariant_check(total), invariant_message
        return total

# Select exact equality rather than mere truthiness.
invariant_check = exact_total

  test test1 (value_equals, visible=True): {"expr":"[(lambda scope: (exec('# Supplied verification harness; leave unchanged.\\ndef check_contract(total, quantity):\\n    try:\\n        helper = internal_total(total)\\n    except AssertionError as exc:\\n        helper = [\"AssertionError\", str(exc)]\\n    try:\\n        public = public_quantity(quantity)\\n    except ValueError as exc:\\n        public = [\"ValueError\", str(exc)]\\n    import ast\\n    tree = ast.parse(open(\"main.py\").read())\\n    node = next(n for n in ast.walk(tre | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"49a5d1164f9262470fd0a3779f09c62081d1491c4a322a6ca74a390892a4fc96","tests_passed":1}
  feedback✔: assert condition, message raises AssertionError when the condition is false in normal debugging execution. Python can omit assert statements when optimization is requested with -O, so an assertion must not replace input checks required in production. Use an explicit conditional and raise for required runtime validation rather than relying on a removable debugging assertion.  feedback✘: Recheck the evidence against the stated requirement. assert condition, message raises AssertionError when the condition is false in normal debugging execution. Python can omit assert statements when optimization is requested with -O, so an assertion must not replace input checks required in production. Use an explicit conditional and raise for required runtime validation rather than relying on a removable debugging assertion.  hints: ['Separate checks that must always run from checks used only during debugging.']
  MEASURES: A:distinguish_internal_invariant_assertions_from_required_runtime_validation(f1,f2,f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · recap · Takeaways
Keep these distinctions — 
(takeaway) Assertions are removable debugging checks; required input validation needs a conditional and raise. ⟦A.f2 A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Iterables and iterators: Distinguish iterables from iterators.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Development checks with the Python assert statement
(mechanism) In normal debugging execution, `assert condition, message` raises AssertionError if the condition is false. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Python can omit assertions with `-O`; they must not replace required production input checks. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(mechanism) For required runtime validation, use an explicit conditional and `raise`, not a removable assertion. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an internal invariant with a required public input check: optimization must not remove the latter. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expr: [(lambda scope: (exec('# Supplied verification harness; leave unchanged.\ndef check_contract(total, quantity):\n    try:\n        helper = internal_total(total)\n    except AssertionError as exc:\n        helper = ["AssertionError", str(exc)]\n    try:\n        public = public_quantity(quantity)\n    except ValueError as exc:\n        public = ["ValueError", str(exc)]\n    import ast\n    tree = ast.parse(open("main.py").read())\n    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "public_quantity")\n    optimized = {"minimum_quantity": minimum_quantity, "quantity_message": quantity_message}\n    exec(compile(ast.Module(body=[node], type_ignores=[]), "public", "exec", optimize=1), optimized)\n    try:\n        opt = optimized["public_quantity"](quantity)\n    except ValueError as exc:\n        opt = ["ValueError", str(exc)]\n    return [helper, public, opt]\n', scope), scope['check_contract'](total, quantity))[1])(globals()), (lambda scope: (exec('# Supplied verification harness; leave unchanged.\ndef check_contract(total, quantity):\n    try:\n        helper = internal_total(total)\n    except AssertionError as exc:\n        helper = ["AssertionError", str(exc)]\n    try:\n        public = public_quantity(quantity)\n    except ValueError as exc:\n        public = ["ValueError", str(exc)]\n    import ast\n    tree = ast.parse(open("main.py").read())\n    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "public_quantity")\n    optimized = {"minimum_quantity": minimum_quantity, "quantity_message": quantity_message}\n    exec(compile(ast.Module(body=[node], type_ignores=[]), "public", "exec", optimize=1), optimized)\n    try:\n        opt = optimized["public_quantity"](quantity)\n    except ValueError as exc:\n        opt = ["ValueError", str(exc)]\n    return [helper, public, opt]\n', scope), scope['check_contract'](total + 1, quantity))[1])(globals())]
· ops.value: internal total must equal 10_x
· expected.value: internal total must equal 10_x

=========

# EVALUATOR PACKET — Iterables and iterators / Generator functions with yield / Generator expressions / Iterator consumption and exhaustion (learn_python.tile.100_103)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.iterables_and_iterators — Iterables and iterators
B = python.generator_functions — Generator functions with yield
C = python.generator_expressions — Generator expressions
D = python.iterator_consumption_and_exhaustion — Iterator consumption and exhaustion

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=8
  warn: remediation step learn_python.tile.100_103.r02 is never referenced
  warn: remediation step learn_python.tile.100_103.r05 is never referenced
  warn: remediation step learn_python.tile.100_103.r07 is never referenced
  warn: remediation step learn_python.tile.100_103.r08 is never referenced
  warn: learn_python.tile.100_103.s03/ix.learn_python.tile.100_103.s03: ADVISORY — syntax descriptors with no detector: ['None', 'generator expressions', 'integer literals', 'is', 'itertools.*', 'list literals', 'unittest.*', 'yield', 'yield from']
  warn: learn_python.tile.100_103.s06/ix.learn_python.tile.100_103.s06: ADVISORY — syntax descriptors with no detector: ['function calls', 'generator expressions', 'if value > 0:', 'indented blocks', 'integer literals', 'itertools calls', 'list literals', 'unittest test classes and assertions', 'yield from', 'yield value']
  warn: learn_python.tile.100_103.s09/ix.learn_python.tile.100_103.s09: ADVISORY — syntax descriptors with no detector: ['(expression for item in iterable if condition)', '(expression for item in iterable)', 'comparison with >', 'integer literals', 'itertools utility calls', 'list literals', 'multiplication with *', 'unittest test classes and assertions', 'variable references']
  warn: learn_python.tile.100_103.s13/ix.learn_python.tile.100_103.s13: ADVISORY — syntax descriptors with no detector: ['except StopIteration', 'from itertools import ...', 'from unittest import ...', 'function parameters and calls', 'integer literals', 'is', 'list literals', 'try', 'tuple construction']

## SOURCE FACTS — A (python.iterables_and_iterators)   objective: Distinguish iterables from iterators.
A.f1: An iterable supplies an iterator via iter(value); an iterator supplies successive values via next(iterator) and signals exhaustion with StopIteration.   [sources: python_tutorial#classes.html#iterators]
A.f2: Separate iter(list_value) calls produce separate traversal state, while the list stores the reusable items.   [sources: python_tutorial#classes.html#iterators]
A.f3: Calling iter on an iterator returns that same iterator rather than a new independent traversal.   [sources: python_stdlib_reference#stdtypes.html#iterator.__iter__]
A.f4: next(iterator, default) returns default when the iterator is exhausted instead of raising StopIteration.   [sources: python_stdlib_reference#functions.html#next]
note: Begin with this objective: Distinguish iterables from iterators.
note: Keep the example in the Iterators, generators and exhaustion tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.generator_functions, python.generator_expressions, python.iterator_consumption_and_exhaustion.
PRACTICE ANCHOR (live_code): Obtain two independent iterators from values = [3, 2] and request their values explicitly with next.  SUCCESS: Advancing first twice returns 3 and 2, while the first request from second still returns 3. A further request from first with None as the default returns None, and iter(first) is first evaluates to True.
ASSESSMENT ANCHOR: use_iter_and_next_and_identify_stop_iteration facts=['f1']
ASSESSMENT ANCHOR: predict_independent_state_from_separate_list_iterators facts=['f2']
ASSESSMENT ANCHOR: predict_same_iterator_from_iter_on_iterator facts=['f3']
ASSESSMENT ANCHOR: predict_default_value_after_iterator_exhaustion facts=['f4']

## SOURCE FACTS — B (python.generator_functions)   objective: Produce lazy values with yield.
B.f1: A function containing yield creates a generator iterator when called; advancing it runs until the next yield.   [sources: python_tutorial#classes.html#generators]
B.f2: yield value supplies one item and suspends execution, retaining local state until the next advance.   [sources: python_tutorial#classes.html#generators]
B.f3: Write a for loop and a condition inside a generator function, yielding each accepted item; reaching the function’s end terminates iteration.   [sources: python_tutorial#classes.html#generators]
note: Begin with this objective: Produce lazy values with yield.
note: Keep the example in the Iterators, generators and exhaustion tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.generator_expressions, python.iterator_consumption_and_exhaustion, python.eager_vs_lazy_processing.
PRACTICE ANCHOR (live_code): Write positive_quantities(values) to yield each valid quantity, defined as a value greater than zero, one at a time from the input iterable.  SUCCESS: For values [3, -1, 2], the function supplies 3 followed by 2, omits -1, and reaches its end after processing the input.
ASSESSMENT ANCHOR: write_generator_that_yields_required_sequence_and_terminates facts=['f1', 'f2', 'f3']

## SOURCE FACTS — C (python.generator_expressions)   objective: Write generator expressions for lazy transformations.
C.f1: (expression for item in iterable if condition) defines a generator that transforms accepted items lazily; the filtering if clause is optional.   [sources: python_language_reference#expressions.html#generator-expressions]
C.f2: The leftmost iterable expression is evaluated immediately, while item transformations and filtering happen during iteration.   [sources: python_language_reference#expressions.html#generator-expressions]
C.f3: Pass a generator expression as the sole argument to sum to total transformed values without creating an intermediate list.   [sources: python_tutorial#classes.html#generator-expressions]
note: Begin with this objective: Write generator expressions for lazy transformations.
note: Keep the example in the Iterators, generators and exhaustion tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.iterator_consumption_and_exhaustion, python.eager_vs_lazy_processing, python.itertools_utilities.
PRACTICE ANCHOR (live_code): Use a generator expression as the sole argument to sum to double and total the positive entries in values.  SUCCESS: With values = [3, -1, 2], total is 10, calculated by filtering positive entries and doubling them without constructing an intermediate collection.
ASSESSMENT ANCHOR: transform_and_filter_without_intermediate_collection facts=['f1', 'f3']
ASSESSMENT ANCHOR: distinguish_immediate_iterable_evaluation_from_deferred_item_processing facts=['f2']

## SOURCE FACTS — D (python.iterator_consumption_and_exhaustion)   objective: Account for iterator consumption and exhaustion.
D.f1: Each next(iterator) consumes the next available item; a traversal or consumer sees only the remaining items.   [sources: python_stdlib_reference#functions.html#next]
D.f2: Once an iterator raises StopIteration, it must continue to do so on subsequent calls.   [sources: python_stdlib_reference#stdtypes.html#iterator.__next__]
D.f3: iter(iterator) returns the same iterator and does not reset it.   [sources: python_stdlib_reference#stdtypes.html#iterator.__iter__]
D.f4: For another pass over a reusable collection, obtain a fresh iterator from that collection rather than reusing its exhausted iterator.   [sources: python_tutorial#classes.html#iterators]
note: Begin with this objective: Account for iterator consumption and exhaustion.
note: Keep the example in the Iterators, generators and exhaustion tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.eager_vs_lazy_processing, python.itertools_utilities, python.map_and_filter.
PRACTICE ANCHOR (live_code): Fix a helper that attempts two complete passes over values but reuses an exhausted traversal for the second pass.  SUCCESS: For values = [3, 2], the helper returns two lists containing [3, 2] by obtaining a fresh iterator from values for the second pass.
ASSESSMENT ANCHOR: predict_remaining_items_after_partial_consumption facts=['f1']
ASSESSMENT ANCHOR: predict_repeated_next_calls_after_exhaustion facts=['f2']
ASSESSMENT ANCHOR: predict_iterator_state_after_iter_call facts=['f3']
ASSESSMENT ANCHOR: predict_results_from_a_fresh_collection_iterator facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Generator expressions; Generator functions with yield; Iterator consumption and exhaustion; Managing unittest setup and teardown; Reading and explaining generated Python; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Iterables and iterators
Understand — 
(mechanism) An iterable supplies an iterator through `iter(value)`. An iterator supplies successive items through `next(iterator)` and signals exhaustion with StopIteration. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Separate `iter(list_value)` calls have separate traversal state; the list stores reusable items. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Calling `iter` on an iterator returns that same iterator, not an independent traversal. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) At exhaustion, `next(iterator, default)` returns the default instead of raising StopIteration. ⟦A.f4 A:tb3 A:tb4⟧
[CODE python]
values = [3, 2]
first = iter(values)
second = iter(values)
print(next(first))
print(next(first))
print(next(first, None))
print(next(second))
print(iter(first) is first)
  annotations: ['Separate state from second.', 'Independent list traversal.', 'Same iterator; no reset.']

### s02 · check · Check: Iterables and iterators
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, intro, grading=client] After first = iter([3, 2]) and two next(first) calls, what does next(first, None) do?
  ✔ o1: Returns None.
      why: next(iterator, default) returns default when the iterator is exhausted instead of raising StopIteration.
  ✘ o2: Raises StopIteration.
      why: The supplied default is returned on exhaustion rather than raising StopIteration.
  ✘ o3: Returns 3 by restarting first.
      why: An exhausted iterator does not restart; the default applies.
  feedback✔: next(iterator, default) returns default when the iterator is exhausted instead of raising StopIteration.  feedback✘: Recheck the evidence against the stated requirement. next(iterator, default) returns default when the iterator is exhausted instead of raising StopIteration.  hints: ['Track each traversal position separately and notice whether a default was supplied.']  remediation→r01
  MEASURES: A:predict_default_value_after_iterator_exhaustion(f4)   anchors=['assessment:predict_default_value_after_iterator_exhaustion']
  taught-before-tested: A.f4←s01

### s03 · hands_on · Practice: Iterables and iterators
Practice — Obtain two independent iterators from values = [3, 2] and request their values explicitly with next.
QUESTION [code_exercise, core, grading=client] Create independent first and second iterators from values. Print, on five separate lines in order: the first two next(first) results, the first next(second) result, next(first, None), and iter(first) is first. Do not replace the supplied values. The final identity comparison is supplied and must remain unchanged; write the creation and next calls before that block.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'list literals', 'integer literals', 'None', 'iter(values)', 'iter(first)', 'next(first)', 'next(second)', 'next(first, None)', 'print()', 'is'] blocked=7 items
  file main.py [editable]:
values_input_0 = 3
values_input_1 = 2
values = [values_input_0, values_input_1]
first = None
second = None
# TODO: create first and second; request values and check iterator identity.
if first is not None:
    print(iter(first) is first)

  SOLUTION main.py:
values_input_0 = 3
values_input_1 = 2
values = [values_input_0, values_input_1]
first = None
second = None
# TODO: create first and second; request values and check iterator identity.
first = iter(values)
second = iter(values)
print(next(first))
print(next(first))
print(next(second))
print(next(first, None))
if first is not None:
    print(iter(first) is first)

  test test1 (stdout_equals, visible=True): {"expected":"3\n2\n3\nNone\nTrue\n"} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"cf89ff10711e9ee99783e4c2e9ed92b429b2133a914a8847a26387df6396cb24","tests_passed":1}
  feedback✔: An iterable supplies an iterator via iter(value); an iterator supplies successive values via next(iterator) and signals exhaustion with StopIteration. Separate iter(list_value) calls produce separate traversal state, while the list stores the reusable items. Calling iter on an iterator returns that same iterator rather than a new independent traversal. next(iterator, default) returns default when the iterator is exhausted instead of raising StopIteration.  feedback✘: Recheck the evidence against the stated requirement. An iterable supplies an iterator via iter(value); an iterator supplies successive values via next(iterator) and signals exhaustion with StopIteration. Separate iter(list_value) calls produce separate traversal state, while the list stores the reusable items. Calling iter on an iterator returns that same iterator rather than a new independent traversal. next(iterator, default) returns default when the iterator is exhausted instead of raising StopIteration.  hints: ['Track each traversal position separately and notice whether a default was supplied.']
  MEASURES: A:use_iter_and_next_and_identify_stop_iteration(f1); A:predict_independent_state_from_separate_list_iterators(f2); A:predict_same_iterator_from_iter_on_iterator(f3); A:predict_default_value_after_iterator_exhaustion(f4)   anchors=['practice', 'assessment:use_iter_and_next_and_identify_stop_iteration', 'assessment:predict_independent_state_from_separate_list_iterators', 'assessment:predict_same_iterator_from_iter_on_iterator', 'assessment:predict_default_value_after_iterator_exhaustion']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s04 · explainer · Generator functions with yield
Understand — 
(mechanism) Calling a function containing `yield` creates a generator iterator. Advancing it runs to the next yield. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) `yield value` supplies one item and suspends execution, retaining local state until the next advance. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
(mechanism) Inside the function, use a for loop and condition to yield accepted items. Reaching the function’s end terminates iteration. ⟦B.f3 B:tb3 B:tb4⟧
[CODE python]
def positive_quantities(values):
    for value in values:
        if value > 0:
            yield value

quantities = positive_quantities([3, -1, 2])
print(next(quantities))
print(next(quantities))
  annotations: ['Only accepted items reach yield.', 'Supply an item; suspend with local state retained.']

### s05 · check · Check: Generator functions with yield
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] Which body for positive_quantities(values) yields only positive values one at a time and finishes after the input ends?
  ✔ o1: for value in values:
    if value > 0:
        yield value
      why: A function containing yield creates a generator iterator when called; advancing it runs until the next yield. yield value supplies one item and suspends execution, retaining local state until the next advance. Write a for loop and a condition inside a generator function, yielding each accepted item; reaching the function’s end terminates iteration.
  ✘ o2: for value in values:
    yield value
      why: There is no acceptance condition, so negative values are yielded too.
  ✘ o3: for value in values:
    if value > 0:
        return value
      why: return ends the function rather than suspending to supply successive values with yield.
  feedback✔: A function containing yield creates a generator iterator when called; advancing it runs until the next yield. yield value supplies one item and suspends execution, retaining local state until the next advance. Write a for loop and a condition inside a generator function, yielding each accepted item; reaching the function’s end terminates iteration.  feedback✘: Recheck the evidence against the stated requirement. A function containing yield creates a generator iterator when called; advancing it runs until the next yield. yield value supplies one item and suspends execution, retaining local state until the next advance. Write a for loop and a condition inside a generator function, yielding each accepted item; reaching the function’s end terminates iteration.  hints: ['Follow what happens at a yield and when the loop reaches the end of its input.']  remediation→r03
  MEASURES: B:write_generator_that_yields_required_sequence_and_terminates(f1,f2,f3)   anchors=['assessment:write_generator_that_yields_required_sequence_and_terminates']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s06 · hands_on · Practice: Generator functions with yield
Practice — Write positive_quantities(values) to yield each valid quantity, defined as a value greater than zero, one at a time from the input iterable.
QUESTION [code_exercise, core, grading=client] Choose the supplied generator helper that yields each quantity greater than zero, one at a time. Complete the positive_quantities binding by choosing the helper that yields only values greater than zero, one at a time, omits negative values, and ends after the finite input. Do not edit the supplied helper block. The checker requires a generator iterator yielding 3 then 2 for values [3, -1, 2].
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def positive_quantities(values):', 'for value in values:', 'if value > 0:', 'yield value', 'variable assignment', 'function calls', 'list literals', 'integer literals', 'next()', 'print()', 'indented blocks'] blocked=6 items
  file main.py [editable]:
values_input_0 = 3
values_input_1 = -1
values_input_2 = 2
values = [values_input_0, values_input_1, values_input_2]

# Supplied scaffold: preserve this block unchanged.
if True:
    def supplied_positive_quantities(values):
        for value in values:
            if value > 0:
                yield value

    def all_quantities(values):
        for value in values:
            yield value

# TODO: bind positive_quantities to the helper that yields only positive values.
positive_quantities = all_quantities

  SOLUTION main.py:
values_input_0 = 3
values_input_1 = -1
values_input_2 = 2
values = [values_input_0, values_input_1, values_input_2]

# Supplied scaffold: preserve this block unchanged.
if True:
    def supplied_positive_quantities(values):
        for value in values:
            if value > 0:
                yield value

    def all_quantities(values):
        for value in values:
            yield value

# TODO: bind positive_quantities to the helper that yields only positive values.
positive_quantities = supplied_positive_quantities

  test test1 (value_equals, visible=True): {"expr":"[list(positive_quantities(values)), type(positive_quantities(values)).__name__ == 'generator']","expected":[[3,2],true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"40b75de8247090c77d88c39e1bd6bfc44cd0426e706fe517d0857b06a134e4e1","tests_passed":1}
  feedback✔: A function containing yield creates a generator iterator when called; advancing it runs until the next yield. yield value supplies one item and suspends execution, retaining local state until the next advance. Write a for loop and a condition inside a generator function, yielding each accepted item; reaching the function’s end terminates iteration.  feedback✘: Recheck the evidence against the stated requirement. A function containing yield creates a generator iterator when called; advancing it runs until the next yield. yield value supplies one item and suspends execution, retaining local state until the next advance. Write a for loop and a condition inside a generator function, yielding each accepted item; reaching the function’s end terminates iteration.  hints: ['Follow what happens at a yield and when the loop reaches the end of its input.']
  MEASURES: B:write_generator_that_yields_required_sequence_and_terminates(f1,f2,f3)   anchors=['practice']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s07 · explainer · Generator expressions
Understand — 
(mechanism) `(expression for item in iterable if condition)` lazily transforms accepted items. The filtering if clause is optional. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(mechanism) The leftmost iterable expression is evaluated immediately; filtering and item transformations happen during iteration. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(mechanism) As the sole argument to `sum`, a generator expression totals transformed values without an intermediate list. ⟦C.f3 C:tb1 C:tb3 C:tb4⟧
[CODE python]
values = [3, -1, 2]
total = sum(value * 2 for value in values if value > 0)
print(total)
  annotations: ['Evaluate the leftmost source now; filter and transform as consumed.']

### s08 · check · Check: Generator expressions
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] In (value * 2 for value in values if value > 0), which work happens immediately at creation, rather than during advances?
  ✔ o1: Evaluation of the leftmost iterable expression, values.
      why: The leftmost iterable expression is evaluated immediately, while item transformations and filtering happen during iteration.
  ✘ o2: All doubling and filtering of the items.
      why: Item transformations and filtering are deferred until iteration.
  ✘ o3: Nothing at all, including evaluation of values.
      why: The leftmost iterable expression is evaluated immediately.
  feedback✔: The leftmost iterable expression is evaluated immediately, while item transformations and filtering happen during iteration.  feedback✘: Recheck the evidence against the stated requirement. The leftmost iterable expression is evaluated immediately, while item transformations and filtering happen during iteration.  hints: ['Distinguish obtaining the source iterable from processing each item.']  remediation→r04
  MEASURES: C:distinguish_immediate_iterable_evaluation_from_deferred_item_processing(f2)   anchors=['assessment:distinguish_immediate_iterable_evaluation_from_deferred_item_processing']
  taught-before-tested: C.f2←s07

### s09 · hands_on · Practice: Generator expressions
Practice — Use a generator expression as the sole argument to sum to double and total the positive entries in values.
QUESTION [code_exercise, core, grading=client] The supplied doubled_positives generator expression filters positive values and doubles them without an intermediate collection. Assign total by passing that lazy stream directly to sum. Do not materialize a list or edit the supplied expression. With values [3, -1, 2], total must be 10.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'integer literals', 'list literals', 'variable references', 'multiplication with *', 'comparison with >', '(expression for item in iterable if condition)', '(expression for item in iterable)', 'sum(expression for item in iterable if condition)', 'print(total)'] blocked=4 items
  file main.py [editable]:
values_input_0 = 3
values_input_1 = -1
values_input_2 = 2
values = [values_input_0, values_input_1, values_input_2]
# TODO: assign total by passing the supplied lazy stream directly to sum.
# Supplied lazy transformation; do not edit.
doubled_positives = (value * 2 for value in values if value > 0)
total = None
# TODO: total this lazy stream directly with sum.

  SOLUTION main.py:
total = None
values_input_0 = 3
values_input_1 = -1
values_input_2 = 2
values = [values_input_0, values_input_1, values_input_2]
# TODO: assign total using a generator expression directly inside sum.
# Supplied lazy transformation; do not edit.
doubled_positives = (value * 2 for value in values if value > 0)
total = None
# TODO: total this lazy stream directly with sum.
total = sum(doubled_positives)

  test test1 (value_equals, visible=True): {"expr":"[total, any(isinstance(n, __import__('ast').Assign) and any(isinstance(t, __import__('ast').Name) and t.id == 'doubled_positives' for t in n.targets) and isinstance(n.value, __import__('ast').GeneratorExp) for n in __import__('ast').walk(__import__('ast').parse(open('main.py').read())))]","expected":[10,true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"09b7e12d043eb48c0809483c6568331e102a795a1364563d63a02645b592d563","tests_passed":1}
  feedback✔: (expression for item in iterable if condition) defines a generator that transforms accepted items lazily; the filtering if clause is optional. Pass a generator expression as the sole argument to sum to total transformed values without creating an intermediate list.  feedback✘: Recheck the evidence against the stated requirement. (expression for item in iterable if condition) defines a generator that transforms accepted items lazily; the filtering if clause is optional. Pass a generator expression as the sole argument to sum to total transformed values without creating an intermediate list.  hints: ['Distinguish obtaining the source iterable from processing each item.']
  MEASURES: C:transform_and_filter_without_intermediate_collection(f1,f3)   anchors=['practice', 'assessment:transform_and_filter_without_intermediate_collection']
  taught-before-tested: C.f1←s07; C.f3←s07

### s10 · explainer · Iterator consumption and exhaustion
Understand — 
(mechanism) Each `next(iterator)` consumes an item. A later traversal or consumer sees only what remains. ⟦D.f1 D:tb1 D:tb2 D:tb4 D:tb5⟧
(mechanism) Once an iterator raises StopIteration, subsequent calls must continue to raise it. ⟦D.f2 D:tb3 D:tb4⟧
(mechanism) `iter(iterator)` returns the same iterator; it does not reset progress. ⟦D.f3 D:tb1 D:tb3 D:tb4 D:tb5⟧
(mechanism) For another pass over a reusable collection, obtain a fresh iterator from the collection, not its exhausted iterator. ⟦D.f4 D:tb3 D:tb4⟧
[CODE python]
values = [3, 2]
traversal = iter(values)
print(next(traversal))
print(list(traversal))
print(list(iter(traversal)))
print(list(iter(values)))
  annotations: ['Consumes the next item.', 'Same traversal, not a restart.', 'Fresh pass over the reusable list.']

### s11 · check · Check: Iterator consumption and exhaustion
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, stretch, grading=client] Given traversal = iter([3, 2]) and next(traversal), which describes list(traversal) followed by two next(traversal, None) calls?
  ✔ o1: The list contains only the remaining item; both defaulted calls return None.
      why: Each next(iterator) consumes the next available item; a traversal or consumer sees only the remaining items. Once an iterator raises StopIteration, it must continue to do so on subsequent calls.
  ✘ o2: The list contains both original items; both calls return None.
      why: The first item was consumed by next and is not included in the remaining list.
  ✘ o3: The list contains only the remaining item; the second defaulted call restarts the iterator.
      why: Exhaustion persists; further defaulted next calls do not restart traversal.
  feedback✔: Each next(iterator) consumes the next available item; a traversal or consumer sees only the remaining items. Once an iterator raises StopIteration, it must continue to do so on subsequent calls.  feedback✘: Recheck the evidence against the stated requirement. Each next(iterator) consumes the next available item; a traversal or consumer sees only the remaining items. Once an iterator raises StopIteration, it must continue to do so on subsequent calls.  hints: ['Mark each item that an earlier advance has already consumed.']  remediation→r06
  MEASURES: D:predict_remaining_items_after_partial_consumption(f1); D:predict_repeated_next_calls_after_exhaustion(f2)   anchors=['assessment:predict_remaining_items_after_partial_consumption', 'assessment:predict_repeated_next_calls_after_exhaustion']
  taught-before-tested: D.f1←s10; D.f2←s10

### s12 · check · Check: Iterator consumption and exhaustion
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, stretch, grading=client] After traversal = iter([3, 2]) and next(traversal), what does iter(traversal) do?
  ✔ o1: Returns that same, partly consumed traversal.
      why: iter(iterator) returns the same iterator and does not reset it.
  ✘ o2: Creates a fresh traversal over both items.
      why: iter on an iterator preserves the same traversal and position.
  ✘ o3: Returns the same traversal but resets its position.
      why: Returning the same iterator does not reset consumption.
  feedback✔: iter(iterator) returns the same iterator and does not reset it.  feedback✘: Recheck the evidence against the stated requirement. iter(iterator) returns the same iterator and does not reset it.  hints: ['Mark each item that an earlier advance has already consumed.']
  MEASURES: D:predict_iterator_state_after_iter_call(f3)   anchors=['assessment:predict_iterator_state_after_iter_call']
  taught-before-tested: D.f3←s10

### s13 · hands_on · Practice: Iterator consumption and exhaustion
Practice — Fix a helper that attempts two complete passes over values but reuses an exhausted traversal for the second pass.
QUESTION [code_exercise, stretch, grading=client] The supplied two_passes helper consumes traversal on its first pass. Repair its second pass by selecting the supplied source helper that permits a fresh traversal of values, so it obtains a fresh iterator from values. Leave the supplied helpers and exhaustion trace unchanged. two_passes must return two full lists for each input; the supplied trace must continue to show repeated exhaustion and iterator identity.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def', 'function parameters and calls', 'return', 'variable assignment', 'list literals', 'integer literals', 'tuple construction', 'iter()', 'next()', 'list()', 'print()', 'is', 'try', 'except StopIteration'] blocked=6 items
  file main.py [editable]:
values_input_0 = 3
values_input_1 = 2
values = [values_input_0, values_input_1]

# Supplied scaffold: preserve this block unchanged.
if True:
    def collection_source(values, traversal):
        return values

    def exhausted_source(values, traversal):
        return traversal

    def two_passes(values):
        traversal = iter(values)
        first = list(traversal)
        second = list(iter(second_source(values, traversal)))
        return first, second
    # TODO: repair the second pass.

    def trace_exhaustion(values):
        traversal = iter(values)
        first = next(traversal)
        remaining = list(traversal)
        exhausted_once = next(traversal, None)
        exhausted_again = next(traversal, None)
        return first, remaining, exhausted_once, exhausted_again, iter(traversal) is traversal

# TODO: select the reusable collection as the second-pass source.
second_source = exhausted_source

  SOLUTION main.py:
values_input_0 = 3
values_input_1 = 2
values = [values_input_0, values_input_1]

# Supplied scaffold: preserve this block unchanged.
if True:
    def collection_source(values, traversal):
        return values

    def exhausted_source(values, traversal):
        return traversal

    def two_passes(values):
        traversal = iter(values)
        first = list(traversal)
        second = list(iter(second_source(values, traversal)))
        return first, second
    # TODO: repair the second pass.

    def trace_exhaustion(values):
        traversal = iter(values)
        first = next(traversal)
        remaining = list(traversal)
        exhausted_once = next(traversal, None)
        exhausted_again = next(traversal, None)
        return first, remaining, exhausted_once, exhausted_again, iter(traversal) is traversal

# TODO: select the reusable collection as the second-pass source.
second_source = collection_source

  test test1 (function_call, visible=True): {"function":"two_passes","args":[[3,2]],"expected":[[3,2],[3,2]]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  test test2 (function_call, visible=True): {"function":"two_passes","args":[[5,4,3]],"expected":[[5,4,3],[5,4,3]]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  test test3 (function_call, visible=True): {"function":"trace_exhaustion","args":[[3,2]],"expected":[3,[2],null,null,true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  test test4 (function_call, visible=True): {"function":"trace_exhaustion","args":[[5,4,3]],"expected":[5,[4,3],null,null,true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4117f8030861aa88aea40fd15abe3dbe17495e287563f5e558229e494f3a3d49","tests_passed":4}
  feedback✔: For another pass over a reusable collection, obtain a fresh iterator from that collection rather than reusing its exhausted iterator.  feedback✘: Recheck the evidence against the stated requirement. For another pass over a reusable collection, obtain a fresh iterator from that collection rather than reusing its exhausted iterator.  hints: ['Mark each item that an earlier advance has already consumed.']
  MEASURES: D:predict_results_from_a_fresh_collection_iterator(f4)   anchors=['practice', 'assessment:predict_results_from_a_fresh_collection_iterator']
  taught-before-tested: D.f4←s10

### s14 · recap · Takeaways
Keep these distinctions — 
(takeaway) Lists store reusable items; separate list iterators track independent progress. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Yield supplies an item, suspends execution and retains local state. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
(takeaway) Evaluate the leftmost source immediately; filter and transform during iteration. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(takeaway) Consumption does not reset: obtain a fresh collection iterator for another pass. ⟦D.f1 D.f3 D.f4 D:tb1 D:tb2 D:tb3 D:tb4 D:tb5⟧
[UP NEXT] Choosing eager or lazy processing: Choose eager or lazy processing for an iterable workload.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Iterables and iterators
(mechanism) At exhaustion, `next(iterator, default)` returns the default instead of raising StopIteration. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast exhaustion with and without a default: the default form returns a fallback instead of raising StopIteration. ⟦A.f4 A:tb3 A:tb4⟧
### r02 · Revisit: Iterables and iterators
(mechanism) An iterable supplies an iterator through `iter(value)`. An iterator supplies successive items through `next(iterator)` and signals exhaustion with StopIteration. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Separate `iter(list_value)` calls have separate traversal state; the list stores reusable items. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Calling `iter` on an iterator returns that same iterator, not an independent traversal. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) At exhaustion, `next(iterator, default)` returns the default instead of raising StopIteration. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast a fresh list iterator with iter applied to an existing iterator: only the former gives independent progress. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Generator functions with yield
(mechanism) Calling a function containing `yield` creates a generator iterator. Advancing it runs to the next yield. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) `yield value` supplies one item and suspends execution, retaining local state until the next advance. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
(mechanism) Inside the function, use a for loop and condition to yield accepted items. Reaching the function’s end terminates iteration. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) Contrast yielding an item with completing an ordinary return-style calculation: yield suspends and retains state. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit: Generator expressions
(mechanism) The leftmost iterable expression is evaluated immediately; filtering and item transformations happen during iteration. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast evaluating the source expression now with transforming its items during iteration. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
### r05 · Revisit: Generator expressions
(mechanism) `(expression for item in iterable if condition)` lazily transforms accepted items. The filtering if clause is optional. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(mechanism) As the sole argument to `sum`, a generator expression totals transformed values without an intermediate list. ⟦C.f3 C:tb1 C:tb3 C:tb4⟧
(misconception) Contrast evaluating the source expression now with transforming its items during iteration. ⟦C.f1 C.f3 C:tb1 C:tb2 C:tb3 C:tb4⟧
### r06 · Revisit: Iterator consumption and exhaustion
(mechanism) Each `next(iterator)` consumes an item. A later traversal or consumer sees only what remains. ⟦D.f1 D:tb1 D:tb2 D:tb4 D:tb5⟧
(mechanism) Once an iterator raises StopIteration, subsequent calls must continue to raise it. ⟦D.f2 D:tb3 D:tb4⟧
(misconception) Contrast the original collection with the consumed traversal: later consumers see only remaining items, and exhaustion persists. ⟦D.f1 D.f2 D:tb1 D:tb2 D:tb3 D:tb4 D:tb5⟧
### r07 · Revisit: Iterator consumption and exhaustion
(mechanism) `iter(iterator)` returns the same iterator; it does not reset progress. ⟦D.f3 D:tb1 D:tb3 D:tb4 D:tb5⟧
(misconception) Contrast a fresh pass from values with another pass from traversal: the exhausted traversal does not restart. ⟦D.f3 D:tb1 D:tb3 D:tb4 D:tb5⟧
### r08 · Revisit: Iterator consumption and exhaustion
(mechanism) For another pass over a reusable collection, obtain a fresh iterator from the collection, not its exhausted iterator. ⟦D.f4 D:tb3 D:tb4⟧
(misconception) Contrast a fresh pass from values with another pass from traversal: the exhausted traversal does not restart. ⟦D.f4 D:tb3 D:tb4⟧

=========

# EVALUATOR PACKET — Choosing eager or lazy processing / Chaining iterables with itertools / Choosing map or filter for iterable transformations (learn_python.tile.104_106)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.eager_vs_lazy_processing — Choosing eager or lazy processing
B = python.itertools_utilities — Chaining iterables with itertools
C = python.map_and_filter — Choosing map or filter for iterable transformations

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: remediation step learn_python.tile.104_106.r02 is never referenced
  warn: remediation step learn_python.tile.104_106.r05 is never referenced
  warn: learn_python.tile.104_106.s04/ix.learn_python.tile.104_106.s04: ADVISORY — syntax descriptors with no detector: ['generator expressions', 'integer literals', 'itertools', 'list comprehensions', 'list literals', 'multiplication', 'unittest']
  warn: learn_python.tile.104_106.s08/ix.learn_python.tile.104_106.s08: ADVISORY — syntax descriptors with no detector: ['integer literals', 'list literals']
  warn: learn_python.tile.104_106.s12/ix.learn_python.tile.104_106.s12: ADVISORY — syntax descriptors with no detector: ['* multiplication', '> comparisons', 'def statements', 'function parameters and calls', 'integer literals', 'list literals', 'return statements']

## SOURCE FACTS — A (python.eager_vs_lazy_processing)   objective: Choose eager or lazy processing for an iterable workload.
A.f1: list(iterable) materializes its remaining items into a list that can be traversed repeatedly.   [sources: python_stdlib_reference#stdtypes.html#lists]
A.f2: Generator expressions compute values as consumed and tend to use less memory than equivalent list comprehensions.   [sources: python_tutorial#classes.html#generator-expressions]
A.f3: For a one-pass total, sum(expression for item in iterable) avoids constructing an intermediate transformed list.   [sources: python_tutorial#classes.html#generator-expressions]
A.f4: An iterator is consumed as it advances and stays exhausted after completion, so repeated reuse may require a stored collection or a new source traversal.   [sources: python_stdlib_reference#stdtypes.html#iterator.__next__]
note: Begin with this objective: Choose eager or lazy processing for an iterable workload.
note: Keep the example in the Choosing eager or lazy transformations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.itertools_utilities, python.map_and_filter, python.unittest_test_cases.
PRACTICE ANCHOR (live_code): Rewrite a one-pass total over doubled values so it avoids building an intermediate transformed list.  SUCCESS: The rewritten expression produces 10 from values = [3, 2] using a generator expression directly inside sum(), without materializing the doubled values.
ASSESSMENT ANCHOR: choose_materialization_for_repeated_traversal facts=['f1', 'f4']
ASSESSMENT ANCHOR: choose_lazy_processing_for_memory_efficient_one_pass_totals facts=['f2', 'f3']

## SOURCE FACTS — B (python.itertools_utilities)   objective: Chain iterable inputs lazily using itertools.chain.
B.f1: After from itertools import chain, chain(first, second) traverses each input in order, exhausting the first before moving to the second, without first concatenating them into a list.   [sources: python_stdlib_reference#itertools.html#itertools.chain]
B.f2: sum(chain(first, second)) totals numeric items from the combined traversal.   [sources: python_stdlib_reference#functions.html#sum]
note: Begin with this objective: Chain iterable inputs lazily using itertools.chain.
note: Keep the example in the Choosing eager or lazy transformations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.map_and_filter, python.unittest_test_cases, python.unittest_execution_and_results.
PRACTICE ANCHOR (live_code): Aggregate quantities from first and second using sum(chain(first, second)), without constructing an intermediate concatenated list.  SUCCESS: The code imports chain and directly totals first = [3, 2] and second = [5, 4], producing 14 without concatenating or materialising the combined traversal as a list.
ASSESSMENT ANCHOR: combine_iterables_in_order_without_intermediate_list facts=['f1']
ASSESSMENT ANCHOR: total_numeric_inputs_using_chained_traversal facts=['f1', 'f2']

## SOURCE FACTS — C (python.map_and_filter)   objective: Choose a readable iterable transformation idiom.
C.f1: map(function, iterable) lazily applies a callable to successive items and yields the results.   [sources: python_stdlib_reference#functions.html#map]
C.f2: filter(predicate, iterable) lazily yields items for which the predicate is true; filter(None, iterable) keeps truthy items.   [sources: python_stdlib_reference#functions.html#filter]
C.f3: filter(predicate, iterable) corresponds to (item for item in iterable if predicate(item)).   [sources: python_stdlib_reference#functions.html#filter]
C.f4: [function(item) for item in iterable if predicate(item)] makes a materialized transform-and-filter list and can replace a map/filter composition when that form communicates the computation more clearly.   [sources: python_tutorial#datastructures.html#list-comprehensions]
C.f5: Use a parenthesized generator expression instead of a list comprehension when preserving lazy traversal is required.   [sources: python_tutorial#classes.html#generator-expressions]
note: Begin with this objective: Choose a readable iterable transformation idiom.
note: Keep the example in the Choosing eager or lazy transformations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.unittest_test_cases, python.unittest_execution_and_results, python.unittest_setup_and_teardown.
PRACTICE ANCHOR (live_code): Rewrite map(double, filter(positive, values)) as a readable list comprehension, then write a generator expression that preserves the pipeline's lazy traversal.  SUCCESS: The comprehension produces [6, 4] for values = [3, -1, 2]. The generator expression yields the same results when consumed without materializing a list when it is created.
ASSESSMENT ANCHOR: choose_map_filter_or_comprehension_for_callable_reuse_and_clarity facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: select_equivalent_expression_with_required_materialization facts=['f3', 'f4', 'f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing map or filter for iterable transformations; Managing unittest setup and teardown; Reading and explaining generated Python; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Choosing eager or lazy processing
Understand — 
(mechanism) `list(iterable)` materializes remaining items into a list that supports repeated traversal. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Generator expressions compute as consumed and tend to use less memory than equivalent list comprehensions. ⟦A.f2 A:tb1 A:tb3⟧
(mechanism) For a one-pass total, `sum(expression for item in iterable)` avoids an intermediate transformed list. ⟦A.f3 A:tb3⟧
(mechanism) An iterator advances by consuming items and stays exhausted after completion. Reuse may require a stored collection or new source traversal. ⟦A.f4 A:tb3⟧
[CODE python]
values = [3, 2]
lazy = (value * 2 for value in values)
print(sum(lazy))
print(list(lazy))
stored = list(value * 2 for value in values)
print(sum(stored))
print(sum(stored))
  annotations: ['Consume lazy items.', 'Only remaining items.', 'Materialize for repeated traversal.']

### s02 · explainer · Choosing eager or lazy processing
Understand — 
(mechanism) `list(iterable)` materializes remaining items into a list that supports repeated traversal. ⟦A.f1 A:tb4⟧
(mechanism) Generator expressions compute as consumed and tend to use less memory than equivalent list comprehensions. ⟦A.f2 A:tb4⟧
(mechanism) For a one-pass total, `sum(expression for item in iterable)` avoids an intermediate transformed list. ⟦A.f3 A:tb4⟧
(mechanism) An iterator advances by consuming items and stays exhausted after completion. Reuse may require a stored collection or new source traversal. ⟦A.f4 A:tb4 A:tb5⟧
(misconception) Contrast one-pass lazy consumption with repeated traversal of stored items. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check: Choosing eager or lazy processing
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, intro, grading=client] You need two complete passes over transformed values from a finite generator. The source cannot be traversed again. What should you do before either pass?
  ✔ o1: Materialize the generator with list and reuse the stored list.
      why: list(iterable) materializes its remaining items into a list that can be traversed repeatedly. An iterator is consumed as it advances and stays exhausted after completion, so repeated reuse may require a stored collection or a new source traversal.
  ✘ o2: Pass the same generator to each pass without storing its items.
      why: The first complete pass exhausts the generator, leaving no items for the second.
  ✘ o3: Call iter on the exhausted generator for the second pass.
      why: iter on an existing iterator does not create a new source traversal.
  feedback✔: list(iterable) materializes its remaining items into a list that can be traversed repeatedly. An iterator is consumed as it advances and stays exhausted after completion, so repeated reuse may require a stored collection or a new source traversal.  feedback✘: Recheck the evidence against the stated requirement. list(iterable) materializes its remaining items into a list that can be traversed repeatedly. An iterator is consumed as it advances and stays exhausted after completion, so repeated reuse may require a stored collection or a new source traversal.  hints: ['Count how many complete traversals the requirement needs.']  remediation→r01
  MEASURES: A:choose_materialization_for_repeated_traversal(f1,f4)   anchors=['assessment:choose_materialization_for_repeated_traversal']
  taught-before-tested: A.f1←s01; A.f4←s01

### s04 · hands_on · Practice: Choosing eager or lazy processing
Practice — Rewrite a one-pass total over doubled values so it avoids building an intermediate transformed list.
QUESTION [code_exercise, core, grading=client] Assign stored by passing the supplied lazy_doubled generator directly to sum. Preserve values and the supplied generator expression. Do not construct an intermediate transformed list. With values [3, 2], stored must be 10.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'integer literals', 'list literals', 'multiplication', 'list comprehensions', 'generator expressions', 'sum()', 'list()', 'print()'] blocked=4 items
  file main.py [editable]:
values_input_0 = 3
values_input_1 = 2
values = [values_input_0, values_input_1]
# Supplied lazy transformation; preserve this expression.
lazy_doubled = (value * 2 for value in values)
stored = None
# TODO: total the lazy stream directly with sum.

  SOLUTION main.py:
values_input_0 = 3
values_input_1 = 2
values = [values_input_0, values_input_1]
# Supplied lazy transformation; preserve this expression.
lazy_doubled = (value * 2 for value in values)
stored = None
# TODO: total the lazy stream directly with sum.
stored = sum(lazy_doubled)

  test test1 (value_equals, visible=True): {"expr":"[stored, any((isinstance(n, __import__('ast').Assign) and any((isinstance(t, __import__('ast').Name) and t.id == 'lazy_doubled' for t in n.targets)) and isinstance(n.value, __import__('ast').GeneratorExp) for n in __import__('ast').walk(__import__('ast').parse(open('main.py').read()))))]","expected":[10,true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9d57388ba713ae738dc3f144bbcb3501ce367fa6c577d35673689c3ff7370fb5","tests_passed":1}
  feedback✔: Generator expressions compute values as consumed and tend to use less memory than equivalent list comprehensions. For a one-pass total, sum(expression for item in iterable) avoids constructing an intermediate transformed list.  feedback✘: Recheck the evidence against the stated requirement. Generator expressions compute values as consumed and tend to use less memory than equivalent list comprehensions. For a one-pass total, sum(expression for item in iterable) avoids constructing an intermediate transformed list.  hints: ['Count how many complete traversals the requirement needs.']
  MEASURES: A:choose_lazy_processing_for_memory_efficient_one_pass_totals(f2,f3)   anchors=['practice', 'assessment:choose_lazy_processing_for_memory_efficient_one_pass_totals']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · explainer · Chaining iterables with itertools
Understand — 
(mechanism) After `from itertools import chain`, `chain(first, second)` exhausts the first input before traversing the second, without first concatenating them into a list. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) `sum(chain(first, second))` totals numeric items from that combined traversal. ⟦B.f2 B:tb3 B:tb4⟧
[CODE python]
from itertools import chain
first = [3, 2]
second = [5, 4]
print(list(chain(first, second)))
print(sum(chain(first, second)))
  annotations: ['Display input-order traversal.', 'Total directly; no concatenated list required.']

### s06 · video · Chaining iterables with itertools
Worked walkthrough — 
[VIDEO Traverse inputs in sequence with chain] bridge-before: Watch for the first string’s characters followed by the second’s, and the distinction between retrieving items one at a time and constructing a concatenated list. | bridge-after: The clip explains sequential traversal without a concatenated list. The text supplies the exact from itertools import chain statement and shows how sum totals numeric inputs.
  - p8FUoSIyIVY 601-646s facts=['f1'] label: Chain two strings without concatenating lists | summary: Chaining two string inputs produces the characters from the first string, followed by those from the second. The combined traversal is an iterator: items can be retrieved and processed one at a time rather than first constructing a concatenated list. This avoids storing an additional list of all the combined items.

### s07 · check · Check: Chaining iterables with itertools
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] first and second are numeric lists. Which expression totals their items in order without first building a combined list?
  ✔ o1: sum(chain(first, second)) after importing chain.
      why: After from itertools import chain, chain(first, second) traverses each input in order, exhausting the first before moving to the second, without first concatenating them into a list. sum(chain(first, second)) totals numeric items from the combined traversal.
  ✘ o2: sum(list(chain(first, second))) after importing chain.
      why: This materializes an intermediate combined list, contrary to the requirement.
  ✘ o3: sum(first) alone.
      why: This omits the second input rather than traversing both.
  feedback✔: After from itertools import chain, chain(first, second) traverses each input in order, exhausting the first before moving to the second, without first concatenating them into a list. sum(chain(first, second)) totals numeric items from the combined traversal.  feedback✘: Recheck the evidence against the stated requirement. After from itertools import chain, chain(first, second) traverses each input in order, exhausting the first before moving to the second, without first concatenating them into a list. sum(chain(first, second)) totals numeric items from the combined traversal.  hints: ['Check whether the expression includes both sources and creates an extra collection.']  remediation→r03
  MEASURES: B:total_numeric_inputs_using_chained_traversal(f1,f2)   anchors=['assessment:total_numeric_inputs_using_chained_traversal']
  taught-before-tested: B.f1←s05; B.f2←s05

### s08 · hands_on · Practice: Chaining iterables with itertools
Practice — Aggregate quantities from first and second using sum(chain(first, second)), without constructing an intermediate concatenated list.
QUESTION [code_exercise, core, grading=client] Import chain from itertools. Assign total by directly passing chain(first, second) to sum. Traverse both inputs in their given order without concatenating or materializing the combined traversal.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['from itertools import chain', 'variable assignment', 'integer literals', 'list literals', 'chain(first, second)', 'sum(chain(first, second))', 'print()'] blocked=6 items
  file main.py [editable]:
total = None
first_input_0 = 3
first_input_1 = 2
first = [first_input_0, first_input_1]
second_input_0 = 5
second_input_1 = 4
second = [second_input_0, second_input_1]
# TODO: import chain and directly total its combined traversal.

  SOLUTION main.py:
total = None
first_input_0 = 3
first_input_1 = 2
first = [first_input_0, first_input_1]
second_input_0 = 5
second_input_1 = 4
second = [second_input_0, second_input_1]
# TODO: import chain and directly total its combined traversal.
from itertools import chain
total = sum(chain(first, second))

  test test1 (value_equals, visible=True): {"expr":"[total, __import__('ast').dump(next(n.value for n in reversed(__import__('ast').parse(open('main.py').read()).body) if isinstance(n, __import__('ast').Assign) and any(isinstance(t, __import__('ast').Name) and t.id == 'total' for t in n.targets))) == __import__('ast').dump(__import__('ast').parse('sum(chain(first, second))', mode='eval').body)]","expected":[14,true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f328422f8d9151b4d0428bcef6c5396e8bb6d03206486c0ca9be5c9b23a6a6ed","tests_passed":1}
  feedback✔: After from itertools import chain, chain(first, second) traverses each input in order, exhausting the first before moving to the second, without first concatenating them into a list. sum(chain(first, second)) totals numeric items from the combined traversal.  feedback✘: Recheck the evidence against the stated requirement. After from itertools import chain, chain(first, second) traverses each input in order, exhausting the first before moving to the second, without first concatenating them into a list. sum(chain(first, second)) totals numeric items from the combined traversal.  hints: ['Check whether the expression includes both sources and creates an extra collection.']
  MEASURES: B:combine_iterables_in_order_without_intermediate_list(f1); B:total_numeric_inputs_using_chained_traversal(f1,f2)   anchors=['practice', 'assessment:combine_iterables_in_order_without_intermediate_list', 'assessment:total_numeric_inputs_using_chained_traversal']
  taught-before-tested: B.f1←s05; B.f1←s05; B.f2←s05

### s09 · explainer · Choosing map or filter for iterable transformations
Understand — 
(mechanism) `map(function, iterable)` lazily applies a callable to successive items, yielding results. ⟦C.f1 C:tb2⟧
(mechanism) `filter(predicate, iterable)` lazily keeps items whose predicate is true; `filter(None, iterable)` keeps truthy items. ⟦C.f2 C:tb3⟧
(mechanism) `filter(predicate, iterable)` corresponds to `(item for item in iterable if predicate(item))`. ⟦C.f3 C:tb3⟧
(mechanism) `[function(item) for item in iterable if predicate(item)]` materializes a transform-and-filter list; it can replace a map/filter composition when clearer. ⟦C.f4 C:tb3⟧
(mechanism) To preserve lazy traversal, use a parenthesized generator expression rather than a list comprehension. ⟦C.f5 C:tb3⟧
[SIDE_BY_SIDE] List materializes; the parenthesized form stays lazy. left_label: Callable pipeline | right_label: Comprehension forms
  left:
[CODE python]
def positive(value):
    return value > 0

def double(value):
    return value * 2

values = [3, -1, 2]
lazy = map(double, filter(positive, values))
print(list(lazy))
  annotations: []
  right:
[CODE python]
def positive(value):
    return value > 0

def double(value):
    return value * 2

values = [3, -1, 2]
stored = [double(value) for value in values if positive(value)]
lazy = (double(value) for value in values if positive(value))
  annotations: []

### s10 · explainer · Choosing map or filter for iterable transformations
Understand — 
(mechanism) `map(function, iterable)` lazily applies a callable to successive items, yielding results. ⟦C.f1 C:tb4⟧
(mechanism) `filter(predicate, iterable)` lazily keeps items whose predicate is true; `filter(None, iterable)` keeps truthy items. ⟦C.f2 C:tb4⟧
(mechanism) `filter(predicate, iterable)` corresponds to `(item for item in iterable if predicate(item))`. ⟦C.f3 C:tb4⟧
(mechanism) `[function(item) for item in iterable if predicate(item)]` materializes a transform-and-filter list; it can replace a map/filter composition when clearer. ⟦C.f4 C:tb4 C:tb5⟧
(mechanism) To preserve lazy traversal, use a parenthesized generator expression rather than a list comprehension. ⟦C.f5 C:tb4 C:tb5⟧
(misconception) Contrast a materialized comprehension with a parenthesized expression that preserves lazy traversal. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4 C:tb5⟧

### s11 · check · Check: Choosing map or filter for iterable transformations
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, stretch, grading=client] positive is a predicate and double is a transformation. Which rewrite of map(double, filter(positive, values)) creates a materialized list?
  ✔ o1: [double(value) for value in values if positive(value)]
      why: filter(predicate, iterable) corresponds to (item for item in iterable if predicate(item)). [function(item) for item in iterable if predicate(item)] makes a materialized transform-and-filter list and can replace a map/filter composition when that form communicates the computation more clearly. Use a parenthesized generator expression instead of a list comprehension when preserving lazy traversal is required.
  ✘ o2: (double(value) for value in values if positive(value))
      why: Parentheses create a lazy generator expression, not a materialized list.
  ✘ o3: [value for value in values if positive(value)]
      why: This selects values but omits the required double transformation.
  feedback✔: filter(predicate, iterable) corresponds to (item for item in iterable if predicate(item)). [function(item) for item in iterable if predicate(item)] makes a materialized transform-and-filter list and can replace a map/filter composition when that form communicates the computation more clearly. Use a parenthesized generator expression instead of a list comprehension when preserving lazy traversal is required.  feedback✘: Recheck the evidence against the stated requirement. filter(predicate, iterable) corresponds to (item for item in iterable if predicate(item)). [function(item) for item in iterable if predicate(item)] makes a materialized transform-and-filter list and can replace a map/filter composition when that form communicates the computation more clearly. Use a parenthesized generator expression instead of a list comprehension when preserving lazy traversal is required.  hints: ['Separate selection from transformation, then inspect the outer brackets or parentheses.']  remediation→r04
  MEASURES: C:select_equivalent_expression_with_required_materialization(f3,f4,f5)   anchors=['assessment:select_equivalent_expression_with_required_materialization']
  taught-before-tested: C.f3←s09; C.f4←s09; C.f5←s09

### s12 · hands_on · Practice: Choosing map or filter for iterable transformations
Practice — Rewrite map(double, filter(positive, values)) as a readable list comprehension, then write a generator expression that preserves the pipeline's lazy traversal.
QUESTION [code_exercise, stretch, grading=client] Compare the supplied map/filter traversal with equivalent_stored (a filtered list comprehension) and equivalent_lazy (a filtered generator expression). Bind stored to the eager comprehension result and lazy to the generator result, preserving the supplied transformations and predicate. Both must yield doubled positive entries [6, 4] for values [3, -1, 2], and lazy must be a generator iterator.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'integer literals', 'list literals', 'def statements', 'function parameters and calls', 'return statements', '> comparisons', '* multiplication', 'map(function, iterable)', 'filter(predicate, iterable)', 'list(iterable)', '[double(value) for value in values if positive(value)]', '(double(value) for value in values if positive(value))'] blocked=6 items
  file main.py [editable]:
stored = None
# Supplied scaffold: preserve this block unchanged.
if True:
    def positive(value):
        return value > 0
# Supplied scaffold: preserve this block unchanged.
if True:
    def double(value):
        return value * 2
values_input_0 = 3
values_input_1 = -1
values_input_2 = 2
values = [values_input_0, values_input_1, values_input_2]
lazy = map(double, filter(positive, values))
equivalent_stored = [double(value) for value in values if positive(value)]
equivalent_lazy = (double(value) for value in values if positive(value))

stored = None
lazy = None
# TODO: bind the equivalent eager and lazy comprehension results.

  SOLUTION main.py:
stored = None
# Supplied scaffold: preserve this block unchanged.
if True:
    def positive(value):
        return value > 0
# Supplied scaffold: preserve this block unchanged.
if True:
    def double(value):
        return value * 2
values_input_0 = 3
values_input_1 = -1
values_input_2 = 2
values = [values_input_0, values_input_1, values_input_2]
lazy = map(double, filter(positive, values))
equivalent_stored = [double(value) for value in values if positive(value)]
equivalent_lazy = (double(value) for value in values if positive(value))

stored = None
lazy = None
# TODO: bind the equivalent eager and lazy comprehension results.
stored = equivalent_stored
lazy = equivalent_lazy

  test test1 (value_equals, visible=True): {"expr":"[stored, list(lazy), type(lazy).__name__ == 'generator']","expected":[[6,4],[6,4],true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"cf04f546790991d6043ead98896160e4f94e5029324ec23d3d872098d3367d11","tests_passed":1}
  feedback✔: map(function, iterable) lazily applies a callable to successive items and yields the results. filter(predicate, iterable) lazily yields items for which the predicate is true; filter(None, iterable) keeps truthy items. [function(item) for item in iterable if predicate(item)] makes a materialized transform-and-filter list and can replace a map/filter composition when that form communicates the computation more clearly.  feedback✘: Recheck the evidence against the stated requirement. map(function, iterable) lazily applies a callable to successive items and yields the results. filter(predicate, iterable) lazily yields items for which the predicate is true; filter(None, iterable) keeps truthy items. [function(item) for item in iterable if predicate(item)] makes a materialized transform-and-filter list and can replace a map/filter composition when that form communicates the computation more clearly.  hints: ['Separate selection from transformation, then inspect the outer brackets or parentheses.']
  MEASURES: C:choose_map_filter_or_comprehension_for_callable_reuse_and_clarity(f1,f2,f4)   anchors=['practice', 'assessment:choose_map_filter_or_comprehension_for_callable_reuse_and_clarity']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f4←s09

### s13 · recap · Takeaways
Keep these distinctions — 
(takeaway) Materialize for repeated traversal; a one-pass total can avoid an intermediate list. ⟦A.f1 A.f3 A:tb1 A:tb2 A:tb3 A:tb4⟧
(takeaway) Chain exhausts inputs in order; sum can total the combined traversal directly. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Map and filter are lazy; a list comprehension materializes, while a generator expression preserves laziness. ⟦C.f1 C.f2 C.f4 C.f5 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Writing Python unittest test cases: Express supplied checks in Python unittest.TestCase syntax.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Choosing eager or lazy processing
(mechanism) `list(iterable)` materializes remaining items into a list that supports repeated traversal. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) An iterator advances by consuming items and stays exhausted after completion. Reuse may require a stored collection or new source traversal. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast one-pass lazy consumption with repeated traversal of stored items. ⟦A.f1 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Choosing eager or lazy processing
(mechanism) Generator expressions compute as consumed and tend to use less memory than equivalent list comprehensions. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(mechanism) For a one-pass total, `sum(expression for item in iterable)` avoids an intermediate transformed list. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast one-pass lazy consumption with repeated traversal of stored items. ⟦A.f2 A.f3 A:tb1 A:tb3 A:tb4⟧
### r03 · Revisit: Chaining iterables with itertools
(mechanism) After `from itertools import chain`, `chain(first, second)` exhausts the first input before traversing the second, without first concatenating them into a list. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) `sum(chain(first, second))` totals numeric items from that combined traversal. ⟦B.f2 B:tb3 B:tb4⟧
(misconception) Contrast exhausting first before second with alternating between the batches: chain follows input order. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit: Choosing map or filter for iterable transformations
(mechanism) `filter(predicate, iterable)` corresponds to `(item for item in iterable if predicate(item))`. ⟦C.f3 C:tb3 C:tb4⟧
(mechanism) `[function(item) for item in iterable if predicate(item)]` materializes a transform-and-filter list; it can replace a map/filter composition when clearer. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(mechanism) To preserve lazy traversal, use a parenthesized generator expression rather than a list comprehension. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast a materialized comprehension with a parenthesized expression that preserves lazy traversal. ⟦C.f3 C.f4 C.f5 C:tb3 C:tb4 C:tb5⟧
### r05 · Revisit: Choosing map or filter for iterable transformations
(mechanism) `map(function, iterable)` lazily applies a callable to successive items, yielding results. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) `filter(predicate, iterable)` lazily keeps items whose predicate is true; `filter(None, iterable)` keeps truthy items. ⟦C.f2 C:tb3 C:tb4⟧
(mechanism) `[function(item) for item in iterable if predicate(item)]` materializes a transform-and-filter list; it can replace a map/filter composition when clearer. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast a materialized comprehension with a parenthesized expression that preserves lazy traversal. ⟦C.f1 C.f2 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: from unittest import TestCase
· constraints.blocked_syntax: from unittest import TestCase
· constraints.blocked_syntax: unittest.TestCase subclasses

=========

# EVALUATOR PACKET — Writing Python unittest test cases / Running unittest and interpreting its results / Managing unittest setup and teardown (learn_python.tile.107_109)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.unittest_test_cases — Writing Python unittest test cases
B = python.unittest_execution_and_results — Running unittest and interpreting its results
C = python.unittest_setup_and_teardown — Managing unittest setup and teardown

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=7
  warn: remediation step learn_python.tile.107_109.r02 is never referenced
  warn: remediation step learn_python.tile.107_109.r04 is never referenced
  warn: remediation step learn_python.tile.107_109.r05 is never referenced
  warn: remediation step learn_python.tile.107_109.r07 is never referenced
  warn: learn_python.tile.107_109.s03/ix.learn_python.tile.107_109.s03: ADVISORY — syntax descriptors with no detector: ['comparison expressions', 'if quantity < 0:', 'indented class, method and with bodies', 'integer literals', 'return quantity * 4']
  warn: learn_python.tile.107_109.s09/ix.learn_python.tile.107_109.s09: ADVISORY — syntax descriptors with no detector: ['def test_<name>(self):', 'function calls', 'numeric literals', 'python -m unittest discover', 'python -m unittest discover -s <starting_directory> -p <filename_pattern>', 'python -m unittest test_cost']
  warn: learn_python.tile.107_109.s13/ix.learn_python.tile.107_109.s13: ADVISORY — syntax descriptors with no detector: ['function and method calls', 'instance attribute access', 'list indexing and mutation', 'unittest assertion method calls']

## SOURCE FACTS — A (python.unittest_test_cases)   objective: Express supplied checks in Python unittest.TestCase syntax.
A.f1: After import unittest, define class Tests(unittest.TestCase): with methods named test_* to express individual supplied checks.   [sources: python_stdlib_reference#unittest.html#basic-example]
A.f2: Use self.assertEqual(actual, expected) for equality and self.assertTrue(condition) for a required true condition.   [sources: python_stdlib_reference#unittest.html#basic-example]
A.f3: Use with self.assertRaises(ExceptionType): around the supplied failing operation to check that it raises the expected exception.   [sources: python_stdlib_reference#unittest.html#unittest.TestCase.assertRaises]
note: Begin with this objective: Express supplied checks in Python unittest.TestCase syntax.
note: Keep the example in the Writing and running unittest tests tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.unittest_execution_and_results, python.unittest_setup_and_teardown, python.read_generated_code.
note: Require testing.write_unit_tests_with_assertions and testing.test_edge_cases_and_failures before applying the supplied checks. This unit does not supply the external testing foundations.
PRACTICE ANCHOR (live_code): Translate supplied normal and invalid-input cases for cost(quantity) into a unittest.TestCase module: cost(3) equals 12, cost(3) is positive, and cost(-1) raises ValueError.  SUCCESS: The module imports unittest and defines a TestCase subclass with test_* methods containing the supplied equality, truth and expected-exception checks. The call cost(-1) is inside the assertRaises body.
ASSESSMENT ANCHOR: define_named_unittest_test_methods facts=['f1']
ASSESSMENT ANCHOR: implement_supplied_equality_and_truth_checks facts=['f2']
ASSESSMENT ANCHOR: check_supplied_expected_exceptions facts=['f3']

## SOURCE FACTS — B (python.unittest_execution_and_results)   objective: Run Python unittest discovery and interpret runner outcomes.
B.f1: python -m unittest test_module runs a named test module, and python -m unittest discover invokes test discovery.   [sources: python_stdlib_reference#unittest.html#command-line-interface]
B.f2: Discovery defaults to the current directory and test*.py filenames; -s selects a starting directory and -p selects a filename pattern.   [sources: python_stdlib_reference#unittest.html#test-discovery]
B.f3: A failure is an unsuccessful assertion check; the runner report identifies the test and traceback for the failed assertion.   [sources: python_stdlib_reference#unittest.html#unittest.TestResult.failures]
B.f4: An error is an unexpected exception during a test rather than an explicitly failed assertion.   [sources: python_stdlib_reference#unittest.html#unittest.TestResult.errors]
B.f5: The reported test count records how many tests ran; a count of zero supplies no executed checks of the helper’s behavior.   [sources: python_stdlib_reference#unittest.html#unittest.TestResult.testsRun]
note: Begin with this objective: Run Python unittest discovery and interpret runner outcomes.
note: Keep the example in the Writing and running unittest tests tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.unittest_setup_and_teardown, python.read_generated_code, python.review_generated_file_operations.
note: Require testing.write_unit_tests_with_assertions and testing.test_edge_cases_and_failures before applying the supplied checks. This unit does not supply the external testing foundations.
PRACTICE ANCHOR (live_code): Run the supplied test_cost.py module with unittest and identify its failing assertion from the runner report.  SUCCESS: The learner runs python -m unittest test_cost, identifies the reported failing test and assertion from its traceback, and classifies the outcome as a failure rather than an error.
ASSESSMENT ANCHOR: invoke_unittest_discovery_with_directory_and_pattern facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_assertion_failures_from_unexpected_errors facts=['f3', 'f4']
ASSESSMENT ANCHOR: recognize_zero_tests_as_no_executed_checks facts=['f5']

## SOURCE FACTS — C (python.unittest_setup_and_teardown)   objective: Implement isolated unittest fixtures with setup and cleanup hooks.
C.f1: Define setUp(self) to initialize fresh per-test state before each test method; an error in setUp prevents that test method from running.   [sources: python_stdlib_reference#unittest.html#unittest.TestCase.setUp]
C.f2: tearDown(self) runs after a test when setUp succeeded, including when the test failed.   [sources: python_stdlib_reference#unittest.html#unittest.TestCase.tearDown]
C.f3: self.addCleanup(function, *args, **kwargs) registers cleanup that runs after tearDown, or after a failed setUp; registered actions run in reverse registration order.   [sources: python_stdlib_reference#unittest.html#unittest.TestCase.addCleanup]
C.f4: Register the release callable after acquiring the supplied test resource and store mutable test data on self in setUp rather than in shared class attributes.   [sources: python_stdlib_reference#unittest.html#unittest.TestCase.addCleanup]
note: Begin with this objective: Implement isolated unittest fixtures with setup and cleanup hooks.
note: Keep the example in the Writing and running unittest tests tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.read_generated_code, python.review_generated_file_operations, python.review_untrusted_input_and_execution.
note: Require testing.write_unit_tests_with_assertions and testing.test_edge_cases_and_failures before applying the supplied checks. This unit does not supply the external testing foundations.
note: Require testing.fixtures_and_test_data before fixture/isolation work.
PRACTICE ANCHOR (live_code): Implement TestCase.setUp to assign fresh self.quantities = [3, 2] and register the supplied release callable immediately after the supplied resource-acquisition step.  SUCCESS: Each test starts with quantities [3, 2], regardless of mutations in another test. The supplied resource is released after normal completion, test failure, and a setup failure occurring after cleanup registration.
ASSESSMENT ANCHOR: initialize_fresh_per_test_mutable_state facts=['f1', 'f4']
ASSESSMENT ANCHOR: trace_setup_test_teardown_and_cleanup_order facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: register_resource_release_for_setup_failure facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Managing unittest setup and teardown; Reading and explaining generated Python; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Verifying generated Python API claims

## LESSON, in learner order

### s01 · explainer · Writing Python unittest test cases
Understand — 
(mechanism) After `import unittest`, subclass `unittest.TestCase` and name methods `test_*` to express individual supplied checks. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Use `self.assertEqual(actual, expected)` for equality and `self.assertTrue(condition)` for a required true condition. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(mechanism) Place the supplied failing operation inside `with self.assertRaises(ExceptionType):` to check its expected exception. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
[CODE python]
import unittest

def cost(quantity):
    if quantity < 0:
        raise ValueError("negative quantity")
    return quantity * 4

class CostTests(unittest.TestCase):
    def test_cost(self):
        self.assertEqual(cost(3), 12)
        self.assertTrue(cost(3) > 0)
    def test_invalid_quantity(self):
        with self.assertRaises(ValueError):
            cost(-1)
  annotations: ['TestCase subclass with test_* checks.', 'Actual, then expected.', 'Indent the expected failing operation inside this context.']

### s02 · check · Check: Writing Python unittest test cases
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, intro, grading=client] A supplied case requires cost(-1) to raise ValueError. Which test checks that exception?
  ✔ o1: with self.assertRaises(ValueError):
    cost(-1)
      why: Use with self.assertRaises(ExceptionType): around the supplied failing operation to check that it raises the expected exception.
  ✘ o2: self.assertEqual(cost(-1), ValueError)
      why: The call raises instead of returning an exception class; equality is not the expected-exception check.
  ✘ o3: with self.assertRaises(ValueError):
    cost(3)
      why: The body must contain the supplied invalid-input operation, not the normal call.
  feedback✔: Use with self.assertRaises(ExceptionType): around the supplied failing operation to check that it raises the expected exception.  feedback✘: Recheck the evidence against the stated requirement. Use with self.assertRaises(ExceptionType): around the supplied failing operation to check that it raises the expected exception.  hints: ['Match each supplied behavior to the assertion intended for that kind of check.']  remediation→r01
  MEASURES: A:check_supplied_expected_exceptions(f3)   anchors=['assessment:check_supplied_expected_exceptions']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Practice: Writing Python unittest test cases
Practice — Translate supplied normal and invalid-input cases for cost(quantity) into a unittest.TestCase module: cost(3) equals 12, cost(3) is positive, and cost(-1) raises ValueError.
QUESTION [code_exercise, core, grading=client] Inspect the supplied CostTests: test_cost checks equality and positivity; test_invalid_quantity checks ValueError inside assertRaises. Complete only expected_cost using supplied_expected_cost, the required cost(3) result. Preserve the assertion calls and exception body. The checker executes both test methods against the helper and verifies that the equality assertion detects a changed multiplier.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import unittest', 'class CostTests(unittest.TestCase):', 'def test_cost(self):', 'def test_invalid_quantity(self):', 'self.assertEqual(actual, expected)', 'self.assertTrue(condition)', 'with self.assertRaises(ValueError):', 'def cost(quantity):', 'if quantity < 0:', 'raise ValueError("negative quantity")', 'return quantity * 4', 'cost(3)', 'cost(-1)', 'integer literals', 'comparison expressions', 'indented class, method and with bodies'] blocked=9 items
  file main.py [editable]:
multiplier = 4
supplied_expected_cost = 12
# Supplied scaffold: preserve this block unchanged.
if True:
    def cost(quantity):
        if quantity < 0:
            raise ValueError("negative quantity")
        return quantity * 4

    # Supplied cases: cost(3) == 12; cost(3) > 0; cost(-1) raises ValueError.
    # Supplied TestCase: preserve the named methods and assertion bodies.
    import unittest

    class CostTests(unittest.TestCase):
        def test_cost(self):
            self.assertEqual(cost(3), expected_cost)
            self.assertTrue(cost(3) > 0)

        def test_invalid_quantity(self):
            with self.assertRaises(ValueError):
                cost(-1)

# TODO: bind the equality assertion expectation to the supplied requirement.
expected_cost = None

  SOLUTION main.py:
multiplier = 4
supplied_expected_cost = 12
# Supplied scaffold: preserve this block unchanged.
if True:
    def cost(quantity):
        if quantity < 0:
            raise ValueError("negative quantity")
        return quantity * 4

    # Supplied cases: cost(3) == 12; cost(3) > 0; cost(-1) raises ValueError.
    # TODO: import unittest and implement CostTests with named test methods.
    import unittest

    class CostTests(unittest.TestCase):
        def test_cost(self):
            self.assertEqual(cost(3), expected_cost)
            self.assertTrue(cost(3) > 0)

        def test_invalid_quantity(self):
            with self.assertRaises(ValueError):
                cost(-1)

# TODO: bind the equality assertion expectation to the supplied requirement.
expected_cost = supplied_expected_cost

  test test1 (value_equals, visible=True): {"expr":"[(lambda scope: (exec('# Supplied checker: leave unchanged. It runs the checks against a candidate helper.\\ndef check_tests(multiplier):\\n    import unittest, io, ast\\n    global cost\\n    original = cost\\n    def candidate(quantity):\\n        if quantity < 0:\\n            raise ValueError(\"negative quantity\")\\n        return quantity * multiplier\\n    cost = candidate\\n    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CostTests)\\n    result = unittest.TextTestRu | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ad77661e2d17960d710513217f6985ffa77243f5359e3bee8863d0b6be71ae7c","tests_passed":1}
  feedback✔: After import unittest, define class Tests(unittest.TestCase): with methods named test_* to express individual supplied checks. Use self.assertEqual(actual, expected) for equality and self.assertTrue(condition) for a required true condition. Use with self.assertRaises(ExceptionType): around the supplied failing operation to check that it raises the expected exception.  feedback✘: Recheck the evidence against the stated requirement. After import unittest, define class Tests(unittest.TestCase): with methods named test_* to express individual supplied checks. Use self.assertEqual(actual, expected) for equality and self.assertTrue(condition) for a required true condition. Use with self.assertRaises(ExceptionType): around the supplied failing operation to check that it raises the expected exception.  hints: ['Match each supplied behavior to the assertion intended for that kind of check.']
  MEASURES: A:define_named_unittest_test_methods(f1); A:implement_supplied_equality_and_truth_checks(f2); A:check_supplied_expected_exceptions(f3)   anchors=['practice', 'assessment:define_named_unittest_test_methods', 'assessment:implement_supplied_equality_and_truth_checks', 'assessment:check_supplied_expected_exceptions']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · explainer · Running unittest and interpreting its results
Understand — 
(mechanism) `python -m unittest test_module` runs a named module; `python -m unittest discover` invokes discovery. ⟦B.f1 B:tb2⟧
(mechanism) Discovery defaults to the current directory and `test*.py`; `-s` selects a starting directory and `-p` a filename pattern. ⟦B.f2 B:tb3⟧
(mechanism) A failure is an unsuccessful assertion. The report identifies the test and failed-assertion traceback. ⟦B.f3 B:tb1 B:tb3⟧
(mechanism) An error is an unexpected exception during a test, rather than an explicitly failed assertion. ⟦B.f4 B:tb1 B:tb3⟧
(mechanism) The reported count tells how many tests ran. Zero supplies no executed checks of the helper’s behavior. ⟦B.f5 B:tb1 B:tb3⟧
[DIAGRAM: Named-module runner report and zero-test contrast] nodes=['python -m unittest test_cost', 'FAIL: test_cost (builtins.CostTests.test_cost)', 'AssertionError: None != 0', 'Ran 1 test in 0.000s', 'FAILED (failures=1)', 'Ran 0 tests in 0.000s', 'NO TESTS RAN'] edges=[] alt: Named-module runner report and zero-test contrast: python -m unittest test_cost; FAIL: test_cost (builtins.CostTests.test_cost); AssertionError: None != 0; Ran 1 test in 0.000s; FAILED (failures=1); Ran 0 tests in 0.000s; NO TESTS RAN

### s05 · explainer · Running unittest and interpreting its results
Understand — 
(mechanism) `python -m unittest test_module` runs a named module; `python -m unittest discover` invokes discovery. ⟦B.f1 B:tb4⟧
(mechanism) Discovery defaults to the current directory and `test*.py`; `-s` selects a starting directory and `-p` a filename pattern. ⟦B.f2 B:tb4⟧
(mechanism) A failure is an unsuccessful assertion. The report identifies the test and failed-assertion traceback. ⟦B.f3 B:tb4 B:tb5⟧
(mechanism) An error is an unexpected exception during a test, rather than an explicitly failed assertion. ⟦B.f4 B:tb4 B:tb5⟧
(mechanism) The reported count tells how many tests ran. Zero supplies no executed checks of the helper’s behavior. ⟦B.f5 B:tb4 B:tb5⟧
(misconception) Contrast an assertion failure with an unexpected exception; a zero-test report checks neither behavior. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4 B:tb5⟧

### s06 · video · Running unittest and interpreting its results
Worked walkthrough — 
[VIDEO Interpreting unittest failures and errors] bridge-before: Watch how a false equality assertion and an unexpected ValueError produce different result categories. Focus on what each outcome tells you about the test. | bridge-after: The clip distinguishes failures from errors. The text also teaches execution commands, discovery defaults and options, locating a failed assertion in the report, and interpreting a zero-test count.
  - 7Df7Pb0imqQ 325-379s facts=['f4'] label: Distinguish a failed assertion from an unexpected exception | summary: An unsuccessful equality assertion records a failure; raising an unexpected ValueError records an error. Both outcomes are unsuccessful, but they describe different problems: an unmet checked expectation versus an unexpected exception during execution. An assertion that correctly expects an exception can pass. Start diagnosis with the specific test case, exception type and result category, then use the traceback and test intent to understand the appropriate repair.

### s07 · check · Check: Running unittest and interpreting its results
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] Which command invokes discovery from checks with filenames matching quantity_*.py?
  ✔ o1: python -m unittest discover -s checks -p "quantity_*.py"
      why: python -m unittest test_module runs a named test module, and python -m unittest discover invokes test discovery. Discovery defaults to the current directory and test*.py filenames; -s selects a starting directory and -p selects a filename pattern.
  ✘ o2: python -m unittest discover -s "quantity_*.py" -p checks
      why: -s is the starting directory and -p is the filename pattern; these are reversed.
  ✘ o3: python -m unittest discover
      why: Default discovery uses the current directory and test*.py, not the requested directory and pattern.
  feedback✔: python -m unittest test_module runs a named test module, and python -m unittest discover invokes test discovery. Discovery defaults to the current directory and test*.py filenames; -s selects a starting directory and -p selects a filename pattern.  feedback✘: Recheck the evidence against the stated requirement. python -m unittest test_module runs a named test module, and python -m unittest discover invokes test discovery. Discovery defaults to the current directory and test*.py filenames; -s selects a starting directory and -p selects a filename pattern.  hints: ['Use -s for the starting directory and -p for the filename pattern.']  remediation→r03
  MEASURES: B:invoke_unittest_discovery_with_directory_and_pattern(f1,f2)   anchors=['assessment:invoke_unittest_discovery_with_directory_and_pattern']
  taught-before-tested: B.f1←s04; B.f2←s04

### s08 · check · Check: Running unittest and interpreting its results
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] A runner report says Ran 0 tests. What evidence of the helper behavior does this provide?
  ✔ o1: No executed checks of the helper behavior.
      why: The reported test count records how many tests ran; a count of zero supplies no executed checks of the helper’s behavior.
  ✘ o2: All supplied checks executed successfully.
      why: A count of zero means no checks executed, not that supplied checks passed.
  ✘ o3: A failed assertion was found.
      why: Zero tests supplies no executed assertion result.
  feedback✔: The reported test count records how many tests ran; a count of zero supplies no executed checks of the helper’s behavior.  feedback✘: Recheck the evidence against the stated requirement. The reported test count records how many tests ran; a count of zero supplies no executed checks of the helper’s behavior.  hints: ['Read the count, reported test name and traceback, not just the final status.']
  MEASURES: B:recognize_zero_tests_as_no_executed_checks(f5)   anchors=['assessment:recognize_zero_tests_as_no_executed_checks']
  taught-before-tested: B.f5←s04

### s09 · hands_on · Practice: Running unittest and interpreting its results
Practice — Run the supplied test_cost.py module with unittest and identify its failing assertion from the runner report.
QUESTION [code_exercise, core, grading=client] Execute the supplied TestCase with the browser checker (the equivalent of python -m unittest test_cost; no shell). Keep the supplied helper and assertion unchanged. Add a comment beginning # Review: that identifies the reported test, the assertEqual line, the actual mismatch, and whether the reported outcome is a failure or an error. The checker grades both the executed report and your evidence note. Use the exact evidence-note form "# Review: <failure/error>; <test-method>; <assertion-line>; actual <actual-value> does not equal expected <expected-value>." Fill each field from the executed report.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['python -m unittest test_cost', 'python -m unittest discover', 'python -m unittest discover -s <starting_directory> -p <filename_pattern>', 'import unittest', 'class <name>(unittest.TestCase):', 'def test_<name>(self):', 'self.assertEqual(actual, expected)', 'function calls', 'numeric literals'] blocked=7 items
  file main.py [editable]:
expected = 0
import unittest

# Supplied scaffold: preserve this block unchanged.
if True:
    def cost(quantity):
        if quantity > 0:
            return quantity * 4

# Supplied scaffold: preserve this block unchanged.
if True:
    class CostTests(unittest.TestCase):
        def test_cost(self):
            self.assertEqual(cost(0), expected)

# Supplied named-module command: python -m unittest test_cost
# Browser equivalent: TextTestRunner executes this TestCase without a shell.

  SOLUTION main.py:
expected = 0
import unittest

# Supplied scaffold: preserve this block unchanged.
if True:
    def cost(quantity):
        if quantity > 0:
            return quantity * 4

# Supplied scaffold: preserve this block unchanged.
if True:
    class CostTests(unittest.TestCase):
        def test_cost(self):
            self.assertEqual(cost(0), expected)

# Supplied named-module command: python -m unittest test_cost
# Browser equivalent: TextTestRunner executes this TestCase without a shell.

# Review: failure; test_cost; self.assertEqual(cost(0), expected); actual None does not equal expected 0.

  test test1 (value_equals, visible=True): {"expr":"[(lambda scope: (exec('def run_review(expectation):\\n    import io, unittest\\n    global expected\\n    expected = expectation\\n    stream = io.StringIO()\\n    result = unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromTestCase(CostTests))\\n    source = open(\"main.py\").read()\\n    note = \"# Review: failure; test_cost; self.assertEqual(cost(0), expected); actual None does not equal expected 0.\"\\n    noted = note in source\\n    errors = [str(en | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"3ee3d5bab80b3ced8007120c1a70b49d64b4709e38fb3d3513d1f2d72278caa1","tests_passed":1}
  feedback✔: A failure is an unsuccessful assertion check; the runner report identifies the test and traceback for the failed assertion. An error is an unexpected exception during a test rather than an explicitly failed assertion.  feedback✘: Recheck the evidence against the stated requirement. A failure is an unsuccessful assertion check; the runner report identifies the test and traceback for the failed assertion. An error is an unexpected exception during a test rather than an explicitly failed assertion.  hints: ['Read the count, reported test name and traceback, not just the final status.']
  MEASURES: B:distinguish_assertion_failures_from_unexpected_errors(f3,f4)   anchors=['practice', 'assessment:distinguish_assertion_failures_from_unexpected_errors']
  taught-before-tested: B.f3←s04; B.f4←s04

### s10 · explainer · Managing unittest setup and teardown
Understand — 
(mechanism) `setUp(self)` initializes fresh state before each test method; setup errors prevent that method from running. ⟦C.f1 C:tb2⟧
(mechanism) After successful setup, `tearDown(self)` runs after the test, even when the test fails. ⟦C.f2 C:tb3⟧
(mechanism) `self.addCleanup(function, *args, **kwargs)` registers actions that run after tearDown or failed setup, in reverse registration order. ⟦C.f3 C:tb3⟧
(mechanism) After acquiring the supplied resource, register its release callable. Store mutable data on self in setUp, not shared class attributes. ⟦C.f4 C:tb3⟧
[PROCESS_FLOW] nodes=['setUp: acquire resource', 'Register release callable', 'setUp succeeds?', 'Test: pass or fail', 'tearDown', 'Registered cleanup: reverse registration order'] edges=[('n0', 'n1', None), ('n1', 'n2', None), ('n2', 'n3', 'yes'), ('n3', 'n4', None), ('n4', 'n5', None), ('n2', 'n5', 'no: skip test and tearDown')] alt: Successful setup: test, tearDown, registered cleanup. Failed setup: skip test and tearDown; run already registered cleanup.

### s11 · explainer · Managing unittest setup and teardown
Understand — 
(mechanism) `setUp(self)` initializes fresh state before each test method; setup errors prevent that method from running. ⟦C.f1 C:tb4 C:tb5⟧
(mechanism) After successful setup, `tearDown(self)` runs after the test, even when the test fails. ⟦C.f2 C:tb4 C:tb5⟧
(mechanism) `self.addCleanup(function, *args, **kwargs)` registers actions that run after tearDown or failed setup, in reverse registration order. ⟦C.f3 C:tb4 C:tb5⟧
(mechanism) After acquiring the supplied resource, register its release callable. Store mutable data on self in setUp, not shared class attributes. ⟦C.f4 C:tb4⟧
(misconception) Contrast failed setup with a failed test after successful setup: only the latter runs tearDown, but registered cleanup covers both. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4 C:tb5⟧

### s12 · check · Check: Managing unittest setup and teardown
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, stretch, grading=client] Two tests mutate quantities. Which initialization gives each test fresh mutable state?
  ✔ o1: Assign self.quantities = [3, 2] in setUp before each test.
      why: Define setUp(self) to initialize fresh per-test state before each test method; an error in setUp prevents that test method from running. Register the release callable after acquiring the supplied test resource and store mutable test data on self in setUp rather than in shared class attributes.
  ✘ o2: Store quantities = [3, 2] as a shared class attribute.
      why: The shared class list can retain another test's mutations.
  ✘ o3: Initialize self.quantities only in tearDown.
      why: tearDown runs after the test, so it does not supply fresh initial state before that test.
  feedback✔: Define setUp(self) to initialize fresh per-test state before each test method; an error in setUp prevents that test method from running. Register the release callable after acquiring the supplied test resource and store mutable test data on self in setUp rather than in shared class attributes.  feedback✘: Recheck the evidence against the stated requirement. Define setUp(self) to initialize fresh per-test state before each test method; an error in setUp prevents that test method from running. Register the release callable after acquiring the supplied test resource and store mutable test data on self in setUp rather than in shared class attributes.  hints: ['Trace setup, the test, teardown and registered cleanup as separate phases.']  remediation→r06
  MEASURES: C:initialize_fresh_per_test_mutable_state(f1,f4)   anchors=['assessment:initialize_fresh_per_test_mutable_state']
  taught-before-tested: C.f1←s10; C.f4←s10

### s13 · hands_on · Practice: Managing unittest setup and teardown
Practice — Implement TestCase.setUp to assign fresh self.quantities = [3, 2] and register the supplied release callable immediately after the supplied resource-acquisition step.
QUESTION [code_exercise, stretch, grading=client] The supplied setUp acquires the resource, immediately registers resource_cleanup with addCleanup, and constructs a fresh list from quantity_inputs for each test. Complete resource_cleanup with the release callable (do not call it) and quantity_inputs with supplied_quantities. Preserve the scaffold. The checker verifies independent [3, 2] state and release after normal completion, test failure, and setup failure after registration.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import unittest', 'class declaration inheriting from unittest.TestCase', 'def setUp(self):', 'def tearDown(self):', 'def test_method(self):', 'self.quantities = [3, 2]', 'instance attribute access', 'list indexing and mutation', 'function and method calls', 'self.addCleanup(release)', 'self.addCleanup(function, *args, **kwargs)', 'unittest assertion method calls'] blocked=0 items
  file main.py [editable]:
quantity_input_0 = 3
quantity_input_1 = 2
# Supplied scaffold: preserve this block unchanged.
if True:
    mode = "normal"
    import unittest

    # Supplied in-memory resource only; no filesystem or host resource.
    resource_events = []

    def acquire():
        resource_events.append("acquire")

    def release():
        resource_events.append("release")

    class QuantityTests(unittest.TestCase):
        def setUp(self):
            acquire()
            self.addCleanup(resource_cleanup)
            self.quantities = list(quantity_inputs)

        def test_mutation(self):
            self.assertEqual(self.quantities, [3, 2])
            self.quantities[0] = 0

        def test_fresh_state(self):
            self.assertEqual(self.quantities, [3, 2])

    # The downstream exercise supplies normal/test-failure/setup-failure checks.

supplied_quantities = [quantity_input_0, quantity_input_1]
# TODO: choose a deferred release callable and each setup's initial quantities.
resource_cleanup = None
quantity_inputs = []

  SOLUTION main.py:
quantity_input_0 = 3
quantity_input_1 = 2
# Supplied scaffold: preserve this block unchanged.
if True:
    mode = "normal"
    import unittest

    # Supplied in-memory resource only; no filesystem or host resource.
    resource_events = []

    def acquire():
        resource_events.append("acquire")

    def release():
        resource_events.append("release")

    class QuantityTests(unittest.TestCase):
        def setUp(self):
            acquire()
            self.addCleanup(resource_cleanup)
            self.quantities = list(quantity_inputs)

        def test_mutation(self):
            self.assertEqual(self.quantities, [3, 2])
            self.quantities[0] = 0

        def test_fresh_state(self):
            self.assertEqual(self.quantities, [3, 2])

    # The downstream exercise supplies normal/test-failure/setup-failure checks.

supplied_quantities = [quantity_input_0, quantity_input_1]
# TODO: choose a deferred release callable and each setup's initial quantities.
resource_cleanup = release
quantity_inputs = supplied_quantities

  test test1 (value_equals, visible=True): {"expr":"[(lambda scope: (exec('# Supplied checks: leave unchanged.\\ndef check_lifecycle(mode):\\n    import io\\n    resource_events.clear()\\n    class Probe(QuantityTests):\\n        def setUp(self):\\n            super().setUp()\\n            resource_events.append(\"setup\")\\n            if mode not in (\"normal\", \"test_failure\"):\\n                raise ValueError(\"setup failure\")\\n        def tearDown(self):\\n            resource_events.append(\"teardown\")\\n        def test_pro | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d32f715dbdcfa7198cd807f96b01d24c2dd76fe641020abd03d208938a461d18","tests_passed":1}
  feedback✔: Define setUp(self) to initialize fresh per-test state before each test method; an error in setUp prevents that test method from running. tearDown(self) runs after a test when setUp succeeded, including when the test failed. self.addCleanup(function, *args, **kwargs) registers cleanup that runs after tearDown, or after a failed setUp; registered actions run in reverse registration order. Register the release callable after acquiring the supplied test resource and store mutable test data on self in setUp rather than in shared class attributes.  feedback✘: Recheck the evidence against the stated requirement. Define setUp(self) to initialize fresh per-test state before each test method; an error in setUp prevents that test method from running. tearDown(self) runs after a test when setUp succeeded, including when the test failed. self.addCleanup(function, *args, **kwargs) registers cleanup that runs after tearDown, or after a failed setUp; registered actions run in reverse registration order. Register the release callable after acquiring the supplied test resource and store mutable test data on self in setUp rather than in shared class attributes.  hints: ['Trace setup, the test, teardown and registered cleanup as separate phases.']
  MEASURES: C:trace_setup_test_teardown_and_cleanup_order(f1,f2,f3); C:register_resource_release_for_setup_failure(f3,f4)   anchors=['practice', 'assessment:trace_setup_test_teardown_and_cleanup_order', 'assessment:register_resource_release_for_setup_failure']
  taught-before-tested: C.f1←s10; C.f2←s10; C.f3←s10; C.f3←s10; C.f4←s10

### s14 · recap · Takeaways
Keep these distinctions — 
(takeaway) Use test_* methods with equality, truth and expected-exception assertions for supplied checks. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Distinguish failed assertions from unexpected exceptions; zero tests supply no executed checks. ⟦B.f3 B.f4 B.f5 B:tb1 B:tb3 B:tb4 B:tb5⟧
(takeaway) Fresh setup isolates mutable state; registered cleanup also covers failed setup. ⟦C.f1 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Reading and explaining generated Python: Explain generated code in terms of the stated requirements.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Writing Python unittest test cases
(mechanism) Place the supplied failing operation inside `with self.assertRaises(ExceptionType):` to check its expected exception. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast checking an exception with comparing a return: the failing operation belongs inside assertRaises. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Writing Python unittest test cases
(mechanism) After `import unittest`, subclass `unittest.TestCase` and name methods `test_*` to express individual supplied checks. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Use `self.assertEqual(actual, expected)` for equality and `self.assertTrue(condition)` for a required true condition. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(mechanism) Place the supplied failing operation inside `with self.assertRaises(ExceptionType):` to check its expected exception. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast checking an exception with comparing a return: the failing operation belongs inside assertRaises. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Running unittest and interpreting its results
(mechanism) `python -m unittest test_module` runs a named module; `python -m unittest discover` invokes discovery. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) Discovery defaults to the current directory and `test*.py`; `-s` selects a starting directory and `-p` a filename pattern. ⟦B.f2 B:tb3 B:tb4⟧
(misconception) Contrast a named-module command with discovery: discovery searches using its directory and filename-pattern settings. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4⟧
### r04 · Revisit: Running unittest and interpreting its results
(mechanism) The reported count tells how many tests ran. Zero supplies no executed checks of the helper’s behavior. ⟦B.f5 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast intended discovery with executed checks: a zero count supplies no helper behavior evidence. ⟦B.f5 B:tb1 B:tb3 B:tb4 B:tb5⟧
### r05 · Revisit: Running unittest and interpreting its results
(mechanism) A failure is an unsuccessful assertion. The report identifies the test and failed-assertion traceback. ⟦B.f3 B:tb1 B:tb3 B:tb4 B:tb5⟧
(mechanism) An error is an unexpected exception during a test, rather than an explicitly failed assertion. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast an assertion failure with an unexpected exception; a zero-test report checks neither behavior. ⟦B.f3 B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
### r06 · Revisit: Managing unittest setup and teardown
(mechanism) `setUp(self)` initializes fresh state before each test method; setup errors prevent that method from running. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(mechanism) After acquiring the supplied resource, register its release callable. Store mutable data on self in setUp, not shared class attributes. ⟦C.f4 C:tb3 C:tb4⟧
(misconception) Contrast failed setup with a failed test after successful setup: only the latter runs tearDown, but registered cleanup covers both. ⟦C.f1 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r07 · Revisit: Managing unittest setup and teardown
(mechanism) `setUp(self)` initializes fresh state before each test method; setup errors prevent that method from running. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(mechanism) After successful setup, `tearDown(self)` runs after the test, even when the test fails. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(mechanism) `self.addCleanup(function, *args, **kwargs)` registers actions that run after tearDown or failed setup, in reverse registration order. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(mechanism) After acquiring the supplied resource, register its release callable. Store mutable data on self in setUp, not shared class attributes. ⟦C.f4 C:tb3 C:tb4⟧
(misconception) Contrast failed setup with a failed test after successful setup: only the latter runs tearDown, but registered cleanup covers both. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: def setUpClass(cls):
· constraints.blocked_syntax: def tearDownClass(cls):
· constraints.blocked_syntax: self.addCleanup(...)
· spec.expr: [(lambda scope: (exec('# Supplied checker: leave unchanged. It runs the checks against a candidate helper.\ndef check_tests(multiplier):\n    import unittest, io, ast\n    global cost\n    original = cost\n    def candidate(quantity):\n        if quantity < 0:\n            raise ValueError("negative quantity")\n        return quantity * multiplier\n    cost = candidate\n    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CostTests)\n    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)\n    cost = original\n    tree = ast.parse(open("main.py").read())\n    cls = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "CostTests")\n    equality = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "assertEqual" for n in ast.walk(cls))\n    truth = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "assertTrue" for n in ast.walk(cls))\n    exception = any(isinstance(n, ast.With) and any(isinstance(k, ast.Call) and isinstance(k.func, ast.Name) and k.func.id == "cost" and ast.literal_eval(k.args[0]) == -1 for body in n.body for k in ast.walk(body)) for n in ast.walk(cls))\n    return [result.testsRun, len(result.failures), len(result.errors), equality, truth, exception]\n', scope), scope['check_tests'](multiplier))[1])(globals()), (lambda scope: (exec('# Supplied checker: leave unchanged. It runs the checks against a candidate helper.\ndef check_tests(multiplier):\n    import unittest, io, ast\n    global cost\n    original = cost\n    def candidate(quantity):\n        if quantity < 0:\n            raise ValueError("negative quantity")\n        return quantity * multiplier\n    cost = candidate\n    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CostTests)\n    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)\n    cost = original\n    tree = ast.parse(open("main.py").read())\n    cls = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "CostTests")\n    equality = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "assertEqual" for n in ast.walk(cls))\n    truth = any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "assertTrue" for n in ast.walk(cls))\n    exception = any(isinstance(n, ast.With) and any(isinstance(k, ast.Call) and isinstance(k.func, ast.Name) and k.func.id == "cost" and ast.literal_eval(k.args[0]) == -1 for body in n.body for k in ast.walk(body)) for n in ast.walk(cls))\n    return [result.testsRun, len(result.failures), len(result.errors), equality, truth, exception]\n', scope), scope['check_tests'](multiplier + 1))[1])(globals())]
· constraints.blocked_syntax: def setUpClass(cls):
· constraints.blocked_syntax: def tearDownClass(cls):
· constraints.blocked_syntax: def tearDownModule():
· constraints.blocked_syntax: self.addCleanup(...)
· spec.expr: [(lambda scope: (exec('def run_review(expectation):\n    import io, unittest\n    global expected\n    expected = expectation\n    stream = io.StringIO()\n    result = unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromTestCase(CostTests))\n    source = open("main.py").read()\n    note = "# Review: failure; test_cost; self.assertEqual(cost(0), expected); actual None does not equal expected 0."\n    noted = note in source\n    errors = [str(entry[1]).splitlines()[-1] for entry in result.failures]\n    return [result.testsRun, len(result.failures), len(result.errors), errors, noted]\n', scope), scope['run_review'](expected))[1])(globals()), (lambda scope: (exec('def run_review(expectation):\n    import io, unittest\n    global expected\n    expected = expectation\n    stream = io.StringIO()\n    result = unittest.TextTestRunner(stream=stream).run(unittest.defaultTestLoader.loadTestsFromTestCase(CostTests))\n    source = open("main.py").read()\n    note = "# Review: failure; test_cost; self.assertEqual(cost(0), expected); actual None does not equal expected 0."\n    noted = note in source\n    errors = [str(entry[1]).splitlines()[-1] for entry in result.failures]\n    return [result.testsRun, len(result.failures), len(result.errors), errors, noted]\n', scope), scope['run_review'](None))[1])(globals())]
· expected.value: AssertionError: None != 7
· spec.expr: [(lambda scope: (exec('# Supplied checks: leave unchanged.\ndef check_lifecycle(mode):\n    import io\n    resource_events.clear()\n    class Probe(QuantityTests):\n        def setUp(self):\n            super().setUp()\n            resource_events.append("setup")\n            if mode not in ("normal", "test_failure"):\n                raise ValueError("setup failure")\n        def tearDown(self):\n            resource_events.append("teardown")\n        def test_probe(self):\n            resource_events.append("test")\n            self.assertEqual(self.quantities, [3, 2])\n            if mode == "test_failure":\n                self.fail("supplied failure")\n    result = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.TestSuite([Probe("test_probe")]))\n    events = list(resource_events)\n    a = QuantityTests("test_mutation")\n    b = QuantityTests("test_fresh_state")\n    a.setUp()\n    b.setUp()\n    a.quantities[0] = 0\n    fresh = b.quantities == [3, 2] and a.quantities is not b.quantities\n    a.doCleanups()\n    b.doCleanups()\n    return [events, len(result.failures), len(result.errors), fresh]\n', scope), scope['check_lifecycle'](mode))[1])(globals()), (lambda scope: (exec('# Supplied checks: leave unchanged.\ndef check_lifecycle(mode):\n    import io\n    resource_events.clear()\n    class Probe(QuantityTests):\n        def setUp(self):\n            super().setUp()\n            resource_events.append("setup")\n            if mode not in ("normal", "test_failure"):\n                raise ValueError("setup failure")\n        def tearDown(self):\n            resource_events.append("teardown")\n        def test_probe(self):\n            resource_events.append("test")\n            self.assertEqual(self.quantities, [3, 2])\n            if mode == "test_failure":\n                self.fail("supplied failure")\n    result = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.TestSuite([Probe("test_probe")]))\n    events = list(resource_events)\n    a = QuantityTests("test_mutation")\n    b = QuantityTests("test_fresh_state")\n    a.setUp()\n    b.setUp()\n    a.quantities[0] = 0\n    fresh = b.quantities == [3, 2] and a.quantities is not b.quantities\n    a.doCleanups()\n    b.doCleanups()\n    return [events, len(result.failures), len(result.errors), fresh]\n', scope), scope['check_lifecycle']('test_failure'))[1])(globals()), (lambda scope: (exec('# Supplied checks: leave unchanged.\ndef check_lifecycle(mode):\n    import io\n    resource_events.clear()\n    class Probe(QuantityTests):\n        def setUp(self):\n            super().setUp()\n            resource_events.append("setup")\n            if mode not in ("normal", "test_failure"):\n                raise ValueError("setup failure")\n        def tearDown(self):\n            resource_events.append("teardown")\n        def test_probe(self):\n            resource_events.append("test")\n            self.assertEqual(self.quantities, [3, 2])\n            if mode == "test_failure":\n                self.fail("supplied failure")\n    result = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.TestSuite([Probe("test_probe")]))\n    events = list(resource_events)\n    a = QuantityTests("test_mutation")\n    b = QuantityTests("test_fresh_state")\n    a.setUp()\n    b.setUp()\n    a.quantities[0] = 0\n    fresh = b.quantities == [3, 2] and a.quantities is not b.quantities\n    a.doCleanups()\n    b.doCleanups()\n    return [events, len(result.failures), len(result.errors), fresh]\n', scope), scope['check_lifecycle']('setup_failure'))[1])(globals())]

=========

# EVALUATOR PACKET — Reading and explaining generated Python / Reviewing generated Python file operations for safety / Reviewing untrusted input and arbitrary Python execution (learn_python.tile.110_112)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.read_generated_code — Reading and explaining generated Python
B = python.review_generated_file_operations — Reviewing generated Python file operations for safety
C = python.review_untrusted_input_and_execution — Reviewing untrusted input and arbitrary Python execution

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=7
  warn: remediation step learn_python.tile.110_112.r02 is never referenced
  warn: remediation step learn_python.tile.110_112.r04 is never referenced
  warn: remediation step learn_python.tile.110_112.r06 is never referenced
  warn: remediation step learn_python.tile.110_112.r07 is never referenced
  warn: learn_python.tile.110_112.s03/ix.learn_python.tile.110_112.s03: ADVISORY — syntax descriptors with no detector: ['# comments', '*', '>', 'None', 'assignment', 'function calls', 'function parameters', 'integer literals']
  warn: learn_python.tile.110_112.s07/ix.learn_python.tile.110_112.s07: ADVISORY — syntax descriptors with no detector: ['comments', 'function definitions and calls', 'path joining with /', 'return statements', 'string literals']
  warn: learn_python.tile.110_112.s12/ix.learn_python.tile.110_112.s12: ADVISORY — syntax descriptors with no detector: ['None', 'if statements', 'integer literals', 'less-than comparison', 'string literals', 'try/except ValueError']

## SOURCE FACTS — A (python.read_generated_code)   objective: Explain generated code in terms of the stated requirements.
A.f1: Trace each supplied input through the conditions to its actual return; a path reaching the end of a function without a return produces None.   [sources: think_python#chap06.html#return-values-and-conditionals]
A.f2: Track each assignment and selected branch in order to determine the actual data and control flow for valid and invalid inputs.   [sources: python_language_reference#simple_stmts.html#assignment-statements, python_language_reference#compound_stmts.html#if]
A.f3: Code from a virtual assistant can be mistaken, so check its behavior rather than treating its generated form as proof of correctness.   [sources: think_python#chap01.html#ask-a-virtual-assistant]
note: Begin with this objective: Explain generated code in terms of the stated requirements.
note: Keep the example in the Tracing generated code and checking risky operations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.review_generated_file_operations, python.review_untrusted_input_and_execution, python.verify_generated_api_claims.
PRACTICE ANCHOR (live_code): Annotate how the generated cost helper handles quantity 3 and an invalid quantity of -1, recording the selected branch and actual return for each.  SUCCESS: The annotations show that quantity 3 selects the positive branch and returns 12, while quantity -1 skips that branch and returns None implicitly. They identify the unmet requirement that invalid quantities must return 0.
ASSESSMENT ANCHOR: trace_assignments_branches_and_actual_returns facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_unmet_requirements_in_generated_code facts=['f1', 'f3']

## SOURCE FACTS — B (python.review_generated_file_operations)   objective: Check generated Python code for destructive filesystem behavior.
B.f1: Opening a file in w mode truncates existing content; inspect generated mode choices to identify an unintended overwrite.   [sources: python_stdlib_reference#functions.html#open]
B.f2: Path.unlink() removes the file or symbolic link at that path; remove an unintended unlink call instead of executing it.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path.unlink]
B.f3: Path.rename(target) moves an entry and can replace an existing file on Unix; inspect the actual source and destination paths.   [sources: python_stdlib_reference#pathlib.html#pathlib.Path.rename]
B.f4: An absolute child path replaces a preceding base path, and a relative rename target is interpreted against the working directory; trace these path rules to check the actual destination before execution.   [sources: python_stdlib_reference#pathlib.html#operators, python_stdlib_reference#pathlib.html#pathlib.Path.rename]
note: Begin with this objective: Check generated Python code for destructive filesystem behavior.
note: Keep the example in the Tracing generated code and checking risky operations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.review_untrusted_input_and_execution, python.verify_generated_api_claims, python.review_generated_dependencies.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
note: Require linux.permissions_ownership_and_users and security.access_control_identities_and_permissions before reviewing generated file operations.
PRACTICE ANCHOR (live_code): Review a generated cleanup helper without executing its filesystem operations, and remove an unintended deletion.  SUCCESS: The unintended path.unlink() call is removed, the intended helper behavior is preserved, and review notes identify the overwrite risk and actual rename destination.
ASSESSMENT ANCHOR: identify_unintended_overwrites_from_file_modes facts=['f1']
ASSESSMENT ANCHOR: identify_and_remove_unintended_file_deletions facts=['f2']
ASSESSMENT ANCHOR: trace_actual_source_and_destination_paths_before_execution facts=['f3', 'f4']

## SOURCE FACTS — C (python.review_untrusted_input_and_execution)   objective: Reject unsafe execution of untrusted input in generated Python code.
C.f1: eval evaluates a Python expression and can execute arbitrary code, so it must not be used to process untrusted text.   [sources: python_stdlib_reference#functions.html#eval]
C.f2: exec executes Python code supplied as text or a code object and is unsafe for untrusted instructions.   [sources: python_stdlib_reference#functions.html#exec]
C.f3: Invoking a shell makes quoting and metacharacters a security responsibility; inspect shell=True and untrusted command construction for injection risk.   [sources: python_stdlib_reference#subprocess.html#security-considerations]
C.f4: Replace execution-based parsing with a parser matching the expected data, such as int or float for numeric text and json.loads for JSON, with explicit validation and handling of malformed input.   [sources: python_stdlib_reference#functions.html#int, python_stdlib_reference#functions.html#float, python_stdlib_reference#json.html#json.loads]
C.f5: Non-executing parsing is not unlimited resource safety: impose input-size limits for untrusted JSON because malicious input can consume substantial CPU and memory.   [sources: python_stdlib_reference#json.html#module-json]
note: Begin with this objective: Reject unsafe execution of untrusted input in generated Python code.
note: Keep the example in the Tracing generated code and checking risky operations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.verify_generated_api_claims, python.review_generated_dependencies, python.accept_repair_or_reject_generated_code.
note: Require security.access_control_identities_and_permissions before reviewing untrusted-input execution.
PRACTICE ANCHOR (live_code): Replace a generated eval-based quantity parser with int(text), handle malformed input, and validate that quantity is non-negative without executing untrusted text.  SUCCESS: Valid non-negative integer text produces the expected quantity. Malformed text and negative quantities produce quantity = None without an uncaught conversion error. The repaired parser contains no eval, exec, or shell invocation.
ASSESSMENT ANCHOR: identify_unsafe_execution_of_untrusted_text facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_shell_command_injection_risk facts=['f3']
ASSESSMENT ANCHOR: choose_data_matching_non_executing_parser facts=['f4']
ASSESSMENT ANCHOR: identify_validation_and_resource_limits_for_parsing facts=['f4', 'f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Verifying generated Python API claims

## LESSON, in learner order

### s01 · explainer · Reading and explaining generated Python
Understand — 
(mechanism) Trace each input through the conditions to its actual return. A path reaching the function’s end without return produces None. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Track assignments and selected branches in order for valid and invalid inputs to determine actual data and control flow. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(mechanism) Generated code can be mistaken. Check its behavior; generated form is not proof of correctness. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
[CODE python]
# Requirement: positive quantity returns quantity * 4; nonpositive returns 0.
def cost(quantity):
    if quantity > 0:
        return quantity * 4

print(cost(3))
print(cost(-1))
  annotations: ['Trace the selected branch for each supplied input.', 'Skipping this branch reaches the end without return.']

### s02 · check · Check: Reading and explaining generated Python
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, intro, grading=client] Requirement: cost returns quantity * 4 for positive quantities, and 0 otherwise. Read this generated helper:
```python
def cost(quantity):
    if quantity > 0:
        return quantity * 4
```
Which requirement is unmet?
  ✔ o1: For quantity -1, the positive branch is skipped and the helper implicitly returns None instead of 0.
      why: Trace each supplied input through the conditions to its actual return; a path reaching the end of a function without a return produces None. Code from a virtual assistant can be mistaken, so check its behavior rather than treating its generated form as proof of correctness.
  ✘ o2: For quantity -1, the helper explicitly returns -4.
      why: The multiplication return is only in the positive branch, which -1 skips.
  ✘ o3: No requirement is unmet because the helper was generated.
      why: Generated code can be wrong; reaching the end without return produces None.
  feedback✔: Trace each supplied input through the conditions to its actual return; a path reaching the end of a function without a return produces None. Code from a virtual assistant can be mistaken, so check its behavior rather than treating its generated form as proof of correctness.  feedback✘: Recheck the evidence against the stated requirement. Trace each supplied input through the conditions to its actual return; a path reaching the end of a function without a return produces None. Code from a virtual assistant can be mistaken, so check its behavior rather than treating its generated form as proof of correctness.  hints: ['Follow the selected branch all the way to an actual return or the end of the function.']  remediation→r01
  MEASURES: A:identify_unmet_requirements_in_generated_code(f1,f3)   anchors=['assessment:identify_unmet_requirements_in_generated_code']
  taught-before-tested: A.f1←s01; A.f3←s01

### s03 · hands_on · Practice: Reading and explaining generated Python
Practice — Annotate how the generated cost helper handles quantity 3 and an invalid quantity of -1, recording the selected branch and actual return for each.
QUESTION [code_exercise, core, grading=client] Keep cost unchanged. Assign positive_return = traced_positive and invalid_return = traced_invalid to record actual returns. Add comments starting # Trace positive: and # Trace invalid:. For each, record the input binding, condition result, selected or skipped branch, actual return, and whether it is explicit or implicit. State any mismatch with the requirement that nonpositive quantity returns 0. Use these comment templates, filling each bracketed field from the trace: "# Trace positive: binding quantity = <input>; condition <True/False>; <positive branch/branch skipped>; <explicit/implicit> return <actual>." and "# Trace invalid: binding quantity = <input>; condition <True/False>; <positive branch/branch skipped>; <explicit/implicit> return <actual>; required <required-return> is <met/unmet>." The traced return values and helper calls are supplied scaffolding; complete only the two output bindings and trace comments.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def', 'function parameters', 'function calls', 'if', '>', '*', 'return', 'integer literals', 'None', 'assignment', 'print()', '# comments'] blocked=2 items
  file main.py [editable]:
positive_quantity = 3
invalid_quantity = -1
# Supplied scaffold: preserve this block unchanged.
if True:
    positive_return = None
    invalid_return = None
    # Requirement: positive quantity returns quantity * 4; nonpositive returns 0.
    def cost(quantity):
        if quantity > 0:
            return quantity * 4

    print(cost(positive_quantity))
    print(cost(invalid_quantity))
    traced_positive = cost(positive_quantity)
    traced_invalid = cost(invalid_quantity)
# TODO: annotate bindings, conditions, branches and actual returns; do not repair.

  SOLUTION main.py:
positive_quantity = 3
invalid_quantity = -1
# Supplied scaffold: preserve this block unchanged.
if True:
    positive_return = None
    invalid_return = None
    # Requirement: positive quantity returns quantity * 4; nonpositive returns 0.
    def cost(quantity):
        if quantity > 0:
            return quantity * 4

    print(cost(positive_quantity))
    print(cost(invalid_quantity))
    traced_positive = cost(positive_quantity)
    traced_invalid = cost(invalid_quantity)
# TODO: annotate bindings, conditions, branches and actual returns; do not repair.
# Trace positive: binding quantity = 3; condition True; positive branch; explicit return 12.
# Trace invalid: binding quantity = -1; condition False; branch skipped; implicit return None; required 0 is unmet.
positive_return = traced_positive
invalid_return = traced_invalid

  test test1 (value_equals, visible=True): {"expr":"[positive_return, invalid_return, '# Trace positive: binding quantity = 3; condition True; positive branch; explicit return 12.' in open('main.py').read(), '# Trace invalid: binding quantity = -1; condition False; branch skipped; implicit return None; required 0 is unmet.' in open('main.py').read()]","expected":[12,null,true,true]} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"b332238aa117e726f646b3364be8796be177cae76ab94e3c9878b03d60a00bb6","tests_passed":1}
  feedback✔: Trace each supplied input through the conditions to its actual return; a path reaching the end of a function without a return produces None. Track each assignment and selected branch in order to determine the actual data and control flow for valid and invalid inputs. Code from a virtual assistant can be mistaken, so check its behavior rather than treating its generated form as proof of correctness.  feedback✘: Recheck the evidence against the stated requirement. Trace each supplied input through the conditions to its actual return; a path reaching the end of a function without a return produces None. Track each assignment and selected branch in order to determine the actual data and control flow for valid and invalid inputs. Code from a virtual assistant can be mistaken, so check its behavior rather than treating its generated form as proof of correctness.  hints: ['Follow the selected branch all the way to an actual return or the end of the function.']
  MEASURES: A:trace_assignments_branches_and_actual_returns(f1,f2); A:identify_unmet_requirements_in_generated_code(f1,f3)   anchors=['practice', 'assessment:trace_assignments_branches_and_actual_returns', 'assessment:identify_unmet_requirements_in_generated_code']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f1←s01; A.f3←s01

### s04 · explainer · Reviewing generated Python file operations for safety
Understand — 
(mechanism) Opening in `w` mode truncates existing content. Inspect mode choices for unintended overwrites. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) `Path.unlink()` removes the file or symbolic link at that path. Remove unintended unlink calls instead of executing them. ⟦B.f2 B:tb3⟧
(mechanism) `Path.rename(target)` moves an entry and can replace an existing file on Unix. Inspect source and destination. ⟦B.f3 B:tb1 B:tb3⟧
(mechanism) An absolute child replaces the preceding base path. A relative rename target uses the working directory. Trace actual destinations before execution. ⟦B.f4 B:tb1 B:tb3⟧
[CODE python]
from pathlib import Path

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
  annotations: ['Absolute child replaces the base.', 'w truncates existing content.', 'Remove unintended deletion; do not try it.', 'Relative target uses cwd; Unix can replace an existing file.']

### s05 · explainer · Reviewing generated Python file operations for safety
Understand — 
(mechanism) Opening in `w` mode truncates existing content. Inspect mode choices for unintended overwrites. ⟦B.f1 B:tb4 B:tb5⟧
(mechanism) `Path.unlink()` removes the file or symbolic link at that path. Remove unintended unlink calls instead of executing them. ⟦B.f2 B:tb4⟧
(mechanism) `Path.rename(target)` moves an entry and can replace an existing file on Unix. Inspect source and destination. ⟦B.f3 B:tb4⟧
(mechanism) An absolute child replaces the preceding base path. A relative rename target uses the working directory. Trace actual destinations before execution. ⟦B.f4 B:tb4 B:tb5⟧
(misconception) Contrast a reassuring variable name with the actual mode and resolved path. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s06 · check · Check: Reviewing generated Python file operations for safety
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] On Unix, cwd is /project. Read output = Path("/project") / "/reports/output.txt", source = Path("/project/source.txt"), target = Path("target.txt"), then source.rename(target). Which paths must the review use?
  ✔ o1: Output /reports/output.txt; rename /project/source.txt to /project/target.txt.
      why: Path.rename(target) moves an entry and can replace an existing file on Unix; inspect the actual source and destination paths. An absolute child path replaces a preceding base path, and a relative rename target is interpreted against the working directory; trace these path rules to check the actual destination before execution.
  ✘ o2: Output /project/reports/output.txt; rename /project/source.txt to /project/target.txt.
      why: An absolute child path replaces the preceding base, so output is not under /project.
  ✘ o3: Output /reports/output.txt; rename /project/source.txt to /target.txt.
      why: The relative target is interpreted against /project, the working directory.
  feedback✔: Path.rename(target) moves an entry and can replace an existing file on Unix; inspect the actual source and destination paths. An absolute child path replaces a preceding base path, and a relative rename target is interpreted against the working directory; trace these path rules to check the actual destination before execution.  feedback✘: Recheck the evidence against the stated requirement. Path.rename(target) moves an entry and can replace an existing file on Unix; inspect the actual source and destination paths. An absolute child path replaces a preceding base path, and a relative rename target is interpreted against the working directory; trace these path rules to check the actual destination before execution.  hints: ['Resolve each path and check each operation against what the requirement permits.']  remediation→r03
  MEASURES: B:trace_actual_source_and_destination_paths_before_execution(f3,f4)   anchors=['assessment:trace_actual_source_and_destination_paths_before_execution']
  taught-before-tested: B.f3←s04; B.f4←s04

### s07 · hands_on · Practice: Reviewing generated Python file operations for safety
Practice — Review a generated cleanup helper without executing its filesystem operations, and remove an unintended deletion.
QUESTION [code_exercise, core, grading=client] Never call cleanup_helper. Remove the unintended deletion while preserving the permitted disposable write and source rename. Assign rename_destination = resolved_destination to resolve the relative target without moving anything. Add comments starting # Review mode:, # Review output:, and # Review rename:. Explain the w-mode effect, whether the absolute child preserves the base, the actual output and rename destinations, and Unix existing-destination behavior. The checker reads source; it never executes the proposed filesystem changes. Use these exact note forms with your chosen findings: "# Review mode: w <preserves/truncates> existing output content.", "# Review output: <absolute child replaces base/base retained>; <output-path>.", and "# Review rename: relative target uses <cwd/base>; <destination>; Unix <may replace/never replaces> an existing destination file." The helper is now supplied as commented review-only source; remove its commented unintended deletion, not any real file. The path resolution is supplied; preserve resolved_destination unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['from pathlib import Path', 'variable assignment', 'string literals', 'function definitions and calls', 'return statements', 'comments', 'with open(output, "w") as file', 'file.write()', 'Path()', 'path joining with /', 'path.unlink()', 'source.rename(target)'] blocked=4 items
  file main.py [editable]:
rename_destination = None
cwd = "/project"
from pathlib import Path

# Fictional review state, not provisioned files:
# cwd: /project; /reports/output.txt already contains a disposable report.
# /project/target.txt exists. /project/preserve.txt must be preserved.
# Writing disposable output and moving source to /project/target.txt are permitted.
# Do NOT call this helper. Review its proposed effects and remove unintended deletion.
# Proposed helper (review-only; never executed):
# def cleanup_helper():
#     output = Path("/project") / "/reports/output.txt"
#     path = Path("/project/preserve.txt")
#     source = Path("/project/source.txt")
#     target = Path("target.txt")
#     with open(output, "w") as file:
#         file.write("report")
#     path.unlink()
#     source.rename(target)
#     return output

resolved_destination = Path(cwd) / "target.txt"
# TODO: remove the unintended unlink and add mode/path/Unix replacement notes.

  SOLUTION main.py:
rename_destination = None
cwd = "/project"
from pathlib import Path

# Fictional review state, not provisioned files:
# cwd: /project; /reports/output.txt already contains a disposable report.
# /project/target.txt exists. /project/preserve.txt must be preserved.
# Writing disposable output and moving source to /project/target.txt are permitted.
# Do NOT call this helper. Review its proposed effects and remove unintended deletion.
# Proposed helper (review-only; never executed):
# def cleanup_helper():
#     output = Path("/project") / "/reports/output.txt"
#     path = Path("/project/preserve.txt")
#     source = Path("/project/source.txt")
#     target = Path("target.txt")
#     with open(output, "w") as file:
#         file.write("report")
#     source.rename(target)
#     return output

resolved_destination = Path(cwd) / "target.txt"
# TODO: remove the unintended unlink and add mode/path/Unix replacement notes.
# Review mode: w truncates existing output content.
# Review output: absolute child replaces base; /reports/output.txt.
# Review rename: relative target uses cwd; /project/target.txt; Unix may replace an existing destination file.
rename_destination = resolved_destination

  test test1 (value_equals, visible=True): {"expr":"[str(rename_destination), not any(isinstance(n, __import__('ast').Call) and isinstance(n.func, __import__('ast').Attribute) and n.func.attr == 'unlink' for n in __import__('ast').walk(__import__('ast').parse('\\n'.join(line[2:] for line in open('main.py').read().splitlines() if line.startswith('# ') and (line.startswith('# def cleanup_helper') or line.startswith('#     ')))))), '# Review mode: w truncates existing output content.' in open('main.py').read(), '# Review output: absolute ch | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"daacef01fa3e386a46434950af8a7a45a563b4016e0eeb60d3c2988913e2e502","tests_passed":1}
  feedback✔: Opening a file in w mode truncates existing content; inspect generated mode choices to identify an unintended overwrite. Path.unlink() removes the file or symbolic link at that path; remove an unintended unlink call instead of executing it. Path.rename(target) moves an entry and can replace an existing file on Unix; inspect the actual source and destination paths. An absolute child path replaces a preceding base path, and a relative rename target is interpreted against the working directory; trace these path rules to check the actual destination before execution.  feedback✘: Recheck the evidence against the stated requirement. Opening a file in w mode truncates existing content; inspect generated mode choices to identify an unintended overwrite. Path.unlink() removes the file or symbolic link at that path; remove an unintended unlink call instead of executing it. Path.rename(target) moves an entry and can replace an existing file on Unix; inspect the actual source and destination paths. An absolute child path replaces a preceding base path, and a relative rename target is interpreted against the working directory; trace these path rules to check the actual destination before execution.  hints: ['Resolve each path and check each operation against what the requirement permits.']
  MEASURES: B:identify_unintended_overwrites_from_file_modes(f1); B:identify_and_remove_unintended_file_deletions(f2); B:trace_actual_source_and_destination_paths_before_execution(f3,f4)   anchors=['practice', 'assessment:identify_unintended_overwrites_from_file_modes', 'assessment:identify_and_remove_unintended_file_deletions', 'assessment:trace_actual_source_and_destination_paths_before_execution']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04

### s08 · explainer · Reviewing untrusted input and arbitrary Python execution
Understand — 
(mechanism) `eval` evaluates Python expressions and can execute arbitrary code; do not use it for untrusted text. ⟦C.f1 C:tb1 C:tb2⟧
(mechanism) `exec` executes supplied text or code objects and is unsafe for untrusted instructions. ⟦C.f2 C:tb1 C:tb3⟧
(mechanism) A shell makes quoting and metacharacters a security responsibility. Inspect `shell=True` and untrusted command construction for injection risk. ⟦C.f3 C:tb3⟧
(mechanism) Replace execution-based parsing with a matching parser: int or float for numeric text, json.loads for JSON. Validate values and handle malformed input. ⟦C.f4 C:tb1 C:tb3⟧
(mechanism) Non-executing parsing is not unlimited resource safety. Limit untrusted JSON input size: malicious input can consume substantial CPU and memory. ⟦C.f5 C:tb3⟧
[CODE python]
text = "3"
quantity = None
# Rejected, non-executable proposal: quantity = eval(text)
# Requirement: a nonnegative integer; malformed/negative text leaves quantity None.
try:
    parsed = int(text)
except ValueError:
    quantity = None
else:
    if parsed >= 0:
        quantity = parsed
  annotations: ['Unsafe execution proposal: review only.', 'Parse numeric text; handle malformed input.', 'Validate the required nonnegative value.']

### s09 · explainer · Reviewing untrusted input and arbitrary Python execution
Understand — 
(mechanism) `eval` evaluates Python expressions and can execute arbitrary code; do not use it for untrusted text. ⟦C.f1 C:tb4 C:tb5⟧
(mechanism) `exec` executes supplied text or code objects and is unsafe for untrusted instructions. ⟦C.f2 C:tb4 C:tb5⟧
(mechanism) A shell makes quoting and metacharacters a security responsibility. Inspect `shell=True` and untrusted command construction for injection risk. ⟦C.f3 C:tb4⟧
(mechanism) Replace execution-based parsing with a matching parser: int or float for numeric text, json.loads for JSON. Validate values and handle malformed input. ⟦C.f4 C:tb4⟧
(mechanism) Non-executing parsing is not unlimited resource safety. Limit untrusted JSON input size: malicious input can consume substantial CPU and memory. ⟦C.f5 C:tb4 C:tb5⟧
(misconception) Contrast parsing data with executing instructions; a non-executing parser still needs validation and resource limits. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4 C:tb5⟧

### s10 · check · Check: Reviewing untrusted input and arbitrary Python execution
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] Read the proposal:
```python
subprocess.run("report " + text, shell=True)
```
text is untrusted. What requires rejection or correction before execution?
  ✔ o1: Shell invocation with untrusted command construction creates injection risk.
      why: Invoking a shell makes quoting and metacharacters a security responsibility; inspect shell=True and untrusted command construction for injection risk.
  ✘ o2: The shell guarantees untrusted text is treated only as data.
      why: Shell quoting and metacharacters are a security responsibility, not an automatic guarantee.
  ✘ o3: Only eval can execute unsafe untrusted input; this proposal is safe.
      why: Shell invocation is a separate execution risk from eval.
  feedback✔: Invoking a shell makes quoting and metacharacters a security responsibility; inspect shell=True and untrusted command construction for injection risk.  feedback✘: Recheck the evidence against the stated requirement. Invoking a shell makes quoting and metacharacters a security responsibility; inspect shell=True and untrusted command construction for injection risk.  hints: ['Distinguish interpreting data from executing instructions, then review rejection behavior.']  remediation→r05
  MEASURES: C:identify_shell_command_injection_risk(f3)   anchors=['assessment:identify_shell_command_injection_risk']
  taught-before-tested: C.f3←s08

### s11 · check · Check: Reviewing untrusted input and arbitrary Python execution
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, stretch, grading=client] A proposal uses json.loads on untrusted JSON. Which additional review is needed?
  ✔ o1: Handle malformed input, validate the parsed data, and impose an input-size limit.
      why: Replace execution-based parsing with a parser matching the expected data, such as int or float for numeric text and json.loads for JSON, with explicit validation and handling of malformed input. Non-executing parsing is not unlimited resource safety: impose input-size limits for untrusted JSON because malicious input can consume substantial CPU and memory.
  ✘ o2: No other checks: a non-executing parser guarantees unlimited resource safety.
      why: Malicious JSON can consume substantial CPU and memory despite non-executing parsing.
  ✘ o3: Use eval instead so malformed input is handled automatically.
      why: eval can execute arbitrary code and is not a safe replacement for JSON parsing.
  feedback✔: Replace execution-based parsing with a parser matching the expected data, such as int or float for numeric text and json.loads for JSON, with explicit validation and handling of malformed input. Non-executing parsing is not unlimited resource safety: impose input-size limits for untrusted JSON because malicious input can consume substantial CPU and memory.  feedback✘: Recheck the evidence against the stated requirement. Replace execution-based parsing with a parser matching the expected data, such as int or float for numeric text and json.loads for JSON, with explicit validation and handling of malformed input. Non-executing parsing is not unlimited resource safety: impose input-size limits for untrusted JSON because malicious input can consume substantial CPU and memory.  hints: ['Distinguish interpreting data from executing instructions, then review rejection behavior.']
  MEASURES: C:identify_validation_and_resource_limits_for_parsing(f4,f5)   anchors=['assessment:identify_validation_and_resource_limits_for_parsing']
  taught-before-tested: C.f4←s08; C.f5←s08

### s12 · hands_on · Practice: Reviewing untrusted input and arbitrary Python execution
Practice — Replace a generated eval-based quantity parser with int(text), handle malformed input, and validate that quantity is non-negative without executing untrusted text.
QUESTION [code_exercise, stretch, grading=client] Complete convert with the int callable, not evaluated input text. Preserve the supplied try/except ValueError and explicit nonnegative validation block, which invokes convert(text) and leaves quantity None for malformed or negative text. Keep text unchanged. The checker runs fresh valid, zero, malformed and negative inputs and rejects eval, exec and shell invocation.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'integer literals', 'None', 'int(text)', 'try/except ValueError', 'if statements', 'less-than comparison'] blocked=0 items
  file main.py [editable]:
text = "3"
quantity = None
# Rejected, non-executable proposal: quantity = eval(text)
# Requirement: a nonnegative integer; malformed/negative text leaves quantity None.
# TODO: select the safe integer conversion callable.
convert = None
# Supplied scaffold: preserve this block unchanged.
if True:
    try:
        quantity = convert(text)
        if quantity < 0:
            quantity = None
    except ValueError:
        quantity = None

  SOLUTION main.py:
text = "3"
quantity = None
# Rejected, non-executable proposal: quantity = eval(text)
# Requirement: a nonnegative integer; malformed/negative text leaves quantity None.
# TODO: use int(text), catch ValueError, and validate quantity explicitly.
# TODO: select the safe integer conversion callable.
convert = int
# Supplied scaffold: preserve this block unchanged.
if True:
    try:
        quantity = convert(text)
        if quantity < 0:
            quantity = None
    except ValueError:
        quantity = None

  test test1 (value_equals, visible=True): {"expr":"[(lambda scope: (exec('# Supplied fresh-run checker; leave unchanged.\\ndef check_parse(candidate):\\n    import ast\\n    source = open(\"main.py\").read()\\n    tree = ast.parse(source)\\n    body = [n for n in tree.body if not isinstance(n, ast.FunctionDef)]\\n    scope = {\"text\": candidate}\\n    body = [n for n in body if not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == \"text\" for t in n.targets))]\\n    exec(compile(ast.Module(body=body, type_ignores= | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e89f3583f7c3f94f24b5ddb67bed3a5fe675bda40957626fc0abed5dba87034d","tests_passed":1}
  feedback✔: eval evaluates a Python expression and can execute arbitrary code, so it must not be used to process untrusted text. exec executes Python code supplied as text or a code object and is unsafe for untrusted instructions. Replace execution-based parsing with a parser matching the expected data, such as int or float for numeric text and json.loads for JSON, with explicit validation and handling of malformed input.  feedback✘: Recheck the evidence against the stated requirement. eval evaluates a Python expression and can execute arbitrary code, so it must not be used to process untrusted text. exec executes Python code supplied as text or a code object and is unsafe for untrusted instructions. Replace execution-based parsing with a parser matching the expected data, such as int or float for numeric text and json.loads for JSON, with explicit validation and handling of malformed input.  hints: ['Distinguish interpreting data from executing instructions, then review rejection behavior.']
  MEASURES: C:identify_unsafe_execution_of_untrusted_text(f1,f2); C:choose_data_matching_non_executing_parser(f4)   anchors=['practice', 'assessment:identify_unsafe_execution_of_untrusted_text', 'assessment:choose_data_matching_non_executing_parser']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f4←s08

### s13 · recap · Takeaways
Keep these distinctions — 
(takeaway) Trace actual branches and returns; reaching the end without return produces None. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Inspect modes and resolved paths; remove unintended deletion before execution. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Parse matching data instead of executing untrusted text; validate inputs and limit untrusted JSON size. ⟦C.f1 C.f2 C.f4 C.f5 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Verifying generated Python API claims: Check generated Python API claims in authoritative documentation.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Reading and explaining generated Python
(mechanism) Trace each input through the conditions to its actual return. A path reaching the function’s end without return produces None. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Generated code can be mistaken. Check its behavior; generated form is not proof of correctness. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast intended behavior in a requirement with the path the helper actually takes. ⟦A.f1 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Reading and explaining generated Python
(mechanism) Trace each input through the conditions to its actual return. A path reaching the function’s end without return produces None. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Track assignments and selected branches in order for valid and invalid inputs to determine actual data and control flow. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(mechanism) Generated code can be mistaken. Check its behavior; generated form is not proof of correctness. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast intended behavior in a requirement with the path the helper actually takes. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Reviewing generated Python file operations for safety
(mechanism) `Path.rename(target)` moves an entry and can replace an existing file on Unix. Inspect source and destination. ⟦B.f3 B:tb1 B:tb3 B:tb4⟧
(mechanism) An absolute child replaces the preceding base path. A relative rename target uses the working directory. Trace actual destinations before execution. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a reassuring variable name with the actual mode and resolved path. ⟦B.f3 B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit: Reviewing generated Python file operations for safety
(mechanism) Opening in `w` mode truncates existing content. Inspect mode choices for unintended overwrites. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(mechanism) `Path.unlink()` removes the file or symbolic link at that path. Remove unintended unlink calls instead of executing them. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) `Path.rename(target)` moves an entry and can replace an existing file on Unix. Inspect source and destination. ⟦B.f3 B:tb1 B:tb3 B:tb4⟧
(mechanism) An absolute child replaces the preceding base path. A relative rename target uses the working directory. Trace actual destinations before execution. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a reassuring variable name with the actual mode and resolved path. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Revisit: Reviewing untrusted input and arbitrary Python execution
(mechanism) A shell makes quoting and metacharacters a security responsibility. Inspect `shell=True` and untrusted command construction for injection risk. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) Contrast parsing data with constructing a shell command: shell quoting and metacharacters create an injection responsibility. ⟦C.f3 C:tb3 C:tb4⟧
### r06 · Revisit: Reviewing untrusted input and arbitrary Python execution
(mechanism) Replace execution-based parsing with a matching parser: int or float for numeric text, json.loads for JSON. Validate values and handle malformed input. ⟦C.f4 C:tb1 C:tb3 C:tb4⟧
(mechanism) Non-executing parsing is not unlimited resource safety. Limit untrusted JSON input size: malicious input can consume substantial CPU and memory. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast parsing data with executing instructions; a non-executing parser still needs validation and resource limits. ⟦C.f4 C.f5 C:tb1 C:tb3 C:tb4 C:tb5⟧
### r07 · Revisit: Reviewing untrusted input and arbitrary Python execution
(mechanism) `eval` evaluates Python expressions and can execute arbitrary code; do not use it for untrusted text. ⟦C.f1 C:tb1 C:tb2 C:tb4 C:tb5⟧
(mechanism) `exec` executes supplied text or code objects and is unsafe for untrusted instructions. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(mechanism) Replace execution-based parsing with a matching parser: int or float for numeric text, json.loads for JSON. Validate values and handle malformed input. ⟦C.f4 C:tb1 C:tb3 C:tb4⟧
(misconception) Contrast parsing data with executing instructions; a non-executing parser still needs validation and resource limits. ⟦C.f1 C.f2 C.f4 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expr: [str(rename_destination), not any(isinstance(n, __import__('ast').Call) and isinstance(n.func, __import__('ast').Attribute) and n.func.attr == 'unlink' for n in __import__('ast').walk(__import__('ast').parse('\n'.join(line[2:] for line in open('main.py').read().splitlines() if line.startswith('# ') and (line.startswith('# def cleanup_helper') or line.startswith('#     ')))))), '# Review mode: w truncates existing output content.' in open('main.py').read(), '# Review output: absolute child replaces base; /reports/output.txt.' in open('main.py').read(), '# Review rename: relative target uses cwd; /project/target.txt; Unix may replace an existing destination file.' in open('main.py').read(), __import__('ast').dump(next(n for n in __import__('ast').parse('\n'.join(line[2:] for line in open('main.py').read().splitlines() if line.startswith('# ') and (line.startswith('# def cleanup_helper') or line.startswith('#     ')))).body if isinstance(n, __import__('ast').FunctionDef) and n.name == 'cleanup_helper')) == __import__('ast').dump(__import__('ast').parse("def cleanup_helper():\n    output = Path('/project') / '/reports/output.txt'\n    path = Path('/project/preserve.txt')\n    source = Path('/project/source.txt')\n    target = Path('target.txt')\n    with open(output, 'w') as file:\n        file.write('report')\n    source.rename(target)\n    return output").body[0])]
· expected.value: /project_x/target.txt
· spec.expr: [(lambda scope: (exec('# Supplied fresh-run checker; leave unchanged.\ndef check_parse(candidate):\n    import ast\n    source = open("main.py").read()\n    tree = ast.parse(source)\n    body = [n for n in tree.body if not isinstance(n, ast.FunctionDef)]\n    scope = {"text": candidate}\n    body = [n for n in body if not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "text" for t in n.targets))]\n    exec(compile(ast.Module(body=body, type_ignores=[]), "parser", "exec"), scope)\n    unsafe = any(isinstance(n, ast.Call) and ((isinstance(n.func, ast.Name) and n.func.id in ("eval", "exec")) or (isinstance(n.func, ast.Attribute) and n.func.attr in ("run", "system", "Popen"))) for node in body for n in ast.walk(node))\n    return [scope["quantity"], unsafe]\n', scope), scope['check_parse'](text))[1])(globals()), (lambda scope: (exec('# Supplied fresh-run checker; leave unchanged.\ndef check_parse(candidate):\n    import ast\n    source = open("main.py").read()\n    tree = ast.parse(source)\n    body = [n for n in tree.body if not isinstance(n, ast.FunctionDef)]\n    scope = {"text": candidate}\n    body = [n for n in body if not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "text" for t in n.targets))]\n    exec(compile(ast.Module(body=body, type_ignores=[]), "parser", "exec"), scope)\n    unsafe = any(isinstance(n, ast.Call) and ((isinstance(n.func, ast.Name) and n.func.id in ("eval", "exec")) or (isinstance(n.func, ast.Attribute) and n.func.attr in ("run", "system", "Popen"))) for node in body for n in ast.walk(node))\n    return [scope["quantity"], unsafe]\n', scope), scope['check_parse']('0'))[1])(globals()), (lambda scope: (exec('# Supplied fresh-run checker; leave unchanged.\ndef check_parse(candidate):\n    import ast\n    source = open("main.py").read()\n    tree = ast.parse(source)\n    body = [n for n in tree.body if not isinstance(n, ast.FunctionDef)]\n    scope = {"text": candidate}\n    body = [n for n in body if not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "text" for t in n.targets))]\n    exec(compile(ast.Module(body=body, type_ignores=[]), "parser", "exec"), scope)\n    unsafe = any(isinstance(n, ast.Call) and ((isinstance(n.func, ast.Name) and n.func.id in ("eval", "exec")) or (isinstance(n.func, ast.Attribute) and n.func.attr in ("run", "system", "Popen"))) for node in body for n in ast.walk(node))\n    return [scope["quantity"], unsafe]\n', scope), scope['check_parse']('bad'))[1])(globals()), (lambda scope: (exec('# Supplied fresh-run checker; leave unchanged.\ndef check_parse(candidate):\n    import ast\n    source = open("main.py").read()\n    tree = ast.parse(source)\n    body = [n for n in tree.body if not isinstance(n, ast.FunctionDef)]\n    scope = {"text": candidate}\n    body = [n for n in body if not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "text" for t in n.targets))]\n    exec(compile(ast.Module(body=body, type_ignores=[]), "parser", "exec"), scope)\n    unsafe = any(isinstance(n, ast.Call) and ((isinstance(n.func, ast.Name) and n.func.id in ("eval", "exec")) or (isinstance(n.func, ast.Attribute) and n.func.attr in ("run", "system", "Popen"))) for node in body for n in ast.walk(node))\n    return [scope["quantity"], unsafe]\n', scope), scope['check_parse']('-1'))[1])(globals())]

=========

# EVALUATOR PACKET — Verifying generated Python API claims / Reviewing generated Python dependency suggestions / Accepting, repairing or rejecting generated Python on evidence (learn_python.tile.113_115)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.verify_generated_api_claims — Verifying generated Python API claims
B = python.review_generated_dependencies — Reviewing generated Python dependency suggestions
C = python.accept_repair_or_reject_generated_code — Accepting, repairing or rejecting generated Python on evidence

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step learn_python.tile.113_115.r02 is never referenced
  warn: remediation step learn_python.tile.113_115.r04 is never referenced
  warn: remediation step learn_python.tile.113_115.r06 is never referenced
  warn: learn_python.tile.113_115.s12/ix.learn_python.tile.113_115.s12: ADVISORY — syntax descriptors with no detector: ['None', 'assert statements', 'function calls', 'function definitions with def', 'function parameters', 'numeric literals', 'return statements', 'string literals']

## SOURCE FACTS — A (python.verify_generated_api_claims)   objective: Check generated Python API claims in authoritative documentation.
A.f1: An official API entry such as sorted documents its signature, keyword-only options and returned value; compare a generated call’s name, arguments and expected result to those documented elements.   [sources: python_stdlib_reference#functions.html#sorted]
A.f2: Virtual assistants can make mistakes even about Python, so their plausible API claims need checking.   [sources: think_python#chap01.html#ask-a-virtual-assistant]
A.f3: help(object) displays documentation for an available object, supporting inspection of its actual interface in the selected runtime.   [sources: python_stdlib_reference#functions.html#help]
A.f4: Check the executing interpreter’s version when comparing an API claim to version-specific documentation.   [sources: python_stdlib_reference#sys.html#sys.version]
note: Begin with this objective: Check generated Python API claims in authoritative documentation.
note: Keep the example in the Verifying claims and making acceptance decisions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.review_generated_dependencies, python.accept_repair_or_reject_generated_code.
PRACTICE ANCHOR (live_code): Check the generated call sorted(records, key=quantity_key, reverse=True) against the official reference documentation and help(sorted) in the selected interpreter.  SUCCESS: Identify the executing interpreter's version, confirm that sorted exists, and explain how the proposed arguments and expected result match its documented interface: key and reverse are keyword-only options, and sorted returns a new sorted list.
ASSESSMENT ANCHOR: verify_api_existence_and_documented_interface facts=['f1', 'f3']
ASSESSMENT ANCHOR: compare_generated_arguments_and_expected_return_to_documentation facts=['f1']
ASSESSMENT ANCHOR: match_reference_documentation_to_executing_interpreter_version facts=['f4']

## SOURCE FACTS — B (python.review_generated_dependencies)   objective: Verify suggested dependencies before installation.
B.f1: pip installs from the Python Package Index by default; browse that index to check the actual named distribution rather than installing an unchecked suggestion.   [sources: python_tutorial#venv.html#managing-packages-with-pip]
B.f2: An installable distribution package and an import package need not have the same name; confirm the distribution name from the project’s installation documentation.   [sources: python_packaging_user_guide#discussions/distribution-package-vs-import-package/#what-are-the-links-between-distribution-packages-and-import-packages]
B.f3: An --index-url changes the package index used for installation; inspect a proposed install command’s source as well as its name.   [sources: python_packaging_user_guide#installing-from-other-indexes]
B.f4: The Python standard library supplies modules for many common tasks; check whether documented standard-library functionality already meets the requirement before adding a third-party dependency.   [sources: python_tutorial#stdlib.html]
B.f5: Assistant output can contain mistakes; withhold installation of a dependency suggestion whose identity and documented use cannot be verified.   [sources: think_python#chap01.html#ask-a-virtual-assistant]
note: Begin with this objective: Verify suggested dependencies before installation.
note: Keep the example in the Verifying claims and making acceptance decisions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.accept_repair_or_reject_generated_code.
PRACTICE ANCHOR (external_proof): Review a generated dependency suggestion against the Python Package Index and project installation documentation. Check its distribution identity, documented import name, installation source and necessity, and reject an unverifiable package name without installing it.  SUCCESS: The review records the evidence checked, distinguishes the distribution name from the import name, identifies whether --index-url changes the installation source, and checks documented standard-library alternatives. It rejects the unverifiable suggestion and leaves it uninstalled.
ASSESSMENT ANCHOR: verify_distribution_identity_against_index_and_documentation facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_proposed_installation_source facts=['f3']
ASSESSMENT ANCHOR: check_dependency_necessity_against_standard_library_functionality facts=['f4']
ASSESSMENT ANCHOR: withhold_installation_of_unverifiable_dependency facts=['f5']

## SOURCE FACTS — C (python.accept_repair_or_reject_generated_code)   objective: Decide whether generated Python code is acceptable using evidence.
C.f1: Generated code can be wrong; test code obtained from a virtual assistant rather than accepting it solely because it was generated.   [sources: think_python#chap01.html#ask-a-virtual-assistant]
C.f2: Use the supplied failed assertions and unexpected exceptions to identify behavior requiring correction; these results do not support accepting the helper unchanged.   [sources: python_stdlib_reference#unittest.html#unittest.TestResult.failures, python_stdlib_reference#unittest.html#unittest.TestResult.errors]
C.f3: Compare traced returns and supplied test expectations with the required behavior; record acceptance only for behavior supported by that evidence, and record correction when a mismatch can be addressed.   [sources: think_python#chap06.html#return-values-and-conditionals, python_stdlib_reference#unittest.html#basic-example]
C.f4: Reject execution of a proposed implementation that evaluates untrusted input or truncates a file contrary to the requirements until those unsafe operations are removed or corrected.   [sources: python_stdlib_reference#functions.html#eval, python_stdlib_reference#functions.html#open]
note: Begin with this objective: Decide whether generated Python code is acceptable using evidence.
note: Keep the example in the Verifying claims and making acceptance decisions tile focused on this operation, rather than introducing additional capabilities.
note: Require testing.write_unit_tests_with_assertions and testing.test_edge_cases_and_failures before applying the supplied checks. This unit does not supply the external testing foundations.
PRACTICE ANCHOR (live_code): Review supplied versions of the cost helper against their requirements, traced returns, safety findings and test results. Record an accept, correct or reject decision with an evidence-based justification for each version, without executing unsafe proposals.  SUCCESS: Recorded decisions accept only behavior supported by the supplied evidence, require correction for addressable mismatches or unexpected failures, and reject execution when untrusted input is evaluated or a file is truncated contrary to requirements.
ASSESSMENT ANCHOR: justify_acceptance_from_requirements_and_test_evidence facts=['f1', 'f3']
ASSESSMENT ANCHOR: justify_correction_from_failures_and_behavior_mismatches facts=['f2', 'f3']
ASSESSMENT ANCHOR: justify_rejection_of_unsafe_execution facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Reviewing generated Python dependency suggestions

## LESSON, in learner order

### s01 · explainer · Verifying generated Python API claims
Understand — 
(mechanism) Compare a generated call’s name, arguments and expected result with the official API entry’s signature, keyword-only options and returned value. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Assistants can make mistakes about Python; plausible API claims need checking. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) `help(object)` displays documentation for an available object, supporting inspection of its interface in the selected runtime. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) Check the executing interpreter’s version before comparing version-specific documentation. ⟦A.f4 A:tb1 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Plausible wording is not an API specification. left_label: Proposed call | right_label: Executing version and documented interface
  left:
[CODE python]
sorted(records, key=quantity_key, reverse=True)
  annotations: ['records supplies the iterable; quantity_key supplies the key function; reverse=True requests descending order. key and reverse are keyword-only options. sorted returns a new sorted list.']
  right:
[CODE python]
import sys
print(sys.version)
help(sorted)
  annotations: ['Inspect available-object documentation; match the executing interpreter version.']

### s02 · check · Check: Verifying generated Python API claims
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, intro, grading=client] A generated snippet was checked against a Python documentation version different from the executing interpreter. What should the API review do?
  ✔ o1: Match the reference documentation version to the executing interpreter, then check the documented interface.
      why: Check the executing interpreter’s version when comparing an API claim to version-specific documentation.
  ✘ o2: Accept the snippet because the function name looks familiar.
      why: A familiar-looking name does not establish existence or the interface in the executing version.
  ✘ o3: Check only that the snippet parses; the documentation version does not matter.
      why: Parsing alone does not confirm the version-specific API or call interface.
  feedback✔: Check the executing interpreter’s version when comparing an API claim to version-specific documentation.  feedback✘: Recheck the evidence against the stated requirement. Check the executing interpreter’s version when comparing an API claim to version-specific documentation.  hints: ['Compare the supplied signature and return description with the claim, including the reference version.']  remediation→r01
  MEASURES: A:match_reference_documentation_to_executing_interpreter_version(f4)   anchors=['assessment:match_reference_documentation_to_executing_interpreter_version']
  taught-before-tested: A.f4←s01

### s03 · hands_on · Review generated Python API claims
Practice — Read the supplied excerpts in this step and judge which claims or proposed actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each review excerpt and decide whether the API claim is supported by the supplied version-matched documentation evidence. The documented signature is sorted(iterable, /, *, key=None, reverse=False); the result is a new list. No documentation lookup or code execution is required.
  'Interpreter and reference: matching Python version. Documented name: sorted. Code: result = sorted(values, key=quantity_key, reverse=True). Claim: result is a new list; values is not sorted in place. Review evidence: signature and return description match.' -> Conclusion supported
      feedback: The name, positional iterable, keyword-only options, new-list return, and version match the supplied documentation.
  'Interpreter and reference: matching Python version. Code: result = sorted(values, quantity_key). Claim: the second positional argument supplies key. Review evidence: key follows * in the documented signature.' -> Conclusion not supported
      feedback: key is keyword-only; this argument placement does not match the documented interface.
  'Interpreter and reference: matching Python version. Code: result = sorted(values). Claim: the API sorts values in place and returns None. Review evidence: sorted returns a new list.' -> Conclusion not supported
      feedback: The expected return and in-place claim conflict with the documented new-list return.
  'Interpreter: one Python version; reference: a different version. The generated name and arguments have not been checked in the executing version. Review conclusion: verified for this interpreter.' -> Conclusion not supported
      feedback: A different reference version is not the version-matched evidence required for this conclusion.
  feedback✔: An official API entry such as sorted documents its signature, keyword-only options and returned value; compare a generated call’s name, arguments and expected result to those documented elements. help(object) displays documentation for an available object, supporting inspection of its actual interface in the selected runtime. Check the executing interpreter’s version when comparing an API claim to version-specific documentation.  feedback✘: Recheck the evidence against the stated requirement. An official API entry such as sorted documents its signature, keyword-only options and returned value; compare a generated call’s name, arguments and expected result to those documented elements. help(object) displays documentation for an available object, supporting inspection of its actual interface in the selected runtime. Check the executing interpreter’s version when comparing an API claim to version-specific documentation.  hints: ['Compare the supplied signature and return description with the claim, including the reference version.']
  MEASURES: A:verify_api_existence_and_documented_interface(f1,f3); A:compare_generated_arguments_and_expected_return_to_documentation(f1); A:match_reference_documentation_to_executing_interpreter_version(f4)   anchors=['practice', 'assessment:verify_api_existence_and_documented_interface', 'assessment:compare_generated_arguments_and_expected_return_to_documentation', 'assessment:match_reference_documentation_to_executing_interpreter_version']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f1←s01; A.f4←s01

### s04 · explainer · Reviewing generated Python dependency suggestions
Understand — 
(mechanism) pip uses the Python Package Index by default. Browse it to check the named distribution before installing an unchecked suggestion. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Distribution and import package names need not match. Confirm the distribution in the project’s installation documentation. ⟦B.f2 B:tb3⟧
(mechanism) `--index-url` changes the package index. Inspect the installation source as well as the name. ⟦B.f3 B:tb1 B:tb3⟧
(mechanism) The standard library supplies modules for many common tasks. Check whether documented functionality meets the requirement before adding a dependency. ⟦B.f4 B:tb3⟧
(mechanism) Assistant suggestions can be mistaken. Withhold installation when identity and documented use cannot be verified. ⟦B.f5 B:tb1 B:tb3⟧
[SIDE_BY_SIDE] Read-only comparison: <proposed_distribution>, <proposed_index> and <proposed_import> are placeholders, not verified package names. Verify before installation; do not install an unverifiable suggestion. left_label: Illustrative proposal — placeholders, not verified package names | right_label: Supplied evidence and withheld installation
  left:
[DIAGRAM: Read-only illustrative proposal] nodes=['Requirement: parse JSON text', 'Command template—not an installation instruction: pip install <proposed_distribution> --index-url <proposed_index>', 'Proposed import: <proposed_import>'] edges=[] alt: Read-only illustrative proposal: Requirement: parse JSON text; Command template—not an installation instruction: pip install <proposed_distribution> --index-url <proposed_index>; Proposed import: <proposed_import>
  right:
[DIAGRAM: Read-only verification evidence] nodes=['Distribution identity: no verifying index entry supplied', 'Import name: no project installation documentation supplied', 'Installation source: --index-url selects <proposed_index>, not pip’s default Python Package Index', 'Standard-library alternative: json.loads parses JSON; check whether it meets the requirement', 'Decision: withhold installation because identity and documented use remain unverified.'] edges=[] alt: Read-only verification evidence: Distribution identity: no verifying index entry supplied; Import name: no project installation documentation supplied; Installation source: --index-url selects <proposed_index>, not pip’s default Python Package Index; Standard-library alternative: json.loads parses JSON; check whether it meets the requirement; Decision: withhold installation because identity and documented use remain unverified.

### s05 · explainer · Reviewing generated Python dependency suggestions
Understand — 
(mechanism) pip uses the Python Package Index by default. Browse it to check the named distribution before installing an unchecked suggestion. ⟦B.f1 B:tb4⟧
(mechanism) Distribution and import package names need not match. Confirm the distribution in the project’s installation documentation. ⟦B.f2 B:tb4⟧
(mechanism) `--index-url` changes the package index. Inspect the installation source as well as the name. ⟦B.f3 B:tb4 B:tb5⟧
(mechanism) The standard library supplies modules for many common tasks. Check whether documented functionality meets the requirement before adding a dependency. ⟦B.f4 B:tb4⟧
(mechanism) Assistant suggestions can be mistaken. Withhold installation when identity and documented use cannot be verified. ⟦B.f5 B:tb4 B:tb5⟧
(misconception) Contrast a plausible package name with verified distribution identity and documented use. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4 B:tb5⟧

### s06 · check · Check: Reviewing generated Python dependency suggestions
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, core, grading=client] A suggested distribution has no verifiable index entry or project installation documentation. What is the defensible decision before installation?
  ✔ o1: Withhold installation because identity and documented use cannot be verified.
      why: Assistant output can contain mistakes; withhold installation of a dependency suggestion whose identity and documented use cannot be verified.
  ✘ o2: Install first to discover whether the suggestion exists.
      why: The review should reject an unverifiable suggestion without installing it.
  ✘ o3: Assume its distribution name equals the suggested import name and install it.
      why: Distribution and import names need not match, and the suggestion remains unverified.
  feedback✔: Assistant output can contain mistakes; withhold installation of a dependency suggestion whose identity and documented use cannot be verified.  feedback✘: Recheck the evidence against the stated requirement. Assistant output can contain mistakes; withhold installation of a dependency suggestion whose identity and documented use cannot be verified.  hints: ['Review identity, import name, installation source and necessity independently.']  remediation→r03
  MEASURES: B:withhold_installation_of_unverifiable_dependency(f5)   anchors=['assessment:withhold_installation_of_unverifiable_dependency']
  taught-before-tested: B.f5←s04

### s07 · hands_on · Review generated Python dependency suggestions
Practice — Read the supplied excerpts in this step and judge which claims or proposed actions are correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read the supplied dependency-review excerpts and decide whether each conclusion is supported by the evidence shown. These are fictional review records, not installation instructions. Judge the recorded checks; do not install anything.
  'Evidence: project installation documentation names distribution quantity-reports and import quantity_reports; the index entry matches quantity-reports. Proposed command uses pip with no --index-url. Documented standard-library alternatives were checked and do not meet the supplied reporting requirement. Review conclusion: identity is verified; import and distribution names differ; default source is the Python Package Index.' -> Conclusion supported
      feedback: The conclusion distinguishes the documented names, checks the index identity, identifies the default source, and records the necessity check.
  'Evidence: project installation documentation names distribution quantity-reports and import quantity_reports. Review conclusion: install distribution quantity_reports because import and distribution names must match.' -> Conclusion not supported
      feedback: The installation documentation supplies a different distribution name; import names need not equal distribution names.
  'Evidence: proposed command contains --index-url https://packages.example.invalid/simple. Review conclusion: this still selects the default Python Package Index.' -> Conclusion not supported
      feedback: --index-url changes the installation source; the conclusion fails to identify that change.
  'Evidence: requirement is numeric-text conversion, already met by documented int(text). Suggested extra distribution quantity-magic has no verifiable index identity or project installation documentation. Review conclusion: reject this suggestion and leave it uninstalled; no extra dependency is needed for the supplied conversion requirement.' -> Conclusion supported
      feedback: The record checks a standard-library alternative and withholds installation of an unverifiable suggestion.
  'Evidence: suggested distribution has no verifiable identity or documented use. Review conclusion: install first because generated advice proves it is legitimate.' -> Conclusion not supported
      feedback: Assistant output can be mistaken; the unverifiable suggestion must remain uninstalled.
  feedback✔: pip installs from the Python Package Index by default; browse that index to check the actual named distribution rather than installing an unchecked suggestion. An installable distribution package and an import package need not have the same name; confirm the distribution name from the project’s installation documentation. An --index-url changes the package index used for installation; inspect a proposed install command’s source as well as its name. The Python standard library supplies modules for many common tasks; check whether documented standard-library functionality already meets the requirement before adding a third-party dependency. Assistant output can contain mistakes; withhold installation of a dependency suggestion whose identity and documented use cannot be verified.  feedback✘: Recheck the evidence against the stated requirement. pip installs from the Python Package Index by default; browse that index to check the actual named distribution rather than installing an unchecked suggestion. An installable distribution package and an import package need not have the same name; confirm the distribution name from the project’s installation documentation. An --index-url changes the package index used for installation; inspect a proposed install command’s source as well as its name. The Python standard library supplies modules for many common tasks; check whether documented standard-library functionality already meets the requirement before adding a third-party dependency. Assistant output can contain mistakes; withhold installation of a dependency suggestion whose identity and documented use cannot be verified.  hints: ['Review identity, import name, installation source and necessity independently.']
  MEASURES: B:verify_distribution_identity_against_index_and_documentation(f1,f2); B:identify_proposed_installation_source(f3); B:check_dependency_necessity_against_standard_library_functionality(f4); B:withhold_installation_of_unverifiable_dependency(f5)   anchors=['practice', 'assessment:verify_distribution_identity_against_index_and_documentation', 'assessment:identify_proposed_installation_source', 'assessment:check_dependency_necessity_against_standard_library_functionality', 'assessment:withhold_installation_of_unverifiable_dependency']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04; B.f5←s04

### s08 · explainer · Accepting, repairing or rejecting generated Python on evidence
Understand — 
(mechanism) Generated code can be wrong. Test it rather than accepting it solely because an assistant generated it. ⟦C.f1 C:tb1 C:tb2⟧
(mechanism) Failed assertions and unexpected exceptions identify behavior needing correction; they do not support unchanged acceptance. ⟦C.f2 C:tb1 C:tb3⟧
(mechanism) Compare traced returns and supplied expectations with requirements. Accept only supported behavior; record correction for an addressable mismatch. ⟦C.f3 C:tb1 C:tb3⟧
(mechanism) Reject execution that evaluates untrusted input or truncates a file contrary to requirements until those unsafe operations are removed or corrected. ⟦C.f4 C:tb1 C:tb3⟧
[SIDE_BY_SIDE] Generated origin is not acceptance evidence. left_label: Requirements, traces and tests | right_label: Evidence-based decision
  left:
[DIAGRAM: Supplied versions and evidence] nodes=['supported\ndef cost(quantity):\n    return quantity * 4\nSupplied requirement: cost(3) == 12\nTraced result: 12\nSupplied check: passed', 'missing_return\ndef cost(quantity):\n    if quantity > 0:\n        return quantity * 4\nSupplied requirement: cost(0) == 0\nTraced result: None\nSupplied check: failed assertion', 'unexpected_exception\ndef cost(quantity):\n    raise ValueError("unexpected quantity")\nSupplied requirement: cost(3) == 12\nTraced result: ValueError: unexpected quantity\nSupplied check: unexpected exception', 'unsafe_input (read-only text, never executed):\ndef cost(text):\n    return eval(text)\nRequirement: do not evaluate untrusted text. Safety finding: evaluates untrusted input.\n\nunsafe_file (read-only text, never executed):\ndef cost(output):\n    with open(output, "w") as file:\n        file.write("report")\nRequirement: preserve existing file content. Safety finding: proposed w mode truncates existing content.'] edges=[] alt: Supplied versions and evidence: supported
def cost(quantity):
    return quantity * 4
Supplied requirement: cost(3) == 12
Traced result: 12
Supplied check: passed; missing_return
def cost(quantity):
    if quantity > 0:
        return quantity * 4
Supplied requirement: cost(0) == 0
Traced result: None
Supplied check: failed assertion; unexpected_exception
def cost(quantity):
    raise ValueError("unexpected quantity")
Supplied requirement: cost(3) == 12
Traced result: ValueError: unexpected quantity
Supplied check: unexpected exception; unsafe_input (read-only text, never executed):
def cost(text):
    return eval(text)
Requirement: do not evaluate untrusted text. Safety finding: evaluates untrusted input.

unsafe_file (read-only text, never executed):
def cost(output):
    with open(output, "w") as file:
        file.write("report")
Requirement: preserve existing file content. Safety finding: proposed w mode truncates existing content.
  right:
[DIAGRAM: Decision rules] nodes=['Supported requirements and checks: accept', 'Failed assertion or unexpected exception: correct', 'Addressable behavior mismatch: correct', 'Untrusted evaluation or forbidden truncation: reject execution until corrected'] edges=[] alt: Decision rules: Supported requirements and checks: accept; Failed assertion or unexpected exception: correct; Addressable behavior mismatch: correct; Untrusted evaluation or forbidden truncation: reject execution until corrected

### s09 · explainer · Accepting, repairing or rejecting generated Python on evidence
Understand — 
(mechanism) Generated code can be wrong. Test it rather than accepting it solely because an assistant generated it. ⟦C.f1 C:tb4 C:tb5⟧
(mechanism) Failed assertions and unexpected exceptions identify behavior needing correction; they do not support unchanged acceptance. ⟦C.f2 C:tb4 C:tb5⟧
(mechanism) Compare traced returns and supplied expectations with requirements. Accept only supported behavior; record correction for an addressable mismatch. ⟦C.f3 C:tb4⟧
(mechanism) Reject execution that evaluates untrusted input or truncates a file contrary to requirements until those unsafe operations are removed or corrected. ⟦C.f4 C:tb4 C:tb5⟧
(misconception) Contrast supported behavior with a mismatch or unsafe operation: generated origin justifies none of these decisions. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4 C:tb5⟧

### s10 · video · Accepting, repairing or rejecting generated Python on evidence
Worked walkthrough — 
[VIDEO Decide from requirements and test evidence] bridge-before: Watch how one passing test hides a requirement mismatch, while a second input exposes it. Focus on the evidence supporting correction and verification, not the generated origin. | bridge-after: The clip demonstrates a requirement mismatch and verified repair, but not failed assertions, unexpected exceptions or unsafe-operation rejection. The text explains how those findings affect correction and rejection decisions.
  - mJLwFf0dHSA 2-207s facts=['f1', 'f3'] label: Repair a generated discount helper using expected results | summary: A generated discount helper runs successfully and returns 80 for a price of 100 with a 20% discount. That result hides a mistake: the helper subtracts 20 as a fixed amount rather than calculating 20% of the price. With a price of 200, it returns 180 instead of the required 160. The repair calculates the discount amount as price multiplied by discount divided by 100, then subtracts that amount. Assertions for both expected results pass after the repair. Generated code and one passing test are not enough to establish correctness; acceptance needs evidence that the behavior matches the requirements.

### s11 · check · Check: Accepting, repairing or rejecting generated Python on evidence
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.
QUESTION [choice, stretch, grading=client] Requirement: preserve existing output content and never evaluate untrusted input. Read a proposal containing eval(text) and open(output, "w"). What decision is supported before execution?
  ✔ o1: Reject execution until these unsafe operations are removed or corrected.
      why: Reject execution of a proposed implementation that evaluates untrusted input or truncates a file contrary to the requirements until those unsafe operations are removed or corrected.
  ✘ o2: Accept unchanged because the generated implementation is concise.
      why: Generated form does not override the safety requirements; eval executes text and w truncates content.
  ✘ o3: Accept unchanged if the normal cost example passed.
      why: A normal-case result does not remove evaluation or truncation contrary to requirements.
  feedback✔: Reject execution of a proposed implementation that evaluates untrusted input or truncates a file contrary to the requirements until those unsafe operations are removed or corrected.  feedback✘: Recheck the evidence against the stated requirement. Reject execution of a proposed implementation that evaluates untrusted input or truncates a file contrary to the requirements until those unsafe operations are removed or corrected.  hints: ['Compare the requirement, traced result, test evidence and safety findings separately.']  remediation→r05
  MEASURES: C:justify_rejection_of_unsafe_execution(f4)   anchors=['assessment:justify_rejection_of_unsafe_execution']
  taught-before-tested: C.f4←s08

### s12 · hands_on · Practice: Accepting, repairing or rejecting generated Python on evidence
Practice — Review supplied versions of the cost helper against their requirements, traced returns, safety findings and test results. Record an accept, correct or reject decision with an evidence-based justification for each version, without executing unsafe proposals.
QUESTION [code_exercise, stretch, grading=client] Read the supplied commented cost versions and evidence; never execute those proposals. Complete only the unsafe_result, matched_result, and mismatched_result bindings with the supplied reject_decision, accept_decision and correct_decision names. The branch and return statements in review_cost are supplied and must remain unchanged. Return exactly "reject: untrusted evaluation or contrary truncation must not execute" for unsafe evidence; otherwise "accept: traced return and supplied passing check meet the requirement" when required equals traced; otherwise "correct: traced mismatch or unexpected exception does not support unchanged acceptance". The tests record a justified decision for supported, missing-return, unexpected-exception, unsafe-input and unsafe-file evidence.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'numeric literals', 'None', 'function definitions with def', 'function parameters', 'return statements', 'function calls', 'comparison operators', 'assert statements'] blocked=0 items
  file main.py [editable]:
# Supplied decision labels; preserve these inputs.
correct_decision = 'correct: traced mismatch or unexpected exception does not support unchanged acceptance'
reject_decision = 'reject: untrusted evaluation or contrary truncation must not execute'
accept_decision = 'accept: traced return and supplied passing check meet the requirement'

# Supplied review-only evidence (never executed):
# supported
# def cost(quantity):
#     return quantity * 4
# Supplied requirement: cost(3) == 12
# Traced result: 12
# Supplied check: passed
# 
# 
# missing_return
# def cost(quantity):
#     if quantity > 0:
#         return quantity * 4
# Supplied requirement: cost(0) == 0
# Traced result: None
# Supplied check: failed assertion
# 
# 
# unexpected_exception
# def cost(quantity):
#     raise ValueError("unexpected quantity")
# Supplied requirement: cost(3) == 12
# Traced result: ValueError: unexpected quantity
# Supplied check: unexpected exception
# 
# 
# unsafe_input (read-only text, never executed):
# def cost(text):
#     return eval(text)
# Requirement: do not evaluate untrusted text. Safety finding: evaluates untrusted input.
# 
# unsafe_file (read-only text, never executed):
# def cost(output):
#     with open(output, "w") as file:
#         file.write("report")
# Requirement: preserve existing file content. Safety finding: proposed w mode truncates existing content.

# Supplied branch scaffold: preserve unchanged; complete the decision bindings below.
# Supplied scaffold: preserve this block unchanged.
if True:
    def review_cost(required, traced, unsafe):
        if unsafe:
            return unsafe_result
        if required == traced:
            return matched_result
        return mismatched_result

# TODO: associate each evidence branch with its justified decision.
unsafe_result = None
matched_result = None
mismatched_result = None

  SOLUTION main.py:
# Supplied decision labels; preserve these inputs.
correct_decision = 'correct: traced mismatch or unexpected exception does not support unchanged acceptance'
reject_decision = 'reject: untrusted evaluation or contrary truncation must not execute'
accept_decision = 'accept: traced return and supplied passing check meet the requirement'

# Supplied review-only evidence (never executed):
# supported
# def cost(quantity):
#     return quantity * 4
# Supplied requirement: cost(3) == 12
# Traced result: 12
# Supplied check: passed
# 
# 
# missing_return
# def cost(quantity):
#     if quantity > 0:
#         return quantity * 4
# Supplied requirement: cost(0) == 0
# Traced result: None
# Supplied check: failed assertion
# 
# 
# unexpected_exception
# def cost(quantity):
#     raise ValueError("unexpected quantity")
# Supplied requirement: cost(3) == 12
# Traced result: ValueError: unexpected quantity
# Supplied check: unexpected exception
# 
# 
# unsafe_input (read-only text, never executed):
# def cost(text):
#     return eval(text)
# Requirement: do not evaluate untrusted text. Safety finding: evaluates untrusted input.
# 
# unsafe_file (read-only text, never executed):
# def cost(output):
#     with open(output, "w") as file:
#         file.write("report")
# Requirement: preserve existing file content. Safety finding: proposed w mode truncates existing content.

# Supplied branch scaffold. Complete the return strings only.
# Supplied scaffold: preserve this block unchanged.
if True:
    def review_cost(required, traced, unsafe):
        if unsafe:
            return unsafe_result
        if required == traced:
            return matched_result
        return mismatched_result

# TODO: associate each evidence branch with its justified decision.
unsafe_result = reject_decision
matched_result = accept_decision
mismatched_result = correct_decision

  test test1 (function_call, visible=True): {"function":"review_cost","args":[12,12,false],"expected":"accept: traced return and supplied passing check meet the requirement"} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  test test2 (function_call, visible=True): {"function":"review_cost","args":[0,null,false],"expected":"correct: traced mismatch or unexpected exception does not support unchanged acceptance"} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  test test3 (function_call, visible=True): {"function":"review_cost","args":[12,"ValueError: unexpected quantity",false],"expected":"correct: traced mismatch or unexpected exception does not support unchanged acceptance"} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  test test4 (function_call, visible=True): {"function":"review_cost","args":[0,null,true],"expected":"reject: untrusted evaluation or contrary truncation must not execute"} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  test test5 (function_call, visible=True): {"function":"review_cost","args":[12,12,true],"expected":"reject: untrusted evaluation or contrary truncation must not execute"} | on-fail: Match the required output and preserve the supplied scaffold; review the trace or contract in the prompt.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"85bb7c1ff88806fb412c5d0ca6f5299e0bd1f95668d6f8d89472d607d4d29706","tests_passed":5}
  feedback✔: Generated code can be wrong; test code obtained from a virtual assistant rather than accepting it solely because it was generated. Use the supplied failed assertions and unexpected exceptions to identify behavior requiring correction; these results do not support accepting the helper unchanged. Compare traced returns and supplied test expectations with the required behavior; record acceptance only for behavior supported by that evidence, and record correction when a mismatch can be addressed. Reject execution of a proposed implementation that evaluates untrusted input or truncates a file contrary to the requirements until those unsafe operations are removed or corrected.  feedback✘: Recheck the evidence against the stated requirement. Generated code can be wrong; test code obtained from a virtual assistant rather than accepting it solely because it was generated. Use the supplied failed assertions and unexpected exceptions to identify behavior requiring correction; these results do not support accepting the helper unchanged. Compare traced returns and supplied test expectations with the required behavior; record acceptance only for behavior supported by that evidence, and record correction when a mismatch can be addressed. Reject execution of a proposed implementation that evaluates untrusted input or truncates a file contrary to the requirements until those unsafe operations are removed or corrected.  hints: ['Compare the requirement, traced result, test evidence and safety findings separately.']
  MEASURES: C:justify_acceptance_from_requirements_and_test_evidence(f1,f3); C:justify_correction_from_failures_and_behavior_mismatches(f2,f3); C:justify_rejection_of_unsafe_execution(f4)   anchors=['practice', 'assessment:justify_acceptance_from_requirements_and_test_evidence', 'assessment:justify_correction_from_failures_and_behavior_mismatches', 'assessment:justify_rejection_of_unsafe_execution']
  taught-before-tested: C.f1←s08; C.f3←s08; C.f2←s08; C.f3←s08; C.f4←s08

### s13 · recap · Takeaways
Keep these distinctions — 
(takeaway) Compare API claims with the documented interface for the executing interpreter’s version. ⟦A.f1 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Verify distribution identity, documented use and source; check standard-library alternatives before installation. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Accept supported behavior, correct addressable mismatches, and reject unsafe execution until corrected. ⟦C.f2 C.f3 C.f4 C:tb1 C:tb3 C:tb4 C:tb5⟧

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Verifying generated Python API claims
(mechanism) Check the executing interpreter’s version before comparing version-specific documentation. ⟦A.f4 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a confident generated claim with documentation for the actual object and interpreter version. ⟦A.f4 A:tb1 A:tb3 A:tb4 A:tb5⟧
### r02 · Revisit: Verifying generated Python API claims
(mechanism) Compare a generated call’s name, arguments and expected result with the official API entry’s signature, keyword-only options and returned value. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) `help(object)` displays documentation for an available object, supporting inspection of its interface in the selected runtime. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) Check the executing interpreter’s version before comparing version-specific documentation. ⟦A.f4 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a confident generated claim with documentation for the actual object and interpreter version. ⟦A.f1 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Revisit: Reviewing generated Python dependency suggestions
(mechanism) Assistant suggestions can be mistaken. Withhold installation when identity and documented use cannot be verified. ⟦B.f5 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a plausible package name with verified distribution identity and documented use. ⟦B.f5 B:tb1 B:tb3 B:tb4 B:tb5⟧
### r04 · Revisit: Reviewing generated Python dependency suggestions
(mechanism) pip uses the Python Package Index by default. Browse it to check the named distribution before installing an unchecked suggestion. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) Distribution and import package names need not match. Confirm the distribution in the project’s installation documentation. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) `--index-url` changes the package index. Inspect the installation source as well as the name. ⟦B.f3 B:tb1 B:tb3 B:tb4 B:tb5⟧
(mechanism) The standard library supplies modules for many common tasks. Check whether documented functionality meets the requirement before adding a dependency. ⟦B.f4 B:tb3 B:tb4⟧
(mechanism) Assistant suggestions can be mistaken. Withhold installation when identity and documented use cannot be verified. ⟦B.f5 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a plausible package name with verified distribution identity and documented use. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Revisit: Accepting, repairing or rejecting generated Python on evidence
(mechanism) Reject execution that evaluates untrusted input or truncates a file contrary to requirements until those unsafe operations are removed or corrected. ⟦C.f4 C:tb1 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast supported behavior with a mismatch or unsafe operation: generated origin justifies none of these decisions. ⟦C.f4 C:tb1 C:tb3 C:tb4 C:tb5⟧
### r06 · Revisit: Accepting, repairing or rejecting generated Python on evidence
(mechanism) Generated code can be wrong. Test it rather than accepting it solely because an assistant generated it. ⟦C.f1 C:tb1 C:tb2 C:tb4 C:tb5⟧
(mechanism) Failed assertions and unexpected exceptions identify behavior needing correction; they do not support unchanged acceptance. ⟦C.f2 C:tb1 C:tb3 C:tb4 C:tb5⟧
(mechanism) Compare traced returns and supplied expectations with requirements. Accept only supported behavior; record correction for an addressable mismatch. ⟦C.f3 C:tb1 C:tb3 C:tb4⟧
(mechanism) Reject execution that evaluates untrusted input or truncates a file contrary to requirements until those unsafe operations are removed or corrected. ⟦C.f4 C:tb1 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast supported behavior with a mismatch or unsafe operation: generated origin justifies none of these decisions. ⟦C.f1 C.f2 C.f3 C.f4 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· ops.value: accept: traced return and supplied passing check meet the requirement_x
· expected.value: accept: traced return and supplied passing check meet the requirement_x
· ops.value: correct: traced mismatch or unexpected exception does not support unchanged acceptance_x
· expected.value: correct: traced mismatch or unexpected exception does not support unchanged acceptance_x
· ops.value: correct: traced mismatch or unexpected exception does not support unchanged acceptance_x
· expected.value: correct: traced mismatch or unexpected exception does not support unchanged acceptance_x
· ops.value: reject: untrusted evaluation or contrary truncation must not execute_x
· expected.value: reject: untrusted evaluation or contrary truncation must not execute_x
· ops.value: reject: untrusted evaluation or contrary truncation must not execute_x
· expected.value: reject: untrusted evaluation or contrary truncation must not execute_x