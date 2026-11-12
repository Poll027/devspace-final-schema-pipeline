"""Which glossary syntax descriptors does a spreadsheet exercise use? Maps the glossary's human-readable `allowed_syntax` / `blocked_syntax` strings
(e.g. "SUM(range)", "=VLOOKUP(key, table, col, FALSE)", "absolute references ($A$1)") onto TAGS read from the formulas in the learner's sheet file.

    parse_cells(text) -> [(sheet|None, "A1", content)]       the sheet file: lines `[Sheet!]A1: value-or-=formula`
    tags(formula)     -> set of feature tags                  ("fn:SUM", "ref_rel", "ref_abs", "ref_mixed", "range", "col_range", "ref_sheet", "op_add", "concat", "cmp_gt", ...)
    descriptor_tags(d) -> set of tags a descriptor stands for, or None when it cannot be machine-checked
    judge(text, allowed, blocked) -> (violations, unmapped, not_checkable)

Same rule as pysyntax/sqlsyntax: a used feature is a violation if the glossary blocks it or never allowed it; a feature SOME allowed descriptor covers is fine.
Function names are the main axis: any `NAME(` in a descriptor (or a bare list of UPPERCASE names) maps to `fn:NAME`, so new functions need no table entry.
Only the phrases below are tables: EXPLICIT (exact descriptor -> tags), PHRASES (regex -> tags, first match), UI_IDEAS (regex: spreadsheet UI features that no program
can check, so the evaluator reads them). To extend: add a line to PHRASES; `scripts/practice_survey.py <bundle> spreadsheet` lists whatever is still unmapped.
Only formula cells are judged; typed constants (the starter's inputs) are not syntax.
"""
import re

BASE = {"formula"}
LINE = re.compile(r"^(?:([^!:]+)!)?\$?([A-Za-z]{1,3})\$?(\d{1,6})\s*:\s?(.*)$")
OPS = {"+": "op_add", "-": "op_sub", "*": "op_mul", "/": "op_div", "^": "op_pow", "%": "op_pct", "&": "concat",
       "<": "cmp_lt", "<=": "cmp_le", ">": "cmp_gt", ">=": "cmp_ge", "=": "cmp_eq", "<>": "cmp_ne"}
ARITH = {"op_add", "op_sub", "op_mul", "op_div", "op_pow"}
COMPARE = {"cmp_lt", "cmp_le", "cmp_gt", "cmp_ge", "cmp_eq", "cmp_ne"}
REFS = {"ref_rel", "ref_abs", "ref_mixed"}
# one cell ref: optional $ before column and row; not part of a longer word and not a function call
CELL = r"(?<![\w.$])(\$?)([A-Za-z]{1,3})(\$?)(\d{1,7})(?![\w(])"


def parse_cells(text):
    out = []
    for ln in text.splitlines():
        m = LINE.match(ln) if ln.strip() and not ln.strip().startswith("//") else None
        if m:
            out.append((m.group(1), m.group(2).upper() + m.group(3), m.group(4).strip()))
    return out


def tags(formula):
    f = formula.strip()
    t = {"formula"}
    f = f[1:] if f.startswith("=") else f
    t |= {"lit_str"} if re.search(r'"(?:[^"]|"")*"', f) else set()
    f = re.sub(r'"(?:[^"]|"")*"', '""', f)  # string contents are not syntax
    if re.search(r"(?<![\w.])(TRUE|FALSE)(?![\w(])", f, re.I):
        t.add("lit_bool")
    if re.search(r"\{", f):
        t.add("array_const")
    if re.search(r"(?<![\w.$!:])\d+\.?\d*(?:e[-+]?\d+)?(?![\w(!:])|(?<![\w.])\.\d+", f, re.I):
        t.add("lit_num")
    for m in re.finditer(r"(?<![\w.])([A-Za-z_][\w.]*)\(", f):
        t.add(f"fn:{m.group(1).upper()}")
    if re.search(r"(?<![\w.])\(", f):
        t.add("paren_group")
    if re.search(r"(?:'[^']+'|[A-Za-z_]\w*)!", f):
        t.add("ref_sheet")
    f2 = re.sub(r"(?:'[^']+'|[A-Za-z_]\w*)!", "", f)
    if re.search(r"(?<![\w.$])\$?[A-Za-z]{1,3}:\$?[A-Za-z]{1,3}(?![\w(\d])|(?<![\w.$])\$?\d+:\$?\d+(?![\w(])", f2):
        t.add("col_range")
        f2 = re.sub(r"\$?[A-Za-z]{1,3}:\$?[A-Za-z]{1,3}(?![\w(\d])", "", f2)
    for m in re.finditer(CELL, f2):
        d1, d2 = bool(m.group(1)), bool(m.group(3))
        t.add("ref_abs" if d1 and d2 else "ref_mixed" if d1 or d2 else "ref_rel")
    if re.search(CELL + r"\s*:\s*\$?[A-Za-z]{1,3}\$?\d", f2):
        t.add("range")
    bare = re.sub(CELL, "", re.sub(r"(?<![\w.])[A-Za-z_][\w.]*\(", "(", f2))
    if re.search(r"(?<![\w.$])[A-Za-z_]\w*(?![\w(])", re.sub(r"\b(TRUE|FALSE)\b", "", bare, flags=re.I)):
        t.add("name_ref")
    ops = re.sub(r"(?<=[\w)\]%$\"])\s*", lambda m: m.group(0), f2)
    for m in re.finditer(r"(?<=[\w)\]%$\"}])\s*(<>|<=|>=|[-+*/^&<>=%])", ops):
        t.add(OPS[m.group(1)])
    return t


# ---------------------------------------------------------------- descriptors
EXPLICIT = {
    "numbers": {"lit_num"}, "text in quotes": {"lit_str"}, "TRUE / FALSE": {"lit_bool"}, "TRUE and FALSE": {"lit_bool"},
    "+ - * /": {"op_add", "op_sub", "op_mul", "op_div"}, "+ - * / ^": ARITH, "arithmetic operators": ARITH | {"op_pct"},
    "comparison operators": COMPARE, "< <= > >= = <>": COMPARE, "& (concatenation)": {"concat"}, "&": {"concat"},
    "parentheses": {"paren_group"}, "parentheses for grouping": {"paren_group"},
}
# first match wins; patterns are tested on the lowercased descriptor
PHRASES = [
    (r"absolute (cell )?reference|\$[a-z]+\$\d", {"ref_abs"}),
    (r"mixed (cell )?reference", {"ref_mixed"}),
    (r"relative (cell )?reference", {"ref_rel"}),
    (r"cell reference|a1 (notation|style)", REFS),
    (r"whole[- ]column|column range|entire column", {"col_range"}),
    (r"cell range|\brange\b.*\ba1:|a1:[a-z]+\d|range reference", {"range"}),
    (r"cross-sheet|other sheet|sheet reference|sheet1!|sheet name!", {"ref_sheet"}),
    (r"named range|defined name|named cell", {"name_ref"}),
    (r"array (constant|literal)|\{1,2,3\}", {"array_const"}),
    (r"percent", {"op_pct"}),
    (r"concatenat", {"concat"}),
    (r"arithmetic|math operators", ARITH | {"op_pct"}),
    (r"comparison|relational", COMPARE),
    (r"text and number|string and number|literal", {"lit_num", "lit_str", "lit_bool"}),
    (r"^formula|^=\s*(prefix|sign)|leading =|formula bar|starting with =", set()),
]
# spreadsheet UI features and ideas: nothing a formula checker can decide; the evaluator reads these
UI_IDEAS = re.compile(r"pivot ?table|chart|graph|conditional format|data validation|format cells|number format|keyboard|shortcut|freeze|menu|ribbon|toolbar|"
                      r"autofill|fill handle|drag|filter(ing)? (rows|data|view)|sort(ing)? (rows|data|dialog)|slicer|macro|vba|apps script|goal seek|solver|what-if|"
                      r"import|paste|click|select(ing)?\b|dialog|button|sheet tab|column width|row height|hide|protect|comment|note", re.I)
NOT_CHECKABLE = set()  # exact descriptors a survey decides are ideas, not syntax (add here when UI_IDEAS over- or under-matches)
FN_WORDS = re.compile(r"[A-Z][A-Z0-9.]+")


def descriptor_tags(d):
    s = d.strip()
    if s in EXPLICIT:
        return EXPLICIT[s]
    if s in NOT_CHECKABLE:
        return None
    low = s.lower()
    if re.fullmatch(r"=?\s*[A-Z][A-Z0-9.]*(\s*(,|/|\||and|or|&)\s*[A-Z][A-Z0-9.]*)*(\s*functions?)?", s) and not re.fullmatch(r"[A-Z]", s):  # "SUM, AVERAGE" / "IF / IFS"
        return {f"fn:{w}" for w in FN_WORDS.findall(s)}
    if re.search(r"(?<![\w.])[A-Za-z_][\w.]*\(", s) or s.startswith("="):  # formula-like: "=SUM(B2:B9)", "VLOOKUP(key, table, col, FALSE)"
        tg = tags(s) - BASE - {"name_ref"}  # in a descriptor, `range` / `key` are placeholders, not defined names
        if re.search(r"\b(range|array|table|table_array)\b", low):  # SUM(range): the argument is a range reference
            tg.add("range")
        return tg or None
    for pat, tg in PHRASES:
        if re.search(pat, low):
            return tg
    if UI_IDEAS.search(low):
        return None
    fns = {f"fn:{w}" for w in re.findall(r"\b([A-Z][A-Z0-9.]{1,})\s+function\b", s)}  # "the VLOOKUP function"
    return fns or None


def is_idea(d):
    """A descriptor about the spreadsheet UI / a concept, not formula syntax (the evaluator reads these)."""
    s = d.strip()
    return s in NOT_CHECKABLE or (descriptor_tags(s) is None and bool(UI_IDEAS.search(s)) and not re.search(r"(?<![\w.])[A-Za-z_][\w.]*\(", s))


def judge(text, allowed, blocked):
    """text: the sheet file. (violations, unmapped, not_checkable)"""
    amap, bmap, unmapped, nochk = {}, {}, [], []
    for d, m in [(d, amap) for d in allowed] + [(d, bmap) for d in blocked]:
        tg = descriptor_tags(d)
        if tg is None:
            (nochk if is_idea(d) else unmapped).append(d)
        else:
            m[d] = tg
    ok = set().union(*amap.values()) if amap else set()
    viol = []
    used = set()
    for _, _, c in parse_cells(text):
        if c.startswith("="):
            used |= tags(c)
    if not allowed and (used - BASE):  # no list at all: say so, instead of blaming each operator as "not yet taught"
        viol.append("constraints.allowed_syntax is empty or missing, but the solution uses " + ", ".join(sorted(used - BASE)) + ". The glossary gave this practice no live_code list, "
                    "so YOU must write it: descriptors for the operators, reference styles and functions this concept and the earlier ones taught "
                    "(e.g. '+ - * /', 'relative cell references', 'absolute references ($A$1)', 'SUM'), and blocked_syntax for later concepts' functions. See GENERATOR.md.")
        return viol, sorted(set(unmapped)), sorted(set(nochk))
    for f in sorted(used - BASE):
        if f in ok:
            continue
        who = sorted(d for d, tg in bmap.items() if f in tg)
        viol.append(f"uses {f!r}, which the glossary blocks for this practice ({who[0]!r})" if who else f"uses {f!r}, which is not in this practice's allowed syntax (not yet taught)")
    return viol, sorted(set(unmapped)), sorted(set(nochk))


def used_tags(text):
    return set().union(set(), *(tags(c) for _, _, c in parse_cells(text) if c.startswith("="))) - BASE


def cell_tags(text, ref):
    """Tags of the formula in cell `ref` ('A1' or 'Sheet!A1') of a sheet file, or None when that cell holds no formula."""
    want = ref.rsplit("!", 1)[-1].replace("$", "").upper()
    for _, r, c in parse_cells(text):
        if r == want and c.startswith("="):
            return tags(c)
    return None
