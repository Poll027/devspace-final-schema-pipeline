# Stage 08 — Independent pedagogy review

VERDICT: PASS

## Scope and method

Reviewed all five assembled lessons (80 main steps), including learner-facing text, visuals, prompts, answer keys, option/item feedback, hints, remediation and representative code-workspace contracts. Re-derived the content against the 14 relevant glossary bundles and the scenario/asset registry. Read the stage evaluator and the playbook's teaching-before-assessment, fixed-plan, fixture and learner-facing lesson-contract guidance. Did not inspect generator reasoning, repair reports or self-audits, execute exercises, or rerun deterministic gates. This is a JSON/content review; no reference-player screenshots were available in the reviewed inputs.

Inspect-and-judge fixtures were evaluated as read-and-judge practice, not as live cloud/container labs. No runtime provisioning, executed evidence or external submission route is requested by this review.

## Journey assessment

| Tile | Main steps | Declared minutes | Assessment |
|---|---:|---:|---|
| mle.tile.080_082 | 15 | 12.5 | Aligned summaries precede drift/quality distinctions and feature-level decisions. Checks and applications have the necessary rules. Wide summary tables add reading burden. |
| mle.tile.083_085 | 17 | 13.1 | Cohort membership and maturity precede quality calculations; alert rules precede replay checks; diagnosis requires distinguishing evidence. The full mature-join display and repeated statistics boilerplate slow the journey. |
| mle.tile.086_089 | 22 | 19.9 | Eligibility, authorized immutable-input invocation, durable admission and candidate acceptance form a coherent ramp. Inspect-and-judge keys are defensible and feedback addresses the actual violations. This is substantially longer than the target journey. |
| mle.tile.090_090 | 6 | 4.4 | A short, coherent recovery sequence distinguishes VM state from service recovery. Practice is action ordering through a supplied simulator, despite the generic function-writing lede. |
| mle.tile.091_094 | 20 | 19.1 | Utilization, attribution, notification/action separation and scoped cleanup are taught before assessment. Rules and fixture evidence support the judgements. Long tables and the large cleanup excerpt make this a heavier session. |

No BLOCKING defect found. Required distinctions are not hidden behind video or later-concept understanding. Option/item-specific feedback and linked remediation correct the tested misconceptions; generic feedback remains a wording/helpfulness issue because specific hints and explanations supply the missing direction. Visuals support reference alignment, identity binding, cohort denominators, lifecycle scope and postchecks rather than contradicting the text. There are no video steps in these lessons, so the video-added-value check is not applicable; absence alone is not treated as a defect.

## Findings

ADVISORY mle.tile.080_082/s01: The 15-step, 12.5-minute journey slightly exceeds the target, and two ten-column tables repeat identity/window fields and mostly empty statistic cells → Preserve the fixed step skeleton and calculated values; make the captions explicitly “Reference summaries” and “Production-window summaries,” introduce the comparison with “Compare proportions only at matching definitions; each window retains its own denominator,” and present category/class, bins and numeric summaries as clearly separated table sections or optional detail views.

ADVISORY mle.tile.083_085/s01: The identity-preserving join prints all 60 mature rows immediately after the aggregate, increasing reading load without adding a new rule; the tile is already 17 steps and 13.1 minutes → Keep the aggregate visible and show a small representative join preview with prediction ID and both timestamps; provide the complete 60-row result in an expandable detail view, labelled “Full matched mature cohort: 60 rows.” Retain all underlying result data and the existing duplicate/unmatched handling explanation.

ADVISORY mle.tile.086_089/s22: At 22 steps and 19.9 declared minutes, this is materially longer than the 8–14-step/about-6–12-minute target → Do not remove required facts or change the fixed interaction types. Advertise this as an approximately 20-minute extended lesson, provide a resume/break cue after s10 (“Pause here if needed: next we prevent duplicate runs, then gate candidates”), and shorten repeated Cloud Build/PyYAML boilerplate in s13 to a reminder referencing the already taught s07–s08 rules while retaining fatal-gate and successful-dependency requirements.

ADVISORY mle.tile.090_090/s05: The lede asks for a learner-defined function and imports, but the editable task is ordering action0 through action9 for the supplied recover callable → Replace the lede with “Order the supplied recovery actions under the runbook; the simulator checks the sequence and required recovery evidence.” Keep the existing action-ordering task and simulator, not an implement-and-submit lab.

ADVISORY mle.tile.090_090/s06: Six steps and 4.4 declared minutes fall below the usual journey target, but the recovery sequence is complete and adding filler would not help → Label this a “Short recovery consolidation — about 4–5 minutes” at entry and recommend completing it alongside the adjacent operations lesson; retain the fixed six-step plan rather than padding it with repeated runbook text.

ADVISORY mle.tile.091_094/s05: This 20-step, 19.1-minute tile includes five billing/lifecycle/allocation tables on one explainer, making the evidence-to-result path difficult to scan → Advertise the extended approximately 20-minute duration, add a break/resume cue after s09, and introduce the tables with “Read in order: billing rows → workload windows → direct/shared allocations → reconciliation and unit costs → per-workload summaries.” Keep full row data available, but place detailed allocations behind a clearly labelled detail view so the reconciled totals remain the primary visible takeaway.

ADVISORY mle.tile.083_085/s11: The generic incorrect feedback names observations, denominators, boundaries and gates without locating an alert-configuration or replay mistake; specific hints make the task recoverable, but the first feedback message is weak → Replace this step's incorrect message with “Check the reloaded indicator, baseline window, threshold, divisor, owner and response first. Then check that normal and equality windows emit no record and a breached window emits the configured owner/action.” Preserve the existing specific hint and replay task.

ADVISORY mle.tile.091_094/s18: “Cleanup evidence contract” sounds like the full cleanup verification contract, while Audit A and the measured fact focus on the audit's ownership/identity/action/retention/non-disclosure fields → Narrow the prompt to “Which excerpt contains the required cleanup audit fields for ownership, active/retired identities, authorization, artifact retention and credential non-disclosure?” Keep the options and key; s19 remains the full health/absence/destructive-action judgement.

## Disposition

0 BLOCKING defects; 8 ADVISORY findings. PASS with advisory improvements recorded. No generator artifact was edited.
