# Stage 08 — Independent pedagogy review

Batch: `final_batch_persistence`

VERDICT: PASS

Blocking defects: 0. Advisory findings: 9.

## Scope and method

Reviewed all 12 tiles, rather than sampling, including their explanation blocks, visuals, checks, practice prompts, feedback and remediation. Independently consulted `inputs/path_glossary_bundle.json` (required facts and teaching intent) and `scenario_asset_registry.json` (order fields, identities, policies and exercise contracts). Applied the stage evaluator and Playbook §§2, 3 and 5. Did not read generator reasoning or rerun deterministic gates.

This is a lesson-JSON review. No rendered screenshots or playable video inspection were available in the reviewed inputs; visual judgements concern authored labels, code, edges and tables, and video judgements concern the supplied segment summaries and bridges, not an independently watched clip. No execution-environment requirement was imposed on inspect-and-judge practice. The fixed step plan was respected.

## Learner-journey assessment

| Tile | Steps / estimated minutes | Assessment |
|---|---:|---|
| tile_061 | 12 / 7.9 | Identity versus conditional retrieval is taught before checks and application. Transaction scope and standalone failed-flush recovery are explicitly distinguished. Some opening explanation repeats rather than advances. |
| tile_063 | 5 / 3.4 | Extraction, missing/malformed cases and validity distinction precede assessment. The code annotation explicitly covers empty Bearer input. Shorter than the review's pacing target. |
| tile_064 | 6 / 6.1 | Authority, miss population, eligibility and result-specific keys precede judgement and practice. The profile-video example transfers the sequence to another domain; text stands alone. |
| tile_065 | 10 / 7.8 | Migration reversal versus data recovery is explained before review-only practice. Index workload and cost precede declaration. The review visual is mostly comments rather than a concrete candidate. |
| tile_067 | 13 / 11.0 | Public field selection, failed-transaction recovery and shared HTTP envelopes have separate explain/check/apply sequences. Registered public fields, fixed reasons, status and relevant headers agree with the lesson. |
| tile_070 | 6 / 4.4 | Sender-based trust, wildcard restriction and stripped-prefix configuration are taught before checks. Adapter-based practice clearly states its verification boundary. Shorter than target. |
| tile_071 | 5 / 3.7 | Typed validation, acknowledgment versus completion, and task registration are taught before application. Media-type enforcement is supplied rather than an unexplained learner implementation requirement. Shorter than target. |
| tile_072 | 8 / 7.2 | Request-local correlation precedes practice. Frequency, fraction and duration precede aligned-window comparison. The classification excerpts contain the values necessary to make one defensible judgement for each item. |
| tile_074 | 9 / 7.1 | Ordering, page arithmetic and numeric bounds precede pagination practice. Bound values versus allowlisted structure precedes the injection check. Remediation includes a worked offset example. |
| tile_076 | 13 / 10.5 | Creation, deletion and partial update each receive explanation and independent-verification practice. Examples agree with registered target and comparison identities. The update walkthrough needs an earlier fixture-specific label. |
| tile_079 | 7 / 4.4 | Readable claims, required presence, configured verification and time constraints precede checks. The verification code shows rejection rather than unverified fallback. Shorter than target. |
| tile_080 | 10 / 8.9 | TTL meanings and invalidation precede freshness practice; cache-boundary failure policy precedes failure practice. Video adds the missed-invalidation/expiry safety-net scenario. |

No question was found to require an untaught idea for success. Related mechanics on a single explainer are explicitly stated and visually separated; no hidden second teaching objective was found. Wrong-option feedback addresses the actual misconception. General feedback and hint ladders are often boilerplate, but specific option/item feedback prevents that from being a blocking remediation failure. Authored visuals support the text without a discovered contradiction. The short tiles' pacing deviations are advisory, not evidence that learners cannot succeed; do not add steps contrary to the fixed plan merely to reach a count.

## Findings

ADVISORY tile_061/s02-s03: Two consecutive explainers restate identity-versus-selection absence, and s03 asks learners to trace cases without showing the trace outcomes → retain the fixed steps, but make s03 a concrete mini-trace: `get(Order, 42) → Order 42; get(Order, 999) → None; a condition with no matching rows → []; handle either absence before entity use.` Keep the bounded queued selection as the contrasting condition.

ADVISORY tile_063/s01-s05: Five steps and 3.4 estimated minutes fall below the 8–14-step/about-6–12-minute review target → keep the fixed plan; either identify this as an intentionally short tile or enrich s02 with a compact four-input/handler-reached table and re-estimate duration from learner testing rather than adding filler.

ADVISORY tile_064/s01-s06: Six steps fall below the review's step-count target, although the 6.1-minute estimate is within its time target → document the compact single-concept exception; preserve the planned sequence and do not add redundant steps solely to reach eight.

ADVISORY tile_065/s01: The code walkthrough contains only pass statements and comments describing a possible drop/add, so it adds little concrete evidence beyond the prose → keep the visual block but show the review-only candidate with named fields (`orders.note` and `orders.customer_note`) and annotate the data-loss points in both directions; explicitly label it `Candidate excerpt — do not execute`.

ADVISORY tile_070/s01-s06: Six steps and 4.4 estimated minutes are below the review pacing target → retain the fixed plan and mark a short-tile exception, or enrich s02 with a trusted-versus-untrusted sender observation pair and re-estimate actual reading/practice time.

ADVISORY tile_071/s01-s05: Five steps and 3.7 estimated minutes are below the review pacing target → retain the fixed plan and mark a short-tile exception, or use s02 to show an accepted body, missing-field body and unsupported-media observation side by side before application.

ADVISORY tile_076/s09: The walkthrough is named generically `update` and permits note/quantity assignments, but its final assertions assume a note-only update with omitted quantity; s10 supplies that scope only afterward → add immediately before the code: `This walkthrough uses a note-only change for Order 42; quantity is omitted and must remain unchanged.` Rename the sample function `update_note_only` to make the example scope visible.

ADVISORY tile_076/s12: The two generic hints do not help locate mistakes in the partial-update lifecycle → replace them with `Use model_dump(exclude_unset=True) and assign only permitted supplied fields; do not copy defaults for omitted quantity.` and `After commit, reload in the independent session and compare the new note and original quantity; on failure, roll back before reuse.`

ADVISORY tile_079/s01-s07: Seven steps and 4.4 estimated minutes are below the review pacing target, and s03 lists fixture cases without showing their outcomes → retain the fixed plan; make s03 a compact valid/rejected fixture trace, then re-estimate time or document an intentionally short tile.

VERDICT: PASS
