"""ASSET checker for rendered images (render_plot.py): the file exists under assets/, its sha256 matches, its provenance sidecar exists, and under --strict
the sidecar code re-renders to the same bytes. An image that cannot be reproduced from code and registered data does not pass: the pipeline never accepts a
typed-in or hand-edited picture."""
import hashlib
from pathlib import Path


def check_image(C, a, rep):
    here, uri = a["asset_id"], a["uri"]
    if uri.startswith("/") or ".." in Path(uri).parts or not uri.startswith("assets/"):
        rep.e(f"{here}: uri {uri!r} must be a relative path under assets/")
        return
    base = getattr(C, "base", None)
    if base is None:
        rep.w(f"{here}: UNVERIFIED — image asset checked without the batch folder")
        return
    f = Path(base) / uri
    if not f.exists():
        rep.e(f"{here}: file {uri} is missing")
        return
    digest = hashlib.sha256(f.read_bytes()).hexdigest()
    if not a.get("sha256"):
        rep.e(f"{here}: sha256 is required for an image asset (render_plot.py writes it)")
    elif a["sha256"] != digest:
        rep.e(f"{here}: sha256 does not match {uri} (edited after rendering?)")
    if not (Path(base) / "assets" / f"{here}.render.json").exists():
        rep.e(f"{here}: no render provenance assets/{here}.render.json: images must come from render_plot.py")
    elif getattr(C, "strict", False):
        import render_plot  # at call time: render_plot imports this package
        for _, why in render_plot.verify(Path(base), C.registry, only={here}):
            rep.e(f"{here}: {why}")


ASSET = {"image": check_image}
