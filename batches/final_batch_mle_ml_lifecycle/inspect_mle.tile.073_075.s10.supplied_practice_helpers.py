# Supplied practice implementation. Read-only scaffolding.
def test_behavior(package, fixture, contract):
    if 'expected_exception' in fixture:
        try:
            package.predict(fixture['inputs'])
        except InputContractError:
            return {'rejected_input': True}
        raise AssertionError('expected InputContractError')
    output = package.predict(fixture['inputs'])
    assert len(output['sample_ids']) == len(fixture['inputs'])
    assert output['sample_ids'] == fixture['expected_sample_ids']
    assert list(output['values'].shape) == fixture['expected_shape']
    expected = np.array(fixture['expected_values']).reshape(fixture['expected_shape'])
    np.testing.assert_allclose(output['values'], expected, rtol=contract['rtol'], atol=contract['atol'])
    return {'sample_ids': output['sample_ids'], 'values': output['values'].tolist(), 'shape': list(output['values'].shape)}
