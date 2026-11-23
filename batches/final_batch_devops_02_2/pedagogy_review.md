# Stage 08 — Independent pedagogy review

VERDICT: PASS

## Scope and method
Reviewed all five tiles (027–031), including every main-path step, interaction prompt, answer choices/items, grading feedback, remediation step, referenced registry dataset, and the glossary coverage/teaching blocks. Used `tile_lessons/*.json`, `inputs/path_glossary_bundle.json`, and `scenario_asset_registry.json` as independent evidence. No generator reasoning or prior evaluator claims were consulted, and no deterministic gates were rerun. EVALUATOR.md cites no additional playbook sections.

This is a lesson-text/asset review. No player screenshots were supplied. The video judgement is based on the bundled segment summary and bridge notes, not external playback.

## Learner-journey judgement
- **027:** Assignment/context and intended-access verification, plus named SSO configuration/login, are taught before assessment. The practice's hypothetical tested mismatch is expressly distinct from the registered untested case; its key is defensible. Credential and test errors receive specific feedback. The video adds UI navigation and permission-set selection, with its limits clearly bridged.
- **028:** Allow rules and statefulness precede the check; source references and filtering exceptions precede practice. The ingress-baseline and source-reference judgements are supported by the supplied excerpts. Feedback distinguishes new ingress from tracked responses and reference from rule import. The diagram supports the text; several boundary annotations anticipate s02 but do not require unexplained knowledge to answer a question.
- **029:** Exact provider syntax, supplied resource values, and execution/verification stages are taught before the check and practice. The four alternatives have defensible declaration/evidence keys, with specific feedback. Omitting the declared subnet remains a declaration defect even when supplied plan/result settings match. Reading density and repeated evidence dominate the practice.
- **030:** Field matching, ARN scope, deny precedence, and the qualified ordinary cross-account rule are all taught. Each of the eight row-selection tasks has a uniquely supported answer in the registry. Task feedback identifies the relevant permission failure. The application is heavily scaffolded by precomputed match summaries, and its difficulty ramp is modest.
- **031:** Standardized onboarding, approved inputs, enrollment/placement, and checkpoint verification precede assessment. Individual checkpoint keys do not confuse a verified checkpoint with overall case completion. Remediation correctly explains missing evidence. The very short main path compresses the journey.

All required ideas are present; none is hidden in a way that prevents success. No false wrong-answer feedback, contradictory visual, required later-concept understanding, or unsupported keyed judgement was found. These are inspect-and-judge exercises, not execution labs; no runtime, provisioned environment, or executed submission is required.

## Findings

ADVISORY aws_devops.tile.027/s01: The five-step main path (estimated 5.9 minutes) puts both assignment/access verification and named CLI-session setup into its opening screen, rather than the recommended 8–14-step journey → In the upstream plan, separate assignment/context, intended-access testing, and named-profile configuration/login into focused teaching screens; retain the existing video, check, and inspect-and-judge practice and target roughly 6–12 minutes without adding filler.

ADVISORY aws_devops.tile.028/s01: The five-step main path is estimated at 4.0 minutes and the opening diagram presents statefulness, source references, and filtering exceptions before their separate explanations → Rebalance the upstream plan into focused allow-rule, tracked-response, source-reference, and filtering-boundary teaching screens; introduce each corresponding diagram annotation alongside its explanation and target roughly 6–12 minutes.

ADVISORY aws_devops.tile.029/s01: The five-step main path is estimated at 3.9 minutes, while its opening side-by-side combines full HCL and an eight-column, four-stage evidence table → Give exact provider syntax, instance-value mapping, and execution-versus-verification their own focused teaching screens in the upstream plan; present the HCL before the stage comparison rather than placing both dense assets side by side, targeting roughly 6–12 minutes.

ADVISORY aws_devops.tile.030/s02: The five-step main path is estimated at 3.9 minutes and displays an eleven-column request table containing outcomes and explanatory notes immediately before an eight-task application → Work through one same-account and one cross-account row as focused examples; in the remaining instructional comparison, show request fields and supplied identity/deny evidence without `permission_outcome` and `evidence_note`, retaining those columns for worked-example explanations or remediation. Rebalance the upstream journey toward roughly 6–12 minutes.

ADVISORY aws_devops.tile.031/s01: The four-step main path (estimated 3.5 minutes) compresses account creation, enrollment/OU checks, and baseline verification into one explainer → In the upstream plan, separate standardized account creation, approved-input/enrollment/placement comparison, and individual-checkpoint versus overall-completion evidence into focused teaching screens; keep the existing read-and-judge practice and target roughly 6–12 minutes.

ADVISORY aws_devops.tile.029/s04: Each of four alternatives repeats the same full specification, plan, execution fields, and result settings, making the stretch step chiefly a long scanning task → Place the common specification once in the practice introduction; preserve each alternative's complete observed declaration and case-specific execution/plan/result evidence, but remove the four duplicated specification blocks. Keep all four judgements and their current specific feedback.

ADVISORY aws_devops.tile.030/s04: Request evidence includes precomputed `resource_allow` match/failure descriptions, so learners can answer the field-mismatch tasks without comparing the supplied policy fields themselves → Hide `resource_allow` from the practice table projection while retaining `request_id`, `Principal`, `Action`, `Resource`, `Condition`, `account_relationship`, `identity_allow`, and `explicit_deny`; keep the policy statements in the introduction and expose the match descriptions in feedback/remediation instead.

## Summary
Review completed for all five tiles. Findings: **0 BLOCKING, 7 ADVISORY**. Verdict is PASS because no blocking pedagogy defect was established; the listed pacing and evidence-presentation improvements remain nonblocking.
