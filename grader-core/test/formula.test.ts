// Every finished formula_entry: its reference formula passes; a typed-in answer, a wrong function, and no '=' fail. Also routes through gradeInteraction.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { gradeInteraction } from "../src/index.ts";
import { sheetEngine } from "./node-engines.ts";

const BATCHES = join(import.meta.dirname, "..", "..", "batches");
for (const b of readdirSync(BATCHES)) {
  const f = join(BATCHES, b, "interactions.json"), r = join(BATCHES, b, "scenario_asset_registry.json");
  if (!existsSync(f) || !existsSync(r)) continue;
  const registry = JSON.parse(readFileSync(r, "utf8"));
  for (const t of JSON.parse(readFileSync(f, "utf8")).tiles) for (const x of t.interactions) {
    const i = x.interaction;
    if (i.type !== "formula_entry") continue;
    const ctx = { registry, sheet: sheetEngine };
    test(`${b} ${i.interaction_id}: reference passes; typed-in value, empty and no '=' fail`, async () => {
      const ok = await gradeInteraction(i, { formula: i.grading.reference_formula }, ctx) as any;
      assert.equal(ok.correct, true, JSON.stringify(ok));
      const typed = await gradeInteraction(i, { formula: `=${JSON.stringify(i.grading.expected_value)}` }, ctx) as any;
      assert.equal(typed.correct, false, "typed-in value passes");
      assert.equal(((await gradeInteraction(i, { formula: "" }, ctx)) as any).correct, false);
      assert.equal(((await gradeInteraction(i, { formula: String(i.grading.reference_formula).replace(/^=/, "") }, ctx)) as any).correct, false);
    });
  }
}
test("a missing engine says so instead of guessing", async () => {
  const r = await gradeInteraction({ type: "code_exercise", public: { runtime: { kind: "sql" } } }, { code: "SELECT 1" }, {});
  assert.equal(r.correct, null);
});
