// Node adapters over the pipeline's sandbox runners (same engines the player uses: DuckDB-WASM, Pyodide, HyperFormula).
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import type { SqlEngine } from "../src/sql.ts";

const SANDBOX = join(import.meta.dirname, "..", "..", "00_FINAL_PIPELINE_CORE", "sandbox");
const run = (file: string, job: unknown) => {
  const r = spawnSync("node", ["--permission", `--allow-fs-read=${SANDBOX}`, "--max-old-space-size=2048", join(SANDBOX, file)], { input: JSON.stringify(job), encoding: "utf8", maxBuffer: 1 << 28, cwd: SANDBOX });
  if (r.status !== 0) throw new Error(`${file} failed: ${r.stderr.slice(0, 500)}`);
  return JSON.parse(r.stdout);
};
export const sqlEngine: SqlEngine = async (job) => run("run_sql.mjs", job).results;
