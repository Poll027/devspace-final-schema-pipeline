import json
from pathlib import Path
import sys
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers import pysyntax
b = Path('batches/final_batch_mle.region.reproducible_release')
p = b / 'interactions.json'
d = json.loads(p.read_text())
i = next(s['interaction'] for t in d['tiles'] for s in t['interactions'] if s['step_id'] == 'mle.tile.058_058.s04')
def walk(x):
    if isinstance(x, dict):
        yield x
        for v in x.values(): yield from walk(v)
    elif isinstance(x, list):
        for v in x: yield from walk(v)
g = json.loads((b/'inputs/path_glossary_bundle.json').read_text())
a = next(x['practice_anchor']['live_code'] for x in walk(g) if x.get('practice_anchor', {}).get('live_code', {}).get('allowed_syntax') == i['public']['constraints']['allowed_syntax'])
assert i['public']['constraints'] == {k:a[k] for k in ('allowed_syntax','blocked_syntax')}
old = i['grading']['solution_files'][0]['content']
infra, body = old.split('\nimport numpy as np\n', 1)
body = body.replace('np.sum(', 'count_errors(')
scaffold = infra + '\n# Supplied evaluation/reporting scaffold; leave unchanged.\nexec(' + repr(body) + ')\n\n'
starter = scaffold + '# TODO: import NumPy and bind count_errors to its Boolean-mask sum reducer.\ncount_errors = None\n'
solution = scaffold + 'import numpy as np\ncount_errors = np.sum\n'
i['public']['workspace']['files'][0]['content'] = starter
i['grading']['solution_files'][0]['content'] = solution
i['public']['prompt'] = ('Complete the reducer binding in evaluate_protected.py: import NumPy as np and replace count_errors = None with a binding of count_errors to np.sum (the function itself, not a call). The supplied evaluation scaffold calls your reducer on each TN, FP, FN and TP Boolean mask for frozen B and the baseline on the same protected rows. Leave all supplied scaffolding unchanged. evaluate_protected(policy, variant) returns selected_candidate unchanged and B and baseline dictionaries containing TN, FP, FN, TP, actual_negatives (FP+TN), actual_positives (FN+TP), FPR, FNR, expected_error_cost and requirement_outcome. The scaffold uses actual-class denominators, reports None for empty-group rates and dependent cost, and applies the fixed deployment probabilities, error costs and policy maxima. Outcomes are undefined for undefined rates, pass when all maxima are satisfied, and fail otherwise. Tests cover base, no_negatives and no_positives. Do not replace B, refit preprocessing, change thresholds or modify policy.')
viol, _, _ = pysyntax.judge(solution, a['allowed_syntax'], a['blocked_syntax'], starter)
assert not viol, viol
# Only the named interaction's starter, solution and prompt change; tests/constraints remain intact.
p.write_text(json.dumps(d, indent=2) + '\n')
print('Interactions:', sum(len(t['interactions']) for t in d['tiles']))
print('Patched one interaction; syntax gate passed.')
