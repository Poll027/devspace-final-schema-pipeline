import json,sys,copy,textwrap
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in G['bundles']}; assets={x['asset_id']:x for x in R['assets']}
pin=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']['python']['version']
programs={}
def prog(c,setup,body,expr='result',calls=None,mounts=None,extra=None,prompt=''):
 programs[c]=dict(setup=textwrap.dedent(setup).lstrip(),body=textwrap.dedent(body).lstrip(),expr=expr,calls=calls or [],mounts=mounts or [],extra=extra or [],prompt=prompt)
prog('numpy_shape_dtype','''
from fixtures import FIXTURES
fixture = FIXTURES['valid']
boundary = ((2, 10),)
''','''
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
''',calls=[('validate',[assets['ds.order_features']['rows']]),('validate',[[[2,10]]])],prompt='Write the NumPy import and validate(fixture), returning the accepted array. Inspect rank, shape, dtype and boolean decisions locally. Check rank before axes; accept only width two and batches one through three. Assign result for fixture. Author assertions for the list and tuple boundary, empty, flat, wrong-width and too-many fixtures; reject with ValueError, not premature axis access.')
prog('numpy_dtype_selection','''
from fixtures import FIXTURES
import numpy as np
reference = np.array(FIXTURES['a'])
boundaries = np.array([FIXTURES['boundary_values']])
candidates = FIXTURES['candidate_dtypes']
tolerance = FIXTURES['tolerance']
budget = FIXTURES['element_storage_budget']
''','''
def compare(reference, boundaries, candidates, tolerance, budget):
    records = {}
    choice = 'neither'
    for candidate in candidates:
        cast = reference.astype(candidate)
        boundary_cast = boundaries.astype(candidate)
        inspected_dtype = cast.dtype
        calculated = cast.size * cast.itemsize
        preserve = cast.size == reference.size and calculated == cast.nbytes
        differences = []
        for i in range(reference.shape[0]):
            row = []
            for j in range(reference.shape[1]):
                difference = abs(cast[i,j] - reference[i,j])
                row.append(difference)
                if difference > tolerance:
                    preserve = False
            differences.append(row)
        boundary_differences = []
        for j in range(boundaries.shape[1]):
            difference = abs(boundary_cast[0,j] - boundaries[0,j])
            boundary_differences.append(difference)
            if difference > tolerance:
                preserve = False
        accepted = preserve and calculated <= budget
        records[candidate] = {'count':cast.size,'calculated_bytes':calculated,'nbytes':cast.nbytes,'differences':differences,'boundary_differences':boundary_differences,'accepted':accepted}
        if accepted:
            choice = candidate
    return {'candidates':records,'choice':choice,'justification':'Only preserved values within the element-storage budget qualify; element bytes exclude total object and process overhead.'}
result = compare(reference, boundaries, candidates, tolerance, budget)
''',prompt='Implement compare(reference, boundaries, candidates, tolerance, budget). Cast BOTH candidates from the unchanged reference and boundary arrays. Check every scalar difference against tolerance and record count, calculated_bytes, nbytes, differences, boundary_differences and accepted under each candidate. Return candidates, choice (last qualifying candidate, or neither), and the element-storage justification shown by the task contract. Assign result from the supplied inputs. Do not accept byte saving without value preservation.')
# append is not allowed for dtype anchor: scaffold the report accumulation helper, keeping comparison learner-authored
programs['numpy_dtype_selection']['body']=programs['numpy_dtype_selection']['body'].replace('row.append(difference)','row = row + [difference]').replace('differences.append(row)','differences = differences + [row]').replace('boundary_differences.append(difference)','boundary_differences = boundary_differences + [difference]')
prog('numpy_vectorization','''
from fixtures import FIXTURES
matrix = FIXTURES['matrix']
references = FIXTURES['feature_references']
rtol = FIXTURES['rtol']
atol = FIXTURES['atol']
''','''
import numpy as np
def subtract(matrix, references):
    result = np.array(matrix) - np.array(references)
    reference = [[row[0]-references[0], row[1]-references[1]] for row in matrix]
    assert result.shape == np.array(matrix).shape
    np.testing.assert_allclose(result, reference, rtol=rtol, atol=atol)
    return result
result = subtract(matrix, references)
''',calls=[('subtract',[assets['ds.order_features']['rows'],[1,5]]),('subtract',[[[2,10]],[1,5]])],prompt='Write the NumPy import and subtract(matrix, references). Use elementwise array subtraction, independently build a row-wise list-comprehension reference, assert the input matrix shape is preserved, and check agreement with the supplied explicit rtol and atol. Return the array and assign result for the provided fixture.')
prog('chunked_ingestion','''
from fixtures import FIXTURES
path = FIXTURES['path']
declared_types = FIXTURES['declared_types']
array_budget = FIXTURES['array_budget']
feature_count = FIXTURES['feature_count']
element_width = FIXTURES['element_width']
''','''
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
''',mounts=[{'asset_id':'ds.chunked_orders','mount_path':'ds.chunked_orders.csv'}],prompt='Write the pandas import and inspect_chunks(path, declared_types, array_budget, feature_count, element_width). Calculate row_limit by floor division. Keep the file open while iterating read_csv chunks. For each matrix, including the final short chunk, verify shape-derived element bytes equal nbytes and fit the budget, release it, and retain only the maximum. Assign result to that maximum, not total reader or process memory.')
prog('dataset_inspection','''
from fixtures import FIXTURES
columns = FIXTURES['feature_columns']
rows = FIXTURES['fixture']['rows']
ddof = FIXTURES['ddof']
''','''
import numpy as np
def inspect(columns, rows, ddof=0):
    numeric_values = np.array(rows)
    shape = numeric_values.shape
    return {'columns':columns,'column_dtypes':[numeric_values.dtype, numeric_values.dtype], 'means':np.mean(numeric_values,axis=0),'stds':np.std(numeric_values,axis=0,ddof=ddof),'shape':shape,'axes':['observations','features'],'dtype':numeric_values.dtype,'element_bytes':numeric_values.nbytes,'memory_scope':'array elements only, not total process memory'}
result = inspect(columns, rows, ddof)
''',calls=[('inspect',[['distance','feature_2'],assets['ds.order_features']['rows']]),('inspect',[['distance','feature_2'],[[2,10]]])],prompt='Implement inspect(columns, rows, ddof=0) with a NumPy import. Return these named readiness fields: columns, column_dtypes (both selected numerical columns), means, stds (columnwise), shape, axes [observations, features], dtype, element_bytes and memory_scope. Assign result for the supplied inputs. Describe memory_scope as array elements only, not total process memory. Accept the same columns with a one-row fixture too.')
prog('dataset_schema_validation','''
from fixtures import FIXTURES
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
''','''
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
wrong_type = valid.copy()
wrong_type['distance'] = wrong_type['distance'].astype('string')
assert rejected(wrong_type)
''',expr='result',prompt='Implement validate(table, contract) without altering the table. Check exactly the declared columns and dtypes before inclusive distance bounds and lowercase north/south predicates. Raise descriptive ValueError on each violation and return accepted table as result. Author assertions for both endpoints and every supplied failure fixture, including a wrong distance dtype. The provided rejected helper only catches ValueError.')
prog('dataset_cleaning_policy','''
from fixtures import FIXTURES
records = FIXTURES['records']
policy = FIXTURES['policy']
''','''
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
assert len(result['cleaned']) == 3
assert len(result['report']) == 3
boundary = clean(FIXTURES['valid'], policy)
assert boundary['cleaned'][3]['distance'] == policy['distance_max']
''',calls=[('clean',[json.loads(next(f['content'] for f in assets['ws.dataset_cleaning_policy']['files'] if f['path']=='fixtures.json'))['records'],json.loads(next(f['content'] for f in assets['ws.dataset_cleaning_policy']['files'] if f['path']=='fixtures.json'))['policy']]),('clean',[[],json.loads(next(f['content'] for f in assets['ws.dataset_cleaning_policy']['files'] if f['path']=='fixtures.json'))['policy']])],prompt='Implement clean(records, policy), returning cleaned and report. Track only accepted keys; apply policy repeat rejection, inclusive distance bounds, and approved zone repair without mutating inputs. Report each affected observation_id and action. Assign result; author assertions for repairs, rejection, repeats and both boundaries using the records and valid fixtures. A false predicate must fail in ordinary execution.')
prog('dataset_selection_bias','''
from fixtures import FIXTURES
import numpy as np
sample = np.array([FIXTURES['sample_counts']['zone-A'], FIXTURES['sample_counts']['zone-B']])
target = np.array([FIXTURES['target_counts']['zone-A'], FIXTURES['target_counts']['zone-B']])
numeric_values = np.array(FIXTURES['numeric_values'])
''','''
sample_shares = sample / (sample[0]+sample[1])
target_shares = target / (target[0]+target[1])
inclusion = sample / target
mean = np.mean(numeric_values)
std = np.std(numeric_values, ddof=0)
limitation = 'Zone B has lower inclusion and sample share than its target share; the counts establish neither a cause nor inevitable prediction failure.'
result = [sample_shares, target_shares, inclusion, mean, std, limitation]
''',prompt='Using the supplied nonempty category denominators, assign sample_shares, target_shares and inclusion arrays in zone-A, zone-B order. Compute mean and std of numeric_values with ddof=0. Set limitation to the supported lower-inclusion observation for zone B (not a causal or performance claim). Assign result as [sample_shares, target_shares, inclusion, mean, std, limitation].')
prog('label_integrity','''
from fixtures import FIXTURES
observations = FIXTURES['observations']
labels = FIXTURES['labels']
contract = FIXTURES['contract']
''','''
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
    for key in obs_ids:
        if key in label_ids:
            row = keyed[key]
            if row['label'] not in contract['label_values'] or row['observation_timestamp'] != obs[key]['observation_timestamp'] or row['availability_timestamp'] > contract['availability_cutoff']:
                bad.append(key)
    ok = len(repeated_obs) == 0 and len(repeated_labels) == 0 and len(missing) == 0 and len(orphaned) == 0 and len(bad) == 0
    return {'ok':ok,'repeated_observation_ids':repeated_obs,'repeated_label_ids':repeated_labels,'missing':missing,'orphaned':orphaned,'invalid':bad,'matched':keyed}
result = audit(observations, labels, contract)
assert result['ok']
for case in FIXTURES['cases']:
    assert not audit(observations, FIXTURES['cases'][case], contract)['ok']
assert result['matched']['B']['availability_timestamp'] == contract['availability_cutoff']
''',prompt='Implement audit(observations, labels, contract). Check repeated IDs before constructing keyed records, distinguish missing and orphaned sets, and audit label values, matched observation timestamps and inclusive availability cutoff. Return ok, repeated_observation_ids, repeated_label_ids, missing, orphaned, invalid and matched (the first label record for each ID). Assign result; assert reordered acceptance, every supplied failure case and cutoff equality. The task concerns label availability for this audit, not permission to use later labels as prediction inputs.')
prog('deployment_matched_splits','''
from fixtures import FIXTURES
records = FIXTURES['group_records']
training_groups = FIXTURES['training_groups']
validation_groups = FIXTURES['validation_groups']
''','''
def group_split(records, training_groups, validation_groups):
    train = [row for row in records if row['customer_group'] in training_groups]
    validation = [row for row in records if row['customer_group'] in validation_groups]
    train_groups = {row['customer_group'] for row in train}
    val_groups = {row['customer_group'] for row in validation}
    assert not (train_groups & val_groups)
    train_share = sum([row['target'] for row in train]) / len(train)
    val_share = sum([row['target'] for row in validation]) / len(validation)
    return {'training':train,'validation':validation,'training_proportion':train_share,'validation_proportion':val_share}
def time_split(records, cutoff, end):
    train = [row for row in records if row['observation_timestamp'] < cutoff]
    validation = [row for row in records if cutoff <= row['observation_timestamp'] and row['observation_timestamp'] < end]
    assert max([row['observation_timestamp'] for row in train]) < cutoff
    assert min([row['observation_timestamp'] for row in validation]) >= cutoff
    return {'training':train,'validation':validation,'training_proportion':sum([row['target'] for row in train])/len(train),'validation_proportion':sum([row['target'] for row in validation])/len(validation)}
result = group_split(records, training_groups, validation_groups)
assert result['training'][0]['customer_group'] == 'G1'
time_result = time_split(FIXTURES['time_records'], FIXTURES['cutoff'], FIXTURES['evaluation_end'])
assert time_result['validation'][0]['observation_timestamp'] == FIXTURES['cutoff']
''',expr='[result,time_result]',prompt='Write group_split and time_split. For groups, assign only supplied memberships and assert no shared group. For time, use training < cutoff and evaluation cutoff <= timestamp < evaluation_end. Return training, validation, training_proportion and validation_proportion from each function; each nonempty share is target count / row count. Assign result for the group fixture and time_result for the time fixture. Author assertions for group isolation and cutoff equality. These boundaries represent unseen groups and later orders, respectively; random splitting would not preserve them.')
prog('training_fitted_imputation','''
from fixtures import FIXTURES
import numpy as np
X_train = np.array(FIXTURES['X_train'], dtype=float)
X_validation = np.array(FIXTURES['X_validation'], dtype=float)
numeric_values = np.array(FIXTURES['numeric_values'])
boundary = np.array(FIXTURES['boundary_missing'], dtype=float)
strategy = FIXTURES['declared_strategy']
''','''
from sklearn.impute import SimpleImputer
def impute(X_train, X_validation, numeric_values, boundary, strategy):
    imputer = SimpleImputer(strategy=strategy)
    imputer.fit(X_train)
    before = imputer.statistics_.copy()
    validation = imputer.transform(X_validation)
    boundary_result = imputer.transform(boundary)
    assert np.array_equal(before, imputer.statistics_)
    mean = np.mean(numeric_values,axis=0)
    std = np.std(numeric_values,axis=0,ddof=0)
    assert np.allclose(boundary_result[0], mean)
    return [mean,std,validation,boundary_result,imputer.statistics_]
result = impute(X_train,X_validation,numeric_values,boundary,strategy)
assert result[2][0][0] == X_validation[0][0]
assert np.allclose(result[2][1],result[0])
assert not np.allclose(result[2][1],FIXTURES['incorrect_replacement'])
''',prompt='Write the SimpleImputer import and impute(X_train, X_validation, numeric_values, boundary, strategy). Fit once on training only; transform validation and the single-missing boundary without refitting. Compute observed training columnwise mean/std with ddof=0, assert statistics_ stays unchanged and the boundary matches mean. Return [mean, std, validation, boundary_result, statistics_], assign result and assert observed validation preservation and rejection of the supplied incorrect replacement.')
prog('training_fitted_scaling','''
from fixtures import FIXTURES
import numpy as np
X_train = np.array(FIXTURES['X_train'])
X_validation = np.array(FIXTURES['X_validation'])
''','''
from sklearn.preprocessing import StandardScaler
def scale(X_train,X_validation):
    mean = np.mean(X_train,axis=0)
    std = np.std(X_train,axis=0,ddof=0)
    scaler = StandardScaler(with_mean=True,with_std=True)
    scaler.fit(X_train)
    before_mean = scaler.mean_.copy()
    before_scale = scaler.scale_.copy()
    validation = scaler.transform(X_validation)
    assert np.allclose(scaler.mean_,before_mean)
    assert np.allclose(scaler.scale_,before_scale)
    assert scaler.scale_[1] == 1
    assert np.allclose(validation[0][0],(X_validation[0][0]-mean[0])/std[0])
    return [mean,std,validation,scaler.mean_,scaler.scale_]
result = scale(X_train,X_validation)
assert not np.allclose(result[2],FIXTURES['incorrect_transformed_fixture'])
''',prompt='Implement scale(X_train, X_validation), writing the StandardScaler import. Compute training columnwise mean/std with ddof=0, fit once and transform validation. Assert unchanged mean_/scale_, constant-feature scale 1, and the distance transformation formula. Return [mean, std, validation, mean_, scale_] as result; reject the supplied incorrect result with an assertion.')
prog('categorical_encoding','''
from fixtures import FIXTURES
import numpy as np
X_train = FIXTURES['X_train']
X_train_missing = [['north'],['south'],[np.nan]]
cases = {'known':[['north']], 'unseen':[['east']], 'missing':[[np.nan]]}
# The driver catches the declared unknown-category exception only.
def attempt(encoder, rows):
    try:
        return encoder.transform(rows)
    except ValueError:
        return 'ValueError'
''','''
from sklearn.preprocessing import OneHotEncoder
def encode(X_train,X_train_missing,cases):
    encoder = OneHotEncoder(handle_unknown='ignore',sparse_output=False)
    encoder.fit(X_train)
    before = encoder.categories_[0].copy()
    mapping = {'zone':encoder.categories_[0].tolist()}
    known = encoder.transform(cases['known'])
    unseen = encoder.transform(cases['unseen'])
    missing = encoder.transform(cases['missing'])
    assert np.array_equal(before,encoder.categories_[0])
    assert known.shape[1] == len(mapping['zone'])
    assert np.all(unseen == 0)
    assert np.all(missing == 0)
    error_encoder = OneHotEncoder(handle_unknown='error',sparse_output=False)
    error_encoder.fit(X_train)
    assert attempt(error_encoder,cases['unseen']) == 'ValueError'
    assert attempt(error_encoder,cases['missing']) == 'ValueError'
    missing_encoder = OneHotEncoder(handle_unknown='error',sparse_output=False)
    missing_encoder.fit(X_train_missing)
    learned_missing = missing_encoder.transform(cases['missing'])
    assert learned_missing[0][2] == 1
    return [mapping,known,unseen,missing,learned_missing]
result = encode(X_train,X_train_missing,cases)
''',prompt='Implement encode(X_train, X_train_missing, cases) with OneHotEncoder. Build mapping under zone from fitted categories_. Check known, unseen and absent-at-fit missing cases under ignore; assert output width and categories remain unchanged. Also fit an error-policy encoder and assert supplied attempt returns ValueError for unseen and absent missing. Fit missing-present training and assert missing activates its learned indicator. Return [mapping, known, unseen, missing, learned_missing] as result.')
prog('prediction_boundary_leakage','''
from fixtures import FIXTURES
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
''','''
def correct(training,held_out,features):
    X_train = training[features]
    X_held = held_out[features]
    preprocessing = workflow()
    train_result = preprocessing.fit_transform(X_train)
    before = preprocessing.named_transformers_['numeric'].mean_.copy()
    held_result = preprocessing.transform(X_held)
    verify(X_train.columns,X_held.columns,training['order_key'],training['order_key'])
    assert (preprocessing.named_transformers_['numeric'].mean_ == before).all()
    return [train_result,held_result,before]
result = correct(training,held_out,features)
''',prompt='Correct the acceptance-time workflow in correct(training, held_out, features). Select only the supplied distance and zone fields on each side, fit_transform training only and transform held-out without refitting. Invoke verify for input columns and fit-row IDs; assert fitted numeric state is unchanged. Return [training_representation, held_out_representation, training_mean] as result. Use the same boundary assertions on the future-field and combined-fit-row failure fixtures: they must fail before correction and pass for this corrected workflow.')
prog('leakage_safe_features','''
from fixtures import FIXTURES
from datetime import datetime
records = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in FIXTURES['records']]
augmented = [{'available_at':datetime.fromisoformat(r['available_at']), 'value':r['value']} for r in FIXTURES['augmented_records']]
prediction_time = datetime.fromisoformat(FIXTURES['prediction_time'])
''','''
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
''',prompt='Implement feature(records, prediction_time). Select available_at <= prediction_time with a list comprehension, initialize total and accumulate only accepted value entries. Return total and assign result. Author assertions for the added-later record, empty input and exact-boundary inclusion; use the supplied datetime fixtures, never a latest lookup without a boundary.')
prog('sensitive_ml_assets','''
from fixtures import FIXTURES
from authorized_runtime import read_sample, use_secret
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
''','''
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
''',calls=[('audit',[json.loads(next(f['content'] for f in assets['ws.sensitive_ml_assets']['files'] if f['path']=='fixtures.json'))['sample'],['run_id','row_count'],'fixture_reader']),('audit',[{'run_id':'run_other','row_count':2,'token':'DUMMY'},['run_id','row_count'],'fixture_reader'])],prompt='Implement audit(sample, permitted, identity). Read only through supplied read_sample (unauthorized identity raises PermissionError); construct a NEW permitted-field dictionary using membership checks. Assign result. Assert only original run_id/row_count remain, both restricted fields are absent, unauthorized access is denied, and use_secret succeeds without returning or printing a credential. Do not print any sample or secret.')
# Fixtures are supplied in readonly files. Additional assertions are tests of learner logic, never an implementation hidden in a helper.
choices={
'prediction_task_definition':('An estimate is made at order acceptance. Which candidate must be excluded from its inputs?','Eventual arrival time','Promised delivery zone','Distance','Eventual arrival is known afterward; distance and promised zone are available at acceptance.'),
'numpy_shape_dtype':('A model boundary accepts one through three orders, with two features per order. Which input passes both checks?','Rank two, shape (3, 2)','Rank one, shape (6,)','Rank two, shape (4, 2)','Rank one lacks the two-axis contract; four orders exceed the batch limit.'),
'numpy_dtype_selection':('A lower-width cast saves bytes but one scalar difference exceeds the declared tolerance. What is the defensible decision?','Reject it despite the byte saving','Accept it because nbytes is smaller','Accept it because shape is unchanged','Storage saving and unchanged shape do not establish value preservation.'),
'numpy_vectorization':('For elementwise subtraction of a feature reference from each observation, which approach applies NumPy arithmetic to the array?','Subtract the reference array from the observation array','Call a Python scalar subtraction separately for each observation','Declare that array arithmetic is impossible without a Python loop','Array arithmetic supports elementwise operations; a per-observation Python loop is not the requested vectorized expression.'),
'file_object_ingestion':('Which snippet correctly writes a local text identity record with an explicit UTF-8 handle?','with open(path, "w", encoding="utf-8") as f: f.write(text)','with open(path, "r", encoding="utf-8") as f: f.write(text)','with open(path, "w", encoding="utf-8") as f: text = f.read()','Reading mode is not the declared writing operation; reading from a write-only handle does not write the record.'),
'chunked_ingestion':('Which approach supports the declared single-chunk numerical-array budget?','Iterate chunks while the file is open, check each matrix and release prior matrices','Read once, then retain every materialized chunk in a list','Use a row-limit estimate and skip all actual nbytes checks','Retaining chunks defeats bounded working matrices, and an estimate does not replace checking each allocation.'),
'dataset_inspection':('Which readiness evidence retains the structure needed to interpret model input?','Column names and dtypes plus shape with observation/feature axis meanings','Only the total element count','Only the matrix nbytes','Neither element count nor element bytes identifies columns and axis meanings.'),
'dataset_schema_validation':('A required input boundary fails. Which action implements validation rather than a fixture-only assertion?','Conditionally raise a descriptive ValueError','Continue with the invalid input','Use only assert and call that the production rejection boundary','A conditional exception enforces input rejection; continuing accepts invalid data and assert is a fixture predicate that can be disabled by optimization.'),
'dataset_cleaning_policy':('In ordinary non-optimized execution, what happens to a deliberately false cleaning-policy assertion?','It raises AssertionError','It silently repairs the data','It changes the declared policy to retain the row','Assertions verify predicates; they neither repair data nor rewrite policy.'),
'dataset_selection_bias':('To estimate inclusion within a category whose target members are known, which denominator is needed?','All target members in that category','The total sample across all categories','The included members in that category','A category-specific inclusion rate divides included category members by target category members, not all sampled rows or the numerator itself.'),
'label_integrity':('A deliberately false label-integrity predicate is asserted in ordinary non-optimized execution. What follows?','AssertionError','The label is automatically realigned','The duplicated ID is automatically removed','An assertion verifies a predicate; it does not align or remove records.'),
'deployment_matched_splits':('Evaluation represents unseen customer groups. Which boundary meets that scenario?','Every observation in one group remains entirely on one side','Split each group between training and validation','Ignore groups and justify the split solely as random','Splitting a common group across sides violates the declared group boundary; randomness alone does not match this scenario.'),
 'training_fitted_imputation':('After fitting a mean imputer on training distances, what should validation receive?','Transform with the existing imputer and verify statistics_ unchanged','Fit a new imputer on validation','Combine training and validation before fitting','Validation must reuse training statistics; either refitting or fitting combined data changes the information boundary.'),
 'training_fitted_scaling':('How should a validation input be standardized?','Use the scaler fitted only on training and inspect unchanged mean_/scale_','Fit a validation-only scaler','Leave validation raw while training is scaled','Refitting changes the parameters, while raw validation omits the transformations used for training.'),
 'categorical_encoding':('An unseen zone was absent at fit. Which explicit OneHotEncoder policy yields all-zero indicators for that feature?','handle_unknown="ignore"','handle_unknown="error"','Refit the encoder on validation','Error rejects the unknown category; validation refitting changes the learned mapping rather than applying it.'),
 'preprocessing_pipeline':('Which workflow preserves a composed pipeline for validation?','Fit the composed workflow on training, then call its predict on validation','Fit each validation batch before predicting','Bypass fitted transformations and send raw validation to the estimator','Validation must reuse the fitted transformations; refitting or bypassing them does not preserve the training workflow.'),
 'prediction_boundary_leakage':('For an acceptance-time task, which change removes both supplied information-boundary defects?','Exclude eventual arrival from inputs and fit preprocessing on training only','Exclude eventual arrival but fit on combined training and held-out rows','Fit on training only but keep eventual arrival as an input','Each alternative leaves one defect: held-out fit rows or a future input.'),
 'leakage_safe_features':('What property should a feature for an earlier prediction satisfy when a later unavailable record is added?','The earlier feature remains unchanged','The earlier feature must include the new value','The boundary record must always be excluded','Only decision-available records contribute; a later record is excluded, while equality at the stated inclusive boundary is allowed.'),
 'sensitive_ml_assets':('Which handling respects the supplied authorization and permitted-field policy?','Keep credentials in the authorized runtime mechanism and return only permitted fields','Copy the runtime credential into the audit record','Treat possession of a log file as authorization','Copying credentials discloses them; possession is not authenticated authorization.'),
}
# Exact anchor testing uses glossary facts, not qualified screen lineage IDs.
out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for tile in P['tiles']:
 st=next(x for x in S['tiles'] if x['tile_id']==tile['tile_id']); rows=[];seen=set()
 interactions=[s for s in tile['steps'] if s['type'] in ['check','hands_on']]
 for idx,s in enumerate(interactions):
  cid=s['concept_ids'][0]; short=cid.split('.',1)[1]; bundle=bundles[cid]
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    concept,cap=anchor.split('#assessment:'); ab=next(a for a in bundles[concept]['assessment_anchors'] if a['capability']==cap)
    measures.append({'concept_id':concept,'capability':cap,'fact_ids':ab['fact_ids']})
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if idx==0 else ('stretch' if idx==len(interactions)-1 else 'core'),'grading_mode':'client','standalone':False,'measures':measures,'anchors':[a for a in s['anchors'] if a.endswith('#practice')]}
  ix['feedback']={'correct':'You applied the declared boundary and its required checks.','incorrect':'Recheck the declared contract and the evidence for each decision.','hints':['Separate the policy requirement from the fixture observation.','Check the boundary cases as well as the ordinary case.']}
  if cid not in seen:
   rem=next((x for x in st.get('remediation_steps',[]) if cid in x['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
   seen.add(cid)
  if ix['type']=='choice':
   q,a,b,c,why=choices[short]
   ix['standalone']=True;ix['public']={'prompt':q,'selection':'single','shuffle':True,'options':[{'option_id':str(i),'text':v} for i,v in enumerate([a,b,c])]};ix['grading']={'correct_option_ids':['0'],'option_feedback':{str(i):{'message':('Correct. '+why) if i==0 else why} for i in range(3)}}
  elif ix['type']=='code_exercise':
   d=programs[short]; w=assets['ws.'+short]; readonly=[{'path':'fixtures.py','role':'readonly','language':'python','content':next(f['content'] for f in w['files'] if f['path']=='fixtures.py')}]+d['extra']
   if short=='sensitive_ml_assets':readonly.append({'path':'authorized_runtime.py','role':'readonly','language':'python','content':next(f['content'] for f in w['files'] if f['path']=='authorized_runtime.py')})
   starter=d['setup']+'\n# TODO: write your implementation and assertions below.\n';solution=d['setup']+'\n'+d['body']
   packages=['numpy'] if 'numpy' in solution else []
   if 'pandas' in solution:packages.append('pandas')
   if 'sklearn' in solution:packages.append('scipy')
   ix['public']={'prompt':d['prompt'],'runtime':{'kind':'python','version':pin,'packages':packages},'workspace':{'files':[{'path':'learner.py','role':'editable','language':'python','content':starter}]+readonly,'entry':'learner.py','asset_mounts':d['mounts']},'constraints':copy.deepcopy({k:bundle['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']})}
   tests=[{'test_id':'result','kind':'value_equals','spec':{'expr':d['expr'],'expected':None},'visible':True,'message_on_fail':'The named result does not meet the declared contract.'}]
   for i,(fn,args) in enumerate(d['calls']):tests.append({'test_id':'call'+str(i),'kind':'function_call','spec':{'function':fn,'args':args,'expected':None},'visible':False,'message_on_fail':'The parameterized function fails a supplied boundary fixture.'})
   ix['grading']={'solution_files':[{'path':'learner.py','content':solution}],'tests':tests}
  else:
   ix['public']={'prompt':'','buckets':[{'bucket_id':'meets','label':'Meets declared criterion'},{'bucket_id':'violates','label':'Violates declared criterion'}],'items':[]};ix['grading']={'assignments':{},'item_feedback':{}}
  rows.append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append({'tile_id':tile['tile_id'],'interactions':rows})
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('Authored',sum(len(t['interactions']) for t in out['tiles']),'interactions')
