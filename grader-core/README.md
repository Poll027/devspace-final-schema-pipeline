# grader-core

One grader for every tile interaction, shared by the player, the backend and the pipeline's checks. Zero dependencies; TypeScript runs natively on Node 22.18+.

```ts
import { gradeInteraction } from "./src/index.ts";
const r = await gradeInteraction(interaction, submission, { registry, sql, py, sheet });
// r = { correct: boolean | null, score: 0..1, feedback: string | null, parts, needs? }
```

Submissions: `choice {selected[]}`, `ordering {order[]}`, `classify {assignments}`, `match_pairs {pairs}`, `short_answer {text}`, `table_select {answers}`, `field_selection {selected[]}`,
`diagram_label {placements}`, `find_issues {flags[]}`, `code_exercise {code}` (the entry file's text), `formula_entry {formula}`. `external_proof` returns `needs: "review"`.

Code engines are injected, not bundled: `sql` (DuckDB-WASM), `py` (Pyodide + the pipeline's harness in `00_FINAL_PIPELINE_CORE/sandbox/run_py.mjs`), `sheet` (HyperFormula).
Each takes the job shape documented at the top of `sandbox/run_sql.mjs`, `run_py.mjs`, `run_sheet.mjs` and returns the same results. A missing engine returns `needs: "runtime"`.

The comparison rules are ports of the pipeline's reference graders (`scripts/checkers/sandbox.py`: `grade_learner`, `grade_learner_py`, `grade_learner_sheet`); the tests replay every finished lesson's authored answer
(`npm test`). Known gaps: python/sheet `forbidden_syntax` tests come back in `unchecked` (they need a parser); the player's Pyodide must apply the `boxplot(tick_labels=)` alias from `run_py.mjs`.
