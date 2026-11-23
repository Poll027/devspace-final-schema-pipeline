import json,re,copy
from pprint import pformat
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle')
p=json.loads((B/'tile_plans.json').read_text()); g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); r=json.loads((B/'scenario_asset_registry.json').read_text())
G={x['context']['concept_id']:x for x in g['bundles']}; A={x['asset_id']:x for x in r['assets']}
texts={
'dataset_quality_gate':[
'Make dataset rejection a stopping point, not a warning that training can ignore.',
'Validate data before training. Unexpected or missing features and invalid feature values should stop the affected execution. Give every required check a name, then aggregate its result under the supplied pass/fail policy. If a required test fails, raise or return the declared failure and do not call training.',
'Keep the tested snapshot and failed-check evidence for revalidation after repair. Use assert predicates for valid, boundary and failure cases; false predicates raise AssertionError in ordinary non-optimized execution. In Cloud Build YAML/JSON, name selects the execution image; args or script supplies the command. Wire the assigned test entry point there.',
'Give steps IDs and make waitFor name the required predecessors. Successful completion, not position in the file, establishes the dependency. Leave required failures fatal: no allowFailure and no failing gate codes in allowExitCodes. A rejected Python gate must exit unsuccessfully. Use the configured commit trigger and branch filter, inspecting stage results and resolved inputs for accepted and rejected fixtures.',
'With PyYAML installed, import yaml. Serialize mapping/list configuration with yaml.safe_dump(config, file_handle), then reload with yaml.safe_load(file_handle). Inspect required resolved fields before submission. Safe loading supports standard YAML tags, not arbitrary Python object constructors.',
'For the missing-feature snapshot, retain its identity and failed named check, reject it, and inspect that training did not start. Wire the test command and image into the quality step; set IDs and waitFor edges. Keep rejection fatal. Exercise both accepted and rejected fixtures through the configured repository trigger and branch filter, inspecting resolved inputs and stage results. A repaired snapshot must meet the unchanged requirements.',
'A failure message is not a blocking gate if training still runs. Failure-tolerant settings defeat that boundary.'
],
'model_behavior_tests':[
'Test what clients call: the packaged model with its fitted preprocessing. An isolated estimator on manually prepared inputs could miss a package defect.',
'Call the same packaged prediction path used for inference. Before comparing numbers, check expected row count, feature/target correspondence and output shape for each fixture. Use np.testing.assert_allclose with explicitly declared tolerances for numerical comparisons.',
'Try malformed and boundary inputs; require explicit rejection wherever the contract forbids them. Assert valid, boundary and failure predicates: false predicates raise AssertionError in ordinary non-optimized execution. Wire the test entry point into the existing Cloud Build step using name for its image and args or script for its command.',
'Use step IDs and waitFor for required successful predecessors, not just written order. Keep rejected Python tests unsuccessful: do not enable allowFailure or allow their failing exit codes. Run the configured repository commit trigger and branch filter. Inspect stage results and resolved inputs for accepted and rejected fixtures.',
'Import yaml with the declared PyYAML dependency. Write mapping/list configuration using yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.',
'For the supplied valid fixture, check count, correspondence and shape before numerical tolerance. Test malformed and boundary cases with the contract-required rejection. Wire the entry point and dependencies, keeping failure fatal. Run the configured repository trigger and inspect accepted and failed stages: a locally passing test is not a pipeline verdict. Parse the YAML and inspect resolved fields. Right-looking values assigned to the wrong rows must fail too.',
'Matching numbers do not establish matching rows or shape. Use the fitted package, and make required test failure stop dependent execution.'
],
'model_release_quality_gate':[
'Bind release eligibility to exact candidate evidence and requirements declared beforehand. Aggregate improvement cannot replace complete, passing required predicates.',
'Before promotion, compare the candidate with the accepted reference and fixed quality requirements. Read its evidence, evaluate each required acceptance predicate, and name failed predicates on rejection. Compute validation expected error cost with the supplied deployment probabilities and error costs. Fixed latency and operating limits also determine eligibility.',
'Failed or incomplete required gates block promotion. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty conditioning groups give no defined rate. With zero cost for correct predictions, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
'Keep protected-test observations out of preprocessing fitting, model choice and settings tuning; those uses leak information into the selected system. Wire the assigned entry point into the Cloud Build step: name declares the image, args or script the command. Assign IDs and waitFor dependencies on successful required predecessors; textual position is not enough.',
'Keep required gate failure fatal: no allowFailure or allowed failing exit codes, and rejected Python exits unsuccessfully. Use the configured Pub/Sub event trigger, payload bindings and filters; inspect stage results and resolved inputs for accepted and rejected fixtures. Import yaml, safe_dump mapping/list configuration, safe_load it, and inspect required fields before submission. Safe loading accepts standard tags, not arbitrary Python object constructors.',
'A candidate can meet the cost bound yet fail fixed latency. Reject it and name latency rather than treating cost success as approval. Use fixed deployment probabilities, error costs and actual-class denominators; bind evidence to candidate identity. Configure the event-triggered gate image, command and waitFor edges without failure tolerance. Inspect resolved inputs and stage results for accepted and rejected events. Keep protected-test observations outside fitting and tuning. Missing required evidence blocks promotion too.',
'Requirements are not averaged. One failed or incomplete required condition blocks promotion despite improvement elsewhere.'
],
'pipeline_artifact_dependencies':[
'Validation must consume the identified artifact training produced. Correct-looking stage order can still connect the wrong files.',
'Explicit component inputs and outputs let a workflow run across experiment and production environments. Record consumed dataset/artifact identity, execution parameters and produced identity per stage. Do not join unrelated outputs by filename alone. Build a dependency dictionary and check every required upstream identity against its downstream reference.',
'Require the relevant dataset or model validation result before dependent execution. Assert valid, boundary and failure cases; false predicates raise AssertionError in ordinary non-optimized execution. Wire the assigned entry point into existing Cloud Build YAML/JSON: name declares its image and args or script its command.',
'Use IDs and waitFor to require successful predecessor completion, not just textual ordering. Keep rejected Python gates unsuccessful, without allowFailure or allowed failing exit codes. Exercise the configured Pub/Sub event trigger with its bindings and filters. Inspect accepted and rejected stage results and resolved inputs.',
'Bind consumer args/substitutions to the immutable identifier from the declared producer, then inspect actual run inputs. With PyYAML, import yaml, write mapping/list configuration using yaml.safe_dump(config, file_handle), and reload with yaml.safe_load(file_handle). Inspect required resolved fields before submission. Safe loading permits standard YAML tags, not arbitrary Python object constructors.',
'Training produces A, but validation references B: flag the mismatch even if filenames look alike. Record consumed identity, parameters and produced identity. Bind consumers through args/substitutions to the declared upstream immutable identifier and inspect resolved run inputs. Require relevant validation before dependent execution. Parse configuration, set waitFor edges and keep required failures fatal. Exercise accepted and rejected events through the configured bindings and filters to verify artifact edges, not merely stage sequence.',
'waitFor proves a completion dependency, not artifact agreement. Check both separately.'
],
'staged_ml_promotion':[
'Carry one approved artifact across test and production boundaries. A completed build is not separate deployment authorization.',
'Read the approved registered model name/version and originating run/artifact link. Continuous delivery checks compatibility in a test environment, then model validation before production. Preserve the exact artifact’s validation verdict, offline requirements and supplied staged evaluation evidence.',
'Stay within the permitted identity and approval scope; record accountable authorization instead of changing policy. Record approval, registry version, artifact identity and per-stage results. Wire the assigned Cloud Build entry point using name for the execution image and args or script for the command.',
'Set IDs and waitFor for required successful predecessors; file order is insufficient. Keep gate rejection fatal: no allowFailure or failing gate codes in allowExitCodes, and unsuccessful Python exit. Use configured Pub/Sub bindings and filters; inspect accepted and rejected stage results and resolved inputs.',
'Bind approved Secret Manager versions through availableSecrets.secretManager; expose them only to the needed step with secretEnv. YAML holds references, not values. Use the authorized build/step identity and preserve separate promotion authorization. Check captured output for non-disclosure; never echo or serialize runtime credentials.',
'Edit and parse staging/production YAML so production requires staging quality and authorization for the same immutable artifact. Test unauthorized promotion and inspect that production did not execute. With PyYAML, import yaml, safe_dump mapping/list configuration, safe_load it, and inspect required resolved fields before submission. Safe loading supports standard tags, not arbitrary Python object constructors.',
'Read the approved registry version and run/artifact link. Bind production to staging quality and authorization for that identical artifact. Record offline requirements, staged evidence, approval and per-stage results. Use the approved identity and step-scoped secretEnv references, never literal credentials. Replay unauthorized promotion and inspect that production did not run. Parse configuration, inspect event-bound inputs and keep failures fatal. Check captured output without disclosing secrets.',
'Staging success for A cannot approve B. Training or staging success is not authorization, and credentials do not belong in the promotion record.'
],
'pipeline_failure_recovery':[
'After a partial upload, preserve valid completed effects, finish missing work and rerun required gates. Do not hide conflicting content or create extra generations.',
'Locate the failed stage using execution status and retained artifacts; preserve successful required-stage identities. Catch only the declared recoverable error with try/except, record it and apply the supplied recovery action. After repair, rerun the affected required quality check. Stop if it still fails; recovery cannot bypass dataset or model gates.',
'Reuse upstream output only when recorded identity and required validation remain valid for the resumed stage. Wire the assigned Cloud Build entry point: name selects the image; args or script the command. Set IDs and waitFor for successful required predecessors, not merely textual order.',
'Keep rejected gates fatal: no allowFailure or allowed failing exit codes, and unsuccessful Python exit. Use configured Pub/Sub bindings and filters and inspect accepted/rejected stage results and resolved inputs. Distinguish the injected recoverable exception from unrelated failures. Retry from the verified artifact boundary and inspect that the retry and later required gates actually ran.',
'Import yaml with PyYAML; safe_dump mapping/list configuration, safe_load it, and inspect required resolved fields before submission. Safe loading accepts standard tags, not arbitrary Python constructors.\n\nReconcile only declared named uploads. Use blob.exists(), blob.reload() and generation to retrieve existing bytes; verify expected hash and required validation. Skip only matching completed uploads. Create missing output with blob.upload_from_filename(path, if_generation_match=0). On 412 Precondition Failed, re-read and verify instead of overwriting. Conflict or failed validation stops recovery.\n\nInject failure after one upload, before remaining work. Assert the first generation/hash is retained, only missing uploads complete, the retried stage and downstream required gates run, and invalid existing output fails. Invoke recovery again: assert no extra generations/uploads while validation remains enforced.',
'Inject failure after A, before B. Inspect A’s existence, generation, bytes, expected hash and validation. Skip a matching A; create missing B with if_generation_match=0. On 412, re-read and verify, never overwrite. Conflict or failed validation stops recovery. Retry from the verified boundary and inspect the affected stage and later required gates. Invoke again and verify no extra uploads or generations, with validation still enforced.',
'Catch only the declared recoverable exception. Unrelated failures cannot authorize continuation; completed output requires verified identity and validation.'
],
'deployed_model_lineage_audit':[
'Trace the served model through recorded identities, not similar names. Compare the supplied links pair by pair.',
'Lineage links the served artifact to training execution, resolved configuration, code revision and dataset snapshot. Resolve the deployed registry version and inspect its artifact source and run link. Retrieve that run, then compare dataset, configuration and artifact evidence with deployment and approval records.',
'Check each supplied identity edge; report missing or mismatched links rather than inferring provenance from names. Assert valid, boundary and failure cases: false predicates raise AssertionError in ordinary non-optimized execution. Download the exact registry-recorded artifact generation and verify its content identity against the lineage record.',
'Inspect the recorded local revision with git rev-parse --verify REVISION and git show REVISION. Verify the referenced commit exists; copying its string is insufficient.',
'Resolve the deployed version, artifact source and originating run. Compare dataset, configuration and artifact identities with deployment and approval. Download the exact recorded generation and verify content. Inspect the referenced commit with git rev-parse and git show. If deployment points to B while approval covers A, flag the mismatch. Preserve absent links explicitly rather than guessing a training source from a familiar name.\n\nWalk deployment → registry → artifact/run → configuration/dataset, and code → existing commit. Each edge can fail independently. Exact-generation content verification and local revision inspection check different evidence; neither repairs a missing link by inference.',
'Matching names do not prove lineage. Report absent or mismatched run/artifact links. A revision string alone does not establish that its commit exists.'
]}
# Compact remediation restates the measured facts without adding answers or outcomes.
common_short={
"In an existing Cloud Build": "Wire the assigned entry point in Cloud Build YAML/JSON: each steps item uses name for its execution image and args or script for its command.",
"Assign step IDs": "Assign IDs and waitFor references to required predecessors. Their successful completion, not textual order, establishes downstream dependency.",
"Keep required gate failures fatal": "Keep required failure fatal: no allowFailure or failing codes in allowExitCodes; rejected Python must exit unsuccessfully.",
"Use the configured repository": "Use the configured repository commit trigger and branch filter. Inspect actual stage results and resolved inputs for accepted and rejected fixtures.",
"Use the configured Pub/Sub": "Use the configured Pub/Sub event trigger, payload bindings and filters. Inspect actual stage results and resolved inputs for accepted and rejected fixtures.",
"With the declared PyYAML": "With PyYAML, import yaml; yaml.safe_dump(config, file_handle) writes mapping/list configuration and yaml.safe_load(file_handle) reloads it. Inspect required fields before submission. Safe loading accepts standard tags, not arbitrary Python constructors.",
"Write assert predicate": "Assert valid, boundary and failure predicates; false predicates raise AssertionError in ordinary non-optimized execution."
}
rem_specific={
'dataset_quality_gate':{
'f1':'Validate before training. Unexpected or missing features and invalid feature values should stop the affected execution.',
'f2':'Name each required schema/quality check and aggregate results into explicit pass/fail under the supplied policy.',
'f3':'On required failure, raise or return the declared failure; do not invoke training.',
'f4':'Retain tested snapshot and failed-check evidence to validate repaired data against the same requirements.'},
'model_behavior_tests':{
'f1':'Test the packaged fitted preprocessing and model through the inference prediction path.',
'f2':'Check expected row count, feature/target alignment and output shape before comparing values.',
'f3':'Compare numerical output against the expected fixture using np.testing.assert_allclose and explicit tolerances.',
'f4':'Test malformed and boundary fixtures, requiring explicit rejection where the contract forbids input.'},
'model_release_quality_gate':{
'f1':'Before promotion, compare candidate evidence with the accepted reference and predeclared quality requirements.',
'f2':'Evaluate each required candidate-evidence predicate and identify failed predicates when rejecting.',
'f3':'Calculate validation expected error cost with predeclared deployment probabilities and costs; include fixed latency/operating limits in eligibility.',
'f4':'Any failed or incomplete required gate blocks promotion.',
'f5':'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups have no defined rate.',
'f6':'With zero correct-prediction cost, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
'f7':'Never fit preprocessing, choose models or tune settings with protected-test observations; doing so leaks information into the chosen system.'},
'pipeline_artifact_dependencies':{
'f1':'Explicit component input/output artifacts let the workflow run across experiment and production environments.',
'f2':'Record each stage’s consumed dataset/artifact identity, parameters and produced identity; filenames alone cannot join unrelated outputs.',
'f3':'Use a dependency dictionary and compare each required upstream artifact identity with the supplied downstream reference.',
'f4':'Require relevant dataset/model validation before dependent execution.',
'f10':'Bind consumer args/substitutions to the declared producer’s immutable identifier; inspect actual run inputs to verify the edge.'},
'staged_ml_promotion':{
'f1':'Read approved registered model name/version and its run/artifact link before authorizing staged deployment.',
'f2':'Continuous delivery checks compatibility in a test environment, then model validation before production.',
'f3':'Preserve the exact artifact’s validation verdict, offline requirements and supplied staged evidence.',
'f4':'Stay within permitted identity/approval scope and record accountable authorization; do not change policy.',
'f5':'Record approval, registry version, artifact identity and per-stage results.',
'f10':'Bind approved Secret Manager versions with availableSecrets.secretManager; expose only needed steps via secretEnv. YAML holds references, not values.',
'f11':'Use the authorized build/step identity while preserving separate promotion authorization.',
'f12':'Check captured build output for secret non-disclosure; never echo or serialize runtime credentials.',
'f13':'Edit and parse staging/production YAML: production requires staging quality and authorization for the identical artifact. Test unauthorized promotion and inspect that production did not execute.'},
'pipeline_failure_recovery':{
'f1':'Locate the failed stage from status and retained artifacts; preserve completed required-stage identities.',
'f2':'Catch the declared recoverable error with try/except, record it and apply only the supplied action; do not declare success silently.',
'f3':'After repair, rerun the affected required quality check; stop if it still fails. Recovery cannot bypass dataset/model gates.',
'f4':'Reuse completed upstream output only when recorded identity and required validation remain valid for the resumed stage.',
'f9':'Distinguish the injected recoverable exception from unrelated failures. Retry from the verified boundary and inspect that retry and later required gates ran.',
'f11':'For declared named uploads, use blob.exists(), blob.reload() and generation to retrieve bytes. Verify expected hash and validation before skipping matching output. Create missing output with blob.upload_from_filename(path, if_generation_match=0). On 412, re-read and verify, never overwrite. Conflict or failed validation stops recovery.',
'f12':'Inject failure after one upload, before remaining work. Assert retained generation/hash, only missing uploads, retried stage and downstream gates, and rejection of invalid existing output. Invoke again: no extra generations/uploads, while required validation still runs.'},
'deployed_model_lineage_audit':{
'f1':'Link served artifact to training execution, resolved configuration, code revision and dataset snapshot.',
'f2':'Resolve the deployed registry version; inspect artifact source and run link.',
'f3':'Retrieve that run; compare dataset/configuration/artifact evidence with deployment and approval.',
'f4':'Check supplied lineage identities pairwise. Flag missing or mismatched links; never infer provenance from similar names.',
'f6':'Download the exact registry-recorded artifact generation and verify content identity against the lineage record.',
'f7':'Inspect the recorded local revision with git rev-parse --verify REVISION and git show REVISION; verify the commit exists instead of copying its string.'}
}
def short_fact(c,fid,text):
 for prefix,rewrite in common_short.items():
  if text.startswith(prefix):return rewrite
 return rem_specific[c.split('.')[-1]].get(fid,text)

# Qualified lineage comes from frozen inputs, never from shorthand in the artifact.
def lin(c,tbs=None,facts=None,visual=False):
 d={'concept_ids':[c], 'teaching_block_ids':tbs or [],'fact_ids':facts or []}
 if visual:d['anchors']=[c+'#visual']
 return d

def prose(text,lineage):return {'type':'prose','text':text,'lineage':copy.deepcopy(lineage)}
def chunks(text):
 # Preserve sentence boundaries; every prose block has a single small paragraph.
 out=[]
 for para in text.split('\n\n'):
  acc=''
  for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z])',para):
   if len((acc+' '+sent).split())>90 and acc:out.append(acc);acc=''
   acc=(acc+' '+sent).strip()
  if acc:out.append(acc)
 return out

def files(c):return {f['path']:f['content'] for f in A['ws.'+c.split('.')[-1]]['files']}
def load(c,path):return json.loads(files(c)[path])
def walk(code,l):return {'type':'code_walkthrough','language':'python','code':code,'reveal':'all','lineage':copy.deepcopy(l)}
def table(asset,l,variant=None):
 ref={'asset_id':asset}
 if variant:ref['variant_id']=variant
 return {'type':'data_table','asset_ref':ref,'lineage':copy.deepcopy(l)}
def diagram(nodes,edges,title,l):return {'type':'diagram','diagram_kind':'sequence','title':title,'nodes':[{'id':f'n{i}','label':label,'fields':fields} for i,(label,fields) in enumerate(nodes)],'edges':[{'from':f'n{x}','to':f'n{y}','label':label,'directed':True} for x,y,label in edges],'alt_text':title,'lineage':copy.deepcopy(l)}

def visual(c,s):
 l=lin(c,s['teaching_block_ids'],s['fact_ids'],True);short=c.split('.')[-1];f=files(c)
 if short=='dataset_quality_gate':
  cases=load(c,'fixtures/dataset_cases.json'); config=json.loads(f['cloudbuild.yaml']);q=config['steps'][0]; tr=config['steps'][1]
  nodes=[]
  for key in ['valid','missing_required_feature']:
   case=cases[key]
   nodes.extend([(case['snapshot_id'],['Recorded snapshot sha256: '+case['sha256']]),(q['id'],['Image: '+q['name'],'Command: '+' '.join(q['args']),'Required feature check: '+('present' if key=='valid' else 'missing')]),(tr['id'],['Policy path: '+('start only after quality passes' if key=='valid' else 'do not start after required failure')])])
  return diagram(nodes,[(0,1,'validate'),(1,2,'accepted policy path'),(3,4,'validate'),(4,5,'rejected policy path')],'Dataset gate contract: accepted versus missing-feature paths (not hosted run results)',l)
 if short=='model_behavior_tests':
  contract=load(c,'fixtures/behavior_contract.json'); cases=load(c,'fixtures/behavior_execution_cases.json')
  def panel(key):
   code='execution_case = '+pformat(cases[key])+'\ncontract = '+pformat(contract)+'\n# Check count, correspondence and shape before numerical tolerance.\n# Invoke the packaged path; inspect fatal test and dependent-stage results.'
   return walk(code,l)
  return {'type':'side_by_side','left_label':'Accepted fixture specification','right_label':'Regressed fixture specification','left':panel('accepted'),'right':panel('regressed'),'takeaway':'Reversed rows must fail correspondence even when numerical values look familiar.','lineage':l}
 if short=='model_release_quality_gate':
  return {'type':'side_by_side','left_label':'Fixed candidate evidence','right_label':'Predeclared acceptance contract','left':table('ds.release_evidence',l),'right':walk('contract = '+pformat(load(c,'fixtures/release_contract.json'))+'\n# Calculate rates and expected cost from supplied counts.\n# Require complete evidence and every operating predicate too.',l),'takeaway':'Cost eligibility cannot compensate for a failed fixed latency requirement.','lineage':l}
 if short=='pipeline_failure_recovery':
  contract=load(c,'fixtures/recovery_contract.json');cases=load(c,'fixtures/recovery_cases.json')
  before=walk('failure_fixture = '+pformat(cases['accepted'])+'\noutputs = '+pformat(contract['outputs'])+'\n# Failure is injected after the first upload, before remaining work.',l)
  after=walk('completed_fixture = '+pformat(cases['boundary_completed'])+'\nrequirements = '+pformat(contract['requirements'])+'\n# Verify existing content/generation and validation before reuse.\n# Second invocation must preserve uploads/generations and revalidate.',l)
  return {'type':'before_after','before':before,'after':after,'change_summary':'Required recovery boundary: retain verified completed output, create only missing output, and rerun required gates. These are fixture specifications, not computed run results.','lineage':l}
 if short=='pipeline_artifact_dependencies':
  cases=load(c,'fixtures/dependency_cases.json');code='dependency_cases = '+pformat(cases)+'\nconfig = '+pformat(json.loads(f['cloudbuild.yaml']))+'\n# Inspect producer/consumer identities independently of waitFor completion.\n# Supplied configuration requires repair before execution.'
 elif short=='staged_ml_promotion':
  code='config = '+pformat(json.loads(f['cloudbuild.yaml']))+'\ncontract = '+pformat(load(c,'fixtures/promotion_contract.json'))+'\n# Supplied configuration requires staging-quality and authorization edges.\n# Preserve the same artifact and expose secret references only to needed steps.\n# Inspect captured output for non-disclosure without displaying credentials.'
 else:
  case=load(c,'fixtures/lineage_cases.json')['valid']
  code='records = '+pformat(case)+'\nedge_checks = '+pformat(load(c,'fixtures/lineage_contract.json')['edge_checks'])+'\n# Resolve the selected registry version and originating run.\n# Compare each edge, download the exact generation, and verify content.\n# Inspect the recorded local commit with both required git commands.\n# Assert declared cases; report missing or mismatched edges explicitly.'
 return walk(code,l)

out={k:p[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for t in p['tiles']:
 tile={'tile_id':t['tile_id'],'title':t['title'],'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  c=s['concept_ids'][0]; step={k:copy.deepcopy(s[k]) for k in ['step_id','type','concept_ids']};step['lineage']={k:copy.deepcopy(s[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']};step['eyebrow']=G[c]['context']['concept_name'];step['title']=''
  if s['type']=='explainer':
   blocks=[]
   for tbid in s['teaching_block_ids']:
    tb=next(x for x in G[c]['teaching_blocks'] if c+'#'+x['id']==tbid); text=texts[c.split('.')[-1]][int(tb['id'][2:])-1]
    lineage=lin(c,[tbid],[c+'#'+fid for fid in tb['fact_ids']])
    blocks.extend(prose(x,lineage) for x in chunks(text))
   step['title']={'intro':'Set the boundary','mechanism':'Wire and verify the contract','example':'Follow the fixture','misconception':'Keep the distinction'}[next(x for x in G[c]['teaching_blocks'] if c+'#'+x['id']==s['teaching_block_ids'][0])['purpose']]
   if s['planned_visual_block_type']:blocks.append(visual(c,s))
   step['blocks']=blocks
  elif s['type'] in ['check','hands_on']:
   step['title']='Inspect the required evidence' if s['type']=='check' else 'Apply the contract to the fixture'
   # Only framing: interaction payload and rewards remain the interaction stage's responsibility.
   step['lede']='Use the supplied fictional fixture and the requirements you have just learned.'
  elif s['type']=='recap':
   step['title']='Carry the boundary forward';step['eyebrow']='Recap'; blocks=[]
   recaps={
    'mle.dataset_quality_gate':'Required dataset failure stops training; retain the snapshot and named check evidence.',
    'mle.model_behavior_tests':'Test the fitted package: count, correspondence and shape come before numerical tolerance.',
    'mle.model_release_quality_gate':'Every required acceptance condition must be complete and passing. Cost improvement cannot cancel a latency failure.',
    'mle.pipeline_artifact_dependencies':'Successful predecessors and matching immutable artifact inputs are separate requirements.',
    'mle.staged_ml_promotion':'Validation and accountable authorization apply to the exact promoted artifact; keep credentials out of records.',
    'mle.pipeline_failure_recovery':'Reuse only verified completed effects; retry missing work and required gates without duplicate uploads.',
    'mle.deployed_model_lineage_audit':'Verify lineage edges, exact artifact content and the existing code commit; never infer absent links from names.'}
   for rc in s['concept_ids']:
    tb=G[rc]['teaching_blocks'][1];blocks.append(prose(recaps[rc],lin(rc,[rc+'#'+tb['id']],[rc+'#'+f for f in tb['fact_ids']])))
   nxt=t['next_tile_id']; next_c=(next((x['concept_ids'][0] for x in p['tiles'] if x['tile_id']==nxt),None))
   if next_c is None:
    ordered_concepts=list(g['names']);next_c=ordered_concepts[ordered_concepts.index(t['concept_ids'][-1])+1]
   blocks.append({'type':'up_next','title':g['names'][next_c],'text':'Next: '+g['names'][next_c]+'.'})
   step['blocks']=blocks
  elif s['type']=='video':
   step['title']='Optional support';step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  tile['steps'].append(step)
 # Separate remediation for every distinct measured fact set, including the first hands-on.
 seen=set()
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  key=(tuple(s['concept_ids']),tuple(s['fact_ids']))
  if key in seen:continue
  seen.add(key); c=s['concept_ids'][0]; required=set(s['fact_ids']); related=[tb for tb in G[c]['teaching_blocks'] if required.intersection(c+'#'+f for f in tb['fact_ids']) and tb['purpose']=='mechanism']
  blocks=[]
  for tb in related:
   ids=[c+'#'+fid for fid in tb['fact_ids'] if c+'#'+fid in required]
   # Exact fact meaning is retained in remediation; no answer key or invented outcome.
   facts=[f['statement'] for f in G[c]['coverage']['required_facts'] if c+'#'+f['id'] in ids]
   for fid,text in zip(ids,facts):
    for part in chunks(short_fact(c,fid.split('#')[-1],text)):
     blocks.append(prose(part,lin(c,[c+'#'+tb['id']],[fid])))
  dataset_for={'dataset_quality_gate':'ds.dataset_snapshot','model_behavior_tests':'ds.behavior_inputs','model_release_quality_gate':'ds.release_evidence','pipeline_artifact_dependencies':'ds.artifact_records','staged_ml_promotion':'ds.artifact_records','pipeline_failure_recovery':'ds.artifact_records','deployed_model_lineage_audit':'ds.lineage_links'}
  blocks.insert(0,table(dataset_for[c.split('.')[-1]],lin(c,[c+'#'+tb['id'] for tb in related],s['fact_ids'],True)))
  contrast=texts[c.split('.')[-1]][-1];blocks.append(prose(contrast,lin(c,[c+'#'+G[c]['teaching_blocks'][-1]['id']],[c+'#'+f for f in G[c]['teaching_blocks'][-1]['fact_ids']])))
  tile['remediation_steps'].append({'step_id':t['tile_id']+f'.r{len(tile["remediation_steps"])+1:02d}','type':'remediation','concept_ids':[c],'title':'Rebuild the distinction','eyebrow':G[c]['context']['concept_name'],'blocks':blocks,'lineage':lin(c,[c+'#'+tb['id'] for tb in related],s['fact_ids'])})
 out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print([(t['tile_id'],len(t['steps']),len(t['remediation_steps'])) for t in out['tiles']])
