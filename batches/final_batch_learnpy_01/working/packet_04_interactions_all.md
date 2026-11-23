# EVALUATOR PACKET — Variables Assignment / Core Data Types / Arithmetic Operators (learn_python.tile.000_002)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.variables_assignment — Variables Assignment
B = python.core_data_types — Core Data Types
C = python.arithmetic_operators — Arithmetic Operators

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=11
  warn: remediation step learn_python.tile.000_002.r02 is never referenced
  warn: remediation step learn_python.tile.000_002.r04 is never referenced
  warn: remediation step learn_python.tile.000_002.r05 is never referenced
  warn: remediation step learn_python.tile.000_002.r07 is never referenced
  warn: learn_python.tile.000_002.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.000_002.s04/ix.learn_python.tile.000_002.s04: ADVISORY — syntax descriptors with no detector: ['ASCII variable names beginning with a letter or underscore, followed by letters, underscores or digits, excluding keywords', 'Assignment expressions', 'Attribute access and method calls', 'Augmented assignment', 'Chained assignment and unpacking assignment', 'Comments', 'Comparison operators', 'Comprehensions', 'Indexing and slicing', 'List, tuple, set and dictionary displays', 'Logical operators', 'Numeric expressions using +, -, * or /', 'Numeric literals', 'Previously assigned names in right-hand expressions', 'Quoted string literals', 'Single-target assignment with =', 'Type annotations', 'assert', 'break and continue', 'class', 'def and return', 'del', 'for and while', 'global and nonlocal', 'if, elif and else', 'import and from', 'try, except, finally and raise', 'with', 'yield']
  warn: learn_python.tile.000_002.s05: prose block without lineage.fact_ids
  warn: learn_python.tile.000_002.s10/ix.learn_python.tile.000_002.s10: ADVISORY — syntax descriptors with no detector: ['True and False', 'class', 'decimal and exponent float literals', 'dictionary literals', 'for', 'import', 'integer literals', 'list literals', 'set literals', 'single-quoted and double-quoted string literals', 'try/except', 'tuple literals', 'variable assignment with =', 'variable reassignment with =', 'while']
  warn: learn_python.tile.000_002.s11: prose block without lineage.fact_ids
  warn: learn_python.tile.000_002.s13/ix.learn_python.tile.000_002.s13: ADVISORY — syntax descriptors with no detector: ['!=', '%', '*', '**', '+', '-', '/', '//', '<', '<=', '==', '>', '>=', 'assert', 'assignment with =', 'comprehensions', 'dictionary literals', 'for', 'import', 'integer literals', 'list literals', 'set literals', 'tuple literals', 'variable references', 'while']
  warn: plan: learn_python.tile.000_002.s04 was planned to measure python.variables_assignment#assessment:choose_meaningful_valid_variable_names but its interaction does not

## SOURCE FACTS — A (python.variables_assignment)   objective: Create and reassign variables to store values using the assignment operator.
A.f1: Assignment binds or rebinds a name to the value of the expression on the right of =.   [sources: python_language_reference#simple_stmts.html#assignment-statements]
A.f2: Use name = value to assign a value, and use the name in a later right-hand expression to reuse its current value.   [sources: python_language_reference#simple_stmts.html#assignment-statements]
A.f3: Names are case-sensitive; ASCII names can contain letters, underscores and digits, but cannot start with a digit or be a keyword.   [sources: python_language_reference#lexical_analysis.html#identifiers]
A.f4: A right-hand expression can combine named numeric values using +, -, * or / before assigning the result.   [sources: python_tutorial#introduction.html#numbers]
note: Begin with this objective: Create and reassign variables to store values using the assignment operator.
note: Keep the example in the Names, types and calculations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.core_data_types, python.arithmetic_operators, python.comparison_operators.
PRACTICE ANCHOR (live_code): Assign quantity, unit_price and cost for a notebook purchase, then reassign cost using a computation involving quantity and unit_price.  SUCCESS: Three meaningful names receive values, and cost is subsequently reassigned to the result of quantity * unit_price using their current values.
ASSESSMENT ANCHOR: choose_meaningful_valid_variable_names facts=['f3']
ASSESSMENT ANCHOR: assign_and_reassign_named_values facts=['f1', 'f2']
ASSESSMENT ANCHOR: assign_results_using_current_named_values facts=['f2', 'f4']

## SOURCE FACTS — B (python.core_data_types)   objective: Recognize and use Python's core scalar data types: int, float, str, and bool.
B.f1: An int represents an integer; a numeric literal with a decimal point or exponent produces a float.   [sources: python_stdlib_reference#stdtypes.html#typesnumeric]
B.f2: Mixed int and float arithmetic converts the int operand to float.   [sources: python_stdlib_reference#stdtypes.html#typesnumeric]
B.f3: A str represents text and can be created with single- or double-quoted literals; + concatenates strings.   [sources: python_tutorial#introduction.html#text]
B.f4: A bool has the values True and False and represents truth values.   [sources: python_stdlib_reference#stdtypes.html#boolean-type-bool]
B.f5: Numeric values can be compared for equality or ordering, producing a boolean.   [sources: python_stdlib_reference#stdtypes.html#comparisons]
B.f6: type(value) returns the value’s type.   [sources: python_stdlib_reference#functions.html#type]
B.f7: print(value) displays a string representation of the value.   [sources: python_stdlib_reference#functions.html#print]
note: Begin with this objective: Recognize and use Python's core scalar data types: int, float, str, and bool.
note: Keep the example in the Names, types and calculations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.arithmetic_operators, python.comparison_operators, python.logical_operators.
PRACTICE ANCHOR (live_code): Create int, float, str, and bool values in the notebook example and display each value’s type using print(type(...)). Use quantity, price, and label, then reuse quantity for a bool after inspecting its integer value.  SUCCESS: The code displays int, float, str, and bool type results in that order, using correctly formed literals and inspecting quantity before and after its reassignment.
ASSESSMENT ANCHOR: identify_core_value_types facts=['f1', 'f3', 'f4', 'f6']
ASSESSMENT ANCHOR: predict_mixed_numeric_result_type facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_string_concatenation_from_numeric_addition facts=['f3']
ASSESSMENT ANCHOR: predict_numeric_comparison_results facts=['f4', 'f5']
ASSESSMENT ANCHOR: predict_displayed_values_and_types facts=['f6', 'f7']

## SOURCE FACTS — C (python.arithmetic_operators)   objective: Use Python arithmetic operators for numeric calculations.
C.f1: For numeric values, x + y adds, x - y subtracts, x * y multiplies and x / y divides; division of ints produces a float.   [sources: python_stdlib_reference#stdtypes.html#typesnumeric]
C.f2: x // y gives the floored quotient, x % y gives the remainder and x ** y raises x to power y.   [sources: python_stdlib_reference#stdtypes.html#typesnumeric]
C.f3: Parentheses group a calculation; exponentiation has higher precedence than multiplication, division and remainder, which have higher precedence than addition and subtraction.   [sources: python_language_reference#expressions.html#operator-precedence]
note: Begin with this objective: Use Python arithmetic operators for numeric calculations.
note: Keep the example in the Names, types and calculations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.comparison_operators, python.logical_operators, python.type_conversion.
PRACTICE ANCHOR (live_code): Compute derived values from numeric inputs using division, floor division, remainder and exponentiation, then compare calculations with and without parentheses.  SUCCESS: The calculations produce 3.4 for 17 / 5, 3 for 17 // 5, 2 for 17 % 5, 8 for 2 ** 3, 20 for (2 + 3) * 4 and 14 for 2 + 3 * 4.
ASSESSMENT ANCHOR: apply_basic_arithmetic_operators facts=['f1']
ASSESSMENT ANCHOR: apply_floor_division_remainder_and_exponentiation facts=['f2']
ASSESSMENT ANCHOR: apply_parentheses_and_operator_precedence facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Arithmetic Operators; Choosing a built-in collection; Comparison Operators; Comprehensions; Conditional Statements; Core Data Types; Defining Calling Functions; Dictionaries; Error Handling; File Io; For Loops; Function Default Keyword Args; Import Statements; Iterating Collections; Lists; Logical Operators; Loop Control; PEP 8 Style; Parameters Arguments; Reading and displaying console values; Return Values; Sets; String Basics Formatting; Tuples; Type Conversion; Variable Scope; While Loops

## LESSON, in learner order

### s01 · explainer · Variables Assignment
(intro) Name the notebook quantity, unit price and cost. ⟦A:tb1⟧
(definition) Assignment binds a name to the right-hand expression’s value; another assignment can rebind it. ⟦A.f1 A:tb2⟧
(mechanism) Write name = value. A later right-hand expression uses a name’s current value. ⟦A.f2 A:tb3⟧
(mechanism) Names are case-sensitive. ASCII names may contain letters, underscores and digits, but cannot begin with a digit or be a keyword. ⟦A.f3 A:tb3⟧
(mechanism) Combine named numbers with +, -, * or / on the right, then assign the result. ⟦A.f4 A:tb3⟧
[CODE python]
quantity = 3
unit_price = 4
cost = quantity * unit_price
quantity = 5
cost = quantity * unit_price
  annotations: ['This assignment binds cost to 12.', 'quantity becomes 5; cost remains 12.', 'Recalculating with the current values binds cost to 20.']

### s02 · explainer · Variables Assignment
(example) Read each notebook assignment from right to left: evaluate the expression, then bind its target. Changing quantity and recalculating cost are separate assignments. Use unit_price as a meaningful name; changing quantity to Quantity refers to a different name. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Changing quantity does not keep the earlier cost expression running. Assign cost again to use the new quantity. ⟦A.f1 A.f2 A:tb5⟧

### s03 · check · Check variables assignment
Quick check — Decide which assignment uses the current values of the named variables.
QUESTION [choice, intro, grading=client] Which action uses a valid, meaningful unit-price name and recalculates cost from the current quantity and unit price?
  ✔ a: Use unit_price and reassign cost = quantity * unit_price
      why: unit_price is a valid, meaningful name; reassignment calculates cost using the current named values.
  ✘ b: Use 2unit_price and reassign cost = quantity * 2unit_price
      why: 2unit_price starts a name with a digit, so it is not a valid variable name.
  ✘ c: Use unit_price and let cost update automatically.
      why: cost does not recalculate automatically when an input changes; reassign it to calculate with the current values.
  feedback✔: unit_price is a valid, meaningful name; reassignment calculates cost using the current named values.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:assign_results_using_current_named_values(f2,f4); A:choose_meaningful_valid_variable_names(f3)   anchors=['assessment:assign_results_using_current_named_values', 'assessment:choose_meaningful_valid_variable_names']
  taught-before-tested: A.f2←s01; A.f4←s01; A.f3←s01

### s04 · hands_on · Practice variables assignment
Practice — Assign quantity, unit_price and cost for a notebook purchase, then reassign cost using a computation involving quantity and unit_price.
QUESTION [code_exercise, intro, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_cost to cost. The checker reads cost.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['ASCII variable names beginning with a letter or underscore, followed by letters, underscores or digits, excluding keywords', 'Numeric literals', 'Single-target assignment with =', 'Previously assigned names in right-hand expressions', 'Numeric expressions using +, -, * or /'] blocked=26 items
  file main.py [editable]:
quantity = 3
unit_price = 4
cost = 0
computed_cost = quantity * unit_price

  SOLUTION main.py:
quantity = 3
unit_price = 4
cost = 0
computed_cost = quantity * unit_price
cost = computed_cost

  test t0 (value_equals, visible=True): {"expr":"[quantity, unit_price, cost]","expected":[3,4,12]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"317fbcd4a152806807057af061ffae60afa0f2075fd7bea7c25a5f775b6e9e0a","tests_passed":1}
  feedback✔: The result meets the task. Three meaningful names receive values, and cost is subsequently reassigned to the result of quantity * unit_price using their current values.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['The product is already stored in computed_cost. Rebind cost to that current value.']
  MEASURES: A:assign_and_reassign_named_values(f1,f2); A:assign_results_using_current_named_values(f2,f4)   anchors=['practice', 'assessment:assign_and_reassign_named_values', 'assessment:assign_results_using_current_named_values']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f4←s01

### s05 · explainer · Core Data Types
(intro) Inspect notebook quantity, price, label and truth value. ⟦B:tb1⟧
(definition) An int represents an integer. A numeric literal with a decimal point or exponent produces a float. ⟦B.f1 B:tb2⟧
(mechanism) In mixed int/float arithmetic, the int operand is converted to float. ⟦B.f2 B:tb3⟧
(mechanism) Text has type str. Single or double quotes create string literals; + joins strings. ⟦B.f3 B:tb3⟧
(mechanism) A bool represents truth with True or False. ⟦B.f4 B:tb3⟧
(mechanism) Equality or ordering comparisons between numbers produce a boolean. ⟦B.f5 B:tb3⟧
(mechanism) type(value) returns the type of that value. ⟦B.f6 B:tb3⟧
(mechanism) print(value) displays the value’s string representation. ⟦B.f7 B:tb3⟧
[CODE python]
quantity = 3
price = 4.5
label = "Notebook"
print(type(quantity))
print(type(price))
print(label + " order")
print(quantity * price)
print(quantity == 3)
quantity = True
print(type(quantity))
  annotations: ['Inspect quantity’s current type, before and after reassignment.', 'Inspect quantity’s current type, before and after reassignment.', 'The operands are strings, so + joins their text.', 'This calculation mixes an integer and a float.']

### s06 · explainer · Core Data Types
(example) Inspect quantity and price with type, then compare numeric multiplication with joining label text. Finally, reassign quantity to a bool and inspect its type again: inspect the current value, not the name’s spelling. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B:tb4⟧
(misconception) A quoted number is text. Joining strings with + is not numeric addition; type(value) distinguishes the kinds of value. ⟦B.f1 B.f3 B.f6 B:tb5⟧

### s07 · video · Explore core data types
[VIDEO Recognize core types and inspect values] bridge-before: Watch the first clip connect changed values to type() results, then the second distinguish four core types. Use Python’s names str for text and bool for Boolean truth values. | bridge-after: The first clip establishes type(); the second establishes True and False. Neither fully covers exponent literals, mixed numeric arithmetic, string concatenation, numeric comparisons, or print’s string-representation behavior. The text teaches all these details independently.
  - khKv-8q7YmY 0-49s facts=['f6'] label: Inspect integer and float values with type() | summary: An integer is a whole number, while a decimal literal such as 3.14 produces a float. Assigning 3 to num and displaying type(num) identifies its type as int. Reassigning num to 3.14 and displaying its type again identifies float. type(value) reports the type of the value currently assigned, rather than a permanent type attached to the variable name.
  - OFrLs22MDAw 170-325s facts=['f4'] label: Recognize int, float, str, and bool values | summary: Python’s int type represents whole numbers, including negative integers and zero. The str type represents text enclosed in single or double quotation marks; quoted digits are text too. Either quotation style can surround text containing the other kind of quotation mark. The bool values are True and False, with capital initials. These reserved words cannot be variable names. Decimal literals such as 1.23 produce float values.

### s08 · check · Check core data types
Quick check — Decide whether the supplied expressions perform numeric addition or string concatenation, and identify the numeric result type.
QUESTION [choice, core, grading=client] Which statement correctly distinguishes 3 + 4.5 from "3" + "4.5"?
  ✔ a: The first is numeric addition with a float result; the second concatenates text.
      why: Correct. The first is numeric addition with a float result; the second concatenates text.
  ✘ b: Both concatenate text.
      why: Unquoted numeric values use numeric arithmetic, not string concatenation.
  ✘ c: Both add numbers and produce a float.
      why: Quoted values are strings, and + concatenates those strings.
  feedback✔: Correct. The first is numeric addition with a float result; the second concatenates text.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r03
  MEASURES: B:predict_mixed_numeric_result_type(f1,f2); B:distinguish_string_concatenation_from_numeric_addition(f3)   anchors=['assessment:predict_mixed_numeric_result_type', 'assessment:distinguish_string_concatenation_from_numeric_addition']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05

### s09 · check · Check core data types
Quick check — Decide which Boolean results follow from the supplied numeric comparisons.
QUESTION [choice, core, grading=client] What kind of value does the numeric comparison quantity >= 3 produce?
  ✔ a: A bool, either True or False.
      why: Correct. A bool, either True or False.
  ✘ b: A string containing the expression.
      why: A numeric comparison produces a boolean, not text.
  ✘ c: The integer quantity itself.
      why: Comparison tests the values; it does not return the quantity as its result.
  feedback✔: Correct. A bool, either True or False.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: B:predict_numeric_comparison_results(f4,f5)   anchors=['assessment:predict_numeric_comparison_results']
  taught-before-tested: B.f4←s05; B.f5←s05

### s10 · hands_on · Practice core data types
Practice — Create int, float, str, and bool values in the notebook example and display each value’s type using print(type(...)). Use quantity, price, and label, then reuse quantity for a bool after inspecting its integer value.
QUESTION [code_exercise, core, grading=client] Keep the int quantity, float price and str label inputs. Display each type with print(type(...)) in that order. After each type line, print its value on a separate line. Then reassign quantity from truth and print its bool type followed by its value. Print exactly these eight lines; no other output.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'variable reassignment with =', 'integer literals', 'decimal and exponent float literals', 'single-quoted and double-quoted string literals', 'True and False', 'type(value)', 'print(value)', 'print(type(variable))'] blocked=22 items
  file main.py [editable]:
quantity = 3
price = 4.5
label = "notebook"
truth = True

  SOLUTION main.py:
quantity = 3
price = 4.5
label = "notebook"
truth = True
print(type(quantity))
print(quantity)
print(type(price))
print(price)
print(type(label))
print(label)
quantity = truth
print(type(quantity))
print(quantity)

  test t0 (stdout_equals, visible=True): {"expected":"<class 'int'>\n3\n<class 'float'>\n4.5\n<class 'str'>\nnotebook\n<class 'bool'>\nTrue"} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"efaf86a597f1555eee83061277653ffab7ae0a6bd411f3b9459ddb3118f79073","tests_passed":1}
  feedback✔: The result meets the task. The code displays int, float, str, and bool type results in that order, using correctly formed literals and inspecting quantity before and after its reassignment.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Keep the supplied inputs and use their names in your computation.', 'Check indentation and the exact result names requested in the prompt.']
  MEASURES: B:identify_core_value_types(f1,f3,f4,f6); B:predict_displayed_values_and_types(f6,f7)   anchors=['practice', 'assessment:identify_core_value_types', 'assessment:predict_displayed_values_and_types']
  taught-before-tested: B.f1←s05; B.f3←s05; B.f4←s05; B.f6←s05; B.f6←s05; B.f7←s05

### s11 · explainer · Arithmetic Operators
(intro) Choose the operation that answers the token-grouping question. ⟦C:tb1⟧
(definition) For numbers, + adds, - subtracts, * multiplies and / divides. Dividing ints produces a float. ⟦C.f1 C:tb2⟧
(mechanism) // gives the floored quotient, % the remainder, and ** a power. ⟦C.f2 C:tb3⟧
(mechanism) Parentheses group calculations. Exponentiation has higher precedence than multiplication, division and remainder; those have higher precedence than addition and subtraction. ⟦C.f3 C:tb3⟧
(example) Compare ordinary division, the floored quotient and the remainder on the same token inputs. Then compare the grouped and ungrouped addition-and-multiplication expressions. Trace grouping before calculating. ⟦C.f1 C.f2 C.f3 C:tb4⟧
(misconception) // is a floored quotient, not ordinary division displayed differently. Parentheses change grouping, not just appearance. ⟦C.f2 C.f3 C:tb5⟧
[CODE python]
print(17 / 5)
print(17 // 5)
print(17 % 5)
print(2 ** 3)
print((2 + 3) * 4)
print(2 + 3 * 4)
  annotations: ['Compare division, floored quotient and remainder on identical inputs.', 'Compare division, floored quotient and remainder on identical inputs.', 'Compare division, floored quotient and remainder on identical inputs.', 'The parentheses group addition before multiplication.', 'Without parentheses, multiplication has higher precedence.']

### s12 · check · Check arithmetic operators
Quick check — Decide which arithmetic operator matches the supplied calculation.
QUESTION [choice, core, grading=client] Which expression assigns the cost of quantity items at unit_price each?
  ✔ a: cost = quantity * unit_price
      why: Correct. cost = quantity * unit_price
  ✘ b: cost = quantity + unit_price
      why: Addition combines the two amounts once; multiplication applies the unit price to the quantity.
  ✘ c: cost = quantity / unit_price
      why: Division is not multiplication of quantity by the per-item price.
  feedback✔: Correct. cost = quantity * unit_price  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r06
  MEASURES: C:apply_basic_arithmetic_operators(f1)   anchors=['assessment:apply_basic_arithmetic_operators']
  taught-before-tested: C.f1←s11

### s13 · hands_on · Practice arithmetic operators
Practice — Compute derived values from numeric inputs using division, floor division, remainder and exponentiation, then compare calculations with and without parentheses.
QUESTION [code_exercise, intro, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_division to division. Assign computed_quotient to quotient. Assign computed_remainder to remainder. Assign computed_power to power. Assign computed_grouped to grouped. Assign computed_ungrouped to ungrouped. The checker reads division, quotient, remainder, power, grouped, ungrouped.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['integer literals', 'float literals', 'variable references', 'assignment with =', '+', '-', '*', '/', '//', '%', '**', 'parentheses for grouping'] blocked=28 items
  file main.py [editable]:
tokens = 17
group_size = 5
a = 2
b = 3
c = 4
computed_division = tokens / group_size
computed_quotient = tokens // group_size
computed_remainder = tokens % group_size
computed_power = a ** b
computed_grouped = (a + b) * c
computed_ungrouped = a + b * c

  SOLUTION main.py:
tokens = 17
group_size = 5
a = 2
b = 3
c = 4
computed_division = tokens / group_size
computed_quotient = tokens // group_size
computed_remainder = tokens % group_size
computed_power = a ** b
computed_grouped = (a + b) * c
computed_ungrouped = a + b * c
division = computed_division
quotient = computed_quotient
remainder = computed_remainder
power = computed_power
grouped = computed_grouped
ungrouped = computed_ungrouped

  test t0 (value_equals, visible=True): {"expr":"[division, quotient, remainder, power, grouped, ungrouped]","expected":[3.4,3,2,8,20,14]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2f3f21d11548c314abbe636fc64fb8fc6a6864943155cb01df4a2c5f66f04eaa","tests_passed":1}
  feedback✔: The result meets the task. The calculations produce 3.4 for 17 / 5, 3 for 17 // 5, 2 for 17 % 5, 8 for 2 ** 3, 20 for (2 + 3) * 4 and 14 for 2 + 3 * 4.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Read each supplied calculation: / divides, // floors the quotient, % gives the remainder, ** raises a power, and parentheses group addition before multiplication. Bind each result to its requested output name.']
  MEASURES: C:apply_floor_division_remainder_and_exponentiation(f2); C:apply_parentheses_and_operator_precedence(f3)   anchors=['practice', 'assessment:apply_floor_division_remainder_and_exponentiation', 'assessment:apply_parentheses_and_operator_precedence']
  taught-before-tested: C.f2←s11; C.f3←s11

### s14 · recap · Takeaways
(takeaway) Assignment uses current values; recalculation needs a new assignment. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3⟧
(takeaway) Distinguish int, float, str and bool before combining values. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B:tb2 B:tb3⟧
(takeaway) Operators and parentheses determine the calculation. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3⟧
[UP NEXT] Comparison Operators: Choose whether a quantity threshold includes its boundary.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit variables assignment
(definition) Write name = value. A later right-hand expression uses a name’s current value. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Combine named numbers with +, -, * or / on the right, then assign the result. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Changing quantity does not recalculate cost. Assign cost again to use quantity’s current value. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
quantity = 3
unit_price = 4
cost = quantity * unit_price
quantity = 5
cost = quantity * unit_price
  annotations: []
### r02 · Revisit variables assignment
(definition) Assignment binds a name to the right-hand expression’s value; another assignment can rebind it. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Write name = value. A later right-hand expression uses a name’s current value. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Names are case-sensitive. ASCII names may contain letters, underscores and digits, but cannot begin with a digit or be a keyword. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Combine named numbers with +, -, * or / on the right, then assign the result. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Changing quantity does not recalculate cost. Assign cost again to use quantity’s current value. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
quantity = 3
unit_price = 4
cost = quantity * unit_price
quantity = 5
cost = quantity * unit_price
  annotations: []
### r03 · Revisit core data types
(definition) An int represents an integer. A numeric literal with a decimal point or exponent produces a float. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) In mixed int/float arithmetic, the int operand is converted to float. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Text has type str. Single or double quotes create string literals; + joins strings. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Quoted numeric text is a string; joining text is different from adding numbers. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
quantity = 3
price = 4.5
label = "Notebook"
print(type(quantity))
print(type(price))
print(label + " order")
print(quantity * price)
print(quantity == 3)
  annotations: []
### r04 · Revisit core data types
(definition) A bool represents truth with True or False. ⟦B.f4 B:tb3 B:tb4⟧
(definition) Equality or ordering comparisons between numbers produce a boolean. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) A numeric comparison produces a bool, not a text label. ⟦B.f5 B:tb3 B:tb4⟧
[CODE python]
quantity = 3
price = 4.5
label = "Notebook"
print(type(quantity))
print(type(price))
print(label + " order")
print(quantity * price)
print(quantity == 3)
  annotations: []
### r05 · Revisit core data types
(definition) An int represents an integer. A numeric literal with a decimal point or exponent produces a float. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Text has type str. Single or double quotes create string literals; + joins strings. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) A bool represents truth with True or False. ⟦B.f4 B:tb3 B:tb4⟧
(definition) type(value) returns the type of that value. ⟦B.f6 B:tb3 B:tb4 B:tb5⟧
(definition) print(value) displays the value’s string representation. ⟦B.f7 B:tb3 B:tb4⟧
(misconception) Quoted numeric text is a string; joining text is different from adding numbers. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
quantity = 3
price = 4.5
label = "Notebook"
print(type(quantity))
print(type(price))
print(label + " order")
print(quantity * price)
print(quantity == 3)
  annotations: []
### r06 · Revisit arithmetic operators
(definition) For numbers, + adds, - subtracts, * multiplies and / divides. Dividing ints produces a float. ⟦C.f1 C:tb2 C:tb4⟧
(misconception) Ordinary division of integer inputs produces a float; it is not the floored quotient. ⟦C.f1 C:tb2 C:tb4⟧
[CODE python]
print(17 / 5)
print(17 // 5)
print(17 % 5)
print(2 ** 3)
print((2 + 3) * 4)
print(2 + 3 * 4)
  annotations: []
### r07 · Revisit arithmetic operators
(definition) // gives the floored quotient, % the remainder, and ** a power. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) Parentheses group calculations. Exponentiation has higher precedence than multiplication, division and remainder; those have higher precedence than addition and subtraction. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) The floored quotient counts complete groups; the remainder answers what is left over. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
[CODE python]
print(17 / 5)
print(17 // 5)
print(17 % 5)
print(2 ** 3)
print((2 + 3) * 4)
print(2 + 3 * 4)
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: Function calls, including print() and input()
· spec.expected: <class 'int'>
3
<class 'float'>
4.5
<class 'str'>
notebook
<class 'bool'>
True
· expected.value: <class 'int'>
10
<class 'float'>
4.5
<class 'str'>
notebook
<class 'bool'>
True
· expected.value: <class 'int'>
3
<class 'float'>
11.5
<class 'str'>
notebook
<class 'bool'>
True

=========

# EVALUATOR PACKET — Comparison Operators / Logical Operators / Type Conversion (learn_python.tile.003_005)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.comparison_operators — Comparison Operators
B = python.logical_operators — Logical Operators
C = python.type_conversion — Type Conversion

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=12
  warn: remediation step learn_python.tile.003_005.r02 is never referenced
  warn: remediation step learn_python.tile.003_005.r04 is never referenced
  warn: remediation step learn_python.tile.003_005.r06 is never referenced
  warn: remediation step learn_python.tile.003_005.r07 is never referenced
  warn: learn_python.tile.003_005.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.003_005.s04/ix.learn_python.tile.003_005.s04: ADVISORY — syntax descriptors with no detector: ['!=', '<', '<=', '==', '>', '>=', 'assert', 'assignment with =', 'boolean literals True and False', 'comprehensions', 'conditional expressions', 'dictionary literals', 'for', 'import', 'integer literals', 'is', 'is not', 'list literals', 'set literals', 'tuple literals', 'variable references', 'while']
  warn: learn_python.tile.003_005.s05: prose block without lineage.fact_ids
  warn: learn_python.tile.003_005.s09/ix.learn_python.tile.003_005.s09: ADVISORY — syntax descriptors with no detector: ['True and False', 'assert', 'comparison operators ==, !=, <, <=, >, >=', 'comprehensions', 'for', 'import', 'integer literals', 'list, tuple, set, and dictionary construction', 'try/except', 'variable assignment with =', 'variable names', 'while']
  warn: learn_python.tile.003_005.s10: prose block without lineage.fact_ids
  warn: learn_python.tile.003_005.s14/ix.learn_python.tile.003_005.s14: ADVISORY — syntax descriptors with no detector: ['comprehensions', 'floating-point literals', 'for', 'if / elif / else', 'import', 'integer literals', 'list, set, dictionary, and tuple constructions', 'name = expression', 'numeric multiplication with *', 'raise', 'string literals', 'string method calls', 'try / except / finally', 'while']
  warn: plan: learn_python.tile.003_005.s14 was planned to measure python.type_conversion#assessment:convert_value_to_string but its interaction does not
  warn: plan: learn_python.tile.003_005.s14 was planned to measure python.type_conversion#assessment:recognize_unsuitable_numeric_text_and_value_error but its interaction does not

## SOURCE FACTS — A (python.comparison_operators)   objective: Compare Python values and produce booleans.
A.f1: x == y tests equality and x != y tests inequality.   [sources: python_stdlib_reference#stdtypes.html#comparisons]
A.f2: x < y and x > y test strict ordering, while x <= y and x >= y include equality.   [sources: python_stdlib_reference#stdtypes.html#comparisons]
A.f3: Comparisons between supported scalar values produce True or False.   [sources: python_stdlib_reference#stdtypes.html#comparisons]
note: Begin with this objective: Compare Python values and produce booleans.
note: Keep the example in the Comparisons, conditions and conversions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.logical_operators, python.type_conversion, python.conditional_statements.
PRACTICE ANCHOR (live_code): Create simple threshold checks for quantity: at least three, more than three, at most three, and less than three.  SUCCESS: Use >=, >, <=, and < for the corresponding rules. With quantity equal to 3, the checks evaluate to True, False, True, and False respectively.
ASSESSMENT ANCHOR: write_equality_and_inequality_comparisons facts=['f1', 'f3']
ASSESSMENT ANCHOR: write_strict_and_inclusive_threshold_comparisons facts=['f2', 'f3']
ASSESSMENT ANCHOR: predict_boolean_comparison_results facts=['f3']

## SOURCE FACTS — B (python.logical_operators)   objective: Combine boolean conditions with and, or, and not.
B.f1: For boolean conditions, a and b is true when both are true; a or b is true when at least one is true; not a reverses its truth value.   [sources: python_stdlib_reference#stdtypes.html#boolean-operations-and-or-not]
B.f2: and skips its second operand when the first is false, while or skips its second operand when the first is true.   [sources: python_stdlib_reference#stdtypes.html#boolean-operations-and-or-not]
B.f3: not has higher priority than and, which has higher priority than or; parentheses can make the intended grouping explicit.   [sources: python_stdlib_reference#stdtypes.html#boolean-operations-and-or-not]
note: Begin with this objective: Combine boolean conditions with and, or, and not.
note: Keep the example in the Comparisons, conditions and conversions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.type_conversion, python.conditional_statements, python.while_loops.
PRACTICE ANCHOR (live_code): Create a multi-condition eligibility rule that is true only when both quantity_ok and budget_ok are true.  SUCCESS: The expression quantity_ok and budget_ok produces False for the starting values and True when both conditions are true.
ASSESSMENT ANCHOR: predict_compound_boolean_results facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_short_circuited_operands facts=['f2']
ASSESSMENT ANCHOR: write_grouped_boolean_conditions facts=['f1', 'f3']

## SOURCE FACTS — C (python.type_conversion)   objective: Convert a value from one core type to another using casting functions like int(), float(), str().
C.f1: int(value) constructs an integer from suitable numeric text or a number; conversion from float truncates toward zero.   [sources: python_stdlib_reference#functions.html#int]
C.f2: float(text) constructs a floating-point value from text in a supported numeric form.   [sources: python_stdlib_reference#functions.html#float]
C.f3: str(value) constructs a string representation of a value.   [sources: python_stdlib_reference#stdtypes.html#str]
C.f4: An invalid numeric string can raise ValueError, indicating that the value is unsuitable for the requested conversion.   [sources: python_stdlib_reference#exceptions.html#ValueError]
C.f5: To reuse a converted value in a calculation, assign the conversion result to a name; this does not rebind the original name unless that name is the assignment target.   [sources: python_language_reference#simple_stmts.html#assignment-statements]
note: Begin with this objective: Convert a value from one core type to another using casting functions like int(), float(), str().
note: Keep the example in the Comparisons, conditions and conversions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.conditional_statements, python.while_loops, python.lists.
note: Adapt the practice objective's reading step to use an already assigned numeric string; console input is outside the allowed boundary.
note: Adapt assessment of conversion errors to recognizing unsuitable numeric text and the resulting ValueError; implementing exception recovery is outside the allowed boundary.
PRACTICE ANCHOR (live_code): Convert the numeric string assigned to quantity_text to a float stored as quantity, then multiply quantity by price and assign the calculation result to price.  SUCCESS: With quantity_text initially "3" and price initially 4.5, quantity holds 3.0 and price holds 13.5 after the calculation; quantity_text remains "3".
ASSESSMENT ANCHOR: convert_to_integer_and_predict_truncation facts=['f1']
ASSESSMENT ANCHOR: convert_numeric_text_to_float facts=['f2']
ASSESSMENT ANCHOR: convert_value_to_string facts=['f3']
ASSESSMENT ANCHOR: recognize_unsuitable_numeric_text_and_value_error facts=['f4']
ASSESSMENT ANCHOR: reuse_conversion_result_without_rebinding_original_name facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Choosing a built-in collection; Comprehensions; Conditional Statements; Defining Calling Functions; Dictionaries; Enumerate iteration; Error Handling; File Io; Floating-point approximation limits; For Loops; Function Default Keyword Args; Import Statements; Indentation and code blocks; Iterating Collections; Lists; Logical Operators; Loop Control; PEP 8 Style; Parameters Arguments; Reading and displaying console values; Return Values; Sets; String Basics Formatting; Tuples; Type Conversion; Variable Scope; While Loops

## LESSON, in learner order

### s01 · explainer · Comparison Operators
(intro) Choose whether a quantity threshold includes its boundary. ⟦A:tb1⟧
(definition) Use == to test equality and != to test inequality. ⟦A.f1 A:tb2⟧
(mechanism) < and > test strict ordering. <= and >= also include equality. ⟦A.f2 A:tb3⟧
(mechanism) Comparisons between supported scalar values produce True or False. ⟦A.f3 A:tb3⟧
(example) Read each quantity comparison as a question. Equality is different from assignment; an inclusive threshold accepts the boundary while a strict threshold does not. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) At the boundary, >= includes equality but > does not. Use == for an equality test, not assignment’s =. ⟦A.f1 A.f2 A:tb5⟧
[CODE python]
quantity = 3
print(quantity == 3)
print(quantity != 3)
print(quantity > 3)
print(quantity >= 3)
print(quantity < 3)
print(quantity <= 3)
  annotations: ['Read the operator: strict or inclusive, equality or inequality?', 'Read the operator: strict or inclusive, equality or inequality?', 'Read the operator: strict or inclusive, equality or inequality?', 'Read the operator: strict or inclusive, equality or inequality?', 'Read the operator: strict or inclusive, equality or inequality?', 'Read the operator: strict or inclusive, equality or inequality?']

### s02 · check · Check comparison operators
Quick check — Decide which comparison expresses equality, inequality, or an inclusive or strict quantity threshold.
QUESTION [choice, intro, grading=client] Which group correctly expresses equal, unequal, strictly above and at least the threshold 3?
  ✔ a: quantity == 3; quantity != 3; quantity > 3; quantity >= 3
      why: Correct. quantity == 3; quantity != 3; quantity > 3; quantity >= 3
  ✘ b: quantity = 3; quantity != 3; quantity >= 3; quantity > 3
      why: Single = assigns rather than compares, and the strict and inclusive checks are swapped.
  ✘ c: quantity == 3; quantity == 3; quantity < 3; quantity <= 3
      why: Equality is not inequality, and below checks do not express above thresholds.
  feedback✔: Correct. quantity == 3; quantity != 3; quantity > 3; quantity >= 3  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:write_equality_and_inequality_comparisons(f1,f3); A:write_strict_and_inclusive_threshold_comparisons(f2,f3)   anchors=['assessment:write_equality_and_inequality_comparisons', 'assessment:write_strict_and_inclusive_threshold_comparisons']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01; A.f3←s01

### s03 · check · Check comparison operators
Quick check — Decide which Boolean result the supplied quantity comparison produces.
QUESTION [choice, core, grading=client] With quantity = 3 and threshold 3, which listed comparison produces False because it excludes equality?
  ✔ a: quantity > 3
      why: Correct. quantity > 3
  ✘ b: quantity >= 3
      why: >= includes equality.
  ✘ c: quantity == 3
      why: == explicitly tests equality rather than excluding it.
  feedback✔: Correct. quantity > 3  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: A:predict_boolean_comparison_results(f3)   anchors=['assessment:predict_boolean_comparison_results']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Practice comparison operators
Practice — Create simple threshold checks for quantity: at least three, more than three, at most three, and less than three.
QUESTION [code_exercise, intro, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_at_least to at_least. Assign computed_more to more. Assign computed_at_most to at_most. Assign computed_less to less. The checker reads at_least, more, at_most, less.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable references', 'assignment with =', 'integer literals', 'boolean literals True and False', '==', '!=', '<', '>', '<=', '>='] blocked=20 items
  file main.py [editable]:
quantity = 3
computed_at_least = quantity >= 3
computed_more = quantity > 3
computed_at_most = quantity <= 3
computed_less = quantity < 3

  SOLUTION main.py:
quantity = 3
computed_at_least = quantity >= 3
computed_more = quantity > 3
computed_at_most = quantity <= 3
computed_less = quantity < 3
at_least = computed_at_least
more = computed_more
at_most = computed_at_most
less = computed_less

  test t0 (value_equals, visible=True): {"expr":"[at_least, more, at_most, less]","expected":[true,false,true,false]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"48f8db4814202085461ccc0585225d52a4ea004292fbff682b5dde746f2c95d8","tests_passed":1}
  feedback✔: The result meets the task. Use >=, >, <=, and < for the corresponding rules. With quantity equal to 3, the checks evaluate to True, False, True, and False respectively.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Read the supplied operators first: >= and <= include equality; > and < exclude it. Bind each computed result to its corresponding output name.']
  MEASURES: A:write_equality_and_inequality_comparisons(f1,f3); A:write_strict_and_inclusive_threshold_comparisons(f2,f3); A:predict_boolean_comparison_results(f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01; A.f3←s01; A.f3←s01

### s05 · explainer · Logical Operators
(intro) Combine quantity and budget conditions. ⟦B:tb1⟧
(definition) For boolean conditions, and is true when both are true; or is true when at least one is true; not reverses the truth value. ⟦B.f1 B:tb2⟧
(mechanism) and skips its second operand if the first is false. or skips its second operand if the first is true. ⟦B.f2 B:tb3⟧
(mechanism) not has higher priority than and, and and higher priority than or. Parentheses make grouping explicit. ⟦B.f3 B:tb3⟧
[CODE python]
quantity_ok = 3 >= 3
budget_ok = 12 >= 15
print(quantity_ok and budget_ok)
print(quantity_ok or budget_ok)
print(not budget_ok)
print(not (quantity_ok and budget_ok))
  annotations: ['quantity_ok is True, so and evaluates budget_ok; the result is False.', 'quantity_ok is True, so or skips budget_ok; the result is True.', 'Trace grouping and whether the second operand is evaluated.', 'Parentheses group quantity_ok and budget_ok; not reverses that grouped result.']

### s06 · explainer · Logical Operators
(example) Track quantity_ok and budget_ok separately before combining them. Mark whether a second operand is needed, then read any not and parentheses before evaluating the full rule. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) Do not assume both operands are evaluated: and can stop after a false first operand, while or can stop after a true one. ⟦B.f2 B.f3 B:tb5⟧

### s07 · check · Check logical operators
Quick check — Trace the compound Boolean expression and decide which operands are evaluated or skipped.
QUESTION [choice, core, grading=client] For False and quantity_ok, which statement describes the result and evaluation of the right operand?
  ✔ a: The result is False and quantity_ok is not evaluated.
      why: Correct. The result is False and quantity_ok is not evaluated.
  ✘ b: The result is True and quantity_ok is evaluated.
      why: and with a false left operand short-circuits with that false value.
  ✘ c: The result is False but quantity_ok must still be evaluated.
      why: and skips its right operand when its left operand is false.
  feedback✔: Correct. The result is False and quantity_ok is not evaluated.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r03
  MEASURES: B:predict_compound_boolean_results(f1,f3); B:identify_short_circuited_operands(f2)   anchors=['assessment:predict_compound_boolean_results', 'assessment:identify_short_circuited_operands']
  taught-before-tested: B.f1←s05; B.f3←s05; B.f2←s05

### s08 · check · Check logical operators
Quick check — Decide which grouping expresses the intended Boolean condition.
QUESTION [choice, core, grading=client] To allow a request only if budget_ok is true and either quantity_ok or label_ok is true, which grouping fits?
  ✔ a: budget_ok and (quantity_ok or label_ok)
      why: Correct. budget_ok and (quantity_ok or label_ok)
  ✘ b: (budget_ok and quantity_ok) or label_ok
      why: This permits label_ok alone to bypass the budget requirement.
  ✘ c: budget_ok or (quantity_ok and label_ok)
      why: This allows budget_ok alone and does not enforce the stated combined requirement.
  feedback✔: Correct. budget_ok and (quantity_ok or label_ok)  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: B:write_grouped_boolean_conditions(f1,f3)   anchors=['assessment:write_grouped_boolean_conditions']
  taught-before-tested: B.f1←s05; B.f3←s05

### s09 · hands_on · Practice logical operators
Practice — Create a multi-condition eligibility rule that is true only when both quantity_ok and budget_ok are true.
QUESTION [code_exercise, core, grading=client] Combine the supplied boolean checks: accepted must be true only when both quantity_ok and budget_ok are true. Keep the input checks; assign their combination to accepted.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'variable names', 'integer literals', 'True and False', 'comparison operators ==, !=, <, <=, >, >=', 'and', 'or', 'not', 'parentheses for grouping'] blocked=14 items
  file main.py [editable]:
quantity = 3
budget = 12
quantity_ok = quantity >= 3
budget_ok = budget >= 15

  SOLUTION main.py:
quantity = 3
budget = 12
quantity_ok = quantity >= 3
budget_ok = budget >= 15
accepted = quantity_ok and budget_ok

  test t0 (value_equals, visible=True): {"expr":"accepted","expected":false} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"1ceac17029525aeaab2bce0c6186988df22ecd1122ea4f4fbe404b5b8162c1f4","tests_passed":1}
  feedback✔: The result meets the task. The expression quantity_ok and budget_ok produces False for the starting values and True when both conditions are true.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Keep the supplied inputs and use their names in your computation.', 'Check indentation and the exact result names requested in the prompt.']
  MEASURES: B:predict_compound_boolean_results(f1,f3); B:identify_short_circuited_operands(f2); B:write_grouped_boolean_conditions(f1,f3)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f3←s05; B.f2←s05; B.f1←s05; B.f3←s05

### s10 · explainer · Type Conversion
(intro) Convert numeric quantity text before using it in a calculation. ⟦C:tb1⟧
(definition) int(value) constructs an integer from suitable numeric text or a number. A float-to-int conversion truncates toward zero. ⟦C.f1 C:tb2⟧
(mechanism) float(text) constructs a floating-point value from supported numeric text. ⟦C.f2 C:tb3⟧
(mechanism) str(value) constructs a string representation. ⟦C.f3 C:tb3⟧
(mechanism) Invalid numeric text can raise ValueError: the value is unsuitable for that conversion. ⟦C.f4 C:tb3⟧
(mechanism) Assign the converted result to a name for later calculations. The original name changes only if it is the assignment target. ⟦C.f5 C:tb3⟧
[CODE python]
quantity_text = "3"
quantity = float(quantity_text)
price = float("4.5")
price = quantity * price
print(quantity_text)
print(quantity)
print(price)
print(int(-3.8))
  annotations: ['Bind quantity to the converted float; quantity_text remains text.', 'Use the current quantity and price, then rebind price to the product.', 'Float-to-int conversion truncates toward zero.']

### s11 · explainer · Type Conversion
(example) Keep quantity_text separate from the converted quantity. The price conversion supplies a numeric value for multiplication. Compare suitable numeric text with an arbitrary word, and read float-to-int conversion as truncation toward zero. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4⟧
(misconception) A conversion returns a value; it does not automatically rebind quantity_text. Truncating toward zero is not general rounding. ⟦C.f1 C.f5 C:tb5⟧

### s12 · check · Check type conversion
Quick check — Decide which integer results from the supplied conversion, accounting for truncation.
QUESTION [choice, core, grading=client] Which statement correctly describes int(-3.8), str(3), and float("three")?
  ✔ a: -3; the string "3"; raises ValueError
      why: int(-3.8) truncates toward zero to -3; str(3) constructs the string "3"; unsuitable numeric text "three" makes float raise ValueError.
  ✘ b: -4; the integer 3; returns 3.0
      why: int(-3.8) truncates toward zero, not down to -4. str(3) produces a string, not an integer, and "three" is unsuitable numeric text, so float raises ValueError.
  ✘ c: -3; the string "3"; returns 0.0
      why: The integer truncation and string construction are correct, but float("three") raises ValueError rather than returning 0.0.
  feedback✔: int(-3.8) truncates toward zero to -3; str(3) constructs the string "3"; unsuitable numeric text "three" makes float raise ValueError.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r05
  MEASURES: C:convert_to_integer_and_predict_truncation(f1); C:convert_value_to_string(f3); C:recognize_unsuitable_numeric_text_and_value_error(f4)   anchors=['assessment:convert_to_integer_and_predict_truncation', 'assessment:convert_value_to_string', 'assessment:recognize_unsuitable_numeric_text_and_value_error']
  taught-before-tested: C.f1←s10; C.f3←s10; C.f4←s10

### s13 · check · Check type conversion
Quick check — Decide which name stores the conversion result and which retains its original value.
QUESTION [choice, core, grading=client] After quantity = float(quantity_text), what happens to quantity_text?
  ✔ a: Its original text binding remains unchanged.
      why: Correct. Its original text binding remains unchanged.
  ✘ b: It now holds the converted float too.
      why: The returned conversion is assigned to quantity, not quantity_text.
  ✘ c: It is removed because its value was converted.
      why: Conversion returns a new result and does not remove the original binding.
  feedback✔: Correct. Its original text binding remains unchanged.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: C:reuse_conversion_result_without_rebinding_original_name(f5)   anchors=['assessment:reuse_conversion_result_without_rebinding_original_name']
  taught-before-tested: C.f5←s10

### s14 · hands_on · Practice type conversion
Practice — Convert the numeric string assigned to quantity_text to a float stored as quantity, then multiply quantity by price and assign the calculation result to price.
QUESTION [code_exercise, intro, grading=client] Replace the placeholder so quantity receives the floating-point conversion of quantity_text. Keep the supplied multiplication unchanged, then assign computed_price to price. Keep quantity_text unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['name = expression', 'string literals', 'integer literals', 'floating-point literals', 'float(value)', 'int(value)', 'str(value)', 'numeric multiplication with *'] blocked=14 items
  file main.py [editable]:
quantity_text = "3"
price = 4.5
quantity = price
computed_price = quantity * price

  SOLUTION main.py:
quantity_text = "3"
price = 4.5
quantity = float(quantity_text)
computed_price = quantity * price
price = computed_price

  test t0 (value_equals, visible=True): {"expr":"[type(quantity).__name__, quantity, type(price).__name__, price, quantity_text]","expected":["float",3.0,"float",13.5,"3"]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"0eec05ba36669bb67960d4c128930f9e4389af9b7a3e35823e79740dfcfe43b1","tests_passed":1}
  feedback✔: The result meets the task. With quantity_text initially "3" and price initially 4.5, quantity holds 3.0 and price holds 13.5 after the calculation; quantity_text remains "3".  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Check the exact operations and result names requested in the prompt.']
  MEASURES: C:convert_numeric_text_to_float(f2)   anchors=['practice', 'assessment:convert_numeric_text_to_float']
  taught-before-tested: C.f2←s10

### s15 · recap · Takeaways
(takeaway) Strict and inclusive comparisons differ at equality. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3⟧
(takeaway) Combine boolean conditions and respect short-circuiting and grouping. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3⟧
(takeaway) Store conversion results; distinguish truncation from rounding. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3⟧
[UP NEXT] Conditional Statements: Choose one order-size response by testing conditions in order.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit comparison operators
(definition) Use == to test equality and != to test inequality. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) < and > test strict ordering. <= and >= also include equality. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) Comparisons between supported scalar values produce True or False. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) An inclusive threshold includes equality at the boundary; a strict threshold excludes it. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
quantity = 3
print(quantity == 3)
print(quantity != 3)
print(quantity > 3)
print(quantity >= 3)
print(quantity < 3)
print(quantity <= 3)
  annotations: []
### r02 · Revisit comparison operators
(definition) Comparisons between supported scalar values produce True or False. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Read a comparison as a question with a boolean result, not an assignment of its right-hand value. ⟦A.f3 A:tb3 A:tb4⟧
[CODE python]
quantity = 3
print(quantity == 3)
print(quantity != 3)
print(quantity > 3)
print(quantity >= 3)
print(quantity < 3)
print(quantity <= 3)
  annotations: []
### r03 · Revisit logical operators
(definition) For boolean conditions, and is true when both are true; or is true when at least one is true; not reverses the truth value. ⟦B.f1 B:tb2 B:tb4⟧
(definition) and skips its second operand if the first is false. or skips its second operand if the first is true. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) not has higher priority than and, and and higher priority than or. Parentheses make grouping explicit. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) and requires both boolean conditions; or accepts at least one. ⟦B.f1 B:tb2 B:tb4⟧
[CODE python]
quantity_ok = 3 >= 3
budget_ok = 12 >= 15
print(quantity_ok and budget_ok)
print(quantity_ok or budget_ok)
print(not budget_ok)
  annotations: []
### r04 · Revisit logical operators
(definition) For boolean conditions, and is true when both are true; or is true when at least one is true; not reverses the truth value. ⟦B.f1 B:tb2 B:tb4⟧
(definition) not has higher priority than and, and and higher priority than or. Parentheses make grouping explicit. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) and requires both boolean conditions; or accepts at least one. ⟦B.f1 B:tb2 B:tb4⟧
[CODE python]
quantity_ok = 3 >= 3
budget_ok = 12 >= 15
print(quantity_ok and budget_ok)
print(quantity_ok or budget_ok)
print(not budget_ok)
  annotations: []
### r05 · Revisit type conversion
(definition) int(value) constructs an integer from suitable numeric text or a number. A float-to-int conversion truncates toward zero. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(misconception) Float-to-int conversion truncates toward zero; it is not general rounding. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
[CODE python]
quantity_text = "3"
quantity = int(quantity_text)
price = float("4.5")
print(quantity * price)
print(quantity_text)
print(int(-3.8))
print(str(quantity))
  annotations: []
### r06 · Revisit type conversion
(definition) Assign the converted result to a name for later calculations. The original name changes only if it is the assignment target. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
(misconception) Assigning a conversion to quantity does not rebind quantity_text. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantity_text = "3"
quantity = int(quantity_text)
price = float("4.5")
print(quantity * price)
print(quantity_text)
print(int(-3.8))
print(str(quantity))
  annotations: []
### r07 · Revisit type conversion
(definition) float(text) constructs a floating-point value from supported numeric text. ⟦C.f2 C:tb3 C:tb4⟧
(definition) str(value) constructs a string representation. ⟦C.f3 C:tb3 C:tb4⟧
(definition) Invalid numeric text can raise ValueError: the value is unsuitable for that conversion. ⟦C.f4 C:tb3 C:tb4⟧
(misconception) Suitable numeric text and an arbitrary word are different conversion inputs; an invalid input can raise ValueError. ⟦C.f4 C:tb3 C:tb4⟧
[CODE python]
quantity_text = "3"
quantity = int(quantity_text)
price = float("4.5")
print(quantity * price)
print(quantity_text)
print(int(-3.8))
print(str(quantity))
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: function calls, including print(), input(), and conversion calls
· constraints.blocked_syntax: int(), float(), str(), bool()

=========

# EVALUATOR PACKET — Conditional Statements / While Loops (learn_python.tile.006_007)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.conditional_statements — Conditional Statements
B = python.while_loops — While Loops

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=6
  warn: remediation step learn_python.tile.006_007.r02 is never referenced
  warn: remediation step learn_python.tile.006_007.r04 is never referenced
  warn: learn_python.tile.006_007.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.006_007.s03/ix.learn_python.tile.006_007.s03: ADVISORY — syntax descriptors with no detector: ['assert', 'class', 'comprehensions', 'dictionary literals', 'elif condition:', 'else:', 'for', 'from ... import', 'if condition:', 'import', 'indented branch bodies', 'integer literals', 'list literals', 'raise', 'set literals', 'string formatting', 'string literals', 'string method calls', 'try/except', 'tuple literals', 'variable assignment with =', 'while', 'with', 'yield']
  warn: learn_python.tile.006_007.s04: prose block without lineage.fact_ids
  warn: learn_python.tile.006_007.s07/ix.learn_python.tile.006_007.s07: ADVISORY — syntax descriptors with no detector: ['comparison with !=', 'comprehensions', 'for', 'import', 'list, set, dictionary, and tuple construction', 'nested loops', 'string method calls', 'text literals', 'try/except', 'variable assignment with =', 'while condition: with an indented body']

## SOURCE FACTS — A (python.conditional_statements)   objective: Branch program execution based on conditions using if/elif/else.
A.f1: Write if condition: followed by an indented body, with aligned elif condition: bodies and an optional else: body.   [sources: python_language_reference#compound_stmts.html#if]
A.f2: Conditions are tested in order and the first true condition’s body executes; else executes if no condition is true.   [sources: python_language_reference#compound_stmts.html#if]
note: Begin with this objective: Branch program execution based on conditions using if/elif/else.
note: Keep the example in the Branching and condition-based repetition tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.while_loops, python.lists, python.sets.
PRACTICE ANCHOR (live_code): Write an if/elif/else chain that classifies a numeric score stored in quantity into three grade bands: A for scores at least 90, B for scores at least 70 but below 90, and C for scores below 70. Assign the selected band to grade.  SUCCESS: The chain assigns exactly one correct grade for each score, including scores at both boundaries, using aligned branch headers and indented assignment bodies.
ASSESSMENT ANCHOR: write_aligned_if_elif_else_branches facts=['f1']
ASSESSMENT ANCHOR: order_conditions_to_select_the_correct_branch_for_every_case facts=['f2']

## SOURCE FACTS — B (python.while_loops)   objective: Repeat a block of code until a condition becomes false using a while loop.
B.f1: Write while condition: followed by an indented body; the condition is tested before each repetition and the loop stops when it is false.   [sources: python_language_reference#compound_stmts.html#while]
B.f2: A false initial condition means the body does not run.   [sources: python_language_reference#compound_stmts.html#while]
B.f3: Update the values used by the condition in the loop body so that a condition-based loop can reach its stopping condition.   [sources: python_tutorial#introduction.html#first-steps-towards-programming]
B.f4: input(prompt) displays the prompt and returns the entered line as text, excluding its trailing newline; assign its result again in the loop to obtain a new response.   [sources: python_stdlib_reference#functions.html#input]
note: Begin with this objective: Repeat a block of code until a condition becomes false using a while loop.
note: Keep the example in the Branching and condition-based repetition tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.lists, python.sets, python.dictionaries.
PRACTICE ANCHOR (live_code): Write a while loop that keeps requesting a response until the user enters the accepted value "done".  SUCCESS: Entering "blue" requests another response; entering "done" ends repetition. Entering "done" at the first prompt skips the loop body.
ASSESSMENT ANCHOR: write_pretested_while_loop facts=['f1', 'f2']
ASSESSMENT ANCHOR: update_condition_values_to_enable_termination facts=['f1', 'f3']
ASSESSMENT ANCHOR: write_terminating_response_loop facts=['f1', 'f2', 'f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Choosing a built-in collection; Comprehensions; Defining Calling Functions; Dictionaries; Enumerate iteration; Error Handling; File Io; Floating-point approximation limits; For Loops; Function Default Keyword Args; Import Statements; Indentation and code blocks; Iterating Collections; Lists; Loop Control; PEP 8 Style; Parameters Arguments; Reading and displaying console values; Return Values; Sets; String Basics Formatting; Tuples; Using math for numeric calculations; Variable Scope; While Loops

## LESSON, in learner order

### s01 · explainer · Conditional Statements
(intro) Choose one order-size response by testing conditions in order. ⟦A:tb1⟧
(definition) Write if condition: with an indented body. Align any elif condition: headers and the optional else: header with if; indent their bodies. ⟦A.f1 A:tb2⟧
(mechanism) Test conditions in order. Execute the first true condition’s body; execute else only if none is true. ⟦A.f2 A:tb3⟧
(example) Read the size branches top to bottom. Stop at the first true condition; do not run another branch just because its test could also be true. ⟦A.f1 A.f2 A:tb4⟧
(misconception) An elif chain chooses the first true branch, not every true branch. else is the fallback only when all tests fail. ⟦A.f2 A:tb5⟧
[CODE python]
quantity = 5
if quantity >= 10:
    print("Large")
elif quantity >= 3:
    print("Medium")
else:
    print("Small")
  annotations: ['Begin with the first condition.', 'Test this only if the earlier condition was false.', 'Use this body only when no condition was true.', 'Boundary trace: quantity 12 or 10 selects Large; quantity 5 or 3 selects Medium; quantity 2 selects Small. At each input, only the first true branch runs.']

### s02 · check · Check conditional statements
Quick check — Decide which ordering of conditions selects the intended branch for each input.
QUESTION [choice, intro, grading=client] A grade chain awards A at scores >= 90, B at scores >= 70 but < 90, C otherwise. Which order works when using >= threshold conditions?
  ✔ a: Test >= 90 first, then >= 70, then else.
      why: Correct. Test >= 90 first, then >= 70, then else.
  ✘ b: Test >= 70 first, then >= 90, then else.
      why: The earlier >= 70 branch would also catch scores deserving A.
  ✘ c: Use two independent if statements followed by else.
      why: Independent if statements are not the required exclusive if/elif/else chain.
  feedback✔: Correct. Test >= 90 first, then >= 70, then else.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:order_conditions_to_select_the_correct_branch_for_every_case(f2)   anchors=['assessment:order_conditions_to_select_the_correct_branch_for_every_case']
  taught-before-tested: A.f2←s01

### s03 · hands_on · Practice conditional statements
Practice — Write an if/elif/else chain that classifies a numeric score stored in quantity into three grade bands: A for scores at least 90, B for scores at least 70 but below 90, and C for scores below 70. Assign the selected band to grade.
QUESTION [code_exercise, intro, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_grade to grade. The checker reads grade.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'integer literals', 'string literals', 'comparison operators', 'if condition:', 'elif condition:', 'else:', 'indented branch bodies'] blocked=24 items
  file main.py [editable]:
quantity = 85
high_boundary = 90
middle_boundary = 70
high_grade = "A"
middle_grade = "B"
low_grade = "C"
if quantity >= high_boundary:
    computed_grade = high_grade
elif quantity >= middle_boundary:
    computed_grade = middle_grade
else:
    computed_grade = low_grade

  SOLUTION main.py:
quantity = 85
high_boundary = 90
middle_boundary = 70
high_grade = "A"
middle_grade = "B"
low_grade = "C"
if quantity >= high_boundary:
    computed_grade = high_grade
elif quantity >= middle_boundary:
    computed_grade = middle_grade
else:
    computed_grade = low_grade
grade = computed_grade

  test t0 (value_equals, visible=True): {"expr":"[grade, [(lambda scope: (exec(open(\"main.py\").read().replace(\"quantity = 85\", \"quantity = \" + str(score)), scope), scope[\"grade\"])[1])({}) for score in [69, 70, 89, 90]]]","expected":["B",["C","B","B","A"]]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"525dd2e920241592405c98a0ef19696b88942ae1aa0493d5ece9a4755327330c","tests_passed":1}
  feedback✔: The result meets the task. The chain assigns exactly one correct grade for each score, including scores at both boundaries, using aligned branch headers and indented assignment bodies.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Trace the higher boundary first, then the middle boundary, then the fallback. After the chain, bind its selected computed_grade to grade.']
  MEASURES: A:write_aligned_if_elif_else_branches(f1); A:order_conditions_to_select_the_correct_branch_for_every_case(f2)   anchors=['practice', 'assessment:write_aligned_if_elif_else_branches', 'assessment:order_conditions_to_select_the_correct_branch_for_every_case']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · explainer · While Loops
(intro) Keep asking for labels until the response reaches the stopping condition. ⟦B:tb1⟧
(definition) Write while condition: with an indented body. Test before each repetition; stop when the condition is false. ⟦B.f1 B:tb2⟧
(mechanism) If the initial condition is false, the body never runs. ⟦B.f2 B:tb3⟧
(mechanism) Update values used by the condition inside the body so the loop can reach its stopping condition. ⟦B.f3 B:tb3⟧
(mechanism) input(prompt) displays a prompt and returns the entered line as text without its trailing newline. Assign another input result inside the loop to get a fresh response. ⟦B.f4 B:tb3⟧
[CODE python]
response = input("Enter a label, or done: ")
while response != "done":
    print(response)
    response = input("Enter a label, or done: ")
  annotations: ['Test the response before entering or repeating the body.', 'Get a new text response before the next test.', 'Trace A: the first response is red, so the condition is True and the body runs. The next response is done, so the next test is False and the loop stops. Trace B: the first response is done, so the body runs zero times.', 'In Trace A, this repeated prompt obtains done and rebinds response before the next test.']

### s05 · explainer · While Loops
(example) The first input provides the response tested at entry. The input inside the body replaces it before the next test. A stopping response at the first prompt skips the body entirely. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧
(misconception) Testing before the body means zero repetitions are possible. Reusing the old response without updating it can keep the loop repeating. ⟦B.f1 B.f2 B.f3 B:tb5⟧

### s06 · check · Check while loops
Quick check — Decide which update lets the response loop reach its stopping condition.
QUESTION [choice, core, grading=client] A loop tests response != "done". What must its body do to let a later entered done terminate it?
  ✔ a: Reassign response from a fresh input request.
      why: Correct. Reassign response from a fresh input request.
  ✘ b: Keep response unchanged and only test it again.
      why: An unchanged non-done response keeps the same condition true.
  ✘ c: Assign the fresh input only to a different name.
      why: The loop condition reads response, so updating an unrelated name does not update that condition.
  feedback✔: Correct. Reassign response from a fresh input request.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r03
  MEASURES: B:update_condition_values_to_enable_termination(f1,f3)   anchors=['assessment:update_condition_values_to_enable_termination']
  taught-before-tested: B.f1←s04; B.f3←s04

### s07 · hands_on · Practice while loops
Practice — Write a while loop that keeps requesting a response until the user enters the accepted value "done".
QUESTION [code_exercise, intro, grading=client] Assign supplied_stop_label to stop_label before the supplied first input call and while loop. Keep the input calls and the loop unchanged; the loop requests another response until the stop label is entered.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'text literals', 'comparison with !=', 'while condition: with an indented body', 'input(prompt)'] blocked=15 items
  file main.py [editable]:
seed = "blue"
_requests = []
_supplied = []
_answers = iter([seed, "done"])
input = lambda prompt: (_requests.append(prompt), _supplied.append(next(_answers)), _supplied[-1])[-1]
prompt = "Enter a label, or done: "
supplied_stop_label = "done"
response = input(prompt)
while response != stop_label:
    response = input(prompt)

  SOLUTION main.py:
seed = "blue"
_requests = []
_supplied = []
_answers = iter([seed, "done"])
input = lambda prompt: (_requests.append(prompt), _supplied.append(next(_answers)), _supplied[-1])[-1]
prompt = "Enter a label, or done: "
supplied_stop_label = "done"
stop_label = supplied_stop_label
response = input(prompt)
while response != stop_label:
    response = input(prompt)

  test t0 (value_equals, visible=True): {"expr":"[_supplied, response, len(_requests), (lambda scope: (exec(open(\"main.py\").read().replace('seed = \"blue\"', 'seed = \"done\"'), scope), [scope[\"response\"], len(scope[\"_requests\"])])[1])({})]","expected":[["blue","done"],"done",2,["done",1]]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"8312dcde138fbbbdd98cd84098b167a6e884de6c7592f333aa1e6d7c191bdb6c","tests_passed":1}
  feedback✔: The result meets the task. Entering "blue" requests another response; entering "done" ends repetition. Entering "done" at the first prompt skips the loop body.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Bind stop_label before the first input call. Then trace why blue requests another response and an initial done skips the body.']
  MEASURES: B:write_pretested_while_loop(f1,f2); B:write_terminating_response_loop(f1,f2,f3,f4)   anchors=['practice', 'assessment:write_pretested_while_loop', 'assessment:write_terminating_response_loop']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04

### s08 · recap · Takeaways
(takeaway) An if/elif chain selects its first true branch. ⟦A.f1 A.f2 A:tb2 A:tb3⟧
(takeaway) A while loop tests first and needs a reachable stopping state. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3⟧
[UP NEXT] Lists: Keep the color labels in order, then correct and extend them.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit conditional statements
(definition) Test conditions in order. Execute the first true condition’s body; execute else only if none is true. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) The first true branch runs; the chain does not run every branch whose condition could be true. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
quantity = 5
if quantity >= 10:
    print("Large")
elif quantity >= 3:
    print("Medium")
else:
    print("Small")
  annotations: []
### r02 · Revisit conditional statements
(definition) Write if condition: with an indented body. Align any elif condition: headers and the optional else: header with if; indent their bodies. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Test conditions in order. Execute the first true condition’s body; execute else only if none is true. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) The first true branch runs; the chain does not run every branch whose condition could be true. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
quantity = 5
if quantity >= 10:
    print("Large")
elif quantity >= 3:
    print("Medium")
else:
    print("Small")
  annotations: []
### r03 · Revisit while loops
(definition) Write while condition: with an indented body. Test before each repetition; stop when the condition is false. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Update values used by the condition inside the body so the loop can reach its stopping condition. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) The test comes before the body, so the loop need not run once. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
[CODE python]
response = input("Enter a label, or done: ")
while response != "done":
    print(response)
    response = input("Enter a label, or done: ")
  annotations: []
### r04 · Revisit while loops
(definition) Write while condition: with an indented body. Test before each repetition; stop when the condition is false. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) If the initial condition is false, the body never runs. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Update values used by the condition inside the body so the loop can reach its stopping condition. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(definition) input(prompt) displays a prompt and returns the entered line as text without its trailing newline. Assign another input result inside the loop to get a fresh response. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) The test comes before the body, so the loop need not run once. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
[CODE python]
response = input("Enter a label, or done: ")
while response != "done":
    print(response)
    response = input("Enter a label, or done: ")
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expr: [grade, [(lambda scope: (exec(open("main.py").read().replace("quantity = 85", "quantity = " + str(score)), scope), scope["grade"])[1])({}) for score in [69, 70, 89, 90]]]
· spec.expr: [_supplied, response, len(_requests), (lambda scope: (exec(open("main.py").read().replace('seed = "blue"', 'seed = "done"'), scope), [scope["response"], len(scope["_requests"])])[1])({})]

=========

# EVALUATOR PACKET — Lists / Sets / Dictionaries (learn_python.tile.008_010)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.lists — Lists
B = python.sets — Sets
C = python.dictionaries — Dictionaries

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=13
  warn: remediation step learn_python.tile.008_010.r02 is never referenced
  warn: remediation step learn_python.tile.008_010.r03 is never referenced
  warn: remediation step learn_python.tile.008_010.r05 is never referenced
  warn: remediation step learn_python.tile.008_010.r07 is never referenced
  warn: remediation step learn_python.tile.008_010.r08 is never referenced
  warn: learn_python.tile.008_010.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.008_010.s04/ix.learn_python.tile.008_010.s04: ADVISORY — syntax descriptors with no detector: ['assert statements', 'def statements', 'for statements', 'integer literals', 'list comprehensions', 'list indexing with nonnegative and negative indices', 'list literals [item1, item2, ...]', 'list slicing with [start:stop]', 'return statements', 'string literals', 'variable assignment with =']
  warn: learn_python.tile.008_010.s05: prose block without lineage.fact_ids
  warn: learn_python.tile.008_010.s07/ix.learn_python.tile.008_010.s07: ADVISORY — syntax descriptors with no detector: ['a & b', 'a | b', 'assert', 'class', 'comprehensions', 'dictionary literals', 'for', 'import', 'list literals', 'nonempty set literals', 'string literals', 'try', 'tuple literals', 'with']
  warn: learn_python.tile.008_010.s08: prose block without lineage.fact_ids
  warn: learn_python.tile.008_010.s11/ix.learn_python.tile.008_010.s11: ADVISORY — syntax descriptors with no detector: ['Dictionary comprehensions', 'Dictionary literals using {key: value, ...}', 'Integer literals for prices', 'Nested collection access', 'String literals for product keys', 'Tuple literals', 'Variable assignment with =', 'for', 'from ... import ...', 'import', 'raise', 'try/except']
  warn: plan: learn_python.tile.008_010.s02 was planned to measure python.lists#assessment:create_ordered_mutable_list but its interaction does not
  warn: plan: learn_python.tile.008_010.s09 was planned to measure python.dictionaries#assessment:create_dictionary_with_unique_product_keys but its interaction does not

## SOURCE FACTS — A (python.lists)   objective: Create and manipulate Python's core ordered, mutable data structure: the list.
A.f1: Create a list with [item1, item2, ...]; it is an ordered collection that can be changed.   [sources: python_tutorial#introduction.html#lists]
A.f2: items[0] selects the first item, and negative indices count from the end.   [sources: python_tutorial#introduction.html#lists]
A.f3: items[start:stop] returns a new list containing items from start up to but not including stop.   [sources: python_tutorial#introduction.html#lists]
A.f4: items[index] = value replaces an item.   [sources: python_tutorial#introduction.html#lists]
A.f5: items.append(value) adds a value at the end of the list.   [sources: python_tutorial#datastructures.html#more-on-lists]
note: Begin with this objective: Create and manipulate Python's core ordered, mutable data structure: the list.
note: Keep the example in the Core mutable collections tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.sets, python.dictionaries, python.string_basics_formatting.
PRACTICE ANCHOR (live_code): Create labels with the values "red", "blue", and "green" in that order, append "yellow", and assign labels[1:3] to a variable named selected_labels.  SUCCESS: labels contains ["red", "blue", "green", "yellow"], and selected_labels contains ["blue", "green"].
ASSESSMENT ANCHOR: create_ordered_mutable_list facts=['f1']
ASSESSMENT ANCHOR: retrieve_items_by_positive_and_negative_index facts=['f2']
ASSESSMENT ANCHOR: retrieve_slice_with_exclusive_stop facts=['f3']
ASSESSMENT ANCHOR: replace_item_at_index facts=['f4']
ASSESSMENT ANCHOR: append_item_to_list facts=['f5']

## SOURCE FACTS — B (python.sets)   objective: Create and use Python's core unordered, unique-element data structure: the set.
B.f1: A set is an unordered collection of distinct elements; set(items) constructs one and removes repeated values.   [sources: python_tutorial#datastructures.html#sets]
B.f2: Use {item1, item2, ...} for a nonempty set and set() for an empty set; {} creates a dictionary.   [sources: python_tutorial#datastructures.html#sets]
B.f3: value in values tests set membership.   [sources: python_tutorial#datastructures.html#sets]
B.f4: a | b is union, containing elements in either set; a & b is intersection, containing elements in both sets.   [sources: python_tutorial#datastructures.html#sets]
note: Begin with this objective: Create and use Python's core unordered, unique-element data structure: the set.
note: Keep the example in the Core mutable collections tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.dictionaries, python.string_basics_formatting, python.defining_calling_functions.
PRACTICE ANCHOR (live_code): Convert the list assigned to first into a set to remove repeated labels, then test whether "red" belongs to first.  SUCCESS: first contains exactly "red" and "blue", with no repeated elements, and the membership expression evaluates to True.
ASSESSMENT ANCHOR: create_sets_for_unique_values facts=['f1', 'f2']
ASSESSMENT ANCHOR: test_set_membership facts=['f3']
ASSESSMENT ANCHOR: compute_set_union_and_intersection facts=['f4']

## SOURCE FACTS — C (python.dictionaries)   objective: Create and use Python's core key-value data structure: the dictionary.
C.f1: A dictionary stores key-value pairs with unique keys; use {key: value, ...} to create one.   [sources: python_tutorial#datastructures.html#dictionaries]
C.f2: mapping[key] retrieves the associated value and raises an error if the key is absent.   [sources: python_tutorial#datastructures.html#dictionaries]
C.f3: mapping[key] = value adds a key-value pair or replaces the value for an existing key.   [sources: python_tutorial#datastructures.html#dictionaries]
note: Begin with this objective: Create and use Python's core key-value data structure: the dictionary.
note: Keep the example in the Core mutable collections tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.string_basics_formatting, python.defining_calling_functions, python.parameters_arguments.
PRACTICE ANCHOR (live_code): Build a dictionary mapping notebook and pen to prices of 3 and 2, then retrieve the notebook price using bracket lookup.  SUCCESS: The dictionary associates notebook with 3 and pen with 2, and the notebook lookup retrieves 3.
ASSESSMENT ANCHOR: create_dictionary_with_unique_product_keys facts=['f1']
ASSESSMENT ANCHOR: retrieve_value_by_key_and_recognize_absent_key_error facts=['f2']
ASSESSMENT ANCHOR: add_and_replace_dictionary_values_by_key facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Choosing a built-in collection; Comprehensions; Defining Calling Functions; Dictionaries; Enumerate iteration; Error Handling; File Io; Floating-point approximation limits; For Loops; Function Default Keyword Args; Import Statements; Indentation and code blocks; Iterating Collections; Loop Control; Nested loops; PEP 8 Style; Parameters Arguments; Reading and displaying console values; Return Values; Running Python scripts; Sets; String Basics Formatting; Tuples; Using math for numeric calculations; Using range for counted iteration; Variable Scope

## LESSON, in learner order

### s01 · explainer · Lists
(intro) Keep the color labels in order, then correct and extend them. ⟦A:tb1⟧
(definition) [item1, item2, ...] creates a list: an ordered collection that can change. ⟦A.f1 A:tb2⟧
(mechanism) items[0] selects the first item. Negative indices count from the end. ⟦A.f2 A:tb3⟧
(mechanism) items[start:stop] returns a new list from start up to, but excluding, stop. ⟦A.f3 A:tb3⟧
(mechanism) items[index] = value replaces the item at that position. ⟦A.f4 A:tb3⟧
(mechanism) items.append(value) adds a value at the list’s end. ⟦A.f5 A:tb3⟧
(example) Track label positions through the replacement and append. Replacement changes an existing position; append extends the end. The slice selects a range into a new list, excluding its stop position. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧
(misconception) A slice’s stop is excluded. A slice returns a new list, unlike a single-index lookup; replacing an item is different from appending. ⟦A.f2 A.f3 A:tb5⟧
[CODE python]
labels = ["red", "blue", "green"]
print(labels[0])
print(labels[-1])
labels[1] = "navy"
labels.append("yellow")
print(labels[1:3])
print(labels)
  annotations: ['Replace the existing label at this position.', 'Append at the end.', 'Include the start position and exclude the stop position.']

### s02 · check · Check lists
Quick check — Decide which list items the supplied indexes and slice select.
QUESTION [choice, intro, grading=client] For labels = ["red", "blue", "green", "yellow"], which group retrieves the first item, last item, and a new list containing only the second and third items, respectively?
  ✔ a: labels[0]; labels[-1]; labels[1:3]
      why: Index 0 retrieves the first item, -1 retrieves the last, and [1:3] selects the second and third items, excluding the stop index.
  ✘ b: labels[1]; labels[-1]; labels[1:4]
      why: labels[1] retrieves the second item, not the first. labels[-1] is correct, but labels[1:4] includes the fourth item as well.
  ✘ c: labels[0]; labels[0]; labels[2:3]
      why: The first lookup is correct, but labels[0] retrieves the first item again, not the last; labels[2:3] contains only the third item.
  feedback✔: Index 0 retrieves the first item, -1 retrieves the last, and [1:3] selects the second and third items, excluding the stop index.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:retrieve_items_by_positive_and_negative_index(f2); A:retrieve_slice_with_exclusive_stop(f3)   anchors=['assessment:retrieve_items_by_positive_and_negative_index', 'assessment:retrieve_slice_with_exclusive_stop']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · check · Check lists
Quick check — Decide how replacing an indexed item and appending an item change the list.
QUESTION [choice, core, grading=client] Which pair of operations replaces the first label with blue, then adds yellow at the end?
  ✔ a: labels[0] = "blue"; labels.append("yellow")
      why: Correct. labels[0] = "blue"; labels.append("yellow")
  ✘ b: labels.append("blue"); labels[0] = "yellow"
      why: append adds at the end; this does not replace the first item with blue.
  ✘ c: labels[1] = "blue"; labels.append("yellow")
      why: Index 1 identifies the second item, not the first.
  feedback✔: Correct. labels[0] = "blue"; labels.append("yellow")  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: A:replace_item_at_index(f4); A:append_item_to_list(f5)   anchors=['assessment:replace_item_at_index', 'assessment:append_item_to_list']
  taught-before-tested: A.f4←s01; A.f5←s01

### s04 · hands_on · Practice lists
Practice — Create labels with the values "red", "blue", and "green" in that order, append "yellow", and assign labels[1:3] to a variable named selected_labels.
QUESTION [code_exercise, intro, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_selected_labels to selected_labels. The checker reads selected_labels.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'string literals', 'integer literals', 'list literals [item1, item2, ...]', 'list indexing with nonnegative and negative indices', 'list slicing with [start:stop]', 'indexed assignment with items[index] = value', 'items.append(value)'] blocked=8 items
  file main.py [editable]:
new_label = "yellow"
labels = ["red", "blue", "green"]
labels.append(new_label)
computed_selected_labels = labels[1:3]

  SOLUTION main.py:
new_label = "yellow"
labels = ["red", "blue", "green"]
labels.append(new_label)
computed_selected_labels = labels[1:3]
selected_labels = computed_selected_labels

  test t0 (value_equals, visible=True): {"expr":"[labels, selected_labels]","expected":[["red","blue","green","yellow"],["blue","green"]]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"1ce4fd80f0aba3df10d173e55371231457d7621cd55bce38643ee4b1fc826b52","tests_passed":1}
  feedback✔: The result meets the task. labels contains ["red", "blue", "green", "yellow"], and selected_labels contains ["blue", "green"].  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Trace the ordered labels, the appended new_label, and the slice whose stop index is excluded. Bind the resulting list to selected_labels.']
  MEASURES: A:create_ordered_mutable_list(f1); A:append_item_to_list(f5)   anchors=['practice', 'assessment:create_ordered_mutable_list']
  taught-before-tested: A.f1←s01; A.f5←s01

### s05 · explainer · Sets
(intro) Collect distinct color labels rather than repeated occurrences. ⟦B:tb1⟧
(definition) A set is unordered and contains distinct elements. set(items) constructs it, removing repeated values. ⟦B.f1 B:tb2⟧
(mechanism) {item1, item2, ...} makes a nonempty set. set() makes an empty set; {} makes a dictionary. ⟦B.f2 B:tb3⟧
(mechanism) value in values tests membership in a set. ⟦B.f3 B:tb3⟧
(mechanism) a | b is union: elements in either set. a & b is intersection: elements in both. ⟦B.f4 B:tb3⟧
(example) Compare the label sets by membership, not display order. Repeated source labels contribute one distinct element. Union combines membership from either set; intersection keeps only shared members. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧
(misconception) set() is an empty set, whereas {} is a dictionary. Sets do not provide stable first and second sequence positions. ⟦B.f1 B.f2 B:tb5⟧
[CODE python]
first = set(["red", "blue", "red"])
print(first)
second = {"blue", "green"}
print("red" in first)
print(first | second)
print(first & second)
empty = set()
  annotations: ['Repeated source labels contribute one distinct element.', 'The resulting set contains red and blue once each. Their displayed order is not a stable sequence order.', 'Union includes members from either set.', 'Intersection includes members shared by both sets.']

### s06 · check · Check sets
Quick check — Decide which distinct labels remain when the source list becomes a set.
QUESTION [choice, core, grading=client] What happens to repeated red entries when first = set(["red", "blue", "red"])?
  ✔ a: The set retains unique labels only.
      why: Correct. The set retains unique labels only.
  ✘ b: The set keeps both red entries in their original positions.
      why: Sets store unique elements and do not provide positional sequence traversal.
  ✘ c: The repeated red label is entirely removed.
      why: Deduplication keeps one occurrence as an element, rather than removing the label altogether.
  feedback✔: Correct. The set retains unique labels only.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r04
  MEASURES: B:create_sets_for_unique_values(f1,f2)   anchors=['assessment:create_sets_for_unique_values']
  taught-before-tested: B.f1←s05; B.f2←s05

### s07 · hands_on · Practice sets
Practice — Convert the list assigned to first into a set to remove repeated labels, then test whether "red" belongs to first.
QUESTION [code_exercise, core, grading=client] Insert first = set(first) before the supplied membership, union and intersection calculations. Keep those calculations unchanged. Then assign computed_member to member, computed_combined to combined and computed_shared to shared.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'list literals', 'nonempty set literals', 'set(items)', 'set()', 'value in values', 'a | b', 'a & b'] blocked=16 items
  file main.py [editable]:
first = ["red", "blue", "red"]
label = "red"
second = {"blue", "green"}
computed_member = label in first
computed_combined = first | second
computed_shared = first & second

  SOLUTION main.py:
first = ["red", "blue", "red"]
label = "red"
second = {"blue", "green"}
first = set(first)
computed_member = label in first
computed_combined = first | second
computed_shared = first & second
member = computed_member
combined = computed_combined
shared = computed_shared

  test t0 (value_equals, visible=True): {"expr":"[sorted(first), member, sorted(combined), sorted(shared)]","expected":[["blue","red"],true,["blue","green","red"],["blue"]]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e7ff9df6266be40040435dc96ccd612efad91a22acccc76e9641945ede6509c2","tests_passed":1}
  feedback✔: The result meets the task. first contains exactly "red" and "blue", with no repeated elements, and the membership expression evaluates to True.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Convert first before the set operations. Then distinguish membership, union of either set’s elements, and intersection of shared elements when binding the outputs.']
  MEASURES: B:test_set_membership(f3); B:compute_set_union_and_intersection(f4)   anchors=['practice', 'assessment:test_set_membership', 'assessment:compute_set_union_and_intersection']
  taught-before-tested: B.f3←s05; B.f4←s05

### s08 · explainer · Dictionaries
(intro) Retrieve a quantity using its product label as the key. ⟦C:tb1⟧
(definition) {key: value, ...} creates a dictionary of key-value pairs with unique keys. ⟦C.f1 C:tb2⟧
(mechanism) mapping[key] retrieves the associated value. If the key is absent, lookup raises an error. ⟦C.f2 C:tb3⟧
(mechanism) mapping[key] = value adds a new pair or replaces the existing key’s value. ⟦C.f3 C:tb3⟧
(example) Follow the notebook key through its replacement, then distinguish adding the pencil key from updating notebook. An eraser lookup would fail because that key has not been added. ⟦C.f1 C.f2 C.f3 C:tb4⟧
(misconception) Updating notebook replaces its value; it does not create a duplicate key. An absent-key bracket lookup raises an error, not a fallback value. ⟦C.f1 C.f2 C.f3 C:tb5⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
print(quantities["notebook"])
quantities["notebook"] = 5
quantities["pencil"] = 4
print(quantities["notebook"])
  annotations: ['Replace the value associated with an existing key.', 'Add a pair under a new key.']

### s09 · check · Check dictionaries
Quick check — Decide how dictionary key lookup retrieves a product value or encounters an absent key.
QUESTION [choice, core, grading=client] A quantities dictionary has notebook and pen keys. Which lookup retrieves the notebook value, and what happens for an absent key?
  ✔ a: quantities["notebook"] retrieves it; an absent key raises an error.
      why: quantities["notebook"] retrieves it; an absent key raises an error.
  ✘ b: quantities[0] retrieves the first product and absent keys return zero.
      why: Dictionary lookup uses keys, not sequence positions, and missing keys do not default to zero.
  ✘ c: quantities["notebook"] retrieves it; absent keys are added automatically.
      why: A missing-key lookup raises an error rather than inserting an entry.
  feedback✔: quantities["notebook"] retrieves it; an absent key raises an error.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r06
  MEASURES: C:retrieve_value_by_key_and_recognize_absent_key_error(f2)   anchors=['assessment:retrieve_value_by_key_and_recognize_absent_key_error']
  taught-before-tested: C.f2←s08

### s10 · check · Check dictionaries
Quick check — Decide whether each dictionary assignment adds a key or replaces its value.
QUESTION [choice, core, grading=client] For an existing notebook key, what does quantities["notebook"] = 5 do?
  ✔ a: It replaces the value associated with notebook.
      why: Correct. It replaces the value associated with notebook.
  ✘ b: It adds a second notebook key beside the first.
      why: Dictionary keys are unique; assigning an existing key replaces its associated value.
  ✘ c: It changes every product value to 5.
      why: Subscription assignment targets the named key, not every key.
  feedback✔: Correct. It replaces the value associated with notebook.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: C:add_and_replace_dictionary_values_by_key(f3)   anchors=['assessment:add_and_replace_dictionary_values_by_key']
  taught-before-tested: C.f3←s08

### s11 · hands_on · Practice dictionaries
Practice — Build a dictionary mapping notebook and pen to prices of 3 and 2, then retrieve the notebook price using bracket lookup.
QUESTION [code_exercise, intro, grading=client] Keep the supplied dictionary construction and inputs unchanged. Assign quantities[product_key] to price.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['Variable assignment with =', 'String literals for product keys', 'Integer literals for prices', 'Dictionary literals using {key: value, ...}', 'Dictionary lookup using mapping[key]', 'Dictionary insertion or replacement using mapping[key] = value'] blocked=15 items
  file main.py [editable]:
notebook_price = 3
pen_price = 2
product_key = "notebook"
quantities = {"notebook": notebook_price, "pen": pen_price}

  SOLUTION main.py:
notebook_price = 3
pen_price = 2
product_key = "notebook"
quantities = {"notebook": notebook_price, "pen": pen_price}
price = quantities[product_key]

  test t0 (value_equals, visible=True): {"expr":"[quantities, price]","expected":[{"notebook":3,"pen":2},3]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ecec87cf605d3c25a5ad4273452bb8c838874bdd7929502ccb0aa7ad334183d1","tests_passed":1}
  feedback✔: The result meets the task. The dictionary associates notebook with 3 and pen with 2, and the notebook lookup retrieves 3.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['The dictionary is already constructed. Use product_key as a key—not a sequence position—to retrieve the value assigned to price.']
  MEASURES: C:create_dictionary_with_unique_product_keys(f1)   anchors=['practice', 'assessment:create_dictionary_with_unique_product_keys']
  taught-before-tested: C.f1←s08

### s12 · recap · Takeaways
(takeaway) Lists support positional access, replacement, slicing and append. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(takeaway) Sets represent distinct membership, not sequence positions. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3⟧
(takeaway) Dictionary lookup and updates operate on unique keys. ⟦C.f1 C.f2 C.f3 C:tb2 C:tb3⟧
[UP NEXT] String Basics Formatting: Build a readable notebook-cost message from text and values.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit lists
(definition) [item1, item2, ...] creates a list: an ordered collection that can change. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) items[0] selects the first item. Negative indices count from the end. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(definition) items[start:stop] returns a new list from start up to, but excluding, stop. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A slice excludes its stop position and returns a new list; it is not a single-index lookup. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
labels = ["red", "blue", "green"]
print(labels[0])
print(labels[-1])
labels[1] = "navy"
labels.append("yellow")
print(labels[1:3])
print(labels)
  annotations: []
### r02 · Revisit lists
(definition) items[index] = value replaces the item at that position. ⟦A.f4 A:tb1 A:tb3 A:tb4⟧
(definition) items.append(value) adds a value at the list’s end. ⟦A.f5 A:tb3 A:tb4⟧
(misconception) Replacement changes an existing position; append adds at the end. ⟦A.f4 A:tb1 A:tb3 A:tb4⟧
[CODE python]
labels = ["red", "blue", "green"]
print(labels[0])
print(labels[-1])
labels[1] = "navy"
labels.append("yellow")
print(labels[1:3])
print(labels)
  annotations: []
### r03 · Revisit lists
(definition) [item1, item2, ...] creates a list: an ordered collection that can change. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) items[0] selects the first item. Negative indices count from the end. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(definition) items[start:stop] returns a new list from start up to, but excluding, stop. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(definition) items[index] = value replaces the item at that position. ⟦A.f4 A:tb1 A:tb3 A:tb4⟧
(definition) items.append(value) adds a value at the list’s end. ⟦A.f5 A:tb3 A:tb4⟧
(misconception) A slice excludes its stop position and returns a new list; it is not a single-index lookup. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
labels = ["red", "blue", "green"]
print(labels[0])
print(labels[-1])
labels[1] = "navy"
labels.append("yellow")
print(labels[1:3])
print(labels)
  annotations: []
### r04 · Revisit sets
(definition) A set is unordered and contains distinct elements. set(items) constructs it, removing repeated values. ⟦B.f1 B:tb1 B:tb2 B:tb4 B:tb5⟧
(definition) {item1, item2, ...} makes a nonempty set. set() makes an empty set; {} makes a dictionary. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) set() creates an empty set; empty braces create a dictionary. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
[CODE python]
first = set(["red", "blue", "red"])
second = {"blue", "green"}
print("red" in first)
print(first | second)
print(first & second)
empty = set()
  annotations: []
### r05 · Revisit sets
(definition) value in values tests membership in a set. ⟦B.f3 B:tb3 B:tb4⟧
(definition) a | b is union: elements in either set. a & b is intersection: elements in both. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) Union includes labels in either set; intersection requires membership in both. ⟦B.f4 B:tb3 B:tb4⟧
[CODE python]
first = set(["red", "blue", "red"])
second = {"blue", "green"}
print("red" in first)
print(first | second)
print(first & second)
empty = set()
  annotations: []
### r06 · Revisit dictionaries
(definition) {key: value, ...} creates a dictionary of key-value pairs with unique keys. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) mapping[key] retrieves the associated value. If the key is absent, lookup raises an error. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(misconception) An absent-key lookup raises an error rather than providing a fallback value. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
print(quantities["notebook"])
quantities["notebook"] = 5
quantities["pencil"] = 4
print(quantities["notebook"])
  annotations: []
### r07 · Revisit dictionaries
(definition) mapping[key] = value adds a new pair or replaces the existing key’s value. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) Updating notebook replaces its value; adding pencil creates a new key-value pair. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
print(quantities["notebook"])
quantities["notebook"] = 5
quantities["pencil"] = 4
print(quantities["notebook"])
  annotations: []
### r08 · Revisit dictionaries
(definition) {key: value, ...} creates a dictionary of key-value pairs with unique keys. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(definition) mapping[key] retrieves the associated value. If the key is absent, lookup raises an error. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
(definition) mapping[key] = value adds a new pair or replaces the existing key’s value. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(misconception) An absent-key lookup raises an error rather than providing a fallback value. ⟦C.f2 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
print(quantities["notebook"])
quantities["notebook"] = 5
quantities["pencil"] = 4
print(quantities["notebook"])
  annotations: []

=========

# EVALUATOR PACKET — String Basics Formatting (learn_python.tile.011_011)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.string_basics_formatting — String Basics Formatting

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.011_011.r02 is never referenced
  warn: learn_python.tile.011_011.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.011_011.s03/ix.learn_python.tile.011_011.s03: ADVISORY — syntax descriptors with no detector: ['class', 'colon followed by .2f inside f-string braces', 'comprehensions', 'except', 'expressions inside f-string braces', 'f-string prefix f', 'finally', 'for', 'from', 'import', 'integer and float literals', 'multiplication with *', 'raise', 'single-quoted and double-quoted string literals', 'string method calls', 'try', 'variable assignment with =', 'variable references', 'while', 'with', 'yield']

## SOURCE FACTS — A (python.string_basics_formatting)   objective: Create string literals and format values into readable strings using f-strings.
A.f1: Strings represent text, and single or double quotes delimit string literals.   [sources: python_tutorial#introduction.html#text]
A.f2: Prefix a string literal with f and place expressions inside braces to insert their values: f"{expression}".   [sources: python_tutorial#inputoutput.html#formatted-string-literals]
A.f3: A format specification after a colon controls presentation; f"{value:.2f}" displays a number in fixed-point form with two digits after the decimal point.   [sources: python_tutorial#inputoutput.html#formatted-string-literals]
note: Begin with this objective: Create string literals and format values into readable strings using f-strings.
note: Keep the example in the Readable string formatting tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.defining_calling_functions, python.parameters_arguments, python.return_values.
PRACTICE ANCHOR (live_code): Compute a total from quantity and cost, then assign an f-string sentence to message with the total formatted to two decimal places.  SUCCESS: With quantity = 3 and cost = 13.5, message contains the sentence "The total is 40.50." and uses an f-string with a .2f format specification.
ASSESSMENT ANCHOR: write_f_string_combining_literal_text_and_variable_values facts=['f1', 'f2']
ASSESSMENT ANCHOR: format_numeric_value_to_two_decimal_places_in_f_string facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Choosing a built-in collection; Comprehensions; Defining Calling Functions; Enumerate iteration; Error Handling; File Io; Floating-point approximation limits; For Loops; Function Default Keyword Args; Import Statements; Indentation and code blocks; Iterating Collections; Loop Control; Nested loops; PEP 8 Style; Parameters Arguments; Reading and displaying console values; Return Values; Running Python scripts; Statements and expressions; Tuples; Using math for numeric calculations; Using range for counted iteration; Variable Scope

## LESSON, in learner order

### s01 · explainer · String Basics Formatting
(intro) Build a readable notebook-cost message from text and values. ⟦A:tb1⟧
(definition) Strings represent text; single or double quotes delimit their literals. ⟦A.f1 A:tb2⟧
(mechanism) Prefix a literal with f and put expressions inside braces to insert their values: f"{expression}". ⟦A.f2 A:tb3⟧
(mechanism) A colon introduces a presentation specification. f"{value:.2f}" displays fixed-point form with two digits after the decimal point. ⟦A.f3 A:tb3⟧
(example) Separate the f prefix, literal text, braced expression and colon-led format specification. The expression supplies a value; .2f controls how that value appears in the message. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) Two decimal digits describe the formatted text. Formatting does not change the underlying numeric calculation. ⟦A.f3 A:tb5⟧
[CODE python]
quantity = 3
cost = 13.5
message = f"The total is {quantity * cost:.2f}."
print(message)
  annotations: ['f enables insertion; braces hold the expression; :.2f sets fixed-point presentation.']

### s02 · check · Check string basics formatting
Quick check — Decide which f-string combines the supplied literal text and variable values.
QUESTION [choice, intro, grading=client] Which literal inserts quantity into the surrounding sentence?
  ✔ a: f"Quantity: {quantity}"
      why: Correct. f"Quantity: {quantity}"
  ✘ b: "Quantity: {quantity}"
      why: Without the f prefix, braces and the name remain literal text.
  ✘ c: f"Quantity: quantity"
      why: Without braces, quantity is literal text rather than an inserted expression.
  feedback✔: Correct. f"Quantity: {quantity}"  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:write_f_string_combining_literal_text_and_variable_values(f1,f2)   anchors=['assessment:write_f_string_combining_literal_text_and_variable_values']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · hands_on · Practice string basics formatting
Practice — Compute a total from quantity and cost, then assign an f-string sentence to message with the total formatted to two decimal places.
QUESTION [code_exercise, intro, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_message to message. The checker reads message.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'integer and float literals', 'single-quoted and double-quoted string literals', 'variable references', 'multiplication with *', 'f-string prefix f', 'expressions inside f-string braces', 'colon followed by .2f inside f-string braces'] blocked=20 items
  file main.py [editable]:
quantity = 3
cost = 13.5
computed_message = f"The total is {quantity * cost:.2f}."

  SOLUTION main.py:
quantity = 3
cost = 13.5
computed_message = f"The total is {quantity * cost:.2f}."
message = computed_message

  test t0 (value_equals, visible=True): {"expr":"message","expected":"The total is 40.50."} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"778eab8f937ecc616b90056533d9f3ca0a8e4541d8132d43705977cbafe0d30f","tests_passed":1}
  feedback✔: The result meets the task. With quantity = 3 and cost = 13.5, message contains the sentence "The total is 40.50." and uses an f-string with a .2f format specification.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Inspect the f prefix, braced product and :.2f specification before binding computed_message to message.']
  MEASURES: A:format_numeric_value_to_two_decimal_places_in_f_string(f2,f3)   anchors=['practice', 'assessment:format_numeric_value_to_two_decimal_places_in_f_string']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · recap · Takeaways
(takeaway) F-strings insert expression values; format specifications control presentation. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3⟧
[UP NEXT] Defining Calling Functions: Name the greeting action, then choose when to call it.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit string basics formatting
(definition) Strings represent text; single or double quotes delimit their literals. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Prefix a literal with f and put expressions inside braces to insert their values: f"{expression}". ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Braced expressions insert their values; the surrounding literal text supplies the message wording. ⟦A.f2 A:tb3 A:tb4⟧
[CODE python]
quantity = 3
cost = 13.5
message = f"Quantity: {quantity}; cost: {cost:.2f}"
print(message)
  annotations: []
### r02 · Revisit string basics formatting
(definition) Prefix a literal with f and put expressions inside braces to insert their values: f"{expression}". ⟦A.f2 A:tb3 A:tb4⟧
(definition) A colon introduces a presentation specification. f"{value:.2f}" displays fixed-point form with two digits after the decimal point. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Braced expressions insert their values; the surrounding literal text supplies the message wording. ⟦A.f2 A:tb3 A:tb4⟧
[CODE python]
quantity = 3
cost = 13.5
message = f"Quantity: {quantity}; cost: {cost:.2f}"
print(message)
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· expected.value: The total is 135.00.

=========

# EVALUATOR PACKET — Defining Calling Functions / Parameters Arguments / Return Values (learn_python.tile.012_014)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.defining_calling_functions — Defining Calling Functions
B = python.parameters_arguments — Parameters Arguments
C = python.return_values — Return Values

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=10
  warn: remediation step learn_python.tile.012_014.r02 is never referenced
  warn: remediation step learn_python.tile.012_014.r04 is never referenced
  warn: remediation step learn_python.tile.012_014.r06 is never referenced
  warn: learn_python.tile.012_014.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.012_014.s03/ix.learn_python.tile.012_014.s03: ADVISORY — syntax descriptors with no detector: ['An indented function body', 'Calls with arguments', 'Decorators', 'Function parameters', 'String literals', 'Variable assignment', 'for', 'global', 'import', 'nonlocal', 'yield']
  warn: learn_python.tile.012_014.s04: prose block without lineage.fact_ids
  warn: learn_python.tile.012_014.s06/ix.learn_python.tile.012_014.s06: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'Comprehensions', 'Indented function body', 'Integer literals', 'Keyword arguments', 'String concatenation with +', 'String literals', 'Tuple expressions', 'Variable assignment', 'assert', 'class', 'for', 'global', 'import', 'nonlocal', 'raise', 'try']
  warn: learn_python.tile.012_014.s07: prose block without lineage.fact_ids
  warn: learn_python.tile.012_014.s10/ix.learn_python.tile.012_014.s10: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'Comprehensions', 'Function calls with positional arguments', 'Indented function body', 'Integer and float literals', 'Keyword arguments', 'Multiplication with *', 'Tuple expressions', 'Variable assignment with =', 'assert', 'class', 'for', 'global', 'import', 'is None', 'nonlocal', 'return quantity * price', 'try/except', 'yield']
  warn: plan: learn_python.tile.012_014.s10 was planned to measure python.return_values#assessment:identify_stored_results_of_returning_and_display_only_functions but its interaction does not

## SOURCE FACTS — A (python.defining_calling_functions)   objective: Define a Python function and call it by name.
A.f1: Define a function with def name(): followed by an indented body.   [sources: python_tutorial#controlflow.html#defining-functions]
A.f2: A function definition binds its name to a function; name() calls it and executes its body.   [sources: python_tutorial#controlflow.html#defining-functions]
note: Begin with this objective: Define a Python function and call it by name.
note: Keep the example in the Defining and using functions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.parameters_arguments, python.return_values, python.tuples.
PRACTICE ANCHOR (live_code): Create a reusable helper named greet with an empty pair of parentheses and an indented body, then call it twice.  SUCCESS: The definition uses def greet(): with an indented body. Two separate greet() calls appear after the definition, outside its body, and each executes the body.
ASSESSMENT ANCHOR: recognize_function_definition facts=['f1']
ASSESSMENT ANCHOR: distinguish_definition_from_call facts=['f2']
ASSESSMENT ANCHOR: invoke_function_by_name facts=['f2']

## SOURCE FACTS — B (python.parameters_arguments)   objective: Pass values into functions through parameters and arguments.
B.f1: Parameters are names listed in a function definition; arguments are the values supplied at a call.   [sources: python_tutorial#controlflow.html#defining-functions]
B.f2: Define def name(parameter): with an indented body using parameter, then call name(argument) to supply that value.   [sources: python_tutorial#controlflow.html#defining-functions]
B.f3: Positional arguments bind to the corresponding parameters in order.   [sources: python_tutorial#controlflow.html#defining-functions]
note: Begin with this objective: Pass values into functions through parameters and arguments.
note: Keep the example in the Defining and using functions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.return_values, python.tuples, python.function_default_keyword_args.
PRACTICE ANCHOR (live_code): Parameterize a describe helper so its body builds a label from supplied label and quantity values rather than hard-coded values.  SUCCESS: The helper defines label and quantity as parameters, uses both in its body, and is called with the positional arguments "notebook", 3 and "pen", 2 in the correct order.
ASSESSMENT ANCHOR: match_positional_arguments_to_parameters facts=['f1', 'f3']
ASSESSMENT ANCHOR: distinguish_definition_parameters_from_call_arguments facts=['f1', 'f2']

## SOURCE FACTS — C (python.return_values)   objective: Return a computed value from a function for later reuse.
C.f1: return expression ends the current function call and supplies that expression’s value to the caller.   [sources: python_tutorial#controlflow.html#defining-functions]
C.f2: Use result = function(arguments) to store a returned value.   [sources: python_tutorial#controlflow.html#defining-functions]
C.f3: A function that reaches its end without return, or uses return without an expression, returns None.   [sources: python_tutorial#controlflow.html#defining-functions]
C.f4: print displays values rather than supplying them as the function’s calculated return result.   [sources: python_stdlib_reference#functions.html#print]
note: Begin with this objective: Return a computed value from a function for later reuse.
note: Keep the example in the Defining and using functions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.tuples, python.function_default_keyword_args, python.variable_scope.
PRACTICE ANCHOR (live_code): Make order_cost return quantity multiplied by price, then store the result of order_cost(3, 4.5) in cost.  SUCCESS: The function returns the calculated product, and cost holds 13.5 after the call without requiring any display instruction.
ASSESSMENT ANCHOR: distinguish_returned_values_from_displayed_values facts=['f1', 'f4']
ASSESSMENT ANCHOR: identify_stored_results_of_returning_and_display_only_functions facts=['f2', 'f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Choosing a built-in collection; Comprehensions; Enumerate iteration; Error Handling; File Io; Floating-point approximation limits; For Loops; Function Default Keyword Args; Import Statements; Indentation and code blocks; Iterating Collections; Loop Control; Nested loops; PEP 8 Style; Parameters Arguments; Python comments; Python interpreter execution model; Reading and displaying console values; Return Values; Running Python interactively; Running Python scripts; Statements and expressions; Tuples; Using math for numeric calculations; Using range for counted iteration; Variable Scope

## LESSON, in learner order

### s01 · explainer · Defining Calling Functions
(intro) Name the greeting action, then choose when to call it. ⟦A:tb1⟧
(definition) Define a function with def name(): and an indented body. ⟦A.f1 A:tb2⟧
(mechanism) The definition binds its name to a function. name() calls the function and executes its body. ⟦A.f2 A:tb3⟧
(example) The greeting definition makes the function available. Each call outside the indented body asks that body to execute; the definition itself is not a call. ⟦A.f1 A.f2 A:tb4⟧
(misconception) def greet(): binds the function name; greet() invokes the body. Defining and calling are different actions. ⟦A.f2 A:tb5⟧
[CODE python]
def greet():
    print("Hello")

greet()
greet()
  annotations: ['Define and bind the function name.', 'This indented body executes when the function is called.', 'A call outside the body invokes the function.', 'A call outside the body invokes the function.']

### s02 · check · Check defining calling functions
Quick check — Decide which expression calls the defined helper by name.
QUESTION [choice, intro, grading=client] After defining greet, which statement invokes its body?
  ✔ a: greet()
      why: Correct. greet()
  ✘ b: greet
      why: Naming the function without call parentheses does not invoke it.
  ✘ c: def greet():
      why: def introduces the definition, rather than calling an already defined function.
  feedback✔: Correct. greet()  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:invoke_function_by_name(f2)   anchors=['assessment:invoke_function_by_name']
  taught-before-tested: A.f2←s01

### s03 · hands_on · Practice defining calling functions
Practice — Create a reusable helper named greet with an empty pair of parentheses and an indented body, then call it twice.
QUESTION [code_exercise, intro, grading=client] The supplied function definition defines greet with an indented body that uses greeting. Keep it unchanged. Add two separate greet() calls after the function definition, outside the function body. The checker observes both executions and their local message values.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def greet():', 'An indented function body', 'String literals', 'Variable assignment', 'greet()'] blocked=12 items
  file main.py [editable]:
greeting = "Hello"
if True:
    def greet():
        message = greeting


  SOLUTION main.py:
greeting = "Hello"
if True:
    def greet():
        message = greeting
greet()
greet()

  test t0 (value_equals, visible=True): {"expr":"(lambda scope: (exec('import sys\\n_capture = []\\ndef _observer(frame, event, arg):\\n    if frame.f_code.co_name == \\'greet\\' and event == \"return\":\\n        _capture.append(frame.f_locals.copy())\\n    return _observer\\nsys.settrace(_observer)\\ngreet()\\ngreet()\\nsys.settrace(None)\\nimport ast\\n_tree = ast.parse(open(\"main.py\").read())\\n_calls = [n for n in _tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and  | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"1fcaa48f0f548b76c565a95ec7c5ce87450289f179df0eff07c81085a9f4828f","tests_passed":1}
  feedback✔: The result meets the task. The definition uses def greet(): with an indented body. Two separate greet() calls appear after the definition, outside its body, and each executes the body.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Check the exact operations and result names requested in the prompt.']
  MEASURES: A:recognize_function_definition(f1); A:distinguish_definition_from_call(f2)   anchors=['practice', 'assessment:recognize_function_definition', 'assessment:distinguish_definition_from_call']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · explainer · Parameters Arguments
(intro) Reuse describe with different notebook and pen call values. ⟦B:tb1⟧
(definition) Parameters are names in a function definition. Arguments are values supplied at a call. ⟦B.f1 B:tb2⟧
(mechanism) Define def name(parameter): with an indented body using parameter; call name(argument) to supply a value. ⟦B.f2 B:tb3⟧
(mechanism) Positional arguments bind to the corresponding parameters in order. ⟦B.f3 B:tb3⟧
(example) In describe, label and quantity are parameter names. For each call, connect the first argument to label and the second to quantity before reading the body. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) label is a parameter name, not one particular product label. Each call supplies arguments that bind in positional order. ⟦B.f1 B.f3 B:tb5⟧
[CODE python]
def describe(label, quantity):
    print(label, quantity)

describe("notebook", 3)
describe("pen", 2)
  annotations: ['label and quantity are parameters.', 'The first argument binds label; the second binds quantity.', 'The first argument binds label; the second binds quantity.']

### s05 · check · Check parameters arguments
Quick check — Identify the parameters in the definition and the arguments supplied by the call.
QUESTION [choice, core, grading=client] In def describe(label, quantity): followed by describe("pen", 2), which are the parameters?
  ✔ a: label and quantity; the arguments are pen and 2.
      why: Correct. label and quantity; the arguments are pen and 2.
  ✘ b: pen and 2; the arguments are label and quantity.
      why: Parameters are the names in the definition, not the values at the call.
  ✘ c: Only quantity is a parameter; pen binds to it first.
      why: Both definition names are parameters, and positional arguments bind in the listed order.
  feedback✔: Correct. label and quantity; the arguments are pen and 2.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r03
  MEASURES: B:distinguish_definition_parameters_from_call_arguments(f1,f2)   anchors=['assessment:distinguish_definition_parameters_from_call_arguments']
  taught-before-tested: B.f1←s04; B.f2←s04

### s06 · hands_on · Practice parameters arguments
Practice — Parameterize a describe helper so its body builds a label from supplied label and quantity values rather than hard-coded values.
QUESTION [code_exercise, intro, grading=client] The supplied function definition defines describe(label, quantity) and uses both parameters in its body. Keep it unchanged. Add describe("notebook", 3), then describe("pen", 2), as two separate calls in that order. The checker observes the argument order and the local label values after execution.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def describe(label, quantity):', 'Indented function body', 'Variable assignment', 'String literals', 'Integer literals', 'String concatenation with +', 'str(quantity)', 'describe("notebook", 3)', 'describe("pen", 2)'] blocked=20 items
  file main.py [editable]:
separator = ": "
if True:
    def describe(label, quantity):
        label = label + separator + str(quantity)


  SOLUTION main.py:
separator = ": "
if True:
    def describe(label, quantity):
        label = label + separator + str(quantity)
describe("notebook", 3)
describe("pen", 2)

  test t0 (value_equals, visible=True): {"expr":"(lambda scope: (exec('import sys\\n_capture = []\\ndef _observer(frame, event, arg):\\n    if frame.f_code.co_name == \\'describe\\' and event == \"return\":\\n        _capture.append(frame.f_locals.copy())\\n    return _observer\\nsys.settrace(_observer)\\ndescribe(\"notebook\", 3)\\ndescribe(\"pen\", 2)\\nsys.settrace(None)\\nimport ast\\n_tree = ast.parse(open(\"main.py\").read())\\n_calls = [n for n in _tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isins | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f3a084980dcb780ec4483c14b0e8a78e51d66081a5236b17d06abc735f2a4a91","tests_passed":1}
  feedback✔: The result meets the task. The helper defines label and quantity as parameters, uses both in its body, and is called with the positional arguments "notebook", 3 and "pen", 2 in the correct order.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Check the exact operations and result names requested in the prompt.']
  MEASURES: B:match_positional_arguments_to_parameters(f1,f3); B:distinguish_definition_parameters_from_call_arguments(f1,f2)   anchors=['practice', 'assessment:match_positional_arguments_to_parameters', 'assessment:distinguish_definition_parameters_from_call_arguments']
  taught-before-tested: B.f1←s04; B.f3←s04; B.f1←s04; B.f2←s04

### s07 · explainer · Return Values
(intro) Give the caller an order cost it can use again. ⟦C:tb1⟧
(definition) return expression ends the current call and supplies the expression’s value to the caller. ⟦C.f1 C:tb2⟧
(mechanism) result = function(arguments) stores the returned value. ⟦C.f2 C:tb3⟧
(mechanism) Reaching the function’s end without return, or using return with no expression, returns None. ⟦C.f3 C:tb3⟧
(mechanism) print displays values; it does not supply the function’s calculated return result. ⟦C.f4 C:tb3⟧
(example) Trace the product through return into cost, then into the caller’s addition. Contrast that with a helper that only prints the product: displaying it does not return it. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4⟧
(misconception) A display-only helper reaches its end and returns None. A missing return does not return the last calculation. ⟦C.f3 C.f4 C:tb5⟧
[CODE python]
def order_cost(quantity, price):
    return quantity * price

cost = order_cost(3, 4.5)
print(cost + 2)
  annotations: ['End this call and supply the product to the caller.', 'Store the returned value in cost.', 'The caller can reuse the stored result.']
[CODE python]
def order_cost(quantity, price):
    print(quantity * price)
cost = order_cost(3, 4.5)
print(cost)
  annotations: []

### s08 · video · Explore return values
[VIDEO Return a value the caller can reuse] bridge-before: Watch how returning an area lets the caller store and reuse it, unlike displaying it. Notice why an instruction after return is never reached. | bridge-after: The clip connects returning, storing, and reusing values. It does not explain falling through or return without an expression; the text covers how both produce None.
  - AetGXMcNU3M 9-410s facts=['f1', 'f2', 'f4'] label: Return calculated areas, store them, and combine them | summary: An area function initially displays length multiplied by width. Although the apartment and yard areas appear on screen, those displayed numbers are not supplied as calculated results for the caller to combine. Changing the function to return length * width lets the caller store the results in house and yard, then add them to obtain 3,500 square feet. Return also stops the current function call: a display instruction placed after it is never reached. Moving that instruction before return allows the function to display the area and still supply its calculated value to the caller.

### s09 · check · Check return values
Quick check — Decide whether the helper returns a value or only displays one.
QUESTION [choice, core, grading=client] A helper displays a product with print but reaches its end without return. What does assigning its call to cost store?
  ✔ a: None, not the displayed product.
      why: Correct. None, not the displayed product.
  ✘ b: The displayed product.
      why: Displaying a value is not supplying the function’s calculated return value.
  ✘ c: The helper’s parameter values as a pair.
      why: No pair is returned automatically; reaching the end without return yields None.
  feedback✔: Correct. None, not the displayed product.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r05
  MEASURES: C:distinguish_returned_values_from_displayed_values(f1,f4); C:identify_stored_results_of_returning_and_display_only_functions(f2,f3,f4)   anchors=['assessment:distinguish_returned_values_from_displayed_values', 'assessment:identify_stored_results_of_returning_and_display_only_functions']
  taught-before-tested: C.f1←s07; C.f4←s07; C.f2←s07; C.f3←s07; C.f4←s07

### s10 · hands_on · Practice return values
Practice — Make order_cost return quantity multiplied by price, then store the result of order_cost(3, 4.5) in cost.
QUESTION [code_exercise, intro, grading=client] Keep the supplied function and inputs unchanged. Assign order_cost(quantity_input, price_input) to cost. Do not display output.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def order_cost(quantity, price):', 'Indented function body', 'return quantity * price', 'Function calls with positional arguments', 'Variable assignment with =', 'Multiplication with *', 'Integer and float literals'] blocked=20 items
  file main.py [editable]:
quantity_input = 3
price_input = 4.5
if True:
    def order_cost(quantity, price):
        return quantity * price


  SOLUTION main.py:
quantity_input = 3
price_input = 4.5
if True:
    def order_cost(quantity, price):
        return quantity * price
cost = order_cost(quantity_input, price_input)

  test t0 (value_equals, visible=True): {"expr":"cost","expected":13.5} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t1 (function_call, visible=True): {"function":"order_cost","args":[3,4.5],"kwargs":{},"expected":13.5} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t2 (function_call, visible=True): {"function":"order_cost","args":[2,4],"kwargs":{},"expected":8} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a44ddc651a102983b037e1cf2f9a70ac8baf95fccd99b39b526332e4187f4ecc","tests_passed":3}
  feedback✔: The result meets the task. The function returns the calculated product, and cost holds 13.5 after the call without requiring any display instruction.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Check the exact operations and result names requested in the prompt.']
  MEASURES: C:distinguish_returned_values_from_displayed_values(f1,f4)   anchors=['practice', 'assessment:distinguish_returned_values_from_displayed_values']
  taught-before-tested: C.f1←s07; C.f4←s07

### s11 · recap · Takeaways
(takeaway) A definition binds a function; a call executes its body. ⟦A.f1 A.f2 A:tb2 A:tb3⟧
(takeaway) Parameters name inputs; call arguments supply their values. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3⟧
(takeaway) Return supplies a reusable result; print only displays. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3⟧
[UP NEXT] Tuples: Return the smallest and largest quantities together as an ordered pair.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit defining calling functions
(definition) The definition binds its name to a function. name() calls the function and executes its body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) The definition binds greet; the later greet() calls execute its body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def greet():
    print("Hello")

greet()
greet()
  annotations: []
### r02 · Revisit defining calling functions
(definition) Define a function with def name(): and an indented body. ⟦A.f1 A:tb2 A:tb4⟧
(definition) The definition binds its name to a function. name() calls the function and executes its body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) The definition binds greet; the later greet() calls execute its body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def greet():
    print("Hello")

greet()
greet()
  annotations: []
### r03 · Revisit parameters arguments
(definition) Parameters are names in a function definition. Arguments are values supplied at a call. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Define def name(parameter): with an indented body using parameter; call name(argument) to supply a value. ⟦B.f2 B:tb3 B:tb4⟧
(misconception) label is a parameter name in describe; a product label supplied at a call is an argument. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
[CODE python]
def describe(label, quantity):
    print(label, quantity)

describe("notebook", 3)
describe("pen", 2)
  annotations: []
### r04 · Revisit parameters arguments
(definition) Parameters are names in a function definition. Arguments are values supplied at a call. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) Define def name(parameter): with an indented body using parameter; call name(argument) to supply a value. ⟦B.f2 B:tb3 B:tb4⟧
(definition) Positional arguments bind to the corresponding parameters in order. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) label is a parameter name in describe; a product label supplied at a call is an argument. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
[CODE python]
def describe(label, quantity):
    print(label, quantity)

describe("notebook", 3)
describe("pen", 2)
  annotations: []
### r05 · Revisit return values
(definition) return expression ends the current call and supplies the expression’s value to the caller. ⟦C.f1 C:tb2 C:tb4⟧
(definition) print displays values; it does not supply the function’s calculated return result. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Printing the product displays it; returning the product supplies it to the caller. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
[CODE python]
def order_cost(quantity, price):
    return quantity * price

cost = order_cost(3, 4.5)
print(cost + 2)
  annotations: []
### r06 · Revisit return values
(definition) result = function(arguments) stores the returned value. ⟦C.f2 C:tb3 C:tb4⟧
(definition) Reaching the function’s end without return, or using return with no expression, returns None. ⟦C.f3 C:tb3 C:tb4 C:tb5⟧
(definition) print displays values; it does not supply the function’s calculated return result. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Printing the product displays it; returning the product supplies it to the caller. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
[CODE python]
def order_cost(quantity, price):
    return quantity * price

cost = order_cost(3, 4.5)
print(cost + 2)
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expr: (lambda scope: (exec('import sys\n_capture = []\ndef _observer(frame, event, arg):\n    if frame.f_code.co_name == \'greet\' and event == "return":\n        _capture.append(frame.f_locals.copy())\n    return _observer\nsys.settrace(_observer)\ngreet()\ngreet()\nsys.settrace(None)\nimport ast\n_tree = ast.parse(open("main.py").read())\n_calls = [n for n in _tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id == \'greet\']\n_result = [[entry[\'message\'] for entry in _capture], len(_calls)]\n', scope), scope["_result"])[1])(globals().copy())
· constraints.blocked_syntax: Default parameter values
· spec.expr: (lambda scope: (exec('import sys\n_capture = []\ndef _observer(frame, event, arg):\n    if frame.f_code.co_name == \'describe\' and event == "return":\n        _capture.append(frame.f_locals.copy())\n    return _observer\nsys.settrace(_observer)\ndescribe("notebook", 3)\ndescribe("pen", 2)\nsys.settrace(None)\nimport ast\n_tree = ast.parse(open("main.py").read())\n_calls = [n for n in _tree.body if isinstance(n, ast.Expr) and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name) and n.value.func.id == \'describe\']\n_result = [[entry[\'label\'] for entry in _capture], len(_calls)]\n_result.append([[ast.literal_eval(a) for a in n.value.args] for n in _calls])\n', scope), scope["_result"])[1])(globals().copy())
· constraints.blocked_syntax: Default parameter values

=========

# EVALUATOR PACKET — Tuples / Function Default Keyword Args / Variable Scope (learn_python.tile.015_017)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.tuples — Tuples
B = python.function_default_keyword_args — Function Default Keyword Args
C = python.variable_scope — Variable Scope

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=12
  warn: remediation step learn_python.tile.015_017.r02 is never referenced
  warn: remediation step learn_python.tile.015_017.r03 is never referenced
  warn: remediation step learn_python.tile.015_017.r05 is never referenced
  warn: remediation step learn_python.tile.015_017.r07 is never referenced
  warn: remediation step learn_python.tile.015_017.r08 is never referenced
  warn: learn_python.tile.015_017.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.015_017.s04/ix.learn_python.tile.015_017.s04: ADVISORY — syntax descriptors with no detector: ['**kwargs', '*args', 'Generator expressions', 'Keyword arguments', 'List literals containing integers', 'List, set, and dictionary comprehensions', 'One-item tuple literals with a trailing comma', 'Parenthesized tuple literals', 'Starred unpacking targets', 'Variable assignment', 'assert', 'for ... in ...:', 'from ... import ...', 'import', 'raise', 'try / except']
  warn: learn_python.tile.015_017.s05: prose block without lineage.fact_ids
  warn: learn_python.tile.015_017.s07/ix.learn_python.tile.015_017.s07: ADVISORY — syntax descriptors with no detector: ['*args and **kwargs', 'argument unpacking with * or **', 'assert statements', 'class statements', 'for statements', 'global and nonlocal statements', 'integer literals', 'keyword function arguments', 'lambda expressions', 'omission of a defaulted argument', 'positional function arguments', 'return quantity * price + fee', 'try/except statements']
  warn: learn_python.tile.015_017.s08: prose block without lineage.fact_ids
  warn: learn_python.tile.015_017.s12/ix.learn_python.tile.015_017.s12: ADVISORY — syntax descriptors with no detector: ['addition with +', 'assert statements', 'break and continue', 'comprehensions', 'dictionary lookup with ["quantity"]', 'for loops', 'integer literals', 'lambda expressions', 'module-level and local assignment with =', 'nonlocal declarations', 'quantity', 'raise statements', 'try/except/finally', 'with statements', 'yield expressions']
  warn: plan: learn_python.tile.015_017.s12 was planned to measure python.variable_scope#assessment:identify_local_names_and_predict_unbound_reads but its interaction does not

## SOURCE FACTS — A (python.tuples)   objective: Create and use Python's core ordered, immutable data structure: the tuple.
A.f1: A tuple is an ordered group of values whose individual items cannot be reassigned.   [sources: python_tutorial#datastructures.html#tuples-and-sequences]
A.f2: Comma-separated values form a tuple; (value,) creates a one-item tuple.   [sources: python_tutorial#datastructures.html#tuples-and-sequences]
A.f3: Unpack a pair with first, second = pair; the number of targets must match the number of values.   [sources: python_tutorial#datastructures.html#tuples-and-sequences]
A.f4: return first, second returns a tuple containing the two expression values.   [sources: python_language_reference#simple_stmts.html#return]
A.f5: min(values) and max(values) obtain the smallest and largest items of a nonempty collection.   [sources: python_stdlib_reference#functions.html#min, python_stdlib_reference#functions.html#max]
note: Begin with this objective: Create and use Python's core ordered, immutable data structure: the tuple.
note: Keep the example in the Function results, defaults and scope tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.function_default_keyword_args, python.variable_scope, python.error_handling.
PRACTICE ANCHOR (live_code): Write bounds(values) to return a tuple containing the minimum and maximum of a nonempty list, then unpack the result into smallest and largest.  SUCCESS: Calling bounds([3, 8, 5]) returns (3, 8), and unpacking assigns 3 to smallest and 8 to largest in that order.
ASSESSMENT ANCHOR: construct_fixed_ordered_tuple facts=['f1', 'f2']
ASSESSMENT ANCHOR: unpack_tuple_with_matching_targets facts=['f3']
ASSESSMENT ANCHOR: return_and_unpack_minimum_maximum_pair facts=['f4', 'f5']

## SOURCE FACTS — B (python.function_default_keyword_args)   objective: Give function parameters default values and call functions using keyword argument syntax.
B.f1: Define a default with def name(required, optional=default):; omitting optional in a call uses its default value.   [sources: python_tutorial#controlflow.html#default-argument-values]
B.f2: Positional arguments bind in order and keyword arguments bind by parameter name; keyword arguments follow ordinary positional arguments.   [sources: python_tutorial#controlflow.html#keyword-arguments]
B.f3: A call must supply required arguments and must not bind one parameter twice or supply an unaccepted keyword.   [sources: python_tutorial#controlflow.html#keyword-arguments]
note: Begin with this objective: Give function parameters default values and call functions using keyword argument syntax.
note: Keep the example in the Function results, defaults and scope tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.variable_scope, python.error_handling, python.import_statements.
PRACTICE ANCHOR (live_code): Define cost(quantity, price, fee=2) to return quantity * price + fee. Call it once using only keyword arguments with fee=5, and once omitting fee to use its default. Assign each returned value to a variable.  SUCCESS: The keyword-only call cost(quantity=3, price=4, fee=5) returns 17, and cost(3, 4) returns 14. Both results are assigned to variables, with each required parameter supplied exactly once.
ASSESSMENT ANCHOR: omit_defaulted_arguments facts=['f1']
ASSESSMENT ANCHOR: combine_positional_and_keyword_arguments facts=['f2']
ASSESSMENT ANCHOR: recognize_invalid_argument_bindings facts=['f3']

## SOURCE FACTS — C (python.variable_scope)   objective: Understand how local and global scope determine where a variable name is visible and modifiable.
C.f1: A function’s assigned names are local throughout that function unless declared otherwise; reading a local name before binding it raises UnboundLocalError.   [sources: python_language_reference#executionmodel.html#resolution-of-names]
C.f2: Without a local binding, ordinary lookup can read an enclosing or module-level binding.   [sources: python_language_reference#executionmodel.html#resolution-of-names]
C.f3: globals() returns the current module namespace dictionary; globals()["name"] explicitly reads its entry even when an ordinary local name shadows it.   [sources: python_stdlib_reference#functions.html#globals]
C.f4: Assigning to an ordinary local name changes that local binding rather than a same-named module binding.   [sources: python_language_reference#simple_stmts.html#assignment-statements]
C.f5: A global declaration makes assignments to the declared name use its module-level binding instead.   [sources: python_language_reference#simple_stmts.html#global]
note: Begin with this objective: Understand how local and global scope determine where a variable name is visible and modifiable.
note: Keep the example in the Function results, defaults and scope tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.error_handling, python.import_statements, python.pep8_style.
PRACTICE ANCHOR (live_code): Write show() so it reads the module-level quantity through globals()["quantity"], assigns that value to a local quantity, increases the local quantity by 2, and returns it without changing the module-level quantity.  SUCCESS: With module-level quantity initially 3, show() returns 5 and the module-level quantity remains 3 after the call.
ASSESSMENT ANCHOR: identify_local_names_and_predict_unbound_reads facts=['f1']
ASSESSMENT ANCHOR: resolve_names_without_local_bindings facts=['f2']
ASSESSMENT ANCHOR: distinguish_explicit_module_lookup_from_local_lookup facts=['f3']
ASSESSMENT ANCHOR: predict_local_and_declared_global_assignment_effects facts=['f4', 'f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Choosing a built-in collection; Comprehensions; Continuing expressions across lines; Distinguishing syntax and runtime errors; Enumerate iteration; Error Handling; File Io; Floating-point approximation limits; For Loops; Function Default Keyword Args; Import Statements; Indentation and code blocks; Iterating Collections; Loop Control; Nested loops; PEP 8 Style; Python comments; Python interpreter execution model; Reading and displaying console values; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Using math for numeric calculations; Using range for counted iteration; Variable Scope

## LESSON, in learner order

### s01 · explainer · Tuples
(intro) Return the smallest and largest quantities together as an ordered pair. ⟦A:tb1⟧
(definition) A tuple is an ordered group whose individual items cannot be reassigned. ⟦A.f1 A:tb2⟧
(mechanism) Comma-separated values form a tuple; (value,) forms a one-item tuple. ⟦A.f2 A:tb3⟧
(mechanism) first, second = pair unpacks a pair. Target and value counts must match. ⟦A.f3 A:tb3⟧
(mechanism) return first, second returns a tuple of the two expression values. ⟦A.f4 A:tb3⟧
(mechanism) For a nonempty collection, min(values) obtains the smallest item and max(values) the largest. ⟦A.f5 A:tb3⟧
(example) Trace the first returned expression into smallest and the second into largest. Both targets match the pair’s two values. The separate one-item tuple needs its comma. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧
(misconception) Tuple items cannot be replaced like list items. Unpacking requires matching counts, and a one-item tuple requires the comma. ⟦A.f1 A.f2 A.f3 A:tb5⟧
[CODE python]
def bounds(values):
    return min(values), max(values)

smallest, largest = bounds([3, 8, 5])
print(smallest, largest)
one_item = (3,)
  annotations: ['The first expression supplies the lower bound; the second the upper bound.', 'Unpack the returned pair into the corresponding two names.', 'The comma forms a one-item tuple.']

### s02 · check · Check tuples
Quick check — Decide which expression constructs the intended fixed, ordered tuple.
QUESTION [choice, intro, grading=client] Which expression creates an ordered, immutable one-item tuple containing label?
  ✔ a: (label,)
      why: Correct. (label,)
  ✘ b: (label)
      why: Parentheses alone group an expression; the trailing comma makes a one-item tuple.
  ✘ c: [label]
      why: Brackets create a mutable list rather than a tuple.
  feedback✔: Correct. (label,)  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:construct_fixed_ordered_tuple(f1,f2)   anchors=['assessment:construct_fixed_ordered_tuple']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · check · Check tuples
Quick check — Decide which unpacking assignment matches the tuple items to its targets.
QUESTION [choice, core, grading=client] A pair contains two values. Which assignment unpacks both in order?
  ✔ a: smallest, largest = pair
      why: Correct. smallest, largest = pair
  ✘ b: smallest, middle, largest = pair
      why: Three targets do not match the pair’s two values.
  ✘ c: smallest = pair
      why: This binds the whole pair to one name rather than unpacking its two items.
  feedback✔: Correct. smallest, largest = pair  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: A:unpack_tuple_with_matching_targets(f3)   anchors=['assessment:unpack_tuple_with_matching_targets']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Practice tuples
Practice — Write bounds(values) to return a tuple containing the minimum and maximum of a nonempty list, then unpack the result into smallest and largest.
QUESTION [code_exercise, core, grading=client] Keep the supplied bounds call and tuple unpacking unchanged. Assign computed_smallest to smallest and computed_largest to largest.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def bounds(values):', 'return min(values), max(values)', 'min(values)', 'max(values)', 'bounds([3, 8, 5])', 'smallest, largest = bounds([3, 8, 5])', 'Comma-separated tuple values', 'Parenthesized tuple literals', 'One-item tuple literals with a trailing comma', 'List literals containing integers', 'Variable assignment'] blocked=16 items
  file main.py [editable]:
first = 3
second = 8
third = 5
values = [first, second, third]
if True:
    def bounds(values):
        return min(values), max(values)
computed_smallest, computed_largest = bounds(values)

  SOLUTION main.py:
first = 3
second = 8
third = 5
values = [first, second, third]
if True:
    def bounds(values):
        return min(values), max(values)
computed_smallest, computed_largest = bounds(values)
smallest = computed_smallest
largest = computed_largest

  test t0 (value_equals, visible=True): {"expr":"[type(bounds(values)).__name__, bounds(values), smallest, largest]","expected":["tuple",[3,8],3,8]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t1 (function_call, visible=True): {"function":"bounds","args":[[3,8,5]],"kwargs":{},"expected":[3,8]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t2 (function_call, visible=True): {"function":"bounds","args":[[2,9,4]],"kwargs":{},"expected":[2,9]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"99a4e440c9fb65d622a991abe5619f609112df4ec696c603da0e9de510ad66f1","tests_passed":3}
  feedback✔: The result meets the task. Calling bounds([3, 8, 5]) returns (3, 8), and unpacking assigns 3 to smallest and 8 to largest in that order.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['The supplied unpacking places the minimum in computed_smallest and the maximum in computed_largest. Preserve that order when binding smallest and largest.']
  MEASURES: A:return_and_unpack_minimum_maximum_pair(f4,f5)   anchors=['practice', 'assessment:return_and_unpack_minimum_maximum_pair']
  taught-before-tested: A.f4←s01; A.f5←s01

### s05 · explainer · Function Default Keyword Args
(intro) Use the ordinary order fee unless a call overrides it. ⟦B:tb1⟧
(definition) In def name(required, optional=default):, omitting optional at a call uses its default. ⟦B.f1 B:tb2⟧
(mechanism) Positional arguments bind in order; keyword arguments bind by parameter name. Keywords follow ordinary positional arguments. ⟦B.f2 B:tb3⟧
(mechanism) Supply required arguments. Do not bind a parameter twice or use an unaccepted keyword. ⟦B.f3 B:tb3⟧
(example) Identify quantity and price as required parameters and fee as defaulted. Compare omitting fee, naming all arguments, and using keywords after positional arguments. A named fee overrides the default. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) A keyword does not permit a duplicate binding. Supply required parameters once each, and only use accepted keyword names. ⟦B.f2 B.f3 B:tb5⟧
[CODE python]
def cost(quantity, price, fee=2):
    return quantity * price + fee

print(cost(3, 4))
print(cost(3, 4, fee=5))
print(cost(quantity=3, price=4))
  annotations: ['quantity and price are required; fee has a default.', 'Match arguments by position or parameter name; omitted fee uses the default.', 'Match arguments by position or parameter name; omitted fee uses the default.', 'Match arguments by position or parameter name; omitted fee uses the default.']

### s06 · check · Check function default keyword args
Quick check — Decide which function call has invalid argument bindings.
QUESTION [choice, core, grading=client] For def cost(quantity, price, fee=2), which call supplies required arguments without binding a parameter twice?
  ✔ a: cost(3, price=4)
      why: Correct. cost(3, price=4)
  ✘ b: cost(3, 4, quantity=3)
      why: The first positional argument already binds quantity, so the keyword binds it twice.
  ✘ c: cost(quantity=3)
      why: price is required and has not been supplied.
  feedback✔: Correct. cost(3, price=4)  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r04
  MEASURES: B:recognize_invalid_argument_bindings(f3)   anchors=['assessment:recognize_invalid_argument_bindings']
  taught-before-tested: B.f3←s05

### s07 · hands_on · Practice function default keyword args
Practice — Define cost(quantity, price, fee=2) to return quantity * price + fee. Call it once using only keyword arguments with fee=5, and once omitting fee to use its default. Assign each returned value to a variable.
QUESTION [code_exercise, core, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_with_fee to with_fee. Assign computed_default_cost to default_cost. The checker reads with_fee, default_cost.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def cost(quantity, price, fee=2):', 'return quantity * price + fee', 'integer literals', 'variable assignment', 'positional function arguments', 'keyword function arguments', 'omission of a defaulted argument'] blocked=11 items
  file main.py [editable]:
quantity_input = 3
price_input = 4
if True:
    def cost(quantity, price, fee=2):
        return quantity * price + fee
computed_with_fee = cost(quantity=quantity_input, price=price_input, fee=5)
computed_default_cost = cost(quantity_input, price_input)

  SOLUTION main.py:
quantity_input = 3
price_input = 4
if True:
    def cost(quantity, price, fee=2):
        return quantity * price + fee
computed_with_fee = cost(quantity=quantity_input, price=price_input, fee=5)
computed_default_cost = cost(quantity_input, price_input)
with_fee = computed_with_fee
default_cost = computed_default_cost

  test t0 (value_equals, visible=True): {"expr":"[with_fee, default_cost]","expected":[17,14]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t1 (function_call, visible=True): {"function":"cost","args":[3,4],"kwargs":{},"expected":14} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t2 (function_call, visible=True): {"function":"cost","args":[],"kwargs":{"quantity":3,"price":4,"fee":5},"expected":17} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t3 (function_call, visible=True): {"function":"cost","args":[2,4],"kwargs":{},"expected":10} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"cff7fbc59ffdc0128cda0fd0b5633f5a65f7d57d21f1a1d3ffb1d698f6f8d7f5","tests_passed":4}
  feedback✔: The all-keyword call returns 17; the call omitting fee returns 14. Both results are stored.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Check the exact operations and result names requested in the prompt.']
  MEASURES: B:omit_defaulted_arguments(f1); B:combine_positional_and_keyword_arguments(f2)   anchors=['practice', 'assessment:omit_defaulted_arguments', 'assessment:combine_positional_and_keyword_arguments']
  taught-before-tested: B.f1←s05; B.f2←s05

### s08 · explainer · Variable Scope
(intro) Distinguish the module quantity from a helper’s local quantity. ⟦C:tb1⟧
(definition) Names assigned within a function are local throughout that function unless declared otherwise. Reading a local before binding it raises UnboundLocalError. ⟦C.f1 C:tb2⟧
(mechanism) Without a local binding, ordinary lookup can read an enclosing or module binding. ⟦C.f2 C:tb3⟧
(mechanism) globals() returns the current module namespace dictionary. globals()["name"] explicitly reads that entry even when a local shadows it. ⟦C.f3 C:tb3⟧
(mechanism) Ordinary local assignment changes the local binding, not a same-named module binding. ⟦C.f4 C:tb3⟧
(mechanism) A global declaration directs assignments to that name’s module binding instead. ⟦C.f5 C:tb3⟧
[CODE python]
quantity = 3

def show():
    quantity = 5
    print(quantity)
    print(globals()["quantity"])

show()
print(quantity)
  annotations: ['The unindented assignment binds the module name.', 'This assignment binds a separate local quantity.', 'Explicit lookup selects the module namespace entry.']

### s09 · explainer · Variable Scope
(example) In show, ordinary quantity reads its local binding, while globals()["quantity"] reads the module entry. After the call, the module quantity still refers to its module binding. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4⟧
(misconception) A module quantity cannot rescue a read of an unbound local quantity. Assignment makes that name local throughout the function unless declared otherwise. ⟦C.f1 C.f4 C:tb5⟧

### s10 · check · Check variable scope
Quick check — Decide which binding ordinary name lookup or explicit module lookup reads.
QUESTION [choice, core, grading=client] Which statement correctly describes these three functions: (1) reads quantity without assigning it; (2) assigns a local quantity, then reads globals()["quantity"]; (3) reads quantity before a later local assignment?
  ✔ a: (1) can read the module binding; (2) explicitly reads the module binding; (3) raises UnboundLocalError
      why: Without a local assignment, (1) can read the module binding. globals()["quantity"] explicitly accesses that binding in (2). The later assignment makes quantity local throughout (3), so reading it before it is bound raises UnboundLocalError.
  ✘ b: All three ordinary reads use the module binding
      why: (2) uses an explicit globals() lookup, not an ordinary local read. In (3), the later assignment makes quantity local, and the earlier unbound read raises UnboundLocalError.
  ✘ c: (1) cannot read the module binding; (2) reads the local binding; (3) reads the module binding
      why: (1) can read the module binding because it does not assign a local quantity. (2) explicitly reads the module binding through globals(). (3) reads an unbound local name and raises UnboundLocalError.
  feedback✔: Without a local assignment, (1) can read the module binding. globals()["quantity"] explicitly accesses that binding in (2). The later assignment makes quantity local throughout (3), so reading it before it is bound raises UnboundLocalError.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r06
  MEASURES: C:resolve_names_without_local_bindings(f2); C:distinguish_explicit_module_lookup_from_local_lookup(f3); C:identify_local_names_and_predict_unbound_reads(f1)   anchors=['assessment:resolve_names_without_local_bindings', 'assessment:distinguish_explicit_module_lookup_from_local_lookup', 'assessment:identify_local_names_and_predict_unbound_reads']
  taught-before-tested: C.f2←s08; C.f3←s08; C.f1←s08

### s11 · check · Check variable scope
Quick check — Decide which binding changes after local assignment or assignment with a global declaration.
QUESTION [choice, core, grading=client] Which comparison of assignment effects is correct?
  ✔ a: Ordinary local assignment changes the local binding; global quantity makes assignment target the module binding.
      why: Correct. Ordinary local assignment changes the local binding; global quantity makes assignment target the module binding.
  ✘ b: Both kinds always change the module binding.
      why: An ordinary function-assigned name is local unless declared otherwise.
  ✘ c: global quantity creates an independent local binding.
      why: global directs the name to the module binding rather than making a new local binding.
  feedback✔: Correct. Ordinary local assignment changes the local binding; global quantity makes assignment target the module binding.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: C:predict_local_and_declared_global_assignment_effects(f4,f5)   anchors=['assessment:predict_local_and_declared_global_assignment_effects']
  taught-before-tested: C.f4←s08; C.f5←s08

### s12 · hands_on · Practice variable scope
Practice — Write show() so it reads the module-level quantity through globals()["quantity"], assigns that value to a local quantity, increases the local quantity by 2, and returns it without changing the module-level quantity.
QUESTION [code_exercise, intro, grading=client] Keep the supplied function definition, call and module-level quantity unchanged. Assign computed_result to result. The supplied function modifies only its local quantity; module-level quantity must remain unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['module-level and local assignment with =', 'def show(): with an indented function body', 'quantity', 'integer literals', 'addition with +', 'globals()', 'dictionary lookup with ["quantity"]', 'return', 'show()'] blocked=15 items
  file main.py [editable]:
quantity = 3
if True:
    def show():
        quantity = globals()["quantity"]
        quantity = quantity + 2
        return quantity
computed_result = show()

  SOLUTION main.py:
quantity = 3
if True:
    def show():
        quantity = globals()["quantity"]
        quantity = quantity + 2
        return quantity
computed_result = show()
result = computed_result

  test t0 (value_equals, visible=True): {"expr":"[result, quantity]","expected":[5,3]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a5d6ea5e944830949b238a4ace6b5b98b9c9a5968c89767cd41902d70c396df2","tests_passed":1}
  feedback✔: The result meets the task. With module-level quantity initially 3, show() returns 5 and the module-level quantity remains 3 after the call.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Inside show, globals()["quantity"] reads the module value, while the assignments change only local quantity. Bind the returned computed_result to result.']
  MEASURES: C:distinguish_explicit_module_lookup_from_local_lookup(f3)   anchors=['practice', 'assessment:distinguish_explicit_module_lookup_from_local_lookup']
  taught-before-tested: C.f3←s08

### s13 · recap · Takeaways
(takeaway) Tuples carry ordered values; unpacking requires matching counts. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(takeaway) Defaults fill omissions; keywords bind accepted parameter names. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3⟧
(takeaway) Local assignment and explicit module lookup refer to different bindings. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3⟧
[UP NEXT] Error Handling: Give unsuitable quantity text a defined recovery path.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit tuples
(definition) A tuple is an ordered group whose individual items cannot be reassigned. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(definition) Comma-separated values form a tuple; (value,) forms a one-item tuple. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) A one-item tuple needs its comma, not just parentheses. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def bounds(values):
    return min(values), max(values)

smallest, largest = bounds([3, 8, 5])
print(smallest, largest)
one_item = (3,)
  annotations: []
### r02 · Revisit tuples
(definition) first, second = pair unpacks a pair. Target and value counts must match. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A pair requires two unpacking targets, not three. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def bounds(values):
    return min(values), max(values)

smallest, largest = bounds([3, 8, 5])
print(smallest, largest)
one_item = (3,)
  annotations: []
### r03 · Revisit tuples
(definition) return first, second returns a tuple of the two expression values. ⟦A.f4 A:tb3 A:tb4⟧
(definition) For a nonempty collection, min(values) obtains the smallest item and max(values) the largest. ⟦A.f5 A:tb3 A:tb4⟧
(misconception) Returning two expressions supplies one tuple to the caller, whose two values can then be unpacked. ⟦A.f4 A:tb3 A:tb4⟧
[CODE python]
def bounds(values):
    return min(values), max(values)

smallest, largest = bounds([3, 8, 5])
print(smallest, largest)
one_item = (3,)
  annotations: []
### r04 · Revisit function default keyword args
(definition) Supply required arguments. Do not bind a parameter twice or use an unaccepted keyword. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(misconception) Naming an argument does not allow binding that same parameter twice. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
[CODE python]
def cost(quantity, price, fee=2):
    return quantity * price + fee

print(cost(3, 4))
print(cost(3, 4, fee=5))
  annotations: []
### r05 · Revisit function default keyword args
(definition) In def name(required, optional=default):, omitting optional at a call uses its default. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(definition) Positional arguments bind in order; keyword arguments bind by parameter name. Keywords follow ordinary positional arguments. ⟦B.f2 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Omitting fee uses its default; explicitly supplying fee overrides that default. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
[CODE python]
def cost(quantity, price, fee=2):
    return quantity * price + fee

print(cost(3, 4))
print(cost(3, 4, fee=5))
  annotations: []
### r06 · Revisit variable scope
(definition) Without a local binding, ordinary lookup can read an enclosing or module binding. ⟦C.f2 C:tb3 C:tb4⟧
(definition) globals() returns the current module namespace dictionary. globals()["name"] explicitly reads that entry even when a local shadows it. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) Ordinary quantity can refer to a local; globals()["quantity"] explicitly reads the module entry. ⟦C.f3 C:tb3 C:tb4⟧
[CODE python]
quantity = 3

def show():
    quantity = 5
    print(quantity)
    print(globals()["quantity"])

show()
print(quantity)
  annotations: []
### r07 · Revisit variable scope
(definition) Ordinary local assignment changes the local binding, not a same-named module binding. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(definition) A global declaration directs assignments to that name’s module binding instead. ⟦C.f5 C:tb3 C:tb4⟧
(misconception) An ordinary local assignment leaves the module binding alone; a global declaration redirects assignment to the module. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantity = 3

def show():
    quantity = 5
    print(quantity)
    print(globals()["quantity"])

show()
print(quantity)
  annotations: []
### r08 · Revisit variable scope
(definition) Assigned function names are local throughout that function unless declared otherwise. Reading a local before binding it raises UnboundLocalError. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(misconception) A module quantity does not rescue a read of a quantity classified as local but not yet bound. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
[CODE python]
quantity = 3

def show():
    quantity = 5
    print(quantity)
    print(globals()["quantity"])

show()
print(quantity)
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: Default parameter values

=========

# EVALUATOR PACKET — Error Handling (learn_python.tile.018_018)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.error_handling — Error Handling

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step learn_python.tile.018_018.r02 is never referenced
  warn: remediation step learn_python.tile.018_018.r03 is never referenced
  warn: learn_python.tile.018_018.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.018_018.s04/ix.learn_python.tile.018_018.s04: ADVISORY — syntax descriptors with no detector: ['assert statements', 'comprehensions', 'finally clauses', 'for loops', 'indented try and except bodies', 'integer literals', 'lambda expressions', 'raise statements', 'string literals', 'with statements']

## SOURCE FACTS — A (python.error_handling)   objective: Catch and handle runtime errors gracefully using try/except.
A.f1: Wrap the operation in an indented try: body and provide an aligned except ExceptionType: body for its recovery action.   [sources: python_tutorial#errors.html#handling-exceptions]
A.f2: On a matching exception, remaining operations in the try body are skipped and the handler runs; without an exception the handler is skipped.   [sources: python_tutorial#errors.html#handling-exceptions]
A.f3: An unmatched exception is passed to an outer handler, or stops execution if none is found.   [sources: python_tutorial#errors.html#handling-exceptions]
A.f4: Use except ValueError: to handle an invalid numeric conversion from entered text.   [sources: python_tutorial#errors.html#handling-exceptions]
note: Begin with this objective: Catch and handle runtime errors gracefully using try/except.
note: Keep the example in the Basic runtime error handling tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.import_statements, python.pep8_style, python.for_loops.
note: The practice objective requires reading user input and printing a message, but console input/output is blocked. Use preassigned text and store the friendly recovery message in text; inspect variable state rather than requiring input() or print().
PRACTICE ANCHOR (live_code): Attempt to convert the supplied text into a numeric quantity. Handle ValueError by assigning a friendly recovery message to text instead of displaying it.  SUCCESS: Invalid numeric text produces the friendly recovery message in text without an unhandled ValueError. Valid numeric text produces quantity and skips the recovery assignment.
ASSESSMENT ANCHOR: wrap_numeric_conversion_in_try_except facts=['f1', 'f4']
ASSESSMENT ANCHOR: trace_matching_and_unmatched_exception_paths facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Choosing a built-in collection; Comprehensions; Continuing expressions across lines; Distinguishing syntax and runtime errors; Enumerate iteration; File Io; Floating-point approximation limits; For Loops; Import Statements; Indentation and code blocks; Iterating Collections; Loop Control; Nested loops; PEP 8 Style; Python comments; Python interpreter execution model; Reading and displaying console values; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration

## LESSON, in learner order

### s01 · explainer · Error Handling
(intro) Give unsuitable quantity text a defined recovery path. ⟦A:tb1⟧
(definition) Put the operation in an indented try: body; align except ExceptionType: with try and indent the recovery body. ⟦A.f1 A:tb2⟧
(mechanism) A matching exception skips the rest of try and runs the handler. With no exception, the handler is skipped. ⟦A.f2 A:tb3⟧
(mechanism) An unmatched exception passes to an outer handler, or stops execution if no handler is found. ⟦A.f3 A:tb3⟧
(mechanism) except ValueError: handles an invalid numeric conversion from entered text. ⟦A.f4 A:tb3⟧
(example) Read the conversion before the multiplication. Invalid numeric text reaches the matching ValueError handler and skips the remaining try operations. Suitable numeric text takes the success path and skips that handler. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧
(misconception) Handling the failure does not make conversion succeed. The multiplication remaining in try is skipped after the conversion raises. ⟦A.f2 A.f3 A:tb5⟧
[CODE python]
text = "three"
try:
    quantity = int(text)
    print(quantity * 4)
except ValueError:
    print("Enter a numeric quantity")
  annotations: ['Begin the protected body.', 'A conversion failure transfers control to a matching handler.', 'This operation is skipped if the preceding conversion raises.', 'The aligned handler matches invalid numeric conversion.']

### s02 · check · Check error handling
Quick check — Decide which try/except arrangement handles the supplied numeric conversion.
QUESTION [choice, intro, grading=client] Which layout protects quantity = int(text) with ValueError recovery?
  ✔ a: Put conversion in an indented try body and recovery in an aligned except ValueError body.
      why: Correct. Put conversion in an indented try body and recovery in an aligned except ValueError body.
  ✘ b: Put conversion before try and recovery inside try.
      why: A conversion outside the protected body is not protected by that try.
  ✘ c: Indent except ValueError underneath the conversion inside try.
      why: The except header must align with try; its recovery body is indented below its own header.
  feedback✔: Correct. Put conversion in an indented try body and recovery in an aligned except ValueError body.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:wrap_numeric_conversion_in_try_except(f1,f4)   anchors=['assessment:wrap_numeric_conversion_in_try_except']
  taught-before-tested: A.f1←s01; A.f4←s01

### s03 · check · Check error handling
Quick check — Trace whether each exception matches the handler and which path follows.
QUESTION [choice, core, grading=client] What happens if the try body succeeds, versus raising an exception that does not match except ValueError?
  ✔ a: Success skips the handler; an unmatched exception propagates.
      why: Correct. Success skips the handler; an unmatched exception propagates.
  ✘ b: Success runs the handler; unmatched exceptions are ignored.
      why: The handler runs only for a matching exception, and an unmatched exception is not handled there.
  ✘ c: The handler catches every exception because it names ValueError.
      why: A typed handler catches matching exceptions, not arbitrary unmatched types.
  feedback✔: Correct. Success skips the handler; an unmatched exception propagates.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: A:trace_matching_and_unmatched_exception_paths(f2,f3)   anchors=['assessment:trace_matching_and_unmatched_exception_paths']
  taught-before-tested: A.f2←s01; A.f3←s01

### s04 · hands_on · Practice error handling
Practice — Attempt to convert the supplied text into a numeric quantity. Handle ValueError by assigning a friendly recovery message to text instead of displaying it.
QUESTION [code_exercise, stretch, grading=client] Assign supplied_message to friendly_message before the supplied try/except block. Keep the conversion and handler unchanged: valid text produces quantity; invalid text recovers with friendly_message.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'integer literals', 'int(text)', 'try:', 'except ValueError:', 'indented try and except bodies'] blocked=13 items
  file main.py [editable]:
text = "3"
supplied_message = "Enter a numeric quantity"
try:
    quantity = int(text)
except ValueError:
    text = friendly_message

  SOLUTION main.py:
text = "3"
supplied_message = "Enter a numeric quantity"
friendly_message = supplied_message
try:
    quantity = int(text)
except ValueError:
    text = friendly_message

  test t0 (value_equals, visible=True): {"expr":"[text, globals().get(\"quantity\"), (lambda scope: (exec(open(\"main.py\").read().replace('text = \"3\"', 'text = \"three\"'), scope), [scope[\"text\"], scope.get(\"quantity\")])[1])({})]","expected":["3",3,["Enter a numeric quantity",null]]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"8af3b4824387c6d64b3f4a7386b3b1adb87840d11299fe478e92c88008577e84","tests_passed":1}
  feedback✔: The result meets the task. Invalid numeric text produces the friendly recovery message in text without an unhandled ValueError. Valid numeric text produces quantity and skips the recovery assignment.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Bind friendly_message before the protected block. Valid text skips the handler; invalid text reaches the handler that uses this binding.']
  MEASURES: A:wrap_numeric_conversion_in_try_except(f1,f4); A:trace_matching_and_unmatched_exception_paths(f2,f3)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f4←s01; A.f2←s01; A.f3←s01

### s05 · recap · Takeaways
(takeaway) Matching failures enter the handler and skip the rest of try. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3⟧
[UP NEXT] Import Statements: Choose the name that gives access to the math operation.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit error handling
(definition) Put the operation in an indented try: body; align except ExceptionType: with try and indent the recovery body. ⟦A.f1 A:tb2 A:tb4⟧
(definition) except ValueError: handles an invalid numeric conversion from entered text. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) The ValueError handler matches invalid numeric conversion; it is not a handler for every exception type. ⟦A.f4 A:tb3 A:tb4⟧
[CODE python]
text = "three"
try:
    quantity = int(text)
    print(quantity * 4)
except ValueError:
    print("Enter a numeric quantity")
  annotations: []
### r02 · Revisit error handling
(definition) A matching exception skips the rest of try and runs the handler. With no exception, the handler is skipped. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) An unmatched exception passes to an outer handler, or stops execution if no handler is found. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) A failed conversion skips the remaining try work; a successful conversion skips the handler. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
[CODE python]
text = "three"
try:
    quantity = int(text)
    print(quantity * 4)
except ValueError:
    print("Enter a numeric quantity")
  annotations: []
### r03 · Revisit error handling
(definition) Put the operation in an indented try: body; align except ExceptionType: with try and indent the recovery body. ⟦A.f1 A:tb2 A:tb4⟧
(definition) except ValueError: handles an invalid numeric conversion from entered text. ⟦A.f4 A:tb3 A:tb4⟧
(definition) A matching exception skips the rest of try and runs the handler. With no exception, the handler is skipped. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(definition) An unmatched exception passes to an outer handler, or stops execution if no handler is found. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) The ValueError handler matches invalid numeric conversion; it is not a handler for every exception type. ⟦A.f4 A:tb3 A:tb4⟧
[CODE python]
text = "three"
try:
    quantity = int(text)
    print(quantity * 4)
except ValueError:
    print("Enter a numeric quantity")
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expr: [text, globals().get("quantity"), (lambda scope: (exec(open("main.py").read().replace('text = "3"', 'text = "three"'), scope), [scope["text"], scope.get("quantity")])[1])({})]
· ops.value: Enter a numeric quantity_x
· expected.value: Enter a numeric quantity_x

=========

# EVALUATOR PACKET — Import Statements (learn_python.tile.019_019)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.import_statements — Import Statements

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step learn_python.tile.019_019.r02 is never referenced
  warn: learn_python.tile.019_019.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.019_019.s03/ix.learn_python.tile.019_019.s03: ADVISORY — syntax descriptors with no detector: ['comprehensions', 'for statements', 'integer and floating-point literals', 'lambda expressions', 'with statements']
  warn: plan: learn_python.tile.019_019.s03 was planned to measure python.import_statements#assessment:import_member_and_call_directly but its interaction does not

## SOURCE FACTS — A (python.import_statements)   objective: Bring code from another module into the current file using import.
A.f1: import module binds the module name; use module.member to access its functionality.   [sources: python_tutorial#modules.html#more-on-modules]
A.f2: from module import member binds that member directly in the importing namespace.   [sources: python_tutorial#modules.html#more-on-modules]
A.f3: After import math, a call such as math.cos(value) accesses a math function.   [sources: python_tutorial#stdlib.html#mathematics]
note: Begin with this objective: Bring code from another module into the current file using import.
note: Keep the example in the Importing reusable code tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.pep8_style, python.for_loops, python.loop_control.
PRACTICE ANCHOR (live_code): Import the math module, call math.cos with value as its argument, and assign the returned value back to value.  SUCCESS: The code uses import math followed by value = math.cos(value), leaving value equal to 1.0 from a starting value of 0.
ASSESSMENT ANCHOR: import_module_and_call_qualified_member facts=['f1', 'f3']
ASSESSMENT ANCHOR: import_member_and_call_directly facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Checking for None with identity; Choosing a built-in collection; Comprehensions; Continuing expressions across lines; Distinguishing syntax and runtime errors; Enumerate iteration; File Io; Floating-point approximation limits; For Loops; Indentation and code blocks; Iterating Collections; Loop Control; Nested loops; PEP 8 Style; Python comments; Python interpreter execution model; Reading and displaying console values; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration

## LESSON, in learner order

### s01 · explainer · Import Statements
(intro) Choose the name that gives access to the math operation. ⟦A:tb1⟧
(definition) import module binds the module name. Access functionality with module.member. ⟦A.f1 A:tb2⟧
(mechanism) from module import member binds that member directly in the importing namespace. ⟦A.f2 A:tb3⟧
(mechanism) After import math, math.cos(value) accesses a math function. ⟦A.f3 A:tb3⟧
(example) Connect import math to math.cos, and from math import cos to the bare cos name. Both call forms access the same member; their name bindings differ. ⟦A.f1 A.f2 A.f3 A:tb4⟧
(misconception) import math does not bind every member as a bare name. Use math.cos, or explicitly import cos before using that name. ⟦A.f1 A.f2 A:tb5⟧
[CODE python]
import math
print(math.cos(0))
from math import cos
print(cos(0))
  annotations: ['Bind the module name; the following call uses math.cos.', 'Bind cos directly; the following call uses cos without the module prefix.']

### s02 · check · Check import statements
Quick check — Decide which import allows the supplied member to be called directly.
QUESTION [choice, intro, grading=client] After from math import cos, how is the imported function called directly for value?
  ✔ a: cos(value)
      why: Correct. cos(value)
  ✘ b: math.cos(value), assuming this import also binds math
      why: Importing the member binds cos directly; it does not bind the module name math.
  ✘ c: import cos(value)
      why: import binds names; it is not a function-call expression.
  feedback✔: Correct. cos(value)  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:import_member_and_call_directly(f2)   anchors=['assessment:import_member_and_call_directly']
  taught-before-tested: A.f2←s01

### s03 · hands_on · Practice import statements
Practice — Import the math module, call math.cos with value as its argument, and assign the returned value back to value.
QUESTION [code_exercise, stretch, grading=client] Import math, then update value by calling math.cos(value). Keep the starting value; do not display it. The checker reads value.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import math', 'from math import cos', 'math.cos(value)', 'cos(value)', 'variable assignment', 'integer and floating-point literals'] blocked=10 items
  file main.py [editable]:
value = 0

  SOLUTION main.py:
value = 0
import math
value = math.cos(value)

  test t0 (value_equals, visible=True): {"expr":"value","expected":1.0} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"947cb217ddc7d446f0c1b1672c54130f1bd38074c4d07e9b5ac9a1ab5dc9608c","tests_passed":1}
  feedback✔: The result meets the task. The code uses import math followed by value = math.cos(value), leaving value equal to 1.0 from a starting value of 0.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Keep the supplied inputs and use their names in your computation.', 'Check indentation and the exact result names requested in the prompt.']
  MEASURES: A:import_module_and_call_qualified_member(f1,f3)   anchors=['practice', 'assessment:import_module_and_call_qualified_member']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · recap · Takeaways
(takeaway) Import form determines whether a call uses a module prefix. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3⟧
[UP NEXT] PEP 8 Style: Reformat the order helper without changing operations.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit import statements
(definition) from module import member binds that member directly in the importing namespace. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) import math binds math; from math import cos binds cos directly. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
[CODE python]
import math
print(math.cos(0))
from math import cos
print(cos(0))
  annotations: []
### r02 · Revisit import statements
(definition) import module binds the module name. Access functionality with module.member. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(definition) from module import member binds that member directly in the importing namespace. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(definition) After import math, math.cos(value) accesses a math function. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) import math binds math; from math import cos binds cos directly. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
[CODE python]
import math
print(math.cos(0))
from math import cos
print(cos(0))
  annotations: []

=========

# EVALUATOR PACKET — PEP 8 Style (learn_python.tile.020_020)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.pep8_style — PEP 8 Style

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.020_020.r02 is never referenced
  warn: learn_python.tile.020_020.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.020_020.s04/ix.learn_python.tile.020_020.s04: ADVISORY — syntax descriptors with no detector: ['assert statements', 'class statements', 'comment lines', 'comprehensions', 'def with named parameters', 'docstring literals', 'for statements', 'four-space block indentation', 'function calls with positional arguments', 'integer literals', 'lambda expressions', 'lowercase identifiers with underscores', 'multiline expression continuation', 'multiplication with *', 'parentheses and comma-separated arguments', 'variable assignment with =', 'with statements', 'yield']

## SOURCE FACTS — A (python.pep8_style)   objective: Write idiomatic, PEP 8-compliant Python for readability (naming, spacing, line length).
A.f1: Use four spaces per block indentation level.   [sources: pep8_style_guide#indentation]
A.f2: Use lowercase function and variable names, separating words with underscores when this improves readability.   [sources: pep8_style_guide#function-and-variable-names]
A.f3: Avoid extra spaces immediately inside parentheses, brackets or braces, before commas or colons, and between a function name and its call parentheses.   [sources: pep8_style_guide#pet-peeves]
A.f4: Use a single space on either side of assignment and comparison operators, while grouping arithmetic spacing to reflect priority.   [sources: pep8_style_guide#other-recommendations]
A.f5: PEP 8 recommends limiting code lines to 79 characters and flowing comments or docstrings to 72 characters.   [sources: pep8_style_guide#maximum-line-length]
note: Begin with this objective: Write idiomatic, PEP 8-compliant Python for readability (naming, spacing, line length).
note: Keep the example in the Readable Python style tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.for_loops, python.loop_control, python.iterating_collections.
PRACTICE ANCHOR (live_code): Rewrite a working but poorly styled order-cost function using lowercase underscore-separated names, four-space indentation, and appropriate punctuation and operator spacing without changing its calculation.  SUCCESS: The function is named order_cost, its parameters are quantity and unit_price, and its local result is cost. Its body uses four-space indentation, appropriate spacing, and lines within 79 characters. Calling order_cost(3, 4) returns 12.
ASSESSMENT ANCHOR: apply_four_space_indentation facts=['f1']
ASSESSMENT ANCHOR: apply_lowercase_underscore_naming facts=['f2']
ASSESSMENT ANCHOR: apply_pep8_punctuation_and_operator_spacing facts=['f3', 'f4']
ASSESSMENT ANCHOR: apply_recommended_line_length_limits facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Checking for None with identity; Choosing a built-in collection; Comprehensions; Continuing expressions across lines; Distinguishing syntax and runtime errors; Encoding and decoding Unicode text and bytes; Enumerate iteration; File Io; Floating-point approximation limits; For Loops; Indentation and code blocks; Iterating Collections; Loop Control; Nested loops; Python comments; Python interpreter execution model; Reading and displaying console values; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration

## LESSON, in learner order

### s01 · explainer · PEP 8 Style
(intro) Reformat the order helper without changing operations. ⟦A:tb1⟧
(definition) Use four spaces per block indentation level. ⟦A.f1 A:tb2⟧
(mechanism) Use lowercase function and variable names; add underscores between words when that improves readability. ⟦A.f2 A:tb3⟧
(mechanism) Avoid extra spaces inside parentheses, brackets or braces, before commas or colons, or between a function name and its call parentheses. ⟦A.f3 A:tb3⟧
(mechanism) Put one space beside assignment and comparison operators; group arithmetic spacing to reflect priority. ⟦A.f4 A:tb3⟧
(mechanism) PEP 8 recommends code lines of at most 79 characters, and comments or docstrings flowed to 72. ⟦A.f5 A:tb3⟧
[BEFORE_AFTER] Same calculation; clearer names, indentation and spacing.
  before:
[CODE python]
def OrderCost( Quantity , UnitPrice ) :
  Cost=Quantity*UnitPrice
  return Cost

print( OrderCost( 3 , 4))
  annotations: []
  after:
[CODE python]
def order_cost(quantity, unit_price):
    cost = quantity * unit_price
    return cost

print(order_cost(3, 4))
  annotations: ['Use lowercase words separated with underscores.', 'Four-space indentation; spaced assignment and arithmetic.', 'No extra punctuation spacing.']

### s02 · explainer · PEP 8 Style
(example) Compare the same helper before and after reformatting. Notice lowercase underscore-separated names, four-space indentation and punctuation spacing. Keep the recommended line limits in view as the helper grows. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧
(misconception) Recommended line lengths are not a rule that longer lines are invalid syntax. Keep style recommendations distinct from block indentation. ⟦A.f5 A:tb5⟧

### s03 · check · Check pep 8 style
Quick check — Decide which example follows the recommended line-length limits.
QUESTION [choice, intro, grading=client] Which PEP 8 pair gives the recommended code-line and flowing comment/docstring limits?
  ✔ a: 79 characters for code; 72 for flowing comments or docstrings.
      why: Correct. 79 characters for code; 72 for flowing comments or docstrings.
  ✘ b: 72 for code; 79 for flowing comments or docstrings.
      why: This reverses the two recommendations.
  ✘ c: 79 for both.
      why: Flowing comments and docstrings have the shorter recommended limit.
  feedback✔: Correct. 79 characters for code; 72 for flowing comments or docstrings.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:apply_recommended_line_length_limits(f5)   anchors=['assessment:apply_recommended_line_length_limits']
  taught-before-tested: A.f5←s01

### s04 · hands_on · Practice pep 8 style
Practice — Rewrite a working but poorly styled order-cost function using lowercase underscore-separated names, four-space indentation, and appropriate punctuation and operator spacing without changing its calculation.
QUESTION [code_exercise, stretch, grading=client] Keep the supplied input constants, four-space-indented function definition and call unchanged. Restyle the last assignment: use the lowercase name result and a single space on each side of =, assigning computed_result to result. Preserve the calculation and keep all lines within 79 characters.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def with named parameters', 'return', 'variable assignment with =', 'integer literals', 'multiplication with *', 'function calls with positional arguments', 'parentheses and comma-separated arguments', 'lowercase identifiers with underscores', 'four-space block indentation'] blocked=15 items
  file main.py [editable]:
quantity_input = 3
price_input = 4
if True:
    def order_cost(quantity, unit_price):
        cost = quantity * unit_price
        return cost
computed_result = order_cost(quantity_input, price_input)
Result=computed_result

  SOLUTION main.py:
quantity_input = 3
price_input = 4
if True:
    def order_cost(quantity, unit_price):
        cost = quantity * unit_price
        return cost
computed_result = order_cost(quantity_input, price_input)
result = computed_result

  test t0 (value_equals, visible=True): {"expr":"[result, (lambda scope: (exec('import ast\\n_tree = ast.parse(open(\"main.py\").read())\\n_assignments = [n for n in _tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == \"result\" for t in n.targets)]\\n_lines = open(\"main.py\").read().splitlines()\\n_assignment_ok = len(_assignments) == 1 and ast.dump(_assignments[0].value, include_attributes=False) == ast.dump(ast.parse(\"computed_result\", mode=\"eval\").body, include_attributes=False) and all(len(_li | on-fail: Preserve the calculation and check the required names, four-space body indentation, punctuation/operator spacing and 79-character code-line limit.
  test t1 (function_call, visible=True): {"function":"order_cost","args":[3,4],"kwargs":{},"expected":12} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t2 (function_call, visible=True): {"function":"order_cost","args":[2,5],"kwargs":{},"expected":10} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"54a3bf301aa239a57a126a2f54369d9c7b32d7f97e200b014fd7f6e6ee829bb9","tests_passed":3}
  feedback✔: The result meets the task. The function is named order_cost, its parameters are quantity and unit_price, and its local result is cost. Its body uses four-space indentation, appropriate spacing, and lines within 79 characters. Calling order_cost(3, 4) returns 12.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Restyle Result=computed_result as result = computed_result. The supplied function already demonstrates the remaining style requirements.']
  MEASURES: A:apply_four_space_indentation(f1); A:apply_lowercase_underscore_naming(f2); A:apply_pep8_punctuation_and_operator_spacing(f3,f4)   anchors=['practice', 'assessment:apply_four_space_indentation', 'assessment:apply_lowercase_underscore_naming', 'assessment:apply_pep8_punctuation_and_operator_spacing']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s05 · recap · Takeaways
(takeaway) Use readable names and spacing; distinguish recommendations from syntax. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
[UP NEXT] For Loops: Visit the quantities while carrying a running total.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit pep 8 style
(definition) PEP 8 recommends code lines of at most 79 characters, and comments or docstrings flowed to 72. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Recommended line lengths do not mean every longer line is invalid syntax. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def order_cost(quantity, unit_price):
    cost = quantity * unit_price
    return cost

print(order_cost(3, 4))
  annotations: []
### r02 · Revisit pep 8 style
(definition) Use four spaces per block indentation level. ⟦A.f1 A:tb2 A:tb4⟧
(definition) Use lowercase function and variable names; add underscores between words when that improves readability. ⟦A.f2 A:tb3 A:tb4⟧
(definition) Avoid extra spaces inside parentheses, brackets or braces, before commas or colons, or between a function name and its call parentheses. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Put one space beside assignment and comparison operators; group arithmetic spacing to reflect priority. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Keep spaces around operators, not extra spaces inside call punctuation. ⟦A.f3 A:tb3 A:tb4⟧
[CODE python]
def order_cost(quantity, unit_price):
    cost = quantity * unit_price
    return cost

print(order_cost(3, 4))
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expr: [result, (lambda scope: (exec('import ast\n_tree = ast.parse(open("main.py").read())\n_assignments = [n for n in _tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "result" for t in n.targets)]\n_lines = open("main.py").read().splitlines()\n_assignment_ok = len(_assignments) == 1 and ast.dump(_assignments[0].value, include_attributes=False) == ast.dump(ast.parse("computed_result", mode="eval").body, include_attributes=False) and all(len(_lines[n.lineno-1]) <= 79 for n in _assignments)\n', scope), scope["_assignment_ok"])[1])(globals().copy()), (lambda scope: (exec('import ast, io, tokenize\n_style_source = open("main.py").read()\n_style_tree = ast.parse(_style_source)\n_style_functions = [n for n in ast.walk(_style_tree) if isinstance(n, ast.FunctionDef)]\n_style_ok = len(_style_functions) == 1\nif _style_ok:\n    _style_f = _style_functions[0]\n    _style_ok = _style_f.name == "order_cost" and [a.arg for a in _style_f.args.args] == ["quantity", "unit_price"]\n    _style_ok = _style_ok and {n.id for n in ast.walk(_style_f) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)} == {"cost"}\n_style_lines = _style_source.splitlines()\n_style_ok = _style_ok and all(len(line) <= 79 and "\\t" not in line for line in _style_lines)\nif _style_functions:\n    _style_ok = _style_ok and all(n.col_offset == _style_functions[0].col_offset + 4 for n in _style_functions[0].body)\n_style_tokens = [t for t in tokenize.generate_tokens(io.StringIO(_style_source).readline) if t.type not in (tokenize.ENCODING, tokenize.INDENT, tokenize.DEDENT, tokenize.NL, tokenize.NEWLINE, tokenize.ENDMARKER)]\nfor index, token in enumerate(_style_tokens):\n    before = _style_tokens[index - 1] if index else None\n    after = _style_tokens[index + 1] if index + 1 < len(_style_tokens) else None\n    if token.string in ("=", "*"):\n        _style_ok = _style_ok and before is not None and after is not None and before.end[0] == token.start[0] == after.start[0]\n        if before and after and before.end[0] == token.start[0] == after.start[0]:\n            line = _style_lines[token.start[0] - 1]\n            _style_ok = _style_ok and line[before.end[1]:token.start[1]] == " " and line[token.end[1]:after.start[1]] == " "\n    if token.string in ("(", "[", "{") and after and token.end[0] == after.start[0]:\n        _style_ok = _style_ok and token.end[1] == after.start[1]\n    if token.string in (")", "]", "}", ",", ":") and before and before.end[0] == token.start[0]:\n        _style_ok = _style_ok and before.end[1] == token.start[1]\n    if token.string == "(" and before and before.type == tokenize.NAME and before.end[0] == token.start[0]:\n        _style_ok = _style_ok and before.end[1] == token.start[1]\n    if token.string == "," and after and token.end[0] == after.start[0]:\n        _style_ok = _style_ok and _style_lines[token.start[0]-1][token.end[1]:after.start[1]] == " "\n', scope), result if scope["_style_ok"] else None)[1])(globals().copy())]

=========

# EVALUATOR PACKET — For Loops / Loop Control / Iterating Collections / Comprehensions (learn_python.tile.021_024)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.for_loops — For Loops
B = python.loop_control — Loop Control
C = python.iterating_collections — Iterating Collections
D = python.comprehensions — Comprehensions

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=15
  warn: remediation step learn_python.tile.021_024.r02 is never referenced
  warn: remediation step learn_python.tile.021_024.r04 is never referenced
  warn: remediation step learn_python.tile.021_024.r06 is never referenced
  warn: remediation step learn_python.tile.021_024.r07 is never referenced
  warn: remediation step learn_python.tile.021_024.r09 is never referenced
  warn: remediation step learn_python.tile.021_024.r10 is never referenced
  warn: learn_python.tile.021_024.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.021_024.s03/ix.learn_python.tile.021_024.s03: ADVISORY — syntax descriptors with no detector: ['addition with +', 'flat list literals', 'for ... else', 'for quantity in quantities:', 'generator expressions', 'indented for-loop body', 'integer literals', 'list, set, and dictionary comprehensions', 'nested for loops', 'variable assignment with =']
  warn: learn_python.tile.021_024.s04: prose block without lineage.fact_ids
  warn: learn_python.tile.021_024.s07/ix.learn_python.tile.021_024.s07: ADVISORY — syntax descriptors with no detector: ['== comparisons', 'addition with +', 'assert statements', 'for quantity in a list', 'if conditions', 'integer literals', 'list literals', 'list, set, and dictionary comprehensions', 'nested for or while loops']
  warn: learn_python.tile.021_024.s08: prose block without lineage.fact_ids
  warn: learn_python.tile.021_024.s11/ix.learn_python.tile.021_024.s11: ADVISORY — syntax descriptors with no detector: ['assignment to an existing dictionary key', 'comprehensions', 'dictionary literals', 'indented loop body', 'integer addition with +', 'integer literals', 'nested collection literals', 'nested loops', 'string literals', 'yield']
  warn: learn_python.tile.021_024.s12: prose block without lineage.fact_ids
  warn: learn_python.tile.021_024.s15/ix.learn_python.tile.021_024.s15: ADVISORY — syntax descriptors with no detector: ['[expression for quantity in quantities if condition]', 'assert statements', 'equality comparison with ==', 'generator expressions', 'integer literals, including negative integers', 'lambda expressions', 'list literals', 'multiplication with *', 'nested comprehensions', 'remainder with %', 'variable assignment with =', 'yield']
  warn: learn_python.tile.021_024.s16: text contains the name of blocked future concept python.comprehensions ('comprehensions') — check it is not needed to understand

## SOURCE FACTS — A (python.for_loops)   objective: Iterate a known, finite number of times over a sequence using a for loop.
A.f1: Write for item in sequence: followed by an indented body to process successive sequence items in their order.   [sources: python_tutorial#controlflow.html#for-statements]
A.f2: Initialize total = 0 before the loop, then assign total = total + item inside the loop to accumulate the numeric items.   [sources: python_tutorial#introduction.html#numbers, python_tutorial#controlflow.html#for-statements]
note: Begin with this objective: Iterate a known, finite number of times over a sequence using a for loop.
note: Keep the example in the Processing and transforming collections tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.loop_control, python.iterating_collections, python.comprehensions.
PRACTICE ANCHOR (live_code): Write a for loop that sums the values in quantities = [3, 2, 5], initializing total before the loop and updating it for each quantity.  SUCCESS: The loop processes all three quantities exactly once, in list order, and leaves total equal to 10.
ASSESSMENT ANCHOR: write_for_loop_processing_each_sequence_item_once facts=['f1']
ASSESSMENT ANCHOR: accumulate_numeric_items_with_a_for_loop facts=['f1', 'f2']

## SOURCE FACTS — B (python.loop_control)   objective: Alter normal loop iteration using break (exit early) and continue (skip to the next iteration).
B.f1: break exits the innermost enclosing for or while loop.   [sources: python_tutorial#controlflow.html#break-and-continue-statements]
B.f2: continue skips the rest of the current loop body and proceeds to the next iteration.   [sources: python_tutorial#controlflow.html#break-and-continue-statements]
B.f3: Place break or continue in a conditional inside the loop so it applies only when its condition holds.   [sources: python_tutorial#controlflow.html#break-and-continue-statements]
note: Begin with this objective: Alter normal loop iteration using break (exit early) and continue (skip to the next iteration).
note: Keep the example in the Processing and transforming collections tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.iterating_collections, python.comprehensions, python.file_io.
PRACTICE ANCHOR (live_code): Write a loop that searches [3, 0, 2, -1, 8] for the target -1, breaking as soon as it is found. Treat zero as an invalid entry and skip it with continue. Add other quantities to total.  SUCCESS: Zero bypasses the addition, -1 ends the loop immediately, and 8 is never processed. The final value of total is 5.
ASSESSMENT ANCHOR: use_conditional_break_for_early_exit facts=['f1', 'f3']
ASSESSMENT ANCHOR: use_conditional_continue_for_selective_skipping facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_loop_exit_from_iteration_skipping facts=['f1', 'f2']

## SOURCE FACTS — C (python.iterating_collections)   objective: Iterate over the elements of Python's core data structures (lists, dicts, sets, tuples) uniformly.
C.f1: Use for item in collection: with an indented body to visit successive elements.   [sources: python_tutorial#controlflow.html#for-statements]
C.f2: Lists and tuples are ordered sequences.   [sources: python_tutorial#datastructures.html#tuples-and-sequences]
C.f3: Sets are unordered, so their traversal is not positional sequence traversal.   [sources: python_tutorial#datastructures.html#sets]
C.f4: Iterating a dictionary directly visits its keys.   [sources: python_tutorial#datastructures.html#dictionaries]
C.f5: Use for key, value in mapping.items(): to visit dictionary key-value pairs together.   [sources: python_tutorial#datastructures.html#looping-techniques]
note: Begin with this objective: Iterate over the elements of Python's core data structures (lists, dicts, sets, tuples) uniformly.
note: Keep the example in the Processing and transforming collections tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.comprehensions, python.file_io, python.collection_selection.
note: The practice objective requests printing, but console output is blocked at this boundary. Replace printing with updating each existing quantity through its bound key; this preserves dictionary pair traversal and makes success inspectable without console output.
PRACTICE ANCHOR (live_code): Write a loop over quantities.items() that binds each pair to label and quantity, then assigns quantity + 1 to quantities[label].  SUCCESS: The loop visits both key-value pairs and updates the existing quantities to {"notebook": 4, "pen": 3}, without adding or removing keys or using console output.
ASSESSMENT ANCHOR: iterate_list_and_tuple_elements_in_sequence_order facts=['f1', 'f2']
ASSESSMENT ANCHOR: iterate_set_elements_without_assuming_positions facts=['f1', 'f3']
ASSESSMENT ANCHOR: iterate_dictionary_keys_directly facts=['f1', 'f4']
ASSESSMENT ANCHOR: iterate_dictionary_key_value_pairs facts=['f1', 'f5']

## SOURCE FACTS — D (python.comprehensions)   objective: Build a new list or dict in one expression using comprehension syntax.
D.f1: [expression for item in iterable if condition] builds a new list by evaluating expression for the items that pass the optional condition.   [sources: python_tutorial#datastructures.html#list-comprehensions]
D.f3: {key_expression: value_expression for item in iterable} builds a dictionary from computed keys and values; an if clause can filter the items.   [sources: python_tutorial#datastructures.html#dictionaries]
note: Begin with this objective: Build a new list or dict in one expression using comprehension syntax.
note: Keep the example in the Processing and transforming collections tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.file_io, python.collection_selection, python.console_input_output.
PRACTICE ANCHOR (live_code): Write a list comprehension that squares the even numbers in quantities.  SUCCESS: The comprehension assigns doubled the value [4] when quantities is [3, -1, 2], excluding the odd numbers and squaring the accepted number.
ASSESSMENT ANCHOR: write_list_comprehension_with_optional_filter facts=['f1']
ASSESSMENT ANCHOR: write_dict_comprehension_with_optional_filter facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Avoiding unintended mutations through shared references; Checking for None with identity; Choosing a built-in collection; Comprehensions; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Encoding and decoding Unicode text and bytes; Enumerate iteration; File Io; Floating-point approximation limits; Indentation and code blocks; Inspecting program state with diagnostic printing; Iterating Collections; Loop Control; Nested loops; Python comments; Python interpreter execution model; Reading and displaying console values; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · For Loops
(intro) Visit the quantities while carrying a running total. ⟦A:tb1⟧
(definition) Write for item in sequence: with an indented body. Process successive sequence items in their order. ⟦A.f1 A:tb2⟧
(mechanism) Initialize total = 0 before the loop. Inside, use total = total + item to accumulate numeric items. ⟦A.f2 A:tb3⟧
(example) Initialize once, then reuse the current total on the right of each update. Each quantity is the next sequence item, so the accumulator carries earlier additions forward. ⟦A.f1 A.f2 A:tb4⟧
(misconception) Initializing total inside the loop discards the earlier accumulated value. Prepare it once outside, then update it inside. ⟦A.f2 A:tb5⟧
[CODE python]
quantities = [3, 2, 5]
total = 0
for quantity in quantities:
    total = total + quantity
print(total)
  annotations: ['Initialize once before the loop.', 'Bind the next sequence item.', 'Reuse the previous total, then assign the updated result.', 'Iteration trace: quantity 3 changes total from 0 to 3; quantity 2 changes it from 3 to 5; quantity 5 changes it from 5 to 10.']

### s02 · check · Check for loops
Quick check — Trace the accumulator and decide how each quantity updates total.
QUESTION [choice, intro, grading=client] In a loop that adds each quantity to total, why is total = 0 placed before the loop rather than inside it?
  ✔ a: It initializes the running total once so each addition retains earlier items.
      why: Correct. It initializes the running total once so each addition retains earlier items.
  ✘ b: It must reset total each iteration to accumulate all items.
      why: Resetting inside the loop discards the earlier accumulated items.
  ✘ c: It makes the loop process only the final item.
      why: Initialization before the loop does not skip iterations; for visits successive items.
  feedback✔: Correct. It initializes the running total once so each addition retains earlier items.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:accumulate_numeric_items_with_a_for_loop(f1,f2)   anchors=['assessment:accumulate_numeric_items_with_a_for_loop']
  taught-before-tested: A.f1←s01; A.f2←s01

### s03 · hands_on · Practice for loops
Practice — Write a for loop that sums the values in quantities = [3, 2, 5], initializing total before the loop and updating it for each quantity.
QUESTION [code_exercise, core, grading=client] Initialize total by assigning zero to total before the supplied loop. Keep the loop and its input assignments unchanged. The checker reads total.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'integer literals', 'flat list literals', 'for quantity in quantities:', 'indented for-loop body', 'addition with +'] blocked=12 items
  file main.py [editable]:
quantities = [3, 2, 5]
zero = 0
for quantity in quantities:
    total = total + quantity

  SOLUTION main.py:
quantities = [3, 2, 5]
zero = 0
total = zero
for quantity in quantities:
    total = total + quantity

  test t0 (value_equals, visible=True): {"expr":"total","expected":10} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"803ae93f26dd8e8d16c7224356bd8c5bed54b8a62af7410d0a44f138529e03af","tests_passed":1}
  feedback✔: The result meets the task. The loop processes all three quantities exactly once, in list order, and leaves total equal to 10.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Bind total to zero before the loop so each supplied update retains the earlier accumulated value.']
  MEASURES: A:write_for_loop_processing_each_sequence_item_once(f1)   anchors=['practice', 'assessment:write_for_loop_processing_each_sequence_item_once']
  taught-before-tested: A.f1←s01

### s04 · explainer · Loop Control
(intro) Choose whether a quantity means skip or stop. ⟦B:tb1⟧
(definition) break exits the innermost enclosing for or while loop. ⟦B.f1 B:tb2⟧
(mechanism) continue skips the rest of the current body and proceeds to the next iteration. ⟦B.f2 B:tb3⟧
(mechanism) Put break or continue inside a loop conditional so it applies only when its condition holds. ⟦B.f3 B:tb3⟧
(example) Trace each quantity through the stop and skip conditions before adding it. The stop marker exits the loop; the skip value bypasses addition but permits another iteration. ⟦B.f1 B.f2 B.f3 B:tb4⟧
(misconception) continue skips this iteration’s remaining work; break exits the innermost loop. They are not interchangeable. ⟦B.f1 B.f2 B:tb5⟧
[CODE python]
total = 0
for quantity in [3, 0, 2, -1, 8]:
    if quantity == -1:
        break
    if quantity == 0:
        continue
    total = total + quantity
print(total)
  annotations: ['Exit this loop; later quantities are not processed.', 'Skip addition for this item, then proceed to the next iteration.', 'Add only when neither control condition applies.', 'Trace: 3 raises total to 3; 0 reaches continue and skips addition; 2 raises total to 5; -1 reaches break and exits the loop, so 8 is never processed.']

### s05 · check · Check loop control
Quick check — Decide where break should stop the loop and continue should skip an item.
QUESTION [choice, core, grading=client] A quantity loop must stop at -1 and skip zero before adding to total. Which arrangement fits?
  ✔ a: if quantity == -1: break; if quantity == 0: continue; then add.
      why: Correct. if quantity == -1: break; if quantity == 0: continue; then add.
  ✘ b: if quantity == -1: continue; if quantity == 0: break; then add.
      why: The stop and skip actions are reversed.
  ✘ c: Add first, then test break and continue.
      why: Placing the addition first does not let the zero bypass it or the stop value end processing before addition.
  feedback✔: Correct. if quantity == -1: break; if quantity == 0: continue; then add.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r03
  MEASURES: B:use_conditional_break_for_early_exit(f1,f3); B:use_conditional_continue_for_selective_skipping(f2,f3)   anchors=['assessment:use_conditional_break_for_early_exit', 'assessment:use_conditional_continue_for_selective_skipping']
  taught-before-tested: B.f1←s04; B.f3←s04; B.f2←s04; B.f3←s04

### s06 · check · Check loop control
Quick check — Decide whether the supplied control statement ends the loop or skips only the current iteration.
QUESTION [choice, core, grading=client] Which statement correctly contrasts break and continue?
  ✔ a: break exits the innermost loop; continue skips the rest of the current iteration.
      why: Correct. break exits the innermost loop; continue skips the rest of the current iteration.
  ✘ b: Both end the entire loop.
      why: continue advances to the next iteration instead of exiting the loop.
  ✘ c: break skips only the current iteration; continue exits the loop.
      why: This reverses the distinct effects.
  feedback✔: Correct. break exits the innermost loop; continue skips the rest of the current iteration.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: B:distinguish_loop_exit_from_iteration_skipping(f1,f2)   anchors=['assessment:distinguish_loop_exit_from_iteration_skipping']
  taught-before-tested: B.f1←s04; B.f2←s04

### s07 · hands_on · Practice loop control
Practice — Write a loop that searches [3, 0, 2, -1, 8] for the target -1, breaking as soon as it is found. Treat zero as an invalid entry and skip it with continue. Add other quantities to total.
QUESTION [code_exercise, core, grading=client] Initialize total by assigning zero to total before the supplied loop. Keep the loop and its input assignments unchanged. The checker reads total and the final quantity.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['integer literals', 'list literals', 'variable assignment', 'for quantity in a list', 'if conditions', '== comparisons', 'addition with +', 'break', 'continue'] blocked=9 items
  file main.py [editable]:
quantities = [3, 0, 2, -1, 8]
stop_value = -1
skip_value = 0
zero = 0
for quantity in quantities:
    if quantity == stop_value:
        break
    if quantity == skip_value:
        continue
    total = total + quantity

  SOLUTION main.py:
quantities = [3, 0, 2, -1, 8]
stop_value = -1
skip_value = 0
zero = 0
total = zero
for quantity in quantities:
    if quantity == stop_value:
        break
    if quantity == skip_value:
        continue
    total = total + quantity

  test t0 (value_equals, visible=True): {"expr":"[total, quantity]","expected":[5,-1]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"34f70a611582d9848d763079cd36d1c32408fa91b969e15395bf20cf198fa236","tests_passed":1}
  feedback✔: The result meets the task. Zero bypasses the addition, -1 ends the loop immediately, and 8 is never processed. The final value of total is 5.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Initialize total before the loop. Trace stop before skip before addition: -1 exits, zero bypasses addition, and later items after the stop are not processed.']
  MEASURES: B:use_conditional_break_for_early_exit(f1,f3); B:use_conditional_continue_for_selective_skipping(f2,f3); B:distinguish_loop_exit_from_iteration_skipping(f1,f2)   anchors=['practice']
  taught-before-tested: B.f1←s04; B.f3←s04; B.f2←s04; B.f3←s04; B.f1←s04; B.f2←s04

### s08 · explainer · Iterating Collections
(intro) Decide whether the order loop needs keys or key-value pairs. ⟦C:tb1⟧
(definition) Use for item in collection: with an indented body to visit successive elements. ⟦C.f1 C:tb2⟧
(mechanism) Lists and tuples are ordered sequences. ⟦C.f2 C:tb3⟧
(mechanism) Sets are unordered; their traversal is not positional sequence traversal. ⟦C.f3 C:tb3⟧
(mechanism) Direct dictionary iteration visits keys. ⟦C.f4 C:tb3⟧
(mechanism) for key, value in mapping.items(): visits each dictionary key-value pair together. ⟦C.f5 C:tb3⟧
(example) In direct quantities traversal, label binds a key. In quantities.items() traversal, label and quantity bind the key and associated value together. Read the collection type before assuming what an item means. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4⟧
(misconception) Direct dictionary iteration does not yield values or key-value pairs. Use quantities.items() when both the label and its quantity are needed. ⟦C.f4 C.f5 C:tb5⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
for label in quantities:
    print(label)
for label, quantity in quantities.items():
    print(label, quantity)
  annotations: ['Direct traversal binds label to each key.', 'items() binds the key and associated value together.']

### s09 · check · Check iterating collections
Quick check — Decide which traversal respects list and tuple order without assuming positions in a set.
QUESTION [choice, core, grading=client] Which traversal expectation is justified for lists, tuples and sets?
  ✔ a: Lists and tuples follow sequence order; sets have no positional sequence order.
      why: Correct. Lists and tuples follow sequence order; sets have no positional sequence order.
  ✘ b: All three guarantee the same positional traversal.
      why: Sets are unordered rather than positional sequences.
  ✘ c: Lists and tuples are unordered, but sets are positional.
      why: This reverses the sequence/set distinction.
  feedback✔: Correct. Lists and tuples follow sequence order; sets have no positional sequence order.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r05
  MEASURES: C:iterate_list_and_tuple_elements_in_sequence_order(f1,f2); C:iterate_set_elements_without_assuming_positions(f1,f3)   anchors=['assessment:iterate_list_and_tuple_elements_in_sequence_order', 'assessment:iterate_set_elements_without_assuming_positions']
  taught-before-tested: C.f1←s08; C.f2←s08; C.f1←s08; C.f3←s08

### s10 · check · Check iterating collections
Quick check — Decide which values direct iteration over the dictionary supplies.
QUESTION [choice, core, grading=client] What does for label in quantities visit when quantities is a dictionary?
  ✔ a: Its keys.
      why: Correct. Its keys.
  ✘ b: Its values.
      why: Direct dictionary iteration visits keys; it does not directly yield values.
  ✘ c: Its key-value pairs.
      why: Use items() to visit pairs together; direct iteration yields keys.
  feedback✔: Correct. Its keys.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: C:iterate_dictionary_keys_directly(f1,f4)   anchors=['assessment:iterate_dictionary_keys_directly']
  taught-before-tested: C.f1←s08; C.f4←s08

### s11 · hands_on · Practice iterating collections
Practice — Write a loop over quantities.items() that binds each pair to label and quantity, then assigns quantity + 1 to quantities[label].
QUESTION [code_exercise, core, grading=client] Assign input_quantities to quantities before the supplied items() loop. Keep the loop unchanged; it updates each existing key by requested_increment without console output.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment', 'string literals', 'integer literals', 'dictionary literals', 'for label, quantity in quantities.items():', 'indented loop body', 'dictionary subscription with quantities[label]', 'assignment to an existing dictionary key', 'integer addition with +'] blocked=10 items
  file main.py [editable]:
input_quantities = {"notebook": 3, "pen": 2}
requested_increment = 1
for label, quantity in quantities.items():
    quantities[label] = quantity + requested_increment

  SOLUTION main.py:
input_quantities = {"notebook": 3, "pen": 2}
requested_increment = 1
quantities = input_quantities
for label, quantity in quantities.items():
    quantities[label] = quantity + requested_increment

  test t0 (value_equals, visible=True): {"expr":"quantities","expected":{"notebook":4,"pen":3}} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"44bb0090e79e97e231ba7cc2c6de5aad46207eb45776ff7c9c90038cdf70291a","tests_passed":1}
  feedback✔: The result meets the task. The loop visits both key-value pairs and updates the existing quantities to {"notebook": 4, "pen": 3}, without adding or removing keys or using console output.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Bind quantities before items() is called. The supplied loop binds each key and value together and replaces only that existing key’s value.']
  MEASURES: C:iterate_dictionary_key_value_pairs(f1,f5)   anchors=['practice', 'assessment:iterate_dictionary_key_value_pairs']
  taught-before-tested: C.f1←s08; C.f5←s08

### s12 · explainer · Comprehensions
(intro) Build new collections from accepted source quantities. ⟦D:tb1⟧
(definition) [expression for item in iterable if condition] builds a new list by evaluating expression for accepted items. The condition is optional. ⟦D.f1 D:tb2⟧
(mechanism) {key_expression: value_expression for item in iterable} builds a dictionary of computed keys and values. An if clause can filter the source items. ⟦D.f3 D:tb3⟧
(example) Read each comprehension as source, optional filter and computed result. In the dictionary form, the colon separates key and value expressions. Items failing the filter contribute nothing. ⟦D.f1 D.f3 D:tb4⟧
(misconception) The condition selects source items; it is not a result value. The result expression computes what each accepted item contributes. ⟦D.f1 D.f3 D:tb5⟧
[CODE python]
quantities = [3, -1, 2]
doubled = [quantity * 2 for quantity in quantities if quantity > 0]
by_quantity = {quantity: quantity * 2 for quantity in quantities if quantity > 0}
print(doubled)
print(by_quantity)
  annotations: ['Source follows in; if selects; the leading expression computes each list item.', 'The expressions before and after the colon compute keys and values.']

### s13 · check · Check comprehensions
Quick check — Decide which list comprehension computes the intended results and applies the supplied filter.
QUESTION [choice, core, grading=client] Which list comprehension squares only even quantities?
  ✔ a: [quantity * quantity for quantity in quantities if quantity % 2 == 0]
      why: Correct. [quantity * quantity for quantity in quantities if quantity % 2 == 0]
  ✘ b: [quantity * quantity for quantity in quantities]
      why: Without the condition it also includes odd quantities.
  ✘ c: [quantity for quantity in quantities if quantity % 2 == 0]
      why: This filters even values but does not compute their squares.
  feedback✔: Correct. [quantity * quantity for quantity in quantities if quantity % 2 == 0]  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r08
  MEASURES: D:write_list_comprehension_with_optional_filter(f1)   anchors=['assessment:write_list_comprehension_with_optional_filter']
  taught-before-tested: D.f1←s12

### s14 · check · Check comprehensions
Quick check — Decide which dictionary comprehension creates the intended key-value pairs and applies the supplied filter.
QUESTION [choice, core, grading=client] Which form builds a dictionary mapping each label to a computed value?
  ✔ a: {label: expression for label in labels}
      why: Correct. {label: expression for label in labels}
  ✘ b: [expression for label in labels]
      why: Square brackets build a list, not key-value associations.
  ✘ c: {label: expression}
      why: This is a dictionary literal with one association, not iteration over all labels.
  feedback✔: Correct. {label: expression for label in labels}  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']
  MEASURES: D:write_dict_comprehension_with_optional_filter(f3)   anchors=['assessment:write_dict_comprehension_with_optional_filter']
  taught-before-tested: D.f3←s12

### s15 · hands_on · Practice comprehensions
Practice — Write a list comprehension that squares the even numbers in quantities.
QUESTION [code_exercise, stretch, grading=client] Keep the supplied input-dependent calculations unchanged. Assign computed_doubled to doubled. The checker reads doubled.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['variable assignment with =', 'integer literals, including negative integers', 'list literals', '[expression for quantity in quantities if condition]', 'multiplication with *', 'remainder with %', 'equality comparison with =='] blocked=13 items
  file main.py [editable]:
even_quantity = 2
quantities = [3, -1, even_quantity]
even_divisor = 2
zero = 0
computed_doubled = [quantity * quantity for quantity in quantities if quantity % even_divisor == zero]

  SOLUTION main.py:
even_quantity = 2
quantities = [3, -1, even_quantity]
even_divisor = 2
zero = 0
computed_doubled = [quantity * quantity for quantity in quantities if quantity % even_divisor == zero]
doubled = computed_doubled

  test t0 (value_equals, visible=True): {"expr":"[doubled, quantities]","expected":[[4],[3,-1,2]]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5d0699ddebde51915ab6ecc7cfa3d853d81f1602a9535e730c2d6241bcba0404","tests_passed":1}
  feedback✔: The result meets the task. The comprehension assigns doubled the value [4] when quantities is [3, -1, 2], excluding the odd numbers and squaring the accepted number.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Read the filter separately from the result expression: remainder equal to zero accepts an item, and quantity * quantity squares it. Bind the computed list to doubled.']
  MEASURES: D:write_list_comprehension_with_optional_filter(f1)   anchors=['practice']
  taught-before-tested: D.f1←s12

### s16 · recap · Takeaways
(takeaway) Initialize an accumulator once, then update it for each item. ⟦A.f1 A.f2 A:tb2 A:tb3⟧
(takeaway) continue skips remaining work; break exits the innermost loop. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3⟧
(takeaway) Dictionary iteration visits keys; items() visits key-value pairs. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3⟧
(takeaway) Comprehensions separate source, optional filtering and computed results. ⟦D.f1 D.f3 D:tb2 D:tb3⟧
[UP NEXT] File Io: Read saved notebook orders with managed file opening.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit for loops
(definition) Write for item in sequence: with an indented body. Process successive sequence items in their order. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(definition) Initialize total = 0 before the loop. Inside, use total = total + item to accumulate numeric items. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Initializing total in the body would discard earlier additions; initialize once before the loop. ⟦A.f2 A:tb1 A:tb3 A:tb4 A:tb5⟧
[CODE python]
quantities = [3, 2, 5]
total = 0
for quantity in quantities:
    total = total + quantity
print(total)
  annotations: []
### r02 · Revisit for loops
(definition) Write for item in sequence: with an indented body. Process successive sequence items in their order. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(misconception) The body processes each successive sequence item, not the entire sequence as one item. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
[CODE python]
quantities = [3, 2, 5]
total = 0
for quantity in quantities:
    total = total + quantity
print(total)
  annotations: []
### r03 · Revisit loop control
(definition) break exits the innermost enclosing for or while loop. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) continue skips the rest of the current body and proceeds to the next iteration. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(definition) Put break or continue inside a loop conditional so it applies only when its condition holds. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) break exits the innermost loop; continue only skips the current body’s remaining work. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
[CODE python]
total = 0
for quantity in [3, 0, 2, -1, 8]:
    if quantity == -1:
        break
    if quantity == 0:
        continue
    total = total + quantity
print(total)
  annotations: []
### r04 · Revisit loop control
(definition) break exits the innermost enclosing for or while loop. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(definition) continue skips the rest of the current body and proceeds to the next iteration. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) break exits the innermost loop; continue only skips the current body’s remaining work. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
[CODE python]
total = 0
for quantity in [3, 0, 2, -1, 8]:
    if quantity == -1:
        break
    if quantity == 0:
        continue
    total = total + quantity
print(total)
  annotations: []
### r05 · Revisit iterating collections
(definition) Use for item in collection: with an indented body to visit successive elements. ⟦C.f1 C:tb2 C:tb4⟧
(definition) Lists and tuples are ordered sequences. ⟦C.f2 C:tb3 C:tb4⟧
(definition) Sets are unordered; their traversal is not positional sequence traversal. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) Lists and tuples have sequence order; set traversal is not positional. ⟦C.f3 C:tb3 C:tb4⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
for label in quantities:
    print(label)
for label, quantity in quantities.items():
    print(label, quantity)
  annotations: []
### r06 · Revisit iterating collections
(definition) Use for item in collection: with an indented body to visit successive elements. ⟦C.f1 C:tb2 C:tb4⟧
(definition) Direct dictionary iteration visits keys. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Direct dictionary traversal visits keys, not associated values. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
for label in quantities:
    print(label)
for label, quantity in quantities.items():
    print(label, quantity)
  annotations: []
### r07 · Revisit iterating collections
(definition) Use for item in collection: with an indented body to visit successive elements. ⟦C.f1 C:tb2 C:tb4⟧
(definition) for key, value in mapping.items(): visits each dictionary key-value pair together. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
(misconception) Use items() to bind each label and quantity together; direct traversal binds only keys. ⟦C.f5 C:tb3 C:tb4 C:tb5⟧
[CODE python]
quantities = {"notebook": 3, "pen": 2}
for label in quantities:
    print(label)
for label, quantity in quantities.items():
    print(label, quantity)
  annotations: []
### r08 · Revisit comprehensions
(definition) [expression for item in iterable if condition] builds a new list by evaluating expression for accepted items. The condition is optional. ⟦D.f1 D:tb2 D:tb4 D:tb5⟧
(misconception) The condition selects quantities; the result expression computes list items. The condition is not itself the result. ⟦D.f1 D:tb2 D:tb4 D:tb5⟧
[CODE python]
quantities = [3, -1, 2]
doubled = [quantity * 2 for quantity in quantities if quantity > 0]
by_quantity = {quantity: quantity * 2 for quantity in quantities if quantity > 0}
print(doubled)
print(by_quantity)
  annotations: []
### r09 · Revisit comprehensions
(definition) {key_expression: value_expression for item in iterable} builds a dictionary of computed keys and values. An if clause can filter the source items. ⟦D.f3 D:tb3 D:tb4 D:tb5⟧
(misconception) The colon separates computed keys from computed values; the optional condition only filters source items. ⟦D.f3 D:tb3 D:tb4 D:tb5⟧
[CODE python]
quantities = [3, -1, 2]
doubled = [quantity * 2 for quantity in quantities if quantity > 0]
by_quantity = {quantity: quantity * 2 for quantity in quantities if quantity > 0}
print(doubled)
print(by_quantity)
  annotations: []
### r10 · Revisit comprehensions
(definition) [expression for item in iterable if condition] builds a new list by evaluating expression for accepted items. The condition is optional. ⟦D.f1 D:tb2 D:tb4 D:tb5⟧
(definition) {key_expression: value_expression for item in iterable} builds a dictionary of computed keys and values. An if clause can filter the source items. ⟦D.f3 D:tb3 D:tb4 D:tb5⟧
(misconception) The condition selects quantities; the result expression computes list items. The condition is not itself the result. ⟦D.f1 D:tb2 D:tb4 D:tb5⟧
[CODE python]
quantities = [3, -1, 2]
doubled = [quantity * 2 for quantity in quantities if quantity > 0]
by_quantity = {quantity: quantity * 2 for quantity in quantities if quantity > 0}
print(doubled)
print(by_quantity)
  annotations: []

=========

# EVALUATOR PACKET — File Io (learn_python.tile.025_025)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.file_io — File Io

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: learn_python.tile.025_025.s01: prose block without lineage.fact_ids
  warn: learn_python.tile.025_025.s04/ix.learn_python.tile.025_025.s04: ADVISORY — syntax descriptors with no detector: ['assert', 'finally', 'indented body under with open', 'keyword arguments', 'open modes other than "r" and "w"', 'pathlib', 'string literals', 'yield']

## SOURCE FACTS — A (python.file_io)   objective: Read and write text and CSV files from Python using open() and the csv module.
A.f1: open(path, mode) returns a file object; r reads and w writes, replacing existing contents.   [sources: python_tutorial#inputoutput.html#reading-and-writing-files]
A.f2: Use with open(path, mode) as f: followed by an indented body so that f is closed after use.   [sources: python_tutorial#inputoutput.html#reading-and-writing-files]
A.f3: f.read() reads the remaining contents; f.write(text) writes text through a text-mode file object.   [sources: python_tutorial#inputoutput.html#methods-of-file-objects]
A.f4: Without managed opening, call f.close() when finished.   [sources: python_tutorial#inputoutput.html#methods-of-file-objects]
A.f5: Open a CSV file with newline="" for the CSV reader.   [sources: python_stdlib_reference#csv.html#csv.reader]
A.f6: csv.DictReader(f) produces row dictionaries using the first row as keys by default, excluding that header row from results; list(csv.DictReader(f)) collects those rows.   [sources: python_stdlib_reference#csv.html#csv.DictReader]
note: Begin with this objective: Read and write text and CSV files from Python using open() and the csv module.
note: Keep the example in the Text and CSV file I/O tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.collection_selection, python.console_input_output, python.enumerate_iteration.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Import csv and use with open("orders.csv", "r", newline="") as source: to collect the CSV data rows into rows using list(csv.DictReader(source)).  SUCCESS: rows contains one dictionary with label equal to "notebook" and quantity equal to "3". The header is not included as a data row, and the file is closed after the indented body.
ASSESSMENT ANCHOR: select_read_or_write_mode facts=['f1']
ASSESSMENT ANCHOR: close_file_resources_after_use facts=['f2', 'f4']
ASSESSMENT ANCHOR: read_and_write_text_file_contents facts=['f3']
ASSESSMENT ANCHOR: collect_csv_rows_as_dictionaries facts=['f5', 'f6']

## DATA ASSETS USED
ds.orders: orders.csv — columns: label(categorical), quantity(numerical)
   ["notebook",3]
   variant v.orders.pen: 2 ops; planted: 
   variant v.orders.changed_quantity: 2 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing and updating nested collections; Avoiding unintended mutations through shared references; Checking for None with identity; Choosing a built-in collection; Continuing expressions across lines; Counting values with collections.Counter; Distinguishing syntax and runtime errors; Documenting Python interfaces with docstrings; Encoding and decoding Unicode text and bytes; Enumerate iteration; Floating-point approximation limits; Indentation and code blocks; Inspecting program state with diagnostic printing; Nested loops; Python comments; Python interpreter execution model; Reading and displaying console values; Running Python interactively; Running Python scripts; Statements and expressions; Transforming text with string methods; Truth-value testing; Using math for numeric calculations; Using range for counted iteration; Zip iteration

## LESSON, in learner order

### s01 · explainer · File Io
(intro) Read saved notebook orders with managed file opening. ⟦A:tb1⟧
(definition) open(path, mode) returns a file object. r reads; w writes and replaces existing contents. ⟦A.f1 A:tb2⟧
(mechanism) with open(path, mode) as f: uses an indented body and closes f after use. ⟦A.f2 A:tb3⟧
(mechanism) f.read() reads remaining contents. f.write(text) writes text through a text-mode file object. ⟦A.f3 A:tb3⟧
(mechanism) Without managed opening, call f.close() when finished. ⟦A.f4 A:tb3⟧
(mechanism) Open CSV input with newline="" for the reader. ⟦A.f5 A:tb3⟧
(mechanism) By default, csv.DictReader(f) uses the first row as dictionary keys, not a result row. list(csv.DictReader(f)) collects the row dictionaries. ⟦A.f6 A:tb3⟧
[TABLE ds.orders cols=['label', 'quantity'] ] caption: 
[CODE python]
import csv
with open("orders.csv", "r", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows)
  annotations: ['Read the CSV with newline handling and managed closure.', 'Collect data-row dictionaries using the header keys.', 'Outside the managed body, the file is closed.']

### s02 · explainer · File Io
(example) In orders.csv, the header supplies label and quantity keys. DictReader returns CSV field text, including numeric-looking quantity text. The managed body collects rows; the file is closed afterward. For text, read remaining contents or write text through the file object. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb4⟧
(misconception) w replaces existing contents; it is not a reading mode. The CSV header supplies keys by default, rather than appearing as a returned data row. ⟦A.f1 A.f6 A:tb5⟧

### s03 · check · Check file io
Quick check — Decide which file-opening mode matches the supplied reading or writing task.
QUESTION [choice, intro, grading=client] Which group reads existing text, writes replacement text, and closes an unmanaged file, respectively?
  ✔ a: open(path, "r") followed by f.read(); open(path, "w") followed by f.write(text); f.close()
      why: Mode "r" opens for reading with read(); mode "w" opens for replacement writing with write(text); close() releases the unmanaged file.
  ✘ b: open(path, "w") followed by f.read(); open(path, "r") followed by f.write(text); f.close()
      why: The modes are swapped: "w" is for writing, not read(), and "r" is for reading, not write(text). f.close() is the correct closure operation.
  ✘ c: f.write(text); f.read(); leave the unmanaged file open
      why: write(text) writes rather than reads, and read() reads rather than writes. An unmanaged file must be closed after use, not left open.
  feedback✔: Mode "r" opens for reading with read(); mode "w" opens for replacement writing with write(text); close() releases the unmanaged file.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Distinguish the requested operation from the similar-looking alternatives.']  remediation→r01
  MEASURES: A:select_read_or_write_mode(f1); A:read_and_write_text_file_contents(f3)   anchors=['assessment:select_read_or_write_mode', 'assessment:read_and_write_text_file_contents']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · hands_on · Practice file io
Practice — Import csv and use with open("orders.csv", "r", newline="") as source: to collect the CSV data rows into rows using list(csv.DictReader(source)).
QUESTION [code_exercise, stretch, grading=client] Keep the supplied managed read and copy blocks unchanged. After the DictReader block assign parsed_rows to rows. Before the copy blocks, assign csv_text to written_text. The checker verifies rows, source closure and matching copied text.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import csv', 'with open("orders.csv", "r", newline="") as source:', 'indented body under with open', 'variable assignment', 'list(csv.DictReader(source))', 'string literals', 'keyword arguments'] blocked=12 items
  file main.py [editable]:
import csv
with open("orders.csv", "r", newline="") as text_source:
    csv_text = text_source.read()
with open("orders.csv", "r", newline="") as source:
    parsed_rows = list(csv.DictReader(source))
written_text = ""
with open("copy.txt", "w", newline="") as destination:
    destination.write(written_text)
with open("copy.txt", "r", newline="") as copied_source:
    copied_text = copied_source.read()

  SOLUTION main.py:
import csv
with open("orders.csv", "r", newline="") as text_source:
    csv_text = text_source.read()
with open("orders.csv", "r", newline="") as source:
    parsed_rows = list(csv.DictReader(source))
rows = parsed_rows
written_text = csv_text
with open("copy.txt", "w", newline="") as destination:
    destination.write(written_text)
with open("copy.txt", "r", newline="") as copied_source:
    copied_text = copied_source.read()

  test t0 (value_equals, visible=True): {"expr":"[rows, source.closed]","expected":[[{"label":"notebook","quantity":"3"}],true]} | on-fail: Check the required computation and the named output; keep the supplied inputs.
  test t1 (value_equals, visible=True): {"expr":"[copied_text == csv_text, rows]","expected":[true,[{"label":"notebook","quantity":"3"}]]} | on-fail: Reuse the original text for writing and the parsed dictionaries for rows.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5454b65a4f2c5ec9308fc102e8dae0b38b59b442e23431b36c2d5fa60c864a76","tests_passed":2}
  feedback✔: The result meets the task. rows contains one dictionary with label equal to "notebook" and quantity equal to "3". The header is not included as a data row, and the file is closed after the indented body.  feedback✘: Revisit the stated rule and check the exact operation requested.  hints: ['Bind parsed_rows to rows after the managed reader closes source. Replace written_text’s empty placeholder with csv_text before the copy blocks.']  remediation→r02
  MEASURES: A:close_file_resources_after_use(f2,f4); A:collect_csv_rows_as_dictionaries(f5,f6); A:read_and_write_text_file_contents(f3)   anchors=['practice', 'assessment:close_file_resources_after_use', 'assessment:collect_csv_rows_as_dictionaries', 'assessment:read_and_write_text_file_contents']
  taught-before-tested: A.f2←s01; A.f4←s01; A.f5←s01; A.f6←s01; A.f3←s01

### s05 · recap · Takeaways
(takeaway) Choose file modes carefully; manage closure and CSV header handling. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3⟧
[UP NEXT] Collection selection: Next, choose a collection for a task.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit file io
(definition) open(path, mode) returns a file object. r reads; w writes and replaces existing contents. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) Reading uses r; w replaces existing contents rather than inspecting them. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
[CODE python]
import csv
with open("orders.csv", "r", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows)
  annotations: []
### r02 · Revisit file io
(definition) with open(path, mode) as f: uses an indented body and closes f after use. ⟦A.f2 A:tb3 A:tb4⟧
(definition) f.read() reads remaining contents. f.write(text) writes text through a text-mode file object. ⟦A.f3 A:tb3 A:tb4⟧
(definition) Without managed opening, call f.close() when finished. ⟦A.f4 A:tb3 A:tb4⟧
(definition) Open CSV input with newline="" for the reader. ⟦A.f5 A:tb3 A:tb4⟧
(definition) By default, csv.DictReader(f) uses the first row as dictionary keys, not a result row. list(csv.DictReader(f)) collects the row dictionaries. ⟦A.f6 A:tb3 A:tb4 A:tb5⟧
(misconception) The CSV header supplies keys by default; it is not returned as a data-row dictionary. ⟦A.f6 A:tb3 A:tb4 A:tb5⟧
[CODE python]
import csv
with open("orders.csv", "r", newline="") as source:
    rows = list(csv.DictReader(source))
print(rows)
  annotations: []

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: encoding argument to open()