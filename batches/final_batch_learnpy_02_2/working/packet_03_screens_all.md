# EVALUATOR PACKET — Zip iteration (learn_python.tile.046_046)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.zip_iteration — Zip iteration

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Predict the stopping point
Check your understanding — Choose which entries the supplied zip traversal visits and which it omits.

### s04 · hands_on · Pair stationery labels
Your turn — Write a two-variable zip loop for the supplied labels and quantities, and identify the unmatched label.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · check · Trace the shared inner list
Check your understanding — Read the supplied list changes and choose where each mutation is visible.

### s05 · hands_on · Separate the outer list
Your turn — Repair the helper so appending to its returned list does not change the caller’s outer list.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Interpret the Counter result
Check your understanding — Inspect the supplied labels and decide how counts and most_common results should be interpreted.

### s09 · check · Interpret a tie
Check your understanding — Inspect the supplied labels and decide how counts and most_common results should be interpreted.

### s10 · hands_on · Report a frequent label safely
Your turn — Complete the Counter helper: request the most common pair and report it only if one exists.

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

=========

# EVALUATOR PACKET — Inspecting program state with diagnostic printing / Documenting Python interfaces with docstrings (learn_python.tile.049_050)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.diagnostic_printing — Inspecting program state with diagnostic printing
B = python.docstrings — Documenting Python interfaces with docstrings

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Locate the observation
Check your understanding — Inspect the supplied code and choose the diagnostic that reveals the intended current value.

### s04 · check · Reveal hidden text details
Check your understanding — Inspect the supplied code and choose the diagnostic that reveals the intended current value.

### s05 · hands_on · Inspect the conversion
Your turn — Add labeled observations before and after conversion, use repr for text, then remove the temporary print calls.

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

### s08 · hands_on · Document the cost helper
Your turn — Add an accurate first-statement docstring without changing the calculation, then inspect it with help(cost).

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