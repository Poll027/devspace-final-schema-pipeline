import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from application import app, fixtures
@pytest.mark.parametrize('case',fixtures['cases'],ids=lambda c:c['credential_condition'])
def test_order_gate(case):
    bearer_fixtures=json.loads(Path('bearer_fixtures.json').read_text())
    with TestClient(app) as client:
        # TODO: send bearer_fixtures[case['credential_condition']] as headers
        # to GET /orders/{requested_order_id}; assert exact declared_status and
        # json.loads(case['safe_body_or_public_result']). No dependency overrides.
        pass
