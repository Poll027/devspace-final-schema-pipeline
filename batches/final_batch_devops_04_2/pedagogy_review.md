# Stage 08 — independent pedagogy review

Batch: `final_batch_aws_devops.region.04_2`

VERDICT: PASS

Blocking defects: 0. Advisory defects: 7.

## Scope and method

Reviewed all six assembled lessons (067, 068, 069, 070, 071, 073), including every check, practice item, keyed judgement, item-specific feedback, hint and remediation screen. Re-derived the judgements from `inputs/path_glossary_bundle.json`, the seven datasets in `scenario_asset_registry.json`, and the preceding lesson text. Consulted the fixed tile plans for the intended journey, and Playbook §§2, 5 and 7. Did not inspect generator reasoning, alter generator artifacts, or rerun deterministic gates.

This is an authored-content review. No rendered player screenshots or playable local video were provided; visual judgements concern the authored diagrams/tables/code annotations, and the video judgement is limited to the supplied segment summary and bridge.

## Journey assessment

| Tile | Journey | Assessment |
|---|---|---|
| aws_devops.tile.067 | 2 explainers → check → classify code → recap (5 steps) | The attempt-count contrast, eligible-versus-terminal distinction, optional metadata access and final reporting are taught before assessment. Each implementation has a defensible classification and targeted feedback. Initial reading is concentrated; repeated full snippets add scanning work. |
| aws_devops.tile.068 | 2 explainers → check → classify review notes → recap (5 steps) | Account/period scope, category evidence and owner-supported avoidability are available before the learner judges recommendations. Wrong-account, wrong-period and required-usage notes are distinguishable from the supported note. Introductory distractors are much less plausible than the key. |
| aws_devops.tile.069 | 2 explainers → check → classify test reports → recap (5 steps) | Requested versus observed counts and replacement identity are taught explicitly. Reports carry sufficient evidence; deletion acceptance is correctly distinguished from verified reconciliation. The initial visual presentation is not chronological. |
| aws_devops.tile.070 | 2 explainers → check → dependency ordering plus follow-up → recap (5 steps) | Supplied dependency edges give one required order. Readiness gates and the qualitative recovery objective are taught. The follow-up correctly avoids an unsupported numerical guarantee. Repeated explanation makes this short journey feel more like a summary than a developed walkthrough. |
| aws_devops.tile.071 | Logs explain/check/apply → routing explain/video/check/apply → shared recap (9 steps) | Each concept is taught before its own questions. Log identity, interval and order judgements match the evidence. Routing judgements correctly require confirmation where needed, unchanged evaluation and contextual receipt. The clip adds a configuration-screen demonstration; its bridge explicitly excludes threshold lowering and identifies missing receipt demonstration. Long repeated JSON reports burden the log practice. |
| aws_devops.tile.073 | 2 explainers → check → classify task reports → recap (5 steps) | Bounded execution-role scope, unchanged supplied payload and invocation-versus-task outcomes are taught. Successful and failed task reports are judged consistently with results/logs; permission failure does not justify widening the role. The up-next block supplies no useful next-step information. |

All required ideas are visible rather than hidden inside a two-idea step. The checks precede more demanding evidence reviews. Option/item-specific remediation explains the relevant mistake; some shared incorrect messages are generic, but they do not replace the specific feedback. Authored visuals agree with the registry evidence and support the lesson distinctions.

Five tiles have five planned steps rather than the review's 8–14-step pacing target. Treat this as an advisory pacing issue, not an instruction to override the fixed plan or add execution labs. There is no measured completion-time evidence; the 6–12-minute target cannot be certified from step count alone. Improvements below keep the planned interaction types and read-and-judge practice model.

## Findings

ADVISORY aws_devops.tile.067/s01: The opening screen concentrates prose, a complete code walkthrough and a comparison table, then s02 repeats much of the same explanation; the five-step journey front-loads the reading → Keep s01's finite-budget definition, count contrast and annotated code; move the comparison table to s02 and make s02 a worked trace: “With total_max_attempts=3, one initial request leaves at most two retries. A terminal or exhausted-retry ClientError ends in a failure report; missing RequestId must not prevent Code and Message from being reported.” Retain the once-only application-call rule and safe optional-access example before s04.

ADVISORY aws_devops.tile.068/s03: The key is a long, carefully qualified evidence note while both distractors use obvious resource-existence/deletion errors, making the introductory check easy to answer by style → Keep the key's account/period/cost/usage/owner evidence, but use similarly shaped distractors: “Recommend review of idle-test-usage for account 1002 using billed cost 48 and usage 240; treat it as evidence for selected account 1001” and “Recommend review of required-data-usage for account 1001 using billed cost 12 and usage 60, despite the owner record that it remains required.” Update their feedback to identify account mismatch and required-usage context respectively.

ADVISORY aws_devops.tile.069/s01: The before/after visual shows the completed replacement before a separate ‘during reconciliation’ table, so a learner must mentally reconstruct before → during → after → Move the during-reconciliation table to s02 and introduce it with “Immediately after the controlled removal, requested replicas remain 3 but observed replicas are 2. Continue inspection until replacement orders-pod-d restores the observed count to 3.” Keep s01's before/after contrast as the destination view and explicitly label it “Starting state versus completed reconciliation.”

ADVISORY aws_devops.tile.070/s02: The second explainer largely repeats the dependency graph and general rule in an already short five-step journey → Replace the repetitive example with a concrete readiness pause: “Infrastructure restoration finished, but its readiness check has not passed. Database restoration must wait. Once infrastructure readiness passes, restore the database and verify database readiness before resuming orders. This plan uses the supplied capabilities to support usable service with verified prerequisites; it establishes no numerical recovery guarantee.” Keep the warning that the sequence belongs only to the supplied workload.

ADVISORY aws_devops.tile.071/s04: Four full JSON reports repeat the same group, interval and event records; finding the changed identity/order/window requires excessive scanning unrelated to the conceptual judgement → Present one shared target/scope and canonical three-event sequence, then shorten each item to its query, retained-event identities/timestamps, sequence and claim. Keep the distinct wrong-request event, descending order and 09:59 out-of-window event visible within their respective items; do not remove the evidence needed to classify them.

ADVISORY aws_devops.tile.073/s04: Five long reports repeat function, role and payload context already supplied in the prompt, concentrating reading in one practice step → State once that all items use orders-resource-check, orders-check-role and the unchanged supplied payload unless explicitly overridden. In each item retain task scope, invocation status, task result, execution-log evidence and conclusion; keep the unlimited-scope override and missing-approved-action evidence explicit. Preserve all five classifications and their specific feedback.

ADVISORY aws_devops.tile.073/s05: The up-next title and text both say “Continue the operational-response path,” providing no additional learner guidance → Replace the text with “Carry forward the distinction between an accepted invocation and a task outcome verified by returned results and execution logs.” Do not invent an unspecified next tile.
