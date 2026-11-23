# EVALUATOR PACKET — Computing dates and elapsed times with datetime (learn_python.tile.084_084)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.datetime_operations — Computing dates and elapsed times with datetime

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Practise computing dates and elapsed times with datetime
Practice — Parse two year-month-day date strings into calendar dates and compute the signed number of days between them in both subtraction orders.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: derive module name from python filename
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s04 · check · Check: explain sibling import availability in ordinary script invocation
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s05 · hands_on · Practise creating local modules
Practice — Move the cost(quantity, price) helper from report.py into a sibling helpers.py file, then import and call the shared helper from report.py.

### s06 · explainer · Organising importable packages
Explore — 
(mechanism) A regular package groups modules in a directory with __init__.py, which may be empty. In the orders layout, costs.py and __init__.py belong inside the orders directory. ⟦B.f1 B:tb2 B:tb4 B:tb5 B:tb1⟧
(mechanism) Where orders is importable, use import orders.costs and orders.costs.cost(quantity, price). Alternatively, from orders.costs import cost gives the direct call cost(quantity, price). Keep package, module and helper distinct. ⟦B.f2 B:tb3 B:tb4 B:tb5⟧
[DIAGRAM: Regular package layout] nodes=['orders/', 'orders/__init__.py (may be empty)', 'orders/costs.py: cost helper', 'import orders.costs', 'orders.costs.cost(3, 4)', 'from orders.costs import cost', 'cost(quantity, price)', 'orders/: second related module'] edges=[('n1', 'n2', 'contains'), ('n1', 'n3', 'contains'), ('n4', 'n5', 'qualified call'), ('n6', 'n7', 'direct call'), ('n1', 'n8', 'contains')] alt: Regular package layout: orders/; orders/__init__.py (may be empty); orders/costs.py: cost helper; import orders.costs; orders.costs.cost(3, 4); from orders.costs import cost; cost(quantity, price); orders/: second related module

### s07 · check · Check: create regular package layout
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s08 · hands_on · Practise organising importable packages
Practice — Group costs.py and a second related module into a local orders package containing an empty __init__.py, then import and call the cost helper through the package name.

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

=========

# EVALUATOR PACKET — Recording program events with logging (learn_python.tile.087_087)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.logging — Recording program events with logging

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · check · Check: avoid duplicate output from ancestor handlers
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s05 · hands_on · Practise recording program events with logging
Practice — Replace diagnostic prints in a report helper with a module logger, using DEBUG for detailed quantity calculation and INFO for report completion.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: guard command interface actions against import execution
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s04 · hands_on · Practise guarding a program entry point
Practice — Make the cost helper importable without triggering user prompts, while retaining the script's interactive cost calculation during direct execution.

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

### s08 · hands_on · Practise parsing command-line arguments with argparse
Practice — Give the order-report script a required input_path argument and an optional --verbose flag, then inspect the parsed values.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: diagnose module not found from search locations
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s04 · hands_on · Practise diagnosing module search-path problems
Practice — Diagnose and fix a local json.py filename that shadows the standard-library json module.

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

=========

# EVALUATOR PACKET — Accessing environment variables with os.environ (learn_python.tile.091_091)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.os_environment — Accessing environment variables with os.environ

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · check · Check: recognize missing key error from bracket lookup
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s04 · hands_on · Practise accessing environment variables with os.environ
Practice — Read a nonsecret output-directory setting stored under ORDER_SOURCE with os.environ.get, and report its absence explicitly.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Check: select seeded random for reproducible simulation
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s04 · check · Check: select secrets for security sensitive tokens
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s05 · hands_on · Practise choosing random or secrets for randomness
Practice — Use random.seed(7) and random.random() to generate a short sequence of simulation values, then reset the same seed and repeat the calls to demonstrate reproducibility.

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

=========

# EVALUATOR PACKET — Matching text patterns with re (learn_python.tile.093_093)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.regular_expressions — Matching text patterns with re

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s04 · hands_on · Practise matching text patterns with re
Practice — Validate a nonempty uppercase-letter label using a simple pattern, re.fullmatch, and an explicit is not None success test.

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

=========

# EVALUATOR PACKET — Inspecting interpreter runtime information with sys · Creating isolated virtual environments · Selecting the project environment interpreter (learn_python.tile.094_096)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = python.sys_runtime_interface — Inspecting interpreter runtime information with sys
B = python.virtual_environments — Creating isolated virtual environments
C = python.environment_interpreter_selection — Selecting the project environment interpreter

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review inspecting interpreter runtime information with sys
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.

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

### s07 · hands_on · Review creating isolated virtual environments
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.

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

### s11 · check · Check: verify interpreter selection after rerun
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s12 · hands_on · Review selecting the project environment interpreter
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Review installing dependencies with python -m pip
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.

### s04 · explainer · Recreating dependencies from requirements files
Explore — 
(mechanism) A requirements file lists dependencies. package_name==version pins a specific version; replace placeholders only with verified project information. ⟦B.f1 B:tb1 B:tb2 B:tb4⟧
(mechanism) Install the listed requirements using the fresh environment’s Python with -m pip install -r requirements.txt. ⟦B.f2 B:tb3 B:tb4⟧
(mechanism) Inspect installed versions with that same interpreter’s -m pip list. ⟦B.f3 B:tb3 B:tb4⟧
(mechanism) Check required documented imports in the recreated interpreter. An installation report alone does not prove that every required module is importable. ⟦B.f4 B:tb1 B:tb3 B:tb4 B:tb5⟧
[PROCESS_FLOW] nodes=['Verified dependency pins: package_name==version', 'Fresh environment Python: -m pip install -r requirements.txt', 'Same interpreter: -m pip list', 'Same interpreter: check required documented imports'] edges=[('n1', 'n2', None), ('n2', 'n3', None), ('n3', 'n4', None)] alt: Recreate from verified pins, then inspect installed versions and check imports through the fresh environment interpreter.

### s05 · check · Check: verify required imports in recreated interpreter
Quick check — Read the supplied question and choose the answer that fits the requirement.

### s06 · hands_on · Review recreating dependencies from requirements files
Practice — Read the supplied excerpts in this step and judge which meet the requirement and which are defective.

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