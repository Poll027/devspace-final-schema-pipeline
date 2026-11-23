from build_screens import *
from collections import Counter

def lineage(cids,fids=(),tbs=(),anchors=()):
 return {'concept_ids':list(cids),'fact_ids':list(fids),'teaching_block_ids':list(tbs),'anchors':list(anchors)}
def prose(text,cid,fids,tbs,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':lineage([cid],fids,tbs)}
def diagram(labels,lin,title,edges=(),kind='mapping'):
 nodes=[{'id':f'n{i+1}','label':x,'kind':'callout'} for i,x in enumerate(labels)]
 return {'type':'diagram','diagram_kind':kind,'title':title,'nodes':nodes,'edges':[{'from':f'n{a+1}','to':f'n{b+1}','label':l,'directed':True} for a,b,l in edges], 'layout':'manual','positions':{n['id']:{'x':(i%3)*320,'y':(i//3)*120} for i,n in enumerate(nodes)},'alt_text':title+': '+ '; '.join(labels),'lineage':copy.deepcopy(lin)}
def visual(ps,cid):
 i=C.index(cid); vt=ps['planned_visual_block_type']; lin=lineage([cid],ps['fact_ids'],ps['teaching_block_ids'],[cid+'#visual'])
 if vt=='data_table':
  asset=next(a for a in registry['assets'] if a['asset_id']==('ds.orders_restart_runbook' if i==2 else 'ds.orders_review_handoff'))
  return {'type':'data_table','asset_ref':{'asset_id':asset['asset_id'],'columns':[x['name'] for x in asset['columns']]},'caption':asset['title']+' — fictional supplied evidence','lineage':lin}
 if vt=='process_flow':
  labels=V[i]; nodes=[{'id':f'n{j+1}','label':v,'kind':'step'} for j,v in enumerate(labels)]
  nodes[3]['kind']='decision'; nodes[4]['kind']='end'
  es=[(0,1,'full listing'),(1,2,'automatic service request'),(2,3,'response received'),(3,2,'more results: next request'),(3,4,'no results remain'),(0,5,'bounded collection'),(5,6,'retain continuation'),(6,7,'same explicit profile and Region'),(7,5,'collect remainder')]
  return {'type':'process_flow','title':D[i][0],'direction':'LR','nodes':nodes,'edges':[{'from':f'n{a+1}','to':f'n{b+1}','label':l} for a,b,l in es],'alt_text':'Automatic collection follows requests and responses until no results remain. Bounded --max-items collection resumes NextToken with --starting-token, keeping the same explicit profile and Region. --page-size changes service-call size, not total output.','lineage':lin}
 if vt=='side_by_side' and i==6:
  return {'type':'side_by_side','left_label':'Publisher: tagged publication','right_label':'Consumer: exact-content retrieval','left':diagram(['Approved publisher identity','REGISTRY/REPOSITORY:TAG','docker push','Record published digest','Check publisher access'],lin,'Publication',[(0,2,'under this identity'),(1,2,'reference'),(2,3,'record content identity')]),'right':diagram(['Approved consumer identity','REGISTRY/REPOSITORY@sha256:DIGEST','docker pull','Use the recorded published digest','Check consumer access'],lin,'Consumption',[(0,2,'under this identity'),(1,2,'reference'),(3,1,'same digest')]),'takeaway':'The tag reference publishes; the recorded digest selects exact content. Check each approved identity’s access separately.','lineage':lin}
 if vt=='side_by_side' and i==12:
  return {'type':'side_by_side','left_label':'Declared expectation','right_label':'Changed live property','left':diagram(['Bucket: supported explicitly declared property','Supplied declared value A'],lin,'Expected',[(0,1,'declares')]),'right':diagram(['Same checked bucket property','Current value B','Wait for completed drift detection','Inspect expected / actual difference','Detection does not repair'],lin,'Actual',[(0,1,'current value'),(2,3,'then inspect')]),'takeaway':'Compare the expected/actual pair after completed detection. Unsupported or undeclared properties may not be checked.','lineage':lin}
 if vt=='code_walkthrough':
  # The code anchor permits side_by_side; no YAML language in the code block schema.
  return {'type':'side_by_side','left_label':'Provider and role trust','right_label':'Workflow and boundary tests','left':diagram(V[i][:4],lin,'Trust context',[(0,1,'configure issuer as provider'),(1,2,'aud restriction'),(1,3,'sub restriction')]),'right':diagram(['Workflow id-token: write','AWS credential action: approved role','Approved token context: expect success','Unapproved repository/branch: expect rejection'],lin,'Workflow review',[(0,1,'configure workflow'),(1,2,'approved case'),(1,3,'negative case')]),'takeaway':'Review the issuer and both aud/sub restrictions alongside the credential action’s approved role. Token permission alone does not establish role trust.','lineage':lin}
 # Registered images do not exist: use labelled UI/architecture diagrams instead.
 edges={0:[(0,1,'create'),(1,2,'activate'),(2,3,'inside environment'),(3,4,'use this interpreter'),(5,4,'confirm separately before script')],3:[(0,1,'containers share'),(2,0,'may replace'),(0,3,'phase observation'),(3,4,'inspect status'),(3,5,'inspect events'),(3,6,'inspect intended output')],4:[(0,1,'inspect'),(1,2,'verify'),(2,3,'before connecting'),(3,4,'then query'),(4,5,'verify data separately')],5:[(0,1,'overwrite case'),(1,2,'restore selected version'),(2,3,'creates'),(0,4,'simple-delete case'),(4,5,'undo deletion'),(0,6,'different permanent operation'),(7,1,'check recoverability window')],7:[(0,1,'attest this file'),(1,2,'bind provenance'),(0,3,'upload same file'),(3,4,'download integrity'),(4,5,'verify extracted file')],8:[(0,1,'declares'),(1,2,'Type'),(1,3,'Properties'),(1,4,'Ref'),(3,5,'approved declaration'),(5,6,'verify deployment')],9:[(0,3,'identify secret'),(1,3,'authorized runtime identity'),(2,3,'required permission'),(3,4,'use returned value'),(4,5,'verify without display')],11:[(0,1,'open results'),(1,2,'identify affected resource'),(2,5,'compare with evaluation and parameters'),(3,5,'evaluation'),(4,5,'parameters'),(5,6,'governing policy decides')],13:[(0,1,'inspect first failure'),(1,2,'follow subsequent events'),(2,3,'complete outcome'),(2,4,'failed outcome')],14:[(0,1,'approved assignment'),(1,4,'use role credentials'),(4,5,'inspect'),(5,6,'verify permission evidence')],15:[(0,4,'cluster scope'),(1,4,'namespace scope'),(2,4,'service account'),(3,4,'role'),(4,5,'must match'),(6,7,'supplies to associated Pods'),(5,8,'verify identity-specific access')],17:[(0,1,'bounded request'),(1,2,'returned field'),(1,3,'returned field'),(1,4,'returned field'),(1,5,'issued lifetime ends')],18:[(1,2,'required trust'),(2,3,'scoped role permissions'),(4,5,'different authorization model')]}.get(i,[])
 return diagram(V[i],lin,D[i][0],edges,'timeline' if i==17 else ('architecture' if i in [15,18] else 'mapping'))

def authored_blocks(ps):
 cid=ps['concept_ids'][0]; i=C.index(cid); d=D[i]; b=B[cid]; tbs={x['id']:x for x in b['teaching_blocks']}; facts={x['id']:d[1][j] for j,x in enumerate(b['coverage']['required_facts'])}; blocks=[]
 for qualified in ps['teaching_block_ids']:
  tb=tbs[qualified.partition('#')[2]]; fids=[cid+'#'+f for f in tb['fact_ids']]
  if tb['purpose'] in ['definition','mechanism']:
   for f in tb['fact_ids']: blocks.append(prose(facts[f],cid,[cid+'#'+f],[qualified],tb['purpose']))
  else:
   idx={'intro':2,'example':3,'misconception':4}[tb['purpose']]
   blocks.append(prose(d[idx],cid,fids,[qualified],tb['purpose']))
 if ps['planned_visual_block_type']:
  blocks.append(visual(ps,cid))
 return blocks

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for t in plan['tiles']:
 topics=[D[C.index(cid)][0] for cid in t['concept_ids']]
 tile={'tile_id':t['tile_id'],'title':' / '.join(topics),'summary':'Inspect the supplied evidence and distinguish what each check establishes.','steps':[],'remediation_steps':[]}
 seen=set()
 for ps in t['steps']:
  cid=ps['concept_ids'][0]; i=C.index(cid)
  s={'step_id':ps['step_id'],'type':ps['type'],'concept_ids':copy.deepcopy(ps['concept_ids']),'title':D[i][0],'eyebrow':'Orders sandbox · '+ps['type'].replace('_',' '),'lineage':lineage(ps['concept_ids'],ps['fact_ids'],ps['teaching_block_ids'],ps['anchors'])}
  s['lineage']['segment_ids']=copy.deepcopy(ps['segment_ids'])
  if ps['type']=='explainer':
   s['blocks']=authored_blocks(ps)
   # Label repeated screens by the planned teaching purpose, not duplicate titles.
   purposes=[q.partition('#')[2] for q in ps['teaching_block_ids']]
   if purposes and purposes[0]=='tb4': s['title']='Work through the evidence: '+D[i][0]
   elif purposes and purposes[0]=='tb3': s['title']='The verification sequence: '+D[i][0]
  elif ps['type']=='video':
   s['title']='A closer look: '+D[i][0];s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
  elif ps['type'] in ['check','hands_on']:
   s['title']=('Review ' if ps['type']=='hands_on' else 'Check ')+D[i][0][0].lower()+D[i][0][1:]
   s['lede']=('Read the supplied excerpts in this step and decide which are correct, defective or unsafe.' if ps['planned_interaction_type'] in ['classify','choice'] and ps['type']=='hands_on' else 'Read the supplied evidence in this step and choose the interpretation it supports.')
   rem_fids=([cid+'#'+f['id'] for f in B[cid]['coverage']['required_facts']] if ps['type']=='hands_on' else ps['fact_ids'])
   key=(cid,tuple(rem_fids))
   if key not in seen:
    seen.add(key); fids=rem_fids; related=[cid+'#'+tb['id'] for tb in B[cid]['teaching_blocks'] if set(tb['fact_ids']) & {f.partition('#')[2] for f in fids}]
    rem={'step_id':t['tile_id']+f'.r{len(tile["remediation_steps"])+1:02d}','type':'remediation','required':False,'concept_ids':[cid],'title':'One contrast: '+D[i][0],'eyebrow':'Review the distinction','lineage':lineage([cid],fids,related),'blocks':[]}
    for f in fids:
     j=next(j for j,x in enumerate(B[cid]['coverage']['required_facts']) if cid+'#'+x['id']==f)
     supporting=[q for q in related if f.partition('#')[2] in next(tb['fact_ids'] for tb in B[cid]['teaching_blocks'] if tb['id']==q.partition('#')[2])]
     rem['blocks'].append(prose(D[i][1][j],cid,[f],supporting))
    # Reuse the scenario's misconception contrast, with its own factual lineage.
    mtb=next(tb for tb in B[cid]['teaching_blocks'] if tb['purpose']=='misconception')
    rem['blocks'].append(prose(D[i][4],cid,[cid+'#'+f for f in mtb['fact_ids']],[cid+'#'+mtb['id']],'misconception'))
    if i in [2,10]: rem['blocks'].append(visual(next(p for p in t['steps'] if p['type']=='explainer' and p['concept_ids']==[cid] and p['planned_visual_block_type']),cid))
    tile['remediation_steps'].append(rem)
  elif ps['type']=='recap':
   s['title']='Keep these distinctions';s['blocks']=[]
   for rcid in ps['concept_ids']:
    j=C.index(rcid); rb=B[rcid];s['blocks'].append(prose(D[j][5],rcid,[rcid+'#'+f['id'] for f in rb['coverage']['required_facts']],[rcid+'#'+tb['id'] for tb in rb['teaching_blocks'] if tb['fact_ids']],'takeaway'))
   nt=next((z for z in plan['tiles'] if z['tile_id']==t['next_tile_id']),None)
   # Names retain the frozen glossary concept order, including the next batch.
   ncid=nt['concept_ids'][0] if nt else list(gloss['names'])[list(gloss['names']).index(t['concept_ids'][-1])+1]
   s['blocks'].append({'type':'up_next','title':'Up next: '+gloss['names'][ncid].split(';')[0].split(' after ')[0],'text':'Next tile: '+t['next_tile_id']+'.'})
  tile['steps'].append(s)
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Tiles:',len(out['tiles']));print('Planned steps:',sum(len(t['steps']) for t in out['tiles']));print('Remediation:',sum(len(t['remediation_steps']) for t in out['tiles']));print(Counter(s['type'] for t in out['tiles'] for s in t['steps']))
for t,ot in zip(plan['tiles'],out['tiles']):
 for ps,s in zip(t['steps'],ot['steps']):
  n=sum(len(b.get('text','').split()) for b in s.get('blocks',[]) if b['type']=='prose')
  if ps['word_budget'] and n>ps['word_budget']: print('OVER',ps['step_id'],n,ps['word_budget'])
