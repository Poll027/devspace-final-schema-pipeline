import json,sys,pprint,copy
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_mle.region.data_readiness');load=lambda n:json.loads((B/n).read_text())
d=load('interactions.json');r=load('scenario_asset_registry.json')
fx={a['asset_id'][3:]:json.loads(next(f['content'] for f in a['files'] if f['path']=='fixtures.json')) for a in r['assets'] if a['asset_kind']=='code_workspace'}
defs={
'numpy_shape_dtype':'''def probe_contract(fixture):
    try:
        a = validate(fixture)
        return {'values':a.tolist(),'rank':a.ndim,'shape':a.shape,'dtype':str(a.dtype)}
    except ValueError:
        return 'ValueError'
''',
'numpy_vectorization':'''def probe_contract(matrix, references):
    return transform(matrix,references)
''',
'dataset_schema_validation':'''def probe_contract(fixture, contract, wrong_type=False):
    t = pd.DataFrame(fixture['rows'], columns=fixture['columns'])
    t = t.astype({k:v for k,v in contract['declared_types'].items() if k in t.columns})
    if wrong_type: t = t.astype({'distance':'string'})
    try:
        return validate(t,contract)
    except ValueError as error:
        return str(error)
''',
'dataset_cleaning_policy':'''def probe_contract(records,policy):
    return clean(records,policy)
''',
'label_integrity':'''def probe_contract(observations, labels, contract):
    return audit(observations,labels,contract)
''',
'training_fitted_imputation':'''def probe_contract(training, validation, boundary, observed):
    arrays = [np.array([[np.nan if v is None else v for v in row] for row in rows]) for rows in [training,validation,boundary,observed]]
    return impute(*arrays)
''',
'training_fitted_scaling':'''def probe_contract(training,validation):
    return scale(np.array(training),np.array(validation))
''',
'categorical_encoding':'''def probe_contract(training, known, unseen, missing, policy):
    arrays = [[[np.nan if v is None else v for v in row] for row in rows] for rows in [training,known,unseen,missing]]
    return encode(*arrays,policy)
''',
'prediction_boundary_leakage':'''def probe_contract(training,held_out,columns):
    return correct(training,held_out,columns)
''',
'leakage_safe_features':'''def probe_contract(records,boundary):
    converted = [{'available_at':datetime.fromisoformat(r['available_at']),'value':r['value']} for r in records]
    return feature(converted,datetime.fromisoformat(boundary))
''',
'sensitive_ml_assets':'''def probe_contract(identity,sample,fields):
    import io, contextlib
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            record = audit(identity,sample,fields)
        except PermissionError:
            record = 'PermissionError'
    return {'record':record,'stdout':output.getvalue()}
'''}
args={}
f=fx['numpy_shape_dtype'];args['numpy_shape_dtype']=[[f[k]] for k in ['valid','tuple_boundary','empty','flat','wrong_width','too_many']]
f=fx['numpy_vectorization'];args['numpy_vectorization']=[[f['matrix'],f['feature_references']],[f['matrix'][:1],f['feature_references']]]
f=fx['dataset_schema_validation'];args['dataset_schema_validation']=[[f[k],f['contract']] for k in ['valid','negative','too_large','missing_column','invalid_representation','unexpected_column']]+[[f['valid'],f['contract'],True]]
f=fx['dataset_cleaning_policy'];modified=copy.deepcopy(f['records']);modified[0]['distance']=f['policy']['distance_min']-1;args['dataset_cleaning_policy']=[[f['records'],f['policy']],[f['valid'],f['policy']],[modified,f['policy']]]
f=fx['label_integrity'];args['label_integrity']=[[f['observations'],f['labels'],f['contract']]]+[[f['observations'],rows,f['contract']] for rows in f['cases'].values()]
f=fx['training_fitted_imputation'];modified=copy.deepcopy(f['X_validation']);modified[0][0]+=1;args['training_fitted_imputation']=[[f['X_train'],f['X_validation'],f['boundary_missing'],f['numeric_values']],[f['X_train'],modified,f['boundary_missing'],f['numeric_values']]]
f=fx['training_fitted_scaling'];modified=copy.deepcopy(f['X_validation']);modified[0][0]+=1;args['training_fitted_scaling']=[[f['X_train'],f['X_validation']],[f['X_train'],modified]]
f=fx['categorical_encoding'];args['categorical_encoding']=[[training,f['cases']['north'],f['cases']['east'],f['cases']['None'],policy] for training,policy in [(f['X_train'],'ignore'),(f['X_train'],'error'),(f['X_train_missing'],'ignore')]]
f=fx['prediction_boundary_leakage'];args['prediction_boundary_leakage']=[[f['training'],f['held_out'],f['permitted_features']],[f['training'],f['held_out'][:1],f['permitted_features']]]
f=fx['leakage_safe_features'];args['leakage_safe_features']=[[rows,f['prediction_time']] for rows in [f['records'],f['augmented_records'],f['empty'],[f['records'][-1]]]]
f=fx['sensitive_ml_assets'];args['sensitive_ml_assets']=[[f['authorized_identity'],f['sample'],f['permitted_fields']],[f['unauthorized_identity'],f['sample'],f['permitted_fields']]]
index={};jobs=[]
for t in d['tiles']:
 for entry in t['interactions']:
  ix=entry['interaction']
  if ix['type']!='code_exercise':continue
  name=next(a.split('#')[0].split('.',1)[1] for a in ix['anchors'] if a.endswith('#practice'))
  if name not in defs:continue
  # A supplied test adapter only converts JSON test arguments and captures declared errors.
  # It contains no implementation of the task. The authentic learner function remains editable.
  scaffold='\n# Supplied grading adapter; do not change it.\nexec('+repr(defs[name])+')\n'
  ix['public']['workspace']['files'][0]['content']+=scaffold
  ix['grading']['solution_files'][0]['content']+=scaffold
  probes=[{'id':'call'+str(i),'kind':'call','function':'probe_contract','args':aa} for i,aa in enumerate(args[name])]
  tables,_=sandbox._tables(r,ix['public']['workspace']['asset_mounts'],{},[])
  jobs.append(sandbox._py_script(name,'main.py',ix['grading']['solution_files'][0]['content'],sandbox._py_mounts(tables),probes))
  index[name]=ix
results=sandbox.node_run(sandbox._py_job('python',['numpy','pandas'],jobs),sandbox.RUNTIMES['python']['runner'])
(B/'stage04_function_expectations.json').write_text(json.dumps(results,indent=2))
for name,ix in index.items():
 result=results['results'][name]
 if not result['ok']:raise RuntimeError(name+': '+result['error'])
 tests=[]
 for i,aa in enumerate(args[name]):
  p=result['probes']['call'+str(i)]
  if not p['ok']:raise RuntimeError(name+': '+p['error'])
  tests.append({'test_id':'call'+str(i),'kind':'function_call','spec':{'function':'probe_contract','args':aa,'expected':p['value']},'message_on_fail':'The reusable function violates the supplied fixture contract.'})
 ix['grading']['tests']=tests
(B/'interactions.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Added',sum(len(v['grading']['tests']) for v in index.values()),'input-sensitive function tests for',len(index),'exercises')
