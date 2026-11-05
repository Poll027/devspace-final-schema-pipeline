# EVALUATOR PACKET — A/B Test Structure and Lift (tile_stats_ab_test_lift)
Tile summary: Introduces the structure of a randomised A/B test (control group, treatment group, metric) and the concept of lift (relative improvement) using QuickRide's checkout-button experiment. Learners identify the parts of an experiment and compute lift from control and treatment conversion rates.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stats.ab_test_structure — Basic A/B test structure (control vs treatment group)
B = stats.lift_interpretation — Interpreting lift/percentage change between groups

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (stats.ab_test_structure)   objective: Given a description of an experiment, identify its control group, its treatment group, and the metric being compared between them.
A.f1: Studies where researchers assign treatments to cases are called experiments; when the assignment includes randomization, it is called a randomized experiment.   [sources: openintro_statistics_textbook#1.4]
A.f2: Researchers randomly assign cases to a control group and a treatment group so that differences between the groups that cannot otherwise be controlled are evened out.   [sources: openintro_statistics_textbook#1.4.1]
A.f3: A/B testing works by showing two variants of a page or experience to users at random: the original (control, or A) and a modified version (variation, or B); engagement with each version is measured and then compared against the baseline, the control.   [sources: optimizely_ab_testing_glossary#What is A/B testing?]
PRACTICE ANCHOR (field_selection): Given a short description of an A/B test scenario, identify which group is the control, which is the treatment, and which metric is being compared between them.  SUCCESS: The learner correctly labels the control group (original/A), the treatment group (modified/B), and names the single metric used to compare the two groups, with no confusion between the two roles.
ASSESSMENT ANCHOR: identify_control_and_treatment_groups_from_experiment_description facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: identify_metric_being_compared_in_ab_test facts=['f3']
ASSESSMENT ANCHOR: distinguish_randomized_experiment_from_non_randomized_study facts=['f1', 'f2']

## SOURCE FACTS — B (stats.lift_interpretation)   objective: Compute and interpret the lift (percentage change) between a treatment group's result and a control group's result.
B.f1: Relative improvement (lift) is the percentage difference in the variation's conversion rate over the baseline (control) conversion rate; for example, a 10% relative improvement over a 25% baseline conversion rate means the variation's conversion rate is 27.5%.   [sources: optimizely_improvement_intervals_guide#Improvement intervals]
B.f2: Relative improvement describes the variation's change as a percentage of the baseline's rate.   [sources: optimizely_improvement_intervals_guide#Improvement intervals]
B.f3: Analyzing an A/B test's results means determining whether the variation had a positive, negative, or neutral effect compared with the baseline (control).   [sources: optimizely_ab_testing_glossary#What is A/B testing?]
PRACTICE ANCHOR (live_code): Given a control conversion rate and a treatment conversion rate as Python floats, write a function that computes the lift and returns a string stating whether the variation had a positive, negative, or neutral effect and by how much.  SUCCESS: The function correctly computes lift as (treatment - control) / control * 100, returns a string that includes the numeric lift value and correctly labels the direction (positive, negative, or neutral) for at least three distinct input pairs.
ASSESSMENT ANCHOR: compute_lift_from_control_and_treatment_rates facts=['f1', 'f2']
ASSESSMENT ANCHOR: interpret_lift_direction_and_magnitude_in_ab_test_context facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: classify_ab_test_outcome_as_positive_negative_or_neutral facts=['f3']

## DATA ASSETS USED
ds_ab_test_summary: A/B Test Summary — Checkout Button — columns: group(categorical), users(numerical), conversions(numerical), conversion_rate(numerical)
   ["control",500,100,0.2]
   ["treatment",500,110,0.22]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Anticipating stakeholder questions and objections; Basic presentation structure (opening, body, call to action); Building a data model for the capstone dataset; Conceptual effect of sample size on confidence; Conceptual interpretation of statistical significance/confidence level; Converting a vague business question into a specific, measurable analytical question; Defining a capstone business question/problem statement; Drawing a business conclusion from an experiment-result summary; Framing an actionable recommendation that is distinct from the finding itself; Identifying stakeholder needs/requirements before analysis; Identifying the business decision a stakeholder needs the analysis to inform; Integrating Python/pandas cleaning and analysis into an end-to-end project; Integrating SQL querying into an end-to-end project; Integrating spreadsheet analysis into an end-to-end project; Interpreting lift/percentage change between groups; Making a data-driven recommendation; Matching chart type to the specific point being made (trend vs. comparison vs. distribution vs. part-to-whole); Prioritizing findings by relevance to the stakeholder's specific decision, not by analytical interestin

## LESSON, in learner order

### s01 · explainer · Two groups, one metric, one baseline  [reward 3]
A/B Test Structure — QuickRide's product team wants to know whether a redesigned checkout button gets more users to complete an order. Rather than guess, they run a controlled test — showing each user one version at random and measuring what happens.
### Randomised experiments: control vs treatment
(definition) Studies where researchers assign treatments to cases are called **experiments**. When the assignment includes randomisation, it is called a **randomised experiment**. Researchers randomly assign cases to a **control group** and a **treatment group** so that differences between the groups that cannot otherwise be controlled are evened out. ⟦A.f1 A.f2 A:tb2⟧
(mechanism) **A/B testing** works by showing two variants of a page or experience to users at random: the original (**control, or A**) and a modified version (**variation, or B**). Engagement with each version is measured and then compared against the baseline — the control. For the checkout button: the existing button is A, the redesigned button is B, and the metric compared is the share of each group that completes an order. ⟦A.f3 A:tb3⟧
[DIAGRAM: A/B test structure: population → two arms → comparison] nodes=['All app users', 'Random assignment', 'Control (A)\nOriginal checkout button', 'Treatment (B)\nRedesigned checkout button', 'Conversion rate A\n(baseline)', 'Conversion rate B', 'Compare B vs A\n(treatment vs baseline)'] edges=[('population', 'random_split', None), ('random_split', 'control_arm', '~50 %'), ('random_split', 'treatment_arm', '~50 %'), ('control_arm', 'control_metric', None), ('treatment_arm', 'treatment_metric', None), ('control_metric', 'comparison', None), ('treatment_metric', 'comparison', None)] alt: Diagram showing all app users flowing into a random-assignment step, which splits them into a control arm (original checkout button, conversion rate A as baseline) and a treatment arm (redesigned checkout button, conversion rate B). Both metric arrows point to a comparison step labelled 'Compare B vs A'.

### s02 · video · Watch: split testing in practice  [reward 1]
A/B Test Structure — This clip shows how A/B testing grew out of randomised controlled trials and names the two groups. Note: the clip calls the treatment group the 'experimental group' — Devspace uses 'treatment group'.
[VIDEO A/B test structure: two variants, one metric, one baseline] bridge-before:  | bridge-after: 

### s03 · check · Randomised vs non-randomised  [reward 2]
Quick check — Test your understanding of what makes an experiment randomised.

### s04 · hands_on · Identify the groups and metric  [reward 3]
Hands-on — Use the individual user records from the checkout-button test to identify which column marks the control and treatment groups, and which column records the metric being compared.

### s05 · explainer · Turning raw rates into a single comparison figure  [reward 3]
Lift — The checkout test is done: the control button converted 20 % of users, the redesigned button converted 22 %. Those two numbers need to be turned into a comparison that's easy to talk about — that's where lift comes in.
### Relative improvement (lift)
(definition) **Relative improvement (lift)** is the percentage difference in the variation's conversion rate over the baseline (control) conversion rate. For example, a 10 % relative improvement over a 25 % baseline means the variation's conversion rate is 27.5 %. Relative improvement describes the variation's change **as a percentage of the baseline's rate** — not as a percentage-point difference. ⟦B.f1 B.f2 B:tb2⟧
(example) Applying that to the checkout test: treatment rate 22 % minus control rate 20 % is a **2-percentage-point** absolute difference. As a percentage of the 20 % baseline: 2 ÷ 20 × 100 = **10 % lift**. The redesigned button produced a 10 % relative improvement over the original. ⟦B.f1 B:tb3⟧
[SIDE_BY_SIDE] Absolute difference: 0.22 − 0.20 = 0.02 (2 pp). Lift: 0.02 ÷ 0.20 × 100 = 10 % — the redesigned button produced a 10 % relative improvement over the baseline. left_label: Control (A) — original button | right_label: Treatment (B) — redesigned button
  left:
[TABLE computed result ] caption: Control group: 500 users, 100 conversions, rate = 0.20
  produced by sql: SELECT group, users, conversions, conversion_rate FROM ab_test_summary WHERE group = 'control'
  right:
[TABLE computed result ] caption: Treatment group: 500 users, 110 conversions, rate = 0.22
  produced by sql: SELECT group, users, conversions, conversion_rate FROM ab_test_summary WHERE group = 'treatment'

### s06 · check · Positive, negative, or neutral?  [reward 2]
Quick check — Practise classifying an A/B test outcome by its direction.

### s07 · hands_on · Compute lift and classify the outcome  [reward 4]
Hands-on — Write a Python function that computes lift from a control rate and a treatment rate, then returns a string stating whether the variation had a positive, negative, or neutral effect and by how much.

### s08 · recap · What you've learned  [reward 2]
Recap — Every A/B test has the same three parts, and lift turns the raw rates into one interpretable figure.
(takeaway) Every A/B test has a **control group**, a **treatment group**, and the **measure** being compared between them. The treatment group's result is compared against the control — the baseline. Analysing the results means determining whether the variation had a **positive, negative, or neutral** effect. **Lift** puts the observed difference into one figure: a positive lift means the variation's rate came out above the control's in this test; a negative lift means it came out below. ⟦A.f1 A.f2 A.f3 B.f3 A:tb4 B:tb4⟧
[UP NEXT] Up next: Sample Size and Statistical Significance: You can now compute lift — but how do you know whether a 10 % lift is a real signal or just random variation? The next tile introduces sample size and statistical significance: the tools that tell you whether your A/B test result is trustworthy.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · What makes an experiment randomised? — The check asked you to distinguish a randomised experiment from a non-randomised study. Here's the key contrast.
(definition) Studies where researchers **assign** treatments to cases are called **experiments**. When that assignment includes **randomisation**, it is a **randomised experiment**. Randomly assigning cases to a control group and a treatment group evens out differences between the groups that cannot otherwise be controlled — that's what makes the comparison fair. ⟦A.f1 A.f2 A:tb2⟧
(misconception) A non-randomised study lets participants choose their own group, or assigns them by convenience. Without random assignment, the two groups may differ in ways that affect the outcome — so you can't be sure the treatment caused any difference you observe. In the checkout-button test, users are randomly shown one version or the other, which is what makes it a randomised experiment. ⟦A.f1 A.f2 A:tb2 A:tb3⟧
### r02 · Identifying the groups and metric in an A/B test — The hands-on asked you to identify the control group, treatment group, and the metric being compared. Here's how to read the table.
(mechanism) In the user records table, the **`group`** column tells you which arm each user was assigned to: `'control'` for the original button (A) and `'treatment'` for the redesigned button (B). The **`converted`** column records the metric: 1 if the user completed an order, 0 if not. The metric being compared between the two groups is the **share of users who converted** — the conversion rate. ⟦A.f2 A.f3 A:tb3⟧
### r03 · Classifying a test outcome: positive, negative, or neutral — The check asked you to classify an A/B test outcome. Here's the rule.
(definition) Analysing an A/B test's results means determining whether the variation had a **positive**, **negative**, or **neutral** effect compared with the baseline (control). A **positive lift** means the variation's rate came out above the control's in this test. A **negative lift** means it came out below. A **neutral** result means the rates were effectively the same. ⟦B.f3 B:tb4⟧
### r04 · Computing lift step by step — The hands-on asked you to compute lift. Here's the calculation laid out clearly.
(definition) **Lift formula:** (treatment rate − control rate) ÷ control rate × 100. For the checkout test: (0.22 − 0.20) ÷ 0.20 × 100 = **10 % lift**. This is a relative improvement — it expresses the variation's change as a percentage of the baseline's rate, not as a raw percentage-point difference. ⟦B.f1 B.f2 B:tb2 B:tb3⟧
(example) Three cases to check your function against: (1) control=0.20, treatment=0.22 → **+10 % (positive)**. (2) control=0.25, treatment=0.20 → **−20 % (negative)**. (3) control=0.30, treatment=0.30 → **0 % (neutral)**. A positive lift means the variation's rate came out above the control's; a negative lift means it came out below. ⟦B.f1 B.f2 B.f3 B:tb3 B:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: Control (A)
Original checkout button
· nodes.label: Treatment (B)
Redesigned checkout button
· nodes.label: Conversion rate A
(baseline)
· nodes.label: Compare B vs A
(treatment vs baseline)