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


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def node_run(job, runner):
    if not shutil.which("node") or not (SANDBOX / "node_modules").exists():
        raise SandboxError("node or sandbox/node_modules missing: run `npm ci` in 00_FINAL_PIPELINE_CORE/sandbox")
    env = {"PATH": os.environ.get("PATH", ""), "HOME": "/nonexistent", "LANG": "C"}  # no credentials, no proxies
    try:
        r = subprocess.run(["node", "--max-old-space-size=512", str(SANDBOX / Path(runner).name)], input=json.dumps(job), capture_output=True,
                           text=True, cwd=SANDBOX, env=env, timeout=NODE_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        raise SandboxError(f"runner exceeded {NODE_TIMEOUT_S}s (infinite loop or a query that is far too heavy)")
    if r.returncode or not r.stdout.strip():
        raise SandboxError(f"runner crashed ({r.returncode}): {(r.stderr or r.stdout)[-400:]}")
    return json.loads(r.stdout)


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


def candidate_mutations(tables):
    """Deterministic, role-agnostic candidates per table, in a fixed order: drop first row, duplicate last row, change the first string and the first
    numeric cell of row 0, drop the last row. Only mutations that change the solution's result are kept (and stored as hidden_checks)."""
    out = []
    for t in tables:
        if not t["rows"]:
            continue
        n, name = len(t["rows"]), t["name"]
        cands = [("drop_first", [{"op": "drop_row", "index": 0}]), ("dup_last", [{"op": "duplicate_row", "index": n - 1}])]
        for kind, test in (("str", lambda c, v: c.get("type", "string") == "string" and isinstance(v, str)),
                           ("num", lambda c, v: c.get("type") in ("integer", "number") and isinstance(v, (int, float)) and not isinstance(v, bool))):
            for j, c in enumerate(t["columns"]):
                v = t["rows"][0][j]
                if test(c, v):
                    cands.append((f"set_{kind}_{c['name']}", [{"op": "set_cell", "index": 0, "column": c["name"], "value": (v + "_x") if kind == "str" else v + 1000}]))
                    break
        cands.append(("drop_last", [{"op": "drop_row", "index": n - 1}]))
        out += [{"check_id": f"hc_{name}_{label}", "mutation": {"table": name, "ops": ops}} for label, ops in cands]
    return out


def _mutated(tables, mutation):
    return [apply_ops(t, mutation["ops"]) if t["name"] == mutation["table"] else t for t in tables]


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
    cands = candidate_mutations(tables)
    scripts += [{"id": f"mut:{c['check_id']}", "statements": sqlsyntax.split_statements(solution), "tables": _mutated(tables, c["mutation"])} for c in cands]
    res = node_run({"tables": tables, "scripts": scripts}, pin["runner"])["results"]
    if not res["solution"]["ok"]:
        o.problems.append(f"solution does not run: {res['solution']['error'].splitlines()[0]}")
        return o
    starter_passes = res["starter"]["ok"]
    for t in tests:
        spec, tid = t["spec"], t["test_id"]
        o.tests_total += 1
        if t["kind"] == "query_result_equals":
            exp = spec.get("expected")
            if not exp or "columns" not in exp or "rows" not in exp:
                o.problems.append(f"{tid}: spec.expected needs {{columns, rows}}")
                continue
            ordered, tol = bool(spec.get("ordered", False)), float(spec.get("tolerance", 1e-9))
            r = res.get(f"test:{tid}", res["solution"])
            if not r["ok"]:
                o.problems.append(f"{tid}: solution fails on this test's data: {r['error'].splitlines()[0]}")
                continue
            good = [c.lower() for c in r["columns"]] == [c.lower() for c in exp["columns"]] and rows_equal(r["rows"], exp["rows"], ordered, tol)
            if good:
                o.tests_passed += 1
            else:
                o.problems.append(f"{tid}: the solution's result differs from spec.expected — solution gives columns {r['columns']} rows {r['rows'][:3]}"
                                  f"{'...' if len(r['rows']) > 3 else ''}; expected columns {exp['columns']} rows {exp['rows'][:3]}")
            if starter_passes:  # does the starter (unsolved) code already satisfy this test?
                s = res["starter"]
                starter_passes = [c.lower() for c in s["columns"]] == [c.lower() for c in exp["columns"]] and rows_equal(s["rows"], exp["rows"], ordered, tol)
        else:  # forbidden_syntax: the SOLUTION must not use the listed descriptors
            bad = sorted(set(spec.get("descriptors", [])) & {d for s in sqlsyntax.split_statements(solution) for d in sqlsyntax.used(s, coltypes)})
            if bad:
                o.problems.append(f"{tid}: solution uses forbidden syntax {bad}")
            else:
                o.tests_passed += 1
    if starter_passes:
        o.problems.append("the starter code already passes every result test: the learner has nothing to do")
    first = next((t for t in tests if t["kind"] == "query_result_equals"), None)
    ordered = bool(first and first["spec"].get("ordered", False))
    base = res["solution"]
    hidden = []
    for c in cands:
        m = res[f"mut:{c['check_id']}"]
        if m["ok"] and not ([x.lower() for x in m["columns"]] == [x.lower() for x in base["columns"]] and rows_equal(m["rows"], base["rows"], ordered)):
            hidden.append({**c, "expected": {"columns": m["columns"], "rows": m["rows"]}, "ordered": ordered})
    o.hidden_checks = hidden[:MAX_HIDDEN]
    if not hidden:
        o.problems.append("the solution's result does not change when the data changes (drop/duplicate a row, change a cell): a hard-coded query would pass. "
                          "Ask for a result that depends on the data, e.g. include columns or rows that the data determines")
    cons = pub.get("constraints") or {}
    viol, unmapped = sqlsyntax.judge(solution, cons.get("allowed_syntax", []), cons.get("blocked_syntax", []), coltypes)
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
            r = res.get(f"test:{t['test_id']}", res["base"])
            exp = spec["expected"]
            if not r["ok"] or [c.lower() for c in r["columns"]] != [c.lower() for c in exp["columns"]] or not rows_equal(r["rows"], exp["rows"], bool(spec.get("ordered")), float(spec.get("tolerance", 1e-9))):
                reasons.append(f"{t['test_id']}: result differs")
        elif t["kind"] == "forbidden_syntax":
            bad = sorted(set(spec.get("descriptors", [])) & {d for x in stmts for d in sqlsyntax.used(x, {})})
            if bad:
                reasons.append(f"{t['test_id']}: uses forbidden syntax {bad}")
    for h in gr.get("hidden_checks", []):
        r = res[f"hidden:{h['check_id']}"]
        if not r["ok"] or [c.lower() for c in r["columns"]] != [c.lower() for c in h["expected"]["columns"]] or not rows_equal(r["rows"], h["expected"]["rows"], bool(h.get("ordered"))):
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


RUNNERS = {"sql": run_sql}


def run_exercise(registry, ix):
    kind = ix["public"]["runtime"]["kind"]
    if kind not in RUNNERS:
        return Outcome(unverified=f"no runner for runtime {kind!r} yet")
    try:
        return RUNNERS[kind](registry, ix)
    except SandboxError as ex:
        return Outcome(problems=[f"sandbox: {ex}"])
