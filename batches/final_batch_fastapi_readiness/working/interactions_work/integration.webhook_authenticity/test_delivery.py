from scaffold import client, config, raw_body, processed_events
import pytest
@pytest.fixture(autouse=True)
def clear_recorder():
    processed_events.clear()
@pytest.mark.parametrize('condition', ['valid', 'modified', 'absent'])
def test_delivery(condition):
    body = raw_body if condition != 'modified' else raw_body + b' '
    headers = {} if condition == 'absent' else {config['signature_header']: config['signature']}
    with client() as http:
        # TODO: http.post('/webhook', content=body, headers=headers).
        # Assert exact status/body and recorder length (one only for valid).
        raise NotImplementedError('Complete this delivery test')
