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


def main():
    src = Path(sys.argv[1]).resolve()
    tmp_root = src.parent / "_selftest_tmp"
    failures = unit_interactions(src) + unit_fail_closed(src) + unit_graph_blocks() + unit_stale_cleanup(src)
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
