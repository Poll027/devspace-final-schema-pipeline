# EVALUATOR PACKET — Development checks with the Python assert statement (learn_python.tile.099_099)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.assert_statement — Development checks with the Python assert statement

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice: Development checks with the Python assert statement
Practice — Add an assertion that an internal helper's total equals 10, while preserving the public function's explicit rejection of negative quantity.

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

=========

# EVALUATOR PACKET — Iterables and iterators / Generator functions with yield / Generator expressions / Iterator consumption and exhaustion (learn_python.tile.100_103)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.iterables_and_iterators — Iterables and iterators
B = python.generator_functions — Generator functions with yield
C = python.generator_expressions — Generator expressions
D = python.iterator_consumption_and_exhaustion — Iterator consumption and exhaustion

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice: Iterables and iterators
Practice — Obtain two independent iterators from values = [3, 2] and request their values explicitly with next.

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

### s06 · hands_on · Practice: Generator functions with yield
Practice — Write positive_quantities(values) to yield each valid quantity, defined as a value greater than zero, one at a time from the input iterable.

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

### s09 · hands_on · Practice: Generator expressions
Practice — Use a generator expression as the sole argument to sum to double and total the positive entries in values.

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

### s12 · check · Check: Iterator consumption and exhaustion
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.

### s13 · hands_on · Practice: Iterator consumption and exhaustion
Practice — Fix a helper that attempts two complete passes over values but reuses an exhausted traversal for the second pass.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Practice: Choosing eager or lazy processing
Practice — Rewrite a one-pass total over doubled values so it avoids building an intermediate transformed list.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Check: Chaining iterables with itertools
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.

### s08 · hands_on · Practice: Chaining iterables with itertools
Practice — Aggregate quantities from first and second using sum(chain(first, second)), without constructing an intermediate concatenated list.

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

### s12 · hands_on · Practice: Choosing map or filter for iterable transformations
Practice — Rewrite map(double, filter(positive, values)) as a readable list comprehension, then write a generator expression that preserves the pipeline's lazy traversal.

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

=========

# EVALUATOR PACKET — Writing Python unittest test cases / Running unittest and interpreting its results / Managing unittest setup and teardown (learn_python.tile.107_109)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.unittest_test_cases — Writing Python unittest test cases
B = python.unittest_execution_and_results — Running unittest and interpreting its results
C = python.unittest_setup_and_teardown — Managing unittest setup and teardown

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice: Writing Python unittest test cases
Practice — Translate supplied normal and invalid-input cases for cost(quantity) into a unittest.TestCase module: cost(3) equals 12, cost(3) is positive, and cost(-1) raises ValueError.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Check: Running unittest and interpreting its results
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.

### s08 · check · Check: Running unittest and interpreting its results
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.

### s09 · hands_on · Practice: Running unittest and interpreting its results
Practice — Run the supplied test_cost.py module with unittest and identify its failing assertion from the runner report.

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

### s13 · hands_on · Practice: Managing unittest setup and teardown
Practice — Implement TestCase.setUp to assign fresh self.quantities = [3, 2] and register the supplied release callable immediately after the supplied resource-acquisition step.

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

=========

# EVALUATOR PACKET — Reading and explaining generated Python / Reviewing generated Python file operations for safety / Reviewing untrusted input and arbitrary Python execution (learn_python.tile.110_112)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.read_generated_code — Reading and explaining generated Python
B = python.review_generated_file_operations — Reviewing generated Python file operations for safety
C = python.review_untrusted_input_and_execution — Reviewing untrusted input and arbitrary Python execution

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice: Reading and explaining generated Python
Practice — Annotate how the generated cost helper handles quantity 3 and an invalid quantity of -1, recording the selected branch and actual return for each.

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

### s07 · hands_on · Practice: Reviewing generated Python file operations for safety
Practice — Review a generated cleanup helper without executing its filesystem operations, and remove an unintended deletion.

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

### s11 · check · Check: Reviewing untrusted input and arbitrary Python execution
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.

### s12 · hands_on · Practice: Reviewing untrusted input and arbitrary Python execution
Practice — Replace a generated eval-based quantity parser with int(text), handle malformed input, and validate that quantity is non-negative without executing untrusted text.

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

=========

# EVALUATOR PACKET — Verifying generated Python API claims / Reviewing generated Python dependency suggestions / Accepting, repairing or rejecting generated Python on evidence (learn_python.tile.113_115)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.verify_generated_api_claims — Verifying generated Python API claims
B = python.review_generated_dependencies — Reviewing generated Python dependency suggestions
C = python.accept_repair_or_reject_generated_code — Accepting, repairing or rejecting generated Python on evidence

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review generated Python API claims
Practice — Read the supplied excerpts in this step and judge which claims or proposed actions are correct, defective or unsafe.

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

### s07 · hands_on · Review generated Python dependency suggestions
Practice — Read the supplied excerpts in this step and judge which claims or proposed actions are correct, defective or unsafe.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s11 · check · Check: Accepting, repairing or rejecting generated Python on evidence
Check your understanding — Read the supplied question and choose the response supported by the rules you just learned.

### s12 · hands_on · Practice: Accepting, repairing or rejecting generated Python on evidence
Practice — Review supplied versions of the cost helper against their requirements, traced returns, safety findings and test results. Record an accept, correct or reject decision with an evidence-based justification for each version, without executing unsafe proposals.

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