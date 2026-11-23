from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient
class PublicModel(BaseModel):
    id: int
    status: str
class ConflictModel(BaseModel):
    detail: str
app = FastAPI()
# TODO: complete only response documentation, preserving the outcome implementation.
@app.post('/orders')
def create_order(conflict: bool = False):
    if conflict:
        raise HTTPException(status_code=409, detail='Order conflict')
    return {'id': 101, 'status': 'pending'}
with TestClient(app) as client:
    success = client.post('/orders')
    conflict = client.post('/orders?conflict=true')
    schema = app.openapi()
    # TODO: compare actual responses with generated entries and schemas.
