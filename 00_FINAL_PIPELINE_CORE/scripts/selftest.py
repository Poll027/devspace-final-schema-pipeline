"""Mutation self-test for the deterministic gates: copy a PASSing batch, break it in a known way, assert the right error appears.
A validator that cannot fail is worthless — run this after ANY change to validate_tile.py / assemble_tiles.py / the schemas.

  python3 selftest.py batches/<passing_batch_id>
"""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

S = Path(__file__).resolve().parent
PY = sys.executable


def run(script, *args):
    p = subprocess.run([PY, str(S / script), *map(str, args)], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def jl(p):
    return json.loads(Path(p).read_text())


def dump(p, o):
    Path(p).write_text(json.dumps(o, indent=2, ensure_ascii=False))


def step(screens, suffix):
    return next(s for s in screens["tiles"][0]["steps"] if s["step_id"].endswith(suffix))


def ixo(inters, suffix):
    return next(i["interaction"] for i in inters["tiles"][0]["interactions"] if i["step_id"].endswith(suffix))


# each mutation: (name, fn(reg, screens, inters) -> None, expected substring, which gate)
def m_wrong_key(reg, sc, ix):
    next(a for a in ixo(ix, ".s04")["grading"]["answers"] if a["task_id"] == "t3")["expect_value"] = 42


def m_classify_contradicts(reg, sc, ix):
    ixo(ix, ".s07")["grading"]["assignments"]["i5"] = "b_num"


def m_untaught_fact(reg, sc, ix):  # s02 no longer claims to teach f3/f4, so the s03 check tests something never taught
    for b in step(sc, ".s02")["blocks"]:
        if b["type"] == "prose":
            b["lineage"]["fact_ids"] = []


def m_drop_misconception(reg, sc, ix):
    s = step(sc, ".s05")
    s["blocks"] = [b for b in s["blocks"] if b["type"] != "callout"]


def m_video_phrase(reg, sc, ix):
    step(sc, ".s01")["blocks"][0]["text"] += " As the video shows, this is the key idea."


def m_missing_step(reg, sc, ix):
    sc["tiles"][0]["steps"] = [s for s in sc["tiles"][0]["steps"] if not s["step_id"].endswith(".s06")]
    ix["tiles"][0]["interactions"] = [i for i in ix["tiles"][0]["interactions"] if not i["step_id"].endswith(".s06")]


def m_unknown_fact(reg, sc, ix):
    step(sc, ".s01")["blocks"][0]["lineage"]["fact_ids"] = ["data.dataset_rows_columns#f9"]


def m_unmeasured_anchor(reg, sc, ix):
    ixo(ix, ".s04")["measures"] = [m for m in ixo(ix, ".s04")["measures"] if m["capability"] != "identify_row_as_observation"]


def m_bad_planted_rule(reg, sc, ix):
    reg["assets"][0]["variants"][0]["planted_issues"][1]["rule"]["value"] = -5


def m_wrong_choice_key(reg, sc, ix):
    ixo(ix, ".s03")["grading"]["correct_option_ids"] = ["o9"]


def m_ghost_column(reg, sc, ix):
    step(sc, ".s01")["blocks"][1]["asset_ref"]["columns"] = ["order_id", "no_such_column"]


def m_wrong_planned_type(reg, sc, ix):
    ixo(ix, ".s07")["type"] = "match_pairs"  # schema should reject before anything else


MUTATIONS = [
    ("answer key typed wrong (table_select expect_value)", m_wrong_key, "answer key was typed wrong"),
    ("classify key contradicts column role", m_classify_contradicts, "answer key contradicts the dataset"),
    ("interaction tests a fact no earlier step taught", m_untaught_fact, "never have been taught"),
    ("misconception never taught", m_drop_misconception, "is never taught by a text block"),
    ("text refers to the video", m_video_phrase, "text must teach on its own"),
    ("planned step deleted", m_missing_step, "planned step"),
    ("lineage cites a fact that does not exist", m_unknown_fact, "does not exist in the glossary bundle"),
    ("assessment anchor never measured", m_unmeasured_anchor, "is never measured"),
    ("planted issue that does not hold (registry gate)", m_bad_planted_rule, "planted issue does not hold"),
    ("choice key points at a missing option", m_wrong_choice_key, "not among the options"),
    ("data_table shows a column the dataset lacks", m_ghost_column, "not in dataset"),
    ("interaction schema violated", m_wrong_planned_type, "schema"),
]


def unit_interactions(src):
    """Demo-parity interactions (find_issues / field_selection / ordering) against the canary registry: valid ones pass, broken ones are caught."""
    sys.path.insert(0, str(S))
    import validate_tile as VT
    from schema_check import errors as schema_errors
    C = VT.Ctx(src)
    items = {i["name"]: i for i in jl(S.parent.parent / "examples" / "demo_parity_interactions.json")["items"]}
    cases = []

    def case(name, base, mutate, expect):
        ix = copy.deepcopy(items[base]["interaction"])
        mutate(ix)
        cases.append((name, base, ix, expect))
    case("baseline find_issues", "find_issues", lambda x: None, None)
    case("baseline field_selection", "field_selection", lambda x: None, None)
    case("baseline ordering", "ordering", lambda x: None, None)
    case("find_issues: issue location moved off the planted cell", "find_issues", lambda x: x["grading"]["issues"][0]["locations"][0]["where"].update({"order_id": "NS1002"}), "locations differ from the registry")
    case("find_issues: answer is not a planted issue", "find_issues", lambda x: x["grading"]["issues"][0].update({"issue_id": "i_made_up"}), "not a planted issue")
    case("find_issues: decoy sits on a real issue", "find_issues", lambda x: x["grading"]["decoys"][0].update({"location": {"where": {"order_id": "NS1003"}, "column": "city"}}), "decoy sits on a real planted issue")
    case("find_issues: goal_count wrong", "find_issues", lambda x: x["public"].update({"goal_count": 3}), "goal_count")
    case("field_selection: rule missing for a field", "field_selection", lambda x: x["grading"]["rules"].pop(), "rules must cover exactly the fields")
    case("ordering: not a permutation", "ordering", lambda x: x["grading"]["correct_order"].__setitem__(0, "bogus"), "not a permutation")
    case("ordering: follow-up key points nowhere", "ordering", lambda x: x["grading"].update({"follow_up_correct_option_ids": ["zz"]}), "not among the follow-up options")
    bad = 0
    for name, base, ix, expect in cases:
        errs = [f"schema: {e}" for e in schema_errors(ix, f"ix.{ix['type']}.schema.json")]
        rep = VT.Report(name)
        if not errs:
            VT.check_interaction(C, {"step_id": "demo.s00"}, ix, rep)
            errs = rep.E
        ok = (not errs) if expect is None else any(expect in e for e in errs)
        bad += not ok
        print(("caught " if ok and expect else "ok     " if ok else "MISSED ") + name + ("" if ok else f"  -> {errs[:2]}"))
    return bad


def unit_fail_closed(src):
    """A type with no registered checker must be UNVERIFIED (warning) and an ERROR under --strict — never a silent pass."""
    sys.path.insert(0, str(S))
    import validate_tile as VT
    C = VT.Ctx(src)
    tile = C.ctx["tile_ids"][0]
    removed = VT.checkers.INTERACTION.pop("choice")
    try:
        rep_lax, st = VT.validate_tile(C, tile, strict=False)
        rep_strict, _ = VT.validate_tile(C, tile, strict=True)
    finally:
        VT.checkers.INTERACTION["choice"] = removed
    ok = (not rep_lax.E) and st["unverified"] >= 1 and any("strict" in e for e in rep_strict.E)
    print(("caught " if ok else "MISSED ") + "fail-closed: interaction type with no checker is UNVERIFIED, error under --strict")
    return 0 if ok else 1


def unit_graph_blocks():
    """Diagrams without edges (venn, layers, array...) are valid and must not crash the checker; broken ones must still be caught."""
    sys.path.insert(0, str(S))
    from checkers import core

    class Rep:
        def __init__(self): self.E, self.W = [], []
        def e(self, m): self.E.append(m)
        def w(self, m): self.W.append(m)
    step = {"step_id": "t.s01"}
    cases = [("edgeless diagram is accepted", {"type": "diagram", "nodes": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}]}, 0),
             ("edgeless diagram with duplicate node ids is rejected", {"type": "diagram", "nodes": [{"id": "a", "label": "A"}, {"id": "a", "label": "B"}]}, 1),
             ("edge to an unknown node is rejected", {"type": "diagram", "nodes": [{"id": "a", "label": "A"}], "edges": [{"from": "a", "to": "zz"}]}, 1)]
    bad = 0
    for name, b, want in cases:
        rep = Rep()
        try:
            core.diagram({}, step, b, rep)
            ok = len(rep.E) == want
        except Exception as ex:
            ok = False
            name += f" (checker crashed: {type(ex).__name__})"
        bad += not ok
        print(("caught " if ok else "MISSED ") + "graph blocks: " + name)
    return bad


def unit_stale_cleanup(src):
    """assemble_tiles.py must delete compiled files of tiles that are not in the batch."""
    d = src.parent / "_selftest_tmp" / "stale"
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(src, d, ignore=shutil.ignore_patterns("reports", "final_stage_gate_ledger.json"))
    for sub in ("tile_lessons", "tile_lessons_public", "grading"):
        (d / sub / "tile_not_in_batch.json").write_text("{}")
    rc, _ = run("assemble_tiles.py", d)
    ok = rc == 0 and not any((d / sub / "tile_not_in_batch.json").exists() for sub in ("tile_lessons", "tile_lessons_public", "grading"))
    print(("caught " if ok else "MISSED ") + "assemble leaves a compiled lesson of a tile that is not in the batch")
    return 0 if ok else 1


def unit_sql_runner():
    """The SQL sandbox: a good exercise passes and gets provenance; every way to be wrong or to escape is caught."""
    import copy
    sys.path.insert(0, str(S))
    from checkers import code, sandbox

    reg = {"assets": [{"asset_id": "ds_customers", "asset_kind": "dataset", "columns": [
        {"name": "customer_id", "type": "integer"}, {"name": "city", "type": "string"}, {"name": "spend", "type": "number"}, {"name": "joined", "type": "date"}],
        "rows": [[1, "Lagos", 10.5, "2024-01-05"], [2, "Abuja", 20.0, "2024-02-10"], [3, "Lagos", 7.0, "2024-03-15"]],
        "variants": [{"variant_id": "v_two", "derived_from": "base", "ops": [{"op": "drop_rows", "where": {"customer_id": 3}}]}]}]}
    allowed = ["SELECT", "FROM", "AS output_name", "WHERE", "< > <= >= = <> !=", "ORDER BY"]
    good = {"type": "code_exercise", "interaction_id": "ix.t.s01", "anchors": ["sql.demo#practice"], "difficulty": "core", "grading_mode": "client", "standalone": False,
        "measures": [{"concept_id": "sql.demo", "capability": "write_filtered_select", "fact_ids": ["f1"]}],
        "feedback": {"correct": {"message": "Right."}, "incorrect": {"message": "Not yet."}, "hints": ["Filter with WHERE."]}, "public": {
        "prompt": "p", "runtime": {"kind": "sql", "version": "1.32.0"},
        "workspace": {"files": [{"path": "q.sql", "role": "editable", "content": "SELECT 1 AS customer_id"}], "entry": "q.sql",
                      "asset_mounts": [{"asset_id": "ds_customers", "mount_path": "customers"}]},
        "constraints": {"allowed_syntax": allowed, "blocked_syntax": ["GROUP BY"]}},
        "grading": {"solution_files": [{"path": "q.sql", "content": "SELECT customer_id, city AS town FROM customers WHERE spend > 8 ORDER BY customer_id"}],
                    "tests": [{"test_id": "t1", "kind": "query_result_equals", "message_on_fail": "no",
                               "spec": {"expected": {"columns": ["customer_id", "town"], "rows": [[1, "Lagos"], [2, "Abuja"]]}, "ordered": True}}]}}

    class Rep:
        def __init__(self): self.E, self.W = [], []
        def e(self, m): self.E.append(m)
        def w(self, m): self.W.append(m)

    class _B:
        by_id = {"sql.demo": {"practice_anchor": {"live_code": {"allowed_syntax": allowed, "blocked_syntax": ["GROUP BY"]}}}}

    class C:
        registry = reg
        bundles = _B()

    def check(ix):
        rep = Rep()
        code.code_exercise(C, {"step_id": "t.s01"}, ix, rep)
        return rep

    def variant(mutate):
        ix = copy.deepcopy(good)
        mutate(ix)
        return ix
    fails = 0
    from schema_check import errors as schema_errors
    se = schema_errors(good, "ix.code_exercise.schema.json")
    print(("caught " if not se else "MISSED ") + f"sql: the fixture is a schema-valid code_exercise ({se[:2] or ''})")
    fails += bool(se)
    out = sandbox.run_exercise(reg, good)
    ok = not out.problems and out.provenance and out.provenance["tests_passed"] == 1
    print(("caught " if ok else "MISSED ") + f"sql: a correct exercise passes and gets provenance ({out.problems or ''})")
    fails += not ok
    stamped = variant(lambda ix: ix["grading"].update(execution_provenance=out.provenance, hidden_checks=out.hidden_checks))
    ok = not check(stamped).E
    print(("caught " if ok else "MISSED ") + "sql: the validator accepts matching provenance")
    fails += not ok
    cases = [
        ("a solution that does not return the expected rows", lambda ix: ix["grading"]["solution_files"][0].update(content="SELECT customer_id, city AS town FROM customers WHERE spend > 15"), "differs from spec.expected"),
        ("a wrong expected row typed in the key", lambda ix: ix["grading"]["tests"][0]["spec"]["expected"]["rows"].append([9, "Kano"]), "differs from spec.expected"),
        ("a starter that already solves the task", lambda ix: ix["public"]["workspace"]["files"][0].update(content=ix["grading"]["solution_files"][0]["content"]), "starter code already passes"),
        ("a solution using blocked syntax", lambda ix: (ix["grading"]["solution_files"][0].update(content="SELECT customer_id, city AS town FROM customers WHERE spend > 8 GROUP BY customer_id, city"), ix["grading"]["tests"][0]["spec"].update(ordered=False)), "blocks for this practice"),
        ("a solution using syntax not yet taught", lambda ix: ix["public"]["constraints"].update(allowed_syntax=["SELECT", "FROM", "AS output_name", "WHERE", "< > <= >= = <> !="]), "not yet taught"),
        ("constraints widened beyond the glossary's allowed syntax", lambda ix: ix["public"]["constraints"].update(allowed_syntax=allowed + ["GROUP BY"]), "differs from sql.demo's glossary practice anchor"),
        ("an unpinned runtime version", lambda ix: ix["public"]["runtime"].update(version="9.9.9"), "pinned"),
        ("a solution that reads a host file", lambda ix: ix["grading"]["solution_files"][0].update(content="SELECT * FROM read_csv_auto('/etc/passwd')"), "solution does not run"),
        ("a solution that fetches from the network", lambda ix: ix["grading"]["solution_files"][0].update(content="SELECT * FROM read_csv_auto('https://example.com/x.csv')"), "solution does not run"),
        ("a solution that tries to unlock the sandbox", lambda ix: ix["grading"]["solution_files"][0].update(content="SET enable_external_access=true"), "solution does not run"),
        ("a hidden test whose data variant gives different rows", lambda ix: ix["grading"]["tests"].append({"test_id": "t2", "kind": "query_result_equals", "message_on_fail": "no", "spec": {"mount_variants": {"customers": "v_two"}, "ordered": True, "expected": {"columns": ["customer_id", "town"], "rows": [[1, "Lagos"], [2, "Abuja"], [3, "Lagos"]]}}}), "differs from spec.expected"),
        ("an unsupported test kind", lambda ix: ix["grading"]["tests"].append({"test_id": "t3", "kind": "dataframe_equals", "message_on_fail": "no", "spec": {}}), "not supported by the sql runtime"),
        ("a forbidden_syntax test the solution violates", lambda ix: ix["grading"]["tests"].append({"test_id": "t4", "kind": "forbidden_syntax", "message_on_fail": "no", "spec": {"descriptors": ["WHERE"]}}), "forbidden syntax"),
    ]
    for name, mut, expect in cases:
        rep = check(stamped_for(variant, out, mut))
        ok = any(expect in e for e in rep.E)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "sql: " + name + ("" if ok else f"\n    expected {expect!r}; got {rep.E}"))
    job = {"tables": [{"name": "t", "columns": [{"name": c, "type": ty} for c, ty in (("a", "integer"), ("p", "number"), ("d", "date"), ("ts", "datetime"), ("ok", "boolean"))],
                       "rows": [[1, 12.5, "2024-03-05", "2024-03-05 10:11:12", True], [2, None, None, None, None]]}],
           "scripts": [{"id": "x", "statements": ["SELECT SUM(a) AS s, AVG(a) AS av, COUNT(*) AS n, SUM(p) AS sp, MAX(d) AS md, MAX(ts) AS mts, CAST(12.50 AS DECIMAL(10,2)) AS dec, MAX(ok) AS ok FROM t"]}]}
    got = sandbox.node_run(job, "sandbox/run_sql.mjs")["results"]["x"]["rows"]
    want = [[3, 1.5, 2, 12.5, "2024-03-05", "2024-03-05 10:11:12", 12.5, True]]
    ok = got == want
    print(("caught " if ok else "MISSED ") + f"sql: SUM/AVG/DECIMAL/DATE/TIMESTAMP/NULL/BOOLEAN come back as plain values ({got if not ok else ''})")
    fails += not ok
    pkg = json.loads((S.parent / "sandbox" / "package.json").read_text())["dependencies"]["@duckdb/duckdb-wasm"]
    ok = pkg == sandbox.RUNTIMES["sql"]["version"] == sandbox.node_run({"tables": [], "scripts": []}, "sandbox/run_sql.mjs")["version"]
    print(("caught " if ok else "MISSED ") + f"sql: registry/runtimes.json, package.json and the running engine agree on the version ({pkg})")
    fails += not ok
    import time
    keep, sandbox.NODE_TIMEOUT_S = sandbox.NODE_TIMEOUT_S, 8
    t0 = time.time()
    heavy = variant(lambda ix: ix["grading"]["solution_files"][0].update(content="WITH RECURSIVE r(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM r) SELECT COUNT(*) AS n FROM r"))
    rep = check(heavy)
    sandbox.NODE_TIMEOUT_S = keep
    ok = any("exceeded" in e or "does not run" in e or "crashed" in e for e in rep.E) and time.time() - t0 < 40
    print(("caught " if ok else "MISSED ") + f"sql: a runaway query is stopped by the timeout ({time.time() - t0:.0f}s: {rep.E[:1]})")
    fails += not ok
    # hidden checks: a hard-coded answer must fail, a correct alternative phrasing must pass
    stamped_ix = variant(lambda ix: ix["grading"].update(execution_provenance=out.provenance, hidden_checks=out.hidden_checks))
    ok = len(out.hidden_checks) >= 1 and all("expected" in h and h["mutation"]["ops"] for h in out.hidden_checks)
    print(("caught " if ok else "MISSED ") + f"hidden: {len(out.hidden_checks)} sensitive checks derived from the solution")
    fails += not ok
    for name, sql, want in [
            ("the reference solution passes every visible and hidden check", good["grading"]["solution_files"][0]["content"], True),
            ("a differently written correct query passes", "SELECT c.customer_id, c.city AS town FROM customers AS c WHERE c.spend > 8 ORDER BY 1", True),
            ("a hard-coded answer that matches the visible rows is rejected", "SELECT 1 AS customer_id, 'Lagos' AS town UNION ALL SELECT 2, 'Abuja' ORDER BY 1", False),
            ("a query that ignores the filter is rejected", "SELECT customer_id, city AS town FROM customers ORDER BY customer_id", False)]:
        passed, reasons = sandbox.grade_learner(reg, stamped_ix, sql)
        ok = passed == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + "hidden: " + name + ("" if ok else f" (passed={passed}: {reasons})"))
    const = variant(lambda ix: (ix["grading"]["solution_files"][0].update(content="SELECT 1 AS customer_id, 'Lagos' AS town"),
                                ix["grading"]["tests"][0]["spec"].update(expected={"columns": ["customer_id", "town"], "rows": [[1, "Lagos"]]}),
                                ix["public"]["constraints"].update(allowed_syntax=allowed)))
    rep = check(const)
    ok = any("a hard-coded query would pass" in e for e in rep.E)
    print(("caught " if ok else "MISSED ") + "hidden: an exercise whose answer ignores the data is flagged as hard-codable")
    fails += not ok
    for name, mut, expect in [("hidden_checks typed or edited by hand", lambda g: g["hidden_checks"][0]["expected"]["rows"].append([9, "Kano"]), "do not match a fresh derivation"),
                              ("hidden_checks missing from a compiled lesson", lambda g: g.pop("hidden_checks"), "hidden_checks missing")]:
        ix2 = copy.deepcopy(stamped_ix)
        mut(ix2["grading"])
        ok = any(expect in e for e in check(ix2).E)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "hidden: " + name)
    # multi-statement exercises (batch 006: "write two queries"): each test names its statement; hidden checks cover each tested statement
    def two_queries(ix):
        ix["grading"]["solution_files"][0]["content"] = ("SELECT customer_id FROM customers WHERE city = 'Lagos' ORDER BY customer_id;\n"
                                                        "SELECT customer_id FROM customers WHERE spend > 8 ORDER BY customer_id;")
        ix["public"]["workspace"]["files"][0]["content"] = "-- query 1: Lagos customers\n-- query 2: customers who spent more than 8"
        ix["grading"]["tests"] = [
            {"test_id": "q1", "kind": "query_result_equals", "message_on_fail": "q1", "spec": {"statement": 0, "ordered": True, "expected": {"columns": ["customer_id"], "rows": [[1], [3]]}}},
            {"test_id": "q2", "kind": "query_result_equals", "message_on_fail": "q2", "spec": {"statement": 1, "ordered": True, "expected": {"columns": ["customer_id"], "rows": [[1], [2]]}}}]
    multi = variant(two_queries)
    mout = sandbox.run_exercise(reg, multi)
    stmts_hidden = sorted({h.get("statement") for h in mout.hidden_checks})
    ok = not mout.problems and stmts_hidden == [0, 1]
    print(("caught " if ok else "MISSED ") + f"multi: a two-query exercise passes and gets hidden checks for statements {stmts_hidden} ({mout.problems or ''})")
    fails += not ok
    multi_stamped = variant(lambda ix: (two_queries(ix), ix["grading"].update(execution_provenance=mout.provenance, hidden_checks=mout.hidden_checks)))
    for name, sql, want in [
            ("both queries written properly pass", multi["grading"]["solution_files"][0]["content"], True),
            ("query 1 hard-coded (query 2 real) is rejected", "SELECT 1 AS customer_id UNION ALL SELECT 3 ORDER BY 1;\nSELECT customer_id FROM customers WHERE spend > 8 ORDER BY customer_id;", False),
            ("only the last query written is rejected (query 1 missing)", "SELECT customer_id FROM customers WHERE spend > 8 ORDER BY customer_id;", False)]:
        passed, reasons = sandbox.grade_learner(reg, multi_stamped, sql)
        ok = passed == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + "multi: " + name + ("" if ok else f" (passed={passed}: {reasons})"))
    one_test = variant(lambda ix: (two_queries(ix), ix["grading"].update(tests=[ix["grading"]["tests"][1]])))
    ok = any("statement #0 of the solution returns rows but no query_result_equals test grades it" in e for e in check(one_test).E)
    fails += not ok
    print(("caught " if ok else "MISSED ") + "multi: a two-query exercise with a test for only one query is rejected, naming the missing statement")
    for name, mut, expect in [
            ("a test aimed at a statement the file does not have", lambda ix: ix["grading"]["tests"][1]["spec"].update(statement=5), "returns no rows; the file has 2 statement"),
            ("a wrong expected result for statement 0", lambda ix: ix["grading"]["tests"][0]["spec"]["expected"]["rows"].append([9]), "statement 0 gives columns")]:
        bad = variant(lambda ix: (two_queries(ix), mut(ix)))
        ok = any(expect in e for e in check(bad).E)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "multi: " + name)
    # NULL-sensitive exercises (batch 006: "IS NULL" / "IS NOT NULL"): a mutation must be able to change an IS NULL result
    reg_n = {"assets": [{"asset_id": "ds_orders", "asset_kind": "dataset", "columns": [{"name": "order_id", "type": "integer"}, {"name": "delivery", "type": "integer"}],
                         "rows": [[1001, 15], [1002, None], [1003, 22], [1004, None], [1005, 31]]}]}
    nullq = variant(lambda ix: (ix["public"]["workspace"].update(asset_mounts=[{"asset_id": "ds_orders", "mount_path": "orders"}]),
                                ix["public"]["workspace"]["files"][0].update(content="-- query: orders with no delivery time"),
                                ix["public"].update(constraints={"allowed_syntax": ["SELECT", "FROM", "WHERE", "IS NULL", "IS NOT NULL"], "blocked_syntax": []}),
                                ix.pop("anchors", None),
                                ix["grading"].update(solution_files=[{"path": "q.sql", "content": "SELECT order_id FROM orders WHERE delivery IS NULL;"}],
                                                     tests=[{"test_id": "t_null", "kind": "query_result_equals", "message_on_fail": "m", "spec": {"ordered": False, "expected": {"columns": ["order_id"], "rows": [[1002], [1004]]}}}])))
    nout = sandbox.run_exercise(reg_n, nullq)
    ok = not nout.problems and any("null_delivery" in h["check_id"] for h in nout.hidden_checks)
    print(("caught " if ok else "MISSED ") + f"null: an IS NULL exercise is accepted because a NULL mutation changes its result ({nout.problems or ''})")
    fails += not ok
    nstamped = variant(lambda ix: None)
    nullq["grading"].update(execution_provenance=nout.provenance, hidden_checks=nout.hidden_checks)
    for name, sql, want in [("the IS NULL solution passes", "SELECT order_id FROM orders WHERE delivery IS NULL;", True),
                            ("a hard-coded IS NULL answer is rejected", "SELECT 1002 AS order_id UNION ALL SELECT 1004 ORDER BY 1;", False)]:
        passed, reasons = sandbox.grade_learner(reg_n, nullq, sql)
        ok = passed == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + "null: " + name + ("" if ok else f" (passed={passed}: {reasons})"))
    # syntax detection: a typed date literal is not a CAST (batch 006: "days since order" needs a reference date)
    from checkers import sqlsyntax as sx
    for q, want in [("SELECT COUNT(*) AS n FROM orders", False), ("SELECT * FROM orders", True), ("SELECT o.* FROM orders AS o", True)]:
        ok = ("* and table_name.*" in sx.used(q, {})) == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + f"syntax: the star feature is {'detected' if want else 'not reported'} for {q[:32]}")
    for name, q, want_cast, want_colon in [("DATE literal", "SELECT DATE '2024-02-01' - order_date AS d FROM orders", False, False),
                                           ("TIMESTAMP literal", "SELECT TIMESTAMP '2024-02-01 10:00:00' AS t", False, False),
                                           ("CAST(...)", "SELECT CAST('2024-02-01' AS DATE) AS d", True, False),
                                           ("TRY_CAST(...)", "SELECT TRY_CAST('x' AS INTEGER) AS d", True, False),
                                           ("::", "SELECT '2024-02-01'::DATE AS d", False, True)]:
        f = sx.used(q, {"order_date": "date"})
        ok = ("CAST(expression AS type)" in f) == want_cast and ("expression::type" in f) == want_colon
        fails += not ok
        print(("caught " if ok else "MISSED ") + f"syntax: {name} is classified correctly ({sorted(x for x in f if 'CAST' in x or '::' in x)})")
    # data_table.result_of: query-result tables are computed, never typed (the batch-005 DISTINCT-panel finding)
    from checkers import data as datachk
    tbl = {"type": "data_table", "result_of": {"runtime": "sql", "sql": "SELECT DISTINCT city FROM customers ORDER BY city", "asset_mounts": [{"asset_id": "ds_customers", "mount_path": "customers"}]}}
    res, probs = sandbox.run_query(reg, tbl["result_of"])
    ok = not probs and res["columns"] == ["city"] and res["rows"] == [["Abuja"], ["Lagos"]]
    print(("caught " if ok else "MISSED ") + f"result_of: DISTINCT is computed by the engine, not truncated or typed ({probs or res['rows']})")
    fails += not ok

    def tcheck(b):
        rep = Rep()
        datachk.data_table(C, {"step_id": "t.s05"}, b, rep)
        return rep
    ok = not tcheck({**tbl, "result": res}).E
    print(("caught " if ok else "MISSED ") + "result_of: a correctly computed result is accepted")
    fails += not ok
    for name, b, expect in [
            ("a typed result that is not what the query returns", {**tbl, "result": {**res, "rows": [["Lagos"], ["Abuja"], ["Kano"]]}}, "does not match a fresh run"),
            ("a result_of table with no computed result", dict(tbl), "result missing"),
            ("a result_of whose SQL does not run", {**tbl, "result_of": {**tbl["result_of"], "sql": "SELECT nope FROM customers"}, "result": res}, "does not run"),
            ("a result_of mounting a dataset that is not registered", {**tbl, "result_of": {**tbl["result_of"], "asset_mounts": [{"asset_id": "ds_ghost", "mount_path": "customers"}]}, "result": res}, "no dataset asset"),
            ("a highlight on a column the result does not have", {**tbl, "result": res, "highlight": [{"target": {"kind": "column", "column": "spend"}}]}, "not a result column")]:
        rep = tcheck(b)
        ok = any(expect in e for e in rep.E)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "result_of: " + name + ("" if ok else f"\n    expected {expect!r}; got {rep.E}"))
    tampered = variant(lambda ix: ix["grading"].update(execution_provenance={**out.provenance, "solution_sha256": "0" * 64}))
    ok = any("does not match a fresh run" in e for e in check(tampered).E)
    print(("caught " if ok else "MISSED ") + "sql: provenance that does not match a fresh run")
    fails += not ok
    ok = any("missing" in e for e in check(copy.deepcopy(good)).E)
    print(("caught " if ok else "MISSED ") + "sql: provenance missing from a compiled lesson")
    fails += not ok
    py = variant(lambda ix: ix["public"]["runtime"].update(kind="bash", version="1"))
    rep = check(py)
    ok = not rep.E and any("UNVERIFIED" in w for w in rep.W)
    print(("caught " if ok else "MISSED ") + "sql: an unsupported runtime is UNVERIFIED, not a pass")
    fails += not ok
    unm = variant(lambda ix: ix["public"]["constraints"].update(allowed_syntax=allowed + ["MYSTERY SYNTAX"]))
    rep = check(stamped_for(variant, out, lambda ix: ix["public"]["constraints"].update(allowed_syntax=allowed + ["MYSTERY SYNTAX"])))
    ok = any("no detector" in w for w in rep.W)
    print(("caught " if ok else "MISSED ") + "sql: a syntax descriptor with no detector is UNVERIFIED")
    fails += not ok
    return fails


def unit_python_runner():
    """The Python (Pyodide) runner and the Python syntax checker: correct work passes, every kind of wrong work is caught, and the sandbox holds."""
    import copy
    from checkers import pysyntax, sandbox
    reg = {"assets": [{"asset_id": "ds_customers", "asset_kind": "dataset", "columns": [
        {"name": "customer_id", "type": "integer"}, {"name": "city", "type": "string"}, {"name": "spend", "type": "number"}],
        "rows": [[1, "Lagos", 10.5], [2, "Abuja", 20.0], [3, "Lagos", 7.0], [4, "Kano", 31.0]]}]}
    starter = "import pandas as pd\ncustomers = pd.read_csv('customers.csv')\nlimit = 8\n# keep customers whose spend is above the limit\n"
    sol = starter + "big = customers[customers['spend'] > limit]\n"
    allowed = ["import pandas as pd", "pd.read_csv(path)", "name = value assignment", "whole-number literals as in the examples", "single- or double-quoted strings",
               "df[df['col'] > value]", "df['col']"]
    good = {"type": "code_exercise", "interaction_id": "ix.p", "public": {"prompt": "p", "runtime": {"kind": "python", "version": "0.29.5", "packages": ["pandas"]},
            "workspace": {"entry": "main.py", "files": [{"path": "main.py", "role": "editable", "content": starter}],
                          "asset_mounts": [{"asset_id": "ds_customers", "mount_path": "customers.csv"}]},
            "constraints": {"allowed_syntax": allowed, "blocked_syntax": []}},
            "grading": {"solution_files": [{"path": "main.py", "role": "editable", "content": sol}],
                        "tests": [{"test_id": "t1", "kind": "dataframe_equals", "message_on_fail": "no",
                                   "spec": {"expr": "big[['customer_id']]", "expected": {"columns": ["customer_id"], "rows": [[2], [4], [1]][::-1][::-1]}, "ordered": True}}]}}
    good["grading"]["tests"][0]["spec"]["expected"]["rows"] = [[1], [2], [4]]
    fails = 0

    def verdict(name, ix, want_text=None, want_ok=False):
        nonlocal fails
        out = sandbox.run_exercise(reg, ix)
        ok = (not out.problems) if want_ok else any(want_text in x for x in out.problems)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "python: " + name + ("" if ok else f" ({out.problems})"))
        return out

    def variant(f):
        ix = copy.deepcopy(good)
        f(ix)
        return ix
    out = verdict("a correct exercise passes and gets provenance + hidden checks", good, want_ok=True)
    ok = out.provenance and len(out.hidden_checks) >= 2
    fails += not ok
    print(("caught " if ok else "MISSED ") + f"python: {len(out.hidden_checks)} hidden checks derived (data and starter-variable mutations)")
    verdict("a wrong expected row typed in the key", variant(lambda ix: ix["grading"]["tests"][0]["spec"]["expected"]["rows"].append([9])), "differs from spec.expected")
    verdict("a starter that already solves the task", variant(lambda ix: ix["public"]["workspace"]["files"][0].update(content=sol)), "starter code already passes")
    verdict("an unpinned runtime version", variant(lambda ix: ix["public"]["runtime"].update(version="3.12")), "pinned")
    verdict("a package that is not installed", variant(lambda ix: ix["public"]["runtime"].update(packages=["tensorflow"])), "not installed")
    verdict("a solution that raises", variant(lambda ix: ix["grading"]["solution_files"][0].update(content=starter + "big = customers[customers['nope'] > limit]\n")), "solution does not run")
    verdict("a solution using syntax not yet taught", variant(lambda ix: ix["grading"]["solution_files"][0].update(content=sol + "print(len(big))\n")), "not yet taught")
    verdict("a solution using blocked syntax", variant(lambda ix: ix["public"]["constraints"].update(blocked_syntax=["df[df['col'] > value]"], allowed_syntax=allowed[:-2])), "blocks for this practice")
    hard = variant(lambda ix: (ix["grading"]["solution_files"][0].update(content="import pandas as pd\nbig = pd.DataFrame({'customer_id': [1, 2, 4]})\n"),
                               ix["public"]["constraints"].update(allowed_syntax=allowed + ["pd.DataFrame(dict_of_lists)", "{key: value} dictionary literal", "[...] list literal"])))
    verdict("a hard-coded solution whose result never depends on the data", hard, "hard-coded answer would pass")
    verdict("a syntax descriptor with no detector is UNVERIFIED", variant(lambda ix: ix["public"]["constraints"].update(allowed_syntax=allowed + ["MYSTERY"])), "no detector", ) if False else None
    out2 = sandbox.run_exercise(reg, variant(lambda ix: ix["public"]["constraints"].update(allowed_syntax=allowed + ["MYSTERY"])))
    ok = out2.unverified and "MYSTERY" in out2.unverified
    fails += not ok
    print(("caught " if ok else "MISSED ") + "python: a syntax descriptor with no detector is UNVERIFIED")
    # reference grader: alternative phrasing passes; hard-coded and filter-ignoring answers fail (data, starter variable and hidden checks)
    stamped = copy.deepcopy(good)
    stamped["grading"]["hidden_checks"] = out.hidden_checks
    for name, code, want in [("the reference passes", sol, True), ("a differently written correct program passes", starter + "big = customers.loc[customers.spend > limit]\n", True),
                             ("a hard-coded frame is rejected", "import pandas as pd\nlimit = 8\nbig = pd.DataFrame({'customer_id': [1, 2, 4]})\n", False),
                             ("a program that ignores the limit variable is rejected", starter + "big = customers[customers['spend'] > 8]\n", False)]:
        passed, reasons = sandbox.grade_learner_py(reg, stamped, code)
        ok = passed == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + "python hidden: " + name + ("" if ok else f" (passed={passed}: {reasons})"))
    # isolation
    probe = lambda body: sandbox.node_run({"scripts": [{"id": "x", "entry": "m.py", "files": [{"path": "m.py", "content": body}], "mounts": [], "probes": []}]}, "sandbox/run_py.mjs")["results"]["x"]
    for name, body, expect in [("reading a host file", "print(open('/etc/hosts').read())", "No such file"),
                               ("importing the JS bridge", "import js", "not available"), ("importing pyodide_js", "import pyodide_js", "not available"),
                               ("running a shell command", "import os\nos.system('echo owned > /tmp/_py_sandbox_probe')", "restricted")]:
        r = probe(body)
        ok = not r["ok"] and expect in r.get("error", "")
        fails += not ok
        print(("caught " if ok else "MISSED ") + "python: sandbox blocks " + name + ("" if ok else f" ({r})"))
    ok = not Path("/tmp/_py_sandbox_probe").exists()
    fails += not ok
    print(("caught " if ok else "MISSED ") + "python: a sandboxed shell command wrote nothing to the host")
    pkg = json.loads((S.parent / "sandbox" / "package.json").read_text())["dependencies"]["pyodide"]
    ok = pkg == sandbox.RUNTIMES["python"]["version"] == sandbox.node_run({"scripts": []}, "sandbox/run_py.mjs")["version"]
    fails += not ok
    print(("caught " if ok else "MISSED ") + f"python: registry/runtimes.json, package.json and the running engine agree on the version ({pkg})")
    # syntax checker
    for name, code_, al, bl, want in [("assignments and arithmetic need only what is allowed", "a = 3\nb = a * 2\nprint(b)\n", ["print()", "+ - * / // % **", "whole-number literals as in the examples"], [], 0),
                                      ("a for loop is flagged when blocked", "for x in [1]:\n    pass\n", ["whole-number literals as in the examples"], ["for item in sequence:", "[...] list literal"], 3),
                                      ("a call to a user function is not a library call", "def f(a):\n    return a\nf(1)\n", ["def f(a, b):", "return", "calling name()", "positional arguments in a call", "whole-number literals as in the examples"], [], 0),
                                      ("an f-string is flagged when not taught", "x = 1\nprint(f'{x}')\n", ["print()", "single- or double-quoted strings", "whole-number literals as in the examples"], [], 1)]:
        v, _, _ = pysyntax.judge(code_, al, bl)
        ok = (len(v) == want) if want <= 1 else len(v) >= 1
        fails += not ok
        print(("caught " if ok else "MISSED ") + "pysyntax: " + name + ("" if ok else f" ({v})"))
    return fails


def unit_sheet_runner():
    """The spreadsheet (HyperFormula) runner and the formula syntax checker: correct work passes, every kind of wrong work is caught, and the sandbox holds."""
    import copy
    from checkers import sandbox, sheetsyntax
    reg = {"assets": [{"asset_id": "ds_sales", "asset_kind": "dataset", "columns": [
        {"name": "region", "type": "string"}, {"name": "units", "type": "integer"}, {"name": "price", "type": "number"}],
        "rows": [["N", 3, 2.5], ["S", 4, 10.0], ["N", 5, 1.0], ["E", 2, 4.0]]}]}
    starter = "// units and price are in sales (A2:C5); the discount rate is an input\nE1: 0.1\n"
    sol = starter + "D2: =B2*C2\nD3: =B3*C3\nD4: =B4*C4\nD5: =B5*C5\nF1: =SUM(D2:D5)*(1-E1)\nF2: =SUMIF(A2:A5,\"N\",B2:B5)\n"
    allowed = ["=B2*C2", "SUM(range)", "SUMIF(range, criteria, sum_range)", "relative references", "+ - * /", "parentheses", "numbers", "text in quotes"]
    good = {"type": "code_exercise", "interaction_id": "ix.s", "public": {"prompt": "p", "runtime": {"kind": "spreadsheet", "version": "3.4.0"},
            "workspace": {"entry": "book.sheet", "files": [{"path": "book.sheet", "role": "editable", "content": starter}],
                          "asset_mounts": [{"asset_id": "ds_sales", "mount_path": "sales.csv"}]},
            "constraints": {"allowed_syntax": allowed, "blocked_syntax": []}},
            "grading": {"solution_files": [{"path": "book.sheet", "content": sol}],
                        "tests": [{"test_id": "t1", "kind": "cell_equals", "message_on_fail": "no", "spec": {"cell": "F1", "expected": 60.5 * 0.9}},
                                  {"test_id": "t2", "kind": "range_equals", "message_on_fail": "no", "spec": {"range": "D2:D5", "expected": [[7.5], [40], [5], [8]]}},
                                  {"test_id": "t3", "kind": "formula_uses", "message_on_fail": "no", "spec": {"cell": "F2", "functions": ["SUMIF"]}}]}}
    good["grading"]["tests"].append({"test_id": "t4", "kind": "cell_equals", "message_on_fail": "no", "spec": {"cell": "F2", "expected": 8}})
    fails = 0

    def verdict(name, ix, want_text=None, want_ok=False):
        nonlocal fails
        out = sandbox.run_exercise(reg, ix)
        ok = (not out.problems) if want_ok else any(want_text in x for x in out.problems)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "sheet: " + name + ("" if ok else f" ({out.problems})"))
        return out

    def variant(f):
        ix = copy.deepcopy(good)
        f(ix)
        return ix
    sol_of = lambda ix, text: ix["grading"]["solution_files"][0].update(content=text)
    out = verdict("a correct exercise passes and gets provenance + hidden checks", good, want_ok=True)
    ok = out.provenance and len(out.hidden_checks) >= 2 and any(h["mutation"]["ops"][0]["op"] == "set_variable" for h in out.hidden_checks)
    fails += not ok
    print(("caught " if ok else "MISSED ") + f"sheet: {len(out.hidden_checks)} hidden checks derived (data and input-cell mutations)")
    verdict("a wrong expected value typed in the key", variant(lambda ix: ix["grading"]["tests"][1]["spec"]["expected"].__setitem__(0, [9])), "differs from spec.expected")
    verdict("a wrong formula in the solution (SUM over the wrong range)", variant(lambda ix: sol_of(ix, sol.replace("SUM(D2:D5)", "SUM(D2:D4)"))), "differs from spec.expected")
    verdict("a starter that already solves the task", variant(lambda ix: ix["public"]["workspace"]["files"][0].update(content=sol)), "starter sheet already passes")
    verdict("an unpinned runtime version", variant(lambda ix: ix["public"]["runtime"].update(version="2.0")), "pinned")
    verdict("a function nobody taught (and the engine does not know)", variant(lambda ix: sol_of(ix, sol + "G1: =NOSUCHFN(1)\n")), "not yet taught")
    verdict("a solution cell that does not use the required function", variant(lambda ix: sol_of(ix, sol.replace("=SUMIF(A2:A5,\"N\",B2:B5)", "=B2+B4"))), "does not hold a formula using")
    verdict("a bad line in the sheet file", variant(lambda ix: sol_of(ix, sol + "this is not a cell\n")), "solution does not load")
    verdict("a function not yet taught (blocked function)", variant(lambda ix: ix["public"]["constraints"].update(allowed_syntax=[a for a in allowed if "SUMIF" not in a], blocked_syntax=["SUMIF(range, criteria, sum_range)"])), "blocks for this practice")
    verdict("a forbidden_syntax test on a used function", variant(lambda ix: ix["grading"]["tests"].append({"test_id": "t5", "kind": "forbidden_syntax", "message_on_fail": "no", "spec": {"descriptors": ["SUMIF(range, criteria, sum_range)"]}})), "forbidden syntax")
    hard = variant(lambda ix: (sol_of(ix, starter + "D2: 7.5\nD3: 40\nD4: 5\nD5: 8\nF1: 54.45\nF2: 8\n"), ix["grading"]["tests"].pop(2)))
    verdict("a hard-coded solution whose cells never depend on the data", hard, "typed-in answer would pass")
    out2 = sandbox.run_exercise(reg, variant(lambda ix: ix["public"]["constraints"].update(allowed_syntax=allowed + ["MYSTERY HABIT"])))
    ok = out2.unverified and "MYSTERY HABIT" in out2.unverified
    fails += not ok
    print(("caught " if ok else "MISSED ") + "sheet: a syntax descriptor with no detector is UNVERIFIED")
    # reference grader
    stamped = copy.deepcopy(good)
    stamped["grading"]["hidden_checks"] = out.hidden_checks
    typed = starter + "D2: 7.5\nD3: 40\nD4: 5\nD5: 8\nF1: 54.45\nF2: =SUMIF(A2:A5,\"N\",B2:B5)\n"
    for name, text, want in [("the reference passes", sol, True),
                             ("a differently written correct sheet passes", starter + "D2: =C2*B2\nD3: =C3*B3\nD4: =C4*B4\nD5: =C5*B5\nF1: =(D2+D3+D4+D5)*(1-E1)\nF2: =SUMIF(A2:A5,\"N\",B2:B5)\n", True),
                             ("typed-in numbers are rejected by the hidden checks", typed, False),
                             ("a sheet that ignores the discount input cell is rejected", sol.replace("*(1-E1)", "*0.9"), False),
                             ("a wrong formula is rejected", sol.replace("SUM(D2:D5)", "SUM(D2:D4)"), False)]:
        passed, reasons = sandbox.grade_learner_sheet(reg, stamped, text)
        ok = passed == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + "sheet hidden: " + name + ("" if ok else f" (passed={passed}: {reasons})"))
    # isolation: hostile formulas are just errors, hostile sheet names/ids/keys are inert, and the process can neither write nor spawn
    run = lambda content, probes=(): sandbox.node_run({"scripts": [{"id": "__proto__", "content": content, "sheets": [], "probes": list(probes)}]}, "sandbox/run_sheet.mjs")["results"]["__proto__"]
    hostile = "A1: =process.exit()\nA2: =require('fs')\nA3: =constructor\nA4: =fetch(\"http://x\")\n"
    r = run(hostile, [{"id": f"p{i}", "kind": "cell", "ref": f"A{i}"} for i in range(1, 5)])
    ok = r["ok"] and all(r["probes"][f"p{i}"]["ok"] and str(r["probes"][f"p{i}"]["value"]).startswith("#") for i in range(1, 5))
    fails += not ok
    print(("caught " if ok else "MISSED ") + "sheet: hostile formulas (process, require, fetch, constructor) evaluate to errors" + ("" if ok else f" ({r})"))
    r = run("__proto__!A1: 1\n")
    ok = not r["ok"] and "unknown sheet" in r["error"]
    fails += not ok
    print(("caught " if ok else "MISSED ") + "sheet: a hostile sheet name is rejected" + ("" if ok else f" ({r})"))
    r = run("A1: 1\nB1: =A1+1\n", [{"id": "constructor", "kind": "cell", "ref": "B1"}])
    ok = r["ok"] and r["probes"]["constructor"]["value"] == 2
    fails += not ok
    print(("caught " if ok else "MISSED ") + "sheet: hostile script and probe ids are inert")
    r = run("A9999: 1\n")
    ok = not r["ok"] and "outside the allowed" in r["error"]
    fails += not ok
    print(("caught " if ok else "MISSED ") + "sheet: a cell far outside the allowed area is rejected (no memory blow-up)")
    import subprocess
    probe = f"import('node:fs').then(f => {{ try {{ f.writeFileSync('/tmp/_sheet_sandbox_probe', 'x'); console.log('WROTE'); }} catch (e) {{ console.log('DENIED ' + e.code); }} }})"
    p = subprocess.run(["node", "--permission", f"--allow-fs-read={sandbox.SANDBOX}", "-e", probe], capture_output=True, text=True, cwd=sandbox.SANDBOX)
    ok = "DENIED" in p.stdout and not Path("/tmp/_sheet_sandbox_probe").exists()
    fails += not ok
    print(("caught " if ok else "MISSED ") + "sheet: the permission flags the runner uses deny host writes" + ("" if ok else f" ({p.stdout} {p.stderr[-200:]})"))
    pkg = json.loads((S.parent / "sandbox" / "package.json").read_text())["dependencies"]["hyperformula"]
    ok = pkg == sandbox.RUNTIMES["spreadsheet"]["version"] == sandbox.node_run({"scripts": []}, "sandbox/run_sheet.mjs")["version"]
    fails += not ok
    print(("caught " if ok else "MISSED ") + f"sheet: registry/runtimes.json, package.json and the running engine agree on the version ({pkg})")
    # syntax checker
    for name, f, al, bl, want in [("arithmetic and SUM need only what is allowed", "=SUM(B2:B9)*2", ["SUM(range)", "relative references", "+ - * /", "numbers"], [], 0),
                                  ("an untaught function is flagged", "=VLOOKUP(A2,B2:C9,2,FALSE)", ["SUM(range)", "relative references", "numbers", "TRUE / FALSE"], [], 1),
                                  ("an absolute reference is flagged when only relative are taught", "=SUM($B$2:$B$9)", ["SUM(range)", "relative references"], [], 1),
                                  ("a function named in a bare list is allowed", "=IF(A1>1,1,0)", ["IF, AND, OR", "relative references", "numbers", "comparison operators"], [], 0),
                                  ("a function example with arguments allows that function", "=XLOOKUP(A2,B:B,C:C)", ["=XLOOKUP(key, lookup_col, return_col)", "whole column references", "relative references"], [], 0),
                                  ("strings are not read as syntax", "=A1&\"SUM(1)\"", ["relative references", "& (concatenation)", "text in quotes"], [], 0)]:
        v, _, _ = sheetsyntax.judge("A1: " + f, al, bl)
        ok = len(v) == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + "sheetsyntax: " + name + ("" if ok else f" ({v})"))
    for d, want_none in [("pivot tables", True), ("conditional formatting", True), ("some unheard-of concept", True), ("SUM(range)", False), ("cross-sheet references", False)]:
        ok = (sheetsyntax.descriptor_tags(d) is None) == want_none
        fails += not ok
        print(("caught " if ok else "MISSED ") + f"sheetsyntax: descriptor {d!r} {'is' if want_none else 'is not'} unmapped")
    ok = sheetsyntax.is_idea("pivot tables") and not sheetsyntax.is_idea("some unheard-of concept")
    fails += not ok
    print(("caught " if ok else "MISSED ") + "sheetsyntax: UI ideas are not_checkable, unknown descriptors are unmapped (-> UNVERIFIED)")
    return fails


def stamped_for(variant, out, mutate):
    """A mutated copy of the good exercise carrying the good run's provenance, so only the mutation is under test."""
    return variant(lambda ix: (ix["grading"].update(execution_provenance=out.provenance, hidden_checks=out.hidden_checks), mutate(ix)))


# ---- chart_renderer (matplotlib/seaborn on the Pyodide runner) ----
def unit_chart_runner():
    """Figure structure is graded, not pixels: correct charts pass, a wrong chart type / hard-coded figure / ignored data is caught, state does not leak, the sandbox holds."""
    import copy
    from checkers import sandbox
    reg = {"assets": [{"asset_id": "ds_customers", "asset_kind": "dataset", "columns": [
        {"name": "customer_id", "type": "integer"}, {"name": "city", "type": "string"}, {"name": "spend", "type": "number"}],
        "rows": [[1, "Lagos", 10.5], [2, "Abuja", 20.0], [3, "Lagos", 7.0], [4, "Kano", 31.0]]}]}
    starter = "import pandas as pd\nimport matplotlib.pyplot as plt\ncustomers = pd.read_csv('customers.csv')\nlimit = 8\n# bar chart of the spend of customers above the limit\n"
    sol = starter + "big = customers[customers['spend'] > limit]\nplt.bar(big['city'], big['spend'])\nplt.title('Spend')\n"
    allowed = ["import pandas as pd", "import matplotlib.pyplot as plt", "pd.read_csv(path)", "name = value assignment", "whole-number literals as in the examples",
               "single- or double-quoted strings", "df[df['col'] > value]", "df['col']", "plt.bar(x, y)", "plt.title(text)", "plt.scatter(x, y)"]
    t = lambda tid, kind, spec: {"test_id": tid, "kind": kind, "spec": spec, "message_on_fail": "no"}
    good = {"type": "code_exercise", "interaction_id": "ix.c", "public": {"prompt": "p", "runtime": {"kind": "chart_renderer", "version": "0.29.5", "packages": ["pandas", "matplotlib"]},
            "workspace": {"entry": "main.py", "files": [{"path": "main.py", "role": "editable", "content": starter}],
                          "asset_mounts": [{"asset_id": "ds_customers", "mount_path": "customers.csv"}]},
            "constraints": {"allowed_syntax": allowed, "blocked_syntax": []}},
            "grading": {"solution_files": [{"path": "main.py", "content": sol}],
                        "tests": [t("t1", "plotted_data_equals", {"chart": "bar", "field": "heights", "expected": [10.5, 20.0, 31.0]}),
                                  t("t2", "axes_property", {"property": "title", "expected": "Spend"}),
                                  t("t3", "figure_equals", {"expected": {"n_axes": 1, "chart_types": [["bar"]]}}),
                                  t("t4", "axes_property", {"property": "xticklabels", "expected": ["Lagos", "Abuja", "Kano"]})]}}
    fails = 0

    def variant(f):
        ix = copy.deepcopy(good)
        f(ix)
        return ix
    setsol = lambda code: (lambda ix: ix["grading"]["solution_files"][0].update(content=code))
    out = sandbox.run_exercise(reg, good)
    ok = not out.problems and out.provenance and len(out.hidden_checks) >= 2 and out.preview_png and out.preview_png.startswith("iVBOR")
    fails += not ok
    print(("caught " if ok else "MISSED ") + f"chart: a correct exercise passes with provenance, {len(out.hidden_checks)} hidden checks and a PNG preview" + ("" if ok else f" ({out.problems})"))
    for name, mut, want in [("a wrong chart type in the solution (line instead of bar)", setsol(starter + "big = customers[customers['spend'] > limit]\nplt.plot(big['city'], big['spend'])\nplt.title('Spend')\n"), "differs from spec.expected"),
                            ("a wrong typed title", lambda ix: ix["grading"]["tests"][1]["spec"].update(expected="Sales"), "differs from spec.expected"),
                            ("a starter that already draws the chart", lambda ix: ix["public"]["workspace"]["files"][0].update(content=sol), "starter code already passes"),
                            ("a hard-coded figure whose data never depends on the dataset or variables", lambda ix: (ix["grading"]["solution_files"][0].update(content="import matplotlib.pyplot as plt\nplt.bar(['Lagos', 'Abuja', 'Kano'], [10.5, 20.0, 31.0])\nplt.title('Spend')\n"),
                                                                                               ix["public"]["constraints"].update(allowed_syntax=allowed + ["[...] list literal"])), "hard-coded"),
                            ("a chart test kind on a python runtime", lambda ix: ix["public"]["runtime"].update(kind="python"), "not supported"),
                            ("a figure_equals key that is not a figure property", lambda ix: ix["grading"]["tests"][2]["spec"].update(expected={"colour": "red"}), "figure_equals"),
                            ("a solution that draws nothing", setsol(starter + "big = customers[customers['spend'] > limit]\n"), "no figure was drawn")]:
        o = sandbox.run_exercise(reg, variant(mut))
        ok = any(want in x for x in o.problems)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "chart: " + name + ("" if ok else f" ({o.problems})"))
    # reference grader: another way to draw the same chart passes; wrong chart, hard-coded and variable-ignoring figures fail
    stamped = copy.deepcopy(good)
    stamped["grading"]["hidden_checks"] = out.hidden_checks
    for name, code, want in [("the reference passes", sol, True),
                             ("a differently written correct chart passes", starter + "big = customers[customers.spend > limit]\nfig, ax = plt.subplots()\nax.bar(big.city, big.spend)\nax.set_title('Spend')\n", True),
                             ("a scatter instead of a bar is rejected", starter + "big = customers[customers['spend'] > limit]\nplt.scatter(big['city'], big['spend'])\nplt.title('Spend')\n", False),
                             ("a hard-coded figure is rejected", "import matplotlib.pyplot as plt\nlimit = 8\nplt.bar(['Lagos', 'Abuja', 'Kano'], [10.5, 20.0, 31.0])\nplt.title('Spend')\n", False),
                             ("a program that ignores the limit variable is rejected", starter + "big = customers[customers['spend'] > 8]\nplt.bar(big['city'], big['spend'])\nplt.title('Spend')\n", False)]:
        passed, reasons = sandbox.grade_learner_chart(reg, stamped, code)
        ok = passed == want
        fails += not ok
        print(("caught " if ok else "MISSED ") + "chart hidden: " + name + ("" if ok else f" (passed={passed}: {reasons})"))
    # isolation: matplotlib state does not leak between the scripts of one process; the sandbox still holds with matplotlib loaded
    sc = lambda i, body: {"id": i, "entry": "m.py", "files": [{"path": "m.py", "content": body}], "mounts": [], "probes": [], "chart": True}
    r = sandbox.node_run({"packages": ["numpy", "pandas", "matplotlib", "seaborn"], "scripts": [
        sc("f", "import seaborn as sns, pandas as pd\nsns.set_theme()\nsns.histplot(pd.Series([1, 2, 2, 3, 9]))\nimport matplotlib.pyplot as plt\nplt.figure()\nsns.heatmap([[1, 2], [3, 4]])\n"),
        sc("a", "import matplotlib.pyplot as plt\nplt.rcParams['axes.titlesize'] = 99\nplt.style.use('ggplot')\nplt.plot([1])\nplt.title('leak')\nopen('stray.txt', 'w').write('x')\n"),
        sc("b", "import matplotlib.pyplot as plt, os\nprint(plt.rcParams['axes.titlesize'], plt.rcParams['axes.facecolor'], len(plt.get_fignums()), os.path.exists('stray.txt'))\n"),
        sc("c", "import matplotlib\nmatplotlib.use('module://matplotlib_pyodide.html5_canvas_backend')\nimport matplotlib.pyplot as plt\nplt.plot([1])\n"),
        sc("d", "import js\n"), sc("e", "import os\nprint(open('/etc/hosts').read())\n")]}, "sandbox/run_py.mjs")["results"]
    for name, ok in [("seaborn is installed and its histplot/heatmap read back as hist/heatmap (colorbar axes dropped)",
                      r["f"]["ok"] and [[a["chart_types"] for a in f["axes"]] for f in r["f"]["fig"]["figures"]] == [[["hist"]], [["heatmap"]]]),
                     ("matplotlib rcParams, style, figures and files do not leak into the next script", r["b"]["ok"] and r["b"]["stdout"].strip() == "large white 0 False"),
                     ("switching to the browser backend cannot reach the JS bridge", not r["c"]["ok"] or "js" not in r["c"].get("error", "js")),
                     ("importing the JS bridge with matplotlib loaded", not r["d"]["ok"] and "not available" in r["d"]["error"]),
                     ("reading a host file with matplotlib loaded", not r["e"]["ok"] and "No such file" in r["e"]["error"])]:
        fails += not ok
        print(("caught " if ok else "MISSED ") + "chart: sandbox: " + name + ("" if ok else f" ({r})"))
    return fails


def unit_formula_entry():
    """formula_entry is verified by running its reference formula in the spreadsheet engine: right answer passes; wrong value, typed-in number, missing reference are caught."""
    from checkers import sandbox
    reg = {"assets": [{"asset_id": "ds_sales", "asset_kind": "dataset", "columns": [{"name": "region", "type": "string"}, {"name": "units", "type": "integer"}, {"name": "price", "type": "number"}],
                       "rows": [["N", 3, 2.5], ["S", 4, 10.0], ["N", 5, 1.0], ["E", 2, 4.0]]}]}
    mk = lambda **g: {"type": "formula_entry", "interaction_id": "ix.f", "public": {"prompt": "p", "asset_ref": {"asset_id": "ds_sales"}, "sheet_name": "sales", "target_cell": "F1"},
                      "grading": {"expected_value": 14, "must_use_functions": ["SUM"], "reference_formula": "=SUM(B2:B5)", **g}}
    cases = [("a correct formula_entry passes", mk(), None), ("a wrong expected_value", mk(expected_value=99), "differs from spec.expected"),
             ("a typed-in answer (no formula)", mk(reference_formula="=14", must_use_functions=[]), "typed-in"), ("a missing reference_formula", mk(reference_formula=""), "reference_formula is missing"),
             ("a required function not used", mk(reference_formula="=B2+B3+B4+B5"), "does not hold a formula using")]
    fails = 0
    grid = {"type": "spreadsheet_grid", "asset_ref": {"asset_id": "ds_sales"}, "sheet_name": "sales", "range": "A1:C5", "cells": [{"ref": "E1", "formula": "=SUM(B2:B5)"}, {"ref": "E2", "formula": "=NOSUCH(1)"}]}
    vals, probs = sandbox.sheet_cell_values(reg, grid)
    ok = vals.get("E1") == 14 and str(vals.get("E2", "")).startswith("#") and not probs
    fails += not ok
    print(("caught " if ok else "MISSED ") + f"spreadsheet_grid: formula cells are computed by the engine ({vals} {probs})")
    for name, ix, want in cases:
        probs = sandbox.formula_entry_outcome(reg, ix).problems
        ok = (not probs) if want is None else any(want in p for p in probs)
        fails += not ok
        print(("caught " if ok else "MISSED ") + "formula_entry: " + name + ("" if ok else f" ({probs})"))
    return fails


def main():
    src = Path(sys.argv[1]).resolve()
    tmp_root = src.parent / "_selftest_tmp"
    failures = unit_interactions(src) + unit_fail_closed(src) + unit_graph_blocks() + unit_stale_cleanup(src) + unit_sql_runner() + unit_python_runner() + unit_sheet_runner() + unit_chart_runner() + unit_formula_entry()
    for name, fn, expect in MUTATIONS:
        d = tmp_root / "case"
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(src, d, ignore=shutil.ignore_patterns("tile_lessons*", "grading", "reports", "final_stage_gate_ledger.json"))
        reg, sc, ix = jl(d / "scenario_asset_registry.json"), jl(d / "screens.json"), jl(d / "interactions.json")
        fn(reg, sc, ix)
        dump(d / "scenario_asset_registry.json", reg), dump(d / "screens.json", sc), dump(d / "interactions.json", ix)
        out = ""
        if "registry gate" in name:
            rc, out = run("validate_tile.py", d, "--registry")
        else:
            rc_a, out_a = run("assemble_tiles.py", d)
            rc_v, out_v = run("validate_tile.py", d)
            rc, out = (rc_a or rc_v), out_a + out_v
        ok = rc != 0 and expect in out
        failures += not ok
        print(("caught " if ok else "MISSED ") + name + ("" if ok else f"\n    expected {expect!r}; got rc={rc}:\n{out[-600:]}"))
    # tamper after assembly: edit a compiled lesson without reassembling
    d = tmp_root / "case"
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(src, d, ignore=shutil.ignore_patterns("reports", "final_stage_gate_ledger.json"))
    p = next((d / "tile_lessons").glob("*.json"))
    t = jl(p)
    t["steps"][0]["title"] += " (edited)"
    dump(p, t)
    rc, out = run("validate_tile.py", d)
    ok = rc != 0 and "content_hash mismatch" in out
    failures += not ok
    print(("caught " if ok else "MISSED ") + "compiled lesson edited after assembly")
    # baseline must still pass
    rc, out = run("validate_tile.py", src)
    ok = rc == 0
    failures += not ok
    print(("baseline PASS " if ok else "BASELINE BROKEN ") + out.splitlines()[0])
    shutil.rmtree(tmp_root, ignore_errors=True)
    print(f"\n{len(MUTATIONS) + 1} mutations, {failures} missed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
