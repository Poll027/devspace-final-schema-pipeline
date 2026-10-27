"""Shared, role-agnostic helpers: hashing, glossary-bundle access, per-path profile, batch context. (Dataset helpers live in checkers/dataset.py.)"""
import hashlib
import json
import re
from pathlib import Path

CORE = Path(__file__).resolve().parent.parent
ROOT = CORE.parent


def load(p):
    return json.loads(Path(p).read_text())


def save(p, obj):
    Path(p).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(obj):
    """sha256 of the canonical JSON form (key order and whitespace never matter)."""
    return hashlib.sha256(canon(obj).encode()).hexdigest()


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def words(text):
    return len(re.findall(r"\w+", text or ""))


# ------------------------------------------------------------------ glossary bundle access
class Bundles:
    """Index over path_glossary_bundle.<path>.json: bundles by concept_id, facts, names, segments, tile membership."""

    def __init__(self, path):
        self.raw = load(path)
        self.order = [b["context"]["concept_id"] for b in self.raw["bundles"]]
        self.by_id = {b["context"]["concept_id"]: b for b in self.raw["bundles"]}
        self.clusters = self.raw.get("clusters", [])

    def facts(self, cid):
        b = self.by_id[cid]
        out = {f["id"]: f["statement"] for f in b["coverage"]["required_facts"]}
        out.update({m["id"]: m["statement"] for m in b["coverage"].get("misconceptions", [])})
        return out

    def blocks(self, cid):
        return {t["id"]: t for t in self.by_id[cid]["teaching_blocks"]}

    def segments(self, cid):
        m = self.by_id[cid].get("media")
        return {s["segment_id"]: s for s in (m or {}).get("segments", [])}

    def anchors(self, cid):
        b = self.by_id[cid]
        return {a["capability"]: a for a in b["assessment_anchors"]}

    def name(self, cid):
        return self.by_id[cid]["context"]["concept_name"]

    def tiles(self):
        """tile_id -> ordered concept ids (TOC order, first-seen tile order preserved)."""
        out = {}
        for cid in self.order:
            out.setdefault(self.by_id[cid]["context"]["toc_location"]["tile_id"], []).append(cid)
        return out

    def next_tile(self, tile_id):
        ids = list(self.tiles())
        return ids[ids.index(tile_id) + 1] if tile_id in ids and ids.index(tile_id) + 1 < len(ids) else None


# ------------------------------------------------------------------ per-path profile (settings that differ by role live in registry/path_profiles/<path_id>.json)
def profile(path_id):
    d = CORE / "registry" / "path_profiles"
    f = d / f"{path_id}.json"
    return load(f if f.exists() else d / "_default.json")


class Ctx:
    """Everything a check needs: batch context, glossary bundles, scenario/asset registry, tile plans."""

    def __init__(self, B):
        self.B = Path(B)
        self.ctx = load(self.B / "batch_run_context.json")
        self.bundles = Bundles(self.B / self.ctx["glossary_bundle_file"])
        self.registry = load(self.B / "scenario_asset_registry.json")
        self.plans = {t["tile_id"]: t for t in load(self.B / "tile_plans.json")["tiles"]}
        self.profile = profile(self.ctx["path_id"])
