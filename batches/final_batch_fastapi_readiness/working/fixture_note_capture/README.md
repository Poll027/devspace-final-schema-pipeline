# Inspecting generated OpenAPI for drift and sensitive exposure

Fictional order-service training workspace.

Audit the supplied orders router against its models, supplied HTTP evidence, and established security configuration; record declaration drift without adding authentication tests.

http_evidence.json, generated_schema.json and security_configuration.json are bundled outputs of an executed capture.py run; capture_runtime.json records the actual runtime versions. Install requirements.txt and rerun python capture.py if sources change, then run python run_audit.py. Capture records actual non-authentication TestClient outcomes and source hashes, not typed expected code output. The orders router deliberately declares duplicate status 409 while emitting 400; the audit is unfinished in starter.py. Public output excludes owner_id. Compare generated security declarations with this supplied established configuration; do not add authentication or authorization tests to this audit.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
