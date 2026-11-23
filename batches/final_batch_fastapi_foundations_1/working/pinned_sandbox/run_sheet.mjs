// Spreadsheet job runner: HyperFormula (the engine the player will use) under Node. Run with `node --permission --allow-fs-read=<this dir>` (see checkers/sandbox.py):
// pure JS, no host writes, no child processes, no workers; network globals are removed before any learner formula is parsed.
//   node run_sheet.mjs < job.json  ->  stdout: one JSON document
// job: { scripts: [{ id, sheets: [{name, columns:[names], rows:[[...]]}], content: "<learner sheet file>", probes: [{id, kind: "cell"|"range", ref}] }] }
// The sheet file is lines `[Sheet!]A1: value-or-=formula` (blank lines and lines starting // are ignored). Each mounted CSV is a sheet (header in row 1,
// data from row 2); the file's cells are laid over it. Each script builds a FRESH workbook, so no state survives between scripts.
// result: { ok, error?, probes: { id: { ok, value|error } } }; an error cell reads as its text ("#DIV/0!"), an empty cell as null.
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { HyperFormula, DetailedCellError } = require("hyperformula");
for (const g of ["fetch", "XMLHttpRequest", "WebSocket", "EventSource"]) delete globalThis[g];

async function readStdin() { let s = ""; for await (const c of process.stdin) s += c; return JSON.parse(s); }
const job = await readStdin();
const out = { engine: "hyperformula", version: HyperFormula.version, results: Object.create(null) };

const colNum = (s) => [...s].reduce((n, c) => n * 26 + c.charCodeAt(0) - 64, 0) - 1;
const LINE = /^(?:([^!:]+)!)?\$?([A-Za-z]{1,3})\$?(\d{1,6})\s*:\s?(.*)$/;
const constant = (v) => { const t = v.trim(); if (t === "") return null; if (/^[-+]?(\d+\.?\d*|\.\d+)(e[-+]?\d+)?$/i.test(t)) return Number(t); if (/^(true|false)$/i.test(t)) return t.toLowerCase() === "true"; return v; };
const plain = (v) => (v instanceof DetailedCellError ? v.value : v === undefined || v === "" ? null : v);

function build(sc) {
  const names = sc.sheets.map((s) => s.name);
  if (!names.length) names.push("Sheet1");
  const grid = new Map(sc.sheets.map((s) => [s.name, [s.columns.slice(), ...s.rows.map((r) => r.slice())]]));
  if (!grid.has(names[0])) grid.set(names[0], []);
  const find = (n) => names.find((x) => x.toLowerCase() === n.trim().toLowerCase());
  sc.content.split(/\r?\n/).forEach((line, i) => {
    if (!line.trim() || line.trim().startsWith("//")) return;
    const m = LINE.exec(line);
    if (!m) throw new Error(`line ${i + 1}: expected "A1: value" or "A1: =formula"`);
    const sheet = m[1] ? find(m[1]) : names[0];
    if (!sheet) throw new Error(`line ${i + 1}: unknown sheet ${JSON.stringify(m[1])}`);
    const r = Number(m[3]) - 1, c = colNum(m[2].toUpperCase());
    if (r > 5000 || c > 200) throw new Error(`line ${i + 1}: cell outside the allowed 5000 x 200 area`);
    const rows = grid.get(sheet);
    while (rows.length <= r) rows.push([]);
    while (rows[r].length <= c) rows[r].push(null);
    rows[r][c] = m[4].trim().startsWith("=") ? m[4].trim() : constant(m[4]);
  });
  return HyperFormula.buildFromSheets(Object.fromEntries(names.map((n) => [n, grid.get(n)])), { licenseKey: "gpl-v3", useColumnIndex: false });
}

for (const sc of job.scripts) {
  let hf = null;
  try {
    hf = build(sc);
    const res = { ok: true, probes: Object.create(null) };
    for (const p of sc.probes || []) {
      try {
        if (p.kind === "cell") {
          const a = hf.simpleCellAddressFromString(p.ref, 0);
          if (!a) throw new Error(`bad cell reference ${p.ref}`);
          res.probes[p.id] = { ok: true, value: plain(hf.getCellValue(a)) };
        } else {
          const r = hf.simpleCellRangeFromString(p.ref, 0);
          if (!r) throw new Error(`bad range ${p.ref}`);
          res.probes[p.id] = { ok: true, value: hf.getRangeValues(r).map((row) => row.map(plain)) };
        }
      } catch (e) { res.probes[p.id] = { ok: false, error: String(e.message || e).slice(0, 300) }; }
    }
    out.results[sc.id] = res;
  } catch (e) {
    out.results[sc.id] = { ok: false, probes: {}, error: String(e.message || e).slice(0, 500) };
  }
  try { hf?.destroy(); } catch { /* ignore */ }
}
process.stdout.write(JSON.stringify(out));
