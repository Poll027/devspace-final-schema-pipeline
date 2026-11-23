from fastapi import Depends, Security
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
# TODO: declare the supplied bearer presentation scheme.
bearer_scheme = None
def authorization_code_scheme(issuer_configuration):
    # TODO: supplied authorization/token URLs and permission descriptions.
    raise NotImplementedError('Complete security declarations')
# TODO: add scheme/scopes to each operation while keeping read_orders and
# write_orders enforcement dependencies unchanged. See fixtures.json.
