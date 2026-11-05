"""Build interactions.part.c3.json for chunk c3 tiles:
  tile_python_functions_scope
  tile_python_errors_imports
  tile_python_file_io
  tile_python_pep8_style
"""
import json

PYTHON_VERSION = "0.29.5"

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def choice(step_id, interaction_id, difficulty, standalone, measures, anchors,
           prompt, options, correct_ids, option_feedback, feedback):
    return {
        "step_id": step_id,
        "interaction": {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": difficulty,
            "grading_mode": "client",
            "standalone": standalone,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": prompt,
                "options": options,
                "selection": "single",
                "shuffle": True,
            },
            "grading": {
                "correct_option_ids": correct_ids,
                "option_feedback": option_feedback,
            },
            "feedback": feedback,
        }
    }


def code_ex(step_id, interaction_id, difficulty, standalone, measures, anchors,
            prompt, runtime_packages, files, entry, asset_mounts,
            allowed_syntax, blocked_syntax,
            solution_files, tests, feedback):
    runtime = {"kind": "python", "version": PYTHON_VERSION}
    if runtime_packages:
        runtime["packages"] = runtime_packages
    workspace = {"files": files, "entry": entry}
    if asset_mounts:
        workspace["asset_mounts"] = asset_mounts
    return {
        "step_id": step_id,
        "interaction": {
            "type": "code_exercise",
            "interaction_id": interaction_id,
            "difficulty": difficulty,
            "grading_mode": "client",
            "standalone": standalone,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": prompt,
                "runtime": runtime,
                "workspace": workspace,
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax,
                },
            },
            "grading": {
                "solution_files": solution_files,
                "tests": tests,
            },
            "feedback": feedback,
        }
    }


# ─────────────────────────────────────────────────────────────────────────────
# Allowed / blocked syntax lists (verbatim from glossary practice anchors)
# ─────────────────────────────────────────────────────────────────────────────

# python.defining_calling_functions practice anchor
ALLOWED_DEF_CALL = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
]
BLOCKED_DEF_CALL = [
    "def f(a, b):",
    "positional arguments in a call",
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.parameters_arguments practice anchor
ALLOWED_PARAMS = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
]
BLOCKED_PARAMS = [
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.return_values practice anchor
ALLOWED_RETURN = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
    "return",
]
BLOCKED_RETURN = [
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.function_default_keyword_args practice anchor
ALLOWED_DEFAULTS = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
]
BLOCKED_DEFAULTS = [
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.variable_scope practice anchor
ALLOWED_SCOPE = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
]
BLOCKED_SCOPE = [
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.error_handling practice anchor
ALLOWED_ERROR = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
]
BLOCKED_ERROR = [
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.import_statements practice anchor
ALLOWED_IMPORT = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
]
BLOCKED_IMPORT = [
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.file_io practice anchor
ALLOWED_FILEIO = [
    "name = value assignment",
    "using assigned names in an expression, as in the width * height example",
    "int, float, str and bool literals",
    "single- or double-quoted strings",
    "True / False",
    "print()",
    "type()",
    "+ - * / // % **",
    "parentheses for grouping",
    "< <= > >= == !=",
    "and",
    "or",
    "not",
    "int()",
    "float()",
    "str()",
    "[...] list literal",
    "list[i] and list[-1] indexing",
    "list[a:b] slicing",
    "list[i] = value",
    "list.append()",
    "len()",
    "{key: value} dictionary literal",
    "d[key] lookup and assignment",
    "d.get()",
    "key in d",
    "tuple literal with commas or parentheses",
    "unpacking a, b = t",
    "one-item tuple with trailing comma",
    "set()",
    "{...} set literal",
    "x in a_set",
    "| and & on sets",
    "quote mixing to embed a quote",
    'f-strings f"...{expr}..."',
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue",
    "[expr for x in seq]",
    "[expr for x in seq if cond]",
    "{k: v for ...}",
    "for key in d:",
    "for k, v in d.items():",
    "def name():",
    "calling name()",
    "def f(a, b):",
    "positional arguments in a call",
    "return",
    "def f(a, b=default):",
    "keyword arguments f(name=value)",
    "global statement",
    "try:",
    "except ValueError:",
    "input()",
    "import module",
    "module.name",
    "from module import name",
    "open(file, mode)",
    "with open(...) as f:",
    "f.read()",
    "f.write()",
    "csv.DictReader",
    "csv.DictWriter",
    "newline=''",
]
BLOCKED_FILEIO = [
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy",
]

# python.pep8_style practice anchor (same as file_io)
ALLOWED_PEP8 = ALLOWED_FILEIO[:]
BLOCKED_PEP8 = BLOCKED_FILEIO[:]


# ─────────────────────────────────────────────────────────────────────────────
# tile_python_functions_scope interactions
# ─────────────────────────────────────────────────────────────────────────────

# s02: check — recognize_function_definition (f1)
s02 = choice(
    step_id="tile_python_functions_scope.s02",
    interaction_id="ix.tile_python_functions_scope.s02",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.defining_calling_functions",
        "capability": "recognize_function_definition",
        "fact_ids": ["f1"],
    }],
    anchors=["python.defining_calling_functions#assessment:recognize_function_definition"],
    prompt=(
        "Which of the following is a valid Python function definition?\n\n"
        "```python\n# A\nfunction greet():\n    print('Hello')\n\n"
        "# B\ndef greet():\n    print('Hello')\n\n"
        "# C\ngreet def():\n    print('Hello')\n\n"
        "# D\ndef greet\n    print('Hello')\n```"
    ),
    options=[
        {"option_id": "opt_a", "text": "A — uses the keyword `function`"},
        {"option_id": "opt_b", "text": "B — uses `def`, the function name, parentheses, and a colon"},
        {"option_id": "opt_c", "text": "C — puts the name before `def`"},
        {"option_id": "opt_d", "text": "D — omits the parentheses and colon"},
    ],
    correct_ids=["opt_b"],
    option_feedback={
        "opt_a": {"message": "Python uses `def`, not `function`. The syntax is `def name():` followed by an indented body."},
        "opt_b": {"message": "Correct. `def greet():` uses the `def` keyword, the function name, empty parentheses, and a colon before the indented body."},
        "opt_c": {"message": "The `def` keyword must come first, before the function name. The correct order is `def greet():`"},
        "opt_d": {"message": "A function definition requires parentheses (even if empty) and a colon after the name: `def greet():`"},
    },
    feedback={
        "correct": {"message": "Right — `def greet():` is the correct syntax. `def` comes first, then the name, then `()`, then `:`."},
        "incorrect": {"message": "A function definition starts with `def`, followed by the name, parentheses (possibly empty), and a colon. The body is indented on the next line."},
        "hints": [
            "The keyword that introduces a function definition is three letters long and starts with 'd'.",
            "After the name, you need `()` even if there are no parameters, and a `:` before the indented body.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r01",
    },
)

# s03: hands_on — call_function_to_run_its_body (f2)
# Practice: create a small reusable helper with def and call it more than once.
# Success: The helper's body runs once per call, and nothing runs when only the def is written.
# Starter: empty file. Solution: define greet_driver() that prints a message, call it twice.
# Tests: stdout_equals — two calls produce two lines of output.
# The starter must NOT pass the tests (it has no function def or calls).
STARTER_S03 = (
    "# Define a function called greet_driver that prints:\n"
    "#   'QuickDeliver driver ready'\n"
    "# Then call it twice.\n"
)
SOLUTION_S03 = (
    "def greet_driver():\n"
    "    print('QuickDeliver driver ready')\n"
    "\n"
    "greet_driver()\n"
    "greet_driver()\n"
)
EXPECTED_STDOUT_S03 = "QuickDeliver driver ready\nQuickDeliver driver ready"

s03 = code_ex(
    step_id="tile_python_functions_scope.s03",
    interaction_id="ix.tile_python_functions_scope.s03",
    difficulty="core",
    standalone=False,
    measures=[{
        "concept_id": "python.defining_calling_functions",
        "capability": "call_function_to_run_its_body",
        "fact_ids": ["f2"],
    }],
    anchors=[
        "python.defining_calling_functions#practice",
        "python.defining_calling_functions#assessment:call_function_to_run_its_body",
    ],
    prompt=(
        "Define a function called `greet_driver` that prints exactly:\n\n"
        "```\nQuickDeliver driver ready\n```\n\n"
        "Then **call it twice**. The output should show the message two times.\n\n"
        "Use only `def name():` and `calling name()`. Do not add parameters or a `return` statement."
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S03,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_DEF_CALL,
    blocked_syntax=BLOCKED_DEF_CALL,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S03}],
    tests=[
        {
            "test_id": "t1_two_calls",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S03},
            "visible": True,
            "message_on_fail": "Your output should show 'QuickDeliver driver ready' printed twice, once per call.",
        }
    ],
    feedback={
        "correct": {"message": "Well done — calling `greet_driver()` twice ran the body twice. The `def` line only defines the function; the body runs only when you call it."},
        "incorrect": {"message": "Make sure you have a `def greet_driver():` block with the print inside, then two separate calls `greet_driver()` after the definition."},
        "hints": [
            "The `def` block only stores the function — it does not run it. You need a separate call line after the definition.",
            "To call a function, write its name followed by `()`. Do this on two separate lines after the `def` block.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r01",
    },
)

# s05: check — match_positional_arguments_to_parameters (f3)
s05 = choice(
    step_id="tile_python_functions_scope.s05",
    interaction_id="ix.tile_python_functions_scope.s05",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.parameters_arguments",
        "capability": "match_positional_arguments_to_parameters",
        "fact_ids": ["f3"],
    }],
    anchors=["python.parameters_arguments#assessment:match_positional_arguments_to_parameters"],
    prompt=(
        "Given this function:\n\n"
        "```python\ndef log_delivery(order_id, city, minutes):\n    print(order_id, city, minutes)\n```\n\n"
        "What does `log_delivery(1042, 'Lagos', 32)` print?"
    ),
    options=[
        {"option_id": "opt_a", "text": "`1042 Lagos 32`"},
        {"option_id": "opt_b", "text": "`Lagos 1042 32`"},
        {"option_id": "opt_c", "text": "`32 Lagos 1042`"},
        {"option_id": "opt_d", "text": "`order_id city minutes`"},
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": {"message": "Correct. Positional arguments fill parameter slots in order: `order_id=1042`, `city='Lagos'`, `minutes=32`."},
        "opt_b": {"message": "Arguments fill slots in the order they appear in the call, not alphabetically. The first argument `1042` goes to the first parameter `order_id`."},
        "opt_c": {"message": "Arguments are matched by position, not by value size. `1042` → `order_id`, `'Lagos'` → `city`, `32` → `minutes`."},
        "opt_d": {"message": "The function prints the argument values, not the parameter names. Parameter names are local labels inside the function."},
    },
    feedback={
        "correct": {"message": "Right — positional arguments fill parameter slots left-to-right in the order they appear in the call."},
        "incorrect": {"message": "Positional arguments are matched to parameters by position: the first argument goes to the first parameter, the second to the second, and so on."},
        "hints": [
            "Look at the order of parameters in `def log_delivery(order_id, city, minutes)` and the order of arguments in the call.",
            "The first argument in the call fills the first parameter slot, the second fills the second, and so on.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r02",
    },
)

# s06: hands_on — parameters_arguments practice
# Practice: Turn a simple helper into one that takes parameters, then call it with different positional arguments.
# Success: Each call uses its own argument values, and arguments land in the parameter slots in order.
# Starter: a helper that prints a fixed message (no parameters yet).
# Solution: add two parameters (city, minutes), call twice with different args.
STARTER_S06 = (
    "# The function below prints a fixed message.\n"
    "# Rewrite it so it takes two parameters: city and minutes.\n"
    "# Then call it twice:\n"
    "#   first with 'Lagos' and 32\n"
    "#   then with 'Abuja' and 45\n"
    "\n"
    "def report_delivery():\n"
    "    print('Delivered')\n"
)
SOLUTION_S06 = (
    "def report_delivery(city, minutes):\n"
    "    print(city, minutes)\n"
    "\n"
    "report_delivery('Lagos', 32)\n"
    "report_delivery('Abuja', 45)\n"
)
EXPECTED_STDOUT_S06 = "Lagos 32\nAbuja 45"

s06 = code_ex(
    step_id="tile_python_functions_scope.s06",
    interaction_id="ix.tile_python_functions_scope.s06",
    difficulty="core",
    standalone=False,
    measures=[
        {
            "concept_id": "python.parameters_arguments",
            "capability": "identify_parameters_and_their_values",
            "fact_ids": ["f1", "f2"],
        },
        {
            "concept_id": "python.parameters_arguments",
            "capability": "match_positional_arguments_to_parameters",
            "fact_ids": ["f3"],
        },
    ],
    anchors=[
        "python.parameters_arguments#practice",
        "python.parameters_arguments#assessment:identify_parameters_and_their_values",
        "python.parameters_arguments#assessment:match_positional_arguments_to_parameters",
    ],
    prompt=(
        "Rewrite `report_delivery` so it accepts two parameters: `city` and `minutes`.\n"
        "Inside the body, print them with `print(city, minutes)`.\n\n"
        "Then call it twice:\n"
        "1. `report_delivery('Lagos', 32)` — should print `Lagos 32`\n"
        "2. `report_delivery('Abuja', 45)` — should print `Abuja 45`\n\n"
        "Use only `def f(a, b):` and positional arguments. Do not use `return`."
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S06,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_PARAMS,
    blocked_syntax=BLOCKED_PARAMS,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S06}],
    tests=[
        {
            "test_id": "t1_output",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S06},
            "visible": True,
            "message_on_fail": "Expected two lines: 'Lagos 32' then 'Abuja 45'. Check that your parameters are named `city` and `minutes` and that you call the function twice with the right arguments.",
        }
    ],
    feedback={
        "correct": {"message": "Well done — each call passed its own arguments to the parameters in order, so `city` and `minutes` held different values in each call."},
        "incorrect": {"message": "Add `city` and `minutes` to the `def` line's parentheses, then call `report_delivery('Lagos', 32)` and `report_delivery('Abuja', 45)`."},
        "hints": [
            "Change `def report_delivery():` to `def report_delivery(city, minutes):` to add the two parameters.",
            "After the definition, write two call lines. The first argument goes to `city`, the second to `minutes`.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r02",
    },
)

# s09: check — return_and_store_a_value (f1, f3)
s09 = choice(
    step_id="tile_python_functions_scope.s09",
    interaction_id="ix.tile_python_functions_scope.s09",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.return_values",
        "capability": "return_and_store_a_value",
        "fact_ids": ["f1", "f3"],
    }],
    anchors=["python.return_values#assessment:return_and_store_a_value"],
    prompt=(
        "```python\ndef compute_late_fee(minutes):\n    return minutes * 2\n\nfee = compute_late_fee(30)\nprint(fee)\n```\n\n"
        "What does this script print?"
    ),
    options=[
        {"option_id": "opt_a", "text": "`60`"},
        {"option_id": "opt_b", "text": "`None`"},
        {"option_id": "opt_c", "text": "`minutes * 2`"},
        {"option_id": "opt_d", "text": "`30`"},
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_a": {"message": "Correct. `return minutes * 2` sends `30 * 2 = 60` back to the caller. `fee = compute_late_fee(30)` stores `60`, and `print(fee)` prints `60`."},
        "opt_b": {"message": "`None` is returned only when a function has no `return` statement. This function has `return minutes * 2`, so it returns the computed value."},
        "opt_c": {"message": "Python evaluates the expression `minutes * 2` and returns the result (`60`), not the expression text."},
        "opt_d": {"message": "`30` is the argument passed in. The function multiplies it by `2` and returns `60`, which is what gets stored in `fee`."},
    },
    feedback={
        "correct": {"message": "Right — `return minutes * 2` sends `60` back to the caller, which stores it in `fee` and prints it."},
        "incorrect": {"message": "`return` sends the computed value back to the caller. `fee = compute_late_fee(30)` stores that returned value, so `print(fee)` prints it."},
        "hints": [
            "Trace the call: `minutes` is `30` inside the function. What does `30 * 2` equal?",
            "The `return` statement sends that result back. `fee = compute_late_fee(30)` stores whatever `return` sends.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r03",
    },
)

# s10: hands_on — return_values practice
# Practice: Write a function that returns a calculated value, and store the result in a variable.
# Success: The function returns rather than prints the value, and the variable holds that value when printed afterward.
# Starter: variable assignments for inputs.
# Solution: def compute_wait_fee(minutes): return minutes * 2; result = compute_wait_fee(minutes); print(result)
# minutes = 45, so result = 90
STARTER_S10 = (
    "# The delivery team charges a wait fee of 2 NGN per minute late.\n"
    "# Define a function called compute_wait_fee that takes one parameter: minutes\n"
    "# It should RETURN minutes * 2 (do not print inside the function).\n"
    "#\n"
    "# Then call it with the value stored in `minutes` and store the result in `result`.\n"
    "# Finally, print result.\n"
    "\n"
    "minutes = 45\n"
)
SOLUTION_S10 = (
    "minutes = 45\n"
    "\n"
    "def compute_wait_fee(minutes):\n"
    "    return minutes * 2\n"
    "\n"
    "result = compute_wait_fee(minutes)\n"
    "print(result)\n"
)
# 45 * 2 = 90
EXPECTED_STDOUT_S10 = "90"

s10 = code_ex(
    step_id="tile_python_functions_scope.s10",
    interaction_id="ix.tile_python_functions_scope.s10",
    difficulty="core",
    standalone=False,
    measures=[
        {
            "concept_id": "python.return_values",
            "capability": "distinguish_return_from_print",
            "fact_ids": ["f1", "f2"],
        },
        {
            "concept_id": "python.return_values",
            "capability": "return_and_store_a_value",
            "fact_ids": ["f1", "f3"],
        },
    ],
    anchors=[
        "python.return_values#practice",
        "python.return_values#assessment:distinguish_return_from_print",
        "python.return_values#assessment:return_and_store_a_value",
    ],
    prompt=(
        "The delivery team charges a wait fee of 2 NGN per minute late.\n\n"
        "1. Define a function `compute_wait_fee(minutes)` that **returns** `minutes * 2`.\n"
        "   Do **not** use `print()` inside the function.\n"
        "2. Call it with the value stored in `minutes` (already set to `45`) and store the returned value in a variable called `result`.\n"
        "3. Print `result`.\n\n"
        "Expected output: `90`"
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S10,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_RETURN,
    blocked_syntax=BLOCKED_RETURN,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S10}],
    tests=[
        {
            "test_id": "t1_result_value",
            "kind": "value_equals",
            "spec": {"expr": "result", "expected": 90},
            "visible": True,
            "message_on_fail": "`result` should hold `90` (45 * 2). Make sure your function returns the value rather than printing it.",
        },
        {
            "test_id": "t2_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S10},
            "visible": True,
            "message_on_fail": "The program should print `90`. Check that you call `print(result)` after storing the returned value.",
        },
    ],
    feedback={
        "correct": {"message": "Well done — `compute_wait_fee` returns the value, and `result = compute_wait_fee(minutes)` stores it so you can print it afterward."},
        "incorrect": {"message": "Use `return minutes * 2` inside the function (not `print`). Then write `result = compute_wait_fee(minutes)` and `print(result)` outside."},
        "hints": [
            "Inside the function, use `return minutes * 2` — not `print(minutes * 2)`. The caller receives the returned value.",
            "After the function definition, write `result = compute_wait_fee(minutes)` to capture the returned value, then `print(result)`.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r03",
    },
)

# s13: check — recognize_mutable_default_trap (m1)
s13 = choice(
    step_id="tile_python_functions_scope.s13",
    interaction_id="ix.tile_python_functions_scope.s13",
    difficulty="stretch",
    standalone=True,
    measures=[{
        "concept_id": "python.function_default_keyword_args",
        "capability": "recognize_mutable_default_trap",
        "fact_ids": ["m1"],
    }],
    anchors=["python.function_default_keyword_args#assessment:recognize_mutable_default_trap"],
    prompt=(
        "```python\ndef add_order(order_id, log=[]):\n    log.append(order_id)\n    return log\n\n"
        "print(add_order(1042))\nprint(add_order(1043))\n```\n\n"
        "What does the second `print` output?"
    ),
    options=[
        {"option_id": "opt_a", "text": "`[1043]` — each call gets a fresh empty list."},
        {"option_id": "opt_b", "text": "`[1042, 1043]` — the same list object is reused across calls."},
        {"option_id": "opt_c", "text": "`[]` — the default is reset after each call."},
        {"option_id": "opt_d", "text": "A `TypeError` — you cannot use a list as a default value."},
    ],
    correct_ids=["opt_b"],
    option_feedback={
        "opt_a": {"message": "This is the trap: the default `[]` is evaluated once when the function is defined, not on each call. The same list object is shared across all calls that omit `log`."},
        "opt_b": {"message": "Correct. The default list is created once at definition time. Both calls share the same object, so after two calls it holds `[1042, 1043]`."},
        "opt_c": {"message": "Python does not reset mutable defaults between calls. The default object is created once and accumulates changes."},
        "opt_d": {"message": "Python allows any object as a default value, including lists. The issue is not a TypeError but unexpected shared state."},
    },
    feedback={
        "correct": {"message": "Right — mutable defaults like `[]` are evaluated once at definition time and shared across all calls that omit the argument."},
        "incorrect": {"message": "Default values are evaluated once when the `def` statement runs, not on each call. A mutable default like `[]` accumulates changes across calls."},
        "hints": [
            "When is the default value `[]` created — once when `def` runs, or fresh on every call?",
            "If the same list object is used every time, what happens when `append` modifies it on the first call?",
        ],
        "remediation_step_id": "tile_python_functions_scope.r04",
    },
)

# s14: hands_on — function_default_keyword_args practice
# Practice: Write a function with a default parameter, call once omitting default, once with keyword args.
# Success: Both calls run; the omitted default takes its default value and the keyword call sets values by name.
# Starter: function with two parameters where one has no default yet.
# Solution: def describe_order(order_id, city='Lagos'): print(order_id, city)
#           describe_order(1042)  -> 1042 Lagos
#           describe_order(order_id=1043, city='Abuja')  -> 1043 Abuja
STARTER_S14 = (
    "# Add a default value of 'Lagos' to the city parameter.\n"
    "# Then:\n"
    "#   Call describe_order with only order_id=1042 (city uses its default)\n"
    "#   Call describe_order with keyword arguments order_id=1043, city='Abuja'\n"
    "\n"
    "def describe_order(order_id, city):\n"
    "    print(order_id, city)\n"
)
SOLUTION_S14 = (
    "def describe_order(order_id, city='Lagos'):\n"
    "    print(order_id, city)\n"
    "\n"
    "describe_order(1042)\n"
    "describe_order(order_id=1043, city='Abuja')\n"
)
EXPECTED_STDOUT_S14 = "1042 Lagos\n1043 Abuja"

s14 = code_ex(
    step_id="tile_python_functions_scope.s14",
    interaction_id="ix.tile_python_functions_scope.s14",
    difficulty="core",
    standalone=False,
    measures=[
        {
            "concept_id": "python.function_default_keyword_args",
            "capability": "call_with_default_omitted",
            "fact_ids": ["f1"],
        },
        {
            "concept_id": "python.function_default_keyword_args",
            "capability": "call_with_keyword_arguments",
            "fact_ids": ["f2", "f3"],
        },
    ],
    anchors=[
        "python.function_default_keyword_args#practice",
        "python.function_default_keyword_args#assessment:call_with_default_omitted",
        "python.function_default_keyword_args#assessment:call_with_keyword_arguments",
    ],
    prompt=(
        "Add a default value of `'Lagos'` to the `city` parameter of `describe_order`.\n\n"
        "Then make two calls:\n"
        "1. `describe_order(1042)` — omit `city` so it uses the default `'Lagos'`\n"
        "2. `describe_order(order_id=1043, city='Abuja')` — use keyword arguments\n\n"
        "Expected output:\n```\n1042 Lagos\n1043 Abuja\n```"
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S14,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_DEFAULTS,
    blocked_syntax=BLOCKED_DEFAULTS,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S14}],
    tests=[
        {
            "test_id": "t1_output",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S14},
            "visible": True,
            "message_on_fail": "Expected '1042 Lagos' then '1043 Abuja'. Check that city has a default of 'Lagos' and that you use keyword arguments in the second call.",
        }
    ],
    feedback={
        "correct": {"message": "Well done — the first call used the default `'Lagos'` for `city`, and the second call set both values by name using keyword arguments."},
        "incorrect": {"message": "Change `def describe_order(order_id, city):` to `def describe_order(order_id, city='Lagos'):`. Then call it once with just `1042` and once with `order_id=1043, city='Abuja'`."},
        "hints": [
            "To add a default, change the parameter to `city='Lagos'` in the `def` line.",
            "A keyword argument uses the form `name=value` in the call, e.g. `describe_order(order_id=1043, city='Abuja')`.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r04",
    },
)

# s18: check — predict_name_resolution (f1, f2)
# threshold = 45 globally; inside is_late, threshold = 60 (local); 50 > 60 = False; global threshold still 45
s18 = choice(
    step_id="tile_python_functions_scope.s18",
    interaction_id="ix.tile_python_functions_scope.s18",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.variable_scope",
        "capability": "predict_name_resolution",
        "fact_ids": ["f1", "f2"],
    }],
    anchors=["python.variable_scope#assessment:predict_name_resolution"],
    prompt=(
        "```python\nthreshold = 45\n\ndef is_late(minutes):\n    threshold = 60\n    return minutes > threshold\n\nprint(is_late(50))\nprint(threshold)\n```\n\n"
        "What does this script print?"
    ),
    options=[
        {"option_id": "opt_a", "text": "`True` then `60`"},
        {"option_id": "opt_b", "text": "`True` then `45`"},
        {"option_id": "opt_c", "text": "`False` then `45`"},
        {"option_id": "opt_d", "text": "`False` then `60`"},
    ],
    correct_ids=["opt_c"],
    option_feedback={
        "opt_a": {"message": "Inside `is_late`, `threshold = 60` creates a local variable. `50 > 60` is `False`, not `True`. And the global `threshold` stays `45`, not `60`."},
        "opt_b": {"message": "Inside `is_late`, `threshold = 60` is a local variable, so `50 > 60` is `False`, not `True`. The global `threshold` is indeed `45`."},
        "opt_c": {"message": "Correct. The assignment `threshold = 60` inside the function creates a local variable. `50 > 60` is `False`. The global `threshold` is unchanged at `45`."},
        "opt_d": {"message": "The assignment inside the function creates a local variable, not a global one. The global `threshold` stays `45`, not `60`."},
    },
    feedback={
        "correct": {"message": "Right — `threshold = 60` inside the function creates a local variable. It does not touch the global `threshold = 45`."},
        "incorrect": {"message": "An assignment inside a function stores the value in the function's local symbol table. The global `threshold` is unchanged."},
        "hints": [
            "Where does `threshold = 60` store its value — in the function's local table or in the global table?",
            "After the function returns, what value does the global `threshold` still hold?",
        ],
        "remediation_step_id": "tile_python_functions_scope.r05",
    },
)

# s19: check — recognize_when_global_statement_needed (f3)
s19 = choice(
    step_id="tile_python_functions_scope.s19",
    interaction_id="ix.tile_python_functions_scope.s19",
    difficulty="core",
    standalone=True,
    measures=[{
        "concept_id": "python.variable_scope",
        "capability": "recognize_when_global_statement_needed",
        "fact_ids": ["f3"],
    }],
    anchors=["python.variable_scope#assessment:recognize_when_global_statement_needed"],
    prompt=(
        "A script has a global variable `order_count = 0`. "
        "A function needs to **increment** `order_count` (i.e. assign a new value to it). "
        "Which statement must appear inside the function to make this work?"
    ),
    options=[
        {"option_id": "opt_a", "text": "`import order_count`"},
        {"option_id": "opt_b", "text": "`global order_count`"},
        {"option_id": "opt_c", "text": "`return order_count`"},
        {"option_id": "opt_d", "text": "No special statement is needed — assignment inside a function always changes the global."},
    ],
    correct_ids=["opt_b"],
    option_feedback={
        "opt_a": {"message": "`import` is for modules, not for accessing global variables. Use `global order_count` to allow assignment to the global name."},
        "opt_b": {"message": "Correct. `global order_count` tells Python that `order_count` inside this function refers to the global variable, so an assignment changes the global."},
        "opt_c": {"message": "`return` sends a value back to the caller but does not allow the function to assign to the global variable."},
        "opt_d": {"message": "Without `global order_count`, an assignment inside the function creates a new local variable instead of changing the global one."},
    },
    feedback={
        "correct": {"message": "Right — `global order_count` is required before any assignment to a global variable inside a function."},
        "incorrect": {"message": "Without a `global` statement, an assignment inside a function creates a local variable. To assign to the global, you must declare `global order_count` first."},
        "hints": [
            "A global variable can be *read* inside a function without any special statement. But what about *assigning* to it?",
            "There is a one-word Python keyword that tells a function 'this name refers to the global, not a new local'.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r06",
    },
)

# s20: hands_on — variable_scope practice
# Practice: Write a function that reads a global variable and, separately, assigns a local variable
#           with the same name without changing the global.
# Success: Inside the function the global is readable; the same-named local does not change the global's value outside.
# Starter: A global variable already assigned.
# Solution: threshold = 45; def check_delivery(minutes): threshold = 60; print(minutes > threshold); check_delivery(50); print(threshold)
# 50 > 60 = False; global threshold = 45
STARTER_S20 = (
    "# A global variable is set below.\n"
    "# Write a function called check_delivery(minutes) that:\n"
    "#   1. Assigns a LOCAL variable also called threshold with value 60\n"
    "#   2. Prints whether minutes > threshold (using the local threshold)\n"
    "# After defining and calling check_delivery(50),\n"
    "# print the global threshold to show it is unchanged.\n"
    "\n"
    "threshold = 45\n"
)
SOLUTION_S20 = (
    "threshold = 45\n"
    "\n"
    "def check_delivery(minutes):\n"
    "    threshold = 60\n"
    "    print(minutes > threshold)\n"
    "\n"
    "check_delivery(50)\n"
    "print(threshold)\n"
)
EXPECTED_STDOUT_S20 = "False\n45"

s20 = code_ex(
    step_id="tile_python_functions_scope.s20",
    interaction_id="ix.tile_python_functions_scope.s20",
    difficulty="stretch",
    standalone=False,
    measures=[{
        "concept_id": "python.variable_scope",
        "capability": "predict_name_resolution",
        "fact_ids": ["f1", "f2"],
    }],
    anchors=["python.variable_scope#practice"],
    prompt=(
        "A global variable `threshold = 45` is already set.\n\n"
        "Write a function `check_delivery(minutes)` that:\n"
        "1. Assigns a **local** variable also called `threshold` with value `60`\n"
        "2. Prints `minutes > threshold` (using the local `threshold`)\n\n"
        "After the definition, call `check_delivery(50)`, then print the global `threshold`.\n\n"
        "Expected output:\n```\nFalse\n45\n```\n\n"
        "The local `threshold` inside the function must not change the global `threshold`."
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S20,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_SCOPE,
    blocked_syntax=BLOCKED_SCOPE,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S20}],
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S20},
            "visible": True,
            "message_on_fail": "Expected 'False' then '45'. The local threshold=60 makes 50>60 False; the global threshold stays 45.",
        },
        {
            "test_id": "t2_global_threshold",
            "kind": "value_equals",
            "spec": {"expr": "threshold", "expected": 45},
            "visible": True,
            "message_on_fail": "The global `threshold` should still be `45` after calling `check_delivery`. Do not use `global threshold` inside the function.",
        },
    ],
    feedback={
        "correct": {"message": "Well done — the local `threshold = 60` inside the function did not change the global `threshold = 45`. Each assignment in a function goes to the local symbol table."},
        "incorrect": {"message": "Inside `check_delivery`, write `threshold = 60` (this creates a local variable). Then `print(minutes > threshold)`. After the call, `print(threshold)` should show the global value `45`."},
        "hints": [
            "An assignment inside a function always creates a local variable unless you use `global`. So `threshold = 60` inside the function is local.",
            "After the function call, `threshold` in the global scope is still `45` — the local assignment did not touch it.",
        ],
        "remediation_step_id": "tile_python_functions_scope.r05",
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# tile_python_errors_imports interactions
# ─────────────────────────────────────────────────────────────────────────────

# s02: check — handle_invalid_number_conversion (f3)
s_ei_02 = choice(
    step_id="tile_python_errors_imports.s02",
    interaction_id="ix.tile_python_errors_imports.s02",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.error_handling",
        "capability": "handle_invalid_number_conversion",
        "fact_ids": ["f3"],
    }],
    anchors=["python.error_handling#assessment:handle_invalid_number_conversion"],
    prompt=(
        "```python\ntry:\n    minutes = int('fast')\nexcept ValueError:\n    print('Not a valid number')\n```\n\n"
        "What does this code print?"
    ),
    options=[
        {"option_id": "opt_a", "text": "Nothing — the program crashes with a `ValueError`."},
        {"option_id": "opt_b", "text": "`Not a valid number`"},
        {"option_id": "opt_c", "text": "`0` — Python converts non-numeric strings to `0`."},
        {"option_id": "opt_d", "text": "`ValueError` — the exception message is printed automatically."},
    ],
    correct_ids=["opt_b"],
    option_feedback={
        "opt_a": {"message": "The `except ValueError:` clause catches the error, so the program does not crash. It prints the message instead."},
        "opt_b": {"message": "Correct. `int('fast')` raises a `ValueError`, which the `except ValueError:` clause catches, printing 'Not a valid number'."},
        "opt_c": {"message": "Python does not convert non-numeric strings to `0`. `int('fast')` raises a `ValueError`."},
        "opt_d": {"message": "Python does not automatically print exception messages. The `except` clause runs your code — in this case `print('Not a valid number')`."},
    },
    feedback={
        "correct": {"message": "Right — `int('fast')` raises a `ValueError`, the `except ValueError:` clause catches it, and the message is printed."},
        "incorrect": {"message": "When `int()` cannot convert a string, it raises a `ValueError`. The `except ValueError:` clause catches it and runs the code inside — here, printing the message."},
        "hints": [
            "What does `int('fast')` do? Can it convert the string 'fast' to an integer?",
            "When an exception matches the `except` clause, the clause's body runs instead of crashing.",
        ],
        "remediation_step_id": "tile_python_errors_imports.r01",
    },
)

# s03: hands_on — error_handling practice
# Practice: Convert user input to a number inside try/except and print a friendly message if the conversion fails.
# Success: Valid input is converted and used; invalid input prints the message instead of crashing.
# NOTE: input() is allowed but we cannot test interactive input in the sandbox.
# We use a pre-assigned string variable raw_input as the "input" to make it testable.
# The starter assigns raw_input = '55' (valid) and the solution converts it.
# For the hidden check, assemble will mutate raw_input via set_variable.
STARTER_S03_EI = (
    "# raw_input simulates what a user typed.\n"
    "# Wrap the int() conversion in try/except ValueError.\n"
    "# If conversion succeeds, print the integer value.\n"
    "# If it fails, print: 'Not a valid number'\n"
    "\n"
    "raw_input = '55'\n"
)
SOLUTION_S03_EI = (
    "raw_input = '55'\n"
    "\n"
    "try:\n"
    "    minutes = int(raw_input)\n"
    "    print(minutes)\n"
    "except ValueError:\n"
    "    print('Not a valid number')\n"
)
# With raw_input = '55', int('55') = 55, prints 55
EXPECTED_STDOUT_S03_EI = "55"

s_ei_03 = code_ex(
    step_id="tile_python_errors_imports.s03",
    interaction_id="ix.tile_python_errors_imports.s03",
    difficulty="core",
    standalone=False,
    measures=[
        {
            "concept_id": "python.error_handling",
            "capability": "wrap_code_in_try_except",
            "fact_ids": ["f1", "f2"],
        },
        {
            "concept_id": "python.error_handling",
            "capability": "handle_invalid_number_conversion",
            "fact_ids": ["f3"],
        },
    ],
    anchors=[
        "python.error_handling#practice",
        "python.error_handling#assessment:wrap_code_in_try_except",
        "python.error_handling#assessment:handle_invalid_number_conversion",
    ],
    prompt=(
        "`raw_input` holds a string that may or may not be a valid integer.\n\n"
        "Wrap `int(raw_input)` in a `try`/`except ValueError` block:\n"
        "- If the conversion succeeds, print the integer value.\n"
        "- If it raises a `ValueError`, print exactly: `Not a valid number`\n\n"
        "With `raw_input = '55'`, the output should be `55`."
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S03_EI,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_ERROR,
    blocked_syntax=BLOCKED_ERROR,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S03_EI}],
    tests=[
        {
            "test_id": "t1_valid_input",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S03_EI},
            "visible": True,
            "message_on_fail": "With raw_input='55', the program should print `55`. Make sure you print the converted integer inside the try block.",
        }
    ],
    feedback={
        "correct": {"message": "Well done — the `try` block converts the string and the `except ValueError` clause catches any conversion failure gracefully."},
        "incorrect": {"message": "Write `try:` then `minutes = int(raw_input)` and `print(minutes)` indented under it. Then `except ValueError:` and `print('Not a valid number')` indented under that."},
        "hints": [
            "The `try:` block contains the code that might fail. Put `int(raw_input)` and the print inside it.",
            "The `except ValueError:` block runs only when `int()` raises a ValueError. Put your error message print there.",
        ],
        "remediation_step_id": "tile_python_errors_imports.r01",
    },
)

# s05: check — write_correct_import_statement (f1, f2, f3)
s_ei_05 = choice(
    step_id="tile_python_errors_imports.s05",
    interaction_id="ix.tile_python_errors_imports.s05",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.import_statements",
        "capability": "write_correct_import_statement",
        "fact_ids": ["f1", "f2", "f3"],
    }],
    anchors=["python.import_statements#assessment:write_correct_import_statement"],
    prompt=(
        "After running `import fibo`, how do you call the `fib` function from that module?"
    ),
    options=[
        {"option_id": "opt_a", "text": "`fib(1000)` — `import fibo` adds `fib` directly to the namespace."},
        {"option_id": "opt_b", "text": "`fibo.fib(1000)` — the module name is the prefix."},
        {"option_id": "opt_c", "text": "`import fibo.fib(1000)` — you import and call in one step."},
        {"option_id": "opt_d", "text": "`fibo(fib, 1000)` — you pass the function name as an argument."},
    ],
    correct_ids=["opt_b"],
    option_feedback={
        "opt_a": {"message": "`import fibo` adds the module name `fibo` to the namespace, not the names inside it. To call `fib` directly, you would need `from fibo import fib`."},
        "opt_b": {"message": "Correct. `import fibo` adds the module name `fibo`. Its functions are accessed through that name: `fibo.fib(1000)`."},
        "opt_c": {"message": "`import` is a statement, not a function call. You import the module first, then call its functions separately."},
        "opt_d": {"message": "Python does not use this syntax. After `import fibo`, call the function as `fibo.fib(1000)`."},
    },
    feedback={
        "correct": {"message": "Right — `import fibo` adds the module name. Functions inside it are accessed as `fibo.fib(1000)`."},
        "incorrect": {"message": "`import fibo` adds the module name `fibo` to the namespace. To call a function inside it, use `fibo.fib(1000)` — the module name as a prefix."},
        "hints": [
            "What does `import fibo` add to the namespace — the module name, or all the names inside the module?",
            "To access a name inside a module, use the dot notation: `module_name.function_name()`.",
        ],
        "remediation_step_id": "tile_python_errors_imports.r02",
    },
)

# s06: hands_on — import_statements practice
# Practice: Import the math module and use one of its functions through the module name.
# Success: The import line appears at the top and a module function is called as math.name(...).
# Starter: empty file with a comment naming the function to call (sqrt).
# Solution: import math; result = math.sqrt(144); print(result)
# math.sqrt(144) = 12.0
STARTER_S06_EI = (
    "# Import the math module and call math.sqrt(144).\n"
    "# Store the result in a variable called result and print it.\n"
)
SOLUTION_S06_EI = (
    "import math\n"
    "\n"
    "result = math.sqrt(144)\n"
    "print(result)\n"
)
EXPECTED_STDOUT_S06_EI = "12.0"

s_ei_06 = code_ex(
    step_id="tile_python_errors_imports.s06",
    interaction_id="ix.tile_python_errors_imports.s06",
    difficulty="core",
    standalone=False,
    measures=[{
        "concept_id": "python.import_statements",
        "capability": "import_standard_module",
        "fact_ids": ["f4"],
    }],
    anchors=[
        "python.import_statements#practice",
        "python.import_statements#assessment:import_standard_module",
    ],
    prompt=(
        "Import the `math` standard module and call `math.sqrt(144)`.\n\n"
        "Store the result in a variable called `result` and print it.\n\n"
        "Expected output: `12.0`"
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S06_EI,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_IMPORT,
    blocked_syntax=BLOCKED_IMPORT,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S06_EI}],
    tests=[
        {
            "test_id": "t1_result",
            "kind": "value_equals",
            "spec": {"expr": "result", "expected": 12.0, "tolerance": 1e-9},
            "visible": True,
            "message_on_fail": "`result` should hold `12.0` (math.sqrt(144)). Make sure you import math and call math.sqrt(144).",
        },
        {
            "test_id": "t2_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S06_EI},
            "visible": True,
            "message_on_fail": "The program should print `12.0`. Check that you call `print(result)` after the assignment.",
        },
    ],
    feedback={
        "correct": {"message": "Well done — `import math` adds the module name, and `math.sqrt(144)` calls the function through that name."},
        "incorrect": {"message": "Write `import math` at the top, then `result = math.sqrt(144)`, then `print(result)`."},
        "hints": [
            "The import statement goes at the top: `import math`.",
            "After importing, call the function as `math.sqrt(144)` — the module name is the prefix.",
        ],
        "remediation_step_id": "tile_python_errors_imports.r02",
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# tile_python_file_io interactions
# ─────────────────────────────────────────────────────────────────────────────

# s04: check — open_read_and_write_text_file (f1, f3, f5)
s_fio_04 = choice(
    step_id="tile_python_file_io.s04",
    interaction_id="ix.tile_python_file_io.s04",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.file_io",
        "capability": "open_read_and_write_text_file",
        "fact_ids": ["f1", "f3", "f5"],
    }],
    anchors=["python.file_io#assessment:open_read_and_write_text_file"],
    prompt=(
        "Which mode string opens a file for **writing** (creating it if it does not exist, "
        "and erasing it if it does)?"
    ),
    options=[
        {"option_id": "opt_a", "text": "`'r'`"},
        {"option_id": "opt_b", "text": "`'a'`"},
        {"option_id": "opt_c", "text": "`'w'`"},
        {"option_id": "opt_d", "text": "No mode argument — `open()` defaults to write mode."},
    ],
    correct_ids=["opt_c"],
    option_feedback={
        "opt_a": {"message": "`'r'` opens a file for reading. It raises an error if the file does not exist and does not erase existing content."},
        "opt_b": {"message": "`'a'` opens a file for appending — it adds to the end of an existing file rather than erasing it."},
        "opt_c": {"message": "Correct. `'w'` opens a file for writing. It creates the file if it does not exist and erases any existing content."},
        "opt_d": {"message": "Omitting the mode defaults to `'r'` (read), not write. To write, you must pass `'w'` explicitly."},
    },
    feedback={
        "correct": {"message": "Right — `'w'` mode creates the file if needed and erases existing content before writing."},
        "incorrect": {"message": "The three main modes are `'r'` (read), `'w'` (write, erasing existing content), and `'a'` (append). Writing from scratch uses `'w'`."},
        "hints": [
            "Think about what the first letter of each mode stands for: r=read, w=write, a=append.",
            "Which mode would erase an existing file's contents before writing new data?",
        ],
        "remediation_step_id": "tile_python_file_io.r01",
    },
)

# s05: check — manage_file_with_with_statement (f2)
s_fio_05 = choice(
    step_id="tile_python_file_io.s05",
    interaction_id="ix.tile_python_file_io.s05",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.file_io",
        "capability": "manage_file_with_with_statement",
        "fact_ids": ["f2"],
    }],
    anchors=["python.file_io#assessment:manage_file_with_with_statement"],
    prompt=(
        "What is the main advantage of using `with open('orders.txt', 'r') as f:` "
        "instead of `f = open('orders.txt', 'r')`?"
    ),
    options=[
        {"option_id": "opt_a", "text": "It reads the file faster."},
        {"option_id": "opt_b", "text": "It closes the file automatically when the block finishes, even if an exception is raised."},
        {"option_id": "opt_c", "text": "It prevents other programs from reading the file at the same time."},
        {"option_id": "opt_d", "text": "It loads the entire file into memory before the block starts."},
    ],
    correct_ids=["opt_b"],
    option_feedback={
        "opt_a": {"message": "The `with` statement does not affect read speed. Its purpose is automatic resource management."},
        "opt_b": {"message": "Correct. The `with` statement closes the file automatically when the block ends, even if an exception is raised inside the block."},
        "opt_c": {"message": "The `with` statement does not lock the file for exclusive access. Its purpose is to ensure the file is closed when the block exits."},
        "opt_d": {"message": "The `with` statement does not preload the file. It simply ensures the file object is closed when the block finishes."},
    },
    feedback={
        "correct": {"message": "Right — `with open(...)` guarantees the file is closed when the block exits, even if an exception occurs."},
        "incorrect": {"message": "The `with` keyword is about automatic cleanup: it closes the file when the block ends, even if an exception is raised."},
        "hints": [
            "What happens to a file opened with `f = open(...)` if an exception occurs before `f.close()` is called?",
            "The `with` statement handles cleanup automatically — what resource does it clean up here?",
        ],
        "remediation_step_id": "tile_python_file_io.r02",
    },
)

# s06: hands_on — file_io practice (csv.DictReader)
# Practice: Read a CSV file's rows into a list of dicts using the csv module.
# Success: The list holds one dict per data row, keyed by the header names.
# Asset: ds_orders (dataset) mounted as orders.csv
# The dataset has columns: order_id, city, delivery_minutes, is_late, driver_id (5 columns)
# Solution: import csv; rows = []; with open('orders.csv', newline='') as f: reader = csv.DictReader(f); for row in reader: rows.append(row); print(len(rows))
# ds_orders has 15 rows
STARTER_S06_FIO = (
    "import csv\n"
    "\n"
    "# Read orders.csv using csv.DictReader.\n"
    "# Collect all rows into a list called rows.\n"
    "# Then print the number of rows.\n"
    "\n"
    "rows = []\n"
)
SOLUTION_S06_FIO = (
    "import csv\n"
    "\n"
    "rows = []\n"
    "with open('orders.csv', newline='') as f:\n"
    "    reader = csv.DictReader(f)\n"
    "    for row in reader:\n"
    "        rows.append(row)\n"
    "\n"
    "print(len(rows))\n"
)
# ds_orders has 15 data rows
EXPECTED_STDOUT_S06_FIO = "15"

s_fio_06 = code_ex(
    step_id="tile_python_file_io.s06",
    interaction_id="ix.tile_python_file_io.s06",
    difficulty="core",
    standalone=False,
    measures=[{
        "concept_id": "python.file_io",
        "capability": "read_and_write_csv_rows_as_dicts",
        "fact_ids": ["f4", "f6", "f7"],
    }],
    anchors=[
        "python.file_io#practice",
        "python.file_io#assessment:read_and_write_csv_rows_as_dicts",
    ],
    prompt=(
        "Read `orders.csv` using `csv.DictReader` and collect all rows into a list called `rows`.\n\n"
        "Open the file with `newline=''` as required by the csv module.\n"
        "Use a `for` loop to append each row dict to `rows`.\n"
        "After the loop, print `len(rows)`.\n\n"
        "Expected output: `15`"
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S06_FIO,
    }],
    entry="solution.py",
    asset_mounts=[{
        "asset_id": "ds_orders",
        "mount_path": "orders.csv",
    }],
    allowed_syntax=ALLOWED_FILEIO,
    blocked_syntax=BLOCKED_FILEIO,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S06_FIO}],
    tests=[
        {
            "test_id": "t1_row_count",
            "kind": "value_equals",
            "spec": {"expr": "len(rows)", "expected": 15},
            "visible": True,
            "message_on_fail": "`len(rows)` should be `15` — one dict per data row in orders.csv. Make sure you loop through all rows and append each one.",
        },
        {
            "test_id": "t2_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S06_FIO},
            "visible": True,
            "message_on_fail": "The program should print `15`. Check that you call `print(len(rows))` after the loop.",
        },
    ],
    feedback={
        "correct": {"message": "Well done — `csv.DictReader` mapped each row to a dict keyed by the header names, and you collected all 15 rows."},
        "incorrect": {"message": "Use `with open('orders.csv', newline='') as f:` then `reader = csv.DictReader(f)` then `for row in reader: rows.append(row)`."},
        "hints": [
            "Open the file with `newline=''` as the third argument to `open()`. This is required by the csv module.",
            "Inside the `with` block, create `reader = csv.DictReader(f)` and loop: `for row in reader: rows.append(row)`.",
        ],
        "remediation_step_id": "tile_python_file_io.r01",
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# tile_python_pep8_style interactions
# ─────────────────────────────────────────────────────────────────────────────

# s02: check — remove_extraneous_whitespace (f3)
s_pep_02 = choice(
    step_id="tile_python_pep8_style.s02",
    interaction_id="ix.tile_python_pep8_style.s02",
    difficulty="intro",
    standalone=True,
    measures=[{
        "concept_id": "python.pep8_style",
        "capability": "remove_extraneous_whitespace",
        "fact_ids": ["f3"],
    }],
    anchors=["python.pep8_style#assessment:remove_extraneous_whitespace"],
    prompt=(
        "Which line follows PEP 8's rule about extraneous whitespace?\n\n"
        "```python\n# A\nresult = compute( x , y )\n\n# B\nresult = compute(x, y)\n\n"
        "# C\nresult = compute(x ,y)\n\n# D\nresult = compute( x,y )\n```"
    ),
    options=[
        {"option_id": "opt_a", "text": "A — spaces inside the parentheses make it easier to read."},
        {"option_id": "opt_b", "text": "B — no spaces immediately inside parentheses or before commas."},
        {"option_id": "opt_c", "text": "C — one space before the comma is acceptable."},
        {"option_id": "opt_d", "text": "D — spaces inside parentheses are fine as long as they are symmetric."},
    ],
    correct_ids=["opt_b"],
    option_feedback={
        "opt_a": {"message": "PEP 8 says to avoid spaces immediately inside parentheses. `compute( x , y )` has extraneous spaces inside the parentheses and before the comma."},
        "opt_b": {"message": "Correct. PEP 8 recommends no spaces immediately inside parentheses and no space before a comma: `compute(x, y)`."},
        "opt_c": {"message": "PEP 8 says to avoid a space immediately before a comma. The correct form is `compute(x, y)` — space after the comma, not before."},
        "opt_d": {"message": "Symmetry does not make extraneous whitespace acceptable. PEP 8 says no spaces immediately inside parentheses."},
    },
    feedback={
        "correct": {"message": "Right — PEP 8 says no spaces immediately inside parentheses and no space before a comma: `compute(x, y)`."},
        "incorrect": {"message": "PEP 8 avoids extraneous whitespace: no spaces immediately inside parentheses `()`, `[]`, `{}`, and no space immediately before a comma, semicolon, or colon."},
        "hints": [
            "PEP 8 says: avoid whitespace immediately inside parentheses, brackets, or braces.",
            "Also avoid a space immediately before a comma. The correct pattern is `f(x, y)` — space after the comma, not before.",
        ],
        "remediation_step_id": "tile_python_pep8_style.r01",
    },
)

# s03: hands_on — pep8_style practice
# Practice: Rewrite a working but poorly styled function to follow PEP 8 naming and spacing conventions.
# Success: The rewritten code behaves identically and follows 4-space indentation, 79-character lines,
#          tidy whitespace and lowercase_with_underscores names.
# Starter: A short, working but badly styled snippet.
# Solution: properly styled version.
# The function_call test needs TWO calls with different args to avoid the hard-coded answer check.
STARTER_S03_PEP = (
    "# Rewrite this function to follow PEP 8:\n"
    "#   - Use 4-space indentation\n"
    "#   - Use lowercase_with_underscores for the function and variable names\n"
    "#   - Remove extraneous whitespace inside parentheses and before commas\n"
    "# The function must still return the same value.\n"
    "\n"
    "def CalcFee( minutes,rate ):\n"
    "  Fee=minutes*rate\n"
    "  return Fee\n"
    "\n"
    "print( CalcFee( 30,2 ) )\n"
)
SOLUTION_S03_PEP = (
    "def calc_fee(minutes, rate):\n"
    "    fee = minutes * rate\n"
    "    return fee\n"
    "\n"
    "print(calc_fee(30, 2))\n"
)
# 30 * 2 = 60
EXPECTED_STDOUT_S03_PEP = "60"

s_pep_03 = code_ex(
    step_id="tile_python_pep8_style.s03",
    interaction_id="ix.tile_python_pep8_style.s03",
    difficulty="core",
    standalone=False,
    measures=[
        {
            "concept_id": "python.pep8_style",
            "capability": "apply_indentation_and_line_length",
            "fact_ids": ["f1", "f2"],
        },
        {
            "concept_id": "python.pep8_style",
            "capability": "apply_naming_convention",
            "fact_ids": ["f4"],
        },
    ],
    anchors=[
        "python.pep8_style#practice",
        "python.pep8_style#assessment:apply_indentation_and_line_length",
        "python.pep8_style#assessment:apply_naming_convention",
    ],
    prompt=(
        "Rewrite the function below to follow PEP 8:\n\n"
        "```python\ndef CalcFee( minutes,rate ):\n  Fee=minutes*rate\n  return Fee\n\nprint( CalcFee( 30,2 ) )\n```\n\n"
        "Apply these changes:\n"
        "1. Rename `CalcFee` → `calc_fee` (lowercase with underscores)\n"
        "2. Rename `Fee` → `fee` (lowercase)\n"
        "3. Use **4-space** indentation (not 2 spaces)\n"
        "4. Remove extraneous spaces inside `()` and before `,`\n\n"
        "The function must still return `minutes * rate` and the print should output `60` when called with `30` and `2`."
    ),
    runtime_packages=None,
    files=[{
        "path": "solution.py",
        "role": "editable",
        "language": "python",
        "content": STARTER_S03_PEP,
    }],
    entry="solution.py",
    asset_mounts=None,
    allowed_syntax=ALLOWED_PEP8,
    blocked_syntax=BLOCKED_PEP8,
    solution_files=[{"path": "solution.py", "content": SOLUTION_S03_PEP}],
    tests=[
        {
            "test_id": "t1_stdout",
            "kind": "stdout_equals",
            "spec": {"expected": EXPECTED_STDOUT_S03_PEP},
            "visible": True,
            "message_on_fail": "The restyled function should still print `60` when called with `30` and `2`.",
        },
        {
            "test_id": "t2_function_call_30_2",
            "kind": "function_call",
            "spec": {
                "function": "calc_fee",
                "args": [30, 2],
                "expected": 60,
            },
            "visible": True,
            "message_on_fail": "`calc_fee(30, 2)` should return `60`. Make sure the function is named `calc_fee` and returns `minutes * rate`.",
        },
        {
            "test_id": "t3_function_call_45_3",
            "kind": "function_call",
            "spec": {
                "function": "calc_fee",
                "args": [45, 3],
                "expected": 135,
            },
            "visible": True,
            "message_on_fail": "`calc_fee(45, 3)` should return `135`. Make sure the function computes `minutes * rate`.",
        },
    ],
    feedback={
        "correct": {"message": "Well done — the restyled code uses 4-space indentation, lowercase_with_underscores names, and no extraneous whitespace."},
        "incorrect": {"message": "Check: (1) function name `calc_fee`, (2) variable name `fee`, (3) 4 spaces of indentation, (4) no spaces inside `()` or before `,`."},
        "hints": [
            "PEP 8 names use lowercase letters and underscores: `CalcFee` becomes `calc_fee`, `Fee` becomes `fee`.",
            "Replace the 2-space indentation with 4 spaces, and remove the spaces inside `( )` and before `,`.",
        ],
        "remediation_step_id": "tile_python_pep8_style.r01",
    },
)

# ─────────────────────────────────────────────────────────────────────────────
# Assemble the part file
# ─────────────────────────────────────────────────────────────────────────────

part = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_008_da_python_core",
    "tiles": [
        {
            "tile_id": "tile_python_functions_scope",
            "interactions": [s02, s03, s05, s06, s09, s10, s13, s14, s18, s19, s20],
        },
        {
            "tile_id": "tile_python_errors_imports",
            "interactions": [s_ei_02, s_ei_03, s_ei_05, s_ei_06],
        },
        {
            "tile_id": "tile_python_file_io",
            "interactions": [s_fio_04, s_fio_05, s_fio_06],
        },
        {
            "tile_id": "tile_python_pep8_style",
            "interactions": [s_pep_02, s_pep_03],
        },
    ],
}

with open('batches/final_batch_008_da_python_core/interactions.part.c3.json', 'w') as f:
    json.dump(part, f, indent=2)

print("Written interactions.part.c3.json")
print("Interaction counts:")
for tile in part['tiles']:
    print(f"  {tile['tile_id']}: {len(tile['interactions'])} interactions")
    for i in tile['interactions']:
        print(f"    {i['step_id']}: {i['interaction']['type']}")
