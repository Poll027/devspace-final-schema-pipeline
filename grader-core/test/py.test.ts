// Every finished Python and chart exercise: the authored solution passes the grader; the starter and an empty program fail.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { gradePython, applyVar } from "../src/py.ts";
import { pyEngine } from "./node-engines.ts";

const BATCHES = join(import.meta.dirname, "..", "..", "batches");
const only = process.env.KIND;  // python | chart_renderer (default: both)

test("applyVar replaces only the named top-level constant", () => {
  assert.equal(applyVar('n = 5  # c\nm = 5\n', "n", 9), "n = 9  # c\nm = 5\n");
  assert.equal(applyVar('s = "a"\n', "s", "a_x"), 's = "a_x"\n');
  assert.equal(applyVar("x = f(1)\n", "x", 3), "x = f(1)\n");
});

for (const b of readdirSync(BATCHES).filter((x) => x.startsWith("final_batch_"))) {
  const f = join(BATCHES, b, "interactions.json"), r = join(BATCHES, b, "scenario_asset_registry.json");
  if (!existsSync(f) || !existsSync(r)) continue;
  const registry = JSON.parse(readFileSync(r, "utf8"));
  for (const t of JSON.parse(readFileSync(f, "utf8")).tiles) for (const x of t.interactions) {
    const i = x.interaction, kind = i.public?.runtime?.kind;
    if (i.type !== "code_exercise" || !["python", "chart_renderer"].includes(kind) || (only && only !== kind)) continue;
    const ws = i.public.workspace, entry = ws.entry ?? ws.files.find((f: any) => f.role === "editable")?.path ?? ws.files[0].path;
    const solution = i.grading.solution_files.find((s: any) => s.path === entry).content;
    const starter = ws.files.find((s: any) => s.path === entry).content;
    test(`${b} ${i.interaction_id} (${kind}): solution passes, starter and empty program fail`, async () => {
      const ok = await gradePython(i, solution, { registry, engine: pyEngine });
      assert.equal(ok.correct, true, JSON.stringify({ failed: ok.failed, feedback: ok.feedback }));
      assert.equal((await gradePython(i, starter, { registry, engine: pyEngine })).correct, false, "starter passes");
      assert.equal((await gradePython(i, "pass\n", { registry, engine: pyEngine })).correct, false, "empty program passes");
    });
  }
}
