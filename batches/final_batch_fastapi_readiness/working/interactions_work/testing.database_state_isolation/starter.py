import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from application import app, engine, session_provider
@pytest.fixture
def isolated_client():
    original_overrides = app.dependency_overrides.copy()
    connection = engine.connect()
    outer_transaction = connection.begin()
    # TODO: bind Session with join_transaction_mode="create_savepoint".
    test_session = None
    # TODO: override session_provider with a yield provider using test_session.
    try:
        with TestClient(app) as client:
            yield client, test_session
    finally:
        # TODO: close session, roll back outer transaction, close connection,
        # restore original_overrides even if the test fails.
        pass
# TODO: test write/read within one boundary; test target absence in another.
# Run both execution orders. Never migrate/create schema inside per-test transaction.
