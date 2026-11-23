# EVALUATOR PACKET — Zip iteration (learn_python.tile.046_046)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.zip_iteration — Zip iteration

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: learn_python.tile.046_046.s04/ix.learn_python.tile.046_046.s04: ADVISORY — syntax descriptors with no detector: ['*args and **kwargs parameter declarations', 'assert statements', 'comments', 'generator expressions', 'indented loop bodies', 'integer literals', 'lambda expressions', 'list literals', 'raise statements', 'starred call-argument expansion', 'string literals', 'with statements', 'yield statements']

## SOURCE FACTS — A (python.zip_iteration)   objective: Traverse corresponding values from parallel iterables using zip.
A.f1: zip(left, right) pairs corresponding elements into tuples for parallel traversal.   [sources: python_stdlib_reference#functions.html#zip]
A.f2: Use for left_item, right_item in zip(left, right): to process each pair in an indented body.   [sources: python_stdlib_reference#functions.html#zip]
A.f3: By default zip stops at the shortest input, omitting unmatched trailing values from longer inputs.   [sources: python_stdlib_reference#functions.html#zip]
note: Begin with this objective: Traverse corresponding values from parallel iterables using zip.
note: Keep the example in the Paired iteration tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.aliasing_mutability_and_copying, python.collections_utilities, python.diagnostic_printing.
PRACTICE ANCHOR (live_code): Combine corresponding labels and quantities using zip in a two-variable for loop, and identify the omitted label in the supplied unequal-length case.  SUCCESS: The loop displays notebook 3 and pen 2, and the learner identifies pencil as omitted because no corresponding quantity exists.
ASSESSMENT ANCHOR: identify_corresponding_pairs_and_loop_bindings facts=['f1', 'f2']
ASSESSMENT ANCHOR: predict_pairs_and_omitted_trailing_values facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Avoiding unintended mutations through shared references; Binding variable arguments with *args and **kwargs; Choosing instance, class or static method binding; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Counting values with collections.Counter; Distinguishing input failures from programming defects; Documenting Python interfaces with docstrings; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Initialising instance state with __init__; Inspecting program state with diagnostic printing; Instance methods and self; Investigating Python execution with a debugger; Lambda expressions; Object composition; Ordering iterables with a key function; Passing and storing functions as values; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers

## LESSON, in learner order

### s01 · explainer · Zip iteration
(mechanism) zip(left, right) pairs corresponding elements into tuples. In for left_item, right_item in zip(left, right):, the two variables receive each pair; an indented body processes it. ⟦A.f1 A.f2 A:tb1 A:tb2 A:tb3⟧
(misconception) By default, zip stops at the shortest input. Here pencil has no corresponding quantity and is omitted, not given a missing value. Account for unmatched trailing entries before treating the pairs as a complete report. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
labels = ["notebook", "pen", "pencil"]
quantities = [3, 2]
for label, quantity in zip(labels, quantities):
    print(label, quantity)
  annotations: ['Each paired tuple binds the two loop variables.', 'pencil is unmatched and omitted by default.', 'Output: notebook 3, then pen 2. No pencil line is printed because zip stops at the shorter quantities list.']

### s02 · video · Explore zip iteration
[VIDEO Pair corresponding values with zip] bridge-before: Watch how zip replaces index-based pairing and assigns each pair to two loop variables. The clip’s closing reference to “combinations” means corresponding positions here, not every possible combination. | bridge-after: The clip demonstrates all three essentials: corresponding tuple pairs, a two-variable loop, and stopping at the shortest input. The text applies the same rule to labels and quantities.
  - ALWe-tbrzQU 0-177s facts=['f1', 'f2', 'f3'] label: Traverse corresponding list values with zip | summary: Two lists are compared at corresponding positions, first using indexes and then using zip. Zip pairs their elements into tuples: (1, 1), (2, 1), (3, 3), and (4, 7). The longer list’s trailing 9 is omitted because it has no partner. Reversing the inputs reverses the order of values within each tuple. Adding a third list with only two elements limits the result to two tuples, each containing three values. Finally, a for loop assigns each pair to two variables and uses an indented conditional body to display whether the values match.

### s03 · check · Predict the stopping point
Check your understanding — Choose which entries the supplied zip traversal visits and which it omits.
QUESTION [choice, intro, grading=client] Read this code. Which description accounts for every printed pair and any omitted label?
```python
labels = ['notebook', 'pen', 'pencil']
quantities = [3, 2]
for label, quantity in zip(labels, quantities):
    print(label, quantity)
```
  ✔ o1: notebook 3
pen 2
pencil is omitted because it has no corresponding quantity.
      why: zip pairs corresponding entries and stops at the shorter input.
  ✘ o2: notebook 3
pen 2
pencil is also printed with a missing quantity.
      why: Default zip does not supply a missing value for an unmatched trailing entry.
  ✘ o3: Only the first pair is printed; zip stops after one pair.
      why: zip visits all corresponding pairs, not just the first pair.
  feedback✔: zip pairs corresponding entries and stops at the shorter input.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Compare the number of entries available in each input.']  remediation→r01
  MEASURES: A:predict_pairs_and_omitted_trailing_values(f3)   anchors=['assessment:predict_pairs_and_omitted_trailing_values']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Pair stationery labels
Your turn — Write a two-variable zip loop for the supplied labels and quantities, and identify the unmatched label.
QUESTION [code_exercise, stretch, grading=client] Repair the pairs assignment in main.py so zip pairs labels with quantities rather than labels with themselves. Keep the supplied two-variable loop: label and quantity receive each corresponding pair, and print(label, quantity) displays it on its own line separated by a space. Add one or more comment lines explaining that pencil is omitted because no corresponding quantity exists and zip stops at the shorter input. Include the words pencil, omitted, quantity, and shorter or shortest. Keep the supplied inputs and loop unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'list literals', 'string literals', 'integer literals', 'zip(labels, quantities)', 'for label, quantity in zip(labels, quantities):', 'indented loop bodies', 'print(label, quantity)', 'comments'] blocked=9 items
  file main.py [editable]:
first_label = 'notebook'
labels = [first_label, 'pen', 'pencil']
quantities = [3, 2]
pairs = zip(labels, labels)

# Repair the zip arguments above; retain this supplied two-variable loop.
for label, quantity in pairs:
    print(label, quantity)

# Add a comment identifying the omitted label and explaining the stopping rule.

  SOLUTION main.py:
first_label = 'notebook'
labels = [first_label, 'pen', 'pencil']
quantities = [3, 2]
pairs = zip(labels, quantities)

# Repair the zip arguments above; retain this supplied two-variable loop.
for label, quantity in pairs:
    print(label, quantity)

# Add a comment identifying the omitted label and explaining the stopping rule.
# pencil is omitted: no corresponding quantity; zip stops at the shorter list.

  test t1 (stdout_equals, visible=True): {"expected":"notebook 3\npen 2\n"} | on-fail: Compare what the two inputs represent and account for their different lengths.
  test t2 (value_equals, visible=True): {"expr":"[labels, (lambda comments: 'pencil' in comments and 'omitted' in comments and 'quantity' in comments and ('shorter' in comments or 'shortest' in comments))(' '.join(line for line in open('main.py').read().splitlines() if line.lstrip().startswith('#')).lower())]","expected":[["notebook","pen","pencil"],true]} | on-fail: Compare what the two inputs represent and account for their different lengths.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"57f8898f157d2f729dfaf144677ec1d089e796317cde9032b73aa835436cc2d5","tests_passed":2}
  feedback✔: The loop displays notebook 3 and pen 2, and the learner identifies pencil as omitted because no corresponding quantity exists.  feedback✘: Check the requested behavior and keep the supplied scaffold unchanged.  hints: ['Compare what the two inputs represent and account for their different lengths.']  remediation→r02
  MEASURES: A:identify_corresponding_pairs_and_loop_bindings(f1,f2)   anchors=['practice', 'assessment:identify_corresponding_pairs_and_loop_bindings']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · recap · Takeaways
(takeaway) zip forms corresponding tuples, and two loop variables bind each pair. By default, traversal stops at the shortest input and leaves unmatched trailing values unvisited. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Avoiding unintended mutations through shared references: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Shortest input, not missing values
(mechanism) The labels list ends with pencil, but that entry has no corresponding quantity. By default zip stops at the shortest input: it omits the unmatched tail rather than supplying a missing value. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r02 · Pair values, then bind them
(mechanism) zip(labels, quantities) forms tuples from corresponding positions. Use for label, quantity in zip(labels, quantities): with an indented body: label receives the label and quantity receives its corresponding quantity, not the whole tuple in each variable. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4⟧

=========

# EVALUATOR PACKET — Avoiding unintended mutations through shared references / Counting values with collections.Counter (learn_python.tile.047_048)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.aliasing_mutability_and_copying — Avoiding unintended mutations through shared references
B = python.collections_utilities — Counting values with collections.Counter

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: learn_python.tile.047_048.s05/ix.learn_python.tile.047_048.s05: ADVISORY — syntax descriptors with no detector: ['*args and **kwargs parameter declarations', 'assert statements', 'class declarations', 'decorators', 'def with a required positional parameter', 'equality comparisons', 'finally clauses', 'full-list slicing with [:]', 'function calls with positional arguments', 'generator expressions', 'integer literals', 'lambda expressions', 'list indexing', 'list literals', 'nested list literals', 'nonlocal statements', 'raise statements', 'return statements', 'with statements', 'yield expressions and statements']
  warn: learn_python.tile.047_048.s10/ix.learn_python.tile.047_048.s10: ADVISORY — syntax descriptors with no detector: ['**kwargs parameter declarations', '*args parameter declarations', 'assert statements', 'generator expressions', 'if pairs:', 'integer literals', 'lambda expressions', 'list literals', 'raise statements', 'string literals', 'with statements', 'yield expressions']

## SOURCE FACTS — A (python.aliasing_mutability_and_copying)   objective: Avoid unintended collection mutation through aliases and shallow copies.
A.f1: Assignment can bind multiple names to the same object rather than copying it; mutating a shared list or dictionary can be visible through other names and to a function’s caller.   [sources: python_tutorial#classes.html#a-word-about-names-and-objects]
A.f2: items.copy() or items[:] creates a shallow copy of a list, allowing independent changes to that list’s top-level items.   [sources: python_tutorial#datastructures.html#more-on-lists]
A.f3: A shallow copy still contains references to the original elements, so a nested mutable element can remain shared.   [sources: python_stdlib_reference#stdtypes.html#mutable-sequence-types]
note: Begin with this objective: Avoid unintended collection mutation through aliases and shallow copies.
note: Keep the example in the Collection state and specialized containers tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.collections_utilities, python.diagnostic_printing, python.docstrings.
PRACTICE ANCHOR (live_code): Fix a helper that appends [5] to its caller's list unexpectedly by making a shallow copy before appending and returning the changed copy.  SUCCESS: Calling the repaired helper with original = [[3, 2]] leaves original equal to [[3, 2]] and returns [[3, 2], [5]]. The repair separates the outer lists without claiming that their existing nested elements are independent.
ASSESSMENT ANCHOR: predict_caller_visible_mutations_through_aliases facts=['f1']
ASSESSMENT ANCHOR: predict_independent_top_level_changes_after_shallow_copy facts=['f2']
ASSESSMENT ANCHOR: predict_shared_nested_mutations_after_shallow_copy facts=['f3']

## SOURCE FACTS — B (python.collections_utilities)   objective: Count repeated values with collections.Counter.
B.f1: After from collections import Counter, Counter(items) counts occurrences of hashable elements in a mapping from elements to counts.   [sources: python_stdlib_reference#collections.html#collections.Counter]
B.f2: counts.most_common(1) returns a list with the most frequent element and its count, or an empty list for an empty counter.   [sources: python_stdlib_reference#collections.html#collections.Counter.most_common]
B.f3: most_common orders pairs by descending count, with ties ordered by first encounter; access the first returned pair only if the result is nonempty.   [sources: python_stdlib_reference#collections.html#collections.Counter.most_common]
note: Begin with this objective: Count repeated values with collections.Counter.
note: Keep the example in the Collection state and specialized containers tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.diagnostic_printing, python.docstrings, python.exception_hierarchy.
PRACTICE ANCHOR (live_code): Count blue and red labels in a list with Counter, then report the most frequent label and its count only when a result exists.  SUCCESS: The list ["blue", "red", "blue"] produces blue with count 2. An empty list produces no winning label and is not indexed. For ["red", "blue"], red is selected because it occurs first.
ASSESSMENT ANCHOR: produce_correct_element_frequencies facts=['f1']
ASSESSMENT ANCHOR: retrieve_most_frequent_pair_safely facts=['f2', 'f3']
ASSESSMENT ANCHOR: interpret_frequency_order_and_ties facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Binding variable arguments with *args and **kwargs; Choosing instance, class or static method binding; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Counting values with collections.Counter; Distinguishing input failures from programming defects; Documenting Python interfaces with docstrings; Exception hierarchy; Exception propagation through calls; Extending inherited behavior with super; Guaranteed cleanup with finally; Initialising instance state with __init__; Inspecting program state with diagnostic printing; Instance methods and self; Investigating Python execution with a debugger; Lambda expressions; Object composition; Ordering iterables with a key function; Passing and storing functions as values; Python encapsulation conventions; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers

## LESSON, in learner order

### s01 · explainer · Avoiding unintended mutations through shared references
(mechanism) Different names can refer to one object: assignment is not a copy. Mutating a shared list or dictionary can be visible through another name and to a caller. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) items.copy() or items[:] makes a shallow list copy: top-level changes are independent, but references to existing elements remain. A nested mutable element can still be shared. ⟦A.f2 A.f3 A:tb3⟧
[DIAGRAM: Separate outer lists, shared inner list] nodes=['original', 'alias', 'copied', 'Shared outer list', 'Copied outer list', 'Existing inner list', 'alias.append: outer change', 'copied[0][0]: inner change'] edges=[('original', 'outer', 'refers to'), ('alias', 'outer', 'refers to'), ('copied', 'copy_outer', 'refers to'), ('outer', 'inner', 'element reference'), ('copy_outer', 'inner', 'same element reference'), ('append', 'outer', 'changes this list only'), ('update', 'inner', 'changes shared element')] alt: original and alias point to one outer list. copied points to another outer list. Both outer lists reference the same existing inner list. An append through alias changes the shared outer list; a nested update through copied changes the shared inner list.

### s02 · explainer · Follow outer and inner changes
(example) alias and original share an outer list, so appending through alias affects original. copied has a separate outer list, so that append does not affect its top level. Updating an existing inner element through copied is visible through original because the inner list is shared. original[:] also makes a shallow copy. ⟦A.f1 A.f2 A.f3 A:tb4 A:tb5⟧
[CODE python]
original = [[3, 2]]
alias = original
copied = original.copy()
alias.append([5])
copied[0][0] = 9
print(original)
print(copied)
  annotations: []

### s03 · check · Trace the shared reference
Check your understanding — Read the supplied list changes and choose where each mutation is visible.
QUESTION [choice, intro, grading=client] Before repair, what is original after this helper call?
```python
def append_copy(items):
    copied = items
    copied.append([5])
    return copied

original = [[3, 2]]
changed = append_copy(original)
```
  ✔ o1: [[3, 2], [5]]
      why: items and original refer to the shared list, so the append is visible to the caller.
  ✘ o2: [[3, 2]]
      why: No copy is made: the top-level append changes the caller's list.
  ✘ o3: The caller's list is unaffected because the helper uses the name items.
      why: Changing the name does not copy the object; mutation can remain visible to the caller.
  feedback✔: items and original refer to the shared list, so the append is visible to the caller.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Follow the object referred to by each name, not the name spelling.']  remediation→r01
  MEASURES: A:predict_caller_visible_mutations_through_aliases(f1)   anchors=['assessment:predict_caller_visible_mutations_through_aliases']
  taught-before-tested: A.f1←s01

### s04 · check · Trace the shared inner list
Check your understanding — Read the supplied list changes and choose where each mutation is visible.
QUESTION [choice, core, grading=client] Which result follows this nested update?
```python
original = [[3, 2]]
copied = original.copy()
copied[0][0] = 9
```
  ✔ o1: original = [[9, 2]]; copied = [[9, 2]]
      why: The separate outer lists still reference the same inner list.
  ✘ o2: original = [[3, 2]]; copied = [[9, 2]]
      why: A shallow copy does not make the existing inner list independent.
  ✘ o3: original = [[9, 2]]; copied = [[3, 2]]
      why: The update was made through copied, and that inner list remains shared with original.
  feedback✔: The separate outer lists still reference the same inner list.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Distinguish copying the outer list from copying its elements.']  remediation→r02
  MEASURES: A:predict_shared_nested_mutations_after_shallow_copy(f3)   anchors=['assessment:predict_shared_nested_mutations_after_shallow_copy']
  taught-before-tested: A.f3←s01

### s05 · hands_on · Separate the outer list
Your turn — Repair the helper so appending to its returned list does not change the caller’s outer list.
QUESTION [code_exercise, stretch, grading=client] The scaffold supplies two possible assignments for append_copy: alias_assignment uses copied = items, while shallow_assignment uses copied = items[:]. Select the shallow-copy repair by changing only the copy_assignment binding to select the fragment that separates the outer lists before the supplied append and return. Do not edit the supplied fragments or helper assembly. Keep first_quantity and appended_item unchanged. Calling append_copy must leave original unchanged and return changed with the appended item; a subsequent top-level append to changed must not affect original. This does not make existing nested elements independent.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'integer literals', 'list literals', 'nested list literals', 'def with a required positional parameter', 'function calls with positional arguments', 'return statements', 'list.append()', 'list.copy()', 'full-list slicing with [:]', 'list indexing', 'equality comparisons'] blocked=11 items
  file main.py [editable]:
first_quantity = 3
appended_item = [5]
alias_assignment = '    copied = items\n'
shallow_assignment = '    copied = items[:]\n'

# Select the assignment used inside the supplied helper.
copy_assignment = alias_assignment

# Supplied helper assembly: do not edit.
exec('def append_copy(items):\n' + copy_assignment + '    copied.append(appended_item)\n    return copied\n')

original = [[first_quantity, 2]]
changed = append_copy(original)

  SOLUTION main.py:
first_quantity = 3
appended_item = [5]
alias_assignment = '    copied = items\n'
shallow_assignment = '    copied = items[:]\n'

# Select the assignment used inside the supplied helper.
copy_assignment = shallow_assignment

# Supplied helper assembly: do not edit.
exec('def append_copy(items):\n' + copy_assignment + '    copied.append(appended_item)\n    return copied\n')

original = [[first_quantity, 2]]
changed = append_copy(original)

  test t1 (function_call, visible=True): {"function":"append_copy","args":[[[3,2]]],"expected":[[3,2],[5]]} | on-fail: Separate the outer list before the top-level mutation, without claiming a deep copy.
  test t2 (function_call, visible=True): {"function":"append_copy","args":[[[9]]],"expected":[[9],[5]]} | on-fail: Separate the outer list before the top-level mutation, without claiming a deep copy.
  test t3 (value_equals, visible=True): {"expr":"[original, changed]","expected":[[[3,2]],[[3,2],[5]]]} | on-fail: Separate the outer list before the top-level mutation, without claiming a deep copy.
  test t4 (value_equals, visible=True): {"expr":"(changed.append([9]), [original, changed])[1]","expected":[[[3,2]],[[3,2],[5],[9]]]} | on-fail: Separate the outer list before the top-level mutation, without claiming a deep copy.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a174084cb396d8a2426e0c4facc7f0568e688993c0c98faf9635ec5ca0d96306","tests_passed":4}
  feedback✔: Calling the repaired helper with original = [[3, 2]] leaves original equal to [[3, 2]] and returns [[3, 2], [5]]. The repair separates the outer lists without claiming that their existing nested elements are independent.  feedback✘: Check the requested behavior and keep the supplied scaffold unchanged.  hints: ['Separate the outer list before the top-level mutation, without claiming a deep copy.']  remediation→r03
  MEASURES: A:predict_independent_top_level_changes_after_shallow_copy(f2)   anchors=['practice', 'assessment:predict_independent_top_level_changes_after_shallow_copy']
  taught-before-tested: A.f2←s01

### s06 · explainer · Counting values with collections.Counter
(mechanism) After from collections import Counter, Counter(items) counts occurrences of hashable elements, mapping each element to its count. Use it to summarize repeated stationery labels. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) counts.most_common(1) returns a list containing the most frequent element/count pair, or an empty list for an empty counter. Check that the list is nonempty before selecting its first pair. ⟦B.f2 B.f3 B:tb3 B:tb4 B:tb5⟧
(mechanism) most_common orders pairs by descending count. Tied counts follow first encounter, not a separate ranking. Compare the repeated-label example with empty input and a tie using the same labels. ⟦B.f3 B:tb3 B:tb4⟧
[CODE python]
from collections import Counter
counts = Counter(["blue", "red", "blue"])
print(counts)
pairs = counts.most_common(1)
print(pairs)
if pairs:
    label, count = pairs[0]
    print(label, count)
  annotations: ['Guard first-pair access.', "Output: Counter({'blue': 2, 'red': 1})", "Output: [('blue', 2)]", 'Output: blue 2']
[CODE python]
from collections import Counter
counts = Counter([])
pairs = counts.most_common(1)
print(counts)
print(pairs)
if pairs:
    label, count = pairs[0]
    print(label, count)
  annotations: ['Empty input: inspect the returned list before indexing.', 'Output: Counter()', 'Output: []. The guarded body does not run.']
[CODE python]
from collections import Counter
counts = Counter(['blue', 'red'])
print(counts)
print(counts.most_common(1))
  annotations: ['Tied counts: first encounter decides the order.', "Output: Counter({'blue': 1, 'red': 1})", "Output: [('blue', 1)]. Blue was encountered first."]

### s07 · video · Explore counting values with collections.counter
[VIDEO Count repeated values with Counter] bridge-before: Watch how repeated values become element-count entries. The clip loosely distinguishes Counter from dictionaries; Devspace describes its result as a mapping, and counting requires hashable elements. | bridge-after: The clip demonstrates counting, but omits the hashability restriction and most_common. The text supplies these requirements, including empty results, safe first-pair access, descending counts, and first-encounter tie ordering.
  - cgDRugJzBfM 79-207s facts=['f1'] label: Import Counter and inspect element counts | summary: Import Counter from collections to use it directly. Passing a string counts its characters; passing a list counts repeated values. The examples also supply existing counts through a dictionary and keyword arguments. Displayed results associate each element with its count. Counter has its own type, but its element-to-count structure is a mapping.

### s08 · check · Interpret the Counter result
Check your understanding — Inspect the supplied labels and decide how counts and most_common results should be interpreted.
QUESTION [choice, intro, grading=client] Read the code. Which description gives the counts and a safe way to report the winning pair, including if counts were empty?
```python
from collections import Counter
counts = Counter(['blue', 'red', 'blue'])
pairs = counts.most_common(1)
```
  ✔ o1: Counts: {'blue': 2, 'red': 1}. pairs is [('blue', 2)]; check if pairs before unpacking pairs[0].
      why: Counter counts occurrences; most_common returns a list whose first pair is accessed only when nonempty.
  ✘ o2: Counts: {'blue': 2, 'red': 1}. most_common(1) returns the bare pair, so unpack pairs directly.
      why: most_common(1) returns a list containing a pair, not a bare pair.
  ✘ o3: Counts: {'blue': 2, 'red': 1}. Access pairs[0] unconditionally, even for an empty counter.
      why: An empty counter returns an empty list; access its first pair only when nonempty.
  feedback✔: Counter counts occurrences; most_common returns a list whose first pair is accessed only when nonempty.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Check the shape of the result as well as the empty-input rule.']  remediation→r04
  MEASURES: B:produce_correct_element_frequencies(f1); B:retrieve_most_frequent_pair_safely(f2,f3)   anchors=['assessment:produce_correct_element_frequencies', 'assessment:retrieve_most_frequent_pair_safely']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06

### s09 · check · Interpret a tie
Check your understanding — Inspect the supplied labels and decide how counts and most_common results should be interpreted.
QUESTION [choice, core, grading=client] Which pair is selected, and why?
```python
from collections import Counter
counts = Counter(['red', 'blue'])
pairs = counts.most_common(1)
```
  ✔ o1: ('red', 1), because tied counts follow first encounter.
      why: Both counts are equal, so first encounter determines the selected pair.
  ✘ o2: ('blue', 1), because labels are alphabetized.
      why: Ties follow first encounter, not alphabetic label ranking.
  ✘ o3: No pair, because tied frequencies cannot be reported.
      why: most_common can return a pair for tied counts; it uses first encounter.
  feedback✔: Both counts are equal, so first encounter determines the selected pair.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Look at the encounter order only after comparing the counts.']  remediation→r05
  MEASURES: B:interpret_frequency_order_and_ties(f3)   anchors=['assessment:interpret_frequency_order_and_ties']
  taught-before-tested: B.f3←s06

### s10 · hands_on · Report a frequent label safely
Your turn — Complete the Counter helper: request the most common pair and report it only if one exists.
QUESTION [code_exercise, stretch, grading=client] Replace pairs = [] with an assignment that constructs Counter(labels) and requests its most common pair. Keep the supplied inputs and safe reporting block unchanged. Run the code and inspect the guard: it reports blue 2 for the supplied labels, reports no winner for an empty list without indexing it, and selects red 1 for ["red", "blue"] because red occurs first.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['from collections import Counter', 'variable assignment', 'list literals', 'string literals', 'integer literals', 'Counter(...)', 'counts.most_common(1)', 'if pairs:', 'pairs[0]', 'label, count = pairs[0]', 'print(label, count)'] blocked=10 items
  file main.py [editable]:
from collections import Counter
first_label = 'blue'
labels = [first_label, 'red', first_label]
pairs = []

# Repair the pairs assignment; retain the supplied safe reporting block.
if pairs:
    label, count = pairs[0]
    print(label, count)

  SOLUTION main.py:
from collections import Counter
first_label = 'blue'
labels = [first_label, 'red', first_label]
pairs = Counter(labels).most_common(1)

# Repair the pairs assignment; retain the supplied safe reporting block.
if pairs:
    label, count = pairs[0]
    print(label, count)

  test t1 (stdout_equals, visible=True): {"expected":"blue 2\n"} | on-fail: Request a list of pairs and guard access to its first entry.
  test t2 (value_equals, visible=True): {"expr":"pairs","expected":[["blue",2]]} | on-fail: Request a list of pairs and guard access to its first entry.
  test t3 (value_equals, visible=True): {"expr":"[pairs, (lambda ns, buf: (lambda cm: (cm.__enter__(), exec(open('main.py').read().replace(\"labels = [first_label, 'red', first_label]\", 'labels = []'), ns), cm.__exit__(None, None, None), [ns['pairs'], buf.getvalue()])[3])(__import__('contextlib').redirect_stdout(buf)))({}, __import__('io').StringIO())]","expected":[[["blue",2]],[[],""]]} | on-fail: Request a list of pairs and guard access to its first entry.
  test t4 (value_equals, visible=True): {"expr":"[pairs, (lambda ns, buf: (lambda cm: (cm.__enter__(), exec(open('main.py').read().replace(\"labels = [first_label, 'red', first_label]\", \"labels = ['red', 'blue']\"), ns), cm.__exit__(None, None, None), [ns['pairs'], buf.getvalue()])[3])(__import__('contextlib').redirect_stdout(buf)))({}, __import__('io').StringIO())]","expected":[[["blue",2]],[[["red",1]],"red 1\n"]]} | on-fail: Request a list of pairs and guard access to its first entry.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e77be67e3801afa096e6f65cc21ff90ec7e119cd7a5b9b54b606bb7dbc6da822","tests_passed":4}
  feedback✔: The list ["blue", "red", "blue"] produces blue with count 2. An empty list produces no winning label and is not indexed. For ["red", "blue"], red is selected because it occurs first.  feedback✘: Check the requested behavior and keep the supplied scaffold unchanged.  hints: ['Request a list of pairs and guard access to its first entry.']  remediation→r04
  MEASURES: B:produce_correct_element_frequencies(f1); B:retrieve_most_frequent_pair_safely(f2,f3); B:interpret_frequency_order_and_ties(f3)   anchors=['practice']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06; B.f3←s06

### s11 · recap · Takeaways
(takeaway) Assignment can share an object. A shallow copy separates top-level list changes, but nested mutable elements can remain shared. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Counter maps elements to frequencies. most_common returns a list: guard first-pair access, and interpret ties by first encounter. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Inspecting program state with diagnostic printing: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · New name versus new object
(mechanism) alias = original binds another name to the same list; it does not copy. An append through alias is visible through original and can affect a caller sharing that list. Different names do not imply independent objects. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
### r02 · Separate outer list, shared inner element
(mechanism) copied = original.copy() separates the outer list but retains references to existing elements. A nested update through copied can therefore be visible through original. Separate outer lists do not imply separate nested mutable elements. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Copy before changing the top level
(mechanism) Contrast copied = items with copied = items.copy() or copied = items[:]. The first shares the list; either copy form creates a separate outer list, allowing independent top-level changes. Appending to that copied outer list does not append to the caller’s outer list. ⟦A.f2 A:tb2 A:tb3 A:tb4⟧
### r04 · A returned list, not a bare pair
(mechanism) Counter counts hashable elements into an element-to-count mapping. most_common(1) returns a list containing the most frequent pair, not the bare pair. An empty counter returns an empty list: check pairs before pairs[0]. Pairs descend by count; ties follow first encounter. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · First encounter, not a separate rank
(mechanism) With tied counts among the supplied labels, most_common follows first encounter. It orders by descending count first, not a separate label ranking. Check that the returned list is nonempty before accessing its first pair. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: sorted(..., key=...)
· spec.expr: [pairs, (lambda ns, buf: (lambda cm: (cm.__enter__(), exec(open('main.py').read().replace("labels = [first_label, 'red', first_label]", 'labels = []'), ns), cm.__exit__(None, None, None), [ns['pairs'], buf.getvalue()])[3])(__import__('contextlib').redirect_stdout(buf)))({}, __import__('io').StringIO())]
· spec.expr: [pairs, (lambda ns, buf: (lambda cm: (cm.__enter__(), exec(open('main.py').read().replace("labels = [first_label, 'red', first_label]", "labels = ['red', 'blue']"), ns), cm.__exit__(None, None, None), [ns['pairs'], buf.getvalue()])[3])(__import__('contextlib').redirect_stdout(buf)))({}, __import__('io').StringIO())]

=========

# EVALUATOR PACKET — Inspecting program state with diagnostic printing / Documenting Python interfaces with docstrings (learn_python.tile.049_050)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.diagnostic_printing — Inspecting program state with diagnostic printing
B = python.docstrings — Documenting Python interfaces with docstrings

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: learn_python.tile.049_050.s05/ix.learn_python.tile.049_050.s05: ADVISORY — syntax descriptors with no detector: ['**kwargs parameters', '*args parameters', 'assert statements', 'decorators', 'def with named parameters', 'function calls', 'integer literals', 'lambda expressions', 'raise statements', 'string literals', 'try/finally', 'with statements', 'yield expressions']
  warn: learn_python.tile.049_050.s08/ix.learn_python.tile.049_050.s08: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', '@classmethod', '@staticmethod', 'assert', 'blank lines within docstrings', 'class', 'finally', 'indented function bodies', 'numeric literals', 'raise', 'return quantity * unit_price', 'triple-quoted string literals', 'yield']

## SOURCE FACTS — A (python.diagnostic_printing)   objective: Inspect Python state using temporary diagnostic output.
A.f1: print(label, value) displays a label and a value to reveal the state at that execution point.   [sources: python_stdlib_reference#functions.html#print]
A.f2: repr(value) returns a printable representation that can expose details obscured by ordinary string display.   [sources: python_stdlib_reference#functions.html#repr]
A.f3: Place diagnostic output after the binding or before the operation being investigated to observe that current value; removing the print call removes that diagnostic output.   [sources: python_stdlib_reference#functions.html#print, python_language_reference#simple_stmts.html#assignment-statements]
note: Begin with this objective: Inspect Python state using temporary diagnostic output.
note: Keep the example in the Observability and documentation tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.docstrings, python.exception_hierarchy, python.exception_propagation.
PRACTICE ANCHOR (live_code): Instrument a supplied failing conversion helper with labeled diagnostic output to reveal the unexpected text value before conversion and the resulting quantity, then remove the diagnostic calls.  SUCCESS: The temporary output identifies the current text, including its surrounding spaces, and the converted quantity. Removing the diagnostic calls leaves the helper's conversion and return behavior unchanged.
ASSESSMENT ANCHOR: place_labeled_diagnostics_at_relevant_execution_points facts=['f1', 'f3']
ASSESSMENT ANCHOR: use_repr_to_reveal_hidden_string_details facts=['f2', 'f3']

## SOURCE FACTS — B (python.docstrings)   objective: Document a reusable Python interface with a docstring.
B.f1: Document public functions, modules, classes and methods with docstrings.   [sources: pep8_style_guide#documentation-strings]
B.f2: Place a string literal first in a function body to provide its docstring, with a concise purpose summary and additional calling-convention details after a blank line.   [sources: python_tutorial#controlflow.html#documentation-strings]
B.f3: Document the function’s arguments, return values and applicable exceptions as part of its interface.   [sources: pep8_style_guide#https://peps.python.org/pep-0257/#multi-line-docstrings]
B.f4: help(function) displays documentation for the function, including its docstring and signature.   [sources: python_stdlib_reference#functions.html#help]
note: Begin with this objective: Document a reusable Python interface with a docstring.
note: Keep the example in the Observability and documentation tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.exception_hierarchy, python.exception_propagation, python.finally_cleanup.
PRACTICE ANCHOR (live_code): Add a first-statement docstring to cost(quantity, unit_price), describing its purpose, numeric arguments and returned product, then inspect it with help(cost). Document applicable exceptions only when supported by the helper's behavior.  SUCCESS: The helper retains its multiplication behavior. Its docstring starts with a concise purpose summary, separates calling details with a blank line, accurately describes both arguments and the return value, and makes no unsupported exception claims. help(cost) displays the signature and documentation.
ASSESSMENT ANCHOR: write_docstring_describing_inputs_outputs_and_applicable_exceptions facts=['f2', 'f3']
ASSESSMENT ANCHOR: inspect_function_signature_and_docstring_with_help facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Binding variable arguments with *args and **kwargs; Choosing instance, class or static method binding; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Defining custom exceptions; Distinguishing input failures from programming defects; Documenting Python interfaces with docstrings; Exception hierarchy; Exception propagation through calls; Extending inherited behavior with super; Guaranteed cleanup with finally; Initialising instance state with __init__; Instance methods and self; Instance versus class attributes; Investigating Python execution with a debugger; Lambda expressions; Object composition; Ordering iterables with a key function; Passing and storing functions as values; Python encapsulation conventions; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers

## LESSON, in learner order

### s01 · explainer · Inspecting program state with diagnostic printing
(mechanism) Use print(label, value) for a labeled view of the state at an execution point. Observe the text before conversion and the quantity after its binding rather than guessing from a final result. ⟦A.f1 A.f3 A:tb1 A:tb2 A:tb3 A:tb4⟧
(mechanism) repr(value) returns a printable representation that can expose details ordinary string display obscures. Here it makes surrounding spaces and quotes visible. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Place the diagnostic after the binding or before the operation you are investigating. A print before a later reassignment cannot show the later value. Remove the print call when that diagnostic output is no longer needed. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def convert_quantity(text):
    text = ' 3 '
    print("raw text", repr(text))
    quantity = int(text)
    print("converted quantity", quantity)
    return quantity

convert_quantity(' 3 ')
  annotations: ["Observe after the text reassignment, before conversion. Output: raw text ' 3 '", 'Observe after the quantity binding. Output: converted quantity 3']

### s02 · video · Explore inspecting program state with diagnostic printing
[VIDEO Reveal string details with repr()] bridge-before: Watch for the quotation marks in the string representation. The list comparison also shows that str() and repr() do not always produce visibly different results. | bridge-after: The clip demonstrates repr(), not labeled diagnostic placement or removal. The text covers labeling values, observing them at the relevant execution point, and removing temporary print calls.
  - 5cvM-crlDvg 0-58s facts=['f2'] label: Compare ordinary string display with repr() | summary: Comparing str() and repr() shows why a representation can reveal details that ordinary display hides. Both produce the same displayed result for the example list. For the sample string, repr() includes surrounding quotation marks, while str() does not.

### s03 · check · Locate the observation
Check your understanding — Inspect the supplied code and choose the diagnostic that reveals the intended current value.
QUESTION [choice, intro, grading=client] You want to observe the current text before conversion and the bound quantity afterward. Which placement is appropriate?
```python
def convert_quantity(text):
    text = ' 3 '
    quantity = int(text)
    return quantity
```
  ✔ o1: Put print("raw text", repr(text)) after text is reassigned and before int(text); put print("converted quantity", quantity) after quantity is bound. Remove both diagnostics when finished.
      why: Each label observes state at the relevant execution point; removing the print calls removes temporary output.
  ✘ o2: Print text only before its reassignment, and use that output to describe the later text.
      why: A print before reassignment cannot reveal the later value.
  ✘ o3: Print quantity before quantity is bound, to observe the conversion result.
      why: Observe quantity after its binding, not before the value exists at that execution point.
  feedback✔: Each label observes state at the relevant execution point; removing the print calls removes temporary output.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Place each observation next to the binding or operation it is meant to inspect.']  remediation→r01
  MEASURES: A:place_labeled_diagnostics_at_relevant_execution_points(f1,f3)   anchors=['assessment:place_labeled_diagnostics_at_relevant_execution_points']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · check · Reveal hidden text details
Check your understanding — Inspect the supplied code and choose the diagnostic that reveals the intended current value.
QUESTION [choice, core, grading=client] The helper has just assigned text = ' 3 ' and has not yet converted it. Which diagnostic best exposes the surrounding spaces and quotes, and what should happen when the diagnostic is no longer needed?
  ✔ o1: Use print("raw text", repr(text)) now; remove that print when finished.
      why: repr exposes string details at the relevant point, and the print call is temporary.
  ✘ o2: Use print("raw text", text) before the reassignment; keep it to describe the later text.
      why: Ordinary display can obscure string details, and an earlier observation does not reveal a later binding.
  ✘ o3: Use print("converted quantity", quantity) after conversion to expose the original string's surrounding spaces.
      why: The converted quantity is not the original represented text. Use a text observation before conversion.
  feedback✔: repr exposes string details at the relevant point, and the print call is temporary.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Choose an observation of the string itself at its current binding.']  remediation→r02
  MEASURES: A:use_repr_to_reveal_hidden_string_details(f2,f3)   anchors=['assessment:use_repr_to_reveal_hidden_string_details']
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · hands_on · Inspect the conversion
Your turn — Add labeled observations before and after conversion, use repr for text, then remove the temporary print calls.
QUESTION [code_exercise, stretch, grading=client] Select temporary labeled observations, then compare the instrumented helper with the supplied diagnostic-free helper. raw_observation contains print(raw_label, repr(text)); converted_observation contains print(converted_label, quantity); no_observation contains no diagnostic call. Change only before_conversion and after_conversion to select the observations that reveal the reassigned text before int(text) and the quantity after conversion. The scaffold retains the instrumented inspect_quantity and the final convert_quantity side by side, with both diagnostic calls removed from the final helper. Keep all supplied fragments, helper assembly, inputs, and calls unchanged. The whole program must print only the two labeled observations from inspect_quantity; the final helper must return the same quantity without diagnostic output.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def with named parameters', 'function calls', 'return', 'variable assignment', 'string literals', 'integer literals', 'int(text)', 'print(label, value)', 'repr(text)'] blocked=10 items
  file main.py [editable]:
raw_label = 'raw text'
converted_label = 'converted quantity'
raw_quantity = 3
spaced_text = ' ' + str(raw_quantity) + ' '

no_observation = ''
raw_observation = '    print(raw_label, repr(text))\n'
converted_observation = '    print(converted_label, quantity)\n'

# Select the temporary observations; the final helper stays clean.
before_conversion = no_observation
after_conversion = no_observation

# Supplied helpers: do not edit this assembly.
exec('def inspect_quantity(text):\n    text = spaced_text\n' + before_conversion + '    quantity = int(text)\n' + after_conversion + '    return quantity\n')
exec('def convert_quantity(text):\n    text = spaced_text\n    quantity = int(text)\n    return quantity\n')

debug_result = inspect_quantity('ignored')
result = convert_quantity('ignored')

  SOLUTION main.py:
raw_label = 'raw text'
converted_label = 'converted quantity'
raw_quantity = 3
spaced_text = ' ' + str(raw_quantity) + ' '

no_observation = ''
raw_observation = '    print(raw_label, repr(text))\n'
converted_observation = '    print(converted_label, quantity)\n'

# Select the temporary observations; the final helper stays clean.
before_conversion = raw_observation
after_conversion = converted_observation

# Supplied helpers: do not edit this assembly.
exec('def inspect_quantity(text):\n    text = spaced_text\n' + before_conversion + '    quantity = int(text)\n' + after_conversion + '    return quantity\n')
exec('def convert_quantity(text):\n    text = spaced_text\n    quantity = int(text)\n    return quantity\n')

debug_result = inspect_quantity('ignored')
result = convert_quantity('ignored')

  test t1 (stdout_equals, visible=True): {"expected":"raw text ' 3 '\nconverted quantity 3\n"} | on-fail: Observe each value after its relevant binding, and preserve conversion behavior in the cleaned-up helper.
  test t2 (value_equals, visible=True): {"expr":"[result, debug_result, not any(isinstance(n, __import__('ast').Call) and isinstance(n.func, __import__('ast').Name) and n.func.id == 'print' for f in __import__('ast').parse(open('main.py').read()).body if isinstance(f, __import__('ast').FunctionDef) and f.name == 'convert_quantity' for n in __import__('ast').walk(f))]","expected":[3,3,true]} | on-fail: Observe each value after its relevant binding, and preserve conversion behavior in the cleaned-up helper.
  test t3 (function_call, visible=True): {"function":"convert_quantity","args":["9"],"expected":3} | on-fail: Observe each value after its relevant binding, and preserve conversion behavior in the cleaned-up helper.
  test t4 (function_call, visible=True): {"function":"convert_quantity","args":["2"],"expected":3} | on-fail: Observe each value after its relevant binding, and preserve conversion behavior in the cleaned-up helper.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"22982fb5ae7099f0d84234a691cd4c6b3719b7d87d13f2e17c2c88873da2ef5a","tests_passed":4}
  feedback✔: The temporary output identifies the current text, including its surrounding spaces, and the converted quantity. Removing the diagnostic calls leaves the helper's conversion and return behavior unchanged.  feedback✘: Check the requested behavior and keep the supplied scaffold unchanged.  hints: ['Observe each value after its relevant binding, and preserve conversion behavior in the cleaned-up helper.']  remediation→r01
  MEASURES: A:place_labeled_diagnostics_at_relevant_execution_points(f1,f3); A:use_repr_to_reveal_hidden_string_details(f2,f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01; A.f3←s01

### s06 · explainer · Documenting Python interfaces with docstrings
(mechanism) Document public functions, modules, classes and methods with docstrings so callers can inspect the interface. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) A string literal first in a function body provides its docstring. Start with a concise purpose summary; separate additional calling details with a blank line. A string later in the body is not its first-statement docstring. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) Describe arguments, return values and applicable exceptions accurately. For cost, document the numeric arguments and returned product without inventing exception claims. help(cost) displays the function signature and documentation, including its docstring. ⟦B.f3 B.f4 B:tb3 B:tb4 B:tb5⟧
[CODE python]
def cost(quantity, unit_price):
    """Calculate an order cost.

    Arguments are numeric quantity and unit_price.
    Return their product.
    """
    return quantity * unit_price

help(cost)
  annotations: ['First statement: concise purpose summary.', 'Calling details follow a blank line.', 'Help displays the signature cost(quantity, unit_price) and the documentation: Calculate an order cost. [blank line] Arguments are numeric quantity and unit_price. Return their product.']

### s07 · check · Inspect interface documentation
Check your understanding — Choose the call that displays the helper’s signature and documentation.
QUESTION [choice, intro, grading=client] cost(quantity, unit_price) has a first-statement docstring describing its numeric arguments and returned product. Which operation displays both its signature and documentation?
  ✔ o1: help(cost)
      why: help(function) displays its signature and documentation, including the docstring.
  ✘ o2: cost(3, 2)
      why: Calling cost computes its returned product; that is not documentation inspection.
  ✘ o3: Read a string placed after the return statement as the function's docstring.
      why: The function's docstring is a string literal first in its body, not a later string.
  feedback✔: help(function) displays its signature and documentation, including the docstring.  feedback✘: Review the stated rule and trace the supplied example again.  hints: ['Distinguish inspecting an interface from invoking its calculation.']  remediation→r03
  MEASURES: B:inspect_function_signature_and_docstring_with_help(f4)   anchors=['assessment:inspect_function_signature_and_docstring_with_help']
  taught-before-tested: B.f4←s06

### s08 · hands_on · Document the cost helper
Your turn — Add an accurate first-statement docstring without changing the calculation, then inspect it with help(cost).
QUESTION [code_exercise, stretch, grading=client] Select the supplied documentation fragment that meets the lesson’s first-statement and interface-description rules, then add help(cost) to inspect it. Change only the documentation binding and add help(cost), without changing return quantity * unit_price. Keep all supplied fragments, helper assembly, quantity, and unit_price unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def cost(quantity, unit_price):', 'indented function bodies', 'triple-quoted string literals', 'blank lines within docstrings', 'return quantity * unit_price', 'help(cost)', 'numeric literals', 'cost(quantity, unit_price)'] blocked=10 items
  file main.py [editable]:
empty_documentation = ''
first_statement_documentation = '    """Calculate an order cost.\n\n    Arguments are numeric quantity and unit_price.\n    Return their product.\n    """\n'

# Select the supplied first-statement documentation.
documentation = empty_documentation

# Supplied helper assembly: do not edit.
exec('def cost(quantity, unit_price):\n' + documentation + '    return quantity * unit_price\n')

quantity = 3
unit_price = 2

# Inspect the helper's signature and documentation.

  SOLUTION main.py:
empty_documentation = ''
first_statement_documentation = '    """Calculate an order cost.\n\n    Arguments are numeric quantity and unit_price.\n    Return their product.\n    """\n'

# Select the supplied first-statement documentation.
documentation = first_statement_documentation

# Supplied helper assembly: do not edit.
exec('def cost(quantity, unit_price):\n' + documentation + '    return quantity * unit_price\n')

quantity = 3
unit_price = 2

# Inspect the helper's signature and documentation.
help(cost)

  test t1 (function_call, visible=True): {"function":"cost","args":[3,2],"expected":6} | on-fail: Put interface documentation first in the body and keep it consistent with the unchanged calculation.
  test t2 (function_call, visible=True): {"function":"cost","args":[2,5],"expected":10} | on-fail: Put interface documentation first in the body and keep it consistent with the unchanged calculation.
  test t3 (value_equals, visible=True): {"expr":"[cost(quantity, unit_price), __import__('inspect').cleandoc(cost.__doc__), any(isinstance(n, __import__('ast').Expr) and isinstance(n.value, __import__('ast').Call) and isinstance(n.value.func, __import__('ast').Name) and n.value.func.id == 'help' and len(n.value.args) == 1 and isinstance(n.value.args[0], __import__('ast').Name) and n.value.args[0].id == 'cost' for n in __import__('ast').parse(open('main.py').read()).body)]","expected":[6,"Calculate an order cost.\n\nArguments are numer | on-fail: Put interface documentation first in the body and keep it consistent with the unchanged calculation.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6a339f636449dca1a7bc7f893ebfd44f4dd29682ee4fa126b2c368bd8f412e89","tests_passed":3}
  feedback✔: The helper retains its multiplication behavior. Its docstring starts with a concise purpose summary, separates calling details with a blank line, accurately describes both arguments and the return value, and makes no unsupported exception claims. help(cost) displays the signature and documentation.  feedback✘: Check the requested behavior and keep the supplied scaffold unchanged.  hints: ['Put interface documentation first in the body and keep it consistent with the unchanged calculation.']  remediation→r04
  MEASURES: B:write_docstring_describing_inputs_outputs_and_applicable_exceptions(f2,f3); B:inspect_function_signature_and_docstring_with_help(f4)   anchors=['practice', 'assessment:write_docstring_describing_inputs_outputs_and_applicable_exceptions', 'assessment:inspect_function_signature_and_docstring_with_help']
  taught-before-tested: B.f2←s06; B.f3←s06; B.f4←s06

### s09 · recap · Takeaways
(takeaway) Label observations, use repr to expose string details, and place diagnostics at the binding or operation you want to inspect. Remove temporary print calls afterward. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Put the docstring first. Summarize purpose, then give accurate argument, return and applicable exception details after a blank line. Inspect signature and documentation with help. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Exception hierarchy: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Observe the current binding
(mechanism) print(label, value) reveals state at that execution point. Place it after the binding or before the operation under investigation. A diagnostic before a later reassignment cannot reveal the later value. Remove that print to remove its diagnostic output. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Represent the text at the right point
(mechanism) Ordinary string display can obscure details; repr(text) returns a printable representation that exposes surrounding spaces and quotes in the supplied text. Observe after the relevant binding and before conversion, not before a later reassignment. Remove the diagnostic print when no longer needed. ⟦A.f2 A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Inspect documentation, not the calculation
(mechanism) help(cost) displays the function’s signature and documentation, including its docstring. Contrast inspecting the interface with calling the helper to calculate a product. ⟦B.f4 B:tb3 B:tb4⟧
### r04 · First-statement documentation
(mechanism) Put a string literal first in cost’s body, not later. Give a concise purpose summary, a blank line, then accurate numeric argument and returned-product details. Document exceptions when applicable, without inventing claims. help(cost) displays the signature and documentation. ⟦B.f2 B.f3 B.f4 B:tb3 B:tb4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expected: raw text ' 3 '
converted quantity 3

· expected.value: raw text_x ' 3 '
converted quantity 3
· ops.value: converted quantity_x
· expected.value: raw text ' 3 '
converted quantity_x 3
· spec.expected: Calculate an order cost.

Arguments are numeric quantity and unit_price.
Return their product.
· expected.value: Calculate an order cost.

Arguments are numeric quantity and unit_price.
Return their product.
· expected.value: Calculate an order cost.

Arguments are numeric quantity and unit_price.
Return their product.