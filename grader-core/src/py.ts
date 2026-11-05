// Python and chart exercises (runtime kinds `python` and `chart_renderer`): port of scripts/checkers/sandbox.py grade_learner_py.
// The engine is injected (the player: Pyodide with the pipeline's harness; Node tests: sandbox/run_py.mjs) and takes/returns the run_py.mjs job shape.
import { mountTables, mutated, type Registry, type Table } from "./data.ts";
import { rowsEqual } from "./sql.ts";
import type { GradeOut } from "./sql.ts";

type PyScript = { id: string; entry: string; files: { path: string; content: string }[]; mounts: any[]; probes: any[]; chart?: boolean };
export type PyEngine = (job: { packages: string[]; scripts: PyScript[] }) => Promise<Record<string, any>>;

const isNum = (x: unknown): x is number => typeof x === "number";
export function deepEqual(a: any, b: any, tol = 1e-9): boolean {
  if (isNum(a) && isNum(b)) return Math.abs(a - b) <= tol;
  if (Array.isArray(a) && Array.isArray(b)) return a.length === b.length && a.every((x, i) => deepEqual(x, b[i], tol));
  if (a && b && typeof a === "object" && typeof b === "object" && !Array.isArray(a) && !Array.isArray(b)) {
    const ka = Object.keys(a), kb = Object.keys(b);
    return ka.length === kb.length && ka.every((k) => k in b && deepEqual(a[k], b[k], tol));
  }
  return a === b;
}
const normOut = (t: string) => (t ?? "").trim().split("\n").map((x) => x.trimEnd()).join("\n");
const CHART = new Set(["figure_equals", "axes_property", "plotted_data_equals"]);

/** Replace the constant in the first top-level `name = <number|string>` line, keeping the rest of the file as it was. */
export function applyVar(code: string, name: string, value: unknown): string {
  const re = new RegExp(`^(${name}\\s*=\\s*)(?:-?\\d+(?:\\.\\d+)?(?:[eE][-+]?\\d+)?|"(?:[^"\\\\]|\\\\.)*"|'(?:[^'\\\\]|\\\\.)*')(\\s*(?:#.*)?)$`, "m");
  return code.replace(re, (_m, a, b) => `${a}${JSON.stringify(value)}${b}`);
}

function chartValue(kind: string, spec: any, r: any): { got?: any; why?: string } {
  const figs = r.fig?.figures ?? [];
  if (!figs.length) return { why: `no figure was drawn (${r.fig_error ?? "nothing was plotted"})` };
  const f = figs[spec.figure === undefined ? figs.length - 1 : spec.figure < 0 ? figs.length + spec.figure : spec.figure];
  const miss = { why: `the figure has no such part (${kind})` };
  if (!f) return miss;
  if (kind === "figure_equals") return { got: Object.fromEntries(Object.keys(spec.expected).map((k) => [k, k === "chart_types" ? f.axes.map((a: any) => a.chart_types) : f[k]])) };
  const ax = f.axes[spec.axes ?? 0];
  if (!ax) return miss;
  if (kind === "axes_property") return spec.property in ax ? { got: ax[spec.property] } : miss;
  const art = ax.artists.filter((a: any) => a.type === spec.chart)[spec.series ?? 0];
  if (!art || !(spec.field in art)) return miss;
  const v = art[spec.field];
  return { got: spec.sorted && Array.isArray(v) ? [...v].sort((a, b) => (a < b ? -1 : a > b ? 1 : 0)) : v };
}

function result(kind: string, spec: any, id: string, r: any): { got?: any; why?: string } {
  if (!r?.ok) return { why: `the file does not run: ${String(r?.error ?? "?").split("\n").pop()}` };
  if (kind === "stdout_equals") return { got: normOut(r.stdout) };
  if (CHART.has(kind)) return chartValue(kind, spec, r);
  const p = r.probes?.[id];
  return !p || !p.ok ? { why: `cannot evaluate: ${p?.error ?? "no result"}` } : { got: p.value };
}

function match(kind: string, spec: any, got: any): boolean {
  const tol = Number(spec.tolerance ?? 1e-9);
  if (kind === "stdout_equals") return got === normOut(spec.expected);
  if (kind === "dataframe_equals") return !!got && typeof got === "object" && deepEqual(got.columns, spec.expected.columns) && rowsEqual(got.rows, spec.expected.rows, !!spec.ordered, tol);
  return deepEqual(got, spec.expected, tol);
}

export async function gradePython(ix: any, code: string, ctx: { registry: Registry; engine: PyEngine }): Promise<GradeOut & { unchecked: string[] }> {
  const { public: pub, grading: gr } = ix.interaction ?? ix;
  const chart = pub.runtime.kind === "chart_renderer";
  const mounts = pub.workspace.asset_mounts ?? [];
  const tables = mountTables(ctx.registry, mounts);
  const entry = pub.workspace.entry ?? pub.workspace.files.find((f: any) => f.role === "editable")?.path ?? pub.workspace.files[0].path;
  const graded = gr.tests.filter((t: any) => t.kind !== "forbidden_syntax");
  const probes = graded.filter((t: any) => t.kind !== "stdout_equals" && !CHART.has(t.kind)).map((t: any) =>
    t.kind === "function_call" ? { id: t.test_id, kind: "call", function: t.spec.function, args: t.spec.args ?? [], kwargs: t.spec.kwargs ?? {} } : { id: t.test_id, kind: "expr", expr: t.spec.expr });
  const mk = (id: string, src: string, tb: Table[]): PyScript => ({ id, entry, files: [{ path: entry, content: src }],
    mounts: tb.map((t) => ({ path: t.name, columns: t.columns.map((c) => c.name), rows: t.rows })), probes, ...(chart ? { chart: true } : {}) });
  const scripts = [mk("base", code, tables)];
  for (const t of graded) if (t.spec.mount_variants) scripts.push(mk(`test:${t.test_id}`, code, mountTables(ctx.registry, mounts, t.spec.mount_variants)));
  for (const h of gr.hidden_checks ?? []) {
    const ops = h.mutation.ops;
    if (ops[0].op === "set_variable") scripts.push(mk(`hidden:${h.check_id}`, ops.reduce((c: string, o: any) => applyVar(c, o.name, o.value), code), tables));
    else scripts.push(mk(`hidden:${h.check_id}`, code, mutated(tables, h.mutation)));
  }
  const packages = [...new Set(["numpy", "pandas", ...(chart ? ["matplotlib"] : []), ...(pub.runtime.packages ?? [])])];
  const res = await ctx.engine({ packages, scripts });
  const parts: Record<string, boolean> = {}, failed: string[] = [];
  let feedback: string | null = null;
  const fail = (id: string, msg: string | null) => { parts[id] = false; failed.push(id); feedback ??= msg; };
  if (!res.base?.ok) return { correct: false, feedback: `Your code did not run: ${String(res.base?.error ?? "").split("\n").pop()}`, parts: {}, failed: ["base"], unchecked: [] };
  const unchecked: string[] = [];
  for (const t of gr.tests) {
    if (t.kind === "forbidden_syntax") { unchecked.push(t.test_id); continue; }  // needs a Python parser: judged by the pipeline gate on authored code, not here
    const { got, why } = result(t.kind, t.spec, t.test_id, res[`test:${t.test_id}`] ?? res.base);
    if (!why && match(t.kind, t.spec, got)) parts[t.test_id] = true; else fail(t.test_id, t.message_on_fail ?? null);
  }
  for (const h of gr.hidden_checks ?? []) {
    const t = graded.find((x: any) => x.test_id === h.test_id);
    if (!t) continue;
    const { got, why } = result(t.kind, t.spec, t.test_id, res[`hidden:${h.check_id}`]);
    const want = "rows" in h.expected ? { columns: h.expected.columns, rows: h.expected.rows } : h.expected.value;
    if (!why && match(t.kind, { ...t.spec, expected: want }, got)) parts[h.check_id] = true;
    else fail(h.check_id, "Your code gives the right answer on the sample data but not when the data changes: it must compute the answer, not hard-code it.");
  }
  return { correct: failed.length === 0, feedback, parts, failed, unchecked };
}
