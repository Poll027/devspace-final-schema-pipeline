"""
Build interactions.part.c2.json for tiles:
  tile_python_conditionals_for_loops
  tile_python_while_loop_control
  tile_python_comprehensions_iterating
"""
import json

PYTHON_VERSION = "0.29.5"

# ── helpers ──────────────────────────────────────────────────────────────────

def ix_id(step_id):
    return f"ix.{step_id}"

# ── tile_python_conditionals_for_loops ───────────────────────────────────────

# s02 check: explain_when_if_block_runs  (fact f1, intro)
s02 = {
    "step_id": "tile_python_conditionals_for_loops.s02",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_python_conditionals_for_loops.s02"),
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": True,
        "measures": [
            {
                "concept_id": "python.conditional_statements",
                "capability": "explain_when_if_block_runs",
                "fact_ids": ["f1"]
            }
        ],
        "anchors": [
            "python.conditional_statements#assessment:explain_when_if_block_runs"
        ],
        "public": {
            "prompt": (
                "When does the body of an `if` statement execute?\n\n"
                "```python\n"
                "delivery_minutes = 30\n"
                "if delivery_minutes > 45:\n"
                "    print('late')\n"
                "```"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "Only when its condition is true"
                },
                {
                    "option_id": "opt_b",
                    "text": "Every time the program runs, regardless of the condition"
                },
                {
                    "option_id": "opt_c",
                    "text": "Only when its condition is false"
                },
                {
                    "option_id": "opt_d",
                    "text": "Only when the variable equals zero"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. An `if` statement executes its block only when its condition is true. Here `30 > 45` is false, so `print('late')` is skipped."
                },
                "opt_b": {
                    "message": "The body only runs when the condition is true, not unconditionally. If you need code to always run, place it outside the `if` block."
                },
                "opt_c": {
                    "message": "That is the opposite of how `if` works. The body runs when the condition is true; when it is false the body is skipped."
                },
                "opt_d": {
                    "message": "The `if` body runs when its condition evaluates to true — not specifically when a variable equals zero. Any true condition triggers it."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Right — an `if` block runs only when its condition is true. Since `30 > 45` is false, `print('late')` is skipped entirely."
            },
            "incorrect": {
                "message": "An `if` statement executes its block only when its condition is true. If the condition is false, Python skips the indented block and moves on."
            },
            "hints": [
                "Evaluate `30 > 45` — is that true or false?",
                "What does Python do with the indented block when the condition is false?"
            ],
            "remediation_step_id": "tile_python_conditionals_for_loops.s01"
        }
    }
}

# s03 check: predict_branch_taken  (fact f3, core)
s03 = {
    "step_id": "tile_python_conditionals_for_loops.s03",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_python_conditionals_for_loops.s03"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": True,
        "measures": [
            {
                "concept_id": "python.conditional_statements",
                "capability": "predict_branch_taken",
                "fact_ids": ["f3"]
            }
        ],
        "anchors": [
            "python.conditional_statements#assessment:predict_branch_taken"
        ],
        "public": {
            "prompt": (
                "What does this code print when `delivery_minutes = 30`?\n\n"
                "```python\n"
                "delivery_minutes = 30\n"
                "if delivery_minutes < 15:\n"
                "    category = 'fast'\n"
                "elif delivery_minutes < 45:\n"
                "    category = 'normal'\n"
                "else:\n"
                "    category = 'slow'\n"
                "print(category)\n"
                "```"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "`normal`"
                },
                {
                    "option_id": "opt_b",
                    "text": "`fast`"
                },
                {
                    "option_id": "opt_c",
                    "text": "`slow`"
                },
                {
                    "option_id": "opt_d",
                    "text": "Both `normal` and `slow` — two conditions are checked"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. `30 < 15` is false, so the `if` branch is skipped. `30 < 45` is true, so the `elif` branch runs and `category` is set to `'normal'`."
                },
                "opt_b": {
                    "message": "The `if` condition `30 < 15` is false, so the `fast` branch is skipped. Python moves to the `elif`."
                },
                "opt_c": {
                    "message": "The `else` branch only runs when all earlier conditions are false. Here `30 < 45` is true, so the `elif` branch runs first and `else` is skipped."
                },
                "opt_d": {
                    "message": "An if/elif/else chain selects exactly one branch — the first whose condition is true. Once `30 < 45` matches, no further branches are evaluated."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Correct. Python evaluates conditions top to bottom and runs the first true branch. `30 < 15` is false; `30 < 45` is true, so `category = 'normal'`."
            },
            "incorrect": {
                "message": "Evaluate each condition in order: `30 < 15` is false (skip `fast`); `30 < 45` is true (run `normal`). The chain stops there — `else` is never reached."
            },
            "hints": [
                "Is `30 < 15` true or false? What happens to that branch?",
                "After the `if` is skipped, Python checks the `elif`. Is `30 < 45` true?"
            ],
            "remediation_step_id": "tile_python_conditionals_for_loops.s01"
        }
    }
}

# s04 hands_on: code_exercise — write_if_elif_else_chain  (facts f2,f3,f4, core)
# Practice anchor: classify delivery_minutes into fast/normal/slow
# Starter: delivery_minutes = 38  (38+7=45 → 'slow', so result changes on mutation)
# Solution: if/elif/else; print(category)
# stdout: "normal"
COND_ALLOWED = [
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
    "f-strings f\"...{expr}...\"",
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block"
]
COND_BLOCKED = [
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
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy"
]

s04 = {
    "step_id": "tile_python_conditionals_for_loops.s04",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": ix_id("tile_python_conditionals_for_loops.s04"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "python.conditional_statements",
                "capability": "write_if_elif_else_chain",
                "fact_ids": ["f2", "f3", "f4"]
            }
        ],
        "anchors": [
            "python.conditional_statements#practice",
            "python.conditional_statements#assessment:write_if_elif_else_chain"
        ],
        "public": {
            "prompt": (
                "QuickDeliver classifies each order by speed.\n\n"
                "`delivery_minutes` is already assigned below.\n\n"
                "Add an `if`/`elif`/`else` chain that sets `category` to:\n"
                "- `'fast'` when `delivery_minutes < 15`\n"
                "- `'normal'` when `delivery_minutes < 45`\n"
                "- `'slow'` otherwise\n\n"
                "Then print `category`.\n\n"
                "Expected output for the starter value:\n"
                "```\n"
                "normal\n"
                "```"
            ),
            "runtime": {
                "kind": "python",
                "version": PYTHON_VERSION
            },
            "workspace": {
                "files": [
                    {
                        "path": "solution.py",
                        "role": "editable",
                        "language": "python",
                        "content": (
                            "delivery_minutes = 38\n"
                            "# Write your if/elif/else chain here\n"
                        )
                    }
                ],
                "entry": "solution.py"
            },
            "constraints": {
                "allowed_syntax": COND_ALLOWED,
                "blocked_syntax": COND_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "solution.py",
                    "content": (
                        "delivery_minutes = 38\n"
                        "if delivery_minutes < 15:\n"
                        "    category = 'fast'\n"
                        "elif delivery_minutes < 45:\n"
                        "    category = 'normal'\n"
                        "else:\n"
                        "    category = 'slow'\n"
                        "print(category)\n"
                    )
                }
            ],
            "tests": [
                {
                    "test_id": "t1_stdout",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "normal"
                    },
                    "visible": True,
                    "message_on_fail": "Expected output `normal` for delivery_minutes = 38. Check your elif condition."
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": "Well done — exactly one branch ran and printed `normal` for `delivery_minutes = 38`."
            },
            "incorrect": {
                "message": "Check that your chain has `if delivery_minutes < 15`, `elif delivery_minutes < 45`, and `else`, each ending with a colon and an indented body."
            },
            "hints": [
                "Each branch header ends with a colon, and the body is indented four spaces beneath it.",
                "Only one branch runs — the first whose condition is true. For `38`, which condition is true first?"
            ],
            "remediation_step_id": "tile_python_conditionals_for_loops.s01"
        }
    }
}

# s07 check: trace_loop_variable_each_pass  (fact f2, intro)
s07 = {
    "step_id": "tile_python_conditionals_for_loops.s07",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_python_conditionals_for_loops.s07"),
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": True,
        "measures": [
            {
                "concept_id": "python.for_loops",
                "capability": "trace_loop_variable_each_pass",
                "fact_ids": ["f2"]
            }
        ],
        "anchors": [
            "python.for_loops#assessment:trace_loop_variable_each_pass"
        ],
        "public": {
            "prompt": (
                "What does `minutes` equal on the **second** pass of this loop?\n\n"
                "```python\n"
                "delivery_times = [32, 45, 21]\n"
                "for minutes in delivery_times:\n"
                "    print(minutes)\n"
                "```"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "`45`"
                },
                {
                    "option_id": "opt_b",
                    "text": "`32`"
                },
                {
                    "option_id": "opt_c",
                    "text": "`21`"
                },
                {
                    "option_id": "opt_d",
                    "text": "`1` — the index of the second item"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. On the first pass `minutes` is `32`, on the second pass it is `45`, and on the third it is `21`."
                },
                "opt_b": {
                    "message": "`32` is the value on the first pass. Each pass binds the loop variable to the next item in the sequence."
                },
                "opt_c": {
                    "message": "`21` is the value on the third (last) pass. The second pass binds `minutes` to `45`."
                },
                "opt_d": {
                    "message": "A `for` loop binds the loop variable to the item itself, not its index. To get the index you would need `enumerate()`, which has not been taught yet."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Right — each pass binds `minutes` to the next item in order: `32`, then `45`, then `21`."
            },
            "incorrect": {
                "message": "Each pass through a `for` loop binds the loop variable to the next item of the sequence in order. The second item in `[32, 45, 21]` is `45`."
            },
            "hints": [
                "List the items in `delivery_times` in order. Which one is at position 1 (the second item)?",
                "On each pass, `minutes` is set to the next item — not its index."
            ],
            "remediation_step_id": "tile_python_conditionals_for_loops.s05"
        }
    }
}

# s08 hands_on: code_exercise — write_for_loop_over_collection  (facts f1,f2,f3, core)
# Practice anchor: sum a list of delivery times
# delivery_times = [32, 45, 21, 60, 18, 27, 50, 13, 41, 36]  sum = 343
# total = 0 (scalar, gets mutated to 7 → but total is reset to 0 in solution anyway)
# Actually the list is the data — when a row is dropped/duplicated, sum changes
# But there's no mounted data. The list literal can't be mutated by py_var_mutations.
# However, total = 0 is a scalar that gets mutated to 7.
# With total = 7, the sum becomes 343 + 7 = 350. That's different from 343. ✓
FOR_ALLOWED = [
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
    "f-strings f\"...{expr}...\"",
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:"
]
FOR_BLOCKED = [
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
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy"
]

s08_cfl = {
    "step_id": "tile_python_conditionals_for_loops.s08",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": ix_id("tile_python_conditionals_for_loops.s08"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "python.for_loops",
                "capability": "write_for_loop_over_collection",
                "fact_ids": ["f1", "f2", "f3"]
            }
        ],
        "anchors": [
            "python.for_loops#practice",
            "python.for_loops#assessment:write_for_loop_over_collection"
        ],
        "public": {
            "prompt": (
                "QuickDeliver wants the total delivery time across all orders.\n\n"
                "`delivery_times` and `total` are already assigned below.\n\n"
                "Add a `for` loop that visits every item in `delivery_times` and adds it to `total` "
                "using a plain assignment (`total = total + minutes`).\n\n"
                "Then print `total`.\n\n"
                "Expected output:\n"
                "```\n"
                "343\n"
                "```"
            ),
            "runtime": {
                "kind": "python",
                "version": PYTHON_VERSION
            },
            "workspace": {
                "files": [
                    {
                        "path": "solution.py",
                        "role": "editable",
                        "language": "python",
                        "content": (
                            "delivery_times = [32, 45, 21, 60, 18, 27, 50, 13, 41, 36]\n"
                            "total = 0\n"
                            "# Write your for loop here\n"
                        )
                    }
                ],
                "entry": "solution.py"
            },
            "constraints": {
                "allowed_syntax": FOR_ALLOWED,
                "blocked_syntax": FOR_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "solution.py",
                    "content": (
                        "delivery_times = [32, 45, 21, 60, 18, 27, 50, 13, 41, 36]\n"
                        "total = 0\n"
                        "for minutes in delivery_times:\n"
                        "    total = total + minutes\n"
                        "print(total)\n"
                    )
                }
            ],
            "tests": [
                {
                    "test_id": "t1_stdout",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "343"
                    },
                    "visible": True,
                    "message_on_fail": "Expected output `343`. Make sure your loop adds each item to `total` and you print `total` after the loop."
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": "The loop visited all 10 items and the total is 343. Every item was processed exactly once."
            },
            "incorrect": {
                "message": "Make sure your `for` loop header ends with a colon, the body is indented, and you use `total = total + minutes` (not `+=`) to accumulate the sum."
            },
            "hints": [
                "The loop header is `for minutes in delivery_times:` — the body runs once per item.",
                "Inside the loop, update `total` with `total = total + minutes`, then print `total` after the loop ends."
            ],
            "remediation_step_id": "tile_python_conditionals_for_loops.s05"
        }
    }
}

# ── tile_python_while_loop_control ────────────────────────────────────────────

# s03 check: update_state_so_loop_terminates  (fact f2, intro)
s03_wlc = {
    "step_id": "tile_python_while_loop_control.s03",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_python_while_loop_control.s03"),
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": True,
        "measures": [
            {
                "concept_id": "python.while_loops",
                "capability": "update_state_so_loop_terminates",
                "fact_ids": ["f2"]
            }
        ],
        "anchors": [
            "python.while_loops#assessment:update_state_so_loop_terminates"
        ],
        "public": {
            "prompt": (
                "Why must the body of a `while` loop change the value its condition checks?\n\n"
                "```python\n"
                "pending = 3\n"
                "while pending > 0:\n"
                "    print('deliveries left:', pending)\n"
                "    pending = pending - 1\n"
                "```"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "So the condition eventually becomes false and the loop stops"
                },
                {
                    "option_id": "opt_b",
                    "text": "So the loop variable is available after the loop ends"
                },
                {
                    "option_id": "opt_c",
                    "text": "So Python knows how many times to repeat the loop"
                },
                {
                    "option_id": "opt_d",
                    "text": "So the condition is checked only once at the start"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. If the body never changes what the condition checks, the condition stays true forever and the loop never stops."
                },
                "opt_b": {
                    "message": "Variable availability is not the reason. The body must update the condition's variable so the condition can eventually become false and the loop can stop."
                },
                "opt_c": {
                    "message": "A `while` loop does not know in advance how many times it will run — that is the key difference from a `for` loop. It keeps going until the condition becomes false."
                },
                "opt_d": {
                    "message": "A `while` loop re-checks its condition before every pass, not just once. The body must change the variable so the condition can eventually become false."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Right — if nothing in the body changes what the condition checks, the condition stays true forever and the loop runs without stopping."
            },
            "incorrect": {
                "message": "A `while` loop re-checks its condition before every pass. If the body never changes the variable the condition tests, the condition stays true and the loop never ends."
            },
            "hints": [
                "What happens to `pending` on each pass? What would happen if that line were missing?",
                "A `while` loop stops only when its condition becomes false — what makes it false here?"
            ],
            "remediation_step_id": "tile_python_while_loop_control.s01"
        }
    }
}

# s04 hands_on: code_exercise — write_while_loop_with_condition  (fact f1, core)
# Practice anchor: while loop counting down pending
# pending = 3; while pending > 0: print; pending = pending - 1
# stdout: "deliveries left: 3\ndeliveries left: 2\ndeliveries left: 1"
# pending = 3 is a scalar → mutated to 10 → output changes ✓
WHILE_ALLOWED = [
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
    "f-strings f\"...{expr}...\"",
    "format specifier such as {value:.2f}",
    "if",
    "elif",
    "else",
    "colon and indented block",
    "for item in sequence:",
    "while condition:",
    "break",
    "continue"
]
WHILE_BLOCKED = [
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
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy"
]

s04_wlc = {
    "step_id": "tile_python_while_loop_control.s04",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": ix_id("tile_python_while_loop_control.s04"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "python.while_loops",
                "capability": "write_while_loop_with_condition",
                "fact_ids": ["f1"]
            }
        ],
        "anchors": [
            "python.while_loops#practice",
            "python.while_loops#assessment:write_while_loop_with_condition"
        ],
        "public": {
            "prompt": (
                "QuickDeliver's dispatcher tracks how many deliveries are still pending.\n\n"
                "`pending` is already assigned below.\n\n"
                "Add a `while` loop that:\n"
                "1. Runs as long as `pending > 0`\n"
                "2. Prints `'deliveries left:'` followed by the current value of `pending`\n"
                "3. Decreases `pending` by 1 each pass using `pending = pending - 1`\n\n"
                "Expected output:\n"
                "```\n"
                "deliveries left: 3\n"
                "deliveries left: 2\n"
                "deliveries left: 1\n"
                "```"
            ),
            "runtime": {
                "kind": "python",
                "version": PYTHON_VERSION
            },
            "workspace": {
                "files": [
                    {
                        "path": "solution.py",
                        "role": "editable",
                        "language": "python",
                        "content": (
                            "pending = 3\n"
                            "# Write your while loop here\n"
                        )
                    }
                ],
                "entry": "solution.py"
            },
            "constraints": {
                "allowed_syntax": WHILE_ALLOWED,
                "blocked_syntax": WHILE_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "solution.py",
                    "content": (
                        "pending = 3\n"
                        "while pending > 0:\n"
                        "    print('deliveries left:', pending)\n"
                        "    pending = pending - 1\n"
                    )
                }
            ],
            "tests": [
                {
                    "test_id": "t1_stdout",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "deliveries left: 3\ndeliveries left: 2\ndeliveries left: 1"
                    },
                    "visible": True,
                    "message_on_fail": "Expected three lines counting down from 3. Check your condition and the update step."
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": "The loop ran exactly 3 times and stopped once `pending` reached 0 — the condition became false."
            },
            "incorrect": {
                "message": "Make sure the `while` header is `while pending > 0:`, the body prints `pending`, and then decreases it with `pending = pending - 1`."
            },
            "hints": [
                "The loop header ends with a colon; the body is indented beneath it.",
                "Without `pending = pending - 1` inside the loop, `pending` never changes and the loop runs forever."
            ],
            "remediation_step_id": "tile_python_while_loop_control.s01"
        }
    }
}

# s06 check: skip_iteration_with_continue  (fact f2, core)
s06_wlc = {
    "step_id": "tile_python_while_loop_control.s06",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_python_while_loop_control.s06"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": True,
        "measures": [
            {
                "concept_id": "python.loop_control",
                "capability": "skip_iteration_with_continue",
                "fact_ids": ["f2"]
            }
        ],
        "anchors": [
            "python.loop_control#assessment:skip_iteration_with_continue"
        ],
        "public": {
            "prompt": (
                "What does this code print?\n\n"
                "```python\n"
                "delivery_times = [32, -5, 21]\n"
                "for minutes in delivery_times:\n"
                "    if minutes < 0:\n"
                "        continue\n"
                "    print(minutes)\n"
                "```"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "`32` and `21` — the negative value is skipped"
                },
                {
                    "option_id": "opt_b",
                    "text": "`32`, `-5`, and `21` — `continue` does not remove items"
                },
                {
                    "option_id": "opt_c",
                    "text": "`32` only — the loop stops when it hits `-5`"
                },
                {
                    "option_id": "opt_d",
                    "text": "Nothing — `continue` exits the loop immediately"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. `continue` skips the rest of the current iteration and moves to the next item. `-5 < 0` is true, so `print(-5)` is skipped; `32` and `21` are printed."
                },
                "opt_b": {
                    "message": "`continue` skips the remaining statements in the current iteration. When `minutes` is `-5`, `continue` jumps to the next item before `print` is reached."
                },
                "opt_c": {
                    "message": "`continue` does not stop the loop — it only skips the rest of the current iteration. `break` is the statement that exits the loop early."
                },
                "opt_d": {
                    "message": "`continue` does not exit the loop. It skips the rest of the current iteration and moves to the next item. `break` is what exits the loop entirely."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "`continue` skips the rest of the current iteration. For `-5`, the `print` is never reached; the loop continues with `21`."
            },
            "incorrect": {
                "message": "`continue` skips the remaining statements in the current pass and moves to the next item. It does not stop the loop — that is what `break` does."
            },
            "hints": [
                "When `minutes = -5`, the `if` condition is true. What does `continue` do at that point?",
                "After `continue`, does the loop end or does it move to the next item?"
            ],
            "remediation_step_id": "tile_python_while_loop_control.s05"
        }
    }
}

# s07 hands_on: code_exercise — exit_loop_early_with_break + skip_iteration_with_continue
# Practice anchor: for loop with break and continue
# delivery_times = [32, -5, 45, 21, 60, 18]; target = 45
# skip negatives with continue; break when target found
# stdout: "found: 45"
# target = 45 is a scalar → mutated to 52 → output changes (52 not in list → no output)
# Actually: target = 45 → mutated to 52. 52 is not in the list → no output.
# That's different from "found: 45". ✓
CTRL_ALLOWED = WHILE_ALLOWED  # same list (includes break, continue, for item in sequence:)
CTRL_BLOCKED = WHILE_BLOCKED

s07_wlc = {
    "step_id": "tile_python_while_loop_control.s07",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": ix_id("tile_python_while_loop_control.s07"),
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "python.loop_control",
                "capability": "exit_loop_early_with_break",
                "fact_ids": ["f1"]
            },
            {
                "concept_id": "python.loop_control",
                "capability": "skip_iteration_with_continue",
                "fact_ids": ["f2"]
            }
        ],
        "anchors": [
            "python.loop_control#practice",
            "python.loop_control#assessment:exit_loop_early_with_break",
            "python.loop_control#assessment:skip_iteration_with_continue"
        ],
        "public": {
            "prompt": (
                "QuickDeliver's script scans a list of delivery times to find a target value, "
                "skipping any invalid (negative) entries.\n\n"
                "`delivery_times` and `target` are already assigned below.\n\n"
                "Add a `for` loop that:\n"
                "1. Skips any item that is less than `0` using `continue`\n"
                "2. Prints `'found:'` followed by the item when it equals `target`, then stops the loop with `break`\n\n"
                "Expected output:\n"
                "```\n"
                "found: 45\n"
                "```"
            ),
            "runtime": {
                "kind": "python",
                "version": PYTHON_VERSION
            },
            "workspace": {
                "files": [
                    {
                        "path": "solution.py",
                        "role": "editable",
                        "language": "python",
                        "content": (
                            "delivery_times = [32, -5, 45, 21, 60, 18]\n"
                            "target = 45\n"
                            "# Write your for loop here\n"
                        )
                    }
                ],
                "entry": "solution.py"
            },
            "constraints": {
                "allowed_syntax": CTRL_ALLOWED,
                "blocked_syntax": CTRL_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "solution.py",
                    "content": (
                        "delivery_times = [32, -5, 45, 21, 60, 18]\n"
                        "target = 45\n"
                        "for minutes in delivery_times:\n"
                        "    if minutes < 0:\n"
                        "        continue\n"
                        "    if minutes == target:\n"
                        "        print('found:', minutes)\n"
                        "        break\n"
                    )
                }
            ],
            "tests": [
                {
                    "test_id": "t1_stdout",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "found: 45"
                    },
                    "visible": True,
                    "message_on_fail": "Expected output `found: 45`. Check that you skip negatives with `continue` and stop at the target with `break`."
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": "The loop skipped `-5` with `continue`, found `45`, printed it, and stopped — nothing after the match was processed."
            },
            "incorrect": {
                "message": "Use `continue` to skip items where `minutes < 0`, and `break` to stop the loop once `minutes == target`. Both must be inside the loop body."
            },
            "hints": [
                "Handle the invalid entry first: `if minutes < 0: continue` skips the rest of that pass.",
                "To stop at the target: `if minutes == target: print('found:', minutes)` then `break`."
            ],
            "remediation_step_id": "tile_python_while_loop_control.s05"
        }
    }
}

# ── tile_python_comprehensions_iterating ──────────────────────────────────────

# s02 check: write_dict_comprehension  (fact f3, core)
s02_ci = {
    "step_id": "tile_python_comprehensions_iterating.s02",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_python_comprehensions_iterating.s02"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": True,
        "measures": [
            {
                "concept_id": "python.comprehensions",
                "capability": "write_dict_comprehension",
                "fact_ids": ["f3"]
            }
        ],
        "anchors": [
            "python.comprehensions#assessment:write_dict_comprehension"
        ],
        "public": {
            "prompt": (
                "Which expression creates a dictionary that maps each number in "
                "`[2, 4, 6]` to its square?\n\n"
                "Expected result: `{2: 4, 4: 16, 6: 36}`"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "`{x: x**2 for x in [2, 4, 6]}`"
                },
                {
                    "option_id": "opt_b",
                    "text": "`[x: x**2 for x in [2, 4, 6]]`"
                },
                {
                    "option_id": "opt_c",
                    "text": "`{x**2 for x in [2, 4, 6]}`"
                },
                {
                    "option_id": "opt_d",
                    "text": "`{x**2: x for x in [2, 4, 6]}`"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. A dict comprehension uses `{key_expr: value_expr for var in iterable}`. Here `x` is the key and `x**2` is the value."
                },
                "opt_b": {
                    "message": "Square brackets `[...]` create a list, not a dictionary. A dict comprehension uses curly braces `{key: value for ...}`."
                },
                "opt_c": {
                    "message": "`{x**2 for x in [2, 4, 6]}` is a set comprehension — it produces a set of values, not a key-value dictionary. A dict comprehension needs `key: value` inside the braces."
                },
                "opt_d": {
                    "message": "This maps the square to the original number — the key and value are swapped. The prompt asks for `{number: square}`, so the key should be `x` and the value `x**2`."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Right — `{x: x**2 for x in [2, 4, 6]}` is a dict comprehension: curly braces, `key: value` expression, then the `for` clause."
            },
            "incorrect": {
                "message": "A dict comprehension uses `{key_expr: value_expr for var in iterable}` with curly braces and a colon separating key from value."
            },
            "hints": [
                "A dict comprehension starts with `{` and contains `key: value` before the `for` clause.",
                "Which part should be the key (the original number) and which the value (its square)?"
            ],
            "remediation_step_id": "tile_python_comprehensions_iterating.s01"
        }
    }
}

# s03 hands_on: code_exercise — write_list_comprehension + write_dict_comprehension
# Practice anchor: squares of even numbers
# numbers = [1, 2, 3, 4, 5, 6, 7, 8]; threshold = 2
# result = [x * x for x in numbers if x % threshold == 0]  → [4, 16, 36, 64]
# threshold = 2 is a scalar → mutated to 9 → result = [] (no multiples of 9 in 1-8) ✓
COMP_ALLOWED = [
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
    "f-strings f\"...{expr}...\"",
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
    "{k: v for ...}"
]
COMP_BLOCKED = [
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
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy"
]

s03_ci = {
    "step_id": "tile_python_comprehensions_iterating.s03",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": ix_id("tile_python_comprehensions_iterating.s03"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "python.comprehensions",
                "capability": "write_list_comprehension",
                "fact_ids": ["f1", "f2"]
            },
            {
                "concept_id": "python.comprehensions",
                "capability": "write_dict_comprehension",
                "fact_ids": ["f3"]
            }
        ],
        "anchors": [
            "python.comprehensions#practice",
            "python.comprehensions#assessment:write_list_comprehension",
            "python.comprehensions#assessment:write_dict_comprehension"
        ],
        "public": {
            "prompt": (
                "QuickDeliver wants to flag orders whose delivery time is even.\n\n"
                "`numbers` and `threshold` are already assigned below.\n\n"
                "Write a list comprehension that assigns to `result` the squares of only the numbers "
                "in `numbers` that are divisible by `threshold`, in the original order. "
                "Use `x * x` as the expression and `x % threshold == 0` as the filter.\n\n"
                "Then print `result`.\n\n"
                "Expected output:\n"
                "```\n"
                "[4, 16, 36, 64]\n"
                "```"
            ),
            "runtime": {
                "kind": "python",
                "version": PYTHON_VERSION
            },
            "workspace": {
                "files": [
                    {
                        "path": "solution.py",
                        "role": "editable",
                        "language": "python",
                        "content": (
                            "numbers = [1, 2, 3, 4, 5, 6, 7, 8]\n"
                            "threshold = 2\n"
                            "# Write your list comprehension here\n"
                        )
                    }
                ],
                "entry": "solution.py"
            },
            "constraints": {
                "allowed_syntax": COMP_ALLOWED,
                "blocked_syntax": COMP_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "solution.py",
                    "content": (
                        "numbers = [1, 2, 3, 4, 5, 6, 7, 8]\n"
                        "threshold = 2\n"
                        "result = [x * x for x in numbers if x % threshold == 0]\n"
                        "print(result)\n"
                    )
                }
            ],
            "tests": [
                {
                    "test_id": "t1_stdout",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "[4, 16, 36, 64]"
                    },
                    "visible": True,
                    "message_on_fail": "Expected `[4, 16, 36, 64]`. Check your expression (`x * x`), for clause, and if clause (`x % threshold == 0`)."
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": "The comprehension filtered to numbers divisible by `threshold` and squared each one — `[4, 16, 36, 64]`."
            },
            "incorrect": {
                "message": "A list comprehension has the form `[expression for var in iterable if condition]`. Use `x * x` as the expression and `x % threshold == 0` as the filter."
            },
            "hints": [
                "The structure is `[x * x for x in numbers if ...]` — fill in the filter condition using `threshold`.",
                "A number divisible by `threshold` has no remainder: `x % threshold == 0`."
            ],
            "remediation_step_id": "tile_python_comprehensions_iterating.s01"
        }
    }
}

# s05 check: recognize_unordered_set_iteration  (fact f3, core)
s05_ci = {
    "step_id": "tile_python_comprehensions_iterating.s05",
    "interaction": {
        "type": "choice",
        "interaction_id": ix_id("tile_python_comprehensions_iterating.s05"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": True,
        "measures": [
            {
                "concept_id": "python.iterating_collections",
                "capability": "recognize_unordered_set_iteration",
                "fact_ids": ["f3"]
            }
        ],
        "anchors": [
            "python.iterating_collections#assessment:recognize_unordered_set_iteration"
        ],
        "public": {
            "prompt": (
                "A colleague writes this code and expects the cities to print in the order "
                "`Lagos`, `Abuja`, `Kano`:\n\n"
                "```python\n"
                "cities = {'Lagos', 'Abuja', 'Kano'}\n"
                "for city in cities:\n"
                "    print(city)\n"
                "```\n\n"
                "What is wrong with that expectation?"
            ),
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "A set is unordered, so the items may come out in any order"
                },
                {
                    "option_id": "opt_b",
                    "text": "Nothing — sets always iterate in insertion order"
                },
                {
                    "option_id": "opt_c",
                    "text": "Nothing — sets always iterate in alphabetical order"
                },
                {
                    "option_id": "opt_d",
                    "text": "The loop will raise an error because sets are not iterable"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. A set is unordered, so its elements may come out in a different order than expected when iterated over."
                },
                "opt_b": {
                    "message": "Sets do not preserve insertion order. That property belongs to dictionaries (since Python 3.7) and lists, not sets."
                },
                "opt_c": {
                    "message": "Sets do not guarantee alphabetical order. The iteration order of a set is determined by the hash values of its elements, which is not predictable."
                },
                "opt_d": {
                    "message": "Sets are iterable — a `for` loop over a set works fine. The issue is that the order of elements is not guaranteed."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Right — a set is unordered, so iterating over it gives elements in an unpredictable order, not necessarily the insertion order."
            },
            "incorrect": {
                "message": "A set is unordered. When you iterate over a set, the elements may come out in any order — not insertion order, not alphabetical order."
            },
            "hints": [
                "What does 'unordered' mean for a set? Does it keep track of the order items were added?",
                "Compare a set `{'Lagos', 'Abuja', 'Kano'}` with a list `['Lagos', 'Abuja', 'Kano']` — which one preserves order?"
            ],
            "remediation_step_id": "tile_python_comprehensions_iterating.s04"
        }
    }
}

# s06 hands_on: code_exercise — loop_over_keys_or_sequence_items + loop_over_key_value_pairs
# Practice anchor: loop over dict items and print each key-value pair
# Use scalar city variables so py_var_mutations can mutate them
# city_a = 'Lagos', city_b = 'Abuja', city_c = 'Kano'
# order_city = {1042: city_a, 1043: city_b, 1044: city_c}
# for k, v in order_city.items(): print(k, v)
# stdout: "1042 Lagos\n1043 Abuja\n1044 Kano"
# When city_a is mutated to 'Lagos_x', output changes ✓
# NOTE: 'd.items()' and 'module.name' added to allowed to cover attr:items and attr_module
# generated by order_city.items() — the glossary's 'for k, v in d.items():' descriptor
# maps to {for, for_items, unpack} but does not cover attr:items or attr_module.
ITER_ALLOWED = [
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
    "f-strings f\"...{expr}...\"",
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
    "d.items()",
    "module.name"
]
ITER_BLOCKED = [
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
    "range()",
    "+= and other augmented assignment",
    "enumerate()",
    "zip()",
    "lambda",
    "class definitions",
    "pandas / numpy"
]

s06_ci = {
    "step_id": "tile_python_comprehensions_iterating.s06",
    "interaction": {
        "type": "code_exercise",
        "interaction_id": ix_id("tile_python_comprehensions_iterating.s06"),
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "python.iterating_collections",
                "capability": "loop_over_keys_or_sequence_items",
                "fact_ids": ["f1", "f4"]
            },
            {
                "concept_id": "python.iterating_collections",
                "capability": "loop_over_key_value_pairs",
                "fact_ids": ["f2"]
            }
        ],
        "anchors": [
            "python.iterating_collections#practice",
            "python.iterating_collections#assessment:loop_over_keys_or_sequence_items",
            "python.iterating_collections#assessment:loop_over_key_value_pairs"
        ],
        "public": {
            "prompt": (
                "QuickDeliver stores a mapping of order IDs to cities.\n\n"
                "`order_city` is already assigned below using city variables.\n\n"
                "Add a `for` loop that uses `.items()` to unpack each key and value, "
                "then prints the order ID and city on one line.\n\n"
                "Expected output:\n"
                "```\n"
                "1042 Lagos\n"
                "1043 Abuja\n"
                "1044 Kano\n"
                "```"
            ),
            "runtime": {
                "kind": "python",
                "version": PYTHON_VERSION
            },
            "workspace": {
                "files": [
                    {
                        "path": "solution.py",
                        "role": "editable",
                        "language": "python",
                        "content": (
                            "city_a = 'Lagos'\n"
                            "city_b = 'Abuja'\n"
                            "city_c = 'Kano'\n"
                            "order_city = {1042: city_a, 1043: city_b, 1044: city_c}\n"
                            "# Write your for loop here\n"
                        )
                    }
                ],
                "entry": "solution.py"
            },
            "constraints": {
                "allowed_syntax": ITER_ALLOWED,
                "blocked_syntax": ITER_BLOCKED
            }
        },
        "grading": {
            "solution_files": [
                {
                    "path": "solution.py",
                    "content": (
                        "city_a = 'Lagos'\n"
                        "city_b = 'Abuja'\n"
                        "city_c = 'Kano'\n"
                        "order_city = {1042: city_a, 1043: city_b, 1044: city_c}\n"
                        "for k, v in order_city.items():\n"
                        "    print(k, v)\n"
                    )
                }
            ],
            "tests": [
                {
                    "test_id": "t1_stdout",
                    "kind": "stdout_equals",
                    "spec": {
                        "expected": "1042 Lagos\n1043 Abuja\n1044 Kano"
                    },
                    "visible": True,
                    "message_on_fail": "Expected three lines, one per entry. Use `for k, v in order_city.items():` and `print(k, v)`."
                }
            ]
        },
        "feedback": {
            "correct": {
                "message": "Every key-value pair was printed exactly once using `.items()` to unpack both the key and the value."
            },
            "incorrect": {
                "message": "Use `for k, v in order_city.items():` to unpack each key and value, then `print(k, v)` inside the loop body."
            },
            "hints": [
                "`.items()` returns each entry as a `(key, value)` pair — unpack it with `for k, v in order_city.items():`.",
                "Inside the loop, `print(k, v)` prints the key and value separated by a space."
            ],
            "remediation_step_id": "tile_python_comprehensions_iterating.s04"
        }
    }
}

# ── assemble ──────────────────────────────────────────────────────────────────

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_008_da_python_core",
    "tiles": [
        {
            "tile_id": "tile_python_conditionals_for_loops",
            "interactions": [s02, s03, s04, s07, s08_cfl]
        },
        {
            "tile_id": "tile_python_while_loop_control",
            "interactions": [s03_wlc, s04_wlc, s06_wlc, s07_wlc]
        },
        {
            "tile_id": "tile_python_comprehensions_iterating",
            "interactions": [s02_ci, s03_ci, s05_ci, s06_ci]
        }
    ]
}

out_path = "batches/final_batch_008_da_python_core/interactions.part.c2.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"Written: {out_path}")
print(f"Tiles: {len(output['tiles'])}")
for tile in output['tiles']:
    print(f"  {tile['tile_id']}: {len(tile['interactions'])} interactions")
