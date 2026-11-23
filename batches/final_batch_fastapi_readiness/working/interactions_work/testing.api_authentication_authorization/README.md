# Authentication and authorization tests including invalid-token rejection

Fictional order-service training workspace.

Send each supplied credential condition through the protected endpoint and assert its exact denial contract or public result; do not override extraction or verification.

Install requirements.txt, run python prepare_credentials.py, then pytest starter.py. The acquisition script generates controlled test credentials, including genuinely bad signatures and separately expired, wrong-issuer and wrong-audience tokens. It writes bearer_fixtures.json, indexed by each existing matrix condition. These local signed test tokens are not authorization-server credentials. All HTTP gates are active in application.py/security.py. Preserve every existing matrix answer contract and test each row independently.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
