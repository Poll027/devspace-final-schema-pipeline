# EVALUATOR PACKET — Variables and Core Data Types (tile_python_variables_types)
Tile summary: Learn to store values in variables using Python's assignment operator, understand naming rules, and recognise the four core scalar types: int, float, str and bool.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.variables_assignment — Variables and assignment
B = python.core_data_types — Core data types (int, float, str, bool)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (python.variables_assignment)   objective: Create variables to store values and reassign them to new values using Python's assignment operator.
A.f1: The equal sign (=) is used to assign a value to a variable.   [sources: python_docs_tutorial_introduction#numbers]
A.f2: If a variable has not been assigned a value, trying to use it raises a NameError.   [sources: python_docs_tutorial_introduction#numbers]
A.f3: Assigning to a name that already has a value rebinds it to the new value.   [sources: python_official_docs#reference/simple_stmts.html#assignment-statements]
A.f4: A valid variable name is made of letters, digits and the underscore, cannot start with a digit, is case-significant, and is not a reserved keyword such as if, for or class.   [sources: python_official_docs#reference/lexical_analysis.html#identifiers]
A.f5: An assigned name can be used in a later expression, e.g. after width = 20 and height = 5 * 9, width * height computes using their assigned values.   [sources: python_docs_tutorial_introduction#numbers]
note: Learner has zero prior Python vocabulary here -- keep values simple (a delivery-minutes number) and don't lean on any type distinctions yet, since python.core_data_types comes next.
note: The TOC practice says the reassignment is 'based on a computation'; python.arithmetic_operators comes later, so the practice here uses only a single multiplication like the f5 example (width * height).
PRACTICE ANCHOR (live_code): Assign three variables to simple values, then reassign one of them to a new value built from the others.  SUCCESS: Three names are assigned; the reassigned name holds the new value built from the others; no name is used before it is assigned.
ASSESSMENT ANCHOR: assign_and_reassign_variables facts=['f1', 'f3', 'f5']
ASSESSMENT ANCHOR: choose_valid_variable_name facts=['f4']
ASSESSMENT ANCHOR: predict_name_error_for_unassigned_name facts=['f2']

## SOURCE FACTS — B (python.core_data_types)   objective: Recognize Python's four core scalar types (int, float, str, bool) from a literal or value, and predict how each behaves in arithmetic, comparisons, and printing.
B.f1: Integer literals (e.g. 2, 4, 20) have type int, and literals with a fractional part (e.g. 5.0, 1.6) have type float.   [sources: python_docs_tutorial_introduction#numbers]
B.f2: Text values are of type str (a string) and can be written with single quotes or double quotes with the same result.   [sources: python_docs_tutorial_introduction#text]
B.f3: The bool type has exactly two values, True and False.   [sources: python_docs_stdtypes#boolean-type-bool]
B.f4: print() writes the value of its arguments; strings are printed without their quotes.   [sources: python_docs_tutorial_introduction#first-steps-towards-programming, python_docs_tutorial_introduction#text]
B.f5: The built-in type() function, called with one argument, returns the type of that object.   [sources: python_docs_library_functions#type]
note: TOC conflict: this concept's assessment_target asks the learner to predict how a value behaves in arithmetic and comparisons, but python.arithmetic_operators and python.comparison_operators come later in the same region -- this entry teaches only literal recognition, print() and type(), per the coverage brief's required facts.
note: Don't demonstrate bool-as-int behavior (optional f6) at length -- it's easy to skip and mostly a caution against relying on it.
PRACTICE ANCHOR (live_code): Create one variable of each core type (int, float, str, bool) and print the type of each using type().  SUCCESS: Four variables are created; type() is printed for each and shows int, float, str and bool respectively.
ASSESSMENT ANCHOR: identify_value_type facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: predict_print_output_and_check_type facts=['f4', 'f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Arithmetic operators; Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparison operators; Control flow: if/elif/else; Core data structure: dictionaries; Core data structure: lists; Core data structure: sets; Core data structure: tuples; Core data types (int, float, str, bool); Default and keyword arguments; Defining calling functions; For loops; Idiomatic style conventions for readable Python; Iterating over data structures; List and dict comprehensions; Logical operators; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Modules and imports; Parameters arguments; Return values; String basics and f-string formatting; Type conversion/casting; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Storing a value under a name  [reward 5]
Variables and assignment — Before you can work with a delivery time in code, you need to give it a name you can refer back to.
(intro) Suppose you are processing a delivery order and need to keep track of how long it took. In Python, the equal sign (=) is used to assign a value to a variable, so writing delivery_minutes = 32 stores the number 32 under the name delivery_minutes. From that point on, any line that mentions delivery_minutes reads back the stored value. ⟦A.f1 A:tb1⟧
(misconception) A name only exists once something has been assigned to it. Referring to average_delivery_minutes before any earlier line has set it raises a NameError — Python does not invent a default value for you. ⟦A.f2 A:tb2⟧
[BEFORE_AFTER] Assigning to delivery_minutes a second time replaces 32 with 45 — the name now refers to the new value.
  before:
[CODE python]
delivery_minutes = 32
  annotations: ['delivery_minutes now holds 32']
  after:
[CODE python]
delivery_minutes = 32
delivery_minutes = 45
  annotations: ['The name is rebound to 45; 32 is gone']

### s02 · explainer · Naming rules and using stored values  [reward 5]
Variables and assignment — Not every word is a valid variable name, and once a name holds a value you can use it in later expressions.
(syntax) A valid variable name is made of letters, digits and underscores, cannot start with a digit, is case-significant (delivery_minutes and Delivery_Minutes are two different names), and cannot be a reserved keyword such as if, for or class. ⟦A.f4 A:tb4⟧
(example) Once a name holds a value, later code can use it in an expression. After orders_per_driver = 20 and days_worked = 5, a line such as orders_per_driver * days_worked reads back both stored values and computes a result from them. ⟦A.f5 A:tb5⟧

### s03 · check · What happens when you use an unassigned name?  [reward 10]
Quick check — Test whether you can predict what Python does when a name has never been assigned.

### s04 · hands_on · Assign and reassign delivery variables  [reward 15]
Practice — Write Python to store delivery values, reassign one of them, and use the stored names in an expression.

### s05 · explainer · Four kinds of value: int, float, str and bool  [reward 5]
Core data types — Every value in Python has a type. Delivery data uses all four core scalar types.
(intro) Every value in Python has a type. In delivery data, an order id like 1042, a delivery time like 32.5, a city name like 'Lagos', and whether an order was late are four different kinds of value — Python has a core scalar type for each. ⟦B.f1 B.f2 B.f3 B:tb1⟧
(definition) Whole numbers written without a decimal point — such as 2, 4 or 20 — have type int. A literal written with a fractional part, such as 5.0 or 1.6, has type float. So order_id = 1042 is an int, while delivery_minutes = 32.5 is a float. ⟦B.f1 B:tb2⟧
(definition) Text values are of type str. They can be written with single quotes or double quotes with the same result — city = 'Lagos' and city = "Lagos" create the identical string value. ⟦B.f2 B:tb3⟧
[SIDE_BY_SIDE] 1042, 32.5, 'Lagos' and True are four different kinds of value — int, float, str and bool. left_label: int and float | right_label: str and bool
  left:
[CODE python]
order_id = 1042        # int
delivery_minutes = 32.5  # float
  annotations: ['Whole number → int', 'Fractional part → float']
  right:
[CODE python]
city = 'Lagos'   # str
is_late = True   # bool
  annotations: ['Text in quotes → str', 'True or False → bool']

### s06 · explainer · Printing values and checking types  [reward 5]
Core data types — Two built-in tools let you see what a value is and what type it has.
(mechanism) print() writes the value of its argument. When that value is a string, print() writes it without the surrounding quotes — print(city) displays Lagos, not 'Lagos'. ⟦B.f4 B:tb5⟧
(syntax) The built-in type() function returns the type of its argument. print(type(delivery_minutes)) shows <class 'float'> and print(type(city)) shows <class 'str'>, so you can check a value's type directly. ⟦B.f5 B:tb6⟧

### s07 · check · Predict print() output and check a type  [reward 10]
Quick check — Test whether you can predict what print() and type() produce for a given value.

### s08 · hands_on · Create one variable of each core type  [reward 15]
Practice — Write Python to create an int, float, str and bool variable, then print the type of each using type().

### s09 · recap · What you learned  [reward 10]
Recap — Key ideas from this tile.
(takeaway) = stores a value under a name; assigning again to that name replaces what it held; using a name that was never assigned raises a NameError. The four core scalar types are int, float, str and bool — type() tells you which one a value is. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 B.f3 B.f5 A:tb6 B:tb7⟧
[UP NEXT] Up next: Operators and Type Conversion: In the next tile you will use arithmetic and comparison operators on the values you have just learned to store.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Why does Python raise NameError? — A name only exists after you assign it. Here is the contrast.
(misconception) Python does not create a variable for you automatically. If you write print(average_delivery_minutes) before any line has assigned a value to that name, Python raises NameError: name 'average_delivery_minutes' is not defined. You must assign first: average_delivery_minutes = 32 before you can use it. ⟦A.f2 A:tb2⟧
[BEFORE_AFTER] Adding the assignment before the print removes the NameError.
  before:
[CODE python]
print(average_delivery_minutes)
  annotations: ['NameError — name was never assigned']
  after:
[CODE python]
average_delivery_minutes = 32
print(average_delivery_minutes)
  annotations: ['Assign first', 'Now the name exists — prints 32']
### r02 · Assigning, reassigning and naming variables — A quick recap of the rules before you try the exercise again.
(mechanism) Use = to assign: delivery_minutes = 32. Assigning again to the same name replaces the old value — delivery_minutes = 45 makes the name hold 45. Once assigned, you can use the name in an expression: orders_per_driver * days_worked reads both stored values. ⟦A.f1 A.f3 A.f5 A:tb1 A:tb3 A:tb5⟧
(syntax) A valid name uses letters, digits and underscores, cannot start with a digit, is case-significant, and cannot be a reserved keyword such as if or for. delivery_minutes is valid; 1st_order and for are not. ⟦A.f4 A:tb4⟧
### r03 · What print() and type() show — A clear contrast between what print() displays and what type() returns.
(mechanism) print() writes the value without quotes — print(city) displays Lagos, not 'Lagos'. type() returns the type object — print(type(city)) shows <class 'str'> and print(type(delivery_minutes)) shows <class 'float'>. ⟦B.f4 B.f5 B:tb5 B:tb6⟧
[BEFORE_AFTER] Wrapping city in type() changes the output from the value to its type.
  before:
[CODE python]
city = 'Lagos'
print(city)
  annotations: ['Displays: Lagos  (no quotes)']
  after:
[CODE python]
city = 'Lagos'
print(type(city))
  annotations: ["Displays: <class 'str'>"]
### r04 · The four core types and how to inspect them — A quick recap of int, float, str and bool, plus print() and type().
(definition) Whole numbers are int (order_id = 1042); numbers with a decimal point are float (delivery_minutes = 32.5); text in quotes is str (city = 'Lagos'); True or False is bool (is_late = True). These are the four core scalar types. ⟦B.f1 B.f2 B.f3 B:tb2 B:tb3 B:tb4⟧
(syntax) print(city) displays Lagos without quotes. print(type(city)) shows <class 'str'>. Use type() any time you need to confirm what kind of value a variable holds. ⟦B.f4 B.f5 B:tb5 B:tb6⟧