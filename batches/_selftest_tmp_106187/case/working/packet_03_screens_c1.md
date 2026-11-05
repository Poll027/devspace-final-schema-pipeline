# EVALUATOR PACKET — Comparison and Logical Operators (tile_python_operators_conversion)
Tile summary: Learn Python's arithmetic, comparison and logical operators, understand short-circuit evaluation and operator priority, and convert values between int, float and str.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.arithmetic_operators — Arithmetic operators
B = python.comparison_operators — Comparison operators
C = python.logical_operators — Logical operators
D = python.type_conversion — Type conversion/casting

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.arithmetic_operators)   objective: Apply Python's arithmetic operators (+, -, *, /, //, %, **) to combine numeric values into a derived result.
A.f1: The operators +, -, * and / perform addition, subtraction, multiplication and division; division (/) always returns a float.   [sources: python_docs_tutorial_introduction#numbers]
A.f2: The // operator performs floor division, discarding the fractional part, and the % operator returns the remainder of the division.   [sources: python_docs_tutorial_introduction#numbers]
A.f3: The ** operator calculates a power, e.g. 5 ** 2 is 5 squared.   [sources: python_docs_tutorial_introduction#numbers]
A.f4: Parentheses can be used to group an expression and control how it is evaluated.   [sources: python_docs_tutorial_introduction#numbers]
A.f5: Operators with mixed int/float operands convert the integer operand to floating point, e.g. 4 * 3.75 - 1 evaluates to 14.0.   [sources: python_docs_tutorial_introduction#numbers]
note: Keep this tight -- reference tier, one line per operator group.
PRACTICE ANCHOR (live_code): Compute derived values from numeric inputs using the arithmetic operators, for example a total, an average-style quotient and a remainder.  SUCCESS: Each derived value prints the correct number, with / giving a float and // and % giving the quotient and remainder.
ASSESSMENT ANCHOR: choose_arithmetic_operator facts=['f1']
ASSESSMENT ANCHOR: use_floor_division_and_remainder facts=['f2']
ASSESSMENT ANCHOR: use_power_operator facts=['f3']
ASSESSMENT ANCHOR: predict_grouped_and_mixed_type_result facts=['f4', 'f5']

## SOURCE FACTS — B (python.comparison_operators)   objective: Write comparisons between Python values using <, <=, >, >=, == and != so each evaluates to the boolean result a task requires.
B.f1: The standard comparison operators are <, <=, >, >=, == and !=.   [sources: python_docs_tutorial_introduction#first-steps-towards-programming]
B.f2: A comparison evaluates to a boolean value: True or False, e.g. 3 < 5 is True.   [sources: python_official_docs#reference/expressions.html#comparisons]
note: Skip chained comparisons (optional f3) unless there's room -- it's enrichment, not required.
PRACTICE ANCHOR (live_code): Write simple threshold checks that compare a number to a limit and print the True or False result.  SUCCESS: Each check prints True or False correctly for values below, at and above the threshold.
ASSESSMENT ANCHOR: write_comparison_expression facts=['f1', 'f2']
ASSESSMENT ANCHOR: predict_boolean_result_of_comparison facts=['f2']

## SOURCE FACTS — C (python.logical_operators)   objective: Combine comparisons and boolean conditions using and, or, and not to express compound rules.
C.f1: The Boolean operations, in ascending priority, are or, and, and not.   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
C.f2: x or y evaluates to x if x is true, otherwise to y, and is a short-circuit operator that only evaluates y if x is false.   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
C.f3: x and y evaluates to x if x is false, otherwise to y, and is a short-circuit operator that only evaluates y if x is true.   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
C.f4: not x evaluates to True if x is false, else False; not has a lower priority than the comparison operators, so not a == b is interpreted as not (a == b).   [sources: python_docs_stdtypes#boolean-operations-and-or-not]
note: Keep is_late/is_far as the running example throughout -- don't introduce a third condition.
note: No video was approved for this concept (every candidate clip was rejected), so the text carries all four facts alone.
PRACTICE ANCHOR (live_code): Write a rule that combines comparisons with and, or and not and print whether a sample delivery meets it, using is_late and is_far as the condition variables.  SUCCESS: The compound expression prints the expected True or False for sample values of is_late and is_far, including a case where the priority of and over or matters.
ASSESSMENT ANCHOR: predict_operator_priority facts=['f1', 'f4']
ASSESSMENT ANCHOR: predict_short_circuit_result facts=['f2', 'f3']
ASSESSMENT ANCHOR: write_compound_boolean_expression facts=['f1', 'f2', 'f3', 'f4']

## SOURCE FACTS — D (python.type_conversion)   objective: Convert a value from one core type to another using int(), float(), or str(), and recognize when a conversion is invalid.
D.f1: The constructors int() and float() can be used to produce a number of a specific type from another value.   [sources: python_docs_stdtypes#numeric-types-int-float-complex]
D.f2: int(string) returns an integer object constructed from a string, e.g. int('123') returns 123.   [sources: python_docs_library_functions#int]
D.f3: float(string) returns a floating-point number constructed from a string, e.g. float('+1.23') returns 1.23.   [sources: python_docs_library_functions#float]
D.f4: Strings may also be created from other objects using the str constructor.   [sources: python_docs_stdtypes#text-sequence-type-str]
D.f5: float(string) requires the string to conform to a specific numeric format (an optional sign and digits, optionally with a decimal point or exponent, after surrounding whitespace is removed); not every string can be converted this way.   [sources: python_docs_library_functions#float]
D.f6: A string that isn't in the format the target type accepts (for int(), an integer string) raises a ValueError, e.g. int('3.5').   [sources: python_docs_library_functions#int, python_docs_tutorial_errors#handling-exceptions]
note: TOC conflict: the assessment_target mentions 'handling conversion errors', but try/except is taught later in python.error_handling. The assessment anchors cover recognizing when a conversion raises a ValueError, not handling it.
PRACTICE ANCHOR (live_code): Take a numeric string, convert it to a float and use it in a calculation.  SUCCESS: The string is converted with float() and the calculation prints a numeric result.
ASSESSMENT ANCHOR: convert_value_to_target_type facts=['f1', 'f2', 'f3', 'f4']
ASSESSMENT ANCHOR: recognize_invalid_conversion facts=['f5', 'f6']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparison operators; Control flow: if/elif/else; Core data structure: dictionaries; Core data structure: lists; Core data structure: sets; Core data structure: tuples; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); For loops; Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Iterating over data structures; List and dict comprehensions; Logical operators; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Return values; String basics and f-string formatting; Type conversion/casting; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Seven operators for numeric work  [reward 5]
Arithmetic operators — Python gives you seven arithmetic operators — including two you may not have seen before.
(definition) Python provides seven arithmetic operators for numeric work. The familiar four — + (addition), - (subtraction), * (multiplication) and / (division) — work as expected, but / always returns a float even when both operands are whole numbers: 8 / 2 gives 4.0, not 4. The ** operator raises a number to a power: 5 ** 2 is 25. ⟦A.f1 A.f3 A:tb1⟧
[SIDE_BY_SIDE] 17 // 5 is 3 and 17 % 5 is 2; parentheses control evaluation order; mixing int and float promotes the result to float. left_label: // and % | right_label: Grouping and mixed types
  left:
[CODE python]
17 // 5   # floor division
17 % 5    # remainder
  annotations: ['Result: 3 (fractional part discarded)', "Result: 2 (what's left over)"]
  right:
[CODE python]
(32 + 8) * 2    # parentheses group first
4 * 3.75 - 1    # int promoted to float
  annotations: ['Result: 80 — parentheses force addition before multiplication', 'Result: 14.0 — mixed int/float gives float']

### s02 · check · Predict the result of a grouped, mixed-type expression  [reward 10]
Quick check — Can you work out what Python evaluates when parentheses and a float are involved?

### s03 · hands_on · Use arithmetic operators on delivery data  [reward 15]
Practice — Apply +, -, *, /, //, % and ** to compute delivery metrics.

### s04 · explainer · Six operators that return True or False  [reward 5]
Comparison operators — Comparisons turn a question about data into a boolean value Python can branch on.
(definition) Comparing two values is how a question like 'is this delivery late?' becomes something Python can act on. The six comparison operators are < (less than), <= (less than or equal), > (greater than), >= (greater than or equal), == (equal) and != (not equal). Every comparison evaluates to exactly one of the two boolean values: True or False. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
[SIDE_BY_SIDE] Each operator returns True or False; delivery_minutes > 60 is True for a 72-minute order and False for a 32-minute one. left_label: Greater-than family | right_label: Less-than family and !=
  left:
[CODE python]
delivery_minutes > 60
delivery_minutes >= 60
delivery_minutes == 60
  annotations: ['True if over 60 minutes', 'True if 60 or more', 'True only if exactly 60']
  right:
[CODE python]
delivery_minutes < 60
delivery_minutes <= 60
city != 'Lagos'
  annotations: ['True if under 60 minutes', 'True if 60 or fewer', 'True for any city other than Lagos']

### s05 · check · Choose the right comparison operator  [reward 10]
Quick check — Pick the operator that expresses the condition described.

### s06 · check · Predict the boolean result of a comparison  [reward 10]
Quick check — Given a value and an operator, what does the expression evaluate to?

### s07 · hands_on · Write comparison expressions for delivery data  [reward 15]
Practice — Use the six comparison operators to filter and flag orders.

### s08 · explainer · Combining conditions with and, or and not  [reward 5]
Logical operators — Build compound conditions from simpler comparisons using Python's three logical operators.
(intro) A single comparison asks one question at a time. To combine conditions — 'is this delivery both late and far from the depot?' — Python provides three logical operators: or, and and not. In ascending priority order they are: or (lowest), and, not (highest among the three). When there are no parentheses, and binds more tightly than or, so is_late or is_far and is_first_week groups as is_late or (is_far and is_first_week). ⟦C.f1 C:tb1 C:tb2⟧
(mechanism) x or y returns x if x is true, otherwise y. It is short-circuit: if is_late is True, Python never evaluates is_far. x and y returns x if x is false, otherwise y. It is also short-circuit: if is_late is False, Python skips is_far entirely. ⟦C.f2 C.f3 C:tb3 C:tb4⟧
[SIDE_BY_SIDE] or is true when at least one operand is true; and is true only when both are; both short-circuit to skip the second operand when the result is already determined. left_label: or — true if either | right_label: and — true only if both
  left:
[CODE python]
is_late or is_far
True or False
False or True
False or False
  annotations: ['True if either condition holds', 'True — first operand is true', 'True — second operand is true', 'False — neither is true']
  right:
[CODE python]
is_late and is_far
True and True
True and False
False and True
  annotations: ['True only if both conditions hold', 'True — both are true', 'False — second is false', 'False — first is false, short-circuits']

### s09 · explainer · not, priority and real-world compound conditions  [reward 5]
Logical operators — not flips a boolean; priority rules determine how mixed expressions group without parentheses.
(mechanism) not x flips the boolean: not is_late is True when is_late is False, and False when is_late is True. not has lower priority than the comparison operators, so not delivery_minutes == 0 is read as not (delivery_minutes == 0), not as (not delivery_minutes) == 0. ⟦C.f4 C:tb5⟧
(example) A rule like 'flag this delivery if it is late or unusually far' reads directly as is_late or is_far. A stricter rule — 'flag it only if it is late and it is the driver's first week' — reads as is_late and is_first_week. and, or and not let you build one compound condition out of several simpler comparisons. ⟦C.f2 C.f3 C:tb6⟧

### s10 · check · Predict operator priority in a mixed expression  [reward 10]
Quick check — How does Python group an expression that mixes and and or without parentheses?

### s11 · check · Predict the result of a short-circuit expression  [reward 10]
Quick check — Which operand does Python evaluate when the first one already decides the outcome?

### s12 · hands_on · Write compound boolean expressions  [reward 15]
Practice — Combine comparisons with and, or and not to express multi-condition rules.

### s13 · explainer · Converting between strings and numbers  [reward 5]
Type conversion — int(), float() and str() let you move values between types — but only when the format matches.
(intro) Data often arrives as the wrong type. A delivery time typed into a form as the text '32' cannot be used in arithmetic until it is converted to a number. Python provides three constructors for explicit conversion: int() and float() produce a number from a string or another numeric type, and str() turns any value into its string representation. ⟦D.f1 D.f4 D:tb1 D:tb4⟧
(mechanism) int('123') returns the integer 123. float('+1.23') returns the float 1.23. str(32) turns the integer 32 into the string '32'. These conversions work in both directions between numbers and their string representations. ⟦D.f2 D.f3 D.f4 D:tb2 D:tb3 D:tb4⟧
(misconception) Not every string can be converted. float() requires the string to match a numeric format — an optional sign, digits, and optionally a decimal point or exponent — after stripping surrounding whitespace. int() requires an integer string. A string that does not match raises a ValueError: int('3.5') fails because '3.5' is not an integer string. ⟦D.f5 D.f6 D:tb5⟧
[BEFORE_AFTER] Converting '32' from string to int with int() makes arithmetic possible; without conversion, adding a number raises a TypeError.
  before:
[CODE python]
delivery_time = '32'
delivery_time + 10
  annotations: ["String '32' — cannot add a number to it", 'TypeError: can only concatenate str to str']
  after:
[CODE python]
delivery_time = int('32')
delivery_time + 10
  annotations: ["int('32') returns the integer 32", 'Result: 42 — arithmetic now works']

### s14 · check · Convert a value to the target type  [reward 10]
Quick check — Which constructor and argument produces the value described?

### s15 · check · Recognise an invalid conversion  [reward 10]
Quick check — Which string cannot be converted by the given constructor?

### s16 · hands_on · Convert delivery data between types  [reward 15]
Practice — Use int(), float() and str() to fix type mismatches in order records.

### s17 · recap · What you learned  [reward 5]
Recap — Key ideas from this tile.
(takeaway) Comparison operators (<, <=, >, >=, ==, !=) each return True or False. and, or and not combine those booleans into compound conditions; and has higher priority than or. Converting a string to a number only works when the string matches the format the target type accepts — otherwise the conversion raises a ValueError. ⟦B.f2 C.f1 D.f5 D.f6 B:tb4 C:tb7 D:tb6⟧
[UP NEXT] Up next: Lists, Dictionaries, and Tuples: In the next tile you will store ordered sequences of delivery times in lists, map order IDs to cities in dictionaries, and group fixed records in tuples.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Grouping with parentheses and mixed int/float — A clear contrast showing how parentheses change the result, and why mixing int and float gives a float.
(mechanism) Parentheses control evaluation order: (32 + 8) * 2 adds first, giving 80. Without parentheses, * runs before +. When you mix an int and a float in one operation, Python promotes the int to float: 4 * 3.75 - 1 gives 14.0, not 14. ⟦A.f4 A.f5 A:tb2⟧
[BEFORE_AFTER] Adding parentheses changes the evaluation order and the result.
  before:
[CODE python]
32 + 8 * 2
  annotations: ['Result: 48 — * runs before +']
  after:
[CODE python]
(32 + 8) * 2
  annotations: ['Result: 80 — parentheses force addition first']
### r02 · Comparison operators and boolean results — A side-by-side contrast showing the same expression returning different booleans for different values.
(definition) The six comparison operators are < (less than), <= (less than or equal), > (greater than), >= (greater than or equal), == (equal) and != (not equal). Every comparison returns exactly True or False — never a number. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
[SIDE_BY_SIDE] The same expression delivery_minutes > 60 gives False for 32 and True for 72. left_label: 32 minutes (not late) | right_label: 72 minutes (late)
  left:
[CODE python]
delivery_minutes = 32
delivery_minutes > 60
  annotations: ['32 minutes', 'False — 32 is not greater than 60']
  right:
[CODE python]
delivery_minutes = 72
delivery_minutes > 60
  annotations: ['72 minutes', 'True — 72 is greater than 60']
### r03 · Operator priority: and before or — A contrast showing how and and or group when there are no parentheses.
(mechanism) In ascending priority order the logical operators are: or (lowest), and, not. and binds more tightly than or, so is_late or is_far and is_first_week groups as is_late or (is_far and is_first_week). not has lower priority than comparison operators: not delivery_minutes == 0 means not (delivery_minutes == 0). ⟦C.f1 C.f4 C:tb2 C:tb5⟧
[BEFORE_AFTER] Without parentheses, and groups first; adding parentheses changes which conditions must both be true.
  before:
[CODE python]
is_late or is_far and is_first_week
  annotations: ['Groups as: is_late or (is_far and is_first_week)']
  after:
[CODE python]
(is_late or is_far) and is_first_week
  annotations: ['Parentheses override priority — both sides must be true']
### r04 · Short-circuit evaluation in or and and — A side-by-side contrast showing when each operator stops evaluating early.
(mechanism) or short-circuits: if the first operand is True, Python returns it immediately without evaluating the second. and short-circuits: if the first operand is False, Python returns it immediately without evaluating the second. This means is_late or is_far only checks is_far when is_late is False, and is_late and is_far only checks is_far when is_late is True. ⟦C.f2 C.f3 C:tb3 C:tb4⟧
[SIDE_BY_SIDE] Both operators skip the second operand when the first operand already determines the result. left_label: or short-circuits on True | right_label: and short-circuits on False
  left:
[CODE python]
is_late = True
is_late or is_far
  annotations: ['is_late is True', 'Returns True — is_far never evaluated']
  right:
[CODE python]
is_late = False
is_late and is_far
  annotations: ['is_late is False', 'Returns False — is_far never evaluated']
### r05 · Converting between strings and numbers — A before/after showing what happens with and without int().
(mechanism) int('123') returns 123. float('+1.23') returns 1.23. str(32) returns '32'. These constructors convert between compatible types: a string of digits to int, a numeric-format string to float, any value to its string form. ⟦D.f1 D.f2 D.f3 D.f4 D:tb2 D:tb3 D:tb4⟧
[BEFORE_AFTER] Wrapping '32' in int() converts it to the integer 32, making arithmetic possible.
  before:
[CODE python]
delivery_time = '32'
result = delivery_time + 10
  annotations: ['String — cannot add to int', 'TypeError raised']
  after:
[CODE python]
delivery_time = int('32')
result = delivery_time + 10
  annotations: ["int('32') gives 32", 'Result: 42']
### r06 · When type conversion raises ValueError — A contrast between a failing conversion and a working alternative.
(misconception) float() requires the string to match a numeric format: an optional sign, digits, and optionally a decimal point or exponent, after stripping surrounding whitespace. int() requires an integer string — no decimal point. A string that does not match raises a ValueError: int('3.5') fails because '3.5' contains a decimal point. ⟦D.f5 D.f6 D:tb5⟧
[SIDE_BY_SIDE] int() cannot parse a decimal string directly; convert to float first if you need to truncate. left_label: int('3.5') — ValueError | right_label: int(float('3.5')) — works
  left:
[CODE python]
int('3.5')
  annotations: ["ValueError — '3.5' is not an integer string"]
  right:
[CODE python]
int(float('3.5'))
  annotations: ['Result: 3 — convert to float first, then truncate']

=========

# EVALUATOR PACKET — Lists, Dictionaries, and Tuples (tile_python_lists_dicts_tuples)
Tile summary: Store ordered sequences in lists, map keys to values in dictionaries, and group fixed records in immutable tuples.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.lists — Core data structure: lists
B = python.dictionaries — Core data structure: dictionaries
C = python.tuples — Core data structure: tuples

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.lists)   objective: Create a list, then index into it, slice it, and append a new item to build and read an ordered, mutable collection.
A.f1: A list is written as a comma-separated sequence of values inside square brackets, e.g. squares = [1, 4, 9, 16, 25].   [sources: python_docs_tutorial_introduction#lists]
A.f2: Like strings, lists can be indexed (squares[0] returns the first item, squares[-1] returns the last) and sliced (squares[-3:] returns a new list of the last three items).   [sources: python_docs_tutorial_introduction#lists]
A.f3: Lists are mutable: an item can be replaced in place, e.g. cubes[3] = 64 changes the value stored at that index.   [sources: python_docs_tutorial_introduction#lists]
A.f4: New items can be added to the end of a list with the list.append() method.   [sources: python_docs_tutorial_introduction#lists, python_docs_tutorial_datastructures#more-on-lists]
A.f5: In a slice such as word[0:2], the start index is included and the end index is excluded; lists support the same indexing and slicing operations as strings, e.g. squares[1:3] returns [4, 9], the items from index 1 up to but not including index 3.   [sources: python_docs_tutorial_introduction#text, python_docs_tutorial_introduction#lists]
note: Keep delivery_times = [32, 45, 21, 60, 18] as the one running list for every operation in this entry.
PRACTICE ANCHOR (live_code): Build a list of delivery times, append one more item, and retrieve a slice of it.  SUCCESS: The list holds the original items plus the appended one, and the printed slice is exactly the expected items.
ASSESSMENT ANCHOR: create_a_list facts=['f1']
ASSESSMENT ANCHOR: index_and_slice_a_list facts=['f2', 'f5']
ASSESSMENT ANCHOR: modify_and_extend_a_list facts=['f3', 'f4']

## SOURCE FACTS — B (python.dictionaries)   objective: Build a dictionary mapping keys to values, and look up, add, or update a value by its key.
B.f1: A dictionary is a collection of key: value pairs, written inside braces, where the keys must be unique within the dictionary.   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f2: A value is stored or updated by assigning to a key, e.g. tel['guido'] = 4127, and retrieved by subscripting with the key, e.g. tel['jack'].   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f3: Extracting a value for a key that is not in the dictionary by subscripting raises a KeyError.   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f4: The get() method returns None or a specified default instead of raising an error when a key is not in the dictionary.   [sources: python_docs_tutorial_datastructures#dictionaries]
B.f5: The in keyword checks whether a key is present in a dictionary.   [sources: python_docs_tutorial_datastructures#dictionaries]
note: Keep order_city as the one running dictionary across all blocks.
PRACTICE ANCHOR (live_code): Build a dictionary mapping product names to prices and look up one price by its key.  SUCCESS: The dictionary has the product names as keys; looking up one name prints that product's price.
ASSESSMENT ANCHOR: build_and_update_dictionary facts=['f1', 'f2']
ASSESSMENT ANCHOR: look_up_value_by_key facts=['f2']
ASSESSMENT ANCHOR: predict_missing_key_error facts=['f3']

## SOURCE FACTS — C (python.tuples)   objective: Create a tuple to group a fixed set of values together, and unpack it into separate variables.
C.f1: A tuple consists of a number of values separated by commas; a tuple's items are shown enclosed in parentheses on output, and a tuple may be written with or without surrounding parentheses as input, e.g. t = 12345, 54321, 'hello!'.   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
C.f2: Tuples are immutable: once created, an item inside a tuple cannot be reassigned (t[0] = 88888 raises a TypeError).   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
C.f3: A tuple can be unpacked into several variables at once, e.g. x, y, z = t, provided there are as many variables as there are elements in the tuple.   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
C.m1 (misconception): Enclosing a single value in parentheses does not make it a tuple; a one-item tuple requires a trailing comma, e.g. singleton = 'hello',.   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
note: TOC conflict: this concept's practice_objective returns a tuple from a function, but functions aren't taught until python.defining_calling_functions, much later in this region -- this entry teaches tuple creation, immutability and unpacking without using any function.
PRACTICE ANCHOR (live_code): Create a tuple holding a smallest and a largest delivery time, then unpack it into two variables and print them.  SUCCESS: The tuple has two values; unpacking gives each value its own name, and printing both shows the correct numbers.
ASSESSMENT ANCHOR: create_a_tuple facts=['f1']
ASSESSMENT ANCHOR: recognize_tuple_immutability facts=['f2']
ASSESSMENT ANCHOR: unpack_tuple_into_variables facts=['f3']
ASSESSMENT ANCHOR: recognize_single_item_tuple_needs_comma facts=['m1']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparing correlation strength across multiple variable pairs; Control flow: if/elif/else; Core data structure: dictionaries; Core data structure: sets; Core data structure: tuples; Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); For loops; Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Iterating over data structures; List and dict comprehensions; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Return values; String basics and f-string formatting; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Ordered, mutable sequences  [reward 5]
Lists — A list stores an ordered sequence of values you can index, slice and modify.
(intro) Keeping five separate variables for five delivery times gets unwieldy fast. A list stores an ordered sequence of values in a single name: delivery_times = [32, 45, 21, 60, 18]. Items are indexed from 0 at the left and from -1 at the right, so delivery_times[0] is 32 and delivery_times[-1] is 18. ⟦A.f1 A.f2 A:tb1 A:tb2⟧
(mechanism) A slice extracts a sub-list: delivery_times[1:3] returns [45, 21]. The start index is included; the end index is excluded. delivery_times[-3:] returns the last three items. Lists are mutable: delivery_times[3] = 64 replaces the item at index 3 in place. ⟦A.f3 A.f5 A:tb3⟧
[DIAGRAM: delivery_times — positive and negative indexes] nodes=['32 {index 0; index -5}', '45 {index 1; index -4}', '21 {index 2; index -3}', '60 {index 3; index -2}', '18 {index 4; index -1}', 'slice [1:3] starts here (included)', 'slice [1:3] ends here (excluded)'] edges=[('slice_start', 'i1', None), ('slice_end', 'i3', None)] alt: Array of five delivery times with positive indexes 0–4 above and negative indexes -5 to -1 below; a bracket marks slice [1:3] from index 1 (included) to index 3 (excluded), yielding [45, 21].

### s02 · video · Lists in action
Watch — See list creation, indexing and slicing demonstrated.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Adding items with append()  [reward 5]
Lists — append() grows a list by one item at the end.
(mechanism) To add a new item to the end of a list, call the append() method: delivery_times.append(27) adds 27 as the last element. ⟦A.f4 A:tb5⟧

### s04 · check · Modify and extend a list  [reward 10]
Quick check — Can you predict what a list looks like after an assignment and an append?

### s05 · hands_on · Build and work with a list of delivery times  [reward 15]
Practice — Create a list, index into it, slice it and append a new item.

### s06 · explainer · Key-to-value lookup  [reward 5]
Dictionaries — A dictionary maps unique keys to values — look up a city by order ID, not by position.
(intro) Sometimes you need to look up a value by a meaningful key rather than by position. A dictionary is a collection of key: value pairs written inside braces, where keys must be unique: order_city = {1042: 'Lagos', 1043: 'Abuja', 1044: 'Kano'}. Retrieve a value by subscripting with its key: order_city[1042] returns 'Lagos'. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
(mechanism) Store or update a value by assigning to a key: order_city[1044] = 'Kano' adds a new entry; assigning to an existing key replaces its value. The get() method returns None (or a specified default) instead of raising an error when a key is absent: order_city.get(9999) returns None rather than crashing. ⟦B.f2 B.f4 B:tb2 B:tb4⟧
(misconception) Subscripting a key that is not in the dictionary raises a KeyError: order_city[9999] fails if no order 9999 was ever added. Use get() when you are not certain the key exists. ⟦B.f3 B:tb3⟧
[DIAGRAM: order_city — key-to-value lookup] nodes=['1042', '1043', '1044', '9999 (missing)', "'Lagos'", "'Abuja'", "'Kano'", 'KeyError'] edges=[('k1042', 'v_lagos', 'lookup'), ('k1043', 'v_abuja', 'lookup'), ('k1044', 'v_kano', 'lookup'), ('k9999', 'v_error', 'KeyError')] alt: Mapping diagram: keys 1042, 1043, 1044 each point to their city values; key 9999 points to a KeyError node showing what happens when a missing key is subscripted.

### s07 · video · Dictionaries in action
Watch — See dictionary creation, lookup and the KeyError demonstrated.
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · explainer · Testing key membership with in  [reward 5]
Dictionaries — Use in to check whether a key exists before accessing it.
(mechanism) The in keyword checks whether a key is present in a dictionary: 1042 in order_city is True. ⟦B.f5 B:tb5⟧

### s09 · check · Predict what happens with a missing key  [reward 10]
Quick check — What does Python do when you subscript a key that is not in the dictionary?

### s10 · hands_on · Build and query an order-city dictionary  [reward 15]
Practice — Create a dictionary, add entries, look up values and use get() for safe access.

### s11 · explainer · Immutable sequences and unpacking  [reward 5]
Tuples — A tuple groups a fixed set of values; unpacking hands each piece back to its own name.
(intro) A tuple groups a small, fixed set of values together. It is written as comma-separated values, with or without surrounding parentheses: order = 1042, 'Lagos', 32 or order = (1042, 'Lagos', 32). Python shows tuples enclosed in parentheses on output. ⟦C.f1 C:tb1⟧
(misconception) Tuples are immutable: once created, an item cannot be reassigned. order[0] = 1099 raises a TypeError. Also, enclosing a single value in parentheses does not make it a tuple — singleton = ('Lagos') is still just the string 'Lagos'. A one-item tuple needs a trailing comma: singleton = 'Lagos', ⟦C.f2 C.m1 C:tb2 C:tb4⟧
[BEFORE_AFTER] Unpacking hands each element of the tuple back to its own name — order_id, city and minutes are now separate variables. ⟦C.f3⟧
  before:
[CODE python]
order = (1042, 'Lagos', 32)
  annotations: ['Three values packed into one tuple']
  after:
[CODE python]
order_id, city, minutes = order
  annotations: ["Unpacking: order_id=1042, city='Lagos', minutes=32"]

### s12 · check · Recognise when a one-item tuple needs a trailing comma  [reward 10]
Quick check — Which expression actually creates a tuple with one element?

### s13 · hands_on · Create, inspect and unpack a tuple  [reward 15]
Practice — Build a tuple for an order record, confirm it is immutable, and unpack it into named variables.

### s14 · recap · What you learned  [reward 5]
Recap — Key ideas from this tile.
(takeaway) A list is an ordered, mutable sequence indexed from 0; slices use start-included, end-excluded bounds; index assignment replaces an item in place and append() adds one at the end. A dictionary maps unique keys to values; subscripting a missing key raises a KeyError — use get() to avoid it. A tuple groups a fixed set of values that cannot be reassigned; unpacking distributes each element to its own name. ⟦A.f1 A.f3 A.f4 B.f1 B.f2 C.f2 C.f3 A:tb7 B:tb6 C:tb5⟧
[UP NEXT] Up next: Sets and Strings: In the next tile you will use sets to collect unique delivery cities with no duplicates, and f-strings to build readable messages that embed variable values.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Modifying a list and adding items — A before/after showing index assignment and append() on the same list.
(mechanism) Lists are mutable: you can replace any item by assigning to its index. delivery_times[3] = 64 changes the value at index 3 in place. append() adds a new item to the end: delivery_times.append(27) grows the list by one. ⟦A.f3 A.f4 A:tb3 A:tb5⟧
[BEFORE_AFTER] Index assignment replaces an item in place; append() adds a new item at the end.
  before:
[CODE python]
delivery_times = [32, 45, 21, 60, 18]
  annotations: ['Original list']
  after:
[CODE python]
delivery_times[3] = 64
delivery_times.append(27)
  annotations: ['60 replaced by 64 at index 3', '27 added at the end']
### r02 · KeyError vs get() for missing keys — A side-by-side contrast between subscripting a missing key and using get().
(misconception) Subscripting a key that is not in the dictionary raises a KeyError. order_city[9999] fails if 9999 was never added. Use get() to avoid the error: order_city.get(9999) returns None instead of crashing. ⟦B.f3 B:tb3 B:tb4⟧
[SIDE_BY_SIDE] Use get() when you are not certain the key exists; it returns None (or a default) instead of raising an error. left_label: Subscript — raises KeyError | right_label: get() — returns None
  left:
[CODE python]
order_city = {1042: 'Lagos', 1043: 'Abuja'}
order_city[9999]
  annotations: ['Dictionary with two entries', 'KeyError — 9999 is not a key']
  right:
[CODE python]
order_city = {1042: 'Lagos', 1043: 'Abuja'}
order_city.get(9999)
  annotations: ['Same dictionary', 'Returns None — no error raised']
### r03 · One-item tuples need a trailing comma — A side-by-side contrast showing that parentheses alone do not create a tuple.
(misconception) Enclosing a single value in parentheses does not make it a tuple — singleton = ('Lagos') is still just the string 'Lagos'. A one-item tuple requires a trailing comma: singleton = 'Lagos', or equivalently singleton = ('Lagos',). ⟦C.m1 C:tb4⟧
[SIDE_BY_SIDE] The trailing comma, not the parentheses, is what makes a one-item tuple. left_label: ('Lagos') — str, not tuple | right_label: ('Lagos',) — one-item tuple
  left:
[CODE python]
singleton = ('Lagos')
type(singleton)
  annotations: ['Just parentheses — still a str', "<class 'str'>"]
  right:
[CODE python]
singleton = ('Lagos',)
type(singleton)
  annotations: ['Trailing comma — this is a tuple', "<class 'tuple'>"]

=========

# EVALUATOR PACKET — Sets and Strings (tile_python_sets_strings)
Tile summary: Use sets to collect unique values and test membership, combine sets with union and intersection, and build readable messages with f-strings and format specifiers.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.sets — Core data structure: sets
B = python.string_basics_formatting — String basics and f-string formatting

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.sets)   objective: Create a set to store unique values, test membership in it, and combine two sets with union and intersection.
A.f1: A set is an unordered collection with no duplicate elements, used for membership testing and eliminating duplicate entries.   [sources: python_docs_tutorial_datastructures#sets]
A.f2: Curly braces or the set() function create a set; set() must be used for an empty set, because {} creates an empty dictionary instead.   [sources: python_docs_tutorial_datastructures#sets]
A.f3: set() can also build a set from the items of another collection, e.g. set('abracadabra') produces the set of unique letters in that string.   [sources: python_docs_tutorial_datastructures#sets]
A.f4: The in operator tests membership in a set, e.g. 'orange' in basket.   [sources: python_docs_tutorial_datastructures#sets]
A.f5: Set objects support mathematical operations such as union (a | b) and intersection (a & b).   [sources: python_docs_tutorial_datastructures#sets]
note: Keep the cities-from-orders framing throughout so 'unique values' stays concrete.
PRACTICE ANCHOR (live_code): Remove duplicates from a list of cities by converting it to a set, then test whether a given city is in the set.  SUCCESS: The set holds each city once; the membership test prints True for a city in the list and False for one that is not.
ASSESSMENT ANCHOR: create_set_of_unique_values facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: test_set_membership facts=['f4']
ASSESSMENT ANCHOR: combine_sets_with_union_and_intersection facts=['f5']

## SOURCE FACTS — B (python.string_basics_formatting)   objective: Write string literals and use f-strings to build a readable message that embeds variable values, including numbers formatted to a chosen number of decimal places.
B.f1: A quote character can be embedded in a string without escaping it by enclosing the string in the other kind of quote instead, e.g. "doesn't" instead of 'doesn\'t'.   [sources: python_docs_tutorial_introduction#text]
B.f2: An f-string is a string literal prefixed with f or F that embeds the value of a Python expression inside the string by writing the expression in curly brackets {expression}.   [sources: python_docs_tutorial_inputoutput#formatted-string-literals]
B.f3: An optional format specifier can follow the expression after a colon, giving greater control over how the value is formatted, such as rounding a number to a chosen number of places after the decimal (e.g. {value:.3f}).   [sources: python_docs_tutorial_inputoutput#formatted-string-literals]
PRACTICE ANCHOR (live_code): Write an f-string that reports a computed total inside a sentence, formatted to two decimal places.  SUCCESS: The printed sentence contains the computed total rounded to two decimal places.
ASSESSMENT ANCHOR: embed_quote_without_escaping facts=['f1']
ASSESSMENT ANCHOR: write_formatted_fstring facts=['f2', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparing correlation strength across multiple variable pairs; Control flow: if/elif/else; Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); For loops; Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Iterating over data structures; List and dict comprehensions; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Return values; Series and DataFrame data structures; String basics and f-string formatting; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Unique, unordered collections  [reward 5]
Sets — A set stores only distinct values — duplicates are automatically removed.
(intro) Sometimes you only care about which distinct values appear — which cities orders were delivered to, with no duplicates. A set is an unordered collection with no duplicate elements, used for membership testing and eliminating duplicate entries. ⟦A.f1 A:tb1⟧
(mechanism) Curly braces or the set() function create a set. set() must be used for an empty set, because {} creates an empty dictionary instead. set() can also build a set from another collection: cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano']) produces {'Lagos', 'Abuja', 'Kano'} — the duplicate 'Lagos' is collapsed to one entry. ⟦A.f2 A.f3 A:tb2 A:tb3⟧
[BEFORE_AFTER] Passing the list through set() collapses the repeated 'Lagos' to a single entry, leaving only unique cities.
  before:
[CODE python]
cities_list = ['Lagos', 'Abuja', 'Lagos', 'Kano']
  annotations: ['List with a repeated city']
  after:
[CODE python]
cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano'])
  annotations: ["{'Lagos', 'Abuja', 'Kano'} — duplicate removed"]
(mechanism) Test whether a value is in the set with the `in` operator: `'Lagos' in cities` returns `True` if `'Lagos'` is in the set, and `False` otherwise. This membership test is the primary reason to use a set rather than a list when you only need to check presence. ⟦A.f4⟧ ⟦A.f4 A:tb4⟧

### s02 · video · Sets in action
Watch — See set creation, membership testing and set operations demonstrated.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Union and intersection  [reward 5]
Sets — | combines two sets; & finds what they share.
(mechanism) Set objects support mathematical operations. Union (a | b) gives all elements from both sets. Intersection (a & b) gives only elements present in both: week1_cities & week2_cities gives cities that appeared in both weeks. ⟦A.f5 A:tb5⟧

### s04 · check · Create a set of unique values  [reward 10]
Quick check — Which expression produces a set with no duplicates from a list of cities?

### s05 · check · Combine sets with union and intersection  [reward 10]
Quick check — Which operator gives elements present in both sets, and which gives all elements from either?

### s06 · hands_on · Test membership in a set of cities  [reward 15]
Practice — Build a set of delivery cities and use in to check whether a given city is present.

### s07 · explainer · Embedding values and formatting numbers  [reward 5]
Strings and f-strings — f-strings embed variable values directly in a string; a format specifier controls how numbers are displayed.
(mechanism) A quote character can be embedded in a string without escaping it by using the other kind of quote. Writing "This delivery wasn't late" inside double quotes needs no escaping; the same text inside single quotes would need the apostrophe escaped as \'. ⟦B.f1 B:tb1⟧
(definition) An f-string is a string literal prefixed with f or F that embeds the value of a Python expression inside the string by writing the expression in curly brackets: f"Delivery to {city} took {delivery_minutes} minutes" substitutes in the current values of city and delivery_minutes. ⟦B.f2 B:tb2⟧
(mechanism) An optional format specifier follows the expression after a colon, controlling how the value is displayed. f"Average: {avg_minutes:.2f} minutes" produces 'Average: 32.67 minutes' when avg_minutes is 32.666 — the .2f specifier rounds to two decimal places. ⟦B.f3 B:tb3⟧
[BEFORE_AFTER] Adding :.2f after the expression rounds the output to two decimal places — the {value:.2f} part and its rounded result.
  before:
[CODE python]
avg_minutes = 32.666
f"Average: {avg_minutes} minutes"
  annotations: ['avg_minutes holds 32.666', "Produces: 'Average: 32.666 minutes'"]
  after:
[CODE python]
avg_minutes = 32.666
f"Average: {avg_minutes:.2f} minutes"
  annotations: ['Same value', "Produces: 'Average: 32.67 minutes'"]

### s08 · check · Embed a quote without escaping  [reward 10]
Quick check — Which string literal correctly embeds an apostrophe without a backslash escape?

### s09 · hands_on · Write a formatted f-string  [reward 15]
Practice — Build an f-string that reports a computed total formatted to two decimal places.

### s10 · recap · What you learned  [reward 5]
Recap — Key ideas from this tile.
(takeaway) A set stores only distinct values — pass a list through set() to remove duplicates. The in operator tests membership; | and & compute union and intersection. f-strings embed variable values with {expression}; a format specifier like :.2f controls decimal places. ⟦A.f1 A.f4 B.f2 B.f3 A:tb6 B:tb4⟧
[UP NEXT] Up next: Conditionals and For Loops: In the next tile you will write if/elif/else chains to branch on conditions and for loops to iterate over lists and other sequences.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Creating a set and removing duplicates — A before/after showing how set() collapses duplicates from a list.
(mechanism) A set is an unordered collection with no duplicate elements. Use set() to create one from a list: set(['Lagos', 'Abuja', 'Lagos', 'Kano']) gives {'Lagos', 'Abuja', 'Kano'}. Use {} for a non-empty set literal: {'Lagos', 'Abuja'}. For an empty set, you must use set() — {} creates an empty dictionary. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3⟧
[BEFORE_AFTER] Converting the list to a set removes the duplicate 'Lagos', reducing the count from 4 to 3.
  before:
[CODE python]
cities = ['Lagos', 'Abuja', 'Lagos', 'Kano']
len(cities)
  annotations: ['List — 4 items, with a duplicate', '4']
  after:
[CODE python]
cities = set(['Lagos', 'Abuja', 'Lagos', 'Kano'])
len(cities)
  annotations: ['Set — duplicate removed', '3']
### r02 · Union and intersection on sets — A side-by-side contrast showing | and & on the same two sets.
(mechanism) | (union) gives all elements from either set — no duplicates. & (intersection) gives only the elements present in both sets. If week1_cities = {'Lagos', 'Abuja'} and week2_cities = {'Abuja', 'Kano'}, then week1_cities | week2_cities is {'Lagos', 'Abuja', 'Kano'} and week1_cities & week2_cities is {'Abuja'}. ⟦A.f5 A:tb5⟧
[SIDE_BY_SIDE] | combines both sets; & keeps only what they have in common. left_label: | union — all cities from either | right_label: & intersection — only shared cities
  left:
[CODE python]
week1 = {'Lagos', 'Abuja'}
week2 = {'Abuja', 'Kano'}
week1 | week2
  annotations: ['Week 1 cities', 'Week 2 cities', "{'Lagos', 'Abuja', 'Kano'} — all cities"]
  right:
[CODE python]
week1 = {'Lagos', 'Abuja'}
week2 = {'Abuja', 'Kano'}
week1 & week2
  annotations: ['Week 1 cities', 'Week 2 cities', "{'Abuja'} — only the shared city"]
### r03 · Embedding a quote without escaping — A side-by-side contrast showing the same string with and without an escape.
(mechanism) A quote character can be embedded in a string without escaping it by enclosing the string in the other kind of quote. "This delivery wasn't late" uses double quotes, so the apostrophe in wasn't needs no backslash. Inside single quotes the same apostrophe would need escaping: 'This delivery wasn\'t late'. ⟦B.f1 B:tb1⟧
[SIDE_BY_SIDE] Switching to the other kind of quote avoids the need to escape the embedded quote character. left_label: Single quotes — escape needed | right_label: Double quotes — no escape needed
  left:
[CODE python]
'This delivery wasn\'t late'
  annotations: ['Backslash needed inside single quotes']
  right:
[CODE python]
"This delivery wasn't late"
  annotations: ['No backslash needed — double quotes wrap the string']