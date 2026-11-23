import json, copy
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.03_2')
plan=json.loads((P/'tile_plans.json').read_text())
g=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
r=json.loads((P/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in g['bundles']}
assets={a['asset_id']:a for a in r['assets']}
def lin(cid, tb, fs, anchors=[]):
 return {'concept_ids':[cid], 'teaching_block_ids':[cid+'#'+t for t in tb], 'fact_ids':[cid+'#'+f for f in fs], 'anchors':anchors}
def prose(cid,text,tb,fs,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':lin(cid,tb,fs)}
def table(cid,aid,fs):
 return {'type':'data_table','asset_ref':{'asset_id':aid,'columns':[c['name'] for c in assets[aid]['columns']]},'lineage':lin(cid,['tb4'],fs)}
def ui(cid,aid,fs):
 a=assets[aid]; cols=a['columns']; rows=[dict(zip([c['name'] for c in cols],row)) for row in a['rows']]
 if aid=='ds.config_evaluations':
  panels=[('Rule settings',[(k,rows[0][k]) for k in ['selected_rule','resource_scope','parameters']])]+[(row['resource_id'],[(k,row[k]) for k in ['resource_id','compliance_result']]) for row in rows]
 else:
  row=rows[-1]
  panels=[('Cost budget',[(k,row[k]) for k in ['budget_id','scope','amount','period']]),('Single notification',[(k,row[k]) for k in ['notification_id','threshold_value','threshold_basis','recipient']])]
 def display(k,v):
  col=next(c for c in cols if c['name']==k)
  return k.replace('_',' ')+': '+str(v)+(' '+col['unit'] if 'unit' in col else '')
 nodes=[{'id':'panel'+str(i),'label':label,'kind':'UI panel','fields':[display(k,v) for k,v in vals]} for i,(label,vals) in enumerate(panels)]
 return {'type':'diagram','diagram_kind':'container','title':'Supplied settings and evidence','nodes':nodes,'edges':[],'layout':'manual','positions':{n['id']:{'x':0,'y':i*160} for i,n in enumerate(nodes)},'alt_text':'Read-only schematic of the supplied settings. '+'. '.join(n['label']+'; '+'; '.join(n['fields']) for n in nodes),'lineage':lin(cid,['tb3','tb4'],fs,[cid+'#visual'])}
out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='screens_part',tiles=[])
for ti,t in enumerate(plan['tiles']):
 cid=t['concept_ids'][0]; b=bundles[cid]; title=b['context']['concept_name']; aid=r['assets'][ti]['asset_id']
 tile={'tile_id':t['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 for ps in t['steps']:
  s={k:copy.deepcopy(ps[k]) for k in ['step_id','type','concept_ids']}
  s['lineage']={k:copy.deepcopy(ps[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}
  s['title']=title
  n=int(ps['step_id'].rsplit('s',1)[1]); fs=[f.split('#')[1] for f in ps['fact_ids']]
  if ps['type']=='explainer':
   if ti==0 and n==1:
    s['title']='Rule presence is not a passing result'
    s['blocks']=[prose(cid,'A Config managed rule evaluates supported resource configuration against its criteria and configured parameters. Its presence is setup evidence, not proof that every resource passed.',['tb1','tb2'],['f1']),prose(cid,'Choose the supplied rule, resource scope and parameters. Run or inspect its evaluation, comparing compliant and noncompliant samples. Read each resource ID and compliance result.',['tb3'],['f2','f3']),ui(cid,aid,fs)]
   elif ti==0:
    s['title']='Check both sides of the boundary'
    s['blocks']=[prose(cid,'For the supplied rule, compare the approved scope and parameters with the requirement, then inspect both sample evaluations. Tie each resource ID and compliance result to the rule criteria. The acceptable sample should pass; the prohibited sample should be flagged. A sample outside the configured scope cannot validate the intended in-scope criterion.',['tb4'],['f1','f2','f3'],'example'),table(cid,aid,fs),prose(cid,'If the prohibited sample is reported as compliant, inspect scope and parameters against the supplied requirement rather than accepting rule presence as success. Individual results matter. This detection check does not install remediation, and a compliance report does not establish malicious activity.',['tb4','tb5'],['f1','f2','f3'],'misconception')]
   else:
    row=dict(zip([c['name'] for c in assets[aid]['columns']],assets[aid]['rows'][-1]))
    s['title']='An alert has settings, not stopping power'
    s['blocks']=[prose(cid,'An AWS budget compares cost or usage with a configured amount over a selected period. Create a cost budget using the approved scope, amount and period; configure an actual or forecast threshold and the approved recipient.',['tb1','tb2','tb3'],['f1','f2']),prose(cid,f"Here the scope is {row['scope']}, the amount is {row['amount']} USD, and the period is {row['period']}. The single notification uses {row['threshold_value']} percent of the budget amount on an {row['threshold_basis']} basis, sent to {row['recipient']}. Compare the saved settings with the approved inputs and retain the recipient setting.",['tb4'],['f1','f2'],'example'),ui(cid,aid,fs),prose(cid,'A notification alerts recipients. It does not itself stop resources or cap spending; stopping requires separately configured actions. No resource-stopping actions are configured in this example.',['tb3','tb4','tb5'],['f3'],'misconception')]
  elif ps['type']=='check':
   s['title']='Check the individual evidence' if ti==0 else 'Check the notification settings'
   s['lede']='Read the supplied evidence and choose the interpretation that matches the approved settings and individual results.' if ti==0 else 'Compare the supplied notification settings with the approved inputs and choose the matching configuration.'
  elif ps['type']=='hands_on':
   s['title']='Review the configuration evidence' if ti==0 else 'Judge the budget notification excerpts'
   s['lede']='Read the supplied excerpts in this step and decide which correctly select the rule, scope and parameters and verify the individual sample results.' if ti==0 else 'Read the supplied excerpts in this step and decide which match the approved budget and single notification settings.'
  elif ps['type']=='recap':
   s['title']='Takeaways'
   text='The rule evaluates supported configuration against its criteria and parameters. Select the supplied rule, scope and parameters, then run or inspect evaluations for both sample configurations. Read individual resource IDs and compliance results: rule presence alone does not mean all resources passed.' if ti==0 else 'A budget compares cost or usage with an amount over a period. Match the approved scope, amount and period, plus the single notification’s threshold value, actual or forecast basis, and recipient. Notifications alert recipients; stopping resources needs separately configured actions.'
   s['blocks']=[prose(cid,text,[tb['id'] for tb in b['teaching_blocks']],['f1','f2','f3'],'takeaway')]
   if ti==0:
    s['blocks'].append({'type':'up_next','title':bundles[plan['tiles'][ti+1]['concept_ids'][0]]['context']['concept_name'],'text':'Next: comparing cost or usage with a budget amount over a selected period.'})
   else:
    s['blocks'].append({'type':'up_next','title':'Next: '+t['next_tile_id'],'text':'Continue to the next tile in this path.'})
  tile['steps'].append(s)
 # One contrast for each distinct measured fact set; the second budget task can reuse r01.
 tasks=[ps for ps in t['steps'] if ps['type'] in ['check','hands_on']]
 seen=set()
 for ps in tasks:
  fs=[f.split('#')[1] for f in ps['fact_ids']]
  if tuple(fs) in seen: continue
  seen.add(tuple(fs))
  rem={'step_id':t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2),'type':'remediation','concept_ids':[cid],'title':'Contrast the evidence','lineage':lin(cid,['tb3','tb4','tb5'],fs)}
  if ti==0:
   text='Choose the supplied rule, approved resource scope and parameters, then run or inspect evaluations for both sample configurations. Read each resource ID alongside its compliance result. Rule presence alone cannot distinguish an acceptable sample from a prohibited one.'
   if 'f1' in fs: text='The managed rule evaluates supported configuration against its criteria and configured parameters. '+text
   rem['blocks']=[prose(cid,text,['tb3','tb4','tb5'],fs),table(cid,aid,fs)]
  else:
   rem['blocks']=[prose(cid,'Match the cost budget’s approved scope, amount and period, then its single notification’s threshold value, actual or forecast basis, and approved recipient. A matching threshold alone is not enough if the basis or recipient differs. Compare the approved-input record with the saved-configuration record.',['tb3','tb4'],fs),table(cid,aid,fs)]
  tile['remediation_steps'].append(rem)
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote',sum(len(t['steps']) for t in out['tiles']),'steps and',sum(len(t['remediation_steps']) for t in out['tiles']),'remediations')
