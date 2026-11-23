# Object-level authorization against the authenticated principal

Fictional order-service training workspace.

Add the trusted-owner predicate, then verify both own-order successes and both cross-owner denials through the supplied endpoint without changing either order.

Install requirements.txt and run pytest test_ownership.py. Only trusted_principal is substituted by caller_a/caller_b; caller input cannot select an owner. Explicit unavailable contract is fixtures.json unavailable_object (404 {"detail":"Not found"}). The four supplied pairs each use a fresh seeded in-memory database. Complete the query predicate in starter.py and the HTTP assertions, including database snapshots for unchanged orders.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
