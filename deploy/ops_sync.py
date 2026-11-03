#!/usr/bin/env python3
"""Run on the instance every 5 minutes (deploy/install_ops.sh). Two jobs, no inbound access needed:

 1. PUBLISH: write a status snapshot of every final-pipeline* service to the `ops-status` branch (own clone, ~/ops-status) so a remote agent can read it.
 2. APPLY:   for a service that has STOPPED (systemd 'failed' = the driver exited 2/3) and whose repo has a newer origin/main than the commit it last
             restarted on: `git pull --ff-only` and restart it once. A running service is never touched (in-flight work is kept). The driver's own startup
             selftest is the guard against a bad fix: it stops again and we do not retry the same commit.
Never edits code, never commits to main. Stdlib only.
"""
import json, os, re, subprocess, time
from pathlib import Path

HOME = Path.home()
CLONE = HOME / "ops-status"
STATE = HOME / ".ops_sync_state.json"
REMOTE = os.environ.get("OPS_REMOTE", "https://github.com/Poll027/devspace-final-schema-pipeline")
TAIL, STOP_CHARS = 60, 7000


def sh(*a, cwd=None, ok=False):
    r = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
    if r.returncode and not ok:
        raise RuntimeError(f"{' '.join(a)}: {(r.stdout + r.stderr)[-400:]}")
    return r.stdout.strip()


def services():
    out = sh("systemctl", "list-units", "final-pipeline*", "--all", "--plain", "--no-legend", "--type=service", ok=True)
    return sorted({l.split()[0] for l in out.splitlines() if l.strip() and "-ops" not in l.split()[0]})


def describe(unit):
    props = dict(l.split("=", 1) for l in sh("systemctl", "show", unit, "-p", "ActiveState,SubState,ExecMainStatus,WorkingDirectory,ExecStart,ActiveEnterTimestamp").splitlines() if "=" in l)
    m = re.search(r"batches/([\w.-]+)", props.get("ExecStart", ""))
    repo = Path(props["WorkingDirectory"])
    batch = repo / "batches" / m.group(1) if m else None
    d = {"service": unit, "active": props["ActiveState"], "sub": props["SubState"], "exit_status": props["ExecMainStatus"], "repo": str(repo), "batch": m.group(1) if m else None}
    d["code_commit"] = sh("git", "rev-parse", "--short", "HEAD", cwd=repo, ok=True)
    if batch and (batch / "working").exists():
        w = batch / "working"
        log = w / "driver.log"
        d["log_tail"] = log.read_text(errors="replace").splitlines()[-TAIL:] if log.exists() else []
        d["log_age_min"] = round((time.time() - log.stat().st_mtime) / 60, 1) if log.exists() else None
        stop = w / "DRIVER_STOPPED.md"
        d["stopped"] = stop.read_text(errors="replace")[:STOP_CHARS] if stop.exists() else None
        done = w / "DRIVER_DONE.md"
        d["done"] = done.read_text(errors="replace")[:1500] if done.exists() else None
        fix = w / "proposed_fix.md"
        d["proposed_fix"] = fix.read_text(errors="replace")[:STOP_CHARS] if fix.exists() else None
        cost = w / "cost_log.jsonl"
        try:
            d["spend_usd"] = round(sum(json.loads(l)["usd"] for l in cost.read_text().splitlines() if l.strip()), 2) if cost.exists() else 0.0
        except Exception:
            d["spend_usd"] = None
    return d, repo


def apply_fix(d, repo, state):
    """Restart a stopped service on newer origin/main, once per commit."""
    if d["active"] != "failed":
        return None
    sh("git", "fetch", "-q", "origin", cwd=repo, ok=True)
    new = sh("git", "rev-parse", "--short", "origin/main", cwd=repo, ok=True)
    if not new or state.get(d["service"]) == new:
        return None
    try:
        sh("git", "pull", "--ff-only", "-q", cwd=repo)
    except RuntimeError as ex:
        return f"pull failed, not restarting: {ex}"
    state[d["service"]] = new
    sh("sudo", "systemctl", "restart", d["service"], ok=True)
    return f"pulled {new} and restarted"


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    snap = {"taken_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()), "services": []}
    for unit in services():
        try:
            d, repo = describe(unit)
            d["ops_action"] = apply_fix(d, repo, state)
            snap["services"].append(d)
        except Exception as ex:
            snap["services"].append({"service": unit, "error": str(ex)[:300]})
    STATE.write_text(json.dumps(state))
    if not CLONE.exists():
        sh("git", "clone", "-q", REMOTE, str(CLONE))
    sh("git", "fetch", "-q", "origin", cwd=CLONE, ok=True)
    if sh("git", "ls-remote", "--heads", "origin", "ops-status", cwd=CLONE, ok=True):
        sh("git", "checkout", "-q", "-B", "ops-status", "origin/ops-status", cwd=CLONE)
    else:
        sh("git", "checkout", "-q", "--orphan", "ops-status", cwd=CLONE)
        sh("git", "rm", "-rfq", ".", cwd=CLONE, ok=True)
    (CLONE / "status.json").write_text(json.dumps(snap, indent=1))
    sh("git", "add", "status.json", cwd=CLONE)
    if sh("git", "status", "--porcelain", cwd=CLONE):
        sh("git", "-c", "user.name=ops-sync", "-c", "user.email=ops-sync@localhost", "commit", "-qm", f"status {snap['taken_at']}", cwd=CLONE)
        sh("git", "push", "-q", "--force", "origin", "ops-status", cwd=CLONE, ok=True)  # one-file branch: history is not needed


if __name__ == "__main__":
    main()
