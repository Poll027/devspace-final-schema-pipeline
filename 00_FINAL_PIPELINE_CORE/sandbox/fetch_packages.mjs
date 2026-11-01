// Downloads the pinned Pyodide packages (and their dependencies) next to node_modules/pyodide so the runner works with no network at run time.
//   node fetch_packages.mjs        (run once after `npm ci`; verifies every file against the sha256 in pyodide-lock.json)
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), "node_modules/pyodide");
const lock = JSON.parse(fs.readFileSync(path.join(dir, "pyodide-lock.json"), "utf8"));
const version = JSON.parse(fs.readFileSync(path.join(dir, "package.json"), "utf8")).version;
const WANT = ["numpy", "pandas", "scipy"];  // ponytail: add matplotlib/statsmodels here when the viz/stats tiles need them
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
