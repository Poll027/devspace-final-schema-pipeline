import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())

import numpy as np
from prediction_package import FittedPackage, InputContractError
execution = load('fixtures/behavior_execution_cases.json')[sys.argv[1]]
package = FittedPackage(execution['regression'])
contract = load('fixtures/behavior_contract.json')
results = {}
for name, case in load('fixtures/behavior_cases.json').items():
 if 'expected_exception' in case:
  try: package.predict(case['inputs'])
  except InputContractError as e: results[name]={'required_rejection':True,'exception':type(e).__name__}
  else: results[name]={'required_rejection':False}
  continue
 actual = package.predict(case['inputs'])
 expected = np.array(case['expected_values']).reshape(case['expected_shape'])
 shape_ok = list(actual['values'].shape)==case['expected_shape']
 checks={'row_count':len(actual['values'])==len(case['expected_sample_ids']),
 'correspondence':actual['sample_ids']==case['expected_sample_ids'], 'shape':shape_ok}
 structural_ok = all(checks.values())
 comparison = {'rtol':contract['rtol'],'atol':contract['atol'], 'executed_after_structure_pass':structural_ok}
 if structural_ok:
  try: np.testing.assert_allclose(actual['values'],expected,rtol=contract['rtol'],atol=contract['atol'])
  except AssertionError: comparison['allclose']=False
  else: comparison['allclose']=True
  comparison['absolute_error']=np.abs(actual['values']-expected).tolist()
  comparison['allowed_error']=(contract['atol']+contract['rtol']*np.abs(expected)).tolist()
 else: comparison['not_executed_reason']='structural check failed; values cannot substitute for correspondence'
 results[name]={'actual_row_count':len(actual['values']), 'expected_row_count':len(case['expected_sample_ids']),
 'actual_sample_ids':actual['sample_ids'],'expected_sample_ids':case['expected_sample_ids'],
 'actual_shape':list(actual['values'].shape),'expected_shape':case['expected_shape'],'checks':checks,'tolerance_comparison':comparison}
passed=all(r.get('required_rejection', all(r.get('checks',{}).values()) and r.get('tolerance_comparison',{}).get('allclose',False)) for r in results.values())
print(json.dumps({'execution':execution,'fixture_results':results,'passed':passed}))
sys.exit(not passed)
