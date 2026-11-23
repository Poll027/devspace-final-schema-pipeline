import json,copy
from pathlib import Path
p=Path('batches/final_batch_aws_devops.region.03_1/screens.json')
d=json.loads(p.read_text());before=copy.deepcopy(d)
steps={s['step_id']:s for t in d['tiles'] for s in t['steps']}
def step(x):return steps['aws_devops.tile.'+x]
def visual(x):return next(b for b in step(x)['blocks'] if b['type'] in ('diagram','side_by_side'))
def refresh(b):
 b['positions']={n['id']:{'x':(i%2)*520,'y':(i//2)*180} for i,n in enumerate(b['nodes'])}
 b['alt_text']=b['title']+': '+'; '.join(n['label'] for n in b['nodes'])+'. '+'; '.join(next(n['label'] for n in b['nodes'] if n['id']==e['from'])+' → '+e['label']+' → '+next(n['label'] for n in b['nodes'] if n['id']==e['to']) for e in b['edges'])
def diagram(b,title,labels,edges):
 b['title']=title;b['nodes']=[{'id':f'n{i+1}','label':label,'kind':'callout'} for i,label in enumerate(labels)]
 b['edges']=[{'from':f'n{a}','to':f'n{z}','label':label,'directed':True} for a,z,label in edges];refresh(b)
diagram(visual('032.s01'),'Illustrative evidence checklist—not an execution transcript.',[
 'Virtual environment: ENV_DIR active',
 'Dependency installation: requirements.txt through ENV_DIR’s interpreter',
 'Package inspection: through the same interpreter',
 'AWS context: approved profile and Region confirmed separately',
 'Supplied script: uses ENV_DIR’s interpreter after both checks'],[(1,2,'environment-scoped installation'),(2,3,'inspect installed packages'),(3,5,'dependency evidence checked'),(4,5,'separate AWS-context check')])
diagram(visual('035.s01'),'Illustrative case from the lesson—not an execution transcript.',[
 'Supplied Pod: phase Running','Described runtime events: container problem','Intended container’s logs: container problem',
 'Running is a Pod phase; the events and intended-container output still show a problem.'],[(1,2,'same Pod'),(2,3,'same intended container'),(1,4,'phase alone is insufficient'),(3,4,'container evidence')])
diagram(visual('036.s01'),'Illustrative missing-marker case—not an execution transcript.',[
 'Intended RDS instance: identifier, engine, endpoint and status inspected',
 'Expected query outcome: required data marker present','Observed query outcome: required data marker missing',
 'Acceptable instance status does not establish application-data success.'],[(1,3,'supplied query on intended instance'),(2,3,'Compare the same marker'),(3,4,'missing marker')])
diagram(visual('036.s05'),'Illustrative schematic histories: releases/orders.zip',[
 'Overwrite: selected prior version','Copy to releases/orders.zip','New current version',
 'Simple deletion: delete marker above preceding version','Remove marker','Preceding version exposed',
 'Versioning enabled; inspect noncurrent-version expiration and other lifecycle rules against the required recovery window',
 'Deleting a specified version is permanent.'],[(1,2,'copy selected prior version'),(2,3,'creates'),(4,5,'undo simple deletion'),(5,6,'exposes'),(7,1,'overwrite recovery window'),(7,4,'simple-deletion recovery window'),(7,8,'specified-version deletion is distinct')])
b=visual('038.s01')
b['left_label']='Illustrative successful publication-and-consumption case: publisher'
b['right_label']='Illustrative successful publication-and-consumption case: consumer'
diagram(b['left'],'Tagged push: illustrative successful publication',[
 'REGISTRY/REPOSITORY:TAG','docker push','Approved publisher: push access verified; published digest DIGEST'],[(1,2,'tagged push reference'),(2,3,'under approved publisher identity')])
diagram(b['right'],'Digest-qualified pull: illustrative successful consumption',[
 'REGISTRY/REPOSITORY@sha256:DIGEST','docker pull','Approved consumer: pull access verified; retrieved digest DIGEST',
 'Published digest DIGEST (approved publisher, left panel)'],[(1,2,'digest-qualified pull reference'),(2,3,'under approved consumer identity'),(4,3,'Same content digest')])
b['takeaway']='Same content digest: the approved publisher’s published digest DIGEST matches the approved consumer’s retrieved digest DIGEST.'
diagram(visual('038.s05'),'Illustrative successful verification case—not an execution transcript.',[
 'Supplied orders output: revision rev-42',
 'Immutable upload record: workflow run, revision-based artifact name, upload SHA256',
 'Download integrity result: upload SHA256 matches',
 'Verified extracted-file attestation: artifact digest, source repository, revision rev-42, build workflow/run'],[(1,2,'upload same supplied file'),(2,3,'Upload/download digest check'),(3,4,'Extracted-file provenance verification'),(4,2,'verified revision/workflow linked to upload record'),(1,4,'same revision rev-42')])
diagram(visual('043.s01'),'Illustrative configuration mismatch: A and B are symbolic values.',[
 'Affected resource: recorded configuration value B','Rule parameter: required value A',
 'Evaluation result: noncompliant because recorded B differs from required A',
 'Governing policy: select the established remediation or escalation path—not proof of an attack'],[(1,3,'recorded value'),(2,3,'required value'),(3,4,'governing response')])
b=visual('044.s01')['right']
for n in b['nodes']:
 if n['label']=='Wait for completed drift detection':n['label']='Detection status: complete'
 if n['label']=='Inspect expected / actual difference':n['label']='Resource drift result: checked declared value A differs from current value B'
for e in b['edges']:
 if e['from']=='n3':e['label']='completed result'
refresh(b)
diagram(visual('044.s05'),'Two illustrative ordered traces—not execution transcripts.',[
 '1. Resource update failed—original update failure reason',
 '2. Subsequent rollback events',
 '3. Final stack status: UPDATE_ROLLBACK_COMPLETE—previous working state restored',
 '1. Resource update failed—original update failure reason',
 '2. Rollback operation failed—separate rollback failure reason',
 '3. Final stack status: UPDATE_ROLLBACK_FAILED—resolve rollback failure before continuing'],[(1,2,'then'),(2,3,'then'),(4,5,'then: separate rollback failure'),(5,6,'then')])
diagram(visual('046.s01'),'Illustrative permission-test evidence—not an execution transcript.',[
 'Approved instance profile: contains one IAM role','Caller-identity result: assigned role',
 'Supplied allowed operation: allowed','Supplied denied operation: denied'],[(1,2,'instance role credential provider, not embedded keys'),(2,3,'same assigned-role identity'),(2,4,'same assigned-role identity')])
b=visual('046.s06')
# Preserve association and credential-delivery qualification; split only the combined test evidence.
b['nodes']=[n for n in b['nodes'] if n['id']!='n9']
for n in b['nodes']:
 if n['id']=='n6':n['label']='Intended workload: serviceAccountName matches the cluster/namespace/service-account association'
 if n['id']=='n7':n['label']='Pod Identity agent + supported SDK credential chain'
b['nodes'] += [
 {'id':'n9','label':'Supplied allowed-access result: success','kind':'callout'},
 {'id':'n10','label':'Unassociated workload','kind':'callout'},
 {'id':'n11','label':'Supplied access result: rejected','kind':'callout'}]
b['edges']=[e for e in b['edges'] if e['to']!='n9']+[
 {'from':'n6','to':'n9','label':'intended workload','directed':True},
 {'from':'n10','to':'n11','label':'unassociated workload','directed':True},
 {'from':'n8','to':'n6','label':'temporary role credentials to associated Pod','directed':True}]
refresh(b)
step('046.s13')['title']='Review workflow federation trust'
# Reword the existing example using its already-cited declaration/output/live-property contrast.
b=step('040.s02')['blocks'][0]
b['text']='The supplied bucket logical ID declares the approved property value; its Ref output names that bucket. Compare the corresponding live property with the declaration after deployment. Check Type and Properties under Resources, make only approved property/reference edits, and retain validation, sandbox-creation, event and output evidence with the live-property comparison.'
changed=[]
for old_t,new_t in zip(before['tiles'],d['tiles']):
 for old_s,new_s in zip(old_t['steps'],new_t['steps']):
  if old_s!=new_s:changed.append(new_s['step_id'])
expected=['aws_devops.tile.'+x for x in ['032.s01','035.s01','036.s01','036.s05','038.s01','038.s05','040.s02','043.s01','044.s01','044.s05','046.s01','046.s06','046.s13']]
assert set(changed)==set(expected)
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Changed',len(changed),'steps:',', '.join(changed))
