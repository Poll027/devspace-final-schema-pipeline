# EVALUATOR PACKET — Handling Errors and Importing Modules (tile_python_errors_imports)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.error_handling — Basic error handling (try/except)
B = python.import_statements — Modules and imports

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (python.error_handling)   objective: Wrap code that might fail in a try/except block so the program prints a helpful message instead of crashing when the exception occurs.
A.f1: The try statement first executes the statements in its try clause; if no exception occurs, the except clause is skipped and execution of the try statement finishes.   [sources: python_docs_tutorial_errors#handling-exceptions]
A.f2: If an exception occurs during the try clause and its type matches the exception named after except, the except clause is executed and execution continues after the try/except block.   [sources: python_docs_tutorial_errors#handling-exceptions]
A.f3: For example, wrapping int(input(...)) in a try clause with except ValueError lets the program print a message such as 'Oops! That was no valid number. Try again...' instead of crashing when the conversion fails.   [sources: python_docs_tutorial_errors#handling-exceptions]
PRACTICE ANCHOR (live_code): Convert user input to a number inside try/except and print a friendly message if the conversion fails.  SUCCESS: Valid input is converted and used; invalid input prints the message instead of crashing.
ASSESSMENT ANCHOR: wrap_code_in_try_except facts=['f1', 'f2']
ASSESSMENT ANCHOR: handle_invalid_number_conversion facts=['f3']

## SOURCE FACTS — B (python.import_statements)   objective: Import a module with import, and access the names it defines through the module's name.
B.f1: A module is a file containing Python definitions and statements; definitions from a module can be imported into another module or into the main script with the import statement, e.g. import fibo.   [sources: python_docs_tutorial_modules#modules]
B.f2: Importing a module this way does not add the names defined in it directly to the current namespace; it adds the module name, so its functions are accessed through that name, e.g. fibo.fib(1000).   [sources: python_docs_tutorial_modules#modules]
B.f3: The from module import name variant imports names from a module directly into the importing module's namespace, e.g. from fibo import fib, so it can then be called as fib(500) without the module prefix.   [sources: python_docs_tutorial_modules#more-on-modules]
B.f4: Python comes with a library of standard modules that are imported the same way, e.g. import sys makes the sys module's names, such as sys.path, available through sys.   [sources: python_docs_tutorial_modules#standard-modules]
note: The math function to call is named in the practice starter, because the facts only teach the import mechanics (fibo and sys), not any specific math function.
note: Logged upstream gap: no fact covers the 'import X as Y' alias form.
PRACTICE ANCHOR (live_code): Import the math module and use one of its functions through the module name.  SUCCESS: The import line appears at the top and a module function is called as math.name(...).
ASSESSMENT ANCHOR: write_correct_import_statement facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: import_standard_module facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic file I/O (reading/writing text and CSV files); Boolean/conditional filtering; Comparing correlation strength across multiple variable pairs; Computing descriptive statistics with pandas (describe, mean, median, std); Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Distribution shape (skewness, symmetry, outliers); Handling missing data (isna, dropna, fillna); Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Inspecting data (head, info, describe, shape, dtypes); Map substitution; Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Removing duplicate rows; Renaming columns and index labels; Selecting rows/columns with loc/iloc; Series and DataFrame data structures; Sorting values; String cleaning with the .str accessor; Type conversion and dtype management (astype); Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Catch failures before they crash your script  [reward 5]
Error handling — A try/except block lets your code attempt something that might fail and respond to the specific failure instead of stopping entirely.
(intro) The `try` statement first executes the statements in its `try` clause. If no exception occurs, the `except` clause is skipped and execution continues normally after the block. ⟦A.f1 A:tb1⟧
(mechanism) If an exception occurs during the `try` clause and its type matches the exception named after `except`, the `except` clause is executed and execution continues after the `try`/`except` block. An unmatched exception propagates upward. ⟦A.f2 A:tb2⟧
(example) Wrapping `int(input(...))` in a `try` clause with `except ValueError` lets the program print `'Oops! That was no valid number. Try again...'` instead of crashing when the conversion fails. If the input is `'twelve'`, `int()` raises a `ValueError`, the `except` clause runs, and the program continues. ⟦A.f3 A:tb3⟧
[PROCESS_FLOW: try/except execution flow] nodes=['Execute try clause', 'Exception occurred?', 'Skip except clause', 'Exception raised', 'Type matches except?', 'Run except clause', 'Continue after block'] edges=[('n_try', 'n_ok', None), ('n_ok', 'n_skip', 'no'), ('n_ok', 'n_exc', 'yes'), ('n_skip', 'n_cont', None), ('n_exc', 'n_match', None), ('n_match', 'n_run', 'yes'), ('n_run', 'n_cont', None)] alt: Flowchart: 'Execute try clause' leads to a decision 'Exception occurred?'. No path goes to 'Skip except clause' then 'Continue'. Yes path goes to 'Exception raised', then 'Type matches except?'. Yes path goes to 'Run except clause' then 'Continue'.

### s02 · check · Handle an invalid number conversion  [reward 5]
Quick check — Which code correctly catches a ValueError when converting user input to an integer?
QUESTION [choice, intro, grading=client] ```python
try:
    minutes = int('fast')
except ValueError:
    print('Not a valid number')
```

What does this code print?
  ✘ opt_a: Nothing — the program crashes with a `ValueError`.
      why: The `except ValueError:` clause catches the error, so the program does not crash. It prints the message instead.
  ✔ opt_b: `Not a valid number`
      why: Correct. `int('fast')` raises a `ValueError`, which the `except ValueError:` clause catches, printing 'Not a valid number'.
  ✘ opt_c: `0` — Python converts non-numeric strings to `0`.
      why: Python does not convert non-numeric strings to `0`. `int('fast')` raises a `ValueError`.
  ✘ opt_d: `ValueError` — the exception message is printed automatically.
      why: Python does not automatically print exception messages. The `except` clause runs your code — in this case `print('Not a valid number')`.
  feedback✔: Right — `int('fast')` raises a `ValueError`, the `except ValueError:` clause catches it, and the message is printed.  feedback✘: When `int()` cannot convert a string, it raises a `ValueError`. The `except ValueError:` clause catches it and runs the code inside — here, printing the message.  hints: ["What does `int('fast')` do? Can it convert the string 'fast' to an integer?", "When an exception matches the `except` clause, the clause's body runs instead of crashing."]  remediation→r01
  MEASURES: A:handle_invalid_number_conversion(f3)   anchors=['assessment:handle_invalid_number_conversion']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Wrap risky code in try/except  [reward 10]
Practice — Add a try/except block so the script prints a message instead of crashing on bad input.
QUESTION [code_exercise, core, grading=client] `raw_input` holds a string that may or may not be a valid integer.

Wrap `int(raw_input)` in a `try`/`except ValueError` block:
- If the conversion succeeds, print the integer value.
- If it raises a `ValueError`, print exactly: `Not a valid number`

With `raw_input = '55'`, the output should be `55`.
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call', 'return', 'def f(a, b=default):', 'keyword arguments f(name=value)', 'global statement', 'try:', 'except ValueError:', 'input()'] blocked=17 items
  file solution.py [editable]:
# raw_input simulates what a user typed.
# Wrap the int() conversion in try/except ValueError.
# If conversion succeeds, print the integer value.
# If it fails, print: 'Not a valid number'

raw_input = '55'

  SOLUTION solution.py:
raw_input = '55'

try:
    minutes = int(raw_input)
    print(minutes)
except ValueError:
    print('Not a valid number')

  test t1_valid_input (stdout_equals, visible=True): {"expected":"55"} | on-fail: With raw_input='55', the program should print `55`. Make sure you print the converted integer inside the try block.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4ad82d66e1bea43c324d1288f778bbc9d34d55bfa5081708bac4cf635ee18ec1","tests_passed":1}
  feedback✔: Well done — the `try` block converts the string and the `except ValueError` clause catches any conversion failure gracefully.  feedback✘: Write `try:` then `minutes = int(raw_input)` and `print(minutes)` indented under it. Then `except ValueError:` and `print('Not a valid number')` indented under that.  hints: ['The `try:` block contains the code that might fail. Put `int(raw_input)` and the print inside it.', 'The `except ValueError:` block runs only when `int()` raises a ValueError. Put your error message print there.']  remediation→r01
  MEASURES: A:wrap_code_in_try_except(f1,f2); A:handle_invalid_number_conversion(f3)   anchors=['practice', 'assessment:wrap_code_in_try_except', 'assessment:handle_invalid_number_conversion']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s04 · explainer · Bring in code from other files  [reward 5]
Modules — A module is a file of Python definitions; import gives your script access to them.
(intro) A module is a file containing Python definitions and statements. Definitions from a module can be imported into another module or into the main script with the `import` statement — `import fibo` makes the module available under the name `fibo`. ⟦B.f1 B:tb1⟧
(mechanism) Importing a module this way does not add the names defined in it directly to the current namespace — it adds the module name. Its functions are accessed through that name: `fibo.fib(1000)`. The `from module import name` variant imports names directly into the current namespace, so `from fibo import fib` lets you call `fib(500)` without the module prefix. ⟦B.f2 B.f3 B:tb2 B:tb3⟧
(example) Python comes with a library of standard modules imported the same way. `import sys` makes the `sys` module's names — such as `sys.path` — available through `sys`. `import math` gives access to `math.sqrt`, `math.pi`, and so on. ⟦B.f4 B:tb4⟧
[SIDE_BY_SIDE] import module keeps names behind the module prefix; from module import name brings them directly into scope. left_label: import module | right_label: from module import name
  left:
[CODE python]
import fibo

fibo.fib(1000)   # module prefix required
fibo.fib2(100)
  annotations: ['Names accessed through the module name']
  right:
[CODE python]
from fibo import fib

fib(500)         # no prefix needed
  annotations: ['Name imported directly into namespace']

### s05 · check · Write the correct import  [reward 5]
Quick check — Which statement correctly imports fib so it can be called as fib(500)?
QUESTION [choice, intro, grading=client] After running `import fibo`, how do you call the `fib` function from that module?
  ✘ opt_a: `fib(1000)` — `import fibo` adds `fib` directly to the namespace.
      why: `import fibo` adds the module name `fibo` to the namespace, not the names inside it. To call `fib` directly, you would need `from fibo import fib`.
  ✔ opt_b: `fibo.fib(1000)` — the module name is the prefix.
      why: Correct. `import fibo` adds the module name `fibo`. Its functions are accessed through that name: `fibo.fib(1000)`.
  ✘ opt_c: `import fibo.fib(1000)` — you import and call in one step.
      why: `import` is a statement, not a function call. You import the module first, then call its functions separately.
  ✘ opt_d: `fibo(fib, 1000)` — you pass the function name as an argument.
      why: Python does not use this syntax. After `import fibo`, call the function as `fibo.fib(1000)`.
  feedback✔: Right — `import fibo` adds the module name. Functions inside it are accessed as `fibo.fib(1000)`.  feedback✘: `import fibo` adds the module name `fibo` to the namespace. To call a function inside it, use `fibo.fib(1000)` — the module name as a prefix.  hints: ['What does `import fibo` add to the namespace — the module name, or all the names inside the module?', 'To access a name inside a module, use the dot notation: `module_name.function_name()`.']  remediation→r02
  MEASURES: B:write_correct_import_statement(f1,f2,f3)   anchors=['assessment:write_correct_import_statement']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s06 · hands_on · Import and use a standard module  [reward 10]
Practice — Import the math module and use math.sqrt() to compute a square root.
QUESTION [code_exercise, core, grading=client] A starter variable `x = 144` is already defined.

1. Write `import math` at the top of the file.
2. Compute the square root of `x` using `math.sqrt(x)` and store the result in a variable called `result`.
3. Print `result`.

Expected output: `12.0`
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call', 'return', 'def f(a, b=default):', 'keyword arguments f(name=value)', 'global statement', 'try:', 'except ValueError:', 'input()', 'import module', 'module.name', 'from module import name'] blocked=14 items
  file solution.py [editable]:
# Import the math module and use math.sqrt() on x.
# Store the result in a variable called result and print it.

x = 144

  SOLUTION solution.py:
import math

x = 144
result = math.sqrt(x)
print(result)

  test t1_result (value_equals, visible=True): {"expr":"result","expected":12.0,"tolerance":1e-09} | on-fail: `result` should hold `12.0` (math.sqrt(144)). Make sure you write `result = math.sqrt(x)`.
  test t2_stdout (stdout_equals, visible=True): {"expected":"12.0"} | on-fail: The program should print `12.0`. Check that you call `print(result)` after the assignment.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2e293ec4ffea056d511576a1a9104a7d7b6e87d80151866dbb706869df15c3ce","tests_passed":2}
  feedback✔: Well done — `import math` adds the module to the namespace, and `math.sqrt(x)` calls the module function to compute the square root.  feedback✘: Write `import math` at the top, then `result = math.sqrt(x)`, then `print(result)`.  hints: ['The import statement goes at the top: `import math`.', 'Compute the square root by calling the module function: `result = math.sqrt(x)`.']
  MEASURES: B:import_standard_module(f4)   anchors=['practice', 'assessment:import_standard_module']
  taught-before-tested: B.f4←s04

### s07 · recap · Errors and imports: what you've learned  [reward 5]
Recap — Two tools that make scripts more robust and reusable.
(takeaway) `try`/`except` lets the program attempt something that might fail and respond to the specific failure rather than stopping entirely. If no exception occurs, the `except` clause is skipped; if the exception type matches, the `except` clause runs and execution continues. `import` gives you access to code written in another file — either through the module's name (`import fibo`, `fibo.fib(...)`) or directly by name (`from fibo import fib`, `fib(...)`). ⟦A.f1 A.f2 B.f2 B.f3 A:tb4 B:tb5⟧
[UP NEXT] Up next: Reading and writing files: Next you will learn how open() and the with statement manage file connections, and how the csv module reads and writes rows as dictionaries.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Catching a ValueError from int() — The except clause only runs when the exception type matches.
(example) Wrapping `int(input(...))` in a `try` clause with `except ValueError` catches the error when the input cannot be converted. If the typed text is `'twelve'`, `int()` raises a `ValueError`, the `except` clause runs and prints a message, and the program continues. If the input is `'12'`, `int()` succeeds, the `except` clause is skipped, and `minutes_late` holds `12`. ⟦A.f3 A:tb3⟧
### r02 · import vs from … import — The two forms differ in what lands in your namespace.
(mechanism) `import fibo` adds the module name `fibo` to your namespace; you then call `fibo.fib(1000)`. `from fibo import fib` adds the name `fib` directly, so you call `fib(500)` without a prefix. Both forms import from the same module file — they differ only in what name lands in your namespace. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment

=========

# EVALUATOR PACKET — Reading and Writing Files (tile_python_file_io)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.file_io — Basic file I/O (reading/writing text and CSV files)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_python_file_io.s06: remediation tile_python_file_io.r01 re-teaches ['python.file_io#f1', 'python.file_io#f3', 'python.file_io#f5'] but the check measures ['python.file_io#f4', 'python.file_io#f7'] — a learner who fails it is sent to an unrelated fact

## SOURCE FACTS — A (python.file_io)   objective: Open, read from, and write to text and CSV files using Python's open() function and the csv module, closing the file resource properly.
A.f1: open(filename, mode) returns a file object; mode can be 'r' to read, 'w' to write (erasing an existing file of the same name), or 'a' to append, and 'r' is assumed if mode is omitted.   [sources: python_docs_tutorial_inputoutput#reading-and-writing-files]
A.f2: It is good practice to use the with keyword when working with a file object, because it closes the file automatically after its block finishes, even if an exception is raised.   [sources: python_docs_tutorial_inputoutput#reading-and-writing-files]
A.f3: f.read() reads a file's contents and returns them as a string in text mode; once the end of the file is reached, further calls to f.read() return an empty string.   [sources: python_docs_tutorial_inputoutput#methods-of-file-objects]
A.f4: csv.DictReader(f) creates a reader that maps each row of a CSV file to a dict, using the first row's values as keys by default, e.g. for row in reader: print(row['first_name'], row['last_name']).   [sources: python_docs_csv#module-contents]
A.f5: f.write(string) writes the contents of string to the file, returning the number of characters written.   [sources: python_docs_tutorial_inputoutput#methods-of-file-objects]
A.f6: csv.DictWriter(f, fieldnames=...) creates a writer that maps a dict to a row; writer.writeheader() writes the header row and writer.writerow(dict) writes one data row, in the order given by fieldnames.   [sources: python_docs_csv#module-contents]
A.f7: A CSV file used with the csv module should be opened with newline='', e.g. open('names.csv', 'w', newline='').   [sources: python_docs_csv#module-contents]
note: Keep 'orders.csv' with order_id/city/delivery_minutes-style columns as the one running file example.
PRACTICE ANCHOR (live_code): Read a CSV file's rows into a list of dicts using the csv module.  SUCCESS: The list holds one dict per data row, keyed by the header names.
ASSESSMENT ANCHOR: open_read_and_write_text_file facts=['f1', 'f3', 'f5']
ASSESSMENT ANCHOR: manage_file_with_with_statement facts=['f2']
ASSESSMENT ANCHOR: read_and_write_csv_rows_as_dicts facts=['f4', 'f6', 'f7']

## DATA ASSETS USED
ds_orders: orders — QuickDeliver order records (orders.csv) — columns: order_id(identifier,digits-as-label), city(categorical), delivery_minutes(numerical), is_late(categorical), driver_id(identifier,digits-as-label)
   [1042,"Lagos",32,false,201]
   [1043,"Abuja",45,false,202]
   [1044,"Kano",21,false,201]
   [1045,"Lagos",60,true,203]
   [1046,"Ibadan",18,false,202]
   [1047,"Abuja",12,false,204]
   [1048,"Kano",55,true,203]
   [1049,"Lagos",38,false,201]
   variant orders_messy: 4 ops; planted: issue_missing_delivery_minutes(missing_value); issue_impossible_delivery_minutes(impossible_value); issue_duplicate_order_1042(duplicate_row); issue_city_casing(inconsistent_category)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply transform; Boolean/conditional filtering; Comparing correlation strength across multiple variable pairs; Computing descriptive statistics with pandas (describe, mean, median, std); Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Distribution shape (skewness, symmetry, outliers); Handling missing data (isna, dropna, fillna); Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Inspecting data (head, info, describe, shape, dtypes); Map substitution; Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Removing duplicate rows; Renaming columns and index labels; Selecting rows/columns with loc/iloc; Series and DataFrame data structures; Sorting values; String cleaning with the .str accessor; Type conversion and dtype management (astype); Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Open a file and read its contents  [reward 5]
File I/O — Delivery records often live in files on disk. open() and with give you a safe, automatic way to read them.
(intro) `open(filename, mode)` returns a file object. The mode can be `'r'` to read, `'w'` to write (erasing an existing file of the same name), or `'a'` to append; `'r'` is assumed if mode is omitted. `open('orders.txt')` opens `orders.txt` for reading. ⟦A.f1 A:tb1⟧
(practical_context) It is good practice to use the `with` keyword when working with a file object, because it closes the file automatically after its block finishes — even if an exception is raised. `with open('orders.txt') as f:` opens the file and assigns the file object to `f`; the file is closed when the `with` block exits. ⟦A.f2 A:tb2⟧
(mechanism) `f.read()` reads the file's entire contents and returns them as a string in text mode. Once the end of the file is reached, further calls to `f.read()` return an empty string. `csv.DictReader(f)` creates a reader that maps each row of a CSV file to a dict, using the first row's values as keys by default. ⟦A.f3 A.f4 A:tb3 A:tb4⟧
[BEFORE_AFTER] Switch from f.read() (one string) to csv.DictReader (one dict per row, keyed by column name).
  before:
[CODE python]
# Raw text read — one big string
with open('orders.txt') as f:
    contents = f.read()
print(contents)
  annotations: ['contents is one long string']
  after:
[CODE python]
import csv

# CSV read — each row is a dict
with open('orders.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['order_id'], row['city'])
  annotations: ['Each row is a dict keyed by the header names']

### s02 · explainer · Write text and CSV rows to a file  [reward 5]
File I/O — f.write() sends a string to a file; csv.DictWriter maps dicts to rows.
(mechanism) `f.write(string)` writes the contents of `string` to the file, returning the number of characters written. Opening with mode `'w'` erases any existing file of the same name before writing; mode `'a'` appends to the end. ⟦A.f5 A.f1 A:tb5⟧
(mechanism) `csv.DictWriter(f, fieldnames=['order_id', 'city'])` creates a writer that maps a dict to a row. `writer.writeheader()` writes the header row and `writer.writerow(dict)` writes one data row, in the order given by `fieldnames`. ⟦A.f6 A:tb6⟧
(practical_context) A CSV file used with the `csv` module should be opened with `newline=''` — for example, `open('orders.csv', 'w', newline='')`. This prevents the csv module from seeing extra blank lines on some platforms. ⟦A.f7 A:tb7⟧
(walkthrough) A complete read-then-write workflow: open `orders.csv` with `newline=''` and `csv.DictReader` to iterate rows, then open `lagos_orders.csv` for writing with `csv.DictWriter`, call `writeheader()`, and call `writerow(row)` for each Lagos order. Both `open()` calls use `with` so files close automatically. ⟦A.f1 A.f2 A.f4 A.f5 A.f6 A.f7 A:tb8⟧

### s03 · video · File I/O in Python  [reward 3]
Watch — See open(), with, and the csv module in action.
[VIDEO Opening, reading and writing a file safely] bridge-before: Watch the with block close the file for you. Caveats: the second clip overstates the risk of an unclosed file ('no one else can modify it') and calls end='' a 'null character'; it is an empty string. | bridge-after: Neither clip uses the csv module or newline=''; the text covers DictReader, DictWriter and newline='' alongside open(). The text also states that w erases an existing file.
  - Uh2ebFW8OYM 18-386s facts=['f1', 'f2', 'f3'] label: open()'s r/w/a/r+ modes and its default-to-read behavior, manually closing a file, then the with statement closing it automatically (even on exceptions), then f.read() | summary: Opens a text file with open(), explaining that the second argument picks the mode (r to read, w to write, a to append, r+ for both) and that reading is the default when none is given. Shows closing manually with close() and why forgetting to close can leak resources, then the with statement, which closes the file automatically after its block even when an error is raised, confirmed by the closed attribute being True afterward and a read after the block failing. Ends by calling read() to get the file's whole contents as one string.
  - Jsnw6HLASZA 38-546s facts=['f1', 'f2', 'f3', 'f5'] label: Opening a file with open()+mode, reading it with a context manager, and writing/overwriting with write() | summary: Reads a text file by calling open() in r mode, read() to get the whole contents as a string, and close(), then repeats it with the with statement, which closes the file when the block ends even after an unexpected error. Compares read() with looping over lines, read(100) and readlines(). Then writes: opens in w mode, calls write() with a short text, notes the file is created if missing and its old contents are overwritten if it exists, and shows this by running it again with different text.

### s04 · check · Open, read, and write a text file  [reward 5]
Quick check — Which mode string opens a file for writing, erasing any existing content?
QUESTION [choice, intro, grading=client] Which mode string opens a file for **writing** (creating it if it does not exist, and erasing it if it does)?
  ✘ opt_a: `'r'`
      why: `'r'` opens a file for reading. It raises an error if the file does not exist and does not erase existing content.
  ✘ opt_b: `'a'`
      why: `'a'` opens a file for appending — it adds to the end of an existing file rather than erasing it.
  ✔ opt_c: `'w'`
      why: Correct. `'w'` opens a file for writing. It creates the file if it does not exist and erases any existing content.
  ✘ opt_d: No mode argument — `open()` defaults to write mode.
      why: Omitting the mode defaults to `'r'` (read), not write. To write, you must pass `'w'` explicitly.
  feedback✔: Right — `'w'` mode creates the file if needed and erases existing content before writing.  feedback✘: The three main modes are `'r'` (read), `'w'` (write, erasing existing content), and `'a'` (append). Writing from scratch uses `'w'`.  hints: ['Think about what the first letter of each mode stands for: r=read, w=write, a=append.', "Which mode would erase an existing file's contents before writing new data?"]  remediation→r01
  MEASURES: A:open_read_and_write_text_file(f1,f3,f5)   anchors=['assessment:open_read_and_write_text_file']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f5←s02

### s05 · check · Manage a file with the with statement  [reward 5]
Quick check — What does the with statement guarantee when working with a file object?
QUESTION [choice, intro, grading=client] What is the main advantage of using `with open('orders.txt', 'r') as f:` instead of `f = open('orders.txt', 'r')`?
  ✘ opt_a: It reads the file faster.
      why: The `with` statement does not affect read speed. Its purpose is automatic resource management.
  ✔ opt_b: It closes the file automatically when the block finishes, even if an exception is raised.
      why: Correct. The `with` statement closes the file automatically when the block ends, even if an exception is raised inside the block.
  ✘ opt_c: It prevents other programs from reading the file at the same time.
      why: The `with` statement does not lock the file for exclusive access. Its purpose is to ensure the file is closed when the block exits.
  ✘ opt_d: It loads the entire file into memory before the block starts.
      why: The `with` statement does not preload the file. It simply ensures the file object is closed when the block finishes.
  feedback✔: Right — `with open(...)` guarantees the file is closed when the block exits, even if an exception occurs.  feedback✘: The `with` keyword is about automatic cleanup: it closes the file when the block ends, even if an exception is raised.  hints: ['What happens to a file opened with `f = open(...)` if an exception occurs before `f.close()` is called?', 'The `with` statement handles cleanup automatically — what resource does it clean up here?']  remediation→r02
  MEASURES: A:manage_file_with_with_statement(f2)   anchors=['assessment:manage_file_with_with_statement']
  taught-before-tested: A.f2←s01

### s06 · hands_on · Read and write CSV rows as dicts  [reward 10]
Practice — Use csv.DictReader to read orders.csv and csv.DictWriter to write a filtered output file.
QUESTION [code_exercise, core, grading=client] Read `orders.csv` using `csv.DictReader` and collect all rows into a list called `rows`.

Open the file with `newline=''` as required by the csv module.
Use a `for` loop to append each row dict to `rows`.
After the loop, print `len(rows)`.

Expected output: `15`
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call', 'return', 'def f(a, b=default):', 'keyword arguments f(name=value)', 'global statement', 'try:', 'except ValueError:', 'input()', 'import module', 'module.name', 'from module import name', 'open(file, mode)', 'with open(...) as f:', 'f.read()', 'f.write()', 'csv.DictReader', 'csv.DictWriter', "newline=''"] blocked=7 items
  file solution.py [editable]:
import csv

# Read orders.csv using csv.DictReader.
# Collect all rows into a list called rows.
# Then print the number of rows.

rows = []

  SOLUTION solution.py:
import csv

rows = []
with open('orders.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(len(rows))

  test t1_row_count (value_equals, visible=True): {"expr":"len(rows)","expected":15} | on-fail: `len(rows)` should be `15` — one dict per data row in orders.csv. Make sure you loop through all rows and append each one.
  test t2_stdout (stdout_equals, visible=True): {"expected":"15"} | on-fail: The program should print `15`. Check that you call `print(len(rows))` after the loop.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4687f1098c72fc83e82674ff262fa1fe6b2e04269ede1ec4eb185dc5da96f9e5","tests_passed":2}
  feedback✔: Well done — `csv.DictReader` mapped each row to a dict keyed by the header names, and you collected all 15 rows.  feedback✘: Use `with open('orders.csv', newline='') as f:` then `reader = csv.DictReader(f)` then `for row in reader: rows.append(row)`.  hints: ["Open the file with `newline=''` as the third argument to `open()`. This is required by the csv module.", 'Inside the `with` block, create `reader = csv.DictReader(f)` and loop: `for row in reader: rows.append(row)`.']  remediation→r01
  MEASURES: A:read_and_write_csv_rows_as_dicts(f4,f7)   anchors=['practice', 'assessment:read_and_write_csv_rows_as_dicts']
  taught-before-tested: A.f4←s01; A.f7←s02

### s07 · recap · File I/O: what you've learned  [reward 5]
Recap — Four ideas that connect your script to data on disk.
(takeaway) Reading and writing files is how a program's delivery data gets in from, and results get out to, storage that outlives the program run. `open()` and `with` manage the connection and guarantee the file closes. The `csv` module adds structured row-by-row access: `csv.DictReader` maps each row to a dict keyed by the header names, and `csv.DictWriter` maps dicts back to rows. ⟦A.f1 A.f2 A.f4 A.f6 A:tb9⟧
[UP NEXT] Up next: PEP 8 style: Next you will learn the PEP 8 style recommendations — indentation, line length, whitespace, and naming — that make Python code easier to read.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · open() modes and f.read() / f.write() — The mode string controls whether you read, write, or append.
(mechanism) `open(filename, mode)` returns a file object. Mode `'r'` reads (default), `'w'` writes and erases any existing file of the same name, `'a'` appends. `f.read()` returns the file's contents as a string; once the end is reached, further calls return an empty string. `f.write(string)` writes the string and returns the number of characters written. ⟦A.f1 A.f3 A.f5 A:tb1 A:tb3 A:tb5⟧
### r02 · The with statement closes the file automatically — with guarantees cleanup even when an exception occurs.
(practical_context) It is good practice to use the `with` keyword when working with a file object, because it closes the file automatically after its block finishes — even if an exception is raised. `with open('orders.txt') as f:` opens the file and assigns the file object to `f`; the file is closed when the `with` block exits, without needing an explicit `f.close()` call. ⟦A.f2 A:tb2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: += and other augmented assignment

=========

# EVALUATOR PACKET — Defining Functions, Parameters, and Return Values (tile_python_functions_scope)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.defining_calling_functions — Defining calling functions
B = python.parameters_arguments — Parameters arguments
C = python.return_values — Return values
D = python.function_default_keyword_args — Default and keyword arguments
E = python.variable_scope — Variable scope (local vs global)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (python.defining_calling_functions)   objective: Define a function with def and a name, and call it by that name to run its body.
A.f1: The keyword def introduces a function definition, followed by the function's name and a parenthesized, possibly empty, list of parameter names, e.g. def my_function():; the statements forming the body start on the next line and must be indented.   [sources: python_docs_tutorial_controlflow#defining-functions, python_docs_tutorial_controlflow#documentation-strings]
A.f2: A function definition associates the function name with the function object; calling the function by that name (e.g. fib(2000)) runs its body.   [sources: python_docs_tutorial_controlflow#defining-functions]
PRACTICE ANCHOR (live_code): Create a small reusable helper with def and call it more than once.  SUCCESS: The helper's body runs once per call, and nothing runs when only the def is written.
ASSESSMENT ANCHOR: recognize_function_definition facts=['f1']
ASSESSMENT ANCHOR: call_function_to_run_its_body facts=['f2']

## SOURCE FACTS — B (python.parameters_arguments)   objective: Pass values into a function's parameters as positional arguments in a call, matching each argument to the parameter in that position.
B.f1: The formal parameters of a function are named in its def statement's parenthesized list.   [sources: python_docs_tutorial_controlflow#defining-functions]
B.f2: Inside the function body, each parameter name refers to the argument value that was passed for it when the function was called.   [sources: python_docs_tutorial_controlflow#defining-functions]
B.f3: When a function is called with positional arguments, if there are N positional arguments, they are placed in the function's first N parameter slots, in order.   [sources: python_official_docs#reference/expressions.html#calls]
PRACTICE ANCHOR (live_code): Turn a simple helper into one that takes parameters, then call it with different positional arguments.  SUCCESS: Each call uses its own argument values, and arguments land in the parameter slots in order.
ASSESSMENT ANCHOR: identify_parameters_and_their_values facts=['f1', 'f2']
ASSESSMENT ANCHOR: match_positional_arguments_to_parameters facts=['f3']

## SOURCE FACTS — C (python.return_values)   objective: Use return to send a computed value back from a function so the caller can store and reuse it, instead of only printing it.
C.f1: A return statement sends a value back to the code that called the function, e.g. return result gives the caller access to that value.   [sources: python_docs_tutorial_controlflow#defining-functions]
C.f2: Even a function without a return statement does return a value: the built-in value None.   [sources: python_docs_tutorial_controlflow#defining-functions]
C.f3: The returned value can be stored in a variable for later use, e.g. f100 = fib2(100) stores the list fib2 returns in f100.   [sources: python_docs_tutorial_controlflow#defining-functions]
PRACTICE ANCHOR (live_code): Write a function that returns a calculated value, and store the result in a variable.  SUCCESS: The function returns rather than prints the value, and the variable holds that value when printed afterward.
ASSESSMENT ANCHOR: distinguish_return_from_print facts=['f1', 'f2']
ASSESSMENT ANCHOR: return_and_store_a_value facts=['f1', 'f3']

## SOURCE FACTS — D (python.function_default_keyword_args)   objective: Give a function parameter a default value so the argument can be omitted, and call the function using keyword arguments to supply values by name.
D.f1: Specifying a default value for a parameter, e.g. def ask_ok(prompt, retries=4):, creates a function that can be called with fewer arguments than it is defined to accept.   [sources: python_docs_tutorial_controlflow#default-argument-values]
D.f2: A function can also be called using keyword arguments of the form kwarg=value, e.g. parrot(voltage=1000); in a call, keyword arguments must follow any positional arguments.   [sources: python_docs_tutorial_controlflow#keyword-arguments]
D.f3: All the keyword arguments passed in a call must match one of the function's parameters, and no parameter may receive a value more than once.   [sources: python_docs_tutorial_controlflow#keyword-arguments]
D.m1 (misconception): A default value is evaluated only once, at the point the function is defined, not on each call; if the default is a mutable object such as a list, that same object is shared and can accumulate changes across calls unless the function is written to create a fresh value each time.   [sources: python_docs_tutorial_controlflow#default-argument-values]
note: The mutable-default misconception is easy to skip -- state it explicitly, don't just imply it.
PRACTICE ANCHOR (live_code): Write a function with a default parameter, then call it once using only keyword arguments and once omitting the default.  SUCCESS: Both calls run; the omitted default takes its default value and the keyword call sets values by name.
ASSESSMENT ANCHOR: call_with_default_omitted facts=['f1']
ASSESSMENT ANCHOR: call_with_keyword_arguments facts=['f2', 'f3']
ASSESSMENT ANCHOR: recognize_mutable_default_trap facts=['m1']

## SOURCE FACTS — E (python.variable_scope)   objective: Predict whether a name inside a function refers to a local variable or a same-named global variable, based on where it is assigned.
E.f1: All variable assignments in a function store the value in that function's local symbol table.   [sources: python_docs_tutorial_controlflow#defining-functions]
E.f2: For a function that is not nested inside another function, variable references inside it first look in the local symbol table, then the global symbol table, and finally the table of built-in names.   [sources: python_docs_tutorial_controlflow#defining-functions]
E.f3: A global variable cannot be directly assigned a value from inside a function unless it is named in a global statement; it may still be referenced (read) without such a statement.   [sources: python_docs_tutorial_controlflow#defining-functions]
PRACTICE ANCHOR (live_code): Write a function that reads a global variable and, separately, assigns a local variable with the same name without changing the global.  SUCCESS: Inside the function the global is readable; the same-named local does not change the global's value outside.
ASSESSMENT ANCHOR: predict_name_resolution facts=['f1', 'f2']
ASSESSMENT ANCHOR: recognize_when_global_statement_needed facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Basic error handling (try/except); Basic file I/O (reading/writing text and CSV files); Boolean/conditional filtering; Comparing correlation strength across multiple variable pairs; Computing descriptive statistics with pandas (describe, mean, median, std); Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Default and keyword arguments; Distribution shape (skewness, symmetry, outliers); Identifying and reasoning about outliers; Idiomatic style conventions for readable Python; Inspecting data (head, info, describe, shape, dtypes); Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Modules and imports; Parameters arguments; Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Removing duplicate rows; Renaming columns and index labels; Return values; Selecting rows/columns with loc/iloc; Series and DataFrame data structures; Sorting values; String cleaning with the .str accessor; Type conversion and dtype management (astype); Variable scope (local vs global); Working with datetime data (to_da

## LESSON, in learner order

### s01 · explainer · Define once, run whenever you need it  [reward 5]
Functions — A function packages a block of code under a name so you can run it as many times as you like without copying it.
(definition) The keyword `def` introduces a function definition: `def summarize_delivery():` gives the function its name and an empty parameter list. The statements that form the body start on the next line and must be indented. Writing the `def` block only stores the function under that name — nothing in the body runs yet. ⟦A.f1 A:tb1⟧
(mechanism) Calling the function by its name followed by parentheses — `summarize_delivery()` — is what actually runs the body. You can call the same function multiple times; each call runs the body from the top. ⟦A.f2 A:tb2⟧
[PROCESS_FLOW: def stores; calling runs] nodes=["def summarize_delivery():\n    print('--- summary ---') — Definition — body does NOT run here", 'summarize_delivery() — First call — body runs', 'summarize_delivery() — Second call — body runs again'] edges=[('n_def', 'n_call1', 'call 1'), ('n_def', 'n_call2', 'call 2')] alt: A box labelled with the def statement sits on the left. Two arrows labelled 'call 1' and 'call 2' point from it to two separate call boxes on the right, showing the body runs once per call.

### s02 · check · Spot the function definition  [reward 5]
Quick check — Which line introduces a function definition?
QUESTION [choice, intro, grading=client] Which of the following is a valid Python function definition?

```python
# A
function greet():
    print('Hello')

# B
def greet():
    print('Hello')

# C
greet def():
    print('Hello')

# D
def greet
    print('Hello')
```
  ✘ opt_a: A — uses the keyword `function`
      why: Python uses `def`, not `function`. The syntax is `def name():` followed by an indented body.
  ✔ opt_b: B — uses `def`, the function name, parentheses, and a colon
      why: Correct. `def greet():` uses the `def` keyword, the function name, empty parentheses, and a colon before the indented body.
  ✘ opt_c: C — puts the name before `def`
      why: The `def` keyword must come first, before the function name. The correct order is `def greet():`
  ✘ opt_d: D — omits the parentheses and colon
      why: A function definition requires parentheses (even if empty) and a colon after the name: `def greet():`
  feedback✔: Right — `def greet():` is the correct syntax. `def` comes first, then the name, then `()`, then `:`.  feedback✘: A function definition starts with `def`, followed by the name, parentheses (possibly empty), and a colon. The body is indented on the next line.  hints: ["The keyword that introduces a function definition is three letters long and starts with 'd'.", 'After the name, you need `()` even if there are no parameters, and a `:` before the indented body.']  remediation→r01
  MEASURES: A:recognize_function_definition(f1)   anchors=['assessment:recognize_function_definition']
  taught-before-tested: A.f1←s01

### s03 · hands_on · Call a function to run its body  [reward 10]
Practice — Write a call that runs the helper function defined for you.
QUESTION [code_exercise, core, grading=client] A starter variable `message` is already set to `'QuickDeliver driver ready'`.

Define a function called `greet_driver` that prints the value stored in `message`.

Then **call it twice**. The output should show the message two times.

Use only `def name():` and `calling name()`. Do not add parameters or a `return` statement.
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()'] blocked=26 items
  file solution.py [editable]:
# A starter variable is already set below.
# Define a function called greet_driver that prints message.
# Then call it twice.

message = 'QuickDeliver driver ready'

  SOLUTION solution.py:
message = 'QuickDeliver driver ready'

def greet_driver():
    print(message)

greet_driver()
greet_driver()

  test t1_two_calls (stdout_equals, visible=True): {"expected":"QuickDeliver driver ready\nQuickDeliver driver ready"} | on-fail: Your output should show 'QuickDeliver driver ready' printed twice, once per call.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"917e4053b69a284a9d1390eff7715e0d76854b208853d670e14461608f8b835c","tests_passed":1}
  feedback✔: Well done — calling `greet_driver()` twice ran the body twice. The `def` line only defines the function; the body runs only when you call it.  feedback✘: Make sure you have a `def greet_driver():` block with the print inside, then two separate calls `greet_driver()` after the definition.  hints: ['The `def` block only stores the function — it does not run it. You need a separate call line after the definition.', 'To call a function, write its name followed by `()`. Do this on two separate lines after the `def` block.']
  MEASURES: A:call_function_to_run_its_body(f2)   anchors=['practice', 'assessment:call_function_to_run_its_body']
  taught-before-tested: A.f2←s01

### s04 · explainer · Give your function the inputs it needs  [reward 5]
Parameters — Parameters let a function work with different values on each call instead of always doing the same thing.
(intro) The formal parameters of a function are named in its `def` statement's parenthesised list. `def classify_delivery(minutes):` declares one parameter, `minutes`. Inside the body, `minutes` refers to whatever value was passed when the function was called. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
(mechanism) When you call a function with positional arguments, the first argument fills the first parameter slot, the second fills the second, and so on. For `def delivery_summary(city, minutes):`, calling `delivery_summary('Lagos', 32)` sets `city` to `'Lagos'` and `minutes` to `32`. ⟦B.f3 B:tb3⟧
[DIAGRAM: Arguments fill parameter slots in order] nodes=["'Lagos'", '32', 'city', 'minutes'] edges=[('arg_city', 'par_city', '1st → 1st'), ('arg_min', 'par_min', '2nd → 2nd')] alt: Two argument values ('Lagos' and 32) on the left with arrows pointing to the matching parameter names (city and minutes) on the right, labelled 1st→1st and 2nd→2nd.

### s05 · check · Match arguments to parameters  [reward 5]
Quick check — Given a function call, which value does each parameter receive?
QUESTION [choice, intro, grading=client] Given this function:

```python
def log_delivery(order_id, city, minutes):
    print(order_id, city, minutes)
```

What does `log_delivery(1042, 'Lagos', 32)` print?
  ✔ opt_a: `1042 Lagos 32`
      why: Correct. Positional arguments fill parameter slots in order: `order_id=1042`, `city='Lagos'`, `minutes=32`.
  ✘ opt_b: `Lagos 1042 32`
      why: Arguments fill slots in the order they appear in the call, not alphabetically. The first argument `1042` goes to the first parameter `order_id`.
  ✘ opt_c: `32 Lagos 1042`
      why: Arguments are matched by position, not by value size. `1042` → `order_id`, `'Lagos'` → `city`, `32` → `minutes`.
  ✘ opt_d: `order_id city minutes`
      why: The function prints the argument values, not the parameter names. Parameter names are local labels inside the function.
  feedback✔: Right — positional arguments fill parameter slots left-to-right in the order they appear in the call.  feedback✘: Positional arguments are matched to parameters by position: the first argument goes to the first parameter, the second to the second, and so on.  hints: ['Look at the order of parameters in `def log_delivery(order_id, city, minutes)` and the order of arguments in the call.', 'The first argument in the call fills the first parameter slot, the second fills the second, and so on.']  remediation→r02
  MEASURES: B:match_positional_arguments_to_parameters(f3)   anchors=['assessment:match_positional_arguments_to_parameters']
  taught-before-tested: B.f3←s04

### s06 · hands_on · Add parameters and call with arguments  [reward 10]
Practice — Extend a function to accept a city and a delivery time, then call it with QuickDeliver order values.
QUESTION [code_exercise, core, grading=client] Starter variables `city1 = 'Lagos'`, `minutes1 = 32`, `city2 = 'Abuja'`, `minutes2 = 45` are already set.

Define a function `report_delivery(city, minutes)` that prints `city` and `minutes` separated by a space.

Then call it twice:
1. `report_delivery(city1, minutes1)`
2. `report_delivery(city2, minutes2)`

Expected output:
```
Lagos 32
Abuja 45
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call'] blocked=24 items
  file solution.py [editable]:
# Starter variables are set below.
# Define report_delivery(city, minutes) that prints city and minutes.
# Then call it twice with the starter variables.

city1 = 'Lagos'
minutes1 = 32
city2 = 'Abuja'
minutes2 = 45

  SOLUTION solution.py:
city1 = 'Lagos'
minutes1 = 32
city2 = 'Abuja'
minutes2 = 45

def report_delivery(city, minutes):
    print(city, minutes)

report_delivery(city1, minutes1)
report_delivery(city2, minutes2)

  test t1_output (stdout_equals, visible=True): {"expected":"Lagos 32\nAbuja 45"} | on-fail: Expected two lines: 'Lagos 32' then 'Abuja 45'. Check that your parameters are named `city` and `minutes` and that you call the function twice with the right arguments.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a02184d4a2783288a11f28b6d393f1b06c400f3bf8719768e95be90c21ef33df","tests_passed":1}
  feedback✔: Well done — each call passed its own arguments to the parameters in order, so `city` and `minutes` held different values in each call.  feedback✘: Add `city` and `minutes` to the `def` line's parentheses, then call `report_delivery('Lagos', 32)` and `report_delivery('Abuja', 45)`.  hints: ['Change `def report_delivery():` to `def report_delivery(city, minutes):` to add the two parameters.', 'After the definition, write two call lines. The first argument goes to `city`, the second to `minutes`.']  remediation→r02
  MEASURES: B:identify_parameters_and_their_values(f1,f2); B:match_positional_arguments_to_parameters(f3)   anchors=['practice', 'assessment:identify_parameters_and_their_values', 'assessment:match_positional_arguments_to_parameters']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s07 · explainer · Hand a result back to the caller  [reward 5]
Return values — A function that only prints its result can't be reused — the caller needs a `return` statement to get the value back.
(intro) A `return` statement sends a value back to the code that called the function. `return category` gives the caller access to the string `category` computed inside the function. Without `return`, the caller receives `None` — the built-in empty value Python uses when nothing is explicitly returned. ⟦C.f1 C.f2 C:tb1 C:tb2⟧
(mechanism) The returned value can be stored in a variable for later use. After `result = classify_delivery(32)`, the variable `result` holds whatever `classify_delivery` returned, so later code can reuse `result` without calling the function again. ⟦C.f3 C:tb3⟧
[BEFORE_AFTER] Replace print() with return so the caller receives the value instead of None.
  before:
[CODE python]
def classify_delivery(minutes):
    if minutes > 45:
        print('slow')
    else:
        print('fast')

classify_delivery(32)   # prints 'fast'
result = classify_delivery(32)  # result is None
  annotations: ['result is None — print() returns nothing']
  after:
[CODE python]
def classify_delivery(minutes):
    if minutes > 45:
        return 'slow'
    else:
        return 'fast'

result = classify_delivery(32)  # result is 'fast'
print(result)                   # 'fast'
  annotations: ["result holds 'fast' — the caller can reuse it"]

### s08 · video · Return values in action  [reward 3]
Watch — See how return hands a result back to the caller.
[VIDEO From printing a result to getting it back] bridge-before: Watch the difference between a function that only prints and one that returns: only the returned value can be stored and reused. The second clip labels names as 'local' and 'global'; read these as names made inside and outside the function. | bridge-after: The first clip never mentions None; the second does. The first clip builds its printed text with str() and string joining; the second returns a cleaned name string. Devspace's example returns a category string.
  - AetGXMcNU3M 0-300s facts=['f1', 'f3'] label: Getting a value back from a function to reuse, instead of just printing it | summary: Starts with an area function that prints length times width, so the result appears on screen but the program cannot use it, for example to add an apartment and a yard together; the clip calls the printing a side effect. Changes the function to return the product, stores each call's result in its own variable (house and yard), adds them and prints a total of 3,500 square feet. The point is that return gives a value back that the program can store and reuse.
  - DZ2yBGzvlXk 0-397s facts=['f1', 'f2', 'f3'] label: Return sends a value back to the caller; a function without return sends back None; the returned value can be stored | summary: Contrasts printing with returning: programs need a function to hand a value back rather than only show it. Shows the syntax, with return followed by a value at the end of the body and a call whose result is assigned to a variable, and traces a call that multiplies its argument by two and stores 6. States that a function with no return still gives back None, then demonstrates with a name-cleaning function: returning the cleaned name stores 'Maria' in a variable, and removing the return makes that variable None.

### s09 · check · Return and store a value  [reward 5]
Quick check — Which snippet correctly returns a value and stores it in a variable?
QUESTION [choice, core, grading=client] ```python
def compute_late_fee(minutes):
    return minutes * 2

fee = compute_late_fee(30)
print(fee)
```

What does this script print?
  ✔ opt_a: `60`
      why: Correct. `return minutes * 2` sends `30 * 2 = 60` back to the caller. `fee = compute_late_fee(30)` stores `60`, and `print(fee)` prints `60`.
  ✘ opt_b: `None`
      why: `None` is returned only when a function has no `return` statement. This function has `return minutes * 2`, so it returns the computed value.
  ✘ opt_c: `minutes * 2`
      why: Python evaluates the expression `minutes * 2` and returns the result (`60`), not the expression text.
  ✘ opt_d: `30`
      why: `30` is the argument passed in. The function multiplies it by `2` and returns `60`, which is what gets stored in `fee`.
  feedback✔: Right — `return minutes * 2` sends `60` back to the caller, which stores it in `fee` and prints it.  feedback✘: `return` sends the computed value back to the caller. `fee = compute_late_fee(30)` stores that returned value, so `print(fee)` prints it.  hints: ['Trace the call: `minutes` is `30` inside the function. What does `30 * 2` equal?', 'The `return` statement sends that result back. `fee = compute_late_fee(30)` stores whatever `return` sends.']  remediation→r03
  MEASURES: C:return_and_store_a_value(f1,f3)   anchors=['assessment:return_and_store_a_value']
  taught-before-tested: C.f1←s07; C.f3←s07

### s10 · hands_on · Write a function that returns a result  [reward 10]
Practice — Convert a print-only function into one that returns its result so the caller can store and reuse it.
QUESTION [code_exercise, core, grading=client] The delivery team charges a wait fee of 2 NGN per minute late.

1. Define a function `compute_wait_fee(minutes)` that **returns** `minutes * 2`.
   Do **not** use `print()` inside the function.
2. Call it with the value stored in `minutes` (already set to `45`) and store the returned value in a variable called `result`.
3. Print `result`.

Expected output: `90`
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call', 'return'] blocked=23 items
  file solution.py [editable]:
# The delivery team charges a wait fee of 2 NGN per minute late.
# Define a function called compute_wait_fee that takes one parameter: minutes
# It should RETURN minutes * 2 (do not print inside the function).
#
# Then call it with the value stored in `minutes` and store the result in `result`.
# Finally, print result.

minutes = 45

  SOLUTION solution.py:
minutes = 45

def compute_wait_fee(minutes):
    return minutes * 2

result = compute_wait_fee(minutes)
print(result)

  test t1_result_value (value_equals, visible=True): {"expr":"result","expected":90} | on-fail: `result` should hold `90` (45 * 2). Make sure your function returns the value rather than printing it.
  test t2_stdout (stdout_equals, visible=True): {"expected":"90"} | on-fail: The program should print `90`. Check that you call `print(result)` after storing the returned value.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"08977b71728b3bc873a9cca475316168b7ff6f2d37f96028882a53dadebef6ca","tests_passed":2}
  feedback✔: Well done — `compute_wait_fee` returns the value, and `result = compute_wait_fee(minutes)` stores it so you can print it afterward.  feedback✘: Use `return minutes * 2` inside the function (not `print`). Then write `result = compute_wait_fee(minutes)` and `print(result)` outside.  hints: ['Inside the function, use `return minutes * 2` — not `print(minutes * 2)`. The caller receives the returned value.', 'After the function definition, write `result = compute_wait_fee(minutes)` to capture the returned value, then `print(result)`.']  remediation→r03
  MEASURES: C:distinguish_return_from_print(f1,f2); C:return_and_store_a_value(f1,f3)   anchors=['practice', 'assessment:distinguish_return_from_print', 'assessment:return_and_store_a_value']
  taught-before-tested: C.f1←s07; C.f2←s07; C.f1←s07; C.f3←s07

### s11 · explainer · Optional parameters and named arguments  [reward 5]
Default and keyword arguments — Default values let callers omit arguments; keyword arguments let callers name them explicitly.
(definition) Specifying a default value for a parameter — `def ask_ok(prompt, retries=4):` — creates a function that can be called with fewer arguments than it is defined to accept. Calling `ask_ok('Delete this order?')` works and uses `4` for `retries`. ⟦D.f1 D:tb1⟧
(syntax) A function can also be called using keyword arguments of the form `kwarg=value` — `ask_ok(prompt='Delete this order?', retries=2)`. In a call, keyword arguments must follow any positional arguments. All keyword arguments must match one of the function's parameters, and no parameter may receive a value more than once. ⟦D.f2 D.f3 D:tb2 D:tb3⟧
(misconception) A default value is evaluated only once, at the point the function is defined — not on each call. If that default is a mutable object such as a list, the same object is shared across calls and can accumulate changes unless the function creates a fresh value each time. ⟦D.m1 D:tb4⟧
[DIAGRAM: Three ways to call ask_ok(prompt, retries=4)] nodes=['def ask_ok(prompt, retries=4):', "ask_ok('Delete?', 2)", "ask_ok(prompt='Delete?', retries=2)", "ask_ok('Delete?')", "prompt='Delete?', retries=2", "prompt='Delete?', retries=2", "prompt='Delete?', retries=4 (default)"] edges=[('call_pos', 'res_pos', None), ('call_kw', 'res_kw', None), ('call_def', 'res_def', None)] alt: Function signature at top with default retries=4. Three call styles below — positional, keyword, and default-omitted — each mapped to the parameter values they produce.

### s12 · video · Default values and keyword arguments  [reward 3]
Watch — See default parameters and keyword calls in action.
[VIDEO Default values and named arguments] bridge-before: Watch omitted arguments fall back to defaults, then keyword arguments given in any order but only after positional ones. Both clips use their own functions; Devspace's examples use ask_ok. | bridge-after: Neither clip covers a call with an unknown keyword, giving one parameter two values, or the shared-list trap with mutable defaults; the text covers all three.
  - m2uURZxex3c 0-195s facts=['f1'] label: Live demo: adding default values to function parameters with a net-price calculator example | summary: Explains a default argument as a value a parameter uses when that argument is left out of the call. Defines a net-price function with a list price, a discount and a tax, and shows it cannot be called with only the price. Giving discount a default of 0 and tax a default of 0.05 lets the call pass just 500 and get 525. Passing 0.1 as a second argument overrides the discount default and gives 472.50, and passing 0 for tax gives 450.
  - 7QCHpAtlSMo 0-201s facts=['f2'] label: Calling a function with named arguments instead of position | summary: Explains a keyword argument as an argument written with its parameter's name and an equals sign, which helps readability and means the order of keyword arguments does not matter. Starts from a greeting function called with four positional arguments, shows that swapping positional arguments swaps their meaning, then rewrites the call with title, first and last names as keywords in any order. Mixing the two works only if the positional arguments come first; putting one after a keyword argument is a syntax error. Ends with a first-name and last-name example where keywords remove the ambiguity.

### s13 · check · Spot the mutable default trap  [reward 5]
Quick check — What happens when a function uses a mutable object as a default value?
QUESTION [choice, stretch, grading=client] ```python
def add_order(order_id, log=[]):
    log.append(order_id)
    return log

print(add_order(1042))
print(add_order(1043))
```

What does the second `print` output?
  ✘ opt_a: `[1043]` — each call gets a fresh empty list.
      why: This is the trap: the default `[]` is evaluated once when the function is defined, not on each call. The same list object is shared across all calls that omit `log`.
  ✔ opt_b: `[1042, 1043]` — the same list object is reused across calls.
      why: Correct. The default list is created once at definition time. Both calls share the same object, so after two calls it holds `[1042, 1043]`.
  ✘ opt_c: `[]` — the default is reset after each call.
      why: Python does not reset mutable defaults between calls. The default object is created once and accumulates changes.
  ✘ opt_d: A `TypeError` — you cannot use a list as a default value.
      why: Python allows any object as a default value, including lists. The issue is not a TypeError but unexpected shared state.
  feedback✔: Right — mutable defaults like `[]` are evaluated once at definition time and shared across all calls that omit the argument.  feedback✘: Default values are evaluated once when the `def` statement runs, not on each call. A mutable default like `[]` accumulates changes across calls.  hints: ['When is the default value `[]` created — once when `def` runs, or fresh on every call?', 'If the same list object is used every time, what happens when `append` modifies it on the first call?']  remediation→r04
  MEASURES: D:recognize_mutable_default_trap(m1)   anchors=['assessment:recognize_mutable_default_trap']
  taught-before-tested: D.m1←s11

### s14 · hands_on · Call with defaults and keyword arguments  [reward 10]
Practice — Call a delivery-classification function three ways: omitting a default, using positional arguments, and using keyword arguments.
QUESTION [code_exercise, core, grading=client] Starter variables `order_id1 = 1042`, `order_id2 = 1043`, and `city2 = 'Abuja'` are already set.

Add a default value of `'Lagos'` to the `city` parameter of `describe_order`.

Then make two calls:
1. `describe_order(order_id1)` — omit `city` so it uses the default `'Lagos'`
2. `describe_order(order_id=order_id2, city=city2)` — use keyword arguments by name

Expected output:
```
1042 Lagos
1043 Abuja
```
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call', 'return', 'def f(a, b=default):', 'keyword arguments f(name=value)'] blocked=21 items
  file solution.py [editable]:
# Starter variables are set below.
# Add a default value of 'Lagos' to the city parameter.
# Then:
#   Call describe_order with only order_id1 (city uses its default)
#   Call describe_order(order_id=order_id2, city=city2)

order_id1 = 1042
order_id2 = 1043
city2 = 'Abuja'

def describe_order(order_id, city):
    print(order_id, city)

  SOLUTION solution.py:
order_id1 = 1042
order_id2 = 1043
city2 = 'Abuja'

def describe_order(order_id, city='Lagos'):
    print(order_id, city)

describe_order(order_id1)
describe_order(order_id=order_id2, city=city2)

  test t1_output (stdout_equals, visible=True): {"expected":"1042 Lagos\n1043 Abuja"} | on-fail: Expected '1042 Lagos' then '1043 Abuja'. Check that city has a default of 'Lagos' and that you use keyword arguments by name in the second call.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ff42df155d5a4550a2891bf648375cab73ab56fc9000bc3955d226210d8076bf","tests_passed":1}
  feedback✔: Well done — the first call used the default `'Lagos'` for `city`, and the second call passed keyword arguments by name.  feedback✘: Change `def describe_order(order_id, city):` to `def describe_order(order_id, city='Lagos'):`. Then call it once with just `order_id1` and once with `describe_order(order_id=order_id2, city=city2)`.  hints: ["To add a default, change the parameter to `city='Lagos'` in the `def` line.", 'Use `describe_order(order_id=order_id2, city=city2)` to pass keyword arguments by name.']
  MEASURES: D:call_with_default_omitted(f1); D:call_with_keyword_arguments(f2,f3)   anchors=['practice', 'assessment:call_with_default_omitted', 'assessment:call_with_keyword_arguments']
  taught-before-tested: D.f1←s11; D.f2←s11; D.f3←s11

### s15 · explainer · Where Python looks for a name  [reward 5]
Variable scope — A name created inside a function lives in that function's local table — it doesn't automatically reach the outside world.
(intro) All variable assignments in a function store the value in that function's local symbol table. A name like `total` assigned inside a function is a different variable from any `total` that exists outside it. ⟦E.f1 E:tb1⟧
(mechanism) For a function that is not nested inside another, variable references inside it first look in the local symbol table, then the global symbol table, and finally the table of built-in names. So a name assigned only outside the function is still readable inside it — Python finds it in the global table once the local lookup fails. ⟦E.f2 E:tb2⟧
(misconception) A global variable cannot be directly assigned a value from inside a function unless it is named in a `global` statement. Without `global total`, writing `total = 0` inside a function creates a new local `total` and leaves the global `total` unchanged. The global may still be read without the statement. ⟦E.f3 E:tb3⟧
[DIAGRAM: Local and global symbol tables] nodes=['Global symbol table', 'total = 100', 'Local symbol table (inside function)', 'total = 0  (new local)'] edges=[('local_table', 'global_table', 'lookup order: local → global → built-ins')] alt: Two nested boxes: an outer 'Global symbol table' containing total=100, and an inner 'Local symbol table' containing a separate total=0. An arrow from the inner box to the outer box is labelled 'lookup order: local → global → built-ins'.

### s16 · video · Local, global, and the global statement  [reward 3]
Watch — See the lookup order in action and when you need the global statement.
[VIDEO Where a name is found: local, global, and the global statement] bridge-before: Watch the same x and y code three ways: reading finds the global, assigning makes a new local, and a global statement makes the assignment change the global. The clip's list includes an 'enclosing' level for nested functions, which Devspace's rule here leaves out. | bridge-after: Built-in names are listed but not demonstrated in this range. The rule to keep: assigning inside a function makes a local name by default, while reading can reach a global.
  - QVdf0LgmICw 34-375s facts=['f1', 'f2', 'f3'] label: The LEGB resolution order, then live demos of a local variable shadowing a global one, and the global statement letting a function reassign it | summary: Starts with the lookup order Python uses: local names first, then names from an enclosing function, then global names, then built-in names. Demonstrates with a global x and a function: a name made inside the function (y) cannot be read outside it and fails with a name error, and print(x) inside the function finds the global x when no local x exists. Assigning x inside the function creates a separate local x and leaves the global untouched, while writing global x first makes the same assignment change the global value.

### s17 · explainer · Local shadows global without changing it  [reward 3]
Scope — A same-named local inside a function hides the global — but the global keeps its value outside.
(example) A same-named local can shadow a global inside a function without disturbing the global's value outside it. Reading the name inside the function sees the local one; code outside the function still sees the unchanged global. ⟦E.f1 E.f3 E:tb4⟧

### s18 · check · Predict name resolution  [reward 5]
Quick check — What value does the name refer to inside the function?
QUESTION [choice, core, grading=client] ```python
threshold = 45

def is_late(minutes):
    threshold = 60
    return minutes > threshold

print(is_late(50))
print(threshold)
```

What does this script print?
  ✘ opt_a: `True` then `60`
      why: Inside `is_late`, `threshold = 60` creates a local variable. `50 > 60` is `False`, not `True`. And the global `threshold` stays `45`, not `60`.
  ✘ opt_b: `True` then `45`
      why: Inside `is_late`, `threshold = 60` is a local variable, so `50 > 60` is `False`, not `True`. The global `threshold` is indeed `45`.
  ✔ opt_c: `False` then `45`
      why: Correct. The assignment `threshold = 60` inside the function creates a local variable. `50 > 60` is `False`. The global `threshold` is unchanged at `45`.
  ✘ opt_d: `False` then `60`
      why: The assignment inside the function creates a local variable, not a global one. The global `threshold` stays `45`, not `60`.
  feedback✔: Right — `threshold = 60` inside the function creates a local variable. It does not touch the global `threshold = 45`.  feedback✘: An assignment inside a function stores the value in the function's local symbol table. The global `threshold` is unchanged.  hints: ["Where does `threshold = 60` store its value — in the function's local table or in the global table?", 'After the function returns, what value does the global `threshold` still hold?']  remediation→r05
  MEASURES: E:predict_name_resolution(f1,f2)   anchors=['assessment:predict_name_resolution']
  taught-before-tested: E.f1←s15; E.f2←s15

### s19 · check · When do you need global?  [reward 5]
Quick check — Which situation requires a global statement?
QUESTION [choice, core, grading=client] A script has a global variable `order_count = 0`. A function needs to **increment** `order_count` (i.e. assign a new value to it). Which statement must appear inside the function to make this work?
  ✘ opt_a: `import order_count`
      why: `import` is for modules, not for accessing global variables. Use `global order_count` to allow assignment to the global name.
  ✔ opt_b: `global order_count`
      why: Correct. `global order_count` tells Python that `order_count` inside this function refers to the global variable, so an assignment changes the global.
  ✘ opt_c: `return order_count`
      why: `return` sends a value back to the caller but does not allow the function to assign to the global variable.
  ✘ opt_d: No special statement is needed — assignment inside a function always changes the global.
      why: Without `global order_count`, an assignment inside the function creates a new local variable instead of changing the global one.
  feedback✔: Right — `global order_count` is required before any assignment to a global variable inside a function.  feedback✘: Without a `global` statement, an assignment inside a function creates a local variable. To assign to the global, you must declare `global order_count` first.  hints: ['A global variable can be *read* inside a function without any special statement. But what about *assigning* to it?', "There is a one-word Python keyword that tells a function 'this name refers to the global, not a new local'."]  remediation→r06
  MEASURES: E:recognize_when_global_statement_needed(f3)   anchors=['assessment:recognize_when_global_statement_needed']
  taught-before-tested: E.f3←s15

### s20 · hands_on · Local vs global names  [reward 10]
Practice — Write a function that reads a global variable and assigns a same-named local without changing the global.
QUESTION [code_exercise, stretch, grading=client] A global variable `threshold = 45` is already set.

Write a function `check_delivery(minutes)` that:
1. Assigns a **local** variable also called `threshold` with value `60`
2. Prints `minutes > threshold` (using the local `threshold`)

After the definition, call `check_delivery(50)`, then print the global `threshold`.

Expected output:
```
False
45
```

The local `threshold` inside the function must not change the global `threshold`.
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call', 'return', 'def f(a, b=default):', 'keyword arguments f(name=value)', 'global statement'] blocked=20 items
  file solution.py [editable]:
# A global variable is set below.
# Write a function called check_delivery(minutes) that:
#   1. Assigns a LOCAL variable also called threshold with value 60
#   2. Prints whether minutes > threshold (using the local threshold)
# After defining and calling check_delivery(50),
# print the global threshold to show it is unchanged.

threshold = 45

  SOLUTION solution.py:
threshold = 45

def check_delivery(minutes):
    threshold = 60
    print(minutes > threshold)

check_delivery(50)
print(threshold)

  test t1_stdout (stdout_equals, visible=True): {"expected":"False\n45"} | on-fail: Expected 'False' then '45'. The local threshold=60 makes 50>60 False; the global threshold stays 45.
  test t2_global_threshold (value_equals, visible=True): {"expr":"threshold","expected":45} | on-fail: The global `threshold` should still be `45` after calling `check_delivery`. Do not use `global threshold` inside the function.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"3862a80a714703f6f48f3e2ade81d71af15f021f06424b82b202565ebe0b43dd","tests_passed":2}
  feedback✔: Well done — the local `threshold = 60` inside the function did not change the global `threshold = 45`. Each assignment in a function goes to the local symbol table.  feedback✘: Inside `check_delivery`, write `threshold = 60` (this creates a local variable). Then `print(minutes > threshold)`. After the call, `print(threshold)` should show the global value `45`.  hints: ['An assignment inside a function always creates a local variable unless you use `global`. So `threshold = 60` inside the function is local.', 'After the function call, `threshold` in the global scope is still `45` — the local assignment did not touch it.']  remediation→r05
  MEASURES: E:predict_name_resolution(f1,f2)   anchors=['practice']
  taught-before-tested: E.f1←s15; E.f2←s15

### s21 · recap · Functions: what you've learned  [reward 5]
Recap — Five ideas that make functions reusable and predictable.
(takeaway) `def` creates a reusable block of code under a name; calling that name followed by parentheses is what actually runs it. Parameters name the inputs a function expects; arguments in a specific call supply the actual values. `return` turns a function from something that does an action into something that hands back a result the caller can store and reuse. A function with no `return` statement (or a bare `return`) hands back `None` to its caller. Assigning to a name inside a function makes it local by default; only reading reaches out to a global unless a `global` statement says otherwise. ⟦A.f2 B.f1 B.f2 C.f1 C.f2 E.f1 E.f2 E.f3 A:tb4 B:tb4 C:tb5 E:tb5⟧
[UP NEXT] Up next: Handling errors and importing modules: Next you will learn how try/except lets your code respond to failures instead of crashing, and how import gives you access to code written in other files.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · What makes a function definition? — A function definition always starts with the keyword def.
(definition) The keyword `def` introduces a function definition, followed by the function's name and a parenthesised list of parameters. `def summarize_delivery():` is a definition — it stores the function but does not run it. A bare call like `summarize_delivery()` without a preceding `def` would raise a `NameError`. ⟦A.f1 A:tb1⟧
### r02 · Positional arguments fill slots in order — The first argument always goes to the first parameter, the second to the second.
(mechanism) When you call `delivery_summary('Lagos', 32)`, Python places `'Lagos'` in the first parameter slot (`city`) and `32` in the second (`minutes`) — strictly by position. Swapping the arguments to `delivery_summary(32, 'Lagos')` would swap their meanings, giving `city` the value `32`. ⟦B.f3 B:tb3⟧
### r03 · return sends a value back; print does not — Only return gives the caller a value to store.
(misconception) A `return` statement sends a value back to the code that called the function — `result = classify_delivery(32)` stores whatever `classify_delivery` returns. A function that only calls `print()` hands back `None` to its caller, not the printed text. To store and reuse a result, the function must use `return`. ⟦C.f1 C.f3 C:tb1 C:tb2 C:tb3⟧
### r04 · Mutable defaults are shared across calls — A default value is created once — not freshly on each call.
(misconception) A default value is evaluated only once, at the point the function is defined — not on each call. If that default is a mutable object such as a list, the same object is shared across all calls and can accumulate changes. To avoid this, create a fresh value inside the function body rather than in the parameter default. ⟦D.m1 D:tb4⟧
### r05 · Local first, then global — Python checks the local table before the global one.
(mechanism) All variable assignments in a function store the value in that function's local symbol table. When Python looks up a name inside a function, it checks the local table first, then the global table, then built-ins. A name assigned only outside the function is still readable inside — Python finds it in the global table once the local lookup fails. ⟦E.f1 E.f2 E:tb1 E:tb2⟧
### r06 · Assigning to a global requires the global statement — Reading a global is free; writing to it requires declaring it.
(misconception) A global variable cannot be directly assigned a value from inside a function unless it is named in a `global` statement. Without `global total`, writing `total = 0` inside a function creates a new local `total` and leaves the global `total` unchanged. The global may still be read without the statement. ⟦E.f3 E:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: def summarize_delivery():
    print('--- summary ---')
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· spec.expected: QuickDeliver driver ready
QuickDeliver driver ready
· ops.value: QuickDeliver driver ready_x
· expected.value: QuickDeliver driver ready_x
QuickDeliver driver ready_x
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment
· expected.value: 1049 Lagos
1043 Abuja
· expected.value: 1042 Lagos
1050 Abuja
· constraints.blocked_syntax: from module import name
· constraints.blocked_syntax: with open(...) as f:
· constraints.blocked_syntax: += and other augmented assignment

=========

# EVALUATOR PACKET — PEP 8 Style Conventions (tile_python_pep8_style)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.pep8_style — Idiomatic style conventions for readable Python

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: tile_python_pep8_style.s03: remediation tile_python_pep8_style.r01 re-teaches ['python.pep8_style#f3'] but the check measures ['python.pep8_style#f1', 'python.pep8_style#f2', 'python.pep8_style#f4'] — a learner who fails it is sent to an unrelated fact

## SOURCE FACTS — A (python.pep8_style)   objective: Reformat unstyled Python code to follow PEP 8 conventions for indentation, line length, whitespace, and naming.
A.f1: PEP 8 recommends using 4 spaces per indentation level, with spaces rather than tabs as the preferred indentation method.   [sources: pep8_style_guide#indentation, pep8_style_guide#tabs-or-spaces]
A.f2: PEP 8 recommends limiting all lines to a maximum of 79 characters.   [sources: pep8_style_guide#maximum-line-length]
A.f3: PEP 8 recommends avoiding extraneous whitespace, such as immediately inside parentheses/brackets/braces or immediately before a comma, semicolon, or colon.   [sources: pep8_style_guide#pet-peeves]
A.f4: PEP 8 recommends that function and variable names be lowercase, with words separated by underscores as necessary for readability.   [sources: pep8_style_guide#function-and-variable-names]
PRACTICE ANCHOR (live_code): Rewrite a working but poorly styled function to follow PEP 8 naming and spacing conventions.  SUCCESS: The rewritten code behaves identically and follows 4-space indentation, 79-character lines, tidy whitespace and lowercase_with_underscores names.
ASSESSMENT ANCHOR: apply_indentation_and_line_length facts=['f1', 'f2']
ASSESSMENT ANCHOR: remove_extraneous_whitespace facts=['f3']
ASSESSMENT ANCHOR: apply_naming_convention facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply transform; Boolean/conditional filtering; Comparing correlation strength across multiple variable pairs; Computing descriptive statistics with pandas (describe, mean, median, std); Concat stacking; Correlation between two variables; Correlation-vs-causation caveat in business interpretation; Creating DataFrames from dicts/lists/files; Distribution shape (skewness, symmetry, outliers); Handling missing data (isna, dropna, fillna); Identifying and reasoning about outliers; Inspecting data (head, info, describe, shape, dtypes); Map substitution; Measures of central tendency (mean, median, mode); Measures of spread (range, variance, standard deviation); Reading a frequency distribution/histogram in statistical terms; Reading data (read_csv, read_excel); Removing duplicate rows; Renaming columns and index labels; Selecting rows/columns with loc/iloc; Series and DataFrame data structures; Sorting values; String cleaning with the .str accessor; Type conversion and dtype management (astype); Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Write code others can read  [reward 5]
PEP 8 — PEP 8 is Python's style guide. Its recommendations make code easier to read for the next person — including a later you.
(definition) PEP 8 recommends using 4 spaces per indentation level, with spaces rather than tabs as the preferred indentation method, and limiting all lines to a maximum of 79 characters. PEP 8 also recommends avoiding extraneous whitespace — such as immediately inside parentheses, brackets or braces, or immediately before a comma, semicolon, or colon. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2⟧
(mechanism) PEP 8 recommends that function and variable names be lowercase, with words separated by underscores as necessary for readability — `delivery_minutes` rather than `deliveryMinutes` or `DeliveryMinutes`. ⟦A.f4 A:tb3⟧
[BEFORE_AFTER] Apply PEP 8: lowercase_with_underscores name, 4-space indent, no extraneous whitespace inside parentheses.
  before:
[CODE python]
def ClassifyDelivery( minutes,threshold ):
  if minutes>threshold:
    return 'slow'
  else:
    return 'fast'
result=ClassifyDelivery( 32,45 )
  annotations: ['CamelCase name; spaces inside parens; 2-space indent', 'No spaces around =; spaces inside parens']
  after:
[CODE python]
def classify_delivery(minutes, threshold):
    if minutes > threshold:
        return 'slow'
    else:
        return 'fast'

result = classify_delivery(32, 45)
  annotations: ['lowercase_with_underscores; no extra spaces', '4-space indent; spaces around operator', 'Spaces around = in assignment']

### s02 · check · Remove extraneous whitespace  [reward 5]
Quick check — Which line follows PEP 8's whitespace recommendation?
QUESTION [choice, intro, grading=client] Which line follows PEP 8's rule about extraneous whitespace?

```python
# A
result = compute( x , y )

# B
result = compute(x, y)

# C
result = compute(x ,y)

# D
result = compute( x,y )
```
  ✘ opt_a: A — spaces inside the parentheses make it easier to read.
      why: PEP 8 says to avoid spaces immediately inside parentheses. `compute( x , y )` has extraneous spaces inside the parentheses and before the comma.
  ✔ opt_b: B — no spaces immediately inside parentheses or before commas.
      why: Correct. PEP 8 recommends no spaces immediately inside parentheses and no space before a comma: `compute(x, y)`.
  ✘ opt_c: C — one space before the comma is acceptable.
      why: PEP 8 says to avoid a space immediately before a comma. The correct form is `compute(x, y)` — space after the comma, not before.
  ✘ opt_d: D — spaces inside parentheses are fine as long as they are symmetric.
      why: Symmetry does not make extraneous whitespace acceptable. PEP 8 says no spaces immediately inside parentheses.
  feedback✔: Right — PEP 8 says no spaces immediately inside parentheses and no space before a comma: `compute(x, y)`.  feedback✘: PEP 8 avoids extraneous whitespace: no spaces immediately inside parentheses `()`, `[]`, `{}`, and no space immediately before a comma, semicolon, or colon.  hints: ['PEP 8 says: avoid whitespace immediately inside parentheses, brackets, or braces.', 'Also avoid a space immediately before a comma. The correct pattern is `f(x, y)` — space after the comma, not before.']  remediation→r01
  MEASURES: A:remove_extraneous_whitespace(f3)   anchors=['assessment:remove_extraneous_whitespace']
  taught-before-tested: A.f3←s01

### s03 · hands_on · Restyle a function to follow PEP 8  [reward 10]
Practice — Rewrite a working but poorly styled function to use 4-space indentation, 79-character lines, and lowercase_with_underscores names.
QUESTION [code_exercise, core, grading=client] Rewrite the function below to follow PEP 8:

```python
def CalcFee( minutes,rate ):
  Fee=minutes*rate
  return Fee

print( CalcFee( 30,2 ) )
```

Apply these changes:
1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)
2. Rename `Fee` → `fee` (lowercase)
3. Rename `Minutes` → `minutes` and `Rate` → `rate` (lowercase)
4. Use **4-space** indentation (not 2 spaces)
5. Remove extraneous spaces inside `()` and before `,`

The function must still return `minutes * rate` and the print should output `60` when called with `30` and `2`.
  runtime={'kind': 'python', 'version': '0.29.5'} constraints.allowed=['name = value assignment', 'using assigned names in an expression, as in the width * height example', 'int, float, str and bool literals', 'single- or double-quoted strings', 'True / False', 'print()', 'type()', '+ - * / // % **', 'parentheses for grouping', '< <= > >= == !=', 'and', 'or', 'not', 'int()', 'float()', 'str()', '[...] list literal', 'list[i] and list[-1] indexing', 'list[a:b] slicing', 'list[i] = value', 'list.append()', 'len()', '{key: value} dictionary literal', 'd[key] lookup and assignment', 'd.get()', 'key in d', 'tuple literal with commas or parentheses', 'unpacking a, b = t', 'one-item tuple with trailing comma', 'set()', '{...} set literal', 'x in a_set', '| and & on sets', 'quote mixing to embed a quote', 'f-strings f"...{expr}..."', 'format specifier such as {value:.2f}', 'if', 'elif', 'else', 'colon and indented block', 'for item in sequence:', 'while condition:', 'break', 'continue', '[expr for x in seq]', '[expr for x in seq if cond]', '{k: v for ...}', 'for key in d:', 'for k, v in d.items():', 'def name():', 'calling name()', 'def f(a, b):', 'positional arguments in a call', 'return', 'def f(a, b=default):', 'keyword arguments f(name=value)', 'global statement', 'try:', 'except ValueError:', 'input()', 'import module', 'module.name', 'from module import name', 'open(file, mode)', 'with open(...) as f:', 'f.read()', 'f.write()', 'csv.DictReader', 'csv.DictWriter', "newline=''"] blocked=7 items
  file solution.py [editable]:
minutes = 30
rate = 2

# Rewrite the function below to follow PEP 8 style.
# Use 4-space indentation, lowercase_with_underscores names,
# and tidy whitespace. Do not change what the function does.

def CalcFee(Minutes,Rate):
  Fee=Minutes*Rate
  return Fee

print(CalcFee(minutes, rate))

  SOLUTION solution.py:
minutes = 30
rate = 2

def calc_fee(minutes, rate):
    fee = minutes * rate
    return fee

print(calc_fee(minutes, rate))

  test t1_stdout (stdout_equals, visible=True): {"expected":"60"} | on-fail: The restyled function should still print `60` when called with `30` and `2`.
  test t2_function_call_30_2 (function_call, visible=True): {"function":"calc_fee","args":[30,2],"expected":60} | on-fail: `calc_fee(30, 2)` should return `60`. Make sure the function is named `calc_fee` and returns `minutes * rate`.
  test t3_function_call_45_3 (function_call, visible=True): {"function":"calc_fee","args":[45,3],"expected":135} | on-fail: `calc_fee(45, 3)` should return `135`. Make sure the function computes `minutes * rate`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ec645599adba806577dd832e51e077d1d4801fde896e8181fd35d22eabf6837a","tests_passed":3}
  feedback✔: Well done — the restyled code uses 4-space indentation, lowercase_with_underscores names, and no extraneous whitespace.  feedback✘: Check: (1) function name `calc_fee`, (2) variable name `fee`, (3) 4 spaces of indentation, (4) no spaces inside `()` or before `,`.  hints: ['PEP 8 names use lowercase letters and underscores: `CalcFee` becomes `calc_fee`, `Fee` becomes `fee`.', 'Replace the 2-space indentation with 4 spaces, and remove the spaces inside `( )` and before `,`.']  remediation→r01
  MEASURES: A:apply_indentation_and_line_length(f1,f2); A:apply_naming_convention(f4)   anchors=['practice', 'assessment:apply_indentation_and_line_length', 'assessment:apply_naming_convention']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01

### s04 · recap · PEP 8: what you've learned  [reward 5]
Recap — Four recommendations that make Python code readable.
(takeaway) PEP 8 recommends 4 spaces per indentation level (not tabs), lines of at most 79 characters, no extraneous whitespace inside parentheses or before commas, and `lowercase_with_underscores` names for functions and variables. These are recommendations for readability — following them makes code easier to read for the next person, including a later you. ⟦A.f1 A.f4 A.f2 A.f3 A:tb4⟧
[UP NEXT] Up next: Descriptive statistics: Next you will move into statistics, starting with measures of center and spread that summarise a distribution of delivery times.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Extraneous whitespace: what to avoid — PEP 8 names specific places where extra spaces hurt readability.
(mechanism) PEP 8 recommends avoiding extraneous whitespace immediately inside parentheses, brackets or braces — `spam(ham[1], {eggs: 2})` rather than `spam( ham[ 1], { eggs: 2} )`. It also recommends no space immediately before a comma, semicolon, or colon — `x, y = 1, 2` rather than `x , y = 1 , 2`. ⟦A.f3 A:tb2⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: += and other augmented assignment