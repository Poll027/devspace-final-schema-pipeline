"""Which glossary syntax descriptors does a Python text use? Maps the glossary's human-readable `allowed_syntax` / `blocked_syntax` strings
(e.g. "for item in sequence:", "df.groupby('key')['col'].mean()") onto TAGS read from the code's parse tree and token stream.

    tags(code)  -> set of feature tags the code uses            (e.g. "for", "op_mul", "attr:groupby", "call:print", "import:pandas")
    descriptor_tags(d) -> set of tags a descriptor stands for, or None when it cannot be machine-checked
    judge(code, allowed, blocked) -> (violations, unmapped, not_checkable)

Same rule as sqlsyntax: a used feature is a violation if the glossary blocks it or never allowed it. A feature that SOME allowed descriptor covers is
fine even when another blocked descriptor also names it (blocked entries are often the other forms of the same feature). Library calls are tagged
by method name (`attr:groupby`), so the glossary's own example strings define what is allowed. Descriptors that describe an idea rather than syntax
("hypothesis testing functions") are `not_checkable`: the evaluator reads those; they are never silently treated as verified by a program.
"""
import ast
import io
import re
import tokenize

LIBS = {"pandas", "numpy", "matplotlib", "seaborn", "scipy", "statsmodels"}
BASE = {"assign", "comment", "expr_stmt"}  # always fine: assigning names, comments

OPS = {ast.Add: "op_add", ast.Sub: "op_sub", ast.Mult: "op_mul", ast.Div: "op_div", ast.FloorDiv: "op_floordiv", ast.Mod: "op_mod", ast.Pow: "op_pow",
       ast.BitAnd: "op_bitand", ast.BitOr: "op_bitor"}
CMPS = {ast.Lt: "cmp_lt", ast.LtE: "cmp_le", ast.Gt: "cmp_gt", ast.GtE: "cmp_ge", ast.Eq: "cmp_eq", ast.NotEq: "cmp_ne", ast.In: "cmp_in", ast.NotIn: "cmp_in"}
ARITH = {"op_add", "op_sub", "op_mul", "op_div", "op_floordiv", "op_mod", "op_pow"}
COMPARE = {"cmp_lt", "cmp_le", "cmp_gt", "cmp_ge", "cmp_eq", "cmp_ne"}
LITS = {"lit_int", "lit_float", "lit_str", "lit_bool"}
KEYWORD_TAGS = {"if", "elif", "else", "for", "while", "break", "continue", "return", "global", "try", "except", "lambda", "class", "with"}


def tags(code):
    t = set()
    tree = ast.parse(code)
    user_funcs = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    modules = {(a.asname or a.name).split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names if a.name.split(".")[0] not in LIBS}
    for tok in tokenize.generate_tokens(io.StringIO(code).readline):
        if tok.type == tokenize.COMMENT:
            t.add("comment")
        elif tok.type == tokenize.NAME and tok.string in KEYWORD_TAGS:
            t.add(tok.string)
        elif tok.type == tokenize.STRING:
            body = tok.string.lstrip("rbuRBU")
            q = body[:1]
            if not tok.string.lstrip("rbuRBU").startswith(("f", "F")) and q in "'\"" and ({"'", '"'} - {q}).pop() in body[1:-1]:
                t.add("quote_mixing")
        elif tok.type == tokenize.OP and tok.string == "~":
            t.add("op_invert")
    t |= _paren_groups(code)
    for n in ast.walk(tree):
        if isinstance(n, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.ClassDef)):
            t.add("block")
        if isinstance(n, ast.For):
            t.add("for")
            if isinstance(n.iter, ast.Call) and isinstance(n.iter.func, ast.Attribute) and n.iter.func.attr == "items":
                t.add("for_items")
            if isinstance(n.target, ast.Tuple):
                t.add("unpack")
        elif isinstance(n, ast.Constant):
            v = n.value
            t.add("lit_bool" if isinstance(v, bool) else "lit_int" if isinstance(v, int) else "lit_float" if isinstance(v, float) else "lit_str" if isinstance(v, str) else "lit_other")
        elif isinstance(n, ast.JoinedStr):
            t.add("fstring")
            if any(isinstance(x, ast.FormattedValue) and x.format_spec is not None for x in n.values):
                t.add("fmt_spec")
        elif isinstance(n, ast.BinOp):
            t.add(OPS.get(type(n.op), "op_other"))
        elif isinstance(n, ast.Compare):
            t |= {CMPS.get(type(o), "cmp_other") for o in n.ops}
        elif isinstance(n, ast.BoolOp):
            t.add("bool_and" if isinstance(n.op, ast.And) else "bool_or")
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not):
            t.add("bool_not")
        elif isinstance(n, ast.AugAssign):
            t.add("aug_assign")
        elif isinstance(n, ast.List):
            t.add("list_lit")
        elif isinstance(n, ast.Dict):
            t.add("dict_lit")
        elif isinstance(n, ast.Set):
            t.add("set_lit")
        elif isinstance(n, ast.Tuple):
            t.add("tuple_lit")
            if len(n.elts) == 1:
                t.add("tuple_one")
            if isinstance(getattr(n, "ctx", None), ast.Store):
                t.add("unpack")
        elif isinstance(n, ast.ListComp):
            t.add("listcomp_if" if any(g.ifs for g in n.generators) else "listcomp")
        elif isinstance(n, ast.DictComp):
            t.add("dictcomp")
        elif isinstance(n, (ast.SetComp, ast.GeneratorExp)):
            t.add("comp_other")
        elif isinstance(n, ast.FunctionDef):
            a = n.args
            t.add("def_default" if a.defaults or a.kw_defaults else "def_args" if (a.args or a.kwonlyargs) else "def_noargs")
        elif isinstance(n, ast.Return):
            t.add("return")
        elif isinstance(n, ast.Global):
            t.add("global")
        elif isinstance(n, ast.Import):
            for a in n.names:
                if a.name.split(".")[0] in LIBS:
                    t.add(f"import:{a.name.split('.')[0]}")
                else:
                    t.add("import_mod")
        elif isinstance(n, ast.ImportFrom):
            top = (n.module or "").split(".")[0]
            t.add("from_import" if top not in LIBS else f"import:{top}")
        elif isinstance(n, ast.Subscript):
            sl = n.slice
            parts = sl.elts if isinstance(sl, ast.Tuple) else [sl]
            if any(isinstance(p, ast.Slice) for p in parts):
                t.add("slice")
            if isinstance(n.value, ast.Attribute) and n.value.attr in ("loc", "iloc"):
                pass
            elif not all(isinstance(p, ast.Slice) for p in parts):
                t.add("idx")
            if isinstance(sl, (ast.Compare, ast.BoolOp)) or (isinstance(sl, ast.BinOp) and isinstance(sl.op, (ast.BitAnd, ast.BitOr))):
                t.add("bool_filter")
            if isinstance(getattr(n, "ctx", None), ast.Store):
                t.add("idx_assign")
        elif isinstance(n, ast.Attribute):
            if not (isinstance(n.value, ast.Name) and n.value.id in modules):  # math.sqrt: the module's own names are not separate syntax
                t.add(f"attr:{n.attr}")
            if isinstance(n.value, ast.Name) and n.value.id not in ("pd", "np", "plt", "sns", "mpl", "ax", "fig", "df"):
                t.add("attr_module")
        elif isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                if f.id in user_funcs:
                    t.add("call_user")
                    if n.args:
                        t.add("call_pos_user")
                    if n.keywords:
                        t.add("call_kw_user")
                else:
                    t.add(f"call:{f.id}")
            if not (isinstance(f, ast.Name) and f.id in user_funcs):  # f(city="x") on the learner's own function is "call_kw_user", not a named keyword
                for k in n.keywords:
                    if k.arg:
                        t.add(f"kw:{k.arg}")
        elif isinstance(n, ast.Name) and n.id in ("FacetGrid", "GridSpec"):
            t.add(f"attr:{n.id}")
    return t


def _paren_groups(code):
    """Parentheses used for grouping (not a call, not a tuple)."""
    toks = [x for x in tokenize.generate_tokens(io.StringIO(code).readline) if x.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT)]
    for i, x in enumerate(toks):
        if x.type == tokenize.OP and x.string == "(":
            prev = toks[i - 1] if i else None
            if prev and (prev.type == tokenize.NAME and prev.string not in {"and", "or", "not", "in", "return", "if", "elif", "while", "is"} or prev.string in (")", "]")):
                continue  # a call
            depth, comma = 0, False
            for y in toks[i:]:
                if y.type == tokenize.OP and y.string in "([{":
                    depth += 1
                elif y.type == tokenize.OP and y.string in ")]}":
                    depth -= 1
                    if depth == 0:
                        break
                elif y.type == tokenize.OP and y.string == "," and depth == 1:
                    comma = True
            if not comma and not (toks[i + 1].string == ")"):
                return {"paren_group"}
    return set()


# ---------------------------------------------------------------- descriptors
EXPLICIT = {
    "custom theme dictionaries": {"dict_lit"}, "fig, axes": {"unpack"},
    "name = value assignment": {"assign"}, "variable assignment": {"assign"}, "list literals and variable assignment": {"assign", "list_lit"},
    "variable assignment (fig, ax = ...)": {"assign", "unpack"},
    "using assigned names in an expression, as in the width * height example": set(),
    "int, float, str and bool literals": LITS, "single- or double-quoted strings": {"lit_str"}, "string literals for style and palette names": {"lit_str"},
    "True / False": {"lit_bool"}, "whole-number literals as in the examples": {"lit_int"}, "float literals": {"lit_float"},
    "float, str and bool literals": {"lit_float", "lit_str", "lit_bool"},
    "+ - * / // % **": ARITH, "+ - * / // % ** (all arithmetic operators)": ARITH, "+ - / // % ** (only the single * from the width * height example is allowed)": ARITH - {"op_mul"},
    "arithmetic operators (-, /, *)": {"op_sub", "op_div", "op_mul"},
    "parentheses for grouping": {"paren_group"},
    "< <= > >= == !=": COMPARE, "comparison operators": COMPARE, "comparison operators (>, <, ==)": {"cmp_lt", "cmp_gt", "cmp_eq"},
    "and": {"bool_and"}, "or": {"bool_or"}, "not": {"bool_not"},
    "& | ~ with parenthesised conditions": {"op_bitand", "op_bitor", "op_invert", "paren_group"}, "| and & on sets": {"op_bitand", "op_bitor"},
    "[...] list literal": {"list_lit"}, "Python list literals": {"list_lit"}, "list of labels": {"list_lit"}, "tuple literals for figsize": {"tuple_lit"},
    "list[i] and list[-1] indexing": {"idx"}, "list[a:b] slicing": {"slice"}, "integer slices": {"slice"}, "label slices": {"slice"},
    "list[i] = value": {"idx_assign"}, "list.append()": {"attr:append"}, "len()": {"call:len"},
    "{key: value} dictionary literal": {"dict_lit"}, "d[key] lookup and assignment": {"idx", "idx_assign"}, "d.get()": {"attr:get"}, "key in d": {"cmp_in"}, "x in a_set": {"cmp_in"},
    "tuple literal with commas or parentheses": {"tuple_lit"}, "unpacking a, b = t": {"unpack"}, "one-item tuple with trailing comma": {"tuple_one"},
    "set()": {"call:set"}, "{...} set literal": {"set_lit"},
    "quote mixing to embed a quote": {"quote_mixing"}, "f-strings": {"fstring"}, 'f-strings f"...{expr}..."': {"fstring"}, "format specifier such as {value:.2f}": {"fmt_spec"},
    "if": {"if"}, "elif": {"elif"}, "else": {"else"}, "if/elif/else": {"if", "elif", "else"}, "colon and indented block": {"block"},
    "for item in sequence:": {"for"}, "for key in d:": {"for"}, "for k, v in d.items():": {"for", "for_items", "unpack"}, "while condition:": {"while"},
    "break": {"break"}, "continue": {"continue"},
    "[expr for x in seq]": {"listcomp"}, "[expr for x in seq if cond]": {"listcomp_if"}, "{k: v for ...}": {"dictcomp"},
    "def name():": {"def_noargs"}, "calling name()": {"call_user"}, "def f(a, b):": {"def_args"}, "positional arguments in a call": {"call_pos_user"},
    "return": {"return"}, "def f(a, b=default):": {"def_default"}, "keyword arguments f(name=value)": {"call_kw_user"}, "global statement": {"global"},
    "def": {"def_noargs", "def_args", "def_default"}, "def function(row): ...": {"def_args"}, "def / return (functions come later)": {"def_noargs", "def_args", "def_default", "return"},
    "try:": {"try"}, "except ValueError:": {"except"}, "input()": {"call:input"},
    "import module": {"import_mod"}, "module.name": {"attr_module"}, "from module import name": {"from_import"},
    "open(file, mode)": {"call:open"}, "with open(...) as f:": {"with", "call:open"}, "f.read()": {"attr:read"}, "f.write()": {"attr:write"},
    "csv.DictReader": {"attr:DictReader"}, "csv.DictWriter": {"attr:DictWriter"}, "newline=''": {"kw:newline"},
    "range()": {"call:range"}, "+= and other augmented assignment": {"aug_assign"}, "enumerate()": {"call:enumerate"}, "zip()": {"call:zip"},
    "lambda": {"lambda"}, "class definitions": {"class"}, "pandas / numpy": {"import:pandas", "import:numpy"}, "pandas": {"import:pandas"}, "numpy": {"import:numpy"},
    "import numpy": {"import:numpy"}, "import seaborn": {"import:seaborn"}, "seaborn": {"import:seaborn"}, "seaborn functions": {"import:seaborn"}, "sns.": {"import:seaborn"}, "sns.*": {"import:seaborn"},
    "scipy.stats": {"import:scipy"}, "statsmodels": {"import:statsmodels"},
    "import pandas as pd": {"import:pandas"}, "import matplotlib.pyplot as plt": {"import:matplotlib"}, "import matplotlib as mpl": {"import:matplotlib"}, "import seaborn as sns": {"import:seaborn"},
    "single-line comments (#)": {"comment"}, "boolean filtering": {"bool_filter"}, "df[df['col'] > value]": {"idx", "cmp_gt", "bool_filter"},
    "for loops over rows": {"for"}, "if statements around the membership test": {"if", "cmp_in"},
    "matplotlib.rcParams direct manipulation": {"attr:rcParams"}, "FacetGrid": {"attr:FacetGrid"}, "GridSpec": {"attr:GridSpec"},
    "subplots / multi-panel figures": {"attr:subplots"},
    "fig, ax = plt.subplots()": {"attr:subplots", "unpack"}, "fig, axes = plt.subplots(...)": {"attr:subplots", "unpack"},
}
# --- chart_renderer additions (assumption: the glossary writes charting calls bare, e.g. "bar(x, y)" / "plot(kind='bar')", for what a program writes as a method of
# plt/ax/sns/df). A bare call to one of these names is matched as the attribute the learner's code actually uses. Extend this set from `practice_survey.py <bundle> viz`.
CHART_METHODS = {"plot", "hist", "scatter", "bar", "barh", "boxplot", "heatmap", "pie", "legend", "title", "xlabel", "ylabel", "figure", "subplots", "savefig", "show",
                 "imshow", "histplot", "lineplot", "scatterplot", "barplot", "countplot", "violinplot", "pairplot", "set_title", "set_xlabel", "set_ylabel",
                 "tight_layout", "grid", "xticks", "yticks", "xlim", "ylim", "annotate", "axhline", "axvline", "fill_between", "errorbar", "suptitle", "set_theme", "corr"}
# ideas, not syntax: nothing a program can decide; the evaluator checks these by reading
NOT_CHECKABLE = {"SQL syntax", "regex patterns", "hypothesis testing functions", "p-value computations", "compression options", "custom theme dictionaries",
                 "confidence interval calculations", "df.sort_values then drop", "list of labels (ideas)"}


def descriptor_tags(d):
    if d in EXPLICIT:
        return EXPLICIT[d]
    if d in NOT_CHECKABLE:
        return None
    m = re.fullmatch(r"import (\w+)(?: as \w+)?", d)  # "import math", "import random as rnd"
    if m:
        return {f"import:{m.group(1)}"} if m.group(1) in LIBS else {"import_mod"}
    m = re.fullmatch(r"from (\w+) import [\w, *]+", d)
    if m:
        return {f"import:{m.group(1)}"} if m.group(1) in LIBS else {"from_import"}
    if re.match(r"(math|random|statistics|csv|json|datetime|os|sys|time|string|re)\.\w+", d):  # "math.sqrt()", "random.choice(...)"
        return {"attr_module"}
    tg = set()
    for m in re.finditer(r"\.([A-Za-z_]\w*)", d):  # attribute / method names (also inside dotted examples like plt.style.use)
        tg.add(f"attr:{m.group(1)}")
    for m in re.finditer(r"(?<![\w.])([A-Za-z_]\w*)\(", d):  # plain calls
        if m.group(1) not in {"df", "pd", "plt", "sns", "ax", "fig", "mpl", "orders", "customers"}:
            tg.add(f"attr:{m.group(1)}" if m.group(1) in CHART_METHODS else f"call:{m.group(1)}")
    for m in re.finditer(r"(?<![\w.])([A-Za-z_]\w*)=", d):  # keyword arguments
        tg.add(f"kw:{m.group(1)}")
    if re.search(r"\w\[", d):
        tg.add("idx")
    if "] = " in d or re.search(r"\]\s*=\s", d):
        tg.add("idx_assign")
    for m in re.finditer(r"\b(shape|dtypes|columns|index|values|available|rcParams)\b", d):
        tg.add(f"attr:{m.group(1)}")
    if tg:  # an example call shows the literal arguments it takes: 'title' -> a string, (2, 2) / <int> -> whole numbers
        if re.search(r"""['"]""", d):
            tg.add("lit_str")
        if re.search(r"(?<![\w.])\d+(?![\w.])|<int>", d):
            tg.add("lit_int")
        if re.search(r"<float>|\d\.\d", d):
            tg.add("lit_float")
    return tg or None


def learner_part(code, starter):
    """The solution with its top-level statements that appear unchanged in the starter blanked out (line numbers kept).
    The starter's imports and `name = value` inputs are scaffolding the generator supplies (and the hard-coded-answer gate requires): the learner did not write them,
    so their literals/imports are not judged against the concept's allowed syntax. Everything the learner adds or edits is still judged."""
    if not starter:
        return code
    try:
        mine, theirs = ast.parse(code), ast.parse(starter)
    except SyntaxError:
        return code
    given = {ast.dump(n) for n in theirs.body}
    lines = code.split("\n")
    for n in mine.body:
        if ast.dump(n) in given and not isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            for i in range(n.lineno - 1, n.end_lineno):
                lines[i] = ""
    return "\n".join(lines)


def judge(code, allowed, blocked, starter=None):
    """(violations, unmapped, not_checkable)"""
    code = learner_part(code, starter)
    amap, bmap, unmapped, nochk = {}, {}, [], []
    for d, m in [(d, amap) for d in allowed] + [(d, bmap) for d in blocked]:
        tg = descriptor_tags(d)
        if tg is None:
            (nochk if d in NOT_CHECKABLE else unmapped).append(d)
        else:
            m[d] = tg
    ok = set().union(*amap.values()) if amap else set()
    no = set().union(*bmap.values()) if bmap else set()
    viol = []
    for f in sorted(tags(code) - BASE - {"lit_other"}):
        if f in ok:
            continue
        who = sorted(d for d, tg in bmap.items() if f in tg)
        viol.append(f"uses {f!r}, which the glossary blocks for this practice ({who[0]!r})" if who else f"uses {f!r}, which is not in this practice's allowed syntax (not yet taught)")
    return viol, sorted(set(unmapped)), sorted(set(nochk))
