import json, sys, math, hashlib
from pathlib import Path
load = lambda p: json.loads(Path(p).read_text())

cases=load('fixtures/release_cases.json'); c=cases[sys.argv[1]]; contract=load('fixtures/release_contract.json')
def cost(c):
 fpr=c['FP']/(c['FP']+c['TN']); fnr=c['FN']/(c['FN']+c['TP'])
 return fpr*contract['costs']['cost_FP']*contract['probabilities']['P(Y=0)']+fnr*contract['costs']['cost_FN']*contract['probabilities']['P(Y=1)']
value=cost(c); reference=cost(cases[contract['accepted_reference']])
checks={'all_evidence_present':all(k in c and c[k] is not None for k in cases[contract['accepted_reference']]),
 'nonnegative_integer_counts':all(type(c[k]) is int and c[k]>=0 for k in ('FP','TN','FN','TP')),
 'negative_denominator_nonempty':c['FP']+c['TN']>0,'positive_denominator_nonempty':c['FN']+c['TP']>0,
 'candidate_identity_matches_event':c['candidate_id']==sys.argv[2],
 'cost_within_fixed_maximum':value<=contract['max_expected_error_cost'], 'cost_not_worse_than_reference':value<=reference,
 'latency_within_fixed_maximum':c['latency_ms']<=contract['max_latency_ms'],
 'operating_ok':c['operating_ok'] is True,'evidence_complete':c['evidence_complete'] is True}
print(json.dumps({'candidate':c,'expected_error_cost':value,'reference_cost':reference,
 'fixed_cost_limit':contract['max_expected_error_cost'],'fixed_latency_limit_ms':contract['max_latency_ms'],
 'probabilities':contract['probabilities'],'costs':contract['costs'],'predicates':checks,'failed_predicates':[k for k,v in checks.items() if not v]}))
sys.exit(not all(checks.values()))
