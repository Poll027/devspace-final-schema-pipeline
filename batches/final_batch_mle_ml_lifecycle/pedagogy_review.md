# Stage 08 — Independent pedagogy review

## Scope and method

Reviewed both tiles, including all 41 main steps, interactions, learner-facing workspace scaffolds, answer feedback and remediation steps. Re-derived the teaching requirements from `inputs/path_glossary_bundle.json` and the fictional fixture context from `scenario_asset_registry.json`; reviewed the assembled `tile_lessons/` artifacts rather than generator reports or reasoning. Applied `08_pedagogy_review/EVALUATOR.md` and the playbook's text-before-assessment and lesson-contract principles. This is a text/artifact review; rendered player screenshots were not supplied. No deterministic gates were rerun and no generator artifacts were changed.

## Learner-journey assessment

- **Explain → check → apply:** Each concept has text instruction before its check and practice. The dependency, fail-closed, safe-YAML, protected-test, secret non-disclosure, recovery and lineage judgements are supported by preceding instruction. The inspect-and-classify lineage practice is treated as read-and-judge, not as an execution lab.
- **Defensible judgements:** The choice keys follow the taught distinctions. The lineage classification includes concrete missing/mismatched links, wrong-generation retrieval, failed commit inspection and suppressed assertion evidence; these distinguish rejection from the guarded valid and exact-version boundary cases.
- **Remediation:** Option-specific feedback and linked remediation address the tested mistakes. Generic top-level feedback and practice hints are less useful than the specific choice feedback, but do not create an unsupported judgement.
- **Visuals:** Accepted/rejected fixture comparisons support the text and distinguish intended configuration from observed fixture outcomes. No contradictory teaching visual was identified. Several visuals expose far more raw output than learners need for the stated distinction.
- **Difficulty and pacing:** The tiles have 18 and 23 steps and declare 14.3 and 18.8 minutes respectively, exceeding the review's preferred 8–14 steps / approximately 6–12 minutes. Full-function authoring, fixture assertions and long output dumps likely require longer still. This is a pacing advisory, not a request to change the fixed plan or attach execution labs.
- **Video:** Neither assembled tile contains a video step. The glossary marks video need HIGH, but text still teaches the assessed ideas. There is no video contribution to evaluate; no blocker is inferred solely from absent media.

## Findings

ADVISORY mle.tile.073_075/s01: The accepted/rejected-panel introduction is repeated verbatim before and after the diagram → retain the introduction once and replace the trailing duplicate with “The rejected snapshot retains its failed checks, and training remains NOT_STARTED.”

ADVISORY mle.tile.076_079/s01: The sentence beginning “Successful predecessor completion and artifact-identity agreement are separate checks” is repeated verbatim around four code panels → keep it once; replace the trailing duplicate with “In the mismatch run, compare training's produced A with model validation's resolved input B.”

ADVISORY mle.tile.073_075/s06: Two fully expanded 86/93-line fixture reports make the package-contract distinction unnecessarily expensive to read → display a compact accepted/rejected comparison containing prediction path, expected/actual sample IDs, row count, shape, numerical verdict, declared tolerances and dependent-stage status; retain the complete computed records as optional details without changing their values.

ADVISORY mle.tile.076_079/s18: Five code panels include a 151-line expanded audit record and long command output, overwhelming the first lineage explanation → lead with a compact chain of deployment, approval, selected registry version, recorded run, artifact generation/hash, dataset/configuration identity and commit-check exit results; keep full records and Git output in optional details. Preserve the missing/mismatched-link evidence rather than replacing it with a bare “verified” label.

ADVISORY mle.tile.073_075/s05: The tile's 14.3-minute estimate is optimistic for three full-function/fixture-assertion authoring practices in addition to the explanations → retain the planned step types, label s05/s10/s17 as extended practice, and revise the tile estimate using a timed learner walkthrough after reducing raw-output reading load.

ADVISORY mle.tile.076_079/s17: The 18.8-minute tile estimate obscures the sharp ramp from small binding repairs to recovery-function and repeat-invocation assertion authoring → retain the practice type; divide the prompt into “Verify existing output,” “Recover missing work,” and “Assert first/repeat outcomes,” and update the duration estimate from a timed learner walkthrough.

ADVISORY mle.tile.076_079/s11: Practice hints repeat generic evidence/predicate advice without directing the learner to the four marked binding mistakes → replace them with “Bind production_artifact to approved_artifact; staging_waits must name compatibility.” and “authorization_waits must name staging_quality; production_waits must require both staging_quality and authorization.”

## Verdict

No BLOCKING pedagogy defect identified. The findings above concern reading load, duplication, pacing and hint specificity, not unsupported facts, unanswerable judgements or missing runtime provision.

VERDICT: PASS
