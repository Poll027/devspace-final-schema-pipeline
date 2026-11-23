# Upstream failure translation

Fictional order-service training workspace.

Provide an async integration function with a supplied HTTPX client, a fixed upstream URL, and an incomplete failure-translation block. Supply the contract: upstream 503 becomes local 502 with detail 'Upstream unavailable'; an upstream timeout becomes local 504 with detail 'Upstream timed out'; other unsuccessful statuses and transport failures use the supplied local 502 fallback. Provide endpoint test scaffolding and dependency replacements for the two required failures.

Starter code is deliberately incomplete; not a completed solution. See glossary_contract.json for exact sourced teaching and observable success. See provisioning.json for runtime or publisher/issuer prerequisites not present in the glossary. Do not treat authored evidence packets as captured code output. No hypothetical issuer may stand in for actual issuer integration.
