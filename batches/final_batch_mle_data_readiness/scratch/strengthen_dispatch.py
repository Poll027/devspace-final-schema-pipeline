import json,sys,copy
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts');from checkers import sandbox
b=Path('batches/final_batch_mle.region.data_readiness');p=b/'interactions.json';d=json.loads(p.read_text());r=json.loads((b/'scenario_asset_registry.json').read_text());assets={a['asset_id']:a for a in r['assets']}
xs={i['interaction']['anchors'][0].split('#')[0].split('.',1)[1]:i['interaction'] for t in d['tiles'] for i in t['interactions'] if i['interaction']['anchors']}
def fixture(short):return json.loads(next(f['content'] for f in assets['ws.'+short]['files'] if f['path']=='fixtures.json'))
ix=xs['chunked_ingestion'];f=fixture('chunked_ingestion');budget=len(assets['ds.chunked_orders']['rows'])*f['feature_count']*f['element_width']+f['feature_count']*f['element_width']
t=copy.deepcopy(ix['grading']['tests'][0]);t.update(test_id='short_whole_file',visible=False);t['spec']['args'][2]=budget;t['spec']['expected']=None;ix['grading']['tests'].append(t)
ix=xs['dataset_selection_bias'];ix['public']['prompt'] += ' Use this exact supported limitation sentence in the result: Zone B has lower inclusion and sample share than its target share; the counts establish neither a cause nor inevitable prediction failure.'
ix=xs['label_integrity'];f=fixture('label_integrity');t=copy.deepcopy(ix['grading']['tests'][0]);t.update(test_id='repeated_observation',visible=False);t['spec']['args'][0]=f['observations']+[f['observations'][0]];t['spec']['expected']=None;ix['grading']['tests'].append(t)
ix=xs['numpy_shape_dtype'];f=fixture('numpy_shape_dtype')
helper="\ndef validation_outcome(fixture):\n    try:\n        return {'accepted': True, 'array':validate(fixture)}\n    except ValueError:\n        return {'accepted':False}\n"
for c in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:c['content']=c['content'].replace('boundary = ((2, 10),)','boundary = '+repr(tuple(tuple(row) for row in f['tuple_boundary'])))+helper
for key in ['empty','flat','wrong_width','too_many']:
 ix['grading']['tests'].append({'test_id':key,'kind':'function_call','spec':{'function':'validation_outcome','args':[f[key]],'expected':None},'visible':False,'message_on_fail':'The declared invalid boundary must reject with ValueError.'})
# Enrich the inline judgement with real pinned-engine representations and outcomes.
f=fixture('preprocessing_pipeline');ix=xs['preprocessing_pipeline']
code='''import json
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.dummy import DummyRegressor
FIXTURES = json.loads('''+repr(json.dumps(f))+''')
X_train = pd.DataFrame(FIXTURES['X_train'])
y_train = FIXTURES['y_train']
X_validation = pd.DataFrame(FIXTURES['X_validation'])
bounded = pd.DataFrame([FIXTURES['X_validation'][0]])
malformed = pd.DataFrame(FIXTURES['malformed'])
# Supplied deterministic fixture estimator, not a model-selection decision:
estimator = DummyRegressor(strategy='mean')
numeric = Pipeline([('impute', SimpleImputer(strategy='mean')),
                    ('scale', StandardScaler(with_mean=True,with_std=True))])
prep = ColumnTransformer([('numeric',numeric,['distance']),
                         ('zone',OneHotEncoder(handle_unknown='ignore',sparse_output=False),['zone'])])
workflow = Pipeline([('preprocessing',prep),('estimator',estimator)])
workflow.fit(X_train,y_train)
mean_before = prep.named_transformers_['numeric'].named_steps['impute'].statistics_.copy()
scale_before = prep.named_transformers_['numeric'].named_steps['scale'].scale_.copy()
representation = prep.transform(X_validation)
outputs = workflow.predict(X_validation)
bounded_outputs = workflow.predict(bounded)
assert np.array_equal(mean_before,prep.named_transformers_['numeric'].named_steps['impute'].statistics_)
assert np.array_equal(scale_before,prep.named_transformers_['numeric'].named_steps['scale'].scale_)
try:
    workflow.predict(malformed)
    assert False
except ValueError as error:
    malformed_outcome = type(error).__name__ + ': ' + str(error)
missing_outputs = workflow.predict(X_validation.iloc[[1]])
result = {'representation':representation.tolist(),'outputs':outputs.tolist(),'bounded_outputs':bounded_outputs.tolist(),'missing_outputs':missing_outputs.tolist(),'training_imputation':mean_before.tolist(),'training_scale':scale_before.tolist(),'malformed_outcome':malformed_outcome}
'''
job=sandbox._py_job('python',['numpy','pandas','scikit-learn'],[sandbox._py_script('excerpt','excerpt.py',code,[],[{'id':'result','kind':'expr','expr':'result'}])]);out=sandbox.node_run(job,sandbox.RUNTIMES['python']['runner'])['results']['excerpt']
(b/'scratch/pipeline_excerpt_execution.json').write_text(json.dumps(out,indent=2));assert out['ok'],out
observed=out['probes']['result']['value'];assert out['probes']['result']['ok']
ix['public']['items'][0]['text']=code+'\n# Observed fixture evidence (pinned runtime):\n'+json.dumps(observed,indent=2)
ix['public']['items'][2]['text']='From the supplied training-fitted workflow:\n'+json.dumps({k:observed[k] for k in ['representation','outputs','training_imputation','training_scale']},indent=2)+'\n# The supplied representation and output equality predicates pass.\n# mean_before and scale_before compare equal after transform and predict; no refit occurs.'
ix['public']['items'][3]['text']='Missing-distance case '+json.dumps(f['X_validation'][1])+':\nmissing_predictions = workflow.predict(X_validation.iloc[[1]])\n# Observed output: '+json.dumps(observed['missing_outputs'])+'\n# The supplied missing-case outcome equality predicate passes.'
ix['public']['items'][4]['text']='Malformed input '+json.dumps(f['malformed'])+':\ntry:\n    workflow.predict(malformed)\n    assert False\nexcept ValueError:\n    pass\n# Observed failure: '+observed['malformed_outcome']
p.write_text(json.dumps(d,indent=2)+'\n')
