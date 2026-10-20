"""Deterministic validation — the gate that makes content trustworthy without an LLM. ROLE-AGNOSTIC: everything specific to a kind of content
(datasets, code, diagrams...) lives in pack checkers (scripts/checkers/); this file knows only the universal rules.

  python3 validate_tile.py batches/<batch_id> --registry        stage 01 gate: scenario_asset_registry.json
  python3 validate_tile.py batches/<batch_id>                   stage 07 gate: every tile_lessons/<tile>.json
  python3 validate_tile.py batches/<batch_id> --tile <tile_id> [--strict] [--json]

Universal checks (E = blocking error, W = advisory warning):
  structure  ids unique, step ids prefixed by tile id, remediation targets resolve, `requires` + content_hash recomputed, bundle hashes match
  lineage    every fact / teaching-block / anchor id exists in the glossary bundle; media segments are verbatim copies
  coverage   every required fact + misconception is TAUGHT by text (not video-only); every assessment anchor is MEASURED; every practice anchor has a
             hands_on step; every visual anchor is realised
  order      an interaction may only test facts taught in an earlier step (the playbook's traceability rule)
  plan       authored steps follow tile_plans.json (ids, types, lineage, planned interaction + visual block types)
  lint       no "as the video shows" in text, per-step word budget, blocked-future-concept names in text (advisory)
Pack checks (dispatched by block / interaction / asset type): answer keys executed against the registered assets. FAIL-CLOSED: a type with no
checker is reported UNVERIFIED (warning; error under --strict).
"""
import argparse
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import checkers
from finlib import CORE, Ctx, load, save, sha, words
from schema_check import errors as schema_errors

_MAP = load(CORE / "registry" / "anchor_mapping.json")
VISUAL_MAP, ALTERNATES = _MAP["visual_anchor_to_block"], _MAP.get("visual_alternates", {})
VIDEO_PHRASES = re.compile(r"\b(as (the )?(video|clip) (shows|explains|demonstrates)|in the (video|clip)|watch (the|this) (video|clip)|as shown in the (video|clip))\b", re.I)
TEXT_BLOCKS = ("prose", "callout")


class Report:
    def __init__(self, name):
        self.name, self.E, self.W = name, [], []

    def e(self, m):
        self.E.append(m)

    def w(self, m):
        self.W.append(m)


def iter_blocks(blocks):
    for b in blocks or []:
        yield b
        if b["type"] == "before_after":
            yield b["before"]
            yield b["after"]
        if b["type"] == "side_by_side":
            yield b["left"]
            yield b["right"]


def check_block(C, step, b, rep):
    t = b["type"]
    if t in checkers.NO_CHECK_NEEDED:
        return
    if t in checkers.BLOCK:
        checkers.BLOCK[t](C, step, b, rep)
    else:
        rep.w(f"{step['step_id']}/{t}: UNVERIFIED — no checker registered for block type {t!r}")


def check_interaction(C, step, ix, rep):
    t = ix["type"]
    if t in checkers.INTERACTION:
        checkers.INTERACTION[t](C, step, ix, rep)
    else:
        rep.w(f"{step['step_id']}/{ix['interaction_id']}: UNVERIFIED — no checker registered for interaction type {t!r}")


# ------------------------------------------------------------------ registry gate (stage 01)
def check_registry(registry, rep):
    for e in schema_errors(registry, "scenario_asset_registry.schema.json"):
        rep.e(f"schema: {e}")
    if rep.E:
        return
    ids = [a["asset_id"] for a in registry["assets"]]
    for dup in {i for i in ids if ids.count(i) > 1}:
        rep.e(f"duplicate asset_id {dup}")
    scen = {s["scenario_id"] for s in registry["scenarios"]}
    C = SimpleNamespace(registry=registry)
    for a in registry["assets"]:
        if a["scenario_id"] not in scen:
            rep.e(f"{a['asset_id']}: unknown scenario_id {a['scenario_id']}")
        if a["asset_kind"] in checkers.ASSET:
            checkers.ASSET[a["asset_kind"]](C, a, rep)
        else:
            rep.w(f"{a['asset_id']}: UNVERIFIED — no checker registered for asset kind {a['asset_kind']!r}")


# ------------------------------------------------------------------ tile gate (stage 07)
def validate_tile(C, tile_id, strict=False):
    rep = Report(tile_id)
    path = C.B / "tile_lessons" / f"{tile_id}.json"
    if not path.exists():
        rep.e("tile_lessons file missing (run assemble_tiles.py)")
        return rep, {}
    L = load(path)
    for e in schema_errors(L, "tile_lesson.schema.json"):
        rep.e(f"schema: {e}")
    if rep.E:
        return rep, {}
    plan = C.plans[tile_id]
    bundles = C.bundles
    cids = set(L["concept_ids"])
    if cids != set(plan["concept_ids"]):
        rep.e("concept_ids differ from the plan")
    # structure
    sids = [s["step_id"] for s in L["steps"] + L["remediation_steps"]]
    for d in {s for s in sids if sids.count(s) > 1}:
        rep.e(f"duplicate step_id {d}")
    for s in sids:
        if not s.startswith(tile_id + "."):
            rep.e(f"step_id {s} must start with '{tile_id}.'")
    iids = [s["interaction"]["interaction_id"] for s in L["steps"] if "interaction" in s]
    for d in {i for i in iids if iids.count(i) > 1}:
        rep.e(f"duplicate interaction_id {d}")
    rem_ids = {s["step_id"] for s in L["remediation_steps"]}
    referenced = {s["interaction"]["feedback"]["remediation_step_id"] for s in L["steps"] if s.get("interaction", {}).get("feedback", {}).get("remediation_step_id")}
    for r in referenced - rem_ids:
        rep.e(f"feedback.remediation_step_id {r} is not a remediation step")
    for r in rem_ids - referenced:
        rep.w(f"remediation step {r} is never referenced")
    for c in cids:
        if L["source"]["glossary_bundle_hashes"].get(c) != sha(bundles.by_id[c]):
            rep.e(f"source hash for {c} does not match the glossary bundle")
    if L["source"]["scenario_registry_hash"] != sha(C.registry):
        rep.e("scenario_registry_hash is stale (registry changed after assembly — re-assemble)")
    if L["content_hash"] != sha({k: v for k, v in L.items() if k != "content_hash"}):
        rep.e("content_hash mismatch (file edited after assembly)")
    # pass over steps in learner order
    taught, measured, practice_done, visual_done = set(), set(), set(), set()
    blocked_names = {}
    for c in cids:
        for bid in bundles.by_id[c]["context"].get("blocked_future_concepts", []):
            nm = bundles.raw.get("names", {}).get(bid)
            if nm and len(nm) >= 6:
                blocked_names[nm.lower()] = bid
    for s in L["steps"] + L["remediation_steps"]:
        st_words = 0
        for b in iter_blocks(s.get("blocks")):
            check_block(C, s, b, rep)
            lin = b.get("lineage", {})
            if b["type"] in TEXT_BLOCKS:
                st_words += words(b["text"])
                if VIDEO_PHRASES.search(b["text"]):
                    rep.e(f"{s['step_id']}: text refers to the video — the text must teach on its own")
                low = b["text"].lower()
                for nm, bid in blocked_names.items():
                    if re.search(r"\b" + re.escape(nm) + r"\b", low):
                        rep.w(f"{s['step_id']}: text contains the name of blocked future concept {bid} ({nm!r}) — check it is not needed to understand")
                if not lin.get("fact_ids"):
                    rep.w(f"{s['step_id']}: {b['type']} block without lineage.fact_ids")
                for f in lin.get("fact_ids", []):
                    cid, _, fid = f.partition("#")
                    if cid not in cids or fid not in bundles.facts(cid):
                        rep.e(f"{s['step_id']}: lineage fact {f} does not exist in the glossary bundle")
                for tb in lin.get("teaching_block_ids", []):
                    cid, _, bid = tb.partition("#")
                    if cid not in cids or bid not in bundles.blocks(cid):
                        rep.e(f"{s['step_id']}: lineage teaching block {tb} does not exist")
            for a in lin.get("anchors", []):
                if a.endswith("#visual"):
                    visual_done.add(a.split("#")[0])
        for a in s["lineage"].get("anchors", []):
            if a.endswith("#visual"):
                visual_done.add(a.split("#")[0])
            if a.endswith("#practice") and s["type"] == "hands_on":
                practice_done.add(a.split("#")[0])
        for f in s["lineage"].get("fact_ids", []):
            cid, _, fid = f.partition("#")
            if cid not in cids or fid not in bundles.facts(cid):
                rep.e(f"{s['step_id']}: step lineage fact {f} does not exist in the glossary bundle")
        if s["type"] in ("explainer", "recap", "remediation") and s in L["steps"]:
            ps = next((p for p in plan["steps"] if p["step_id"] == s["step_id"]), None)
            if ps and ps["word_budget"] and st_words > ps["word_budget"] * 1.5 + 20:
                rep.e(f"{s['step_id']}: {st_words} words of text vs budget {ps['word_budget']} (hard cap 1.5x)")
            elif ps and ps["word_budget"] and st_words > ps["word_budget"] * 1.2 + 20:
                rep.w(f"{s['step_id']}: {st_words} words vs budget {ps['word_budget']}")
        ix = s.get("interaction")
        if ix:
            check_interaction(C, s, ix, rep)
            for m in ix["measures"]:
                if m["concept_id"] not in cids:
                    rep.e(f"{s['step_id']}: measures concept {m['concept_id']} is not in this tile")
                    continue
                if m["capability"] not in bundles.anchors(m["concept_id"]):
                    rep.e(f"{s['step_id']}: capability {m['capability']!r} is not a glossary assessment anchor of {m['concept_id']}")
                measured.add((m["concept_id"], m["capability"]))
                for f in m["fact_ids"]:
                    q = f"{m['concept_id']}#{f}"
                    if f not in bundles.facts(m["concept_id"]):
                        rep.e(f"{s['step_id']}: measures fact {q} does not exist")
                    elif q not in taught:
                        rep.e(f"{s['step_id']}: tests {q} but no earlier step has taught it by text (the answer would never have been taught)")
            for a in ix.get("anchors", []):
                if a.endswith("#practice"):
                    practice_done.add(a.split("#")[0])
        for b in iter_blocks(s.get("blocks")):
            if b["type"] in TEXT_BLOCKS:
                taught |= set(b.get("lineage", {}).get("fact_ids", []))
    # coverage
    for c in cids:
        for f in bundles.facts(c):
            if f"{c}#{f}" not in taught:
                rep.e(f"coverage: {c}#{f} is never taught by a text block ({bundles.facts(c)[f][:70]}...)")
        for cap in bundles.anchors(c):
            if (c, cap) not in measured:
                rep.e(f"coverage: assessment anchor {c}#{cap} is never measured by an interaction")
        b = bundles.by_id[c]
        if b.get("practice_anchor") and c not in practice_done:
            rep.e(f"coverage: practice anchor of {c} ({b['practice_anchor']['type']}) is not realised by a hands_on step (anchors must include '{c}#practice')")
        if b.get("visual_anchor") and c not in visual_done:
            rep.e(f"coverage: visual anchor of {c} ({b['visual_anchor']['type']}) is not realised (a block/step lineage.anchors must include '{c}#visual')")
        if not bundles.segments(c):
            for s in L["steps"]:
                if c in s["concept_ids"] and any(b["type"] == "media_group" for b in s.get("blocks", [])):
                    rep.e(f"{s['step_id']}: media_group for {c}, which has no approved video (media: null)")
    # plan conformance
    authored = L["steps"]
    for p in plan["steps"]:
        s = next((x for x in authored if x["step_id"] == p["step_id"]), None)
        if not s:
            rep.e(f"plan: planned step {p['step_id']} ({p['type']}) is missing")
            continue
        if s["type"] != p["type"]:
            rep.e(f"plan: {p['step_id']} is {s['type']}, plan says {p['type']}")
        if p["teaching_block_ids"] and set(s["lineage"].get("teaching_block_ids", [])) != set(p["teaching_block_ids"]):
            rep.e(f"plan: {p['step_id']} lineage.teaching_block_ids != planned {p['teaching_block_ids']}")
        if p["segment_ids"]:
            got = {sid for b in s.get("blocks", []) if b["type"] == "media_group" for sid in b["segment_ids"]}
            if got != set(p["segment_ids"]):
                rep.e(f"plan: {p['step_id']} media segments {sorted(got)} != planned {p['segment_ids']}")
        if p["planned_interaction_type"] and s.get("interaction", {}).get("type") != p["planned_interaction_type"]:
            rep.e(f"plan: {p['step_id']} interaction is {s.get('interaction', {}).get('type')}, plan says {p['planned_interaction_type']}")
        if p["planned_visual_block_type"] and p["type"] == "explainer":
            anchor = next((k for k, v in VISUAL_MAP.items() if v == p["planned_visual_block_type"]), "")
            ok_types = {p["planned_visual_block_type"]} | set(ALTERNATES.get(anchor, []))
            if not ok_types & {b["type"] for b in iter_blocks(s.get("blocks"))}:
                rep.e(f"plan: {p['step_id']} must contain a {' or '.join(sorted(ok_types))} block ({p['visual_purpose']})")
        for a in p["anchors"]:
            if a.split("#", 1)[1].startswith("assessment:") and s.get("interaction"):
                cap = a.split("assessment:")[1]
                if (a.split("#")[0], cap) not in {(m["concept_id"], m["capability"]) for m in s["interaction"]["measures"]}:
                    rep.w(f"plan: {p['step_id']} was planned to measure {a} but its interaction does not")
    planned = {p["step_id"] for p in plan["steps"]}
    for s in authored:
        if s["step_id"] not in planned:
            (rep.w if s["type"] in ("check", "explainer") else rep.e)(f"plan: extra step {s['step_id']} ({s['type']}) not in the plan")
    unverified = [w for w in rep.W if "UNVERIFIED" in w]
    stats = {"steps": len(authored), "by_type": {t: sum(1 for s in authored if s["type"] == t) for t in sorted({s['type'] for s in authored})},
             "interactions": sorted({s["interaction"]["type"] for s in authored if "interaction" in s}), "est_minutes": L["pacing"].get("estimated_minutes"),
             "unverified": len(unverified)}
    if strict and unverified:
        rep.e(f"strict: {len(unverified)} item(s) could not be verified by any checker (see UNVERIFIED warnings)")
    return rep, stats


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("batch_dir")
    ap.add_argument("--registry", action="store_true")
    ap.add_argument("--tile")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    B = Path(a.batch_dir)
    reports = []
    if a.registry:
        rep = Report("scenario_asset_registry")
        check_registry(load(B / "scenario_asset_registry.json"), rep)
        if a.strict and any("UNVERIFIED" in w for w in rep.W):
            rep.e("strict: some asset kinds could not be verified")
        reports.append((rep, {}))
    else:
        C = Ctx(B)
        for t in ([a.tile] if a.tile else C.ctx["tile_ids"]):
            reports.append(validate_tile(C, t, a.strict))
    bad, out = False, []
    for rep, stats in reports:
        status = "PASS" if not rep.E else "FAIL"
        bad |= bool(rep.E)
        out.append({"name": rep.name, "status": status, "errors": rep.E, "warnings": rep.W, "stats": stats})
        if not a.json:
            print(f"{rep.name}: {status}  ({len(rep.E)} error, {len(rep.W)} warning)  {json.dumps(stats) if stats else ''}")
            for m in rep.E:
                print("  E", m)
            for m in rep.W:
                print("  W", m)
    if a.json:
        print(json.dumps(out, indent=2))
    (B / "reports").mkdir(exist_ok=True)
    save(B / "reports" / ("validation.registry.json" if a.registry else "validation.tiles.json"), out)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
