# Stage 08 — Independent pedagogy review

VERDICT: PASS

Reviewed all 12 tiles, rather than sampling, including every explainer, check, inspect-and-judge practice, recap and conditional remediation. Independently used `inputs/path_glossary_bundle.json` (required facts, prerequisites, teaching notes and practice intent), `scenario_asset_registry.json`, and the assembled `tile_lessons/*.json`. Applied the stage evaluator and Playbook §§2, 3 and 5. No generator reasoning or prior evaluator claims were consulted; deterministic gates were not rerun. Review is of authored lesson data, not a rendered-player or external-video playback inspection.

## Overall judgement

No BLOCKING pedagogy defects found. Checks follow the relevant text teaching. Required distinctions remain intact: both test gates versus one successful test; approval versus execution; surviving capacity versus client availability; lifetime versus authorization; integrity detection versus prevention; governance versus compliance; replacement mechanics versus authorization; stack completion versus recovery readiness; and deployment completion versus live validation. The supplied practice excerpts permit defensible judgements without a cloud or execution environment. Remediation restates the relevant mechanism and misconception, and wrong-option feedback addresses the offered mistakes. Registry observations support the presented conclusions.

Multi-concept tiles teach and assess each concept in a separate sequence rather than hiding an untaught second concept inside a check. Diagrams and tables do not contradict their text. Some label-only diagrams and repeated excerpts contribute less than their screen space suggests. The main pacing issue is the short single-concept journeys, not missing knowledge. The long audit-selection exercise has the opposite problem: many repetitive selections for two records.

The two video steps have identifiable incremental value in their authored summaries: tile 110 shows an actual destruction-prevention error and removal of the lifecycle rule; tile 116 adds concrete examples of quick live-behavior checks. Their bridges explicitly identify what the clips omit. Tile 110 also separates the clip's automatic apply approval from the lesson's required plan inspection and authorization. No additional factual teaching depends on watching either clip. Other tiles have no video step to evaluate; absence alone is not a blocker.

## Reviewed journeys

| Tile | Main steps | Authored estimate | Judgement |
|---|---:|---:|---|
| aws_devops.tile.100 | 4 | 3.2 min | Complete teach/check/apply flow; short and repetitive practice presentation |
| aws_devops.tile.101 | 5 | 3.4 min | Focused-change and approved-execution distinctions taught; short journey, weak diagram |
| aws_devops.tile.102 | 5 | 3.3 min | Capacity/path distinction and bounded experiment taught; short journey |
| aws_devops.tile.103 | 5 | 3.4 min | Scope, dependency order, version cleanup and follow-up taught; short journey |
| aws_devops.tile.104 | 7 | 6.3 min | Credential readiness and rehearsal isolation separately taught and checked |
| aws_devops.tile.106 | 7 | 6.3 min | Approval/stop and audit evidence separately taught; audit practice overly repetitive |
| aws_devops.tile.108 | 8 | 6.7 min | Integrity and retention distinctions taught with scoped evidence |
| aws_devops.tile.110 | 10 | 8.6 min | Backend sequence and replacement controls separately taught; video bridge preserves authorization boundary |
| aws_devops.tile.112 | 5 | 3.4 min | Target authority and separate readiness checks taught; short journey |
| aws_devops.tile.113 | 5 | 3.4 min | Threshold, exceptions and enforced promotion dependency taught; short journey |
| aws_devops.tile.114 | 9 | 6.8 min | Pipeline and workload diagnosis separately taught; health-practice hints could be more targeted |
| aws_devops.tile.116 | 5 | 4.7 min | Live validation and job-result reporting taught; below the approximate duration target |

Step counts above describe the journeys, not a new structural gate. Preserve planned step types; the following suggestions require neither execution labs nor implement-and-submit tasks. Extend short journeys through useful comparisons within existing steps, not padding or new prerequisite material. Re-time after revision rather than merely changing the estimate.

## Findings — 0 BLOCKING, 11 ADVISORY

ADVISORY aws_devops.tile.100/s01: The 3.2-minute journey is well below the approximate 6–12-minute target and moves directly from compact rules to recognition → Within s01, add a guided trace using the existing UNIT_JOB exit 1, INTEGRATION_JOB exit 0 and skipped promotion records: explain how each outcome contributes to the two-job dependency; re-time the journey without adding new facts or step types.

ADVISORY aws_devops.tile.101/s02: The 3.4-minute journey gives little time to distinguish review completeness from execution completeness → Expand s02 with a guided comparison of the existing complete record and the alternate record missing CI execution and instance verification; explicitly identify what approval proves and what remains unverified, then re-time.

ADVISORY aws_devops.tile.102/s02: The 3.3-minute journey compresses the key availability comparison into one short paragraph → Walk through both existing cases field by field in s02: capacity remains in both, request-path availability differs, and the client-required-behavior result follows that distinction; include a pause to identify the decisive evidence and re-time.

ADVISORY aws_devops.tile.103/s02: The 3.4-minute journey offers limited rehearsal of several removal decisions before the eight-item practice → Expand s02 into a worked trace of the existing object/version/delete-marker cleanup before bucket removal, followed by contrasting the retained and failed resource records with confirmed removal; re-time while preserving the deletion-versus-billing boundary.

ADVISORY aws_devops.tile.112/s02: The 3.4-minute journey states the stack/readiness distinction but barely works through it → In s02, compare the two registered restoration cases explicitly: both have completed creation and passing instance checks, but only one has a passing service check; trace which evidence establishes each conclusion and re-time.

ADVISORY aws_devops.tile.113/s02: The 3.4-minute journey moves quickly from policy rules to already-labelled outcomes → In s02, work through severity HIGH against threshold HIGH for both registered findings, then compare absent exception basis with the documented covering exception and trace each policy result into its promotion outcome; re-time.

ADVISORY aws_devops.tile.116/s01: Even with the video, the authored 4.7-minute journey is below the approximate duration target → Add a guided comparison of the two existing smoke-check records within s01, explicitly tracing expected/observed response to the job-result call and dependent progression; keep deployment completion separate and re-time.

ADVISORY aws_devops.tile.100/s03: The same workflow prelude is repeated in all three items, while the stretch-labelled task mainly matches explicitly named statuses → Move the shared workflow and continue-on-error context into the public prompt once, leave only the individual execution record in each item, and set difficulty to intro unless the judgement itself becomes more demanding. Keep the classification interaction and existing correct assignments.

ADVISORY aws_devops.tile.101/s01: The four unconnected diagram labels mostly duplicate the prose and table rather than showing the evidence sequence → Add labelled edges from focused review to commit/saved-plan evidence, from that evidence to reviewer approval, and from approval to CI apply/resulting-instance verification; label the final edge “approval before execution.” Preserve the table as the concrete evidence record.

ADVISORY aws_devops.tile.106/s06: Twenty-two selections over two rows repeatedly retrieve information already captured by the full-row selections, adding mechanical load rather than a difficulty ramp → Keep the successful and failed full-row tasks and, in each section, the target identity, CloudTrail request identity and operation cell tasks. Remove the remaining duplicate cell tasks; both full rows still preserve execution identifiers, timing, inputs, outputs and failure information.

ADVISORY aws_devops.tile.114/s08: The generic hints about intended outcomes and reassuring fields do not direct attention to this practice's specific metric-versus-health-check mistake → Replace the two hints with “Compare health_check across the original failure, improved-metric record and repeated-check record.” and “A running container and an improved metric are insufficient when the supplied health check still says fail.”

VERDICT: PASS
