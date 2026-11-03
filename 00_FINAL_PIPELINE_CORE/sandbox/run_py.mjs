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
# ---- chart_renderer: serialise the matplotlib figures to plain JSON (grading reads structure, never pixels)
def _chart_patch():
    import matplotlib.axes as _ax, matplotlib.container as _ct
    if getattr(_ax.Axes, "_dsp_patched", False): return
    _ax.Axes._dsp_patched = True
    _bar, _hist, _bxp = _ax.Axes.bar, _ax.Axes.hist, _ax.Axes.bxp
    def bar(self, *a, **k):
        c = _bar(self, *a, **k)
        f, hist = sys._getframe(1), False
        while f is not None and not hist:  # seaborn.histplot draws its bins with Axes.bar
            hist, f = ("seaborn" in f.f_code.co_filename and "distributions" in f.f_code.co_filename), f.f_back
        c._dsp = "hist" if hist else ("barh" if getattr(c, "orientation", "vertical") == "horizontal" else "bar")
        return c
    def hist(self, *a, **k):
        n = len(self.containers); r = _hist(self, *a, **k)
        for c in self.containers[n:]: c._dsp = "hist"
        return r
    def bxp(self, *a, **k):
        d = _bxp(self, *a, **k)
        self._dsp_box = getattr(self, "_dsp_box", []) + [d]
        return d
    _ax.Axes.bar, _ax.Axes.hist, _ax.Axes.bxp = bar, hist, bxp
def _arr(a): return _js(a.tolist() if hasattr(a, "tolist") else list(a))
def _hex(c):
    import matplotlib.colors as mc
    try: return mc.to_hex(c)
    except Exception: return None
def _axes_json(ax):
    import numpy as np, matplotlib.container as ct, matplotlib.collections as mcol, matplotlib.patches as mp
    skip = set()
    arts, box = [], getattr(ax, "_dsp_box", [])
    for d in box:
        for v in d.values():
            for a in v: skip.add(id(a))
        arts.append({"type": "box", "n": len(d["medians"]), "medians": [_js(m.get_ydata()[0]) for m in d["medians"]]})
    for c in ax.containers:
        if isinstance(c, ct.BarContainer):
            for p in c.patches: skip.add(id(p))
            k = getattr(c, "_dsp", "bar")
            h = [(p.get_width() if k == "barh" else p.get_height()) for p in c.patches]
            pos = [(p.get_y() if k == "barh" else p.get_x()) for p in c.patches]
            arts.append({"type": k, "heights": _js(h), "positions": _js(pos), "widths": _js([(p.get_height() if k == "barh" else p.get_width()) for p in c.patches]),
                         "label": c.get_label() if not c.get_label().startswith("_") else None, "color": _hex(c.patches[0].get_facecolor()) if c.patches else None})
    for l in ax.lines:
        if id(l) in skip: continue
        x, y = l.get_xdata(), l.get_ydata()
        arts.append({"type": "line", "x": _arr(x), "y": _arr(y), "label": l.get_label() if not l.get_label().startswith("_") else None, "color": _hex(l.get_color())})
    for c in ax.collections:
        if isinstance(c, mcol.QuadMesh):
            arts.append({"type": "heatmap", "values": _js(np.ma.filled(np.ma.masked_invalid(c.get_array().reshape(-1)).astype(float), np.nan).reshape(_mesh_shape(c)).tolist())})
        elif isinstance(c, mcol.PathCollection):
            o = np.asarray(c.get_offsets())
            arts.append({"type": "scatter", "x": _arr(o[:, 0]) if len(o) else [], "y": _arr(o[:, 1]) if len(o) else [], "label": c.get_label() if not c.get_label().startswith("_") else None,
                         "color": _hex(c.get_facecolor()[0]) if len(c.get_facecolor()) else None})
        elif isinstance(c, mcol.PolyCollection) and not isinstance(c, mcol.QuadMesh):
            arts.append({"type": "area"})
    for im in ax.images:
        arts.append({"type": "heatmap", "values": _js(np.ma.filled(im.get_array().astype(float), np.nan).tolist())})
    wedges = [p for p in ax.patches if id(p) not in skip and isinstance(p, mp.Wedge)]
    if wedges: arts.append({"type": "pie", "values": _js([round(w.theta2 - w.theta1, 6) % 360 or 360.0 for w in wedges])})
    leg = ax.get_legend()
    return {"title": ax.get_title(), "xlabel": ax.get_xlabel(), "ylabel": ax.get_ylabel(),
            "xticklabels": [t.get_text() for t in ax.get_xticklabels()], "yticklabels": [t.get_text() for t in ax.get_yticklabels()],
            "legend": [t.get_text() for t in leg.get_texts()] if leg else [], "xscale": ax.get_xscale(), "yscale": ax.get_yscale(),
            "xlim": _js(list(ax.get_xlim())), "ylim": _js(list(ax.get_ylim())), "artists": arts, "chart_types": list(dict.fromkeys(a["type"] for a in arts))}
def _mesh_shape(c):
    n = len(c.get_array().reshape(-1)); co = c.get_coordinates()
    return (co.shape[0] - 1, co.shape[1] - 1) if co is not None and getattr(co, "ndim", 0) == 3 else (1, n)
def _figs_json():
    import matplotlib.pyplot as plt
    figs = []
    for n in plt.get_fignums():
        f = plt.figure(n); f.canvas.draw()
        axs = [a for a in f.axes if a.get_label() != "<colorbar>"]  # a colorbar is not a chart of its own
        figs.append({"suptitle": f._suptitle.get_text() if f._suptitle else "", "n_axes": len(axs), "axes": [_axes_json(a) for a in axs]})
    return {"n_figures": len(figs), "figures": figs}
def _png():
    import matplotlib.pyplot as plt, base64
    if not plt.get_fignums(): return None
    b = io.BytesIO(); plt.gcf().savefig(b, format="png", dpi=72); return base64.b64encode(b.getvalue()).decode()
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
    if res["ok"] and sc.get("chart"):
        try:
            res["fig"] = _figs_json()
            if sc.get("png"): res["png"] = _png()
        except BaseException as e:
            res["fig_error"] = "".join(traceback.format_exception_only(type(e), e)).strip()[-300:]
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
const charts = pkgs.includes("matplotlib") || pkgs.includes("seaborn");
let py = null;
// loads every lazily-imported matplotlib/pandas/seaborn module once, so the "modules the script imported" purge between scripts cannot drop a half-initialised library
const WARM = `
import matplotlib.pyplot as _p, pandas as _pd, numpy as _n
_f, _a = _p.subplots(); _a.plot([1, 2]); _a.bar(["a", "b"], [1, 2]); _a.hist([1, 2, 2]); _a.scatter([1], [1]); _a.boxplot([1, 2, 3]); _a.pie([1, 2]); _a.fill_between([0, 1], [0, 1]); _a.legend(["x"]); _a.set_title("t")
_a.imshow([[1, 2], [3, 4]]); _f.canvas.draw(); _f.savefig(io.BytesIO(), format="png")
_pd.DataFrame({"a": [1, 2]}).plot(kind="line"); _pd.DataFrame({"a": [1, 2]}).plot.bar()
if "seaborn" in sys.modules:
    import seaborn as _s
    _d = _pd.DataFrame({"a": ["x", "y", "x"], "b": [1.0, 2.0, 3.0]})
    _s.barplot(data=_d, x="a", y="b"); _s.histplot(data=_d, x="b"); _s.boxplot(data=_d, x="a", y="b"); _s.scatterplot(data=_d, x="b", y="b"); _s.lineplot(data=_d, x="b", y="b"); _s.heatmap(_n.eye(2)); _s.countplot(data=_d, x="a")
_p.close("all")
`;
async function boot() {
  process.binding = stubBinding;
  try {
    py = await loadPyodide({ indexURL: dist, stdout: () => {}, stderr: () => {}, fullStdLib: false });
    await py.loadPackage(pkgs.map((p) => (p === "seaborn" ? "matplotlib" : p)).filter((p, i, a) => a.indexOf(p) === i));
    if (pkgs.includes("seaborn")) py.unpackArchive(new Uint8Array(fs.readFileSync(path.join(dist, "seaborn-0.13.2-py3-none-any.whl"))), "whl");  // pinned by fetch_packages.mjs
    py.runPython(HARNESS);
    if (charts) py.runPython(`import os
os.environ["MPLBACKEND"] = "Agg"
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot
${pkgs.includes("seaborn") ? "import seaborn" : ""}
_chart_patch()
`);
    py.runPython(`import ${pkgs.filter((p) => ["numpy", "pandas", "scipy"].includes(p)).join(", ")}
${charts ? WARM : ""}
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
if "matplotlib" in sys.modules:
    import matplotlib, matplotlib.pyplot as _plt
    _plt.close("all"); matplotlib.rcdefaults(); _plt.style.use("default"); matplotlib.use("Agg")
    if "seaborn" in sys.modules: sys.modules["seaborn"].reset_orig()
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
