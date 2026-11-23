import json
from pathlib import Path
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from existing_verifier import ExistingVerifier
configuration=json.loads(Path('issuer_configuration.json').read_text())
existing_verifier=ExistingVerifier();existing_verifier.configure(configuration)
extraction=HTTPBearer(auto_error=False)
async def authenticated(request:Request):
    credential=await extraction(request)
    if credential is None:raise HTTPException(401,'Bearer token required')
    return existing_verifier.verify(credential.credentials)
def enforce_permission(principal,required):
    if required not in principal.get('scope','').split():raise HTTPException(403,'Permission required')
    return principal
from fastapi import Depends
def read_orders(principal=Depends(authenticated)):
    return enforce_permission(principal,'orders:read')
def write_orders(principal=Depends(authenticated)):
    return enforce_permission(principal,'orders:write')
