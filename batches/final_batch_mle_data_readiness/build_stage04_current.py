import json, sys, pprint, copy
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_mle.region.data_readiness')
load=lambda p:json.loads((B/p).read_text())
plans=load('tile_plans.json'); screens=load('screens.json'); registry=load('scenario_asset_registry.json'); glossary=load('inputs/path_glossary_bundle.json')
g={x['context']['concept_id']:x for x in glossary['bundles']}; assets={a['asset_id']:a for a in registry['assets']}
fx={a['asset_id'][3:]:json.loads(next(f['content'] for f in a['files'] if f['path']=='fixtures.json')) for a in registry['assets'] if a['asset_kind']=='code_workspace'}
py=lambda v:pprint.pformat(v,width=95,sort_dicts=False)
checks={
'prediction_task_definition':('At order acceptance, which field must be excluded from the prediction inputs?', 'Eventual arrival time','Distance known at acceptance','Promised delivery zone known at acceptance','The eventual arrival is later information used to judge the target.','Distance is already available at the declared prediction time.','The promised zone is already available at the declared prediction time.'),
'numpy_shape_dtype':('A batch/feature contract requires rank two and two features. What should happen before reading the second axis length?','Check rank; reject invalid rank with ValueError.','Index shape[1] immediately, even for a flat fixture.','Accept any fixture with the same total number of values.','Rank must be checked before accessing a possibly absent axis.','A flat fixture has no second axis to inspect.','Value count alone does not establish the declared batch/feature axes.'),
'numpy_dtype_selection':('A cast saves element bytes but changes a reference value beyond the supplied tolerance. Under a precision-and-budget contract, should it be accepted?','No: it violates the value-preservation requirement.','Yes: lower element storage alone establishes acceptance.','Yes: a successful cast guarantees preserved values.','Both value preservation and element-storage requirements must hold.','Element bytes do not establish precision preservation.','A cast may lose precision or overflow.'),
'numpy_vectorization':('Compatible broadcasting produces a larger result than the declared output shape. Which conclusion follows?','The operation is compatible but its output fails the declared shape contract.','Compatibility alone proves the intended result is correct.','Numerical closeness alone removes the need for a shape check.','Check intended output shape as well as compatible operands and values.','Compatibility permits expansion and does not establish intent.','Both the intended shape and numerical agreement need checks.'),
'file_object_ingestion':('The authorized prefix lists orders-a.csv and orders-b.csv; the task names orders-b.csv. Which retrieval rule follows the contract?','Select the named orders-b.csv object and download it to the supplied local path.','Select whichever object appears first in the listing.','Treat the prefix itself as the dataset object.','A listing supplies names; retrieve the specifically named object.','Listing order does not identify the requested dataset.','A prefix is not the named CSV object.'),
'chunked_ingestion':('A CSV chunk row limit was chosen from an array-element budget. What claim can checked matrix.nbytes values support?','Each checked materialized chunk array fits the element budget.','The whole process uses no more than that array budget.','The last short chunk does not require checking.','The bound is on checked single-chunk element allocations.','Element bytes exclude reader and other process allocations.','Every materialized matrix needs checking, including a short final chunk.'),
'dataset_inspection':('For a matrix whose rows are observations and columns are features, which mean summarizes each feature over observations?','np.mean(numeric_values, axis=0)','np.mean(numeric_values, axis=1)','One overall mean with no axis selection','Axis zero summarizes rows separately for each feature.','Axis one summarizes features within each observation instead.','A pooled mean does not preserve the feature-wise summaries.'),
'dataset_schema_validation':('A table has an unexpected column, but its distance values are in range. Under an exact-column contract, what should validation do?','Reject the column violation before accepting value predicates.','Accept because the distance values are in range.','Silently delete the unexpected column during validation.','Schema validity includes the declared columns and types, not only values.','Passing one value rule does not satisfy the exact-column rule.','This validation contract rejects violations rather than cleaning them.'),
'dataset_cleaning_policy':('The policy rejects invalid distance rows and later repeats of accepted keys. An invalid row occurs before a valid row with the same key. When should the key enter the accepted-key set?','Only after the row is accepted.','Before checking its distance.','For every rejected row as well as accepted rows.','A rejected row must not reserve an accepted key.','Adding it first could wrongly reject the later valid row.','The repeat policy concerns already accepted keys, not rejected rows.'),
'dataset_selection_bias':('Zone B has a lower inclusion probability than zone A in the supplied selection counts. What is a justified limitation?','The selected sample has lower inclusion for B; the counts alone do not identify a cause or inevitable prediction failure.','The counts prove the reason B was less likely to be selected.','The counts guarantee prediction failure for every B order.','Report the observed selection limitation without an unsupported causal or performance claim.','The supplied counts quantify selection, not its cause.','Selection counts do not establish inevitable prediction failure.'),
'label_integrity':('Label rows are reversed relative to observation rows, but IDs and required timestamps match. How should alignment be determined?','Match labels to observations by ID and check the supplied predicates.','Attach labels by row position.','Replace repeated IDs in a dictionary before checking for repeats.','Identity alignment is independent of label row order.','Position can associate an observation with the wrong label.','Dictionary replacement can hide repeated IDs before the audit reports them.'),
'deployment_matched_splits':('The declared deployment scenario is prediction for previously unseen customer groups. Which split respects this boundary?','Keep every customer group wholly in one partition.','Put different orders from the same group on opposite sides.','Require equal target proportions instead of group separation.','Group sets must have no intersection.','Splitting a group across sides violates the unseen-group boundary.','Reporting proportions does not replace the declared group separation.'),
'training_fitted_imputation':('An imputer is fitted on training rows. Validation includes a missing distance. Which operation respects the fitting boundary?','Transform validation using the stored training statistic.','Fit a new statistic on validation before replacing its missing value.','Combine training and validation to refit the replacement statistic.','Validation receives the training-fitted replacement without refitting.','A validation fit changes the intended training-only statistic.','Combining rows allows held-out information into fitted preprocessing.'),
'training_fitted_scaling':('Training and validation distances differ. Which scaling path preserves the training representation?','Fit on training, then transform validation using the stored mean_ and scale_.','Fit a separate scaler on validation.','Refit on combined rows before transforming validation.','Unseen inputs use the stored training parameters.','Separate validation fitting uses a different transformation.','Combined fitting violates training-only parameter estimation.'),
'categorical_encoding':('A category was absent during encoder fit and handle_unknown is explicitly ignore. What does transform produce for that feature?','All-zero indicators, without learning a new category.','A newly learned indicator added during transform.','A guaranteed ValueError despite the ignore policy.','Ignore gives all-zero indicators for an unseen category.','Transform preserves the training-fitted mapping and width.','Error is the other declared policy; it is not ignore.'),
'preprocessing_pipeline':('A fitted preprocessing pipeline is ready for validation. Which call preserves the fitted preprocessing state?','Use the same fitted pipeline predict path on validation.','Fit a fresh pipeline on validation first.','Fit the existing pipeline again on validation before predict.','Prediction uses the previously fitted transformations.','A new validation fit does not reuse training-fitted state.','Refitting changes the state instead of reusing it.'),
'prediction_boundary_leakage':('An acceptance-time workflow fits preprocessing using held-out rows and includes eventual arrival as a prediction input. Which correction addresses both defects?','Fit preprocessing only on training rows and exclude eventual arrival from prediction inputs.','Exclude eventual arrival but keep the held-out preprocessing fit.','Fit only on training but retain eventual arrival as an input.','Both row and field information boundaries must hold.','Removing the future field leaves held-out information in the fit.','Training-only fitting does not make a future target-side field available at acceptance.'),
'leakage_safe_features':('A historical prediction uses a changing lookup. Which values should form its features?','Values available at the recorded prediction boundary.','The latest lookup values regardless of their availability time.','All later observations because they are now known.','The relevant recorded boundary determines information availability.','The latest lookup is not necessarily the historical lookup.','Later information cannot enter the earlier feature.'),
'sensitive_ml_assets':('The diagnostic policy permits only run_id and row_count. What should a generated record contain?','Only those permitted values; keep credentials in the authorized secret mechanism.','Also copy the token because the reader is authorized.','Also copy raw customer values to make diagnostics detailed.','Authorization does not expand the supplied permitted-field policy.','The credential remains in the secret mechanism, not the generated record.','Restricted raw values are excluded by the supplied field policy.')}
code={}
def add(name,prompt,starter,body,exprs,mounts=None,packages=None):
 code[name]={'prompt':prompt,'starter':starter,'solution':starter+'\n'+body,'exprs':exprs,'mounts':mounts or [],'packages':packages or ['numpy']}
def inputs(**kw):return ''.join(k+' = '+py(v)+'\n' for k,v in kw.items())
# First array contract: no conversions or reshape hide invalid dimensions.
f=fx['numpy_shape_dtype'];s=inputs(valid=f['valid'],tuple_boundary=tuple(map(tuple,f['tuple_boundary'])),empty=f['empty'],flat=f['flat'],wrong_width=f['wrong_width'],too_many=f['too_many'])
body='''import numpy as np
def validate(fixture):
    a = np.array(fixture)
    rank = a.ndim
    shape = a.shape
    dtype = a.dtype
    rank_ok = rank == 2
    if not rank_ok:
        raise ValueError("rank")
    batch = shape[0]
    width = shape[1]
    batch_ok = batch >= 1 and batch <= 3
    width_ok = width == 2
    if not batch_ok or not width_ok:
        raise ValueError("dimensions")
    return a
accepted = validate(valid)
boundary = validate(tuple_boundary)
rank = accepted.ndim
shape = accepted.shape
dtype = accepted.dtype
batch = shape[0]
width = shape[1]
rank_ok = rank == 2
batch_ok = batch >= 1 and batch <= 3
width_ok = width == 2
assert accepted.shape == (3, 2)
assert boundary.shape == (1, 2)
'''
for name in ['empty','flat','wrong_width','too_many']:
 body+=f'''try:
    validate({name})
    assert False
except ValueError:
    {name}_rejected = True
assert {name}_rejected
'''
add('numpy_shape_dtype','Write import numpy as np and validate(fixture): accept rank-two arrays with one through three rows and exactly two features. Inspect rank before axis indexing and raise ValueError on violations; return the unchanged array. Author assertions for every supplied fixture. Expose accepted, boundary, rank, shape, dtype, batch, width, rank_ok, batch_ok, width_ok and the four named *_rejected booleans.',s,body,['[accepted.tolist(), boundary.tolist(), rank, shape, str(dtype), batch, width, rank_ok, batch_ok, width_ok, empty_rejected, flat_rejected, wrong_width_rejected, too_many_rejected]'])
f=fx['numpy_dtype_selection'];s='import numpy as np\n'+inputs(reference_rows=f['a'],candidate_dtypes=f['candidate_dtypes'],boundary_values=f['boundary_values'],tolerance=f['tolerance'],element_storage_budget=f['element_storage_budget'])+'a = np.array(reference_rows)\nboundary_reference = np.array([[v] for v in boundary_values])\n'
body='''def compare(a, candidate_dtypes, tolerance, element_storage_budget):
    reports = []
    choice = "neither"
    for candidate_dtype in candidate_dtypes:
        candidate = a.astype(candidate_dtype)
        element_bytes = candidate.size * candidate.itemsize
        preserved = True
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                difference = abs(candidate[i, j] - a[i, j])
                if difference > tolerance:
                    preserved = False
        accepted = preserved and element_bytes <= element_storage_budget
        if accepted:
            choice = candidate_dtype
        reports.append({"dtype": candidate_dtype, "count": candidate.size, "itemsize": candidate.itemsize, "element_bytes": element_bytes, "nbytes": candidate.nbytes, "preserved": preserved, "accepted": accepted})
    return {"reports": reports, "choice": choice, "scope": "element storage excludes object overhead"}
result = compare(a, candidate_dtypes, tolerance, element_storage_budget)
boundary_result = compare(boundary_reference, candidate_dtypes, tolerance, element_storage_budget)
'''
add('numpy_dtype_selection','Implement compare(a, candidate_dtypes, tolerance, element_storage_budget). Explicitly cast each candidate from the unchanged reference; check every scalar difference, including a separate invocation on boundary_reference. Return reports in candidate order with dtype, count, itemsize, element_bytes, nbytes, preserved, accepted; choice is the last accepted dtype or "neither". Include scope="element storage excludes object overhead". Expose result and boundary_result. Acceptance requires both preservation within tolerance and bytes within budget.',s,body,['[result, boundary_result, a.tolist()]'])
f=fx['numpy_vectorization'];s=inputs(matrix=f['matrix'],feature_references=f['feature_references'],rtol=f['rtol'],atol=f['atol'])
body='''import numpy as np
def transform(matrix, feature_references):
    a = np.array(matrix)
    result = a - np.array(feature_references)
    reference = np.array([[row[0] - feature_references[0], row[1] - feature_references[1]] for row in matrix])
    assert result.shape == a.shape
    np.testing.assert_allclose(result, reference, rtol=rtol, atol=atol)
    return result
result = transform(matrix, feature_references)
'''
add('numpy_vectorization','Write the NumPy import and transform(matrix, feature_references). Subtract the two per-feature references elementwise and return the array. Independently build a two-feature list-comprehension reference and assert unchanged intended shape and numerical agreement at the supplied rtol/atol. Expose result.',s,body,['result'])
f=fx['chunked_ingestion'];s=inputs(path=f['path'],declared_types=f['declared_types'],array_budget=f['array_budget'],feature_count=f['feature_count'],element_width=f['element_width'])
body='''import pandas as pd
def inspect_chunks(path, declared_types, array_budget, feature_count, element_width):
    row_limit = array_budget // (feature_count * element_width)
    largest = 0
    total_rows = 0
    chunk_rows = []
    with open(path) as file_handle:
        for chunk in pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types):
            matrix = chunk.to_numpy()
            rows, columns = matrix.shape
            element_bytes = rows * columns * matrix.dtype.itemsize
            assert element_bytes == matrix.nbytes
            assert element_bytes <= array_budget
            largest = max(largest, element_bytes)
            total_rows = total_rows + rows
            chunk_rows.append(rows)
            del matrix
    return {"row_limit": row_limit, "chunk_rows": chunk_rows, "total_rows": total_rows, "largest_element_bytes": largest, "scope": "single chunk elements, not total process memory"}
result = inspect_chunks(path, declared_types, array_budget, feature_count, element_width)
'''
# append/addition are bookkeeping scaffolding; the anchor's conceptual checks are unchanged.
add('chunked_ingestion','Implement inspect_chunks(path, declared_types, array_budget, feature_count, element_width). Choose floor(budget/(features*element width)) rows. Keep the file open while iterating typed CSV chunks, check actual shape-times-itemsize against nbytes and budget for every chunk, then release each matrix. Return result with row_limit, chunk_rows in iteration order, total_rows, largest_element_bytes and scope="single chunk elements, not total process memory".',s,body,['result'],[{'asset_id':'ds.chunked_orders','mount_path':f['path']}],['pandas'])
f=fx['dataset_inspection'];s='import numpy as np\n'+inputs(columns=f['fixture']['columns'],rows=f['fixture']['rows'],boundary_rows=f['boundary']['rows'],ddof=f['ddof'])+'numeric_values = np.array(rows)\nboundary_values = np.array(boundary_rows)\n'
body='''def inspect(columns, numeric_values, ddof=0):
    shape = numeric_values.shape
    return {"columns": columns, "column_dtypes": [numeric_values.dtype, numeric_values.dtype], "observation_count": shape[0], "feature_count": shape[1], "shape": shape, "axis_meanings": ["observations", "features"], "means": np.mean(numeric_values, axis=0), "std": np.std(numeric_values, axis=0, ddof=ddof), "dtype": numeric_values.dtype, "element_bytes": shape[0] * shape[1] * numeric_values.dtype.itemsize, "nbytes": numeric_values.nbytes, "scope": "element storage, not total process memory"}
result = inspect(columns, numeric_values, ddof)
boundary_result = inspect(columns, boundary_values, ddof)
'''
add('dataset_inspection','Implement inspect(columns, numeric_values, ddof=0) for the loaded two-feature matrix. Expose result and boundary_result. Return columns, column_dtypes, observation_count, feature_count, shape, axis_meanings=["observations","features"], means and std over rows using the supplied divisor, dtype, element_bytes, nbytes, scope="element storage, not total process memory". Reuse identical fields for both fixtures.',s,body,['[result,boundary_result]'])
f=fx['dataset_schema_validation'];s='import pandas as pd\n'+inputs(contract=f['contract'],fixtures={k:v for k,v in f.items() if k!='contract'})+'''tables = {name: pd.DataFrame(v['rows'], columns=v['columns']).astype({k:t for k,t in contract['declared_types'].items() if k in v['columns']}) for name,v in fixtures.items()}
tables['incorrect_type'] = tables['valid'].astype({'distance':'string'})
'''
body='''def validate(table, contract):
    if set(table.columns) != set(contract["columns"]):
        raise ValueError("columns")
    for column in contract["columns"]:
        if table.dtypes[column] != contract["declared_types"][column]:
            raise ValueError("dtype")
    distance = table["distance"]
    if not ((distance >= contract["distance_min"]) & (distance <= contract["distance_max"])).all():
        raise ValueError("distance")
    zone = table["zone"]
    if not ((zone == "north") | (zone == "south")).all():
        raise ValueError("zone")
    return table
assert validate(tables["valid"], contract).equals(tables["valid"])
verdicts = {}
for name in tables:
    try:
        validate(tables[name], contract)
        verdicts[name] = "accepted"
    except ValueError as error:
        verdicts[name] = str(error)
assert verdicts["valid"] == "accepted"
assert verdicts["negative"] == "distance"
assert verdicts["too_large"] == "distance"
assert verdicts["missing_column"] == "columns"
assert verdicts["unexpected_column"] == "columns"
assert verdicts["incorrect_type"] == "dtype"
assert verdicts["invalid_representation"] == "zone"
result = [tables["valid"], verdicts]
'''
add('dataset_schema_validation','Write validate(table, contract), checking exact columns then dtypes before inclusive distance range and the two permitted zone spellings. Raise ValueError("columns"), ("dtype"), ("distance") or ("zone") for the first violation and return unchanged valid input. Author assertions on every supplied table, including 0 and 100 boundaries and incorrect_type. Expose verdicts keyed by fixture name ("accepted" or error message), and result=[tables["valid"],verdicts].',s,body,['result'],packages=['pandas'])
f=fx['dataset_cleaning_policy'];s=inputs(records=f['records'],valid=f['valid'],policy=f['policy'])
body='''def clean(records, policy):
    accepted_keys = set()
    cleaned = []
    report = []
    for row in records:
        key = row["order_key"]
        if row["distance"] < policy["distance_min"] or row["distance"] > policy["distance_max"]:
            report.append({"observation_id": row["observation_id"], "action": "rejected"})
        elif key in accepted_keys:
            report.append({"observation_id": row["observation_id"], "action": "rejected_repeat"})
        else:
            new = {"observation_id": row["observation_id"], "order_key": key, "distance": row["distance"], "zone": row["zone"]}
            if row["zone"] in policy["zone_repairs"]:
                new["zone"] = policy["zone_repairs"][row["zone"]]
                report.append({"observation_id": row["observation_id"], "action": "repaired"})
            accepted_keys.add(key)
            cleaned.append(new)
    return {"cleaned": cleaned, "report": report}
result = clean(records, policy)
valid_result = clean(valid, policy)
assert result["cleaned"][1]["zone"] == "south"
assert len(result["cleaned"]) == 3
assert len(valid_result["cleaned"]) == 4
'''
add('dataset_cleaning_policy','Implement clean(records,policy) without changing the source. Reject out-of-range distance, then repeats of already accepted keys; repair only approved zone spellings. Return {cleaned: retained record dictionaries, report: affected records in input order as {observation_id,action}}. Actions are "rejected", "rejected_repeat", "repaired". Add assertions for normal, boundary, repair, rejection and repeat cases; expose result and valid_result. Also demonstrate in the supplied assertion harness that a deliberately false predicate raises AssertionError.',s,body,['[result,valid_result]'],packages=[])
f=fx['dataset_selection_bias'];s='import numpy as np\n'+inputs(sample_counts=f['sample_counts'],target_counts=f['target_counts'],numeric_rows=f['numeric_values'],ddof=f['ddof'])+'numeric_values = np.array(numeric_rows)\n'
body='''sample_total = sample_counts["zone-A"] + sample_counts["zone-B"]
target_total = target_counts["zone-A"] + target_counts["zone-B"]
sample_shares = np.array([sample_counts["zone-A"], sample_counts["zone-B"]]) / sample_total
target_shares = np.array([target_counts["zone-A"], target_counts["zone-B"]]) / target_total
inclusion = np.array([sample_counts["zone-A"], sample_counts["zone-B"]]) / np.array([target_counts["zone-A"], target_counts["zone-B"]])
mean = np.mean(numeric_values)
std = np.std(numeric_values, ddof=0)
limitation = "Zone B has lower inclusion and sample share; counts do not identify a cause or inevitable prediction failure."
'''
add('dataset_selection_bias','Calculate sample_shares, target_shares, inclusion in zone-A then zone-B order from the counts. Calculate mean and population std of numeric_values; no ingestion or model fit. Record limitation="Zone B has lower inclusion and sample share; counts do not identify a cause or inevitable prediction failure." The three proportions have different denominators.',s,body,['[sample_shares,target_shares,inclusion,mean,std,limitation]'])
f=fx['label_integrity'];s=inputs(observations=f['observations'],labels=f['labels'],cases=f['cases'],contract=f['contract'])
body='''def audit(observations, labels, contract):
    obs = {}
    lab = {}
    repeated = []
    invalid = []
    misaligned = []
    unavailable = []
    for row in observations:
        key = row["observation_id"]
        if key in obs:
            repeated.append(key)
        else:
            obs[key] = row
    for row in labels:
        key = row["observation_id"]
        if key in lab:
            repeated.append(key)
        else:
            lab[key] = row
            if row["label"] not in contract["label_values"]:
                invalid.append(key)
            if key in obs and row["observation_timestamp"] != obs[key]["observation_timestamp"]:
                misaligned.append(key)
            if row["availability_timestamp"] > contract["availability_cutoff"]:
                unavailable.append(key)
    missing = set(obs) - set(lab)
    orphan = set(lab) - set(obs)
    accepted = len(repeated) == 0 and len(invalid) == 0 and len(misaligned) == 0 and len(unavailable) == 0 and len(missing) == 0 and len(orphan) == 0
    return {"accepted": accepted, "repeated": repeated, "missing": missing, "orphan": orphan, "invalid": invalid, "misaligned": misaligned, "unavailable": unavailable}
result = audit(observations, labels, contract)
assert result["accepted"]
case_results = {}
for name in cases:
    case_results[name] = audit(observations, cases[name], contract)
    assert not case_results[name]["accepted"]
'''
add('label_integrity','Implement audit(observations,labels,contract), aligning by observation_id, not position. Detect repeated IDs before replacement. Return accepted, repeated (IDs in detection order), missing and orphan (ID sets), invalid, misaligned, unavailable (ID lists in label order). Check allowed label values, matching observation_timestamp and availability_timestamp <= cutoff. Expose result and case_results keyed by supplied failure names and write assertions for each; the normal B label is exactly on the inclusive cutoff.',s,body,['[result,case_results]'],packages=[])
f=fx['deployment_matched_splits'];s=inputs(group_records=f['group_records'],time_records=f['time_records'],training_groups=f['training_groups'],cutoff=f['cutoff'],evaluation_end=f['evaluation_end'],invalid_training_keys=f['invalid_training_keys'],invalid_validation_keys=f['invalid_validation_keys'])
body='''def partition(records, scenario, training_groups, cutoff, evaluation_end):
    if scenario == "group":
        train = [r for r in records if r["customer_group"] in training_groups]
        validation = [r for r in records if r["customer_group"] not in training_groups]
        train_groups = {r["customer_group"] for r in train}
        validation_groups = {r["customer_group"] for r in validation}
        assert not train_groups & validation_groups
    else:
        train = [r for r in records if r["observation_timestamp"] < cutoff]
        validation = [r for r in records if cutoff <= r["observation_timestamp"] < evaluation_end]
        assert max([r["observation_timestamp"] for r in train]) < cutoff
        assert min([r["observation_timestamp"] for r in validation]) >= cutoff
        assert max([r["observation_timestamp"] for r in validation]) < evaluation_end
    train_proportion = sum([r["target"] for r in train]) / len(train)
    validation_proportion = sum([r["target"] for r in validation]) / len(validation)
    return {"train": train, "validation": validation, "train_proportion": train_proportion, "validation_proportion": validation_proportion}
group_result = partition(group_records, "group", training_groups, cutoff, evaluation_end)
time_result = partition(time_records, "time", training_groups, cutoff, evaluation_end)
'''
add('deployment_matched_splits','Write partition(records,scenario,training_groups,cutoff,evaluation_end). For group, membership in training_groups assigns training and all others validation. For time, training < cutoff, cutoff <= validation < evaluation_end. Return train, validation records in source order and each target count / partition size as train_proportion, validation_proportion. Inputs here have nonempty partitions. Assert group separation or time inequalities. Expose group_result and time_result. The supplied failure-check harness must catch invalid assignments.',s,body,['[group_result,time_result]'],packages=[])
# Bounded API scaffolding for the preprocessing tasks. These in-memory teaching interfaces
# implement only the declared behaviors; they are explicitly not a full sklearn installation.
imputer='''import numpy as np
class MeanImputerFixture:
    def __init__(self, strategy="mean"):
        self.strategy = strategy
    def fit(self, X):
        self.statistics_ = np.nanmean(X, axis=0)
        return self
    def transform(self, X):
        return np.where(np.isnan(X), self.statistics_, X)
SimpleImputer = MeanImputerFixture
'''
scaler='''import numpy as np
class ScalerFixture:
    def __init__(self, with_mean=True, with_std=True):
        self.with_mean = with_mean
        self.with_std = with_std
    def fit(self, X):
        self.mean_ = np.mean(X, axis=0)
        std = np.std(X, axis=0, ddof=0)
        self.scale_ = np.where(std == 0, 1, std)
        return self
    def transform(self, X):
        return (X - self.mean_) / self.scale_
StandardScaler = ScalerFixture
'''
# Put infrastructure definitions in a single unchanged exec statement so they are scaffolding,
# not learner code, and retain them verbatim in both starter and solution.
f=fx['training_fitted_imputation'];s='exec('+repr(imputer)+')\n'+inputs(training_rows=f['X_train'],observed_rows=f['numeric_values'],validation_rows=f['X_validation'],boundary_rows=f['boundary_missing'],declared_strategy=f['declared_strategy'],incorrect_replacement=f['incorrect_replacement'])+'''X_train = np.array([[np.nan if v is None else v for v in row] for row in training_rows])
numeric_values = np.array(observed_rows)
X_validation = np.array([[np.nan if v is None else v for v in row] for row in validation_rows])
X_boundary = np.array([[np.nan if v is None else v for v in row] for row in boundary_rows])
'''
body='''def impute(X_train, X_validation, X_boundary, numeric_values):
    imputer = SimpleImputer(strategy=declared_strategy)
    imputer.fit(X_train)
    stored = imputer.statistics_.copy()
    transformed = imputer.transform(X_validation)
    boundary = imputer.transform(X_boundary)
    mean = np.mean(numeric_values, axis=0)
    std = np.std(numeric_values, axis=0, ddof=0)
    assert np.array_equal(stored, imputer.statistics_)
    assert np.allclose(transformed[0], X_validation[0])
    assert np.allclose(transformed[1], stored)
    assert np.allclose(boundary[0], stored)
    return {"transformed": transformed, "boundary": boundary, "statistics": imputer.statistics_, "mean": mean, "std": std}
result = impute(X_train, X_validation, X_boundary, numeric_values)
'''
add('training_fitted_imputation','Use the supplied in-memory mean-imputer teaching interface (not a full sklearn installation). Implement impute(X_train,X_validation,X_boundary,numeric_values): fit training only, copy statistics_, transform validation and one-row missing boundary without refitting. Compute observed-training column mean and population std. Assert observed validation is unchanged, missing outputs use stored statistics and fit state is unchanged. Return transformed, boundary, statistics, mean, std; expose result. The supplied harness also checks a deliberately wrong replacement assertion fails.',s,body,['result'])
f=fx['training_fitted_scaling'];s='exec('+repr(scaler)+')\n'+inputs(training_rows=f['X_train'],validation_rows=f['X_validation'],incorrect_transformed_fixture=f['incorrect_transformed_fixture'])+'X_train = np.array(training_rows)\nX_validation = np.array(validation_rows)\n'
body='''def scale(X_train, X_validation):
    scaler = StandardScaler(with_mean=True, with_std=True)
    scaler.fit(X_train)
    stored_mean = scaler.mean_.copy()
    stored_scale = scaler.scale_.copy()
    train = scaler.transform(X_train)
    validation = scaler.transform(X_validation)
    mean = np.mean(X_train, axis=0)
    std = np.std(X_train, axis=0, ddof=0)
    assert np.allclose(scaler.mean_, stored_mean)
    assert np.allclose(scaler.scale_, stored_scale)
    assert np.allclose(validation, (X_validation - stored_mean) / stored_scale)
    assert scaler.scale_[1] == 1
    return {"train": train, "validation": validation, "mean": mean, "std": std, "mean_": scaler.mean_, "scale_": scaler.scale_}
result = scale(X_train, X_validation)
'''
add('training_fitted_scaling','Use the supplied in-memory StandardScaler teaching interface (not a full sklearn installation). Implement scale(X_train,X_validation), fit on training only, transform both inputs using the same state, compute column means/population std, and assert validation arithmetic, constant feature scale 1, and unchanged mean_/scale_. Return train, validation, mean, std, mean_, scale_; expose result. The supplied harness catches wrong output or changed fitted parameters.',s,body,['result'])
encoder='''import numpy as np
class EncoderFixture:
    def __init__(self, handle_unknown="error", sparse_output=False):
        self.handle_unknown = handle_unknown
    def fit(self, X):
        values = [r[0] for r in X]
        known = sorted(set(v for v in values if not (isinstance(v,float) and np.isnan(v))))
        if any(isinstance(v,float) and np.isnan(v) for v in values): known.append(np.nan)
        self.categories_ = [np.array(known,dtype=object)]
        return self
    def transform(self, X):
        out = []
        for row in X:
            value = row[0]
            flags = [value == c or (isinstance(value,float) and isinstance(c,float) and np.isnan(value) and np.isnan(c)) for c in self.categories_[0]]
            if not any(flags) and self.handle_unknown == "error": raise ValueError("unknown category")
            out.append([int(v) for v in flags])
        return np.array(out)
OneHotEncoder = EncoderFixture
'''
f=fx['categorical_encoding'];s='exec('+repr(encoder)+')\n'+inputs(training_rows=f['X_train'],training_missing_rows=f['X_train_missing'],cases=f['cases'],feature_name=f['feature_name'])+'''X_train = training_rows
X_train_missing = [[np.nan if v is None else v for v in row] for row in training_missing_rows]
known = cases['north']
unseen = cases['east']
missing = [[np.nan]]
'''
body='''def encode(X_train, known, unseen, missing, policy):
    encoder = OneHotEncoder(handle_unknown=policy, sparse_output=False)
    encoder.fit(X_train)
    stored = encoder.categories_[0].copy()
    mapping = {"zone": encoder.categories_[0].tolist()}
    outputs = {}
    for name in ["known", "unseen", "missing"]:
        if name == "known":
            rows = known
        if name == "unseen":
            rows = unseen
        if name == "missing":
            rows = missing
        try:
            outputs[name] = encoder.transform(rows).tolist()
        except ValueError:
            outputs[name] = "ValueError"
    assert encoder.categories_[0].tolist() == stored.tolist()
    return {"mapping": mapping, "outputs": outputs, "width": len(stored)}
ignore_result = encode(X_train, known, unseen, missing, "ignore")
error_result = encode(X_train, known, unseen, missing, "error")
seen_missing_result = encode(X_train_missing, known, unseen, missing, "ignore")
assert ignore_result["outputs"]["known"] == [[1, 0]]
assert ignore_result["outputs"]["unseen"] == [[0, 0]]
assert ignore_result["outputs"]["missing"] == [[0, 0]]
assert error_result["outputs"]["unseen"] == "ValueError"
assert error_result["outputs"]["missing"] == "ValueError"
assert seen_missing_result["outputs"]["missing"] == [[0, 0, 1]]
'''
add('categorical_encoding','Use the supplied in-memory OneHotEncoder teaching interface (not a full sklearn installation). Implement encode(X_train,known,unseen,missing,policy) with explicit policy; fit once, build mapping={"zone": training categories list}, transform all three reusable cases without refitting, record ValueError as that string. Return mapping, outputs keyed known/unseen/missing, and width. Expose ignore_result, error_result and seen_missing_result. Author assertions matching known indicators, unseen/missing policies, output width and unchanged category mapping, including missing present during fit.',s,body,['[ignore_result,error_result,seen_missing_result]'])
f=fx['prediction_boundary_leakage'];runtime=next(z['content'] for z in assets['ws.prediction_boundary_leakage']['files'] if z['path']=='authorized_runtime.py');s='exec('+repr(runtime)+')\n'+inputs(training=f['training'],held_out=f['held_out'],permitted_features=f['permitted_features'],failure_fit_rows=f['failure_fit_rows'],failure_features=f['failure_features'])+'''select = lambda rows, columns: [{k:r[k] for k in columns} for r in rows]
'''
body='''def correct(training, held_out, permitted_features):
    preprocessor = TracePreprocessor()
    predictor = TracePredictor()
    train_inputs = select(training, permitted_features)
    held_inputs = select(held_out, permitted_features)
    preprocessor.fit(train_inputs)
    transformed = preprocessor.transform(held_inputs)
    predictor.predict(transformed)
    assert preprocessor.fit_rows == train_inputs
    assert preprocessor.transform_rows == [held_inputs]
    assert predictor.input_rows == [held_inputs]
    return {"fit_rows": preprocessor.fit_rows, "transform_rows": preprocessor.transform_rows, "prediction_rows": predictor.input_rows}
result = correct(training, held_out, permitted_features)
'''
add('prediction_boundary_leakage','Implement correct(training,held_out,permitted_features) using the supplied trace interfaces. Use select to exclude eventual arrival, fit preprocessing only on selected training inputs, transform held-out once, predict once. Return fit_rows, transform_rows and prediction_rows from the recorded traces. Expose result. Write the same trace/feature assertions that the harness applies to the deliberately leaked and corrected workflows; leaked traces must fail and corrected traces must pass.',s,body,['result'],packages=[])
f=fx['leakage_safe_features'];s='from datetime import datetime\n'+inputs(raw_records=f['records'],raw_augmented=f['augmented_records'],raw_prediction_time=f['prediction_time'])+'''records = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in raw_records]
augmented_records = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in raw_augmented]
prediction_time = datetime.fromisoformat(raw_prediction_time)
'''
body='''def feature(records, prediction_time):
    accepted = [row for row in records if row["available_at"] <= prediction_time]
    total = 0
    for record in accepted:
        total += record["value"]
    return total
result = feature(records, prediction_time)
augmented_result = feature(augmented_records, prediction_time)
assert result == augmented_result
assert feature([], prediction_time) == 0
'''
add('leakage_safe_features','Implement feature(records,prediction_time): filter available_at <= boundary with a list comprehension, then sum only accepted value entries using total=0 and accumulation. Expose result and augmented_result; author assertions for invariance after the later observation and for an empty list. Include a separate exact-boundary assertion. Timestamp parsing is supplied scaffolding.',s,body,['[result,augmented_result]'],packages=[])
f=fx['sensitive_ml_assets'];runtime=next(z['content'] for z in assets['ws.sensitive_ml_assets']['files'] if z['path']=='authorized_runtime.py');s='exec('+repr(runtime)+')\n'+inputs(sample=f['sample'],permitted_fields=f['permitted_fields'],authorized_identity=f['authorized_identity'],unauthorized_identity=f['unauthorized_identity'],runtime_secret_name=f['runtime_secret_name'])
body='''def audit(identity, sample, permitted_fields):
    authorized_sample = read_sample(identity, sample)
    record = {key: value for key, value in authorized_sample.items() if key in permitted_fields}
    return record
result = audit(authorized_identity, sample, permitted_fields)
assert result == {"run_id": sample["run_id"], "row_count": sample["row_count"]}
assert "token" not in result
assert "raw_customer_values" not in result
secret_used = use_secret(authorized_identity, runtime_secret_name)
'''
add('sensitive_ml_assets','Implement audit(identity,sample,permitted_fields), obtain the sample only via read_sample, construct a new permitted-field dictionary by membership checks, return it without printing restricted values. Expose result and secret_used; use the authorized secret interface without copying out the credential. Assert exact permitted values and absence of token/raw customer fields. The supplied harness checks unauthorized access raises PermissionError and captured output contains no restricted values.',s,body,['[result,secret_used]'],packages=[])
# Failure paths are supplied checking scaffolding; functions/skill remain learner-authored.
code['dataset_cleaning_policy']['solution']+='''\ntry:
    assert len(result["cleaned"]) == -1
except AssertionError:
    false_assertion_caught = True
assert false_assertion_caught
'''
code['deployment_matched_splits']['solution']+='''\ntry:
    assert not {r['customer_group'] for r in group_records if r['order_key'] in invalid_training_keys} & {r['customer_group'] for r in group_records if r['order_key'] in invalid_validation_keys}
except AssertionError:
    invalid_assignment_caught = True
assert invalid_assignment_caught
'''
code['training_fitted_imputation']['solution']+='''\ntry:
    assert np.allclose(result['boundary'], incorrect_replacement)
except AssertionError:
    bad_replacement_caught = True
assert bad_replacement_caught
'''
code['training_fitted_scaling']['solution']+='''\ntry:
    assert np.allclose(result['validation'], incorrect_transformed_fixture)
except AssertionError:
    bad_output_caught = True
assert bad_output_caught
'''
code['prediction_boundary_leakage']['solution']+='''\nleaked_fit = select(failure_fit_rows, failure_features)
try:
    assert leaked_fit == select(training, permitted_features)
except AssertionError:
    leaked_fit_caught = True
assert leaked_fit_caught
leaked_inputs = select(held_out, failure_features)
try:
    assert leaked_inputs == select(held_out, permitted_features)
except AssertionError:
    leaked_inputs_caught = True
assert leaked_inputs_caught
'''
code['leakage_safe_features']['solution']+='''\nboundary_records = [records[1]]
assert feature(boundary_records, prediction_time) == records[1]["value"]
'''
code['sensitive_ml_assets']['solution']+='''\ntry:
    audit(unauthorized_identity, sample, permitted_fields)
except PermissionError:
    unauthorized_caught = True
assert unauthorized_caught
'''
# Execute every result probe in the pinned engine: expected values never authored by hand.
jobs=[]
for name,c in code.items():
 tables,_=sandbox._tables(registry,c['mounts'],{},[])
 probes=[{'id':'t'+str(i),'kind':'expr','expr':e} for i,e in enumerate(c['exprs'])]
 jobs.append(sandbox._py_script(name,'main.py',c['solution'],sandbox._py_mounts(tables),probes))
res=sandbox.node_run(sandbox._py_job('python',['numpy','pandas'],jobs),sandbox.RUNTIMES['python']['runner'])
(B/'stage04_expected_runtime.json').write_text(json.dumps(res,indent=2))
for name,c in code.items():
 r=res['results'][name]
 if not r['ok']:raise RuntimeError(name+': '+r['error'])
 for p in r['probes'].values():
  if not p['ok']:raise RuntimeError(name+': '+p['error'])
# Inspect-and-judge excerpts: independent alternatives, no registry asset_ref.
inspect={
'file_object_ingestion':[
('good', 'import pandas as pd\n# client is already authorized; object selected by its listed name\nobject_name = "approved/orders-b.csv"\nclient.bucket(bucket_name).blob(object_name).download_to_filename(local_path)\ntable = pd.read_csv(local_path, dtype=declared_types)\nchecks = (list(table.columns) == expected_columns, len(table) == expected_row_count, table["order_key"].iloc[0] == "0012")\nwith open(identity_record_path, "w", encoding="utf-8") as f:\n    f.write(object_name + " -> " + local_path)\n# Complete delimited-text read; selected-column Parquet access would suit a separately declared columnar task.', 'pass', 'The named object, typed CSV checks and UTF-8 identity write follow the supplied contract.'),
('object', '# Authorized prefix listing: approved/orders-a.csv, approved/orders-b.csv\n# Contract requires orders-b.csv\nobject_name = "approved/orders-a.csv"\nclient.bucket(bucket_name).blob(object_name).download_to_filename(local_path)', 'fail', 'The selected name is not the required object.'),
('key', 'table = pd.read_csv(local_path, dtype={"order_key":"int64", "distance":"float64", "zone":"string", "eventual_arrival":"string"})\n# Required text key representation: "0012"', 'fail', 'Integer conversion does not preserve the declared zero-padded text key.'),
('identity', '# table and object checks have passed\n# Requirement: identity written through an explicit UTF-8 file handle\nidentity_text = object_name + " -> " + local_path\n# Function returns here; no open/write block', 'fail', 'An in-memory string is not the required UTF-8 file-handle write.'),
('format', '# Access pattern: retrieve the complete named orders-b.csv\n# Proposed rationale: CSV is columnar and intrinsically selects only requested columns like Parquet.', 'fail', 'The rationale confuses delimited CSV with the stated columnar selected-column Parquet access.')],
'preprocessing_pipeline':[
('reuse','pipeline = Pipeline([("prep", ColumnTransformer([("distance", numerical_steps, ["distance"]), ("zone", encoder, ["zone"])])), ("model", supplied_estimator)])\npipeline.fit(X_train, y_train)\nbefore = snapshot_fitted_parameters(pipeline)\nvalidation_predictions = pipeline.predict(X_validation)\ninference_predictions = pipeline.predict(X_inference)\nassert snapshot_fitted_parameters(pipeline) == before\nassert_representation_and_predictions(pipeline, declared_expected)\nassert_missing_input_accepted(pipeline)\nassert_malformed_missing_zone_raises(pipeline, ValueError)\n# Supplied checks all pass; numerical_steps: mean imputer then scaler; encoder: ignore unknown.', 'pass','One fitted workflow applies the column-specific transformations and passes the declared output/state/failure checks.'),
('refit','pipeline.fit(X_train, y_train)\npipeline.fit(X_validation, validation_labels)\nvalidation_predictions = pipeline.predict(X_validation)', 'fail','The validation fit changes the fitted state instead of reusing training transformations.'),
('columns','ColumnTransformer([("zone", numerical_steps, ["zone"]), ("distance", encoder, ["distance"])])\n# Contract: numerical steps on distance, categorical encoding on zone.', 'fail','The column assignments reverse the declared numerical and categorical operations.'),
('missing','pipeline.fit(X_train, y_train)\n# Supplied contract requires missing distance input to follow mean imputation\nmissing_distance_case: ValueError("missing distance")\n# All other declared checks pass.', 'fail','The observed missing-value failure contradicts the supplied imputation outcome.'),
('malformed','pipeline.fit(X_train, y_train)\n# Contract: missing required zone is malformed and must raise ValueError\nmalformed_missing_zone_case: predictions [0]\n# All normal/missing-distance checks pass.', 'fail','Returning predictions for the declared malformed fixture fails its specified exception contract.')]
}
out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for ti,t in enumerate(plans['tiles']):
 st=next(z for z in screens['tiles'] if z['tile_id']==t['tile_id']);first=set();entries=[]
 for step in t['steps']:
  if step['type'] not in ['check','hands_on']:continue
  cid=step['concept_ids'][0];name=cid.split('.',1)[1];bundle=g[cid]
  measures=[]
  for anchor in step['anchors']:
   if '#assessment:' in anchor:
    ac,cap=anchor.split('#assessment:');a=next(a for a in g[ac]['assessment_anchors'] if a['capability']==cap)
    measures.append({'concept_id':ac,**copy.deepcopy(a)})
  facts=' '.join(f['statement'] for f in bundle['coverage']['required_facts'] if f['id'] in {f for a in measures for f in a['fact_ids']})
  feedback={'correct':{'message':'The response satisfies the declared information and input contract.'},'incorrect':{'message':facts},'hints':['Separate the declared requirement from incidental fixture details.','Compare each operation with the supplied boundary or policy before accepting it.']}
  if cid not in first:
   rem=next((r for r in st['remediation_steps'] if cid in r['concept_ids']),None)
   if rem:feedback['remediation_step_id']=rem['step_id']
   first.add(cid)
  ix={'type':step['planned_interaction_type'],'interaction_id':'ix.'+step['step_id'],'difficulty':'intro' if step['type']=='check' and len(entries)==0 else ('stretch' if step['type']=='hands_on' else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':step['anchors'],'feedback':feedback}
  if step['type']=='check':
   q,right,w1,w2,fr,fw1,fw2=checks[name]
   ix['public']={'prompt':q,'selection':'single','shuffle':True,'options':[{'option_id':'a','text':right},{'option_id':'b','text':w1},{'option_id':'c','text':w2}]}
   ix['grading']={'correct_option_ids':['a'],'option_feedback':{k:{'message':m} for k,m in zip(['a','b','c'],[fr,fw1,fw2])}}
  elif name in inspect:
   ex=inspect[name]
   ix['public']={'prompt':('Inspect each independent excerpt against the supplied practice contract. All unshown infrastructure is already authorized and unshown operations satisfy the contract; classify ONLY the evidence shown. ' + ( 'Retrieve approved/orders-b.csv, preserve declared types including text order_key, verify columns/row count/key, write identity via UTF-8 handle, and distinguish complete CSV access from selected-column Parquet.' if name=='file_object_ingestion' else 'Distance uses mean imputation then scaling, zone uses encoding with ignore; fit training once, reuse predict, preserve state, accept missing distance and reject missing required zone. Supplied assertion helper names mean the declared checks shown in their comments.')),'buckets':[{'bucket_id':'pass','label':'Satisfies the shown contract'},{'bucket_id':'fail','label':'Violates the shown contract'}],'items':[{'item_id':i,'text':'```python\n'+text+'\n```'} for i,text,role,fb in ex]}
   ix['grading']={'assignments':{i:role for i,text,role,fb in ex},'item_feedback':{i:{'message':fb} for i,text,role,fb in ex}}
  elif name=='prediction_task_definition':
   rows=assets['ds.task_record']['rows'];parts=[label+': '+value for label,value in rows]
   counts=assets['ds.outcome_counts']['rows'];parts += [f'{r[0]} outcome proportion ({r[3]}-minute horizon): '+str(r[1]/r[2]) for r in counts]
   parts+=['Zone proportion describes only the specified zone, not every zone.']
   # A single graded formula builds the full record and both labeled proportions.
   formula='='+ '&" | "&'.join('"'+p.replace('"','""')+'"' for p in parts[:7])+ '&" | "&"'+counts[0][0]+f' outcome proportion ({counts[0][3]}-minute horizon): "&B2/C2&" | "&"'+counts[1][0]+f' outcome proportion ({counts[1][3]}-minute horizon): "&B3/C3&" | "&"'+parts[-1]+'"'
   ix['public']={'prompt':'In E2 enter one formula producing the complete task record below, with fields separated by " | ". Derive both proportions by division of the supplied count cells (B=target_count, C=population_count; row 2 all orders, row 3 specified zone); concatenate their calculated values, not hard-coded proportions. Preserve the exact labels and text: '+ ' | '.join(parts[:7])+f' | {counts[0][0]} outcome proportion ({counts[0][3]}-minute horizon): [B2/C2] | {counts[1][0]} outcome proportion ({counts[1][3]}-minute horizon): [B3/C3] | '+parts[-1], 'asset_ref':{'asset_id':'ds.outcome_counts'},'sheet_name':'Counts','target_cell':'E2','allowed_functions':[]}
   ix['grading']={'reference_formula':formula,'expected_value':' | '.join(parts),'forbid_hardcoded_values':True}
  else:
   c=code[name];ix['standalone']=True
   ix['public']={'prompt':c['prompt'],'runtime':{'kind':'python','version':sandbox.RUNTIMES['python']['version'],'packages':c['packages']},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':c['starter']+'\n# TODO: implement the contract, then run your assertions.\n'}],'asset_mounts':c['mounts']},'constraints':{k:bundle['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'main.py','content':c['solution']}],'tests':[{'test_id':'t'+str(i),'kind':'value_equals','spec':{'expr':e,'expected':res['results'][name]['probes']['t'+str(i)]['value']},'message_on_fail':'The computed result does not match the declared input contract.'} for i,e in enumerate(c['exprs'])]}
  entries.append({'step_id':step['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':t['tile_id'],'interactions':entries})
(B/'interactions.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
