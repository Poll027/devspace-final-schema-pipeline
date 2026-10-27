"""Core-pack checker for `code_exercise`: executes the authored solution and tests in the pinned sandbox (checkers/sandbox.py).
A runtime with no runner stays UNVERIFIED (a warning, an error under --strict)."""
from . import sandbox


def _glossary_constraints(C, ix):
    """The glossary's own live_code lists for the concepts this exercise practises (the constraints are copied from there, never invented)."""
    bundles = getattr(C, "bundles", None)
    if bundles is None:
        return None
    for a in ix.get("anchors", []):
        cid, _, kind = a.partition("#")
        if kind == "practice" and cid in bundles.by_id:
            lc = ((bundles.by_id[cid].get("practice_anchor") or {}).get("live_code")) or None
            if lc:
                return cid, lc
    return None


def code_exercise(C, step, ix, rep):
    where = f"{step['step_id']}/{ix['interaction_id']}"
    g = _glossary_constraints(C, ix)
    if g:
        cid, lc = g
        have = ix["public"].get("constraints") or {}
        for k in ("allowed_syntax", "blocked_syntax"):
            if list(have.get(k, [])) != list(lc.get(k, [])):
                rep.e(f"{where}: constraints.{k} differs from {cid}'s glossary practice anchor (it must be copied verbatim, never widened or trimmed)")
    out = sandbox.run_exercise(C.registry, ix)
    if out.unverified and not out.problems and out.provenance is None and ix["public"]["runtime"]["kind"] not in sandbox.RUNNERS:
        rep.w(f"{where}: UNVERIFIED — {out.unverified}")
        return
    for p in out.problems:
        rep.e(f"{where}: {p}")
    if out.unverified:
        rep.w(f"{where}: UNVERIFIED — {out.unverified}")
    if not out.problems:
        got = ix["grading"].get("execution_provenance")
        if got is None:
            rep.e(f"{where}: execution_provenance missing (run assemble_tiles.py: outputs come from the run, never typed)")
        elif got != out.provenance:
            rep.e(f"{where}: execution_provenance does not match a fresh run ({got} vs {out.provenance})")


INTERACTION = {"code_exercise": code_exercise}
