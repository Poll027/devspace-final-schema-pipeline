#!/usr/bin/env python3
"""Render matplotlib/seaborn plots to SVG image assets, deterministically, inside the pinned Pyodide sandbox (the engine the player runs).

A rendered plot is the only kind of image the pipeline can produce: real output of real code over registered data, never a typed-in picture.

    python3 render_plot.py <batch_dir> <plots.json> [--registry]   render every plot; with --registry also register them in the batch's
                                                                    scenario_asset_registry.json (replaces an image asset of the same id)
    python3 render_plot.py <batch_dir> --verify                     re-render every registered image from its sidecar and compare sha256

plots.json: {"plots": [{"asset_id": "img.styled_bars", "scenario_id": "scen.x", "title": "...", "alt_text": "what the picture shows, for a learner who cannot see it",
                        "datasets": [{"asset_id": "ds.orders", "mount_path": "orders.csv"}], "code": "import pandas as pd\\nimport matplotlib.pyplot as plt\\n..."}]}
The code reads the mounted files exactly like a learner's exercise does (`pd.read_csv("orders.csv")`), draws ONE figure (the last one is saved) and does not call savefig/show.

Writes <batch>/assets/<asset_id>.svg and a sidecar <batch>/assets/<asset_id>.render.json (the code, the datasets, the engine version, the sha256): the validator
re-renders from the sidecar under --strict, so an image that cannot be reproduced from its code fails the gate. Text is converted to paths (svg.fonttype=path)
and the hash salt is fixed, so the same code always gives the same bytes.
# ponytail: one figure per asset; no PNG (SVG scales and diffs); matplotlib's own style/rcParams are honoured, so "default vs ggplot" pairs are two assets.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from checkers import sandbox as SB  # noqa: E402

MAX_SVG_BYTES = 400_000
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PRELUDE = '''import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "devspace-final-schema"
matplotlib.rcParams["svg.fonttype"] = "path"
'''
EPILOGUE = '''
import io as _io
import matplotlib.pyplot as _plt
_buf = _io.StringIO()
_plt.gcf().savefig(_buf, format="svg", metadata={"Date": None, "Creator": None}, bbox_inches="tight")
_SVG = _buf.getvalue()
'''


def load(p):
    return json.loads(Path(p).read_text())


def _check_plot(p):
    errs = []
    for k in ("asset_id", "scenario_id", "title", "alt_text", "code"):
        if not isinstance(p.get(k), str) or not p[k].strip():
            errs.append(f"missing {k}")
    if p.get("asset_id") and not ID.match(p["asset_id"]):
        errs.append("asset_id must match [A-Za-z0-9][A-Za-z0-9._-]*")
    if len(p.get("alt_text", "")) < 20:
        errs.append("alt_text must describe what the picture shows (at least 20 characters)")
    if re.search(r"\b(savefig|plt\.show|show\(\))", p.get("code", "")):
        errs.append("the code must not call savefig/show: the renderer saves the last figure itself")
    return errs


def render(registry, plots):
    """{asset_id: {"ok": True, "svg": str, "engine": ..} | {"ok": False, "error": str}} for every plot, one sandbox job."""
    scripts, out, bad = [], {}, {}
    for p in plots:
        errs = _check_plot(p)
        problems = []
        tables, _ = SB._tables(registry, p.get("datasets", []), {}, problems)
        errs += problems
        if errs:
            bad[p.get("asset_id", "?")] = {"ok": False, "error": "; ".join(errs)}
            continue
        scripts.append(SB._py_script(p["asset_id"], "plot.py", PRELUDE + p["code"].rstrip() + "\n" + EPILOGUE, SB._py_mounts(tables),
                                     [{"id": "svg", "kind": "expr", "expr": "_SVG"}], chart=True))
    out.update(bad)
    if not scripts:
        return out
    pkgs = ["numpy", "pandas", "matplotlib"] + (["seaborn"] if any("seaborn" in p.get("code", "") for p in plots) else [])
    res = SB.node_run({"packages": pkgs, "scripts": scripts}, "run_py.mjs")
    for s in scripts:
        r = res["results"][s["id"]]
        svg = ((r.get("probes") or {}).get("svg") or {}).get("value")
        if not r.get("ok") or not isinstance(svg, str) or "<svg" not in svg:
            out[s["id"]] = {"ok": False, "error": (r.get("error") or (r.get("probes") or {}).get("svg", {}).get("error") or "the code drew no figure")[-900:] + (f"\nstdout: {r['stdout'][-300:]}" if r.get("stdout") else "")}
        elif len(svg.encode()) > MAX_SVG_BYTES:
            out[s["id"]] = {"ok": False, "error": f"the SVG is {len(svg.encode()):,} bytes (max {MAX_SVG_BYTES:,}): plot fewer marks or points"}
        else:
            out[s["id"]] = {"ok": True, "svg": svg if svg.endswith("\n") else svg + "\n", "engine": f"{res.get('engine')} {res.get('version')}"}
    return out


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def write_assets(batch, plots, results):
    entries = []
    adir = batch / "assets"
    adir.mkdir(exist_ok=True)
    for p in plots:
        r = results[p["asset_id"]]
        (adir / f"{p['asset_id']}.svg").write_text(r["svg"])
        digest = sha(r["svg"])
        (adir / f"{p['asset_id']}.render.json").write_text(json.dumps({"asset_id": p["asset_id"], "code": p["code"], "datasets": p.get("datasets", []), "engine": r["engine"],
                                                                      "sha256": digest}, indent=1) + "\n")
        entries.append({"asset_id": p["asset_id"], "asset_kind": "image", "scenario_id": p["scenario_id"], "title": p["title"], "uri": f"assets/{p['asset_id']}.svg",
                        "sha256": digest, "alt_text": p["alt_text"]})
    return entries


def verify(batch, registry, only=None):
    """[(asset_id, problem)] for every registered image whose sidecar does not reproduce the file byte for byte."""
    bad, plots = [], []
    for a in registry["assets"]:
        if a["asset_kind"] != "image" or (only and a["asset_id"] not in only):
            continue
        side = batch / "assets" / f"{a['asset_id']}.render.json"
        if not side.exists():
            bad.append((a["asset_id"], f"no render provenance assets/{a['asset_id']}.render.json (images must come from render_plot.py)"))
            continue
        s = load(side)
        plots.append({"asset_id": a["asset_id"], "scenario_id": a["scenario_id"], "title": a["title"], "alt_text": a["alt_text"], "datasets": s["datasets"], "code": s["code"]})
    res = render(registry, plots) if plots else {}
    for p in plots:
        r, f = res[p["asset_id"]], batch / "assets" / f"{p['asset_id']}.svg"
        if not r["ok"]:
            bad.append((p["asset_id"], f"re-render failed: {r['error'][-300:]}"))
        elif not f.exists() or f.read_text() != r["svg"]:
            bad.append((p["asset_id"], "the SVG on disk is not what its sidecar code renders (edited, or non-deterministic)"))
    return bad


def main():
    a = sys.argv[1:]
    if not a or "-h" in a or "--help" in a:
        print(__doc__)
        return 0
    batch = Path(a[0])
    reg_path = batch / "scenario_asset_registry.json"
    registry = load(reg_path)
    if "--verify" in a:
        bad = verify(batch, registry)
        for i, why in bad:
            print(f"FAIL {i}: {why}")
        print("verified" if not bad else f"{len(bad)} image(s) failed")
        return 1 if bad else 0
    plots = load(a[1])["plots"]
    ids = [p.get("asset_id") for p in plots]
    if len(ids) != len(set(ids)):
        print("FAIL duplicate asset_id in plots.json")
        return 1
    results = render(registry, plots)
    failed = {k: v for k, v in results.items() if not v["ok"]}
    for k, v in failed.items():
        print(f"FAIL {k}: {v['error']}")
    ok = [p for p in plots if results[p["asset_id"]]["ok"]]
    entries = write_assets(batch, ok, results)
    if "--registry" in a and entries:
        known = {s["scenario_id"] for s in registry["scenarios"]}
        for e in entries:
            if e["scenario_id"] not in known:
                print(f"FAIL {e['asset_id']}: scenario_id {e['scenario_id']} is not in the registry's scenarios")
                return 1
        ids_new = {e["asset_id"] for e in entries}
        registry["assets"] = [x for x in registry["assets"] if x["asset_id"] not in ids_new] + entries
        reg_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
    for e in entries:
        print(f"OK {e['asset_id']}  {e['uri']}  sha256={e['sha256'][:12]}  ({(batch / e['uri']).stat().st_size:,} bytes)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
