# Stage 08 — Independent pedagogy review

VERDICT: PASS

## Scope and method

Reviewed all seven tiles as the conservative canary scope. Read the assembled `tile_lessons` in learner order, including questions, supplied practice scaffolds, feedback, remediation, visual specifications/results and video summaries/bridges. Re-derived the pedagogical judgements from `inputs/path_glossary_bundle.json` and `scenario_asset_registry.json`; did not consult author scripts, repair histories or generator reasoning, and did not rerun deterministic gates. Applied the stage evaluator and Playbook §§2, 5 and 7. This is a JSON-content review: no rendered-player screenshots or measured learner timings were supplied, so rendering and elapsed-time claims are not certified.

No BLOCKING defect identified. The findings below concern load, repetition and hint quality, not missing ML instruction, unsupported answer keys or inaccessible execution environments. Existing step types and supplied-runtime/inspect-and-judge boundaries should be preserved.

## Learner-journey assessment

| Tile | Steps | Assessment |
|---|---:|---|
| mle.tile.019_020 | 11 | Metric definitions and conditioning populations precede checks and calculation. Classification/regression distinctions and acceptance eligibility are supported by the text and registered evidence. First-screen load and repetition can be reduced. |
| mle.tile.021_023 | 15 | Training-only reference fitting, approach eligibility and the fitted estimator path each precede their assessment. Frozen validation evidence and protected-test boundaries are explicit. Large tables, long scaffolds and exact-format output requirements make this a demanding journey. |
| mle.tile.024_025 | 12 | Threshold-dependent decisions precede threshold practice; matched-cohort eligibility precedes comparison practice. Checks are defensible from taught distinctions. The comparison output format adds avoidable clerical burden. |
| mle.tile.026_028 | 17 | Failure-group analysis leads to slice evaluation and then mitigation. Eligible denominators, descriptive rather than causal conclusions, and population versus sample limitations are taught before assessment. The slice video adds a separate synthetic language-fraud example and its bridge distinguishes its limits from the text's calculations. |
| mle.tile.029_032 | 24 | Keyed logging, paired random trials, regularization and bounded search are taught before their respective checks. The logging excerpts contain enough evidence for the explicitly scoped judgements. The regularization video adds a dynamic training/validation divergence illustration, rather than supplying required instruction. The four-concept journey is long, with generic practice hints and repetitive cost instruction. |
| mle.tile.033_033 | 6 | Existing policy and supplied observations precede the check and single risk-record application. Scope deviations, redacted credential handling, task limits and sample-bounded segment evidence are supported. No padding recommended merely to reach eight steps. |
| mle.tile.034_034 | 6 | Alignment, fixed acceptance, cost arithmetic and protected-test exclusion precede supplied-output evaluation. The bounded scaffold preserves task-output evaluation rather than application construction. No padding recommended merely to reach eight steps. |

Choice-option and logging-item feedback address the actual distractor/item distinctions. Remediation restates relevant rules, including empty groups, pipeline preservation, matched cohorts and scope limitations; it is not unrelated to the targeted mistakes. The videos' bridges explicitly delimit what the clips do and do not teach. No visual/text contradiction was identified in the inspected specifications and registered fixtures.

## Findings

ADVISORY mle.tile.019_020/s01: The opening screen introduces classification metric selection, two conditioning populations, regression losses, prevalence and the calibration limitation alongside four tables; all are taught, but the first encounter is dense → Keep the classification definitions and confusion-count/metric tables in s01; move the regression residual and average tables with their MAE/MSE explanation into s02, before s04. Preserve the prevalence/calibration text and all existing facts and step types.

ADVISORY mle.tile.019_020/s03: The misconception screen largely repeats the preceding two screens without applying its distinction to an observation → Replace its prose with: “In this cohort, precision is 12/(12+3)=0.80, while recall is 12/(12+8)=0.60. The first denominator is predicted positives; the second is actual positives. Neither ratio establishes calibration of individual probability scores.”

ADVISORY mle.tile.021_023/s06: The approach grid exposes 24 columns, including multiple redundant derived metrics, next to another contract table and a computed eligibility table, making the decision path difficult to scan → In the main approach grid show alternative_id, model_family, delivery_mode, cohort_id, TP, FP, FN, TN, expected_error_cost, the six operating/compatibility flags and maintenance_responsibility; leave precision, recall, prevalence and intermediate derived denominators/rates to the computed evidence or optional detail. Retain all registered source data and assessment inputs.

ADVISORY mle.tile.021_023/s09: A long exact semicolon-separated record mixes calculations, maintenance evidence and prescribed explanatory suffixes; transcription competes with the intended approach judgement → Keep formula_entry and its required calculations, but present the existing output template in a separately labelled compact callout/example skeleton and group instructions into “calculate”, “exclude”, “select”, and “retain maintenance evidence”. Clearly separate literal required output from instructional text; do not add a new executed-evidence task or change the selection rule.

ADVISORY mle.tile.024_025/s11: The long single-cell comparison record requires repeated formatting and a fixed prose suffix in addition to rates, exclusions and ranking → Keep the existing formula_entry, grading fields and precedence, but separate the row skeleton, exclusion-precedence list and literal suffix into clearly labelled compact sections. Show one placeholder-only row skeleton, not a solved candidate, so the learner can focus on the comparison rather than reconstructing punctuation.

ADVISORY mle.tile.026_028/s16: The practice shifts from fixed deployment-class weighting used earlier to row-specific class proportions for conditional harm without a concise worked bridge; the prompt supplies the rule, so this is clarification rather than untaught assessment → Add this prose to s13: “For these supplied scope records, conditional harm uses that row’s actual-class proportions: (negatives/row total) × FPR × cost_FP + (positives/row total) × FNR × cost_FN, with zero correct-prediction cost. For an affected-subgroup row, multiply that harm by the separately supplied deployment subgroup probability to obtain its contribution. Do not substitute validation subgroup prevalence for that deployment probability.”

ADVISORY mle.tile.029_032/s05: The generic denominator/decision-input hint ladder is poorly matched to logging excerpts, although the item feedback and remediation do teach the relevant corrections → Replace the generic incorrect message with “Check the named logging requirement in each excerpt: resolved values, inspected revision and path, keyed retrieval, or metric-history interpretation.” Replace the hints with “An explicit keyword override must be the value logged; copying an expected revision is not repository inspection.” and “A run_id links the metric and artifact to retrieval; recorded.data.metrics is not the full metric history.”

ADVISORY mle.tile.029_032/s24: The learner has traversed 24 steps and four distinct concept/application cycles before one final recap; this substantially exceeds the 8–14-step pacing target and plausibly the 6–12-minute target, although no elapsed-time measurement is available → Preserve the fixed step plan, but add brief progress cues at s06, s11 and s18 (“2 of 4: repeated trials”, “3 of 4: regularization”, “4 of 4: bounded search”), shorten repeated cost/protected-test exposition to a compact reminder where previously taught, and label the tile as four short sections with resumable boundaries. Confirm actual elapsed time in the reference player before setting a duration label; do not remove required facts or replace practice with implementation/submission labs.

## Disposition

Eight ADVISORY findings; zero BLOCKING findings. Review completed honestly. Advisory-only content passes this stage; suggested improvements do not require re-deriving the ML facts or changing the fixed practice plan.

VERDICT: PASS
