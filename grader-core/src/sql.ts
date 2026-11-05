// SQL exercises: same comparison, same data copies and same hidden checks as the pipeline's reference grader
// (scripts/checkers/sandbox.py grade_learner). The engine is injected: the player passes a DuckDB-WASM adapter,
// Node tests pass an adapter over sandbox/run_sql.mjs. Both take/return the job shape documented in run_sql.mjs.
import { mountTables, mutated, type Registry, type Table } from "./data.ts";

export type SqlResult = { ok: boolean; error?: string; columns: string[]; rows: unknown[][]; outputs?: ({ columns: string[]; rows: unknown[][] } | null)[] };
export type SqlEngine = (job: { tables: Table[]; scripts: { id: string; statements: string[]; tables?: Table[] }[] }) => Promise<Record<string, SqlResult>>;
export type GradeOut = { correct: boolean; feedback: string | null; parts: Record<string, boolean>; failed: string[] };

/** Split on `;` outside quotes and comments. */
export function splitStatements(sql: string): string[] {
  const out: string[] = []; let cur = "", q: string | null = null;
  for (let i = 0; i < sql.length; i++) {
    const c = sql[i], n = sql[i + 1];
    if (q) { cur += c; if (c === q) { if (n === q) { cur += n; i++; } else q = null; } continue; }
    if (c === "-" && n === "-") { while (i < sql.length && sql[i] !== "\n") i++; cur += "\n"; continue; }
    if (c === "/" && n === "*") { i += 2; while (i < sql.length && !(sql[i] === "*" && sql[i + 1] === "/")) i++; i++; continue; }
    if (c === "'" || c === '"') { q = c; cur += c; continue; }
    if (c === ";") { if (cur.trim()) out.push(cur.trim()); cur = ""; continue; }
    cur += c;
  }
  if (cur.trim()) out.push(cur.trim());
  return out;
}

const isNum = (x: unknown): x is number => typeof x === "number";
const same = (a: unknown, b: unknown, tol: number) => (isNum(a) && isNum(b) ? Math.abs(a - b) <= tol : a === b);
const rounded = (r: unknown[]) => JSON.stringify(r.map((v) => (isNum(v) ? Math.round(v * 1e6) / 1e6 : v)));
export function rowsEqual(got: unknown[][], want: unknown[][], ordered: boolean, tol = 1e-9): boolean {
  if (got.length !== want.length) return false;
  if (!ordered) { const key = (r: unknown[]) => JSON.stringify(r); got = [...got].sort((a, b) => (key(a) < key(b) ? -1 : 1)); want = [...want].sort((a, b) => (key(a) < key(b) ? -1 : 1)); got = [...got].sort((a, b) => (rounded(a) < rounded(b) ? -1 : 1)); want = [...want].sort((a, b) => (rounded(a) < rounded(b) ? -1 : 1)); }
  return got.every((g, i) => g.length === want[i].length && g.every((x, j) => same(x, want[i][j], tol)));
}
const pick = (r: SqlResult | undefined, idx: number | null | undefined) => (!r || !r.ok ? null : idx == null ? r : (r.outputs ?? [])[idx] ?? null);
const sameResult = (r: { columns: string[]; rows: unknown[][] } | null, exp: { columns: string[]; rows: unknown[][] }, ordered: boolean, tol = 1e-9) =>
  r !== null && JSON.stringify(r.columns.map((c) => c.toLowerCase())) === JSON.stringify(exp.columns.map((c) => c.toLowerCase())) && rowsEqual(r.rows, exp.rows, ordered, tol);

// forbidden_syntax descriptors seen in the lessons; unknown descriptors are reported, not silently passed.
const DETECT: Record<string, RegExp> = {
  DISTINCT: /\bDISTINCT\b/i, WHERE: /\bWHERE\b/i, "CASE WHEN ... THEN ... ELSE ... END": /\bCASE\b/i,
  "table alias (FROM table AS alias)": /\b(?:FROM|JOIN)\s+[\w."]+\s+(?:AS\s+)?(?!WHERE\b|JOIN\b|ON\b|GROUP\b|ORDER\b|LIMIT\b|INNER\b|LEFT\b|RIGHT\b|FULL\b|CROSS\b|UNION\b|HAVING\b|USING\b)[A-Za-z_]\w*/i,
};
const bare = (sql: string) => sql.replace(/'(?:[^']|'')*'/g, "''");

export async function gradeSql(ix: any, learnerSql: string, ctx: { registry: Registry; engine: SqlEngine }): Promise<GradeOut> {
  const { public: pub, grading: gr } = ix.interaction ?? ix;
  const mounts = pub.workspace.asset_mounts ?? [];
  const tables = mountTables(ctx.registry, mounts), stmts = splitStatements(learnerSql);
  const scripts: { id: string; statements: string[]; tables?: Table[] }[] = [{ id: "base", statements: stmts }];
  for (const t of gr.tests) if (t.kind === "query_result_equals" && t.spec.mount_variants)
    scripts.push({ id: `test:${t.test_id}`, statements: stmts, tables: mountTables(ctx.registry, mounts, t.spec.mount_variants) });
  for (const h of gr.hidden_checks ?? []) scripts.push({ id: `hidden:${h.check_id}`, statements: stmts, tables: mutated(tables, h.mutation) });
  const res = await ctx.engine({ tables, scripts });
  const parts: Record<string, boolean> = {}, failed: string[] = [];
  let feedback: string | null = null;
  const fail = (id: string, msg: string | null) => { parts[id] = false; failed.push(id); feedback ??= msg; };
  if (!res.base?.ok) return { correct: false, feedback: `Your query did not run: ${(res.base?.error ?? "").split("\n")[0]}`, parts: {}, failed: ["base"] };
  for (const t of gr.tests) {
    const s = t.spec;
    if (t.kind === "query_result_equals") {
      const whole = res[`test:${t.test_id}`] ?? res.base;
      if (sameResult(pick(whole, s.statement), s.expected, !!s.ordered, Number(s.tolerance ?? 1e-9))) parts[t.test_id] = true; else fail(t.test_id, t.message_on_fail ?? null);
    } else if (t.kind === "forbidden_syntax") {
      const text = stmts.map(bare).join("\n");
      const bad = (s.descriptors ?? []).filter((d: string) => DETECT[d]?.test(text));
      if (bad.length) fail(t.test_id, t.message_on_fail ?? null); else parts[t.test_id] = true;
    }
  }
  for (const h of gr.hidden_checks ?? []) {
    if (sameResult(pick(res[`hidden:${h.check_id}`], h.statement), h.expected, !!h.ordered)) parts[h.check_id] = true;
    else fail(h.check_id, "Your query gives the right answer on the sample data but not when the data changes: it must compute the answer, not hard-code it.");
  }
  return { correct: failed.length === 0, feedback, parts, failed };
}
