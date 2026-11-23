# EVALUATOR PACKET — Choosing a built-in collection (learn_python.tile.026_026)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.collection_selection — Choosing a built-in collection

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.026_026.r02 is never referenced
  warn: remediation step learn_python.tile.026_026.r03 is never referenced
  warn: learn_python.tile.026_026.s05/ix.learn_python.tile.026_026.s05: ADVISORY — syntax descriptors with no detector: ['assert statements', 'dictionary item assignment', 'dictionary subscription by string key', 'integer literals', 'lambda expressions', 'nested collection literals', 'nested loops', 'nested subscription', 'string literals']

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
QUESTION [choice, intro, grading=client] Choose the collection types, in order: (1) ordered quantities that must be updated; (2) a fixed immutable ordered pair; (3) distinct labels for membership tests.
  ✔ a: list; tuple; set
      why: Correct: list; tuple; set
  ✘ b: tuple; list; set
      why: A tuple is immutable, whereas the first requirement needs updates; the second calls for an immutable tuple.
  ✘ c: list; tuple; list
      why: A list is a positional sequence, not the distinct-value collection specified for membership.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:choose_sequence_by_order_and_mutability(f1,f2); A:choose_set_for_distinct_values_and_membership(f3)   anchors=['assessment:choose_sequence_by_order_and_mutability', 'assessment:choose_set_for_distinct_values_and_membership']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · check · Choose the right distinction
Check your understanding — Use what you learned about choosing a built-in collection to choose the answer.
QUESTION [choice, core, grading=client] Quantities must be updated and retrieved by item label, not by position. Which collection meets that requirement?
  ✔ a: A dictionary mapping labels to quantities.
      why: Correct: A dictionary mapping labels to quantities.
  ✘ b: A tuple of quantities.
      why: A tuple is immutable and provides sequence positions, not label-based lookup.
  ✘ c: A set of quantities.
      why: A set stores distinct values, not a mapping from labels to quantities.
  ✘ d: A list of quantities accessed by position.
      why: The requirement is lookup by label, not by sequence position.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:choose_collection_from_storage_requirements(f1,f2,f3,f4)   anchors=['assessment:choose_collection_from_storage_requirements']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s05 · hands_on · Practice choosing a built-in collection
Try it — Create a lookup table for notebook and pen quantities, retrieve a quantity by label, and update it. Justify choosing a dictionary rather than an ordered list of quantities.
QUESTION [code_exercise, stretch, grading=client] Repair the three named inputs so the initial notebook lookup is 3, the updated notebook quantity is 5, pen remains 2, and justification explains label-based lookup rather than list positions. Keep the dictionary scaffold unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'integer literals', 'flat dictionary literals with string keys and integer values', 'flat list literals with integer values', 'dictionary subscription by string key', 'dictionary item assignment'] blocked=11 items
  file main.py [editable]:
notebook_quantity = 3
pen_quantity = 2
revised_quantity = 5
zero = 0
key_reason = "Labels require dictionary key lookup, not list positions; dictionary insertion order is not positional access."
position_reason = "Use sequence positions instead of label keys."
initial_notebook = zero
update_amount = pen_quantity
justification = position_reason
order = {"notebook": initial_notebook, "pen": pen_quantity}
selected = order["notebook"]
order["notebook"] = update_amount

  SOLUTION main.py:
notebook_quantity = 3
pen_quantity = 2
revised_quantity = 5
zero = 0
key_reason = "Labels require dictionary key lookup, not list positions; dictionary insertion order is not positional access."
position_reason = "Use sequence positions instead of label keys."
initial_notebook = notebook_quantity
update_amount = revised_quantity
justification = key_reason
order = {"notebook": initial_notebook, "pen": pen_quantity}
selected = order["notebook"]
order["notebook"] = update_amount

  test v1 (value_equals, visible=None): {"expr":"[selected, order, justification]","expected":[3,{"notebook":5,"pen":2},"Labels require dictionary key lookup, not list positions; dictionary insertion order is not positional access."]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ff1e1c79c4e8e729be16d86e7aaca24540f1cc9b347f9f637b060a8d6974e423","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:distinguish_key_lookup_from_positional_access(f1,f4)   anchors=['practice', 'assessment:distinguish_key_lookup_from_positional_access']
  taught-before-tested: A.f1←s01; A.f4←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.027_028.r02 is never referenced
  warn: remediation step learn_python.tile.027_028.r03 is never referenced
  warn: learn_python.tile.027_028.s07/ix.learn_python.tile.027_028.s07: ADVISORY — syntax descriptors with no detector: ['assert statements', 'generator expressions', 'indented for-loop body', 'integer literals', 'lambda expressions', 'list literals', 'nested for loops', 'string literals', 'yield']

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
QUESTION [choice, intro, grading=client] Which print call separates two values with a colon and space and ends with an exclamation mark followed by a newline?
  ✔ a: print("Selected", "pen", sep=": ", end="!\n")
      why: Correct: print("Selected", "pen", sep=": ", end="!\n")
  ✘ b: print("Selected", "pen")
      why: The defaults are a space between values and a newline at the end, not the requested delimiters.
  ✘ c: print("Selected", "pen", sep="!\n", end=": ")
      why: sep separates the values; end terminates the output. These arguments are reversed.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:display_values_with_default_and_custom_delimiters(f2)   anchors=['assessment:display_values_with_default_and_custom_delimiters']
  taught-before-tested: A.f2←s01

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about reading and displaying console values to choose the answer.
QUESTION [choice, core, grading=client] Ada is entered at the prompt. Which two lines store the entered text in label and then display Hello Ada with one space and a final newline?
  ✔ a: label = input("Name: ")
print("Hello", label)
      why: Correct: label = input("Name: ")
print("Hello", label)
  ✘ b: label = input("Name: ")
print("Hello", label, sep="")
      why: An empty separator removes the required space.
  ✘ c: label = input("Name: ")
print("Hello", label, end="")
      why: An empty end removes the required final newline.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:read_text_and_display_required_response(f1,f2)   anchors=['assessment:read_text_and_display_required_response']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Judge reading and displaying console values
Review the supplied examples — Read the supplied excerpts in this step and decide which are correct or defective for the stated task.
QUESTION [classify, stretch, grading=client] Read each supplied implementation for the same input Ada. Decide whether it requests a name, stores only the entered text in label, and displays Hello Ada with one space and a final newline.
  'label = input("Name: ")
print("Hello", label)' -> Meets the criterion
      feedback: input returns entered text without the prompt or trailing newline; print supplies the required space and newline.
  'label = input("Name: ")
print("Hello", label, sep="")' -> Violates the criterion
      feedback: An empty sep removes the space between Hello and Ada.
  'label = input("Name: ")
print("Hello", label, end="")' -> Violates the criterion
      feedback: An empty end removes the required final newline.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:read_entered_text_without_prompt_or_trailing_newline(f1)   anchors=['practice', 'assessment:read_entered_text_without_prompt_or_trailing_newline']
  taught-before-tested: A.f1←s01

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
QUESTION [choice, core, grading=client] Which loop header numbers labels from one while obtaining both the counter and the corresponding element?
  ✔ a: for position, label in enumerate(labels, start=1):
      why: Correct: for position, label in enumerate(labels, start=1):
  ✘ b: for position, label in enumerate(labels):
      why: The default counter begins at zero, not one.
  ✘ c: for position, label in enumerate(labels, start=2):
      why: This starts at two, not the specified one.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r04
  MEASURES: B:set_specified_starting_label(f1,f2)   anchors=['assessment:set_specified_starting_label']
  taught-before-tested: B.f1←s05; B.f2←s05

### s07 · hands_on · Practice enumerate iteration
Try it — Number the entries in labels from one using enumerate, without manual counter updates.
QUESTION [code_exercise, stretch, grading=client] Keep the supplied labels and loop unchanged. Set numbered_labels using enumerate so the loop obtains each label together with a counter starting at one.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'list literals', 'string literals', 'integer literals', 'for position, label in enumerate(labels, start=1):', 'enumerate(labels)', 'enumerate(labels, start=0)', 'indented for-loop body', 'print(position, label)'] blocked=7 items
  file main.py [editable]:
first_label = "notebook"
second_label = "pen"
third_label = "pencil"
one = 1
zero = 0
labels = [first_label, second_label, third_label]
numbered_labels = []
for position, label in numbered_labels:
    print(position, label)

  SOLUTION main.py:
first_label = "notebook"
second_label = "pen"
third_label = "pencil"
one = 1
zero = 0
labels = [first_label, second_label, third_label]
numbered_labels = enumerate(labels, start=1)
for position, label in numbered_labels:
    print(position, label)

  test output (stdout_equals, visible=None): {"expected":"1 notebook\n2 pen\n3 pencil\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"343252a2ba9680e92d48d4f8d11ceda81cbb8e82deb2cfe813e9d4a36c76971b","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: B:write_enumerate_loop_with_correct_counter_and_value(f1,f2)   anchors=['practice', 'assessment:write_enumerate_loop_with_correct_counter_and_value']
  taught-before-tested: B.f1←s05; B.f2←s05

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
· spec.expected: 1 notebook
2 pen
3 pencil

· expected.value: 1 notebook_x
2 pen
3 pencil
· expected.value: 1 notebook
2 pen_x
3 pencil

=========

# EVALUATOR PACKET — Floating-point approximation limits (learn_python.tile.029_029)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.floating_point_limits — Floating-point approximation limits

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.029_029.r02 is never referenced
  warn: learn_python.tile.029_029.s03/ix.learn_python.tile.029_029.s03: ADVISORY — syntax descriptors with no detector: ['+', '==', 'assert', 'class', 'integer and floating-point literals', 'raise', 'with', 'yield']

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
QUESTION [choice, intro, grading=client] A computed decimal sum is to be compared within a tolerance, rather than for exact equality. Which comparison is appropriate?
  ✔ a: math.isclose(a, b)
      why: Correct: math.isclose(a, b)
  ✘ b: a == b
      why: Exact equality does not apply a tolerance; binary floating-point representations can be approximate.
  ✘ c: Always declare the values unequal without comparing them.
      why: Approximate representation does not mean every pair is unequal; isclose compares using tolerances.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:choose_approximate_comparison_for_computed_float(f1,f2)   anchors=['assessment:choose_approximate_comparison_for_computed_float']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · hands_on · Practice floating-point approximation limits
Try it — Check the computed sum 0.1 + 0.2 against 0.3 using math.isclose, then check a small nonzero value against zero with an appropriate positive absolute tolerance.
QUESTION [code_exercise, stretch, grading=client] Keep the numeric inputs and supplied comparisons unchanged. Choose positive_tolerance from the supplied values so the near-zero comparison accepts the small nonzero difference. The checker reads False, True, True on three separate lines.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import math', 'print(...)', 'integer and floating-point literals', '+', '==', 'math.isclose(a, b)', 'math.isclose(a, b, rel_tol=..., abs_tol=...)'] blocked=10 items
  file main.py [editable]:
computed = 0.1 + 0.2
target = 0.3
near_zero = 0.000001
supplied_tolerance = 0.00001
zero = 0.0
positive_tolerance = zero
import math
print(computed == target)
print(math.isclose(computed, target))
print(math.isclose(near_zero, zero, abs_tol=positive_tolerance))

  SOLUTION main.py:
computed = 0.1 + 0.2
target = 0.3
near_zero = 0.000001
supplied_tolerance = 0.00001
zero = 0.0
positive_tolerance = supplied_tolerance
import math
print(computed == target)
print(math.isclose(computed, target))
print(math.isclose(near_zero, zero, abs_tol=positive_tolerance))

  test output (stdout_equals, visible=None): {"expected":"False\nTrue\nTrue\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"78376cb18c46d50bb0dbbcc82dfa6d3bdf1104474150a537b8cd73c8636a9a83","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:choose_positive_absolute_tolerance_near_zero(f3)   anchors=['practice', 'assessment:choose_positive_absolute_tolerance_near_zero']
  taught-before-tested: A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.030_030.r02 is never referenced
  warn: learn_python.tile.030_030.s05/ix.learn_python.tile.030_030.s05: ADVISORY — syntax descriptors with no detector: ['# comments', 'A for or while loop inside another loop', 'Addition with +', 'Assignment with =', 'Backslash line continuation', 'Colon-ended headers', 'Comparison with >', 'Four-space indentation levels and dedenting', 'Integer literals, including negative integers', 'List literals', 'assert statements', 'for quantity in [3, -1, 2]:', 'if quantity > 0:', 'lambda expressions', 'yield statements']

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
[VIDEO Grouping statements with indentation] bridge-before: Watch how indentation changes statement membership and how the second clip adds a deeper block. Both discuss alternative indentation widths; Devspace uses four spaces per level. A block is the header's multi-line suite. | bridge-after: The first clip does not explain deeper nesting or the colon-ended header requirement; the text covers both. The second demonstrates nested conditions; the text applies the same grouping rules to a condition inside a loop.
  - aWe2BfHXnik 29-193s facts=['f2', 'f3'] label: Recognise block membership and repair inconsistent indentation | summary: Indentation determines which statements belong to an if body. Statements aligned within that body share its condition; an unindented statement following it is outside the body. The example uses x = 10 and compares x with 5. Giving statements in the same body different indentation produces errors; aligning them consistently repairs the structure. Although consistent two-space indentation can work, use four spaces per level.
  - CcgSYrWwSpE 0-398s facts=['f1', 'f2', 'f3'] label: Build indented bodies and add a deeper nested block | summary: An if header ends with a colon, and its indented statements run only when its condition is true. Moving a following statement into or out of that indentation changes whether it belongs to the conditional body. Inconsistent spacing produces an indentation error. Tabs and spaces are different characters, and mixing them can fail even when their alignment looks similar. Use four spaces per level rather than the alternative widths discussed. An if inside another if introduces a deeper body, indented another four spaces.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about indentation and code blocks to choose the answer.
QUESTION [choice, intro, grading=client] A loop is at the outer level. An if condition must belong to the loop, its addition must belong to the condition, and the final report must run after the loop. Using four spaces per level, choose their leading-space counts in that order.
  ✔ a: 4, 8, 0
      why: Correct: 4, 8, 0
  ✘ b: 0, 4, 0
      why: The condition at zero spaces would be outside the loop rather than in its suite.
  ✘ c: 4, 4, 4
      why: The addition must be deeper than the condition, and the final report must be dedented out of the loop.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:repair_wrongly_nested_block(f1,f2,f3)   anchors=['assessment:repair_wrongly_nested_block']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · check · Choose the right distinction
Check your understanding — Use what you learned about indentation and code blocks to choose the answer.
QUESTION [choice, core, grading=client] Read the block structure:
```python
for quantity in [3, 2]:
    if quantity > 0:
        total = total + quantity
    print(total)
```
Where does print(total) belong?
  ✔ a: Inside the loop, but outside the if suite.
      why: Correct: Inside the loop, but outside the if suite.
  ✘ b: Inside both the loop and the if suite.
      why: The print is dedented from the if body, so it is not part of that deeper suite.
  ✘ c: Outside the loop.
      why: It still has one indentation level beneath the loop header.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:predict_statement_suite_membership(f1,f2)   anchors=['assessment:predict_statement_suite_membership']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · hands_on · Practice indentation and code blocks
Try it — Correct the indentation of the quantity condition inside the loop, its total update, and the final report using four spaces per level.
QUESTION [code_exercise, stretch, grading=client] Choose condition_indent, addition_indent, and report_indent from the supplied indentation values so the condition belongs to the loop, the addition belongs to the condition, and the report is outside the loop. Keep statement text and input values unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['Integer literals, including negative integers', 'List literals', 'Assignment with =', 'Addition with +', 'Comparison with >', 'for quantity in [3, -1, 2]:', 'if quantity > 0:', 'print(total)', 'Colon-ended headers', 'Four-space indentation levels and dedenting'] blocked=9 items
  file main.py [editable]:
first_quantity = 3
second_quantity = -1
third_quantity = 2
one_level = "    "
two_levels = "        "
outer_level = ""
condition_indent = outer_level
addition_indent = outer_level
report_indent = one_level
source = "total = 0\nfor quantity in [first_quantity, second_quantity, third_quantity]:\n" + condition_indent + "if quantity > 0:\n" + addition_indent + "total = total + quantity\n" + report_indent + "print(total)\n"
exec(source)

  SOLUTION main.py:
first_quantity = 3
second_quantity = -1
third_quantity = 2
one_level = "    "
two_levels = "        "
outer_level = ""
condition_indent = one_level
addition_indent = two_levels
report_indent = outer_level
source = "total = 0\nfor quantity in [first_quantity, second_quantity, third_quantity]:\n" + condition_indent + "if quantity > 0:\n" + addition_indent + "total = total + quantity\n" + report_indent + "print(total)\n"
exec(source)

  test output (stdout_equals, visible=None): {"expected":"5\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6dcb4f3a39e0920f7d018449511648f4975e52e733578be667e84d61a559ceba","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:repair_wrongly_nested_block(f1,f2,f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.031_031.r02 is never referenced
  warn: learn_python.tile.031_031.s04/ix.learn_python.tile.031_031.s04: ADVISORY — syntax descriptors with no detector: ['assert statements', 'floating-point literals', 'integer literals', 'lambda expressions', 'nested collection indexing', 'nested for or while loops', 'raise statements']

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
[VIDEO Import math and calculate real square roots] bridge-before: Watch how importing math enables the qualified call math.sqrt(25). The presenter initially calls sqrt an inbuilt function; Devspace uses the more precise term standard-library module function. | bridge-after: The clip demonstrates square roots of positive inputs. It does not explain the real-valued domain or negative-input ValueError; the text covers both, including math.sqrt(-1.0).
  - EkYrfV7M1ks 27-108s facts=['f1'] label: Import math and calculate a square root | summary: An initial attempt to use sqrt without the module name fails. Importing math and calling math.sqrt(25) produces a value that is stored and printed as 5.0. A second calculation uses 15 to demonstrate the same operation with another positive input. Although the presenter initially calls sqrt an inbuilt function, the demonstrated interface is the standard-library function math.sqrt.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about using math for numeric calculations to choose the answer.
QUESTION [choice, intro, grading=client] After import math, what happens when math.sqrt(-1.0) is evaluated?
  ✔ a: It raises ValueError because this math operation is invalid for that real input.
      why: Correct: It raises ValueError because this math operation is invalid for that real input.
  ✘ b: It returns a complex square root.
      why: The math functions here operate on real rather than complex values.
  ✘ c: It returns the square root of 1.0 instead.
      why: sqrt does not discard the negative sign; the negative real argument is invalid.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:recognize_math_sqrt_domain_and_invalid_input(f2)   anchors=['assessment:recognize_math_sqrt_domain_and_invalid_input']
  taught-before-tested: A.f2←s01

### s04 · hands_on · Practice using math for numeric calculations
Try it — Use math.sqrt to calculate the side length of a square with area 9 square units.
QUESTION [code_exercise, stretch, grading=client] Keep area unchanged. Include import math in your own added lines, then print math.sqrt(area), displaying only the numeric side length with a final newline.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import math', 'math.sqrt(...)', 'integer literals', 'floating-point literals', 'print(...)'] blocked=7 items
  file main.py [editable]:
area = 9

  SOLUTION main.py:
area = 9
import math
print(math.sqrt(area))

  test output (stdout_equals, visible=None): {"expected":"3.0\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6f6f62f51475adc8747e28973e3138944475bc0c2b09a53c1e90f168234a53bc","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:select_and_apply_math_sqrt(f1)   anchors=['practice', 'assessment:select_and_apply_math_sqrt']
  taught-before-tested: A.f1←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: remediation step learn_python.tile.032_034.r04 is never referenced
  warn: remediation step learn_python.tile.032_034.r05 is never referenced
  warn: learn_python.tile.032_034.s04/ix.learn_python.tile.032_034.s04: ADVISORY — syntax descriptors with no detector: ['Assignment expressions using :=', 'Backslash line continuation', 'Class definitions', 'Comment syntax using #', 'Dictionary literals', 'Dictionary lookup with [key]', 'List literals', 'Nested for or while loops', 'String and integer literals', 'Successive bracket selections', 'Variable assignment with =', 'assert statements', 'lambda expressions']
  warn: learn_python.tile.032_034.s07/ix.learn_python.tile.032_034.s07: ADVISORY — syntax descriptors with no detector: ['assert statements', 'for cell in row:', 'for row in rows:', 'generator expressions', 'indented loop bodies', 'integer literals', 'lambda expressions', 'nested list literals', 'variable assignment with =', 'yield']
  warn: learn_python.tile.032_034.s11/ix.learn_python.tile.032_034.s11: ADVISORY — syntax descriptors with no detector: ['assert', 'class', 'indented loop bodies', 'integer literals', 'negative integer literals', 'yield']

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
[VIDEO Selecting values inside nested collections] bridge-before: Watch how each index selects one level deeper. The clip calls these “2D” or “multi-dimensional” lists; here, they are nested collections containing other lists. | bridge-after: Successive indices reach an inner item. The clip does not cover dictionary-key selection or nested assignment; the text teaches both through the order quantities example.
  - EWbET9xdHUE 19-193s facts=['f1'] label: Access values in a list of lists using successive indices | summary: A list can hold other lists as its elements. Separate lists of drinks, dinner items, and desserts are placed inside a list named food. The inner lists need not contain the same number of items. Selecting food[0] retrieves the drinks list; adding another index, food[0][0], retrieves coffee. Changing the outer index selects a different inner list: food[1][2] selects hot dog from the dinner list. Each pair of brackets selects one level deeper.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about accessing and updating nested collections to choose the answer.
QUESTION [choice, intro, grading=client] For order = [{"quantities": [3, 2]}], which assignment changes only the second quantity of the first order to 5?
  ✔ a: order[0]["quantities"][1] = 5
      why: Correct: order[0]["quantities"][1] = 5
  ✘ b: order[0]["quantities"][0] = 5
      why: Index zero selects the first quantity, not the second.
  ✘ c: order[0]["quantities"] = 5
      why: This replaces the entire quantities list, rather than its second entry.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:follow_keys_and_indices_to_update_a_nested_record(f1,f2)   anchors=['assessment:follow_keys_and_indices_to_update_a_nested_record']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Practice accessing and updating nested collections
Try it — Update the second quantity in an order dictionary stored inside a list of order records.
QUESTION [code_exercise, stretch, grading=client] Keep the supplied order structure and bracket-selection assignment unchanged. Choose replacement_quantity from the supplied quantity values so only the second quantity of the first order becomes 5. Preserve the surrounding list and dictionary.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['Variable assignment with =', 'List literals', 'Dictionary literals', 'String and integer literals', 'List indexing with [index]', 'Dictionary lookup with [key]', 'Successive bracket selections', 'Assignment to a selected list index or dictionary key'] blocked=8 items
  file main.py [editable]:
first_quantity = 3
second_quantity = 2
revised_quantity = 5
order = [{"quantities": [first_quantity, second_quantity]}]
replacement_quantity = second_quantity
order[0]["quantities"][1] = replacement_quantity

  SOLUTION main.py:
first_quantity = 3
second_quantity = 2
revised_quantity = 5
order = [{"quantities": [first_quantity, second_quantity]}]
replacement_quantity = revised_quantity
order[0]["quantities"][1] = replacement_quantity

  test v1 (value_equals, visible=None): {"expr":"order","expected":[{"quantities":[3,5]}]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"7cea685e5f86031d6d64b46ad1135486a23f499703c254ad0fcd3e27cd9aad01","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:follow_keys_and_indices_to_update_a_nested_record(f1,f2)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01

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
QUESTION [choice, core, grading=client] For rows = [[3, 2], [5, 4]], an outer loop uses for row in rows: and its inner loop uses for cell in row:. What is the cell traversal order?
  ✔ a: 3, 2, 5, 4
      why: Correct: 3, 2, 5, 4
  ✘ b: 3, 5, 2, 4
      why: The inner loop finishes the current row before proceeding to the next row; this interleaves rows.
  ✘ c: 3, 2, 3, 2
      why: The outer loop advances to the second row; it does not always traverse the first row.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r02
  MEASURES: B:predict_row_cell_iteration_pairs(f1,f2)   anchors=['assessment:predict_row_cell_iteration_pairs']
  taught-before-tested: B.f1←s05; B.f2←s05

### s07 · hands_on · Practice nested loops
Try it — Write nested for loops to visit and display each cell in rows = [[3, 2], [5, 4]], completing each row before moving to the next.
QUESTION [code_exercise, stretch, grading=client] The nested list in supplied_rows and both nested loops are supplied. Keep them and the four input variables unchanged. Replace rows = [] with an assignment binding rows to supplied_rows. Before running, trace how the inner loop uses the current row. Each cell must print once on its own line, completing each row before advancing.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'integer literals', 'nested list literals', 'for row in rows:', 'for cell in row:', 'indented loop bodies', 'print(cell)'] blocked=7 items
  file main.py [editable]:
first = 3
second = 2
third = 5
fourth = 4
supplied_rows = [[first, second], [third, fourth]]
rows = []
for row in rows:
    for cell in row:
        print(cell)

  SOLUTION main.py:
first = 3
second = 2
third = 5
fourth = 4
supplied_rows = [[first, second], [third, fourth]]
rows = supplied_rows
for row in rows:
    for cell in row:
        print(cell)

  test output (stdout_equals, visible=None): {"expected":"3\n2\n5\n4\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9df9a5d44604f30a2025cdcc6e2a71ad71c742d7b1ba256691114e648c4d5753","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: B:produce_row_by_row_nested_traversal(f1,f2)   anchors=['practice', 'assessment:produce_row_by_row_nested_traversal']
  taught-before-tested: B.f1←s05; B.f2←s05

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
QUESTION [choice, core, grading=client] Which description of range(6) is correct?
  ✔ a: It starts at zero and uses step one.
      why: Correct: It starts at zero and uses step one.
  ✘ b: It starts at one and uses step one.
      why: With one stop argument, the default start is zero.
  ✘ c: It starts at zero and uses step zero.
      why: The default step is one; range requires a nonzero step.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r03
  MEASURES: C:choose_range_start_and_default_step(f1)   anchors=['assessment:choose_range_start_and_default_step']
  taught-before-tested: C.f1←s08

### s10 · check · Choose the right distinction
Check your understanding — Use what you learned about using range for counted iteration to choose the answer.
QUESTION [choice, core, grading=client] Which range produces decreasing integers from 5 through 1, excluding zero?
  ✔ a: range(5, 0, -1)
      why: Correct: range(5, 0, -1)
  ✘ b: range(5, 1, -1)
      why: The stop is excluded, so stopping at 1 leaves out 1.
  ✘ c: range(5, 0, 1)
      why: A positive step does not move down from 5 toward the smaller stop.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: C:choose_excluded_stop_and_directional_step(f1,f2)   anchors=['assessment:choose_excluded_stop_and_directional_step']
  taught-before-tested: C.f1←s08; C.f2←s08

### s11 · hands_on · Practice using range for counted iteration
Try it — Process every second integer position from zero up to the excluded limit of six using a for loop with range.
QUESTION [code_exercise, stretch, grading=client] Keep the supplied inputs and loop unchanged. Set positions using range so the loop prints every second position starting at zero, excludes limit, and prints each selected position once on its own line.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['for index in range(start, stop, step):', 'range(stop)', 'integer literals', 'negative integer literals', 'indented loop bodies', 'print(index)'] blocked=6 items
  file main.py [editable]:
limit = 6
every_second = 2
zero = 0
positions = []
for index in positions:
    print(index)

  SOLUTION main.py:
limit = 6
every_second = 2
zero = 0
positions = range(zero, limit, every_second)
for index in positions:
    print(index)

  test output (stdout_equals, visible=None): {"expected":"0\n2\n4\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"665fdb813cb8886ac8d44eff9bb61fa398ebc163909653649fd9d1a2c8930293","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: C:choose_range_values_for_every_second_position(f1,f2,f3)   anchors=['practice', 'assessment:choose_range_values_for_every_second_position']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f3←s08

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step learn_python.tile.035_037.r02 is never referenced
  warn: remediation step learn_python.tile.035_037.r04 is never referenced
  warn: learn_python.tile.035_037.s07/ix.learn_python.tile.035_037.s07: ADVISORY — syntax descriptors with no detector: ['addition with +', 'assert statements', 'assignment expressions with :=', 'backslash line continuation', 'comments with #', 'expressions continued across multiple lines', 'identity tests with is or is not', 'integer literals', 'lambda expressions', 'multiplication with *', 'parenthesized expressions', 'quantity and cost variable references', 'single-target assignment with =', 'yield expressions']
  warn: learn_python.tile.035_037.s10/ix.learn_python.tile.035_037.s10: ADVISORY — syntax descriptors with no detector: ['# comments', '>= comparison', 'addition', 'assert statements', 'backslash line continuation', 'function docstrings', 'if statements with indented bodies', 'integer literals', 'is and is not comparisons', 'lambda expressions', 'multiplication', 'raise statements', 'yield statements']

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
[VIDEO Save a script and run it by path] bridge-before: Watch how saving the file precedes execution and how the terminal command pairs an executable with a script path. The clip uses python; use your explicitly chosen executable instead. | bridge-after: The clip demonstrates saving and invoking a script, but does not explain standard output or exit status. The text covers both, including requesting a status with sys.exit(status).
  - NfTrFhfqmFY 260-358s facts=['f1'] label: Save a Python script and invoke it from a terminal | summary: Create hello.py, enter print("hello world"), and save the file before running it. The editor’s unsaved-change indicator helps confirm that edits have been saved. Running the file with the editor’s play button displays hello world in its built-in terminal. The same saved script can be run directly by entering python hello.py in that terminal: the executable name comes first, followed by the script path.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about running python scripts to choose the answer.
QUESTION [choice, intro, grading=client] A script prints Ready and requests exit status 2. Which statement correctly distinguishes these observations?
  ✔ a: Ready is standard output; 2 is a separate nonzero process status indicating abnormal termination.
      why: Correct: Ready is standard output; 2 is a separate nonzero process status indicating abnormal termination.
  ✘ b: Ready is the exit status and 2 is printed text.
      why: print sends text to standard output; the process status is a separate result.
  ✘ c: Printing Ready guarantees exit status zero.
      why: Printed output does not determine the requested process status.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:distinguish_printed_output_from_exit_status(f2,f3)   anchors=['assessment:distinguish_printed_output_from_exit_status']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Judge running python scripts
Review the supplied examples — Read the supplied excerpts in this step and decide which are correct or defective for the stated task.
QUESTION [classify, stretch, grading=client] Read each recorded pair of script runs. The supplied executable is selected_python and the saved file is report.py. Decide whether the record meets the criterion: explicit executable plus script path, Ready on standard output in both runs, and separately requested process statuses changing from 0 to 2.
  'Command for both saved versions: selected_python report.py
Version A: import sys; print("Ready"); sys.exit(0)
Recorded stdout: Ready\n ; process status: 0
Version B: import sys; print("Ready"); sys.exit(2)
Recorded stdout: Ready\n ; process status: 2' -> Meets the criterion
      feedback: The explicit executable receives the script path; printed output stays the same while requested statuses change.
  'Command: selected_python
Saved report.py contains print("Ready")
Record claims that this command executed report.py.' -> Violates the criterion
      feedback: No script path was passed to the selected executable, so this does not demonstrate invocation of the saved script.
  'Command for both versions: selected_python report.py
Version A: import sys; print("Ready"); sys.exit(0)
Version B: import sys; print("Ready"); sys.exit(2)
Record labels Ready as the process status and 0/2 as standard output.' -> Violates the criterion
      feedback: The record swaps printed standard output with the separate requested process statuses.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:invoke_script_with_explicit_executable(f1); A:identify_default_standard_output(f2); A:interpret_and_request_process_exit_status(f3); A:distinguish_printed_output_from_exit_status(f2,f3)   anchors=['practice', 'assessment:invoke_script_with_explicit_executable', 'assessment:identify_default_standard_output', 'assessment:interpret_and_request_process_exit_status', 'assessment:distinguish_printed_output_from_exit_status']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f2←s01; A.f3←s01

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
QUESTION [choice, core, grading=client] Read quantity = 3; cost = quantity * 4 + 2; quantity = 5 (as three statements in that order). Does the last assignment recalculate cost?
  ✔ a: No. cost keeps the previously evaluated result; quantity is rebound to 5.
      why: Correct: No. cost keeps the previously evaluated result; quantity is rebound to 5.
  ✘ b: Yes. cost is a live formula that updates whenever quantity changes.
      why: Assignment evaluates its right-hand expression before binding a value; it does not store a live formula.
  ✘ c: No. The last assignment cannot change quantity once it has a value.
      why: Assignment can rebind quantity; it is cost that retains its earlier result.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r03
  MEASURES: B:predict_evaluation_order_and_name_bindings(f2,f3)   anchors=['assessment:predict_evaluation_order_and_name_bindings']
  taught-before-tested: B.f2←s05; B.f3←s05

### s07 · hands_on · Practice statements and expressions
Try it — Trace a short assignment sequence using quantity and cost, predicting each right-hand expression's value before its target is bound.
QUESTION [code_exercise, stretch, grading=client] Trace the supplied assignments before running. The scaffold computes cost using the initial quantity, then changes quantity and computes later. Correct only output selection: first_output = cost and second_output = later. Do not change arithmetic or inputs. Print the stored cost followed by the later expression result on separate lines. Explain in your trace why cost keeps the old evaluated result rather than recalculating after quantity is rebound.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['integer literals', 'quantity and cost variable references', 'single-target assignment with =', 'addition with +', 'multiplication with *', 'parenthesized expressions', 'print() with a single numeric expression'] blocked=9 items
  file main.py [editable]:
initial_quantity = 3
new_quantity = 5
quantity = initial_quantity
cost = quantity * 4 + 2
quantity = new_quantity
later = (quantity + 1) * 4
first_output = quantity
second_output = cost
print(first_output)
print(second_output)

  SOLUTION main.py:
initial_quantity = 3
new_quantity = 5
quantity = initial_quantity
cost = quantity * 4 + 2
quantity = new_quantity
later = (quantity + 1) * 4
first_output = cost
second_output = later
print(first_output)
print(second_output)

  test output (stdout_equals, visible=None): {"expected":"14\n24\n"} | on-fail: Check the required printed values and delimiters.
  test v1 (value_equals, visible=None): {"expr":"[cost, quantity]","expected":[14,5]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5df153aff07156f830588ae32de312468765bf5e1ea5f378357a50e1e7d515b7","tests_passed":2}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: B:distinguish_expression_value_from_assignment_effect(f1,f2); B:predict_evaluation_order_and_name_bindings(f2,f3)   anchors=['practice', 'assessment:distinguish_expression_value_from_assignment_effect', 'assessment:predict_evaluation_order_and_name_bindings']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f2←s05; B.f3←s05

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
QUESTION [choice, core, grading=client] The fixed fee applies only when at least one item is present. Which comment accurately explains the reason for if quantity >= 1: before cost = quantity * 4 + 2?
  ✔ a: # Exclude zero so no fixed fee is charged when no items are present.
      why: Correct: # Exclude zero so no fixed fee is charged when no items are present.
  ✘ b: # Compare quantity with one.
      why: This merely restates the comparison instead of explaining its non-obvious purpose.
  ✘ c: # Charge the fixed fee even when there are no items.
      why: That contradicts the quantity check and the stated fee rule.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r05
  MEASURES: C:replace_misleading_or_redundant_comment_with_accurate_intent(f1,f2,f3)   anchors=['assessment:replace_misleading_or_redundant_comment_with_accurate_intent']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f3←s08

### s10 · hands_on · Practice python comments
Try it — Add one comment explaining why the quantity check excludes zero: the fixed fee should apply only when at least one item is present.
QUESTION [code_exercise, stretch, grading=client] ### Insert an accurate reason comment

Insert the supplied reason comment immediately above the quantity check without changing executable statements.

# Exclude zero so no fixed fee is charged when no items are present.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['# comments', 'variable assignment', 'integer literals', '>= comparison', 'if statements with indented bodies', 'multiplication', 'addition'] blocked=7 items
  file main.py [editable]:
quantity = 3
cost = 0
if quantity >= 1:
    cost = quantity * 4 + 2

  SOLUTION main.py:
quantity = 3
cost = 0
# Exclude zero so no fixed fee is charged when no items are present.
if quantity >= 1:
    cost = quantity * 4 + 2

  test v1 (value_equals, visible=None): {"expr":"[cost, \"# Exclude zero so no fixed fee is charged when no items are present.\\nif quantity >= 1:\" in open(\"main.py\").read()]","expected":[14,true]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"68370aa58cfc393c01b2059e2ac454828ed75c8b1ee73b96a05dac68b0d04cdf","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: C:replace_misleading_or_redundant_comment_with_accurate_intent(f1,f2,f3)   anchors=['practice']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f3←s08

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

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expr: [cost, "# Exclude zero so no fixed fee is charged when no items are present.\nif quantity >= 1:" in open("main.py").read()]

=========

# EVALUATOR PACKET — Running Python interactively · Python interpreter execution model · Continuing expressions across lines (learn_python.tile.038_040)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.interactive_execution — Running Python interactively
B = python.interpreter_execution_model — Python interpreter execution model
C = python.multiline_expressions — Continuing expressions across lines

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=6
  warn: remediation step learn_python.tile.038_040.r02 is never referenced
  warn: remediation step learn_python.tile.038_040.r04 is never referenced
  warn: remediation step learn_python.tile.038_040.r05 is never referenced
  warn: learn_python.tile.038_040.s08/ix.learn_python.tile.038_040.s08: ADVISORY — syntax descriptors with no detector: ['assert statements', 'assignment with =', 'backslash line continuation', 'class statements', 'finally clauses', 'integer literals', 'lambda expressions', 'multiplication with *', 'raise statements', 'variable references', 'with statements', 'yield expressions']
  warn: learn_python.tile.038_040.s11/ix.learn_python.tile.038_040.s11: ADVISORY — syntax descriptors with no detector: ['*args and **kwargs parameter declarations', 'arithmetic multiplication and addition', 'assert statements', 'class declarations', 'generator expressions', 'hanging indentation', 'integer and string literals', 'lambda expressions', 'optional trailing comma in a function call', 'parentheses for implicit continuation', 'raise statements', 'starred argument unpacking', 'string transformation method calls', 'with statements', 'yield']
  warn: plan: learn_python.tile.038_040.s08 was planned to measure python.interpreter_execution_model#assessment:identify_top_level_execution_triggers but its interaction does not

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
QUESTION [choice, intro, grading=client] In an interactive tutorial, >>> quantity = 3 is followed by >>> quantity * 4 and then 12 without a prompt. Which text is a command to type?
  ✔ a: quantity * 4, without >>>
      why: Correct: quantity * 4, without >>>
  ✘ b: >>> quantity * 4, including >>>
      why: Prompt characters mark interpreter input and must not be copied into the command.
  ✘ c: 12, because the line has no prompt.
      why: The unprompted line is displayed output in this tutorial, not a command.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:distinguish_interactive_prompts_commands_and_output(f1,f3)   anchors=['assessment:distinguish_interactive_prompts_commands_and_output']
  taught-before-tested: A.f1←s01; A.f3←s01

### s03 · hands_on · Judge running python interactively
Review the supplied examples — Read the supplied excerpts in this step and decide which are correct or defective for the stated task.
QUESTION [classify, stretch, grading=client] Read each fresh interactive-session record and decide whether it correctly enters commands without prompt characters, uses the retained quantity binding, and distinguishes displayed output from input. The assignment is quantity = 3 and the expression is quantity * (4 + 1).
  'Typed command: quantity = 3
Displayed result of assignment: none
Typed command: quantity * (4 + 1)
Displayed result: 15
Explanation: the expression uses quantity retained as 3.' -> Meets the criterion
      feedback: The assignment retains its binding; the later expression uses it and displays a result.
  'Typed command: >>> quantity = 3
Explanation: prompt markers must be included in typed commands.' -> Violates the criterion
      feedback: Prompt markers are not part of the command and must not be copied.
  'Typed command: quantity = 3
Typed command: quantity * (4 + 1)
Displayed result: 15
Explanation: the unprompted result line is another command to type.' -> Violates the criterion
      feedback: An unprompted tutorial result is output, not another command.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:evaluate_expressions_using_retained_session_state(f2); A:distinguish_interactive_prompts_commands_and_output(f1,f3)   anchors=['practice', 'assessment:evaluate_expressions_using_retained_session_state', 'assessment:distinguish_interactive_prompts_commands_and_output']
  taught-before-tested: A.f2←s01; A.f1←s01; A.f3←s01

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
QUESTION [choice, core, grading=client] Which statement correctly describes compilation and the triggers for top-level module execution?
  ✔ a: Valid source can compile to a code object; CPython uses implementation-specific bytecode. Top-level module statements execute on first import or when the file is executed as a script.
      why: Correct: Valid source can compile to a code object; CPython uses implementation-specific bytecode. Top-level module statements execute on first import or when the file is executed as a script.
  ✘ b: Every implementation must use CPython bytecode, and top-level statements execute only during compilation.
      why: CPython bytecode is implementation-specific; top-level statements execute at runtime on first import or script execution.
  ✘ c: Invalid syntax compiles successfully, and importing or executing the file never runs its top-level statements.
      why: Invalid syntax raises SyntaxError; first import and script execution trigger top-level execution.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r03
  MEASURES: B:identify_parsing_and_cpython_compilation(f1,f2); B:identify_top_level_execution_triggers(f3)   anchors=['assessment:identify_parsing_and_cpython_compilation', 'assessment:identify_top_level_execution_triggers']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s07 · check · Choose the right distinction
Check your understanding — Use what you learned about python interpreter execution model to choose the answer.
QUESTION [choice, core, grading=client] A script executes quantity = 3, then cost = quantity * 4. Which trace correctly explains the second binding?
  ✔ a: quantity is bound first; cost then uses its current value to compute and bind the result.
      why: Correct: quantity is bound first; cost then uses its current value to compute and bind the result.
  ✘ b: cost is bound before the right-hand expression is evaluated.
      why: Assignment evaluates its expression before binding the result.
  ✘ c: The compiler binds cost to a value without executing the assignments.
      why: Evaluation and binding of these assignments occur at runtime.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: B:predict_runtime_assignment_bindings(f4)   anchors=['assessment:predict_runtime_assignment_bindings']
  taught-before-tested: B.f4←s04

### s08 · hands_on · Practice python interpreter execution model
Try it — Trace the top-level execution of a supplied source file containing quantity = 3 followed by cost = quantity * 4, then execute it as a script in the interpreter.
QUESTION [code_exercise, stretch, grading=client] Keep the supplied quantity and cost statements unchanged. Before running, trace their execution order and explain which current binding the cost expression uses. Correct the two trace assignments: trace_quantity must record the resulting quantity binding and trace_cost must record the resulting cost binding, using variable references. The checker reads trace_quantity and trace_cost; no printed output is required.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['assignment with =', 'integer literals', 'variable references', 'multiplication with *'] blocked=8 items
  file main.py [editable]:
quantity = 3
cost = quantity * 4
trace_quantity = cost
trace_cost = quantity

  SOLUTION main.py:
quantity = 3
cost = quantity * 4
trace_quantity = quantity
trace_cost = cost

  test v1 (value_equals, visible=None): {"expr":"[trace_quantity, trace_cost]","expected":[3,12]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c4c8550bb6d2dabbcea5af4ad9f5c45f1a76319ae991dcbbd396163cb0f0fb62","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: B:predict_runtime_assignment_bindings(f4)   anchors=['practice']
  taught-before-tested: B.f4←s04

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
QUESTION [choice, core, grading=client] Which formatting preserves both print arguments and uses implicit continuation with a hanging indent?
  ✔ a: print(
    "Cost",
    cost
)
      why: Correct: print(
    "Cost",
    cost
)
  ✘ b: print
    ("Cost", cost)
      why: The open parenthesis must enclose the continued call; this splits before the delimiter opens.
  ✘ c: print(
    cost,
    "Cost"
)
      why: Although enclosed, this reverses the arguments rather than preserving the call.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r06
  MEASURES: C:reformat_expression_with_implicit_continuation_preserving_value(f1,f2,f3)   anchors=['assessment:reformat_expression_with_implicit_continuation_preserving_value']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f3←s09

### s11 · hands_on · Practice continuing expressions across lines
Try it — Rewrite print("Cost", cost) across several lines inside its parentheses, using a hanging indent and preserving the arguments.
QUESTION [code_exercise, stretch, grading=client] Keep the supplied cost input unchanged. Reformat only print("Cost", cost) across multiple physical lines inside its parentheses, with four-space hanging indentation and no backslashes. Keep "Cost" first and cost second. The checker verifies a multiline call with preserved arguments and the printed label and cost with default delimiters.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'integer and string literals', 'arithmetic multiplication and addition', 'print() with comma-separated arguments', 'parentheses for implicit continuation', 'hanging indentation', 'optional trailing comma in a function call'] blocked=10 items
  file main.py [editable]:
cost = 14
print("Cost", cost)

  SOLUTION main.py:
cost = 14
print(
    "Cost",
    cost
)

  test output (stdout_equals, visible=None): {"expected":"Cost 14\n"} | on-fail: Check the required printed values and delimiters.
  test v1 (value_equals, visible=None): {"expr":"[cost, all(n.end_lineno > n.lineno and len(n.args) == 2 and isinstance(n.args[0], __import__('ast').Constant) and n.args[0].value == 'Cost' and isinstance(n.args[1], __import__('ast').Name) and n.args[1].id == 'cost' for n in __import__('ast').walk(__import__('ast').parse(open('main.py').read())) if isinstance(n, __import__('ast').Call) and isinstance(n.func, __import__('ast').Name) and n.func.id == 'print')]","expected":[14,true]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"73a290323433f8d5b755496e4937c4930169d94e670aa6470ee8ed40d5b3cd95","tests_passed":2}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: C:reformat_expression_with_implicit_continuation_preserving_value(f1,f2,f3)   anchors=['practice', 'assessment:reformat_expression_with_implicit_continuation_preserving_value']
  taught-before-tested: C.f1←s09; C.f2←s09; C.f3←s09

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.041_041.r02 is never referenced
  warn: learn_python.tile.041_041.s04/ix.learn_python.tile.041_041.s04: ADVISORY — syntax descriptors with no detector: ['assert statements', 'chained string method calls', 'generator expressions', 'lambda expressions', 'list literals', 'string literals', 'yield expressions']

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
[VIDEO Removing surrounding whitespace] bridge-before: Watch how surrounding spaces affect the displayed result. The clip briefly says “all” spaces, but strip() removes only leading and trailing whitespace, not interior whitespace. | bridge-after: The clip demonstrates edge cleanup. The text also covers strip's removable-character argument, lowercase conversion, and the different empty-field behavior of delimiter splitting and whitespace splitting.
  - ERww7FiLrqk 30-122s facts=['f1'] label: Remove surrounding whitespace with text.strip() | summary: Calling text.strip() removes leading and trailing whitespace from entered text. The example accepts hello surrounded by spaces and displays hello after applying strip(). Without that call, the surrounding spaces remain. This cleanup is useful before comparing an entered label with an expected value.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about transforming text with string methods to choose the answer.
QUESTION [choice, intro, grading=client] Which code removes surrounding whitespace and converts text to lowercase, retaining the returned normalized string?
  ✔ a: normalized = text.strip().lower()
      why: Correct: normalized = text.strip().lower()
  ✘ b: text.strip()
text.lower()
      why: The returned strings are discarded; these calls do not modify the original string.
  ✘ c: normalized = text.lower()
      why: Lowercasing alone leaves the surrounding whitespace in place.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:select_methods_for_label_normalization(f1,f2,f3)   anchors=['assessment:select_methods_for_label_normalization']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · hands_on · Practice transforming text with string methods
Try it — Normalize an entered label by removing surrounding whitespace and converting it to lowercase, then split comma-delimited and whitespace-separated text into fields.
QUESTION [code_exercise, stretch, grading=client] Choose label_input, comma_input, and whitespace_input from the supplied strings so normalized contains the cleaned lowercase label, comma_parts preserves the repeated-comma empty field, and words contains the whitespace-separated fields. Keep the transformation calls and supplied strings unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'list literals', 'input()', 'print()', 'text.strip()', 'text.strip(chars)', 'text.lower()', 'text.split(separator)', 'text.split()', 'chained string method calls'] blocked=10 items
  file main.py [editable]:
text = "  Blue  "
comma_text = "red,,blue"
whitespace_text = "  red   blue  "
blank = ""
label_input = blank
comma_input = blank
whitespace_input = blank
normalized = label_input.strip().lower()
comma_parts = comma_input.split(",")
words = whitespace_input.split()

  SOLUTION main.py:
text = "  Blue  "
comma_text = "red,,blue"
whitespace_text = "  red   blue  "
blank = ""
label_input = text
comma_input = comma_text
whitespace_input = whitespace_text
normalized = label_input.strip().lower()
comma_parts = comma_input.split(",")
words = whitespace_input.split()

  test v1 (value_equals, visible=None): {"expr":"[normalized, comma_parts, words]","expected":["blue",["red","","blue"],["red","blue"]]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"271742b6b17d64120ece39fd6f60e2cd46ce7a293baccc39a974cdd68f97600c","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:select_splitting_method_for_delimiters_and_whitespace(f4,f5)   anchors=['practice', 'assessment:select_splitting_method_for_delimiters_and_whitespace']
  taught-before-tested: A.f4←s01; A.f5←s01

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.042_042.r02 is never referenced
  warn: learn_python.tile.042_042.s03/ix.learn_python.tile.042_042.s03: ADVISORY — syntax descriptors with no detector: ['Assignment with =', 'Comparison with >', 'Integer and string literals', 'Specific exception-handler clauses', 'assert statements', 'finally clauses', 'if statements with a colon and an indented body', 'lambda expressions', 'raise statements', 'yield expressions']

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
QUESTION [choice, intro, grading=client] An if header is missing its colon and its body contains int("three"). What must happen before tracing execution of that source?
  ✔ a: Repair the missing colon so the source can compile.
      why: Correct: Repair the missing colon so the source can compile.
  ✘ b: Trace the conversion first; invalid syntax does not prevent execution.
      why: Invalid syntax prevents compilation to an executable code object.
  ✘ c: Treat the missing colon as a runtime ValueError.
      why: The missing colon is a parsing failure; ValueError from conversion belongs to execution.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:identify_syntax_repair_as_prerequisite_to_execution(f3)   anchors=['assessment:identify_syntax_repair_as_prerequisite_to_execution']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Practice distinguishing syntax and runtime errors
Try it — Repair a missing colon in an if statement before investigating the runtime exception caused by int("three") in its body.
QUESTION [code_exercise, stretch, grading=client] Choose ending so the generated if header parses. Run the repaired source, inspect failure, and choose stage from execution_label and parsing_label to identify when the reported failure occurs. Keep the wrapper, inputs, and conversion body unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['Assignment with =', 'Integer and string literals', 'Comparison with >', 'if statements with a colon and an indented body', 'Calls to int()'] blocked=7 items
  file main.py [editable]:
quantity = 1
raw = "three"
newline = "\n"
colon_newline = ":\n"
execution_label = "execution"
parsing_label = "parsing"
ending = newline
stage = parsing_label
source = "if quantity > 0" + ending + "    quantity = int(raw)"
failure = ""
try:
    exec(source)
except Exception as exc:
    failure = type(exc).__name__ + ": " + str(exc)

  SOLUTION main.py:
quantity = 1
raw = "three"
newline = "\n"
colon_newline = ":\n"
execution_label = "execution"
parsing_label = "parsing"
ending = colon_newline
stage = execution_label
source = "if quantity > 0" + ending + "    quantity = int(raw)"
failure = ""
try:
    exec(source)
except Exception as exc:
    failure = type(exc).__name__ + ": " + str(exc)

  test v1 (value_equals, visible=None): {"expr":"[failure, stage]","expected":["ValueError: invalid literal for int() with base 10: 'three'","execution"]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a2cbe036cf100684b43af6da977601737846e7b175804c3bbedf4a5db4f266e1","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:classify_failure_by_parsing_or_execution(f1,f2); A:identify_syntax_repair_as_prerequisite_to_execution(f3)   anchors=['practice', 'assessment:classify_failure_by_parsing_or_execution', 'assessment:identify_syntax_repair_as_prerequisite_to_execution']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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

## OTHER CONTENT (fields without a dedicated renderer)
· expected.value: ValueError: invalid literal for int() with base 10: 'three_x'
· expected.value: IndentationError: expected an indented block after 'if' statement on line 1 (<string>, line 2)

=========

# EVALUATOR PACKET — Truth-value testing · Checking for None with identity (learn_python.tile.043_044)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.truth_value_testing — Truth-value testing
B = python.none_and_identity — Checking for None with identity

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step learn_python.tile.043_044.r02 is never referenced
  warn: remediation step learn_python.tile.043_044.r04 is never referenced
  warn: learn_python.tile.043_044.s04/ix.learn_python.tile.043_044.s04: ADVISORY — syntax descriptors with no detector: ['assert', 'class', 'empty and nonempty list literals', 'finally', 'if statements with indented bodies', 'integer literals', 'is', 'is not', 'raise', 'string literals', 'with', 'yield']
  warn: learn_python.tile.043_044.s08/ix.learn_python.tile.043_044.s08: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'None', 'assert', 'async', 'await', 'class', 'finally', 'integer literals', 'is', 'is not', 'raise', 'string literals', 'with', 'yield']

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
QUESTION [choice, intro, grading=client] Which pair has false truth value followed by true truth value?
  ✔ a: An empty list, then a list containing 3.
      why: Correct: An empty list, then a list containing 3.
  ✘ b: A list containing 0, then an empty list.
      why: Nonempty built-in lists are true even when the element is zero; an empty list is false.
  ✘ c: An empty dictionary, then an empty tuple.
      why: Both are empty collections and therefore false.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:predict_truth_values_of_empty_and_nonempty_collections(f1)   anchors=['assessment:predict_truth_values_of_empty_and_nonempty_collections']
  taught-before-tested: A.f1←s01

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about truth-value testing to choose the answer.
QUESTION [choice, core, grading=client] Which scalar pair has false truth value followed by true truth value?
  ✔ a: 0, then 3.
      why: Correct: 0, then 3.
  ✘ b: 3, then 0.
      why: Nonzero numbers are true; zero is false, so this reverses the required order.
  ✘ c: None, then False.
      why: Both None and False have false truth values.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:predict_truth_values_of_scalar_values(f1)   anchors=['assessment:predict_truth_values_of_scalar_values']
  taught-before-tested: A.f1←s01

### s04 · hands_on · Practice truth-value testing
Try it — Write an empty-collection guard using if not quantities: without comparing quantities to True.
QUESTION [code_exercise, stretch, grading=client] Immediately after quantities = empty, write an if not quantities: guard that prints message. Keep the supplied inputs and second run unchanged. The initial empty list must produce one message; the nonempty second run must produce none. Do not compare quantities with True.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'empty and nonempty list literals', 'integer literals', 'string literals', 'if statements with indented bodies', 'not', 'print()'] blocked=9 items
  file main.py [editable]:
input_count = 0
message = "No quantities"
sample = [3]
empty = list(range(input_count))
quantities = empty
quantities = sample
if not quantities:
    print(message)

  SOLUTION main.py:
input_count = 0
message = "No quantities"
sample = [3]
empty = list(range(input_count))
quantities = empty
if not quantities:
    print(message)
quantities = sample
if not quantities:
    print(message)

  test output (stdout_equals, visible=None): {"expected":"No quantities\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"8f5cb6f13b609b3de9680ab50d37a3cb1773a64152c97bdeb56c9b1aed9167e8","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:predict_truth_values_of_empty_and_nonempty_collections(f1)   anchors=['practice']
  taught-before-tested: A.f1←s01

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
QUESTION [choice, core, grading=client] quantity may be None (absent) or a legitimate zero. Which condition tests only absence?
  ✔ a: quantity is None
      why: Correct: quantity is None
  ✘ b: not quantity
      why: A truth test also treats zero as false, so it does not isolate absence.
  ✘ c: quantity is not None
      why: This tests that quantity is supplied, the opposite of the requested absence test.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r03
  MEASURES: B:test_absence_with_identity(f1,f2,f3)   anchors=['assessment:test_absence_with_identity']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05

### s07 · check · Choose the right distinction
Check your understanding — Use what you learned about checking for none with identity to choose the answer.
QUESTION [choice, core, grading=client] Why use quantity is not None rather than if quantity: to recognize a supplied quantity that may be zero?
  ✔ a: The identity test accepts zero as supplied and rejects only None.
      why: Correct: The identity test accepts zero as supplied and rejects only None.
  ✘ b: Because zero and None are the same object.
      why: None represents absence; a legitimate numeric zero is not None.
  ✘ c: Because truth testing considers zero true.
      why: Zero has false truth value, which is why the truth test would reject it.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: B:distinguish_absence_from_zero_and_empty_values(f3)   anchors=['assessment:distinguish_absence_from_zero_and_empty_values']
  taught-before-tested: B.f3←s05

### s08 · hands_on · Practice checking for none with identity
Try it — Handle an optional quantity lookup result using an explicit None check, preserving zero as a legitimate supplied quantity.
QUESTION [code_exercise, stretch, grading=client] After quantity = supplied, write an explicit None check: print Quantity absent when quantity is None; otherwise print Quantity supplied and quantity with default delimiters. Keep the supplied inputs and second run unchanged. Zero must count as supplied.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'None', 'integer literals', 'string literals', 'is', 'is not', 'if', 'else', 'print()'] blocked=11 items
  file main.py [editable]:
supplied = 0
absent = None
quantity = supplied
quantity = absent
if quantity is None:
    print("Quantity absent")
else:
    print("Quantity supplied", quantity)

  SOLUTION main.py:
supplied = 0
absent = None
quantity = supplied
if quantity is None:
    print("Quantity absent")
else:
    print("Quantity supplied", quantity)
quantity = absent
if quantity is None:
    print("Quantity absent")
else:
    print("Quantity supplied", quantity)

  test output (stdout_equals, visible=None): {"expected":"Quantity supplied 0\nQuantity absent\n"} | on-fail: Check the required printed values and delimiters.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6956760040789d2f57a02387b84647b1dc6a67d78fdf567c1560fd9782f10e3e","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: B:test_absence_with_identity(f1,f2,f3)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05

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

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expected: Quantity supplied 0
Quantity absent

· expected.value: Quantity supplied 7
Quantity absent

=========

# EVALUATOR PACKET — Encoding and decoding Unicode text and bytes (learn_python.tile.045_045)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.unicode_and_bytes — Encoding and decoding Unicode text and bytes

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.045_045.r02 is never referenced
  warn: remediation step learn_python.tile.045_045.r03 is never referenced
  warn: learn_python.tile.045_045.s05/ix.learn_python.tile.045_045.s05: ADVISORY — syntax descriptors with no detector: ['assert statements', 'equality comparison with ==', 'except UnicodeDecodeError:', 'finally clauses', 'lambda expressions', 'raise statements', 'string literals containing non-ASCII characters', 'with statements', 'yield expressions']

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
[VIDEO Encoding text as UTF-8 bytes] bridge-before: Watch how encode() changes a string into bytes. The clip relies on the default UTF-8 encoding; Devspace writes encode("utf-8") explicitly to make the encoding choice clear. | bridge-after: The clip demonstrates encoding only. The text also explains Unicode str versus binary bytes, decoding with a matching encoding, and UnicodeDecodeError when bytes are invalid for the chosen decoding.
  - YPn7bXOF7-U 4-45s facts=['f2'] label: Encode a Python string as UTF-8 bytes | summary: The encode method converts a string into bytes using an encoding. Calling encode() without an argument uses UTF-8 by default. The example encodes "hello python" and identifies the resulting bytes value by the b prefix in its displayed representation.

### s03 · check · Choose the right distinction
Check your understanding — Use what you learned about encoding and decoding unicode text and bytes to choose the answer.
QUESTION [choice, intro, grading=client] Which pair of operations recovers Unicode text after converting it to UTF-8 bytes?
  ✔ a: payload = text.encode("utf-8")
restored = payload.decode("utf-8")
      why: Correct: payload = text.encode("utf-8")
restored = payload.decode("utf-8")
  ✘ b: payload = text.decode("utf-8")
restored = payload.encode("utf-8")
      why: Encoding converts text to bytes; decoding converts bytes back to text. These directions are reversed.
  ✘ c: payload = text.encode("utf-8")
restored = payload
      why: payload is bytes, not the decoded Unicode text required for restored.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']  remediation→r01
  MEASURES: A:round_trip_unicode_text_with_utf8(f1,f2,f3)   anchors=['assessment:round_trip_unicode_text_with_utf8']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · check · Choose the right distinction
Check your understanding — Use what you learned about encoding and decoding unicode text and bytes to choose the answer.
QUESTION [choice, core, grading=client] A bytes payload is not valid for the chosen decoding encoding. What failure does decoding report?
  ✔ a: UnicodeDecodeError
      why: Correct: UnicodeDecodeError
  ✘ b: It always recovers the original text regardless of encoding.
      why: The decoding encoding must match the data, and invalid bytes can cause a decoding failure.
  ✘ c: It silently treats bytes as already-decoded Unicode text.
      why: bytes and str are distinct; decoding can fail instead of returning text.
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:recognize_invalid_byte_decoding_failures(f3,f4)   anchors=['assessment:recognize_invalid_byte_decoding_failures']
  taught-before-tested: A.f3←s01; A.f4←s01

### s05 · hands_on · Practice encoding and decoding unicode text and bytes
Try it — Encode the non-ASCII string "café" as UTF-8 bytes, then decode those bytes using UTF-8 to recover the original text.
QUESTION [code_exercise, stretch, grading=client] The UTF-8 encoding, decoding, and equality check are supplied. Keep text and those operations unchanged. Replace payload = b"" with an assignment that binds payload to the supplied encoded bytes in encoded. Trace the round trip before running: payload must contain the UTF-8 bytes for text, restored must recover text, and matches must be true. The checker reads payload, restored, and matches; no printed output is required.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals containing non-ASCII characters', 'text.encode("utf-8")', 'payload.decode("utf-8")', 'equality comparison with =='] blocked=9 items
  file main.py [editable]:
text = "caf\u00e9"
encoded = text.encode("utf-8")
payload = b""
restored = payload.decode("utf-8")
matches = restored == text

  SOLUTION main.py:
text = "caf\u00e9"
encoded = text.encode("utf-8")
payload = encoded
restored = payload.decode("utf-8")
matches = restored == text

  test v1 (value_equals, visible=None): {"expr":"[list(payload), restored, matches]","expected":[[99,97,102,195,169],"café",true]} | on-fail: Check the named result and the requested behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"626effa35e1a9cf073c66832d9e01d4e1ab91879ce60031556d447198a06e671","tests_passed":1}
  feedback✔: That meets the stated criterion.  feedback✘: Recheck the stated requirement and the relevant rule before trying again.  hints: ['Trace the supplied values and distinguish the requested behavior from its alternatives.']
  MEASURES: A:round_trip_unicode_text_with_utf8(f1,f2,f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

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