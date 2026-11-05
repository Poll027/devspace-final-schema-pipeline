// Replays every finished tile's authored answer key through grade(): the authored correct answer must pass,
// and a deliberately wrong answer must fail (choice: with the lesson's own feedback for that option).
import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { grade } from "../src/index.ts";

const BATCHES = join(import.meta.dirname, "..", "..", "batches");
const correct = (i: any): any => {
  const g = i.grading;
  switch (i.type) {
    case "choice": return { selected: g.correct_option_ids };
    case "ordering": return { order: g.correct_order };
    case "classify": return { assignments: g.assignments };
    case "match_pairs": return { pairs: g.pairs };
    case "short_answer": return { text: g.accepted_answers?.[0] ?? String(g.numeric?.value) };
    case "table_select": return { answers: Object.fromEntries(g.answers.map((a: any) => [a.task_id, { row: a.row, column: a.column }])) };
    case "field_selection": return { selected: g.rules.filter((r: any) => r.role !== "unneeded" && r.role !== "forbidden").map((r: any) => r.field_id) };
    case "diagram_label": return { placements: g.placements };
    case "find_issues": return { flags: g.issues.map((x: any) => ({ location: x.locations[0], category_id: x.category_id })) };
  }
};
const wrong = (i: any): any => {
  const g = i.grading;
  switch (i.type) {
    case "choice": return { selected: [] };
    case "ordering": return { order: [...g.correct_order].reverse() };
    case "classify": return { assignments: {} };
    case "table_select": return { answers: {} };
    case "find_issues": return { flags: [] };
    case "match_pairs": return { pairs: [] };
    case "diagram_label": return { placements: {} };
    default: return undefined;
  }
};

let seen = 0, wrongSeen = 0;
for (const b of readdirSync(BATCHES).filter((x) => x.startsWith("final_batch_"))) {
  const f = join(BATCHES, b, "interactions.json");
  if (!existsSync(f)) continue;
  for (const t of JSON.parse(readFileSync(f, "utf8")).tiles) for (const x of t.interactions) {
    const i = x.interaction, c = correct(i);
    if (c === undefined) continue;
    test(`${b} ${i.interaction_id}: authored answer passes`, () => { assert.equal(grade(i, c).correct, true); seen++; });
    const w = wrong(i);
    if (w !== undefined) test(`${b} ${i.interaction_id}: wrong answer fails`, () => { assert.equal(grade(i, w).correct, false); wrongSeen++; });
    if (i.type === "choice") for (const [opt, v] of Object.entries<any>(i.grading.option_feedback ?? {}).filter(([o]) => !i.grading.correct_option_ids.includes(o))) {
      test(`${b} ${i.interaction_id}: option ${opt} gives its authored feedback`, () => {
        const r = grade(i, { selected: [opt] });
        assert.equal(r.correct, false); assert.equal(r.feedback, v.message);
      });
    }
  }
}
test("something was checked", () => assert.ok(seen > 0 && wrongSeen > 0));
