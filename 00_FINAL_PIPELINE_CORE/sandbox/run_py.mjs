// Python job runner: Pyodide (the engine the player will use) under Node. Run with `node --permission --allow-fs-read=<this dir>` (see checkers/sandbox.py):
// no host writes, no child processes, no workers; network globals are removed before any learner code runs.
//   node run_py.mjs < job.json  ->  stdout: one JSON document
// job: { scripts: [{ id, files: [{path, content}], entry, mounts: [{path, columns:[names], rows:[[...]]}], probes: [{id, kind: "expr"|"call", expr|function,args,kwargs}] }] }
// Each script runs in a FRESH interpreter. result: { ok, stdout, error?, probes: { id: { ok, value|error } } }
import path from "node:path";
import fs from "node:fs";
import os from "node:os";
import { fileURLToPath } from "node:url";
import { loadPyodide } from "pyodide";
const here = path.dirname(fileURLToPath(import.meta.url));
const dist = path.join(here, "node_modules/pyodide") + "/";

async function readStdin() { let s = ""; for await (const c of process.stdin) s += c; return JSON.parse(s); }

// Pyodide's Node file layer asks process.binding("constants"), which the permission model denies: serve it from the public modules instead,
// and take process.binding away again once the interpreter is up.
const realBinding = process.binding;
const stubBinding = (n) => (n === "constants" ? { fs: fs.constants, os: os.constants, crypto: {}, zlib: {}, trace: {} } : realBinding.call(process, n));
process.binding = stubBinding;
const job = await readStdin();
const out = { engine: "pyodide", version: "0.29.5", results: {} };

// runs inside the interpreter: executes one script, returns a JSON string
const HARNESS = `
import sys, io, json, math, contextlib, traceback, builtins, importlib.abc
class _Block(importlib.abc.MetaPathFinder):  # the JS bridge is the only way out of the sandbox: learner code never gets it
    def find_spec(self, name, path=None, target=None):
        if name.split(".")[0] in ("js", "pyodide_js", "_pyodide_core", "pyodide_http", "micropip") or name in ("pyodide.ffi", "pyodide.code", "pyodide.http", "pyodide.webloop"):
            raise ImportError("module " + name + " is not available in the exercise sandbox")
def _js(v):
    import numpy as np, pandas as pd
    if v is None or isinstance(v, (bool, str)): return v
    if isinstance(v, (np.bool_,)): return bool(v)
    if isinstance(v, (int, np.integer)): return int(v)
    if isinstance(v, (float, np.floating)): return None if math.isnan(v) or math.isinf(v) else float(v)
    if v is pd.NaT or (isinstance(v, float) and v != v): return None
    if isinstance(v, pd.Timestamp): return v.strftime("%Y-%m-%d") if (v.hour, v.minute, v.second, v.microsecond) == (0, 0, 0, 0) else v.strftime("%Y-%m-%d %H:%M:%S")
    if hasattr(v, "isoformat"): return v.isoformat().replace("T", " ")
    if isinstance(v, pd.DataFrame): return {"columns": [str(c) for c in v.columns], "rows": [[_js(x) for x in r] for r in v.itertuples(index=False, name=None)]}
    if isinstance(v, pd.Series): return {"index": [_js(i) for i in v.index], "values": [_js(x) for x in v.tolist()]}
    if isinstance(v, np.ndarray): return _js(v.tolist())
    if isinstance(v, dict): return {str(k): _js(x) for k, x in v.items()}
    if isinstance(v, (set, frozenset)): return sorted((_js(x) for x in v), key=lambda x: json.dumps(x, default=str))
    if isinstance(v, (list, tuple)): return [_js(x) for x in v]
    return repr(v)
def _run(job_json):
    import os
    sc = json.loads(job_json)
    for m in sc.get("mounts", []):
        os.makedirs(os.path.dirname(m["path"]) or ".", exist_ok=True)
        import csv
        with open(m["path"], "w", newline="") as f:
            w = csv.writer(f); w.writerow(m["columns"]); w.writerows([["" if x is None else x for x in r] for r in m["rows"]])
    files = {f["path"]: f["content"] for f in sc["files"]}
    for p, c in files.items():
        os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
        with open(p, "w") as f: f.write(c)
    sys.meta_path.insert(0, _Block())
    for k in [k for k in sys.modules if k in ("js", "pyodide_js") or k.startswith("pyodide.ffi")]: sys.modules.pop(k, None)
    sys.path.insert(0, ".")
    ns = {"__name__": "__main__"}
    buf, res = io.StringIO(), {"ok": True, "probes": {}}
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(files[sc["entry"]], sc["entry"], "exec"), ns)
    except BaseException as e:
        res["ok"], res["error"] = False, "".join(traceback.format_exception_only(type(e), e)).strip()[-500:]
    res["stdout"] = buf.getvalue()
    if res["ok"]:
        for p in sc.get("probes", []):
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    v = eval(p["expr"], ns) if p["kind"] == "expr" else ns[p["function"]](*p.get("args", []), **p.get("kwargs", {}))
                res["probes"][p["id"]] = {"ok": True, "value": _js(v)}
            except BaseException as e:
                res["probes"][p["id"]] = {"ok": False, "error": "".join(traceback.format_exception_only(type(e), e)).strip()[-300:]}
    return json.dumps(res)
`;

// One interpreter per node process (the full load is ~4s locally and far slower on a small server); between scripts the state is reset:
// working files removed, every module the script imported dropped, pandas options and random seeds restored, a new namespace for the program.
// ponytail: a program that monkeypatches the pandas/numpy classes themselves would leak into the next script of the same process; the scripts of one
// exercise are the solution/starter/learner code and mutated copies of the same program, so the leak would repeat identically in each.
const pkgs = job.packages || ["numpy", "pandas"];
let py = null;
async function boot() {
  process.binding = stubBinding;
  try {
    py = await loadPyodide({ indexURL: dist, stdout: () => {}, stderr: () => {}, fullStdLib: false });
    await py.loadPackage(pkgs);
    py.runPython(HARNESS);
    py.runPython(`import ${pkgs.filter((p) => ["numpy", "pandas", "scipy"].includes(p)).join(", ")}
_BASE_MODULES = set(sys.modules)
import random as _random
`);
    for (const g of ["fetch", "XMLHttpRequest", "WebSocket", "EventSource"]) delete globalThis[g];  // no network from inside the sandbox
  } catch (e) { py = null; out.error = String(e.message || e).slice(0, 500); }
  process.binding = () => { throw new Error("process.binding is not available"); };
}
if (job.scripts.length) await boot();
const RESET = `
import os, shutil, sys, random as _r
for k in [k for k in sys.modules if k not in _BASE_MODULES]: sys.modules.pop(k, None)
sys.meta_path[:] = [f for f in sys.meta_path if type(f).__name__ != "_Block"]
sys.path[:] = [p for p in sys.path if p != "."]
for e in os.listdir("."):
    shutil.rmtree(e, ignore_errors=True) if os.path.isdir(e) else os.remove(e)
try:
    import pandas as pd, numpy as np
    pd.reset_option("all"); np.random.seed(0)
except Exception: pass
_r.seed(0)
`;
for (const s of job.scripts) {
  try {
    if (!py) throw new Error(out.error || "interpreter failed to start");
    py.runPython(RESET);
    py.globals.set("_job", JSON.stringify(s));
    out.results[s.id] = JSON.parse(py.runPython("_run(_job)"));
  } catch (e) {
    out.results[s.id] = { ok: false, stdout: "", probes: {}, error: String(e.message || e).slice(0, 500) };
  }
  try { py.runPython("1"); } catch { await boot(); }  // a fatal interpreter error (e.g. a blocked shell command) must not poison the next script
}
process.stdout.write(JSON.stringify(out));
