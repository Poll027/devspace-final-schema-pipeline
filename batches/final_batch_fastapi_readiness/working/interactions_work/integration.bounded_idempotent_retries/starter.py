import json
from pathlib import Path
contract = json.loads(Path('fixtures.json').read_text())
policy = {'retryable_failures':None,'max_attempts':None,'total_time_budget':None,
          'retry_after':None,'bounded_backoff':None,'retry_safe':None}
# TODO: complete policy for the provisioned maintained adapter. Respect both
# Retry-After forms. Timeout/lost response alone never proves no remote effect.
# Test transient-then-success, exhausted budget and unsafe non-idempotent case.
