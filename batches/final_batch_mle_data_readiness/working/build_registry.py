import ast, csv, io, json, pprint, re, sys
from pathlib import Path
from datetime import datetime, timedelta
ROOT=Path.cwd()
B=ROOT/'batches/final_batch_mle.region.data_readiness'
raw=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bundles={b['context']['concept_id'].split('.',1)[1]:b for b in raw['bundles']}
def text(k):
 b=bundles[k]
 return '\n'.join(t['content'] for t in b['teaching_blocks'])+'\n'+json.dumps(b['practice_anchor'],ensure_ascii=False)+'\n'+json.dumps(b['visual_anchor'],ensure_ascii=False)
def number(k,pattern,group=1): return int(re.search(pattern,text(k)).group(group).replace(',',''))
def literal(k,pattern):return ast.literal_eval(re.search(pattern,text(k)).group(1))
matrix=literal('numpy_shape_dtype',r'Consider the fixture (\[\[.*?\]\])')
flat=[v for row in matrix for v in row]
ref=literal('numpy_vectorization',r'subtract (\[.*?\])')
horizon=number('prediction_task_definition',r'more than (\d+) minutes')
total=number('prediction_task_definition',r'contains (\d+) orders')
events=number('prediction_task_definition',r'of which (\d+) meet')
zone_events=number('prediction_task_definition',r'zone, (\d+) of')
zone_total=number('prediction_task_definition',r'of (\d+) orders meet')
lo=number('dataset_schema_validation',r'between (\d+) and')
hi=number('dataset_schema_validation',r'between \d+ and (\d+)')
neg=-number('dataset_schema_validation',r'while −(\d+) is')
feature_width=number('chunked_ingestion',r'has (\d+) columns')
word_numbers={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}
width=word_numbers[re.search(r'columns of (\w+)-byte',text('chunked_ingestion')).group(1)]
dtype_words=re.search(r'element widths of (\w+) and (\w+) bytes',text('numpy_dtype_selection')).groups()
dtype_widths=[word_numbers[w] for w in dtype_words]
budget=number('chunked_ingestion',r'budget of ([\d,]+) bytes')
row_limit=budget//(feature_width*width)
scenario='scn.delivery_readiness'
# Vocabulary comes from teaching and anchors, including verbatim example blocks;
# short code tokens are extracted rather than normalized into invented names.
vocab=[]
for b in raw['bundles']:
 for t in b['teaching_blocks']:
  if t['purpose']=='example':
   vocab += re.findall(r'\b(?:delivery orders|order at acceptance|promised delivery zone|eventual arrival time|all orders|specified zone|zone-A|zone-B|order A|order B|customer G1|G2|[0-9]+(?:\.[0-9]+)?|float32|float64|int64)\b',t['content'])
   vocab += re.findall(r'\[\[.*?\]\]|‘[^’]+’',t['content'])
 s=json.dumps([b['teaching_blocks'],b['practice_anchor'],b['visual_anchor']],ensure_ascii=False)
 vocab += re.findall(r'\b(?:orders-[ab]\.csv|distance|zone|north|south|east|order_key|observation_id|run_id|row_count|token|available_at|prediction_time|numeric_values|X_train|X_validation|G1|G2|NumPy|pandas|Parquet|ColumnTransformer|Pipeline|SimpleImputer|StandardScaler|OneHotEncoder|statistics_|categories_|mean_|scale_)\b',s)
vocab=list(dict.fromkeys(vocab))
reg={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':raw['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':scenario,'name':'Fictional delivery-order readiness lab','summary':'An operations team prepares order-at-acceptance delivery predictions in an authorized, local fixture runtime. Each bounded fixture is independent: population counts, array examples, selection counts and training/validation examples are not claims about one shared production sample. All rows, identities, timestamps and policies are illustrative.','domain':'delivery operations','glossary_example_vocab':vocab}],'assets':[]}
def col(name,typ='string',role=None,description=None):
 d={'name':name,'type':typ,'semantic_role':role or {'string':'categorical','number':'numerical','integer':'numerical','datetime':'datetime','boolean':'categorical'}[typ]}
 if typ in ('integer','number') and d['semantic_role'] in ('identifier','categorical'):d['numeric_looking_label']=True
 if description:d['description']=description
 return d
def ds(id,title,columns,rows,description='Independent authored fixture; not observed production data.'):
 a={'asset_id':'ds.'+id,'asset_kind':'dataset','scenario_id':scenario,'title':title,'description':description,'columns':columns,'rows':rows,'variants':[],'provenance':'authored'}
 reg['assets'].append(a);return a
def variant(a,id,ops,issues=None,purpose='Declared boundary or failure fixture'):
 v={'variant_id':id,'derived_from':a['asset_id'],'purpose':purpose,'ops':ops,'planted_issues':issues or []};a['variants'].append(v);return v
def cell(where,column,value,occurrence=0):return {'op':'set_cell','where':where,'occurrence':occurrence,'column':column,'value':value}
def issue(id,kind,where,column,description,occurrence=0,rule=None):
 d={'issue_id':id,'kind':kind,'locations':[{'where':where,'occurrence':occurrence,'column':column}],'description':description}
 if rule:d['rule']=rule
 return d
def rule(column,op,value):return {'column':column,'op':op,'value':value}
# Count and task records keep distinct populations and denominators explicit.
counts=ds('outcome_counts','Outcome counts by declared population',[col('population'),col('target_count','integer'),col('population_count','integer'),col('horizon_minutes','integer')],[['all orders',events,total,horizon],['specified zone',zone_events,zone_total,horizon]])
task=ds('task_record','Order-at-acceptance prediction task',[col('field','string','identifier'),col('value','string','text')],[['prediction_unit','one order at acceptance'],['eligible_population','all '+str(total)+' supplied accepted orders'],['target_event','arrival more than '+str(horizon)+' minutes after acceptance'],['prediction_time','acceptance'],['horizon',str(horizon)+' minutes'],['allowed_inputs','distance; promised delivery zone'],['excluded_input','eventual arrival time']])
features=ds('order_features','Three observations with two numerical features',[col('distance','number',description='First numerical feature; illustrative distance, no physical unit declared.'),col('feature_2','number',description='Second unnamed numerical feature in the glossary matrix; not a zone code.')],matrix)
variant(features,'one_order',[{'op':'drop_rows','where':{'distance':r[0]}} for r in matrix[1:]])
variant(features,'wrong_width',[{'op':'drop_columns','columns':['feature_2']}])
variant(features,'four_orders',[{'op':'duplicate_row','where':{'distance':matrix[0][0]},'insert':'end'}])
variant(features,'empty',[{'op':'drop_rows','where':{'distance':r[0]}} for r in matrix])
dtype_rows=[r[:] for r in matrix]
dtype_rows[0][0]=float(re.search(r'reference value (\d+\.\d+)',text('numpy_dtype_selection')).group(1))
dtype_ds=ds('dtype_reference','Six-value dtype comparison reference',features['columns'],dtype_rows)
key=re.search(r'key such as ‘([^’]+)’',text('file_object_ingestion')).group(1)
orders=ds('orders','orders-b.csv',[col('order_key','string','identifier','Zero-padded text key, e.g. '+key+'; never a measured quantity. Preserve leading zeros through CSV loading.'),col('distance','number'),col('zone'),col('eventual_arrival','datetime')],[[key,matrix[0][0],'north','2025-01-01T09:45:00'],['0013',matrix[1][0],'south','2025-01-01T10:20:00'],['0014',matrix[2][0],'north','2025-01-01T11:31:00'],['0015',lo,'south','2025-01-01T12:30:00'],['0016',hi,'north','2025-01-01T13:50:00'],['0017',matrix[1][0],'south','2025-01-01T14:10:00']], 'Intended CSV object orders-b.csv. eventual_arrival is target-side information unavailable at acceptance. order_key is string, preserving '+key+'.')
variant(orders,'missing_distance',[cell({'order_key':key},'distance',None)],[issue('missing_distance','missing_value',{'order_key':key},'distance','Missing distance fixture.')])
variant(orders,'duplicate_order',[{'op':'duplicate_row','where':{'order_key':key},'insert':'end'}],[issue('duplicate_order','duplicate_row',{'order_key':key},'order_key','Repeated complete order row.',1)])
variant(orders,'mixed_distance',[cell({'order_key':key},'distance','not_numeric')],[issue('mixed_distance','wrong_type',{'order_key':key},'distance','Numeric distance replaced by an explicit text failure value.',rule=rule('distance','eq','not_numeric'))])
variant(orders,'zone_spelling',[cell({'order_key':'0013'},'zone','South')],[issue('zone_spelling','inconsistent_category',{'order_key':'0013'},'zone','Category casing disagrees with declared lower-case representation.',rule=rule('zone','casing_differs_from_siblings',None))])
schema=ds('distance_zone','Exact distance/zone schema',[col('distance','number'),col('zone')],[[lo,'north'],[matrix[0][0],'south'],[hi,'north']],'Exactly distance and zone; numeric distance in inclusive [0,100]; zone is lower-case north or south. Bounds are fixture policy, not a universal domain rule.')
variant(schema,'negative_distance',[cell({'distance':lo},'distance',neg)],[issue('negative_distance','impossible_value',{'distance':neg},'distance','Distance violates supplied lower bound.',rule=rule('distance','lt',lo))])
variant(schema,'over_upper_bound',[cell({'distance':hi},'distance',hi+1)],[issue('over_upper_bound','impossible_value',{'distance':hi+1},'distance','Distance violates supplied upper bound.',rule=rule('distance','gt',hi))])
variant(schema,'missing_zone_column',[{'op':'drop_columns','columns':['zone']}])
variant(schema,'invalid_zone',[cell({'distance':lo},'zone','NORTH')],[issue('invalid_zone','inconsistent_category',{'distance':lo},'zone','Declared representation requires lower-case north.',rule=rule('zone','ne','north'))])
clean=ds('cleaning_orders','Policy-driven accepted-order cleaning',[col('observation_id','string','identifier'),col('order_key','string','identifier'),col('distance','number'),col('zone')],[['obs_A','A',matrix[0][0],'north'],['obs_B','B',matrix[1][0],'south'],['obs_C','C',lo,'north'],['obs_D','D',hi,'south']])
variant(clean,'policy_defects',[{'op':'duplicate_row','where':{'order_key':'A'},'insert':'end'},cell({'order_key':'A'},'observation_id','obs_A_repeat',1),cell({'order_key':'B'},'zone','South'),cell({'order_key':'D'},'distance',neg)],[issue('repeated_key','other',{'observation_id':'obs_A_repeat'},'order_key','A was already accepted; reject this repeated key.',rule=rule('order_key','eq','A')),issue('spelling','inconsistent_category',{'order_key':'B'},'zone','Approved repair South to south.',rule=rule('zone','eq','South')),issue('invalid_distance','impossible_value',{'order_key':'D'},'distance','Reject negative distance under supplied policy.',rule=rule('distance','lt',lo))])
chunk=ds('chunked_orders','Twenty eight-byte feature columns',[col('feature_'+str(i+1),'number') for i in range(feature_width)],[[float((r+1)*(c+1)) for c in range(feature_width)] for r in range(row_limit*2+1)],'Independent homogeneous float64 CSV fixture: multiple full chunks and a final short chunk. Only per-matrix element storage is constrained.')
sel=text('dataset_selection_bias')
target_A=int(re.search(r'has (\d+) zone-A',sel).group(1));target_B=int(re.search(r'and (\d+) zone-B',sel).group(1));sample_A=int(re.search(r'includes (\d+) A',sel).group(1));sample_B=int(re.search(r'and (\d+) B',sel).group(1))
selection_counts=ds('selection_counts','Known target/sample membership counts',[col('zone'),col('sample_count','integer'),col('target_count','integer')],[['zone-A',sample_A,target_A],['zone-B',sample_B,target_B]])
# Timestamp fixtures are authored, explicitly declared and intentionally local.
t0=datetime(2025,1,1,9);boundary=t0+timedelta(minutes=horizon)
obs=ds('observations','Observation IDs and observation timestamps',[col('observation_id','string','identifier'),col('observation_timestamp','datetime')],[['A',t0.isoformat()],['B',(t0+timedelta(hours=1)).isoformat()]])
labels=ds('labels','Labels in reversed keyed order',[col('observation_id','string','identifier'),col('label','integer','categorical','Binary target event label, 0 or 1; no arithmetic measurement.'),col('observation_timestamp','datetime'),col('availability_timestamp','datetime')],[['B',0,(t0+timedelta(hours=1)).isoformat(),(boundary+timedelta(hours=1)).isoformat()],['A',1,t0.isoformat(),boundary.isoformat()]],'Join by observation_id, not row position. Matched observation timestamps must agree; labels must be binary and available by the supplied audit cutoff. Later label availability does not permit using a label as a prediction-time feature.')
variant(labels,'duplicate_id',[{'op':'duplicate_row','where':{'observation_id':'A'},'insert':'end'}],[issue('duplicate_label','duplicate_row',{'observation_id':'A'},'observation_id','Second competing label record for A.',1)])
variant(labels,'missing_label',[{'op':'drop_rows','where':{'observation_id':'A'}}])
variant(labels,'orphan_label',[cell({'observation_id':'B'},'observation_id','C')])
variant(labels,'invalid_label',[cell({'observation_id':'A'},'label',2)],[issue('invalid_label','other',{'observation_id':'A'},'label','Declared binary label is neither zero nor one.',rule=rule('label','gt',1))])
variant(labels,'misaligned_timestamp',[cell({'observation_id':'A'},'observation_timestamp',(t0+timedelta(minutes=1)).isoformat())])
variant(labels,'unavailable_label',[cell({'observation_id':'A'},'availability_timestamp',(boundary+timedelta(days=1)).isoformat())])
group=ds('group_orders','Separate group evaluation fixture',[col('order_key','string','identifier'),col('customer_group','string','identifier'),col('target','integer','categorical')],[['A','G1',1],['B','G1',0],['C','G2',1]])
time=ds('time_orders','Separate later-order evaluation fixture',[col('order_key','string','identifier'),col('observation_timestamp','datetime'),col('target','integer','categorical')],[[f'T{i+1}',(t0+timedelta(days=i-3)).isoformat(),int(i>=3 and i<7)] for i in range(13)],'Cutoff is 2025-01-01T09:00:00. Training timestamp < cutoff; evaluation cutoff <= timestamp < cutoff + 10 days. Evaluation has four events among ten rows, independently of other fixtures.')
train_dist=[matrix[0][0],matrix[-1][0]]
imp=ds('imputation_train','Training distance with missing entry',[col('distance','number')],[[v] for v in train_dist]+[[None]])
variant(imp,'observed_only',[{'op':'drop_rows','where':{'distance':None}}])
impv=ds('imputation_validation','Validation distances; do not fit',[col('distance','number')],[[hi],[None]])
variant(impv,'one_missing',[{'op':'drop_rows','where':{'distance':hi}}])
scale=ds('scaling_train','Distance and constant feature for scaling',[col('distance','number'),col('constant_feature','number')],[[v,10] for v in train_dist])
scalev=ds('scaling_validation','Scaling validation input',[col('distance','number'),col('constant_feature','number')],[[train_dist[-1]+(train_dist[-1]-train_dist[0])/2,10]])
cat=ds('zone_train','Training-only zone categories',[col('zone')],[['north'],['south']])
variant(cat,'missing_seen_at_fit',[{'op':'duplicate_row','where':{'zone':'south'},'insert':'end'},cell({'zone':'south'},'zone',None,1)],purpose='Missing is intentionally present during fit; not automatically a defect.')
case=ds('zone_cases','Known, unseen and missing zone cases',[col('zone')],[['north'],['east'],[None]])
records=ds('feature_records','Timestamp-bounded sum records',[col('available_at','datetime'),col('value','integer')],[[t0.isoformat(),matrix[0][0]],[boundary.isoformat(),matrix[1][0]-1]])
later_value=number('leakage_safe_features',r'later record with value (\d+)')
variant(records,'later_record',[{'op':'duplicate_row','where':{'available_at':t0.isoformat()},'insert':'end'},cell({'available_at':t0.isoformat()},'available_at',(boundary+timedelta(seconds=1)).isoformat(),1),cell({'available_at':(boundary+timedelta(seconds=1)).isoformat()},'value',later_value)],purpose='Append post-boundary information; earlier feature must be invariant.')
audit=ds('audit_sample','Dummy permitted/restricted diagnostic fields',[col('run_id','string','identifier'),col('row_count','integer'),col('token','string','pii'),col('raw_customer_values','string','pii')],[['run_fixture',len(orders['rows']),'DUMMY_TOKEN_NOT_A_CREDENTIAL','DUMMY_CUSTOMER_NOT_A_PERSON']], 'Dummy restricted values only. Existing policy permits run_id and row_count only; neither token nor raw customer values may appear in generated records or captured output.')
# Register dataset CSVs; compute all hashes and file metadata from bytes.
sys.path.insert(0,str(ROOT/'00_FINAL_PIPELINE_CORE/scripts'))
from checkers.dataset import resolve_dataset
import hashlib
(B/'assets').mkdir(exist_ok=True)
for a in reg['assets']:
 if a['asset_kind']!='dataset':continue
 s=io.StringIO(newline='');w=csv.writer(s);w.writerow([c['name'] for c in a['columns']]);w.writerows(a['rows']);data=s.getvalue().encode()
 filename='orders-b.csv' if a['asset_id']==orders['asset_id'] else a['asset_id']+'.csv'
 path=B/'assets'/filename;path.write_bytes(data)
 a['data_file']={'uri':'assets/'+filename,'format':'csv','sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}
# Each live-code anchor receives its own unimplemented workspace, fixtures and
# verbatim authoring contract. No completed learner function or answer is supplied.
def rows(a,v=None):return resolve_dataset(reg,a['asset_id'],v)[1]
def table(a,v=None):
 c,r=resolve_dataset(reg,a['asset_id'],v)
 return {'columns':[x['name'] for x in c],'rows':[[row[x['name']] for x in c] for row in r]}
fixtures={
 'numpy_shape_dtype':{'contract':{'feature_count':len(matrix[0]),'min_batch':1,'max_batch':len(matrix)},'valid':matrix,'tuple_boundary':((matrix[0][0],matrix[0][1]),),'empty':[],'flat':flat,'wrong_width':[[r[0]] for r in matrix],'too_many':matrix+[matrix[0]]},
 'numpy_dtype_selection':{'a':dtype_rows,'candidate_dtypes':['float'+str(w*8) for w in dtype_widths],'boundary_values':[1.25,1.0,16777217.0],'tolerance':0.0,'element_storage_budget':len(flat)*min(dtype_widths),'integer_cast_probe':{'reference':[1.25],'candidate_dtype':'int64'},'policy_note':'Tolerance and budget are supplied illustrative policy; byte saving alone never establishes acceptance.'},
 'numpy_vectorization':{'matrix':matrix,'feature_references':ref,'expected_shape':(len(matrix),len(matrix[0])),'broadcast_column':[[r[0]] for r in matrix],'broadcast_row':[ref],'rtol':1e-7,'atol':1e-9},
 'file_object_ingestion':{'bucket':'authorized-fixture-bucket','prefix':'approved/','object_names':['orders-a.csv','orders-b.csv'],'intended_object':'orders-b.csv','local_path':'orders-b.csv','identity_record_path':'identity.txt','declared_types':{'order_key':'string','distance':'float64','zone':'string','eventual_arrival':'string'},'expected_columns':[c['name'] for c in orders['columns']],'expected_row_count':len(orders['rows']),'expected_order_key':key,'access_pattern':'Read complete named CSV; a separately declared Parquet task would allow selected columns.'},
 'chunked_ingestion':{'path':chunk['asset_id']+'.csv','declared_types':{c['name']:'float64' for c in chunk['columns']},'array_budget':budget,'feature_count':feature_width,'element_width':width},
 'dataset_inspection':{'fixture':table(features),'feature_columns':[c['name'] for c in features['columns']],'ddof':0,'boundary':{'columns':[c['name'] for c in features['columns']],'rows':[matrix[0]]}},
 'dataset_schema_validation':{'contract':{'columns':['distance','zone'],'declared_types':{'distance':'float64','zone':'string'},'distance_min':lo,'distance_max':hi,'zone_categories':['north','south']},'valid':table(schema),'negative':table(schema,'negative_distance'),'too_large':table(schema,'over_upper_bound'),'missing_column':table(schema,'missing_zone_column'),'invalid_representation':table(schema,'invalid_zone'),'unexpected_column':{'columns':[c['name'] for c in schema['columns']]+['extra_feature'],'rows':[r+[matrix[0][1]] for r in schema['rows']]}},
 'dataset_cleaning_policy':{'records':rows(clean,'policy_defects'),'valid':rows(clean),'policy':{'repeat_accepted_key':'reject','zone_repairs':{'South':'south'},'distance_min':lo,'distance_max':hi,'invalid_distance':'reject'},'connection':'authorized local fixture only'},
 'dataset_selection_bias':{'sample_counts':{'zone-A':sample_A,'zone-B':sample_B},'target_counts':{'zone-A':target_A,'zone-B':target_B},'numeric_values':[[r[0]] for r in matrix],'ddof':0},
 'label_integrity':{'observations':rows(obs),'labels':rows(labels),'cases':{v['variant_id']:rows(labels,v['variant_id']) for v in labels['variants']},'contract':{'label_values':[0,1],'require_matching_observation_timestamp':True,'availability_cutoff':(boundary+timedelta(hours=1)).isoformat(),'availability_boundary_inclusive':True}},
 'deployment_matched_splits':{'group_records':rows(group),'training_groups':['G1'],'validation_groups':['G2'],'invalid_training_keys':['A'],'invalid_validation_keys':['B','C'],'time_records':rows(time),'cutoff':t0.isoformat(),'evaluation_end':(t0+timedelta(days=10)).isoformat(),'time_policy':'training < cutoff; cutoff <= evaluation < evaluation_end'},
 'training_fitted_imputation':{'X_train':table(imp)['rows'],'numeric_values':[[v] for v in train_dist],'X_validation':table(impv)['rows'],'boundary_missing':[[None]],'declared_strategy':'mean','incorrect_replacement':train_dist[0]},
 'training_fitted_scaling':{'X_train':table(scale)['rows'],'X_validation':table(scalev)['rows'],'with_mean':True,'with_std':True,'ddof':0,'incorrect_transformed_fixture':[[0,1]]},
 'categorical_encoding':{'X_train':table(cat)['rows'],'X_train_missing':table(cat,'missing_seen_at_fit')['rows'],'feature_name':'zone','cases':{str(r[0]):[r] for r in case['rows']},'unknown_policies':['error','ignore'],'missing_marker':'Replace JSON null with np.nan when constructing the supplied arrays.'},
 'preprocessing_pipeline':{'X_train':rows(schema),'y_train':[0,0,1],'X_validation':[{'distance':matrix[1][0],'zone':'north'},{'distance':None,'zone':'south'}],'malformed':[{'distance':matrix[0][0]}],'numerical_policy':'SimpleImputer(strategy="mean") then StandardScaler(with_mean=True, with_std=True)','categorical_policy':'OneHotEncoder(handle_unknown="ignore")','estimator':'supplied deterministic fixture estimator; not a model-selection exercise'},
 'prediction_boundary_leakage':{'training':rows(orders)[:3],'held_out':rows(orders)[3:],'permitted_features':['distance','zone'],'future_field':'eventual_arrival','prediction_time':'acceptance','failure_fit_rows':rows(orders),'failure_features':['distance','zone','eventual_arrival']},
 'leakage_safe_features':{'records':rows(records),'augmented_records':rows(records,'later_record'),'prediction_time':boundary.isoformat(),'empty':[],'policy':'available_at <= prediction_time; timestamps are ISO strings converted with datetime.fromisoformat'},
 'sensitive_ml_assets':{'sample':rows(audit)[0],'permitted_fields':['run_id','row_count'],'authorized_identity':'fixture_reader','unauthorized_identity':'fixture_other','policy':'Only fixture_reader may read sample; permission denial raises PermissionError. No restricted value in returned record or stdout.','runtime_secret_name':'fixture_token'}
}
mounts={
 'numpy_shape_dtype':[features], 'numpy_dtype_selection':[dtype_ds], 'numpy_vectorization':[features], 'file_object_ingestion':[orders], 'chunked_ingestion':[chunk], 'dataset_inspection':[features], 'dataset_schema_validation':[schema,features], 'dataset_cleaning_policy':[clean], 'dataset_selection_bias':[selection_counts,features], 'label_integrity':[obs,labels], 'deployment_matched_splits':[group,time], 'training_fitted_imputation':[imp,impv], 'training_fitted_scaling':[scale,scalev], 'categorical_encoding':[cat,case], 'preprocessing_pipeline':[schema], 'prediction_boundary_leakage':[orders], 'leakage_safe_features':[records], 'sensitive_ml_assets':[audit]
}
# Offline ingestion stub mirrors only authorized object listing and downloading.
local_runtime='''from pathlib import Path
import shutil
class FixtureS3:
    def list_objects_v2(self, Bucket, Prefix):
        if Bucket != 'authorized-fixture-bucket' or Prefix != 'approved/':
            raise PermissionError('Outside approved fixture scope')
        return {'Contents': [{'Key': Prefix + name} for name in ('orders-a.csv', 'orders-b.csv')]}
    def download_file(self, Bucket, Key, Filename):
        if Bucket != 'authorized-fixture-bucket' or Key not in ('approved/orders-a.csv','approved/orders-b.csv'):
            raise PermissionError('Outside approved fixture scope')
        source = Path('objects') / Key
        shutil.copyfile(source, Filename)
'''
secret_runtime='''_SECRET = 'DUMMY_RUNTIME_SECRET_NOT_A_CREDENTIAL'
def read_sample(identity, sample):
    if identity != 'fixture_reader':
        raise PermissionError('Unauthorized fixture identity')
    return dict(sample)
def use_secret(identity, secret_name):
    if identity != 'fixture_reader' or secret_name != 'fixture_token':
        raise PermissionError('Unauthorized fixture secret use')
    return bool(_SECRET)  # Use the authorized dummy without disclosing its literal.
'''
# Trace-only infrastructure, not learner preprocessing or leakage correction.
trace_runtime='''class TracePreprocessor:
    def __init__(self):
        self.fit_rows = []
        self.transform_rows = []
    def fit(self, rows):
        self.fit_rows = [dict(r) for r in rows]
        return self
    def transform(self, rows):
        self.transform_rows.append([dict(r) for r in rows])
        return rows
class TracePredictor:
    def __init__(self):
        self.input_rows = []
    def predict(self, rows):
        self.input_rows.append([dict(r) for r in rows])
        return [0 for _ in rows]
'''
estimator_runtime='''import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
class FixtureEstimator(ClassifierMixin, BaseEstimator):
    def fit(self, X, y):
        self.n_features_in_ = X.shape[1]
        self.classes_ = np.unique(y)
        return self
    def predict(self, X):
        if X.shape[1] != self.n_features_in_:
            raise ValueError('Fixture width changed')
        return np.zeros(X.shape[0], dtype=int)
'''
coverage=[]
for k,b in bundles.items():
 mounted=mounts.get(k,[])
 if b['practice_anchor']['type']!='live_code':
  coverage.append({'concept_id':b['context']['concept_id'],'asset_ids':[task['asset_id'],counts['asset_id']]});continue
 f=fixtures[k]
 readme='\n\n'.join([b['context']['concept_name'], 'Independent fictional fixture; supplied policies are not general real-world facts.', 'Practice contract:\n'+json.dumps(b['practice_anchor'],ensure_ascii=False,indent=2), 'Visual contract:\n'+json.dumps(b['visual_anchor'],ensure_ascii=False,indent=2), 'Mounted registered datasets:\n'+'\n'.join(a['asset_id']+' -> '+Path(a['data_file']['uri']).name for a in mounted), 'fixtures.py supplies in-memory fixtures only. Learner writes imports, function and assertions in learner.py. JSON null means missing: use np.nan for NumPy/sklearn examples. Timestamp strings are converted with datetime.fromisoformat when datetime objects are needed.'])
 files=[{'path':'README.md','content':readme},{'path':'fixtures.json','content':json.dumps(f,ensure_ascii=False,indent=2)},{'path':'fixtures.py','content':'# Authored fixtures only; no learner solution.\nFIXTURES = '+pprint.pformat(f,sort_dicts=False)+'\n'},{'path':'learner.py','content':'# Write the imports, parameterized function, and assertions required by README.md.\n'}]
 for a in mounted: files.append({'path':Path(a['data_file']['uri']).name,'content':(B/a['data_file']['uri']).read_text()})
 if k=='file_object_ingestion':
  content=(B/orders['data_file']['uri']).read_text()
  for name in f['object_names']:
   files.append({'path':'objects/approved/'+name,'content':content if name==f['intended_object'] else content.splitlines()[0]+'\n'+content.splitlines()[2]+'\n'})
  files.append({'path':'authorized_runtime.py','content':local_runtime})
  files.append({'path':'boto3.py','content':'from authorized_runtime import FixtureS3\ndef client(service):\n    if service != "s3":\n        raise PermissionError("Only fixture S3 is authorized")\n    return FixtureS3()\n'})
 if k=='sensitive_ml_assets':files.append({'path':'authorized_runtime.py','content':secret_runtime})
 if k=='prediction_boundary_leakage':files.append({'path':'authorized_runtime.py','content':trace_runtime})
 if k=='preprocessing_pipeline':files.append({'path':'authorized_runtime.py','content':estimator_runtime})
 a={'asset_id':'ws.'+k,'asset_kind':'code_workspace','scenario_id':scenario,'title':b['context']['concept_name']+' — unimplemented fixture workspace','runtime':'python','files':files}
 reg['assets'].append(a)
 coverage.append({'concept_id':b['context']['concept_id'],'asset_ids':[a['asset_id']]+[x['asset_id'] for x in mounted]})
(B/'scenario_asset_registry.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
(B/'working/asset_coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
print('scenarios',len(reg['scenarios']),'datasets',sum(a['asset_kind']=='dataset' for a in reg['assets']),'workspaces',sum(a['asset_kind']=='code_workspace' for a in reg['assets']),'concepts',len(coverage))
