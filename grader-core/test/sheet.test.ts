// Every finished spreadsheet exercise: authored solution passes; starter and an empty sheet fail.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { gradeSheet, applyCellVar, cellFunctions } from "../src/sheet.ts";
import { sheetEngine } from "./node-engines.ts";

const BATCHES = join(import.meta.dirname, "..", "..", "batches");

test("applyCellVar edits only a typed constant; cellFunctions reads formulas", () => {
  assert.equal(applyCellVar("A1: 5\nB1: =SUM(A1)\n", "A1", 9), "A1: 9\nB1: =SUM(A1)\n");
  assert.equal(applyCellVar("B1: =SUM(A1)\n", "B1", 3), "B1: =SUM(A1)\n");
  assert.deepEqual([...cellFunctions('C2: =ROUND(AVERAGE(A1:A3), 2) & ")"\n', "C2")!].sort(), ["AVERAGE", "ROUND"]);
});

for (const b of readdirSync(BATCHES).filter((x) => x.startsWith("final_batch_"))) {
  const f = join(BATCHES, b, "interactions.json"), r = join(BATCHES, b, "scenario_asset_registry.json");
  if (!existsSync(f) || !existsSync(r)) continue;
  const registry = JSON.parse(readFileSync(r, "utf8"));
  for (const t of JSON.parse(readFileSync(f, "utf8")).tiles) for (const x of t.interactions) {
    const i = x.interaction;
    if (i.type !== "code_exercise" || i.public?.runtime?.kind !== "spreadsheet") continue;
    const ws = i.public.workspace, entry = ws.entry ?? ws.files.find((f: any) => f.role === "editable")?.path ?? ws.files[0].path;
    const solution = i.grading.solution_files.find((s: any) => s.path === entry).content;
    const starter = ws.files.find((s: any) => s.path === entry).content;
    test(`${b} ${i.interaction_id}: solution passes, starter and empty sheet fail`, async () => {
      const ok = await gradeSheet(i, solution, { registry, engine: sheetEngine });
      assert.equal(ok.correct, true, JSON.stringify({ failed: ok.failed, feedback: ok.feedback }));
      assert.equal((await gradeSheet(i, starter, { registry, engine: sheetEngine })).correct, false, "starter passes");
      assert.equal((await gradeSheet(i, "", { registry, engine: sheetEngine })).correct, false, "empty sheet passes");
    });
  }
}
