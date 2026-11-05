#!/usr/bin/env python3
"""Patch interactions.part.c2.json to fix remediation_step_id references and constraints."""
import json, copy

SRC = "batches/final_batch_008_da_python_core/interactions.part.c2.json"
DST = SRC

with open(SRC) as f:
    data = json.load(f)

# ── Glossary practice anchor for python.while_loops ──────────────────────────
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
]

WHILE_BLOCKED = [
    "input()",
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

# ── Glossary practice anchor for python.iterating_collections ─────────────────
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
    "pandas / numpy",
]

for tile in data["tiles"]:
    tid = tile["tile_id"]

    if tid == "tile_python_conditionals_for_loops":
        # r01 → conditional_statements#f1
        # r02 → conditional_statements#f3
        # r03 → for_loops#f2
        for item in tile["interactions"]:
            sid = item["step_id"]
            fb = item["interaction"]["feedback"]
            if sid == "tile_python_conditionals_for_loops.s02":
                # measures conditional_statements#f1 → r01
                fb["remediation_step_id"] = "tile_python_conditionals_for_loops.r01"
            elif sid == "tile_python_conditionals_for_loops.s03":
                # measures conditional_statements#f3 → r02
                fb["remediation_step_id"] = "tile_python_conditionals_for_loops.r02"
            elif sid == "tile_python_conditionals_for_loops.s04":
                # measures conditional_statements#f2,f3,f4 → r02 (f3 overlap)
                fb["remediation_step_id"] = "tile_python_conditionals_for_loops.r02"
            elif sid == "tile_python_conditionals_for_loops.s07":
                # measures for_loops#f2 → r03
                fb["remediation_step_id"] = "tile_python_conditionals_for_loops.r03"
            elif sid == "tile_python_conditionals_for_loops.s08":
                # measures for_loops#f1,f2,f3 → r03 (f2 overlap)
                fb["remediation_step_id"] = "tile_python_conditionals_for_loops.r03"

    elif tid == "tile_python_while_loop_control":
        # r01 → while_loops#f2
        # r02 → loop_control#f1,f2
        for item in tile["interactions"]:
            sid = item["step_id"]
            ix = item["interaction"]
            fb = ix["feedback"]
            if sid == "tile_python_while_loop_control.s03":
                # measures while_loops#f2 → r01
                fb["remediation_step_id"] = "tile_python_while_loop_control.r01"
            elif sid == "tile_python_while_loop_control.s04":
                # measures while_loops#f1 → r01 (best match)
                fb["remediation_step_id"] = "tile_python_while_loop_control.r01"
                # Fix constraints to match glossary verbatim
                ix["public"]["constraints"]["allowed_syntax"] = WHILE_ALLOWED
                ix["public"]["constraints"]["blocked_syntax"] = WHILE_BLOCKED
            elif sid == "tile_python_while_loop_control.s06":
                # measures loop_control#f2 → r02
                fb["remediation_step_id"] = "tile_python_while_loop_control.r02"
            elif sid == "tile_python_while_loop_control.s07":
                # measures loop_control#f1,f2 → r02
                fb["remediation_step_id"] = "tile_python_while_loop_control.r02"

    elif tid == "tile_python_comprehensions_iterating":
        # r01 → comprehensions#f3
        # r02 → iterating_collections#f3
        for item in tile["interactions"]:
            sid = item["step_id"]
            ix = item["interaction"]
            fb = ix["feedback"]
            if sid == "tile_python_comprehensions_iterating.s02":
                # measures comprehensions#f3 → r01
                fb["remediation_step_id"] = "tile_python_comprehensions_iterating.r01"
            elif sid == "tile_python_comprehensions_iterating.s03":
                # measures comprehensions#f1,f2,f3 → r01 (f3 overlap)
                fb["remediation_step_id"] = "tile_python_comprehensions_iterating.r01"
            elif sid == "tile_python_comprehensions_iterating.s05":
                # measures iterating_collections#f3 → r02
                fb["remediation_step_id"] = "tile_python_comprehensions_iterating.r02"
            elif sid == "tile_python_comprehensions_iterating.s06":
                # measures iterating_collections#f1,f4,f2 → r02 (best match)
                fb["remediation_step_id"] = "tile_python_comprehensions_iterating.r02"
                # Fix constraints to match glossary verbatim
                ix["public"]["constraints"]["allowed_syntax"] = ITER_ALLOWED
                ix["public"]["constraints"]["blocked_syntax"] = ITER_BLOCKED

with open(DST, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Patch applied successfully.")
