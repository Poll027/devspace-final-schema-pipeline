"""Data-pack checkers: everything that resolves a registered dataset and executes the answer key against it.
Covers blocks data_table / spreadsheet_grid / chart, interactions table_select / find_issues / classify, and the `dataset` asset kind.
A role whose glossary needs none of these never loads this module's checks. (formula_entry is declared but UNVERIFIED until the sandbox runner exists.)"""
import re

from .dataset import asset_by_id, find_row, resolve_dataset, rule_holds


def resolve_ref(C, ref, rep, where):
    try:
        return resolve_dataset(C.registry, ref["asset_id"], ref.get("variant_id"))
    except (KeyError, ValueError) as ex:
        rep.e(f"{where}: {ex}")
        return None


def cell_value(rows, row_ref, column, rep, where):
    i = find_row(rows, row_ref["where"], row_ref.get("occurrence", 0))
    if i is None:
        rep.e(f"{where}: row {row_ref['where']}#{row_ref.get('occurrence', 0)} matches nothing")
        return None, None
    if column is not None and column not in rows[i]:
        rep.e(f"{where}: no column {column!r}")
        return i, None
    return i, (rows[i][column] if column else None)


# ---------------------------------------------------------------- blocks
def data_table_result(C, step, b, rep):
    """A query-result table: re-run the query and require the stored `result` to equal a fresh run (computed, never typed)."""
    from . import sandbox
    here = f"{step['step_id']}/data_table"
    fresh, problems = sandbox.run_query(C.registry, b["result_of"])
    for p in problems:
        rep.e(f"{here}: result_of {p}")
    if problems:
        return
    if "result" not in b:
        rep.e(f"{here}: result missing (run assemble_tiles.py: the rows are computed from result_of, never typed)")
    elif b["result"] != fresh:
        rep.e(f"{here}: stored result does not match a fresh run of result_of.sql")
    names = fresh["columns"]
    rows = [dict(zip(names, r)) for r in fresh["rows"]]
    sel = (b.get("asset_ref") or {}).get("columns") or []
    for h in b.get("highlight", []):
        tg = h["target"]
        if tg["kind"] in ("row", "cell") and ("row" not in tg or cell_value(rows, tg["row"], None, rep, here)[0] is None):
            rep.e(f"{here}: {tg['kind']} highlight needs a `row` that matches a result row")
        if tg["kind"] in ("column", "cell") and tg.get("column") not in names:
            rep.e(f"{here}: highlight column {tg.get('column')!r} is not a result column")
    for tc in b.get("tag_columns", []):
        if tc["column"] not in names:
            rep.e(f"{here}: tag_columns column {tc['column']!r} is not a result column")
    if sel:
        rep.w(f"{here}: asset_ref.columns is ignored when result_of is set")


def data_table(C, step, b, rep):
    if "result_of" in b:
        return data_table_result(C, step, b, rep)
    here = f"{step['step_id']}/data_table"
    res = resolve_ref(C, b["asset_ref"], rep, here)
    if not res:
        return
    cols, rows = res
    names = [c["name"] for c in cols]
    sel = b["asset_ref"].get("columns") or []
    for c in sel:
        if c not in names:
            rep.e(f"{here}: asset_ref column {c!r} not in dataset")
    shown = sel or names
    for h in b.get("highlight", []):
        tg = h["target"]
        if tg["kind"] in ("row", "cell"):
            if "row" not in tg:
                rep.e(f"{here}: {tg['kind']} highlight needs a `row`")
            else:
                cell_value(rows, tg["row"], None, rep, here)
        if tg["kind"] in ("column", "cell") and tg.get("column") not in shown:
            rep.e(f"{here}: highlight column {tg.get('column')!r} not displayed")
    for tc in b.get("tag_columns", []):
        if tc["column"] not in shown:
            rep.e(f"{here}: tag_columns column {tc['column']!r} not displayed")
    ins = b.get("inspect", {})
    if ins.get("enabled"):
        if ins.get("id_column") and ins["id_column"] not in names:
            rep.e(f"{here}: inspect.id_column {ins['id_column']!r} not in dataset")
        for ph in re.findall(r"\{(\w+)\}", ins.get("caption_template", "")):
            if ph not in names and ph not in ("column", "value", "row_number"):
                rep.e(f"{here}: caption_template placeholder {{{ph}}} is neither a column nor column/value/row_number")


def spreadsheet_grid(C, step, b, rep):
    here = f"{step['step_id']}/spreadsheet_grid"
    if resolve_ref(C, b["asset_ref"], rep, here):
        rep.w(f"{here}: formulas/computed_values are not executed yet (spreadsheet engine runner pending) — UNVERIFIED")


def chart(C, step, b, rep):
    here = f"{step['step_id']}/chart"
    res = resolve_ref(C, b["asset_ref"], rep, here)
    if not res:
        return
    names = [c["name"] for c in res[0]]
    for ax in ("x", "y", "color"):
        f = b["encoding"].get(ax, {}).get("field")
        if f and f not in names:
            rep.e(f"{here}: encoding.{ax}.field {f!r} not in dataset")


# ---------------------------------------------------------------- interactions
def table_select(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    res = resolve_ref(C, pub["asset_ref"], rep, here)
    if not res:
        return
    names = [c["name"] for c in res[0]]
    rows = res[1]
    kinds = {t["task_id"]: t["target_kind"] for t in pub["tasks"]}
    ans = {a["task_id"]: a for a in gr["answers"]}
    if set(ans) != set(kinds):
        rep.e(f"{here}: answers must cover exactly the tasks")
    for tid, a in ans.items():
        k = kinds.get(tid)
        if k in ("row", "cell") and "row" not in a:
            rep.e(f"{here}/{tid}: {k} task needs `row`")
        if k in ("column", "cell") and "column" not in a:
            rep.e(f"{here}/{tid}: {k} task needs `column`")
        if "column" in a and a["column"] not in names:
            rep.e(f"{here}/{tid}: no column {a['column']!r}")
        if "row" in a:
            i, val = cell_value(rows, a["row"], a.get("column"), rep, f"{here}/{tid}")
            if i is not None and "expect_value" in a and val != a["expect_value"]:
                rep.e(f"{here}/{tid}: expect_value {a['expect_value']!r} but the dataset says {val!r}  <- the answer key was typed wrong")
        if k == "cell" and "expect_value" not in a:
            rep.w(f"{here}/{tid}: cell answer without expect_value (add one so a script can verify the key)")


def find_issues(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    res = resolve_ref(C, pub["asset_ref"], rep, here)
    if not res:
        return
    rows = res[1]
    ds = asset_by_id(C.registry, pub["asset_ref"]["asset_id"])
    planted = {}
    for v in ds.get("variants", []):
        if v["variant_id"] == pub["asset_ref"].get("variant_id"):
            planted = {p["issue_id"]: p for p in v.get("planted_issues", [])}
    cats = {c["category_id"] for c in pub["categories"]}

    def key(loc):
        return (find_row(rows, loc["where"], loc.get("occurrence", 0)), loc["column"])
    for iss in gr["issues"]:
        reg = planted.get(iss["issue_id"])
        if not reg:
            rep.e(f"{here}: issue {iss['issue_id']} is not a planted issue of the variant (answer keys must come from the registry)")
            continue
        if iss["category_id"] not in cats:
            rep.e(f"{here}: issue {iss['issue_id']} category {iss['category_id']} not in categories")
        if {key(l) for l in iss["locations"]} != {key(l) for l in reg["locations"]}:
            rep.e(f"{here}: issue {iss['issue_id']} locations differ from the registry's")
    if pub["goal_count"] != len(gr["issues"]):
        rep.e(f"{here}: goal_count {pub['goal_count']} != {len(gr['issues'])} issues in the key")
    locs = {key(l) for p in planted.values() for l in p["locations"]}
    for d in gr.get("decoys", []):
        k = key(d["location"])
        if k[0] is None:
            rep.e(f"{here}: decoy location resolves to no row")
        elif k in locs:
            rep.e(f"{here}: a decoy sits on a real planted issue")


def classify(C, step, ix, rep):
    here, pub, gr = f"{step['step_id']}/{ix['interaction_id']}", ix["public"], ix["grading"]
    buckets = {b["bucket_id"] for b in pub["buckets"]}
    items = {i["item_id"]: i for i in pub["items"]}
    if set(gr["assignments"]) != set(items):
        rep.e(f"{here}: assignments must cover exactly the items")
    for it, b in gr["assignments"].items():
        if b not in buckets:
            rep.e(f"{here}: item {it} assigned to unknown bucket {b}")
    rm = gr.get("role_map", {})
    sourced = [i for i in items.values() if i.get("source")]
    if sourced and not rm:
        rep.w(f"{here}: no role_map, so classify answers cannot be executed against column roles")
    for it, item in items.items():
        src = item.get("source")
        if not src:
            continue
        ds = asset_by_id(C.registry, src["asset_id"])
        if not ds:
            rep.e(f"{here}: item {it} source asset {src['asset_id']} missing")
            continue
        col = next((c for c in ds["columns"] if c["name"] == src["column"]), None)
        if not col:
            rep.e(f"{here}: item {it} source column {src['column']!r} not in dataset")
            continue
        _, rows = resolve_dataset(C.registry, src["asset_id"])
        if find_row(rows, src["row"]["where"], src["row"].get("occurrence", 0)) is None:
            rep.e(f"{here}: item {it} source row matches nothing")
        want = rm.get(gr["assignments"].get(it))
        if want and want != col["semantic_role"]:
            rep.e(f"{here}: item {it} is a {col['semantic_role']} column ({src['column']}) but the key puts it in a {want} bucket  <- answer key contradicts the dataset")


def formula_entry(C, step, ix, rep):
    rep.w(f"{step['step_id']}/{ix['interaction_id']}: formula_entry is not executed yet (spreadsheet engine runner pending) — UNVERIFIED")


# ---------------------------------------------------------------- dataset asset (registry gate)
def check_dataset(C, a, rep):
    reg = C.registry
    for c in a["columns"]:
        numeric = c["type"] in ("integer", "number")
        if c["semantic_role"] == "numerical" and not numeric:
            rep.e(f"{a['asset_id']}.{c['name']}: semantic_role numerical but type {c['type']}")
        if c.get("numeric_looking_label") and not (numeric and c["semantic_role"] in ("categorical", "identifier")):
            rep.e(f"{a['asset_id']}.{c['name']}: numeric_looking_label needs a numeric type and a categorical/identifier role")
    try:
        resolve_dataset(reg, a["asset_id"])
    except (KeyError, ValueError) as ex:
        rep.e(f"{a['asset_id']}: {ex}")
        return
    for v in a.get("variants", []):
        try:
            _, rows = resolve_dataset(reg, a["asset_id"], v["variant_id"])
        except (KeyError, ValueError) as ex:
            rep.e(f"{a['asset_id']}/{v['variant_id']}: {ex}")
            continue
        for issue in v.get("planted_issues", []):
            for loc in issue["locations"]:
                i = find_row(rows, loc["where"], loc.get("occurrence", 0))
                if i is None:
                    rep.e(f"{v['variant_id']}/{issue['issue_id']}: location {loc['where']}#{loc.get('occurrence', 0)} matches no row")
                    continue
                if loc["column"] not in rows[i]:
                    rep.e(f"{v['variant_id']}/{issue['issue_id']}: no column {loc['column']}")
                    continue
                if "rule" in issue:
                    ok, why = rule_holds(issue["rule"], rows, i, loc["column"])
                elif issue["kind"] == "missing_value":
                    ok, why = rows[i][loc["column"]] is None, f"value={rows[i][loc['column']]!r}"
                elif issue["kind"] == "duplicate_row":
                    ok, why = any(j != i and rows[j] == rows[i] for j in range(len(rows))), "no identical sibling row"
                else:
                    ok, why = False, f"kind {issue['kind']} needs a `rule` so it can be executed"
                if not ok:
                    rep.e(f"{v['variant_id']}/{issue['issue_id']}: planted issue does not hold at {loc['where']}.{loc['column']} ({why})")


BLOCK = {"data_table": data_table, "spreadsheet_grid": spreadsheet_grid, "chart": chart}
INTERACTION = {"table_select": table_select, "find_issues": find_issues, "classify": classify, "formula_entry": formula_entry}
ASSET = {"dataset": check_dataset}
