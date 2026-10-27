"""Stage 02 (script): deterministic step skeleton per tile — the STRUCTURE is decided here by rules, the model only fills CONTENT.

  python3 plan_tiles.py batches/<batch_id>

Rules (all tunable at the top / in registry/anchor_mapping.json):
  * teaching blocks (minus takeaways) are packed greedily into explainer steps of <= WORD_CAP words; a misconception block may overshoot slightly
  * a concept with media gets one video step after the explainer whose facts best overlap the segments
  * assessment anchors that the practice anchor plausibly realizes (capability-token overlap) are carried by the hands_on step; the rest become
    check steps (max 2 per concept; at least 1 check per concept even if hands_on covers everything — the last anchor)
  * a practice anchor becomes one hands_on step; its interaction type is chosen from registry/anchor_mapping.json keyword rules
  * the glossary visual anchor is attached to the concept's first explainer as a planned visual block type
  * every tile ends with one recap step (the takeaway blocks)
Anchors/facts/blocks are written fully qualified ("<concept_id>#f1", "<concept_id>#tb2", "<concept_id>#assessment:<capability>").
"""
import sys
from pathlib import Path

from finlib import CORE, Bundles, load, profile, save, words
from schema_check import validate

MAP = load(CORE / "registry" / "anchor_mapping.json")
BLOCK_REG = {b["type"]: b["pack"] for b in load(CORE / "registry" / "block_registry.json")["blocks"]}
IX_REG = {i["type"]: i["pack"] for i in load(CORE / "registry" / "interaction_registry.json")["interactions"]}
WORD_CAP, MISCONCEPTION_SLACK = 180, 40
MIN_STEPS, MAX_STEPS = 6, 16
IGN = set(MAP["verbs_ignored_in_capability_tokens"])


def group_blocks(blocks):
    groups, cur, cw = [], [], 0
    for b in blocks:
        w = words(b["content"])
        cap = WORD_CAP + (MISCONCEPTION_SLACK if b["purpose"] == "misconception" else 0)
        if cur and cw + w > cap:
            groups.append(cur)
            cur, cw = [], 0
        cur.append(b)
        cw += w
    if cur:
        groups.append(cur)
    return groups


def realized_by_practice(capability, practice):
    toks = [t for t in capability.lower().split("_") if t not in IGN and len(t) > 2]
    text = (practice["objective"] + " " + practice["success"]).lower()
    if not toks:
        return False
    hits = sum(1 for t in toks if t in text or t.rstrip("s") in text)
    return hits / len(toks) >= 0.5


def pick_interaction(ptype, practice):
    text = (practice["objective"] + " " + practice["success"]).lower()
    for rule in MAP["interaction_keyword_rules"]:
        if ptype in rule["anchor_types"] and any(k in text for k in rule["keywords"]):
            return rule["interaction"], f"keyword rule -> {rule['interaction']}"
    cands = MAP["practice_anchor_to_interaction"].get(ptype, [])
    return (cands[0], f"default for practice type {ptype}") if cands else (None, f"NO interaction type registered for practice type {ptype}")


def plan_tile(bundles, tile_id, cids, next_tile, prof):
    steps, warnings = [], []
    n = [0]

    def sid():
        n[0] += 1
        return f"{tile_id}.s{n[0]:02d}"

    recap_blocks, recap_facts = [], []
    for cid in cids:
        b = bundles.by_id[cid]
        blocks = [t for t in b["teaching_blocks"] if t["purpose"] != "takeaway"]
        for t in b["teaching_blocks"]:
            if t["purpose"] == "takeaway":
                recap_blocks.append(f"{cid}#{t['id']}")
                recap_facts += [f"{cid}#{f}" for f in t["fact_ids"]]
        groups = group_blocks(blocks)
        va = b.get("visual_anchor")
        vblock = MAP["visual_anchor_to_block"].get(va["type"]) if va else None
        if va and not vblock:
            warnings.append(f"{cid}: visual_anchor type {va['type']!r} has no block mapping (needs a new block type)")
        expl_ids = []
        for gi, g in enumerate(groups):
            s = {"step_id": sid(), "type": "explainer", "concept_ids": [cid],
                 "teaching_block_ids": [f"{cid}#{t['id']}" for t in g],
                 "fact_ids": sorted({f"{cid}#{f}" for t in g for f in t["fact_ids"]}),
                 "segment_ids": [], "anchors": [], "planned_interaction_type": None, "planned_visual_block_type": None, "visual_purpose": None,
                 "word_budget": min(WORD_CAP + MISCONCEPTION_SLACK, sum(words(t["content"]) for t in g)), "mapping_rule": None}
            if gi == 0 and vblock:
                s["planned_visual_block_type"], s["visual_purpose"], s["anchors"] = vblock, va["purpose"], [f"{cid}#visual"]
            steps.append(s)
            expl_ids.append(s)
        segs = bundles.segments(cid)
        if segs:
            seg_facts = {f"{cid}#{f}" for s in segs.values() for f in s["fact_ids"]}
            best = max(expl_ids, key=lambda e: (len(set(e["fact_ids"]) & seg_facts), expl_ids.index(e)))
            pos = steps.index(best) + 1
            steps.insert(pos, {"step_id": "", "type": "video", "concept_ids": [cid], "teaching_block_ids": [], "fact_ids": sorted(seg_facts & set(bundles_facts(bundles, cid))),
                               "segment_ids": list(segs), "anchors": [], "planned_interaction_type": None, "planned_visual_block_type": "media_group", "visual_purpose": None,
                               "word_budget": 0, "mapping_rule": "concept has approved media"})
        anchors = b["assessment_anchors"]
        practice = b.get("practice_anchor")
        hands_anchors = [a for a in anchors if practice and realized_by_practice(a["capability"], practice)]
        check_anchors = [a for a in anchors if a not in hands_anchors]
        if not check_anchors and anchors:
            check_anchors = [anchors[-1]]
        bins = [[a] for a in check_anchors] if len(check_anchors) <= 2 else [check_anchors[: (len(check_anchors) + 1) // 2], check_anchors[(len(check_anchors) + 1) // 2:]]
        for bn in bins:
            steps.append({"step_id": "", "type": "check", "concept_ids": [cid], "teaching_block_ids": [],
                          "fact_ids": sorted({f"{cid}#{f}" for a in bn for f in a["fact_ids"]}), "segment_ids": [],
                          "anchors": [f"{cid}#assessment:{a['capability']}" for a in bn], "planned_interaction_type": MAP["check_default_interaction"],
                          "planned_visual_block_type": None, "visual_purpose": None, "word_budget": 0, "mapping_rule": "default_check"})
        if practice:
            itype, rule = pick_interaction(practice["type"], practice)
            if itype is None:
                warnings.append(f"{cid}: {rule} (needs a new interaction type)")
            steps.append({"step_id": "", "type": "hands_on", "concept_ids": [cid], "teaching_block_ids": [],
                          "fact_ids": sorted({f"{cid}#{f}" for a in hands_anchors for f in a["fact_ids"]}), "segment_ids": [],
                          "anchors": [f"{cid}#practice"] + [f"{cid}#assessment:{a['capability']}" for a in hands_anchors],
                          "planned_interaction_type": itype, "planned_visual_block_type": None, "visual_purpose": None, "word_budget": 0, "mapping_rule": rule})
    steps.append({"step_id": "", "type": "recap", "concept_ids": list(cids), "teaching_block_ids": recap_blocks, "fact_ids": sorted(set(recap_facts)), "segment_ids": [],
                  "anchors": [], "planned_interaction_type": None, "planned_visual_block_type": "up_next" if next_tile else None, "visual_purpose": None,
                  "word_budget": 90, "mapping_rule": "tile recap"})
    for i, s in enumerate(steps, 1):
        s["step_id"] = f"{tile_id}.s{i:02d}"
    if not MIN_STEPS <= len(steps) <= MAX_STEPS:
        warnings.append(f"tile has {len(steps)} steps (target {MIN_STEPS}-{MAX_STEPS})")
    btypes = {"prose", "heading"} | {s["planned_visual_block_type"] for s in steps if s["planned_visual_block_type"]}
    itypes = {s["planned_interaction_type"] for s in steps if s["planned_interaction_type"]}
    packs = sorted({BLOCK_REG[t] for t in btypes if t in BLOCK_REG} | {IX_REG[t] for t in itypes if t in IX_REG})
    runtimes = sorted({prof["runtime_by_concept_prefix"].get(c.split(".")[0]) for c in cids if itypes & {"code_exercise", "formula_entry"}} - {None})
    return {"tile_id": tile_id, "region_id": bundles.by_id[cids[0]]["context"]["toc_location"]["region_id"], "terrain_id": bundles.by_id[cids[0]]["context"]["toc_location"]["terrain_id"],
            "title": next((c["title"] for c in bundles.clusters if set(c["concept_ids"]) & set(cids) and c["tile_id"] == tile_id), tile_id),
            "concept_ids": list(cids), "cluster_ids": sorted({b["cluster_ref"] for b in (bundles.by_id[c] for c in cids) if b.get("cluster_ref")}),
            "next_tile_id": next_tile, "steps": steps,
            "needs": {"packs": packs, "block_types": sorted(btypes), "interaction_types": sorted(itypes), "runtimes": runtimes}, "warnings": warnings}


def bundles_facts(bundles, cid):
    return [f"{cid}#{f}" for f in bundles.facts(cid)]


def main():
    B = Path(sys.argv[1])
    ctx = load(B / "batch_run_context.json")
    bundles = Bundles(B / ctx["glossary_bundle_file"])
    order = bundles.raw.get("tile_order") or list(bundles.tiles())
    tiles = bundles.tiles()
    out = {"schema_version": "0.1.0", "kind": "tile_plan", "path_id": ctx["path_id"], "batch_id": ctx["batch_id"], "tiles": []}
    for t in ctx["tile_ids"]:
        nxt = order[order.index(t) + 1] if t in order and order.index(t) + 1 < len(order) else None
        out["tiles"].append(plan_tile(bundles, t, tiles[t], nxt, profile(ctx["path_id"])))
    validate(out, "tile_plan.schema.json")
    save(B / "tile_plans.json", out)
    for t in out["tiles"]:
        kinds = [s["type"] for s in t["steps"]]
        print(f"{t['tile_id']}: {len(t['steps'])} steps  {' '.join(k[:4] for k in kinds)}")
        for w in t["warnings"]:
            print("  WARN", w)


if __name__ == "__main__":
    main()
