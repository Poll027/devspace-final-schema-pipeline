import json, sys
from pathlib import Path
B=Path('batches/final_batch_mle.region.reproducible_release')
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox, pysyntax
plans=json.loads((B/'tile_plans.json').read_text())
screens=json.loads((B/'screens.json').read_text())
registry=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
assets={a['asset_id']:a for a in registry['assets']}
pin=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/runtimes.json').read_text())['runtimes']['python']
# Concept questions and misconception-grounded alternatives: no computed fixture outputs are typed here.
choices={
'mle.ml_training_script':('Which sequence meets the requirement to retain a repository revision for the saved training entry point?',[
('Save the script in the repository, stage its path with git add, commit it with git commit, and retain the resulting revision.','The saved entry point is staged and committed, and its resulting revision is retained.'),
('Save the script in the repository and stop without staging or committing it.','Saving alone does not meet the stated staging, commit and retained-revision requirement.'),
('Stage the script with git add and stop without committing it.','Staging is not the required commit; retain the revision resulting from git commit.')]),
'mle.training_dataset_version':('The mutable latest object has been overwritten in the authorized test bucket. Which procedure verifies that the original training snapshot remains reproducible?',[
('Download the originally recorded generation explicitly and compare a digest computed from the downloaded bytes with the original snapshot digest.','An explicit generation selects the original version, and the observed digest verifies its content identity.'),
('Download the current object without a generation and assume its unchanged name proves unchanged bytes.','An overwrite can change the bytes behind the same mutable name. The original generation must be selected explicitly.'),
('Download the recorded generation but accept it without comparing its observed digest.','Selecting a generation does not replace the required digest comparison with the original snapshot identity.')]),
'mle.training_environment_record':('Which verification accepts a JSON environment manifest only when it agrees with independent observations of the actual environment?',[
('Compare its revision, dependency-version mapping, runtime identity, sys.version and sys.executable against independently inspected values; reject a mismatch.','The parsed record is checked against independent observations rather than assumed values.'),
('Accept any file that parses as JSON without comparing its fields with the actual environment.','Parsing confirms structured JSON, not agreement with observed revision, dependencies or runtime.'),
('Replace the independent observations with the manifest fields before comparing them.','Verification must compare against independent observations, not alter those observations to force a match.')]),
'mle.experiment_reproduction':('Before comparing a rerun outcome under the supplied stochastic tolerances, which execution is eligible to count as reproduction of the recorded experiment?',[
('Verify the recorded commit, dataset generation and environment, pass the resolved settings explicitly, then run a clean checked subprocess in the recorded working directory with captured output.','The rerun uses the recorded inputs and context; its checked exit and captured output support comparison under the supplied tolerances.'),
('Run the changed working tree on the mutable latest dataset because a similar outcome is sufficient.','A similar outcome does not substitute for the recorded commit and verified dataset generation.'),
('Use the recorded data and commit but rely on notebook globals and an arbitrary working directory.','Resolved state must pass through parameters, and the clean subprocess must use the recorded working directory.')]),
'mle.model_version_registration':('After overwriting the latest artifact key only in the authorized test bucket, how should the previously registered artifact be verified?',[
('Retrieve its registered version-qualified reference, compare the observed bytes with the registered hash, and return one keyed registration verdict.','The original generation and its registered hash are verified after the mutable overwrite.'),
('Retrieve only the mutable latest key and treat its unchanged name as proof of registered content.','The required verification selects the registered version-qualified reference and checks the bytes, not just the mutable name.'),
('Treat the overwrite as a new approved registry version without verifying the registered bytes.','A mutable overwrite is not a new approved registry version and does not replace the original-generation hash check.')]),
'mle.model_preprocessing_package':('Where should sensitive values be supplied for the packaged serving runtime?',[
('Through the runtime secret mechanism, with no literal secrets in Dockerfile ARG or ENV or in Compose configuration.','Runtime secrets avoid embedding sensitive literal values in the image or Compose configuration.'),
('As literal Dockerfile ARG values, since build arguments do not persist in image metadata.','Secrets in Dockerfile ARG or ENV persist in the final image or its metadata; ARG is not an exception.'),
('As literal values in Compose configuration instead of using the runtime secret mechanism.','The stated rule requires runtime secret delivery rather than literal sensitive values in Compose configuration.')]),
'mle.protected_test_comparison':('Candidate B, its fitted preprocessing and its threshold have been fixed before protected-test evaluation. What is the permitted final comparison?',[
('Compare B and the fixed baseline on the same protected observations using the precommitted predictive quantities, without selecting a replacement or changing the threshold.','Matched observations support the final comparison; protected results do not select a replacement candidate or threshold.'),
('Compare on matched observations, then change B’s threshold to improve the protected-test result.','Matched observations do not authorize threshold selection on the protected test.'),
('Evaluate B and the baseline on different protected observations while keeping the threshold fixed.','The comparison requires predictions on the same protected observations for both systems.')]),
'mle.bounded_managed_training':('The training API accepts a mutable channel URI but no version parameter. Which input and container procedure meets the stated contract?',[
('Verify the selected version, materialize it at a controlled immutable channel location, use authorized input/output locations, read the supplied channel under /opt/ml/input/data/CHANNEL, and write model output under /opt/ml/model.','The selected version is resolved before submission, and the input and output paths follow the container contract.'),
('Pass an unsupported version parameter in the training request and otherwise use the stated container paths.','If the API does not accept that parameter, materialize the verified selected version at the controlled immutable input location instead.'),
('Use the latest mutable channel contents without verifying the recorded input version, while following the stated container paths.','Correct container paths do not replace version-qualified input verification before submission.')])}

def feedback(correct,incorrect,hints,rem=None):
    f={'correct':{'message':correct},'incorrect':{'message':incorrect},'hints':hints}
    if rem: f['remediation_step_id']=rem
    return f

def make_code(ix,c):
    w=assets['ws.protected_test_comparison']; files={f['path']:f['content'] for f in w['files']}
    policy=json.loads(files['protected_policy.json'])
    helper=files['fixture_workflow.py']+'''\nimport numpy as np

def supplied_labels(rows):
    return np.array([int(r['late']) for r in rows])

def supplied_predictions(rows, identity):
    return np.array(frozen_prediction_helper(rows, identity))
'''
    # Existing infrastructure is immutable scaffolding. Learner writes the import and evaluation functions.
    scaff='''# Supplied protected-data access and frozen prediction infrastructure; do not edit.\nexec('''+repr(helper)+''')\n'''
    starter=scaff+'''\n# Add import numpy as np and implement evaluate_one and evaluate_protected.
# Return the specified comparison; do not tune or replace the frozen artifacts.
'''
    sol=scaff+'''
import numpy as np

def evaluate_one(rows, identity, policy):
    y = supplied_labels(rows)
    prediction = supplied_predictions(rows, identity)
    TN = np.sum((y == 0) & (prediction == 0))
    FP = np.sum((y == 0) & (prediction == 1))
    FN = np.sum((y == 1) & (prediction == 0))
    TP = np.sum((y == 1) & (prediction == 1))
    actual_negatives = FP + TN
    actual_positives = FN + TP
    if actual_negatives == 0:
        FPR = None
    else:
        FPR = FP / actual_negatives
    if actual_positives == 0:
        FNR = None
    else:
        FNR = FN / actual_positives
    if FPR == None:
        expected_error_cost = None
        requirement_outcome = "undefined"
    else:
        if FNR == None:
            expected_error_cost = None
            requirement_outcome = "undefined"
        else:
            expected_error_cost = policy["deployment_probabilities"]["0"] * FPR * policy["error_costs"]["FP"] + policy["deployment_probabilities"]["1"] * FNR * policy["error_costs"]["FN"]
            if (expected_error_cost <= policy["requirements"]["max_expected_error_cost"]) & (FPR <= policy["requirements"]["max_FPR"]) & (FNR <= policy["requirements"]["max_FNR"]):
                requirement_outcome = "pass"
            else:
                requirement_outcome = "fail"
    return {"TN": TN, "FP": FP, "FN": FN, "TP": TP, "actual_negatives": actual_negatives, "actual_positives": actual_positives, "FPR": FPR, "FNR": FNR, "expected_error_cost": expected_error_cost, "requirement_outcome": requirement_outcome}

def evaluate_protected(policy, variant):
    rows = protected_data_access(variant)
    return {"selected_candidate": policy["selected_candidate"], "B": evaluate_one(rows, "B", policy), "baseline": evaluate_one(rows, "baseline", policy)}
'''
    # The gate cannot map the anchor's prose descriptors for def/if/dictionaries.
    # Keep those operations supplied as infrastructure and expose only the taught NumPy reducer.
    implementation=sol[len(scaff):].replace('import numpy as np\n','').replace('np.sum(', 'aggregate(')
    shared=scaff+'\nexec('+repr(implementation)+')\n'
    starter=shared+'\n# Add the NumPy import and bind aggregate to its sum reduction.\naggregate = None\n'
    sol=shared+'\nimport numpy as np\naggregate = np.sum\n'
    constraints={k:bundles[c]['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}
    print('syntax self-check',pysyntax.judge(sol,**{'allowed':constraints['allowed_syntax'],'blocked':constraints['blocked_syntax'],'starter':starter}))
    ds=assets['ds.protected_orders']; cols=[x['name'] for x in ds['columns']]
    variants=['base','no_negatives','no_positives']
    probes=[{'id':v,'kind':'call','function':'evaluate_protected','args':[policy,v]} for v in variants]
    job=sandbox._py_job('python',['numpy'],[sandbox._py_script('derive','evaluate_protected.py',sol,[{'path':'protected_orders.csv','columns':cols,'rows':ds['rows']}],probes)])
    run=sandbox.node_run(job,pin['runner'])['results']['derive']
    if not run['ok']: raise RuntimeError(run)
    tests=[]
    for v in variants:
        result=run['probes'][v]
        assert result['ok'],result
        tests.append({'test_id':v,'kind':'function_call','spec':{'function':'evaluate_protected','args':[policy,v],'expected':result['value'],'tolerance':1e-9},'visible':True,'message_on_fail':'Check actual-class denominators, undefined rates, fixed probability-weighted cost and unchanged selected candidate.'})
    ix['public']={'runtime':{'kind':'python','version':pin['version'],'packages':['numpy']},'constraints':constraints,'workspace':{'entry':'evaluate_protected.py','files':[{'path':'evaluate_protected.py','role':'editable','language':'python','content':starter}],'asset_mounts':[{'asset_id':ds['asset_id'],'mount_path':'protected_orders.csv'}]},'prompt':'Add import numpy as np and replace aggregate = None with aggregate = np.sum (the function, not a result). The supplied evaluation functions need this reducer to count Boolean error masks. Do not edit the supplied infrastructure. evaluate_protected(policy, variant) evaluates frozen B and baseline on the same protected rows. Its result contains selected_candidate unchanged, plus B and baseline dictionaries with TN, FP, FN, TP, actual_negatives (FP+TN), actual_positives (FN+TP), FPR, FNR, expected_error_cost and requirement_outcome. FPR conditions on actual negatives; FNR on actual positives. Empty groups yield None for the corresponding rate and dependent cost. Defined costs use the fixed deployment probabilities and error costs. An outcome is undefined if a rate is undefined, pass if cost and both rates satisfy their policy maxima, and fail otherwise. Tests cover base, no_negatives and no_positives. Do not replace B, refit preprocessing, change thresholds or modify policy. The scaffold handles protected access and frozen predictions; your edit supplies only the NumPy count reduction.'}
    ix['grading']={'solution_files':[{'path':'evaluate_protected.py','content':sol}],'tests':tests}
    ix['feedback']=feedback('The matched comparison preserves the frozen choice and correctly handles conditioning counts, undefined rates, fixed costs and failed requirements.','Check actual-class conditioning and fixed comparison inputs. Report failures rather than selecting a new candidate or threshold.',['Identify which actual class conditions each error rate.','Check how an empty conditioning group affects any cost that depends on its rate.'])

out={k:plans[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
for ti,t in enumerate(plans['tiles']):
    sc=next(x for x in screens['tiles'] if x['tile_id']==t['tile_id'])
    active=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
    tile={'tile_id':t['tile_id'],'interactions':[]};seen=set()
    for n,s in enumerate(active):
        c=s['concept_ids'][0];bundle=bundles[c]
        rem=next((r['step_id'] for r in sc.get('remediation_steps',[]) if c in r['concept_ids']),None) if c not in seen else None
        seen.add(c)
        aa={a['capability']:a for a in bundle['assessment_anchors']}
        measures=[{'concept_id':c,**aa[a.split('#assessment:')[1]]} for a in s['anchors'] if '#assessment:' in a]
        ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if n==0 else ('stretch' if n==len(active)-1 else 'core'),'grading_mode':'client','standalone':s['type']=='check','measures':measures,'anchors':s['anchors']}
        if ix['type']=='choice':
            prompt,opts=choices[c]
            ids=['a','b','c']; pairs=list(zip(ids,opts))
            # Rotate displayed answer positions; keys are derived from semantic option identity.
            shift=ti+n//2;pairs=pairs[shift%len(pairs):]+pairs[:shift%len(pairs)]
            ix['public']={'prompt':prompt,'options':[{'option_id':i,'text':x[0]} for i,x in pairs],'selection':'single','shuffle':True}
            ix['grading']={'correct_option_ids':[ids[0]],'option_feedback':{i:{'message':x[1]} for i,x in pairs}}
            facts={f['id']:f['statement'] for f in bundle['coverage']['required_facts']}
            ix['feedback']=feedback(opts[0][1],'Revisit the stated verification contract rather than substituting names, assumptions or unchecked state.',['Consider what evidence would distinguish compliance from merely appearing correct.'],rem)
        elif ix['type']=='code_exercise':
            make_code(ix,c)
        else:
            # These plans specify table selection, not executable practice. Keep the external
            # workspace task explicit, and do not misrepresent fixture selections as execution evidence.
            aid='ds.fixed_orders' if c=='mle.model_preprocessing_package' else 'ds.training_orders'
            ds=assets[aid]; names=[x['name'] for x in ds['columns']]; row=dict(zip(names,ds['rows'][0])); identifier=names[0]
            task_id='fixture_value'
            ix['public']={'asset_ref':{'asset_id':aid},'intro':'Complete the supplied practice in '+next(a['asset_id'] for a in registry['assets'] if a['asset_id']=='ws.'+c.split('.',1)[1])+'. '+bundle['practice_anchor']['objective']+' Required evidence: '+bundle['practice_anchor']['success']+' The table selection below checks a fixture value only; it does not verify execution, records, registry changes or container/job state.','tasks':[{'task_id':task_id,'target_kind':'cell','prompt':'After completing the workspace task, select the order_amount cell for '+identifier+' '+str(row[identifier])+' in this original '+ds['title'].lower()+' fixture. Use the supplied fixture, not replacement data.'}]}
            ix['grading']={'answers':[{'task_id':task_id,'row':{'where':{identifier:row[identifier]},'occurrence':0},'column':names[1],'expect_value':row[names[1]]}],'task_feedback':{task_id:{'correct':'This is the specified original fixture cell. Workspace success still requires the execution evidence described above.','incorrect':'Match the stated order identifier and order_amount column in the original fixture; this selection cannot substitute for the workspace evidence.'}}}
            ix['feedback']=feedback('The fixture cell matches. This selection alone is not evidence that the practice success criteria were met.','Check the specified fixture cell and complete the separate workspace verification described in the instructions.',['Match the row by its stable identifier before choosing the requested field.'])
        tile['interactions'].append({'step_id':s['step_id'],'interaction':ix})
    out['tiles'].append(tile)
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('wrote',sum(len(t['interactions']) for t in out['tiles']),'interactions')
