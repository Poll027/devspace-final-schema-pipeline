import json, re, copy, html, pprint
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle')
P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
compact=json.loads((B/'working/03_compact_remediation.json').read_text())
bundles={b['context']['concept_id']:b for b in G['bundles']}; assets={a['asset_id']:a for a in R['assets']}
# Re-voiced teaching paragraphs, in the glossary's block order.
common_order='Give stages IDs and waitFor their required predecessors: successful completion, not textual position, controls dependencies. Keep rejection fatal: no allowFailure or failing exit codes in allowExitCodes; rejected Python gates must exit unsuccessfully.'
common_yaml='With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.'
commit='Use the configured repository commit trigger and branch filter; inspect stage results and resolved inputs for accepted and rejected fixtures.'
event='Use the configured Pub/Sub trigger, payload bindings and filters; inspect stage results and resolved inputs for accepted and rejected fixtures.'
texts={
'dataset_quality_gate':[
'Keep data-quality rejection fatal on the affected training path, rather than reporting a warning that training can ignore.',
'Validate before training. Unexpected or missing features and invalid feature values should stop the affected execution. Give every required schema/quality check a name, aggregate its result under the supplied pass/fail policy, and raise or return the declared failure without invoking training.',
'Retain the tested snapshot and failed checks for revalidation after repair. Assert the declared valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. In Cloud Build steps, name selects the execution image and args or script supplies the command: wire the assigned function/test entry point.',
common_order+' '+commit,
common_yaml,
'For the missing-required-feature fixture, retain the snapshot identity and named failure. Raise or return the declared rejection and verify training did not run. Wire the assigned image, command, IDs and waitFor edges; do not allow failing gate exits. Inspect accepted and rejected repository-triggered results. Repair must pass the same requirements before this path continues.',
'A failure report is not a blocking gate if training still runs. Allowing gate failures or their exit codes defeats the fatal boundary.'
],
'model_behavior_tests':[
'Test the package clients use, including fitted preprocessing. An isolated estimator with manually prepared input could miss a package defect.',
'Call the packaged fitted preprocessing and model through the inference prediction path. Check fixture row count, feature/target correspondence and output shape before values. Compare numerical output with np.testing.assert_allclose and explicitly declared tolerances.',
'Exercise malformed and boundary fixtures, requiring explicit rejection where the contract forbids them. Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Wire the assigned test entry point into Cloud Build: name specifies its image, args or script its command.',
common_order+' '+commit,
common_yaml,
'For the supplied valid fixture, check rows, correspondence and shape before numerical agreement at explicit tolerances. Exercise malformed and boundary inputs with contract-required rejection. Wire dependencies and fatal rejection into the existing build. Inspect repository-triggered stage results and resolved YAML fields: local test success alone is not the pipeline verdict.',
'Right-looking numbers for the wrong rows are still defective. Require correspondence and shape, call the packaged fitted path, and block downstream execution on required test failure.'
],
'model_release_quality_gate':[
'Gate the exact candidate evidence against predeclared requirements. Aggregate improvement cannot replace complete, passing quality and operating predicates.',
'Before promotion, compare the candidate with the accepted reference and predeclared requirements. Evaluate every supplied acceptance predicate and identify failures. Calculate validation expected error cost with fixed deployment probabilities and error costs; include fixed latency and operating limits in eligibility.',
'Failed or incomplete required gates block promotion. FPR conditions on actual negatives; FNR on actual positives. An empty conditioning group has no defined rate. With zero cost for correct predictions, weight each error rate by its supplied deployment class probability and error cost.',
'Protected test observations must not fit preprocessing, select a model or tune settings: that leaks information into the chosen system. Wire the assigned Cloud Build entry point with name for its image and args or script for its command. Set IDs and waitFor required predecessors; textual order is not the dependency.',
'Keep rejection fatal: no allowFailure or allowed failing exit codes, and a rejected Python gate exits unsuccessfully. '+event+' '+common_yaml,
'If cost meets its bound but latency fails, reject and name the latency predicate. Use fixed probabilities, costs and actual-class denominators. Bind evidence to the candidate. Configure image, command and waitFor without failure tolerance, then inspect event-bound inputs and results. Keep protected tests outside fitting/tuning; incomplete requirements block promotion too.',
'This gate is not an average of requirements. One failed or incomplete condition blocks promotion even when another metric improves.'
],
'pipeline_artifact_dependencies':[
'Explicitly connect the artifact training produces to the one validation consumes. Correct stage order alone can still connect the wrong files.',
'Give reusable components explicit input/output artifacts across experiment and production environments. Record each stage’s consumed identities, execution parameters and produced identity, not just filenames. Represent dependencies as a dictionary and check each required upstream identity against its downstream reference.',
'Require relevant dataset or model validation before dependent execution. Assert declared valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Wire the assigned Cloud Build entry point: name specifies the image, args or script the command.',
common_order+' '+event,
'Bind consumer args/substitutions to the immutable identifier produced by its declared upstream stage. Inspect actual run inputs to verify this edge, not just stage order. '+common_yaml,
'If training produces A but validation arguments name B, flag the mismatch even if filenames look alike. Record input identities, parameters and outputs; bind consumers to the upstream immutable identifier and inspect resolved inputs. Require relevant validation, waitFor predecessors and fatal failure. Inspect accepted/rejected events under the existing trigger bindings and filters.',
'waitFor proves a completion dependency, not artifact agreement. Verify the consumed identity separately.'
],
'staged_ml_promotion':[
'Carry one approved artifact across existing test and production boundaries. A completed build is not deployment permission: retain validation and separate authorization.',
'Read the approved registered name/version and run/artifact link. Continuous delivery checks test-environment compatibility, then model validation before production. Preserve the exact artifact’s validation verdict, including offline requirements and supplied staged evidence.',
'Stay within permitted identity and approval scope; record accountable authorization without changing policy. Record approval, registry version, artifact identity and per-stage gates. In Cloud Build, name selects the image and args or script the command for the assigned entry point.',
common_order+' '+event,
'Bind approved Secret Manager version references through availableSecrets.secretManager, exposing them only to the needed step through secretEnv. YAML stores references, not values. Use the authorized build/step identity and separate promotion authorization. Check captured output for non-disclosure; never echo or serialize runtime credentials.',
'Edit and parse existing staging/production YAML: production depends on staging quality and authorization for the identical immutable artifact. Test unauthorized promotion and inspect that production did not execute. '+common_yaml,
'Read the approved version and run/artifact link. Make production depend on staging quality and authorization for that same artifact. Record offline/staged evidence, approval and stage results. Use the approved identity and step-scoped secret references. Inspect unauthorized-event results, resolved inputs and output non-disclosure; keep rejection fatal.',
'Passing staging for A cannot approve B. Training or staging success is not promotion authorization, and credentials must not enter the promotion record.'
],
'pipeline_failure_recovery':[
'Resume at a verified artifact boundary after the declared recoverable failure. Preserve required quality decisions instead of turning retry into permission to continue.',
'Locate the failed stage and affected artifacts, preserving identities of completed required stages. Catch only the declared recoverable error with try/except, record it, and apply only the supplied recovery action. After repair, rerun the affected required check; stop if it still fails.',
'Reuse upstream output only when its recorded identity and required validation remain valid for the resumed stage. Wire the assigned Cloud Build entry point using name for the image and args or script for the command. Set IDs and waitFor required predecessors: successful completion, not textual location, controls dependencies.',
'Keep gate failures fatal: no allowFailure or allowed failing exit codes; rejected Python gates exit unsuccessfully. '+event+' Distinguish the injected recoverable exception from unrelated failures. Retry at the verified boundary and inspect execution of the retry and later required gates.',
common_yaml+'\n\nReconcile only declared named uploads. Use blob.exists(), blob.reload() and generation to retrieve bytes; verify expected hash and required validation. Skip only verified completed uploads. Create missing output with blob.upload_from_filename(path, if_generation_match=0). On 412, re-read and verify, never overwrite; conflicts or failed validation stop recovery.\n\nInject failure after one upload; assert its generation/hash is retained, only missing outputs complete, retry and later gates run, and invalid existing output fails. Repeat recovery: no extra uploads/generations, with required validation still enforced.',
'After failure between A and B uploads, verify A’s generation, bytes, hash and validation before reuse. Create only missing B with if_generation_match=0; on 412 re-read and verify, never overwrite. Conflict or invalid content stops recovery. Retry the stage and required gates; repeat recovery with no extra uploads/generations while revalidating. Catch only the declared recoverable exception.',
'Recovery is not ignore-and-continue. Reuse requires identity and validation; retry must not overwrite conflicting content or bypass gates.'
],
'deployed_model_lineage_audit':[
'Trace the served model through supplied records to training, code and data. Similar record names do not establish identity links.',
'Lineage connects the served artifact to training execution, resolved configuration, code revision and dataset snapshot. Resolve the deployed registry version’s artifact source and run link. Retrieve that run and compare dataset, configuration and artifact evidence with deployment and approval records.',
'Check the supplied lineage chain pair by pair; flag missing or mismatched identities instead of inferring provenance from names. Assert declared valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution. Download the registry’s exact recorded artifact generation and verify content identity against the lineage record.',
'Inspect the recorded local revision with git rev-parse --verify REVISION and git show REVISION. Confirm the commit exists rather than merely copying its string.',
'Walk deployment → registry → artifact/run → configuration and dataset; check the recorded code against an existing local commit. Resolve the exact registry generation and verify downloaded content against the lineage record. Compare run evidence with deployment and approval, preserving each missing or mismatched edge. Approval for A cannot cover a deployment linked to B. Inspect the revision with git rev-parse and git show; a revision string alone is not commit-existence evidence. These checks audit supplied provenance; they cannot recover an absent link by guessing from familiar model names.',
'Matching names are not lineage. Report missing or mismatched run/artifact links; an unverified revision string does not prove a commit exists.'
]}

def lineage(c,tbs=(),facts=(),anchors=()):
 return {'concept_ids':[c], 'teaching_block_ids':list(tbs),'fact_ids':list(facts),'anchors':list(anchors)}
def prose(text,lin,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':copy.deepcopy(lin)}
def tbline(c,t):
 return lineage(c,[c+'#'+t['id']],[c+'#'+f for f in t['fact_ids']])
def diagram(c,title,labels,edges=()):
 return {'type':'diagram','diagram_kind':'graph','title':title,'nodes':[{'id':'n'+str(i),'label':v} for i,v in enumerate(labels)],'edges':[{'from':'n'+str(a),'to':'n'+str(b),'label':label,'directed':True} for a,b,label in edges],'alt_text':title+': '+'; '.join(labels),'lineage':lineage(c,anchors=[c+'#visual'])}
def table(c,asset,variant=None):
 ref={'asset_id':asset}
 if variant:ref['variant_id']=variant
 return {'type':'data_table','asset_ref':ref,'lineage':lineage(c,anchors=[c+'#visual'])}
def file(c,path):
 return next(f['content'] for f in assets['ws.'+c.split('.')[-1]]['files'] if f['path']==path)
def source_panel(c,path,annotation):
 # Fixture inputs are source, not computed verdicts or execution output.
 obj=json.loads(file(c,path))
 if path.endswith('release_cases.json'): obj={k:obj[k] for k in ['A','operating_failure']}
 elif path.endswith('dependency_cases.json'): obj={k:obj[k] for k in ['valid','mismatch']}
 elif path.endswith('promotion_cases.json'): obj={k:obj[k] for k in ['accepted','wrong_artifact']}
 elif path.endswith('lineage_cases.json'): obj={k:obj[k] for k in ['valid','approval_A_deployment_B']}
 code='fixture_inputs = '+pprint.pformat(obj,width=88,sort_dicts=False)
 return {'type':'code_walkthrough','language':'python','code':code,'annotations':[{'start_line':1,'end_line':1,'text':annotation}],'reveal':'all','lineage':lineage(c,anchors=[c+'#visual'])}
def visual(c,v):
 key=c.split('.')[-1]
 if v=='annotated_image':
  assert not any(a['asset_kind']=='image' for a in R['assets'])
  return diagram(c,'Required quality-gate states (schematic, not captured runs)', ['Accepted fixture: retain snapshot and named checks','Required quality passes','Training may start','Missing required feature: retain snapshot and failed check','Required quality rejects','Training must not start'],[(0,1,'validate'),(1,2,'success required'),(3,4,'validate'),(4,5,'fatal boundary')])
 if v=='side_by_side' and key=='model_behavior_tests':
  return {'type':v,'left_label':'Valid packaged-path input','right_label':'Malformed packaged-path input','left':table(c,'ds.behavior_inputs'),'right':table(c,'ds.behavior_inputs','malformed'),'takeaway':'Check rows, correspondence and shape before toleranced values; malformed input requires contract rejection. These are fixture inputs, not captured results.','lineage':lineage(c,anchors=[c+'#visual'])}
 if v=='side_by_side':
  left=source_panel(c,'fixtures/release_contract.json','Fixed quality and operating requirements; rates use actual-class denominators.')
  right=source_panel(c,'fixtures/release_cases.json','Candidate fixture inputs, not run verdicts. Evaluate every required predicate; cost cannot excuse latency failure.')
  return {'type':v,'left_label':'Predeclared requirements','right_label':'Supplied candidate evidence','left':left,'right':right,'takeaway':'Reject a failed or incomplete required condition, even when another metric improves.','lineage':lineage(c,anchors=[c+'#visual'])}
 if v=='before_after':
  return {'type':v,'before':diagram(c,'Before recovery: declared injection boundary',['A uploaded: identity and validation must be verified','Failure before B upload','B missing'],[(0,1,'injected failure'),(1,2,'remaining work')]),'after':diagram(c,'Required recovery behavior (not captured execution)',['Verify A: generation, bytes, hash and validation','Create missing B with if_generation_match=0','On 412: re-read and verify','Retry stage and required gates','Repeat: revalidate; no additional uploads/generations'],[(0,1,'reuse only verified output'),(1,2,'if creation races'),(1,3,'verified completion'),(2,3,'verified completion'),(3,4,'second invocation')]),'change_summary':'Preserve verified completed output, finish only missing uploads, and keep required validation fatal.','lineage':lineage(c,anchors=[c+'#visual'])}
 paths={'pipeline_artifact_dependencies':'fixtures/dependency_cases.json','staged_ml_promotion':'fixtures/promotion_cases.json','deployed_model_lineage_audit':'fixtures/lineage_cases.json'}
 annotations={'pipeline_artifact_dependencies':'Inspect consumed/produced identities and parameters. A waitFor edge alone cannot establish the same artifact was consumed. Fixture inputs are not run results.', 'staged_ml_promotion':'Compare approval, registry/run and staged artifact identities; retain separate authorization. Fixture inputs are not deployment results.', 'deployed_model_lineage_audit':'Compare deployment → registry → artifact/run and run → dataset/configuration links. Request the exact recorded generation, compare content, and inspect the local commit; fixture records are not audit output.'}
 return source_panel(c,paths[key],annotations[key])

out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for tile in P['tiles']:
 result={'tile_id':tile['tile_id'],'title':tile['title'],'steps':[],'remediation_steps':[]}
 for plan in tile['steps']:
  c=plan['concept_ids'][0]; key=c.split('.')[-1]
  step={'step_id':plan['step_id'],'type':plan['type'],'concept_ids':plan['concept_ids'],'title':'','eyebrow':tile['title'],'lineage':{k:copy.deepcopy(plan[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}}
  step['lineage']['concept_ids']=plan['concept_ids']
  if plan['type']=='explainer':
   step['title']={'s01':'Keep the boundary explicit'}.get(plan['step_id'].split('.')[-1],bundles[c]['context']['concept_name'])
   step['blocks']=[]
   for tid in plan['teaching_block_ids']:
    t=next(t for t in bundles[c]['teaching_blocks'] if c+'#'+t['id']==tid)
    for paragraph in texts[key][int(t['id'][2:])-1].split('\n\n'):
     step['blocks'].append(prose(paragraph,tbline(c,t),'example' if t['purpose']=='example' else 'mechanism'))
   # Symbolic formula, never computed numerical output.
   if key=='model_release_quality_gate' and c+'#tb3' in plan['teaching_block_ids']:
    step['blocks'].append({'type':'code_walkthrough','language':'python','code':'fpr = FP / (FP + TN)\nfnr = FN / (FN + TP)\nexpected_cost = p_negative * fpr * cost_FP + p_positive * fnr * cost_FN','annotations':[{'start_line':1,'end_line':3,'text':'Apply only with nonempty actual-class groups and zero cost for correct predictions; probabilities and error costs are predeclared.'}],'lineage':lineage(c,[c+'#tb3'],[c+'#f5',c+'#f6'])})
   if plan['planned_visual_block_type']:step['blocks'].append(visual(c,plan['planned_visual_block_type']))
  elif plan['type'] in ('check','hands_on'):
   judge=plan['type']=='hands_on' and plan['planned_interaction_type'] in ('choice','classify')
   step['title']=('Review the lineage evidence' if judge else ('Inspect the gate evidence' if plan['type']=='check' else 'Verify '+bundles[c]['context']['concept_name'].lower()))
   step['lede']=('Read the supplied excerpts in this step and decide which preserve the required identity checks and which are defective.' if judge else ('Use the supplied evidence to judge the required predicates and boundaries.' if plan['type']=='check' else 'Implement the assigned function and configuration checks using the supplied fixtures; verify accepted and rejected behavior at the required fatal boundary.'))
   # Distinct fact sets receive separate remediation targets. Re-teach exact measured facts.
   facts=plan['fact_ids']; tbs=[t for t in bundles[c]['teaching_blocks'] if set(t['fact_ids']) & {f.split('#')[-1] for f in facts} and t['purpose'] not in ('example','distinction')]
   rid=tile['tile_id']+'.r'+str(len(result['remediation_steps'])+1).zfill(2)
   lin=lineage(c,[c+'#'+t['id'] for t in tbs],facts)
   rem={'step_id':rid,'type':'remediation','concept_ids':[c],'title':'Separate the required checks','lede':'Return to the same fictional lifecycle fixtures.','lineage':lin,'blocks':[]}
   # Each fact paragraph is kept small; no facts are merely attributed to a contrast.
   for fid in facts:
    f=next(f for f in bundles[c]['coverage']['required_facts'] if c+'#'+f['id']==fid)
    ft=[c+'#'+t['id'] for t in tbs if f['id'] in t['fact_ids']]
    remtext=compact[key].get(f['id'],f['statement'])
    patterns={'In an existing Cloud Build':'image','Assign step IDs':'order','Keep required gate failures':'fatal','Write assert predicate':'assert','With the declared PyYAML':'yaml','Use the configured repository':'commit','Use the configured Pub/Sub':'event'}
    for prefix,shared in patterns.items():
     if f['statement'].startswith(prefix): remtext=compact['shared'][shared]
    rem['blocks'].append(prose(remtext,lineage(c,ft,[fid])))
   contrast=texts[key][-1]
   rem['blocks'].append(prose(contrast,lineage(c,[c+'#'+bundles[c]['teaching_blocks'][-1]['id']],[c+'#'+f for f in bundles[c]['teaching_blocks'][-1]['fact_ids']]),'misconception'))
   result['remediation_steps'].append(rem)
  elif plan['type']=='video':
   step['title']='Review the core mechanism';step['blocks']=[{'type':'media_group','segment_ids':plan['segment_ids']}]
  elif plan['type']=='recap':
   step['title']='Keep each boundary accountable';step['blocks']=[]
   for cc in tile['concept_ids']:
    bb=bundles[cc];t=bb['teaching_blocks'][-1]
    recap={'dataset_quality_gate':'Dataset rejection must stop the affected training path.','model_behavior_tests':'Test the packaged fitted path: correspondence and shape matter alongside numbers.','model_release_quality_gate':'One failed or incomplete required acceptance condition blocks promotion.','pipeline_artifact_dependencies':'Stage order and artifact-identity agreement are separate checks.','staged_ml_promotion':'Validation and authorization must cover the exact promoted artifact.','pipeline_failure_recovery':'Reuse only verified output; recovery must not bypass required gates.','deployed_model_lineage_audit':'Report missing identity links; inspect exact content and the recorded commit.'}[cc.split('.')[-1]]
    step['blocks'].append(prose(recap,tbline(cc,t),'takeaway'))
   nextidea='Define explicit input/output artifact dependencies' if tile['next_tile_id']==P['tiles'][1]['tile_id'] else G['names']['mle.distribution_monitoring']
   step['blocks'].append({'type':'up_next','title':nextidea,'text':'Next: '+tile['next_tile_id']+'.'})
  result['steps'].append(step)
 out['tiles'].append(result)
(B/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',B/'screens.json')
