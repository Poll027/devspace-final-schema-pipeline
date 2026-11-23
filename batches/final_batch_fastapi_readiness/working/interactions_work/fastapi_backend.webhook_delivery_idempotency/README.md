# Webhook delivery idempotency

Fictional order-service training workspace.

Complete the atomic handler and verify sequential duplicates, concurrent duplicates, retained records after restart, and rollback of both writes on failure.

Install requirements.txt. Complete handle_authenticated_event in starter.py and assertions in delivery_checks.py; run the four run_*.py runners. Each scenario uses a real temporary SQLite file; restart constructs a new application while retaining that same file. Every HTTP delivery has its own AsyncSession. Seeded orders are inserted only if absent. Unique publisher_event_id is enforced by the database. A request-local SQLAlchemy after_flush_postexec failure hook raises before commit; the failure scenario must show neither write persists. Controlled endpoint /authenticated-events intentionally starts after authenticity; this is not a public unsigned webhook. Suggested acknowledgement contract: 200 {"received":true} for completed processing and confirmed duplicates. Unrelated transaction errors must not be acknowledged as duplicates.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
