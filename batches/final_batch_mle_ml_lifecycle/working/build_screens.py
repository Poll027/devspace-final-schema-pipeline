import json, copy, re
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle')
P=json.loads((B/'tile_plans.json').read_text())
G=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
R=json.loads((B/'scenario_asset_registry.json').read_text())
GLOSS={x['context']['concept_id']:x for x in G['bundles']}
ASSETS={x['asset_id']:x for x in R['assets']}
# Screen prose is authored here; identifiers, lineage and fixture values are sourced below.
assertion='Use assert predicates for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.'
entry='In each existing Cloud Build steps item, name selects the execution image; args or script supplies the command. Wire the assigned function/test entry point there.'
deps='Give steps IDs and set waitFor to required preceding IDs: successful completion, not textual order, controls downstream execution.'
fatal='Keep required failures fatal: omit allowFailure and failing codes from allowExitCodes; a rejected Python gate must exit unsuccessfully.'
commit='Use the existing repository commit trigger and branch filter. Inspect actual stage results and resolved inputs for accepted and rejected fixtures.'
event='Use the existing Pub/Sub artifact/event trigger, payload bindings and filters. Inspect actual stage results and resolved inputs for accepted and rejected fixtures.'
yaml='With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.'
TEXT={
'dataset_quality_gate':[
'A data-quality gate makes named validation results a fatal boundary before training, not an ignorable warning.',
'Validate before training. Unexpected or missing features and invalid feature values should stop the affected path. Give each required schema/quality check a name and aggregate results under the supplied pass/fail policy. On failure, raise or return the declared failure result; do not call training.',
'Retain the tested snapshot and failed-check evidence so repaired data faces the same requirements. '+assertion+' '+entry,
deps+' '+fatal+' '+commit,
yaml,
'In the missing-required-feature fixture, preserve the snapshot identity and named failure, then reject without training. Wire the test image and command, set explicit waitFor dependencies, and keep rejection fatal. Use the configured commit trigger and inspect accepted/rejected results. Repaired data must pass the unchanged requirements.',
'A failure report is not a blocking gate if training still runs. Allowing required failures or their exit codes defeats the boundary.'
],
'model_behavior_tests':[
'Test the packaged inference path, including fitted preprocessing. An isolated estimator fed manually prepared inputs could miss a package defect.',
'Call the same packaged fitted preprocessing/model path used for inference. For each fixture, check expected row count, feature/target correspondence and output shape before values. Use np.testing.assert_allclose with explicitly declared tolerances for numerical comparisons.',
'Exercise malformed and boundary inputs; check explicit rejection whenever the contract disallows them. '+assertion+' '+entry,
deps+' '+fatal+' '+commit,
yaml,
'For the supplied valid fixture, check count, alignment and shape before comparing values with explicit tolerances. Exercise malformed/boundary cases and required rejection. Wire the existing entry point and dependencies with fatal failures. Inspect triggered stage results and parsed YAML fields; a local pass is not the pipeline verdict.',
'Right-looking numbers for the wrong rows are still a regression. Shape, correspondence and the packaged fitted path matter; required failures must block dependent stages.'
],
'model_release_quality_gate':[
'Release requires complete evidence for the exact candidate and all predeclared requirements. Aggregate improvement cannot replace a required predicate.',
'Compare the candidate with the accepted reference and predeclared quality requirements. Read evidence, evaluate every required predicate and name failed predicates on rejection. Calculate validation expected error cost from fixed deployment probabilities and error costs; include fixed latency/operating limits in eligibility.',
'Failed or incomplete required gates block promotion. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups have no defined rate. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
'Keep protected-test observations out of preprocessing fitting, model selection and tuning: using them leaks information into the chosen system. '+entry+' '+deps,
fatal+' '+event+' '+yaml,
'Consider candidate evidence with acceptable expected cost but a failed fixed latency check: reject and identify latency, not cost success as approval. Use fixed probabilities/costs and actual-class denominators, binding evidence to candidate identity. Configure image, command and waitFor without failure tolerance; inspect event-bound inputs and stage results. Keep protected tests out of fitting/tuning.',
'The gate is not an average of requirements. Any failed or incomplete required condition blocks promotion even if another metric improves.'
],
'pipeline_artifact_dependencies':[
'Stage order alone does not connect the right files. Validation must consume the same identified artifact that training produced.',
'Give reusable components explicit input/output artifacts across experiment and production environments. Record each stage’s consumed dataset/artifact identity, parameters and produced identity; filenames alone do not join outputs. Represent dependencies as a dictionary and check every required upstream identity against its downstream reference.',
'Require the relevant dataset/model validation result before a dependent stage consumes that artifact. '+assertion+' '+entry,
deps+' '+fatal+' '+event,
'Bind consumer args/substitutions to the immutable identifier produced by the declared upstream stage. Inspect actual run inputs to verify the edge, not merely stage order. '+yaml,
'If training produces one immutable artifact but validation names another, flag the mismatch despite similar filenames. Record consumed/produced identities and parameters. Bind consumers through args/substitutions, inspect actual inputs, and require relevant validation before dependent execution. Parse configuration, set waitFor, keep failures fatal, and inspect configured event-trigger results.',
'waitFor proves a completion dependency, not correct artifact consumption. Check completion and identity agreement separately.'
],
'staged_ml_promotion':[
'Carry one approved artifact through the existing test and production boundaries. A completed build is not deployment permission: retain validation and separate authorization.',
'Read the approved registered name/version and run/artifact link before staged deployment authorization. Continuous delivery checks compatibility in a test environment, then model validation before production. Preserve the verdict for that exact artifact, including offline requirements and supplied staged evidence.',
'Stay within permitted identity and approval scope; record accountable authorization rather than changing policy. Record approval, registry version, artifact identity and per-stage gate results. '+entry,
deps+' '+fatal+' '+event,
'Use availableSecrets.secretManager for approved Secret Manager version references and secretEnv only on the needed step. YAML holds references, not values. Use the authorized build/step identity; preserve separate promotion authorization. Check captured output for non-disclosure; never echo or serialize runtime credentials.',
'Edit and parse existing staging/production YAML: production must depend on staging quality and authorization for the identical immutable artifact. Test unauthorized promotion and inspect that production did not execute. '+yaml,
'Read approved registry/run/artifact links. Bind production to staging quality and authorization for that same immutable artifact; record offline/staged evidence, approval and stage results. Scope Secret Manager references to needed steps using secretEnv and the approved identity. Replay unauthorized promotion, inspect non-execution, parsed configuration and event inputs, and keep failures fatal. Check output without exposing credentials.',
'Training or staging success is not authorization. Validation and approval cover the exact artifact; credentials never belong in the promotion record.'
],
'pipeline_failure_recovery':[
'When a stage fails after an output upload, preserve valid completed effects, finish missing work and rerun gates without extra generations or hidden conflicts.',
'Locate the failed stage using execution status and retained artifact records; preserve successfully completed required-stage identities. Catch only the declared recoverable error with try/except, record it and apply the supplied recovery action. After repair, rerun the affected required quality check and stop if it fails; never bypass dataset/model gates.',
'Reuse a completed upstream artifact only when its recorded identity and required validation remain valid for the resumed stage. '+entry+' '+deps,
fatal+' '+event+' Distinguish the injected recoverable exception from unrelated failures. Retry from the verified artifact boundary and inspect that the retry and later required gates executed.',
[yaml,
'Limit partial effects to declared named Cloud Storage uploads. For each output, use blob.exists(), blob.reload() and its generation to retrieve existing bytes. Verify expected content hash and required validation; skip only a matching completed upload. Create missing output with blob.upload_from_filename(path, if_generation_match=0). On 412 Precondition Failed, re-read and verify the already-created output instead of overwriting. Conflicting content or failed validation stops recovery.',
'Inject failure after one upload, before remaining stage work. Assert recovery preserves its generation/hash, uploads only missing outputs, executes the retried stage and downstream gates, and fails for invalid existing output. Call recovery again on the completed fixture: assert no extra generations/uploads while still enforcing required validation.'],
'After the declared first upload, inspect its existence, generation, bytes, expected hash and validation. Skip only verified completion; create missing output with if_generation_match=0. On 412, re-read and verify instead of overwriting. Stop on conflicts or invalid content. Retry required work and downstream gates, then call recovery again: no extra uploads/generations, with validation enforced.',
'Recovery does not mean ignoring failure. Reuse requires verified identity and validation; never overwrite a conflict, and never catch unrelated failures as permission to resume.'
],
'deployed_model_lineage_audit':[
'Trace the active model to its training record, code and data. Similar deployment/tracking names do not establish provenance; inspect identity links pairwise.',
'Follow the served artifact to training execution, resolved configuration, code revision and dataset snapshot. Resolve the deployed registry version, artifact source and run link. Retrieve that run and compare dataset/configuration/artifact evidence with deployment and approval records.',
'Check identities pairwise. Report missing links or mismatches rather than guessing provenance from names. '+assertion+' Download the registry’s exact recorded artifact generation and verify its content identity against the lineage record.',
'Inspect the recorded local revision with git rev-parse --verify REVISION and git show REVISION. Verify the commit exists; copying its revision string is not verification.',
['Resolve deployed version, artifact source and originating run. Compare run dataset/configuration/artifact identities with deployment and approval. Download the exact recorded generation and verify content. Inspect the local commit with git rev-parse and git show. Flag the fixture where deployment uses one artifact but approval covers another. Preserve missing links and mismatches; do not infer unrecorded training sources from names.',
'Walk deployment → registry → artifact/run → recorded configuration/dataset, and code record → existing commit. Each edge can fail independently: retain the explicit missing/mismatched edge. Exact-generation content checks and local revision inspection make supplied evidence auditable; they cannot reconstruct an absent link by guessing.'],
'Matching names do not prove lineage. Report a missing/mismatched run or artifact link; an unverified revision string does not prove the commit exists.'
]}

def lineage(c,tbs=(),facts=(),anchors=()):
 return dict(concept_ids=[c],teaching_block_ids=list(tbs),fact_ids=list(facts),anchors=list(anchors))
def q(c,ids): return [c+'#'+x for x in ids]
def tb(c,i):return GLOSS[c]['teaching_blocks'][i-1]
def prose(c,i,text,facts=None):
 src=tb(c,i)
 return dict(type='prose',text=text,role={'intro':'intro','mechanism':'mechanism'}.get(src['purpose'],'example' if i==len(TEXT[c.split('.')[-1]])-1 else 'workflow'),lineage=lineage(c,[c+'#'+src['id']],q(c,src['fact_ids'] if facts is None else facts)))
def fixture(c,path):
 a=ASSETS['ws.'+c.split('.')[-1]]
 return json.loads(next(f['content'] for f in a['files'] if f['path']==path))
def diagram(c,title,labels,facts=()):
 return dict(type='diagram',diagram_kind='sequence',title=title,nodes=[{'id':'n'+str(i),'label':v} for i,v in enumerate(labels)],edges=[{'from':'n'+str(i),'to':'n'+str(i+1),'directed':True} for i in range(len(labels)-1)],alt_text=title+': '+' → '.join(labels),lineage=lineage(c,facts=q(c,facts),anchors=[c+'#visual']))
def code(c,source,notes):
 return dict(type='code_walkthrough',language='python',code=source,annotations=[{'start_line':1,'end_line':len(source.splitlines()),'text':notes}],reveal='all',lineage=lineage(c,anchors=[c+'#visual']))

def visual(c,s):
 short=c.split('.')[-1]
 if short=='dataset_quality_gate':
  contract=fixture(c,'fixtures/dataset_contract.json')
  return diagram(c,'Expected local fixture run boundaries — not captured results', ['Resolved input snapshot identity','Named checks: '+', '.join(contract['required_checks']),'Accepted quality → training permitted; rejected quality → training must not start','Retain snapshot and failed-check evidence'],['f1','f2','f3','f4'])
 if short=='model_behavior_tests':
  ct=fixture(c,'fixtures/behavior_contract.json')
  checks='Count, sample correspondence, shape '+ct['output_shape']+'; explicit rtol/atol; expected rejection'
  return dict(type='side_by_side',left_label='Acceptance contract',right_label='Regression contract',left=diagram(c,'Expected acceptance',[checks,'Packaged fitted path meets fixture contract','Fatal test stage permits dependent execution']),right=diagram(c,'Expected regression',[checks,'Structure/value regression or required rejection missing','Fatal failure: dependent execution must not start']),takeaway='These are expected local fixture paths, not captured run results.',lineage=lineage(c,anchors=[c+'#visual']))
 if short=='model_release_quality_gate':
  ct=fixture(c,'fixtures/release_contract.json')
  base='Compare accepted reference; cost and latency limits'
  return dict(type='side_by_side',left_label='All required predicates pass',right_label='Any required predicate fails or is incomplete',left=diagram(c,'Expected eligibility',[base,'Complete evidence bound to exact candidate','Promotion permitted by this gate']),right=diagram(c,'Expected rejection',[base,'A failed latency/operating check still rejects','Name failure; promotion blocked']),takeaway='Expected contract paths, not observed pipeline results.',lineage=lineage(c,anchors=[c+'#visual']))
 if short=='pipeline_artifact_dependencies':
  # Generate illustrative access code from the registered dictionary schema, not typed identity values.
  cases=fixture(c,'fixtures/dependency_cases.json'); stagekeys=list(cases['valid'])
  upstream=stagekeys[1]; downstream=stagekeys[2]
  src='import json\nwith open("fixtures/dependency_cases.json") as f:\n    cases = json.load(f)\nedges = cases["valid"]\nproducer = edges['+repr(upstream)+']\nconsumer = edges['+repr(downstream)+']\nassert producer["produced"] == consumer["consumed"]\n'
  return code(c,src,'Inspect consumed identities, parameters and produced identities. Check validation separately before dependent execution; output is computed later.')
 if short=='staged_ml_promotion':
  src='import json\nwith open("fixtures/promotion_cases.json") as f:\n    cases = json.load(f)\ncase = cases["wrong_artifact"]\napproval = case["approval"]\nidentity_matches = case["artifact_id"] == approval["artifact_id"]\nstaging_matches = case["artifact_id"] == case["staged_artifact_id"]\n'
  return code(c,src,'Compare approval and staged evidence with the promoted immutable identity. Compatibility, model validation and separate authorization remain required; this snippet is not a full approval function.')
 if short=='pipeline_failure_recovery':
  ct=fixture(c,'fixtures/recovery_contract.json'); names=list(ct['outputs'])
  return dict(type='before_after',before=diagram(c,'Injected partial-effect boundary (expected)',[ct['injection_point'],'Inspect '+names[0]+' generation, content identity and validation','Missing '+names[1]+' remains to be reconciled']),after=diagram(c,'Verified recovery contract (expected)',['Skip verified '+names[0]+'; create missing '+names[1]+' conditionally','On 412: reload and verify; stop on conflict','Retry required stage and downstream gates','Repeat: no extra uploads/generations; still validate']),change_summary='Contract states for the local simulator, not captured storage or stage output.',lineage=lineage(c,anchors=[c+'#visual']))
 if short=='deployed_model_lineage_audit':
  src='import json\nwith open("fixtures/lineage_contract.json") as f:\n    contract = json.load(f)\nfor edge in contract["edge_checks"]:\n    print(edge)\n'
  src='import json\nwith open("fixtures/lineage_cases.json") as f:\n    cases = json.load(f)\ncase = cases["valid"]\ndeployment = case["deployment"]\nregistered = case["registry"][deployment["registry_version"]]\nrun = case["runs"][registered["run_id"]]\nassert deployment["artifact_id"] == registered["artifact_id"]\nassert case["approval"]["artifact_id"] == deployment["artifact_id"]\ndataset = case["datasets"][run["dataset_id"]]\nconfiguration = case["configurations"][run["configuration_id"]]\ncode_record = case["code"][run["code_id"]]\n'
  return code(c,src,'Resolve the exact version and its recorded run, then compare identities pairwise. Missing keys are missing links, not permission to infer provenance. Complete the audit with exact-generation content verification and both local Git inspections; no verified verdict is supplied here.')
 raise ValueError(c)

TITLES={
'dataset_quality_gate':['Reject before training','Make the build boundary fatal','Missing feature: unchanged requirements'],
'model_behavior_tests':['Test the packaged fitted path','Wire fatal behavior tests','Check structure before numbers'],
'model_release_quality_gate':['Evaluate every release predicate','Isolate protected tests','Wire the event-driven release gate','Cost success is not release approval'],
'pipeline_artifact_dependencies':['Bind producers to consumers','Verify edges in resolved inputs','Completion is not artifact identity'],
'staged_ml_promotion':['Carry exact approval through staging','Scope credentials and authorization','Make production depend on quality and approval','Reject artifact substitution'],
'pipeline_failure_recovery':['Find a verified recovery boundary','Retry only declared recoverable failures','Reconcile partial uploads','Repeat safely without bypassing gates'],
'deployed_model_lineage_audit':['Walk the recorded identity chain','Audit exact content and code','Names are not lineage']}
CONTRAST={
'dataset_quality_gate':'A named failure with training still running is a report, not a gate.',
'model_behavior_tests':'Matching numbers are insufficient if row correspondence or shape is wrong.',
'model_release_quality_gate':'An improved cost cannot compensate for a failed or incomplete required gate.',
'pipeline_artifact_dependencies':'Successful waitFor completion does not prove the consumer used the producer’s artifact.',
'staged_ml_promotion':'Successful staging does not replace separate authorization for the exact artifact.',
'pipeline_failure_recovery':'A completed upload is reusable only after identity and validation checks; unrelated failures do not permit resumption.',
'deployed_model_lineage_audit':'Similar names cannot fill a missing or mismatched identity link.'}

def make_rem(c,s,n,tile):
 facts=s['lineage']['fact_ids']; local={x.split('#')[1] for x in facts}; blocks=[]; tbids=[]
 if s['type']=='check':
  short=c.split('.')[-1]
  pieces={
   'dataset_quality_gate':[(3,entry,['f6']),(4,deps+' '+fatal,['f7','f8']),(5,yaml,['f10'])],
   'model_behavior_tests':[(5,yaml,['f10'])],
   'pipeline_artifact_dependencies':[(4,event,['f9']),(5,'Bind consumer args/substitutions to the declared producer’s immutable artifact identifier, and inspect actual resolved run inputs to verify that edge.',['f10'])],
   'staged_ml_promotion':[(5,'Bind approved Secret Manager version references with availableSecrets.secretManager; expose them only to the needed step via secretEnv. YAML contains references, not values. Check captured output for non-disclosure: never echo or serialize runtime credentials.',['f10','f12'])],
   'pipeline_failure_recovery':[(4,event+' Distinguish the injected recoverable exception from unrelated failures; retry at the verified boundary and inspect actual retry and downstream required-gate execution.',['f8','f9'])],
   'deployed_model_lineage_audit':[(2,'Connect the served artifact to training execution, resolved configuration, code and dataset. Resolve the exact deployed registry version, artifact source and run link. Retrieve that recorded run; compare its dataset/configuration/artifact evidence with deployment and approval records.',['f1','f2','f3'])]
  }
  contrast=CONTRAST[short]
  if short=='model_release_quality_gate':
   if local=={'f7'}:
    selected=[(4,'Protected-test observations must not fit preprocessing, select a model or tune settings; using them leaks information into the chosen system.',['f7'])]
    contrast='Protected-test observations are not fitting or tuning data.'
   else:
    selected=[(5,yaml,['f12'])]
    contrast='Writing a YAML file is not enough: reload and inspect its required resolved fields.'
  else:selected=pieces[short]
  for i,text,fs in selected:
   blocks.append(prose(c,i,text,fs));tbids.append(c+'#'+tb(c,i)['id'])
  i=selected[-1][0]
  blocks.append(prose(c,i,contrast,[]))
  return dict(step_id=tile+'.r'+str(n).zfill(2),type='remediation',concept_ids=[c],title='Recheck: '+s['title'],blocks=blocks,lineage=lineage(c,tbids,facts))
 # Re-teach from mechanism blocks, not from example blocks that summarize multiple facts.
 for i in range(2,len(TEXT[c.split('.')[-1]])-1):
  src=tb(c,i); intersect=local.intersection(src['fact_ids'])
  if not intersect:continue
  tbids.append(c+'#'+src['id'])
  texts=TEXT[c.split('.')[-1]][i-1]
  if isinstance(texts,str):texts=[texts]
  for j,text in enumerate(texts):
   relevant=intersect
   if c=='mle.pipeline_failure_recovery' and i==5:relevant=intersect.intersection([['f10'],['f11'],['f12']][j])
   if relevant:blocks.append(prose(c,i,text,sorted(relevant)))
 # Clear contrast for the same registered workspace/fixtures.
 last=len(TEXT[c.split('.')[-1]])
 blocks.append(prose(c,last,CONTRAST[c.split('.')[-1]],[]))
 tbids.append(c+'#'+tb(c,last)['id'])
 return dict(step_id=tile+'.r'+str(n).zfill(2),type='remediation',concept_ids=[c],title='Recheck: '+s['title'],blocks=blocks,lineage=lineage(c,tbids,facts))

out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for tile in P['tiles']:
 title=tile['title'] if tile['title']!=tile['tile_id'] else 'Orchestrate Traceable Promotion'
 dst=dict(tile_id=tile['tile_id'],title=title,summary='Fictional classification lifecycle fixtures in a bounded local simulator; run evidence is produced in the exercise, not supplied as hosted Cloud Build results.',steps=[],remediation_steps=[])
 counts={}
 for ps in tile['steps']:
  cs=ps['concept_ids'];c=cs[0];short=c.split('.')[-1]
  s=dict(step_id=ps['step_id'],type=ps['type'],concept_ids=copy.deepcopy(cs),title='',lineage=dict(concept_ids=copy.deepcopy(cs),teaching_block_ids=copy.deepcopy(ps['teaching_block_ids']),fact_ids=copy.deepcopy(ps['fact_ids']),segment_ids=copy.deepcopy(ps['segment_ids']),anchors=copy.deepcopy(ps['anchors'])))
  if ps['type']=='explainer':
   idx=counts.get(c,0);counts[c]=idx+1;s['title']=TITLES[short][idx];s['blocks']=[]
   for bid in ps['teaching_block_ids']:
    i=int(bid.split('#tb')[1]);text=TEXT[short][i-1]
    for j,textpart in enumerate([text] if isinstance(text,str) else text):
     fs=None
     if short=='pipeline_failure_recovery' and i==5:fs=[['f10'],['f11'],['f12']][j]
     if short=='deployed_model_lineage_audit' and i==5:fs=['f1','f2','f3','f4','f6','f7']
     s['blocks'].append(prose(c,i,textpart,fs))
   if ps['planned_visual_block_type']:s['blocks'].append(visual(c,ps))
  elif ps['type'] in ('check','hands_on'):
   s['title']=('Inspect: ' if ps['type']=='check' else 'Apply: ')+GLOSS[c]['context']['concept_name']
   if ps['type']=='check':
    cap=ps['anchors'][0].split('#assessment:')[1]
    s['title']='Inspect: '+cap.replace('_',' ')
   # No teaching or interaction content on framing-only steps.
   dst['remediation_steps'].append(make_rem(c,s,len(dst['remediation_steps'])+1,tile['tile_id']))
  elif ps['type']=='video':
   s['title']='Pipeline walkthrough';s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
  elif ps['type']=='recap':
   s['title']='Keep the boundaries distinct';s['blocks']=[]
   takeaways={
    'dataset_quality_gate':'Validate data before training; preserve named failure evidence and keep rejection fatal.',
    'model_behavior_tests':'Test packaged fitted inference, checking structure and correspondence before numerical tolerances.',
    'model_release_quality_gate':'Require complete candidate evidence and every fixed quality/operating predicate; isolate protected tests.',
    'pipeline_artifact_dependencies':'Check completion dependencies and immutable producer/consumer identities separately.',
    'staged_ml_promotion':'Carry exact-artifact validation and separate accountable approval through staging to production.',
    'pipeline_failure_recovery':'Reconcile verified uploads, retry required work, and never bypass gates.',
    'deployed_model_lineage_audit':'Audit pairwise provenance links, exact-generation content and the existing local code commit.'}
   for rc in cs:
    b=prose(rc,len(TEXT[rc.split('.')[-1]]),takeaways[rc.split('.')[-1]],[])
    # Takeaways link to the actual supporting mechanism, not solely the distinction block.
    b['role']='takeaway';b['lineage']['teaching_block_ids']=q(rc,[x['id'] for x in GLOSS[rc]['teaching_blocks'] if x['purpose']=='mechanism'])
    recap_facts={
     'dataset_quality_gate':['f1','f2','f3','f4','f8'],
     'model_behavior_tests':['f1','f2','f3'],
     'model_release_quality_gate':['f1','f2','f3','f4','f7'],
     'pipeline_artifact_dependencies':['f3','f7','f10'],
     'staged_ml_promotion':['f3','f4','f13'],
     'pipeline_failure_recovery':['f3','f9','f11'],
     'deployed_model_lineage_audit':['f4','f6','f7']}
    b['lineage']['fact_ids']=q(rc,recap_facts[rc.split('.')[-1]])
    s['blocks'].append(b)
   nextc='mle.pipeline_artifact_dependencies' if tile['next_tile_id']==P['tiles'][1]['tile_id'] else 'mle.distribution_monitoring'
   s['blocks'].append(dict(type='up_next',title=G['names'][nextc],text='Next: '+tile['next_tile_id']))
  else:raise ValueError(ps['type'])
  dst['steps'].append(s)
 out['tiles'].append(dst)
(B/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('Written',B/'screens.json')
