import json
from pathlib import Path
p=Path('batches/final_batch_mle.region.data_readiness/interactions.json');d=json.loads(p.read_text());ix={x['step_id'].replace('mle.tile.',''):x['interaction'] for t in d['tiles'] for x in t['interactions']}
todos={
'001_003.s05':['Inspect rank before indexing axes; reject invalid rank, batch, or width.','Expose inspection variables for the accepted array.','Assert valid and boundary acceptance; assert each supplied invalid fixture raises ValueError.'],
'001_003.s10':['Cast each candidate independently from a.','Check every scalar difference against tolerance; compute count, itemsize, element_bytes, and nbytes.','Build candidate-ordered reports and the last-accepted choice; set both result variables.'],
'001_003.s16':['Subtract feature references; independently build the two-feature list-comprehension reference.','Assert intended shape and check agreement using the supplied explicit rtol and atol.'],
'004_006.s11':['Calculate the row limit including all features and element width.','Iterate typed chunks inside the open-file block and verify actual element bytes and budget.','Return row_limit, chunk_rows, total_rows, largest_element_bytes, and the declared scope.'],
'004_006.s16':['Build the declared readiness dictionary from the observed columns, shape, dtype, and element bytes.','Compute feature-wise means and std over rows with the supplied ddof.'],
'007_008.s05':['Check exact columns, declared types, inclusive distance bounds, and permitted zones in that order.','Assert the expected verdict for every fixture, including both boundaries and each failure.'],
'007_008.s10':['Use accepted keys and policy-driven reject, repeat, and repair branches; preserve source records.','Assert valid and boundary retention, repaired spelling, invalid-distance rejection, repeat rejection, and action ordering.','Catch the deliberately false assertion and expose false_assertion_caught.'],
'009_011.s11':['Detect repeats before dictionary replacement; align by ID and compute missing and orphan sets.','Report invalid, misaligned, and unavailable IDs in the specified order.','Assert valid and reordered acceptance; each duplicate, missing, orphan, invalid, misaligned, and unavailable failure; and inclusive-cutoff acceptance.'],
'009_011.s16':['Implement both scenarios, preserve source order, and calculate both target proportions.','Assert disjoint groups and time inequalities, including cutoff equality and the invalid assignment.'],
'012_015.s05':['Fit the supplied imputer on training only; transform held-out fixtures without refitting.','Compute observed-training column means and population std.','Assert expected outputs and unchanged fitted statistics; catch the deliberately incorrect replacement assertion.'],
'012_015.s11':['Fit the supplied scaler on training only and transform both inputs.','Calculate training column means and population std.','Assert validation arithmetic under saved parameters, constant-feature scale 1, unchanged state, and failure of the wrong-output assertion.'],
'012_015.s16':['Fit the supplied encoder once on training and build the zone dictionary from categories_.','Transform known, unseen, and missing cases under each declared policy; record ValueError as that string.','Assert aligned indicators, width, and unchanged mapping for ignore, error, and missing-seen-at-fit fixtures.'],
'016_017.s05':['Project permitted fields; fit projected training only; transform and predict projected held-out inputs once.','Build leaked and corrected trace dictionaries and apply each pinned invariant to both.'],
'016_017.s11':['Filter by inclusive available_at boundary with a list comprehension; initialize total=0 and accumulate only accepted values.','Assert the original total, later-record invariance, empty total, and exact-boundary inclusion.'],
'018_018.s05':['Read through read_sample; retain original values only for permitted dictionary keys.','Set result and secret_used using the authorized interfaces without copying the credential.','Assert permitted values and restricted-field absence; assert unauthorized access raises PermissionError.']}
for k,lines in todos.items():
 i=ix[k];s=i['public']['workspace']['files'][0]['content'];s=s.replace('# Implement the operations and return fields in the prompt.','\n'.join('# TODO: '+line for line in lines));i['public']['workspace']['files'][0]['content']=s
# Restore the audit's supplied result binding (not implementation or assertions).
i=ix['009_011.s11'];s=i['public']['workspace']['files'][0]['content'];s=s.replace('# TODO: Calculate and expose result, case_results.','result = audit(observations, labels, contract)\n# TODO: Calculate case_results for the supplied cases.');i['public']['workspace']['files'][0]['content']=s
# Remove obsolete harness-implementation wording; invariants are learner-authored.
i=ix['016_017.s05'];i['public']['prompt']=i['public']['prompt'].replace('Write the same trace/feature assertions that the harness applies to the deliberately leaked and corrected workflows;','Write the same trace/feature assertions for the deliberately leaked and corrected workflows;')
# Checks in reference solutions illustrate the required authored assertions without changing any tests/keys.
i=ix['007_008.s10'];sol=i['grading']['solution_files'][0]['content'];mark='# Supplied grading adapter; do not change it.'
checks='''assert records[1]["zone"] != result["cleaned"][1]["zone"]
assert result["cleaned"][2]["observation_id"] == records[2]["observation_id"]
assert records[3]["observation_id"] not in [r["observation_id"] for r in result["cleaned"]]
assert records[4]["observation_id"] not in [r["observation_id"] for r in result["cleaned"]]
assert [r["action"] for r in result["report"]] == ["repaired", "rejected", "rejected_repeat"]
''';sol=sol.replace(mark,checks+'\n'+mark);i['grading']['solution_files'][0]['content']=sol
i=ix['009_011.s11'];sol=i['grading']['solution_files'][0]['content'];checks='''reordered_labels = labels[::-1]
assert audit(observations, reordered_labels, contract)["accepted"]
# The original valid fixture includes availability equal to the cutoff.
assert audit(observations, labels, contract)["accepted"]
''';i['grading']['solution_files'][0]['content']=sol.replace(mark,checks+'\n'+mark)
i=ix['016_017.s11'];sol=i['grading']['solution_files'][0]['content'];sol=sol.replace('assert result == augmented_result','assert result == sum([row["value"] for row in records])\nassert result == augmented_result');i['grading']['solution_files'][0]['content']=sol
p.write_text(json.dumps(d,indent=2)+'\n')
