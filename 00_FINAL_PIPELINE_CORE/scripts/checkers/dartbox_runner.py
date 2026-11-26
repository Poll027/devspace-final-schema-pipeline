"""Runs INSIDE the systemd sandbox (user dartbox, no network, no /home): source is passed with `python3 -c`, the job arrives on stdin.
job {template, flutter, pub_cache, runs: [{id, files: {path: content}, tests: [test paths]}]}  ->  {results: {run_id: {test_path: {result: pass|fail|error, count, message}}}}
`error` = the file did not load/compile; `fail` = it ran and an expectation or the framework failed."""
import json, os, shutil, subprocess, sys

job = json.load(sys.stdin)
env = {"PATH": f"{job['flutter']}/bin:/usr/bin:/bin", "HOME": "/tmp/home", "PUB_CACHE": job["pub_cache"], "LANG": "C.UTF-8", "CI": "true", "FLUTTER_SUPPRESS_ANALYTICS": "true", "FLUTTER_ROOT": job["flutter"]}  # the snapshot is run directly: bin/flutter wants to write into the read-only SDK
os.makedirs("/tmp/home", exist_ok=True)
out = {}
for n, run in enumerate(job["runs"]):
    work = f"/tmp/w{n}"
    shutil.copytree(job["template"], work, ignore=shutil.ignore_patterns("build", "android", "ios", "web"), copy_function=shutil.copyfile)
    for path, content in run["files"].items():
        f = os.path.normpath(os.path.join(work, path))
        assert f.startswith(work + "/") and path.split("/")[0] in ("lib", "test"), f"bad path {path}"
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, "w").write(content)
    p = subprocess.run([f"{job['flutter']}/bin/cache/dart-sdk/bin/dart", f"{job['flutter']}/bin/cache/flutter_tools.snapshot", "--no-version-check", "test", "--no-pub", "--reporter", "json", "--timeout", "30s", *run["tests"]],
                       cwd=work, env=env, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=240)
    suites, tests, msgs, done = {}, {}, {}, {}
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if not isinstance(e, dict):
            continue
        t = e.get("type")
        if t == "suite":
            suites[e["suite"]["id"]] = os.path.relpath(e["suite"]["path"], work)
        elif t == "testStart":
            tests[e["test"]["id"]] = (e["test"]["suiteID"], e["test"]["name"])
        elif t in ("error", "print"):
            msgs.setdefault(e["testID"], []).append(e.get("error") or e.get("message") or "")
        elif t == "testDone":
            done[e["testID"]] = (e["result"], e.get("hidden", False), e.get("skipped", False))
    res = {}
    for path in run["tests"]:
        ids = [i for i, (s, _) in tests.items() if suites.get(s) == path]
        real = [i for i in ids if not done.get(i, ("", True, False))[1] and not done.get(i, ("", True, False))[2]]
        bad = [i for i in ids if done.get(i, ("error",))[0] != "success"]
        text = "\n".join(m for i in (bad or ids) for m in msgs.get(i, []))
        if any(tests[i][1].startswith("loading ") for i in bad) or not ids or (not real and not bad):
            res[path] = {"result": "error", "count": 0, "message": (text or p.stdout[-1500:] + p.stderr[-1500:])[:2500]}
        else:
            res[path] = {"result": "fail" if bad else "pass", "count": len(real), "message": text[:2500]}
    out[run["id"]] = res
    shutil.rmtree(work, ignore_errors=True)
json.dump({"results": out}, sys.stdout)
