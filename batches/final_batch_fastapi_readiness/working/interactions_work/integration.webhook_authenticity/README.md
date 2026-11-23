# Webhook authenticity verification

Fictional order-service training workspace.

Use the supplied publisher verifier and signed fixture; complete the verification gate and three delivery tests.

Install requirements.txt, then run pytest test_delivery.py. Stripe signing contract: Stripe-Signature contains t=<timestamp>,v1=<HMAC-SHA256>; the signed message is ASCII timestamp + dot + exact raw body. The configured whsec_ value is a generated test-only endpoint secret, not a live publisher credential. The fixture was signed by the repair script using that documented contract; scaffold.py validates it using Stripe Webhook.construct_event. tolerance=0 is solely for a durable teaching snapshot, not a production freshness setting. Production must retain the SDK default tolerance. Never reserialize the body before verification. Public rejection: 400 {"detail":"Invalid signature"}; success: 200 {"received":true}. Source: https://docs.stripe.com/webhooks/signature .

See glossary_contract.json for the sourced teaching contract. Supplied test data are fictional, not production data.
