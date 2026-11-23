import json, re, pprint, copy, sys
sys.path.insert(0,"00_FINAL_PIPELINE_CORE/scripts")
from finlib import words
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
p=json.loads((B/'tile_plans.json').read_text()); g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); r=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={v['context']['concept_id']:v for v in g['bundles']}; assets={a['asset_id']:a for a in r['assets']}
F={
'prediction_task_definition': 'Start with the inference you need and the example data that supports it.|Use only inputs available when the prediction is made, not information arriving afterward.|Empirical outcome proportion is outcome count divided by the specified population total. A conditional proportion uses only members of its stated group.|Specify one prediction unit, the target event or value, prediction time and judgement horizon so each example has an unambiguous target.',
'numpy_shape_dtype': 'Import numpy as np, create np.array(fixture) from the supplied list or tuple, and inspect ndim, shape and dtype.|For a two-axis batch/feature contract, check a.ndim == 2 before comparing a.shape[1] with the required feature count.|Each shape entry is an axis length. After checking rank, use a.shape[0] to check the batch-length requirement.|Reject an input requirement violation with a conditional raise ValueError(message), rather than continuing with invalid input.|Use assert predicate for valid, boundary and failure fixtures. In ordinary non-optimized execution, a false predicate raises AssertionError.',
'numpy_dtype_selection': 'Numerical dtypes have a representable range and bit width; integer and floating candidates may preserve different values.|Inspect a.dtype and compare explicit casts made with a.astype(candidate_dtype).|For fixed-width numerical arrays, a.size * a.itemsize equals a.nbytes: element-storage bytes, excluding non-element object overhead.|Before accepting lower precision, subtract reference values from cast values. A cast can overflow or lose precision.',
'numpy_vectorization': 'NumPy arithmetic can act elementwise on arrays rather than performing one Python operation per observation.|Broadcasting aligns axes from the right. Aligned lengths must match or one must be 1; missing leading axes count as length 1.|Check result shape separately from operand compatibility: compatible broadcasting can expand the result.|Compare against a list-comprehension reference with np.testing.assert_allclose(array_result, reference_result, rtol=..., atol=...) using explicit tolerances.',
'file_object_ingestion': 'An authorized Google Cloud Storage client lists existing prefix-matching objects with client.list_blobs(bucket_name, prefix=prefix).|Select the intended name, then download with bucket.blob(object_name).download_to_filename(local_path).|Read CSV with pd.read_csv(local_path, dtype=declared_types). Verify columns, row count and value representations against the expected dataset.|CSV is delimited text. Parquet is columnar and its reader can select columns; use the supplied format that fits the required access pattern.|For a local text identity record, use with open(path, mode, encoding="utf-8") as f and read or write inside that block.|Import from google.cloud import storage and construct storage.Client() with the existing authorized runtime identity.|Import pandas as pd. Apply explicit per-column conversions for declared types and inspect converted values; inference is not a type guarantee.',
'chunked_ingestion': 'Iterate pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types) with a for loop, processing bounded chunks instead of retaining the whole dataset.|A homogeneous fixed-width matrix with R rows, F columns and W bytes per element needs R * F * W element bytes.|Choose chunksize within the stated array budget and verify every materialized matrix. This estimate does not bound total reader or process memory.|Keep the dataset stream open with with open(...) throughout chunk iteration.',
'dataset_inspection': 'Inspect loaded columns, dtypes and descriptive summaries before declaring model-input readiness.|Report matrix shape and dtype with each axis meaning, not just total element count.|Use array.nbytes for matrix element memory, distinguishing it from total process memory.|Return named readiness fields in a dictionary from a parameterized inspection function so callers can check consistent fields.|Use np.mean(numeric_values, axis=0) to average each selected numeric feature over rows.|Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root. Use ddof=1 only when the stated calculation requires N-1.',
'dataset_schema_validation': 'A schema specifies expected features and permitted representations or values. Missing, unexpected and invalid features violate it.|Compare table.columns and table.dtypes to the declared contract before checking constrained columns.|Express value constraints as boolean predicates. Raise an explicit validation exception for a failed required column, type or value boundary.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
'dataset_cleaning_policy': 'Track accepted observation keys in a set; check membership before adding the next accepted key.|Choose the declared retain, repair or reject action from a policy dictionary for each invalid or repeated observation.|Inspect and clean examples as needed, making representations consistent with their intended training use.|Implement policy actions with conditional branches and report affected observation IDs rather than changing data silently.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
'dataset_selection_bias': 'Collection or filtering omissions can exclude observations important to the intended prediction population.|Compare category count divided by population total in sample and target to identify supported coverage differences.|With known target membership, estimate inclusion probability as included category members divided by all target category members. An empty denominator cannot support a rate.|Unequal inclusion probabilities affect sample interpretation. A descriptive sample summary is not automatically target-representative.|Compute the selected numeric observations\' arithmetic mean with np.mean(numeric_values).|Use np.std(numeric_values, ddof=0) to divide squared deviations by N before taking the square root. Use ddof=1 only if the stated calculation needs N-1.',
'label_integrity': 'Match labels to observations or predictions by the intended unique identifier, not incidental row order.|Check duplicate IDs before constructing the ID-to-label dictionary: reassignment of an existing key replaces its earlier value.|Use observation-ID and label-ID set differences to detect missing labels and labels without observations.|Use keyed dictionary lookups to compare labels, observation timestamps and availability timestamps under task-specific acceptance predicates.|Information unavailable at the relevant prediction boundary is not an available input to that prediction.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
'deployment_matched_splits': 'A random split is appropriate only when its sampling interpretation matches evaluation. Group dependence or time ordering can require different boundaries.|Keep a common evaluation group on one side; keep time-ordered training observations earlier than the intended later evaluation observations.|Represent supplied groups with sets and assert an empty training/validation group intersection.|For a time cutoff, select earlier training and the stated later evaluation observations; check timestamp inequalities.|Report each partition\'s target count divided by its total to describe the population actually evaluated.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
 'training_fitted_imputation': 'SimpleImputer learns a replacement per feature from fit data. Strategies include mean, median, most_frequent and constant.|Use SimpleImputer(strategy=declared_strategy).fit(X_train), then transform(X_validation) without fitting validation rows.|Inspect statistics_ for fitted replacements and verify validation transformation leaves them unchanged.|Use np.mean(numeric_values, axis=0) to average selected numeric feature columns over rows.|Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires N-1.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
 'training_fitted_scaling': 'With with_mean and with_std enabled, StandardScaler centers each feature by its training mean and scales by its training standard deviation.|Fit StandardScaler on X_train and reuse transform on X_validation. Inspect stored parameters through mean_ and scale_.|A constant feature cannot become unit variance; StandardScaler leaves its scaling factor at 1.|Validation and prediction must receive training transformations, not separately fitted transformations.|Use np.mean(numeric_values, axis=0) to average selected numeric feature columns over rows.|Use np.std(numeric_values, axis=0, ddof=0) to divide squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires N-1.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
 'categorical_encoding': 'OneHotEncoder learns categories from fit data and represents values in corresponding indicator columns.|Fit training categories, inspect categories_, and transform validation without relearning the mapping.|Choose handle_unknown explicitly. Default error rejects unknowns; ignore gives all-zero indicators for an unknown category in that feature.|Missing values can become a learned category if present during fit. Missing values absent from learned categories follow the unknown policy.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.|Build a training-category dictionary from categories_ and feature names. Align list-based known, unseen and missing fixtures with that stored mapping.',
 'preprocessing_pipeline': 'Construct Pipeline([(name, transformer), ..., (name, estimator)]) to chain transformations with a final estimator.|Pipeline.fit fits transformations and the final estimator on training data; predict applies fitted transformations before prediction.|ColumnTransformer assigns declared transformers to selected columns, allowing numerical and categorical operations in one fitted workflow.|Reuse the fitted pipeline for validation and bounded inference; do not fit new preprocessing state.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
 'prediction_boundary_leakage': 'Leakage uses information unavailable at prediction time to build a model and can make held-out performance estimates overly optimistic.|Trace rows and fields reaching fit and prediction, then remove held-out or future information from those operations.|Separate training and evaluation before fitting preprocessing. On held-out inputs call transform, not fit or fit_transform.|Use assert predicate for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
 'leakage_safe_features': 'Derive prediction features only from information available when the prediction is made.|Select available records with [row for row in records if row["available_at"] <= prediction_time].|Changing lookup tables can produce different training and serving values. Use the value at the relevant recorded boundary, not an assumed historical latest value.|Compare the feature on original records and on records augmented with later unavailable observations; assert the earlier feature is unchanged.|Apply arithmetic only to time-filtered records. For a sum, initialize total = 0 and accumulate total += record["value"] over the accepted list.',
 'sensitive_ml_assets': 'Access depends on authenticated identities and authorization, not simply possession of a dataset or log.|Use dictionary membership checks to construct a record containing only the values permitted by the supplied policy.|Literal credentials in images or metadata can be exposed. Remove them from data/log samples rather than treating them as diagnostics.|Keep the credential in the authorized runtime secret mechanism instead of copying its value into a generated record.'
}
E={
'prediction_task_definition': 'In this fictional task, the order at acceptance is the unit. The task record separates target, decision time, horizon and permitted inputs. Later arrival establishes the target but is excluded from acceptance-time inputs. Divide each outcome count by the total for its own declared population: all orders and the specified zone answer different questions. Changing the unit or horizon changes the task, not merely its implementation.',
'numpy_shape_dtype': 'The order matrix has one row per order and one column per feature. Flattening those same values destroys the declared two-axis interpretation. Check rank first, then feature width and batch length; a narrow matrix fails a different requirement from a flat one. Explicit ValueError rejects invalid inputs, while assertions exercise valid, boundary and failure fixtures.',
'numpy_dtype_selection': 'Retain the reference while comparing candidate casts. Inspect dtype, element count, itemsize and nbytes; subtract reference values to reveal precision changes, including the boundary probe. Apply the supplied tolerance and element-storage budget together. A smaller representation does not establish acceptable differences, and element bytes exclude other object overhead.',
'numpy_vectorization': 'Subtract the feature-reference vector from the order matrix and check against an independent list-comprehension calculation. Right-aligned compatibility permits the operation, but the resulting shape must still match the contract. The column/row contrast broadcasts successfully while expanding the result: success alone is not shape acceptance.',
'file_object_ingestion': 'The approved object listing contains alternatives, but the task names one object. Select that name, download to the declared local path, load with declared types and verify identity, columns and row count. Inspect the converted order key rather than relying on inference. Keep the identity-record write inside its file context. For a separately specified selected-column task, relate Parquet to that access pattern; do not change formats arbitrarily.',
'chunked_ingestion': 'Choose a row limit from the supplied feature count, element width and array budget. Keep the file context around the loop and verify each materialized matrix, including the smaller final chunk. Process rather than collect the chunks. The element-byte calculation concerns this homogeneous matrix, not parsing buffers or total process memory.',
'dataset_inspection': 'Inspect the supplied order-feature table and return a named dictionary. Keep observation and feature axis meanings beside shape and dtype. Compute feature-wise mean and population standard deviation over rows, retaining the specified divisor. Report observed nbytes as element storage, not total process memory. A parameterized function lets another caller inspect the same named fields for a different fixture.',
'dataset_schema_validation': 'Compare the distance/zone column set and declared dtypes first. Then check the inclusive distance bounds and permitted zone representation. A lower-bound row is a boundary fixture; an out-of-range row is a value failure. An unexpected feature is a structural failure even if its values look plausible. Use explicit exceptions for rejection and assertions to exercise the supplied fixtures.',
'dataset_cleaning_policy': 'Check the accepted-key set before accepting another observation. Apply the supplied repeat-key rejection and approved zone-spelling repair through the policy dictionary, recording affected IDs. A different defect may require rejection rather than repair. These are this dataset\'s approved actions, not a universal deduplication rule; test normal, boundary and repeated-key cases.',
'dataset_selection_bias': 'Compare the supplied sample and target zone counts with their own population totals. Inclusion uses a different denominator: all target members of that zone. These ratios support a coverage comparison, not claims about every zone characteristic. Summarize the selected numeric observations using their stated mean and standard-deviation divisor. Do not invent an inclusion rate when target membership is empty.',
'label_integrity': 'The label records are reordered relative to observations. Keyed lookup preserves correspondence; matching row counts alone does not. Detect duplicate IDs before dictionary construction, then inspect both ID-set differences and matched timestamps under the supplied predicates. Later label availability does not make it an earlier prediction input. Exercise reordered, duplicate, missing and boundary fixtures.',
'deployment_matched_splits': 'The group fixture keeps every observation from one customer group together; splitting that group across partitions violates its boundary. Assert group disjointness. In the separate time fixture, check earlier training and the declared later evaluation interval directly. Report target counts over each partition total. That proportion describes the cohort actually evaluated; group disjointness does not prove timestamp ordering.',
'training_fitted_imputation': 'Under the supplied mean strategy, fit only observed training distances and retain statistics_. Transform validation, including missing entries, without incorporating validation distances into a new replacement. Compare stored state before and after. Keep complete, missing and boundary checks; feature-spread summaries use the stated divisor and are distinct from the chosen imputation strategy.',
'training_fitted_scaling': 'Use the training distances to compute columnwise mean and population spread, then inspect mean_ and scale_ from the fitted scaler. Apply that same rule to validation rather than recentering the held-out cohort. Confirm fitted parameters remain unchanged. Include the constant feature: its scaling factor stays 1, not a promise of unit variance.',
'categorical_encoding': 'Fit the supplied training zones and store the dictionary in categories_ order under the feature name. Align known, unseen and missing fixtures with it. Compare explicit error and ignore policies for unseen values. A missing value learned during fit differs from one absent at fit. Validation must preserve the mapping; all-zero indicators do not mean an unseen category was learned.',
'preprocessing_pipeline': 'Assign distance to the declared numerical transformation and zone to the category encoder using ColumnTransformer. Chain this with the final estimator in Pipeline. Fit training once, then predict validation and bounded inference through the same fitted object. Trace a row through selected columns and transformations; separately preparing validation with a new encoder breaks that workflow. Check supplied valid, boundary and failure cases and unchanged fitted state.',
'prediction_boundary_leakage': 'At order acceptance, the eventual-arrival field is unavailable. Remove it from prediction inputs. Independently inspect preprocessing fit rows: fitting on training plus held-out rows violates that boundary even if the estimator fits training only. Split first and transform held-out inputs with training state. Check field selection and fit-row membership explicitly; separate filenames alone do not establish the boundary.',
'leakage_safe_features': 'Filter records by availability before summing their values. Compare original and later-augmented records at the same prediction time; the accepted list and earlier feature must not change. A record exactly on the boundary follows the supplied <= predicate. If a changing lookup contributes, select its value at the recorded boundary rather than assuming the latest lookup is historical.',
'sensitive_ml_assets': 'Apply the existing identity and permitted-field policy to the dummy audit sample. Construct a new dictionary rather than copying every field: only run_id and row_count are permitted here. Inspect both the returned record and captured output for restricted values. Keep credentials in the authorized runtime secret mechanism, not images, metadata or diagnostics. This implements supplied policy; it does not authorize additional readers or fields.'
}
# One concise, fact-backed contrast reused for targeted recovery.
C={
'prediction_task_definition':'Later arrival can establish the target, but cannot be an acceptance-time input. A zone denominator does not describe all orders.',
'numpy_shape_dtype':'The flat fixture and matrix can contain the same values, yet only the matrix has the declared batch/feature axes.',
'numpy_dtype_selection':'A smaller cast can meet a byte budget while failing value fidelity; keep the unchanged reference for comparison.',
'numpy_vectorization':'Broadcast-compatible does not mean contract-shaped: the column/row example expands the output.',
'file_object_ingestion':'A downloaded file can still be the wrong named object or have the wrong converted key representation.',
'chunked_ingestion':'One bounded working matrix is not the whole process; collecting every chunk defeats the working-chunk approach.',
'dataset_inspection':'Total element count omits axis meanings; nbytes omits other process memory.',
'dataset_schema_validation':'A loaded table can violate structure or value bounds; explicit exceptions reject it, while assertions exercise fixtures.',
'dataset_cleaning_policy':'An approved spelling repair does not authorize silently repairing every defect; report each policy action and affected ID.',
'dataset_selection_bias':'Sample share and inclusion probability have different denominators. A sample summary is not automatically target-representative.',
'label_integrity':'Equal row counts can hide reordered identities. A dictionary built before duplicate checks can hide a replaced label.',
'deployment_matched_splits':'An empty group intersection checks group separation, not whether training timestamps precede evaluation.',
'training_fitted_imputation':'Transform reuses training replacements; fitting validation learns different state.',
'training_fitted_scaling':'Validation reuses training mean and scale; it is not separately centered to its own mean.',
'categorical_encoding':'An all-zero unseen indicator under ignore is not a newly learned category. Missing treatment depends on what fit saw.',
'preprocessing_pipeline':'Predict applies fitted transformations; fitting a new encoder for validation changes the workflow.',
'prediction_boundary_leakage':'Excluding future fields does not repair a preprocessing fit that still sees held-out rows; check both boundaries.',
'leakage_safe_features':'Removing timestamps after arithmetic cannot remove a later record\'s contribution. Filter before summing.',
'sensitive_ml_assets':'Possessing the sample does not authorize disclosure. Moving a literal credential into metadata does not remove exposure risk.'
}
D={
'prediction_task_definition':['ds.task_record','ds.outcome_counts'], 'numpy_shape_dtype':['ds.order_features'], 'numpy_dtype_selection':['ds.dtype_reference'], 'numpy_vectorization':['ds.order_features'], 'file_object_ingestion':['ds.orders'], 'chunked_ingestion':['ds.chunked_orders'], 'dataset_inspection':['ds.order_features'], 'dataset_schema_validation':['ds.distance_zone'], 'dataset_cleaning_policy':['ds.cleaning_orders'], 'dataset_selection_bias':['ds.selection_counts','ds.order_features'], 'label_integrity':['ds.observations','ds.labels'], 'deployment_matched_splits':['ds.group_orders','ds.time_orders'], 'training_fitted_imputation':['ds.imputation_train','ds.imputation_validation'], 'training_fitted_scaling':['ds.scaling_train','ds.scaling_validation'], 'categorical_encoding':['ds.zone_train','ds.zone_cases'], 'preprocessing_pipeline':['ds.distance_zone'], 'prediction_boundary_leakage':['ds.orders'], 'leakage_safe_features':['ds.feature_records'], 'sensitive_ml_assets':['ds.audit_sample']}
fixture={a['asset_id'].removeprefix('ws.'):json.loads(next(f['content'] for f in a['files'] if f['path']=='fixtures.json')) for a in r['assets'] if a['asset_kind']=='code_workspace'}
code={
'numpy_shape_dtype':'''import numpy as np

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
        print(name, str(error))''',
'numpy_dtype_selection':'''import numpy as np
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
    print("faithful, within element budget, accepted:", faithful, within_budget, faithful and within_budget)''',
'numpy_vectorization':'''import numpy as np
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
assert expanded.shape != column.shape''',
'file_object_ingestion':'''from google.cloud import storage
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
# ingest(fixture)''',
'chunked_ingestion':'''import pandas as pd
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
print("maximum working-matrix bytes:", maximum)''',
'dataset_inspection':'''import numpy as np
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
    print(name, readiness)''',
'dataset_schema_validation':'''import pandas as pd

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
        print(str(error))''',
'dataset_cleaning_policy':'''accepted_keys = set()
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
print("result:", accepted, "affected:", affected)''',
'dataset_selection_bias':'''import numpy as np
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
print("mean, std, divisor choice:", np.mean(values), np.std(values, ddof=fixture["ddof"]), fixture["ddof"])''',
'label_integrity':'''from datetime import datetime

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
        print(name, type(error).__name__)''',
'deployment_matched_splits':'''from datetime import datetime
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
    print(name, "target count, total, proportion:", count, len(partition), count / len(partition) if partition else None)''',
 'training_fitted_imputation':'''import numpy as np
from sklearn.impute import SimpleImputer
X_train = np.array(fixture["X_train"], dtype=float)
X_validation = np.array(fixture["X_validation"], dtype=float)
imputer = SimpleImputer(strategy=fixture["declared_strategy"]).fit(X_train)
before = imputer.statistics_.copy()
transformed = imputer.transform(X_validation)
np.testing.assert_array_equal(imputer.statistics_, before)
observed = X_train[~np.isnan(X_train)].reshape(-1, X_train.shape[1])
print("observed training mean and population spread:", np.mean(observed, axis=0), np.std(observed, axis=0, ddof=0))
print("statistics before, transformed validation, statistics after:", before, transformed, imputer.statistics_)''',
 'training_fitted_scaling':'''import numpy as np
from sklearn.preprocessing import StandardScaler
X_train = np.array(fixture["X_train"], dtype=float)
X_validation = np.array(fixture["X_validation"], dtype=float)
scaler = StandardScaler(with_mean=fixture["with_mean"], with_std=fixture["with_std"]).fit(X_train)
before_mean, before_scale = scaler.mean_.copy(), scaler.scale_.copy()
transformed = scaler.transform(X_validation)
np.testing.assert_array_equal(before_mean, scaler.mean_)
np.testing.assert_array_equal(before_scale, scaler.scale_)
print("training mean and population spread:", np.mean(X_train, axis=0), np.std(X_train, axis=0, ddof=0))
print("mean_, scale_, transformed, unchanged state:", before_mean, before_scale, transformed, scaler.mean_, scaler.scale_)''',
 'categorical_encoding':'''import numpy as np
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
            np.testing.assert_array_equal(before, encoder.categories_[0])''',
 'preprocessing_pipeline':'''from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def compose(estimator):
    numerical = Pipeline([("impute", SimpleImputer(strategy="mean")), ("scale", StandardScaler())])
    columns = ColumnTransformer([("distance", numerical, ["distance"]),
                                 ("zone", OneHotEncoder(handle_unknown="ignore"), ["zone"])])
    return Pipeline([("prepare", columns), ("estimate", estimator)])

# In the supplied fixture runtime, estimator is the declared deterministic estimator.
# workflow = compose(estimator).fit(X_train, y_train)
# before = workflow.named_steps["prepare"].named_transformers_["distance"].named_steps["impute"].statistics_.copy()
# representation = workflow.named_steps["prepare"].transform(X_validation)
# predictions = workflow.predict(X_validation)
# inference = workflow.predict(bounded_inference)
# assert (before == workflow.named_steps["prepare"].named_transformers_["distance"].named_steps["impute"].statistics_).all()
# print(representation, predictions, inference)''',
 'prediction_boundary_leakage':'''import pandas as pd
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
      [row["order_key"] for row in fixture["failure_fit_rows"]])''',
 'leakage_safe_features':'''from datetime import datetime

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
print("accepted, total, augmented accepted, augmented total:", original, total, augmented, later_total)'''
}


# The estimator implementation is supplied runtime scaffolding, copied from the registry.
code['preprocessing_pipeline'] = next(f['content'] for f in assets['ws.preprocessing_pipeline']['files'] if f['path']=='authorized_runtime.py') + '\n' + code['preprocessing_pipeline'].split('# In the supplied fixture runtime')[0] + """
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
"""

def lin(c,tbs=(),facts=(),anchors=()):
    return {'concept_ids':[c], 'teaching_block_ids':list(tbs), 'fact_ids':list(facts), 'anchors':list(anchors)}
def prose(c,text,tbs,facts,role):
    return {'type':'prose','text':text,'role':role,'lineage':lin(c,tbs,facts)}
def table(c,aid,cols=None,caption=None):
    ref={'asset_id':aid}
    if cols:ref['columns']=cols
    return {'type':'data_table','asset_ref':ref,'caption':caption or assets[aid]['title'], 'lineage':lin(c,anchors=[c+'#visual'])}
def walkthrough(c,key,text=None,fixture_keys=None):
    data=fixture[key]
    if fixture_keys is not None:data={k:data[k] for k in fixture_keys}
    return {'type':'code_walkthrough','language':'python','code':'fixture = '+pprint.pformat(data,sort_dicts=False,width=90)+'\n\n'+(text or code[key]),'reveal':'all','lineage':lin(c,anchors=[c+'#visual'])}

def visual(c,kind):
    key=c.removeprefix('mle.')
    if key=='prediction_task_definition':
        aid='ds.outcome_counts';a=assets[aid]
        cols=[v['name'] for v in a['columns']];count=chr(65+cols.index('target_count'));den=chr(65+cols.index('population_count'));end=chr(65+len(cols))
        grid={'type':'spreadsheet_grid','asset_ref':{'asset_id':aid},'range':f'A1:{end}{len(a["rows"])+1}','show_formula_bar':True,'cells':[{'ref':f'{end}{i+2}','formula':f'={count}{i+2}/{den}{i+2}','note':'Outcome count divided by this row\'s specified population total.'} for i in range(len(a['rows']))], 'annotations':[{'target':f'{end}1','text':'Outcome proportion'}], 'lineage':lin(c,anchors=[c+'#visual'])}
        return [table(c,'ds.task_record'),grid]
    if key=='numpy_dtype_selection':
        left=walkthrough(c,key,fixture_keys=['a','candidate_dtypes','boundary_values','tolerance','element_storage_budget'])
        right=walkthrough(c,key,'''import numpy as np
reference = np.array(fixture["integer_cast_probe"]["reference"], dtype=np.float64)
candidate = reference.astype(fixture["integer_cast_probe"]["candidate_dtype"])
print("retained reference, integer candidate, arithmetic difference:", reference, candidate, candidate - reference)''',fixture_keys=['integer_cast_probe'])
        return [table(c,D[key][0]),{'type':'side_by_side','left':left,'right':right,'left_label':'Floating candidates and boundary probe','right_label':'Integer cast contrast','takeaway':'Check fidelity against retained references as well as the supplied element budget.', 'lineage':lin(c,anchors=[c+'#visual'])}]
    if key=='sensitive_ml_assets':
        before=table(c,'ds.audit_sample',caption='Dummy input only: possession is not authorization to redistribute these fields.')
        after=table(c,'ds.audit_sample',cols=fixture[key]['permitted_fields'],caption='New permitted-field record: runtime secrets remain outside generated diagnostics.')
        return [{'type':'before_after','before':before,'after':after,'change_summary':'Dictionary membership selects only supplied permitted fields; dummy restricted values are excluded. Credentials stay in the authorized runtime secret mechanism.', 'lineage':lin(c,anchors=[c+'#visual'])}]
    tables=[table(c,a) for a in D[key]]
    return tables+[walkthrough(c,key)]

def split_fact_prose(c,texts,tbs,fids,role):
    # Partition by factual units, not arbitrary mid-sentence cuts.
    out=[];group=[];ids=[]
    for text,fid in zip(texts,fids):
        if group and words(' '.join(group+[text]))>85:
            out.append(prose(c,' '.join(group),tbs,ids,role));group=[];ids=[]
        group.append(text);ids.append(fid)
    if group:out.append(prose(c,' '.join(group),tbs,ids,role))
    return out

def facttexts(c,fids):
    fs=F[c.removeprefix('mle.')].split('|')
    return [fs[int(fid.rsplit('#f',1)[1])-1] for fid in fids]

# Derive next-tile first concept from glossary TOC membership, never guess from a tile id.
first_by_tile={}
for v in g['bundles']:
    first_by_tile.setdefault(v['context']['toc_location']['tile_id'],v['context']['concept_id'])
for t in p['tiles']: first_by_tile[t['tile_id']]=t['concept_ids'][0]
result={'schema_version':'0.1.0','kind':'screens_part','path_id':p['path_id'],'batch_id':p['batch_id'],'tiles':[]}
for t in p['tiles']:
    tile={'tile_id':t['tile_id'],'title':' / '.join(bundles[c]['teaching_blocks'][0]['title'] for c in t['concept_ids']), 'summary':'Prepare the fictional delivery fixtures under explicit prediction, data and handling contracts.', 'steps':[], 'remediation_steps':[]}
    for s in t['steps']:
        cs=s['concept_ids'];c=cs[0];key=c.removeprefix('mle.');v=bundles[c];typ=s['type']
        lineage={'concept_ids':cs,'teaching_block_ids':s['teaching_block_ids'],'fact_ids':s['fact_ids'],'segment_ids':s['segment_ids'],'anchors':s['anchors']}
        st={'step_id':s['step_id'],'type':typ,'concept_ids':cs,'title':'','eyebrow':{'explainer':'Working rule','video':'Optional walkthrough','check':'Check your judgement','hands_on':'Practice','recap':'Takeaways'}[typ],'lineage':lineage}
        if typ in ('check','hands_on'):
            if typ=='hands_on' and s['planned_interaction_type'] in ('classify','choice'):
                st['title']='Review '+v['teaching_blocks'][0]['title'].lower()
                st['lede']='Read the supplied excerpts in this step and decide which satisfy the stated contract and which are defective or unsafe.'
            elif typ=='check':
                st['title']='Judge the '+v['teaching_blocks'][0]['title'].lower()+' decision'
                st['lede']='Choose the interpretation that satisfies the supplied contract.'
            else:
                st['title']='Verify '+v['teaching_blocks'][0]['title'].lower()
                st['lede']='Use the supplied fixtures to implement the stated rule and check normal, boundary and failure cases.'
        elif typ=='video':
            st['title']='Trace the working rule'
            st['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
        elif typ=='recap':
            st['title']='Keep the contracts explicit';st['blocks']=[]
            for rc in cs:
                rk=rc.removeprefix('mle.');rv=bundles[rc]
                # Short synthesis per concept, supported by the planned teaching facts.
                takeaway=C[rk]
                ids=[rc+'#'+f['id'] for f in rv['coverage']['required_facts']]
                tbs=[rc+'#'+tb['id'] for tb in rv['teaching_blocks'] if tb['fact_ids']]
                st['blocks'].append(prose(rc,takeaway,tbs,ids,'takeaway'))
            nc=first_by_tile.get(t['next_tile_id'])
            if nc is None:
                names=list(g['names']); nc=names[names.index(t['concept_ids'][-1])+1]
            st['blocks'].append({'type':'up_next','title':g['names'][nc],'text':'Next: '+g['names'][nc]+'.'})
        else:
            st['blocks']=[]
            for tbid in s['teaching_block_ids']:
                tb=next(tb for tb in v['teaching_blocks'] if tb['id']==tbid.split('#')[1])
                fids=[c+'#'+f for f in tb['fact_ids']]
                if tb['purpose']=='intro':
                    st['blocks'].append(prose(c,'Before accepting a delivery-fixture result, state the contract and the checks this rule requires.',[tbid],[],'intro'))
                elif tb['purpose']=='example':st['blocks'].append(prose(c,E[key],[tbid],fids,'example'))
                elif tb['purpose']=='misconception':st['blocks'].append(prose(c,C[key],[tbid],fids,'misconception'))
                else:st['blocks']+=split_fact_prose(c,facttexts(c,fids),[tbid],fids,tb['purpose'] if tb['purpose'] in ('definition','mechanism') else 'mechanism')
            st['title']=next(tb['title'] for tb in v['teaching_blocks'] if c+'#'+tb['id']==s['teaching_block_ids'][0])
            if s['planned_visual_block_type']:st['blocks']+=visual(c,s['planned_visual_block_type'])
        tile['steps'].append(st)
        if typ in ('check','hands_on'):
            fids=s['fact_ids']
            tbs=[c+'#'+tb['id'] for tb in v['teaching_blocks'] if any(c+'#'+f in fids for f in tb['fact_ids'])]
            rid=f'{t["tile_id"]}.r{len(tile["remediation_steps"])+1:02d}'
            rem={'step_id':rid,'type':'remediation','required':False,'concept_ids':[c],'title':'Contrast: '+v['teaching_blocks'][0]['title'], 'eyebrow':'Try the rule again','lineage':lin(c,tbs,fids), 'blocks':split_fact_prose(c,facttexts(c,fids),tbs,fids,'definition')+[prose(c,C[key],tbs,fids,'example')]}
            # Dataset remains the same as the original concept's teaching fixture.
            rem['blocks'].append(table(c,D[key][0],caption='Use the same supplied fixture to distinguish the two interpretations.'))
            tile['remediation_steps'].append(rem)
    result['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print('Wrote',len(result['tiles']),'tiles;',sum(len(t['steps']) for t in result['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in result['tiles']),'remediation steps')
