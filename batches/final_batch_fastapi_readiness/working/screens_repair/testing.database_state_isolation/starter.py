import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from application import app, engine, session_provider
@pytest.fixture
def isolated_client():
    original = app.dependency_overrides.copy()
    connection = engine.connect()
    outer = connection.begin()
    test_session = Session(bind=connection,
                           join_transaction_mode='create_savepoint')
    def test_provider():
        yield test_session
    app.dependency_overrides[session_provider] = test_provider
    try:
        with TestClient(app) as client:
            yield client, test_session
    finally:
        try:
            test_session.close()
        finally:
            try:
                outer.rollback()
            finally:
                try:
                    connection.close()
                finally:
                    app.dependency_overrides.clear()
                    app.dependency_overrides.update(original)
