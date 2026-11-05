"""Run authored code in the pinned engine and judge it against the tests. ROLE-AGNOSTIC dispatch; one runner function per runtime kind.

    run_exercise(registry, ix) -> Outcome(problems=[...], tests_passed, tests_total, provenance|None, unverified=bool)

Used twice with the same code: assemble_tiles.py (fills grading.execution_provenance from a real run) and checkers/code.py (re-runs and
checks everything, so a tampered lesson or a wrong key cannot pass). A runtime with no runner is `unverified`, never a silent pass.
Isolation: the Node process runs the engine with host-file/network access disabled and configuration locked (see sandbox/run_sql.mjs),
under a wall-clock timeout and a heap limit, with a minimal environment.
# ponytail: one `node` process per exercise batch (~0.5s per script); a pool would be faster if validation time ever matters.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from . import sqlsyntax
from .dataset import resolve_dataset

CORE = Path(__file__).resolve().parents[2]
SANDBOX = CORE / "sandbox"
RUNTIMES = json.loads((CORE / "registry" / "runtimes.json").read_text())["runtimes"]
NODE_TIMEOUT_S = int(os.environ.get("SANDBOX_TIMEOUT_S", 90))


class SandboxError(Exception):
    pass


@dataclass
class Outcome:
    problems: list = field(default_factory=list)
    tests_passed: int = 0
    tests_total: int = 0
    provenance: dict | None = None
    unverified: str | None = None
    hidden_checks: list = field(default_factory=list)
    preview_png: str | None = None  # chart_renderer: base64 PNG of the reference solution's last figure (player preview; not stored in the lesson)


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def _node_once(job, runner):
    if not shutil.which("node") or not (SANDBOX / "node_modules").exists():
        raise SandboxError("node or sandbox/node_modules missing: run `npm ci` in 00_FINAL_PIPELINE_CORE/sandbox")
    env = {"PATH": os.environ.get("PATH", ""), "HOME": "/nonexistent", "LANG": "C"}  # no credentials, no proxies
    try:
        flags = ["--permission", f"--allow-fs-read={SANDBOX}"] if Path(runner).name in ("run_py.mjs", "run_sheet.mjs") else []  # python/sheet: no host writes, children or workers
        r = subprocess.run(["node", "--max-old-space-size=512", *flags, str(SANDBOX / Path(runner).name)], input=json.dumps(job), capture_output=True,
                           text=True, cwd=SANDBOX, env=env, timeout=NODE_TIMEOUT_S + 4 * len(job.get('scripts', [])))  # a slow server needs time per script, not just per process
    except subprocess.TimeoutExpired:
        raise SandboxError(f"runner exceeded {NODE_TIMEOUT_S}s (infinite loop or a query that is far too heavy)")
    if r.returncode or not r.stdout.strip():
        raise SandboxError(f"runner crashed ({r.returncode}): {(r.stderr or r.stdout)[-400:]}")
    return json.loads(r.stdout)


WORKERS = max(1, min(int(os.environ.get("SANDBOX_WORKERS", 3)), os.cpu_count() or 1))


def node_run(job, runner):
    """Run the job's scripts in the engine. Every script already gets a fresh database, so scripts are independent: with many of them they are
    spread over up to SANDBOX_WORKERS node processes (default 3, never more than the CPU count) and the results merged."""
    scripts = job["scripts"]
    if WORKERS == 1 or len(scripts) < 6:
        return _node_once(job, runner)
    from concurrent.futures import ThreadPoolExecutor
    shares = [scripts[i::WORKERS] for i in range(WORKERS)]
    with ThreadPoolExecutor(WORKERS) as ex:
        parts = list(ex.map(lambda sc: _node_once({**job, "scripts": sc}, runner), [x for x in shares if x]))
    merged = dict(parts[0])
    merged["results"] = {k: v for p in parts for k, v in p["results"].items()}
    return merged


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _same(a, b, tol):
    if _num(a) and _num(b):
        return abs(a - b) <= tol
    return a == b


def rows_equal(got, want, ordered, tol=1e-9):
    if len(got) != len(want):
        return False
    if not ordered:
        key = lambda r: json.dumps(r, default=str)
        got, want = sorted(got, key=key), sorted(want, key=key)
        # sort numerically-near-equal floats consistently by rounding the sort key only
        key = lambda r: json.dumps([round(v, 6) if _num(v) else v for v in r], default=str)
        got, want = sorted(got, key=key), sorted(want, key=key)
    return all(len(g) == len(w) and all(_same(x, y, tol) for x, y in zip(g, w)) for g, w in zip(got, want))


# ---------------------------------------------------------------- SQL
def _tables(registry, mounts, overrides, problems):
    out, coltypes = [], {}
    for m in mounts:
        variant = overrides.get(m["mount_path"], m.get("variant_id"))
        try:
            cols, rows = resolve_dataset(registry, m["asset_id"], variant)
        except (KeyError, ValueError) as ex:
            problems.append(f"mount {m['mount_path']}: {ex}")
            continue
        names = [c["name"] for c in cols]
        out.append({"name": m["mount_path"], "columns": [{"name": c["name"], "type": c.get("type", "string")} for c in cols], "rows": [[r[n] for n in names] for r in rows]})
        coltypes.update({c["name"]: c.get("type", "string") for c in cols})
    return out, coltypes


def _entry(ix, which):
    pub, gr = ix["public"], ix["grading"]
    ws = pub["workspace"]
    entry = ws.get("entry") or next((f["path"] for f in ws["files"] if f["role"] == "editable"), ws["files"][0]["path"])
    pool = ws["files"] if which == "starter" else gr["solution_files"]
    f = next((f for f in pool if f["path"] == entry), None)
    return entry, (f["content"] if f else None)


# ---- hidden checks: deterministic mutations of the mounted data (the player's grader must apply the same ops)
MAX_HIDDEN = 4


def apply_ops(table, ops):
    """Return a mutated deep copy of {name, columns, rows}. ops: drop_row{index} | duplicate_row{index} | set_cell{index, column, value}."""
    t = json.loads(json.dumps(table))
    names = [c["name"] for c in t["columns"]]
    for o in ops:
        i = o["index"]
        if o["op"] == "drop_row" and i < len(t["rows"]):
            del t["rows"][i]
        elif o["op"] == "duplicate_row" and i < len(t["rows"]):
            t["rows"].insert(i + 1, list(t["rows"][i]))
        elif o["op"] == "set_cell" and i < len(t["rows"]) and o["column"] in names:
            t["rows"][i][names.index(o["column"])] = o["value"]
    return t


def candidate_mutations(tables, ref_cols=None):
    """Deterministic, role-agnostic candidates per table, in a fixed order: drop first row, duplicate last row, drop last row, then for each column the
    solution references (all columns, capped, for SELECT *): set row 0's cell to NULL, and change it (strings + "_x", numbers + 1000). Only mutations
    that change the solution's result are kept (stored as hidden_checks). NULL matters: it changes any IS NULL / IS NOT NULL / COUNT(col) query."""
    out = []
    for t in tables:
        if not t["rows"]:
            continue
        n, name = len(t["rows"]), t["name"]
        cands = [("drop_first", [{"op": "drop_row", "index": 0}]), ("dup_last", [{"op": "duplicate_row", "index": n - 1}]), ("drop_last", [{"op": "drop_row", "index": n - 1}])]
        cols = [c for c in t["columns"] if ref_cols is None or c["name"].lower() in ref_cols][:6]
        for c in cols:
            j = [x["name"] for x in t["columns"]].index(c["name"])
            v = t["rows"][0][j]
            if v is None:
                continue
            cands.append((f"null_{c['name']}", [{"op": "set_cell", "index": 0, "column": c["name"], "value": None}]))
            if isinstance(v, str) and c.get("type", "string") == "string":
                cands.append((f"set_{c['name']}", [{"op": "set_cell", "index": 0, "column": c["name"], "value": v + "_x"}]))
            elif isinstance(v, (int, float)) and not isinstance(v, bool) and c.get("type") in ("integer", "number"):
                cands.append((f"set_{c['name']}", [{"op": "set_cell", "index": 0, "column": c["name"], "value": v + 1000}]))
        out += [{"check_id": f"hc_{name}_{label}", "mutation": {"table": name, "ops": ops}} for label, ops in cands]
    return out


def _mutated(tables, mutation):
    return [apply_ops(t, mutation["ops"]) if t["name"] == mutation["table"] else t for t in tables]


def pick(r, idx):
    """The result set a test grades: statement `idx` of the learner's file (0-based), or the last statement that returned rows when idx is None.
    None when that statement returned no rows."""
    if idx is None:
        return r if r.get("ok") else None
    outs = r.get("outputs") or []
    return outs[idx] if r.get("ok") and idx < len(outs) else None


def same_result(r, exp, ordered, tol=1e-9):
    return r is not None and [c.lower() for c in r["columns"]] == [c.lower() for c in exp["columns"]] and rows_equal(r["rows"], exp["rows"], ordered, tol)


SYNTAX_EXEMPT_PREFIXES = ("capstone.",)  # integration tasks reuse everything taught before: the code must run and pass its tests, the allowed-syntax gate is skipped


def syntax_exempt(ix):
    return any(a.startswith(SYNTAX_EXEMPT_PREFIXES) for a in ix.get("anchors", []))


def run_sql(registry, ix):
    o = Outcome()
    pub, gr = ix["public"], ix["grading"]
    pin = RUNTIMES["sql"]
    if pub["runtime"].get("version") != pin["version"]:
        o.problems.append(f"runtime.version {pub['runtime'].get('version')!r} must equal the pinned {pin['version']!r} (registry/runtimes.json)")
    entry, solution = _entry(ix, "solution")
    _, starter = _entry(ix, "starter")
    if solution is None or starter is None:
        o.problems.append(f"entry file {entry!r} missing from workspace.files or grading.solution_files")
        return o
    mounts = pub["workspace"].get("asset_mounts", [])
    tables, coltypes = _tables(registry, mounts, {}, o.problems)
    if not tables:
        o.problems.append("sql exercise mounts no dataset")
        return o
    tests = gr["tests"]
    ok_kinds = {"query_result_equals", "forbidden_syntax"}
    for t in tests:
        if t["kind"] not in ok_kinds:
            o.problems.append(f"{t['test_id']}: test kind {t['kind']!r} is not supported by the sql runtime (use {sorted(ok_kinds)})")
    if not any(t["kind"] == "query_result_equals" for t in tests):
        o.problems.append("no query_result_equals test: nothing checks what the query returns")
    scripts = [{"id": "solution", "statements": sqlsyntax.split_statements(solution)}, {"id": "starter", "statements": sqlsyntax.split_statements(starter)}]
    for t in tests:
        ov = t["spec"].get("mount_variants")
        if t["kind"] == "query_result_equals" and ov:
            tb, _ = _tables(registry, mounts, ov, o.problems)
            scripts.append({"id": f"test:{t['test_id']}", "statements": sqlsyntax.split_statements(solution), "tables": tb})
    if o.problems:
        return o
    ref, star = sqlsyntax.referenced_columns(solution)
    cands = candidate_mutations(tables, None if star or not ref else ref)
    scripts += [{"id": f"mut:{c['check_id']}", "statements": sqlsyntax.split_statements(solution), "tables": _mutated(tables, c["mutation"])} for c in cands]
    res = node_run({"tables": tables, "scripts": scripts}, pin["runner"])["results"]
    if not res["solution"]["ok"]:
        o.problems.append(f"solution does not run: {res['solution']['error'].splitlines()[0]}")
        return o
    starter_passes = res["starter"]["ok"]
    tested = []  # statement indices the result tests grade (None = last); hidden checks are derived for each
    for t in tests:
        spec, tid = t["spec"], t["test_id"]
        o.tests_total += 1
        if t["kind"] == "query_result_equals":
            exp = spec.get("expected")
            if not exp or "columns" not in exp or "rows" not in exp:
                o.problems.append(f"{tid}: spec.expected needs {{columns, rows}}")
                continue
            idx = spec.get("statement")
            if idx is not None and (not isinstance(idx, int) or isinstance(idx, bool) or idx < 0):
                o.problems.append(f"{tid}: spec.statement must be a 0-based statement index")
                continue
            tested.append((idx, bool(spec.get("ordered", False))))
            ordered, tol = bool(spec.get("ordered", False)), float(spec.get("tolerance", 1e-9))
            whole = res.get(f"test:{tid}", res["solution"])
            if not whole["ok"]:
                o.problems.append(f"{tid}: solution fails on this test's data: {whole['error'].splitlines()[0]}")
                continue
            r = pick(whole, idx)
            if r is None:
                o.problems.append(f"{tid}: the solution's statement {'#' + str(idx) if idx is not None else '(last)'} returns no rows; the file has "
                                  f"{len(whole.get('outputs', []))} statement(s)")
                continue
            if same_result(r, exp, ordered, tol):
                o.tests_passed += 1
            else:
                o.problems.append(f"{tid}: the solution's result differs from spec.expected — statement {idx if idx is not None else '(last)'} gives columns {r['columns']} "
                                  f"rows {r['rows'][:3]}{'...' if len(r['rows']) > 3 else ''}; expected columns {exp['columns']} rows {exp['rows'][:3]}")
            if starter_passes:  # does the starter (unsolved) code already satisfy this test?
                starter_passes = same_result(pick(res["starter"], idx), exp, ordered, tol)
        else:  # forbidden_syntax: the SOLUTION must not use the listed descriptors
            bad = sorted(set(spec.get("descriptors", [])) & {d for s in sqlsyntax.split_statements(solution) for d in sqlsyntax.used(s, coltypes)})
            if bad:
                o.problems.append(f"{tid}: solution uses forbidden syntax {bad}")
            else:
                o.tests_passed += 1
    if starter_passes:
        o.problems.append("the starter code already passes every result test: the learner has nothing to do")
    outs = res["solution"].get("outputs") or []
    row_stmts = [i for i, x in enumerate(outs) if x is not None]
    graded = {(row_stmts[-1] if i is None else i) for i, _ in tested if row_stmts or i is not None}
    for i in row_stmts:  # every query the learner writes must be graded, or a blank query still passes
        if i not in graded:
            o.problems.append(f"statement #{i} of the solution returns rows but no query_result_equals test grades it: a learner could leave that query blank and still pass. "
                              f"Add a test with spec.statement = {i} (0-based position in the file) and its expected result")
    hidden = []
    for idx, ordered in dict.fromkeys(tested):
        base, mine = pick(res["solution"], idx), []
        for c in cands:
            m = pick(res[f"mut:{c['check_id']}"], idx)
            if base is not None and m is not None and not same_result(m, base, ordered):
                mine.append({**c, **({"check_id": f"{c['check_id']}_s{idx}", "statement": idx} if idx is not None else {}),
                             "expected": {"columns": m["columns"], "rows": m["rows"]}, "ordered": ordered})
        hidden += mine[:MAX_HIDDEN]
        if not mine and base is not None:
            o.problems.append(f"the solution's result for statement {idx if idx is not None else '(last)'} does not change when the data changes (drop/duplicate a row, "
                              "change a cell): a hard-coded query would pass. Ask for a result that depends on the data, never a constant")
    o.hidden_checks = hidden
    cons = pub.get("constraints") or {}
    viol, unmapped = sqlsyntax.judge(solution, cons.get("allowed_syntax", []), cons.get("blocked_syntax", []), coltypes)
    if syntax_exempt(ix):
        viol, unmapped = [], []
    o.problems += [f"solution {v}" for v in viol]
    if unmapped:
        o.unverified = f"syntax descriptors with no detector: {unmapped}"
    if not o.problems:
        o.provenance = {"runtime": pin["engine"], "runtime_version": pin["version"], "solution_sha256": sha(solution), "tests_passed": o.tests_passed}
    return o


def grade_learner(registry, ix, learner_sql):
    """Reference grader for a SQL exercise: does the learner's query pass every visible test AND every hidden check?
    Returns (passed, [reasons]). The player's grader-core must behave identically (same data copies, same comparison)."""
    pub, gr = ix["public"], ix["grading"]
    pin = RUNTIMES["sql"]
    problems = []
    mounts = pub["workspace"].get("asset_mounts", [])
    tables, _ = _tables(registry, mounts, {}, problems)
    stmts = sqlsyntax.split_statements(learner_sql)
    scripts, meta = [{"id": "base", "statements": stmts}], {}
    for t in gr["tests"]:
        if t["kind"] == "query_result_equals" and t["spec"].get("mount_variants"):
            tb, _ = _tables(registry, mounts, t["spec"]["mount_variants"], problems)
            scripts.append({"id": f"test:{t['test_id']}", "statements": stmts, "tables": tb})
    byname = {t["name"]: t for t in tables}
    for h in gr.get("hidden_checks", []):
        scripts.append({"id": f"hidden:{h['check_id']}", "statements": stmts, "tables": _mutated(tables, h["mutation"])})
    res = node_run({"tables": tables, "scripts": scripts}, pin["runner"])["results"]
    reasons = []
    for t in gr["tests"]:
        spec = t["spec"]
        if t["kind"] == "query_result_equals":
            whole = res.get(f"test:{t['test_id']}", res["base"])
            if not same_result(pick(whole, spec.get("statement")), spec["expected"], bool(spec.get("ordered")), float(spec.get("tolerance", 1e-9))):
                reasons.append(f"{t['test_id']}: result differs")
        elif t["kind"] == "forbidden_syntax":
            bad = sorted(set(spec.get("descriptors", [])) & {d for x in stmts for d in sqlsyntax.used(x, {})})
            if bad:
                reasons.append(f"{t['test_id']}: uses forbidden syntax {bad}")
    for h in gr.get("hidden_checks", []):
        if not same_result(pick(res[f"hidden:{h['check_id']}"], h.get("statement")), h["expected"], bool(h.get("ordered"))):
            reasons.append(f"{h['check_id']}: result differs on changed data (the query does not really compute the answer)")
    return not reasons, reasons


def run_query(registry, result_of):
    """Computed table for a data_table `result_of`: returns ({columns, rows, execution_provenance}, problems)."""
    pin = RUNTIMES.get(result_of["runtime"])
    if not pin or pin["status"] != "verified":
        return None, [f"no verified runner for runtime {result_of['runtime']!r}"]
    problems = []
    tables, _ = _tables(registry, result_of["asset_mounts"], {}, problems)
    stmts = sqlsyntax.split_statements(result_of["sql"])
    if problems or not stmts:
        return None, problems or ["empty sql"]
    try:
        r = node_run({"tables": tables, "scripts": [{"id": "q", "statements": stmts}]}, pin["runner"])["results"]["q"]
    except SandboxError as ex:
        return None, [f"sandbox: {ex}"]
    if not r["ok"]:
        return None, [f"query does not run: {r['error'].splitlines()[0]}"]
    return {"columns": r["columns"], "rows": r["rows"],
            "execution_provenance": {"runtime": pin["engine"], "runtime_version": pin["version"], "sql_sha256": sha(result_of["sql"])}}, []


# ---------------------------------------------------------------- Python
PY_INSTALLED = {"numpy", "pandas", "scipy", "matplotlib", "seaborn"}  # sandbox/fetch_packages.mjs
PY_KINDS = {"stdout_equals", "value_equals", "dataframe_equals", "function_call", "forbidden_syntax"}
# chart_renderer = the same Pyodide runner plus matplotlib/seaborn; the figures are serialised to JSON (sandbox/run_py.mjs _figs_json) and graded on structure, never pixels
CHART_KINDS = {"figure_equals", "axes_property", "plotted_data_equals"}
CHART_STATIC = {"title", "xlabel", "ylabel", "legend", "chart_types", "xscale", "yscale"}  # properties the data cannot change: exempt from "must vary" (>=1 test must still vary)
FIGURE_KEYS = {"n_axes", "suptitle", "chart_types"}


def _chart_value(kind, spec, r):
    """The comparable value a chart test grades, read from the serialised figures of a script result, or (None, why)."""
    figs = (r.get("fig") or {}).get("figures") or []
    if not figs:
        return None, "no figure was drawn (" + (r.get("fig_error") or "nothing was plotted") + ")"
    try:
        f = figs[spec.get("figure", -1)]
        if kind == "figure_equals":
            return {k: ([a["chart_types"] for a in f["axes"]] if k == "chart_types" else f[k]) for k in spec["expected"]}, None
        ax = f["axes"][spec.get("axes", 0)]
        if kind == "axes_property":
            return ax[spec["property"]], None
        arts = [a for a in ax["artists"] if a["type"] == spec["chart"]]
        v = arts[spec.get("series", 0)][spec["field"]]
        return (sorted(v) if spec.get("sorted") and isinstance(v, list) else v), None
    except (IndexError, KeyError):
        return None, f"the figure has no such part ({kind} {json.dumps({k: v for k, v in spec.items() if k != 'expected'})})"


def deep_equal(a, b, tol=1e-9):
    if _num(a) and _num(b):
        return abs(a - b) <= tol
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(deep_equal(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(deep_equal(a[k], b[k], tol) for k in a)
    return a == b


def _norm_out(t):
    return "\n".join(x.rstrip() for x in (t or "").strip().splitlines())


def py_apply_var(code, name, value):
    """Replace the constant in the top-level `name = <constant>` assignment (the first one), keeping the rest of the file byte-for-byte."""
    import ast
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return code
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name and isinstance(n.value, ast.Constant):
            lines = code.splitlines(keepends=True)
            if n.value.lineno != n.value.end_lineno:
                return code
            ln = lines[n.value.lineno - 1]
            lines[n.value.lineno - 1] = ln[:n.value.col_offset] + json.dumps(value) + ln[n.value.end_col_offset:]
            return "".join(lines)
    return code


def py_var_mutations(code):
    """Candidate set_variable mutations: each top-level `name = <number|string>` assignment gets a different constant."""
    import ast
    out = []
    try:
        body = ast.parse(code).body
    except SyntaxError:
        return out
    for n in body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Constant) and not isinstance(n.value.value, bool):
            v = n.value.value
            if isinstance(v, (int, float)):
                new = v + 7
            elif isinstance(v, str):
                new = v + "_x"
            else:
                continue
            out.append({"check_id": f"hc_var_{n.targets[0].id}", "mutation": {"ops": [{"op": "set_variable", "name": n.targets[0].id, "value": new}]}})
    return out[:4]


def _py_script(sid, entry, code, mounts, probes, extra=None, chart=False):
    files = [{"path": entry, "content": code}] + (extra or [])
    return {"id": sid, "entry": entry, "files": files, "mounts": mounts, "probes": probes, **({"chart": True, "png": sid == "solution"} if chart else {})}


def _py_mounts(tables):
    return [{"path": t["name"], "columns": [c["name"] for c in t["columns"]], "rows": t["rows"]} for t in tables]


def _py_result(kind, spec, r, tid):
    """The comparable value a test grades, from a script result, or (None, why)."""
    if not r.get("ok"):
        return None, f"the file does not run: {r.get('error', '?').splitlines()[-1]}"
    if kind == "stdout_equals":
        return _norm_out(r["stdout"]), None
    if kind in CHART_KINDS:
        return _chart_value(kind, spec, r)
    p = r["probes"].get(tid)
    if not p or not p["ok"]:
        return None, f"cannot evaluate: {(p or {}).get('error', 'no result')}"
    return p["value"], None


def _py_match(kind, spec, got):
    tol = float(spec.get("tolerance", 1e-9))
    if kind == "stdout_equals":
        return got == _norm_out(spec["expected"])
    if kind == "dataframe_equals":
        exp = spec["expected"]
        return isinstance(got, dict) and got.get("columns") == exp["columns"] and rows_equal(got["rows"], exp["rows"], bool(spec.get("ordered", False)), tol)
    return deep_equal(got, spec["expected"], tol)


def _py_expected(kind, spec, got):
    if kind == "dataframe_equals":
        return {"columns": got["columns"], "rows": got["rows"]}
    return {"value": got}


def run_python(registry, ix):
    from . import pysyntax
    o = Outcome()
    pub, gr = ix["public"], ix["grading"]
    rt = pub["runtime"]
    chart = rt["kind"] == "chart_renderer"
    pin = RUNTIMES[rt["kind"]] if chart else RUNTIMES["python"]
    kinds = PY_KINDS | (CHART_KINDS if chart else set())
    if rt.get("version") != pin["version"]:
        o.problems.append(f"runtime.version {rt.get('version')!r} must equal the pinned {pin['version']!r} (registry/runtimes.json)")
    pkgs = list(rt.get("packages") or [])
    bad = sorted(set(pkgs) - PY_INSTALLED)
    if bad:
        o.problems.append(f"runtime.packages {bad} are not installed in the sandbox (installed: {sorted(PY_INSTALLED)})")
    entry, solution = _entry(ix, "solution")
    _, starter = _entry(ix, "starter")
    if solution is None or starter is None:
        o.problems.append(f"entry file {entry!r} missing from workspace.files or grading.solution_files")
        return o
    mounts = pub["workspace"].get("asset_mounts", [])
    tables, _ = _tables(registry, mounts, {}, o.problems)
    tests = gr["tests"]
    for t in tests:
        if t["kind"] not in kinds:
            o.problems.append(f"{t['test_id']}: test kind {t['kind']!r} is not supported by the {rt['kind']} runtime (use {sorted(kinds)})")
    graded = [t for t in tests if t["kind"] != "forbidden_syntax"]
    if not graded:
        o.problems.append("no test checks what the program produces")
    for t in graded:
        sp = t["spec"]
        need = {"stdout_equals": ["expected"], "value_equals": ["expr", "expected"], "dataframe_equals": ["expr", "expected"], "function_call": ["function", "expected"],
                "figure_equals": ["expected"], "axes_property": ["property", "expected"], "plotted_data_equals": ["chart", "field", "expected"]}[t["kind"]]
        miss = [k for k in need if k not in sp]
        if miss:
            o.problems.append(f"{t['test_id']}: spec needs {miss}")
        if t["kind"] == "dataframe_equals" and not ("columns" in sp.get("expected", {}) and "rows" in sp.get("expected", {})):
            o.problems.append(f"{t['test_id']}: spec.expected needs {{columns, rows}}")
        if t["kind"] == "figure_equals" and (not isinstance(sp.get("expected"), dict) or set(sp["expected"]) - FIGURE_KEYS):
            o.problems.append(f"{t['test_id']}: figure_equals spec.expected is an object with keys from {sorted(FIGURE_KEYS)}")
    if o.problems:
        return o
    probes = [({"id": t["test_id"], "kind": "call", "function": t["spec"]["function"], "args": t["spec"].get("args", []), "kwargs": t["spec"].get("kwargs", {})}
               if t["kind"] == "function_call" else {"id": t["test_id"], "kind": "expr", "expr": t["spec"]["expr"]}) for t in graded if t["kind"] not in {"stdout_equals"} | CHART_KINDS]
    mk = lambda sid, code, tb: _py_script(sid, entry, code, _py_mounts(tb), probes, chart=chart)
    cands = [{**c, "tag": "data"} for c in candidate_mutations(tables, None)] + [{**c, "tag": "var"} for c in py_var_mutations(solution)]

    def mutated_script(c):
        if c["tag"] == "var":
            code = solution
            for op in c["mutation"]["ops"]:
                code = py_apply_var(code, op["name"], op["value"])
            return mk(f"mut:{c['check_id']}", code, tables)
        return mk(f"mut:{c['check_id']}", solution, _mutated(tables, c["mutation"]))

    scripts = [mk("solution", solution, tables), mk("starter", starter, tables)]
    for t in graded:
        ov = t["spec"].get("mount_variants")
        if ov:
            tb, _ = _tables(registry, mounts, ov, o.problems)
            scripts.append(mk(f"test:{t['test_id']}", solution, tb))
    if o.problems:
        return o
    scripts += [mutated_script(c) for c in cands]
    res = node_run({"packages": list(dict.fromkeys(["numpy", "pandas"] + (["matplotlib"] if chart else []) + pkgs)), "scripts": scripts}, pin["runner"])["results"]
    if not res["solution"]["ok"]:
        o.problems.append(f"solution does not run: {res['solution']['error'].splitlines()[-1]}")
        return o
    o.preview_png = res["solution"].get("png")
    starter_passes = res["starter"]["ok"]
    code_tags = None
    for t in tests:
        tid, kind, spec = t["test_id"], t["kind"], t["spec"]
        o.tests_total += 1
        if kind == "forbidden_syntax":
            try:
                have = pysyntax.tags(solution)
            except SyntaxError as ex:
                o.problems.append(f"solution does not parse: {ex}")
                continue
            hit = sorted(d for d in spec.get("descriptors", []) if (pysyntax.descriptor_tags(d) or None) and pysyntax.descriptor_tags(d) <= have)
            if hit:
                o.problems.append(f"{tid}: solution uses forbidden syntax {hit}")
            else:
                o.tests_passed += 1
            continue
        got, why = _py_result(kind, spec, res.get(f"test:{tid}", res["solution"]), tid)
        if why:
            o.problems.append(f"{tid}: solution {why}")
            continue
        if _py_match(kind, spec, got):
            o.tests_passed += 1
        else:
            o.problems.append(f"{tid}: the solution's result differs from spec.expected — gives {json.dumps(got)[:200]}; expected {json.dumps(spec['expected'])[:200]}")
        if starter_passes:
            sv, sw = _py_result(kind, spec, res["starter"], tid)
            starter_passes = sw is None and _py_match(kind, spec, sv)
    if starter_passes:
        o.problems.append("the starter code already passes every result test: the learner has nothing to do")
    # hidden checks + anti-hard-coding
    calls = {}
    for t in graded:
        if t["kind"] == "function_call":
            calls.setdefault(t["spec"]["function"], set()).add(json.dumps([t["spec"].get("args", []), t["spec"].get("kwargs", {})], sort_keys=True))
    hidden = []
    for t in graded:
        tid, kind, spec = t["test_id"], t["kind"], t["spec"]
        base, _ = _py_result(kind, spec, res["solution"], tid)
        mine = []
        for c in cands:
            m, why = _py_result(kind, spec, res[f"mut:{c['check_id']}"], tid)
            if why is None and base is not None and not _py_match_vs(kind, spec, m, base):
                mine.append({"check_id": f"{c['check_id']}_{tid}", "mutation": c["mutation"], "test_id": tid, "expected": _py_expected(kind, spec, m),
                             "ordered": bool(spec.get("ordered", False))})
        var = [h for h in mine if h["check_id"].startswith("hc_var_")]  # starter-variable checks always make the cut: they catch a program that ignores its inputs
        hidden += var[:2] + [h for h in mine if h not in var][:MAX_HIDDEN - len(var[:2])]
        static = kind == "figure_equals" or (kind == "axes_property" and spec.get("property") in CHART_STATIC)
        if not mine and not static and not (kind == "function_call" and len(calls[spec["function"]]) >= 2):
            o.problems.append(f"{tid}: the solution's result does not change when the data or the starter's values change: a hard-coded answer would pass. "
                              "Make the result depend on the mounted data or on a starter variable, or (function tests) test the function with at least two different argument sets")
    o.hidden_checks = hidden
    if chart and not hidden:
        o.problems.append("no chart test depends on the data or the starter's values: a hard-coded figure would pass. Add a plotted_data_equals test (or xticklabels/ylim) on data the program reads or computes")
    cons = pub.get("constraints") or {}
    try:
        viol, unmapped, _ = pysyntax.judge(solution, cons.get("allowed_syntax", []), cons.get("blocked_syntax", []), starter)
    except SyntaxError as ex:
        viol, unmapped = [f"does not parse: {ex}"], []
    if syntax_exempt(ix) and not any(v.startswith("does not parse") for v in viol):
        viol, unmapped = [], []
    o.problems += [f"solution {v}" for v in viol]
    if unmapped:
        o.unverified = f"syntax descriptors with no detector: {unmapped}"
    if not o.problems:
        o.provenance = {"runtime": pin["engine"], "runtime_version": pin["version"], "solution_sha256": sha(solution), "tests_passed": o.tests_passed}
    return o


def _py_match_vs(kind, spec, a, b):
    """Do two results of the same test agree (used to decide whether a mutation changes the solution's output)?"""
    tol = float(spec.get("tolerance", 1e-9))
    if kind == "dataframe_equals":
        return a.get("columns") == b.get("columns") and rows_equal(a["rows"], b["rows"], bool(spec.get("ordered", False)), tol)
    return deep_equal(a, b, tol)


def grade_learner_py(registry, ix, learner_code):
    pub, gr = ix["public"], ix["grading"]
    chart = pub["runtime"]["kind"] == "chart_renderer"
    pin = RUNTIMES[pub["runtime"]["kind"]] if chart else RUNTIMES["python"]
    problems = []
    mounts = pub["workspace"].get("asset_mounts", [])
    tables, _ = _tables(registry, mounts, {}, problems)
    entry, _ = _entry(ix, "starter")
    graded = [t for t in gr["tests"] if t["kind"] != "forbidden_syntax"]
    probes = [({"id": t["test_id"], "kind": "call", "function": t["spec"]["function"], "args": t["spec"].get("args", []), "kwargs": t["spec"].get("kwargs", {})}
               if t["kind"] == "function_call" else {"id": t["test_id"], "kind": "expr", "expr": t["spec"]["expr"]}) for t in graded if t["kind"] not in {"stdout_equals"} | CHART_KINDS]
    mk = lambda sid, code, tb: _py_script(sid, entry, code, _py_mounts(tb), probes, chart=chart)
    scripts = [mk("base", learner_code, tables)]
    for t in graded:
        if t["spec"].get("mount_variants"):
            tb, _ = _tables(registry, mounts, t["spec"]["mount_variants"], problems)
            scripts.append(mk(f"test:{t['test_id']}", learner_code, tb))
    for h in gr.get("hidden_checks", []):
        m = h["mutation"]
        if m["ops"][0]["op"] == "set_variable":
            code = learner_code
            for op in m["ops"]:
                code = py_apply_var(code, op["name"], op["value"])
            scripts.append(mk(f"hidden:{h['check_id']}", code, tables))
        else:
            scripts.append(mk(f"hidden:{h['check_id']}", learner_code, _mutated(tables, m)))
    pkgs = list(dict.fromkeys(["numpy", "pandas"] + (["matplotlib"] if chart else []) + list(pub["runtime"].get("packages") or [])))
    res = node_run({"packages": pkgs, "scripts": scripts}, pin["runner"])["results"]
    reasons = []
    for t in gr["tests"]:
        if t["kind"] == "forbidden_syntax":
            from . import pysyntax
            have = pysyntax.tags(learner_code)
            hit = sorted(d for d in t["spec"].get("descriptors", []) if (pysyntax.descriptor_tags(d) or None) and pysyntax.descriptor_tags(d) <= have)
            if hit:
                reasons.append(f"{t['test_id']}: uses forbidden syntax {hit}")
            continue
        got, why = _py_result(t["kind"], t["spec"], res.get(f"test:{t['test_id']}", res["base"]), t["test_id"])
        if why or not _py_match(t["kind"], t["spec"], got):
            reasons.append(f"{t['test_id']}: result differs")
    for h in gr.get("hidden_checks", []):
        t = next(x for x in graded if x["test_id"] == h["test_id"])
        got, why = _py_result(t["kind"], t["spec"], res[f"hidden:{h['check_id']}"], t["test_id"])
        exp = h["expected"]
        want = {"columns": exp["columns"], "rows": exp["rows"]} if "rows" in exp else exp["value"]
        fake = {**t["spec"], "expected": want}
        if why or not _py_match(t["kind"], fake, got):
            reasons.append(f"{h['check_id']}: result differs on changed data (the program does not really compute the answer)")
    return not reasons, reasons


# ---------------------------------------------------------------- Spreadsheet
# The exercise's editable file is a sheet file (`[Sheet!]A1: value-or-=formula`, see sandbox/run_sheet.mjs, checkers/sheetsyntax.py); each mounted CSV is a sheet.
# Tests: cell_equals {cell, expected}, range_equals {range, expected: [[...]]}, formula_uses {cell, functions: [NAMES]} (static), forbidden_syntax {descriptors}.
SHEET_KINDS = {"cell_equals", "range_equals", "formula_uses", "forbidden_syntax"}
SHEET_VALUE = {"cell_equals", "range_equals"}


def _sheet_payload(tables):
    return [{"name": os.path.splitext(os.path.basename(t["name"]))[0], "columns": [c["name"] for c in t["columns"]], "rows": t["rows"]} for t in tables]


def _sheet_script(sid, content, tables, probes):
    return {"id": sid, "content": content, "sheets": _sheet_payload(tables), "probes": probes}


def _sheet_probes(tests):
    return [{"id": t["test_id"], "kind": "cell" if t["kind"] == "cell_equals" else "range", "ref": t["spec"]["cell" if t["kind"] == "cell_equals" else "range"]}
            for t in tests if t["kind"] in SHEET_VALUE]


def sheet_apply_var(text, ref, value):
    """Replace the typed constant in the sheet file's cell `ref` ('A1' or 'Sheet!A1'), keeping every other line. A formula cell is left alone."""
    from . import sheetsyntax
    want = ref.rsplit("!", 1)[-1].replace("$", "").upper()
    out, done = [], False
    for ln in text.splitlines(keepends=True):
        body = ln.rstrip("\r\n")
        m = sheetsyntax.LINE.match(body)
        if not done and m and (m.group(2).upper() + m.group(3)) == want and not m.group(4).strip().startswith("="):
            out.append(body[:m.start(4)] + (json.dumps(value) if isinstance(value, str) else str(value)) + ln[len(body):])
            done = True
        else:
            out.append(ln)
    return "".join(out)


def sheet_var_mutations(text):
    """Candidate set_variable mutations: each typed numeric constant cell of the file (the starter's inputs) gets a different number."""
    from . import sheetsyntax
    out = []
    for sh, ref, c in sheetsyntax.parse_cells(text):
        try:
            v = float(c)
        except ValueError:
            continue
        v = int(v) if v == int(v) else v
        name = f"{sh}!{ref}" if sh else ref
        out.append({"check_id": f"hc_cell_{ref}", "mutation": {"ops": [{"op": "set_variable", "name": name, "value": v + 7}]}})
    return out[:4]


def _formula_uses_ok(spec, content):
    from . import sheetsyntax
    tg = sheetsyntax.cell_tags(content, spec["cell"])
    return tg is not None and all(f"fn:{f.upper()}" in tg for f in spec["functions"])


def _sheet_result(r, tid):
    if not r.get("ok"):
        return None, f"the sheet does not load: {r.get('error', '?').splitlines()[-1]}"
    p = r["probes"].get(tid)
    return (p["value"], None) if p and p["ok"] else (None, f"cannot evaluate: {(p or {}).get('error', 'no result')}")


def _sheet_forbidden(spec, content):
    from . import sheetsyntax
    have = sheetsyntax.used_tags(content)
    return sorted(d for d in spec.get("descriptors", []) if (sheetsyntax.descriptor_tags(d) or None) and sheetsyntax.descriptor_tags(d) <= have)


def run_sheet(registry, ix):
    from . import sheetsyntax
    o = Outcome()
    pub, gr = ix["public"], ix["grading"]
    pin = RUNTIMES["spreadsheet"]
    if pub["runtime"].get("version") != pin["version"]:
        o.problems.append(f"runtime.version {pub['runtime'].get('version')!r} must equal the pinned {pin['version']!r} (registry/runtimes.json)")
    entry, solution = _entry(ix, "solution")
    _, starter = _entry(ix, "starter")
    if solution is None or starter is None:
        o.problems.append(f"entry file {entry!r} missing from workspace.files or grading.solution_files")
        return o
    tables, _ = _tables(registry, pub["workspace"].get("asset_mounts", []), {}, o.problems)
    tests = gr["tests"]
    for t in tests:
        if t["kind"] not in SHEET_KINDS:
            o.problems.append(f"{t['test_id']}: test kind {t['kind']!r} is not supported by the spreadsheet runtime (use {sorted(SHEET_KINDS)})")
            continue
        sp = t["spec"]
        need = {"cell_equals": ["cell", "expected"], "range_equals": ["range", "expected"], "formula_uses": ["cell", "functions"], "forbidden_syntax": []}[t["kind"]]
        miss = [k for k in need if k not in sp]
        if miss:
            o.problems.append(f"{t['test_id']}: spec needs {miss}")
        elif t["kind"] == "range_equals" and not (isinstance(sp["expected"], list) and all(isinstance(r, list) for r in sp["expected"])):
            o.problems.append(f"{t['test_id']}: spec.expected must be a list of rows (a 2-D list)")
        elif t["kind"] == "formula_uses" and not (isinstance(sp["functions"], list) and sp["functions"]):
            o.problems.append(f"{t['test_id']}: spec.functions must list the function names the cell's formula must use")
    graded = [t for t in tests if t["kind"] in SHEET_VALUE]
    if not graded:
        o.problems.append("no cell_equals / range_equals test checks what the sheet computes")
    if o.problems:
        return o
    probes = _sheet_probes(tests)
    cands = [{**c, "tag": "data"} for c in candidate_mutations(tables, None)] + [{**c, "tag": "var"} for c in sheet_var_mutations(solution)]

    def mutated_script(c):
        if c["tag"] == "var":
            code = solution
            for op in c["mutation"]["ops"]:
                code = sheet_apply_var(code, op["name"], op["value"])
            return _sheet_script(f"mut:{c['check_id']}", code, tables, probes)
        return _sheet_script(f"mut:{c['check_id']}", solution, _mutated(tables, c["mutation"]), probes)

    scripts = [_sheet_script("solution", solution, tables, probes), _sheet_script("starter", starter, tables, probes)] + [mutated_script(c) for c in cands]
    res = node_run({"scripts": scripts}, pin["runner"])["results"]
    if not res["solution"]["ok"]:
        o.problems.append(f"solution does not load: {res['solution']['error'].splitlines()[-1]}")
        return o
    starter_passes = res["starter"]["ok"]
    for t in tests:
        tid, kind, spec = t["test_id"], t["kind"], t["spec"]
        o.tests_total += 1
        if kind == "forbidden_syntax":
            hit = _sheet_forbidden(spec, solution)
            if hit:
                o.problems.append(f"{tid}: solution uses forbidden syntax {hit}")
            else:
                o.tests_passed += 1
            continue
        if kind == "formula_uses":
            if _formula_uses_ok(spec, solution):
                o.tests_passed += 1
            else:
                o.problems.append(f"{tid}: cell {spec['cell']} of the solution does not hold a formula using {spec['functions']}")
            starter_passes = starter_passes and _formula_uses_ok(spec, starter)
            continue
        got, why = _sheet_result(res["solution"], tid)
        if why:
            o.problems.append(f"{tid}: solution {why}")
            continue
        tol = float(spec.get("tolerance", 1e-9))
        if deep_equal(got, spec["expected"], tol):
            o.tests_passed += 1
        else:
            o.problems.append(f"{tid}: the solution's result differs from spec.expected — gives {json.dumps(got)[:200]}; expected {json.dumps(spec['expected'])[:200]}")
        if starter_passes:
            sv, sw = _sheet_result(res["starter"], tid)
            starter_passes = sw is None and deep_equal(sv, spec["expected"], tol)
    if starter_passes:
        o.problems.append("the starter sheet already passes every test: the learner has nothing to do")
    hidden = []
    for t in graded:
        tid, spec = t["test_id"], t["spec"]
        tol = float(spec.get("tolerance", 1e-9))
        base, _ = _sheet_result(res["solution"], tid)
        mine = []
        for c in cands:
            m, why = _sheet_result(res[f"mut:{c['check_id']}"], tid)
            if why is None and base is not None and not deep_equal(m, base, tol):
                mine.append({"check_id": f"{c['check_id']}_{tid}", "mutation": c["mutation"], "test_id": tid, "expected": {"value": m}})
        var = [h for h in mine if h["check_id"].startswith("hc_cell_")]
        hidden += var[:2] + [h for h in mine if h not in var][:MAX_HIDDEN - len(var[:2])]
        if not mine:
            o.problems.append(f"{tid}: the solution's result does not change when the mounted data or an input cell changes: a typed-in answer would pass. "
                              "Make the result a formula over the mounted data or over input cells the starter file holds")
    o.hidden_checks = hidden
    cons = pub.get("constraints") or {}
    viol, unmapped, _ = sheetsyntax.judge(solution, cons.get("allowed_syntax", []), cons.get("blocked_syntax", []))
    if syntax_exempt(ix):
        viol, unmapped = [], []
    o.problems += [f"solution {v}" for v in viol]
    if unmapped:
        o.unverified = f"syntax descriptors with no detector: {unmapped}"
    if not o.problems:
        o.provenance = {"runtime": pin["engine"], "runtime_version": pin["version"], "solution_sha256": sha(solution), "tests_passed": o.tests_passed}
    return o


def grade_learner_sheet(registry, ix, learner_sheet):
    """Reference grader for a spreadsheet exercise: does the learner's sheet file pass every visible test AND every hidden check?
    Returns (passed, [reasons]). The player's grader-core must behave identically (same engine, same data copies, same comparison)."""
    pub, gr = ix["public"], ix["grading"]
    pin = RUNTIMES["spreadsheet"]
    problems = []
    tables, _ = _tables(registry, pub["workspace"].get("asset_mounts", []), {}, problems)
    probes = _sheet_probes(gr["tests"])
    scripts = [_sheet_script("base", learner_sheet, tables, probes)]
    for h in gr.get("hidden_checks", []):
        m = h["mutation"]
        if m["ops"][0]["op"] == "set_variable":
            code = learner_sheet
            for op in m["ops"]:
                code = sheet_apply_var(code, op["name"], op["value"])
            scripts.append(_sheet_script(f"hidden:{h['check_id']}", code, tables, probes))
        else:
            scripts.append(_sheet_script(f"hidden:{h['check_id']}", learner_sheet, _mutated(tables, m), probes))
    res = node_run({"scripts": scripts}, pin["runner"])["results"]
    reasons = []
    for t in gr["tests"]:
        spec = t["spec"]
        if t["kind"] == "forbidden_syntax":
            hit = _sheet_forbidden(spec, learner_sheet)
            if hit:
                reasons.append(f"{t['test_id']}: uses forbidden syntax {hit}")
        elif t["kind"] == "formula_uses":
            if not _formula_uses_ok(spec, learner_sheet):
                reasons.append(f"{t['test_id']}: cell {spec['cell']} must hold a formula using {spec['functions']}")
        else:
            got, why = _sheet_result(res["base"], t["test_id"])
            if why or not deep_equal(got, spec["expected"], float(spec.get("tolerance", 1e-9))):
                reasons.append(f"{t['test_id']}: result differs")
    for h in gr.get("hidden_checks", []):
        t = next(x for x in gr["tests"] if x["test_id"] == h["test_id"])
        got, why = _sheet_result(res[f"hidden:{h['check_id']}"], t["test_id"])
        if why or not deep_equal(got, h["expected"]["value"], float(t["spec"].get("tolerance", 1e-9))):
            reasons.append(f"{h['check_id']}: result differs on changed data (the sheet does not really compute the answer)")
    return not reasons, reasons


run_chart, grade_learner_chart = run_python, grade_learner_py  # the same code path; the exercise's runtime.kind picks chart mode
RUNNERS = {"sql": run_sql, "python": run_python, "spreadsheet": run_sheet, "chart_renderer": run_python}


def run_exercise(registry, ix):
    kind = ix["public"]["runtime"]["kind"]
    if kind not in RUNNERS:
        return Outcome(unverified=f"no runner for runtime {kind!r} yet")
    try:
        return RUNNERS[kind](registry, ix)
    except SandboxError as ex:
        return Outcome(problems=[f"sandbox: {ex}"])

def formula_entry_outcome(registry, ix):
    """Verify a formula_entry by running its reference formula in the spreadsheet engine: the formula must produce expected_value on the mounted
    dataset, use the required functions, and (via the data mutations of run_sheet) not be a typed-in number. Returns an Outcome."""
    o = Outcome()
    pub, gr = ix["public"], ix["grading"]
    ref = (gr.get("reference_formula") or "").strip()
    if not ref:
        o.problems.append("grading.reference_formula is missing: the answer formula must be given so the gate can compute expected_value in the engine")
        return o
    ref = ref if ref.startswith("=") else "=" + ref
    sheet, cell = pub.get("sheet_name") or "Sheet1", pub["target_cell"]
    mount = {"asset_id": pub["asset_ref"]["asset_id"], "mount_path": sheet + ".csv"}
    if pub["asset_ref"].get("variant_id"):
        mount["variant_id"] = pub["asset_ref"]["variant_id"]
    note = "// the learner types the formula in the target cell\n"
    tests = [{"test_id": "t_value", "kind": "cell_equals", "message_on_fail": "wrong value", "spec": {"cell": cell, "expected": gr["expected_value"], **({"tolerance": gr["tolerance"]} if "tolerance" in gr else {})}}]
    if gr.get("must_use_functions"):
        tests.append({"test_id": "t_fn", "kind": "formula_uses", "message_on_fail": "wrong function", "spec": {"cell": cell, "functions": gr["must_use_functions"]}})
    fns = pub.get("allowed_functions") or sorted(set(re.findall(r"([A-Z][A-Z0-9.]*)\(", ref)) | set(gr.get("must_use_functions") or []))
    syn = {"allowed_syntax": [f"{f}(range)" for f in fns] + ["cell references", "absolute references", "mixed references", "whole-column or column range",
           "cross-sheet or sheet reference", "+ - * /", "comparison operators", "& (concatenation)", "parentheses", "numbers", "text in quotes", "TRUE / FALSE"], "blocked_syntax": []}
    synth = {"type": "code_exercise", "interaction_id": ix["interaction_id"], "public": {"prompt": pub["prompt"], "runtime": {"kind": "spreadsheet", "version": RUNTIMES["spreadsheet"]["version"]},
             "workspace": {"entry": "book.sheet", "files": [{"path": "book.sheet", "role": "editable", "content": note}], "asset_mounts": [mount]}, "constraints": syn},
             "grading": {"solution_files": [{"path": "book.sheet", "content": note + f"{cell}: {ref}\n"}], "tests": tests}}
    return run_exercise(registry, synth)


def sheet_cell_values(registry, block):
    """Values the engine computes for a spreadsheet_grid block's formula cells on its dataset (shown values are computed, never typed). Returns (values, problems)."""
    cells = [c for c in block.get("cells", []) if c.get("formula")]
    if not cells:
        return {}, []
    problems = []
    ref = block["asset_ref"]
    mount = {"asset_id": ref["asset_id"], "mount_path": (block.get("sheet_name") or "Sheet1") + ".csv"}
    if ref.get("variant_id"):
        mount["variant_id"] = ref["variant_id"]
    tables, _ = _tables(registry, [mount], {}, problems)
    if problems:
        return {}, problems
    text = "".join(f"{c['ref']}: {c['formula'] if c['formula'].startswith('=') else '=' + c['formula']}\n" for c in cells)
    probes = [{"id": c["ref"], "kind": "cell", "ref": c["ref"]} for c in cells]
    try:
        r = node_run({"scripts": [_sheet_script("grid", text, tables, probes)]}, RUNTIMES["spreadsheet"]["runner"])["results"]["grid"]
    except SandboxError as ex:
        return {}, [f"sandbox: {ex}"]
    if not r.get("ok"):
        return {}, [f"the formulas do not load: {r.get('error', '?').splitlines()[-1]}"]
    values = {}
    for c in cells:
        pr = r["probes"].get(c["ref"])
        if pr and pr["ok"]:
            values[c["ref"]] = pr["value"]
        else:
            problems.append(f"cell {c['ref']}: cannot evaluate {c['formula']!r}: {(pr or {}).get('error', 'no result')}")
    return values, problems
