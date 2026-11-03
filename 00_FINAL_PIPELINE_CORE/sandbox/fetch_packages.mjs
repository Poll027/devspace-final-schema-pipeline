// Downloads the pinned Pyodide packages (and their dependencies) next to node_modules/pyodide so the runner works with no network at run time.
//   node fetch_packages.mjs        (run once after `npm ci`; verifies every file against the sha256 in pyodide-lock.json)
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "node_modules/pyodide");
const lock = JSON.parse(fs.readFileSync(path.join(dir, "pyodide-lock.json"), "utf8"));
const version = JSON.parse(fs.readFileSync(path.join(dir, "package.json"), "utf8")).version;
const WANT = ["numpy", "pandas", "scipy", "matplotlib"];  // ponytail: add statsmodels here when the stats tiles need it
const need = new Set();
const stack = [...WANT];
while (stack.length) { const n = stack.pop(); if (need.has(n)) continue; need.add(n); stack.push(...(lock.packages[n].depends || [])); }
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

// chart_renderer: seaborn is not in the Pyodide lock; it is one pure-Python wheel, pinned by the PyPI-published sha256 (run_py.mjs unpacks it into the interpreter).
const SEABORN = { file: "seaborn-0.13.2-py3-none-any.whl", sha256: "636f8336facf092165e27924f223d3c62ca560b1f2bb5dff7ab7fad265361987",
  url: "https://files.pythonhosted.org/packages/83/11/00d3c3dfc25ad54e731d91449895a79e4bf2384dc3ac01809010ba88f6d5/seaborn-0.13.2-py3-none-any.whl" };
const sf = path.join(dir, SEABORN.file);
const sok = () => fs.existsSync(sf) && crypto.createHash("sha256").update(fs.readFileSync(sf)).digest("hex") === SEABORN.sha256;
if (!sok()) {
  const r = await fetch(SEABORN.url);
  if (!r.ok) throw new Error(`${SEABORN.file}: HTTP ${r.status}`);
  fs.writeFileSync(sf, Buffer.from(await r.arrayBuffer()));
  if (!sok()) { fs.unlinkSync(sf); throw new Error(`${SEABORN.file}: sha256 mismatch`); }
  console.log("fetched", SEABORN.file);
}
