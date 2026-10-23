"""AWS Bedrock plumbing shared by the driver, the agent loop and the supervisor: client, model ladders, pricing, cost log, SNS.
Role-agnostic. Generalised from the glossary pack's glm_generate.py (stage-08 code dropped).

Credentials: default AWS chain only. Region: AWS_REGION / AWS_DEFAULT_REGION (default us-east-1).
Env: GEN_LADDER / EVAL_LADDER (comma lists of model ids), PRICE_GEN / PRICE_EVAL ("in,out" USD per million tokens),
     COST_LOG (set by Budget), QUOTA_STATE, QUOTA_COOLDOWN_H, SNS_TOPIC_ARN.
# ponytail: pricing is by model-name (opus => EVAL rate, else GEN rate); give PRICE_* overrides when ids change.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_LADDERS = {
    "GEN": ["us.anthropic.claude-sonnet-4-6", "us.anthropic.claude-sonnet-4-5-20250929-v1:0", "us.anthropic.claude-haiku-4-5-20251001-v1:0"],
    # evaluators stay Opus-class: when both are out of quota the run waits instead of silently getting a weaker gate
    "EVAL": ["us.anthropic.claude-opus-4-6-v1", "us.anthropic.claude-opus-4-5-20251101-v1:0"],
}
USED, LAST = set(), {}  # models called in this process / the latest call's model and cost
_MEM = {}  # quota block list when no QUOTA_STATE file is configured


def load_env():
    """Read the gitignored .env (KEY=value lines); real env vars win."""
    if (ROOT / ".env").exists():
        for ln in (ROOT / ".env").read_text().splitlines():
            if "=" in ln and not ln.lstrip().startswith("#"):
                k, v = ln.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def make_client():
    import boto3
    from botocore.config import Config
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client("bedrock-runtime", region_name=region,
                        config=Config(retries={"max_attempts": 6, "mode": "standard"}, read_timeout=300, connect_timeout=20))


def price_usd(model, usage):
    role = "EVAL" if "opus" in model.lower() else "GEN"
    pin, pout = (5.0, 25.0) if role == "EVAL" else (3.0, 15.0)
    if os.environ.get(f"PRICE_{role}"):
        pin, pout = (float(x) for x in os.environ[f"PRICE_{role}"].split(","))
    return usage.get("inputTokens", 0) / 1e6 * pin + usage.get("outputTokens", 0) / 1e6 * pout


def log_usage(model, usage, label=""):
    """Append the call's estimated cost to $COST_LOG so every caller's spend is counted. Returns the USD."""
    usd = round(price_usd(model, usage), 4)
    LAST["usd"] = usd
    p = os.environ.get("COST_LOG")
    if p:
        with open(p, "a") as f:
            f.write(json.dumps({"t": datetime.now(timezone.utc).isoformat(timespec="seconds"), "model": model, "label": label or Path(sys.argv[0]).name,
                                "in": usage.get("inputTokens", 0), "out": usage.get("outputTokens", 0), "usd": usd}) + "\n")
    return usd


def ladder(role):
    v = os.environ.get(f"{role}_LADDER")
    return [x.strip() for x in v.split(",") if x.strip()] if v else DEFAULT_LADDERS[role]


def _state():
    p = os.environ.get("QUOTA_STATE")
    if not p:
        return _MEM
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return {}


def _put_state(st):
    p = os.environ.get("QUOTA_STATE")
    if p:
        Path(p + ".tmp").write_text(json.dumps(st))
        os.replace(p + ".tmp", p)


def _block(model, hours):
    st = _state()
    st[model] = time.time() + hours * 3600
    _put_state(st)


def warn(msg):
    print(f"[ladder] {msg}", file=sys.stderr, flush=True)


def sns(subject, body):
    topic = os.environ.get("SNS_TOPIC_ARN")
    if not topic:
        return
    try:
        import boto3
        boto3.client("sns", region_name=topic.split(":")[3]).publish(TopicArn=topic, Subject=subject[:100], Message=body[:20000])
    except Exception as e:
        warn(f"SNS failed: {e}")


def converse_ladder(client, role, label="", **kw):
    """Converse on the first model of the role's ladder that is not quota-blocked. A daily-token-quota error blocks that model for
    QUOTA_COOLDOWN_H hours (default 1); the call moves to the next rung. All blocked: wait and re-probe."""
    announced = False
    while True:
        st, now = _state(), time.time()
        free = [m for m in ladder(role) if st.get(m, 0) <= now]
        if not free:
            wake = min(st.get(m, 0) for m in ladder(role))
            warn(f"all {role} models are out of quota; waiting until {time.strftime('%H:%M', time.localtime(wake))}")
            key = f"__announced_{role}"  # one notification per role per 6h across processes
            if not announced and now - st.get(key, 0) > 6 * 3600:
                announced = True
                st[key] = now
                _put_state(st)
                sns(f"Final pipeline waiting on {role} quota", f"All {role} models are out of daily quota. The run waits and retries automatically.")
            time.sleep(min(max(wake - now, 5), 600))
            continue
        m = free[0]
        try:
            r = client.converse(modelId=m, **kw)
        except Exception as e:
            s = str(e)
            if "per day" in s:
                _block(m, float(os.environ.get("QUOTA_COOLDOWN_H", 1)))
                warn(f"{m}: daily quota hit, falling back")
                continue
            if "not available for this account" in s or "AccessDenied" in type(e).__name__:
                _block(m, 24)
                warn(f"{m}: no access on this account, skipping for 24h")
                continue
            raise
        USED.add(m)
        LAST["model"] = m
        log_usage(m, r["usage"], label)
        return r
