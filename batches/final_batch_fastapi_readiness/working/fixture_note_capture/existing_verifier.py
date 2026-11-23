import jwt
from jwt import PyJWKClient
from fastapi import HTTPException
class ExistingVerifier:
    def __init__(self):self.configuration=None;self.jwks=None
    def configure(self,configuration):
        self.configuration=configuration
        self.jwks=PyJWKClient(configuration['jwks_url'])
    def verify(self,token):
        if self.configuration is None:raise HTTPException(503,'Integration settings incomplete')
        c=self.configuration
        try:
            signing_key=self.jwks.get_signing_key_from_jwt(token)
            return jwt.decode(token,signing_key.key,algorithms=c['algorithms'],issuer=c['issuer'],audience=c['audience'],options={'require':c['required_claims']})
        except jwt.PyJWTError:
            raise HTTPException(401,'Invalid access token')
