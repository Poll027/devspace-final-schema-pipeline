#!/usr/bin/env python3
"""Evaluator packet renderer: one plain-text packet with everything an independent evaluator needs to judge a tile, so it can judge in a
single tool-free call instead of exploring files with ~100 (measured: same 11/11 seeded-defect catch, ~1/3 fewer tokens, ~45% faster).

A packet holds: source facts (+source ids), the dataset digest, every screen's text with lineage, every question with its key and per-option
feedback, a script-computed taught-before-tested map, the deterministic gate result and the nearest blocked future concepts.
ROLE-AGNOSTIC: unknown block/interaction types are dumped as compact JSON, never dropped. A COMPLETENESS check proves every judgeable
string of the tile appears verbatim in the packet (anything without a dedicated renderer is appended under "OTHER CONTENT").

    python3 evaluator_packet.py <batch_dir> <out_dir> [--lessons <dir of assembled tile json>] [tile_id ...]   # CLI: write *.packet.md, report completeness
    from evaluator_packet import Env, render, completeness   # driver use
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("dataset", HERE / "checkers" / "dataset.py")
DS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(DS)

J = lambda p: json.loads(Path(p).read_text())
tok = lambda s: len(re.findall(r"\w+|[^\w\s]", s))
j = lambda o, n=900: json.dumps(o, separators=(",", ":"), ensure_ascii=False)[:n]


class Env:
    """Batch-level inputs a packet needs: glossary bundles, asset registry, tile order, the gate's per-tile report (optional)."""

    def __init__(self, batch, report_dir=None):
        batch = Path(batch)
        bundle = J(batch / "inputs" / "path_glossary_bundle.json")
        self.B = {b["context"]["concept_id"]: b for b in bundle["bundles"]}
        self.names, self.order = bundle.get("names", {}), bundle.get("tile_order", [])
        self.registry = J(batch / "scenario_asset_registry.json")
        rep = next((p for p in (Path(report_dir or batch) / "reports" / "validation.tiles.json", batch / "reports" / "validation.tiles.json") if p.exists()), None)
        self.vrep = {r["name"]: r for r in J(rep)} if rep else {}


class Packet:
    def __init__(self, L, env):
        self.L, self.env = L, env
        self.al = {c: chr(65 + i) for i, c in enumerate(L["concept_ids"])}
        self.out = []

    def f(self, qualified):  # "concept#f1" -> "A.f1"
        c, _, x = qualified.partition("#")
        return f"{self.al.get(c, c)}.{x}"

    def lin(self, lineage):
        if not lineage:
            return ""
        parts = [self.f(x) for x in lineage.get("fact_ids", [])] + [self.f(x).replace(".", ":") for x in lineage.get("teaching_block_ids", [])]
        return f" ⟦{' '.join(parts)}⟧" if parts else ""

    def w(self, s=""):
        self.out.append(s)


def render_block(P, b):
    t = b["type"]
    if t in ("prose", "callout"):
        tag = b.get("role") or b.get("tone")
        P.w(f"({tag}) {b['text']}{P.lin(b.get('lineage'))}")
    elif t == "heading":
        P.w(f"### {b['text']}")
    elif t == "data_table":
        a = b.get("asset_ref")
        extra = []
        if a and a.get("variant_id"):
            extra.append(f"variant={a['variant_id']}")
        if b.get("highlight"):
            extra.append("highlights=" + j([(h["target"].get("kind"), h["target"].get("column"), h.get("label")) for h in b["highlight"]]))
        if b.get("tag_columns"):
            extra.append("tags=" + ", ".join(f"{x['column']}:{x['tag']}" for x in b["tag_columns"]))
        src = f"{a['asset_id']} cols={a.get('columns') or 'all'}" if a else "computed result"
        P.w(f"[TABLE {src} {' '.join(extra)}] caption: {b.get('caption', '')}")
        if b.get("result_of"):
            P.w(f"  produced by {b['result_of'].get('runtime')}: {b['result_of'].get('sql') or j(b['result_of'], 300)}")
        if b.get("result"):
            P.w(f"  result columns={b['result']['columns']} rows({len(b['result']['rows'])})=" + j(b["result"]["rows"][:10], 500))
    elif t == "media_group":
        P.w(f"[VIDEO {b.get('group_title', '')}] bridge-before: {b.get('bridge', {}).get('before', '')} | bridge-after: {b.get('bridge', {}).get('after', '')}")
        for s in b.get("segments", []):
            P.w(f"  - {s['video_id']} {s['start_seconds']}-{s['end_seconds']}s facts={s.get('fact_ids')} label: {s.get('label', '')} | summary: {s['summary']}")
    elif t in ("before_after", "side_by_side"):
        P.w(f"[{t.upper()}] {b.get('change_summary') or b.get('takeaway', '')}" + (f" left_label: {b['left_label']} | right_label: {b['right_label']}" if "left_label" in b else ""))
        for k in ("before", "after", "left", "right"):
            if k in b:
                P.w(f"  {k}:")
                render_block(P, b[k])
    elif t == "comparison":
        P.w(f"[COMPARISON] cols={[c['label'] for c in b['columns']]}")
        for r in b["rows"]:
            P.w(f"  - {r['criterion']}: {j(r['cells'], 400)}")
    elif t in ("process_flow", "diagram"):
        P.w(f"[{t.upper()}{(': ' + b['title']) if b.get('title') else ''}] nodes={[(n['label'] + (' — ' + n['detail'] if n.get('detail') else '') + (' {' + '; '.join(n['fields']) + '}' if n.get('fields') else '')) for n in b['nodes']]} edges={[(e['from'], e['to'], e.get('label')) for e in b.get('edges', [])]} alt: {b['alt_text']}")
    elif t == "code_walkthrough":
        P.w(f"[CODE {b['language']}]\n{b['code']}\n  annotations: {[a['text'] for a in b.get('annotations', [])]}" + (f"\n  output: {b['output'].get('text', '')}" if b.get("output") else ""))
    elif t == "chart":
        enc = b["encoding"]
        P.w(f"[CHART {b['chart_kind']}: {b['title']}] data={b['asset_ref']['asset_id']} x={enc['x']['field']} y={enc.get('y', {}).get('field')} color={enc.get('color', {}).get('field')} annotations={[a['text'] for a in b.get('annotations', [])]} alt: {b['alt_text']}")
    elif t == "up_next":
        P.w(f"[UP NEXT] {b['title']}: {b.get('text', '')}")
    elif t == "concept_chips":
        P.w("[CHIPS] " + "; ".join(f"{i['label']}: {i['short_text']}" for i in b["items"]))
    else:
        P.w(f"[{t.upper()} — unrendered type, raw] {j(b, 1500)}")


def resolved(P, a, where, column=None):
    try:
        cols, rows = DS.resolve_dataset(P.env.registry, a["asset_id"], a.get("variant_id"))
    except Exception:
        return None
    i = DS.find_row(rows, where["where"], where.get("occurrence", 0))
    return None if i is None else (rows[i].get(column) if column else rows[i])


def render_interaction(P, i, taught_at):
    t, pub, gr, fb = i["type"], i["public"], i["grading"], i["feedback"]
    P.w(f"QUESTION [{t}, {i.get('difficulty')}, grading={i.get('grading_mode')}] " + (pub.get("prompt") or pub.get("instructions") or pub.get("instruction") or ""))
    if pub.get("intro"):
        P.w(f"  intro shown to learner: {pub['intro']}")
    if t == "choice":
        for o in pub["options"]:
            ok = o["option_id"] in gr["correct_option_ids"]
            P.w(f"  {'✔' if ok else '✘'} {o['option_id']}: {o['text']}")
            m = gr.get("option_feedback", {}).get(o["option_id"], {}).get("message")
            if m:
                P.w(f"      why: {m}")
    elif t == "table_select":
        a = pub["asset_ref"]
        for tk, an in zip(pub["tasks"], gr["answers"]):
            val = resolved(P, a, an["row"], an.get("column")) if "row" in an else None
            P.w(f"  task {tk['task_id']} ({tk['target_kind']}): {tk['prompt']}  KEY: row={an.get('row', {}).get('where')} column={an.get('column')} expect={an.get('expect_value')} dataset-says={val}")
            fbm = gr.get("task_feedback", {}).get(tk["task_id"])
            if fbm:
                P.w(f"      feedback: {fbm}")
    elif t == "find_issues":
        P.w("  categories: " + ", ".join(c["label"] for c in pub["categories"]))
        for s in gr["issues"]:
            P.w(f"  issue {s['issue_id']} [{s['category_id']}] at {[(l['where'], l['column']) for l in s['locations']]}: {s['explanation']}")
        for d in gr.get("decoys", []):
            P.w(f"  decoy at {d['location']['where']}.{d['location']['column']}: {d['message']}")
    elif t == "ordering":
        txt = {x["item_id"]: x["text"] for x in pub["items"]}
        P.w("  items(shown): " + " | ".join(x["text"] for x in pub["items"]))
        P.w("  KEY order: " + " > ".join(txt[x] for x in gr["correct_order"]) + (f"  alt orders: {len(gr.get('accepted_alternatives', []))}" if gr.get("accepted_alternatives") else ""))
        if pub.get("follow_up"):
            P.w(f"  follow-up: {pub['follow_up']['prompt']} options={[o['text'] for o in pub['follow_up']['options']]} KEY={gr.get('follow_up_correct_option_ids')}")
    elif t == "classify":
        bk = {b["bucket_id"]: b["label"] for b in pub["buckets"]}
        for it in pub["items"]:
            src = it.get("source")
            role = None
            if src:
                ds = DS.asset_by_id(P.env.registry, src["asset_id"])
                role = next((c["semantic_role"] for c in ds["columns"] if c["name"] == src["column"]), None) if ds else None
            P.w(f"  '{it['text']}' -> {bk[gr['assignments'][it['item_id']]]}" + (f"  (column {src['column']}, role={role})" if src else ""))
            m = gr.get("item_feedback", {}).get(it["item_id"], {}).get("message")
            if m:
                P.w(f"      feedback: {m}")
    elif t == "field_selection":
        P.w(f"  scenario: {pub.get('scenario', '')}")
        for r in gr["rules"]:
            P.w(f"  {r['field_id']}: {r['role']} — {r['rationale']}")
    elif t == "match_pairs":
        L = {x["id"]: x["text"] for x in pub["left"]}
        R = {x["id"]: x["text"] for x in pub["right"]}
        for p in gr["pairs"]:
            P.w(f"  {L[p['left']]} ↔ {R[p['right']]}")
    elif t == "code_exercise":
        P.w(f"  runtime={pub['runtime']} constraints.allowed={pub.get('constraints', {}).get('allowed_syntax')} blocked={len(pub.get('constraints', {}).get('blocked_syntax', []))} items")
        for f in pub["workspace"]["files"]:
            P.w(f"  file {f['path']} [{f['role']}]:\n{f['content']}")
        for f in gr.get("solution_files", []):
            P.w(f"  SOLUTION {f['path']}:\n{f['content']}")
        for tst in gr["tests"]:
            P.w(f"  test {tst['test_id']} ({tst['kind']}, visible={tst.get('visible')}): {j(tst['spec'], 500)} | on-fail: {tst['message_on_fail']}")
        if gr.get("execution_provenance"):
            P.w(f"  provenance: {j(gr['execution_provenance'], 300)}")
    else:
        P.w(f"  [unrendered interaction type {t}] public={j(pub, 900)} grading={j(gr, 900)}")
    P.w(f"  feedback✔: {fb['correct']['message']}  feedback✘: {fb['incorrect']['message']}" + (f"  hints: {fb['hints']}" if fb.get("hints") else "") + (f"  remediation→{fb['remediation_step_id'].split('.')[-1]}" if fb.get("remediation_step_id") else ""))
    P.w("  MEASURES: " + "; ".join(f"{P.al.get(m['concept_id'], m['concept_id'])}:{m['capability']}({','.join(m['fact_ids'])})" for m in i["measures"]) + f"   anchors={[a.split('#')[1] for a in i.get('anchors', [])]}")
    P.w("  taught-before-tested: " + "; ".join(f"{P.al[m['concept_id']]}.{fid}←{taught_at.get(m['concept_id'] + '#' + fid, 'NEVER')}" for m in i["measures"] for fid in m["fact_ids"]))


def render(L, env):
    P = Packet(L, env)
    B, names, vrep, registry = env.B, env.names, env.vrep, env.registry
    P.w(f"# EVALUATOR PACKET — {L['title']} ({L['tile_id']})")
    P.w(f"Tile summary: {L.get('summary', '')}")
    P.w("Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.")
    for c, a in P.al.items():
        P.w(f"{a} = {c} — {names.get(c, '')}")
    g = vrep.get(L["tile_id"])
    P.w(f"\n## DETERMINISTIC GATE (already passed — do not re-derive): {g['status'] if g else 'n/a'}  errors={len(g['errors']) if g else 0} warnings={len(g['warnings']) if g else 0}")
    for w in (g or {}).get("warnings", []):
        P.w(f"  warn: {w}")
    for c in L["concept_ids"]:
        b = B[c]
        P.w(f"\n## SOURCE FACTS — {P.al[c]} ({c})   objective: {b['coverage']['learning_objective']}")
        for f in b["coverage"]["required_facts"]:
            P.w(f"{P.al[c]}.{f['id']}: {f['statement']}   [sources: {', '.join(f['source_refs'])}]")
        for m in b["coverage"].get("misconceptions", []):
            P.w(f"{P.al[c]}.{m['id']} (misconception): {m['statement']}   [sources: {', '.join(m['source_refs'])}]")
        for n in b.get("teaching_notes", []):
            P.w(f"note: {n}")
        pa = b.get("practice_anchor")
        if pa:
            P.w(f"PRACTICE ANCHOR ({pa['type']}): {pa['objective']}  SUCCESS: {pa['success']}")
        for a in b["assessment_anchors"]:
            P.w(f"ASSESSMENT ANCHOR: {a['capability']} facts={a['fact_ids']}")
    P.w("\n## DATA ASSETS USED")
    for aid in L["requires"]["asset_ids"]:
        a = DS.asset_by_id(registry, aid)
        if not a or a["asset_kind"] != "dataset":
            P.w(f"{aid}: {a['asset_kind'] if a else 'MISSING'}")
            continue
        P.w(f"{aid}: {a['title']} — columns: " + ", ".join(f"{c['name']}({c['semantic_role']}{',digits-as-label' if c.get('numeric_looking_label') else ''})" for c in a["columns"]))
        for r in a["rows"][:8]:
            P.w("   " + j(r, 300))
        for v in a.get("variants", []):
            P.w(f"   variant {v['variant_id']}: {len(v['ops'])} ops; planted: " + "; ".join(f"{p['issue_id']}({p['kind']})" for p in v.get("planted_issues", [])))
    blocked = []
    for c in L["concept_ids"]:
        blocked += B[c]["context"].get("blocked_future_concepts", [])[:25]
    P.w("\n## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): " + "; ".join(sorted({names.get(x, x) for x in blocked}))[:1200])
    taught_at, step_names = {}, {}
    for s in L["steps"] + L["remediation_steps"]:
        step_names[s["step_id"]] = s["step_id"].split(".")[-1]
        for b in s.get("blocks", []):
            for f in b.get("lineage", {}).get("fact_ids", []):
                taught_at.setdefault(f, step_names[s["step_id"]])
    P.w("\n## LESSON, in learner order")
    for s in L["steps"]:
        P.w(f"\n### {step_names[s['step_id']]} · {s['type']} · {s['title']}" + (f"  [reward {s['reward']['gems']}]" if s.get("reward") else ""))
        if s.get("eyebrow") or s.get("lede"):
            P.w(f"{s.get('eyebrow', '')} — {s.get('lede', '')}")
        for b in s.get("blocks", []):
            render_block(P, b)
        if s.get("interaction"):
            render_interaction(P, s["interaction"], taught_at)
    if L["remediation_steps"]:
        P.w("\n## REMEDIATION STEPS (shown only after a wrong answer)")
        for s in L["remediation_steps"]:
            P.w(f"### {step_names[s['step_id']]} · {s['title']}" + (f" — {s['lede']}" if s.get("lede") else ""))
            for b in s.get("blocks", []):
                render_block(P, b)
    text = "\n".join(P.out)
    n, miss = completeness(L, text)
    if miss:
        P.w("\n## OTHER CONTENT (fields without a dedicated renderer)")
        for path, st in strings(L):
            if len(st) >= 20 and not (SKIP & set(path)) and not re.fullmatch(r"[\w.#:\-]+", st) and st not in text:
                P.w(f"· {'.'.join(path[-2:])}: {st}")
    return "\n".join(P.out)


def strings(o, path=()):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + (k,))
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, path)
    elif isinstance(o, str):
        yield path, o


SKIP = {"lineage", "execution_provenance", "source", "content_hash", "youtube_url", "review_url", "transcript_ref", "segment_ids", "anchors", "measures", "toc_location", "requires"}


def completeness(L, text):
    miss, n = [], 0
    for path, s in strings(L):
        if len(s) < 20 or SKIP & set(path) or re.fullmatch(r"[\w.#:\-]+", s):
            continue
        n += 1
        if s not in text:
            miss.append((".".join(path[-3:]), s[:90]))
    return n, miss


def screens_lesson(tile, plan):
    """A stage-03 tile (screens only, no interactions yet) in the shape render() expects, concept ids from its plan."""
    ids = set()

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("asset_id"), str):
                ids.add(o["asset_id"])
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(tile)
    return {**tile, "concept_ids": plan["concept_ids"], "requires": {"asset_ids": sorted(ids)}, "remediation_steps": tile.get("remediation_steps", [])}


def main():
    a = sys.argv[1:]
    lessons = None
    if "--lessons" in a:
        i = a.index("--lessons")
        lessons = Path(a[i + 1])
        del a[i:i + 2]
    batch, out, only = Path(a[0]), Path(a[1]), a[2:]
    lessons = lessons or batch / "tile_lessons"
    env = Env(batch, lessons.parent)
    out.mkdir(parents=True, exist_ok=True)
    print(f"{'tile':52} {'JSON tok':>9} {'packet tok':>10} {'ratio':>6}  completeness")
    for p in sorted(lessons.glob("*.json")):
        L = J(p)
        if only and L["tile_id"] not in only:
            continue
        text = render(L, env)
        (out / f"{L['tile_id']}.packet.md").write_text(text + "\n")
        n, miss = completeness(L, text)
        tj = tok(json.dumps(L, separators=(",", ":"), ensure_ascii=False))
        print(f"{L['tile_id'][:52]:52} {tj:9,} {tok(text):10,} {tj / tok(text):5.1f}x  {n - len(miss)}/{n} judgeable strings present" + (f"  MISSING: {miss[:3]}" if miss else ""))


if __name__ == "__main__":
    main()
