# EVALUATOR PACKET — Define the Prediction Task (mle.tile.000_000)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_task_definition — Frame a prediction task with prediction-time inputs

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦A:tb1⟧
(definition) Start with the inference you need and the example data that supports it. Use only inputs available when the prediction is made, not information arriving afterward. Empirical outcome proportion is outcome count divided by the specified population total. A conditional proportion uses only members of its stated group. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Specify one prediction unit, the target event or value, prediction time and judgement horizon so each example has an unambiguous target. ⟦A.f4 A:tb3⟧
[TABLE ds.task_record cols=all ] caption: Order-at-acceptance prediction task
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"ds.outcome_counts"},"range":"A1:E3","show_formula_bar":true,"cells":[{"ref":"E2","formula":"=B2/C2","note":"Outcome count divided by this row's specified population total."},{"ref":"E3","formula":"=B3/C3","note":"Outcome count divided by this row's specified population total."}],"annotations":[{"target":"E1","text":"Outcome proportion"}],"lineage":{"concept_ids":["mle.prediction_task_definition"],"teaching_block_ids":[],"fact_ids":[],"anchors":["mle.prediction_task_definition#visual"]}}

### s02 · explainer · A bounded work example
Working rule — 
(example) In this fictional task, the order at acceptance is the unit. The task record separates target, decision time, horizon and permitted inputs. Later arrival establishes the target but is excluded from acceptance-time inputs. Divide each outcome count by the total for its own declared population: all orders and the specified zone answer different questions. Changing the unit or horizon changes the task, not merely its implementation. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · video · Trace the working rule
Optional walkthrough — 
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · explainer · A distinction to keep
Working rule — 
(misconception) Later arrival can establish the target, but cannot be an acceptance-time input. A zone denominator does not describe all orders. ⟦A.f2 A.f3 A:tb5⟧

### s05 · check · Judge the define the prediction task decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.

### s06 · hands_on · Review define the prediction task
Practice — Read the supplied excerpts in this step and decide which satisfy the stated contract and which are defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
 'tuple_boundary': [[2, 10]],
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

for name in ("valid", "tuple_boundary", "flat", "wrong_width", "too_many"):
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

### s05 · hands_on · Verify numerical arrays for ml
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

### s10 · hands_on · Verify numerical arrays for ml
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s15 · check · Judge the numerical arrays for ml decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.

### s16 · hands_on · Verify numerical arrays for ml
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

=========

# EVALUATOR PACKET — Ingest and Inspect Model Data / Ingest and Inspect Model Data / Ingest and Inspect Model Data (mle.tile.004_006)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.file_object_ingestion — Consume existing file or object-storage datasets in a format suited to ML access patterns
B = mle.chunked_ingestion — Read model datasets in chunks sized to an array memory budget
C = mle.dataset_inspection — Inspect model-facing dataset structure, distributions and memory footprint

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s06 · hands_on · Review ingest and inspect model data
Practice — Read the supplied excerpts in this step and decide which satisfy the stated contract and which are defective or unsafe.

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

### s11 · hands_on · Verify ingest and inspect model data
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

### s16 · hands_on · Verify ingest and inspect model data
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

=========

# EVALUATOR PACKET — Validate and Clean Datasets / Validate and Clean Datasets (mle.tile.007_008)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.dataset_schema_validation — Validate dataset schema constraints before training
B = mle.dataset_cleaning_policy — Resolve duplicate and invalid observations with a documented cleaning policy

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s05 · hands_on · Verify validate and clean datasets
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

### s06 · explainer · Validate and Clean Datasets
Working rule — 
(intro) Before accepting a delivery-fixture result, state the contract and the checks this rule requires. ⟦B:tb1⟧
(mechanism) Track accepted observation keys in a set; check membership before adding the next accepted key. Choose the declared retain, repair or reject action from a policy dictionary for each invalid or repeated observation. Inspect and clean examples as needed, making representations consistent with their intended training use. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Implement policy actions with conditional branches and report affected observation IDs rather than changing data silently. Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.cleaning_orders cols=all ] caption: Policy-driven accepted-order cleaning
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

### s10 · hands_on · Verify validate and clean datasets
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

=========

# EVALUATOR PACKET — Representation, Labels and Splits / Representation, Labels and Splits / Representation, Labels and Splits (mle.tile.009_011)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.dataset_selection_bias — Identify sampling and selection bias in dataset coverage
B = mle.label_integrity — Validate labels and their availability for the prediction task
C = mle.deployment_matched_splits — Choose leakage-safe train, validation and test splits matching deployment conditions

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s04 · explainer · A distinction to keep
Working rule — 
(misconception) Sample share and inclusion probability have different denominators. A sample summary is not automatically target-representative. ⟦A.f4 A:tb5⟧

### s05 · check · Judge the representation, labels and splits decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.

### s06 · hands_on · Verify representation, labels and splits
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

### s11 · hands_on · Verify representation, labels and splits
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

### s16 · hands_on · Verify representation, labels and splits
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

=========

# EVALUATOR PACKET — Fit and Compose Preprocessing / Fit and Compose Preprocessing / Fit and Compose Preprocessing / Fit and Compose Preprocessing (mle.tile.012_015)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.training_fitted_imputation — Fit missing-value imputation using training data only
B = mle.training_fitted_scaling — Scale numerical features using training-fitted parameters
C = mle.categorical_encoding — Encode categorical features with an unseen-category policy
D = mle.preprocessing_pipeline — Compose a fitted preprocessing pipeline reused across training and bounded inference

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s05 · hands_on · Verify fit and compose preprocessing
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

### s11 · hands_on · Verify fit and compose preprocessing
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

### s16 · hands_on · Verify fit and compose preprocessing
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

### s21 · hands_on · Review fit and compose preprocessing
Practice — Read the supplied excerpts in this step and decide which satisfy the stated contract and which are defective or unsafe.

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

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s05 · hands_on · Verify prevent prediction-time leakage
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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
[VIDEO ] bridge-before:  | bridge-after: 

### s10 · check · Judge the prevent prediction-time leakage decision
Check your judgement — Choose the interpretation that satisfies the supplied contract.

### s11 · hands_on · Verify prevent prediction-time leakage
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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

=========

# EVALUATOR PACKET — Protect Sensitive ML Assets (mle.tile.018_018)
Tile summary: Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.sensitive_ml_assets — Protect sensitive training and inference data under an existing handling policy

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s05 · hands_on · Verify protect sensitive ml assets
Practice — Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.

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