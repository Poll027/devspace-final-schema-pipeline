from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
from existing_verifier import ExistingVerifier
app=FastAPI()
bearer=HTTPBearer(auto_error=False)
existing_verifier=ExistingVerifier()
def authenticated(credential=Depends(bearer)):
    if credential is None:raise HTTPException(401,'Bearer token required')
    return existing_verifier.verify(credential.credentials)
@app.get('/protected')
def protected(principal=Depends(authenticated)):
    return {'subject':principal['sub']}
