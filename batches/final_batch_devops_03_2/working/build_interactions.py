import json, copy
from pathlib import Path
B=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((B/p).read_text())
plan=load('tile_plans.json'); screens=load('screens.json'); glossary=load('inputs/path_glossary_bundle.json'); registry=load('scenario_asset_registry.json')
bundles={b['context']['concept_id']:b for b in glossary['bundles']}
assets={a['asset_id']:a for a in registry['assets']}
def rows(a):
 d=assets[a];return [dict(zip([c['name'] for c in d['columns']],r)) for r in d['rows']]
cfg=rows('ds.config_evaluations'); budget=rows('ds.budget_notification'); approved,saved=budget

def dump(d):return json.dumps(d,indent=2)
def feedback(correct,incorrect,hints):return {'correct':{'message':correct},'incorrect':{'message':incorrect},'hints':hints}
def choice(prompt,opts):
 return {'public':{'prompt':prompt,'options':[{'option_id':o[0],'text':o[1]} for o in opts],'selection':'single','shuffle':True},'grading':{'correct_option_ids':[o[0] for o in opts if o[2]],'option_feedback':{o[0]:{'message':o[3]} for o in opts}}}
def classify(prompt,reviews,predicate):
 return {'public':{'prompt':prompt,'buckets':[{'bucket_id':'meets','label':'Meets the supplied review criteria'},{'bucket_id':'fails','label':'Fails the supplied review criteria'}], 'items':[{'item_id':f'review{i+1}','text':dump(r[0])} for i,r in enumerate(reviews)]},'grading':{'assignments':{f'review{i+1}':('meets' if predicate(r[0]) else 'fails') for i,r in enumerate(reviews)},'item_feedback':{f'review{i+1}':{'message':r[1]} for i,r in enumerate(reviews)}}}
output={'schema_version':plan['schema_version'],'kind':'interactions_part','path_id':plan['path_id'],'batch_id':plan['batch_id'],'tiles':[]}
for ti,t in enumerate(plan['tiles']):
 cid=t['concept_ids'][0]; bundle=bundles[cid]; interactions=[]
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if s['type']=='check' else 'stretch','grading_mode':'client','standalone':True,'anchors':s['anchors'],'measures':[]}
  for a in s['anchors']:
   if '#assessment:' in a:
    cap=a.split('#assessment:')[1]; anchor=next(x for x in bundle['assessment_anchors'] if x['capability']==cap)
    ix['measures'].append({'concept_id':cid,'capability':cap,'fact_ids':anchor['fact_ids']})
  if ti==0 and s['type']=='check':
   prompt='Read these supplied in-scope sample evaluation rows. Which conclusion is supported?\n```json\n'+dump(cfg)+'\n```'
   passrow=next(r for r in cfg if r['compliance_result']=='COMPLIANT'); failrow=next(r for r in cfg if r['compliance_result']!='COMPLIANT')
   ix.update(choice(prompt,[('individual',f"{passrow['resource_id']} passes and {failrow['resource_id']} is flagged; rule presence alone does not prove all resources passed.",True,'Each conclusion is tied to an individual resource ID and compliance result.'),('presence','Both samples passed because the supplied managed rule is present.',False,'Rule presence is setup evidence, not each resource’s compliance result. One supplied row is noncompliant.'),('all_fail','Both samples failed because one noncompliant result invalidates the compliant result.',False,'Read individual resource IDs and results. The compliant sample still has its own passing result.')]))
   ix['feedback']=feedback('You used both individual results, not just rule presence.','Tie each conclusion to its own evaluation row.',['Compare the two compliance results.','Does the existence of a rule tell you the outcome for each resource?'])
  elif ti==0:
   requirement={k:cfg[0][k] for k in ['selected_rule','resource_scope','parameters']}
   good={'selected_settings':requirement,'evaluation_rows':cfg,'compliance_evidence':'individual resource IDs and compliance results','remediation_performed':False}
   falsepass=copy.deepcopy(good);falsepass['evaluation_rows'][1]['compliance_result']=cfg[0]['compliance_result']
   presence=copy.deepcopy(good);presence['evaluation_rows']=[];presence['compliance_evidence']='rule presence alone'
   wrongscope=copy.deepcopy(good);wrongscope['selected_settings']['resource_scope']='scope excludes the supplied noncompliant sample'
   reviews=[(good,'The rule, scope and parameters match, both resource IDs and their expected results are retained, and no remediation is performed.'),(falsepass,'The supplied prohibited sample must be flagged. Reporting both samples as compliant fails the boundary check; inspect scope and parameters.'),(presence,'Rule presence alone omits both individual evaluations and cannot prove compliance.'),(wrongscope,'The scope excludes a required sample, so its result cannot validate the intended in-scope criterion.')]
   def valid(r):return r['selected_settings']==requirement and r['evaluation_rows']==cfg and r['compliance_evidence']==good['compliance_evidence'] and not r['remediation_performed']
   ix.update(classify('Read each proposed Config review excerpt and decide whether it meets ALL supplied criteria. Required settings:\n```json\n'+dump(requirement)+'\n```\nRequired sample evidence:\n```json\n'+dump(cfg)+'\n```\nBoth samples are in the approved scope. A valid review matches the rule, scope and parameters, retains each resource ID and its expected compliance result, does not accept rule presence alone, and performs no remediation.',reviews,valid))
   ix['feedback']=feedback('You checked settings, both sample results and the evidence boundary.','A complete review needs matching settings and both expected individual evaluations, without remediation.',['Check the selected scope before trusting a sample result.','Look for both resource IDs, not merely a rule name.'])
  elif s['type']=='check':
   fields=['threshold_value','threshold_basis','recipient']
   candidates=[{k:saved[k] for k in fields}]
   wrong=copy.deepcopy(candidates[0]);wrong['threshold_basis']='forecast' if approved['threshold_basis']=='actual' else 'actual';candidates.append(wrong)
   wrong=copy.deepcopy(candidates[0]);wrong['recipient']='';candidates.append(wrong)
   reasons=['All three settings match the approved inputs.','The threshold basis differs from the approved input; the same threshold value does not make actual and forecast interchangeable for this requirement.','The approved recipient is missing; a matching threshold alone is insufficient.']
   opts=[(f'option{i+1}',dump(c),all(c[k]==approved[k] for k in fields),reasons[i]) for i,c in enumerate(candidates)]
   ix.update(choice('Read the approved notification settings below. Which candidate matches the threshold value (percent of budget amount), actual or forecast basis, and recipient?\n```json\n'+dump({k:approved[k] for k in fields})+'\n```',opts))
   ix['feedback']=feedback('The threshold value, basis and recipient all match.','Compare all three settings; one matching field is not enough.',['Check the threshold basis separately from its value.','The recipient must also match the approved input.'])
  else:
   def review(r):
    return {'budget':{k:r[k] for k in ['budget_id','scope','amount','period']},'notifications':[{k:r[k] for k in ['notification_id','threshold_value','threshold_basis','recipient']}], 'resource_stopping_actions_configured':r['resource_stopping_actions_configured']}
   good=review(saved);req=review(approved)
   wrongbasis=copy.deepcopy(good);wrongbasis['notifications'][0]['threshold_basis']='forecast' if approved['threshold_basis']=='actual' else 'actual'
   wrongamount=copy.deepcopy(good);wrongamount['budget']['amount']=approved['amount']*2
   double=copy.deepcopy(good);double['notifications']*=2
   actions=copy.deepcopy(good);actions['resource_stopping_actions_configured']=True
   reviews=[(good,'The saved budget and its exactly one notification match every approved setting, with no resource-stopping actions.'),(wrongbasis,'The notification basis differs from the approved basis, even though its threshold and recipient match.'),(wrongamount,'The saved budget amount differs from the approved amount; matching notification settings do not fix that.'),(double,'Two notification entries violate the exactly-one requirement, even though their settings match.'),(actions,'Resource-stopping actions are configured, contrary to this notification-only task.')]
   ix.update(classify('Read each saved-settings excerpt and decide whether it meets ALL approved criteria below. The threshold value is a percent of the budget amount. A valid result has matching scope, amount and period, exactly one matching notification (threshold value, actual or forecast basis, and approved recipient), and no resource-stopping actions.\nApproved criteria:\n```json\n'+dump(req)+'\n```',reviews,lambda r:r==req))
   ix['feedback']=feedback('You checked the full saved budget, exactly one notification and the absence of stopping actions.','Check every budget and notification field, the notification count and the action setting.',['A matching threshold does not establish that the budget amount matches.','Inspect the full notification list and the action setting.'])
  if not interactions:
   sc=next(x for x in screens['tiles'] if x['tile_id']==t['tile_id'])
   rem=next((r for r in sc['remediation_steps'] if cid in r['concept_ids']),None)
   if rem:ix['feedback']['remediation_step_id']=rem['step_id']
  interactions.append({'step_id':s['step_id'],'interaction':ix})
 output['tiles'].append({'tile_id':t['tile_id'],'interactions':interactions})
(B/'interactions.json').write_text(json.dumps(output,indent=2)+'\n')
# Self-check: exact coverage/types, anchor fidelity, bare facts, source-free inspect tasks,
# derived keys, unique choices, feedback for every distractor, both classification buckets.
for t,ot in zip(plan['tiles'],output['tiles']):
 expected=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 assert [s['step_id'] for s in expected]==[i['step_id'] for i in ot['interactions']]
 for s,entry in zip(expected,ot['interactions']):
  ix=entry['interaction'];assert ix['type']==s['planned_interaction_type'];assert ix['anchors']==s['anchors']
  assert all('#' not in f for m in ix['measures'] for f in m['fact_ids'])
  if ix['type']=='choice':
   assert len(ix['grading']['correct_option_ids'])==1
   assert len({o['text'] for o in ix['public']['options']})==len(ix['public']['options'])
   assert set(ix['grading']['option_feedback'])=={o['option_id'] for o in ix['public']['options']}
  else:
   assert set(ix['grading']['assignments'].values())=={'meets','fails'}
   assert all('source' not in i for i in ix['public']['items'])
print('Wrote 4 interactions (2 choice, 2 classify); structural mistakes checklist passed.')
