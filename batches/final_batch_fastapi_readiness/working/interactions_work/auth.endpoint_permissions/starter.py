from fastapi import Depends, HTTPException
from fastapi.security import SecurityScopes
from security import verified_token_context
# Active verification remains a dependency, not a plain unbound parameter.
def require_permissions(security_scopes: SecurityScopes,
                        verified_context=Depends(verified_token_context)):
    # TODO: compare all security_scopes.scopes to verified_context['scopes'].
    # Deny missing permission with 403 {"detail":"Forbidden"}.
    raise NotImplementedError('Complete permission comparison')
# Wire Security(provider, scopes=['orders:write']) for the supplied order-modification operation.
