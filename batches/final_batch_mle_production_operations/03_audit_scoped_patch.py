import copy, csv, io, json
from pathlib import Path
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'screens.json'
d = json.loads(p.read_text())
before = copy.deepcopy(d)
r = json.loads((B / 'scenario_asset_registry.json').read_text())
a = {x['asset_id']: x for x in r['assets']}
def files(asset):
    return {x['path']: x['content'] for x in a[asset]['files']}
def step(n):
    return next(s for t in d['tiles'] for s in t['steps'] if s['step_id'] == 'mle.tile.091_094.' + n)
def diagram(title, nodes, lineage, alt):
    return {'type':'diagram','diagram_kind':'mapping','title':title,'nodes':nodes,'layout':'auto','alt_text':alt,'lineage':copy.deepcopy(lineage)}
s = step('s16')
s['blocks'][0]['text'] = 'Preserve active images and required model/preprocessing artifacts. Verify active readiness and bounded prediction, and confirm approved retired resources are absent. Record ownership, active/retired identities, authorization, inspection evidence, actions, retained artifacts and credential non-disclosure checks in one audit.'
s['blocks'][1]['text'] = 'Use gcloud compute instances describe INSTANCE --zone=ZONE before and after the authorized action to inspect identity and status. Confirm successful deletion completion and specific-instance not-found evidence; authentication or permission failures do not establish retired absence.'

v = next(b for b in step('s15')['blocks'] if b['type']=='before_after')
f = files('ws.serving_resource_cleanup')
evidence = list(csv.DictReader(io.StringIO(f['cleanup_evidence.csv'])))
nodes = []
for row in evidence:
    phase = row['phase']
    nodes.append({'id':phase+'.active','label':phase + ': active release', 'fields':[key+' = '+row[key] for key in ['active_NAME','active_INSTANCE','ZONE','active_owner_label','active_release_label','authorized_identity','active_instance_state','active_process_state','active_readiness','bounded_prediction_contract_pass']]})
    nodes.append({'id':phase+'.retired','label':phase + ': approved retired resources', 'fields':[key+' = '+row[key] for key in ['approved_retired_NAME','approved_retired_INSTANCE','retired_container_present','retired_instance_present','retired_instance_state']]})
row = next(x for x in evidence if x['phase']=='after')
nodes.append({'id':'after.retention','label':'After: retention and output review','fields':[key+' = '+row[key] for key in ['required_retained_artifacts','required_artifacts_present','disk_policy','all_attached_disks_retained','credential_review_pass']]})
v['after'] = diagram('Registered fixture evidence: ws.serving_resource_cleanup / cleanup_evidence.csv', nodes, v['lineage'], 'The registered before/after fixture records show approved retired absence, preserved active identity and health, required artifacts and disks retained, and credential review. These are supplied fixture records, not learner execution evidence.')
v['change_summary'] = 'Compare approved inventory with the registered before/after fixture evidence, not expected_after labels. Verify retired absence, active health, required artifacts, disk retention and credential-safe output.'

v = next(b for b in step('s10')['blocks'] if b['type']=='before_after')
f = files('ws.ml_workload_cost_guardrail')
policy = json.loads(f['policy.json'])
config = {k:policy[k] for k in ['workload_scope','budget_amount','period','threshold_ratio','notification_topic','response_pipeline','INSTANCE','ZONE','authorized_identity','secret_version_reference']}
v['before'] = {'type':'code_walkthrough','language':'python','code':'import yaml\n\n# Supplied contract: ws.ml_workload_cost_guardrail / policy.json\nconfig = '+repr(config)+'\nwith open("response.yaml", "w") as file_handle:\n    yaml.safe_dump(config, file_handle)\nwith open("response.yaml") as file_handle:\n    resolved = yaml.safe_load(file_handle)\nprint(resolved)\n','annotations':[{'start_line':4,'end_line':4,'text':'Inspect scope, budget, period, threshold, existing event path, fixed target, approved identity and secret reference; the reference is not a literal credential.'},{'start_line':5,'end_line':9,'text':'Safely reload and inspect before applying through the existing platform. This excerpt is configuration inspection, not notification or response execution evidence.'}],'lineage':copy.deepcopy(v['lineage'])}
v['after'] = diagram('Evidence to inspect after below-threshold and breach replays', [
    {'id':'receipt','label':'Notification receipt','fields':['Inspect emitted notification records separately from resource actions.']},
    {'id':'response','label':'Authorized response execution','fields':['Verify the safe stop acted only on '+policy['INSTANCE']+' in '+policy['ZONE']+'.','Compare before/after instance identity and status.']},
    {'id':'review','label':'Credential-safe guardrail record','fields':['Verify captured logs contain no literal credentials.',policy['residual_limitation']]}
], v['lineage'], 'Required notification, response and post-action inspection evidence, not observed outcomes. The registry supplies budget replay expectations but no captured guardrail execution records.')
v['change_summary'] = 'Inspect safely reloaded configuration before applying; then inspect notification receipt and authorized response execution separately. Expected replay states alone are not execution evidence.'

changed = []
for old_t, new_t in zip(before['tiles'], d['tiles']):
    for old, new in zip(old_t['steps'], new_t['steps']):
        if old != new:
            assert new['step_id'] in {'mle.tile.091_094.s10','mle.tile.091_094.s15','mle.tile.091_094.s16'}
            assert old['lineage'] == new['lineage']
            changed.append(new['step_id'])
    assert old_t.get('remediation_steps') == new_t.get('remediation_steps')
p.write_text(json.dumps(d,indent=2)+'\n')
print('Changed:', changed)
print('Tiles:',len(d['tiles']),'Steps:',sum(len(t['steps']) for t in d['tiles']),'Remediation:',sum(len(t.get('remediation_steps',[])) for t in d['tiles']))
