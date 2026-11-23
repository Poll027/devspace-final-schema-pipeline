import csv, json, datetime
import numpy as np
SCHEMAS = {'release_evidence': {'release_id': 'string', 'cohort_id': 'string', 'timestamp': 'datetime', 'active_artifact': 'string', 'approved_artifact': 'string', 'active_config': 'string', 'approved_config': 'string', 'schema_pass': 'boolean', 'distribution_distance': 'number', 'matched_eligible_labels': 'integer', 'labeled_errors': 'integer', 'client_impact': 'string', 'hypothesis_test': 'string', 'supported_response': 'string'}}
def load(name):
    with open(name+'.csv') as f:
        data=list(csv.DictReader(f))
    for r in data:
        for k,t in SCHEMAS[name].items():
            v=r[k]
            r[k] = None if v=='' else (v=='True' if t=='boolean' else int(v) if t=='integer' else float(v) if t=='number' else v)
    return data
def column(data,key):
    return np.asarray([r[key] for r in data])
def emit(value):
    return value


policy = {'permitted_responses': ['data_repair', 'approved_rollback', 'gated_retraining'], 'selected_fixture_authorization': 'approved rollback cfg.bad -> cfg.r1 under lab.operator; readiness and bounded prediction gates required', 'quality_denominator': 'matched_eligible_labels; zero means undefined', 'hypothesis': 'configuration mismatch, distinguished by approved-configuration replay'}
def calculate_contract(release_evidence_input):
    supplied_rows = {'release_evidence':release_evidence_input}
    def load(name):
        return supplied_rows[name]
    policy = {'permitted_responses': ['data_repair', 'approved_rollback', 'gated_retraining'], 'selected_fixture_authorization': 'approved rollback cfg.bad -> cfg.r1 under lab.operator; readiness and bounded prediction gates required', 'quality_denominator': 'matched_eligible_labels; zero means undefined', 'hypothesis': 'configuration mismatch, distinguished by approved-configuration replay'}
    data = load('release_evidence')
    results = []
    
    for r in data:
        denominator = r['matched_eligible_labels']
        rate = None
        if denominator > 0:
            rate = r['labeled_errors'] / denominator
        response = r['supported_response']
        gates = []
        if response == 'approved_rollback':
            gates = ['readiness','bounded prediction']
        results.append({'release':r['release_id'],'cohort':r['cohort_id'],'time':r['timestamp'],'impact':r['client_impact'],'artifact_match':r['active_artifact']==r['approved_artifact'],'config_match':r['active_config']==r['approved_config'],'schema_pass':r['schema_pass'],'hypothesis_test':r['hypothesis_test'],'distribution_distance':r['distribution_distance'],'denominator':denominator,'errors':r['labeled_errors'],'error_proportion':rate,'response':response,'gates':gates,'scope':'distribution difference alone does not establish quality loss'})
    
    report = results
    return report

# OUTER

release_evidence_rows = load('release_evidence')
release_evidence_input = release_evidence_rows
report = calculate_contract(release_evidence_input)
