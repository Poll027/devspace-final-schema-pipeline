"""`flutter` runtime: the learner's Dart files + hidden `flutter test` files, run by checkers/dartbox_runner.py inside a systemd sandbox
(see runtimes.json). Test kind `dart_test` spec {code?, replace?, expect?}: `code` is a complete hidden test file (omitted = the learner's own
editable test file under test/ is what runs), `replace` swaps readonly files for that test (a deliberately broken widget for test-writing practice),
`expect` is "pass" (default) or "fail"."""
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

RUNNER = Path(__file__).with_name("dartbox_runner.py")


def flutter_missing(pin):
    return None if Path(pin["sdk"], "bin", "flutter").exists() and Path(pin["template"]).exists() else "flutter SDK/template not installed on this host (registry/runtimes.json flutter.sdk)"


def sandbox_cmd(limit, lockfile):
    props = [f"ReadWritePaths={lockfile}",  # the one SDK file the flutter tool must open for writing
             "User=dartbox", "PrivateNetwork=yes", "PrivateTmp=yes", "PrivateDevices=yes", "ProtectHome=yes", "ProtectSystem=strict", "ProtectProc=invisible",
             "NoNewPrivileges=yes", "MemoryMax=6G", "TasksMax=1024", f"RuntimeMaxSec={limit}"]
    return ["sudo", "-n", "systemd-run", "--quiet", "--pipe", "--wait", "--collect", *[a for p in props for a in ("-p", p)], "/usr/bin/python3", "-I", "-c", RUNNER.read_text()]


def build_runs(workspace_files, solution_files, tests):
    """One run per (state, replaced files): state is `solution` or `starter`; tests sharing the same files share one `flutter test` call."""
    base = {f["path"]: f["content"] for f in workspace_files}
    solved = {**base, **{f["path"]: f["content"] for f in solution_files}}
    learner_tests = [f["path"] for f in workspace_files if f["role"] == "editable" and f["path"].startswith("test/") and f["path"].endswith("_test.dart")]
    runs, where = {}, {}
    for state, files in (("solution", solved), ("starter", base)):
        for t in tests:
            sp = t["spec"]
            rep = sp.get("replace") or {}
            rid = f"{state}:{json.dumps(rep, sort_keys=True)}"
            r = runs.setdefault(rid, {"id": rid, "files": {**files, **rep}, "tests": []})
            if sp.get("code"):
                path = f"test/{re.sub(r'[^A-Za-z0-9_]', '_', t['test_id'])}_grader_test.dart"
                r["files"][path] = sp["code"]
                paths = [path]
            else:
                paths = learner_tests
            r["tests"] += [p for p in paths if p not in r["tests"]]
            where[(state, t["test_id"])] = (rid, paths)
    return list(runs.values()), where


def execute(pin, runs):
    job = {"template": pin["template"], "flutter": pin["sdk"], "pub_cache": pin["pub_cache"], "runs": runs}
    limit = 120 + 120 * len(runs)
    # identical code + tests + SDK pin gives identical results, and the gates re-run every exercise many times (~13 s each)
    key = hashlib.sha256(json.dumps([pin["version"], RUNNER.read_text(), job], sort_keys=True).encode()).hexdigest()
    cache = Path(os.environ.get("DARTBOX_CACHE", Path.home() / ".cache" / "dartbox")) / f"{key}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    p = subprocess.run(sandbox_cmd(limit, f"{pin['sdk']}/bin/cache/lockfile"), input=json.dumps(job), capture_output=True, text=True, timeout=limit + 60)
    if p.returncode or not p.stdout.strip():
        raise RuntimeError(f"flutter runner crashed ({p.returncode}): {(p.stderr or p.stdout)[-600:]}")
    results = json.loads(p.stdout)["results"]
    if not any(t["result"] == "error" for r in results.values() for t in r.values()):  # never remember a failure to load: it may be the host, not the code
        cache.parent.mkdir(parents=True, exist_ok=True)
        tmp = cache.with_suffix(f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(results))
        tmp.replace(cache)
    return results


def outcome_of(results, where, state, test_id):
    rid, paths = where[(state, test_id)]
    got = [results[rid][p] for p in paths]
    for kind in ("error", "fail"):
        for g in got:
            if g["result"] == kind:
                return kind, g["message"]
    return ("pass" if got else "error"), ""
