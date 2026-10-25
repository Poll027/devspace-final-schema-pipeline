#!/usr/bin/env python3
"""Offline test of run_pipeline.py: the model is stubbed (no AWS, no spend), the scripts and gates are real.

    python3 test_driver.py batches/<a PASSing batch>      # its content is the stub generator's "answer"

Scenarios: happy path with a blocking round + advisories (gate always runs before an evaluator, stage skip on rerun),
a corrupt first draft (gate failure is repaired without an evaluator call), the same blocker twice (stops), the spend cap.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_pipeline as rp  # noqa: E402
from bedrock_agent import BudgetExceeded  # noqa: E402
from finlib import ROOT, load, save  # noqa: E402

GOLD = Path(sys.argv[1]).resolve()
EVAL_ONLY = {"08_pedagogy_review": ("pedagogy_review.md", "# review\n"), "09_leakage_check": ("leakage_report.json", '{"issues": []}'),
             "11_final_audit": ("final_audit_report.json", '{"verdict": "PASS", "issues": []}')}


def make_batch(name):
    B = ROOT / "batches" / name
    shutil.rmtree(B, ignore_errors=True)
    B.mkdir(parents=True)
    ctx = load(GOLD / "batch_run_context.json")
    save(B / "run_config.json", {"path_id": ctx["path_id"], "glossary_bundle": str(GOLD / "inputs" / "path_glossary_bundle.json"),
                                 "glossary_batch_id": ctx["glossary_batch_id"], "toc_workspace": ctx["toc_workspace"], "tiles": ctx["tile_ids"]})
    return B


class Stub:
    """Plays generator and evaluator. script[(sid, role)] is a list of replies consumed in order; default = gold artifact / PASS."""

    def __init__(self, B, evals=None, corrupt_first=False):
        self.B, self.evals, self.corrupt_first = B, evals or {}, corrupt_first
        self.calls = []

    def __call__(self, ctx, role, task, label):
        sid = label.split(":")[0]
        self.calls.append((label, sid))
        if role == "GEN":
            if label.endswith(":gen"):
                art = ctx.artifact(sid)
                doc = json.loads((GOLD / art).read_text().replace(GOLD.name, self.B.name))
                if self.corrupt_first and sid == "03_screens":
                    doc["tiles"] = []  # breaks tile coverage
                    self.corrupt_first = False
                save(ctx.part(sid, "all"), doc)
            elif label.endswith(":gatefix"):
                art = ctx.artifact(sid)
                save(ctx.part(sid, "all"), json.loads((GOLD / art).read_text().replace(GOLD.name, self.B.name)))
            return "ok"
        if sid in EVAL_ONLY:
            name, body = EVAL_ONLY[sid]
            (self.B / name).write_text(body)
            return "reviewed\nVERDICT: PASS"
        q = self.evals.get(sid, [])
        return q.pop(0) if q else "VERDICT: PASS"


def run(B, stub, cap=25):
    rp.Ctx.agent = lambda self, role, task, label, tiles=1: stub(self, role, task, label)
    sys.argv = ["run_pipeline.py", str(B), "--max-usd", str(cap)]
    try:
        rp.main()
        return 0
    except SystemExit as e:
        return e.code


def retry_test():
    """A dropped connection is retried with backoff and the call still succeeds; a non-transient error is not retried."""
    import bedrock_agent as BA
    from botocore.exceptions import ConnectionClosedError

    class Fake:
        def __init__(self, errs): self.errs, self.n = errs, 0

        def converse(self, **kw):
            self.n += 1
            if self.errs:
                raise self.errs.pop(0)
            return {"usage": {"inputTokens": 1, "outputTokens": 1}, "stopReason": "end_turn", "output": {"message": {"role": "assistant", "content": [{"text": "done"}]}}}
    keep = BA.make_client
    import time
    real_sleep = time.sleep
    time.sleep = lambda s: None
    try:
        f = Fake([ConnectionClosedError(error=Exception("x"), request=None, endpoint_url="u")] * 2)
        BA.make_client = lambda: f
        b = BA.Budget(5, Path(tempfile.mkdtemp()) / "c.jsonl")
        assert BA.run_agent("us.anthropic.claude-sonnet-4-6", "s", "t", b) == "done" and f.n == 3, f.n
        f2 = Fake([ValueError("not transient")])
        BA.make_client = lambda: f2
        try:
            BA.run_agent("us.anthropic.claude-sonnet-4-6", "s", "t", b)
            raise AssertionError("non-transient error was swallowed")
        except ValueError:
            assert f2.n == 1
    finally:
        BA.make_client, time.sleep = keep, real_sleep
    return "connection-retry OK"


def cache_test():
    """Each call carries at most 4 cache checkpoints, exactly one on the newest message; reads/writes are priced at 0.1x/1.25x."""
    import bedrock_agent as BA
    import bedrock_llm as BL

    class Fake:
        def __init__(self): self.calls = []

        def converse(self, **kw):
            self.calls.append(json.loads(json.dumps(kw)))
            n = len(self.calls)
            if n < 4:
                m = {"role": "assistant", "content": [{"toolUse": {"toolUseId": f"t{n}", "name": "bash", "input": {"command": "echo hi"}}}]}
                return {"usage": {"inputTokens": 10, "outputTokens": 5, "cacheReadInputTokens": 1000, "cacheWriteInputTokens": 100}, "stopReason": "tool_use", "output": {"message": m}}
            return {"usage": {"inputTokens": 10, "outputTokens": 5}, "stopReason": "end_turn", "output": {"message": {"role": "assistant", "content": [{"text": "done"}]}}}
    keep, f = BA.make_client, Fake()
    BA.make_client = lambda: f
    try:
        b = BA.Budget(5, Path(tempfile.mkdtemp()) / "c.jsonl")
        assert BA.run_agent("us.anthropic.claude-sonnet-4-6", "sys", "task", b) == "done"
    finally:
        BA.make_client = keep
    for kw in f.calls:
        pts = sum("cachePoint" in x for x in kw["system"]) + sum("cachePoint" in x for x in kw["toolConfig"]["tools"]) \
            + sum("cachePoint" in x for m in kw["messages"] for x in m["content"])
        last = sum("cachePoint" in x for x in kw["messages"][-1]["content"])
        assert pts == 3 and last == 1, (pts, last)
    u = {"inputTokens": 1_000_000, "cacheReadInputTokens": 1_000_000, "cacheWriteInputTokens": 1_000_000, "outputTokens": 0}
    assert abs(BL.price_usd("us.anthropic.claude-sonnet-4-6", u) - 3.0 * (1 + 0.1 + 1.25)) < 1e-9
    return "prompt-cache checkpoints + pricing OK"


def main():
    out = [retry_test(), cache_test()]
    # 1. happy path
    B = make_batch("_drvtest_a")
    s = Stub(B, evals={"03_screens": ["BLOCKING t/s01: wrong\nVERDICT: FAIL", "ADVISORY t/s02: reword\nVERDICT: PASS"],
                       "04_interactions": ["VERDICT: PASS"]})
    code = run(B, s)
    labels = [l for l, _ in s.calls]
    assert code == 0, (code, (B / "working" / "DRIVER_STOPPED.md").read_text() if (B / "working" / "DRIVER_STOPPED.md").exists() else "")
    assert labels.index("03_screens:all:gen") < labels.index("03_screens:all:eval"), "evaluator before generator"
    assert labels.count("03_screens:all:eval") == 2 and labels.count("03_screens:all:repair") == 2, labels  # blocker repair + advisory repair, no 3rd eval
    gates = {g["stage_id"]: g["verdict"] for g in load(B / "final_stage_gate_ledger.json")["gates"]}
    assert all(v == "PASS" for v in gates.values()) and "11_final_audit" in gates and "05_code_exercises" not in gates, gates
    n = len(s.calls)
    assert run(B, s) == 0 and len(s.calls) == n, "rerun must skip gated stages"
    out.append("happy path + resume OK")
    # 2. corrupt first draft: gate failure repaired, evaluator never sees it
    B = make_batch("_drvtest_b")
    s = Stub(B, corrupt_first=True)
    assert run(B, s) == 0
    labels = [l for l, _ in s.calls]
    assert labels.index("03_screens:all:gatefix") < labels.index("03_screens:all:eval"), labels
    out.append("gate-before-evaluator OK")
    # 3. same blocker twice
    B = make_batch("_drvtest_c")
    s = Stub(B, evals={"03_screens": ["BLOCKING t/s01: wrong\nVERDICT: FAIL"] * 3})
    assert run(B, s) == 2 and "unchanged" in (B / "working" / "DRIVER_STOPPED.md").read_text()
    out.append("repeat-blocker stop OK")
    # 4. spend cap
    B = make_batch("_drvtest_d")
    s = Stub(B)
    inner = s.__call__

    def costly(ctx, role, task, label):
        (B / "working").mkdir(exist_ok=True)
        with open(B / "working" / "cost_log.jsonl", "a") as f:
            f.write(json.dumps({"t": "2999-01-01T00:00:00", "model": "x", "label": label, "in": 0, "out": 0, "usd": 20}) + "\n")
        return inner(ctx, role, task, label)
    assert run(B, costly, cap=25) == 3
    out.append("spend cap stop OK")
    for n in "abcd":
        shutil.rmtree(ROOT / "batches" / f"_drvtest_{n}", ignore_errors=True)
    print("\n".join(out))


if __name__ == "__main__":
    main()
