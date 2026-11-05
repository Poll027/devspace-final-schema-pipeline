// Spreadsheet exercises (runtime `spreadsheet`): port of scripts/checkers/sandbox.py grade_learner_sheet.
// The learner's file is lines `[Sheet!]A1: value-or-=formula` laid over the mounted CSVs; HyperFormula is injected (job shape of sandbox/run_sheet.mjs).
import { mountTables, mutated, type Registry, type Table } from "./data.ts";
import { deepEqual } from "./py.ts";
import type { GradeOut } from "./sql.ts";

type SheetScript = { id: string; content: string; sheets: { name: string; columns: string[]; rows: unknown[][] }[]; probes: { id: string; kind: "cell" | "range"; ref: string }[] };
export type SheetEngine = (job: { scripts: SheetScript[] }) => Promise<Record<string, any>>;

const LINE = /^(?:([^!:]+)!)?\$?([A-Za-z]{1,3})\$?(\d{1,6})\s*:\s?(.*)$/;
const sheetName = (p: string) => p.replace(/^.*\//, "").replace(/\.[^.]+$/, "");

/** Replace the typed constant of cell `ref` ('A1' or 'Sheet!A1'); a formula cell is left alone. */
export function applyCellVar(text: string, ref: string, value: unknown): string {
  const want = ref.split("!").pop()!.replace(/\$/g, "").toUpperCase();
  let done = false;
  return text.split(/(?<=\n)/).map((ln) => {
    const body = ln.replace(/\r?\n$/, ""), m = LINE.exec(body);
    if (!done && m && (m[2].toUpperCase() + m[3]) === want && !m[4].trim().startsWith("=")) {
      done = true;
      const at = body.length - m[4].length;
      return body.slice(0, at) + (typeof value === "string" ? JSON.stringify(value) : String(value)) + ln.slice(body.length);
    }
    return ln;
  }).join("");
}

/** Function names used by the formula in cell `ref`, or null when that cell holds no formula. */
export function cellFunctions(text: string, ref: string): Set<string> | null {
  const want = ref.split("!").pop()!.replace(/\$/g, "").toUpperCase();
  for (const ln of text.split(/\r?\n/)) {
    const m = LINE.exec(ln);
    if (m && (m[2].toUpperCase() + m[3]) === want && m[4].trim().startsWith("=")) {
      const f = m[4].replace(/"(?:[^"]|"")*"/g, '""');
      return new Set([...f.matchAll(/([A-Za-z][A-Za-z0-9.]*)\s*\(/g)].map((x) => x[1].toUpperCase()));
    }
  }
  return null;
}

const probesOf = (tests: any[]) => tests.filter((t) => t.kind === "cell_equals" || t.kind === "range_equals")
  .map((t) => ({ id: t.test_id, kind: (t.kind === "cell_equals" ? "cell" : "range") as "cell" | "range", ref: t.spec[t.kind === "cell_equals" ? "cell" : "range"] }));
const value = (r: any, id: string) => (!r?.ok ? { why: `the sheet does not load: ${String(r?.error ?? "?").split("\n").pop()}` } : r.probes?.[id]?.ok ? { got: r.probes[id].value } : { why: `cannot evaluate: ${r.probes?.[id]?.error ?? "no result"}` });

export async function gradeSheet(ix: any, content: string, ctx: { registry: Registry; engine: SheetEngine }): Promise<GradeOut & { unchecked: string[] }> {
  const { public: pub, grading: gr } = ix.interaction ?? ix;
  const tables = mountTables(ctx.registry, pub.workspace.asset_mounts ?? []), probes = probesOf(gr.tests);
  const mk = (id: string, text: string, tb: Table[]): SheetScript => ({ id, content: text, sheets: tb.map((t) => ({ name: sheetName(t.name), columns: t.columns.map((c) => c.name), rows: t.rows })), probes });
  const scripts = [mk("base", content, tables)];
  for (const h of gr.hidden_checks ?? []) {
    const ops = h.mutation.ops;
    scripts.push(ops[0].op === "set_variable" ? mk(`hidden:${h.check_id}`, ops.reduce((c: string, o: any) => applyCellVar(c, o.name, o.value), content), tables) : mk(`hidden:${h.check_id}`, content, mutated(tables, h.mutation)));
  }
  const res = await ctx.engine({ scripts });
  const parts: Record<string, boolean> = {}, failed: string[] = [], unchecked: string[] = [];
  let feedback: string | null = null;
  const fail = (id: string, msg: string | null) => { parts[id] = false; failed.push(id); feedback ??= msg; };
  if (!res.base?.ok) return { correct: false, feedback: `Your sheet did not load: ${String(res.base?.error ?? "").split("\n").pop()}`, parts: {}, failed: ["base"], unchecked };
  for (const t of gr.tests) {
    if (t.kind === "forbidden_syntax") { unchecked.push(t.test_id); continue; }
    if (t.kind === "formula_uses") {
      const fns = cellFunctions(content, t.spec.cell);
      if (fns && t.spec.functions.every((f: string) => fns.has(f.toUpperCase()))) parts[t.test_id] = true; else fail(t.test_id, t.message_on_fail ?? null);
      continue;
    }
    const { got, why } = value(res.base, t.test_id);
    if (!why && deepEqual(got, t.spec.expected, Number(t.spec.tolerance ?? 1e-9))) parts[t.test_id] = true; else fail(t.test_id, t.message_on_fail ?? null);
  }
  for (const h of gr.hidden_checks ?? []) {
    const t = gr.tests.find((x: any) => x.test_id === h.test_id);
    if (!t) continue;
    const { got, why } = value(res[`hidden:${h.check_id}`], t.test_id);
    if (!why && deepEqual(got, h.expected.value, Number(t.spec.tolerance ?? 1e-9))) parts[h.check_id] = true;
    else fail(h.check_id, "Your sheet gives the right answer on the sample data but not when the data changes: use formulas over the data, not typed-in numbers.");
  }
  return { correct: failed.length === 0, feedback, parts, failed, unchecked };
}

/** formula_entry: the learner types one formula into `target_cell`. Right value on the data, the required functions, and (unless forbid_hardcoded_values
 *  is false) the same result as the reference formula on changed data, so a typed-in number fails. */
export async function gradeFormulaEntry(ix: any, formula: string, ctx: { registry: Registry; engine: SheetEngine }): Promise<GradeOut> {
  const { public: pub, grading: gr } = ix.interaction ?? ix;
  const sheet = pub.sheet_name || "Sheet1", cell = pub.target_cell, f = (formula ?? "").trim();
  if (!f.startsWith("=")) return { correct: false, feedback: "Start the formula with =", parts: {}, failed: ["value"] };
  const mount = { asset_id: pub.asset_ref.asset_id, mount_path: sheet + ".csv", ...(pub.asset_ref.variant_id ? { variant_id: pub.asset_ref.variant_id } : {}) };
  const tables = mountTables(ctx.registry, [mount]);
  const probes = [{ id: "v", kind: "cell" as const, ref: cell }];
  const ref = (gr.reference_formula ?? "").trim(), refF = ref.startsWith("=") ? ref : "=" + ref;
  const mk = (id: string, text: string, tb: Table[]): SheetScript => ({ id, content: `${cell}: ${text}\n`, sheets: tb.map((t) => ({ name: sheetName(t.name), columns: t.columns.map((c) => c.name), rows: t.rows })), probes });
  const n = tables[0].rows.length, cands = n ? [[{ op: "drop_row", index: 0 }], [{ op: "duplicate_row", index: n - 1 }], [{ op: "drop_row", index: n - 1 }]] : [];
  const scripts = [mk("base", f, tables)];
  if (gr.forbid_hardcoded_values !== false && ref) cands.forEach((ops, k) => {
    const tb = mutated(tables, { table: tables[0].name, ops });
    scripts.push(mk(`l${k}`, f, tb), mk(`r${k}`, refF, tb));
  });
  const res = await ctx.engine({ scripts });
  const parts: Record<string, boolean> = {}, failed: string[] = [];
  const bad = (id: string) => { parts[id] = false; failed.push(id); };
  const base = value(res.base, "v");
  const okValue = !base.why && deepEqual(base.got, gr.expected_value, Number(gr.tolerance ?? 1e-9));
  parts.value = okValue; if (!okValue) failed.push("value");
  const fns = cellFunctions(`${cell}: ${f}`, cell);
  if (gr.must_use_functions?.length) { const ok = !!fns && gr.must_use_functions.every((x: string) => fns.has(x.toUpperCase())); parts.functions = ok; if (!ok) failed.push("functions"); }
  cands.forEach((_o, k) => {
    if (!res[`l${k}`]) return;
    const a = value(res[`l${k}`], "v"), b = value(res[`r${k}`], "v");
    if (a.why || b.why || !deepEqual(a.got, b.got, Number(gr.tolerance ?? 1e-9))) bad(`data_${k}`); else parts[`data_${k}`] = true;
  });
  const fb = !okValue ? "That formula does not give the expected value." : failed.includes("functions") ? `Use ${gr.must_use_functions.join(", ")} in your formula.` : failed.length ? "Your formula gives the right value here but not when the data changes: use cell references, not typed-in numbers." : null;
  return { correct: failed.length === 0, feedback: fb, parts, failed };
}
