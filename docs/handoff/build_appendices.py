#!/usr/bin/env python3
"""Regenerates the handoff appendices from the repo's own artifacts, so they can never drift from the data.
  python3 docs/handoff/build_appendices.py --toc <toc.json> --glossary <path_glossary_bundle.data_analyst.json>
A: tile catalog | B: block/interaction schema reference | C: dataset & asset catalog | D: glossary export (not committed) | E: example payloads."""
import argparse, collections, glob, hashlib, json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BATCHES, CORE = ROOT / "batches", ROOT / "00_FINAL_PIPELINE_CORE"
OUT = Path(__file__).parent
load = lambda p: json.load(open(p))


def latest_tiles():
    """tile_id -> (batch, full lesson, public lesson). The latest batch that produced a tile wins (001 and 002 both built the canary tile)."""
    found = {}
    for d in sorted(BATCHES.glob("final_batch_*")):
        for f in sorted((d / "tile_lessons").glob("*.json")) if (d / "tile_lessons").exists() else []:
            pub = d / "tile_lessons_public" / f.name
            found[f.stem] = (d.name, load(f), load(pub) if pub.exists() else None)
    return found


def appendix_a(toc, tiles):
    L = ["# Appendix A: Tile catalog (all 72 tiles, in learning order)", "",
         "Source: `tile_lessons/` of the batch named in each row. Order, regions and terrains come from the frozen TOC (`04_data_analyst_V2_WORKSPACE/toc.json`).", ""]
    n = 0
    for r in toc["regions"]:
        L += [f"## Region: {r['title']} (`{r['region_id']}`)", r.get("summary", ""), ""]
        for t in r["terrains"]:
            L += [f"### Terrain: {t['title']} (`{t['terrain_id']}`)", t.get("summary", ""), ""]
            for tl in t["tiles"]:
                n += 1
                b, full, pub = tiles[tl["tile_id"]]
                steps = collections.Counter(s["type"] for s in full["steps"])
                ixs = collections.Counter(s["interaction"]["type"] for s in full["steps"] if s.get("interaction"))
                rt = full["requires"].get("runtimes", [])
                L += [f"#### {n}. {full['title']}  (`{tl['tile_id']}`)", f"{full.get('summary', '')}", "",
                      f"- Concepts: {', '.join('`'+c+'`' for c in full['concept_ids'])}",
                      f"- Built in: `{b}` | content_hash `{full['content_hash'][:12]}…` | steps {len(full['steps'])} ({', '.join(f'{v} {k}' for k, v in steps.items())}) | remediation steps {len(full.get('remediation_steps') or [])}",
                      f"- Interactions: {', '.join(f'{v} {k}' for k, v in ixs.items()) or 'none'} | runtimes: {', '.join(rt) or 'none'} | packs: {', '.join(full['requires']['packs'])}",
                      f"- Blocks used: {', '.join(full['requires']['block_types'])}",
                      f"- Assets: {', '.join(full['requires']['asset_ids']) or 'none'} | est. minutes: {(full.get('pacing') or {}).get('estimated_minutes', '?')} | completion reward: {full['completion'].get('reward')} | next tile: `{full['completion'].get('next_tile_id')}`",
                      f"- Public copy present: {'yes' if pub else 'no'} | step titles: " + "; ".join(s['title'] for s in full['steps']), ""]
    (OUT / "appendix_A_tile_catalog.md").write_text("\n".join(L))
    return n


def props(schema, depth=0, defs=None):
    out = []
    if not isinstance(schema, dict):
        return out
    req = set(schema.get("required", []))
    for k, v in (schema.get("properties") or {}).items():
        if "$ref" in v:
            t = v["$ref"].split("/")[-1]
        elif "enum" in v:
            t = "enum " + " | ".join(map(str, v["enum"])) if len(v["enum"]) < 14 else f"enum ({len(v['enum'])} values)"
        elif v.get("const") is not None:
            t = f"const {v['const']!r}"
        elif v.get("type") == "array":
            it = v.get("items", {})
            t = "array of " + (it.get("$ref", "").split("/")[-1] or it.get("type") or ("object" if it.get("properties") else "?"))
        elif "oneOf" in v or "anyOf" in v:
            t = "one of several shapes"
        else:
            t = v.get("type", "object" if v.get("properties") else "?")
            if v.get("minLength"):
                t += f" (min {v['minLength']} chars)"
        out.append(("  " * depth) + f"- `{k}`{' *(required)*' if k in req else ''}: {t}")
        if v.get("type") == "object" and v.get("properties") and depth < 2:
            out += props(v, depth + 1)
        if v.get("type") == "array" and isinstance(v.get("items"), dict) and v["items"].get("properties") and depth < 2:
            out += props(v["items"], depth + 1)
    return out


def appendix_b():
    L = ["# Appendix B: Schema reference", "",
         "Generated from `00_FINAL_PIPELINE_CORE/schemas/*.json` and `registry/*.json`. The JSON Schemas are the contract: validate every lesson you ingest against them (`scripts/schema_check.py` does, with `jsonschema` Draft 2020-12 and cross-file `$ref`s).", ""]
    for name, title in [("tile_lesson", "Tile lesson (the unit the backend stores)"), ("step", "Step"), ("common", "Shared definitions (`$defs`)")]:
        s = load(CORE / "schemas" / f"{name}.schema.json")
        L += [f"## {title}", f"File: `schemas/{name}.schema.json`", ""]
        if name == "common":
            for k, v in s.get("$defs", {}).items():
                L += [f"### `{k}`"] + (props(v) or [f"`{json.dumps(v)[:300]}`"]) + [""]
        else:
            L += props(s) + [""]
    br, ir = load(CORE / "registry" / "block_registry.json"), load(CORE / "registry" / "interaction_registry.json")
    L += ["## Block types", "", "| type | pack | status | min player |", "|---|---|---|---|"] + [f"| {b['type']} | {b['pack']} | {b['status']} | {b['min_player_version']} |" for b in br["blocks"]] + [""]
    for b in br["blocks"]:
        s = load(CORE / "schemas" / b["schema"])
        L += [f"### Block `{b['type']}` ({b['pack']})"] + props(s) + [""]
    L += ["## Interaction types", "", "| type | pack | status |", "|---|---|---|"] + [f"| {i['type']} | {i['pack']} | {i['status']} |" for i in ir["interactions"]] + [""]
    for i in ir["interactions"]:
        s = load(CORE / "schemas" / i["schema"])
        L += [f"### Interaction `{i['type']}` ({i['pack']})"] + props(s) + [""]
    (OUT / "appendix_B_schema_reference.md").write_text("\n".join(L))


def appendix_c(tiles):
    by = collections.defaultdict(dict)
    scen = {}
    for d in sorted(BATCHES.glob("final_batch_*")):
        p = d / "scenario_asset_registry.json"
        if p.exists():
            r = load(p)
            for a in r["assets"]:
                by[a["asset_id"]][d.name] = a
            for s in r.get("scenarios", []):
                scen[s.get("scenario_id")] = s
    L = ["# Appendix C: Datasets, code workspaces and scenarios", "",
         f"{len(by)} distinct asset ids across the batches' `scenario_asset_registry.json` files.", "",
         "## IMPORTANT: asset ids are not globally unique",
         "Each batch has its own registry. **Seven asset ids occur in several batches with different content** (different rows/columns). A lesson refers to an asset by `asset_id` only; the registry it was authored against is identified by `source.scenario_registry_hash` in the lesson. "
         "The backend must therefore key assets by `(scenario_registry_hash, asset_id)` (or by a content hash of the asset), never by `asset_id` alone, or lessons will silently read the wrong data.", ""]
    for k, v in by.items():
        if len(v) > 1:
            L.append(f"- `{k}`: " + "; ".join(f"{b}: {len(a.get('rows', []))} rows, columns {[c['name'] for c in a.get('columns', [])]}" for b, a in v.items()))
    L += ["", "## Scenarios", ""] + [f"- `{k}`: {s.get('title', '')} - {s.get('description', '')[:300]}" for k, s in scen.items()] + ["", "## Assets", ""]
    for k, v in sorted(by.items()):
        for b, a in v.items():
            h = hashlib.sha256(json.dumps(a, sort_keys=True).encode()).hexdigest()[:10]
            L += [f"### `{k}` ({a['asset_kind']}) - batch `{b}` - content `{h}`", f"{a.get('description', '')}", ""]
            if a["asset_kind"] == "dataset":
                L += [f"Rows: {len(a.get('rows', []))}" + (", variants: " + ", ".join(f"`{x['variant_id']}`" for x in a.get("variants", [])) if a.get("variants") else ""),
                      "| column | type | role | notes |", "|---|---|---|---|"] + [f"| {c['name']} | {c.get('type', '')} | {c.get('semantic_role', '')} | {c.get('description', '')[:120]} |" for c in a.get("columns", [])] + [""]
            else:
                L += [f"`{json.dumps({x: y for x, y in a.items() if x not in ('asset_id', 'description')})[:600]}`", ""]
    (OUT / "appendix_C_assets.md").write_text("\n".join(L))


def appendix_d(path):
    g = load(path)
    L = ["# Appendix D: Glossary export (Data Analyst path)", "",
         f"{g['counts']['concepts']} concepts, {g['counts']['segments']} video segments on {g['counts']['with_video']} concepts; depth tiers {g['counts']['core']} core / {g['counts']['standard']} standard / {g['counts']['reference']} reference. "
         "This is the teaching bank the lessons were built from. **Not committed to git** (see BACKEND_HANDOFF.md section 2).", "",
         "## Clusters (concept groups the TOC assigned to tiles)", ""]
    L += [f"- `{c['cluster_id']}` -> `{c['tile_id']}`: {c['title']} ({', '.join(c['concept_ids'])})" for c in g["clusters"]] + [""]
    for b in g["bundles"]:
        c, cov = b["context"], b["coverage"]
        L += [f"## `{c['concept_id']}`: {c['concept_name']}", f"- Depth tier: {c['depth_tier']} | tile: `{c['toc_location']['tile_id']}` | prerequisites: {', '.join(c['prerequisites']) or 'none'}",
              f"- Learning objective: {cov['learning_objective']}", "", "**Required facts**", ""]
        L += [f"- `{f['id']}` {f['statement']}  *(sources: {', '.join(f.get('source_refs', []))})*" for f in cov["required_facts"]]
        if cov.get("misconceptions"):
            L += ["", "**Misconceptions**"] + [f"- {json.dumps(m)}" for m in cov["misconceptions"]]
        L += ["", "**Teaching blocks**", ""] + [f"- `{t['id']}` ({t['purpose']}; facts {', '.join(t.get('fact_ids', []))}): {t['content']}" for t in b["teaching_blocks"]]
        vn = b.get("video_need") or {}
        L += ["", f"**Video need:** {vn.get('level')} - {vn.get('reason', '')}"]
        if b.get("media"):
            L += [f"**Media group:** {b['media'].get('group_title')}"] + [f"- `{s['segment_id']}` {s['youtube_url']} {s['start_seconds']}-{s['end_seconds']}s (facts {', '.join(s['fact_ids'])}): {s['label']}. {s['summary']}" for s in b["media"]["segments"]]
        L += ["", "**Assessment anchors**"] + [f"- {a['capability']} (facts {', '.join(a['fact_ids'])})" for a in b["assessment_anchors"]]
        pa, va = b.get("practice_anchor") or {}, b.get("visual_anchor") or {}
        L += ["", f"**Practice anchor:** {pa.get('type')} - {pa.get('objective', '')} | success: {pa.get('success', '')}"]
        if pa.get("live_code"):
            L += [f"  - live_code: `{json.dumps(pa['live_code'])[:900]}`"]
        L += [f"**Visual anchor:** {va.get('type')} - {va.get('purpose', '')}", "**Teaching notes:** " + " | ".join(b.get("teaching_notes") or []), ""]
    (OUT / "appendix_D_glossary_export.md").write_text("\n".join(L))


def appendix_e(tiles):
    seen, L = {}, ["# Appendix E: Example payloads", "", "One real, complete interaction of each type used by the Data Analyst path (as stored in `interactions.json`: `public` goes to the player, `grading` stays server-side when `grading_mode` is `server`).", ""]
    for b, full, pub in tiles.values():
        for s in full["steps"]:
            i = s.get("interaction")
            key = (i["type"], (i.get("public") or {}).get("runtime", {}).get("kind")) if i else None
            if i and key not in seen and len(json.dumps(i)) < 9000:
                seen[key] = (full["tile_id"], s["step_id"], i)
    for (t, rk), (tile, step, i) in sorted(seen.items(), key=str):
        L += [f"## `{t}`" + (f" ({rk})" if rk else ""), f"From `{tile}` step `{step}`.", "", "```json", json.dumps(i, indent=1), "```", ""]
    full = next(iter(tiles.values()))[1]
    step = next(s for s in full["steps"] if s["type"] == "explainer")
    L += ["## One explainer step with its blocks (shape of the non-interactive content)", "", "```json", json.dumps(step, indent=1)[:7000], "```", ""]
    (OUT / "appendix_E_examples.md").write_text("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--toc", required=True)
    ap.add_argument("--glossary")
    a = ap.parse_args()
    tiles = latest_tiles()
    print("tiles:", len(tiles), "| catalog rows:", appendix_a(load(a.toc), tiles))
    appendix_b(); appendix_c(tiles); appendix_e(tiles)
    if a.glossary:
        appendix_d(a.glossary)
    print("written to", OUT)
