# EVALUATOR PACKET — Conditionals and For Loops (tile_python_conditionals_for_loops)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.conditional_statements — Control flow: if/elif/else
B = python.for_loops — For loops

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Which branch runs?  [reward 5]
Quick check — Given a delivery time, predict which branch of an if/elif/else chain executes.

### s04 · hands_on · Write an if/elif/else chain  [reward 10]
Practice — Use the QuickDeliver dataset to write a chain that categorises each delivery as fast, normal, or slow.

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
[VIDEO Stepping through a list with a for loop] bridge-before:  | bridge-after: 

### s07 · check · Trace the loop variable  [reward 5]
Quick check — What value does the loop variable hold on each pass through the list?

### s08 · hands_on · Write a for loop over a collection  [reward 10]
Practice — Loop over the delivery_times list and print each time that exceeds 45 minutes.

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

=========

# EVALUATOR PACKET — While Loops and Loop Control (tile_python_while_loop_control)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.while_loops — While loops
B = python.loop_control — Loop control statements (break, continue)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO A while loop as a counter] bridge-before:  | bridge-after: 

### s03 · check · Making a while loop terminate  [reward 5]
Quick check — Which change to the loop body ensures the loop eventually stops?

### s04 · hands_on · Write a while loop with a condition  [reward 10]
Practice — Write a while loop that counts down pending deliveries until none remain.

### s05 · explainer · Steering mid-loop: break and continue  [reward 5]
Loop control — Exit a loop early or skip a bad record without stopping the whole loop.
### Steering mid-loop: break and continue
(mechanism) The break statement exits the innermost enclosing for or while loop immediately — useful for stopping a search over delivery orders as soon as the one you want is found. The continue statement skips the rest of the current iteration and moves to the next one — for example, skipping a delivery record that's missing a time without exiting the whole loop. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
[PROCESS_FLOW: break exits the loop; continue skips to the next item] nodes=['start loop', 'next item available?', 'run body', 'continue condition? — e.g. missing delivery time', 'break condition? — e.g. target order found', 'loop finished', 'exited by break'] edges=[('start', 'next_item', None), ('next_item', 'body', 'Yes'), ('next_item', 'end_loop', 'No'), ('body', 'cont_dec', None), ('cont_dec', 'next_item', 'continue'), ('cont_dec', 'brk_dec', 'No'), ('brk_dec', 'end_break', 'break'), ('brk_dec', 'next_item', 'No')] alt: Loop flow with two side exits: continue jumps back to the next item check, break exits the loop entirely.

### s06 · check · Skip an iteration with continue  [reward 5]
Quick check — Which statement skips the rest of the current iteration and moves to the next?

### s07 · hands_on · Use break and continue in a loop  [reward 10]
Practice — Write a loop that skips orders with missing times and stops as soon as a late order is found.

### s08 · recap · What you've learned  [reward 5]
Recap — Condition-driven loops and mid-loop steering.
(takeaway) Unlike a for loop, which is bound to a known collection, a while loop keeps running purely based on its condition — so the code inside it must eventually make that condition false or the loop never stops. Use break to exit a loop early and continue to skip the rest of the current iteration. ⟦A.f1 A.f2 A:tb4⟧
[UP NEXT] Up next: Comprehensions and Iterating Collections: Next you'll learn how to build lists and dictionaries in a single expression, and how to loop over any of Python's core collection types.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · The body must change what the condition checks — Let's revisit why the loop body must update the condition variable.
### Reminder: the body must change what the condition checks
(mechanism) The body of a while loop must change what the condition checks — otherwise the condition stays true forever and the loop never stops. In the pending example, pending = pending - 1 decreases pending each pass, so pending > 0 eventually becomes false and the loop exits. ⟦A.f2 A:tb2⟧
### r02 · continue vs break — Let's revisit the difference between continue and break.
### Reminder: continue vs break
(mechanism) continue skips the rest of the current iteration and moves to the next one — the loop keeps running. break exits the innermost loop entirely — no more iterations happen. Use continue to skip a bad record; use break to stop searching once you've found what you need. ⟦B.f1 B.f2 B:tb1 B:tb2⟧

=========

# EVALUATOR PACKET — Comprehensions and Iterating Collections (tile_python_comprehensions_iterating)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.comprehensions — List and dict comprehensions
B = python.iterating_collections — Iterating over data structures

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
(definition) Building a new list from an existing one by looping is common enough that Python has a shorthand for it. A list comprehension consists of brackets containing an expression followed by a for clause, and optionally an if clause; it produces a new list by evaluating the expression for each item — [minutes * 2 for minutes in delivery_times] doubles every value. ⟦A.f1 A:tb1⟧
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

### s03 · hands_on · Write list and dict comprehensions  [reward 10]
Practice — Use comprehensions to filter delivery times and build a city-length dictionary.

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

# each integer key in insertion order
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

### s06 · hands_on · Loop over keys and key-value pairs  [reward 10]
Practice — Write loops that iterate over the order_city dictionary — first keys only, then key-value pairs.

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