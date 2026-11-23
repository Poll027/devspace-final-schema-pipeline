# Bounding payloads, expensive requests and API resource consumption

Fictional order-service training workspace.

Apply the supplied byte, batch, timeout, and concurrency budgets to the supplied endpoint, then verify accepted and rejected requests.

POST /orders/batch returns 200 {"accepted": <batch length>}. Batch overflow uses Pydantic validation (422). beyond_body is raw JSON with one valid item and padding exceeding the byte budget; beyond_batch stays a separate four-item case. HTTPX outbound_timeout must become httpx.Timeout(budgets["dependency_timeout_seconds"]), and launch.sh must use the supplied --limit-concurrency. The unmodified maintained Starlette wheel is bundled as base64 under vendor/. Run python install_middleware.py, then install requirements.txt. The integration point is application.py: import RequestBodyLimitMiddleware from starlette.middleware.body_limit and call app.add_middleware with max_body_size from the body_bytes budget before serving requests. middleware_verification.json records the inspected constructor interface and executed supplier check. With that budget, beyond_body returns 413 with Content-Type text/plain; charset=utf-8 and exact response text "Content Too Large"; the counted dependency runs 0 times. These are supplier observations, not completed learner assertions. Leave the byte, batch, timeout and concurrency configuration and test assertions for the learner.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
