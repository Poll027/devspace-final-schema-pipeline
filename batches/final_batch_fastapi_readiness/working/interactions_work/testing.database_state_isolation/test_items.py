import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from application import app, engine, Item
from sqlalchemy.orm import Session
item = json.loads(Path('fixtures.json').read_text())['item']
# Initially sharing application state. Learner replaces this fixture by
# importing isolated_client from starter instead of this fixture.
@pytest.fixture
def isolated_client():
    with TestClient(app) as client:
        yield client, None
def test_writes_item(isolated_client):
    client, _ = isolated_client
    assert client.post('/items', json=item).json() == item
    assert client.get(f"/items/{item['id']}").json() == item
def test_item_absent(isolated_client):
    client, _ = isolated_client
    response = client.get(f"/items/{item['id']}")
    assert response.status_code == 404
    assert response.json() == {'detail':'Not found'}
