# Stage 08 — Independent pedagogy review

VERDICT: PASS

Reviewed all twelve tiles, aws_devops.tile.015–026, rather than taking a risk sample. Sources: the assembled tile lessons (including every interaction, option/item feedback and remediation step), the matching glossary coverage and teaching text, and scenario_asset_registry.json. Applied EVALUATOR.md and Playbook §§2, 5 and 7. No generator reasoning or earlier evaluator claims were used; deterministic gates were not rerun. This is a lesson-data review, not a screenshot/rendering certification. No player screenshots were supplied with the reviewed artifacts.

## Learner-journey judgement

All tiles teach their assessed ideas in text before checking them, then provide inspect-and-judge application and a recap. The required facts remain understandable without video. Every glossary media field is null and there are no video steps, so video's incremental contribution is not assessable; absence alone is not a blocker. The HIGH video-need tiles do have relevant authored visuals or tables.

No BLOCKING defects found. The cases carry enough evidence for their intended judgements. Option/item feedback addresses the specific wrong distinctions, even where the generic hints are weak. The visuals support the text and the referenced tables agree with the registry. Adjacent facts in the opening explainers are related and explicitly presented, not hidden ideas. Practice is read-and-judge; no execution environment or submitted execution evidence is required.

| Tile | Main journey reviewed | Required steps | Assessment judgement |
|---|---|---:|---|
| 015 | Approved string configuration → rejection boundary → combined review | 6 | Configuration and pre-mutation outcomes distinguished |
| 016 | Preview → replacement review → approved execution | 5 | Preview does not provision or guarantee success |
| 017 | Scoped MFA condition → absent-key check → request records | 5 | True/false/absent and unchanged scope distinguished |
| 018 | Trust/caller permission/session permission → cross-account review | 5 | Entry and session work remain separate |
| 019 | Independent root-protection criteria → checklist classification | 5 | MFA does not excuse routine root use; still-needed key case is separate |
| 020 | Regional history/filter → actor/operation/target/time comparison | 5 | Matching target and operation, not timestamp alone |
| 021 | Active billing tag → allocation evidence → category review | 5 | Resource name does not allocate untagged spend |
| 022 | Collector/destination/JSON → known-event verification | 5 | Intended stream and structured fields both checked |
| 023 | Rollback/check/activation → outcome validation → recovery review | 5 | Restoring a file without reactivation is insufficient |
| 024 | Strategy proposals → constraints → proposal selection | 5 | One proposal meets all stated constraints; application repeats check |
| 025 | Metric/dimension/start → source verification → host records | 4 | Matching metric name alone does not verify host |
| 026 | Counts/policies → complete and all-missing windows → state classification | 5 | Zero is observed data; ignore retains prior state |

## Findings

The short step counts below are pacing advisories, not structural blockers: the skeleton is fixed by the tile plan. Do not insert steps or alter planned types directly in lesson JSON. Any expansion requires upstream replanning and reassembly. The 6–12 minute target is not demonstrated by these compact journeys; this is not a measured runtime claim.

ADVISORY aws_devops.tile.015/s01: Six required steps fall below the suggested 8–14-step journey → at the next planning revision, separate configuration comparison from rejection-trace reading and add a fresh bounded case; retain inspect-and-judge practice rather than padding text.
ADVISORY aws_devops.tile.016/s01: Five required steps compress preview, replacement review and execution into a short journey → at the next planning revision, separate new-stack preview/execution from update-replacement review and add a fresh discrepancy case.
ADVISORY aws_devops.tile.017/s01: Five required steps give little incremental practice between the scoped condition explanation and full request review → at the next planning revision, add distinct in-scope and out-of-scope request comparisons without broadening the taught policy.
ADVISORY aws_devops.tile.018/s01: Five required steps introduce all three permission boundaries almost together → at the next planning revision, separate trust entry, caller permission and session work into short related screens with an intervening comparison.
ADVISORY aws_devops.tile.019/s01: Five required steps produce a brief checklist journey → at the next planning revision, stage MFA, routine-use and existing-key findings separately and add a new mixed checklist rather than repeating the same evidence.
ADVISORY aws_devops.tile.020/s01: Five required steps give a short attribution journey → at the next planning revision, separate regional filtering from event-field attribution and add a fresh operation/target mismatch case.
ADVISORY aws_devops.tile.021/s01: Five required steps provide little ramp beyond the displayed report categories → at the next planning revision, separate resource tagging, billing activation and report interpretation, then add a fresh unallocated-spend judgement.
ADVISORY aws_devops.tile.022/s01: Five required steps compress collector configuration and delivery verification → at the next planning revision, stage file/destination comparison and structured-event verification separately with a fresh record.
ADVISORY aws_devops.tile.023/s01: Five required steps compress preparation, activation and recovery → at the next planning revision, separate pre-activation checks from post-activation outcomes and add a fresh recovery record.
ADVISORY aws_devops.tile.024/s01: Five required steps provide a short strategy-comparison journey → at the next planning revision, give exposure, capacity and return-route comparisons separate practice before the combined judgement.
ADVISORY aws_devops.tile.025/s01: Four required steps make the shortest journey, with nearly all teaching on the opening screen → at the next planning revision, separate metric selection, instance dimension and start-versus-verification evidence, with a fresh check before combined review.
ADVISORY aws_devops.tile.026/s01: Five required steps compress the most complex evaluation journey → at the next planning revision, separate complete-window counting from missing-data policy comparison with an intervening check.
ADVISORY aws_devops.tile.024/s04: Application repeats s03's exact proposals, requirements and answer, then adds an unrelated Workload-row response mapping → keep table_select, but author a registered delivery-proposal table for this step and a fresh bounded constraint case; select an actual proposal row rather than a cost-category response slot. Preserve the explicit distinction between fictional proposal evidence and universal strategy guarantees.
ADVISORY aws_devops.tile.026/s01: The opening visual is an 18-column table immediately after four rule blocks, making the worked comparison difficult to scan → retain common alarm configuration in the prose/caption and display window_id, three samples, breach_count, policy, prior_state and resulting_state in the table. In s02, explicitly walk through window 1: two samples exceed 60, so 2-of-3 yields ALARM.
ADVISORY aws_devops.tile.026/s03: Generic hints about configuration/approval do not guide an ignore-versus-missing mistake → replace the hints with “Which policy retains the current state rather than assigning a new one?” and “For ignore, carry forward the supplied current state, ALARM.” Keep the existing specific option feedback.

## Disposition

Review completed honestly. Advisory-only content: PASS under the evaluator's blocking/advisory rule. No generator artifact edited. No runtime, lab or submission-route changes requested.
