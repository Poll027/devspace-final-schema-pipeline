# EVALUATOR PACKET — Define the Prediction Task (mle.tile.000_000)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_task_definition — Frame a prediction task with prediction-time inputs

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: mle.tile.000_000.s01: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.prediction_task_definition)   objective: Define an unambiguous prediction record with its unit, target, decision time, horizon and permitted inputs.
A.f1: Define the prediction problem in terms of the inference to be generated and the example data needed to support it.   [sources: sagemaker_developer_guide#how-it-works-mlconcepts.html — The machine learning workflow]
A.f2: Inputs for a prediction must be information available at its prediction time, not information that only becomes available afterward.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f3: An empirical outcome proportion is the count of that outcome divided by the total count in the specified population; a conditional outcome proportion uses only the count in its specified conditioning group.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: Write the task record with one prediction unit, a target event or value, the time a prediction is made and the horizon over which the target is judged, so the example/target relationship is unambiguous.   [sources: google_ml_crash_course#https://developers.google.com/machine-learning/problem-framing/ml-framing — Define the ideal outcome and the model’s goal (weather, video and transaction tasks); Predict the decision, google_rules_of_ml#Rule 29; Rule 31 — serving-time features, scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Define the Prediction Task.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Complete a task record for the delivery-order example: identify the eligible population, one order at acceptance as the prediction unit, arrival more than 30 minutes after acceptance as the target event, prediction time, horizon and allowed inputs. Use the supplied counts to calculate the empirical outcome proportion for all 100 orders and the conditional proportion for the specified zone’s 40 orders.  SUCCESS: The record separates unit, population, target, prediction time and 30-minute horizon. It allows distance and promised delivery zone as inputs and excludes eventual arrival time. Calculations show 20/100 = 0.20 and 12/40 = 0.30, each labeled with its population and target horizon. The explanation connects these counts to a measurable order-level target without treating the zone proportion as applying to every zone.
ASSESSMENT ANCHOR: specify_prediction_unit_target_time_and_horizon facts=['f1', 'f4']
ASSESSMENT ANCHOR: restrict_inputs_to_prediction_time_information facts=['f2']

## DATA ASSETS USED
ds.outcome_counts: Outcome counts by declared population — columns: population(categorical), target_count(numerical), population_count(numerical), horizon_minutes(numerical)
   ["all orders",20,100,30]
   ["specified zone",12,40,30]
ds.task_record: Order-at-acceptance prediction task — columns: field(identifier), value(text)
   ["prediction_unit","one order at acceptance"]
   ["eligible_population","all 100 supplied accepted orders"]
   ["target_event","arrival more than 30 minutes after acceptance"]
   ["prediction_time","acceptance"]
   ["horizon","30 minutes"]
   ["allowed_inputs","distance; promised delivery zone"]
   ["excluded_input","eventual arrival time"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply vectorized array operations with compatible broadcasting; Choose leakage-safe train, validation and test splits matching deployment conditions; Choose numerical dtypes against precision and memory requirements; Compare model candidates against a baseline using validation evidence before freezing the choice; Compose a fitted preprocessing pipeline reused across training and bounded inference; Consume existing file or object-storage datasets in a format suited to ML access patterns; Define measurable model acceptance criteria from task objectives; Derive task-relevant features from prediction-time information; Detect target or preprocessing leakage across training and prediction boundaries; Encode categorical features with an unseen-category policy; Establish a simple reference prediction baseline; Fit and predict with a bounded scikit-learn baseline workflow; Fit missing-value imputation using training data only; Identify sampling and selection bias in dataset coverage; Inspect model-facing dataset structure, distributions and memory footprint; Justify classical versus neural modeling using validation quality, latency and cost evidence; Protect sensitive training and inference

## LESSON, in learner order

### s01 · explainer · Define the Prediction Task
Working rule — 
(intro) An operations team needs a delivery estimate at order acceptance. First define exactly what each prediction means and which inputs are available then. ⟦A:tb1⟧
(definition) Start with the inference you need and the example data that supports it. Use only inputs available when the prediction is made, not information arriving afterward. Empirical outcome proportion is outcome count divided by the specified population total. A conditional proportion uses only members of its stated group. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Specify one prediction unit, the target event or value, prediction time and judgement horizon so each example has an unambiguous target. ⟦A.f4 A:tb3⟧
[TABLE ds.task_record cols=all ] caption: Order-at-acceptance prediction task
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"ds.outcome_counts"},"range":"A1:E3","show_formula_bar":true,"cells":[{"ref":"E2","formula":"=B2/C2","note":"Outcome count divided by this row's specified population total."},{"ref":"E3","formula":"=B3/C3","note":"Outcome count divided by this row's specified population total."}],"annotations":[{"target":"E1","text":"Outcome proportion"}],"lineage":{"concept_ids":["mle.prediction_task_definition"],"teaching_block_ids":[],"fact_ids":[],"anchors":["mle.prediction_task_definition#visual"]},"computed_values":{"E2":0.2,"E3":0.3}}

### s02 · explainer · A bounded work example
Working rule — 
(example) In this fictional task, the order at acceptance is the unit. The task record separates target, decision time, horizon and permitted inputs. Later arrival establishes the target but is excluded from acceptance-time inputs. Divide each outcome count by the total for its own declared population: all orders and the specified zone answer different questions. Changing the unit or horizon changes the task, not merely its implementation. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · video · Trace the working rule
Optional walkthrough — 
[VIDEO Define the task and its prediction-time inputs] bridge-before: Watch how one order, its target and checkout-time inputs form a task record, called a “contract” here. The clip’s lateness target uses a checkout promise; our example uses 30 minutes after acceptance. | bridge-after: The clip establishes the prediction-time input boundary but supplies neither outcome-proportion calculations nor an explicit observation horizon. The text supplies both, including the full-population and zone-specific denominators.
  - zCu19zBMZXM 54-105s facts=['f1', 'f2'] label: An order-level task with checkout-time inputs | summary: A task record connects the intended prediction to the examples needed to support it. Here, each example represents one order. The speaker describes two possible targets: minutes from checkout to arrival, and whether arrival occurs after the delivery promise fixed at checkout. Predictions are made at checkout, so later dispatch information, the courier’s route and actual delivery cannot be inputs. The record also identifies the business decision the prediction supports, such as setting a delivery promise or offering an express upgrade, and whether the intended population includes future orders, unseen customers or both.

### s04 · explainer · A distinction to keep
Working rule — 
(misconception) Later arrival can establish the target, but cannot be an acceptance-time input. A zone denominator does not describe all orders. ⟦A.f2 A.f3 A:tb5⟧

### s05 · check · Judge the define the prediction task decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] An estimate is made at order acceptance. Which candidate must be excluded from its inputs?
  ✔ 0: Eventual arrival time
      why: Correct. Eventual arrival is known afterward; distance and promised zone are available at acceptance.
  ✘ 1: Promised delivery zone
      why: Eventual arrival is known afterward; distance and promised zone are available at acceptance.
  ✘ 2: Distance
      why: Eventual arrival is known afterward; distance and promised zone are available at acceptance.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Trace when each candidate input becomes available relative to order acceptance.']  remediation→r01
  MEASURES: A:restrict_inputs_to_prediction_time_information(f2)   anchors=[]
  taught-before-tested: A.f2←s01

### s06 · hands_on · Review define the prediction task
Practice — Read the supplied excerpts in this step and decide which satisfy the stated contract and which are defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each candidate task-record excerpt and decide whether it meets the order-at-acceptance task criterion. Judge its fields, input boundary and population-labeled calculations, not how you would implement a sheet.
  'prediction_unit: one order at acceptance
eligible_population: all 100 supplied accepted orders
target_event: arrival more than 30 minutes after acceptance
prediction_time: acceptance
horizon: 30 minutes
allowed_inputs: distance; promised delivery zone
excluded_input: eventual arrival time
all orders: 20/100 = 0.20; target horizon 30 minutes
specified zone: 12/40 = 0.30; target horizon 30 minutes
Interpretation: these counts measure the specified order-level target; the zone proportion is not a claim about every zone.' -> Meets declared criterion
      feedback: The record separates unit, population, target, time and horizon, excludes future arrival, and labels the two denominators.
  'prediction_unit: one order at acceptance
eligible_population: all 100 supplied accepted orders
target_event: arrival more than 30 minutes after acceptance
prediction_time: acceptance
horizon: 30 minutes
allowed_inputs: distance; promised delivery zone; eventual arrival time
excluded_input: eventual arrival time
all orders: 20/100 = 0.20; target horizon 30 minutes
specified zone: 12/40 = 0.30; target horizon 30 minutes' -> Violates declared criterion
      feedback: Eventual arrival is not available at acceptance and cannot be a prediction input.
  'prediction_unit: one order at acceptance
eligible_population: all 100 supplied accepted orders
target_event: arrival more than 30 minutes after acceptance
prediction_time: acceptance
horizon: 30 minutes
allowed_inputs: distance; promised delivery zone
excluded_input: eventual arrival time
all orders: 20/100 = 0.20; target horizon 30 minutes
specified zone: 12/40 = 0.30; target horizon 30 minutes
Interpretation: the specified-zone proportion applies to every zone.' -> Violates declared criterion
      feedback: The conditional denominator is the specified zone only, not every zone.
  'prediction_unit: one delivery zone
eligible_population: all 100 supplied accepted orders
target_event: arrival more than 30 minutes after acceptance
prediction_time: acceptance
horizon: 30 minutes
allowed_inputs: distance; promised delivery zone
excluded_input: eventual arrival time
all orders: 20/100 = 0.20; target horizon 30 minutes
specified zone: 12/40 = 0.30; target horizon 30 minutes' -> Violates declared criterion
      feedback: The counts and target concern orders, not a zone as the prediction unit.
  feedback✔: You judged each supplied implementation against its named criterion.  feedback✘: Find the exact operation or field that meets or violates the declared criterion.  hints: ['Check each excerpt against the task fields, availability boundary and labeled population.']  remediation→r02
  MEASURES: A:specify_prediction_unit_target_time_and_horizon(f1,f4); A:restrict_inputs_to_prediction_time_information(f2)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f4←s01; A.f2←s01

### s07 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) Later arrival can establish the target, but cannot be an acceptance-time input. A zone denominator does not describe all orders. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Validate NumPy input array shapes at the model boundary: Next: Validate NumPy input array shapes at the model boundary.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Define the Prediction Task
(definition) Use only inputs available when the prediction is made, not information arriving afterward. ⟦A.f2 A:tb2 A:tb4 A:tb5⟧
(example) Later arrival can establish the target, but cannot be an acceptance-time input. A zone denominator does not describe all orders. ⟦A.f2 A:tb2 A:tb4 A:tb5⟧
[TABLE ds.task_record cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Define the Prediction Task
(definition) Start with the inference you need and the example data that supports it. Use only inputs available when the prediction is made, not information arriving afterward. Specify one prediction unit, the target event or value, prediction time and judgement horizon so each example has an unambiguous target. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Later arrival can establish the target, but cannot be an acceptance-time input. A zone denominator does not describe all orders. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.task_record cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

=========

# EVALUATOR PACKET — Numerical Arrays for ML / Numerical Arrays for ML / Numerical Arrays for ML (mle.tile.001_003)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.numpy_shape_dtype — Validate NumPy input array shapes at the model boundary
B = mle.numpy_dtype_selection — Choose numerical dtypes against precision and memory requirements
C = mle.numpy_vectorization — Apply vectorized array operations with compatible broadcasting

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=6
  warn: mle.tile.001_003.s01: prose block without lineage.fact_ids
  warn: mle.tile.001_003.s05/ix.mle.tile.001_003.s05: ADVISORY — syntax descriptors with no detector: ['and, or, not', 'arithmetic with dimension integers', 'assert predicate', 'def with parameters', 'elementwise array arithmetic', 'function calls', 'if statements', 'integer, floating-point, boolean and string literals', 'list and tuple literals', 'scikit-learn imports', 'torch imports', 'try and except ValueError', 'tuple indexing after a rank check']
  warn: mle.tile.001_003.s06: prose block without lineage.fact_ids
  warn: mle.tile.001_003.s10/ix.mle.tile.001_003.s10: ADVISORY — syntax descriptors with no detector: ['MLflow logging calls', 'abs', 'array-wide arithmetic and broadcasting', 'boolean operators', 'cloud storage or managed-training client calls', 'for loops', 'function parameters and calls', 'lists and dictionaries', 'numeric and string literals', 'range', 'scalar comparisons', 'scalar subtraction and multiplication', 'sklearn preprocessing, fit, and predict calls', 'torch tensor construction and training calls', 'two-dimensional scalar indexing']
  warn: mle.tile.001_003.s11: prose block without lineage.fact_ids
  warn: mle.tile.001_003.s16/ix.mle.tile.001_003.s16: ADVISORY — syntax descriptors with no detector: ['==', 'array subtraction', 'assert', 'list comprehensions', 'list indexing', 'list literals', 'numeric literals', 'rtol and atol keyword arguments', 'tuple literals']

## SOURCE FACTS — A (mle.numpy_shape_dtype)   objective: Accept or reject a numerical input against a declared rank and batch/feature-axis contract.
A.f1: Create an array from the supplied list or tuple fixture with import numpy as np and np.array(fixture); inspect its ndim, shape and dtype.   [sources: numpy_user_guide#user/absolute_beginners.html — Attributes of an array; How to create a basic array]
A.f2: For a declared two-axis batch/feature contract, check a.ndim == 2 and compare a.shape[1] to the declared feature count before accepting the input.   [sources: numpy_user_guide#user/absolute_beginners.html — Attributes of an array; How to create a basic array]
A.f3: The shape tuple gives the length of each axis, so the batch-length requirement can be checked with a.shape[0] after checking rank.   [sources: numpy_user_guide#user/absolute_beginners.html — Attributes of an array; How to create a basic array]
A.f4: Reject a violated input requirement with a conditional raise ValueError(message), rather than continuing with an invalid array.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
A.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Numerical Arrays for ML.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write your own NumPy import and parameterized validator for order fixtures with two features per order and an accepted batch length of one through three orders. Convert each list or tuple fixture into an array; assign and inspect rank, shape, dtype, dimension lengths and boolean check results. Check rank before indexing axis lengths, use arithmetic dimension comparisons, and conditionally raise ValueError for invalid inputs. Return the accepted array. Write assertions covering valid, boundary, empty and malformed fixtures, including assertions that rejected fixtures raise ValueError.  SUCCESS: The learner-written function accepts one-order and three-order fixtures of width two, including both list and tuple inputs. It rejects an empty fixture, a flat six-value fixture, a rank-two fixture of width one and a four-order fixture. Assertions verify accepted shapes and expected rejection without accessing a missing axis. Rank, dimension, dtype and boolean variables are inspectable; dtype is observed without selecting or converting its representation.
ASSESSMENT ANCHOR: inspect_array_rank_shape_and_dtype facts=['f1']
ASSESSMENT ANCHOR: decide_acceptance_under_batch_feature_contract facts=['f2', 'f3']
ASSESSMENT ANCHOR: distinguish_input_rejection_from_fixture_assertions facts=['f4', 'f5']

## SOURCE FACTS — B (mle.numpy_dtype_selection)   objective: Choose a numerical representation by checking its value preservation and element-memory cost.
B.f1: A numerical dtype specifies a representable value range and a bit width, so candidate integer and floating types need not preserve the same input values.   [sources: numpy_user_guide#user/basics.types.html — Array types and conversions between types; Numerical Data Types; Overflow errors]
B.f2: Inspect a.dtype and explicitly cast with a.astype(candidate_dtype) when comparing representations.   [sources: numpy_user_guide#user/basics.types.html — Array types and conversions between types; Numerical Data Types; Overflow errors]
B.f3: For a fixed-width numerical array, a.size × a.itemsize is its element-storage byte count, exposed by a.nbytes; it excludes non-element object overhead.   [sources: numpy_user_guide#reference/generated/numpy.ndarray.nbytes.html]
B.f4: Compare the cast values with the reference values using arithmetic differences before accepting a lower-precision representation; casting can overflow or lose precision.   [sources: numpy_user_guide#user/basics.types.html — Array types and conversions between types; Numerical Data Types; Overflow errors]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Numerical Arrays for ML.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_shape_dtype. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the NumPy import and a learner-defined Python function that compares two supplied numerical dtypes for the six-value order feature matrix. Retain the reference matrix, explicitly cast it into each candidate dtype, inspect each dtype, calculate element-storage bytes, and use scalar arithmetic differences to check every value against the supplied tolerance and range requirements. Return the choice and its justification under the declared storage budget, or report that neither candidate satisfies the requirements.  SUCCESS: Both candidates are explicitly cast from the unchanged reference. Their element counts remain unchanged, their size-times-itemsize totals agree with nbytes, and every supplied value—including boundary fixtures—is checked against the reference. The returned justification distinguishes element storage from total object memory and accepts only a candidate satisfying the declared value-preservation and storage requirements.
ASSESSMENT ANCHOR: evaluate_dtype_range_and_precision_preservation facts=['f1', 'f4']
ASSESSMENT ANCHOR: inspect_and_explicitly_cast_candidate_dtypes facts=['f2']
ASSESSMENT ANCHOR: calculate_fixed_width_element_storage facts=['f3']
ASSESSMENT ANCHOR: choose_dtype_within_precision_and_memory_limits facts=['f1', 'f3', 'f4']

## SOURCE FACTS — C (mle.numpy_vectorization)   objective: Implement shape-correct array arithmetic and verify agreement with a bounded reference.
C.f1: NumPy arithmetic operations can operate elementwise on arrays instead of executing a Python operation once per observation.   [sources: numpy_user_guide#user/basics.broadcasting.html — General broadcasting rules]
C.f2: Broadcasting compares axes from the right; aligned lengths must be equal or one must be 1, and missing leading axes are treated as length 1.   [sources: numpy_user_guide#user/basics.broadcasting.html — General broadcasting rules]
C.f3: Check the resulting shape as well as operand compatibility, because compatible broadcasting can expand the result to a larger shape.   [sources: numpy_user_guide#user/basics.broadcasting.html — General broadcasting rules]
C.f4: Use np.testing.assert_allclose(array_result, reference_result, rtol=..., atol=...) to test agreement with the list-comprehension reference under explicit tolerances.   [sources: numpy_user_guide#reference/generated/numpy.testing.assert_allclose.html]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Numerical Arrays for ML.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_shape_dtype. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Within supplied execution scaffolding, write a Python function and its NumPy import. Replace the row-wise subtraction for [[2, 10], [4, 20], [6, 30]] and feature references [1, 5] with an array expression. Author a list-comprehension reference, an intended-shape assertion, and an explicit-tolerance agreement check.  SUCCESS: The learner-defined function returns [[1, 5], [3, 15], [5, 25]] as an array of shape (3, 2). Learner-written assertions independently check the intended shape and agreement with the list-comprehension reference using explicit rtol and atol values.
ASSESSMENT ANCHOR: express_elementwise_numeric_transform facts=['f1']
ASSESSMENT ANCHOR: check_broadcast_compatibility_and_intended_shape facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_array_result_with_explicit_tolerances facts=['f4']

## DATA ASSETS USED
ds.dtype_reference: Six-value dtype comparison reference — columns: distance(numerical), feature_2(numerical)
   [1.25,10]
   [4,20]
   [6,30]
ds.order_features: Three observations with two numerical features — columns: distance(numerical), feature_2(numerical)
   [2,10]
   [4,20]
   [6,30]
   variant one_order: 2 ops; planted: 
   variant wrong_width: 1 ops; planted: 
   variant four_orders: 1 ops; planted: 
   variant empty: 3 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply vectorized array operations with compatible broadcasting; Choose leakage-safe train, validation and test splits matching deployment conditions; Choose numerical dtypes against precision and memory requirements; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compose a fitted preprocessing pipeline reused across training and bounded inference; Consume existing file or object-storage datasets in a format suited to ML access patterns; Define measurable model acceptance criteria from task objectives; Derive task-relevant features from prediction-time information; Detect target or preprocessing leakage across training and prediction boundaries; Encode categorical features with an unseen-category policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Fit and predict with a bounded scikit-learn baseline workflow; Fit missing-value imputation using training data only; Identify sampling and selection bias in dataset coverage; Inspect model-facing dataset structure, distributions and memory footprint; 

## LESSON, in learner order

### s01 · explainer · Numerical Arrays for ML
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(mechanism) Import numpy as np, create np.array(fixture) from the supplied list or tuple, and inspect ndim, shape and dtype. For a two-axis batch/feature contract, check a.ndim == 2 before comparing a.shape[1] with the required feature count. Each shape entry is an axis length. After checking rank, use a.shape[0] to check the batch-length requirement. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Reject an input requirement violation with a conditional raise ValueError(message), rather than continuing with invalid input. Use assert predicate for valid, boundary and failure fixtures. In ordinary non-optimized execution, a false predicate raises AssertionError. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.order_features cols=all ] caption: Three observations with two numerical features
[CODE python]
fixture = {'contract': {'feature_count': 2, 'min_batch': 1, 'max_batch': 3},
 'valid': [[2, 10], [4, 20], [6, 30]],
 'single_row_boundary': [[2, 10]],
 'empty': [],
 'flat': [2, 10, 4, 20, 6, 30],
 'wrong_width': [[2], [4], [6]],
 'too_many': [[2, 10], [4, 20], [6, 30], [2, 10]]}

import numpy as np

def inspect_input(values, contract):
    a = np.array(values)
    print("rank, shape, dtype:", a.ndim, a.shape, a.dtype)
    if a.ndim != 2:
        raise ValueError("expected batch/feature axes")
    if a.shape[1] != contract["feature_count"]:
        raise ValueError("feature width violated")
    if not contract["min_batch"] <= a.shape[0] <= contract["max_batch"]:
        raise ValueError("batch length violated")
    return a

for name in ("valid", "single_row_boundary", "flat", "wrong_width", "too_many"):
    try:
        accepted = inspect_input(fixture[name], fixture["contract"])
        assert accepted.ndim == 2
        print(name, "accepted")
    except ValueError as error:
        print(name, str(error))
  annotations: []

### s02 · explainer · A bounded work example
Working rule — 
(example) The order matrix has one row per order and one column per feature. Flattening those same values destroys the declared two-axis interpretation. Check rank first, then feature width and batch length; a narrow matrix fails a different requirement from a flat one. Explicit ValueError rejects invalid inputs, while assertions exercise valid, boundary and failure fixtures. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · A distinction to keep
Working rule — 
(misconception) The flat fixture and matrix can contain the same values, yet only the matrix has the declared batch/feature axes. ⟦A.f2 A.f4 A.f5 A:tb5⟧

### s04 · check · Judge the numerical arrays for ml decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] A model boundary accepts one through three orders, with two features per order. Which input passes both checks?
  ✔ 0: Rank two, shape (3, 2)
      why: Correct. Rank one lacks the two-axis contract; four orders exceed the batch limit.
  ✘ 1: Rank one, shape (6,)
      why: Rank one lacks the two-axis contract; four orders exceed the batch limit.
  ✘ 2: Rank two, shape (4, 2)
      why: Rank one lacks the two-axis contract; four orders exceed the batch limit.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check rank before interpreting axes, then check feature width and batch size.']  remediation→r01
  MEASURES: A:decide_acceptance_under_batch_feature_contract(f2,f3)   anchors=[]
  taught-before-tested: A.f2←s01; A.f3←s01

### s05 · hands_on · Verify numerical arrays for ml
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Write the NumPy import and validate(fixture), returning the accepted array. Inspect rank, shape, dtype and boolean decisions locally. Check rank before axes; accept only width two and batches one through three. Assign result for fixture. Author assertions for the list and tuple boundary, empty, flat, wrong-width and too-many fixtures; reject with ValueError, not premature axis access.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'def with parameters', 'return', 'variable assignment', 'list and tuple literals', 'integer, floating-point, boolean and string literals', 'np.array(fixture)', 'a.ndim', 'a.shape', 'a.dtype', 'tuple indexing after a rank check', 'arithmetic with dimension integers', 'comparison operators', 'and, or, not', 'if statements', 'raise ValueError(message)', 'assert predicate', 'try and except ValueError', 'function calls', 'type(variable)'] blocked=10 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'contract': {'feature_count': 2, 'min_batch': 1, 'max_batch': 3},
 'valid': [[2, 10], [4, 20], [6, 30]],
 'tuple_boundary': ((2, 10),),
 'empty': [],
 'flat': [2, 10, 4, 20, 6, 30],
 'wrong_width': [[2], [4], [6]],
 'too_many': [[2, 10], [4, 20], [6, 30], [2, 10]]}

fixture = FIXTURES['valid']
boundary = ((2, 10),)

# TODO: write your implementation and assertions below.

def validation_outcome(fixture):
    try:
        return {'accepted': True, 'array':validate(fixture)}
    except ValueError:
        return {'accepted':False}

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'contract': {'feature_count': 2, 'min_batch': 1, 'max_batch': 3},
 'valid': [[2, 10], [4, 20], [6, 30]],
 'tuple_boundary': ((2, 10),),
 'empty': [],
 'flat': [2, 10, 4, 20, 6, 30],
 'wrong_width': [[2], [4], [6]],
 'too_many': [[2, 10], [4, 20], [6, 30], [2, 10]]}

fixture = FIXTURES['valid']
boundary = ((2, 10),)

import numpy as np
def validate(fixture):
    a = np.array(fixture)
    rank = a.ndim
    shape = a.shape
    dtype = a.dtype
    rank_ok = rank == 2
    if not rank_ok:
        raise ValueError('rank must be two')
    batch = shape[0]
    features = shape[1]
    width_ok = features == 2
    batch_ok = batch >= 1 and batch <= 3
    if not (width_ok and batch_ok):
        raise ValueError('batch or width violates contract')
    return a
result = validate(fixture)
assert result.shape == (3, 2)
assert validate(boundary).shape == (1, 2)
try:
    validate(FIXTURES['empty'])
    assert False
except ValueError:
    pass
try:
    validate(FIXTURES['flat'])
    assert False
except ValueError:
    pass
try:
    validate(FIXTURES['wrong_width'])
    assert False
except ValueError:
    pass
try:
    validate(FIXTURES['too_many'])
    assert False
except ValueError:
    pass

def validation_outcome(fixture):
    try:
        return {'accepted': True, 'array':validate(fixture)}
    except ValueError:
        return {'accepted':False}

  test call0 (function_call, visible=False): {"function":"validate","args":[[[2,10],[4,20],[6,30]]],"expected":[[2,10],[4,20],[6,30]]} | on-fail: The parameterized function fails a supplied boundary fixture.
  test call1 (function_call, visible=False): {"function":"validate","args":[[[2,10]]],"expected":[[2,10]]} | on-fail: The parameterized function fails a supplied boundary fixture.
  test empty (function_call, visible=False): {"function":"validation_outcome","args":[[]],"expected":{"accepted":false}} | on-fail: The declared invalid boundary must reject with ValueError.
  test flat (function_call, visible=False): {"function":"validation_outcome","args":[[2,10,4,20,6,30]],"expected":{"accepted":false}} | on-fail: The declared invalid boundary must reject with ValueError.
  test wrong_width (function_call, visible=False): {"function":"validation_outcome","args":[[[2],[4],[6]]],"expected":{"accepted":false}} | on-fail: The declared invalid boundary must reject with ValueError.
  test too_many (function_call, visible=False): {"function":"validation_outcome","args":[[[2,10],[4,20],[6,30],[2,10]]],"expected":{"accepted":false}} | on-fail: The declared invalid boundary must reject with ValueError.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9c598fba813d413e672bd8deae4d4cfd8aa9d2c32cbf057364ccf1ac2746fc63","tests_passed":6}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Validate rank before accessing axis lengths; test both accepted and rejected shapes.']  remediation→r02
  MEASURES: A:inspect_array_rank_shape_and_dtype(f1); A:distinguish_input_rejection_from_fixture_assertions(f4,f5)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f4←s01; A.f5←s01

### s06 · explainer · Numerical Arrays for ML
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦B:tb1⟧
(mechanism) Numerical dtypes have a representable range and bit width; integer and floating candidates may preserve different values. Inspect a.dtype and compare explicit casts made with a.astype(candidate_dtype). For fixed-width numerical arrays, a.size * a.itemsize equals a.nbytes: element-storage bytes, excluding non-element object overhead. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Before accepting lower precision, subtract reference values from cast values. A cast can overflow or lose precision. ⟦B.f4 B:tb3⟧
[TABLE ds.dtype_reference cols=all ] caption: Six-value dtype comparison reference
[SIDE_BY_SIDE] Check fidelity against retained references as well as the supplied element budget. left_label: Floating candidates and boundary probe | right_label: Integer cast contrast
  left:
[CODE python]
fixture = {'a': [[1.25, 10], [4, 20], [6, 30]],
 'candidate_dtypes': ['float64', 'float32'],
 'boundary_values': [1.25, 1.0, 16777217.0],
 'tolerance': 0.0,
 'element_storage_budget': 24}

import numpy as np
reference = np.array(fixture["a"], dtype=np.float64)
boundary = np.array(fixture["boundary_values"], dtype=np.float64)
for dtype in fixture["candidate_dtypes"]:
    candidate = reference.astype(dtype)
    differences = candidate.astype(np.float64) - reference
    boundary_differences = boundary.astype(dtype).astype(np.float64) - boundary
    faithful = bool(np.all(np.abs(differences) <= fixture["tolerance"]) and
                    np.all(np.abs(boundary_differences) <= fixture["tolerance"]))
    within_budget = candidate.nbytes <= fixture["element_storage_budget"]
    print(dtype, candidate, differences, boundary_differences)
    print("dtype, count, itemsize, calculated bytes, nbytes:", candidate.dtype,
          candidate.size, candidate.itemsize, candidate.size * candidate.itemsize, candidate.nbytes)
    print("faithful, within element budget, accepted:", faithful, within_budget, faithful and within_budget)
  annotations: []
  right:
[CODE python]
fixture = {'integer_cast_probe': {'reference': [1.25], 'candidate_dtype': 'int64'}}

import numpy as np
reference = np.array(fixture["integer_cast_probe"]["reference"], dtype=np.float64)
candidate = reference.astype(fixture["integer_cast_probe"]["candidate_dtype"])
print("retained reference, integer candidate, arithmetic difference:", reference, candidate, candidate - reference)
  annotations: []

### s07 · explainer · A bounded work example
Working rule — 
(example) Retain the reference while comparing candidate casts. Inspect dtype, element count, itemsize and nbytes; subtract reference values to reveal precision changes, including the boundary probe. Apply the supplied tolerance and element-storage budget together. A smaller representation does not establish acceptable differences, and element bytes exclude other object overhead. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧

### s08 · explainer · A distinction to keep
Working rule — 
(misconception) A smaller cast can meet a byte budget while failing value fidelity; keep the unchanged reference for comparison. ⟦B.f3 B.f4 B:tb5⟧

### s09 · check · Judge the numerical arrays for ml decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] A lower-width cast saves bytes but one scalar difference exceeds the declared tolerance. What is the defensible decision?
  ✔ 0: Reject it despite the byte saving
      why: Correct. Storage saving and unchanged shape do not establish value preservation.
  ✘ 1: Accept it because nbytes is smaller
      why: Storage saving and unchanged shape do not establish value preservation.
  ✘ 2: Accept it because shape is unchanged
      why: Storage saving and unchanged shape do not establish value preservation.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Compare value preservation with tolerance separately from byte savings.']  remediation→r03
  MEASURES: B:choose_dtype_within_precision_and_memory_limits(f1,f3,f4)   anchors=[]
  taught-before-tested: B.f1←s06; B.f3←s06; B.f4←s06

### s10 · hands_on · Verify numerical arrays for ml
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Implement compare(reference, boundaries, candidates, tolerance, budget). Cast BOTH candidates from the unchanged reference and boundary arrays. Check every scalar difference against tolerance and record count, calculated_bytes, nbytes, differences, boundary_differences and accepted under each candidate. Return candidates, choice (last qualifying candidate, or neither), and the element-storage justification shown by the task contract. Assign result from the supplied inputs. Do not accept byte saving without value preservation. Report differences as row/column-index dictionaries and boundary_differences by column index; justification must state: Only preserved values within the element-storage budget qualify; element bytes exclude total object and process overhead. Store absolute differences: abs(cast[i, j] - reference[i, j]) and abs(boundary_cast[0, j] - boundaries[0, j]). Compare those absolute differences with tolerance.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'def', 'function parameters and calls', 'return', 'variable assignment', 'for loops', 'range', 'if/elif/else', 'numeric and string literals', 'lists and dictionaries', 'a.shape', 'a.dtype', 'a.size', 'a.itemsize', 'a.nbytes', 'a.astype(candidate_dtype)', 'two-dimensional scalar indexing', 'scalar subtraction and multiplication', 'abs', 'scalar comparisons', 'boolean operators'] blocked=12 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'a': [[1.25, 10], [4, 20], [6, 30]],
 'candidate_dtypes': ['float64', 'float32'],
 'boundary_values': [1.25, 1.0, 16777217.0],
 'tolerance': 0.0,
 'element_storage_budget': 24,
 'integer_cast_probe': {'reference': [1.25], 'candidate_dtype': 'int64'},
 'policy_note': 'Tolerance and budget are supplied illustrative policy; byte '
                'saving alone never establishes acceptance.'}

import numpy as np
reference = np.array(FIXTURES['a'])
boundaries = np.array([FIXTURES['boundary_values']])
candidates = FIXTURES['candidate_dtypes']
tolerance = 0.0
budget = 24

row_count = reference.shape[0]
column_count = reference.shape[1]
boundary_count = boundaries.shape[1]
# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'a': [[1.25, 10], [4, 20], [6, 30]],
 'candidate_dtypes': ['float64', 'float32'],
 'boundary_values': [1.25, 1.0, 16777217.0],
 'tolerance': 0.0,
 'element_storage_budget': 24,
 'integer_cast_probe': {'reference': [1.25], 'candidate_dtype': 'int64'},
 'policy_note': 'Tolerance and budget are supplied illustrative policy; byte '
                'saving alone never establishes acceptance.'}

import numpy as np
reference = np.array(FIXTURES['a'])
boundaries = np.array([FIXTURES['boundary_values']])
candidates = FIXTURES['candidate_dtypes']
tolerance = 0.0
budget = 24

def compare(reference, boundaries, candidates, tolerance, budget):
    row_count = reference.shape[0]
    column_count = reference.shape[1]
    boundary_count = boundaries.shape[1]
    records = {}
    choice = 'neither'
    for candidate in candidates:
        cast = reference.astype(candidate)
        boundary_cast = boundaries.astype(candidate)
        inspected_dtype = cast.dtype
        calculated = cast.size * cast.itemsize
        preserve = cast.size == reference.size and calculated == cast.nbytes
        differences = {}
        for i in range(row_count):
            row = {}
            for j in range(column_count):
                difference = abs(cast[i,j] - reference[i,j])
                row[j] = difference
                if difference > tolerance:
                    preserve = False
            differences[i] = row
        boundary_differences = {}
        for j in range(boundary_count):
            difference = abs(boundary_cast[0,j] - boundaries[0,j])
            boundary_differences[j] = difference
            if difference > tolerance:
                preserve = False
        accepted = preserve and calculated <= budget
        records[candidate] = {'count':cast.size,'calculated_bytes':calculated,'nbytes':cast.nbytes,'differences':differences,'boundary_differences':boundary_differences,'accepted':accepted}
        if accepted:
            choice = candidate
    return {'candidates':records,'choice':choice,'justification':'Only preserved values within the element-storage budget qualify; element bytes exclude total object and process overhead.'}
result = compare(reference, boundaries, candidates, tolerance, budget)

  test result (value_equals, visible=True): {"expr":"result","expected":{"candidates":{"float64":{"count":6,"calculated_bytes":48,"nbytes":48,"differences":{"0":{"0":0,"1":0},"1":{"0":0,"1":0},"2":{"0":0,"1":0}},"boundary_differences":{"0":0,"1":0,"2":0},"accepted":false},"float32":{"count":6,"calculated_bytes":24,"nbytes":24,"differences":{"0":{"0":0,"1":0},"1":{"0":0,"1":0},"2":{"0":0,"1":0}},"boundary_differences":{"0":0,"1":0,"2":1},"accepted":false}},"choice":"neither","justification":"Only preserved values within the element-storage | on-fail: The named result does not meet the declared contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"08fc935bc9a638026f6272ace710753dd63474f16affbd49a068ffedc4e234c1","tests_passed":1}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Evaluate precision and element storage separately for each cast from the reference.']  remediation→r04
  MEASURES: B:evaluate_dtype_range_and_precision_preservation(f1,f4); B:inspect_and_explicitly_cast_candidate_dtypes(f2); B:calculate_fixed_width_element_storage(f3); B:choose_dtype_within_precision_and_memory_limits(f1,f3,f4)   anchors=['practice']
  taught-before-tested: B.f1←s06; B.f4←s06; B.f2←s06; B.f3←s06; B.f1←s06; B.f3←s06; B.f4←s06

### s11 · explainer · Numerical Arrays for ML
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦C:tb1⟧
(mechanism) NumPy arithmetic can act elementwise on arrays rather than performing one Python operation per observation. Broadcasting aligns axes from the right. Aligned lengths must match or one must be 1; missing leading axes count as length 1. Check result shape separately from operand compatibility: compatible broadcasting can expand the result. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Compare against a list-comprehension reference with np.testing.assert_allclose(array_result, reference_result, rtol=..., atol=...) using explicit tolerances. ⟦C.f4 C:tb3⟧
[TABLE ds.order_features cols=all ] caption: Three observations with two numerical features
[CODE python]
fixture = {'matrix': [[2, 10], [4, 20], [6, 30]],
 'feature_references': [1, 5],
 'expected_shape': [3, 2],
 'broadcast_column': [[2], [4], [6]],
 'broadcast_row': [[1, 5]],
 'rtol': 1e-07,
 'atol': 1e-09}

import numpy as np
matrix = np.array(fixture["matrix"])
references = np.array(fixture["feature_references"])
result = matrix - references
independent = np.array([[value - ref for value, ref in zip(row, fixture["feature_references"])]
                        for row in fixture["matrix"]])
np.testing.assert_allclose(result, independent, rtol=fixture["rtol"], atol=fixture["atol"])
assert result.shape == tuple(fixture["expected_shape"])
print("operands:", matrix.shape, references.shape)
print("result and reference:", result, independent, result.shape)
column = np.array(fixture["broadcast_column"])
row = np.array(fixture["broadcast_row"])
expanded = column - row
print("compatible expansion:", column.shape, row.shape, expanded.shape, expanded)
assert expanded.shape != column.shape
  annotations: []

### s12 · explainer · A bounded work example
Working rule — 
(example) Subtract the feature-reference vector from the order matrix and check against an independent list-comprehension calculation. Right-aligned compatibility permits the operation, but the resulting shape must still match the contract. The column/row contrast broadcasts successfully while expanding the result: success alone is not shape acceptance. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4⟧

### s13 · explainer · A distinction to keep
Working rule — 
(misconception) Broadcast-compatible does not mean contract-shaped: the column/row example expands the output. ⟦C.f2 C.f3 C:tb5⟧

### s14 · video · Trace the working rule
Optional walkthrough — 
[VIDEO Compatible broadcasting can expand the result] bridge-before: Watch how a single row and a single column combine into a multiplication table. Distinguish the operand compatibility checks from the stated dimensions of the result. | bridge-after: The clip demonstrates shape expansion. The text also teaches the Python-versus-array distinction, the complete right-aligned rule including missing leading axes, and tolerance-based comparison with a list-comprehension reference.
  - P67wiuTx7l0 252-358s facts=['f3'] label: Broadcast a row and column into a 10-by-10 multiplication table | summary: A two-dimensional row containing the numbers 1 through 10 is multiplied by a two-dimensional column containing the same numbers. Their shapes are inspected: each aligned dimension either matches or has length 1, so the operands are compatible. Multiplication produces a table with 10 rows and 10 columns, larger than either operand. Compatibility therefore does not guarantee that the result has the intended shape.

### s15 · check · Judge the numerical arrays for ml decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] For elementwise subtraction of a feature reference from each observation, which approach applies NumPy arithmetic to the array?
  ✔ 0: Subtract the reference array from the observation array
      why: Correct. Array arithmetic supports elementwise operations; a per-observation Python loop is not the requested vectorized expression.
  ✘ 1: Call a Python scalar subtraction separately for each observation
      why: Array arithmetic supports elementwise operations; a per-observation Python loop is not the requested vectorized expression.
  ✘ 2: Declare that array arithmetic is impossible without a Python loop
      why: Array arithmetic supports elementwise operations; a per-observation Python loop is not the requested vectorized expression.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Choose the expression that subtracts the reference from the whole observation array rather than calling Python subtraction once per observation.']  remediation→r05
  MEASURES: C:express_elementwise_numeric_transform(f1)   anchors=[]
  taught-before-tested: C.f1←s11

### s16 · hands_on · Verify numerical arrays for ml
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, stretch, grading=client] Write the NumPy import and subtract(matrix, references). Use elementwise array subtraction, independently build a row-wise list-comprehension reference, assert the input matrix shape is preserved, and check agreement with the supplied explicit rtol and atol. Return the array and assign result for the provided fixture.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'def', 'return', 'variable assignment', 'numeric literals', 'list literals', 'list comprehensions', 'list indexing', 'np.array', 'array subtraction', '.shape', 'tuple literals', 'assert', '==', 'np.testing.assert_allclose', 'rtol and atol keyword arguments'] blocked=7 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'matrix': [[2, 10], [4, 20], [6, 30]],
 'feature_references': [1, 5],
 'expected_shape': (3, 2),
 'broadcast_column': [[2], [4], [6]],
 'broadcast_row': [[1, 5]],
 'rtol': 1e-07,
 'atol': 1e-09}

matrix = FIXTURES['matrix']
references = FIXTURES['feature_references']
rtol = FIXTURES['rtol']
atol = FIXTURES['atol']

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'matrix': [[2, 10], [4, 20], [6, 30]],
 'feature_references': [1, 5],
 'expected_shape': (3, 2),
 'broadcast_column': [[2], [4], [6]],
 'broadcast_row': [[1, 5]],
 'rtol': 1e-07,
 'atol': 1e-09}

matrix = FIXTURES['matrix']
references = FIXTURES['feature_references']
rtol = FIXTURES['rtol']
atol = FIXTURES['atol']

import numpy as np
def subtract(matrix, references):
    result = np.array(matrix) - np.array(references)
    reference = [[row[0]-references[0], row[1]-references[1]] for row in matrix]
    assert result.shape == np.array(matrix).shape
    np.testing.assert_allclose(result, reference, rtol=rtol, atol=atol)
    return result
result = subtract(matrix, references)

  test call0 (function_call, visible=False): {"function":"subtract","args":[[[2,10],[4,20],[6,30]],[1,5]],"expected":[[1,5],[3,15],[5,25]]} | on-fail: The parameterized function fails a supplied boundary fixture.
  test call1 (function_call, visible=False): {"function":"subtract","args":[[[2,10]],[1,5]],"expected":[[1,5]]} | on-fail: The parameterized function fails a supplied boundary fixture.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ffa2fc5f4502f2bb4ede63c96a21d9c0c7373e1965d35970eaa79f88eee7c333","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check both the output shape and agreement with the independent row-wise reference.']  remediation→r06
  MEASURES: C:check_broadcast_compatibility_and_intended_shape(f2,f3); C:verify_array_result_with_explicit_tolerances(f4)   anchors=['practice']
  taught-before-tested: C.f2←s11; C.f3←s11; C.f4←s11

### s17 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) The flat fixture and matrix can contain the same values, yet only the matrix has the declared batch/feature axes. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) A smaller cast can meet a byte budget while failing value fidelity; keep the unchanged reference for comparison. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Broadcast-compatible does not mean contract-shaped: the column/row example expands the output. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Consume existing file or object-storage datasets in a format suited to ML access patterns: Next: Consume existing file or object-storage datasets in a format suited to ML access patterns.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Numerical Arrays for ML
(definition) For a two-axis batch/feature contract, check a.ndim == 2 before comparing a.shape[1] with the required feature count. Each shape entry is an axis length. After checking rank, use a.shape[0] to check the batch-length requirement. ⟦A.f2 A.f3 A:tb2 A:tb4 A:tb5⟧
(example) The flat fixture and matrix can contain the same values, yet only the matrix has the declared batch/feature axes. ⟦A.f2 A.f3 A:tb2 A:tb4 A:tb5⟧
[TABLE ds.order_features cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Numerical Arrays for ML
(definition) Import numpy as np, create np.array(fixture) from the supplied list or tuple, and inspect ndim, shape and dtype. Reject an input requirement violation with a conditional raise ValueError(message), rather than continuing with invalid input. Use assert predicate for valid, boundary and failure fixtures. In ordinary non-optimized execution, a false predicate raises AssertionError. ⟦A.f1 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) The flat fixture and matrix can contain the same values, yet only the matrix has the declared batch/feature axes. ⟦A.f1 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.order_features cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r03 · Contrast: Numerical Arrays for ML
(definition) Numerical dtypes have a representable range and bit width; integer and floating candidates may preserve different values. For fixed-width numerical arrays, a.size * a.itemsize equals a.nbytes: element-storage bytes, excluding non-element object overhead. Before accepting lower precision, subtract reference values from cast values. A cast can overflow or lose precision. ⟦B.f1 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) A smaller cast can meet a byte budget while failing value fidelity; keep the unchanged reference for comparison. ⟦B.f1 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.dtype_reference cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r04 · Contrast: Numerical Arrays for ML
(definition) Numerical dtypes have a representable range and bit width; integer and floating candidates may preserve different values. Inspect a.dtype and compare explicit casts made with a.astype(candidate_dtype). For fixed-width numerical arrays, a.size * a.itemsize equals a.nbytes: element-storage bytes, excluding non-element object overhead. Before accepting lower precision, subtract reference values from cast values. A cast can overflow or lose precision. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) A smaller cast can meet a byte budget while failing value fidelity; keep the unchanged reference for comparison. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.dtype_reference cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r05 · Contrast: Numerical Arrays for ML
(definition) NumPy arithmetic can act elementwise on arrays rather than performing one Python operation per observation. ⟦C.f1 C:tb2 C:tb4⟧
(example) Broadcast-compatible does not mean contract-shaped: the column/row example expands the output. ⟦C.f1 C:tb2 C:tb4⟧
[TABLE ds.order_features cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r06 · Contrast: Numerical Arrays for ML
(definition) Broadcasting aligns axes from the right. Aligned lengths must match or one must be 1; missing leading axes count as length 1. Check result shape separately from operand compatibility: compatible broadcasting can expand the result. Compare against a list-comprehension reference with np.testing.assert_allclose(array_result, reference_result, rtol=..., atol=...) using explicit tolerances. ⟦C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
(example) Broadcast-compatible does not mean contract-shaped: the column/row example expands the output. ⟦C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
[TABLE ds.order_features cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: np.array with a dtype argument
· constraints.blocked_syntax: np.broadcast_to(...)
· constraints.blocked_syntax: pandas.read_csv with chunksize

=========

# EVALUATOR PACKET — Ingest and Inspect Model Data / Ingest and Inspect Model Data / Ingest and Inspect Model Data (mle.tile.004_006)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.file_object_ingestion — Consume existing file or object-storage datasets in a format suited to ML access patterns
B = mle.chunked_ingestion — Read model datasets in chunks sized to an array memory budget
C = mle.dataset_inspection — Inspect model-facing dataset structure, distributions and memory footprint

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: mle.tile.004_006.s01: prose block without lineage.fact_ids
  warn: mle.tile.004_006.s07: prose block without lineage.fact_ids
  warn: mle.tile.004_006.s11/ix.mle.tile.004_006.s11: ADVISORY — syntax descriptors with no detector: ['assert', 'assignment', 'del', 'dictionary access', 'floor division', 'for', 'function parameters and calls', 'integer and string literals', 'max', 'multiplication', 'tuple unpacking']
  warn: mle.tile.004_006.s12: prose block without lineage.fact_ids
  warn: mle.tile.004_006.s16/ix.mle.tile.004_006.s16: ADVISORY — syntax descriptors with no detector: ['arithmetic multiplication', 'def with named parameters and defaults', 'dictionary and tuple indexing', 'dictionary literals with string keys', 'function calls with keyword arguments', 'list and tuple literals', 'mlflow imports', 'sklearn imports', 'string, integer and floating-point literals', 'torch imports']

## SOURCE FACTS — A (mle.file_object_ingestion)   objective: Retrieve and inspect an authorized dataset using the declared format and column types.
A.f1: With an authorized Google Cloud Storage client, client.list_blobs(bucket_name, prefix=prefix) iterates existing objects matching the supplied prefix.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/listing-objects — Python]
A.f2: Select the intended object by name and use bucket.blob(object_name).download_to_filename(local_path) to obtain a local dataset file.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/downloading-objects — Python]
A.f3: Read a CSV with pd.read_csv(local_path, dtype=declared_types), and verify its loaded columns, row count and value representations against the expected dataset.   [sources: pandas_user_guide#io.html — CSV & text files; Iteration; Parquet]
A.f4: CSV is a delimited text format, while Parquet is a columnar format whose reader can select columns; choose the supplied format according to the required access pattern.   [sources: pandas_user_guide#io.html — CSV & text files; Iteration; Parquet]
A.f5: Use with open(path, mode, encoding="utf-8") as f for a local text identity record, and use f.read() or f.write(text) within the block.   [sources: python_tutorial#inputoutput.html — Reading and Writing Files]
A.f6: Import the Google Cloud Storage dependency with from google.cloud import storage and construct storage.Client() using the existing authorized runtime identity.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/downloading-objects — Python]
A.f7: Import pandas as pd and apply explicit per-column conversions for the declared types, inspecting the converted values rather than accepting inference as a type guarantee.   [sources: pandas_user_guide#io.html — CSV & text files; Iteration; Parquet]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Ingest and Inspect Model Data.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required imports and a Python ingestion function that uses the existing authorized runtime to list the supplied object-storage prefix, select orders-b.csv by name, download it to the supplied local path, and read it with explicit declared column types. Verify the loaded observations against the supplied expectations, write a local text identity record through an explicit file handle, and explain why CSV fits the stated access pattern and when selected-column Parquet access would fit instead.  SUCCESS: The function retrieves orders-b.csv rather than orders-a.csv, returns the downloaded local path and loaded table, and provides checks of the expected columns, row count, and converted value representations, including the supplied order key example '0012'. The identity record is written inside a UTF-8 open-file block. The format explanation distinguishes delimited text from columnar selected-column access without changing the supplied format arbitrarily.
ASSESSMENT ANCHOR: retrieve_named_object_with_authorized_client facts=['f1', 'f2', 'f6']
ASSESSMENT ANCHOR: read_csv_with_declared_types_and_verify_loaded_observations facts=['f3', 'f7']
ASSESSMENT ANCHOR: match_supplied_format_to_ml_access_pattern facts=['f4']
ASSESSMENT ANCHOR: write_local_identity_record_with_explicit_file_handle facts=['f5']

## SOURCE FACTS — B (mle.chunked_ingestion)   objective: Process a dataset stream in chunks whose numerical allocations fit the declared memory bound.
B.f1: Use pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types) as an iterator of bounded row chunks, and process it with a for loop rather than retaining the entire dataset.   [sources: pandas_user_guide#io.html — CSV & text files; Iteration; Parquet]
B.f2: For a homogeneous fixed-width feature matrix with F columns and element width W bytes, a chunk of R rows requires R × F × W element bytes.   [sources: numpy_user_guide#reference/generated/numpy.ndarray.nbytes.html]
B.f3: Choose chunksize so the chunk matrix fits the stated array budget and verify each materialized chunk; this element estimate is not a guarantee about total reader or process memory.   [sources: pandas_user_guide#io.html — CSV & text files; Iteration; Parquet]
B.f4: Keep the dataset stream open using a with open(...) block while iterating its chunks.   [sources: python_tutorial#inputoutput.html — Reading and Writing Files]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Ingest and Inspect Model Data.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.file_object_ingestion, mle.numpy_dtype_selection, mle.numpy_shape_dtype. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports that reads the supplied order dataset through an open file handle and a pandas chunk iterator. Use the supplied declared_types mapping for the fixture's 20 eight-byte feature columns. Calculate a row limit for the 16,000-byte array budget, materialize and verify each chunk's feature matrix, and return the largest observed per-chunk array byte count without retaining previous chunks.  SUCCESS: The function chooses a row limit of 100, keeps the file open throughout iteration, and checks every materialized matrix, including the final short chunk. It calculates element bytes from actual shape and dtype, confirms agreement with the matrix's nbytes, and verifies that each matrix uses at most 16,000 bytes. It reports the largest observed single-chunk array allocation without claiming a bound on total reader or process memory.
ASSESSMENT ANCHOR: choose_chunk_size_within_array_budget facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_bounded_chunk_iteration facts=['f1', 'f3', 'f4']

## SOURCE FACTS — C (mle.dataset_inspection)   objective: Produce a reproducible dataset-readiness summary of structure, types, memory and feature statistics.
C.f1: Inspect the loaded dataset column names, dtypes and descriptive summaries before declaring it ready for model input.   [sources: pandas_user_guide#basics.html — Descriptive statistics; dtypes]
C.f2: Report the feature matrix shape and dtype, retaining the meaning of each axis rather than only the total number of elements.   [sources: numpy_user_guide#user/absolute_beginners.html — Attributes of an array; How to create a basic array]
C.f3: Report matrix element memory with array.nbytes and distinguish it from total process memory.   [sources: numpy_user_guide#reference/generated/numpy.ndarray.nbytes.html]
C.f4: Return named readiness results as a dictionary from a parameterized inspection function, so callers can check the same fields.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
C.f5: Compute the arithmetic mean with np.mean(numeric_values, axis=0), so each selected numeric feature column is summarized over rows.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
C.f6: Compute standard deviation with np.std(numeric_values, axis=0, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Ingest and Inspect Model Data.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_shape_dtype, mle.numpy_dtype_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required NumPy import and a parameterized inspection function for the supplied loaded two-column dataset. Accept its column names, numeric feature matrix and stated standard-deviation divisor as inputs. Return a readiness dictionary containing column names, column dtypes, feature-wise descriptive summaries, matrix shape with named axis meanings, matrix dtype and element memory cost.  SUCCESS: The function returns consistently named fields for the supplied fixture and another fixture with the same columns. For rows [2, 10], [4, 20] and [6, 30], it reports three observations, two features, means [4, 20], and population standard deviations approximately [1.633, 8.165]. Dtype and element bytes match the supplied array. The dictionary distinguishes element storage from total process memory.
ASSESSMENT ANCHOR: identify_model_input_structure_constraints facts=['f1', 'f2']
ASSESSMENT ANCHOR: interpret_feature_wise_distribution_summaries facts=['f5', 'f6']
ASSESSMENT ANCHOR: distinguish_element_storage_from_process_memory facts=['f2', 'f3']
ASSESSMENT ANCHOR: identify_reusable_named_readiness_evidence facts=['f4']

## DATA ASSETS USED
ds.chunked_orders: Twenty eight-byte feature columns — columns: feature_1(numerical), feature_2(numerical), feature_3(numerical), feature_4(numerical), feature_5(numerical), feature_6(numerical), feature_7(numerical), feature_8(numerical), feature_9(numerical), feature_10(numerical), feature_11(numerical), feature_12(numerical), feature_13(numerical), feature_14(numerical), feature_15(numerical), feature_16(numerical), feature_17(numerical), feature_18(numerical), feature_19(numerical), feature_20(numerical)
   [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0]
   [2.0,4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0,26.0,28.0,30.0,32.0,34.0,36.0,38.0,40.0]
   [3.0,6.0,9.0,12.0,15.0,18.0,21.0,24.0,27.0,30.0,33.0,36.0,39.0,42.0,45.0,48.0,51.0,54.0,57.0,60.0]
   [4.0,8.0,12.0,16.0,20.0,24.0,28.0,32.0,36.0,40.0,44.0,48.0,52.0,56.0,60.0,64.0,68.0,72.0,76.0,80.0]
   [5.0,10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0]
   [6.0,12.0,18.0,24.0,30.0,36.0,42.0,48.0,54.0,60.0,66.0,72.0,78.0,84.0,90.0,96.0,102.0,108.0,114.0,120.0]
   [7.0,14.0,21.0,28.0,35.0,42.0,49.0,56.0,63.0,70.0,77.0,84.0,91.0,98.0,105.0,112.0,119.0,126.0,133.0,140.0]
   [8.0,16.0,24.0,32.0,40.0,48.0,56.0,64.0,72.0,80.0,88.0,96.0,104.0,112.0,120.0,128.0,136.0,144.0,152.0,160.0]
ds.order_features: Three observations with two numerical features — columns: distance(numerical), feature_2(numerical)
   [2,10]
   [4,20]
   [6,30]
   variant one_order: 2 ops; planted: 
   variant wrong_width: 1 ops; planted: 
   variant four_orders: 1 ops; planted: 
   variant empty: 3 ops; planted: 
ds.orders: orders-b.csv — columns: order_key(identifier), distance(numerical), zone(categorical), eventual_arrival(datetime)
   ["0012",2,"north","2025-01-01T09:45:00"]
   ["0013",4,"south","2025-01-01T10:20:00"]
   ["0014",6,"north","2025-01-01T11:31:00"]
   ["0015",0,"south","2025-01-01T12:30:00"]
   ["0016",100,"north","2025-01-01T13:50:00"]
   ["0017",4,"south","2025-01-01T14:10:00"]
   variant missing_distance: 1 ops; planted: missing_distance(missing_value)
   variant duplicate_order: 1 ops; planted: duplicate_order(duplicate_row)
   variant mixed_distance: 1 ops; planted: mixed_distance(wrong_type)
   variant zone_spelling: 1 ops; planted: zone_spelling(inconsistent_category)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Choose leakage-safe train, validation and test splits matching deployment conditions; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compose a fitted preprocessing pipeline reused across training and bounded inference; Control random seeds for reproducible training comparisons; Define measurable model acceptance criteria from task objectives; Derive task-relevant features from prediction-time information; Detect target or preprocessing leakage across training and prediction boundaries; Encode categorical features with an unseen-category policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Fit and predict with a bounded scikit-learn baseline workflow; Fit missing-value imputation using training data only; Identify sampling and selection bias in dataset coverage; Inspect model-facing dataset structure, distributions and memory footprint; Inspect prediction errors for recurring failure modes; Justify classical versus neural modeling using validation quality, latency and cost evidence; Protect sensi

## LESSON, in learner order

### s01 · explainer · Ingest and Inspect Model Data
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(mechanism) An authorized Google Cloud Storage client lists existing prefix-matching objects with client.list_blobs(bucket_name, prefix=prefix). Select the intended name, then download with bucket.blob(object_name).download_to_filename(local_path). Read CSV with pd.read_csv(local_path, dtype=declared_types). Verify columns, row count and value representations against the expected dataset. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) CSV is delimited text. Parquet is columnar and its reader can select columns; use the supplied format that fits the required access pattern. For a local text identity record, use with open(path, mode, encoding="utf-8") as f and read or write inside that block. Import from google.cloud import storage and construct storage.Client() with the existing authorized runtime identity. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[TABLE ds.orders cols=all ] caption: orders-b.csv
[CODE python]
fixture = {'bucket': 'authorized-fixture-bucket',
 'prefix': 'approved/',
 'object_names': ['approved/orders-a.csv', 'approved/orders-b.csv'],
 'intended_object': 'approved/orders-b.csv',
 'local_path': 'orders-b.csv',
 'identity_record_path': 'identity.txt',
 'declared_types': {'order_key': 'string',
                    'distance': 'float64',
                    'zone': 'string',
                    'eventual_arrival': 'string'},
 'expected_columns': ['order_key', 'distance', 'zone', 'eventual_arrival'],
 'expected_row_count': 6,
 'expected_order_key': '0012',
 'access_pattern': 'Read complete named CSV; a separately declared Parquet task would '
                   'allow selected columns.'}

from google.cloud import storage
import pandas as pd

def ingest(contract):
    client = storage.Client()  # existing authorized runtime identity
    names = [blob.name for blob in client.list_blobs(contract["bucket"], prefix=contract["prefix"])]
    print("listed:", names)
    name = contract["intended_object"]
    if name not in names:
        raise ValueError("intended object absent")
    bucket = client.bucket(contract["bucket"])
    bucket.blob(name).download_to_filename(contract["local_path"])
    table = pd.read_csv(contract["local_path"], dtype=contract["declared_types"])
    for column, dtype in contract["declared_types"].items():
        table[column] = table[column].astype(dtype)
    assert list(table.columns) == contract["expected_columns"]
    assert len(table) == contract["expected_row_count"]
    assert table["order_key"].iloc[0] == contract["expected_order_key"]
    identity = f"{name} -> {contract['local_path']}; rows={len(table)}"
    with open(contract["identity_record_path"], "w", encoding="utf-8") as f:
        f.write(identity)
    print(table.dtypes, table["order_key"].tolist(), identity)
    return table

# Review this authorized-runtime ingestion path; no access grant is created here.
# ingest(fixture)
  annotations: []

### s02 · explainer · Apply and verify
Working rule — 
(mechanism) Import pandas as pd. Apply explicit per-column conversions for declared types and inspect converted values; inference is not a type guarantee. ⟦A.f7 A:tb4⟧

### s03 · explainer · A bounded work example
Working rule — 
(example) The approved object listing contains alternatives, but the task names one object. Select that name, download to the declared local path, load with declared types and verify identity, columns and row count. Inspect the converted order key rather than relying on inference. Keep the identity-record write inside its file context. For a separately specified selected-column task, relate Parquet to that access pattern; do not change formats arbitrarily. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧

### s04 · explainer · A distinction to keep
Working rule — 
(misconception) A downloaded file can still be the wrong named object or have the wrong converted key representation. ⟦A.f3 A.f6 A.f7 A:tb6⟧

### s05 · check · Judge the ingest and inspect model data decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] Which snippet correctly writes a local text identity record with an explicit UTF-8 handle?
  ✔ 0: with open(path, "w", encoding="utf-8") as f: f.write(text)
      why: Correct. Reading mode is not the declared writing operation; reading from a write-only handle does not write the record.
  ✘ 1: with open(path, "r", encoding="utf-8") as f: f.write(text)
      why: Reading mode is not the declared writing operation; reading from a write-only handle does not write the record.
  ✘ 2: with open(path, "w", encoding="utf-8") as f: text = f.read()
      why: Reading mode is not the declared writing operation; reading from a write-only handle does not write the record.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check the handle mode and explicit text encoding in each snippet.']  remediation→r01
  MEASURES: A:write_local_identity_record_with_explicit_file_handle(f5)   anchors=[]
  taught-before-tested: A.f5←s01

### s06 · hands_on · Review ingest and inspect model data
Practice — Read the supplied excerpts in this step and decide which satisfy the stated contract and which are defective or unsafe.
QUESTION [classify, core, grading=client] Read each supplied ingestion excerpt and decide whether it meets the named retrieval, loaded-observation, identity-record or format criterion. The runtime identity is already authorized; judge the excerpt, do not run or write ingestion code.
  'from google.cloud import storage
import pandas as pd
def ingest(bucket_name, prefix, object_name, local_path, identity_path, declared_types):
    client = storage.Client()  # supplied authorized runtime identity
    names = [blob.name for blob in client.list_blobs(bucket_name, prefix=prefix)]
    bucket = client.bucket(bucket_name)
    bucket.blob(object_name).download_to_filename(local_path)
    table = pd.read_csv(local_path, dtype=declared_types)
    columns_ok = list(table.columns) == ['order_key', 'distance', 'zone', 'eventual_arrival']
    rows_ok = len(table) == 6
    key_ok = table['order_key'].iloc[0] == '0012'
    inspected = table.dtypes
    with open(identity_path, 'w', encoding='utf-8') as f:
        f.write(object_name + '\n' + local_path)
    return local_path, table, columns_ok, rows_ok, key_ok, inspected
# Supplied call selects 'approved/orders-b.csv', path 'orders-b.csv', declared_types={'order_key': 'string', 'distance': 'float64', 'zone': 'string', 'eventual_arrival': 'string'}
# Format judgement: complete named CSV fits this full-file delimited-text read;
# a separately declared selected-column task would suit columnar Parquet.' -> Meets declared criterion
      feedback: The exact supplied object is selected, explicit types and loaded comparisons are checked, and the identity record is written inside UTF-8 context. The format statement distinguishes complete CSV access from selected-column Parquet.
  '# Intended object: 'approved/orders-b.csv'
object_name = 'approved/orders-a.csv'
bucket.blob(object_name).download_to_filename(local_path)' -> Violates declared criterion
      feedback: Selecting the other prefix object does not retrieve the named dataset.
  'table = pd.read_csv(local_path)
# No dtype or value comparisons: inference is treated as a type guarantee.' -> Violates declared criterion
      feedback: Explicit declared types and inspection of loaded representations are required; inference is not a guarantee.
  'with open(identity_path, 'r', encoding='utf-8') as f:
    f.write(object_name + '\n' + local_path)' -> Violates declared criterion
      feedback: The text record must be written through a writing-mode handle inside the UTF-8 block.
  '# Full named CSV is the supplied format and access pattern.
# Change its suffix to .parquet without converting or changing the supplied format.' -> Violates declared criterion
      feedback: The format must match the supplied file and access pattern; changing a suffix is not selected-column Parquet access.
  feedback✔: You judged each supplied implementation against its named criterion.  feedback✘: Find the exact operation or field that meets or violates the declared criterion.  hints: ['Distinguish retrieving bytes, loading observations and recording file identity.']  remediation→r02
  MEASURES: A:retrieve_named_object_with_authorized_client(f1,f2,f6); A:read_csv_with_declared_types_and_verify_loaded_observations(f3,f7); A:match_supplied_format_to_ml_access_pattern(f4); A:write_local_identity_record_with_explicit_file_handle(f5)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f6←s01; A.f3←s01; A.f7←s02; A.f4←s01; A.f5←s01

### s07 · explainer · Ingest and Inspect Model Data
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦B:tb1⟧
(mechanism) Iterate pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types) with a for loop, processing bounded chunks instead of retaining the whole dataset. A homogeneous fixed-width matrix with R rows, F columns and W bytes per element needs R * F * W element bytes. Choose chunksize within the stated array budget and verify every materialized matrix. This estimate does not bound total reader or process memory. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Keep the dataset stream open with with open(...) throughout chunk iteration. ⟦B.f4 B:tb3⟧
[TABLE ds.chunked_orders cols=all ] caption: Twenty eight-byte feature columns
[CODE python]
fixture = {'path': 'ds.chunked_orders.csv',
 'declared_types': {'feature_1': 'float64',
                    'feature_2': 'float64',
                    'feature_3': 'float64',
                    'feature_4': 'float64',
                    'feature_5': 'float64',
                    'feature_6': 'float64',
                    'feature_7': 'float64',
                    'feature_8': 'float64',
                    'feature_9': 'float64',
                    'feature_10': 'float64',
                    'feature_11': 'float64',
                    'feature_12': 'float64',
                    'feature_13': 'float64',
                    'feature_14': 'float64',
                    'feature_15': 'float64',
                    'feature_16': 'float64',
                    'feature_17': 'float64',
                    'feature_18': 'float64',
                    'feature_19': 'float64',
                    'feature_20': 'float64'},
 'array_budget': 16000,
 'feature_count': 20,
 'element_width': 8}

import pandas as pd
row_limit = fixture["array_budget"] // (fixture["feature_count"] * fixture["element_width"])
maximum = 0
with open(fixture["path"], "r", encoding="utf-8") as stream:
    for chunk in pd.read_csv(stream, chunksize=row_limit, dtype=fixture["declared_types"]):
        matrix = chunk.to_numpy()
        calculated = matrix.shape[0] * matrix.shape[1] * matrix.itemsize
        assert calculated == matrix.nbytes
        assert matrix.nbytes <= fixture["array_budget"]
        maximum = max(maximum, matrix.nbytes)
        print("rows, features, element width, calculated, observed:", *matrix.shape,
              matrix.itemsize, calculated, matrix.nbytes)
        # Process this chunk here; do not append it to a retained collection.
print("maximum working-matrix bytes:", maximum)
  annotations: []

### s08 · explainer · A bounded work example
Working rule — 
(example) Choose a row limit from the supplied feature count, element width and array budget. Keep the file context around the loop and verify each materialized matrix, including the smaller final chunk. Process rather than collect the chunks. The element-byte calculation concerns this homogeneous matrix, not parsing buffers or total process memory. ⟦B.f1 B.f2 B.f3 B.f4 B:tb4⟧

### s09 · explainer · A distinction to keep
Working rule — 
(misconception) One bounded working matrix is not the whole process; collecting every chunk defeats the working-chunk approach. ⟦B.f1 B.f3 B:tb5⟧

### s10 · check · Judge the ingest and inspect model data decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] Which approach supports the declared single-chunk numerical-array budget?
  ✔ 0: Iterate chunks while the file is open, check each matrix and release prior matrices
      why: Correct. Retaining chunks defeats bounded working matrices, and an estimate does not replace checking each allocation.
  ✘ 1: Read once, then retain every materialized chunk in a list
      why: Retaining chunks defeats bounded working matrices, and an estimate does not replace checking each allocation.
  ✘ 2: Use a row-limit estimate and skip all actual nbytes checks
      why: Retaining chunks defeats bounded working matrices, and an estimate does not replace checking each allocation.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Relate the chunk row limit to feature count, element width and the array budget.']  remediation→r03
  MEASURES: B:verify_bounded_chunk_iteration(f1,f3,f4)   anchors=[]
  taught-before-tested: B.f1←s07; B.f3←s07; B.f4←s07

### s11 · hands_on · Verify ingest and inspect model data
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Write the pandas import and inspect_chunks(path, declared_types, array_budget, feature_count, element_width). Calculate row_limit by floor division. Keep the file open while iterating read_csv chunks. For each matrix, including the final short chunk, verify shape-derived element bytes equal nbytes and fit the budget, release it, and retain only the maximum. Assign result to that maximum, not total reader or process memory.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import pandas as pd', 'def', 'function parameters and calls', 'assignment', 'return', 'with open(...) as file_handle', 'pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types)', 'for', 'integer and string literals', 'dictionary access', 'tuple unpacking', 'multiplication', 'floor division', 'comparison operators', 'assert', 'max', 'chunk.to_numpy()', 'matrix.shape', 'matrix.dtype.itemsize', 'matrix.nbytes', 'del'] blocked=11 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'path': 'ds.chunked_orders.csv',
 'declared_types': {'feature_1': 'float64',
                    'feature_2': 'float64',
                    'feature_3': 'float64',
                    'feature_4': 'float64',
                    'feature_5': 'float64',
                    'feature_6': 'float64',
                    'feature_7': 'float64',
                    'feature_8': 'float64',
                    'feature_9': 'float64',
                    'feature_10': 'float64',
                    'feature_11': 'float64',
                    'feature_12': 'float64',
                    'feature_13': 'float64',
                    'feature_14': 'float64',
                    'feature_15': 'float64',
                    'feature_16': 'float64',
                    'feature_17': 'float64',
                    'feature_18': 'float64',
                    'feature_19': 'float64',
                    'feature_20': 'float64'},
 'array_budget': 16000,
 'feature_count': 20,
 'element_width': 8}

path = FIXTURES['path']
declared_types = FIXTURES['declared_types']
array_budget = 16000
feature_count = FIXTURES['feature_count']
element_width = FIXTURES['element_width']

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'path': 'ds.chunked_orders.csv',
 'declared_types': {'feature_1': 'float64',
                    'feature_2': 'float64',
                    'feature_3': 'float64',
                    'feature_4': 'float64',
                    'feature_5': 'float64',
                    'feature_6': 'float64',
                    'feature_7': 'float64',
                    'feature_8': 'float64',
                    'feature_9': 'float64',
                    'feature_10': 'float64',
                    'feature_11': 'float64',
                    'feature_12': 'float64',
                    'feature_13': 'float64',
                    'feature_14': 'float64',
                    'feature_15': 'float64',
                    'feature_16': 'float64',
                    'feature_17': 'float64',
                    'feature_18': 'float64',
                    'feature_19': 'float64',
                    'feature_20': 'float64'},
 'array_budget': 16000,
 'feature_count': 20,
 'element_width': 8}

path = FIXTURES['path']
declared_types = FIXTURES['declared_types']
array_budget = 16000
feature_count = FIXTURES['feature_count']
element_width = FIXTURES['element_width']

import pandas as pd
def inspect_chunks(path, declared_types, array_budget, feature_count, element_width):
    row_limit = array_budget // (feature_count * element_width)
    largest = 0
    with open(path) as file_handle:
        for chunk in pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types):
            matrix = chunk.to_numpy()
            rows, columns = matrix.shape
            calculated = rows * columns * matrix.dtype.itemsize
            assert columns == feature_count
            assert calculated == matrix.nbytes
            assert calculated <= array_budget
            largest = max(largest, calculated)
            del matrix
    return largest
result = inspect_chunks(path, declared_types, array_budget, feature_count, element_width)

  test budget0 (function_call, visible=True): {"function":"inspect_chunks","args":["ds.chunked_orders.csv",{"feature_1":"float64","feature_2":"float64","feature_3":"float64","feature_4":"float64","feature_5":"float64","feature_6":"float64","feature_7":"float64","feature_8":"float64","feature_9":"float64","feature_10":"float64","feature_11":"float64","feature_12":"float64","feature_13":"float64","feature_14":"float64","feature_15":"float64","feature_16":"float64","feature_17":"float64","feature_18":"float64","feature_19":"float64","feature_2 | on-fail: The maximum actual chunk element allocation does not match this budget.
  test budget1 (function_call, visible=False): {"function":"inspect_chunks","args":["ds.chunked_orders.csv",{"feature_1":"float64","feature_2":"float64","feature_3":"float64","feature_4":"float64","feature_5":"float64","feature_6":"float64","feature_7":"float64","feature_8":"float64","feature_9":"float64","feature_10":"float64","feature_11":"float64","feature_12":"float64","feature_13":"float64","feature_14":"float64","feature_15":"float64","feature_16":"float64","feature_17":"float64","feature_18":"float64","feature_19":"float64","feature_2 | on-fail: The maximum actual chunk element allocation does not match this budget.
  test short_whole_file (function_call, visible=False): {"function":"inspect_chunks","args":["ds.chunked_orders.csv",{"feature_1":"float64","feature_2":"float64","feature_3":"float64","feature_4":"float64","feature_5":"float64","feature_6":"float64","feature_7":"float64","feature_8":"float64","feature_9":"float64","feature_10":"float64","feature_11":"float64","feature_12":"float64","feature_13":"float64","feature_14":"float64","feature_15":"float64","feature_16":"float64","feature_17":"float64","feature_18":"float64","feature_19":"float64","feature_2 | on-fail: The maximum actual chunk element allocation does not match this budget.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"dc1e74c92286f72cb6e50ed3ac28b511d92c0029917155ecbbc58c77e91166b3","tests_passed":3}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check each chunk, including the final short one, before retaining the maximum byte count.']  remediation→r04
  MEASURES: B:choose_chunk_size_within_array_budget(f2,f3); B:verify_bounded_chunk_iteration(f1,f3,f4)   anchors=['practice']
  taught-before-tested: B.f2←s07; B.f3←s07; B.f1←s07; B.f3←s07; B.f4←s07

### s12 · explainer · Ingest and Inspect Model Data
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦C:tb1⟧
(mechanism) Inspect loaded columns, dtypes and descriptive summaries before declaring model-input readiness. Report matrix shape and dtype with each axis meaning, not just total element count. Use array.nbytes for matrix element memory, distinguishing it from total process memory. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Return named readiness fields in a dictionary from a parameterized inspection function so callers can check consistent fields. Use np.mean(numeric_values, axis=0) to average each selected numeric feature over rows. Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root. Use ddof=1 only when the stated calculation requires N-1. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[TABLE ds.order_features cols=all ] caption: Three observations with two numerical features
[CODE python]
fixture = {'fixture': {'columns': ['distance', 'feature_2'], 'rows': [[2, 10], [4, 20], [6, 30]]},
 'feature_columns': ['distance', 'feature_2'],
 'ddof': 0,
 'boundary': {'columns': ['distance', 'feature_2'], 'rows': [[2, 10]]}}

import numpy as np
import pandas as pd

def inspect(table, feature_columns, ddof):
    matrix = table[feature_columns].to_numpy()
    return {"columns": list(table.columns), "dtypes": table.dtypes.astype(str).to_dict(),
            "descriptive": table.describe().to_dict(), "observation_count": matrix.shape[0],
            "feature_count": matrix.shape[1], "shape": matrix.shape, "dtype": str(matrix.dtype),
            "element_bytes": matrix.nbytes, "mean": np.mean(matrix, axis=0),
            "std": np.std(matrix, axis=0, ddof=ddof), "ddof": ddof}

for name in ("fixture", "boundary"):
    spec = fixture[name]
    table = pd.DataFrame(spec["rows"], columns=spec["columns"])
    readiness = inspect(table, fixture["feature_columns"], fixture["ddof"])
    assert readiness["feature_count"] == len(fixture["feature_columns"])
    print(name, readiness)
  annotations: []

### s13 · explainer · A bounded work example
Working rule — 
(example) Inspect the supplied order-feature table and return a named dictionary. Keep observation and feature axis meanings beside shape and dtype. Compute feature-wise mean and population standard deviation over rows, retaining the specified divisor. Report observed nbytes as element storage, not total process memory. A parameterized function lets another caller inspect the same named fields for a different fixture. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb4⟧

### s14 · explainer · A distinction to keep
Working rule — 
(misconception) Total element count omits axis meanings; nbytes omits other process memory. ⟦C.f2 C.f6 C:tb5⟧

### s15 · check · Judge the ingest and inspect model data decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] Which readiness evidence retains the structure needed to interpret model input?
  ✔ 0: Column names and dtypes plus shape with observation/feature axis meanings
      why: Correct. Neither element count nor element bytes identifies columns and axis meanings.
  ✘ 1: Only the total element count
      why: Neither element count nor element bytes identifies columns and axis meanings.
  ✘ 2: Only the matrix nbytes
      why: Neither element count nor element bytes identifies columns and axis meanings.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Separate input structure and category roles from numerical summaries.']  remediation→r05
  MEASURES: C:identify_model_input_structure_constraints(f1,f2)   anchors=[]
  taught-before-tested: C.f1←s12; C.f2←s12

### s16 · hands_on · Verify ingest and inspect model data
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, stretch, grading=client] Implement inspect(columns, rows, ddof=0) with a NumPy import. Return these named readiness fields: columns, column_dtypes (both selected numerical columns), means, stds (columnwise), shape, axes [observations, features], dtype, element_bytes and memory_scope. Assign result for the supplied inputs. Describe memory_scope as array elements only, not total process memory. Accept the same columns with a one-row fixture too. Construct the matrix with np.array(rows), without selecting or casting its dtype. Return column_dtypes as a two-item list of NumPy dtype objects and dtype as the matrix’s NumPy dtype object. Use the exact memory_scope string 'array elements only, not total process memory'.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'def with named parameters and defaults', 'return', 'variable assignment', 'dictionary literals with string keys', 'list and tuple literals', 'string, integer and floating-point literals', 'dictionary and tuple indexing', 'function calls with keyword arguments', 'np.array', 'np.mean(numeric_values, axis=0)', 'np.std(numeric_values, axis=0, ddof=0)', 'np.std(numeric_values, axis=0, ddof=1)', 'numeric_values.shape', 'numeric_values.dtype', 'numeric_values.dtype.itemsize', 'numeric_values.nbytes', 'arithmetic multiplication'] blocked=10 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'fixture': {'columns': ['distance', 'feature_2'],
             'rows': [[2, 10], [4, 20], [6, 30]]},
 'feature_columns': ['distance', 'feature_2'],
 'ddof': 0,
 'boundary': {'columns': ['distance', 'feature_2'], 'rows': [[2, 10]]}}

columns = FIXTURES['feature_columns']
rows = FIXTURES['fixture']['rows']
ddof = FIXTURES['ddof']

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'fixture': {'columns': ['distance', 'feature_2'],
             'rows': [[2, 10], [4, 20], [6, 30]]},
 'feature_columns': ['distance', 'feature_2'],
 'ddof': 0,
 'boundary': {'columns': ['distance', 'feature_2'], 'rows': [[2, 10]]}}

columns = FIXTURES['feature_columns']
rows = FIXTURES['fixture']['rows']
ddof = FIXTURES['ddof']

import numpy as np
def inspect(columns, rows, ddof=0):
    numeric_values = np.array(rows)
    shape = numeric_values.shape
    return {'columns':columns,'column_dtypes':[numeric_values.dtype, numeric_values.dtype], 'means':np.mean(numeric_values,axis=0),'stds':np.std(numeric_values,axis=0,ddof=ddof),'shape':shape,'axes':['observations','features'],'dtype':numeric_values.dtype,'element_bytes':numeric_values.nbytes,'memory_scope':'array elements only, not total process memory'}
result = inspect(columns, rows, ddof)

  test call0 (function_call, visible=False): {"function":"inspect","args":[["distance","feature_2"],[[2,10],[4,20],[6,30]]],"expected":{"columns":["distance","feature_2"],"column_dtypes":["dtype('int32')","dtype('int32')"],"means":[4,20],"stds":[1.632993161855452,8.16496580927726],"shape":[3,2],"axes":["observations","features"],"dtype":"dtype('int32')","element_bytes":24,"memory_scope":"array elements only, not total process memory"}} | on-fail: The parameterized function fails a supplied boundary fixture.
  test call1 (function_call, visible=False): {"function":"inspect","args":[["distance","feature_2"],[[2,10]]],"expected":{"columns":["distance","feature_2"],"column_dtypes":["dtype('int32')","dtype('int32')"],"means":[2,10],"stds":[0,0],"shape":[1,2],"axes":["observations","features"],"dtype":"dtype('int32')","element_bytes":8,"memory_scope":"array elements only, not total process memory"}} | on-fail: The parameterized function fails a supplied boundary fixture.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9c544dcb931f8ab46374eafec248cc57bc8f41ea8f8fad8b9e27a32b925695b8","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Inspect the selected columns before constructing the matrix; compute summaries columnwise.']  remediation→r06
  MEASURES: C:interpret_feature_wise_distribution_summaries(f5,f6); C:distinguish_element_storage_from_process_memory(f2,f3); C:identify_reusable_named_readiness_evidence(f4)   anchors=['practice']
  taught-before-tested: C.f5←s12; C.f6←s12; C.f2←s12; C.f3←s12; C.f4←s12

### s17 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) A downloaded file can still be the wrong named object or have the wrong converted key representation. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(takeaway) One bounded working matrix is not the whole process; collecting every chunk defeats the working-chunk approach. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) Total element count omits axis meanings; nbytes omits other process memory. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Validate dataset schema constraints before training: Next: Validate dataset schema constraints before training.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Ingest and Inspect Model Data
(definition) For a local text identity record, use with open(path, mode, encoding="utf-8") as f and read or write inside that block. ⟦A.f5 A:tb3 A:tb5⟧
(example) A downloaded file can still be the wrong named object or have the wrong converted key representation. ⟦A.f5 A:tb3 A:tb5⟧
[TABLE ds.orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Ingest and Inspect Model Data
(definition) An authorized Google Cloud Storage client lists existing prefix-matching objects with client.list_blobs(bucket_name, prefix=prefix). Select the intended name, then download with bucket.blob(object_name).download_to_filename(local_path). Read CSV with pd.read_csv(local_path, dtype=declared_types). Verify columns, row count and value representations against the expected dataset. CSV is delimited text. Parquet is columnar and its reader can select columns; use the supplied format that fits the required access pattern. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(definition) For a local text identity record, use with open(path, mode, encoding="utf-8") as f and read or write inside that block. Import from google.cloud import storage and construct storage.Client() with the existing authorized runtime identity. Import pandas as pd. Apply explicit per-column conversions for declared types and inspect converted values; inference is not a type guarantee. ⟦A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
(example) A downloaded file can still be the wrong named object or have the wrong converted key representation. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6⟧
[TABLE ds.orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r03 · Contrast: Ingest and Inspect Model Data
(definition) Iterate pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types) with a for loop, processing bounded chunks instead of retaining the whole dataset. Choose chunksize within the stated array budget and verify every materialized matrix. This estimate does not bound total reader or process memory. Keep the dataset stream open with with open(...) throughout chunk iteration. ⟦B.f1 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) One bounded working matrix is not the whole process; collecting every chunk defeats the working-chunk approach. ⟦B.f1 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.chunked_orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r04 · Contrast: Ingest and Inspect Model Data
(definition) Iterate pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types) with a for loop, processing bounded chunks instead of retaining the whole dataset. A homogeneous fixed-width matrix with R rows, F columns and W bytes per element needs R * F * W element bytes. Choose chunksize within the stated array budget and verify every materialized matrix. This estimate does not bound total reader or process memory. Keep the dataset stream open with with open(...) throughout chunk iteration. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) One bounded working matrix is not the whole process; collecting every chunk defeats the working-chunk approach. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.chunked_orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r05 · Contrast: Ingest and Inspect Model Data
(definition) Inspect loaded columns, dtypes and descriptive summaries before declaring model-input readiness. Report matrix shape and dtype with each axis meaning, not just total element count. ⟦C.f1 C.f2 C:tb2 C:tb4 C:tb5⟧
(example) Total element count omits axis meanings; nbytes omits other process memory. ⟦C.f1 C.f2 C:tb2 C:tb4 C:tb5⟧
[TABLE ds.order_features cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r06 · Contrast: Ingest and Inspect Model Data
(definition) Report matrix shape and dtype with each axis meaning, not just total element count. Use array.nbytes for matrix element memory, distinguishing it from total process memory. Return named readiness fields in a dictionary from a parameterized inspection function so callers can check consistent fields. Use np.mean(numeric_values, axis=0) to average each selected numeric feature over rows. ⟦C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3 C:tb4 C:tb5⟧
(definition) Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root. Use ddof=1 only when the stated calculation requires N-1. ⟦C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
(example) Total element count omits axis meanings; nbytes omits other process memory. ⟦C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
[TABLE ds.order_features cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: DataFrame.describe()
· constraints.blocked_syntax: DataFrame.drop_duplicates()

=========

# EVALUATOR PACKET — Validate and Clean Datasets / Validate and Clean Datasets (mle.tile.007_008)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.dataset_schema_validation — Validate dataset schema constraints before training
B = mle.dataset_cleaning_policy — Resolve duplicate and invalid observations with a documented cleaning policy

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: mle.tile.007_008.s01: prose block without lineage.fact_ids
  warn: mle.tile.007_008.s05/ix.mle.tile.007_008.s05: ADVISORY — syntax descriptors with no detector: ['assert predicate statements', 'comparison operators and boolean operators', 'def statements, parameters, and return statements', 'dictionary, list, set, string, and numeric literals', 'elementwise boolean predicates combined with &', 'for loops', 'if statements', 'raise ValueError with a descriptive message', 'set equality and dtype comparisons', 'sklearn preprocessing and pipeline APIs', 'try and except ValueError', 'variable assignment and function calls']
  warn: mle.tile.007_008.s06: prose block without lineage.fact_ids
  warn: mle.tile.007_008.s10/ix.mle.tile.007_008.s10: ADVISORY — syntax descriptors with no detector: ['and, or and not', 'assert predicate', 'def with parameters and return', 'dictionary item assignment', 'dictionary key lookup', 'for loops', 'if, elif and else', 'import and from ... import for required supplied dependencies', 'in and not in membership tests', 'list and dictionary literals', 'local variable assignment', 'string and numeric literals']

## SOURCE FACTS — A (mle.dataset_schema_validation)   objective: Implement and test a dataset column, type and value contract.
A.f1: A dataset schema declares expected features and their permitted representations or values; absent, unexpected or invalid features are schema violations.   [sources: google_mlops_pipelines#Data and model validation]
A.f2: Compare table.columns and table.dtypes with the declared column/type contract before checking each constrained column.   [sources: pandas_user_guide#basics.html — Descriptive statistics; dtypes]
A.f3: Implement value constraints as boolean predicates and raise an explicit validation exception when a required column, type or value boundary fails.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
A.f4: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Validate and Clean Datasets.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.dataset_inspection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Within supplied runtime scaffolding, write the required pandas import and a reusable Python validation function for a table containing exactly distance and zone. Use a supplied explicit contract for both column types and the permitted zone representation, with distance constrained to 0 through 100 inclusive. Check columns and dtypes before value predicates, raise descriptive validation exceptions on failures, and author reusable fixtures and assertions for valid input, both inclusive boundaries, missing or unexpected columns, incorrect types, and out-of-range values.  SUCCESS: The learner-written function accepts valid tables and distance values of 0 and 100, rejects each declared column, type, and value violation with an identifiable validation exception, and passes learner-written assertions confirming acceptance and rejection without changing the input.
ASSESSMENT ANCHOR: detect_column_and_type_contract_violations facts=['f1', 'f2']
ASSESSMENT ANCHOR: detect_value_boundary_violations facts=['f3']
ASSESSMENT ANCHOR: distinguish_validation_exceptions_from_fixture_assertions facts=['f3', 'f4']

## SOURCE FACTS — B (mle.dataset_cleaning_policy)   objective: Apply an explicit retain, repair or reject policy to repeated and invalid observations.
B.f1: Use a set of accepted observation keys to test whether a key has already been seen before adding the next accepted key.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f2: Use a policy dictionary to choose the declared retain, repair or reject action for each detected invalid or repeated observation.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f3: Inspect and clean example data as needed, making representations consistent with its intended training use.   [sources: sagemaker_developer_guide#how-it-works-mlconcepts.html — The machine learning workflow]
B.f4: Implement the declared action with conditional branches and report the affected observation IDs, instead of silently altering the dataset.   [sources: python_tutorial#errors.html — Handling Exceptions; Raising Exceptions]
B.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Validate and Clean Datasets.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.dataset_schema_validation, mle.dataset_inspection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function that cleans supplied order observations under the stated validity policy within existing infrastructure scaffolding. Write imports for required supplied dependencies. Use an accepted-key set, a policy dictionary and conditional branches to retain valid observations, resolve repeated accepted keys, repair the approved zone spelling and reject invalid distances as declared. Return cleaned observations and a report of affected observation IDs and actions. Author assertions for valid, boundary, repair, rejection and repeated-key cases.  SUCCESS: The resulting observations match the supplied policy, accepted keys are added only after acceptance, and every affected observation ID is reported with its declared action. Assertions verify expected repaired values, retained valid and boundary observations, and exclusion of rejected observations and prohibited repeats. A deliberately false assertion raises AssertionError during ordinary non-optimized execution.
ASSESSMENT ANCHOR: apply_declared_duplicate_resolution_policy facts=['f1', 'f2']
ASSESSMENT ANCHOR: resolve_invalid_observations_and_report_actions facts=['f2', 'f3', 'f4']
ASSESSMENT ANCHOR: verify_cleaning_policy_with_assert_predicates facts=['f5']

## DATA ASSETS USED
ds.cleaning_orders: Policy-driven accepted-order cleaning — columns: observation_id(identifier), order_key(identifier), distance(numerical), zone(categorical)
   ["obs_A","A",2,"north"]
   ["obs_B","B",4,"south"]
   ["obs_C","C",0,"north"]
   ["obs_D","D",100,"south"]
   variant policy_defects: 4 ops; planted: repeated_key(other); spelling(inconsistent_category); invalid_distance(impossible_value)
ds.distance_zone: Exact distance/zone schema — columns: distance(numerical), zone(categorical)
   [0,"north"]
   [2,"south"]
   [100,"north"]
   variant negative_distance: 1 ops; planted: negative_distance(impossible_value)
   variant over_upper_bound: 1 ops; planted: over_upper_bound(impossible_value)
   variant missing_zone_column: 1 ops; planted: 
   variant invalid_zone: 1 ops; planted: invalid_zone(inconsistent_category)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Choose leakage-safe train, validation and test splits matching deployment conditions; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compose a fitted preprocessing pipeline reused across training and bounded inference; Control random seeds for reproducible training comparisons; Define measurable model acceptance criteria from task objectives; Derive task-relevant features from prediction-time information; Detect target or preprocessing leakage across training and prediction boundaries; Document model limitations and foreseeable misuse under an existing risk policy; Encode categorical features with an unseen-category policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Fit and predict with a bounded scikit-learn baseline workflow; Fit missing-value imputation using training data only; Identify sampling and selection bias in dataset coverage; Inspect prediction errors for recurring failure modes; Justify classical versus neural modeling using validation quality, latency and cost evidence; Protect 

## LESSON, in learner order

### s01 · explainer · Validate and Clean Datasets
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(definition) A schema specifies expected features and permitted representations or values. Missing, unexpected and invalid features violate it. Compare table.columns and table.dtypes to the declared contract before checking constrained columns. Express value constraints as boolean predicates. Raise an explicit validation exception for a failed required column, type or value boundary. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f4 A:tb3⟧
[TABLE ds.distance_zone cols=all ] caption: Exact distance/zone schema
[CODE python]
fixture = {'contract': {'columns': ['distance', 'zone'],
              'declared_types': {'distance': 'float64', 'zone': 'string'},
              'distance_min': 0,
              'distance_max': 100,
              'zone_categories': ['north', 'south']},
 'valid': {'columns': ['distance', 'zone'],
           'rows': [[0, 'north'], [2, 'south'], [100, 'north']]},
 'negative': {'columns': ['distance', 'zone'],
              'rows': [[-1, 'north'], [2, 'south'], [100, 'north']]},
 'too_large': {'columns': ['distance', 'zone'],
               'rows': [[0, 'north'], [2, 'south'], [101, 'north']]},
 'missing_column': {'columns': ['distance'], 'rows': [[0], [2], [100]]},
 'invalid_representation': {'columns': ['distance', 'zone'],
                            'rows': [[0, 'NORTH'], [2, 'south'], [100, 'north']]},
 'unexpected_column': {'columns': ['distance', 'zone', 'extra_feature'],
                       'rows': [[0, 'north', 10], [2, 'south', 10], [100, 'north', 10]]}}

import pandas as pd

def validate(table, contract):
    if set(table.columns) != set(contract["columns"]):
        raise ValueError("column contract violated")
    for name, dtype in contract["declared_types"].items():
        if str(table[name].dtype) != dtype:
            raise ValueError("dtype contract violated")
    valid_distance = table["distance"].between(contract["distance_min"], contract["distance_max"])
    valid_zone = table["zone"].isin(contract["zone_categories"])
    print("predicates:", valid_distance.tolist(), valid_zone.tolist())
    if not valid_distance.all() or not valid_zone.all():
        raise ValueError("value contract violated")
    return True

for name in ("valid", "negative", "too_large", "unexpected_column", "missing_column", "invalid_representation"):
    spec = fixture[name]
    table = pd.DataFrame(spec["rows"], columns=spec["columns"])
    table = table.astype({c:d for c,d in fixture["contract"]["declared_types"].items() if c in table})
    print(name, list(table.columns), table.dtypes)
    try:
        assert validate(table, fixture["contract"])
        print("accepted")
    except ValueError as error:
        print(str(error))
  annotations: []

### s02 · explainer · A bounded work example
Working rule — 
(example) Compare the distance/zone column set and declared dtypes first. Then check the inclusive distance bounds and permitted zone representation. A lower-bound row is a boundary fixture; an out-of-range row is a value failure. An unexpected feature is a structural failure even if its values look plausible. Use explicit exceptions for rejection and assertions to exercise the supplied fixtures. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · A distinction to keep
Working rule — 
(misconception) A loaded table can violate structure or value bounds; explicit exceptions reject it, while assertions exercise fixtures. ⟦A.f3 A.f4 A:tb5⟧

### s04 · check · Judge the validate and clean datasets decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] A required input boundary fails. Which action implements validation rather than a fixture-only assertion?
  ✔ 0: Conditionally raise a descriptive ValueError
      why: Correct. A conditional exception enforces input rejection; continuing accepts invalid data and assert is a fixture predicate that can be disabled by optimization.
  ✘ 1: Continue with the invalid input
      why: A conditional exception enforces input rejection; continuing accepts invalid data and assert is a fixture predicate that can be disabled by optimization.
  ✘ 2: Use only assert and call that the production rejection boundary
      why: A conditional exception enforces input rejection; continuing accepts invalid data and assert is a fixture predicate that can be disabled by optimization.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Distinguish a runtime rejection rule from an assertion about a supplied fixture.']  remediation→r01
  MEASURES: A:distinguish_validation_exceptions_from_fixture_assertions(f3,f4)   anchors=[]
  taught-before-tested: A.f3←s01; A.f4←s01

### s05 · hands_on · Verify validate and clean datasets
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Implement validate(table, contract) without altering the table. Check exactly the declared columns and dtypes before inclusive distance bounds and lowercase north/south predicates. Raise descriptive ValueError on each violation and return accepted table as result. Author assertions for both endpoints and every supplied failure fixture, including a wrong distance dtype. The provided rejected helper only catches ValueError.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', 'def statements, parameters, and return statements', 'if statements', 'for loops', 'dictionary, list, set, string, and numeric literals', 'variable assignment and function calls', 'pd.DataFrame construction with explicit column dtypes', 'table.columns and table.dtypes', 'column selection with table[column_name]', 'set equality and dtype comparisons', 'comparison operators and boolean operators', 'elementwise boolean predicates combined with &', 'Series.all()', 'raise ValueError with a descriptive message', 'try and except ValueError', 'assert predicate statements'] blocked=6 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'contract': {'columns': ['distance', 'zone'],
              'declared_types': {'distance': 'float64', 'zone': 'string'},
              'distance_min': 0,
              'distance_max': 100,
              'zone_categories': ['north', 'south']},
 'valid': {'columns': ['distance', 'zone'],
           'rows': [[0, 'north'], [2, 'south'], [100, 'north']]},
 'negative': {'columns': ['distance', 'zone'],
              'rows': [[-1, 'north'], [2, 'south'], [100, 'north']]},
 'too_large': {'columns': ['distance', 'zone'],
               'rows': [[0, 'north'], [2, 'south'], [101, 'north']]},
 'missing_column': {'columns': ['distance'], 'rows': [[0], [2], [100]]},
 'invalid_representation': {'columns': ['distance', 'zone'],
                            'rows': [[0, 'NORTH'],
                                     [2, 'south'],
                                     [100, 'north']]},
 'unexpected_column': {'columns': ['distance', 'zone', 'extra_feature'],
                       'rows': [[0, 'north', 10],
                                [2, 'south', 10],
                                [100, 'north', 10]]}}

import pandas as pd
contract = FIXTURES['contract']
# Fixture construction and test drivers are provided; validation is your task.
def make(case):
    table = pd.DataFrame(case['rows'], columns=case['columns'])
    for name in case['columns']:
        if name in contract['declared_types']:
            table[name] = table[name].astype(contract['declared_types'][name])
    return table
def rejected(table):
    try:
        validate(table, contract)
    except ValueError:
        return True
    return False
valid = make(FIXTURES['valid'])

def validate_fixture(case):
    return validate(make(case), contract)
wrong_type = valid.copy()
wrong_type['distance'] = wrong_type['distance'].astype('string')
# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'contract': {'columns': ['distance', 'zone'],
              'declared_types': {'distance': 'float64', 'zone': 'string'},
              'distance_min': 0,
              'distance_max': 100,
              'zone_categories': ['north', 'south']},
 'valid': {'columns': ['distance', 'zone'],
           'rows': [[0, 'north'], [2, 'south'], [100, 'north']]},
 'negative': {'columns': ['distance', 'zone'],
              'rows': [[-1, 'north'], [2, 'south'], [100, 'north']]},
 'too_large': {'columns': ['distance', 'zone'],
               'rows': [[0, 'north'], [2, 'south'], [101, 'north']]},
 'missing_column': {'columns': ['distance'], 'rows': [[0], [2], [100]]},
 'invalid_representation': {'columns': ['distance', 'zone'],
                            'rows': [[0, 'NORTH'],
                                     [2, 'south'],
                                     [100, 'north']]},
 'unexpected_column': {'columns': ['distance', 'zone', 'extra_feature'],
                       'rows': [[0, 'north', 10],
                                [2, 'south', 10],
                                [100, 'north', 10]]}}

import pandas as pd
contract = FIXTURES['contract']
# Fixture construction and test drivers are provided; validation is your task.
def make(case):
    table = pd.DataFrame(case['rows'], columns=case['columns'])
    for name in case['columns']:
        if name in contract['declared_types']:
            table[name] = table[name].astype(contract['declared_types'][name])
    return table
def rejected(table):
    try:
        validate(table, contract)
    except ValueError:
        return True
    return False
valid = make(FIXTURES['valid'])
def validate_fixture(case):
    return validate(make(case), contract)
wrong_type = valid.copy()
wrong_type['distance'] = wrong_type['distance'].astype('string')

def validate(table, contract):
    if set(table.columns) != set(contract['columns']):
        raise ValueError('columns violate contract')
    for name in contract['columns']:
        if table.dtypes[name] != contract['declared_types'][name]:
            raise ValueError('dtype violates contract')
    distance_ok = (table['distance'] >= contract['distance_min']) & (table['distance'] <= contract['distance_max'])
    zone_ok = (table['zone'] == 'north') | (table['zone'] == 'south')
    if not distance_ok.all():
        raise ValueError('distance violates inclusive boundary')
    if not zone_ok.all():
        raise ValueError('zone violates representation')
    return table
result = validate(valid, contract)
assert result['distance'][0] == contract['distance_min']
assert result['distance'][2] == contract['distance_max']
assert rejected(make(FIXTURES['negative']))
assert rejected(make(FIXTURES['too_large']))
assert rejected(make(FIXTURES['missing_column']))
assert rejected(make(FIXTURES['unexpected_column']))
assert rejected(make(FIXTURES['invalid_representation']))
assert rejected(wrong_type)

  test case0 (function_call, visible=True): {"function":"validate_fixture","args":[{"columns":["distance","zone"],"rows":[[0,"north"],[2,"south"],[100,"north"]]}],"expected":{"columns":["distance","zone"],"rows":[[0,"north"],[2,"south"],[100,"north"]]}} | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"validate_fixture","args":[{"columns":["distance","zone"],"rows":[[2,"south"]]}],"expected":{"columns":["distance","zone"],"rows":[[2,"south"]]}} | on-fail: This fixture does not satisfy the declared return contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"7258ba382422d7db55c152cfaaf24aa4f257c0a43e2b539a89cfa3b0825684fb","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check columns and dtypes before applying value predicates; include both endpoints.']  remediation→r02
  MEASURES: A:detect_column_and_type_contract_violations(f1,f2); A:detect_value_boundary_violations(f3); A:distinguish_validation_exceptions_from_fixture_assertions(f3,f4)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f3←s01; A.f4←s01

### s06 · explainer · Validate and Clean Datasets
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦B:tb1⟧
(mechanism) Track accepted observation keys in a set; check membership before adding the next accepted key. Choose the declared retain, repair or reject action from a policy dictionary for each invalid or repeated observation. Inspect and clean examples as needed, making representations consistent with their intended training use. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Implement policy actions with conditional branches and report affected observation IDs rather than changing data silently. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.cleaning_orders cols=all ] caption: Valid reference dataset; the walkthrough processes the policy_defects variant.
[CODE python]
fixture = {'records': [{'observation_id': 'obs_A',
              'order_key': 'A',
              'distance': 2,
              'zone': 'north'},
             {'observation_id': 'obs_B',
              'order_key': 'B',
              'distance': 4,
              'zone': 'South'},
             {'observation_id': 'obs_C',
              'order_key': 'C',
              'distance': 0,
              'zone': 'north'},
             {'observation_id': 'obs_D',
              'order_key': 'D',
              'distance': -1,
              'zone': 'south'},
             {'observation_id': 'obs_A_repeat',
              'order_key': 'A',
              'distance': 2,
              'zone': 'north'}],
 'valid': [{'observation_id': 'obs_A', 'order_key': 'A', 'distance': 2, 'zone': 'north'},
           {'observation_id': 'obs_B', 'order_key': 'B', 'distance': 4, 'zone': 'south'},
           {'observation_id': 'obs_C', 'order_key': 'C', 'distance': 0, 'zone': 'north'},
           {'observation_id': 'obs_D',
            'order_key': 'D',
            'distance': 100,
            'zone': 'south'}],
 'policy': {'repeat_accepted_key': 'reject',
            'zone_repairs': {'South': 'south'},
            'distance_min': 0,
            'distance_max': 100,
            'invalid_distance': 'reject'},
 'connection': 'authorized local fixture only'}

accepted_keys = set()
accepted = []
affected = []
policy = fixture["policy"]
for original in fixture["records"]:
    row = dict(original)
    before = sorted(accepted_keys)
    action = "retain"
    if row["order_key"] in accepted_keys:
        action = policy["repeat_accepted_key"]
    elif not policy["distance_min"] <= row["distance"] <= policy["distance_max"]:
        action = policy["invalid_distance"]
    elif row["zone"] in policy["zone_repairs"]:
        action = "repair"
        row["zone"] = policy["zone_repairs"][row["zone"]]
    if action != "retain":
        affected.append({"observation_id": row["observation_id"], "action": action})
    if action != "reject":
        accepted.append(row)
        accepted_keys.add(row["order_key"])
    print(before, row["observation_id"], action, sorted(accepted_keys))
assert len(accepted_keys) == len(accepted)
print("result:", accepted, "affected:", affected)
  annotations: []

### s07 · explainer · A bounded work example
Working rule — 
(example) Check the accepted-key set before accepting another observation. Apply the supplied repeat-key rejection and approved zone-spelling repair through the policy dictionary, recording affected IDs. A different defect may require rejection rather than repair. These are this dataset's approved actions, not a universal deduplication rule; test normal, boundary and repeated-key cases. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s08 · explainer · A distinction to keep
Working rule — 
(misconception) An approved spelling repair does not authorize silently repairing every defect; report each policy action and affected ID. ⟦B.f2 B.f4 B:tb5⟧

### s09 · check · Judge the validate and clean datasets decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] In ordinary non-optimized execution, what happens to a deliberately false cleaning-policy assertion?
  ✔ 0: It raises AssertionError
      why: Correct. Assertions verify predicates; they neither repair data nor rewrite policy.
  ✘ 1: It silently repairs the data
      why: Assertions verify predicates; they neither repair data nor rewrite policy.
  ✘ 2: It changes the declared policy to retain the row
      why: Assertions verify predicates; they neither repair data nor rewrite policy.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Evaluate the predicate first, then consider what assert does when it is false.']  remediation→r03
  MEASURES: B:verify_cleaning_policy_with_assert_predicates(f5)   anchors=[]
  taught-before-tested: B.f5←s06

### s10 · hands_on · Verify validate and clean datasets
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, stretch, grading=client] Implement clean(records, policy). Return {'cleaned': cleaned, 'report': report}. Preserve input order in cleaned and report. Each report entry is {'observation_id': the affected ID, 'action': the declared action}; do not report unchanged retained observations. Track only accepted keys; apply policy repeat rejection, inclusive distance bounds, and approved zone repair without mutating inputs. Report each affected observation_id and action. Assign result; author assertions for repairs, rejection, repeats and both boundaries using the records and valid fixtures. A false predicate must fail in ordinary execution.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import and from ... import for required supplied dependencies', 'def with parameters and return', 'local variable assignment', 'list and dictionary literals', 'string and numeric literals', 'set()', 'for loops', 'if, elif and else', 'in and not in membership tests', 'set.add()', 'dictionary key lookup', 'dictionary item assignment', 'list.append()', 'comparison operators', 'and, or and not', 'len()', 'assert predicate'] blocked=9 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'records': [{'observation_id': 'obs_A',
              'order_key': 'A',
              'distance': 2,
              'zone': 'north'},
             {'observation_id': 'obs_B',
              'order_key': 'B',
              'distance': 4,
              'zone': 'South'},
             {'observation_id': 'obs_C',
              'order_key': 'C',
              'distance': 0,
              'zone': 'north'},
             {'observation_id': 'obs_D',
              'order_key': 'D',
              'distance': -1,
              'zone': 'south'},
             {'observation_id': 'obs_A_repeat',
              'order_key': 'A',
              'distance': 2,
              'zone': 'north'}],
 'valid': [{'observation_id': 'obs_A',
            'order_key': 'A',
            'distance': 2,
            'zone': 'north'},
           {'observation_id': 'obs_B',
            'order_key': 'B',
            'distance': 4,
            'zone': 'south'},
           {'observation_id': 'obs_C',
            'order_key': 'C',
            'distance': 0,
            'zone': 'north'},
           {'observation_id': 'obs_D',
            'order_key': 'D',
            'distance': 100,
            'zone': 'south'}],
 'policy': {'repeat_accepted_key': 'reject',
            'zone_repairs': {'South': 'south'},
            'distance_min': 0,
            'distance_max': 100,
            'invalid_distance': 'reject'},
 'connection': 'authorized local fixture only'}

records = FIXTURES['records']
policy = FIXTURES['policy']

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'records': [{'observation_id': 'obs_A',
              'order_key': 'A',
              'distance': 2,
              'zone': 'north'},
             {'observation_id': 'obs_B',
              'order_key': 'B',
              'distance': 4,
              'zone': 'South'},
             {'observation_id': 'obs_C',
              'order_key': 'C',
              'distance': 0,
              'zone': 'north'},
             {'observation_id': 'obs_D',
              'order_key': 'D',
              'distance': -1,
              'zone': 'south'},
             {'observation_id': 'obs_A_repeat',
              'order_key': 'A',
              'distance': 2,
              'zone': 'north'}],
 'valid': [{'observation_id': 'obs_A',
            'order_key': 'A',
            'distance': 2,
            'zone': 'north'},
           {'observation_id': 'obs_B',
            'order_key': 'B',
            'distance': 4,
            'zone': 'south'},
           {'observation_id': 'obs_C',
            'order_key': 'C',
            'distance': 0,
            'zone': 'north'},
           {'observation_id': 'obs_D',
            'order_key': 'D',
            'distance': 100,
            'zone': 'south'}],
 'policy': {'repeat_accepted_key': 'reject',
            'zone_repairs': {'South': 'south'},
            'distance_min': 0,
            'distance_max': 100,
            'invalid_distance': 'reject'},
 'connection': 'authorized local fixture only'}

records = FIXTURES['records']
policy = FIXTURES['policy']

def clean(records, policy):
    accepted = set()
    cleaned = []
    report = []
    for row in records:
        key = row['order_key']
        if key in accepted:
            report.append({'observation_id':row['observation_id'],'action':policy['repeat_accepted_key']})
        elif row['distance'] < policy['distance_min'] or row['distance'] > policy['distance_max']:
            report.append({'observation_id':row['observation_id'],'action':policy['invalid_distance']})
        else:
            zone = row['zone']
            if zone in policy['zone_repairs']:
                zone = policy['zone_repairs'][zone]
                report.append({'observation_id':row['observation_id'],'action':'repair'})
            new = {'observation_id':row['observation_id'],'order_key':key,'distance':row['distance'],'zone':zone}
            cleaned.append(new)
            accepted.add(key)
    return {'cleaned':cleaned,'report':report}
result = clean(records, policy)
assert result['cleaned'][1]['zone'] == 'south'
assert result['cleaned'][2]['distance'] == policy['distance_min']
assert result['cleaned'][2]['observation_id'] == records[2]['observation_id']
assert result['report'][2]['observation_id'] == records[4]['observation_id']
boundary = clean(FIXTURES['valid'], policy)
assert boundary['cleaned'][3]['distance'] == policy['distance_max']

  test call0 (function_call, visible=False): {"function":"clean","args":[[{"observation_id":"obs_A","order_key":"A","distance":2,"zone":"north"},{"observation_id":"obs_B","order_key":"B","distance":4,"zone":"South"},{"observation_id":"obs_C","order_key":"C","distance":0,"zone":"north"},{"observation_id":"obs_D","order_key":"D","distance":-1,"zone":"south"},{"observation_id":"obs_A_repeat","order_key":"A","distance":2,"zone":"north"}],{"repeat_accepted_key":"reject","zone_repairs":{"South":"south"},"distance_min":0,"distance_max":100,"inval | on-fail: The parameterized function fails a supplied boundary fixture.
  test call1 (function_call, visible=False): {"function":"clean","args":[[],{"repeat_accepted_key":"reject","zone_repairs":{"South":"south"},"distance_min":0,"distance_max":100,"invalid_distance":"reject"}],"expected":{"cleaned":[],"report":[]}} | on-fail: The parameterized function fails a supplied boundary fixture.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"fa6ca981ca24f95b8c326f20e20679d8023ac861dee4aacd85a07d6ae4deaefa","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Track accepted keys and distinguish changed observations from unchanged retained ones.']  remediation→r04
  MEASURES: B:apply_declared_duplicate_resolution_policy(f1,f2); B:resolve_invalid_observations_and_report_actions(f2,f3,f4); B:verify_cleaning_policy_with_assert_predicates(f5)   anchors=['practice']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f2←s06; B.f3←s06; B.f4←s06; B.f5←s06

### s11 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) A loaded table can violate structure or value bounds; explicit exceptions reject it, while assertions exercise fixtures. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) An approved spelling repair does not authorize silently repairing every defect; report each policy action and affected ID. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Identify sampling and selection bias in dataset coverage: Next: Identify sampling and selection bias in dataset coverage.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Validate and Clean Datasets
(definition) Express value constraints as boolean predicates. Raise an explicit validation exception for a failed required column, type or value boundary. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) A loaded table can violate structure or value bounds; explicit exceptions reject it, while assertions exercise fixtures. ⟦A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.distance_zone cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Validate and Clean Datasets
(definition) A schema specifies expected features and permitted representations or values. Missing, unexpected and invalid features violate it. Compare table.columns and table.dtypes to the declared contract before checking constrained columns. Express value constraints as boolean predicates. Raise an explicit validation exception for a failed required column, type or value boundary. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) A loaded table can violate structure or value bounds; explicit exceptions reject it, while assertions exercise fixtures. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.distance_zone cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r03 · Contrast: Validate and Clean Datasets
(definition) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f5 B:tb3 B:tb4⟧
(example) An approved spelling repair does not authorize silently repairing every defect; report each policy action and affected ID. ⟦B.f5 B:tb3 B:tb4⟧
[TABLE ds.cleaning_orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r04 · Contrast: Validate and Clean Datasets
(definition) Track accepted observation keys in a set; check membership before adding the next accepted key. Choose the declared retain, repair or reject action from a policy dictionary for each invalid or repeated observation. Inspect and clean examples as needed, making representations consistent with their intended training use. Implement policy actions with conditional branches and report affected observation IDs rather than changing data silently. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) An approved spelling repair does not authorize silently repairing every defect; report each policy action and affected ID. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.cleaning_orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: DataFrame.drop_duplicates()
· constraints.blocked_syntax: pandas.get_dummies()
· constraints.blocked_syntax: model.fit() and model.predict()

=========

# EVALUATOR PACKET — Representation, Labels and Splits / Representation, Labels and Splits / Representation, Labels and Splits (mle.tile.009_011)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.dataset_selection_bias — Identify sampling and selection bias in dataset coverage
B = mle.label_integrity — Validate labels and their availability for the prediction task
C = mle.deployment_matched_splits — Choose leakage-safe train, validation and test splits matching deployment conditions

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=6
  warn: mle.tile.009_011.s01: prose block without lineage.fact_ids
  warn: mle.tile.009_011.s06/ix.mle.tile.009_011.s06: ADVISORY — syntax descriptors with no detector: ['array arithmetic', 'array indexing', 'division', 'if/else', 'integer and floating-point literals', 'list literals', 'numeric comparisons', 'string literals']
  warn: mle.tile.009_011.s07: prose block without lineage.fact_ids
  warn: mle.tile.009_011.s11/ix.mle.tile.009_011.s11: ADVISORY — syntax descriptors with no detector: ['assert predicate statements', 'calls to supplied acceptance predicates', 'comparison and Boolean operators', 'def with parameters and return', 'dictionary key lookup and assignment', 'for loops', 'if, elif and else', 'import statements for supplied dataset and timestamp handling', 'list, tuple, dictionary and set literals', 'membership checks with in and not in', 'mlflow API calls', 'string, numeric, Boolean and None literals', 'torch API calls']
  warn: mle.tile.009_011.s12: prose block without lineage.fact_ids
  warn: mle.tile.009_011.s16/ix.mle.tile.009_011.s16: ADVISORY — syntax descriptors with no detector: ['Boolean operators and, or, and not', 'arithmetic operators + and /', 'assert predicate', 'calls to the supplied fixture and unit-test interfaces', 'comparison operators <, <=, >, >=, ==, and !=', 'def and return', 'dictionary literals and supplied observation field access', 'for loops', 'if, elif, and else', 'import and from ... import for required supplied fixture dependencies', 'integer, floating-point, string, and Boolean literals', 'list literals and list comprehensions', 'membership tests with in and not in']

## SOURCE FACTS — A (mle.dataset_selection_bias)   objective: Diagnose sample coverage using empirical inclusion proportions and numeric summaries.
A.f1: Data omitted by collection or filtering can exclude observations that matter to the intended prediction population.   [sources: google_rules_of_ml#Rule #6: Be careful about dropped data when copying pipelines]
A.f2: Compare each category count divided by its population total between the supplied sample and target population to identify supported coverage differences.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f3: For a category with known target membership, estimate inclusion probability as included category members divided by all target category members; an empty denominator cannot support a rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: Unequal sampling probabilities affect the interpretation of a sample; a descriptive sample summary is not automatically representative of the target population.   [sources: google_rules_of_ml#Rule #30: Importance-weight sampled data, don’t arbitrarily drop it!]
A.f5: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f6: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Representation, Labels and Splits.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Using the supplied zone-A and zone-B order counts and selected numeric_values, calculate sample and target category proportions, category-specific inclusion probabilities, the arithmetic mean, and standard deviation with ddof=0. Record one coverage limitation supported by the counts.  SUCCESS: The results distinguish sample shares of 0.75 and 0.25 from target shares of 0.60 and 0.40 and inclusion probabilities of 0.50 and 0.25. Numeric summaries match the supplied observations and specified divisor. The recorded limitation identifies lower inclusion and sample share for zone B without claiming an unobserved cause or inevitable prediction failure.
ASSESSMENT ANCHOR: identify_collection_related_coverage_limitations facts=['f1', 'f4']
ASSESSMENT ANCHOR: compare_sample_and_target_category_proportions facts=['f2']
ASSESSMENT ANCHOR: interpret_category_inclusion_rates_with_valid_denominators facts=['f3', 'f4']

## SOURCE FACTS — B (mle.label_integrity)   objective: Verify keyed label correspondence and the declared label-availability boundaries.
B.f1: A label must match its prediction or observation through the intended unique identifier, rather than through incidental row order.   [sources: sagemaker_model_monitor#model-monitor-model-quality-merge.html — Ingest Ground Truth labels and merge them with predictions]
B.f2: Check for repeated IDs before building an ID-to-label dictionary, because assigning an existing dictionary key replaces its earlier value.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f3: Use set differences between observation IDs and label IDs to detect observations missing labels and labels with no observation.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f4: Use keyed dictionary lookups to compare each label, observation timestamp and availability timestamp against the task-specific acceptance predicates.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f5: Do not treat information unavailable at the relevant prediction boundary as an available input to that prediction.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
B.f6: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Representation, Labels and Splits.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition, mle.dataset_schema_validation, mle.dataset_inspection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement one learner-defined Python audit function with learner-written imports for the supplied A/B fixtures and acceptance predicates. Check repeated observation and label IDs before accepting an observation-ID-to-label-and-timestamps dictionary. Use set differences to identify missing and orphaned labels, then keyed lookups to evaluate identity, label validity and task-specific timestamp predicates. Return one label-integrity verdict with affected IDs and author assert checks for valid, reordered, duplicate, missing, orphaned, misaligned, unavailable and declared boundary cases.  SUCCESS: The audit accepts valid records regardless of label row order, reports repeated IDs before dictionary replacement can hide them, distinguishes both unmatched-ID directions, and reports invalid, misaligned or time-unsuitable records using the supplied predicates. Assertions verify the verdict and affected IDs for every declared fixture, including the timestamp boundary.
ASSESSMENT ANCHOR: identify_misaligned_labels_by_observation_id facts=['f1', 'f4']
ASSESSMENT ANCHOR: identify_duplicate_missing_and_orphaned_label_ids facts=['f2', 'f3']
ASSESSMENT ANCHOR: determine_label_validity_and_task_specific_availability facts=['f4', 'f5']
ASSESSMENT ANCHOR: verify_label_integrity_with_assert_predicates facts=['f6']

## SOURCE FACTS — C (mle.deployment_matched_splits)   objective: Implement a split that matches the evaluation scenario’s group and time dependencies.
C.f1: A random split is appropriate only if its sampling interpretation matches the intended evaluation; dependent grouped or time-ordered data can require different boundaries.   [sources: scikit_learn_user_guide#modules/cross_validation.html — 3.1.1 Computing cross-validated metrics; 3.1.2 Cross validation iterators]
C.f2: Keep observations from a common evaluation group entirely on one side of the boundary, and keep time-ordered training observations earlier than the intended later evaluation observations.   [sources: scikit_learn_user_guide#modules/cross_validation.html — 3.1.1 Computing cross-validated metrics; 3.1.2 Cross validation iterators]
C.f3: Implement the supplied group membership with sets and assert that training and validation group intersections are empty.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
C.f4: For a time boundary, select training observations before the cutoff and later evaluation observations under the stated scenario, and check the timestamp inequalities.   [sources: scikit_learn_user_guide#modules/cross_validation.html — 3.1.1 Computing cross-validated metrics; 3.1.2 Cross validation iterators]
C.f5: Calculate each partition’s target outcome count divided by its partition total to report the population actually evaluated.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
C.f6: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Representation, Labels and Splits.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition, mle.label_integrity. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function that partitions supplied list observations according to a declared group-based or time-based deployment scenario. Justify the boundaries, calculate each partition's target proportion, and verify the deliverable with learner-written assertions and supplied unit-test fixtures. Write any imports required by the supplied fixture interface.  SUCCESS: The function assigns observations according to the stated scenario. Group-based partitions keep each group wholly on one side and have empty group-set intersections. Time-based partitions satisfy the declared cutoff and later-interval inequalities, including cutoff equality cases. Each nonempty partition reports its target count divided by its total. Assertions pass for valid fixtures and raise AssertionError for declared violations during ordinary non-optimized execution; supplied unit-test fixtures confirm the same deliverable.
ASSESSMENT ANCHOR: choose_deployment_matched_split_boundaries facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_disjoint_evaluation_groups facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_scenario_matched_time_boundaries facts=['f2', 'f4']
ASSESSMENT ANCHOR: interpret_partition_target_proportions facts=['f5']
ASSESSMENT ANCHOR: assert_valid_boundary_and_failure_cases facts=['f6']

## DATA ASSETS USED
ds.group_orders: Separate group evaluation fixture — columns: order_key(identifier), customer_group(identifier), target(categorical,digits-as-label)
   ["A","G1",1]
   ["B","G1",0]
   ["C","G2",1]
ds.labels: Labels in reversed keyed order — columns: observation_id(identifier), label(categorical,digits-as-label), observation_timestamp(datetime), availability_timestamp(datetime)
   ["B",0,"2025-01-01T10:00:00","2025-01-01T10:30:00"]
   ["A",1,"2025-01-01T09:00:00","2025-01-01T09:30:00"]
   variant duplicate_id: 1 ops; planted: duplicate_label(duplicate_row)
   variant missing_label: 1 ops; planted: 
   variant orphan_label: 1 ops; planted: 
   variant invalid_label: 1 ops; planted: invalid_label(other)
   variant misaligned_timestamp: 1 ops; planted: 
   variant unavailable_label: 1 ops; planted: 
ds.observations: Observation IDs and observation timestamps — columns: observation_id(identifier), observation_timestamp(datetime)
   ["A","2025-01-01T09:00:00"]
   ["B","2025-01-01T10:00:00"]
ds.order_features: Three observations with two numerical features — columns: distance(numerical), feature_2(numerical)
   [2,10]
   [4,20]
   [6,30]
   variant one_order: 2 ops; planted: 
   variant wrong_width: 1 ops; planted: 
   variant four_orders: 1 ops; planted: 
   variant empty: 3 ops; planted: 
ds.selection_counts: Known target/sample membership counts — columns: zone(categorical), sample_count(numerical), target_count(numerical)
   ["zone-A",30,60]
   ["zone-B",10,40]
ds.time_orders: Separate later-order evaluation fixture — columns: order_key(identifier), observation_timestamp(datetime), target(categorical,digits-as-label)
   ["T1","2024-12-29T09:00:00",0]
   ["T2","2024-12-30T09:00:00",0]
   ["T3","2024-12-31T09:00:00",0]
   ["T4","2025-01-01T09:00:00",1]
   ["T5","2025-01-02T09:00:00",1]
   ["T6","2025-01-03T09:00:00",1]
   ["T7","2025-01-04T09:00:00",1]
   ["T8","2025-01-05T09:00:00",0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Build a dataset and minibatch loader; Choose leakage-safe train, validation and test splits matching deployment conditions; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compose a fitted preprocessing pipeline reused across training and bounded inference; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define measurable model acceptance criteria from task objectives; Derive task-relevant features from prediction-time information; Detect target or preprocessing leakage across training and prediction boundaries; Document model limitations and foreseeable misuse under an existing risk policy; Encode categorical features with an unseen-category policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Fit and predict with a bounded scikit-learn baseline workflow; Fit missing-value imputation using training data only; Ins

## LESSON, in learner order

### s01 · explainer · Representation, Labels and Splits
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(definition) Collection or filtering omissions can exclude observations important to the intended prediction population. Compare category count divided by population total in sample and target to identify supported coverage differences. With known target membership, estimate inclusion probability as included category members divided by all target category members. An empty denominator cannot support a rate. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Unequal inclusion probabilities affect sample interpretation. A descriptive sample summary is not automatically target-representative. Compute the selected numeric observations' arithmetic mean with np.mean(numeric_values). Use np.std(numeric_values, ddof=0) to divide squared deviations by N before taking the square root. Use ddof=1 only if the stated calculation needs N-1. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[TABLE ds.selection_counts cols=all ] caption: Known target/sample membership counts
[TABLE ds.order_features cols=all ] caption: Three observations with two numerical features
[CODE python]
fixture = {'sample_counts': {'zone-A': 30, 'zone-B': 10},
 'target_counts': {'zone-A': 60, 'zone-B': 40},
 'numeric_values': [[2], [4], [6]],
 'ddof': 0}

import numpy as np
sample_total = sum(fixture["sample_counts"].values())
target_total = sum(fixture["target_counts"].values())
for zone, target in fixture["target_counts"].items():
    sample = fixture["sample_counts"].get(zone, 0)
    inclusion = sample / target if target else None
    print(zone, "sample share:", sample, sample_total, sample / sample_total,
          "target share:", target, target_total, target / target_total,
          "inclusion:", sample, target, inclusion)
values = np.array(fixture["numeric_values"])
print("selected numeric observations:", values)
print("mean, std, divisor choice:", np.mean(values), np.std(values, ddof=fixture["ddof"]), fixture["ddof"])
  annotations: []

### s02 · explainer · A bounded work example
Working rule — 
(example) Compare the supplied sample and target zone counts with their own population totals. Inclusion uses a different denominator: all target members of that zone. These ratios support a coverage comparison, not claims about every zone characteristic. Summarize the selected numeric observations using their stated mean and standard-deviation divisor. Do not invent an inclusion rate when target membership is empty. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb4⟧

### s03 · video · Trace the working rule
Optional walkthrough — 
[VIDEO How missing observations distort dataset coverage] bridge-before: Watch how observing only returning aircraft changes the interpretation of bullet holes. Connect the clip’s term “selection bias” to collection that excludes relevant observations. | bridge-after: The clip explains missing observations and misleading sample summaries qualitatively. The text supplies category proportions, conditional inclusion rates, empty-denominator handling, and NumPy mean and standard-deviation calculations.
  - _yR5wZsh4YI 21-137s facts=['f1', 'f4'] label: Selection bias: reasoning about observations that never arrived | summary: Selection bias arises when observed information does not represent the population being studied. The narrated aircraft example describes returning planes with many bullet holes in their bodies and wings but fewer near their engines. Looking only at those planes suggested adding armor where holes were most common. Wald instead argued for protecting areas with few observed holes: aircraft hit in the engine were not returning. The observed damage therefore reflected which aircraft survived to be counted, not the damage across all aircraft. Missing observations changed how the sample should be interpreted.

### s04 · explainer · A distinction to keep
Working rule — 
(misconception) Sample share and inclusion probability have different denominators. A sample summary is not automatically target-representative. ⟦A.f4 A:tb5⟧

### s05 · check · Judge the representation, labels and splits decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] To estimate inclusion within a category whose target members are known, which denominator is needed?
  ✔ 0: All target members in that category
      why: Correct. A category-specific inclusion rate divides included category members by target category members, not all sampled rows or the numerator itself.
  ✘ 1: The total sample across all categories
      why: A category-specific inclusion rate divides included category members by target category members, not all sampled rows or the numerator itself.
  ✘ 2: The included members in that category
      why: A category-specific inclusion rate divides included category members by target category members, not all sampled rows or the numerator itself.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Compare category inclusion with category shares before interpreting coverage.']  remediation→r01
  MEASURES: A:interpret_category_inclusion_rates_with_valid_denominators(f3,f4)   anchors=[]
  taught-before-tested: A.f3←s01; A.f4←s01

### s06 · hands_on · Verify representation, labels and splits
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Using the supplied nonempty category denominators, assign sample_shares, target_shares and inclusion arrays in zone-A, zone-B order. Compute mean and std of numeric_values with ddof=0. Set limitation to the supported lower-inclusion observation for zone B (not a causal or performance claim). Assign result as [sample_shares, target_shares, inclusion, mean, std, limitation]. First identify the supporting comparisons: zone-B inclusion 0.25 versus zone-A 0.50, and zone-B sample share 0.25 versus target share 0.40. Use this exact supported limitation sentence in the result: Zone B has lower inclusion and sample share than its target share; the counts establish neither a cause nor inevitable prediction failure.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'variable assignment', 'integer and floating-point literals', 'string literals', 'list literals', 'np.array(...)', 'array indexing', 'array arithmetic', 'division', 'numeric comparisons', 'if/else', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1)'] blocked=7 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'sample_counts': {'zone-A': 30, 'zone-B': 10},
 'target_counts': {'zone-A': 60, 'zone-B': 40},
 'numeric_values': [[2], [4], [6]],
 'ddof': 0}

import numpy as np
sample = np.array([FIXTURES['sample_counts']['zone-A'], FIXTURES['sample_counts']['zone-B']])
target = np.array([FIXTURES['target_counts']['zone-A'], FIXTURES['target_counts']['zone-B']])
numeric_values = np.array(FIXTURES['numeric_values'])

sample_A = 30
sample[0] = sample_A
# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'sample_counts': {'zone-A': 30, 'zone-B': 10},
 'target_counts': {'zone-A': 60, 'zone-B': 40},
 'numeric_values': [[2], [4], [6]],
 'ddof': 0}

import numpy as np
sample = np.array([FIXTURES['sample_counts']['zone-A'], FIXTURES['sample_counts']['zone-B']])
target = np.array([FIXTURES['target_counts']['zone-A'], FIXTURES['target_counts']['zone-B']])
numeric_values = np.array(FIXTURES['numeric_values'])
sample_A = 30
sample[0] = sample_A

sample_shares = sample / (sample[0]+sample[1])
target_shares = target / (target[0]+target[1])
inclusion = sample / target
mean = np.mean(numeric_values)
std = np.std(numeric_values, ddof=0)
limitation = 'Zone B has lower inclusion and sample share than its target share; the counts establish neither a cause nor inevitable prediction failure.'
result = [sample_shares, target_shares, inclusion, mean, std, limitation]

  test result (value_equals, visible=True): {"expr":"result","expected":[[0.75,0.25],[0.6,0.4],[0.5,0.25],4,1.632993161855452,"Zone B has lower inclusion and sample share than its target share; the counts establish neither a cause nor inevitable prediction failure."]} | on-fail: The named result does not meet the declared contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5c6bf00dd80bab93504f712641368ad07d3cb4c2a602a6efd7da0c2c7f3c565b","tests_passed":1}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['For inclusion probability, count all target members of the same category in the denominator.']  remediation→r02
  MEASURES: A:identify_collection_related_coverage_limitations(f1,f4); A:compare_sample_and_target_category_proportions(f2); A:interpret_category_inclusion_rates_with_valid_denominators(f3,f4)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f4←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s07 · explainer · Representation, Labels and Splits
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦B:tb1⟧
(mechanism) Match labels to observations or predictions by the intended unique identifier, not incidental row order. Check duplicate IDs before constructing the ID-to-label dictionary: reassignment of an existing key replaces its earlier value. Use observation-ID and label-ID set differences to detect missing labels and labels without observations. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use keyed dictionary lookups to compare labels, observation timestamps and availability timestamps under task-specific acceptance predicates. Information unavailable at the relevant prediction boundary is not an available input to that prediction. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.observations cols=all ] caption: Observation IDs and observation timestamps
[TABLE ds.labels cols=all ] caption: Labels in reversed keyed order
[CODE python]
fixture = {'observations': [{'observation_id': 'A', 'observation_timestamp': '2025-01-01T09:00:00'},
                  {'observation_id': 'B',
                   'observation_timestamp': '2025-01-01T10:00:00'}],
 'labels': [{'observation_id': 'B',
             'label': 0,
             'observation_timestamp': '2025-01-01T10:00:00',
             'availability_timestamp': '2025-01-01T10:30:00'},
            {'observation_id': 'A',
             'label': 1,
             'observation_timestamp': '2025-01-01T09:00:00',
             'availability_timestamp': '2025-01-01T09:30:00'}],
 'cases': {'duplicate_id': [{'observation_id': 'B',
                             'label': 0,
                             'observation_timestamp': '2025-01-01T10:00:00',
                             'availability_timestamp': '2025-01-01T10:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'}],
           'missing_label': [{'observation_id': 'B',
                              'label': 0,
                              'observation_timestamp': '2025-01-01T10:00:00',
                              'availability_timestamp': '2025-01-01T10:30:00'}],
           'orphan_label': [{'observation_id': 'C',
                             'label': 0,
                             'observation_timestamp': '2025-01-01T10:00:00',
                             'availability_timestamp': '2025-01-01T10:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'}],
           'invalid_label': [{'observation_id': 'B',
                              'label': 0,
                              'observation_timestamp': '2025-01-01T10:00:00',
                              'availability_timestamp': '2025-01-01T10:30:00'},
                             {'observation_id': 'A',
                              'label': 2,
                              'observation_timestamp': '2025-01-01T09:00:00',
                              'availability_timestamp': '2025-01-01T09:30:00'}],
           'misaligned_timestamp': [{'observation_id': 'B',
                                     'label': 0,
                                     'observation_timestamp': '2025-01-01T10:00:00',
                                     'availability_timestamp': '2025-01-01T10:30:00'},
                                    {'observation_id': 'A',
                                     'label': 1,
                                     'observation_timestamp': '2025-01-01T09:01:00',
                                     'availability_timestamp': '2025-01-01T09:30:00'}],
           'unavailable_label': [{'observation_id': 'B',
                                  'label': 0,
                                  'observation_timestamp': '2025-01-01T10:00:00',
                                  'availability_timestamp': '2025-01-01T10:30:00'},
                                 {'observation_id': 'A',
                                  'label': 1,
                                  'observation_timestamp': '2025-01-01T09:00:00',
                                  'availability_timestamp': '2025-01-02T09:30:00'}]},
 'contract': {'label_values': [0, 1],
              'require_matching_observation_timestamp': True,
              'availability_cutoff': '2025-01-01T10:30:00',
              'availability_boundary_inclusive': True}}

from datetime import datetime

def match(observations, labels, contract):
    observation_ids = [row["observation_id"] for row in observations]
    label_ids = [row["observation_id"] for row in labels]
    if len(set(observation_ids)) != len(observation_ids) or len(set(label_ids)) != len(label_ids):
        raise ValueError("repeated ID")
    missing = set(observation_ids) - set(label_ids)
    extra = set(label_ids) - set(observation_ids)
    print("missing, extra:", missing, extra)
    if missing or extra:
        raise ValueError("ID correspondence violated")
    by_id = {row["observation_id"]: row for row in labels}
    matched = []
    for observation in observations:
        label = by_id[observation["observation_id"]]
        assert label["label"] in contract["label_values"]
        if contract["require_matching_observation_timestamp"]:
            assert label["observation_timestamp"] == observation["observation_timestamp"]
        # The fixture's label may arrive later; it is not an earlier prediction input.
        available = datetime.fromisoformat(label["availability_timestamp"])
        cutoff = datetime.fromisoformat(contract["availability_cutoff"])
        assert available <= cutoff if contract["availability_boundary_inclusive"] else available < cutoff
        matched.append((observation, label))
    return matched

print(match(fixture["observations"], fixture["labels"], fixture["contract"]))
for name, labels in fixture["cases"].items():
    try:
        print(name, match(fixture["observations"], labels, fixture["contract"]))
    except (ValueError, AssertionError) as error:
        print(name, type(error).__name__)
  annotations: []

### s08 · explainer · A bounded work example
Working rule — 
(example) The label records are reordered relative to observations. Keyed lookup preserves correspondence; matching row counts alone does not. Detect duplicate IDs before dictionary construction, then inspect both ID-set differences and matched timestamps under the supplied predicates. Later label availability does not make it an earlier prediction input. Exercise reordered, duplicate, missing and boundary fixtures. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb4⟧

### s09 · explainer · A distinction to keep
Working rule — 
(misconception) Equal row counts can hide reordered identities. A dictionary built before duplicate checks can hide a replaced label. ⟦B.f1 B.f2 B:tb5⟧

### s10 · check · Judge the representation, labels and splits decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] A deliberately false label-integrity predicate is asserted in ordinary non-optimized execution. What follows?
  ✔ 0: AssertionError
      why: Correct. An assertion verifies a predicate; it does not align or remove records.
  ✘ 1: The label is automatically realigned
      why: An assertion verifies a predicate; it does not align or remove records.
  ✘ 2: The duplicated ID is automatically removed
      why: An assertion verifies a predicate; it does not align or remove records.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Consider the false predicate under the stated non-optimized execution mode.']  remediation→r03
  MEASURES: B:verify_label_integrity_with_assert_predicates(f6)   anchors=[]
  taught-before-tested: B.f6←s07

### s11 · hands_on · Verify representation, labels and splits
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Implement audit(observations, labels, contract). Check repeated IDs before constructing keyed records, distinguish missing and orphaned sets, and audit label values, matched observation timestamps and inclusive availability cutoff. Return ok, repeated_observation_ids, repeated_label_ids, missing, orphaned, invalid and matched (the first label record for each ID). Assign result; assert reordered acceptance, every supplied failure case and cutoff equality. The task concerns label availability for this audit, not permission to use later labels as prediction inputs. Return a dictionary. repeated_observation_ids and repeated_label_ids are lists in encounter order, with one entry for each repeated occurrence after the first. missing and orphaned are sets. invalid is a list of affected matched IDs in observation encounter order. matched is a dictionary containing the first complete label record for every label ID, including orphaned IDs. ok is a Boolean.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['import statements for supplied dataset and timestamp handling', 'def with parameters and return', 'list, tuple, dictionary and set literals', 'string, numeric, Boolean and None literals', 'variable assignment', 'for loops', 'if, elif and else', 'dictionary key lookup and assignment', 'membership checks with in and not in', 'set() and set difference', 'len()', 'list.append() and set.add()', 'comparison and Boolean operators', 'calls to supplied acceptance predicates', 'assert predicate statements'] blocked=9 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'observations': [{'observation_id': 'A',
                   'observation_timestamp': '2025-01-01T09:00:00'},
                  {'observation_id': 'B',
                   'observation_timestamp': '2025-01-01T10:00:00'}],
 'labels': [{'observation_id': 'B',
             'label': 0,
             'observation_timestamp': '2025-01-01T10:00:00',
             'availability_timestamp': '2025-01-01T10:30:00'},
            {'observation_id': 'A',
             'label': 1,
             'observation_timestamp': '2025-01-01T09:00:00',
             'availability_timestamp': '2025-01-01T09:30:00'}],
 'cases': {'duplicate_id': [{'observation_id': 'B',
                             'label': 0,
                             'observation_timestamp': '2025-01-01T10:00:00',
                             'availability_timestamp': '2025-01-01T10:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'}],
           'missing_label': [{'observation_id': 'B',
                              'label': 0,
                              'observation_timestamp': '2025-01-01T10:00:00',
                              'availability_timestamp': '2025-01-01T10:30:00'}],
           'orphan_label': [{'observation_id': 'C',
                             'label': 0,
                             'observation_timestamp': '2025-01-01T10:00:00',
                             'availability_timestamp': '2025-01-01T10:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'}],
           'invalid_label': [{'observation_id': 'B',
                              'label': 0,
                              'observation_timestamp': '2025-01-01T10:00:00',
                              'availability_timestamp': '2025-01-01T10:30:00'},
                             {'observation_id': 'A',
                              'label': 2,
                              'observation_timestamp': '2025-01-01T09:00:00',
                              'availability_timestamp': '2025-01-01T09:30:00'}],
           'misaligned_timestamp': [{'observation_id': 'B',
                                     'label': 0,
                                     'observation_timestamp': '2025-01-01T10:00:00',
                                     'availability_timestamp': '2025-01-01T10:30:00'},
                                    {'observation_id': 'A',
                                     'label': 1,
                                     'observation_timestamp': '2025-01-01T09:01:00',
                                     'availability_timestamp': '2025-01-01T09:30:00'}],
           'unavailable_label': [{'observation_id': 'B',
                                  'label': 0,
                                  'observation_timestamp': '2025-01-01T10:00:00',
                                  'availability_timestamp': '2025-01-01T10:30:00'},
                                 {'observation_id': 'A',
                                  'label': 1,
                                  'observation_timestamp': '2025-01-01T09:00:00',
                                  'availability_timestamp': '2025-01-02T09:30:00'}]},
 'contract': {'label_values': [0, 1],
              'require_matching_observation_timestamp': True,
              'availability_cutoff': '2025-01-01T10:30:00',
              'availability_boundary_inclusive': True}}

observations = FIXTURES['observations']
labels = FIXTURES['labels']
contract = FIXTURES['contract']

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'observations': [{'observation_id': 'A',
                   'observation_timestamp': '2025-01-01T09:00:00'},
                  {'observation_id': 'B',
                   'observation_timestamp': '2025-01-01T10:00:00'}],
 'labels': [{'observation_id': 'B',
             'label': 0,
             'observation_timestamp': '2025-01-01T10:00:00',
             'availability_timestamp': '2025-01-01T10:30:00'},
            {'observation_id': 'A',
             'label': 1,
             'observation_timestamp': '2025-01-01T09:00:00',
             'availability_timestamp': '2025-01-01T09:30:00'}],
 'cases': {'duplicate_id': [{'observation_id': 'B',
                             'label': 0,
                             'observation_timestamp': '2025-01-01T10:00:00',
                             'availability_timestamp': '2025-01-01T10:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'}],
           'missing_label': [{'observation_id': 'B',
                              'label': 0,
                              'observation_timestamp': '2025-01-01T10:00:00',
                              'availability_timestamp': '2025-01-01T10:30:00'}],
           'orphan_label': [{'observation_id': 'C',
                             'label': 0,
                             'observation_timestamp': '2025-01-01T10:00:00',
                             'availability_timestamp': '2025-01-01T10:30:00'},
                            {'observation_id': 'A',
                             'label': 1,
                             'observation_timestamp': '2025-01-01T09:00:00',
                             'availability_timestamp': '2025-01-01T09:30:00'}],
           'invalid_label': [{'observation_id': 'B',
                              'label': 0,
                              'observation_timestamp': '2025-01-01T10:00:00',
                              'availability_timestamp': '2025-01-01T10:30:00'},
                             {'observation_id': 'A',
                              'label': 2,
                              'observation_timestamp': '2025-01-01T09:00:00',
                              'availability_timestamp': '2025-01-01T09:30:00'}],
           'misaligned_timestamp': [{'observation_id': 'B',
                                     'label': 0,
                                     'observation_timestamp': '2025-01-01T10:00:00',
                                     'availability_timestamp': '2025-01-01T10:30:00'},
                                    {'observation_id': 'A',
                                     'label': 1,
                                     'observation_timestamp': '2025-01-01T09:01:00',
                                     'availability_timestamp': '2025-01-01T09:30:00'}],
           'unavailable_label': [{'observation_id': 'B',
                                  'label': 0,
                                  'observation_timestamp': '2025-01-01T10:00:00',
                                  'availability_timestamp': '2025-01-01T10:30:00'},
                                 {'observation_id': 'A',
                                  'label': 1,
                                  'observation_timestamp': '2025-01-01T09:00:00',
                                  'availability_timestamp': '2025-01-02T09:30:00'}]},
 'contract': {'label_values': [0, 1],
              'require_matching_observation_timestamp': True,
              'availability_cutoff': '2025-01-01T10:30:00',
              'availability_boundary_inclusive': True}}

observations = FIXTURES['observations']
labels = FIXTURES['labels']
contract = FIXTURES['contract']

def audit(observations, labels, contract):
    obs = {}
    keyed = {}
    repeated_obs = []
    repeated_labels = []
    obs_ids = set()
    label_ids = set()
    bad = []
    for row in observations:
        key = row['observation_id']
        if key in obs_ids:
            repeated_obs.append(key)
        else:
            obs[key] = row
        obs_ids.add(key)
    for row in labels:
        key = row['observation_id']
        if key in label_ids:
            repeated_labels.append(key)
        else:
            keyed[key] = row
        label_ids.add(key)
    missing = obs_ids - label_ids
    orphaned = label_ids - obs_ids
    for key in obs:
        if key in label_ids:
            row = keyed[key]
            if row['label'] not in contract['label_values'] or row['observation_timestamp'] != obs[key]['observation_timestamp'] or row['availability_timestamp'] > contract['availability_cutoff']:
                bad.append(key)
    ok = not repeated_obs and not repeated_labels and not missing and not orphaned and not bad
    return {'ok':ok,'repeated_observation_ids':repeated_obs,'repeated_label_ids':repeated_labels,'missing':missing,'orphaned':orphaned,'invalid':bad,'matched':keyed}
result = audit(observations, labels, contract)
assert result['ok']
for case in FIXTURES['cases']:
    assert not audit(observations, FIXTURES['cases'][case], contract)['ok']
assert result['matched']['B']['availability_timestamp'] == contract['availability_cutoff']

  test case0 (function_call, visible=True): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"}],[{"observation_id":"B","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"},{"observation_id":"A","label":1,"observation_timestamp":"2025-01-01T09:00:00","availability_timestamp":"2025-01-01T09:30:00"}],{"label_values":[0,1],"require_matching_observation_timestamp":true,"availabil | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"}],[{"observation_id":"B","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"},{"observation_id":"A","label":1,"observation_timestamp":"2025-01-01T09:00:00","availability_timestamp":"2025-01-01T09:30:00"},{"observation_id":"A","label":1,"observation_timestamp":"2025-01-01T09:00:00"," | on-fail: This fixture does not satisfy the declared return contract.
  test case2 (function_call, visible=False): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"}],[{"observation_id":"B","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"}],{"label_values":[0,1],"require_matching_observation_timestamp":true,"availability_cutoff":"2025-01-01T10:30:00","availability_boundary_inclusive":true}],"expected":{"ok":false,"repeated_observation_ids":[ | on-fail: This fixture does not satisfy the declared return contract.
  test case3 (function_call, visible=False): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"}],[{"observation_id":"C","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"},{"observation_id":"A","label":1,"observation_timestamp":"2025-01-01T09:00:00","availability_timestamp":"2025-01-01T09:30:00"}],{"label_values":[0,1],"require_matching_observation_timestamp":true,"availabil | on-fail: This fixture does not satisfy the declared return contract.
  test case4 (function_call, visible=False): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"}],[{"observation_id":"B","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"},{"observation_id":"A","label":2,"observation_timestamp":"2025-01-01T09:00:00","availability_timestamp":"2025-01-01T09:30:00"}],{"label_values":[0,1],"require_matching_observation_timestamp":true,"availabil | on-fail: This fixture does not satisfy the declared return contract.
  test case5 (function_call, visible=False): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"}],[{"observation_id":"B","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"},{"observation_id":"A","label":1,"observation_timestamp":"2025-01-01T09:01:00","availability_timestamp":"2025-01-01T09:30:00"}],{"label_values":[0,1],"require_matching_observation_timestamp":true,"availabil | on-fail: This fixture does not satisfy the declared return contract.
  test case6 (function_call, visible=False): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"}],[{"observation_id":"B","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"},{"observation_id":"A","label":1,"observation_timestamp":"2025-01-01T09:00:00","availability_timestamp":"2025-01-02T09:30:00"}],{"label_values":[0,1],"require_matching_observation_timestamp":true,"availabil | on-fail: This fixture does not satisfy the declared return contract.
  test repeated_observation (function_call, visible=False): {"function":"audit","args":[[{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"},{"observation_id":"B","observation_timestamp":"2025-01-01T10:00:00"},{"observation_id":"A","observation_timestamp":"2025-01-01T09:00:00"}],[{"observation_id":"B","label":0,"observation_timestamp":"2025-01-01T10:00:00","availability_timestamp":"2025-01-01T10:30:00"},{"observation_id":"A","label":1,"observation_timestamp":"2025-01-01T09:00:00","availability_timestamp":"2025-01-01T09:30:00"}],{"label_v | on-fail: This fixture does not satisfy the declared return contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c4b619368a7922aef7935f5757ca2c7dc862bdb4b152944ffeed6fd49d8fd242","tests_passed":8}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check repeated IDs before keyed records can hide them, then compare observation and label ID sets.']  remediation→r04
  MEASURES: B:identify_misaligned_labels_by_observation_id(f1,f4); B:identify_duplicate_missing_and_orphaned_label_ids(f2,f3); B:determine_label_validity_and_task_specific_availability(f4,f5); B:verify_label_integrity_with_assert_predicates(f6)   anchors=['practice']
  taught-before-tested: B.f1←s07; B.f4←s07; B.f2←s07; B.f3←s07; B.f4←s07; B.f5←s07; B.f6←s07

### s12 · explainer · Representation, Labels and Splits
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦C:tb1⟧
(mechanism) A random split is appropriate only when its sampling interpretation matches evaluation. Group dependence or time ordering can require different boundaries. Keep a common evaluation group on one side; keep time-ordered training observations earlier than the intended later evaluation observations. Represent supplied groups with sets and assert an empty training/validation group intersection. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) For a time cutoff, select earlier training and the stated later evaluation observations; check timestamp inequalities. Report each partition's target count divided by its total to describe the population actually evaluated. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[TABLE ds.group_orders cols=all ] caption: Separate group evaluation fixture
[TABLE ds.time_orders cols=all ] caption: Separate later-order evaluation fixture
[CODE python]
fixture = {'group_records': [{'order_key': 'A', 'customer_group': 'G1', 'target': 1},
                   {'order_key': 'B', 'customer_group': 'G1', 'target': 0},
                   {'order_key': 'C', 'customer_group': 'G2', 'target': 1}],
 'training_groups': ['G1'],
 'validation_groups': ['G2'],
 'invalid_training_keys': ['A'],
 'invalid_validation_keys': ['B', 'C'],
 'time_records': [{'order_key': 'T1',
                   'observation_timestamp': '2024-12-29T09:00:00',
                   'target': 0},
                  {'order_key': 'T2',
                   'observation_timestamp': '2024-12-30T09:00:00',
                   'target': 0},
                  {'order_key': 'T3',
                   'observation_timestamp': '2024-12-31T09:00:00',
                   'target': 0},
                  {'order_key': 'T4',
                   'observation_timestamp': '2025-01-01T09:00:00',
                   'target': 1},
                  {'order_key': 'T5',
                   'observation_timestamp': '2025-01-02T09:00:00',
                   'target': 1},
                  {'order_key': 'T6',
                   'observation_timestamp': '2025-01-03T09:00:00',
                   'target': 1},
                  {'order_key': 'T7',
                   'observation_timestamp': '2025-01-04T09:00:00',
                   'target': 1},
                  {'order_key': 'T8',
                   'observation_timestamp': '2025-01-05T09:00:00',
                   'target': 0},
                  {'order_key': 'T9',
                   'observation_timestamp': '2025-01-06T09:00:00',
                   'target': 0},
                  {'order_key': 'T10',
                   'observation_timestamp': '2025-01-07T09:00:00',
                   'target': 0},
                  {'order_key': 'T11',
                   'observation_timestamp': '2025-01-08T09:00:00',
                   'target': 0},
                  {'order_key': 'T12',
                   'observation_timestamp': '2025-01-09T09:00:00',
                   'target': 0},
                  {'order_key': 'T13',
                   'observation_timestamp': '2025-01-10T09:00:00',
                   'target': 0}],
 'cutoff': '2025-01-01T09:00:00',
 'evaluation_end': '2025-01-11T09:00:00',
 'time_policy': 'training < cutoff; cutoff <= evaluation < evaluation_end'}

from datetime import datetime
orders = fixture["group_records"]
train = [row for row in orders if row["customer_group"] in fixture["training_groups"]]
validation = [row for row in orders if row["customer_group"] in fixture["validation_groups"]]
train_groups = {row["customer_group"] for row in train}
validation_groups = {row["customer_group"] for row in validation}
print("partitions:", train, validation)
print("group sets and intersection:", train_groups, validation_groups, train_groups & validation_groups)
assert not train_groups & validation_groups
cutoff = datetime.fromisoformat(fixture["cutoff"])
earlier = [row for row in fixture["time_records"] if datetime.fromisoformat(row["observation_timestamp"]) < cutoff]
end = datetime.fromisoformat(fixture["evaluation_end"])
later = [row for row in fixture["time_records"] if cutoff <= datetime.fromisoformat(row["observation_timestamp"]) < end]
assert all(datetime.fromisoformat(row["observation_timestamp"]) < cutoff for row in earlier)
assert all(cutoff <= datetime.fromisoformat(row["observation_timestamp"]) < end for row in later)
for name, partition in (("group training", train), ("group validation", validation), ("earlier training", earlier), ("later evaluation", later)):
    count = sum(row["target"] for row in partition)
    print(name, "target count, total, proportion:", count, len(partition), count / len(partition) if partition else None)
  annotations: []

### s13 · explainer · A bounded work example
Working rule — 
(example) The group fixture keeps every observation from one customer group together; splitting that group across partitions violates its boundary. Assert group disjointness. In the separate time fixture, check earlier training and the declared later evaluation interval directly. Report target counts over each partition total. That proportion describes the cohort actually evaluated; group disjointness does not prove timestamp ordering. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb4⟧

### s14 · explainer · A distinction to keep
Working rule — 
(misconception) An empty group intersection checks group separation, not whether training timestamps precede evaluation. ⟦C.f1 C.f2 C:tb5⟧

### s15 · check · Judge the representation, labels and splits decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] Evaluation represents unseen customer groups. Which boundary meets that scenario?
  ✔ 0: Every observation in one group remains entirely on one side
      why: Correct. Splitting a common group across sides violates the declared group boundary; randomness alone does not match this scenario.
  ✘ 1: Split each group between training and validation
      why: Splitting a common group across sides violates the declared group boundary; randomness alone does not match this scenario.
  ✘ 2: Ignore groups and justify the split solely as random
      why: Splitting a common group across sides violates the declared group boundary; randomness alone does not match this scenario.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Match the partition boundary to the stated unseen-group evaluation scenario.']  remediation→r05
  MEASURES: C:assert_valid_boundary_and_failure_cases(f6)   anchors=[]
  taught-before-tested: C.f6←s12

### s16 · hands_on · Verify representation, labels and splits
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, stretch, grading=client] Write group_split and time_split. For groups, assign only supplied memberships and assert no shared group. For time, use training < cutoff and evaluation cutoff <= timestamp < evaluation_end. Return training, validation, training_proportion and validation_proportion from each function; each nonempty share is target count / row count. Assign result for the group fixture and time_result for the time fixture. Author assertions for group isolation and cutoff equality. These boundaries represent unseen groups and later orders, respectively; random splitting would not preserve them. Define group_split(records, training_groups, validation_groups) and time_split(records, cutoff, end), where end is evaluation_end. Each returns a dictionary with keys training, validation, training_proportion and validation_proportion. Partition lists must preserve records’ input order.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def and return', 'import and from ... import for required supplied fixture dependencies', 'variable assignment', 'list literals and list comprehensions', 'set literals, set comprehensions, and set()', 'dictionary literals and supplied observation field access', 'for loops', 'if, elif, and else', 'membership tests with in and not in', 'set intersection with & or intersection()', 'comparison operators <, <=, >, >=, ==, and !=', 'Boolean operators and, or, and not', 'len(), sum(), min(), and max()', 'integer, floating-point, string, and Boolean literals', 'arithmetic operators + and /', 'assert predicate', 'calls to the supplied fixture and unit-test interfaces'] blocked=12 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'group_records': [{'order_key': 'A', 'customer_group': 'G1', 'target': 1},
                   {'order_key': 'B', 'customer_group': 'G1', 'target': 0},
                   {'order_key': 'C', 'customer_group': 'G2', 'target': 1}],
 'training_groups': ['G1'],
 'validation_groups': ['G2'],
 'invalid_training_keys': ['A'],
 'invalid_validation_keys': ['B', 'C'],
 'time_records': [{'order_key': 'T1',
                   'observation_timestamp': '2024-12-29T09:00:00',
                   'target': 0},
                  {'order_key': 'T2',
                   'observation_timestamp': '2024-12-30T09:00:00',
                   'target': 0},
                  {'order_key': 'T3',
                   'observation_timestamp': '2024-12-31T09:00:00',
                   'target': 0},
                  {'order_key': 'T4',
                   'observation_timestamp': '2025-01-01T09:00:00',
                   'target': 1},
                  {'order_key': 'T5',
                   'observation_timestamp': '2025-01-02T09:00:00',
                   'target': 1},
                  {'order_key': 'T6',
                   'observation_timestamp': '2025-01-03T09:00:00',
                   'target': 1},
                  {'order_key': 'T7',
                   'observation_timestamp': '2025-01-04T09:00:00',
                   'target': 1},
                  {'order_key': 'T8',
                   'observation_timestamp': '2025-01-05T09:00:00',
                   'target': 0},
                  {'order_key': 'T9',
                   'observation_timestamp': '2025-01-06T09:00:00',
                   'target': 0},
                  {'order_key': 'T10',
                   'observation_timestamp': '2025-01-07T09:00:00',
                   'target': 0},
                  {'order_key': 'T11',
                   'observation_timestamp': '2025-01-08T09:00:00',
                   'target': 0},
                  {'order_key': 'T12',
                   'observation_timestamp': '2025-01-09T09:00:00',
                   'target': 0},
                  {'order_key': 'T13',
                   'observation_timestamp': '2025-01-10T09:00:00',
                   'target': 0}],
 'cutoff': '2025-01-01T09:00:00',
 'evaluation_end': '2025-01-11T09:00:00',
 'time_policy': 'training < cutoff; cutoff <= evaluation < evaluation_end'}

records = FIXTURES['group_records']
training_groups = FIXTURES['training_groups']
validation_groups = FIXTURES['validation_groups']

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'group_records': [{'order_key': 'A', 'customer_group': 'G1', 'target': 1},
                   {'order_key': 'B', 'customer_group': 'G1', 'target': 0},
                   {'order_key': 'C', 'customer_group': 'G2', 'target': 1}],
 'training_groups': ['G1'],
 'validation_groups': ['G2'],
 'invalid_training_keys': ['A'],
 'invalid_validation_keys': ['B', 'C'],
 'time_records': [{'order_key': 'T1',
                   'observation_timestamp': '2024-12-29T09:00:00',
                   'target': 0},
                  {'order_key': 'T2',
                   'observation_timestamp': '2024-12-30T09:00:00',
                   'target': 0},
                  {'order_key': 'T3',
                   'observation_timestamp': '2024-12-31T09:00:00',
                   'target': 0},
                  {'order_key': 'T4',
                   'observation_timestamp': '2025-01-01T09:00:00',
                   'target': 1},
                  {'order_key': 'T5',
                   'observation_timestamp': '2025-01-02T09:00:00',
                   'target': 1},
                  {'order_key': 'T6',
                   'observation_timestamp': '2025-01-03T09:00:00',
                   'target': 1},
                  {'order_key': 'T7',
                   'observation_timestamp': '2025-01-04T09:00:00',
                   'target': 1},
                  {'order_key': 'T8',
                   'observation_timestamp': '2025-01-05T09:00:00',
                   'target': 0},
                  {'order_key': 'T9',
                   'observation_timestamp': '2025-01-06T09:00:00',
                   'target': 0},
                  {'order_key': 'T10',
                   'observation_timestamp': '2025-01-07T09:00:00',
                   'target': 0},
                  {'order_key': 'T11',
                   'observation_timestamp': '2025-01-08T09:00:00',
                   'target': 0},
                  {'order_key': 'T12',
                   'observation_timestamp': '2025-01-09T09:00:00',
                   'target': 0},
                  {'order_key': 'T13',
                   'observation_timestamp': '2025-01-10T09:00:00',
                   'target': 0}],
 'cutoff': '2025-01-01T09:00:00',
 'evaluation_end': '2025-01-11T09:00:00',
 'time_policy': 'training < cutoff; cutoff <= evaluation < evaluation_end'}

records = FIXTURES['group_records']
training_groups = FIXTURES['training_groups']
validation_groups = FIXTURES['validation_groups']

def group_split(records, training_groups, validation_groups):
    train = [row for row in records if row['customer_group'] in training_groups]
    validation = [row for row in records if row['customer_group'] in validation_groups]
    for row in train:
        assert row['customer_group'] not in [v['customer_group'] for v in validation]
    train_count = 0
    train_positive = 0
    for row in train:
        train_count += 1
        train_positive += row['target']
    val_count = 0
    val_positive = 0
    for row in validation:
        val_count += 1
        val_positive += row['target']
    train_share = train_positive / train_count
    val_share = val_positive / val_count
    return {'training':train,'validation':validation,'training_proportion':train_share,'validation_proportion':val_share}
def time_split(records, cutoff, end):
    train = [row for row in records if row['observation_timestamp'] < cutoff]
    validation = [row for row in records if cutoff <= row['observation_timestamp'] and row['observation_timestamp'] < end]
    for row in train:
        assert row['observation_timestamp'] < cutoff
    for row in validation:
        assert cutoff <= row['observation_timestamp'] and row['observation_timestamp'] < end
    train_count = 0
    train_positive = 0
    for row in train:
        train_count += 1
        train_positive += row['target']
    val_count = 0
    val_positive = 0
    for row in validation:
        val_count += 1
        val_positive += row['target']
    return {'training':train,'validation':validation,'training_proportion':train_positive/train_count,'validation_proportion':val_positive/val_count}
result = group_split(records, training_groups, validation_groups)
assert result['training'][0]['customer_group'] == 'G1'
time_result = time_split(FIXTURES['time_records'], FIXTURES['cutoff'], FIXTURES['evaluation_end'])
assert time_result['validation'][0]['observation_timestamp'] == FIXTURES['cutoff']

  test case0 (function_call, visible=True): {"function":"group_split","args":[[{"order_key":"A","customer_group":"G1","target":1},{"order_key":"B","customer_group":"G1","target":0},{"order_key":"C","customer_group":"G2","target":1}],["G1"],["G2"]],"expected":{"training":[{"order_key":"A","customer_group":"G1","target":1},{"order_key":"B","customer_group":"G1","target":0}],"validation":[{"order_key":"C","customer_group":"G2","target":1}],"training_proportion":0.5,"validation_proportion":1}} | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"group_split","args":[[{"order_key":"A","customer_group":"G1","target":1},{"order_key":"B","customer_group":"G1","target":0},{"order_key":"C","customer_group":"G2","target":1},{"order_key":"A_add","customer_group":"G1","target":1}],["G1"],["G2"]],"expected":{"training":[{"order_key":"A","customer_group":"G1","target":1},{"order_key":"B","customer_group":"G1","target":0},{"order_key":"A_add","customer_group":"G1","target":1}],"validation":[{"order_key":"C","customer_group":"G2","targe | on-fail: This fixture does not satisfy the declared return contract.
  test time0 (function_call, visible=False): {"function":"time_split","args":[[{"order_key":"T1","observation_timestamp":"2024-12-29T09:00:00","target":0},{"order_key":"T2","observation_timestamp":"2024-12-30T09:00:00","target":0},{"order_key":"T3","observation_timestamp":"2024-12-31T09:00:00","target":0},{"order_key":"T4","observation_timestamp":"2025-01-01T09:00:00","target":1},{"order_key":"T5","observation_timestamp":"2025-01-02T09:00:00","target":1},{"order_key":"T6","observation_timestamp":"2025-01-03T09:00:00","target":1},{"order_ke | on-fail: The time cutoff, later interval or partition shares are incorrect.
  test time1 (function_call, visible=False): {"function":"time_split","args":[[{"order_key":"T1","observation_timestamp":"2024-12-29T09:00:00","target":0},{"order_key":"T2","observation_timestamp":"2024-12-30T09:00:00","target":0},{"order_key":"T3","observation_timestamp":"2024-12-31T09:00:00","target":0},{"order_key":"T4","observation_timestamp":"2025-01-01T09:00:00","target":1},{"order_key":"T5","observation_timestamp":"2025-01-02T09:00:00","target":1},{"order_key":"T6","observation_timestamp":"2025-01-03T09:00:00","target":1},{"order_ke | on-fail: The time cutoff, later interval or partition shares are incorrect.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"dc936e3578f11c49a57286d6f6bc477fbf17baba5fe4aa76c7086ee8b3d3928e","tests_passed":4}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Apply supplied group memberships and timestamp inequalities while preserving record order.']  remediation→r06
  MEASURES: C:choose_deployment_matched_split_boundaries(f1,f2); C:verify_disjoint_evaluation_groups(f2,f3); C:verify_scenario_matched_time_boundaries(f2,f4); C:interpret_partition_target_proportions(f5); C:assert_valid_boundary_and_failure_cases(f6)   anchors=['practice']
  taught-before-tested: C.f1←s12; C.f2←s12; C.f2←s12; C.f3←s12; C.f2←s12; C.f4←s12; C.f5←s12; C.f6←s12

### s17 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) Sample share and inclusion probability have different denominators. A sample summary is not automatically target-representative. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Equal row counts can hide reordered identities. A dictionary built before duplicate checks can hide a replaced label. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3 B:tb4 B:tb5⟧
(takeaway) An empty group intersection checks group separation, not whether training timestamps precede evaluation. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Fit missing-value imputation using training data only: Next: Fit missing-value imputation using training data only.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Representation, Labels and Splits
(definition) With known target membership, estimate inclusion probability as included category members divided by all target category members. An empty denominator cannot support a rate. Unequal inclusion probabilities affect sample interpretation. A descriptive sample summary is not automatically target-representative. ⟦A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Sample share and inclusion probability have different denominators. A sample summary is not automatically target-representative. ⟦A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.selection_counts cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Representation, Labels and Splits
(definition) Collection or filtering omissions can exclude observations important to the intended prediction population. Compare category count divided by population total in sample and target to identify supported coverage differences. With known target membership, estimate inclusion probability as included category members divided by all target category members. An empty denominator cannot support a rate. Unequal inclusion probabilities affect sample interpretation. A descriptive sample summary is not automatically target-representative. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Sample share and inclusion probability have different denominators. A sample summary is not automatically target-representative. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.selection_counts cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r03 · Contrast: Representation, Labels and Splits
(definition) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f6 B:tb3 B:tb4⟧
(example) Equal row counts can hide reordered identities. A dictionary built before duplicate checks can hide a replaced label. ⟦B.f6 B:tb3 B:tb4⟧
[TABLE ds.observations cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r04 · Contrast: Representation, Labels and Splits
(definition) Match labels to observations or predictions by the intended unique identifier, not incidental row order. Check duplicate IDs before constructing the ID-to-label dictionary: reassignment of an existing key replaces its earlier value. Use observation-ID and label-ID set differences to detect missing labels and labels without observations. Use keyed dictionary lookups to compare labels, observation timestamps and availability timestamps under task-specific acceptance predicates. Information unavailable at the relevant prediction boundary is not an available input to that prediction. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
(definition) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f6 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Equal row counts can hide reordered identities. A dictionary built before duplicate checks can hide a replaced label. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.observations cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r05 · Contrast: Representation, Labels and Splits
(definition) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦C.f6 C:tb3 C:tb4⟧
(example) An empty group intersection checks group separation, not whether training timestamps precede evaluation. ⟦C.f6 C:tb3 C:tb4⟧
[TABLE ds.group_orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r06 · Contrast: Representation, Labels and Splits
(definition) A random split is appropriate only when its sampling interpretation matches evaluation. Group dependence or time ordering can require different boundaries. Keep a common evaluation group on one side; keep time-ordered training observations earlier than the intended later evaluation observations. Represent supplied groups with sets and assert an empty training/validation group intersection. For a time cutoff, select earlier training and the stated later evaluation observations; check timestamp inequalities. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3 C:tb4 C:tb5⟧
(definition) Report each partition's target count divided by its total to describe the population actually evaluated. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦C.f5 C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
(example) An empty group intersection checks group separation, not whether training timestamps precede evaluation. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
[TABLE ds.group_orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: train_test_split(...)
· ops.value: Zone B has lower inclusion and sample share than its target share; the counts establish neither a cause nor inevitable prediction failure._x
· expected.value: Zone B has lower inclusion and sample share than its target share; the counts establish neither a cause nor inevitable prediction failure._x
· constraints.blocked_syntax: sklearn.model_selection.train_test_split()
· constraints.blocked_syntax: sklearn.impute.SimpleImputer()
· constraints.blocked_syntax: sklearn.preprocessing.StandardScaler()
· constraints.blocked_syntax: sklearn.preprocessing.OneHotEncoder()
· constraints.blocked_syntax: sklearn.pipeline.Pipeline()
· constraints.blocked_syntax: sklearn.metrics API calls
· constraints.blocked_syntax: sklearn estimator fit() and predict() calls
· constraints.blocked_syntax: transformer.fit_transform(...)
· constraints.blocked_syntax: transformer.transform(...)
· constraints.blocked_syntax: RandomizedSearchCV(...)
· constraints.blocked_syntax: mlflow.start_run(...)

=========

# EVALUATOR PACKET — Fit and Compose Preprocessing / Fit and Compose Preprocessing / Fit and Compose Preprocessing / Fit and Compose Preprocessing (mle.tile.012_015)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.training_fitted_imputation — Fit missing-value imputation using training data only
B = mle.training_fitted_scaling — Scale numerical features using training-fitted parameters
C = mle.categorical_encoding — Encode categorical features with an unseen-category policy
D = mle.preprocessing_pipeline — Compose a fitted preprocessing pipeline reused across training and bounded inference

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=7
  warn: mle.tile.012_015.s01: prose block without lineage.fact_ids
  warn: mle.tile.012_015.s05/ix.mle.tile.012_015.s05: ADVISORY — syntax descriptors with no detector: ['Boolean operators', 'ColumnTransformer', 'GridSearchCV', 'MinMaxScaler', 'OneHotEncoder', 'OrdinalEncoder', 'Pipeline', 'RandomizedSearchCV', 'StandardScaler', 'array indexing and slicing', 'assert predicate', 'function parameters and calls', 'list literals', 'mlflow', 'numeric and string literals', 'torch']
  warn: mle.tile.012_015.s06: prose block without lineage.fact_ids
  warn: mle.tile.012_015.s11/ix.mle.tile.012_015.s11: ADVISORY — syntax descriptors with no detector: ['ColumnTransformer', 'OneHotEncoder', 'OrdinalEncoder', 'Pipeline', 'arithmetic operators', 'array indexing', 'assert predicate', 'mlflow', 'torch']
  warn: mle.tile.012_015.s12: prose block without lineage.fact_ids
  warn: mle.tile.012_015.s16/ix.mle.tile.012_015.s16: ADVISORY — syntax descriptors with no detector: ['ColumnTransformer', 'Pipeline', 'assert predicate', 'dictionaries', 'equality comparisons', 'for loops', 'function calls and keyword arguments', 'if statements', 'indexing', 'lists and nested lists', 'pytest fixtures and decorators', 'string, numeric and Boolean literals', 'try/except ValueError']
  warn: mle.tile.012_015.s17: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.training_fitted_imputation)   objective: Learn missing-value replacements on training rows and prove validation reuses that state.
A.f1: SimpleImputer learns one replacement value per feature from the data passed to fit, with strategies including mean, median, most_frequent and constant.   [sources: scikit_learn_user_guide#modules/impute.html — 7.4.2 Univariate feature imputation]
A.f2: Use SimpleImputer(strategy=declared_strategy).fit(X_train), then call transform(X_validation) without fitting on validation rows.   [sources: scikit_learn_user_guide#modules/impute.html — 7.4.2 Univariate feature imputation]
A.f3: Inspect statistics_ to check the fitted replacement values and verify they remain unchanged after validation transformation.   [sources: scikit_learn_user_guide#modules/impute.html — 7.4.2 Univariate feature imputation]
A.f4: Compute the arithmetic mean with np.mean(numeric_values, axis=0), so each selected numeric feature column is summarized over rows.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f5: Compute standard deviation with np.std(numeric_values, axis=0, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
A.f6: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Fit and Compose Preprocessing.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.deployment_matched_splits, mle.dataset_cleaning_policy. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Within supplied infrastructure scaffolding, write the required imports and a Python function that fits one SimpleImputer on training distance values using the declared mean strategy, then reuses it on validation distance values. Compute the mean and population standard deviation of the observed training distances, and author assertions for valid, boundary and deliberately incorrect results.  SUCCESS: Observed training distances 2 and 6 produce a columnwise mean of 4 and population standard deviation of 2. Validation distance 100 remains 100, and a missing validation distance becomes 4. A validation input consisting of one missing distance also becomes 4. Assertions verify these outputs and unchanged statistics_ after both transformations. A deliberately incorrect expected replacement fails an assertion under ordinary non-optimized execution.
ASSESSMENT ANCHOR: apply_declared_training_fitted_replacement facts=['f1', 'f2']
ASSESSMENT ANCHOR: verify_validation_preserves_fitted_replacement_state facts=['f2', 'f3']
ASSESSMENT ANCHOR: compute_columnwise_training_mean_and_declared_spread facts=['f4', 'f5']
ASSESSMENT ANCHOR: assert_replacement_output_and_state_invariants facts=['f3', 'f6']

## SOURCE FACTS — B (mle.training_fitted_scaling)   objective: Learn feature scaling from training data and check unchanged validation transformation parameters.
B.f1: StandardScaler centers each feature using its training mean and scales by its training standard deviation when with_mean and with_std are enabled.   [sources: scikit_learn_user_guide#modules/preprocessing.html — 7.3.1 Standardization, or mean removal and variance scaling]
B.f2: Fit StandardScaler on X_train and reuse its transform on X_validation; mean_ and scale_ expose the stored training parameters.   [sources: scikit_learn_user_guide#modules/preprocessing.html — 7.3.1 Standardization, or mean removal and variance scaling]
B.f3: A constant feature cannot be scaled to unit variance, so StandardScaler leaves its scaling factor as 1.   [sources: scikit_learn_user_guide#modules/preprocessing.html — 7.3.1 Standardization, or mean removal and variance scaling]
B.f4: Validation and prediction inputs must receive the transformations used for training, rather than separately fitted transformations.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
B.f5: Compute the arithmetic mean with np.mean(numeric_values, axis=0), so each selected numeric feature column is summarized over rows.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f6: Compute standard deviation with np.std(numeric_values, axis=0, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
B.f7: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Fit and Compose Preprocessing.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.deployment_matched_splits, mle.numpy_shape_dtype, mle.numpy_vectorization. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written NumPy and StandardScaler imports. Within the supplied scaffolding, compute column-wise training means and population standard deviations, fit one scaler on X_train, and transform X_validation without refitting. Author assertions for valid transformations, a constant-feature boundary case, and supplied incorrect-result or changed-state failure cases.  SUCCESS: The function uses training-only fitted parameters. Training distance values 2 and 6 yield mean 4 and population standard deviation 2; validation distance 8 transforms to 2. The constant feature has scale_ equal to 1. Assertions verify numerical results and unchanged mean_ and scale_ after validation transformation, and reject supplied incorrect results or changed fitted parameters.
ASSESSMENT ANCHOR: reuse_training_fitted_scaling_on_unseen_features facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: interpret_constant_feature_scaling facts=['f3']
ASSESSMENT ANCHOR: compute_column_wise_training_scaling_parameters facts=['f5', 'f6']
ASSESSMENT ANCHOR: assert_validation_transformation_preserves_fitted_state facts=['f2', 'f4', 'f7']

## SOURCE FACTS — C (mle.categorical_encoding)   objective: Freeze a categorical representation and test its known, unseen and missing-value behavior.
C.f1: OneHotEncoder learns categories from fit data and represents each categorical value with the corresponding indicator columns.   [sources: scikit_learn_user_guide#modules/preprocessing.html — 7.3.4 Encoding categorical features]
C.f2: Fit the encoder on the training categories, inspect categories_, and use transform for validation inputs without relearning the mapping.   [sources: scikit_learn_user_guide#modules/preprocessing.html — 7.3.4 Encoding categorical features]
C.f3: Choose handle_unknown explicitly: its default error rejects unknown categories, whereas ignore produces all-zero indicators for an unknown category in that feature.   [sources: scikit_learn_user_guide#modules/preprocessing.html — 7.3.4 Encoding categorical features]
C.f4: Missing categorical values can be represented as a learned category when present at fit time; missing values absent from the learned categories follow the unknown-category behavior.   [sources: scikit_learn_user_guide#modules/preprocessing.html — 7.3.4 Encoding categorical features]
C.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
C.f6: Build the training-category dictionary from the fitted encoder’s categories_ and feature names, and keep list-based known, unseen and missing cases aligned with that stored mapping.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Fit and Compose Preprocessing.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.deployment_matched_splits, mle.dataset_schema_validation. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required imports and a Python function that fits OneHotEncoder on training zone rows, explicitly declares handle_unknown, and builds a training-category dictionary from categories_ under the feature name zone. Create reusable list-based known, unseen and missing fixtures, transform them without refitting, and author assertions checking their outputs against the stored mapping. Exercise both error and ignore policies, including missing values present and absent during fit.  SUCCESS: Known categories activate the indicator specified by the stored training mapping. Transformation preserves categories_ and output width. Unseen categories and missing values absent during fit produce all-zero indicators under ignore and raise ValueError under error. Missing values represented during fit activate their learned indicator. Learner-written assertions verify valid, boundary and failure cases.
ASSESSMENT ANCHOR: preserve_training_fitted_category_mapping facts=['f1', 'f2', 'f6']
ASSESSMENT ANCHOR: apply_declared_unknown_and_missing_category_policy facts=['f3', 'f4']
ASSESSMENT ANCHOR: verify_encoding_with_aligned_fixture_assertions facts=['f5', 'f6']

## SOURCE FACTS — D (mle.preprocessing_pipeline)   objective: Assemble one fitted feature/model pipeline and verify its reuse for held-out inference.
D.f1: Construct Pipeline([(name, transformer), ..., (name, estimator)]) to chain transformations with a final estimator.   [sources: scikit_learn_user_guide#modules/compose.html — 7.1.1 Pipeline: chaining estimators; 7.1.4 ColumnTransformer for heterogeneous data]
D.f2: Pipeline.fit fits the transformations and final estimator on training data, while predict applies the fitted transformations before prediction.   [sources: scikit_learn_user_guide#modules/compose.html — 7.1.1 Pipeline: chaining estimators; 7.1.4 ColumnTransformer for heterogeneous data]
D.f3: ColumnTransformer applies declared transformers to selected columns, so categorical and numerical columns can use different operations within the same fitted workflow.   [sources: scikit_learn_user_guide#modules/compose.html — 7.1.1 Pipeline: chaining estimators; 7.1.4 ColumnTransformer for heterogeneous data]
D.f4: Reuse that fitted pipeline for validation and bounded inference rather than fitting a new preprocessing state.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
D.f5: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Fit and Compose Preprocessing.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.training_fitted_imputation, mle.training_fitted_scaling, mle.categorical_encoding, mle.deployment_matched_splits. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a learner-defined Python function with learner-written imports that composes the supplied numerical transformation, category encoder and estimator into one pipeline for distance and zone. Fit it on training data only, then use its prediction path for validation and bounded inference within supplied scaffolding. Author reusable normal, missing-value and malformed fixtures using those columns, with assertions for the supplied valid, boundary and failure expectations and unchanged fitted preprocessing state.  SUCCESS: The function fits one workflow on training data and predicts validation and bounded inference through that same fitted object without further fitting. Assertions confirm the declared transformed representation and output expectations, unchanged fitted preprocessing parameters, the specified missing-value outcome and the specified malformed-input failure.
ASSESSMENT ANCHOR: compose_column_specific_preprocessing_with_an_estimator facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: reuse_training_fitted_transformations_without_refitting facts=['f2', 'f4']
ASSESSMENT ANCHOR: assert_fitted_state_reuse_and_declared_input_outcomes facts=['f4', 'f5']

## DATA ASSETS USED
ds.distance_zone: Exact distance/zone schema — columns: distance(numerical), zone(categorical)
   [0,"north"]
   [2,"south"]
   [100,"north"]
   variant negative_distance: 1 ops; planted: negative_distance(impossible_value)
   variant over_upper_bound: 1 ops; planted: over_upper_bound(impossible_value)
   variant missing_zone_column: 1 ops; planted: 
   variant invalid_zone: 1 ops; planted: invalid_zone(inconsistent_category)
ds.imputation_train: Training distance with missing entry — columns: distance(numerical)
   [2]
   [6]
   [null]
   variant observed_only: 1 ops; planted: 
ds.imputation_validation: Validation distances; do not fit — columns: distance(numerical)
   [100]
   [null]
   variant one_missing: 1 ops; planted: 
ds.scaling_train: Distance and constant feature for scaling — columns: distance(numerical), constant_feature(numerical)
   [2,10]
   [6,10]
ds.scaling_validation: Scaling validation input — columns: distance(numerical), constant_feature(numerical)
   [8.0,10]
ds.zone_cases: Known, unseen and missing zone cases — columns: zone(categorical)
   ["north"]
   ["east"]
   [null]
ds.zone_train: Training-only zone categories — columns: zone(categorical)
   ["north"]
   ["south"]
   variant missing_seen_at_fit: 2 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Build a dataset and minibatch loader; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compose a fitted preprocessing pipeline reused across training and bounded inference; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Define measurable model acceptance criteria from task objectives; Derive task-relevant features from prediction-time information; Detect target or preprocessing leakage across training and prediction boundaries; Document model limitations and foreseeable misuse under an existing risk policy; Encode categorical features with an unseen-category policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific vali

## LESSON, in learner order

### s01 · explainer · Fit and Compose Preprocessing
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(mechanism) SimpleImputer learns a replacement per feature from fit data. Strategies include mean, median, most_frequent and constant. Use SimpleImputer(strategy=declared_strategy).fit(X_train), then transform(X_validation) without fitting validation rows. Inspect statistics_ for fitted replacements and verify validation transformation leaves them unchanged. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use np.mean(numeric_values, axis=0) to average selected numeric feature columns over rows. Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires N-1. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[TABLE ds.imputation_train cols=all ] caption: Training distance with missing entry
[TABLE ds.imputation_validation cols=all ] caption: Validation distances; do not fit
[CODE python]
fixture = {'X_train': [[2], [6], [None]],
 'numeric_values': [[2], [6]],
 'X_validation': [[100], [None]],
 'boundary_missing': [[None]],
 'declared_strategy': 'mean',
 'incorrect_replacement': 2}

import numpy as np
from sklearn.impute import SimpleImputer
X_train = np.array(fixture["X_train"], dtype=float)
X_validation = np.array(fixture["X_validation"], dtype=float)
imputer = SimpleImputer(strategy=fixture["declared_strategy"]).fit(X_train)
before = imputer.statistics_.copy()
transformed = imputer.transform(X_validation)
np.testing.assert_array_equal(imputer.statistics_, before)
observed = X_train[~np.isnan(X_train)].reshape(-1, X_train.shape[1])
print("observed training mean and population spread:", np.mean(observed, axis=0), np.std(observed, axis=0, ddof=0))
print("statistics before, transformed validation, statistics after:", before, transformed, imputer.statistics_)
  annotations: []

### s02 · explainer · A bounded work example
Working rule — 
(example) Under the supplied mean strategy, fit only observed training distances and retain statistics_. Transform validation, including missing entries, without incorporating validation distances into a new replacement. Compare stored state before and after. Keep complete, missing and boundary checks; feature-spread summaries use the stated divisor and are distinct from the chosen imputation strategy. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb4⟧

### s03 · explainer · A distinction to keep
Working rule — 
(misconception) Transform reuses training replacements; fitting validation learns different state. ⟦A.f2 A.f3 A:tb5⟧

### s04 · check · Judge the fit and compose preprocessing decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] After fitting a mean imputer on training distances, what should validation receive?
  ✔ 0: Transform with the existing imputer and verify statistics_ unchanged
      why: Correct. Validation must reuse training statistics; either refitting or fitting combined data changes the information boundary.
  ✘ 1: Fit a new imputer on validation
      why: Validation must reuse training statistics; either refitting or fitting combined data changes the information boundary.
  ✘ 2: Combine training and validation before fitting
      why: Validation must reuse training statistics; either refitting or fitting combined data changes the information boundary.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Trace which partition supplies the fitted imputation statistic.']  remediation→r01
  MEASURES: A:assert_replacement_output_and_state_invariants(f3,f6)   anchors=[]
  taught-before-tested: A.f3←s01; A.f6←s01

### s05 · hands_on · Verify fit and compose preprocessing
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Write the SimpleImputer import and impute(X_train, X_validation, numeric_values, boundary, strategy). Fit once on training only; transform validation and the single-missing boundary without refitting. Compute observed training columnwise mean/std with ddof=0, assert statistics_ stays unchanged and the boundary matches mean. Return [mean, std, validation, boundary_result, statistics_], assign result and assert observed validation preservation and rejection of the supplied incorrect replacement.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'scipy', 'scikit-learn']} constraints.allowed=['import numpy as np', 'from sklearn.impute import SimpleImputer', 'def', 'return', 'variable assignment', 'function parameters and calls', 'numeric and string literals', 'list literals', 'array indexing and slicing', 'np.array', 'np.nan', 'np.mean(numeric_values, axis=0)', 'np.std(numeric_values, axis=0, ddof=0)', 'np.std(numeric_values, axis=0, ddof=1)', 'np.allclose', 'np.array_equal', 'array.copy()', 'SimpleImputer(strategy=declared_strategy)', 'imputer.fit(X_train)', 'imputer.transform(X_validation)', 'imputer.statistics_', 'assert predicate', 'comparison operators', 'Boolean operators'] blocked=11 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'X_train': [[2], [6], [None]],
 'numeric_values': [[2], [6]],
 'X_validation': [[100], [None]],
 'boundary_missing': [[None]],
 'declared_strategy': 'mean',
 'incorrect_replacement': 2}

import numpy as np
X_train = np.array(FIXTURES['X_train'], dtype=float)
X_validation = np.array(FIXTURES['X_validation'], dtype=float)
numeric_values = np.array(FIXTURES['numeric_values'])
boundary = np.array(FIXTURES['boundary_missing'], dtype=float)
strategy = FIXTURES['declared_strategy']

def evaluate(case):
    return impute(np.array(case['X_train'],dtype=float),np.array(case['X_validation'],dtype=float),np.array(case['numeric_values']),np.array(case['boundary_missing'],dtype=float),case['declared_strategy'])

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'X_train': [[2], [6], [None]],
 'numeric_values': [[2], [6]],
 'X_validation': [[100], [None]],
 'boundary_missing': [[None]],
 'declared_strategy': 'mean',
 'incorrect_replacement': 2}

import numpy as np
X_train = np.array(FIXTURES['X_train'], dtype=float)
X_validation = np.array(FIXTURES['X_validation'], dtype=float)
numeric_values = np.array(FIXTURES['numeric_values'])
boundary = np.array(FIXTURES['boundary_missing'], dtype=float)
strategy = FIXTURES['declared_strategy']
def evaluate(case):
    return impute(np.array(case['X_train'],dtype=float),np.array(case['X_validation'],dtype=float),np.array(case['numeric_values']),np.array(case['boundary_missing'],dtype=float),case['declared_strategy'])


from sklearn.impute import SimpleImputer
def impute(X_train, X_validation, numeric_values, boundary, strategy):
    imputer = SimpleImputer(strategy=strategy)
    imputer.fit(X_train)
    before = imputer.statistics_[0]
    validation = imputer.transform(X_validation)
    boundary_result = imputer.transform(boundary)
    assert before == imputer.statistics_[0]
    mean = np.mean(numeric_values,axis=0)
    std = np.std(numeric_values,axis=0,ddof=0)
    assert boundary_result[0][0] == mean[0]
    return [mean,std,validation,boundary_result,imputer.statistics_]
result = impute(X_train,X_validation,numeric_values,boundary,strategy)
assert result[2][0][0] == X_validation[0][0]
assert result[2][1][0] == result[0][0]
assert result[2][1][0] != FIXTURES['incorrect_replacement']

  test case0 (function_call, visible=True): {"function":"evaluate","args":[{"X_train":[[2],[6],[null]],"numeric_values":[[2],[6]],"X_validation":[[100],[null]],"boundary_missing":[[null]],"declared_strategy":"mean","incorrect_replacement":2}],"expected":[[4],[2],[[100],[4]],[[4]],[4]]} | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"evaluate","args":[{"X_train":[[2],[6],[null]],"numeric_values":[[2],[6]],"X_validation":[[200],[null]],"boundary_missing":[[null]],"declared_strategy":"mean","incorrect_replacement":2}],"expected":[[4],[2],[[200],[4]],[[4]],[4]]} | on-fail: This fixture does not satisfy the declared return contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"e62ef8f18e59c08c83663353c58cb2220930d4eeebb6d24e6bd4f92b6f7c2d54","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Keep fitting separate from transforming, and compare fitted state before and after validation.']  remediation→r02
  MEASURES: A:apply_declared_training_fitted_replacement(f1,f2); A:verify_validation_preserves_fitted_replacement_state(f2,f3); A:compute_columnwise_training_mean_and_declared_spread(f4,f5); A:assert_replacement_output_and_state_invariants(f3,f6)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s01; A.f3←s01; A.f6←s01

### s06 · explainer · Fit and Compose Preprocessing
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦B:tb1⟧
(mechanism) With with_mean and with_std enabled, StandardScaler centers each feature by its training mean and scales by its training standard deviation. Fit StandardScaler on X_train and reuse transform on X_validation. Inspect stored parameters through mean_ and scale_. A constant feature cannot become unit variance; StandardScaler leaves its scaling factor at 1. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Validation and prediction must receive training transformations, not separately fitted transformations. Use np.mean(numeric_values, axis=0) to average selected numeric feature columns over rows. Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires N-1. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.scaling_train cols=all ] caption: Distance and constant feature for scaling
[TABLE ds.scaling_validation cols=all ] caption: Scaling validation input
[CODE python]
fixture = {'X_train': [[2, 10], [6, 10]],
 'X_validation': [[8.0, 10]],
 'with_mean': True,
 'with_std': True,
 'ddof': 0,
 'incorrect_transformed_fixture': [[0, 1]]}

import numpy as np
from sklearn.preprocessing import StandardScaler
X_train = np.array(fixture["X_train"], dtype=float)
X_validation = np.array(fixture["X_validation"], dtype=float)
scaler = StandardScaler(with_mean=fixture["with_mean"], with_std=fixture["with_std"]).fit(X_train)
before_mean, before_scale = scaler.mean_.copy(), scaler.scale_.copy()
transformed = scaler.transform(X_validation)
np.testing.assert_array_equal(before_mean, scaler.mean_)
np.testing.assert_array_equal(before_scale, scaler.scale_)
print("training mean and population spread:", np.mean(X_train, axis=0), np.std(X_train, axis=0, ddof=0))
print("mean_, scale_, transformed, unchanged state:", before_mean, before_scale, transformed, scaler.mean_, scaler.scale_)
  annotations: []

### s07 · explainer · Apply and verify
Working rule — 
(mechanism) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f7 B:tb4⟧

### s08 · explainer · A bounded work example
Working rule — 
(example) Use the training distances to compute columnwise mean and population spread, then inspect mean_ and scale_ from the fitted scaler. Apply that same rule to validation rather than recentering the held-out cohort. Confirm fitted parameters remain unchanged. Include the constant feature: its scaling factor stays 1, not a promise of unit variance. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B:tb5⟧

### s09 · explainer · A distinction to keep
Working rule — 
(misconception) Validation reuses training mean and scale; it is not separately centered to its own mean. ⟦B.f3 B.f4 B:tb6⟧

### s10 · check · Judge the fit and compose preprocessing decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] How should a validation input be standardized?
  ✔ 0: Use the scaler fitted only on training and inspect unchanged mean_/scale_
      why: Correct. Refitting changes the parameters, while raw validation omits the transformations used for training.
  ✘ 1: Fit a validation-only scaler
      why: Refitting changes the parameters, while raw validation omits the transformations used for training.
  ✘ 2: Leave validation raw while training is scaled
      why: Refitting changes the parameters, while raw validation omits the transformations used for training.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Identify the source of the fitted mean and scale before transforming validation.']  remediation→r03
  MEASURES: B:assert_validation_transformation_preserves_fitted_state(f2,f4,f7)   anchors=[]
  taught-before-tested: B.f2←s06; B.f4←s06; B.f7←s07

### s11 · hands_on · Verify fit and compose preprocessing
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Implement scale(X_train, X_validation), writing the StandardScaler import. Compute training columnwise mean/std with ddof=0, fit once and transform validation. Assert unchanged mean_/scale_, constant-feature scale 1, and the distance transformation formula. Return [mean, std, validation, mean_, scale_] as result; reject the supplied incorrect result with an assertion.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'scipy', 'scikit-learn']} constraints.allowed=['import numpy as np', 'from sklearn.preprocessing import StandardScaler', 'def', 'return', 'variable assignment', 'array indexing', 'arithmetic operators', 'comparison operators', 'assert predicate', 'np.array', 'np.mean(numeric_values, axis=0)', 'np.std(numeric_values, axis=0, ddof=0)', 'np.std(numeric_values, axis=0, ddof=1)', 'np.allclose', 'array.copy()', 'StandardScaler(with_mean=True, with_std=True)', 'scaler.fit(X_train)', 'scaler.transform(X_train)', 'scaler.transform(X_validation)', 'scaler.mean_', 'scaler.scale_'] blocked=8 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'X_train': [[2, 10], [6, 10]],
 'X_validation': [[8.0, 10]],
 'with_mean': True,
 'with_std': True,
 'ddof': 0,
 'incorrect_transformed_fixture': [[0, 1]]}

import numpy as np
X_train = np.array(FIXTURES['X_train'])
X_validation = np.array(FIXTURES['X_validation'])

def evaluate(case):
    return scale(np.array(case['X_train']),np.array(case['X_validation']))

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'X_train': [[2, 10], [6, 10]],
 'X_validation': [[8.0, 10]],
 'with_mean': True,
 'with_std': True,
 'ddof': 0,
 'incorrect_transformed_fixture': [[0, 1]]}

import numpy as np
X_train = np.array(FIXTURES['X_train'])
X_validation = np.array(FIXTURES['X_validation'])
def evaluate(case):
    return scale(np.array(case['X_train']),np.array(case['X_validation']))


from sklearn.preprocessing import StandardScaler
def scale(X_train,X_validation):
    mean = np.mean(X_train,axis=0)
    std = np.std(X_train,axis=0,ddof=0)
    scaler = StandardScaler(with_mean=True,with_std=True)
    scaler.fit(X_train)
    before_mean = np.array(scaler.mean_)
    before_scale = np.array(scaler.scale_)
    validation = scaler.transform(X_validation)
    assert np.array_equal(scaler.mean_,before_mean)
    assert np.array_equal(scaler.scale_,before_scale)
    assert scaler.scale_[1] == 1
    assert validation[0][0] == (X_validation[0][0]-mean[0])/std[0]
    return [mean,std,validation,scaler.mean_,scaler.scale_]
result = scale(X_train,X_validation)
assert not np.array_equal(result[2],FIXTURES['incorrect_transformed_fixture'])

  test case0 (function_call, visible=True): {"function":"evaluate","args":[{"X_train":[[2,10],[6,10]],"X_validation":[[8.0,10]],"with_mean":true,"with_std":true,"ddof":0,"incorrect_transformed_fixture":[[0,1]]}],"expected":[[4,10],[2,0],[[2,0]],[4,10],[2,1]]} | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"evaluate","args":[{"X_train":[[2,10],[6,10]],"X_validation":[[10,10]],"with_mean":true,"with_std":true,"ddof":0,"incorrect_transformed_fixture":[[0,1]]}],"expected":[[4,10],[2,0],[[3,0]],[4,10],[2,1]]} | on-fail: This fixture does not satisfy the declared return contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"1cb5b0a1b0b39673977ccdee87e853db5594e052f1c33f69f0b19891a44fbaf0","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Compare the distance transformation with the training-derived formula and inspect constant-feature scale.']  remediation→r04
  MEASURES: B:reuse_training_fitted_scaling_on_unseen_features(f1,f2,f4); B:interpret_constant_feature_scaling(f3); B:compute_column_wise_training_scaling_parameters(f5,f6); B:assert_validation_transformation_preserves_fitted_state(f2,f4,f7)   anchors=['practice']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f4←s06; B.f3←s06; B.f5←s06; B.f6←s06; B.f2←s06; B.f4←s06; B.f7←s07

### s12 · explainer · Fit and Compose Preprocessing
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦C:tb1⟧
(mechanism) OneHotEncoder learns categories from fit data and represents values in corresponding indicator columns. Fit training categories, inspect categories_, and transform validation without relearning the mapping. Choose handle_unknown explicitly. Default error rejects unknowns; ignore gives all-zero indicators for an unknown category in that feature. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Missing values can become a learned category if present during fit. Missing values absent from learned categories follow the unknown policy. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. Build a training-category dictionary from categories_ and feature names. Align list-based known, unseen and missing fixtures with that stored mapping. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[TABLE ds.zone_train cols=all ] caption: Training-only zone categories
[TABLE ds.zone_cases cols=all ] caption: Known, unseen and missing zone cases
[CODE python]
fixture = {'X_train': [['north'], ['south']],
 'X_train_missing': [['north'], ['south'], [None]],
 'feature_name': 'zone',
 'cases': {'north': [['north']], 'east': [['east']], 'None': [[None]]},
 'unknown_policies': ['error', 'ignore'],
 'missing_marker': 'Replace JSON null with np.nan when constructing the supplied arrays.'}

import numpy as np
from sklearn.preprocessing import OneHotEncoder
for rows in (fixture["X_train"], fixture["X_train_missing"]):
    training = np.array([[np.nan if value is None else value for value in row] for row in rows], dtype=object)
    for policy in fixture["unknown_policies"]:
        encoder = OneHotEncoder(handle_unknown=policy, sparse_output=False).fit(training)
        mapping = {"zone": encoder.categories_[0].tolist()}
        before = encoder.categories_[0].copy()
        print("training, policy, mapping:", training, policy, mapping)
        for name, rows in fixture["cases"].items():
            try:
                case = np.array([[np.nan if value is None else value for value in row] for row in rows], dtype=object)
                transformed = encoder.transform(case)
                print(name, transformed)
            except ValueError as error:
                print(name, type(error).__name__)
            np.testing.assert_array_equal(before, encoder.categories_[0])
  annotations: []

### s13 · explainer · A bounded work example
Working rule — 
(example) Fit the supplied training zones and store the dictionary in categories_ order under the feature name. Align known, unseen and missing fixtures with it. Compare explicit error and ignore policies for unseen values. A missing value learned during fit differs from one absent at fit. Validation must preserve the mapping; all-zero indicators do not mean an unseen category was learned. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb4⟧

### s14 · explainer · A distinction to keep
Working rule — 
(misconception) An all-zero unseen indicator under ignore is not a newly learned category. Missing treatment depends on what fit saw. ⟦C.f3 C.f4 C:tb5⟧

### s15 · check · Judge the fit and compose preprocessing decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] An unseen zone was absent at fit. Which explicit OneHotEncoder policy yields all-zero indicators for that feature?
  ✔ 0: handle_unknown="ignore"
      why: Correct. Error rejects the unknown category; validation refitting changes the learned mapping rather than applying it.
  ✘ 1: handle_unknown="error"
      why: Error rejects the unknown category; validation refitting changes the learned mapping rather than applying it.
  ✘ 2: Refit the encoder on validation
      why: Error rejects the unknown category; validation refitting changes the learned mapping rather than applying it.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Distinguish the encoder’s unknown-category policy from its fitted category mapping.']  remediation→r05
  MEASURES: C:verify_encoding_with_aligned_fixture_assertions(f5,f6)   anchors=[]
  taught-before-tested: C.f5←s12; C.f6←s12

### s16 · hands_on · Verify fit and compose preprocessing
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Implement encode(X_train, X_train_missing, cases) with OneHotEncoder. Build mapping under zone from fitted categories_. Check known, unseen and absent-at-fit missing cases under ignore; assert output width and categories remain unchanged. Also fit an error-policy encoder and assert supplied attempt returns ValueError for unseen and absent missing. Fit missing-present training and assert missing activates its learned indicator. Return [mapping, known, unseen, missing, learned_missing] as result.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'scipy', 'scikit-learn']} constraints.allowed=['import numpy as np', 'from sklearn.preprocessing import OneHotEncoder', 'def', 'return', 'variable assignment', 'function calls and keyword arguments', 'string, numeric and Boolean literals', 'lists and nested lists', 'dictionaries', 'indexing', 'for loops', 'if statements', 'try/except ValueError', 'assert predicate', 'equality comparisons', 'not', 'len()', 'np.nan', 'np.isnan()', 'np.array_equal()', 'np.all()', 'OneHotEncoder(handle_unknown=..., sparse_output=False)', 'encoder.fit()', 'encoder.transform()', 'encoder.categories_', 'array.copy()', 'array.tolist()', 'array.shape'] blocked=9 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'X_train': [['north'], ['south']],
 'X_train_missing': [['north'], ['south'], [None]],
 'feature_name': 'zone',
 'cases': {'north': [['north']], 'east': [['east']], 'None': [[None]]},
 'unknown_policies': ['error', 'ignore'],
 'missing_marker': 'Replace JSON null with np.nan when constructing the '
                   'supplied arrays.'}

import numpy as np
X_train = FIXTURES['X_train']
X_train_missing = np.array([['north'],['south'],[np.nan]], dtype=object)
cases = {'known':[['north']], 'unseen':[['east']], 'missing':np.array([[np.nan]],dtype=object)}
# The driver catches the declared unknown-category exception only.
def attempt(encoder, rows):
    try:
        return encoder.transform(rows)
    except ValueError:
        return 'ValueError'

def evaluate(case):
    missing_train = np.array([[np.nan if row[0] is None else row[0]] for row in case['X_train_missing']],dtype=object)
    test_cases = {'known':case['cases']['north'],'unseen':case['cases']['east'],'missing':np.array([[np.nan]],dtype=object)}
    return encode(case['X_train'],missing_train,test_cases)

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'X_train': [['north'], ['south']],
 'X_train_missing': [['north'], ['south'], [None]],
 'feature_name': 'zone',
 'cases': {'north': [['north']], 'east': [['east']], 'None': [[None]]},
 'unknown_policies': ['error', 'ignore'],
 'missing_marker': 'Replace JSON null with np.nan when constructing the '
                   'supplied arrays.'}

import numpy as np
X_train = FIXTURES['X_train']
X_train_missing = np.array([['north'],['south'],[np.nan]], dtype=object)
cases = {'known':[['north']], 'unseen':[['east']], 'missing':np.array([[np.nan]],dtype=object)}
# The driver catches the declared unknown-category exception only.
def attempt(encoder, rows):
    try:
        return encoder.transform(rows)
    except ValueError:
        return 'ValueError'
def evaluate(case):
    missing_train = np.array([[np.nan if row[0] is None else row[0]] for row in case['X_train_missing']],dtype=object)
    test_cases = {'known':case['cases']['north'],'unseen':case['cases']['east'],'missing':np.array([[np.nan]],dtype=object)}
    return encode(case['X_train'],missing_train,test_cases)


from sklearn.preprocessing import OneHotEncoder
def encode(X_train,X_train_missing,cases):
    encoder = OneHotEncoder(handle_unknown='ignore',sparse_output=False)
    encoder.fit(X_train)
    before = encoder.categories_[0].tolist()
    mapping = {'zone':encoder.categories_[0].tolist()}
    known = encoder.transform(cases['known'])
    unseen = encoder.transform(cases['unseen'])
    missing = encoder.transform(cases['missing'])
    assert before == encoder.categories_[0].tolist()
    assert known.shape[1] == len(mapping['zone'])
    assert unseen[0][0] == 0 and unseen[0][1] == 0
    assert missing[0][0] == 0 and missing[0][1] == 0
    error_encoder = OneHotEncoder(handle_unknown='error',sparse_output=False)
    error_encoder.fit(X_train)
    assert np.array_equal(error_encoder.transform(cases['known']), known)
    assert attempt(error_encoder,cases['unseen']) == 'ValueError'
    assert attempt(error_encoder,cases['missing']) == 'ValueError'
    missing_encoder = OneHotEncoder(handle_unknown='error',sparse_output=False)
    missing_encoder.fit(X_train_missing)
    learned_missing = missing_encoder.transform(cases['missing'])
    assert learned_missing[0][2] == 1
    return [mapping,known,unseen,missing,learned_missing]
result = encode(X_train,X_train_missing,cases)

  test case0 (function_call, visible=True): {"function":"evaluate","args":[{"X_train":[["north"],["south"]],"X_train_missing":[["north"],["south"],[null]],"feature_name":"zone","cases":{"north":[["north"]],"east":[["east"]],"None":[[null]]},"unknown_policies":["error","ignore"],"missing_marker":"Replace JSON null with np.nan when constructing the supplied arrays."}],"expected":[{"zone":["north","south"]},[[1,0]],[[0,0]],[[0,0]],[[0,0,1]]]} | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"evaluate","args":[{"X_train":[["north"],["south"]],"X_train_missing":[["north"],["south"],[null]],"feature_name":"zone","cases":{"north":[["south"]],"east":[["east"]],"None":[[null]]},"unknown_policies":["error","ignore"],"missing_marker":"Replace JSON null with np.nan when constructing the supplied arrays."}],"expected":[{"zone":["north","south"]},[[0,1]],[[0,0]],[[0,0]],[[0,0,1]]]} | on-fail: This fixture does not satisfy the declared return contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"650f01a4020ede091a4c5e1d5c710894ff7d89527427af071c53d3854c099722","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Compare known, unseen and missing cases with the categories present at fit.']  remediation→r06
  MEASURES: C:preserve_training_fitted_category_mapping(f1,f2,f6); C:apply_declared_unknown_and_missing_category_policy(f3,f4); C:verify_encoding_with_aligned_fixture_assertions(f5,f6)   anchors=['practice']
  taught-before-tested: C.f1←s12; C.f2←s12; C.f6←s12; C.f3←s12; C.f4←s12; C.f5←s12; C.f6←s12

### s17 · explainer · Fit and Compose Preprocessing
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦D:tb1⟧
(mechanism) Construct Pipeline([(name, transformer), ..., (name, estimator)]) to chain transformations with a final estimator. Pipeline.fit fits transformations and the final estimator on training data; predict applies fitted transformations before prediction. ColumnTransformer assigns declared transformers to selected columns, allowing numerical and categorical operations in one fitted workflow. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) Reuse the fitted pipeline for validation and bounded inference; do not fit new preprocessing state. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦D.f4 D.f5 D:tb3⟧
[TABLE ds.distance_zone cols=all ] caption: Exact distance/zone schema
[CODE python]
fixture = {'X_train': [{'distance': 0, 'zone': 'north'},
             {'distance': 2, 'zone': 'south'},
             {'distance': 100, 'zone': 'north'}],
 'y_train': [0, 0, 1],
 'X_validation': [{'distance': 4, 'zone': 'north'}, {'distance': None, 'zone': 'south'}],
 'malformed': [{'distance': 2}],
 'numerical_policy': 'SimpleImputer(strategy="mean") then StandardScaler(with_mean=True, '
                     'with_std=True)',
 'categorical_policy': 'OneHotEncoder(handle_unknown="ignore")',
 'estimator': 'supplied deterministic fixture estimator; not a model-selection exercise'}

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
class FixtureEstimator(ClassifierMixin, BaseEstimator):
    def fit(self, X, y):
        self.n_features_in_ = X.shape[1]
        self.classes_ = np.unique(y)
        return self
    def predict(self, X):
        if X.shape[1] != self.n_features_in_:
            raise ValueError('Fixture width changed')
        return np.zeros(X.shape[0], dtype=int)

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def compose(estimator):
    numerical = Pipeline([("impute", SimpleImputer(strategy="mean")), ("scale", StandardScaler())])
    columns = ColumnTransformer([("distance", numerical, ["distance"]),
                                 ("zone", OneHotEncoder(handle_unknown="ignore"), ["zone"])])
    return Pipeline([("prepare", columns), ("estimate", estimator)])


import pandas as pd
X_train = pd.DataFrame(fixture['X_train'])
X_validation = pd.DataFrame(fixture['X_validation'])
workflow = compose(FixtureEstimator()).fit(X_train, fixture['y_train'])
prepare = workflow.named_steps['prepare']
numerical = prepare.named_transformers_['distance']
encoder = prepare.named_transformers_['zone']
before_statistics = numerical.named_steps['impute'].statistics_.copy()
before_mean = numerical.named_steps['scale'].mean_.copy()
before_scale = numerical.named_steps['scale'].scale_.copy()
before_categories = encoder.categories_[0].copy()
representation = prepare.transform(X_validation)
predictions = workflow.predict(X_validation)
inference = workflow.predict(X_validation.iloc[:1])
np.testing.assert_array_equal(before_statistics, numerical.named_steps['impute'].statistics_)
np.testing.assert_array_equal(before_mean, numerical.named_steps['scale'].mean_)
np.testing.assert_array_equal(before_scale, numerical.named_steps['scale'].scale_)
np.testing.assert_array_equal(before_categories, encoder.categories_[0])
print('selected columns:', prepare.transformers_)
print('validation representation, predictions, bounded inference:', representation, predictions, inference)
print('before and after numerical state:', before_statistics, numerical.named_steps['impute'].statistics_, before_mean, numerical.named_steps['scale'].mean_, before_scale, numerical.named_steps['scale'].scale_)
print('before and after category state:', before_categories, encoder.categories_)
try:
    workflow.predict(pd.DataFrame(fixture['malformed']))
except (ValueError, KeyError) as error:
    print('malformed input:', type(error).__name__)

  annotations: []

### s18 · explainer · A bounded work example
Working rule — 
(example) Assign distance to the declared numerical transformation and zone to the category encoder using ColumnTransformer. Chain this with the final estimator in Pipeline. Fit training once, then predict validation and bounded inference through the same fitted object. Trace a row through selected columns and transformations; separately preparing validation with a new encoder breaks that workflow. Check supplied valid, boundary and failure cases and unchanged fitted state. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D:tb4⟧

### s19 · explainer · A distinction to keep
Working rule — 
(misconception) Predict applies fitted transformations; fitting a new encoder for validation changes the workflow. ⟦D.f2 D.f4 D:tb5⟧

### s20 · check · Judge the fit and compose preprocessing decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] Which workflow preserves a composed pipeline for validation?
  ✔ 0: Fit the composed workflow on training, then call its predict on validation
      why: Correct. Validation must reuse the fitted transformations; refitting or bypassing them does not preserve the training workflow.
  ✘ 1: Fit each validation batch before predicting
      why: Validation must reuse the fitted transformations; refitting or bypassing them does not preserve the training workflow.
  ✘ 2: Bypass fitted transformations and send raw validation to the estimator
      why: Validation must reuse the fitted transformations; refitting or bypassing them does not preserve the training workflow.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Trace which rows reach fit and which calls reuse fitted state.']  remediation→r07
  MEASURES: D:assert_fitted_state_reuse_and_declared_input_outcomes(f4,f5)   anchors=[]
  taught-before-tested: D.f4←s17; D.f5←s17

### s21 · hands_on · Review fit and compose preprocessing
Practice — Read the supplied excerpts in this step and decide which satisfy the stated contract and which are defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each supplied workflow excerpt and decide whether it meets the stated training-only pipeline, reusable prediction, representation/state, missing-value or malformed-input criterion. All constructors, policies and the deterministic fixture estimator are supplied; judge the implementation rather than running or writing it.
  'import json
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.dummy import DummyRegressor
FIXTURES = json.loads('{"X_train": [{"distance": 0, "zone": "north"}, {"distance": 2, "zone": "south"}, {"distance": 100, "zone": "north"}], "y_train": [0, 0, 1], "X_validation": [{"distance": 4, "zone": "north"}, {"distance": null, "zone": "south"}], "malformed": [{"distance": 2}], "numerical_policy": "SimpleImputer(strategy=\\"mean\\") then StandardScaler(with_mean=True, with_std=True)", "categorical_policy": "OneHotEncoder(handle_unknown=\\"ignore\\")", "estimator": "supplied deterministic fixture estimator; not a model-selection exercise"}')
X_train = pd.DataFrame(FIXTURES['X_train'])
y_train = FIXTURES['y_train']
X_validation = pd.DataFrame(FIXTURES['X_validation'])
bounded = pd.DataFrame([FIXTURES['X_validation'][0]])
malformed = pd.DataFrame(FIXTURES['malformed'])
# Supplied deterministic fixture estimator, not a model-selection decision:
estimator = DummyRegressor(strategy='mean')
numeric = Pipeline([('impute', SimpleImputer(strategy='mean')),
                    ('scale', StandardScaler(with_mean=True,with_std=True))])
prep = ColumnTransformer([('numeric',numeric,['distance']),
                         ('zone',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['zone'])])
workflow = Pipeline([('preprocessing',prep),('estimator',estimator)])
workflow.fit(X_train,y_train)
mean_before = prep.named_transformers_['numeric'].named_steps['impute'].statistics_.copy()
scale_before = prep.named_transformers_['numeric'].named_steps['scale'].scale_.copy()
representation = prep.transform(X_validation)
outputs = workflow.predict(X_validation)
bounded_outputs = workflow.predict(bounded)
assert np.array_equal(mean_before,prep.named_transformers_['numeric'].named_steps['impute'].statistics_)
assert np.array_equal(scale_before,prep.named_transformers_['numeric'].named_steps['scale'].scale_)
try:
    workflow.predict(malformed)
    assert False
except ValueError as error:
    malformed_outcome = type(error).__name__ + ': ' + str(error)
missing_outputs = workflow.predict(X_validation.iloc[[1]])
result = {'representation':representation.tolist(),'outputs':outputs.tolist(),'bounded_outputs':bounded_outputs.tolist(),'missing_outputs':missing_outputs.tolist(),'training_imputation':mean_before.tolist(),'training_scale':scale_before.tolist(),'malformed_outcome':malformed_outcome}

# Observed fixture evidence (pinned runtime):
{
  "representation": [
    [
      -0.6427259876700476,
      1,
      0
    ],
    [
      0,
      0,
      1
    ]
  ],
  "outputs": [
    0.3333333333333333,
    0.3333333333333333
  ],
  "bounded_outputs": [
    0.3333333333333333
  ],
  "missing_outputs": [
    0.3333333333333333
  ],
  "training_imputation": [
    34
  ],
  "training_scale": [
    46.676189504571454
  ],
  "malformed_outcome": "ValueError: columns are missing: {'zone'}"
}' -> Meets declared criterion
      feedback: The declared numerical and categorical operations are composed with the supplied estimator and fitted once on training; both prediction paths reuse that object.
  'workflow.fit(X_train, y_train)
workflow.fit(X_validation, y_validation)
validation_predictions = workflow.predict(X_validation)' -> Violates declared criterion
      feedback: Validation refitting violates the required unchanged training-fitted workflow.
  'From the supplied training-fitted workflow:
{
  "representation": [
    [
      -0.6427259876700476,
      1,
      0
    ],
    [
      0,
      0,
      1
    ]
  ],
  "outputs": [
    0.3333333333333333,
    0.3333333333333333
  ],
  "training_imputation": [
    34
  ],
  "training_scale": [
    46.676189504571454
  ]
}
# The supplied representation and output equality predicates pass.
# mean_before and scale_before compare equal after transform and predict; no refit occurs.' -> Meets declared criterion
      feedback: Representation, output and unchanged fitted state are explicitly verified without another fit.
  'Missing-distance case {"distance": null, "zone": "south"}:
missing_predictions = workflow.predict(X_validation.iloc[[1]])
# Observed output: [0.3333333333333333]
# The supplied missing-case outcome equality predicate passes.' -> Meets declared criterion
      feedback: The missing-distance fixture follows the same fitted imputer and prediction path, with its declared outcome checked.
  'Malformed input [{"distance": 2}]:
try:
    workflow.predict(malformed)
    assert False
except ValueError:
    pass
# Observed failure: ValueError: columns are missing: {'zone'}' -> Meets declared criterion
      feedback: The missing required zone is a malformed input; the excerpt asserts the supplied failure rather than silently fabricating a zone.
  '# Missing zone is a declared malformed failure.
malformed['zone'] = 'north'
predictions = workflow.predict(malformed)
# No failure assertion.' -> Violates declared criterion
      feedback: Silently filling the absent feature does not verify the specified malformed-input failure.
  feedback✔: You judged each supplied implementation against its named criterion.  feedback✘: Find the exact operation or field that meets or violates the declared criterion.  hints: ['Read each workflow’s fit and transform calls, then check its stated input criterion.']  remediation→r08
  MEASURES: D:compose_column_specific_preprocessing_with_an_estimator(f1,f2,f3); D:reuse_training_fitted_transformations_without_refitting(f2,f4); D:assert_fitted_state_reuse_and_declared_input_outcomes(f4,f5)   anchors=['practice']
  taught-before-tested: D.f1←s17; D.f2←s17; D.f3←s17; D.f2←s17; D.f4←s17; D.f4←s17; D.f5←s17

### s22 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) Transform reuses training replacements; fitting validation learns different state. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Validation reuses training mean and scale; it is not separately centered to its own mean. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(takeaway) An all-zero unseen indicator under ignore is not a newly learned category. Missing treatment depends on what fit saw. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
(takeaway) Predict applies fitted transformations; fitting a new encoder for validation changes the workflow. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D:tb2 D:tb3 D:tb4 D:tb5⟧
[UP NEXT] Detect target or preprocessing leakage across training and prediction boundaries: Next: Detect target or preprocessing leakage across training and prediction boundaries.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Fit and Compose Preprocessing
(definition) Inspect statistics_ for fitted replacements and verify validation transformation leaves them unchanged. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f3 A.f6 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Transform reuses training replacements; fitting validation learns different state. ⟦A.f3 A.f6 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.imputation_train cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Fit and Compose Preprocessing
(definition) SimpleImputer learns a replacement per feature from fit data. Strategies include mean, median, most_frequent and constant. Use SimpleImputer(strategy=declared_strategy).fit(X_train), then transform(X_validation) without fitting validation rows. Inspect statistics_ for fitted replacements and verify validation transformation leaves them unchanged. Use np.mean(numeric_values, axis=0) to average selected numeric feature columns over rows. Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires N-1. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3 A:tb4 A:tb5⟧
(definition) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f6 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Transform reuses training replacements; fitting validation learns different state. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.imputation_train cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r03 · Contrast: Fit and Compose Preprocessing
(definition) Fit StandardScaler on X_train and reuse transform on X_validation. Inspect stored parameters through mean_ and scale_. Validation and prediction must receive training transformations, not separately fitted transformations. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f2 B.f4 B.f7 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Validation reuses training mean and scale; it is not separately centered to its own mean. ⟦B.f2 B.f4 B.f7 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[TABLE ds.scaling_train cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r04 · Contrast: Fit and Compose Preprocessing
(definition) With with_mean and with_std enabled, StandardScaler centers each feature by its training mean and scales by its training standard deviation. Fit StandardScaler on X_train and reuse transform on X_validation. Inspect stored parameters through mean_ and scale_. A constant feature cannot become unit variance; StandardScaler leaves its scaling factor at 1. Validation and prediction must receive training transformations, not separately fitted transformations. Use np.mean(numeric_values, axis=0) to average selected numeric feature columns over rows. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(definition) Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires N-1. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f6 B.f7 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
(example) Validation reuses training mean and scale; it is not separately centered to its own mean. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
[TABLE ds.scaling_train cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r05 · Contrast: Fit and Compose Preprocessing
(definition) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. Build a training-category dictionary from categories_ and feature names. Align list-based known, unseen and missing fixtures with that stored mapping. ⟦C.f5 C.f6 C:tb3 C:tb4⟧
(example) An all-zero unseen indicator under ignore is not a newly learned category. Missing treatment depends on what fit saw. ⟦C.f5 C.f6 C:tb3 C:tb4⟧
[TABLE ds.zone_train cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r06 · Contrast: Fit and Compose Preprocessing
(definition) OneHotEncoder learns categories from fit data and represents values in corresponding indicator columns. Fit training categories, inspect categories_, and transform validation without relearning the mapping. Choose handle_unknown explicitly. Default error rejects unknowns; ignore gives all-zero indicators for an unknown category in that feature. Missing values can become a learned category if present during fit. Missing values absent from learned categories follow the unknown policy. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3 C:tb4 C:tb5⟧
(definition) Build a training-category dictionary from categories_ and feature names. Align list-based known, unseen and missing fixtures with that stored mapping. ⟦C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
(example) An all-zero unseen indicator under ignore is not a newly learned category. Missing treatment depends on what fit saw. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3 C:tb4 C:tb5⟧
[TABLE ds.zone_train cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r07 · Contrast: Fit and Compose Preprocessing
(definition) Reuse the fitted pipeline for validation and bounded inference; do not fit new preprocessing state. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦D.f4 D.f5 D:tb3 D:tb4 D:tb5⟧
(example) Predict applies fitted transformations; fitting a new encoder for validation changes the workflow. ⟦D.f4 D.f5 D:tb3 D:tb4 D:tb5⟧
[TABLE ds.distance_zone cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r08 · Contrast: Fit and Compose Preprocessing
(definition) Construct Pipeline([(name, transformer), ..., (name, estimator)]) to chain transformations with a final estimator. Pipeline.fit fits transformations and the final estimator on training data; predict applies fitted transformations before prediction. ColumnTransformer assigns declared transformers to selected columns, allowing numerical and categorical operations in one fitted workflow. Reuse the fitted pipeline for validation and bounded inference; do not fit new preprocessing state. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D:tb2 D:tb3 D:tb4 D:tb5⟧
(example) Predict applies fitted transformations; fitting a new encoder for validation changes the workflow. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D:tb2 D:tb3 D:tb4 D:tb5⟧
[TABLE ds.distance_zone cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

=========

# EVALUATOR PACKET — Prevent Prediction-Time Leakage / Prevent Prediction-Time Leakage (mle.tile.016_017)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_boundary_leakage — Detect target or preprocessing leakage across training and prediction boundaries
B = mle.leakage_safe_features — Derive task-relevant features from prediction-time information

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=5
  warn: mle.tile.016_017.s01: prose block without lineage.fact_ids
  warn: mle.tile.016_017.s05/ix.mle.tile.016_017.s05: ADVISORY — syntax descriptors with no detector: ['array or table indexing and column selection', 'assert predicate statements', 'boolean operators', 'calls to supplied fixture and workflow interfaces', 'def with parameters', 'deployment or prediction-service client construction', 'held-out preprocessing transform calls', 'import statements for the required fixture and preprocessing dependencies', 'list and tuple literals', 'new estimator construction or learner-authored estimator training', 'return statements', 'training-only preprocessing fit calls', 'training-only preprocessing fit_transform calls']
  warn: mle.tile.016_017.s06: prose block without lineage.fact_ids
  warn: mle.tile.016_017.s11/ix.mle.tile.016_017.s11: ADVISORY — syntax descriptors with no detector: ['assert actual == expected', 'dictionary literals with available_at and value keys', 'for record in accepted:', 'function calls', 'integer literals', 'list concatenation with +', 'list literals', 'return total', 'total = 0']
  warn: plan: mle.tile.016_017.s11 was planned to measure mle.leakage_safe_features#assessment:select_lookup_value_at_recorded_boundary but its interaction does not

## SOURCE FACTS — A (mle.prediction_boundary_leakage)   objective: Find and repair one evaluation-information leak without changing the evaluation boundary.
A.f1: Leakage uses information not available at prediction time when building a model and can make held-out performance estimates overly optimistic.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f2: Audit which rows and fields reach fit operations and each prediction, then remove held-out or future information from those operations.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f3: Separate training and evaluation before fitting preprocessing, and call transform rather than fit or fit_transform on held-out inputs.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f4: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Prevent Prediction-Time Leakage.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition, mle.deployment_matched_splits, mle.preprocessing_pipeline. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Audit the supplied order workflow against its acceptance-time prediction contract. In a learner-defined Python function with learner-written imports, exclude the eventual-arrival field from prediction inputs and ensure preprocessing fits only the designated training rows. Write assert checks using the supplied valid, boundary and failure fixtures.  SUCCESS: The learner localizes each information-boundary defect. The same assertions fail on the leaked workflow and pass after correction, establishing that prediction inputs contain only decision-available fields, preprocessing fits only training rows, and held-out inputs receive transform without refitting.
ASSESSMENT ANCHOR: identify_target_and_future_information_leakage facts=['f1', 'f2']
ASSESSMENT ANCHOR: localize_held_out_information_in_preprocessing_fits facts=['f2', 'f3']
ASSESSMENT ANCHOR: verify_boundary_cases_with_assert_predicates facts=['f4']

## SOURCE FACTS — B (mle.leakage_safe_features)   objective: Compute a prediction-time feature using only records available at that time.
B.f1: A feature for a prediction must be derived only from information available when that prediction is made.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
B.f2: A list comprehension of the form [row for row in records if row["available_at"] <= prediction_time] selects the records available at the declared boundary.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f3: A changing lookup table can yield different training and serving values, so use values from the relevant recorded boundary rather than assuming the latest table is historical.   [sources: google_rules_of_ml#Rule #31: Beware that if you join data from a table at training and serving time, the data in the table may change.]
B.f4: Test the feature on the original records and on records augmented with later unavailable observations, asserting that the earlier feature is unchanged.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
B.f5: Apply the declared arithmetic feature to the time-filtered records only; for a sum, initialize total = 0 and accumulate total += record["value"] over the accepted list.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Prevent Prediction-Time Leakage.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_boundary_leakage, mle.deployment_matched_splits, mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function that accepts records and prediction_time, filters records with a list comprehension using available_at <= prediction_time, and sums only accepted value entries. Write the required datetime import for the supplied timestamp fixtures. Within the supplied infrastructure scaffolding, author assertions and verify the function with supplied unit-test fixtures, including a record exactly at the boundary and an added later observation.  SUCCESS: The available values 2 and 3 produce 5. Adding the later value 7 leaves the earlier feature at 5. A record exactly at prediction_time is included, and the learner-written assertions and supplied feature fixtures pass.
ASSESSMENT ANCHOR: derive_feature_from_prediction_time_records facts=['f1', 'f2', 'f5']
ASSESSMENT ANCHOR: select_lookup_value_at_recorded_boundary facts=['f1', 'f3']
ASSESSMENT ANCHOR: verify_feature_invariance_to_later_observations facts=['f2', 'f4', 'f5']

## DATA ASSETS USED
ds.feature_records: Timestamp-bounded sum records — columns: available_at(datetime), value(numerical)
   ["2025-01-01T09:00:00",2]
   ["2025-01-01T09:30:00",3]
   variant later_record: 3 ops; planted: 
ds.orders: orders-b.csv — columns: order_key(identifier), distance(numerical), zone(categorical), eventual_arrival(datetime)
   ["0012",2,"north","2025-01-01T09:45:00"]
   ["0013",4,"south","2025-01-01T10:20:00"]
   ["0014",6,"north","2025-01-01T11:31:00"]
   ["0015",0,"south","2025-01-01T12:30:00"]
   ["0016",100,"north","2025-01-01T13:50:00"]
   ["0017",4,"south","2025-01-01T14:10:00"]
   variant missing_distance: 1 ops; planted: missing_distance(missing_value)
   variant duplicate_order: 1 ops; planted: duplicate_order(duplicate_row)
   variant mixed_distance: 1 ops; planted: mixed_distance(wrong_type)
   variant zone_spelling: 1 ops; planted: zone_spelling(inconsistent_category)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Define measurable model acceptance criteria from task objectives; Derive task-relevant features from prediction-time information; Document model limitations and foreseeable misuse under an existing risk policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Fit and predict with a bounded scikit-learn baseline workflow; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction er

## LESSON, in learner order

### s01 · explainer · Prevent Prediction-Time Leakage
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(mechanism) Leakage uses information unavailable at prediction time to build a model and can make held-out performance estimates overly optimistic. Trace rows and fields reaching fit and prediction, then remove held-out or future information from those operations. Separate training and evaluation before fitting preprocessing. On held-out inputs call transform, not fit or fit_transform. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f4 A:tb3⟧
[TABLE ds.orders cols=all ] caption: orders-b.csv
[CODE python]
fixture = {'training': [{'order_key': '0012',
               'distance': 2,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T09:45:00'},
              {'order_key': '0013',
               'distance': 4,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T10:20:00'},
              {'order_key': '0014',
               'distance': 6,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T11:31:00'}],
 'held_out': [{'order_key': '0015',
               'distance': 0,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T12:30:00'},
              {'order_key': '0016',
               'distance': 100,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T13:50:00'},
              {'order_key': '0017',
               'distance': 4,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T14:10:00'}],
 'permitted_features': ['distance', 'zone'],
 'future_field': 'eventual_arrival',
 'prediction_time': 'acceptance',
 'failure_fit_rows': [{'order_key': '0012',
                       'distance': 2,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T09:45:00'},
                      {'order_key': '0013',
                       'distance': 4,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T10:20:00'},
                      {'order_key': '0014',
                       'distance': 6,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T11:31:00'},
                      {'order_key': '0015',
                       'distance': 0,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T12:30:00'},
                      {'order_key': '0016',
                       'distance': 100,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T13:50:00'},
                      {'order_key': '0017',
                       'distance': 4,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T14:10:00'}],
 'failure_features': ['distance', 'zone', 'eventual_arrival']}

import pandas as pd
from sklearn.impute import SimpleImputer
permitted = fixture["permitted_features"]
assert fixture["future_field"] not in permitted
train = pd.DataFrame(fixture["training"])
held_out = pd.DataFrame(fixture["held_out"])
fit_ids = train["order_key"].tolist()
assert set(fit_ids).isdisjoint(held_out["order_key"])
print("fit row trace:", fit_ids, "prediction input columns:", permitted)
# The distance preprocessing fit receives only designated training rows.
preprocessor = SimpleImputer(strategy="mean").fit(train[["distance"]])
before = preprocessor.statistics_.copy()
transformed = preprocessor.transform(held_out[["distance"]])
assert (before == preprocessor.statistics_).all()
print("held-out transform:", transformed)
print("contrasts: future field and held-out fit-row trace:", fixture["failure_features"],
      [row["order_key"] for row in fixture["failure_fit_rows"]])
  annotations: []

### s02 · explainer · A bounded work example
Working rule — 
(example) At order acceptance, the eventual-arrival field is unavailable. Remove it from prediction inputs. Independently inspect preprocessing fit rows: fitting on training plus held-out rows violates that boundary even if the estimator fits training only. Split first and transform held-out inputs with training state. Check field selection and fit-row membership explicitly; separate filenames alone do not establish the boundary. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · A distinction to keep
Working rule — 
(misconception) Excluding future fields does not repair a preprocessing fit that still sees held-out rows; check both boundaries. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s04 · check · Judge the prevent prediction-time leakage decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] For an acceptance-time task, which change removes both supplied information-boundary defects?
  ✔ 0: Exclude eventual arrival from inputs and fit preprocessing on training only
      why: Correct. Each alternative leaves one defect: held-out fit rows or a future input.
  ✘ 1: Exclude eventual arrival but fit on combined training and held-out rows
      why: Each alternative leaves one defect: held-out fit rows or a future input.
  ✘ 2: Fit on training only but keep eventual arrival as an input
      why: Each alternative leaves one defect: held-out fit rows or a future input.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Trace both future input fields and held-out rows reaching preprocessing fits.']  remediation→r01
  MEASURES: A:identify_target_and_future_information_leakage(f1,f2)   anchors=[]
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · hands_on · Verify prevent prediction-time leakage
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, core, grading=client] Correct the acceptance-time workflow in correct(training, held_out, features). Select only the supplied distance and zone fields on each side, fit_transform training only and transform held-out without refitting. Invoke verify for input columns and fit-row IDs; assert fitted numeric state is unchanged. Return [training_representation, held_out_representation, training_mean] as result. Use the same boundary assertions on the future-field and combined-fit-row failure fixtures: they must fail before correction and pass for this corrected workflow.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas', 'scipy', 'scikit-learn']} constraints.allowed=['import statements for the required fixture and preprocessing dependencies', 'def with parameters', 'return statements', 'variable assignment', 'calls to supplied fixture and workflow interfaces', 'array or table indexing and column selection', 'list and tuple literals', 'comparison operators', 'boolean operators', 'assert predicate statements', 'training-only preprocessing fit calls', 'training-only preprocessing fit_transform calls', 'held-out preprocessing transform calls'] blocked=7 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'training': [{'order_key': '0012',
               'distance': 2,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T09:45:00'},
              {'order_key': '0013',
               'distance': 4,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T10:20:00'},
              {'order_key': '0014',
               'distance': 6,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T11:31:00'}],
 'held_out': [{'order_key': '0015',
               'distance': 0,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T12:30:00'},
              {'order_key': '0016',
               'distance': 100,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T13:50:00'},
              {'order_key': '0017',
               'distance': 4,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T14:10:00'}],
 'permitted_features': ['distance', 'zone'],
 'future_field': 'eventual_arrival',
 'prediction_time': 'acceptance',
 'failure_fit_rows': [{'order_key': '0012',
                       'distance': 2,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T09:45:00'},
                      {'order_key': '0013',
                       'distance': 4,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T10:20:00'},
                      {'order_key': '0014',
                       'distance': 6,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T11:31:00'},
                      {'order_key': '0015',
                       'distance': 0,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T12:30:00'},
                      {'order_key': '0016',
                       'distance': 100,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T13:50:00'},
                      {'order_key': '0017',
                       'distance': 4,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T14:10:00'}],
 'failure_features': ['distance', 'zone', 'eventual_arrival']}

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
training = pd.DataFrame(FIXTURES['training'])
held_out = pd.DataFrame(FIXTURES['held_out'])
features = FIXTURES['permitted_features']
# Supplied factory is not an exercise in transformer selection.
def workflow():
    return ColumnTransformer([('numeric',StandardScaler(),['distance']),('zone',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['zone'])])
def verify(train_columns, held_columns, fit_keys, expected_keys):
    assert list(train_columns) == features
    assert list(held_columns) == features
    assert list(fit_keys) == list(expected_keys)

from sklearn import preprocessing
import numpy as np
def evaluate(case):
    return correct(pd.DataFrame(case['training']), pd.DataFrame(case['held_out']), case['permitted_features'])
# The same verification predicate is applied to both declared leaked boundaries.
def rejected_boundary(train_columns, held_columns, keys, expected):
    try:
        verify(train_columns, held_columns, keys, expected)
    except AssertionError:
        return True
    return False
failure_fit_keys = [row['order_key'] for row in FIXTURES['failure_fit_rows']]
# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'training': [{'order_key': '0012',
               'distance': 2,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T09:45:00'},
              {'order_key': '0013',
               'distance': 4,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T10:20:00'},
              {'order_key': '0014',
               'distance': 6,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T11:31:00'}],
 'held_out': [{'order_key': '0015',
               'distance': 0,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T12:30:00'},
              {'order_key': '0016',
               'distance': 100,
               'zone': 'north',
               'eventual_arrival': '2025-01-01T13:50:00'},
              {'order_key': '0017',
               'distance': 4,
               'zone': 'south',
               'eventual_arrival': '2025-01-01T14:10:00'}],
 'permitted_features': ['distance', 'zone'],
 'future_field': 'eventual_arrival',
 'prediction_time': 'acceptance',
 'failure_fit_rows': [{'order_key': '0012',
                       'distance': 2,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T09:45:00'},
                      {'order_key': '0013',
                       'distance': 4,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T10:20:00'},
                      {'order_key': '0014',
                       'distance': 6,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T11:31:00'},
                      {'order_key': '0015',
                       'distance': 0,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T12:30:00'},
                      {'order_key': '0016',
                       'distance': 100,
                       'zone': 'north',
                       'eventual_arrival': '2025-01-01T13:50:00'},
                      {'order_key': '0017',
                       'distance': 4,
                       'zone': 'south',
                       'eventual_arrival': '2025-01-01T14:10:00'}],
 'failure_features': ['distance', 'zone', 'eventual_arrival']}

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
training = pd.DataFrame(FIXTURES['training'])
held_out = pd.DataFrame(FIXTURES['held_out'])
features = FIXTURES['permitted_features']
# Supplied factory is not an exercise in transformer selection.
def workflow():
    return ColumnTransformer([('numeric',StandardScaler(),['distance']),('zone',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['zone'])])
def verify(train_columns, held_columns, fit_keys, expected_keys):
    assert list(train_columns) == features
    assert list(held_columns) == features
    assert list(fit_keys) == list(expected_keys)
from sklearn import preprocessing
import numpy as np
def evaluate(case):
    return correct(pd.DataFrame(case['training']), pd.DataFrame(case['held_out']), case['permitted_features'])
# The same verification predicate is applied to both declared leaked boundaries.
def rejected_boundary(train_columns, held_columns, keys, expected):
    try:
        verify(train_columns, held_columns, keys, expected)
    except AssertionError:
        return True
    return False
failure_fit_keys = [row['order_key'] for row in FIXTURES['failure_fit_rows']]

def correct(training,held_out,features):
    X_train = training[features]
    X_held = held_out[features]
    preprocessing = workflow()
    train_result = preprocessing.fit_transform(X_train)
    before = preprocessing.named_transformers_['numeric'].mean_.copy()
    held_result = preprocessing.transform(X_held)
    verify(X_train.columns,X_held.columns,training['order_key'],training['order_key'])
    assert np.array_equal(preprocessing.named_transformers_['numeric'].mean_, before)
    return [train_result,held_result,before]
result = correct(training,held_out,features)

assert rejected_boundary(FIXTURES['failure_features'], features, training['order_key'], training['order_key'])
assert rejected_boundary(features, features, failure_fit_keys, training['order_key'])

  test case0 (function_call, visible=True): {"function":"evaluate","args":[{"training":[{"order_key":"0012","distance":2,"zone":"north","eventual_arrival":"2025-01-01T09:45:00"},{"order_key":"0013","distance":4,"zone":"south","eventual_arrival":"2025-01-01T10:20:00"},{"order_key":"0014","distance":6,"zone":"north","eventual_arrival":"2025-01-01T11:31:00"}],"held_out":[{"order_key":"0015","distance":0,"zone":"south","eventual_arrival":"2025-01-01T12:30:00"},{"order_key":"0016","distance":100,"zone":"north","eventual_arrival":"2025-01-01T13 | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"evaluate","args":[{"training":[{"order_key":"0012","distance":2,"zone":"north","eventual_arrival":"2025-01-01T09:45:00"},{"order_key":"0013","distance":4,"zone":"south","eventual_arrival":"2025-01-01T10:20:00"},{"order_key":"0014","distance":6,"zone":"north","eventual_arrival":"2025-01-01T11:31:00"}],"held_out":[{"order_key":"0015","distance":8,"zone":"south","eventual_arrival":"2025-01-01T12:30:00"},{"order_key":"0016","distance":100,"zone":"north","eventual_arrival":"2025-01-01T13 | on-fail: This fixture does not satisfy the declared return contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"61bf4789a2c8f31ef7baa24ba5816bbcba9b567c4227d749d1502eb8c10d38c9","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check selected columns and fit-row IDs independently before checking unchanged fitted state.']  remediation→r02
  MEASURES: A:localize_held_out_information_in_preprocessing_fits(f2,f3); A:verify_boundary_cases_with_assert_predicates(f4)   anchors=['practice']
  taught-before-tested: A.f2←s01; A.f3←s01; A.f4←s01

### s06 · explainer · Prevent Prediction-Time Leakage
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦B:tb1⟧
(mechanism) Derive prediction features only from information available when the prediction is made. Select available records with [row for row in records if row["available_at"] <= prediction_time]. Changing lookup tables can produce different training and serving values. Use the value at the relevant recorded boundary, not an assumed historical latest value. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Compare the feature on original records and on records augmented with later unavailable observations; assert the earlier feature is unchanged. Apply arithmetic only to time-filtered records. For a sum, initialize total = 0 and accumulate total += record["value"] over the accepted list. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.feature_records cols=all ] caption: Timestamp-bounded sum records
[CODE python]
fixture = {'records': [{'available_at': '2025-01-01T09:00:00', 'value': 2},
             {'available_at': '2025-01-01T09:30:00', 'value': 3}],
 'augmented_records': [{'available_at': '2025-01-01T09:00:00', 'value': 2},
                       {'available_at': '2025-01-01T09:30:00', 'value': 3},
                       {'available_at': '2025-01-01T09:30:01', 'value': 7}],
 'prediction_time': '2025-01-01T09:30:00',
 'empty': [],
 'policy': 'available_at <= prediction_time; timestamps are ISO strings converted with '
           'datetime.fromisoformat'}

from datetime import datetime

def derive(records, boundary):
    prediction_time = datetime.fromisoformat(boundary)
    dated = [dict(row, available_at=datetime.fromisoformat(row["available_at"])) for row in records]
    accepted = [row for row in dated if row["available_at"] <= prediction_time]
    total = 0
    for record in accepted:
        total += record["value"]
    return accepted, total

original, total = derive(fixture["records"], fixture["prediction_time"])
augmented, later_total = derive(fixture["augmented_records"], fixture["prediction_time"])
assert original == augmented
assert total == later_total
print("boundary:", fixture["prediction_time"])
print("original input, augmented input:", fixture["records"], fixture["augmented_records"])
print("accepted, total, augmented accepted, augmented total:", original, total, augmented, later_total)
  annotations: []

### s07 · explainer · A bounded work example
Working rule — 
(example) Filter records by availability before summing their values. Compare original and later-augmented records at the same prediction time; the accepted list and earlier feature must not change. A record exactly on the boundary follows the supplied <= predicate. If a changing lookup contributes, select its value at the recorded boundary rather than assuming the latest lookup is historical. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s08 · explainer · A distinction to keep
Working rule — 
(misconception) Removing timestamps after arithmetic cannot remove a later record's contribution. Filter before summing. ⟦B.f1 B.f2 B.f3 B.f5 B:tb5⟧

### s09 · video · Trace the working rule
Optional walkthrough — 
[VIDEO Keep feature inputs inside the prediction boundary] bridge-before: Watch how earlier values become prediction inputs. Interpret the speaker’s phrase “at the time of the target” through the explicit example: predicting t+1 while currently at t. | bridge-after: The clip establishes the availability rule. The text supplies what it does not demonstrate: timestamp-filtering code, historical lookup handling, unchanged-feature assertions after adding later observations, and accumulation over accepted records.
  - 9QtL7m3YS9I 253-335s facts=['f1'] label: Use known earlier values to predict the next time step | summary: To predict sales at time t+1 while currently at time t, construct features from values already known, such as those at t and t−1. These earlier-value inputs are called lag features. For a prediction of sales at time t, the corresponding inputs instead start at t−1 and t−2. The available history shifts with each prediction boundary. Using future information would leak information into an earlier prediction.

### s10 · check · Judge the prevent prediction-time leakage decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, core, grading=client] An earlier feature was calculated using records and a lookup snapshot available at prediction_time. Later unavailable records are added and the latest lookup changes. Which treatment preserves the earlier prediction boundary?
  ✔ 0: Exclude the later records and retain the lookup value recorded at the earlier boundary.
      why: Correct. Excluding later unavailable records and retaining the recorded lookup snapshot preserves the earlier prediction boundary.
  ✘ 1: Exclude later records but substitute the latest lookup value
      why: Substituting the changed latest lookup admits information unavailable at the earlier boundary, even though later records are excluded.
  ✘ 2: Retain the earlier lookup value but include later records.
      why: Including later unavailable records admits information unavailable at the earlier boundary, even though the earlier lookup value is retained.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Trace the availability boundary for records and the lookup snapshot separately.']  remediation→r03
  MEASURES: B:verify_feature_invariance_to_later_observations(f2,f4,f5); B:select_lookup_value_at_recorded_boundary(f1,f3)   anchors=[]
  taught-before-tested: B.f2←s06; B.f4←s06; B.f5←s06; B.f1←s06; B.f3←s06

### s11 · hands_on · Verify prevent prediction-time leakage
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, stretch, grading=client] Implement feature(records, prediction_time). Select available_at <= prediction_time with a list comprehension, initialize total and accumulate only accepted value entries. Return total and assign result. Author assertions for the added-later record, empty input and exact-boundary inclusion; use the supplied datetime fixtures, never a latest lookup without a boundary.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['from datetime import datetime', 'def function_name(records, prediction_time):', 'return total', 'variable assignment', 'integer literals', 'datetime(...)', 'list literals', 'dictionary literals with available_at and value keys', 'row["available_at"]', 'record["value"]', '[row for row in records if row["available_at"] <= prediction_time]', 'total = 0', 'for record in accepted:', 'total += record["value"]', 'list concatenation with +', 'function calls', 'assert actual == expected'] blocked=7 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'records': [{'available_at': '2025-01-01T09:00:00', 'value': 2},
             {'available_at': '2025-01-01T09:30:00', 'value': 3}],
 'augmented_records': [{'available_at': '2025-01-01T09:00:00', 'value': 2},
                       {'available_at': '2025-01-01T09:30:00', 'value': 3},
                       {'available_at': '2025-01-01T09:30:01', 'value': 7}],
 'prediction_time': '2025-01-01T09:30:00',
 'empty': [],
 'policy': 'available_at <= prediction_time; timestamps are ISO strings '
           'converted with datetime.fromisoformat'}

from datetime import datetime
records = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in FIXTURES['records']]
augmented = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in FIXTURES['augmented_records']]
prediction_time = datetime.fromisoformat(FIXTURES['prediction_time'])

def evaluate(case):
    rs = [{'available_at':datetime.fromisoformat(r['available_at']),'value':r['value']} for r in case['records']]
    return feature(rs,datetime.fromisoformat(case['prediction_time']))
# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'records': [{'available_at': '2025-01-01T09:00:00', 'value': 2},
             {'available_at': '2025-01-01T09:30:00', 'value': 3}],
 'augmented_records': [{'available_at': '2025-01-01T09:00:00', 'value': 2},
                       {'available_at': '2025-01-01T09:30:00', 'value': 3},
                       {'available_at': '2025-01-01T09:30:01', 'value': 7}],
 'prediction_time': '2025-01-01T09:30:00',
 'empty': [],
 'policy': 'available_at <= prediction_time; timestamps are ISO strings '
           'converted with datetime.fromisoformat'}

from datetime import datetime
records = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in FIXTURES['records']]
augmented = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in FIXTURES['augmented_records']]
prediction_time = datetime.fromisoformat(FIXTURES['prediction_time'])
def evaluate(case):
    rs = [{'available_at':datetime.fromisoformat(r['available_at']),'value':r['value']} for r in case['records']]
    return feature(rs,datetime.fromisoformat(case['prediction_time']))

def feature(records,prediction_time):
    accepted = [row for row in records if row['available_at'] <= prediction_time]
    total = 0
    for record in accepted:
        total += record['value']
    return total
result = feature(records,prediction_time)
assert feature(augmented,prediction_time) == result
assert feature([],prediction_time) == 0
assert feature([records[1]],prediction_time) == records[1]['value']

  test case0 (function_call, visible=True): {"function":"evaluate","args":[{"records":[{"available_at":"2025-01-01T09:00:00","value":2},{"available_at":"2025-01-01T09:30:00","value":3}],"augmented_records":[{"available_at":"2025-01-01T09:00:00","value":2},{"available_at":"2025-01-01T09:30:00","value":3},{"available_at":"2025-01-01T09:30:01","value":7}],"prediction_time":"2025-01-01T09:30:00","empty":[],"policy":"available_at <= prediction_time; timestamps are ISO strings converted with datetime.fromisoformat"}],"expected":5} | on-fail: This fixture does not satisfy the declared return contract.
  test case1 (function_call, visible=False): {"function":"evaluate","args":[{"records":[{"available_at":"2025-01-01T09:00:00","value":4},{"available_at":"2025-01-01T09:30:00","value":3}],"augmented_records":[{"available_at":"2025-01-01T09:00:00","value":2},{"available_at":"2025-01-01T09:30:00","value":3},{"available_at":"2025-01-01T09:30:01","value":7}],"prediction_time":"2025-01-01T09:30:00","empty":[],"policy":"available_at <= prediction_time; timestamps are ISO strings converted with datetime.fromisoformat"}],"expected":7} | on-fail: This fixture does not satisfy the declared return contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2dfa33da79c22fdd8f12bcb5ddb7c813a1c208d2a56129051918d8ff9946c0f0","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Filter by availability before summing, then compare the original and augmented inputs.']  remediation→r04
  MEASURES: B:derive_feature_from_prediction_time_records(f1,f2,f5); B:verify_feature_invariance_to_later_observations(f2,f4,f5)   anchors=['practice']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f5←s06; B.f2←s06; B.f4←s06; B.f5←s06

### s12 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) Excluding future fields does not repair a preprocessing fit that still sees held-out rows; check both boundaries. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(takeaway) Removing timestamps after arithmetic cannot remove a later record's contribution. Filter before summing. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Protect sensitive training and inference data under an existing handling policy: Next: Protect sensitive training and inference data under an existing handling policy.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Prevent Prediction-Time Leakage
(definition) Leakage uses information unavailable at prediction time to build a model and can make held-out performance estimates overly optimistic. Trace rows and fields reaching fit and prediction, then remove held-out or future information from those operations. ⟦A.f1 A.f2 A:tb2 A:tb4 A:tb5⟧
(example) Excluding future fields does not repair a preprocessing fit that still sees held-out rows; check both boundaries. ⟦A.f1 A.f2 A:tb2 A:tb4 A:tb5⟧
[TABLE ds.orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Prevent Prediction-Time Leakage
(definition) Trace rows and fields reaching fit and prediction, then remove held-out or future information from those operations. Separate training and evaluation before fitting preprocessing. On held-out inputs call transform, not fit or fit_transform. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Excluding future fields does not repair a preprocessing fit that still sees held-out rows; check both boundaries. ⟦A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.orders cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r03 · Contrast: Prevent Prediction-Time Leakage
(definition) Select available records with [row for row in records if row["available_at"] <= prediction_time]. Compare the feature on original records and on records augmented with later unavailable observations; assert the earlier feature is unchanged. Apply arithmetic only to time-filtered records. For a sum, initialize total = 0 and accumulate total += record["value"] over the accepted list. ⟦B.f2 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Removing timestamps after arithmetic cannot remove a later record's contribution. Filter before summing. ⟦B.f2 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.feature_records cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r04 · Contrast: Prevent Prediction-Time Leakage
(definition) Derive prediction features only from information available when the prediction is made. Select available records with [row for row in records if row["available_at"] <= prediction_time]. Changing lookup tables can produce different training and serving values. Use the value at the relevant recorded boundary, not an assumed historical latest value. Compare the feature on original records and on records augmented with later unavailable observations; assert the earlier feature is unchanged. ⟦B.f1 B.f2 B.f3 B.f4 B:tb2 B:tb3 B:tb4 B:tb5⟧
(definition) Apply arithmetic only to time-filtered records. For a sum, initialize total = 0 and accumulate total += record["value"] over the accepted list. ⟦B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
(example) Removing timestamps after arithmetic cannot remove a later record's contribution. Filter before summing. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3 B:tb4 B:tb5⟧
[TABLE ds.feature_records cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: RandomizedSearchCV(...)
· constraints.blocked_syntax: mlflow.start_run(...)
· constraints.blocked_syntax: torch.nn.Module subclass definitions
· constraints.blocked_syntax: model.predict_proba(...)
· constraints.blocked_syntax: mlflow.start_run(...)

=========

# EVALUATOR PACKET — Protect Sensitive ML Assets (mle.tile.018_018)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.sensitive_ml_assets — Protect sensitive training and inference data under an existing handling policy

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: mle.tile.018_018.s01: prose block without lineage.fact_ids
  warn: mle.tile.018_018.s05/ix.mle.tile.018_018.s05: ADVISORY — syntax descriptors with no detector: ['MLflow tracking API calls', 'PyTorch tensor, neural-network, autograd and optimizer APIs', 'assert statements and equality comparisons', 'calls to supplied authorized runtime interfaces', 'def and function parameters', 'deployment, registry and pipeline orchestration API calls', 'dictionary comprehensions', 'dictionary literals and dictionary key access', 'for loops', 'if statements', 'import and from ... import statements for required dependencies', 'in and not in membership checks', 'list, tuple and set literals for supplied permitted-field collections', 'prediction-service route and authentication-handler definitions', 'return statements', 'string, integer and boolean literals']

## SOURCE FACTS — A (mle.sensitive_ml_assets)   objective: Enforce an existing permitted-field and credential-exposure policy in diagnostic records.
A.f1: Data access is governed by authenticated identities and authorization, not merely by possession of a dataset or log file.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
A.f2: Implement the supplied permitted-field policy with dictionary membership checks and create a record containing only the permitted values.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
A.f3: Credentials written into an image or its metadata can be exposed; remove literal credentials from the data/log sample rather than treating them as ordinary diagnostic values.   [sources: docker_docs#https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/ — Description]
A.f4: Keep the credential value in the authorized runtime secret mechanism rather than copying it into a generated record.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/secrets/ — secrets]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Protect Sensitive ML Assets.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write one Python audit in a learner-defined function, including learner-written imports for any required library or supplied runtime-client dependencies. Apply the supplied identity and permitted-field policy to a dataset/log sample, construct a new dictionary using membership checks, and exclude restricted values and literal credentials without copying the credential out of the authorized runtime secret mechanism.  SUCCESS: For the authorized fixture, the returned record contains only run_id and row_count with their original values. Neither token nor restricted raw customer values appear in the returned record or captured output. The supplied authorization boundary is respected, and the credential remains available only through the existing authorized runtime secret mechanism.
ASSESSMENT ANCHOR: apply_existing_identity_and_authorization_policy facts=['f1']
ASSESSMENT ANCHOR: construct_permitted_field_records_with_membership_checks facts=['f2']
ASSESSMENT ANCHOR: remove_literal_credentials_from_generated_assets facts=['f3']
ASSESSMENT ANCHOR: retain_credentials_in_authorized_runtime_secret_mechanism facts=['f4']

## DATA ASSETS USED
ds.audit_sample: Dummy permitted/restricted diagnostic fields — columns: run_id(identifier), row_count(numerical), token(pii), raw_customer_values(pii)
   ["run_fixture",6,"DUMMY_TOKEN_NOT_A_CREDENTIAL","DUMMY_CUSTOMER_NOT_A_PERSON"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Define measurable model acceptance criteria from task objectives; Document model limitations and foreseeable misuse under an existing risk policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Fit and predict with a bounded scikit-learn baseline workflow; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction errors for recurring failure modes; Justify classical versus neura

## LESSON, in learner order

### s01 · explainer · Protect Sensitive ML Assets
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(mechanism) Access depends on authenticated identities and authorization, not simply possession of a dataset or log. Use dictionary membership checks to construct a record containing only the values permitted by the supplied policy. Literal credentials in images or metadata can be exposed. Remove them from data/log samples rather than treating them as diagnostics. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Keep the credential in the authorized runtime secret mechanism instead of copying its value into a generated record. ⟦A.f4 A:tb3⟧
[BEFORE_AFTER] Dictionary membership selects only supplied permitted fields; dummy restricted values are excluded. Credentials stay in the authorized runtime secret mechanism.
  before:
[TABLE ds.audit_sample cols=all ] caption: Dummy input only: possession is not authorization to redistribute these fields.
  after:
[TABLE ds.audit_sample cols=['run_id', 'row_count'] ] caption: New permitted-field record: runtime secrets remain outside generated diagnostics.

### s02 · explainer · A bounded work example
Working rule — 
(example) Apply the existing identity and permitted-field policy to the dummy audit sample. Construct a new dictionary rather than copying every field: only run_id and row_count are permitted here. Inspect both the returned record and captured output for restricted values. Keep credentials in the authorized runtime secret mechanism, not images, metadata or diagnostics. This implements supplied policy; it does not authorize additional readers or fields. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · A distinction to keep
Working rule — 
(misconception) Possessing the sample does not authorize disclosure. Moving a literal credential into metadata does not remove exposure risk. ⟦A.f1 A.f3 A.f4 A:tb5⟧

### s04 · check · Judge the protect sensitive ml assets decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.
QUESTION [choice, intro, grading=client] Which handling respects the supplied authorization and permitted-field policy?
  ✔ 0: Keep credentials in the authorized runtime mechanism and return only permitted fields
      why: Correct. Copying credentials discloses them; possession is not authenticated authorization.
  ✘ 1: Copy the runtime credential into the audit record
      why: Copying credentials discloses them; possession is not authenticated authorization.
  ✘ 2: Treat possession of a log file as authorization
      why: Copying credentials discloses them; possession is not authenticated authorization.
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Check authorization separately from which fields the policy permits.']  remediation→r01
  MEASURES: A:remove_literal_credentials_from_generated_assets(f3)   anchors=[]
  taught-before-tested: A.f3←s01

### s05 · hands_on · Verify protect sensitive ml assets
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.
QUESTION [code_exercise, stretch, grading=client] Implement audit(sample, permitted, identity). Read only through supplied read_sample (unauthorized identity raises PermissionError); construct a NEW permitted-field dictionary using membership checks. Assign result. Assert only original run_id/row_count remain, both restricted fields are absent, unauthorized access is denied, and use_secret succeeds without returning or printing a credential. Do not print any sample or secret.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': []} constraints.allowed=['def and function parameters', 'return statements', 'import and from ... import statements for required dependencies', 'variable assignment', 'dictionary literals and dictionary key access', 'dictionary items() iteration', 'for loops', 'if statements', 'in and not in membership checks', 'dictionary comprehensions', 'list, tuple and set literals for supplied permitted-field collections', 'string, integer and boolean literals', 'calls to supplied authorized runtime interfaces', 'assert statements and equality comparisons'] blocked=5 items
  file learner.py [editable]:
# Authored fixtures only; no learner solution.
FIXTURES = {'sample': {'run_id': 'run_fixture',
            'row_count': 6,
            'token': 'DUMMY_TOKEN_NOT_A_CREDENTIAL',
            'raw_customer_values': 'DUMMY_CUSTOMER_NOT_A_PERSON'},
 'permitted_fields': ['run_id', 'row_count'],
 'authorized_identity': 'fixture_reader',
 'unauthorized_identity': 'fixture_other',
 'policy': 'Only fixture_reader may read sample; permission denial raises '
           'PermissionError. No restricted value in returned record or stdout.',
 'runtime_secret_name': 'fixture_token'}

_SECRET = 'DUMMY_RUNTIME_SECRET_NOT_A_CREDENTIAL'
def read_sample(identity, sample):
    if identity != 'fixture_reader':
        raise PermissionError('Unauthorized fixture identity')
    return dict(sample)
def use_secret(identity, secret_name):
    if identity != 'fixture_reader' or secret_name != 'fixture_token':
        raise PermissionError('Unauthorized fixture secret use')
    return bool(_SECRET)  # Use the authorized dummy without disclosing its literal.

sample = FIXTURES['sample']
permitted = FIXTURES['permitted_fields']
identity = FIXTURES['authorized_identity']
secret_name = FIXTURES['runtime_secret_name']
# This driver tests authorization without disclosing a credential.
def denied(sample, permitted, identity):
    try:
        audit(sample,permitted,identity)
    except PermissionError:
        return True
    return False

# TODO: write your implementation and assertions below.

  SOLUTION learner.py:
# Authored fixtures only; no learner solution.
FIXTURES = {'sample': {'run_id': 'run_fixture',
            'row_count': 6,
            'token': 'DUMMY_TOKEN_NOT_A_CREDENTIAL',
            'raw_customer_values': 'DUMMY_CUSTOMER_NOT_A_PERSON'},
 'permitted_fields': ['run_id', 'row_count'],
 'authorized_identity': 'fixture_reader',
 'unauthorized_identity': 'fixture_other',
 'policy': 'Only fixture_reader may read sample; permission denial raises '
           'PermissionError. No restricted value in returned record or stdout.',
 'runtime_secret_name': 'fixture_token'}

_SECRET = 'DUMMY_RUNTIME_SECRET_NOT_A_CREDENTIAL'
def read_sample(identity, sample):
    if identity != 'fixture_reader':
        raise PermissionError('Unauthorized fixture identity')
    return dict(sample)
def use_secret(identity, secret_name):
    if identity != 'fixture_reader' or secret_name != 'fixture_token':
        raise PermissionError('Unauthorized fixture secret use')
    return bool(_SECRET)  # Use the authorized dummy without disclosing its literal.

sample = FIXTURES['sample']
permitted = FIXTURES['permitted_fields']
identity = FIXTURES['authorized_identity']
secret_name = FIXTURES['runtime_secret_name']
# This driver tests authorization without disclosing a credential.
def denied(sample, permitted, identity):
    try:
        audit(sample,permitted,identity)
    except PermissionError:
        return True
    return False

def audit(sample,permitted,identity):
    authorized = read_sample(identity,sample)
    result = {key:value for key,value in authorized.items() if key in permitted}
    return result
result = audit(sample,permitted,identity)
assert result == {'run_id':sample['run_id'],'row_count':sample['row_count']}
assert 'token' not in result
assert 'raw_customer_values' not in result
assert denied(sample,permitted,FIXTURES['unauthorized_identity'])
assert use_secret(identity,secret_name)

  test call0 (function_call, visible=False): {"function":"audit","args":[{"run_id":"run_fixture","row_count":6,"token":"DUMMY_TOKEN_NOT_A_CREDENTIAL","raw_customer_values":"DUMMY_CUSTOMER_NOT_A_PERSON"},["run_id","row_count"],"fixture_reader"],"expected":{"run_id":"run_fixture","row_count":6}} | on-fail: The parameterized function fails a supplied boundary fixture.
  test call1 (function_call, visible=False): {"function":"audit","args":[{"run_id":"run_other","row_count":2,"token":"DUMMY"},["run_id","row_count"],"fixture_reader"],"expected":{"run_id":"run_other","row_count":2}} | on-fail: The parameterized function fails a supplied boundary fixture.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6520332861be39d1d4e0c982c23e3a475f0ec9f138ea1453c2f59759680f65db","tests_passed":2}
  feedback✔: You applied the declared boundary and its required checks.  feedback✘: Recheck the declared contract and the evidence for each decision.  hints: ['Distinguish authorized reading, permitted-field selection and secret use without disclosure.']  remediation→r02
  MEASURES: A:apply_existing_identity_and_authorization_policy(f1); A:construct_permitted_field_records_with_membership_checks(f2); A:retain_credentials_in_authorized_runtime_secret_mechanism(f4)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01

### s06 · recap · Keep the contracts explicit
Takeaways — 
(takeaway) Possessing the sample does not authorize disclosure. Moving a literal credential into metadata does not remove exposure risk. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Select task-appropriate classification or regression metrics: Next: Select task-appropriate classification or regression metrics.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Contrast: Protect Sensitive ML Assets
(definition) Literal credentials in images or metadata can be exposed. Remove them from data/log samples rather than treating them as diagnostics. ⟦A.f3 A:tb2 A:tb4 A:tb5⟧
(example) Possessing the sample does not authorize disclosure. Moving a literal credential into metadata does not remove exposure risk. ⟦A.f3 A:tb2 A:tb4 A:tb5⟧
[TABLE ds.audit_sample cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.
### r02 · Contrast: Protect Sensitive ML Assets
(definition) Access depends on authenticated identities and authorization, not simply possession of a dataset or log. Use dictionary membership checks to construct a record containing only the values permitted by the supplied policy. Keep the credential in the authorized runtime secret mechanism instead of copying its value into a generated record. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
(example) Possessing the sample does not authorize disclosure. Moving a literal credential into metadata does not remove exposure risk. ⟦A.f1 A.f2 A.f4 A:tb2 A:tb3 A:tb4 A:tb5⟧
[TABLE ds.audit_sample cols=all ] caption: Use the same supplied fixture to distinguish the two interpretations.

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: model.fit() and model.predict() calls