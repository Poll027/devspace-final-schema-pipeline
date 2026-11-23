# EVALUATOR PACKET — Computing dates and elapsed times with datetime (learn_python.tile.084_084)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.datetime_operations — Computing dates and elapsed times with datetime

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.084_084.r02 is never referenced
  warn: learn_python.tile.084_084.s03/ix.learn_python.tile.084_084.s03: ADVISORY — syntax descriptors with no detector: ['assert', 'generator expressions', 'if __name__ == "__main__":', 'parenthesized expressions', 'string literals', 'subtraction with -', 'yield', 'yield from']

## SOURCE FACTS — A (python.datetime_operations)   objective: Calculate date and time differences with datetime.
A.f1: datetime.strptime(text, format) parses text according to an explicit format, and .date() obtains its calendar date.   [sources: python_stdlib_reference#datetime.html#datetime.datetime.strptime, python_stdlib_reference#datetime.html#datetime.datetime.date]
A.f2: Use %Y-%m-%d for a year-month-day numeric date.   [sources: python_stdlib_reference#datetime.html#datetime.datetime.strptime, python_stdlib_reference#datetime.html#strftime-and-strptime-format-codes]
A.f3: Subtracting one date from another returns a timedelta representing their difference.   [sources: python_stdlib_reference#datetime.html#datetime.date]
A.f4: For calendar dates, (later_date - earlier_date).days gives their signed day difference.   [sources: python_stdlib_reference#datetime.html#datetime.timedelta]
note: Begin with this objective: Calculate date and time differences with datetime.
note: Keep the example in the Date and time operations tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.local_modules, python.importable_packages, python.logging.
PRACTICE ANCHOR (live_code): Parse two year-month-day date strings into calendar dates and compute the signed number of days between them in both subtraction orders.  SUCCESS: The dates 2025-03-01 and 2025-03-04 are parsed using %Y-%m-%d and .date(); subtracting first from second yields 3 days, and reversing the subtraction yields -3 days.
ASSESSMENT ANCHOR: parse_compatible_calendar_dates facts=['f1', 'f2']
ASSESSMENT ANCHOR: compute_signed_elapsed_days facts=['f3', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Choosing random or secrets for randomness; Creating isolated virtual environments; Creating local modules; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Guarding a program entry point; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Recording program events with logging; Recreating dependencies from requirements files; Running unittest and interpreting its results; Selecting the project environment interpreter; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Computing dates and elapsed times with datetime
Explore — 
(mechanism) Parse date text with datetime.strptime(text, format); .date() then obtains the calendar date. ⟦A.f1 A:tb2 A:tb4 A:tb1⟧
(mechanism) For numeric year-month-day text, the explicit parsing format is %Y-%m-%d. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Subtracting one date from another produces a timedelta that represents the difference. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) For calendar dates, (later_date - earlier_date).days gives a signed day difference. Reversing the subtraction reverses the sign in this example, rather than preserving an absolute distance. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
[CODE python]
from datetime import datetime
first = datetime.strptime("2025-03-01", "%Y-%m-%d").date()
second = datetime.strptime("2025-03-04", "%Y-%m-%d").date()
print(first)
print(second)
print((second - first).days)
print((first - second).days)

  annotations: ['Parse with an explicit format and obtain calendar dates.', 'Display the parsed calendar dates before comparing subtraction orders.', 'Display both subtraction orders; .days keeps the sign.']

### s02 · check · Check: compute signed elapsed days
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] Two calendar dates have already been parsed. Which statement correctly interprets (second - first).days and the reversed subtraction?
  ✔ correct: The result is signed; reversing the subtraction reverses its sign.
      why: Correct. The result is signed; reversing the subtraction reverses its sign.
  ✘ trap1: Both expressions must give the same positive distance.
      why: Calendar-date subtraction gives a signed difference, not an absolute distance.
  ✘ trap2: Subtraction returns a date, so .days reads its day of month.
      why: Subtraction returns a timedelta, not a calendar date.
  feedback✔: Correct. The result is signed; reversing the subtraction reverses its sign.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Consider what the subtraction order expresses.']  remediation→r01
  MEASURES: A:compute_signed_elapsed_days(f3,f4)   anchors=['assessment:compute_signed_elapsed_days']
  taught-before-tested: A.f3←s01; A.f4←s01

### s03 · hands_on · Practise computing dates and elapsed times with datetime
Practice — Parse two year-month-day date strings into calendar dates and compute the signed number of days between them in both subtraction orders.
QUESTION [code_exercise, core, grading=client] The fixed scaffold builds the two supplied year-month-day strings and parses them with %Y-%m-%d. Complete the editable lines: reassign first and second using their .date() methods. The fixed arithmetic then computes forward = second - first and reverse = first - second. Print forward.days and reverse.days in that order, one per line. Keep the day inputs and fixed blocks unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['from datetime import datetime', 'variable assignment', 'string literals', 'datetime.strptime(text, "%Y-%m-%d")', '.date()', 'subtraction with -', 'parenthesized expressions', '.days', 'print()'] blocked=18 items
  file main.py [editable]:
first_day = 1
second_day = 4
if True:  # Fixed scaffold; leave this block unchanged.
    from datetime import datetime
    first_text = f"2025-03-{first_day:02d}"
    second_text = f"2025-03-{second_day:02d}"
    first = datetime.strptime(first_text, "%Y-%m-%d")
    second = datetime.strptime(second_text, "%Y-%m-%d")
# Obtain calendar dates here.
if True:  # Fixed scaffold; leave this block unchanged.
    forward = second - first
    reverse = first - second
# Print both signed day counts.

  SOLUTION main.py:
first_day = 1
second_day = 4
if True:  # Fixed scaffold; leave this block unchanged.
    from datetime import datetime
    first_text = f"2025-03-{first_day:02d}"
    second_text = f"2025-03-{second_day:02d}"
    first = datetime.strptime(first_text, "%Y-%m-%d")
    second = datetime.strptime(second_text, "%Y-%m-%d")
first = first.date()
second = second.date()
if True:  # Fixed scaffold; leave this block unchanged.
    forward = second - first
    reverse = first - second
print(forward.days)
print(reverse.days)

  test test1 (stdout_equals, visible=True): {"expected":"3\n-3\n"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test2 (value_equals, visible=True): {"expr":"[type(first).__name__, type(second).__name__, forward.days, reverse.days]","expected":["date","date",3,-3]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4d0e58f6ff963477312d33b1a68e5d30661c5393115c49ba88b12e05253917b3","tests_passed":2}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Convert both parsed values with .date(), then print forward.days followed by reverse.days.']
  MEASURES: A:parse_compatible_calendar_dates(f1,f2); A:compute_signed_elapsed_days(f3,f4)   anchors=['practice', 'assessment:parse_compatible_calendar_dates', 'assessment:compute_signed_elapsed_days']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s04 · recap · Keep these ideas
Recap — 
(takeaway) Parse calendar dates with an explicit format; use subtraction and .days for a signed difference. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Creating local modules: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Computing dates and elapsed times with datetime
(mechanism) Subtracting one date from another produces a timedelta that represents the difference. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) For calendar dates, (later_date - earlier_date).days gives a signed day difference. Reversing the subtraction reverses the sign in this example, rather than preserving an absolute distance. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast subtraction order: second - first and first - second describe opposite signed differences for these calendar dates. ⟦A.f3 A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Computing dates and elapsed times with datetime
(mechanism) Parse date text with datetime.strptime(text, format); .date() then obtains the calendar date. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) For numeric year-month-day text, the explicit parsing format is %Y-%m-%d. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) Subtracting one date from another produces a timedelta that represents the difference. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(mechanism) For calendar dates, (later_date - earlier_date).days gives a signed day difference. Reversing the subtraction reverses the sign in this example, rather than preserving an absolute distance. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast subtraction order: second - first and first - second describe opposite signed differences for these calendar dates. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Creating local modules · Organising importable packages (learn_python.tile.085_086)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.local_modules — Creating local modules
B = python.importable_packages — Organising importable packages

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: remediation step learn_python.tile.085_086.r02 is never referenced
  warn: remediation step learn_python.tile.085_086.r03 is never referenced
  warn: remediation step learn_python.tile.085_086.r05 is never referenced
  warn: learn_python.tile.085_086.s05/ix.learn_python.tile.085_086.s05: ADVISORY — syntax descriptors with no detector: ['assert statements', 'generator expressions', 'if __name__ == "__main__":', 'indented function bodies', 'integer literals', 'return quantity * price', 'yield expressions']
  warn: learn_python.tile.085_086.s08/ix.learn_python.tile.085_086.s08: ADVISORY — syntax descriptors with no detector: ['assert', 'function parameters and arguments', 'generator expressions', 'if __name__ == "__main__":', 'integer literals', 'multiplication with *', 'yield', 'yield from']

## SOURCE FACTS — A (python.local_modules)   objective: Extract reusable code into a local Python module.
A.f1: A module is a file of Python definitions and statements, with a .py suffix; its filename without that suffix supplies the module name.   [sources: python_tutorial#modules.html]
A.f2: Move a shared helper definition into a sibling module, then import module and call module.helper(arguments), or use from module import helper.   [sources: python_tutorial#modules.html]
A.f3: In ordinary script invocation, the script’s directory is included in the module search path, permitting sibling-module imports.   [sources: python_tutorial#modules.html#the-module-search-path]
note: Begin with this objective: Extract reusable code into a local Python module.
note: Keep the example in the Local modules and packages tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.importable_packages, python.logging, python.main_entry_point.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Move the cost(quantity, price) helper from report.py into a sibling helpers.py file, then import and call the shared helper from report.py.  SUCCESS: helpers.py contains the cost definition, report.py no longer defines it, and the imported helper call with arguments 3 and 4 produces 12.
ASSESSMENT ANCHOR: derive_module_name_from_python_filename facts=['f1']
ASSESSMENT ANCHOR: import_and_call_a_local_helper facts=['f2']
ASSESSMENT ANCHOR: explain_sibling_import_availability_in_ordinary_script_invocation facts=['f3']

## SOURCE FACTS — B (python.importable_packages)   objective: Organize local importable Python packages.
B.f1: A regular package groups modules in a directory containing __init__.py; that file may be empty.   [sources: python_tutorial#modules.html#packages]
B.f2: Use import package.module and package.module.helper(arguments), or from package.module import helper, to access a packaged helper.   [sources: python_tutorial#modules.html#packages]
note: Begin with this objective: Organize local importable Python packages.
note: Keep the example in the Local modules and packages tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.logging, python.main_entry_point, python.argparse_command_line.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
PRACTICE ANCHOR (live_code): Group costs.py and a second related module into a local orders package containing an empty __init__.py, then import and call the cost helper through the package name.  SUCCESS: The orders directory contains both related modules and an empty __init__.py. Importing orders.costs and calling orders.costs.cost(3, 4) produces 12.
ASSESSMENT ANCHOR: create_regular_package_layout facts=['f1']
ASSESSMENT ANCHOR: import_and_call_packaged_helper facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Choosing random or secrets for randomness; Creating isolated virtual environments; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Guarding a program entry point; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Matching text patterns with re; Organising importable packages; Parsing command-line arguments with argparse; Reading and explaining generated Python; Recording program events with logging; Recreating dependencies from requirements files; Reviewing generated Python file operations for safety; Running unittest and interpreting its results; Selecting the project environment interpreter; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Creating local modules
Explore — 
(mechanism) A module is a .py file containing Python definitions and statements. Its filename without .py is the module name: helpers.py is imported as helpers, not as a dotted filename. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb1⟧
(mechanism) Move the shared cost helper into sibling helpers.py. Use import helpers with helpers.cost(quantity, price), or from helpers import cost with cost(quantity, price). Follow the import binding when choosing the call. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) In ordinary script invocation, the script directory is included in the module search path, allowing this sibling-module import. ⟦A.f3 A:tb3 A:tb4⟧
[BEFORE_AFTER] Move the shared definition into helpers.py; import helpers from sibling report.py.
  before:
[DIAGRAM: Before: definition and call in report.py] nodes=['report.py: def cost(quantity, price):\n    return quantity * price', 'report.py: cost(3, 4)'] edges=[('n1', 'n2', 'local call')] alt: Before: definition and call in report.py: report.py: def cost(quantity, price):
    return quantity * price; report.py: cost(3, 4)
  after:
[DIAGRAM: After: shared sibling module] nodes=['helpers.py: def cost(quantity, price):\n    return quantity * price', 'report.py: import helpers', 'report.py: helpers.cost(3, 4)', 'helpers.py filename → helpers module name'] edges=[('n2', 'n1', 'imports sibling'), ('n2', 'n3', 'qualified call binding'), ('n4', 'n2', 'import name')] alt: After: shared sibling module: helpers.py: def cost(quantity, price):
    return quantity * price; report.py: import helpers; report.py: helpers.cost(3, 4); helpers.py filename → helpers module name

### s02 · video · Creating local modules
Demonstration — 
[VIDEO Define and reuse helpers in sibling modules] bridge-before: Watch the first clip create helpers in a separate file and call them through its module name. The second demonstrates both module-qualified calls and direct helper imports. | bridge-after: Neither clip moves an existing helper or explains the script-directory search mechanism; the text covers both. It also explicitly states the .py suffix/name rule, which the first clip leaves unstated and the second illustrates.
  - XcfxkHrHTVE 233-372s facts=['f2'] label: Create a local module and call its helpers | summary: A new Python file named example holds a pi value and functions for squaring, cubing, circumference and circle area. The main script imports example, accesses example.pi and calls functions through the module name. Squaring 3 produces 9, and cubing it produces 27. Keeping these definitions in a separate file separates reusable calculations from the calling script.
  - CqvZ3vGoGs0 0-242s facts=['f1', 'f2'] label: Import a sibling helper with either import form | summary: The file my_module.py contains statements, a variable and a find_index helper that returns a matching position or -1 when no match exists. A sibling script imports my_module and calls my_module.find_index with a course list and the target 'Math', returning 1. The initial import also executes the module's diagnostic print statement. An alias shortens the module-qualified call; from my_module import find_index instead binds the helper directly, allowing find_index to be called without the module prefix.

### s03 · check · Check: derive module name from python filename
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] The shared helper is in helpers.py. What module name belongs in its import?
  ✔ correct: helpers
      why: Correct. helpers
  ✘ trap1: helpers.py
      why: The .py suffix is removed to obtain the module name.
  ✘ trap2: cost
      why: cost is the helper name, not the filename-derived module name.
  feedback✔: Correct. helpers  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Separate the file name from a definition inside the file.']  remediation→r01
  MEASURES: A:derive_module_name_from_python_filename(f1)   anchors=['assessment:derive_module_name_from_python_filename']
  taught-before-tested: A.f1←s01

### s04 · check · Check: explain sibling import availability in ordinary script invocation
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] report.py and helpers.py are siblings. In ordinary script invocation, why can report.py import helpers?
  ✔ correct: The script directory is included in the module search path.
      why: Correct. The script directory is included in the module search path.
  ✘ trap1: Every directory on the computer is automatically searched.
      why: The fact describes inclusion of the script directory, not every directory.
  ✘ trap2: The helper is copied into report.py before the import.
      why: Importing a sibling module does not require copying its helper definition.
  feedback✔: Correct. The script directory is included in the module search path.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Recall the location associated with ordinary script invocation.']
  MEASURES: A:explain_sibling_import_availability_in_ordinary_script_invocation(f3)   anchors=['assessment:explain_sibling_import_availability_in_ordinary_script_invocation']
  taught-before-tested: A.f3←s01

### s05 · hands_on · Practise creating local modules
Practice — Move the cost(quantity, price) helper from report.py into a sibling helpers.py file, then import and call the shared helper from report.py.
QUESTION [code_exercise, core, grading=client] The fixed scaffold extracts the supplied cost definition into sibling helpers.py. Complete the REPORT SECTION using from helpers import cost and assign result = cost(quantity, price). Do not define cost in that report section. The final fixed block records this section as report.py. Keep the inputs and adapters unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def cost(quantity, price):', 'return quantity * price', 'import helpers', 'helpers.cost(3, 4)', 'from helpers import cost', 'cost(3, 4)', 'variable assignment', 'integer literals', 'indented function bodies'] blocked=6 items
  file main.py [editable]:
if True:  # Fixed scaffold; leave this block unchanged.
    def cost(quantity, price):
        return quantity * price
    
    # Fixed workspace adapter: materialize the helper definition in a sibling file.
    import inspect as _inspect, pathlib as _pathlib, ast as _ast, textwrap as _textwrap
    _pathlib.Path('helpers.py').write_text(_textwrap.dedent(_inspect.getsource(cost)))
    del cost
# REPORT SECTION
quantity = 3
price = 4
result = None
# Import cost from helpers and compute result.
# END REPORT
if True:  # Fixed scaffold; leave this block unchanged.
    
    # Fixed adapter records the report section as report.py for layout verification.
    _text = _pathlib.Path(__file__ if '__file__' in globals() else 'main.py').read_text()
    _pathlib.Path('report.py').write_text(_text.split('# REPORT SECTION\n', 1)[1].split('# END REPORT', 1)[0])

  SOLUTION main.py:
if True:  # Fixed scaffold; leave this block unchanged.
    def cost(quantity, price):
        return quantity * price
    
    # Fixed workspace adapter: materialize the helper definition in a sibling file.
    import inspect as _inspect, pathlib as _pathlib, ast as _ast, textwrap as _textwrap
    _pathlib.Path('helpers.py').write_text(_textwrap.dedent(_inspect.getsource(cost)))
    del cost
# REPORT SECTION
quantity = 3
price = 4
from helpers import cost
result = cost(quantity, price)
# END REPORT
if True:  # Fixed scaffold; leave this block unchanged.
    
    # Fixed adapter records the report section as report.py for layout verification.
    _text = _pathlib.Path(__file__ if '__file__' in globals() else 'main.py').read_text()
    _pathlib.Path('report.py').write_text(_text.split('# REPORT SECTION\n', 1)[1].split('# END REPORT', 1)[0])

  test test1 (value_equals, visible=True): {"expr":"[result, cost(quantity, price), cost.__module__, not any(isinstance(n, _ast.FunctionDef) and n.name == 'cost' for n in _ast.parse(_pathlib.Path('report.py').read_text()).body)]","expected":[12,12,"helpers",true]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c181a2d7680eeb91ec6791f638775959c03b2290c97e2e78c0fd64dbacec3752","tests_passed":1}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: A:import_and_call_a_local_helper(f2)   anchors=['practice', 'assessment:import_and_call_a_local_helper']
  taught-before-tested: A.f2←s01

### s06 · explainer · Organising importable packages
Explore — 
(mechanism) A regular package groups modules in a directory with __init__.py, which may be empty. In the orders layout, costs.py and __init__.py belong inside the orders directory. ⟦B.f1 B:tb2 B:tb4 B:tb5 B:tb1⟧
(mechanism) Where orders is importable, use import orders.costs and orders.costs.cost(quantity, price). Alternatively, from orders.costs import cost gives the direct call cost(quantity, price). Keep package, module and helper distinct. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
[DIAGRAM: Regular package layout] nodes=['orders/', 'orders/__init__.py (may be empty)', 'orders/costs.py: cost helper', 'import orders.costs', 'orders.costs.cost(3, 4)', 'from orders.costs import cost', 'cost(quantity, price)', 'orders/: second related module'] edges=[('n1', 'n2', 'contains'), ('n1', 'n3', 'contains'), ('n4', 'n5', 'qualified call'), ('n6', 'n7', 'direct call'), ('n1', 'n8', 'contains')] alt: Regular package layout: orders/; orders/__init__.py (may be empty); orders/costs.py: cost helper; import orders.costs; orders.costs.cost(3, 4); from orders.costs import cost; cost(quantity, price); orders/: second related module

### s07 · check · Check: create regular package layout
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] Which layout meets the taught regular-package requirement for the orders modules?
  ✔ correct: orders/ contains __init__.py and the related .py modules; __init__.py may be empty.
      why: Correct. orders/ contains __init__.py and the related .py modules; __init__.py may be empty.
  ✘ trap1: Only orders.py exists, with no directory of modules.
      why: A single module file is not the described directory-based regular package.
  ✘ trap2: orders/ contains the modules but deliberately omits __init__.py.
      why: The taught regular-package layout includes __init__.py, even when empty.
  feedback✔: Correct. orders/ contains __init__.py and the related .py modules; __init__.py may be empty.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Distinguish the directory from its modules.']  remediation→r04
  MEASURES: B:create_regular_package_layout(f1)   anchors=['assessment:create_regular_package_layout']
  taught-before-tested: B.f1←s06

### s08 · hands_on · Practise organising importable packages
Practice — Group costs.py and a second related module into a local orders package containing an empty __init__.py, then import and call the cost helper through the package name.
QUESTION [code_exercise, stretch, grading=client] The fixed scaffold creates orders with an empty __init__.py and two related modules, imports orders.costs, and binds cost to orders.costs.cost. Assign result by calling this imported cost with quantity and price, then print result. Do not define a local helper or change the fixed package scaffold or inputs.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def cost(...):', 'return', 'function parameters and arguments', 'integer literals', 'multiplication with *', 'variable assignment', 'import orders.costs', 'orders.costs.cost(3, 4)', 'from orders.costs import cost', 'cost(3, 4)', 'print()'] blocked=18 items
  file main.py [editable]:
quantity = 3
price = 4
if True:  # Fixed scaffold; leave this block unchanged.
    def cost(quantity, price):
        return quantity * price
    def report(quantity):
        return quantity
    
    # Fixed workspace adapter groups the helper and a second related module.
    import inspect as _inspect, pathlib as _pathlib, textwrap as _textwrap
    _pathlib.Path('orders').mkdir(exist_ok=True)
    _pathlib.Path('orders/__init__.py').write_text('')
    _pathlib.Path('orders/costs.py').write_text(_textwrap.dedent(_inspect.getsource(cost)))
    _pathlib.Path('orders/reports.py').write_text(_textwrap.dedent(_inspect.getsource(report)))
    del cost, report
    
if True:  # Fixed package import and binding; leave unchanged.
    import orders.costs
    cost = orders.costs.cost
result = None
# Call the imported cost helper with quantity and price, then print result.

  SOLUTION main.py:
quantity = 3
price = 4
if True:  # Fixed scaffold; leave this block unchanged.
    def cost(quantity, price):
        return quantity * price
    def report(quantity):
        return quantity
    
    # Fixed workspace adapter groups the helper and a second related module.
    import inspect as _inspect, pathlib as _pathlib, textwrap as _textwrap
    _pathlib.Path('orders').mkdir(exist_ok=True)
    _pathlib.Path('orders/__init__.py').write_text('')
    _pathlib.Path('orders/costs.py').write_text(_textwrap.dedent(_inspect.getsource(cost)))
    _pathlib.Path('orders/reports.py').write_text(_textwrap.dedent(_inspect.getsource(report)))
    del cost, report
    
if True:  # Fixed package import and binding; leave unchanged.
    import orders.costs
    cost = orders.costs.cost
result = cost(quantity, price)
print(result)

  test test1 (value_equals, visible=True): {"expr":"[result, orders.costs.cost(quantity, price), orders.costs.cost.__module__, _pathlib.Path('orders/__init__.py').read_text(), _pathlib.Path('orders/reports.py').is_file()]","expected":[12,12,"orders.costs","",true]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ed6dac036826e8ef91ffd99c0d17f5befc6e8a2948d02deeda6643b07cc24142","tests_passed":1}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: B:import_and_call_packaged_helper(f2)   anchors=['practice', 'assessment:import_and_call_packaged_helper']
  taught-before-tested: B.f2←s06

### s09 · recap · Keep these ideas
Recap — 
(takeaway) Share helpers through sibling modules and match calls to import bindings. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) A regular package contains __init__.py; dotted access separates package, module and helper. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Next: Recording program events with logging: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Creating local modules
(mechanism) A module is a .py file containing Python definitions and statements. Its filename without .py is the module name: helpers.py is imported as helpers, not as a dotted filename. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(misconception) Contrast helpers.py, the file, with helpers, the import name. Match the call to the import binding. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
### r02 · Try the contrast: Creating local modules
(mechanism) In ordinary script invocation, the script directory is included in the module search path, allowing this sibling-module import. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast helpers.py, the file, with helpers, the import name. Match the call to the import binding. ⟦A.f3 A:tb3 A:tb4⟧
### r03 · Try the contrast: Creating local modules
(mechanism) Move the shared cost helper into sibling helpers.py. Use import helpers with helpers.cost(quantity, price), or from helpers import cost with cost(quantity, price). Follow the import binding when choosing the call. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) Contrast helpers.py, the file, with helpers, the import name. Match the call to the import binding. ⟦A.f2 A:tb3 A:tb4⟧
### r04 · Try the contrast: Organising importable packages
(mechanism) A regular package groups modules in a directory with __init__.py, which may be empty. In the orders layout, costs.py and __init__.py belong inside the orders directory. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
(misconception) Contrast the orders package directory with its costs module. A regular package includes __init__.py even when that file is empty. ⟦B.f1 B:tb2 B:tb4 B:tb5⟧
### r05 · Try the contrast: Organising importable packages
(mechanism) Where orders is importable, use import orders.costs and orders.costs.cost(quantity, price). Alternatively, from orders.costs import cost gives the direct call cost(quantity, price). Keep package, module and helper distinct. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast the orders package directory with its costs module. A regular package includes __init__.py even when that file is empty. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: relative imports such as from .helpers import cost
· constraints.blocked_syntax: sys.path manipulation

=========

# EVALUATOR PACKET — Recording program events with logging (learn_python.tile.087_087)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.logging — Recording program events with logging

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.087_087.r02 is never referenced
  warn: remediation step learn_python.tile.087_087.r03 is never referenced
  warn: learn_python.tile.087_087.s05/ix.learn_python.tile.087_087.s05: ADVISORY — syntax descriptors with no detector: ['assert', 'assignment', 'generator expressions', 'if __name__ == "__main__":', 'indented function bodies', 'string literals', 'yield', 'yield from']

## SOURCE FACTS — A (python.logging)   objective: Report program events using logging.
A.f1: After import logging, logger = logging.getLogger(__name__) obtains a logger named for the module.   [sources: python_stdlib_reference#logging.html#logging.getLogger]
A.f2: DEBUG is for detailed diagnostics, INFO for expected progress, WARNING for an unexpected condition while operation continues, ERROR for inability to perform a function, and CRITICAL for a serious failure.   [sources: python_stdlib_reference#logging.html#logging-levels]
A.f3: Emit events with logger.debug(message) or logger.info(message), choosing a method corresponding to the desired level.   [sources: python_stdlib_reference#logging.html#logging.Logger.debug, python_stdlib_reference#logging.html#logging.Logger.info]
A.f4: Configure application logging with logging.basicConfig(level=logging.INFO) to include INFO and higher events; the default root threshold is WARNING.   [sources: python_stdlib_reference#logging.html#logging.basicConfig]
A.f5: Propagation normally passes events to ancestor handlers; attaching handlers to both a logger and its ancestors can duplicate output, so ordinarily configure a handler at one suitable ancestor.   [sources: python_stdlib_reference#logging.html#logging.Logger.propagate]
note: Begin with this objective: Report program events using logging.
note: Keep the example in the Logging tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.main_entry_point, python.argparse_command_line, python.module_search_paths.
note: Require security.secrets_handling_basics before this consuming unit; do not introduce a general secrets-handling curriculum here.
PRACTICE ANCHOR (live_code): Replace diagnostic prints in a report helper with a module logger, using DEBUG for detailed quantity calculation and INFO for report completion.  SUCCESS: The helper uses logger.debug and logger.info instead of diagnostic prints. With application logging configured at INFO, report completion appears once and the detailed diagnostic is excluded.
ASSESSMENT ANCHOR: emit_events_with_a_module_logger facts=['f1', 'f3']
ASSESSMENT ANCHOR: choose_appropriate_logging_levels facts=['f2']
ASSESSMENT ANCHOR: predict_events_included_by_logging_threshold facts=['f4']
ASSESSMENT ANCHOR: avoid_duplicate_output_from_ancestor_handlers facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Choosing random or secrets for randomness; Creating isolated virtual environments; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Guarding a program entry point; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Matching text patterns with re; Parsing command-line arguments with argparse; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Selecting the project environment interpreter; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Recording program events with logging
Explore — 
(mechanism) After import logging, logger = logging.getLogger(__name__) obtains a logger named for the module. ⟦A.f1 A:tb2 A:tb1⟧
(mechanism) Choose the event level by meaning: DEBUG for detailed diagnostics; INFO for expected progress; WARNING for an unexpected condition while continuing; ERROR for inability to perform a function; CRITICAL for a serious failure. ⟦A.f2 A:tb3⟧
(mechanism) Emit events with the corresponding method, such as logger.debug(message) or logger.info(message). ⟦A.f3 A:tb3⟧
(mechanism) logging.basicConfig(level=logging.INFO) includes INFO and higher events. The default root threshold is WARNING. A missing DEBUG message need not mean that its line was never reached. ⟦A.f4 A:tb3⟧
(mechanism) Propagation normally sends events to ancestor handlers. Handlers on both a logger and its ancestors can duplicate output; ordinarily configure a handler at one suitable ancestor. ⟦A.f5 A:tb3⟧
[CODE python]
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.debug("Detailed quantity calculation")
logger.info("Report complete")

  annotations: ['Set the application threshold.', 'Name the logger for the module.', 'Choose diagnostic and progress event methods.']

### s02 · explainer · Recording program events with logging
Explore — 
(mechanism) With propagation enabled, use one suitable ancestor handler. Adding another handler to the module logger can emit the same event twice. ⟦A.f5 A:tb4 A:tb5⟧

### s03 · check · Check: choose appropriate logging levels / predict events included by logging threshold
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] Detailed quantity calculation is a DEBUG event and report completion is an INFO event. Application logging is configured at INFO. What should appear?
  ✔ correct: Report completion, but not the detailed calculation.
      why: Correct. Report completion, but not the detailed calculation.
  ✘ trap1: Both events, because DEBUG describes more detail.
      why: DEBUG is below the INFO threshold and is excluded.
  ✘ trap2: Neither event, because only WARNING is ever emitted.
      why: WARNING is the default root threshold; configuring INFO changes that threshold.
  feedback✔: Correct. Report completion, but not the detailed calculation.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Compare each event level with the configured threshold.']  remediation→r01
  MEASURES: A:choose_appropriate_logging_levels(f2); A:predict_events_included_by_logging_threshold(f4)   anchors=['assessment:choose_appropriate_logging_levels', 'assessment:predict_events_included_by_logging_threshold']
  taught-before-tested: A.f2←s01; A.f4←s01

### s04 · check · Check: avoid duplicate output from ancestor handlers
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] A module logger propagates events to an ancestor handler. Which arrangement avoids the taught duplicate-output trap?
  ✔ correct: Configure one suitable ancestor handler without also attaching a redundant module handler.
      why: Correct. Configure one suitable ancestor handler without also attaching a redundant module handler.
  ✘ trap1: Attach handlers to both the module logger and its ancestor for the same event.
      why: Propagation can deliver the same event to both handlers, duplicating output.
  ✘ trap2: Replace all logging events with diagnostic prints.
      why: Diagnostic prints do not implement the taught module-logger approach.
  feedback✔: Correct. Configure one suitable ancestor handler without also attaching a redundant module handler.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Trace which handlers can receive the same propagated event.']
  MEASURES: A:avoid_duplicate_output_from_ancestor_handlers(f5)   anchors=['assessment:avoid_duplicate_output_from_ancestor_handlers']
  taught-before-tested: A.f5←s01

### s05 · hands_on · Practise recording program events with logging
Practice — Replace diagnostic prints in a report helper with a module logger, using DEBUG for detailed quantity calculation and INFO for report completion.
QUESTION [code_exercise, stretch, grading=client] Bind logger to the supplied module_logger. The fixed report helper emits detail at DEBUG and completion at INFO through logger; the fixed application configures INFO and calls report(). Completion must appear once, detail must be excluded, and no handler should be added to the module logger. Leave the fixed blocks and message inputs unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import logging', 'logging.getLogger(__name__)', 'logging.basicConfig(level=logging.INFO)', 'logger = logging.getLogger(__name__)', 'logger.debug(message)', 'logger.info(message)', 'def report():', 'report()', 'print(message)', 'string literals', 'assignment', 'indented function bodies'] blocked=12 items
  file main.py [editable]:
detail = 'Detailed quantity calculation'
completion = 'Report complete'
if True:  # Fixed scaffold; leave this block unchanged.
    import logging, io as _io
    _stream = _io.StringIO()
    logging.root.handlers.clear()
    logging.root.setLevel(logging.WARNING)
if True:  # Fixed module logger and report helper; leave unchanged.
    module_logger = logging.getLogger(__name__)
    def report():
        logger.debug(detail)
        logger.info(completion)
logger = None
# Bind logger to the supplied module_logger.
if True:  # Fixed scaffold; leave this block unchanged.
    logging.basicConfig(level=logging.INFO, stream=_stream, format='%(message)s')
    report()

  SOLUTION main.py:
detail = 'Detailed quantity calculation'
completion = 'Report complete'
if True:  # Fixed scaffold; leave this block unchanged.
    import logging, io as _io
    _stream = _io.StringIO()
    logging.root.handlers.clear()
    logging.root.setLevel(logging.WARNING)
if True:  # Fixed module logger and report helper; leave unchanged.
    module_logger = logging.getLogger(__name__)
    def report():
        logger.debug(detail)
        logger.info(completion)
logger = module_logger
if True:  # Fixed scaffold; leave this block unchanged.
    logging.basicConfig(level=logging.INFO, stream=_stream, format='%(message)s')
    report()

  test test1 (value_equals, visible=True): {"expr":"[_stream.getvalue(), len(logger.handlers)]","expected":["Report complete\n",0]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6b15731743e15605614224ebabace0d468066771d71c4e5ce987bd63b74825aa","tests_passed":1}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: A:emit_events_with_a_module_logger(f1,f3)   anchors=['practice', 'assessment:emit_events_with_a_module_logger']
  taught-before-tested: A.f1←s01; A.f3←s01

### s06 · recap · Keep these ideas
Recap — 
(takeaway) Choose meaningful levels, configure thresholds, and avoid duplicate handlers along propagation. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Guarding a program entry point: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Recording program events with logging
(mechanism) Choose the event level by meaning: DEBUG for detailed diagnostics; INFO for expected progress; WARNING for an unexpected condition while continuing; ERROR for inability to perform a function; CRITICAL for a serious failure. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) logging.basicConfig(level=logging.INFO) includes INFO and higher events. The default root threshold is WARNING. A missing DEBUG message need not mean that its line was never reached. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast expected progress with detailed diagnostics: choose the event method, then consider the configured threshold and handler placement. ⟦A.f2 A.f4 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Recording program events with logging
(mechanism) Propagation normally sends events to ancestor handlers. Handlers on both a logger and its ancestors can duplicate output; ordinarily configure a handler at one suitable ancestor. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast expected progress with detailed diagnostics: choose the event method, then consider the configured threshold and handler placement. ⟦A.f5 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Recording program events with logging
(mechanism) After import logging, logger = logging.getLogger(__name__) obtains a logger named for the module. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Emit events with the corresponding method, such as logger.debug(message) or logger.info(message). ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast expected progress with detailed diagnostics: choose the event method, then consider the configured threshold and handler placement. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4⟧

=========

# EVALUATOR PACKET — Guarding a program entry point · Parsing command-line arguments with argparse (learn_python.tile.088_089)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.main_entry_point — Guarding a program entry point
B = python.argparse_command_line — Parsing command-line arguments with argparse

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step learn_python.tile.088_089.r02 is never referenced
  warn: remediation step learn_python.tile.088_089.r04 is never referenced
  warn: learn_python.tile.088_089.s04/ix.learn_python.tile.088_089.s04: ADVISORY — syntax descriptors with no detector: ['argparse', 'assert statements', 'function calls', 'generator expressions', 'if __name__ == "__main__":', 'indented blocks', 'itertools', 'module attribute access', 'return quantity * price', 'string and integer literals', 'sys', 'unittest', 'yield']
  warn: learn_python.tile.088_089.s08/ix.learn_python.tile.088_089.s08: ADVISORY — syntax descriptors with no detector: ['assert']

## SOURCE FACTS — A (python.main_entry_point)   objective: Separate importable definitions from script-only execution.
A.f1: A module executed as the main script has __name__ equal to "__main__"; an imported module has its module name instead.   [sources: python_tutorial#modules.html#executing-modules-as-scripts]
A.f2: Put command-interface actions under if __name__ == "__main__": so importing the module does not execute those actions.   [sources: python_tutorial#modules.html#executing-modules-as-scripts]
A.f3: Keep reusable helper definitions outside that guarded command-interface body so importers can use them.   [sources: python_tutorial#modules.html#executing-modules-as-scripts]
note: Begin with this objective: Separate importable definitions from script-only execution.
note: Keep the example in the Entry points and command-line arguments tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.argparse_command_line, python.module_search_paths, python.os_environment.
PRACTICE ANCHOR (live_code): Make the cost helper importable without triggering user prompts, while retaining the script's interactive cost calculation during direct execution.  SUCCESS: Importing the module produces no prompts or command output, and cost(3, 4) returns 12. Running the file directly still prompts for quantity and price and displays their calculated cost.
ASSESSMENT ANCHOR: distinguish_main_script_and_imported_module_names facts=['f1']
ASSESSMENT ANCHOR: guard_command_interface_actions_against_import_execution facts=['f1', 'f2']
ASSESSMENT ANCHOR: preserve_importable_helper_definitions facts=['f3']

## SOURCE FACTS — B (python.argparse_command_line)   objective: Parse a script's command-line interface with argparse.
B.f1: After import argparse, create parser = argparse.ArgumentParser() to define a command interface.   [sources: python_stdlib_reference#argparse.html#argparse.ArgumentParser]
B.f2: parser.add_argument("input_path") declares a required positional value, while a name starting with -- declares an option.   [sources: python_stdlib_reference#argparse.html#argparse.ArgumentParser.add_argument]
B.f3: parser.add_argument("--verbose", action="store_true") creates a boolean flag that defaults to False and becomes True when present.   [sources: python_stdlib_reference#argparse.html#action]
B.f4: args = parser.parse_args() parses the command line into attributes such as args.input_path and args.verbose.   [sources: python_stdlib_reference#argparse.html#argparse.ArgumentParser.parse_args]
B.f5: By default invalid arguments produce an error message and exit status 2; missing required arguments are invalid.   [sources: python_stdlib_reference#argparse.html#invalid-arguments]
note: Begin with this objective: Parse a script's command-line interface with argparse.
note: Keep the example in the Entry points and command-line arguments tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.module_search_paths, python.os_environment, python.random_vs_secrets.
PRACTICE ANCHOR (live_code): Give the order-report script a required input_path argument and an optional --verbose flag, then inspect the parsed values.  SUCCESS: Supplying orders.csv yields input_path equal to orders.csv and verbose equal to False; adding --verbose changes verbose to True. Omitting input_path produces an argparse error and exit status 2.
ASSESSMENT ANCHOR: implement_required_input_path facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: implement_optional_boolean_flag facts=['f2', 'f3', 'f4']
ASSESSMENT ANCHOR: reject_invalid_command_line_invocation facts=['f5']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accessing environment variables with os.environ; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Choosing random or secrets for randomness; Creating isolated virtual environments; Development checks with the Python assert statement; Diagnosing module search-path problems; Generator expressions; Generator functions with yield; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Matching text patterns with re; Parsing command-line arguments with argparse; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Selecting the project environment interpreter; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Guarding a program entry point
Explore — 
(mechanism) When a module runs as the main script, __name__ is "__main__". When imported, __name__ is its module name instead. ⟦A.f1 A:tb2 A:tb4 A:tb1⟧
(mechanism) Place command-interface actions inside if __name__ == "__main__":. Importing the module then does not execute those guarded actions; the guard applies only to its body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Keep reusable helper definitions outside the guarded body so importers can use them. Guard the command actions, not the shared cost definition. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
def cost(quantity, price):
    return quantity * price

if __name__ == "__main__":
    print(cost(3, 4))

  annotations: ['Reusable helper remains outside the guard.', 'Only the guarded command action depends on main-script execution.']

### s02 · video · Guarding a program entry point
Demonstration — 
[VIDEO Separate script execution from importing] bridge-before: Watch how each module's __name__ changes with its execution role and how the guard controls output. The presenter calls main a method; here, it is a function. | bridge-after: The clip explains execution names and guarded calls, but not how to preserve reusable helpers for importers. The text covers that requirement: keep helper definitions outside the guarded body.
  - sugvnHA7ElY 0-298s facts=['f1', 'f2'] label: Compare direct execution and importing with the __main__ guard | summary: Running first_module directly gives its __name__ the value "__main__". When second_module imports it, first_module's __name__ is "first_module", while the directly executed second_module has __name__ equal to "__main__". Initially, an unguarded print in first_module executes during import. Moving that action into a main function and calling it under if __name__ == "__main__": preserves the output during direct execution but prevents that call during import. The guard controls the actions inside its body; it does not stop the module from being imported.

### s03 · check · Check: guard command interface actions against import execution
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] A module must expose cost for imports but prompt for input only during direct execution. Which boundary is correct?
  ✔ correct: Define cost at module level; guard the prompts and display with if __name__ == "__main__":.
      why: Correct. Define cost at module level; guard the prompts and display with if __name__ == "__main__":.
  ✘ trap1: Put cost and all command actions inside the guard.
      why: Import does not execute the guarded body, so the helper would not be defined there.
  ✘ trap2: Leave prompts outside the guard and guard only the print.
      why: Only guarded actions are skipped on import; unguarded prompts would still run.
  feedback✔: Correct. Define cost at module level; guard the prompts and display with if __name__ == "__main__":.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Check every command-interface action, not just its final output.']  remediation→r01
  MEASURES: A:guard_command_interface_actions_against_import_execution(f1,f2)   anchors=['assessment:guard_command_interface_actions_against_import_execution']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Practise guarding a program entry point
Practice — Make the cost helper importable without triggering user prompts, while retaining the script's interactive cost calculation during direct execution.
QUESTION [code_exercise, core, grading=client] The supplied cost helper remains at module level, and the fixed __main__ guard handles direct execution only. Bind read_quantity and read_price to input, convert to int, and display to print. Leave the helper, guard, input adapter and input values unchanged. Direct execution must prompt for quantity and price and display their cost; importing must produce no prompts or output and leave cost callable.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def cost(quantity, price):', 'return quantity * price', 'if __name__ == "__main__":', 'indented blocks', 'variable assignment', 'input()', 'int()', 'print()', 'function calls', 'string and integer literals', 'import statements', 'module attribute access'] blocked=12 items
  file main.py [editable]:
quantity_input = 3
price_input = 4
if True:  # Fixed scaffold; leave this block unchanged.
    import builtins as _builtins, io as _io, contextlib as _contextlib, pathlib as _pathlib
    _inputs = iter([str(quantity_input), str(price_input)])
    _builtin_input = _builtins.input
    _builtins.input = lambda prompt='': next(_inputs)
# LEARNER SECTION
if True:  # Fixed importable cost helper; leave unchanged.
    def cost(quantity, price):
        return quantity * price
read_quantity = None
read_price = None
convert = None
display = None
# Bind the readers, conversion and display functions.
if __name__ == "__main__":  # Fixed direct-execution guard; leave unchanged.
    quantity = convert(read_quantity("Quantity: "))
    price = convert(read_price("Price: "))
    display(cost(quantity, price))
# END LEARNER
if True:  # Fixed scaffold; leave this block unchanged.
    
    # Fixed adapter checks the same learner section in import mode with prompts forbidden.
    _builtins.input = _builtin_input
    def import_case(q, p):
        section = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\n', 1)[1].split('# END LEARNER', 1)[0]
        out = _io.StringIO()
        def forbidden(prompt=''):
            raise RuntimeError('prompt during import')
        previous = _builtins.input
        _builtins.input = forbidden
        try:
            ns = {'__name__': 'report'}
            with _contextlib.redirect_stdout(out):
                exec(section, ns)
            return [out.getvalue(), ns['cost'](q,p)]
        finally:
            _builtins.input = previous

  SOLUTION main.py:
quantity_input = 3
price_input = 4
if True:  # Fixed scaffold; leave this block unchanged.
    import builtins as _builtins, io as _io, contextlib as _contextlib, pathlib as _pathlib
    _inputs = iter([str(quantity_input), str(price_input)])
    _builtin_input = _builtins.input
    _builtins.input = lambda prompt='': next(_inputs)
# LEARNER SECTION
if True:  # Fixed importable cost helper; leave unchanged.
    def cost(quantity, price):
        return quantity * price
read_quantity = input
read_price = input
convert = int
display = print
if __name__ == "__main__":  # Fixed direct-execution guard; leave unchanged.
    quantity = convert(read_quantity("Quantity: "))
    price = convert(read_price("Price: "))
    display(cost(quantity, price))
# END LEARNER
if True:  # Fixed scaffold; leave this block unchanged.
    
    # Fixed adapter checks the same learner section in import mode with prompts forbidden.
    _builtins.input = _builtin_input
    def import_case(q, p):
        section = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\n', 1)[1].split('# END LEARNER', 1)[0]
        out = _io.StringIO()
        def forbidden(prompt=''):
            raise RuntimeError('prompt during import')
        previous = _builtins.input
        _builtins.input = forbidden
        try:
            ns = {'__name__': 'report'}
            with _contextlib.redirect_stdout(out):
                exec(section, ns)
            return [out.getvalue(), ns['cost'](q,p)]
        finally:
            _builtins.input = previous

  test test1 (stdout_equals, visible=True): {"expected":"12\n"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test2 (function_call, visible=True): {"function":"import_case","args":[3,4],"expected":["",12]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test3 (function_call, visible=True): {"function":"import_case","args":[4,7],"expected":["",28]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"281cb187c69cbd1adecbf8e5be5ca9893feb45a43b1cc236724a204d02f241ce","tests_passed":3}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: A:distinguish_main_script_and_imported_module_names(f1); A:preserve_importable_helper_definitions(f3)   anchors=['practice', 'assessment:distinguish_main_script_and_imported_module_names', 'assessment:preserve_importable_helper_definitions']
  taught-before-tested: A.f1←s01; A.f3←s01

### s05 · explainer · Parsing command-line arguments with argparse
Explore — 
(mechanism) After import argparse, create parser = argparse.ArgumentParser() to define the command interface. ⟦B.f1 B:tb2 B:tb1⟧
(mechanism) parser.add_argument("input_path") defines a required positional value. An argument name beginning with -- defines an option. ⟦B.f2 B:tb3⟧
(mechanism) parser.add_argument("--verbose", action="store_true") defines a boolean flag: absent means False; present means True. Its presence selects it, rather than a following text value. ⟦B.f3 B:tb3⟧
(mechanism) args = parser.parse_args() parses command-line arguments into attributes such as args.input_path and args.verbose. ⟦B.f4 B:tb3⟧
(mechanism) Invalid arguments, including missing required arguments, produce an error message and exit status 2 by default. ⟦B.f5 B:tb3⟧
[DIAGRAM: Command interface and parsed attributes] nodes=['Argument declarations: required input_path; --verbose with store_true', 'orders.csv → args.input_path: orders.csv; args.verbose: False', 'orders.csv --verbose → args.input_path: orders.csv; args.verbose: True', 'No input_path → error message; default exit status 2'] edges=[('n1', 'n2', 'invocation case'), ('n1', 'n3', 'invocation case'), ('n1', 'n4', 'invocation case')] alt: Command interface and parsed attributes: Argument declarations: required input_path; --verbose with store_true; orders.csv → args.input_path: orders.csv; args.verbose: False; orders.csv --verbose → args.input_path: orders.csv; args.verbose: True; No input_path → error message; default exit status 2

### s06 · explainer · Parsing command-line arguments with argparse
Explore — 
(mechanism) input_path requires a value. --verbose is selected by presence and does not consume a following text value. Missing input_path is invalid and produces an error with default exit status 2. ⟦B.f2 B.f3 B.f5 B:tb4 B:tb5⟧

### s07 · check · Check: reject invalid command line invocation
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] A parser declares required positional input_path and optional --verbose with store_true. No command-line arguments are supplied. What happens by default?
  ✔ correct: An argparse error is reported and the process exits with status 2.
      why: Correct. An argparse error is reported and the process exits with status 2.
  ✘ trap1: input_path becomes an empty string and execution succeeds.
      why: A missing required positional argument is invalid, not an implicit empty value.
  ✘ trap2: --verbose supplies the missing input_path automatically.
      why: The optional boolean flag does not replace the required positional value.
  feedback✔: Correct. An argparse error is reported and the process exits with status 2.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Identify which declaration makes a value required.']  remediation→r03
  MEASURES: B:reject_invalid_command_line_invocation(f5)   anchors=['assessment:reject_invalid_command_line_invocation']
  taught-before-tested: B.f5←s05

### s08 · hands_on · Practise parsing command-line arguments with argparse
Practice — Give the order-report script a required input_path argument and an optional --verbose flag, then inspect the parsed values.
QUESTION [code_exercise, stretch, grading=client] Complete the three argument-definition inputs: positional_name = input_path_name, option_name = verbose_name, and option_action = boolean_action. The supplied strings specify input_path, --verbose, and store_true. The fixed ArgumentParser skeleton declares these arguments, parses into args, and prints args.input_path, args.verbose. Preserve the skeleton and adapter: orders.csv must produce False without the flag and True with it; omitting input_path must report an argparse error and exit 2.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import argparse', 'parser = argparse.ArgumentParser()', 'parser.add_argument("input_path")', 'parser.add_argument("--verbose", action="store_true")', 'args = parser.parse_args()', 'args.input_path', 'args.verbose', 'print(args.input_path, args.verbose)'] blocked=7 items
  file main.py [editable]:
path_input = 'orders.csv'
if True:  # Fixed scaffold; leave this block unchanged.
    # Fixed adapter supplies the command line and independently checks fresh invocations.
    import sys as _sys, pathlib as _pathlib, io as _io, contextlib as _contextlib
    _old_argv = _sys.argv
    _sys.argv = ['report.py', path_input]
# LEARNER SECTION
if True:  # Fixed scaffold; leave this block unchanged.
    input_path_name = "input_path"
    verbose_name = "--verbose"
    boolean_action = "store_true"
positional_name = None
option_name = None
option_action = None
if True:  # Fixed scaffold; leave this block unchanged.
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(positional_name)
    parser.add_argument(option_name, action=option_action)
    args = parser.parse_args()
    print(args.input_path, args.verbose)
# END LEARNER
if True:  # Fixed scaffold; leave this block unchanged.
    
    _sys.argv = _old_argv
    def command_case(argv):
        code = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\n',1)[1].split('# END LEARNER',1)[0]
        out, err = _io.StringIO(), _io.StringIO()
        previous = _sys.argv
        _sys.argv = ['report.py'] + argv
        status = 0
        try:
            with _contextlib.redirect_stdout(out), _contextlib.redirect_stderr(err):
                try:
                    exec(code, {'__name__': '__main__'})
                except SystemExit as e:
                    status = e.code
            return [out.getvalue().strip(), status, 'input_path' in err.getvalue()]
        finally:
            _sys.argv = previous

  SOLUTION main.py:
path_input = 'orders.csv'
if True:  # Fixed scaffold; leave this block unchanged.
    # Fixed adapter supplies the command line and independently checks fresh invocations.
    import sys as _sys, pathlib as _pathlib, io as _io, contextlib as _contextlib
    _old_argv = _sys.argv
    _sys.argv = ['report.py', path_input]
# LEARNER SECTION
if True:  # Fixed scaffold; leave this block unchanged.
    input_path_name = "input_path"
    verbose_name = "--verbose"
    boolean_action = "store_true"
positional_name = input_path_name
option_name = verbose_name
option_action = boolean_action
if True:  # Fixed scaffold; leave this block unchanged.
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(positional_name)
    parser.add_argument(option_name, action=option_action)
    args = parser.parse_args()
    print(args.input_path, args.verbose)
# END LEARNER
if True:  # Fixed scaffold; leave this block unchanged.
    
    _sys.argv = _old_argv
    def command_case(argv):
        code = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\n',1)[1].split('# END LEARNER',1)[0]
        out, err = _io.StringIO(), _io.StringIO()
        previous = _sys.argv
        _sys.argv = ['report.py'] + argv
        status = 0
        try:
            with _contextlib.redirect_stdout(out), _contextlib.redirect_stderr(err):
                try:
                    exec(code, {'__name__': '__main__'})
                except SystemExit as e:
                    status = e.code
            return [out.getvalue().strip(), status, 'input_path' in err.getvalue()]
        finally:
            _sys.argv = previous

  test test1 (stdout_equals, visible=True): {"expected":"orders.csv False\n"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test2 (function_call, visible=True): {"function":"command_case","args":[["orders.csv"]],"expected":["orders.csv False",0,false]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test3 (function_call, visible=True): {"function":"command_case","args":[["orders.csv","--verbose"]],"expected":["orders.csv True",0,false]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test4 (function_call, visible=True): {"function":"command_case","args":[[]],"expected":["",2,true]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c24bbdafd428ae7587458ddc06473b5fd093942d11b9f1fdce30c1eb3c1d92a0","tests_passed":4}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: B:implement_required_input_path(f1,f2,f4); B:implement_optional_boolean_flag(f2,f3,f4)   anchors=['practice', 'assessment:implement_required_input_path', 'assessment:implement_optional_boolean_flag']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f4←s05; B.f2←s05; B.f3←s05; B.f4←s05

### s09 · recap · Keep these ideas
Recap — 
(takeaway) Guard command actions while keeping reusable helpers available to importers. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Declare required values and presence-only flags; parse attributes and recognise invalid arguments. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Next: Diagnosing module search-path problems: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Guarding a program entry point
(mechanism) When a module runs as the main script, __name__ is "__main__". When imported, __name__ is its module name instead. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Place command-interface actions inside if __name__ == "__main__":. Importing the module then does not execute those guarded actions; the guard applies only to its body. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast running report.py as the main script with importing report. The guarded actions and the unguarded helper have different roles. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Guarding a program entry point
(mechanism) When a module runs as the main script, __name__ is "__main__". When imported, __name__ is its module name instead. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) Keep reusable helper definitions outside the guarded body so importers can use them. Guard the command actions, not the shared cost definition. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast running report.py as the main script with importing report. The guarded actions and the unguarded helper have different roles. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Parsing command-line arguments with argparse
(mechanism) Invalid arguments, including missing required arguments, produce an error message and exit status 2 by default. ⟦B.f5 B:tb3 B:tb4⟧
(misconception) Contrast the required input_path value with the presence-only --verbose flag. Missing a required value is invalid. ⟦B.f5 B:tb3 B:tb4⟧
### r04 · Try the contrast: Parsing command-line arguments with argparse
(mechanism) After import argparse, create parser = argparse.ArgumentParser() to define the command interface. ⟦B.f1 B:tb2 B:tb4⟧
(mechanism) parser.add_argument("input_path") defines a required positional value. An argument name beginning with -- defines an option. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) parser.add_argument("--verbose", action="store_true") defines a boolean flag: absent means False; present means True. Its presence selects it, rather than a following text value. ⟦B.f3 B:tb3 B:tb4 B:tb5⟧
(mechanism) args = parser.parse_args() parses command-line arguments into attributes such as args.input_path and args.verbose. ⟦B.f4 B:tb3 B:tb4⟧
(misconception) Contrast the required input_path value with the presence-only --verbose flag. Missing a required value is invalid. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧

=========

# EVALUATOR PACKET — Diagnosing module search-path problems (learn_python.tile.090_090)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.module_search_paths — Diagnosing module search-path problems

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.090_090.r02 is never referenced
  warn: learn_python.tile.090_090.s04/ix.learn_python.tile.090_090.s04: ADVISORY — syntax descriptors with no detector: ['assert', 'yield', 'yield from']

## SOURCE FACTS — A (python.module_search_paths)   objective: Diagnose Python module discovery and name shadowing.
A.f1: After checking built-in modules, an ordinary import searches sys.path for the named module; the script directory normally comes before standard-library directories.   [sources: python_tutorial#modules.html#the-module-search-path]
A.f2: A local file with the same name as a standard-library module can shadow that module; rename the conflicting local file to remove that ambiguity.   [sources: python_tutorial#modules.html#the-module-search-path]
A.f3: Inspect sys.path to see the search locations used by the interpreter.   [sources: python_stdlib_reference#sys.html#sys.path]
A.f4: Inspect module.__file__ to locate a file-backed imported module.   [sources: python_tutorial#modules.html]
note: Begin with this objective: Diagnose Python module discovery and name shadowing.
note: Keep the example in the Module search paths tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.os_environment, python.random_vs_secrets, python.regular_expressions.
PRACTICE ANCHOR (live_code): Diagnose and fix a local json.py filename that shadows the standard-library json module.  SUCCESS: The conflicting local file has a non-conflicting name, and a fresh diagnostic run shows json.__file__ pointing to the standard-library module rather than the local file.
ASSESSMENT ANCHOR: diagnose_wrong_module_resolution facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: diagnose_module_not_found_from_search_locations facts=['f1', 'f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Accessing environment variables with os.environ; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Choosing random or secrets for randomness; Creating isolated virtual environments; Development checks with the Python assert statement; Generator expressions; Generator functions with yield; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Matching text patterns with re; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Selecting the project environment interpreter; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Diagnosing module search-path problems
Explore — 
(mechanism) An ordinary import checks built-in modules, then searches sys.path. The script directory normally precedes standard-library directories. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb1⟧
(mechanism) A same-named local file can shadow a standard-library module. Rename the conflicting local file to remove the ambiguity; a familiar import name alone does not prove its source. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) Inspect sys.path for the search locations used by the executing interpreter. Exact paths depend on the environment. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) For a file-backed imported module, inspect module.__file__ to locate its file. In the diagnostic example, inspect json.__file__ rather than guessing from the name json. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
[BEFORE_AFTER] Paths are schematic; exact paths depend on the executing environment.
  before:
[DIAGRAM: Before: schematic local import] nodes=['Local file: json.py', 'sys.path: script directory before standard-library directories', 'json.__file__: local json.py'] edges=[('n1', 'n2', 'search order'), ('n2', 'n3', 'imported location')] alt: Before: schematic local import: Local file: json.py; sys.path: script directory before standard-library directories; json.__file__: local json.py
  after:
[DIAGRAM: After: schematic repaired import] nodes=['Local file renamed: no longer json.py', 'Fresh run: inspect sys.path and json.__file__', 'json.__file__: standard-library json module location'] edges=[('n1', 'n2', 'fresh run'), ('n2', 'n3', 'imported location')] alt: After: schematic repaired import: Local file renamed: no longer json.py; Fresh run: inspect sys.path and json.__file__; json.__file__: standard-library json module location

### s02 · video · Diagnosing module search-path problems
Demonstration — 
[VIDEO Inspecting module search locations] bridge-before: Watch how importing sys and printing sys.path exposes the directories Python searches when resolving a module name. | bridge-after: The clip teaches search-location inspection. The text also covers built-in checks, script-directory precedence, renaming a shadowing local file, and using module.__file__ to locate an imported file.
  - CqvZ3vGoGs0 374-415s facts=['f3'] label: Inspect Python's module search locations with sys.path | summary: Python uses a list of search locations to find modules by name. Importing sys and displaying sys.path reveals the directories searched by the interpreter. The demonstration prints this list and explains that Python searches its locations in order.

### s03 · check · Check: diagnose module not found from search locations
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] An ordinary script imports a file-backed helper that is not built in. ModuleNotFoundError occurs. What is the relevant first diagnostic?
  ✔ correct: Inspect sys.path and whether the helper is available in those search locations.
      why: Correct. Inspect sys.path and whether the helper is available in those search locations.
  ✘ trap1: Change the logging threshold instead of inspecting module search locations.
      why: The search locations, not a logging threshold, determine ordinary module discovery.
  ✘ trap2: Assume Python searches every unrelated directory automatically.
      why: Ordinary imports search sys.path, not every directory on the computer.
  feedback✔: Correct. Inspect sys.path and whether the helper is available in those search locations.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Focus on where this interpreter searches for the named module.']  remediation→r01
  MEASURES: A:diagnose_module_not_found_from_search_locations(f1,f3)   anchors=['assessment:diagnose_module_not_found_from_search_locations']
  taught-before-tested: A.f1←s01; A.f3←s01

### s04 · hands_on · Practise diagnosing module search-path problems
Practice — Diagnose and fix a local json.py filename that shadows the standard-library json module.
QUESTION [code_exercise, intro, grading=client] The first-line Workspace filename controls the local file materialized by the fixed adapter. Diagnose the conflicting json.py using sys.path and json.__file__. Choose a non-conflicting filename for the local report-data module; report_data.py is the required repaired filename for this exercise and retain the diagnostic imports and both prints. In a fresh run json.__file__ must identify the standard library, not the local file. Keep the adapter unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import sys', 'import json', 'print(sys.path)', 'print(json.__file__)'] blocked=14 items
  file main.py [editable]:
# Workspace filename: json.py
# Fixed adapter materializes the editable local filename and runs a fresh diagnostic import.
project = 'order_project'
import pathlib as _pathlib, sys as _sys
_filename = _pathlib.Path('main.py').read_text().splitlines()[0].split(': ',1)[1]
_pathlib.Path(project).mkdir(exist_ok=True)
_pathlib.Path(project, _filename).write_text('# Local report data module.\n')
_sys.path.insert(0, str(_pathlib.Path(project).resolve()))
_sys.modules.pop('json', None)
import sys
import json
print(sys.path)
print(json.__file__)

  SOLUTION main.py:
# Workspace filename: report_data.py
# Fixed adapter materializes the editable local filename and runs a fresh diagnostic import.
project = 'order_project'
import pathlib as _pathlib, sys as _sys
_filename = _pathlib.Path('main.py').read_text().splitlines()[0].split(': ',1)[1]
_pathlib.Path(project).mkdir(exist_ok=True)
_pathlib.Path(project, _filename).write_text('# Local report data module.\n')
_sys.path.insert(0, str(_pathlib.Path(project).resolve()))
_sys.modules.pop('json', None)
import sys
import json
print(sys.path)
print(json.__file__)

  test test1 (value_equals, visible=True): {"expr":"[sys.path[0], json.__file__, _pathlib.Path(project, 'report_data.py').exists(), not _pathlib.Path(project, 'json.py').exists()]","expected":["/home/pyodide/order_project","/lib/python313.zip/json/__init__.py",true,true]} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"0cbc98ca23d632125225031f83e46194f9138f3e42cff3e8d0c29d6bf54d217a","tests_passed":1}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: A:diagnose_wrong_module_resolution(f1,f2,f4)   anchors=['practice', 'assessment:diagnose_wrong_module_resolution']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01

### s05 · recap · Keep these ideas
Recap — 
(takeaway) Inspect search locations and imported files; resolve conflicting local filenames. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Accessing environment variables with os.environ: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Diagnosing module search-path problems
(mechanism) An ordinary import checks built-in modules, then searches sys.path. The script directory normally precedes standard-library directories. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Inspect sys.path for the search locations used by the executing interpreter. Exact paths depend on the environment. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast the name json with the file actually imported. A local json.py can conflict with the standard-library module. ⟦A.f1 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Diagnosing module search-path problems
(mechanism) An ordinary import checks built-in modules, then searches sys.path. The script directory normally precedes standard-library directories. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) A same-named local file can shadow a standard-library module. Rename the conflicting local file to remove the ambiguity; a familiar import name alone does not prove its source. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) For a file-backed imported module, inspect module.__file__ to locate its file. In the diagnostic example, inspect json.__file__ rather than guessing from the name json. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast the name json with the file actually imported. A local json.py can conflict with the standard-library module. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· expected.value: /home/pyodide/order_project_x

=========

# EVALUATOR PACKET — Accessing environment variables with os.environ (learn_python.tile.091_091)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.os_environment — Accessing environment variables with os.environ

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.091_091.r02 is never referenced
  warn: remediation step learn_python.tile.091_091.r03 is never referenced
  warn: learn_python.tile.091_091.s04/ix.learn_python.tile.091_091.s04: ADVISORY — syntax descriptors with no detector: ['assert', 'generator expressions', 'if/else', 'is None', 'string literals', 'yield', 'yield from']

## SOURCE FACTS — A (python.os_environment)   objective: Read environment-variable configuration with os.environ.
A.f1: os.environ maps process environment names to string values.   [sources: python_stdlib_reference#os.html#os.environ]
A.f2: os.environ.get("SETTING", fallback) returns the configured string or fallback if the name is absent; without a fallback it returns None for absence.   [sources: python_stdlib_reference#stdtypes.html#dict.get]
A.f3: For a required setting, check absence explicitly or use bracket lookup, which raises KeyError for a missing key; report missing configuration instead of proceeding with an unintended value.   [sources: python_stdlib_reference#stdtypes.html#dict, python_tutorial#errors.html#raising-exceptions]
note: Begin with this objective: Read environment-variable configuration with os.environ.
note: Keep the example in the Environment values tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.random_vs_secrets, python.regular_expressions, python.sys_runtime_interface.
note: Require security.secrets_handling_basics before this consuming unit; do not introduce a general secrets-handling curriculum here.
PRACTICE ANCHOR (live_code): Read a nonsecret output-directory setting stored under ORDER_SOURCE with os.environ.get, and report its absence explicitly.  SUCCESS: When ORDER_SOURCE is configured, the program retrieves its string value. When it is absent, the program reports missing configuration instead of using an unintended directory.
ASSESSMENT ANCHOR: retrieve_configured_environment_string facts=['f1', 'f2']
ASSESSMENT ANCHOR: provide_fallback_for_absent_optional_setting facts=['f2']
ASSESSMENT ANCHOR: detect_and_report_missing_required_configuration facts=['f2', 'f3']
ASSESSMENT ANCHOR: recognize_missing_key_error_from_bracket_lookup facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Choosing random or secrets for randomness; Creating isolated virtual environments; Development checks with the Python assert statement; Generator expressions; Generator functions with yield; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Matching text patterns with re; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Selecting the project environment interpreter; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Accessing environment variables with os.environ
Explore — 
(mechanism) os.environ maps process environment names to string values. Configuration arrives as text. ⟦A.f1 A:tb2 A:tb4 A:tb1⟧
(mechanism) os.environ.get("SETTING", fallback) returns the configured string or, if absent, the fallback. Without a fallback, absence returns None. An absent name is not the same as a configured empty string. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) For required configuration, check absence explicitly or use bracket lookup, which raises KeyError for a missing key. Report missing configuration instead of proceeding with an unintended value. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
[CODE python]
import os
label = os.environ.get("ORDER_LABEL", "notebook")
required = os.environ.get("ORDER_SOURCE")
print(label)
if required is None:
    print("Missing ORDER_SOURCE configuration")
else:
    print(required)

  annotations: ['Optional fallback versus required configuration.', 'Check None explicitly for absence.', 'Display the configured string when ORDER_SOURCE is present.']
[DIAGRAM: ORDER_SOURCE environment states] nodes=['os.environ.get("ORDER_SOURCE")', 'ORDER_SOURCE present → retrieved string → absence check is false', 'ORDER_SOURCE absent → None → report missing configuration'] edges=[('n1', 'n2', 'present'), ('n1', 'n3', 'absent')] alt: ORDER_SOURCE environment states: os.environ.get("ORDER_SOURCE"); ORDER_SOURCE present → retrieved string → absence check is false; ORDER_SOURCE absent → None → report missing configuration

### s02 · check · Check: provide fallback for absent optional setting
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] ORDER_LABEL is optional and may be absent. Which expression supplies notebook only when the key is absent?
  ✔ correct: os.environ.get("ORDER_LABEL", "notebook")
      why: Correct. os.environ.get("ORDER_LABEL", "notebook")
  ✘ trap1: os.environ["ORDER_LABEL"]
      why: Bracket lookup raises KeyError when the key is absent; it does not provide this fallback.
  ✘ trap2: os.environ.get("ORDER_LABEL")
      why: Without a fallback argument, get returns None on absence, not notebook.
  feedback✔: Correct. os.environ.get("ORDER_LABEL", "notebook")  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Compare optional configuration with required configuration.']  remediation→r01
  MEASURES: A:provide_fallback_for_absent_optional_setting(f2)   anchors=['assessment:provide_fallback_for_absent_optional_setting']
  taught-before-tested: A.f2←s01

### s03 · check · Check: recognize missing key error from bracket lookup
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] ORDER_SOURCE is absent. What does os.environ["ORDER_SOURCE"] do?
  ✔ correct: It raises KeyError.
      why: Correct. It raises KeyError.
  ✘ trap1: It returns None.
      why: None on absence is the behavior of get without a fallback, not bracket lookup.
  ✘ trap2: It returns a default directory automatically.
      why: Bracket lookup does not supply a default for a missing key.
  feedback✔: Correct. It raises KeyError.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['The two lookup forms differ on absence.']
  MEASURES: A:recognize_missing_key_error_from_bracket_lookup(f3)   anchors=['assessment:recognize_missing_key_error_from_bracket_lookup']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Practise accessing environment variables with os.environ
Practice — Read a nonsecret output-directory setting stored under ORDER_SOURCE with os.environ.get, and report its absence explicitly.
QUESTION [code_exercise, stretch, grading=client] The fixed scaffold retrieves ORDER_SOURCE with os.environ.get and supplies the value as supplied_required. Assign required from supplied_required before the fixed explicit None check, then print required after that check. Keep the retrieval, absence check and environment adapter unchanged. A configured value must be displayed as a string, absence must display Missing ORDER_SOURCE configuration, and a configured empty string must remain empty.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import os', 'variable assignment', 'string literals', 'os.environ.get(name)', 'os.environ.get(name, fallback)', 'is None', 'if/else', 'print()'] blocked=12 items
  file main.py [editable]:
configured_source = 'orders'
if True:  # Fixed scaffold; leave this block unchanged.
    # Fixed adapter supplies process configuration and tests separate environment cases.
    import os, pathlib as _pathlib, io as _io, contextlib as _contextlib
    os.environ['ORDER_SOURCE'] = configured_source
# LEARNER SECTION
if True:  # Fixed retrieval and explicit absence handling; leave unchanged.
    supplied_message = "Missing ORDER_SOURCE configuration"
    supplied_required = os.environ.get("ORDER_SOURCE")
required = None
if required is None:  # Fixed explicit absence check; leave unchanged.
    required = supplied_message
# Print required after the fixed absence check.
# END LEARNER
if True:  # Fixed scaffold; leave this block unchanged.
    
    def environment_case(value):
        code = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\n',1)[1].split('# END LEARNER',1)[0]
        previous = os.environ.get('ORDER_SOURCE')
        if value is None:
            os.environ.pop('ORDER_SOURCE', None)
        else:
            os.environ['ORDER_SOURCE'] = value
        out = _io.StringIO()
        try:
            with _contextlib.redirect_stdout(out):
                exec(code, {'__name__': '__main__', 'os': os})
            return out.getvalue().strip()
        finally:
            if previous is None:
                os.environ.pop('ORDER_SOURCE', None)
            else:
                os.environ['ORDER_SOURCE'] = previous

  SOLUTION main.py:
configured_source = 'orders'
if True:  # Fixed scaffold; leave this block unchanged.
    # Fixed adapter supplies process configuration and tests separate environment cases.
    import os, pathlib as _pathlib, io as _io, contextlib as _contextlib
    os.environ['ORDER_SOURCE'] = configured_source
# LEARNER SECTION
if True:  # Fixed retrieval and explicit absence handling; leave unchanged.
    supplied_message = "Missing ORDER_SOURCE configuration"
    supplied_required = os.environ.get("ORDER_SOURCE")
required = supplied_required
if required is None:  # Fixed explicit absence check; leave unchanged.
    required = supplied_message
print(required)
# END LEARNER
if True:  # Fixed scaffold; leave this block unchanged.
    
    def environment_case(value):
        code = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\n',1)[1].split('# END LEARNER',1)[0]
        previous = os.environ.get('ORDER_SOURCE')
        if value is None:
            os.environ.pop('ORDER_SOURCE', None)
        else:
            os.environ['ORDER_SOURCE'] = value
        out = _io.StringIO()
        try:
            with _contextlib.redirect_stdout(out):
                exec(code, {'__name__': '__main__', 'os': os})
            return out.getvalue().strip()
        finally:
            if previous is None:
                os.environ.pop('ORDER_SOURCE', None)
            else:
                os.environ['ORDER_SOURCE'] = previous

  test test1 (stdout_equals, visible=True): {"expected":"orders\n"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test2 (function_call, visible=True): {"function":"environment_case","args":["orders"],"expected":"orders"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test3 (function_call, visible=True): {"function":"environment_case","args":[null],"expected":"Missing ORDER_SOURCE configuration"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  test test4 (function_call, visible=True): {"function":"environment_case","args":[""],"expected":""} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"0ff18fbd64589c97167bf62fc0a2a83e91962c24c156de3940f40444a7a7cbc4","tests_passed":4}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: A:retrieve_configured_environment_string(f1,f2); A:detect_and_report_missing_required_configuration(f2,f3)   anchors=['practice', 'assessment:retrieve_configured_environment_string', 'assessment:detect_and_report_missing_required_configuration']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01

### s05 · recap · Keep these ideas
Recap — 
(takeaway) Environment values are strings. Distinguish absence, optional fallbacks and required configuration. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Choosing random or secrets for randomness: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Accessing environment variables with os.environ
(mechanism) os.environ.get("SETTING", fallback) returns the configured string or, if absent, the fallback. Without a fallback, absence returns None. An absent name is not the same as a configured empty string. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an absent ORDER_SOURCE with a configured empty string. Test absence explicitly for a required setting. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Accessing environment variables with os.environ
(mechanism) For required configuration, check absence explicitly or use bracket lookup, which raises KeyError for a missing key. Report missing configuration instead of proceeding with an unintended value. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an absent ORDER_SOURCE with a configured empty string. Test absence explicitly for a required setting. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Accessing environment variables with os.environ
(mechanism) os.environ maps process environment names to string values. Configuration arrives as text. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) os.environ.get("SETTING", fallback) returns the configured string or, if absent, the fallback. Without a fallback, absence returns None. An absent name is not the same as a configured empty string. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) For required configuration, check absence explicitly or use bracket lookup, which raises KeyError for a missing key. Report missing configuration instead of proceeding with an unintended value. ⟦A.f3 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast an absent ORDER_SOURCE with a configured empty string. Test absence explicitly for a required setting. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

=========

# EVALUATOR PACKET — Choosing random or secrets for randomness (learn_python.tile.092_092)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.random_vs_secrets — Choosing random or secrets for randomness

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.092_092.r02 is never referenced
  warn: remediation step learn_python.tile.092_092.r03 is never referenced
  warn: learn_python.tile.092_092.s05/ix.learn_python.tile.092_092.s05: ADVISORY — syntax descriptors with no detector: ['<', '==', '>=', 'assert', 'generator expressions', 'integer and floating-point literals', 'list literals', 'yield', 'yield from']

## SOURCE FACTS — A (python.random_vs_secrets)   objective: Choose random or secrets according to the use of randomness.
A.f1: random is designed for modelling and simulation, while secrets provides cryptographically strong randomness for security-sensitive values.   [sources: python_stdlib_reference#secrets.html#module-secrets]
A.f2: random.seed(seed) initializes the pseudo-random generator; reuse a seed to reproduce a sequence under the documented reproducibility conditions.   [sources: python_stdlib_reference#random.html#random.seed]
A.f3: random.random() returns a floating-point value in the half-open interval from 0.0 to 1.0.   [sources: python_stdlib_reference#random.html#random.random]
A.f4: secrets.token_hex(nbytes) generates a random hexadecimal token for security-sensitive use.   [sources: python_stdlib_reference#secrets.html#secrets.token_hex]
note: Begin with this objective: Choose random or secrets according to the use of randomness.
note: Keep the example in the Randomness and security-sensitive choices tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.regular_expressions, python.sys_runtime_interface, python.virtual_environments.
note: Require security.secrets_handling_basics before this consuming unit; do not introduce a general secrets-handling curriculum here.
PRACTICE ANCHOR (live_code): Use random.seed(7) and random.random() to generate a short sequence of simulation values, then reset the same seed and repeat the calls to demonstrate reproducibility.  SUCCESS: The two sequences match in the same execution environment with no intervening random calls, and each value is at least 0.0 and less than 1.0.
ASSESSMENT ANCHOR: select_seeded_random_for_reproducible_simulation facts=['f1', 'f2']
ASSESSMENT ANCHOR: select_secrets_for_security_sensitive_tokens facts=['f1', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Creating isolated virtual environments; Development checks with the Python assert statement; Generator expressions; Generator functions with yield; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Matching text patterns with re; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Selecting the project environment interpreter; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Choosing random or secrets for randomness
Explore — 
(mechanism) Use random for modelling and simulation. Use secrets for cryptographically strong randomness in security-sensitive values; seeded simulation output is not a substitute. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb1⟧
(mechanism) random.seed(seed) initializes the pseudo-random generator. Reusing a seed reproduces a sequence under the documented reproducibility conditions, not a guarantee across every environment. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) random.random() returns a floating-point value from 0.0 inclusive to 1.0 exclusive. ⟦A.f3 A:tb3 A:tb4⟧
(mechanism) secrets.token_hex(nbytes) generates a random hexadecimal token for security-sensitive use. Choose the module from the requirement, not convenience. ⟦A.f4 A:tb3 A:tb4⟧
[CODE python]
import random
random.seed(7)
first = [random.random(), random.random()]
random.seed(7)
second = [random.random(), random.random()]
print(first)
print(second)
print(first == second)
import secrets
print(secrets.token_hex(16))

  annotations: ['Reset the seed and compare repeated simulation calls.', 'Use secrets for a security-sensitive token.', 'random.random(): 0.0 included; 1.0 excluded', 'random.random(): 0.0 included; 1.0 excluded']

### s02 · video · Choosing random or secrets for randomness
Demonstration — 
[VIDEO Choosing randomness for simulation] bridge-before: Watch for the distinction between ordinary random data and security-sensitive values, then follow the random.random() example: its lower bound is included and its upper bound is excluded. | bridge-after: The clip explains the interval and recommends secrets for security. The text additionally teaches cryptographic strength, seeding with documented reproducibility conditions, and generating security-sensitive hexadecimal tokens with secrets.token_hex(nbytes).
  - KzqSDvzOFNA 0-102s facts=['f3'] label: Using random.random() and understanding its bounds | summary: The random module is suitable for dummy data and games, but not for security-sensitive randomness; secrets is recommended for that purpose. After importing random, assigning random.random() to a variable produces a floating-point value that can equal 0.0 but cannot equal 1.0. Repeated runs demonstrate generating values within those bounds.

### s03 · check · Check: select seeded random for reproducible simulation
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] A simulation needs a repeatable pseudo-random sequence in the same execution environment, with no intervening random calls. Which approach fits?
  ✔ correct: Use random.seed(7), generate the sequence, reset that seed, and repeat the calls.
      why: Correct. Use random.seed(7), generate the sequence, reset that seed, and repeat the calls.
  ✘ trap1: Use secrets.token_hex(16) as a seeded simulation sequence.
      why: secrets supplies security-sensitive randomness, not this seeded random simulation workflow.
  ✘ trap2: Call random.random() again without resetting the seed and assume the sequence restarts.
      why: Reproducing the taught sequence requires resetting the seed before repeating the calls.
  feedback✔: Correct. Use random.seed(7), generate the sequence, reset that seed, and repeat the calls.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Separate reproducible modelling from security-sensitive randomness.']  remediation→r01
  MEASURES: A:select_seeded_random_for_reproducible_simulation(f1,f2)   anchors=['assessment:select_seeded_random_for_reproducible_simulation']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · check · Check: select secrets for security sensitive tokens
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] Which taught operation fits a security-sensitive random hexadecimal token?
  ✔ correct: secrets.token_hex(16)
      why: Correct. secrets.token_hex(16)
  ✘ trap1: random.seed(7) followed by random.random()
      why: The seeded simulation generator is not the taught cryptographically strong token source.
  ✘ trap2: Reuse the same seeded simulation sequence as the token.
      why: Reproducible modelling behavior is not the security-sensitive randomness supplied by secrets.
  feedback✔: Correct. secrets.token_hex(16)  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Choose based on the purpose of the randomness.']
  MEASURES: A:select_secrets_for_security_sensitive_tokens(f1,f4)   anchors=['assessment:select_secrets_for_security_sensitive_tokens']
  taught-before-tested: A.f1←s01; A.f4←s01

### s05 · hands_on · Practise choosing random or secrets for randomness
Practice — Use random.seed(7) and random.random() to generate a short sequence of simulation values, then reset the same seed and repeat the calls to demonstrate reproducibility.
QUESTION [code_exercise, intro, grading=client] The fixed skeleton seeds random, draws two values, resets the same seed, and repeats those draws. Complete seed = initial_seed (the supplied seed is 7), preserving the skeleton without intervening calls. Print first, second, matching, and in_bounds in that order, one per line. The displayed sequences must match and every value must be >= 0.0 and < 1.0.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import random', 'random.seed(7)', 'random.random()', 'variable assignment', 'integer and floating-point literals', 'list literals', '==', '<', '>=', 'and', 'print()'] blocked=12 items
  file main.py [editable]:
initial_seed = 7
seed = None
# Choose the supplied seed.
if True:  # Fixed scaffold; leave this block unchanged.
    import random
    random.seed(seed)
    a = random.random()
    b = random.random()
    first = [a, b]
    random.seed(seed)
    c = random.random()
    d = random.random()
    second = [c, d]
    matching = first == second
    in_bounds = a >= 0.0 and a < 1.0 and b >= 0.0 and b < 1.0 and c >= 0.0 and c < 1.0 and d >= 0.0 and d < 1.0
# Display the two sequences and checks.

  SOLUTION main.py:
initial_seed = 7
seed = initial_seed
if True:  # Fixed scaffold; leave this block unchanged.
    import random
    random.seed(seed)
    a = random.random()
    b = random.random()
    first = [a, b]
    random.seed(seed)
    c = random.random()
    d = random.random()
    second = [c, d]
    matching = first == second
    in_bounds = a >= 0.0 and a < 1.0 and b >= 0.0 and b < 1.0 and c >= 0.0 and c < 1.0 and d >= 0.0 and d < 1.0
print(first)
print(second)
print(matching)
print(in_bounds)

  test test1 (stdout_equals, visible=True): {"expected":"[0.32383276483316237, 0.15084917392450192]\n[0.32383276483316237, 0.15084917392450192]\nTrue\nTrue\n"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"b0ee01b1ff2b8c5a08e8a2c0aa58e8673fc48e8ab3c03f27266606592e773f1b","tests_passed":1}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Print the two stored sequences first, then their equality and bounds checks.']
  MEASURES: A:select_seeded_random_for_reproducible_simulation(f1,f2)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01

### s06 · recap · Keep these ideas
Recap — 
(takeaway) Separate simulation randomness from security-sensitive randomness; preserve reproducibility limits and value bounds. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Matching text patterns with re: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Choosing random or secrets for randomness
(mechanism) Use random for modelling and simulation. Use secrets for cryptographically strong randomness in security-sensitive values; seeded simulation output is not a substitute. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) random.seed(seed) initializes the pseudo-random generator. Reusing a seed reproduces a sequence under the documented reproducibility conditions, not a guarantee across every environment. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast reproducible simulation with a security-sensitive token. A seeded simulation is not a security recipe. ⟦A.f1 A.f2 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Choosing random or secrets for randomness
(mechanism) Use random for modelling and simulation. Use secrets for cryptographically strong randomness in security-sensitive values; seeded simulation output is not a substitute. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) secrets.token_hex(nbytes) generates a random hexadecimal token for security-sensitive use. Choose the module from the requirement, not convenience. ⟦A.f4 A:tb3 A:tb4⟧
(misconception) Contrast reproducible simulation with a security-sensitive token. A seeded simulation is not a security recipe. ⟦A.f1 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Choosing random or secrets for randomness
(mechanism) Use random for modelling and simulation. Use secrets for cryptographically strong randomness in security-sensitive values; seeded simulation output is not a substitute. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) random.seed(seed) initializes the pseudo-random generator. Reusing a seed reproduces a sequence under the documented reproducibility conditions, not a guarantee across every environment. ⟦A.f2 A:tb3 A:tb4 A:tb5⟧
(mechanism) secrets.token_hex(nbytes) generates a random hexadecimal token for security-sensitive use. Choose the module from the requirement, not convenience. ⟦A.f4 A:tb3 A:tb4⟧
(mechanism) random.random() returns a floating-point value from 0.0 inclusive to 1.0 exclusive. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast reproducible simulation with a security-sensitive token. A seeded simulation is not a security recipe. ⟦A.f1 A.f2 A.f4 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expected: [0.32383276483316237, 0.15084917392450192]
[0.32383276483316237, 0.15084917392450192]
True
True

· expected.value: [0.10682853770165568, 0.7025855239868555]
[0.10682853770165568, 0.7025855239868555]
True
True

=========

# EVALUATOR PACKET — Matching text patterns with re (learn_python.tile.093_093)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.regular_expressions — Matching text patterns with re

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.093_093.r02 is never referenced
  warn: learn_python.tile.093_093.s04/ix.learn_python.tile.093_093.s04: ADVISORY — syntax descriptors with no detector: ['*', '[A-Z]', 'assert', 'concatenated pattern elements', 'for loops', 'generator expressions', 'is not None', 'list literals', 'raw string literals', 'string literals', 'yield', 'yield from']

## SOURCE FACTS — A (python.regular_expressions)   objective: Recognize simple text patterns using re.
A.f1: A regular expression describes a text pattern; [...] selects one character from a set, ranges such as A-Z select a range, and * allows zero or more repetitions.   [sources: python_stdlib_reference#re.html#regular-expression-syntax]
A.f2: Concatenated pattern elements match in sequence; a raw string literal such as r"..." avoids Python string-escape processing of pattern backslashes.   [sources: python_stdlib_reference#re.html#regular-expression-syntax]
A.f3: re.fullmatch(pattern, text) returns a Match if the whole text matches and None otherwise; test is not None for successful validation.   [sources: python_stdlib_reference#re.html#re.fullmatch]
A.f4: re.match checks at the beginning, while re.search looks for a match anywhere; neither requires the entire text to match.   [sources: python_stdlib_reference#re.html#re.match, python_stdlib_reference#re.html#re.search]
note: Begin with this objective: Recognize simple text patterns using re.
note: Keep the example in the Regular expressions tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.sys_runtime_interface, python.virtual_environments, python.environment_interpreter_selection.
PRACTICE ANCHOR (live_code): Validate a nonempty uppercase-letter label using a simple pattern, re.fullmatch, and an explicit is not None success test.  SUCCESS: The validation accepts BLUE and a single uppercase letter, and rejects Blue, BLUE!, and an empty string.
ASSESSMENT ANCHOR: choose_pattern_for_label_requirement facts=['f1', 'f2']
ASSESSMENT ANCHOR: choose_whole_text_validation_operation facts=['f3', 'f4']
ASSESSMENT ANCHOR: interpret_validation_result facts=['f3']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Creating isolated virtual environments; Development checks with the Python assert statement; Generator expressions; Generator functions with yield; Inspecting interpreter runtime information with sys; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Selecting the project environment interpreter; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Matching text patterns with re
Explore — 
(mechanism) A regular expression describes a text pattern. [...] selects one character from a set; A-Z is a range; * permits zero or more repetitions. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) Concatenated elements match in sequence. A raw literal such as r"..." avoids Python string-escape processing of pattern backslashes. ⟦A.f2 A:tb3⟧
(mechanism) re.fullmatch(pattern, text) returns a Match for a whole-text match and None otherwise. Test is not None for success. ⟦A.f3 A:tb1 A:tb3⟧
(mechanism) re.match checks the beginning; re.search looks anywhere. Neither requires the entire text to match, so a matching prefix or substring does not establish whole-label validity. ⟦A.f4 A:tb3⟧
[CODE python]
import re
pattern = r"[A-Z][A-Z]*"
for label in ["BLUE", "Blue", "BLUE!"]:
    accepted = re.fullmatch(pattern, label) is not None
    print(label, accepted)

  annotations: ['First character required; later characters may repeat.', 'Whole-text match with an explicit success test.']

### s02 · explainer · Matching text patterns with re
Explore — 
(mechanism) A matching prefix is not whole-label validation. re.fullmatch checks the complete label; re.match checks its beginning, and re.search looks anywhere. ⟦A.f3 A.f4 A:tb4 A:tb5⟧

### s03 · check · Check: choose whole text validation operation
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] The requirement is to validate an entire label, not just find an uppercase substring. Which operation matches that scope?
  ✔ correct: re.fullmatch(pattern, label)
      why: Correct. re.fullmatch(pattern, label)
  ✘ trap1: re.search(pattern, label)
      why: search can find a match anywhere without requiring the whole text to match.
  ✘ trap2: re.match(pattern, label)
      why: match checks the beginning rather than imposing the whole-text requirement.
  feedback✔: Correct. re.fullmatch(pattern, label)  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Distinguish whole-text validation from locating a match.']  remediation→r01
  MEASURES: A:choose_whole_text_validation_operation(f3,f4)   anchors=['assessment:choose_whole_text_validation_operation']
  taught-before-tested: A.f3←s01; A.f4←s01

### s04 · hands_on · Practise matching text patterns with re
Practice — Validate a nonempty uppercase-letter label using a simple pattern, re.fullmatch, and an explicit is not None success test.
QUESTION [code_exercise, core, grading=client] Choose the supplied pattern that requires at least one uppercase letter: complete pattern = nonempty_uppercase or pattern = possibly_empty_uppercase as appropriate. The fixed loop uses re.fullmatch and is not None, printing label and accepted for each supplied label. It must accept BLUE and A and reject Blue, BLUE!, and empty text. Leave the input list and validation loop unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import re', 'variable assignment', 'string literals', 'raw string literals', 'list literals', 'for loops', 'print()', 're.fullmatch(pattern, label)', 'is not None', '[A-Z]', '*', 'concatenated pattern elements'] blocked=11 items
  file main.py [editable]:
first_label = 'BLUE'
if True:  # Fixed scaffold; leave this block unchanged.
    import re
    labels = [first_label, 'A', 'Blue', 'BLUE!', '']
    nonempty_uppercase = r'[A-Z][A-Z]*'
    possibly_empty_uppercase = r'[A-Z]*'
pattern = None
if True:  # Fixed scaffold; leave this block unchanged.
    for label in labels:
        accepted = re.fullmatch(pattern, label) is not None
        print(label, accepted)

  SOLUTION main.py:
first_label = 'BLUE'
if True:  # Fixed scaffold; leave this block unchanged.
    import re
    labels = [first_label, 'A', 'Blue', 'BLUE!', '']
    nonempty_uppercase = r'[A-Z][A-Z]*'
    possibly_empty_uppercase = r'[A-Z]*'
pattern = nonempty_uppercase
if True:  # Fixed scaffold; leave this block unchanged.
    for label in labels:
        accepted = re.fullmatch(pattern, label) is not None
        print(label, accepted)

  test test1 (stdout_equals, visible=True): {"expected":"BLUE True\nA True\nBlue False\nBLUE! False\n False\n"} | on-fail: The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"a95acce0a5b08bce090adfda259f7ee6c9d9163dc0396a8113244086aa468cf1","tests_passed":1}
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['The first [A-Z] requires one character; the following [A-Z]* permits any additional uppercase letters.']
  MEASURES: A:choose_pattern_for_label_requirement(f1,f2); A:interpret_validation_result(f3)   anchors=['practice', 'assessment:choose_pattern_for_label_requirement', 'assessment:interpret_validation_result']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · recap · Keep these ideas
Recap — 
(takeaway) Validate complete labels with fullmatch and an explicit success test, not just a prefix or substring. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Next: Inspecting interpreter runtime information with sys: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Matching text patterns with re
(mechanism) re.fullmatch(pattern, text) returns a Match for a whole-text match and None otherwise. Test is not None for success. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(mechanism) re.match checks the beginning; re.search looks anywhere. Neither requires the entire text to match, so a matching prefix or substring does not establish whole-label validity. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a whole-label check with a prefix check. Use the registered labels with fullmatch, not just match. ⟦A.f3 A.f4 A:tb1 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Matching text patterns with re
(mechanism) A regular expression describes a text pattern. [...] selects one character from a set; A-Z is a range; * permits zero or more repetitions. ⟦A.f1 A:tb1 A:tb2 A:tb4⟧
(mechanism) Concatenated elements match in sequence. A raw literal such as r"..." avoids Python string-escape processing of pattern backslashes. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) re.fullmatch(pattern, text) returns a Match for a whole-text match and None otherwise. Test is not None for success. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast a whole-label check with a prefix check. Use the registered labels with fullmatch, not just match. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· spec.expected: BLUE True
A True
Blue False
BLUE! False
 False

· expected.value: BLUE_x False
A True
Blue False
BLUE! False
 False

=========

# EVALUATOR PACKET — Inspecting interpreter runtime information with sys · Creating isolated virtual environments · Selecting the project environment interpreter (learn_python.tile.094_096)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.sys_runtime_interface — Inspecting interpreter runtime information with sys
B = python.virtual_environments — Creating isolated virtual environments
C = python.environment_interpreter_selection — Selecting the project environment interpreter

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: remediation step learn_python.tile.094_096.r02 is never referenced
  warn: remediation step learn_python.tile.094_096.r05 is never referenced
  warn: remediation step learn_python.tile.094_096.r06 is never referenced

## SOURCE FACTS — A (python.sys_runtime_interface)   objective: Inspect interpreter runtime information using sys.
A.f1: sys.executable gives the running interpreter’s executable path when available; it may be an empty string or None if Python cannot retrieve it.   [sources: python_stdlib_reference#sys.html#sys.executable]
A.f2: sys.version gives the interpreter version plus build and compiler information.   [sources: python_stdlib_reference#sys.html#sys.version]
A.f3: After import sys, print(sys.executable) and print(sys.version) display which runtime is actually executing the code.   [sources: python_stdlib_reference#functions.html#print, python_stdlib_reference#sys.html#sys.executable, python_stdlib_reference#sys.html#sys.version]
note: Begin with this objective: Inspect interpreter runtime information using sys.
note: Keep the example in the Runtime and isolated interpreter selection tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.virtual_environments, python.environment_interpreter_selection, python.pip_installation.
PRACTICE ANCHOR (live_code): Print a compact runtime diagnostic showing the running interpreter's executable and version information.  SUCCESS: The code imports sys and prints sys.executable and sys.version, preserving the actual executable value even when it is an empty string or None.
ASSESSMENT ANCHOR: identify_running_interpreter_executable facts=['f1', 'f3']
ASSESSMENT ANCHOR: identify_running_interpreter_version_and_build facts=['f2', 'f3']

## SOURCE FACTS — B (python.virtual_environments)   objective: Create and use an isolated Python virtual environment.
B.f1: Run the selected Python executable with -m venv .venv to create a project environment, containing bin/python on POSIX or Scripts/python.exe on Windows.   [sources: python_stdlib_reference#venv.html#creating-virtual-environments]
B.f2: Activation changes command lookup to the environment’s executable, but activation is not required when invoking that executable by its full path.   [sources: python_stdlib_reference#venv.html#how-venvs-work]
B.f3: sys.prefix != sys.base_prefix identifies an interpreter running in a virtual environment.   [sources: python_stdlib_reference#venv.html#how-venvs-work]
B.f4: Run the environment’s Python with -m pip list to inspect its installed packages.   [sources: python_tutorial#venv.html#managing-packages-with-pip]
B.f5: Virtual environments are isolated from base-environment packages by default.   [sources: python_stdlib_reference#venv.html#module-venv]
note: Begin with this objective: Create and use an isolated Python virtual environment.
note: Keep the example in the Runtime and isolated interpreter selection tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.environment_interpreter_selection, python.pip_installation, python.requirements_files.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
note: Require linux.shell_pipes_and_redirection before shell-dependent environment work; commands here teach Python invocation, not shell fundamentals.
PRACTICE ANCHOR (live_code): Create a project .venv with the selected Python executable, invoke the environment's interpreter explicitly, inspect its runtime prefixes, and list its installed packages.  SUCCESS: The project environment exists, its explicitly invoked interpreter reports sys.prefix != sys.base_prefix as True, and its Python successfully runs -m pip list.
ASSESSMENT ANCHOR: create_project_virtual_environment facts=['f1']
ASSESSMENT ANCHOR: verify_environment_interpreter_use facts=['f1', 'f2', 'f3']

## SOURCE FACTS — C (python.environment_interpreter_selection)   objective: Select and verify the interpreter used for a Python project.
C.f1: Inspect sys.executable in the executed program to identify its actual interpreter, rather than relying on an environment label.   [sources: python_stdlib_reference#sys.html#sys.executable]
C.f2: A venv supplies its interpreter at bin/python on POSIX or Scripts/python.exe on Windows.   [sources: python_stdlib_reference#venv.html#creating-virtual-environments]
C.f3: Configure an execution tool to invoke the intended venv executable explicitly when command lookup selects the wrong Python; activation is not required for explicit executable invocation.   [sources: python_stdlib_reference#venv.html#how-venvs-work]
C.f4: Check sys.prefix != sys.base_prefix and the executable path again after changing the selected runtime.   [sources: python_stdlib_reference#venv.html#how-venvs-work]
note: Begin with this objective: Select and verify the interpreter used for a Python project.
note: Keep the example in the Runtime and isolated interpreter selection tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.pip_installation, python.requirements_files, python.assert_statement.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
note: Require linux.shell_pipes_and_redirection before shell-dependent environment work; commands here teach Python invocation, not shell fundamentals.
PRACTICE ANCHOR (live_code): Correct an editor configuration that runs the project with system Python by selecting the intended venv executable, then rerun a diagnostic program to verify the change.  SUCCESS: The editor invokes the intended venv executable explicitly. The rerun reports that executable through sys.executable and reports True for sys.prefix != sys.base_prefix.
ASSESSMENT ANCHOR: diagnose_actual_interpreter_from_runtime_path facts=['f1']
ASSESSMENT ANCHOR: select_explicit_project_venv_executable facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_interpreter_selection_after_rerun facts=['f1', 'f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Creating isolated virtual environments; Development checks with the Python assert statement; Generator expressions; Generator functions with yield; Installing dependencies with python -m pip; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Selecting the project environment interpreter; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Inspecting interpreter runtime information with sys
Explore — 
(mechanism) sys.executable identifies the running interpreter’s executable path when available. It may be an empty string or None if Python cannot retrieve it; do not invent a path. ⟦A.f1 A:tb2 A:tb4 A:tb5 A:tb1⟧
(mechanism) sys.version includes the interpreter version plus build and compiler information. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) After import sys, print(sys.executable) and print(sys.version) display the actual executing runtime. Compare these observations with the interpreter you intended, rather than relying only on a tool label. ⟦A.f3 A:tb3 A:tb4⟧
[CODE python]
import sys
print(sys.executable)
print(sys.version)

  annotations: ['Observe the actual process, not a tool label.']

### s02 · check · Check: identify running interpreter version and build
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] Which runtime field provides interpreter version, build, and compiler information?
  ✔ correct: sys.version
      why: Correct. sys.version
  ✘ trap1: sys.executable
      why: executable identifies the executable path when available, not version/build information.
  ✘ trap2: A hard-coded project version string
      why: A fixed string is not an observation of the executing interpreter.
  feedback✔: Correct. sys.version  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Match the diagnostic field to the information requested.']  remediation→r01
  MEASURES: A:identify_running_interpreter_version_and_build(f2,f3)   anchors=['assessment:identify_running_interpreter_version_and_build']
  taught-before-tested: A.f2←s01; A.f3←s01

### s03 · hands_on · Review inspecting interpreter runtime information with sys
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.
QUESTION [classify, core, grading=client] Read each diagnostic implementation. Decide whether it displays the actual executable followed by actual version, preserving empty or None executable values.
  'import sys
print(sys.executable)
print(sys.version)' -> Meets the stated criterion
      feedback: Both fields come directly from the running interpreter.
  'import sys
print(sys.executable or "/project/.venv/bin/python")
print(sys.version)' -> Does not meet the stated criterion
      feedback: The fallback fabricates an executable path when the actual value is empty or None.
  'print("/project/.venv/bin/python")
print("Python 3.13")' -> Does not meet the stated criterion
      feedback: Hard-coded text is not the executing runtime's diagnostic values.
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: A:identify_running_interpreter_executable(f1,f3); A:identify_running_interpreter_version_and_build(f2,f3)   anchors=['practice', 'assessment:identify_running_interpreter_executable', 'assessment:identify_running_interpreter_version_and_build']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01; A.f3←s01

### s04 · explainer · Creating isolated virtual environments
Explore — 
(mechanism) Use the selected Python executable with -m venv .venv to create a project environment. Its interpreter is bin/python on POSIX or Scripts/python.exe on Windows. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) Activation changes command lookup to the environment executable. It is not required when invoking that executable by its full path. ⟦B.f2 B:tb3⟧
(mechanism) sys.prefix != sys.base_prefix identifies an interpreter running in a virtual environment. ⟦B.f3 B:tb3⟧
(mechanism) Inspect installed packages using the environment’s Python with -m pip list. ⟦B.f4 B:tb3⟧
(mechanism) Virtual environments are isolated from base-environment packages by default; do not assume the base package list applies. ⟦B.f5 B:tb1 B:tb3⟧
[DIAGRAM: Environment executable and inspection] nodes=['Selected Python: -m venv .venv', '.venv/bin/python (POSIX)', '.venv/Scripts/python.exe (Windows)', 'Explicit full-path invocation: activation not required', 'Inspect sys.prefix != sys.base_prefix', 'Environment Python: -m pip list'] edges=[('n1', 'n2', 'POSIX'), ('n1', 'n3', 'Windows'), ('n2', 'n4', 'explicit invocation'), ('n3', 'n4', 'explicit invocation'), ('n4', 'n5', 'identify environment'), ('n4', 'n6', 'inspect packages')] alt: Environment executable and inspection: Selected Python: -m venv .venv; .venv/bin/python (POSIX); .venv/Scripts/python.exe (Windows); Explicit full-path invocation: activation not required; Inspect sys.prefix != sys.base_prefix; Environment Python: -m pip list

### s05 · explainer · Creating isolated virtual environments
Explore — 
(mechanism) Activation changes command lookup, but explicit executable invocation does not require activation. Check sys.prefix != sys.base_prefix and inspect packages through that environment’s Python. ⟦B.f2 B.f3 B.f4 B:tb4 B:tb5⟧

### s06 · check · Check: verify environment interpreter use
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] A process reports sys.prefix != sys.base_prefix as True. What does the taught diagnostic establish?
  ✔ correct: The interpreter is running in a virtual environment.
      why: Correct. The interpreter is running in a virtual environment.
  ✘ trap1: Every documented project import has already succeeded.
      why: The prefix comparison identifies a virtual environment, not import verification.
  ✘ trap2: Activation was necessarily performed before invocation.
      why: Explicit environment-executable invocation does not require activation.
  feedback✔: Correct. The interpreter is running in a virtual environment.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Separate environment identity from dependency checks.']  remediation→r03
  MEASURES: B:verify_environment_interpreter_use(f1,f2,f3)   anchors=['assessment:verify_environment_interpreter_use']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04

### s07 · hands_on · Review creating isolated virtual environments
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.
QUESTION [classify, core, grading=client] POSIX order-report project: /project. Selected base interpreter: /usr/bin/python3. Read each independent transcript and decide whether it proves creation and explicit use of the project venv, a True prefix comparison, and successful package listing.
  '/usr/bin/python3 -m venv .venv -> success
/project/.venv/bin/python diagnostic.py
sys.executable: /project/.venv/bin/python
sys.prefix != sys.base_prefix: True
/project/.venv/bin/python -m pip list -> success' -> Meets the stated criterion
      feedback: Creation, explicit venv execution, prefix comparison and listing all meet the criterion.
  '/usr/bin/python3 -m venv .venv -> success
/usr/bin/python3 diagnostic.py
sys.executable: /usr/bin/python3
sys.prefix != sys.base_prefix: False
/usr/bin/python3 -m pip list -> success' -> Does not meet the stated criterion
      feedback: The later commands use system Python, not the created environment.
  '/usr/bin/python3 -m venv .venv -> success
/project/.venv/bin/python diagnostic.py
sys.executable: /project/.venv/bin/python
sys.prefix != sys.base_prefix: True
No package listing was performed.' -> Does not meet the stated criterion
      feedback: The required package-listing evidence is missing.
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: B:create_project_virtual_environment(f1); B:verify_environment_interpreter_use(f1,f2,f3)   anchors=['practice', 'assessment:create_project_virtual_environment', 'assessment:verify_environment_interpreter_use']
  taught-before-tested: B.f1←s04; B.f1←s04; B.f2←s04; B.f3←s04

### s08 · explainer · Selecting the project environment interpreter
Explore — 
(mechanism) Inspect sys.executable in the executed program to identify its actual interpreter. An environment label is not the evidence for this check. ⟦C.f1 C:tb2 C:tb1⟧
(mechanism) A venv interpreter is at bin/python on POSIX or Scripts/python.exe on Windows. ⟦C.f2 C:tb3⟧
(mechanism) If command lookup selects the wrong Python, configure the tool to invoke the intended venv executable explicitly. Explicit invocation does not require activation. ⟦C.f3 C:tb3⟧
(mechanism) After changing the runtime, check the executable path and sys.prefix != sys.base_prefix again in the program that runs. Changing the displayed label is not the final check. ⟦C.f4 C:tb3⟧
[BEFORE_AFTER] Illustrative runtime states; exact executable paths depend on the environment.
  before:
[DIAGRAM: Before: system Python] nodes=['Editor executable selection: system Python', 'sys.executable: system-Python executable', 'sys.prefix != sys.base_prefix: False'] edges=[('n1', 'n2', 'executed program'), ('n2', 'n3', 'prefix comparison')] alt: Before: system Python: Editor executable selection: system Python; sys.executable: system-Python executable; sys.prefix != sys.base_prefix: False
  after:
[DIAGRAM: After: intended venv] nodes=['Editor executable selection: intended .venv/bin/python (POSIX) or .venv/Scripts/python.exe (Windows)', 'sys.executable: intended venv executable', 'sys.prefix != sys.base_prefix: True'] edges=[('n1', 'n2', 'executed program'), ('n2', 'n3', 'prefix comparison')] alt: After: intended venv: Editor executable selection: intended .venv/bin/python (POSIX) or .venv/Scripts/python.exe (Windows); sys.executable: intended venv executable; sys.prefix != sys.base_prefix: True

### s09 · explainer · Selecting the project environment interpreter
Explore — 
(mechanism) After selecting the intended executable, inspect sys.executable and sys.prefix != sys.base_prefix again in the executed program. A changed environment label alone is not verification. ⟦C.f1 C.f4 C:tb4 C:tb5⟧

### s10 · check · Check: diagnose actual interpreter from runtime path
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] An editor shows a .venv label, but the running program reports a system executable path. Which evidence should guide diagnosis?
  ✔ correct: The running process's sys.executable, compared with the intended environment executable.
      why: Correct. The running process's sys.executable, compared with the intended environment executable.
  ✘ trap1: The label alone proves the intended interpreter ran.
      why: An environment label is not the executed-process evidence used in this check.
  ✘ trap2: Assume any Python executable is the project venv executable.
      why: The actual path must match the intended platform-appropriate environment interpreter.
  feedback✔: Correct. The running process's sys.executable, compared with the intended environment executable.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Inspect the actual process, not only the selection label.']  remediation→r04
  MEASURES: C:diagnose_actual_interpreter_from_runtime_path(f1)   anchors=['assessment:diagnose_actual_interpreter_from_runtime_path']
  taught-before-tested: C.f1←s08

### s11 · check · Check: verify interpreter selection after rerun
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] After selecting the intended project venv executable in the editor, what is the taught verification?
  ✔ correct: Rerun and inspect sys.executable plus sys.prefix != sys.base_prefix.
      why: Correct. Rerun and inspect sys.executable plus sys.prefix != sys.base_prefix.
  ✘ trap1: Stop at changing the editor label without rerunning.
      why: Only a rerun reveals which executable the new process actually uses.
  ✘ trap2: Require activation even when the editor invokes the full environment executable path.
      why: Explicit executable invocation does not depend on activation.
  feedback✔: Correct. Rerun and inspect sys.executable plus sys.prefix != sys.base_prefix.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Check both process identity and virtual-environment status after the change.']
  MEASURES: C:verify_interpreter_selection_after_rerun(f1,f4)   anchors=['assessment:verify_interpreter_selection_after_rerun']
  taught-before-tested: C.f1←s08; C.f4←s08

### s12 · hands_on · Review selecting the project environment interpreter
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.
QUESTION [classify, stretch, grading=client] Read each editor-change and rerun excerpt. On POSIX the intended existing interpreter is /project/.venv/bin/python. Decide whether the change is verified by the actual rerun.
  'Editor executable = /project/.venv/bin/python
Rerun sys.executable = /project/.venv/bin/python
Rerun sys.prefix != sys.base_prefix = True' -> Meets the stated criterion
      feedback: The explicit selection and both rerun observations identify the intended venv.
  'Editor label = .venv
Rerun sys.executable = /usr/bin/python3
Rerun sys.prefix != sys.base_prefix = False' -> Does not meet the stated criterion
      feedback: The label does not override the system-runtime evidence.
  'Editor executable = /project/.venv/bin/python
No rerun has occurred.' -> Does not meet the stated criterion
      feedback: The selected executable has not been verified in a new process.
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: C:select_explicit_project_venv_executable(f2,f3)   anchors=['practice', 'assessment:select_explicit_project_venv_executable']
  taught-before-tested: C.f2←s08; C.f3←s08

### s13 · recap · Keep these ideas
Recap — 
(takeaway) Inspect the actual executable and version, preserving the executable-path availability limit. ⟦A.f1 A.f2 A.f3 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Use the environment executable, check prefixes and inspect its packages; activation is not required for explicit invocation. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Configure the intended executable and verify the executed process again. ⟦C.f1 C.f2 C.f3 C.f4 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Next: Installing dependencies with python -m pip: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Inspecting interpreter runtime information with sys
(mechanism) sys.version includes the interpreter version plus build and compiler information. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) After import sys, print(sys.executable) and print(sys.version) display the actual executing runtime. Compare these observations with the interpreter you intended, rather than relying only on a tool label. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast the selected tool label with observations from the running process. Preserve unavailable executable-path values. ⟦A.f2 A.f3 A:tb3 A:tb4⟧
### r02 · Try the contrast: Inspecting interpreter runtime information with sys
(mechanism) sys.executable identifies the running interpreter’s executable path when available. It may be an empty string or None if Python cannot retrieve it; do not invent a path. ⟦A.f1 A:tb2 A:tb4 A:tb5⟧
(mechanism) sys.version includes the interpreter version plus build and compiler information. ⟦A.f2 A:tb3 A:tb4⟧
(mechanism) After import sys, print(sys.executable) and print(sys.version) display the actual executing runtime. Compare these observations with the interpreter you intended, rather than relying only on a tool label. ⟦A.f3 A:tb3 A:tb4⟧
(misconception) Contrast the selected tool label with observations from the running process. Preserve unavailable executable-path values. ⟦A.f1 A.f2 A.f3 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Creating isolated virtual environments
(mechanism) Use the selected Python executable with -m venv .venv to create a project environment. Its interpreter is bin/python on POSIX or Scripts/python.exe on Windows. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) Activation changes command lookup to the environment executable. It is not required when invoking that executable by its full path. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
(mechanism) sys.prefix != sys.base_prefix identifies an interpreter running in a virtual environment. ⟦B.f3 B:tb3 B:tb4⟧
(misconception) Contrast activation with explicit invocation of the environment executable. Explicit invocation does not depend on activation. ⟦B.f1 B.f2 B.f3 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r04 · Try the contrast: Selecting the project environment interpreter
(mechanism) Inspect sys.executable in the executed program to identify its actual interpreter. An environment label is not the evidence for this check. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(misconception) Contrast a changed environment label with a rechecked running process. Verify the actual executable and prefixes. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
### r05 · Try the contrast: Selecting the project environment interpreter
(mechanism) Inspect sys.executable in the executed program to identify its actual interpreter. An environment label is not the evidence for this check. ⟦C.f1 C:tb2 C:tb4 C:tb5⟧
(mechanism) After changing the runtime, check the executable path and sys.prefix != sys.base_prefix again in the program that runs. Changing the displayed label is not the final check. ⟦C.f4 C:tb3 C:tb4 C:tb5⟧
(misconception) Contrast a changed environment label with a rechecked running process. Verify the actual executable and prefixes. ⟦C.f1 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r06 · Try the contrast: Selecting the project environment interpreter
(mechanism) A venv interpreter is at bin/python on POSIX or Scripts/python.exe on Windows. ⟦C.f2 C:tb3 C:tb4⟧
(mechanism) If command lookup selects the wrong Python, configure the tool to invoke the intended venv executable explicitly. Explicit invocation does not require activation. ⟦C.f3 C:tb3 C:tb4⟧
(misconception) Contrast a changed environment label with a rechecked running process. Verify the actual executable and prefixes. ⟦C.f2 C.f3 C:tb3 C:tb4⟧

=========

# EVALUATOR PACKET — Installing dependencies with python -m pip · Recreating dependencies from requirements files (learn_python.tile.097_098)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.pip_installation — Installing dependencies with python -m pip
B = python.requirements_files — Recreating dependencies from requirements files

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: remediation step learn_python.tile.097_098.r02 is never referenced
  warn: remediation step learn_python.tile.097_098.r04 is never referenced

## SOURCE FACTS — A (python.pip_installation)   objective: Install dependencies using the intended Python environment's pip.
A.f1: Invoke the intended environment’s interpreter with -m pip install package_name to install that distribution into that interpreter’s environment.   [sources: python_tutorial#venv.html#managing-packages-with-pip]
A.f2: Use -m pip show package_name or -m pip list through the same interpreter to inspect the installation.   [sources: python_tutorial#venv.html#managing-packages-with-pip]
A.f3: Import the package’s documented import name using the same interpreter to verify it is usable there.   [sources: python_tutorial#modules.html#more-on-modules]
A.f4: A distribution package installed by pip is not necessarily named the same as the import package used in Python code.   [sources: python_packaging_user_guide#discussions/distribution-package-vs-import-package/#what-are-the-links-between-distribution-packages-and-import-packages]
note: Begin with this objective: Install dependencies using the intended Python environment's pip.
note: Keep the example in the Installing and recording dependencies tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.requirements_files, python.assert_statement, python.iterables_and_iterators.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
note: Require linux.shell_pipes_and_redirection before shell-dependent environment work; commands here teach Python invocation, not shell fundamentals.
PRACTICE ANCHOR (live_code): Install a documented distribution into the intended virtual environment using its interpreter, inspect the installation, and import its documented import name using that same interpreter.  SUCCESS: The intended environment's interpreter completes installation, reports the distribution through pip show or pip list, and runs the documented import without an import error.
ASSESSMENT ANCHOR: install_distribution_with_intended_interpreter facts=['f1']
ASSESSMENT ANCHOR: inspect_installation_with_same_interpreter facts=['f2']
ASSESSMENT ANCHOR: verify_documented_import_in_active_environment facts=['f3', 'f4']

## SOURCE FACTS — B (python.requirements_files)   objective: Recreate an environment's dependencies from a requirements file.
B.f1: A requirements file lists dependencies, and package_name==version pins a specific version.   [sources: python_tutorial#venv.html#managing-packages-with-pip]
B.f2: Invoke the fresh environment’s Python with -m pip install -r requirements.txt to install the listed requirements.   [sources: python_tutorial#venv.html#managing-packages-with-pip]
B.f3: Use the same interpreter’s -m pip list to inspect installed versions.   [sources: python_tutorial#venv.html#managing-packages-with-pip]
B.f4: Check required imports in the recreated interpreter rather than assuming an installation report proves each module is importable.   [sources: python_tutorial#modules.html#more-on-modules]
note: Begin with this objective: Recreate an environment's dependencies from a requirements file.
note: Keep the example in the Installing and recording dependencies tile focused on this operation, rather than introducing additional capabilities.
note: Defer later concepts such as python.assert_statement, python.iterables_and_iterators, python.generator_functions.
note: Require linux.filesystem_navigation_and_files before this filesystem, script, module or environment unit; do not teach terminal navigation here.
note: Require linux.shell_pipes_and_redirection before shell-dependent environment work; commands here teach Python invocation, not shell fundamentals.
PRACTICE ANCHOR (live_code): Recreate a small project's declared dependencies in a fresh virtual environment, inspect their installed versions, and check the project's documented imports using that environment's interpreter.  SUCCESS: The declared dependencies are installed at their pinned versions, the same interpreter's package listing confirms those versions, and all documented required imports run successfully in the recreated interpreter.
ASSESSMENT ANCHOR: recognize_pinned_dependency_versions facts=['f1']
ASSESSMENT ANCHOR: install_requirements_in_fresh_environment facts=['f2']
ASSESSMENT ANCHOR: verify_installed_versions_with_same_interpreter facts=['f3']
ASSESSMENT ANCHOR: verify_required_imports_in_recreated_interpreter facts=['f4']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Accepting, repairing or rejecting generated Python on evidence; Chaining iterables with itertools; Choosing eager or lazy processing; Choosing map or filter for iterable transformations; Development checks with the Python assert statement; Generator expressions; Generator functions with yield; Iterables and iterators; Iterator consumption and exhaustion; Managing unittest setup and teardown; Reading and explaining generated Python; Recreating dependencies from requirements files; Reviewing generated Python dependency suggestions; Reviewing generated Python file operations for safety; Reviewing untrusted input and arbitrary Python execution; Running unittest and interpreting its results; Verifying generated Python API claims; Writing Python unittest test cases

## LESSON, in learner order

### s01 · explainer · Installing dependencies with python -m pip
Explore — 
(mechanism) Install a verified distribution using the intended environment interpreter with -m pip install package_name. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Through that same interpreter, inspect installation with -m pip show package_name or -m pip list. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(mechanism) Check usability by importing the documented import name under the same interpreter that will run the project. Installation with one interpreter does not verify usability in another. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(mechanism) A pip distribution name need not equal its Python import-package name. Use documented names rather than guessing the import spelling from the installation name. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
[DIAGRAM: Same interpreter across three checks] nodes=['Intended environment executable', '-m pip install package_name: verified distribution name', '-m pip show package_name or -m pip list', 'Import documented import name: may differ from distribution name'] edges=[('n1', 'n2', 'install through'), ('n1', 'n3', 'inspect through'), ('n1', 'n4', 'verify through')] alt: Same interpreter across three checks: Intended environment executable; -m pip install package_name: verified distribution name; -m pip show package_name or -m pip list; Import documented import name: may differ from distribution name

### s02 · check · Check: verify documented import in active environment
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, intro, grading=client] A distribution has been installed. What verifies its documented import is usable in the intended environment?
  ✔ correct: Run its documented import name using that same environment interpreter.
      why: Correct. Run its documented import name using that same environment interpreter.
  ✘ trap1: Guess that the distribution spelling is always the import name.
      why: Distribution and import package names need not be identical.
  ✘ trap2: Rely only on an installation success message.
      why: The documented import under the same interpreter is a separate usability check.
  feedback✔: Correct. Run its documented import name using that same environment interpreter.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Keep distribution installation and Python import verification separate.']  remediation→r01
  MEASURES: A:verify_documented_import_in_active_environment(f3,f4)   anchors=['assessment:verify_documented_import_in_active_environment']
  taught-before-tested: A.f3←s01; A.f4←s01

### s03 · hands_on · Review installing dependencies with python -m pip
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.
QUESTION [classify, core, grading=client] Project documentation specifies distribution package_name and import module_name. The intended existing POSIX interpreter is /project/.venv/bin/python. Read each transcript and decide whether installation, inspection, and documented import are all verified in that same environment.
  '/project/.venv/bin/python -m pip install package_name -> success
/project/.venv/bin/python -m pip show package_name -> package_name installed
/project/.venv/bin/python import_check.py (import module_name) -> no import error' -> Meets the stated criterion
      feedback: All three checks use the intended executable and the documented names.
  '/project/.venv/bin/python -m pip install package_name -> success
/project/.venv/bin/python -m pip show package_name -> package_name installed
/usr/bin/python3 import_check.py (import module_name) -> no import error' -> Does not meet the stated criterion
      feedback: The import check runs in another interpreter and does not verify this environment.
  '/project/.venv/bin/python -m pip install package_name -> success
/project/.venv/bin/python -m pip show package_name -> package_name installed
/project/.venv/bin/python import_check.py (import package_name) -> ModuleNotFoundError' -> Does not meet the stated criterion
      feedback: The script guesses the distribution spelling rather than using documented import module_name.
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: A:install_distribution_with_intended_interpreter(f1); A:inspect_installation_with_same_interpreter(f2); A:verify_documented_import_in_active_environment(f3,f4)   anchors=['practice', 'assessment:install_distribution_with_intended_interpreter', 'assessment:inspect_installation_with_same_interpreter', 'assessment:verify_documented_import_in_active_environment']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s04 · explainer · Recreating dependencies from requirements files
Explore — 
(mechanism) A requirements file lists dependencies. package_name==version pins a specific version; replace placeholders only with verified project information. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) Install the listed requirements using the fresh environment’s Python with -m pip install -r requirements.txt. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) Inspect installed versions with that same interpreter’s -m pip list. ⟦B.f3 B:tb3 B:tb4⟧
(mechanism) Check required documented imports in the recreated interpreter. An installation report alone does not prove that every required module is importable. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
[PROCESS_FLOW] nodes=['Verified dependency pins: package_name==version', 'Fresh environment Python: -m pip install -r requirements.txt', 'Same interpreter: -m pip list', 'Same interpreter: check required documented imports'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None)] alt: Recreate from verified pins, then inspect installed versions and check imports through the fresh environment interpreter.

### s05 · check · Check: verify required imports in recreated interpreter
Quick check — Read the supplied question and choose the answer that fits the requirement.
QUESTION [choice, core, grading=client] The fresh environment reports successful requirements installation. What is still needed to verify required imports?
  ✔ correct: Run the documented required imports in the recreated interpreter.
      why: Correct. Run the documented required imports in the recreated interpreter.
  ✘ trap1: Assume the install report proves every required import works.
      why: The installation report alone is not final evidence of module importability.
  ✘ trap2: Check imports only in the old system interpreter.
      why: Imports must be checked in the recreated interpreter, not another environment.
  feedback✔: Correct. Run the documented required imports in the recreated interpreter.  feedback✘: Compare the alternatives with the taught distinction; the selected claim does not meet it.  hints: ['Which process must demonstrate importability?']  remediation→r03
  MEASURES: B:verify_required_imports_in_recreated_interpreter(f4)   anchors=['assessment:verify_required_imports_in_recreated_interpreter']
  taught-before-tested: B.f4←s04

### s06 · hands_on · Review recreating dependencies from requirements files
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.
QUESTION [classify, stretch, grading=client] Project documentation: requirements.txt contains package_name==version; required import is module_name. Fresh POSIX interpreter: /project/.venv/bin/python. Read each transcript and decide whether pinned installation, version listing, and required import are verified in that interpreter.
  '/project/.venv/bin/python -m pip install -r requirements.txt -> success
/project/.venv/bin/python -m pip list -> package_name version
/project/.venv/bin/python import_check.py (import module_name) -> no import error' -> Meets the stated criterion
      feedback: The fresh interpreter installs the pinned requirement, confirms its version and imports the documented name.
  '/project/.venv/bin/python -m pip install -r requirements.txt -> success
/project/.venv/bin/python -m pip list -> package_name version
No import check performed.' -> Does not meet the stated criterion
      feedback: Installation and listing do not alone verify the required import.
  '/project/.venv/bin/python -m pip install -r requirements.txt -> success
/usr/bin/python3 -m pip list -> package_name version
/usr/bin/python3 import_check.py (import module_name) -> no import error' -> Does not meet the stated criterion
      feedback: Listing and import in system Python are not verification of the recreated interpreter.
  feedback✔: Correct: your judgement follows the stated requirement.  feedback✘: Recheck the requirement and the supplied evidence before trying again.  hints: ['Compare the requested behavior with each step of the supplied code or evidence.']
  MEASURES: B:recognize_pinned_dependency_versions(f1); B:install_requirements_in_fresh_environment(f2); B:verify_installed_versions_with_same_interpreter(f3); B:verify_required_imports_in_recreated_interpreter(f4)   anchors=['practice', 'assessment:recognize_pinned_dependency_versions', 'assessment:install_requirements_in_fresh_environment', 'assessment:verify_installed_versions_with_same_interpreter', 'assessment:verify_required_imports_in_recreated_interpreter']
  taught-before-tested: B.f1←s04; B.f2←s04; B.f3←s04; B.f4←s04

### s07 · recap · Keep these ideas
Recap — 
(takeaway) Use one interpreter for installation, inspection and documented imports; distribution and import names may differ. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Record verified version pins, install into a fresh environment, inspect versions and check required imports. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Next: Development checks with the Python assert statement: 

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Try the contrast: Installing dependencies with python -m pip
(mechanism) Check usability by importing the documented import name under the same interpreter that will run the project. Installation with one interpreter does not verify usability in another. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(mechanism) A pip distribution name need not equal its Python import-package name. Use documented names rather than guessing the import spelling from the installation name. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast installation evidence with import evidence. Both checks must use the intended interpreter and documented names. ⟦A.f3 A.f4 A:tb1 A:tb3 A:tb4 A:tb5⟧
### r02 · Try the contrast: Installing dependencies with python -m pip
(mechanism) Install a verified distribution using the intended environment interpreter with -m pip install package_name. ⟦A.f1 A:tb1 A:tb2 A:tb4 A:tb5⟧
(mechanism) Through that same interpreter, inspect installation with -m pip show package_name or -m pip list. ⟦A.f2 A:tb1 A:tb3 A:tb4⟧
(mechanism) Check usability by importing the documented import name under the same interpreter that will run the project. Installation with one interpreter does not verify usability in another. ⟦A.f3 A:tb1 A:tb3 A:tb4 A:tb5⟧
(mechanism) A pip distribution name need not equal its Python import-package name. Use documented names rather than guessing the import spelling from the installation name. ⟦A.f4 A:tb3 A:tb4 A:tb5⟧
(misconception) Contrast installation evidence with import evidence. Both checks must use the intended interpreter and documented names. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
### r03 · Try the contrast: Recreating dependencies from requirements files
(mechanism) Check required documented imports in the recreated interpreter. An installation report alone does not prove that every required module is importable. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a successful installation report with checking required imports in the recreated interpreter. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
### r04 · Try the contrast: Recreating dependencies from requirements files
(mechanism) A requirements file lists dependencies. package_name==version pins a specific version; replace placeholders only with verified project information. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) Install the listed requirements using the fresh environment’s Python with -m pip install -r requirements.txt. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) Inspect installed versions with that same interpreter’s -m pip list. ⟦B.f3 B:tb3 B:tb4⟧
(mechanism) Check required documented imports in the recreated interpreter. An installation report alone does not prove that every required module is importable. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
(misconception) Contrast a successful installation report with checking required imports in the recreated interpreter. ⟦B.f1 B.f2 B.f3 B.f4 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧