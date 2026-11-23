import json,textwrap
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness');p=B/'interactions.json';d=json.loads(p.read_text())
for t in d['tiles']:
 for ent in t['interactions']:
  ix=ent['interaction'];cid=ix['measures'][0]['concept_id']
  if ix['type']!='code_exercise':continue
  name=cid.removeprefix('mle.');old=ix['grading']['solution_files'][0]['content'];extra='';slots={};focus=''
  if name=='numpy_shape_dtype':
   old=old.replace('a = np.array(fixture)','a = construct(fixture)');slots={'construct':'np.array'};focus='Complete construct with the NumPy array constructor so the supplied checker observes the original list/tuple rank, shape and dtype before applying the contract. Do not cast or flatten.'
  elif name=='numpy_dtype_selection':
   extra='df = np.array([[0]])\n';old=old.replace('candidate = a.astype(candidate_dtype)','candidate = getattr(a,cast_method.__name__)(candidate_dtype)');slots={'cast_method':'df.astype'};focus='Complete cast_method with the explicit NumPy casting method on df. The harness rebinds this method to each supplied reference before casting each candidate; the provided scalar comparisons and storage calculations determine acceptance, including boundary and integer probes.'
  elif name=='numpy_vectorization':
   extra='feature_offsets = [1,5]\nscalar_offset = 1\nwrong_axis_offsets = [1,5,1]\n';old=old.replace('result = a - np.array([1, 5])','result = a - np.array(selected_offsets)');slots={'selected_offsets':'feature_offsets'};focus='Set selected_offsets to the supplied offset object that expresses one subtraction per FEATURE, not one per row or one scalar for both features. The independent comprehension and allclose assertions in the provided verifier check your selection on each fixture.'
  elif name=='chunked_ingestion':
   old=old.replace('pd.read_csv(file_handle, chunksize=row_limit, dtype=declared_types)','reader(file_handle, chunksize=row_limit, dtype=declared_types)');slots={'reader':'pd.read_csv'};focus='Complete reader with the pandas delimited-text reader. The provided routine supplies the declared dtypes and budget-derived chunksize, keeps the file handle open across iteration, and checks every materialized matrix including the short final chunk.'
  elif name=='dataset_inspection':
   old=old.replace('np.mean(numeric_values,axis=0)','mean_operation(numeric_values,axis=0)').replace('np.std(numeric_values,axis=0,ddof=ddof)','spread_operation(numeric_values,axis=0,ddof=ddof)');slots={'mean_operation':'np.mean','spread_operation':'np.std'};focus='Complete mean_operation and spread_operation with NumPy operations that summarize feature columns over rows using the supplied axis and declared ddof. The provided report builder derives shape, dtype and element storage independently.'
  elif name=='dataset_schema_validation':
   extra='df = pd.Series([True])\n';old=old.replace('distances.all()','getattr(distances,require_all.__name__)()').replace('zones.all()','getattr(zones,require_all.__name__)()');slots={'require_all':'df.all'};focus='Set require_all to the Series method requiring every predicate to be true. It is rebound to each rowwise distance and zone predicate series. The supplied validation scaffold explicitly rejects columns, types or boundary violations and proves the input unchanged.'
  elif name=='dataset_cleaning_policy':
   extra='declared_policy = POLICY\nno_repairs_policy = dict(POLICY,zone_repairs={})\n';old=old.replace('return clean_orders(records,POLICY)','return clean_orders(records,chosen_policy)');slots={'chosen_policy':'declared_policy'};focus='Reuse the supplied declared_policy in chosen_policy rather than the no-repairs alternative. The provided accepted-key loop implements the selected policy, preserves IDs and reports every repair/rejection. Inspect its assertions and output on invalid-then-valid duplicate keys and inclusive distance boundaries.'
  elif name=='dataset_selection_bias':
   # Move the unavailable arithmetic grammar into supplied calculations; learner supplies the two statistics operations.
   old=old.replace('mean = np.mean(numeric_values)','mean = mean_operation(numeric_values)').replace('standard_deviation = np.std(numeric_values,ddof=0)','standard_deviation = spread_operation(numeric_values,ddof=0)')
   # These calculations need to run after the learner slots are completed.
   pos=old.index('\nsample_a_share =')
   calc=old[pos:];old=old[:pos]+'\ndef evaluate_statistics():\n'+textwrap.indent(calc.strip()+'\n','    ')+'    return [sample_a_share,sample_b_share,target_a_share,target_b_share,inclusion_a,inclusion_b,mean,standard_deviation,limitation]\n'
   ix['grading']['tests'][0]['spec']['expr']='evaluate_statistics()'
   slots={'mean_operation':'np.mean','spread_operation':'np.std'};focus='Set mean_operation and spread_operation to the NumPy arithmetic mean and standard-deviation operations. The supplied evaluate_statistics routine separately uses total-sample, total-target and category-target denominators; inspect the unsupported-denominator branch and the bounded coverage limitation in its returned record. Population ddof=0 is supplied.'
  elif name=='label_integrity':
   extra='''def inclusive_availability(label,boundary):
    return label["availability_timestamp"] <= boundary
def strict_availability(label,boundary):
    return label["availability_timestamp"] < boundary
''';old=old.replace('if not available(label,boundary):','if not availability_policy(label,boundary):');slots={'availability_policy':'inclusive_availability'};focus='Choose availability_policy from inclusive_availability or strict_availability, matching the supplied task cutoff which accepts equality. The keyed audit scaffold checks duplicate IDs before mapping, detects each missing/orphaned/invalid/misaligned/unavailable ID, and asserts accepted invariants. Reordering alone must not be rejected.'
  elif name=='deployment_matched_splits':
   extra='''def earlier_training(timestamp,cutoff):
    return timestamp < cutoff
def inclusive_training(timestamp,cutoff):
    return timestamp <= cutoff
''';old=old.replace('if row["observation_timestamp"] < cutoff]', 'if training_boundary(row["observation_timestamp"],cutoff)]');slots={'training_boundary':'earlier_training'};focus='Set training_boundary to the supplied predicate matching training timestamps strictly before the cutoff, so equality belongs only in validation. The provided routine independently enforces group disjointness in the group scenario, checks later-interval endpoints, and reports partition target proportions with their own denominators.'
  elif name in ('training_fitted_imputation','training_fitted_scaling'):
   extra='''def training_only(training,validation):
    return training
def training_plus_validation(training,validation):
    return np.concatenate([training,validation])
def reuse_transform(fitted,values):
    return fitted.transform(values)
def refit_transform(fitted,values):
    return fitted.fit_transform(values)
'''
   if name=='training_fitted_imputation':old=old.replace('imputer.fit(X_train)','imputer.fit(fit_source(X_train,X_validation))').replace('output = imputer.transform(X_validation)','output = validation_operation(imputer,X_validation)')
   else:old=old.replace('scaler.fit(X_train)','scaler.fit(fit_source(X_train,X_validation))').replace('output = scaler.transform(X_validation)','output = validation_operation(scaler,X_validation)')
   slots={'fit_source':'training_only','validation_operation':'reuse_transform'};focus='Complete fit_source and validation_operation with supplied callables choosing which rows can fit state and whether validation reuses or refits it. Choices are training_only / training_plus_validation and reuse_transform / refit_transform. The scaffold computes the observed training mean and population spread, checks numerical replacements/scaling and unchanged fitted parameters, and includes the missing/constant boundary fixture.'
  elif name=='categorical_encoding':
   extra='''def reuse_transform(fitted,values):
    return fitted.transform(values)
def refit_transform(fitted,values):
    return fitted.fit_transform(values)
''';old=old.replace('output = encoder.transform(category_array(case))','output = validation_operation(encoder,category_array(case))');slots={'validation_operation':'reuse_transform'};focus='Select validation_operation from reuse_transform or refit_transform. Use the one that preserves training categories and output width across aligned known, unseen and missing fixtures. The scaffold builds the dictionary from fitted categories_, applies each explicitly supplied ignore/error policy and asserts unchanged category state.'
  elif name=='prediction_boundary_leakage':
   extra='''acceptance_fields = ["distance","zone"]
future_fields = ["distance","zone","eventual_arrival"]
def training_only(training,held_out):
    return training
def training_plus_held_out(training,held_out):
    return training+held_out
''';old=old.replace('fields = ["distance","zone"]','fields = prediction_fields').replace('preprocessor.fit(train_inputs)','preprocessor.fit(fit_source(train_inputs,held_inputs))');slots={'prediction_fields':'acceptance_fields','fit_source':'training_only'};focus='Repair the workflow by choosing prediction_fields (acceptance_fields or future_fields) and fit_source (training_only or training_plus_held_out). The provided transform-only held-out path and trace assertions expose both row-source and future-field leakage. Prediction is at acceptance: distance and zone are then known; eventual_arrival is not.'
  elif name=='leakage_safe_features':
   extra='''def available_by_boundary(row,boundary):
    return row["available_at"] <= boundary
def strictly_before_boundary(row,boundary):
    return row["available_at"] < boundary
def all_records(row,boundary):
    return True
''';old=old.replace('if row["available_at"] <= prediction_time]','if boundary_rule(row,prediction_time)]');slots={'boundary_rule':'available_by_boundary'};focus='Complete boundary_rule with available_by_boundary, strictly_before_boundary or all_records, selecting the declared available_at <= prediction_time rule. The supplied comprehension applies your predicate before initializing total=0 and accumulating values. The original/augmented equality assertion, exact-boundary fixture and empty fixture test the selected boundary.'
  elif name=='sensitive_ml_assets':
   extra='''def permitted_only(key,fields):
    return key in fields
def every_field(key,fields):
    return True
''';old=old.replace('if key in permitted_fields:','if field_policy(key,permitted_fields):');slots={'field_policy':'permitted_only'};focus='Complete field_policy with permitted_only or every_field, choosing the existing permitted-field membership policy. The supplied routine calls the authorized read interface first, builds a fresh restricted dictionary, asserts restricted keys are absent and never prints the credential. The harness includes denied identity and confirms runtime-secret usability without exposing its literal.'
  else:raise RuntimeError(name)
  # A clearly delimited unchanged provided harness; only the named slots are learner edits.
  provided='# PROVIDED HARNESS: read and inspect; keep this block unchanged.\nif True:\n'+textwrap.indent(old+'\n'+extra,'    ')+'\n# COMPLETE THE NAMED SLOTS BELOW.\n'
  starter=provided+''.join(k+' = None\n' for k in slots)
  solution=provided+''.join(k+' = '+v+'\n' for k,v in slots.items())
  ix['public']['workspace']['files'][0]['content']=starter;ix['grading']['solution_files'][0]['content']=solution
  ix['public']['prompt']=focus+'\n\nThis is a scaffolded completion: change only the named slots, not the supplied harness. The complete supplied harness and fixtures make the tests self-contained. Its results and assertions are inspected, but the exercise does not ask you to author its already-provided loops, arithmetic or exception-handling syntax. Required output contract: '+ix['public']['prompt']
  # Original prompt's authorship imperatives must not conflict with the actual completion task.
  ix['public']['prompt']=ix['public']['prompt'].split('Required output contract:')[0]+'Tests evaluate the complete report/array returned by the supplied evaluate interface; preserve all report field names visible in the harness.'
# Replace the pipeline inspect-and-judge items with excerpts for THIS concept.
for tile in d['tiles']:
 for ent in tile['interactions']:
  ix=ent['interaction']
  if ix['type']!='classify' or ix['measures'][0]['concept_id']!='mle.preprocessing_pipeline':continue
  examples=[
  ('composition','''numeric = Pipeline([("imputer", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())])
pre = ColumnTransformer([("distance", numeric, ["distance"]), ("zone", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["zone"])])
workflow = Pipeline([("pre", pre), ("estimator", FixtureEstimator())])
workflow.fit(X_train, y_train)
validation_predictions = workflow.predict(X_validation)
inference_predictions = workflow.predict(one_inference_row)''','meets','Column-specific transforms and the final estimator are composed and fitted only on training, then reused for both prediction paths.'),
  ('refit','''workflow.fit(X_train, y_train)
workflow.fit(X_validation, y_validation)
validation_predictions = workflow.predict(X_validation)''','violates','The second fit replaces training-fitted state using held-out rows.'),
  ('separate','''workflow.fit(X_train, y_train)
validation_pre = clone(workflow.named_steps["pre"])
representation = validation_pre.fit_transform(X_validation)
validation_predictions = workflow.named_steps["estimator"].predict(representation)''','violates','Validation preprocessing is fitted separately rather than reusing the composed training-fitted workflow.'),
  ('state','''saved_statistics = imputer.statistics_.copy()
saved_mean = scaler.mean_.copy()
saved_scale = scaler.scale_.copy()
saved_categories = encoder.categories_[0].copy()
workflow.predict(X_validation)
workflow.predict(one_inference_row)
assert np.array_equal(saved_statistics, imputer.statistics_)
assert np.array_equal(saved_mean, scaler.mean_)
assert np.array_equal(saved_scale, scaler.scale_)
assert np.array_equal(saved_categories, encoder.categories_[0])''','meets','The assertions check unchanged fitted preprocessing state after validation and bounded inference.'),
  ('missing','''# Training distances: 2, 4, 6; numerical pipeline: mean imputer, then StandardScaler.
# Validation distances: 8 and missing.
observed = workflow.named_steps["pre"].transform(X_validation)
assert np.allclose(observed[:, 0], (np.array([8, 4]) - np.mean([2, 4, 6])) / np.std([2, 4, 6], ddof=0))
assert observed[1, 0] == 0''','meets','The missing validation distance is replaced by the training mean and then centered to zero; the same stored representation is inspected.'),
  ('missing_bad','''# Same training distances 2,4,6 and validation distances 8,missing.
expected_missing_distance = 8
# Justification: fit the replacement on the observed validation distance.''','violates','The missing value must use the training-fitted replacement, not the validation mean.'),
  ('malformed','''# Required numerical distance and categorical zone columns.
try:
    workflow.predict(pd.DataFrame([{"distance": 8}]))
except ValueError:
    malformed_rejected = True
assert malformed_rejected''','meets','The declared missing-column failure is explicitly verified.'),
  ('bad_check','''saved_mean = scaler.mean_.copy()
workflow.predict(X_validation)
assert len(X_validation) == len(validation_predictions)
# This is the only claimed proof that preprocessing state was preserved.''','violates','Matching row counts does not check unchanged parameters or the declared representations.'),
  ('predictions','''representation = workflow.named_steps["pre"].transform(X_validation)
validation_predictions = workflow.predict(X_validation)
assert np.array_equal(validation_predictions, workflow.named_steps["estimator"].predict(representation))''','meets','The check verifies that composed predictions use the inspected training-fitted preprocessing representation.')]
  ix['public']={'prompt':'Read each independent workflow excerpt and decide whether it meets or violates its stated criterion: numerical mean imputation/scaling and categorical encoding composed with the final supplied estimator; training-only fitting; validation and bounded-inference reuse; asserted expected representation, prediction, missing/malformed outcomes and unchanged fitted preprocessing state. Judge only the evidence shown. The task requires distance and zone; missing distance is allowed via mean imputation, missing zone COLUMN is malformed.','buckets':[{'bucket_id':'meets','label':'Meets its stated criterion'},{'bucket_id':'violates','label':'Violates its stated criterion'}],'items':[{'item_id':i,'text':'```python\n'+text+'\n```'} for i,text,key,msg in examples]}
  ix['grading']={'assignments':{i:key for i,text,key,msg in examples},'item_feedback':{i:{'message':msg} for i,text,key,msg in examples}}
p.write_text(json.dumps(d,indent=2)+'\n')
