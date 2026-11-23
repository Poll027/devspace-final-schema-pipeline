import json, re, hashlib
from pathlib import Path
from datetime import datetime

batch = Path(__file__).resolve().parents[1]
glossary = json.loads((batch/'inputs/path_glossary_bundle.json').read_text())
bs = glossary['bundles']
scenario_id = 'scenario.operational_release_and_recovery'
# Mine vocabulary only from teaching blocks and anchors, not external sources.
texts=[]
for b in bs:
    texts.extend(t['content'] for t in b['teaching_blocks'])
    texts.extend(json.dumps(b[k], ensure_ascii=False) for k in ('visual_anchor','practice_anchor','assessment_anchors'))
texts.extend(s for b in bs for s in b['practice_anchor'].get('live_code',{}).get('allowed_syntax',[]))
text='\n'.join(texts)
candidates=['EventBridge','RetryPolicy','MaximumRetryAttempts','MaximumEventAgeInSeconds','DeadLetterConfig','SQS','ARN','ECS','desiredCount','minimumHealthyPercent','maximumPercent','task-definition revision','image version A','version B','staging','production','immutable artifact','digest','build provenance','environment configuration','Cost Explorer','24 hours','account','service','usage type','usage timestamps','resource-deletion evidence','initial','refreshed report','Terraform','S3','ListBucket','GetObject','PutObject','DeleteObject','use_lockfile','true','.tflock','state bucket','prefix','object key','exercise bucket','approved identity','unapproved identity','manual approval','review link','revision context','authorized approver','runbook','preconditions','expected outcome','stop condition','escalation owner','RTO','RPO','10:00','10:18','09:56','09:50','20 minutes','5 minutes','18 minutes','4 minutes','readiness checks','recovered data marker','configuration error','preventive action','accountable owner','completion check','DNS','TTL','cached answers','restored target']
vocab=[v for v in candidates if v in text]
for b in bs:
    for syntax in b['practice_anchor'].get('live_code',{}).get('allowed_syntax',[]):
        if syntax not in vocab: vocab.append(syntax)

assets=[]
def col(name,typ='string',role='text',description=None,unit=None):
    c={'name':name,'type':typ,'semantic_role':role}
    if description: c['description']=description
    if unit: c['unit']=unit
    return c
def dataset(aid,title,description,columns,rows):
    assets.append({'asset_id':aid,'asset_kind':'dataset','scenario_id':scenario_id,'title':title,'description':description,'columns':columns,'rows':rows,'provenance':'authored'})

# Opaque authored digests are calculated, not manually typed or real build evidence.
build_id='build.release_b'
digest='sha256:'+hashlib.sha256(('fictional exercise artifact:'+build_id).encode()).hexdigest()
dataset('ds.artifact_promotion','One build, two environment releases',
    'Read-only authored comparison. Digest is calculated from a fictional artifact label, not a real deployed artifact. Staging and production retain the same build output; configuration differs by environment.',
    [col('environment',role='categorical'),col('immutable_artifact_reference',role='identifier'),col('deployed_digest',role='identifier'),col('recorded_build_provenance',role='identifier'),col('environment_configuration',role='identifier'),col('new_build_during_promotion','boolean','categorical')],
    [[env,'artifact.release_b',digest,build_id,'config.'+env,False] for env in ('staging','production')])

# Times and amounts below are explicitly authored observations, not AWS prices or reporting guarantees.
window_start='2026-01-12T09:00:00Z'; window_end='2026-01-12T12:00:00Z'; deletion='2026-01-12T10:00:00Z'
dataset('ds.residual_charge_reports','Initial and refreshed teardown reports',
    'Fictional read-only Cost Explorer extracts for a single account and service filter. Null usage/cost cells mean the initial extract returned no matching row, not measured zero usage. The later charge concerns usage before deletion. The illustrated later report is not a final-billing deadline; data refreshes at least every 24 hours and some data can take longer to appear. Cost is an authored report amount, not a rate estimate.',
    [col('report_state',role='categorical'),col('reported_at','datetime','datetime'),col('teardown_interval_start','datetime','datetime'),col('teardown_interval_end','datetime','datetime'),col('account',role='identifier'),col('service',role='categorical'),col('resource',role='identifier'),col('usage_timestamp','datetime','datetime'),col('cost','number','numerical',unit='USD'),col('deleted_at','datetime','datetime'),col('deletion_evidence'),col('report_result')],
    [['initial','2026-01-12T12:00:00Z',window_start,window_end,'account.exercise','Amazon ECS','service.exercise',None,None,deletion,'Deletion recorded for service.exercise','No matching usage row in current extract; provisional'],
     ['refreshed','2026-01-14T12:00:00Z',window_start,window_end,'account.exercise','Amazon ECS','service.exercise','2026-01-12T09:30:00Z',0.25,deletion,'Deletion recorded for service.exercise','Usage before deletion appeared in refreshed extract; not proof of continuing usage']])

# Extract glossary time/objective values and compute measured outcomes.
b=next(b for b in bs if b['context']['concept_id'].endswith('verify_restored_service_and_data_against_rto_rpo_in_an_isolated_rehearsal'))
example=next(t['content'] for t in b['teaching_blocks'] if t['purpose']=='example')
times=list(dict.fromkeys(re.findall(r'\b\d{2}:\d{2}\b',example)))
start,ready,marker,alternative=times[:4]
limits=re.search(r'(\d+) minutes RTO and (\d+) minutes RPO',example)
rto,rpo=map(int,limits.groups())
def minutes(a,b):
    return int((datetime.strptime(b,'%H:%M')-datetime.strptime(a,'%H:%M')).total_seconds()/60)
rows=[]
for name,m in [('illustrative',marker),('alternative_marker',alternative)]:
    elapsed=minutes(start,ready); gap=minutes(m,start)
    rows.append([name,'isolated rehearsal',start,ready,'Supplied service-readiness checks pass',m,elapsed,rto,'pass' if elapsed<=rto else 'fail',gap,rpo,'pass' if gap<=rpo else 'fail'])
dataset('ds.recovery_objectives','Independent RTO and RPO comparisons',
    'Read-only illustrative glossary measurements, not AWS defaults. Clock times are on the same rehearsal day. Interval and pass/fail columns are computed from those times and stated objectives; the alternative marker leaves restoration time unchanged.',
    [col('case_id',role='identifier'),col('environment',role='categorical'),col('disruption_start',role='datetime',description='Same-day HH:MM clock time'),col('passing_readiness_at',role='datetime',description='Same-day HH:MM clock time'),col('readiness_evidence'),col('latest_recovered_marker',role='datetime',description='Same-day HH:MM clock time'),col('restoration_minutes','integer','numerical',unit='minutes'),col('rto_minutes','integer','numerical',unit='minutes'),col('rto_result',role='categorical'),col('data_gap_minutes','integer','numerical',unit='minutes'),col('rpo_minutes','integer','numerical',unit='minutes'),col('rpo_result',role='categorical')],rows)

dataset('ds.incident_evidence_to_action','Factual timeline and bounded prevention',
    'Fictional read-only incident evidence illustrating the glossary configuration-error example. No AWS resource commands or sensitive state contents are supplied. Direct observations are separated from the narrow conclusion supported by the verified correction; no other causal attribution is made. The owner is a fictional team role.',
    [col('record_id',role='identifier'),col('timestamp','datetime','datetime'),col('record_kind',role='categorical'),col('impact_evidence'),col('direct_observation'),col('supported_causal_conclusion'),col('preventive_action'),col('accountable_owner',role='categorical'),col('completion_check')],
    [['incident.symptom','2026-01-12T10:00:00Z','observation','Supplied service-readiness check fails','Readiness failure recorded','','','',''],
     ['incident.investigation','2026-01-12T10:02:00Z','observation','','Supplied configuration comparison records a mismatch against the approved configuration','','','',''],
     ['incident.correction','2026-01-12T10:10:00Z','observation','','Approved correction restores the mismatched configuration to the supplied approved value','','','',''],
     ['incident.verification','2026-01-12T10:18:00Z','observation','Supplied service-readiness check passes','Readiness passes after the approved configuration correction','','','',''],
     ['incident.follow_up','2026-01-12T10:20:00Z','conclusion_and_action','','','The verified correction supports the identified configuration error; no additional cause is asserted','Detect that configuration mismatch before accepting the configuration','Operational owner','Replay the supplied mismatch and verify the configuration check detects it']])

registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':glossary['path_id'],'batch_id':batch.name,'scenarios':[{'scenario_id':scenario_id,'name':'An operational release and isolated recovery exercise','summary':'A fictional operations team reviews an EventBridge failure route, an ECS version A to B release, staging-to-production promotion, state authorization and locking, approval and runbook records, teardown reports, and an isolated recovery rehearsal. Everything is read-only evidence: no cloud resources, credentials, terminal runtime or executable workspace are provisioned. Numeric limits not supplied by the glossary are not asserted as defaults.','domain':'AWS operational release and recovery','glossary_example_vocab':vocab}],'assets':assets}

# Mistakes-to-avoid self-check: row widths, roles and types, labels, coverage,
# no undeclared messy variants, no duplicate occurrence or issue assertions.
for a in assets:
    assert len({c['name'] for c in a['columns']})==len(a['columns'])
    for r in a['rows']:
        assert len(r)==len(a['columns'])
        for c,v in zip(a['columns'],r):
            if v is None: continue
            t=c['type']; role=c['semantic_role']
            assert t!='integer' or (isinstance(v,int) and not isinstance(v,bool))
            assert t!='number' or (isinstance(v,(int,float)) and not isinstance(v,bool))
            assert t!='boolean' or isinstance(v,bool)
            assert t not in ('string','datetime','date') or isinstance(v,str)
            assert role!='numerical' or t in ('number','integer')
            if role in ('identifier','categorical') and isinstance(v,str) and v.isdigit():
                c['numeric_looking_label']=True
    assert not a.get('variants')
assert len(bs)==11
mandatory=[b for b in bs if b['visual_anchor']['type'] in ('data_table','spreadsheet')]
assert len(mandatory)==len(assets)
assert all(v in text for v in vocab)
assert all(a['asset_kind']=='dataset' for a in assets)
(batch/'scenario_asset_registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'concepts':len(bs),'scenarios':1,'assets':len(assets),'rows':sum(len(a['rows']) for a in assets),'asset_ids':[a['asset_id'] for a in assets]},indent=2))
