import json
from pathlib import Path
import application
from fastapi.testclient import TestClient
import pytest
fixtures = json.loads(Path('fixtures.json').read_text())
@pytest.mark.parametrize('condition', ['within_batch','beyond_batch','within_body','beyond_body'])
def test_boundary(condition):
    calls = []
    async def counted(value: application.BatchInput):
        calls.append(True)
        return True
    previous = application.app.dependency_overrides.copy()
    application.app.dependency_overrides[application.expensive_dependency] = counted
    try:
        with TestClient(application.app) as client:
            if condition == 'beyond_body':
                response = client.post('/orders/batch', content=fixtures[condition], headers={'Content-Type':'application/json'})
            else:
                response = client.post('/orders/batch', json=fixtures[condition])
            # TODO: assert exact accepted contract or independent byte/batch
            # rejection, plus counted invocation for accepted requests only.
    finally:
        application.app.dependency_overrides.clear()
        application.app.dependency_overrides.update(previous)
