#!/usr/bin/env python3
"""Move every role through TOC -> glossary -> final schema on its own. Run on the VM by a systemd timer every 3 minutes (deploy/install_chain.sh).
Stateless and idempotent: each run looks at the disk and starts whatever is now ready. Never touches a running or finished service.

Layout per role R under ~/roles/R/:  toc/ (universal-toc-pipeline), glossary/ (devspace-glossary-pipeline), final/ (this repo), final_runs/<batch>/ (one clone per final batch).
 1. TOC frozen (freeze_manifest.json + working/DRIVER_DONE.md)  -> create glossary batch + systemd service `glossary-R`.
 2. glossary bundle exists (batches/<id>/path_glossary_bundle.*.json)  -> one final batch per TOC region (split above MAX_TILES tiles), each its own clone and
    service `final-pipeline-R-<region>`; at most MAX_PAR_FINAL running per role.
Services stay stopped on a human decision or after the supervisor gives up; the hourly ops routine and ops_sync handle fixes and restarts.
Env: ROLES (comma list, default every folder under ~/roles), MAX_PAR_FINAL (default 6), MAX_TILES (12), GLOSSARY_MAX_USD (80), FINAL_MAX_USD (25).
# ponytail: no database, the disk is the state. A region whose batch folder exists is never recreated.
"""
import json, os, re, shutil, subprocess, sys
from pathlib import Path

HOME = Path.home()
ROLES = HOME / "roles"
MAX_PAR = int(os.environ.get("MAX_PAR_FINAL", 6))
MAX_TILES = int(os.environ.get("MAX_TILES", 12))
ENV_LINES = {"GEN_LADDER": "gpt-6.1-sol", "EVAL_LADDER": "gpt-6.1-sol", "LLM_SERVICE_TIER": "flex", "CHUNK_WORKERS": "2", "MAX_ROUNDS": "5", "MAX_STALLS": "3"}


def sh(*a, cwd=None, ok=True):
    r = subprocess.run(list(a), cwd=cwd, capture_output=True, text=True)
    if r.returncode and not ok:
        raise RuntimeError(f"{' '.join(a)}: {(r.stdout + r.stderr)[-300:]}")
    return r.stdout.strip()


def load(p):
    return json.loads(Path(p).read_text())


def unit_state(name):
    return sh("systemctl", "is-active", name) or "unknown"


def unit_exists(name):
    return Path(f"/etc/systemd/system/{name}.service").exists()


def install_unit(name, repo, cmd, max_usd, desc):
    env = {**ENV_LINES, "MAX_USD": str(max_usd), "SUPERVISED": "1"}
    Path(f"/tmp/{name}.env").write_text("".join(f"{k}={v}\n" for k, v in env.items()))
    sh("sudo", "cp", f"/tmp/{name}.env", f"/etc/{name}.env")
    unit = f"""[Unit]
Description={desc}
After=network-online.target
[Service]
User={os.environ.get('USER', 'azureuser')}
WorkingDirectory={repo}
EnvironmentFile=/etc/{name}.env
ExecStart={HOME}/env/bin/python {cmd}
Restart=on-failure
RestartSec=60
RestartPreventExitStatus=2 3
[Install]
WantedBy=multi-user.target
"""
    Path(f"/tmp/{name}.service").write_text(unit)
    sh("sudo", "cp", f"/tmp/{name}.service", f"/etc/systemd/system/{name}.service")
    sh("sudo", "systemctl", "daemon-reload")
    sh("sudo", "systemctl", "enable", "--now", name)


def toc_frozen(role):
    ws = ROLES / role / "toc" / f"04_{role}_OUTPUT_WORKSPACE"
    return ws if (ws / "freeze_manifest.json").exists() and (ws / "working" / "DRIVER_DONE.md").exists() else None


def glossary_step(role, ws):
    g = ROLES / role / "glossary"
    bid = f"glossary_batch_{role}"
    B = g / "batches" / bid
    bundles = list(B.glob("path_glossary_bundle.*.json"))
    if bundles:
        return bundles[0], bid
    svc = f"glossary-{role}"
    if not unit_exists(svc):
        B.mkdir(parents=True, exist_ok=True)
        n = len(load(ws / "resolved_concept_inventory.json").get("resolved_concepts", []))
        (B / "batch_run_context.json").write_text(json.dumps({
            "batch_id": bid, "opened_at": sh("date", "+%F"), "rollout_phase": "2_per_role", "career_family_id": role,
            "paths": [{"path_id": role, "toc_workspace": str(ws)}],
            "expected_concept_volume": {"estimate": n, "reasoning": f"resolved_concept_inventory.json lists {n} resolved_concepts"},
            "source_pack_ids_required": [role], "registry_snapshot_ref": "concept_evidence_registry_snapshot.json"}, indent=2))
        install_unit(svc, g, f"{g}/deploy/supervisor.py batches/{bid}", os.environ.get("GLOSSARY_MAX_USD", 80), f"Glossary pipeline {role}")
        print(f"[chain] {role}: glossary service started", flush=True)
    return None, bid


def regions(ws):
    """[(key, [tile_ids])] one per TOC region, split above MAX_TILES."""
    out = []
    for r in load(ws / "toc.json")["regions"]:
        tiles = [t["tile_id"] for terr in r["terrains"] for t in terr["tiles"]]
        key = re.sub(r"^region_", "", r["region_id"])[:40]
        for i in range(0, len(tiles), MAX_TILES):
            out.append((key if len(tiles) <= MAX_TILES else f"{key}_{i // MAX_TILES + 1}", tiles[i:i + MAX_TILES]))
    return out


def final_step(role, ws, bundle, gbid):
    base = ROLES / role / "final"
    runs = ROLES / role / "final_runs"
    runs.mkdir(exist_ok=True)
    running = sum(1 for k, _ in regions(ws) if unit_state(f"final-pipeline-{role}-{k}") in ("active", "activating"))
    started = 0
    for key, tiles in regions(ws):
        svc = f"final-pipeline-{role}-{key}"
        if unit_exists(svc):
            continue
        if running + started >= MAX_PAR:
            break
        run = runs / key
        if not run.exists():
            sh("git", "clone", "-q", "--local", str(base), str(run), ok=False)
            shutil.copy(base / ".env", run / ".env")
            nm = base / "00_FINAL_PIPELINE_CORE" / "sandbox" / "node_modules"
            if nm.exists() and not (run / "00_FINAL_PIPELINE_CORE" / "sandbox" / "node_modules").exists():
                os.symlink(nm, run / "00_FINAL_PIPELINE_CORE" / "sandbox" / "node_modules")  # one set of Pyodide wheels for every clone
        batch = f"final_batch_{key}"
        B = run / "batches" / batch
        B.mkdir(parents=True, exist_ok=True)
        (B / "run_config.json").write_text(json.dumps({"path_id": role, "glossary_bundle": str(bundle), "glossary_batch_id": gbid, "toc_workspace": str(ws),
                                                       "tiles": tiles, "player_version": "0.1.0"}, indent=2))
        install_unit(svc, run, f"{run}/deploy/supervisor.py batches/{batch}", os.environ.get("FINAL_MAX_USD", 25), f"Final schema {role} {key}")
        started += 1
        print(f"[chain] {role}: final batch {key} ({len(tiles)} tiles) started", flush=True)


def main():
    roles = [r for r in os.environ.get("ROLES", "").split(",") if r] or sorted(p.name for p in ROLES.iterdir() if p.is_dir())
    for role in roles:
        try:
            ws = toc_frozen(role)
            if not ws:
                continue
            bundle, gbid = glossary_step(role, ws)
            if bundle:
                final_step(role, ws, bundle, gbid)
        except Exception as e:
            print(f"[chain] {role}: {e}", flush=True)


if __name__ == "__main__":
    main()
