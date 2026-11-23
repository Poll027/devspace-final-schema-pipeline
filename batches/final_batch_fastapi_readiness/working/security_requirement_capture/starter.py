import json
from pathlib import Path
from fastapi import Depends, Security
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
issuer_configuration=json.loads(Path('issuer_configuration.json').read_text())
bearer_scheme=HTTPBearer(scheme_name='OrderBearer')
code_scheme=OAuth2AuthorizationCodeBearer(
    authorizationUrl=issuer_configuration['authorization_url'],
    tokenUrl=issuer_configuration['token_url'],
    scopes=issuer_configuration['scopes'],scheme_name='OrderAuthorizationCode')

