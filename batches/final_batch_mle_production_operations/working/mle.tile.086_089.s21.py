import csv, json, datetime
import numpy as np
SCHEMAS = {'validation_counts': {'fixture': 'string', 'model_role': 'string', 'cohort_id': 'string', 'registry_artifact_id': 'string', 'FP': 'integer', 'TN': 'integer', 'FN': 'integer', 'TP': 'integer', 'slice_pass': 'boolean', 'compatibility_pass': 'boolean'}}
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

def rates(r):
    fpr = None
    fnr = None
    cost = None
    if r['FP']+r['TN'] > 0 and r['FN']+r['TP'] > 0:
        fpr = r['FP']/(r['FP']+r['TN'])
        fnr = r['FN']/(r['FN']+r['TP'])
        cost = policy['P_Y0']*fpr*policy['cost_FP'] + policy['P_Y1']*fnr*policy['cost_FN']
    return {'FPR':fpr,'FNR':fnr,'expected_cost':cost}


policy = {'P_Y0': 0.5, 'P_Y1': 0.5, 'cost_FP': 1, 'cost_FN': 2, 'acceptance': {'maximum_FPR': 0.1, 'maximum_FNR': 0.1, 'cost_not_above_incumbent': True, 'slice_pass_required': True, 'compatibility_pass_required': True}, 'empty_group': 'undefined; reject', 'cohort': 'cohort.validation', 'decision_record_fields': ['registry_artifact_id', 'cohort_id', 'FPR', 'FNR', 'expected_cost', 'quality_pass', 'slice_pass', 'compatibility_pass', 'verdict'], 'protected_test': 'not provided; never used for selection'}
def calculate_contract(validation_counts_input):
    supplied_rows = {'validation_counts':validation_counts_input}
    def load(name):
        return supplied_rows[name]
    policy = {'P_Y0': 0.5, 'P_Y1': 0.5, 'cost_FP': 1, 'cost_FN': 2, 'acceptance': {'maximum_FPR': 0.1, 'maximum_FNR': 0.1, 'cost_not_above_incumbent': True, 'slice_pass_required': True, 'compatibility_pass_required': True}, 'empty_group': 'undefined; reject', 'cohort': 'cohort.validation', 'decision_record_fields': ['registry_artifact_id', 'cohort_id', 'FPR', 'FNR', 'expected_cost', 'quality_pass', 'slice_pass', 'compatibility_pass', 'verdict'], 'protected_test': 'not provided; never used for selection'}
    data = load('validation_counts')
    results = []
    
    for r in data:
        if r['model_role']=='candidate':
            incumbent = None
            for other in data:
                if other['fixture']==r['fixture'] and other['model_role']=='incumbent':
                    incumbent = other
            rr = rates(r)
            ir = rates(incumbent)
            defined = rr['expected_cost'] != None and ir['expected_cost'] != None
            quality_pass = False
            cost_pass = False
            if defined:
                quality_pass = rr['FPR'] <= policy['acceptance']['maximum_FPR'] and rr['FNR'] <= policy['acceptance']['maximum_FNR']
                cost_pass = rr['expected_cost'] <= ir['expected_cost']
            cohort_pass = r['cohort_id']==incumbent['cohort_id'] and r['cohort_id']==policy['cohort']
            for promotion_identity in [r['registry_artifact_id'],r['registry_artifact_id']+'.different']:
                identity_match = promotion_identity == r['registry_artifact_id']
                accept = defined and quality_pass and cost_pass and r['slice_pass'] and r['compatibility_pass'] and cohort_pass and identity_match
                if not identity_match:
                    assert not accept
                results.append({'fixture':r['fixture'],'candidate':r['registry_artifact_id'],'cohort':r['cohort_id'],'rates':rr,'incumbent_rates':ir,'quality_pass':quality_pass,'cost_pass':cost_pass,'slice_pass':r['slice_pass'],'compatibility_pass':r['compatibility_pass'],'cohort_pass':cohort_pass,'promotion_identity':promotion_identity,'promotion_identity_matches':identity_match,'verdict':accept})
    
    report = results
    return report

# OUTER

validation_counts_rows = load('validation_counts')
validation_counts_input = validation_counts_rows
report = calculate_contract(validation_counts_input)
