import numpy as np
import yaml
from prediction_package import FittedPackage, InputContractError
from support import read, inspect_config, trigger_run, fixture_events, status, assertion_failure, rejection
def test_behavior(package, fixture, contract):
    if 'expected_exception' in fixture:
        try:
            package.predict(fixture['inputs'])
        except InputContractError:
            return {'rejected_input':True}
        raise AssertionError('expected InputContractError')
    output = package.predict(fixture['inputs'])
    assert len(output['sample_ids']) == len(fixture['inputs'])
    assert output['sample_ids'] == fixture['expected_sample_ids']
    assert list(output['values'].shape) == fixture['expected_shape']
    expected = np.array(fixture['expected_values']).reshape(fixture['expected_shape'])
    np.testing.assert_allclose(output['values'],expected,rtol=contract['rtol'],atol=contract['atol'])
    return {'sample_ids':output['sample_ids'],'values':output['values'].tolist(),'shape':list(output['values'].shape)}
def fatal_behavior(args):
    case=execution[args[-1]]
    return test_behavior(FittedPackage(case['regression']),cases[case['fixture_id']],contract)
