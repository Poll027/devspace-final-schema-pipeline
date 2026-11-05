# EVALUATOR PACKET — Defining Functions, Parameters, and Return Values (tile_python_functions_scope)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.defining_calling_functions — Defining calling functions
B = python.parameters_arguments — Parameters arguments
C = python.return_values — Return values
D = python.function_default_keyword_args — Default and keyword arguments
E = python.variable_scope — Variable scope (local vs global)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Call a function to run its body  [reward 10]
Practice — Write a call that runs the helper function defined for you.

### s04 · explainer · Give your function the inputs it needs  [reward 5]
Parameters — Parameters let a function work with different values on each call instead of always doing the same thing.
(intro) The formal parameters of a function are named in its `def` statement's parenthesised list. `def classify_delivery(minutes):` declares one parameter, `minutes`. Inside the body, `minutes` refers to whatever value was passed when the function was called. ⟦B.f1 B.f2 B:tb1 B:tb2⟧
(mechanism) When you call a function with positional arguments, the first argument fills the first parameter slot, the second fills the second, and so on. For `def delivery_summary(city, minutes):`, calling `delivery_summary('Lagos', 32)` sets `city` to `'Lagos'` and `minutes` to `32`. ⟦B.f3 B:tb3⟧
[DIAGRAM: Arguments fill parameter slots in order] nodes=["'Lagos'", '32', 'city', 'minutes'] edges=[('arg_city', 'par_city', '1st → 1st'), ('arg_min', 'par_min', '2nd → 2nd')] alt: Two argument values ('Lagos' and 32) on the left with arrows pointing to the matching parameter names (city and minutes) on the right, labelled 1st→1st and 2nd→2nd.

### s05 · check · Match arguments to parameters  [reward 5]
Quick check — Given a function call, which value does each parameter receive?

### s06 · hands_on · Add parameters and call with arguments  [reward 10]
Practice — Extend a function to accept a city and a delivery time, then call it with QuickDeliver order values.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s09 · check · Return and store a value  [reward 5]
Quick check — Which snippet correctly returns a value and stores it in a variable?

### s10 · hands_on · Write a function that returns a result  [reward 10]
Practice — Convert a print-only function into one that returns its result so the caller can store and reuse it.

### s11 · explainer · Optional parameters and named arguments  [reward 5]
Default and keyword arguments — Default values let callers omit arguments; keyword arguments let callers name them explicitly.
(definition) Specifying a default value for a parameter — `def ask_ok(prompt, retries=4):` — creates a function that can be called with fewer arguments than it is defined to accept. Calling `ask_ok('Delete this order?')` works and uses `4` for `retries`. ⟦D.f1 D:tb1⟧
(syntax) A function can also be called using keyword arguments of the form `kwarg=value` — `ask_ok(prompt='Delete this order?', retries=2)`. In a call, keyword arguments must follow any positional arguments. All keyword arguments must match one of the function's parameters, and no parameter may receive a value more than once. ⟦D.f2 D.f3 D:tb2 D:tb3⟧
(misconception) A default value is evaluated only once, at the point the function is defined — not on each call. If that default is a mutable object such as a list, the same object is shared across calls and can accumulate changes unless the function creates a fresh value each time. ⟦D.m1 D:tb4⟧
[DIAGRAM: Three ways to call ask_ok(prompt, retries=4)] nodes=['def ask_ok(prompt, retries=4):', "ask_ok('Delete?', 2)", "ask_ok(prompt='Delete?', retries=2)", "ask_ok('Delete?')", "prompt='Delete?', retries=2", "prompt='Delete?', retries=2", "prompt='Delete?', retries=4 (default)"] edges=[('call_pos', 'res_pos', None), ('call_kw', 'res_kw', None), ('call_def', 'res_def', None)] alt: Function signature at top with default retries=4. Three call styles below — positional, keyword, and default-omitted — each mapped to the parameter values they produce.

### s12 · video · Default values and keyword arguments  [reward 3]
Watch — See default parameters and keyword calls in action.
[VIDEO ] bridge-before:  | bridge-after: 

### s13 · check · Spot the mutable default trap  [reward 5]
Quick check — What happens when a function uses a mutable object as a default value?

### s14 · hands_on · Call with defaults and keyword arguments  [reward 10]
Practice — Call a delivery-classification function three ways: omitting a default, using positional arguments, and using keyword arguments.

### s15 · explainer · Where Python looks for a name  [reward 5]
Variable scope — A name created inside a function lives in that function's local table — it doesn't automatically reach the outside world.
(intro) All variable assignments in a function store the value in that function's local symbol table. A name like `total` assigned inside a function is a different variable from any `total` that exists outside it. ⟦E.f1 E:tb1⟧
(mechanism) For a function that is not nested inside another, variable references inside it first look in the local symbol table, then the global symbol table, and finally the table of built-in names. So a name assigned only outside the function is still readable inside it — Python finds it in the global table once the local lookup fails. ⟦E.f2 E:tb2⟧
(misconception) A global variable cannot be directly assigned a value from inside a function unless it is named in a `global` statement. Without `global total`, writing `total = 0` inside a function creates a new local `total` and leaves the global `total` unchanged. The global may still be read without the statement. ⟦E.f3 E:tb3⟧
[DIAGRAM: Local and global symbol tables] nodes=['Global symbol table', 'total = 100', 'Local symbol table (inside function)', 'total = 0  (new local)'] edges=[('local_table', 'global_table', 'lookup order: local → global → built-ins')] alt: Two nested boxes: an outer 'Global symbol table' containing total=100, and an inner 'Local symbol table' containing a separate total=0. An arrow from the inner box to the outer box is labelled 'lookup order: local → global → built-ins'.

### s16 · video · Local, global, and the global statement  [reward 3]
Watch — See the lookup order in action and when you need the global statement.
[VIDEO ] bridge-before:  | bridge-after: 

### s17 · explainer · Local shadows global without changing it  [reward 3]
Scope — A same-named local inside a function hides the global — but the global keeps its value outside.
(example) A same-named local can shadow a global inside a function without disturbing the global's value outside it. Reading the name inside the function sees the local one; code outside the function still sees the unchanged global. ⟦E.f1 E.f3 E:tb4⟧

### s18 · check · Predict name resolution  [reward 5]
Quick check — What value does the name refer to inside the function?

### s19 · check · When do you need global?  [reward 5]
Quick check — Which situation requires a global statement?

### s20 · hands_on · Local vs global names  [reward 10]
Practice — Write a function that reads a global variable and assigns a same-named local without changing the global.

### s21 · recap · Functions: what you've learned  [reward 5]
Recap — Five ideas that make functions reusable and predictable.
(takeaway) `def` creates a reusable block of code under a name; calling that name followed by parentheses is what actually runs it. Parameters name the inputs a function expects; arguments in a specific call supply the actual values. `return` turns a function from something that does an action into something that hands back a result the caller can store and reuse. Assigning to a name inside a function makes it local by default; only reading reaches out to a global unless a `global` statement says otherwise. ⟦A.f2 B.f1 B.f2 C.f1 C.f2 E.f1 E.f2 E.f3 A:tb4 B:tb4 C:tb5 E:tb5⟧
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

=========

# EVALUATOR PACKET — Handling Errors and Importing Modules (tile_python_errors_imports)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.error_handling — Basic error handling (try/except)
B = python.import_statements — Modules and imports

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[PROCESS_FLOW: try/except execution flow] nodes=['Execute try clause', 'No exception', 'Skip except clause', 'Exception raised', 'Type matches except?', 'Run except clause', 'Continue after block'] edges=[('n_try', 'n_ok', None), ('n_ok', 'n_skip', 'yes'), ('n_ok', 'n_exc', 'no'), ('n_skip', 'n_cont', None), ('n_exc', 'n_match', None), ('n_match', 'n_run', 'yes'), ('n_run', 'n_cont', None)] alt: Flowchart: 'Execute try clause' leads to a decision 'No exception?'. Yes path goes to 'Skip except clause' then 'Continue'. No path goes to 'Exception raised', then 'Type matches except?'. Yes path goes to 'Run except clause' then 'Continue'.

### s02 · check · Handle an invalid number conversion  [reward 5]
Quick check — Which code correctly catches a ValueError when converting user input to an integer?

### s03 · hands_on · Wrap risky code in try/except  [reward 10]
Practice — Add a try/except block so the script prints a message instead of crashing on bad input.

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

### s06 · hands_on · Import and use a standard module  [reward 10]
Practice — Import the sys module and print sys.path to see where Python looks for modules.

### s07 · recap · Errors and imports: what you've learned  [reward 5]
Recap — Two tools that make scripts more robust and reusable.
(takeaway) `try`/`except` lets the program attempt something that might fail and respond to the specific failure rather than stopping entirely. If no exception occurs, the `except` clause is skipped; if the exception type matches, the `except` clause runs and execution continues. `import` gives you access to code written in another file — either through the module's name (`import fibo`, `fibo.fib(...)`) or directly by name (`from fibo import fib`, `fib(...)`). ⟦A.f1 A.f2 B.f2 B.f3 A:tb4 B:tb5⟧
[UP NEXT] Up next: Reading and writing files: Next you will learn how open() and the with statement manage file connections, and how the csv module reads and writes rows as dictionaries.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Catching a ValueError from int() — The except clause only runs when the exception type matches.
(example) Wrapping `int(input(...))` in a `try` clause with `except ValueError` catches the error when the input cannot be converted. If the typed text is `'twelve'`, `int()` raises a `ValueError`, the `except` clause runs and prints a message, and the program continues. If the input is `'12'`, `int()` succeeds, the `except` clause is skipped, and `minutes_late` holds `12`. ⟦A.f3 A:tb3⟧
### r02 · import vs from … import — The two forms differ in what lands in your namespace.
(mechanism) `import fibo` adds the module name `fibo` to your namespace; you then call `fibo.fib(1000)`. `from fibo import fib` adds the name `fib` directly, so you call `fib(500)` without a prefix. Both forms import from the same module file — they differ only in what name lands in your namespace. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3⟧

=========

# EVALUATOR PACKET — Reading and Writing Files (tile_python_file_io)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.file_io — Basic file I/O (reading/writing text and CSV files)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · check · Open, read, and write a text file  [reward 5]
Quick check — Which mode string opens a file for writing, erasing any existing content?

### s05 · check · Manage a file with the with statement  [reward 5]
Quick check — What does the with statement guarantee when working with a file object?

### s06 · hands_on · Read and write CSV rows as dicts  [reward 10]
Practice — Use csv.DictReader to read orders.csv and csv.DictWriter to write a filtered output file.

### s07 · recap · File I/O: what you've learned  [reward 5]
Recap — Four ideas that connect your script to data on disk.
(takeaway) Reading and writing files is how a program's delivery data gets in from, and results get out to, storage that outlives the program run. `open()` and `with` manage the connection and guarantee the file closes. The `csv` module adds structured row-by-row access: `csv.DictReader` maps each row to a dict keyed by the header names, and `csv.DictWriter` maps dicts back to rows. ⟦A.f1 A.f2 A.f4 A.f6 A:tb9⟧
[UP NEXT] Up next: PEP 8 style: Next you will learn the PEP 8 style recommendations — indentation, line length, whitespace, and naming — that make Python code easier to read.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · open() modes and f.read() / f.write() — The mode string controls whether you read, write, or append.
(mechanism) `open(filename, mode)` returns a file object. Mode `'r'` reads (default), `'w'` writes and erases any existing file of the same name, `'a'` appends. `f.read()` returns the file's contents as a string; once the end is reached, further calls return an empty string. `f.write(string)` writes the string and returns the number of characters written. ⟦A.f1 A.f3 A.f5 A:tb1 A:tb3 A:tb5⟧
### r02 · The with statement closes the file automatically — with guarantees cleanup even when an exception occurs.
(practical_context) It is good practice to use the `with` keyword when working with a file object, because it closes the file automatically after its block finishes — even if an exception is raised. `with open('orders.txt') as f:` opens the file and assigns the file object to `f`; the file is closed when the `with` block exits, without needing an explicit `f.close()` call. ⟦A.f2 A:tb2⟧

=========

# EVALUATOR PACKET — PEP 8 Style Conventions (tile_python_pep8_style)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.pep8_style — Idiomatic style conventions for readable Python

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Restyle a function to follow PEP 8  [reward 10]
Practice — Rewrite a working but poorly styled function to use 4-space indentation, 79-character lines, and lowercase_with_underscores names.

### s04 · recap · PEP 8: what you've learned  [reward 5]
Recap — Four recommendations that make Python code readable.
(takeaway) PEP 8 recommends 4 spaces per indentation level (not tabs), lines of at most 79 characters, no extraneous whitespace inside parentheses or before commas, and `lowercase_with_underscores` names for functions and variables. These are recommendations for readability — following them makes code easier to read for the next person, including a later you. ⟦A.f1 A.f4 A:tb4⟧
[UP NEXT] Up next: Descriptive statistics: Next you will move into statistics, starting with measures of center and spread that summarise a distribution of delivery times.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Extraneous whitespace: what to avoid — PEP 8 names specific places where extra spaces hurt readability.
(mechanism) PEP 8 recommends avoiding extraneous whitespace immediately inside parentheses, brackets or braces — `spam(ham[1], {eggs: 2})` rather than `spam( ham[ 1], { eggs: 2} )`. It also recommends no space immediately before a comma, semicolon, or colon — `x, y = 1, 2` rather than `x , y = 1 , 2`. ⟦A.f3 A:tb2⟧