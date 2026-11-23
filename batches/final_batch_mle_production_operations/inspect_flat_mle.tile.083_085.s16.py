import csv, json

import numpy as np

policy = json.loads('{"permitted_responses": ["data_repair", "approved_rollback", "gated_retraining"], "selected_fixture_authorization": "approved rollback cfg.bad -> cfg.r1 under lab.operator; readiness and bounded prediction gates required", "quality_denominator": "matched_eligible_labels; zero means undefined", "hypothesis": "configuration mismatch, distinguished by approved-configuration replay"}')

release_evidence_rows = list(csv.DictReader(open('release_evidence.csv')))

release_evidence = {}

release_evidence['release_id'] = np.array([r['release_id'] for r in release_evidence_rows])

release_evidence['cohort_id'] = np.array([r['cohort_id'] for r in release_evidence_rows])

release_evidence['timestamp'] = np.array([r['timestamp'] for r in release_evidence_rows])

release_evidence['active_artifact'] = np.array([r['active_artifact'] for r in release_evidence_rows])

release_evidence['approved_artifact'] = np.array([r['approved_artifact'] for r in release_evidence_rows])

release_evidence['active_config'] = np.array([r['active_config'] for r in release_evidence_rows])

release_evidence['approved_config'] = np.array([r['approved_config'] for r in release_evidence_rows])

release_evidence['schema_pass'] = np.array([r['schema_pass'] == 'True' for r in release_evidence_rows])

release_evidence['distribution_distance'] = np.array([float(r['distribution_distance'] or 'nan') for r in release_evidence_rows])

release_evidence['matched_eligible_labels'] = np.array([float(r['matched_eligible_labels'] or 'nan') for r in release_evidence_rows])

release_evidence['labeled_errors'] = np.array([float(r['labeled_errors'] or 'nan') for r in release_evidence_rows])

release_evidence['client_impact'] = np.array([r['client_impact'] for r in release_evidence_rows])

release_evidence['hypothesis_test'] = np.array([r['hypothesis_test'] for r in release_evidence_rows])

release_evidence['supported_response'] = np.array([r['supported_response'] for r in release_evidence_rows])

evidence = [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in release_evidence.items()} for i in range(len(release_evidence_rows))]

matched_counts = release_evidence['matched_eligible_labels']

error_counts = release_evidence['labeled_errors']

rate_groups = list(range(len(matched_counts)))

zero = 0

has_labels = None

selected_rates = []

for group in rate_groups:
    rate = None
    if has_labels[group]:
        rate = error_counts[group] / matched_counts[group]
    selected_rates = selected_rates + [rate]

result = []

def diagnostic_record(row, rate, response, gates):
    n = row['matched_eligible_labels']
    errors = row['labeled_errors']
    return {'release': row['release_id'], 'cohort': row['cohort_id'], 'timestamp': row['timestamp'], 'impact': row['client_impact'], 'active_artifact': row['active_artifact'], 'approved_artifact': row['approved_artifact'], 'active_config': row['active_config'], 'approved_config': row['approved_config'], 'hypothesis': policy['hypothesis'], 'hypothesis_test': row['hypothesis_test'], 'matched_eligible_labels': n, 'errors': errors, 'error_rate': rate, 'response': response, 'required_gates': gates, 'quality_claim': 'matched mature cohort only; distribution alone does not establish quality loss'}

label_investigate = 'investigate'

label_approved_rollback = 'approved_rollback'

label_none = 'none'

for row in evidence:
    n = row['matched_eligible_labels']
    rate = selected_rates[len(result)]
    response = label_investigate
    gates = []
    mismatch_replay = row['active_config'] != row['approved_config'] and row['active_artifact'] == row['approved_artifact'] and n > 0 and row['schema_pass'] and row['hypothesis_test'] == 'bad configuration reproduces errors; approved rollback restores baseline' and row['supported_response'] == label_approved_rollback
    if mismatch_replay:
        response = label_approved_rollback
        gates = ['readiness', 'bounded_prediction']
    elif row['client_impact'] == 'baseline':
        response = label_none
    result = result + [diagnostic_record(row, rate, response, gates)]