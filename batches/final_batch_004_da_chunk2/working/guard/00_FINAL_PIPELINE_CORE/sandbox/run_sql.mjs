// SQL job runner: DuckDB-WASM (the engine the player will use) under Node. No network, no host filesystem.
//   node run_sql.mjs < job.json  ->  stdout: one JSON document
// job: { tables: [{name, columns:[{name,type}], rows:[[...]]}], scripts: [{id, statements:[sql,...]}] }
// Each script runs in a FRESH database (own tables) so a learner query can't see another script's changes.
// Each script is a list of statements; the result is that of the LAST statement that returns rows.
// Isolation: WASM-under-Node can reach the host fs/network by default, so every script runs with external access disabled and the
// configuration locked; the Python wrapper adds a wall-clock timeout and a Node heap limit.
// ponytail: types are mapped from the registry column types; DATE/TIMESTAMP columns arrive as ISO strings.
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
const require = createRequire(import.meta.url);
const duckdb = require("@duckdb/duckdb-wasm/dist/duckdb-node-blocking.cjs");
const here = path.dirname(fileURLToPath(import.meta.url));
const dist = path.join(here, "node_modules/@duckdb/duckdb-wasm/dist");

const TYPE = { string: "VARCHAR", integer: "BIGINT", number: "DOUBLE", float: "DOUBLE", decimal: "DOUBLE", boolean: "BOOLEAN", date: "DATE", datetime: "TIMESTAMP", timestamp: "TIMESTAMP" };
const q = (s) => `"${String(s).replace(/"/g, '""')}"`;
const lit = (v) => (v === null || v === undefined ? "NULL" : typeof v === "number" ? (Number.isFinite(v) ? String(v) : "NULL") : typeof v === "boolean" ? (v ? "TRUE" : "FALSE") : `'${String(v).replace(/'/g, "''")}'`);

async function readStdin() { let s = ""; for await (const c of process.stdin) s += c; return JSON.parse(s); }

// Result values -> plain JSON, by Arrow type: DECIMAL arrives as an UNSCALED integer (12.50 -> 1250), DATE/TIMESTAMP as epoch ms.
// Output contract (the exercise's spec.expected uses the same forms): numbers for integers/floats/decimals; dates "YYYY-MM-DD";
// timestamps "YYYY-MM-DD HH:MM:SS" (UTC); booleans; null; strings; lists as arrays.
function normalise(v, type) {
  if (v === null || v === undefined) return null;
  const t = String(type);
  if (t.startsWith("Decimal")) return Number(String(v)) / 10 ** (type.scale || 0);
  if (t.startsWith("Date")) return new Date(Number(v)).toISOString().slice(0, 10);
  if (t.startsWith("Timestamp")) return new Date(Number(v)).toISOString().slice(0, 19).replace("T", " ");
  if (typeof v === "bigint") return Number.isSafeInteger(Number(v)) ? Number(v) : String(v);
  if (typeof v === "object" && typeof v[Symbol.iterator] === "function") return Array.from(v, (x) => normalise(x, type.children?.[0]?.type));
  if (typeof v === "object") return String(v);
  return v;
}

const job = await readStdin();
const bundles = { mvp: { mainModule: path.join(dist, "duckdb-mvp.wasm"), mainWorker: "" }, eh: { mainModule: path.join(dist, "duckdb-eh.wasm"), mainWorker: "" } };
async function freshDb() {  // a brand-new in-memory database per script: nothing a query creates can leak into another script
  const b = await duckdb.createDuckDB(bundles, new duckdb.VoidLogger(), duckdb.NODE_RUNTIME);
  await b.instantiate(() => {});
  return b;
}
const out = { engine: "duckdb-wasm", version: "1.32.0", results: {} };
for (const s of job.scripts) {
  const bindings = await freshDb();
  const conn = bindings.connect();
  try {
    for (const t of s.tables || job.tables) {  // a script may carry its own tables (hidden-test data variant)
      conn.query(`CREATE TABLE ${q(t.name)} (${t.columns.map((c) => `${q(c.name)} ${TYPE[c.type] || "VARCHAR"}`).join(", ")})`);
      for (let i = 0; i < t.rows.length; i += 200) {
        const chunk = t.rows.slice(i, i + 200).map((r) => `(${r.map(lit).join(", ")})`).join(", ");
        conn.query(`INSERT INTO ${q(t.name)} VALUES ${chunk}`);
      }
    }
    // lock down BEFORE any learner/solution SQL runs: no host files, no network, no extensions; the setting cannot be re-enabled
    conn.query("SET enable_external_access=false");
    conn.query("SET lock_configuration=true");
    let last = null;
    for (const sql of s.statements) {
      const res = conn.query(sql);
      if (res.numCols > 0) {
        last = { columns: res.schema.fields.map((f) => f.name), rows: res.toArray().map((row) => res.schema.fields.map((f) => normalise(row[f.name], f.type))) };
      }
    }
    out.results[s.id] = last ? { ok: true, ...last } : { ok: true, columns: [], rows: [] };
  } catch (e) {
    out.results[s.id] = { ok: false, error: String(e.message || e).slice(0, 500) };
  } finally {
    conn.close();
  }
}
process.stdout.write(JSON.stringify(out));
