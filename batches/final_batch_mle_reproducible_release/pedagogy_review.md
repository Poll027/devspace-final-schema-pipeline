# Independent pedagogy review — 08_pedagogy_review

Batch: `final_batch_mle.region.reproducible_release`

## Scope and method
Reviewed all four tiles (canary-conservative coverage), including every main step, interaction prompt, grading key, item/option feedback and linked remediation. Used `tile_lessons/*.json`, the eight concept bundles in `inputs/path_glossary_bundle.json`, and `scenario_asset_registry.json` as independent evidence. Did not consult generator reasoning, repair scripts or prior findings, and did not rerun deterministic gates. No reference-player screenshots were available among the supplied review inputs; visual judgement is of the authored blocks and referenced registry data, not rendered layout or playback.

The review treats hands-on classify interactions as inspect-and-judge practice, not execution labs. Hypothetical inspection evidence explicitly supplied in an item is accepted as evidence for that judgement.

## Learner journeys

| Tile | Main steps | Declared minutes | Assessment |
| --- | ---: | ---: | --- |
| mle.tile.052_055 | 24 | 22.7 | Script → snapshot → environment → reproduction is a coherent prerequisite progression. Each cluster teaches before checking and applying. Excess repetition and overall length weaken pacing. |
| mle.tile.056_057 | 12 | 9.7 | Artifact verification precedes registration practice; fitted-state packaging precedes package inspection. The substantive concepts and mistake-specific item feedback support the judgements. Several screens front-load too many details. |
| mle.tile.058_058 | 5 | 4.3 | Frozen policy and rate/cost formulas precede checks. Matched counts and costs agree with the registry fixture. The jump from a policy check to a large combined numeric classification merits a smaller intermediate worked example. |
| mle.tile.059_059 | 6 | 4.8 | Request limits, version resolution, container paths and terminal inspection are taught before application. The first screen carries a disproportionately long end-to-end example. |

No BLOCKING pedagogy defect was found. The keyed judgements are defensible from the teaching and supplied evidence. Option/item feedback addresses the particular errors, and linked remediation supplies the relevant mechanism. The protected-cohort visual agrees with the authored fixture; the package side-by-side supports the distinction between prediction agreement and preserved fitted state. The entry-point video adds a concrete direct-execution/import demonstration and the distinction between guarding a call and suppressing all module-level statements, rather than merely duplicating an instruction to add the guard.

## Findings

ADVISORY mle.tile.052_055/s01–s24: The 24-step, 22.7-minute journey exceeds the review's 8–14-step/about-6–12-minute target; repeated standalone misconception screens and full-process restatements add substantial reading without another judgement → Keep the plan-fixed step types for this revision, shorten s03, s09, s14 and s20 to fixture-specific evidence rather than repeated procedures, and reduce s10, s15 and s21 to one-line contrasts; request a separate upstream plan revision if the tile must meet the target rather than silently deleting or changing step types.

ADVISORY mle.tile.052_055/s05,s06,s11,s12,s17,s22,s23: Several ledes pose a different question from the interaction, and application ledes imply one defective shared scenario although items are independent; s22's latest-data premise is especially distracting beside its verified-inputs/out-of-tolerance prompt → Replace s05 lede with “The script is saved locally. Identify how to retain its committed revision.”; s11 with “Latest has changed. Identify how to verify the original snapshot.”; s22 with “Inputs and execution are verified, but the outcome is outside the supplied tolerance. Decide what to report.”; replace the listed application-step ledes with “Judge each independent excerpt against its own named criterion; do not carry one item's assumptions into another.”

ADVISORY mle.tile.056_057/s03,s04,s10,s11: Registration-check and secret-policy prompts are preceded by hash-mismatch and inference-refitting ledes, respectively, while the application items are independent → Replace s03 lede with “Latest has been overwritten. Verify the existing registered version.”; s10 with “The proposed configuration embeds credentials. Identify the permitted correction.”; replace s04 and s11 ledes with “Judge each independent excerpt against its own named criterion; do not carry one item's assumptions into another.”

ADVISORY mle.tile.056_057/s06–s09: Persistence/trust, Dockerfile construction, build/run inspection, secret handling and agreement checks are densely packed, followed by a restatement of nearly the entire workflow in s09 → Add short headings within the existing blocks (“Trusted fitted-state persistence”, “Image recipe”, “Build and inspect”, “Runtime secrets”, “Agreement assertions”); shorten s09 to the concrete fixed-input predictions [0, 1, 1] and preserved preprocessing mean 42.5, with one contrast explaining why successful startup is insufficient. Preserve all required mechanisms in s06–s08 and preserve the planned step types.

ADVISORY mle.tile.058_058/s01–s05: Five steps and 4.3 declared minutes are below the review pacing target, yet s04 concentrates rate denominators, cost weighting, undefined groups and policy preservation into one large application without a small numeric intermediate example → Within s02, add “For B, actual negatives = 1+2 = 3, so FPR = 1/3; actual positives = 1+4 = 5, so FNR = 1/5. Expected cost = 0.7×(1/3)×2 + 0.3×(1/5)×5 ≈ 0.767, above the fixed 0.5 maximum. Report the failure without changing B.” Retain the existing read-and-judge application. If 8–14 steps are mandatory for the product, route the step-count change to the upstream plan owner rather than changing fixed types here.

ADVISORY mle.tile.058_058/s04: The lede asks only whether to change B's threshold, but the independent items also judge calculations and undefined quantities → Replace it with “Judge each independent excerpt for frozen-policy compliance, conditional error rates and deployment-weighted cost.”

ADVISORY mle.tile.059_059/s01–s06: Six steps and 4.8 declared minutes are below the review target, while s01 combines an extensive supplied contract and a roughly 80-line complete workflow before s02 explains the inspection client; the load is front-heavy rather than progressively worked → Keep step types and move the terminal polling, artifact retrieval and execution-record portion of the walkthrough from s01 into s02 after its client explanation. Present the s01 contract as a compact labelled summary of input identity, image/role, channel/output and instance/runtime bounds. If the product requires 8–14 steps, request an upstream plan revision rather than adding arbitrary screens or execution tasks.

ADVISORY mle.tile.059_059/s04,s05: The ledes ask whether submission proves completion, but s04 actually tests version-preserving channel configuration and s05 contains independent request/inspection criteria → Replace s04 lede with “The channel API accepts a URI, not a version parameter. Identify how to preserve the selected input bytes.”; replace s05 lede with “Judge each independent excerpt against its own input, request-budget or terminal-output criterion.”

VERDICT: PASS
