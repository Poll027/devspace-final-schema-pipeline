# Bounded retry decisions respecting HTTP idempotency

Fictional order-service training workspace.

Configure the supplied adapter using its documented policy fields and run the supplied retry-safety and timing checks.

Install requirements.txt; run the four run_*.py scripts after completing starter.py. adapter.py wraps maintained Tenacity Retrying (https://tenacity.readthedocs.io/). Its exact policy interface: retryable_failures = list of names from controlled_failures.json; max_attempts = inclusive integer attempt cap; total_time_budget = seconds including scripted operation duration and delay; retry_after = Boolean enabling both delta-seconds and HTTP-date; bounded_backoff = maximum client-only backoff seconds; retry_safe = Boolean allowing retries only where the supplied operation contract is idempotent or known_not_applied. Fill numeric budgets from fixtures.json, not new domain assumptions. ScriptedTransport injects concretely classified failures rather than claiming observed network outcomes. Clock.sleep advances virtual time deterministically. Retry-After delays are never clipped to the client cap: a delay that cannot fit stops repetition. GET may retry under the supplied contract; unsafe POST must make one attempt only. Terminal classifications stop immediately. The maintained engine implementation is supplied, not learner work.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
