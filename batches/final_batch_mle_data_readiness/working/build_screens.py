import json, re, copy, pprint
from pathlib import Path
P=Path('batches/final_batch_mle.region.data_readiness')
plan=json.loads((P/'tile_plans.json').read_text()); gloss=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); reg=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in gloss['bundles']}; A={a['asset_id']:a for a in reg['assets']}
F={}
for a in reg['assets']:
 if a['asset_kind']=='code_workspace': F[a['asset_id'][3:]]=json.loads(next(f['content'] for f in a['files'] if f['path']=='fixtures.json'))
# Each entry revoices the glossary blocks, in their original order.
TEXT={
'prediction_task_definition':[
'Before preparing delivery examples, settle what the prediction means. A task record prevents different decision times or meanings of late from being mistaken for the same task.',
'Define the inference you want and the example data that supports it. Use only inputs available at prediction time. For an empirical outcome proportion, divide the outcome count by the specified population total. For a conditional proportion, restrict both counts to the specified group.',
'Keep prediction unit, target event or value, prediction time and judging horizon in separate task-record fields. That makes the relationship between each example and its target explicit.',
'The registered task record describes an accepted order, not a whole zone. Its allowed inputs are decision-time information; eventual arrival belongs on the target side. Changing the unit or horizon changes the question, not just the implementation. In the count sheet, the all-orders denominator and the specified-zone denominator describe different populations. Calculate each proportion from its own row, and keep its population and horizon visible. The zone result does not describe every zone.',
'Later arrival can establish the target outcome, but cannot supply an acceptance-time input. Likewise, a proportion for the specified zone is not a proportion for every zone.'
],
'numpy_shape_dtype':[
'The order fixture declares observations and features on different axes. Check those axes before doing arithmetic: a flat collection is not interchangeable with a batch of feature rows.',
'Import numpy as np, build np.array(fixture), and inspect ndim, shape and dtype. Under the declared batch/feature contract, first require a.ndim == 2; then compare a.shape[1] with the feature count. Each shape entry is an axis length, so check the batch requirement using a.shape[0] after rank.',
'When an input violates the contract, use a conditional raise ValueError(message). Exercise valid, boundary and failure fixtures with assert predicates. A false assertion raises AssertionError in ordinary non-optimized execution.',
'The valid fixture and flat fixture contain the same values, but they do not express the same axes. Rank must pass before you inspect a second axis. The wrong-width fixture tests a different requirement from rank; the tuple boundary tests the batch limit. Keep dtype inspection separate too: an accepted shape does not establish an accepted numerical representation. Explicit rejection protects the input boundary, while assertions exercise the declared fixture cases.',
'An element count does not explain the axes. Assertions check fixtures in ordinary non-optimized execution; they do not replace explicit rejection of invalid inputs.'
],
'numpy_dtype_selection':[
'Choose an order-array representation by inspecting preservation and storage together. A smaller dtype is useful only if its converted values satisfy the declared task requirements.',
'Numerical dtypes have representable ranges and bit widths; integer and floating candidates may preserve different values. Inspect a.dtype and compare explicit a.astype(candidate_dtype) casts. For fixed-width numerical elements, a.size × a.itemsize equals a.nbytes. That counts element storage, not other object overhead.',
'Before accepting lower precision, subtract the retained reference from the cast values. Overflow or precision loss can make a completed cast unacceptable.',
'Keep the reference while comparing both supplied candidates. Inspect their cast values, differences, itemsize and nbytes, then apply the supplied tolerance and element-storage budget. Include the boundary values and integer-cast probe rather than relying on one ordinary value. Keep the number of elements fixed: fewer elements and narrower elements are different reasons for a smaller byte count. Passing the storage budget alone does not establish preservation.',
'Fewer element bytes does not establish faithful values. Casting can overflow or lose precision, and nbytes does not measure the whole memory cost.'
],
'numpy_vectorization':[
'Apply one feature reference across the order rows with array arithmetic. The shorter expression still needs an explicit interpretation of its axes.',
'NumPy arithmetic can act elementwise instead of repeating a Python operation for each observation. Broadcasting aligns axes from the right: each pair must match or include length 1; absent leading axes count as 1. Check the result shape separately, because compatible operands can expand it.',
'Test against an independent list-comprehension reference with np.testing.assert_allclose(array_result, reference_result, rtol=..., atol=...). Supply the tolerances explicitly.',
'The fixture subtracts a per-feature reference from each order row. Build the list-comprehension result from that intended rule, then check numerical agreement and the declared shape. Contrast the column and row operands: they are compatible, but their combination expands across both positions. A completed operation is not enough if the resulting axes violate the output contract.',
'Broadcast compatibility and intended result shape are separate requirements. Compatible operands can still expand the output beyond what the task intended.'
],
'file_object_ingestion':[
'The storage location and dataset contract already exist. Retrieve the named object using the existing authorized identity, then verify how its bytes became a table.',
'With an authorized client, client.list_blobs(bucket_name, prefix=prefix) iterates matching existing objects. Select the intended name, then call bucket.blob(object_name).download_to_filename(local_path). Read CSV with pd.read_csv(local_path, dtype=declared_types); check columns, row count and value representations against the dataset contract.',
'CSV is delimited text; Parquet is columnar and supports reader-selected columns. Choose according to the supplied access pattern. For a local text identity record, use with open(path, mode, encoding="utf-8") as f and read or write inside it. Import from google.cloud import storage and construct storage.Client() with the existing authorized runtime identity.',
'Import pandas as pd. Apply the declared per-column conversions explicitly and inspect the converted values: inferred types are not a guarantee.',
'The listing includes more than one order object; the named object, not listing position, decides which to download. Verify its declared columns and row count after loading. Inspect the zero-padded order key as text after explicit conversion. Record the selected identity and local path within the text-file context. A selected-column Parquet task would use its stated access requirement; it would not excuse dropping a needed column. Listing proves availability, while inspecting the loaded table checks representation.',
'A successful download does not establish correct columns or types. Inference is not a guarantee, and access still depends on the existing authorized identity.'
],
'chunked_ingestion':[
'Work on a bounded chunk rather than collecting the entire order dataset. Keeping every processed chunk would defeat that working-array plan.',
'Iterate pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types) with a for loop instead of retaining the dataset. For homogeneous fixed-width features, R rows × F columns × W bytes is element storage. Choose a fitting chunksize and verify every materialized matrix. This estimate does not guarantee total reader or process memory.',
'Place the whole chunk iteration inside with open(...), keeping its dataset stream open until processing finishes.',
'The supplied feature width, element width and array budget determine a proposed row limit. For each materialized chunk, compare its actual element-byte calculation with nbytes and the budget. Apply the same check to the shorter final chunk without padding it. Process each chunk without retaining all earlier chunks. If the feature width changes, recalculate: the old row estimate no longer proves that the allocation fits. Keep the file context around the entire loop.',
'Chunksize is not a total-memory guarantee. The element estimate concerns the working matrix; accumulating all chunks defeats the intended bound.'
],
'dataset_inspection':[
'A readiness record should expose what was inspected, not just say the order data looks fine. Keep columns, axes and storage as named evidence.',
'Before calling data ready, inspect column names, dtypes and descriptive summaries. Report matrix shape and dtype with each axis meaning intact. Use array.nbytes for element memory, explicitly separate from total process memory.',
'Return a dictionary of named results from a parameterized inspection function. Compute feature-wise means with np.mean(numeric_values, axis=0). For standard deviation, np.std(numeric_values, axis=0, ddof=0) divides squared deviations by N before the square root. Use ddof=1 only for a stated N−1 calculation.',
'Use the registered feature columns and rows to build the matrix. Return observation count and feature count separately, alongside shape, dtype, means, spread and element bytes. Axis 0 summaries produce a result for each feature, not an average over every matrix element. The boundary fixture should return the same named fields. This makes a width mismatch distinguishable from a summary-value issue and keeps the observed representation separate from task-value summaries.',
'Total element count is not a readiness record. Also, ddof=0 is not interchangeable with a calculation that requires the N−1 divisor.'
],
'dataset_schema_validation':[
'A table can load while violating the declared distance/zone contract. Schema validation makes acceptance conditions explicit before downstream work depends on them.',
'A schema declares expected features and permitted representations or values. Missing, extra or invalid features violate it. Compare table.columns and table.dtypes with the contract first, then test constrained values using boolean predicates. Raise an explicit validation exception for a required column, type or boundary failure.',
'Use assert predicates on valid, boundary and failure fixtures. In ordinary non-optimized execution, a false predicate raises AssertionError.',
'The contract supplies inclusive distance limits and permitted zone representations. Check structure before value ranges: a missing zone column and an out-of-range distance are different failures. Exercise both limits and rejected fixtures, including an extra column and invalid spelling. The exception should identify the failed condition rather than waiting for a later estimator error. The fixtures verify that the validator neither accepts everything nor rejects everything.',
'Loading is not validation. Assertions exercise fixtures in ordinary non-optimized execution; explicit exceptions reject invalid inputs in the validation path.'
],
'dataset_cleaning_policy':[
'Repeated and invalid order observations need the supplied policy, not an unrecorded preference. The result must explain what happened to affected observations.',
'Before adding an accepted key, test membership in the accepted-key set. Use the policy dictionary to choose retain, repair or reject for detected defects or repeats. Inspect and clean examples as needed so their representations fit the intended training use.',
'Implement the chosen actions with conditional branches and report affected observation IDs rather than silently changing data. Assert the valid, boundary and failure fixtures; false predicates raise AssertionError in ordinary non-optimized execution.',
'The supplied policy rejects a repeated accepted key and repairs only the declared zone spelling. Add a key after acceptance, not after merely seeing a rejected observation. Record each repair or rejection by observation ID. A repaired row and a rejected row contribute differently to the resulting data, so keep their actions distinguishable. Check the repaired value, retained boundary and prohibited repeat. This is the dataset’s policy, not a universal deduplication rule.',
'A defect does not choose its own action. Follow the declared policy and report the affected ID; cleaning does not authorize silent rewriting.'
],
'dataset_selection_bias':[
'Compare the collected order sample with the intended population before treating its summary as population evidence. The category counts make coverage inspectable.',
'Collection or filtering can omit observations important to the intended population. Compare category count / population total for sample and target. When target membership is known, inclusion probability is included category members / all target category members. An empty denominator cannot support that rate.',
'Unequal sampling probabilities affect interpretation: a sample summary is not automatically representative. Use np.mean(numeric_values) on selected observations. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires N−1.',
'The counts support three different questions: a category’s share of the sample, its share of the target population, and the fraction of its target members included. Name each numerator and denominator before dividing. The supplied counts support unequal coverage, not an unobserved cause or inevitable model failure. Mean and standard deviation describe only the selected numerical observations with the stated divisor. If a target-category denominator is empty, record the rate as unsupported.',
'A sample statistic is not automatically a target-population statistic. Sample share, target share and category inclusion use different denominators.'
],
'label_integrity':[
'The label file may be reordered without changing observation identity. Attach labels by their intended keys and test correspondence before judging completeness.',
'Match labels through the intended unique identifier, not row position. Detect repeated IDs before constructing the dictionary: reassignment would replace an earlier value. Observation-ID minus label-ID sets reveal missing labels; the reverse difference reveals labels without observations.',
'Use keyed lookups to check label values, observation timestamps and availability timestamps against the task predicates. Later unavailable information is not an earlier prediction input. Assert valid, boundary and failure cases; false predicates raise AssertionError in ordinary non-optimized execution.',
'The label fixture reverses observation order, so positional attachment would not establish identity. Check repeats before dictionary construction and both unmatched directions before joining. On matched records, test timestamp alignment and the supplied availability boundary separately from key correspondence. A correctly keyed label can still fail a time predicate. Later label availability does not make the label available as an earlier prediction input. Reordered, missing, duplicate and boundary cases keep those requirements distinct.',
'Equal row counts do not establish matching identities. Constructing a dictionary before checking repeats can conceal them by replacing an existing value.'
],
'deployment_matched_splits':[
'The intended evaluation may concern new groups or later orders. Choose that interpretation before assigning observations to partitions.',
'Use a random split only when its sampling interpretation matches evaluation. Group dependence or time ordering can require other boundaries. Keep a common evaluation group wholly on one side and training times earlier than the intended later evaluation. Represent group membership with sets and assert an empty training/validation intersection.',
'For time-based evaluation, select training before the cutoff and evaluation within the stated later interval; check the inequalities. Report each partition’s target count / partition total. Assert valid, boundary and failure fixtures; false predicates raise AssertionError in ordinary non-optimized execution.',
'The group fixture must not separate orders from the same customer group across training and validation. Distinct order keys do not prove group separation. The separate time fixture needs timestamp inequalities: an empty group intersection does not establish chronological order. Calculate target prevalence only after assigning the deployment-matched partitions. Each proportion describes its evaluated cohort, not automatically the whole intended population, and does not retrospectively choose the boundary.',
'Random does not mean deployment-matched. Group and time boundaries answer different questions; an empty group intersection does not test timestamp ordering.'
],
 'training_fitted_imputation':[
'A missing order feature should reuse a training-learned replacement. Validation’s different values are application cases, not a new reference for the fit.',
'SimpleImputer learns a replacement per feature from fit data; strategies include mean, median, most_frequent and constant. Use SimpleImputer(strategy=declared_strategy).fit(X_train), then transform(X_validation) without fitting validation. Inspect statistics_ before and after to verify unchanged replacements.',
'Use np.mean(numeric_values, axis=0) for feature-wise means over rows. np.std(numeric_values, axis=0, ddof=0) divides squared deviations by N before the square root; use ddof=1 only when N−1 is specified. Assert valid, boundary and failure fixtures; false predicates raise AssertionError in ordinary non-optimized execution.',
'Fit the supplied strategy on training distances, then copy statistics_ before transforming validation. Check the transformed missing row and unchanged state together: they test replacement behavior and state reuse separately. Validation’s observed distance must not contribute to learning the replacement. Feature-wise mean and spread summaries use their specified observations and divisor; spread does not choose the strategy. Another supplied strategy may produce a different replacement while preserving the same fit-versus-transform boundary.',
'Fitting validation learns new state. Transforming validation reuses training state; it does not select a more convenient held-out replacement.'
],
 'training_fitted_scaling':[
'Use one fitted reference for training and later order cohorts. Inspect the training mean and scale rather than making validation define a new reference.',
'With with_mean and with_std enabled, StandardScaler centers each feature by its training mean and scales by training standard deviation. Fit on X_train and reuse transform on X_validation; inspect mean_ and scale_. A constant feature cannot gain unit variance, so its scaling factor remains 1.',
'Validation and prediction reuse training transformations, not separately fitted ones. Use np.mean(numeric_values, axis=0) for feature means. np.std(numeric_values, axis=0, ddof=0) divides squared deviations by N before the square root; use ddof=1 only if N−1 is specified.',
'Assert valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.',
'The registered training fixture includes a varying distance and a constant feature. Inspect column-wise training summaries and the stored mean_ and scale_ before transforming validation. Check that both stored arrays remain unchanged. A validation distance beyond the training range can legitimately transform beyond the training outputs; that does not justify refitting validation to zero mean. The stated centering/scaling rule depends on both configuration flags, and a constant feature still cannot become unit variance.',
'Scaling does not give every arriving cohort its own zero mean. Reuse training state; a constant feature cannot be forced to unit variance by this scaler.'
],
 'categorical_encoding':[
'Zone values determine fitted indicator columns. Specify how held-out categories behave before transforming them.',
'OneHotEncoder learns categories at fit and maps values to indicator columns. Fit training categories, inspect categories_, and transform validation without relearning. Choose handle_unknown explicitly: default error rejects an unknown category; ignore gives all-zero indicators for that feature.',
'Missing values present at fit can become a learned category; otherwise they follow unknown-category behavior. Assert valid, boundary and failure fixtures; false predicates raise AssertionError in ordinary non-optimized execution. Build the category dictionary from feature names and fitted categories_, keeping known, unseen and missing list cases aligned.',
'Inspect the stored category order rather than inventing column order from a validation batch. Known and unseen zone fixtures test the explicit policy while categories_ remains fixed. Compare missing absent from fit with missing included during fit: these can require different expectations. A batch containing only one known zone still uses the fitted mapping. All-zero unknown indicators do not mean that the unknown zone acquired its own learned category.',
'An all-zero unknown vector does not imply a learned category. Missing and unseen treatment depends on fit data and the explicit unknown policy.'
],
 'preprocessing_pipeline':[
'The distance and zone columns need different declared transformations. Keep those operations attached to the fitted prediction path rather than recreating them for each caller.',
'Construct Pipeline([(name, transformer), ..., (name, estimator)]) to chain transformations with a final estimator. fit learns transformations and estimator from training; predict applies fitted transformations first. ColumnTransformer assigns declared operations to selected columns, letting numerical and categorical features differ within one workflow.',
'Reuse the fitted pipeline for validation and bounded inference instead of learning new preprocessing state. Assert valid, boundary and failure fixtures; false predicates raise AssertionError in ordinary non-optimized execution.',
'Assign the registered numerical operations to distance and categorical operation to zone. Fit the composed workflow only on training, then use its transformed row representation and predictions for held-out inputs. Compare stored fitted state before and after these applications. The supplied estimator is fixture scaffolding, not a model-selection exercise. A malformed row must be checked against the column contract rather than silently changing which transformations a caller supplies.',
'A pipeline does not legitimize fitting held-out rows. Declared columns, training-only fit and later reuse must remain explicit.'
],
 'prediction_boundary_leakage':[
'A score can look persuasive while future fields or held-out rows reached the fitted system. Trace the fields and fit rows, not just file names.',
'Leakage uses information unavailable at prediction time and can make held-out performance overly optimistic. Audit rows and fields reaching each fit and prediction, removing held-out or future information. Separate training and evaluation before fitting preprocessing; use transform, not fit or fit_transform, for held-out inputs.',
'Assert valid, boundary and failure fixtures. False predicates raise AssertionError in ordinary non-optimized execution.',
'The eventual-arrival field is unavailable when an order is accepted; exclude it from prediction inputs. Independently inspect the preprocessing fit-row trace. Restricting only the estimator’s fit does not repair preprocessing already fitted on validation. Removing a future field addresses one boundary; splitting before fit addresses the other. Test both paths so held-out predictions use decision-available fields and training-fitted state. Different file names alone do not establish either condition.',
'Holding out a label file does not establish a leakage-free workflow. Future fields and held-out preprocessing fits can each violate the boundary.'
],
 'leakage_safe_features':[
'An order’s complete record today may include information added after an earlier prediction. Construct that earlier feature from its recorded availability boundary.',
'Derive prediction features only from information available then. Select [row for row in records if row["available_at"] <= prediction_time]. A changing lookup can differ between training and serving, so use its relevant recorded-boundary value rather than assuming today’s table is historical.',
'Compare original records with records augmented by later observations and assert the earlier feature is unchanged. Apply arithmetic only after filtering; for a sum, initialize total = 0 and accumulate total += record["value"] over accepted records.',
'Filter the fixture’s records before accumulating their values. Add the supplied later record and check that both accepted membership and the earlier total stay unchanged. A record at the permitted equality boundary tests the exact predicate. Removing timestamps after summing would not remove a later value’s contribution. For changing lookups, check the recorded historical value separately. Later source records need not be deleted; they must be excluded from the earlier calculation.',
'A timestamp is not enough if arithmetic ignores it. Filter before summing, and do not assume the latest lookup value was available historically.'
],
 'sensitive_ml_assets':[
'A useful inspection sample can also contain restricted values. Existing identity and field policy govern what a generated diagnostic record may expose.',
'Authentication and authorization govern access; possessing data or logs is not permission. Use dictionary membership checks to create a record containing only supplied permitted fields. Literal credentials in images or metadata can be exposed, so remove them from data and logs rather than treating them as diagnostics.',
'Keep the credential in the authorized runtime secret mechanism, not copied into a generated record.',
'The supplied sample includes permitted diagnostic fields and dummy restricted values. Build a new dictionary using the existing permitted-field collection; do not expand policy because another field looks useful. Inspect the returned record and captured output. Removing a token from the return value does not prevent disclosure if the input was printed first. Runtime secret delivery and permitted-field selection are distinct handling paths: preserve authorized runtime use without exposing literal credentials in data, logs, images or metadata.',
'Possession is not authorization to expose contents. Moving a credential into image metadata or a generated diagnostic record preserves the exposure risk.'
]}
# Same registered fixture, one contrast for the recovery path. Numbers and names
# appearing here are read from the registry, never manually copied from a display.
REM={
 'prediction_task_definition': 'In the task-record sheet, distance and promised delivery zone are acceptance-time inputs; eventual arrival establishes the later target. The all-orders count row and specified-zone row need their own denominators, not a shared population label.',
 'numpy_shape_dtype': 'Compare the valid order matrix with the flat fixture containing the same values. The first expresses observations and features on separate axes; the second fails the declared rank. Check rank before reading a feature axis, and reject the failure explicitly.',
 'numpy_dtype_selection': 'Compare casts of the same retained dtype-reference array, not arrays with fewer elements. A candidate can fit the supplied byte budget yet fail preservation on a boundary probe. Accepting a completed cast is different from checking its differences against the tolerance.',
 'numpy_vectorization': 'Compare the matrix-minus-feature-reference operation with the separate column-minus-row fixture. Both have compatible operands, but the latter expands across row and column positions. Test the intended result shape as well as agreement with an independent reference.',
 'file_object_ingestion': f"The fixture listing includes {F['file_object_ingestion']['object_names'][0]} and {F['file_object_ingestion']['intended_object']}. The task names the latter: listing position does not select it. After explicit conversion, inspect the declared text key {F['file_object_ingestion']['expected_order_key']!r} rather than treating inferred types as proof.",
 'chunked_ingestion': 'In the chunked-orders fixture, processing a working matrix and then releasing it differs from saving every chunk in a growing collection. Verify the actual element bytes of each matrix, including the final short chunk. The stated bound does not cover total process memory.',
 'dataset_inspection': 'In the order-feature fixture, report observations and features separately from total elements. Feature-wise means summarize rows within each column, not all matrix values together. Return the same named dictionary fields for the ordinary and boundary fixtures.',
 'dataset_schema_validation': f"The distance/zone contract accepts its lower distance boundary {F['dataset_schema_validation']['contract']['distance_min']}, but the negative fixture contains {F['dataset_schema_validation']['negative']['rows'][0][0]}. Test the inclusive predicate after the column/type checks; successful loading alone establishes neither requirement.",
 'dataset_cleaning_policy': f"The policy repairs the declared spelling {next(iter(F['dataset_cleaning_policy']['policy']['zone_repairs']))!r}, but rejects a repeated accepted order key. These are different actions, not interchangeable cleaning choices. Record the affected observation ID, and add a key only after acceptance.",
 'dataset_selection_bias': f"For {next(iter(F['dataset_selection_bias']['sample_counts']))}, sample share divides its sample count by the sample total; inclusion divides that count by the category's target count. Those denominators answer different questions. Use the selected numeric observations for descriptive summaries, not as automatic target-population evidence.",
 'label_integrity': 'The observation fixture and reversed label fixture still match by observation ID. Matching by position is different. Detect duplicate IDs before constructing the dictionary, check both set differences, then test the matched label and timestamps; a later label is not an earlier prediction input.',
 'deployment_matched_splits': f"Orders {F['deployment_matched_splits']['group_records'][0]['order_key']} and {F['deployment_matched_splits']['group_records'][1]['order_key']} share {F['deployment_matched_splits']['group_records'][0]['customer_group']}. Distinct order IDs do not permit splitting that evaluation group. An empty group intersection tests this boundary, not the separate time fixture's cutoff inequalities.",
 'training_fitted_imputation': 'In the distance-imputation fixture, a missing validation row uses the replacement learned from training. Fitting validation instead would learn new state. Check both the transformed missing row and unchanged statistics_; the selected training summaries use their own stated observations and divisor.',
 'training_fitted_scaling': 'In the distance/constant-feature fixture, transform validation with stored training mean and scale. Refitting validation is a different rule. Inspect the constant feature separately: it cannot gain unit variance, and the scaler retains its factor of 1.',
 'categorical_encoding': f"The zone fixture fits {F['categorical_encoding']['X_train'][0][0]!r} and {F['categorical_encoding']['X_train'][1][0]!r}. An unseen zone follows the explicit error or ignore policy without extending categories_. Contrast missing absent from fit with missing included during fit: only the latter can have its own learned category.",
 'preprocessing_pipeline': 'In the distance/zone fixture, validation passes through the already-fitted column transformations and estimator. Building new preprocessing state for validation is not reuse. Check fitted state before and after both validation and bounded inference, and keep the declared column assignments intact.',
 'prediction_boundary_leakage': f"The orders fixture excludes {F['prediction_boundary_leakage']['future_field']!r} from acceptance-time inputs. That fixes the field boundary, not a preprocessing fit that saw held-out rows. Separately check the fit-row trace against designated training rows, then transform held-out inputs.",
 'leakage_safe_features': f"The augmented feature-record fixture adds later value {F['leakage_safe_features']['augmented_records'][-1]['value']}. Filtering before accumulation leaves the earlier accepted list and total unchanged; summing first and removing timestamps later does not. Test the exact availability boundary and use historical lookup values where relevant.",
 'sensitive_ml_assets': f"The dummy audit sample permits {', '.join(F['sensitive_ml_assets']['permitted_fields'])}, not its token or raw customer values. Building a permitted-field dictionary differs from copying the whole sample. Inspect captured output too: printing the restricted input would expose values removed from the returned record. Keep credentials in the authorized runtime secret mechanism."
}

TAKE={
'prediction_task_definition':'Record unit, target, decision time and horizon; keep inputs decision-available and denominators population-specific.',
'numpy_shape_dtype':'Check rank before axes; reject violated contracts and test fixtures.',
'numpy_dtype_selection':'Compare preservation and element storage, not bytes alone.',
'numpy_vectorization':'Check broadcast compatibility, intended shape and independent numerical agreement.',
'file_object_ingestion':'Retrieve the named authorized object and verify its loaded representation.',
'chunked_ingestion':'Keep the stream open and verify each bounded working matrix.',
'dataset_inspection':'Return named column, axis, summary and element-storage evidence.',
'dataset_schema_validation':'Enforce declared columns, types and inclusive value boundaries.',
'dataset_cleaning_policy':'Apply declared actions and report affected observation IDs.',
'dataset_selection_bias':'Distinguish sample share, target share and category inclusion.',
'label_integrity':'Check duplicates, keyed correspondence, unmatched IDs and time predicates.',
'deployment_matched_splits':'Match group or time boundaries to the intended evaluation.',
 'training_fitted_imputation':'Learn replacements on training; transform held-out rows without changing statistics_.',
 'training_fitted_scaling':'Reuse training mean and scale, including constant-feature behavior.',
 'categorical_encoding':'Preserve fitted category mapping and explicit unseen/missing behavior.',
 'preprocessing_pipeline':'Keep column-specific transformations attached to the training-fitted prediction path.',
 'prediction_boundary_leakage':'Audit prediction-time fields and held-out fit rows independently.',
 'leakage_safe_features':'Filter by availability before arithmetic; test invariance to later records.',
 'sensitive_ml_assets':'Honor existing authorization, permitted fields and runtime secret handling.'}
# Read fixture declarations directly from registered workspace files: never hand-type values.
def fixture_prefix(key, fields=None):
 f=copy.deepcopy(F[key]); f={k:f[k] for k in fields} if fields else f
 return 'FIXTURES = '+pprint.pformat(f, width=88,sort_dicts=False)+'\n'
CODE={
'numpy_shape_dtype':'''import numpy as np

def validate(fixture, contract):
    a = np.array(fixture)
    if a.ndim != 2:
        raise ValueError("rank")
    if a.shape[1] != contract["feature_count"]:
        raise ValueError("feature width")
    if not contract["min_batch"] <= a.shape[0] <= contract["max_batch"]:
        raise ValueError("batch length")
    print(a.ndim, a.shape, a.dtype)
    return a

for name in ("valid", "tuple_boundary", "flat", "wrong_width", "too_many"):
    try:
        a = validate(FIXTURES[name], FIXTURES["contract"])
        assert a.ndim == 2
        print(name, "accepted")
    except ValueError as error:
        print(name, "rejected", str(error))
''',
'numpy_vectorization':'''import numpy as np
matrix = np.array(FIXTURES["matrix"])
offset = np.array(FIXTURES["feature_references"])
result = matrix - offset
reference = np.array([[value - offset[j] for j, value in enumerate(row)]
                      for row in FIXTURES["matrix"]])
assert result.shape == tuple(FIXTURES["expected_shape"])
np.testing.assert_allclose(result, reference,
    rtol=FIXTURES["rtol"], atol=FIXTURES["atol"])
column = np.array(FIXTURES["broadcast_column"])
row = np.array(FIXTURES["broadcast_row"])
expanded = column - row
print(matrix.shape, offset.shape, result.shape, result, reference)
print(column.shape, row.shape, expanded.shape, expanded)
''',
'file_object_ingestion':'''from google.cloud import storage
import pandas as pd

def ingest(client, bucket_name, prefix, object_name, local_path, declared_types):
    names = [blob.name for blob in client.list_blobs(bucket_name, prefix=prefix)]
    if object_name not in names:
        raise ValueError("intended object absent")
    client.bucket(bucket_name).blob(object_name).download_to_filename(local_path)
    table = pd.read_csv(local_path, dtype=declared_types)
    for column, dtype in declared_types.items():
        table[column] = table[column].astype(dtype)
    print(names, object_name, local_path, table.columns.tolist(), len(table))
    print(table.dtypes, table["order_key"].tolist())
    return table

client = storage.Client()  # Existing authorized identity; supplied local fixture client.
table = ingest(client, FIXTURES["bucket"], FIXTURES["prefix"],
    FIXTURES["intended_object"], FIXTURES["local_path"], FIXTURES["declared_types"])
assert table.columns.tolist() == FIXTURES["expected_columns"]
assert len(table) == FIXTURES["expected_row_count"]
assert table["order_key"].iloc[0] == FIXTURES["expected_order_key"]
with open(FIXTURES["identity_record_path"], "w", encoding="utf-8") as f:
    f.write(FIXTURES["intended_object"] + "\\n" + FIXTURES["local_path"])
with open(FIXTURES["identity_record_path"], "r", encoding="utf-8") as f:
    print(f.read())
''',
'chunked_ingestion':'''import pandas as pd
row_limit = FIXTURES["array_budget"] // (FIXTURES["feature_count"] * FIXTURES["element_width"])
maximum = 0
with open(FIXTURES["path"], "r", encoding="utf-8") as f:
    for chunk in pd.read_csv(f, chunksize=row_limit, dtype=FIXTURES["declared_types"]):
        matrix = chunk.to_numpy()
        rows, columns = matrix.shape
        estimate = rows * columns * matrix.itemsize
        assert estimate == matrix.nbytes
        assert matrix.nbytes <= FIXTURES["array_budget"]
        maximum = max(maximum, matrix.nbytes)
        print(rows, columns, matrix.itemsize, estimate, matrix.nbytes)
        # Process this chunk without retaining earlier chunks.
print("maximum working element bytes", maximum)
''',
'dataset_inspection':'''import numpy as np
import pandas as pd

def inspect(table, feature_columns, ddof):
    matrix = table[feature_columns].to_numpy()
    return {"columns": table.columns.tolist(), "dtypes": table.dtypes,
            "observations": matrix.shape[0], "features": matrix.shape[1],
            "shape": matrix.shape, "dtype": matrix.dtype,
            "means": np.mean(matrix, axis=0),
            "std": np.std(matrix, axis=0, ddof=ddof),
            "element_bytes": matrix.nbytes}

for name in ("fixture", "boundary"):
    fixture = FIXTURES[name]
    table = pd.DataFrame(fixture["rows"], columns=fixture["columns"])
    print(table, inspect(table, FIXTURES["feature_columns"], FIXTURES["ddof"]))
''',
'dataset_schema_validation':'''import pandas as pd

def validate(table, contract):
    if set(table.columns) != set(contract["columns"]):
        raise ValueError("column contract")
    if any(str(table.dtypes[c]) != t for c, t in contract["declared_types"].items()):
        raise ValueError("type contract")
    distance_ok = table["distance"].between(contract["distance_min"], contract["distance_max"])
    zone_ok = table["zone"].isin(contract["zone_categories"])
    print(table.columns.tolist(), table.dtypes, distance_ok, zone_ok)
    if not distance_ok.all() or not zone_ok.all():
        raise ValueError("value contract")
    return True

contract = FIXTURES["contract"]
for name in ("valid", "negative", "too_large", "missing_column", "invalid_representation", "unexpected_column"):
    fixture = FIXTURES[name]
    table = pd.DataFrame(fixture["rows"], columns=fixture["columns"])
    for column in table.columns:
        if column in contract["declared_types"]:
            table[column] = table[column].astype(contract["declared_types"][column])
    try:
        assert validate(table, contract)
        print(name, "accepted")
    except ValueError as error:
        print(name, "rejected", str(error))
''',
'dataset_cleaning_policy':'''def clean(records, policy):
    accepted_keys, cleaned, report = set(), [], []
    for original in records:
        row = dict(original)
        before = sorted(accepted_keys)
        action = "retain"
        if not policy["distance_min"] <= row["distance"] <= policy["distance_max"]:
            action = policy["invalid_distance"]
        elif row["order_key"] in accepted_keys:
            action = policy["repeat_accepted_key"]
        elif row["zone"] in policy["zone_repairs"]:
            row["zone"] = policy["zone_repairs"][row["zone"]]
            action = "repair"
        if action != "retain":
            report.append({"observation_id": row["observation_id"], "action": action})
        if action != "reject":
            cleaned.append(row)
            accepted_keys.add(row["order_key"])
        print(row["observation_id"], before, action, sorted(accepted_keys))
    return cleaned, report

cleaned, report = clean(FIXTURES["records"], FIXTURES["policy"])
assert len({r["order_key"] for r in cleaned}) == len(cleaned)
print(cleaned, report)
''',
'label_integrity':'''from datetime import datetime

def audit(observations, labels, contract):
    observed = {r["observation_id"] for r in observations}
    label_ids, repeats = set(), set()
    for label in labels:
        key = label["observation_id"]
        if key in label_ids:
            repeats.add(key)
        label_ids.add(key)
    missing, orphan = observed - label_ids, label_ids - observed
    if repeats or missing or orphan:
        return {"accepted": False, "repeats": sorted(repeats),
                "missing": sorted(missing), "orphan": sorted(orphan)}
    by_id = {r["observation_id"]: r for r in labels}
    affected = []
    cutoff = datetime.fromisoformat(contract["availability_cutoff"])
    for observation in observations:
        key = observation["observation_id"]
        label = by_id[key]
        available = datetime.fromisoformat(label["availability_timestamp"])
        time_ok = available <= cutoff if contract["availability_boundary_inclusive"] else available < cutoff
        aligned = (not contract["require_matching_observation_timestamp"] or
                   label["observation_timestamp"] == observation["observation_timestamp"])
        ok = label["label"] in contract["label_values"] and aligned and time_ok
        print(key, label, ok)
        if not ok:
            affected.append(key)
    return {"accepted": not affected, "affected": affected}

verdict = audit(FIXTURES["observations"], FIXTURES["labels"], FIXTURES["contract"])
assert verdict["accepted"]
print(verdict)
for name, labels in FIXTURES["cases"].items():
    verdict = audit(FIXTURES["observations"], labels, FIXTURES["contract"])
    assert not verdict["accepted"]
    print(name, verdict)
''',
'deployment_matched_splits':'''from datetime import datetime
records = FIXTURES["group_records"]
train = [r for r in records if r["customer_group"] in FIXTURES["training_groups"]]
validation = [r for r in records if r["customer_group"] in FIXTURES["validation_groups"]]
train_groups = {r["customer_group"] for r in train}
validation_groups = {r["customer_group"] for r in validation}
assert not train_groups & validation_groups
print(train, validation, train_groups, validation_groups, train_groups & validation_groups)
cutoff = datetime.fromisoformat(FIXTURES["cutoff"])
end = datetime.fromisoformat(FIXTURES["evaluation_end"])
train_time = [r for r in FIXTURES["time_records"]
              if datetime.fromisoformat(r["observation_timestamp"]) < cutoff]
validation_time = [r for r in FIXTURES["time_records"]
                   if cutoff <= datetime.fromisoformat(r["observation_timestamp"]) < end]
assert all(datetime.fromisoformat(r["observation_timestamp"]) < cutoff for r in train_time)
assert all(cutoff <= datetime.fromisoformat(r["observation_timestamp"]) < end for r in validation_time)
for partition in (train, validation, train_time, validation_time):
    count = sum(r["target"] for r in partition)
    print(partition, count, len(partition), count / len(partition) if partition else "unsupported")
''',
 'training_fitted_imputation':'''import numpy as np
from sklearn.impute import SimpleImputer
X_train = np.array(FIXTURES["X_train"], dtype=float)
X_validation = np.array(FIXTURES["X_validation"], dtype=float)
observed = np.array(FIXTURES["numeric_values"], dtype=float)
imputer = SimpleImputer(strategy=FIXTURES["declared_strategy"]).fit(X_train)
before = imputer.statistics_.copy()
transformed = imputer.transform(X_validation)
np.testing.assert_array_equal(before, imputer.statistics_)
assert np.all(np.isfinite(transformed))
print(X_train, X_validation, np.mean(observed, axis=0), np.std(observed, axis=0, ddof=0))
print(before, transformed, imputer.statistics_)
''',
 'training_fitted_scaling':'''import numpy as np
from sklearn.preprocessing import StandardScaler
X_train = np.array(FIXTURES["X_train"], dtype=float)
X_validation = np.array(FIXTURES["X_validation"], dtype=float)
scaler = StandardScaler(with_mean=FIXTURES["with_mean"], with_std=FIXTURES["with_std"]).fit(X_train)
before_mean, before_scale = scaler.mean_.copy(), scaler.scale_.copy()
transformed = scaler.transform(X_validation)
np.testing.assert_array_equal(before_mean, scaler.mean_)
np.testing.assert_array_equal(before_scale, scaler.scale_)
print(X_train, X_validation, np.mean(X_train, axis=0), np.std(X_train, axis=0, ddof=FIXTURES["ddof"]))
print(before_mean, before_scale, transformed, scaler.mean_, scaler.scale_)
''',
 'categorical_encoding':'''import numpy as np
from sklearn.preprocessing import OneHotEncoder

def array(rows):
    return np.array([[np.nan if v is None else v for v in row] for row in rows], dtype=object)

for training_name in ("X_train", "X_train_missing"):
    for policy in FIXTURES["unknown_policies"]:
        encoder = OneHotEncoder(handle_unknown=policy).fit(array(FIXTURES[training_name]))
        before = [categories.copy() for categories in encoder.categories_]
        dictionary = {FIXTURES["feature_name"]: encoder.categories_[0].tolist()}
        print(training_name, policy, dictionary)
        for name, rows in FIXTURES["cases"].items():
            try:
                result = encoder.transform(array(rows)).toarray()
                print(name, rows, result)
            except ValueError:
                print(name, "unknown category rejected")
            for old, current in zip(before, encoder.categories_):
                np.testing.assert_array_equal(old, current)
''',
 'preprocessing_pipeline':'''import copy
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from authorized_runtime import FixtureEstimator
numeric = Pipeline([("impute", SimpleImputer(strategy="mean")),
                    ("scale", StandardScaler(with_mean=True, with_std=True))])
columns = ColumnTransformer([("distance", numeric, ["distance"]),
                             ("zone", OneHotEncoder(handle_unknown="ignore"), ["zone"])])
pipeline = Pipeline([("columns", columns), ("estimator", FixtureEstimator())])
X_train = pd.DataFrame(FIXTURES["X_train"])
X_validation = pd.DataFrame(FIXTURES["X_validation"])
pipeline.fit(X_train, FIXTURES["y_train"])
fitted = pipeline.named_steps["columns"]
numeric_state = fitted.named_transformers_["distance"]
encoder = fitted.named_transformers_["zone"]
before = copy.deepcopy((numeric_state.named_steps["impute"].statistics_,
    numeric_state.named_steps["scale"].mean_, numeric_state.named_steps["scale"].scale_, encoder.categories_))
print(fitted.transform(X_validation), pipeline.predict(X_validation))
print(pipeline.predict(X_validation.iloc[:1]))  # Bounded inference reuses fitted state.
after = (numeric_state.named_steps["impute"].statistics_,
    numeric_state.named_steps["scale"].mean_, numeric_state.named_steps["scale"].scale_, encoder.categories_)
for old, current in zip(before[:3], after[:3]):
    np.testing.assert_array_equal(old, current)
for old, current in zip(before[3], after[3]):
    np.testing.assert_array_equal(old, current)
print(before, after)
''',
 'prediction_boundary_leakage':'''from authorized_runtime import TracePreprocessor, TracePredictor
features = FIXTURES["permitted_features"]
train = [{k: row[k] for k in features} for row in FIXTURES["training"]]
held_out = [{k: row[k] for k in features} for row in FIXTURES["held_out"]]
preprocessor = TracePreprocessor().fit(train)
predictor = TracePredictor()
predictions = predictor.predict(preprocessor.transform(held_out))
assert preprocessor.fit_rows == train
assert all(FIXTURES["future_field"] not in row for row in train + held_out)
assert preprocessor.transform_rows[-1] == held_out
assert predictor.input_rows[-1] == held_out
print(features, preprocessor.fit_rows, preprocessor.transform_rows, predictor.input_rows)
# Independent failures: future-field selection and held-out rows reaching fit.
print(FIXTURES["failure_features"], FIXTURES["failure_fit_rows"])
''',
 'leakage_safe_features':'''from datetime import datetime

def feature(records, prediction_time):
    boundary = datetime.fromisoformat(prediction_time)
    accepted = [row for row in records
                if datetime.fromisoformat(row["available_at"]) <= boundary]
    total = 0
    for record in accepted:
        total += record["value"]
    return accepted, total

original = feature(FIXTURES["records"], FIXTURES["prediction_time"])
augmented = feature(FIXTURES["augmented_records"], FIXTURES["prediction_time"])
assert original == augmented
print(FIXTURES["prediction_time"], FIXTURES["records"], original)
print(FIXTURES["augmented_records"], augmented)
'''
}

def lin(cid,tbs=(),facts=(),anchors=()):
 return {'concept_ids':[cid], 'teaching_block_ids':list(tbs), 'fact_ids':list(facts), **({'anchors':list(anchors)} if anchors else {})}
def prose(text,cid,tbs,facts,role):
 return {'type':'prose','text':text,'role':role,'lineage':lin(cid,tbs,facts)}
def cw(code,L):return {'type':'code_walkthrough','language':'python','code':code,'reveal':'all','lineage':copy.deepcopy(L)}
def table(asset,L):return {'type':'data_table','asset_ref':{'asset_id':asset},'lineage':copy.deepcopy(L)}
def visual(s):
 cid=s['concept_ids'][0]; key=cid[4:]; L=lin(cid,s['teaching_block_ids'],s['fact_ids'],[cid+'#visual']); typ=s['planned_visual_block_type']
 if key=='prediction_task_definition':
  counts=A['ds.outcome_counts']; n=len(counts['rows'])+1
  return [{'type':'spreadsheet_grid','asset_ref':{'asset_id':'ds.task_record'},'range':f"A1:B{len(A['ds.task_record']['rows'])+1}",'sheet_name':'Task record','lineage':copy.deepcopy(L)},
  {'type':'spreadsheet_grid','asset_ref':{'asset_id':'ds.outcome_counts'},'range':f'A1:E{n}','sheet_name':'Outcome counts','show_formula_bar':True,
   'cells':[{'ref':f'E{i}','formula':f'=B{i}/C{i}','note':'Outcome count divided by this row’s population count.'} for i in range(2,n+1)],'lineage':copy.deepcopy(L)}]
 if key=='numpy_dtype_selection':
  def cast_code(dtype):
   return fixture_prefix(key)+'''import numpy as np
reference = np.array(FIXTURES["a"], dtype="float64")
probe = np.array(FIXTURES["boundary_values"], dtype="float64")
'''+f'candidate_dtype = {dtype!r}\n'+'''candidate = reference.astype(candidate_dtype)
converted_probe = probe.astype(candidate_dtype)
differences = candidate.astype("float64") - reference
probe_differences = converted_probe.astype("float64") - probe
preserved = (np.all(np.abs(differences) <= FIXTURES["tolerance"]) and
             np.all(np.abs(probe_differences) <= FIXTURES["tolerance"]))
fits = candidate.nbytes <= FIXTURES["element_storage_budget"]
print(reference, candidate, differences, probe, converted_probe, probe_differences)
print(candidate.dtype, candidate.size, candidate.itemsize,
      candidate.size * candidate.itemsize, candidate.nbytes, preserved, fits, preserved and fits)
integer_probe = FIXTURES["integer_cast_probe"]
integer_reference = np.array(integer_probe["reference"])
integer_cast = integer_reference.astype(integer_probe["candidate_dtype"])
print(integer_reference, integer_cast, integer_cast - integer_reference)
'''
  dtypes=F[key]['candidate_dtypes']
  return [{'type':'side_by_side','left':cw(cast_code(dtypes[0]),L),'right':cw(cast_code(dtypes[1]),L),'left_label':dtypes[0],'right_label':dtypes[1],'takeaway':'Keep the reference and test both preservation and element-storage budget.','lineage':L}]
 if key=='dataset_selection_bias':
  return [table('ds.selection_counts',L),cw(fixture_prefix(key)+'''import numpy as np
sample, target = FIXTURES["sample_counts"], FIXTURES["target_counts"]
for zone in target:
    sample_share = sample[zone] / sum(sample.values())
    target_share = target[zone] / sum(target.values())
    inclusion = sample[zone] / target[zone] if target[zone] > 0 else "unsupported"
    print(zone, sample[zone], sum(sample.values()), sample_share,
          target[zone], sum(target.values()), target_share, inclusion)
values = np.array(FIXTURES["numeric_values"])
print(values, np.mean(values), np.std(values, ddof=FIXTURES["ddof"]))
''',L)]
 if key=='sensitive_ml_assets':
  before=fixture_prefix(key,['sample','permitted_fields'])+'# Illustrative dummy values only; possession is not authorization.\n'
  after=fixture_prefix(key,['sample','permitted_fields'])+'''sample = FIXTURES["sample"]
permitted = FIXTURES["permitted_fields"]
record = {key: value for key, value in sample.items() if key in permitted}
assert set(record) <= set(permitted)
print(record)  # Never print the original restricted sample.
# Credential use belongs to the existing authorized runtime secret mechanism.
'''
  return [{'type':'before_after','before':cw(before,L),'after':cw(after,L),'change_summary':'Create a new permitted-field record; do not copy restricted values into outputs or metadata.','lineage':L}]
 return [cw(fixture_prefix(key)+CODE[key],L)]

def split_short(text,cap=90):
 # Break only at sentence boundaries; code-like punctuation is not split.
 sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',text)
 result=[]; current=''
 for sentence in sentences:
  if current and len((current+' '+sentence).split())>cap:result.append(current);current=''
  current=(current+' '+sentence).strip()
 if current:result.append(current)
 return result

def teaching_prose(cid,tb):
 key=cid[4:]; index=int(tb['id'][2:])-1
 text=TEXT[key][index]
 tbs=[cid+'#'+tb['id']];facts=[cid+'#'+f for f in tb['fact_ids']]
 return [prose(chunk,cid,tbs,facts,tb['purpose']) for chunk in split_short(text)]

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for tile in plan['tiles']:
 cids=tile['concept_ids']; title=' · '.join(B[c]['teaching_blocks'][0]['title'] for c in cids)
 # Shared glossary chapter labels need not be repeated within a tile.
 title=' · '.join(dict.fromkeys(title.split(' · ')))
 target={'tile_id':tile['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 for s in tile['steps']:
  cid=s['concept_ids'][0]; b=B[cid]; key=cid[4:]
  lineage=lin(cid,s['teaching_block_ids'],s['fact_ids'],s['anchors'])
  if len(s['concept_ids'])>1:lineage['concept_ids']=s['concept_ids'][:]
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'][:],'title':b['context']['concept_name'],'lineage':lineage}
  if s['type']=='explainer':
   step['blocks']=[]
   for tbid in s['teaching_block_ids']:
    concept,short=tbid.split('#');tb=next(tb for tb in B[concept]['teaching_blocks'] if tb['id']==short)
    step['blocks']+=teaching_prose(concept,tb)
   first_id=s['teaching_block_ids'][0].split('#')[1]
   step['title']={'tb1':b['context']['concept_name']}.get(first_id, next(tb['title'] for tb in b['teaching_blocks'] if tb['id']==first_id))
   if s['planned_visual_block_type']:step['blocks']+=visual(s)
  elif s['type']=='video':
   step['title']='A worked perspective';step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids'][:]}]
  elif s['type'] in ['check','hands_on']:
   step['eyebrow']='Check your understanding' if s['type']=='check' else 'Apply the contract'
   step['title']=('Choose the supported rule' if s['type']=='check' else 'Work with the supplied fixture')
   # Framing only: no interaction or teaching blocks are authored here.
  elif s['type']=='recap':
   step['title']='Takeaways'; step['blocks']=[]
   for c in cids:
    relevant=[c+'#'+tb['id'] for tb in B[c]['teaching_blocks'] if tb['fact_ids']]
    facts=[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]
    step['blocks'].append(prose(TAKE[c[4:]],c,relevant,facts,'takeaway'))
   next_tile=next((t for t in plan['tiles'] if t['tile_id']==tile['next_tile_id']),None)
   next_cid=next_tile['concept_ids'][0] if next_tile else list(gloss['names'])[int(tile['next_tile_id'].split('.')[-1].split('_')[0])]
   step['blocks'].append({'type':'up_next','title':gloss['names'][next_cid],'text':'Next: '+gloss['names'][next_cid]+'.'})
  target['steps'].append(step)
 # Each distinct assessed fact set gets a separately targetable recovery screen.
 seen=set()
 for s in tile['steps']:
  if s['type'] not in ['check','hands_on']:continue
  for cid in s['concept_ids']:
   facts=[f for f in s['fact_ids'] if f.startswith(cid+'#')]
   signature=(cid,tuple(sorted(facts)))
   if signature in seen:continue
   seen.add(signature);b=B[cid];key=cid[4:]
   teaching=[tb for tb in b['teaching_blocks'] if set(tb['fact_ids']) & {f.split('#')[1] for f in facts} and tb['purpose'] in ['definition','mechanism']]
   rid=tile['tile_id']+f'.r{len(target["remediation_steps"])+1:02d}'
   blocks=[]
   # Retain complete fact meanings from the specific teaching blocks, with matching lineage.
   for tb in teaching:blocks+=teaching_prose(cid,tb)
   example=next(tb for tb in b['teaching_blocks'] if tb['purpose']=='example')
   misconception=next(tb for tb in b['teaching_blocks'] if tb['purpose']=='misconception')
   # A bounded same-fixture contrast, not a second interaction or a new topic.
   contrast=REM[key]
   blocks.append(prose(contrast,cid,[cid+'#'+example['id'],cid+'#'+misconception['id']],list(dict.fromkeys(facts+[cid+'#'+f for f in misconception['fact_ids']])),'misconception'))
   target['remediation_steps'].append({'step_id':rid,'type':'remediation','required':False,'concept_ids':[cid],'title':'Revisit: '+b['context']['concept_name'],'blocks':blocks,'lineage':lin(cid,[cid+'#'+tb['id'] for tb in teaching]+[cid+'#'+example['id'],cid+'#'+misconception['id']],facts)})
 out['tiles'].append(target)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Stage-local deterministic checklist, beyond the JSON Schema gate.
issues=[]
for planned,tile in zip(plan['tiles'],out['tiles']):
 assert [(s['step_id'],s['type'],s['concept_ids']) for s in planned['steps']]==[(s['step_id'],s['type'],s['concept_ids']) for s in tile['steps']]
 for ps,s in zip(planned['steps'],tile['steps']):
  assert s['lineage']['fact_ids']==ps['fact_ids'] and s['lineage']['teaching_block_ids']==ps['teaching_block_ids']
  text_words=sum(len(block.get('text','').split()) for block in s.get('blocks',[]) if block['type'] in ['prose','up_next'])
  if text_words>ps['word_budget']:issues.append((s['step_id'],'budget',text_words,ps['word_budget']))
  if ps['type'] in ['check','hands_on']:assert 'blocks' not in s and 'interaction' not in s
  if ps['type']=='video':assert s['blocks']==[{'type':'media_group','segment_ids':ps['segment_ids']}]
 for s in tile['steps']+tile['remediation_steps']:
  def inspect_block(block):
   for k in ['output','computed_values','result','execution_provenance']:assert k not in block
   if block['type']=='prose':
    assert 'lineage' in block and len(block['text'].split())<=90
    assert not re.search(r'\bvideo\b',block['text'],re.I)
   if 'lineage' in block:
    for k in ['fact_ids','teaching_block_ids','anchors']:
     for value in block['lineage'].get(k,[]):assert '#' in value
   if 'asset_ref' in block:assert block['asset_ref']['asset_id'] in A
   for k in ['left','right','before','after']:
    if k in block:inspect_block(block[k])
  for block in s.get('blocks',[]):inspect_block(block)
report={'tiles':len(out['tiles']),'steps':sum(len(t['steps']) for t in out['tiles']),'remediation_steps':sum(len(t['remediation_steps']) for t in out['tiles']),'word_budget_issues':issues,'counts_by_tile':[{ 'tile_id':t['tile_id'],'steps':len(t['steps']),'remediation_steps':len(t['remediation_steps'])} for t in out['tiles']]}
(P/'working/screens_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert not issues
