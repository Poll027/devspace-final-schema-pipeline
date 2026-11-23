import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())

case=load('fixtures/dependency_cases.json')[sys.argv[1]]
stage=sys.argv[2]
if stage=='data_validation':
 result={'stage':stage, 'resolved_consumed':case[stage]['consumed'],'validation_ok':case[stage]['validation_ok']}
 passed=result['validation_ok']
else:
 result={'stage':stage,'training_produced':case['training']['produced'],'resolved_consumed':sys.argv[3],
 'dictionary_consumed':case[stage]['consumed'],'identity_matches':case['training']['produced']==sys.argv[3],
 'args_match_dictionary':sys.argv[3]==case[stage]['consumed'],'validation_ok':case[stage]['validation_ok']}
 passed=result['identity_matches'] and result['args_match_dictionary'] and result['validation_ok']
print(json.dumps(result)); sys.exit(not passed)
