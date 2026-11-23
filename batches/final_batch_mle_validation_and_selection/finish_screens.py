exec((B/'build_visuals.py').read_text())
TITLES={
 'mle.tile.019_020':'Metrics and acceptance criteria',
 'mle.tile.021_023':'Matched baselines and modeling approaches',
 'mle.tile.024_025':'Thresholds and candidate comparisons',
 'mle.tile.026_028':'Errors, slices and supplied mitigations',
 'mle.tile.029_032':'Recorded, repeatable validation choices',
 'mle.tile.033_033':'Document model risks without changing policy',
 'mle.tile.034_034':'Evaluate supplied foundation-model outputs'}
SHORT={
 'task_metric_selection':'Match the metric to the task', 'model_acceptance_criteria':'Precommit predictive and operating requirements',
 'reference_baseline':'Establish a training-fitted reference', 'model_approach_decision':'Choose among eligible matched alternatives',
 'sklearn_baseline_workflow':'Fit, predict and evaluate the bounded baseline', 'decision_threshold_selection':'Separate scores from decisions',
 'validation_candidate_comparison':'Compare eligible candidates on matched evidence', 'prediction_error_analysis':'Inspect the predefined failure group',
 'slice_evaluation':'Keep each slice’s population visible', 'subgroup_risk_mitigation':'Check subgroup and overall mitigation evidence',
 'experiment_metric_logging':'Verify a keyed experiment record', 'training_randomness':'Retain completed paired trials',
 'validation_regularization':'Select regularization from validation', 'bounded_hyperparameter_search':'Resolve and respect the search budget',
 'model_risk_documentation':'Preserve policy and supported limitations', 'foundation_model_baseline_evaluation':'Compare supplied outputs with the reference'}
TAKEAWAYS={
 'task_metric_selection':'Choose metrics by error consequences; cohort ratios do not establish individual-score calibration.',
 'model_acceptance_criteria':'Fix deployment probabilities, costs and acceptance bounds before comparison; operating eligibility stays separate.',
 'reference_baseline':'Fit the reference on training, then measure its frozen validation predictions.',
 'model_approach_decision':'Matched quality, operating and ownership evidence—not model labels—determines the eligible choice.',
 'sklearn_baseline_workflow':'Predict through fitted state and evaluate against aligned held-out labels.',
 'decision_threshold_selection':'Select the eligible cutoff on validation and freeze its score representation before protected testing.',
 'validation_candidate_comparison':'Exclude incomparable or ineligible records before ranking with fixed cost inputs.',
 'prediction_error_analysis':'Keep the predefined group, eligible count and same-cohort reference with observed failures.',
 'slice_evaluation':'Report slice counts and conditional quality without claiming an unsupported population disparity.',
 'subgroup_risk_mitigation':'Check representation and both subgroup and overall evidence; population weighting is not conditional harm.',
 'experiment_metric_logging':'Verify resolved settings, actual revision and artifact path against the keyed run.',
 'training_randomness':'Keep seeds and completed pairs; controlled randomness does not guarantee universal determinism.',
 'validation_regularization':'Use validation and eligibility, not training alone; penalty direction is estimator-specific.',
 'bounded_hyperparameter_search':'Resolve overrides before searching and keep protected-test evidence outside tuning.',
 'model_risk_documentation':'Preserve existing permissions and supported limitations; record exposure without reproducing secrets.',
 'foundation_model_baseline_evaluation':'Evaluate supplied outputs on aligned validation evidence without claiming application-building or training competence.'}
CONTRAST={
 'task_metric_selection':'Contrast predicted-positive precision with actual-positive recall; neither ratio proves individual-score calibration.',
 'model_acceptance_criteria':'Contrast a predictive bound pass with unresolved operating eligibility; one does not settle the other.',
 'reference_baseline':'Contrast training-derived reference state with validation-derived quality evidence; they have separate roles.',
 'model_approach_decision':'Contrast low cost with eligibility: a failed operating requirement excludes a record before ranking.',
 'sklearn_baseline_workflow':'Contrast producing predictions with evaluating them: matching held-out labels and fitted representation are still required.',
 'decision_threshold_selection':'Contrast an unchanged score with changed cutoff decisions; retain the validation-selected rule, not a protected-test rescue.',
 'validation_candidate_comparison':'Contrast a smaller cost from another cohort with an eligible matched record; only matched evidence can enter this ranking.',
 'prediction_error_analysis':'Contrast an error count with errors per eligible observation; the predefined group supplies the denominator.',
 'slice_evaluation':'Contrast an observed sample gap with a population claim; representation limits what the gap supports.',
 'subgroup_risk_mitigation':'Contrast subgroup-conditional harm with population-weighted contribution; neither replaces overall evidence or representation checks.',
 'experiment_metric_logging':'Contrast a printed run name with verified keyed lineage: resolved settings, revision and artifact location must agree.',
 'training_randomness':'Contrast controlled random sources with universal determinism; wins still need the completed matched-pair denominator.',
 'validation_regularization':'Contrast increasing Ridge alpha with increasing LogisticRegression C: their penalty directions differ.',
 'bounded_hyperparameter_search':'Contrast the default budget with the resolved keyword override; the latter bounds completed trials.',
 'model_risk_documentation':'Contrast documenting an out-of-scope grant with authorizing it; existing permissions do not change.',
 'foundation_model_baseline_evaluation':'Contrast evaluating supplied outputs with building an application; only aligned task-specific validation evidence is being assessed.'}
REM_ASSET={
 'task_metric_selection':'ds.metric_summary','model_acceptance_criteria':'ds.acceptance_terms','reference_baseline':'ds.reference_train',
 'model_approach_decision':'ds.approach_records','sklearn_baseline_workflow':'ds.orders_validation','decision_threshold_selection':'ds.threshold_records',
 'validation_candidate_comparison':'ds.candidate_records','prediction_error_analysis':'ds.slice_observations','slice_evaluation':'ds.slice_summary',
 'subgroup_risk_mitigation':'ds.mitigation_records','experiment_metric_logging':'ds.execution_contract','training_randomness':'ds.paired_trials',
 'validation_regularization':'ds.regularization_records','bounded_hyperparameter_search':'ds.search_trials','model_risk_documentation':'ds.risk_policy_evidence',
 'foundation_model_baseline_evaluation':'ds.foundation_outputs'}
def prose(text,cid,tbid,fids,role):
 # Split a long paragraph only at sentence boundaries; every fragment retains its qualified provenance.
 out=[]
 for paragraph in text.split('\n\n'):
  sentences=re.split(r'(?<=[.!?])\s+(?=[A-Z])',paragraph); chunk=''
  for sent in sentences:
   if chunk and len((chunk+' '+sent).split())>90:
    out.append(chunk);chunk=sent
   else:chunk=(chunk+' '+sent).strip()
  if chunk:out.append(chunk)
 return [{'type':'prose','text':p,'role':role,'lineage':{'concept_ids':[cid],'teaching_block_ids':[tbid] if tbid else [],'fact_ids':fids}} for p in out]

def main():
 out={k:copy.deepcopy(P[k]) for k in ('schema_version','path_id','batch_id')};out['kind']='screens_part';out['tiles']=[]
 plans={t['tile_id']:t for t in P['tiles']}
 for t in P['tiles']:
  tile={'tile_id':t['tile_id'],'title':TITLES[t['tile_id']],'summary':'Apply the supplied fictional order-task evidence within fixed validation and policy boundaries.','steps':[],'remediation_steps':[]}
  for ps in t['steps']:
   cid=ps['concept_ids'][0];short=cid.removeprefix('mle.');name=SHORT[short]
   st={'step_id':ps['step_id'],'type':ps['type'],'concept_ids':copy.deepcopy(ps['concept_ids']),'required':True,'eyebrow':{'explainer':'Work the evidence','video':'Optional supporting media','check':'Quick check','hands_on':'Your turn','recap':'Keep the rule'}[ps['type']],'title':name,'lineage':lin(ps)}
   st['lineage']['anchors']=copy.deepcopy(ps['anchors']);st['lineage']['segment_ids']=copy.deepcopy(ps['segment_ids'])
   if ps['type'] in ('check','hands_on'):
    st['title']=('Check: ' if ps['type']=='check' else 'Practice: ')+name
    st['lede']='Use the supplied order-task evidence and the fixed rule.'
   elif ps['type']=='video':
    st['title']='Supporting media: '+name
    st['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
   elif ps['type']=='recap':
    st['title']='Carry these decisions forward';st['blocks']=[]
    for c in ps['concept_ids']:
     key=c.removeprefix('mle.');bundle=bundles[c]
     # A takeaway consolidates facts already taught; provenance points to that concept’s teaching bank.
     tb=bundle['teaching_blocks'][-1]
     newblocks=prose(TAKEAWAYS[key],c,None,[c+'#'+f['id'] for f in bundle['coverage']['required_facts']],'takeaway')
     for block in newblocks:
      block['lineage']['teaching_block_ids']=[c+'#'+bank['id'] for bank in bundle['teaching_blocks'] if bank['fact_ids']]
     st['blocks']+=newblocks
    nt=plans.get(t['next_tile_id'])
    next_c=nt['steps'][0]['concept_ids'][0] if nt else bundles[c]['context']['blocked_future_concepts'][0]
    next_name=G['names'][next_c]
    st['blocks'].append({'type':'up_next','title':next_name,'text':'Next: '+next_name+'.'})
   else:
    st['blocks']=[]
    for qtb in ps['teaching_block_ids']:
     c,tbid=qtb.split('#');key=c.removeprefix('mle.');idx=next(i for i,tb in enumerate(bundles[c]['teaching_blocks']) if tb['id']==tbid);tb=bundles[c]['teaching_blocks'][idx]
     st['blocks']+=prose(TEXT[key][idx],c,qtb,[c+'#'+f for f in tb['fact_ids']],tb['purpose'])
    if ps['planned_visual_block_type']:st['blocks']+=visuals(ps)
    if ps['teaching_block_ids']:
     tbid=ps['teaching_block_ids'][0].split('#')[1];tb=next(x for x in bundles[cid]['teaching_blocks'] if x['id']==tbid)
     suffix={'intro':'','definition':' — working rule','mechanism':' — apply the rule','example':' — read the fixture','misconception':' — keep the distinction'}.get(tb['purpose'],'')
     st['title']=name+suffix
   tile['steps'].append(st)
  # One remediation per distinct planned measured fact set. First check and hands-on for every concept are covered.
  seen=set();rnum=0
  for ps in t['steps']:
   if ps['type'] not in ('check','hands_on'):continue
   key=(tuple(ps['concept_ids']),tuple(sorted(ps['fact_ids'])))
   if key in seen:continue
   seen.add(key);rnum+=1;cid=ps['concept_ids'][0];short=cid.removeprefix('mle.');bundle=bundles[cid]
   rem={'step_id':t['tile_id']+f'.r{rnum:02d}','type':'remediation','required':False,'concept_ids':copy.deepcopy(ps['concept_ids']),'eyebrow':'Try one contrast','title':SHORT[short]+' — '+('check reset' if ps['type']=='check' else 'practice reset'),'blocks':[],'lineage':{'concept_ids':copy.deepcopy(ps['concept_ids']),'teaching_block_ids':[],'fact_ids':[]}}
   needed=set(ps['fact_ids']);selected=[]
   candidates=[(i,tb) for i,tb in enumerate(bundle['teaching_blocks']) if tb['purpose'] in ('definition','mechanism') or (tb['purpose']=='example' and len(tb['content'].split())<100)]
   while needed:
    idx,tb=max(candidates,key=lambda pair:len(needed & {cid+'#'+f for f in pair[1]['fact_ids']}))
    hit=needed & {cid+'#'+f for f in tb['fact_ids']}
    if not hit:raise ValueError(('uncovered remediation facts',needed))
    selected.append((idx,tb));needed-=hit;candidates.remove((idx,tb))
   for idx,tb in sorted(selected):
    fids=[cid+'#'+f for f in tb['fact_ids']];qtb=cid+'#'+tb['id']
    rem['blocks']+=prose(TEXT[short][idx],cid,qtb,fids,tb['purpose'])
    rem['lineage']['teaching_block_ids'].append(qtb)
    rem['lineage']['fact_ids']+=fids
   rem['lineage']['fact_ids']=list(dict.fromkeys(rem['lineage']['fact_ids']))
   # The contrast uses that concept’s same registered evidence and no alternate population.
   contrast_blocks=prose(CONTRAST[short],cid,None,rem['lineage']['fact_ids'],'mental_model')
   for block in contrast_blocks:block['lineage']['teaching_block_ids']=copy.deepcopy(rem['lineage']['teaching_block_ids'])
   rem['blocks']+=contrast_blocks
   if short=='bounded_hyperparameter_search':
    # Do not display future trial counts as executed remediation evidence.
    rem['blocks']+=visuals({**ps,'teaching_block_ids':rem['lineage']['teaching_block_ids'],'fact_ids':rem['lineage']['fact_ids']})
   elif short=='foundation_model_baseline_evaluation':
    rem['blocks']+=visuals({**ps,'teaching_block_ids':rem['lineage']['teaching_block_ids'],'fact_ids':rem['lineage']['fact_ids']})
   else:rem['blocks'].append(table({**ps,'teaching_block_ids':rem['lineage']['teaching_block_ids'],'fact_ids':rem['lineage']['fact_ids']},REM_ASSET[short]))
   tile['remediation_steps'].append(rem)
  out['tiles'].append(tile)
 # Stable block IDs are generated, never separately typed.
 def assign(blocks,prefix):
  for i,b in enumerate(blocks,1):
   b['block_id']=prefix+f'.b{i:02d}'
   for field in ('left','right'):
    if isinstance(b.get(field),dict):assign([b[field]],b['block_id']+'.'+field)
 for tile in out['tiles']:
  for st in tile['steps']+tile['remediation_steps']:assign(st.get('blocks',[]),st['step_id'])
 (B/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('Wrote',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
 return out
OUT=main()
