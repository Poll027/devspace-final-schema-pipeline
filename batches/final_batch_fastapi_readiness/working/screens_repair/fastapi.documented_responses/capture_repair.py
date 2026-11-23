import json
from pathlib import Path
fixtures=json.loads(Path("fixtures.json").read_text())
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.testclient import TestClient
class PublicModel(BaseModel):
    id: int
    status: str
class ConflictModel(BaseModel):
    detail: str
app = FastAPI()
@app.post('/orders', response_model=PublicModel,
          status_code=fixtures['success_status'],
          response_description='The public order state',
          responses={fixtures['conflict_status']: {
              'model': ConflictModel,
              'description': 'The requested order conflicts'}})
def create_order(conflict: bool = False):
    if conflict:
        raise HTTPException(status_code=fixtures['conflict_status'],
                            detail=fixtures['conflict_body']['detail'])
    return fixtures['success_body']
schema=app.openapi()
print(json.dumps({"responses": {str(status):schema["paths"]["/orders"]["post"]["responses"][str(status)] for status in (fixtures["success_status"], fixtures["conflict_status"])}, "components": {"schemas": {name:schema["components"]["schemas"][name] for name in ("PublicModel","ConflictModel")}}}, indent=2))
