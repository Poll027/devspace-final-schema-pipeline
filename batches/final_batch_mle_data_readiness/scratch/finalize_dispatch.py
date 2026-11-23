import json,copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness');D=json.loads((B/'interactions.json').read_text());R=json.loads((B/'scenario_asset_registry.json').read_text());A={a['asset_id']:a for a in R['assets']}
xs={i['interaction']['anchors'][0].split('#')[0].split('.',1)[1]:i['interaction'] for t in D['tiles'] for i in t['interactions'] if i['interaction'].get('anchors')}
def source_f(short):return json.loads(next(f['content'] for f in A['ws.'+short]['files'] if f['path']=='fixtures.json'))
def append_setup(ix,text):
 ix['public']['workspace']['files'][0]['content']=ix['public']['workspace']['files'][0]['content'].replace('# TODO:',text+'\n# TODO:')
 code=ix['grading']['solution_files'][0]['content'];marker='\n\n';pos=code.index(marker);ix['grading']['solution_files'][0]['content']=code[:pos]+ '\n'+text+code[pos:]
def readonly(ix,name,text):ix['public']['workspace']['files'].append({'path':name,'role':'readonly','language':'python','content':text})
def replace_tests(ix,fn,args_list):
 ix['grading']['tests']=[{'test_id':'case'+str(i),'kind':'function_call','spec':{'function':fn,'args':args,'expected':None},'visible':i==0,'message_on_fail':'This fixture does not satisfy the declared return contract.'} for i,args in enumerate(args_list)]
def calls(ix,fn,args):
 ix['grading']['tests']=[t for t in ix['grading']['tests'] if t['kind']=='function_call']
 if not ix['grading']['tests']:replace_tests(ix,fn,args)
# Test parameterized skill directly with distinct input fixtures; expected values will come only from a pinned-engine execution.
for short in ['numpy_shape_dtype','numpy_vectorization','dataset_inspection','dataset_cleaning_policy','sensitive_ml_assets']:
 ix=xs[short];ix['grading']['tests']=[t for t in ix['grading']['tests'] if t['kind']=='function_call']
ix=xs['numpy_dtype_selection']; f=source_f('numpy_dtype_selection');code=ix['grading']['solution_files'][0]['content']
code=code.replace('budget = FIXTURES[\'element_storage_budget\']','budget = '+repr(f['element_storage_budget']))
code=code.replace('differences = []','differences = {}').replace('row = []','row = {}').replace('row = row + [difference]','row[j] = difference').replace('differences = differences + [row]','differences[i] = row').replace('boundary_differences = {}','boundary_differences = {}').replace('boundary_differences = boundary_differences + [difference]','boundary_differences[j] = difference')
# use scalar reference value after cast to avoid NumPy scalar subtraction selecting the lower dtype
ix['grading']['solution_files'][0]['content']=code
ix['public']['workspace']['files'][0]['content']=ix['public']['workspace']['files'][0]['content'].replace('budget = FIXTURES[\'element_storage_budget\']','budget = '+repr(f['element_storage_budget']))
ix['public']['prompt']+=' Report differences as row/column-index dictionaries and boundary_differences by column index; justification must state: Only preserved values within the element-storage budget qualify; element bytes exclude total object and process overhead.'
ix=xs['dataset_selection_bias'];f=source_f('dataset_selection_bias'); append_setup(ix,'sample_A = '+repr(f['sample_counts']['zone-A'])+'\nsample[0] = sample_A')
# Schema validation call driver constructs declared fixture types; not a completed validator.
ix=xs['dataset_schema_validation'];
append_setup(ix,"def validate_fixture(case):\n    return validate(make(case), contract)")
f=source_f('dataset_schema_validation');replace_tests(ix,'validate_fixture',[[f['valid']],[{'columns':f['valid']['columns'],'rows':[f['valid']['rows'][1]]}]])
# Ensure no untaught copy/astype method is learner-authored: wrong-type input construction belongs to provided fixture scaffolding.
append_setup(ix,"wrong_type = valid.copy()\nwrong_type['distance'] = wrong_type['distance'].astype('string')")
code=ix['grading']['solution_files'][0]['content'];last=code.rfind("wrong_type = valid.copy()")
code=code[:last]+code[last:].replace("wrong_type = valid.copy()\nwrong_type['distance'] = wrong_type['distance'].astype('string')\n",'',1);ix['grading']['solution_files'][0]['content']=code
ix=xs['label_integrity'];f=source_f('label_integrity');replace_tests(ix,'audit',[[f['observations'],f['labels'],f['contract']]]+[[f['observations'],v,f['contract']] for v in f['cases'].values()])
# group/time boundary functions each tested on two distinct, nonempty partitions
ix=xs['deployment_matched_splits'];f=source_f('deployment_matched_splits');
code=ix['grading']['solution_files'][0]['content'];code=code.replace("FIXTURES['evaluation_end']","FIXTURES['evaluation_end_exclusive']") if 'evaluation_end_exclusive' in f else code
ix['grading']['solution_files'][0]['content']=code
endkey=next(k for k in f if 'end' in k);print('time keys',list(f),endkey)
replace_tests(ix,'group_split',[[f['group_records'],f['training_groups'],f['validation_groups']],[f['group_records']+[dict(f['group_records'][0],order_key='A_add')],f['training_groups'],f['validation_groups']]])
ix['grading']['tests'] += [{'test_id':'time'+str(i),'kind':'function_call','spec':{'function':'time_split','args':[rows,f['cutoff'],f[endkey]],'expected':None},'visible':False,'message_on_fail':'The time cutoff, later interval or partition shares are incorrect.'} for i,rows in enumerate([f['time_records'],f['time_records']+[dict(f['time_records'][0],order_key='T_add')]])]
# For library functions, a provided conversion driver accepts arbitrary JSON fixtures.
for short,fn,argnames in [('training_fitted_imputation','impute',['X_train','X_validation','numeric_values','boundary_missing','declared_strategy']),('training_fitted_scaling','scale',['X_train','X_validation']),('categorical_encoding','encode',['X_train','X_train_missing','cases'])]:
 ix=xs[short];f=source_f(short)
 if short=='training_fitted_imputation':
  driver="def evaluate(case):\n    return impute(np.array(case['X_train'],dtype=float),np.array(case['X_validation'],dtype=float),np.array(case['numeric_values']),np.array(case['boundary_missing'],dtype=float),case['declared_strategy'])\n"
  second=copy.deepcopy(f);second['X_validation']=[[200],[None]]
 elif short=='training_fitted_scaling':
  driver="def evaluate(case):\n    return scale(np.array(case['X_train']),np.array(case['X_validation']))\n"
  second=copy.deepcopy(f);second['X_validation']=[[10,10]]
 else:
  driver="def evaluate(case):\n    missing_train = [[np.nan if row[0] is None else row[0]] for row in case['X_train_missing']]\n    test_cases = {'known':case['cases']['north'],'unseen':case['cases']['east'],'missing':[[np.nan]]}\n    return encode(case['X_train'],missing_train,test_cases)\n"
  second=copy.deepcopy(f);second['cases']['north']=[['south']]
 append_setup(ix,driver)
 replace_tests(ix,'evaluate',[[f],[second]])
 # scikit-learn is the pinned runtime dependency actually imported by these practices.
 ix['public']['runtime']['packages'].append('scikit-learn')
# Boundary audit tests verify leaked fixture rejection without widening allowed syntax.
ix=xs['prediction_boundary_leakage'];f=source_f('prediction_boundary_leakage')
append_setup(ix,"from sklearn import preprocessing\nimport numpy as np\ndef evaluate(case):\n    return correct(pd.DataFrame(case['training']), pd.DataFrame(case['held_out']), case['permitted_features'])\n# The same verification predicate is applied to both declared leaked boundaries.\ndef rejected_boundary(train_columns, held_columns, keys, expected):\n    try:\n        verify(train_columns, held_columns, keys, expected)\n    except AssertionError:\n        return True\n    return False")
code=ix['grading']['solution_files'][0]['content'];code=code.replace("assert (preprocessing.named_transformers_['numeric'].mean_ == before).all()","assert np.array_equal(preprocessing.named_transformers_['numeric'].mean_, before)")
code += "\nassert rejected_boundary(FIXTURES['failure_features'], features, training['order_key'], training['order_key'])\nassert rejected_boundary(features, features, [row['order_key'] for row in FIXTURES['failure_fit_rows']], training['order_key'])\n"
# list-comprehension of failure-fit keys is scaffolding; learners assert only the supplied rejected predicate
code=code.replace("[row['order_key'] for row in FIXTURES['failure_fit_rows']]","failure_fit_keys")
ix['grading']['solution_files'][0]['content']=code
append_setup(ix,"failure_fit_keys = [row['order_key'] for row in FIXTURES['failure_fit_rows']]")
second=copy.deepcopy(f);second['held_out'][0]['distance']=8
replace_tests(ix,'evaluate',[[f],[second]])
ix['public']['runtime']['packages']+=['scikit-learn']
# Feature wrapper supplies documented datetime conversion, while the learner owns boundary selection/summation.
ix=xs['leakage_safe_features'];f=source_f('leakage_safe_features')
append_setup(ix,"def evaluate(case):\n    rs = [{'available_at':datetime.fromisoformat(r['available_at']),'value':r['value']} for r in case['records']]\n    return feature(rs,datetime.fromisoformat(case['prediction_time']))")
second=copy.deepcopy(f);second['records'][0]['value']=4
replace_tests(ix,'evaluate',[[f],[second]])
# Realistic, inline inspect-and-judge tasks; no invented registry references.
def judge(short,prompt,items):
 ix=xs[short];ix['public']['prompt']=prompt
 ix['public']['items']=[{'item_id':'j'+str(i),'text':text} for i,(text,ok,why) in enumerate(items)]
 ix['grading']['assignments']={'j'+str(i):'meets' if ok else 'violates' for i,(text,ok,why) in enumerate(items)}
 ix['grading']['item_feedback']={'j'+str(i):{'message':why} for i,(text,ok,why) in enumerate(items)}
 ix['feedback']['correct']='You judged each supplied implementation against its named criterion.'
 ix['feedback']['incorrect']='Find the exact operation or field that meets or violates the declared criterion.'
records=A['ds.task_record']['rows'];record='\n'.join(k+': '+v for k,v in records)
counts=A['ds.outcome_counts']['rows'];calcs='\n'.join(f'{r[0]}: {r[1]}/{r[2]} = {r[1]/r[2]:.2f}; target horizon {r[3]} minutes' for r in counts)
judge('prediction_task_definition','Read each candidate task-record excerpt and decide whether it meets the order-at-acceptance task criterion. Judge its fields, input boundary and population-labeled calculations, not how you would implement a sheet.',[(record+'\n'+calcs+'\nInterpretation: these counts measure the specified order-level target; the zone proportion is not a claim about every zone.',True,'The record separates unit, population, target, time and horizon, excludes future arrival, and labels the two denominators.'),(record.replace('distance; promised delivery zone','distance; promised delivery zone; eventual arrival time')+'\n'+calcs,False,'Eventual arrival is not available at acceptance and cannot be a prediction input.'),(record+'\n'+calcs+'\nInterpretation: the specified-zone proportion applies to every zone.',False,'The conditional denominator is the specified zone only, not every zone.'),(record.replace('one order at acceptance','one delivery zone')+'\n'+calcs,False,'The counts and target concern orders, not a zone as the prediction unit.')])
f=source_f('file_object_ingestion');named=f['intended_object'];path=f['local_path'];types=repr(f['declared_types']);expect=repr(f['expected_columns']);rowcount=f['expected_row_count'];key=repr(f['expected_order_key'])
correct=f'''from google.cloud import storage
import pandas as pd
def ingest(bucket_name, prefix, object_name, local_path, identity_path, declared_types):
    client = storage.Client()  # supplied authorized runtime identity
    names = [blob.name for blob in client.list_blobs(bucket_name, prefix=prefix)]
    bucket = client.bucket(bucket_name)
    bucket.blob(object_name).download_to_filename(local_path)
    table = pd.read_csv(local_path, dtype=declared_types)
    columns_ok = list(table.columns) == {expect}
    rows_ok = len(table) == {rowcount}
    key_ok = table['order_key'].iloc[0] == {key}
    inspected = table.dtypes
    with open(identity_path, 'w', encoding='utf-8') as f:
        f.write(object_name + '\\n' + local_path)
    return local_path, table, columns_ok, rows_ok, key_ok, inspected
# Supplied call selects {named!r}, path {path!r}, declared_types={types}
# Format judgement: complete named CSV fits this full-file delimited-text read;
# a separately declared selected-column task would suit columnar Parquet.'''
judge('file_object_ingestion','Read each supplied ingestion excerpt and decide whether it meets the named retrieval, loaded-observation, identity-record or format criterion. The runtime identity is already authorized; judge the excerpt, do not run or write ingestion code.',[(correct,True,'The exact supplied object is selected, explicit types and loaded comparisons are checked, and the identity record is written inside UTF-8 context. The format statement distinguishes complete CSV access from selected-column Parquet.'),("# Intended object: "+repr(named)+"\nobject_name = 'approved/orders-a.csv'\nbucket.blob(object_name).download_to_filename(local_path)",False,'Selecting the other prefix object does not retrieve the named dataset.'),("table = pd.read_csv(local_path)\n# No dtype or value comparisons: inference is treated as a type guarantee.",False,'Explicit declared types and inspection of loaded representations are required; inference is not a guarantee.'),("with open(identity_path, 'r', encoding='utf-8') as f:\n    f.write(object_name + '\\n' + local_path)",False,'The text record must be written through a writing-mode handle inside the UTF-8 block.'),("# Full named CSV is the supplied format and access pattern.\n# Change its suffix to .parquet without converting or changing the supplied format.",False,'The format must match the supplied file and access pattern; changing a suffix is not selected-column Parquet access.')])
judge('preprocessing_pipeline','Read each supplied workflow excerpt and decide whether it meets the stated training-only pipeline, reusable prediction, representation/state, missing-value or malformed-input criterion. All constructors, policies and the deterministic fixture estimator are supplied; judge the implementation rather than running or writing it.',[("""from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
def build(X_train, y_train, X_validation, bounded, estimator):
    numeric = Pipeline([('impute', SimpleImputer(strategy='mean')),
                        ('scale', StandardScaler(with_mean=True, with_std=True))])
    prep = ColumnTransformer([('numeric', numeric, ['distance']),
                              ('zone', OneHotEncoder(handle_unknown='ignore'), ['zone'])])
    workflow = Pipeline([('preprocessing', prep), ('estimator', estimator)])
    workflow.fit(X_train, y_train)
    return workflow, workflow.predict(X_validation), workflow.predict(bounded)
# X_train has distance and zone; validation and bounded inputs use these same columns.
""",True,'The declared numerical and categorical operations are composed with the supplied estimator and fitted once on training; both prediction paths reuse that object.'),("workflow.fit(X_train, y_train)\nworkflow.fit(X_validation, y_validation)\nvalidation_predictions = workflow.predict(X_validation)",False,'Validation refitting violates the required unchanged training-fitted workflow.'),("""prep = workflow.named_steps['preprocessing']
mean_before = prep.named_transformers_['numeric'].named_steps['impute'].statistics_.copy()
scale_before = prep.named_transformers_['numeric'].named_steps['scale'].scale_.copy()
representation = prep.transform(X_validation)
assert_representation(representation, supplied_expected_representation)
predictions = workflow.predict(X_validation)
assert_outputs(predictions, supplied_expected_outputs)
assert_equal(mean_before, prep.named_transformers_['numeric'].named_steps['impute'].statistics_)
assert_equal(scale_before, prep.named_transformers_['numeric'].named_steps['scale'].scale_)
# assert_* are the supplied fixture equality predicates, not fitting operations.
""",True,'Representation, output and unchanged fitted state are explicitly verified without another fit.'),("missing_case = [{'distance': None, 'zone': 'south'}]\nmissing_predictions = workflow.predict(as_table(missing_case))\nassert_outputs(missing_predictions, supplied_missing_outcome)\n# as_table only constructs the supplied table fixture.",True,'The missing-distance fixture follows the same fitted imputer and prediction path, with its declared outcome checked.'),("malformed = as_table([{'distance': 2}])\n# Supplied malformed criterion requires rejection of absent zone.\ntry:\n    workflow.predict(malformed)\n    assert False\nexcept KeyError:\n    pass",True,'The missing required zone is a malformed input; the excerpt asserts the supplied failure rather than silently fabricating a zone.'),("# Missing zone is a declared malformed failure.\nmalformed['zone'] = 'north'\npredictions = workflow.predict(malformed)\n# No failure assertion.",False,'Silently filling the absent feature does not verify the specified malformed-input failure.')])
(B/'interactions.json').write_text(json.dumps(D,indent=2)+'\n')
