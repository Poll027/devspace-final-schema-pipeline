import json, sys, copy, textwrap
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_mle.region.data_readiness')
plans=json.loads((B/'tile_plans.json').read_text()); screens=json.loads((B/'screens.json').read_text()); registry=json.loads((B/'scenario_asset_registry.json').read_text()); glossary=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
gloss={x['context']['concept_id']:x for x in glossary['bundles']}; assets={x['asset_id']:x for x in registry['assets']}
fixtures={k[3:]:json.loads(next(f['content'] for f in v['files'] if f['path']=='fixtures.json')) for k,v in assets.items() if k.startswith('ws.')}
pin=sandbox.RUNTIMES['python']['version']
# Questions and misconceptions are authored; all fixture values and keys below are copied or executed.
choices={
'prediction_task_definition':('An order is predicted at acceptance. Which input is admissible?', 'Promised delivery zone already known at acceptance.', 'Eventual arrival time recorded after acceptance.', 'Inputs must already be available when the prediction is made; eventual arrival is later information.'),
'numpy_shape_dtype':('A contract requires rank two, two features and one through three orders. Which acceptance procedure respects both axes?', 'Check rank first, then feature-axis width and batch-axis length.', 'Accept whenever the total element count is six.', 'Total element count does not establish rank, feature width or the required batch length.'),
'numpy_dtype_selection':('A candidate saves element bytes but changes a supplied boundary value beyond the declared tolerance. What should the comparison decide?', 'Reject the candidate because preservation and storage requirements must both hold.', 'Accept it because lower nbytes is sufficient.', 'A byte saving does not compensate for a failed value-preservation requirement.'),
'numpy_vectorization':('For a numerical array a and one compatible reference per feature, which expression performs the taught elementwise subtraction?', 'a - feature_references', 'a + feature_references', 'Addition changes values in the opposite direction; the requested transform subtracts the feature references.'),
'file_object_ingestion':('Which procedure writes a local text identity record using the taught file-lifetime rule?', 'Use with open(path, "w", encoding="utf-8") as f and call f.write(text) inside the block.', 'Call f.write(text) only after leaving the with open block.', 'The file handle is managed by the block; the write belongs inside it.'),
'chunked_ingestion':('What does verifying matrix.nbytes against the declared array budget establish?', 'That this materialized chunk fits the element-storage budget.', 'That the entire reader and process fit the same memory budget.', 'Element storage is not a guarantee about total reader or process memory.'),
'dataset_inspection':('Which readiness result is reusable by a caller inspecting another fixture?', 'A dictionary with consistently named inspection fields.', 'A different unnamed output layout for each fixture.', 'Named readiness fields let callers check the same evidence across fixtures; changing the layout defeats that purpose.'),
'dataset_schema_validation':('How should production input validation and fixture checks differ?', 'Raise ValueError for a declared input violation; use assertions to verify expected fixture behavior.', 'Use only assertions as the rejection mechanism for incoming invalid inputs.', 'Assertions check fixture expectations; an explicit validation exception identifies a violated input contract.'),
'dataset_cleaning_policy':('Under a policy that rejects repeats of accepted keys, when is a key added to the accepted-key set?', 'Only after the observation has passed acceptance.', 'Before deciding whether the observation is valid.', 'Recording a rejected observation as accepted can wrongly exclude a later valid observation with the same key.'),
'dataset_selection_bias':('The supplied sample has a lower inclusion probability for zone B. Which conclusion stays within the evidence?', 'Record the coverage limitation without claiming its unobserved cause or inevitable prediction failure.', 'Conclude that every prediction in zone B will fail.', 'A coverage limitation does not establish inevitable prediction failure or an unobserved collection cause.'),
'label_integrity':('A fixture audit expects a valid label at the exact inclusive availability cutoff. How should its boundary assertion behave?', 'It passes when all other supplied validity predicates also hold.', 'It must fail solely because availability equals the cutoff.', 'The declared inclusive boundary permits equality; excluding equality contradicts the fixture predicate.'),
'deployment_matched_splits':('Which check verifies the declared common-group boundary?', 'Assert that training and validation group sets have an empty intersection.', 'Assert only that individual order keys differ between partitions.', 'Different order keys can still belong to the same evaluation group; group sets must be disjoint.'),
'training_fitted_imputation':('A validation transformation leaves outputs plausible but changes statistics_. Which assertion should reject it?', 'Assert that the stored training-fitted statistics are unchanged after transformation.', 'Check only the number of output rows.', 'An output row count does not verify reuse of the training-fitted replacement state.'),
'training_fitted_scaling':('Which assertion checks that validation reused training-fitted scaling?', 'Compare mean_ and scale_ before and after validation transformation.', 'Refit on validation and compare only the resulting shape.', 'Refitting replaces the state that should be preserved; shape alone does not establish state reuse.'),
'categorical_encoding':('Under handle_unknown="ignore", a category absent during fitting produces all-zero indicators. Which fixture assertion matches the declared policy?', 'Assert the all-zero output and unchanged stored category mapping and width.', 'Assert that transformation adds a new indicator column for the unseen category.', 'Transformation must preserve the training mapping and width; ignore does not learn a new indicator.'),
'preprocessing_pipeline':('What should a fixture check establish after validation uses a fitted preprocessing pipeline?', 'Fitted state is unchanged and the declared valid and malformed-input outcomes hold.', 'Only that predict returned without an error for one valid input.', 'One successful call does not verify fitted-state reuse or the declared malformed-input outcome.'),
'prediction_boundary_leakage':('A delivery prediction is made at acceptance. Why must eventual arrival be excluded from its inputs?', 'It becomes available after the prediction boundary.', 'It must be included because it describes the target outcome well.', 'Describing the target does not make later information available at prediction time.'),
'leakage_safe_features':('Which fixture check verifies a feature against later-information leakage?', 'Append a record after prediction_time and assert the earlier feature is unchanged.', 'Append a later record and require the earlier feature to increase.', 'A feature for the earlier boundary must not change when only later observations are added.'),
'sensitive_ml_assets':('Which handling of a literal credential in a generated diagnostic asset follows the taught exposure rule?', 'Remove the literal credential from the generated asset.', 'Keep the literal credential as an ordinary diagnostic field.', 'Literal credentials in generated assets can be exposed; they are not ordinary diagnostic values.')}
solutions={}; prompts={}; calls={}; pkgs={}; scaffolds={}
def code(name, prompt, source, arguments, packages=(), scaffold=''):
 prompts[name]=prompt;solutions[name]=textwrap.dedent(source).strip()+'\n';calls[name]=arguments;pkgs[name]=list(packages);scaffolds[name]=scaffold
f=fixtures['numpy_shape_dtype']
code('numpy_shape_dtype','Implement validate(fixture): convert with np.array, inspect rank/shape/dtype, reject non-rank-two arrays before indexing axes, then reject width other than two or batch length outside one through three with ValueError. Return the accepted array. Define verify(fixture) to return {accepted, array, rank, shape, dtype} for valid inputs and {accepted: False} for ValueError. Write assertions for the supplied list/tuple boundaries and all invalid fixtures; never cast the dtype.', '''
import numpy as np
def validate(fixture):
    a = np.array(fixture)
    rank = a.ndim
    shape = a.shape
    dtype = a.dtype
    rank_ok = rank == 2
    if not rank_ok:
        raise ValueError('rank')
    batch = shape[0]
    features = shape[1]
    dimensions_ok = features == 2 and batch >= 1 and batch <= 3
    if not dimensions_ok:
        raise ValueError('dimensions')
    return a
def verify(fixture):
    try:
        a = validate(fixture)
        return {'accepted': True, 'array': a, 'rank': a.ndim, 'shape': a.shape, 'dtype': a.dtype}
    except ValueError:
        return {'accepted': False}
assert validate(FIXTURES['valid']).shape == (3, 2)
assert validate(((2, 10),)).shape == (1, 2)
assert verify(FIXTURES['empty']) == {'accepted': False}
assert verify(FIXTURES['flat']) == {'accepted': False}
assert verify(FIXTURES['wrong_width']) == {'accepted': False}
assert verify(FIXTURES['too_many']) == {'accepted': False}
''',[[f[k]] for k in ['valid','tuple_boundary','empty','flat','wrong_width','too_many']],['numpy'])
f=fixtures['numpy_dtype_selection']
code('numpy_dtype_selection','Implement compare(reference) for the supplied two-dimensional reference list. Compare float64 and float32 explicitly from the unchanged reference, including each supplied boundary value. Return one entry per dtype with dtype, count, bytes, nbytes, differences (all reference cells followed by boundary cells), accepted, and explanation. Use the exact explanation "element storage, not total object memory" for each entry. Acceptance requires all absolute scalar differences <= supplied tolerance and reference matrix bytes <= supplied budget. Leave the reference unchanged. Work scalar-by-scalar, not with array-wide arithmetic.', '''
import numpy as np
def compare(reference):
    a = np.array(reference)
    boundary = np.array([FIXTURES['boundary_values']])
    result = {}
    for candidate in FIXTURES['candidate_dtypes']:
        b = a.astype(candidate)
        boundary_cast = boundary.astype(candidate)
        differences = []
        preserved = True
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                difference = abs(b[i,j] - a[i,j])
                differences.append(difference)
                if difference > FIXTURES['tolerance']:
                    preserved = False
        for j in range(boundary.shape[1]):
            difference = abs(boundary_cast[0,j] - boundary[0,j])
            differences.append(difference)
            if difference > FIXTURES['tolerance']:
                preserved = False
        byte_count = b.size * b.itemsize
        result[candidate] = {'dtype': candidate, 'count': b.size, 'bytes': byte_count, 'nbytes': b.nbytes, 'differences': differences, 'accepted': preserved and byte_count <= FIXTURES['element_storage_budget'], 'explanation': 'element storage, not total object memory'}
    return result
''',[[f['a']],[[f['a'][0]]]],['numpy'])
f=fixtures['numpy_vectorization']
code('numpy_vectorization','Implement transform(matrix, references). Return np.array(matrix) minus np.array(references), broadcasting one reference per feature. Independently build a nested list-comprehension subtraction reference. Assert the intended shape (number of input rows, two features) and numerical agreement with explicit rtol=1e-7 and atol=1e-9. Return only the resulting array.', '''
import numpy as np
def transform(matrix, references):
    a = np.array(matrix)
    refs = np.array(references)
    result = a - refs
    reference = np.array([[row[0] - references[0], row[1] - references[1]] for row in matrix])
    assert result.shape == a.shape
    np.testing.assert_allclose(result, reference, rtol=1e-7, atol=1e-9)
    return result
''',[[f['matrix'],f['feature_references']],[[f['matrix'][0]],f['feature_references']]],['numpy'])
f=fixtures['chunked_ingestion']
code('chunked_ingestion','Implement inspect_chunks(path, budget). Compute row_limit = budget // (feature_count * element_width) using the supplied fixed-width contract. Keep the UTF-8 input stream open while iterating pd.read_csv with explicit dtype and chunksize. For every matrix, including the final short chunk, assert actual shape-times-itemsize equals nbytes and is <= budget. Return {row_limit, largest_bytes}; largest_bytes is the maximum single-chunk element allocation, not reader/process memory. Do not retain matrices.', '''
import pandas as pd
def inspect_chunks(path, budget):
    row_limit = budget // (FIXTURES['feature_count'] * FIXTURES['element_width'])
    largest_bytes = 0
    with open(path, 'r', encoding='utf-8') as file_handle:
        for chunk in pd.read_csv(file_handle, chunksize=row_limit, dtype=FIXTURES['declared_types']):
            matrix = chunk.to_numpy()
            rows, features = matrix.shape
            element_bytes = rows * features * matrix.dtype.itemsize
            assert element_bytes == matrix.nbytes
            assert element_bytes <= budget
            largest_bytes = max(largest_bytes, element_bytes)
            del matrix
    return {'row_limit': row_limit, 'largest_bytes': largest_bytes}
''',[[f['path'],f['array_budget']],[f['path'],f['array_budget']//2]],['pandas'])
f=fixtures['dataset_inspection']
code('dataset_inspection','Implement inspect(rows, columns). Return named fields columns, shape, dtype, element_bytes, means and std, plus memory_scope equal to "matrix elements, not total process memory". Convert rows to a numeric NumPy array; preserve batch/feature axes and compute means and population standard deviations over rows (axis=0, ddof=0).', '''
import numpy as np
def inspect(rows, columns):
    numeric_values = np.array(rows)
    return {'columns': columns, 'shape': numeric_values.shape, 'dtype': numeric_values.dtype, 'element_bytes': numeric_values.nbytes, 'means': np.mean(numeric_values, axis=0), 'std': np.std(numeric_values, axis=0, ddof=0), 'memory_scope': 'matrix elements, not total process memory'}
''',[[f['fixture']['rows'],f['fixture']['columns']],[f['boundary']['rows'],f['boundary']['columns']]],['numpy'])
f=fixtures['dataset_schema_validation']
# DataFrame creation/copy and probe adaptation are supplied harness, not learner validation.
sc='''import pandas as pd

def supplied_table(case, bad_type=False):
    table = pd.DataFrame(case['rows'], columns=case['columns'])
    for column in table.columns:
        if column in FIXTURES['contract']['declared_types']:
            table[column] = table[column].astype(FIXTURES['contract']['declared_types'][column])
    if bad_type:
        table['distance'] = table['distance'].astype('string')
    return table

def verify(case, bad_type=False):
    table = supplied_table(case, bad_type)
    original = table.copy(deep=True)
    try:
        validate(table)
        verdict = 'accepted'
    except ValueError as error:
        verdict = str(error)
    assert table.equals(original)
    return verdict
'''
code('dataset_schema_validation','Implement validate(table) without changing its input. Require exactly the supplied column set and declared dtypes, inclusive distance bounds, and the two declared zone spellings. Raise ValueError with exactly "columns", "types", "distance" or "zone" for the respective first violation, in that order. The supplied verify harness checks unchanged inputs. Add assertions for valid boundary fixtures and every column/type/value failure.', '''
def validate(table):
    if set(table.columns) != set(FIXTURES['contract']['columns']):
        raise ValueError('columns')
    for column in FIXTURES['contract']['columns']:
        if table.dtypes[column] != FIXTURES['contract']['declared_types'][column]:
            raise ValueError('types')
    if not ((table['distance'] >= FIXTURES['contract']['distance_min']) & (table['distance'] <= FIXTURES['contract']['distance_max'])).all():
        raise ValueError('distance')
    if not ((table['zone'] == 'north') | (table['zone'] == 'south')).all():
        raise ValueError('zone')
    return table
assert verify(FIXTURES['valid']) == 'accepted'
assert verify(FIXTURES['negative']) == 'distance'
assert verify(FIXTURES['too_large']) == 'distance'
assert verify(FIXTURES['missing_column']) == 'columns'
assert verify(FIXTURES['unexpected_column']) == 'columns'
assert verify(FIXTURES['invalid_representation']) == 'zone'
assert verify(FIXTURES['valid'], True) == 'types'
''',[[f[k]] for k in ['valid','negative','too_large','missing_column','unexpected_column','invalid_representation']]+[[f['valid'],True]],['pandas'],sc)
f=fixtures['dataset_cleaning_policy']
code('dataset_cleaning_policy','Implement clean(records). Return {accepted: list of new observation dictionaries, actions: list of {observation_id, action}} in input order. Action labels are retained, repaired, rejected. Reject repeated accepted keys, reject distance outside the supplied inclusive bounds, repair only the approved zone spelling, and add a key only after acceptance. Do not change input records. Write assertions for repairs, boundary values and repeats; use the supplied false-assertion harness to confirm AssertionError.', '''
def clean(records):
    accepted = []
    actions = []
    seen = set()
    for row in records:
        action = 'retained'
        if row['order_key'] in seen:
            action = 'rejected'
        elif row['distance'] < FIXTURES['policy']['distance_min'] or row['distance'] > FIXTURES['policy']['distance_max']:
            action = 'rejected'
        else:
            item = {'observation_id': row['observation_id'], 'order_key': row['order_key'], 'distance': row['distance'], 'zone': row['zone']}
            if row['zone'] in FIXTURES['policy']['zone_repairs']:
                item['zone'] = FIXTURES['policy']['zone_repairs'][row['zone']]
                action = 'repaired'
            accepted.append(item)
            seen.add(row['order_key'])
        actions.append({'observation_id': row['observation_id'], 'action': action})
    return {'accepted': accepted, 'actions': actions}
assert clean(FIXTURES['records'])['accepted'][1]['zone'] == 'south'
assert len(clean(FIXTURES['records'])['accepted']) == 3
assert len(clean(FIXTURES['valid'])['accepted']) == 4
assert clean(FIXTURES['valid'])['accepted'][3]['distance'] == 100
assert supplied_false_assertion()
''',[[f['records']],[f['valid']]],[],'''def supplied_false_assertion():
    try:
        assert False
    except AssertionError:
        return True
''')
f=fixtures['dataset_selection_bias']
# This anchor permits no functions/dictionaries. The exercise uses expressions on mutable starter variables and mounted data instead.
code('dataset_selection_bias','Using supplied sample, target and numeric_values arrays, assign sample_shares, target_shares, inclusion, mean and std (population divisor ddof=0). Assign limitation exactly "zone B has lower inclusion and sample share; cause and prediction failure are not established" when zone B has both lower inclusion and lower sample share, otherwise "comparison changed". Keep denominators distinct; do not infer an unobserved cause.', '''
import numpy as np
sample_shares = sample / np.sum(sample)
target_shares = target / np.sum(target)
inclusion = sample / target
mean = np.mean(numeric_values)
std = np.std(numeric_values, ddof=0)
if inclusion[1] < inclusion[0] and sample_shares[1] < sample_shares[0]:
    limitation = 'zone B has lower inclusion and sample share; cause and prediction failure are not established'
else:
    limitation = 'comparison changed'
''',[],['numpy'],'''import pandas as pd
import numpy as np
counts = pd.read_csv('ds.selection_counts.csv')
sample = counts['sample_count'].to_numpy()
target = counts['target_count'].to_numpy()
numeric_values = np.array(FIXTURES['numeric_values'])
# Supplied reductions provide the denominator only; learner computes the shares.
sample_total = np.sum(sample)
target_total = np.sum(target)
''')
# use supplied reductions so np.sum isn't learner syntax
solutions['dataset_selection_bias']=solutions['dataset_selection_bias'].replace('np.sum(sample)','sample_total').replace('np.sum(target)','target_total')
f=fixtures['label_integrity']
code('label_integrity','Implement audit(observations, labels). Return {duplicates, missing, orphan, invalid, misaligned, unavailable, accepted}. Each issue is a list of affected IDs in encounter order (missing in observation order). Detect duplicates before replacing a dictionary entry. Match by ID, not row order; binary label values, identical observation timestamps, and availability <= the supplied inclusive cutoff are required. accepted is true only if all six issue lists are empty. Assert valid reordered labels, all supplied failure cases and exact cutoff acceptance.', '''
def audit(observations, labels):
    observed = {}
    for row in observations:
        observed[row['observation_id']] = row
    mapped = {}
    duplicates = []
    orphan = []
    invalid = []
    misaligned = []
    unavailable = []
    for row in labels:
        key = row['observation_id']
        if key in mapped:
            duplicates.append(key)
        else:
            mapped[key] = row
        if key not in observed:
            orphan.append(key)
        else:
            if row['observation_timestamp'] != observed[key]['observation_timestamp']:
                misaligned.append(key)
        if row['label'] not in FIXTURES['contract']['label_values']:
            invalid.append(key)
        if row['availability_timestamp'] > FIXTURES['contract']['availability_cutoff']:
            unavailable.append(key)
    missing = []
    for key in observed:
        if key not in mapped:
            missing.append(key)
    return {'duplicates': duplicates, 'missing': missing, 'orphan': orphan, 'invalid': invalid, 'misaligned': misaligned, 'unavailable': unavailable, 'accepted': not duplicates and not missing and not orphan and not invalid and not misaligned and not unavailable}
assert audit(FIXTURES['observations'], FIXTURES['labels'])['accepted']
for case in FIXTURES['cases']:
    assert not audit(FIXTURES['observations'], FIXTURES['cases'][case])['accepted']
''',[[f['observations'],f['labels']]]+[[f['observations'],z] for z in f['cases'].values()])
f=fixtures['deployment_matched_splits']
code('deployment_matched_splits','Implement split(records, scenario). For "group", use supplied training_groups and validation_groups, keeping group sets disjoint; for "time", training timestamps are < cutoff and evaluation is cutoff <= timestamp < evaluation_end. Return {training, validation, training_proportion, validation_proportion}; partitions retain input order and proportions are target counts / partition totals (None for empty). Assert group disjointness and all time inequalities, including equality at cutoff. The supplied false-assertion harness must confirm that a shared-group violation fails.', '''
def split(records, scenario):
    if scenario == 'group':
        training = [row for row in records if row['customer_group'] in FIXTURES['training_groups']]
        validation = [row for row in records if row['customer_group'] in FIXTURES['validation_groups']]
        train_groups = {row['customer_group'] for row in training}
        validation_groups = {row['customer_group'] for row in validation}
        assert not train_groups & validation_groups
    else:
        training = [row for row in records if row['observation_timestamp'] < FIXTURES['cutoff']]
        validation = [row for row in records if FIXTURES['cutoff'] <= row['observation_timestamp'] and row['observation_timestamp'] < FIXTURES['evaluation_end']]
        for row in training:
            assert row['observation_timestamp'] < FIXTURES['cutoff']
        for row in validation:
            assert FIXTURES['cutoff'] <= row['observation_timestamp'] and row['observation_timestamp'] < FIXTURES['evaluation_end']
    training_proportion = None
    validation_proportion = None
    if training:
        training_proportion = sum([row['target'] for row in training]) / len(training)
    if validation:
        validation_proportion = sum([row['target'] for row in validation]) / len(validation)
    return {'training': training, 'validation': validation, 'training_proportion': training_proportion, 'validation_proportion': validation_proportion}
assert supplied_false_assertion()
''',[[f['group_records'],'group'],[f['time_records'],'time']],[],'''def supplied_false_assertion():
    try:
        assert not {'G1'} & {'G1', 'G2'}
    except AssertionError:
        return True
''')
f=fixtures['training_fitted_imputation']
code('training_fitted_imputation','Implement impute(training, validation), using supplied mean strategy and np.nan for JSON missing values (the harness converts them). Fit only training, transform validation and the supplied one-missing boundary. Assert unchanged statistics_ after both transforms. Return {statistics, validation, boundary, observed_mean, observed_std}, summarizing only observed training values with axis=0 and ddof=0. Assert replacement and unchanged observed validation values using the independent supplied mean calculation, and verify the deliberately wrong replacement assertion fails via the harness.', '''
import numpy as np
from sklearn.impute import SimpleImputer
def impute(training, validation):
    X_train = supplied_array(training)
    X_validation = supplied_array(validation)
    imputer = SimpleImputer(strategy=FIXTURES['declared_strategy'])
    imputer.fit(X_train)
    statistics = imputer.statistics_.copy()
    transformed = imputer.transform(X_validation)
    assert np.array_equal(statistics, imputer.statistics_)
    boundary = imputer.transform(np.array([[np.nan]]))
    assert np.array_equal(statistics, imputer.statistics_)
    observed = supplied_observed(training)
    mean = np.mean(observed, axis=0)
    std = np.std(observed, axis=0, ddof=0)
    assert np.allclose(boundary[0], mean)
    assert supplied_replacement_checks(transformed, X_validation, mean)
    assert supplied_wrong_assertion(boundary, FIXTURES['incorrect_replacement'])
    return {'statistics': statistics, 'validation': transformed, 'boundary': boundary, 'observed_mean': mean, 'observed_std': std}
''',[[f['X_train'],f['X_validation']],[f['X_train'],f['boundary_missing']]],['numpy','scikit-learn'],'''import numpy as np
def supplied_array(rows):
    return np.array([[np.nan if value is None else value for value in row] for row in rows])
def supplied_observed(rows):
    return np.array([row for row in rows if row[0] is not None])
def supplied_replacement_checks(transformed, original, mean):
    assert np.allclose(transformed[~np.isnan(original)], original[~np.isnan(original)])
    assert np.allclose(transformed[np.isnan(original)], mean[0])
    return True
def supplied_wrong_assertion(boundary, wrong):
    try:
        assert boundary[0,0] == wrong
    except AssertionError:
        return True
    return False
''')
f=fixtures['training_fitted_scaling']
code('training_fitted_scaling','Implement scale(training, validation). Fit StandardScaler(with_mean=True, with_std=True) only on training, then transform validation. Return {mean, scale, validation, population_std}. Compute population_std over training rows with axis=0, ddof=0. Assert unchanged mean_ and scale_, verify constant feature scale is one, and compare transformed validation with an independent arithmetic calculation. The supplied deliberately wrong-result harness must fail its assertion.', '''
import numpy as np
from sklearn.preprocessing import StandardScaler
def scale(training, validation):
    X_train = np.array(training)
    X_validation = np.array(validation)
    scaler = StandardScaler(with_mean=True, with_std=True)
    scaler.fit(X_train)
    mean = scaler.mean_.copy()
    scale = scaler.scale_.copy()
    transformed = scaler.transform(X_validation)
    assert np.allclose(mean, scaler.mean_)
    assert np.allclose(scale, scaler.scale_)
    assert scale[1] == 1
    assert np.allclose(transformed, (X_validation - mean) / scale)
    assert supplied_wrong_result(transformed)
    return {'mean': mean, 'scale': scale, 'validation': transformed, 'population_std': np.std(X_train, axis=0, ddof=0)}
''',[[f['X_train'],f['X_validation']],[f['X_train'],[f['X_train'][0]]]],['numpy','scikit-learn'],'''import numpy as np
def supplied_wrong_result(actual):
    try:
        assert np.allclose(actual, FIXTURES['incorrect_transformed_fixture'])
    except AssertionError:
        return True
    return False
''')
f=fixtures['categorical_encoding']
code('categorical_encoding','Implement encode(training, cases, policy). Fit OneHotEncoder(handle_unknown=policy, sparse_output=False) on supplied category rows (harness converts JSON missing to np.nan). Return {categories, width, outputs}; outputs is one array or the string "ValueError" per case in input order. Assert categories_ remains unchanged with missing-aware comparison and every successful output keeps fitted width. Verify known indicators by the stored mapping; absent categories, including missing absent during fit, follow error/ignore; missing present during fitting activates its learned indicator. Assert each case against the supplied independent policy predicate.', '''
import numpy as np
from sklearn.preprocessing import OneHotEncoder
def encode(training, cases, policy):
    X_train = supplied_categories(training)
    encoder = OneHotEncoder(handle_unknown=policy, sparse_output=False)
    encoder.fit(X_train)
    categories = encoder.categories_[0].copy()
    width = len(categories)
    outputs = []
    for case in cases:
        try:
            transformed = encoder.transform(supplied_categories(case))
            assert transformed.shape[1] == width
            assert supplied_mapping_matches(categories, encoder.categories_[0])
            assert supplied_policy_matches(categories, case, policy, transformed)
            outputs.append(transformed)
        except ValueError:
            assert supplied_expected_error(categories, case, policy)
            outputs.append('ValueError')
    return {'categories': categories, 'width': width, 'outputs': outputs}
''',[[f['X_train'],list(f['cases'].values()),'ignore'],[f['X_train'],list(f['cases'].values()),'error'],[f['X_train_missing'],list(f['cases'].values()),'ignore']],['numpy','scikit-learn'],'''import numpy as np
def supplied_categories(rows):
    return np.array([[np.nan if v is None else v for v in row] for row in rows], dtype=object)
def supplied_mapping_matches(before, after):
    return all((a == b) or (a != a and b != b) for a,b in zip(before,after)) and len(before) == len(after)
def supplied_known(categories, value):
    return [i for i,c in enumerate(categories) if c == value or (value is None and c != c)]
def supplied_expected_error(categories, case, policy):
    return policy == 'error' and not supplied_known(categories, case[0][0])
def supplied_policy_matches(categories, case, policy, actual):
    expected = np.zeros((1,len(categories)))
    known = supplied_known(categories,case[0][0])
    if known:
        expected[0,known[0]] = 1
    return np.array_equal(expected,actual)
''')
f=fixtures['prediction_boundary_leakage']
sc=next(z['content'] for z in assets['ws.prediction_boundary_leakage']['files'] if z['path']=='authorized_runtime.py')+'''\ndef supplied_select(rows, features):
    return [{key: row[key] for key in features} for row in rows]
def supplied_boundary_assertions(preprocessor, predictor, training, held_out):
    assert preprocessor.fit_rows == training
    assert preprocessor.transform_rows[-1] == held_out
    for row in predictor.input_rows[-1]:
        assert set(row) == set(FIXTURES['permitted_features'])
    return True
def supplied_leaked_fails(training, held_out):
    prep = TracePreprocessor()
    pred = TracePredictor()
    prep.fit(training + held_out)
    pred.predict(prep.transform(held_out))
    try:
        supplied_boundary_assertions(prep, pred, supplied_select(training, FIXTURES['permitted_features']), supplied_select(held_out, FIXTURES['permitted_features']))
    except AssertionError:
        return True
    return False
'''
code('prediction_boundary_leakage','Implement workflow(training, held_out) with the supplied trace interfaces. Select only the permitted decision-time fields for both partitions, fit preprocessing only on selected training rows, transform held-out without refitting and pass only selected fields to the predictor. Use the same supplied boundary assertions on the corrected trace and the leaked workflow; assert the former passes and the latter fails. Return {fit_rows, transformed, predictions}; transformed is the selected held-out rows.', '''
def workflow(training, held_out):
    train_inputs = supplied_select(training, FIXTURES['permitted_features'])
    held_inputs = supplied_select(held_out, FIXTURES['permitted_features'])
    prep = TracePreprocessor()
    predictor = TracePredictor()
    prep.fit(train_inputs)
    transformed = prep.transform(held_inputs)
    predictions = predictor.predict(transformed)
    assert supplied_boundary_assertions(prep, predictor, train_inputs, held_inputs)
    assert supplied_leaked_fails(training, held_out)
    return {'fit_rows': prep.fit_rows, 'transformed': transformed, 'predictions': predictions}
''',[[f['training'],f['held_out']],[f['training'],[f['held_out'][0]]]],[],sc)
f=fixtures['leakage_safe_features']
code('leakage_safe_features','Implement feature(records, prediction_time). The supplied harness converts ISO times to datetime. Accept records with available_at <= prediction_time, iterate accepted records and return their value total. Implement verify(records, prediction_time) to call feature and assert invariance when the supplied later record is appended. Return the total. The tests include the exact-boundary, empty and augmented fixtures.', '''
from datetime import datetime
def feature(records, prediction_time):
    accepted = [row for row in records if row['available_at'] <= prediction_time]
    total = 0
    for record in accepted:
        total += record['value']
    return total
def verify(records, prediction_time):
    records = supplied_dates(records)
    prediction_time = supplied_time(prediction_time)
    actual = feature(records, prediction_time)
    later = supplied_dates([FIXTURES['augmented_records'][-1]])
    expected = feature(records + later, prediction_time)
    assert actual == expected
    return actual
''',[[f['records'],f['prediction_time']],[f['augmented_records'],f['prediction_time']],[f['empty'],f['prediction_time']],[[f['records'][-1]],f['prediction_time']]],[],'''from datetime import datetime
def supplied_dates(rows):
    return [{'available_at': datetime.fromisoformat(row['available_at']), 'value': row['value']} for row in rows]
def supplied_time(value):
    return datetime.fromisoformat(value)
''')
f=fixtures['sensitive_ml_assets']
sc=next(z['content'] for z in assets['ws.sensitive_ml_assets']['files'] if z['path']=='authorized_runtime.py')+'''\nimport io
from contextlib import redirect_stdout
def verify(identity, sample):
    output = io.StringIO()
    try:
        with redirect_stdout(output):
            record = audit(identity,sample)
        assert not output.getvalue()
        assert 'token' not in record and 'raw_customer_values' not in record
        assert use_secret(identity,FIXTURES['runtime_secret_name'])
        return record
    except PermissionError:
        return 'PermissionError'
'''
code('sensitive_ml_assets','Implement audit(identity, sample). Use supplied read_sample to enforce the existing authorization boundary, then construct and return a new dictionary using membership in permitted_fields. Include only permitted keys with their original values. Never print restricted values or retrieve a secret literal. The supplied verify harness captures output, checks restricted-field exclusion, and verifies the authorized secret mechanism still works; unauthorized access must raise PermissionError.', '''
def audit(identity, sample):
    authorized = read_sample(identity, sample)
    record = {}
    for key, value in authorized.items():
        if key in FIXTURES['permitted_fields']:
            record[key] = value
    return record
''',[[f['authorized_identity'],f['sample']],[f['unauthorized_identity'],f['sample']]],[],sc)
function_names={'numpy_shape_dtype':'verify','numpy_dtype_selection':'compare','numpy_vectorization':'transform','chunked_ingestion':'inspect_chunks','dataset_inspection':'inspect','dataset_schema_validation':'verify','dataset_cleaning_policy':'clean','label_integrity':'audit','deployment_matched_splits':'split','training_fitted_imputation':'impute','training_fitted_scaling':'scale','categorical_encoding':'encode','prediction_boundary_leakage':'workflow','leakage_safe_features':'verify','sensitive_ml_assets':'verify'}

def make_code(name, ix):
 f=fixtures[name]
 starter='# Supplied independent fixture data and harness. Implement the task below.\nFIXTURES = '+repr(f)+'\n'+scaffolds[name]+'\n# TODO: write imports, implementation and assertions.\n'
 solution=starter+solutions[name]
 mounts=[]
 ws=assets['ws.'+name]
 for file in ws['files']:
  if file['path'].endswith('.csv') and file['path'].removesuffix('.csv') in assets:
   mounts.append({'asset_id':file['path'].removesuffix('.csv'),'mount_path':file['path']})
 tests=[]
 if name=='dataset_selection_bias':
  expressions=["{'sample_shares': sample_shares, 'target_shares': target_shares, 'inclusion': inclusion, 'limitation': limitation, 'mean': mean, 'std': std, 'counts': sample}"]
  tests=[{'test_id':'result','kind':'value_equals','spec':{'expr':expressions[0]},'message_on_fail':'Recheck each denominator, population divisor and evidence limitation.'}]
 else:
  for i,args in enumerate(calls[name]):
   tests.append({'test_id':'case_'+str(i+1),'kind':'function_call','spec':{'function':function_names[name],'args':args},'message_on_fail':'Recheck the declared fixture contract and boundary assertions.'})
 ix['public']={'prompt':prompts[name], 'runtime':{'kind':'python','version':pin,'packages':pkgs[name]},'workspace':{'entry':'learner.py','files':[{'path':'learner.py','role':'editable','language':'python','content':starter}], 'asset_mounts':mounts},'constraints':{k:copy.deepcopy(gloss['mle.'+name]['practice_anchor']['live_code'][k]) for k in ['allowed_syntax','blocked_syntax']}}
 ix['grading']={'solution_files':[{'path':'learner.py','content':solution}],'tests':tests}
 # Produce expected outputs from the pinned runtime, not authored literals.
 tables,_=sandbox._tables(registry,mounts,{},[])
 probes=[sandbox._py_probe(t) for t in tests]
 script=sandbox._py_script(name,'learner.py',solution,sandbox._py_mounts(tables),probes)
 return ix,script

out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='interactions_part',tiles=[])
jobs=[]
for tile in plans['tiles']:
 entries=[]; seen=set(); screen=next(x for x in screens['tiles'] if x['tile_id']==tile['tile_id'])
 steps=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
 for index,s in enumerate(steps):
  cid=s['concept_ids'][0];name=cid.split('.')[-1];g=gloss[cid]
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1];a=next(a for a in g['assessment_anchors'] if a['capability']==capability)
    measures.append({'concept_id':cid,'capability':capability,'fact_ids':copy.deepcopy(a['fact_ids'])})
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if index==0 else ('stretch' if index==len(steps)-1 else 'core'),'grading_mode':'client','standalone':False,'measures':measures,'anchors':copy.deepcopy(s['anchors']), 'feedback':{'correct':'The response matches the declared contract and its evidence boundary.','incorrect':'Recheck the declared contract and distinguish fixture evidence from assumptions.','hints':['Identify the decision or data boundary before choosing a procedure.']}}
  if cid not in seen:
   rem=next((r for r in screen.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
   seen.add(cid)
  if ix['type']=='choice':
   prompt,right,wrong,why=choices[name]
   ix['standalone']=True
   ix['public']={'prompt':prompt,'options':[{'option_id':'follow_contract','text':right},{'option_id':'misconception','text':wrong}],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':['follow_contract'],'option_feedback':{'follow_contract':{'message':right},'misconception':{'message':why}}}
   ix['feedback']['correct']=right;ix['feedback']['incorrect']=why
   ix['feedback']['hints']=['Separate the stated requirement from what the tempting shortcut actually establishes.']
  elif ix['type']=='code_exercise':
   ix,script=make_code(name,ix);jobs.append((ix,script,name))
  elif ix['type']=='formula_entry':
   record=assets['ds.task_record']['rows']; counts=assets['ds.outcome_counts']['rows']
   # One scalar formula produces the complete labeled task record and both population-specific calculations.
   prefix='; '.join(row[0]+'='+str(row[1]) for row in record)+'; all orders proportion='
   suffix='; specified zone proportion='
   formula='="'+prefix+'"&B2/C2&"'+suffix+'"&B3/C3&"; proportions judge arrival more than 30 minutes after acceptance; specified zone does not represent every zone"'
   ix['public']={'asset_ref':{'asset_id':'ds.outcome_counts'},'sheet_name':'outcomes','target_cell':'E2','prompt':'Enter one formula in E2 that returns a labeled text task record followed by both computed proportions. Use this exact record prefix: '+prefix+' Then append the all-orders target_count/population_count from row 2, the text "'+suffix+'", the specified-zone ratio from row 3, and this exact suffix: "; proportions judge arrival more than 30 minutes after acceptance; specified zone does not represent every zone". The sheet has headers in row 1. Use & for text joining and / for division; do not type the proportions as constants.'}
   # Engine computes the expected scalar below.
   ix['grading']={'reference_formula':formula,'expected_value':None,'forbid_hardcoded_values':True}
   tables,_=sandbox._tables(registry,[{'asset_id':'ds.outcome_counts','mount_path':'outcomes.csv'}],{},[])
   sheet_script=sandbox._sheet_script('formula','E2: '+formula+'\n',tables,[{'id':'value','kind':'cell','ref':'E2'}])
   sheet_result=sandbox.node_run({'scripts':[sheet_script]},sandbox.RUNTIMES['spreadsheet']['runner'])['results']['formula']
   print('sheet',sheet_result)
   ix['grading']['expected_value']=sheet_result['probes']['value']['value']
   ix['feedback']['hints']=['Use the outcome and total counts from the same population row.']
  elif ix['type']=='table_select':
   if name=='file_object_ingestion':
    aid='ds.orders'; rows=assets[aid]['rows']; cols=[c['name'] for c in assets[aid]['columns']]
    tasks=[('identifier','After the authorized named-object retrieval selects approved/orders-b.csv and reads its local CSV with declared string order_key, select the first row\'s order_key cell that verifies leading-zero preservation.','cell'),('numeric','Select the numeric distance column required by the declared CSV conversion.','column'),('schema','Select the eventual_arrival column that must be present in the loaded schema (this task checks ingestion, not prediction-time eligibility).','column')]
    answers=[{'task_id':'identifier','row':{'where':{'order_key':rows[0][0]},'occurrence':0},'column':'order_key','expect_value':rows[0][0]},{'task_id':'numeric','column':'distance'},{'task_id':'schema','column':'eventual_arrival'}]
    intro='Authorized fixture tool simulation: select approved/orders-b.csv by exact object name, download to orders-b.csv, read the complete CSV with declared types, and verify columns and row count. The displayed table is that registered local result. Its order-key string preserves leading zeros. The identity record is written inside with open(path, "w", encoding="utf-8") as f using f.write(text). This supplied complete-file CSV task stays delimited text; a separately declared Parquet task can select columns.'
   else:
    aid='ds.distance_zone'; rows=assets[aid]['rows']
    tasks=[('numeric','Select the training column that receives mean imputation followed by StandardScaler.','column'),('categorical','Select the training column that receives OneHotEncoder(handle_unknown="ignore").','column'),('boundary','Select the distance cell at the declared inclusive upper boundary whose valid-input outcome the fixture assertion must check.','cell')]
    answers=[{'task_id':'numeric','column':'distance'},{'task_id':'categorical','column':'zone'},{'task_id':'boundary','row':{'where':{'distance':max(row[0] for row in rows)},'occurrence':0},'column':'distance','expect_value':max(row[0] for row in rows)}]
    intro='Bounded pipeline tool simulation: the registered table is the supplied training fixture. Compose the numeric and categorical branches with the supplied estimator, fit only training, then reuse transforms on validation and bounded inference without refitting. Compare fitted replacement, scaling and category state before and after reuse; assert unchanged state and the declared malformed-input rejection. Select the branch inputs and valid boundary used by these checks.'
   ix['public']={'asset_ref':{'asset_id':aid},'intro':intro,'tasks':[{'task_id':a,'prompt':b,'target_kind':c} for a,b,c in tasks]};ix['grading']={'answers':answers,'task_feedback':{a:{'correct':'This selection matches the declared field contract.','incorrect':'Distinguish identifier representation, numerical and categorical fields and the declared boundary.'} for a,_,_ in tasks}}
  ix['feedback']['correct']={'message':ix['feedback']['correct']}
  ix['feedback']['incorrect']={'message':ix['feedback']['incorrect']}
  entries.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':entries})

def compute(item):
 ix,script,name=item
 res=sandbox.node_run(sandbox._py_job('python',pkgs[name],[script]),sandbox.RUNTIMES['python']['runner'])['results'][name]
 if not res['ok']:raise RuntimeError(name+': '+res['error'])
 for t in ix['grading']['tests']:
  probe=res['probes'][t['test_id']]
  if not probe['ok']:raise RuntimeError(name+': '+str(probe))
  t['spec']['expected']=probe['value']
 return name
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3) as pool:
  for name in pool.map(compute,jobs): print('computed',name,flush=True)
 (B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
 print('interactions',sum(len(t['interactions']) for t in out['tiles']))
