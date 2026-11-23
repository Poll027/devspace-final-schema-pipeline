# Stage 08 — Independent pedagogy review

Batch: `final_batch_learn_python.region.01`

VERDICT: PASS

**Result:** 0 BLOCKING defects; 10 ADVISORY findings. PASS is advisory-only, not a claim that no improvements are needed.

## Scope and method

Reviewed all 12 tiles as the first-region/canary learner journey, including their explainers, checks, editable practice prompts and starter files, answer keys, option feedback, hints, recaps and remediation screens. Independently used `inputs/path_glossary_bundle.json` (the 26 concepts represented here), `scenario_asset_registry.json`, and the assembled `tile_lessons/*.json`. Followed the stage evaluator instructions and the playbook's text-before-assessment and learner-contract principles. Did not consult generator reasoning or repair scripts/logs, edit generator artifacts, or rerun deterministic gates.

This is a source-content review. No rendered screenshots were reviewed. Video judgements use the bundled segment descriptions, summaries and bridges; no external video playback was available. Consequently, actual rendering, narration quality and visual timing are not certified here.

## Journey assessment

| Tile suffix | Steps | Estimated minutes | Assessment |
|---|---:|---:|---|
| 000_002 | 14 | 14.5 | Assignment → types → arithmetic; checks follow teaching, then increasingly demanding practice. Final practice has avoidable instruction load. |
| 003_005 | 15 | 12.4 | Comparisons → logical grouping/short-circuiting → conversion. Boundary and invalid-text mistakes receive truthful option feedback. |
| 006_007 | 8 | 6.9 | Exclusive branches precede pre-tested repetition. The input simulator is supplied scaffolding, not required knowledge. |
| 008_010 | 12 | 11.7 | Positional collections → distinct membership → key-based access. Visuals and keys agree with the taught operations. |
| 011_011 | 4 | 3.3 | Compact f-string lesson with a taught computation and presentation specification; prompt repeats too much of its expected outcome. |
| 012_014 | 11 | 16.6 | Define/call → parameter binding → return/reuse. Return/print contrast is explicit. Video makes the journey noticeably long. |
| 015_017 | 13 | 11.9 | Tuple return/unpacking → defaults/keywords → scope. Explicit module lookup and unbound-local behaviour are taught, not assumed. |
| 018_018 | 5 | 4.2 | Protected operation → matching/unmatched control flow → recovery practice. |
| 019_019 | 4 | 3.3 | Module versus directly imported member → check → short application. |
| 020_020 | 5 | 3.5 | Before/after styling → recommendation versus syntax → restyling practice. |
| 021_024 | 16 | 15.6 | Accumulation → skip/stop → collection traversal → comprehensions. This is the longest concept sequence and has a demanding final transfer task. |
| 025_025 | 5 | 3.7 | Modes and closure → CSV header/field semantics → managed reading practice. The fixture agrees with the returned text quantity. |

The 8–14-step/6–12-minute aspiration is not met uniformly. The brief, single-concept tiles are not intrinsically unsuccessful: they complete coherent teach/check/apply cycles, and padding them merely to reach a duration target would add dead text. The dense multi-concept journeys merit pacing attention; findings below propose improvements within existing step types rather than changing the fixed skeleton.

No check requires an untaught Python capability to identify its answer. The multipart choices explicitly expose their component judgements rather than hiding an additional idea. Remediation and per-option explanations supply the relevant rules; there is room for more targeted hints, but no identified remediation makes a learner's specific misconception impossible to resolve. Supplied simulation machinery is not treated as something learners must understand or implement.

Code walkthroughs generally earn their place by showing binding changes, branch selection, iteration state, lookup differences or before/after style. No visual/text contradiction was identified. The CSV table describes a count of 3, whereas DictReader produces the serialized field text "3"; the lesson correctly explains that distinction. Video offers changed-value/type demonstrations and a different return/reuse scenario, although the learner-facing bridges contain avoidable coverage-audit language.

## Findings

ADVISORY learn_python.tile.000_002/s13: The six-assignment arithmetic task is presented as one long paragraph, adding working-memory load at the end of an already 14.5-minute journey → Keep the same task and outputs, but present six numbered requirements: `division: tokens divided by group_size`; `quotient: the floored quotient`; `remainder: the remainder`; `power: a raised to b`; `grouped: add a and b, then multiply by c`; `ungrouped: add a to b multiplied by c, without parentheses`. Retain the instruction to use supplied names and make no output calls.

ADVISORY learn_python.tile.003_005/s01: Every comparison-line annotation repeats the same question instead of showing what changes at the boundary → Replace the annotations on lines 2–7 with, respectively, `Equality: True.`, `Inequality: False.`, `Strictly above: False at the boundary.`, `At least: True at the boundary.`, `Strictly below: False at the boundary.`, and `At most: True at the boundary.`

ADVISORY learn_python.tile.006_007/s07: The editable starter visibly contains iterators, lambda, indexing and recording lists that are not needed to solve the while-loop task; the prompt exempts the setup but does not clearly mark where learner work begins → Leave the simulator unchanged and add to the prompt: `The lines through stop_label are supplied test setup; you do not need to understand or edit them. Add your first input request and while loop below stop_label.` Do not introduce a lab or teach the simulator internals here.

ADVISORY learn_python.tile.008_010/s11: Calling a price mapping quantities introduces unnecessary naming friction after teaching quantities as counts → Without changing the registered workspace or required output names, add a short clarification: `In this exercise, the required dictionary name is quantities, but its values are product prices.` Future asset authoring should use a price-specific dictionary name.

ADVISORY learn_python.tile.011_011/s03: The prompt repeats the entire computed expected sentence and format requirement after already specifying the task, making practice read like a restatement of the solution → Shorten the prompt to: `Using the supplied quantity and cost, assign message an f-string in the form "The total is <total>." Compute quantity * cost inside the braces and display that number with two digits after the decimal point. No output call is needed.` Keep the same grading expectations.

ADVISORY learn_python.tile.012_014/s08: The 401-second return-values clip contributes substantially to a 16.6-minute tile, and the after-bridge is a coverage audit rather than a learner takeaway → Preserve the frozen segment and its optional availability; prefer summary mode for the short journey. Replace the after-bridge with: `Return supplies a value the caller can store and combine, and ends the current call. Printing alone only displays a value. Reaching the end without return supplies None.`

ADVISORY learn_python.tile.015_017/s10: Three function scenarios are packed into one continuous prompt, increasing comparison load even though each underlying rule is taught → Preserve the same options and key, but format the stem as three numbered cases on separate lines. Precede them with `Assume quantity is already bound at module level. Compare these functions:` and end with `Which option correctly describes all three?`

ADVISORY learn_python.tile.021_024/s12: The transition from doubling positive quantities in the example to squaring even quantities in the next check is defensible transfer, but lacks a small bridge explaining the new filter/result combination → Add a closing sentence: `For the next task, quantity % 2 == 0 selects even quantities because their remainder on division by 2 is zero; quantity * quantity computes a square. These go in the filter and result positions, respectively.` Preserve the comprehension practice type.

ADVISORY learn_python.tile.021_024/s15: The practice hint is a generic construct reminder and does not help distinguish filtering from computing, the most likely mistake here → Replace it with `First identify the accepted items using a remainder comparison with even_divisor and zero. Separately choose the expression that squares each accepted quantity; place that expression before for.`

ADVISORY learn_python.tile.025_025/s01: The opening screen introduces ordinary text I/O, unmanaged closure and CSV collection in a single flat sequence, so the learner must infer which operations belong to which route → Keep all facts and blocks, but insert learner-facing headings or short prose labels `Text-file operations`, `Closing the file`, and `CSV row dictionaries` before the corresponding groups. Do not add steps or remove required facts.

VERDICT: PASS
