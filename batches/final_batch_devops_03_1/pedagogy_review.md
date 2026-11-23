# Stage 08 — Independent pedagogy review

VERDICT: PASS

No BLOCKING defects found. Advisory changes are recommended; they do not prevent a learner from succeeding from the taught material.

## Scope and method

Reviewed all 12 full lessons: aws_devops.tile.032, .034, .035, .036, .038, .040, .041, .042, .043, .044, .046 and .050, including their optional remediation steps. Used the frozen glossary bundle's required facts, teaching examples and practice intents, and the scenario registry's two authored datasets as independent references. Applied the evaluator instructions and Playbook §§2, 5 and 7. Did not inspect generator reasoning or re-run deterministic gates.

This is an authored-content review, not a rendered-player review. No screenshots were present in the batch. Video judgments use the supplied segment summaries and bridge text; playback and visual rendering were not independently verified.

## Learner-journey assessment

- Explain/check/apply order is sound across the reviewed lessons. Text teaches the distinctions before the associated checks, including the separate credential contexts, exact-digest consumption, download-integrity/provenance distinction, rollback statuses and qualified STS grant rules.
- The keys are defensible from the learner-visible evidence and prior teaching. The fictional runbook and handoff examples agree with the registry data. The handoff observations support improved (40 to 25), unchanged (40 to 40) and worsened (40 to 55) waiting time.
- Wrong-choice and wrong-item feedback identifies the relevant mistake. Remediation revisits the applicable distinction rather than requiring a new untaught operation. Generic top-level feedback is backed by more specific option/item feedback.
- Illustrative visuals support the relevant comparisons and are labeled as schematic or fictional rather than claimed execution evidence. No text/visual contradiction found. Some complex diagrams and dense steps could be easier to read.
- The three video steps have a reasonable distinct purpose: service-request assembly (.032/s07), locating the console attachment workflow (.046/s03), and following a workflow authentication/run result (.046/s11). Their bridges state what the clips do not establish, and the required teaching remains in text.
- Inspect-and-judge practice was assessed as read-only practice, not as an execution lab. No environment, execution or submission-route requirement was imposed.
- Pacing is uneven: seven lessons are 4–5-step microtiles estimated at 3.5–4.3 minutes, while .046 has 18 steps estimated at 18.2 minutes. These are planning/pacing advisories, not data-integrity blockers. The authored step types should not be changed independently of the planner.

## Findings

ADVISORY aws_devops.tile.034/s01–s04: The four-step, 3.5-minute plan is below the nominal 8–14-step / 6–12-minute target, yet s03 repeats almost the entire lengthy runbook three times, concentrating the reading burden in one interaction → Keep the registered runbook as the common reference; replace i1 with “The candidate retains the complete supplied runbook unchanged,” i2 with “The candidate retains the supplied runbook except that its stop condition and escalation recipient are replaced by ‘use your judgement’,” and i3 with “The candidate retains the supplied runbook and adds: ‘if the health result is absent, repeat the restart until healthy.’” Preserve the current classifications and feedback; request an explicit planner-level microtile pacing exception rather than padding or changing step types.
ADVISORY aws_devops.tile.035/s01–s05: Five steps and 3.6 estimated minutes make this a microtile rather than the stated normal tile journey → Request an explicit planner-level microtile pacing exception and expose the short duration to learners; keep the existing explain/check/apply sequence rather than adding repetitive filler.
ADVISORY aws_devops.tile.040/s01–s05: Five steps and 3.7 estimated minutes fall below the normal pacing target → Request an explicit planner-level microtile pacing exception and expose the short duration to learners; retain the authored step types.
ADVISORY aws_devops.tile.041/s01–s05: Five steps and 4.3 estimated minutes fall below the normal pacing target → Request an explicit planner-level microtile pacing exception and expose the short duration to learners; retain the two distinct checks and the current step types.
ADVISORY aws_devops.tile.042/s01–s05: Five steps and 3.5 estimated minutes fall below the normal pacing target, particularly with a 13-task application step → Request a planner-level microtile pacing exception and revise the learner-facing estimate to include the actual table-reading and task-selection workload; do not add filler steps.
ADVISORY aws_devops.tile.043/s01–s05: Five steps and 3.5 estimated minutes fall below the normal pacing target → Request an explicit planner-level microtile pacing exception and expose the short duration to learners; retain the authored step types.
ADVISORY aws_devops.tile.050/s01–s05: Five steps and 3.6 estimated minutes fall below the normal pacing target → Request an explicit planner-level microtile pacing exception and expose the short duration to learners; retain the role-based versus resource-based practice contrast.
ADVISORY aws_devops.tile.042/s04: Thirteen selections in one interaction include six repetitive baseline/after-value lookups, slowing the ramp from evidence location to outcome judgment → If task-count constraints permit, keep t1–t6 and t11–t13 and remove t7–t10; the three row judgments still apply the fixed signal to all outcomes. Otherwise group t1–t4, t5–t10 and t11–t13 visibly as “Identify the proposal,” “Locate observations” and “Judge outcomes.” Preserve the table_select interaction and required capability coverage.
ADVISORY aws_devops.tile.046/s01–s18: Four identity concepts, 18 steps and 18.2 estimated minutes exceed both normal tile pacing targets → Request a planner-level pacing exception or replanning for this tile; while the current skeleton remains frozen, signal four explicit progress milestones in existing ledes: “1 of 4: EC2 instance profile,” “2 of 4: EKS Pod Identity,” “3 of 4: GitHub OIDC,” and “4 of 4: STS session.” Keep step types and all required teaching intact.
ADVISORY aws_devops.tile.046/s14–s15: Credential composition/lifetime and three permission-grant distinctions are all packed into s14; its nominal timeline also contains four disconnected policy-rule callouts, making the permission explanation harder to organize → Keep composition, assume-role fields and Expiration in s14. Move the full permission-rule prose to the beginning of s15, before its worked explanation, and group its text under “Role identity grants,” “Resource-based grants / direct session ARN” and “Explicit deny.” Place the policy-rule callouts with s15 rather than in the credential timeline, retaining the full direct-session-ARN qualification before s16.

## Disposition

All findings are ADVISORY. No answer, feedback, required teaching or registry contradiction warrants failure. Planning exceptions/replanning belong to the planner; this review does not authorize editing the frozen lesson step types.
