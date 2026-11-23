# Diagnose service failures from emitted and interpreted evidence

Fictional order-service training workspace.

Execute the supplied failing request once and record its status, interaction identifier, and supporting evidence before proposing a change.

Install requirements.txt and run python starter.py after completing it. application.py supplies POST /orders and client(). The configured lookup raises a deterministic TimeoutError and returns 504 with the configured X-Interaction-ID. No real network or SQL is executed. fixtures.json retains its authored synthetic provenance; its latency and SQL counts must not be reported as measurements from this reproduction. runtime_evidence records executed control-flow events and explicitly labels the simulated database boundary.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
