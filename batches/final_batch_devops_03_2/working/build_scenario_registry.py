import json
from pathlib import Path

B = Path('batches/final_batch_aws_devops.region.03_2')
glossary = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
profile = json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/' + glossary['path_id'] + '.json').read_text())
assert len(glossary['bundles']) == 2
assert all(b['context']['concept_id'] in profile['practice_type_by_concept'] for b in glossary['bundles'])
source_text = '\n'.join(t['content'] for b in glossary['bundles'] for t in b['teaching_blocks']) + '\n' + '\n'.join(json.dumps(b[k]) for b in glossary['bundles'] for k in ('visual_anchor', 'practice_anchor'))
terms = ['Config managed rule', 'resource scope', 'parameters', 'resource ID', 'compliance result', 'compliant', 'noncompliant', 'sample resources', 'rule criteria', 'evaluation', 'remediation', 'AWS budget', 'cost budget', 'scope', 'amount', 'period', 'actual', 'forecast', 'threshold', 'notification', 'recipient', 'resource-stopping actions', 'sandbox']
vocab = [t for t in terms if t in source_text]
scenario_id = 'scenario.sandbox_controls'

def col(name, role='text', typ='string', **extra):
    return dict(name=name, type=typ, semantic_role=role, **extra)

def dataset(asset_id, title, description, columns, rows):
    return dict(asset_id=asset_id, asset_kind='dataset', scenario_id=scenario_id, title=title, description=description, columns=columns, rows=rows, variants=[], provenance='authored')

assets = [
    dataset('ds.config_evaluations', 'Supplied configuration evaluation evidence',
        'Read-only fictional review evidence. The selected rule and its approved scope and parameters are symbolic references to supplied inputs, not an invented AWS managed-rule implementation. Both samples are in the approved scope. No evaluation is executed and no remediation is provisioned.',
        [col('resource_id', 'identifier'), col('selected_rule', 'identifier'), col('resource_scope', 'categorical'), col('parameters', 'text'), col('sample_configuration', 'categorical'), col('compliance_result', 'categorical')],
        [
            ['sample-acceptable', 'supplied Config managed rule', 'approved sandbox resource scope', 'supplied approved parameters', 'supplied compliant sample', 'COMPLIANT'],
            ['sample-prohibited', 'supplied Config managed rule', 'approved sandbox resource scope', 'supplied approved parameters', 'supplied noncompliant sample', 'NON_COMPLIANT'],
        ]),
    dataset('ds.budget_notification', 'Approved and saved budget notification settings',
        'Read-only fictional settings comparison: approved inputs and the saved configuration of the same single budget and its single notification. Amount and threshold are authored exercise inputs, not workload cost estimates. Recipient is fictional. No resource-stopping actions are configured.',
        [col('settings_record', 'categorical'), col('budget_id', 'identifier'), col('scope', 'categorical'), col('amount', 'numerical', 'number', unit='USD'), col('period', 'categorical'), col('notification_id', 'identifier'), col('threshold_value', 'numerical', 'number', unit='percent of budget amount'), col('threshold_basis', 'categorical'), col('recipient', 'text'), col('resource_stopping_actions_configured', 'categorical', 'boolean')],
        [
            ['approved inputs', 'sandbox-cost-budget', 'sandbox workload', 1000, 'monthly', 'sandbox-cost-alert', 80, 'actual', 'budget-owner@example.invalid', False],
            ['saved configuration', 'sandbox-cost-budget', 'sandbox workload', 1000, 'monthly', 'sandbox-cost-alert', 80, 'actual', 'budget-owner@example.invalid', False],
        ]),
]
registry = dict(schema_version='1.0', kind='scenario_asset_registry', path_id=glossary['path_id'], batch_id=B.name,
    scenarios=[dict(scenario_id=scenario_id, name='Sandbox controls review', domain='AWS operations', summary='A fictional operations team reviews a supplied sandbox Config rule and its two sample evaluation results, then checks a single budget notification against approved settings. All evidence is read-only; no cloud service or executable workspace is provisioned.', glossary_example_vocab=vocab)], assets=assets)

# Stage 01 mistakes-to-avoid checklist: row widths, roles, numeric labels,
# no undeclared variants/issues, sufficient anchor fields, and vocabulary fidelity.
assert len({a['asset_id'] for a in assets}) == len(assets)
for a in assets:
    assert all(len(r) == len(a['columns']) for r in a['rows'])
    assert not a['variants']  # No messy-data teaching or planted issues in scope.
    for c in a['columns']:
        assert (c['type'] in ('number', 'integer')) == (c['semantic_role'] == 'numerical')
        j = a['columns'].index(c)
        if any(isinstance(r[j], str) and r[j].isdigit() for r in a['rows']):
            assert c.get('numeric_looking_label') is True
assert all(t in source_text for t in vocab)
assert {r[-1] for r in assets[0]['rows']} == {'COMPLIANT', 'NON_COMPLIANT'}
assert assets[1]['rows'][0][1:] == assets[1]['rows'][1][1:]
assert len({r[5] for r in assets[1]['rows']}) == 1
assert not any(r[-1] for r in assets[1]['rows'])
(B / 'scenario_asset_registry.json').write_text(json.dumps(registry, indent=2) + '\n')
print(f"Checklist PASS: {len(registry['scenarios'])} scenario, {len(assets)} assets, {sum(len(a['rows']) for a in assets)} rows; all {len(glossary['bundles'])} concepts covered.")
