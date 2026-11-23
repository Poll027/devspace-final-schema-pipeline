import json, re, copy
from pathlib import Path
p = Path(__file__).parent / 'interactions.json'
d = json.loads(p.read_text())
before = copy.deepcopy(d)
entries = {e['step_id']: e['interaction'] for t in d['tiles'] for e in t['interactions']}
i = entries['mle.tile.052_055.s23']
i['public']['items'][0]['text'] = i['public']['items'][0]['text'].replace('Verify the recorded git commit', 'Check out the recorded commit, verify HEAD, and reject tracked working-tree differences.')
# Separate the requested replacement sentence from the unchanged retrieval action.
i['public']['items'][0]['text'] = i['public']['items'][0]['text'].replace('differences., retrieve', 'differences. Retrieve')
i['public']['items'][1]['text'] = '''Proposed execution and comparison:
# Define the rerun function with default arguments and explicit settings parameters; resolve defaults before execution.
# Invoke it with explicit keyword overrides carrying the unchanged recorded settings, working directory and environment.
# Run the recorded script in a clean subprocess using the verified working directory; require a zero exit status.
# In that directory, also capture the recorded invocation with shell redirection: <recorded invocation> > capture.log 2>&1
# Inspect capture.log for resolved settings, outcome and execution errors.
# Compare the rerun outcome with the recorded outcome under the supplied stochastic tolerances.
# From that same directory, demonstrate a pipe:
cat capture.log | grep validation_accuracy'''
i['feedback']['correct']['message'] = 'Correct. The Meets excerpts verify the recorded inputs, resolve function defaults, pass unchanged settings through explicit keyword overrides, require checked execution with a zero exit status, capture output with shell redirection, inspect capture.log, demonstrate a pipe and compare outcomes under the supplied stochastic tolerances.'
i['feedback']['incorrect']['message'] = 'Verify the recorded inputs and distinguish defaults and keyword overrides from notebook globals. Checked execution, shell redirection, inspection, a pipe and tolerance comparison are required; a matching dataset name or zero exit status alone does not establish reproduction.'
i = entries['mle.tile.058_058.s04']
i['public']['prompt'] = 'Import numpy as np and implement score_counts(TN, FP, FN, TP, policy). Compute actual_negatives and actual_positives, derive FPR and FNR with None for empty conditioning groups, and compute expected_error_cost from the fixed deployment probabilities and error costs, returning None when either required rate is undefined. Compare each defined quantity with its precommitted maximum; return None for each undefined requirement and report overall undefined, pass or fail without changing policy. Return the exact field names shown in the supplied comparison contract. Also replace the 24 count placeholders with sums of their matching masks. Leave frozen artifacts, masks, policy and report assembly unchanged.'
i['feedback']['hints'] = ['A True mask element contributes one observation to its confusion count; sum the matching mask', 'Use FP + TN for actual negatives and FN + TP for actual positives. An empty denominator makes its rate, and any dependent cost, undefined.']
pattern = r'def score_counts\(TN, FP, FN, TP, policy\):\n.*?(?=\n\n\n_masks)'
for file, starter in [(i['public']['workspace']['files'][0], True), (i['grading']['solution_files'][0], False)]:
    content = file['content']
    match = re.search(pattern, content, flags=re.S)
    assert match
    function = match.group()
    if starter:
        return_line = next(line for line in function.splitlines() if line.startswith('    return '))
        names = ['negatives', 'positives', 'FPR', 'FNR', 'expected_error_cost', 'FPR_requirement', 'FNR_requirement', 'cost_requirement', 'requirement_outcome']
        function = ('def score_counts(TN, FP, FN, TP, policy):\n'
                    '    # TODO: derive conditioning counts and rates; handle empty groups.\n'
                    '    # TODO: compute fixed-policy cost and requirement outcomes.\n' +
                    ''.join('    ' + name + ' = None\n' for name in names) +
                    '    # Supplied comparison contract: keep these returned field names.\n' + return_line + '\n')
    content = content[:match.start()] + content[match.end():]
    marker = 'exec(supplied_support)\n'
    assert content.count(marker) == 1
    content = content.replace(marker, marker + '\n# Learner section: implement this evaluation function.\n' + function + '\n')
    if starter:
        content = content.replace('# TODO: import numpy as np and replace each None with np.sum of the matching mask name.', '# TODO: import numpy as np and replace each count placeholder with np.sum of its matching mask.')
    file['content'] = content
# Ensure all unrelated interactions, grading keys/tests, anchors and constraints stayed unchanged.
for t, old_t in zip(d['tiles'], before['tiles']):
    for e, old_e in zip(t['interactions'], old_t['interactions']):
        if e['step_id'] not in ['mle.tile.052_055.s23', 'mle.tile.058_058.s04']:
            assert e == old_e
        else:
            new, old = e['interaction'], old_e['interaction']
            for key in ['type', 'measures', 'anchors', 'grading_mode', 'standalone']:
                assert new.get(key) == old.get(key)
            if new['type'] == 'classify':
                assert new['grading'] == old['grading']
            else:
                assert new['grading']['tests'] == old['grading']['tests']
                assert new['public']['constraints'] == old['public']['constraints']
p.write_text(json.dumps(d, indent=2) + '\n')
print('Patched 2 interactions; total interactions:', sum(len(t['interactions']) for t in d['tiles']))
