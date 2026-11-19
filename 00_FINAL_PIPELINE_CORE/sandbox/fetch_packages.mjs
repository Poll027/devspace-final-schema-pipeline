// Downloads the pinned Pyodide packages (and their dependencies) next to node_modules/pyodide so the runner works with no network at run time.
//   node fetch_packages.mjs        (run once after `npm ci`; verifies every file against the sha256 in pyodide-lock.json)
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "node_modules/pyodide");
const lock = JSON.parse(fs.readFileSync(path.join(dir, "pyodide-lock.json"), "utf8"));
const version = JSON.parse(fs.readFileSync(path.join(dir, "package.json"), "utf8")).version;
const WANT = ["numpy", "pandas", "scipy", "matplotlib", "scikit-learn", "pyyaml", "fastapi", "httpx", "pydantic", "sqlalchemy", "anyio", "jinja2"];  // the last six: python_asgi  // ponytail: add statsmodels here when the stats tiles need it
const need = new Set();  // dependency names are normalised: the lock lists pydantic_core but keys it pydantic-core
const stack = [...WANT];
while (stack.length) { const n = stack.pop(); if (need.has(n)) continue; need.add(n); stack.push(...(lock.packages[n].depends || []).map((d) => d.replace(/_/g, "-"))); }
for (const n of need) {
  const p = lock.packages[n], file = path.join(dir, p.file_name);
  const ok = () => fs.existsSync(file) && crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex") === p.sha256;
  if (ok()) continue;
  const r = await fetch(`https://cdn.jsdelivr.net/pyodide/v${version}/full/${p.file_name}`);
  if (!r.ok) throw new Error(`${p.file_name}: HTTP ${r.status}`);
  fs.writeFileSync(file, Buffer.from(await r.arrayBuffer()));
  if (!ok()) throw new Error(`${p.file_name}: sha256 mismatch`);
  console.log("fetched", p.file_name);
}
console.log("packages ready:", [...need].sort().join(", "));

// Pure-python wheels that are not in the Pyodide lock, pinned by the PyPI-published sha256 (run_py.mjs unpacks them into the interpreter when the job lists the package):
// seaborn for chart_renderer; pyjwt and python-multipart for python_asgi (JWT auth, Form/UploadFile).
const WHEELS = [
  { file: "seaborn-0.13.2-py3-none-any.whl", sha256: "636f8336facf092165e27924f223d3c62ca560b1f2bb5dff7ab7fad265361987",
    url: "https://files.pythonhosted.org/packages/83/11/00d3c3dfc25ad54e731d91449895a79e4bf2384dc3ac01809010ba88f6d5/seaborn-0.13.2-py3-none-any.whl" },
  { file: "PyJWT-2.10.1-py3-none-any.whl", sha256: "dcdd193e30abefd5debf142f9adfcdd2b58004e644f25406ffaebd50bd98dacb",
    url: "https://files.pythonhosted.org/packages/61/ad/689f02752eeec26aed679477e80e632ef1b682313be70793d798c1d5fc8f/PyJWT-2.10.1-py3-none-any.whl" },
  { file: "python_multipart-0.0.20-py3-none-any.whl", sha256: "8a62d3a8335e06589fe01f2a3e178cdcc632f3fbe0d492ad9ee0ec35aab1f104",
    url: "https://files.pythonhosted.org/packages/45/58/38b5afbc1a800eeea951b9285d3912613f2603bdf897a4ab0f4bd7f405fc/python_multipart-0.0.20-py3-none-any.whl" },
];
for (const W of WHEELS) {
  const f = path.join(dir, W.file);
  const good = () => fs.existsSync(f) && crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex") === W.sha256;
  if (good()) continue;
  const r = await fetch(W.url);
  if (!r.ok) throw new Error(`${W.file}: HTTP ${r.status}`);
  fs.writeFileSync(f, Buffer.from(await r.arrayBuffer()));
  if (!good()) { fs.unlinkSync(f); throw new Error(`${W.file}: sha256 mismatch`); }
  console.log("fetched", W.file);
}
