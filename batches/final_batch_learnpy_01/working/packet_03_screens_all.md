# EVALUATOR PACKET — Variables Assignment / Core Data Types / Arithmetic Operators (learn_python.tile.000_002)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.variables_assignment — Variables Assignment
B = python.core_data_types — Core Data Types
C = python.arithmetic_operators — Arithmetic Operators

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Practice variables assignment
Practice — Assign quantity, unit_price and cost for a notebook purchase, then reassign cost using a computation involving quantity and unit_price.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Check core data types
Quick check — Decide whether the supplied expressions perform numeric addition or string concatenation, and identify the numeric result type.

### s09 · check · Check core data types
Quick check — Decide which Boolean results follow from the supplied numeric comparisons.

### s10 · hands_on · Practice core data types
Practice — Create int, float, str, and bool values in the notebook example and display each value’s type using print(type(...)). Use quantity, price, and label, then reuse quantity for a bool after inspecting its integer value.

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

### s13 · hands_on · Practice arithmetic operators
Practice — Compute derived values from numeric inputs using division, floor division, remainder and exponentiation, then compare calculations with and without parentheses.

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

=========

# EVALUATOR PACKET — Comparison Operators / Logical Operators / Type Conversion (learn_python.tile.003_005)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.comparison_operators — Comparison Operators
B = python.logical_operators — Logical Operators
C = python.type_conversion — Type Conversion

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Check comparison operators
Quick check — Decide which Boolean result the supplied quantity comparison produces.

### s04 · hands_on · Practice comparison operators
Practice — Create simple threshold checks for quantity: at least three, more than three, at most three, and less than three.

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

### s08 · check · Check logical operators
Quick check — Decide which grouping expresses the intended Boolean condition.

### s09 · hands_on · Practice logical operators
Practice — Create a multi-condition eligibility rule that is true only when both quantity_ok and budget_ok are true.

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

### s13 · check · Check type conversion
Quick check — Decide which name stores the conversion result and which retains its original value.

### s14 · hands_on · Practice type conversion
Practice — Convert the numeric string assigned to quantity_text to a float stored as quantity, then multiply quantity by price and assign the calculation result to price.

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

=========

# EVALUATOR PACKET — Conditional Statements / While Loops (learn_python.tile.006_007)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.conditional_statements — Conditional Statements
B = python.while_loops — While Loops

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice conditional statements
Practice — Write an if/elif/else chain that classifies a numeric score stored in quantity into three grade bands: A for scores at least 90, B for scores at least 70 but below 90, and C for scores below 70. Assign the selected band to grade.

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

### s07 · hands_on · Practice while loops
Practice — Write a while loop that keeps requesting a response until the user enters the accepted value "done".

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

=========

# EVALUATOR PACKET — Lists / Sets / Dictionaries (learn_python.tile.008_010)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.lists — Lists
B = python.sets — Sets
C = python.dictionaries — Dictionaries

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Check lists
Quick check — Decide how replacing an indexed item and appending an item change the list.

### s04 · hands_on · Practice lists
Practice — Create labels with the values "red", "blue", and "green" in that order, append "yellow", and assign labels[1:3] to a variable named selected_labels.

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

### s07 · hands_on · Practice sets
Practice — Convert the list assigned to first into a set to remove repeated labels, then test whether "red" belongs to first.

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

### s10 · check · Check dictionaries
Quick check — Decide whether each dictionary assignment adds a key or replaces its value.

### s11 · hands_on · Practice dictionaries
Practice — Build a dictionary mapping notebook and pen to prices of 3 and 2, then retrieve the notebook price using bracket lookup.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice string basics formatting
Practice — Compute a total from quantity and cost, then assign an f-string sentence to message with the total formatted to two decimal places.

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

=========

# EVALUATOR PACKET — Defining Calling Functions / Parameters Arguments / Return Values (learn_python.tile.012_014)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.defining_calling_functions — Defining Calling Functions
B = python.parameters_arguments — Parameters Arguments
C = python.return_values — Return Values

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice defining calling functions
Practice — Create a reusable helper named greet with an empty pair of parentheses and an indented body, then call it twice.

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

### s06 · hands_on · Practice parameters arguments
Practice — Parameterize a describe helper so its body builds a label from supplied label and quantity values rather than hard-coded values.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · check · Check return values
Quick check — Decide whether the helper returns a value or only displays one.

### s10 · hands_on · Practice return values
Practice — Make order_cost return quantity multiplied by price, then store the result of order_cost(3, 4.5) in cost.

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

=========

# EVALUATOR PACKET — Tuples / Function Default Keyword Args / Variable Scope (learn_python.tile.015_017)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.tuples — Tuples
B = python.function_default_keyword_args — Function Default Keyword Args
C = python.variable_scope — Variable Scope

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Check tuples
Quick check — Decide which unpacking assignment matches the tuple items to its targets.

### s04 · hands_on · Practice tuples
Practice — Write bounds(values) to return a tuple containing the minimum and maximum of a nonempty list, then unpack the result into smallest and largest.

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

### s07 · hands_on · Practice function default keyword args
Practice — Define cost(quantity, price, fee=2) to return quantity * price + fee. Call it once using only keyword arguments with fee=5, and once omitting fee to use its default. Assign each returned value to a variable.

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

### s11 · check · Check variable scope
Quick check — Decide which binding changes after local assignment or assignment with a global declaration.

### s12 · hands_on · Practice variable scope
Practice — Write show() so it reads the module-level quantity through globals()["quantity"], assigns that value to a local quantity, increases the local quantity by 2, and returns it without changing the module-level quantity.

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

=========

# EVALUATOR PACKET — Error Handling (learn_python.tile.018_018)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.error_handling — Error Handling

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Check error handling
Quick check — Trace whether each exception matches the handler and which path follows.

### s04 · hands_on · Practice error handling
Practice — Attempt to convert the supplied text into a numeric quantity. Handle ValueError by assigning a friendly recovery message to text instead of displaying it.

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

=========

# EVALUATOR PACKET — Import Statements (learn_python.tile.019_019)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.import_statements — Import Statements

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice import statements
Practice — Import the math module, call math.cos with value as its argument, and assign the returned value back to value.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Practice pep 8 style
Practice — Rewrite a working but poorly styled order-cost function using lowercase underscore-separated names, four-space indentation, and appropriate punctuation and operator spacing without changing its calculation.

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

=========

# EVALUATOR PACKET — For Loops / Loop Control / Iterating Collections / Comprehensions (learn_python.tile.021_024)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.for_loops — For Loops
B = python.loop_control — Loop Control
C = python.iterating_collections — Iterating Collections
D = python.comprehensions — Comprehensions

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practice for loops
Practice — Write a for loop that sums the values in quantities = [3, 2, 5], initializing total before the loop and updating it for each quantity.

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

### s06 · check · Check loop control
Quick check — Decide whether the supplied control statement ends the loop or skips only the current iteration.

### s07 · hands_on · Practice loop control
Practice — Write a loop that searches [3, 0, 2, -1, 8] for the target -1, breaking as soon as it is found. Treat zero as an invalid entry and skip it with continue. Add other quantities to total.

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

### s10 · check · Check iterating collections
Quick check — Decide which values direct iteration over the dictionary supplies.

### s11 · hands_on · Practice iterating collections
Practice — Write a loop over quantities.items() that binds each pair to label and quantity, then assigns quantity + 1 to quantities[label].

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

### s14 · check · Check comprehensions
Quick check — Decide which dictionary comprehension creates the intended key-value pairs and applies the supplied filter.

### s15 · hands_on · Practice comprehensions
Practice — Write a list comprehension that squares the even numbers in quantities.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Practice file io
Practice — Import csv and use with open("orders.csv", "r", newline="") as source: to collect the CSV data rows into rows using list(csv.DictReader(source)).

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