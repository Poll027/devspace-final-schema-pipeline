#!/usr/bin/env python3
"""Live check of Azure deployments: does each reply, do tool calls round-trip, do usage and caching come back, what does a call cost.

    python3 azure_smoke.py [deployment ...]        # default: every name in GEN_LADDER and EVAL_LADDER

Reads AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY from the environment or the repo's .env (never printed). Spends a few cents per deployment.
Exit 1 if any deployment fails a check.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bedrock_llm as BL  # noqa: E402

TOOL = {"tools": [{"toolSpec": {"name": "add", "description": "Add two integers.", "inputSchema": {"json": {
    "type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}, "required": ["a", "b"]}}}}]}
PADDING = "Reference text. " * 400  # >1,024 tokens so the automatic prompt cache can engage on the second call


def check(model, client):
    out = {}
    t = time.time()
    r = client.converse(modelId=model, system=[{"text": "Answer briefly. " + PADDING}], messages=[{"role": "user", "content": [{"text": "Reply with the single word: pong"}]}],
                        inferenceConfig={"maxTokens": 2000})
    text = "".join(b.get("text", "") for b in r["output"]["message"]["content"])
    out["plain"] = ("pong" in text.lower(), f"{time.time() - t:.1f}s, in={r['usage']['inputTokens']} out={r['usage']['outputTokens']} stop={r['stopReason']}")
    BL.log_usage(model, r["usage"], "smoke")
    msgs = [{"role": "user", "content": [{"text": "Use the add tool to compute 17 + 25, then state the result."}]}]
    r = client.converse(modelId=model, messages=msgs, toolConfig=TOOL, inferenceConfig={"maxTokens": 2000})
    use = [b["toolUse"] for b in r["output"]["message"]["content"] if "toolUse" in b]
    ok = r["stopReason"] == "tool_use" and bool(use) and use[0]["name"] == "add"
    out["tool_call"] = (ok, f"stop={r['stopReason']} input={use[0]['input'] if use else None}")
    if ok:
        msgs += [r["output"]["message"], {"role": "user", "content": [{"toolResult": {"toolUseId": use[0]["toolUseId"], "content": [{"text": "42"}]}}]}]
        r2 = client.converse(modelId=model, messages=msgs, toolConfig=TOOL, inferenceConfig={"maxTokens": 2000})
        final = "".join(b.get("text", "") for b in r2["output"]["message"]["content"])
        out["tool_result"] = ("42" in final, final[:60].replace("\n", " "))
    r = client.converse(modelId=model, system=[{"text": "Answer briefly. " + PADDING}], messages=[{"role": "user", "content": [{"text": "Reply with the single word: pong"}]}],
                        inferenceConfig={"maxTokens": 2000})
    out["cache"] = (True, f"cacheRead={r['usage']['cacheReadInputTokens']} of {r['usage']['inputTokens'] + r['usage']['cacheReadInputTokens']} prompt tokens (info only)")
    BL.log_usage(model, r["usage"], "smoke")
    return out


def main():
    BL.load_env()
    client = BL.make_client()
    names = sys.argv[1:] or list(dict.fromkeys(BL.ladder("GEN") + BL.ladder("EVAL")))
    bad = 0
    for m in names:
        print(f"== {m}  (priced at {BL.rates(m)['in']}/{BL.rates(m)['out']} per M tokens)")
        try:
            for k, (ok, note) in check(m, client).items():
                bad += not ok
                print(f"   {'ok  ' if ok else 'FAIL'} {k}: {note}")
        except Exception as e:
            bad += 1
            print(f"   FAIL {type(e).__name__}: {str(e)[:400]}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
