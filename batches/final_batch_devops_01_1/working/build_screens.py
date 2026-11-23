import json, re, copy, ipaddress
from pathlib import Path
P=Path('batches/final_batch_aws_devops.region.01_1')
plan=json.loads((P/'tile_plans.json').read_text())
gloss=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
registry=json.loads((P/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in gloss['bundles']}
assets={a['asset_id']:a for a in registry['assets']}
vocab=registry['scenarios'][0]['glossary_example_vocab']
# All concrete example tokens and dataset fields are read from the supplied inputs.
def token(s):
 assert s in vocab,s
 return vocab[vocab.index(s)]
def line(cid,tbs,facts,anchors=None):
 d={'concept_ids':[cid],'teaching_block_ids':tbs,'fact_ids':facts}
 if anchors is not None:d['anchors']=anchors
 return d
def prose(text,cid,tbs,facts,role='example'):
 return {'type':'prose','text':text,'role':role,'lineage':line(cid,tbs,facts)}
def table(aid,lin,cols=None):
 a=assets[aid]
 return {'type':'data_table','caption':a['title'],'asset_ref':{'asset_id':aid,'columns':cols or [c['name'] for c in a['columns']]},'lineage':copy.deepcopy(lin)}
def diagram(title,labels,lin,edges=None,kind='architecture'):
 nodes=[{'id':f'n{i}','label':v[0] if isinstance(v,tuple) else v,**({'fields':v[1]} if isinstance(v,tuple) else {})} for i,v in enumerate(labels)]
 return {'type':'diagram','diagram_kind':kind,'title':title,'nodes':nodes,'edges':[{'from':f'n{a}','to':f'n{b}','label':s} for a,b,s in (edges or [])],'layout':'manual','positions':{f'n{i}':{'x':(i%2)*420,'y':(i//2)*170} for i in range(len(nodes))},'alt_text':title+'. '+'; '.join(n['label']+(': '+', '.join(n.get('fields',[])) if n.get('fields') else '') for n in nodes),'lineage':copy.deepcopy(lin)}
intros=[
 'Make the sandbox context explicit before changing resources. A profile name starts the identity check; it does not replace it.',
 'For two Availability Zones, check both address fit and usable capacity. Complete the external IP-addressing and CIDR preparation first.',
 'Compare platform work with the application work the team retains, not just the word managed.',
 'Check which route table the subnet uses before comparing destination matches.',
 'Name tolerated downtime and tolerated data loss separately; they are different business requirements.',
 'Route the EC2 update and RDS parameter-check reports by the service boundary.',
 'Separate ordinary demand from the service requirement after a component fails.',
 'An unresolved event needs an accountable owner and a defined next responder.',
 'Evaluate the requested action and resource, not whether the policy looks permissive. Complete the external access-control preparation first.',
 'Read when the workflow starts, where jobs run and what steps declare. Logs provide execution evidence.',
 'Read throughput and instability together before interpreting a delivery report.',
 'Specify the event fields to select, then test both sides of that selection boundary.'
]
examples=[
 [f"Select {token('lab-operator')} explicitly with {token('--profile')}. The illustrative caller check shows Account: {token('[REDACTED_ACCOUNT]')} and Arn: arn:aws:iam::{token('[REDACTED_ACCOUNT]')}:user/{token('[REDACTED_OPERATOR]')}. Compare both with the supplied operator context.",f"The illustrative configure list Region row shows {token('us-west-2')}, Type {token('config-file')}, Location {token('~/.aws/config')}. That evidence answers configuration and origin, not caller identity. A command's explicit {token('--region')} option overrides this configured Region; keep the same explicit profile."],
 ['The allocation worksheet places separate, nonintersecting subnets inside the VPC in different zones. Compare usable addresses, not total addresses, with the requirement. The overlapping candidate remains invalid even though it fits inside the VPC.'],
 ['A Kubernetes API and ecosystem requirement points the comparison toward managed EKS, provided the team is willing to operate Kubernetes workloads. Without that dependency, compare the ECS scheduling option. Neither proposal transfers application operation to AWS; retain the compute-option qualification for EKS worker-node duties.'],
 [f"In the intended table, {token('10.20.2.10')} matches both {token('10.20.0.0/16')} and {token('0.0.0.0/0')}; the more specific prefix wins. {token('198.51.100.8')} uses the internet-gateway default when no more specific route matches. First verify association: without an explicit association, the subnet uses the main table, not necessarily the table you edited."],
 ['Compare each recovery approach with both business limits in the table. Meeting restoration time while losing too much recent data fails the data-loss requirement. Recent data alone does not establish timely restoration. These are illustrative business limits, not recommended AWS defaults.'],
 ['The EC2 OS-update report concerns customer guest-OS work. The RDS parameter-check report concerns customer-controlled engine configuration values, not AWS-managed OS maintenance. Name that boundary in the handoff; customer data and access duties remain.'],
 ['Both proposals have equal total capacity. Evaluate that capacity against ordinary demand, then evaluate independent surviving capacity against the post-loss service requirement. A larger single component can address demand without answering the failure requirement.'],
 ['Read the resource owner, process owner, initial responder, unresolved-issue condition and next recipient together. When the supplied checklist condition is reached, the established record identifies the recipient. These fictional team assignments and conditions are exercise inputs, not a universal escalation chain.'],
 ['Compare the object-read request with Action, Resource and Condition. An unmet condition or unmatched resource can leave no applicable allow: implicit deny. When an applicable Deny also covers the request, it overrides the Allow. The supplied table evaluates these identity-policy rules, not every AWS policy type.'],
 ['Follow the intended job and its selected runner, then distinguish uses actions from run commands. Inspect job and step logs from that same workflow execution. In the glossary’s illustrative case, two steps succeed and the third fails; declared steps alone would not establish those outcomes.'],
 ['For the same application, more deployments and shorter commit-to-production time concern throughput. A greater proportion needing intervention concerns change fail rate; recovery duration supplies the other instability measure. Keep all four measures together across reporting periods, rather than ranking individuals by one improving measure.'],
 [f"The pattern accepts source {token('lab.orders')} and detail-type {token('OrderReady')}. Test those values, then test a sample with detail-type {token('OrderCancelled')}. Also vary an omitted field: it is not required to match. Compare test results with the intended requirement before using a rule; these names are invented sample data."]
]
contrasts=[
 'A profile label is not caller evidence, and caller evidence is not a Region check.',
 'VPC containment does not excuse overlap, and total addresses do not establish usable capacity. One subnet cannot span zones.',
 'Managed does not mean AWS operates the application. EKS worker-node duties remain compute-dependent.',
 'Editing a table does not establish association. A default route does not override more specific matches or prove a working connection.',
 'RTO bounds restoration time; RPO bounds data loss measured in time. Neither substitutes for the other.',
 'EC2 guest-OS patching is customer work; RDS OS maintenance is AWS work. RDS customer configuration and data duties remain.',
 'Increasing one component’s size is not independent redundancy. Ordinary capacity and post-loss capacity answer separate requirements.',
 'Contacts alone are not an escalation path. Document when an unresolved issue moves on and to whom; name resource and process owners.',
 'An Allow elsewhere does not allow this request. Scope and conditions must match; applicable explicit deny wins.',
 'YAML declares steps; logs establish execution and status. Runner selection alone does not prove success.',
 'Frequent delivery alone does not describe stability. Interpret the combined evidence within application context.',
 'An event need not duplicate every field of a sample. Omitted fields are not required to match; positive and negative tests expose the boundary.'
]
recaps=[
 'Select the named profile explicitly. Check caller ARN and account separately from effective configuration and its origin. A command’s Region option overrides the configured Region.',
 'Require containment, nonoverlap, allowed subnet size and capacity after reservations. Use separate subnets for separate Availability Zones.',
 'ECS manages scheduling; managed EKS manages the Kubernetes control plane. Retain application duties and the compute-dependent worker-node qualification. Compare Kubernetes needs with team willingness.',
 'Establish explicit association or main-table fallback first. Prefer the most specific matching prefix. The attached internet-gateway default serves destinations without a more specific match.',
 'Derive RTO and RPO from business requirements. Compare recovery capabilities with both restoration-time and time-based data-loss limits.',
 'EC2 guest-OS updates remain customer work. RDS infrastructure and OS maintenance are AWS work; customer data, access and controlled engine configuration remain customer duties.',
 'Match capacity to demand. Separately evaluate independent surviving capacity for a component-failure constraint; equal totals do not settle availability.',
 'Identify resource and process owners. Assign event response and document both the unresolved-issue escalation condition and the next recipient.',
 'Match action, resource and conditions to identity-policy statements. Applicable explicit deny overrides allow; no applicable allow means implicit deny.',
 'Read triggers, jobs, runner selection and uses/run steps in the workflow. Verify actual execution and success or failure with that run’s job and step logs.',
 'Compare deployment frequency and change lead time with change fail rate and failed deployment recovery time. Interpret all four over time within application context, not as individual rankings.',
 'Patterns constrain named fields to acceptable values. Omitted fields need not match. Test matching and nonmatching samples before using a pattern in a rule.'
]
asset_by_index={2:'ds.container_ownership',4:'ds.recovery_options',5:'ds.service_responsibilities',7:'ds.ownership_escalation',8:'ds.identity_policy_evaluation',10:'ds.delivery_evidence'}
def visual(i,s,cid):
 lin=line(cid,s['teaching_block_ids'],s['fact_ids'],[cid+'#visual'])
 if i in asset_by_index:return [table(asset_by_index[i],lin)]
 if i==0:
  name=token('lab-operator');account=token('[REDACTED_ACCOUNT]');operator=token('[REDACTED_OPERATOR]')
  return [diagram('Illustrative operator-context checks',[
   (f'aws sts get-caller-identity --profile {name}',[f'Account: {account}',f'Arn: arn:aws:iam::{account}:user/{operator}']),
   (f'aws configure list --profile {name}',[f'Region Value: {token("us-west-2")}',f'Type: {token("config-file")}',f'Location: {token("~/.aws/config")}']),
   ('Command Region selection',['Keep the explicit named profile','An explicit --region REGION overrides the configured Region for this command'])],lin,kind='layers')]
 if i==1:
  a=assets['ds.subnet_candidates'];rows=[dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
  nodes=[(rows[0]['vpc_cidr'],['VPC range'])];edges=[]
  for r in rows:
   nodes.append((r['subnet_cidr'],[r['availability_zone'],f"Reserved: {r['reserved_addresses']}",f"Usable addresses: {r['usable_addresses']}"]))
   edges.append((0,len(nodes)-1,'inside VPC'))
  edges += [(1,2,'nonintersecting ranges'),(1,3,'candidate lies within first subnet: overlap')]
  return [diagram('Contained ranges: separate zones, separate usable-capacity checks',nodes,lin,edges,kind='container'),table(a['asset_id'],lin)]
 if i==3:
  vpc=token('10.20.0.0/16');default=token('0.0.0.0/0')
  return [diagram('Before and after explicit subnet association',[
   ('Subnet: before',['No explicit route-table association']),('VPC main route table',['Used by fallback before association']),
   ('Subnet: afterward',['Explicitly associated with intended table']),('Intended route table',[vpc,default+' → attached internet gateway']),
   (token('10.20.2.10'),['Matches both displayed prefixes; select the more specific /16']),
   (token('198.51.100.8'),['Select internet-gateway default when no more specific route matches'])],lin,[(0,1,'main-table fallback'),(2,3,'explicit association'),(3,4,'more specific match'),(3,5,'default match')],kind='network')]
 if i==6:
  a=assets['ds.capacity_proposals'];rows=[dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
  left=diagram(rows[0]['proposal'],[('Single component',['Loss removes this component’s capacity'])],lin)
  right=diagram(rows[1]['proposal'],[('Independent component A',['Capacity remains if the other component is lost']),('Independent component B',['Capacity remains if the other component is lost'])],lin)
  return [{'type':'side_by_side','left':left,'right':right,'left_label':rows[0]['proposal'],'right_label':rows[1]['proposal'],'takeaway':'Equal total capacity does not settle surviving capacity after one component is lost.','lineage':lin},table(a['asset_id'],lin)]
 if i==9:
  return [diagram('Workflow declaration versus illustrative execution evidence',[
   (token('.github/workflows'),['Workflow YAML location']),('on',['Triggering events']),('jobs / runs-on',['Job definitions / selected runner']),
   ('steps',['uses: referenced action','run: supplied command']),('Same-run job and step logs',['Inspect executed steps and their success or failure','Illustrative glossary case: first two steps succeeded; third failed'])],lin,[(0,1,'workflow declares'),(1,2,'trigger starts work'),(2,3,'job declares'),(3,4,'compare declaration with evidence')],kind='layers')]
 if i==11:
  pattern={token('source'):[token('lab.orders')],token('detail-type'):[token('OrderReady')]}
  # JSON literals are embedded as JavaScript declarations, not typed execution output.
  ready={token('source'):token('lab.orders'),token('detail-type'):token('OrderReady'),token('id'):token('OrderReady')}
  cancelled={**ready,token('detail-type'):token('OrderCancelled')}
  changed={**ready,token('id'):token('OrderCancelled')}
  snippets=[]
  notes=['Constrain source and detail-type to arrays of acceptable values.','Positive sample: both constrained values satisfy the pattern. id is omitted from the pattern.','Negative sample: detail-type differs from its acceptable value.','Only id changes from the positive sample. Because id is omitted, the matching decision is unchanged.']
  for name,obj,note in zip(['pattern','readyEvent','cancelledEvent','changedIdEvent'],[pattern,ready,cancelled,changed],notes):
   code=f'const {name} = '+json.dumps(obj,indent=2)+';'
   snippets.append({'type':'code_walkthrough','language':'javascript','code':code,'annotations':[{'start_line':1,'end_line':len(code.splitlines()),'text':note}],'reveal':'all','lineage':copy.deepcopy(lin)})
  return snippets
 raise ValueError(i)

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for i,t in enumerate(plan['tiles']):
 cid=t['concept_ids'][0];b=bundles[cid];facts={cid+'#'+f['id']:f['statement'] for f in b['coverage']['required_facts']};tb={cid+'#'+x['id']:x for x in b['teaching_blocks']}
 title=b['context']['concept_name']
 tile={'tile_id':t['tile_id'],'title':title,'summary':recaps[i],'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'title':title,'lineage':line(cid,s['teaching_block_ids'],s['fact_ids'],s['anchors'])}
  if s['type']=='explainer':
   step['eyebrow']='Learn';step['title']='Check the operating model' if s['step_id'].endswith('s01') else 'Read the sandbox case';blocks=[]
   for tid in s['teaching_block_ids']:
    x=tb[tid];fids=[cid+'#'+f for f in x['fact_ids']]
    if x['purpose']=='intro':blocks.append(prose(intros[i],cid,[tid],fids,'intro'))
    elif x['purpose'] in ['definition','mechanism']:
     # Split multi-fact mechanisms so each prose block teaches one idea.
     for fid in fids:blocks.append(prose(facts[fid],cid,[tid],[fid],x['purpose']))
    elif x['purpose']=='example':
     for text in examples[i]:blocks.append(prose(text,cid,[tid],fids,'example'))
    elif x['purpose']=='misconception':blocks.append(prose(contrasts[i],cid,[tid],fids,'misconception'))
   if s['planned_visual_block_type']:blocks.extend(visual(i,s,cid))
   step['blocks']=blocks
  elif s['type']=='video':
   step['title']='Follow the evidence';step['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
  elif s['type'] in ['check','hands_on']:
   step['eyebrow']='Review' if s['type']=='hands_on' else 'Check'
   step['title']='Review the supplied evidence' if s['type']=='hands_on' else 'Choose the supported conclusion'
   step['lede']='Read the supplied excerpts in this step and decide which conclusions are correct, defective or unsafe.' if s['planned_interaction_type'] in ['classify','choice'] else 'Inspect the supplied table and select the entries that satisfy the stated requirement.'
  elif s['type']=='recap':
   step['title']='Keep the distinctions';step['eyebrow']='Recap'
   allfacts=list(facts);alltb=list(tb)
   step['blocks']=[prose(recaps[i],cid,alltb,allfacts,'takeaway')]
   nexttitle=bundles[plan['tiles'][i+1]['concept_ids'][0]]['context']['concept_name'] if i+1<len(plan['tiles']) else 'Operate an EC2 instance'
   step['blocks'].append({'type':'up_next','title':'Next: '+nexttitle,'text':'Continue to '+t['next_tile_id']+'.'})
  tile['steps'].append(step)
 # Separate recovery routes for every distinct tested fact set.
 seen=set()
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  fids=s['fact_ids'];key=tuple(fids)
  if key in seen:continue
  seen.add(key)
  tids=[tid for tid,x in tb.items() if any(cid+'#'+f in fids for f in x['fact_ids'])]
  rid=f"{t['tile_id']}.r{len(tile['remediation_steps'])+1:02d}"
  blocks=[prose(facts[fid],cid,[tid for tid in tids if fid in [cid+'#'+f for f in tb[tid]['fact_ids']]],[fid],'definition') for fid in fids]
  blocks.append(prose(contrasts[i],cid,[cid+'#tb5'],[cid+'#'+f for f in tb[cid+'#tb5']['fact_ids']],'misconception'))
  # Same registered worksheet when one exists; other cases reuse the same glossary sample.
  aid=asset_by_index.get(i) or ({1:'ds.subnet_candidates',6:'ds.capacity_proposals'}.get(i))
  if aid:blocks.append(table(aid,line(cid,tids,fids)))
  else:
   context = {3:'Return to the same intended route table: distinguish the internal destination’s more specific match from the external destination’s default match.',0:'Return to the same lab-operator example: compare the caller check with the configuration check.',9:'Return to the same illustrative workflow: compare declared steps with that execution’s job and step logs.',11:'Return to the same lab.orders samples: contrast OrderReady with OrderCancelled while keeping the pattern fixed.'}[i]
   blocks.append(prose(context,cid,[cid+'#tb4'],[cid+'#'+f for f in tb[cid+'#tb4']['fact_ids']],'example'))
  tile['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':[cid],'title':'Separate the two kinds of evidence','eyebrow':'Review the contrast','lineage':line(cid,tids,fids),'blocks':blocks})
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
# Stage mistakes-to-avoid checks: plan equality, framing only, traceability,
# budgets, qualified ids, data references/columns, visual anchors, no outputs.
for t,ot in zip(plan['tiles'],out['tiles']):
 assert len(t['steps'])==len(ot['steps'])
 for s,os in zip(t['steps'],ot['steps']):
  for k in ['step_id','type','concept_ids']:assert s[k]==os[k]
  for k in ['teaching_block_ids','fact_ids']:assert s[k]==os['lineage'][k]
  if s['type'] in ['check','hands_on']:assert 'blocks' not in os and 'interaction' not in os
  if s['type'] in ['explainer','recap']:
   words=sum(len(bl['text'].split()) for bl in os['blocks'] if bl['type']=='prose')
   assert words<=s['word_budget'],(s['step_id'],words,s['word_budget'])
 def inspect(bl):
  if bl['type']=='prose':
   assert len(bl['text'].split())<=90
   assert 'lineage' in bl
   assert not re.search(r'\bvideo\b',bl['text'],re.I)
  for f in bl.get('lineage',{}).get('fact_ids',[]):assert '#f' in f
  for f in bl.get('lineage',{}).get('teaching_block_ids',[]):assert '#tb' in f
  assert not any(k in bl for k in ['output','result','computed_values','execution_provenance'])
  if bl['type']=='data_table':
   a=assets[bl['asset_ref']['asset_id']]
   assert set(bl['asset_ref']['columns'])<=set(c['name'] for c in a['columns'])
  for k in ['left','right']:
   if k in bl:inspect(bl[k])
 for os in ot['steps']+ot['remediation_steps']:
  for bl in os.get('blocks',[]):inspect(bl)
 for s,os in zip(t['steps'],ot['steps']):
  if any(a.endswith('#visual') for a in s['anchors']):assert any(t['concept_ids'][0]+'#visual' in bl.get('lineage',{}).get('anchors',[]) for bl in os['blocks'])
print('Checklist passed:',len(out['tiles']),'tiles,',sum(len(t['steps']) for t in out['tiles']),'planned steps,',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
