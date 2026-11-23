from application import app, fixtures, trusted_principal, caller_a, caller_b, Sessions, Order
from fastapi.testclient import TestClient
from sqlalchemy import select
import pytest
@pytest.mark.parametrize('caller,order_id',fixtures['pairs'])
def test_pair(caller,order_id):
    original=app.dependency_overrides.copy()
    app.dependency_overrides[trusted_principal]={'caller_a':caller_a,'caller_b':caller_b}[caller]
    try:
        with TestClient(app) as client:
            response=client.get(f'/orders/{order_id}')
            # TODO: both own successes and both cross-owner unavailable results.
            # Read the database through client.portal.call(snapshot) and assert
            # every id, owner_id and status equals fixtures['orders'].
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original)
async def snapshot():
    async with Sessions() as session:
        rows=(await session.scalars(select(Order).order_by(Order.id))).all()
        return [{'id':row.id,'owner_id':row.owner_id,'status':row.status} for row in rows]
