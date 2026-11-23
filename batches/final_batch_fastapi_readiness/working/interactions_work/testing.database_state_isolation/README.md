# Database test-state isolation

Fictional order-service training workspace.

Complete the transaction fixture for the supplied application and run both supplied test orders, including failure-path cleanup.

Install requirements.txt. test_items.py initially has a shared-state client; replace that fixture with `from starter import isolated_client`. Complete only starter.py transaction isolation/teardown. Run python run_orders.py (it executes both orderings even when the first fails), then python check_failure_cleanup.py on a clean database. Schema is prepared when application.py loads, outside any test transaction. Requests commit normally, so the test Session must use join_transaction_mode="create_savepoint" on the shared outer-transaction connection. Restore overrides in a finally block even after exceptions.

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
