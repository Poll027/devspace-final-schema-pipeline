// Every finished SQL exercise: its authored solution must pass the grader, its starter and a constant query must fail.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { gradeSql, splitStatements } from "../src/sql.ts";
import { sqlEngine } from "./node-engines.ts";

const BATCHES = join(import.meta.dirname, "..", "..", "batches");
const entryOf = (pub: any) => pub.workspace.entry ?? pub.workspace.files.find((f: any) => f.role === "editable")?.path ?? pub.workspace.files[0].path;

test("splitStatements ignores semicolons in strings and comments", () => {
  assert.deepEqual(splitStatements("SELECT 'a;b' AS x; -- c;d\nSELECT 2 /* ; */;"), ["SELECT 'a;b' AS x", "-- c;d\nSELECT 2".replace("-- c;d\n", "")]);
});

let n = 0;
for (const b of readdirSync(BATCHES)) {
  const f = join(BATCHES, b, "interactions.json"), r = join(BATCHES, b, "scenario_asset_registry.json");
  if (!existsSync(f) || !existsSync(r)) continue;
  const registry = JSON.parse(readFileSync(r, "utf8"));
  for (const t of JSON.parse(readFileSync(f, "utf8")).tiles) for (const x of t.interactions) {
    const i = x.interaction;
    if (i.type !== "code_exercise" || i.public.runtime.kind !== "sql") continue;
    const entry = entryOf(i.public);
    const solution = i.grading.solution_files.find((s: any) => s.path === entry).content;
    const starter = i.public.workspace.files.find((s: any) => s.path === entry).content;
    test(`${b} ${i.interaction_id}: solution passes, starter and SELECT 1 fail`, async () => {
      n++;
      const ok = await gradeSql(i, solution, { registry, engine: sqlEngine });
      assert.equal(ok.correct, true, JSON.stringify(ok.failed));
      assert.equal((await gradeSql(i, starter, { registry, engine: sqlEngine })).correct, false, "starter passes");
      assert.equal((await gradeSql(i, "SELECT 1", { registry, engine: sqlEngine })).correct, false, "constant passes");
    });
  }
}
