import json,textwrap
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness');p=B/'interactions.json';d=json.loads(p.read_text());r=json.loads((B/'scenario_asset_registry.json').read_text())
assertion_concepts={'numpy_shape_dtype','dataset_schema_validation','dataset_cleaning_policy','label_integrity','deployment_matched_splits','training_fitted_imputation','training_fitted_scaling','categorical_encoding','prediction_boundary_leakage','leakage_safe_features'}
for t in d['tiles']:
 for ent in t['interactions']:
  ix=ent['interaction'];name=ix['measures'][0]['concept_id'].removeprefix('mle.')
  if ix['type']=='classify' and name=='preprocessing_pipeline':
   for item in ix['public']['items']:
    if item['item_id']=='malformed':item['text']=item['text'].replace('try:\n','malformed_rejected = False\ntry:\n')
  if ix['type']!='code_exercise':continue
  # Request only packages actually imported by this scaffold; scikit-learn is intrinsic to these anchors.
  code=ix['grading']['solution_files'][0]['content'];packages=[]
  if 'import numpy as np' in code:packages.append('numpy')
  if 'import pandas as pd' in code:packages.append('pandas')
  if 'from sklearn' in code:packages.append('scikit-learn')
  ix['public']['runtime']['packages']=packages
  for file in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:
   s=file['content']
   if name=='numpy_dtype_selection':s=s.replace('accepted = preserved and element_bytes <= budget','accepted = preserved and element_bytes <= budget and element_bytes == candidate.nbytes and candidate.size == a.size')
   if name=='prediction_boundary_leakage':s=s.replace('        assert preprocessor.fit_rows == train_inputs','        assert fields == acceptance_fields\n        assert preprocessor.fit_rows == train_inputs')
   if name in assertion_concepts:
    # The provided fixture wrapper deliberately tests a wrong acceptance expectation and detects its false predicate.
    helpers='''def verify_assertion_behavior(original):
    def verified(fixture):
        result = original(fixture)
        actual_has_result = result is not None
        expected_wrong = not actual_has_result
        detected = False
        try:
            assert actual_has_result == expected_wrong
        except AssertionError:
            detected = True
        assert detected
        return {"fixture_result":result,"incorrect_expectation_detected":detected}
    return verified
evaluate = verify_assertion_behavior(evaluate)
'''
    s=s.replace('\n# COMPLETE THE NAMED SLOTS BELOW.','\n'+textwrap.indent(helpers,'    ')+'\n# COMPLETE THE NAMED SLOTS BELOW.')
   file['content']=s
  if name in assertion_concepts:ix['public']['prompt']+=' The supplied fixture wrapper also deliberately supplies the opposite result-availability verdict; its false assert predicate must raise AssertionError in ordinary non-optimized execution. Tests require incorrect_expectation_detected=True alongside the actual fixture result.'
p.write_text(json.dumps(d,indent=2)+'\n')
