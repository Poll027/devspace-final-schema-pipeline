import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())

c=load('fixtures/promotion_cases.json')[sys.argv[1]]; stage=sys.argv[2]; r=load('fixtures/registry.json')[c['registry_version']]
identity=(c['artifact_id']==r['artifact_id']==c['staged_artifact_id']==c['approval']['artifact_id'] and c['run_id']==r['run_id'] and c['registry_version']==c['approval']['registry_version'])
checks={'compatibility':c['compatibility_ok'], 'offline_validation':c['offline_validation_ok'],
 'staged_validation':c['staged_validation_ok'] and identity,
 'authorization':c['approval']['authorized'] and identity and bool(c['approval']['accountable_identity'])}
passed={'compatibility':checks['compatibility'], 'staging_quality':checks['offline_validation'] and checks['staged_validation'], 'authorization':checks['authorization']}[stage]
print(json.dumps({'stage':stage,'passed':passed,'immutable_artifact_reference':r,
 'promotion_record':{**{k:c[k] for k in ('approval','registry_version','run_id','artifact_id')},'accountable_identity':c['approval']['accountable_identity'],'per_stage_results':checks}}))
sys.exit(not passed)
