# EVALUATOR PACKET — Choosing a built-in collection (learn_python.tile.026_026)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.collection_selection — Choosing a built-in collection

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.collection_selection)   objective: Choose a built-in collection for a storage requirement.
A.f1: A list is a mutable sequence, suitable for ordered positional access with updates.   [sources: python_stdlib_reference#stdtypes.html#lists]
A.f2: A tuple is an immutable sequence, suitable for a fixed ordered group of values.   [sources: python_stdlib_reference#stdtypes.html#tuples]
A.f3: A set stores distinct hashable values without sequence positions and supports membership tests and set operations.   [sources: python_stdlib_reference#stdtypes.html#set-types-set-frozenset]
A.f4: A dictionary maps hashable keys to values, supports updates and preserves insertion order; use it for lookup by key rather than by sequence position.   [sources: python_stdlib_reference#stdtypes.html#typesmapping]
note: Begin with this objective: Choose a built-in collection for a storage requirement.
note: Keep the example in the Choosing a collection tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.console_input_output, python.enumerate_iteration, python.floating_point_limits.
PRACTICE ANCHOR (live_code): Create a lookup table for notebook and pen quantities, retrieve a quantity by label, and update it. Justify choosing a dictionary rather than an ordered list of quantities.  SUCCESS: The dictionary initially maps notebook to 3 and pen to 2. Lookup by notebook yields 3, and updating the notebook entry changes it to 5 while pen remains 2. The justification distinguishes label-based lookup from list positions and notes that dictionary insertion order does not provide positional access.
ASSESSMENT ANCHOR: choose_sequence_by_order_and_mutability facts=['f1', 'f2']
ASSESSMENT ANCHOR: choose_set_for_distinct_values_and_membership facts=['f3']
ASSESSMENT ANCHOR: distinguish_key_lookup_from_positional_access facts=['f1', 'f4']
ASSESSMENT ANCHOR: choose_collection_from_storage_requirements facts=['f1', 'f2', 'f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Avoiding unintended mutations through shared references; Checking for None with identity; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Enumerate iteration; Exception hierarchy; Floating-point approximation limits; Indentation and code blocks; Inspecting program state with diagnostic printing; Nested loops; Python comments; Python interpreter execution model; Reading and displaying console values; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · Choosing a built-in collection
Learn — 
(definition) Use a list when ordered positions need updates: it is a mutable sequence. ⟦A.f1 A:tb2⟧
(definition) A tuple is an immutable sequence for a fixed, ordered group. ⟦A.f2 A:tb3⟧
(definition) Sets hold distinct hashable values, not sequence positions. They support membership tests and set operations. ⟦A.f3 A:tb3⟧
(definition) A dictionary maps hashable keys to values and allows updates. It preserves insertion order, but lookup uses keys rather than sequence positions. ⟦A.f4 A:tb3⟧
[COMPARISON] cols=['Order helper collection', 'Access and updates']
  - List: editable positions: {"example":"[3, 2, 5]","access":"Mutable sequence; access by position."}
  - Tuple: fixed ordered group: {"example":"(2, 5)","access":"Immutable sequence; fixed ordered values."}
  - Set: distinct membership: {"example":"{\"notebook\", \"pen\"}","access":"Distinct hashable values; membership and set operations; no sequence positions."}
  - Dictionary: key lookup: {"example":"{\"notebook\": 3, \"pen\": 2}","access":"Hashable keys map to values; updates and insertion order; lookup by key."}

### s02 · explainer · Choosing a built-in collection
Learn — 
(example) Use [3, 2, 5] for editable quantities, (2, 5) for fixed bounds, {"notebook", "pen"} for distinct labels, and {"notebook": 3, "pen": 2} for quantities by label. Choose by the access and update needed, not literal length. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Insertion order does not make dictionary lookup positional: it uses keys. Sets also have no sequence positions, even when a display looks ordered. ⟦A.f3 A.f4 A:tb5⟧

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about choosing a built-in collection to choose the answer.

### s04 · check · Choose the right distinction
Check your understanding — Use what you learned about choosing a built-in collection to choose the answer.

### s05 · hands_on · Practice choosing a built-in collection
Try it — Create a lookup table for notebook and pen quantities, retrieve a quantity by label, and update it. Justify choosing a dictionary rather than an ordered list of quantities.

### s06 · recap · Keep these distinctions
Takeaways — 
(takeaway) Choose lists for editable positions, tuples for fixed ordered groups, sets for distinct membership, and dictionaries for key lookup. Dictionary insertion order does not make lookup positional. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Reading and displaying console values: Next: Reading and displaying console values.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review choosing a built-in collection
(definition) Use a list when ordered positions need updates: it is a mutable sequence. ⟦A.f1 A:tb2 A:tb4⟧
(definition) A tuple is an immutable sequence for a fixed, ordered group. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Sets hold distinct hashable values, not sequence positions. They support membership tests and set operations. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Insertion order does not make dictionary lookup positional: it uses keys. Sets also have no sequence positions, even when a display looks ordered. ⟦A.f3 A.f4 A:tb5⟧
(example) For the order helper, compare positional quantities [3, 2, 5] with quantities by label {"notebook": 3, "pen": 2}. One selects positions; the other selects keys. ⟦A.f1 A.f2 A.f3 A:tb4⟧
### r02 · Review choosing a built-in collection
(definition) Use a list when ordered positions need updates: it is a mutable sequence. ⟦A.f1 A:tb2 A:tb4⟧
(definition) A tuple is an immutable sequence for a fixed, ordered group. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Sets hold distinct hashable values, not sequence positions. They support membership tests and set operations. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) A dictionary maps hashable keys to values and allows updates. It preserves insertion order, but lookup uses keys rather than sequence positions. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Insertion order does not make dictionary lookup positional: it uses keys. Sets also have no sequence positions, even when a display looks ordered. ⟦A.f3 A.f4 A:tb5⟧
(example) For the order helper, compare positional quantities [3, 2, 5] with quantities by label {"notebook": 3, "pen": 2}. One selects positions; the other selects keys. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
### r03 · Review choosing a built-in collection
(definition) Use a list when ordered positions need updates: it is a mutable sequence. ⟦A.f1 A:tb2 A:tb4⟧
(definition) A dictionary maps hashable keys to values and allows updates. It preserves insertion order, but lookup uses keys rather than sequence positions. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Insertion order does not make dictionary lookup positional: it uses keys. Sets also have no sequence positions, even when a display looks ordered. ⟦A.f3 A.f4 A:tb5⟧
(example) For the order helper, compare positional quantities [3, 2, 5] with quantities by label {"notebook": 3, "pen": 2}. One selects positions; the other selects keys. ⟦A.f1 A.f4 A:tb4⟧

=========

# EVALUATOR PACKET — Reading and displaying console values · Enumerate iteration (learn_python.tile.027_028)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.console_input_output — Reading and displaying console values
B = python.enumerate_iteration — Enumerate iteration

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.console_input_output)   objective: Implement a simple text-based console interaction.
A.f1: input(prompt) displays an optional prompt and returns entered text without its trailing newline.   [sources: python_stdlib_reference#functions.html#input]
A.f2: print(value1, value2, ...) displays values separated by a space by default and ends with a newline; sep and end customize those delimiters.   [sources: python_stdlib_reference#functions.html#print]
note: Begin with this objective: Implement a simple text-based console interaction.
note: Keep the example in the Console input and indexed iteration tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.enumerate_iteration, python.floating_point_limits, python.indentation_and_blocks.
PRACTICE ANCHOR (live_code): Prompt for a name, store the entered text in label, and print a greeting using that value.  SUCCESS: Entering Ada at the name prompt produces Hello Ada on a new output line, with one space between the greeting and the name and a newline at the end.
ASSESSMENT ANCHOR: read_entered_text_without_prompt_or_trailing_newline facts=['f1']
ASSESSMENT ANCHOR: display_values_with_default_and_custom_delimiters facts=['f2']
ASSESSMENT ANCHOR: read_text_and_display_required_response facts=['f1', 'f2']

## SOURCE FACTS — B (python.enumerate_iteration)   objective: Iterate over values together with their positions using enumerate.
B.f1: enumerate(sequence, start=0) supplies pairs of a counter and the corresponding element; the counter starts at zero by default.   [sources: python_stdlib_reference#functions.html#enumerate]
B.f2: Use for position, value in enumerate(sequence, start=1): with an indented body to number entries from one without updating a manual counter.   [sources: python_stdlib_reference#functions.html#enumerate]
note: Begin with this objective: Iterate over values together with their positions using enumerate.
note: Keep the example in the Console input and indexed iteration tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.floating_point_limits, python.indentation_and_blocks, python.math_utilities.
PRACTICE ANCHOR (live_code): Number the entries in labels from one using enumerate, without manual counter updates.  SUCCESS: The loop displays 1 notebook, 2 pen and 3 pencil, obtaining both the counter and label from enumerate with start=1.
ASSESSMENT ANCHOR: write_enumerate_loop_with_correct_counter_and_value facts=['f1', 'f2']
ASSESSMENT ANCHOR: set_specified_starting_label facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Avoiding unintended mutations through shared references; Checking for None with identity; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Enumerate iteration; Exception hierarchy; Exception propagation through calls; Floating-point approximation limits; Guaranteed cleanup with finally; Indentation and code blocks; Inspecting program state with diagnostic printing; Nested loops; Python comments; Python interpreter execution model; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · Reading and displaying console values
Learn — 
(definition) input(prompt) can display a prompt. It returns the entered text, leaving off the trailing newline. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) print separates displayed values with spaces and finishes with a newline by default. Customize the separators with sep and the ending with end. ⟦A.f2 A:tb3 A:tb4⟧
[CODE python]
label = input("Label: ")
print("Selected", label, sep=": ", end="!\n")
  annotations: ['The prompt is displayed, but it is not part of the returned input text.', "Displayed prompt: `Label: `. Entered text: `notebook`. Returned value: `'notebook'`, without the entered newline or prompt.", "Displayed response: `Selected: notebook!`, followed by a newline. `sep=': '` replaces the default space; `end='!\\n'` replaces the default newline. Without these overrides, `print('Selected', label)` displays `Selected notebook`, followed by a newline."]

### s02 · check · Choose the right distinction
Check your understanding — Use what you learned about reading and displaying console values to choose the answer.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about reading and displaying console values to choose the answer.

### s04 · hands_on · Judge reading and displaying console values
Review the supplied examples — Read the supplied excerpts in this step and decide which are correct or defective for the stated task.

### s05 · explainer · Enumerate iteration
Learn — 
(definition) enumerate(sequence, start=0) supplies pairs of a counter and the corresponding element; the counter starts at zero by default. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) With an indented body, for position, value in enumerate(sequence, start=1): numbers entries from one. No manual counter update is needed. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
[CODE python]
labels = ["notebook", "pen", "pencil"]
for position, label in enumerate(labels, start=1):
    print(position, label)
  annotations: ["Pass 1: counter 1, label `'notebook'`, output `1 notebook`, original list index 0. Pass 2: counter 2, label `'pen'`, output `2 pen`, original index 1. Pass 3: counter 3, label `'pencil'`, output `3 pencil`, original index 2. `start=1` changes the counter, not the list indices."]

### s06 · check · Choose the right distinction
Check your understanding — Use what you learned about enumerate iteration to choose the answer.

### s07 · hands_on · Practice enumerate iteration
Try it — Number the entries in labels from one using enumerate, without manual counter updates.

### s08 · recap · Keep these distinctions
Takeaways — 
(takeaway) Input returns text without the trailing newline. Print controls displayed separators and endings. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Enumerate pairs a counter with each element; changing its start does not change list indices. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Floating-point approximation limits: Next: Floating-point approximation limits.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review reading and displaying console values
(definition) print separates displayed values with spaces and finishes with a newline by default. Customize the separators with sep and the ending with end. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) The prompt is displayed, but it is not part of the returned input text. ⟦A.f1 A:tb5⟧
[CODE python]
label = input("Label: ")
print("Selected", label, sep=": ", end="!\n")
  annotations: ['The prompt is displayed, but it is not part of the returned input text.']
### r02 · Review reading and displaying console values
(definition) input(prompt) can display a prompt. It returns the entered text, leaving off the trailing newline. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) print separates displayed values with spaces and finishes with a newline by default. Customize the separators with sep and the ending with end. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) The prompt is displayed, but it is not part of the returned input text. ⟦A.f1 A:tb5⟧
[CODE python]
label = input("Label: ")
print("Selected", label, sep=": ", end="!\n")
  annotations: ['The prompt is displayed, but it is not part of the returned input text.']
### r03 · Review reading and displaying console values
(definition) input(prompt) can display a prompt. It returns the entered text, leaving off the trailing newline. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) The prompt is displayed, but it is not part of the returned input text. ⟦A.f1 A:tb5⟧
[CODE python]
label = input("Label: ")
print("Selected", label, sep=": ", end="!\n")
  annotations: ['The prompt is displayed, but it is not part of the returned input text.']
### r04 · Review enumerate iteration
(definition) enumerate(sequence, start=0) supplies pairs of a counter and the corresponding element; the counter starts at zero by default. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) With an indented body, for position, value in enumerate(sequence, start=1): numbers entries from one. No manual counter update is needed. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) Changing the display counter’s start does not change list indexing. ⟦B.f1 B.f2 B:tb5⟧
[CODE python]
labels = ["notebook", "pen", "pencil"]
for position, label in enumerate(labels, start=1):
    print(position, label)
  annotations: ['Changing the display counter’s start does not change list indexing.']

## OTHER CONTENT (fields without a dedicated renderer)
· annotations.text: Displayed response: `Selected: notebook!`, followed by a newline. `sep=': '` replaces the default space; `end='!\n'` replaces the default newline. Without these overrides, `print('Selected', label)` displays `Selected notebook`, followed by a newline.

=========

# EVALUATOR PACKET — Floating-point approximation limits (learn_python.tile.029_029)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.floating_point_limits — Floating-point approximation limits

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.floating_point_limits)   objective: Account for floating-point approximation in numeric comparisons.
A.f1: Many decimal fractions cannot be represented exactly as binary floating-point values.   [sources: python_tutorial#floatingpoint.html#representation-error]
A.f2: math.isclose(a, b, rel_tol=..., abs_tol=...) compares values using relative and absolute tolerances rather than exact equality.   [sources: python_stdlib_reference#math.html#math.isclose]
A.f3: The default relative tolerance is 1e-9 and absolute tolerance is 0.0; comparison to zero requires an appropriate positive absolute tolerance when nonzero differences should count as close.   [sources: python_stdlib_reference#math.html#math.isclose]
note: Begin with this objective: Account for floating-point approximation in numeric comparisons.
note: Keep the example in the Floating-point limits tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.indentation_and_blocks, python.math_utilities, python.nested_collections.
PRACTICE ANCHOR (live_code): Check the computed sum 0.1 + 0.2 against 0.3 using math.isclose, then check a small nonzero value against zero with an appropriate positive absolute tolerance.  SUCCESS: The exact equality comparison returns False, while both math.isclose comparisons return True; the comparison against zero explicitly supplies a suitable positive abs_tol.
ASSESSMENT ANCHOR: choose_approximate_comparison_for_computed_float facts=['f1', 'f2']
ASSESSMENT ANCHOR: choose_positive_absolute_tolerance_near_zero facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Avoiding unintended mutations through shared references; Checking for None with identity; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Indentation and code blocks; Inspecting program state with diagnostic printing; Nested loops; Passing and storing functions as values; Python comments; Python interpreter execution model; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · Floating-point approximation limits
Learn — 
(definition) Many decimal fractions have no exact binary floating-point representation. ⟦A.f1 A:tb2 A:tb4⟧
(definition) math.isclose(a, b, rel_tol=..., abs_tol=...) uses relative and absolute tolerances instead of demanding exact equality. ⟦A.f2 A:tb3 A:tb4⟧
(definition) The default relative tolerance is 1e-9 and absolute tolerance is 0.0; comparison to zero requires an appropriate positive absolute tolerance when nonzero differences should count as close. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
import math
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(math.isclose(0.000001, 0.0, abs_tol=0.00001))
  annotations: ['Near zero, the default absolute tolerance supplies no positive allowance.', 'Result: `False`; this computed sum is not exactly equal to 0.3.', 'Result: `True`; the values are close under the default tolerances.', 'Result: `True`; the explicit positive `abs_tol=0.00001` allows this difference from zero.']

### s02 · check · Choose the right distinction
Check your understanding — Use what you learned about floating-point approximation limits to choose the answer.

### s03 · hands_on · Practice floating-point approximation limits
Try it — Check the computed sum 0.1 + 0.2 against 0.3 using math.isclose, then check a small nonzero value against zero with an appropriate positive absolute tolerance.

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Many decimal fractions are approximate as binary floats. Compare with suitable tolerances; near zero, use a positive absolute tolerance when small differences should count as close. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Indentation and code blocks: Next: Indentation and code blocks.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review floating-point approximation limits
(definition) Many decimal fractions have no exact binary floating-point representation. ⟦A.f1 A:tb2 A:tb4⟧
(definition) math.isclose(a, b, rel_tol=..., abs_tol=...) uses relative and absolute tolerances instead of demanding exact equality. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Near zero, the default absolute tolerance supplies no positive allowance. ⟦A.f3 A:tb5⟧
[CODE python]
import math
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(math.isclose(0.000001, 0.0, abs_tol=0.00001))
  annotations: ['Near zero, the default absolute tolerance supplies no positive allowance.']
### r02 · Review floating-point approximation limits
(definition) The default relative tolerance is 1e-9 and absolute tolerance is 0.0; comparison to zero requires an appropriate positive absolute tolerance when nonzero differences should count as close. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Near zero, the default absolute tolerance supplies no positive allowance. ⟦A.f3 A:tb5⟧
[CODE python]
import math
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
print(math.isclose(0.000001, 0.0, abs_tol=0.00001))
  annotations: ['Near zero, the default absolute tolerance supplies no positive allowance.']

=========

# EVALUATOR PACKET — Indentation and code blocks (learn_python.tile.030_030)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.indentation_and_blocks — Indentation and code blocks

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.indentation_and_blocks)   objective: Use indentation to express Python block structure.
A.f1: A compound statement’s header ends with a colon and its multi-line suite is an indented block; nested suites require deeper indentation.   [sources: python_language_reference#compound_stmts.html]
A.f2: Indentation determines statement grouping; dedenting ends a deeper group, and inconsistent indentation can be invalid.   [sources: python_language_reference#lexical_analysis.html#indentation]
A.f3: Use four spaces for each indentation level when repairing block structure.   [sources: pep8_style_guide#indentation]
note: Begin with this objective: Use indentation to express Python block structure.
note: Keep the example in the Indentation and blocks tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.math_utilities, python.nested_collections, python.nested_loops.
PRACTICE ANCHOR (live_code): Correct the indentation of the quantity condition inside the loop, its total update, and the final report using four spaces per level.  SUCCESS: The condition belongs to the loop, the addition belongs to the condition, and print(total) belongs outside the loop. Only positive quantities contribute, so the final report displays 5 once.
ASSESSMENT ANCHOR: repair_wrongly_nested_block facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: predict_statement_suite_membership facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Avoiding unintended mutations through shared references; Checking for None with identity; Closures and enclosing scope; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Inspecting program state with diagnostic printing; Nested loops; Passing and storing functions as values; Python comments; Python interpreter execution model; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · Indentation and code blocks
Learn — 
(definition) End a compound-statement header with a colon. Its multi-line body is indented; a nested body goes deeper. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Indentation groups statements. Dedenting ends the deeper group; inconsistent indentation can be invalid. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Use four spaces for each indentation level when repairing block structure. ⟦A.f3 A:tb3 A:tb4⟧
[CODE python]
total = 0
for quantity in [3, -1, 2]:
    if quantity > 0:
        total = total + quantity
print(total)
  annotations: ['Lines 1 and 5 are at the outer level; lines 2–4 form the loop structure. Line 3 has four leading spaces and is inside the loop. Line 4 has eight leading spaces and is inside the condition. Dedenting line 5 places the final report outside both bodies.']

### s02 · video · Indentation and code blocks
Optional walkthrough — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about indentation and code blocks to choose the answer.

### s04 · check · Choose the right distinction
Check your understanding — Use what you learned about indentation and code blocks to choose the answer.

### s05 · hands_on · Practice indentation and code blocks
Try it — Correct the indentation of the quantity condition inside the loop, its total update, and the final report using four spaces per level.

### s06 · recap · Keep these distinctions
Takeaways — 
(takeaway) Colons introduce multi-line bodies. Indentation defines grouping, nested bodies go deeper, and dedenting ends a deeper group. Repair each level with four spaces. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Using math for numeric calculations: Next: Using math for numeric calculations.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review indentation and code blocks
(definition) End a compound-statement header with a colon. Its multi-line body is indented; a nested body goes deeper. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Indentation groups statements. Dedenting ends the deeper group; inconsistent indentation can be invalid. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Use four spaces for each indentation level when repairing block structure. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Dedenting moves a statement out of a deeper group; indentation is not merely decoration. ⟦A.f1 A.f2 A:tb5⟧
[CODE python]
total = 0
for quantity in [3, -1, 2]:
    if quantity > 0:
        total = total + quantity
print(total)
  annotations: ['Dedenting moves a statement out of a deeper group; indentation is not merely decoration.']
### r02 · Review indentation and code blocks
(definition) End a compound-statement header with a colon. Its multi-line body is indented; a nested body goes deeper. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Indentation groups statements. Dedenting ends the deeper group; inconsistent indentation can be invalid. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Dedenting moves a statement out of a deeper group; indentation is not merely decoration. ⟦A.f1 A.f2 A:tb5⟧
[CODE python]
total = 0
for quantity in [3, -1, 2]:
    if quantity > 0:
        total = total + quantity
print(total)
  annotations: ['Dedenting moves a statement out of a deeper group; indentation is not merely decoration.']

=========

# EVALUATOR PACKET — Using math for numeric calculations (learn_python.tile.031_031)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.math_utilities — Using math for numeric calculations

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.math_utilities)   objective: Select math functions for a numeric calculation.
A.f1: After import math, math.sqrt(x) returns the square root of x.   [sources: python_stdlib_reference#math.html#math.sqrt]
A.f2: math functions operate on real rather than complex values; an invalid operation such as sqrt(-1.0) raises ValueError.   [sources: python_stdlib_reference#math.html#module-math]
note: Begin with this objective: Select math functions for a numeric calculation.
note: Keep the example in the Standard numeric utilities tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.nested_collections, python.nested_loops, python.range_iteration.
PRACTICE ANCHOR (live_code): Use math.sqrt to calculate the side length of a square with area 9 square units.  SUCCESS: After importing math, calculate math.sqrt(9), producing a side length of 3.0 units.
ASSESSMENT ANCHOR: select_and_apply_math_sqrt facts=['f1']
ASSESSMENT ANCHOR: recognize_math_sqrt_domain_and_invalid_input facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Avoiding unintended mutations through shared references; Checking for None with identity; Closures and enclosing scope; Constructing and resolving pathlib paths; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Inspecting program state with diagnostic printing; Nested loops; Passing and storing functions as values; Python comments; Python interpreter execution model; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · Using math for numeric calculations
Learn — 
(definition) Import math, then call math.sqrt(x) for the square root of x. ⟦A.f1 A:tb2 A:tb4⟧
(definition) math functions operate on real rather than complex values; an invalid operation such as sqrt(-1.0) raises ValueError. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
import math
print(math.sqrt(9))
try:
    print(math.sqrt(-1.0))
except ValueError:
    print("No real square root for this input")
  annotations: ['Import the math module before using its functions.', '`math.sqrt(9)` returns `3.0`, which this print call displays.', '`math.sqrt(-1.0)` raises `ValueError`: this input has no real square root. It does not return a complex result.']

### s02 · video · Using math for numeric calculations
Optional walkthrough — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about using math for numeric calculations to choose the answer.

### s04 · hands_on · Practice using math for numeric calculations
Try it — Use math.sqrt to calculate the side length of a square with area 9 square units.

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Import math to use math.sqrt. These functions operate on real values; an invalid real-valued operation can raise ValueError. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Accessing and updating nested collections: Next: Accessing and updating nested collections.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review using math for numeric calculations
(definition) math functions operate on real rather than complex values; an invalid operation such as sqrt(-1.0) raises ValueError. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) A real-valued square-root operation is not a request for a complex result. ⟦A.f2 A:tb5⟧
[CODE python]
import math
print(math.sqrt(9))
try:
    print(math.sqrt(-1.0))
except ValueError:
    print("No real square root for this input")
  annotations: ['A real-valued square-root operation is not a request for a complex result.']
### r02 · Review using math for numeric calculations
(definition) Import math, then call math.sqrt(x) for the square root of x. ⟦A.f1 A:tb2 A:tb4⟧
(misconception) A real-valued square-root operation is not a request for a complex result. ⟦A.f2 A:tb5⟧
[CODE python]
import math
print(math.sqrt(9))
try:
    print(math.sqrt(-1.0))
except ValueError:
    print("No real square root for this input")
  annotations: ['A real-valued square-root operation is not a request for a complex result.']

=========

# EVALUATOR PACKET — Accessing and updating nested collections · Nested loops · Using range for counted iteration (learn_python.tile.032_034)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.nested_collections — Accessing and updating nested collections
B = python.nested_loops — Nested loops
C = python.range_iteration — Using range for counted iteration

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.nested_collections)   objective: Access and update values in nested collections.
A.f1: A collection can contain other collections; successive indices and keys select progressively nested values.   [sources: python_tutorial#introduction.html#lists, python_tutorial#datastructures.html#dictionaries]
A.f2: Assign to the final selected list index or dictionary key to update that nested value.   [sources: python_tutorial#introduction.html#lists, python_tutorial#datastructures.html#dictionaries]
note: Begin with this objective: Access and update values in nested collections.
note: Keep the example in the Nested data and bounded iteration tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.nested_loops, python.range_iteration, python.running_scripts.
PRACTICE ANCHOR (live_code): Update the second quantity in an order dictionary stored inside a list of order records.  SUCCESS: The selected order's quantities change from [3, 2] to [3, 5], with the surrounding list and dictionary structure preserved.
ASSESSMENT ANCHOR: follow_keys_and_indices_to_update_a_nested_record facts=['f1', 'f2']

## SOURCE FACTS — B (python.nested_loops)   objective: Write and trace nested loops.
B.f1: Place an indented inner for loop in an outer for loop to traverse the inner collection for each outer item.   [sources: python_tutorial#controlflow.html#for-statements, python_tutorial#datastructures.html#nested-list-comprehensions]
B.f2: For nested rows, for row in rows: with a nested for cell in row: visits each row’s cells before proceeding to the next row.   [sources: python_tutorial#controlflow.html#for-statements, python_tutorial#datastructures.html#nested-list-comprehensions]
note: Begin with this objective: Write and trace nested loops.
note: Keep the example in the Nested data and bounded iteration tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.range_iteration, python.running_scripts, python.statements_and_expressions.
PRACTICE ANCHOR (live_code): Write nested for loops to visit and display each cell in rows = [[3, 2], [5, 4]], completing each row before moving to the next.  SUCCESS: The inner loop uses the current row as its source, and the cells are displayed in the order 3, 2, 5, 4.
ASSESSMENT ANCHOR: predict_row_cell_iteration_pairs facts=['f1', 'f2']
ASSESSMENT ANCHOR: produce_row_by_row_nested_traversal facts=['f1', 'f2']

## SOURCE FACTS — C (python.range_iteration)   objective: Use range for bounded integer iteration.
C.f1: range(stop) starts at zero with step one; range(start, stop, step) uses the specified start and nonzero step.   [sources: python_stdlib_reference#stdtypes.html#ranges]
C.f2: The stop value is excluded; a positive step continues below stop and a negative step continues above stop.   [sources: python_stdlib_reference#stdtypes.html#ranges]
C.f3: Use for index in range(start, stop, 2): to traverse every second integer position in an increasing interval.   [sources: python_stdlib_reference#stdtypes.html#ranges]
note: Begin with this objective: Use range for bounded integer iteration.
note: Keep the example in the Nested data and bounded iteration tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.running_scripts, python.statements_and_expressions, python.comments.
PRACTICE ANCHOR (live_code): Process every second integer position from zero up to the excluded limit of six using a for loop with range.  SUCCESS: The loop displays 0, 2 and 4 in order, processing each position once and excluding six.
ASSESSMENT ANCHOR: choose_range_start_and_default_step facts=['f1']
ASSESSMENT ANCHOR: choose_excluded_stop_and_directional_step facts=['f1', 'f2']
ASSESSMENT ANCHOR: choose_range_values_for_every_second_position facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding unintended mutations through shared references; Checking for None with identity; Closures and enclosing scope; Constructing and resolving pathlib paths; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Inspecting program state with diagnostic printing; Investigating Python execution with a debugger; Nested loops; Passing and storing functions as values; Python comments; Python interpreter execution model; Raising exceptions; Reading Python tracebacks; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · Accessing and updating nested collections
Learn — 
(definition) Collections can hold other collections. Each successive index or key selects a value one level further inside. ⟦A.f1 A:tb2 A:tb4⟧
(definition) To change a nested value, assign to the final selected list index or dictionary key. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
order = [{"quantities": [3, 2]}]
print(order[0]["quantities"][1])
order[0]["quantities"][1] = 5
print(order)
  annotations: ["`order[0]` selects the first order dictionary; `['quantities']` selects its list; `[1]` selects the second quantity, 2.", "Assigning at the final index replaces 2 with 5. The updated structure is `[{'quantities': [3, 5]}]`; the first quantity remains 3."]

### s02 · video · Accessing and updating nested collections
Optional walkthrough — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about accessing and updating nested collections to choose the answer.

### s04 · hands_on · Practice accessing and updating nested collections
Try it — Update the second quantity in an order dictionary stored inside a list of order records.

### s05 · explainer · Nested loops
Learn — 
(definition) Indent an inner for loop inside an outer for loop. The inner collection is traversed for each outer item. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) With for row in rows: and an inner for cell in row:, finish the current row’s cells before moving to the next row. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
[CODE python]
rows = [[3, 2], [5, 4]]
for row in rows:
    for cell in row:
        print(cell)
  annotations: ['For row `[3, 2]`, cell is first 3 and then 2. Only after completing that row does the outer loop advance to `[5, 4]`, where cell is first 5 and then 4. The displayed values, on separate lines, are 3, 2, 5, 4.']

### s06 · check · Choose the right distinction
Check your understanding — Use what you learned about nested loops to choose the answer.

### s07 · hands_on · Practice nested loops
Try it — Write nested for loops to visit and display each cell in rows = [[3, 2], [5, 4]], completing each row before moving to the next.

### s08 · explainer · Using range for counted iteration
Learn — 
(definition) range(stop) starts at zero with step one; range(start, stop, step) uses the specified start and nonzero step. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) The stop is excluded. Positive steps keep values below stop; negative steps keep values above stop. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Use for index in range(start, stop, 2): to traverse every second integer position in an increasing interval. ⟦C.f3 C:tb3 C:tb4⟧
[CODE python]
for index in range(0, 6, 2):
    print(index)
for index in range(5, 0, -2):
    print(index)
  annotations: ['The stop is an excluded boundary, not a guaranteed final value.', '`range(0, 6, 2)` supplies 0, 2, 4; stop 6 is excluded.', '`range(5, 0, -2)` supplies 5, 3, 1; stop 0 is excluded.']

### s09 · check · Choose the right distinction
Check your understanding — Use what you learned about using range for counted iteration to choose the answer.

### s10 · check · Choose the right distinction
Check your understanding — Use what you learned about using range for counted iteration to choose the answer.

### s11 · hands_on · Practice using range for counted iteration
Try it — Process every second integer position from zero up to the excluded limit of six using a for loop with range.

### s12 · recap · Keep these distinctions
Takeaways — 
(takeaway) Follow successive indices and keys inward; assign to the final selection to update a nested value. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) The inner loop finishes the current row’s cells before the outer loop advances. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Range excludes stop. Choose start and a nonzero step with the intended direction. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Running Python scripts: Next: Running Python scripts.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review accessing and updating nested collections
(definition) Collections can hold other collections. Each successive index or key selects a value one level further inside. ⟦A.f1 A:tb2 A:tb4⟧
(definition) To change a nested value, assign to the final selected list index or dictionary key. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Follow the selections inward; update the final selection, not the outer container. ⟦A.f2 A:tb5⟧
[CODE python]
order = [{"quantities": [3, 2]}]
print(order[0]["quantities"][1])
order[0]["quantities"][1] = 5
print(order)
  annotations: ["`order[0]` selects the first order dictionary; `['quantities']` selects its list; `[1]` selects the second quantity, 2.", "Assigning at the final index replaces 2 with 5. The updated structure is `[{'quantities': [3, 5]}]`; the first quantity remains 3."]
### r02 · Review nested loops
(definition) Indent an inner for loop inside an outer for loop. The inner collection is traversed for each outer item. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) With for row in rows: and an inner for cell in row:, finish the current row’s cells before moving to the next row. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) Finish the inner traversal for the current row before advancing the outer loop. ⟦B.f1 B.f2 B:tb5⟧
[CODE python]
rows = [[3, 2], [5, 4]]
for row in rows:
    for cell in row:
        print(cell)
  annotations: ['Finish the inner traversal for the current row before advancing the outer loop.']
### r03 · Review using range for counted iteration
(definition) range(stop) starts at zero with step one; range(start, stop, step) uses the specified start and nonzero step. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(misconception) The stop is an excluded boundary, not a guaranteed final value. ⟦C.f1 C.f2 C:tb5⟧
[CODE python]
for index in range(0, 6, 2):
    print(index)
for index in range(5, 0, -2):
    print(index)
  annotations: ['The stop is an excluded boundary, not a guaranteed final value.']
### r04 · Review using range for counted iteration
(definition) range(stop) starts at zero with step one; range(start, stop, step) uses the specified start and nonzero step. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) The stop is excluded. Positive steps keep values below stop; negative steps keep values above stop. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(misconception) The stop is an excluded boundary, not a guaranteed final value. ⟦C.f1 C.f2 C:tb5⟧
[CODE python]
for index in range(0, 6, 2):
    print(index)
for index in range(5, 0, -2):
    print(index)
  annotations: ['The stop is an excluded boundary, not a guaranteed final value.']
### r05 · Review using range for counted iteration
(definition) range(stop) starts at zero with step one; range(start, stop, step) uses the specified start and nonzero step. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) The stop is excluded. Positive steps keep values below stop; negative steps keep values above stop. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Use for index in range(start, stop, 2): to traverse every second integer position in an increasing interval. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) The stop is an excluded boundary, not a guaranteed final value. ⟦C.f1 C.f2 C:tb5⟧
[CODE python]
for index in range(0, 6, 2):
    print(index)
for index in range(5, 0, -2):
    print(index)
  annotations: ['The stop is an excluded boundary, not a guaranteed final value.']

=========

# EVALUATOR PACKET — Running Python scripts · Statements and expressions · Python comments (learn_python.tile.035_037)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.running_scripts — Running Python scripts
B = python.statements_and_expressions — Statements and expressions
C = python.comments — Python comments

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.running_scripts)   objective: Run a saved Python script with the intended interpreter.
A.f1: Invoke an explicitly chosen Python executable with a script path as its argument to execute the script.   [sources: python_tutorial#interpreter.html#invoking-the-interpreter]
A.f2: print sends script output to the standard output stream by default.   [sources: python_stdlib_reference#functions.html#print]
A.f3: A zero process exit status indicates successful termination and a nonzero status abnormal termination; sys.exit(status) requests that status.   [sources: python_stdlib_reference#sys.html#sys.exit]
note: Begin with this objective: Run a saved Python script with the intended interpreter.
note: Keep the example in the Scripts and source structure tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.statements_and_expressions, python.comments, python.interactive_execution.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Save report.py and run it by passing its path to an explicitly selected Python executable. Display Ready and request an exit status, then compare runs requesting zero and a nonzero status.  SUCCESS: The saved report.py is invoked with the supplied executable path. Both runs display Ready on standard output, while the separately displayed process status changes from 0 to 2.
ASSESSMENT ANCHOR: invoke_script_with_explicit_executable facts=['f1']
ASSESSMENT ANCHOR: identify_default_standard_output facts=['f2']
ASSESSMENT ANCHOR: interpret_and_request_process_exit_status facts=['f3']
ASSESSMENT ANCHOR: distinguish_printed_output_from_exit_status facts=['f2', 'f3']

## SOURCE FACTS — B (python.statements_and_expressions)   objective: Distinguish statements from expressions during Python evaluation.
B.f1: An expression statement evaluates an expression; in interactive mode its non-None value is displayed.   [sources: python_language_reference#simple_stmts.html#expression-statements]
B.f2: An assignment evaluates its right-hand expression before binding the resulting value to its target.   [sources: python_language_reference#simple_stmts.html#assignment-statements]
B.f3: Python evaluates expressions from left to right; operator precedence and parentheses determine how constituent operations group.   [sources: python_language_reference#expressions.html#evaluation-order]
note: Begin with this objective: Distinguish statements from expressions during Python evaluation.
note: Keep the example in the Scripts and source structure tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.comments, python.interactive_execution, python.interpreter_execution_model.
PRACTICE ANCHOR (live_code): Trace a short assignment sequence using quantity and cost, predicting each right-hand expression's value before its target is bound.  SUCCESS: Correctly predict cost as 14 and the later expression (quantity + 1) * 4 as 24, explaining why changing quantity does not recalculate cost.
ASSESSMENT ANCHOR: distinguish_expression_value_from_assignment_effect facts=['f1', 'f2']
ASSESSMENT ANCHOR: predict_evaluation_order_and_name_bindings facts=['f2', 'f3']

## SOURCE FACTS — C (python.comments)   objective: Write source comments that explain non-obvious intent.
C.f1: A # outside a string starts a comment extending to the physical line’s end; comments are ignored by syntax.   [sources: python_language_reference#lexical_analysis.html#comments]
C.f2: Keep comments accurate when code changes, because a comment contradicting code is worse than no comment.   [sources: pep8_style_guide#comments]
C.f3: Use inline comments sparingly and explain a useful reason rather than restating an obvious operation.   [sources: pep8_style_guide#inline-comments]
note: Begin with this objective: Write source comments that explain non-obvious intent.
note: Keep the example in the Scripts and source structure tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.interactive_execution, python.interpreter_execution_model, python.multiline_expressions.
PRACTICE ANCHOR (live_code): Add one comment explaining why the quantity check excludes zero: the fixed fee should apply only when at least one item is present.  SUCCESS: The comment accurately explains the reason for the quantity check without merely restating the comparison or changing the calculation.
ASSESSMENT ANCHOR: replace_misleading_or_redundant_comment_with_accurate_intent facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Avoiding unintended mutations through shared references; Checking for None with identity; Closures and enclosing scope; Constructing and resolving pathlib paths; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Inspecting program state with diagnostic printing; Investigating Python execution with a debugger; Lambda expressions; Ordering iterables with a key function; Passing and storing functions as values; Python comments; Python interpreter execution model; Raising exceptions; Reading Python tracebacks; Running Python interactively; Statements and expressions; Transforming text with string methods; Truth-value testing; Zip iteration

## LESSON, in learner order

### s01 · explainer · Running Python scripts
Learn — 
(definition) Choose the Python executable explicitly and pass the script path as its argument. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Script print output goes to standard output by default. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Zero exit status means successful termination; nonzero means abnormal termination. sys.exit(status) requests the status. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Terminal: invocation and separate signals] nodes=['report.py {print("Ready")}', 'selected_python report.py {Replace the executable placeholder with the actual chosen executable.}', 'Standard output {Ready; The displayed message is followed by a newline.}', 'Process exit status {0 — successful termination for this completed script.; This process status is separate from the printed message. Nonzero indicates abnormal termination; sys.exit(status) requests a status.}'] edges=[('file', 'command', None), ('command', 'stdout', None), ('command', 'status', None)] alt: A saved script is passed to a chosen executable. Standard output and process exit status are shown as separate signals.

### s02 · video · Running Python scripts
Optional walkthrough — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about running python scripts to choose the answer.

### s04 · hands_on · Judge running python scripts
Review the supplied examples — Read the supplied excerpts in this step and decide which are correct or defective for the stated task.

### s05 · explainer · Statements and expressions
Learn — 
(definition) An expression statement evaluates its expression. Interactive mode displays a non-None value. ⟦B.f1 B:tb2 B:tb4⟧
(definition) Assignment first evaluates the right-hand expression, then binds its result to the target. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Expressions are evaluated left to right. Operator precedence and parentheses still determine how operations group. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4 + 2
quantity = 5
print(cost)
print((quantity + 1) * 4)
  annotations: ['Evaluate 3, then bind `quantity = 3`.', 'Group as `(quantity * 4) + 2`; with quantity 3, compute 14, then bind `cost = 14`.', 'Bind `quantity = 5`; `cost` remains 14.', 'Displays 14.', 'Parentheses group `quantity + 1`: compute `(5 + 1) * 4 = 24`; displays 24.']

### s06 · check · Choose the right distinction
Check your understanding — Use what you learned about statements and expressions to choose the answer.

### s07 · hands_on · Practice statements and expressions
Try it — Trace a short assignment sequence using quantity and cost, predicting each right-hand expression's value before its target is bound.

### s08 · explainer · Python comments
Learn — 
(definition) Outside a string, # begins a comment through the physical line’s end. Syntax ignores comments. ⟦C.f1 C:tb2 C:tb4⟧
(definition) Update comments when code changes. A comment contradicting the code is worse than no comment. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Use inline comments sparingly. Explain a useful reason instead of repeating an obvious operation. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4 + 2  # This example includes a fixed fee of two.
print(cost)
print("# is text here")
  annotations: ['A comment does not prove that the code implements its description.']

### s09 · check · Choose the right distinction
Check your understanding — Use what you learned about python comments to choose the answer.

### s10 · hands_on · Practice python comments
Try it — Add one comment explaining why the quantity check excludes zero: the fixed fee should apply only when at least one item is present.

### s11 · recap · Keep these distinctions
Takeaways — 
(takeaway) Run a script with the explicitly chosen executable. Printed output and exit status are different signals. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Assignment evaluates before binding. Precedence and parentheses group operations within left-to-right evaluation. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Keep comments accurate and explain useful reasons, not obvious operations. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Running Python interactively: Next: Running Python interactively.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review running python scripts
(definition) Script print output goes to standard output by default. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Zero exit status means successful termination; nonzero means abnormal termination. sys.exit(status) requests the status. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A printed message and a process exit status are different signals. ⟦A.f2 A.f3 A:tb5⟧
(example) In the saved report example, inspect printed messages separately from the process status. ⟦A.f2 A.f3 A:tb4⟧
### r02 · Review running python scripts
(definition) Choose the Python executable explicitly and pass the script path as its argument. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Script print output goes to standard output by default. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Zero exit status means successful termination; nonzero means abnormal termination. sys.exit(status) requests the status. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A printed message and a process exit status are different signals. ⟦A.f2 A.f3 A:tb5⟧
(example) In the saved report example, inspect printed messages separately from the process status. ⟦A.f1 A.f2 A.f3 A:tb4⟧
### r03 · Review statements and expressions
(definition) Assignment first evaluates the right-hand expression, then binds its result to the target. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Expressions are evaluated left to right. Operator precedence and parentheses still determine how operations group. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Left-to-right evaluation does not cancel operator precedence. ⟦B.f3 B:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4 + 2
quantity = 5
print(cost)
print((quantity + 1) * 4)
  annotations: ['Left-to-right evaluation does not cancel operator precedence.']
### r04 · Review statements and expressions
(definition) An expression statement evaluates its expression. Interactive mode displays a non-None value. ⟦B.f1 B:tb2 B:tb4⟧
(definition) Assignment first evaluates the right-hand expression, then binds its result to the target. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Expressions are evaluated left to right. Operator precedence and parentheses still determine how operations group. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Left-to-right evaluation does not cancel operator precedence. ⟦B.f3 B:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4 + 2
quantity = 5
print(cost)
print((quantity + 1) * 4)
  annotations: ['Left-to-right evaluation does not cancel operator precedence.']
### r05 · Review python comments
(definition) Outside a string, # begins a comment through the physical line’s end. Syntax ignores comments. ⟦C.f1 C:tb2 C:tb4⟧
(definition) Update comments when code changes. A comment contradicting the code is worse than no comment. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Use inline comments sparingly. Explain a useful reason instead of repeating an obvious operation. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) A comment does not prove that the code implements its description. ⟦C.f2 C.f3 C:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4 + 2  # This example includes a fixed fee of two.
print(cost)
print("# is text here")
  annotations: ['A comment does not prove that the code implements its description.']

=========

# EVALUATOR PACKET — Running Python interactively · Python interpreter execution model · Continuing expressions across lines (learn_python.tile.038_040)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.interactive_execution — Running Python interactively
B = python.interpreter_execution_model — Python interpreter execution model
C = python.multiline_expressions — Continuing expressions across lines

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.interactive_execution)   objective: Use the interactive interpreter to investigate small expressions.
A.f1: Starting the interpreter without a script enters interactive mode, with >>> for a new command and ... for continuation.   [sources: python_tutorial#interpreter.html#interactive-mode]
A.f2: Entering an expression displays its result, and a variable assigned in the session can be used by later expressions.   [sources: python_tutorial#introduction.html#numbers]
A.f3: Type commands without copying the prompt characters; lines without prompts in tutorial examples are output.   [sources: python_tutorial#introduction.html]
note: Begin with this objective: Use the interactive interpreter to investigate small expressions.
note: Keep the example in the Interactive execution and expression layout tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.interpreter_execution_model, python.multiline_expressions, python.string_methods.
PRACTICE ANCHOR (live_code): Check the unfamiliar expression quantity * (4 + 1) in a fresh interactive session after assigning quantity = 3.  SUCCESS: Enter commands without prompt characters, observe the result 15, and explain how the expression uses the quantity value retained in the session.
ASSESSMENT ANCHOR: evaluate_expressions_using_retained_session_state facts=['f2']
ASSESSMENT ANCHOR: distinguish_interactive_prompts_commands_and_output facts=['f1', 'f3']

## SOURCE FACTS — B (python.interpreter_execution_model)   objective: Explain how Python executes source in a selected runtime.
B.f1: Source can be compiled to a code object; invalid source syntax raises SyntaxError.   [sources: python_stdlib_reference#functions.html#compile]
B.f2: In CPython, the compiler produces bytecode used by the interpreter; bytecode is an implementation detail, not a cross-implementation guarantee.   [sources: python_stdlib_reference#dis.html#module-dis]
B.f3: Top-level module statements execute when the module is first imported or when its file is executed as a script.   [sources: python_tutorial#modules.html#more-on-modules]
B.f4: At runtime, an assignment evaluates its expression using current values and binds the result to its target.   [sources: python_language_reference#simple_stmts.html#assignment-statements]
note: Begin with this objective: Explain how Python executes source in a selected runtime.
note: Keep the example in the Interactive execution and expression layout tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.multiline_expressions, python.string_methods, python.syntax_vs_runtime_errors.
PRACTICE ANCHOR (live_code): Trace the top-level execution of a supplied source file containing quantity = 3 followed by cost = quantity * 4, then execute it as a script in the interpreter.  SUCCESS: Identify that quantity is bound to 3 before cost is evaluated, and that cost is then bound to 12 using the current value of quantity.
ASSESSMENT ANCHOR: identify_parsing_and_cpython_compilation facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_top_level_execution_triggers facts=['f3']
ASSESSMENT ANCHOR: predict_runtime_assignment_bindings facts=['f4']

## SOURCE FACTS — C (python.multiline_expressions)   objective: Continue a Python expression across lines safely.
C.f1: Expressions inside parentheses, square brackets or braces may span physical lines without backslashes.   [sources: python_language_reference#lexical_analysis.html#implicit-line-joining]
C.f2: Keep the delimiters and expression intact when splitting a long call across lines; continuation indentation does not determine block grouping.   [sources: python_language_reference#lexical_analysis.html#implicit-line-joining]
C.f3: Align continuation arguments with the opening delimiter or use a hanging indent.   [sources: pep8_style_guide#indentation]
note: Begin with this objective: Continue a Python expression across lines safely.
note: Keep the example in the Interactive execution and expression layout tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.string_methods, python.syntax_vs_runtime_errors, python.truth_value_testing.
PRACTICE ANCHOR (live_code): Rewrite print("Cost", cost) across several lines inside its parentheses, using a hanging indent and preserving the arguments.  SUCCESS: The reformatted call uses implicit continuation without backslashes, retains both arguments in their original order, and displays Cost 14.
ASSESSMENT ANCHOR: reformat_expression_with_implicit_continuation_preserving_value facts=['f1', 'f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Avoiding unintended mutations through shared references; Binding variable arguments with *args and **kwargs; Checking for None with identity; Closures and enclosing scope; Constructing and resolving pathlib paths; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing input failures from programming defects; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Inspecting program state with diagnostic printing; Investigating Python execution with a debugger; Lambda expressions; Ordering iterables with a key function; Passing and storing functions as values; Python interpreter execution model; Raising exceptions; Reading Python tracebacks; Selecting specific exception handlers; Transforming text with string methods; Truth-value testing; Zip iteration

## LESSON, in learner order

### s01 · explainer · Running Python interactively
Learn — 
(definition) Start the interpreter without a script for interactive mode. >>> marks a new command; ... marks continuation. ⟦A.f1 A:tb2 A:tb4⟧
(definition) An entered expression displays its result. Later expressions can use variables assigned earlier in the session. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Copy commands without their prompt characters. In tutorial sessions, unprompted lines are output, not commands. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
>>> quantity = 3
>>> quantity * 4
12
  annotations: ['Lines beginning with `>>>` are entered commands; do not type the prompt characters.', 'The unprompted `12` is displayed output, not a command. `...` is the continuation prompt when a command needs more input.']

### s02 · check · Choose the right distinction
Check your understanding — Use what you learned about running python interactively to choose the answer.

### s03 · hands_on · Judge running python interactively
Review the supplied examples — Read the supplied excerpts in this step and decide which are correct or defective for the stated task.

### s04 · explainer · Python interpreter execution model
Learn — 
(definition) Source can compile to a code object. Invalid source syntax raises SyntaxError. ⟦B.f1 B:tb2⟧
(definition) CPython compiles to bytecode that its interpreter uses. Bytecode is an implementation detail, not a guarantee across Python implementations. ⟦B.f2 B:tb3⟧
(definition) Top-level module statements execute on first import or when the file runs as a script. ⟦B.f3 B:tb3⟧
(definition) At runtime, assignment evaluates the expression using current values, then binds the result to its target. ⟦B.f4 B:tb3⟧
[SIDE_BY_SIDE] Compilation validity and runtime evaluation are separate stages. left_label: From source to execution | right_label: Runtime bindings
  left:
[PROCESS_FLOW] nodes=['Source', 'Parse syntax', 'SyntaxError', 'Compile to code object — CPython produces implementation-specific bytecode.', 'Execute top-level statements — First import or script execution; assignment evaluates current values, then binds.'] edges=[('source', 'parse', None), ('parse', 'invalid', 'Invalid syntax'), ('parse', 'compile', 'Valid syntax'), ('compile', 'runtime', None)] alt: Source is parsed; invalid syntax raises SyntaxError. Valid source can compile to a code object and execute; CPython bytecode is implementation-specific.
  right:
[CODE python]
quantity = 3
cost = quantity * 4
  annotations: ['First evaluate 3, then bind `quantity = 3`.', 'Next evaluate `quantity * 4` using the current quantity 3, then bind `cost = 12`.']

### s05 · explainer · Python interpreter execution model
Learn — 
(example) In `quantity = 3`, then `cost = quantity * 4`, the second assignment uses the current value bound by the first. Top-level statements execute on first import or when the file runs as a script. Invalid source syntax raises SyntaxError when compilation is attempted. CPython produces bytecode for its interpreter, but that is not guaranteed across implementations. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧
(misconception) CPython bytecode is not a universal promise about every implementation. ⟦B.f2 B:tb5⟧

### s06 · check · Choose the right distinction
Check your understanding — Use what you learned about python interpreter execution model to choose the answer.

### s07 · check · Choose the right distinction
Check your understanding — Use what you learned about python interpreter execution model to choose the answer.

### s08 · hands_on · Practice python interpreter execution model
Try it — Trace the top-level execution of a supplied source file containing quantity = 3 followed by cost = quantity * 4, then execute it as a script in the interpreter.

### s09 · explainer · Continuing expressions across lines
Learn — 
(definition) Parentheses, square brackets and braces allow expressions to continue across physical lines without backslashes. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) Keep the expression and delimiters intact when splitting a call. Continuation indentation does not group statement blocks. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Align continued arguments with the opening delimiter, or use a hanging indent. ⟦C.f3 C:tb3 C:tb4⟧
[SIDE_BY_SIDE] Continuation spacing is not compound-statement block grouping. left_label: Single-line form | right_label: Continued form
  left:
[CODE python]
cost = (3 * 4 + 2)
print("Cost", cost)
  annotations: ['The calculation and call occupy single lines.']
  right:
[CODE python]
cost = (
    3 * 4
    + 2
)
print(
    "Cost",
    cost,
)
  annotations: ['Matching parentheses preserve the expressions; arguments use a hanging indent.']

### s10 · check · Choose the right distinction
Check your understanding — Use what you learned about continuing expressions across lines to choose the answer.

### s11 · hands_on · Practice continuing expressions across lines
Try it — Rewrite print("Cost", cost) across several lines inside its parentheses, using a hanging indent and preserving the arguments.

### s12 · recap · Keep these distinctions
Takeaways — 
(takeaway) Interactive prompts distinguish new commands from continuation; do not type the prompt markers. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Valid source can compile to a code object. CPython bytecode is implementation-specific; runtime assignments use current values. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Continue inside matching delimiters; continuation spacing is not block grouping. ⟦C.f1 C.f2 C.f3 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Transforming text with string methods: Next: Transforming text with string methods.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review running python interactively
(definition) Start the interpreter without a script for interactive mode. >>> marks a new command; ... marks continuation. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Copy commands without their prompt characters. In tutorial sessions, unprompted lines are output, not commands. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Prompt markers identify input; they are not source to type. ⟦A.f3 A:tb5⟧
[CODE python]
quantity = 3
quantity * 4
  annotations: ['Prompt markers identify input; they are not source to type.']
### r02 · Review running python interactively
(definition) Start the interpreter without a script for interactive mode. >>> marks a new command; ... marks continuation. ⟦A.f1 A:tb2 A:tb4⟧
(definition) An entered expression displays its result. Later expressions can use variables assigned earlier in the session. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Copy commands without their prompt characters. In tutorial sessions, unprompted lines are output, not commands. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Prompt markers identify input; they are not source to type. ⟦A.f3 A:tb5⟧
[CODE python]
quantity = 3
quantity * 4
  annotations: ['Prompt markers identify input; they are not source to type.']
### r03 · Review python interpreter execution model
(definition) Source can compile to a code object. Invalid source syntax raises SyntaxError. ⟦B.f1 B:tb2 B:tb4⟧
(definition) CPython compiles to bytecode that its interpreter uses. Bytecode is an implementation detail, not a guarantee across Python implementations. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) CPython bytecode is not a universal promise about every implementation. ⟦B.f2 B:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4
  annotations: ['CPython bytecode is not a universal promise about every implementation.']
### r04 · Review python interpreter execution model
(definition) At runtime, assignment evaluates the expression using current values, then binds the result to its target. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) CPython bytecode is not a universal promise about every implementation. ⟦B.f2 B:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4
  annotations: ['CPython bytecode is not a universal promise about every implementation.']
### r05 · Review python interpreter execution model
(definition) Top-level module statements execute on first import or when the file runs as a script. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) CPython bytecode is not a universal promise about every implementation. ⟦B.f2 B:tb5⟧
[CODE python]
quantity = 3
cost = quantity * 4
  annotations: ['CPython bytecode is not a universal promise about every implementation.']
### r06 · Review continuing expressions across lines
(definition) Parentheses, square brackets and braces allow expressions to continue across physical lines without backslashes. ⟦C.f1 C:tb1 C:tb2 C:tb4⟧
(definition) Keep the expression and delimiters intact when splitting a call. Continuation indentation does not group statement blocks. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Align continued arguments with the opening delimiter, or use a hanging indent. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) Continuation spacing is not compound-statement block grouping. ⟦C.f2 C:tb5⟧
[CODE python]
cost = (
    3 * 4
    + 2
)
print(
    "Cost",
    cost,
)
  annotations: ['Continuation spacing is not compound-statement block grouping.']

=========

# EVALUATOR PACKET — Transforming text with string methods (learn_python.tile.041_041)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.string_methods — Transforming text with string methods

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.string_methods)   objective: Transform and split text using string methods.
A.f1: text.strip() returns text with leading and trailing whitespace removed; it does not remove interior whitespace.   [sources: python_stdlib_reference#stdtypes.html#str.strip]
A.f2: The optional chars argument to strip is a set of removable characters, not a literal prefix or suffix.   [sources: python_stdlib_reference#stdtypes.html#str.strip]
A.f3: text.lower() returns a copy with cased characters converted to lowercase.   [sources: python_stdlib_reference#stdtypes.html#str.lower]
A.f4: text.split(separator) separates on that delimiter and preserves empty fields between repeated delimiters.   [sources: python_stdlib_reference#stdtypes.html#str.split]
A.f5: text.split() without a separator splits on runs of whitespace and omits leading and trailing empty fields.   [sources: python_stdlib_reference#stdtypes.html#str.split]
note: Begin with this objective: Transform and split text using string methods.
note: Keep the example in the String methods tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.syntax_vs_runtime_errors, python.truth_value_testing, python.none_and_identity.
PRACTICE ANCHOR (live_code): Normalize an entered label by removing surrounding whitespace and converting it to lowercase, then split comma-delimited and whitespace-separated text into fields.  SUCCESS: The normalized label is lowercase with surrounding whitespace removed. Comma splitting preserves the empty field between repeated commas; whitespace splitting produces fields without leading or trailing empty entries.
ASSESSMENT ANCHOR: select_methods_for_label_normalization facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: select_splitting_method_for_delimiters_and_whitespace facts=['f4', 'f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Avoiding unintended mutations through shared references; Binding variable arguments with *args and **kwargs; Checking for None with identity; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Counting values with collections.Counter; Distinguishing input failures from programming defects; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Inspecting program state with diagnostic printing; Investigating Python execution with a debugger; Lambda expressions; Ordering iterables with a key function; Passing and storing functions as values; Raising exceptions; Reading Python tracebacks; Selecting specific exception handlers; Truth-value testing; Zip iteration

## LESSON, in learner order

### s01 · explainer · Transforming text with string methods
Learn — 
(definition) strip() removes leading and trailing whitespace, not whitespace inside the text. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) The chars argument to strip describes removable edge characters, not a literal prefix or suffix. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) lower() returns a copy with cased characters changed to lowercase. ⟦A.f3 A:tb3 A:tb4⟧
(definition) With an explicit separator, split separates on that delimiter and keeps empty fields between repeated delimiters. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Without a separator, split() groups whitespace runs and omits leading and trailing empty fields. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] Removing edge whitespace is not the same operation as splitting fields. left_label: Clean edges and change case | right_label: Separate fields
  left:
[CODE python]
text = "  Blue  "
print(text.strip().lower())
print("xylabelyx".strip("xy"))
print("  red   blue  ".strip())
  annotations: ['Strip removes edge whitespace, not interior whitespace. Lower returns a lowercase copy; strip chars are removable characters.', "`text.strip()` returns `'Blue'`; applying `.lower()` returns `'blue'`.", "`'xylabelyx'.strip('xy')` returns `'label'`: x and y are removable edge characters, not a literal affix.", "Returns `'red   blue'`: the three interior spaces remain."]
  right:
[CODE python]
print("red,,blue".split(","))
print("  red   blue  ".split())
  annotations: ['An explicit delimiter preserves empty fields between repeated delimiters; whitespace splitting groups runs and omits edge empty fields.', "`'red,,blue'.split(',')` returns `['red', '', 'blue']`.", "`'  red   blue  '.split()` returns `['red', 'blue']`."]

### s02 · video · Transforming text with string methods
Optional walkthrough — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about transforming text with string methods to choose the answer.

### s04 · hands_on · Practice transforming text with string methods
Try it — Normalize an entered label by removing surrounding whitespace and converting it to lowercase, then split comma-delimited and whitespace-separated text into fields.

### s05 · recap · Keep these distinctions
Takeaways — 
(takeaway) Strip cleans edges, lower changes case, and split separates fields. Strip’s chars argument is a character set, not a literal substring. Explicit separators keep empty fields between repeated delimiters; whitespace splitting groups whitespace runs. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Distinguishing syntax and runtime errors: Next: Distinguishing syntax and runtime errors.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review transforming text with string methods
(definition) strip() removes leading and trailing whitespace, not whitespace inside the text. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) The chars argument to strip describes removable edge characters, not a literal prefix or suffix. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) lower() returns a copy with cased characters changed to lowercase. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Removing edge whitespace is not the same operation as splitting fields. ⟦A.f1 A.f2 A.f4 A.f5 A:tb5⟧
(example) In the supplied label examples, distinguish cleaning edges from choosing how to split fields. ⟦A.f1 A.f2 A.f3 A:tb4⟧
### r02 · Review transforming text with string methods
(definition) With an explicit separator, split separates on that delimiter and keeps empty fields between repeated delimiters. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(definition) Without a separator, split() groups whitespace runs and omits leading and trailing empty fields. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Removing edge whitespace is not the same operation as splitting fields. ⟦A.f1 A.f2 A.f4 A.f5 A:tb5⟧
(example) In the supplied label examples, distinguish cleaning edges from choosing how to split fields. ⟦A.f4 A.f5 A:tb4⟧

=========

# EVALUATOR PACKET — Distinguishing syntax and runtime errors (learn_python.tile.042_042)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.syntax_vs_runtime_errors — Distinguishing syntax and runtime errors

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.syntax_vs_runtime_errors)   objective: Distinguish syntax errors from runtime failures.
A.f1: Syntax errors occur while parsing source; the error report identifies the line and location where the parser detected invalid syntax.   [sources: python_tutorial#errors.html#syntax-errors]
A.f2: Syntactically valid code can raise an exception during execution; its error message identifies the exception type and explanation.   [sources: python_tutorial#errors.html#exceptions]
A.f3: Invalid syntax prevents the source from compiling to an executable code object, so repair the syntax before tracing that source’s runtime behavior.   [sources: python_stdlib_reference#functions.html#compile]
note: Begin with this objective: Distinguish syntax errors from runtime failures.
note: Keep the example in the Syntax versus runtime failures tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.truth_value_testing, python.none_and_identity, python.unicode_and_bytes.
PRACTICE ANCHOR (live_code): Repair a missing colon in an if statement before investigating the runtime exception caused by int("three") in its body.  SUCCESS: The source parses after the colon is restored. Executing it then produces ValueError, which the learner identifies as an execution failure caused by text unsuitable for integer conversion.
ASSESSMENT ANCHOR: classify_failure_by_parsing_or_execution facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_syntax_repair_as_prerequisite_to_execution facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Avoiding unintended mutations through shared references; Binding variable arguments with *args and **kwargs; Checking for None with identity; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Counting values with collections.Counter; Distinguishing input failures from programming defects; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Inspecting program state with diagnostic printing; Investigating Python execution with a debugger; Lambda expressions; Ordering iterables with a key function; Passing and storing functions as values; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers; Truth-value testing; Zip iteration

## LESSON, in learner order

### s01 · explainer · Distinguishing syntax and runtime errors
Learn — 
(definition) Syntax errors happen during parsing. The report points to the line and location where the parser detected invalid syntax. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Valid syntax can still raise an exception during execution. Read the exception type and explanation in its error message. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Invalid syntax blocks compilation to an executable code object. Repair it before tracing that source’s runtime behavior. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[BEFORE_AFTER] Repairing source structure is separate from investigating the runtime value.
  before:
[CODE python]
quantity = 1
if quantity > 0
    quantity = int("three")
  annotations: ['The header is missing its colon. Parsing detects invalid syntax; repair it before tracing execution.', "Parser report: `SyntaxError: expected ':'`; the detected location is the end of the `if quantity > 0` header, where its colon is missing."]
  after:
[CODE python]
quantity = 1
if quantity > 0:
    quantity = int("three")
  annotations: ['The colon repairs syntax. The conversion still raises ValueError during execution; read its exception type and explanation.', "Runtime report: `ValueError: invalid literal for int() with base 10: 'three'`. Parsing now succeeds, but converting this text to an integer fails during execution."]

### s02 · check · Choose the right distinction
Check your understanding — Use what you learned about distinguishing syntax and runtime errors to choose the answer.

### s03 · hands_on · Practice distinguishing syntax and runtime errors
Try it — Repair a missing colon in an if statement before investigating the runtime exception caused by int("three") in its body.

### s04 · recap · Keep these distinctions
Takeaways — 
(takeaway) Syntax errors arise during parsing; runtime exceptions arise during execution. Read the reported location or exception explanation, and fix invalid syntax before tracing runtime behavior. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Truth-value testing: Next: Truth-value testing.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review distinguishing syntax and runtime errors
(definition) Invalid syntax blocks compilation to an executable code object. Repair it before tracing that source’s runtime behavior. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Repair invalid syntax before inventing a runtime trace for it. ⟦A.f3 A:tb5⟧
[CODE python]
quantity = 1
if quantity > 0
    quantity = int("three")
  annotations: ['Repair invalid syntax before inventing a runtime trace for it.']
### r02 · Review distinguishing syntax and runtime errors
(definition) Syntax errors happen during parsing. The report points to the line and location where the parser detected invalid syntax. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Valid syntax can still raise an exception during execution. Read the exception type and explanation in its error message. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Invalid syntax blocks compilation to an executable code object. Repair it before tracing that source’s runtime behavior. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Repair invalid syntax before inventing a runtime trace for it. ⟦A.f3 A:tb5⟧
[CODE python]
quantity = 1
if quantity > 0
    quantity = int("three")
  annotations: ['Repair invalid syntax before inventing a runtime trace for it.']

=========

# EVALUATOR PACKET — Truth-value testing · Checking for None with identity (learn_python.tile.043_044)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.truth_value_testing — Truth-value testing
B = python.none_and_identity — Checking for None with identity

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.truth_value_testing)   objective: Use Python truth-value rules in conditions.
A.f1: False, None, numeric zero and empty built-in strings and collections have false truth values; nonzero numbers and nonempty built-in strings and collections have true truth values.   [sources: python_stdlib_reference#stdtypes.html#truth-value-testing]
A.f2: Use if collection: for a nonempty guard or if not collection: for an empty guard; truth testing does not require equality to True.   [sources: python_stdlib_reference#stdtypes.html#truth-value-testing]
note: Begin with this objective: Use Python truth-value rules in conditions.
note: Keep the example in the Truth values and absence tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.none_and_identity, python.unicode_and_bytes, python.zip_iteration.
PRACTICE ANCHOR (live_code): Write an empty-collection guard using if not quantities: without comparing quantities to True.  SUCCESS: The guard displays "No quantities" when quantities is empty and does not display it when quantities contains 3.
ASSESSMENT ANCHOR: predict_truth_values_of_empty_and_nonempty_collections facts=['f1']
ASSESSMENT ANCHOR: predict_truth_values_of_scalar_values facts=['f1']

## SOURCE FACTS — B (python.none_and_identity)   objective: Check for the absence sentinel None using identity.
B.f1: None is the singleton object commonly used to represent absence of a value.   [sources: python_stdlib_reference#stdtypes.html#the-null-object]
B.f2: is tests whether operands are the same object and is not tests whether they are different objects.   [sources: python_stdlib_reference#stdtypes.html#comparisons]
B.f3: Use value is None or value is not None to test absence rather than a truth test that would also reject a legitimate zero or empty value.   [sources: pep8_style_guide#programming-recommendations]
note: Begin with this objective: Check for the absence sentinel None using identity.
note: Keep the example in the Truth values and absence tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.unicode_and_bytes, python.zip_iteration, python.aliasing_mutability_and_copying.
PRACTICE ANCHOR (live_code): Handle an optional quantity lookup result using an explicit None check, preserving zero as a legitimate supplied quantity.  SUCCESS: The code reports quantity as supplied when it is zero and as absent when it is None.
ASSESSMENT ANCHOR: test_absence_with_identity facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: distinguish_absence_from_zero_and_empty_values facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Avoiding unintended mutations through shared references; Binding variable arguments with *args and **kwargs; Checking for None with identity; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Counting values with collections.Counter; Distinguishing input failures from programming defects; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Initialising instance state with __init__; Inspecting program state with diagnostic printing; Instance methods and self; Investigating Python execution with a debugger; Lambda expressions; Ordering iterables with a key function; Passing and storing functions as values; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers; Zip iteration

## LESSON, in learner order

### s01 · explainer · Truth-value testing
Learn — 
(definition) False, None, numeric zero, and empty built-in strings and collections test false. Nonzero numbers and nonempty built-in strings and collections test true. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Use if collection: for a nonempty guard, or if not collection: for an empty guard. No equality comparison to True is required. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
quantities = []
if not quantities:
    print("No quantities")
quantities = [3]
if quantities:
    print("Quantities available")
  annotations: ['An empty guard uses not; a nonempty guard uses the collection itself.']

### s02 · check · Choose the right distinction
Check your understanding — Use what you learned about truth-value testing to choose the answer.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about truth-value testing to choose the answer.

### s04 · hands_on · Practice truth-value testing
Try it — Write an empty-collection guard using if not quantities: without comparing quantities to True.

### s05 · explainer · Checking for None with identity
Learn — 
(definition) None is a singleton commonly used to mark an absent value. ⟦B.f1 B:tb2 B:tb4⟧
(definition) is asks whether two operands are the same object; is not asks whether they are different objects. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Test absence with value is None or value is not None. A truth test also rejects legitimate zero or empty values. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
quantity = 0
if quantity is not None:
    print("Quantity supplied", quantity)
quantity = None
if quantity is None:
    print("Quantity absent")
  annotations: ['For quantity 0, `quantity is not None` is true even though a truth test of quantity is false. For quantity None, `quantity is None` is true and a truth test is also false. Identity distinguishes absence from legitimate zero.']

### s06 · check · Choose the right distinction
Check your understanding — Use what you learned about checking for none with identity to choose the answer.

### s07 · check · Choose the right distinction
Check your understanding — Use what you learned about checking for none with identity to choose the answer.

### s08 · hands_on · Practice checking for none with identity
Try it — Handle an optional quantity lookup result using an explicit None check, preserving zero as a legitimate supplied quantity.

### s09 · recap · Keep these distinctions
Takeaways — 
(takeaway) Empty built-in collections test false; nonempty ones test true. Use the collection or not collection as the guard. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) None commonly marks absence. Identity checks distinguish it from legitimate zero or empty values that a truth test rejects. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Encoding and decoding Unicode text and bytes: Next: Encoding and decoding Unicode text and bytes.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review truth-value testing
(definition) False, None, numeric zero, and empty built-in strings and collections test false. Nonzero numbers and nonempty built-in strings and collections test true. ⟦A.f1 A:tb2 A:tb4⟧
(misconception) An empty guard uses not; a nonempty guard uses the collection itself. ⟦A.f2 A:tb5⟧
[CODE python]
quantities = []
if not quantities:
    print("No quantities")
quantities = [3]
if quantities:
    print("Quantities available")
  annotations: ['An empty guard uses not; a nonempty guard uses the collection itself.']
### r02 · Review truth-value testing
(definition) False, None, numeric zero, and empty built-in strings and collections test false. Nonzero numbers and nonempty built-in strings and collections test true. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Use if collection: for a nonempty guard, or if not collection: for an empty guard. No equality comparison to True is required. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) An empty guard uses not; a nonempty guard uses the collection itself. ⟦A.f2 A:tb5⟧
[CODE python]
quantities = []
if not quantities:
    print("No quantities")
quantities = [3]
if quantities:
    print("Quantities available")
  annotations: ['An empty guard uses not; a nonempty guard uses the collection itself.']
### r03 · Review checking for none with identity
(definition) None is a singleton commonly used to mark an absent value. ⟦B.f1 B:tb2 B:tb4⟧
(definition) is asks whether two operands are the same object; is not asks whether they are different objects. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Test absence with value is None or value is not None. A truth test also rejects legitimate zero or empty values. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) False truth is not the same as absence. ⟦B.f3 B:tb5⟧
[CODE python]
quantity = 0
if quantity is not None:
    print("Quantity supplied", quantity)
quantity = None
if quantity is None:
    print("Quantity absent")
  annotations: ['False truth is not the same as absence.']
### r04 · Review checking for none with identity
(definition) Test absence with value is None or value is not None. A truth test also rejects legitimate zero or empty values. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) False truth is not the same as absence. ⟦B.f3 B:tb5⟧
[CODE python]
quantity = 0
if quantity is not None:
    print("Quantity supplied", quantity)
quantity = None
if quantity is None:
    print("Quantity absent")
  annotations: ['False truth is not the same as absence.']

=========

# EVALUATOR PACKET — Encoding and decoding Unicode text and bytes (learn_python.tile.045_045)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.unicode_and_bytes — Encoding and decoding Unicode text and bytes

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.unicode_and_bytes)   objective: Encode and decode between Unicode strings and bytes.
A.f1: str contains Unicode text, distinct from binary bytes.   [sources: python_stdlib_reference#stdtypes.html#text-sequence-type-str]
A.f2: text.encode("utf-8") produces bytes using UTF-8.   [sources: python_stdlib_reference#stdtypes.html#str.encode]
A.f3: payload.decode("utf-8") produces text from UTF-8 bytes; the decoding encoding must match the encoded data to recover that text.   [sources: python_stdlib_reference#stdtypes.html#bytes.decode]
A.f4: A decoding failure raises UnicodeDecodeError when the supplied bytes are not valid for the chosen decoding.   [sources: python_stdlib_reference#exceptions.html#UnicodeDecodeError]
note: Begin with this objective: Encode and decode between Unicode strings and bytes.
note: Keep the example in the Unicode text and bytes tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.zip_iteration, python.aliasing_mutability_and_copying, python.collections_utilities.
PRACTICE ANCHOR (live_code): Encode the non-ASCII string "café" as UTF-8 bytes, then decode those bytes using UTF-8 to recover the original text.  SUCCESS: payload contains the UTF-8 bytes for "café", restored contains "café", and restored == text evaluates to True.
ASSESSMENT ANCHOR: round_trip_unicode_text_with_utf8 facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: recognize_invalid_byte_decoding_failures facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Avoiding shared mutable default arguments; Avoiding unintended mutations through shared references; Binding variable arguments with *args and **kwargs; Choosing instance, class or static method binding; Classes and instances; Closures and enclosing scope; Constructing and resolving pathlib paths; Counting values with collections.Counter; Distinguishing input failures from programming defects; Documenting Python interfaces with docstrings; Exception hierarchy; Exception propagation through calls; Guaranteed cleanup with finally; Initialising instance state with __init__; Inspecting program state with diagnostic printing; Instance methods and self; Investigating Python execution with a debugger; Lambda expressions; Ordering iterables with a key function; Passing and storing functions as values; Raising exceptions; Reading Python tracebacks; Selecting safe file-opening modes; Selecting specific exception handlers; Zip iteration

## LESSON, in learner order

### s01 · explainer · Encoding and decoding Unicode text and bytes
Learn — 
(definition) str holds Unicode text; bytes holds binary data. They are distinct kinds of values. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) text.encode("utf-8") produces bytes using UTF-8. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Decode UTF-8 bytes with payload.decode("utf-8") to get text. Match the decoding encoding to the encoded data to recover that text. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) Bytes invalid for the chosen decoding cause a decoding failure: UnicodeDecodeError. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
[CODE python]
text = "café"
payload = text.encode("utf-8")
restored = payload.decode("utf-8")
print(type(text))
print(type(payload))
print(restored)
print(restored == text)
  annotations: ['Encoded bytes are not already Unicode text.', "`text` is the Unicode string `'café'`.", "`payload` is the UTF-8 bytes value `b'caf\\xc3\\xa9'`, not a str.", "Matching UTF-8 decoding restores `'café'`.", "The displayed types are `<class 'str'>` and `<class 'bytes'>`.", 'Displays `café`.', 'Displays `True`: restored text equals the original text.']

### s02 · video · Encoding and decoding Unicode text and bytes
Optional walkthrough — 
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about encoding and decoding unicode text and bytes to choose the answer.

### s04 · check · Choose the right distinction
Check your understanding — Use what you learned about encoding and decoding unicode text and bytes to choose the answer.

### s05 · hands_on · Practice encoding and decoding unicode text and bytes
Try it — Encode the non-ASCII string "café" as UTF-8 bytes, then decode those bytes using UTF-8 to recover the original text.

### s06 · recap · Keep these distinctions
Takeaways — 
(takeaway) Unicode text and binary bytes are distinct. Encode to bytes, then decode with the matching encoding to recover text. Invalid bytes for the decoding raise UnicodeDecodeError. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Zip iteration: Next: Zip iteration.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Review encoding and decoding unicode text and bytes
(definition) str holds Unicode text; bytes holds binary data. They are distinct kinds of values. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) text.encode("utf-8") produces bytes using UTF-8. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Decode UTF-8 bytes with payload.decode("utf-8") to get text. Match the decoding encoding to the encoded data to recover that text. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Encoded bytes are not already Unicode text. ⟦A.f1 A.f3 A.f4 A:tb5⟧
[CODE python]
text = "café"
payload = text.encode("utf-8")
restored = payload.decode("utf-8")
print(type(text))
print(type(payload))
print(restored)
  annotations: ['Encoded bytes are not already Unicode text.']
### r02 · Review encoding and decoding unicode text and bytes
(definition) Decode UTF-8 bytes with payload.decode("utf-8") to get text. Match the decoding encoding to the encoded data to recover that text. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) Bytes invalid for the chosen decoding cause a decoding failure: UnicodeDecodeError. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Encoded bytes are not already Unicode text. ⟦A.f1 A.f3 A.f4 A:tb5⟧
[CODE python]
text = "café"
payload = text.encode("utf-8")
restored = payload.decode("utf-8")
print(type(text))
print(type(payload))
print(restored)
  annotations: ['Encoded bytes are not already Unicode text.']
### r03 · Review encoding and decoding unicode text and bytes
(definition) str holds Unicode text; bytes holds binary data. They are distinct kinds of values. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) text.encode("utf-8") produces bytes using UTF-8. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Decode UTF-8 bytes with payload.decode("utf-8") to get text. Match the decoding encoding to the encoded data to recover that text. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) Bytes invalid for the chosen decoding cause a decoding failure: UnicodeDecodeError. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Encoded bytes are not already Unicode text. ⟦A.f1 A.f3 A.f4 A:tb5⟧
[CODE python]
text = "café"
payload = text.encode("utf-8")
restored = payload.decode("utf-8")
print(type(text))
print(type(payload))
print(restored)
  annotations: ['Encoded bytes are not already Unicode text.']

## OTHER CONTENT (fields without a dedicated renderer)
· annotations.text: `payload` is the UTF-8 bytes value `b'caf\xc3\xa9'`, not a str.