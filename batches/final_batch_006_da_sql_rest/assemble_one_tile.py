"""Assemble only tile_sql_text_dates_casts from interactions.json."""
import copy
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "00_FINAL_PIPELINE_CORE" / "scripts"))

from finlib import CORE, Bundles, load, save, sha, words
from checkers import sandbox
from schema_check import errors as schema_errors

BLOCK_PACK = {b["type"]: b["pack"] for b in load(CORE / "registry" / "block_registry.json")["blocks"]}
IX_PACK = {i["type"]: i["pack"] for i in load(CORE / "registry" / "interaction_registry.json")["interactions"]}
SEG_FIELDS = ["segment_id", "video_id", "youtube_url", "review_url", "start_seconds", "end_seconds", "label", "summary", "fact_ids", "transcript_ref"]

B = Path("batches/final_batch_006_da_sql_rest")
TILE_ID = "tile_sql_text_dates_casts"

ctx = load(B / "batch_run_context.json")
bundles = Bundles(B / ctx["glossary_bundle_file"])
plans = {t["tile_id"]: t for t in load(B / "tile_plans.json")["tiles"]}
registry = load(B / "scenario_asset_registry.json")
screens = {t["tile_id"]: t for t in load(B / "screens.json")["tiles"]}
inters = {t["tile_id"]: {i["step_id"]: i["interaction"] for i in t["interactions"]} for t in load(B / "interactions.json")["tiles"]}
cid_by_seg = {sid: cid for cid in bundles.order for sid in bundles.segments(cid)}


def iter_blocks(blocks):
    for b in blocks or []:
        yield b
        if b["type"] == "before_after":
            yield b["before"]
            yield b["after"]
        if b["type"] == "side_by_side":
            yield b["left"]
            yield b["right"]


def compute_results(blocks, registry, errs):
    for b in iter_blocks(blocks):
        if b["type"] == "data_table" and "result_of" in b:
            b.pop("result", None)
            res, problems = sandbox.run_query(registry, b["result_of"])
            if problems:
                errs += [f"data_table result_of: {p}" for p in problems]
            else:
                b["result"] = res


def inline_media(block, cid_by_seg, bundles, errs):
    ids = block["segment_ids"]
    segs, cids = [], set()
    for sid in ids:
        cid = cid_by_seg.get(sid)
        if not cid:
            errs.append(f"media_group references unknown segment {sid}")
            continue
        cids.add(cid)
        segs.append({k: bundles.segments(cid)[sid][k] for k in SEG_FIELDS if k in bundles.segments(cid)[sid]})
    block["segments"] = segs
    if len(cids) == 1:
        media = bundles.by_id[next(iter(cids))]["media"]
        block.setdefault("group_title", media.get("group_title", ""))
        if media.get("bridge_note"):
            block["bridge"] = {k: media["bridge_note"][k] for k in ("before", "after") if k in media["bridge_note"]}
    block.setdefault("default_mode", "video")


def asset_ids_used(steps):
    ids = set()
    for s in steps:
        for b in iter_blocks(s.get("blocks")):
            if "asset_ref" in b:
                ids.add(b["asset_ref"]["asset_id"])
            ids.update(m["asset_id"] for m in b.get("result_of", {}).get("asset_mounts", []))
            if b["type"] == "annotated_image":
                ids.add(b["asset_id"])
        ix = s.get("interaction")
        if ix:
            pub = ix["public"]
            if "asset_ref" in pub:
                ids.add(pub["asset_ref"]["asset_id"])
            for it in pub.get("items", []):
                if isinstance(it, dict) and "source" in it:
                    ids.add(it["source"]["asset_id"])
            for m in pub.get("workspace", {}).get("asset_mounts", []):
                ids.add(m["asset_id"])
    return sorted(ids)


tile_id = TILE_ID
errs = []
plan, sc, ix = plans[tile_id], screens.get(tile_id), inters.get(tile_id, {})
if not sc:
    print(f"{tile_id}: no screens part")
    sys.exit(1)

steps = copy.deepcopy(sc["steps"])
need = {s["step_id"] for s in steps if s["type"] in ("check", "hands_on")}
errs += [f"step {s} needs an interaction but interactions.json has none" for s in sorted(need - set(ix))]
errs += [f"interactions.json has {s} but no check/hands_on step has that id" for s in sorted(set(ix) - need)]

for s in steps:
    if s["step_id"] in ix:
        s["interaction"] = copy.deepcopy(ix[s["step_id"]])
        if s["interaction"]["type"] == "code_exercise":
            s["interaction"]["grading"].pop("execution_provenance", None)
            s["interaction"]["grading"].pop("hidden_checks", None)
            print(f"  Running sandbox for {s['step_id']}...")
            run = sandbox.run_exercise(registry, s["interaction"])
            if run.problems:
                print(f"  PROBLEMS: {run.problems}")
            if run.provenance:
                s["interaction"]["grading"]["execution_provenance"] = run.provenance
                s["interaction"]["grading"]["hidden_checks"] = run.hidden_checks
                print(f"  Provenance set, {len(run.hidden_checks)} hidden checks")
            else:
                print(f"  No provenance (problems above)")
    for b in iter_blocks(s.get("blocks")):
        if b["type"] == "media_group":
            inline_media(b, cid_by_seg, bundles, errs)
    compute_results(s.get("blocks"), registry, errs)

rem = copy.deepcopy(sc.get("remediation_steps", []))
for s in rem:
    for b in iter_blocks(s.get("blocks")):
        if b["type"] == "media_group":
            inline_media(b, cid_by_seg, bundles, errs)
    compute_results(s.get("blocks"), registry, errs)

used_blocks = sorted({b["type"] for s in steps + rem for b in iter_blocks(s.get("blocks"))})
used_ix = sorted({s["interaction"]["type"] for s in steps if "interaction" in s})
runtimes = sorted({s["interaction"]["public"]["runtime"]["kind"] for s in steps if s.get("interaction", {}).get("type") == "code_exercise"}
                  | {b["result_of"]["runtime"] for s in steps + rem for b in iter_blocks(s.get("blocks")) if b["type"] == "data_table" and "result_of" in b})
text_words = sum(words(b.get("text", "")) for s in steps for b in s.get("blocks", []) if b["type"] in ("prose", "callout"))
minutes = round(text_words / 180 + 0.75 * sum(s["type"] == "check" for s in steps) + 2 * sum(s["type"] == "hands_on" for s in steps)
                + sum((g["end_seconds"] - g["start_seconds"]) / 60 for s in steps for b in s.get("blocks", []) if b["type"] == "media_group" for g in b.get("segments", [])), 1)

lesson = {
    "schema_version": "0.1.0", "kind": "tile_lesson", "path_id": ctx["path_id"], "tile_id": tile_id,
    "toc_location": {"region_id": plan["region_id"], "terrain_id": plan["terrain_id"]},
    "title": sc["title"], "summary": sc.get("summary", ""), "concept_ids": plan["concept_ids"],
    "source": {"glossary_batch_id": ctx["glossary_batch_id"], "toc_freeze_hash": ctx["toc_freeze_hash"],
               "glossary_bundle_hashes": {c: sha(bundles.by_id[c]) for c in plan["concept_ids"]}, "scenario_registry_hash": sha(registry)},
    "requires": {"min_player_version": ctx["player_version"],
                 "packs": sorted({BLOCK_PACK[t] for t in used_blocks if t in BLOCK_PACK} | {IX_PACK[t] for t in used_ix if t in IX_PACK}),
                 "block_types": used_blocks, "interaction_types": used_ix, "runtimes": runtimes, "asset_ids": asset_ids_used(steps)},
    "pacing": {"estimated_minutes": minutes}, "steps": steps, "remediation_steps": rem,
    "completion": {"rule": "all_required_steps_complete", "reward": {"gems": sum(s.get("reward", {}).get("gems", 0) for s in steps)}, "next_tile_id": plan["next_tile_id"]},
}
lesson["content_hash"] = sha(lesson)
errs += [f"schema: {e}" for e in schema_errors(lesson, "tile_lesson.schema.json")]

if errs:
    print(f"{tile_id}: ASSEMBLY FAILED")
    for e in errs:
        print("  ", e)
    sys.exit(1)

save(B / "tile_lessons" / f"{tile_id}.json", lesson)
public, grading = copy.deepcopy(lesson), {}
for s in public["steps"]:
    ixo = s.get("interaction")
    if ixo and ixo.get("grading_mode") == "server":
        grading[ixo["interaction_id"]] = ixo.pop("grading")
public["content_hash"] = sha({k: v for k, v in public.items() if k != "content_hash"})
save(B / "tile_lessons_public" / f"{tile_id}.json", public)
save(B / "grading" / f"{tile_id}.json", grading)
print(f"{tile_id}: assembled ({len(steps)} steps, ~{minutes} min, {len(grading)} server-graded) hash {lesson['content_hash'][:12]}")
