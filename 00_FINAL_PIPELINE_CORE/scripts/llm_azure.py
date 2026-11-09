"""Azure OpenAI / Microsoft Foundry client (Responses API) that speaks the interface the pipeline already uses (Bedrock Converse shape).

The driver, the agent loop and the tests build Converse-style requests (content blocks, toolUse/toolResult, usage keys). This module
translates them to POST /openai/v1/responses and back, so nothing above it changed when Bedrock was replaced. Standard library only.
Why Responses and not chat/completions: GPT-6 deployments reject function tools combined with reasoning on /chat/completions.

    AzureClient().converse(modelId=<deployment name>, system=[{"text":..}], messages=[..], toolConfig={"tools":[..]}, inferenceConfig={"maxTokens":..})
    -> {"output": {"message": {"role": "assistant", "content": [{"text"} | {"toolUse"}], "_items": [raw output items]}},
        "stopReason": "end_turn"|"tool_use"|"max_tokens", "usage": {...}}

The assistant message keeps the raw output items (reasoning included) under "_items"; they are replayed on the next turn so the model keeps its
reasoning across tool calls.
Env: AZURE_OPENAI_ENDPOINT (https://<resource>.services.ai.azure.com or .openai.azure.com; a full URL copied from Foundry is trimmed),
     AZURE_OPENAI_API_KEY, optional REASONING_EFFORT (none|low|medium|high), LLM_TEMPERATURE (not sent unless set), LLM_TIMEOUT_S (default 600).
Errors are classed by exception name so bedrock_agent.transient() retries the right ones: ThrottlingError (429), ServiceUnavailableError (5xx),
ConnectionError/TimeoutError (network); LLMError (everything else, never retried). Prompt caching is automatic: cachePoint blocks are dropped and
cached prompt tokens come back as cacheReadInputTokens.
# ponytail: no streaming; an optional parameter a deployment rejects (400 with error.param) is dropped and remembered for that deployment.
"""
import http.client
import json
import os
import urllib.error
import urllib.request


class LLMError(Exception):
    status, param = 0, None


class ThrottlingError(LLMError):
    pass


class ServiceUnavailableError(LLMError):
    pass


OPTIONAL = {"temperature", "reasoning", "top_p"}  # request keys a deployment may refuse; error.param may be "reasoning.effort"
_DROP = {}  # deployment -> optional request keys it rejected


def base_url():
    ep = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    if not ep:
        raise LLMError("AZURE_OPENAI_ENDPOINT is not set (copy .env.example to .env)")
    return ep.split("/openai")[0] + "/openai/v1"  # accepts the bare host or a full URL copied from Foundry (.../openai/v1/responses)


def to_responses(model, system, messages, toolConfig, inferenceConfig):
    items = []
    for m in messages:
        blocks = [b for b in m["content"] if "cachePoint" not in b]
        if m["role"] == "assistant":
            if m.get("_items"):  # replay exactly what the model produced (reasoning, text, function calls)
                items += m["_items"]
                continue
            text = "".join(b.get("text", "") for b in blocks)
            if text:
                items.append({"role": "assistant", "content": text})
            items += [{"type": "function_call", "call_id": b["toolUse"]["toolUseId"], "name": b["toolUse"]["name"], "arguments": json.dumps(b["toolUse"]["input"])}
                      for b in blocks if "toolUse" in b]
            continue
        for b in blocks:
            if "toolResult" in b:
                tr = b["toolResult"]
                items.append({"type": "function_call_output", "call_id": tr["toolUseId"], "output": "".join(c.get("text", "") for c in tr["content"])})
        text = "\n\n".join(b["text"] for b in blocks if "text" in b)
        if text:
            items.append({"role": "user", "content": text})
    body = {"model": model, "input": items, "max_output_tokens": (inferenceConfig or {}).get("maxTokens", 16000)}
    instructions = "\n\n".join(b["text"] for b in system or [] if "text" in b)
    if instructions:
        body["instructions"] = instructions
    tools = [t["toolSpec"] for t in (toolConfig or {}).get("tools", []) if "toolSpec" in t]
    if tools:
        body["tools"] = [{"type": "function", "name": t["name"], "description": t.get("description", ""), "parameters": t["inputSchema"]["json"]} for t in tools]
    if os.environ.get("REASONING_EFFORT"):
        body["reasoning"] = {"effort": os.environ["REASONING_EFFORT"]}
    if os.environ.get("LLM_TEMPERATURE"):
        body["temperature"] = float(os.environ["LLM_TEMPERATURE"])
    return body


def from_responses(r):
    content, items = [], []
    for it in r.get("output") or []:
        items.append(it)
        if it.get("type") == "message":
            text = "".join(c.get("text", "") for c in it.get("content", []) if c.get("type") == "output_text")
            if text:
                content.append({"text": text})
        elif it.get("type") == "function_call":
            raw = it.get("arguments") or "{}"
            try:
                args = json.loads(raw)
            except ValueError:
                args = {"_malformed_arguments": raw[:500]}  # the tool errors back to the model, which retries
            content.append({"toolUse": {"toolUseId": it["call_id"], "name": it["name"], "input": args}})
    u = r.get("usage") or {}
    cached = (u.get("input_tokens_details") or {}).get("cached_tokens", 0)
    if any("toolUse" in b for b in content):
        stop = "tool_use"
    elif r.get("status") == "incomplete" and (r.get("incomplete_details") or {}).get("reason") == "max_output_tokens":
        stop = "max_tokens"
    elif r.get("status") == "incomplete":
        stop = "content_filtered"
    else:
        stop = "end_turn"
    return {"output": {"message": {"role": "assistant", "content": content, "_items": items}}, "stopReason": stop,
            "usage": {"inputTokens": u.get("input_tokens", 0) - cached, "cacheReadInputTokens": cached, "cacheWriteInputTokens": 0,
                      "outputTokens": u.get("output_tokens", 0)}}  # output_tokens already include reasoning tokens (billed as output)


def _error(status, text, retry_after=None):
    msg = f"HTTP {status}: {text[:600]}" + (f" (retry-after {retry_after}s)" if retry_after else "")
    e = (ThrottlingError if status == 429 else ServiceUnavailableError if status >= 500 or status == 408 else LLMError)(msg)
    e.status = status
    try:
        e.param = json.loads(text)["error"].get("param")
    except (ValueError, KeyError, AttributeError, TypeError):
        pass
    return e


def _post(body):
    req = urllib.request.Request(base_url() + "/responses", json.dumps(body).encode(),
                                 {"Content-Type": "application/json", "api-key": os.environ.get("AZURE_OPENAI_API_KEY", "")})
    try:
        with urllib.request.urlopen(req, timeout=float(os.environ.get("LLM_TIMEOUT_S", 600))) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise _error(e.code, e.read().decode(errors="replace"), e.headers.get("retry-after"))
    except (urllib.error.URLError, http.client.HTTPException, OSError) as e:  # dropped connection, DNS, timeout
        raise ConnectionError(f"{type(e).__name__}: {e}")


class AzureClient:
    def converse(self, modelId, system=None, messages=(), toolConfig=None, inferenceConfig=None, **_):
        body = to_responses(modelId, system, messages, toolConfig, inferenceConfig)
        for _ in range(4):
            for p in _DROP.get(modelId, ()):
                body.pop(p, None)
            try:
                return from_responses(_post(body))
            except LLMError as e:
                key = (e.param or "").split(".")[0]
                if e.status == 400 and key in OPTIONAL and key in body:
                    _DROP.setdefault(modelId, set()).add(key)
                    continue
                raise
        raise LLMError(f"{modelId}: request kept failing on optional parameters")
