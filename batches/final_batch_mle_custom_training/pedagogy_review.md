# Stage 08 — Independent pedagogy review

## Scope and method

Reviewed all seven tiles as learner journeys (the conservative all-tile/canary scope): main steps, learner-facing interaction evidence, independently derived answers, option/item feedback, linked remediation, code/diagram/table blocks, recap, and video bridges. Sources were `tile_lessons/*.json`, `inputs/path_glossary_bundle.json` (required facts, teaching blocks, prerequisites, practice/visual anchors and media descriptions), and `scenario_asset_registry.json`. No generator reasoning, repair scripts, earlier review claims, or deterministic gate results were used. The stage evaluator cites no additional playbook sections.

No screenshots/reference-player renderings were present in this batch. Visual judgments concern the authored content, not verified layout. Video judgments use the supplied segment descriptions and bridges; playback/transcripts were not independently available. No execution lab, runtime, VM, checkpoint or submission route is required for the inspect-and-judge practice.

## Result

**VERDICT: PASS** — 0 BLOCKING defects; 10 ADVISORY findings. Advisory-only content receives PASS under the dispatch classification rule.

| Tile | Journey assessment | Main steps / declared minutes |
|---|---|---|
| mle.tile.035_037 | Separate tensor contracts → pairing/boundaries → model widths; checks and applications are teachable. Dense first walkthrough and redundant transitions. | 16 / 11.4 |
| mle.tile.038_040 | Fresh matrix gradients → task/reduction contracts → restricted plain-SGD update; feedback distinguishes the tested mistakes. Long video and accumulated reading burden. | 19 / 18.9 |
| mle.tile.041_043 | Per-batch updates → independent mode/recording controls → compatible persistence; sound evidence and remediation. Dense code and repeated explanations extend pacing. | 18 / 14.1 |
| mle.tile.044_045 | Accepted-checkpoint controller → isolated diagnosis; table and scalar example support the judgments. Minor numerical presentation burden. | 12 / 8.1 |
| mle.tile.046_048 | Placement/lifecycle → eligible batch sizing → live-memory diagnosis; distinctions and wrong-choice explanations are sound. Wide trial table is hard to scan. | 18 / 12.2 |
| mle.tile.049_050 | Attribution versus final timing → matched hardware and scoped cost; evidence supports both judgments. Hardware table presents too many fields together. | 11 / 8.1 |
| mle.tile.051_051 | Adaptation → supervised verification → conditional validation cost; all assessed criteria appear before checks. First visual anticipates later explanations and final application is disproportionately dense. | 7 / 4.9 |

## Substantive checks

- No check requires an untaught decision. Related implementation syntax in setup does not require understanding a later concept to answer the questions.
- Re-derived tensor/loader/model judgments from separate dtype/shape contracts, same-index correspondence, incomplete-batch policy, and per-observation widths.
- Re-derived fresh-gradient, loss-reduction and SGD judgments from the supplied equations and restrictions; neither scalar-loss completion nor shape alone establishes numerical correctness.
- Mode feedback correctly separates evaluation behavior from graph recording, including the dropout identity exception concerning an existing input's `requires_grad` flag.
- Early stopping's accepted checkpoint at 0.44 is supported by the glossary teaching blocks' explicit interpretation of `best` and the registry trace; 0.43 is insufficient under strict `min_delta=0.02`.
- Batch-size 100 is the highest-throughput eligible trial. CPU has the lower eligible lifecycle compute cost (0.9 versus 2.0). Embedded evidence agrees with registry rows; stopped compute is not represented as ending all charges.
- Fine-tuning cost comparisons use actual-negative/actual-positive denominators and the supplied probability/cost weights: reference 0.5 versus adapted 0.25. The gradient-reference transpose and two-image verification batch are explicitly distinguished from the four-image shape fixture.
- Item-specific feedback and linked remediation address the actual distractors, rather than requiring unprovided executed evidence. Authored memory/profiling records are judged as fictional read-only evidence, not real runtime measurements.
- No authored visual contradicts the accompanying text. The autograd clip adds a concrete computation-graph trace and the disabled-tracking contrast. The mode clip mainly repeats existing instruction and would benefit from a sharper observation task.

## Findings and fixes

ADVISORY mle.tile.035_037/s01: Three prose blocks plus a 57-line reveal-all walkthrough create a heavy first screen before the learner's first check → Keep the aligned_pair function visible first; group the accepted, single-row and rejected fixtures into separately revealed code sections, with a one-sentence shape/dtype/result caption for each. Preserve all contracts and fixture evidence.

ADVISORY mle.tile.035_037/s02: The s02/s03 and s07/s08 example–misconception pairs repeat the same distinctions on separate screens, contributing to a 16-step journey above the 8–14-step pacing target → Append s03's distinction to s02 and s08's distinction to s07, retaining the tensor and loader explain → check → apply sequences; this removes two repeat-only screens without removing facts.

ADVISORY mle.tile.038_040/s03: The 369-second default video sits inside an already dense 19-step, 18.9-minute tile, substantially exceeding the approximate 6–12-minute target → Use the existing summary mode as the default for this media group and offer the unchanged full clip as supplemental viewing; consolidate repeat-only distinction prose into the adjacent examples and revise the time estimate after the learner path is shortened. Preserve the graph-tracing and disabled-tracking contrast in the summary.

ADVISORY mle.tile.041_043/s01: The 40-line loop appears in full and is repeated in s05, while the 18-step tile is declared at 14.1 minutes → In s01, reveal setup separately from the inner minibatch update and loss-count recording sections; caption the latter two with 'one current-gradient update per batch' and 'record the actual final-batch count.' Keep the full s05 evidence and consolidate redundant example/distinction prose elsewhere to reduce reading time.

ADVISORY mle.tile.041_043/s10: The video bridge asks learners to observe the same phase switches already explained and demonstrated in s06–s09, making its distinct contribution weak → Replace the before bridge with 'Watch the transition from the training update block to validation: identify where training mode is restored, where evaluation mode begins, and which update operations disappear from validation.' Replace the after bridge with 'Use the phase transition you observed to audit a complete epoch; the dropout fixture separately verifies permitted random outcomes.'

ADVISORY mle.tile.044_045/s08: The example exposes the floating-point display artifact 0.6400000000000001, distracting from the isolated learning-rate diagnosis → Display the post-update loss as 'approximately 0.64' consistently in the prose, diagram labels/alt text, and s11 item i1; leave the gradient 2.0, parameter 1.8 and change −0.2 unchanged.

ADVISORY mle.tile.046_048/s07: The initial trial table exposes 23 columns, mixing selection evidence with byte-estimate details and measurement metadata → Present a compact selection table with batch_size, input_estimate_bytes, peak_allocated_tensor_bytes, budget_bytes, throughput_examples_per_second, minimum_throughput and completed; follow it with a separately captioned detail table for actual shapes, final-row counts, element widths and measurement protocol. Retain all registry values and the measured-memory-scope explanation.

ADVISORY mle.tile.049_050/s06: The 17-column hardware table requires scanning placement, eligibility, cost and lifecycle records simultaneously → Separate the display into an eligibility/placement table and a cost/closeout table, keeping execution_seconds, lifecycle_seconds, rate_per_second and their two cost columns together in the latter. Retain all registry values, verified stopped states, and the continuing-charge note.

ADVISORY mle.tile.051_051/s01: The first comparison visual introduces FPR/FNR, expected cost, head-gradient orientation and parameter-change checks before their explanations in s02–s03 → Move that comparison block to s04 after those explanations; leave s01 focused on loading the compatible checkpoint/processor and the declared Trainer workflow. This is anticipatory presentation, not an untaught assessment blocker.

ADVISORY mle.tile.051_051/s06: Eight classifications, a long setup excerpt, matrix-reference evidence and a cost table make one application much heavier than the tile's seven steps and 4.9-minute estimate suggest → Keep the same classify interaction and keys, but shorten i1 by referencing the already displayed workflow and retaining only the decisive freeze-before-replace lines, mapping/shape evidence, fresh-gradient agreement, parameter snapshots and matched-cost conclusion. Present adaptation, gradient verification and rate/cost explanation as separate earlier explainer steps within the 8–14-step target, and revise the estimate toward 6–12 minutes. Do not convert the judgment into an execution task.

VERDICT: PASS
