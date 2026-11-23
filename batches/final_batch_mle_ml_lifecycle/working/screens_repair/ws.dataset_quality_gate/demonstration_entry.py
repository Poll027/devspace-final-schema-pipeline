import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())

case = load('fixtures/dataset_cases.json')[sys.argv[1]]
contract = load('fixtures/dataset_contract.json')
rows = case['rows']
def number(x): return not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(x)
checks = {
 'schema': all(set(r)==set(contract['columns']) for r in rows),
 'feature_values': all(number(r.get('feature')) and 0 <= r['feature'] <= 5 for r in rows),
 'label_values': all(type(r.get('label')) is int and r['label'] in (0,1) for r in rows),
 'unique_sample_id': all(isinstance(r.get('sample_id'),str) and r['sample_id'] for r in rows) and len({r.get('sample_id') for r in rows})==len(rows)
}
failed = [k for k in contract['required_checks'] if not checks.get(k,False)]
print(json.dumps({'snapshot_id':case['snapshot_id'],'recorded_sha256':case['sha256'],'named_checks':checks,'failed_checks':failed}))
sys.exit(bool(failed))
