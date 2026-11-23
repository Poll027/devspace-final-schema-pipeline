# EVALUATOR PACKET — Metrics and acceptance (mle.tile.019_020)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.task_metric_selection — Select task-appropriate classification or regression metrics
B = mle.model_acceptance_criteria — Define measurable model acceptance criteria from task objectives

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.task_metric_selection)   objective: Choose an evaluation measure whose conditioning population and error consequences match the task.
A.f1: Select classification metrics in relation to task consequences, class balance and the costs of false positives and false negatives, rather than relying on raw accuracy alone.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f2: Precision = TP/(TP+FP) is the proportion of predicted positives that are actual positives, while recall = TP/(TP+FN) is the proportion of actual positives detected.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f3: For regression, mean absolute error averages absolute prediction errors and mean squared error averages squared errors; the latter increases the influence of large errors.   [sources: scikit_learn_user_guide#modules/model_evaluation.html — 3.4.6 Regression metrics]
A.f4: Class prevalence is the proportion of actual positives in the validation population and helps interpret metrics from that population.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f5: Conditional frequencies from a validation confusion table describe outcomes in that cohort; they do not establish that a model’s individual probability scores are calibrated.   [sources: scikit_learn_user_guide#modules/calibration.html — 1.16 Probability calibration]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Metrics and Acceptance Criteria.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Use the supplied late-order validation counts TP=12, FP=3, FN=8 and TN=77 to calculate precision, recall and class prevalence. Express precision and recall as conditional probabilities with their conditioning populations identified. Given a task consequence statement that prioritizes catching actual late orders over avoiding unnecessary alerts, select and justify one classification metric without claiming individual probability-score calibration.  SUCCESS: Precision is 12/15 = 0.80, interpreted as P(actual positive | predicted positive); recall is 12/20 = 0.60, interpreted as P(predicted positive | actual positive); class prevalence is 20/100 = 0.20. Recall is selected because missed late orders carry the stated greater consequence, rather than because of raw accuracy. The justification states that these validation-cohort frequencies do not establish calibration of individual probability scores.
ASSESSMENT ANCHOR: choose_classification_metric_by_error_consequences facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: choose_regression_metric_by_error_consequences facts=['f3']
ASSESSMENT ANCHOR: interpret_cohort_metrics_without_claiming_score_calibration facts=['f2', 'f4', 'f5']

## SOURCE FACTS — B (mle.model_acceptance_criteria)   objective: Precommit measurable cost, predictive and operating limits for accepting a model.
B.f1: State a measurable predictive-quality acceptance requirement before comparing candidates, along with the supplied deployment compatibility requirements.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: Use the supplied error costs and deployment class probabilities as fixed decision inputs rather than choosing them after seeing which candidate benefits.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f5: An expected-cost requirement can be stated as computed expected cost <= the predeclared permitted bound; operating limits remain separate eligibility conditions.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Metrics and Acceptance Criteria.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition, mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (formula): Write a precommitted acceptance contract for the order prediction task using supplied deployment probabilities, error costs, conditional error probabilities, a permitted expected-cost bound, and operating limits. State the zero-cost assumption for correct predictions, calculate expected error cost, and express predictive acceptance as an inequality separate from each supplied operating requirement.  SUCCESS: The contract fixes all supplied decision inputs before candidate results are compared. Using deployment probabilities 0.80 and 0.20, FPR 0.10, FNR 0.20, and error costs 1 and 5, it calculates expected error cost as 0.28 and states the predeclared requirement expected error cost <= 0.30. It records each supplied operating limit independently, without inventing a latency limit or treating predictive acceptance as overall eligibility. It identifies the conditioning denominators for FPR and FNR and marks a rate unresolved if its conditioning group is empty.
ASSESSMENT ANCHOR: precommit_quality_and_operating_requirements facts=['f1', 'f2']
ASSESSMENT ANCHOR: calculate_conditioned_error_rates_and_identify_undefined_rates facts=['f3']
ASSESSMENT ANCHOR: express_expected_error_cost_acceptance_with_separate_operating_limits facts=['f2', 'f4', 'f5']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.acceptance_terms: Expected-cost contributions by actual class — columns: actual_label(categorical,digits-as-label), deployment_class_probability(numerical), conditional_error_rate(numerical), error_cost(numerical), conditioning_count(numerical), weighted_contribution(numerical)
   [0,0.8,0.1,1,80,0.08000000000000002]
   [1,0.2,0.2,5,20,0.20000000000000004]
   variant v.empty_acceptance_positive: 3 ops; planted: 
ds.confusion_counts: Late-order confusion cells — columns: outcome(categorical), actual_label(categorical,digits-as-label), predicted_label(categorical,digits-as-label), count(numerical)
   ["TP",1,1,12]
   ["FP",0,1,3]
   ["FN",1,0,8]
   ["TN",0,0,77]
ds.metric_summary: Confusion-table denominators and computed metrics — columns: cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical)
   ["metric_example",12,3,8,77,20,80,100,0.8,0.6,0.2,0.0375,0.4,0.43000000000000005]
ds.regression_error_summary: Regression error averages — columns: MAE(numerical), MSE(numerical)
   [2.0,5.0]
ds.regression_errors: Two regression residuals — columns: observation_id(identifier), error(numerical), absolute_error(numerical), squared_error(numerical)
   ["reg_error_1",1,1,1]
   ["reg_error_2",3,3,9]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Define measurable model acceptance criteria from task objectives; Diagnose training failures from loss and gradient behavior; Document model limitations and foreseeable misuse under an existing risk policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Fit and predict with a bounded scikit-learn baseline workflow; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction errors

## LESSON, in learner order

### s01 · explainer · Cohort evidence is bounded
(intro) Few total late-order mistakes can still hide missed positives. Choose the metric for the task’s error consequences and conditioning population, not accuracy alone. ⟦A:tb1⟧
(definition) Class balance and false-positive/false-negative costs matter when choosing classification metrics. Precision, TP/(TP+FP), asks how many predicted positives are actual positives. Recall, TP/(TP+FN), asks how many actual positives were detected. For regression, MAE averages absolute errors; MSE averages squared errors, giving larger errors more influence. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Validation prevalence is actual positives divided by the validation population. Use it to interpret cohort metrics. Confusion-table conditional frequencies describe this cohort; they do not demonstrate calibration of individual probability scores. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.confusion_counts cols=['outcome', 'actual_label', 'predicted_label', 'count'] ] caption: Late-order confusion cells: predicted-positive denominator 15; actual-positive denominator 20; cohort denominator 100.
[TABLE ds.metric_summary cols=['actual_positive_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence'] ] caption: Confusion-table denominators and computed metrics
[TABLE ds.regression_errors cols=['observation_id', 'error', 'absolute_error', 'squared_error'] ] caption: Two regression residuals
[TABLE ds.regression_error_summary cols=['MAE', 'MSE'] ] caption: Regression error averages

### s02 · explainer · Read the denominators
(example) Read the confusion cells with their actual and predicted labels. Precision uses predicted positives as its denominator; recall uses actual positives. Prevalence uses the whole validation cohort. The separate regression tables show absolute and squared errors and their averages. Keep task consequences beside the numbers: these cohort summaries do not prove that an individual probability score is calibrated. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · Do not swap the groups
(misconception) Precision and recall use different denominators. Neither replaces the other, and cohort frequencies do not prove probability-score calibration. ⟦A.f2 A.f5 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s05 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.

### s06 · explainer · Cost and eligibility
(intro) Declare quality and operating requirements before inspecting candidate results. The favored candidate must not determine the acceptance contract. ⟦B:tb1⟧
(definition) Precommit a measurable predictive-quality requirement and the supplied deployment compatibility requirements. Keep supplied error costs and deployment class probabilities fixed. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. A rate with an empty conditioning group is undefined. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Require expected cost <= the predeclared bound. Operating limits are separate eligibility conditions. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.acceptance_terms cols=['actual_label', 'deployment_class_probability', 'conditional_error_rate', 'error_cost', 'conditioning_count', 'weighted_contribution'] ] caption: Expected-cost contributions by actual class
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Sum the cost terms; operating eligibility remains separate.
  produced by sql: SELECT SUM(t.weighted_contribution) AS expected_cost, c.expected_cost_bound, SUM(t.weighted_contribution) <= c.expected_cost_bound AS predictive_bound_met, c.operating_limit AS separate_operating_limit FROM terms t CROSS JOIN contract c GROUP BY c.expected_cost_bound, c.operating_limit

### s07 · explainer · Inspect the acceptance contract
(example) The cost-term table keeps the actual-class conditioning counts, supplied deployment probabilities and error costs separate. Add the weighted contributions and compare with the fixed bound in the acceptance contract. Passing that predictive requirement does not override a latency limit. An empty actual-positive group leaves FNR undefined; do not substitute zero or change deployment probabilities to favor a candidate. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s08 · explainer · Cost is not blanket acceptance
(misconception) Low cost is not blanket acceptance. Keep predictive and operating eligibility separate, and do not change supplied probabilities or costs to favor a candidate. ⟦B.f1 B.f2 B.f5 B:tb5⟧

### s09 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s10 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s11 · recap · Keep these distinctions
(takeaway) Choose metrics by task consequences and their denominators. Cohort frequencies do not prove score calibration. Precommit quality, costs and deployment probabilities; keep operating eligibility separate and empty-group rates undefined. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 B.f1 B.f2 B.f3 B.f4 B.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Establish a simple training-fitted reference baseline.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — choose the question
(misconception) Contrast predicted positives with actual positives: precision starts with the first group, recall with the second. Neither group ratio demonstrates score calibration. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(definition) Class balance and false-positive/false-negative costs matter when choosing classification metrics. Precision, TP/(TP+FP), asks how many predicted positives are actual positives. Recall, TP/(TP+FN), asks how many actual positives were detected. For regression, MAE averages absolute errors; MSE averages squared errors, giving larger errors more influence. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Validation prevalence is actual positives divided by the validation population. Use it to interpret cohort metrics. Confusion-table conditional frequencies describe this cohort; they do not demonstrate calibration of individual probability scores. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.confusion_counts cols=['outcome', 'actual_label', 'predicted_label', 'count'] ] caption: Late-order confusion cells
### r02 · Revisit: the practice — choose the question
(misconception) Contrast predicted positives with actual positives: precision starts with the first group, recall with the second. Neither group ratio demonstrates score calibration. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(definition) Class balance and false-positive/false-negative costs matter when choosing classification metrics. Precision, TP/(TP+FP), asks how many predicted positives are actual positives. Recall, TP/(TP+FN), asks how many actual positives were detected. For regression, MAE averages absolute errors; MSE averages squared errors, giving larger errors more influence. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Validation prevalence is actual positives divided by the validation population. Use it to interpret cohort metrics. Confusion-table conditional frequencies describe this cohort; they do not demonstrate calibration of individual probability scores. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.confusion_counts cols=['outcome', 'actual_label', 'predicted_label', 'count'] ] caption: Late-order confusion cells
### r03 · Revisit: the check — precommit acceptance
(misconception) Contrast passing the predictive-cost bound with being deployment-eligible: a separate operating failure still excludes the candidate. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(definition) Precommit a measurable predictive-quality requirement and the supplied deployment compatibility requirements. Keep supplied error costs and deployment class probabilities fixed. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. A rate with an empty conditioning group is undefined. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Require expected cost <= the predeclared bound. Operating limits are separate eligibility conditions. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.acceptance_terms cols=['actual_label', 'deployment_class_probability', 'conditional_error_rate', 'error_cost', 'conditioning_count', 'weighted_contribution'] ] caption: Expected-cost contributions by actual class
### r04 · Revisit: the practice — precommit acceptance
(misconception) Contrast passing the predictive-cost bound with being deployment-eligible: a separate operating failure still excludes the candidate. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(definition) Precommit a measurable predictive-quality requirement and the supplied deployment compatibility requirements. Keep supplied error costs and deployment class probabilities fixed. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. A rate with an empty conditioning group is undefined. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Require expected cost <= the predeclared bound. Operating limits are separate eligibility conditions. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.acceptance_terms cols=['actual_label', 'deployment_class_probability', 'conditional_error_rate', 'error_cost', 'conditioning_count', 'weighted_contribution'] ] caption: Expected-cost contributions by actual class

=========

# EVALUATOR PACKET — Establish a modeling baseline (mle.tile.021_023)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.reference_baseline — Establish a simple reference prediction baseline
B = mle.model_approach_decision — Justify classical versus neural modeling using validation quality, latency and cost evidence
C = mle.sklearn_baseline_workflow — Fit and predict with a bounded scikit-learn baseline workflow

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.reference_baseline)   objective: Train and freeze a simple reference, then evaluate its declared validation quantities.
A.f1: DummyClassifier supplies simple reference rules such as most_frequent, prior and constant; DummyRegressor(strategy="mean") predicts the training-target mean.   [sources: scikit_learn_user_guide#modules/model_evaluation.html — 3.4.8 Dummy estimators]
A.f2: Fit the reference estimator on training inputs and targets, then freeze it and call predict on the separate validation cohort.   [sources: scikit_learn_user_guide#modules/model_evaluation.html — 3.4.8 Dummy estimators]
A.f3: Measure the predeclared validation metric on the baseline’s predictions and actual targets, rather than reporting its training-only result.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f5: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
A.f6: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f7: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f8: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f9: For a classification reference, report the training target-class count divided by the training total, without replacing it with validation or protected-test prevalence.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Establish a Modeling Baseline.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition, mle.task_metric_selection, mle.deployment_matched_splits. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports that establishes a most-frequent classification reference from the supplied training cohort. Calculate the training target mean, population standard deviation and class proportions. Fit once on training, predict the separate validation cohort, and return its predeclared accuracy, conditional error rates and expected error cost using the supplied deployment probabilities and error costs. Preserve the measured validation reference without accessing protected test data.  SUCCESS: The function reports training positive prevalence 0.20 and negative prevalence 0.80 for the eight-negative, two-positive fixture. Its frozen reference predicts the training majority class for every validation observation. Accuracy uses validation predictions and actual targets; FPR and FNR use their respective actual-class denominators. Empty conditioning groups are reported as undefined, not zero, and any cost requiring an undefined rate is also reported as undefined. The returned record contains the training statistics, fixed reference rule, validation metric and applicable error-cost calculation.
ASSESSMENT ANCHOR: define_task_compatible_reference facts=['f1', 'f9']
ASSESSMENT ANCHOR: fit_training_only_and_freeze_reference facts=['f2', 'f8']
ASSESSMENT ANCHOR: measure_predeclared_validation_metric facts=['f3']
ASSESSMENT ANCHOR: justify_reference_with_training_target_statistics facts=['f4', 'f5', 'f9']
ASSESSMENT ANCHOR: calculate_conditional_error_rates_and_expected_cost facts=['f6', 'f7']

## SOURCE FACTS — B (mle.model_approach_decision)   objective: Select a supplied modeling approach from matched quality, operating and ownership evidence.
B.f1: Compare alternatives on the same intended evaluation task and cohort, and check model quality and deployment compatibility before promotion.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: Different inference options have different latency, scale and cost characteristics, so the supplied operating constraints affect eligibility.   [sources: sagemaker_model_deployment#Deploy models for inference]
B.f3: Reject supplied alternatives violating precommitted quality or operating limits, then choose among eligible alternatives using the fixed decision rule.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f5: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f6: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
B.f7: A custom classical or neural model leaves task-model implementation and training choices with the model owner, while a managed service can supply training/hosting infrastructure; compare maintenance responsibility as well as predictive and operating evidence.   [sources: sagemaker_developer_guide#how-it-works-mlconcepts.html — The machine learning workflow]
B.f8: Address classical-versus-neural and custom-versus-managed trade-offs from matched records, without fitting new alternatives to manufacture comparison evidence.   [sources: google_mlops_pipelines#Data and model validation]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Establish a Modeling Baseline.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria, mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Use a supplied spreadsheet containing matched validation confusion counts and operating records for a custom classical model, a custom neural model and a managed ML service. Verify the shared task and cohort; derive FPR, FNR and expected error cost using supplied deployment class probabilities and false-positive and false-negative costs, with zero cost for correct predictions. Apply precommitted quality, latency, scale, training-cost, serving-cost, maintenance and deployment-compatibility limits, then freeze one eligible alternative using the supplied fixed decision rule. Justify both classical-versus-neural and custom-versus-managed trade-offs without fitting alternatives or accessing protected test data.  SUCCESS: The completed spreadsheet uses FP/(FP+TN) and FN/(FN+TP), marks rates with empty conditioning groups as undefined rather than zero, and calculates expected error cost as P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN wherever rates are defined. Eligibility decisions follow every supplied limit; no undefined required rate is treated as evidence of passing a limit. The frozen selection follows the fixed decision rule among eligible alternatives, with a rationale citing matched quality, operating evidence and maintenance responsibility across all three records. No new fitting or protected-test observations are used.
ASSESSMENT ANCHOR: verify_matched_task_cohort_and_deployment_compatibility facts=['f1']
ASSESSMENT ANCHOR: derive_conditional_error_rates_and_identify_undefined_rates facts=['f4']
ASSESSMENT ANCHOR: calculate_prevalence_weighted_expected_error_cost facts=['f4', 'f5']
ASSESSMENT ANCHOR: reject_ineligible_alternatives_and_apply_fixed_decision_rule facts=['f2', 'f3']
ASSESSMENT ANCHOR: justify_classical_neural_and_custom_managed_tradeoffs facts=['f7', 'f8']
ASSESSMENT ANCHOR: freeze_supplied_approach_without_new_fitting_or_protected_test_access facts=['f6', 'f8']

## SOURCE FACTS — C (mle.sklearn_baseline_workflow)   objective: Fit a bounded classical estimator and compare its validation predictions with the fixed reference.
C.f1: For the binary classification baseline, use from sklearn.linear_model import LogisticRegression; estimator = LogisticRegression(random_state=0); estimator.fit(X_train, y_train), with numeric X_train of shape (n_samples, n_features) and aligned class-label y_train of shape (n_samples,).   [sources: scikit_learn_user_guide#https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html — Examples; fit; predict]
C.f2: Obtain predictions with estimator.predict(X_validation) and compare them against the corresponding y_validation observations.   [sources: scikit_learn_user_guide#https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html — Examples; fit; predict]
C.f3: When training used fitted preprocessing, predict through the fitted pipeline so validation inputs receive the same feature representation.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
C.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
C.f5: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Establish a Modeling Baseline.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_shape_dtype, mle.deployment_matched_splits, mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function and its required imports within the supplied runtime scaffolding. Verify the dimensions and declared observation alignment of the six-order, two-feature training fixture and corresponding validation inputs. Fit the declared LogisticRegression baseline, obtain validation predictions through the fitted pipeline when preprocessing is present, and calculate binary error counts, conditional error rates and expected error cost using supplied deployment probabilities and error costs.  SUCCESS: The function verifies X_train has shape (6, 2), y_train has shape (6,), and validation inputs and labels have corresponding observations. It fits the declared estimator, returns aligned validation predictions, calculates FPR and FNR using the correct conditioning groups, and computes expected error cost when both rates are defined. Empty conditioning groups are reported as undefined rather than assigned a rate or used to produce a numerical expected cost.
ASSESSMENT ANCHOR: fit_baseline_with_aligned_numeric_inputs facts=['f1']
ASSESSMENT ANCHOR: obtain_observation_aligned_validation_predictions facts=['f2']
ASSESSMENT ANCHOR: reuse_fitted_preprocessing_for_validation_predictions facts=['f3']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.approach_records: Classical, neural, and managed operating records — columns: alternative_id(identifier), model_family(categorical), delivery_mode(categorical), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), latency_requirement_met(categorical), scale_requirement_met(categorical), training_cost_requirement_met(categorical), serving_cost_requirement_met(categorical), maintenance_requirement_met(categorical), deployment_compatibility_met(categorical), maintenance_responsibility(text)
   ["custom_classical","classical","custom","orders_100",16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true,true,true,true,true,true,"owner maintains task model and infrastructure"]
   ["custom_neural","neural","custom","orders_100",16,4,4,76,20,80,100,0.8,0.8,0.2,0.05,0.2,0.24000000000000005,false,true,true,true,true,true,"owner maintains task model and infrastructure"]
   ["managed_service","classical","managed","orders_100",16,12,4,68,20,80,100,0.5714285714285714,0.8,0.2,0.15,0.2,0.32000000000000006,true,true,true,true,true,true,"service supplies training or hosting infrastructure; owner retains custom task-model choices"]
ds.orders_train: Six-order estimator training inputs — columns: observation_id(identifier), feature_1(numerical), feature_2(numerical), y_train(categorical,digits-as-label)
   ["train_1",-3.0,0.0,0]
   ["train_2",-2.0,2.0,0]
   ["train_3",-1.0,4.0,0]
   ["train_4",0.0,1.0,1]
   ["train_5",1.0,3.0,1]
   ["train_6",2.0,0.0,1]
ds.orders_validation: Held-out aligned estimator inputs — columns: observation_id(identifier), feature_1(numerical), feature_2(numerical), y_validation(categorical,digits-as-label)
   ["validation_1",-2.75,0.0,0]
   ["validation_2",-1.75,3.0,0]
   ["validation_3",-0.75,1.0,0]
   ["validation_4",0.25,4.0,1]
   ["validation_5",1.25,2.0,1]
   ["validation_6",2.25,0.0,1]
   variant v.validation_no_positives: 1 ops; planted: 
   variant v.validation_no_negatives: 1 ops; planted: 
   variant v.validation_bad_alignment: 1 ops; planted: 
ds.reference_train: Reference-only training cohort — columns: observation_id(identifier), feature_1(numerical), y_train(categorical,digits-as-label)
   ["ref_train_1",0.0,0]
   ["ref_train_2",1.0,0]
   ["ref_train_3",2.0,0]
   ["ref_train_4",3.0,0]
   ["ref_train_5",4.0,0]
   ["ref_train_6",5.0,0]
   ["ref_train_7",6.0,0]
   ["ref_train_8",7.0,0]
ds.regression_targets: Separate mean-reference targets — columns: observation_id(identifier), target(numerical)
   ["reg_train_1",2]
   ["reg_train_2",4]
   ["reg_train_3",6]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Fit and predict with a bounded scikit-learn baseline workflow; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction errors for recurring failure mode

## LESSON, in learner order

### s01 · explainer · Statistics and conditioning
(intro) Establish a simple reference before judging more elaborate predictions. Fit it on training observations and evaluate its frozen predictions on validation. ⟦A:tb1⟧
(mechanism) DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean. Fit on training inputs and targets, freeze the estimator, then predict on separate validation observations. Report the predeclared metric against validation targets, not a training-only result. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use np.mean(numeric_values) for the selected numeric observations’ arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when an N−1 divisor is required. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups give undefined rates. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[CODE python]
import numpy as np
from sklearn.dummy import DummyClassifier, DummyRegressor

def evaluate_reference(X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN, numeric_values):
    reference = DummyClassifier(strategy="most_frequent")
    reference.fit(X_train, y_train)
    predictions = reference.predict(X_validation)
    training_positive_proportion = np.sum(y_train == 1) / len(y_train)
    training_target_mean = np.mean(numeric_values)
    training_target_std = np.std(numeric_values, ddof=0)
    FP = np.sum((y_validation == 0) & (predictions == 1))
    TN = np.sum((y_validation == 0) & (predictions == 0))
    FN = np.sum((y_validation == 1) & (predictions == 0))
    TP = np.sum((y_validation == 1) & (predictions == 1))
    FPR = FP / (FP + TN) if FP + TN else None
    FNR = FN / (FN + TP) if FN + TP else None
    expected_cost = (p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
                     if FPR is not None and FNR is not None else None)
    return {
        'training_shape': X_train.shape,
        'training_label_shape': y_train.shape,
        'validation_shape': X_validation.shape,
        'predictions': predictions,
        'validation_labels': y_validation,
        'FP': FP,
        'TN': TN,
        'FN': FN,
        'TP': TP,
        'actual_negative_denominator': FP + TN,
        'actual_positive_denominator': FN + TP,
        'FPR': FPR,
        'FNR': FNR,
        'expected_cost': expected_cost,
        'training_positive_proportion': training_positive_proportion,
        'training_target_mean': training_target_mean,
        'training_target_std_ddof0': training_target_std,
    }
  annotations: []
[TABLE ds.reference_train cols=['observation_id', 'feature_1', 'y_train'] ] caption: Reference-only training cohort
[TABLE ds.regression_targets cols=['observation_id', 'target'] ] caption: Separate mean-reference targets
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract

### s02 · explainer · Keep training and test boundaries
(mechanism) With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations must not fit preprocessing, choose a model or tune settings: that leaks information. For a classification reference, report training target-class count/training total, not validation or protected-test prevalence. ⟦A.f7 A.f8 A.f9 A:tb4⟧

### s03 · explainer · A reference needs validation
(example) The registered training labels determine the reference rule and training class proportions. Keep those statistics separate from validation prevalence. Freeze the fitted reference before predicting on the corresponding validation inputs. Evaluate those predictions with the declared metric and cost assumptions; retain actual-class denominators and mark empty groups undefined. Training-target mean and spread describe the chosen training observations, not the held-out result. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb5⟧
(misconception) A reference still needs held-out evaluation. Training proportions are not validation prevalence, and fitting or selecting with protected-test observations leaks information. ⟦A.f2 A.f3 A.f8 A:tb6⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s05 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s06 · explainer · Conditioned deployment cost
(intro) Use supplied matched records to justify an approach choice. Predictive quality, deployment fit and operating evidence all matter before promotion. ⟦B:tb1⟧
(mechanism) Compare alternatives on the same intended task and cohort. Check quality and deployment compatibility. Inference options differ in latency, scale and cost; supplied constraints govern eligibility. Reject records failing precommitted quality or operating limits, then apply the fixed decision rule among eligible alternatives. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Do not use protected-test observations to fit preprocessing, choose models or tune settings: that leaks information. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"ds.approach_records","columns":["alternative_id","model_family","delivery_mode","cohort_id","TP","FP","FN","TN","actual_positive_count","actual_negative_count","cohort_count","precision","recall","validation_prevalence","FPR","FNR","expected_error_cost","latency_requirement_met","scale_requirement_met","training_cost_requirement_met","serving_cost_requirement_met","maintenance_requirement_met","deployment_compatibility_met","maintenance_responsibility"]},"range":"A1:X4","show_formula_bar":true,"lineage":{"concept_ids":["mle.model_approach_decision"],"teaching_block_ids":[],"fact_ids":[],"anchors":["mle.model_approach_decision#visual"]}}
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.latency_requirement_met = TRUE AND r.scale_requirement_met = TRUE AND r.training_cost_requirement_met = TRUE AND r.serving_cost_requirement_met = TRUE AND r.maintenance_requirement_met = TRUE AND r.deployment_compatibility_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.alternative_id AS tie_order 
FROM records r CROSS JOIN contract c  
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT alternative_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.alternative_id, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.alternative_id=b.alternative_id ORDER BY a.tie_order

### s07 · explainer · Exclude before ranking
(mechanism) Custom classical or neural models leave task-model implementation and training choices with the model owner. A managed service can supply training/hosting infrastructure. Compare maintenance responsibility alongside predictive and operating evidence. Address classical/neural and custom/managed trade-offs from matched records, without fitting new alternatives to manufacture evidence. ⟦B.f7 B.f8 B:tb4⟧
(example) The approach records keep model family, delivery mode, cohort, confusion counts and operating checks together. Use the same supplied deployment probabilities and costs for every row. Exclude an alternative that fails a fixed requirement before applying the selection rule. A lower cost cannot erase an operating failure; maintenance responsibility remains part of the comparison. ⟦B.f1 B.f2 B.f3 B.f5 B.f6 B.f7 B.f8 B:tb5⟧
(misconception) Choose only among eligible matched records. A favorable predictive number cannot excuse a failed operating requirement or replace maintenance evidence. ⟦B.f1 B.f2 B.f7 B:tb6⟧

### s08 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s09 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.

### s10 · explainer · Evaluate conditional errors
(intro) Connect aligned numeric training data to a bounded LogisticRegression baseline, then inspect its held-out predictions under the declared evaluation. ⟦C:tb1⟧
(mechanism) Use from sklearn.linear_model import LogisticRegression, create estimator = LogisticRegression(random_state=0), and call estimator.fit(X_train, y_train). Numeric X_train has shape (n_samples, n_features); aligned class labels y_train have shape (n_samples,). Compare estimator.predict(X_validation) with corresponding y_validation. If fitting used preprocessing, predict through the fitted pipeline to preserve the feature representation. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f4 C.f5 C:tb3⟧
[CODE python]
import numpy as np
from sklearn.linear_model import LogisticRegression

def evaluate_baseline(X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN):
    estimator = LogisticRegression(random_state=0)
    estimator.fit(X_train, y_train)
    predictions = estimator.predict(X_validation)
    # If training used preprocessing, use the fitted pipeline's predict instead.
    FP = np.sum((y_validation == 0) & (predictions == 1))
    TN = np.sum((y_validation == 0) & (predictions == 0))
    FN = np.sum((y_validation == 1) & (predictions == 0))
    TP = np.sum((y_validation == 1) & (predictions == 1))
    FPR = FP / (FP + TN) if FP + TN else None
    FNR = FN / (FN + TP) if FN + TP else None
    expected_cost = (p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
                     if FPR is not None and FNR is not None else None)
    return {
        'training_shape': X_train.shape,
        'training_label_shape': y_train.shape,
        'validation_shape': X_validation.shape,
        'predictions': predictions,
        'validation_labels': y_validation,
        'FP': FP,
        'TN': TN,
        'FN': FN,
        'TP': TP,
        'actual_negative_denominator': FP + TN,
        'actual_positive_denominator': FN + TP,
        'FPR': FPR,
        'FNR': FNR,
        'expected_cost': expected_cost,
    }
  annotations: []
[TABLE ds.orders_train cols=['observation_id', 'feature_1', 'feature_2', 'y_train'] ] caption: Six-order estimator training inputs
[TABLE ds.orders_validation cols=['observation_id', 'feature_1', 'feature_2', 'y_validation'] ] caption: Held-out aligned estimator inputs
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract

### s11 · explainer · Inspect the held-out path
(example) The training and validation tables expose observation identities, numeric features and aligned labels. Fitting establishes estimator state; prediction applies it to validation inputs; evaluation compares outputs with matching held-out labels. Shape agreement alone does not establish observation correspondence. Use the fitted pipeline when preprocessing belongs to it. Inspect conditional error counts and the fixed cost calculation rather than stopping when fit returns. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4⟧

### s12 · explainer · Prediction is not a verdict
(misconception) predict is not a quality verdict. Use matching held-out labels and the fixed evaluation rule; bypassing fitted preprocessing changes the representation. ⟦C.f2 C.f3 C:tb5⟧

### s13 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s14 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s15 · recap · Keep these distinctions
(takeaway) Fit a simple reference on training and evaluate frozen validation predictions. Keep training statistics distinct from held-out evidence. Compare approaches on matched task/cohort records and fixed eligibility rules. Preserve aligned features, labels and fitted preprocessing in the LogisticRegression path. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 C.f1 C.f2 C.f3 C.f4 C.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Up next: Turn classification scores into explicit threshold-dependent decisions.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — start with a reference
(misconception) Contrast training class proportions with validation prevalence. Fit the reference on training, but judge its frozen predictions with matching validation targets. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4⟧
(mechanism) DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean. Fit on training inputs and targets, freeze the estimator, then predict on separate validation observations. Report the predeclared metric against validation targets, not a training-only result. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use np.mean(numeric_values) for the selected numeric observations’ arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when an N−1 divisor is required. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups give undefined rates. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations must not fit preprocessing, choose a model or tune settings: that leaks information. For a classification reference, report training target-class count/training total, not validation or protected-test prevalence. ⟦A.f7 A.f8 A.f9 A:tb4⟧
[TABLE ds.reference_train cols=['observation_id', 'feature_1', 'y_train'] ] caption: Reference-only training cohort
### r02 · Revisit: the practice — start with a reference
(misconception) Contrast training class proportions with validation prevalence. Fit the reference on training, but judge its frozen predictions with matching validation targets. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4⟧
(mechanism) DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean. Fit on training inputs and targets, freeze the estimator, then predict on separate validation observations. Report the predeclared metric against validation targets, not a training-only result. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use np.mean(numeric_values) for the selected numeric observations’ arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when an N−1 divisor is required. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups give undefined rates. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations must not fit preprocessing, choose a model or tune settings: that leaks information. For a classification reference, report training target-class count/training total, not validation or protected-test prevalence. ⟦A.f7 A.f8 A.f9 A:tb4⟧
[TABLE ds.reference_train cols=['observation_id', 'feature_1', 'y_train'] ] caption: Reference-only training cohort
### r03 · Revisit: the check — matched approach evidence
(misconception) Contrast an attractive cost with an eligible approach. Matched task/cohort and every fixed quality/operating requirement come before selection. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb2 B:tb3 B:tb4⟧
(mechanism) Compare alternatives on the same intended task and cohort. Check quality and deployment compatibility. Inference options differ in latency, scale and cost; supplied constraints govern eligibility. Reject records failing precommitted quality or operating limits, then apply the fixed decision rule among eligible alternatives. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Do not use protected-test observations to fit preprocessing, choose models or tune settings: that leaks information. ⟦B.f4 B.f5 B.f6 B:tb3⟧
(mechanism) Custom classical or neural models leave task-model implementation and training choices with the model owner. A managed service can supply training/hosting infrastructure. Compare maintenance responsibility alongside predictive and operating evidence. Address classical/neural and custom/managed trade-offs from matched records, without fitting new alternatives to manufacture evidence. ⟦B.f7 B.f8 B:tb4⟧
[TABLE ds.approach_records cols=['alternative_id', 'model_family', 'delivery_mode', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met', 'maintenance_responsibility'] ] caption: Classical, neural, and managed operating records
### r04 · Revisit: the practice — matched approach evidence
(misconception) Contrast an attractive cost with an eligible approach. Matched task/cohort and every fixed quality/operating requirement come before selection. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb2 B:tb3 B:tb4⟧
(mechanism) Compare alternatives on the same intended task and cohort. Check quality and deployment compatibility. Inference options differ in latency, scale and cost; supplied constraints govern eligibility. Reject records failing precommitted quality or operating limits, then apply the fixed decision rule among eligible alternatives. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Do not use protected-test observations to fit preprocessing, choose models or tune settings: that leaks information. ⟦B.f4 B.f5 B.f6 B:tb3⟧
(mechanism) Custom classical or neural models leave task-model implementation and training choices with the model owner. A managed service can supply training/hosting infrastructure. Compare maintenance responsibility alongside predictive and operating evidence. Address classical/neural and custom/managed trade-offs from matched records, without fitting new alternatives to manufacture evidence. ⟦B.f7 B.f8 B:tb4⟧
[TABLE ds.approach_records cols=['alternative_id', 'model_family', 'delivery_mode', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met', 'maintenance_responsibility'] ] caption: Classical, neural, and managed operating records
### r05 · Revisit: the check — a bounded fitted baseline
(misconception) Contrast predictions with evaluated predictions: matching held-out labels and the fitted representation are needed before a quality verdict. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Use from sklearn.linear_model import LogisticRegression, create estimator = LogisticRegression(random_state=0), and call estimator.fit(X_train, y_train). Numeric X_train has shape (n_samples, n_features); aligned class labels y_train have shape (n_samples,). Compare estimator.predict(X_validation) with corresponding y_validation. If fitting used preprocessing, predict through the fitted pipeline to preserve the feature representation. ⟦C.f1 C.f2 C.f3 C:tb2⟧
[TABLE ds.orders_train cols=['observation_id', 'feature_1', 'feature_2', 'y_train'] ] caption: Six-order estimator training inputs
### r06 · Revisit: the practice — a bounded fitted baseline
(misconception) Contrast predictions with evaluated predictions: matching held-out labels and the fitted representation are needed before a quality verdict. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3⟧
(mechanism) Use from sklearn.linear_model import LogisticRegression, create estimator = LogisticRegression(random_state=0), and call estimator.fit(X_train, y_train). Numeric X_train has shape (n_samples, n_features); aligned class labels y_train have shape (n_samples,). Compare estimator.predict(X_validation) with corresponding y_validation. If fitting used preprocessing, predict through the fitted pipeline to preserve the feature representation. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f4 C.f5 C:tb3⟧
[TABLE ds.orders_train cols=['observation_id', 'feature_1', 'feature_2', 'y_train'] ] caption: Six-order estimator training inputs

=========

# EVALUATOR PACKET — Thresholds and candidate comparison (mle.tile.024_025)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.decision_threshold_selection — Select a decision threshold using validation data and task costs
B = mle.validation_candidate_comparison — Compare model candidates against a baseline using validation evidence before freezing the choice

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.decision_threshold_selection)   objective: Select and freeze a classification cutoff under precommitted validation cost constraints.
A.f1: A classification score and a class decision are different outputs; the decision is obtained by comparing the score with a threshold.   [sources: scikit_learn_user_guide#modules/classification_threshold.html — 3.3.1 The problem; 3.3.2 Post-tuning the decision threshold]
A.f2: For binary scikit-learn predictions, probability scores ordinarily use a 0.5 cutoff and decision_function scores a zero cutoff; an explicitly chosen task threshold changes that decision.   [sources: scikit_learn_user_guide#modules/classification_threshold.html — 3.3.1 The problem; 3.3.2 Post-tuning the decision threshold]
A.f3: For each supplied candidate threshold, form predicted labels, then count TP, FP, TN and FN against validation labels at that threshold.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: Choose the eligible threshold with the minimum predeclared expected cost on validation evidence and freeze it before protected testing.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f5: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f6: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f7: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Threshold and Candidate Selection.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function, including required imports, that evaluates supplied candidate thresholds against validation scores and binary labels. Compute TP, FP, TN, FN, conditional FPR and FNR, and expected cost using supplied deployment class probabilities and fixed error costs. Apply supplied eligibility limits and retain the minimum-cost eligible threshold through the existing scaffolding, without fitting a calibration model or accessing protected test observations.  SUCCESS: Each candidate has correct confusion counts, conditional rates and prevalence-weighted expected cost. Empty conditioning groups are identified as undefined rather than assigned a numerical rate. The selected threshold satisfies supplied eligibility limits and minimizes the declared cost among eligible candidates. Its score representation and validation record are retained unchanged for later testing; no eligible candidate produces an explicit no-selection result.
ASSESSMENT ANCHOR: distinguish_scores_from_thresholded_decisions facts=['f1', 'f2']
ASSESSMENT ANCHOR: calculate_threshold_confusion_counts_and_conditional_error_rates facts=['f3', 'f5']
ASSESSMENT ANCHOR: select_minimum_cost_eligible_validation_threshold facts=['f4', 'f6']
ASSESSMENT ANCHOR: freeze_threshold_without_using_protected_test_observations facts=['f4', 'f7']

## SOURCE FACTS — B (mle.validation_candidate_comparison)   objective: Rank eligible candidate records using a common expected-cost and operating-limit rule.
B.f1: Compare candidate predictive metrics with the baseline on the same evaluation dataset and check predeclared requirements rather than selecting from incomparable cohorts.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: Calculate each record’s expected cost under the same supplied deployment class probabilities and error costs, exclude records failing fixed limits, and rank the eligible records by the declared cost rule.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f5: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Threshold and Candidate Selection.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Compare three supplied candidate validation records and baseline A for the same orders cohort. Derive FPR and FNR from each record's supplied confusion counts, flag empty conditioning groups as undefined, and calculate expected error cost using the same supplied deployment class probabilities and fixed error costs. Apply the predeclared quality and operating limits, rank eligible records by the precommitted cost rule, and record one frozen choice without consulting protected test observations.  SUCCESS: The completed comparison retains the cohort identity, confusion counts, rate denominators, fixed probabilities and error costs for every record. Conditional rates and expected costs are correct; undefined rates are not replaced with zero. Eligibility decisions follow the supplied limits, exclusions have explicit reasons, and eligible records are ranked by the declared cost rule. One selected identity is recorded with its supporting quantities and eligibility result, with no protected test information used.
ASSESSMENT ANCHOR: check_matched_cohort_and_fixed_requirement_eligibility facts=['f1', 'f2']
ASSESSMENT ANCHOR: derive_conditional_error_rates_and_identify_undefined_rates facts=['f3']
ASSESSMENT ANCHOR: calculate_expected_error_cost_and_rank_eligible_records facts=['f2', 'f4']
ASSESSMENT ANCHOR: freeze_validation_choice_without_protected_test_information facts=['f5']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.candidate_records: Baseline and three candidate records — columns: candidate_id(identifier), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), latency_requirement_met(categorical), scale_requirement_met(categorical), training_cost_requirement_met(categorical), serving_cost_requirement_met(categorical), maintenance_requirement_met(categorical), deployment_compatibility_met(categorical)
   ["A","orders_100",16,12,4,68,20,80,100,0.5714285714285714,0.8,0.2,0.15,0.2,0.32000000000000006,true,true,true,true,true,true]
   ["B","orders_100",16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true,true,true,true,true,true]
   ["C","other_orders_100",16,0,4,80,20,80,100,1.0,0.8,0.2,0.0,0.2,0.20000000000000004,true,true,true,true,true,true]
   ["D","orders_100",16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,false,true,true,true,true,true]
   variant v.candidates_none_eligible: 4 ops; planted: 
ds.threshold_records: Computed threshold validation evidence — columns: threshold(numerical), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), predictive_requirement_met(categorical)
   [0.5,16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true]
   [0.7,16,5,4,75,20,80,100,0.7619047619047619,0.8,0.2,0.0625,0.2,0.25000000000000006,true]
ds.thresholds: Declared threshold candidates — columns: threshold(numerical), score_representation(categorical), declared_order(numerical)
   [0.5,"probability",0]
   [0.7,"probability",1]
ds.validation_scores: One fixed labeled cohort with unchanged scores — columns: observation_id(identifier), cohort_id(identifier), actual_label(categorical,digits-as-label), score(numerical), reference_output(categorical,digits-as-label)
   ["order_001","orders_100",1,0.8,0]
   ["order_002","orders_100",1,0.8,0]
   ["order_003","orders_100",1,0.8,0]
   ["order_004","orders_100",1,0.8,0]
   ["order_005","orders_100",1,0.8,0]
   ["order_006","orders_100",1,0.8,0]
   ["order_007","orders_100",1,0.8,0]
   ["order_008","orders_100",1,0.8,0]
   variant v.scores_no_positives: 1 ops; planted: 
   variant v.scores_no_negatives: 1 ops; planted: 
   variant v.scores_none_eligible: 100 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction errors for recurring failure modes; 

## LESSON, in learner order

### s01 · explainer · Choose and freeze
(intro) The same scores can yield different class decisions. Make the threshold explicit, evaluate supplied candidates on validation, and freeze the chosen rule. ⟦A:tb1⟧
(mechanism) A score is not a class decision: comparing it with a threshold produces the decision. Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicit task threshold changes the decision. For each supplied threshold, form labels and count TP, FP, TN and FN against validation labels. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Choose the eligible threshold minimizing predeclared validation expected cost, then freeze it before protected testing. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups yield undefined rates. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[TABLE ds.threshold_records cols=['threshold', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'predictive_requirement_met'] ] caption: Computed threshold validation evidence
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Same supplied score, different threshold-dependent decisions.
  produced by sql: SELECT v.observation_id, v.score, t.threshold, v.score >= t.threshold AS predicted_positive FROM scores v CROSS JOIN thresholds t WHERE v.score > (SELECT MIN(threshold) FROM thresholds) AND v.score < (SELECT MAX(threshold) FROM thresholds) ORDER BY v.observation_id, t.declared_order

### s02 · explainer · Protect the test boundary
(mechanism) Using protected-test observations to fit preprocessing, choose a model or tune settings leaks information into the selected system. Keep them outside those choices. ⟦A.f7 A:tb4⟧

### s03 · explainer · Compare threshold records
(example) Compare supplied thresholds against the same scores and labels. A score between two thresholds changes class decision without changing score. Recount errors at each threshold, apply the fixed costs and eligibility limits, then retain the minimum-cost eligible rule. The ordinary probability and decision_function cutoffs belong to different score representations; do not treat them as interchangeable. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧

### s04 · explainer · Do not change the score story
(misconception) A threshold changes the decision, not the score. Choose with fixed validation evidence and freeze it before protected testing; do not tune on protected-test results. ⟦A.f1 A.f4 A.f7 A:tb6⟧

### s05 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s06 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s07 · explainer · Fixed cost and test boundaries
(intro) Start with comparable records and eligibility, not the smallest displayed number. Baseline and candidates must answer the same evaluation question. ⟦B:tb1⟧
(mechanism) Compare baseline and candidates on the same evaluation dataset and predeclared requirements. Compute each cost using identical supplied deployment probabilities and error costs. Exclude records failing fixed limits; rank eligible records by the declared cost rule. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups give undefined rates. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose a model or tune settings without leaking information. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.candidate_records cols=['candidate_id', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met'] ] caption: Baseline and three candidate records
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.latency_requirement_met = TRUE AND r.scale_requirement_met = TRUE AND r.training_cost_requirement_met = TRUE AND r.serving_cost_requirement_met = TRUE AND r.maintenance_requirement_met = TRUE AND r.deployment_compatibility_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.candidate_id AS tie_order 
FROM records r CROSS JOIN contract c  
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT candidate_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.candidate_id, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.candidate_id=b.candidate_id ORDER BY a.tie_order

### s08 · explainer · Inspect cohort identity
(example) Inspect cohort identity before comparing baseline and candidate costs. A lower number from a different cohort is not matched selection evidence. For matching records, retain confusion counts, conditioning totals and the fixed cost contract. Check quality and operating limits before ranking; do not change deployment probabilities after seeing which candidate benefits. Protected-test observations stay outside fitting and selection. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s09 · explainer · Smallest is not necessarily eligible
(misconception) The smallest number need not be the eligible winner. Matched cohorts and fixed requirements are prerequisites, not checks to postpone until after selection. ⟦B.f1 B.f2 B:tb5⟧

### s10 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s11 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.

### s12 · recap · Keep these distinctions
(takeaway) Scores and threshold-dependent decisions differ. Evaluate supplied thresholds on validation and freeze the eligible minimum-cost choice. Compare candidates only on matched cohorts, with fixed cost inputs and requirements. Keep protected-test observations outside fitting and selection. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 B.f1 B.f2 B.f3 B.f4 B.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Inspect prediction failures in predefined groups.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — score versus decision
(misconception) Contrast a fixed score with its threshold-dependent class decision. Recount validation errors for each supplied threshold before freezing a choice. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) A score is not a class decision: comparing it with a threshold produces the decision. Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicit task threshold changes the decision. For each supplied threshold, form labels and count TP, FP, TN and FN against validation labels. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Choose the eligible threshold minimizing predeclared validation expected cost, then freeze it before protected testing. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups yield undefined rates. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Using protected-test observations to fit preprocessing, choose a model or tune settings leaks information into the selected system. Keep them outside those choices. ⟦A.f7 A:tb4⟧
[TABLE ds.threshold_records cols=['threshold', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'predictive_requirement_met'] ] caption: Computed threshold validation evidence
### r02 · Revisit: the practice — score versus decision
(misconception) Contrast a fixed score with its threshold-dependent class decision. Recount validation errors for each supplied threshold before freezing a choice. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) A score is not a class decision: comparing it with a threshold produces the decision. Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicit task threshold changes the decision. For each supplied threshold, form labels and count TP, FP, TN and FN against validation labels. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Choose the eligible threshold minimizing predeclared validation expected cost, then freeze it before protected testing. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups yield undefined rates. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Using protected-test observations to fit preprocessing, choose a model or tune settings leaks information into the selected system. Keep them outside those choices. ⟦A.f7 A:tb4⟧
[TABLE ds.threshold_records cols=['threshold', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'predictive_requirement_met'] ] caption: Computed threshold validation evidence
### r03 · Revisit: the check — compare like with like
(misconception) Contrast the lowest reported cost with the lowest eligible matched cost. A different-cohort record cannot win this comparison. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Compare baseline and candidates on the same evaluation dataset and predeclared requirements. Compute each cost using identical supplied deployment probabilities and error costs. Exclude records failing fixed limits; rank eligible records by the declared cost rule. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups give undefined rates. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose a model or tune settings without leaking information. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.candidate_records cols=['candidate_id', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met'] ] caption: Baseline and three candidate records
### r04 · Revisit: the practice — compare like with like
(misconception) Contrast the lowest reported cost with the lowest eligible matched cost. A different-cohort record cannot win this comparison. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Compare baseline and candidates on the same evaluation dataset and predeclared requirements. Compute each cost using identical supplied deployment probabilities and error costs. Exclude records failing fixed limits; rank eligible records by the declared cost rule. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups give undefined rates. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose a model or tune settings without leaking information. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.candidate_records cols=['candidate_id', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met'] ] caption: Baseline and three candidate records

=========

# EVALUATOR PACKET — Failure groups, slices and mitigation (mle.tile.026_028)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_error_analysis — Inspect prediction errors for recurring failure modes
B = mle.slice_evaluation — Evaluate important data slices for subgroup performance gaps
C = mle.subgroup_risk_mitigation — Choose practical mitigations for documented subgroup-performance risks

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.prediction_error_analysis)   objective: Explain a localized model failure with conditional error and feature-summary evidence.
A.f1: Inspect prediction failures rather than assuming the developer’s own usage represents the user population.   [sources: google_rules_of_ml#Rule #23: You are not a typical end user.]
A.f2: For a predefined failure group, count its errors and divide by its eligible observation count to obtain its conditional error proportion.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f3: Compare the group’s quality evidence with the same-cohort reference to localize an observed failure instead of assuming an overall score describes every segment.   [sources: google_mlops_pipelines#Data and model validation]
A.f4: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f5: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Errors, Slices and Subgroup Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python analysis function, including the required NumPy import, that inspects supplied order-model validation errors. Preserve the predefined long-distance group, compute its error count divided by its eligible observation count, and compute the mean and population standard deviation of supplied per-example losses. Compare the group's conditional error proportion and loss summaries with the supplied same-cohort reference, then report one recurring failure mode supported by the observations.  SUCCESS: The learner-written function returns the eligible count, error count, conditional error proportion, mean loss, and population standard deviation for the predefined group and its same-cohort reference. A descriptive finding identifies a recurring pattern in supplied failures, cites comparable evidence, and avoids claiming an untested cause.
ASSESSMENT ANCHOR: identify_recurring_failure_with_conditional_error_evidence facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: interpret_loss_mean_and_standard_deviation_for_selected_observations facts=['f4', 'f5']

## SOURCE FACTS — B (mle.slice_evaluation)   objective: Compare predefined validation slices without hiding their counts or representativeness limits.
B.f1: Overall model improvement can coexist with inconsistent performance across data segments, so evaluate the specified slices separately.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: For each predefined slice, report its eligible observation count and errors divided by that count, retaining the conditioning population.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f3: A sample can fail to represent its intended population, so observed sample slice differences do not by themselves establish a population-level disparity.   [sources: google_ml_crash_course#fairness — Types of bias]
B.f4: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f5: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Errors, Slices and Subgroup Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write one Python analysis function, including the required NumPy import, to calculate supplied validation metrics for predefined delivery-zone slices. Report eligible counts, conditional error probabilities, and per-slice loss means and standard deviations. Compare matched validation slices and describe one supported sample gap without claiming population-level disparity.  SUCCESS: The function returns each slice's eligible count, errors divided by that count, and the mean and standard deviation of its supplied loss observations. For the illustrative fixture, zone A reports 2/40 = 0.05 and zone B reports 6/20 = 0.30. The comparison retains both denominators, uses the declared standard-deviation divisor, and limits its conclusion to the observed validation slices.
ASSESSMENT ANCHOR: identify_slice_gaps_with_eligible_counts_and_conditional_error_rates facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_observed_slice_gaps_from_population_disparity facts=['f2', 'f3']
ASSESSMENT ANCHOR: calculate_slice_means_and_standard_deviations_with_the_required_divisor facts=['f4', 'f5']

## SOURCE FACTS — C (mle.subgroup_risk_mitigation)   objective: Choose a supported subgroup mitigation using population-weighted harm and validation evidence.
C.f1: Evaluate whether the data represents the groups for which the model is intended before attributing a subgroup problem solely to the model.   [sources: google_ml_crash_course#fairness — Types of bias]
C.f2: Check the supplied mitigation on the affected validation segment as well as the overall validation cohort before accepting it.   [sources: google_mlops_pipelines#Data and model validation]
C.f3: For a subgroup, its contribution to total expected harm is its deployment population probability multiplied by its subgroup-conditional expected harm; use the supplied error costs for that calculation.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
C.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Errors, Slices and Subgroup Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.slice_evaluation. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Using supplied reference and mitigation validation counts for the affected subgroup and overall cohort, calculate FPR and FNR with their respective conditioning denominators. Calculate subgroup prevalence within validation and keep it distinct from the supplied deployment population probability. Use supplied error costs and subgroup actual-class proportions to calculate subgroup-conditional expected harm and its population-weighted contribution. Select one supplied mitigation tied to the documented slice finding, inspect representation evidence, and state a validation check before comparing the mitigation results.  SUCCESS: FPR uses FP/(FP+TN), FNR uses FN/(FN+TP), and empty conditioning groups are marked undefined rather than zero. Validation subgroup prevalence is calculated as subgroup count divided by overall cohort count, without assuming it equals deployment population probability. Subgroup-conditional harm uses the supplied costs and actual-class proportions; its contribution to total expected harm multiplies that harm by the supplied deployment population probability. The selected mitigation addresses the documented risk, and the precommitted check applies supplied acceptance criteria to both the matched affected validation segment and overall cohort, with representation limitations stated.
ASSESSMENT ANCHOR: choose_mitigation_for_documented_subgroup_risk facts=['f1', 'f2']
ASSESSMENT ANCHOR: justify_mitigation_with_population_weighted_error_harm facts=['f3', 'f4']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.aggregate_slice_evidence: Aggregate evidence from the matched slice cohort — columns: system(categorical), cohort_id(identifier), eligible_count(numerical), error_count(numerical), error_probability(numerical)
   ["reference","slices_60",60,12,0.2]
   ["model","slices_60",60,8,0.13333333333333333]
ds.mitigation_records: Matched reference and supplied mitigation harm — columns: system(categorical), scope(categorical), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), deployment_subgroup_probability(numerical), population_weighted_harm_contribution(numerical), representation_limitation(text), deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), validation_subgroup_prevalence(numerical)
   ["reference","affected_subgroup","mitigation_validation",4,15,1,5,5,20,25,0.21052631578947367,0.8,0.2,0.75,0.2,0.8000000000000002,0.25,0.20000000000000004,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
   ["reference","overall","mitigation_validation",32,24,8,136,40,160,200,0.5714285714285714,0.8,0.2,0.15,0.2,0.32000000000000006,0.25,null,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
   ["mitigation","affected_subgroup","mitigation_validation",4,10,1,10,5,20,25,0.2857142857142857,0.8,0.2,0.5,0.2,0.6000000000000001,0.25,0.15000000000000002,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
   ["mitigation","overall","mitigation_validation",32,16,8,144,40,160,200,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,0.25,null,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
ds.slice_observations: Predefined zones and long-distance observations — columns: observation_id(identifier), cohort_id(identifier), zone(categorical), eligible(categorical), long_distance(categorical), error(categorical), loss(numerical), reference_error(categorical), reference_loss(numerical), distance(numerical)
   ["slice_001","slices_60","A",true,true,true,1.0,true,1.0,5.0]
   ["slice_002","slices_60","A",true,true,true,1.0,true,1.0,7.0]
   ["slice_003","slices_60","A",true,true,false,0.0,true,1.0,9.0]
   ["slice_004","slices_60","A",true,true,false,0.0,true,1.0,11.0]
   ["slice_005","slices_60","A",true,true,false,0.0,false,0.0,13.0]
   ["slice_006","slices_60","A",true,true,false,0.0,false,0.0,15.0]
   ["slice_007","slices_60","A",true,true,false,0.0,false,0.0,17.0]
   ["slice_008","slices_60","A",true,true,false,0.0,false,0.0,19.0]
   variant v.empty_zone_B: 1 ops; planted: 
ds.slice_summary: Computed conditional slice summaries — columns: slice(categorical), eligible_count(numerical), error_count(numerical), error_probability(numerical), loss_mean(numerical), loss_std(numerical), ddof(numerical)
   ["A",40,2,0.05,0.05,0.21794494717703367,0]
   ["B",20,6,0.3,0.3,0.45825756949558394,0]
   ["long-distance",20,8,0.4,0.4,0.48989794855663565,0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, bac

## LESSON, in learner order

### s01 · explainer · Summarize selected observations
(intro) Investigate the predefined failure group rather than treating personally tried cases as representative of users. Keep its eligible population explicit. ⟦A:tb1⟧
(mechanism) Inspect prediction failures; developer usage does not necessarily represent users. For the predefined group, divide errors by eligible observations. Compare its quality evidence with the same-cohort reference to localize observed failure; an overall score does not describe every segment. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Summarize selected numeric observations with np.mean(numeric_values). Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only when the specified calculation requires N−1. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.slice_observations cols=['observation_id', 'cohort_id', 'eligible', 'long_distance', 'error', 'loss', 'reference_error', 'reference_loss'] ] caption: Predefined zones and long-distance observations
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries

### s02 · explainer · Inspect long-distance evidence
(example) The supplied observations identify eligibility and long-distance membership alongside model and reference errors and loss. Keep that group boundary when counting errors and eligible observations. Compare with the group’s same-cohort reference, not unrelated traffic. Selected loss mean and spread describe the measured observations; they do not establish a cause of failure or make developer-chosen examples representative of users. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · Counts need denominators
(misconception) An overall score does not describe every segment. An error count without the eligible count hides the conditional proportion. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s05 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s06 · explainer · Mean and spread
(intro) Evaluate predefined delivery zones separately even when the aggregate improves. Keep each slice’s observation count beside its quality result. ⟦B:tb1⟧
(mechanism) Overall improvement can coexist with uneven segment performance. For each predefined slice, report eligible count and errors/eligible count. Retain that conditioning population. Samples may not represent their intended population, so sample slice differences alone do not establish population-level disparity. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use np.mean(numeric_values) for selected observations’ mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the calculation requires N−1. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries
[TABLE ds.aggregate_slice_evidence cols=['system', 'cohort_id', 'eligible_count', 'error_count', 'error_probability'] ] caption: Aggregate evidence from the matched slice cohort

### s07 · explainer · Inspect zone evidence
(example) Read each zone’s eligible count, errors and conditional error probability together. The loss summaries retain their own selected observations and standard-deviation divisor. Compare slice evidence with the matched overall record without letting one replace the other. Unequal observed sample results support a bounded description of these slices, not an unmeasured population conclusion. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s08 · explainer · Uneven does not prove population disparity
(misconception) Aggregate improvement can coexist with uneven slices. An observed sample difference alone does not prove disparity throughout the intended population. ⟦B.f1 B.f3 B:tb5⟧

### s09 · video · Inspect evaluate important data slices for subgroup performance gaps
[VIDEO ] bridge-before:  | bridge-after: 

### s10 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s11 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s12 · explainer · Keep actual-class groups separate
(intro) Before accepting a supplied mitigation, inspect group representation and both subgroup and overall validation evidence. Do not assume the model alone explains the problem. ⟦C:tb1⟧
(mechanism) Check whether data represents intended groups before attributing a subgroup problem solely to the model. Evaluate the supplied mitigation on the affected validation segment and overall cohort. A subgroup’s contribution to total expected harm is its deployment population probability × subgroup-conditional expected harm, using supplied error costs. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group leaves its rate undefined. ⟦C.f4 C:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"ds.mitigation_records","columns":["system","scope","cohort_id","TP","FP","FN","TN","actual_positive_count","actual_negative_count","cohort_count","precision","recall","validation_prevalence","FPR","FNR","expected_error_cost","deployment_subgroup_probability","population_weighted_harm_contribution","representation_limitation","deployment_negative_probability","deployment_positive_probability","cost_FP","cost_FN","validation_subgroup_prevalence"]},"range":"A1:X5","show_formula_bar":true,"lineage":{"concept_ids":["mle.subgroup_risk_mitigation"],"teaching_block_ids":[],"fact_ids":[],"anchors":["mle.subgroup_risk_mitigation#visual"]}}
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract

### s13 · explainer · Inspect segment and overall evidence
(example) Keep subgroup-conditional harm distinct from its population-weighted contribution. The registered records show reference and mitigation evidence for both affected segment and overall cohort. Apply the supplied deployment subgroup probability, not the validation subgroup prevalence, to weight conditional harm. Inspect representation and the overall result before acceptance; a subgroup improvement alone is insufficient. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4⟧

### s14 · explainer · Subgroup-only is insufficient
(misconception) A subgroup-only improvement is insufficient. Population probability, conditional harm and representation are distinct; empty conditioning groups do not supply defined rates. ⟦C.f1 C.f2 C.f4 C:tb5⟧

### s15 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s16 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.

### s17 · recap · Keep these distinctions
(takeaway) Retain eligible denominators in failure groups and predefined slices. Compare with same-cohort references; sample differences alone do not establish population disparity. Check representation, subgroup and overall evidence before accepting a mitigation. Distinguish conditional harm from population-weighted contribution. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 B.f1 B.f2 B.f3 B.f4 B.f5 C.f1 C.f2 C.f3 C.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Up next: Keep resolved experiment settings, validation metrics and artifacts in a keyed run.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — locate observed failures
(misconception) Contrast error count with conditional error proportion. The predefined eligible population supplies the denominator; an overall score does not locate every failure. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Inspect prediction failures; developer usage does not necessarily represent users. For the predefined group, divide errors by eligible observations. Compare its quality evidence with the same-cohort reference to localize observed failure; an overall score does not describe every segment. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Summarize selected numeric observations with np.mean(numeric_values). Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only when the specified calculation requires N−1. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.slice_observations cols=['observation_id', 'cohort_id', 'zone', 'eligible', 'long_distance', 'error', 'loss', 'reference_error', 'reference_loss', 'distance'] ] caption: Predefined zones and long-distance observations
### r02 · Revisit: the practice — locate observed failures
(misconception) Contrast error count with conditional error proportion. The predefined eligible population supplies the denominator; an overall score does not locate every failure. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Inspect prediction failures; developer usage does not necessarily represent users. For the predefined group, divide errors by eligible observations. Compare its quality evidence with the same-cohort reference to localize observed failure; an overall score does not describe every segment. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Summarize selected numeric observations with np.mean(numeric_values). Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only when the specified calculation requires N−1. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.slice_observations cols=['observation_id', 'cohort_id', 'zone', 'eligible', 'long_distance', 'error', 'loss', 'reference_error', 'reference_loss', 'distance'] ] caption: Predefined zones and long-distance observations
### r03 · Revisit: the check — separate the slices
(misconception) Contrast observed slice evidence with a population claim. Counts and sample conditioning support the former, not automatic generalization to the latter. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Overall improvement can coexist with uneven segment performance. For each predefined slice, report eligible count and errors/eligible count. Retain that conditioning population. Samples may not represent their intended population, so sample slice differences alone do not establish population-level disparity. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use np.mean(numeric_values) for selected observations’ mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the calculation requires N−1. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries
### r04 · Revisit: the practice — separate the slices
(misconception) Contrast observed slice evidence with a population claim. Counts and sample conditioning support the former, not automatic generalization to the latter. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Overall improvement can coexist with uneven segment performance. For each predefined slice, report eligible count and errors/eligible count. Retain that conditioning population. Samples may not represent their intended population, so sample slice differences alone do not establish population-level disparity. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use np.mean(numeric_values) for selected observations’ mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the calculation requires N−1. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries
### r05 · Revisit: the check — check representation first
(misconception) Contrast subgroup-conditional harm with population-weighted contribution. Weight by supplied deployment probability, then inspect representation and overall evidence too. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3⟧
(mechanism) Check whether data represents intended groups before attributing a subgroup problem solely to the model. Evaluate the supplied mitigation on the affected validation segment and overall cohort. A subgroup’s contribution to total expected harm is its deployment population probability × subgroup-conditional expected harm, using supplied error costs. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group leaves its rate undefined. ⟦C.f4 C:tb3⟧
[TABLE ds.mitigation_records cols=['system', 'scope', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'deployment_subgroup_probability', 'population_weighted_harm_contribution', 'representation_limitation', 'deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'validation_subgroup_prevalence'] ] caption: Matched reference and supplied mitigation harm
### r06 · Revisit: the practice — check representation first
(misconception) Contrast subgroup-conditional harm with population-weighted contribution. Weight by supplied deployment probability, then inspect representation and overall evidence too. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3⟧
(mechanism) Check whether data represents intended groups before attributing a subgroup problem solely to the model. Evaluate the supplied mitigation on the affected validation segment and overall cohort. A subgroup’s contribution to total expected harm is its deployment population probability × subgroup-conditional expected harm, using supplied error costs. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group leaves its rate undefined. ⟦C.f4 C:tb3⟧
[TABLE ds.mitigation_records cols=['system', 'scope', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'deployment_subgroup_probability', 'population_weighted_harm_contribution', 'representation_limitation', 'deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'validation_subgroup_prevalence'] ] caption: Matched reference and supplied mitigation harm

=========

# EVALUATOR PACKET — Track, repeat and bound experiments (mle.tile.029_032)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.experiment_metric_logging — Record an MLflow experiment run with parameters, validation metrics and diagnostic artifacts
B = mle.training_randomness — Control random seeds for reproducible training comparisons
C = mle.validation_regularization — Select regularization in response to validation-observed overfitting
D = mle.bounded_hyperparameter_search — Run bounded hyperparameter search using validation evidence without accessing the protected test set

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.experiment_metric_logging)   objective: Create and verify a keyed run record linking parameters, metrics, artifacts and actual code revision.
A.f1: Use import mlflow and with mlflow.start_run() as run to create a run whose run_id identifies its tracking record.   [sources: mlflow_docs#ml/tracking/tracking-api/ — Starting and Managing Runs; Logging Data to Runs; Querying Runs Programmatically]
A.f2: Log the resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and a diagnostic file with mlflow.log_artifact(local_path).   [sources: mlflow_docs#ml/tracking/tracking-api/ — Starting and Managing Runs; Logging Data to Runs; Querying Runs Programmatically]
A.f3: Inspect the actual repository revision with git rev-parse --verify HEAD before recording the run’s code identity.   [sources: git_docs#git-rev-parse — --verify; git-show — DESCRIPTION]
A.f4: Retrieve the keyed run with recorded = mlflow.get_run(run_id), then read recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri; for a metric logged repeatedly, this RunData exposes the most recently logged value at the largest step, not its entire history.   [sources: mlflow_docs#https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html — mlflow.get_run, mlflow_docs#https://mlflow.org/docs/latest/api_reference/python_api/mlflow.entities.html — Run.data; Run.info; RunData.params; RunData.metrics; RunInfo.artifact_uri]
A.f5: Define the logging function with default parameter values and accept explicit keyword overrides, then log the resolved values rather than only the defaults.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
A.f6: Use os.getcwd() to inspect the current working directory and os.chdir(recorded_directory) when resolving local artifact/repository paths, retaining the resolved path in the run lookup.   [sources: python_tutorial#stdlib.html — Operating System Interface; Command Line Arguments]
A.f7: Use subprocess.run with the intended working directory and captured output to inspect git rev-parse --verify HEAD and reject a revision mismatch before claiming the keyed artifact belongs to that run.   [sources: python_tutorial#../library/subprocess.html — Using the subprocess Module]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports, a default trial setting of 10 and an explicit keyword override of 20. Inspect the working directory and repository revision, then record one MLflow run containing the resolved parameter dictionary, a supplied validation metric and an existing diagnostic file. Retain the run ID, repository directory, resolved local artifact path and code revision; retrieve the same run and reject a revision mismatch before accepting its artifact association.  SUCCESS: The retrieved run contains the resolved trial setting of 20, the supplied validation result and an artifact URI for the logged diagnostic file. The retained lookup identifies the same run, repository directory, local artifact path and actual code revision. A revision-mismatch check rejects an incorrect revision rather than accepting the association.
ASSESSMENT ANCHOR: retrieve_run_by_run_id facts=['f1', 'f4']
ASSESSMENT ANCHOR: retrieve_resolved_parameters_and_validation_metrics facts=['f2', 'f4', 'f5']
ASSESSMENT ANCHOR: interpret_repeated_metric_run_data facts=['f4']
ASSESSMENT ANCHOR: verify_run_artifact_path_and_code_identity facts=['f2', 'f3', 'f6', 'f7']

## SOURCE FACTS — B (mle.training_randomness)   objective: Assess paired-run variability with numeric summaries and an empirical candidate-win proportion.
B.f1: Integer random_state values reset supported scikit-learn random generators for repeatable calls, while None or a shared RandomState instance has different state-consumption behavior.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.3 Controlling randomness]
B.f2: Control the estimator and split random sources for a comparison, but distinguish that control from a guarantee that every computation or environment is deterministic.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.3 Controlling randomness]
B.f3: Use a for loop over the declared seed list to execute the repeated comparison and collect each matched pair of validation results.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
B.f4: Estimate the candidate’s empirical win probability as winning paired trials divided by all completed paired trials, retaining the number of trials.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f5: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f6: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.sklearn_baseline_workflow, mle.deployment_matched_splits. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required imports and a learner-defined Python function that repeats the supplied baseline/candidate validation comparison over the declared seed list. Control both split and estimator random sources under the supplied protocol, retain each completed pair with its seed, and report the completed-pair count, candidate win count, empirical win probability, and mean and standard deviation of the selected numeric results. Explain why controlled randomness does not establish universal deterministic replay.  SUCCESS: Every declared seed is processed, both models in each completed trial use the same validation split, and each completed record retains its seed and baseline/candidate results. The reported win probability equals winning completed pairs divided by all completed pairs under the supplied metric direction and tie rule. The report includes the denominator, np.mean results, np.std results with ddof=0, and a bounded reproducibility statement.
ASSESSMENT ANCHOR: distinguish_random_state_consumption facts=['f1']
ASSESSMENT ANCHOR: control_split_and_estimator_randomness_without_overclaiming_determinism facts=['f2']
ASSESSMENT ANCHOR: collect_paired_seed_trials_and_estimate_empirical_win_probability facts=['f3', 'f4']
ASSESSMENT ANCHOR: summarize_repeated_results_with_mean_and_specified_standard_deviation facts=['f5', 'f6']

## SOURCE FACTS — C (mle.validation_regularization)   objective: Select a regularization setting from matched train/validation gaps and expected-cost evidence.
C.f1: A gap between good training performance and poor validation performance provides evidence of overfitting; compare both under the same scoring interpretation.   [sources: scikit_learn_user_guide#modules/learning_curve.html — 3.5.1 Validation curve; 3.5.2 Learning curve]
C.f2: Evaluate the declared regularization settings using the same validation protocol, then select with the predeclared validation criterion rather than the training score alone.   [sources: scikit_learn_user_guide#modules/learning_curve.html — 3.5.1 Validation curve; 3.5.2 Learning curve]
C.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
C.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
C.f5: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
C.f6: Regularization penalizes model complexity during fitting; for Ridge settings larger alpha increases the penalty, while LogisticRegression uses C as inverse regularization strength.   [sources: scikit_learn_user_guide#modules/linear_model.html — Ridge regression; Logistic regression]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.deployment_matched_splits, mle.sklearn_baseline_workflow, mle.validation_candidate_comparison. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports that compares the supplied order-model regularization settings within existing infrastructure scaffolding. Keep preprocessing training-fitted and the validation protocol, deployment probabilities, error costs, scoring interpretation, and eligibility limits fixed. Calculate validation FPR, FNR, and expected error cost, compare training and validation performance, and select an eligible setting using the predeclared validation criterion without protected-test access.  SUCCESS: The function returns the declared settings' comparable training and validation results, correctly calculated conditional error rates and expected costs, and the eligible selection required by the validation criterion. Empty conditioning groups are explicitly reported as undefined rather than assigned a fabricated rate. The comparison preserves all fixed assumptions and never accesses protected-test observations.
ASSESSMENT ANCHOR: recognize_overfitting_from_comparable_training_validation_scores facts=['f1']
ASSESSMENT ANCHOR: select_regularization_using_fixed_validation_criterion_without_test_access facts=['f2', 'f5']
ASSESSMENT ANCHOR: calculate_conditional_error_rates_and_identify_undefined_rates facts=['f3']
ASSESSMENT ANCHOR: calculate_deployment_weighted_expected_error_cost facts=['f4']
ASSESSMENT ANCHOR: interpret_estimator_specific_regularization_strength facts=['f6']

## SOURCE FACTS — D (mle.bounded_hyperparameter_search)   objective: Execute a budgeted validation search with resolved defaults and protected-test isolation.
D.f1: GridSearchCV enumerates combinations from param_grid, while RandomizedSearchCV samples a bounded number of configurations selected by n_iter.   [sources: scikit_learn_user_guide#modules/grid_search.html — 3.2.1 Exhaustive Grid Search; 3.2.2 Randomized Parameter Optimization]
D.f2: Specify the scoring and evaluation protocol before running the search, and inspect the validation-selected best_params_ and cv_results_.   [sources: scikit_learn_user_guide#modules/grid_search.html — 3.2.1 Exhaustive Grid Search; 3.2.2 Randomized Parameter Optimization]
D.f3: For a supplied manual search, iterate the bounded configuration dictionaries, execute each declared trial and record its validation result without exceeding the fixed trial budget.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
D.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
D.f5: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
D.f6: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
D.f7: Define the search function with a default budget parameter and accept explicit keyword overrides; resolve the budget before iterating the trial dictionary/list.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.sklearn_baseline_workflow, mle.validation_candidate_comparison, mle.training_randomness, mle.task_metric_selection, mle.deployment_matched_splits, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python search function within the supplied infrastructure scaffolding, including imports for its required library or client dependencies. Accept a default budget and explicit keyword overrides, resolve the budget before iterating the supplied configuration dictionaries, and execute only the permitted trials. Record validation counts, calculate conditional error rates and prevalence-weighted expected error cost, and return the validation-selected configuration under the supplied fixed selection rule without accessing protected test observations.  SUCCESS: The function respects both its default budget and an explicit keyword override. With three supplied configurations and a keyword budget of two, it executes exactly the first two declared trials and retains their actual configurations and validation results. Its rates use the correct conditioning groups, empty groups remain undefined, and its expected costs use the supplied deployment probabilities and error costs. Selection follows the fixed eligibility and selection rules using validation evidence alone.
ASSESSMENT ANCHOR: interpret_validation_selected_search_results facts=['f1', 'f2']
ASSESSMENT ANCHOR: execute_trials_within_resolved_budget facts=['f3', 'f7']
ASSESSMENT ANCHOR: select_configuration_by_validation_expected_error_cost facts=['f4', 'f5']
ASSESSMENT ANCHOR: exclude_protected_test_evidence_from_search facts=['f6']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.execution_contract: Fixed execution and reporting contracts — columns: estimator_random_state(identifier,digits-as-label), default_trial_setting(numerical), override_trial_setting(numerical), default_search_budget(numerical), override_search_budget(numerical), metric_direction(categorical), tie_policy(categorical), split_protocol(categorical), ddof(numerical)
   [0,10,20,3,2,"lower expected cost is better","ties are not paired wins; selection uses declared order","use same split per seed for both models; set split and estimator random_state to the seed",0]
ds.paired_trials: Five completed matched seed trials — columns: seed(identifier,digits-as-label), baseline_result(numerical), candidate_result(numerical)
   [0,0.32,0.31]
   [1,0.33,0.32]
   [2,0.34,0.33]
   [3,0.35,0.36]
   [4,0.36,0.37]
   variant v.incomplete_pair: 1 ops; planted: 
ds.regularization_directions: Estimator-specific penalty directions — columns: estimator(categorical), parameter(categorical), direction(text)
   ["Ridge","alpha","larger alpha increases penalty"]
   ["LogisticRegression","C","larger C decreases regularization strength"]
ds.regularization_records: Fixed-criterion regularization evidence — columns: configuration_id(identifier), estimator(categorical), parameter_name(categorical), parameter_value(numerical), strength_direction(text), cohort_id(identifier), training_TP(numerical), training_FP(numerical), training_FN(numerical), training_TN(numerical), training_expected_error_cost(numerical), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), operating_requirements_met(categorical)
   ["weak_penalty","LogisticRegression","C",10.0,"inverse regularization strength","orders_100",18,0,2,80,0.10000000000000002,16,15,4,65,20,80,100,0.5161290322580645,0.8,0.2,0.1875,0.2,0.3500000000000001,true]
   ["stronger_penalty","LogisticRegression","C",1.0,"inverse regularization strength","orders_100",17,3,3,77,0.18,16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true]
   variant v.regularization_empty_positive: 13 ops; planted: 
ds.search_trials: Three declared configuration dictionaries — columns: configuration_id(identifier), declared_order(numerical), configuration_json(text), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), operating_requirements_met(categorical)
   ["config_1",0,"{\"C\": 10.0, \"random_state\": 0}","orders_100",16,15,4,65,true]
   ["config_2",1,"{\"C\": 1.0, \"random_state\": 0}","orders_100",16,8,4,72,true]
   ["config_3",2,"{\"C\": 0.1, \"random_state\": 0}","orders_100",16,0,4,80,true]
   variant v.search_empty_positive: 4 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensor

## LESSON, in learner order

### s01 · explainer · Start and log the run
(intro) A keyed run connects resolved parameters, validation results, code identity and a diagnostic artifact. A printed metric alone does not retain that connection. ⟦A:tb1⟧
(mechanism) Use import mlflow and with mlflow.start_run() as run; retain run_id as the tracking key. Log resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and the diagnostic file with mlflow.log_artifact(local_path). Inspect git rev-parse --verify HEAD before recording code identity. ⟦A.f1 A.f2 A.f3 A:tb2⟧
[CODE python]
import os
import subprocess
import mlflow

def record_trial(recorded_directory, local_path, expected_revision,
                 metric_name, metric_value, trial_setting=10):
    original_directory = os.getcwd()
    os.chdir(recorded_directory)
    revision = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=recorded_directory, capture_output=True, text=True, check=True
    ).stdout.strip()
    if revision != expected_revision:
        raise ValueError("Repository revision mismatch")
    resolved_path = os.path.abspath(local_path)
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        mlflow.log_params({"trial_setting": trial_setting,
                           "repository_revision": revision,
                           "diagnostic_path": resolved_path})
        mlflow.log_metric(metric_name, metric_value)
        mlflow.log_artifact(resolved_path)
    recorded = mlflow.get_run(run_id)
    os.chdir(original_directory)
    return {"run_id": run_id, "params": recorded.data.params,
            "metrics": recorded.data.metrics,
            "artifact_uri": recorded.info.artifact_uri,
            "resolved_path": resolved_path}
  annotations: []
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts

### s02 · explainer · Reject revision mismatch
(mechanism) Retrieve recorded = mlflow.get_run(run_id); inspect recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. For repeated metric logging, RunData gives the most recently logged value at the largest step, not the full history. Define function defaults, accept keyword overrides, and log resolved values. Use os.getcwd() and os.chdir(recorded_directory) when resolving repository/artifact paths; retain the resolved path in lookup. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Use subprocess.run in the intended working directory with captured output to inspect git rev-parse --verify HEAD. Reject a revision mismatch before claiming the keyed artifact belongs to that run. ⟦A.f7 A:tb4⟧

### s03 · explainer · A name is not a verified key
(example) An explicit keyword override replaces the default value in the resolved configuration to log. Retain the run key and resolved local artifact path, inspect repository identity in the intended directory, then retrieve the keyed run. Compare its parameters, metrics and artifact URI with the intended record. Interpret repeated metrics as the latest value at the largest step, not a history. A revision mismatch or wrongly resolved path prevents the artifact-ownership claim. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧
(misconception) A run name or printed metric is not a verified keyed record. Retrieved parameters, actual revision, resolved overrides and artifact path must agree. ⟦A.f2 A.f3 A.f5 A.f6 A.f7 A:tb6⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s05 · hands_on · Review the logging excerpts
 — Read the supplied excerpts in this step and decide which correctly preserve the resolved configuration and keyed tracking evidence.

### s06 · explainer · Wins, mean and spread
(intro) Control supplied random sources and retain paired trial results. This supports the declared repeated comparison, not universal determinism. ⟦B:tb1⟧
(mechanism) Integer random_state values reset supported scikit-learn generators for repeatable calls; None and shared RandomState instances consume state differently. Control estimator and split randomness without promising every computation or environment is deterministic. Loop over the declared seeds and collect each matched baseline/candidate validation pair. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Empirical win probability is winning paired trials/all completed paired trials; retain the trial count. Summarize selected numeric results with np.mean(numeric_values) and np.std(numeric_values, ddof=0). The latter divides squared deviations by N before the square root; use ddof=1 only if N−1 is required. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.paired_trials cols=['seed', 'baseline_result', 'candidate_result'] ] caption: Five completed matched seed trials
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
[TABLE computed result ] caption: Completed matched pairs; ties are not wins.
  produced by sql: SELECT seed, baseline_result, candidate_result, candidate_result < baseline_result AS candidate_win FROM pairs ORDER BY seed
[TABLE computed result ] caption: Selected-result means and N-divisor standard deviations.
  produced by sql: SELECT COUNT(*) AS completed_pairs, SUM(CASE WHEN candidate_result < baseline_result THEN 1 ELSE 0 END) AS wins, 1.0*SUM(CASE WHEN candidate_result < baseline_result THEN 1 ELSE 0 END)/COUNT(*) AS empirical_win_probability, AVG(baseline_result) AS baseline_mean, SQRT(AVG(baseline_result*baseline_result)-AVG(baseline_result)*AVG(baseline_result)) AS baseline_std_ddof0, AVG(candidate_result) AS candidate_mean, SQRT(AVG(candidate_result*candidate_result)-AVG(candidate_result)*AVG(candidate_result)) AS candidate_std_ddof0 FROM pairs

### s07 · explainer · Retain each completed pair
(example) Keep each seed with its baseline and candidate results, then judge wins using the declared metric direction and tie policy. Separate averages lose pairing, so calculate wins pair by pair and retain the completed-pair denominator. An incomplete trial is not a win. Mean and spread describe the selected results under the specified divisor. Controlling estimator and split sources does not establish determinism in every environment. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb4⟧

### s08 · explainer · Seeds do not promise certainty
(misconception) Controlled seeds do not guarantee universal determinism. Empirical wins describe completed paired trials, not certainty that the candidate always wins. ⟦B.f2 B.f4 B:tb5⟧

### s09 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s10 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s11 · explainer · Select by validation
(intro) Good training results with worse validation results under the same score interpretation provide overfitting evidence. Investigate declared regularization settings under the fixed validation protocol. ⟦C:tb1⟧
(mechanism) A good-training/poor-validation gap is evidence of overfitting. Compare declared settings under the same scoring interpretation and select by the predeclared validation criterion, not training score alone. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f1 C.f2 C.f3 C:tb2⟧
[SIDE_BY_SIDE] Select by the fixed validation criterion, not training cost alone. left_label: Matched training and validation costs | right_label: Estimator-specific strength directions
  left:
[TABLE ds.regularization_records cols=['configuration_id', 'estimator', 'parameter_name', 'parameter_value', 'strength_direction', 'training_expected_error_cost', 'expected_error_cost', 'operating_requirements_met'] ] caption: Fixed-criterion regularization evidence
  right:
[TABLE ds.regularization_directions cols=['estimator', 'parameter', 'direction'] ] caption: Estimator-specific penalty directions
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.operating_requirements_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.configuration_id AS tie_order 
FROM records r CROSS JOIN contract c  
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT configuration_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.configuration_id, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.configuration_id=b.configuration_id ORDER BY a.tie_order

### s12 · explainer · Estimator-specific strength
(mechanism) Protected-test observations must not fit preprocessing, choose models or tune settings: that leaks information. Regularization penalizes complexity during fitting. Larger Ridge alpha increases the penalty; LogisticRegression C is inverse regularization strength, so larger C weakens regularization. ⟦C.f4 C.f5 C.f6 C:tb3⟧

### s13 · explainer · Inspect setting evidence
(example) Read training and validation cost under the same interpretation. A setting with worse training cost can still be the eligible minimum-validation-cost choice. Retain matched cohort, supplied probabilities and error costs. Identify the estimator before interpreting parameter direction: Ridge alpha and LogisticRegression C run in opposite strength directions. The gap supports investigation, not a claim that every validation weakness has the same cause. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb4⟧

### s14 · video · Inspect select regularization in response to validation-observed overfitting
[VIDEO ] bridge-before:  | bridge-after: 

### s15 · explainer · Training alone cannot choose
(misconception) Best training cost need not mean best validation choice. Parameter direction is estimator-specific: larger LogisticRegression C weakens regularization. ⟦C.f2 C.f6 C:tb5⟧

### s16 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s17 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s18 · explainer · Keep costs and boundaries fixed
(intro) Resolve a trial budget and scoring protocol before search. Candidate settings alone do not define a stopping boundary. ⟦D:tb1⟧
(mechanism) GridSearchCV enumerates param_grid combinations; RandomizedSearchCV samples configurations bounded by n_iter. Predeclare scoring and evaluation protocol, then inspect validation-selected best_params_ and cv_results_. In a supplied manual search, iterate bounded configuration dictionaries, execute declared trials and record validation results without exceeding the fixed budget. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦D.f4 D.f5 D.f6 D:tb3⟧
[TABLE computed result ] caption: Budget boundary: supplied configurations are not all completed trials.
  produced by sql: SELECT r.configuration_id, r.configuration_json, e.override_search_budget AS resolved_budget, r.declared_order < e.override_search_budget AS executed FROM records r CROSS JOIN execution e ORDER BY r.declared_order
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.operating_requirements_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.declared_order AS tie_order , e.override_search_budget AS resolved_budget
FROM records r CROSS JOIN contract c  CROSS JOIN execution e  WHERE r.declared_order < e.override_search_budget
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT configuration_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.configuration_id, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.configuration_id=b.configuration_id ORDER BY a.tie_order

### s19 · explainer · Resolve keyword overrides
(mechanism) Define a default budget parameter and accept explicit keyword overrides. Resolve the budget before iterating the configuration dictionary/list. ⟦D.f7 D:tb4⟧

### s20 · explainer · Inspect completed trials
(example) The execution contract distinguishes default and overridden budgets. Resolve the override before trials, then retain only completed configurations and their validation results. A supplied third response is not a completed trial when the budget stops earlier. Keep scoring, actual-class denominators, deployment probabilities and costs fixed. Inspect selected parameters and trial results under the declared protocol; protected-test results are not search evidence. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb5⟧

### s21 · explainer · An override replaces the default
(misconception) An overridden budget, not the default, governs execution. Validation-selected settings do not authorize protected-test inspection or continued searching to improve that result. ⟦D.f2 D.f6 D.f7 D:tb6⟧

### s22 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s23 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s24 · recap · Keep these distinctions
(takeaway) Verify keyed runs with resolved overrides, repository revision and artifact paths. Control random sources without claiming universal determinism; retain completed paired trials. Select regularization by validation, with estimator-specific parameter direction. Resolve search budgets before trials and keep protected-test observations outside selection. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5 D:tb1 D:tb2 D:tb3 D:tb4 D:tb5 D:tb6⟧
[UP NEXT] Up next: Document supported limitations under the existing risk policy.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — keep a keyed record
(misconception) Contrast a default with the resolved keyword override. Log the value actually used, then verify keyed parameters, revision and resolved artifact path. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) Use import mlflow and with mlflow.start_run() as run; retain run_id as the tracking key. Log resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and the diagnostic file with mlflow.log_artifact(local_path). Inspect git rev-parse --verify HEAD before recording code identity. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Retrieve recorded = mlflow.get_run(run_id); inspect recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. For repeated metric logging, RunData gives the most recently logged value at the largest step, not the full history. Define function defaults, accept keyword overrides, and log resolved values. Use os.getcwd() and os.chdir(recorded_directory) when resolving repository/artifact paths; retain the resolved path in lookup. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Use subprocess.run in the intended working directory with captured output to inspect git rev-parse --verify HEAD. Reject a revision mismatch before claiming the keyed artifact belongs to that run. ⟦A.f7 A:tb4⟧
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
### r02 · Revisit: the practice — keep a keyed record
(misconception) Contrast a default with the resolved keyword override. Log the value actually used, then verify keyed parameters, revision and resolved artifact path. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) Use import mlflow and with mlflow.start_run() as run; retain run_id as the tracking key. Log resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and the diagnostic file with mlflow.log_artifact(local_path). Inspect git rev-parse --verify HEAD before recording code identity. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Retrieve recorded = mlflow.get_run(run_id); inspect recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. For repeated metric logging, RunData gives the most recently logged value at the largest step, not the full history. Define function defaults, accept keyword overrides, and log resolved values. Use os.getcwd() and os.chdir(recorded_directory) when resolving repository/artifact paths; retain the resolved path in lookup. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Use subprocess.run in the intended working directory with captured output to inspect git rev-parse --verify HEAD. Reject a revision mismatch before claiming the keyed artifact belongs to that run. ⟦A.f7 A:tb4⟧
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
### r03 · Revisit: the check — control and pair trials
(misconception) Contrast repeatable supported seeded calls with universal determinism. Empirical wins are measured among completed matched pairs, not guaranteed future wins. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3⟧
(mechanism) Integer random_state values reset supported scikit-learn generators for repeatable calls; None and shared RandomState instances consume state differently. Control estimator and split randomness without promising every computation or environment is deterministic. Loop over the declared seeds and collect each matched baseline/candidate validation pair. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Empirical win probability is winning paired trials/all completed paired trials; retain the trial count. Summarize selected numeric results with np.mean(numeric_values) and np.std(numeric_values, ddof=0). The latter divides squared deviations by N before the square root; use ddof=1 only if N−1 is required. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.paired_trials cols=['seed', 'baseline_result', 'candidate_result'] ] caption: Five completed matched seed trials
### r04 · Revisit: the practice — control and pair trials
(misconception) Contrast repeatable supported seeded calls with universal determinism. Empirical wins are measured among completed matched pairs, not guaranteed future wins. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3⟧
(mechanism) Integer random_state values reset supported scikit-learn generators for repeatable calls; None and shared RandomState instances consume state differently. Control estimator and split randomness without promising every computation or environment is deterministic. Loop over the declared seeds and collect each matched baseline/candidate validation pair. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Empirical win probability is winning paired trials/all completed paired trials; retain the trial count. Summarize selected numeric results with np.mean(numeric_values) and np.std(numeric_values, ddof=0). The latter divides squared deviations by N before the square root; use ddof=1 only if N−1 is required. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.paired_trials cols=['seed', 'baseline_result', 'candidate_result'] ] caption: Five completed matched seed trials
### r05 · Revisit: the check — investigate the train–validation gap
(misconception) Contrast training quality with validation selection. Larger Ridge alpha strengthens its penalty; larger LogisticRegression C weakens regularization. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3⟧
(mechanism) A good-training/poor-validation gap is evidence of overfitting. Compare declared settings under the same scoring interpretation and select by the predeclared validation criterion, not training score alone. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Protected-test observations must not fit preprocessing, choose models or tune settings: that leaks information. Regularization penalizes complexity during fitting. Larger Ridge alpha increases the penalty; LogisticRegression C is inverse regularization strength, so larger C weakens regularization. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[TABLE ds.regularization_records cols=['configuration_id', 'estimator', 'parameter_name', 'parameter_value', 'strength_direction', 'cohort_id', 'training_TP', 'training_FP', 'training_FN', 'training_TN', 'training_expected_error_cost', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'operating_requirements_met'] ] caption: Fixed-criterion regularization evidence
### r06 · Revisit: the practice — investigate the train–validation gap
(misconception) Contrast training quality with validation selection. Larger Ridge alpha strengthens its penalty; larger LogisticRegression C weakens regularization. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3⟧
(mechanism) A good-training/poor-validation gap is evidence of overfitting. Compare declared settings under the same scoring interpretation and select by the predeclared validation criterion, not training score alone. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Protected-test observations must not fit preprocessing, choose models or tune settings: that leaks information. Regularization penalizes complexity during fitting. Larger Ridge alpha increases the penalty; LogisticRegression C is inverse regularization strength, so larger C weakens regularization. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[TABLE ds.regularization_records cols=['configuration_id', 'estimator', 'parameter_name', 'parameter_value', 'strength_direction', 'cohort_id', 'training_TP', 'training_FP', 'training_FN', 'training_TN', 'training_expected_error_cost', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'operating_requirements_met'] ] caption: Fixed-criterion regularization evidence
### r07 · Revisit: the check — resolve the stopping boundary
(misconception) Contrast default budget with resolved overridden budget. Only executed trials belong in the completed-result record. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb2 D:tb3 D:tb4⟧
(mechanism) GridSearchCV enumerates param_grid combinations; RandomizedSearchCV samples configurations bounded by n_iter. Predeclare scoring and evaluation protocol, then inspect validation-selected best_params_ and cv_results_. In a supplied manual search, iterate bounded configuration dictionaries, execute declared trials and record validation results without exceeding the fixed budget. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦D.f4 D.f5 D.f6 D:tb3⟧
(mechanism) Define a default budget parameter and accept explicit keyword overrides. Resolve the budget before iterating the configuration dictionary/list. ⟦D.f7 D:tb4⟧
[TABLE ds.search_trials cols=['configuration_id', 'declared_order', 'configuration_json', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'operating_requirements_met'] ] caption: Three declared configuration dictionaries
### r08 · Revisit: the practice — resolve the stopping boundary
(misconception) Contrast default budget with resolved overridden budget. Only executed trials belong in the completed-result record. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb2 D:tb3 D:tb4⟧
(mechanism) GridSearchCV enumerates param_grid combinations; RandomizedSearchCV samples configurations bounded by n_iter. Predeclare scoring and evaluation protocol, then inspect validation-selected best_params_ and cv_results_. In a supplied manual search, iterate bounded configuration dictionaries, execute declared trials and record validation results without exceeding the fixed budget. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦D.f4 D.f5 D.f6 D:tb3⟧
(mechanism) Define a default budget parameter and accept explicit keyword overrides. Resolve the budget before iterating the configuration dictionary/list. ⟦D.f7 D:tb4⟧
[TABLE ds.search_trials cols=['configuration_id', 'declared_order', 'configuration_json', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'operating_requirements_met'] ] caption: Three declared configuration dictionaries

=========

# EVALUATOR PACKET — Document model risks (mle.tile.033_033)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.model_risk_documentation — Document model limitations and foreseeable misuse under an existing risk policy

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.model_risk_documentation)   objective: Write a model risk record that preserves the existing access policy and supported limitations.
A.f1: Compare supplied access grants against the existing policy’s permitted identity scope, recording any grant outside that scope rather than defining a new authorization policy.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
A.f2: Literal credentials in an image or its metadata are an exposure risk, so a risk record should describe the handling limitation without copying the secret value.   [sources: docker_docs#https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/ — Description]
A.f3: Model performance can differ by segment even when the aggregate result improves; state the supported limitations of the supplied evaluation rather than implying universal suitability.   [sources: google_mlops_pipelines#Data and model validation]
A.f4: Build the single record from the existing policy fields, preserving the supplied permitted identities, documented task limits and foreseeable misuse cases without extending the permission scope.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Document Model Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (external_proof): Write one risk record using the supplied existing policy fields, task evidence, evaluation evidence, sample access grants and credential-handling record. Preserve the permitted identity scope, document grants outside that scope, include task limits and foreseeable misuse, and describe credential/data exposure limitations without reproducing secret values.  SUCCESS: The single record preserves the supplied policy fields and permitted identities without expanding permissions; identifies any out-of-scope grant; documents credential/data exposure by location or handling limitation without copying secrets; retains documented task limits and foreseeable misuse cases; and cites supported segment limitations without treating aggregate improvement as evidence of universal suitability.
ASSESSMENT ANCHOR: audit_access_grants_against_permitted_identity_scope facts=['f1']
ASSESSMENT ANCHOR: document_credential_exposure_without_disclosing_secrets facts=['f2']
ASSESSMENT ANCHOR: state_evidence_supported_segment_limitations facts=['f3']
ASSESSMENT ANCHOR: document_task_limits_and_foreseeable_misuse_under_existing_policy facts=['f4']

## DATA ASSETS USED
ds.access_grants: Permitted identity versus observed grants — columns: identity(categorical), policy_permitted(categorical), observed_grant(categorical)
   ["A",true,true]
   ["B",false,true]
ds.aggregate_slice_evidence: Aggregate evidence from the matched slice cohort — columns: system(categorical), cohort_id(identifier), eligible_count(numerical), error_count(numerical), error_probability(numerical)
   ["reference","slices_60",60,12,0.2]
   ["model","slices_60",60,8,0.13333333333333333]
ds.risk_policy_evidence: Existing policy and redacted risk evidence — columns: field(identifier), existing_policy(text), supplied_observation(text), recording_constraint(text)
   ["permitted_identities","A","A and B","B is outside the existing permitted identity scope"]
   ["credential_handling","do not reproduce secret values","sample_image.credential_field [REDACTED]","record the location and exposure-handling limitation only"]
   ["permitted_use","evaluate supplied order-task validation evidence","task-specific validation fixture","no universal suitability claim"]
   ["task_limits","supplied order task and validation cohort only","no evidence outside the supplied cohort","retain the task/cohort boundary"]
   ["foreseeable_misuse","aggregate improvement used as universal segment suitability","zone A and B have different observed sample errors","retain segment limitations; no population disparity established"]
   ["segment_evidence","retain supported sample limitations","zone B has higher observed eligible error proportion than zone A","sample-only evidence; representation beyond supplied sample is unresolved"]
ds.slice_summary: Computed conditional slice summaries — columns: slice(categorical), eligible_count(numerical), error_count(numerical), error_probability(numerical), loss_mean(numerical), loss_std(numerical), ddof(numerical)
   ["A",40,2,0.05,0.05,0.21794494717703367,0]
   ["B",20,6,0.3,0.3,0.45825756949558394,0]
   ["long-distance",20,8,0.4,0.4,0.48989794855663565,0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensors on the correct compute device; Profile tra

## LESSON, in learner order

### s01 · explainer · Preserve existing scope
(intro) Build one bounded risk record from existing policy and supplied evidence. Documentation must not expand permissions or reproduce exposed secrets. ⟦A:tb1⟧
(definition) Compare observed grants with existing permitted identities and record out-of-scope grants rather than defining a new policy. Literal credentials in images or metadata are exposure risks: describe the handling limitation without copying the secret. Aggregate improvement can coexist with segment differences; state supported evaluation limitations, not universal suitability. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Preserve existing policy fields, permitted identities, documented task limits and foreseeable misuse cases in the single record. Do not extend permission scope. ⟦A.f4 A:tb3⟧
[TABLE ds.risk_policy_evidence cols=['field', 'existing_policy', 'supplied_observation', 'recording_constraint'] ] caption: Existing policy and redacted risk evidence
[TABLE ds.access_grants cols=['identity', 'policy_permitted', 'observed_grant'] ] caption: Permitted identity versus observed grants
[TABLE ds.aggregate_slice_evidence cols=['system', 'cohort_id', 'eligible_count', 'error_count', 'error_probability'] ] caption: Aggregate evidence from the matched slice cohort
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries

### s02 · explainer · Map evidence into the record
(example) Place existing policy beside supplied observations. An observed identity outside the permitted set is a mismatch to record, not a reason to enlarge that set. Describe the redacted credential-exposure location without copying a value. Carry documented task limits, foreseeable misuse and supported aggregate/segment evidence into one record. Keep permission language separate from measured limitations. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · Documentation is not permission
(misconception) Documentation is not authorization. Do not enlarge identity scope, claim universal suitability or disclose the credential being flagged. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s05 · hands_on · Write one bounded risk record
 — Use the supplied policy and evaluation evidence to record mismatches and limitations without changing permissions or copying secrets.

### s06 · recap · Keep these distinctions
(takeaway) Preserve existing permitted identities, task limits and foreseeable misuse in one risk record. Record access mismatches without widening policy. Describe credential exposure without copying secrets. State supported aggregate and segment limitations rather than universal suitability. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Evaluate supplied foundation-model outputs against matched validation evidence.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — one bounded risk record
(misconception) Contrast an observed grant with a permitted identity. Record a mismatch without expanding policy or copying an exposed secret. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3⟧
(definition) Compare observed grants with existing permitted identities and record out-of-scope grants rather than defining a new policy. Literal credentials in images or metadata are exposure risks: describe the handling limitation without copying the secret. Aggregate improvement can coexist with segment differences; state supported evaluation limitations, not universal suitability. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Preserve existing policy fields, permitted identities, documented task limits and foreseeable misuse cases in the single record. Do not extend permission scope. ⟦A.f4 A:tb3⟧
[TABLE ds.risk_policy_evidence cols=['field', 'existing_policy', 'supplied_observation', 'recording_constraint'] ] caption: Existing policy and redacted risk evidence
### r02 · Revisit: the practice — one bounded risk record
(misconception) Contrast an observed grant with a permitted identity. Record a mismatch without expanding policy or copying an exposed secret. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3⟧
(definition) Compare observed grants with existing permitted identities and record out-of-scope grants rather than defining a new policy. Literal credentials in images or metadata are exposure risks: describe the handling limitation without copying the secret. Aggregate improvement can coexist with segment differences; state supported evaluation limitations, not universal suitability. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Preserve existing policy fields, permitted identities, documented task limits and foreseeable misuse cases in the single record. Do not extend permission scope. ⟦A.f4 A:tb3⟧
[TABLE ds.risk_policy_evidence cols=['field', 'existing_policy', 'supplied_observation', 'recording_constraint'] ] caption: Existing policy and redacted risk evidence

=========

# EVALUATOR PACKET — Evaluate supplied foundation-model outputs (mle.tile.034_034)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.foundation_model_baseline_evaluation — Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (mle.foundation_model_baseline_evaluation)   objective: Compare supplied pretrained task outputs with the fixed baseline under declared acceptance rules.
A.f1: Evaluate supplied foundation-model task outputs against the same task-specific labeled validation examples and acceptance requirements used for the reference.   [sources: sagemaker_developer_guide#how-it-works-mlconcepts.html — The machine learning workflow]
A.f2: Compare the supplied output quality with the validation baseline and report observed limitations without treating supplied-output evaluation as construction or training of the application.   [sources: google_mlops_pipelines#Data and model validation]
A.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f5: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Evaluate Supplied Foundation-Model Outputs.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function, including learner-written imports for required dependencies, that evaluates one supplied foundation-model output set for the order task within existing infrastructure scaffolding. Verify alignment with the fixed labeled validation cohort, score the supplied outputs and reference baseline under the same declared criteria, calculate foundation-output FPR, FNR and expected error cost using supplied deployment class probabilities and error costs, and return one evidence-backed task-quality verdict with observed limitations. Accept only foundation-model outputs as the evaluated candidate; do not fit models, change settings or rank approaches.  SUCCESS: The function verifies matched observations, reports comparable validation metrics for the supplied outputs and baseline, uses actual-negative and actual-positive denominators correctly, and calculates expected error cost under the supplied zero-correct-prediction-cost assumption. It marks rates with empty conditioning groups as undefined rather than zero and does not claim acceptance when required evidence is undefined. Its single verdict follows the fixed acceptance requirements, includes cohort-bounded limitations, and uses no protected-test observations.
ASSESSMENT ANCHOR: verify_matched_validation_cohort_and_acceptance_requirements facts=['f1']
ASSESSMENT ANCHOR: issue_bounded_quality_verdict_against_validation_baseline facts=['f2']
ASSESSMENT ANCHOR: calculate_class_conditional_error_rates_with_empty_group_handling facts=['f3']
ASSESSMENT ANCHOR: calculate_expected_error_cost_from_supplied_deployment_assumptions facts=['f4']
ASSESSMENT ANCHOR: preserve_protected_test_boundary_during_supplied_output_evaluation facts=['f5']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.foundation_outputs: Supplied foundation output file aligned to validation — columns: observation_id(identifier), cohort_id(identifier), output_kind(categorical), foundation_output(categorical,digits-as-label)
   ["order_001","orders_100","foundation-model",1]
   ["order_002","orders_100","foundation-model",1]
   ["order_003","orders_100","foundation-model",1]
   ["order_004","orders_100","foundation-model",1]
   ["order_005","orders_100","foundation-model",1]
   ["order_006","orders_100","foundation-model",1]
   ["order_007","orders_100","foundation-model",1]
   ["order_008","orders_100","foundation-model",1]
   variant v.foundation_wrong_cohort: 1 ops; planted: 
   variant v.foundation_missing_observation: 1 ops; planted: 
   variant v.foundation_duplicate: 1 ops; planted: issue.duplicate_foundation(duplicate_row)
ds.validation_scores: One fixed labeled cohort with unchanged scores — columns: observation_id(identifier), cohort_id(identifier), actual_label(categorical,digits-as-label), score(numerical), reference_output(categorical,digits-as-label)
   ["order_001","orders_100",1,0.8,0]
   ["order_002","orders_100",1,0.8,0]
   ["order_003","orders_100",1,0.8,0]
   ["order_004","orders_100",1,0.8,0]
   ["order_005","orders_100",1,0.8,0]
   ["order_006","orders_100",1,0.8,0]
   ["order_007","orders_100",1,0.8,0]
   ["order_008","orders_100",1,0.8,0]
   variant v.scores_no_positives: 1 ops; planted: 
   variant v.scores_no_negatives: 1 ops; planted: 
   variant v.scores_none_eligible: 100 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensors on the correct compute device; Profile training compute and data-loading

## LESSON, in learner order

### s01 · explainer · Cost and protected boundaries
(intro) Evaluate supplied foundation-model outputs for the order task. The bounded target is matched validation evidence, not application construction or model training. ⟦A:tb1⟧
(mechanism) Use the same task-specific labeled validation examples and acceptance requirements as the reference. Compare supplied-output quality with the validation baseline and report observed limitations; this is not application construction or training. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦A.f4 A.f5 A:tb3⟧
[TABLE computed result ] caption: Aligned validation labels, supplied foundation outputs and reference outputs.
  produced by sql: SELECT v.observation_id, v.cohort_id, v.actual_label, f.foundation_output, v.reference_output FROM labels v LEFT JOIN outputs f ON v.observation_id=f.observation_id AND v.cohort_id=f.cohort_id ORDER BY v.observation_id
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Foundation-output counts, conditioning denominators and fixed-contract cost evidence.
  produced by sql: WITH counts AS (
SELECT SUM(CASE WHEN v.actual_label=0 AND f.foundation_output=1 THEN 1 ELSE 0 END) AS FP,
SUM(CASE WHEN v.actual_label=0 AND f.foundation_output=0 THEN 1 ELSE 0 END) AS TN,
SUM(CASE WHEN v.actual_label=1 AND f.foundation_output=0 THEN 1 ELSE 0 END) AS FN,
SUM(CASE WHEN v.actual_label=1 AND f.foundation_output=1 THEN 1 ELSE 0 END) AS TP
FROM labels v JOIN outputs f ON v.observation_id=f.observation_id AND v.cohort_id=f.cohort_id
), rates AS (SELECT *, 1.0*FP/NULLIF(FP+TN,0) AS FPR, 1.0*FN/NULLIF(FN+TP,0) AS FNR FROM counts), costs AS (
SELECT r.*, FP+TN AS actual_negative_denominator, FN+TP AS actual_positive_denominator,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, c.deployment_negative_probability*r.FPR*c.cost_FP + c.deployment_positive_probability*r.FNR*c.cost_FN AS expected_cost
FROM rates r CROSS JOIN contract c)
SELECT *, expected_cost <= expected_cost_bound AS predictive_requirement_met FROM costs

### s02 · explainer · Check alignment before scoring
(example) Align each supplied output to its labeled validation observation and reference output. A different cohort would not support a matched comparison. Use fixed acceptance requirements, deployment probabilities and error costs, retaining actual-class denominators. Report what these supplied task outputs support and their observed limitations; do not generalize to every foundation model or application. Keep protected-test observations outside fitting and setting choice. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · Evaluation is not construction
(misconception) Supplied-output evaluation does not demonstrate application-building or model-training competence. Its conclusion stays task-specific and validation-based. ⟦A.f1 A.f2 A.f5 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.

### s05 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.

### s06 · recap · Keep these distinctions
(takeaway) Align supplied outputs, labeled validation observations and reference outputs. Apply the same fixed acceptance and cost requirements. Mark empty-group rates undefined and report cohort-bounded limitations. Supplied-output evaluation is not application construction or training; protected-test observations stay outside fitting and selection. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Construct PyTorch input tensors with compatible shapes and dtypes.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — evaluate supplied outputs
(misconception) Contrast matched supplied-output evaluation with application construction. The verdict is bounded to aligned labeled validation observations and fixed requirements. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Use the same task-specific labeled validation examples and acceptance requirements as the reference. Compare supplied-output quality with the validation baseline and report observed limitations; this is not application construction or training. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.foundation_outputs cols=['observation_id', 'cohort_id', 'output_kind', 'foundation_output'] ] caption: Supplied foundation output file aligned to validation
### r02 · Revisit: the practice — evaluate supplied outputs
(misconception) Contrast matched supplied-output evaluation with application construction. The verdict is bounded to aligned labeled validation observations and fixed requirements. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Use the same task-specific labeled validation examples and acceptance requirements as the reference. Compare supplied-output quality with the validation baseline and report observed limitations; this is not application construction or training. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.foundation_outputs cols=['observation_id', 'cohort_id', 'output_kind', 'foundation_output'] ] caption: Supplied foundation output file aligned to validation