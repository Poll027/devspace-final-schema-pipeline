import json, ast, textwrap, copy
from pathlib import Path
P=Path('batches/final_batch_mle.region.data_readiness'); path=P/'interactions.json'
d=json.loads(path.read_text()); original=copy.deepcopy(d)
ix={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
def get(tile,step):return ix[f'mle.tile.{tile}.{step}']
def nodes(code):
 tree=ast.parse(code);return tree.body[0].body if isinstance(tree.body[0],ast.If) else tree.body

def extract(code,name):
 n=next(n for n in nodes(code) if isinstance(n,ast.FunctionDef) and n.name==name)
 return textwrap.dedent('\n'.join(code.splitlines()[n.lineno-1:n.end_lineno]))+'\n'
def build(tile,step,name,prompt,replacements=(),remove=(),custom=None,harness_change=None,checks=False):
 i=get(tile,step);code=i['grading']['solution_files'][0]['content'];ns=nodes(code)
 fn=custom or extract(code,name)
 for a,b in replacements:fn=fn.replace(a,b)
 omit=set(remove)|{name,'verify_assertion_behavior'}
 h=[]
 for n in ns:
  if isinstance(n,ast.FunctionDef) and n.name in omit:continue
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='evaluate' for t in n.targets):continue
  h.append(textwrap.dedent('\n'.join(code.splitlines()[n.lineno-1:n.end_lineno])))
 h='\n\n'.join(h)+'\n'
 if harness_change:h=harness_change(h)
 for t in i['grading']['tests']:
  ex=t.get('spec',{}).get('expected')
  if isinstance(ex,dict) and 'fixture_result' in ex:t['spec']['expected']=ex['fixture_result']
 head='# Supplied test interface; leave unchanged.\n'+h
 # preserve original function signature in the incomplete starter
 sig=fn.splitlines()[0]
 imports=[]
 for line in fn.splitlines():
  pass
 learner=fn
 starter=head+'\n# Learner implementation and fixture assertions.\n'+sig+'\n    # TODO: implement the requested operations.\n    pass\n'
 solution=head+'\n# Learner implementation and fixture assertions.\n'+learner
 if checks:
  tests=i['grading']['tests']; fixtures=[t['spec']['args'] for t in tests if t['kind']=='function_call']
  expects=[t['spec']['expected'] for t in tests if t['kind']=='function_call']
  helper='''
# Supplied assertion-test interfaces. Expected results are learner-authored below.
def canonical(value):
    import numpy as np
    if isinstance(value, dict):
        return {k:canonical(v) for k,v in value.items()}
    if isinstance(value, (list, tuple)):
        return [canonical(v) for v in value]
    if isinstance(value, set):
        return sorted(canonical(v) for v in value)
    if isinstance(value, np.ndarray):
        return canonical(value.tolist())
    if isinstance(value, np.dtype):
        return repr(value)
    if isinstance(value, np.generic):
        return canonical(value.item())
    if isinstance(value, float) and np.isnan(value):
        return None
    return value

def check_fixture(index, expected):
    return canonical(evaluate(*CHECK_FIXTURES[index])) == canonical(expected)

def detects_assertion(check):
    try:
        check()
    except AssertionError:
        return True
    return False

def run_checks():
    learner_checks()
    return True
'''
  helper+='\nCHECK_FIXTURES = '+repr(fixtures)+'\n'
  starter=head+helper+'\n# Learner implementation and fixture assertions.\n'+sig+'\n    # TODO: implement.\n    pass\n\ndef learner_checks():\n    # TODO: author the requested fixture assertions.\n    pass\n'
  solchecks='\ndef learner_checks():\n'+''.join('    assert check_fixture('+str(k)+', '+repr(ex)+')\n' for k,ex in enumerate(expects))
  solution=head+helper+'\n# Learner implementation and fixture assertions.\n'+learner+solchecks
  # run_checks must actually require learner-authored assertions, not a pass stub
  # their implementations still fail the result tests even if checks alone are omitted
  i['grading']['tests'].append({'test_id':'learner_assertions','kind':'function_call','spec':{'function':'run_checks','args':[],'expected':True},'visible':True,'message_on_fail':'The learner-authored fixture assertions must pass.'})
  prompt+=' Author your fixture checks in learner_checks(); the supplied check_fixture(index, expected) compares a computed report with your expected result.'
 i['public']['prompt']=prompt+' Preserve the report field names and ordering shown by the tests.'
 i['public']['workspace']['files'][0]['content']=starter
 i['grading']['solution_files'][0]['content']=solution
 return i

build('001_003','s05','inspect','Import NumPy and implement inspect(fixture). Construct the array without casting or flattening; inspect rank, shape and dtype; check rank before axis lengths; accept width two and batches of one through three; otherwise raise ValueError. Return the accepted array. Write assertions for one- and three-order list and tuple inputs and for empty, flat, wrong-width and four-order rejections.', [('a = construct(fixture)','a = np.array(fixture)'),('return {"rank": rank, "shape": shape, "dtype": dtype, "batch": batch, "width": width, "valid": valid}','return a')], harness_change=lambda h:h.replace('return {"accepted": True, "result": inspect(fixture)}','a = inspect(fixture)\n        return {"accepted": True, "result": {"rank":a.ndim,"shape":a.shape,"dtype":a.dtype,"batch":a.shape[0],"width":a.shape[1],"valid":True}}').replace('except ValueError as error:\n        return {"accepted": False, "reason": str(error)}','except ValueError:\n        return {"accepted": False, "reason": "ValueError"}'), checks=True)
i=get('001_003','s05')
for t in i['grading']['tests']:
 ex=t['spec']['expected']
 if isinstance(ex,dict) and ex.get('accepted') is False:ex['reason']='ValueError'
# synchronize learner-authored expectations after exception-type-only repair
for f in i['grading']['solution_files']:f['content']=f['content'].replace("'reason': 'rank'","'reason': 'ValueError'").replace("'reason': 'width'","'reason': 'ValueError'").replace("'reason': 'batch'","'reason': 'ValueError'")
# Include tuple constructions in the learner assertions (JSON calls can only supply lists).
i['grading']['solution_files'][0]['content']+='\n    assert inspect(((2,10),)).shape == (1,2)\n    assert inspect(((2,10),(4,20),(6,30))).shape == (3,2)\n'

build('001_003','s10','compare','Import NumPy and implement compare(reference, candidates, tolerance, budget). Cast each candidate from the unchanged reference; compare every scalar against the reference; calculate size times itemsize and confirm agreement with nbytes; return the shown report fields for each candidate, accepting only candidates that preserve values within tolerance and fit the element-storage budget. The justification must distinguish element storage from total object memory.', [('getattr(a,cast_method.__name__)(candidate_dtype)','a.astype(candidate_dtype)')])
build('001_003','s16','transform','Import NumPy and implement transform(fixture), subtracting the feature references [1, 5] with array arithmetic. Author an independent list-comprehension reference, assert that the result shape equals the input’s two-axis shape, and check agreement using np.testing.assert_allclose with rtol=1e-7 and atol=1e-9. Return the result array.', [('np.array(selected_offsets)','np.array([1, 5])')])

i=get('004_006','s06')
for item in i['public']['items']:
 if 'Declared CSV types' in str(item):
  print('type excerpt keys',item.keys())
  # change only the named excerpt's text
  for key in ['text','excerpt','code']:
   if key in item and ('read_csv' in item[key]):item[key]='declared_types = {"order_key":"string","distance":"float64","zone":"string","eventual_arrival":"string"}\ntable = pd.read_csv(local_path, dtype=declared_types)\n# Observed columns: order_key, distance, zone, eventual_arrival; row count: 6; dtypes match declared_types; first order_key: \'0012\'.'

build('004_006','s11','scan','Import pandas and implement scan(path, budget, feature_count, element_width, declared_types). Calculate the row limit, iterate read_csv chunks inside an open-file block, materialize each matrix, calculate bytes from its actual shape and dtype, assert agreement with nbytes and compliance with budget, and return row_limit, largest_element_bytes and memory_scope. Do not retain previous chunks.', [('reader(file_handle','pd.read_csv(file_handle')])
i=get('004_006','s11');t1,t2=i['grading']['tests'][:2]
# Findings specify the original eight-row packet. The registered asset is now larger;
# preserve the requested test change without silently replacing that external asset.
features=ast.literal_eval(next(n for n in ast.walk(ast.parse(i['public']['workspace']['files'][0]['content'])) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FEATURE_COUNT' for t in n.targets)).value)
width=ast.literal_eval(next(n for n in ast.walk(ast.parse(i['public']['workspace']['files'][0]['content'])) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ELEMENT_WIDTH' for t in n.targets)).value)
t1['spec']['expected']['largest_element_bytes']=8*features*width
t2['spec']['args']=[3*features*width];t2['spec']['expected']['row_limit']=t2['spec']['args'][0]//(features*width);t2['spec']['expected']['largest_element_bytes']=t2['spec']['args'][0]

names=None
screens=json.loads((P/'screens.json').read_text())
for tile in screens['tiles']:
 for e in tile['steps']:
  if e['step_id']=='mle.tile.004_006.s12':
   c=next(b['code'] for b in e['blocks'] if b['type']=='code_walkthrough')
   names=ast.literal_eval(ast.parse(c).body[0].value)['feature_columns']
custom='''def readiness(columns, numeric_values, ddof=0):
    numeric_values = np.array(numeric_values)
    shape = numeric_values.shape
    return {"columns":columns,"column_dtypes":{columns[0]:numeric_values.dtype,columns[1]:numeric_values.dtype},"observations":shape[0],"features":shape[1],"shape":shape,"dtype":numeric_values.dtype,"element_bytes":shape[0]*shape[1]*numeric_values.dtype.itemsize,"means":np.mean(numeric_values,axis=0),"standard_deviations":np.std(numeric_values,axis=0,ddof=ddof),"memory_scope":"element storage, not total process memory"}
'''
i=build('004_006','s16','readiness','Import NumPy and implement readiness(columns, numeric_values, ddof=0). Return columns, column_dtypes, observations, features, shape, dtype, element_bytes, means, standard_deviations and memory_scope. Summarize each feature over rows using the stated divisor, preserve the observation/feature axis meanings, and label bytes as element storage rather than total process memory.',custom=custom,harness_change=lambda h:h.replace('def evaluate(fixture):','def evaluate(fixture, ddof=0):').replace('return readiness(fixture)','return readiness('+repr(names)+',fixture,ddof)'))
for t in i['grading']['tests']:
 ex=t['spec']['expected'];ex['columns']=names;ex['column_dtypes']={k:ex['dtype'] for k in names}
t=copy.deepcopy(i['grading']['tests'][0]);t['test_id']='ddof_one';t['spec']['args'].append(1)
import math
# compute changed divisor from data, without hand-entering a statistic
rows=t['spec']['args'][0]
t['spec']['expected']['standard_deviations']=[math.sqrt(sum((r[j]-sum(x[j] for x in rows)/len(rows))**2 for r in rows)/(len(rows)-1)) for j in range(len(rows[0]))]
i['grading']['tests'].append(t)

# pin string dtype for all relevant zone fixtures before building learner checks
i=get('007_008','s05')
for t in i['grading']['tests']:
 types=t['spec']['args'][0].get('types',{})
 if 'zone' in types:types['zone']='string'
i=build('007_008','s05','validate','Import pandas and implement validate(table) under the stated column, dtype and value contract. Exactly distance: float64 and zone: string; distance 0 through 100 inclusive; zone north or south. Check columns and types before values, raise descriptive ValueError exceptions without changing the input, and return True for accepted tables. Author assertions for valid input, both inclusive boundaries, missing and unexpected columns, wrong types, invalid zones and out-of-range distances.', [('"zone"] != "object"','"zone"] != "string"'),('getattr(distances,require_all.__name__)()','distances.all()'),('getattr(zones,require_all.__name__)()','zones.all()')],remove=['df'],checks=True)

build('007_008','s10','clean_orders','Implement clean_orders(records, policy). Use an accepted-key set, add keys only after acceptance, apply the supplied duplicate, distance and zone-repair policies through branches, and return cleaned observations plus affected observation IDs and actions using the shown report schema. Author assertions for retain, both distance boundaries, repair, rejection, repeated accepted keys and an invalid-then-valid retry; demonstrate detection of a deliberately false expected result.',remove=['declared_policy','no_repairs_policy'],harness_change=lambda h:h.replace('clean_orders(records,chosen_policy)','clean_orders(records,POLICY)'),checks=True)

build('009_011','s06','evaluate_statistics','Import NumPy and implement evaluate_statistics(fixture). Calculate sample shares using the sample total, target shares using the target total, and category inclusion rates using each category’s target count; return \'unsupported\' for a zero category denominator. Compute the selected observations’ mean and population standard deviation. Return the existing ordered result fields and a count-supported limitation without asserting an unobserved cause or inevitable prediction failure.', [('mean_operation(numeric_values)','np.mean(numeric_values)'),('spread_operation(numeric_values,ddof=0)','np.std(numeric_values,ddof=0)')])
i=get('009_011','s06');t=i['grading']['tests'][1];fixture=t['spec']['args'][0];fixture['sample_b']=0
# derive altered expected values from the changed fixture
values=[v[0] for v in fixture['numeric_values']];mean=sum(values)/len(values)
t['spec']['expected'][:8]=[fixture['sample_a']/(fixture['sample_a']+fixture['sample_b']),fixture['sample_b']/(fixture['sample_a']+fixture['sample_b']),fixture['target_a']/(fixture['target_a']+fixture['target_b']),fixture['target_b']/(fixture['target_a']+fixture['target_b']),fixture['sample_a']/fixture['target_a'],'unsupported',mean,math.sqrt(sum((v-mean)**2 for v in values)/len(values))]

build('009_011','s11','audit','Implement audit(observations, labels, boundary) using the supplied acceptance predicates. Detect repeated observation and label IDs before mapping; report both unmatched-ID directions; use keyed lookups to report invalid, misaligned and unavailable records, accepting cutoff equality. Return the shown verdict and affected-ID fields. Author assertions for valid, reordered, duplicate, missing, orphaned, invalid, misaligned, unavailable and equality-boundary fixtures.', [('availability_policy(label,boundary)','available(label,boundary)')],remove=['inclusive_availability','strict_availability'],checks=True)
build('009_011','s16','partition','Implement partition(records, scenario, training_groups, cutoff, end). In the group scenario, assign complete groups and assert disjoint group sets. In the time scenario, use training timestamps < cutoff and cutoff <= validation timestamps < end. Return the shown partitions, their own target proportions or None when empty, and a scenario-specific justification. Author valid, equality-boundary and deliberately invalid group/time assertions.', [('training_boundary(row["observation_timestamp"],cutoff)','row["observation_timestamp"] < cutoff')],remove=['earlier_training','inclusive_training'],checks=True)

build('012_015','s05','replace_missing','Import NumPy and SimpleImputer and implement replace_missing(train, validation, single_missing). Fit a mean imputer only on training rows; compute the observed training column mean and population standard deviation; transform validation and the single-missing boundary without refitting. Return the shown report fields and author assertions for unchanged statistics_, complete and missing outputs, and a deliberately incorrect replacement. This exercise checks imputation outputs, unchanged statistics_ and the single-missing boundary.', [('imputer.fit(fit_source(X_train,X_validation))','imputer.fit(X_train)'),('validation_operation(imputer,X_validation)','imputer.transform(X_validation)')],remove=['training_only','training_plus_validation','reuse_transform','refit_transform'],checks=True)
build('012_015','s11','scale','Import NumPy and StandardScaler and implement scale(train, validation). Compute training column means and population standard deviations; fit one centered, standardized scaler on training only; transform both inputs using that fitted object. Return the shown report fields. Author assertions for expected values, unchanged mean_ and scale_, constant-feature scale_ of 1, and detection of incorrect results or changed state. This exercise checks scaled outputs, unchanged mean_/scale_ and the constant-feature boundary.', [('scaler.fit(fit_source(X_train,X_validation))','scaler.fit(X_train)'),('validation_operation(scaler,X_validation)','scaler.transform(X_validation)')],remove=['training_only','training_plus_validation','reuse_transform','refit_transform'],checks=True)
build('012_015','s16','encode','Import NumPy and OneHotEncoder and implement encode(training, cases, policy). Fit once with the explicitly supplied error or ignore policy, build the zone mapping from categories_, transform the aligned cases without refitting, and return mapping, width and results using the shown schema. Author assertions for known indicators, unknown and missing behavior, unchanged categories and output width across both policies and both missing-at-fit conditions.', [('validation_operation(encoder,category_array(case))','encoder.transform(category_array(case))')],remove=['reuse_transform','refit_transform'],checks=True)

# Genuine deliberately incorrect report assertions, authored by the learner.
for tile,step in [('007_008','s10'),('012_015','s05'),('012_015','s11')]:
 i=get(tile,step)
 for f in i['public']['workspace']['files']:f['content']+='\ndef incorrect_check():\n    # TODO: assert a deliberately incorrect expected result.\n    pass\n'
 content=i['grading']['solution_files'][0]['content'];content=content.replace('def learner_checks():\n','def learner_checks():\n    assert detects_assertion(incorrect_check)\n')
 content+='\ndef incorrect_check():\n    assert check_fixture(0, {})\n'
 i['grading']['solution_files'][0]['content']=content

# Correct fitted-component provenance in the existing state-preservation excerpt.
i=get('012_015','s21')
for item in i['public']['items']:
 for k,v in list(item.items()):
  if isinstance(v,str) and 'imputer.statistics_' in v and 'workflow' in v:
   prefix='# workflow has already been fitted on X_train only.\npre = workflow.named_steps["pre"]; numeric = pre.named_transformers_["distance"]; imputer = numeric.named_steps["imputer"]; scaler = numeric.named_steps["scaler"]; encoder = pre.named_transformers_["zone"]\n'
   # insert before the first state snapshot
   lines=v.splitlines();pos=next((j for j,line in enumerate(lines) if 'imputer.statistics_' in line),0);lines[pos:pos]=prefix.rstrip().splitlines();item[k]='\n'.join(lines)

# Move lookup selection coverage to the existing check.
src=get('016_017','s11');dst=get('016_017','s10')
moved=[m for m in src['measures'] if m['capability']=='select_lookup_value_at_recorded_boundary']
src['measures']=[m for m in src['measures'] if m not in moved]
for m in moved:
 if m not in dst['measures']:dst['measures'].append(m)
for a in list(src.get('anchors',[])):
 if 'select_lookup_value_at_recorded_boundary' in a:
  src['anchors'].remove(a)
  if a not in dst['anchors']:dst['anchors'].append(a)
dst['public']['prompt']='At 09:30 the recorded lookup value is 3; it changes to 7 at 09:30:01. Which check is correct?'
key=dst['grading']['correct_option_ids'][0];texts=['Use latest value 7','Include the later record in the earlier sum.'];wrong=iter(texts)
for option in dst['public']['options']:option['text']='Use recorded value 3 and assert that adding the later record leaves the earlier feature unchanged' if option['option_id']==key else next(wrong)
for option in dst['public']['options']:
 oid=option['option_id'];dst['grading']['option_feedback'][oid]['message']='Use only the recorded information available at the earlier boundary; later records must not change that earlier feature.' if oid==key else 'This uses information recorded after the 09:30 boundary and changes the earlier feature.'

build('016_017','s11','feature','Import datetime and implement feature(records, prediction_time). Use a list comprehension selecting available_at <= prediction_time, initialize total=0, accumulate only accepted values, and return total. Author assertions for the exact boundary, empty input and invariance after adding a later record.', [('boundary_rule(row,prediction_time)','row["available_at"] <= prediction_time')],remove=['available_by_boundary','strictly_before_boundary','all_records'],checks=True)

build('018_018','s05','permitted_record','Implement permitted_record(identity, sample, permitted_fields). Call the supplied authorized read interface before processing; construct a fresh dictionary using permitted-field membership checks; preserve permitted values; exclude token and raw_customer_values; do not print restricted values or retrieve/copy the runtime secret. Return the dictionary and allow authorization denial to propagate.', [('field_policy(key,permitted_fields)','key in permitted_fields and key not in ("token", "raw_customer_values")')],remove=['permitted_only','every_field'])

# Leakage implementation and shared boundary checks are both learner-authored.
custom='''def corrected(training, held_out, preprocessor, predictor):
    fields = ["distance", "zone"]
    train_inputs = select_available(training,fields)
    held_inputs = select_available(held_out,fields)
    preprocessor.fit(train_inputs)
    transformed = preprocessor.transform(held_inputs)
    return predictor.predict(transformed)

def boundary_check(training, held_out, preprocessor, predictor):
    train_inputs = select_available(training,["distance","zone"])
    held_inputs = select_available(held_out,["distance","zone"])
    assert preprocessor.fit_rows == train_inputs
    assert preprocessor.transform_rows == [held_inputs]
    assert predictor.input_rows == [held_inputs]
    return True
'''
def leak_harness(h):
 h=h.replace('corrected(fixture["training"],fixture["held_out"],preprocessor,predictor)','corrected(fixture["training"],fixture["held_out"],preprocessor,predictor)\n    corrected_passed = boundary_check(fixture["training"],fixture["held_out"],preprocessor,predictor)\n    leaked_pre = TracePreprocessor()\n    leaked_pred = TracePredictor()\n    leaked(fixture["training"],fixture["held_out"],leaked_pre,leaked_pred)\n    leaked_failed = False\n    try:\n        boundary_check(fixture["training"],fixture["held_out"],leaked_pre,leaked_pred)\n    except AssertionError:\n        leaked_failed = True\n    assert corrected_passed and leaked_failed')
 h=h.replace('"prediction_inputs":predictor.input_rows}','"prediction_inputs":predictor.input_rows,"corrected_passed":corrected_passed,"leaked_failed":leaked_failed}')
 h+='\ndef leaked(training,held_out,preprocessor,predictor):\n    train_inputs = select_available(training,["distance","zone","eventual_arrival"])\n    held_inputs = select_available(held_out,["distance","zone","eventual_arrival"])\n    preprocessor.fit(train_inputs+held_inputs)\n    predictor.predict(preprocessor.transform(held_inputs))\n'
 return h
i=build('016_017','s05','corrected','Implement corrected(training, held_out, preprocessor, predictor), selecting only distance and zone, fitting preprocessing only on training inputs and transforming held-out inputs without refitting. Author trace assertions for permitted prediction fields, training-only fit rows and held-out transform/prediction inputs in boundary_check. Run the same checks against a supplied leaked variant and the corrected variant, asserting failure for the former and success for the latter.',custom=custom,remove=['training_only','training_plus_held_out'],harness_change=leak_harness)
i['public']['workspace']['files'][0]['content']+='\ndef boundary_check(training, held_out, preprocessor, predictor):\n    # TODO: author the shared trace assertions.\n    pass\n'
for t in i['grading']['tests']:t['spec']['expected'].update(corrected_passed=True,leaked_failed=True)

# Task-specific hints, only rewording the named repeated hint.
hints={
'mle.prediction_task_definition':'Separate the order-level target horizon from the prediction-time inputs and population denominator.',
'mle.numpy_shape_dtype':'Check rank before indexing the shape tuple.',
'mle.numpy_dtype_selection':'Compare each candidate against the unchanged reference, then inspect element-storage bytes.',
'mle.numpy_vectorization':'A feature reference vector must align with the trailing feature axis.',
'mle.file_object_ingestion':'Check the named object and all declared column types; a write must happen before its with block ends.',
'mle.chunked_ingestion':'Calculate element bytes from the current matrix’s actual shape and dtype.',
'mle.dataset_inspection':'axis=0 summarizes each feature over observations; the divisor changes with ddof.',
'mle.input_validation':'Check columns and dtypes before evaluating the inclusive value limits.',
'mle.deterministic_cleaning':'Add an order key to the accepted set only after its observation passes the policy.',
'mle.selection_bias':'Use each category’s own target count as its inclusion-rate denominator.',
'mle.label_alignment':'Inspect repeated IDs before mapping, then compare keyed records in both directions.',
'mle.train_validation_split':'Keep complete groups together; cutoff equality belongs to validation.',
'mle.missing_value_imputation':'The replacement statistic must come only from observed training values.',
'mle.feature_scaling':'Reuse training mean_ and scale_; inspect the constant-feature column separately.',
'mle.categorical_encoding':'Inspect fitted categories_ before and after transforming each aligned case.',
'mle.preprocessing_pipeline':'Check that the snapshots refer to the fitted components inside the workflow.',
'mle.data_leakage':'Trace which fields and rows enter fit and held-out transform calls.',
'mle.prediction_time_features':'Compare each available_at timestamp with the recorded prediction boundary.',
'mle.secure_data_handling':'Authorize the read first, then copy only permitted, nonrestricted fields.'}
bundle=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
for i in ix.values():
 if 'Identify the required input or result boundary before comparing the alternatives.' in i['feedback'].get('hints',[]):
  cid=i['measures'][0]['concept_id'];hint=hints.get(cid)
  if not hint:
   # use the glossary's own mechanism rather than inventing a new fact
   b=next(b for b in bundle['bundles'] if b['context']['concept_id']==cid)
   hint='Recheck '+b['context']['concept_name'].lower()+', using the declared fixture and its stated criterion.'
  i['feedback']['hints']=[hint if h=='Identify the required input or result boundary before comparing the alternatives.' else h for h in i['feedback']['hints']]
path.write_text(json.dumps(d,indent=2)+'\n')
changes=[k for k in ix if next(e['interaction'] for t in original['tiles'] for e in t['interactions'] if e['step_id']==k)!=ix[k]]
(P/'scratch/repair_changes.json').write_text(json.dumps(changes,indent=2))
print('Patched',len(changes),'interactions; s06 planning gap left unchanged except advisory hint.')
