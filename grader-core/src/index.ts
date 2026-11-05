// grader-core: grade(interaction, submission) -> Result. Pure functions, no I/O, no dependencies.
// `interaction` is one entry of interactions.json (its `public` + `grading`); the player only ever sees `public`.
// Rows/cells are identified the way the lessons identify them: {where:{col:val}, occurrence?, column?}.

export type Result = {
  correct: boolean | null;          // null = cannot be decided here (needs a runtime or a human/AI reviewer)
  score: number;                    // 0..1, share of the parts answered correctly
  feedback: string | null;          // message authored for this exact mistake, when the lesson has one
  parts?: Record<string, boolean>;  // per-option / per-item / per-task result
  needs?: "runtime" | "review";
};

const ok = (feedback: string | null = null, parts?: Record<string, boolean>): Result => ({ correct: true, score: 1, feedback, parts });
const no = (feedback: string | null, score = 0, parts?: Record<string, boolean>): Result => ({ correct: false, score, feedback, parts });
const sameSet = (a: string[], b: string[]) => a.length === b.length && new Set(a).size === a.length && a.every((x) => b.includes(x));
const canon = (r: { where?: Record<string, unknown>; occurrence?: number; column?: string }) =>
  JSON.stringify([Object.entries(r.where ?? {}).sort(([a], [b]) => (a < b ? -1 : 1)), r.occurrence ?? 0, r.column ?? null]);
const share = (parts: Record<string, boolean>) => { const v = Object.values(parts); return v.length ? v.filter(Boolean).length / v.length : 0; };

function choice(i: any, s: { selected: string[] }): Result {
  const right: string[] = i.grading.correct_option_ids, picked = s.selected ?? [];
  if (sameSet(picked, right)) return ok();
  const wrong = picked.find((id) => !right.includes(id)) ?? picked[0];
  const fb = i.grading.option_feedback?.[wrong]?.message ?? null;
  return no(fb, right.filter((x) => picked.includes(x)).length / right.length, Object.fromEntries(picked.map((id) => [id, right.includes(id)])));
}

function ordering(i: any, s: { order: string[] }): Result {
  const accepted: string[][] = [i.grading.correct_order, ...(i.grading.accepted_alternatives ?? [])];
  if (accepted.some((o) => JSON.stringify(o) === JSON.stringify(s.order))) return ok();
  const best = accepted[0];
  const parts = Object.fromEntries(best.map((id, k) => [id, s.order?.[k] === id]));
  return no(i.grading.loop_back_note ?? null, share(parts), parts);
}

function classify(i: any, s: { assignments: Record<string, string> }): Result {
  const want: Record<string, string> = i.grading.assignments;
  const parts = Object.fromEntries(Object.keys(want).map((it) => [it, s.assignments?.[it] === want[it]]));
  if (Object.values(parts).every(Boolean)) return ok(null, parts);
  const firstBad = Object.keys(parts).find((k) => !parts[k])!;
  return no(i.grading.item_feedback?.[firstBad]?.message ?? null, share(parts), parts);
}

function matchPairs(i: any, s: { pairs: { left: string; right: string }[] }): Result {
  const key = (p: { left: string; right: string }) => `${p.left}\u0000${p.right}`;
  const given = new Set((s.pairs ?? []).map(key));
  const parts = Object.fromEntries(i.grading.pairs.map((p: any) => [p.left, given.has(key(p))]));
  return Object.values(parts).every(Boolean) && given.size === i.grading.pairs.length ? ok(null, parts) : no(null, share(parts), parts);
}

function shortAnswer(i: any, s: { text: string | number }): Result {
  const g = i.grading, raw = String(s.text ?? "").trim();
  const fold = (x: string) => (g.case_sensitive ? x.trim() : x.trim().toLowerCase());
  if ((g.accepted_answers ?? []).some((a: string) => fold(a) === fold(raw))) return ok();
  if (g.numeric && raw !== "" && Math.abs(Number(raw) - g.numeric.value) <= (g.numeric.tolerance ?? 0)) return ok();
  return no(null);
}

function tableSelect(i: any, s: { answers: Record<string, { row?: any; column?: string }> }): Result {
  const parts: Record<string, boolean> = {};
  let fb: string | null = null;
  for (const a of i.grading.answers) {
    const g = s.answers?.[a.task_id] ?? {};
    const rowOk = a.row === undefined || (g.row !== undefined && canon(g.row) === canon(a.row));
    const colOk = a.column === undefined || g.column === a.column;
    parts[a.task_id] = rowOk && colOk;
    if (!parts[a.task_id] && fb === null) fb = i.grading.task_feedback?.[a.task_id]?.incorrect ?? null;
  }
  return Object.values(parts).every(Boolean) ? ok(null, parts) : no(fb, share(parts), parts);
}

function fieldSelection(i: any, s: { selected: string[] }): Result {
  const rules: { field_id: string; role: string }[] = i.grading.rules, picked = new Set(s.selected ?? []), m = i.grading.outcome_messages ?? {};
  if (rules.some((r) => r.role === "required" && !picked.has(r.field_id))) return no(m.missing_required ?? null);
  if (rules.some((r) => r.role === "forbidden" && picked.has(r.field_id))) return no(m.includes_forbidden ?? null);
  if (rules.some((r) => r.role === "unneeded" && picked.has(r.field_id))) return no(m.includes_unneeded ?? null, 0.5);
  return ok(m.ok ?? null);
}

function diagramLabel(i: any, s: { placements: Record<string, string> }): Result {
  const want: Record<string, string> = i.grading.placements;
  const parts = Object.fromEntries(Object.keys(want).map((k) => [k, s.placements?.[k] === want[k]]));
  return Object.values(parts).every(Boolean) ? ok(null, parts) : no(null, share(parts), parts);
}

// flags: what the learner marked. Each {location: cell_ref, category_id}. Decoys are cells that look wrong but are fine.
function findIssues(i: any, s: { flags: { location: any; category_id?: string }[] }): Result {
  const g = i.grading, flags = s.flags ?? [];
  const parts: Record<string, boolean> = {};
  let fb: string | null = null;
  for (const issue of g.issues) {
    const hit = flags.find((f) => issue.locations.some((l: any) => canon(l) === canon(f.location)));
    parts[issue.issue_id] = !!hit && (hit.category_id === undefined || hit.category_id === issue.category_id);
    if (hit && !parts[issue.issue_id] && fb === null) fb = g.wrong_category_message ?? null;
  }
  for (const d of g.decoys ?? []) {
    if (flags.some((f) => canon(f.location) === canon(d.location))) { parts[`decoy:${canon(d.location)}`] = false; fb ??= d.message; }
  }
  const allOk = Object.values(parts).every(Boolean) && flags.length === g.issues.length;
  return allOk ? ok(g.completion_message ?? null, parts) : no(fb, share(parts), parts);
}

// Code exercises and formulas need a runtime (SQL/Python/chart/sheet); a human or AI rubric grades external proof.
export function grade(interaction: any, submission: any): Result {
  const i = interaction.interaction ?? interaction;
  switch (i.type) {
    case "choice": return choice(i, submission);
    case "ordering": return ordering(i, submission);
    case "classify": return classify(i, submission);
    case "match_pairs": return matchPairs(i, submission);
    case "short_answer": return shortAnswer(i, submission);
    case "table_select": return tableSelect(i, submission);
    case "field_selection": return fieldSelection(i, submission);
    case "diagram_label": return diagramLabel(i, submission);
    case "find_issues": return findIssues(i, submission);
    case "external_proof": return { correct: null, score: 0, feedback: null, needs: "review" };
    case "code_exercise": case "formula_entry": return { correct: null, score: 0, feedback: null, needs: "runtime" };
    default: throw new Error(`grader-core: unknown interaction type ${i.type}`);
  }
}
