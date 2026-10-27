"""What does this path's glossary need from the player? Reads the glossary bundle and reports, against the registries:
visual anchor types -> block types, practice anchor types -> interaction types, preferred video visual modes, concept domains -> runtimes.
Anything unmapped = a block/interaction/runtime a developer must build (and register) before those concepts can be authored.

  python3 visual_inventory.py <path_glossary_bundle.json> [--out report.json]
"""
import collections
import json
import sys

from finlib import CORE, Bundles, load, profile

MAP = load(CORE / "registry" / "anchor_mapping.json")
BLOCKS = {b["type"]: b for b in load(CORE / "registry" / "block_registry.json")["blocks"]}
IX = {i["type"]: i for i in load(CORE / "registry" / "interaction_registry.json")["interactions"]}


def main():
    bundles = Bundles(sys.argv[1])
    prof = profile(bundles.raw["path_id"])
    bs = bundles.raw["bundles"]
    vis = collections.Counter(b["visual_anchor"]["type"] for b in bs if b.get("visual_anchor"))
    pra = collections.Counter(b["practice_anchor"]["type"] for b in bs if b.get("practice_anchor"))
    modes = collections.Counter(m for b in bs for m in b["video_need"]["preferred_visual_modes"])
    dom = collections.Counter(b["context"]["concept_id"].split(".")[0] for b in bs)
    rep = {"path_id": bundles.raw["path_id"], "concepts": len(bs), "visual": [], "practice": [], "runtimes": [], "video_modes": dict(modes), "gaps": []}
    print(f"{rep['path_id']}: {len(bs)} concepts\n\nVISUAL ANCHORS -> block types")
    for t, n in vis.most_common():
        blk = MAP["visual_anchor_to_block"].get(t)
        pack = BLOCKS[blk]["pack"] if blk in BLOCKS else None
        rep["visual"].append({"anchor": t, "count": n, "block": blk, "pack": pack})
        print(f"  {n:4}  {t:22} -> {blk or '*** NO BLOCK ***'}{f' ({pack} pack, {BLOCKS[blk]['status']})' if pack else ''}")
        if not blk:
            rep["gaps"].append(f"visual anchor {t}")
    print("\nPRACTICE ANCHORS -> interaction types")
    for t, n in pra.most_common():
        cands = MAP["practice_anchor_to_interaction"].get(t, [])
        rep["practice"].append({"anchor": t, "count": n, "interactions": cands})
        print(f"  {n:4}  {t:18} -> {', '.join(cands) or '*** NO INTERACTION TYPE ***'}")
        if not cands:
            rep["gaps"].append(f"practice anchor {t}")
    print("\nCONCEPT DOMAINS -> runtimes")
    for d, n in dom.most_common():
        rt = prof["runtime_by_concept_prefix"].get(d)
        rep["runtimes"].append({"domain": d, "concepts": n, "runtime": rt})
        print(f"  {n:4}  {d:12} -> {rt or '(none needed)'}")
    print("\nVIDEO preferred_visual_modes (informational):", ", ".join(f"{m} {n}" for m, n in modes.most_common()))
    print("\nGAPS (build before authoring):", rep["gaps"] or "none")
    if "--out" in sys.argv:
        (open(sys.argv[sys.argv.index("--out") + 1], "w")).write(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
