# EVALUATOR PACKET — A/B Test Structure and Lift (tile_stats_ab_test_lift)
Tile summary: Introduces the structure of a randomised A/B test (control group, treatment group, metric) and the concept of lift (relative improvement) using QuickRide's checkout-button experiment. Learners identify the parts of an experiment and compute lift from control and treatment conversion rates.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stats.ab_test_structure — Basic A/B test structure (control vs treatment group)
B = stats.lift_interpretation — Interpreting lift/percentage change between groups

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
ds_ab_test_users: A/B Test Individual User Records — Checkout Button — columns: user_id(identifier), group(categorical), converted(numerical)
   ["U-C001","control",1]
   ["U-C002","control",1]
   ["U-C003","control",1]
   ["U-C004","control",1]
   ["U-C005","control",1]
   ["U-C006","control",0]
   ["U-C007","control",0]
   ["U-C008","control",0]

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
[VIDEO A/B test structure: two variants, one metric, one baseline] bridge-before: Watch how the clip names the two groups and what gets measured. Note: the clip calls the treatment group the 'experimental group' — Devspace uses 'treatment group'. | bridge-after: The clip covers f3's structure but does not explain randomized assignment (f1, f2). The teaching text covers both.
  - FTpmwX94_Yo 7215-7310s facts=['f3'] label: Defining A/B test structure: control group, treatment group, and the metric tracked | summary: A/B testing (also called split testing) grew out of randomized controlled trials. The core idea: show the new or varied version of a product to one sample of users — the experimental group — and the existing version to a separate sample — the control group. The difference in product performance between the two groups is then tracked over the test period. If the varied version underperforms, the business can decide whether to refine it or explore other directions.

### s03 · check · Randomised vs non-randomised  [reward 2]
Quick check — Test your understanding of what makes an experiment randomised.
QUESTION [choice, core, grading=client] QuickRide's product team wants to test whether a redesigned checkout button increases order completion. They randomly assign each app user to see either the original button (control) or the redesigned button (treatment), then measure the share of each group that completes an order. Is this a randomised experiment?
  ✔ opt_yes: Yes — users are randomly assigned to control or treatment, so differences between the groups are evened out.
      why: Correct. Random assignment evens out differences between the groups that cannot otherwise be controlled, making this a randomised experiment. Each user is randomly shown one version or the other.
  ✘ opt_no_choice: No — users choose which button they see, so the two groups may differ in ways that affect the outcome.
      why: Users do not choose which button they see. The product team randomly assigns each user to control or treatment. When researchers assign treatments and include randomisation, it is a randomised experiment.
  ✘ opt_no_convenience: No — the team assigns users by convenience (e.g., time of day), not by random assignment.
      why: The team does not assign by convenience. Each user is randomly shown one version or the other. Random assignment is what makes this a randomised experiment.
  ✘ opt_no_observational: No — this is an observational study because the team is observing user behavior, not assigning treatments.
      why: This is not an observational study. The team is assigning treatments (which button each user sees), not just observing. Studies where researchers assign treatments are called experiments; when the assignment includes randomisation, it is a randomised experiment.
  feedback✔: Exactly right. Random assignment is the key feature that makes this a randomised experiment.  feedback✘: Think about who decides which button each user sees. Is it the user, or is it the product team assigning users at random?  hints: ["The prompt says users are 'randomly assigned' to see one version or the other. Who is doing the assigning?", 'Studies where researchers assign treatments to cases are called experiments. When the assignment includes randomisation, it is a randomised experiment.']  remediation→r01
  MEASURES: A:distinguish_randomized_experiment_from_non_randomized_study(f1,f2)   anchors=['assessment:distinguish_randomized_experiment_from_non_randomized_study']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Identify the groups and metric  [reward 3]
Hands-on — Use the individual user records from the checkout-button test to identify which column marks the control and treatment groups, and which column records the metric being compared.
QUESTION [table_select, core, grading=client] 
  intro shown to learner: The table below shows individual user records from the checkout-button A/B test. Each row is one user.
  task t1 (row): Select one row that belongs to the **control group** (users who saw the original button, A).  KEY: row={'group': 'control'} column=None expect=None dataset-says={'user_id': 'U-C001', 'group': 'control', 'converted': 1}
      feedback: {'correct': "Correct. The `group` column value 'control' identifies users who saw the original button (A).", 'incorrect': "Look for a row where the `group` column says 'control'. Those users saw the original button (A)."}
  task t2 (row): Select one row that belongs to the **treatment group** (users who saw the redesigned button, B).  KEY: row={'group': 'treatment'} column=None expect=None dataset-says={'user_id': 'U-T001', 'group': 'treatment', 'converted': 1}
      feedback: {'correct': "Correct. The `group` column value 'treatment' identifies users who saw the redesigned button (B).", 'incorrect': "Look for a row where the `group` column says 'treatment'. Those users saw the redesigned button (B)."}
  task t3 (column): Select the column that records the **metric being compared** between the two groups.  KEY: row=None column=converted expect=None dataset-says=None
      feedback: {'correct': 'Correct. The `converted` column records whether each user completed an order (1) or not (0). The metric being compared is the share of each group that converted — the conversion rate.', 'incorrect': 'The metric is what the team measures for each group. Look for the column that records whether each user completed an order.'}
  feedback✔: Well done. The `group` column identifies control vs treatment, and the `converted` column records the metric (whether each user completed an order). The comparison is between the two groups' conversion rates.  feedback✘: Check the `group` column to identify control vs treatment, and think about what the team is measuring for each group.  hints: ["The `group` column tells you which arm each user was assigned to: 'control' for the original button (A), 'treatment' for the redesigned button (B).", 'The metric being compared is the share of users who completed an order. Which column records whether each user converted?']  remediation→r02
  MEASURES: A:identify_control_and_treatment_groups_from_experiment_description(f1,f2,f3); A:identify_metric_being_compared_in_ab_test(f3)   anchors=['practice', 'assessment:identify_control_and_treatment_groups_from_experiment_description', 'assessment:identify_metric_being_compared_in_ab_test']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f3←s01

### s05 · explainer · Turning raw rates into a single comparison figure  [reward 3]
Lift — The checkout test is done: the control button converted 20 % of users, the redesigned button converted 22 %. Those two numbers need to be turned into a comparison that's easy to talk about — that's where lift comes in.
### Relative improvement (lift)
(definition) **Relative improvement (lift)** is the percentage difference in the variation's conversion rate over the baseline (control) conversion rate. For example, a 10 % relative improvement over a 25 % baseline means the variation's conversion rate is 27.5 %. Relative improvement describes the variation's change **as a percentage of the baseline's rate** — not as a percentage-point difference. ⟦B.f1 B.f2 B:tb2⟧
(example) Applying that to the checkout test: treatment rate 22 % minus control rate 20 % is a **2-percentage-point** absolute difference. As a percentage of the 20 % baseline: 2 ÷ 20 × 100 = **10 % lift**. The redesigned button produced a 10 % relative improvement over the original. ⟦B.f1 B:tb3⟧
[SIDE_BY_SIDE] Absolute difference: 0.22 − 0.20 = 0.02 (2 pp). Lift: 0.02 ÷ 0.20 × 100 = 10 % — the redesigned button produced a 10 % relative improvement over the baseline. left_label: Control (A) — original button | right_label: Treatment (B) — redesigned button
  left:
[TABLE computed result ] caption: Control group: 500 users, 100 conversions, rate = 0.20
  produced by sql: SELECT "group", users, conversions, conversion_rate FROM ab_test_summary WHERE "group" = 'control'
  result columns=['group', 'users', 'conversions', 'conversion_rate'] rows(1)=[["control",500,100,0.2]]
  right:
[TABLE computed result ] caption: Treatment group: 500 users, 110 conversions, rate = 0.22
  produced by sql: SELECT "group", users, conversions, conversion_rate FROM ab_test_summary WHERE "group" = 'treatment'
  result columns=['group', 'users', 'conversions', 'conversion_rate'] rows(1)=[["treatment",500,110,0.22]]
(takeaway) Analyzing an A/B test's results means determining whether the variation had a **positive**, **negative**, or **neutral** effect compared with the baseline (control). A **positive lift** means the variation's rate came out above the control's in this test. A **negative lift** means it came out below. A **neutral** result means the rates were effectively the same. ⟦B.f3 B:tb4⟧

### s06 · check · Positive, negative, or neutral?  [reward 2]
Quick check — Practise classifying an A/B test outcome by its direction.
QUESTION [choice, core, grading=client] An A/B test compared two email subject lines. The control (A) had a 15% open rate; the variation (B) had a 12% open rate. How would you classify this test's outcome?
  ✔ opt_negative: Negative — the variation's rate came out below the control's in this test.
      why: Correct. The variation's 12% open rate is below the control's 15%, so this is a negative outcome. The variation underperformed the baseline in this test.
  ✘ opt_positive: Positive — the variation's rate came out above the control's in this test.
      why: The variation's rate (12%) is below the control's rate (15%), not above. A positive outcome means the variation came out above the control.
  ✘ opt_neutral: Neutral — the rates were effectively the same.
      why: The rates are not the same: 12% vs 15% is a 3-percentage-point difference. A neutral outcome means the rates were effectively the same.
  ✘ opt_inconclusive: Inconclusive — you need to know the sample size before classifying the outcome.
      why: Sample size matters for statistical significance, but the question asks how to classify the outcome based on the observed rates. The variation's 12% is below the control's 15%, so the outcome is negative.
  feedback✔: Exactly right. The variation's rate came out below the control's, so this is a negative outcome.  feedback✘: Compare the two rates: control 15%, variation 12%. Which one is higher?  hints: ["A positive outcome means the variation's rate came out above the control's. A negative outcome means it came out below.", 'The control had a 15% open rate; the variation had a 12% open rate. Which one is higher?']  remediation→r03
  MEASURES: B:classify_ab_test_outcome_as_positive_negative_or_neutral(f3)   anchors=['assessment:classify_ab_test_outcome_as_positive_negative_or_neutral']
  taught-before-tested: B.f3←s05

### s07 · hands_on · Compute lift and classify the outcome  [reward 4]
Hands-on — Write a Python function that computes lift from a control rate and a treatment rate, then returns a string stating whether the variation had a positive, negative, or neutral effect and by how much.
QUESTION [code_exercise, stretch, grading=client] Write a function `compute_lift(control_rate, treatment_rate)` that computes the lift (percentage change) and returns a string stating the direction and magnitude.

The lift formula is: (treatment − control) ÷ control × 100. Classify the direction as 'Positive' if lift > 0, 'Negative' if lift < 0, or 'Neutral' if lift == 0.

The starter provides string constants and a template. Replace the two `None` placeholders with your calculations. The function is already called with three test cases.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def', 'return', 'float literals', 'arithmetic operators (-, /, *)', 'comparison operators (>, <, ==)', 'if/elif/else', 'f-strings', 'variable assignment'] blocked=7 items
  file solution.py [editable]:
POSITIVE = "Positive"
NEGATIVE = "Negative"
NEUTRAL = "Neutral"
SUFFIX = " lift of "
PCT = "%"

def compute_lift(control_rate, treatment_rate):
    # Compute lift: (treatment - control) / control * 100
    # Can also be written as: treatment / control * 100 - 100
    lift = None  # replace with: treatment_rate / control_rate * 100.0 - 100.0
    
    # Classify direction: positive if lift > 0, negative if lift < 0, neutral if lift == 0
    direction = None  # replace with: POSITIVE if lift > 0.0 else NEGATIVE if lift < 0.0 else NEUTRAL
    
    # Return formatted string
    return f"{direction}{SUFFIX}{lift}{PCT}"

print(compute_lift(0.10, 0.12))
print(compute_lift(0.15, 0.12))
print(compute_lift(0.25, 0.25))

  SOLUTION solution.py:
POSITIVE = "Positive"
NEGATIVE = "Negative"
NEUTRAL = "Neutral"
SUFFIX = " lift of "
PCT = "%"

def compute_lift(control_rate, treatment_rate):
    lift = treatment_rate / control_rate * 100.0 - 100.0
    direction = POSITIVE if lift > 0.0 else NEGATIVE if lift < 0.0 else NEUTRAL
    return f"{direction}{SUFFIX}{lift}{PCT}"

print(compute_lift(0.10, 0.12))
print(compute_lift(0.15, 0.12))
print(compute_lift(0.25, 0.25))

  test t_output (stdout_equals, visible=True): {"expected":"Positive lift of 20.0%\nNegative lift of -20.0%\nNeutral lift of 0.0%"} | on-fail: The printed output does not match. Check that your lift formula is correct and that you classify the direction correctly.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2e740ec460a47547a1cedcfc718eb2edd6ef059db899169d6ccb48b23d0cc2c6","tests_passed":1}
  feedback✔: Well done. Your function correctly computes lift and classifies the direction. Lift expresses the variation's change as a percentage of the baseline's rate.  feedback✘: Check your lift formula: (treatment − control) ÷ control × 100. Then classify: positive if lift > 0, negative if lift < 0, neutral if lift == 0.  hints: ['The lift formula is (treatment_rate - control_rate) / control_rate * 100.0. You can restructure it as treatment_rate / control_rate * 100.0 - 100.0 to avoid parentheses.', 'Use a ternary expression: POSITIVE if lift > 0.0 else NEGATIVE if lift < 0.0 else NEUTRAL.']  remediation→r04
  MEASURES: B:compute_lift_from_control_and_treatment_rates(f1,f2); B:interpret_lift_direction_and_magnitude_in_ab_test_context(f1,f2); B:classify_ab_test_outcome_as_positive_negative_or_neutral(f3)   anchors=['practice', 'assessment:compute_lift_from_control_and_treatment_rates', 'assessment:interpret_lift_direction_and_magnitude_in_ab_test_context', 'assessment:classify_ab_test_outcome_as_positive_negative_or_neutral']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f1←s05; B.f2←s05; B.f3←s05

### s08 · recap · What you've learned  [reward 2]
Recap — Every A/B test has the same three parts, and lift turns the raw rates into one interpretable figure.
(takeaway) Every A/B test has a **control group**, a **treatment group**, and the **measure** being compared between them. The treatment group's result is compared against the control — the baseline. Analysing the results means determining whether the variation had a **positive, negative, or neutral** effect. **Lift** puts the observed difference into one figure: a positive lift means the variation's rate came out above the control's in this test; a negative lift means it came out below. ⟦A.f1 A.f2 A.f3 B.f3 A:tb4 B:tb4⟧
[UP NEXT] Up next: Sample Size and Statistical Significance: You can now compute lift — but how do you know whether a 10 % lift is a real signal or just random variation? The next tile introduces the tools that tell you whether your A/B test result is trustworthy.

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
· constraints.blocked_syntax: hypothesis testing functions
· constraints.blocked_syntax: confidence interval calculations
· constraints.blocked_syntax: p-value computations
· spec.expected: Positive lift of 20.0%
Negative lift of -20.0%
Neutral lift of 0.0%
· expected.value: Positive_x lift of 20.0%
Negative lift of -20.0%
Neutral lift of 0.0%
· expected.value: Positive lift of 20.0%
Negative_x lift of -20.0%
Neutral lift of 0.0%