import json
from pathlib import Path
cases=json.loads(Path('fixtures.json').read_text())['cases']
for case in cases:
    difference=case['receiver_now']-int(case['signed_delivery_timestamp'])
    accepted=(-case['future_tolerance'] <= difference <= case['acceptance_window'])
    print(f"{case['case_id']}: {difference}/{'accept' if accepted else 'reject'}")
