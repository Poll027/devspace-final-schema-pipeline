# Endpoint authorization with required permissions or scopes

Fictional order-service training workspace.

Wire the supplied order-modification operation to the permission provider and test sufficiently scoped success separately from missing-scope denial.

Install requirements.txt, run python prepare_credentials.py, then pytest test_permissions.py. The two controlled valid contexts use orders:write and no scopes respectively. These locally generated test credentials are only for this permission-boundary exercise, not authorization-server integration. HTTPBearer and PyJWT verification stay active. PATCH /orders/101 is already supplied; complete scope comparison and Security wiring only. Public success is 200 {"id":101,"status":"complete"}; missing scope is 403 {"detail":"Forbidden"}.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
