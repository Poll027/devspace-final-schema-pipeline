import json, sys, subprocess, copy, textwrap
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
bs={b['context']['concept_id']:b for b in G['bundles']}; assets={a['asset_id']:a for a in R['assets']}; screens={t['tile_id']:t for t in S['tiles']}
rt=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']
def fix(name):
 return json.loads(next(f['content'] for f in assets['ws.'+name]['files'] if f['path']=='fixtures.json'))
def clean(x):return textwrap.dedent(x).strip()+'\n'
# Each entry is a concrete question, one correct answer and misconception-based wrong answers with explanations.
checks=[
('An order is predicted at acceptance. Distance and promised zone are known then; eventual arrival is recorded later. Which field must be excluded from prediction inputs?', 'Eventual arrival time','It is unavailable at acceptance even though it can establish the target.', [('Distance','The supplied task says distance is available at acceptance.'),('Promised delivery zone','The supplied task says the promised zone is available at acceptance.')]),
('A contract requires rank 2, width 2 and between one and three orders. Which fixture satisfies it?', '[[2, 10]]','It has one order and two features on separate axes.', [('[]','The empty fixture does not satisfy the nonempty two-axis contract.'),('[2, 10, 4, 20, 6, 30]','Six values in a flat list do not establish rank 2.'),('[[2], [4], [6]]','The second axis has width one, not two.')]),
('Two casts use less element storage than the reference. Which evidence is sufficient to accept a candidate under a declared precision tolerance and element-storage budget?', 'Every supplied value meets the precision tolerance, and size times itemsize agrees with nbytes and meets the budget.','Both value preservation and fixed-width element storage must be checked.', [('Its nbytes is smaller, without a value comparison.','Byte savings alone do not establish value preservation.'),('Its element count is unchanged, without checking scalar differences.','An unchanged size does not show that a cast preserved values.')]),
('For a (3, 2) array a, subtract [1, 5] feature-wise. Which expression performs the declared elementwise subtraction?', 'a - np.array([1, 5])','A length-two offset aligns with the two feature columns.', [('a - np.array([1, 5, 1])','A length-three vector does not align with the trailing dimension of size two.'),('a - 1','The second feature requires subtraction of five, not one.')]),
('Which code writes a local identity record inside an explicit UTF-8 file-handle block?', 'with open(path, "w", encoding="utf-8") as f:\n    f.write(text)','The write occurs through the handle while the file is open.', [('with open(path, "r", encoding="utf-8") as f:\n    f.write(text)','Read mode does not express the required write operation.'),('with open(path, "w", encoding="utf-8") as f:\n    pass\nf.write(text)','The write is outside the open-file block, after the handle is closed.')]),
('A file produces full chunks and a final shorter chunk. Which check supports the declared single-array allocation bound?', 'For every chunk, compute bytes from its actual matrix shape and dtype, compare with nbytes and check against the budget.','The final short chunk is a materialized matrix too.', [('Check only the configured row_limit, without inspecting actual matrices.','The configured limit is not evidence of each actual matrix allocation.'),('Use the single-array bound as a claim about total process memory.','Element storage does not bound reader buffers or process memory.')]),
('A readiness record reports shape (3, 2) for a numerical array under a two-axis contract. Which interpretation matches that contract?', 'Three observations, two features per observation.','The first axis is the observation axis and the second is the feature axis.', [('Two observations, three features per observation.','That reverses the declared axis meanings.'),('Six observations, each with one feature.','Total elements do not replace the two-axis structure.')]),
('A supplied schema violation must be rejected at the function boundary. Which mechanism matches that role?', 'Raise a descriptive ValueError from the validation branch.','Explicit validation rejects the input; assert checks fixture expectations.', [('Use only assert and assume it is permanent input validation.','Assertions can be disabled; they are for ordinary fixture verification here.'),('Change the bad value silently until an assertion passes.','Validation must identify the violation rather than mutate the input.')]),
('Under ordinary non-optimized Python execution, a cleaning fixture has an intentionally false assert predicate. What should happen?', 'It raises AssertionError.','A false assert predicate fails the fixture verification.', [('It silently repairs the input.','An assertion checks a predicate; the policy branches implement repairs.'),('It reports successful validation.','A false predicate cannot establish the expected cleaning result.')]),
('Included category members are known, but the target category count is zero. Which inclusion-rate interpretation is defensible?', 'The denominator cannot support a rate; report it as unsupported.','Inclusion probability requires a positive target-membership denominator.', [('Report zero because no target members exist.','An empty denominator does not establish a zero inclusion rate.'),('Divide by the entire sample size instead.','That denominator describes sample share, not category-specific inclusion.')]),
('An audit verifies fixture acceptance and affected IDs with assert predicates. What makes a deliberately incorrect expected verdict useful under ordinary non-optimized execution?', 'Its false predicate raises AssertionError.','The assertion checks the expectation rather than rewriting the verdict.', [('It remaps labels into row order automatically.','Assertions do not replace the required keyed label mapping.'),('It must still pass because the function ran.','Executing the function is not the same as meeting its expected verdict.')]),
('Which assert predicate directly verifies a required group-disjoint evaluation boundary?', 'assert not (training_groups & validation_groups)','A nonempty intersection violates the declared group boundary.', [('assert len(training_groups) > 0','A nonempty training set does not establish group disjointness.'),('assert training_groups == validation_groups','Equal nonempty group sets violate the required disjointness.')]),
('A mean imputer was fitted on training rows. Which assertion evidence verifies validation reuse?', 'Validation outputs match the declared replacements and statistics_ equals its saved training value after transformation.','Both the outputs and fitted-state invariant must hold.', [('Only the transformed validation shape matches.','The correct shape does not establish correct replacement values or unchanged fitted state.'),('statistics_ was recomputed from validation before comparison.','That replaces training-fitted state rather than verifying reuse.')]),
('Which checks verify that validation scaling reused the training-fitted scaler?', 'Check expected transformed values and compare mean_ and scale_ to their saved training values.','Numerical output and unchanged fitted parameters jointly verify reuse.', [('Refit on validation, then save the new parameters.','Refitting makes the validation representation separately fitted.'),('Check only that the output has the same row count.','Row count alone does not verify numerical results or fitted-state reuse.')]),
('Which fixture check respects a fitted encoder mapping?', 'Align known, unseen and missing cases with categories_, assert their policy-specific indicators and unchanged output width.','The stored training categories determine the indicator columns.', [('Assume the first indicator always means north without inspecting categories_.','Indicator positions must be aligned with the fitted mapping.'),('Fit separately on each case and compare the resulting widths.','That relearns categories instead of checking training-state reuse.')]),
('Which assertion evidence supports reuse of a composed preprocessing pipeline?', 'Expected representations and predictions, unchanged fitted preprocessing state, and declared missing/malformed input outcomes.','Reuse needs both correct outputs and unchanged fitted state.', [('A second fit on validation completes without error.','Validation should pass through the existing fitted object, not refit it.'),('The pipeline object has a name.','Naming an object does not verify its fitted-state or input behavior.')]),
('An acceptance-time prediction uses a field populated only after arrival. Why is this a boundary defect?', 'It supplies information unavailable when the prediction is made.','Future information violates the task boundary.', [('A held-out file makes the future field acceptable.','Holding out labels does not make a future input decision-available.'),('A strong held-out score removes the timing restriction.','Performance estimates do not remove the prediction-time information boundary.')]),
('A sum feature should be unaffected by an added later unavailable record. Which test checks that requirement?', 'Compare the original feature with the feature on records augmented by the later record, and assert equality.','The filter must precede arithmetic so unavailable additions cannot change the earlier feature.', [('Compare the number of records before and after augmentation.','Input length can change while the earlier feature must remain unchanged.'),('Add the later value to the expected sum.','That allows unavailable information to change the feature.')]),
('Which action removes a literal credential from a generated diagnostic record under the supplied policy?', 'Exclude token from the generated record and keep credential use in the authorized runtime secret mechanism.','Moving a literal credential into another generated asset retains exposure.', [('Copy token into image metadata instead.','Credentials in image metadata can be exposed.'),('Rename token to diagnostic_value and keep its value.','Renaming a credential does not remove the literal credential from the record.')])
]
configs={}
def code(name, prompt, scaffold, body, probes, packages=None, mounts=None):
 configs['mle.'+name]={'prompt':prompt,'scaffold':clean(scaffold) if scaffold.strip() else '', 'body':clean(body),'probes':probes,'packages':packages or ['numpy'],'mounts':mounts or []}
def fc(args,fn='evaluate'):return {'kind':'function_call','spec':{'function':fn,'args':args}}
def ve(expr):return {'kind':'value_equals','spec':{'expr':expr}}
def evaluate_scaffold(fn):return f'''def evaluate(fixture):
    try:
        return {{"accepted": True, "result": {fn}(fixture)}}
    except ValueError as error:
        return {{"accepted": False, "reason": str(error)}}
'''
f=fix('numpy_shape_dtype')
code('numpy_shape_dtype','Write import numpy as np and inspect(fixture). Convert the list or tuple with np.array, observe ndim, shape and dtype without casting. Check rank before indexing axes; reject rank != 2, width != 2, or batch outside inclusive [1,3] with ValueError("rank"), ValueError("width") or ValueError("batch"). Return a dictionary with rank, shape, dtype (the observed dtype object), batch, width and valid=True. Write assertions for accepted list and tuple fixtures and each supplied rejection. The evaluate wrapper exposes exceptions as results.',evaluate_scaffold('inspect'),'''
import numpy as np
def inspect(fixture):
    a = np.array(fixture)
    rank = a.ndim
    shape = a.shape
    dtype = a.dtype
    if rank != 2:
        raise ValueError("rank")
    batch = shape[0]
    width = shape[1]
    if width != 2:
        raise ValueError("width")
    if batch < 1 or batch > 3:
        raise ValueError("batch")
    valid = True
    assert rank == 2 and width == 2 and batch >= 1 and batch <= 3
    return {"rank": rank, "shape": shape, "dtype": dtype, "batch": batch, "width": width, "valid": valid}
''',[fc([f[k]]) for k in ['valid','tuple_boundary','empty','flat','wrong_width','too_many']])
# Dtype exercise also evaluates precision boundaries independently of the base matrix.
f=fix('numpy_dtype_selection')
sc='''def evaluate(fixture):
    return compare(fixture["reference"], fixture["candidates"], fixture["tolerance"], fixture["budget"])
'''
args=[{'reference':f['a'],'candidates':f['candidate_dtypes'],'tolerance':f['tolerance'],'budget':f['element_storage_budget']}, {'reference':[f['boundary_values']],'candidates':f['candidate_dtypes'],'tolerance':f['tolerance'],'budget':f['element_storage_budget']},{'reference':[f['integer_cast_probe']['reference']],'candidates':['int64'],'tolerance':0,'budget':24}]
code('numpy_dtype_selection','Write import numpy as np and compare(reference, candidates, tolerance, budget). Explicitly cast each candidate from an unchanged np.array(reference). Check every two-dimensional scalar against the reference using absolute difference <= tolerance. Return one dictionary per candidate containing dtype (observed dtype), size, element_bytes=size*itemsize, nbytes, preserved (Boolean), accepted (preserved AND element_bytes <= budget), and justification="element storage, not total object memory". Reject candidates failing either condition; do not change the reference. Include the supplied boundary and integer-cast probes.',sc,'''
import numpy as np
def compare(reference, candidates, tolerance, budget):
    a = np.array(reference)
    results = []
    for candidate_dtype in candidates:
        candidate = a.astype(candidate_dtype)
        preserved = True
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                if abs(candidate[i, j] - a[i, j]) > tolerance:
                    preserved = False
        element_bytes = candidate.size * candidate.itemsize
        accepted = preserved and element_bytes <= budget
        results = results + [{"dtype": candidate.dtype, "size": candidate.size, "element_bytes": element_bytes, "nbytes": candidate.nbytes, "preserved": preserved, "accepted": accepted, "justification": "element storage, not total object memory"}]
    return results
''',[fc([x]) for x in args])
f=fix('numpy_vectorization'); a=assets['ds.order_features']['rows']
code('numpy_vectorization','Write import numpy as np and transform(fixture). Subtract offsets [1,5] feature-wise from np.array(fixture). Independently build a nested list-comprehension reference using scalar subtraction. Assert shape == (number of supplied rows,2) and agreement with that reference using np.testing.assert_allclose with rtol=1e-7 and atol=1e-9. Return the transformed array. The supplied width-two fixtures determine the row count in the scaffold.', '''def evaluate(fixture):
    return transform(fixture)
''','''
import numpy as np
def transform(fixture):
    a = np.array(fixture)
    result = a - np.array([1, 5])
    reference = [[row[0] - 1, row[1] - 5] for row in fixture]
    assert result.shape == a.shape
    np.testing.assert_allclose(result, np.array(reference), rtol=1e-7, atol=1e-9)
    return result
''',[fc([a]),fc([a[:1]]),fc([[[1,5],[3,15]]])])
f=fix('chunked_ingestion')
code('chunked_ingestion','Write import pandas as pd and scan(path,budget,feature_count,element_width,declared_types). Choose row_limit by budget // (feature_count*element_width). Keep with open(path) active throughout pd.read_csv(..., chunksize=row_limit, dtype=declared_types) iteration. For EVERY matrix, including the final short chunk, derive element bytes from actual shape and dtype, assert equality to nbytes and <= budget, and track the largest single matrix allocation. Return {row_limit, largest_element_bytes, memory_scope:"single matrix element storage only"}. Delete the materialized matrix after checking. The main fixture has a 16,000-byte budget, 20 features and eight-byte elements.', '''def evaluate(budget):
    return scan("ds.chunked_orders.csv",budget,FEATURE_COUNT,ELEMENT_WIDTH,DECLARED_TYPES)
'''+f'FEATURE_COUNT = {f["feature_count"]!r}\nELEMENT_WIDTH = {f["element_width"]!r}\nDECLARED_TYPES = {f["declared_types"]!r}\n','''
import pandas as pd
def scan(path, budget, feature_count, element_width, declared_types):
    row_limit = budget // (feature_count * element_width)
    largest = 0
    with open(path) as file_handle:
        for chunk in pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types):
            matrix = chunk.to_numpy()
            rows, columns = matrix.shape
            element_bytes = rows * columns * matrix.dtype.itemsize
            assert element_bytes == matrix.nbytes
            assert element_bytes <= budget
            largest = max(largest,element_bytes)
            del matrix
    return {"row_limit":row_limit,"largest_element_bytes":largest,"memory_scope":"single matrix element storage only"}
''',[fc([f['array_budget']]),fc([f['array_budget']//2])],['pandas'],[{'asset_id':'ds.chunked_orders','mount_path':f['path']}])
f=fix('dataset_inspection')
code('dataset_inspection','Write import numpy as np and readiness(fixture,ddof=0). Return consistently named fields: observations, features, shape, dtype (observed dtype object), element_bytes, means, standard_deviations, and memory_scope="element storage, not total process memory". Use feature-wise axis=0 means and standard deviations with the supplied ddof, defaulting to population ddof=0. Derive bytes from shape and dtype.itemsize. Return the report for any same-width numerical fixture.', 'def evaluate(fixture):\n    return readiness(fixture)\n','''
import numpy as np
def readiness(fixture, ddof=0):
    numeric_values = np.array(fixture)
    shape = numeric_values.shape
    return {"observations":shape[0],"features":shape[1],"shape":shape,"dtype":numeric_values.dtype,"element_bytes":shape[0]*shape[1]*numeric_values.dtype.itemsize,"means":np.mean(numeric_values,axis=0),"standard_deviations":np.std(numeric_values,axis=0,ddof=ddof),"memory_scope":"element storage, not total process memory"}
''',[fc([a]),fc([[[1,5],[3,15],[5,25]]])])
f=fix('dataset_schema_validation')
# Table construction and result/exception capture are supplied scaffolding, not learner syntax.
sc='''import pandas as pd
def evaluate(fixture):
    table = pd.DataFrame(fixture["rows"], columns=fixture["columns"])
    if "types" in fixture:
        table = table.astype(fixture["types"])
    before = table.copy(deep=True)
    try:
        result = validate(table)
        return {"accepted":result,"unchanged":table.equals(before)}
    except ValueError as error:
        return {"accepted":False,"reason":str(error),"unchanged":table.equals(before)}
'''
base={'rows':assets['ds.distance_zone']['rows'],'columns':['distance','zone'],'types':{'distance':'float64','zone':'object'}}
cases=[base]
for kind in ['columns','type','distance_low','distance_high','zone']:
 x=copy.deepcopy(base)
 if kind=='columns':x['columns']=['distance','other'];x['types']={'distance':'float64','other':'object'}
 if kind=='type':x['types']['distance']='object'
 if kind=='distance_low':x['rows'][0][0]=-1
 if kind=='distance_high':x['rows'][0][0]=101
 if kind=='zone':x['rows'][0][1]='east'
 cases.append(x)
code('dataset_schema_validation','Write validate(table). Require exactly columns distance and zone, distance dtype float64 and zone dtype object, every distance inclusive [0,100], and every zone north or south. Reject violations with ValueError("columns"), ValueError("types"), ValueError("distance") or ValueError("zone") in that order. Do not mutate the table. Return True for accepted input and author assert predicates confirming each accepted requirement. The supplied evaluate wrapper constructs typed tables, captures validation exceptions and verifies unchanged input.',sc,'''
def validate(table):
    if set(table.columns) != {"distance","zone"}:
        raise ValueError("columns")
    if table.dtypes["distance"] != "float64" or table.dtypes["zone"] != "object":
        raise ValueError("types")
    distances = (table["distance"] >= 0) & (table["distance"] <= 100)
    zones = (table["zone"] == "north") | (table["zone"] == "south")
    if not distances.all():
        raise ValueError("distance")
    if not zones.all():
        raise ValueError("zone")
    assert distances.all() and zones.all()
    return True
''',[fc([x]) for x in cases],['pandas'])
f=fix('dataset_cleaning_policy')
code('dataset_cleaning_policy','Write clean_orders(records,policy). Use an accepted-key set; reject repeated already-accepted order keys, reject distance outside inclusive policy bounds, repair only zone spelling in zone_repairs, otherwise retain. Add keys only after acceptance. Return {cleaned:[accepted records],actions:[{observation_id,action} for repairs/rejections]}. Preserve observation IDs, never silently change a row. Write assertions for boundaries, repairs, rejected and repeated keys; the supplied evaluate wrapper compares complete outputs.', 'def evaluate(records):\n    return clean_orders(records,POLICY)\n'+f'POLICY = {f["policy"]!r}\n','''
def clean_orders(records, policy):
    accepted = set()
    cleaned = []
    actions = []
    for row in records:
        key = row["order_key"]
        action = "retain"
        zone = row["zone"]
        if key in accepted:
            action = policy["repeat_accepted_key"]
        elif row["distance"] < policy["distance_min"] or row["distance"] > policy["distance_max"]:
            action = policy["invalid_distance"]
        elif zone in policy["zone_repairs"]:
            zone = policy["zone_repairs"][zone]
            action = "repair"
        if action != "reject":
            accepted.add(key)
            cleaned.append({"observation_id":row["observation_id"],"order_key":key,"distance":row["distance"],"zone":zone})
            assert key in accepted
            assert row["distance"] >= policy["distance_min"] and row["distance"] <= policy["distance_max"]
        if action != "retain":
            actions.append({"observation_id":row["observation_id"],"action":action})
    return {"cleaned":cleaned,"actions":actions}
''',[fc([f['records']]),fc([f['valid']]),fc([[f['records'][3],{'observation_id':'retry_D','order_key':'D','distance':100,'zone':'south'}]])],['numpy'])
f=fix('dataset_selection_bias'); counts=assets['ds.selection_counts']['rows']
sc=f'''import numpy as np
sample_a = {counts[0][1]!r}
sample_b = {counts[1][1]!r}
target_a = {counts[0][2]!r}
target_b = {counts[1][2]!r}
numeric_values = np.array({f['numeric_values']!r})
'''
code('dataset_selection_bias','Compute sample_a_share, sample_b_share using the combined sample denominator; target_a_share, target_b_share using the combined target denominator; inclusion_a and inclusion_b using each corresponding target-category denominator. If a category target denominator is zero set its inclusion to the string "unsupported". Compute mean and standard_deviation from numeric_values with ddof=0. Record limitation="Zone B has lower inclusion and sample share than its target share; counts do not identify a cause or prove prediction failure". These inspectable variable names are graded.',sc,'''
sample_a_share = sample_a / (sample_a + sample_b)
sample_b_share = sample_b / (sample_a + sample_b)
target_a_share = target_a / (target_a + target_b)
target_b_share = target_b / (target_a + target_b)
if target_a > 0:
    inclusion_a = sample_a / target_a
else:
    inclusion_a = "unsupported"
if target_b > 0:
    inclusion_b = sample_b / target_b
else:
    inclusion_b = "unsupported"
mean = np.mean(numeric_values)
standard_deviation = np.std(numeric_values,ddof=0)
limitation = "Zone B has lower inclusion and sample share than its target share; counts do not identify a cause or prove prediction failure"
''',[ve('[sample_a_share,sample_b_share,target_a_share,target_b_share,inclusion_a,inclusion_b,mean,standard_deviation,limitation]')])
# Keyed label audit. Supplied acceptance rules are infrastructure, not guessed universal task policy.
f=fix('label_integrity')
sc='''def label_valid(label):
    return label["label"] in (0,1)
def aligned(observation,label):
    return observation["observation_timestamp"] == label["observation_timestamp"]
def available(label,boundary):
    return label["availability_timestamp"] <= boundary
def evaluate(fixture):
    return audit(fixture["observations"],fixture["labels"],fixture["boundary"])
'''
code('label_integrity','Write audit(observations,labels,boundary). Check repeated IDs BEFORE constructing the keyed label dictionary. Return {accepted,duplicate_observations,duplicate_labels,missing,orphaned,invalid,misaligned,unavailable}, with each issue field a set of affected IDs. Use the supplied label_valid, aligned and available predicates; availability equality at the supplied task boundary is accepted. Reordering alone is acceptable. If duplicate IDs exist, do not build a replacing ID mapping; still report missing/orphaned IDs. Otherwise perform keyed checks. Write assertions that accepted implies every issue set is empty.',sc,'''
def audit(observations,labels,boundary):
    observation_ids = set()
    label_ids = set()
    duplicate_observations = set()
    duplicate_labels = set()
    for observation in observations:
        oid = observation["observation_id"]
        if oid in observation_ids:
            duplicate_observations.add(oid)
        observation_ids.add(oid)
    for label in labels:
        oid = label["observation_id"]
        if oid in label_ids:
            duplicate_labels.add(oid)
        label_ids.add(oid)
    missing = observation_ids - label_ids
    orphaned = label_ids - observation_ids
    invalid = set()
    misaligned = set()
    unavailable = set()
    if not duplicate_labels and not duplicate_observations:
        mapping = {}
        for label in labels:
            mapping[label["observation_id"]] = label
        for observation in observations:
            oid = observation["observation_id"]
            if oid in mapping:
                label = mapping[oid]
                if not label_valid(label):
                    invalid.add(oid)
                if not aligned(observation,label):
                    misaligned.add(oid)
                if not available(label,boundary):
                    unavailable.add(oid)
    accepted = not (duplicate_observations or duplicate_labels or missing or orphaned or invalid or misaligned or unavailable)
    if accepted:
        assert observation_ids == label_ids
        assert not invalid and not misaligned and not unavailable
    return {"accepted":accepted,"duplicate_observations":duplicate_observations,"duplicate_labels":duplicate_labels,"missing":missing,"orphaned":orphaned,"invalid":invalid,"misaligned":misaligned,"unavailable":unavailable}
''',[])
# Add exact registry fixture shapes after reading its contract.
configs['mle.label_integrity']['probes']=[fc([{'observations':f['observations'],'labels':labels,'boundary':f['contract']['availability_cutoff']}]) for labels in [f['labels']]+list(f['cases'].values())]
configs['mle.label_integrity']['probes'].append(fc([{'observations':f['observations']+[f['observations'][0]],'labels':f['labels'],'boundary':f['contract']['availability_cutoff']}]))
# Splits
f=fix('deployment_matched_splits')
sc='''def evaluate(fixture):
    return partition(fixture["records"],fixture["scenario"],fixture["training_groups"],fixture["cutoff"],fixture["end"])
'''
code('deployment_matched_splits','Write partition(records,scenario,training_groups,cutoff,end). For scenario="group", place supplied training_groups wholly in training and all remaining groups in validation. For scenario="time", train on timestamp < cutoff and validate on cutoff <= timestamp < end. Return {training:[records],validation:[records],training_proportion,validation_proportion,justification}; divide target counts by each nonempty partition total, using None for an empty partition. justification is "disjoint groups" or "training before cutoff; validation in later interval". Author assertions for empty group intersection or exact time inequalities. The evaluation harness includes cutoff-equality and invalid-boundary cases.',sc,'''
def partition(records,scenario,training_groups,cutoff,end):
    if scenario == "group":
        training = [row for row in records if row["customer_group"] in training_groups]
        validation = [row for row in records if row["customer_group"] not in training_groups]
        train_groups = {row["customer_group"] for row in training}
        valid_groups = {row["customer_group"] for row in validation}
        assert not (train_groups & valid_groups)
        justification = "disjoint groups"
    else:
        training = [row for row in records if row["observation_timestamp"] < cutoff]
        validation = [row for row in records if cutoff <= row["observation_timestamp"] and row["observation_timestamp"] < end]
        for row in training:
            assert row["observation_timestamp"] < cutoff
        for row in validation:
            assert cutoff <= row["observation_timestamp"] and row["observation_timestamp"] < end
        justification = "training before cutoff; validation in later interval"
    training_proportion = None
    validation_proportion = None
    if len(training) > 0:
        training_proportion = sum([row["target"] for row in training])/len(training)
    if len(validation) > 0:
        validation_proportion = sum([row["target"] for row in validation])/len(validation)
    return {"training":training,"validation":validation,"training_proportion":training_proportion,"validation_proportion":validation_proportion,"justification":justification}
''',[fc([{'records':f['group_records'],'scenario':'group','training_groups':f['training_groups'],'cutoff':f['cutoff'],'end':f['evaluation_end']}]),fc([{'records':f['time_records'],'scenario':'time','training_groups':f['training_groups'],'cutoff':f['cutoff'],'end':f['evaluation_end']}])])
# Training-fitted imputation
f=fix('training_fitted_imputation')
sc='''def evaluate(fixture):
    return replace_missing(fixture["train"],fixture["validation"],fixture["single_missing"])
'''
code('training_fitted_imputation','Write the NumPy and SimpleImputer imports and replace_missing(train,validation,single_missing). Convert None markers to np.nan in the supplied scaffold helper. Fit a mean SimpleImputer on training only. Compute columnwise mean and ddof=0 spread from the observed training distances. Save statistics_, transform validation and the single-missing boundary input without refitting, and assert output equality to the corresponding observed-training mean for each missing value and unchanged statistics_. Return {mean,spread,statistics,validation,single_missing}. The supplied wrapper converts JSON missing values before calling the function.',sc+'''def array_with_missing(rows):
    import numpy as np
    return np.array([[np.nan if value is None else value for value in row] for row in rows])
''','''
import numpy as np
from sklearn.impute import SimpleImputer
def replace_missing(train,validation,single_missing):
    X_train = array_with_missing(train)
    X_validation = array_with_missing(validation)
    numeric_values = X_train[:2]
    mean = np.mean(numeric_values,axis=0)
    spread = np.std(numeric_values,axis=0,ddof=0)
    imputer = SimpleImputer(strategy="mean")
    imputer.fit(X_train)
    saved = imputer.statistics_.copy()
    output = imputer.transform(X_validation)
    boundary = imputer.transform(array_with_missing(single_missing))
    assert np.array_equal(saved,imputer.statistics_)
    assert np.allclose(output[1],mean)
    assert np.allclose(boundary[0],mean)
    assert np.allclose(output[0],X_validation[0])
    return {"mean":mean,"spread":spread,"statistics":imputer.statistics_,"validation":output,"single_missing":boundary}
''',[fc([{'train':f['X_train'],'validation':f['X_validation'],'single_missing':[[None]]}]),fc([{'train':[[4],[8],[None]],'validation':[[90],[None]],'single_missing':[[None]]}])],['numpy','scikit-learn','scipy'])
f=fix('training_fitted_scaling')
code('training_fitted_scaling','Write NumPy and StandardScaler imports and scale(train,validation). Fit StandardScaler(with_mean=True,with_std=True) on training only; save mean_ and scale_ copies; transform training and validation. Assert unchanged fitted state and numerical agreement with (validation - saved_mean)/saved_scale. Compute columnwise training mean and ddof=0 spread. Return {mean,spread,scale,training,validation}; constant features must have scale_=1. The supplied evaluate wrapper calls your function with different fixtures.', 'def evaluate(fixture):\n    return scale(fixture["train"],fixture["validation"])\n','''
import numpy as np
from sklearn.preprocessing import StandardScaler
def scale(train,validation):
    X_train = np.array(train)
    X_validation = np.array(validation)
    scaler = StandardScaler(with_mean=True,with_std=True)
    scaler.fit(X_train)
    saved_mean = scaler.mean_.copy()
    saved_scale = scaler.scale_.copy()
    training = scaler.transform(X_train)
    output = scaler.transform(X_validation)
    assert np.allclose(saved_mean,scaler.mean_)
    assert np.allclose(saved_scale,scaler.scale_)
    assert np.allclose(output,(X_validation-saved_mean)/saved_scale)
    mean = np.mean(X_train,axis=0)
    spread = np.std(X_train,axis=0,ddof=0)
    return {"mean":mean,"spread":spread,"scale":scaler.scale_,"training":training,"validation":output}
''',[fc([{'train':f['X_train'],'validation':f['X_validation']}]),fc([{'train':[[4,5],[8,5]],'validation':[[10,5]]}])],['numpy','scikit-learn','scipy'])
f=fix('categorical_encoding')
sc='''def evaluate(fixture):
    return encode(fixture["training"],fixture["cases"],fixture["policy"])
def category_array(rows):
    import numpy as np
    return np.array([[np.nan if x is None else x for x in row] for row in rows],dtype=object)
def same_categories(left,right):
    import numpy as np
    return repr(left) == repr(right)
'''
code('categorical_encoding','Write NumPy and OneHotEncoder imports and encode(training,cases,policy). Fit OneHotEncoder(handle_unknown=policy,sparse_output=False) only on training. Build mapping={"zone":categories_[0].tolist()}. For each list-based case, return its array indicators or the string "ValueError" if the error policy rejects it. Save categories_ and assert they remain unchanged and each accepted result has the training output width. Return {mapping,width,results}. None becomes np.nan through the supplied category_array helper; same_categories handles matching missing-category markers. Known, unseen and missing fixtures are tested under ignore and error, with and without fit-time missingness.',sc,'''
import numpy as np
from sklearn.preprocessing import OneHotEncoder
def encode(training,cases,policy):
    encoder = OneHotEncoder(handle_unknown=policy,sparse_output=False)
    encoder.fit(category_array(training))
    saved = encoder.categories_[0].copy()
    mapping = {"zone":saved.tolist()}
    width = len(saved)
    results = []
    for case in cases:
        try:
            output = encoder.transform(category_array(case))
            assert output.shape[1] == width
            results = results + [output.tolist()]
        except ValueError:
            results = results + ["ValueError"]
        assert same_categories(saved,encoder.categories_[0])
    return {"mapping":mapping,"width":width,"results":results}
''',[fc([{'training':f[k],'cases':list(f['cases'].values()),'policy':policy}]) for k in ['X_train','X_train_missing'] for policy in f['unknown_policies']],['numpy','scikit-learn','scipy'])
# The deterministic estimator is supplied registry infrastructure, not a model-selection task.
f=fix('preprocessing_pipeline');runtime=next(x['content'] for x in assets['ws.preprocessing_pipeline']['files'] if x['path']=='authorized_runtime.py')
sc=runtime+'''
def evaluate(fixture):
    return workflow(fixture["train"],fixture["target"],fixture["validation"],fixture["inference"],fixture["malformed"])
'''
code('preprocessing_pipeline','Write the prerequisite library imports and workflow(train,target,validation,inference,malformed). Compose numerical mean imputation then StandardScaler, categorical OneHotEncoder(ignore,sparse_output=False), a ColumnTransformer selecting [distance] and [zone], and a Pipeline with the supplied FixtureEstimator. Fit once on train,target; predict validation and bounded inference through the SAME fitted pipeline. Save distance imputer statistics and scaler mean_/scale_, plus categorical categories_. Assert these remain unchanged after both predictions. Assert the specified missing value produces a zero scaled distance, inspect the transformed representation, and verify malformed missing-zone input raises ValueError. Return {validation_representation,validation_predictions,inference_predictions,missing_scaled_distance,malformed_rejected,imputer_statistics,scaler_mean,scaler_scale,categories}.',sc,'''
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
def workflow(train,target,validation,inference,malformed):
    X_train = pd.DataFrame(train)
    X_validation = pd.DataFrame(validation)
    numeric = Pipeline([("imputer",SimpleImputer(strategy="mean")),("scaler",StandardScaler(with_mean=True,with_std=True))])
    categorical = OneHotEncoder(handle_unknown="ignore",sparse_output=False)
    preprocessor = ColumnTransformer([("numeric",numeric,["distance"]),("categorical",categorical,["zone"])])
    pipeline = Pipeline([("preprocessor",preprocessor),("estimator",FixtureEstimator())])
    pipeline.fit(X_train,target)
    fitted = pipeline.named_steps["preprocessor"]
    imputer = fitted.named_transformers_["numeric"].named_steps["imputer"]
    scaler = fitted.named_transformers_["numeric"].named_steps["scaler"]
    encoder = fitted.named_transformers_["categorical"]
    saved_imputer = imputer.statistics_.copy()
    saved_mean = scaler.mean_.copy()
    saved_scale = scaler.scale_.copy()
    saved_categories = encoder.categories_[0].copy()
    validation_predictions = pipeline.predict(X_validation)
    representation = fitted.transform(X_validation)
    inference_predictions = pipeline.predict(pd.DataFrame(inference))
    assert np.array_equal(saved_imputer,imputer.statistics_)
    assert np.array_equal(saved_mean,scaler.mean_)
    assert np.array_equal(saved_scale,scaler.scale_)
    assert np.array_equal(saved_categories,encoder.categories_[0])
    assert np.allclose(representation[1,0],0)
    malformed_rejected = False
    try:
        pipeline.predict(pd.DataFrame(malformed))
    except ValueError:
        malformed_rejected = True
    assert malformed_rejected
    return {"validation_representation":representation,"validation_predictions":validation_predictions,"inference_predictions":inference_predictions,"missing_scaled_distance":representation[1,0],"malformed_rejected":malformed_rejected,"imputer_statistics":imputer.statistics_,"scaler_mean":scaler.mean_,"scaler_scale":scaler.scale_,"categories":encoder.categories_[0]}
''',[fc([{'train':f['X_train'],'target':f['y_train'],'validation':f['X_validation'],'inference':f['X_validation'][:1],'malformed':f['malformed']}]),fc([{'train':[{'distance':0,'zone':'north'},{'distance':4,'zone':'south'},{'distance':8,'zone':'north'}],'target':f['y_train'],'validation':f['X_validation'],'inference':f['X_validation'][:1],'malformed':f['malformed']}])],['numpy','pandas','scikit-learn','scipy'])
f=fix('prediction_boundary_leakage');runtime=next(x['content'] for x in assets['ws.prediction_boundary_leakage']['files'] if x['path']=='authorized_runtime.py')
sc=runtime+'''
def select_available(rows,fields):
    return [{field:row[field] for field in fields} for row in rows]
def evaluate(fixture):
    preprocessor=TracePreprocessor()
    predictor=TracePredictor()
    corrected(fixture["training"],fixture["held_out"],preprocessor,predictor)
    return {"fit_rows":preprocessor.fit_rows,"transform_rows":preprocessor.transform_rows,"prediction_inputs":predictor.input_rows}
'''
code('prediction_boundary_leakage','Repair corrected(training,held_out,preprocessor,predictor). The leaked sketch selects distance, zone, eventual_arrival, fits preprocessing on training+held_out and refits before prediction. Instead select only distance and zone using select_available, fit only training, then transform held_out without refitting and predict on the transformed held-out rows. Author assertions that traced fit_rows equal selected training and last transform/prediction inputs equal selected held_out; the same checks must fail for each leaked row/field path. Supplied TracePreprocessor and TracePredictor expose those traces. Return the predictions.',sc,'''
def corrected(training,held_out,preprocessor,predictor):
    fields = ["distance","zone"]
    train_inputs = select_available(training,fields)
    held_inputs = select_available(held_out,fields)
    preprocessor.fit(train_inputs)
    transformed = preprocessor.transform(held_inputs)
    predictions = predictor.predict(transformed)
    assert preprocessor.fit_rows == train_inputs
    assert preprocessor.transform_rows[-1] == held_inputs
    assert predictor.input_rows[-1] == held_inputs
    return predictions
''',[fc([{'training':f['training'],'held_out':f['held_out']}]),fc([{'training':f['training'][:1],'held_out':f['held_out'][:1]}])])
f=fix('leakage_safe_features')
sc='''def evaluate(fixture):
    records = as_datetime_records(fixture["records"])
    augmented = as_datetime_records(fixture["augmented"])
    boundary = as_datetime(fixture["boundary"])
    original = feature(records,boundary)
    changed = feature(augmented,boundary)
    assert original == changed
    return {"original":original,"augmented":changed}
def as_datetime(value):
    from datetime import datetime
    return datetime.fromisoformat(value)
def as_datetime_records(rows):
    return [{"available_at":as_datetime(row["available_at"]),"value":row["value"]} for row in rows]
'''
code('leakage_safe_features','Write from datetime import datetime and feature(records,prediction_time). Filter available_at <= prediction_time with the taught list comprehension, initialize total=0 and accumulate accepted values only. Return total. Write assertions that adding later unavailable observations leaves the feature unchanged, and that exact-boundary observations are included. The supplied evaluate harness converts ISO fixtures to datetime objects before calling your function, compares original and augmented results, and includes an empty case. This fixture is a sum, not a latest-lookup feature.',sc,'''
from datetime import datetime
def feature(records,prediction_time):
    accepted = [row for row in records if row["available_at"] <= prediction_time]
    total = 0
    for record in accepted:
        total += record["value"]
    return total
''',[fc([{'records':f['records'],'augmented':f['augmented_records'],'boundary':f['prediction_time']}]),fc([{'records':f['records'][-1:],'augmented':f['augmented_records'][1:],'boundary':f['prediction_time']}]),fc([{'records':[],'augmented':f['augmented_records'][-1:],'boundary':f['prediction_time']}])])
f=fix('sensitive_ml_assets');runtime=next(x['content'] for x in assets['ws.sensitive_ml_assets']['files'] if x['path']=='authorized_runtime.py')
# Runtime is present in the editable starter, but its import is a learner-authored dependency line using a supplied interface.
sc=runtime+'''
def evaluate(fixture):
    import io, contextlib
    output=io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            result=permitted_record(fixture["identity"],fixture["sample"],fixture["permitted"])
        return {"record":result,"stdout":output.getvalue(),"secret_usable":use_secret(fixture["identity"],"fixture_token")}
    except PermissionError:
        return {"denied":True,"stdout":output.getvalue()}
'''
code('sensitive_ml_assets','Write permitted_record(identity,sample,permitted_fields). Call the supplied read_sample(identity,sample) interface BEFORE reading fields; its existing policy raises PermissionError for an unauthorized identity. Construct a new dictionary with only fields in permitted_fields using membership checks. Return it without printing or copying token or raw_customer_values. Assert neither restricted key is in your output. The supplied evaluate harness captures output, checks denial, and verifies the secret remains usable only through use_secret, without exposing its literal. No extra library import is needed for this dictionary-only audit.',sc,'''
def permitted_record(identity,sample,permitted_fields):
    authorized = read_sample(identity,sample)
    result = {}
    for key,value in authorized.items():
        if key in permitted_fields:
            result[key] = value
    assert "token" not in result
    assert "raw_customer_values" not in result
    return result
''',[fc([{'identity':f['authorized_identity'],'sample':f['sample'],'permitted':f['permitted_fields']}]),fc([{'identity':f['unauthorized_identity'],'sample':f['sample'],'permitted':f['permitted_fields']}]),fc([{'identity':f['authorized_identity'],'sample':dict(f['sample'],run_id='run_second',row_count=8),'permitted':f['permitted_fields']}])])
# Build metadata from the plan and glossary rather than typing anchor or fact fields.
output={'schema_version':P['schema_version'],'kind':'interactions_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for tile in P['tiles']:
 out={'tile_id':tile['tile_id'],'interactions':[]}; seen=set(); count=sum(s['type'] in ['check','hands_on'] for s in tile['steps']); idx=0
 for st in tile['steps']:
  if st['type'] not in ['check','hands_on']:continue
  idx+=1;cid=st['concept_ids'][0];b=bs[cid];n=G['bundles'].index(b); typ=st['planned_interaction_type']
  measures=[{'concept_id':cid,**copy.deepcopy(x)} for x in b['assessment_anchors'] if cid+'#assessment:'+x['capability'] in st['anchors']]
  fact=' '.join(next(f['statement'] for f in b['coverage']['required_facts'] if f['id']==m['fact_ids'][0]) for m in measures[:1])
  ix={'type':typ,'interaction_id':'ix.'+st['step_id'],'difficulty':'intro' if idx==1 else ('stretch' if idx==count else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':copy.deepcopy(st['anchors']),'feedback':{'correct':{'message':fact},'incorrect':{'message':'Recheck the declared boundary and the evidence for each condition. '+fact},'hints':['Identify the required input or result boundary before comparing the alternatives.']}}
  if cid not in seen:
   rem=next((r for r in screens[tile['tile_id']].get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
  seen.add(cid)
  if typ=='choice':
   question,answer,why,wrong=checks[n];opts=[{'option_id':'correct','text':answer}]+[{'option_id':f'wrong{i+1}','text':text} for i,(text,msg) in enumerate(wrong)]
   ix['public']={'prompt':question,'options':opts,'selection':'single','shuffle':True};ix['grading']={'correct_option_ids':['correct'],'option_feedback':{'correct':{'message':why},**{f'wrong{i+1}':{'message':msg} for i,(text,msg) in enumerate(wrong)}}}
  elif typ=='formula_entry':
   task=assets['ds.task_record'];record='; '.join(str(k)+': '+str(v) for k,v in task['rows']);rows=assets['ds.outcome_counts']['rows'];allrow,zone=rows
   ix['public']={'prompt':f'Read the supplied task record: {record}. The same target horizon labels both population rows. For all orders the displayed calculation is {allrow[1]}/{allrow[2]} = {allrow[1]/allrow[2]}. In outcome_counts, header is row 1, all orders row 2 and specified zone row 3; B is target_count, C is population_count and D is horizon_minutes. Enter in E3 a formula dividing the specified-zone target_count by its own population_count; E3 is the outcome proportion for that specified zone at the recorded horizon, not every zone. Use cell references, not a typed proportion.','asset_ref':{'asset_id':'ds.outcome_counts'},'sheet_name':'outcome_counts','target_cell':'E3'}
   ix['grading']={'expected_value':zone[1]/zone[2],'reference_formula':'=B3/C3','forbid_hardcoded_values':True,'tolerance':1e-9}
  elif typ=='classify':
   excerpts=[('named','Named retrieval','client = storage.Client()\nbucket = client.bucket(bucket_name)\nblob = bucket.blob("approved/orders-b.csv")\nblob.download_to_filename(local_path)\nreturn local_path','meets','The named intended object is selected and the downloaded local path is returned.'),('first','First listed object','for blob in client.list_blobs(bucket_name,prefix="approved/"):\n    blob.download_to_filename(local_path)\n    return local_path\n# listing in this fixture starts with approved/orders-a.csv','violates','Selecting the first listed object retrieves orders-a.csv, not the intended orders-b.csv.'),('types','Declared CSV types','declared_types = {"order_key":"string","distance":"float64","zone":"string"}\ntable = pd.read_csv(local_path,dtype=declared_types)\n# observed order_key first value: "0012"; expected columns and row count confirmed','meets','The declared string key preserves the supplied zero-padded representation.'),('numeric_key','Numeric-looking identifier','table = pd.read_csv(local_path,dtype={"order_key":"int64"})\n# first order_key is 12; original field was "0012"','violates','A numeric-looking key is an identifier; this conversion does not preserve its representation.'),('identity','Identity record','with open(identity_path,"w",encoding="utf-8") as f:\n    f.write("object=approved/orders-b.csv; local_path="+local_path)','meets','The local identity record is written through a live UTF-8 file handle.'),('format','Format judgement','Supplied input: orders-b.csv. Read it as declared delimited text. Parquet is columnar and useful for selected-column access; do not relabel this CSV as Parquet.','meets','The explanation distinguishes the supplied format from a columnar access pattern.'),('format_bad','Wrong format judgement','Supplied input: orders-b.csv. Treat these delimited bytes as Parquet simply because training needs selected columns.','violates','A desired access pattern does not change the supplied object format.')]
   ix['public']={'prompt':'Read each independent ingestion excerpt and decide whether it meets or violates the supplied criterion: authorized named retrieval of orders-b.csv and returned local path, preserved declared CSV types and verified observations, an explicit UTF-8 identity-record write, and a format explanation that distinguishes delimited text from selected-column columnar access. Judge only the evidence shown for that excerpt.','buckets':[{'bucket_id':'meets','label':'Meets its stated criterion'},{'bucket_id':'violates','label':'Violates its stated criterion'}],'items':[{'item_id':i,'text':title+'\n```\n'+text+'\n```'} for i,title,text,bucket,msg in excerpts]};ix['grading']={'assignments':{i:bucket for i,title,text,bucket,msg in excerpts},'item_feedback':{i:{'message':msg} for i,title,text,bucket,msg in excerpts}}
  elif typ=='code_exercise':
   cfg=configs[cid];live=b['practice_anchor']['live_code'];starter=cfg['scaffold']+'\n# TODO: write the required function/imports and fixture assertions.\n';solution=cfg['scaffold']+'\n'+cfg['body']
   ix['public']={'prompt':cfg['prompt'],'runtime':{'kind':'python','version':rt['python']['version'],'packages':cfg['packages']},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'asset_mounts':cfg['mounts']},'constraints':{k:copy.deepcopy(live[k]) for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':[{'test_id':f't{i+1}','kind':pr['kind'],'spec':copy.deepcopy(pr['spec']),'visible':True,'message_on_fail':'The result must satisfy the declared fixture contract and preserve the required boundaries.'} for i,pr in enumerate(cfg['probes'])]}
  out['interactions'].append({'step_id':st['step_id'],'interaction':ix})
 output['tiles'].append(out)
(B/'interactions.json').write_text(json.dumps(output,indent=2)+'\n')
print('built',sum(len(t['interactions']) for t in output['tiles']))
