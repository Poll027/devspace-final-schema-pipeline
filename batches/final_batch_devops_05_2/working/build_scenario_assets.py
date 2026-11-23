import json
from pathlib import Path

B = Path('batches/final_batch_aws_devops.region.05_2')
glossary = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/aws_devops_engineer.json').read_text())
bundles = glossary['bundles']
# Mine only the named stage inputs: teaching blocks and visual/practice anchors.
texts = []
for bundle in bundles:
    texts.extend(t['content'] for t in bundle['teaching_blocks'])
    texts.append(json.dumps(bundle['visual_anchor'], ensure_ascii=False))
    texts.append(json.dumps(bundle['practice_anchor'], ensure_ascii=False))
source = '\n'.join(texts)
terms = [
    'sandbox', 'approved fault', 'limited target scope', 'expected signals',
    'abort conditions', 'alarm state history', 'notification receipt', 'recovery',
    'Lambda', 'NAME', 'ALIAS', 'VERSION', 'NAME:ALIAS', 'published version',
    'aws lambda publish-version --function-name NAME',
    'aws lambda update-alias --function-name NAME --name ALIAS --function-version VERSION',
    'Deployment', 'CONTAINER', 'IMAGE', 'REVISION', 'Pod template', 'readiness',
    'kubectl set image deployment/NAME CONTAINER=IMAGE',
    'kubectl rollout status deployment/NAME',
    'kubectl rollout undo deployment/NAME --to-revision=REVISION',
    'EC2', 'blue/green deployment group', 'replacement fleet', 'load balancer',
    'lifecycle', 'health', 'traffic', 'known-good revision',
    'Python', 'try', 'finally', 'scoped cleanup calls', 'exercise-created identities',
    'preexisting resources', 'Terraform', 'out-of-band', 'refresh-only',
    'state', 'outputs', 'remote infrastructure', 'module', 'source',
    'input arguments', 'module.NAME.OUTPUT', 'planned instance settings',
    'load', 'utilization', 'performance', 'normal', 'peak', 'changing demand',
    'service constraints', 'smaller instance', 'finding ID', 'evidence link',
    'affected resource', 'severity', 'observed activity', 'urgency',
    'responsible owner', 'escalation path', 'EventBridge', 'event bus',
    'event pattern', 'SNS', 'Systems Manager', 'matching', 'nonmatching',
    'target parameters', 'permissions', 'ECS', 'cluster', 'task definition',
    'network settings', 'desiredCount', 'three', 'running', 'pending', 'service events'
]
vocab = []
for term in terms:
    assert term.lower() in source.lower(), f'Vocabulary not in glossary: {term}'
    if term not in vocab:
        vocab.append(term)

scenario_id = 'scenario.sandbox_operations'
def column(name, typ, role, description, unit=None):
    value = dict(name=name, type=typ, semantic_role=role, description=description)
    if unit is not None:
        value['unit'] = unit
    return value

def dataset(asset_id, title, description, columns, rows):
    return dict(asset_id=asset_id, asset_kind='dataset', scenario_id=scenario_id,
                title=title, description=description, columns=columns, rows=rows,
                provenance='authored', variants=[])

# Fictional exercise measurements, not claims about any real EC2 instance family.
# Repeat identical demand observations for each candidate so comparisons are like-for-like.
constraints = {'max_latency_ms': 200, 'max_capacity_utilization_pct': 100}
observations = [
    ('normal', 40, 20, 80, 40, 120),
    ('peak', 200, 90, 200, 100, 260),
    ('changing demand', 160, 75, 180, 100, 230),
]
rows = []
for demand, load, current_util, current_latency, smaller_util, smaller_latency in observations:
    for option, util, latency in [
        ('current size', current_util, current_latency),
        ('smaller candidate', smaller_util, smaller_latency),
    ]:
        rows.append(['sandbox workload', option, demand, load, util, latency,
                     constraints['max_latency_ms'], constraints['max_capacity_utilization_pct']])
assets = [dataset(
    'ds.ec2_sizing_evidence', 'EC2 sizing: baseline and candidate evidence',
    'Read-only authored comparison for a fictional sandbox workload. Current size and smaller candidate are anonymous exercise options, not EC2 instance-type recommendations. Load, measured capacity utilization and response latency are supplied for normal, peak and changing demand. Constraints apply to every period; the current peak reaches the latency boundary, so the low normal sample cannot justify the smaller candidate. No pricing or production-performance claims.',
    [column('workload', 'string', 'identifier', 'Fictional workload identifier.'),
     column('size_option', 'string', 'categorical', 'Anonymous current or proposed smaller EC2 size option.'),
     column('demand_period', 'string', 'categorical', 'Supplied normal, peak or changing-demand observation.'),
     column('load_requests_per_second', 'number', 'numerical', 'Observed request load for the comparable test period.', 'requests/second'),
     column('capacity_utilization_pct', 'number', 'numerical', 'Measured fraction of candidate capacity utilized, not a resource label.', 'percent'),
     column('response_latency_ms', 'number', 'numerical', 'Supplied measured response latency for this period and candidate.', 'ms'),
     column('max_response_latency_ms', 'number', 'numerical', 'Supplied maximum acceptable latency; equality satisfies the bound.', 'ms'),
     column('max_capacity_utilization_pct', 'number', 'numerical', 'Supplied maximum acceptable capacity utilization; equality satisfies the bound.', 'percent')], rows),
    dataset(
    'ds.security_finding_handoff', 'Security finding: evidence and accountable owner',
    'One read-only fictional finding and its supplied owner mapping and established escalation path. The observed activity remains a report of suspicious activity, not a conclusion that the resource is compromised. The finding ID is the evidence reference; no live resource or external evidence endpoint is provisioned.',
    [column('finding_id', 'string', 'identifier', 'Supplied fictional evidence reference.'),
     column('affected_resource', 'string', 'identifier', 'Fictional affected resource identity.'),
     column('severity', 'string', 'categorical', 'Severity as reported in the supplied finding.'),
     column('observed_activity', 'string', 'text', 'Preserved activity description without an unsupported compromise claim.'),
     column('urgency', 'string', 'categorical', 'Supplied urgency of the handoff.'),
     column('accountable_owner', 'string', 'categorical', 'Responsible operational team from the supplied exercise owner mapping.'),
     column('established_escalation_path', 'string', 'text', 'Supplied escalation route; not a newly invented security conclusion.')],
    [['finding-sandbox', 'sandbox-workload-resource', 'high',
      'Finding reports suspicious activity on the affected resource.', 'prompt review',
      'sandbox workload operations team',
      'Notify the accountable owner; escalate to the established security on-call if the owner is unavailable.']])
]
registry = dict(schema_version='1.0', kind='scenario_asset_registry',
                path_id=glossary['path_id'], batch_id=B.name,
                scenarios=[dict(scenario_id=scenario_id, name='Sandbox workload operations',
                    summary='A fictional workload operations team reviews bounded sandbox release, recovery, monitoring and infrastructure evidence. A read-only sizing comparison and a finding handoff use the same sandbox workload vocabulary. All examples are authored; no cloud resources or executable environments are provisioned.',
                    domain='AWS sandbox operations', glossary_example_vocab=vocab)],
                assets=assets)
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2) + '\n')

# Stage-specific mistakes-to-avoid checklist, asserted against the produced artifact.
for asset in assets:
    names = [c['name'] for c in asset['columns']]
    assert len(names) == len(set(names))
    for row in asset['rows']:
        assert len(row) == len(names), 'row width mismatch'
        for c, v in zip(asset['columns'], row):
            assert (c['type'] == 'string' and isinstance(v, str)) or (c['type'] == 'number' and isinstance(v, (int, float)))
            assert (c['semantic_role'] == 'numerical') == (c['type'] == 'number')
            if isinstance(v, str) and v.isdigit():
                assert c.get('numeric_looking_label') is True
    assert not asset['variants'], 'No messy-data concepts: no planted issues or duplicate occurrences needed'
assert {r[2] for r in assets[0]['rows']} == {'normal', 'peak', 'changing demand'}
assert {r[1] for r in assets[0]['rows']} == {'current size', 'smaller candidate'}
assert all(r[5] <= r[6] and r[4] <= r[7] for r in rows if r[1] == 'current size')
assert any(r[5] > r[6] for r in rows if r[1] == 'smaller candidate' and r[2] == 'peak')
mandatory_tables = [b['context']['concept_id'] for b in bundles if b['visual_anchor']['type'] in ('data_table', 'spreadsheet')]
assert len(mandatory_tables) == len(assets)
assert all(b['context']['concept_id'] in profile['practice_type_by_concept'] for b in bundles if b['practice_anchor']['type'] in ('live_code', 'tool_simulation'))
assert all(a['asset_kind'] == 'dataset' for a in assets)
report = dict(concepts_covered=len(bundles), scenarios=len(registry['scenarios']),
              assets=len(assets), rows=sum(len(a['rows']) for a in assets),
              mandatory_table_concepts=mandatory_tables,
              checklist={
                  'row_width_and_column_types': 'PASS',
                  'semantic_roles_unambiguous': 'PASS',
                  'numeric_labels': 'PASS: no digit-only labels',
                  'planted_issue_predicates_and_duplicate_occurrences': 'N/A: no variants',
                  'baseline_normal_peak_changing_and_candidate_coverage': 'PASS',
                  'glossary_example_vocabulary': 'PASS: every vocabulary term verified against teaching blocks or anchors',
                  'glossary_named_tables_columns_places': 'PASS: no fixed table/column/place names in the two data-table anchors',
                  'inspect_and_judge_no_runtime_or_cloud_provisioning': 'PASS',
                  'images': 'N/A: no plot-dependent concepts'
              })
(B / 'working/scenario_assets_checklist.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
