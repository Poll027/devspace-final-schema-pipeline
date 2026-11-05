# EVALUATOR PACKET — Comprehensions and Iterating Collections (tile_python_comprehensions_iterating)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.comprehensions — List and dict comprehensions
B = python.iterating_collections — Iterating over data structures

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_python_comprehensions_iterating.s06: remediation tile_python_comprehensions_iterating.r02 re-teaches ['python.iterating_collections#f3'] but the check measures ['python.iterating_collections#f1', 'python.iterating_collections#f2', 'python.iterating_collections#f4'] — a learner who fails it is sent to an unrelated fact

## SOURCE FACTS — A (python.comprehensions)   objective: Build a new list or dictionary in one expression using comprehension syntax instead of a multi-line loop.
A.f1: A list comprehension consists of brackets containing an expression followed by a for clause, and optionally more for or if clauses; it produces a new list from evaluating the expression in that context, e.g. [x*2 for x in vec] doubles each value in vec.   [sources: python_docs_tutorial_datastructures#list-comprehensions]
A.f2: A list comprehension can filter its source with an if clause, e.g. [x for x in vec if x >= 0] keeps only the values that satisfy the condition.   [sources: python_docs_tutorial_datastructures#list-comprehensions]
A.f3: Dict comprehensions create dictionaries from arbitrary key and value expressions, e.g. {x: x**2 for x in (2, 4, 6)}.   [sources: python_docs_tutorial_datastructures#dictionaries]
PRACTICE ANCHOR (live_code): Write a list comprehension that squares the even numbers in a list.  SUCCESS: The resulting list contains the squares of only the even numbers, in the original order.
ASSESSMENT ANCHOR: write_list_comprehension facts=['f1', 'f2']
ASSESSMENT ANCHOR: write_dict_comprehension facts=['f3']

## SOURCE FACTS — B (python.iterating_collections)   objective: Iterate over any of Python's core collections, using the items() method to retrieve a dictionary's keys and values together.
B.f1: Looping directly over a dictionary (for x in d) yields its keys, since iter(d) returns an iterator over the dictionary's keys.   [sources: python_docs_stdtypes#mapping-types-dict]
B.f2: When looping through a dictionary, the key and its corresponding value can be retrieved together using the items() method, e.g. for k, v in knights.items(): print(k, v).   [sources: python_docs_tutorial_datastructures#looping-techniques]
B.f3: A set's elements may come out in a different order than expected when iterated over, because a set is unordered.   [sources: python_docs_tutorial_datastructures#sets]
B.f4: Tuples are a sequence type, so a for loop visits their items in order the same way it does for a list.   [sources: python_docs_tutorial_datastructures#tuples-and-sequences]
note: Reuse order_city from python.dictionaries as the running dict example here.
PRACTICE ANCHOR (live_code): Write a loop that goes through a dictionary's items and prints each key and its value.  SUCCESS: Every key-value pair is printed exactly once.
ASSESSMENT ANCHOR: loop_over_keys_or_sequence_items facts=['f1', 'f4']
ASSESSMENT ANCHOR: loop_over_key_value_pairs facts=['f2']
ASSESSMENT ANCHOR: recognize_unordered_set_iteration facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Boolean/conditional filtering; Comparing correlation strength across multiple variable pairs; Computing descriptive statistics with pandas (describe, mean, median, std); Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Inspecting data (head, info, describe, shape, dtypes); Iterating over data structures; Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Return values; Selecting rows/columns with loc/iloc; Series and DataFrame data structures; Sorting values; Variable scope (local vs global)

## LESSON, in learner order

### s01 · explainer · Building lists and dicts in one line: comprehensions  [reward 5]
Comprehensions — Replace multi-line loops with compact, readable expressions.
### Building lists and dicts in one line: comprehensions
(definition) Building a new list from an existing one by looping is common enough that Python has a shorthand for it. A list comprehension consists of brackets containing an expression followed by a for clause, and optionally one or more for or if clauses; it produces a new list by evaluating the expression for each item — [minutes * 2 for minutes in delivery_times] doubles every value. ⟦A.f1 A:tb1⟧
(mechanism) Add an if clause to filter the source: [minutes for minutes in delivery_times if minutes >= 45] keeps only the delivery times that satisfy that condition. Dict comprehensions work the same way with curly braces and a key: value expression — {city: len(city) for city in ('Lagos', 'Abuja', 'Kano')} maps each city name to its length. ⟦A.f2 A.f3 A:tb2 A:tb3⟧
[BEFORE_AFTER] Five lines collapse to one: the expression, for clause and if clause move inside brackets.
  before:
[CODE python]
# Multi-line loop
doubled = []
for minutes in delivery_times:
    if minutes >= 45:
        doubled.append(minutes * 2)
  annotations: ['empty list to collect results', 'for clause: iterate over source', 'if clause: filter condition', 'expression: double each kept value']
  after:
[CODE python]
# Equivalent list comprehension
doubled = [minutes * 2 for minutes in delivery_times if minutes >= 45]
  annotations: ['expression · for clause · if clause — all in one line']

### s02 · check · Write a dict comprehension  [reward 5]
Quick check — Which expression correctly builds a dictionary from a sequence using a dict comprehension?
QUESTION [choice, core, grading=client] Which expression creates a dictionary that maps each number in `[2, 4, 6]` to its square?

Expected result: `{2: 4, 4: 16, 6: 36}`
  ✔ opt_a: `{x: x**2 for x in [2, 4, 6]}`
      why: Correct. A dict comprehension uses `{key_expr: value_expr for var in iterable}`. Here `x` is the key and `x**2` is the value.
  ✘ opt_b: `[x: x**2 for x in [2, 4, 6]]`
      why: Square brackets `[...]` create a list, not a dictionary. A dict comprehension uses curly braces `{key: value for ...}`.
  ✘ opt_c: `{x**2 for x in [2, 4, 6]}`
      why: `{x**2 for x in [2, 4, 6]}` is a set comprehension — it produces a set of values, not a key-value dictionary. A dict comprehension needs `key: value` inside the braces.
  ✘ opt_d: `{x**2: x for x in [2, 4, 6]}`
      why: This maps the square to the original number — the key and value are swapped. The prompt asks for `{number: square}`, so the key should be `x` and the value `x**2`.
  feedback✔: Right — `{x: x**2 for x in [2, 4, 6]}` is a dict comprehension: curly braces, `key: value` expression, then the `for` clause.  feedback✘: A dict comprehension uses `{key_expr: value_expr for var in iterable}` with curly braces and a colon separating key from value.  hints: ['A dict comprehension starts with `{` and contains `key: value` before the `for` clause.', 'Which part should be the key (the original number) and which the value (its square)?']  remediation→r01
  MEASURES: A:write_dict_comprehension(f3)   anchors=['assessment:write_dict_comprehension']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Write list and dict comprehensions  [reward 10]
Practice — Use comprehensions to filter delivery times and build a city-length dictionary.
QUESTION [code_exercise, core, grading=client] QuickDeliver wants to flag orders whose delivery time is even.

`numbers` and `threshold` are already assigned below.

Write a list comprehension that assigns to `result` the squares of only the numbers in `numbers` that are divisible by `threshold`, in the original order. Use `x * x` as the expression and `x % threshold == 0` as the filter.

Then print `result`.

Expected output:
```
[4, 16, 36, 64]
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}'] blocked=30 items
  file solution.py [editable]:
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
threshold = 2
# Write your list comprehension here

  SOLUTION solution.py:
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
threshold = 2
result = [x * x for x in numbers if x % threshold == 0]
print(result)

  test t1_stdout (stdout_equals, visible=True): {"expected":"[4, 16, 36, 64]"} | on-fail: Expected `[4, 16, 36, 64]`. Check your expression (`x * x`), for clause, and if clause (`x % threshold == 0`).
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"46f8a88609f942c76b5e7fb7f9b0661370e5c1661f8a8554e2ba33361f7616dd","tests_passed":1}
  feedback✔: The comprehension filtered to numbers divisible by `threshold` and squared each one — `[4, 16, 36, 64]`.  feedback✘: A list comprehension has the form `[expression for var in iterable if condition]`. Use `x * x` as the expression and `x % threshold == 0` as the filter.  hints: ['The structure is `[x * x for x in numbers if ...]` — fill in the filter condition using `threshold`.', 'A number divisible by `threshold` has no remainder: `x % threshold == 0`.']  remediation→r01
  MEASURES: A:write_list_comprehension(f1,f2); A:write_dict_comprehension(f3)   anchors=['practice', 'assessment:write_list_comprehension', 'assessment:write_dict_comprehension']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · explainer · Looping over any collection: lists, dicts, sets and tuples  [reward 5]
Iterating collections — The same for loop syntax works on every collection — what changes is what you get back.
### Looping over any collection: lists, dicts, sets and tuples
(mechanism) You've already looped over lists with for. The same for x in ... pattern works on other collections, but what you get back per pass differs. Looping directly over a dictionary yields its keys — for order_id in order_city: visits each order id, not each city. To get both key and value together, use .items(): for order_id, city in order_city.items(): print(order_id, city). ⟦B.f1 B.f2 B:tb1 B:tb2⟧
(misconception) A set's elements may come out in a different order than expected when iterated over, because a set is unordered — looping over a set of cities won't necessarily visit them in the order they were added. Tuples are a sequence type, so a for loop visits their items in order the same way it does for a list — for value in order: visits 1042, then 'Lagos', then 32, when order = (1042, 'Lagos', 32). ⟦B.f3 B.f4 B:tb3 B:tb4⟧
[SIDE_BY_SIDE] The for x in ... syntax is the same for every collection; what changes is what each pass hands you. left_label: Collection type and loop header | right_label: What the loop variable holds each pass
  left:
[CODE python]
# list
for minutes in delivery_times: ...

# dict (keys only)
for order_id in order_city: ...

# dict (key + value)
for order_id, city in order_city.items(): ...

# set
for city in {'Lagos', 'Abuja', 'Kano'}: ...

# tuple
for value in (1042, 'Lagos', 32): ...
  annotations: []
  right:
[CODE python]
# each integer delivery time in order
# e.g. 32, 45, 21, 60, 18 …

# each integer key
# e.g. 1042, 1043, 1044 …

# each (key, value) pair
# e.g. (1042, 'Lagos'), (1043, 'Abuja') …

# each element — order not guaranteed
# may be 'Kano', 'Lagos', 'Abuja' or any order

# each item in sequence order
# 1042, then 'Lagos', then 32
  annotations: []

### s05 · check · Set iteration order  [reward 5]
Quick check — What can you rely on when iterating over a set?
QUESTION [choice, core, grading=client] A colleague writes this code and expects the cities to print in the order `Lagos`, `Abuja`, `Kano`:

```python
cities = {'Lagos', 'Abuja', 'Kano'}
for city in cities:
    print(city)
```

What is wrong with that expectation?
  ✔ opt_a: A set is unordered, so the items may come out in any order
      why: Correct. A set is unordered, so its elements may come out in a different order than expected when iterated over.
  ✘ opt_b: Nothing — sets always iterate in insertion order
      why: Sets do not preserve insertion order. That property belongs to dictionaries (since Python 3.7) and lists, not sets.
  ✘ opt_c: Nothing — sets always iterate in alphabetical order
      why: Sets do not guarantee alphabetical order. The iteration order of a set is determined by the hash values of its elements, which is not predictable.
  ✘ opt_d: The loop will raise an error because sets are not iterable
      why: Sets are iterable — a `for` loop over a set works fine. The issue is that the order of elements is not guaranteed.
  feedback✔: Right — a set is unordered, so iterating over it gives elements in an unpredictable order, not necessarily the insertion order.  feedback✘: A set is unordered. When you iterate over a set, the elements may come out in any order — not insertion order, not alphabetical order.  hints: ["What does 'unordered' mean for a set? Does it keep track of the order items were added?", "Compare a set `{'Lagos', 'Abuja', 'Kano'}` with a list `['Lagos', 'Abuja', 'Kano']` — which one preserves order?"]  remediation→r02
  MEASURES: B:recognize_unordered_set_iteration(f3)   anchors=['assessment:recognize_unordered_set_iteration']
  taught-before-tested: B.f3←s04

### s06 · hands_on · Loop over keys and key-value pairs  [reward 10]
Practice — Write loops that iterate over the order_city dictionary — first keys only, then key-value pairs.
QUESTION [code_exercise, core, grading=client] QuickDeliver stores a mapping of order IDs to cities.

`order_city` is already assigned below using city variables.

Add a `for` loop that iterates directly over `order_city` (which yields each key), then prints the order ID and its city on one line using `order_city[key]` to look up the value.

Expected output:
```
1042 Lagos
1043 Abuja
1044 Kano
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():'] blocked=28 items
  file solution.py [editable]:
city_a = 'Lagos'
city_b = 'Abuja'
city_c = 'Kano'
order_city = {1042: city_a, 1043: city_b, 1044: city_c}
# Write your for loop here

  SOLUTION solution.py:
city_a = 'Lagos'
city_b = 'Abuja'
city_c = 'Kano'
order_city = {1042: city_a, 1043: city_b, 1044: city_c}
for key in order_city:
    print(key, order_city[key])

  test t1_stdout (stdout_equals, visible=True): {"expected":"1042 Lagos\n1043 Abuja\n1044 Kano"} | on-fail: Expected three lines, one per entry. Use `for key in order_city:` and `print(key, order_city[key])`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f6a83759bd7d0908c98689243a0b8b0e2306ccc7b3d7dfe025f0e855a00551e6","tests_passed":1}
  feedback✔: Every key-value pair was printed exactly once. Looping directly over a dictionary yields its keys; `order_city[key]` retrieves the matching value.  feedback✘: Use `for key in order_city:` to iterate over the keys, then `print(key, order_city[key])` inside the loop body to print each key and its value.  hints: ['Looping directly over a dictionary with `for key in order_city:` gives you each key on every pass.', 'Inside the loop, `order_city[key]` looks up the value for that key — use `print(key, order_city[key])` to print both.']  remediation→r02
  MEASURES: B:loop_over_keys_or_sequence_items(f1,f4); B:loop_over_key_value_pairs(f2)   anchors=['practice', 'assessment:loop_over_keys_or_sequence_items', 'assessment:loop_over_key_value_pairs']
  taught-before-tested: B.f1←s04; B.f4←s04; B.f2←s04

### s07 · recap · What you've learned  [reward 5]
Recap — One-line builders and universal iteration.
(takeaway) A comprehension does in one line what a for loop with an if check and an empty list to append into would otherwise take several lines to build. The same for x in ... syntax works across lists, dicts, sets and tuples — what changes is what each pass hands you: an item, a key, or with .items() a key-value pair. For a set, the order isn't guaranteed. ⟦A.f1 A.f2 B.f1 B.f2 B.f3 B.f4 A:tb4 B:tb5⟧
[UP NEXT] Up next: Functions and Scope: Next you'll learn how to define reusable functions, pass arguments, return values, and understand where variables are visible.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Dict comprehension syntax — Let's revisit how to write a dict comprehension.
### Reminder: dict comprehension syntax
(mechanism) Dict comprehensions use curly braces with a key: value expression before the for clause — {city: len(city) for city in ('Lagos', 'Abuja', 'Kano')} maps each city name to its length. The key and value expressions can be any valid Python expression; the result is a new dictionary, not a list. ⟦A.f3 A:tb3⟧
### r02 · Sets are unordered — Let's revisit why set iteration order is not guaranteed.
### Reminder: sets are unordered
(misconception) A set's elements may come out in a different order than expected when iterated over, because a set is unordered. Looping over {'Lagos', 'Abuja', 'Kano'} won't necessarily visit them in the order they were written — the order can vary between runs. If order matters, use a list or tuple instead. ⟦B.f3 B:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· expected.value: 1042 Lagos_x
1043 Abuja
1044 Kano
· expected.value: 1042 Lagos
1043 Abuja_x
1044 Kano

=========

# EVALUATOR PACKET — Conditionals and For Loops (tile_python_conditionals_for_loops)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.conditional_statements — Control flow: if/elif/else
B = python.for_loops — For loops

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (python.conditional_statements)   objective: Write an if/elif/else chain that branches to the correct block for every case a decision requires.
A.f1: An if statement executes its block only when its condition is true.   [sources: python_docs_tutorial_controlflow#if-statements]
A.f2: There can be zero or more elif parts after an if, and the else part is optional; elif is short for 'else if' and helps avoid excessive indentation from nested if statements.   [sources: python_docs_tutorial_controlflow#if-statements]
A.f3: An if/elif/.../else chain selects exactly one suite by evaluating the conditions one by one until one is found to be true; if none of them are true, the else suite (if present) is executed.   [sources: python_official_docs#reference/compound_stmts.html#the-if-statement]
A.f4: Each condition in an if/elif/else chain ends with a colon, and the block belonging to that branch is indented beneath it, e.g. if x < 0: ... elif x == 0: ... else: ....   [sources: python_docs_tutorial_controlflow#if-statements, python_docs_tutorial_introduction#first-steps-towards-programming]
PRACTICE ANCHOR (live_code): Write an if/elif/else chain that classifies a numeric score into one of three grade bands.  SUCCESS: Scores in each band print or store the right label, and exactly one branch runs per score.
ASSESSMENT ANCHOR: explain_when_if_block_runs facts=['f1']
ASSESSMENT ANCHOR: write_if_elif_else_chain facts=['f2', 'f3', 'f4']
ASSESSMENT ANCHOR: predict_branch_taken facts=['f3']

## SOURCE FACTS — B (python.for_loops)   objective: Write a for loop that visits every element of a known collection exactly once to process it.
B.f1: Python's for statement iterates over the items of any sequence (such as a list or a string), in the order that they appear in the sequence.   [sources: python_docs_tutorial_controlflow#for-statements]
B.f2: Each pass through a for loop binds the loop variable to the next item of the sequence, e.g. for w in words: print(w, len(w)) prints every word in words.   [sources: python_docs_tutorial_controlflow#for-statements]
B.f3: A for statement's header line ends with a colon, and the statements to repeat are indented beneath it, e.g. for w in words: print(w, len(w)).   [sources: python_docs_tutorial_controlflow#for-statements]
note: Reuse the delivery_times list from python.lists as the one collection iterated over here.
PRACTICE ANCHOR (live_code): Write a for loop that adds up the values in a list of numbers and prints the total.  SUCCESS: The loop visits every item exactly once and the printed total equals the sum of the list.
ASSESSMENT ANCHOR: write_for_loop_over_collection facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: trace_loop_variable_each_pass facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparing correlation strength across multiple variable pairs; Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); For loops; Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Inspecting data (head, info, describe, shape, dtypes); Iterating over data structures; List and dict comprehensions; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Return values; Series and DataFrame data structures; Variable scope (local vs global); While loops

## LESSON, in learner order

### s01 · explainer · Branching on data: if, elif, else  [reward 5]
Control flow — Make your code choose the right path based on each delivery's data.
### Branching on data: if, elif, else
(mechanism) Not every line of code should always run — sometimes what happens next depends on the data. An if statement executes its block only when its condition is true. You can add zero or more elif parts after an if, and an optional else at the end; elif is short for 'else if' and keeps the code flat instead of deeply nested. ⟦A.f1 A.f2 A:tb1 A:tb2⟧
(syntax) An if/elif/else chain selects exactly one block by evaluating conditions top to bottom until one is true; if none are true, the else block (if present) runs. Each condition ends with a colon, and the block belonging to that branch is indented beneath it:

if delivery_minutes < 15:
    category = 'fast'
elif delivery_minutes < 45:
    category = 'normal'
else:
    category = 'slow'

With delivery_minutes = 30, the first condition is false and the second is true, so category becomes 'normal' and the else branch is skipped. ⟦A.f3 A.f4 A:tb3 A:tb4⟧
[PROCESS_FLOW: Which branch runs for delivery_minutes = 30?] nodes=['delivery_minutes = 30', 'delivery_minutes < 15?', "category = 'fast' — skipped — condition is false", 'delivery_minutes < 45?', "category = 'normal' — runs — condition is true", "category = 'slow' — skipped — earlier branch matched", "category = 'normal'"] edges=[('start', 'cond1', None), ('cond1', 'fast', 'True'), ('cond1', 'cond2', 'False'), ('fast', 'end', None), ('cond2', 'normal', 'True'), ('cond2', 'slow', 'False'), ('normal', 'end', None), ('slow', 'end', None)] alt: Decision flow: delivery_minutes = 30 fails the first condition (< 15), passes the second (< 45), so category = 'normal' runs and the else branch is skipped.

### s02 · check · When does an if block run?  [reward 5]
Quick check — Choose the correct description of when an if statement executes its block.
QUESTION [choice, intro, grading=client] When does the body of an `if` statement execute?

```python
delivery_minutes = 30
if delivery_minutes > 45:
    print('late')
```
  ✔ opt_a: Only when its condition is true
      why: Correct. An `if` statement executes its block only when its condition is true. Here `30 > 45` is false, so `print('late')` is skipped.
  ✘ opt_b: Every time the program runs, regardless of the condition
      why: The body only runs when the condition is true, not unconditionally. If you need code to always run, place it outside the `if` block.
  ✘ opt_c: Only when its condition is false
      why: That is the opposite of how `if` works. The body runs when the condition is true; when it is false the body is skipped.
  ✘ opt_d: Only when the variable equals zero
      why: The `if` body runs when its condition evaluates to true — not specifically when a variable equals zero. Any true condition triggers it.
  feedback✔: Right — an `if` block runs only when its condition is true. Since `30 > 45` is false, `print('late')` is skipped entirely.  feedback✘: An `if` statement executes its block only when its condition is true. If the condition is false, Python skips the indented block and moves on.  hints: ['Evaluate `30 > 45` — is that true or false?', 'What does Python do with the indented block when the condition is false?']  remediation→r01
  MEASURES: A:explain_when_if_block_runs(f1)   anchors=['assessment:explain_when_if_block_runs']
  taught-before-tested: A.f1←s01

### s03 · check · Which branch runs?  [reward 5]
Quick check — Given a delivery time, predict which branch of an if/elif/else chain executes.
QUESTION [choice, core, grading=client] What does this code print when `delivery_minutes = 30`?

```python
delivery_minutes = 30
if delivery_minutes < 15:
    category = 'fast'
elif delivery_minutes < 45:
    category = 'normal'
else:
    category = 'slow'
print(category)
```
  ✔ opt_a: `normal`
      why: Correct. `30 < 15` is false, so the `if` branch is skipped. `30 < 45` is true, so the `elif` branch runs and `category` is set to `'normal'`.
  ✘ opt_b: `fast`
      why: The `if` condition `30 < 15` is false, so the `fast` branch is skipped. Python moves to the `elif`.
  ✘ opt_c: `slow`
      why: The `else` branch only runs when all earlier conditions are false. Here `30 < 45` is true, so the `elif` branch runs first and `else` is skipped.
  ✘ opt_d: Both `normal` and `slow` — two conditions are checked
      why: An if/elif/else chain selects exactly one branch — the first whose condition is true. Once `30 < 45` matches, no further branches are evaluated.
  feedback✔: Correct. Python evaluates conditions top to bottom and runs the first true branch. `30 < 15` is false; `30 < 45` is true, so `category = 'normal'`.  feedback✘: Evaluate each condition in order: `30 < 15` is false (skip `fast`); `30 < 45` is true (run `normal`). The chain stops there — `else` is never reached.  hints: ['Is `30 < 15` true or false? What happens to that branch?', 'After the `if` is skipped, Python checks the `elif`. Is `30 < 45` true?']  remediation→r02
  MEASURES: A:predict_branch_taken(f3)   anchors=['assessment:predict_branch_taken']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Write an if/elif/else chain  [reward 10]
Practice — Use the QuickDeliver dataset to write a chain that categorises each delivery as fast, normal, or slow.
QUESTION [code_exercise, core, grading=client] QuickDeliver classifies each order by speed.

`delivery_minutes` is already assigned below.

Add an `if`/`elif`/`else` chain that sets `category` to:
- `'fast'` when `delivery_minutes < 15`
- `'normal'` when `delivery_minutes < 45`
- `'slow'` otherwise

Then print `category`.

Expected output for the starter value:
```
normal
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block'] blocked=37 items
  file solution.py [editable]:
delivery_minutes = 38
# Write your if/elif/else chain here

  SOLUTION solution.py:
delivery_minutes = 38
if delivery_minutes < 15:
    category = 'fast'
elif delivery_minutes < 45:
    category = 'normal'
else:
    category = 'slow'
print(category)

  test t1_stdout (stdout_equals, visible=True): {"expected":"normal"} | on-fail: Expected output `normal` for delivery_minutes = 38. Check your elif condition.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a2805b7ebc80ff652bdf4d1ffb31eca36a8a80d46aa1add2f85c7efdade23dd1","tests_passed":1}
  feedback✔: Well done — exactly one branch ran and printed `normal` for `delivery_minutes = 38`.  feedback✘: Check that your chain has `if delivery_minutes < 15`, `elif delivery_minutes < 45`, and `else`, each ending with a colon and an indented body.  hints: ['Each branch header ends with a colon, and the body is indented four spaces beneath it.', 'Only one branch runs — the first whose condition is true. For `38`, which condition is true first?']  remediation→r02
  MEASURES: A:write_if_elif_else_chain(f2,f3,f4)   anchors=['practice', 'assessment:write_if_elif_else_chain']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f4←s01

### s05 · explainer · Visiting every item: the for loop  [reward 5]
Iteration — Process every delivery time in a list without writing the same code over and over.
### Visiting every item: the for loop
(mechanism) Once delivery times are collected in a list, you'll want to do something with every single one of them, not just one at a time by hand. Python's for statement iterates over the items of any sequence — such as a list or a string — in the order they appear. Each pass binds the loop variable to the next item:

for minutes in delivery_times:
    print(minutes)

This prints every delivery time in delivery_times, one per pass. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
(syntax) The header line ends with a colon, and the statements to repeat are indented beneath it. You can combine a for loop with a conditional check inside the body:

for minutes in delivery_times:
    if minutes > 45:
        print(minutes)

With delivery_times = [32, 45, 21, 60, 18], this prints only 60 — the one delivery time above 45 minutes. ⟦B.f2 B.f3 B:tb3 B:tb4⟧
[PROCESS_FLOW: How a for loop steps through delivery_times] nodes=['delivery_times = [32, 45, 21, 60, 18]', 'Next item available?', 'minutes = next item — e.g. 32, then 45, then 21 …', 'run loop body — print(minutes)', 'loop finished'] edges=[('start', 'check', None), ('check', 'bind', 'Yes'), ('check', 'end', 'No'), ('bind', 'body', None), ('body', 'check', None)] alt: Loop flow: check for next item, bind minutes to it, run the body, loop back; exit when no items remain.

### s06 · video · Stepping through a list with a for loop
Watch — See the loop variable take each value in turn.
[VIDEO Stepping through a list with a for loop] bridge-before: Follow the flow diagram, then watch the loop variable take each value in turn. The clip lists 'an array' among the things you can loop over; in Devspace terms that means a sequence such as a list or string. | bridge-after: The clip loops over numbers only and prints or adds them. The text adds a conditional inside the indented body and reuses the delivery-times list.
  - zmIdC0_0BgY 0-207s facts=['f1', 'f2', 'f3'] label: How Python for loops work: syntax, loop variable, and iteration over a list | summary: Opens with a flow diagram of a for loop over a list of five numbers: take the first item, run the body, move to the next, and exit after the last. Then writes it as code: for, a temporary loop variable, in, the list, and a colon, with the print of the variable in the body, printing 1 to 5. A second run prints a fixed word on every pass without using the item, showing the body repeats once per item, and a third renames the loop variable and adds each item to itself.

### s07 · check · Trace the loop variable  [reward 5]
Quick check — What value does the loop variable hold on each pass through the list?
QUESTION [choice, intro, grading=client] What does `minutes` equal on the **second** pass of this loop?

```python
delivery_times = [32, 45, 21]
for minutes in delivery_times:
    print(minutes)
```
  ✔ opt_a: `45`
      why: Correct. On the first pass `minutes` is `32`, on the second pass it is `45`, and on the third it is `21`.
  ✘ opt_b: `32`
      why: `32` is the value on the first pass. Each pass binds the loop variable to the next item in the sequence.
  ✘ opt_c: `21`
      why: `21` is the value on the third (last) pass. The second pass binds `minutes` to `45`.
  ✘ opt_d: `1` — the index of the second item
      why: A `for` loop binds the loop variable to the item itself, not its index. To get the index you would need `enumerate()`, which has not been taught yet.
  feedback✔: Right — each pass binds `minutes` to the next item in order: `32`, then `45`, then `21`.  feedback✘: Each pass through a `for` loop binds the loop variable to the next item of the sequence in order. The second item in `[32, 45, 21]` is `45`.  hints: ['List the items in `delivery_times` in order. Which one is at position 1 (the second item)?', 'On each pass, `minutes` is set to the next item — not its index.']  remediation→r03
  MEASURES: B:trace_loop_variable_each_pass(f2)   anchors=['assessment:trace_loop_variable_each_pass']
  taught-before-tested: B.f2←s05

### s08 · hands_on · Write a for loop over a collection  [reward 10]
Practice — Loop over the delivery_times list and print each time that exceeds 45 minutes.
QUESTION [code_exercise, core, grading=client] QuickDeliver wants the total delivery time across all orders.

`delivery_times` and `total` are already assigned below.

Add a `for` loop that visits every item in `delivery_times` and adds it to `total` using a plain assignment (`total = total + minutes`).

Then print `total`.

Expected output:
```
343
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:'] blocked=36 items
  file solution.py [editable]:
delivery_times = [32, 45, 21, 60, 18, 27, 50, 13, 41, 36]
total = 0
# Write your for loop here

  SOLUTION solution.py:
delivery_times = [32, 45, 21, 60, 18, 27, 50, 13, 41, 36]
total = 0
for minutes in delivery_times:
    total = total + minutes
print(total)

  test t1_stdout (stdout_equals, visible=True): {"expected":"343"} | on-fail: Expected output `343`. Make sure your loop adds each item to `total` and you print `total` after the loop.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"abbc997f24d66f2f131ab72a467feada6232aa3765593b732114a175fbd15137","tests_passed":1}
  feedback✔: The loop visited all 10 items and the total is 343. Every item was processed exactly once.  feedback✘: Make sure your `for` loop header ends with a colon, the body is indented, and you use `total = total + minutes` (not `+=`) to accumulate the sum.  hints: ['The loop header is `for minutes in delivery_times:` — the body runs once per item.', 'Inside the loop, update `total` with `total = total + minutes`, then print `total` after the loop ends.']  remediation→r03
  MEASURES: B:write_for_loop_over_collection(f1,f2,f3)   anchors=['practice', 'assessment:write_for_loop_over_collection']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05

### s09 · recap · What you've learned  [reward 5]
Recap — One branch, every item.
(takeaway) Reading top to bottom, exactly one branch of an if/elif/else chain runs for any given delivery time — the first whose condition is true, or else if none are. A for loop visits every item of a sequence such as a list once, in the order the items appear, which is what you need to process each delivery time in turn. ⟦A.f3 B.f1 A:tb5 B:tb5⟧
[UP NEXT] Up next: While Loops and Loop Control: Next you'll learn how to keep a loop running as long as a condition holds — and how to exit or skip iterations mid-loop.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · When does an if block run? — Let's revisit the rule for when an if block executes.
### Reminder: when does an if block run?
(mechanism) An if statement executes its block only when its condition is true — not every time the code runs. If delivery_minutes = 30 and the condition is delivery_minutes > 45, the block is skipped entirely. The block runs only when the condition evaluates to True. ⟦A.f1 A:tb1⟧
### r02 · Which branch runs in a chain? — Let's revisit how an if/elif/else chain selects exactly one branch.
### Reminder: which branch runs in a chain?
(mechanism) An if/elif/else chain evaluates conditions one by one from top to bottom. The first condition that is true wins — its block runs and all others are skipped. If no condition is true, the else block (if present) runs. With delivery_minutes = 30: the first condition (< 15) is false, the second (< 45) is true, so category = 'normal' runs and the else branch is skipped. ⟦A.f3 A:tb3⟧
### r03 · What value does the loop variable hold? — Let's revisit how the loop variable takes each value in turn.
### Reminder: what value does the loop variable hold?
(mechanism) Each pass through a for loop binds the loop variable to the next item of the sequence. With delivery_times = [32, 45, 21, 60, 18], the first pass sets minutes = 32, the second sets minutes = 45, and so on. The variable takes each value in order, one per pass. ⟦B.f2 B:tb2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment

=========

# EVALUATOR PACKET — While Loops and Loop Control (tile_python_while_loop_control)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.while_loops — While loops
B = python.loop_control — Loop control statements (break, continue)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_python_while_loop_control.s04: remediation tile_python_while_loop_control.r01 re-teaches ['python.while_loops#f2'] but the check measures ['python.while_loops#f1'] — a learner who fails it is sent to an unrelated fact

## SOURCE FACTS — A (python.while_loops)   objective: Write a while loop that repeats its body only while a condition remains true, and stops once the condition becomes false.
A.f1: A while loop executes its body repeatedly as long as its condition remains true; the condition can be a comparison, such as a < 10.   [sources: python_docs_tutorial_introduction#first-steps-towards-programming]
A.f2: The body of a while loop is indented beneath it; in the Fibonacci example, a, b = b, a+b updates a on each pass, and the loop stops once a < 10 becomes false.   [sources: python_docs_tutorial_introduction#first-steps-towards-programming]
note: TOC conflict: the practice_objective says 'keeps prompting for input until a valid value is entered', but input() is not taught before this concept. The practice anchor uses a counter or running value that the loop body updates instead.
PRACTICE ANCHOR (live_code): Write a while loop that repeats until a variable reaches a limit, with the body changing that variable each pass.  SUCCESS: The loop runs a predictable number of times and stops; the final value of the variable shows the loop ended because the condition became false.
ASSESSMENT ANCHOR: write_while_loop_with_condition facts=['f1']
ASSESSMENT ANCHOR: update_state_so_loop_terminates facts=['f2']

## SOURCE FACTS — B (python.loop_control)   objective: Use break to exit a loop as soon as a target is found, and continue to skip the rest of an iteration for values that should be ignored.
B.f1: The break statement breaks out of the innermost enclosing for or while loop.   [sources: python_docs_tutorial_controlflow#break-and-continue-statements]
B.f2: The continue statement continues with the next iteration of the loop, skipping the rest of the current one.   [sources: python_docs_tutorial_controlflow#break-and-continue-statements]
PRACTICE ANCHOR (live_code): Write a loop over a list that skips invalid entries with continue and stops with break as soon as a target is found.  SUCCESS: Invalid entries are ignored, the loop stops at the first match, and nothing after the match is processed.
ASSESSMENT ANCHOR: exit_loop_early_with_break facts=['f1']
ASSESSMENT ANCHOR: skip_iteration_with_continue facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Comparing correlation strength across multiple variable pairs; Computing descriptive statistics with pandas (describe, mean, median, std); Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Default and keyword arguments; Defining calling functions; Distribution shape (skewness, symmetry, outliers); Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Inspecting data (head, info, describe, shape, dtypes); Iterating over data structures; List and dict comprehensions; Loop control statements (break, continue); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Return values; Selecting rows/columns with loc/iloc; Series and DataFrame data structures; Variable scope (local vs global)

## LESSON, in learner order

### s01 · explainer · Repeating while a condition holds: the while loop  [reward 5]
Loops — Keep processing deliveries as long as there are still orders to handle.
### Repeating while a condition holds: the while loop
(intro) Sometimes you don't know in advance how many times you'll need to repeat something — you just want to keep going as long as some condition holds. A while loop executes its body repeatedly as long as its condition remains true; the condition can be a comparison, such as a < 10. ⟦A.f1 A:tb1⟧
(mechanism) The body is indented beneath the while line, and something in the body must change what the condition checks — otherwise the loop never stops:

pending = 3
while pending > 0:
    print('deliveries left:', pending)
    pending = pending - 1

Each pass prints the current count and decreases pending by 1, so the loop stops once pending reaches 0. ⟦A.f2 A:tb2 A:tb3⟧
[PROCESS_FLOW: How a while loop re-checks its condition each pass] nodes=['pending = 3', 'pending > 0?', "print('deliveries left:', pending)", 'pending = pending - 1 — update must change what the condition checks', 'loop finished (pending = 0)'] edges=[('init', 'cond', None), ('cond', 'body1', 'True'), ('cond', 'end', 'False'), ('body1', 'update', None), ('update', 'cond', None)] alt: While loop flow: initialise pending = 3, check pending > 0, run body and decrement, loop back to check; exit when pending = 0.

### s02 · video · A while loop as a counter
Watch — See how the condition is re-checked each pass and what happens without an update.
[VIDEO A while loop as a counter] bridge-before: Watch the trace: each pass re-checks the condition, and with no update line the same check passes forever. The clip counts up with i; Devspace's examples use a Fibonacci-style update and a countdown of pending deliveries. | bridge-after: Both Devspace examples rely on the same idea from the recap: the body must change what the condition checks, or the loop never stops.
  - gD8ePxAhjUM 178-421s facts=['f1', 'f2'] label: Visually explained: building a while-loop counter, including the infinite-loop trap and the fix | summary: Builds a counter with a while loop: write while, a condition such as i smaller than 4, and a body that prints i. Without first assigning i the code fails, so the clip sets i to 1 before the loop. It then traces why the loop never ends when nothing changes i, and fixes that by adding 1 to i on each pass, tracing i from 1 to 4 until the condition becomes false and the loop exits. The recap names three parts: an initial value before the loop, the condition, and an update inside the body.

### s03 · check · Making a while loop terminate  [reward 5]
Quick check — Which change to the loop body ensures the loop eventually stops?
QUESTION [choice, intro, grading=client] Why must the body of a `while` loop change the value its condition checks?

```python
pending = 3
while pending > 0:
    print('deliveries left:', pending)
    pending = pending - 1
```
  ✔ opt_a: So the condition eventually becomes false and the loop stops
      why: Correct. If the body never changes what the condition checks, the condition stays true forever and the loop never stops.
  ✘ opt_b: So the loop variable is available after the loop ends
      why: Variable availability is not the reason. The body must update the condition's variable so the condition can eventually become false and the loop can stop.
  ✘ opt_c: So Python knows how many times to repeat the loop
      why: A `while` loop does not know in advance how many times it will run — that is the key difference from a `for` loop. It keeps going until the condition becomes false.
  ✘ opt_d: So the condition is checked only once at the start
      why: A `while` loop re-checks its condition before every pass, not just once. The body must change the variable so the condition can eventually become false.
  feedback✔: Right — if nothing in the body changes what the condition checks, the condition stays true forever and the loop runs without stopping.  feedback✘: A `while` loop re-checks its condition before every pass. If the body never changes the variable the condition tests, the condition stays true and the loop never ends.  hints: ['What happens to `pending` on each pass? What would happen if that line were missing?', 'A `while` loop stops only when its condition becomes false — what makes it false here?']  remediation→r01
  MEASURES: A:update_state_so_loop_terminates(f2)   anchors=['assessment:update_state_so_loop_terminates']
  taught-before-tested: A.f2←s01

### s04 · hands_on · Write a while loop with a condition  [reward 10]
Practice — Write a while loop that counts down pending deliveries until none remain.
QUESTION [code_exercise, core, grading=client] QuickDeliver's dispatcher tracks how many deliveries are still pending.

`pending` is already assigned below.

Add a `while` loop that:
1. Runs as long as `pending > 0`
2. Prints `'deliveries left:'` followed by the current value of `pending`
3. Decreases `pending` by 1 each pass using `pending = pending - 1`

Expected output:
```
deliveries left: 3
deliveries left: 2
deliveries left: 1
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:'] blocked=35 items
  file solution.py [editable]:
pending = 3
# Write your while loop here

  SOLUTION solution.py:
pending = 3
while pending > 0:
    print('deliveries left:', pending)
    pending = pending - 1

  test t1_stdout (stdout_equals, visible=True): {"expected":"deliveries left: 3\ndeliveries left: 2\ndeliveries left: 1"} | on-fail: Expected three lines counting down from 3. Check your condition and the update step.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"3216d5678adb98da8bae9be90d9e0e2b34b972bf80a0e4690c823ec234f1dc23","tests_passed":1}
  feedback✔: The loop ran exactly 3 times and stopped once `pending` reached 0 — the condition became false.  feedback✘: Make sure the `while` header is `while pending > 0:`, the body prints `pending`, and then decreases it with `pending = pending - 1`.  hints: ['The loop header ends with a colon; the body is indented beneath it.', 'Without `pending = pending - 1` inside the loop, `pending` never changes and the loop runs forever.']  remediation→r01
  MEASURES: A:write_while_loop_with_condition(f1)   anchors=['practice', 'assessment:write_while_loop_with_condition']
  taught-before-tested: A.f1←s01

### s05 · explainer · Steering mid-loop: break and continue  [reward 5]
Loop control — Exit a loop early or skip a bad record without stopping the whole loop.
### Steering mid-loop: break and continue
(mechanism) The break statement exits the innermost enclosing for or while loop immediately — useful for stopping a search over delivery orders as soon as the one you want is found. The continue statement skips the rest of the current iteration and moves to the next one — for example, skipping a delivery record that's missing a time without exiting the whole loop. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
[PROCESS_FLOW: break exits the loop; continue skips to the next item] nodes=['start loop', 'next item available?', 'run body', 'continue condition? — e.g. missing delivery time', 'break condition? — e.g. target order found', 'loop finished', 'exited by break'] edges=[('start', 'next_item', None), ('next_item', 'body', 'Yes'), ('next_item', 'end_loop', 'No'), ('body', 'cont_dec', None), ('cont_dec', 'next_item', 'continue'), ('cont_dec', 'brk_dec', 'No'), ('brk_dec', 'end_break', 'break'), ('brk_dec', 'next_item', 'No')] alt: Loop flow with two side exits: continue jumps back to the next item check, break exits the loop entirely.

### s06 · check · Skip an iteration with continue  [reward 5]
Quick check — Which statement skips the rest of the current iteration and moves to the next?
QUESTION [choice, core, grading=client] What does this code print?

```python
delivery_times = [32, -5, 21]
for minutes in delivery_times:
    if minutes < 0:
        continue
    print(minutes)
```
  ✔ opt_a: `32` and `21` — the negative value is skipped
      why: Correct. `continue` skips the rest of the current iteration and moves to the next item. `-5 < 0` is true, so `print(-5)` is skipped; `32` and `21` are printed.
  ✘ opt_b: `32`, `-5`, and `21` — `continue` does not remove items
      why: `continue` skips the remaining statements in the current iteration. When `minutes` is `-5`, `continue` jumps to the next item before `print` is reached.
  ✘ opt_c: `32` only — the loop stops when it hits `-5`
      why: `continue` does not stop the loop — it only skips the rest of the current iteration. `break` is the statement that exits the loop early.
  ✘ opt_d: Nothing — `continue` exits the loop immediately
      why: `continue` does not exit the loop. It skips the rest of the current iteration and moves to the next item. `break` is what exits the loop entirely.
  feedback✔: `continue` skips the rest of the current iteration. For `-5`, the `print` is never reached; the loop continues with `21`.  feedback✘: `continue` skips the remaining statements in the current pass and moves to the next item. It does not stop the loop — that is what `break` does.  hints: ['When `minutes = -5`, the `if` condition is true. What does `continue` do at that point?', 'After `continue`, does the loop end or does it move to the next item?']  remediation→r02
  MEASURES: B:skip_iteration_with_continue(f2)   anchors=['assessment:skip_iteration_with_continue']
  taught-before-tested: B.f2←s05

### s07 · hands_on · Use break and continue in a loop  [reward 10]
Practice — Write a loop that skips orders with missing times and stops as soon as a late order is found.
QUESTION [code_exercise, stretch, grading=client] QuickDeliver's script scans a list of delivery times to find a target value, skipping any invalid (negative) entries.

`delivery_times` and `target` are already assigned below.

Add a `for` loop that:
1. Skips any item that is less than `0` using `continue`
2. Prints `'found:'` followed by the item when it equals `target`, then stops the loop with `break`

Expected output:
```
found: 45
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue'] blocked=33 items
  file solution.py [editable]:
delivery_times = [32, -5, 45, 21, 60, 18]
target = 45
# Write your for loop here

  SOLUTION solution.py:
delivery_times = [32, -5, 45, 21, 60, 18]
target = 45
for minutes in delivery_times:
    if minutes < 0:
        continue
    if minutes == target:
        print('found:', minutes)
        break

  test t1_stdout (stdout_equals, visible=True): {"expected":"found: 45"} | on-fail: Expected output `found: 45`. Check that you skip negatives with `continue` and stop at the target with `break`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f586749a447c24f950df3fe238eb58085cebd9d51699c8e40b7063f2a900cf94","tests_passed":1}
  feedback✔: The loop skipped `-5` with `continue`, found `45`, printed it, and stopped — nothing after the match was processed.  feedback✘: Use `continue` to skip items where `minutes < 0`, and `break` to stop the loop once `minutes == target`. Both must be inside the loop body.  hints: ['Handle the invalid entry first: `if minutes < 0: continue` skips the rest of that pass.', "To stop at the target: `if minutes == target: print('found:', minutes)` then `break`."]  remediation→r02
  MEASURES: B:exit_loop_early_with_break(f1); B:skip_iteration_with_continue(f2)   anchors=['practice', 'assessment:exit_loop_early_with_break', 'assessment:skip_iteration_with_continue']
  taught-before-tested: B.f1←s05; B.f2←s05

### s08 · recap · What you've learned  [reward 5]
Recap — Condition-driven loops and mid-loop steering.
(takeaway) Unlike a for loop, which is bound to a known collection, a while loop keeps running purely based on its condition — so the code inside it must eventually make that condition false or the loop never stops. Use break to exit a loop early and continue to skip the rest of the current iteration. ⟦A.f1 A.f2 B.f1 B.f2 A:tb4⟧
[UP NEXT] Up next: Comprehensions and Iterating Collections: Next you'll learn how to build lists and dictionaries in a single expression, and how to loop over any of Python's core collection types.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · The body must change what the condition checks — Let's revisit why the loop body must update the condition variable.
### Reminder: the body must change what the condition checks
(mechanism) The body of a while loop must change what the condition checks — otherwise the condition stays true forever and the loop never stops. In the pending example, pending = pending - 1 decreases pending each pass, so pending > 0 eventually becomes false and the loop exits. ⟦A.f2 A:tb2⟧
### r02 · continue vs break — Let's revisit the difference between continue and break.
### Reminder: continue vs break
(mechanism) continue skips the rest of the current iteration and moves to the next one — the loop keeps running. break exits the innermost loop entirely — no more iterations happen. Use continue to skip a bad record; use break to stop searching once you've found what you need. ⟦B.f1 B.f2 B:tb1 B:tb2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· expected.value: deliveries left: 10
deliveries left: 9
deliveries left: 8
deliveries left: 7
deliveries left: 6
deliveries left: 5
deliveries left: 4
deliveries left: 3
deliveries left: 2
deliveries left: 1
· constraints.blocked_syntax: [expr for x in seq if cond]
· constraints.blocked_syntax: for k, v in d.items():
· constraints.blocked_syntax: positional arguments in a call
· constraints.blocked_syntax: def f(a, b=default):
· constraints.blocked_syntax: keyword arguments f(name=value)
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment