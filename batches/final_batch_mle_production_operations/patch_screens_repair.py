import json
from pathlib import Path
p=Path('batches/final_batch_mle.region.production_operations/screens.json')
d=json.loads(p.read_text())
t=next(t for t in d['tiles'] if t['tile_id']=='mle.tile.091_094')
s={s['step_id'].rsplit('.',1)[1]:s for s in t['steps']+t['remediation_steps']}
# Only the named cleanup visual and prose/remediation are touched.
v=s['s15']['blocks'][-1]
v['before']['caption']='Approved cleanup inventory: ownership, release labels, runtime state, logs and artifact references.'
v['after']['caption']='Inventory expectations, not observed cleanup outcomes. Verify retired absence, active health, required artifact and disk retention, and credential non-disclosure against post-action evidence.'
s['s16']['blocks'][0]['text']='Preserve active images and required model/preprocessing artifacts; removing a retired container does not authorize deleting shared artifacts. Verify active readiness and bounded prediction, and confirm approved retired resources are absent. Record ownership, active/retired identities, authorization, inspection evidence, actions, retained artifacts and credential non-disclosure checks in one audit.'
s['s16']['blocks'][1]['text']='Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the specific instance’s identity and status before and after the authorized lifecycle action; confirm retired absence rather than relying on expected inventory labels.'
s['s16']['blocks'][1]['lineage']['fact_ids']=['mle.serving_resource_cleanup#f10','mle.serving_resource_cleanup#f8']
s['s16']['blocks'][1]['lineage']['teaching_block_ids']=['mle.serving_resource_cleanup#tb5','mle.serving_resource_cleanup#tb4']
s['r07']['blocks'][0]['text']='Write one audit record containing verified ownership, active/retired identities, authorization, inspection evidence, actions, retained artifacts and credential non-disclosure checks.'
s['r07']['blocks'][1]['text']='An audit is not just a deletion list. Include the before-and-after inspection evidence and verified active health and retired absence, alongside retained artifacts and credential non-disclosure checks.'
s['r07']['blocks'][1]['lineage']['fact_ids']=['mle.serving_resource_cleanup#f9','mle.serving_resource_cleanup#f8','mle.serving_resource_cleanup#f10']
s['r07']['blocks'][1]['lineage']['teaching_block_ids']=['mle.serving_resource_cleanup#tb4','mle.serving_resource_cleanup#tb5']
s['r08']['blocks'][1]['text']=s['s16']['blocks'][1]['text']
s['r08']['blocks'][1]['lineage']=json.loads(json.dumps(s['s16']['blocks'][1]['lineage']))
p.write_text(json.dumps(d,indent=2)+'\n')
print('Changed s15 visual captions, s16 prose, r07 audit contrast, r08 inspection contrast.')
print('tiles',len(d['tiles']),'steps',sum(len(t['steps']) for t in d['tiles']),'remediation_steps',sum(len(t.get('remediation_steps',[])) for t in d['tiles']))
print('s16 prose words',sum(len(b['text'].split()) for b in s['s16']['blocks']))
