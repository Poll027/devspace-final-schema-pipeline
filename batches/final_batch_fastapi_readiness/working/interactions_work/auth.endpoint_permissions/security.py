import json
from pathlib import Path
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
config=json.loads(Path('test_trust.json').read_text())
bearer=HTTPBearer(auto_error=False)
def verified_token_context(credentials=Depends(bearer)):
    if credentials is None or credentials.scheme.lower()!='bearer':
        raise HTTPException(401,'Not authenticated')
    try:
        claims=jwt.decode(credentials.credentials,config['test_key'],algorithms=['HS256'],
                          issuer=config['issuer'],audience=config['audience'],
                          options={'require':['exp','iss','aud','sub']})
        return {'owner_id':claims['sub'],'scopes':claims.get('scope','').split()}
    except jwt.InvalidTokenError:
        raise HTTPException(401,'Not authenticated')
