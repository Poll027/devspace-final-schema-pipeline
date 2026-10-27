"""Stage 00 (script): verify the frozen TOC + glossary batch, and stage the batch's inputs.

  python3 preflight.py batches/<batch_id> --path-id data_analyst --glossary-bundle <path_glossary_bundle.X.json> \
      --glossary-batch-id <id> --toc-workspace <dir with freeze_manifest.json> [--tiles tile_a,tile_b] [--player-version 0.1.0]

Writes batches/<batch_id>/inputs/path_glossary_bundle.json (only the chosen tiles' bundles, plus a `names` map of EVERY concept
so the leakage lint can name blocked future concepts) and batch_run_context.json. Refuses unless every chosen bundle is
ready_for_final_schema and the TOC workspace has a freeze_manifest.json.
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from finlib import Bundles, load, save, sha_file
from schema_check import validate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch_dir")
    ap.add_argument("--path-id", required=True)
    ap.add_argument("--glossary-bundle", required=True)
    ap.add_argument("--glossary-batch-id", required=True)
    ap.add_argument("--toc-workspace", required=True)
    ap.add_argument("--tiles", default="", help="comma list; default = every tile in the bundle")
    ap.add_argument("--player-version", default="0.1.0")
    a = ap.parse_args()

    B = Path(a.batch_dir)
    freeze = Path(a.toc_workspace) / "freeze_manifest.json"
    if not freeze.exists():
        sys.exit(f"REFUSED: {freeze} missing — the TOC is not frozen")
    bundles = Bundles(a.glossary_bundle)
    all_tiles = bundles.tiles()
    chosen = [t for t in a.tiles.split(",") if t] or list(all_tiles)
    missing = [t for t in chosen if t not in all_tiles]
    if missing:
        sys.exit(f"REFUSED: tiles not in the glossary bundle: {missing}")
    not_ready = [c for t in chosen for c in all_tiles[t] if not bundles.by_id[c]["validation"].get("ready_for_final_schema")]
    if not_ready:
        sys.exit(f"REFUSED: bundles not ready_for_final_schema: {not_ready}")

    keep = {c for t in chosen for c in all_tiles[t]}
    subset = {
        "path_id": bundles.raw["path_id"], "batch_id": bundles.raw["batch_id"], "assembled_at": bundles.raw["assembled_at"],
        "source_file_sha256": sha_file(a.glossary_bundle),
        "bundles": [b for b in bundles.raw["bundles"] if b["context"]["concept_id"] in keep],
        "clusters": [c for c in bundles.raw["clusters"] if set(c["concept_ids"]) & keep],
        "names": {cid: bundles.name(cid) for cid in bundles.order},
        "tile_order": list(all_tiles),
    }
    (B / "inputs").mkdir(parents=True, exist_ok=True)
    save(B / "inputs" / "path_glossary_bundle.json", subset)
    ctx = {"batch_id": B.name, "path_id": a.path_id, "glossary_bundle_file": "inputs/path_glossary_bundle.json", "glossary_batch_id": a.glossary_batch_id,
           "toc_workspace": str(Path(a.toc_workspace)), "toc_freeze_hash": sha_file(freeze), "tile_ids": chosen,
           "player_version": a.player_version, "created_at": datetime.now(timezone.utc).isoformat()}
    validate(ctx, "batch_run_context.schema.json")
    save(B / "batch_run_context.json", ctx)
    print(f"PREFLIGHT OK: {len(chosen)} tile(s), {len(keep)} concept(s) staged in {B}/inputs")


if __name__ == "__main__":
    main()
