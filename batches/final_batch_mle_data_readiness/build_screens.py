import json, re, copy
from pathlib import Path
B=Path(__file__).parent
P=json.loads((B/'tile_plans.json').read_text())
G=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
R=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in G['bundles']}
assets={a['asset_id']:a for a in R['assets']}
fixtures={a['asset_id'].replace('ws.','mle.'):json.loads(next(f['content'] for f in a['files'] if f['path']=='fixtures.json')) for a in R['assets'] if a['asset_kind']=='code_workspace'}
intro={
'prediction_task_definition':'Before preparing delivery examples, pin down what one prediction means. Keep the prediction unit, eligible population, target, decision time and horizon separate.',
'numpy_shape_dtype':'A flat collection of values is not interchangeable with a batch of orders. Check the array boundary before arithmetic.',
'numpy_dtype_selection':'A smaller numerical representation must satisfy both the storage budget and the declared value-preservation requirement.',
'numpy_vectorization':'Subtract a feature reference across the orders with array arithmetic. Axis compatibility alone does not establish the intended result shape.',
'file_object_ingestion':'Retrieve the named existing object in the authorized runtime, then verify how the reader interpreted it. Listing and loading answer different questions.',
'chunked_ingestion':'Process one working chunk at a time. Reading chunks and retaining them all defeats the bounded-array workflow.',
'dataset_inspection':'Make readiness inspectable: return named evidence about columns, axes, feature summaries and element storage, rather than a vague verdict.',
'dataset_schema_validation':'Loading succeeds even for tables that violate the declared contract. Validate structure and types before constrained values.',
'dataset_cleaning_policy':'Resolve each observation under the supplied policy. Record the action and affected identity instead of silently changing the orders.',
'dataset_selection_bias':'Compare the included orders with the supplied target-population counts before interpreting the sample as representative.',
'label_integrity':'Labels can arrive in a different row order. Establish identity correspondence and timestamp suitability independently.',
'deployment_matched_splits':'Choose the supplied evaluation boundary first. Group separation and chronological ordering test different deployment interpretations.',
 'training_fitted_imputation':'Learn the replacement from training, then apply that stored state to validation. A new cohort is not a request to relearn it.',
 'training_fitted_scaling':'Training defines the scaling reference. Put validation through that same fitted rule, even when its values fall outside the training range.',
 'categorical_encoding':'The training fit fixes category-column identity. State what unseen and missing values mean under that learned mapping.',
 'preprocessing_pipeline':'Keep column-specific transformations attached to the estimator. Exercise the fitted raw-input prediction path, not an independently prepared array.',
 'prediction_boundary_leakage':'Audit two information paths: fields available for each prediction, and rows used to fit preprocessing. Holding out labels alone does not test both.',
 'leakage_safe_features':'Filter by recorded availability before calculating a feature. Later records must not change an earlier prediction’s feature.',
 'sensitive_ml_assets':'Apply the existing authorization and permitted-field policy before generating a diagnostic record. Readability is not redistribution permission.'}
contrast={
'prediction_task_definition':'Contrast the target with the inputs: later arrival judges the target but is unavailable at acceptance.',
'numpy_shape_dtype':'Contrast the valid batch with the flat fixture: equal element counts do not establish equal rank.',
'numpy_dtype_selection':'Contrast fewer element bytes with value preservation: a successful cast can still fail the supplied tolerance.',
'numpy_vectorization':'Contrast a compatible operation with the intended shape: broadcasting may expand the result.',
'file_object_ingestion':'Contrast a successful download with a verified table: the intended object still needs the declared representations.',
'chunked_ingestion':'Contrast bounded working chunks with retaining every chunk: only the former follows this streaming approach.',
'dataset_inspection':'Contrast a named feature-wise summary with one total element count: the latter hides axis meanings and divisor choices.',
'dataset_schema_validation':'Contrast loading with validation: a readable table can still violate its declared columns, types or value bounds.',
'dataset_cleaning_policy':'Contrast repair with rejection: report the selected policy action and affected ID, not just an issue count.',
'dataset_selection_bias':'Contrast sample share with inclusion probability: their denominators describe different populations.',
'label_integrity':'Contrast equal row counts with keyed correspondence: reordered labels still need identity and time checks.',
'deployment_matched_splits':'Contrast group disjointness with temporal ordering: passing one check does not establish the other.',
 'training_fitted_imputation':'Contrast transform with another fit: transform reuses the stored training replacement.',
 'training_fitted_scaling':'Contrast reuse with refitting validation: only reuse applies the training reference.',
 'categorical_encoding':'Contrast an all-zero unknown indicator with a learned category: ignoring an unseen value does not extend the mapping.',
 'preprocessing_pipeline':'Contrast the fitted pipeline’s predict path with new validation preprocessing: the latter changes the representation.',
 'prediction_boundary_leakage':'Contrast deleting a future field with excluding held-out fit rows: each repairs a different information path.',
 'leakage_safe_features':'Contrast filtering before summing with summing every record: removing a timestamp afterward does not remove its contribution.',
 'sensitive_ml_assets':'Contrast a new permitted-field record with printing the source: filtering the return value does not undo output disclosure.'}
# Code examples use the registered workspace's fixtures, not hand-entered inputs or outputs.
code={
'numpy_shape_dtype':'''import numpy as np
from fixtures import FIXTURES as F

def accept(fixture, contract):
    a = np.array(fixture)
    print(a.ndim, a.shape, a.dtype)
    if a.ndim != 2:
        raise ValueError("Expected batch and feature axes")
    if a.shape[1] != contract["feature_count"]:
        raise ValueError("Unexpected feature width")
    if not contract["min_batch"] <= a.shape[0] <= contract["max_batch"]:
        raise ValueError("Batch length outside contract")
    return a

assert accept(F["valid"], F["contract"]).ndim == 2
assert accept(F["tuple_boundary"], F["contract"]).shape[1] == F["contract"]["feature_count"]
for name in ("empty", "flat", "wrong_width", "too_many"):
    try:
        accept(F[name], F["contract"])
    except ValueError:
        print(name, "rejected")
    else:
        raise AssertionError("Failure fixture was accepted")''',
'numpy_vectorization':'''import numpy as np
from fixtures import FIXTURES as F

a = np.array(F["matrix"])
b = np.array(F["feature_references"])
array_result = a - b
reference = np.array([[value - offset for value, offset in zip(row, b)]
                      for row in F["matrix"]])
print(a.shape, b.shape, array_result.shape, array_result)
assert array_result.shape == tuple(F["expected_shape"])
np.testing.assert_allclose(array_result, reference, rtol=F["rtol"], atol=F["atol"])
expanded = np.array(F["broadcast_column"]) - np.array(F["broadcast_row"])
print(expanded.shape, expanded)''',
'file_object_ingestion':'''from google.cloud import storage
import pandas as pd
from fixtures import FIXTURES as F

# Existing authorized identity; in this lab storage is the supplied fixture client.
def ingest(client, spec):
    names = [blob.name for blob in client.list_blobs(spec["bucket"], prefix=spec["prefix"])]
    print(names)
    if spec["intended_object"] not in names:
        raise ValueError("Named object absent")
    bucket = client.bucket(spec["bucket"])
    bucket.blob(spec["intended_object"]).download_to_filename(spec["local_path"])
    table = pd.read_csv(spec["local_path"], dtype=spec["declared_types"])
    for column, dtype in spec["declared_types"].items():
        table[column] = table[column].astype(dtype)
    assert list(table.columns) == spec["expected_columns"]
    assert len(table) == spec["expected_row_count"]
    assert table["order_key"].iloc[0] == spec["expected_order_key"]
    print(table.columns.tolist(), len(table), table.dtypes, table["order_key"].tolist())
    with open(spec["identity_record_path"], "w", encoding="utf-8") as f:
        f.write(spec["intended_object"] + " -> " + spec["local_path"])
    return table

client = storage.Client()
table = ingest(client, F)''',
'chunked_ingestion':'''import pandas as pd
from fixtures import FIXTURES as F

row_limit = F["array_budget"] // (F["feature_count"] * F["element_width"])
maximum = 0
with open(F["path"], "r", encoding="utf-8") as stream:
    for table in pd.read_csv(stream, chunksize=row_limit, dtype=F["declared_types"]):
        a = table.to_numpy()
        estimate = a.shape[0] * a.shape[1] * a.itemsize
        assert estimate == a.nbytes
        assert a.nbytes <= F["array_budget"]
        maximum = max(maximum, a.nbytes)
        print(a.shape, a.itemsize, estimate, a.nbytes)
        # Process this chunk here; do not collect prior chunks.
print(maximum)''',
'dataset_inspection':'''import numpy as np
import pandas as pd
from fixtures import FIXTURES as F

def inspect(table, feature_columns, ddof):
    a = table[feature_columns].to_numpy()
    return {"columns": table.columns.tolist(), "dtypes": table.dtypes,
            "descriptive_summary": table.describe(),
            "shape": a.shape, "observation_count": a.shape[0],
            "feature_count": a.shape[1], "axis_meanings": ("observations", "features"),
            "dtype": a.dtype, "element_bytes": a.nbytes,
            "mean": np.mean(a, axis=0), "std": np.std(a, axis=0, ddof=ddof)}

table = pd.DataFrame(F["fixture"]["rows"], columns=F["fixture"]["columns"])
print(inspect(table, F["feature_columns"], F["ddof"]))''',
'dataset_schema_validation':'''import pandas as pd
from fixtures import FIXTURES as F

def validate(table, contract):
    if set(table.columns) != set(contract["columns"]):
        raise ValueError("Column contract")
    if any(str(table.dtypes[c]) != t for c, t in contract["declared_types"].items()):
        raise ValueError("Type contract")
    if not table["distance"].between(contract["distance_min"], contract["distance_max"]).all():
        raise ValueError("Distance boundary")
    if not table["zone"].isin(contract["zone_categories"]).all():
        raise ValueError("Zone representation")
    return True

for name in ("valid", "negative", "too_large", "missing_column", "invalid_representation", "unexpected_column"):
    fixture = F[name]
    table = pd.DataFrame(fixture["rows"], columns=fixture["columns"])
    # Construct fixture types without repairing values or adding missing columns.
    table = table.astype({c: t for c, t in F["contract"]["declared_types"].items() if c in table})
    print(name, table.columns.tolist(), table.dtypes)
    try:
        accepted = validate(table, F["contract"])
    except ValueError as error:
        assert name != "valid"
        print(str(error))
    else:
        assert name == "valid" and accepted''',
'dataset_cleaning_policy':'''from fixtures import FIXTURES as F

def clean(records, policy):
    accepted_keys, accepted, report, trace = set(), [], [], []
    for original in records:
        row = dict(original)
        before = set(accepted_keys)
        if row["order_key"] in accepted_keys:
            action = policy["repeat_accepted_key"]
        elif not policy["distance_min"] <= row["distance"] <= policy["distance_max"]:
            action = policy["invalid_distance"]
        elif row["zone"] in policy["zone_repairs"]:
            action = "repair"
        else:
            action = "retain"
        if action == "repair":
            row["zone"] = policy["zone_repairs"][row["zone"]]
        if action != "reject":
            accepted.append(row)
            accepted_keys.add(row["order_key"])
        if action != "retain":
            report.append({"observation_id": row["observation_id"], "action": action})
        trace.append((before, action, set(accepted_keys)))
    return accepted, report, trace

result, report, trace = clean(F["records"], F["policy"])
assert len({r["order_key"] for r in result}) == len(result)
assert all(F["policy"]["distance_min"] <= r["distance"] <= F["policy"]["distance_max"] for r in result)
assert clean(F["valid"], F["policy"])[0] == F["valid"]
print(result, report, trace)''',
'label_integrity':'''from fixtures import FIXTURES as F

def align(observations, labels, accepts):
    observation_ids = [r["observation_id"] for r in observations]
    label_ids = [r["observation_id"] for r in labels]
    if len(set(observation_ids)) != len(observation_ids) or len(set(label_ids)) != len(label_ids):
        raise ValueError("Repeated ID")
    missing = set(observation_ids) - set(label_ids)
    orphaned = set(label_ids) - set(observation_ids)
    if missing or orphaned:
        raise ValueError((missing, orphaned))
    by_id = {r["observation_id"]: r for r in labels}
    matched = []
    for observation in observations:
        label = by_id[observation["observation_id"]]
        if not accepts(observation, label):
            raise ValueError(observation["observation_id"])
        matched.append((observation, label))
    return matched

def accepts(observation, label):
    contract = F["contract"]
    timestamp_ok = (not contract["require_matching_observation_timestamp"]
                    or label["observation_timestamp"] == observation["observation_timestamp"])
    available = label["availability_timestamp"]
    cutoff = contract["availability_cutoff"]
    time_ok = available <= cutoff if contract["availability_boundary_inclusive"] else available < cutoff
    return label["label"] in contract["label_values"] and timestamp_ok and time_ok

matched = align(F["observations"], F["labels"], accepts)
assert len(matched) == len(F["observations"])
print(matched)
for name, labels in F["cases"].items():
    try:
        align(F["observations"], labels, accepts)
    except ValueError as error:
        print(name, str(error))
    else:
        raise AssertionError("Failure fixture accepted")''',
'deployment_matched_splits':'''from fixtures import FIXTURES as F

def group_partition(records, train_groups, validation_groups):
    train = [r for r in records if r["customer_group"] in set(train_groups)]
    validation = [r for r in records if r["customer_group"] in set(validation_groups)]
    train_set = {r["customer_group"] for r in train}
    validation_set = {r["customer_group"] for r in validation}
    assert not train_set & validation_set
    print(train, validation, train_set, validation_set, train_set & validation_set)
    return train, validation

def describe(partition):
    count = sum(r["target"] for r in partition)
    total = len(partition)
    return {"target_count": count, "total": total, "proportion": count / total if total else None}

group_partition(F["group_records"], F["training_groups"], F["validation_groups"])
train = [r for r in F["time_records"] if r["observation_timestamp"] < F["cutoff"]]
validation = [r for r in F["time_records"] if F["cutoff"] <= r["observation_timestamp"] < F["evaluation_end"]]
assert all(r["observation_timestamp"] < F["cutoff"] for r in train)
assert all(F["cutoff"] <= r["observation_timestamp"] < F["evaluation_end"] for r in validation)
print(train, validation, describe(train), describe(validation))''',
 'training_fitted_imputation':'''import numpy as np
from sklearn.impute import SimpleImputer
from fixtures import FIXTURES as F

train = np.array(F["X_train"], dtype=float)
validation = np.array(F["X_validation"], dtype=float)
observed = np.array(F["numeric_values"], dtype=float)
imputer = SimpleImputer(strategy=F["declared_strategy"]).fit(train)
before = imputer.statistics_.copy()
transformed = imputer.transform(validation)
np.testing.assert_array_equal(before, imputer.statistics_)
print(observed.mean(axis=0), observed.std(axis=0, ddof=0))
print(train, validation, before, transformed, imputer.statistics_)
assert np.isfinite(imputer.transform(np.array(F["boundary_missing"], dtype=float))).all()''',
 'training_fitted_scaling':'''import numpy as np
from sklearn.preprocessing import StandardScaler
from fixtures import FIXTURES as F

train = np.array(F["X_train"], dtype=float)
validation = np.array(F["X_validation"], dtype=float)
scaler = StandardScaler(with_mean=F["with_mean"], with_std=F["with_std"]).fit(train)
mean_before, scale_before = scaler.mean_.copy(), scaler.scale_.copy()
transformed = scaler.transform(validation)
np.testing.assert_array_equal(mean_before, scaler.mean_)
np.testing.assert_array_equal(scale_before, scaler.scale_)
print(train, validation, np.mean(train, axis=0), np.std(train, axis=0, ddof=F["ddof"]))
print(mean_before, scale_before, scaler.transform(train), transformed)''',
 'categorical_encoding':'''import numpy as np
from sklearn.preprocessing import OneHotEncoder
from fixtures import FIXTURES as F

def array(rows):
    return np.array([[np.nan if v is None else v for v in row] for row in rows], dtype=object)

for training in (F["X_train"], F["X_train_missing"]):
    for policy in F["unknown_policies"]:
        encoder = OneHotEncoder(handle_unknown=policy).fit(array(training))
        before = [values.copy() for values in encoder.categories_]
        mapping = {F["feature_name"]: encoder.categories_[0].tolist()}
        print(mapping)
        for name, rows in F["cases"].items():
            try:
                print(name, encoder.transform(array(rows)).toarray())
            except ValueError:
                print(name, "rejected by unknown-category policy")
            for old, new in zip(before, encoder.categories_):
                assert old.tolist() == new.tolist()''',
 'preprocessing_pipeline':'''import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from fixtures import FIXTURES as F

def compose(estimator):
    numerical = Pipeline([("impute", SimpleImputer(strategy="mean")),
                          ("scale", StandardScaler(with_mean=True, with_std=True))])
    columns = ColumnTransformer([("numeric", numerical, ["distance"]),
                                 ("category", OneHotEncoder(handle_unknown="ignore"), ["zone"])])
    return Pipeline([("columns", columns), ("estimator", estimator)])

def apply(estimator):
    workflow = compose(estimator)  # supplied deterministic fixture estimator
    train = pd.DataFrame(F["X_train"])
    validation = pd.DataFrame(F["X_validation"])
    workflow.fit(train, F["y_train"])
    print(workflow.named_steps["columns"].transform(validation))
    print(workflow.predict(validation))
    return workflow
from authorized_runtime import FixtureEstimator
workflow = apply(FixtureEstimator())
columns = workflow.named_steps["columns"]
imputer = columns.named_transformers_["numeric"].named_steps["impute"]
scaler = columns.named_transformers_["numeric"].named_steps["scale"]
encoder = columns.named_transformers_["category"]
before = (imputer.statistics_.copy(), scaler.mean_.copy(), scaler.scale_.copy(),
          [v.copy() for v in encoder.categories_])
workflow.predict(pd.DataFrame(F["X_validation"]))
after = (imputer.statistics_, scaler.mean_, scaler.scale_, encoder.categories_)
import numpy as np
for old, new in zip(before[:3], after[:3]):
    np.testing.assert_array_equal(old, new)
for old, new in zip(before[3], after[3]):
    np.testing.assert_array_equal(old, new)
try:
    workflow.predict(pd.DataFrame(F["malformed"]))
except (ValueError, KeyError):
    pass
else:
    raise AssertionError("Missing feature accepted")''',
 'prediction_boundary_leakage':'''from fixtures import FIXTURES as F

def project(rows, features):
    if F["future_field"] in features:
        raise ValueError("Future information is unavailable at acceptance")
    return [{field: row[field] for field in features} for row in rows]

def audit(fit_rows, training, held_out, features):
    fit_ids = {r["order_key"] for r in fit_rows}
    training_ids = {r["order_key"] for r in training}
    held_out_ids = {r["order_key"] for r in held_out}
    assert fit_ids <= training_ids
    assert not fit_ids & held_out_ids
    print(fit_ids, held_out_ids, features)
    return project(held_out, features)

print(audit(F["training"], F["training"], F["held_out"], F["permitted_features"]))
# Split first. preprocessing.fit(project(training, permitted_features))
# Then preprocessing.transform(project(held_out, permitted_features)), never held-out fit.
# failure_fit_rows violates the fit boundary; failure_features violates prediction availability.''',
 'leakage_safe_features':'''from datetime import datetime
from fixtures import FIXTURES as F

def feature(records, prediction_time):
    boundary = datetime.fromisoformat(prediction_time)
    accepted = [row for row in records
                if datetime.fromisoformat(row["available_at"]) <= boundary]
    total = 0
    for record in accepted:
        total += record["value"]
    return accepted, total

original = feature(F["records"], F["prediction_time"])
augmented = feature(F["augmented_records"], F["prediction_time"])
assert original == augmented
print(F["prediction_time"], F["records"], original)
print(F["augmented_records"], augmented)
# Any changing lookup must also use its value at the recorded boundary.'''
}

def lineage(cid,tbs,facts,anchors=None):
    v={'concept_ids':[cid],'teaching_block_ids':tbs,'fact_ids':facts}
    if anchors: v['anchors']=anchors
    return v

def prose(text,cid,tbs,facts,role):
    return {'type':'prose','text':text,'role':role,'lineage':lineage(cid,tbs,facts)}

def split_text(text):
    # Sentence-level splitting keeps decimal values, qualified names, code and each claim intact.
    sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z‘])',text.replace('\n',' '))
    out=[]; current=''
    for sentence in sentences:
        if current and len((current+' '+sentence).split())>90:
            out.append(current);current=''
        current=(current+' '+sentence).strip()
    if current:out.append(current)
    assert all(len(v.split())<=90 for v in out),out
    return out

def table(asset_id,cid,anchor=False):
    return {'type':'data_table','asset_ref':{'asset_id':asset_id},'lineage':lineage(cid,[],[],[cid+'#visual'] if anchor else None)}

def walkthrough(cid,source):
    return {'type':'code_walkthrough','language':'python','code':source,'lineage':lineage(cid,[],[],[cid+'#visual'])}

def visual(cid,kind):
    key=cid.split('.',1)[1]; F=fixtures.get(cid)
    if key=='prediction_task_definition':
        a=assets['ds.outcome_counts']; columns=[c['name'] for c in a['columns']]
        # Source columns are A:D; E is the engine-calculated proportion.
        rows=list(__import__('csv').DictReader((B/a['data_file']['uri']).open()))
        return [table('ds.task_record',cid),{'type':'spreadsheet_grid','asset_ref':{'asset_id':a['asset_id']},'range':f'A1:E{len(rows)+1}', 'show_formula_bar':True,
                  'cells':[{'ref':f'E{i}','formula':f'=B{i}/C{i}','note':'Target count divided by this population count.'} for i in range(2,len(rows)+2)],
                  'lineage':lineage(cid,[],[],[cid+'#visual'])}]
    if key=='dataset_selection_bias':
        return [table('ds.selection_counts',cid,True),walkthrough(cid,'''import numpy as np
from fixtures import FIXTURES as F

sample_total = sum(F["sample_counts"].values())
target_total = sum(F["target_counts"].values())
for zone, target in F["target_counts"].items():
    included = F["sample_counts"].get(zone, 0)
    print(zone, included, target,
          included / sample_total if sample_total else None,
          target / target_total if target_total else None,
          included / target if target else None)
values = np.array(F["numeric_values"])
print(values, np.mean(values), np.std(values, ddof=F["ddof"]))''')]
    if key=='numpy_dtype_selection':
        panel='''import numpy as np
from fixtures import FIXTURES as F
reference = np.array(F["a"], dtype=np.float64)
probe = np.array(F["boundary_values"], dtype=np.float64)
candidate = reference.astype(DTYPE)
differences = candidate.astype(reference.dtype) - reference
boundary_differences = probe.astype(DTYPE).astype(probe.dtype) - probe
print(reference, candidate, differences, boundary_differences)
print(candidate.dtype, candidate.size, candidate.itemsize,
      candidate.size * candidate.itemsize, candidate.nbytes)
accepted = (candidate.nbytes <= F["element_storage_budget"]
            and np.all(np.abs(differences) <= F["tolerance"])
            and np.all(np.abs(boundary_differences) <= F["tolerance"]))
print(accepted)'''
        types=F['candidate_dtypes']
        return [{'type':'side_by_side','left':walkthrough(cid,panel.replace('DTYPE',repr(types[0]))),'right':walkthrough(cid,panel.replace('DTYPE',repr(types[1]))),
                 'left_label':types[0],'right_label':types[1],'takeaway':'Check preservation and the element-storage budget separately.','lineage':lineage(cid,[],[],[cid+'#visual'])}]
    if key=='sensitive_ml_assets':
        return [{'type':'before_after','before':table('ds.audit_sample',cid),
          'after':walkthrough(cid,'''from authorized_runtime import read_sample, use_secret
from fixtures import FIXTURES as F

def permitted_record(identity, sample, permitted_fields):
    authorized = read_sample(identity, sample)
    return {key: value for key, value in authorized.items() if key in permitted_fields}

record = permitted_record(F["authorized_identity"], F["sample"], F["permitted_fields"])
assert set(record) <= set(F["permitted_fields"])
print(record)  # Never print the source sample or its restricted values.
assert use_secret(F["authorized_identity"], F["runtime_secret_name"])'''),
          'change_summary':'Exclude token and raw customer values; keep credentials in the authorized runtime secret mechanism.','lineage':lineage(cid,[],[],[cid+'#visual'])}]
    ds={'numpy_shape_dtype':'ds.order_features','numpy_vectorization':'ds.order_features','file_object_ingestion':'ds.orders','chunked_ingestion':'ds.chunked_orders',
        'dataset_inspection':'ds.order_features','dataset_schema_validation':'ds.distance_zone','dataset_cleaning_policy':'ds.cleaning_orders',
        'label_integrity':'ds.labels','deployment_matched_splits':'ds.group_orders','training_fitted_imputation':'ds.imputation_train',
        'training_fitted_scaling':'ds.scaling_train','categorical_encoding':'ds.zone_train','preprocessing_pipeline':'ds.distance_zone',
        'prediction_boundary_leakage':'ds.orders','leakage_safe_features':'ds.feature_records'}
    return [table(ds[key],cid),walkthrough(cid,code[key])]

out={k:P[k] for k in ('schema_version','path_id','batch_id')};out.update(kind='screens_part',tiles=[])
for tile in P['tiles']:
    concepts=tile['concept_ids']
    title=' · '.join(bundles[c]['context']['concept_name'] for c in concepts)
    result={'tile_id':tile['tile_id'],'title':title,'summary':'Independent fictional delivery fixtures; follow each supplied contract and policy.','steps':[],'remediation_steps':[]}
    for step in tile['steps']:
        cid=step['concept_ids'][0]; key=cid.split('.',1)[1]; bundle=bundles[cid]
        s={k:copy.deepcopy(step[k]) for k in ('step_id','type','concept_ids')}
        s['lineage']={k:copy.deepcopy(step[k]) for k in ('teaching_block_ids','fact_ids')}
        s['lineage']['concept_ids']=copy.deepcopy(step['concept_ids'])
        if step['anchors']:s['lineage']['anchors']=copy.deepcopy(step['anchors'])
        s['eyebrow']={'explainer':'Learn','video':'Optional media','check':'Check your understanding','hands_on':'Apply the contract','recap':'Takeaways'}[step['type']]
        if step['type'] in ('check','hands_on'):
            s['title']=('Check: ' if step['type']=='check' else 'Practice: ')+bundle['context']['concept_name']
        elif step['type']=='video':
            s['title']=bundle['context']['concept_name']
            s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(step['segment_ids'])}]
        elif step['type']=='recap':
            s['title']='Carry these distinctions forward'
            s['blocks']=[]
            for c in step['concept_ids']:
                b=bundles[c]; tb=next(x for x in b['teaching_blocks'] if x['purpose']=='misconception')
                # The short planned distinction is the takeaway; it retains the qualifying source language.
                s['blocks'].append(prose(tb['content'],c,[c+'#'+tb['id']],[c+'#'+f for f in tb['fact_ids']],'takeaway'))
            # Use a compact recap for multi-concept tiles so the complete step stays within 90 words.
            if sum(len(x['text'].split()) for x in s['blocks'])>65:
                s['blocks']=[prose(contrast[c.split('.',1)[1]],c,[],[], 'takeaway') for c in step['concept_ids']]
            next_tile=next((t for t in P['tiles'] if t['tile_id']==tile['next_tile_id']),None)
            if next_tile: next_name=bundles[next_tile['concept_ids'][0]]['context']['concept_name']
            else:
                next_bundle=next((b for b in G['bundles'] if b['context']['toc_location']['tile_id']==tile['next_tile_id']),None)
                if next_bundle:
                    next_name=next_bundle['context']['concept_name']
                else:
                    # The glossary's ordered names match the numbered tile ranges.
                    ordered=list(G['names'])
                    assert ordered[:len(bundles)] == list(bundles)
                    start=int(tile['next_tile_id'].split('.')[-1].split('_')[0])
                    next_name=G['names'][ordered[start]]
            s['blocks'].append({'type':'up_next','title':next_name})
        else:
            s['blocks']=[]
            tbs={x['id']:x for x in bundle['teaching_blocks']}
            selected=[tbs[q.split('#')[1]] for q in step['teaching_block_ids']]
            s['title']=bundle['context']['concept_name'] if len(selected)>1 else selected[0]['title']
            for tb in selected:
                text=tb['content']
                if tb['purpose']=='intro':text=intro[key]
                elif tb['purpose']=='example':
                    text=text.split('\n\n')[0]
                    text=re.sub(r'^Suppose ', 'In this fictional fixture, ',text)
                    text=re.sub(r'^For this invented ', 'For this fixture’s ',text)
                    text=re.sub(r'^Consider the fixture ', 'Inspect the supplied fixture ',text)
                elif tb['purpose'] in ('definition','mechanism'):
                    text=text.replace('before accepting the input','before acceptance').replace('rather than continuing with an invalid array','instead of continuing with invalid input').replace('so callers can check the same fields','for repeatable caller checks')
                if tb['purpose'] in ('definition','mechanism'):
                    facts_by_id={f['id']:f['statement'] for f in bundle['coverage']['required_facts']}
                    for fid in tb['fact_ids']:
                        statement=facts_by_id[fid]
                        statement=statement.replace('before accepting the input','before acceptance').replace('rather than continuing with an invalid array','instead of continuing with invalid input')
                        s['blocks'].append(prose(statement,cid,[cid+'#'+tb['id']],[cid+'#'+fid],tb['purpose']))
                else:
                    for part in split_text(text):
                        s['blocks'].append(prose(part,cid,[cid+'#'+tb['id']],[cid+'#'+f for f in tb['fact_ids']],tb['purpose']))
            if step['planned_visual_block_type']:
                s['blocks']+=visual(cid,step['planned_visual_block_type'])
        for i,block in enumerate(s.get('blocks',[]),1):block['block_id']=s['step_id']+f'.b{i:02}'
        result['steps'].append(s)
    # Distinct planned measured fact sets receive distinct retry screens. No interactions are authored here.
    seen=set()
    for step in tile['steps']:
        if step['type'] not in ('check','hands_on'):continue
        cid=step['concept_ids'][0]; signature=(cid,tuple(step['fact_ids']))
        if signature in seen:continue
        seen.add(signature); key=cid.split('.',1)[1]; b=bundles[cid]
        facts={cid+'#'+f['id']:f['statement'] for f in b['coverage']['required_facts']}
        measured=step['fact_ids']
        blocks=[]; used=[]
        for fid in measured:
            tb=next(tb for tb in b['teaching_blocks'] if fid.split('#')[1] in tb['fact_ids'] and tb['purpose']!='example')
            qtb=cid+'#'+tb['id'];used.append(qtb)
            blocks.append(prose(facts[fid],cid,[qtb],[fid],'definition'))
        blocks.append(prose(contrast[key],cid,[],[], 'misconception'))
        # Same registered fixture provides the concrete contrast, without revealing interaction keys.
        ds={'prediction_task_definition':'ds.task_record','numpy_shape_dtype':'ds.order_features','numpy_dtype_selection':'ds.dtype_reference',
            'numpy_vectorization':'ds.order_features','file_object_ingestion':'ds.orders','chunked_ingestion':'ds.chunked_orders',
            'dataset_inspection':'ds.order_features','dataset_schema_validation':'ds.distance_zone','dataset_cleaning_policy':'ds.cleaning_orders',
            'dataset_selection_bias':'ds.selection_counts','label_integrity':'ds.labels','deployment_matched_splits':'ds.group_orders',
            'training_fitted_imputation':'ds.imputation_train','training_fitted_scaling':'ds.scaling_train','categorical_encoding':'ds.zone_train',
            'preprocessing_pipeline':'ds.distance_zone','prediction_boundary_leakage':'ds.orders','leakage_safe_features':'ds.feature_records',
            'sensitive_ml_assets':'ds.audit_sample'}
        blocks.append(table(ds[key],cid))
        rid=tile['tile_id']+f'.r{len(result["remediation_steps"])+1:02}'
        for i,block in enumerate(blocks,1):block['block_id']=rid+f'.b{i:02}'
        result['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':[cid],
          'eyebrow':'Try the distinction again','title':'Revisit: '+b['context']['concept_name'],
          'blocks':blocks,'lineage':lineage(cid,list(dict.fromkeys(used)),measured)})
    out['tiles'].append(result)
(B/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Wrote',len(out['tiles']),'tiles',sum(len(t['steps']) for t in out['tiles']),'planned steps',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
