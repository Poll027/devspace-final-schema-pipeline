import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from application import app, order, fixtures
@pytest.mark.parametrize('condition',['verified_with_permission','verified_without_permission'])
def test_modify(condition):
    tokens=json.loads(Path('bearer_fixtures.json').read_text())
    order.update({key:fixtures['order'][key] for key in ['id','status']})
    with TestClient(app) as client:
        response=client.patch('/orders/'+str(fixtures['order']['id']),json=fixtures['modification'],
                              headers={'Authorization':'Bearer '+tokens[condition]})
        # TODO: assert 200/public result for sufficiently scoped context;
        # separately 403 {"detail":"Forbidden"} and unchanged order for no scope.
