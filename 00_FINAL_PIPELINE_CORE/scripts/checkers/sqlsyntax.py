"""Which glossary syntax descriptors does a SQL text use? Maps the glossary's human-readable `allowed_syntax` / `blocked_syntax`
strings (e.g. "table alias (FROM table AS alias)", "< > <= >= = <> !=") onto parse-tree facts via sqlglot.

    used(sql, coltypes) -> set of descriptor strings the query uses
    judge(sql, allowed, blocked, coltypes) -> (violations, unmapped)

A descriptor with no detector is returned in `unmapped` and the caller reports it UNVERIFIED (fail-closed): a constraint nobody can check
must never silently pass. Detectors are keyed by the glossary's exact strings; add one when a new concept introduces a new descriptor.
"""
import re

import sqlglot
import sqlglot.expressions as E
from sqlglot.tokens import Tokenizer, TokenType

DATE_TYPES = {"date", "datetime", "timestamp"}


def split_statements(sql):
    """Split on top-level semicolons using the tokenizer, so a ';' inside a string literal never splits."""
    out, start = [], 0
    for t in Tokenizer().tokenize(sql):
        if t.token_type == TokenType.SEMICOLON:
            out.append(sql[start:t.start]); start = t.end + 1
    out.append(sql[start:])
    return [s.strip() for s in out if s.strip()]


def _inside(node, arg, root_types):
    p = node.parent
    while p is not None:
        if isinstance(p, root_types):
            return True
        p = p.parent
    return False


def _in_join_on(node):
    p = node
    while p.parent is not None:
        if isinstance(p.parent, E.Join) and p.parent.args.get("on") is p:
            return True
        p = p.parent
    return False


def _tables(select):
    own = []
    frm = select.args.get("from_") or select.args.get("from")
    for t in ([frm.this] if frm is not None else []) + [j.this for j in select.args.get("joins") or []]:
        if isinstance(t, E.Table):
            own.append((t.alias_or_name, t.name))
        elif t is not None and getattr(t, "alias", None):
            own.append((t.alias, None))
    return own


def _selects(tree):
    return [n for n in tree.walk() if isinstance(n, E.Select)]


def _correlated(tree):
    for sel in _selects(tree):
        outer = set()
        p = sel.parent
        while p is not None:
            if isinstance(p, E.Select):
                outer |= {a for a, _ in _tables(p)}
            p = p.parent
        if not outer:
            continue
        own = {a for a, _ in _tables(sel)}
        for c in sel.find_all(E.Column):
            if c.find_ancestor(E.Select) is sel and c.table and c.table in outer and c.table not in own:
                return True
    return False


def used(sql, coltypes=None):
    coltypes = {k.lower(): v for k, v in (coltypes or {}).items()}
    tree = sqlglot.parse_one(sql, read="duckdb")
    nodes = list(tree.walk())
    has = lambda *ts: any(isinstance(n, ts) for n in nodes)
    out = set()
    if has(E.Select): out.add("SELECT")
    if has(E.From): out.add("FROM")
    sel = [n for n in nodes if isinstance(n, E.Select)]
    if any(isinstance(x, E.Alias) for s in sel for x in s.expressions): out.add("AS output_name")
    # a star counts as the select-list feature, not when it is the argument of COUNT(*)
    if any(isinstance(n, E.Star) and not isinstance(n.parent, E.Count) for n in nodes) or any(isinstance(c.this, E.Star) for c in tree.find_all(E.Column)):
        out.add("* and table_name.*")
    if any(isinstance(n, (E.GT, E.GTE, E.LT, E.LTE, E.EQ, E.NEQ)) and not _in_join_on(n) for n in nodes): out.add("< > <= >= = <> !=")
    if any(isinstance(n, E.And) and not _in_join_on(n) for n in nodes): out.add("AND")
    if has(E.Or): out.add("OR")
    for n in nodes:
        if isinstance(n, E.Not):
            out.add("IS NOT NULL" if isinstance(n.this, E.Is) and isinstance(n.this.expression, E.Null) else "NOT")
        elif isinstance(n, E.Is) and isinstance(n.expression, E.Null) and not isinstance(n.parent, E.Not):
            out.add("IS NULL")
    if has(E.Paren): out.add("parentheses")
    if any(s.args.get("distinct") for s in sel): out.add("DISTINCT")
    if re.search(r"\bselect\s+all\b", sql, re.I): out.add("ALL")
    if has(E.Order): out.add("ORDER BY")
    if re.search(r"\basc\b", sql, re.I): out.add("ASC")
    if any(isinstance(n, E.Ordered) and n.args.get("desc") for n in nodes): out.add("DESC")
    if has(E.Limit): out.add("LIMIT")
    if has(E.Offset) or re.search(r"\boffset\b", sql, re.I): out.add("OFFSET")
    for cls, name in ((E.Count, "COUNT"), (E.Sum, "SUM"), (E.Avg, "AVG"), (E.Min, "MIN"), (E.Max, "MAX"), (E.Coalesce, "COALESCE"),
                      (E.Length, "LENGTH"), (E.Lower, "LOWER"), (E.Upper, "UPPER"), (E.Trim, "TRIM"), (E.Extract, "EXTRACT(field FROM source)"),
                      (E.Exists, "EXISTS"), (E.Window, "window functions (OVER)"), (E.Having, "HAVING"), (E.Where, "WHERE"), (E.Case, "CASE WHEN ... THEN ... ELSE ... END")):
        if has(cls): out.add(name)
    if has(E.Concat) or re.search(r"\bconcat\s*\(", sql, re.I): out.add("CONCAT")
    if has(E.Group): out.add("GROUP BY")
    # The parser turns a typed literal (DATE '2024-02-01', TIMESTAMP '...') into a Cast node, but it is a literal, not a cast: a cast feature counts
    # only when the SQL text really writes CAST(...) / TRY_CAST(...) or ::.
    if re.search(r"\b(try_)?cast\s*\(", sql, re.I): out.add("CAST(expression AS type)")
    if "::" in sql: out.add("expression::type")
    joins = [n for n in nodes if isinstance(n, E.Join)]
    for j in joins:
        side, kind = (j.args.get("side") or "").upper(), (j.args.get("kind") or "").upper()
        if side == "LEFT": out.add("LEFT JOIN")
        elif side == "RIGHT": out.add("RIGHT JOIN")
        elif side == "FULL": out.add("FULL JOIN")
        elif kind == "CROSS" or (not j.args.get("on") and not j.args.get("using") and not kind): out.add("CROSS JOIN")
        else: out.add("JOIN / INNER JOIN")
        if j.args.get("on") is not None:
            out.add("ON")
            if any(isinstance(n, E.And) for n in j.args["on"].walk()): out.add("ON with AND across several columns")
        if j.args.get("using"):
            out.add("USING")
            if len(j.args["using"]) > 1: out.add("USING (a, b)")
    if re.search(r"\bouter\b", sql, re.I): out.add("OUTER keyword")
    for s in sel:
        names = [n for _, n in _tables(s) if n]
        if len(names) != len(set(names)): out.add("self-joins")
    if any(isinstance(n, E.Table) and n.args.get("alias") for n in nodes): out.add("table alias (FROM table AS alias)")
    if any(isinstance(c, E.Column) and c.table for c in nodes): out.add("alias.column qualification")
    for u in [n for n in nodes if isinstance(n, E.Union)]:
        out.add("UNION" if u.args.get("distinct", True) else "UNION ALL")
    if has(E.With): out.add("WITH name AS (...)")
    if any(isinstance(n, E.In) and n.args.get("query") is not None for n in nodes): out.add("IN (SELECT ...)")
    if any(isinstance(n, E.Select) and _inside(n, None, (E.Where,)) for n in nodes): out.add("subquery in WHERE")
    if any(isinstance(n, E.Subquery) and isinstance(n.parent, (E.From, E.Join)) for n in nodes): out.add("subquery in FROM with an alias")
    if _correlated(tree): out.add("correlated subqueries")
    for n in nodes:
        if isinstance(n, E.Sub):
            side_types = {coltypes.get(c.name.lower()) for c in n.find_all(E.Column)}
            if side_types & DATE_TYPES: out.add("date - date")
    return out


def referenced_columns(sql):
    """(lower-cased column names the SQL mentions, whether it uses *). Used to aim data mutations at the columns the query depends on."""
    cols, star = set(), False
    for stmt in split_statements(sql):
        tree = sqlglot.parse_one(stmt, read="duckdb")
        star = star or any(isinstance(n, E.Star) for n in tree.walk())
        cols |= {c.name.lower() for c in tree.find_all(E.Column) if not isinstance(c.this, E.Star)}
    return cols, star


UNIVERSE = {"SELECT", "FROM", "AS output_name", "* and table_name.*", "< > <= >= = <> !=", "AND", "OR", "NOT", "IS NULL", "IS NOT NULL", "parentheses",
            "DISTINCT", "ALL", "ORDER BY", "ASC", "DESC", "LIMIT", "OFFSET", "COUNT", "SUM", "AVG", "MIN", "MAX", "COALESCE", "LENGTH", "LOWER", "UPPER",
            "TRIM", "EXTRACT(field FROM source)", "EXISTS", "window functions (OVER)", "HAVING", "WHERE", "CASE WHEN ... THEN ... ELSE ... END", "CONCAT",
            "GROUP BY", "CAST(expression AS type)", "expression::type", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "CROSS JOIN", "JOIN / INNER JOIN", "ON",
            "ON with AND across several columns", "USING", "USING (a, b)", "OUTER keyword", "self-joins", "table alias (FROM table AS alias)",
            "alias.column qualification", "UNION", "UNION ALL", "WITH name AS (...)", "IN (SELECT ...)", "subquery in WHERE", "subquery in FROM with an alias",
            "correlated subqueries", "date - date"}


def judge(sql, allowed, blocked, coltypes=None):
    """(violations, unmapped). A used feature is a violation if the glossary blocks it or never allowed it."""
    unmapped = sorted({d for d in list(allowed) + list(blocked) if d not in UNIVERSE})
    feats = set()
    for stmt in split_statements(sql):
        feats |= used(stmt, coltypes)
    viol = []
    for f in sorted(feats):
        if f in blocked:
            viol.append(f"uses {f!r}, which the glossary blocks for this practice")
        elif f not in allowed:
            viol.append(f"uses {f!r}, which is not in this practice's allowed syntax (not yet taught)")
    return viol, unmapped
