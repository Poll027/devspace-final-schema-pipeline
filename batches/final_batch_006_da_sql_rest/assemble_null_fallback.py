"""Assemble tile_sql_null_fallback_and_union from interactions.json."""
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
TILE_ID = "tile_sql_null_fallback_and_union"

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
    segs = []
    for sid in ids:
        cid = cid_by_seg.get(sid)
        if not cid:
            errs.append(f"segment {sid} not found in glossary bundle")
            continue
        raw = bundles.segment(cid, sid)
        segs.append({k: raw[k] for k in SEG_FIELDS if k in raw})
    block["segments"] = segs


errs = []
plan = plans[TILE_ID]
sc = screens.get(TILE_ID)
ix = inters.get(TILE_ID, {})

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
            if run.provenance:
                s["interaction"]["grading"]["execution_provenance"] = run.provenance
                s["interaction"]["grading"]["hidden_checks"] = run.hidden_checks
                print(f"  Provenance set, {len(run.hidden_checks)} hidden checks")
            if run.problems:
                errs += [f"{s['step_id']}: {p}" for p in run.problems]
    for b in iter_blocks(s.get("blocks")):
        if b["type"] == "media_group":
            inline_media(b, cid_by_seg, bundles, errs)
    compute_results(s.get("blocks"), registry, errs)

if errs:
    for e in errs:
        print(f"ERROR: {e}")
    sys.exit(1)

# Build tile lesson (simplified)
tile_lesson = {
    "schema_version": "0.1.0",
    "path_id": ctx["path_id"],
    "tile_id": TILE_ID,
    "steps": steps,
}

# Save
save(B / "tile_lessons" / f"{TILE_ID}.json", tile_lesson)
print(f"{TILE_ID}: assembled ({len(steps)} steps)")
