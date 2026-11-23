# Stage 08 — Independent pedagogy review

## Scope and method

Reviewed all five tiles (tile_054, tile_055, tile_056, tile_058, tile_059), including their explainers, video summaries/bridges, questions, code starters, test cases, feedback and remediation text. Although later batches permit a risk-based third, this five-tile batch was reviewed in full.

Sources: `tile_lessons/*.json`, `inputs/path_glossary_bundle.json` (all seven concepts), and `scenario_asset_registry.json` (synthetic scenarios, models, routes and controlled request cases). Applied the stage evaluator instructions and Playbook §§2–5 concerning text-first teaching, the learner-facing sequence and remediation. No generator reasoning or previous evaluation reports were consulted; deterministic gates were not rerun. No reference-player screenshots were available in the batch, so visual judgments concern authored content, not rendered layout. Actual completion times were not measured.

## Findings by learner journey

| Tile | Journey assessment | Authored pacing |
|---|---|---|
| tile_054 | All metadata mechanisms are explained before selection and implementation. The quantity-2 sample agrees with the positive bound and existing return-only route. Three introductory screens mostly repeat the same example; the first contains several explicitly explained mechanisms. | 6 steps; 3.9 min |
| tile_055 | Callable mapping, HTTP observation and restoration are taught before active/restored-provider checks and implementation. The video bridge correctly identifies the clip's missing assertion and cleanup rather than presenting it as a complete test. | 6 steps; 7.7 min |
| tile_056 | Each concept has explain → check → apply progression. Header case/name mapping, cookie omission and invalid-request/server-bug distinctions support the checks. The code starters preserve the registry's contracts. | 7 steps; 6.9 min |
| tile_058 | Registration, labels, known requests and measurement boundaries precede the boundary check and implementation. Output distinguishes returned 400 responses from escaping 500 exceptions consistently with the glossary and fixture. The large evidence display dominates a short tile. | 5 steps; 4.2 min |
| tile_059 | Supplied-field intent is explained, checked and exercised before compatibility review. The omitted/null/string cases and old/revised requiredness comparisons are consistent with the registry. Compatibility evidence is relevant but overly concentrated in one screen. | 10 steps; 9.6 min |

No BLOCKING defects found. Questions have defensible keys derivable from preceding text; wrong-option explanations are accurate. Remediation text addresses the relevant distinctions, although generic code-failure messages could guide diagnosis better. Multiple mechanisms in some explainers are explicitly taught, not hidden prerequisites, so the load concerns below are ADVISORY. The synthetic retrieval-shaped schema illustration in tile_059 does not require understanding persistence or the later retrieval concept. Visual/code evidence supports the subject matter and does not contradict it.

## Defects and exact recommended changes

ADVISORY tile_054/s01: The tile has only six steps and a 3.9-minute estimate, below the 8–14-step/about 6–12-minute guidance, while the first screen bundles schema examples, validation, named body examples and decorator metadata → Replan into separate short explainers for validated schema examples, named Body examples, and descriptive metadata; add a quantity-0 versus quantity-2 validation check and a named-example placement check before the existing hands-on. Repurpose the repetitive s03 prose instead of adding filler, and reassess the estimate after the split.

ADVISORY tile_055/s01: All setup, observation and cleanup teaching is concentrated in the first screen of a six-step tile → Split provider mapping/HTTP assertion from saving/restoring the previous dictionary; add a short check asking why restoring a saved nonempty dictionary differs from resetting to {}, bringing the journey to eight steps without introducing another concept.

ADVISORY tile_055/s05: The editable main.py places a lengthy no-threads TestClient adapter before the learner's small override task → Move the adapter and override_probe support into a supplied read-only support file imported by main.py, or collapse that region by default. Keep app/providers and the three TODO operations visible together; state that the adapter is not part of the learner task.

ADVISORY tile_056/s01: A seven-step tile puts explicit source selection, header-name controls and cookie omission into one initial screen with a long code listing → Split explicit Header/Cookie source selection from header-name mapping and alias controls, retaining the explanations before s02 and the omission explanation before s03. This gives eight steps while preserving the existing two explain/check/apply sequences.

ADVISORY tile_056/s06: The request/assertion task is visually buried under the sandbox TestClient adapter and followed by an AST-checking scaffold → Place the adapter and checked_invalid_probe implementation in read-only support files or collapsed regions. Show the unchanged model/route, supplied expectations and invalid_probe TODO body as the main editable view; explain that only the request and three equality assertions need editing.

ADVISORY tile_058/s01: A five-step, 4.2-minute tile front-loads registration, label policy, counters, histogram semantics and a large before/after output into one screen → Replan the evidence into focused registration/labels, counter-delta, duration-count/sum, and escaping-exception screens, with a brief interpretation check. Show only the relevant output rows on each screen while retaining the full computed output as expandable evidence; reassess the estimate toward 6–12 minutes.

ADVISORY tile_058/s04: Two very large encoded package wheels appear inside the learner's editable main.py ahead of the two registration TODOs → Move wheel provisioning to a read-only runtime bootstrap asset or support file and import it before the package imports. Collapse the supplied metrics harness; open the editor at the middleware and metrics-route TODOs so no encoded bytes need to be read or edited.

ADVISORY tile_058/s04: Every code-test failure uses the same generic contract-comparison message despite checking different measurement boundaries → Replace the success-case failure message with 'For /success, check middleware registration and the /metrics/ route; request, response and duration counts should each increase by one.' Use the corresponding route name for /expected-error; for /delayed add 'Check that the duration sum includes the controlled delay'; for /escaping-exception use 'The request and response counters should increase, but the duration count must not.' Preserve the existing remediation link.

ADVISORY tile_059/s06: The screen presents three compatibility dimensions alongside a roughly 80-line evidence generator and verbose JSON output, making the learner hunt for the relevant differences → Split requiredness, tightened quantity constraints and removed public fields/operations into three focused explainers before s07–s09. Display each pair's compact result next to its declaration, with the full executed generator/output expandable. This raises the tile to twelve steps without adding untaught ideas.

ADVISORY tile_059/s03: The video repeats supplied-only extraction already explained twice; its different title/content vocabulary is not used for an active transfer task → Add this observation prompt before playback: 'When only title is supplied, which field must be absent from the extracted update? Map title to quantity and content to note in our example.' After playback ask 'Does this clip establish what happens when note=None is explicitly supplied?' and direct the learner back to the text's null comparison. Keep the frozen segment and existing boundary bridge unchanged.

## Verdict

VERDICT: PASS

Review completed independently. Content has no identified blocking pedagogical defect; the ten advisory changes above concern pacing, visual reading load, scaffolding presentation, diagnostic feedback and video activity.
