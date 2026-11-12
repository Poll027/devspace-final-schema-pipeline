#!/usr/bin/env python3
"""Offline test of run_pipeline.py: the model is stubbed (no network, no spend), the scripts and gates are real.

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

    def __init__(self, B, evals=None, corrupt_first=False, block=None):
        self.B, self.evals, self.corrupt_first = B, evals or {}, corrupt_first
        self.block = dict(block or {})  # evaluator-only stage id -> how many times to report a blocking finding first
        self.calls, self.llm_calls = [], []

    def llm(self, ctx, system, blocks, label):
        """The tool-free packet evaluator call (Ctx.llm): recorded, then answered like any evaluator."""
        self.llm_calls.append((label, system, blocks))
        return self(ctx, "EVAL", blocks[-1]["text"], label)

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
        if sid in EVAL_ONLY and self.block.get(sid, 0) > 0:
            self.block[sid] -= 1
            name, _ = EVAL_ONLY[sid]
            tile = "tile_data_shape_and_types" if not getattr(self, "no_tile", False) else "the batch"
            (self.B / name).write_text(f"# review\n| BLOCKING    | 0     |\n**BLOCKING defects: 0**\n| BLOCKING | {tile}/s01 | x |\n- BLOCKING {tile}/s01: a fact in the lesson is wrong -> fix it\n")
            return f"reviewed\n- BLOCKING {tile}/s01: a fact in the lesson is wrong -> fix it\nVERDICT: FAIL"
        if sid in EVAL_ONLY:
            name, body = EVAL_ONLY[sid]
            (self.B / name).write_text(body)
            return "reviewed\nVERDICT: PASS"
        q = self.evals.get(sid, [])
        return q.pop(0) if q else "VERDICT: PASS"


def run(B, stub, cap=25):
    rp.Ctx.agent = lambda self, role, task, label, tiles=1: stub(self, role, task, label)
    rp.Ctx.llm = lambda self, system, blocks, label: stub.llm(self, system, blocks, label)
    sys.argv = ["run_pipeline.py", str(B), "--max-usd", str(cap), "--allow-dirty-code"]
    try:
        rp.main()
        return 0
    except SystemExit as e:
        return e.code


def retry_test():
    """A dropped connection is retried with backoff and the call still succeeds; a non-transient error is not retried."""
    import bedrock_agent as BA

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
        f = Fake([ConnectionError("connection dropped")] * 2)
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


def protect_test():
    """write_file refuses gated artifacts and the ledger, but still lets an agent write its own stage's file."""
    import bedrock_agent as BA
    d = Path(tempfile.mkdtemp())
    (d / "inputs").mkdir()
    prot = [d / "batch_run_context.json", d / "inputs"]
    for name in ("batch_run_context.json", "inputs/x.json"):
        r = BA.run_tool("write_file", {"path": str(d / name), "content": "{}"}, [d], prot)
        assert r.startswith("ERROR") and not (d / name).exists(), (name, r)
    r = BA.run_tool("write_file", {"path": str(d / "screens.json"), "content": "{}"}, [d], prot)
    assert r.startswith("wrote") and (d / "screens.json").exists(), r
    return "write-protection OK"


def guard_test():
    """An agent that edits a schema, adds a file to the pipeline code, or deletes an instruction is caught, undone and stopped."""
    class A:
        max_usd, allow_dirty_code = 1, True
    B = Path(tempfile.mkdtemp())
    c = rp.Ctx(B, A())
    c.guard_snapshot()
    schema = ROOT / "00_FINAL_PIPELINE_CORE" / "schemas" / "ix.code_exercise.schema.json"
    orig = schema.read_bytes()
    stray = ROOT / "01_FINAL_PACK_TEMPLATE" / "_guard_test_stray.md"
    try:
        schema.write_bytes(orig.replace(b'"forbidden_syntax"', b'"forbidden_syntax", "required_syntax"'))  # the batch-005 trick: widen the gate
        stray.write_text("x")
        try:
            c.guard_check("test")
            raise AssertionError("guard did not stop an edit of pipeline code")
        except rp.Stuck as e:
            assert "ix.code_exercise.schema.json" in str(e) and "_guard_test_stray.md" in str(e), str(e)
        assert schema.read_bytes() == orig and not stray.exists(), "guard did not restore the files"
        c.guard_check("clean")  # unchanged code passes
    finally:
        schema.write_bytes(orig)
        stray.unlink(missing_ok=True)
    c.args.allow_dirty_code = False  # the startup check: uncommitted edits to pipeline code refuse to run
    probe = ROOT / "01_FINAL_PACK_TEMPLATE" / "_guard_test_dirty.md"
    probe.write_text("x")
    try:
        c.guard_snapshot()
        raise AssertionError("startup did not refuse uncommitted pipeline code")
    except rp.Stuck as e:
        assert "differs from the committed version" in str(e)
    finally:
        probe.unlink(missing_ok=True)
    return "agent-edit guard OK"


def reopen_test():
    """Blocking findings from stage 08 are routed back to stages 03/04 for the tiles they name, the downstream stages are redone, and the review is
    rerun; persistent findings stop after MAX_REOPENS loops; findings that name no tile stop at once."""
    B = make_batch("_drvtest_g")
    s = Stub(B, block={"08_pedagogy_review": 1})
    assert run(B, s) == 0, (B / "working" / "DRIVER_STOPPED.md").read_text()
    labels = [l for l, _ in s.calls]
    i = labels.index("08_pedagogy_review:eval")
    after = labels[i + 1:]
    assert after[:2] == ["03_screens:all:repair", "04_interactions:all:repair"], after
    assert after.count("08_pedagogy_review:eval") == 1 and labels.count("08_pedagogy_review:eval") == 2, labels
    assert all(g["verdict"] == "PASS" for g in load(B / "final_stage_gate_ledger.json")["gates"]) and (B / "pedagogy_review.md").exists()
    assert "06_assemble" in {g["stage_id"] for g in load(B / "final_stage_gate_ledger.json")["gates"]}
    B = make_batch("_drvtest_h")
    s = Stub(B, block={"08_pedagogy_review": 9})
    assert run(B, s) == 2
    msg = (B / "working" / "DRIVER_STOPPED.md").read_text()
    assert "after 2 automatic repair loops" in msg and [l for l, _ in s.calls].count("03_screens:all:repair") == 2, msg
    B = make_batch("_drvtest_i")
    s = Stub(B, block={"08_pedagogy_review": 1})
    s.no_tile = True
    assert run(B, s) == 2 and "name no tile" in (B / "working" / "DRIVER_STOPPED.md").read_text()
    # a run that stopped on findings leaves the report on disk: the next run repairs from it without re-running the review first
    B = make_batch("_drvtest_j")
    assert run(B, Stub(B, block={"08_pedagogy_review": 9})) == 2
    s = Stub(B)
    assert run(B, s) == 0, (B / "working" / "DRIVER_STOPPED.md").read_text()
    labels = [l for l, _ in s.calls]
    assert labels.index("03_screens:all:repair") < labels.index("08_pedagogy_review:eval") and labels.count("08_pedagogy_review:eval") == 1, labels
    return "automatic repair loop OK"


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


def azure_test():
    """The Azure client turns a Converse-shaped tool loop into Responses-API requests and back: instructions + input items (user, replayed reasoning and
    function call, function output), no cachePoint, cached prompt tokens priced as cache reads, a 429 retried by the agent loop, a rejected optional
    parameter dropped once and remembered, and an unpriced deployment costed at the dearest rate."""
    import os
    import time
    import bedrock_agent as BA
    import bedrock_llm as BL
    import llm_azure as AZ
    sent, replies = [], []

    def post(body):
        sent.append(json.loads(json.dumps(body)))
        r = replies.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    def msg(text=None, calls=False, u=(100, 0, 10)):
        out = [{"type": "reasoning", "id": "rs_1", "summary": []}] if calls else []
        if text:
            out.append({"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text}]})
        if calls:
            out.append({"type": "function_call", "call_id": "call_1", "name": "bash", "arguments": json.dumps({"command": "echo hi"})})
        return {"status": "completed", "output": out, "usage": {"input_tokens": u[0], "output_tokens": u[2], "input_tokens_details": {"cached_tokens": u[1]}}}
    keep, keep_ep = (AZ._post, BA.make_client, time.sleep, os.environ.get("REASONING_EFFORT")), os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    AZ._post, BA.make_client, time.sleep = post, lambda: AZ.AzureClient(), lambda s: None
    os.environ.pop("REASONING_EFFORT", None)
    try:
        replies[:] = [AZ._error(429, "{}", "7"), msg(calls=True, u=(1000, 800, 50)), msg("done")]
        b = BA.Budget(5, Path(tempfile.mkdtemp()) / "c.jsonl")
        assert BA.run_agent("gpt-6.1-sol", "sys", "task", b) == "done" and len(sent) == 3, len(sent)
        assert "cachePoint" not in json.dumps(sent) and sent[0] == sent[1], "429 must be retried unchanged, with caching markers stripped"
        req = sent[2]
        assert req["instructions"] == "sys" and "temperature" not in req and req["max_output_tokens"] > 0
        kinds = [x.get("type") or x["role"] for x in req["input"]]
        assert kinds == ["user", "reasoning", "function_call", "function_call_output"], kinds  # reasoning is replayed between tool calls
        assert req["input"][2]["call_id"] == req["input"][3]["call_id"] == "call_1"
        assert {t["name"] for t in req["tools"]} == {"read_file", "write_file", "bash"} and all(t["type"] == "function" for t in req["tools"])
        u = AZ.from_responses(msg(calls=True, u=(1000, 800, 50)))["usage"]
        assert u == {"inputTokens": 200, "cacheReadInputTokens": 800, "cacheWriteInputTokens": 0, "outputTokens": 50, "serviceTier": "default"}, u
        assert abs(b.spent() - BL.price_usd("gpt-6.1-sol", u)) < 1e-3 and b.spent() > 0
        cut = msg("partial")
        cut.update(status="incomplete", incomplete_details={"reason": "max_output_tokens"})
        assert AZ.from_responses(cut)["stopReason"] == "max_tokens"
        # an optional parameter the deployment rejects is dropped, retried, and never sent again
        os.environ["REASONING_EFFORT"] = "high"
        sent.clear()
        replies[:] = [AZ._error(400, json.dumps({"error": {"param": "reasoning.effort", "code": "unsupported_value"}})), msg("a"), msg("b")]
        c = AZ.AzureClient()
        kw = dict(system=[{"text": "s"}], messages=[{"role": "user", "content": [{"text": "hi"}]}])
        assert c.converse(modelId="gpt-x", **kw)["stopReason"] == "end_turn" and c.converse(modelId="gpt-x", **kw)
        assert "reasoning" in sent[0] and "reasoning" not in sent[1] and "reasoning" not in sent[2], sent
        # a hard error is raised, never retried
        replies[:] = [AZ._error(400, json.dumps({"error": {"param": "input"}}))]
        try:
            c.converse(modelId="gpt-y", **kw)
            raise AssertionError("a 400 on a required field must raise")
        except AZ.LLMError:
            assert not BA.transient(AZ.LLMError("HTTP 400"))
        # a deployment that has no Flex tier: the request is retried without service_tier and never sent with it again
        os.environ["LLM_SERVICE_TIER"] = "flex"
        sent.clear()
        replies[:] = [AZ._error(400, json.dumps({"error": {"code": "service_tier_not_supported", "param": None}})), msg("a"), msg("b")]
        assert c.converse(modelId="gpt-noflex", **kw)["stopReason"] == "end_turn" and c.converse(modelId="gpt-noflex", **kw)
        assert "service_tier" in sent[0] and "service_tier" not in sent[1] and "service_tier" not in sent[2], sent
        os.environ.pop("LLM_SERVICE_TIER", None)
        assert BA.transient(AZ._error(503, "x")) and BA.transient(AZ._error(429, "x")) and not BA.transient(AZ._error(404, "DeploymentNotFound"))
        assert BL.price_usd("mystery-model", {"inputTokens": 1_000_000}) == 10.0, "unpriced deployments must cost the dearest rate"
        os.environ["AZURE_OPENAI_ENDPOINT"] = "https://r.services.ai.azure.com/openai/v1/responses"
        assert AZ.base_url() == "https://r.services.ai.azure.com/openai/v1", "a full URL copied from Foundry must be trimmed to the base"
        os.environ["AZURE_OPENAI_ENDPOINT"] = keep_ep
    finally:
        AZ._post, BA.make_client, time.sleep = keep[:3]
        AZ._DROP.clear()
        os.environ.pop("REASONING_EFFORT", None)
        if keep[3]:
            os.environ["REASONING_EFFORT"] = keep[3]
    return "azure translation + retry + pricing OK"


def sheet_gate_test():
    """A formula practice with no syntax list (spreadsheet glossary anchors have no live_code) gets one explicit message, not an 'untaught' error per operator."""
    sys.path.insert(0, str(Path(__file__).resolve().parent / "checkers"))
    import sheetsyntax as SH
    sol = "H1: 0.075\nE2: =D2*$H$1\nE3: =D3*$H$1\n"
    v, _, _ = SH.judge(sol, [], [])
    assert len(v) == 1 and "constraints.allowed_syntax is empty" in v[0] and "op_mul" in v[0] and "ref_abs" in v[0], v
    assert SH.judge(sol, ["+ - * /", "relative cell references", "absolute references ($A$1)"], ["SUM", "IF"])[0] == []
    assert "not yet taught" in SH.judge(sol, ["+ - * /"], [])[0][0], "a non-empty list that lacks something keeps the old message"
    assert SH.judge("A1: 5\n", [], [])[0] == [], "no formulas, nothing to judge"
    return "empty-syntax-list message OK"


def stall_test():
    """MAX_STALLS lets the same blocker repeat before the run stops (default 1 keeps the old stop at the first repeat); MAX_ROUNDS caps the rounds."""
    keep = (rp.MAX_STALLS, rp.MAX_ROUNDS)
    try:
        B = make_batch("_drvtest_h")
        s = Stub(B, evals={"03_screens": ["BLOCKING t/s01: wrong\nVERDICT: FAIL"] * 3 + ["VERDICT: PASS"], "04_interactions": ["VERDICT: PASS"]})
        rp.MAX_STALLS, rp.MAX_ROUNDS = 3, 5
        assert run(B, s) == 0, (B / "working" / "DRIVER_STOPPED.md").read_text()
        assert [l for l, _ in s.calls].count("03_screens:all:eval") == 4
        B = make_batch("_drvtest_i")
        rp.MAX_STALLS, rp.MAX_ROUNDS = 3, 5
        s = Stub(B, evals={"03_screens": ["BLOCKING t/s01: wrong\nVERDICT: FAIL"] * 6})
        assert run(B, s) == 2 and "unchanged after 3 repair" in (B / "working" / "DRIVER_STOPPED.md").read_text()
    finally:
        rp.MAX_STALLS, rp.MAX_ROUNDS = keep
    return "stall + round limits OK"


def packet_test():
    """Stages 03/04 are judged from one tool-free call over the rendered packet; a reply without a verdict falls back to the agent evaluator;
    --eval-mode agent never uses the packet."""
    B = make_batch("_drvtest_e")
    s = Stub(B, evals={"03_screens": ["BLOCKING t/s01: wrong\nVERDICT: FAIL", "VERDICT: PASS"]})
    assert run(B, s) == 0
    got = {}
    for label, system, blocks in s.llm_calls:
        got.setdefault(label, []).append((system, blocks))
    assert set(got) == {"03_screens:all:eval", "04_interactions:all:eval"}, set(got)
    assert len(got["03_screens:all:eval"]) == 2, "blocker round + scoped re-eval, both through the packet"
    system, blocks = got["04_interactions:all:eval"][0]
    assert "EVALUATOR PACKET" in blocks[0]["text"] and "SOURCE FACTS" in blocks[0]["text"] and "KEY" in blocks[0]["text"] and "taught-before-tested" in blocks[0]["text"], blocks[0]["text"][:300]
    assert "EVALUATION BY PACKET" in system and "04 interactions" in system, system[:200]
    assert "SCOPED re-evaluation" in got["03_screens:all:eval"][1][1][-1]["text"] and "SCOPED" not in blocks[-1]["text"]
    assert (B / "working" / "packet_04_interactions_all.md").exists()
    # no verdict from the packet call -> exactly one agent evaluator call as fallback
    B = make_batch("_drvtest_f")

    class NoVerdict(Stub):
        def llm(self, ctx, system, blocks, label):
            self.llm_calls.append((label, system, blocks))
            return "NEED: the registry"
    s = NoVerdict(B)
    assert run(B, s) == 0
    assert [l for l, _ in s.calls].count("03_screens:all:eval") == 1 and len(s.llm_calls) == 2, (s.calls, len(s.llm_calls))
    # agent mode: no packet call at all
    B = make_batch("_drvtest_g")
    s = Stub(B)
    rp.sys.argv = ["x"]
    import os
    os.environ["EVAL_MODE"] = "agent"
    try:
        assert run(B, s) == 0 and not s.llm_calls
    finally:
        del os.environ["EVAL_MODE"]
    return "packet evaluator + fallback + agent mode OK"


def main():
    out = [retry_test(), cache_test(), azure_test(), protect_test(), guard_test(), sheet_gate_test(), stall_test(), packet_test(), reopen_test()]
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
    for n in "abcdefghij":
        shutil.rmtree(ROOT / "batches" / f"_drvtest_{n}", ignore_errors=True)
    print("\n".join(out))


if __name__ == "__main__":
    main()
